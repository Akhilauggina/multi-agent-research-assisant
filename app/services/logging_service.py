from typing import Protocol
from app.models.enums import AgentType, LogLevel
from app.models.log_entry import LogEntry
from app.models.research_state import ResearchState
from app.utils.logger import get_logger

logger = get_logger(__name__)


class LoggingService:
    """
    Dedicated logging service injected into agents to record structured events
    both to application logs and into the ResearchState without agents directly
    manipulating the state's internal logs collection.
    """

    def log(
        self,
        state: ResearchState,
        agent: AgentType,
        message: str,
        level: LogLevel = LogLevel.INFO,
    ) -> None:
        """
        Records a log entry into the state and outputs to standard logger.

        Args:
            state: Active ResearchState.
            agent: AgentType recording the log.
            message: Informational or error message.
            level: Severity level.
        """
        entry = LogEntry(
            agent=agent,
            message=message,
            level=level,
        )
        state.logs.append(entry)

        log_msg = f"[{agent.value.upper()}] {message}"
        if level == LogLevel.DEBUG:
            logger.debug(log_msg)
        elif level == LogLevel.WARNING:
            logger.warning(log_msg)
        elif level == LogLevel.ERROR:
            logger.error(log_msg)
        else:
            logger.info(log_msg)

