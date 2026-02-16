"""Generate ICS calendar feed for CFP Radar events."""

from __future__ import annotations

from datetime import timedelta

from icalendar import Calendar
from icalendar import Event as ICSEvent

from .collector.models import Event


def generate_ics(events: list[Event], output_file: str) -> None:
    """Generate an ICS calendar file from events.

    Produces up to two VEVENT entries per event:
    - A CFP deadline entry (if cfp_deadline is set)
    - An event entry spanning start_date to end_date
    """
    cal = Calendar()
    cal.add("prodid", "-//CFP Radar//cfp-radar//EN")
    cal.add("version", "2.0")
    cal.add("x-wr-calname", "CFP Radar")

    for event in events:
        location = f"{event.city}, {event.country}"

        # CFP Deadline entry
        if event.cfp_deadline:
            cfp_entry = ICSEvent()
            cfp_entry.add("uid", f"{event.id}-cfp@cfp-radar")
            cfp_entry.add("summary", f"[CFP Deadline] {event.name}")
            cfp_entry.add("dtstart", event.cfp_deadline)
            cfp_entry.add("dtend", event.cfp_deadline + timedelta(days=1))
            cfp_entry.add("transp", "TRANSPARENT")
            cfp_entry.add("location", location)
            if event.cfp_url:
                cfp_entry.add("url", event.cfp_url)
            cfp_entry.add("description", _build_description(event))
            cal.add_component(cfp_entry)

        # Event entry
        event_entry = ICSEvent()
        event_entry.add("uid", f"{event.id}-event@cfp-radar")
        event_entry.add("summary", event.name)
        event_entry.add("dtstart", event.start_date)
        # DTEND is exclusive per RFC 5545 for DATE values
        end = event.end_date if event.end_date else event.start_date
        event_entry.add("dtend", end + timedelta(days=1))
        event_entry.add("transp", "OPAQUE")
        event_entry.add("location", location)
        if event.website:
            event_entry.add("url", event.website)
        event_entry.add("description", _build_description(event))
        cal.add_component(event_entry)

    with open(output_file, "wb") as f:
        f.write(cal.to_ical())


def _build_description(event: Event) -> str:
    """Build a description string for a calendar entry."""
    parts: list[str] = []
    if event.description:
        parts.append(event.description)
    if event.website:
        parts.append(f"Website: {event.website}")
    if event.cfp_url:
        parts.append(f"CFP: {event.cfp_url}")
    if event.topics:
        parts.append(f"Topics: {', '.join(event.topics)}")
    return "\n".join(parts)
