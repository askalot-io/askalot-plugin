"""
Demographic profile management for respondent agents.

Profiles define demographic characteristics that influence how respondent agents
answer survey questions. Each profile is stored as a markdown file with YAML
frontmatter for metadata.

Profiles are loaded from:
1. ASKALOT_PROMPTS_DIR/profiles/ (if ASKALOT_PROMPTS_DIR is set)
2. Module's local profiles/ folder (default)

The parsed profile set is cached at process level — profiles do not
change at runtime.
"""

import logging
import os
from functools import lru_cache
from pathlib import Path
from typing import Any, Optional

from askalot_ai.prompts.loader import parse_frontmatter

logger = logging.getLogger(__name__)

_LOCAL_PROFILES_DIR = Path(__file__).parent


def _get_profiles_dir() -> Path:
    """Get the profiles directory, with environment override support."""
    env_dir = os.environ.get("ASKALOT_PROMPTS_DIR")
    if env_dir:
        return Path(env_dir) / "profiles"
    return _LOCAL_PROFILES_DIR


def _parse_profile_file(file_path: Path) -> dict[str, Any]:
    """Parse a profile markdown file with YAML frontmatter.

    Returns a dict with ``name``, ``description``, and ``details`` keys.
    """
    content = file_path.read_text(encoding="utf-8")
    metadata, body = parse_frontmatter(content)
    fallback_name = file_path.stem.replace("_", " ").title()
    return {
        "name": metadata.get("name", fallback_name),
        "description": metadata.get("description", ""),
        "details": body,
    }


@lru_cache(maxsize=1)
def _load_all_profiles_cached(profiles_dir: Path) -> dict[str, dict[str, Any]]:
    """Glob + parse every ``.md`` profile under ``profiles_dir``.

    Profiles are static within a process, so the result is memoized by
    directory. The cache key includes the directory so an env-var
    override flips cleanly in tests.
    """
    if not profiles_dir.exists():
        raise FileNotFoundError(f"Profiles directory not found: {profiles_dir}")

    profiles = {
        profile_file.stem: _parse_profile_file(profile_file)
        for profile_file in profiles_dir.glob("*.md")
    }
    if not profiles:
        raise FileNotFoundError(f"No profile files found in: {profiles_dir}")
    return profiles


def _load_all_profiles() -> dict[str, dict[str, Any]]:
    """Load all profile files from the active profiles directory."""
    return _load_all_profiles_cached(_get_profiles_dir())


def get_available_profiles() -> dict[str, dict[str, Any]]:
    """Get all available demographic profiles."""
    return _load_all_profiles()


def get_profile_details(profile_name: str) -> str:
    """Return the demographic details body for a profile.

    Unknown names fall back to ``random`` with a warning so callers see
    the substitution in logs. Raises ``FileNotFoundError`` if neither
    the named profile nor ``random`` exists.
    """
    profiles = _load_all_profiles()
    if profile_name in profiles:
        return profiles[profile_name]["details"]

    logger.warning("Unrecognized profile %r, falling back to random", profile_name)
    if "random" not in profiles:
        raise FileNotFoundError(f"Profile not found: {profile_name}")
    return profiles["random"]["details"]


def list_available_profiles() -> list[dict[str, str]]:
    """List all available demographic profiles."""
    return [
        {
            "name": name,
            "display_name": profile["name"],
            "description": profile["description"],
        }
        for name, profile in _load_all_profiles().items()
    ]


def get_profile_for_index(index: int, profiles: list[str] | None = None) -> str:
    """Get a profile name for a given index (for distributing profiles across respondents)."""
    if profiles is None:
        profiles = list(_load_all_profiles().keys())
    return profiles[index % len(profiles)]
