"""Tests for bin/stitch.py — materialize level-3 nodes into a directory tree,
and verify the graph against the live engine tree without writing.

Scope mirrors test_level3.py's fixture style (temp engine repo + temp project
repo, `l3.build_node`/`l3.write_frontmatter` reused to mint realistic nodes)
plus the four drift categories `hyp:level3-node-anatomy` and this script's own
docstring name: missing payload, orphan files, duplicate payload_ref, and
stale contracts (mechanical `how` drift only — never `why`/`perf`/`security`).
"""

import importlib.util
import subprocess
import sys
from pathlib import Path

import pytest

BIN = Path(__file__).resolve().parents[1] / "bin"

_l3_spec = importlib.util.spec_from_file_location("level3_test", BIN / "level3.py")
l3 = importlib.util.module_from_spec(_l3_spec)
_l3_spec.loader.exec_module(l3)

_st_spec = importlib.util.spec_from_file_location("stitch_test", BIN / "stitch.py")
st = importlib.util.module_from_spec(_st_spec)
_st_spec.loader.exec_module(st)

STITCH_BIN = BIN / "stitch.py"


# --- fixtures ----------------------------------------------------------------

ENGINE_FILES = {
    "extensions/agi/bin/foo.py":
        "import os\n\n\ndef foo():\n    pass\n",
    "extensions/agi/src/pkg/__init__.py": "",
    "extensions/agi/src/pkg/bar.py":
        "import sys\n\n\ndef bar():\n    pass\n",
}


def write_engine_tree(root: Path, files: dict[str, str] | None = None) -> Path:
    merged = dict(ENGINE_FILES)
    if files:
        merged.update(files)
    for rel, content in merged.items():
        p = root / rel
        p.parent.mkdir(parents=True, exist_ok=True)
        p.write_text(content, encoding="utf-8")
    subprocess.run(["git", "init", "-q"], cwd=root, check=True)
    subprocess.run(["git", "add", "-A"], cwd=root, check=True)
    return root


@pytest.fixture()
def engine(tmp_path) -> Path:
    return write_engine_tree(tmp_path / "engine")


@pytest.fixture()
def project(tmp_path) -> Path:
    p = tmp_path / "project"
    (p / "nodes" / "build").mkdir(parents=True)
    return p


def mint_node(engine_root: Path, project_root: Path, rel_path: str,
              parent_id: str | None = None, id_suffix: str = "") -> str:
    """Mint a realistic, fresh (matching) level-3 node via level3.py's own
    build_node — never hand-crafted YAML — so fixtures look exactly like the
    real 73-node corpus. `id_suffix` lets a test mint a *second* node
    pointing at the same payload_ref, for the duplicate-ref case."""
    abs_path = engine_root / rel_path
    node_id, fm, body, _analysis = l3.build_node(rel_path, abs_path, parent_id)
    if id_suffix:
        node_id = f"{node_id}-{id_suffix}"
        fm = dict(fm)
        fm["id"] = node_id
    slug = node_id.split(":", 1)[-1]
    out_path = project_root / "nodes" / "build" / f"{slug}.md"
    l3.write_frontmatter(out_path, fm, body, origin="build-scan")
    return node_id


def mint_version_node(engine_root: Path, project_root: Path, rel_path: str,
                       version: int, supersedes: str | None = None,
                       base_node_id: str | None = None) -> str:
    """Mint a level-3 node stamped with an explicit `version`/`supersedes`,
    mirroring the real `origin: build-version` G6.3 convention: v1 keeps the
    plain `build:<slug>` id, v2+ gets `build:<slug>@vN`, and `supersedes`
    (never `parents`) names the previous version. `base_node_id` lets a test
    mint a second, unrelated node at the same payload_ref+version without
    colliding on the same output filename as an existing mint."""
    abs_path = engine_root / rel_path
    node_id, fm, body, _analysis = l3.build_node(rel_path, abs_path, None)
    if base_node_id is None:
        base_node_id = node_id
    versioned_id = base_node_id if version == 1 else f"{base_node_id}@v{version}"
    fm = dict(fm)
    fm["id"] = versioned_id
    fm["version"] = version
    if supersedes is not None:
        fm["supersedes"] = supersedes
    slug = versioned_id.split(":", 1)[-1].replace("@", "-")
    out_path = project_root / "nodes" / "build" / f"{slug}.md"
    origin = "build-version" if version > 1 else "build-scan"
    l3.write_frontmatter(out_path, fm, body, origin=origin)
    return versioned_id


def run(project: Path, engine: Path | None, *args):
    cmd = [sys.executable, str(STITCH_BIN), "--project", str(project)]
    if engine is not None:
        cmd += ["--engine-root", str(engine)]
    cmd += list(args)
    return subprocess.run(cmd, capture_output=True, text=True)


# --- materialize: the happy path --------------------------------------------


