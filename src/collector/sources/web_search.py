"""AI-powered web search for event discovery using Claude on Vertex AI."""

from __future__ import annotations

import json
import re
from datetime import date, datetime
from typing import Any, cast

import httpx

from ...claude_client import extract_text, get_claude_client
from ...config import (
    AI_MODEL,
    REGION_TO_COUNTRIES,
    TARGET_REGIONS,
    TOPICS,
    normalize_country,
)
from ...logging_config import get_logger
from ..models import Event

logger = get_logger(__name__)

WEB_SEARCH_TOOL = [
    {
        "type": "web_search_20250305",
        "name": "web_search",
        "max_uses": 5,
    }
]


async def search_events() -> list[Event]:
    """Use AI to search for and extract event information."""
    client = get_claude_client()
    if client is None:
        logger.info("Skipping AI web search")
        return []

    logger.info(f"Starting web search with {AI_MODEL} model")
    events = []

    for region in TARGET_REGIONS:
        countries = REGION_TO_COUNTRIES.get(region, [])
        countries_str = ", ".join(countries)
        topics_str = ", ".join(TOPICS[:5])
        current_year = date.today().year

        prompt = f"""Search for upcoming tech conferences and meetups in {region} for {current_year} and {current_year + 1}."""

        if countries_str:
            prompt+=f"\n\nCover these countries: {countries_str}"
        if topics_str:
            prompt+=f"\n\nFocus on events related to: {topics_str}"
        prompt+="""

For each event you find, provide the following information in JSON format:
{{
  "events": [
    {{
      "name": "Event Name",
      "city": "City Name",
      "country": "Country Name",
      "start_date": "YYYY-MM-DD",
      "end_date": "YYYY-MM-DD or null",
      "event_type": "conference or meetup or workshop",
      "topics": ["topic1", "topic2"],
      "cfp_deadline": "YYYY-MM-DD or null",
      "cfp_url": "https://... or null",
      "website": "https://...",
      "description": "Brief description"
    }}
  ]
}}

Only include events that:"""
        if {countries_str}:
            prompt+=f"\n- Are in one of these countries: {countries_str}"
        if topics_str:
            prompt+=f"\n- Are related to {topics_str}"
        prompt+="""
- Have dates in the future or within the last month
- You are reasonably confident about
- Are not already in the events list

Return ONLY the JSON, no other text."""
        print(prompt)
        try:
            logger.debug("Querying Claude for region %s", region)
            response = await client.messages.create(
                model=AI_MODEL,
                max_tokens=8192,
                messages=[{"role": "user", "content": prompt}],
                tools=cast(Any, WEB_SEARCH_TOOL),
            )
            content = extract_text(response)
            logger.debug("Claude response for %s: %d chars", region, len(content))
            parsed_events = _parse_response(content, region)
            logger.info("Parsed %d events for %s", len(parsed_events), region)
            events.extend(parsed_events)

        except Exception as e:
            logger.error("Error searching events for %s: %s: %s", region, type(e).__name__, e)
            continue

    return events


def _parse_response(content: str, country: str) -> list[Event]:
    """Parse the model JSON response into Event objects."""
    events: list[Event] = []

    # Try to extract JSON from the response
    try:
        # Find JSON in the response
        json_match = re.search(r"\{[\s\S]*\}", content)
        if not json_match:
            return events

        data = json.loads(json_match.group())
        event_list = data.get("events", [])

        for item in event_list:
            try:
                start_date_str = item.get("start_date")
                if not start_date_str or not isinstance(start_date_str, str):
                    continue
                start_date = date.fromisoformat(start_date_str)

                end_date = None
                if item.get("end_date"):
                    try:
                        end_date = date.fromisoformat(item["end_date"])
                    except ValueError:
                        pass

                cfp_deadline = None
                if item.get("cfp_deadline"):
                    try:
                        cfp_deadline = date.fromisoformat(item["cfp_deadline"])
                    except ValueError:
                        pass

                event = Event(
                    name=item.get("name", ""),
                    city=item.get("city", ""),
                    country=normalize_country(item.get("country", country)),
                    start_date=start_date,
                    end_date=end_date,
                    event_type=item.get("event_type", "conference"),
                    topics=item.get("topics", []),
                    cfp_deadline=cfp_deadline,
                    cfp_url=item.get("cfp_url"),
                    website=item.get("website", ""),
                    description=item.get("description", ""),
                    relevance_score=0.7,  # AI-discovered events get moderate score
                    last_updated=datetime.now(),
                )
                events.append(event)

            except (KeyError, ValueError) as e:
                logger.warning("Error parsing event: %s", e)
                continue

    except json.JSONDecodeError as e:
        logger.warning("Error parsing JSON response: %s", e)

    return events


async def extract_cfp_details(event_url: str) -> dict:
    """Use AI to extract CFP details from an event website."""
    client = get_claude_client()
    if client is None:
        return {}

    # Fetch the page content
    async with httpx.AsyncClient(timeout=30.0, follow_redirects=True) as http:
        try:
            response = await http.get(
                event_url,
                headers={"User-Agent": "Mozilla/5.0 (compatible; gather-cnf/1.0)"},
            )
            if response.status_code != 200:
                return {}
            html = response.text[:50000]  # Limit content size
        except Exception:
            return {}

    prompt = f"""Analyze this event website HTML and extract CFP (Call for Papers/Proposals) information.

HTML content:
{html[:30000]}

Return JSON with:
{{
  "cfp_deadline": "YYYY-MM-DD or null",
  "cfp_url": "https://... or null",
  "cfp_open": true/false,
  "topics": ["topic1", "topic2"]
}}

Return ONLY the JSON, no other text."""

    try:
        genai_response = await client.messages.create(
            model=AI_MODEL,
            max_tokens=4096,
            messages=[{"role": "user", "content": prompt}],
            tools=cast(Any, WEB_SEARCH_TOOL),
        )
        content = extract_text(genai_response)
        json_match = re.search(r"\{[\s\S]*\}", content)
        if json_match:
            result: dict[str, Any] = json.loads(json_match.group())
            return result

    except Exception as e:
        logger.error("Error extracting CFP details: %s", e)

    return {}
