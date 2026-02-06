"""Configuration for the event tracker."""

from __future__ import annotations

import os

import yaml

DEFAULT_CONFIG_FILE = os.path.join(os.path.dirname(os.path.dirname(__file__)), "config.yaml")
_config_file: str | None = None


def set_config_file(path: str) -> None:
    """Set the config file path for subsequent load calls."""
    global _config_file
    _config_file = path


def load_countries(config_file: str | None = None) -> list[str]:
    """Load countries from YAML config file."""
    path = config_file or _config_file or DEFAULT_CONFIG_FILE
    if os.path.exists(path):
        with open(path) as f:
            data = yaml.safe_load(f)
            result: list[str] = data.get("countries", [])
            return result
    return []


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


TARGET_COUNTRIES = load_countries()
GLOBAL_CONFERENCES = load_global_conferences()
TOPICS = load_topics()

GEMINI_API_KEY = os.environ.get("GEMINI_API_KEY", "")
SLACK_WEBHOOK_URL = os.environ.get("SLACK_WEBHOOK_URL", "")
MEETUP_API_KEY = os.environ.get("MEETUP_API_KEY", "")

DATA_DIR = os.path.join(os.path.dirname(os.path.dirname(__file__)), "data")
EVENTS_FILE = os.path.join(DATA_DIR, "events.json")