def test_parse_frontmatter_no_strip_precheck_behaviour_identical():
    """CLAIM (6d/SL7.17, hypothesis:l4-prepare-check-2-reads-the-index-blob...):
    `_parse_frontmatter` relies on `split_frontmatter` alone and drops the
    `strip().startswith("---")` prose pre-check (the exact shape SL7.11
    retired elsewhere). On every real node the behaviour is byte-identical:
    a well-formed node still parses; a leading-blank-line or marker-not-on-
    line-1 input (which the pre-check used to pass to the anchored splitter,
    which then refused it) still returns None."""
    ok = "---\nid: x\ntitle: t\n---\nbody\n"
    fm, body = st._parse_frontmatter(ok)
    assert fm == {"id": "x", "title": "t"}
    assert body == "body\n"
    # leading blank line before the marker: pre-check passed it, the anchored
    # splitter refused it -> None; with the pre-check gone, still None.
    assert st._parse_frontmatter("\n---\nid: x\ntitle: t\n---\n") is None
    # marker not on line 1, and an empty input: both None (unchanged).
    assert st._parse_frontmatter("no marker here\n") is None
    assert st._parse_frontmatter("") is None


def test_materialize_copies_every_payload_byte_identical(tmp_path, engine, project):
    for rel in ENGINE_FILES:
        mint_node(engine, project, rel)
    out = tmp_path / "out"

    stats = st.materialize(project, engine, out)

    assert stats["written"] == len(ENGINE_FILES)
    assert stats["skipped_missing"] == []
    assert stats["skipped_duplicate"] == []
    total_bytes = sum((engine / rel).stat().st_size for rel in ENGINE_FILES)
    assert stats["bytes_written"] == total_bytes
    for rel in ENGINE_FILES:
        assert (out / rel).read_bytes() == (engine / rel).read_bytes()


def test_materialize_preserves_relative_structure(tmp_path, engine, project):
    mint_node(engine, project, "extensions/agi/src/pkg/bar.py")
    out = tmp_path / "out"
    st.materialize(project, engine, out)
    assert (out / "extensions" / "agi" / "src" / "pkg" / "bar.py").is_file()


def test_materialize_zero_nodes_writes_nothing(tmp_path, engine, project):
    out = tmp_path / "out"
    stats = st.materialize(project, engine, out)
    assert stats["nodes_total"] == 0
    assert stats["written"] == 0


# --- materialize: safety -----------------------------------------------------


def test_materialize_refuses_nonempty_out_without_force(tmp_path, engine, project):
    mint_node(engine, project, "extensions/agi/bin/foo.py")
    out = tmp_path / "out"
    out.mkdir()
    (out / "stray.txt").write_text("pre-existing")

    with pytest.raises(st.StitchSafetyError):
        st.materialize(project, engine, out)
    # nothing was written on the refusal path
    assert not (out / "extensions").exists()


def test_materialize_force_writes_into_nonempty_out(tmp_path, engine, project):
    mint_node(engine, project, "extensions/agi/bin/foo.py")
    out = tmp_path / "out"
    out.mkdir()
    (out / "stray.txt").write_text("pre-existing")

    stats = st.materialize(project, engine, out, force=True)
    assert stats["written"] == 1
    assert (out / "stray.txt").read_text() == "pre-existing"  # untouched, not deleted
    assert (out / "extensions/agi/bin/foo.py").is_file()


def test_materialize_refuses_to_write_into_project_root(tmp_path, engine, project):
    mint_node(engine, project, "extensions/agi/bin/foo.py")
    with pytest.raises(st.StitchSafetyError):
        st.materialize(project, engine, project)


def test_materialize_refuses_to_write_into_engine_root(tmp_path, engine, project):
    mint_node(engine, project, "extensions/agi/bin/foo.py")
    with pytest.raises(st.StitchSafetyError):
        st.materialize(project, engine, engine)


def test_materialize_refuses_to_write_into_subdir_of_engine_root(tmp_path, engine, project):
    mint_node(engine, project, "extensions/agi/bin/foo.py")
    with pytest.raises(st.StitchSafetyError):
        st.materialize(project, engine, engine / "some" / "nested" / "dir")


# --- materialize: missing / duplicate payloads --------------------------------


def test_materialize_skips_missing_payload_and_reports_it(tmp_path, engine, project):
    node_id = mint_node(engine, project, "extensions/agi/bin/foo.py")
    (engine / "extensions/agi/bin/foo.py").unlink()  # node outlived the code
    out = tmp_path / "out"

    stats = st.materialize(project, engine, out)
    assert stats["written"] == 0
    assert stats["skipped_missing"] == [node_id]


def test_materialize_first_writer_wins_on_duplicate_ref(tmp_path, engine, project):
    id_a = mint_node(engine, project, "extensions/agi/bin/foo.py")
    id_b = mint_node(engine, project, "extensions/agi/bin/foo.py", id_suffix="dup")
    out = tmp_path / "out"

    stats = st.materialize(project, engine, out)
    # Exactly one of the two nodes wins the write; which one depends on
    # filename sort order (an implementation detail), not on id string order —
    # assert the invariant (one written, one skipped, no duplication) rather
    # than a specific winner.
    assert stats["written"] == 1
    assert stats["skipped_duplicate"] == [id_a] or stats["skipped_duplicate"] == [id_b]
    assert len(stats["skipped_duplicate"]) == 1
    assert (out / "extensions/agi/bin/foo.py").is_file()
    assert (out / "extensions/agi/bin/foo.py").read_bytes() == \
        (engine / "extensions/agi/bin/foo.py").read_bytes()


# --- verify: [1] missing_payload ---------------------------------------------


