"""Tests for bin/dispatch.py's pi argument construction.

Narrow on purpose: `_build_pi_args` is the seam where a config key becomes a
real flag on a real subprocess, and until 2026-08-31 it read `agent_dispatch`
and then used none of it — every kid silently ran whatever `~/.pi/agent/
settings.json` said, while the config key that claims to pick the model picked
nothing. A defect that quiet deserves a test that is loud.
"""
from __future__ import annotations

import importlib.util
import re
import subprocess
import sys
from pathlib import Path

import pytest

BIN = Path(__file__).resolve().parents[1] / "bin"
sys.path.insert(0, str(BIN))


def _load_dispatch():
    spec = importlib.util.spec_from_file_location("agi_dispatch", BIN / "dispatch.py")
    module = importlib.util.module_from_spec(spec)
    spec.loader.exec_module(module)
    return module


dispatch = _load_dispatch()


def test_reaper_restart_inherits_the_iteration_id(tmp_path):
    """hypothesis:l3-killed-agent-restarts-unattributed, red first.

    A killed agent that is legitimately restarted (`_reap_one`) must acquire
    its `-rN` lease with the round's iteration id, so `spawn_budget status`
    attributes the survivor to the round it belongs to instead of iter=None.
    The 2026-09-08 kill measured three live survivors carrying iter=None that
    held a round open invisibly; this pins the seam that produced them.
    """
    import json as _json
    root = tmp_path
    (root / "sessions").mkdir()
    iter_dir = root / "sessions" / "iter-342"
    (iter_dir / "a00-abc123-r1").mkdir(parents=True)

    class FakeAdapter:
        def is_alive(self, pid):
            return False

        def restart(self, **kw):
            self.called = kw
            return 12345

    ada = FakeAdapter()
    rec = {
        "id": "a00-abc123",
        "tier": "parent",
        "node_id": "",
        "status": "running",
        "pid": 999,
        "restart_count": 0,
        "iter": 342,
    }
    outcome = dispatch._reap_one(
        root, iter_dir, ada, rec, "a00-abc123", 999,
        cap=10, cfg={"reaper": {"max_restarts": 1}})
    assert outcome["record"]["status"] == "running"
    import spawn_budget as _sb
    leases = [_json.loads(p.read_text())
              for p in _sb.budget_dir(root).glob("*.lease")]
    assert leases, "a restart should have left a lease"
    assert any(r.get("agent_id", "").endswith("-r1")
               and r.get("iter") == 342 for r in leases), (
        f"restart lease must carry the round's iteration, got {leases}")


def build(cfg: dict, tmp_path: Path) -> list[str]:
    return dispatch._build_pi_args(cfg, str(tmp_path / "ctx.md"), "agent-0", 1, tmp_path)


def flag_value(args: list[str], flag: str) -> str | None:
    return args[args.index(flag) + 1] if flag in args else None


def test_model_and_provider_reach_the_command_line(tmp_path):
    args = build({"agent_dispatch": {"provider": "openrouter",
                                     "model": "z-ai/glm-5.3-flash"}}, tmp_path)
    assert flag_value(args, "--provider") == "openrouter"
    assert flag_value(args, "--model") == "z-ai/glm-5.3-flash"


def test_thinking_is_passed_when_set(tmp_path):
    """The reasoning-effort dial goal:g4.2 asks for — a model name alone does
    not say how hard to think."""
    args = build({"agent_dispatch": {"model": "qwen/qwen3.8-27b",
                                     "thinking": "medium"}}, tmp_path)
    assert flag_value(args, "--thinking") == "medium"


@pytest.mark.parametrize("cfg", [
    {},
    {"agent_dispatch": {}},
    {"agent_dispatch": {"model": "", "provider": "   "}},
    {"agent_dispatch": {"model": None}},
])
def test_absent_or_empty_keys_pass_no_flag(cfg, tmp_path):
    """Omitting the keys must keep the pre-2026-08-31 behaviour exactly: pi's
    own settings win. A default invented here would silently retarget every
    project that never asked for one."""
    args = build(cfg, tmp_path)
    assert "--model" not in args
    assert "--provider" not in args
    assert "--thinking" not in args


def test_flags_precede_the_prompt_arguments(tmp_path):
    """pi parses options before positional messages; a flag emitted after the
    trailing user message would be read as part of it."""
    args = build({"agent_dispatch": {"model": "qwen/qwen3.8-27b"}}, tmp_path)
    assert args.index("--model") < args.index("--append-system-prompt")
    # Headless mode: without -p the trailing prompt opens the interactive
    # TUI, which hangs forever off a TTY (empty output.log, never exits).
    assert "-p" in args and args.index("-p") < args.index("--append-system-prompt")
    assert args[-1].startswith("Begin iteration")


def test_binary_is_still_first(tmp_path):
    args = build({"agent_dispatch": {"model": "qwen/qwen3.8-27b"}}, tmp_path)
    # hypothesis:l4-every-pi-kid-keeps-its-full-tool-call-trajectory-at-
    # spawn-never-pruned-never-rebuilt — the produced command now launches the
    # trajectory wrapper, which in turn runs the real pi (the `--wrapper`
    # segment's first value) under `--mode json`. The guard survives: the
    # arcane pi binary is still IN the command, argv[0] is just its runner.
    assert args[2] == "--wrapper"
    assert args[3].endswith("pi"), f"real pi binary must be the wrapper target: {args}"
    assert args[4].endswith("trajectory.jsonl")
    assert args[5] == "--"


# --- the scaffold prompt ---------------------------------------------------


def scaffold(parent: str) -> dict:
    return {"path": "/tmp/n.md", "node_type": "idea", "node_id": "idea:x", "parent": parent}


def test_parent_flag_is_emitted_when_there_is_a_parent(tmp_path):
    args = dispatch._build_pi_args({}, "ctx", "a00", 1, tmp_path, scaffold("idea:root"))
    prompt = "\n".join(args)
    assert "--parent idea:root" in prompt
    assert "Parent: idea:root" in prompt


@pytest.mark.parametrize("parent", ["", "   ", None])
def test_parentless_node_emits_no_bare_parent_flag(parent, tmp_path):
    """A fresh `idea` is parentless and the schema allows it. Interpolating an
    empty parent produced a command ending in a bare `--parent`, which argparse
    rejects — reported by a kid on the 2026-08-31 live run, which then guessed
    its way around it."""
    args = dispatch._build_pi_args({}, "ctx", "a00", 1, tmp_path, scaffold(parent))
    prompt = "\n".join(args)
    assert "--parent" not in prompt
    assert "parentless" in prompt
    assert "--node-id idea:x" in prompt


# --- the zoom invocation ---------------------------------------------------


def test_zoom_command_always_states_the_runtime(tmp_path):
    """goal:s8. zoom.py's own default answers 'cc' for any project carrying a
    cc_dispatch block, and a project may carry both — so the pi dispatcher has
    to say which runtime it is rather than let a config key guess."""
    cmd = dispatch.zoom_command(tmp_path, 3, "a00", "big", None)
    assert cmd[cmd.index("--runtime") + 1] == "pi"


def test_zoom_command_passes_target_only_for_small(tmp_path):
    small = dispatch.zoom_command(tmp_path, 3, "a00", "small", "idea:x")
    assert small[small.index("--target") + 1] == "idea:x"
    big = dispatch.zoom_command(tmp_path, 3, "a00", "big", "idea:x")
    assert "--target" not in big


def test_zoom_command_small_without_target_omits_the_flag(tmp_path):
    """zoom.py refuses `small` with no target by design (it would otherwise
    serve the whole graph). Passing a bare `--target` here would turn that
    loud refusal into an argparse error instead."""
    cmd = dispatch.zoom_command(tmp_path, 3, "a00", "small", None)
    assert "--target" not in cmd


def test_zoom_command_threads_the_tier_but_stays_byte_identical_for_kid(tmp_path):
    """hypothesis:l4-a-parents-zoom-is-its-target-goal-... — dispatch passes
    the --tier it received into zoom, but only when it is a tier zoom has a
    distinct shape for. A kid spawn (the default) does NOT grow a --tier
    flag, so every existing kid render stays byte-identical to today."""
    kid = dispatch.zoom_command(tmp_path, 3, "a00", "small", "idea:x", tier="kid")
    assert "--tier" not in kid
    base = dispatch.zoom_command(tmp_path, 3, "a00", "small", "idea:x")
    assert kid == base
    par = dispatch.zoom_command(tmp_path, 3, "a00", "small", "idea:x", tier="parent")
    assert par[par.index("--tier") + 1] == "parent"
    # a foreign tier value must never break the zoom invocation
    odd = dispatch.zoom_command(tmp_path, 3, "a00", "small", "idea:x", tier="untrusted")
    assert "--tier" not in odd


# --- aiming a slot: `--target` vs attractiveness scoring -------------------
#
# `_pick_targets` short-circuits at `n <= 1` to ("big", None, "explore_new"),
# so before `_explicit_targets` existed a single-slot pi run could not be
# pointed at anything: it always scaffolded a parentless `idea` and explored
# wherever scoring led. These lock the aim in place.


def test_aimed_slot_carries_the_target():
    got = dispatch._explicit_targets("goal:g4.3", None, "extend_existing", 1)
    assert got == [("small", "goal:g4.3", "extend_existing")]


def test_aim_defaults_to_small_because_big_zoom_discards_a_target():
    """`zoom_command` omits --target for big zoom, so defaulting the level to
    `big` here would silently throw the aim away."""
    level, target, _strategy = dispatch._explicit_targets("goal:g4.3", None, "s", 1)[0]
    assert level == "small"
    assert "--target" in dispatch.zoom_command(Path("/tmp"), 1, "a00", level, target)


def test_every_slot_is_aimed_at_the_same_node():
    got = dispatch._explicit_targets("idea:x", "small", "branch_fork", 3)
    assert len(got) == 3
    assert {t for _l, t, _s in got} == {"idea:x"}


def test_explicit_level_is_honoured():
    assert dispatch._explicit_targets("idea:x", "big", "s", 1)[0][0] == "big"
    assert dispatch._explicit_targets("idea:x", "auto", "s", 1)[0][0] == "auto"


def test_aiming_does_not_scaffold_a_parentless_idea():
    """The regression this closes: an aimed slot must produce a node type that
    follows the target, not the `idea` an untargeted big-zoom slot gets."""
    level, target, _s = dispatch._explicit_targets("hypothesis:x", None, "s", 1)[0]
    assert dispatch._node_type_for(level, target, None) == "experiment"
    assert dispatch._node_type_for("big", None, None) == "idea"


def test_leaf_recency_boost_fires():
    """idea:frontier-invitation / l3-frontier-successor-derivable.

    The 1.2x leaf bump used to be `desc * 1.2`, and `_descendant_count`
    returns 0 for a leaf, so the boost was dead on arrival: `0 * 1.2 == 0.0`
    and every chain tip scored 0.0 and sorted last. The fix floors the
    descendant term at 1; these assert the boost now means something.
    """
    boosted = dispatch._attractiveness(0, 1.2, 0.0, "idea")
    plain = dispatch._attractiveness(0, 1.0, 0.0, "idea")
    assert boosted > 0.0, "a leaf must no longer be condemned to score 0"
    assert boosted > plain, "the 1.2x leaf bump must actually change the score"
    # And the floor is identity for every non-leaf (desc >= 1 already).
    assert dispatch._attractiveness(3, 1.0, 0.0, "idea") == 3.0
    assert dispatch._attractiveness(3, 1.2, 0.0, "idea") == pytest.approx(3.6)


def test_leaf_boost_is_small_relative_to_an_extended_chain():
    """The floor must not let a lone leaf dwarf a real chain: one descendant
    (desc=1, no leaf bump) must still outrank an empty leaf (desc floored to
    1 with the bump) for the same type and diversity."""
    chain = dispatch._attractiveness(2, 1.0, 0.0, "idea")
    leaf = dispatch._attractiveness(0, 1.2, 0.0, "idea")
    assert chain > leaf


def test_attractiveness_type_weighting_preserved():
    assert dispatch._attractiveness(1, 1.0, 0.0, "hypothesis") == pytest.approx(1.4)
    assert dispatch._attractiveness(1, 1.0, 0.0, "experiment") == pytest.approx(1.2)
    assert dispatch._attractiveness(1, 1.0, 0.0, "verdict") == pytest.approx(1.1)
    assert dispatch._attractiveness(1, 1.0, 0.0, "idea") == pytest.approx(1.0)


# ---------------------------------------------------------------------------
# goal:s28 — a parent must not erase itself from the manifest by spawning a kid.
# goal:g4.8 — and that merge has to survive concurrency, which it did not.
#
# `b8cb2ec05` shipped the merge with no test behind it. These are s28's own
# falsifier, executed: spawn a parent, spawn kids into the SAME iteration, and
# assert every agent survives with the parent's `tier: parent` intact.
# ---------------------------------------------------------------------------

import json          # noqa: E402
import os            # noqa: E402
from multiprocessing import Process   # noqa: E402


def _rec(agent_id: str, tier: str) -> dict:
    return {"id": agent_id, "tier": tier, "status": "running"}


def test_merge_preserves_the_parent_when_a_kid_dispatches_into_the_same_iter(tmp_path):
    """s28's falsifier, first two clauses. A parent's entry must survive the
    second dispatch into its own iteration directory."""
    d = _load_dispatch()
    base = {"iter": 101, "started_at": 1, "agents": []}

    d._merge_manifest(tmp_path, base, [_rec("parent-a", "parent")])
    d._merge_manifest(tmp_path, base, [_rec("kid-1", "kid")])
    m = d._merge_manifest(tmp_path, base, [_rec("kid-2", "kid")])

    by_id = {a["id"]: a for a in m["agents"]}
    assert set(by_id) == {"parent-a", "kid-1", "kid-2"}, "an agent was clobbered"
    assert by_id["parent-a"]["tier"] == "parent", "the parent's tier was lost"


def test_started_at_is_carried_forward_not_reset_by_a_later_dispatch(tmp_path):
    """A kid dispatching later must not restart the iteration's clock --
    `heal.py` times agents out against it."""
    d = _load_dispatch()
    d._merge_manifest(tmp_path, {"iter": 1, "started_at": 111, "agents": []},
                      [_rec("parent-a", "parent")])
    m = d._merge_manifest(tmp_path, {"iter": 1, "started_at": 999, "agents": []},
                          [_rec("kid-1", "kid")])
    assert m["started_at"] == 111


def test_redispatching_one_agent_updates_it_rather_than_duplicating(tmp_path):
    """Healing re-dispatches the same id; the manifest must not grow a twin."""
    d = _load_dispatch()
    base = {"iter": 1, "started_at": 1, "agents": []}
    d._merge_manifest(tmp_path, base, [_rec("kid-1", "kid")])
    m = d._merge_manifest(tmp_path, base, [{"id": "kid-1", "tier": "kid",
                                            "status": "restarted"}])
    assert len(m["agents"]) == 1
    assert m["agents"][0]["status"] == "restarted"


def test_a_corrupt_manifest_degrades_with_a_warning_and_still_records(tmp_path, capsys):
    d = _load_dispatch()
    (tmp_path / "manifest.json").write_text("{not json")
    m = d._merge_manifest(tmp_path, {"iter": 1, "started_at": 1, "agents": []},
                          [_rec("kid-1", "kid")])
    assert [a["id"] for a in m["agents"]] == ["kid-1"]
    assert "corrupt manifest" in capsys.readouterr().err


def _concurrent_writer(iter_dir: str, agent_id: str) -> None:
    d = _load_dispatch()
    d._merge_manifest(Path(iter_dir), {"iter": 1, "started_at": 1, "agents": []},
                      [_rec(agent_id, "kid")])


def test_concurrent_dispatches_lose_no_agent(tmp_path):
    """goal:g4.8's falsifier, and the reason this fix exists.

    Measured against the pre-fix code -- a stale read plus a shared
    `.manifest.json.tmp` -- 8 concurrent dispatches lost entries in **6 of 6
    runs**, typically 6-7 of the 8. A lost entry is a spawned agent nothing
    tracks: `heal.py` cannot time it out, `post_wire` cannot wire its node.
    That is `goal:g7` failing at the moment of spawn, and it is what N parents
    at M kids each would have multiplied.
    """
    d = _load_dispatch()
    d._merge_manifest(tmp_path, {"iter": 1, "started_at": 1, "agents": []},
                      [_rec("parent-a", "parent")])

    procs = [Process(target=_concurrent_writer, args=(str(tmp_path), f"kid{i}"))
             for i in range(8)]
    for p in procs:
        p.start()
    for p in procs:
        p.join(timeout=60)

    got = {a["id"] for a in json.loads((tmp_path / "manifest.json").read_text())["agents"]}
    want = {"parent-a"} | {f"kid{i}" for i in range(8)}
    assert got == want, f"lost {sorted(want - got)} under concurrency"


