"""Tests for bin/decompose-engine.py — engine census -> nodes/idea/ (TODO L19).

Scope mirrors test_snapshot_goals.py / test_snapshot_build_site.py: parsing,
pruning safety, and the `preserve` round-trip that H0i said was missing before
any new snapshot-shaped generator ships. See idea:engine-self-decomposition in
the graph repo for the design this script follows.
"""

import importlib.util
import subprocess
import sys
from pathlib import Path

import pytest
import yaml

BIN = Path(__file__).resolve().parents[1] / "bin" / "decompose-engine.py"
spec = importlib.util.spec_from_file_location("decompose_engine", BIN)
de = importlib.util.module_from_spec(spec)
spec.loader.exec_module(de)


# --- fixtures ----------------------------------------------------------------

ENGINE_FILES = {
    "extensions/agi/src/graph_core/__init__.py":
        '"""graph-core: generic node/edge primitives.\n\nMore detail here.\n"""\n'
        "from .node import Node\n",
    "extensions/agi/src/chain_engine/__init__.py":
        '"""Chain engine — virtual chain queries on top of graph-core."""\n',
    # a stray file directly in src/ must not itself become a package
    "extensions/agi/src/__init__.py": "",
    "extensions/agi/bin/cli.py":
        '#!/usr/bin/env python3\n"""cli.py — agent-facing completion CLI."""\n',
    "extensions/agi/bin/dispatch.py":
        '#!/usr/bin/env python3\n"""dispatch.py — spawn N agents in parallel."""\n',
    # a bin file with no docstring at all
    "extensions/agi/bin/nodoc.py":
        "import sys\nprint('hi')\n",
    "extensions/agi/driver.sh":
        "#!/bin/bash\n# driver.sh — orchestrates parallel agent dispatch.\n"
        "#\n# Second header line.\necho hi\n",
    "extensions/agi/hooks/cc-session-start.sh":
        "#!/bin/bash\n# cc-session-start.sh — SessionStart hook.\necho hi\n",
    "extensions/agi/lib/find-root.sh":
        "#!/bin/bash\n# find-root.sh — locate project root.\necho hi\n",
    # deliberately not a unit: a data file living alongside find-root.sh
    "extensions/agi/lib/agent-prompt.md":
        "# Not a code surface, must never become a unit.\n",
    "extensions/agi/scripts/migrate_to_sqlite.py":
        '#!/usr/bin/env python3\n"""One-shot migration: filesystem -> sqlite."""\n',
    "extensions/agi-bridge/index.ts":
        "/**\n * agi-bridge — Pi Extension\n *\n * Injects the map.\n */\n"
        "export function activate() {}\n",
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
    (p / "nodes" / "idea").mkdir(parents=True)
    return p


def run(project: Path, engine: Path | None, *args, goal_map: Path | None = None):
    cmd = [sys.executable, str(BIN), "--project", str(project)]
    if engine is not None:
        cmd += ["--engine-root", str(engine)]
    if goal_map is not None:
        cmd += ["--goal-map", str(goal_map)]
    cmd += list(args)
    return subprocess.run(cmd, capture_output=True, text=True)


def fm_of(path: Path) -> dict:
    return yaml.safe_load(path.read_text(encoding="utf-8").split("---", 2)[1]) or {}


def idea_nodes(project: Path) -> dict:
    return {fm_of(p)["id"]: (p, fm_of(p))
            for p in sorted((project / "nodes" / "idea").glob("*.md"))}


def write_node(project: Path, rel: str, fm: dict, body: str = "body"):
    path = project / "nodes" / rel
    path.parent.mkdir(parents=True, exist_ok=True)
    de.write_frontmatter(path, fm, body)
    return path


# --- 0. default engine root actually resolves to this script's own repo ----


def test_default_engine_root_points_at_this_repo():
    assert de.DEFAULT_ENGINE_ROOT == BIN.resolve().parents[3]
    assert (de.DEFAULT_ENGINE_ROOT / "extensions" / "agi" / "bin" /
            "decompose-engine.py").resolve() == BIN.resolve()


# --- 1. discovery: counts, kinds, exclusions ---------------------------------


def test_discovers_expected_units_with_kinds_and_scale(project, engine):
    r = run(project, engine)
    assert r.returncode == 0, r.stderr
    nodes = idea_nodes(project)
    ids = set(nodes)
    # goal:g6.8 widened discovery past src/+bin/. The pre-widening set must
    # still be minted exactly — nothing was traded away for the new coverage.
    assert {
        "idea:engine-graph-core", "idea:engine-chain-engine",
        "idea:engine-cli", "idea:engine-dispatch", "idea:engine-nodoc",
        "idea:engine-driver-sh", "idea:engine-cc-session-start",
        "idea:engine-find-root", "idea:engine-migrate-to-sqlite",
        "idea:engine-agi-bridge-index",
    } <= ids
    _path, fm = nodes["idea:engine-graph-core"]
    assert fm["unit_kind"] == "src_package"
    assert fm["unit_path"] == "extensions/agi/src/graph_core"
    assert fm["scale"] == "big"
    assert fm["type"] == "idea"
    assert fm["origin"] == "engine-decomp"

    _path, fm2 = nodes["idea:engine-cli"]
    assert fm2["unit_kind"] == "bin_script"
    assert fm2["unit_path"] == "extensions/agi/bin/cli.py"
    assert fm2["scale"] == "small"

    _path, fm3 = nodes["idea:engine-driver-sh"]
    assert fm3["unit_kind"] == "entry_point"


def test_co_location_alone_still_never_mints_a_unit(project, engine):
    """The property the old agent-prompt regression actually protected.

    That test asserted `agent-prompt.md` is never a unit, as the worked example
    of "a data file sitting beside an entry point must not become a unit merely
    by co-location". goal:g6.6/g6.8 then named agent-prompt.md and SKILL.md as
    the two highest-leverage prose surfaces the census MUST cover, so the
    example is superseded — but the rule is not. agent-prompt.md is a unit now
    because it has its own deliberate NAMED_ENTRY_POINTS tuple, never because
    discovery walks the directory it lives in. This asserts the rule directly
    instead of via an example that changed sides.
    """
    engine_root = engine
    stray = engine_root / "extensions" / "agi" / "lib" / "not-listed-anywhere.md"
    stray.write_text("# a data file nobody declared\n", encoding="utf-8")
    subprocess.run(["git", "add", "-A"], cwd=engine_root, check=True)

    run(project, engine)
    nodes = idea_nodes(project)
    assert not any("not-listed-anywhere" in nid for nid in nodes), \
        "a file in a censused directory must not become a unit by co-location"
    # ...and the declared sibling in that same directory still is one.
    assert any("find-root" in nid for nid in nodes)


def test_stray_src_init_is_not_its_own_package(project, engine):
    run(project, engine)
    nodes = idea_nodes(project)
    assert "idea:engine-src" not in nodes
    assert "idea:engine-__init__" not in nodes


# --- 2. docstring / header extraction ----------------------------------------


def test_docstring_extracted_for_py_sh_ts(project, engine):
    run(project, engine)
    nodes = idea_nodes(project)
    body_py = nodes["idea:engine-graph-core"][0].read_text()
    assert "generic node/edge primitives" in body_py
    body_sh = nodes["idea:engine-driver-sh"][0].read_text()
    assert "orchestrates parallel agent dispatch" in body_sh
    body_ts = nodes["idea:engine-agi-bridge-index"][0].read_text()
    assert "Injects the map." in body_ts


def test_missing_docstring_says_so_plainly_not_invented(project, engine):
    run(project, engine)
    body = idea_nodes(project)["idea:engine-nodoc"][0].read_text()
    assert "No module docstring or header comment was found" in body


# --- 3. missing / unreadable engine tree is a hard no-op ---------------------


def test_missing_engine_root_is_noop(project, tmp_path):
    missing = tmp_path / "does-not-exist"
    r = run(project, missing)
    assert r.returncode == 0
    assert "no-op" in r.stderr
    assert idea_nodes(project) == {}


def test_non_git_engine_root_is_noop(project, tmp_path):
    plain = tmp_path / "plain-dir"
    (plain / "extensions" / "agi" / "src").mkdir(parents=True)
    r = run(project, plain)
    assert r.returncode == 0
    assert "no-op" in r.stderr
    assert idea_nodes(project) == {}


def test_missing_engine_root_prunes_nothing(project, engine, tmp_path):
    run(project, engine)  # first, a real run populates nodes/idea/
    before = set(idea_nodes(project))
    assert before  # sanity: something was written

    missing = tmp_path / "vanished"
    r = run(project, missing)
    assert r.returncode == 0
    assert set(idea_nodes(project)) == before  # nothing pruned


# --- 4. dry-run writes nothing -----------------------------------------------


def test_dry_run_writes_nothing(project, engine):
    r = run(project, engine, "--dry-run")
    assert r.returncode == 0
    assert "DRY-RUN" in r.stdout
    assert idea_nodes(project) == {}


# --- 5. goal mapping: declared only, never guessed ---------------------------


def test_unit_with_no_goal_map_entry_is_parentless_and_flagged(
    project, engine, tmp_path
):
    """Must use an explicitly empty map, never the shipped default.

    This asserted against the real `decompose-engine.goalmap.json`, so it
    passed only while that file happened to be empty and broke the moment a
    mapping was declared. A test that reads production data is measuring the
    data, not the behaviour.
    """
    gm = tmp_path / "empty-goalmap.json"
    gm.write_text('{"mappings": {}}', encoding="utf-8")
    r = run(project, engine, goal_map=gm)
    assert r.returncode == 0
    _path, fm = idea_nodes(project)["idea:engine-graph-core"]
    assert "parents" not in fm
    assert "NO_GOAL: extensions/agi/src/graph_core" in r.stdout


def test_declared_goal_map_sets_parents(project, engine, tmp_path):
    gm = tmp_path / "goalmap.json"
    gm.write_text(
        '{"mappings": {"extensions/agi/src/graph_core": "goal:g6.1"}}',
        encoding="utf-8",
    )
    r = run(project, engine, goal_map=gm)
    assert r.returncode == 0
    _path, fm = idea_nodes(project)["idea:engine-graph-core"]
    assert fm["parents"] == ["goal:g6.1"]
    # a unit absent from the table is still parentless and flagged
    assert "NO_GOAL: extensions/agi/bin/cli.py" in r.stdout
    _path2, fm2 = idea_nodes(project)["idea:engine-cli"]
    assert "parents" not in fm2


# --- 6. idempotence -----------------------------------------------------------


def test_idempotent_byte_identical(project, engine):
    assert run(project, engine).returncode == 0
    first = {p.name: p.read_bytes()
             for p in sorted((project / "nodes" / "idea").glob("*.md"))}
    assert run(project, engine).returncode == 0
    second = {p.name: p.read_bytes()
              for p in sorted((project / "nodes" / "idea").glob("*.md"))}
    assert first == second
    assert first  # non-empty


# --------------------------------------------- H0i: re-run must not strip


def test_write_twice_round_trip_preserves_foreign_field(project, engine):
    """The required regression test: write, add a foreign field by hand
    (simulating another writer), write again, assert the field survives.

    Same defect class as H0i in snapshot-build-site.py / snapshot-goals.py:
    rebuilding frontmatter from scratch on a re-run silently dropped
    `next_edges` — chain structure — on 15 nodes of the live corpus.
    """
    assert run(project, engine).returncode == 0
    node_path, fm = idea_nodes(project)["idea:engine-graph-core"]

    text = node_path.read_text(encoding="utf-8")
    head, body = text.split("---", 2)[1], text.split("---", 2)[2]
    node_path.write_text(
        f"---{head}next_edges:\n  - hyp:graph-core-r1\n"
        f"embedding_coords: [0.1, 0.2]\n---{body}",
        encoding="utf-8",
    )

    assert run(project, engine).returncode == 0
    fm2 = fm_of(node_path)
    assert fm2["next_edges"] == ["hyp:graph-core-r1"]
    assert "embedding_coords" in fm2
    # owned fields are still regenerated fresh, not frozen by preserve
    assert fm2["unit_path"] == "extensions/agi/src/graph_core"
    assert fm2["title"] == "Engine surface: extensions/agi/src/graph_core"


# --- 7. prune reach: only our own stamp, never build-site / unstamped -------


def test_prune_removes_stale_engine_decomp_but_spares_others(project, engine):
    run(project, engine)
    stale = project / "nodes" / "idea" / "engine-vanished-module.md"
    de.write_frontmatter(
        stale,
        {"id": "idea:engine-vanished-module", "type": "idea",
         "unit_path": "extensions/agi/src/vanished_module"},
        "body", origin="engine-decomp",
    )
    build_site_node = write_node(
        project, "idea/domain-graph-core.md",
        {"id": "idea:domain-graph-core", "type": "idea", "origin": "build-site"},
    )
    unstamped_node = write_node(
        project, "idea/domain-exporters.md",
        {"id": "idea:domain-exporters", "type": "idea"},
    )
    r = run(project, engine)
    assert r.returncode == 0
    assert not stale.exists()
    assert build_site_node.exists()
    assert unstamped_node.exists()
    assert "removed stale" in r.stdout


# --- 8. STALE detection is advisory-only, never mutates ---------------------


def test_stale_flag_for_domain_node_with_no_matching_unit(project, engine):
    write_node(project, "idea/domain-exporters.md",
              {"id": "idea:domain-exporters", "type": "idea"})
    r = run(project, engine)
    assert r.returncode == 0
    assert "STALE:" in r.stdout
    assert "domain-exporters" in r.stdout
    # advisory only: the file is untouched
    assert (project / "nodes" / "idea" / "domain-exporters.md").exists()
    fm = fm_of(project / "nodes" / "idea" / "domain-exporters.md")
    assert fm["type"] == "idea"  # unchanged


def test_no_stale_flag_when_domain_node_matches_a_live_unit(project, engine):
    write_node(project, "idea/domain-graph-core.md",
              {"id": "idea:domain-graph-core", "type": "idea", "origin": "build-site"})
    r = run(project, engine)
    assert r.returncode == 0
    for line in r.stdout.splitlines():
        if line.startswith("STALE:"):
            assert "domain-graph-core" not in line


# --- 9. no project-local override door ---------------------------------------


def test_no_project_local_script_lookup_argument_exists():
    """The CLI surface intentionally has no way to point at a project-local
    copy of this script — that override mechanism is the H0 data-loss defect
    (see engine-self-decomposition §4.3). Only --project/--engine-root/
    --goal-map/--dry-run should exist.
    """
    r = subprocess.run([sys.executable, str(BIN), "--help"],
                       capture_output=True, text=True)
    assert r.returncode == 0
    for flag in ("--project", "--engine-root", "--goal-map", "--dry-run"):
        assert flag in r.stdout
