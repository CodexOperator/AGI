

def _load_cli():
    import importlib.util
    from pathlib import Path
    bin_dir = Path(__file__).resolve().parents[1] / "bin"
    spec = importlib.util.spec_from_file_location("agi_cli", bin_dir / "cli.py")
    cli = importlib.util.module_from_spec(spec)
    spec.loader.exec_module(cli)
    return cli


def _broken_node(marker=True):
    """A node whose `---` block a kid's write tool mangled (L3.13): the block is
    no longer well-formed YAML, but the body -- anchored by the BODY:BEGIN
    comment the scaffold wrote -- survives intact below."""
    if marker:
        return (
            "---broken frontmatter:\n"
            "id: experiment:e1\n"
            "mint_id: 9f38d062aa\n"
            "<!-- BODY:BEGIN -->\n"
            "# experiment:e1\n\n"
            "The kid wrote this body.\n"
        )
    return (
        "---broken frontmatter:\n"
        "id: experiment:e1\n"
        "mint_id: 9f38d062aa\n"
        "no marker, so the mangled block runs into the body\n"
    )


# --------------------------------------------------------------------------
# hypothesis:l3-done-broken-frontmatter
# --------------------------------------------------------------------------

def test_ensure_frontmatter_repairs_a_broken_block_from_the_manifest(tmp_path):
    """A mangled `---` block + an intact body (the BODY:BEGIN marker survived)
    is rebuilt from the spawn manifest: ok=True, id/type/parents restored, the
    body preserved untouched, and identity (mint_id) salvaged rather than lost."""
    cli = _load_cli()
    node_file = tmp_path / "e1.md"
    node_file.write_text(_broken_node())
    ap = tmp_path / "agent.json"
    ap.write_text('{"node_id": "experiment:e1", "parent": "hypothesis:h1"}')

    ok, msg = cli._ensure_frontmatter(tmp_path, node_file, ap, "experiment:e1")
    assert ok
    assert "repaired" in msg

    text = node_file.read_text()
    assert text.startswith("---\n")
    assert "id: experiment:e1" in text
    assert "type: experiment" in text
    assert "parents:\n  - hypothesis:h1" in text
    # mint_id is identity -- salvaged, never regenerated (goal:s14).
    assert "mint_id: 9f38d062aa" in text
    # The body below the marker is byte-for-byte what the kid wrote.
    assert "The kid wrote this body." in text
    # And the repaired file now parses as valid frontmatter.
    ok2, fm, defect = cli._load_frontmatter(text)
    assert ok2, defect
    assert fm["id"] == "experiment:e1"


def test_ensure_frontmatter_leaves_already_valid_frontmatter_alone(tmp_path):
    cli = _load_cli()
    node_file = tmp_path / "e1.md"
    node_file.write_text(
        "---\nid: experiment:e1\ntype: experiment\nparents:\n- hypothesis:h1\n---\n\nbody\n")
    ok, msg = cli._ensure_frontmatter(tmp_path, node_file, tmp_path / "absent.json",
                                      "experiment:e1")
    assert ok
    assert msg == "frontmatter ok"
    # untouched bytes
    assert node_file.read_text().startswith("---\nid: experiment:e1")


def test_ensure_frontmatter_refuses_when_the_body_is_damaged(tmp_path):
    """Broken `---` block AND no body-start marker => no safe split boundary, so
    `done` must refuse rather than guess. Returns ok=False with the defect."""
    cli = _load_cli()
    node_file = tmp_path / "e1.md"
    node_file.write_text(_broken_node(marker=False))
    ok, msg = cli._ensure_frontmatter(tmp_path, node_file, tmp_path / "agent.json",
                                      "experiment:e1")
    assert not ok
    assert "BODY:BEGIN" in msg
    assert "cannot separate" in msg
    # untouched -- the mangled file is never rewritten on a refusal
    assert "broken frontmatter:" in node_file.read_text()


def test_ensure_frontmatter_repairs_a_closed_block_missing_parents(tmp_path):
    """A node whose `---` block closes cleanly but is missing a required field
    (here `parents`) has a provably intact body -- the close delimits it -- so
    it is repaired from the manifest WITHOUT needing the BODY:BEGIN marker. The
    parsed block is preserved as a whole, not flattened by line salvage."""
    cli = _load_cli()
    node_file = tmp_path / "e1.md"
    node_file.write_text(
        "---\nid: experiment:e1\ntype: experiment\n"
        "evidence_runs:\n  - experiment:run-a\n---\n\nran it twice\n")
    ap = tmp_path / "agent.json"
    ap.write_text('{"parent": "hypothesis:h1"}')
    ok, msg = cli._ensure_frontmatter(tmp_path, node_file, ap, "experiment:e1")
    assert ok
    assert "repaired" in msg
    text = node_file.read_text()
    assert "parents:\n  - hypothesis:h1" in text
    # parsed structure survived -- not flattened to a bare scalar by salvage
    assert "- experiment:run-a" in text
    assert "ran it twice" in text


def test_ensure_frontmatter_repairs_a_closed_block_missing_type(tmp_path):
    cli = _load_cli()
    node_file = tmp_path / "e1.md"
    node_file.write_text(
        "---\nid: experiment:e1\nparents:\n- hypothesis:h1\n---\n\nbody\n")
    ap = tmp_path / "agent.json"
    ap.write_text('{}')
    ok, msg = cli._ensure_frontmatter(tmp_path, node_file, ap, "experiment:e1")
    assert ok
    text = node_file.read_text()
    assert "type: experiment" in text


def _cmd_done_project(tmp_path):
    """A minimal project root + a broken experiment node, ready for cmd_done.
    Returns (graph_root, args)."""
    graph = tmp_path / ".agi"
    (graph / "nodes" / "experiment").mkdir(parents=True)
    (graph / "config.json").write_text("{}")
    (graph / "nodes" / "experiment" / "e1.md").write_text(_broken_node())
    # A valid backer experiment so `proved` resolves real evidence and is not
    # demoted by the H4 gate -- proving the verdict is unchanged.
    (graph / "nodes" / "experiment" / "backer.md").write_text(
        "---\nid: experiment:backer\ntype: experiment\nparents:\n- hypothesis:h1\n---\n\nbody\n")
    (graph / "sessions" / "iter-001" / "a00-x").mkdir(parents=True)
    (graph / "sessions" / "iter-001" / "a00-x" / "agent.json").write_text(
        '{"id": "a00-x", "node_id": "experiment:e1", '
        '"parent": "hypothesis:h1", "status": "running"}')
    _write_holder(graph, "001", "a00-x")
    import argparse
    args = argparse.Namespace(
        iter_n=1, agent_id="a00-x", verdict="proved", confidence=0.9,
        node_id="experiment:e1", parent="hypothesis:h1", notes="",
        next_edge=None, evidence_runs=["experiment:backer"],
        no_evidence_gate=False, owns=None, no_spawn_gate=False,
    )
    return graph, args


def _write_holder(graph, iter_n, agent_id):
    """A bookkept round: the iter manifest carries the agent's row, so
    `_alarm_dispatcher_on_done` finds a holder and returns None (rc 0) -- a
    legitimate round that alarms. A fixture WITHOUT this is a silent-dm round
    and, since SM.67 C2, correctly makes cmd_done return rc 1. Returns the
    manifest path."""
    import json as _json
    d = graph / "sessions" / f"iter-{iter_n}"
    d.mkdir(parents=True, exist_ok=True)
    mpath = d / "manifest.json"
    if not mpath.exists():
        mpath.write_text(_json.dumps({"agents": [{"id": agent_id,
                                                    "status": "running"}]},
                                     indent=2))
    return mpath


def test_done_adopts_a_node_written_outside_node_writer(tmp_path, monkeypatch):
    """hypothesis:l3-node-without-mint-id — `cli.py done` mints a first
    `mint_id` on a node a kid wrote with its own file tool (valid frontmatter,
    but no mint_id), so grid.py can version it -- keyed from the spawn
    manifest, exactly like the frontmatter repair. The verdict is still
    recorded."""
    cli = _load_cli()
    graph = tmp_path / ".agi"
    graph.mkdir(parents=True)
    (graph / "config.json").write_text("{}")
    (graph / "nodes" / "experiment").mkdir(parents=True)
    # kid-written node: valid frontmatter, real content, NO mint_id.
    (graph / "nodes" / "experiment" / "e1.md").write_text(
        "---\nid: experiment:e1\ntype: experiment\n"
        "parents:\n- hypothesis:h1\n---\n\n# experiment:e1\n\n"
        "The kid wrote this body directly.\n")
    # a valid backer experiment so `proved` resolves real evidence
    (graph / "nodes" / "experiment" / "backer.md").write_text(
        "---\nid: experiment:backer\ntype: experiment\nparents:\n"
        "- hypothesis:h1\n---\n\nbody\n")
    (graph / "sessions" / "iter-001" / "a00-x").mkdir(parents=True)
    (graph / "sessions" / "iter-001" / "a00-x" / "agent.json").write_text(
        '{"id": "a00-x", "node_id": "experiment:e1", '
        '"parent": "hypothesis:h1", "status": "running"}')
    _write_holder(graph, "001", "a00-x")
    import argparse
    args = argparse.Namespace(
        iter_n=1, agent_id="a00-x", verdict="proved", confidence=0.9,
        node_id="experiment:e1", parent="hypothesis:h1", notes="",
        next_edge=None, evidence_runs=["experiment:backer"],
        no_evidence_gate=False, owns=None, no_spawn_gate=False,
    )
    monkeypatch.setattr(cli, "_find_root", lambda: graph)

    rc = cli.cmd_done(args)
    assert rc == 0

    text = (graph / "nodes" / "experiment" / "e1.md").read_text()
    import re
    assert re.search(r"^mint_id:\s*\S+", text, re.M) is not None
    assert "verdict: proved" in text
    # the kid's body survived the adoption
    assert "The kid wrote this body directly." in text


def test_done_repairs_broken_frontmatter_and_records_the_verdict_unchanged(
        tmp_path, monkeypatch):
    """The crux of L3.13: `done` repairs the frontmatter from the manifest and
    proceeds -- the verdict is recorded exactly as requested (no demotion, no
    `demoted_from`), because the repair happened before the evidence gate ran."""
    cli = _load_cli()
    graph, args = _cmd_done_project(tmp_path)
    monkeypatch.setattr(cli, "_find_root", lambda: graph)

    rc = cli.cmd_done(args)
    assert rc == 0

    text = (graph / "nodes" / "experiment" / "e1.md").read_text()
    assert "verdict: proved" in text
    assert "confidence: 0.9" in text
    # repaired frontmatter carried the required identity
    assert text.startswith("---\nid: experiment:e1")
    # the kid's body survived the repair
    assert "The kid wrote this body." in text


def test_done_refuses_body_damage_and_stamps_no_demotion(tmp_path, monkeypatch):
    """A node damaged beyond the repair boundary is refused with a non-zero
    exit BEFORE the evidence gate -- so no demotion, no `demoted_from`, and no
    verdict is recorded. A parse failure is not missing evidence and must not
    be demoted as if it were."""
    cli = _load_cli()
    graph, args = _cmd_done_project(tmp_path)
    # unrepairable: no body-start marker survived
    (graph / "nodes" / "experiment" / "e1.md").write_text(_broken_node(marker=False))
    monkeypatch.setattr(cli, "_find_root", lambda: graph)

    rc = cli.cmd_done(args)
    assert rc != 0
    text = (graph / "nodes" / "experiment" / "e1.md").read_text()
    assert "verdict" not in text
    assert "demoted_from" not in text
    assert "broken frontmatter:" in text  # untouched


def test_confidence_percent_is_normalized_not_stored_raw():
    """A kid holding both scales at once passed the lean's integer percent to
    --confidence too, storing `confidence: 65.0` on a 0..1 field (2026-09-01).
    Mirror of the `:0.6` verdict bug found the session before."""
    import importlib.util
    import pytest
    from pathlib import Path
    bin_dir = Path(__file__).resolve().parents[1] / "bin"
    spec = importlib.util.spec_from_file_location("agi_cli", bin_dir / "cli.py")
    cli = importlib.util.module_from_spec(spec)
    spec.loader.exec_module(cli)

    assert cli._normalize_confidence(0.65) == 0.65
    assert cli._normalize_confidence(0.0) == 0.0
    assert cli._normalize_confidence(1.0) == 1.0
    assert cli._normalize_confidence(65) == 0.65
    assert cli._normalize_confidence(100) == 1.0
    for bad in (-1, 101, 1000):
        with pytest.raises(ValueError):
            cli._normalize_confidence(bad)


