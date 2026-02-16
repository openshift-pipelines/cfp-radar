"""Configuration for the event tracker."""

from __future__ import annotations

import os

import yaml

REGION_TO_COUNTRIES: dict[str, list[str]] = {
    "North America": ["USA", "Canada"],
    "Europe": [
        "Netherlands",
        "Spain",
        "France",
        "Germany",
        "UK",
        "Denmark",
        "Belgium",
        "Ireland",
        "Sweden",
        "Switzerland",
        "Poland",
        "Austria",
        "Italy",
        "Portugal",
        "Czech Republic",
        "Finland",
        "Norway",
        "Greece",
    ],
    "Asia Pacific": [
        "India",
        "China",
        "Japan",
        "Singapore",
        "Australia",
        "South Korea",
        "Taiwan",
    ],
    "Middle East": ["Israel", "UAE"],
    "Latin America": ["Brazil", "Argentina", "Mexico"],
}

COUNTRY_ALIASES: dict[str, str] = {
    "u.s.a.": "USA",
    "u.s.a": "USA",
    "u.s.": "USA",
    "usa": "USA",
    "united states": "USA",
    "united states of america": "USA",
    "us": "USA",
    "america": "USA",
    "uk": "UK",
    "united kingdom": "UK",
    "great britain": "UK",
    "england": "UK",
    "uae": "UAE",
    "united arab emirates": "UAE",
}


def normalize_country(country: str) -> str:
    """Normalize country name variants to canonical form."""
    return COUNTRY_ALIASES.get(country.lower().strip(), country)


DEFAULT_CONFIG_FILE = os.path.join(os.path.dirname(os.path.dirname(__file__)), "config.yaml")
_config_file: str | None = None


def set_config_file(path: str) -> None:
    """Set the config file path for subsequent load calls."""
    global _config_file
    _config_file = path


def load_regions(config_file: str | None = None) -> list[str]:
    """Load region names from YAML config file."""
    path = config_file or _config_file or DEFAULT_CONFIG_FILE
    if os.path.exists(path):
        with open(path) as f:
            data = yaml.safe_load(f)
            result: list[str] = data.get("regions", [])
            return result
    return []


def load_countries(config_file: str | None = None) -> list[str]:
    """Load countries by expanding regions from YAML config file."""
    regions = load_regions(config_file)
    countries: list[str] = []
    for region in regions:
        countries.extend(REGION_TO_COUNTRIES.get(region, []))
    return countries


def load_global_conferences(config_file: str | None = None) -> list[str]:
    """Load global conferences from YAML config file."""
    path = config_file or _config_file or DEFAULT_CONFIG_FILE
    if os.path.exists(path):
        with open(path) as f:
            data = yaml.safe_load(f)
            result: list[str] = data.get("global_conferences", [])
            return result
    return []


def load_topics(config_file: str | None = None) -> list[str]:
    """Load topics from YAML config file."""
    path = config_file or _config_file or DEFAULT_CONFIG_FILE
    if os.path.exists(path):
        with open(path) as f:
            data = yaml.safe_load(f)
            result: list[str] = data.get("topics", [])
            return result
    # Fallback defaults if config not found
    return [
        "ci/cd",
        "continuous integration",
        "continuous delivery",
        "devops",
        "platform engineering",
        "cloud native",
        "kubernetes",
        "containers",
        "gitops",
        "tekton",
    ]


TARGET_REGIONS = load_regions()
TARGET_COUNTRIES = load_countries()
GLOBAL_CONFERENCES = load_global_conferences()
TOPICS = load_topics()

GEMINI_API_KEY = os.environ.get("GEMINI_API_KEY", "")
SLACK_WEBHOOK_URL = os.environ.get("SLACK_WEBHOOK_URL", "")
MEETUP_API_KEY = os.environ.get("MEETUP_API_KEY", "")

DATA_DIR = os.path.join(os.path.dirname(os.path.dirname(__file__)), "data")
EVENTS_FILE = os.path.join(DATA_DIR, "events.json")
