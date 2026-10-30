from app.services.llm_service import LLMService
from app.utils.logger import get_logger

logger = get_logger(__name__)


class WriterService:
    """
    Service responsible for transforming the final synthesized summary and verified sections
    into a structured, professional research report formatted strictly in Markdown.
    """

    def __init__(self, llm_service: LLMService) -> None:
        """
        Initializes WriterService with an injected LLMService.

        Args:
            llm_service: Injected LLMService instance.
        """
        self.llm_service = llm_service

    def generate_report(
        self,
        topic: str,
        final_summary: str,
        verified_results: dict[str, str] | None = None,
    ) -> str:
        """
        Generates a comprehensive research report in Markdown.

        Args:
            topic: Research topic.
            final_summary: Synthesized summary text.
            verified_results: Optional section breakdown for detailed context.

        Returns:
            str: Full research report formatted in clean Markdown.
        """
        section_context = ""
        if verified_results:
            section_context = "\n\nDetailed Section Notes:\n" + "\n\n".join(
                f"### {title}\n{text}" for title, text in verified_results.items()
            )

        system_prompt = (
            "You are a Senior Research Analyst and Technical Writer. "
            "Write an extensive, well-structured, production-quality research report "
            "formatted strictly in standard Markdown. "
            "Include: Title, Executive Summary, Key Findings, Section-by-Section Analysis, "
            "and Conclusion. Do NOT output binary formats like PDF or DOCX."
        )

        user_prompt = (
            f"Topic: {topic}\n\n"
            f"Synthesized Summary:\n{final_summary}"
            f"{section_context}"
        )

        try:
            report_md = self.llm_service.generate(prompt=user_prompt, system_prompt=system_prompt)
            return report_md.strip()
        except Exception as e:
            logger.warning(f"WriterService fallback: {e}")
            lines = [
                f"# Research Report: {topic}",
                "",
                "## Executive Summary",
                final_summary,
                "",
                "## Detailed Findings",
            ]
            if verified_results:
                for title, text in verified_results.items():
                    lines.append(f"### {title}")
                    lines.append(text)
                    lines.append("")
            lines.append("## Conclusion")
            lines.append(f"Research completed successfully for topic '{topic}'.")
            return "\n".join(lines)

