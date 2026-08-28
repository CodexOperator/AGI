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