def test_verify_finds_missing_payload(tmp_path, engine, project):
    mint_node(engine, project, "extensions/agi/bin/foo.py")
    (engine / "extensions/agi/bin/foo.py").unlink()

    report = st.verify_tree(project, engine)
    assert len(report["missing_payload"]) == 1
    assert report["missing_payload"][0]["payload_ref"] == "extensions/agi/bin/foo.py"
    assert st.has_drift(report)


def test_verify_from_grid_does_not_call_an_unpublished_new_file_missing(project, engine, tmp_path):
    """goal:g6.1 — a file the graph holds but the engine has not received yet is
    unpublished, not missing, and `--publish` is the thing that resolves it.

    This is the deadlock the engine-first read created: `level3.py` mints a node
    for a file authored under `payloads/`, its bytes land in the grid, and then
    this gate refused to publish because the file was not in the engine tree —
    which publishing was the only way to fix. No flag reached it, so the
    sanctioned "write a new file under payloads/" workflow could record a file
    forever and ship it never.
    """
    rel = "extensions/agi/bin/brand_new.py"
    (engine / rel).write_text("import os\n\n\ndef brand_new():\n    pass\n")
    subprocess.run(["git", "add", "-A"], cwd=engine, check=True)
    for other in ENGINE_FILES:
        mint_node(engine, project, other)
    mint_node(engine, project, rel)
    _grid_project(project, engine)
    (engine / rel).unlink()          # in the graph, not yet in the engine tree

    # No drift at all, not merely an empty category 1: this is the assertion
    # that the publish would actually proceed rather than refuse.
    from_grid = st.verify_tree(project, engine, from_grid=True)
    assert from_grid["missing_payload"] == []
    assert not st.has_drift(from_grid)

    # The engine-tree claim is unweakened: asked about the tree, it still says
    # the file is absent. Only the grid-sourced question changed its answer.
    from_engine = st.verify_tree(project, engine)
    assert [m["payload_ref"] for m in from_engine["missing_payload"]] == [rel]


def test_verify_reads_retired_nodes_from_the_deprecated_dir(project, engine, tmp_path):
    """goal:g2.10 — a build node retired into `nodes/deprecated/build/` is still
    loaded, and still claims its `payload_ref`.

    It has to be. A retired node that stopped being read would turn its engine
    file into an `orphan_files` report — drift, and a refused publish — purely
    because the node was regrouped. Deprecation changes an address, not what the
    graph holds.
    """
    for rel in ENGINE_FILES:
        mint_node(engine, project, rel)

    target = "extensions/agi/bin/foo.py"
    before, _ = st.load_level3_nodes(project)
    assert target in {n.payload_ref for n in before}

    # Retire whichever file claims that payload_ref, without assuming its name.
    build_dir = project / "nodes" / "build"
    live = next(p for p in build_dir.glob("*.md") if target in p.read_text())
    retired_dir = project / "nodes" / "deprecated" / "build"
    retired_dir.mkdir(parents=True, exist_ok=True)
    live.rename(retired_dir / live.name)

    after, _ = st.load_level3_nodes(project)
    assert {n.node_id for n in after} == {n.node_id for n in before}
    assert target in {n.payload_ref for n in after}

    report = st.verify_tree(project, engine)
    assert report["orphan_files"] == []
    assert report["missing_payload"] == []
    assert not st.has_drift(report)


def test_verify_from_grid_still_reports_a_payload_neither_source_has(project, engine, tmp_path):
    """The category keeps its teeth: missing means *neither* source has the
    bytes. A node grid-committed before its payload existed is still drift."""
    rel = "extensions/agi/bin/foo.py"
    mint_node(engine, project, rel)
    _grid_project(project, engine)

    ghost = "extensions/agi/bin/never_existed.py"
    (engine / ghost).write_text("# transient\n")
    mint_node(engine, project, ghost)   # node minted, never grid-committed
    (engine / ghost).unlink()

    report = st.verify_tree(project, engine, from_grid=True)
    assert [m["payload_ref"] for m in report["missing_payload"]] == [ghost]
    assert st.has_drift(report)


def test_has_drift_false_when_all_categories_empty():
    clean = {"missing_payload": [], "orphan_files": [], "duplicate_payload_ref": {},
             "stale_contracts": [], "unreadable_contracts": []}
    assert not st.has_drift(clean)


def test_verify_clean_tree_has_no_drift(tmp_path, engine, project):
    for rel in ENGINE_FILES:
        mint_node(engine, project, rel)
    report = st.verify_tree(project, engine)
    assert report["missing_payload"] == []
    assert report["orphan_files"] == []
    assert report["duplicate_payload_ref"] == {}
    assert report["stale_contracts"] == []
    assert report["unreadable_contracts"] == []
    assert not st.has_drift(report)


# --- verify: [2] orphan_files -------------------------------------------------


def test_verify_finds_orphan_file(tmp_path, engine, project):
    # only mint a node for one of the three engine files
    mint_node(engine, project, "extensions/agi/bin/foo.py")

    report = st.verify_tree(project, engine)
    assert "extensions/agi/src/pkg/bar.py" in report["orphan_files"]
    assert "extensions/agi/bin/foo.py" not in report["orphan_files"]


