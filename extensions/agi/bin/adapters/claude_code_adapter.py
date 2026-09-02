"""The Claude Code harness — declared, deliberately not implemented.

`goal:g4.6`. This file exists so the config entry for `claude-code` resolves to
something honest instead of an `AdapterError` that reads like a typo. It raises
where the work would go, naming the goal.

**Why it is a stub and not the second half of the unification:** the owner's
call on 2026-09-01 is that pi is the primary platform now that OpenRouter is
reachable, so pi gets the working path first and Claude Code follows once the
seam has been proven by use. That ordering is the opposite of `goal:g4.3`'s,
which treated the two runtimes as peers reaching parity, and it is the
correction `goal:g4.6` exists to make.

**The interface is the contract, and it is already fixed** -- whoever writes
this implements `build_command` and `child_env` with the same signatures
`pi_adapter` uses, adds a `claude-code` entry to `harnesses`, and touches
nothing else. If it needs a change in `dispatch.py`, the seam was in the wrong
place and `mvp:unified-spawn-path`'s first falsifier has failed.

Two things known in advance, both real constraints rather than details:

  - **Claude Code spawns Claude models only.** There is no setting that points
    a CC agent at OpenRouter. So this adapter's `models` are Claude ids, and a
    project wanting an OpenRouter model must select the pi harness.
  - **The env scrub runs the other way.** `dispatch.scrubbed_env` strips
    `ANTHROPIC_*`/`CLAUDE_CODE_*` so pi children cannot bill the interactive
    subscription. A CC child legitimately needs some of what that scrub
    removes, which is exactly why `child_env` is per-adapter rather than one
    shared function -- and exactly the thing to get right, since the scrub
    exists because the leak already happened once.
"""
from __future__ import annotations

from pathlib import Path

NAME = "claude-code"

_MSG = (
    "the claude-code adapter is declared in config but not implemented "
    "(goal:g4.6). pi is the primary harness; select it with "
    "`spawn.harness: \"pi\"`, or implement build_command/child_env here with "
    "the same signatures pi_adapter uses."
)


def build_command(
    *,
    harness: dict,
    tier: str,
    context_file: str,
    agent_id: str,
    iter_n: int,
    sess_dir: Path,
    scaffold: dict | None = None,
    cli_py: str | Path = "",
    skill_prompt: Path | None = None,
    dispatch_py: str | Path = "",
    target: str | None = None,
    parallel: int = 1,
    max_live: int = 1,
) -> list[str]:
    # The full pi_adapter signature, deliberately, even though every call
    # raises. Accepting fewer keywords than the caller passes turns the
    # designed `NotImplementedError` -- which dispatch.py catches and reports
    # as a config error naming the harness -- into an uncaught `TypeError`
    # traceback from inside an adapter. The stub has to be reachable to be a
    # stub.
    raise NotImplementedError(_MSG)


def child_env(*, harness: dict, base: dict[str, str]) -> dict[str, str]:
    raise NotImplementedError(_MSG)


def is_alive(pid: int) -> bool:
    """Stub — not implemented for claude-code harness."""
    raise NotImplementedError(_MSG)


def restart(
    *,
    harness: dict,
    tier: str,
    context_file: str,
    agent_id: str,
    iter_n: int,
    sess_dir: Path,
    scaffold: dict | None = None,
    cli_py: str | Path = "",
    skill_prompt: Path | None = None,
    dispatch_py: str | Path = "",
    target: str | None = None,
    parallel: int = 1,
    max_live: int = 1,
    agent_record: dict | None = None,
) -> int | None:
    """Stub — not implemented for claude-code harness."""
    raise NotImplementedError(_MSG)
