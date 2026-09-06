"""Tests for telemetry_rollup.py — goal:g16 / hypothesis:l2w6-telemetry-rollup.

Red-first: these tests are written against the as-yet-unrun code, with
fabricated nodes that carry telemetry fields under a temporary graph.
"""
from __future__ import annotations

import sys
from pathlib import Path

import pytest

BIN = Path(__file__).resolve().parent.parent / "bin"
SRC = Path(__file__).resolve().parent.parent / "src"
sys.path.insert(0, str(BIN))
sys.path.insert(0, str(SRC))

import telemetry_rollup  # noqa: E402


# --------------------------------------------------------------------------
# Helpers: create a minimal node file in a temp graph
# --------------------------------------------------------------------------

def _write_node(graph: Path, nid: str, ntype: str, parents: list[str],
                extra_fm: dict | None = None):
    """Write a minimal node file with the given id, type, and parents.

    Always creates the type's subdirectory (nodes/<type>/).
    Also writes the file under a slug derived from the node id.
    """
    slug = nid.split(":")[-1]
    type_dir = graph / "nodes" / ntype
    type_dir.mkdir(parents=True, exist_ok=True)

    # Build frontmatter with all required fields.
    fm = {
        "id": nid,
        "type": ntype,
        "mint_id": f"mint-{slug[:12]}",
        "title": f"Test {ntype} {slug}",
        "parents": parents,
    }
    if extra_fm:
        fm.update(extra_fm)

    lines = ["---"]
    for k, v in fm.items():
        if isinstance(v, list):
            if v:
                lines.append(f"{k}:")
                for item in v:
                    lines.append(f"  - {item}")
            else:
                lines.append(f"{k}: []")
        elif isinstance(v, bool):
            lines.append(f"{k}: {'true' if v else 'false'}")
        elif v is None:
            lines.append(f"{k}:")
        else:
            lines.append(f"{k}: {v}")
    lines.append("---")
    lines.append("")
    lines.append("# " + slug)
    lines.append("")

    (type_dir / f"{slug}.md").write_text("\n".join(lines) + "\n")


# --------------------------------------------------------------------------
# Fixtures
# --------------------------------------------------------------------------

@pytest.fixture()
def graph(tmp_path: Path) -> Path:
    """Create a temporary graph with telemetry-equipped experiment nodes.
    
    Graph structure:
        goal:g16
          └── hypothesis:h1
                └── experiment:e1  ← carries tokens_in=100, tokens_out=50, cost_usd=0.01
                      └── verdict:v1
                            └── outcome:o1
        goal:g17
          └── hypothesis:h2
                └── experiment:e2  ← carries tokens_in=200, tokens_out=100, cost_usd=0.02, accepted_bytes=500
                      └── verdict:v2
                            └── outcome:o2 (also parent of outcome:o1 via next_edges)
        experiment:e3 (orphan, no telemetry) ← skipped (no data)
    
    outcome:o3 (parent: mvp:m1)
      mvp:m1
        └── build:b1
              └── experiment:e4 ← carries tokens_in=50, tokens_out=25, cost_usd=0.005, accepted_bytes=100
    """
    g = tmp_path / ".agi"
    g.mkdir(parents=True, exist_ok=True)
    (g / "config.json").write_text("{}")

    # Create the graph nodes.
    # Hypothesis and goal nodes exist to give experiment nodes valid parents.
    _write_node(g, "goal:g16", "goal", [], {"title": "G16 Telemetry"})
    _write_node(g, "hypothesis:h1", "hypothesis", ["goal:g16"],
                {"testable_claim": "h1 claim"})
    _write_node(g, "experiment:e1", "experiment", ["hypothesis:h1"],
                {"tokens_in": 100, "tokens_out": 50, "cost_usd": 0.01,
                 "telemetry_source": "pi-log"})
    _write_node(g, "verdict:v1", "verdict", ["experiment:e1"])
    _write_node(g, "outcome:o1", "outcome", ["verdict:v1"])

    _write_node(g, "goal:g17", "goal", [], {"title": "G17 something"})
    _write_node(g, "hypothesis:h2", "hypothesis", ["goal:g17"],
                {"testable_claim": "h2 claim"})
    _write_node(g, "experiment:e2", "experiment", ["hypothesis:h2"],
                {"tokens_in": 200, "tokens_out": 100, "cost_usd": 0.02,
                 "accepted_bytes": 500, "telemetry_source": "pi-log"})
    _write_node(g, "verdict:v2", "verdict", ["experiment:e2"])
    _write_node(g, "outcome:o2", "outcome", ["verdict:v2"])

    # Orphan experiment with no telemetry fields — should be skipped.
    _write_node(g, "experiment:e3", "experiment", ["hypothesis:h1"],
                {"telemetry_source": "unavailable"})
    
    # Another chain through mvp -> build -> experiment
    _write_node(g, "mvp:m1", "mvp", [])
    _write_node(g, "build:b1", "build", ["mvp:m1"])
    _write_node(g, "experiment:e4", "experiment", ["build:b1"],
                {"tokens_in": 50, "tokens_out": 25, "cost_usd": 0.005,
                 "accepted_bytes": 100, "telemetry_source": "pi-log"})
    _write_node(g, "verdict:v3", "verdict", ["experiment:e4"])
    _write_node(g, "outcome:o3", "outcome", ["mvp:m1"])

    return g


