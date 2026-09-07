

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
