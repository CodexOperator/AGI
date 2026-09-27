"""hypothesis:a-rounds-own-path-set-never-fails-open (DH.514).

Two routes into a round's own-path set used to FAIL OPEN in silence:

  (1) the `--node-id` SEED guard short-circuited on `agent_id` being present,
      so a round (or a direct call / a fixture) with NO agent id in hand ran
      no guard at all -- a foreign round-committable node was swept into the
      round's done commit with empty stderr;
  (2) `--owns` was a THIRD kid-supplied route: it is inside `asked`, so it
      widened the set on the type gate ALONE -- the agent-id-in-basename rule
      that covers `--node-id` was never applied to it. It is now bound to the
      dispatch-time `named` set; anything else is refused BY NAME.
"""
import json
import os

from pathlib import Path

import pytest

#: `AGI_CLI_PY` as the PROCESS saw it at COLLECTION time. The suite's strip
#: (extensions/agi/conftest.py:54 `_strip_agi_env`) is a SESSION fixture, so it
#: runs at first test setup -- AFTER this import. Module import is therefore the
#: only moment the var is still readable from inside `extensions/agi/tests`, and
#: the only honest tell for whether a RED proof here was one at all (DH.604).
_CLI_PY_AT_IMPORT = os.environ.get("AGI_CLI_PY")


def _cli_py():
    """The cli.py under test, or the copy `AGI_CLI_PY` names. A RED proof
    must NOT be run from inside `extensions/agi/tests` -- that conftest strips
    every `AGI_*` key session-wide, so the var is invisible and the LIVE
    cli.py loads whatever you name. DH.604 CLOSED the trap: the fixture below
    turns that silence into a NAMED skip. The working route is a copy of this
    file outside that tree, with PYTHONPATH=<engine>/bin (cli.py:29)."""
    return Path(os.environ.get("AGI_CLI_PY")
                or (Path(__file__).resolve().parents[1] / "bin" / "cli.py"))


@pytest.fixture(autouse=True)
def _agi_cli_py_seam_is_loud():
    """A set-but-stripped `AGI_CLI_PY` SKIPS, loudly, instead of falling
    through to the live cli.py: a green there would measure the live tree while
    the operator believed a copy was under test. Refusing to answer is the
    honest state, not a pass."""
    if _CLI_PY_AT_IMPORT and not os.environ.get("AGI_CLI_PY"):
        pytest.skip(
            "AGI_CLI_PY was set at collection and is gone now: "
            "extensions/agi/conftest.py:54 _strip_agi_env deleted every AGI_* "
            "key session-wide, so this run would silently test the LIVE "
            "cli.py. Run this file from a copy OUTSIDE extensions/agi/tests "
            f"(named copy: {Path(_CLI_PY_AT_IMPORT).name})")


def _load_module(name, filename):
    import importlib.util
    spec = importlib.util.spec_from_file_location(name, _cli_py().parent / filename)
    mod = importlib.util.module_from_spec(spec)
    spec.loader.exec_module(mod)
    return mod


def _load_cli():
    return _load_module("agi_cli_own", "cli.py")


def _graph(tmp_path, ids=(("hypothesis", "foreign"),
                          ("hypothesis", "tgt"),
                          ("hypothesis", "a-rounds-own-set"),
                          ("experiment", "a00-me-1"))):
    root = tmp_path / ".agi"
    (root / "context" / "schemas").mkdir(parents=True)
    (root / "config.json").write_text("{}")
    for sub, nid in ids:
        d = root / "nodes" / sub
        d.mkdir(parents=True, exist_ok=True)
        (d / f"{nid}.md").write_text(
            f"---\nid: {sub}:{nid}\ntype: {sub}\n---\n\nbody\n")
    return root


def test_absent_agent_id_refuses_the_seed_by_name(tmp_path, capsys):
    """Defect (1). No agent id in hand => NO silent fall-through: the seed is
    refused and the id is NAMED, so the round can tell "I refuse that" from
    "I never saw it"."""
    cli = _load_cli()
    root = _graph(tmp_path)
    capsys.readouterr()
    paths = cli._round_own_node_paths(
        root, root, "hypothesis:foreign", None, ["experiment:a00-me-1"])
    assert paths == {"nodes/experiment/a00-me-1.md"}, paths
    err = capsys.readouterr().err
    assert "hypothesis:foreign" in err and "refusing" in err, err


def test_absent_agent_id_still_lands_a_dispatch_named_id(tmp_path, capsys):
    """The refusal is narrow: an id DISPATCH named is the round's own whatever
    the agent id is -- the named set is the binding, not the basename."""
    cli = _load_cli()
    root = _graph(tmp_path)
    capsys.readouterr()
    paths = cli._round_own_node_paths(
        root, root, "hypothesis:a-rounds-own-set", None,
        ["hypothesis:a-rounds-own-set"])
    assert paths == {"nodes/hypothesis/a-rounds-own-set.md"}, paths
    assert capsys.readouterr().err == ""


