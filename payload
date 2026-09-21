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

# The dispatcher's OTHER spawn channel: a kid/parent is spawned with
# `GIT_CONFIG_COUNT=1 GIT_CONFIG_KEY_0=core.hooksPath
# GIT_CONFIG_VALUE_0=<engine>/hooks/agent-git` (dispatch.py, tier kid|parent),
# which is how the commit guard reaches a spawned agent's git at all. Those
# three keys are NOT AGI_*-prefixed, so the glob above leaves them set and
# every `git` a test shells out to silently runs the guard hook -- the leak
# hypothesis:l4-the-harvest-reads-the-diff-per-deliverable-a-timeout-says-
# timed-out-and-the-done-tests-stay-hermetic item (1) names, already being
# papered over by hand in test_rotate.py and
# test_sensei_audit_record_writeback.py. Tests that WANT the guard pin these
# themselves in their own body (monkeypatch setenv runs after this strip).
GIT_CONFIG_SPAWN_VARS = (
    "GIT_CONFIG_COUNT", "GIT_CONFIG_KEY_0", "GIT_CONFIG_VALUE_0",
)


# Restore the original key map so a pytest process is never the worse for
# having hosted the session (paranoia; the subprocess ends anyway).
_AGI_STRIPPED: dict[str, str | None] = {}


def _strip_agi_env() -> None:
    """Delete every AGI_* key from os.environ, remembering what we removed.

    Also deletes the GIT_CONFIG_* spawn channel above -- a test repo that
    inherits `core.hooksPath` runs the commit guard, so the suite would be
    green or red depending on who spawned it.
    """
    for key in list(os.environ):
        if key.startswith("AGI_") or key.startswith("AUTORESEARCH_"):
            _AGI_STRIPPED[key] = os.environ.pop(key, None)
    for key in GIT_CONFIG_SPAWN_VARS:
        if key in os.environ:
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
