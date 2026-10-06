"""goal:g15 (hypothesis:l4-the-suite-never-writes-the-live-sessions-or-comms-
root-heal-and-send-take-the-root-they-are-given, SM.77) -- the suite never
writes the LIVE sessions or comms tree.

The `_pin_sessions_and_comms_roots_to_tmp` autouse fixture makes every in-test
sessions/comms write land under the test's `tmp_path` by construction. THIS
guard is the independent witness: it snapshots the REAL live trees (resolved
through the ORIGINAL, unpatched resolvers at import time, before any fixture
body runs), drives the primary heal/send/rotate/cli producer code paths against
a throwaway tmp root, re-snapshots, and asserts the live tree gained no
fixture-named artefact -- no rotation record for a fixture seat, no
`[crash-recovery]` dm in a live inbox naming a fixture seat, no new live inbox
or comms file with a fixture token.

The live tree is shared with live agents/crons that write real seats (belam,
sensei-*, sanctuary-*, master-*) every few seconds, so the assertion is scoped
to the FIXTURE seat set -- the names the four producer modules actually write
in their tests (measured: the pre-fix suite leaked seat-a/dead-a/wt/kid-a/
director-seat/hand-seat/noct-seat/diff-seat/sensei-peer into the live tree).
A live-write leak is the only way a fixture-tokened file can appear or change
in the live tree during the run.
"""
from __future__ import annotations

import importlib.util
import json
import sys
import time
from pathlib import Path

import pytest

BIN = Path(__file__).resolve().parents[1] / "bin"
if str(BIN) not in sys.path:
    sys.path.insert(0, str(BIN))

import locations  # noqa: E402 -- shared module object the fixtures patch


def _load(name):
    spec = importlib.util.spec_from_file_location(name, BIN / f"{name}.py")
    mod = importlib.util.module_from_spec(spec)
    sys.modules.setdefault(name, spec.loader.exec_module(mod) or mod)
    return mod


heal = _load("heal")
cli = _load("cli")
rot = _load("rotate")
send = _load("send")

#: The REAL live sessions + comms roots, resolved at import time through the
#: ORIGINAL resolvers -- the autouse pin fixtures have not run yet, so this is
#: the tree the leak used to hit (git_common_root of the worktree -> MAIN
#: checkout's `.agi`).
_GRAPH = locations.find_project_root(Path(__file__))
_LIVE_SESSIONS = locations.shared_sessions_dir(_GRAPH)
_LIVE_COMMS = send.comms_root(_GRAPH)

#: The fixture seat names the four producer modules write when they leak.
_FIXTURE_TOKENS = ("seat-a", "seat-b", "seat-c", "dead-a", "wt.",
                   "kid-a", "kid-b", "kid-solo", "director-seat",
                   "hand-seat", "noct-seat", "diff-seat", "sensei-peer")


def _snapshot() -> dict:
    """{str(path): int mtime} for every file under the LIVE rotations, inbox,
    seats and comms trees."""
    out = {}
    for base in (_LIVE_SESSIONS / "rotations", _LIVE_SESSIONS / "inbox",
                 _LIVE_SESSIONS / "seats", _LIVE_COMMS):
        if not Path(base).is_dir():
            continue
        for p in Path(base).rglob("*"):
            if p.is_file():
                out[str(p)] = p.stat().st_mtime
    return out


def _leak_markers(before: dict, after: dict) -> list[str]:
    """Names of any live file that is fixture-tokened AND appeared or changed
    during the run -- the only way this suite could have written it."""
    found = []
    for path, aft in after.items():
        is_fixture = any(tok in path for tok in _FIXTURE_TOKENS)
        if not is_fixture:
            continue
        if path not in before or abs(before[path] - aft) > 0.6:
            found.append(path)
    return found


@pytest.fixture
def graph(tmp_path: Path) -> Path:
    """A throwaway fixture project graph (config.json + sessions dir)."""
    g = tmp_path / "project" / ".agi"
    g.mkdir(parents=True, exist_ok=True)
    (g / "config.json").write_text(json.dumps({"metric_primary": "x"}))
    (g / "sessions").mkdir(parents=True, exist_ok=True)
    return g.parent


def test_live_sessions_and_comms_are_byte_identical(graph: Path):
    """Drive the primary heal/send/rotate/cli write paths against a tmp root
    and prove none of them (nor their resolver re-resolution) touches the live
    tree with a fixture artefact."""
    before = _snapshot()

    # heal crash-recovery dm path (the 5-dms-to-master-sensei leak).
    rec = {"name": "seat-a", "rotated_by": "master-sensei"}
    heal._dm_crash_recovery(graph, rec, 7777, "guard-test",
                            "seat-a-succ", "w1", 3)

    # send inbox path (the seat-a.md leak).
    send.send(graph, "seat-a",
              "[crash-recovery] wt pid 0 dead (guard-test); respawned dead-a",
              "heal")

    # rotate run_after_join path (the rotations/*.seating.json leak).
    rot.run_after_join_for_seat(graph, "wt",
                                send_dm=lambda *a, **k: None,
                                type_input=lambda *a, **k: None,
                                _force_due=True)

    # cli harvest-completion dm path (the dispatcher inbox leak).
    it = cli.locations.iteration_dir(graph, "L4.777")
    it.mkdir(parents=True, exist_ok=True)
    (it / "manifest.json").write_text(json.dumps({"agents": [{
        "id": "kid-a", "status": "running", "dispatched_by": "director",
    }]}))
    cli._alarm_dispatcher_on_done(graph, "L4.777", "kid-a",
                                  "experiment:guard-x", "proved")

    after = _snapshot()
    leaked = _leak_markers(before, after)
    assert leaked == [], (
        "the suite wrote a fixture artefact into the LIVE tree: "
        f"{leaked!r}")


def test_pinned_resolvers_never_resolve_to_live(tmp_path):
    """The pin fixture binds the four resolver leaves so no test-callable root
    resolves sessions/comms into the live tree (the git-re-resolution escape
    that caused the leak)."""
    live_sessions = str(_LIVE_SESSIONS.resolve())
    live_comms = str(_LIVE_COMMS.resolve())
    for root in (tmp_path, tmp_path / "nested" / "graph"):
        assert live_sessions not in str(
            locations.shared_sessions_dir(root))
        assert live_comms not in str(send.comms_root(root))
    assert live_sessions not in str(locations.sessions_dir(tmp_path))