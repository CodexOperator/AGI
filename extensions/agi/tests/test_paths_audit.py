"""SM.125 path_max -- paths.py audit is a read-only lister of box literals.

hypothesis:l4-config-max-and-template-max-are-required-verdict-fields-of-
every-merge-up-review-and-a-named-line-of-every-dispatch-order. The audit's
names and its allowlist come from the `box` cells on `.agi/config.json` read
through boxes.py -- never a second hardcoded list. Fixtures live under tmp
only; nothing here reads the live tree or writes a file.
"""
from __future__ import annotations

import json
import subprocess
import sys
from pathlib import Path

import pytest

BIN = Path(__file__).resolve().parents[1] / "bin"
sys.path.insert(0, str(BIN))

import boxes  # noqa: E402
import paths  # noqa: E402

CELLS = {
    "root": "/srv/box/repo",
    "logs_dir": "/srv/box/logs",
    "tmux_session": "box-session",
    "user": "boxuser",
}

SCHEMA = """---
fields:
  root: {type: str}
  logs_dir: {type: str}
  tmux_session: {type: str}
  user: {type: str}
placeholders:
  root: root
  logs: logs_dir
  tmux: tmux_session
  user: user
---
"""


def _write_schema(graph: Path, text: str = SCHEMA) -> None:
    d = graph / "context" / "schemas"
    d.mkdir(parents=True, exist_ok=True)
    (d / "[box].md").write_text(text)


def _graph(tmp_path: Path, **over) -> Path:
    graph = tmp_path / "graph"
    graph.mkdir()
    box = dict(CELLS)
    box.update(over)
    (graph / "config.json").write_text(json.dumps({"box": box}))
    _write_schema(graph)
    return graph


def _run(capsys, argv) -> tuple[int, str]:
    rc = paths.main(argv)
    return rc, capsys.readouterr().out


def test_audit_exits_1_and_names_file_line_class(tmp_path, capsys):
    graph = _graph(tmp_path)
    src = tmp_path / "src"
    src.mkdir()
    (src / "a.py").write_text("ok = 1\nhome = '/home/someone/x'\n")
    rc, out = _run(capsys, ["audit", str(src), "--root", str(graph)])
    assert rc == 1
    assert f"{src / 'a.py'}:2: home: home = '/home/someone/x'" in out


def test_audit_exits_0_on_clean_tree(tmp_path, capsys):
    graph = _graph(tmp_path)
    src = tmp_path / "src"
    src.mkdir()
    (src / "a.py").write_text("ok = 1\n")
    rc, out = _run(capsys, ["audit", str(src), "--root", str(graph)])
    assert (rc, out) == (0, "")


def test_box_cells_and_placeholder_resolver(tmp_path):
    graph = _graph(tmp_path)
    assert boxes.box_cells(graph) == CELLS
    assert boxes.resolve_placeholders(
        "{root}|{logs}|{tmux}|{user}", CELLS, graph
    ) == "/srv/box/repo|/srv/box/logs|box-session|boxuser"


def test_allowlist_comes_from_the_cells_not_a_second_list(tmp_path, capsys):
    graph = _graph(tmp_path, allow=["allowed.py"])
    src = tmp_path / "src"
    src.mkdir()
    (src / "allowed.py").write_text("h = '/home/someone/x'\n")
    (src / "other.py").write_text("h = '/home/someone/x'\n")
    assert "allowed.py" in boxes.allow_paths(graph)
    rc, out = _run(capsys, ["audit", str(src), "--root", str(graph)])
    assert rc == 1
    assert "other.py:1: home:" in out
    assert "allowed.py" not in out


def test_unset_cells_refuse_a_clean_pass(tmp_path, capsys):
    """Residue 1 (fail closed): a graph whose box cells are absent must NEVER
    report the logs/tmux/user classes clean by silence. The audit exits 2 --
    distinct from the 1 a real finding uses -- and names the missing cells."""
    graph = _graph(tmp_path, root="", logs_dir="", tmux_session="", user="")
    src = tmp_path / "src"
    src.mkdir()
    (src / "a.py").write_text("tmux = 'box-session'\n")
    rc, out = _run(capsys, ["audit", str(src), "--root", str(graph)])
    assert rc == 2, (rc, out)
    assert "missing box cells" in out


def test_findings_refuses_unset_cells_by_name(tmp_path):
    """Residue 1b: the refusal must live in findings() itself, not only in
    main()'s pre-check. A caller that reaches findings() directly must be told
    which cell is unset, never handed a clean [] by silence."""
    graph = _graph(tmp_path, root="")
    with pytest.raises(ValueError) as err:
        paths.findings(graph)
    assert "root" in str(err.value)