def test_verify_orphan_scan_skips_when_engine_not_git_repo(tmp_path, project):
    engine = tmp_path / "plain_engine"
    for rel, content in ENGINE_FILES.items():
        p = engine / rel
        p.parent.mkdir(parents=True, exist_ok=True)
        p.write_text(content, encoding="utf-8")
    # deliberately no `git init` here

    report = st.verify_tree(project, engine)
    assert report["scope_files_total"] is None
    assert report["orphan_files"] == []
    assert any("not a git repo" in w for w in report["warnings"])


# --- verify: [3] duplicate_payload_ref -----------------------------------------


def test_verify_finds_duplicate_payload_ref(tmp_path, engine, project):
    id_a = mint_node(engine, project, "extensions/agi/bin/foo.py")
    id_b = mint_node(engine, project, "extensions/agi/bin/foo.py", id_suffix="dup")

    report = st.verify_tree(project, engine)
    dup = report["duplicate_payload_ref"]
    assert "extensions/agi/bin/foo.py" in dup
    assert set(dup["extensions/agi/bin/foo.py"]) == {id_a, id_b}


# --- verify/materialize: version chains (goal:g6.3) ---------------------------
# A v2 of a build node is a NEW node sharing the v1 node's `payload_ref`, with
# the previous version referenced via `supersedes` (never `parents`). A v1+v2
# pair therefore lands in the same `payload_ref` group the duplicate check
# above scans — these tests cover that a *provably ordered* chain is exempted
# from `duplicate_payload_ref`/drift, while every other shape in that group
# (a version collision, a broken `supersedes` link, a version gap) is not.


def test_verify_well_formed_chain_is_not_drift(tmp_path, engine, project):
    v1 = mint_version_node(engine, project, "extensions/agi/bin/foo.py", version=1)
    v2 = mint_version_node(engine, project, "extensions/agi/bin/foo.py", version=2,
                            supersedes=v1, base_node_id=v1)
    # cover the rest of the fixture engine tree too, so orphan_files (an
    # unrelated drift category) doesn't confound the has_drift() assertion.
    for rel in ENGINE_FILES:
        if rel != "extensions/agi/bin/foo.py":
            mint_node(engine, project, rel)

    report = st.verify_tree(project, engine)
    assert report["duplicate_payload_ref"] == {}
    assert report["version_chains"]["extensions/agi/bin/foo.py"] == [v1, v2]
    assert report["orphan_files"] == []
    assert not st.has_drift(report)


def test_verify_same_version_collision_is_still_drift(tmp_path, engine, project):
    v1 = mint_version_node(engine, project, "extensions/agi/bin/foo.py", version=1)
    v1b = mint_version_node(engine, project, "extensions/agi/bin/foo.py", version=1,
                             base_node_id="build:bin-foo-other")

    report = st.verify_tree(project, engine)
    dup = report["duplicate_payload_ref"]
    assert "extensions/agi/bin/foo.py" in dup
    assert set(dup["extensions/agi/bin/foo.py"]) == {v1, v1b}
    assert "extensions/agi/bin/foo.py" not in report["version_chains"]
    assert st.has_drift(report)


def test_verify_supersedes_missing_id_is_still_drift(tmp_path, engine, project):
    v1 = mint_version_node(engine, project, "extensions/agi/bin/foo.py", version=1)
    v2 = mint_version_node(engine, project, "extensions/agi/bin/foo.py", version=2,
                            supersedes="build:does-not-exist-anywhere", base_node_id=v1)

    report = st.verify_tree(project, engine)
    dup = report["duplicate_payload_ref"]
    assert "extensions/agi/bin/foo.py" in dup
    assert set(dup["extensions/agi/bin/foo.py"]) == {v1, v2}
    assert "extensions/agi/bin/foo.py" not in report["version_chains"]
    assert st.has_drift(report)


def test_verify_version_gap_is_still_drift(tmp_path, engine, project):
    """v1 -> v3 with no v2 anywhere in the group: v3's predecessor within the
    group is undefined (a gap leaves an orphan), so even a correct-looking
    supersedes link cannot make this a provable chain."""
    v1 = mint_version_node(engine, project, "extensions/agi/bin/foo.py", version=1)
    v3 = mint_version_node(engine, project, "extensions/agi/bin/foo.py", version=3,
                            supersedes=v1, base_node_id=v1)

    report = st.verify_tree(project, engine)
    assert "extensions/agi/bin/foo.py" in report["duplicate_payload_ref"]
    assert "extensions/agi/bin/foo.py" not in report["version_chains"]


def test_materialize_chain_writes_head_version(tmp_path, engine, project):
    v1 = mint_version_node(engine, project, "extensions/agi/bin/foo.py", version=1)
    v2 = mint_version_node(engine, project, "extensions/agi/bin/foo.py", version=2,
                            supersedes=v1, base_node_id=v1)
    out = tmp_path / "out"

    stats = st.materialize(project, engine, out)
    assert stats["written"] == 1
    assert stats["skipped_duplicate"] == []
    assert stats["chains_materialized"]["extensions/agi/bin/foo.py"] == v2
    assert (out / "extensions/agi/bin/foo.py").is_file()


def test_materialize_version_flag_selects_requested_version(tmp_path, engine, project):
    v1 = mint_version_node(engine, project, "extensions/agi/bin/foo.py", version=1)
    v2 = mint_version_node(engine, project, "extensions/agi/bin/foo.py", version=2,
                            supersedes=v1, base_node_id=v1)
    out = tmp_path / "out"

    stats = st.materialize(project, engine, out, version=1)
    assert stats["written"] == 1
    assert stats["chains_materialized"]["extensions/agi/bin/foo.py"] == v1
    assert stats["skipped_no_version"] == []