def test_no_shared_temp_file_name_is_left_behind(tmp_path):
    """The old fixed `.manifest.json.tmp` was renamed out from under a
    concurrent writer, which then died with FileNotFoundError *after* Popen --
    a spawned-but-untracked agent. Unique names, and none left as litter."""
    d = _load_dispatch()
    d._merge_manifest(tmp_path, {"iter": 1, "started_at": 1, "agents": []},
                      [_rec("kid-1", "kid")])
    assert not (tmp_path / ".manifest.json.tmp").exists()
    leftovers = [p.name for p in tmp_path.iterdir() if p.name.endswith(".tmp")]
    assert leftovers == [], f"temp files left behind: {leftovers}"


# ---------------------------------------------------------------------------
# goal:g4.8 item 3 -- the manifest records slots the budget refused.
#
# An unadmitted slot has no pid and no process. It must be visible (a slot
# that silently did not spawn is indistinguishable from one that spawned and
# died -- the same invisibility the manifest race produced) and it must NOT
# appear in `agents`, because everything that polls `agents` for liveness
# would then go looking for a corpse that was never born.
# ---------------------------------------------------------------------------


def test_unadmitted_slots_are_recorded_apart_from_agents(tmp_path):
    d = _load_dispatch()
    base = {"iter": 107, "started_at": 1, "agents": []}
    refused = {"id": "a03-beef", "tier": "kid", "status": "unadmitted",
               "reason": "spawn budget full (5/5)"}

    m = d._merge_manifest(tmp_path, base, [_rec("a00-live", "kid")],
                          unadmitted=[refused])

    assert [a["id"] for a in m["agents"]] == ["a00-live"]
    assert [a["id"] for a in m["unadmitted"]] == ["a03-beef"]
    assert all(a.get("status") != "unadmitted" for a in m["agents"]), (
        "a slot that never spawned must not be polled for liveness")


def test_unadmitted_entries_merge_by_id_across_dispatches(tmp_path):
    """Same merge discipline as `agents` -- a re-dispatch updates, never twins."""
    d = _load_dispatch()
    base = {"iter": 107, "started_at": 1, "agents": []}
    refused = {"id": "a03-beef", "status": "unadmitted", "reason": "full (5/5)"}

    d._merge_manifest(tmp_path, base, [], unadmitted=[refused])
    d._merge_manifest(tmp_path, base, [], unadmitted=[{"id": "a04-cafe",
                                                       "status": "unadmitted"}])
    m = d._merge_manifest(tmp_path, base, [],
                          unadmitted=[dict(refused, reason="full (3/3)")])

    by_id = {a["id"]: a for a in m["unadmitted"]}
    assert set(by_id) == {"a03-beef", "a04-cafe"}
    assert by_id["a03-beef"]["reason"] == "full (3/3)"


def test_an_admitted_slot_leaves_the_unadmitted_list_empty(tmp_path):
    """The common case writes the key rather than omitting it, so a reader
    never has to distinguish 'nothing refused' from 'this dispatch predates
    the bound'."""
    d = _load_dispatch()
    m = d._merge_manifest(tmp_path, {"iter": 107, "started_at": 1, "agents": []},
                          [_rec("a00-live", "kid")])
    assert m["unadmitted"] == []


# ---------------------------------------------------------------------------
# goal:g4.7 -- restart is wired, and the ORDER of the two checks is the design.
#
# `restart()` was defined and never called ("reserved for a future iteration"),
# which is why its verdict sat at inconclusive_lean_proved:55. Wiring it needed
# one thing decided first: a dead pid is not the same fact as lost work.
# ---------------------------------------------------------------------------


class _FakeAdapter:
    def __init__(self, pid=None):
        self.pid = pid
        self.calls = []

    def is_alive(self, pid):
        return False

    def restart(self, **kw):
        self.calls.append(kw)
        return self.pid


def test_reaper_leaves_an_unknown_status_untouched(tmp_path, monkeypatch):
    """hyp:l4-one-definition-of-terminal, falsifier (c) -- the reaper's SECOND
    guard, asserted directly.

    `_reaper_phase` follows `if status in TERMINAL: continue` with
    `if status != "running": continue`. A status nobody has thought of yet --
    outside the terminal set AND outside "running" -- must therefore be
    skipped: not restarted, not mangled, left exactly as written. This is the
    tolerance that kept the reaper working while the set was wrong
    (`done-unreported` was exactly such a forgotten status), and it is why the
    second guard is KEPT even now that the set is right. A later
    "simplification" that deletes the guard makes an unknown status fall
    through to the restart path, so this test fails on it.
    """
    import json

    d = _load_dispatch()
    graph = _reap_project(tmp_path)
    iter_dir = graph / "sessions" / "iter-unk"
    (iter_dir / "a00-unk").mkdir(parents=True)
    (iter_dir / "manifest.json").write_text(json.dumps(
        {"agents": [{"id": "a00-unk", "status": "zombie"}]}))
    (iter_dir / "a00-unk" / "agent.json").write_text(json.dumps(
        {"id": "a00-unk", "status": "zombie", "pid": 999}))
    adapter = _FakeAdapter(pid=123)
    d._reaper_phase(graph, iter_dir, adapter, max_wait_s=1, cap=5, cfg={})
    rec = json.loads((iter_dir / "a00-unk" / "agent.json").read_text())
    assert rec["status"] == "zombie", "an unknown status must be left as-is"
    assert adapter.calls == [], "an unknown status must never reach a restart"


def _reap_project(tmp_path):
    graph = tmp_path / ".agi"
    (graph / "nodes" / "hypothesis").mkdir(parents=True)
    (graph / "sessions").mkdir(parents=True)
    (graph / "config.json").write_text("{}")
    return graph


def test_a_kid_that_died_after_writing_its_node_is_not_restarted(tmp_path, monkeypatch):
    """The 2026-08-31 field note, made structural.

    Kids routinely die AFTER their node landed, losing only the report.
    Respawning would redo finished work and hand a second agent the same
    scaffolded node.
    """
    d = _load_dispatch()
    graph = _reap_project(tmp_path)
    adapter = _FakeAdapter(pid=4242)

    monkeypatch.setattr(d, "spawn_budget", d.spawn_budget)
    import completion
    monkeypatch.setattr(completion, "is_complete", lambda root, nid: True)

    out = d._reap_one(graph, graph / "sessions" / "iter-1", adapter,
                      {"node_id": "hypothesis:h1", "tier": "kid"},
                      "a00", 999, cap=5, cfg={})

    assert out["record"]["status"] == "done-unreported"
    assert adapter.calls == [], "a completed kid must never be respawned"
    assert "only the report was lost" in out["record"]["fail_reason"]


def test_an_incomplete_kid_is_restarted_once_and_counted(tmp_path, monkeypatch):
    d = _load_dispatch()
    graph = _reap_project(tmp_path)
    adapter = _FakeAdapter(pid=4242)
    import completion
    monkeypatch.setattr(completion, "is_complete", lambda root, nid: False)

    out = d._reap_one(graph, graph / "sessions" / "iter-1", adapter,
                      {"node_id": "hypothesis:h1", "tier": "kid"},
                      "a00", 999, cap=5, cfg={})

    assert out["record"]["status"] == "running"
    assert out["record"]["pid"] == 4242
    assert out["record"]["restart_count"] == 1
    assert len(adapter.calls) == 1


def test_restarts_are_bounded_by_config(tmp_path, monkeypatch):
    d = _load_dispatch()
    graph = _reap_project(tmp_path)
    adapter = _FakeAdapter(pid=4242)
    import completion
    monkeypatch.setattr(completion, "is_complete", lambda root, nid: False)

    out = d._reap_one(graph, graph / "sessions" / "iter-1", adapter,
                      {"node_id": "hypothesis:h1", "restart_count": 1},
                      "a00", 999, cap=5, cfg={"reaper": {"max_restarts": 1}})

    assert out["record"]["status"] == "failed"
    assert adapter.calls == [], "a restart budget that does not bound is not a budget"


def test_a_restart_is_admitted_through_the_spawn_budget(tmp_path, monkeypatch):
    """A restart is a new process. A recovery path that ignores the
    concurrency bound can cause the outage it is recovering from."""
    d = _load_dispatch()
    graph = _reap_project(tmp_path)
    adapter = _FakeAdapter(pid=4242)
    import completion
    monkeypatch.setattr(completion, "is_complete", lambda root, nid: False)

    # Fill the budget with a live lease, then try to reap.
    held = d.spawn_budget.acquire(graph, 1, "occupant")
    d.spawn_budget.commit(held, os.getpid())

    out = d._reap_one(graph, graph / "sessions" / "iter-1", adapter,
                      {"node_id": "hypothesis:h1"}, "a00", 999, cap=1, cfg={})

    assert out["record"]["status"] == "failed"
    assert "budget full" in out["message"]
    assert adapter.calls == []


def test_an_unavailable_restart_fails_the_agent_rather_than_raising(tmp_path, monkeypatch):
    """The claude-code adapter raises NotImplementedError. A reaper that dies
    on it takes the whole dispatch with it."""
    d = _load_dispatch()
    graph = _reap_project(tmp_path)
    import completion
    monkeypatch.setattr(completion, "is_complete", lambda root, nid: False)

    class _NoRestart(_FakeAdapter):
        def restart(self, **kw):
            raise NotImplementedError("claude-code harness")

    out = d._reap_one(graph, graph / "sessions" / "iter-1", _NoRestart(),
                      {"node_id": "hypothesis:h1"}, "a00", 999, cap=5, cfg={})
    assert out["record"]["status"] == "failed"
    assert "restart unavailable" in out["record"]["fail_reason"]


def _branch_repo(tmp_path):
    """A real little git repo: `main` with one commit, `loop/x` cut from it
    with `n` commits on top. Returns (graph_root, branch, base)."""
    from subprocess import run
    root = tmp_path / "graph"
    root.mkdir()
    (root / ".agi").mkdir()
    (root / "config.json").write_text("{}")

    def g(*args):
        run(["git", "-C", str(root), *args], check=True,
            capture_output=True, text=True)

    g("init", "-q", "-b", "main")
    g("config", "user.email", "t@t")
    g("config", "user.name", "t")
    (root / "f").write_text("base\n")
    g("add", "f")
    g("commit", "-q", "-m", "base")
    g("checkout", "-q", "-b", "loop/x")
    for i in range(2):
        (root / "f").write_text((root / "f").read_text() + f"{i}\n")
        g("add", "f")
        g("commit", "-q", "-m", f"c{i}")
    # back on main so the worktree state mirrors a real main checkout
    g("checkout", "-q", "main")
    return root, "loop/x", "main"


def test_a_branch_agent_reaped_carries_commits_ahead(tmp_path, monkeypatch):
    """hypothesis:l3w4-branch-visibility — a `--branch` agent reaped by the
    reaper gets `commits_ahead` COMPUTED (rev-list main..branch == 2), never
    hand-counted, in the record that lands in agent.json."""
    d = _load_dispatch()
    graph, branch, base = _branch_repo(tmp_path)
    adapter = _FakeAdapter(pid=4242)
    import completion
    monkeypatch.setattr(completion, "is_complete", lambda root, nid: True)

    out = d._reap_one(graph, graph / "sessions" / "iter-1", adapter,
                      {"node_id": "hypothesis:h1", "tier": "kid",
                       "branch": branch, "base_branch": base},
                      "a00", 999, cap=5, cfg={})

    assert out["record"]["status"] == "done-unreported"
    assert out["record"]["commits_ahead"] == 2
    assert isinstance(out["record"]["commits_ahead"], int)
    assert adapter.calls == []


def test_commits_ahead_is_present_and_zero_for_no_commits(tmp_path, monkeypatch):
    """A branch cut but never advanced still stamps `commits_ahead == 0` —
    present and correct, not dropped as 'not ahead'."""
    d = _load_dispatch()
    graph, branch, base = _branch_repo(tmp_path)
    from subprocess import run as _run
    _run(["git", "-C", str(graph), "checkout", "-q", "-b", "loop/zero",
          "main"], check=True)
    adapter = _FakeAdapter(pid=4242)
    import completion
    monkeypatch.setattr(completion, "is_complete", lambda root, nid: True)

    out = d._reap_one(graph, graph / "sessions" / "iter-1", adapter,
                      {"node_id": "hypothesis:h1", "tier": "kid",
                       "branch": "loop/zero", "base_branch": base},
                      "a00", 999, cap=5, cfg={})

    assert out["record"]["commits_ahead"] == 0


def test_a_non_branch_agents_record_is_unchanged(tmp_path, monkeypatch):
    """No branch/base_branch -> no commits_ahead key at all; the record is
    byte-for-byte the same shape as before the change."""
    d = _load_dispatch()
    graph = _reap_project(tmp_path)
    adapter = _FakeAdapter(pid=4242)
    import completion
    monkeypatch.setattr(completion, "is_complete", lambda root, nid: True)

    out = d._reap_one(graph, graph / "sessions" / "iter-1", adapter,
                      {"node_id": "hypothesis:h1", "tier": "kid"},
                      "a00", 999, cap=5, cfg={})

    assert "commits_ahead" not in out["record"]
    assert out["record"]["status"] == "done-unreported"


def test_reaped_branch_agent_manifest_entry_gets_commits_ahead(tmp_path, monkeypatch):
    """The manifest.json entry mirrors agent.json: after a branch agent is
    reaped, both carry the same commits_ahead, so the round file and the
    manifest agree (hypothesis:l3w4-branch-visibility, 'in both')."""
    d = _load_dispatch()
    graph, branch, base = _branch_repo(tmp_path)
    iter_dir = graph / "sessions" / "iter-1"
    sess_dir = iter_dir / "a00"
    sess_dir.mkdir(parents=True)
    rec = {"id": "a00", "pid": 4242, "status": "running", "tier": "kid",
           "node_id": "hypothesis:h1", "branch": branch,
           "base_branch": base}
    (sess_dir / "agent.json").write_text(d.json.dumps(rec, indent=2))
    manifest = {"agents": [dict(rec)]}
    (iter_dir / "manifest.json").write_text(d.json.dumps(manifest, indent=2))

    class _Dead(_FakeAdapter):
        def is_alive(self, pid):
            return False

    import completion
    monkeypatch.setattr(completion, "is_complete", lambda root, nid: True)
    d._reaper_phase(graph, iter_dir, _Dead(), timeout_s=1, max_wait_s=1,
                    cap=5, cfg={})

    from json import loads
    agent = loads((sess_dir / "agent.json").read_text())
    man = loads((iter_dir / "manifest.json").read_text())
    assert agent["commits_ahead"] == 2
    assert man["agents"][0]["commits_ahead"] == 2


def test_the_mint_call_is_guarded_by_needs_credential():
    """goal:s34 item 2 — the red-on-purpose half of the experiment
    experiment:a00-d315f97b-8ec39a. The simulation the first draft of this
    test ran (a local copy of the `if` inside the test body) goes green even
    after the gate is deleted from dispatch.py, so it proves nothing about
    dispatch.py. This one reads the ACTUAL mint call site instead: the
    `provisioning.mint` call in main() must sit inside a condition that
    consults `adapters.needs_credential`. Delete the gate and this test is
    red.
    """
    import ast

    src = (BIN / "dispatch.py").read_text()
    tree = ast.parse(src)

    mint_calls = [
        n for n in ast.walk(tree)
        if isinstance(n, ast.Call)
        and isinstance(n.func, ast.Attribute)
        and n.func.attr == "mint"
        and isinstance(n.func.value, ast.Name)
        and n.func.value.id == "provisioning"
    ]
    assert mint_calls, "provisioning.mint call site missing from dispatch.py"

    # ast.walk gives no parent map; build one so a call can walk up.
    parents = {child: p for p in ast.walk(tree)
               for child in ast.iter_child_nodes(p)}

    def guarded(call):
        p = parents.get(call)
        while p is not None:
            if isinstance(p, ast.If):
                cond_src = ast.unparse(p.test)
                if "needs_credential" in cond_src:
                    return True
            p = parents.get(p)
        return False

    assert all(guarded(c) for c in mint_calls), (
        "every provisioning.mint call must be conditioned on "
        "adapters.needs_credential(harness); removing the gate must fail "
        "this test")


# ---------------------------------------------------------------------------
# hypothesis:l3w0-ladder-roles-table — resolve (tier, role) -> spec.
#
# The ladder node declares a `roles:` table (tier x role -> harness, model,
# effort, settings); dispatch resolves the row when it exists and falls back
# to config `harnesses.*.models[role]` when it does not.
# ---------------------------------------------------------------------------


def _roles():
    return [
        {"tier": 3, "role": "prime_director", "harness": "claude-code",
         "model": "claude-fable-5-1", "effort": "max", "settings": "ultracode"},
        {"tier": 3, "role": "parent", "harness": "claude-code",
         "model": "claude-opus-5", "effort": "max", "settings": "ultracode"},
        {"tier": 1, "role": "director", "harness": "claude-code",
         "model": "claude-fable-5-1", "effort": "max", "settings": ""},
        {"tier": 1, "role": "parent", "harness": "pi",
         "model": "~z-ai/glm-flash-latest", "effort": "", "settings": ""},
        {"tier": 0, "role": "kid", "harness": "pi",
         "model": "~deepseek/deepseek-v4-flash-latest", "effort": "", "settings": ""},
    ]


