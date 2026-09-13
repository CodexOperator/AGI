"""DEFECT 4 (hypothesis:l4-...gate-sits-on-the-merge-up-push) -- the write.py
RUNG 3 HUMARM GATE fires ONLY for a config-row write OUTSIDE the writer's
OWN self_row.

The pre-fix gate ran on EVERY submit (`set_fm`/`unset_fm` are always non-None
dicts on a config-row submission), so a writer's OWN self_row write was gated
too. Now: BOTH set_fm and unset_fm empty => no gate; a self_row write is NEVER
gated; a FOREIGN config-row write (not the writer's own self_row) IS gated
while the prime scope is FROZEN, and freed by an owner answer.

Fixture root only; the live tree's config:vetoes stays empty (the gate is
read, and the fixture's own vetoes node carries the gate).
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

LIVE_SCHEMA = (Path(__file__).resolve().parents[3] / ".agi" /
                "context" / "schemas" / "[config].md")

ROWS = [
    {"name": "belam", "role": "prime_director", "model": "claude-opus-5",
     "session_ref": "aca130", "generation": 0, "window": ""},
    {"name": "sanctuary-director", "role": "director",
     "model": "claude-opus-5", "session_ref": "9daa5a", "generation": 0,
     "window": ""},
]


def _write_seats_node(project, rows=None):
    d = project / "nodes" / ".geometry"
    d.mkdir(parents=True, exist_ok=True)
    body = "\n".join(f"  - {r!r}" for r in (rows if rows is not None else ROWS))
    (d / "seats.md").write_text(
        "---\nid: config:seats\nmint_id: 3e88873e3c204c5088f6ab81322a26de\n"
        "type: config\nparents:\n  - goal:g17\nseats:\n" + body +
        "\n---\n\n# config:seats\n\nfixture body\n")


def _write_frozen_vetoes(project):
    """A FROZEN prime-scope vetoes geometry node at
    `<project>/nodes/.geometry/vetoes.md` -- the path `_enforce_written_by`
    (and the veto seam) reads from."""
    from seatsig import veto as _veto
    d = project / "nodes" / ".geometry"
    d.mkdir(parents=True, exist_ok=True)
    geom = {
        "veto_room": "veto", "rate_limit_per_window": 2,
        "window_seconds": 3600, "expiry_seconds": 86400,
        "active_gates": [{"scope": "prime", "since": "2026-09-12T00:00:00Z",
                          "reason": "council veto", "veto_ref": "veto:001",
                          "answered": ""}],
        "vetoes": [{"veto_ref": "veto:001", "scope": "prime",
                    "filed_at": "2026-09-12T00:00:00Z",
                    "expires_at": "2026-09-12T00:00:00Z", "answer": ""}],
    }
    _veto.save(project, geom, Path("nodes") / ".geometry" / "vetoes.md")


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
        (sd / "[config].md").write_text(
            "---\nname: config\nwritten_by: [owner, prime_director]\n"
            "self_row: {list_key: seats, match_key: name, "
            "fields: [session_ref, generation, window]}\n---\n")
    _write_seats_node(agi)
    return agi  # the graph root (.agi)


def _set_seats_edit(rows):
    import json
    e = write.Edit("config:seats")
    write.verb_set(e, "seats", json.dumps(rows))
    return e


def _clone_rows():
    return [dict(r) for r in ROWS]


def test_self_row_write_ungated_while_frozen(project):
    """A seated writer updating its OWN declared row (self_row) is NEVER gated
    -- even while the prime scope is FROZEN (defect 4)."""
    _write_frozen_vetoes(project)
    new = _clone_rows()
    new[1]["session_ref"] = "NEWREF"
    res = write.submit(project, _set_seats_edit(new), actor="sanctuary-director-4e")
    assert res.status == node_writer.UPDATED


def test_foreign_config_row_gated_while_frozen(project):
    """A FOREIGN config-row write (not the writer's own self_row) IS gated
    while the prime scope is FROZEN -- refused BY NAME and never auto-released;
    only an owner answer clears it (defect 4)."""
    from seatsig import veto as _veto
    _write_frozen_vetoes(project)

    # config:vetoes is not the owner's self_row -> gated while frozen
    e = write.Edit("config:vetoes")
    write.verb_set(e, "veto_room", "room2")
    with pytest.raises(write.EditError) as ei:
        write.submit(project, e, actor="owner")
    msg = str(ei.value)
    assert "human gate" in msg and "FROZEN" in msg

    # an OWNER answer clears the gate; the same foreign write now passes
    cell = Path("nodes") / ".geometry" / "vetoes.md"
    g = _veto.read(project, cell)
    freed = _veto.record_answer(g, "prime", "owner answer (fixture)")
    _veto.save(project, freed, cell)
    res = write.submit(project, e, actor="owner")
    assert res.status == node_writer.UPDATED


def test_empty_set_and_unset_gate_nothing(project):
    """Both set_fm and unset_fm EMPTY => NO human gate, even while frozen
    (defect 4: the pre-fix `if set_fm is not None` fired on EVERY submit
    because set_fm was always a non-None dict)."""
    _write_frozen_vetoes(project)
    # Direct seam call: empty set/unset under a FROZEN scope is admitted
    # (no EditError from the human gate). The pre-fix condition would fire.
    write._enforce_written_by(project, "config", "owner", "config:vetoes",
                              set_fm={}, unset_fm=[], allow_self_row=True)  # noqa
    # And NO-OP writes (empty fields, frozen) never raise either.
    assert True