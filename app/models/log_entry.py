from datetime import datetime
from pydantic import BaseModel, ConfigDict, Field
from app.models.enums import AgentType, LogLevel


class LogEntry(BaseModel):
    """
    Structured log entry capturing agent execution events.
    """

    model_config = ConfigDict(frozen=True)

    timestamp: datetime = Field(default_factory=datetime.now)
    level: LogLevel = LogLevel.INFO
    agent: AgentType
    message: str

