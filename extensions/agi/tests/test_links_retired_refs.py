"""hypothesis:links-py-flags-live-references-to-retired-goals (`goal:g15`).

`links.py links` gains a `retired` count and `--strict`: every LIVE reference
to a goal id whose node is `status: retired` or absent, with the successor the
retired node's `THOUGHT` block records. The scanned/exempt surfaces and the
hit-line template live on the `config:links` node, so adding a surface is a
config edit and never a code change.

Discrimination the tests pin: a retired goal RESOLVES (which is why
`broken_links` is 0 for this defect), deprecated nodes and history fields are
exempt, and a `THOUGHT` block is not a live reference.
"""
from __future__ import annotations

import sys
from pathlib import Path

BIN = Path(__file__).resolve().parent.parent / "bin"
SRC = Path(__file__).resolve().parent.parent / "src"
sys.path.insert(0, str(BIN))
sys.path.insert(0, str(SRC))

import links  # noqa: E402

THOUGHT = ("<!-- THOUGHT:BEGIN — authored -->\n"
           "{}\n"
           "<!-- THOUGHT:END -->")


def _graph(tmp_path: Path, scanned: list[str] | None = None,
           template: str = "{file}:{line} {old} \u2192 {succ}") -> Path:
    """A minimal graph whose `config:links` cell names the scanned surfaces."""
    graph = tmp_path / ".agi"
    (graph / "nodes" / "goal").mkdir(parents=True)
    (graph / "nodes" / "hypothesis").mkdir(parents=True)
    (graph / "config.json").write_text("{}")
    _config(graph, scanned or [".agi/nodes/**/*.md"], template)
    return graph


def _config(graph: Path, scanned: list[str], template: str) -> None:
    d = graph / "nodes" / ".geometry"
    d.mkdir(parents=True, exist_ok=True)
    items = ", ".join(f'"{s}"' for s in scanned)
    (d / "links.md").write_text(
        "---\nid: config:links\ntype: config\nmint_id: aa\nlocations: {}\n"
        f"links:\n  scanned: [{items}]\n"
        '  exempt: [".agi/nodes/deprecated/", "THOUGHT", "lens", "judged_against"]\n'
        f'  line_template: "{template}"\n---\n\nbody\n')


def _node(graph: Path, node_id: str, body: str = "body\n", **fields) -> Path:
    ntype, slug = node_id.split(":", 1)
    lines = [f"id: {node_id}", f"type: {ntype}"]
    for key, val in fields.items():
        lines.append(f"{key}: {val}")
    path = graph / "nodes" / ntype / f"{slug}.md"
    path.parent.mkdir(parents=True, exist_ok=True)
    path.write_text("---\n" + "\n".join(lines) + "\n---\n\n" + body)
    return path


def _retired(graph: Path, successor: str = "goal:g-new") -> None:
    _node(graph, "goal:g-retired", status="retired",
          body=THOUGHT.format(f"Superseded 2026-09-19 by {successor}; prior art."))


def test_a_live_node_and_a_card_hit_but_a_history_field_is_exempt(tmp_path):
    graph = _graph(tmp_path, scanned=[".agi/nodes/**/*.md",
                                      ".agi/sessions/quorum/*.md"])
    _retired(graph)
    _node(graph, "hypothesis:h-live", parents="[goal:g-retired]")
    _node(graph, "hypothesis:h-history", judged_against="goal:g-retired")
    cards = graph / "sessions" / "quorum"
    cards.mkdir(parents=True)
    (cards / "card.md").write_text("the seat owns goal:g-retired\n")

    hits = links.scan_retired_refs(graph)
    assert [(h[0], h[2]) for h in hits] == [
        (".agi/nodes/hypothesis/h-live.md", "goal:g-retired"),
        (".agi/sessions/quorum/card.md", "goal:g-retired"),
    ], "the history field was counted or an exempt field was"


def test_the_successor_is_read_from_the_retired_nodes_thought(tmp_path):
    graph = _graph(tmp_path)
    _retired(graph, successor="goal:g20")
    _node(graph, "hypothesis:h1", parents="[goal:g-retired]")

    (hit,) = links.scan_retired_refs(graph)
    assert hit[3] == "goal:g20"


def test_a_thought_block_reference_is_not_a_hit(tmp_path):
    graph = _graph(tmp_path, scanned=[".agi/sessions/quorum/*.md"])
    _retired(graph)
    cards = graph / "sessions" / "quorum"
    cards.mkdir(parents=True)
    (cards / "card.md").write_text("live line\n" + THOUGHT.format("goal:g-retired"))

    assert links.scan_retired_refs(graph) == []


def test_an_absent_goal_id_is_a_hit_with_no_successor(tmp_path):
    graph = _graph(tmp_path)
    _node(graph, "hypothesis:h1", parents="[goal:g-never-existed]")

    (hit,) = links.scan_retired_refs(graph)
    assert hit[2] == "goal:g-never-existed" and hit[3] == "none"


def test_a_surface_added_by_the_config_node_is_scanned(tmp_path):
    graph = _graph(tmp_path, scanned=[".agi/nodes/**/*.md"])
    _retired(graph)
    (tmp_path / "notes.md").write_text("mentions goal:g-retired\n")
    assert links.scan_retired_refs(graph) == [], "the config list was ignored"

    _config(graph, [".agi/nodes/**/*.md", "notes.md"], "{file}:{line} {old} \u2192 {succ}")
    hits = links.scan_retired_refs(graph)
    assert [(h[0], h[2]) for h in hits] == [("notes.md", "goal:g-retired")]


def test_strict_exits_one_and_the_template_is_data_not_code(tmp_path, capsys):
    graph = _graph(tmp_path, template="{file}#{line} {old}=>{succ}")
    _retired(graph, successor="goal:g20")
    _node(graph, "hypothesis:h1", parents="[goal:g-retired]")

    assert links.main(["links", "--root", str(graph)]) == 0
    out = capsys.readouterr().out
    assert "retired: 1 live reference(s)" in out
    assert ".agi/nodes/hypothesis/h1.md#4 goal:g-retired=>goal:g20" in out

    assert links.main(["links", "--strict", "--root", str(graph)]) == 1
