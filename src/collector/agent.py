"""Main collection agent that orchestrates all event sources."""

from __future__ import annotations

import asyncio
from datetime import date, datetime

from ..config import EVENTS_FILE, TOPICS
from ..logging_config import get_logger
from .models import Event, EventStore
from .sources import confs_tech, papercall, web_search

logger = get_logger(__name__)


async def collect_all_events(use_ai: bool = True) -> list[Event]:
    """Collect events from all sources and merge them."""
    logger.info("Starting event collection...")
    all_events: list[Event] = []

    # Collect from structured sources in parallel
    tasks = [
        confs_tech.fetch_conferences(date.today().year),
        confs_tech.fetch_conferences(date.today().year + 1),
        papercall.fetch_cfps(),
    ]

    if use_ai:
        tasks.append(web_search.search_events())

    results = await asyncio.gather(*tasks, return_exceptions=True)

    source_names = ["confs.tech current", "confs.tech next", "papercall", "ai_search"]
    for i, result in enumerate(results):
        if isinstance(result, BaseException):
            logger.error("Error collecting from %s: %s", source_names[i], result)
        else:
            event_list: list[Event] = result
            all_events.extend(event_list)
            logger.info("Collected %d events from %s", len(event_list), source_names[i])

    # Deduplicate events
    unique_events = deduplicate_events(all_events)
    logger.info("Total unique events after deduplication: %d", len(unique_events))

    # Filter out past events (more than 30 days ago)
    cutoff = date.today().replace(day=1)
    future_events = [e for e in unique_events if e.start_date >= cutoff]
    logger.info("Future events: %d", len(future_events))

    # Sort by start date
    future_events.sort(key=lambda e: e.start_date)

    # Save to storage
    store = EventStore(EVENTS_FILE)
    store.merge(future_events)
    logger.info("Events saved to %s", EVENTS_FILE)

    return future_events


def deduplicate_events(events: list[Event]) -> list[Event]:
    """Remove duplicate events based on name similarity and date."""
    if not events:
        return []

    seen = {}
    unique = []

    for event in events:
        # Normalize name for comparison
        normalized_name = _normalize_name(event.name)
        key = (normalized_name, event.start_date.isoformat())

        if key not in seen:
            seen[key] = event
            unique.append(event)
        else:
            # Keep the event with more complete information
            existing = seen[key]
            if _event_completeness(event) > _event_completeness(existing):
                unique.remove(existing)
                unique.append(event)
                seen[key] = event

    return unique


def _normalize_name(name: str) -> str:
    """Normalize event name for comparison."""
    import re

    # Lowercase and remove common suffixes
    name = name.lower()
    name = re.sub(r"\s*(20\d{2}|conference|conf|summit|meetup)\s*", " ", name)
    name = re.sub(r"[^\w\s]", "", name)
    name = " ".join(name.split())
    return name


def _event_completeness(event: Event) -> int:
    """Score event by completeness of information."""
    score = 0
    if event.description:
        score += 1
    if event.cfp_deadline:
        score += 2
    if event.cfp_url:
        score += 2
    if event.website:
        score += 1
    if event.topics:
        score += len(event.topics)
    if event.end_date:
        score += 1
    return score


def calculate_topic_relevance(event: Event) -> float:
    """Calculate relevance score based on topic matches."""
    if not event.topics:
        return 0.3

    topic_lower = [t.lower() for t in event.topics]
    matches = sum(1 for t in TOPICS if any(t.lower() in topic for topic in topic_lower))

    # Base score
    score = 0.3

    # Topic matches (up to 0.5)
    score += min(0.5, matches * 0.1)

    # CFP availability bonus
    if event.cfp_deadline and event.cfp_deadline >= date.today():
        score += 0.15

    # Tekton/CI-CD specific bonus
    name_lower = event.name.lower()
    if any(kw in name_lower for kw in ["tekton", "ci/cd", "cicd", "pipeline"]):
        score += 0.1

    return min(1.0, score)


async def enrich_event_cfp(event: Event) -> Event:
    """Enrich event with CFP details from its website."""
    if not event.website or event.cfp_deadline:
        return event

    details = await web_search.extract_cfp_details(event.website)

    if details.get("cfp_deadline"):
        try:
            event.cfp_deadline = date.fromisoformat(details["cfp_deadline"])
        except ValueError:
            pass

    if details.get("cfp_url"):
        event.cfp_url = details["cfp_url"]

    if details.get("topics"):
        event.topics = list(set(event.topics + details["topics"]))

    event.last_updated = datetime.now()
    return event
