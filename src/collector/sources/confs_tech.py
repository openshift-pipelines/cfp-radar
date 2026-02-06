"""Collector for confs.tech - open source conference list."""

from __future__ import annotations

from datetime import date, datetime

import httpx

from ...config import GLOBAL_CONFERENCES, TARGET_COUNTRIES, TOPICS
from ...logging_config import get_logger
from ..models import Event

logger = get_logger(__name__)


CONFS_TECH_BASE = (
    "https://raw.githubusercontent.com/tech-conferences/conference-data/main/conferences"
)

# confs.tech category mappings for our topics
CATEGORIES = ["devops", "cloud", "general"]


async def fetch_conferences(year: int | None = None) -> list[Event]:
    """Fetch conferences from confs.tech GitHub data."""
    if year is None:
        year = date.today().year

    events = []
    async with httpx.AsyncClient(timeout=30.0) as client:
        for category in CATEGORIES:
            url = f"{CONFS_TECH_BASE}/{year}/{category}.json"
            try:
                response = await client.get(url)
                if response.status_code == 200:
                    data = response.json()
                    events.extend(_parse_conferences(data, category))
            except httpx.HTTPError as e:
                # Category file may not exist for all years
                logger.debug("Error fetching confs.tech for %s/%d: %s", category, year, e)
                continue

    return events


def _parse_conferences(data: list[dict], category: str) -> list[Event]:
    """Parse conference data from confs.tech format."""
    events = []
    target_countries_lower = {c.lower() for c in TARGET_COUNTRIES}
    global_confs_lower = [gc.lower() for gc in GLOBAL_CONFERENCES]

    for conf in data:
        city = conf.get("city", "")
        country = conf.get("country", "")
        name_lower = conf.get("name", "").lower()

        # Check if event is in our target countries or is a global conference
        country_match = country.lower() in target_countries_lower
        global_conf_match = any(gc in name_lower for gc in global_confs_lower)

        if not (country_match or global_conf_match):
            continue

        # Check topic relevance
        topics_found = [t for t in TOPICS if t.lower() in name_lower]

        # Add category as topic
        if category == "devops":
            topics_found.append("devops")
        elif category == "cloud":
            topics_found.append("cloud native")

        if not topics_found and category == "general":
            # Skip general conferences without relevant keywords
            continue

        try:
            start_date = date.fromisoformat(conf["startDate"])
        except (KeyError, ValueError):
            continue

        end_date = None
        if conf.get("endDate"):
            try:
                end_date = date.fromisoformat(conf["endDate"])
            except ValueError:
                pass

        cfp_deadline = None
        cfp_url = None
        if conf.get("cfpEndDate"):
            try:
                cfp_deadline = date.fromisoformat(conf["cfpEndDate"])
            except ValueError:
                pass
        if conf.get("cfpUrl"):
            cfp_url = conf["cfpUrl"]

        event = Event(
            name=conf.get("name", ""),
            city=city,
            country=country,
            start_date=start_date,
            end_date=end_date,
            event_type="conference",
            topics=list(set(topics_found)),
            cfp_deadline=cfp_deadline,
            cfp_url=cfp_url,
            website=conf.get("url", ""),
            description=conf.get("description", ""),
            relevance_score=_calculate_relevance(conf, topics_found),
            last_updated=datetime.now(),
        )
        events.append(event)

    return events


def _calculate_relevance(conf: dict, topics_found: list[str]) -> float:
    """Calculate relevance score based on topic matches."""
    score = 0.3  # Base score for being in target location
    score += min(0.5, len(topics_found) * 0.15)  # Topic matches
    if conf.get("cfpUrl"):
        score += 0.1  # Has CFP
    if conf.get("twitter"):
        score += 0.1  # Active community presence
    return min(1.0, score)
