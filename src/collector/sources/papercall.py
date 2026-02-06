"""Collector for papercall.io - CFP aggregator."""

import httpx
from bs4 import BeautifulSoup
from datetime import date, datetime
from ..models import Event
from ...config import TARGET_COUNTRIES, GLOBAL_CONFERENCES, TOPICS


PAPERCALL_URL = "https://www.papercall.io/events"


async def fetch_cfps() -> list[Event]:
    """Fetch CFPs from papercall.io by scraping the events page."""
    events = []
    async with httpx.AsyncClient(timeout=30.0, follow_redirects=True) as client:
        # Search for relevant CFPs
        for topic in ["devops", "kubernetes", "cloud", "platform"]:
            try:
                response = await client.get(
                    PAPERCALL_URL,
                    params={"keywords": topic},
                    headers={"User-Agent": "Mozilla/5.0 (compatible; gather-cnf/1.0)"},
                )
                if response.status_code == 200:
                    events.extend(_parse_papercall_page(response.text))
            except Exception:
                continue

    # Deduplicate by name
    seen = set()
    unique_events = []
    for event in events:
        if event.name not in seen:
            seen.add(event.name)
            unique_events.append(event)

    return unique_events


def _parse_papercall_page(html: str) -> list[Event]:
    """Parse papercall.io events page."""
    events = []
    soup = BeautifulSoup(html, "html.parser")

    target_countries_lower = {c.lower() for c in TARGET_COUNTRIES}
    global_confs_lower = [gc.lower() for gc in GLOBAL_CONFERENCES]

    # Find event cards
    for card in soup.select(".event-card, .event-listing, article.event"):
        try:
            name_elem = card.select_one("h2, h3, .event-title, .event-name")
            if not name_elem:
                continue
            name = name_elem.get_text(strip=True)

            # Get location
            location_elem = card.select_one(".location, .event-location, .city")
            location = location_elem.get_text(strip=True) if location_elem else ""

            # Check if in target location or is a global conference
            location_lower = location.lower()
            name_lower = name.lower()

            country_match = any(country in location_lower for country in target_countries_lower)
            global_conf_match = any(gc in name_lower for gc in global_confs_lower)

            if not (country_match or global_conf_match):
                continue

            # Get dates
            date_elem = card.select_one(".date, .event-date, time")
            cfp_date_elem = card.select_one(".cfp-date, .deadline")

            start_date = _parse_date_text(
                date_elem.get_text(strip=True) if date_elem else ""
            )
            if not start_date:
                start_date = date.today()  # Default to today if no date found

            cfp_deadline = _parse_date_text(
                cfp_date_elem.get_text(strip=True) if cfp_date_elem else ""
            )

            # Get link
            link_elem = card.select_one("a[href]")
            website = link_elem["href"] if link_elem else ""
            if website and website.startswith("/"):
                website = f"https://www.papercall.io{website}"

            # Determine city and country from location
            city, country = _parse_location(location)

            # Check topic relevance
            topics_found = [t for t in TOPICS if t.lower() in name_lower]

            event = Event(
                name=name,
                city=city,
                country=country,
                start_date=start_date,
                event_type="conference",
                topics=topics_found if topics_found else ["cloud native"],
                cfp_deadline=cfp_deadline,
                cfp_url=website,
                website=website,
                description="",
                relevance_score=0.6,
                last_updated=datetime.now(),
            )
            events.append(event)

        except Exception:
            continue

    return events


def _parse_date_text(text: str) -> date | None:
    """Parse date from various text formats."""
    import re
    from dateutil import parser

    if not text:
        return None

    # Clean up the text
    text = re.sub(r"(CFP|closes?|ends?|deadline):?\s*", "", text, flags=re.IGNORECASE)
    text = text.strip()

    try:
        return parser.parse(text, fuzzy=True).date()
    except Exception:
        return None


def _parse_location(location: str) -> tuple[str, str]:
    """Parse location string into city and country."""
    parts = [p.strip() for p in location.split(",")]
    if len(parts) >= 2:
        return parts[0], parts[-1]
    elif len(parts) == 1:
        return parts[0], ""
    return "", ""
