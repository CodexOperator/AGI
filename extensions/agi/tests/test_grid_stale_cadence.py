"""SM item (5), 11-12 (belam [read] 00:36Z): the grid-stale alarm must not fire in a QUIET hour.

grid_stale calls a trunk node stale when the grid has not versioned it for more than 2 x grid_sync's
every_mins (grid_stale.py, S1). grid_sync versions MAIN's DISK, and MAIN reaches the trunk's bytes only
when graph_metrics_land fast-forwards it (or at a land, which a quiet hour has none of). Measured on the
host 11-11/11-12: with the land at :28 alone, a card commit at :29 sits on the trunk until the NEXT :28,
is versioned by the :30 sync, and the stale read at :30 (the same minute, before that sync's version is
written) sees it ~61 min old: a FALSE alarm at 23:30Z and 00:30Z.

The row: from the LIVE cron:crons cells (read through crons.load_crons_node, never a literal), for a
trunk change at EVERY minute of the hour, simulate land -> sync -> the stale reads, and assert the
oldest age any stale read sees stays at or under the stale bound. A stale read in the SAME minute as
a sync runs before that sync's version (the measured order). RED on the trunk's `28 * * * *` (61 > 60);
GREEN when the land runs a few minutes before EACH sync. The mutant row pins that the simulation bites.
Honest limits: whole minutes; a land's ff and a sync's version are treated as instant; a land with a
non-landable commit in between (board_job C6) is out of scope (a quiet hour holds only the job's own
and the Prime's node commits); the hours field must be `*` for the three jobs (asserted).
"""
from __future__ import annotations

import importlib.util
import os
from pathlib import Path

ROOT = Path(__file__).resolve().parents[3]
BIN = ROOT / "extensions" / "agi" / "bin"


def _crons():
    spec = importlib.util.spec_from_file_location("crons_for_stale_cadence", BIN / "crons.py")
    mod = importlib.util.module_from_spec(spec)
    spec.loader.exec_module(mod)
    return mod


def _minutes(job: dict) -> list[int]:
    """The minutes of the hour a job fires at: `*/n` from every_mins, or the minute field of a 5-field schedule."""
    if job["every_mins"] is not None:
        n = job["every_mins"]
        assert 60 % n == 0, f"every_mins {n} does not divide the hour"
        return list(range(0, 60, n))
    f = job["schedule"].split()
    assert f[1:] == ["*", "*", "*", "*"], f"only an hourly-repeating schedule is simulated, got {job['schedule']!r}"
    out = []
    for part in f[0].split(","):
        if part.startswith("*/"):
            out += list(range(0, 60, int(part[2:])))
        else:
            out.append(int(part))
    return sorted(set(out))


def _next(times: list[int], t: int, strict: bool) -> int:
    """The first absolute minute >= t (or > t when strict) at which a job with these hour-minutes fires."""
    for k in range(t + (1 if strict else 0), t + 121):
        if k % 60 in times:
            return k
    raise AssertionError("no firing within two hours")


def worst_age(land: list[int], sync: list[int], stale: list[int]) -> tuple[int, int]:
    """(oldest age a stale read sees for an unversioned trunk change, the change minute that gives it)."""
    worst = (0, -1)
    for c in range(60):
        l = _next(land, c, strict=True)        # a land at the change's own minute ran before it
        s = _next(sync, l, strict=False)       # a sync in the land's minute versions what the land brought
        r = _next(stale, c, strict=True)
        while r <= s:                           # every stale read up to and INCLUDING the sync's minute sees it unversioned
            worst = max(worst, (r - c, c))
            r = _next(stale, r, strict=True)
    return worst


def _live():
    jobs = _crons().load_crons_node(ROOT / ".agi")["jobs"]
    for name in ("graph_metrics_land", "grid_sync", "grid_stale"):
        assert name in jobs and jobs[name]["enabled"], f"cadences.{name} is not declared enabled on the live node"
    bound = 2 * jobs["grid_sync"]["every_mins"]
    return _minutes(jobs["graph_metrics_land"]), _minutes(jobs["grid_sync"]), _minutes(jobs["grid_stale"]), bound


def test_s1_a_quiet_hour_never_reads_stale():
    land, sync, stale, bound = _live()
    age, c = worst_age(land, sync, stale)
    assert age <= bound, (f"a trunk change at :{c:02d} is seen {age} min old by a stale read (bound {bound}): "
                          f"land {land}, sync {sync}, stale {stale}")


def test_s1m_mutant_the_trunk_schedule_reads_stale():
    """The pre-fix cell (`28 * * * *`) under the live sync and stale cells: the simulation must read it
    over the bound, the false alarm belam measured (a change at :29 seen 61 min old at the next :30; :28 after the land, 62)."""
    _, sync, stale, bound = _live()
    age, c = worst_age([28], sync, stale)
    assert age > bound, (age, c, bound)   # the worst change minute is :28 just after the land ran (62 min); belam's :29 case reads 61


def test_s2_the_land_runs_before_each_sync():
    """The fix is the land a few minutes BEFORE each sync (belam + SM (a)): it shortens the real lag. Where the stale job runs is NOT
    pinned here (SM [ask] 01:11:04Z 11-12, DG2 (A)): belam's 01:00Z third shape (a stale read during a sync's write, a stale anchor) may
    want it AFTER the sync, a separate touch with its own falsifier; s1 already simulates any stale minutes the live cell holds."""
    land, sync, stale, _ = _live()
    for s in sync:
        assert any(0 < (s - l) % 60 <= 5 for l in land), f"no land in the 5 min before the sync at :{s:02d}: land {land}"
