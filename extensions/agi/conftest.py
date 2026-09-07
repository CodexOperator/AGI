"""Pytest conftest — adds src/ to sys.path for clean test imports, and
strips the dispatch spawn variables so a kid/parent verification never
depends on (or is polluted by) its spawning environment.

Dispatch exports AGI_LOOP, AGI_MODEL, AGI_ROLE, AGI_TIER, AGI_SEASON,
AGI_PROFILE, AGI_PROJECT_ROOT and siblings into the spawned agent's env
(hypothesis:l3-dispatch-env-leaks-into-tests). A spawning agent must get the
same green suite as a clean shell, so this session-scoped autouse fixture
deletes every AGI_* key from os.environ before any test imports, keeping the
variables in the spawning process untouched.
"""

import os
import sys
from pathlib import Path

sys.path.insert(0, str(Path(__file__).parent / "src"))


# Documented dispatch variables (the known spawn set). The fixture walks the
# whole os.environ for a glob anyway, so this list is documentation plus a
# canary the test suite can assert against.
AGI_DISPATCH_VARS = (
    "AGI_LOOP", "AGI_MODEL", "AGI_ROLE", "AGI_TIER", "AGI_SEASON",
    "AGI_PROFILE", "AGI_PROJECT_ROOT", "AGI_LADDER_TIER",
    "AGI_TREE_PROJECT_ROOT", "AUTORESEARCH_TREE_PROJECT_ROOT",
)


# Restore the original key map so a pytest process is never the worse for
# having hosted the session (paranoia; the subprocess ends anyway).
_AGI_STRIPPED: dict[str, str | None] = {}


def _strip_agi_env() -> None:
    """Delete every AGI_* key from os.environ, remembering what we removed."""
    for key in list(os.environ):
        if key.startswith("AGI_") or key.startswith("AUTORESEARCH_"):
            _AGI_STRIPPED[key] = os.environ.pop(key, None)


def _restore_agi_env() -> None:
    """Put back whatever the fixture removed (session teardown)."""
    for key, value in _AGI_STRIPPED.items():
        if value is None:
            os.environ.pop(key, None)
        else:
            os.environ[key] = value


import pytest


@pytest.fixture(scope="session", autouse=True)
def _agi_env_stripped():
    """Session-scoped autouse: strip dispatch spawn vars before collection."""
    _strip_agi_env()
    yield
    _restore_agi_env()
