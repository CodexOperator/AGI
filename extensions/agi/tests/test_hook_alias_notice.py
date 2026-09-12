"""hypothesis:l4-the-dry-run-pathspec-and-the-alias-notice-say-only-what-is-true
REGION C — the SessionStart hook must invoke the CURRENT seat spelling
(`--post`), so the deprecated-alias notice is never emitted for a session
that uses none of the deprecated spellings (`--seat`, AGI_SEAT,
config:seats).

The deprecated-alias notice is written to the CONSUMER's stderr by
`geometry_config` (a literal `--seat` on a shared parser fires
`_FLAG_DEP_MSG`; using AGI_SEAT fires `_ENV_DEP_MSG`; the seats.md fallback
fires `_FILE_DEP_MSG`). The acceptance criterion is framed at the
observable boundary of a real hook RUN: run the hook once with a deprecated
env spelling in use (AGI_SEAT, no AGI_POST) and once with only the current
spelling (AGI_POST), and assert the notice appears at most once across the
two runs and NEVER on the run that uses no deprecated spelling.

At least one assertion in this module observes the real subprocess output of
a hook run (stdout and stderr captured SEPARATELY), so a future hook that
emits the notice by some route other than a literal `--seat` — or that drops
the `2>/dev/null` swallow and lets a literal `--seat` reach the session —
fails loudly rather than passing a source-grep that lost the mechanism. The
source-level check at the end is a second, cheaper guard keyed to the ONE
bootstrap-call mechanism, never the only assertion.
"""

import os
import re
import subprocess
from pathlib import Path

import pytest

_HOOKS = [
    Path(__file__).resolve().parents[1]
    / "hooks" / "cc-session-start.next.sh",
    Path(__file__).resolve().parents[1]
    / "hooks" / "cc-session-start.sh",
]

#: The deprecated-alias notice family, one pattern per spelling. `--post`
#: itself must never appear in any pattern body (it is the CURRENT spelling).
#: Matching "is deprecated" as the shared family stretch would also catch the
#: three exact messages above without reinventing them.
_NOTICE = re.compile(
    r"note:\s+(--seat|AGI_SEAT|config:seats)\s+is deprecated"
)


def _make_project(tmp_path: Path) -> Path:
    """A minimal project: `.agi/config.json` (goal:g11 marker) plus a fresh
    `.agi/context/INJECTION.md` so the hook reaches the bootstrap block and
    REUSES the cache (the hook `exit 0`s before the block when no
    INJECTION.md exists; and PROJECT_ROOT resolves to the `.agi` graph dir, so
    the injection file must sit under it, not beside it).
    """
    root = tmp_path / "proj"
    (root / ".agi" / "context").mkdir(parents=True)
    (root / ".agi" / "config.json").write_text('{"name": "tmp-hook-proj"}')
    (root / ".agi" / "context" / "INJECTION.md").write_text(
        "# tmp project injection\n\nmap: none\n"
    )
    return root


def _run_hook(hook: Path, root: Path, env_extra: dict) -> subprocess.CompletedProcess:
    """Run the hook as a real subprocess from inside `root`, stdout and
    stderr captured separately. The hook resolves the project root from its
    cwd, so cwd IS the tmp project."""
    env = dict(os.environ)
    # Never inherit a seat spelling from the runner's own environment; every
    # run is fully specified by env_extra.
    env.pop("AGI_SEAT", None)
    env.pop("AGI_POST", None)
    env.update(env_extra)
    return subprocess.run(
        ["bash", str(hook)],
        cwd=str(root),
        env=env,
        capture_output=True,
        text=True,
        timeout=120,
    )


def _notice_count(proc: subprocess.CompletedProcess) -> int:
    return sum(
        _NOTICE.search(buff) is not None
        for buff in (proc.stdout, proc.stderr)
    )


@pytest.mark.parametrize(
    "hook", _HOOKS, ids=[p.name for p in _HOOKS]
)
def test_deprecated_alias_notice_not_emitted_unconditionally(hook, tmp_path):
    """The notice is not emitted unconditionally: a session using only the
    current spelling sees ZERO deprecated-alias notices, and — counting the
    deprecated-env-spelling run too — the family appears at most once across
    the two runs."""
    root = _make_project(tmp_path)

    run_a = _run_hook(hook, root, {"AGI_SEAT": "seatA"})   # deprecated env spelling in use
    run_b = _run_hook(hook, root, {"AGI_POST": "postB"})   # current spelling only

    assert run_a.returncode == 0, f"hook exited {run_a.returncode}"
    assert run_b.returncode == 0, f"hook exited {run_b.returncode}"

    a_notices = _notice_count(run_a)
    b_notices = _notice_count(run_b)

    # The core of the criterion: a run with no deprecated spelling never
    # emits the deprecated-alias notice.
    assert b_notices == 0, (
        "current-spelling (AGI_POST) run emitted a deprecated-alias notice "
        f"({b_notices}); stderr={run_b.stderr!r}"
    )
    # Across both runs the family appears at most once (the criterion's ceiling).
    assert a_notices + b_notices <= 1, (
        f"deprecated-alias notice seen {a_notices + b_notices} times across "
        f"both runs (a={a_notices}, b={b_notices}); "
        f"A stderr={run_a.stderr!r} B stderr={run_b.stderr!r}"
    )


def test_hook_source_bootstrap_call_uses_post_spelling():
    """Second, cheaper guard keyed to the mechanism, not a blanket absence:
    the actual `rotate.py bootstrap-block` invocation region in each hook
    names the CURRENT spelling (`--post`) and never a literal `--seat`.
    (Never the only check — the parametrized run-based test above is.)"""
    for hook in _HOOKS:
        src = hook.read_text(encoding="utf-8")
        lines = src.splitlines()
        # The bootstrap call is the ONE source line naming rotate.py WITH
        # bootstrap-block, plus its `--root` continuation line. Narrowing to
        # exactly these two keeps a comment mentioning rotate.py (or --seat)
        # from fooling the guard in either direction.
        idx = next(
            i for i, ln in enumerate(lines)
            if "rotate.py" in ln and "bootstrap-block" in ln
        )
        invocation = "\n".join(lines[idx:idx + 2])
        assert "--post" in invocation, (
            f"{hook.name}: bootstrap-block call does not use the current "
            f"--post spelling: {invocation!r}"
        )
        assert "--seat" not in invocation, (
            f"{hook.name}: bootstrap-block call still passes the deprecated "
            f"--seat spelling: {invocation!r}"
        )