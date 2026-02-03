"""AI-powered web search for event discovery using Gemini."""

import json
import re
from datetime import date, datetime

import httpx
from google import genai

from ...config import GEMINI_API_KEY, TARGET_CITIES, TOPICS
from ..models import Event


async def search_events() -> list[Event]:
    """Use Gemini to search for and extract event information."""
    if not GEMINI_API_KEY:
        print("Warning: GEMINI_API_KEY not set, skipping AI search")
        return []

    print(f"Starting Gemini search with API key: {GEMINI_API_KEY[:3]}...")

    client = genai.Client(api_key=GEMINI_API_KEY)
    events = []

    for location in TARGET_CITIES:
        city = location["city"]
        country = location["country"]

        # Build search query for Gemini
        topics_str = ", ".join(TOPICS[:5])
        current_year = date.today().year

        prompt = f"""Search for upcoming tech conferences and meetups in {city}, {country} for {current_year} and {current_year + 1}.

Focus on events related to: {topics_str}

For each event you find, provide the following information in JSON format:
{{
  "events": [
    {{
      "name": "Event Name",
      "city": "{city}",
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
1. Are actually in {city}, {country}
2. Are related to DevOps, CI/CD, Cloud Native, Kubernetes, or Platform Engineering
3. Have dates in the future or within the last month
4. You are reasonably confident about

Return ONLY the JSON, no other text."""

        try:
            print(f"Querying Gemini for {city}, {country}...")
            response = client.models.generate_content(
                model="gemini-2.5-flash-lite",
                contents=prompt,
            )
            content = response.text
            print(f"Gemini response for {city}: {len(content)} chars")
            parsed_events = _parse_response(content, city, country)
            print(f"Parsed {len(parsed_events)} events for {city}")
            events.extend(parsed_events)

        except Exception as e:
            print(f"Error searching events for {city}: {type(e).__name__}: {e}")
            continue

    return events


def _parse_response(content: str, city: str, country: str) -> list[Event]:
    """Parse Gemini's JSON response into Event objects."""
    events = []

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
                start_date = date.fromisoformat(item["start_date"])

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
                    city=item.get("city", city),
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
                print(f"Error parsing event: {e}")
                continue

    except json.JSONDecodeError as e:
        print(f"Error parsing JSON response: {e}")

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
        response = client.models.generate_content(
            model="gemini-2.5-flash-lite",
            contents=prompt,
        )
        content = response.text
        json_match = re.search(r"\{[\s\S]*\}", content)
        if json_match:
            return json.loads(json_match.group())

    except Exception as e:
        print(f"Error extracting CFP details: {e}")

    return {}
