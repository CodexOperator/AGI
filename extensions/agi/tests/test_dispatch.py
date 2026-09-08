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
    assert args[0].endswith("pi")


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
    never collide; the slug tells a human which aim the branch carries."""
    assert (dispatch.loop_branch_name("hypothesis:l3w4-x", "a00-abc8", 2)
            == "loop/hypothesis-l3w4-x-a00-abc8@s2")
    # colon flattened, explore fallback, season stamped
    assert dispatch.loop_branch_name(None, "a00-x", 1) == "loop/explore-a00-x@s1"
    assert dispatch.loop_branch_name("mvp:g", "kid1", 3) == "loop/mvp-g-kid1@s3"


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