def _cfg():
    return {"spawn": {"harness": "pi"},
            "harnesses": {"pi": {"adapter": "pi",
                                   "models": {"kid": "default-kid",
                                               "parent": "default-parent"}}}}


def test_ladder_row_wins_over_config():
    """A ladder row for (0, kid) names deepseek; config fallback would say
    'default-kid'. The row must win."""
    spec = dispatch.resolve_role_spec(_cfg(), _roles(), 0, "kid")
    assert spec["from_ladder"] is True
    assert spec["harness"] == "pi"
    assert spec["model"] == "~deepseek/deepseek-v4-flash-latest"


def test_config_fallback_when_no_ladder_row():
    """No tier-2 kid row exists -> the config's models[kid] is the answer,
    exactly as dispatch behaved before the roles table."""
    spec = dispatch.resolve_role_spec(_cfg(), _roles(), 2, "kid")
    assert spec["from_ladder"] is False
    assert spec["model"] == "default-kid"


def test_empty_cell_values_resolve_to_none():
    """A row that omits effort/settings (the pi rows) resolves to None, so
    the adapter emits no --effort/--settings flag rather than a bare one."""
    spec = dispatch.resolve_role_spec(_cfg(), _roles(), 1, "parent")
    assert spec["from_ladder"] is True
    assert spec["effort"] is None
    assert spec["settings"] is None


def test_missing_roles_table_falls_back_to_config():
    spec = dispatch.resolve_role_spec(_cfg(), None, 0, "kid")
    assert spec["from_ladder"] is False
    assert spec["model"] == "default-kid"


def test_compile_role_rows_covers_every_declared_row():
    """The dry listing (--list-rows) must resolve one spec per declared row."""
    rows = dispatch._compile_role_rows(_roles())
    assert len(rows) == len(_roles())
    for tier, role, spec in rows:
        assert isinstance(tier, int)
        assert isinstance(role, str)
        assert spec["from_ladder"] is True
        assert spec["model"]


def test_default_tier_for_role():
    assert dispatch._default_tier_for_role("kid") == 0
    assert dispatch._default_tier_for_role("director") == 1
    assert dispatch._default_tier_for_role("prime_director") == 3


# ---------------------------------------------------------------------------
# hypothesis:l3w4-seat-registry — resolve a named seat -> spec.
#
# config:seats declares one row per seat; a seat's own cells override the
# ladder's (tier, role) class table. Missing registry / no row fails open.
# ---------------------------------------------------------------------------


def _seats():
    return [
        {"name": "belam", "role": "prime_director", "tier": 3,
         "harness": "claude-code", "model": "claude-fable-5-1",
         "effort": "max", "settings": "ultracode"},
        {"name": "liaison", "role": "director", "tier": 1,
         "harness": "claude-code", "model": "claude-sonnet-5",
         "effort": "high", "settings": ""},
    ]


def test_resolve_seat_spec_liaison_returns_sonnet_high_not_opus():
    """The liaison seat diverges from its director class (opus/max): the seat
    row names sonnet/high. Seat cells override the (tier, role) table."""
    spec = dispatch.resolve_seat_spec(_seats(), "liaison")
    assert spec is not None
    assert spec["from_seat"] is True
    assert spec["model"] == "claude-sonnet-5"
    assert spec["effort"] == "high"
    assert spec["model"] != "claude-opus-5"   # not the class table's opus


def test_dispatch_seat_flag_overrides_role_and_ladder_tier():
    """A seat is a more specific key than (tier, role): belam resolves its own
    fable-5.1/max row, not the tier-3 parent class opus/max."""
    spec = dispatch.resolve_seat_spec(_seats(), "belam")
    assert spec is not None
    assert spec["model"] == "claude-fable-5-1"
    assert spec["effort"] == "max"
    assert spec["settings"] == "ultracode"


def test_resolve_seat_spec_none_when_missing_fails_open():
    """No registry or no row -> None, so dispatch falls back to the ladder's
    (tier, role) lookup. A missing seat must never break dispatch."""
    assert dispatch.resolve_seat_spec(None, "liaison") is None
    assert dispatch.resolve_seat_spec(_seats(), "nobody") is None
    assert dispatch.resolve_seat_spec([], "belam") is None


def test_resolve_seat_spec_thinking_is_none_when_blank():
    """Hypothesis l3w4-director-kids-on-glm — a seat row that omits
    `thinking` (all of today) must resolve the cell to None so the adapter
    emits no --thinking flag rather than a bare one."""
    spec = dispatch.resolve_seat_spec(_seats(), "liaison")
    assert spec is not None
    assert spec["thinking"] is None
    sx = dispatch.resolve_seat_spec(
        [{"name": "glm", "role": "director", "tier": 1,
          "harness": "pi", "model": "~z-ai/glm-flash-latest",
          "effort": "", "thinking": "high", "settings": ""}], "glm")
    assert sx is not None
    assert sx["thinking"] == "high"


def test_thinking_cell_wins_over_config_default():
    """Hypothesis l3w4-director-kids-on-glm — when a ladder/seat row names
    `thinking`, that cell is threaded onto the harness so model_args emits
    `--thinking <cell>` (the configured/tier default loses). On a row with no
    thinking cell the spec carries None and default stands."""
    rows = [{"tier": 1, "role": "director", "harness": "pi",
             "model": "~z-ai/glm-flash-latest", "effort": "",
             "thinking": "high", "settings": ""}]
    spec = dispatch.resolve_role_spec(_cfg(), rows, 1, "director")
    assert spec["from_ladder"] is True
    assert spec["thinking"] == "high"
    assert spec["model"] == "~z-ai/glm-flash-latest"
    blank = dispatch.resolve_role_spec(_cfg(), _roles(), 0, "kid")
    assert blank["thinking"] is None


def test_default_role_follows_tier():
    """hypothesis:l3-dispatch-role-default — a bare --tier must not resolve
    the tier-0 kid row. Tier parent means role parent; tier kid means role
    kid; an explicit --role still wins over both."""
    assert dispatch._default_role_for_tier("parent") == "parent"
    assert dispatch._default_role_for_tier("kid") == "kid"
    assert dispatch._default_role_for_tier("prime_director") == "prime_director"


def test_parent_tier_without_role_resolves_parent_row():
    """The bug this pins: dispatch --tier parent (no --role) used to fall
    through to the tier-0 kid row (deepseek) because --role defaulted to
    'kid'. After the fix the resolved spec must be the tier-1 parent row
    (glm-flash-latest), not the kid model."""
    role = dispatch._default_role_for_tier("parent")
    spec = dispatch.resolve_role_spec(_cfg(), _roles(),
                                      dispatch._default_tier_for_role(role), role)
    assert spec["from_ladder"] is True
    assert spec["model"] == "~z-ai/glm-flash-latest"


# hypothesis:l3w3-advisor-brief — route tier-3 vision spawns to the advisor brief
# ------------------------------------------------------------


def test_brief_tier_routes_tier3_vision_parent_to_advisor():
    """The gap from l3w3-advisor-brief (addendum after L3.11): `dispatch.py
    --tier parent --ladder-tier 3 --target vision:<id>` still assembled the
    generic parent brief. An advisor sent out with the parent's job
    description would never sit the tier3-quorum or spawn its perpetual-goal
    director. When the spawn tier is parent, the ladder tier is 3 AND the
    target names a vision node, the brief tier must become `advisor` (the
    model/role still resolve as parent)."""
    assert dispatch._brief_tier_for("parent", 3, "vision:alive") == "advisor"
    assert dispatch._brief_tier_for("parent", 3, "vision:self-perpetuating") == "advisor"


def test_brief_tier_stays_parent_for_any_other_target():
    """Only a tier-3 parent aimed at a vision node becomes an advisor. A
    tier-3 parent aimed at a goal, unaimed, or at a lower ladder tier keeps
    the generic parent brief."""
    assert dispatch._brief_tier_for("parent", 3, "goal:g12.3") == "parent"
    assert dispatch._brief_tier_for("parent", 3, None) == "parent"
    assert dispatch._brief_tier_for("parent", 2, "vision:alive") == "parent"
    assert dispatch._brief_tier_for("kid", 3, "vision:alive") == "kid"


def test_dispatch_exports_agi_role_env():
    """Every spawn must carry AGI_ROLE so node_writer can stamp `role:` at
    mint. AST check -- dispatch writes spawn_env after Popen is built, so the
    only seam that proves it is the literal in the source."""
    import ast
    src = (BIN / "dispatch.py").read_text()
    tree = ast.parse(src)
    for n in ast.walk(tree):
        if isinstance(n, ast.Assign):
            for t in n.targets:
                if (isinstance(t, ast.Subscript)
                        and isinstance(t.slice, ast.Constant)
                        and t.slice.value == "AGI_ROLE"):
                    return
    pytest.fail("dispatch.py must export AGI_ROLE into the spawn environment")


# ---------------------------------------------------------------------------
# hypothesis:l3w3-advisor-brief addendum after L3.12 — the --goal flag threads
# the pinned perpetual goal into the advisor brief via the environment, so a
# spawn reads it through assemble without every harness adapter gaining a new
# keyword (claude_code_adapter.py is another kid's this round).
# ---------------------------------------------------------------------------

def test_goal_flag_sets_the_advisor_goal_env():
    """`apply_advisor_goal_env` seeds AGI_ADVISOR_GOAL from --goal and clears
    it when the flag is absent (a fresh process per dispatch, so a stale value
    from a prior test never leaks into a real spawn here)."""
    dispatch.apply_advisor_goal_env("goal:g15")
    assert os.environ.get("AGI_ADVISOR_GOAL") == "goal:g15"
    dispatch.apply_advisor_goal_env(None)
    assert "AGI_ADVISOR_GOAL" not in os.environ


def test_goal_flag_is_accepted_by_the_dispatch_argparser():
    """The flag has to exist on the dispatch CLI, not just the env helper. An
    AST-free structural check: `--goal` is registered as a command-line
    argument, so `dispatch.py ... --goal goal:g15` parses."""
    import ast
    src = (BIN / "dispatch.py").read_text()
    tree = ast.parse(src)
    found = any(
        isinstance(n, ast.Call)
        and getattr(n.func, "attr", "") == "add_argument"
        and any(isinstance(a, ast.Constant) and a.value == "--goal" for a in n.args)
        for n in ast.walk(tree)
    )
    assert found, "dispatch.py must register a --goal command-line flag"


def test_scaffold_stamps_the_child_row_not_the_spawner_env(tmp_path, monkeypatch):
    """hypothesis:l3-scaffold-stamps-spawner-env — the red-first build gate.

    A dispatch-spawned scaffold used to be stamped from the DISPATCHER's
    os.environ (node_writer reads AGI_LOOP/AGI_MODEL/AGI_PROFILE/AGI_ROLE at
    mint time), so a kid or advisor spawned under a parent inherited the
    PARENT's role/model/loop: every child was born role=parent model=glm. The
    fix resolves the child's row in dispatch BEFORE scaffolding and hands it
    to node_writer as an explicit `stamp`, which wins over the env.

    This test simulates the parent dispatcher's env still holding the spawner
    identity while the child row names the kid, scaffolds through the actual
    dispatch routine, and asserts the minted node carries the CHILD's stamps
    -- not the parent's env. Green here is the build Verdict-proved requires.
    """
    import yaml as _yaml

    d = _load_dispatch()
    root = tmp_path
    (root / "nodes" / "hypothesis").mkdir(parents=True)
    (root / "nodes" / "hypothesis" / "seed.md").write_text(
        "---\nid: hypothesis:seed\n---\nseed\n")
    (root / "agi-tree.config.json").write_text("{}")

    # The spawner (parent dispatcher) holds its OWN identity in os.environ.
    monkeypatch.setenv("AGI_ROLE", "parent")
    monkeypatch.setenv("AGI_MODEL", "claude-opus-5")
    monkeypatch.setenv("AGI_LOOP", "vision:alive@s2")
    monkeypatch.setenv("AGI_PROFILE", "ultracode")
    monkeypatch.setenv("AGI_SEASON", "7")

    # The child row dispatch resolves before scaffolding: a kid on the pi
    # harness aimed at a hypothesis extends it into an experiment.
    child = {
        "role": "kid",
        "loop": "hypothesis:seed@s2",
        "model": "~deepseek/deepseek-v4-flash-latest",
        "profile": "balanced",
        "season": "2",
    }

    info = d._scaffold_node_for_agent(root, 1, "a00-stubchild", "small",
                                      "hypothesis:seed", role="kid", stamp=child)
    assert info, "scaffold must write a node"
    fm = _yaml.safe_load(Path(info["path"]).read_text().split("---", 2)[1])
    assert fm["role"] == "kid", "node must carry the CHILD's role, not the parent's env"
    assert fm["model"] == "~deepseek/deepseek-v4-flash-latest"
    assert fm["loop"] == "hypothesis:seed@s2"
    assert fm["profile"] == "balanced"
    assert fm["season"] == 2


# ---------------------------------------------------------------------------
# hypothesis:l3w4-parent-branch-merge-up — dispatch.py --branch worktrees
# ---------------------------------------------------------------------------
# The dispatch half of the claim: `--branch` cuts each spawn its own git
# worktree on loop/<slug>-<agent8>@s<N> OFF the SPAWNER's branch, the child
# edits only that worktree (cwd + AGI_TREE_PROJECT_ROOT), and the lease /
# agent record carry branch/base_branch/worktree for season.py merge-up.
# Red-first: these were written before the helpers existed; the real-git
# tests fail when the worktree is missing or is rooted at the wrong layer.


def _git_repo(tmp_path: Path, branch: str = "init") -> Path:
    """git-init a project-looking repo with a committed `.agi/` graph, so
    worktrees cut from it carry their own graph (`.agi/` is tracked)."""
    repo = tmp_path / "main"
    repo.mkdir(parents=True)
    subprocess.run(["git", "-C", str(repo), "init", "-b", branch],
                   check=True, capture_output=True)
    for cfg in ("user.email", "user.name"):
        subprocess.run(["git", "-C", str(repo), "config", cfg, "t"],
                       check=True, capture_output=True)
    (repo / ".agi").mkdir(parents=True)
    (repo / ".agi" / "config.json").write_text('{"metric_primary": "x"}')
    (repo / "README").write_text("x")
    subprocess.run(["git", "-C", str(repo), "add", "-A"], check=True,
                   capture_output=True)
    subprocess.run(["git", "-C", str(repo), "commit", "-m", "init"],
                   check=True, capture_output=True)
    return repo


def test_loop_branch_name_carries_slug_agent_and_season():
    """ADDENDUM item 3: the agent id rides in the branch name so nested layers
    never collide; the slug tells a human which aim the branch carries. The
    branch shape is the grammar's `season<N>/loops/<slug>-<agent>`."""
    assert (dispatch.loop_branch_name("hypothesis:l3w4-x", "a00-abc8", 2)
            == "season2/loops/hypothesis-l3w4-x-a00-abc8")
    # colon flattened, explore fallback, season stamped
    assert dispatch.loop_branch_name(None, "a00-x", 1) \
        == "season1/loops/explore-a00-x"
    assert dispatch.loop_branch_name("mvp:g", "kid1", 3) \
        == "season3/loops/mvp-g-kid1"


def test_spawner_base_branch_returns_the_checked_out_branch(tmp_path):
    """ADDENDUM item 1: a new branch's base is the SPAWNER's branch, never a
    hardcoded season. This helper is what reads the spawner's HEAD."""
    repo = _git_repo(tmp_path)
    assert dispatch.spawner_base_branch(repo) == "init"
    subprocess.run(["git", "-C", str(repo), "checkout", "-b", "season/s1"],
                   check=True, capture_output=True)
    assert dispatch.spawner_base_branch(repo) == "season/s1"


def test_spawner_base_branch_none_when_detached(tmp_path):
    """A detached HEAD has no branch to base a child on — the helper must say
    so (return None) rather than hand a caller a wrong branch name."""
    repo = _git_repo(tmp_path)
    subprocess.run(["git", "-C", str(repo), "checkout", "--detach"],
                   check=True, capture_output=True)
    assert dispatch.spawner_base_branch(repo) is None