# --------------------------------------------------------------------------
# hypothesis:l3w4-branch-parent-commits — parent owns the worktree commit
# --------------------------------------------------------------------------

def _ggit(tmp, *args):
    import subprocess
    return subprocess.run(["git", "-C", str(tmp), *args],
                          capture_output=True, text=True)


def _gitc(tmp, msg):
    (tmp / "file.txt").write_text("x\n")
    _ggit(tmp, "add", "-A")
    return _ggit(tmp, "-c", "user.email=t@t", "-c", "user.name=t",
                 "commit", "-qm", msg)


def test_done_auto_commits_parent_worktree(tmp_path, monkeypatch):
    """The remaining half of hypothesis:l3w4-branch-parent-commits. A
    `--branch` parent accepts its kid's node while resident in a linked
    worktree (nothing else commits there), so `cli.py done` must own the
    commit: the worktree's uncommitted node write lands at base+1 with a
    clean tree, and season.py merge-up against that branch now succeeds
    instead of REFUSING a zero-ahead empty branch."""
    import argparse
    import subprocess
    import sys
    from pathlib import Path

    main = tmp_path / "main"
    main.mkdir()
    graph = main / ".agi"
    (graph / "nodes" / "experiment").mkdir(parents=True)
    (graph / "config.json").write_text("{}")
    (graph / "sessions" / "iter-001" / "a00-p").mkdir(parents=True)
    (graph / "sessions" / "iter-001" / "a00-p" / "agent.json").write_text(
        '{"id": "a00-p", "node_id": "experiment:e1", '
        '"parent": "hypothesis:h1", "status": "running"}')
    _write_holder(graph, "001", "a00-p")

    # git-init main on season/s1, one base commit.
    _ggit(main, "init", "-q")
    _ggit(main, "checkout", "-q", "-b", "season/s1")
    _gitc(main, "base")

    # A linked worktree holding the loop branch.
    br = "loop/slug-abc12345@s2"
    wt = tmp_path / "wt"
    r = _ggit(main, "worktree", "add", "-b", br, str(wt), "season/s1")
    assert r.returncode == 0, r.stderr

    # The worktree's own graph + the kid's UNCOMMITTED node write.
    wt_graph = wt / ".agi"
    (wt_graph / "nodes" / "experiment").mkdir(parents=True)
    (wt_graph / "config.json").write_text("{}")
    (wt_graph / "nodes" / "experiment" / "e1.md").write_text(
        "---\nid: experiment:e1\ntype: experiment\nparents:\n- hypothesis:h1\n"
        "---\n\n# experiment:e1\n\nThe kid wrote this body.\n")
    # A second uncommitted node write in the worktree. Its FILENAME carries
    # the round's agent id, so it is in scope for the scoped done commit
    # (hypothesis:l4-the-round-done-commit-scopes-to-the-round-own-paths-
    # never-git-add-a) -- find_node_file resolves it by its frontmatter id,
    # the filename only decides scope.
    (wt_graph / "nodes" / "experiment" / "a00-p-backer.md").write_text(
        "---\nid: experiment:backer\ntype: experiment\nparents:\n"
        "- hypothesis:h1\n---\n\nbody\n")
    assert _ggit(wt, "status", "--porcelain").stdout.strip(), \
        "precondition: the worktree must be dirty before done"

    # `done` resolves its root to the worktree's graph (the parent's cwd).
    cli = _load_cli()
    monkeypatch.setattr(cli, "_find_root", lambda: wt_graph)
    args = argparse.Namespace(
        iter_n=1, agent_id="a00-p", verdict="proved", confidence=0.9,
        node_id="experiment:e1", parent="hypothesis:h1", notes="",
        next_edge=None, evidence_runs=["experiment:backer"],
        no_evidence_gate=False, owns=None, no_spawn_gate=False,
    )
    assert cli.cmd_done(args) == 0

    # The worktree branch landed at base+1 and the tree is clean.
    ahead = _ggit(main, "rev-list", "--count",
                  f"season/s1..{br}").stdout.strip()
    assert ahead == "1", \
        "parent `done` must commit the worktree's node once (base+1)"
    assert not _ggit(wt, "status", "--porcelain").stdout.strip(), \
        "worktree must be clean after done"

    # season.py merge-up against that branch now lands (was REFUSED at 0 ahead).
    bin_dir = Path(__file__).resolve().parents[1] / "bin"
    result = subprocess.run(
        [sys.executable, str(bin_dir / "season.py"),
         "--root", str(graph), "merge-up", br,
         "--suite", "exit 0", "--worktree", str(wt)],
        capture_output=True, text=True,
    )
    combined = result.stdout + result.stderr
    assert result.returncode == 0, \
        f"merge-up must succeed on a committed branch: {combined}"
    assert "merge-up" in result.stdout
    assert "complete; suite green" in result.stdout
    # The node really landed in the base's history via the merge.
    merged = _ggit(main, "log", "season/s1", "--format=%s").stdout
    assert "verdict=proved" in merged or "base" in merged


def test_done_does_not_commit_main_checkout(tmp_path, monkeypatch):
    """The goal:g4.1 guard — a parent running in the MAIN checkout (not a
    linked worktree) must NOT `git add -A` the shared tree on its own `done`.
    The loop owns commits in main; sweeping up sibling agents' work would be
    the exact hazard this whole guard exists to prevent."""
    import argparse
    main = tmp_path / "main"
    main.mkdir()
    graph = main / ".agi"
    (graph / "nodes" / "experiment").mkdir(parents=True)
    (graph / "config.json").write_text("{}")
    (graph / "sessions" / "iter-001" / "a00-p").mkdir(parents=True)
    (graph / "sessions" / "iter-001" / "a00-p" / "agent.json").write_text(
        '{"id": "a00-p", "node_id": "experiment:e1", '
        '"parent": "hypothesis:h1", "status": "running"}')
    _write_holder(graph, "001", "a00-p")
    (graph / "nodes" / "experiment" / "e1.md").write_text(
        "---\nid: experiment:e1\ntype: experiment\nparents:\n- hypothesis:h1\n"
        "---\n\nbody\n")
    (graph / "nodes" / "experiment" / "backer.md").write_text(
        "---\nid: experiment:backer\ntype: experiment\nparents:\n"
        "- hypothesis:h1\n---\n\nbody\n")
    _ggit(main, "init", "-q")
    _ggit(main, "checkout", "-q", "-b", "season/s1")
    _gitc(main, "base")
    # an UNCOMMITTED sibling write in main must be left alone
    (main / "sibling.md").write_text("sibling's work\n")

    cli = _load_cli()
    monkeypatch.setattr(cli, "_find_root", lambda: graph)
    args = argparse.Namespace(
        iter_n=1, agent_id="a00-p", verdict="proved", confidence=0.9,
        node_id="experiment:e1", parent="hypothesis:h1", notes="",
        next_edge=None, evidence_runs=["experiment:backer"],
        no_evidence_gate=False, owns=None, no_spawn_gate=False,
    )
    assert cli.cmd_done(args) == 0
    # main still sits exactly at base: nothing was committed, sibling intact.
    assert _ggit(main, "rev-list", "--count",
                 "season/s1").stdout.strip() == "1"
    assert _ggit(main, "status", "--porcelain").stdout.strip(), \
        "main's uncommitted work must survive done untouched"
    assert (main / "sibling.md").exists()


# --------------------------------------------------------------------------
# hypothesis:l4-the-round-done-commit-scopes-to-the-round-own-paths-never-
# git-add-a -- the worktree `done` commit names its own paths
# --------------------------------------------------------------------------

def test_done_worktree_commit_scopes_to_the_rounds_own_paths(tmp_path,
                                                             monkeypatch,
                                                             capsys):
    """hypothesis:l4-the-round-done-commit-scopes-to-the-round-own-paths-never-
    git-add-a. Measured on SM.41: `_auto_commit_worktree` ran `git add -A` at
    round done, swept a SIBLING kid's dirty node into the commit, and the
    agent-git pre-commit hook -- which admits only node files whose basename
    carries the committing round's agent id -- refused it, so `done` failed.

    The claim: the done commit adds only the round's OWN paths -- the hook's
    scope rule, mirrored here -- never `add -A`. A foreign dirty path is
    printed by name and left alone.
    """
    import argparse

    agent = "a00-k1ab12cd"
    main = tmp_path / "main"
    main.mkdir()
    graph = main / ".agi"
    (graph / "nodes" / "experiment").mkdir(parents=True)
    (graph / "sessions" / "quorum").mkdir(parents=True)
    (graph / "config.json").write_text("{}")
    # The evidence run the round cites lives in main, committed, so it is
    # NOT one of the dirty paths under test (the gate must still resolve it).
    (graph / "nodes" / "experiment" / "backer.md").write_text(
        "---\nid: experiment:backer\ntype: experiment\nparents:\n"
        "- hypothesis:h1\n---\n\nbody\n")
    _ggit(main, "init", "-q")
    _ggit(main, "checkout", "-q", "-b", "season/s1")
    _gitc(main, "base")

    br = "season2/loops/round-a00-k1ab12cd"
    wt = tmp_path / "wt"
    r = _ggit(main, "worktree", "add", "-b", br, str(wt), "season/s1")
    assert r.returncode == 0, r.stderr
    wt_graph = wt / ".agi"

    # The round's session record (shared state: local-first resolution
    # reads the worktree when the record is there).
    (wt_graph / "sessions" / "iter-001" / agent).mkdir(parents=True)
    (wt_graph / "sessions" / "iter-001" / agent / "agent.json").write_text(
        '{"id": "%s", "node_id": "experiment:%s-own", '
        '"parent": "hypothesis:h1", "status": "running"}' % (agent, agent))
    _write_holder(wt_graph, "001", agent)

    # IN SCOPE: the round's OWN node (basename carries its agent id).
    (wt_graph / "nodes" / "experiment" / f"{agent}-own.md").write_text(
        "---\nid: experiment:%s-own\ntype: experiment\nparents:\n"
        "- hypothesis:h1\n---\n\n# own\n" % agent)
    # IN SCOPE: a non-node source edit the round made.
    (wt / "extensions").mkdir()
    (wt / "extensions" / "round_edit.py").write_text("print('round')\n")
    # FOREIGN: a sibling kid's node (no `agent` substring in the basename).
    (wt_graph / "nodes" / "experiment" / "a99-sibling-xyz.md").write_text(
        "---\nid: experiment:a99-sibling-xyz\ntype: experiment\nparents:\n"
        "- hypothesis:h1\n---\n\n# sibling\n")
    # FOREIGN: config, and another post's quorum card.
    (wt_graph / "config.json").write_text('{"tampered": true}')
    (wt_graph / "sessions" / "quorum").mkdir(parents=True, exist_ok=True)
    (wt_graph / "sessions" / "quorum" / "sanctuary-director.md").write_text(
        "card\n")

    cli = _load_cli()
    monkeypatch.setattr(cli, "_find_root", lambda: wt_graph)
    args = argparse.Namespace(
        iter_n=1, agent_id=agent, verdict="proved", confidence=0.9,
        node_id=f"experiment:{agent}-own", parent="hypothesis:h1", notes="",
        next_edge=None, evidence_runs=["experiment:backer"],
        no_evidence_gate=False, owns=None, no_spawn_gate=False,
    )
    assert cli.cmd_done(args) == 0

    # Exactly ONE commit lands, carrying only the in-scope paths.
    assert _ggit(main, "rev-list", "--count",
                 f"season/s1..{br}").stdout.strip() == "1"
    landed = _ggit(main, "show", "--name-only", "--format=", br).stdout
    assert f".agi/nodes/experiment/{agent}-own.md" in landed
    assert "extensions/round_edit.py" in landed
    assert "a99-sibling-xyz.md" not in landed, \
        "the sibling's node must NOT be swept into the round's commit"
    assert ".agi/config.json" not in landed
    assert "sanctuary-director.md" not in landed

    # The foreign bytes are LEFT ALONE -- printed by name, still dirty.
    dirty = _ggit(wt, "status", "--porcelain", "-uall").stdout
    assert "a99-sibling-xyz.md" in dirty
    assert ".agi/config.json" in dirty
    assert "sanctuary-director.md" in dirty
    err = capsys.readouterr().err
    assert "a99-sibling-xyz.md" in err, \
        "a foreign path must be named on stderr, not silently dropped"


# --------------------------------------------------------------------------
# item (5): done in a linked-worktree kid under the REAL agent-git hook
# --------------------------------------------------------------------------

