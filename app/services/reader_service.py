from typing import Any
from app.models.responses.wikipedia_response import WikipediaResponse
from app.models.tool_result import ToolResult
from app.services.llm_service import LLMService
from app.utils.logger import get_logger

logger = get_logger(__name__)


class ReaderService:
    """
    Service responsible for reading, extracting, and cleaning important information
    from raw search results.
    Delegates extraction to LLMService or parses structured content.
    Does NOT summarize or verify facts.
    """

    def __init__(self, llm_service: LLMService) -> None:
        """
        Initializes ReaderService with an injected LLMService.

        Args:
            llm_service: Injected LLMService instance.
        """
        self.llm_service = llm_service

    def read_and_extract(self, section_title: str, results: list[ToolResult]) -> str:
        """
        Extracts salient, useful factual content from tool results for a given section.

        Args:
            section_title: Title of the research section.
            results: List of tool results retrieved for this section.

        Returns:
            str: Cleaned, extracted content text.
        """
        extracted_texts: list[str] = []

        for res in results:
            if not res.success or not res.content:
                continue

            content = res.content
            if isinstance(content, WikipediaResponse):
                extracted_texts.append(f"Title: {content.title}\n{content.summary}")
            elif isinstance(content, dict):
                summary = content.get("summary") or content.get("text") or content.get("content") or str(content)
                extracted_texts.append(summary)
            else:
                extracted_texts.append(str(content))

        if not extracted_texts:
            logger.warning(f"No successful content found to read for section '{section_title}'.")
            return f"No relevant content could be extracted for section: {section_title}."

        raw_combined = "\n\n".join(extracted_texts)

        system_prompt = (
            "You are an expert research reader. Your job is ONLY to extract and clean "
            "important, relevant facts and information from raw search results for the given section. "
            "Do NOT summarize, do NOT verify facts, and do NOT alter the original meaning. "
            "Filter out boilerplate, errors, and noise. Return only clean informative text."
        )

        user_prompt = f"Section: {section_title}\n\nRaw Search Content:\n{raw_combined}"

        try:
            cleaned = self.llm_service.generate(prompt=user_prompt, system_prompt=system_prompt)
            return cleaned.strip()
        except Exception as e:
            logger.warning(f"LLM extraction fallback for section '{section_title}': {e}")
            return raw_combined.strip()