def test_branch_worktree_for_spawn_cuts_from_the_spawner_branch(tmp_path):
    """The real claim: `git worktree add <main>/.agi/worktrees/<agent>
    -b loop/<slug>-<agent8>@s<N> <spawner-branch>`. The worktree lands under
    the MAIN checkout's `.agi/worktrees/` and its tip EQUALS the recorded base
    branch (here a director layer, not the season) — so merge-up climbs one
    layer at a time and not straight to the season."""
    repo = _git_repo(tmp_path)
    subprocess.run(["git", "-C", str(repo), "checkout", "-b",
                    "tier1/director"], check=True, capture_output=True)
    (repo / "d.txt").write_text("director layer work\n")
    subprocess.run(["git", "-C", str(repo), "add", "-A"], check=True,
                   capture_output=True)
    subprocess.run(["git", "-C", str(repo), "commit", "-m", "director work"],
                   check=True, capture_output=True)

    wt = dispatch.branch_worktree_for_spawn(
        repo, "loop/explore-a00-xy@s2", "a00-xy", "tier1/director")

    # Worktree under the MAIN checkout's `.agi/worktrees/<agent>/`.
    assert str(wt) == str(repo / ".agi" / "worktrees" / "a00-xy")
    assert wt.is_dir()
    # The branch exists and is based on the SPAWNER's layer, not the season.
    branches = subprocess.run(["git", "-C", str(repo), "branch", "--list",
                               "loop/explore-a00-xy@s2"], capture_output=True,
                              text=True)
    assert "loop/explore-a00-xy@s2" in branches.stdout
    tip = subprocess.run(["git", "-C", str(repo), "log", "--oneline",
                          "loop/explore-a00-xy@s2", "-1"], capture_output=True,
                         text=True).stdout.strip()
    base = subprocess.run(["git", "-C", str(repo), "log", "--oneline",
                           "tier1/director", "-1"], capture_output=True,
                          text=True).stdout.strip()
    assert tip == base, ("the loop branch must sit on the SPAWNER's "
                         "director layer, not an empty season base")


def test_child_graph_resolves_to_the_worktrees_own_agi(tmp_path):
    """The kid edits only its own worktree: from inside the worktree the graph
    root resolves to the worktree's `.agi/`, so its node/scaffold writes land
    there and nowhere near another agent's tree."""
    repo = _git_repo(tmp_path)
    wt = dispatch.branch_worktree_for_spawn(
        repo, "loop/guide-a00-zz@s1", "a00-zz", "init")
    graph = dispatch.locations.find_project_root(wt)
    assert graph == (wt / ".agi").resolve()


def test_branch_kid_argv_shares_the_worktree_prefix(tmp_path, monkeypatch):
    """hypothesis:l3-branch-source-paths-never-rerooted, the red-first proof.

    dispatch.py re-roots the child GRAPH (`child_working_graph`) but, before
    the fix, left `cli_py` / `skill_prompt` / `dispatch_py` as module
    constants of the RUNNING (main) dispatch.py. A `--branch` kid's argv
    therefore carried a worktree-absolute scaffold path BESIDE main-absolute
    engine paths — and the model followed the only source anchor it was
    given, main. `child_engine_paths` re-roots all four through
    `locations.source_root` and the brief states the checkout out loud, so a
    `--branch` kid's argv must contain NO absolute path outside the worktree
    prefix: the real main checkout must never appear in it.
    """
    monkeypatch.setenv("AGI_PI_FORGIVENESS_BYPASS", "1")
    repo = _git_repo(tmp_path)
    wt = dispatch.branch_worktree_for_spawn(
        repo, "loop/explore-a00-test@s2", "a00-test", "init")
    child_graph = dispatch.locations.find_project_root(wt)
    assert child_graph == (wt / ".agi").resolve()

    # The re-rooted candidates only exist when the worktree carries an engine
    # layout; the minimal test repo has none, so give the worktree one.
    for rel in ("extensions/agi/bin/cli.py",
                "extensions/agi/bin/dispatch.py",
                "extensions/agi/lib/agent-prompt.md"):
        p = wt / rel
        p.parent.mkdir(parents=True, exist_ok=True)
        p.write_text("# engine placeholder\n", encoding="utf-8")

    engine_paths = dispatch.child_engine_paths(child_graph)

    ctx = wt / "ctx.md"
    ctx.write_text("placeholder\n", encoding="utf-8")
    sess = wt / "sess"
    sess.mkdir(parents=True, exist_ok=True)
    argv = dispatch.adapters.load("pi").build_command(
        harness={"adapter": "pi", "models": {}}, tier="kid",
        context_file=str(ctx), agent_id="a00-test", iter_n=1,
        sess_dir=sess, scaffold=None,
        cli_py=engine_paths["cli_py"],
        skill_prompt=engine_paths["skill_prompt"],
        dispatch_py=engine_paths["dispatch_py"],
        source_root=engine_paths["source_root"],
    )

    text = "\n".join(str(a) for a in argv)
    wt_pref = str(wt.resolve())
    bad = [p for p in re.findall(r"/\\S+", text)
           if not p.startswith(wt_pref)]
    assert not bad, (
        "a --branch kid's argv carries an absolute path outside its own "
        f"worktree ({wt_pref}): {bad}. The engine must be re-rooted to the "
        "child checkout, never left at the running dispatch's main "
        "constants."
    )
    assert f"YOUR CHECKOUT: {wt_pref}" in text, (
        "the brief must state the kid's own checkout out loud")


def test_branch_spawn_anchors_cohere_on_the_single_worktree_root(tmp_path, monkeypatch):
    """hypothesis:l3-branch-isolation-partial-break. The candidate-1 fix at
    hypothesis:l3-branch-source-paths-never-rerooted re-roots engine paths and
    states the checkout out loud, but each anchor is asserted separately: the
    argv test checks paths, the env test checks AGI_TREE_PROJECT_ROOT, and
    nothing checks that the Popen cwd, the env root, the re-rooted engine
    paths AND the brief's stated checkout all resolve to the SAME single
    worktree root. A disagreement among the four -- a main checkout serving as
    cwd or as the brief's source root while the nodes land in a worktree -- is
    exactly the partial-break signature this hypothesis named. Cohesion is the
    property the partial break destroyed: assert one worktree root holds all
    four, and that the real main checkout never appears in the launch bundle.
    """
    import os
    monkeypatch.setenv("AGI_PI_FORGIVENESS_BYPASS", "1")
    repo = _git_repo(tmp_path)
    main_root = os.path.realpath(str(repo))
    wt = dispatch.branch_worktree_for_spawn(
        repo, "loop/explore-a00-test@s2", "a00-test", "init")

    # The re-rooted candidates only exist when the worktree carries an engine
    # layout; the minimal test repo has none, so give the worktree one.
    for rel in ("extensions/agi/bin/cli.py",
                "extensions/agi/bin/dispatch.py",
                "extensions/agi/lib/agent-prompt.md"):
        p = wt / rel
        p.parent.mkdir(parents=True, exist_ok=True)
        p.write_text("# engine placeholder\n", encoding="utf-8")

    child_graph = dispatch.locations.find_project_root(wt)
    engine_paths = dispatch.child_engine_paths(child_graph)

    # The four anchors exactly as dispatch.main assembles them for --branch.
    wt_root = os.path.realpath(str(wt))
    cwd = os.path.realpath(str(wt))            # Popen(cwd=str(branch_root))
    env_root = os.path.realpath(str(wt))       # AGI_TREE_PROJECT_ROOT
    src_root = os.path.realpath(str(engine_paths["source_root"]))
    cli = os.path.realpath(str(engine_paths["cli_py"]))
    skill = os.path.realpath(str(engine_paths["skill_prompt"]))
    dp = os.path.realpath(str(engine_paths["dispatch_py"]))

    assert wt_root != main_root, "sanity: the worktree is a distinct checkout"

    # No anchor may escape the worktree, and the main checkout must never appear.
    for name, a in (("cwd", cwd), ("env_root", env_root), ("source_root", src_root),
                    ("cli_py", cli), ("skill_prompt", skill), ("dispatch_py", dp)):
        assert a.startswith(wt_root), (
            f"anchor {name}={a} escapes the worktree root {wt_root}; "
            f"main is {main_root}. The --branch spawn must launch wholly inside "
            "the worktree, not split across trees.")
        assert not a.startswith(main_root) or a.startswith(wt_root), (
            f"anchor {name}={a} resolves into the MAIN checkout {main_root}")

    # Cohesion: cwd, env root, and the brief's stated checkout are one root.
    assert src_root == wt_root, (
        f"the brief's stated checkout {src_root} must equal the process cwd "
        f"{cwd} - a split is the partial-break signature")
    assert env_root == wt_root, (
        f"AGI_TREE_PROJECT_ROOT {env_root} must equal the brief root {wt_root}")


def test_dispatch_branch_flag_is_registered():
    """The flag has to exist on the dispatch CLI. Structural, AST-free: the
    literal `--branch` must be handed to add_argument."""
    import ast
    src = (BIN / "dispatch.py").read_text()
    tree = ast.parse(src)
    found = any(
        isinstance(n, ast.Call)
        and getattr(n.func, "attr", "") == "add_argument"
        and any(isinstance(a, ast.Constant) and a.value == "--branch"
                for a in n.args)
        for n in ast.walk(tree)
    )
    assert found, "dispatch.py must register a --branch command-line flag"


def test_dispatch_branch_exports_agi_tree_project_root_to_the_child():
    """Under --branch the child is told its project root is the WORKTREE (via
    AGI_TREE_PROJECT_ROOT, the env project_root_from_env checks first), so its
    node + grid ops edit only that tree while shared budget/comms/meter go to
    the main checkout. AST check — dispatch writes spawn_env after Popen is
    built, so the literal in the source is the only seam that proves it."""
    import ast
    src = (BIN / "dispatch.py").read_text()
    tree = ast.parse(src)
    found = any(
        isinstance(n, ast.Assign)
        and any(
            isinstance(t, ast.Subscript)
            and isinstance(t.slice, ast.Constant)
            and t.slice.value == "AGI_TREE_PROJECT_ROOT"
            for t in n.targets)
        for n in ast.walk(tree)
    )
    assert found, ("dispatch.py must export AGI_TREE_PROJECT_ROOT into the "
                   "spawn environment on the --branch path")
    # spawn scripts also route `cwd` to the worktree root, not the main one.
    assert "cwd=str(branch_root)" in src, (
        "dispatch.py must launch the child from the worktree root (branch_root)")


def test_child_working_root_inherits_spawner_worktree_not_main(tmp_path):
    """L3.30 runtime defect (Belam VII): a parent spawned with `--branch`
    runs in its own worktree, and when it spawns a KID (--tier kid, no
    --branch) the kid must inherit that worktree as its working tree.
    Red-first: with the spawner's AGI_TREE_PROJECT_ROOT naming the worktree,
    `child_working_graph` must re-root the kid to the worktree's `.agi/`
    EVEN WHEN the passed project path resolves to the main checkout — the
    exact collapse Belam measured, where both worktrees stood empty while
    every kid's edits landed in the main tree."""
    repo = _git_repo(tmp_path)
    wt = dispatch.branch_worktree_for_spawn(
        repo, "loop/guide-a00-zz@s1", "a00-zz", "init")
    main_graph = dispatch.locations.find_project_root(repo)
    wt_graph = dispatch.locations.find_project_root(wt)
    assert main_graph != wt_graph, "sanity: the worktree has its own graph"

    # Parent passed the MAIN checkout path, but AGI_TREE_PROJECT_ROOT names
    # the spawner's worktree → the kid edits the worktree, not main.
    kid_root = dispatch.child_working_graph(
        passed_root=main_graph,
        spawner_env_root=str(wt.resolve()))
    assert kid_root == wt_graph, (
        "a kid spawned by a --branch parent must edit the parent's worktree, "
        "not walk back out to the main checkout")


def test_child_working_root_unchanged_without_a_worktree_spawner(tmp_path):
    """The re-root only fires when a dispatched --branch parent is the
    spawner. A top-level dispatch (seat/cron, no AGI_TREE_PROJECT_ROOT) must
    resolve exactly as before; so must a spawn whose env value names the same
    tree it was passed."""
    repo = _git_repo(tmp_path)
    main_graph = dispatch.locations.find_project_root(repo)
    # No spawner env → identity.
    assert dispatch.child_working_graph(passed_root=main_graph,
                                        spawner_env_root=None) == main_graph
    # Env names the SAME tree as passed → identity.
    assert dispatch.child_working_graph(passed_root=main_graph,
                                        spawner_env_root=str(repo)) == main_graph


def test_child_working_root_descends_deep_never_ascends(tmp_path):
    """hypothesis:a00-32f358d3-4ee42d — the env-root override DESCENDS but
    never ASCENDS. Red-first: cut a worktree W from main, then simulate a
    deep spawn chain (parent `--branch` in W → kid → grandkid → …). Each
    deeper level inherits AGI_TREE_PROJECT_ROOT=W and its passed root is the
    previous level's result, so every level must resolve to W's graph — which
    is shallower for levels ≥2 — and none may climb back to the main
    checkout, even when a level's passed root would otherwise resolve main.

    Existing tests cover the single hop (parent→kid). This pins the property
    the rest of the chain relies on: the override carries the deepest
    worktree down through any number of generations, and a descendant never
    ascends out of it."""
    repo = _git_repo(tmp_path)
    wt = dispatch.branch_worktree_for_spawn(
        repo, "loop/guide-a00-32f358d3@s2", "a00-32f358d3", "init")
    main_graph = dispatch.locations.find_project_root(repo)
    wt_graph = dispatch.locations.find_project_root(wt)
    assert main_graph != wt_graph, "sanity: the worktree has its own graph"

    # Level 1 = the --branch parent itself working in WT.
    root = wt_graph
    # Descend the chain: each level's passed root is the *child's* root, and
    # the inherited env still names the spawner's worktree WT. It must never
    # drift back to main_graph, for however many generations follow.
    for depth in range(2, 8):
        root = dispatch.child_working_graph(
            passed_root=root, spawner_env_root=str(wt.resolve()))
        assert root == wt_graph, (
            f"depth {depth}: env-root override must DESCEND to the deepest "
            f"worktree, never ascend back to the main checkout")

    # Never-ascends, adversarially: a deep child whose cwd/passed-root
    # resolves the MAIN checkout must be re-rooted back DOWN to the deepest
    # worktree by the inherited env — the child cannot climb out of WT merely
    # because its passed root names main.
    assert dispatch.child_working_graph(
        passed_root=main_graph,
        spawner_env_root=str(wt.resolve())) == wt_graph, (
        "a descendant must not ascend: env-root override re-roots a passed "
        "main path back down to the spawner's deepest worktree")


# ---------------------------------------------------------------------------
# hypothesis:l3w4-push-further-loops — the mechanical stop at the quorum
# ---------------------------------------------------------------------------
# A `--push-further` re-dispatch is REFUSED (exit 2) before any slot is
# admitted when --target names an overview/vision/moral node, so a
# push-further chain can loop through kid/parent/director tiers but never
# auto-continue INTO quorum-judged territory. Red-first: the gate and the
# flag threading are unit-tested against the real dispatch helpers.


def _make_node(root: Path, node_type: str, slug: str, fm: dict | None = None):
    d = root / "nodes" / node_type
    d.mkdir(parents=True, exist_ok=True)
    body = "---\n" + f"id: {node_type}:{slug}\ntype: {node_type}\n"
    for k, v in (fm or {}).items():
        if isinstance(v, str):
            body += f"{k}: {v}\n"
        else:
            body += f"{k}: {v}\n"
    body += "---\n"
    (d / f"{slug}.md").write_text(body)
    return f"{node_type}:{slug}"


def test_push_further_gate_refuses_quorum_targets(tmp_path):
    """overview/vision/moral are the node types a push stops before."""
    for t in ("overview", "vision", "moral"):
        node_id = _make_node(tmp_path, t, f"seed-{t}")
        gate = dispatch._push_further_gate(tmp_path, node_id)
        assert gate is not None, f"must refuse {t}"
        code, msg = gate
        assert code == 2
        assert "quorum-judged" in msg


def test_push_further_gate_requires_a_target(tmp_path):
    code, msg = dispatch._push_further_gate(tmp_path, None)
    assert code == 2
    assert "--target" in msg


def test_push_further_gate_allows_hypothesis_and_missing(tmp_path):
    """A hypothesis (or an unresolved id) is NOT the quorum stop — the flag
    threads through and the dispatch proceeds (zoom will surface a bad id)."""
    assert dispatch._push_further_gate(tmp_path, "hypothesis:seed") is None
    node_id = _make_node(tmp_path, "hypothesis", "seed")
    assert dispatch._push_further_gate(tmp_path, node_id) is None


def test_target_node_type_resolves_frontmatter(tmp_path):
    _make_node(tmp_path, "vision", "seed")
    assert dispatch._target_node_type(tmp_path, "vision:seed") == "vision"
    assert dispatch._target_node_type(tmp_path, "hypothesis:absent") is None


def test_zoom_command_threads_push_further(tmp_path):
    cmd = dispatch.zoom_command(tmp_path, 3, "a00", "small", "hypothesis:x",
                                push_further=True)
    assert "--push-further" in cmd
    cmd2 = dispatch.zoom_command(tmp_path, 3, "a00", "small", "hypothesis:x")
    assert "--push-further" not in cmd2


def test_scaffold_push_further_stamps_pushed_from(tmp_path):
    """A continuation kid's scaffold carries `pushed_from: <target>` so the
    re-dispatch leaves a trace of which node it was pushed from."""
    import yaml as _yaml
    root = tmp_path
    node_id = _make_node(root, "hypothesis", "seed")
    info = dispatch._scaffold_node_for_agent(
        root, 1, "a00-push", "small", node_id, role="kid",
        stamp={"role": "kid", "loop": f"{node_id}@s2", "model": "m", "profile": "b", "season": 2},
        extra_fm={"pushed_from": node_id})
    assert info, "push-further scaffold must write a node"
    fm = _yaml.safe_load(Path(info["path"]).read_text().split("---", 2)[1])
    assert fm["pushed_from"] == node_id


