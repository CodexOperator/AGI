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
#: The ONE home for the suite guards, by PLAIN import -- the same module the
#: declared context suite imports, never an exec of another conftest.
_BIN = str(Path(__file__).parent / "bin")
if _BIN not in sys.path:
    sys.path.insert(0, _BIN)
import suite_guards  # noqa: E402


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
GIT_CONFIG_SPAWN_VARS = suite_guards.GIT_CONFIG_SPAWN_VARS


# Restore the original key map so a pytest process is never the worse for
# having hosted the session (paranoia; the subprocess ends anyway).
_AGI_STRIPPED: dict[str, str | None] = {}


def _strip_agi_env() -> None:
    """Delete every AGI_* key from os.environ, remembering what we removed.

    Also deletes the GIT_CONFIG_* spawn channel above -- a test repo that
    inherits `core.hooksPath` runs the commit guard, so the suite would be
    green or red depending on who spawned it.

    The BODY is `suite_guards.strip_dispatch_env`, with this conftest's policy
    passed as `extra_keys`; the context suite passes none, so the git-hook
    strip cannot leak into it. This seam stays put: test_agi_env_strip.py
    drives THIS function by path.
    """
    suite_guards.strip_dispatch_env(GIT_CONFIG_SPAWN_VARS, memo=_AGI_STRIPPED)


def _restore_agi_env() -> None:
    """Put back whatever the fixture removed (session teardown)."""
    suite_guards.restore_dispatch_env(_AGI_STRIPPED)


import pytest


#: Session-scoped autouse: strip dispatch spawn vars before collection. ONE
#: body, this suite's policy -- the AGI_*/AUTORESEARCH_* channel PLUS the
#: dispatcher's git-hook channel.
_agi_env_stripped = suite_guards.make_agi_env_stripped_fixture(
    GIT_CONFIG_SPAWN_VARS)
