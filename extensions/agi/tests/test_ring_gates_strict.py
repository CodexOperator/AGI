"""goal:g1.41 RD1 (DG1 23:32Z): the round-ring gate (dispatch._round_ring_refusal) and the suite-grant ring
gate (verification._ring_gate_refusal) answer "no ring, admit" when they COULD NOT LOOK.

Both read the rings cell with a non-strict seatsig.rings.load_rings inside `except Exception: ring = None`
and then `return None` (admit): a REAL load failure (a rings file the uid cannot read, a corrupt one, one
whose value is not a list, one whose m is not a number, a seatsig.rings that will not import) must return a
REFUSAL LINE that names the ring and the error class. Real failures, as lane D's write.py rows use, never a
stub of ring_by_name. The intended admits are the controls: a ring the geometry does not name, an absent cell.
NOTE for the builder: load_rings itself degrades an unreadable or unparseable cell to [], so an except-split
in the gates alone cannot see a mode-000 or a corrupt file: use load_rings(strict=True) or look at the cell.
"""
from __future__ import annotations

import hashlib
import os
import re
import sys
from pathlib import Path

import pytest

sys.path.insert(0, str(Path(__file__).resolve().parents[1] / "bin"))
sys.path.insert(0, str(Path(__file__).resolve().parents[1] / "src"))

import dispatch  # noqa: E402
import verification  # noqa: E402
import seatsig  # noqa: E402
from seatsig import Scheme, get, register  # noqa: E402


class _DummyScheme(Scheme):
    name = "fixture"

    def keygen(self, **kw):
        sk = b"k" * 32
        return sk, b"pub" + sk

    def sign(self, priv, msg):
        return hashlib.sha256(msg + priv).digest()[:16]

    def verify(self, pub, msg, sig):
        return sig == hashlib.sha256(msg + pub).digest()[:16]


register(_DummyScheme())
_RINGS = Path("nodes") / ".geometry" / "rings.md"


def _root(tmp_path):
    agi = tmp_path / ".agi"
    (agi / "nodes" / ".geometry").mkdir(parents=True)
    (agi / "config.json").write_text("{}", encoding="utf-8")
    (agi / _RINGS).write_text(
        "---\ntype: cell\nrings:\n  - name: approval\n    m: 2\n    members: [alice, bob, carol]\n---\n",
        encoding="utf-8")
    scheme = get("fixture")
    rows = "\n".join(f"  - name: {nm}\n    pubkey: {scheme.keygen()[0].hex()}" for nm in ("alice", "bob", "carol"))
    (agi / "nodes" / ".geometry" / "posts.md").write_text(f"---\ntype: config\nposts:\n{rows}\n---\n", encoding="utf-8")
    return agi


def _break(agi, how, monkeypatch):
    cell = agi / _RINGS
    if how == "mode000":
        os.chmod(cell, 0)
    elif how == "corrupt":
        cell.write_text("---\ntype: cell\nrings: [ {name: approval, m: 2\n---\n", encoding="utf-8")
    elif how == "not-a-list":
        cell.write_text("---\ntype: cell\nrings: approval\n---\n", encoding="utf-8")
    elif how == "bad-m":
        cell.write_text("---\ntype: cell\nrings:\n  - name: approval\n    m: abc\n    members: [alice, bob, carol]\n---\n",
                        encoding="utf-8")
    elif how == "import":
        monkeypatch.delattr(seatsig, "rings", raising=False)
        monkeypatch.setitem(sys.modules, "seatsig.rings", None)


def _round(tmp_path, ring="approval"):
    return dispatch._round_ring_refusal(str(tmp_path), ring, "kid", "", [])


def _suite(tmp_path, ring="approval"):
    return verification._ring_gate_refusal(tmp_path / ".agi", ring, "rotation", [])


GATES = [("round", _round), ("suite", _suite)]
# goal:g1.42 B5 row 9: only the mode-000 case is unobservable as root (root reads a mode-000 file); the four other cases are real under root and must RUN there.
HOWS = [pytest.param("mode000", marks=pytest.mark.skipif(os.geteuid() == 0, reason="a mode-000 file is readable by root")),
        "corrupt", "not-a-list", "bad-m", "import"]


@pytest.mark.parametrize("how", HOWS)
@pytest.mark.parametrize("gate,call", GATES, ids=[g for g, _ in GATES])
def test_rd1_a_real_rings_load_failure_is_a_refusal_naming_the_ring_and_the_error(tmp_path, monkeypatch, gate, call, how):
    agi = _root(tmp_path)
    _break(agi, how, monkeypatch)
    try:
        refusal = call(tmp_path)
    finally:
        if (agi / _RINGS).exists():
            os.chmod(agi / _RINGS, 0o644)
    assert isinstance(refusal, str) and refusal, f"{gate} gate admitted on {how}"
    assert "approval" in refusal, refusal                   # names the ring
    assert re.search(r"[A-Za-z]+Error", refusal), refusal   # names the error class


