from datetime import datetime
from typing import Any
from uuid import UUID, uuid4

from pydantic import BaseModel, ConfigDict, Field

from app.models.enums import AgentType, WorkflowStatus
from app.models.log_entry import LogEntry
from app.models.research_section import ResearchSection
from app.models.tool_result import ToolResult


class ResearchState(BaseModel):
    """
    Shared Pydantic state flowing through every LangGraph agent node.
    """

    model_config = ConfigDict(validate_assignment=True)

    research_id: UUID = Field(default_factory=uuid4)
    topic: str

    # Agent specific workflow state fields
    plan: list[str] = Field(default_factory=list)
    sections: list[ResearchSection] = Field(default_factory=list)
    search_results: dict[str, list[ToolResult]] = Field(default_factory=dict)
    read_results: dict[str, str] = Field(default_factory=dict)
    verified_results: dict[str, str] = Field(default_factory=dict)
    final_summary: str | None = None
    report: str | None = None

    # Execution metadata & tracking
    current_agent: AgentType = AgentType.PLANNER
    workflow_status: WorkflowStatus = WorkflowStatus.PENDING
    progress: int = Field(default=0, ge=0, le=100)
    logs: list[LogEntry] = Field(default_factory=list)
    retry_counts: dict[str, int] = Field(default_factory=dict)
    metadata: dict[str, Any] = Field(default_factory=dict)
    created_at: datetime = Field(default_factory=datetime.now)
