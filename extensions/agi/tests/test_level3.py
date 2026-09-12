"""Tests for bin/level3.py — one level-3 node per code file, with a contract block.

Scope mirrors test_decompose_engine.py: discovery, mechanical `how` derivation
via `ast`, census-parent matching, pruning safety, and the `preserve`
round-trip. See `hyp:level3-node-anatomy` in the graph repo for the design
this script implements.
"""

import ast
import importlib.util
import os
import subprocess
import sys
from pathlib import Path

import pytest
import yaml

BIN = Path(__file__).resolve().parents[1] / "bin" / "level3.py"
spec = importlib.util.spec_from_file_location("level3", BIN)
l3 = importlib.util.module_from_spec(spec)
spec.loader.exec_module(l3)

sys.path.insert(0, str(Path(__file__).resolve().parents[1] / "src"))
from graph_core import identity  # noqa: E402


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
    (p / "nodes" / "build").mkdir(parents=True)
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
            for p in sorted((project / "nodes" / "build").glob("*.md"))}


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
        "build:src-graph-core-init",
        "build:src-graph-core-node",
        "build:src-graph-core-persistence-filesystem",
        "build:src-graph-core-broken",
        "build:bin-cli",
        "build:bin-orphan",
        "build:src-init",
    } <= ids
    # ...plus what it used to silently drop
    assert "build:bin-nested-inner" in ids, \
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
    _path, fm = level3_nodes(project)["build:src-graph-core-node"]
    assert fm["type"] == "build"
    assert fm["origin"] == "build-scan"
    assert fm["payload_ref"] == "extensions/agi/src/graph_core/node.py"
    assert fm["parents"] == ["idea:engine-graph-core"]
    # no invented top-level keys beyond the standard generated-node set.
    # `mint_id` joined that set under goal:s14 — it is assigned by the shared
    # `write_frontmatter`, at creation, for every generator alike, which is
    # exactly the "not a level3-specific invention" property this test guards.
    assert set(fm) <= {
        "id", "mint_id", "type", "build_kind", "title", "payload_ref", "tags",
        "confidence", "parents", "origin",
    }
    assert identity.is_valid_mint_id(fm["mint_id"])


# --- 3. contract block: mechanical `how`, honest `uncovered`, TODO(model) ----


def test_imports_and_top_level_defs_are_derived(project, engine):
    run(project, engine)
    path, _ = level3_nodes(project)["build:src-graph-core-node"]
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
    path, _ = level3_nodes(project)["build:src-graph-core-persistence-filesystem"]
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
    path, _ = level3_nodes(project)["build:src-graph-core-persistence-filesystem"]
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
    path, _ = level3_nodes(project)["build:src-graph-core-broken"]
    contract = contract_of(path)
    assert contract["parse_ok"] is False
    assert "parse_error" in contract
    assert contract["inputs"] == []
    assert contract["outputs"] == []


def test_empty_file_gets_empty_but_present_contract_lists(project, engine):
    run(project, engine)
    path, _ = level3_nodes(project)["build:src-graph-core-init"]
    contract = contract_of(path)
    assert contract["parse_ok"] is True
    assert contract["inputs"] == []
    assert contract["outputs"] == []


# --- 4. census parent matching: exact for bin_script, prefix for src_package -


def test_bin_script_matches_exact_unit_path(project, engine):
    run(project, engine)
    _path, fm = level3_nodes(project)["build:bin-cli"]
    assert fm["parents"] == ["idea:engine-cli"]


def test_src_package_matches_directory_prefix(project, engine):
    run(project, engine)
    _path, fm = level3_nodes(project)["build:src-graph-core-persistence-filesystem"]
    assert fm["parents"] == ["idea:engine-graph-core"]


def test_no_matching_unit_is_parentless_and_flagged(project, engine):
    r = run(project, engine)
    _path, fm = level3_nodes(project)["build:bin-orphan"]
    assert "parents" not in fm
    _path2, fm2 = level3_nodes(project)["build:src-init"]
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
             for p in sorted((project / "nodes" / "build").glob("*.md"))}
    assert run(project, engine).returncode == 0
    second = {p.name: p.read_bytes()
              for p in sorted((project / "nodes" / "build").glob("*.md"))}
    assert first == second
    assert first


# --- 8. H0i-shaped regression: re-run must not strip a foreign field --------


def test_write_twice_round_trip_preserves_foreign_field(project, engine):
    assert run(project, engine).returncode == 0
    node_path, _fm = level3_nodes(project)["build:src-graph-core-node"]

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
    assert fm2["title"] == "Build: extensions/agi/src/graph_core/node.py"


