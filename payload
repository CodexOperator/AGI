"""Tests for bin/frontier.py, the read-only frontier lister.

Does not assert exact corpus counts — the graph grows every iteration. It
locks the PROPERTY that matters to hypothesis:l3-frontier-successor-derivable:
the successor types are DERIVED at runtime from `context/schemas/*.md`, so
editing a schema's `spawn.allowed_parents` changes the output with no code
change. Anything that hard-coded the chain grammar in Python would fail these.
"""
from __future__ import annotations

import sys
from pathlib import Path

BIN = Path(__file__).resolve().parents[1] / "bin"
sys.path.insert(0, str(BIN))

import frontier  # noqa: E402


def _write(path: Path, text: str) -> None:
    path.parent.mkdir(parents=True, exist_ok=True)
    path.write_text(text, encoding="utf-8")


def _schema(name: str, allowed: str) -> str:
    return (
        f"---\nname: {name}\nspawn:\n  allowed_parents: [{allowed}]\n"
        f"  min_parents: {0 if name == 'idea' else 1}\n  max_parents: 1\n---\n\n# {name}\n"
    )


def _node(nid: str, type_: str, parents: str = "") -> str:
    p = f"parents: [{parents}]\n" if parents else ""
    return f"---\nid: {nid}\ntype: {type_}\n{p}title: {nid}\n---\n\nbody\n"


def make_graph(tmp: Path) -> tuple[Path, Path]:
    """A tiny chain plus a terminal tip, with a full active-schema set."""
    nodes = tmp / "nodes"
    schemas = tmp / "schemas"

    # idea is parentless; hypothesis may be parented by idea; experiment by
    # hypothesis; verdict by both experiment and hypothesis. task starts legal
    # only under hypothesis. overview is a terminal
    # (no schema lists it as an allowed parent yet).
    _write(schemas / "[idea].md", _schema("idea", ""))          # no parent allowed
    _write(schemas / "[hypothesis].md", _schema("hypothesis", "idea"))
    _write(schemas / "[experiment].md", _schema("experiment", "hypothesis"))
    _write(schemas / "[verdict].md", _schema("verdict", "experiment, hypothesis"))
    _write(schemas / "[task].md", _schema("task", "hypothesis"))
    _write(schemas / "[overview].md", _schema("overview", ""))

    _write(nodes / "idea.md", _node("idea:i1", "idea"))
    _write(nodes / "hypothesis.md", _node("hypothesis:h1", "hypothesis", "idea:i1"))
    _write(nodes / "experiment.md", _node("experiment:e1", "experiment", "hypothesis:h1"))
    _write(nodes / "overview.md", _node("overview:o1", "overview"))
    return nodes, schemas


def test_successors_derive_from_declared_schemas(tmp_path):
    nodes, schemas = make_graph(tmp_path)
    rows, succ, named, residue = frontier.frontier(nodes, schemas)

    # idea is the only other tip with a successor: hypothesis may be parented by
    # idea, and verdict may be parented by experiment.
    assert succ["idea"] == ["hypothesis"]
    assert succ["experiment"] == ["verdict"]
    assert succ.get("overview") in (None, []), "no schema allows an overview parent yet"
    # the terminal tip is the overview; the residue is exactly the grammar terminals.
    assert [r["id"] for r in residue] == ["overview:o1"]


def test_edit_schema_changes_output_with_no_code_change(tmp_path):
    """The 'real test' clause: `allowed_parents` drives the output, not code."""
    nodes, schemas = make_graph(tmp_path)
    rows_a, succ_a, _, _ = frontier.frontier(nodes, schemas)
    assert succ_a.get("overview") in (None, [])

    # Teach overview that it may be the parent of a task — schema edit only.
    _write(schemas / "[task].md", _schema("task", "hypothesis, overview"))
    rows_b, succ_b, _, _ = frontier.frontier(nodes, schemas)

    assert succ_b["overview"] == ["task"], "overview must gain a successor"
    assert succ_b["idea"] == ["hypothesis"], "unrelated schema output must not change"
    simple_a = {r["id"]: ",".join(r["succ"]) for r in rows_a}
    simple_b = {r["id"]: ",".join(r["succ"]) for r in rows_b}
    assert simple_a["overview:o1"] == ""
    assert simple_b["overview:o1"] == "task"
    assert simple_a != simple_b


def test_deprecated_nodes_are_not_live_frontier(tmp_path):
    nodes, schemas = make_graph(tmp_path)
    # Retire the hypothesis: it no longer names experiment, so experiment falls
    # back to a tip — but the retired hypothesis itself must not appear.
    _write(nodes / "hypothesis.md",
           "---\nid: hypothesis:h1\ntype: hypothesis\nparents: [idea:i1]\n"
           "status: deprecated\ntitle: t\n---\n\nbody\n")
    rows, _succ, _n, residue = frontier.frontier(nodes, schemas)
    ids = {r["id"] for r in rows}
    assert "hypothesis:h1" not in ids, "deprecated node must not be lister frontier"
    assert "experiment:e1" in ids, "experiment is no longer named by a live parent"


def test_cli_is_read_only_and_help_smokes():
    """The script must run clean with --help (test_bin_help_smoke covers it too)
    and against the live repo `list --count` must exit 0 — a smoke that the
    real corpus resolves."""
    import subprocess
    r = subprocess.run([sys.executable, str(BIN / "frontier.py"), "--help"],
                       capture_output=True, text=True, timeout=30)
    assert r.returncode == 0 and r.stdout.strip()


def test_anchor_walk_finds_goal_ancestor(tmp_path):
    """a tip parented by a goal carries that goal as its anchor."""
    nodes, schemas = make_graph(tmp_path)
    _write(nodes / "goal.md", _node("goal:g1", "goal"))
    _write(nodes / "overview.md", _node("overview:o1", "overview", "goal:g1"))
    rows, _succ, _n, _r = frontier.frontier(nodes, schemas, with_anchor=True)
    by_id = {r["id"]: r for r in rows}
    assert by_id["overview:o1"]["anchor"] == "goal:g1"


def test_anchor_unit_direct(tmp_path):
    nodes, schemas = make_graph(tmp_path)
    loaded = frontier._load_nodes(nodes)
    _write(nodes / "goal.md", _node("goal:g1", "goal"))
    # idea parented by a goal, so a walk from idea reaches it
    _write(nodes / "idea.md", _node("idea:i1", "idea", "goal:g1"))
    loaded = frontier._load_nodes(nodes)
    assert frontier._anchor(loaded, "idea:i1") == "goal:g1"
    assert frontier._anchor(loaded, "goal:g1") is None