# --------------------------- the model/provider guard on the SPAWN path ----

def _guard_project(tmp_path: Path, model: str) -> Path:
    """Minimal project whose pi harness resolves `model` for the kid tier."""
    graph = tmp_path / ".agi"
    (graph / "nodes").mkdir(parents=True, exist_ok=True)
    (graph / "config.json").write_text(
        '{"metric_primary": "outcome_coverage",'
        ' "spawn": {"harness": "pi", "parallel": 1},'
        ' "harnesses": {"pi": {"adapter": "pi", "provider": "openrouter",'
        '                      "models": {"kid": "' + model + '"}}}}')
    return tmp_path


def _run_dispatch(root: Path):
    return subprocess.run(
        [sys.executable, str(BIN / "dispatch.py"), str(root), "1",
         "--tier", "kid", "--dry-run"],
        capture_output=True, text=True)


def test_dispatch_refuses_a_claude_alias_on_an_openrouter_harness(tmp_path):
    """hypothesis:l3-workflow-model-crosses-harness-namespace, spawn-path half.

    workflow.py has refused this since the incident; dispatch.py did not, and
    was safe only because every seat row and every `harnesses.pi.models` entry
    happened to hold a slug -- safe by data, not by rule. One cell edit
    (`harness: pi` beside `model: claude-sonnet-5`) was all it took to bill
    Anthropic against an OpenRouter key. It must refuse, before a credential
    is minted or a process starts -- so even `--dry-run` refuses.
    """
    res = _run_dispatch(_guard_project(tmp_path, "claude-sonnet-5"))
    combined = res.stdout + res.stderr
    assert res.returncode != 0, combined
    assert "claude-sonnet-5" in combined and "openrouter" in combined, combined


def test_dispatch_allows_a_real_openrouter_slug(tmp_path):
    """The control: the guard refuses a crossing, not every model. A real
    slug must still resolve, or the guard has broken every live dispatch."""
    res = _run_dispatch(_guard_project(tmp_path, "~z-ai/glm-flash-latest"))
    combined = res.stdout + res.stderr
    assert "not an OpenRouter slug" not in combined, combined


def test_openrouter_preflight_prints_the_sub_floor_notice_before_the_account_refusal(
        tmp_path, monkeypatch, capsys):
    """hypothesis:l4-sd06-residue-renumber-notice-fixture-dry-run-parity-
    refused-run-key conjunct (2). The notice surface — `dispatch.py`'s
    `notice: {msg}` when `check_key_floor` returns `(True, <marker>)` — had NO
    committed test anywhere in the tree: only the parent's own in-process
    probe exercised it. This is that test, on the live path and the live
    pre-flight (not a helper in isolation): with the key floor returning
    `(True, 'M')` and the account floor `(False, 'X')`, `notice: M` must reach
    stderr BEFORE `ERR: X`, and the round must reach NO spawn. FALSIFIER: drop
    the notice print and this test fails on the ordering assertion (it would
    also fail if the notice moved below the account floor)."""
    root = _guard_project(tmp_path, "~z-ai/glm-flash-latest")
    # `_guard_project` omits `allowed_models` (its tests stop at --dry-run,
    # which returns before the allowlist gate); the live pre-flight needs it.
    (root / ".agi" / "config.json").write_text(
        '{"metric_primary": "outcome_coverage",'
        ' "spawn": {"harness": "pi", "parallel": 1},'
        ' "harnesses": {"pi": {"adapter": "pi", "provider": "openrouter",'
        '   "models": {"kid": "~z-ai/glm-flash-latest"},'
        '   "allowed_extra": ["~z-ai/glm-flash-latest"]}}}')
    monkeypatch.setattr(dispatch.provisioning, "available",
                        lambda root=None: False)
    monkeypatch.setattr(dispatch.provisioning, "check_runtime_key_usable",
                        lambda cfg, root=None: (True, None))
    monkeypatch.setattr(dispatch.provisioning, "check_key_floor",
                        lambda cfg, root=None, iter_n=None: (True, "M"))
    monkeypatch.setattr(dispatch.provisioning, "check_account_floor",
                        lambda cfg, root=None: (False, "X"))
    monkeypatch.delenv("AGI_AGENT_ID", raising=False)
    monkeypatch.delenv("AGI_SEAT", raising=False)

    class _Proc:
        pid = 4242

    spawned: list = []

    def _popen(*a, **k):
        spawned.append(a)
        return _Proc()

    monkeypatch.setattr(dispatch.subprocess, "Popen", _popen)
    monkeypatch.setattr(sys, "argv", [
        str(BIN / "dispatch.py"), str(root), "1", "--tier", "kid",
        "--target", "hypothesis:x", "--harness", "pi"])
    rc = dispatch.main()
    err = capsys.readouterr().err
    assert rc == 1, err
    assert "notice: M" in err, err
    assert "ERR: X" in err, err
    assert err.index("notice: M") < err.index("ERR: X"), err
    assert spawned == [], f"a refused dispatch must never reach Popen: {spawned}"


# --- the respawn defect that cost money, 2026-09-10 -------------------------
# Two bugs in `_reap_one_impl`, both measured in production while the guards
# above were green. $2.01 of key burned in ~30 minutes across four rounds.


def test_restart_inherits_the_iteration_from_a_record_with_no_iter_key(tmp_path):
    """The REAL manifest shape: a record carries NO `iter` key.

    `test_reaper_restart_inherits_the_iteration_id` builds a record with
    `"iter": 342` and passes — but a real manifest record has no such key, so
    production took `rec.get("iter", 0)` -> 0 and every restart registered as
    `iter=0`. A sweep filtered by the round then reported it CLEAR while a
    restart was live in its worktree. The fixture was more generous than
    reality, so the guard could not see the bug it was written for.

    The round's own directory name is the authoritative source.
    """
    import json as _json
    root = tmp_path
    (root / "sessions").mkdir()
    iter_dir = root / "sessions" / "iter-L4.41"
    (iter_dir / "a00-abc123-r1").mkdir(parents=True)

    class FakeAdapter:
        def is_alive(self, pid):
            return False

        def restart(self, **kw):
            return 12345

    rec = {                      # exactly the keys a real manifest carries
        "id": "a00-abc123",
        "tier": "parent",
        "status": "running",
        "pid": 999,
        "restart_count": 0,
    }                            # <- no "iter", and no "node_id"
    dispatch._reap_one(root, iter_dir, FakeAdapter(), rec, "a00-abc123", 999,
                       cap=10, cfg={"reaper": {"max_restarts": 1}})

    import spawn_budget as _sb
    leases = [_json.loads(p.read_text())
              for p in _sb.budget_dir(root).glob("*.lease")]
    assert leases, "a restart should have left a lease"
    assert any(r.get("agent_id", "").endswith("-r1")
               and str(r.get("iter")) == "L4.41" for r in leases), (
        f"restart lease must carry the round's iteration, got {leases}")


def _git(repo, *args):
    return subprocess.run(["git", "-C", str(repo), *args],
                          capture_output=True, text=True, check=True)


def test_a_parent_that_committed_its_round_is_not_restarted(tmp_path):
    """A PARENT authors no node, so the node_id completion check never fires.

    Its manifest record carries `node_id: None` because it signals with
    `cli.py done --owns <kid-node-id>`, and the reaper reads the MAIN
    checkout's manifest while the parent updated its worktree's — so status
    stays "running" however cleanly it finished. Every parent that committed a
    finished round and exited was therefore respawned to redo it, and the
    respawn spawned fresh kids that wrote over committed work.

    A commit authored under the agent's id on its own branch is proof the work
    landed. This is the shape production actually produces.
    """
    repo = tmp_path / "main"
    (repo / ".agi" / "nodes").mkdir(parents=True)
    (repo / ".agi" / "config.json").write_text('{"metric_primary": "x"}')
    _git(repo.parent, "init", "-q", "-b", "season/s2", str(repo))
    for cfg in (("user.email", "t@t"), ("user.name", "t")):
        _git(repo, "config", *cfg)
    _git(repo, "add", "-A")
    _git(repo, "commit", "-qm", "base")
    _git(repo, "branch", "loop/round-a00-abc123@s2")
    _git(repo, "checkout", "-q", "loop/round-a00-abc123@s2")
    (repo / "work.txt").write_text("the round's work\n")
    _git(repo, "add", "-A")
    _git(repo, "commit", "-qm", "a00-abc123 done: experiment:x verdict=proved")
    _git(repo, "checkout", "-q", "season/s2")

    graph = repo / ".agi"
    iter_dir = graph / "sessions" / "iter-L4.41"
    iter_dir.mkdir(parents=True)

    class FakeAdapter:
        restarted = False

        def is_alive(self, pid):
            return False

        def restart(self, **kw):
            FakeAdapter.restarted = True
            return 12345

    rec = {
        "id": "a00-abc123",
        "tier": "parent",
        "status": "running",
        "pid": 999,
        "restart_count": 0,
        "branch": "loop/round-a00-abc123@s2",
        "base_branch": "season/s2",
    }
    out = dispatch._reap_one(graph, iter_dir, FakeAdapter(), rec,
                             "a00-abc123", 999, cap=10,
                             cfg={"reaper": {"max_restarts": 1}})
    assert out["record"]["status"] == "done-unreported", out
    assert "committed" in out["record"]["fail_reason"]
    assert FakeAdapter.restarted is False, "a committed round must not be respawned"


def test_a_parent_with_no_commit_on_its_branch_is_still_restarted(tmp_path):
    """The fix must not become a blanket no-restart.

    A parent killed mid-round leaves NO commit under its id, and that case
    must still restart exactly as before — otherwise stopping the money leak
    would have disabled recovery, which is the opposite failure.
    """
    repo = tmp_path / "main"
    (repo / ".agi" / "nodes").mkdir(parents=True)
    (repo / ".agi" / "config.json").write_text('{"metric_primary": "x"}')
    _git(repo.parent, "init", "-q", "-b", "season/s2", str(repo))
    for cfg in (("user.email", "t@t"), ("user.name", "t")):
        _git(repo, "config", *cfg)
    _git(repo, "add", "-A")
    _git(repo, "commit", "-qm", "base")
    _git(repo, "branch", "loop/round-a00-abc123@s2")

    graph = repo / ".agi"
    iter_dir = graph / "sessions" / "iter-L4.41"
    iter_dir.mkdir(parents=True)

    class FakeAdapter:
        restarted = False

        def is_alive(self, pid):
            return False

        def restart(self, **kw):
            FakeAdapter.restarted = True
            return 12345

    rec = {
        "id": "a00-abc123", "tier": "parent", "status": "running", "pid": 999,
        "restart_count": 0,
        "branch": "loop/round-a00-abc123@s2", "base_branch": "season/s2",
    }
    out = dispatch._reap_one(graph, iter_dir, FakeAdapter(), rec,
                             "a00-abc123", 999, cap=10,
                             cfg={"reaper": {"max_restarts": 1}})
    assert out["record"]["status"] != "done-unreported", out


def test_a_round_committed_under_the_kids_id_is_not_restarted(tmp_path):
    """🔴 The commit is the signal; its SUBJECT never is.

    Built from a real artefact, not from what the code hoped for. The two
    subjects below are copied verbatim from `iter-L4.57` and `iter-L4.58` on
    2026-09-10, where the reaper restarted both rounds:

        a00-852433f1 done: doc:l4-five-unstaffed-seats verdict=inconclusive_lean_proved:85
        a00-5b5defc6 done: experiment:a00-5b5defc6-7baa29 verdict=proved

    Neither leads with its PARENT's id (`a00-41c4e898`, `a00-325a5d78`), so
    the old `startswith(f"{agent_id} done:")` match returned False on a round
    that was fully committed with a clean worktree, and both parents were
    respawned onto finished work — roughly $0.9 of key. A third round the
    same hour, from the same director, happened to type its own id and was
    spared. Same code, same prompt, different string.

    Writing the fixture the other way — a subject the production path never
    produced — is exactly how a guard for this area was green while the bug
    was live, so this one uses the string that actually burned the money.
    """
    repo = tmp_path / "main"
    (repo / ".agi" / "nodes").mkdir(parents=True)
    (repo / ".agi" / "config.json").write_text('{"metric_primary": "x"}')
    _git(repo.parent, "init", "-q", "-b", "season/s2", str(repo))
    for cfg in (("user.email", "t@t"), ("user.name", "t")):
        _git(repo, "config", *cfg)
    _git(repo, "add", "-A")
    _git(repo, "commit", "-qm", "base")
    _git(repo, "checkout", "-q", "-b", "loop/round-a00-41c4e898@s2")
    (repo / "artefact.md").write_text("the round's work\n")
    _git(repo, "add", "-A")
    _git(repo, "commit", "-qm",
         "a00-852433f1 done: doc:l4-five-unstaffed-seats "
         "verdict=inconclusive_lean_proved:85")
    _git(repo, "checkout", "-q", "season/s2")

    graph = repo / ".agi"
    iter_dir = graph / "sessions" / "iter-L4.57"
    iter_dir.mkdir(parents=True)

    class FakeAdapter:
        restarted = False

        def is_alive(self, pid):
            return False

        def restart(self, **kw):
            FakeAdapter.restarted = True
            return 12345

    rec = {
        "id": "a00-41c4e898", "tier": "parent", "status": "running",
        "pid": 999, "restart_count": 0,
        "branch": "loop/round-a00-41c4e898@s2", "base_branch": "season/s2",
    }
    out = dispatch._reap_one(graph, iter_dir, FakeAdapter(), rec,
                             "a00-41c4e898", 999, cap=10,
                             cfg={"reaper": {"max_restarts": 1}})
    assert out["record"]["status"] == "done-unreported", out
    assert FakeAdapter.restarted is False, (
        "the round was committed — the parent's id not appearing in the "
        "subject is not evidence that it was not")
    assert out["record"]["commits_ahead"] == 1


def test_a_restart_names_itself_so_the_manifest_and_the_budget_agree(tmp_path):
    """A restart that leaves no trace cannot be counted, budgeted or believed.

    On iter-L4.57 and iter-L4.58 the manifest recorded a restarted parent as
    `status: running` with a silently swapped pid and nothing else — while
    `spawn_budget status` was listing the same process as `<id>-r1`. The only
    way to know a restart had happened was that the two disagreed. The record
    now carries `restart_of` under the lease's own name, so both readers name
    the process the same way.
    """
    repo = tmp_path / "main"
    (repo / ".agi" / "nodes").mkdir(parents=True)
    (repo / ".agi" / "config.json").write_text('{"metric_primary": "x"}')
    _git(repo.parent, "init", "-q", "-b", "season/s2", str(repo))
    for cfg in (("user.email", "t@t"), ("user.name", "t")):
        _git(repo, "config", *cfg)
    _git(repo, "add", "-A")
    _git(repo, "commit", "-qm", "base")
    _git(repo, "branch", "loop/round-a00-abc123@s2")

    graph = repo / ".agi"
    iter_dir = graph / "sessions" / "iter-L4.41"
    iter_dir.mkdir(parents=True)

    class FakeAdapter:
        def is_alive(self, pid):
            return False

        def restart(self, **kw):
            return 12345

    rec = {
        "id": "a00-abc123", "tier": "parent", "status": "running", "pid": 999,
        "restart_count": 0,
        "branch": "loop/round-a00-abc123@s2", "base_branch": "season/s2",
    }
    out = dispatch._reap_one(graph, iter_dir, FakeAdapter(), rec,
                             "a00-abc123", 999, cap=10,
                             cfg={"reaper": {"max_restarts": 1}})
    assert out["record"]["status"] == "running", out
    assert out["record"]["restart_count"] == 1
    assert out["record"]["restart_of"] == "a00-abc123-r1", (
        "the record must name the process by the lease name "
        "`spawn_budget status` shows, or the two readers disagree")


# hypothesis:l4-a-round-is-cut-from-the-branch-you-are-on — HALF A. The
# freshness guard that decides whether a `--branch` spawn is cut from a stale
# base. These tests pin the helper's fail-open and engine-path-filter behavior
# with a fake git, so no real network or repo is touched.


class _FakeGit:
    """A subprocess.run stand-in keyed on the git verb in argv."""

    def __init__(self, fetch_rc=0, revparse_rc=0, revparse_out="abc1234\n",
                 count_out="3\n", diff_out=""):
        self.fetch_rc = fetch_rc
        self.revparse_rc = revparse_rc
        self.revparse_out = revparse_out
        self.count_out = count_out
        self.diff_out = diff_out
        self.calls = []

    def __call__(self, cmd, **kwargs):
        self.calls.append(list(cmd))
        if "fetch" in cmd:
            return _FakeRes(self.fetch_rc)
        if "rev-parse" in cmd:
            return _FakeRes(self.revparse_rc, self.revparse_out)
        if "rev-list" in cmd:
            return _FakeRes(0, self.count_out)
        if "diff" in cmd:
            return _FakeRes(0, self.diff_out)
        return _FakeRes(0)