def test_materialize_version_flag_reports_missing_version(tmp_path, engine, project):
    mint_version_node(engine, project, "extensions/agi/bin/foo.py", version=1)
    out = tmp_path / "out"

    stats = st.materialize(project, engine, out, version=5)
    assert stats["written"] == 0
    assert stats["skipped_no_version"] == ["extensions/agi/bin/foo.py"]


def test_cli_materialize_version_flag(tmp_path, engine, project):
    v1 = mint_version_node(engine, project, "extensions/agi/bin/foo.py", version=1)
    mint_version_node(engine, project, "extensions/agi/bin/foo.py", version=2,
                       supersedes=v1, base_node_id=v1)
    out = tmp_path / "out"

    result = run(project, engine, "--out", str(out), "--version", "1")
    assert result.returncode == 0
    assert "written: 1 file" in result.stdout


def test_load_level3_nodes_coerces_non_integer_version(tmp_path, engine, project):
    node_id = mint_node(engine, project, "extensions/agi/bin/foo.py")
    slug = node_id.split(":", 1)[-1]
    node_path = project / "nodes" / "build" / f"{slug}.md"
    text = node_path.read_text(encoding="utf-8")
    assert "\nconfidence: 1.0\n" in text  # sanity: no version key present yet
    text = text.replace("confidence: 1.0\n", 'confidence: 1.0\nversion: "not-a-number"\n')
    node_path.write_text(text, encoding="utf-8")

    nodes, warnings = st.load_level3_nodes(project)
    assert len(nodes) == 1
    assert nodes[0].version == 1
    assert any("version" in w and "not-a-number" in w for w in warnings)


# --- verify: [4] stale_contracts -----------------------------------------------


def test_verify_finds_stale_contract_after_source_edit(tmp_path, engine, project):
    node_id = mint_node(engine, project, "extensions/agi/src/pkg/bar.py")

    report_before = st.verify_tree(project, engine)
    assert report_before["stale_contracts"] == []

    # code changes after the node was minted -> contract's mechanical `how`
    # half (imports) is now stale relative to the file it describes.
    bar = engine / "extensions/agi/src/pkg/bar.py"
    bar.write_text("import sys\nimport json\n\n\ndef bar():\n    pass\n", encoding="utf-8")

    report_after = st.verify_tree(project, engine)
    stale_ids = [s["node_id"] for s in report_after["stale_contracts"]]
    assert node_id in stale_ids
    entry = next(s for s in report_after["stale_contracts"] if s["node_id"] == node_id)
    assert "inputs" in entry["diff"]
    added_names = {e["name"] for e in entry["diff"]["inputs"]["added"]}
    assert "json" in added_names


def test_verify_ignores_model_authored_prose_drift(tmp_path, engine, project):
    """A later model pass filling why/perf/security must never register as
    contract staleness — those fields are free-text and not mechanically
    reproducible by design."""
    node_id = mint_node(engine, project, "extensions/agi/bin/foo.py")
    slug = node_id.split(":", 1)[-1]
    node_path = project / "nodes" / "build" / f"{slug}.md"
    text = node_path.read_text(encoding="utf-8")
    text = text.replace("why: TODO(model)", "why: some model-authored rationale")
    node_path.write_text(text, encoding="utf-8")

    report = st.verify_tree(project, engine)
    assert report["stale_contracts"] == []


def test_verify_unreadable_contract_reported_not_crashed(tmp_path, engine, project):
    node_id = mint_node(engine, project, "extensions/agi/bin/foo.py")
    slug = node_id.split(":", 1)[-1]
    node_path = project / "nodes" / "build" / f"{slug}.md"
    # strip the contract markers entirely -> no BUILD-CONTRACT block found
    text = node_path.read_text(encoding="utf-8")
    text = text.split("<!-- BUILD-CONTRACT:BEGIN")[0]
    node_path.write_text(text, encoding="utf-8")

    report = st.verify_tree(project, engine)
    unreadable_ids = [u["node_id"] for u in report["unreadable_contracts"]]
    assert node_id in unreadable_ids
    # this is a level3-scan node (mint_node's stamp) with an absent block —
    # a genuine generator failure, never eligible for the build-version
    # exemption below, regardless of the fact that the block is simply gone.
    not_derived_ids = [c["node_id"] for c in report["contracts_not_derived"]]
    assert node_id not in not_derived_ids
    assert st.has_drift(report)


# --- verify: [4] contracts_not_derived (build-version nodes, goal:g6.3) -------
# A `build-version` node (v2+ of a build node) is hand-authored prose per
# G6.3's convention — it never carries a BUILD-CONTRACT block, because
# level3.py owns that shape and has not been pointed at these nodes. Before
# this split, that absence read identically to a level3-scan node that lost
# its contract to a real bug: both landed in `unreadable_contracts`, which is
# drift. That made every build-version node a *permanent* false positive —
# concretely, this iteration's own v2 nodes would have kept `--strict`
# failing forever, for a reason that was never a defect in the first place.


