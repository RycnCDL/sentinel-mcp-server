"""
Logging Configuration Module

Sets up structured logging using structlog
"""

import sys
import logging
from typing import Optional
import structlog
from structlog.stdlib import LoggerFactory


def setup_logging(level: str = "INFO", format_type: str = "json", log_requests: bool = True) -> None:
    """
    Configure structured logging for the application

    Args:
        level: Logging level (DEBUG, INFO, WARNING, ERROR, CRITICAL)
        format_type: Log format type ("json" or "text")
        log_requests: Whether to log HTTP requests
    """
    # Convert string level to logging constant
    log_level = getattr(logging, level.upper(), logging.INFO)

    # Configure standard library logging
    logging.basicConfig(
        format="%(message)s",
        stream=sys.stdout,
        level=log_level,
    )

    # Choose processors based on format type
    if format_type == "json":
        processors = [
            structlog.contextvars.merge_contextvars,
            structlog.stdlib.add_log_level,
            structlog.stdlib.add_logger_name,
            structlog.processors.TimeStamper(fmt="iso"),
            structlog.processors.StackInfoRenderer(),
            structlog.processors.format_exc_info,
            structlog.processors.UnicodeDecoder(),
            structlog.processors.JSONRenderer(),
        ]
    else:  # text format
        processors = [
            structlog.contextvars.merge_contextvars,
            structlog.stdlib.add_log_level,
            structlog.stdlib.add_logger_name,
            structlog.processors.TimeStamper(fmt="iso"),
            structlog.processors.StackInfoRenderer(),
            structlog.processors.format_exc_info,
            structlog.processors.UnicodeDecoder(),
            structlog.dev.ConsoleRenderer(colors=False),  # Disable colors for STDIO
        ]

    # Configure structlog
    structlog.configure(
        processors=processors,
        wrapper_class=structlog.stdlib.BoundLogger,
        context_class=dict,
        logger_factory=LoggerFactory(),
        cache_logger_on_first_use=True,
    )
    
    # Suppress structlog warnings to stderr
    logging.getLogger("structlog").setLevel(logging.ERROR)

    logger = structlog.get_logger(__name__)
    logger.info(
        "Logging configured",
        level=level,
        format=format_type,
        log_requests=log_requests,
    )


def get_logger(name: str) -> structlog.BoundLogger:
    """
    Get a logger instance

    Args:
        name: Logger name (usually __name__)

    Returns:
        structlog.BoundLogger: Logger instance
    """
    return structlog.get_logger(name)
