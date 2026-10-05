"""goal:g7.33.10 — body row replace-by-NAME (not line numbers).

`replace body <NAME> <path|->` selects the ONE markdown table row whose
first cell equals NAME and splices that single line. Missing or ambiguous
NAME refuses by name; a payload target never accepts a row name. Numeric
`replace body N:M` is unchanged.
"""
from __future__ import annotations

import io
import sys
from contextlib import redirect_stderr, redirect_stdout
from pathlib import Path

import pytest

pytestmark = pytest.mark.skip(reason='retired engine surface (symbol or CLI is gone); skipped instead of keeping dead code green: write row-by-name API is gone')

BIN = Path(__file__).resolve().parent.parent / "bin"
sys.path.insert(0, str(BIN))

import write  # noqa: E402
import node_writer  # noqa: E402


GOAL_BODY = """# goal:g1

| | |
|---|---|
| goal | original goal text |
| origin | original origin |
| done | original done |
| who | original who |
"""


def _project(tmp_path: Path) -> Path:
    graph = tmp_path / ".agi"
    (graph / "nodes" / "goal").mkdir(parents=True)
    (graph / "context" / "schemas").mkdir(parents=True)
    (graph / "nodes" / "goal" / "g1.md").write_text(
        '---\nid: "goal:g1"\ntype: goal\nmint_id: "g1mint"\n'
        'title: "G1: Sample goal"\ngoal_id: "G1"\ngoal_kind: perpetual\n'
        'status: active\norigin: goals-doc\nseeds: []\nconfidence: 0.5\n'
        'tags: []\n---\n<!-- BODY:BEGIN -->\n' + GOAL_BODY,
        encoding="utf-8",
    )
    (graph / "config.json").write_text("{}", encoding="utf-8")
    return graph


def test_resolve_body_row_range_finds_the_named_table_row():
    text = "| goal | a |\n|---|---|\n| done | b |\n| who | c |\n"
    assert write._resolve_body_row_range(text, "done") == "3:3"
    assert write._resolve_body_row_range(text, "goal") == "1:1"


def test_resolve_body_row_range_refuses_missing_and_ambiguous():
    text = "| done | a |\n| done | b |\n"
    with pytest.raises(write.EditError) as exc:
        write._resolve_body_row_range(text, "missing")
    assert "no table row named 'missing'" in str(exc.value)
    with pytest.raises(write.EditError) as exc:
        write._resolve_body_row_range(text, "done")
    assert "2 rows named 'done'" in str(exc.value)


def test_replace_body_by_name_rewrites_the_named_row(tmp_path):
    graph = _project(tmp_path)
    src = tmp_path / "row.txt"
    src.write_text("| done | replaced by NAME |\n", encoding="utf-8")
    before = (graph / "nodes" / "goal" / "g1.md").read_text(encoding="utf-8")
    out, err = io.StringIO(), io.StringIO()
    with redirect_stdout(out), redirect_stderr(err):
        rc = write.main([
            "goal:g1", f"replace body done {src}",
            "--root", str(graph), "--actor", "test", "--role", "prime",
        ])
    assert rc == 0, (out.getvalue(), err.getvalue())
    after = (graph / "nodes" / "goal" / "g1.md").read_text(encoding="utf-8")
    assert "| done | replaced by NAME |" in after
    assert "| done | original done |" not in after
    assert "| goal | original goal text |" in after  # other rows untouched
    assert before != after


def test_replace_body_by_name_refuses_unknown_row_and_writes_nothing(tmp_path):
    graph = _project(tmp_path)
    src = tmp_path / "row.txt"
    src.write_text("| invented | x |\n", encoding="utf-8")
    before = (graph / "nodes" / "goal" / "g1.md").read_text(encoding="utf-8")
    out, err = io.StringIO(), io.StringIO()
    with redirect_stdout(out), redirect_stderr(err):
        rc = write.main([
            "goal:g1", f"replace body invented {src}",
            "--root", str(graph), "--actor", "test", "--role", "prime",
        ])
    assert rc == 2, (out.getvalue(), err.getvalue())
    assert "no table row named 'invented'" in err.getvalue()
    assert (graph / "nodes" / "goal" / "g1.md").read_text(encoding="utf-8") == before


def test_replace_payload_by_name_is_refused(tmp_path):
    """Row-by-NAME is body-only; a payload target must keep START:END."""
    edit = write.Edit(node_id="build:x")
    with pytest.raises(write.EditError) as exc:
        write.verb_replace(edit, "payload", "done", "-")
    assert "body-only" in str(exc.value)


def test_replace_body_numeric_range_still_works(tmp_path):
    """Regression: START:END form is unchanged beside the NAME form."""
    graph = _project(tmp_path)
    # Read body to learn the line of the done row, then replace by number.
    body = write._read_body_text(str(graph), "goal:g1")
    rng = write._resolve_body_row_range(body, "who")
    src = tmp_path / "row.txt"
    src.write_text("| who | numeric path |\n", encoding="utf-8")
    out, err = io.StringIO(), io.StringIO()
    with redirect_stdout(out), redirect_stderr(err):
        rc = write.main([
            "goal:g1", f"replace body {rng} --force {src}",
            "--root", str(graph), "--actor", "test", "--role", "prime",
        ])
    assert rc == 0, (out.getvalue(), err.getvalue())
    after = (graph / "nodes" / "goal" / "g1.md").read_text(encoding="utf-8")
    assert "| who | numeric path |" in after


def test_submit_resolves_replace_row_name(tmp_path):
    graph = _project(tmp_path)
    edit = write.Edit(
        node_id="goal:g1",
        replace_target="body",
        replace_row_name="origin",
        replace_text="| origin | via submit |\n",
    )
    res = write.submit(str(graph), edit, actor="test")
    assert getattr(res, "status", "") != node_writer.REJECTED
    after = (graph / "nodes" / "goal" / "g1.md").read_text(encoding="utf-8")
    assert "| origin | via submit |" in after

def test_replace_body_by_name_dry_run_resolves_and_writes_nothing(tmp_path):
    """Dry-run must resolve NAME and print it without UnboundLocalError."""
    graph = _project(tmp_path)
    src = tmp_path / "row.txt"
    src.write_text("| done | dry |\n", encoding="utf-8")
    before = (graph / "nodes" / "goal" / "g1.md").read_text(encoding="utf-8")
    out, err = io.StringIO(), io.StringIO()
    with redirect_stdout(out), redirect_stderr(err):
        rc = write.main([
            "goal:g1", f"replace body done {src}",
            "--root", str(graph), "--actor", "test", "--role", "prime",
            "--dry-run",
        ])
    assert rc == 0, (out.getvalue(), err.getvalue())
    assert "replace body done" in out.getvalue()
    assert (graph / "nodes" / "goal" / "g1.md").read_text(encoding="utf-8") == before
