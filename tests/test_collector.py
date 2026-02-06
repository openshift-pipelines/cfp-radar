"""Tests for event collectors."""

from datetime import date

from src.collector.agent import _event_completeness, _normalize_name, deduplicate_events
from src.collector.models import Event


class TestDeduplication:
    def test_normalize_name(self):
        assert _normalize_name("KubeCon 2026") == "kubecon"
        assert _normalize_name("DevOpsDays Conference Paris") == "devopsdays paris"
        assert _normalize_name("Cloud Native Summit 2026") == "cloud native"

    def test_deduplicate_identical_events(self):
        events = [
            Event(
                name="Test Event",
                city="Paris",
                country="France",
                start_date=date(2026, 4, 1),
                website="https://test.com",
            ),
            Event(
                name="Test Event",
                city="Paris",
                country="France",
                start_date=date(2026, 4, 1),
                website="https://test.com",
            ),
        ]
        result = deduplicate_events(events)
        assert len(result) == 1

    def test_keep_more_complete_event(self):
        events = [
            Event(
                name="Test Event",
                city="Paris",
                country="France",
                start_date=date(2026, 4, 1),
                website="https://test.com",
            ),
            Event(
                name="Test Event",
                city="Paris",
                country="France",
                start_date=date(2026, 4, 1),
                website="https://test.com",
                cfp_deadline=date(2026, 3, 1),
                cfp_url="https://test.com/cfp",
                description="A great event",
            ),
        ]
        result = deduplicate_events(events)
        assert len(result) == 1
        assert result[0].cfp_deadline is not None
        assert result[0].description == "A great event"

    def test_different_dates_not_deduplicated(self):
        events = [
            Event(
                name="Annual Conference",
                city="Paris",
                country="France",
                start_date=date(2026, 4, 1),
                website="https://test.com",
            ),
            Event(
                name="Annual Conference",
                city="Paris",
                country="France",
                start_date=date(2027, 4, 1),
                website="https://test.com",
            ),
        ]
        result = deduplicate_events(events)
        assert len(result) == 2


class TestEventCompleteness:
    def test_empty_event(self):
        event = Event(
            name="Basic",
            city="Paris",
            country="France",
            start_date=date(2026, 4, 1),
            website="https://test.com",
        )
        score = _event_completeness(event)
        assert score == 1  # Just website

    def test_complete_event(self):
        event = Event(
            name="Complete Event",
            city="Paris",
            country="France",
            start_date=date(2026, 4, 1),
            end_date=date(2026, 4, 3),
            website="https://test.com",
            description="A conference",
            cfp_deadline=date(2026, 3, 1),
            cfp_url="https://test.com/cfp",
            topics=["devops", "kubernetes"],
        )
        score = _event_completeness(event)
        # description(1) + cfp_deadline(2) + cfp_url(2) + website(1) + end_date(1) + topics(2)
        assert score == 9
