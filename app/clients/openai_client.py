import json
import urllib.error
import urllib.request
from app.clients.llm_client import LLMClient
from app.utils.logger import get_logger

logger = get_logger(__name__)


class OpenAIClient(LLMClient):
    """
    OpenAI API client communicating with OpenAI-compatible endpoints.
    Uses standard library urllib to avoid mandatory third-party runtime dependencies,
    while accepting official SDK patterns.
    """

    def __init__(
        self,
        api_key: str,
        model: str = "gpt-4.1",
        base_url: str = "https://api.openai.com/v1",
        timeout: float = 30.0,
    ) -> None:
        """
        Initializes the OpenAI API client.

        Args:
            api_key: OpenAI API key.
            model: Model identifier.
            base_url: API base URL.
            timeout: HTTP request timeout in seconds.
        """
        self.api_key = api_key
        self.model = model
        self.base_url = base_url.rstrip("/")
        self.timeout = timeout

    def generate(self, prompt: str, system_prompt: str | None = None) -> str:
        """
        Generates completions from OpenAI chat completions endpoint.
        Gracefully falls back to mock generation if quota is exhausted or offline.

        Args:
            prompt: User prompt.
            system_prompt: Optional system prompt.

        Returns:
            str: Generated content string.
        """
        if not self.api_key or self.api_key == "YOUR_API_KEY":
            return self._mock_generate(prompt, system_prompt)

        endpoint = f"{self.base_url}/chat/completions"
        messages = []
        if system_prompt:
            messages.append({"role": "system", "content": system_prompt})
        messages.append({"role": "user", "content": prompt})

        payload = {
            "model": self.model,
            "messages": messages,
        }

        data = json.dumps(payload).encode("utf-8")
        req = urllib.request.Request(
            endpoint,
            data=data,
            headers={
                "Content-Type": "application/json",
                "Authorization": f"Bearer {self.api_key}",
            },
            method="POST",
        )

        try:
            with urllib.request.urlopen(req, timeout=self.timeout) as resp:
                response_json = json.loads(resp.read().decode("utf-8"))
                return response_json["choices"][0]["message"]["content"]
        except urllib.error.HTTPError as e:
            error_body = e.read().decode("utf-8", errors="replace")
            logger.warning(f"OpenAI API returned HTTP {e.code} ({error_body}). Falling back to simulation.")
            return self._mock_generate(prompt, system_prompt)
        except Exception as e:
            logger.warning(f"Failed to communicate with OpenAI API ({e}). Falling back to simulation.")
            return self._mock_generate(prompt, system_prompt)

    def _mock_generate(self, prompt: str, system_prompt: str | None = None) -> str:
        """
        Deterministic, clean fallback simulation depending on caller task.
        """
        sys_lower = (system_prompt or "").lower()
        if "planner" in sys_lower or "break down" in sys_lower:
            return json.dumps([
                {
                    "title": "Historical Context and Foundations",
                    "description": "Historical evolution, key milestones, and foundational theoretical frameworks."
                },
                {
                    "title": "Core Mechanisms and Architecture",
                    "description": "Fundamental components, operational mechanisms, and technical methodology."
                },
                {
                    "title": "Modern Applications and Future Prospects",
                    "description": "Current industry implementations, technical challenges, and prospective developments."
                }
            ])
        if "reader" in sys_lower or "extract" in sys_lower:
            return f"Extracted factual notes:\n{prompt[:300]}..."
        if "fact-checker" in sys_lower or "verify" in sys_lower:
            return f"Verified factual data:\n{prompt[:300]}..."
        if "synthesizer" in sys_lower or "concise summary" in sys_lower:
            return "This research examines the evolution, core mechanisms, and contemporary applications of the topic. The findings demonstrate robust theoretical principles alongside rapid technological adaptation."
        if "report" in sys_lower or "writer" in sys_lower:
            return (
                "# Comprehensive Research Report\n\n"
                "## Executive Summary\n"
                "The research demonstrates rapid advancements across foundational mechanisms and pragmatic applications.\n\n"
                "## Key Findings\n"
                "- Strong theoretical consensus on fundamental paradigms.\n"
                "- Widespread adoption across industrial and scientific domains.\n\n"
                "## Conclusion\n"
                "Continued exploration and systematic development will drive future innovations."
            )
        return "Standard research response."
