"""Tests for the phase-1 closeout CARD FORM — `rotate.py closeout` and the
`rotate-self --closeout` wiring (hypothesis:l4-rotate-self-closeout-is-one-
call-a-card-form-the-llm-fills-once-then-stops-prepare-role-captive-steps-and-
the-spawn-every-step-logged-by-name, phase 1).

RED FIRST: every claim below is asserted before (and drives) the code, on a
fixture root (never the live tree):

1. **`closeout` prints ONE JSON array of slots** — the template's
   `closeout.slots` when present, the coded DEFAULT (§0-§6) when absent, each
   `{slot, prompt, current_value}` with current read from the seat's own card.
2. **`closeout --form` applies a filled array BY CODE** — the target section's
   body is replaced (header kept), a missing section is appended, and `keep`
   carries the card's current value; nothing hand-stamps a header.
3. **§3 (where-it-stops) is NOT written by the applier** — it is returned so
   the caller routes it through the existing `_write_stops_section` phase-2
   path (no second stops implementation).
4. **An unknown slot is refused BY NAME** (nothing written on refusal).
5. **The owner-quote check refuses a node reference that does not resolve**
   from the graph, BY SLOT NAME; a reference that resolves passes.
6. **A card over the trim guard (HANDOFF_CARD_LIMIT_LINES) is refused**
   naming the section to cut.
7. **A malformed form (non-JSON / non-array / non-string value) is refused.**
"""
from __future__ import annotations

import json
import sys
from pathlib import Path
from types import SimpleNamespace

import pytest

_REPO = Path(__file__).resolve().parents[3]
sys.path.insert(0, str(_REPO / "extensions"))   # the `agi` package
_BIN = _REPO / "extensions" / "agi" / "bin"
sys.path.insert(0, str(_BIN))  # so the lazy `import verification` resolves

from agi.bin import rotate  # noqa: E402


@pytest.fixture
def co_root(tmp_path):
    """A fixture GRAPH root with a small existing quorum card and one node the
    owner-quote check can resolve against."""
    (tmp_path / "nodes" / "goal").mkdir(parents=True)
    (tmp_path / "nodes" / "goal" / "g15.md").write_text(
        "---\ntype: goal\n---\nbody\n", encoding="utf-8")
    quorum = tmp_path / "sessions" / "quorum"
    quorum.mkdir(parents=True)
    (quorum / "adv-alive.md").write_text(
        "## §0 STATE (driven)\n| Field | Value |\n|---|---|\n| Meter | 0.5 |\n"
        "\n"
        "## §1 PLAN\n- one: do the thing\n"
        "\n"
        "## §2 LANDED\n- old landed\n"
        "\n"
        "### 🔴 Where it stops\n```\nbash next.sh\n```\n",
        encoding="utf-8")
    return tmp_path


def _args(**over):
    base = dict(seat="adv-alive", form=None, role=None, template=None,
                root=None)
    base.update(over)
    return SimpleNamespace(**base)


def _written_card(root):
    return (root / "sessions" / "quorum" / "adv-alive.md").read_text(
        encoding="utf-8")


def test_print_form_is_one_json_array_of_default_slots(co_root, capsys):
    rc = rotate.cmd_closeout(_args(form=None), co_root)
    out = capsys.readouterr().out.strip()
    assert rc == 0
    arr = json.loads(out)
    assert isinstance(arr, list) and len(arr) == 7
    slots = [e["slot"] for e in arr]
    assert slots == ["s0", "s1", "s2", "s3", "s4", "s5", "s6"]
    s3 = next(e for e in arr if e["slot"] == "s3")
    assert "bash next.sh" in s3["current_value"]          # read from the card
    assert s3["prompt"]


def test_print_form_reads_template_closeout_slots_when_present(co_root, capsys):
    (co_root / "nodes" / ".geometry").mkdir(parents=True, exist_ok=True)
    (co_root / "nodes" / ".geometry" / "rotations.md").write_text(
        "---\ntemplates:\n  parent:\n    closeout:\n      slots:\n"
        "        - slot: sA\n          prompt: alpha\n"
        "        - slot: sB\n          prompt: beta\n---\nbody\n",
        encoding="utf-8")
    rc = rotate.cmd_closeout(_args(form=None, role="parent"), co_root)
    arr = json.loads(capsys.readouterr().out.strip())
    assert [e["slot"] for e in arr] == ["sA", "sB"]