def test_owns_is_bound_to_the_dispatch_named_set(tmp_path, capsys):
    """Defect (2). `--owns` is a kid-supplied route: an id dispatch did NOT
    name is refused by name, whatever its type and whatever the basename."""
    cli = _load_cli()
    root = _graph(tmp_path)
    capsys.readouterr()
    paths = cli._round_own_node_paths(
        root, root, None, ["hypothesis:foreign"], ["hypothesis:tgt"],
        agent_id="a00-me")
    assert paths == {"nodes/hypothesis/tgt.md"}, paths
    err = capsys.readouterr().err
    assert "hypothesis:foreign" in err and "refusing" in err, err
    # ...and the very same id DISPATCH named is the round's own -- still lands.
    capsys.readouterr()
    paths = cli._round_own_node_paths(
        root, root, None, ["hypothesis:foreign"],
        ["hypothesis:foreign", "hypothesis:tgt"], agent_id="a00-me")
    assert paths == {"nodes/hypothesis/foreign.md",
                     "nodes/hypothesis/tgt.md"}, paths
    assert capsys.readouterr().err == ""


def test_the_own_minted_scaffold_still_lands_with_its_agent_id(tmp_path,
                                                                capsys):
    """The three cases everyone fears stay GREEN: a kid's own minted scaffold
    (basename carries the agent id) lands, and so does a foreign seed."""
    cli = _load_cli()
    root = _graph(tmp_path)
    capsys.readouterr()
    paths = cli._round_own_node_paths(root, root, "experiment:a00-me-1", None,
                                      [], agent_id="a00-me")
    assert paths == {"nodes/experiment/a00-me-1.md"}, paths
    assert capsys.readouterr().err == ""
    capsys.readouterr()
    paths = cli._round_own_node_paths(
        root, root, "hypothesis:foreign", None, ["experiment:a00-me-1"],
        agent_id="a00-me")
    assert paths == {"nodes/experiment/a00-me-1.md"}, paths
    assert "hypothesis:foreign" in capsys.readouterr().err


def _load_locations():
    """The engine's locations.py, next to the cli.py under test -- the ONE
    place the iteration-dirname spelling lives (never re-spell a path)."""
    return _load_module("agi_loc_own", "locations.py")


def _spawn(root, agent, spawned_by, node_id, dispatch_node_id=None, iter_n=999):
    """A spawn record under the CANONICAL iteration dir for `iter_n`.

    `dispatch_node_id=""` writes the record PRODUCTION writes: the key is
    PRESENT, carrying `""` when there is no dispatch id. DH.632 reverted
    DH.617's `if dispatch_node_id:` guard, which made the key ABSENT -- a
    record shape no real seat's agent.json ever has, since production's own
    writer of the key is the `setdefault(..., rec.get("node_id") or "")` line
    in the `done` path, and a `setdefault` always leaves the key present. The
    ABSENT shape is the WEAKER fixture: `r.get()` reads `None` for it, so a
    cli.py that guards on `v is not None` sails through, and only a
    fallback-style mutant (`r.get("dispatch_node_id", r.get("node_id"))`) is
    caught. With the key PRESENT and `""` it refuses, so a `v is not None`
    mutant now fails the pin too -- the fixture measures the code it is a
    fixture for, in both directions. DH.604: the `sessions` segment is `locations.sessions_dir`'s to spell -- a
    hand-written `root / "sessions"` was a second copy that can drift, and a
    wrong `root` (repo root, not the `.agi` dir) reads as an empty set for the
    WRONG reason. Per-worktree `sessions_dir`, never `shared_sessions_dir`:
    iteration output is the worktree-local fork (locations.iteration_dir).
    DH.557: this used to write `sessions/iter-DH.999/`, which is not the
    dirname `locations.iteration_dirname` emits, and the callers called the
    helper with NO iteration in hand -- so the DH.552 bound (this round's own
    iter dir) read as an empty set for the WRONG reason: the fixture, not the
    bound. The bound itself is correct and stays; the fixture now puts the
    record where a real dispatch puts it, and passes the id.
    """
    loc = _load_locations()
    # DH.617: the whole dir spell is `locations.iteration_dir`'s -- the exact
    # expression production globs (cli.py `_round_spawned_node_ids`). The
    # hand-written `sessions_dir(root) / iteration_dirname(iter_n)` was a
    # second copy of a fact one module owns: it can drift from the glob and
    # then the fixture, not the bound, is what the pin measures.
    d = loc.iteration_dir(root, iter_n) / agent
    d.mkdir(parents=True, exist_ok=True)
    if dispatch_node_id is None:
        dispatch_node_id = node_id
    # DH.632: the key is ALWAYS present, "" when empty -- exactly what
    # production's `rec.setdefault("dispatch_node_id", rec.get("node_id") or
    # "")` leaves on a real seat's agent.json. Same drift class DH.617 fixed
    # for the DIR: a fixture whose spelling drifts from the code's means the
    # fixture, not the bound, is what the pin measures.
    rec = {"spawned_by_agent": spawned_by, "node_id": node_id,
           "dispatch_node_id": dispatch_node_id or ""}
    (d / "agent.json").write_text(json.dumps(rec) + "\n")
    return d


