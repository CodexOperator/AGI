import os
import sys
from pathlib import Path

import pytest

sys.path.insert(0, str(Path(__file__).resolve().parents[2]))
from agi.bin import rotate
from agi.bin import send


def _write_geo(tmp_path, rows, rotations=None):
    """A fixture root: tmp_path is the GRAPH dir, so seats live at
    <root>/nodes/.geometry/posts.md (post-first) and the shared key/card dirs
    resolve to <root>/sessions/. A row dict carries name/role/worktree/pubkey."""
    geo = tmp_path / "nodes" / ".geometry"
    geo.mkdir(parents=True, exist_ok=True)
    lines = ["---", "id: config:posts", "posts:"]
    for r in rows:
        lines.append(f"  - name: {r['name']}")
        lines.append(f"    role: {r['role']}")
        if r.get("worktree"):
            lines.append(f"    worktree: {r['worktree']}")
        if r.get("pubkey"):
            lines.append(f"    pubkey: {r['pubkey']}")
    lines.append("---")
    (geo / "posts.md").write_text("\n".join(lines) + "\n", encoding="utf-8")
    if rotations is not None:
        (geo / "rotations.md").write_text(rotations, encoding="utf-8")


def _mint(root, seat):
    """Mint a seat key like test_rotate/test_send; returns (path, pubhex)."""
    path, pub = send._mint_seat_key(root, seat, "ed25519")
    assert path is not None
    return path, pub.hex()


def _keyed_posts(root, spec):
    """Rows for `spec` = [(name, role), ...]; every row minted a key and the
    committed row's pubkey set from it (the holds-the-key requirement)."""
    rows = []
    for name, role in spec:
        _p, pubhex = _mint(root, name)
        rows.append({"name": name, "role": role, "pubkey": pubhex})
    return rows


# --- (1)/(2) identity resolution -----------------------------------------
def test_env_identity_resolves_keyed_post(tmp_path, monkeypatch):
    rows = _keyed_posts(tmp_path, [("prime", "prime_director"),
                                   ("director", "director")])
    _write_geo(tmp_path, rows)
    monkeypatch.setenv("AGI_POST", "director")
    monkeypatch.delenv("AGI_SEAT", raising=False)
    post, row, how = rotate._caller_post(tmp_path)
    assert post == "director"
    assert row["role"] == "director"
    assert how == "env"


def test_worktree_identity_resolves_post(tmp_path, monkeypatch):
    rows = _keyed_posts(tmp_path, [("wl", "director"),
                                   ("other", "director")])
    rows[0]["worktree"] = "/wptree/a"
    _write_geo(tmp_path, rows)
    monkeypatch.delenv("AGI_POST", raising=False)
    monkeypatch.delenv("AGI_SEAT", raising=False)
    monkeypatch.setattr(rotate, "_git_toplevel",
                        lambda _c: Path("/wptree/a"))
    post, row, how = rotate._caller_post(tmp_path)
    assert post == "wl"
    assert row["role"] == "director"
    assert how == "worktree"


def test_no_identity_refuses_naming_both_sources(tmp_path, monkeypatch):
    rows = _keyed_posts(tmp_path, [("prime", "prime_director")])
    _write_geo(tmp_path, rows)
    monkeypatch.delenv("AGI_POST", raising=False)
    monkeypatch.delenv("AGI_SEAT", raising=False)
    monkeypatch.setattr(rotate, "_git_toplevel", lambda _c: None)
    post, row, why = rotate._caller_post(tmp_path)
    assert (post, row) == (None, None)
    assert "AGI_SEAT" in why and "--post" in why


# --- (3)/(4) key-holder gate ---------------------------------------------
def test_unkeyed_post_refuses_keygen(tmp_path, monkeypatch):
    # an UNKEYED row (no pubkey cell) is refused by name: mint a key but the
    # row carries no pubkey.
    _write_geo(tmp_path, [{"name": "fresh", "role": "director"}])
    monkeypatch.setenv("AGI_POST", "fresh")
    monkeypatch.delenv("AGI_SEAT", raising=False)
    post, row, why = rotate._caller_post(tmp_path)
    assert (post, row) == (None, None)
    assert "fresh" in why and "unkeyed" in why and "keygen fresh" in why