def test_audit_without_dir_reaches_the_repo_top(tmp_path, capsys):
    """Residue 4 (wire): with no dir, `paths.py audit` must list the whole
    REPO the graph describes -- resolved with locations.repo_root -- not only
    the graph's own `.agi/` subtree. The engine baselines under
    extensions/agi/bin were invisible to the audit before this."""
    repo = tmp_path / "repo"
    (repo / ".agi").mkdir(parents=True)
    (repo / ".agi" / "config.json").write_text(json.dumps({"box": dict(CELLS)}))
    _write_schema(repo / ".agi")
    ext = repo / "extensions" / "agi" / "bin"
    ext.mkdir(parents=True)
    (ext / "x.py").write_text("work = 1\nhome = '/home/someone/x'\n")
    subprocess.run(["git", "init", "-q", str(repo)], check=True)
    subprocess.run(["git", "-C", str(repo), "add", "-A"], check=True)
    rc, out = _run(capsys, ["audit", "--root", str(repo / ".agi")])
    assert rc == 1, (rc, out)
    assert f"{ext / 'x.py'}:2: home:" in out


def test_path_shaped_logs_dir_literal_is_caught(tmp_path, capsys):
    """Residue 2 (mur's regex bug): a cell value that BEGINS WITH A SLASH --
    exactly what logs_dir is today -- could never match under a word boundary.
    The logs class was silently dead for every path-shaped cell."""
    graph = _graph(tmp_path, logs_dir="/home/ubuntu/logs")
    src = tmp_path / "src"
    src.mkdir()
    (src / "a.py").write_text("log = '/home/ubuntu/logs/x.log'\n")
    rc, out = _run(capsys, ["audit", str(src), "--root", str(graph)])
    assert rc == 1, (rc, out)
    assert f"{src / 'a.py'}:1: logs:" in out


def test_declared_cell_name_drives_the_classifier(tmp_path, capsys):
    """Residue 3b: the classifier's key names must come from [box].md, so a
    declaration that names the cell `logs` (not `logs_dir`) still REPORTS a
    matching literal -- never a class gone dark behind a disagreeing schema."""
    graph = tmp_path / "graph"
    graph.mkdir()
    (graph / "context" / "schemas").mkdir(parents=True)
    (graph / "context" / "schemas" / "[box].md").write_text(
        "---\nfields:\n  root: {type: str}\n  logs: {type: str}\n"
        "  tmux_session: {type: str}\n  user: {type: str}\n---\n")
    (graph / "config.json").write_text(json.dumps(
        {"box": {"root": "/srv/box/repo", "logs": "/srv/x/logs",
                 "tmux_session": "box-session", "user": "boxuser"}}))
    src = tmp_path / "src"
    src.mkdir()
    (src / "a.py").write_text("log = '/srv/x/logs/a.log'\n")
    rc, out = _run(capsys, ["audit", str(src), "--root", str(graph)])
    assert rc == 1, (rc, out)
    assert f"{src / 'a.py'}:1: logs:" in out


def test_box_schema_names_the_cells_once(tmp_path):
    """Residue 3 (config_max): the four cell names are declared in
    [box].md and READ from there by boxes.py -- not a third hardcoded list."""
    import yaml
    import frontmatter
    schema = Path(__file__).resolve().parents[3] / ".agi/context/schemas/[box].md"
    fm = yaml.safe_load(frontmatter.split_frontmatter(schema.read_text())[0]) or {}
    assert set((fm.get("fields") or {}).keys()) == set(CELLS)


def test_audit_refuses_an_absent_box_schema(tmp_path, capsys):
    """Conjunct 1 (gate): a graph with NO [box].md must refuse the audit by
    name -- never pass with an empty cell set. Exit 3 is distinct from the 1
    a real finding uses and the 2 an unset cell uses."""
    graph = tmp_path / "graph"
    graph.mkdir()
    (graph / "config.json").write_text(json.dumps({"box": dict(CELLS)}))
    src = tmp_path / "src"
    src.mkdir()
    (src / "a.py").write_text("ok = 1\n")
    rc, out = _run(capsys, ["audit", str(src), "--root", str(graph)])
    assert rc == 3, (rc, out)
    assert "[box].md" in out