def test_done_worktree_kid_commit_is_allowed_by_the_real_agent_git_hook(
        tmp_path, monkeypatch, capsys):
    """Item (5) verification, measured not assumed: a kid whose frontmatter
    landed, resident in the linked worktree dispatch creates, commits its own
    node under the REAL agent-git pre-commit hook with the dispatch env
    (AGI_TIER=kid, AGI_TREE_PROJECT_ROOT=<worktree>). `done` must NOT print
    `tier kid may not commit` -- the hook's kid branch admits exactly this
    shape (basename carries the agent id)."""
    import argparse
    from pathlib import Path

    agent = "a00-k1ab12cd"
    main = tmp_path / "main"
    main.mkdir()
    graph = main / ".agi"
    (graph / "nodes" / "experiment").mkdir(parents=True)
    (graph / "config.json").write_text("{}")
    (graph / "nodes" / "experiment" / "backer.md").write_text(
        "---\nid: experiment:backer\ntype: experiment\nparents:\n"
        "- hypothesis:h1\n---\n\nbody\n")
    _ggit(main, "init", "-q")
    _ggit(main, "checkout", "-q", "-b", "season/s1")
    _gitc(main, "base")
    hook = Path(__file__).resolve().parents[1] / "hooks" / "agent-git"
    _ggit(main, "config", "core.hooksPath", str(hook))

    br = f"season2/loops/round-{agent}"
    wt = tmp_path / "wt"
    r = _ggit(main, "worktree", "add", "-b", br, str(wt), "season/s1")
    assert r.returncode == 0, r.stderr
    wt_graph = wt / ".agi"
    (wt_graph / "sessions" / "iter-001" / agent).mkdir(parents=True)
    (wt_graph / "sessions" / "iter-001" / agent / "agent.json").write_text(
        '{"id": "%s", "node_id": "experiment:%s-own", '
        '"parent": "hypothesis:h1", "status": "running"}' % (agent, agent))
    _write_holder(wt_graph, "001", agent)
    (wt_graph / "nodes" / "experiment" / f"{agent}-own.md").write_text(
        "---\nid: experiment:%s-own\ntype: experiment\nparents:\n"
        "- hypothesis:h1\n---\n\n# own\n" % agent)

    monkeypatch.setenv("AGI_TIER", "kid")
    monkeypatch.setenv("AGI_PROJECT_ROOT", str(wt_graph))
    monkeypatch.setenv("AGI_TREE_PROJECT_ROOT", str(wt))
    monkeypatch.setenv("AGI_AGENT_ID", agent)

    cli = _load_cli()
    monkeypatch.setattr(cli, "_find_root", lambda: wt_graph)
    args = argparse.Namespace(
        iter_n=1, agent_id=agent, verdict="proved", confidence=0.9,
        node_id=f"experiment:{agent}-own", parent="hypothesis:h1", notes="",
        next_edge=None, evidence_runs=["experiment:backer"],
        no_evidence_gate=False, owns=None, no_spawn_gate=False,
    )
    assert cli.cmd_done(args) == 0
    cap = capsys.readouterr()
    # the round's own node commit LANDS: the hook admitted it and no
    # `tier kid may not commit` line is printed
    assert "may not commit" not in cap.err, cap.err
    assert "committed worktree" in cap.out, cap.out
    assert "may not commit" not in cap.out, cap.out
    assert _ggit(main, "rev-list", "--count",
                 f"season/s1..{br}").stdout.strip() == "1"


# --------------------------------------------------------------------------
# hypothesis:l3-done-lifts-testable-claim -- the completion-half lift at done
# --------------------------------------------------------------------------

def _hypothesis_schema_project(tmp_path):
    """graph root whose [hypothesis].md schema requires testable_claim, plus a
    hypothesis node the kid wrote and a backer experiment for the gate."""
    graph = tmp_path / ".agi"
    (graph / "nodes" / "hypothesis").mkdir(parents=True)
    (graph / "nodes" / "experiment").mkdir(parents=True)
    (graph / "config.json").write_text("{}")
    schemas = graph / "context" / "schemas"
    schemas.mkdir(parents=True)
    (schemas / "[hypothesis].md").write_text(
        "---\nname: hypothesis\nvalidation:\n  required: ["
        "id, type, mint_id, title, testable_claim]\nspawn:\n"
        "  allowed_parents: [goal]\n  min_parents: 1\n---\n\nbody\n")
    (graph / "nodes" / "experiment" / "backer.md").write_text(
        "---\nid: experiment:backer\ntype: experiment\nparents:\n"
        "- goal:g1\n---\n\nbody\n")
    (graph / "nodes" / "hypothesis" / "hy.md").write_text(
        "--HYPOTHESIS_BODY--")
    (graph / "sessions" / "iter-001" / "a00-x").mkdir(parents=True)
    (graph / "sessions" / "iter-001" / "a00-x" / "agent.json").write_text(
        '{"id": "a00-x", "node_id": "hypothesis:hy", '
        '"parent": "goal:g1", "status": "running"}')
    _write_holder(graph, "001", "a00-x")
    import argparse
    args = argparse.Namespace(
        iter_n=1, agent_id="a00-x", verdict="proved", confidence=0.9,
        node_id="hypothesis:hy", parent="goal:g1", notes="",
        next_edge=None, evidence_runs=["experiment:backer"],
        no_evidence_gate=False, owns=None, no_spawn_gate=False,
    )
    return graph, args, (graph / "nodes" / "hypothesis" / "hy.md")


def test_done_lifts_a_kid_claim_written_under_hypothesis_heading(tmp_path,
                                                                 monkeypatch,
                                                                 capsys):
    """A kid that replaced the scaffold prompt with real prose under
    ## Hypothesis sees the field lifted into testable_claim by real `done`:
    schema-valid at done, empty missing_required, no SCHEMA-WARNING."""
    cli = _load_cli()
    graph, args, hy_md = _hypothesis_schema_project(tmp_path)
    hy_md.write_text(
        "---\nid: hypothesis:hy\ntype: hypothesis\nmint_id: "
        "9f38d062aa\nparents:\n- goal:g1\n---\n\n"
        "# hypothesis:hy\n\n"
        "## Hypothesis\n\n"
        "The live population never exceeds the declared bound.\n")
    monkeypatch.setattr(cli, "_find_root", lambda: graph)

    assert cli.cmd_done(args) == 0

    text = hy_md.read_text()
    assert "testable_claim: The live population never exceeds the declared bound." \
        in text
    import node_writer  # noqa: E402
    from graph_core.persistence import frontmatter as _fm  # noqa: E402
    nf = _fm.load_node_file(hy_md)
    assert "testable_claim" not in node_writer.missing_required(
        graph, "hypothesis", nf.frontmatter, "hypothesis:hy")
    assert "SCHEMA-WARNING" not in capsys.readouterr().err


def test_done_loudly_warns_but_never_invents_when_the_prompt_stays(tmp_path,
                                                                  monkeypatch,
                                                                  capsys):
    """A scaffold left with its untouched placeholder prompt is NOT lifted (that
    would invent a claim the kid never made); `done` prints a loud, never-fatal
    SCHEMA-WARNING and still exits 0 with the work saved."""
    cli = _load_cli()
    graph, args, hy_md = _hypothesis_schema_project(tmp_path)
    # the untouched scaffold: prompt still the default question text
    hy_md.write_text(
        "---\nid: hypothesis:hy\ntype: hypothesis\nmint_id: "
        "9f38d062aa\nparents:\n- goal:g1\n---\n\n"
        "# hypothesis:hy\n\n"
        "## Hypothesis\n\n"
        "What is the testable claim? What would prove it? What would "
        "disprove it?\n")
    monkeypatch.setattr(cli, "_find_root", lambda: graph)

    assert cli.cmd_done(args) == 0  # never-fatal

    err = capsys.readouterr().err
    assert "SCHEMA-WARNING" in err
    assert "testable_claim" in err
    assert "testable_claim:" not in hy_md.read_text()


# --------------------------------------------------------------------------
# hypothesis:l4-the-manifest-mirrors-terminal-agent-status (source half)
# --------------------------------------------------------------------------

def test_done_mirrors_terminal_status_into_iteration_manifest(tmp_path, monkeypatch):
    """A clean `cli.py done` mirrors the agent record's terminal fields onto
    the iteration manifest entry that sits beside it, so the round's own exit
    leaves both files agreeing -- no stale `running` until a later reaper pass.
    The record and manifest both live in the fixture's iter-001 dir."""
    cli = _load_cli()
    import json as _json
    graph, args = _cmd_done_project(tmp_path)
    monkeypatch.setattr(cli, "_find_root", lambda: graph)
    mpath = graph / "sessions" / "iter-001" / "manifest.json"
    mpath.write_text(_json.dumps({
        "agents": [{"id": "a00-x", "status": "running", "dispatched_by": "seat"}],
    }))

    assert cli.cmd_done(args) == 0

    agent = _json.loads(
        (graph / "sessions" / "iter-001" / "a00-x" / "agent.json").read_text())
    manifest = _json.loads(mpath.read_text())
    entry = manifest["agents"][0]
    assert agent["status"] == "done"
    assert entry["status"] == "done"
    assert entry["finished_at"] == agent["finished_at"]
    # unrelated manifest fields survive the mirror
    assert entry["dispatched_by"] == "seat"


def test_done_does_not_downgrade_a_more_authoritative_manifest_entry(tmp_path):
    """The manifest is a document with its own status ranking: a record whose
    status ranks BELOW the entry (a `running` record vs an entry already
    `done`) must not downgrade it. Exercised on the guard directly since
    cmd_done itself always writes the top-ranked `done`."""
    cli = _load_cli()
    import json as _json
    mparent = tmp_path / "a00-x"
    mparent.mkdir(parents=True)
    ap = mparent / "agent.json"
    ap.write_text('{"id": "a00-x", "status": "running"}')
    mpath = tmp_path / "manifest.json"
    mpath.write_text(_json.dumps({"agents": [{"id": "a00-x", "status": "done"}]}))

    cli._mirror_terminal_into_manifest(ap, {"id": "a00-x", "status": "running"},
                                       "a00-x")

    manifest = _json.loads(mpath.read_text())
    # not downgraded to running; `done` (rank 5) beat the record's rank 0
    assert manifest["agents"][0]["status"] == "done"


def test_done_succeeds_with_missing_or_corrupt_manifest(tmp_path, monkeypatch):
    """The round still ends and still records its verdict on both a missing
    and a corrupt manifest. A missing manifest means NO holder, so the
    completion dm is silent -- and since SM.67 C2 that silent dm makes
    cmd_done return rc 1 (the harness that ran done must SEE it); the record
    still carries the verdict. A corrupt manifest is still a holder file, so
    the alarm fails non-fatally and cmd_done exits 0."""
    cli = _load_cli()
    import json as _json

    # missing manifest -> no holder -> silent dm -> rc 1, verdict still written
    graph, args = _cmd_done_project(tmp_path)
    (graph / "sessions" / "iter-001" / "manifest.json").unlink()
    monkeypatch.setattr(cli, "_find_root", lambda: graph)
    assert cli.cmd_done(args) == 1, \
        "a silent done (no manifest holder) must surface as rc 1"
    agent = _json.loads(
        (graph / "sessions" / "iter-001" / "a00-x" / "agent.json").read_text())
    assert agent["status"] == "done"

    # corrupt manifest, same fixture shape in a fresh dir
    graph2, args2 = _cmd_done_project(tmp_path / "corrupt")
    mpath = graph2 / "sessions" / "iter-001" / "manifest.json"
    mpath.write_text("not json {{{")
    monkeypatch.setattr(cli, "_find_root", lambda: graph2)
    assert cli.cmd_done(args2) == 0
    agent2 = _json.loads(
        (graph2 / "sessions" / "iter-001" / "a00-x" / "agent.json").read_text())
    assert agent2["status"] == "done"


def test_done_leaves_a_non_matching_manifest_entry_alone(tmp_path, monkeypatch):
    """An entry whose id does not match the finishing agent is left untouched."""
    cli = _load_cli()
    import json as _json
    graph, args = _cmd_done_project(tmp_path)
    monkeypatch.setattr(cli, "_find_root", lambda: graph)
    mpath = graph / "sessions" / "iter-001" / "manifest.json"
    mpath.write_text(_json.dumps({
        "agents": [{"id": "a00-OTHER", "status": "running"}],
    }))

    assert cli.cmd_done(args) == 0

    manifest = _json.loads(mpath.read_text())
    assert manifest["agents"][0]["id"] == "a00-OTHER"
    assert manifest["agents"][0]["status"] == "running"


