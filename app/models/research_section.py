from pydantic import BaseModel, Field

from app.models.enums import SourceType, TaskStatus
from app.models.tool_result import ToolResult


class ResearchSection(BaseModel):
    """
    Represents an individual section of a research plan.
    """

    title: str
    description: str = ""
    assigned_tool: SourceType = SourceType.WIKIPEDIA
    status: TaskStatus = TaskStatus.PENDING
    research_results: list[ToolResult] = Field(default_factory=list)
    retry_count: int = 0