def test_only_dispatch_node_id_widens_the_set_never_the_node_id_line(tmp_path):
    """DH.552 bound leg 1, unpinned until now: `dispatch_node_id` ONLY -- a
    record carrying NONE contributes nothing, its `node_id` line is not a
    fallback, so a kid-writable id never leaks. Carrying one, it lands.
    DH.632: "carrying NONE" is production's SHAPE -- the key present with
    `""` -- not an absent key; see `_spawn`. A mutant that swaps the
    `isinstance(v, str) and ":" in v` guard for `v is not None` must FAIL
    this, which it cannot do against an absent-key fixture."""
    cli = _load_cli()
    root = _graph(tmp_path)
    kid = "hypothesis:kid-writable"
    _spawn(root, "a00-kid-3", "a00-me", kid, dispatch_node_id="")
    assert cli._round_spawned_node_ids(root, "a00-me", 999) == []
    _spawn(root, "a00-kid-3", "a00-me", kid)  # that leg is the ONLY way in
    assert cli._round_spawned_node_ids(root, "a00-me", 999) == [kid]


def test_owns_reaches_the_nodes_of_the_agents_this_round_spawned(tmp_path,
                                                                 capsys):
    """DH.514 correction. A PARENT round finishing with `done --owns <its kid's
    node id>` is the flow the commit exists for (one parent commit carries 4
    kid files), and binding `--owns` to the parent's OWN dispatch record
    alone refused it. The binding is the union: this round's own dispatch
    ids PLUS the ids of the agents this round spawned."""
    cli = _load_cli()
    root = _graph(tmp_path, ids=(("hypothesis", "tgt"),
                                 ("experiment", "a00-kid-1")))
    _spawn(root, "a00-kid-1", "a00-me", "experiment:a00-kid-1")
    assert cli._round_spawned_node_ids(root, "a00-me", 999) == [
        "experiment:a00-kid-1"]
    # the three refusals the bound buys, all still empty:
    assert cli._round_spawned_node_ids(root, "a00-somebody-else", 999) == []
    assert cli._round_spawned_node_ids(root, None, 999) == []
    assert cli._round_spawned_node_ids(root, "a00-me", None) == []
    # ...and a record of THIS round's spawn in ANOTHER iteration does not leak
    # in: a seat name is not a round id (the DH.552 seat-name leak).
    _spawn(root, "a00-kid-old", "a00-me", "experiment:a00-kid-old", iter_n=1)
    assert cli._round_spawned_node_ids(root, "a00-me", 999) == [
        "experiment:a00-kid-1"]
    named = cli._round_named_node_ids({"target": "hypothesis:tgt"}, None)
    named += cli._round_spawned_node_ids(root, "a00-me", 999)
    capsys.readouterr()
    paths = cli._round_own_node_paths(
        root, root, None, ["experiment:a00-kid-1"], named, agent_id="a00-me")
    assert paths == {"nodes/hypothesis/tgt.md",
                     "nodes/experiment/a00-kid-1.md"}, paths
    assert capsys.readouterr().err == ""


def test_owns_of_a_kid_another_agent_spawned_is_still_refused(tmp_path,
                                                              capsys):
    """The union is scoped to THIS round's spawns: a kid record another agent
    spawned never widens the set, so an id with no dispatch record on this
    round stays refused by name."""
    cli = _load_cli()
    root = _graph(tmp_path, ids=(("hypothesis", "tgt"),
                                 ("experiment", "a00-kid-2")))
    _spawn(root, "a00-kid-2", "a00-other-parent", "experiment:a00-kid-2")
    named = (cli._round_named_node_ids({"target": "hypothesis:tgt"}, None)
             + cli._round_spawned_node_ids(root, "a00-me", 999))
    capsys.readouterr()
    paths = cli._round_own_node_paths(
        root, root, None, ["experiment:a00-kid-2"], named, agent_id="a00-me")
    assert paths == {"nodes/hypothesis/tgt.md"}, paths
    err = capsys.readouterr().err
    assert "experiment:a00-kid-2" in err and "--owns is bound" in err, err


def test_a_refused_parent_is_named_for_the_parent_route(tmp_path, capsys):
    """DH.514: the `--owns` guard sat BEFORE the `--parent` guard, so a
    refused `--parent` id printed the `--owns` sentence and the `--parent
    never widens` print was dead code. Each id is named for the route it
    actually took."""
    cli = _load_cli()
    root = _graph(tmp_path, ids=(("hypothesis", "tgt"),
                                 ("hypothesis", "dp-parent")))
    capsys.readouterr()
    paths = cli._round_own_node_paths(
        root, root, None, None, ["hypothesis:tgt"],
        refused=["hypothesis:dp-parent"], agent_id="a00-me")
    assert paths == {"nodes/hypothesis/tgt.md"}, paths
    err = capsys.readouterr().err
    assert "a kid-supplied --parent never widens" in err, err
    assert "--owns is bound" not in err, err