class _FakeRes:
    def __init__(self, returncode, stdout="", stderr=""):
        self.returncode = returncode
        self.stdout = stdout
        self.stderr = stderr


def test_is_engine_path_filters_graph_bytes():
    assert dispatch._is_engine_path("extensions/agi/bin/dispatch.py")
    assert dispatch._is_engine_path("bin/rotate.py")
    assert dispatch._is_engine_path("hooks/cc-session-start.sh")
    assert dispatch._is_engine_path("skills/agi/SKILL.md")
    assert not dispatch._is_engine_path(".agi/nodes/hypothesis/x.md")
    assert not dispatch._is_engine_path("GOALS.md")
    assert not dispatch._is_engine_path("payloads/foo.py")


def test_stale_base_spawn_current_when_even(tmp_path, monkeypatch):
    fake = _FakeGit(count_out="0\n")
    monkeypatch.setattr(dispatch.subprocess, "run", fake)
    out = dispatch._stale_base_spawn(tmp_path, season=2)
    assert out["status"] == "current", out
    assert out["behind"] == 0
    assert out["files"] == []


def test_stale_base_spawn_behind_names_engine_files(tmp_path, monkeypatch):
    fake = _FakeGit(count_out="7\n", diff_out=(
        "extensions/agi/bin/dispatch.py\n"
        ".agi/nodes/goal/g17.md\n"
        "hooks/cc-session-start.sh\n"
        "GOALS.md\n"
        "bin/rotate.py\n"))
    monkeypatch.setattr(dispatch.subprocess, "run", fake)
    out = dispatch._stale_base_spawn(tmp_path, season=2)
    assert out["status"] == "behind", out
    assert out["behind"] == 7
    # engine paths only — graph bytes and derived docs must not be named
    assert out["files"] == [
        "bin/rotate.py",
        "extensions/agi/bin/dispatch.py",
        "hooks/cc-session-start.sh",
    ], out


def test_stale_base_spawn_fails_open_on_fetch_failure(tmp_path, monkeypatch):
    fake = _FakeGit(fetch_rc=128)  # e.g. remote unreachable
    monkeypatch.setattr(dispatch.subprocess, "run", fake)
    out = dispatch._stale_base_spawn(tmp_path, season=2)
    assert out["status"] == "unchecked", out
    assert out["behind"] == 0
    assert "stale" not in out["status"], "an unreachable remote must not "
    "'read stale' — that would be a false signal to block on"


def test_stale_base_spawn_fails_open_when_remote_ref_unresolvable(
        tmp_path, monkeypatch):
    fake = _FakeGit(revparse_rc=1, revparse_out="")
    monkeypatch.setattr(dispatch.subprocess, "run", fake)
    out = dispatch._stale_base_spawn(tmp_path, season=2)
    assert out["status"] == "unchecked", out


def test_stale_base_record_is_structured_with_actions(tmp_path, monkeypatch):
    fake = _FakeGit(count_out="3\n", diff_out="extensions/agi/bin/dispatch.py\n")
    monkeypatch.setattr(dispatch.subprocess, "run", fake)
    stale = dispatch._stale_base_spawn(tmp_path, season=2)
    rec = dispatch._stale_base_record(stale, season=2)
    assert rec["issue"] == "stale-base"
    assert rec["behind"] == 3
    assert rec["integration"] == "season2/main"
    ids = [a["id"] for a in rec["actions"]]
    assert "sync" in ids and "override" in ids and "abort" in ids, (
        "the must-pick floor: a re-invocation carries one of these — a "
        "synced base, --allow-stale-base <reason>, or an abort")
    assert any("--allow-stale-base" in a.get("cmd", "")
               for a in rec["actions"]), rec


# ---------------------------------------------------------------------------
# Residue 4 — town_branches reader + stale-base guard measured against the
# round's OWN town integration branch (hypothesis:l4-towns-each-app-is-a-
# vision-with-its-own-council; owner ruling 01:4xZ).
# ---------------------------------------------------------------------------


def _town_ladder(repo: Path, season: int = 2) -> Path:
    """Write a ladder with a `town_branches` map into the repo's graph.

    Fixtures write their OWN temp ladder (the live ladder node is READ ONLY).
    The map value is OPAQUE CONFIG (owner ruling 01:4xZ) — code must never
    parse the branch name, only compare it by exact equality.
    """
    geom = repo / ".agi" / "nodes" / ".geometry"
    geom.mkdir(parents=True, exist_ok=True)
    ladder = geom / "ladder.md"
    ladder.write_text(
        "---\nid: ladder:ladder\ntype: ladder\n"
        f"current_season: {season}\n"
        "town_branches:\n"
        "  core: season/s2\n"
        "  streaming-suite: town/streaming-suite@s2\n"
        "  web-app-suite: town/web-app-suite@s2\n"
        "---\nbody\n", encoding="utf-8")
    return ladder


def test_town_branch_behind_season_not_stale_against_own_branch(
        tmp_path):
    """A town branch behind season/s2 must NOT be reported stale against its
    OWN integration branch, and the fallback must still measure plain
    season/s2 exactly as before (residue 4).

    Setup: a repo whose season/s2 is AHEAD of the town branch, so a plain
    season/s2 measurement reads `behind` while the town's own branch is even
    with the spawner's HEAD -> `current`. Both facts must hold from ONE repo.
    """
    repo = _git_repo(tmp_path, branch="season/s2")
    _town_ladder(repo, season=2)
    # The town branch is cut from season/s2 TODAY (even).
    _git(repo, "branch", "town/streaming-suite@s2")
    # Advance season/s2 past the town branch so plain-s2 reads stale.
    (repo / "README").write_text("x2")
    _git(repo, "add", "-A")
    _git(repo, "commit", "-m", "ahead of town")
    # A bare origin holding both branches, season/s2 at its NEW tip and the
    # town branch at the OLD (even) commit, so the stale guard has a real
    # remote tip to measure against (fetch beats a local ref's last sight).
    bare = tmp_path / "remote.git"
    _git(repo, "clone", "--bare", ".", str(bare))

    def _bare(*args):
        return subprocess.run(["git", "-C", str(bare), *args],
                              capture_output=True, text=True, check=True)

    # origin/season/s2 = new tip; origin/town/... = the even commit.
    _bare("branch", "-f", "season/s2", "season/s2")
    town_tip = _git(repo, "rev-parse", "town/streaming-suite@s2").stdout.strip()
    _bare("branch", "-f", "town/streaming-suite@s2", town_tip)
    _bare("symbolic-ref", "HEAD", "refs/heads/season/s2")
    # Point the local repo's origin at the bare, and fetch both refs locally
    # so the stale guard's `git fetch origin <ref>` resolves against it.
    _git(repo, "remote", "add", "origin", str(bare))
    _git(repo, "fetch", "origin", "season/s2")
    _git(repo, "fetch", "origin", "town/streaming-suite@s2")

    # Spawner sits on the town branch (its own integration line).
    _git(repo, "checkout", "town/streaming-suite@s2")
    assert _git(repo, "rev-parse", "--abbrev-ref", "HEAD").stdout.strip() \
        == "town/streaming-suite@s2"

    # Measured against ITS OWN town branch: even -> current, never stale.
    out = dispatch._stale_base_spawn(repo, season=2,
                                     town_branch="town/streaming-suite@s2")
    assert out["status"] == "current", (
        "a town branch even with its own integration line must not read "
        f"stale, however far season/s2 has run ahead: {out}")

    # The same HEAD measured against the FALLBACK (no town branch): the plain
    # season/s2 base is 1 behind -> the plain-s2 behaviour is unchanged.
    fallback = dispatch._stale_base_spawn(repo, season=2)
    assert fallback["status"] == "behind", fallback
    assert fallback["behind"] == 1, fallback
    rec = dispatch._stale_base_record(fallback, season=2)
    assert rec["integration"] == "season2/main", rec
    # The town-path record names the town branch, and its sync target too.
    trec = dispatch._stale_base_record(out, season=2,
                                       town_branch="town/streaming-suite@s2")
    assert trec["integration"] == "town/streaming-suite@s2", trec
    assert any("town/streaming-suite@s2" in a.get("cmd", "")
               for a in trec["actions"]), trec


def test_town_of_branch_resolver_is_exact_equality(tmp_path, monkeypatch):
    """The branch -> town reverse lookup and town -> branch resolver never
    parse the opaque value; only exact string equality maps either way."""
    repo = _git_repo(tmp_path, branch="season/s2")
    _town_ladder(repo, season=2)

    from dispatch import _current_town_branch

    nodes = repo / ".agi" / "nodes"
    # On the town branch HEAD resolves to the town's integration branch.
    _git(repo, "branch", "town/streaming-suite@s2")
    _git(repo, "checkout", "town/streaming-suite@s2")
    assert _current_town_branch(repo, nodes) == "town/streaming-suite@s2"
    # On plain season/s2 (core's own branch, per the test ladder) the resolved
    # town branch IS season/s2 — identical refs to the fallback, so the plain
    # base behaves exactly as today.
    _git(repo, "checkout", "season/s2")
    assert _current_town_branch(repo, nodes) == "season/s2"
    # A branch listed in NO town's opaque map (a seat/loop branch) maps to
    # None -> the guard keeps the plain season/s2 base, byte-for-byte.
    _git(repo, "checkout", "-b", "loop/slug-aaaa@s2")
    assert _current_town_branch(repo, nodes) is None


# ---------------------------------------------------------------------------
# hypothesis:l4-branches-follow-the-season-grammar — the stale-base guard
# must resolve the town/integration branch CANONICAL-first with the one-season
# legacy alias as fallback, so a pre-migration origin that has NOT been
# renamed yet stays measurable instead of failing OPEN to "unchecked".
# ---------------------------------------------------------------------------


def _origin_bare(tmp_path, repo, only_refs, head_ref, repoint=None):
    """A bare origin cloned from `repo`, then pruned to carry ONLY the branch
    names in `only_refs`, HEAD pointed at `head_ref`. `repoint` maps a legacy
    name to the target ref it should point at (so an origin can carry just the
    OLD name at an AHEAD tip). Adds the origin remote to `repo`. Returns
    (bare_path, _bare) so a caller can keep driving origin git ops."""
    bare = tmp_path / "remote.git"
    _git(repo, "clone", "--bare", "-q", ".", str(bare))

    def _bare(*args):
        return subprocess.run(["git", "-C", str(bare), *args],
                              capture_output=True, text=True, check=True)

    for name, target in (repoint or {}).items():
        # exists in the clone (via another branch), so it resolves in the bare.
        _bare("branch", "-f", name, target)
    refs = _git(bare, "for-each-ref", "--format=%(refname)", "refs/heads")
    for r in refs.stdout.splitlines():
        name = r.split("refs/heads/", 1)[1]
        if name not in only_refs:
            _bare("branch", "-D", name)
    _bare("symbolic-ref", "HEAD", f"refs/heads/{head_ref}")
    _git(repo, "remote", "add", "origin", str(bare))
    return bare, _bare


def test_stale_base_loop_resolves_only_legacy_origin(tmp_path):
    """THE regression this round exists for: on an origin carrying ONLY the
    legacy `season/s2`, a spawner on a canonical core post/loop branch must
    read a real fate (`behind`, by a known count) — NEVER `unchecked`.

    Pre-fix, the town/integration branch (`season2/main`, resolved by
    `_current_town_branch` from the post/loop) was fetched as the canonical
    name ALONE; on a pre-migration origin that name 404s, `integration` stayed
    None, and the guard failed OPEN to "unchecked" for EVERY nested spawn
    until the live rename. The fix routes town_branch through
    `branches.ref_candidates`, so the legacy `season/s2` resolves."""
    repo = _git_repo(tmp_path, branch="season2/main")
    _git(repo, "branch", "season/s2")
    # Advance season/s2's TARGET past the loop base so the legacy origin is
    # AHEAD by exactly one known commit once repointed onto it.
    (repo / "README").write_text("x2")
    _git(repo, "add", "-A")
    _git(repo, "commit", "-qm", "ahead of loop base")
    _git(repo, "checkout", "-q", "season/s2")
    _git(repo, "branch", "season2/loops/round-a00-abc123")
    _git(repo, "checkout", "-q", "season2/loops/round-a00-abc123")
    # HEAD is now the loop base; origin carries ONLY season/s2, at the ahead tip.
    _origin_bare(tmp_path, repo, only_refs=["season/s2"],
                 head_ref="season/s2", repoint={"season/s2": "season2/main"})
    from dispatch import _current_town_branch
    town_branch = _current_town_branch(repo, repo / ".agi" / "nodes")
    assert town_branch == "season2/main", town_branch
    out = dispatch._stale_base_spawn(repo, season=2, town_branch=town_branch)
    assert "unchecked" not in out["status"], (
        "a resolvable legacy origin must not fail open: " + str(out))
    assert out["status"] == "behind" and out["behind"] == 1, out


def test_stale_base_both_names_fetches_canonical_first(tmp_path):
    """An origin carrying BOTH `season2/main` and `season/s2` must be fetched
    via the CANONICAL name — the legacy alias is never consulted once the
    canonical resolves (candidates are tried in order and we break on the
    first success, so the legacy remote-tracking ref never materialises)."""
    repo = _git_repo(tmp_path, branch="season2/main")
    _git(repo, "branch", "season/s2")
    _git(repo, "checkout", "-q", "season/s2")
    (repo / "README").write_text("x2")
    _git(repo, "add", "-A")
    _git(repo, "commit", "-qm", "legacy ahead")
    _git(repo, "checkout", "-q", "season2/main")
    _origin_bare(tmp_path, repo,
                 only_refs=["season2/main", "season/s2"],
                 head_ref="season2/main")
    out = dispatch._stale_base_spawn(repo, season=2,
                                     town_branch="season2/main")
    assert out["status"] == "current", out  # even vs origin/season2/main
    resolved = subprocess.run(
        ["git", "-C", str(repo), "rev-parse", "--verify",
         "origin/season2/main^{commit}"], capture_output=True, text=True)
    assert resolved.returncode == 0, (resolved.stdout, resolved.stderr)
    legacy = subprocess.run(
        ["git", "-C", str(repo), "rev-parse", "--verify", "--quiet",
         "origin/season/s2^{commit}"], capture_output=True, text=True)
    assert legacy.returncode != 0, (
        "legacy must not be fetched when the canonical resolves")


def test_stale_base_canonical_town_main_reaches_legacy_literal_origin(tmp_path):
    """The ladder-town case: a town_branch supplied as the CANONICAL town main
    (`season2/streaming-suite/season1/main` — what `_current_town_branch`
    returns for a spawner on that town's canonical post/loop) must still
    resolve on an origin that carries ONLY the literal `town/streaming-suite@s2`
    legacy branch. That literal form is derived by the grammar's own
    ref_candidates/_canonical_to_old for a k==1 town main (hypothesis:
    l4-every-reader-resolves-a-branch-through-branches-py: every resolving
    spelling comes from branches.py, never hand-spelled in dispatch) — an
    unreachable-name 404 must never masquerade as "unchecked" only because
    the resolver stopped routing through the grammar."""
    repo = _git_repo(tmp_path, branch="season/s2")
    _git(repo, "branch", "town/streaming-suite@s2")
    _git(repo, "checkout", "-q", "town/streaming-suite@s2")
    (repo / "README").write_text("x2")
    _git(repo, "add", "-A")
    _git(repo, "commit", "-qm", "town main ahead")
    _origin_bare(tmp_path, repo, only_refs=["town/streaming-suite@s2"],
                 head_ref="town/streaming-suite@s2")
    out = dispatch._stale_base_spawn(
        repo, season=2,
        town_branch="season2/streaming-suite/season1/main")
    assert "unchecked" not in out["status"], out
    resolved = subprocess.run(
        ["git", "-C", str(repo), "rev-parse", "--verify",
         "origin/town/streaming-suite@s2^{commit}"], capture_output=True,
        text=True)
    assert resolved.returncode == 0, (
        "the legacy literal ref must have been fetched and resolved: "
        f"{resolved.stdout} {resolved.stderr}")


