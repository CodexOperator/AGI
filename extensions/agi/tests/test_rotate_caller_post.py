"""hypothesis:l5-rotate-accepts-the-pending-successor-key-the-signer-already-
prefers, conjunct (2) -- the HELD-KEY CHECK reads the tree the identity WRITER
writes (MAIN, via rotate._shared_graph_root), never the rotating post's lagging
worktree copy, and falls back to the worktree copy only when MAIN has no row
for the seat. Conjunct (3): the row's `pubkey` cell is the ONLY authority -- a
pubkey that appears only in `key_history` (retired keys, SM.128) never
authorizes a rotation.

Falsifiers: (a) a rotate refuses when MAIN names the held key while the
worktree copy is stale; (b) a rotate ACCEPTS when only the stale worktree copy
names it; (c) a key found only in `key_history` authorizes; (d) MAIN-as-root
changes behaviour (root == shared root must be a no-op).
"""
import json
import subprocess
import sys
from pathlib import Path

sys.path.insert(0, str(Path(__file__).resolve().parents[2]))
import rotate  # noqa: E402
import send  # noqa: E402


def _write_seats(root, rows):
    gp = root / "nodes" / ".geometry"
    gp.mkdir(parents=True, exist_ok=True)
    body = "---\nid: config:seats\ntype: config\nseats:\n"
    for r in rows:
        body += "  - " + json.dumps(r) + "\n"
    body += "---\n"
    (gp / "seats.md").write_text(body, encoding="utf-8")


def _make(tmp_path):
    """A real MAIN checkout + a linked worktree. The seat's own `.key` file
    (in the ONE shared sessions dir, MAIN) holds pub B (`pub_b`); an unrelated
    keypair gives pub A (`pub_a`). Returns (main, wt, seat, pub_a, pub_b)."""
    repo = tmp_path / "main"
    repo.mkdir(parents=True)
    subprocess.run(["git", "-C", str(repo), "init", "-b", "season/s1"],
                   check=True, capture_output=True)
    for cfg in ("user.email", "user.name"):
        subprocess.run(["git", "-C", str(repo), "config", cfg, "t"],
                       check=True, capture_output=True)
    (repo / ".agi" / "nodes").mkdir(parents=True)
    (repo / ".agi" / "config.json").write_text('{"metric_primary": "x"}')
    seat = "s-director"
    _p_b, pub_b = send._mint_seat_key(repo / ".agi", seat, "ed25519")
    _p_a, pub_a = send._mint_seat_key(repo / ".agi", "unrelated", "ed25519")
    wt = tmp_path / "wt"
    _write_seats(repo / ".agi", [{"name": seat, "role": "director",
                                  "window": "@OLD", "pid": 100, "generation": 3,
                                  "worktree": str(wt), "pubkey": pub_b.hex()}])
    subprocess.run(["git", "-C", str(repo), "add", "-A"], check=True,
                   capture_output=True)
    subprocess.run(["git", "-C", str(repo), "commit", "-m", "init"],
                   check=True, capture_output=True)
    subprocess.run(["git", "-C", str(repo), "worktree", "add",
                    "-b", "loop/x-a@s1", str(wt), "season/s1"],
                   check=True, capture_output=True)
    return repo, wt, seat, pub_a.hex(), pub_b.hex()


def _call_as_worktree(wt, monkeypatch):
    """Resolve the caller from inside the worktree (no env seat)."""
    for k in ("AGI_POST", "AGI_SEAT"):
        monkeypatch.delenv(k, raising=False)
    monkeypatch.setattr(rotate, "_git_toplevel", lambda _c: wt)
    return rotate._caller_post(wt / ".agi")


def _rows(seat, wt, pubkey, **extra):
    row = {"name": seat, "role": "director", "window": "@OLD", "pid": 100,
           "generation": 3, "worktree": str(wt), "pubkey": pubkey}
    row.update(extra)
    return [row]


def test_main_fresh_worktree_stale_resolves(tmp_path, monkeypatch):
    """(a) MAIN's row names the held key B; the worktree COPY is stale (A).
    PRE-FIX this refused at rotate._caller_hold_key -- the held key IS B."""
    repo, wt, seat, pub_a, pub_b = _make(tmp_path)
    _write_seats(repo / ".agi", _rows(seat, wt, pub_b))    # the ONE writer's tree
    _write_seats(wt / ".agi", _rows(seat, wt, pub_a))      # the lagging copy
    post, row, how = _call_as_worktree(wt, monkeypatch)
    assert post == seat and how == "worktree", (post, how)
    assert row["pubkey"] == pub_b, "the resolved row must come from MAIN"


def test_main_stale_worktree_fresh_refuses(tmp_path, monkeypatch):
    """(b) MAIN is stale (A) and only the worktree copy names the held key B.
    The held-key check must REFUSE by name -- MAIN is the authority."""
    repo, wt, seat, pub_a, pub_b = _make(tmp_path)
    _write_seats(repo / ".agi", _rows(seat, wt, pub_a))
    _write_seats(wt / ".agi", _rows(seat, wt, pub_b))
    post, row, why = _call_as_worktree(wt, monkeypatch)
    assert (post, row) == (None, None)
    assert "fingerprint" in why and seat in why


def test_key_history_only_pubkey_never_authorizes(tmp_path, monkeypatch):
    """(c) the row's `pubkey` cell is the ONLY authority: a key that sits only
    in `key_history` (retired) does not authorize. Held key = A; row names B;
    key_history lists A."""
    repo, wt, seat, pub_a, pub_b = _make(tmp_path)
    _write_seats(repo / ".agi", _rows(seat, wt, pub_b, key_history=[pub_a]))
    _write_seats(wt / ".agi", _rows(seat, wt, pub_b, key_history=[pub_a]))
    # swap the seat's `.key` so the caller HOLDS the retired key A
    sk = send._seat_key_path(repo / ".agi", seat)
    sk.write_bytes(send._seat_key_path(repo / ".agi", "unrelated").read_bytes())
    post, row, why = _call_as_worktree(wt, monkeypatch)
    assert (post, row) == (None, None), "a key_history pubkey must not authorize"
    assert "fingerprint" in why and seat in why


def test_seat_absent_from_main_falls_back_to_worktree(tmp_path, monkeypatch):
    """The fallback: when MAIN has rows but NO row for the seat, the worktree
    copy is read (and its held key accepted)."""
    repo, wt, seat, pub_a, pub_b = _make(tmp_path)
    _write_seats(repo / ".agi", [{"name": "someone-else", "role": "director"}])
    _write_seats(wt / ".agi", _rows(seat, wt, pub_b))
    post, row, how = _call_as_worktree(wt, monkeypatch)
    assert post == seat and how == "worktree", (post, how)


def test_main_as_root_is_a_no_op(tmp_path, monkeypatch):
    """(d) from MAIN itself `_shared_graph_root` is the identity, so the read
    root is MAIN's own graph and resolution is byte-identical."""
    repo, wt, seat, pub_a, pub_b = _make(tmp_path)
    _write_seats(repo / ".agi", _rows(seat, wt, pub_b))
    assert rotate._seat_read_root(repo / ".agi", seat) == repo / ".agi"
    monkeypatch.setenv("AGI_POST", seat)
    monkeypatch.delenv("AGI_SEAT", raising=False)
    post, row, how = rotate._caller_post(repo / ".agi")
    assert post == seat and how == "env"