# --------------------------------------------------------------------------
# Test: walk experiments from a report node
# --------------------------------------------------------------------------


def test_walk_experiments_from_outcome(graph: Path):
    """outcome:o1 should discover experiment:e1 and experiment:e3 (e3 has
    no telemetry though)."""
    experiments = telemetry_rollup.walk_experiments(graph, "outcome:o1")
    ids = {efm.get("id") for efm in experiments}
    assert "experiment:e1" in ids, "e1 should be discovered via verdict:v1"
    # experiment:e3 shares the same chain (via hypothesis:h1), so it should
    # also be discovered.
    assert "experiment:e3" in ids, "e3 shares hypothesis:h1, should be found"


def test_walk_experiments_from_separate_outcome(graph: Path):
    """outcome:o2 discovers experiment:e2."""
    experiments = telemetry_rollup.walk_experiments(graph, "outcome:o2")
    ids = {efm.get("id") for efm in experiments}
    assert "experiment:e2" in ids, "e2 should be discovered"
    assert "experiment:e1" not in ids, "e1 is in a different chain"


def test_walk_experiments_with_mvp_parent(graph: Path):
    """outcome:o3's parent is mvp:m1, which points to build:b1 which
    has experiment:e4."""
    experiments = telemetry_rollup.walk_experiments(graph, "outcome:o3")
    ids = {efm.get("id") for efm in experiments}
    assert "experiment:e4" in ids, "e4 should be discovered via mvp:m1 -> build:b1"


def test_walk_experiments_empty_chain(graph: Path):
    """A report node whose chain has no experiments should return empty list."""
    _write_node(graph, "outcome:orphan", "outcome", [])
    experiments = telemetry_rollup.walk_experiments(graph, "outcome:orphan")
    assert experiments == [], "no experiments in an empty chain"


# --------------------------------------------------------------------------
# Test: collect_telemetry sums correctly
# --------------------------------------------------------------------------


def test_collect_telemetry_basic_sum(graph: Path):
    """Sum telemetry from e1 (100, 50, 0.01, 0) and e3 (no telemetry, skipped)."""
    experiments = telemetry_rollup.walk_experiments(graph, "outcome:o1")
    # De-duplicate.
    seen = set()
    unique = [efm for efm in experiments if efm.get("id", "") not in seen
              and not seen.add(efm.get("id", ""))]
    sums, summed, skipped = telemetry_rollup.collect_telemetry(unique)
    assert summed >= 1, "at least e1 should be summed"
    assert skipped >= 1, "e3 has no telemetry and should be skipped"
    assert sums["tokens_in_total"] >= 100, "e1 contributes 100 tokens_in"
    assert sums["tokens_out_total"] >= 50, "e1 contributes 50 tokens_out"
    assert sums["cost_usd_total"] >= 0.01, "e1 contributes 0.01 cost"


def test_collect_telemetry_with_accepted_bytes(graph: Path):
    """outcome:o2 chain has e2 with accepted_bytes=500."""
    experiments = telemetry_rollup.walk_experiments(graph, "outcome:o2")
    seen = set()
    unique = [efm for efm in experiments if efm.get("id", "") not in seen
              and not seen.add(efm.get("id", ""))]
    sums, summed, skipped = telemetry_rollup.collect_telemetry(unique)
    assert summed == 1, "only e2 has data"
    assert skipped == 0, "no experiments in this chain lack telemetry"
    assert sums["tokens_in_total"] == 200
    assert sums["tokens_out_total"] == 100
    assert sums["cost_usd_total"] == 0.02
    assert sums["accepted_bytes_total"] == 500


def test_collect_empty_list():
    """Empty experiment list: all zeros, 0 summed, 0 skipped."""
    sums, summed, skipped = telemetry_rollup.collect_telemetry([])
    assert sums["tokens_in_total"] == 0
    assert sums["tokens_out_total"] == 0
    assert sums["cost_usd_total"] == 0
    assert sums["accepted_bytes_total"] == 0
    assert summed == 0
    assert skipped == 0


# --------------------------------------------------------------------------
# Test: format_ratios
# --------------------------------------------------------------------------