# --------------------------------------------------------------------------
# hypothesis:l4-the-reader-the-brief-hands-out-prints-the-overdue-mark
# --------------------------------------------------------------------------

def _cmd_status_project(tmp_path, agent_status="running", agent_overdue=False):
    """A minimal project whose iteration round has ONE agent record. Returns
    (graph_root, args) so cmd_status can be driven over it."""
    import json as _json
    graph = tmp_path / ".agi"
    (graph / "sessions" / "iter-001" / "a00-x").mkdir(parents=True)
    (graph / "config.json").write_text("{}")
    agent = {"id": "a00-x", "status": agent_status, "verdict": "-", "pid": 42}
    if agent_overdue:
        agent["overdue_since"] = 1750000000
        agent["overdue_reason"] = "past manifest timeout_seconds"
    (graph / "sessions" / "iter-001" / "a00-x" / "agent.json").write_text(
        _json.dumps(agent))
    (graph / "sessions" / "iter-001" / "manifest.json").write_text(_json.dumps(
        {"agents": [{"id": "a00-x", "status": agent_status}]}))
    import argparse
    args = argparse.Namespace(iter_n=1)
    return graph, args


def test_cmd_status_prints_running_overdue_for_a_live_record_past_deadline(
        tmp_path, monkeypatch, capsys):
    """hypothesis:l4-the-reader-the-brief-hands-out-prints-the-overdue-mark —
    `cli.py status <iter>` is the reader the parent brief names as its poll;
    it must print the SAME `running(overdue)` mark spawn_budget prints, off the
    record's `overdue_since`, or the brief names a word no poll ever shows.
    Red before the fix: cmd_status printed bare `status=running`."""
    cli = _load_cli()
    graph, args = _cmd_status_project(tmp_path, agent_status="running",
                                      agent_overdue=True)
    monkeypatch.setattr(cli, "_find_root", lambda: graph)

    assert cli.cmd_status(args) == 0
    out = capsys.readouterr().out
    assert "status=running(overdue)" in out, out


def test_cmd_status_no_overdue_mark_without_overdue_since(tmp_path, monkeypatch,
                                                          capsys):
    """A `running` record that is NOT past deadline shows plain `running`,
    never `(overdue)`."""
    cli = _load_cli()
    graph, args = _cmd_status_project(tmp_path, agent_status="running",
                                      agent_overdue=False)
    monkeypatch.setattr(cli, "_find_root", lambda: graph)

    assert cli.cmd_status(args) == 0
    out = capsys.readouterr().out
    assert "status=running" in out
    assert "(overdue)" not in out


# --------------------------------------------------------------------------
# hypothesis:l4-cli-done-for-tier-parent-refuses-a-lean-proved-verdict-without-
# one-parent-run-negative-probe-per-claim-conjunct
# --------------------------------------------------------------------------

def _parent_probe_project(tmp_path, tier="parent"):
    """A minimal project root whose agent record runs at `tier` and whose
    `hypothesis:target` carries four numbered claim items (conjuncts 1-4)."""
    import json as _json
    graph = tmp_path / ".agi"
    (graph / "nodes" / "experiment").mkdir(parents=True)
    (graph / "nodes" / "hypothesis").mkdir(parents=True)
    (graph / "config.json").write_text("{}")
    (graph / "nodes" / "hypothesis" / "target.md").write_text(
        "---\nid: hypothesis:target\ntype: hypothesis\ntitle: Target\n"
        "testable_claim: \"(1) first leg; (2) second leg; (3) third leg; "
        "(4) fourth leg\"\n---\n\n# hypothesis:target\n\nBody.\n")
    (graph / "nodes" / "experiment" / "backer.md").write_text(
        "---\nid: experiment:backer\ntype: experiment\ntitle: Backer\n"
        "mint_id: backermint\nparents:\n- hypothesis:target\n---\n\nbody\n")
    (graph / "sessions" / "iter-001" / "a00-p").mkdir(parents=True)
    rec = (graph / "sessions" / "iter-001" / "a00-p" / "agent.json")
    rec.write_text(_json.dumps({"id": "a00-p", "tier": tier,
                                "status": "running"}))
    _write_holder(graph, "001", "a00-p")
    return graph, rec


def _probe_args(**over):
    import argparse
    base = dict(
        iter_n=1, agent_id="a00-p", verdict="proved", confidence=0.9,
        node_id="experiment:backer", parent="hypothesis:target", notes="",
        next_edge=None, evidence_runs=["experiment:backer"],
        no_evidence_gate=False, owns=None, no_spawn_gate=False,
    )
    base.update(over)
    return argparse.Namespace(**base)


def test_done_parent_refuses_proved_without_probes_naming_conjuncts(
        tmp_path, monkeypatch, capsys):
    """A tier-parent `done` recording `proved` with no probes is refused with
    a non-zero exit and the missing conjunct numbers named; nothing is written
    to the record."""
    cli = _load_cli()
    graph, rec = _parent_probe_project(tmp_path)
    monkeypatch.setattr(cli, "_find_root", lambda: graph)
    args = _probe_args(node_id=None)

    assert cli.cmd_done(args) == 2
    err = capsys.readouterr().err
    assert "claim conjunct(s): 1, 2, 3, 4" in err, err
    assert 'status": "running"' in rec.read_text(), \
        "refusal must not write a done status"


def test_done_parent_accepted_with_one_probe_per_conjunct(tmp_path, monkeypatch):
    """A tier-parent `proved` carrying one probe per claim conjunct is accepted,
    and the probes are recorded like evidence_runs (same record, same commit),
    reaching both the agent record and the node frontmatter."""
    import json as _json
    cli = _load_cli()
    graph, rec = _parent_probe_project(tmp_path)
    monkeypatch.setattr(cli, "_find_root", lambda: graph)
    probes = _json.dumps([
        {"conjunct": 1, "class": "auth", "cmd": "no-id call",
         "expected": "refuse", "observed": "refused", "result": "passed"},
        {"conjunct": 2, "class": "gate", "cmd": "other leg",
         "expected": "refuse", "observed": "refused", "result": "passed"},
        {"conjunct": 3, "class": "wire", "cmd": "cli path",
         "expected": "refuse", "observed": "refused", "result": "passed"},
        {"conjunct": 4, "class": "wire", "cmd": "dry-run",
         "expected": "no write", "observed": "no write", "result": "passed"},
    ])
    args = _probe_args(probes=probes)

    assert cli.cmd_done(args) == 0

    rec_fm = _json.loads(rec.read_text())
    assert rec_fm["status"] == "done"
    assert {p["conjunct"] for p in rec_fm["probes"]} == {1, 2, 3, 4}, \
        "probes must be recorded on the agent record like evidence_runs"
    node_text = (graph / "nodes" / "experiment" / "backer.md").read_text()
    assert '"conjunct": 1' in node_text and '"conjunct": 4' in node_text, \
        "probes must reach the node frontmatter like evidence_runs"


def test_done_parent_lean_below_50_needs_no_probe(tmp_path, monkeypatch):
    """A tier-parent verdict below inconclusive_lean_proved:50 asserts nothing
    to prove, so it is accepted with no probes."""
    cli = _load_cli()
    graph, _rec = _parent_probe_project(tmp_path)
    monkeypatch.setattr(cli, "_find_root", lambda: graph)
    args = _probe_args(verdict="inconclusive_lean_proved:40", node_id=None)

    assert cli.cmd_done(args) == 0


def test_done_kid_tier_unchanged_by_probe_gate(tmp_path, monkeypatch):
    """The probe gate applies to `tier parent` only: a kid's `proved` with no
    probes is accepted unchanged."""
    cli = _load_cli()
    graph, _rec = _parent_probe_project(tmp_path, tier="kid")
    monkeypatch.setattr(cli, "_find_root", lambda: graph)
    args = _probe_args(node_id="experiment:backer")

    assert cli.cmd_done(args) == 0


def test_done_parent_dry_run_prints_gate_without_writing(tmp_path, monkeypatch,
                                                        capsys):
    """`--dry-run` prints the probe gate's refusal and returns success without
    writing a done status to the record."""
    cli = _load_cli()
    graph, rec = _parent_probe_project(tmp_path)
    monkeypatch.setattr(cli, "_find_root", lambda: graph)
    args = _probe_args(node_id=None, dry_run=True)

    assert cli.cmd_done(args) == 0
    out = capsys.readouterr().out
    assert "[dry-run]" in out and "1, 2, 3, 4" in out, out
    assert 'status": "running"' in rec.read_text(), \
        "dry-run must not write a done status"


def test_done_parent_dry_run_pass_path_never_writes(tmp_path, monkeypatch,
                                                   capsys):
    """DEFECT 1: `--dry-run` on a PASSING probe gate must print the gate's
    decision and return 0 BEFORE any write -- record still running, node bytes
    unchanged, no verdict stamp. A dry-run flag that mutates on the pass path
    is the one command a cautious parent runs first, so it must be inert."""
    import json as _json
    cli = _load_cli()
    graph, rec = _parent_probe_project(tmp_path)
    node = graph / "nodes" / "experiment" / "backer.md"
    node_before = node.read_text()
    monkeypatch.setattr(cli, "_find_root", lambda: graph)
    probes = _json.dumps([
        {"conjunct": 1, "class": "auth", "cmd": "no-id call",
         "expected": "refuse", "observed": "refused", "result": "passed"},
        {"conjunct": 2, "class": "gate", "cmd": "other leg",
         "expected": "refuse", "observed": "refused", "result": "passed"},
        {"conjunct": 3, "class": "wire", "cmd": "cli path",
         "expected": "refuse", "observed": "refused", "result": "passed"},
        {"conjunct": 4, "class": "wire", "cmd": "dry-run",
         "expected": "no write", "observed": "no write", "result": "passed"},
    ])
    args = _probe_args(probes=probes, dry_run=True)

    assert cli.cmd_done(args) == 0
    out = capsys.readouterr().out
    assert "[dry-run]" in out and "PASS" in out and "1, 2, 3, 4" in out, out
    assert 'status": "running"' in rec.read_text(), \
        "dry-run pass path must not mark the record done"
    assert '"verdict"' not in rec.read_text(), \
        "dry-run pass path must not stamp a verdict on the record"
    assert node.read_text() == node_before, \
        "dry-run pass path must not touch the node bytes"


def test_done_dry_run_inactive_gate_disproved_never_writes(tmp_path, monkeypatch,
                                                           capsys):
    """DEFECT 2: `--dry-run` with an INACTIVE probe gate (parent + disproved,
    no probes) must exit 0 and print the gate not-applicable -- never fall
    through to a write. The record stays `{"status": "running"}` exactly and
    the node bytes are untouched. A dry-run flag that mutates on the
    not-applicable path is the path a cautious parent hits first."""
    cli = _load_cli()
    graph, rec = _parent_probe_project(tmp_path)  # tier parent
    node = graph / "nodes" / "experiment" / "backer.md"
    node_before = node.read_text()
    monkeypatch.setattr(cli, "_find_root", lambda: graph)
    args = _probe_args(verdict="disproved", node_id=None, dry_run=True)

    assert cli.cmd_done(args) == 0
    out = capsys.readouterr().out
    assert "[dry-run]" in out and "not applicable" in out, out
    assert "verdict=disproved" in out, out
    assert rec.read_text() == '{"id": "a00-p", "tier": "parent", "status": "running"}', \
        "dry-run on an inactive gate must leave the record byte-identical"
    assert "\"status\": \"running\"" in rec.read_text()
    assert "verdict" not in rec.read_text(), \
        "dry-run on an inactive gate must not stamp a verdict"
    assert node.read_text() == node_before, \
        "dry-run on an inactive gate must not touch the node bytes"


def test_done_dry_run_inactive_gate_kid_tier_never_writes(tmp_path, monkeypatch,
                                                          capsys):
    """DEFECT 2: `--dry-run` with an INACTIVE probe gate at kid tier must exit
    0 and print the gate not-applicable -- record still running exactly, node
    bytes unchanged, no verdict stamp."""
    cli = _load_cli()
    graph, rec = _parent_probe_project(tmp_path, tier="kid")
    node = graph / "nodes" / "experiment" / "backer.md"
    node_before = node.read_text()
    monkeypatch.setattr(cli, "_find_root", lambda: graph)
    args = _probe_args(node_id="experiment:backer", dry_run=True)  # proved

    assert cli.cmd_done(args) == 0
    out = capsys.readouterr().out
    assert "[dry-run]" in out and "not applicable" in out, out
    assert "tier=kid" in out, out
    assert rec.read_text() == '{"id": "a00-p", "tier": "kid", "status": "running"}', \
        "dry-run on an inactive gate must leave the record byte-identical"
    assert "\"status\": \"running\"" in rec.read_text()
    assert "verdict" not in rec.read_text(), \
        "dry-run on an inactive gate must not stamp a verdict"
    assert node.read_text() == node_before, \
        "dry-run on an inactive gate must not touch the node bytes"