def test_apply_replaces_target_keeps_others_and_appends_missing(
        co_root, capsys):
    filled = json.dumps([
        {"slot": "s0", "value": "keep"},
        {"slot": "s2", "value": "- new landed"},
        {"slot": "s6", "value": "- decisions for owner"},
    ])
    filled_map, perr = rotate._closeout_parse_form(filled)
    assert perr is None
    full, s3, aerr = rotate._closeout_apply(co_root, "adv-alive", "parent",
                                            filled_map, None)
    assert aerr is None
    assert "- new landed" in full
    assert "| Meter | 0.5 |" in full            # §0 kept via `keep`
    assert "## §6 BANKED" in full and "- decisions for owner" in full
    # nothing hand-stamped a header: the driven §0 header line is untouched
    assert "## §0 STATE (driven)" in full
    assert "<!--" not in full                   # no generated stamp block


def test_apply_returns_s3_for_stops_and_writes_card(co_root):
    filled = json.dumps([
        {"slot": "s3", "value": "bash DIFF-NEXT-COMMAND.sh"},
        {"slot": "s5", "value": "- verify suite"},
    ])
    filled_map, perr = rotate._closeout_parse_form(filled)
    assert perr is None
    full, s3, aerr = rotate._closeout_apply(co_root, "adv-alive", "parent",
                                            filled_map, None)
    assert aerr is None
    assert s3 == "bash DIFF-NEXT-COMMAND.sh"
    # s3 NOT written into the card by the applier (phase-2 stops path owns it)
    written = _written_card(co_root)
    assert "DIFF-NEXT-COMMAND" not in written
    assert "- verify suite" in written          # non-s3 slot applied to card


def test_apply_keep_s3_returns_no_stops(co_root):
    filled_map, _ = rotate._closeout_parse_form(
        json.dumps([{"slot": "s3", "value": "keep"}]))
    full, s3, aerr = rotate._closeout_apply(co_root, "adv-alive", "parent",
                                            filled_map, None)
    assert aerr is None and s3 is None


def test_unknown_slot_refused_by_name(co_root):
    filled_map, _ = rotate._closeout_parse_form(
        json.dumps([{"slot": "sX", "value": "x"}]))
    full, s3, aerr = rotate._closeout_apply(co_root, "adv-alive", "parent",
                                            filled_map, None)
    assert aerr is not None and "sX" in aerr and "refused" in aerr


def test_owner_quote_unresolved_refused_by_slot(co_root):
    filled_map, _ = rotate._closeout_parse_form(
        json.dumps([{"slot": "s4", "value": "see hypothesis:zzz-nope"}]))
    full, s3, aerr = rotate._closeout_apply(co_root, "adv-alive", "parent",
                                            filled_map, None)
    assert aerr is not None and "s4" in aerr and "not found" in aerr
    # a reference that resolves passes
    filled_map, _ = rotate._closeout_parse_form(
        json.dumps([{"slot": "s4", "value": "see goal:g15"}]))
    full, s3, aerr = rotate._closeout_apply(co_root, "adv-alive", "parent",
                                            filled_map, None)
    assert aerr is None


def test_trim_guard_refused_naming_section(co_root):
    big = "\n".join(f"line {i}" for i in range(200))
    filled_map, _ = rotate._closeout_parse_form(
        json.dumps([{"slot": "s1", "value": big}]))
    full, s3, aerr = rotate._closeout_apply(co_root, "adv-alive", "parent",
                                            filled_map, None)
    assert aerr is not None and "guard" in aerr and "PLAN" in aerr


def test_malformed_form_refused(co_root):
    for text in ("not json", "[1,2]", '[{"slot":"s1"}]',
                 '[{"slot":"s1","value":7}]'):
        filled_map, perr = rotate._closeout_parse_form(text)
        assert filled_map is None and perr is not None


def test_parse_form_accepts_keep_and_unknown_slot_is_refused_by_name():
    filled_map, perr = rotate._closeout_parse_form(
        json.dumps([{"slot": "s2", "value": "keep"}]))
    assert perr is None and filled_map["s2"] == "keep"