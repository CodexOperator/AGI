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
import subprocess
import sys
from pathlib import Path

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


# --- synthetic-root in-repo basetemp guard --------------------------------
# hypothesis:l4-basetemp-advice-excludes-synthetic-root-fixtures. The Prime's
# cross-worktree race advice runs a round's tests with `--basetemp` under its
# own .agi/sessions/ (e.g. .agi/sessions/pytest-basetemp). That is safe for
# tests whose tmp-path fixtures do NOT build a synthetic `.agi/` ROOT. A
# synthetic-root test builds groot = tmp_path / ".agi" and resolves it through
# `locations.*`; under an in-repo --basetemp, tmp_path lands INSIDE the real
# repo, so locations.find_project_root/shared_sessions_dir/git_common_root
# resolve the REAL graph instead of the synthetic root and the test silently
# runs against the wrong tree (measured 4 of 8 test_verification_seat_model.py
# failing; all 8 pass on the default out-of-repo basetemp).
#
# Near-miss this guard must NOT be: "refuse every in-repo basetemp". That
# would re-break the Prime's race fix, which is the whole reason the advice
# exists. So refusal is scoped by a MODULE-NAME ALLOWLIST (the sanctioned
# detection): only the modules that build a synthetic root are refused under
# an in-repo basetemp; every other module keeps the advised behaviour.
SYNTHETIC_ROOT_MODULES = {
    "test_verification_seat_model.py",
}
IN_REPO_BASETEMP_REASON = (
    "--basetemp points INSIDE the project repo (e.g. .agi/sessions/...), but "
    "this invocation's named module builds a synthetic .agi/ root; under an "
    "in-repo basetemp tmp_path lands inside the real repo and locations "
    "resolves the real graph, not the synthetic root (see "
    "hypothesis:l4-basetemp-advice-excludes-synthetic-root-fixtures). "
    "Use pytest's default (out-of-repo) basetemp for synthetic-root tests."
)


def _in_repo_basetemp(config) -> bool:
    """True when --basetemp resolves to a path inside the project root."""
    bt = getattr(config.option, "basetemp", None)
    if not bt:
        return False
    root = locations.find_project_root(Path(__file__).resolve())
    if root is None:
        return False
    try:
        bt_real = Path(bt).resolve()
    except OSError:
        return False
    return bt_real == root or root in bt_real.parents


def _refuse_in_repo_basetemp_on_synthetic_root(config) -> None:
    """Refuse an in-repo --basetemp ONLY for a named synthetic-root module."""
    if not _in_repo_basetemp(config):
        return
    paths = _named_paths(getattr(config, "args", None))
    named = {Path(p).name for p in paths if p.endswith(".py")}
    if named & SYNTHETIC_ROOT_MODULES:
        raise pytest.UsageError(IN_REPO_BASETEMP_REASON)


def pytest_cmdline_main(config):
    _refuse_in_repo_basetemp_on_synthetic_root(config)
    if os.environ.get("AGI_TIER") != GATE_TIER:
        # Invisible at every tier other than kid, and when the var is unset.
        return
    if _is_bare_directory_run(config):
        raise pytest.UsageError(REFUSAL_REASON)


