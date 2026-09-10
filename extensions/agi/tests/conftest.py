"""Collection-time tier gate (goal:g15.6, hypothesis:l4-full-suite-tier-gate).

A brief-level instruction is not a mechanism: text in a node cannot refuse
anything. This conftest makes the "run a targeted path, not the whole suite"
rule a real gate for kid agents.

The signal already exists -- dispatch.py exports AGI_TIER into every spawn's
environment (a kid runs under AGI_TIER=kid). We only READ it here; nothing
else in production changes and no existing test is edited.

RULE (fire before collection, exit uncollected):
  * AGI_TIER == "kid"  AND  the invocation is a BARE DIRECTORY run
    (no specific test file named, no -k filter)  ->  REFUSED, one-line reason.
  * any other case  ->  behaviour exactly as today, including a bare
    directory run at every tier other than kid.

Which hook and why: ``pytest_cmdline_main(config)``. It fires immediately
after the command line has been parsed but BEFORE any collection begins, so a
refusal cannot be bypassed by letting collection start. At that point
``config.args`` still holds the positional paths the invocation named and
``config.option.kw`` holds the -k filter; both are exactly what we need to
tell a bare directory run from a targeted one.
"""
from __future__ import annotations

import os

import pytest

GATE_TIER = "kid"
REFUSAL_REASON = (
    "AGI_TIER=kid refuses a bare full-suite directory run; "
    "run a specific test file or a -k filter instead."
)


def _named_paths(args):
    """Return the positional args that look like paths (drop flag tokens)."""
    return [a for a in (args or []) if a and not a.startswith("-")]


def _is_bare_directory_run(config) -> bool:
    """True when this invocation collects a whole directory with no target.

    Bare means: no -k filter AND every path argument is a directory (or there
    is no path argument at all, so pytest falls back to the configured
    testpaths). Naming any specific ``.py`` test file makes it a targeted run.
    """
    option = getattr(config, "option", None)
    # In pytest the -k filter lands on option.keyword (not option.kw).
    kw = getattr(option, "keyword", None) or getattr(option, "kw", None)
    if kw:
        return False
    paths = _named_paths(getattr(config, "args", None))
    if not paths:
        # No path named -> bare directory run (routes to testpaths).
        return True
    # Refuse only if EVERY named arg is a directory (no explicit test file).
    return all(p.endswith(os.sep) or os.path.isdir(p) or not p.endswith(".py") for p in paths)


def pytest_cmdline_main(config):
    if os.environ.get("AGI_TIER") != GATE_TIER:
        # Invisible at every tier other than kid, and when the var is unset.
        return
    if _is_bare_directory_run(config):
        raise pytest.UsageError(REFUSAL_REASON)