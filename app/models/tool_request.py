from typing import Any
from pydantic import BaseModel, ConfigDict, Field
from app.models.enums import SourceType


class ToolRequest(BaseModel):
    """
    Represents a normalized request payload sent to a research tool.
    """

    model_config = ConfigDict(frozen=True)

    query: str
    source: SourceType
    parameters: dict[str, Any] = Field(default_factory=dict)