def test_audit_refuses_a_schema_with_no_cells(tmp_path, capsys):
    """Conjunct 1 (gate): a [box].md that declares no `fields` is equally
    unable to classify -- the audit refuses and NAMES the schema."""
    graph = tmp_path / "graph"
    (graph / "context" / "schemas").mkdir(parents=True)
    (graph / "context" / "schemas" / "[box].md").write_text(
        "---\nname: box\n---\n")
    (graph / "config.json").write_text(json.dumps({"box": dict(CELLS)}))
    src = tmp_path / "src"
    src.mkdir()
    (src / "a.py").write_text("ok = 1\n")
    rc, out = _run(capsys, ["audit", str(src), "--root", str(graph)])
    assert rc == 3, (rc, out)
    assert "[box].md" in out


def test_findings_refuses_an_absent_box_schema(tmp_path):
    """Conjunct 1 (gate): the refusal lives in findings() itself, so a direct
    caller is refused by name -- never handed an empty clean [] by silence."""
    graph = tmp_path / "graph"
    graph.mkdir()
    with pytest.raises(boxes.BoxSchemaError) as err:
        paths.findings(graph)
    assert "[box].md" in str(err.value)


def test_box_schema_declares_the_placeholder_map(tmp_path):
    """Residue 5 (auth/gate): the placeholder tokens are REAL FIELDS on
    [box].md, not a comment. The schema is the one declaration of the mapping
    from a rendered token to its cell key."""
    import yaml
    import frontmatter
    schema = Path(__file__).resolve().parents[3] / ".agi/context/schemas/[box].md"
    fm = yaml.safe_load(frontmatter.split_frontmatter(schema.read_text())[0]) or {}
    assert (fm.get("placeholders") or {}) == {
        "root": "root", "logs": "logs_dir",
        "tmux": "tmux_session", "user": "user",
        "repo_root": "repo_root", "box": "box",
    }


def test_resolve_placeholders_follows_the_schema_mapping(tmp_path):
    """A schema that names a placeholder differently from any literal the
    engine once held must DRIVE the resolver -- proving the mapping is read,
    not remembered."""
    other = """---
fields:
  root: {type: str}
  log_dir: {type: str}
  tmux_session: {type: str}
  user: {type: str}
placeholders:
  root: root
  log: log_dir
  tmux: tmux_session
  user: user
---
"""
    graph = tmp_path / "graph"
    graph.mkdir()
    _write_schema(graph, other)
    got = boxes.resolve_placeholders(
        "{root}|{log}|{tmux}|{user}",
        {"root": "R", "log_dir": "L", "tmux_session": "T", "user": "U"}, graph)
    assert got == "R|L|T|U"


def test_live_config_declares_the_four_cells():
    graph = Path(__file__).resolve().parents[3] / ".agi"
    cells = boxes.box_cells(graph)
    assert set(cells) == set(CELLS)
    assert all(cells[k] for k in CELLS), cells


def test_repo_root_and_graph_root_read_the_same_cells(tmp_path):
    """A REPO root is not a graph root, but the same tree, so it reads the same.

    `box_schema_path` used to look for `context/schemas/[box].md` under the
    root it was HANDED, so a repo root got an empty cell set SILENTLY -- the
    render `resolve_placeholders` refuses to produce. It resolves the graph the
    way every other reader in the tree does (locations.py), so one tree cannot
    audit two ways depending on which root the caller passed.
    """
    repo = tmp_path / "repo"
    (repo / ".git").mkdir(parents=True)          # a repo boundary
    graph = repo / ".agi"
    graph.mkdir()
    (graph / "config.json").write_text(json.dumps({"box": dict(CELLS)}))
    _write_schema(graph)
    assert boxes.box_cells(repo) == boxes.box_cells(graph) == CELLS
    assert boxes.box_schema_path(repo) == boxes.box_schema_path(graph)


def test_a_root_with_no_graph_refuses_by_name(tmp_path):
    """Not-found resolves to the root handed in, and then it refuses."""
    plain = tmp_path / "plain"
    plain.mkdir()
    assert boxes.graph_root(plain) == plain.resolve()
    with pytest.raises(boxes.BoxSchemaError) as err:
        boxes.require_box_cells(plain)
    assert str(plain.resolve()) in str(err.value)


def test_classify_never_repeats_a_class(tmp_path):
    graph = _graph(tmp_path)
    cells = boxes.box_cells(graph)
    # `root` passed as a class AND matched by the tail: one 'box', not two.
    classes = [(k.split("_")[0], k) for k in boxes.require_box_cells(graph)]
    hits = paths.classify("see %s today" % CELLS["root"], cells, classes)
    assert hits.count("box") == 1