def test_format_ratios_with_data():
    sums = {"tokens_in_total": 300, "tokens_out_total": 150,
            "cost_usd_total": 0.03, "accepted_bytes_total": 600}
    ratios = telemetry_rollup.format_ratios(sums)
    assert "bytes_per_token" in ratios
    assert "bytes_per_dollar" in ratios


def test_format_ratios_no_bytes():
    sums = {"tokens_in_total": 100, "tokens_out_total": 50,
            "cost_usd_total": 0.01, "accepted_bytes_total": 0}
    ratios = telemetry_rollup.format_ratios(sums)
    assert "no ratios computable" in ratios


def test_format_ratios_no_data():
    sums = {"tokens_in_total": 0, "tokens_out_total": 0,
            "cost_usd_total": 0, "accepted_bytes_total": 0}
    ratios = telemetry_rollup.format_ratios(sums)
    assert "no ratios computable" in ratios


# --------------------------------------------------------------------------
# Test: do_rollup writes to the report node (UPDATED or UNCHANGED)
# --------------------------------------------------------------------------


def test_do_rollup_writes_sums(graph: Path):
    """do_rollup on outcome:o2 should write the sums to the node."""
    result = telemetry_rollup.do_rollup(graph, "outcome:o2")
    assert "error" not in result, f"unexpected error: {result.get('error')}"
    assert result["type"] == "outcome"
    assert result["experiments_found"] == 1
    assert result["nodes_summed"] == 1
    assert result["write_results"]["status"] in ("UPDATED", "UNCHANGED")
    # Verify the sums were written by reading the node back.
    from graph_core.persistence import frontmatter as fm_reader
    fpath = list((graph / "nodes" / "outcome").glob("o2.md"))
    assert fpath, "outcome:o2 file should exist"
    nf = fm_reader.load_node_file(fpath[0], body=False)
    assert nf.frontmatter.get("tokens_in_total") == 200
    assert nf.frontmatter.get("tokens_out_total") == 100
    assert nf.frontmatter.get("cost_usd_total") == 0.02
    assert nf.frontmatter.get("accepted_bytes_total") == 500
    assert nf.frontmatter.get("telemetry_nodes_summed") == 1
    assert nf.frontmatter.get("telemetry_nodes_skipped") == 0


def test_do_rollup_dry_run_writes_nothing(graph: Path):
    """Dry run mode should not modify the node."""
    result = telemetry_rollup.do_rollup(graph, "outcome:o2", dry_run=True)
    assert result.get("dry_run") is True
    assert result.get("write_results") is None
    # Verify the node was NOT modified.
    from graph_core.persistence import frontmatter as fm_reader
    fpath = list((graph / "nodes" / "outcome").glob("o2.md"))
    nf = fm_reader.load_node_file(fpath[0], body=False)
    assert "tokens_in_total" not in nf.frontmatter, "dry run should not write"


def test_do_rollup_rejects_non_report_type(graph: Path):
    """A non-report node type should be rejected."""
    result = telemetry_rollup.do_rollup(graph, "hypothesis:h1")
    assert "error" in result, "should reject non-report type"


def test_do_rollup_nonexistent_node(graph: Path):
    """A non-existent node id should return an error."""
    result = telemetry_rollup.do_rollup(graph, "outcome:nonexistent")
    assert "error" in result


# --------------------------------------------------------------------------
# Test: bigger_outcome and overview report types
# --------------------------------------------------------------------------


def test_rollup_from_bigger_outcome(graph: Path):
    """A bigger_outcome whose parent is outcome:o2 should find the same
    experiments."""
    _write_node(graph, "bigger_outcome:bo1", "bigger_outcome",
                ["outcome:o2"])
    result = telemetry_rollup.do_rollup(graph, "bigger_outcome:bo1")
    assert "error" not in result
    assert result["type"] == "bigger_outcome"
    assert result["experiments_found"] == 1
    assert result["nodes_summed"] == 1


def test_rollup_from_overview(graph: Path):
    """An overview whose parent is bigger_outcome should find experiments
    reachable through the chain."""
    _write_node(graph, "bigger_outcome:bo2", "bigger_outcome",
                ["outcome:o2"])
    _write_node(graph, "overview:ov1", "overview", ["bigger_outcome:bo2"])
    result = telemetry_rollup.do_rollup(graph, "overview:ov1")
    assert "error" not in result, f"error: {result.get('error')}"
    assert result["type"] == "overview"
    # Should find e2 through bo2 -> o2 -> v2 -> e2
    assert result["experiments_found"] >= 1


# --------------------------------------------------------------------------
# Test: CLI smoke (argparse parsing, help)
# --------------------------------------------------------------------------


def test_cli_smoke_help():
    """The CLI entry should accept --help."""
    try:
        telemetry_rollup.main(["--help"])
    except SystemExit as e:
        # argparse exits with code 0 on --help
        assert e.code == 0, f"help exit code was {e.code}"