def test_done_parent_probe_missing_result_does_not_cover(tmp_path, monkeypatch,
                                                         capsys):
    """DEFECT 2: a probe missing any of the six fields does NOT count as
    covering its conjunct; the refusal names the malformed probe so the parent
    knows which one to fix."""
    import json as _json
    cli = _load_cli()
    graph, rec = _parent_probe_project(tmp_path)
    monkeypatch.setattr(cli, "_find_root", lambda: graph)
    # A bare conjunct key still covers nothing; the missing `result` probe is
    # named in the refusal.
    probes = _json.dumps([
        {"conjunct": 1, "class": "auth", "cmd": "no-id call",
         "expected": "refuse", "observed": "refused"},  # no `result`
        {"conjunct": 2, "class": "gate", "cmd": "other leg",
         "expected": "refuse", "observed": "refused", "result": "passed"},
        {"conjunct": 3, "class": "wire", "cmd": "cli path",
         "expected": "refuse", "observed": "refused", "result": "passed"},
        {"conjunct": 4, "class": "wire", "cmd": "dry-run",
         "expected": "no write", "observed": "no write", "result": "passed"},
    ])
    args = _probe_args(probes=probes)

    assert cli.cmd_done(args) == 2
    err = capsys.readouterr().err
    assert "claim conjunct(s): 1" in err, err
    assert "missing key(s): result" in err, err
    assert 'status": "running"' in rec.read_text(), \
        "refusal must not write a done status"


def test_done_parent_probe_bad_class_does_not_cover(tmp_path, monkeypatch,
                                                    capsys):
    """DEFECT 2: a probe whose `class` is not auth/gate/wire does not cover
    its conjunct either, and the refusal names it."""
    import json as _json
    cli = _load_cli()
    graph, rec = _parent_probe_project(tmp_path)
    monkeypatch.setattr(cli, "_find_root", lambda: graph)
    probes = _json.dumps([
        {"conjunct": 1, "class": "auth", "cmd": "no-id",
         "expected": "refuse", "observed": "refused", "result": "passed"},
        {"conjunct": 2, "class": "gate", "cmd": "leg",
         "expected": "refuse", "observed": "refused", "result": "passed"},
        {"conjunct": 3, "class": "wire", "cmd": "cli",
         "expected": "refuse", "observed": "refused", "result": "passed"},
        {"conjunct": 4, "class": "bash", "cmd": "shell",
         "expected": "refuse", "observed": "refused", "result": "passed"},
    ])
    args = _probe_args(probes=probes)

    assert cli.cmd_done(args) == 2
    err = capsys.readouterr().err
    assert "claim conjunct(s): 4" in err, err
    assert "invalid class" in err and "bash" in err, err


def test_done_parent_bare_conjunct_probe_covers_nothing(tmp_path, monkeypatch,
                                                        capsys):
    """DEFECT 2 letter-case: `--probes '[{"conjunct":1}]'` -- the exact shape
    the gate used to accept that loses the whole mechanism -- now refuses, since
    the bare probe covers no conjunct and every conjunct is missing."""
    import json as _json
    cli = _load_cli()
    graph, rec = _parent_probe_project(tmp_path)
    monkeypatch.setattr(cli, "_find_root", lambda: graph)
    args = _probe_args(probes=_json.dumps([{"conjunct": 1}]))

    assert cli.cmd_done(args) == 2
    err = capsys.readouterr().err
    assert "claim conjunct(s): 1, 2, 3, 4" in err, err
    assert "missing key(s)" in err, err


# --------------------------------------------------------------------------
# hypothesis:l4-a-reaped-parent-record-names-its-death-class-and-staged-work-
# and-done-salvage-finalizes-a-complete-round-from-the-record
# --------------------------------------------------------------------------

def test_salvage_gate_admits_died_after_work_with_all_kid_verdicts():
    cli = _load_cli()
    manifest = {"agents": [{"id": "parent-p", "death": {
        "class": "died-after-work", "evidence": None, "dirty_paths": 2,
        "kids": [{"id": "experiment:k1", "verdict": "proved"},
                 {"id": "experiment:k2", "verdict": "disproved"}]}}]}
    ok, msg, kids = cli._salvage_gate(manifest, "parent-p")
    assert ok is True, (ok, msg)
    assert msg == ""
    assert [k["id"] for k in kids] == ["experiment:k1", "experiment:k2"]


def test_salvage_gate_refuses_infra_death_by_name():
    cli = _load_cli()
    manifest = {"agents": [{"id": "parent-p", "death": {
        "class": "infra-stream-error",
        "evidence": "HTTP/1.1 500 Internal Server Error", "kids": []}}]}
    ok, msg, kids = cli._salvage_gate(manifest, "parent-p")
    assert ok is False
    assert "infra-stream-error" in msg and "died-after-work" in msg, msg
    assert "redispatch" in msg, msg


def test_salvage_gate_refuses_a_kid_without_a_verdict():
    cli = _load_cli()
    manifest = {"agents": [{"id": "parent-p", "death": {
        "class": "died-after-work",
        "kids": [{"id": "experiment:k1", "verdict": "proved"},
                 {"id": "experiment:k2", "verdict": None}]}}]}
    ok, msg, kids = cli._salvage_gate(manifest, "parent-p")
    assert ok is False
    assert "experiment:k2" in msg, msg
    assert "EVERY kid verdict" in msg, msg


def test_salvage_gate_refuses_a_record_with_no_death_class():
    cli = _load_cli()
    ok, msg, _ = cli._salvage_gate({"agents": [{"id": "parent-p"}]}, "parent-p")
    assert ok is False and "no death class" in msg, msg
    ok, msg, _ = cli._salvage_gate({"agents": []}, "parent-p")
    assert ok is False and "no manifest record" in msg, msg


def _salvage_project(tmp_path, death):
    import json as _json
    graph, rec = _parent_probe_project(tmp_path, tier="kid")
    manifest = {"agents": [{"id": "a00-p", "status": "failed", "death": death}]}
    (graph / "sessions" / "iter-001" / "manifest.json").write_text(
        _json.dumps(manifest))
    return graph, rec


def test_done_salvage_dry_run_prints_death_class_and_would_finalize(
        tmp_path, monkeypatch, capsys):
    """`done --salvage --dry-run` prints the death class + the would-finalize
    summary and mutates nothing."""
    cli = _load_cli()
    graph, rec = _salvage_project(tmp_path, {
        "class": "died-after-work", "evidence": None,
        "kids": [{"id": "experiment:backer", "verdict": "proved"}]})
    monkeypatch.setattr(cli, "_find_root", lambda: graph)
    args = _probe_args(node_id=None, verdict="inconclusive_lean_proved:60",
                       salvage=True, dry_run=True)

    assert cli.cmd_done(args) == 0
    out = capsys.readouterr().out
    assert "death.class=died-after-work" in out, out
    assert "would finalize" in out and "experiment:backer" in out, out
    import json as _json
    assert _json.loads(rec.read_text())["status"] == "running", \
        "dry-run must not write"


def test_done_salvage_refuses_an_infra_death_and_writes_nothing(
        tmp_path, monkeypatch, capsys):
    """`done --salvage` on an infra-stream-error death refuses by name before
    any write."""
    cli = _load_cli()
    graph, rec = _salvage_project(tmp_path, {
        "class": "infra-stream-error", "evidence": "HTTP/1.1 500 x", "kids": []})
    monkeypatch.setattr(cli, "_find_root", lambda: graph)
    args = _probe_args(node_id=None, verdict="inconclusive_lean_proved:60",
                       salvage=True)

    assert cli.cmd_done(args) == 2
    err = capsys.readouterr().err
    assert "infra-stream-error" in err and "died-after-work" in err, err
    import json as _json
    assert _json.loads(rec.read_text())["status"] == "running", \
        "a refused salvage must not write"


def _salvage_worktree_repo(tmp_path, name="wt"):
    """A throwaway git repo with one committed file and one staged change --
    the reaped round's worktree shape (`git -C <wt> add -A` has work to do)."""
    import subprocess
    wt = tmp_path / name
    wt.mkdir()

    def g(*a):
        return subprocess.run(["git", "-C", str(wt), *a],
                              capture_output=True, text=True)

    g("init", "-q")
    g("config", "user.email", "t@t")
    g("config", "user.name", "t")
    (wt / "staged.txt").write_text("before\n")
    g("add", "-A")
    g("commit", "-qm", "base")
    (wt / "staged.txt").write_text("after\n")
    return wt


def _salvage_project_with_worktree(tmp_path):
    """`_salvage_project` (admitted death) whose manifest names a real
    worktree carrying a staged change."""
    import json as _json
    graph, rec = _salvage_project(tmp_path, {
        "class": "died-after-work", "evidence": None,
        "kids": [{"id": "experiment:backer", "verdict": "proved"}]})
    wt = _salvage_worktree_repo(tmp_path)
    mpath = graph / "sessions" / "iter-001" / "manifest.json"
    m = _json.loads(mpath.read_text())
    m["agents"][0]["worktree"] = str(wt)
    mpath.write_text(_json.dumps(m))
    return graph, rec, wt


def test_done_salvage_preserves_staged_bytes_then_finalizes(
        tmp_path, monkeypatch, capsys):
    """An ADMITTED salvage commits the reaped round's staged bytes onto its
    own loop branch with the SM.17 subject, THEN finalizes the record."""
    import json as _json
    import subprocess
    cli = _load_cli()
    graph, rec, wt = _salvage_project_with_worktree(tmp_path)
    monkeypatch.setattr(cli, "_find_root", lambda: graph)
    args = _probe_args(node_id=None, verdict="inconclusive_lean_proved:60",
                       salvage=True)

    assert cli.cmd_done(args) == 0
    subject = subprocess.run(
        ["git", "-C", str(wt), "log", "-1", "--format=%s"],
        capture_output=True, text=True).stdout.strip()
    assert subject.startswith("salvage: staged bytes preserved at "), subject
    # The preserved commit carries the STAGED bytes, and the tree is clean.
    blob = subprocess.run(["git", "-C", str(wt), "show", "HEAD:staged.txt"],
                          capture_output=True, text=True).stdout
    assert blob == "after\n", blob
    assert subprocess.run(["git", "-C", str(wt), "status", "--porcelain"],
                          capture_output=True, text=True).stdout.strip() == ""
    assert "salvage: preserved 1 staged path(s)" in capsys.readouterr().out
    assert _json.loads(rec.read_text())["status"] == "done"


def test_done_salvage_refuses_and_finalizes_nothing_when_preserve_cannot_run(
        tmp_path, monkeypatch, capsys):
    """PRESERVE IS FIRST: an admitted death whose worktree cannot be found
    refuses the whole salvage and writes NOTHING -- the record is not
    finalized."""
    import json as _json
    cli = _load_cli()
    graph, rec = _salvage_project(tmp_path, {
        "class": "died-after-work", "evidence": None,
        "kids": [{"id": "experiment:backer", "verdict": "proved"}]})
    monkeypatch.setattr(cli, "_find_root", lambda: graph)
    args = _probe_args(node_id=None, verdict="inconclusive_lean_proved:60",
                       salvage=True)

    assert cli.cmd_done(args) == 2
    err = capsys.readouterr().err
    assert "no worktree" in err, err
    assert _json.loads(rec.read_text())["status"] == "running", \
        "no preserve commit -> nothing finalized"


def test_done_salvage_dry_run_names_the_would_preserve_sha_and_writes_nothing(
        tmp_path, monkeypatch, capsys):
    """`--dry-run` names the would-preserve sha by staging into a throwaway
    index: no commit, no index change, no record write."""
    import json as _json
    import subprocess
    cli = _load_cli()
    graph, rec, wt = _salvage_project_with_worktree(tmp_path)
    monkeypatch.setattr(cli, "_find_root", lambda: graph)
    args = _probe_args(node_id=None, verdict="inconclusive_lean_proved:60",
                       salvage=True, dry_run=True)

    assert cli.cmd_done(args) == 0
    out = capsys.readouterr().out
    assert "[dry-run] preserve: would preserve 1 path(s) at " in out, out
    assert "would finalize" in out, out
    log = subprocess.run(["git", "-C", str(wt), "log", "--format=%s"],
                         capture_output=True, text=True).stdout
    assert "salvage:" not in log, "dry-run must not commit"
    assert subprocess.run(["git", "-C", str(wt), "status", "--porcelain"],
                          capture_output=True, text=True).stdout.strip() != "", \
        "dry-run must not touch the real index"
    assert _json.loads(rec.read_text())["status"] == "running"


