"""Pytest configuration and fixtures."""

from __future__ import annotations

import pytest

from src.logging_config import setup_logging


@pytest.fixture(autouse=True)
def setup_test_logging() -> None:
    """Set up logging for all tests."""
    setup_logging(level="WARNING")
