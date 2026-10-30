from app.models.enums import SourceType
from app.tools.tool import Tool


class ToolRegistry:
    """
    Registry for managing and retrieving Tool implementations by SourceType.
    """

    def __init__(self) -> None:
        self._tools: dict[SourceType, Tool] = {}

    def register(self, source: SourceType, tool: Tool) -> None:
        """
        Registers a tool for a given source type.

        Args:
            source: SourceType enum key.
            tool: Concrete Tool instance.

        Raises:
            ValueError: If tool is not an instance of Tool or source is invalid.
        """
        if not isinstance(tool, Tool):
            raise ValueError(f"Expected Tool instance, got {type(tool).__name__}")
        self._tools[source] = tool

    def get(self, source: SourceType) -> Tool:
        """
        Retrieves the tool registered for the given source type.

        Args:
            source: SourceType enum key.

        Returns:
            Tool: Registered Tool instance.

        Raises:
            KeyError: If no tool has been registered for the specified source type.
        """
        if source not in self._tools:
            raise KeyError(f"No tool registered for source type: '{source.value}'")
        return self._tools[source]

    def has_tool(self, source: SourceType) -> bool:
        """
        Checks whether a tool is registered for a given source type.

        Args:
            source: SourceType enum key.

        Returns:
            bool: True if registered, False otherwise.
        """
        return source in self._tools

