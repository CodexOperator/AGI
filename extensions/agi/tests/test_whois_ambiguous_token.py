"""goal:g7.16.1.11.45.2 -- a session token two posts.md rows carry is never
answered by the first hit.

Code half: `send.whois` / `_resolve_rows` REFUSE an ambiguous token, naming every
matching row, and the refusal is a NO-MATCH (never an authorization); a token one
row carries answers exactly as before. Data half: every non-empty `session_name`
(and `session_ref`) is unique across ALL rows of the real posts.md, `-retired`
rows included. A mutant per half: the first-hit line restored -> the two-row
fixture answers with a row (RED); one row's session_name copied onto another ->
the data check names the pair (RED).
"""
from __future__ import annotations

import collections
import importlib.util
import sys
from pathlib import Path

import pytest

BIN = Path(__file__).resolve().parents[1] / "bin"
sys.path.insert(0, str(BIN))
spec = importlib.util.spec_from_file_location("send_amb", BIN / "send.py")
send = importlib.util.module_from_spec(spec)
spec.loader.exec_module(send)

POSTS = Path(__file__).resolve().parents[3] / ".agi" / "nodes" / ".geometry" / "posts.md"


def _rows(**extra):
    return [
        {"name": "director-general-3", "role": "director", "session_name": "agi-c8",
         "session_ref": "aaaa11"},
        {"name": "director-general-5-retired", "role": "director",
         "session_name": "agi-c8", "session_ref": "bbbb22"},
        {"name": "prime-x", "role": "prime_director", "session_name": "agi-01",
         "session_ref": "cccc33"},
    ]


def test_an_ambiguous_session_name_is_refused_naming_both_rows():
    code, text = send._resolve_rows(_rows(), "agi-c8", None)
    assert code == send.WHOIS_NO_MATCH, "never an authorization"
    assert "ambiguous" in text
    assert "director-general-3" in text and "director-general-5-retired" in text
    assert "SEAT:" not in text, "no first-hit answer"
    # with a claim naming the FIRST row the token is still not authorized
    code, text = send._resolve_rows(_rows(), "agi-c8", "director-general-3")
    assert code == send.WHOIS_NO_MATCH and "IS-AUTHORIZED" not in text


def test_a_session_ref_of_one_row_equal_to_the_session_name_of_another_is_ambiguous():
    rows = _rows()
    rows[2]["session_ref"] = "agi-c8"   # prime-x's ref == the shared name
    code, text = send._resolve_rows(rows, "agi-c8", None)
    assert code == send.WHOIS_NO_MATCH and "3 rows" in text


def test_a_unique_token_answers_exactly_as_before():
    code, text = send._resolve_rows(_rows(), "agi-01", None)
    assert (code, text) == (send.WHOIS_OK,
                            "SEAT: agi-01 -> seat prime-x, role prime_director")
    code, text = send._resolve_rows(_rows(), "cccc33", "prime-x")
    assert code == send.WHOIS_OK and text.startswith("IS-AUTHORIZED: cccc33 vs claim 'prime-x'")


def test_two_rows_sharing_a_session_id_prefix_are_ambiguous_too():
    rows = _rows()
    rows[0]["session_id"] = "12345678-aaaa"
    rows[2]["session_id"] = "12345678-bbbb"
    code, text = send._resolve_rows(rows, "12345678", None)
    assert code == send.WHOIS_NO_MATCH and "session_id prefix" in text
    rows[2]["session_id"] = "87654321-bbbb"
    assert send._resolve_rows(rows, "12345678", None)[0] == send.WHOIS_OK


def test_seat_mode_refuses_two_rows_with_one_name():
    rows = _rows() + [{"name": "prime-x", "role": "x", "session_ref": "dddd44"}]
    code, text = send._resolve_rows(rows, "ignored", None, target=("seat", "prime-x"))
    assert code == send.WHOIS_NO_MATCH and "ambiguous by name" in text


def test_mutant_the_first_hit_restored_answers_with_a_row(monkeypatch):
    """MUTANT: drop the ambiguity refusal -> the two-row fixture is answered by
    the first hit (RED against the real refusal above)."""
    monkeypatch.setattr(send, "_ambiguous_refusal",
                        lambda token, axis, hits: send._whois_answer(
                            hits[0], f"by {axis}", None, None))
    code, text = send._resolve_rows(_rows(), "agi-c8", None)
    assert code == send.WHOIS_OK and "director-general-3" in text, \
        "the mutant answers with a row: the refusal is what stops it"