# --- 9. prune reach: only our own stamp, never build-site / unstamped -------


def test_prune_removes_stale_level3_scan_but_spares_others(project, engine):
    run(project, engine)
    stale = project / "nodes" / "build" / "level3-vanished-file.md"
    l3.write_frontmatter(
        stale,
        {"id": "build:vanished-file", "type": "build",
         "payload_ref": "extensions/agi/src/vanished.py"},
        "body", origin="build-scan",
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


def test_a_node_stamped_with_the_LEGACY_origin_is_never_pruned(project, engine):
    """The asymmetry that makes the level3 -> build rename survivable.

    Readers accept both names; the pruner recognises only the current
    `ORIGIN`. A straggler still stamped `level3-scan` is therefore *left
    alone* — "this scan does not recognise it" and "this node is stale" are
    different statements, and only the second licenses deletion.

    Pruning on the legacy stamp is precisely how a half-applied rename turns
    into H0i: `level3.py` would stop recognising ~185 nodes as its own output
    and delete every one of them on the next run. This test is the guard on
    that, so the two rules can never quietly converge again.
    """
    run(project, engine)
    legacy = project / "nodes" / "build" / "legacy-stamped-file.md"
    l3.write_frontmatter(
        legacy,
        {"id": "level3:legacy-file", "type": "level3",
         "payload_ref": "extensions/agi/src/legacy.py"},
        "body", origin="level3-scan",
    )
    r = run(project, engine)
    assert r.returncode == 0
    assert legacy.exists(), (
        "a node stamped with the pre-rename origin was pruned; the pruner must "
        "only ever remove nodes carrying its own current ORIGIN"
    )
    assert l3.ORIGIN == "build-scan"
    assert l3.LEGACY_ORIGIN == "level3-scan"
    assert l3.ORIGIN != l3.LEGACY_ORIGIN


def test_build_kind_is_derived_from_the_payload_suffix():
    """`code` vs `prose` answers without a human adjudicating (G6.8)."""
    for path in ("bin/x.py", "lib/y.sh", "src/z.ts", "a/b.js"):
        assert l3.build_kind_for(path) == "code", path
    for path in ("README.md", "c.json", "d.toml", "e.sql", "Makefile"):
        assert l3.build_kind_for(path) == "prose", path


# --- 10. no project-local override door --------------------------------------


def test_no_project_local_script_lookup_argument_exists():
    r = subprocess.run([sys.executable, str(BIN), "--help"],
                       capture_output=True, text=True)
    assert r.returncode == 0
    for flag in ("--project", "--engine-root", "--dry-run"):
        assert flag in r.stdout
    assert "--goal-map" not in r.stdout


def test_entry_point_units_can_be_matched_as_parents(project, engine):
    """Five entry_point census units existed and were correct — driver.sh,
    find-root.sh, cc-session-start.sh, agi-bridge/index.ts,
    migrate_to_sqlite.py — while load_census_units() silently dropped the kind
    and find_parent()'s prefix branch could never match a single file. Those
    files reported NO_PARENT with their unit sitting unread in the graph, and
    it was invisible because a missing parent looks identical to a missing
    unit. They are the exact surfaces goal:g6.6 calls highest-leverage.
    """
    units = [{"node_id": "idea:engine-driver-sh",
              "unit_path": "extensions/agi/driver.sh",
              "unit_kind": "entry_point"}]
    assert l3.find_parent("extensions/agi/driver.sh", units) == "idea:engine-driver-sh"
    assert l3.find_parent("extensions/agi/other.sh", units) is None

    existing = {"idea:engine-driver-sh": {"fm": {
        "type": "idea", "unit_kind": "entry_point",
        "unit_path": "extensions/agi/driver.sh"}}}
    assert [u["node_id"] for u in l3.load_census_units(existing)] == \
        ["idea:engine-driver-sh"]


# --- goal:g2.10 — the authored half of a body survives the scan -----------


def _contract_of(body):
    contract, err = l3.extract_contract(body)
    assert err is None, err
    return contract


def test_unfilled_entries_are_todo():
    """The baseline the corpus is in: nothing filled, everything TODO."""
    out = l3._fill_entries([{"name": "f", "how": "at line 1"}], None)
    assert out == [{"name": "f", "how": "at line 1", "why": "TODO(model)",
                    "perf": "TODO(model)", "security": "TODO(model)"}]


def test_authored_fields_carry_over():
    """8,034 fields across 190 nodes read TODO(model) and 0 were ever filled,
    because filling one lasted exactly until the next scan."""
    prior = {"f": [{"name": "f", "how": "at line 1", "why": "because X",
                    "perf": "O(n)", "security": "TODO(model)"}]}
    out = l3._fill_entries([{"name": "f", "how": "at line 99"}], prior)
    assert out[0]["why"] == "because X"
    assert out[0]["perf"] == "O(n)"
    assert out[0]["security"] == "TODO(model)"


def test_how_is_always_re_derived_never_carried():
    """The derived half must keep being derived -- that is what makes it
    trustworthy and what `stale_contracts` polices."""
    prior = {"f": [{"name": "f", "how": "STALE at line 1", "why": "w"}]}
    out = l3._fill_entries([{"name": "f", "how": "FRESH at line 99"}], prior)
    assert out[0]["how"] == "FRESH at line 99"
    assert "STALE" not in out[0]["how"]


def test_carry_over_survives_a_line_number_change():
    """`how` embeds the line number, so keying the carry-over on it would drop
    a model's `why` the first time anything above the call site shifted."""
    prior = _contract_of(
        "<!-- BUILD-CONTRACT:BEGIN -->\n```yaml\n"
        "inputs:\n- name: f\n  how: 'at line 1'\n  why: kept\n"
        "```\n<!-- BUILD-CONTRACT:END -->")
    idx = l3._prior_index(prior, "inputs")
    assert l3._fill_entries([{"name": "f", "how": "at line 500"}], idx)[0]["why"] == "kept"


def test_duplicate_names_are_matched_positionally():
    prior = {"f": [{"name": "f", "how": "h", "why": "first"},
                   {"name": "f", "how": "h", "why": "second"}]}
    out = l3._fill_entries(
        [{"name": "f", "how": "h"}, {"name": "f", "how": "h"}], prior)
    assert [e["why"] for e in out] == ["first", "second"]


def test_prior_index_tolerates_a_missing_or_broken_contract():
    """A body whose previous contract cannot be parsed must still get a correct
    new one -- refusing would strand the node in the broken state."""
    assert l3._prior_index(None, "inputs") == {}
    assert l3._prior_index({}, "inputs") == {}
    assert l3._prior_index({"inputs": None}, "inputs") == {}
    assert l3._prior_index({"inputs": ["not-a-dict"]}, "inputs") == {}


def test_extract_contract_is_owned_here_not_in_stitch():
    """stitch.py imports level3.py for `analyze_file`, so level3.py borrowing
    the reader back was an import cycle -- it died with RecursionError on the
    first run. Ownership decides direction (stitch.py: "level3.py owns the
    contract shape")."""
    stitch_src = (Path(__file__).resolve().parents[1] / "bin" / "stitch.py").read_text()
    assert "def _extract_contract" not in stitch_src
    assert "_extract_contract = level3.extract_contract" in stitch_src


def test_both_contract_marker_spellings_still_parse():
    """A reader recognising only BUILD- would report every unmigrated node as
    having no contract, which publish-engine.sh turns into a refusal."""
    for marker in ("LEVEL3", "BUILD"):
        body = (f"<!-- {marker}-CONTRACT:BEGIN -->\n```yaml\npayload_ref: x\n"
                f"```\n<!-- {marker}-CONTRACT:END -->")
        contract, err = l3.extract_contract(body)
        assert err is None and contract["payload_ref"] == "x", marker


def test_contract_reader_bounds_on_an_embedded_fence():
    """A `how` value can itself contain a ``` fence; the closing fence is the
    LAST one inside the markers, not the first."""
    body = ("<!-- BUILD-CONTRACT:BEGIN -->\n```yaml\n"
            "inputs:\n- name: f\n  how: 'writes ``` into a file'\n"
            "```\n<!-- BUILD-CONTRACT:END -->")
    contract, err = l3.extract_contract(body)
    assert err is None, err
    assert contract["inputs"][0]["name"] == "f"


# --- retirement: nodes/deprecated/<type>/ (goal:g2.10) ------------------------


def test_scan_rewrites_a_retired_node_in_place_not_at_its_old_address(project, engine):
    """A node retired into `nodes/deprecated/build/` is updated where it lives.

    Without this the scan writes a *second* file at the address a fresh mint
    would choose, and the graph carries one id in two places — the duplicate
    every id-keyed reader resolves differently, and the exact shape a
    deprecation is supposed to avoid.
    """
    assert run(project, engine).returncode == 0
    build_dir = project / "nodes" / "build"
    live = sorted(build_dir.glob("*.md"))[0]
    node_id = fm_of(live)["id"]

    retired_dir = project / "nodes" / "deprecated" / "build"
    retired_dir.mkdir(parents=True, exist_ok=True)
    moved = retired_dir / live.name
    live.rename(moved)

    r = run(project, engine)
    assert r.returncode == 0

    assert moved.exists(), "retired node was not rewritten in place"
    assert not (build_dir / moved.name).exists(), \
        "scan re-minted the retired node at its live address — one id, two files"
    assert fm_of(moved)["id"] == node_id

    ids = [fm_of(p)["id"]
           for p in list(build_dir.glob("*.md")) + list(retired_dir.glob("*.md"))]
    assert len(ids) == len(set(ids)), f"duplicate node ids on disk: {ids}"


def test_scan_does_not_prune_a_retired_node(project, engine):
    """Pruning is origin-gated and path-aware; retirement must not look stale."""
    assert run(project, engine).returncode == 0
    build_dir = project / "nodes" / "build"
    live = sorted(build_dir.glob("*.md"))[0]

    retired_dir = project / "nodes" / "deprecated" / "build"
    retired_dir.mkdir(parents=True, exist_ok=True)
    moved = retired_dir / live.name
    live.rename(moved)

    r = run(project, engine)
    assert r.returncode == 0
    assert moved.exists(), "a retired node was pruned as stale"
    assert "stale build-scan nodes pruned: 0" in r.stdout


def test_node_type_dirs_is_live_first_and_skips_absent(project):
    """Order is load-bearing: callers take the first hit, so live wins."""
    dirs = l3.node_type_dirs(project, "build")
    assert dirs == [project / "nodes" / "build"]

    retired = project / "nodes" / "deprecated" / "build"
    retired.mkdir(parents=True, exist_ok=True)
    assert l3.node_type_dirs(project, "build") == [
        project / "nodes" / "build", retired]

    assert l3.node_type_dirs(project, "no-such-type") == []


# --- goal:s19 — `how` is a function of the payload, not of the interpreter ---
#
# `ast.unparse` re-renders the AST, and its output depends on the CPython
# version that ran it (PEP 701 rewrote f-string parsing in 3.12). One node in
# the real corpus rendered two different ways under 3.11.15 and 3.12.3, so the
# graph flapped between the `:37` publish cron (3.12) and any interactive run
# (3.11 from a venv) — each flap burning a grid version on a file nobody
# edited, and flipping `publish-engine.sh`'s first gate depending on who ran
# last. The fix quotes the payload's own source bytes instead.
#
# These tests deliberately use DOUBLE quotes in their fixtures. The pre-S19
# fixtures in this file all used single quotes, which is exactly why the suite
# passed unchanged through the fix: `ast.unparse` normalises to single quotes,
# so a single-quoted fixture cannot tell a source slice from a re-render.

# The literal construct that flapped, from tests/schema_registry/test_brackets.py:
# an f-string delimited with `"` containing a nested `'[]'`. 3.12 re-renders it
# with `'` delimiters and no escaping — which is not even valid 3.11 syntax.
_FSTRING_FIXTURE = r'''
from pathlib import Path


def write(d, name, fields):
    (d / name).write_text(f"---\nfields:\n  {fields}:\n    type: string\nname: {Path(name).stem.strip('[]')}\n---\n")
'''

# A multi-line call, a comment inside a call, and a `#` inside a string
# literal — the three things a source slice carries that a re-render does not.
_MULTILINE_FIXTURE = r'''
from pathlib import Path


def save(p):
    Path(p).write_text(
        "a: 1\n"      # a comment inside the call
        "b: #2\n",
        encoding="utf-8",
    )
'''


def _sole_how(analysis, section):
    entries = analysis[section]
    assert len(entries) >= 1, analysis
    return entries


def test_how_quotes_the_payload_source_rather_than_re_rendering_it():
    """The S19 falsifier, as a unit test.

    The assertion is the property itself: the backticked fragment in `how` is a
    verbatim substring of the payload. Only a slice can satisfy that; a
    re-render satisfies it at most by coincidence.

    Note what is deliberately *not* asserted here — that the fragment differs
    from `ast.unparse` of the same node. On this exact fixture 3.11 reproduces
    the source byte-for-byte and 3.12 does not, so that assertion would itself
    be interpreter-dependent. That asymmetry is the bug, not a test artefact;
    the stable discriminator lives in
    `test_re_rendering_is_lossy_in_a_version_independent_way` below.
    """
    analysis = l3.analyze_source(_FSTRING_FIXTURE.encode(), ".py", "brackets.py")
    assert analysis["parse_ok"] is True
    how = next(e["how"] for e in analysis["outputs"] if "write_text" in e["how"])
    fragment = how.split("`")[1]

    assert fragment in _FSTRING_FIXTURE, (
        "`how` must quote the payload's own bytes, not a re-render")
    assert 'write_text(f"---' in fragment, "source uses a double-quoted f-string"
    # the indentation inside the template is content; it must survive verbatim
    assert '\\nfields:\\n  {fields}:\\n    type: string' in fragment


def test_re_rendering_is_lossy_in_a_version_independent_way():
    """Why the substring assertion above has teeth, pinned on a stable case.

    Every supported CPython normalises a double-quoted plain string to single
    quotes when unparsing, so this fixture discriminates a slice from a
    re-render on 3.11 and 3.12 alike — unlike the f-string, where the two
    versions disagree with each other.
    """
    src = 'Path("a/b.txt").read_text()\n'
    call = ast.parse(src).body[0].value
    assert ast.unparse(call) == "Path('a/b.txt').read_text()"
    assert l3._render(src, call) == 'Path("a/b.txt").read_text()'


def test_derived_entry_names_are_source_slices_too():
    """`name` goes through the same chokepoint, and it is load-bearing.

    A derived `name` keys `_prior_index`, so an interpreter-dependent `name`
    would not merely churn — it would drop a model's authored `why`/`perf`/
    `security` on the scan that flipped it. (Measured 2026-08-28: 8,427
    authored fields in the corpus, 0 filled, so nothing was actually lost. The
    exposure is real regardless of whether it has been paid yet.)
    """
    src = 'from pathlib import Path\n\n\ndef f():\n    Path("a/b.txt").read_text()\n'
    analysis = l3.analyze_source(src.encode(), ".py", "f.py")
    names = [e["name"] for e in analysis["inputs"]]
    assert 'Path("a/b.txt")' in names, names


def test_how_is_always_one_line_even_when_the_call_is_not():
    """`how` is one YAML scalar and `_cap`'s budget is for content, not indent."""
    analysis = l3.analyze_source(_MULTILINE_FIXTURE.encode(), ".py", "save.py")
    for entry in analysis["inputs"] + analysis["outputs"] + analysis["uncovered"]:
        assert "\n" not in entry["how"], entry
        assert "\r" not in entry["how"], entry
        assert "\n" not in str(entry["name"]), entry
    how = next(e["how"] for e in analysis["outputs"] if "write_text" in e["how"])
    # the continuation lines' indentation is layout, and is joined away
    assert 'Path(p).write_text( "a: 1\\n"' in how, how
    # ...while the source's own quoting and its inline comment both survive,
    # because nothing re-rendered them
    assert 'encoding="utf-8"' in how
    assert "# a comment inside the call" in how


def test_one_line_never_touches_whitespace_inside_a_line():
    """The regression that `\\s+` caused and this collapse must not.

    Most of what this engine writes is indentation-sensitive — YAML fragments,
    markdown, node bodies — carried in string literals whose `\\n` is two
    characters and whose following spaces are content. Collapsing those reports
    an indentation the payload does not have.
    """
    assert l3._one_line('f"a:\\n  b:\\n    c"') == 'f"a:\\n  b:\\n    c"'
    assert l3._one_line("f(a,\n        b)") == "f(a, b)"
    assert l3._one_line("  x  \n\n  y  ") == "x y"
    assert l3._one_line(None) is None


def test_signature_is_the_only_place_ast_unparse_still_runs():
    """`ast.arguments` carries no position, so it is the one unslicable node.

    Pinned rather than assumed, because the two obvious alternatives are both
    wrong: a span built from the child nodes drops the `*` (vararg's position
    starts at the NAME) and cannot see the `/` at all, and paren-matching the
    header text needs a tokenizer — i.e. a second renderer, which is the class
    of thing S19 removed.
    """
    src = "def f(a, /, b, *args, c=1, **kw) -> int:\n    return open('x').read()\n"
    tree = ast.parse(src)
    fn = tree.body[0]

    assert ast.get_source_segment(src, fn.args) is None
    assert l3._render(src, fn.args) == ast.unparse(fn.args)

    # the child-span shortcut, shown to be unavailable
    assert ast.get_source_segment(src, fn.args.vararg) == "args"

    # everything the scanners actually render does have a position
    for node in ast.walk(tree):
        if isinstance(node, (ast.Call, ast.Attribute, ast.Name, ast.Constant)):
            assert ast.get_source_segment(src, node) is not None, ast.dump(node)


def test_scanners_refuse_to_default_the_source():
    """A forgotten `source` must be a TypeError, never a silent re-render.

    This is the shape of the original defect: nothing was wrong loudly. A
    default of `None` here would restore `ast.unparse` behaviour for whichever
    caller forgot, and it would be invisible until two interpreters disagreed.
    """
    tree = ast.parse("x = 1\n")
    with pytest.raises(TypeError):
        l3._scan_io_calls(tree)
    with pytest.raises(TypeError):
        l3._scan_top_level_defs(tree)


def test_derived_how_and_name_round_trip_through_the_contract_yaml(tmp_path):
    """Write-then-read must be byte-identical, or the graph is permanently dirty.

    A source slice can carry quotes, `#`, backslash escapes and (before
    `_one_line`) newlines, all of which go through `yaml.safe_dump` into the
    BUILD-CONTRACT block and come back out through `extract_contract`. If any
    value did not survive that trip, every scan would rewrite the node — which
    is strictly worse than the intermittent flap S19 fixed, because it would
    arm `publish-engine.sh`'s gate on every single run rather than half of them.
    """
    for label, fixture in (("fstring", _FSTRING_FIXTURE),
                           ("multiline", _MULTILINE_FIXTURE)):
        _id, _fm, body, analysis = l3.build_node(
            "extensions/agi/bin/x.py", tmp_path / "x.py", None,
            payload=fixture.encode())
        contract, err = l3.extract_contract(body)
        assert err is None, (label, err)
        for section in ("inputs", "outputs"):
            stored = [(e["name"], e["how"]) for e in contract.get(section) or []]
            derived = [(e["name"], e["how"]) for e in analysis[section]]
            assert stored == derived, (label, section)


def test_derivation_is_a_fixed_point_over_its_own_output(tmp_path):
    """Re-deriving from an unchanged payload reproduces the stored contract.

    `_fill_entries` already had this property for the authored half; S19 is the
    same property for the mechanical half, against a *second run* rather than a
    second interpreter. The two are the same requirement — `how` is a function
    of the payload alone — and this is the half a single-interpreter suite can
    actually check.
    """
    payload = _MULTILINE_FIXTURE.encode()
    _id, _fm, body1, _a = l3.build_node(
        "extensions/agi/bin/x.py", tmp_path / "x.py", None, payload=payload)
    _id, _fm, body2, _a = l3.build_node(
        "extensions/agi/bin/x.py", tmp_path / "x.py", None, payload=payload,
        prior_body=body1)
    assert body1 == body2


def test_no_engine_signature_contains_an_fstring():
    """Guard the premise that licenses the `ast.arguments` fallback.

    Signatures are the one place `ast.unparse` still runs, and an f-string is
    the only construct these CPython versions are known to render differently.
    Zero of this engine's top-level signatures contain one (measured
    2026-08-28: 0 of 1,241), which is what makes the fallback safe — so the
    premise is checked rather than assumed, because it is a fact about the
    corpus and facts about the corpus change.

    If this fails, do **not** relax the test: an f-string default or annotation
    would reintroduce goal:s19's flap, silently and only across interpreters.
    Either write the default some other way, or slice the parameter list out of
    the source (which needs a tokenizer — see `_render`).
    """
    root = l3.DEFAULT_ENGINE_ROOT
    offenders = []
    n_sigs = 0
    for path in sorted(root.glob("extensions/agi/**/*.py")):
        try:
            tree = ast.parse(path.read_text(encoding="utf-8"))
        except (SyntaxError, UnicodeDecodeError, OSError, ValueError):
            continue
        for node in tree.body:
            if not isinstance(node, (ast.FunctionDef, ast.AsyncFunctionDef)):
                continue
            n_sigs += 1
            if any(isinstance(s, ast.JoinedStr) for s in ast.walk(node.args)):
                offenders.append(f"{path.name}:{node.lineno} {node.name}")
    assert n_sigs > 100, f"scanned only {n_sigs} signatures — the glob is wrong"
    assert offenders == [], offenders


# --- trap 0i — --mint-missing-only is ADDITIVE ONLY ----------------------------
#
# default level3.py is destructive (it prunes stale build-scan nodes), which is
# why trap 0i forbids running it without --dry-run. Hypothesis
# l3-engine-files-outside-the-grid's fix is a mode that CANNOT destroy: mint a
# build node + payload_ref ONLY for a tracked code file that has none; never
# prune, never resurrect a deprecated node, never touch an existing node. These
# tests prove the additive property on a fixture tree holding a LIVE node, a
# DEPRECATED node, and an UN-NODED file.


def _tot_build_nodes(project):
    return (len(list((project / "nodes" / "build").glob("*.md"))) +
            len(list((project / "nodes" / "deprecated" / "build").glob("*.md"))))


def test_mint_missing_only_is_additive_and_never_resurrects(project, engine, tmp_path):
    """The additive property, end to end, on one fixture tree holding a LIVE
    node, a DEPRECATED node, and an un-noded file.

    Before/after: `active + deprecated` build-node count must only GROW. On a
    delta of one mint exactly one node must appear, the deprecated node must
    stay retarded where it is (a deprecated node whose file still exists is a
    DELIBERATE state — reviving it destroys a decision), and no live node may
    be pruned or rewritten into a different file.
    """
    # 1. seed the engine with two code files; default scan gives both live nodes.
    write_engine_tree(engine, {
        "extensions/agi/bin/live.py": "def live():\n    return 1\n",
        "extensions/agi/bin/tolive.py": "def tolive():\n    return 2\n",
    })
    assert run(project, engine).returncode == 0
    live_dir = project / "nodes" / "build"
    assert "bin-live.md" in [p.name for p in live_dir.glob("*.md")]
    assert "bin-tolive.md" in [p.name for p in live_dir.glob("*.md")]

    # 2. retire tolive into nodes/deprecated/build/ (the deprecate-never-delete
    #    move) — its engine file still exists, which is the resurrect trap.
    retired_dir = project / "nodes" / "deprecated" / "build"
    retired_dir.mkdir(parents=True, exist_ok=True)
    (live_dir / "bin-tolive.md").rename(retired_dir / "bin-tolive.md")
    live_hash = (live_dir / "bin-live.md").read_bytes()
    retired_hash = (retired_dir / "bin-tolive.md").read_bytes()
    before = _tot_build_nodes(project)

    # 3. add an un-noded code file to the engine (git-tracked) and a subsystem
    #    mvp so the minted node gets a legal goal:s29 parent.
    (engine / "extensions" / "agi" / "bin" / "newmissing.py").write_text(
        "def new():\n    return 3\n")
    subprocess.run(["git", "add", "-A"], cwd=engine, check=True)
    mvp_path = project / "nodes" / "mvp" / "bin-modules.md"
    mvp_path.parent.mkdir(parents=True, exist_ok=True)
    l3.write_frontmatter(mvp_path,
                         {"id": "mvp:bin-modules", "type": "mvp",
                          "title": "t", "parents": ["hyp:l3"]}, "body")
    mvp_map = tmp_path / "mvp-map.md"
    mvp_map.write_text("extensions/agi/bin/ | mvp:bin-modules\n")

    # 4. DRY-RUN: must propose ONLY the un-noded file, and write nothing.
    r = run(project, engine, "--mint-missing-only", "--mvp-map", str(mvp_map),
            "--dry-run")
    assert r.returncode == 0
    proposed = [l for l in r.stdout.splitlines() if "DRY-RUN: would mint" in l]
    assert len(proposed) == 1, proposed
    assert "build:bin-newmissing" in proposed[0]
    assert "parent mvp:bin-modules" in proposed[0], "goal:s29 parent missing"
    # dry-run must not write a single node file under either address
    assert not (live_dir / "bin-newmissing.md").exists()
    live_names = set(p.name for p in live_dir.glob("*.md"))
    retired_names = set(p.name for p in retired_dir.glob("*.md"))
    assert "bin-newmissing.md" not in live_names
    assert "bin-tolive.md" not in live_names, "resurrected at live address in dry-run"
    assert retired_names == {"bin-tolive.md"}

    # 5. REAL run: count only GROWS by exactly the one mint; nothing else moves.
    r = run(project, engine, "--mint-missing-only", "--mvp-map", str(mvp_map))
    assert r.returncode == 0
    assert _tot_build_nodes(project) == before + 1, "count must only grow by 1"
    # the minted node exists at the live address...
    new_fm = fm_of(live_dir / "bin-newmissing.md")
    assert new_fm["payload_ref"] == "extensions/agi/bin/newmissing.py"
    assert new_fm["parents"] == ["mvp:bin-modules"]
    assert identity.is_valid_mint_id(new_fm["mint_id"])
    # ...the deprecated node is NOT resurrected (no live re-mint, file untouched)
    assert not (live_dir / "bin-tolive.md").exists(), \
        "a deprecated node was resurrected at its live address"
    assert (retired_dir / "bin-tolive.md").read_bytes() == retired_hash
    # ...and the live node was neither pruned nor rewritten into a different file
    assert (live_dir / "bin-live.md").read_bytes() == live_hash


def test_mint_missing_only_dry_run_writes_nothing_and_reports_zero(project, engine):
    """With nothing missing the mode reports nothing-to-mint and writes nothing."""
    write_engine_tree(engine, {"extensions/agi/bin/live.py": "x = 1\n"})
    assert run(project, engine).returncode == 0
    before = _tot_build_nodes(project)
    r = run(project, engine, "--mint-missing-only")
    assert r.returncode == 0
    assert "nothing to mint" in r.stdout
    assert _tot_build_nodes(project) == before


def test_refuses_a_rootless_project_path_by_name(tmp_path):
    """goal:g15, hypothesis:l4-stitch-and-level3-project-resolve-the-graph-
    root-or-refuse-by-name-and-verify-prints-its-count — a `--project` path
    that resolves to no graph root (no `.agi/` at or above, no `nodes/` at
    the path) is REFUSED by name, exit 2 — never scanned as an empty tree
    that then prunes authoritative scope."""
    nowhere = tmp_path / "nowhere"
    nowhere.mkdir()
    engine = tmp_path / "engine"
    (engine / "extensions" / "agi" / "bin").mkdir(parents=True)
    (engine / "extensions/agi/bin/a.py").write_text("import os\n")
    subprocess.run(["git", "init", "-q"], cwd=engine, check=True)
    r = run(nowhere, engine, "--dry-run")
    assert r.returncode == 2
    assert f"no graph root at or above {nowhere}" in r.stderr
    assert "no .agi/ and no nodes/" in r.stderr



def _run_nof_flag(cwd: Path, *args,
                  env_remove=("AGI_PROJECT_ROOT", "AGI_TREE_PROJECT_ROOT",
                              "AUTORESEARCH_TREE_PROJECT_ROOT")):
    """Run level3.py with NO `--project` flag, env overrides stripped, from
    `cwd` — the spelling that used to fall back to the raw cwd."""
    cmd = [sys.executable, str(BIN), *args]
    env = {k: v for k, v in os.environ.items() if k not in env_remove}
    return subprocess.run(cmd, cwd=str(cwd), capture_output=True,
                          text=True, env=env)


def test_nof_flag_default_refuses_a_rootless_cwd_by_name(tmp_path):
    """goal:g15, hypothesis:l4-level3-no-flag-default-refuses-a-rootless-cwd-
    and-the-sl7-25-body-names-its-missing-and-orphan-counts — with no
    `--project` and no env override, a run started in a rootless directory
    (no `.agi/` at or above, no `nodes/` here) is REFUSED by name, exit 2,
    exactly like the `--project` spelling — never scanned as an authoritative
    `<cwd>/nodes` tree whose stray output later feeds the next scan."""
    rootless = tmp_path / "rootless"
    rootless.mkdir()
    engine = tmp_path / "engine"
    (engine / "extensions" / "agi" / "bin").mkdir(parents=True)
    (engine / "extensions/agi/bin/a.py").write_text("import os\n")
    subprocess.run(["git", "init", "-q"], cwd=engine, check=True)
    r = _run_nof_flag(rootless, "--dry-run", "--engine-root", str(engine))
    assert r.returncode == 2, r.stderr
    assert f"no graph root at or above {rootless}" in r.stderr
    assert "no .agi/ and no nodes/" in r.stderr


def test_nof_flag_run_from_inside_a_project_resolves_its_nearest_agi(tmp_path):
    """Without `--project` or env, a run whose cwd is inside a project
    resolves that project's own graph root (`<repo>/.agi`) through the same
    resolver the flag uses — it does not misfire into a stray tree."""
    proj = tmp_path / "proj"
    (proj / ".agi" / "nodes" / "build").mkdir(parents=True)
    (proj / ".agi" / "config.json").write_text('{"id": "test-proj"}\n')
    engine = tmp_path / "engine"
    (engine / "extensions" / "agi" / "bin").mkdir(parents=True)
    (engine / "extensions/agi/bin/a.py").write_text("import os\n")
    subprocess.run(["git", "init", "-q"], cwd=engine, check=True)
    subprocess.run(["git", "add", "-A"], cwd=engine, check=True)
    r = _run_nof_flag(proj, "--dry-run", "--engine-root", str(engine))
    assert r.returncode == 0, r.stderr
    assert f"target dir: {proj / '.agi' / 'nodes' / 'build'}" in r.stdout