def test_verify_build_version_node_missing_contract_is_not_drift(tmp_path, engine, project):
    v1 = mint_version_node(engine, project, "extensions/agi/bin/foo.py", version=1)
    v2 = mint_version_node(engine, project, "extensions/agi/bin/foo.py", version=2,
                            supersedes=v1, base_node_id=v1)
    # strip v2's contract block entirely, matching the real build-version
    # convention: hand-authored nodes carry no BUILD-CONTRACT block at all.
    slug = v2.split(":", 1)[-1].replace("@", "-")
    node_path = project / "nodes" / "build" / f"{slug}.md"
    text = node_path.read_text(encoding="utf-8")
    text = text.split("<!-- BUILD-CONTRACT:BEGIN")[0]
    node_path.write_text(text, encoding="utf-8")
    for rel in ENGINE_FILES:
        if rel != "extensions/agi/bin/foo.py":
            mint_node(engine, project, rel)

    report = st.verify_tree(project, engine)
    unreadable_ids = [u["node_id"] for u in report["unreadable_contracts"]]
    assert v2 not in unreadable_ids
    not_derived_ids = [c["node_id"] for c in report["contracts_not_derived"]]
    assert v2 in not_derived_ids
    assert not st.has_drift(report)


def test_verify_build_version_node_malformed_contract_is_still_drift(tmp_path, engine, project):
    v2 = mint_version_node(engine, project, "extensions/agi/bin/foo.py", version=2)
    slug = v2.split(":", 1)[-1].replace("@", "-")
    node_path = project / "nodes" / "build" / f"{slug}.md"
    text = node_path.read_text(encoding="utf-8")
    # markers and fence both present, but the YAML inside is corrupt — this
    # is "malformed", not "absent", and must not be swept into the exemption
    # just because the node happens to be origin: build-version.
    assert "parse_ok: true" in text
    text = text.replace("parse_ok: true", "parse_ok: [unterminated")
    node_path.write_text(text, encoding="utf-8")

    report = st.verify_tree(project, engine)
    unreadable_ids = [u["node_id"] for u in report["unreadable_contracts"]]
    assert v2 in unreadable_ids
    not_derived_ids = [c["node_id"] for c in report["contracts_not_derived"]]
    assert v2 not in not_derived_ids
    assert st.has_drift(report)


def test_verify_reads_contract_with_embedded_backtick_fence(tmp_path, engine, project):
    """Regression: a `how` field can itself contain a ``` fence (e.g. a
    write_text(f\"\"\"...```json...```...\"\"\") call site, truncated mid-string
    by level3.py's `_cap`). A naive "first ``` after ```yaml" scan stops at
    that embedded fence and truncates the contract mid-YAML. Real case:
    `build:bin-heal` in the actual agi-tree corpus. Extraction must bound on
    the BUILD-CONTRACT markers and take the *last* ``` inside that span."""
    rel = "extensions/agi/bin/tricky.py"
    src = engine / rel
    src.parent.mkdir(parents=True, exist_ok=True)
    src.write_text(
        "def f(rec):\n"
        '    ctx.write_text(f"""## Header\\n\\n```json\\n{rec}\\n```\\n\\nmore text ' +
        "x" * 200 + '""")\n',
        encoding="utf-8",
    )
    subprocess.run(["git", "add", "-A"], cwd=engine, check=True)

    node_id = mint_node(engine, project, rel)
    slug = node_id.split(":", 1)[-1]
    node_path = project / "nodes" / "build" / f"{slug}.md"
    text = node_path.read_text(encoding="utf-8")
    # confirm the fixture actually reproduces the embedded-fence shape
    assert "```json" in text

    nodes, warnings = st.load_level3_nodes(project)
    node = next(n for n in nodes if n.node_id == node_id)
    assert node.contract is not None, f"contract failed to parse: {node.contract_error}"
    assert node.contract.get("payload_ref") == rel

    report = st.verify_tree(project, engine)
    assert report["unreadable_contracts"] == []


def test_diff_contract_ignores_prose_fields_directly():
    stored = {"parse_ok": True, "inputs": [{"name": "os", "how": "`import os` at line 1",
                                             "why": "TODO(model)", "perf": "TODO(model)",
                                             "security": "TODO(model)"}],
              "outputs": []}
    fresh = {"parse_ok": True, "inputs": [{"name": "os", "how": "`import os` at line 1"}],
             "outputs": []}
    assert st.diff_contract(stored, fresh) is None


def test_diff_contract_reports_added_and_removed():
    stored = {"parse_ok": True,
              "inputs": [{"name": "os", "how": "`import os` at line 1"}], "outputs": []}
    fresh = {"parse_ok": True,
             "inputs": [{"name": "json", "how": "`import json` at line 1"}], "outputs": []}
    diff = st.diff_contract(stored, fresh)
    assert diff is not None
    assert diff["inputs"]["added"] == [{"name": "json", "how": "`import json` at line 1"}]
    assert diff["inputs"]["removed"] == [{"name": "os", "how": "`import os` at line 1"}]


# --- verify: graceful degradation, no crashes --------------------------------


def test_verify_engine_root_missing_degrades(tmp_path, engine, project):
    mint_node(engine, project, "extensions/agi/bin/foo.py")
    missing_engine = tmp_path / "does-not-exist"

    report = st.verify_tree(project, missing_engine)
    assert report["engine_readable"] is False
    assert report["missing_payload"] == []
    assert report["orphan_files"] == []
    assert report["stale_contracts"] == []
    assert any("missing or unreadable" in w for w in report["warnings"])


