"""hypothesis:l5-a-message-that-did-not-land... — a dotted `set` key must
write NESTED or be refused BY NAME.

Measured defect 2b0ea2284: `write.py set comms.foo 1` landed the FLAT
frontmatter literal key `"comms.foo"` instead of nesting under `comms`, so
every nested reader (`_comms_config`) read the default and the write was
silent in both directions.

The chosen write shape is REFUSAL: the flat literal is forbidden, and the
caller writes the parent mapping as one JSON object (`set comms '{"foo": 1}'`)
— the same shape the rotate-defaults round settled on.
"""
from __future__ import annotations

import sys
from pathlib import Path

import pytest

BIN = Path(__file__).resolve().parent.parent / "bin"
SRC = Path(__file__).resolve().parent.parent / "src"
sys.path.insert(0, str(BIN))
sys.path.insert(0, str(SRC))

import write  # noqa: E402


@pytest.fixture()
def project(tmp_path: Path) -> Path:
    graph = tmp_path / ".agi"
    (graph / "nodes" / "hypothesis").mkdir(parents=True)
    (graph / "config.json").write_text("{}")
    (graph / "nodes" / "hypothesis" / "h1.md").write_text(
        '---\nid: "hypothesis:h1"\ntype: hypothesis\nmint_id: abc123\n'
        'title: "t"\ntestable_claim: "c"\nscaffold_hash: deadbeef\n'
        'status: pending\n---\n\nthe body\n')
    return graph


def test_set_refuses_a_dotted_key_by_name_and_writes_nothing_flat():
    e = write.Edit("hypothesis:h1")
    with pytest.raises(write.EditError, match="comms.x"):
        write.verb_set(e, "comms.x", "1")
    # the forbidden outcome: a flat literal key in the accumulated edit.
    assert e.set_fm == {}


def test_dotted_key_cli_refuses_naming_the_key(project, capsys):
    rc = write.main(["hypothesis:h1", "set comms.x 1", "--root", str(project)])
    assert rc == 2, capsys.readouterr()
    out, err = capsys.readouterr()
    assert "comms.x" in err, err
    text = (project / "nodes" / "hypothesis" / "h1.md").read_text()
    assert "comms.x" not in text          # no flat literal landed
    assert "\ncomms:" not in text


def test_parent_mapping_as_one_object_nests(project):
    """The sanctioned shape: the parent map is set as ONE JSON value."""
    e = write.Edit("hypothesis:h1")
    write.verb_set(e, "comms", '{"x": 1}')
    write.submit(project, e, actor="t")
    text = (project / "nodes" / "hypothesis" / "h1.md").read_text()
    assert "comms.x" not in text
    assert "x: 1" in text
