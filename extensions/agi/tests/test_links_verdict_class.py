"""hypothesis:l5-a-verdict-node-carries-the-class-its-evidence-experiment-recorded.

`links.py schema` gains one report-only check: a verdict's CLASS (its
`verdict:` with any `:N` confidence suffix stripped) must equal the class the
experiment it names in `evidence_runs:`/`parents:` recorded in its own
`verdict:`, unless the verdict carries `demoted_from:` naming that class.

An experiment with no `verdict:` records no class to compare against, so the
pair is silent -- measured on this core graph (TM.54, re-derived): 51 pairs
name an experiment that HAS a class, 11 of them disagree.
"""
from __future__ import annotations

import sys
from pathlib import Path

BIN = Path(__file__).resolve().parent.parent / "bin"
SRC = Path(__file__).resolve().parent.parent / "src"
sys.path.insert(0, str(BIN))
sys.path.insert(0, str(SRC))

import links  # noqa: E402


def _graph(tmp_path: Path) -> Path:
    graph = tmp_path / ".agi"
    (graph / "nodes" / "verdict").mkdir(parents=True)
    (graph / "nodes" / "experiment").mkdir(parents=True)
    (graph / "config.json").write_text("{}")
    return graph


def _node(graph: Path, node_id: str, **fields) -> Path:
    ntype, slug = node_id.split(":", 1)
    lines = [f"id: {node_id}", f"type: {ntype}"]
    for key, val in fields.items():
        if isinstance(val, list):
            lines.append(f"{key}:")
            lines += [f"  - {v}" for v in val]
        else:
            lines.append(f"{key}: {val}")
    path = graph / "nodes" / ntype / f"{slug}.md"
    path.write_text("---\n" + "\n".join(lines) + "\n---\n\nbody\n")
    return path


def _pair(graph: Path, vclass: str, eclass: str | None = None, **v_extra) -> None:
    _node(graph, "experiment:e1", verdict=eclass)
    _node(graph, "verdict:v1",
          parents=["experiment:e1"], evidence_runs=["experiment:e1"],
          verdict=vclass, **v_extra)


def _run(graph: Path) -> tuple[int, str]:
    import io
    import contextlib
    buf = io.StringIO()
    with contextlib.redirect_stdout(buf):
        rc = links._schema_report(graph)
    return rc, buf.getvalue()


def test_equal_classes_are_silent(tmp_path):
    graph = _graph(tmp_path)
    _pair(graph, "proved", "proved")
    rc, out = _run(graph)
    assert "verdict-class:" not in out
    assert "0 verdict-class disagreement(s)" in out


def test_the_confidence_suffix_is_stripped(tmp_path):
    graph = _graph(tmp_path)
    _pair(graph, "inconclusive_lean_proved:70", "inconclusive_lean_proved:45")
    rc, out = _run(graph)
    assert "verdict-class:" not in out
    assert "0 verdict-class disagreement(s)" in out


def test_a_real_flip_is_one_line_and_counted(tmp_path):
    graph = _graph(tmp_path)
    _pair(graph, "proved", "inconclusive_lean_proved:55")
    rc, out = _run(graph)
    lines = [ln for ln in out.splitlines() if ln.startswith("verdict-class:")]
    assert lines == [
        "verdict-class: verdict:v1 says proved, experiment:e1 says "
        "inconclusive_lean_proved"
    ]
    assert "1 verdict-class disagreement(s)" in out


def test_a_named_demotion_is_silent(tmp_path):
    graph = _graph(tmp_path)
    _pair(graph, "inconclusive_lean_proved:65", "proved",
          demoted_from="proved:90")
    rc, out = _run(graph)
    assert "verdict-class:" not in out
    assert "0 verdict-class disagreement(s)" in out


def test_an_experiment_with_no_recorded_class_is_silent(tmp_path):
    """TM.54's measured shape: 125 pairs, only 51 name a classed experiment."""
    graph = _graph(tmp_path)
    _node(graph, "experiment:e1")
    _node(graph, "verdict:v1", parents=["experiment:e1"],
          evidence_runs=["experiment:e1"], verdict="proved")
    rc, out = _run(graph)
    assert "verdict-class:" not in out
    assert "0 verdict-class disagreement(s)" in out


def test_the_schema_report_still_exits_zero_with_and_without_fix(tmp_path):
    graph = _graph(tmp_path)
    _pair(graph, "proved", "disproved")
    assert _run(graph)[0] == 0
    assert links._schema_report(graph, fix=True) == 0