def test_verify_project_with_no_level3_dir_degrades(tmp_path, engine):
    empty_project = tmp_path / "empty_project"
    empty_project.mkdir()

    nodes, warnings = st.load_level3_nodes(empty_project)
    assert nodes == []
    assert warnings

    report = st.verify_tree(empty_project, engine)
    assert report["nodes_total"] == 0


def test_load_level3_nodes_skips_wrong_type_and_malformed(tmp_path, engine, project):
    mint_node(engine, project, "extensions/agi/bin/foo.py")
    (project / "nodes" / "build" / "not-level3.md").write_text(
        "---\nid: idea:stray\ntype: idea\n---\nbody\n", encoding="utf-8")
    (project / "nodes" / "build" / "garbage.md").write_text(
        "not frontmatter at all\n", encoding="utf-8")

    nodes, warnings = st.load_level3_nodes(project)
    assert len(nodes) == 1
    assert len(warnings) == 2


# --- CLI ---------------------------------------------------------------------


def test_cli_verify_exit_0_by_default_even_with_drift(tmp_path, engine, project):
    mint_node(engine, project, "extensions/agi/bin/foo.py")
    (engine / "extensions/agi/bin/foo.py").unlink()

    result = run(project, engine, "--verify")
    assert result.returncode == 0
    assert "missing_payload: 1" in result.stdout


def test_cli_verify_strict_exit_1_with_drift(tmp_path, engine, project):
    mint_node(engine, project, "extensions/agi/bin/foo.py")
    (engine / "extensions/agi/bin/foo.py").unlink()

    result = run(project, engine, "--verify", "--strict")
    assert result.returncode == 1


def test_cli_verify_strict_exit_0_when_clean(tmp_path, engine, project):
    for rel in ENGINE_FILES:
        mint_node(engine, project, rel)
    result = run(project, engine, "--verify", "--strict")
    assert result.returncode == 0


def test_cli_materialize_requires_out(tmp_path, engine, project):
    result = run(project, engine)
    assert result.returncode == 2
    assert "--out is required" in result.stderr


def test_cli_materialize_end_to_end(tmp_path, engine, project):
    mint_node(engine, project, "extensions/agi/bin/foo.py")
    out = tmp_path / "out"

    result = run(project, engine, "--out", str(out))
    assert result.returncode == 0
    assert (out / "extensions/agi/bin/foo.py").is_file()
    assert "written: 1 file" in result.stdout


def test_cli_materialize_refuses_engine_root_as_out(tmp_path, engine, project):
    mint_node(engine, project, "extensions/agi/bin/foo.py")
    result = run(project, engine, "--out", str(engine))
    assert result.returncode == 2
    assert "refusing to write" in result.stderr


# --- goal:g6.3 / goal:g6.1 — --from-grid and the guarded --publish -----------

_grid_spec = importlib.util.spec_from_file_location("grid_test", BIN / "grid.py")
grid = importlib.util.module_from_spec(_grid_spec)
_grid_spec.loader.exec_module(grid)


def _grid_project(project: Path, engine: Path) -> Path:
    """Turn the plain `project` fixture into a real grid-bearing graph repo and
    commit every node's payload into its ref, the way `commit --all` does."""
    subprocess.run(["git", "init", "-q"], cwd=project, check=True)
    (project / "agi-tree.config.json").write_text("{}")
    grid.cmd_commit(project, [], do_all=True, session=None, engine_root=engine)
    return project


def test_from_grid_matches_the_engine_tree_byte_for_byte(project, engine, tmp_path):
    """G6.3's falsifier in miniature: the two sources must agree exactly, or
    the version layer is not a source of truth and must not be called one."""
    mint_node(engine, project, "extensions/agi/bin/foo.py")
    mint_node(engine, project, "extensions/agi/src/pkg/bar.py")
    _grid_project(project, engine)

    a, b = tmp_path / "from-engine", tmp_path / "from-grid"
    st.materialize(project, engine, a)
    stats = st.materialize(project, engine, b, from_grid=True)

    assert stats["source"] == "grid"
    assert stats["written"] == 2 and not stats["skipped_missing"]
    for rel in ("extensions/agi/bin/foo.py", "extensions/agi/src/pkg/bar.py"):
        assert (a / rel).read_bytes() == (b / rel).read_bytes()


def test_from_grid_preserves_the_exec_bit(project, engine, tmp_path):
    """The half of S9 the live corpus exercises: 16 engine files are 100755,
    and the pre-S9 commit_file would have published every one of them 100644."""
    rel = "extensions/agi/bin/run.sh"
    (engine / rel).write_text("#!/bin/sh\necho hi\n")
    (engine / rel).chmod(0o755)
    mint_node(engine, project, rel)
    _grid_project(project, engine)

    out = tmp_path / "out"
    st.materialize(project, engine, out, from_grid=True)
    assert grid.git_mode(out / rel) == grid.GIT_MODE_EXEC