def test_stale_base_multiseason_town_main_invents_no_town_at_alias(tmp_path):
    """A MULTI-season town main (`season3/core/season5/main`) must NOT be
    measured against the invented literal `town/core@s3` — that spelling
    resolves to the season-one branch `season3/core/season1/main`, a
    DIFFERENT branch, so fetching it would be measuring a fork. The pre-fix
    hand-spelled resolver (_town_at_legacy, removed) emitted exactly that
    wrong alias; the grammar's ref_candidates derives the one-season town
    alias only for k==1 town mains, so routing through it drops the bogus
    candidate by construction (hypothesis:
    l4-every-reader-resolves-a-branch-through-branches-py)."""
    repo = _git_repo(tmp_path, branch="season3/main")
    _git(repo, "branch", "season3/core/season5/main")
    _git(repo, "checkout", "-q", "season3/core/season5/main")
    (repo / "README").write_text("x5")
    _git(repo, "add", "-A")
    _git(repo, "commit", "-qm", "multiseason town ahead")
    # The fork a pre-migration tree might carry: a season-ONE branch plus the
    # town-at alias `town/core@s3` that points AT it — a DIFFERENT branch from
    # the guard's multi-season main. The guard must never fetch it.
    _git(repo, "branch", "season3/core/season1/main")
    _git(repo, "checkout", "-q", "season3/core/season1/main")
    (repo / "README").write_text("x1")
    _git(repo, "add", "-A")
    _git(repo, "commit", "-qm", "season one fork")
    _git(repo, "branch", "town/core@s3", "season3/core/season1/main")
    _git(repo, "checkout", "-q", "season3/core/season5/main")
    _origin_bare(tmp_path, repo,
                 only_refs=["season3/core/season5/main", "town/core@s3"],
                 head_ref="season3/core/season5/main")
    out = dispatch._stale_base_spawn(
        repo, season=3, town_branch="season3/core/season5/main")
    assert out["status"] == "current", out
    # The guard resolved against the canonical multi-season main — never the
    # `town/core@s3` alias of the season-one branch, which is NOT the origin
    # it is behind.
    wrong = subprocess.run(
        ["git", "-C", str(repo), "rev-parse", "--verify", "--quiet",
         "origin/town/core@s3^{commit}"], capture_output=True, text=True)
    assert wrong.returncode != 0, (
        "a multi-season town main must never be measured against the "
        "season-one town-at alias: origin/town/core@s3 was fetched")


# ---------------------------------------------------------------------------
# hypothesis:l4-a-parent-cuts-five-and-merges-its-kids — the parent-kid
# ceiling becomes a refusal, not just a printed number.
# ---------------------------------------------------------------------------

def _kid_manifest(n_kids, by="P"):
    """A manifest with n_kids records all stamped spawned_by_agent=<by>."""
    return {
        "iter": 1,
        "agents": [
            {"id": f"k{i}", "tier": "kid", "spawned_by_agent": by}
            for i in range(n_kids)
        ],
    }


def _kid_cfg(ceiling):
    return {"spawn": {"parent_max_kids": ceiling}}


def test_parent_kid_ceiling_gate_refuses_at_ceiling_and_names_both_numbers(monkeypatch):
    """FIXTURES ONLY — a temp manifest, never this repo. A parent that has
    already dispatched `spawn.parent_max_kids` kids is REFUSED its next kid
    with BOTH numbers in the message, exactly the shape the brief expects
    ('refuses kid 6' at ceiling 5)."""
    monkeypatch.setenv("AGI_AGENT_ID", "P")
    refused = dispatch._parent_kid_ceiling_gate(_kid_manifest(5), _kid_cfg(5), 1)
    assert refused is not None
    code, msg = refused
    assert code == 2
    assert "ERR parent P has dispatched 5 kids" in msg
    assert "spawn.parent_max_kids=5" in msg
    assert "refuses kid 6" in msg


def test_parent_kid_ceiling_gate_passes_below_the_ceiling(monkeypatch):
    monkeypatch.setenv("AGI_AGENT_ID", "P")
    assert dispatch._parent_kid_ceiling_gate(_kid_manifest(4), _kid_cfg(5), 1) is None
    # exactly at the ceiling is allowed when THIS invocation adds no kid
    assert dispatch._parent_kid_ceiling_gate(_kid_manifest(5), _kid_cfg(5), 0) is None


def test_parent_kid_ceiling_gate_counts_only_that_parents_kids(monkeypatch):
    """Records spawned by OTHER parents or by nobody must not count against
    this parent's ceiling."""
    monkeypatch.setenv("AGI_AGENT_ID", "P")
    manifest = {
        "agents": (
            [{"id": f"o{i}", "tier": "kid", "spawned_by_agent": "OTHER"}
             for i in range(5)]
            + [{"id": "human", "tier": "kid"}]  # no spawned_by_agent at all
        )
    }
    assert dispatch._parent_kid_ceiling_gate(manifest, _kid_cfg(5), 1) is None


def test_parent_kid_ceiling_gate_fails_open_without_agent_id(monkeypatch):
    """A director or a human at a shell has no AGI_AGENT_ID — the gate must
    NEVER fire, however many kid records exist, exactly like the stale-base
    gate."""
    monkeypatch.delenv("AGI_AGENT_ID", raising=False)
    assert dispatch._parent_kid_ceiling_gate(_kid_manifest(50), _kid_cfg(5), 1) is None


def _live_manifest(parent_id, parent_pid):
    return {"iter": 1, "agents": [{"id": parent_id, "pid": parent_pid}]}


def test_kid_of_live_manifest_parent_is_account_floor_exempt(monkeypatch):
    """l4-a-kid-spawn... — a kid whose parent (AGI_AGENT_ID) is a manifest
    record with a LIVE pid is exempt from the ACCOUNT floor: the helper
    returns the parent id+pid so the pre-flight prints the exempt line and
    skips check_account_floor (the key floor still runs)."""
    monkeypatch.setenv("AGI_AGENT_ID", "parent-a")
    monkeypatch.setattr(dispatch.spawn_budget, "_pid_alive", lambda pid: True)
    got = dispatch._kid_account_floor_exemption(_live_manifest("parent-a", 999))
    assert got == ("parent-a", 999)


def test_kid_with_no_manifest_parent_is_not_account_floor_exempt(monkeypatch):
    """A kid whose parent id is NOT in the iter manifest must read the floor
    as today (refused, floor named) — no record, no exemption."""
    monkeypatch.setenv("AGI_AGENT_ID", "parent-a")
    assert dispatch._kid_account_floor_exemption({"agents": []}) is None


def test_kid_of_a_dead_parent_is_not_account_floor_exempt(monkeypatch):
    """A dead parent (pid not alive) must NOT grant the exemption — the round
    is gone, so its kids read the floor like any other spawn."""
    monkeypatch.setenv("AGI_AGENT_ID", "parent-a")
    monkeypatch.setattr(dispatch.spawn_budget, "_pid_alive", lambda pid: False)
    assert dispatch._kid_account_floor_exemption(_live_manifest("parent-a", 999)) is None


def test_non_kid_spawner_without_agent_id_is_not_account_floor_exempt(monkeypatch):
    """A director or human at a shell (no AGI_AGENT_ID) is never exempt —
    the account floor applies to a top-level spawn exactly as before, which is
    what a kid tier with no caller identity would look like too."""
    monkeypatch.delenv("AGI_AGENT_ID", raising=False)
    assert dispatch._kid_account_floor_exemption(_live_manifest("parent-a", 999)) is None


def test_parent_kid_ceiling_gate_passes_with_no_manifest_agents(monkeypatch):
    monkeypatch.setenv("AGI_AGENT_ID", "P")
    assert dispatch._parent_kid_ceiling_gate({"agents": []}, _kid_cfg(5), 1) is None


def test_reap_pass_mirrors_terminal_record_in_inline_lane(tmp_path, monkeypatch):
    """hyp:l4-the-manifest-mirrors-terminal-agent-status — inline-lane
    (restart_ok=True) parity. `_reap_pass` copies a TERMINAL (done) agent.json
    onto a manifest entry that still reads `running`, returns it under the NEW
    `mirrored` key, does NOT put it in marked/still/died, and stays lane-
    independent (same mirror under restart_ok=True). No restart is attempted
    for a terminal record."""
    import json
    d = _load_dispatch()
    graph = _reap_project(tmp_path)
    iter_dir = graph / "sessions" / "iter-mir"
    (iter_dir / "a00-mir").mkdir(parents=True)
    (iter_dir / "manifest.json").write_text(json.dumps(
        {"agents": [{"id": "a00-mir", "status": "running"}]}))
    (iter_dir / "a00-mir" / "agent.json").write_text(json.dumps(
        {"id": "a00-mir", "status": "done", "finished_at": 7,
         "fail_reason": "completed"}))
    adapter = _FakeAdapter(pid=4242)
    monkeypatch.setattr(d, "stall_detect",
                        type("NS", (), {"record_stalled_in_iteration":
                                        lambda *a, **k: None})())

    out = d._reap_pass(graph, iter_dir, adapter, cap=1, cfg={},
                       restart_ok=True)

    assert out["mirrored"] == ["a00-mir"], out
    assert out["marked"] == [] and out["still"] == [] and out["died"] == [], out
    m = json.loads((iter_dir / "manifest.json").read_text())
    e = m["agents"][0]
    assert e["status"] == "done" and e["finished_at"] == 7, e
    assert adapter.calls == [], "a terminal record must never be restarted"


# --- hypothesis:l4-branches-follow-the-season-grammar clause (5) ---
# dispatch's integration branch for the stale-base guard must resolve a
# spawner on a canonical TOWN post/loop branch to that TOWN's main via the
# grammar module's merge_target -- the exact-string town reverse-lookup
# matches no ladder value for a canonical loop/post spelling, so the old
# code fell back to the CORE main instead.


def test_current_town_branch_prefers_merge_target_for_loop(tmp_path):
    # A spawner on a canonical town loop branch: merge_target runs BEFORE the
    # town reverse-lookup (which would return None for this exact string), so
    # the returned integration is the TOWN main, not a core main.
    repo = _git_repo_on_branch(tmp_path, "season2/web-app-suite/season1/loops/xx-yy")
    # nodes_dir is pointless here: a post/loop branch resolves via merge_target
    # without ever consulting the ladder reverse-lookup.
    assert dispatch._current_town_branch(repo, tmp_path / "scratch") == \
        "season2/web-app-suite/season1/main"


def _git_repo_on_branch(tmp_path: Path, branch: str) -> Path:
    repo = tmp_path / "main"
    repo.mkdir(parents=True)
    subprocess.run(["git", "-C", str(repo), "init", "-b", branch],
                   check=True, capture_output=True)
    for cfg in ("user.email", "user.name"):
        subprocess.run(["git", "-C", str(repo), "config", cfg, "t"],
                       check=True, capture_output=True)
    (repo / "README").write_text("x")
    subprocess.run(["git", "-C", str(repo), "add", "-A"], check=True,
                   capture_output=True)
    subprocess.run(["git", "-C", str(repo), "commit", "-m", "init"],
                   check=True, capture_output=True)
    return repo


# --- hypothesis:l4-a-suspend-killed-round-comes-home-stalled-with-a-dead-pid ---
# ADMISSION under test THROUGH `_reap_pass` (not just `_reap_one`): a `stalled`
# record whose pid is provably gone is resolved by the same rules as a dead
# `running` record (node complete / branch advanced -> done-unreported,
# otherwise -> failed with the stall named), and is NEVER restarted. A
# `stalled` record with a LIVE pid stays stalled (mirror-only, not reaped).


def _stall_pass(tmp_path, monkeypatch, rec_status="stalled", agent_pid=999,
                node_complete=False, branch_committed=False, alive_pid=None,
                restart_ok=True):
    import json
    d = _load_dispatch()
    graph = _reap_project(tmp_path)
    iter_dir = graph / "sessions" / "iter-stall"
    (iter_dir / "a00-stl").mkdir(parents=True)
    (iter_dir / "manifest.json").write_text(json.dumps(
        {"agents": [{"id": "a00-stl", "status": "running"}]}))
    (iter_dir / "a00-stl" / "agent.json").write_text(json.dumps(
        {"id": "a00-stl", "status": rec_status, "pid": agent_pid,
         "node_id": "hypothesis:h-stall"}))
    import completion
    monkeypatch.setattr(completion, "is_complete",
                        lambda root, nid: node_complete)
    monkeypatch.setattr(d, "_branch_has_done_commit",
                        lambda root, rec, aid: branch_committed)
    monkeypatch.setattr(d, "stall_detect",
                        type("NS", (), {"record_stalled_in_iteration":
                                        lambda *a, **k: None})())
    if alive_pid is not None:
        adapter = type("Live", (_FakeAdapter,),
                       {"is_alive": lambda self, p: p == alive_pid})(pid=111)
    else:
        adapter = _FakeAdapter(pid=111)
    out = d._reap_pass(graph, iter_dir, adapter, cap=1, cfg={},
                       restart_ok=restart_ok)
    rec = json.loads((iter_dir / "a00-stl" / "agent.json").read_text())
    return d, out, rec, adapter


def test_stalled_dead_pid_complete_node_resolves_done_unreported(tmp_path, monkeypatch):
    """A suspend-killed round whose pid is gone but whose node is complete
    resolves done-unreported, exactly like a dead `running` record, and is
    never restarted."""
    d, out, rec, adapter = _stall_pass(tmp_path, monkeypatch,
                                       node_complete=True)
    assert rec["status"] == "done-unreported", rec
    assert "complete" in rec["fail_reason"], rec
    assert adapter.calls == [], "a stalled record must never be restarted"


def test_stalled_dead_pid_branch_advanced_resolves_done_unreported(tmp_path, monkeypatch):
    """The parent's completion signal — a commit on its branch — resolves a
    stalled+dead-pid record done-unreported, never restarted."""
    d, out, rec, adapter = _stall_pass(tmp_path, monkeypatch,
                                       branch_committed=True)
    assert rec["status"] == "done-unreported", rec
    assert adapter.calls == [], "a stalled record must never be restarted"


def test_stalled_dead_pid_incomplete_node_fails_named_never_restarted(tmp_path, monkeypatch):
    """No completion signal and no branch advance -> `failed` with the stall
    named, and NEVER a respawn."""
    d, out, rec, adapter = _stall_pass(tmp_path, monkeypatch)
    assert rec["status"] == "failed", rec
    assert "stalled" in rec["fail_reason"], rec
    assert adapter.calls == [], "a stalled record must never be restarted"


def test_stalled_alive_pid_stays_stalled_not_reaped(tmp_path, monkeypatch):
    """A `stalled` record whose pid is still alive is NOT admitted to the reap
    path — it stays stalled, is not mirrored-as-reaped, and never restarts."""
    d, out, rec, adapter = _stall_pass(tmp_path, monkeypatch, alive_pid=999)
    assert rec["status"] == "stalled", rec
    assert out["marked"] == [], out
    assert adapter.calls == [], "a live stalled record must never be reaped"


# --- hypothesis:l4-the-reaper-tolerates-a-null-pid… — the ONE pid reader ---

def test_rec_pid_tolerates_null_missing_and_non_int():
    """`int(rec.get("pid", 0))` raised TypeError on a committed record whose
    pid was null or a non-int, taking the whole reap pass down. `_rec_pid`
    reads every such shape as 0 = unknown."""
    d = _load_dispatch()
    assert d._rec_pid({"pid": None}) == 0
    assert d._rec_pid({}) == 0
    assert d._rec_pid({"pid": "abc"}) == 0
    assert d._rec_pid({"pid": ""}) == 0
    assert d._rec_pid({"pid": 4242}) == 4242
    assert d._rec_pid({"pid": "4242"}) == 4242


def test_is_death_predicate_covers_stalled_and_dead_running():
    """The ONE death predicate: both terminal resolutions that lose a pid are
    deaths, and a mirror-only resolution is not. This is what the `died`
    membership is driven off instead of a `fail_reason` string match."""
    d = _load_dispatch()
    assert d._is_death({"status": "failed", "death": {"class": "died-no-work"}})
    assert d._is_death({"status": "failed", "death": {"class": "died-after-work"}})
    assert not d._is_death({"status": "failed"})            # no death class
    assert not d._is_death({"status": "done-unreported",
                            "fail_reason": "pid 1 disappeared, but ... complete"})
    assert not d._is_death({"status": "running"})


def test_stalled_dead_in_service_lane_lands_in_died(tmp_path, monkeypatch):
    """A stalled-dead record reaped in the SERVICE lane (`restart_ok=False`)
    must surface under `died` — that is what makes the watcher dm it and log
    the reaper line. The old string-match on `fail_reason` never matched the
    `stalled; …` reason, so `died` stayed empty."""
    d, out, rec, adapter = _stall_pass(tmp_path, monkeypatch,
                                       restart_ok=False)
    assert rec["status"] == "failed", rec
    assert "death" in rec, "the stalled-dead record must carry the death class"
    assert out["died"] == ["a00-stl"], out
    assert adapter.calls == [], "a stalled record must never be restarted"