def test_mismatched_key_refuses_fingerprints(tmp_path, monkeypatch):
    # row keyed with pub X but the <seat>.key file holds a DIFFERENT private
    # key Y -> the resolver refuses, naming both fingerprints (the falsifier:
    # never read a key file without comparing its pub to the committed row).
    rows = _keyed_posts(tmp_path, [("k1", "director")])
    _write_geo(tmp_path, rows)
    _p2, _ = _mint(tmp_path, "other")          # a second, unrelated key
    (tmp_path / "sessions" / "seats" / "k1.key").write_bytes(
        (tmp_path / "sessions" / "seats" / "other.key").read_bytes())
    monkeypatch.setenv("AGI_POST", "k1")
    monkeypatch.delenv("AGI_SEAT", raising=False)
    post, row, why = rotate._caller_post(tmp_path)
    assert (post, row) == (None, None)
    assert "fingerprint" in why and "k1" in why


# --- (5) ranks ------------------------------------------------------------
def test_ranks_default_or_node(tmp_path):
    rows = _keyed_posts(tmp_path, [("p", "prime_director")])
    _write_geo(tmp_path, rows)
    assert rotate._ranks(tmp_path) == ["prime_director", "director", "helper"]
    assert rotate._ranks(tmp_path) == rotate.DEFAULT_RANKS
    _write_geo(tmp_path, rows, rotations=(
        "---\nid: config:rotations\nranks:\n  - king\n  - director\n"
        "  - helper\n---\n"))
    assert rotate._ranks(tmp_path) == ["king", "director", "helper"]


# --- (6) rank gate ---------------------------------------------------------
def test_rank_gate_self_and_higher_are_allowed(tmp_path):
    rows = _keyed_posts(tmp_path, [("prime", "prime_director"),
                                   ("director", "director")])
    _write_geo(tmp_path, rows)
    r = {x["name"]: x for x in rows}
    ranks = rotate._ranks(tmp_path)
    # self carve-out AND caller strictly higher
    assert rotate._rank_gate(r["prime"], r["prime"], ranks) is None
    assert rotate._rank_gate(r["prime"], r["director"], ranks) is None


def test_rank_gate_equal_and_upward_refused(tmp_path):
    rows = _keyed_posts(tmp_path, [("d1", "director"), ("d2", "director"),
                                   ("prime", "prime_director")])
    _write_geo(tmp_path, rows)
    r = {x["name"]: x for x in rows}
    ranks = rotate._ranks(tmp_path)
    eq = rotate._rank_gate(r["d1"], r["d2"], ranks)
    assert eq is not None and "equal rank" in eq
    up = rotate._rank_gate(r["d1"], r["prime"], ranks)
    assert up is not None and "refuse upward" in up and "prime" in up


# --- (7) role timeout -------------------------------------------------------
def test_role_timeout_from_template_or_default(tmp_path):
    rows = _keyed_posts(tmp_path, [("d", "director")])
    _write_geo(tmp_path, rows)
    assert rotate._role_timeout(tmp_path, "director") == 600  # no cell yet
    _write_geo(tmp_path, rows, rotations=(
        "---\nid: config:rotations\ntemplates:\n  director:\n"
        "    timeout_s: 900\n---\n"))
    assert rotate._role_timeout(tmp_path, "director") == 900


# --- (8) stops default ------------------------------------------------------
def test_default_stops_text_slot_and_missing(tmp_path):
    _write_geo(tmp_path, [{"name": "s1", "role": "director"}])
    card = tmp_path / "sessions" / "quorum" / "s1.md"
    card.parent.mkdir(parents=True, exist_ok=True)
    card.write_text("# card\n\nlead\n\n## 🔴 Where it stops\nrun the suite "
                    "and report\n", encoding="utf-8")
    text, how = rotate._default_stops_text(tmp_path, "s1")
    assert text == "run the suite and report"
    assert "Where it stops" in how
    # a card with no slot -> (None, why)
    card.write_text("# card\nlead\n", encoding="utf-8")
    text, why = rotate._default_stops_text(tmp_path, "s1")
    assert text is None and "no where-it-stops slot" in why

def test_role_timeout_digit_string_accepted_other_strings_fall_back(tmp_path, monkeypatch):
    """Seat re-cut at the SL7.114 harvest (parent probe B): a digit-only string
    is the shape a quoted yaml cell yields and is accepted; any other string,
    a float or a bool falls back to 600."""
    import rotate as r
    cases = {"900": 900, "9x": 600, " 42 ": 42, "": 600}
    for raw, want in cases.items():
        monkeypatch.setattr(r, "_load_templates",
                            lambda root, _raw=raw: {"director": {"timeout_s": _raw}})
        assert r._role_timeout(tmp_path, "director") == want, raw
    monkeypatch.setattr(r, "_load_templates", lambda root: {"director": {"timeout_s": 9.5}})
    assert r._role_timeout(tmp_path, "director") == 600
    monkeypatch.setattr(r, "_load_templates", lambda root: {"director": {"timeout_s": True}})
    assert r._role_timeout(tmp_path, "director") == 600
