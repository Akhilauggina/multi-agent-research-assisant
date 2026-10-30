from enum import StrEnum


class AgentType(StrEnum):
    SUPERVISOR = "supervisor"
    PLANNER = "planner"
    SEARCH = "search"
    READER = "reader"
    FACT_CHECKER = "fact_checker"
    SUMMARIZER = "summarizer"
    WRITER = "writer"


class WorkflowStatus(StrEnum):
    PENDING = "pending"
    RUNNING = "running"
    COMPLETED = "completed"
    FAILED = "failed"


class TaskStatus(StrEnum):
    PENDING = "pending"
    RUNNING = "running"
    COMPLETED = "completed"
    FAILED = "failed"
    RETRYING = "retrying"


class LogLevel(StrEnum):
    INFO = "info"
    WARNING = "warning"
    ERROR = "error"
    DEBUG = "debug"


class ToolAction(StrEnum):
    SEARCH = "search"
    READ = "read"
    EXTRACT = "extract"


class SourceType(StrEnum):
    WIKIPEDIA = "wikipedia"
    DUCKDUCKGO = "duckduckgo"
    ARXIV = "arxiv"
    YOUTUBE = "youtube"


class LLMProvider(StrEnum):
    OPENAI = "openai"
    GEMINI = "gemini"
