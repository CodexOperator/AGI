"""L4.110 prime ruling B — the generic `self_row` write rule in write.py.

A config node whose schema declares `self_row` lets a SEATED (non-prime,
non-owner) writer update exactly ONE thing: its OWN row (the row whose
`match_key` equals the seat its role resolved from) and only the declared
`fields`. Every prime-only field and every other row is refused WHOLE.
The rule is generic — it reads `self_row` from the schema bytes, with no
`config:seats` literal in the enforcement path. Tested on a fixture root;
never touches the live .agi/nodes/.geometry/seats.md.
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
import node_writer  # noqa: E402

# The shipped self_row declaration — kept byte-for-byte in sync with
# .agi/context/schemas/[config].md so the test pins the real schema.
SELF_ROW_SCHEMA = """---
name: config
written_by: [owner, prime_director]
self_row: {list_key: seats, match_key: name, fields: [session_ref, generation, window]}
---
config
"""

# The LIVE schema file, so the test pins the real bytes the suite ships — a
# hand copy here would drift from the schema the prime reviews at merge-up.
# Checkout root is parents[3] (tests -> agi -> extensions -> checkout root).
LIVE_SCHEMA = (Path(__file__).resolve().parents[3] / ".agi" /
                "context" / "schemas" / "[config].md")

ROWS = [
    {"name": "belam", "role": "prime_director", "model": "claude-opus-5",
     "session_ref": "aca130", "generation": 0, "window": ""},
    {"name": "sanctuary-director", "role": "director",
     "model": "claude-opus-5", "session_ref": "9daa5a", "generation": 0,
     "window": ""},
    {"name": "sanctuary-helper", "role": "director",
     "model": "claude-sonnet-5", "session_ref": "9d073a", "generation": 0,
     "window": ""},
]


def _write_seats_node(project, rows=None):
    import yaml  # noqa: F401  (present in the engine env)
    d = project / "nodes" / ".geometry"
    d.mkdir(parents=True, exist_ok=True)
    body = "\n".join(f"  - {r!r}" for r in (rows if rows is not None else ROWS))
    (d / "seats.md").write_text(
        "---\nid: config:seats\nmint_id: 3e88873e3c204c5088f6ab81322a26de\n"
        "type: config\nparents:\n  - goal:g17\nseats:\n" + body +
        "\n---\n\n# config:seats\n\nfixture body\n")


@pytest.fixture()
def project(tmp_path: Path) -> Path:
    root = tmp_path
    agi = root / ".agi"
    agi.mkdir(parents=True, exist_ok=True)
    (agi / "config.json").write_text("{}")
    sd = agi / "context" / "schemas"
    sd.mkdir(parents=True)
    if LIVE_SCHEMA.exists():
        (sd / "[config].md").write_text(LIVE_SCHEMA.read_text(encoding="utf-8"))
    else:
        (sd / "[config].md").write_text(SELF_ROW_SCHEMA)
    _write_seats_node(agi)
    return agi  # the graph root (.agi), which is what find_project_root returns


def _set_seats_edit(rows):
    e = write.Edit("config:seats")
    write.verb_set(e, "seats", _repr(rows))
    return e


def _repr(obj):
    import json
    return json.dumps(obj)


def _clone_rows():
    return [dict(r) for r in ROWS]


def test_seated_writer_may_update_own_session_ref(project):
    """ACCEPTANCE (L4.110): a seated director writes session_ref on its OWN
    row and nothing else -> admitted, written."""
    new = _clone_rows()
    new[1]["session_ref"] = "NEWREF123"
    res = write.submit(project, _set_seats_edit(new), actor="sanctuary-director-4e")
    assert res.status == node_writer.UPDATED
    text = (project / "nodes/.geometry/seats.md").read_text()
    assert "NEWREF123" in text


def test_seated_writer_refused_when_touching_model(project):
    """REFUSAL (L4.110): the same seated director touching `model` on its own
    row is refused WHOLE, naming the prime-only field."""
    new = _clone_rows()
    new[1]["model"] = "claude-sonnet-5"  # not in the self_row fields
    with pytest.raises(write.EditError) as ei:
        write.submit(project, _set_seats_edit(new), actor="sanctuary-director-4e")
    msg = str(ei.value)
    assert "prime/owner-only" in msg  # names the prime-only field
    assert "model" in msg


def test_seated_writer_refused_touching_another_row(project):
    """A seated writer may not touch another seat's row at all."""
    new = _clone_rows()
    new[2]["session_ref"] = "OTHERREF"  # sanctuary-helper's row
    with pytest.raises(write.EditError):
        write.submit(project, _set_seats_edit(new), actor="sanctuary-director-4e")


def test_seated_writer_refused_own_row_generation_via_unlisted_field(project):
    """generation IS declared, so it is allowed on the own row; role is prime-
    only and refuses."""
    new = _clone_rows()
    new[1]["role"] = "malware"
    with pytest.raises(write.EditError) as ei:
        write.submit(project, _set_seats_edit(new), actor="sanctuary-director-4e")
    assert "prime/owner-only" in str(ei.value)


def test_owner_still_writes_whole_list_model_and_all(project):
    """OWNER / PRIME keep the full write — the carve-out must not shrink them."""
    new = _clone_rows()
    new[1]["model"] = "claude-opus-6"
    new[0]["session_ref"] = "PRIMMOVE"
    res = write.submit(project, _set_seats_edit(new), actor="owner")
    assert res.status == node_writer.UPDATED