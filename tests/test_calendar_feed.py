"""Tests for ICS calendar feed generation."""

from __future__ import annotations

import tempfile
from datetime import date

from icalendar import Calendar  # type: ignore[import-untyped]

from src.calendar_feed import generate_ics
from src.collector.models import Event


def _make_event(**kwargs: object) -> Event:
    defaults: dict[str, object] = {
        "name": "Test Conf",
        "city": "Paris",
        "country": "France",
        "start_date": date(2026, 6, 15),
        "website": "https://testconf.example.com",
    }
    defaults.update(kwargs)
    return Event(**defaults)  # type: ignore[arg-type]


def _generate_and_parse(events: list[Event]) -> Calendar:
    with tempfile.NamedTemporaryFile(suffix=".ics", delete=False) as f:
        path = f.name
    generate_ics(events, path)
    with open(path, "rb") as f:
        return Calendar.from_ical(f.read())


class TestCalendarHeaders:
    def test_valid_ics_headers(self) -> None:
        cal = _generate_and_parse([])
        assert cal["prodid"] == "-//CFP Radar//cfp-radar//EN"
        assert cal["version"] == "2.0"
        assert cal["x-wr-calname"] == "CFP Radar"

    def test_empty_event_list_produces_valid_calendar(self) -> None:
        cal = _generate_and_parse([])
        vevents = [c for c in cal.walk() if c.name == "VEVENT"]
        assert vevents == []


class TestEventEntries:
    def test_event_without_cfp_produces_one_vevent(self) -> None:
        event = _make_event()
        cal = _generate_and_parse([event])
        vevents = [c for c in cal.walk() if c.name == "VEVENT"]
        assert len(vevents) == 1
        assert vevents[0]["summary"] == "Test Conf"

    def test_event_with_cfp_produces_two_vevents(self) -> None:
        event = _make_event(
            cfp_deadline=date(2026, 4, 1),
            cfp_url="https://cfp.example.com",
        )
        cal = _generate_and_parse([event])
        vevents = [c for c in cal.walk() if c.name == "VEVENT"]
        assert len(vevents) == 2
        summaries = {str(v["summary"]) for v in vevents}
        assert "[CFP Deadline] Test Conf" in summaries
        assert "Test Conf" in summaries


class TestTransparency:
    def test_cfp_entry_is_transparent(self) -> None:
        event = _make_event(cfp_deadline=date(2026, 4, 1))
        cal = _generate_and_parse([event])
        vevents = [c for c in cal.walk() if c.name == "VEVENT"]
        cfp_entry = next(v for v in vevents if "CFP Deadline" in str(v["summary"]))
        assert str(cfp_entry["transp"]) == "TRANSPARENT"

    def test_event_entry_is_opaque(self) -> None:
        event = _make_event()
        cal = _generate_and_parse([event])
        vevents = [c for c in cal.walk() if c.name == "VEVENT"]
        assert str(vevents[0]["transp"]) == "OPAQUE"


class TestDateSpanning:
    def test_single_day_event(self) -> None:
        event = _make_event(start_date=date(2026, 6, 15))
        cal = _generate_and_parse([event])
        vevents = [c for c in cal.walk() if c.name == "VEVENT"]
        ev = vevents[0]
        assert ev["dtstart"].dt == date(2026, 6, 15)
        # DTEND is exclusive: single day means next day
        assert ev["dtend"].dt == date(2026, 6, 16)

    def test_multi_day_event(self) -> None:
        event = _make_event(
            start_date=date(2026, 6, 15),
            end_date=date(2026, 6, 18),
        )
        cal = _generate_and_parse([event])
        vevents = [c for c in cal.walk() if c.name == "VEVENT"]
        ev = vevents[0]
        assert ev["dtstart"].dt == date(2026, 6, 15)
        # DTEND exclusive: 18th inclusive means DTEND=19th
        assert ev["dtend"].dt == date(2026, 6, 19)


class TestUIDs:
    def test_stable_uids(self) -> None:
        event = _make_event(cfp_deadline=date(2026, 4, 1))
        cal1 = _generate_and_parse([event])
        cal2 = _generate_and_parse([event])
        uids1 = sorted(str(v["uid"]) for v in cal1.walk() if v.name == "VEVENT")
        uids2 = sorted(str(v["uid"]) for v in cal2.walk() if v.name == "VEVENT")
        assert uids1 == uids2

    def test_uid_format(self) -> None:
        event = _make_event(cfp_deadline=date(2026, 4, 1))
        cal = _generate_and_parse([event])
        uids = {str(v["uid"]) for v in cal.walk() if v.name == "VEVENT"}
        assert any(uid.endswith("-cfp@cfp-radar") for uid in uids)
        assert any(uid.endswith("-event@cfp-radar") for uid in uids)


class TestDescription:
    def test_description_includes_website(self) -> None:
        event = _make_event(website="https://testconf.example.com")
        cal = _generate_and_parse([event])
        vevents = [c for c in cal.walk() if c.name == "VEVENT"]
        desc = str(vevents[0]["description"])
        assert "https://testconf.example.com" in desc

    def test_description_includes_cfp_url(self) -> None:
        event = _make_event(
            cfp_deadline=date(2026, 4, 1),
            cfp_url="https://cfp.example.com",
        )
        cal = _generate_and_parse([event])
        vevents = [c for c in cal.walk() if c.name == "VEVENT"]
        for v in vevents:
            desc = str(v["description"])
            assert "https://cfp.example.com" in desc

    def test_description_includes_topics(self) -> None:
        event = _make_event(topics=["Kubernetes", "CI/CD"])
        cal = _generate_and_parse([event])
        vevents = [c for c in cal.walk() if c.name == "VEVENT"]
        desc = str(vevents[0]["description"])
        assert "Kubernetes" in desc
        assert "CI/CD" in desc


class TestLocation:
    def test_location_format(self) -> None:
        event = _make_event(city="Berlin", country="Germany")
        cal = _generate_and_parse([event])
        vevents = [c for c in cal.walk() if c.name == "VEVENT"]
        assert str(vevents[0]["location"]) == "Berlin, Germany"
