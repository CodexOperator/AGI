"""hypothesis:l3-dispatch-env-leaks-into-tests — the dispatcher exports AGI_*
spawn variables (AGI_LOOP, AGI_MODEL, AGI_ROLE, AGI_TIER, AGI_SEASON,
AGI_PROFILE, ...) into a kid/parent's environment. Two defences make a
verification independent of its spawn env:

1. A session-scoped autouse fixture in extensions/agi/conftest.py deletes every
   AGI_* / AUTORESEARCH_* key before any test runs, so the test process sees a
   clean shell no matter what env it was spawned under.
2. The driver (extensions/agi/driver.sh) ignores a dispatched AGI_LOOP spawn
   label (never a bare loop label) when picking the iteration loop, so
   `driver.sh --smoke` no longer crashes inside a dispatched env.
"""

import os
import subprocess
from pathlib import Path

import pytest

ENGINE = Path(__file__).resolve().parents[1]  # extensions/agi
DRIVER = ENGINE / "driver.sh"

# Keep in sync with the documented list in conftest.py.
AGI_DISPATCH_VARS = (
    "AGI_LOOP", "AGI_MODEL", "AGI_ROLE", "AGI_TIER", "AGI_SEASON",
    "AGI_PROFILE", "AGI_PROJECT_ROOT", "AGI_LADDER_TIER",
    "AGI_TREE_PROJECT_ROOT", "AUTORESEARCH_TREE_PROJECT_ROOT",
)

# hypothesis:l4-the-harvest-reads-the-diff-per-deliverable-a-timeout-says-
# timed-out-and-the-done-tests-stay-hermetic item (1): the dispatch spawn set
# also pins `core.hooksPath` at <engine>/hooks/agent-git through the
# GIT_CONFIG_* channel, which is not AGI_*-prefixed and so used to survive
# into the test process. Any test shelling out to git then ran the commit
# guard -- the reason the two worktree done-commit tests in test_cli.py were
# only green by accident, and the reason test_rotate.py and
# test_sensei_audit_record_writeback.py delenv/setenv these by hand.
GIT_CONFIG_SPAWN_VARS = (
    "GIT_CONFIG_COUNT", "GIT_CONFIG_KEY_0", "GIT_CONFIG_VALUE_0",
)


def _living_agi_vars():
    """Keys in this process's env that conftest should have stripped."""
    return sorted(
        k for k in os.environ
        if k.startswith("AGI_") or k.startswith("AUTORESEARCH_")
    )


def test_conftest_stripped_all_agi_vars():
    """No dispatch var survives into the session — the spawn env is inert."""
    assert _living_agi_vars() == [], _living_agi_vars()


def test_conftest_documented_list_covers_the_spawn_set():
    """Every documented dispatch var is actually stripped by the fixture."""
    for var in AGI_DISPATCH_VARS:
        assert os.environ.get(var) is None, (
            f"conftest should have stripped {var!r}"
        )


def test_conftest_strips_the_git_config_spawn_channel():
    """Item (1): the `core.hooksPath` channel is AGI_*-free, so the glob
    above never caught it. It must be gone too, or a test's own `git` runs
    the commit guard and the suite's colour depends on who spawned it."""
    for var in GIT_CONFIG_SPAWN_VARS:
        assert os.environ.get(var) is None, (
            f"conftest should have stripped {var!r} -- a leftover one makes "
            f"every git call in the suite run the agent-git hook"
        )
    assert sorted(
        k for k in os.environ if k.startswith("GIT_CONFIG_")
    ) == [], "GIT_CONFIG_* cannot leak into the suite"


