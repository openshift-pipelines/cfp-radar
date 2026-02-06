"""Structured logging configuration for CFP Radar."""

from __future__ import annotations

import logging
import os
import sys
from typing import Any


def setup_logging(
    level: str | None = None,
    json_output: bool = False,
) -> logging.Logger:
    """Configure and return the root logger for the application.

    Args:
        level: Log level (DEBUG, INFO, WARNING, ERROR). Defaults to INFO,
               or DEBUG if CFP_RADAR_DEBUG env var is set.
        json_output: If True, output logs in JSON format.

    Returns:
        Configured root logger for the application.
    """
    if level is None:
        level = "DEBUG" if os.environ.get("CFP_RADAR_DEBUG") else "INFO"

    log_level = getattr(logging, level.upper(), logging.INFO)

    # Create logger
    logger = logging.getLogger("cfp_radar")
    logger.setLevel(log_level)

    # Remove existing handlers
    logger.handlers.clear()

    # Create console handler
    handler = logging.StreamHandler(sys.stderr)
    handler.setLevel(log_level)

    formatter: logging.Formatter
    if json_output:
        formatter = JsonFormatter()
    else:
        formatter = logging.Formatter(
            fmt="%(asctime)s [%(levelname)s] %(name)s: %(message)s",
            datefmt="%Y-%m-%d %H:%M:%S",
        )

    handler.setFormatter(formatter)
    logger.addHandler(handler)

    return logger


class JsonFormatter(logging.Formatter):
    """JSON log formatter for structured logging output."""

    def format(self, record: logging.LogRecord) -> str:
        import json

        log_data: dict[str, Any] = {
            "timestamp": self.formatTime(record, self.datefmt),
            "level": record.levelname,
            "logger": record.name,
            "message": record.getMessage(),
        }

        if record.exc_info:
            log_data["exception"] = self.formatException(record.exc_info)

        if hasattr(record, "extra"):
            log_data.update(record.extra)

        return json.dumps(log_data)


def get_logger(name: str) -> logging.Logger:
    """Get a child logger for the given module name.

    Args:
        name: Module name (typically __name__).

    Returns:
        Logger instance.
    """
    return logging.getLogger(f"cfp_radar.{name}")