# ---- data half: unique non-empty names across ALL rows, retired included ------
def _dupes(rows, key):
    seen = collections.defaultdict(list)
    for r in rows:
        v = r.get(key)
        if v:
            seen[v].append(r.get("name") or "?")
    return {v: names for v, names in seen.items() if len(names) > 1}


@pytest.fixture(scope="module")
def real_rows():
    return send._load_seats_rows(POSTS.read_text())


def test_every_nonempty_session_name_and_ref_is_unique_across_posts_md(real_rows):
    assert len(real_rows) > 10, "the real posts.md parsed"
    assert _dupes(real_rows, "session_name") == {}
    assert _dupes(real_rows, "session_ref") == {}


def _token_owners(rows):
    """token -> the set of row indexes carrying it in session_name OR session_ref
    (the union: the code refuses one row's session_ref == another's session_name,
    so the data must too). A row carrying the same token in both cells is ONE row."""
    owners = collections.defaultdict(set)
    for i, r in enumerate(rows):
        for key in ("session_name", "session_ref"):
            v = r.get(key)
            if v:
                owners[v].add(i)
    return owners


def test_every_token_in_session_name_union_session_ref_maps_to_one_row(real_rows):
    """FF6 (alive): the cross-field row. 0 such tokens at the tip today."""
    many = {t: sorted(real_rows[i].get("name", "?") for i in idx)
            for t, idx in _token_owners(real_rows).items() if len(idx) > 1}
    assert many == {}


def test_mutant_a_session_name_copied_into_another_rows_session_ref_is_caught(real_rows):
    rows = [dict(r) for r in real_rows]
    named = [r for r in rows if r.get("session_name")]
    victim = next(r for r in rows if r is not named[0] and not r.get("session_ref"))
    victim["session_ref"] = named[0]["session_name"]
    many = [t for t, idx in _token_owners(rows).items() if len(idx) > 1]
    assert named[0]["session_name"] in many, "the union row names the cross-field pair"
    # ... which the per-field check of the first data row would NOT have seen:
    assert _dupes(rows, "session_name") == {} and _dupes(rows, "session_ref") == {}


def test_mutant_one_session_name_copied_onto_another_row_is_caught(real_rows):
    rows = [dict(r) for r in real_rows]
    named = [r for r in rows if r.get("session_name")]
    assert len(named) >= 2
    named[1]["session_name"] = named[0]["session_name"]
    dup = _dupes(rows, "session_name")
    assert dup and named[0]["name"] in next(iter(dup.values()))


def test_whois_verb_exits_nonzero_naming_both_rows(monkeypatch):
    """Through the verb, over a pushed-rows stub: rc != 0, both rows named."""
    monkeypatch.setattr(send, "_pushed_seats",
                        lambda root, ref, do_fetch: (_rows(), "deadbeef01", "origin/x"))
    rc, text = send.whois(Path("."), "agi-c8", None)
    assert rc == send.WHOIS_NO_MATCH != 0
    assert "director-general-3" in text and "director-general-5-retired" in text


# ---- FF5: an empty token is never resolved ----------------------------------
def test_an_empty_token_is_refused_even_when_one_row_carries_the_empty_name():
    """A 2-row fixture where EXACTLY ONE row has session_name "": whois "" used
    to answer that row (RED on the old code), now NO-MATCH."""
    rows = [{"name": "a", "role": "director", "session_name": "", "session_ref": "aaaa11"},
            {"name": "b", "role": "director", "session_name": "agi-b", "session_ref": "bbbb22"}]
    for tok in ("", "   "):
        code, text = send._resolve_rows(rows, tok, None)
        assert code == send.WHOIS_NO_MATCH and "empty token" in text, (tok, code, text)
    code, text = send._resolve_rows(rows, "ignored", None, target=("seat", ""))
    assert code == send.WHOIS_NO_MATCH and "empty token" in text
    assert send._resolve_rows(rows, "agi-b", None)[0] == send.WHOIS_OK, "a real token still answers"