def test_inherited_hookspath_really_runs_a_hook_and_the_strip_removes_it(
        tmp_path, monkeypatch):
    """Item (1), with teeth on both halves.

    Half (a) MEASURES the mechanism rather than asserting it: pin the
    `core.hooksPath` channel at a hooks dir holding a WITNESS pre-commit and
    make a real commit in a scratch repo -- the witness fires, so an
    inherited GIT_CONFIG_VALUE_0 genuinely reaches a test's own `git`. Half
    (b) is the fix: the session fixture has already removed the key from
    THIS process's env, so no test here ever runs the guard by accident.
    """
    repo = tmp_path / "repo"
    repo.mkdir()
    hooks = tmp_path / "hooks"
    hooks.mkdir()
    witness = tmp_path / "witness.txt"
    hook = hooks / "pre-commit"
    hook.write_text(f"#!/bin/sh\necho fired >> {witness}\n")
    hook.chmod(0o755)
    monkeypatch.setenv("GIT_CONFIG_COUNT", "1")
    monkeypatch.setenv("GIT_CONFIG_KEY_0", "core.hooksPath")
    monkeypatch.setenv("GIT_CONFIG_VALUE_0", str(hooks))
    run = lambda *a: subprocess.run(  # noqa: E731
        ["git", "-C", str(repo), *a], capture_output=True, text=True)
    run("init", "-q")
    (repo / "f.txt").write_text("x\n")
    run("add", "-A")
    run("-c", "user.email=t@t", "-c", "user.name=t", "commit", "-qm", "m")
    assert witness.exists(), (
        "the pinned core.hooksPath did NOT reach the scratch repo's commit "
        "-- then the leak this item names was never real and the strip is "
        "belt-and-braces rather than a fix"
    )
    monkeypatch.delenv("GIT_CONFIG_COUNT", raising=False)
    monkeypatch.delenv("GIT_CONFIG_KEY_0", raising=False)
    monkeypatch.delenv("GIT_CONFIG_VALUE_0", raising=False)
    for var in GIT_CONFIG_SPAWN_VARS:
        assert os.environ.get(var) is None, (
            f"conftest left {var!r} set -- every git call in the suite would "
            f"run the agent-git hook"
        )


# --- driver path ------------------------------------------------------------


def _driver_pick_loop(env):
    """Run the REAL pick_loop from driver.sh against the given env.

    Extracts the function body straight from the checked-in script so the
    test can never drift from the code it claims to guard.
    """
    picked = "awk '/^pick_loop\\(\\)/,/^}/' %s" % (DRIVER,)
    sed = subprocess.run(picked, shell=True, cwd=ENGINE, capture_output=True,
                         text=True)
    assert sed.returncode == 0 and "pick_loop" in sed.stdout, (
        "driver.sh no longer defines pick_loop — the driver fix is gone"
    )
    body = sed.stdout
    harness = (
        "source /dev/stdin <<'BODY'\n"
        + body
        + "BODY\n"
        "loop=\"\"; pick_loop loop; printf '%s' \"$loop\"\n"
    )
    proc = subprocess.run(["bash", "-c", harness], env={**os.environ, **env},
                          capture_output=True, text=True)
    return proc.returncode, proc.stdout


def test_driver_ignores_dispatched_agi_loop():
    """A spawn label AGI_LOOP (hypothesis:x@s1) must NOT become the loop."""
    rc, out = _driver_pick_loop(
        {"CURRENT_LOOP": "", "AGI_LOOP": "hypothesis:l3-dispatch-env-leaks-into-tests@s1"})
    assert rc == 0, out
    assert out == "", f"expected empty loop, got {out!r}"


def test_driver_honours_a_real_loop_label():
    """A bare loop label in AGI_LOOP is still honoured (conductor fallback)."""
    rc, out = _driver_pick_loop({"CURRENT_LOOP": "", "AGI_LOOP": "L3"})
    assert rc == 0, out
    assert out == "L3", f"expected loop 'L3', got {out!r}"


def test_driver_current_loop_wins_over_spawn_label():
    """An explicit CURRENT_LOOP always wins over a dispatched AGI_LOOP."""
    rc, out = _driver_pick_loop(
        {"CURRENT_LOOP": "iter-L3.06", "AGI_LOOP": "hypothesis:x@s1"})
    assert rc == 0, out
    assert out == "iter-L3.06", f"expected CURRENT_LOOP, got {out!r}"