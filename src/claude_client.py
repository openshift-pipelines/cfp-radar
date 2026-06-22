"""Claude on Vertex AI client factory."""

from __future__ import annotations

from anthropic import AsyncAnthropicVertex
from anthropic.types import Message

from .config import GOOGLE_CLOUD_LOCATION, GOOGLE_CLOUD_PROJECT, is_ai_configured
from .logging_config import get_logger

logger = get_logger(__name__)

def get_claude_client() -> AsyncAnthropicVertex | None:
    """Create an async Claude on Vertex AI client, or None when not configured."""
    if not is_ai_configured():
        logger.warning("AI search not configured")
        return None
    return AsyncAnthropicVertex(
        project_id=GOOGLE_CLOUD_PROJECT,
        region=GOOGLE_CLOUD_LOCATION,
    )


def extract_text(response: Message) -> str:
    """Extract concatenated text blocks from a Claude message response."""
    return "".join(block.text for block in response.content if block.type == "text")