@pytest.mark.parametrize("gate,call", GATES, ids=[g for g, _ in GATES])
def test_rd1_control_a_ring_the_geometry_does_not_name_is_admitted(tmp_path, gate, call):
    _root(tmp_path)
    assert call(tmp_path, ring="ghost-ring") is None


@pytest.mark.parametrize("gate,call", GATES, ids=[g for g, _ in GATES])
def test_rd1_control_an_absent_rings_cell_is_admitted(tmp_path, gate, call):
    agi = _root(tmp_path)
    (agi / _RINGS).unlink()
    assert call(tmp_path) is None


@pytest.mark.parametrize("gate,call", GATES, ids=[g for g, _ in GATES])
def test_rd1_control_a_healthy_ring_with_no_signatures_still_refuses_on_the_count(tmp_path, gate, call):
    _root(tmp_path)
    refusal = call(tmp_path)
    assert refusal and "approval" in refusal and "got 0" in refusal, refusal


# goal:g1.41 RD4 (DG1 00:55Z, SM union1 residue): seatsig.rings.load_rings drops every non-dict row BEFORE its strict
# loop, so `rings: [approval]` (a list of STRINGS) loads as no ring at all, ring_by_name answers None and EVERY gate
# admits through the opt-out. A rings cell that holds a row which is not a ring is a cell that could not be read:
# strict loading RAISES, and each gate refuses by name. Real cells, never a stub of ring_by_name.
from seatsig import rings as _rings  # noqa: E402

_ONE = "  - name: approval\n    m: 1\n    members: [alice]\n"
_BAD_CELLS = {
    "all-strings": "rings:\n  - approval\n",
    "inline-strings": "rings: [approval, other]\n",
    "mixed": "rings:\n" + _ONE + "  - approval\n",
    "string-first": "rings:\n  - approval\n" + _ONE,
}
_BAD = list(_BAD_CELLS)


def _cell(agi, body):
    (agi / _RINGS).write_text("---\ntype: cell\n" + body + "---\n", encoding="utf-8")


@pytest.mark.parametrize("shape", _BAD)
def test_rd4_load_rings_strict_raises_on_a_row_that_is_not_a_ring(tmp_path, shape):
    agi = _root(tmp_path)
    _cell(agi, _BAD_CELLS[shape])
    with pytest.raises(Exception):
        _rings.load_rings(agi, strict=True)


@pytest.mark.parametrize("shape", _BAD)
@pytest.mark.parametrize("gate,call", GATES, ids=[g for g, _ in GATES])
def test_rd4_a_rings_cell_holding_a_non_ring_row_is_a_refusal_naming_the_ring_and_the_error(tmp_path, gate, call, shape):
    agi = _root(tmp_path)
    _cell(agi, _BAD_CELLS[shape])
    refusal = call(tmp_path)
    assert isinstance(refusal, str) and refusal, f"{gate} gate admitted on {shape}"
    assert "approval" in refusal, refusal
    assert re.search(r"[A-Za-z]+Error", refusal), refusal


def test_rd4_control_load_rings_strict_still_reads_good_cells(tmp_path):
    agi = _root(tmp_path)
    got = _rings.load_rings(agi, strict=True)
    assert [r["name"] for r in got] == ["approval"], got
    _cell(agi, "rings:\n" + _ONE + "  - name: other\n    m: 2\n    members: [alice, bob]\n")
    assert [r["name"] for r in _rings.load_rings(agi, strict=True)] == ["approval", "other"]
    _cell(agi, "rings: []\n")
    assert _rings.load_rings(agi, strict=True) == []
    (agi / _RINGS).unlink()
    assert _rings.load_rings(agi, strict=True) == []


@pytest.mark.parametrize("gate,call", GATES, ids=[g for g, _ in GATES])
def test_rd4_control_an_all_dict_list_behaves_as_today(tmp_path, gate, call):
    agi = _root(tmp_path)
    _cell(agi, "rings:\n  - name: other\n    m: 1\n    members: [alice]\n" + _ONE.replace("m: 1", "m: 2"))
    refusal = call(tmp_path)
    assert refusal and "approval" in refusal and "got 0" in refusal, refusal      # the count, not a load error
    assert call(tmp_path, ring="ghost-ring") is None                              # a ring no row names: the opt-out


@pytest.mark.parametrize("gate,call", GATES, ids=[g for g, _ in GATES])
def test_rd4_control_an_empty_rings_list_stays_the_opt_out(tmp_path, gate, call):
    agi = _root(tmp_path)
    _cell(agi, "rings: []\n")
    assert call(tmp_path) is None
