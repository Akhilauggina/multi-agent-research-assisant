from abc import ABC, abstractmethod


class LLMClient(ABC):
    """
    Abstract base class defining the contract for LLM provider clients.
    """

    @abstractmethod
    def generate(self, prompt: str, system_prompt: str | None = None) -> str:
        """
        Sends a generation request to the LLM and returns the textual response.

        Args:
            prompt: User or task prompt.
            system_prompt: Optional system instruction prompt.

        Returns:
            str: Generated text response.

        Raises:
            Exception: If API communication or response parsing fails.
        """
        pass

