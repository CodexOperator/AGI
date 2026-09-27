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


def _load_cli():
    """The engine's cli.py, or the copy `AGI_CLI_PY` names -- the RED proof on
    the base tip extracts one with `git show` and points this at it."""
    import importlib.util
    import os
    from pathlib import Path
    src = Path(os.environ.get("AGI_CLI_PY")
               or (Path(__file__).resolve().parents[1] / "bin" / "cli.py"))
    spec = importlib.util.spec_from_file_location("agi_cli_own", src)
    cli = importlib.util.module_from_spec(spec)
    spec.loader.exec_module(cli)
    return cli


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


def _spawn(root, agent, spawned_by, node_id, dispatch_node_id=None):
    d = root / "sessions" / "iter-DH.999" / agent
    d.mkdir(parents=True, exist_ok=True)
    (d / "agent.json").write_text(
        '{"spawned_by_agent": "%s", "node_id": "%s", "dispatch_node_id": '
        '"%s"}\n' % (spawned_by, node_id, dispatch_node_id or node_id))
    return d


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
    assert cli._round_spawned_node_ids(root, "a00-me") == ["experiment:a00-kid-1"]
    assert cli._round_spawned_node_ids(root, "a00-somebody-else") == []
    assert cli._round_spawned_node_ids(root, None) == []
    named = cli._round_named_node_ids({"target": "hypothesis:tgt"}, None)
    named += cli._round_spawned_node_ids(root, "a00-me")
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
             + cli._round_spawned_node_ids(root, "a00-me"))
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