def test_salvage_preserve_dry_run_names_the_preserved_tree_sha(tmp_path):
    """The dry-run sha must be the tree of the WOULD-PRESERVE bytes -- the
    same tree the real preserve commits -- never HEAD^{tree}, which is the
    pre-change tree. Regression: the dry-run branch seeded the throwaway
    index with `read-tree HEAD` and never ran `add -A` into it, so
    `write-tree` returned HEAD unchanged and `--dry-run` named the wrong
    sha. Also proves the dry-run writes nothing: no commit, real index and
    working tree untouched."""
    import os
    import subprocess
    import tempfile
    cli = _load_cli()
    wt = _salvage_worktree_repo(tmp_path)

    def g(*a, env=None):
        return subprocess.run(["git", "-C", str(wt), *a],
                              capture_output=True, text=True, env=env)

    head_tree = g("rev-parse", "HEAD^{tree}").stdout.strip()
    before_log = g("log", "--format=%H").stdout
    before_index = g("diff", "--cached", "--name-only").stdout

    # The reference sha, computed independently with the same throwaway-index
    # recipe: read-tree HEAD + add -A + write-tree into a /tmp index.
    fd, ref_index = tempfile.mkstemp(prefix="agi-test-ref-index-")
    os.close(fd)
    os.unlink(ref_index)
    renv = dict(os.environ, GIT_INDEX_FILE=ref_index)
    try:
        assert g("read-tree", "HEAD", env=renv).returncode == 0
        assert g("add", "-A", env=renv).returncode == 0
        ref_sha = g("write-tree", env=renv).stdout.strip()
    finally:
        try:
            os.unlink(ref_index)
        except OSError:
            pass

    sha, msg = cli._salvage_preserve(wt, "ag", dry_run=True)
    assert sha == ref_sha, (sha, ref_sha)
    assert sha != head_tree, (sha, head_tree)
    # The named tree carries the working bytes, not HEAD's.
    assert g("show", f"{sha}:staged.txt").stdout == "after\n"
    # Dry-run wrote nothing: no commit, real index untouched, tree dirty.
    assert g("log", "--format=%H").stdout == before_log
    assert g("diff", "--cached", "--name-only").stdout == before_index
    assert g("status", "--porcelain").stdout.strip() != ""

    # The real preserve commits exactly that tree -- dry-run and real agree.
    real_sha, _ = cli._salvage_preserve(wt, "ag")
    assert real_sha == sha, (real_sha, sha)
    assert g("rev-parse", "HEAD^{tree}").stdout.strip() == sha


def test_session_complete_stamps_the_acting_seat(tmp_path, monkeypatch):
    """A `session-complete` is the seat's OWN work act (hypothesis:l4-the-card-
    age-captive-...-the-rotating-seat-own-last-act, conjunct 1): the verb
    stamps the acting seat's last-act through the ONE clock (bin/last_act.py),
    and a `--dry-run` touches nothing."""
    import argparse
    cli = _load_cli()
    graph = tmp_path / "proj" / ".agi"
    (graph / "nodes" / ".geometry").mkdir(parents=True)
    (graph / "config.json").write_text("{}")
    monkeypatch.setattr(cli, "_find_root", lambda: graph)
    monkeypatch.setattr(cli, "_main_graph_root", lambda r: r)
    monkeypatch.setattr(cli, "_session_complete", lambda *a, **k: 0)
    monkeypatch.setenv("AGI_SEAT", "seat-a")
    stamp = graph / "sessions" / "seats" / "seat-a.last-act"
    args = argparse.Namespace(iter_n="SM.1", worktree=None, dry_run=True)
    assert cli.cmd_session_complete(args) == 0
    assert not stamp.exists(), "a dry run must stamp nothing"
    args.dry_run = False
    assert cli.cmd_session_complete(args) == 0
    assert stamp.exists(), "session-complete left no seat last-act stamp"


def test_worktree_done_commit_subject_carries_the_kid_nodes_verdict(tmp_path):
    """item (5), commit half. A parent round carries no `--node-id`, so
    `_auto_commit_worktree`'s ref is the OWNED KID node. The subject must
    carry the verdict THAT node carries -- measured at b3523f325: subject
    `a00-19566029 done: experiment:a00-f067c356-b0ad80 verdict=pending` over a
    node carrying `verdict: inconclusive_lean_disproved:70`, which reads as a
    false claim about the kid node. The parent's own `--verdict` may not leak
    into the subject when the ref is the kid's node."""
    main = tmp_path / "main"
    main.mkdir()
    graph = main / ".agi"
    (graph / "nodes" / "experiment").mkdir(parents=True)
    (graph / "config.json").write_text("{}")
    _ggit(main, "init", "-q")
    _ggit(main, "checkout", "-q", "-b", "season/s1")
    _gitc(main, "base")

    br = "loop/slug-abc12345@s2"
    wt = tmp_path / "wt"
    r = _ggit(main, "worktree", "add", "-b", br, str(wt), "season/s1")
    assert r.returncode == 0, r.stderr
    wt_graph = wt / ".agi"
    (wt_graph / "nodes" / "experiment").mkdir(parents=True)
    (wt_graph / "config.json").write_text("{}")
    # The filename carries the round's agent id (scope); find_node_file
    # resolves by frontmatter id -- the kid's stored verdict is the truth.
    (wt_graph / "nodes" / "experiment" / "a00-parent-kid.md").write_text(
        "---\nid: experiment:kid\ntype: experiment\nparents:\n"
        "- hypothesis:h1\nverdict: inconclusive_lean_disproved:70\n"
        "---\n\nbody\n")

    cli = _load_cli()
    root = cli._auto_commit_worktree(wt_graph, "a00-parent", None,
                                     ["experiment:kid"], "pending")
    assert root is not None
    subject = _ggit(main, "log", "-1", "--format=%s", br).stdout.strip()
    assert "done: experiment:kid verdict=inconclusive_lean_disproved:70" in \
        subject, subject
    assert "verdict=pending" not in subject, subject


def test_worktree_done_commit_subject_names_unset_for_an_empty_kid_verdict(
        tmp_path):
    """hypothesis:l4-the-kid-brief-demands-a-title-and-the-done-subject-
    never-borrows-the-parent-verdict-for-an-empty-node item (2): when the
    owned kid node carries NO or an EMPTY verdict key, the subject must NAME
    that (`verdict=unset`) and must never borrow the parent's gate-resolved
    `--verdict` -- the same false-claim shape b3523f325 fixed, one branch
    over."""
    main = tmp_path / "main"
    main.mkdir()
    graph = main / ".agi"
    (graph / "nodes" / "experiment").mkdir(parents=True)
    (graph / "config.json").write_text("{}")
    _ggit(main, "init", "-q")
    _ggit(main, "checkout", "-q", "-b", "season/s1")
    _gitc(main, "base")

    br = "loop/slug-empty@s2"
    wt = tmp_path / "wt"
    r = _ggit(main, "worktree", "add", "-b", br, str(wt), "season/s1")
    assert r.returncode == 0, r.stderr
    wt_graph = wt / ".agi"
    (wt_graph / "nodes" / "experiment").mkdir(parents=True)
    (wt_graph / "config.json").write_text("{}")
    # The kid node exists but its verdict key is EMPTY.
    (wt_graph / "nodes" / "experiment" / "a00-parent-kid2.md").write_text(
        "---\nid: experiment:kid2\ntype: experiment\nparents:\n"
        "- hypothesis:h1\nverdict: ''\n---\n\nbody\n")

    cli = _load_cli()
    root = cli._auto_commit_worktree(wt_graph, "a00-parent", None,
                                     ["experiment:kid2"],
                                     "inconclusive_lean_proved:60")
    assert root is not None
    subject = _ggit(main, "log", "-1", "--format=%s", br).stdout.strip()
    assert "done: experiment:kid2 verdict=unset" in subject, subject
    assert "inconclusive_lean_proved:60" not in subject, subject


def test_worktree_done_commit_subject_unset_when_the_kid_node_is_absent(
        tmp_path):
    """Same item (2), the missing-file leg: with no node to read a verdict
    from, there is nothing to attribute to the kid either, so the subject
    says `unset` rather than the parent's `--verdict`."""
    main = tmp_path / "main"
    main.mkdir()
    graph = main / ".agi"
    (graph / "nodes" / "experiment").mkdir(parents=True)
    (graph / "config.json").write_text("{}")
    _ggit(main, "init", "-q")
    _ggit(main, "checkout", "-q", "-b", "season/s1")
    _gitc(main, "base")

    br = "loop/slug-missing@s2"
    wt = tmp_path / "wt"
    r = _ggit(main, "worktree", "add", "-b", br, str(wt), "season/s1")
    assert r.returncode == 0, r.stderr
    wt_graph = wt / ".agi"
    (wt_graph / "nodes" / "experiment").mkdir(parents=True)
    (wt_graph / "config.json").write_text("{}")
    # A file the round owns (agent id in the filename) but not the node id.
    (wt_graph / "nodes" / "experiment" / "a00-parent-missing.md").write_text(
        "---\nid: experiment:elsewhere\ntype: experiment\n---\n\nbody\n")

    cli = _load_cli()
    root = cli._auto_commit_worktree(wt_graph, "a00-parent", None,
                                     ["experiment:missing"],
                                     "inconclusive_lean_proved:60")
    assert root is not None
    subject = _ggit(main, "log", "-1", "--format=%s", br).stdout.strip()
    assert "done: experiment:missing verdict=unset" in subject, subject
    assert "inconclusive_lean_proved:60" not in subject, subject
# --------------------------------------------------------------------------
# hypothesis:l4-sm36-...-one-scope-rule -- item 9 (the cli half of the ONE
# rule) and item 8 (the died-no-work scaffold moved, never deleted).
# --------------------------------------------------------------------------

def test_round_scope_ok_is_one_rule_and_honours_explicit_own_paths():
    """The cli predicate: a human-slug node named in own_paths is IN scope,
    the very same path without own_paths is another author's node, a sibling
    kid's node is never in scope, and the agent's own id-named node is in
    scope without own_paths."""
    cli = _load_cli()
    agent = "a00-e2890daf"
    own = ".agi/nodes/experiment/human-slug-node.md"
    assert cli._round_scope_ok(own, agent, {own}) is True
    assert cli._round_scope_ok(own, agent, set()) is False
    assert cli._round_scope_ok(
        ".agi/nodes/experiment/a00-otherkid-1.md", agent, {own}) is False
    assert cli._round_scope_ok(
        f".agi/nodes/experiment/{agent}-7f2449.md", agent, set()) is True


def test_scope_check_reads_own_paths_from_the_env_the_hook_exports(
        monkeypatch):
    """The served surface the hook calls: NUL-separated paths on stdin,
    AGI_ROUND_OWN_PATHS carrying the round's own paths. Exit 0 iff every path
    is in the ONE rule."""
    import argparse
    import io
    import sys
    cli = _load_cli()
    own = ".agi/nodes/experiment/human-slug-node.md"
    sibling = ".agi/nodes/experiment/a00-otherkid-1.md"
    monkeypatch.setenv("AGI_ROUND_OWN_PATHS", own)
    args = argparse.Namespace(agent_id="a00-e2890daf", own=[])
    monkeypatch.setattr(sys, "stdin", io.StringIO(own + "\0"))
    assert cli.cmd_scope_check(args) == 0
    monkeypatch.setattr(sys, "stdin", io.StringIO(sibling + "\0"))
    assert cli.cmd_scope_check(args) == 1


