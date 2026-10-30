from app.services.llm_service import LLMService
from app.utils.logger import get_logger

logger = get_logger(__name__)


class SummarizationService:
    """
    Service responsible for consolidating verified section results into one concise summary.
    Does NOT generate markdown formatting or final reports.
    """

    def __init__(self, llm_service: LLMService) -> None:
        """
        Initializes SummarizationService with an injected LLMService.

        Args:
            llm_service: Injected LLMService instance.
        """
        self.llm_service = llm_service

    def summarize_results(self, topic: str, verified_results: dict[str, str]) -> str:
        """
        Combines all verified sections into one cohesive, concise summary text.

        Args:
            topic: Research topic.
            verified_results: Dictionary of section title -> verified text.

        Returns:
            str: Single consolidated summary (plain text).
        """
        if not verified_results:
            return f"No verified information available to summarize for {topic}."

        sections_text = "\n\n".join(
            f"=== {title} ===\n{content}" for title, content in verified_results.items()
        )

        system_prompt = (
            "You are an expert research synthesizer. Combine the provided verified section notes "
            "into a single, unified, concise summary of the entire research topic. "
            "Do NOT generate markdown headers, bullet lists, or report structures. "
            "Produce only clear, concise, well-structured synthesis paragraphs."
        )

        user_prompt = f"Topic: {topic}\n\nVerified Sections:\n{sections_text}"

        try:
            summary = self.llm_service.generate(prompt=user_prompt, system_prompt=system_prompt)
            return summary.strip()
        except Exception as e:
            logger.warning(f"Summarization fallback: {e}")
            return f"Summary of research on {topic}:\n" + "\n".join(
                f"- {title}: {content[:150]}..." for title, content in verified_results.items()
            )

