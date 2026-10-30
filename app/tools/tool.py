from abc import ABC, abstractmethod
from app.models.tool_request import ToolRequest
from app.models.tool_result import ToolResult


class Tool(ABC):
    """
    Abstract base class for all research tools.
    Every tool must implement the execute method, measuring execution time
    and returning a normalized ToolResult.
    """

    @abstractmethod
    def execute(self, request: ToolRequest) -> ToolResult:
        """
        Executes a research task according to the supplied ToolRequest.

        Args:
            request: Standardized request containing query and parameters.

        Returns:
            ToolResult: Standardized outcome of tool execution.
        """
        pass