def test_died_no_work_scaffold_moved_to_deprecated_and_never_deleted():
    """item 8: experiment:a00-af4a5702-dabe39 (spawn died no-work) is MOVED to
    deprecated/ with status: deprecated; the live path is gone and the
    deprecated path exists exactly once."""
    from pathlib import Path
    repo = Path(__file__).resolve().parents[3]
    graph = repo / ".agi"
    live = sorted((graph / "nodes" / "experiment").glob("a00-af4a5702*"))
    dead = (graph / "nodes" / "deprecated" / "experiment"
            / "a00-af4a5702-dabe39.md")
    assert live == [], f"died-no-work scaffold still live: {live}"
    assert dead.is_file(), "scaffold was deleted, not moved to deprecated/"
    text = dead.read_text(encoding="utf-8")
    assert "status: deprecated" in text
    assert "SPAWN DIED NO-WORK" in text, "Agent Notes were not kept verbatim"


# hypothesis:l4-the-harvest-demotes-a-claimed-but-absent-deliverable-in-code-
# and-the-strip-test-asserts-the-strip -- the parent brief used to carry the
# rule as PROSE. `_missing_claimed_deliverables` is the CODE: a round that
# names a deliverable (`--deliverables`) its branch diff does not carry is
# demoted to inconclusive_lean_disproved naming the missing path.
def test_done_demotes_a_claimed_but_absent_deliverable(tmp_path, monkeypatch):
    import argparse
    import json
    import subprocess
    graph = tmp_path / ".agi"
    (graph / "nodes" / "experiment").mkdir(parents=True)
    (graph / "config.json").write_text("{}")
    (graph / "nodes" / "experiment" / "e1.md").write_text(
        "---\nid: experiment:e1\ntype: experiment\n"
        "parents:\n- hypothesis:h1\n---\n\n# experiment:e1\nbody\n")
    (graph / "nodes" / "experiment" / "backer.md").write_text(
        "---\nid: experiment:backer\ntype: experiment\nparents:\n"
        "- hypothesis:h1\n---\n\nbody\n")
    (graph / "sessions" / "iter-001" / "a00-x").mkdir(parents=True)
    (graph / "sessions" / "iter-001" / "a00-x" / "agent.json").write_text(
        '{"id": "a00-x", "node_id": "experiment:e1", "parent": '
        '"hypothesis:h1", "status": "running", "branch": "round-1"}')
    # SM.67: a round always has its iter manifest (dispatch writes one), so
    # the completion-alarm resolves a holder and the clean round exits 0.
    (graph / "sessions" / "iter-001" / "manifest.json").write_text('{"agents": []}')
    # a REAL git repo so the mechanism's git-diff read has a tree to read:
    # `a.py` is an untracked working-tree deliverable this round carries;
    # `gone.py` is NAMED but absent -- the claimed-but-absent shape.
    subprocess.run(["git", "init", "-q"], cwd=tmp_path, check=True)
    (tmp_path / "a.py").write_text("x = 1\n")
    cli = _load_cli()
    monkeypatch.setattr(cli, "_find_root", lambda: graph)
    args = argparse.Namespace(
        iter_n=1, agent_id="a00-x", verdict="proved", confidence=0.9,
        node_id="experiment:e1", parent="hypothesis:h1", notes="",
        next_edge=None, evidence_runs=["experiment:backer"],
        no_evidence_gate=False, owns=None, no_spawn_gate=False,
        deliverables=json.dumps(["a.py", "gone.py"]),
        salvage=False, dry_run=False,
    )
    assert cli.cmd_done(args) == 0
    rec = json.loads((graph / "sessions" / "iter-001" / "a00-x" /
                      "agent.json").read_text())
    assert rec["verdict"] == "inconclusive_lean_disproved:50", rec
    assert rec["missing_deliverables"] == ["gone.py"], rec
    assert "gone.py" in rec["demote_reason"], rec
    # the carried deliverable was NOT demoted for -- only the absent one.
    assert rec["demoted_from"] == "proved"

# --------------------------------------------------------------------------
# hypothesis:l4-the-deliverable-check-diffs-against-the-round-base-in-the-kid-
# worktree-and-runs-in-the-live-harvest
# CONJUNCT 5: a SEASON-SHAPED repo where the round's true fork base (recorded
# base_branch) is NOT master. The pre-fix master-based resolve would carry
# season_thing.py (it lives in the season main, swept by a master diff) and so
# would NOT demote it -- only the round-OWN base resolve names it missing.
# Conjunct 3 (node frontmatter `deliverables:`) and conjunct 4 (a both-demote
# keeps the evidence-gate ORIGINAL verdict) are asserted here too.
# --------------------------------------------------------------------------

def test_done_deliverable_diffs_against_round_base_in_season_repo(tmp_path, monkeypatch):
    import argparse
    import json
    import subprocess
    graph = tmp_path / ".agi"
    (graph / "nodes" / "experiment").mkdir(parents=True)
    (graph / "config.json").write_text("{}")
    (graph / "nodes" / "experiment" / "e1.md").write_text(
        "---\nid: experiment:e1\ntype: experiment\n"
        "deliverables:\n- carried.py\n- gone.py\n- season_thing.py\n"
        "parents:\n- hypothesis:h1\n---\n\n# experiment:e1\nbody\n")
    (graph / "nodes" / "experiment" / "backer.md").write_text(
        "---\nid: experiment:backer\ntype: experiment\nparents:\n"
        "- hypothesis:h1\n---\n\nbody\n")
    (graph / "sessions" / "iter-001" / "a00-x").mkdir(parents=True)
    (graph / "sessions" / "iter-001" / "a00-x" / "agent.json").write_text(
        '{"id": "a00-x", "node_id": "experiment:e1", "parent": '
        '"hypothesis:h1", "status": "running", '
        '"branch": "season2/loops/hyp-x-a00-y", "base_branch": "season2/main"}')
    (graph / "sessions" / "iter-001" / "a00-y").mkdir(parents=True)
    (graph / "sessions" / "iter-001" / "a00-y" / "agent.json").write_text(
        '{"id": "a00-y", "node_id": "experiment:e1", "parent": '
        '"hypothesis:h1", "status": "running", '
        '"branch": "season2/loops/hyp-x-a00-y", "base_branch": "season2/main"}')
    (graph / "sessions" / "iter-001" / "manifest.json").write_text('{"agents": []}')
    # season-shaped live repo: master is REAL and its own fork point; the loop
    # branch forks from season2/main (its recorded base_branch), NOT master.
    subprocess.run(["git", "init", "-q"], cwd=tmp_path, check=True)
    _git = lambda *a: subprocess.run(["git", "-c", "user.email=t@t",
                                      "-c", "user.name=t", "-C", str(tmp_path),
                                      *a], capture_output=True, text=True, check=True)
    _git("checkout", "-q", "-b", "master")
    (tmp_path / "base.py").write_text("x = 1\n")
    _git("add", "-A"); _git("commit", "-qm", "master")
    _git("checkout", "-q", "-b", "season2/main")
    (tmp_path / "season_thing.py").write_text("x = 2\n")
    _git("add", "-A"); _git("commit", "-qm", "season main")
    _git("checkout", "-q", "-b", "season2/loops/hyp-x-a00-y")
    (tmp_path / "carried.py").write_text("x = 3\n")
    _git("add", "-A"); _git("commit", "-qm", "loop work")
    cli = _load_cli()
    monkeypatch.setattr(cli, "_find_root", lambda: graph)
    args = argparse.Namespace(
        iter_n=1, agent_id="a00-x", verdict="proved", confidence=0.9,
        node_id="experiment:e1", parent="hypothesis:h1", notes="",
        next_edge=None, evidence_runs=["experiment:backer"],
        no_evidence_gate=False, owns=None, no_spawn_gate=False,
        deliverables=None,  # node frontmatter carries them (conjunct 3)
        salvage=False, dry_run=False,
    )
    assert cli.cmd_done(args) == 0
    rec = json.loads((graph / "sessions" / "iter-001" / "a00-x" /
                      "agent.json").read_text())
    assert rec["verdict"] == "inconclusive_lean_disproved:50", rec
    # season_thing.py is carried by a MASTER diff but NOT by the true base diff,
    # so only the round-own base resolve demotes it; carried.py stays carried.
    assert rec["missing_deliverables"] == ["gone.py", "season_thing.py"], rec
    assert "carried.py" not in rec["missing_deliverables"]
    assert "season_thing.py" in rec["demote_reason"], rec
    assert rec["demoted_from"] == "proved"
    # conjunct 4: a BOTH-demote (gate: no evidence + absent deliverable) keeps
    # the evidence-gate ORIGINAL verdict, not the gate's demoted lean.
    args2 = argparse.Namespace(**vars(args))
    args2.agent_id = "a00-y"; args2.evidence_runs = []
    assert cli.cmd_done(args2) == 0
    rec2 = json.loads((graph / "sessions" / "iter-001" / "a00-y" /
                       "agent.json").read_text())
    assert rec2["verdict"] == "inconclusive_lean_disproved:50", rec2
    assert rec2["demoted_from"] == "proved", rec2  # gate original survives
    assert "gone.py" in rec2["demote_reason"], rec2


# --------------------------------------------------------------------------
# hypothesis:l5-a-parent-that-accepts-a-kid-branch-lands-that-branch-on-its-
# own-at-done-time -- a parent `done --owns <kid>` folds the kid's own
# `--branch` into the parent's checkout, so an accepted artefact is never left
# stranded on the kid's branch (parent branch base+0 while kids carry the work).
# --------------------------------------------------------------------------

def _kid_branch_worktree(main, tmp_path, name, branch, fname, body):
    """A kid's own --branch worktree cut from season/s1, one real commit."""
    wt = tmp_path / f"wt-{name}"
    r = _ggit(main, "worktree", "add", "-b", branch, str(wt), "season/s1")
    assert r.returncode == 0, r.stderr
    (wt / fname).write_text(body)
    _ggit(wt, "add", "-A")
    rc = _ggit(wt, "-c", "user.email=t@t", "-c", "user.name=t",
               "commit", "-qm", f"kid {name}")
    assert rc.returncode == 0, rc.stderr
    return wt


def _owned_parent_setup(tmp_path, rows):
    """main + a linked parent worktree, clean, carrying the iter manifest that
    names the kid rows (node_id -> branch). Returns (main, pbr, pwt, wt_graph).
    `.agi/sessions/` is committed as ignored so the manifest itself never
    becomes an in-scope dirty path in the parent's round commit."""
    import json as _json
    main = tmp_path / "main"
    main.mkdir()
    graph = main / ".agi"
    (graph / "nodes" / "experiment").mkdir(parents=True)
    (graph / "config.json").write_text("{}")
    (main / ".gitignore").write_text(".agi/sessions/\n")
    _ggit(main, "init", "-q")
    _ggit(main, "checkout", "-q", "-b", "season/s1")
    _gitc(main, "base")
    pbr = "loop/parent-abc12345@s2"
    pwt = tmp_path / "wt-p"
    r = _ggit(main, "worktree", "add", "-b", pbr, str(pwt), "season/s1")
    assert r.returncode == 0, r.stderr
    wt_graph = pwt / ".agi"
    d = wt_graph / "sessions" / "iter-001"
    d.mkdir(parents=True, exist_ok=True)
    (d / "manifest.json").write_text(_json.dumps({"agents": rows}))
    return main, pbr, pwt, wt_graph


def test_done_merges_the_owned_kids_branch_into_the_parent(tmp_path,
                                                           monkeypatch):
    """The claim's conjunct 1/2: with the parent worktree CLEAN (its review was
    real but it made no direct edits) and the accepted kid's one commit sitting
    only on the kid's --branch, `_auto_commit_worktree` must land that branch on
    the parent's own branch -- base+1, carrying the kid's bytes. Today the
    parent reads exactly its fork point (base+0)."""
    main, pbr, pwt, wt_graph = _owned_parent_setup(tmp_path, [
        {"id": "a00-parent", "status": "running"},
        {"id": "a00-k1", "node_id": "experiment:kidA",
         "branch": "loop/kid-aaa11111@s2"},
    ])
    _kid_branch_worktree(main, tmp_path, "a", "loop/kid-aaa11111@s2",
                         "kid_a.py", "a = 1\n")
    cli = _load_cli()
    monkeypatch.setattr(cli, "_find_root", lambda: wt_graph)
    cli._auto_commit_worktree(wt_graph, "a00-parent", None,
                              ["experiment:kidA"], "proved")
    ahead = _ggit(main, "rev-list", "--count", "--first-parent",
                  f"season/s1..{pbr}").stdout.strip()
    assert ahead == "1", f"parent branch must land base+1, got {ahead}"
    ls = _ggit(main, "ls-tree", "-r", "--name-only", pbr).stdout
    assert "kid_a.py" in ls, ls


