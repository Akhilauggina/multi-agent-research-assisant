from app.clients.llm_client import LLMClient
from app.utils.logger import get_logger

logger = get_logger(__name__)


class LLMService:
    """
    Service responsible for coordinating calls to LLM clients.
    Decoupled from specific provider implementations via the LLMClient interface.
    """

    def __init__(
        self,
        llm_client: LLMClient,
        max_retries: int = 3,
    ) -> None:
        """
        Initializes the LLMService.

        Args:
            llm_client: Injected LLMClient implementation.
            max_retries: Maximum retry attempts for LLM calls.
        """
        self.client = llm_client
        self.max_retries = max_retries

    def generate(self, prompt: str, system_prompt: str | None = None) -> str:
        """
        Delegates text generation to the underlying LLM client with retries.

        Args:
            prompt: User/instruction prompt.
            system_prompt: Optional system prompt.

        Returns:
            str: Generated text response.

        Raises:
            RuntimeError: If all retry attempts fail.
        """
        last_error = None
        for attempt in range(1, self.max_retries + 1):
            try:
                return self.client.generate(prompt, system_prompt=system_prompt)
            except Exception as e:
                last_error = e
                logger.warning(f"LLM generation attempt {attempt}/{self.max_retries} failed: {e}")

        logger.error(f"All {self.max_retries} attempts failed in LLMService.")
        raise RuntimeError(f"LLMService failed to generate response: {last_error}") from last_error


    def generate(self, prompt: str, system_prompt: str | None = None) -> str:
        """
        Delegates text generation to the underlying LLM client with retries.

        Args:
            prompt: User/instruction prompt.
            system_prompt: Optional system prompt.

        Returns:
            str: Generated text response.

        Raises:
            RuntimeError: If all retry attempts fail.
        """
        last_error = None
        for attempt in range(1, self.max_retries + 1):
            try:
                return self.client.generate(prompt, system_prompt=system_prompt)
            except Exception as e:
                last_error = e
                logger.warning(f"LLM generation attempt {attempt}/{self.max_retries} failed: {e}")

        logger.error(f"All {self.max_retries} attempts failed in LLMService.")
        raise RuntimeError(f"LLMService failed to generate response: {last_error}") from last_error
        self.max_retries = max_retries