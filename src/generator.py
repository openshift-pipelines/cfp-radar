"""Static HTML generator for events."""

from __future__ import annotations

import os
import shutil
from datetime import date

from jinja2 import Environment, FileSystemLoader

from .collector.models import Event
from .config import TOPICS


def generate_html(events: list[Event], output_file: str) -> None:
    """Generate static HTML file from events.

    Args:
        events: List of Event objects
        output_file: Path to write HTML file to
    """

    # Sort by CFP deadline (upcoming first), then by start date
    def sort_key(e: Event) -> tuple[date, date]:
        cfp_priority = e.cfp_deadline if e.cfp_deadline else date(2099, 12, 31)
        return (cfp_priority, e.start_date)

    events = sorted(events, key=sort_key)

    # Extract unique countries with counts
    country_counts: dict[str, int] = {}
    for event in events:
        country = event.country
        country_counts[country] = country_counts.get(country, 0) + 1

    # Sort countries by count (most events first)
    countries = sorted(country_counts.items(), key=lambda x: x[1], reverse=True)

    # Setup Jinja2 templates
    templates_dir = os.path.join(os.path.dirname(__file__), "web", "templates")
    env = Environment(loader=FileSystemLoader(templates_dir), autoescape=True)
    template = env.get_template("index.html")

    html = template.render(
        events=events,
        topics=TOPICS[:8],
        selected_topic=None,
        has_cfp=None,
        today=date.today(),
        countries=countries,
    )

    # Ensure output directory exists
    output_dir = os.path.dirname(output_file)
    if output_dir:
        os.makedirs(output_dir, exist_ok=True)

    # Write the HTML file
    with open(output_file, "w", encoding="utf-8") as f:
        f.write(html)

    # Copy optimized logo to output directory
    logo_src = os.path.join("data", "logo.webp")
    if os.path.exists(logo_src):
        logo_dst = os.path.join(output_dir, "logo.webp")
        if not os.path.exists(logo_dst):
            shutil.copy2(logo_src, logo_dst)
