"""SM.125 path_max -- paths.py audit is a read-only lister of box literals.

hypothesis:l4-config-max-and-template-max-are-required-verdict-fields-of-
every-merge-up-review-and-a-named-line-of-every-dispatch-order. The audit's
names and its allowlist come from the `box` cells on `.agi/config.json` read
through boxes.py -- never a second hardcoded list. Fixtures live under tmp
only; nothing here reads the live tree or writes a file.
"""
from __future__ import annotations

import json
import sys
from pathlib import Path

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


def _graph(tmp_path: Path, **over) -> Path:
    graph = tmp_path / "graph"
    graph.mkdir()
    box = dict(CELLS)
    box.update(over)
    (graph / "config.json").write_text(json.dumps({"box": box}))
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
        "{root}|{logs}|{tmux}|{user}", CELLS
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
    graph = tmp_path / "graph"
    graph.mkdir()
    (graph / "config.json").write_text(json.dumps({"box": {}}))
    src = tmp_path / "src"
    src.mkdir()
    (src / "a.py").write_text("tmux = 'box-session'\n")
    rc, out = _run(capsys, ["audit", str(src), "--root", str(graph)])
    assert rc == 2, (rc, out)
    assert "missing box cells" in out


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


def test_box_schema_names_the_cells_once(tmp_path):
    """Residue 3 (config_max): the four cell names are declared in
    [box].md and READ from there by boxes.py -- not a third hardcoded list."""
    import yaml
    import frontmatter
    schema = Path(__file__).resolve().parents[3] / ".agi/context/schemas/[box].md"
    fm = yaml.safe_load(frontmatter.split_frontmatter(schema.read_text())[0]) or {}
    assert set((fm.get("fields") or {}).keys()) == set(CELLS)


def test_live_config_declares_the_four_cells():
    graph = Path(__file__).resolve().parents[3] / ".agi"
    cells = boxes.box_cells(graph)
    assert set(cells) == set(CELLS)
    assert all(cells[k] for k in CELLS), cells
