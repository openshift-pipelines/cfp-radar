"""Tests for data models."""

import os
import tempfile
from datetime import date

from src.collector.models import Event, EventStore


class TestEvent:
    def test_create_event(self):
        event = Event(
            name="KubeCon Europe",
            city="Paris",
            country="France",
            start_date=date(2026, 3, 17),
            website="https://kubecon.io",
        )
        assert event.name == "KubeCon Europe"
        assert event.city == "Paris"
        assert event.id  # Auto-generated

    def test_event_id_generation(self):
        event1 = Event(
            name="Test Event",
            city="Paris",
            country="France",
            start_date=date(2026, 3, 17),
            website="https://example.com",
        )
        event2 = Event(
            name="Test Event",
            city="Paris",
            country="France",
            start_date=date(2026, 3, 17),
            website="https://example.com",
        )
        # Same name and date should generate same ID
        assert event1.id == event2.id

    def test_event_to_dict(self):
        event = Event(
            name="DevOpsDays",
            city="Bangalore",
            country="India",
            start_date=date(2026, 5, 15),
            end_date=date(2026, 5, 16),
            cfp_deadline=date(2026, 3, 1),
            website="https://devopsdays.org",
            topics=["devops", "kubernetes"],
        )
        data = event.to_dict()
        assert data["name"] == "DevOpsDays"
        assert data["start_date"] == "2026-05-15"
        assert data["end_date"] == "2026-05-16"
        assert data["cfp_deadline"] == "2026-03-01"
        assert "devops" in data["topics"]

    def test_event_from_dict(self):
        data = {
            "id": "abc123",
            "name": "Test Conf",
            "city": "Tel Aviv",
            "country": "Israel",
            "start_date": "2026-06-10",
            "end_date": None,
            "event_type": "conference",
            "topics": ["ci/cd"],
            "cfp_deadline": "2026-04-01",
            "cfp_url": "https://example.com/cfp",
            "website": "https://example.com",
            "description": "A test conference",
            "relevance_score": 0.8,
            "last_updated": "2026-01-01T12:00:00",
        }
        event = Event.from_dict(data)
        assert event.name == "Test Conf"
        assert event.start_date == date(2026, 6, 10)
        assert event.cfp_deadline == date(2026, 4, 1)


class TestEventStore:
    def test_save_and_load(self):
        with tempfile.TemporaryDirectory() as tmpdir:
            filepath = os.path.join(tmpdir, "events.json")
            store = EventStore(filepath)

            events = [
                Event(
                    name="Event 1",
                    city="Paris",
                    country="France",
                    start_date=date(2026, 4, 1),
                    website="https://event1.com",
                ),
                Event(
                    name="Event 2",
                    city="Brno",
                    country="Czech Republic",
                    start_date=date(2026, 5, 1),
                    website="https://event2.com",
                ),
            ]

            store.save(events)
            loaded = store.load()

            assert len(loaded) == 2
            assert loaded[0].name == "Event 1"
            assert loaded[1].name == "Event 2"

    def test_merge_events(self):
        with tempfile.TemporaryDirectory() as tmpdir:
            filepath = os.path.join(tmpdir, "events.json")
            store = EventStore(filepath)

            # Initial events
            initial = [
                Event(
                    name="Event A",
                    city="Raleigh",
                    country="USA",
                    start_date=date(2026, 6, 1),
                    website="https://eventa.com",
                ),
            ]
            store.save(initial)

            # New events including duplicate
            new_events = [
                Event(
                    name="Event A",  # Duplicate
                    city="Raleigh",
                    country="USA",
                    start_date=date(2026, 6, 1),
                    website="https://eventa.com",
                    cfp_deadline=date(2026, 4, 1),  # New info
                ),
                Event(
                    name="Event B",
                    city="Pune",
                    country="India",
                    start_date=date(2026, 7, 1),
                    website="https://eventb.com",
                ),
            ]

            merged = store.merge(new_events)
            assert len(merged) == 2

    def test_filter_by_city(self):
        with tempfile.TemporaryDirectory() as tmpdir:
            filepath = os.path.join(tmpdir, "events.json")
            store = EventStore(filepath)

            events = [
                Event(
                    name="Paris Event",
                    city="Paris",
                    country="France",
                    start_date=date(2026, 4, 1),
                    website="https://paris.com",
                ),
                Event(
                    name="Bangalore Event",
                    city="Bangalore",
                    country="India",
                    start_date=date(2026, 5, 1),
                    website="https://bangalore.com",
                ),
            ]
            store.save(events)

            paris_events = store.filter(city="Paris")
            assert len(paris_events) == 1
            assert paris_events[0].city == "Paris"

    def test_filter_by_cfp(self):
        with tempfile.TemporaryDirectory() as tmpdir:
            filepath = os.path.join(tmpdir, "events.json")
            store = EventStore(filepath)

            future_date = date(2030, 12, 31)
            events = [
                Event(
                    name="With CFP",
                    city="Paris",
                    country="France",
                    start_date=date(2030, 4, 1),
                    website="https://withcfp.com",
                    cfp_deadline=future_date,
                ),
                Event(
                    name="No CFP",
                    city="Paris",
                    country="France",
                    start_date=date(2030, 5, 1),
                    website="https://nocfp.com",
                ),
            ]
            store.save(events)

            cfp_events = store.filter(has_cfp=True)
            assert len(cfp_events) == 1
            assert cfp_events[0].name == "With CFP"
