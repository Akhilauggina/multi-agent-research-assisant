from typing import Any
from pydantic import BaseModel, ConfigDict, Field
from app.models.enums import SourceType


class ToolResult(BaseModel):
    """
    Represents the normalized execution result from any research tool.
    """

    model_config = ConfigDict(frozen=True)

    success: bool
    content: Any = None
    error: str | None = None
    source: SourceType
    execution_time: float = Field(..., ge=0.0)
