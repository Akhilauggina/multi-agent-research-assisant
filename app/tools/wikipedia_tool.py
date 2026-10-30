import time
from app.clients.wikipedia_client import WikipediaClient
from app.models.enums import SourceType
from app.models.tool_request import ToolRequest
from app.models.tool_result import ToolResult
from app.tools.tool import Tool
from app.utils.logger import get_logger

logger = get_logger(__name__)


class WikipediaTool(Tool):
    """
    Concrete tool implementation for fetching research content from Wikipedia.
    Adheres strictly to the Tool contract: receives ToolRequest, delegates to
    WikipediaClient, measures execution time, catches errors, and returns ToolResult.
    """

    def __init__(self, client: WikipediaClient) -> None:
        """
        Initializes WikipediaTool with an injected WikipediaClient.

        Args:
            client: Injected WikipediaClient instance.
        """
        self.client = client

    def execute(self, request: ToolRequest) -> ToolResult:
        """
        Executes a Wikipedia query, measuring time and handling exceptions.

        Args:
            request: Inbound ToolRequest.

        Returns:
            ToolResult: Standardized execution result with execution time.
        """
        start_time = time.perf_counter()
        try:
            response = self.client.search_and_get_summary(request.query)
            elapsed = time.perf_counter() - start_time
            logger.info(f"WikipediaTool executed query '{request.query}' in {elapsed:.3f}s")
            return ToolResult(
                success=True,
                content=response,
                error=None,
                source=SourceType.WIKIPEDIA,
                execution_time=elapsed,
            )
        except Exception as exc:
            elapsed = time.perf_counter() - start_time
            logger.error(f"WikipediaTool execution failed for '{request.query}': {exc}")
            return ToolResult(
                success=False,
                content=None,
                error=str(exc),
                source=SourceType.WIKIPEDIA,
                execution_time=elapsed,
            )

