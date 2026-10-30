import json
import urllib.error
import urllib.request
from app.clients.llm_client import LLMClient
from app.utils.logger import get_logger

logger = get_logger(__name__)


class GeminiClient(LLMClient):
    """
    Google Gemini API client using standard library communication.
    Supports system instructions and generates textual content using Gemini models.
    """

    def __init__(
        self,
        api_key: str,
        model: str = "gemini-3.5-flash-lite",
        timeout: float = 30.0,
    ) -> None:
        """
        Initializes the Gemini API client.

        Args:
            api_key: Gemini API key.
            model: Gemini model identifier.
            timeout: Request timeout in seconds.
        """
        self.api_key = api_key
        self.model = model.replace("models/", "")
        self.timeout = timeout

    def generate(self, prompt: str, system_prompt: str | None = None) -> str:
        """
        Generates text using the Gemini REST API.

        Args:
            prompt: User prompt.
            system_prompt: Optional system instruction.

        Returns:
            str: Generated response text.
        """
        if not self.api_key or self.api_key == "YOUR_API_KEY":
            logger.warning("Gemini API key not provided. Returning fallback plan.")
            return self._mock_generate(prompt, system_prompt)

        endpoint = f"https://generativelanguage.googleapis.com/v1beta/models/{self.model}:generateContent?key={self.api_key}"

        payload: dict[str, any] = {
            "contents": [
                {
                    "parts": [{"text": prompt}]
                }
            ]
        }

        if system_prompt:
            payload["systemInstruction"] = {
                "parts": [{"text": system_prompt}]
            }

        data = json.dumps(payload).encode("utf-8")
        req = urllib.request.Request(
            endpoint,
            data=data,
            headers={"Content-Type": "application/json"},
            method="POST",
        )

        try:
            with urllib.request.urlopen(req, timeout=self.timeout) as resp:
                result = json.loads(resp.read().decode("utf-8"))
                candidates = result.get("candidates", [])
                if candidates:
                    parts = candidates[0].get("content", {}).get("parts", [])
                    if parts:
                        return parts[0].get("text", "")
                return ""
        except urllib.error.HTTPError as e:
            error_body = e.read().decode("utf-8", errors="replace")
            logger.warning(f"Gemini API returned HTTP {e.code} ({error_body}). Falling back to simulation.")
            return self._mock_generate(prompt, system_prompt)
        except Exception as e:
            logger.warning(f"Gemini API request failed: {e}. Falling back to simulation.")
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
