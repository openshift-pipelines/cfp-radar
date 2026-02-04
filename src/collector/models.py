"""Data models for event tracking."""

from dataclasses import dataclass, field, asdict
from datetime import date, datetime
from typing import Any
import json
import os
import hashlib


@dataclass
class Event:
    """Represents a tech event with CFP information."""

    name: str
    city: str
    country: str
    start_date: date
    website: str
    event_type: str = "conference"  # conference | meetup | workshop
    end_date: date | None = None
    topics: list[str] = field(default_factory=list)
    cfp_deadline: date | None = None
    cfp_url: str | None = None
    cfp_status: str = "check"  # open | closed | check
    description: str = ""
    relevance_score: float = 0.5  # 1-5 scale (5 = highly relevant for Tekton/CI-CD)
    venue: str | None = None
    expected_attendees: int | None = None
    last_updated: datetime = field(default_factory=datetime.now)
    id: str = ""

    def __post_init__(self):
        if not self.id:
            self.id = self._generate_id()

    def _generate_id(self) -> str:
        """Generate unique ID from event name and start date."""
        key = f"{self.name.lower()}-{self.start_date.isoformat()}"
        return hashlib.md5(key.encode()).hexdigest()[:12]

    def to_dict(self) -> dict[str, Any]:
        """Convert to dictionary for JSON serialization."""
        data = asdict(self)
        data["start_date"] = self.start_date.isoformat()
        data["end_date"] = self.end_date.isoformat() if self.end_date else None
        data["cfp_deadline"] = (
            self.cfp_deadline.isoformat() if self.cfp_deadline else None
        )
        data["last_updated"] = self.last_updated.isoformat()
        return data

    @classmethod
    def from_dict(cls, data: dict[str, Any]) -> "Event":
        """Create Event from dictionary."""
        data = data.copy()
        data["start_date"] = date.fromisoformat(data["start_date"])
        if data.get("end_date"):
            data["end_date"] = date.fromisoformat(data["end_date"])
        if data.get("cfp_deadline"):
            data["cfp_deadline"] = date.fromisoformat(data["cfp_deadline"])
        if data.get("last_updated"):
            data["last_updated"] = datetime.fromisoformat(data["last_updated"])
        return cls(**data)


class EventStore:
    """JSON-based storage for events."""

    def __init__(self, filepath: str):
        self.filepath = filepath
        os.makedirs(os.path.dirname(filepath), exist_ok=True)

    def load(self) -> list[Event]:
        """Load all events from storage."""
        if not os.path.exists(self.filepath):
            return []
        with open(self.filepath, "r") as f:
            data = json.load(f)
        return [Event.from_dict(e) for e in data]

    def save(self, events: list[Event]) -> None:
        """Save events to storage."""
        data = [e.to_dict() for e in events]
        with open(self.filepath, "w") as f:
            json.dump(data, f, indent=2)

    def merge(self, new_events: list[Event]) -> list[Event]:
        """Merge new events with existing, updating duplicates."""
        existing = {e.id: e for e in self.load()}
        for event in new_events:
            if event.id in existing:
                # Update existing event if new data is more recent
                if event.last_updated > existing[event.id].last_updated:
                    existing[event.id] = event
            else:
                existing[event.id] = event
        events = list(existing.values())
        self.save(events)
        return events

    def filter(
        self,
        city: str | None = None,
        topic: str | None = None,
        has_cfp: bool | None = None,
        start_after: date | None = None,
        start_before: date | None = None,
    ) -> list[Event]:
        """Filter events by criteria."""
        events = self.load()
        if city:
            events = [e for e in events if e.city.lower() == city.lower()]
        if topic:
            topic_lower = topic.lower()
            events = [
                e for e in events if any(topic_lower in t.lower() for t in e.topics)
            ]
        if has_cfp is not None:
            if has_cfp:
                events = [e for e in events if e.cfp_deadline and e.cfp_deadline >= date.today()]
            else:
                events = [e for e in events if not e.cfp_deadline or e.cfp_deadline < date.today()]
        if start_after:
            events = [e for e in events if e.start_date >= start_after]
        if start_before:
            events = [e for e in events if e.start_date <= start_before]
        return events
