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