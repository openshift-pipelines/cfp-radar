"""AI-powered web search for event discovery using Gemini."""

from __future__ import annotations

import json
import re
from datetime import date, datetime
from typing import Any

import httpx
from google import genai
from google.genai import types

from ...config import GEMINI_API_KEY, TARGET_COUNTRIES, TOPICS
from ...logging_config import get_logger
from ..models import Event

logger = get_logger(__name__)


async def search_events() -> list[Event]:
    """Use Gemini to search for and extract event information."""
    if not GEMINI_API_KEY:
        logger.warning("GEMINI_API_KEY not set, skipping AI search")
        return []

    logger.info("Starting Gemini AI search")

    client = genai.Client(api_key=GEMINI_API_KEY)
    events = []

    for country in TARGET_COUNTRIES:
        # Build search query for Gemini
        topics_str = ", ".join(TOPICS[:5])
        current_year = date.today().year

        prompt = f"""Search for upcoming tech conferences and meetups in {country} for {current_year} and {current_year + 1}.

Focus on events related to: {topics_str}

For each event you find, provide the following information in JSON format:
{{
  "events": [
    {{
      "name": "Event Name",
      "city": "City Name",
      "country": "{country}",
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

Only include events that:
1. Are actually in {country}
2. Are related to DevOps, CI/CD, Cloud Native, Kubernetes, or Platform Engineering
3. Have dates in the future or within the last month
4. You are reasonably confident about

Return ONLY the JSON, no other text."""

        try:
            logger.debug("Querying Gemini for %s", country)
            response = client.models.generate_content(
                model="gemini-3-flash-preview",
                contents=prompt,
                config=types.GenerateContentConfig(
                    tools=[types.Tool(google_search=types.GoogleSearch())],
                ),
            )
            content = response.text or ""
            logger.debug("Gemini response for %s: %d chars", country, len(content))
            parsed_events = _parse_response(content, country)
            logger.info("Parsed %d events for %s", len(parsed_events), country)
            events.extend(parsed_events)

        except Exception as e:
            logger.error("Error searching events for %s: %s: %s", country, type(e).__name__, e)
            continue

    return events


def _parse_response(content: str, country: str) -> list[Event]:
    """Parse Gemini's JSON response into Event objects."""
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
                    country=item.get("country", country),
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
    """Use Gemini to extract CFP details from an event website."""
    if not GEMINI_API_KEY:
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

    client = genai.Client(api_key=GEMINI_API_KEY)

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
        genai_response = client.models.generate_content(
            model="gemini-3-flash-preview",
            contents=prompt,
            config=types.GenerateContentConfig(
                tools=[types.Tool(google_search=types.GoogleSearch())],
            ),
        )
        content = genai_response.text or ""
        json_match = re.search(r"\{[\s\S]*\}", content)
        if json_match:
            result: dict[str, Any] = json.loads(json_match.group())
            return result

    except Exception as e:
        logger.error("Error extracting CFP details: %s", e)

    return {}