def test_orders_copy_is_per_agent_and_written_after_the_last_refusal_gate():
    """goal:g15.25 SM.28 claim (4). Measured pre-fix: the orders copy was the
    ONE path `<iter>/orders.md`, written ABOVE the kid-ceiling and key/account
    floor gates -- so two parent dispatches into one iter dir overwrote each
    other's file, and a round refused after that point left `orders.md` with
    no `manifest.json` beside it. The copy must be keyed by the AGENT ID the
    manifest record is keyed by (`orders.<agent>.md`, never the sender token
    `AGI_ORDERS_FROM`, which two parents can share) and its write must sit
    INSIDE the slot loop, below every per-slot refusal gate (budget lease,
    zoom render, harness/model, mint) and above Popen. Structural: the write
    is inline in `main()`, so the source position is the seam that proves
    it."""
    import ast
    src = (BIN / "dispatch.py").read_text()
    tree = ast.parse(src)
    writes = [
        n for n in ast.walk(tree)
        if isinstance(n, ast.Call)
        and getattr(n.func, "attr", "") == "write_text"
        and n.args
        and isinstance(n.args[0], ast.Name)
        and n.args[0].id == "_orders_text"
    ]
    assert len(writes) == 1, "exactly one orders copy write expected"
    # per-agent: the target is `_orders_file`, never a bare literal path.
    fn = writes[0].func
    assert isinstance(fn.value, ast.Name) and fn.value.id == "_orders_file"
    # keyed template, not a shared constant: no bare `orders.md` literal may
    # survive, and the token is the agent id the manifest record carries.
    keyed = [n for n in ast.walk(tree)
             if isinstance(n, ast.JoinedStr)
             and any(isinstance(v, ast.Constant)
                     and "orders." in str(v.value) for v in n.values)
             and "agent_id" in ast.unparse(n)]
    assert keyed, "the copy path must be the `orders.<agent_id>.md` template"
    assert "\"orders.md\"" not in src, (
        "a single shared `orders.md` is the two-parents-collide defect")
    # after the last whole-dispatch refusal gate ...
    gate = next(n for n in ast.walk(tree)
                if isinstance(n, ast.Call)
                and getattr(n.func, "attr", "") == "check_account_floor")
    assert writes[0].lineno > gate.lineno, (
        "the orders copy must be written after the last whole-dispatch "
        "refusal gate or a refused round leaves an orphan file")
    # ... and inside the slot loop: after the budget lease is taken, before
    # Popen. A write above the per-slot gates is what orphaned the file when
    # a slot was refused (measured: zoom-gate refusal left orders.SAME.md).
    lease = min((n for n in ast.walk(tree)
                 if isinstance(n, ast.Call)
                 and getattr(n.func, "attr", "") == "acquire"),
                key=lambda n: n.lineno)
    popen = next(n for n in ast.walk(tree)
                 if isinstance(n, ast.Call)
                 and getattr(n.func, "attr", "") == "Popen")
    assert lease.lineno < writes[0].lineno < popen.lineno, (
        "the orders copy belongs inside the slot loop, below the per-slot "
        "refusal gates and above Popen")


def test_two_parents_keep_separate_orders_copies_in_one_iter_dir(
        tmp_path, monkeypatch):
    """goal:g15.25 SM.28 claim (4), KEYING half. Measured pre-fix: the copy
    was keyed by the sender (`AGI_ORDERS_FROM`), which two parents sharing a
    `--from` (or both defaulting to "unspecified") collide on, and it was
    written BEFORE the agent id existed. Live path, faked only at the process
    boundary (adapter + Popen + zoom): two parent dispatches into ONE iter dir
    must leave TWO files, each named for the agent id its manifest record is
    keyed by, and each record's `orders.path` must name its own file."""
    import json as _json

    graph = tmp_path / ".agi"
    (graph / "nodes" / ".geometry").mkdir(parents=True)
    (graph / "config.json").write_text(_json.dumps({
        "harnesses": {"claude-code": {
            "adapter": "claude_code",
            "models": {"kid": "claude-sonnet-5", "parent": "claude-opus-5"},
            "allowed_models": ["claude-sonnet-5", "claude-opus-5"]}},
    }))
    (graph / "nodes" / ".geometry" / "ladder.md").write_text(
        "---\ncurrent_season: 2\nroles:\n"
        '  - {"tier": 3, "role": "parent", "harness": "claude-code", '
        '"model": "claude-opus-5", "effort": "max", "settings": "ultracode"}\n'
        "---\n\nbody\n")

    class _Proc:
        pid = 4242

        def poll(self):  # a child that never exits: outlives the startup grace
            return None

    class _Adapter:
        def build_command(self, **kw):
            return [sys.executable, "-c", "pass"]

        def child_env(self, **kw):
            return {}

        def needs_credential(self, *a, **k):
            return False

    class _Run:
        returncode = 0
        stdout = "ctx\n"
        stderr = ""

    monkeypatch.setattr(dispatch.adapters, "load", lambda name: _Adapter())
    monkeypatch.setattr(dispatch.subprocess, "Popen", lambda *a, **k: _Proc())
    monkeypatch.setattr(dispatch.subprocess, "run", lambda *a, **k: _Run())
    # the startup-grace poll's sleep seam: never sleep for real in a test
    monkeypatch.setattr(dispatch, "_GRACE_SLEEP", lambda s: None)

    for from_token in ("p1", "p2"):
        orders = tmp_path / f"orders-{from_token}.md"
        orders.write_text(f"SCOPE: parent {from_token}\n")
        monkeypatch.setattr(sys, "argv", [
            str(BIN / "dispatch.py"), str(tmp_path), "1",
            "--harness", "claude-code", "--tier", "parent",
            "--target", "hypothesis:x", "--orders", str(orders),
            "--from", "SAME",  # both parents share the sender token
            "--detach"])
        assert dispatch.main() == 0

    iter_dir = graph / "sessions" / "iter-001"
    manifest = _json.loads((iter_dir / "manifest.json").read_text())
    recs = [a for a in manifest["agents"] if a.get("orders")]
    assert len(recs) == 2, manifest
    paths = [Path(r["orders"]["path"]) for r in recs]
    assert len({str(p) for p in paths}) == 2, (
        f"two parents into one iter dir collided on {paths}")
    assert not (iter_dir / "orders.SAME.md").exists(), (
        "the sender token must never key the copy")
    for rec, path in zip(recs, paths):
        assert path.name == f"orders.{rec['id']}.md", (rec["id"], path)
        assert path.is_file(), path
    assert {p.read_text() for p in paths} == {
        "SCOPE: parent p1\n", "SCOPE: parent p2\n"}


# --- hypothesis:l4-dispatch-takes-a-per-round-cap-and-refuses-when-cap-
# exceeds-pool-headroom — the `--cap` flag on the REAL spawn path.
#
# Three conjuncts, each driven through `dispatch.main()` with the network
# stubbed (provisioning.mint / credit_balance / list_all_keys and
# subprocess.Popen), so the mint call itself is observed rather than a helper:
#   (a) `--cap 2.00` -> mint(limit_usd=2.00) and the spawn line reports it;
#   (b) no flag    -> mint(limit_usd=<configured 1.5>), byte-identical path;
#   (c) cap over pool-minus-floor-minus-live-caps -> exit 1, stderr names
#       pool/floor/live, and NO mint happened.

def _cap_project(tmp_path, parallel=1):
    """A scratch openrouter project whose standing per-spawn cap is 1.5 and
    whose account floor is 1.0."""
    import json
    graph = tmp_path / ".agi"
    (graph / "nodes" / ".geometry").mkdir(parents=True)
    (graph / "nodes" / "hypothesis").mkdir(parents=True)
    (graph / "nodes" / "goal").mkdir(parents=True)
    (graph / "config.json").write_text(json.dumps({
        "harnesses": {"pi": {"adapter": "pi", "provider": "openrouter",
                             "models": {"kid": "deepseek/deepseek-v4"}}},
        "spawn": {"harness": "pi", "parallel": parallel, "max_live": 25,
                  "credential": {"per_spawn_limit_usd": 1.5,
                                 "ttl_minutes": 180}},
        "provisioning": {"min_account_remaining_usd": 1.0},
        "agent_dispatch": {"inline_reaper": False},
    }))
    (graph / "nodes" / ".geometry" / "ladder.md").write_text(
        "---\ncurrent_season: 2\nroles:\n  - {tier: 0, role: kid, "
        "harness: pi, model: deepseek/deepseek-v4}\n---\nbody")
    (graph / "nodes" / ".geometry" / "secrets.md").write_text(
        "---\nenv_file: /tmp/definitely-not-a-real-secrets-file-zzz\n---\n")
    (graph / "nodes" / "goal" / "g15.md").write_text(
        "---\nid: goal:g15\ntype: goal\n---\nbody\n")
    (graph / "nodes" / "hypothesis" / "x.md").write_text(
        "---\nid: hypothesis:x\ntype: hypothesis\nparents:\n  - goal:g15\n"
        "---\nbody\n")
    return tmp_path


def _run_cap_dispatch(tmp_path, monkeypatch, *extra, balance=(100.0, 0.0, 100.0),
                      keys=(), parallel=1, real_floor=False):
    """Drive dispatch.main() for one openrouter kid slot with the network and
    the child process stubbed. Returns (exit_code, [mint kwargs], captured)."""
    import json
    import os
    import provisioning
    import sys as _sys
    project = _cap_project(tmp_path, parallel=parallel)
    mint_calls: list = []

    class _Minted:
        secret = "sk-or-v1-x"
        key_hash = "h"
        name = "agi-iter1-kid-X"
        expires_at = "Z"

        def __init__(self, limit):
            self.limit_usd = limit

    def _fake_mint(**kw):
        mint_calls.append(kw)
        return _Minted(kw["limit_usd"])

    monkeypatch.setattr(provisioning, "available", lambda root=None: True)
    monkeypatch.setattr(provisioning, "mint", _fake_mint)
    monkeypatch.setattr(provisioning, "check_runtime_key_usable",
                        lambda cfg, root=None: (True, None))
    if not real_floor:
        monkeypatch.setattr(provisioning, "check_key_floor",
                            lambda cfg, root=None, iter_n=None: (True, None))
    monkeypatch.setattr(provisioning, "check_account_floor",
                        lambda cfg, root=None: (True, None))
    monkeypatch.setattr(provisioning, "credit_balance",
                        lambda root=None: balance)
    monkeypatch.setattr(provisioning, "list_all_keys",
                        lambda root=None: list(keys))

    real_popen = subprocess.Popen

    class _StubProc:
        pid = 7777

        def poll(self):
            return None

        def wait(self, timeout=None):
            return 0

        def __enter__(self):
            return self

        def __exit__(self, *a):
            return False

    def _patched(argv, **kw):
        if (kw.get("env") or {}).get("AGI_AGENT_ID"):
            return _StubProc()
        return real_popen(argv, **kw)

    monkeypatch.setattr(subprocess, "Popen", _patched)
    # the startup-grace poll's sleep seam (dispatch.py:97-102): a stub child
    # that never exits (poll() -> None) otherwise sleeps the real 20 s grace
    # on every cap test that gets as far as spawning. Same seam as 1be791764.
    monkeypatch.setattr(dispatch, "_GRACE_SLEEP", lambda s: None)
    for k in ("AGI_TREE_PROJECT_ROOT", "AGI_PROJECT_ROOT", "AGI_AGENT_ID",
              "AGI_ACTOR"):
        monkeypatch.delenv(k, raising=False)
    monkeypatch.setattr(_sys, "argv", [
        str(BIN / "dispatch.py"), str(project), "1", "--level", "small",
        "--harness", "pi", "--tier", "kid", "--target", "hypothesis:x",
        *extra])
    code = dispatch.main()
    return code, mint_calls, project


def test_cap_flag_mints_at_exactly_that_limit(tmp_path, monkeypatch, capsys):
    """(a) `--cap 2.00` overrides the configured 1.5 and the spawn line reports
    the minted key's cap, so the round's real spend bound is the flag."""
    code, mints, _p = _run_cap_dispatch(tmp_path, monkeypatch, "--cap", "2.00")
    out = capsys.readouterr().out
    assert code == 0
    assert [m["limit_usd"] for m in mints] == [2.00]
    assert "cap=$2.0" in out


def test_no_cap_flag_keeps_the_configured_standing_limit(tmp_path, monkeypatch,
                                                         capsys):
    """(b) no flag -> the standing `spawn.credential.per_spawn_limit_usd`
    applies unchanged, and no headroom call is made."""
    code, mints, _p = _run_cap_dispatch(tmp_path, monkeypatch)
    out = capsys.readouterr().out
    assert code == 0
    assert [m["limit_usd"] for m in mints] == [1.5]
    assert "cap=$1.5" in out


def test_cap_over_pool_headroom_is_refused_by_name_and_mints_nothing(
        tmp_path, monkeypatch, capsys):
    """(c) pool 6.00 - floor 1.00 - live 3.50 = 1.50 headroom; a 5.00 cap is
    REFUSED, naming all three numbers, exit 1, and no mint happens."""
    code, mints, _p = _run_cap_dispatch(
        tmp_path, monkeypatch, "--cap", "5.00",
        balance=(10.0, 4.0, 6.0),
        keys=[{"name": "agi-iter1-kid-a", "limit": 2.0},
              {"name": "human-key", "limit": 99.0},
              {"name": "agi-iter1-parent-b", "limit": 1.5}])
    err = capsys.readouterr().err
    assert code == 1
    assert mints == [], "a refused cap must never mint"
    assert "round cap $5.00 exceeds pool headroom $1.50" in err, err
    assert "pool $6.00" in err and "floor $1.00" in err and "live $3.50" in err
    # item 15 (built by a00-4a19ce42): live is limit minus usage on live keys.
    assert "live counts each un-expired agi- key's limit minus usage" in err, err


def test_cap_prices_every_slot_and_names_the_multiplier(
        tmp_path, monkeypatch, capsys):
    """item 13: the slot loop mints ONE key per slot, so at spawn.parallel=3
    a 5.00 cap is priced 15.00 -- it fits once but not three times, and the
    refusal names the multiplier rather than leaving a $10.00 phantom."""
    code, mints, _p = _run_cap_dispatch(
        tmp_path, monkeypatch, "--cap", "5.00", parallel=3,
        balance=(10.0, 0.0, 10.0))
    err = capsys.readouterr().err
    assert code == 1
    assert mints == [], "a refused cap must never mint"
    assert ("round cap $5.00 x 3 slots = $15.00 exceeds pool headroom $9.00"
            in err), err


def test_cap_fail_open_is_a_named_notice_never_silence(
        tmp_path, monkeypatch, capsys):
    """item 12: an unreadable account is a fail-open WITH a marker -- the
    round proceeds but a `notice:` line names that the cap was not measured,
    the same string cap_headroom returned."""
    code, mints, _p = _run_cap_dispatch(
        tmp_path, monkeypatch, "--cap", "5.00", balance=None)
    err = capsys.readouterr().err
    assert code == 0, f"a fail-open must still mint, got {code}: {err}"
    assert len(mints) == 1, mints
    assert "notice: cap not measured" in err, err


def test_non_positive_cap_is_refused_by_name_before_any_mint(
        tmp_path, monkeypatch, capsys):
    """item 14: `--cap 0` and `--cap -1` always fit the comparison, so they
    must never reach it -- each exits non-zero naming the value and no key is
    minted."""
    for bad in ("0", "-1"):
        sub = tmp_path / ("cap_zero" if bad == "0" else "cap_neg")
        code, mints, _p = _run_cap_dispatch(sub, monkeypatch, "--cap", bad)
        err = capsys.readouterr().err
        assert code == 1, (bad, code)
        assert mints == [], (bad, "a refused cap must never mint")
        assert f"ERR: --cap must be > 0, got {bad}" in err, (bad, err)


def test_l4p6_composition_real_check_key_floor_through_dispatch(
        tmp_path, monkeypatch, capsys):
    """hypothesis:l4-pi-review-stages-... item (6) COMPOSITION — the wiring
    and the mechanism on ONE branch, driven through the dispatch pre-flight
    with the REAL `provisioning.check_key_floor` (NOT a signature-compatible
    stub). A wire passing iter_n to a real function that cannot accept it
    raises TypeError; a wire that does not thread iter_n lets ANOTHER
    iteration's drained key (a proxy for this spawn's FRESH mint) refuse the
    spawn — the TM.20 freeze. FALSIFIER: the dispatch call site calls
    check_key_floor without iter_n, or the mechanism never landed and the
    call breaks."""
    # CASE A — another iteration's drained below-floor key (cap 5.0 makes
    # remaining 0.90 < floor 1.0, and cap > floor so it is NOT a sub-floor
    # skip) must NOT refuse this spawn: threading iter_n=1 skips the other-
    # iter proxy key and the round mints its own fresh key.
    other = [{"name": "agi-iter9-kid-a00", "limit": 5.0, "usage": 4.1}]
    code, mints, _p = _run_cap_dispatch(
        tmp_path, monkeypatch, keys=other, real_floor=True)
    err = capsys.readouterr().err
    assert code == 0, \
        f"another iter's drained key refused this spawn: {err}"
    assert len(mints) == 1, "the spawn must mint its own fresh key"

    # CASE B — the SAME iteration's drained key (iter 1 == this dispatch's
    # iter) still refuses, and names the owning iteration.
    same = [{"name": "agi-iter1-kid-a00", "limit": 5.0, "usage": 4.1}]
    code2, mints2, _p2 = _run_cap_dispatch(
        tmp_path / "same", monkeypatch, keys=same, real_floor=True)
    err2 = capsys.readouterr().err
    assert code2 == 1, f"same-iteration drain did not refuse: {err2}"
    assert mints2 == [], "a refused pre-flight must never reach a spawn"
    assert "iteration 1" in err2, \
        f"refusal must name the owning iter: {err2}"
