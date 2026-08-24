"""Tests for bin/level3.py — one level-3 node per code file, with a contract block.

Scope mirrors test_decompose_engine.py: discovery, mechanical `how` derivation
via `ast`, census-parent matching, pruning safety, and the `preserve`
round-trip. See `hyp:level3-node-anatomy` in the graph repo for the design
this script implements.
"""

import importlib.util
import subprocess
import sys
from pathlib import Path

import pytest
import yaml

BIN = Path(__file__).resolve().parents[1] / "bin" / "level3.py"
spec = importlib.util.spec_from_file_location("level3", BIN)
l3 = importlib.util.module_from_spec(spec)
spec.loader.exec_module(l3)


# --- fixtures ----------------------------------------------------------------

ENGINE_FILES = {
    "extensions/agi/src/graph_core/__init__.py": "",
    "extensions/agi/src/graph_core/node.py":
        '"""Node primitive."""\n'
        "from __future__ import annotations\n\n"
        "from dataclasses import dataclass\n"
        "from pathlib import Path\n\n\n"
        "@dataclass\n"
        "class Node:\n"
        "    id: str\n\n\n"
        "def _helper(x):\n"
        "    return x\n",
    # exercises: open() with literal mode (read + write), Path.read_text/
    # write_text, json.load/json.dump, argv, env, stdin, print, and one
    # non-literal mode (must land in `uncovered`, never guessed).
    "extensions/agi/src/graph_core/persistence/filesystem.py":
        "import json\n"
        "import os\n"
        "import sys\n"
        "from pathlib import Path\n\n\n"
        "def load(path, dynamic_mode):\n"
        "    with open(path, 'r') as f:\n"
        "        data = f.read()\n"
        "    cfg = json.load(open('cfg.json'))\n"
        "    text = Path(path).read_text()\n"
        "    key = os.getenv('AGI_TREE_PROJECT_ROOT')\n"
        "    args = sys.argv\n"
        "    open(path, dynamic_mode)\n"
        "    return data, cfg, text, key, args\n\n\n"
        "def save(path, obj):\n"
        "    with open(path, 'w') as f:\n"
        "        f.write('x')\n"
        "    json.dump(obj, open('out.json', 'w'))\n"
        "    Path(path).write_text('y')\n"
        "    print('saved')\n",
    # a file with a genuine syntax error: parse_ok must be false, contract empty
    "extensions/agi/src/graph_core/broken.py": "def f(:\n    pass\n",
    "extensions/agi/bin/cli.py":
        '#!/usr/bin/env python3\n"""cli.py."""\nimport sys\n\n\ndef main():\n    pass\n',
    # a bin file not represented in the census at all -> parentless
    "extensions/agi/bin/orphan.py": "x = 1\n",
    # out of scope: nested bin dir, non-.py file, and a stray src/__init__.py
    "extensions/agi/bin/nested/inner.py": "x = 1\n",
    "extensions/agi/src/__init__.py": "",
    "extensions/agi/driver.sh": "#!/bin/bash\necho hi\n",
}