@pytest.fixture(autouse=True)
def _no_real_tmux(monkeypatch):
    """hypothesis:l4-conftest-tmux-guard — project-wide tmux guard, widened
    from test_send.py's old file-local `_SafeSubprocess`/`_no_real_tmux`
    (hypothesis:l4b23-fixture-leak, CLOSED proved but scoped to send.py only).

    Every test must never reach the live tmux session
    (`rotate.DEFAULT_TMUX_SESSION`, "agi-rc"), where a recipient whose name
    matches a real window would have text typed into a live agent's terminal.
    The guard answers any `tmux` subprocess call with a safe rc-1
    CompletedProcess (so `_nudge_window`/`_existing_windows` short-circuit to
    "no such session", exactly as the old `_SafeSubprocess` did for tmux).

    **Selective, not blanket**: every NON-tmux call (in particular the real
    `git` invocations test_season.py/test_rotate.py's own fixtures depend on)
    is passed through untouched to the real `subprocess.run`. Requesting a
    raise on any non-tmux call (the old `_SafeSubprocess` behaviour) would
    break those tests — see the L4.5x brief.

    Patch target: the real stdlib `subprocess.run`.
    send.py/rotate.py/season.py `import subprocess`, and mail_alert.py
    `import send` (whose module object `import subprocess` too), so every
    module's tmux call ultimately resolves through this one attribute — one
    fixture covers the whole suite. A per-module-alias patch would defeat
    the "project-wide" point.

    Override-precedence for the three `_fake_tmux` tests in test_send.py:
    they monkeypatch `send_mod.subprocess.run` (= this same global
    `subprocess.run`) in the TEST BODY, after this autouse fixture's setup, so
    their fake wins for the duration of the test. (monkeypatch is
    function-scoped, so the fixture's and the test's instances are the same;
    both revert at teardown.)
    """
    real_run = subprocess.run

    def _guarded_run(cmd, *a, **k):
        if isinstance(cmd, list) and cmd[:1] == ["tmux"]:
            return subprocess.CompletedProcess(cmd, 1)
        return real_run(cmd, *a, **k)

    monkeypatch.setattr(subprocess, "run", _guarded_run)


# --- the suite lock belongs to the resource, not a caller -------------------
# `hypothesis:l4-the-suite-lock-belongs-to-pytest-not-its-caller`. Every path
# that starts the pytest suite goes THROUGH this conftest (commands.py run
# tests, verification.py --suite, season.py merge-up, a bare shell), so the
# lock lives here, resolved from Path(__file__) — never cwd — and every caller
# contends for the one file.
_BIN = Path(__file__).resolve().parent.parent / "bin"
if str(_BIN) not in sys.path:
    sys.path.insert(0, str(_BIN))
import locations  # noqa: E402
import verification  # noqa: E402

#: Reentrancy marker. The suite runs pytest INSIDE pytest (test_tier_gate.py's
#: nested runs) and verification.py --suite spawns pytest as a child with no
#: env=, so children inherit os.environ. A nested pytest must NO-OP here, or it
#: refuses itself against its own parent's live lock and deadlocks the round.
#: The name must NOT begin AGI_ or AUTORESEARCH_ (extensions/agi/conftest.py
#: strips those prefixes) — that is why it is VERIFY_*.
SUITE_LOCK_MARKER = "VERIFY_SUITE_LOCK_PID"


@pytest.fixture(scope="session", autouse=True)
def _suite_lock_guard():
    """Acquire the suite lock for the whole pytest session, once.

    A bare `python3 -m pytest extensions/agi/tests/` creates
    `<graph>/sessions/verify-suite.lock` with its own pid and removes it on
    exit. A second independent pytest started while the first runs finds the
    lock held by a LIVE pid and REFUSES, naming that holder. A nested pytest
    (pytest inside pytest) inherits SUITE_LOCK_MARKER from its acquiring
    parent and NO-OPS — the parent still holds the window, so the child must
    not re-acquire.
    """
    if os.environ.get(SUITE_LOCK_MARKER):
        # Inherited: our parent process holds the suite window for this run.
        yield
        return

    root = locations.find_project_root(Path(__file__).resolve())
    if root is None:
        # Not inside an agi project — no graph sessions dir to guard. No-op.
        yield
        return
    lock_path, holder = verification.acquire_suite_lock(root)
    if lock_path is None:
        if holder is None:
            raise RuntimeError(
                "suite window refused — the suite lock could not be written "
                f"under {root / 'sessions'}")
        raise RuntimeError(
            f"suite window refused — pid {holder} is a LIVE runner holding "
            f"{root / 'sessions' / verification.SUITE_LOCK}; one suite at a "
            "time — wait for it or ask whoever owns it")
    os.environ[SUITE_LOCK_MARKER] = str(os.getpid())
    try:
        yield
    finally:
        os.environ.pop(SUITE_LOCK_MARKER, None)
        if lock_path.exists():
            try:
                lock_path.unlink()
            except OSError:
                pass