

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
    import argparse
    args = argparse.Namespace(
        iter_n=1, agent_id="a00-x", verdict="proved", confidence=0.9,
        node_id="experiment:e1", parent="hypothesis:h1", notes="",
        next_edge=None, evidence_runs=["experiment:backer"],
        no_evidence_gate=False, owns=None, no_spawn_gate=False,
    )
    return graph, args


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
    # The agent's session record lives in the MAIN checkout (shared across
    # worktrees); the kid's node lives in the worktree.
    (graph / "sessions" / "iter-001" / "a00-p").mkdir(parents=True)
    (graph / "sessions" / "iter-001" / "a00-p" / "agent.json").write_text(
        '{"id": "a00-p", "node_id": "experiment:e1", '
        '"parent": "hypothesis:h1", "status": "running"}')

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
    (wt_graph / "nodes" / "experiment" / "backer.md").write_text(
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
    """A missing or corrupt manifest must not change cmd_done's exit code or
    drop the agent record -- the round still ends, still writes the record."""
    cli = _load_cli()
    import json as _json

    # missing manifest
    graph, args = _cmd_done_project(tmp_path)
    monkeypatch.setattr(cli, "_find_root", lambda: graph)
    assert cli.cmd_done(args) == 0
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