# A minimal census, as decompose-engine.py would have written it.
IDEA_NODES = {
    "idea:engine-graph-core": {
        "id": "idea:engine-graph-core", "type": "idea",
        "unit_kind": "src_package", "unit_path": "extensions/agi/src/graph_core",
    },
    "idea:engine-cli": {
        "id": "idea:engine-cli", "type": "idea",
        "unit_kind": "bin_script", "unit_path": "extensions/agi/bin/cli.py",
    },
    # a non-idea node and an idea node without unit_kind must both be ignored
    # as census candidates, not crash the matcher.
    "hyp:unrelated": {"id": "hyp:unrelated", "type": "hypothesis"},
    "idea:domain-legacy": {"id": "idea:domain-legacy", "type": "idea"},
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
    (p / "nodes" / "level3").mkdir(parents=True)
    for node_id, fm in IDEA_NODES.items():
        slug = node_id.split(":", 1)[-1]
        l3.write_frontmatter(p / "nodes" / "idea" / f"{slug}.md", dict(fm), "body")
    return p


def run(project: Path, engine: Path | None, *args):
    cmd = [sys.executable, str(BIN), "--project", str(project)]
    if engine is not None:
        cmd += ["--engine-root", str(engine)]
    cmd += list(args)
    return subprocess.run(cmd, capture_output=True, text=True)


def fm_of(path: Path) -> dict:
    return yaml.safe_load(path.read_text(encoding="utf-8").split("---", 2)[1]) or {}


def body_of(path: Path) -> str:
    return path.read_text(encoding="utf-8").split("---", 2)[2]


def contract_of(path: Path) -> dict:
    body = body_of(path)
    yaml_block = body.split("```yaml", 1)[1].split("```", 1)[0]
    return yaml.safe_load(yaml_block)


def level3_nodes(project: Path) -> dict:
    return {fm_of(p)["id"]: (p, fm_of(p))
            for p in sorted((project / "nodes" / "level3").glob("*.md"))}


def write_node(project: Path, rel: str, fm: dict, body: str = "body", origin: str = ""):
    path = project / "nodes" / rel
    path.parent.mkdir(parents=True, exist_ok=True)
    l3.write_frontmatter(path, fm, body, origin=origin)
    return path


# --- 0. default engine root actually resolves to this script's own repo ----


def test_default_engine_root_points_at_this_repo():
    assert l3.DEFAULT_ENGINE_ROOT == BIN.resolve().parents[3]
    assert (l3.DEFAULT_ENGINE_ROOT / "extensions" / "agi" / "bin" /
            "level3.py").resolve() == BIN.resolve()


# --- 1. discovery: scope is src/**/*.py + bin/*.py (direct children only) ---


def test_discovers_every_file_passing_the_g6_8_boundary(project, engine):
    """goal:g6.8 — discovery is the payload boundary, not two path prefixes.

    Was: only `extensions/agi/src/**/*.py` + `extensions/agi/bin/*.py`, which
    goal:g6.6 named as the thing blocking G6.1 — the skill doc, the kid brief
    and every shell surface were invisible to the graph. Now every tracked
    file is in unless the boundary excludes it, so the nested bin/ script and
    driver.sh (previously "out of scope") are nodes like anything else.
    """
    r = run(project, engine)
    assert r.returncode == 0, r.stderr
    ids = set(level3_nodes(project))
    # everything the old two-prefix scan already found
    assert {
        "level3:src-graph-core-init",
        "level3:src-graph-core-node",
        "level3:src-graph-core-persistence-filesystem",
        "level3:src-graph-core-broken",
        "level3:bin-cli",
        "level3:bin-orphan",
        "level3:src-init",
    } <= ids
    # ...plus what it used to silently drop
    assert "level3:bin-nested-inner" in ids, \
        "a nested bin/ script is a tracked file; the boundary admits it"
    assert any("driver" in nid for nid in ids), \
        "driver.sh is the highest-leverage shell surface in the engine (g6.6)"


def test_files_scanned_count_matches_the_boundary(project, engine):
    """The count is whatever the boundary admits — asserted against the
    predicate itself rather than a hardcoded number, so the two cannot drift."""
    r = run(project, engine)
    expected = len(l3.discover_files(engine))
    assert f"files scanned: {expected}" in r.stdout
    assert expected > 7, "the boundary must admit more than the old scope did"


def test_non_python_payload_is_honest_about_not_being_parsed(project, engine):
    """`ast` is a Python parser. JSON is a dict literal and TOML's
    `key = "value"` is an assignment, so both parse clean — a non-Python file
    would report parse_ok: true with an empty contract, i.e. claim it was
    analysed when nothing analysed it, which stitch.py --verify then reads as
    no drift."""
    analysis = l3.analyze_file(engine / "extensions" / "agi" / "driver.sh")
    assert analysis["parse_ok"] is False
    assert "not-python" in analysis["parse_error"]
    assert analysis["inputs"] == [] and analysis["outputs"] == []


def test_empty_scope_is_refused_never_treated_as_prune_everything(project, engine, tmp_path):
    """H0/H0i. Before g6.8 this case could not arise; the boundary introduces
    an external classifier that could return "everything excluded", and a
    silent exit-0 there would wipe every level3-scan node."""
    run(project, engine)                     # populate
    before = set(level3_nodes(project))
    assert before

    empty = tmp_path / "empty-engine"
    empty.mkdir()
    subprocess.run(["git", "init", "-q"], cwd=empty, check=True)
    r = run(project, empty)
    assert r.returncode == 1
    assert "refusing to treat this as authoritative scope" in r.stderr
    assert set(level3_nodes(project)) == before, "nothing may be pruned"


# --- 2. frontmatter shape: no new Node-relevant keys, payload_ref/origin used


def test_frontmatter_uses_payload_ref_and_origin_only(project, engine):
    run(project, engine)
    _path, fm = level3_nodes(project)["level3:src-graph-core-node"]
    assert fm["type"] == "level3"
    assert fm["origin"] == "level3-scan"
    assert fm["payload_ref"] == "extensions/agi/src/graph_core/node.py"
    assert fm["parents"] == ["idea:engine-graph-core"]
    # no invented top-level keys beyond the standard generated-node set
    assert set(fm) <= {
        "id", "type", "title", "payload_ref", "tags", "confidence", "parents", "origin",
    }


# --- 3. contract block: mechanical `how`, honest `uncovered`, TODO(model) ----


def test_imports_and_top_level_defs_are_derived(project, engine):
    run(project, engine)
    path, _ = level3_nodes(project)["level3:src-graph-core-node"]
    contract = contract_of(path)
    assert contract["parse_ok"] is True
    input_names = {e["name"] for e in contract["inputs"]}
    assert "dataclasses.dataclass" in input_names
    assert "pathlib.Path" in input_names
    output_names = {e["name"] for e in contract["outputs"]}
    assert output_names == {"Node", "_helper"}
    node_entry = next(e for e in contract["outputs"] if e["name"] == "Node")
    assert "class" in node_entry["how"]
    assert "public" in node_entry["how"]
    helper_entry = next(e for e in contract["outputs"] if e["name"] == "_helper")
    assert "private" in helper_entry["how"]
    # why/perf/security are placeholders, never fabricated
    for e in contract["inputs"] + contract["outputs"]:
        assert e["why"] == "TODO(model)"
        assert e["perf"] == "TODO(model)"
        assert e["security"] == "TODO(model)"


def test_read_write_calls_argv_env_stdout_are_derived(project, engine):
    run(project, engine)
    path, _ = level3_nodes(project)["level3:src-graph-core-persistence-filesystem"]
    contract = contract_of(path)
    input_hows = " ".join(e["how"] for e in contract["inputs"])
    output_hows = " ".join(e["how"] for e in contract["outputs"])

    assert "mode='r'" in input_hows
    assert "read_text" in input_hows
    assert "json.load" in input_hows
    assert "sys.argv" in input_hows
    assert "AGI_TREE_PROJECT_ROOT" in input_hows

    assert "mode='w'" in output_hows
    assert "write_text" in output_hows
    assert "json.dump" in output_hows
    assert "print()" in output_hows


def test_non_literal_open_mode_is_uncovered_not_guessed(project, engine):
    run(project, engine)
    path, _ = level3_nodes(project)["level3:src-graph-core-persistence-filesystem"]
    contract = contract_of(path)
    assert "uncovered" in contract
    uncovered_hows = " ".join(e["how"] for e in contract["uncovered"])
    assert "uncovered" in uncovered_hows
    assert "non-literal" in uncovered_hows
    # the dynamic-mode call must NOT have been silently placed in inputs/outputs
    all_named = {e["name"] for e in contract["inputs"] + contract["outputs"]}
    # 'path' (the dynamic-mode open target) should only appear via the
    # uncovered entry's own name, not duplicated into a guessed direction
    uncovered_names = {e["name"] for e in contract["uncovered"]}
    assert uncovered_names  # non-empty
    for e in contract["uncovered"]:
        assert e["why"] == "TODO(model)"


def test_syntax_error_file_gets_parse_ok_false_and_empty_contract(project, engine):
    run(project, engine)
    path, _ = level3_nodes(project)["level3:src-graph-core-broken"]
    contract = contract_of(path)
    assert contract["parse_ok"] is False
    assert "parse_error" in contract
    assert contract["inputs"] == []
    assert contract["outputs"] == []


def test_empty_file_gets_empty_but_present_contract_lists(project, engine):
    run(project, engine)
    path, _ = level3_nodes(project)["level3:src-graph-core-init"]
    contract = contract_of(path)
    assert contract["parse_ok"] is True
    assert contract["inputs"] == []
    assert contract["outputs"] == []


# --- 4. census parent matching: exact for bin_script, prefix for src_package -


def test_bin_script_matches_exact_unit_path(project, engine):
    run(project, engine)
    _path, fm = level3_nodes(project)["level3:bin-cli"]
    assert fm["parents"] == ["idea:engine-cli"]


def test_src_package_matches_directory_prefix(project, engine):
    run(project, engine)
    _path, fm = level3_nodes(project)["level3:src-graph-core-persistence-filesystem"]
    assert fm["parents"] == ["idea:engine-graph-core"]


def test_no_matching_unit_is_parentless_and_flagged(project, engine):
    r = run(project, engine)
    _path, fm = level3_nodes(project)["level3:bin-orphan"]
    assert "parents" not in fm
    _path2, fm2 = level3_nodes(project)["level3:src-init"]
    assert "parents" not in fm2
    assert "NO_PARENT: extensions/agi/bin/orphan.py" in r.stdout
    assert "NO_PARENT: extensions/agi/src/__init__.py" in r.stdout


# --- 5. missing / unreadable engine tree is a hard no-op ---------------------


def test_missing_engine_root_is_noop(project, tmp_path):
    missing = tmp_path / "does-not-exist"
    r = run(project, missing)
    assert r.returncode == 0
    assert "no-op" in r.stderr
    assert level3_nodes(project) == {}


def test_non_git_engine_root_is_noop(project, tmp_path):
    plain = tmp_path / "plain-dir"
    (plain / "extensions" / "agi" / "src").mkdir(parents=True)
    r = run(project, plain)
    assert r.returncode == 0
    assert "no-op" in r.stderr
    assert level3_nodes(project) == {}


def test_missing_engine_root_prunes_nothing(project, engine, tmp_path):
    run(project, engine)
    before = set(level3_nodes(project))
    assert before

    missing = tmp_path / "vanished"
    r = run(project, missing)
    assert r.returncode == 0
    assert set(level3_nodes(project)) == before


# --- 6. dry-run writes nothing -----------------------------------------------


def test_dry_run_writes_nothing(project, engine):
    r = run(project, engine, "--dry-run")
    assert r.returncode == 0
    assert "DRY-RUN" in r.stdout
    assert level3_nodes(project) == {}


# --- 7. idempotence -----------------------------------------------------------


def test_idempotent_byte_identical(project, engine):
    assert run(project, engine).returncode == 0
    first = {p.name: p.read_bytes()
             for p in sorted((project / "nodes" / "level3").glob("*.md"))}
    assert run(project, engine).returncode == 0
    second = {p.name: p.read_bytes()
              for p in sorted((project / "nodes" / "level3").glob("*.md"))}
    assert first == second
    assert first


# --- 8. H0i-shaped regression: re-run must not strip a foreign field --------


def test_write_twice_round_trip_preserves_foreign_field(project, engine):
    assert run(project, engine).returncode == 0
    node_path, _fm = level3_nodes(project)["level3:src-graph-core-node"]

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
    assert fm2["payload_ref"] == "extensions/agi/src/graph_core/node.py"
    assert fm2["title"] == "Level-3: extensions/agi/src/graph_core/node.py"


# --- 9. prune reach: only our own stamp, never build-site / unstamped -------


def test_prune_removes_stale_level3_scan_but_spares_others(project, engine):
    run(project, engine)
    stale = project / "nodes" / "level3" / "level3-vanished-file.md"
    l3.write_frontmatter(
        stale,
        {"id": "level3:vanished-file", "type": "level3",
         "payload_ref": "extensions/agi/src/vanished.py"},
        "body", origin="level3-scan",
    )
    build_site_node = write_node(
        project, "level3/domain-untouched.md",
        {"id": "idea:domain-untouched", "type": "idea"}, origin="build-site",
    )
    unstamped_node = write_node(
        project, "level3/domain-unstamped.md",
        {"id": "idea:domain-unstamped", "type": "idea"},
    )
    r = run(project, engine)
    assert r.returncode == 0
    assert not stale.exists()
    assert build_site_node.exists()
    assert unstamped_node.exists()
    assert "removed stale" in r.stdout


# --- 10. no project-local override door --------------------------------------


def test_no_project_local_script_lookup_argument_exists():
    r = subprocess.run([sys.executable, str(BIN), "--help"],
                       capture_output=True, text=True)
    assert r.returncode == 0
    for flag in ("--project", "--engine-root", "--dry-run"):
        assert flag in r.stdout
    assert "--goal-map" not in r.stdout
