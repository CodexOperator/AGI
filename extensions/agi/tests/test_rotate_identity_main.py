"""hypothesis:l4-a-seats-identity-cell-has-one-writer-and-it-writes-main —
KID 1, clause (a). FIXTURE-ROOT proofs, never the live seats row, never the
live tmux server.

A fake main checkout + a linked git worktree; a rotation is performed from the
worktree (a `_successor_row_write` through the ONE `_write_identity_cells`
writer) with NO merge-up. FALSIFIER: MAIN's row still carrying the OLD @id.
After the fix MAIN's row must carry the NEW @id and the worktree's row must be
byte-identical to before. The send/heal READERS that resolve a live @id/pid
must also read MAIN (the same copy the writer wrote), never the worktree copy.
"""
import json
from pathlib import Path
import subprocess

import pytest

import rotate  # noqa: E402


def _write_seats(root, rows):
    """Write config:seats at `<root>/nodes/.geometry/seats.md` (graph root)."""
    gp = root / "nodes" / ".geometry"
    gp.mkdir(parents=True, exist_ok=True)
    body = "---\nid: config:seats\ntype: config\nseats:\n"
    for r in rows:
        body += "  - " + json.dumps(r) + "\n"
    body += "---\n"
    (gp / "seats.md").write_text(body, encoding="utf-8")


def _write_schema(root):
    schemas = root / "context" / "schemas"
    schemas.mkdir(parents=True, exist_ok=True)
    (schemas / "[config].md").write_text(
        "---\nname: config\nwritten_by: [owner, prime_director]\n"
        "self_row: {list_key: seats, match_key: name, "
        "fields: [session_ref, session_id, generation, window, pid]}\n"
        "---\nbody\n", encoding="utf-8")


def _make_main_and_worktree(tmp_path):
    """A main checkout + one linked worktree, both with a real `.agi` graph
    carrying config:seats with a seat row at OLD window. Returns
    `(main, wt, seat)`."""
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
    _write_schema(repo / ".agi")
    _write_seats(repo / ".agi", [{"name": seat, "role": "parent",
                                  "window": "@OLD", "pid": 100,
                                  "generation": 3}])
    subprocess.run(["git", "-C", str(repo), "add", "-A"], check=True,
                   capture_output=True)
    subprocess.run(["git", "-C", str(repo), "commit", "-m", "init"],
                   check=True, capture_output=True)
    wt = tmp_path / "wt"
    subprocess.run(["git", "-C", str(repo), "worktree", "add",
                    "-b", "loop/x-a@s1", str(wt), "season/s1"],
                   check=True, capture_output=True)
    return repo, wt, seat


def _seat_window(root, seat):
    for r in rotate._load_seats(root):
        if r.get("name") == seat:
            return r.get("window")
    return None


def test_identity_writer_rotates_from_worktree_writes_main(
        tmp_path):
    """FALSIFIER: a worktree-driven rotation with NO merge-up must leave the
    NEW @id in MAIN's row, and the worktree copy byte-identical to before."""
    main, wt, seat = _make_main_and_worktree(tmp_path)
    wt_seats = wt / ".agi" / "nodes" / ".geometry" / "seats.md"
    before = wt_seats.read_bytes()

    out = rotate._successor_row_write(
        wt / ".agi", actor=seat, seat=seat, role="parent",
        session_ref="ref-1", generation=4, window="@NEW")

    assert out.startswith("config:seats row")
    # MAIN's row carries the NEW @id.
    assert _seat_window(main / ".agi", seat) == "@NEW", (
        "the identity writer must write MAIN's seats row, not the worktree's")
    # the worktree copy is byte-identical to before (never written).
    assert wt_seats.read_bytes() == before, (
        "a worktree rotation must never touch the worktree's own seats.md on "
        "the identity cells")


def test_identity_writer_ack_backfill_from_worktree_writes_main(tmp_path):
    """The ack back-fill routes through the SAME one writer: from the worktree
    it writes MAIN, not the worktree copy."""
    main, wt, seat = _make_main_and_worktree(tmp_path)
    wt_seats = wt / ".agi" / "nodes" / ".geometry" / "seats.md"
    before = wt_seats.read_bytes()

    out = rotate._backfill_session_ref(
        wt / ".agi", seat=seat, role="parent", ref="ack-ref",
        pid=101, session_id="sess-x")

    assert out.startswith("back-filled")
    row = next(r for r in rotate._load_seats(main / ".agi")
               if r.get("name") == seat)
    assert row["session_ref"] == "ack-ref"
    assert row["session_id"] == "sess-x"
    assert row["pid"] == 101
    assert wt_seats.read_bytes() == before


def test_send_locally_loaded_rows_reads_main_from_a_worktree(tmp_path):
    """send.py's `_locally_loaded_rows` (the working-tree fallback that
    resolves a live @id/pid for wake/nudge/sig) reads MAIN from a worktree
    seat, so it addresses the row the rotation wrote."""
    import send  # noqa: E402
    main, wt, seat = _make_main_and_worktree(tmp_path)
    # rotate from the worktree: MAIN's row advances, worktree's stays OLD.
    rotate._successor_row_write(
        wt / ".agi", actor=seat, seat=seat, role="parent",
        session_ref="r", generation=5, window="@NEW")

    rows = send._locally_loaded_rows(wt / ".agi")
    row = next(r for r in rows if r.get("name") == seat)
    assert row["window"] == "@NEW", (
        "a sender in a worktree must read MAIN's seats row, not the worktree's "
        "stale copy")


def test_heal_live_seat_row_takes_identity_from_main(tmp_path):
    """heal.py's `_live_seat_row` takes the IDENTITY cells from MAIN while the
    other cells stay live-first, so a worktree seat's row is judged dead by
    the CURRENT (main-written) @id/pid, not its stale worktree copy."""
    import heal  # noqa: E402
    main, wt, seat = _make_main_and_worktree(tmp_path)
    # the worktree copy carries a STALE live window @OLD; MAIN has @NEW.
    wrow = next(r for r in rotate._load_seats(wt / ".agi")
                if r.get("name") == seat)
    wrow["window"] = "@OLD"      # stale worktree copy
    wrow["pubkey"] = "livekey"   # a NON-identity cell, live-first only
    _write_seats(wt / ".agi", [wrow])
    rotate._successor_row_write(
        wt / ".agi", actor=seat, seat=seat, role="parent",
        session_ref="r", generation=6, window="@NEW", pid=200)

    got = heal._live_seat_row(wt / ".agi", seat, rotate)
    assert got is not None
    # identity cells from MAIN (the @id/pid the rotation actually wrote).
    assert got["window"] == "@NEW"
    assert got["pid"] == 200
    # non-identity cells stay live-first (from the worktree copy).
    assert got["pubkey"] == "livekey"