def test_done_lands_two_owned_kid_branches_as_two_merges(tmp_path,
                                                         monkeypatch):
    """Conjunct 4, the sequential leg: two sibling kids (both cut from the
    parent's base), each accepted by its own `done --owns`, land as base+2 --
    each merge is its own round's finishing act."""
    main, pbr, pwt, wt_graph = _owned_parent_setup(tmp_path, [
        {"id": "a00-parent", "status": "running"},
        {"id": "a00-k1", "node_id": "experiment:kidA",
         "branch": "loop/kid-aaa11111@s2"},
        {"id": "a00-k2", "node_id": "experiment:kidB",
         "branch": "loop/kid-bbb22222@s2"},
    ])
    _kid_branch_worktree(main, tmp_path, "a", "loop/kid-aaa11111@s2",
                         "kid_a.py", "a = 1\n")
    _kid_branch_worktree(main, tmp_path, "b", "loop/kid-bbb22222@s2",
                         "kid_b.py", "b = 1\n")
    cli = _load_cli()
    monkeypatch.setattr(cli, "_find_root", lambda: wt_graph)
    cli._auto_commit_worktree(wt_graph, "a00-parent", None,
                              ["experiment:kidA"], "proved")
    cli._auto_commit_worktree(wt_graph, "a00-parent", None,
                              ["experiment:kidB"], "proved")
    ahead = _ggit(main, "rev-list", "--count", "--first-parent",
                  f"season/s1..{pbr}").stdout.strip()
    assert ahead == "2", f"two accepted kids must land base+2, got {ahead}"
    ls = _ggit(main, "ls-tree", "-r", "--name-only", pbr).stdout
    assert "kid_a.py" in ls and "kid_b.py" in ls, ls


def test_done_leaves_a_branchless_kid_unchanged(tmp_path, monkeypatch):
    """Conjunct 3: a kid dispatched WITHOUT `--branch` (no branch cell in its
    manifest row) leaves today's path byte-identical -- no merge, parent's
    branch stays at its fork point."""
    main, pbr, pwt, wt_graph = _owned_parent_setup(tmp_path, [
        {"id": "a00-parent", "status": "running"},
        {"id": "a00-k1", "node_id": "experiment:kidA"},
    ])
    cli = _load_cli()
    monkeypatch.setattr(cli, "_find_root", lambda: wt_graph)
    cli._auto_commit_worktree(wt_graph, "a00-parent", None,
                              ["experiment:kidA"], "proved")
    ahead = _ggit(main, "rev-list", "--count", "--first-parent",
                  f"season/s1..{pbr}").stdout.strip()
    assert ahead == "0", f"a branchless kid must not move the parent, got {ahead}"


def test_done_refuses_a_conflicting_kid_branch_by_name(tmp_path, monkeypatch,
                                                       capsys):
    """Conjunct 3, conflict leg: a merge that conflicts is aborted and named --
    never a partial merge. The parent branch is left exactly where it was."""
    main, pbr, pwt, wt_graph = _owned_parent_setup(tmp_path, [
        {"id": "a00-parent", "status": "running"},
        {"id": "a00-k1", "node_id": "experiment:kidA",
         "branch": "loop/kid-aaa11111@s2"},
    ])
    # The parent's own branch is one commit ahead, editing f.txt one way ...
    (pwt / "f.txt").write_text("parent\n")
    _ggit(pwt, "add", "-A")
    rc = _ggit(pwt, "-c", "user.email=t@t", "-c", "user.name=t",
               "commit", "-qm", "parent edit")
    assert rc.returncode == 0, rc.stderr
    # ... and the kid edits the SAME file the other way -> a real conflict.
    kwt = _kid_branch_worktree(main, tmp_path, "a", "loop/kid-aaa11111@s2",
                               "f.txt", "kid\n")
    cli = _load_cli()
    monkeypatch.setattr(cli, "_find_root", lambda: wt_graph)
    cli._auto_commit_worktree(wt_graph, "a00-parent", None,
                              ["experiment:kidA"], "proved")
    err = capsys.readouterr().err
    assert "loop/kid-aaa11111@s2" in err, err
    ahead = _ggit(main, "rev-list", "--count", "--first-parent",
                  f"season/s1..{pbr}").stdout.strip()
    assert ahead == "1", f"a refused merge must not move the parent, got {ahead}"
    assert _ggit(main, "ls-files", "-u").stdout.strip() == "", \
        "no conflict may survive the refusal (no partial merge)"


def test_reshuffle_refs_grid_reads_the_projects_storage_trunk(tmp_path, monkeypatch):
    """`_reshuffle_refs_grid` keys its `for-each-ref` namespace on
    `grid.ref_ns_for` (goal:g14.14.7) rather than the literal `refs/grid`, so
    the before/after identity check follows the project's configured trunk."""
    cli = _load_cli()
    repo = tmp_path / "r"
    repo.mkdir()
    seen: list[list[str]] = []

    class _R:
        returncode = 0
        stdout = ""
        stderr = ""

    def recorder(argv, **kw):
        seen.append([str(a) for a in argv])
        return _R()

    monkeypatch.setattr(cli.subprocess, "run", recorder)
    monkeypatch.setattr(cli.grid, "ref_ns_for",
                        lambda root: "refs/grid/t9")
    out = cli._reshuffle_refs_grid(repo)
    assert out == "\n"
    assert seen and seen[0][-1] == "refs/grid/t9", seen


# --------------------------------------------------------------------------
# hypothesis:a-kid-can-commit-the-existing-nodes-its-orders-name -- the round
# commits an EXISTING node its orders NAME (the target), and still refuses
# every other foreign path, `.agi/config.json` included.
# --------------------------------------------------------------------------

def test_named_target_node_ids_come_from_the_record_and_the_parent():
    cli = _load_cli()
    rec = {"target": "hypothesis:tgt", "parent": "goal:g1",
           "node_id": "experiment:a00-x-1"}
    ids = cli._round_named_node_ids(rec, "hypothesis:tgt")
    assert ids == ["hypothesis:tgt", "goal:g1", "experiment:a00-x-1"]
    # No record (a fixture, a dead tree) yields NOTHING -- a kid's --parent
    # alone is not an order.
    assert cli._round_named_node_ids(None, "hypothesis:tgt") == []
    # A non-id field never becomes a path.
    assert cli._round_named_node_ids({"target": "team/core"}, None) == []


# --------------------------------------------------------------------------
# hypothesis:a-rounds-named-node-set-is-its-dispatch-time-ids-never-a-kid-
# supplied-parent -- the named set is dispatch's, and a type no round may edit
# is never swept, whichever line named it.
# --------------------------------------------------------------------------

def test_kid_supplied_parent_never_widens_the_named_set():
    cli = _load_cli()
    rec = {"target": "hypothesis:tgt"}
    assert cli._round_named_node_ids(rec, "hypothesis:tgt") == ["hypothesis:tgt"]
    # The DH.386 widening: --parent named a prime/owner-only node.
    assert cli._round_named_node_ids(rec, "config:posts") == ["hypothesis:tgt"]
    assert cli._round_named_node_ids({"target": "hypothesis:tgt"},
                                     "doc:unified-head") == ["hypothesis:tgt"]


def test_round_committable_reads_the_config_cell_and_the_schema_written_by(tmp_path):
    import json
    cli = _load_cli()
    root = tmp_path / ".agi"
    (root / "context" / "schemas").mkdir(parents=True)
    (root / "config.json").write_text(json.dumps({"grid": {"round_commit": {
        "node_types": ["hypothesis", "experiment", "doc"],
        "never_node_ids": ["doc:unified-"],
    }}}))
    (root / "context" / "schemas" / "[town].md").write_text(
        "---\nname: town\nwritten_by: [prime_director, owner]\n---\n")
    # In the declared set.
    assert cli._round_committable(root, "hypothesis:tgt")
    # Never declared as round-editable: a goal, a config row, a doc prefix.
    assert not cli._round_committable(root, "goal:g5")
    assert not cli._round_committable(root, "config:posts")
    assert not cli._round_committable(root, "doc:unified-head")
    assert cli._round_committable(root, "doc:goals-preamble")
    # written_by in the type's OWN schema beats the cell's allowlist.
    assert not cli._round_committable(root, "town:local-maxxing")
    # An absent cell gates nothing: a fixture tree behaves as it did.
    (root / "config.json").write_text("{}")
    assert cli._round_committable(root, "goal:g5")
    assert cli._round_committable(root, "doc:unified-head")
    assert not cli._round_committable(root, "town:local-maxxing")


def test_own_node_paths_drops_a_named_goal_and_keeps_the_target(tmp_path):
    import json
    cli = _load_cli()
    root = tmp_path / ".agi"
    (root / "context" / "schemas").mkdir(parents=True)
    (root / "config.json").write_text(json.dumps({"grid": {"round_commit": {
        "node_types": ["hypothesis", "experiment"],
    }}}))
    for sub, nid in (("goal", "g5"), ("hypothesis", "tgt"),
                     ("experiment", "a00-x-1")):
        d = root / "nodes" / sub
        d.mkdir(parents=True, exist_ok=True)
        (d / f"{nid}.md").write_text(
            f"---\nid: {sub}:{nid}\ntype: {sub}\n---\n\nbody\n")
    paths = cli._round_own_node_paths(
        root, root, "experiment:a00-x-1", None,
        ["hypothesis:tgt", "goal:g5"])
    assert paths == {"nodes/experiment/a00-x-1.md",
                     "nodes/hypothesis/tgt.md"}, paths


def test_auto_commit_lands_the_named_target_node_and_refuses_the_rest(tmp_path):
    main = tmp_path / "main"
    main.mkdir()
    (main / ".agi" / "nodes" / "hypothesis").mkdir(parents=True)
    (main / ".agi" / "config.json").write_text("{}")
    _ggit(main, "init", "-q")
    _ggit(main, "checkout", "-q", "-b", "season/s1")
    _gitc(main, "base")

    br = "loop/named-target@s2"
    wt = tmp_path / "wt"
    r = _ggit(main, "worktree", "add", "-b", br, str(wt), "season/s1")
    assert r.returncode == 0, r.stderr
    wt_graph = wt / ".agi"
    (wt_graph / "nodes" / "hypothesis").mkdir(parents=True)
    (wt_graph / "config.json").write_text("{}")
    # The node the round's ORDERS name: a human slug carrying no agent id, so
    # `_round_scope_ok` alone refuses it -- it lands only via the named set.
    target = wt_graph / "nodes" / "hypothesis" / "a-kid-can-commit.md"
    target.write_text("---\nid: hypothesis:a-kid-can-commit\ntype: hypothesis\n"
                      "---\n\nbody\n")
    # A node nobody named, and the config cell: both must stay dirty.
    foreign = wt_graph / "nodes" / "hypothesis" / "not-named.md"
    foreign.write_text("---\nid: hypothesis:not-named\ntype: hypothesis\n"
                       "---\n\nbody\n")
    own = wt_graph / "nodes" / "experiment" / "a00-kid-1.md"
    own.parent.mkdir(parents=True, exist_ok=True)
    own.write_text("---\nid: experiment:a00-kid-1\ntype: experiment\n"
                   "---\n\nbody\n")
    (wt_graph / "config.json").write_text('{"paths": {}}')

    cli = _load_cli()
    rec = {"target": "hypothesis:a-kid-can-commit"}
    # PRE-FIX state: the named set is empty, so the named target is left
    # uncommitted and only the agent-id node lands. This is the measured
    # defect (TMM.212 item 1) the named set removes.
    assert cli._auto_commit_worktree(
        wt_graph, "a00-kid", "experiment:a00-kid-1", None, "pending", []) \
        is not None
    pre = _ggit(wt, "show", "--name-only", "--format=", "HEAD").stdout
    assert "nodes/experiment/a00-kid-1.md" in pre, pre
    assert "nodes/hypothesis/a-kid-can-commit.md" not in pre, pre

    named = cli._round_named_node_ids(rec, "hypothesis:a-kid-can-commit")
    # The kid's --parent carries the SAME id here (dispatch named it), so the
    # target still lands; a --parent DISPATCH did not name lands nothing.
    assert named == ["hypothesis:a-kid-can-commit"]
    root = cli._auto_commit_worktree(wt_graph, "a00-kid",
                                     "experiment:a00-kid-1", None,
                                     "pending", named)
    assert root is not None
    files = _ggit(wt, "show", "--name-only", "--format=", "HEAD").stdout
    assert "nodes/hypothesis/a-kid-can-commit.md" in files, files
    assert "nodes/hypothesis/not-named.md" not in files, files
    assert ".agi/config.json" not in files, files
    assert foreign.read_text().count("not-named") == 1
