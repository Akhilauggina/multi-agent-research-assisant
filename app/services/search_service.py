from app.models.tool_request import ToolRequest
from app.models.tool_result import ToolResult
from app.tools.tool_registry import ToolRegistry
from app.utils.logger import get_logger

logger = get_logger(__name__)


class SearchService:
    """
    Service responsible for executing search requests across tools.
    Uses ToolRegistry to retrieve the appropriate Tool and executes it,
    never masking configuration errors.
    """

    def __init__(self, tool_registry: ToolRegistry) -> None:
        """
        Initializes SearchService with an injected ToolRegistry.

        Args:
            tool_registry: Injected ToolRegistry instance.
        """
        self.tool_registry = tool_registry

    def execute_search(self, request: ToolRequest) -> ToolResult:
        """
        Executes a search using the tool registered for request.source.

        Args:
            request: Standardized ToolRequest.

        Returns:
            ToolResult: Standardized ToolResult from tool execution.

        Raises:
            KeyError: If the tool for the requested source is not registered.
        """
        logger.info(f"Looking up tool for source: '{request.source.value}'")
        tool = self.tool_registry.get(request.source)

        logger.info(f"Executing tool {type(tool).__name__} for query: '{request.query}'")
        return tool.execute(request)