def test_from_grid_reads_the_graph_not_the_engine(project, engine, tmp_path):
    """goal:g6.1's arrow, stated as a test: once the payload is in the grid,
    deleting it from the engine tree changes nothing about what stitch writes."""
    rel = "extensions/agi/bin/foo.py"
    mint_node(engine, project, rel)
    _grid_project(project, engine)
    original = (engine / rel).read_bytes()
    (engine / rel).unlink()

    out = tmp_path / "out"
    stats = st.materialize(project, engine, out, from_grid=True)
    assert stats["written"] == 1
    assert (out / rel).read_bytes() == original


def test_from_grid_reports_a_node_with_no_grid_history(project, engine, tmp_path):
    """Never a silent fallback to disk: a node the grid does not hold is
    reported, because serving the engine file would make --from-grid a no-op
    that looks like a success."""
    mint_node(engine, project, "extensions/agi/bin/foo.py")
    subprocess.run(["git", "init", "-q"], cwd=project, check=True)
    (project / "agi-tree.config.json").write_text("{}")
    # deliberately no grid commit
    stats = st.materialize(project, engine, tmp_path / "out", from_grid=True)
    assert stats["written"] == 0
    assert stats["skipped_missing"] == ["build:bin-foo"]


def test_publish_refuses_without_from_grid(project, engine):
    with pytest.raises(st.StitchSafetyError, match="requires --from-grid"):
        st._guard_out_dir(engine, project, engine, publish=True, from_grid=False)


def test_plain_out_still_refuses_the_engine_repo(project, engine):
    with pytest.raises(st.StitchSafetyError, match="refusing to write"):
        st._guard_out_dir(engine, project, engine)


def test_out_never_writes_into_the_graph_repo_even_with_publish(project, engine):
    with pytest.raises(st.StitchSafetyError, match="graph repo"):
        st._guard_out_dir(project, project, engine, publish=True, from_grid=True)


def test_publish_refuses_a_dirty_engine_tree(project, engine):
    subprocess.run(["git", "-c", "user.email=t@t", "-c", "user.name=t",
                    "commit", "-qm", "init"], cwd=engine, check=True)
    assert st._git_is_clean(engine) is True
    st._guard_out_dir(engine, project, engine, publish=True, from_grid=True)  # ok

    (engine / "extensions/agi/bin/foo.py").write_text("import os\n# edited\n")
    with pytest.raises(st.StitchSafetyError, match="uncommitted changes"):
        st._guard_out_dir(engine, project, engine, publish=True, from_grid=True)


def test_publish_refuses_a_non_git_target(project, tmp_path):
    plain = tmp_path / "not-a-repo"
    plain.mkdir()
    with pytest.raises(st.StitchSafetyError, match="not a git repo"):
        st._guard_out_dir(plain, project, plain, publish=True, from_grid=True)


def test_publish_writes_the_graphs_bytes_into_the_engine(project, engine, tmp_path):
    """The full G6.1 loop end to end: edit in the graph, publish, and the
    engine file is what the graph said — with the edit never having been made
    in the engine repo at all."""
    rel = "extensions/agi/bin/foo.py"
    mint_node(engine, project, rel)
    _grid_project(project, engine)
    subprocess.run(["git", "-c", "user.email=t@t", "-c", "user.name=t",
                    "commit", "-qm", "init"], cwd=engine, check=True)

    edited = "import os\n\n\ndef foo():\n    return 'from the graph'\n"
    staged = project / grid.PAYLOAD_DIR / rel
    staged.parent.mkdir(parents=True, exist_ok=True)
    staged.write_text(edited)
    grid.cmd_commit(project, [], do_all=True, session=None, engine_root=engine)

    st.materialize(project, engine, engine, from_grid=True, publish=True)
    assert (engine / rel).read_text() == edited
    # ...and it is recoverable, which is the property the guard buys.
    subprocess.run(["git", "checkout", "--", "."], cwd=engine, check=True)
    assert (engine / rel).read_text() == ENGINE_FILES[rel]


def test_grid_version_materializes_a_chosen_version_not_the_tip(
        project, engine, tmp_path):
    """goal:g6.3's other untested case, in its own words: `stitch.py`
    materialising a chosen version rather than whichever is current."""
    rel = "extensions/agi/bin/foo.py"
    mint_node(engine, project, rel)
    _grid_project(project, engine)

    staged = project / grid.PAYLOAD_DIR / rel
    staged.parent.mkdir(parents=True, exist_ok=True)
    bodies = ["import os\n# v1\n", "import os\n# v2\n", "import os\n# v3\n"]
    # v1 was committed from the engine tree above; v2 and v3 come from the graph.
    for text in bodies[1:]:
        staged.write_text(text)
        grid.cmd_commit(project, [], do_all=True, session=None, engine_root=engine)

    for n, want in ((2, bodies[1]), (3, bodies[2])):
        out = tmp_path / f"v{n}"
        st.materialize(project, engine, out, from_grid=True, grid_version=n)
        assert (out / rel).read_text() == want

    tip = tmp_path / "tip"
    st.materialize(project, engine, tip, from_grid=True)
    assert (tip / rel).read_text() == bodies[2]


def test_grid_version_beyond_history_is_reported_not_silently_the_tip(
        project, engine, tmp_path):
    rel = "extensions/agi/bin/foo.py"
    node_id = mint_node(engine, project, rel)
    _grid_project(project, engine)
    stats = st.materialize(project, engine, tmp_path / "out",
                           from_grid=True, grid_version=9)
    assert stats["written"] == 0
    assert stats["skipped_missing"] == [node_id]
