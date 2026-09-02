"""Tests for bin/dispatch.py's pi argument construction.

Narrow on purpose: `_build_pi_args` is the seam where a config key becomes a
real flag on a real subprocess, and until 2026-08-31 it read `agent_dispatch`
and then used none of it — every kid silently ran whatever `~/.pi/agent/
settings.json` said, while the config key that claims to pick the model picked
nothing. A defect that quiet deserves a test that is loud.
"""
from __future__ import annotations

import importlib.util
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
