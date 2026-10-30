from app.services.llm_service import LLMService
from app.utils.logger import get_logger

logger = get_logger(__name__)


class FactCheckingService:
    """
    Service responsible for verifying claims and factual consistency in read results.
    Delegates validation analysis to LLMService.
    Produces verified content strings for sections.
    """

    def __init__(self, llm_service: LLMService) -> None:
        """
        Initializes FactCheckingService with an injected LLMService.

        Args:
            llm_service: Injected LLMService instance.
        """
        self.llm_service = llm_service

    def verify_section(self, section_title: str, text: str) -> str:
        """
        Performs factual consistency check and returns verified content for the section.

        Args:
            section_title: Title of the research section.
            text: Raw extracted content from the Reader service.

        Returns:
            str: Verified factual text.
        """
        if not text or not text.strip():
            return "No content available for factual verification."

        system_prompt = (
            "You are a rigorous research fact-checker. Review the provided section notes. "
            "Verify factual statements, eliminate unsupported or contradictory claims, "
            "and retain only substantiated, factual information. "
            "Return the verified content cleanly as plain factual text."
        )

        user_prompt = f"Section: {section_title}\n\nCandidate Text:\n{text}"

        try:
            verified = self.llm_service.generate(prompt=user_prompt, system_prompt=system_prompt)
            return verified.strip()
        except Exception as e:
            logger.warning(f"Fact-checking fallback for section '{section_title}': {e}")
            return text.strip()

