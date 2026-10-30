import logging
import sys
from app.models.enums import LogLevel


def get_logger(name: str, level: LogLevel = LogLevel.INFO) -> logging.Logger:
    """
    Configures and returns a structured logger instance.

    Args:
        name: The logger name, typically __name__.
        level: Log level enum.

    Returns:
        logging.Logger: Configured logger.
    """
    logger = logging.getLogger(name)

    if not logger.handlers:
        handler = logging.StreamHandler(sys.stdout)
        formatter = logging.Formatter(
            fmt="[%(asctime)s] [%(levelname)s] [%(name)s]: %(message)s",
            datefmt="%Y-%m-%d %H:%M:%S",
        )
        handler.setFormatter(formatter)
        logger.addHandler(handler)

    log_level_map = {
        LogLevel.DEBUG: logging.DEBUG,
        LogLevel.INFO: logging.INFO,
        LogLevel.WARNING: logging.WARNING,
        LogLevel.ERROR: logging.ERROR,
    }
    logger.setLevel(log_level_map.get(level, logging.INFO))
    return logger

