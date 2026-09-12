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
from types import SimpleNamespace
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
        "fields: [session_ref, session_id, generation, window, pid, "
        "pubkey, sig_scheme, enc_scheme, key_history]}\n"
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


def test_commit_spawn_row_from_worktree_lands_in_main(tmp_path):
    """hypothesis:l4-the-spawn-row-write-and-its-commit-land-in-one-tree-
    and-the-ack-stages-only-its-own-row clause (1) -- a worktree rotation's
    ONE spawn-row commit must land in the tree the ONE writer wrote: MAIN's
    seats.md, never the caller's worktree copy (which was never touched and
    would SKIP as byte-identical). FALSIFIER: after `_commit_spawn_row`
    from the worktree, MAIN's seats.md is committed (clean) carrying the
    spawn row, and the worktree copy is byte-unchanged."""
    main, wt, seat = _make_main_and_worktree(tmp_path)
    wt_seats = wt / ".agi" / "nodes" / ".geometry" / "seats.md"
    before = wt_seats.read_bytes()

    # rotate from the worktree: the ONE writer puts the row in MAIN.
    out = rotate._successor_row_write(
        wt / ".agi", actor=seat, seat=seat, role="parent",
        session_ref="ref-1", generation=4, window="@NEW")
    assert out.startswith("config:seats row")
    assert _seat_window(main / ".agi", seat) == "@NEW"
    # MAIN's seats.md is dirty (uncommitted) -- the exact dirt a worktree
    # commit used to leave riding to the next merge-up.
    main_dirty = subprocess.run(
        ["git", "-C", str(main), "status", "--porcelain", "--",
         ".agi/nodes/.geometry/seats.md"],
        capture_output=True, text=True).stdout.strip()
    assert main_dirty, ("PRE-FIX: worktree spawn-row write leaves MAIN's "
                        "seats.md dirty")
    assert wt_seats.read_bytes() == before, (
        "a worktree rotation must never touch the worktree's own seats.md "
        "on the identity cells")

    # THE FIX: rotate-self commits it in MAIN's tree (the ONE writer's).
    outcome = rotate._commit_spawn_row(
        wt / ".agi", seat=seat, generation=4, session_id="sess-1",
        window="@NEW", pid=4242)
    assert outcome.startswith("spawn_row_commit: committed"), outcome
    # MAIN's seats.md is now committed and clean; worktree still untouched.
    ok = subprocess.run(
        ["git", "-C", str(main), "status", "--porcelain", "--",
         ".agi/nodes/.geometry/seats.md"],
        capture_output=True, text=True).stdout.strip()
    assert ok == "", "the spawn-row commit must leave MAIN's seats.md clean"
    assert wt_seats.read_bytes() == before, (
        "the spawn-row commit must never touch the worktree's seats.md")
    # the ONE commit on MAIN's seats.md since the seed carries the spawn row.
    log = subprocess.run(
        ["git", "-C", str(main), "log", "--format=%h %s", "--",
         ".agi/nodes/.geometry/seats.md"],
        capture_output=True, text=True).stdout.splitlines()
    assert len(log) == 2 and log[0].endswith(
        f"{seat} spawn row: gen 4, session_id sess-1, "
        "window @NEW, pid 4242"), log


def test_commit_spawn_row_stages_only_own_row_with_foreign_predirty(tmp_path):
    """claim (7): the spawn-row commit stages ONLY ITS OWN row. A FOREIGN
    row whose change is PRE-STAGED in MAIN's seats.md before the spawn write
    must NOT ride the spawn-row commit — the COMMITTED seats.md carries the
    own row's new cells and the foreign row's COMMITTED (HEAD) values, and
    the foreign hunk stays staged/uncommitted.
    (hypothesis:l4-the-predecessor-answers-continue-by-default-and-ask-diff-
    hands-the-successor-exactly-one-call)"""
    main, wt, seat = _make_main_and_worktree(tmp_path)
    seats_path = main / ".agi" / "nodes" / ".geometry" / "seats.md"
    # append a SECOND (foreign) row to MAIN's seats.md and PRE-STAGE it.
    text = seats_path.read_text(encoding="utf-8")
    other_hunk = ("  - {\"name\": \"other-seat\", \"role\": \"parent\", "
                  "\"window\": \"@FOREIGN\", \"pid\": 999, "
                  "\"generation\": 9}")
    seats_path.write_text(text.rstrip() + "\n" + other_hunk + "\n",
                          encoding="utf-8")
    subprocess.run(["git", "-C", str(main), "add", "--",
                    ".agi/nodes/.geometry/seats.md"], check=True,
                   capture_output=True)

    wt_seats = wt / ".agi" / "nodes" / ".geometry" / "seats.md"
    before_wt = wt_seats.read_bytes()
    # the own rotation from the worktree: ONE writer -> MAIN, row -> @NEW.
    out = rotate._successor_row_write(
        wt / ".agi", actor=seat, seat=seat, role="parent",
        session_ref="", generation=4, window="@NEW")
    assert out.startswith("config:seats row")
    outcome = rotate._commit_spawn_row(
        wt / ".agi", seat=seat, generation=4, session_id="sess-9",
        window="@NEW", pid=7777)
    assert outcome.startswith("spawn_row_commit: committed"), outcome
    assert wt_seats.read_bytes() == before_wt

    # the COMMITTED seats.md carries the own row's new window AND the OTHER
    # seat's COMMITTED (HEAD) values — never the @FOREIGN pre-staged hunk.
    head_out = subprocess.run(
        ["git", "-C", str(main), "show", "HEAD:"
         ".agi/nodes/.geometry/seats.md"],
        capture_output=True, text=True).stdout
    assert '"window": "@NEW"' in head_out          # own row committed
    assert '"window": "@FOREIGN"' not in head_out  # foreign NOT committed
    # the foreign hunk is NOT in the real index (the own-row commit re-pointed
    # it at the committed blob) but is BYTE-PRESERVED in the working tree,
    # never bundled under this post's name.
    staged = subprocess.run(
        ["git", "-C", str(main), "diff", "--cached", "--",
         ".agi/nodes/.geometry/seats.md"],
        capture_output=True, text=True).stdout
    work = seats_path.read_text(encoding="utf-8")
    assert '"window": "@FOREIGN"' not in staged, \
        "the foreign hunk must not sit in the real index as a staged change"
    assert '"window": "@FOREIGN"' in work, \
        "the foreign hunk must stay byte-preserved in the working tree"


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


def test_rotate_first_key_from_worktree_writes_main(tmp_path):
    """clause (1) / Prime XIII ask (a): an UNKEYED seat's first mint
    (`_rotate_first_key`) writes its THREE identity cells (pubkey /
    sig_scheme / enc_scheme) through the ONE identity writer into MAIN's
    seats.md, never send._row_write_submit on the caller's worktree copy.
    FALSIFIER: after a worktree post's rotate-self first-mint, MAIN's row
    pubkey == the minted key's pubkey (derived from the key file), and the
    worktree copy is byte-unchanged."""
    import send  # noqa: E402
    main, wt, seat = _make_main_and_worktree(tmp_path)
    wt_seats = wt / ".agi" / "nodes" / ".geometry" / "seats.md"
    before = wt_seats.read_bytes()

    note = rotate._rotate_first_key(
        wt / ".agi", wt / ".agi", seat, {"role": "parent"})

    assert "minted its first key" in note
    assert f"; row {seat!r} keyed" in note
    # derive the minted pubkey from the key file.
    key_path = send._seat_key_path(wt / ".agi", seat)
    assert key_path.is_file()
    obj = json.loads(key_path.read_text())
    scheme = send.seatsig.get(obj["scheme"])
    pub = scheme.public_from_secret(bytes.fromhex(obj["priv_hex"]))
    exp_pub = pub.hex()

    row = next(r for r in rotate._load_seats(main / ".agi")
               if r.get("name") == seat)
    assert row.get("pubkey") == exp_pub, (
        "the first-mint identity cells must land in MAIN's row, pubkey == "
        "the minted key's pubkey")
    assert row.get("sig_scheme") == obj["scheme"]
    assert row.get("enc_scheme")
    # worktree copy must be byte-identical -- never a second writer.
    assert wt_seats.read_bytes() == before, (
        "a worktree first-mint must never write the worktree's own seats.md")


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

def test_worktree_rotate_self_then_ack_continue_lands_in_main(tmp_path, monkeypatch, capsys):
    """g15.24 belt (2a) MANDATORY two-tree falsifier: a worktree post's
    rotate-self (the ONE writer -> MAIN's seats.md, then _commit_spawn_row in
    MAIN's tree) followed by the successor's `cmd_ack ... continue` returns
    rc 0 WITH the ack commit landing in the fixture MAIN — and the worktree
    copy is byte-unchanged through the whole round (never a second writer,
    never a commit in the caller's tree)."""
    main, wt, seat = _make_main_and_worktree(tmp_path)
    wt_seats = wt / ".agi" / "nodes" / ".geometry" / "seats.md"
    before_wt = wt_seats.read_bytes()

    # rotate-self from the worktree: the ONE writer puts the row in MAIN and
    # rotate-self commits its spawn row in MAIN's tree.
    wrote = rotate._successor_row_write(
        wt / ".agi", actor=seat, seat=seat, role="parent",
        session_ref="", generation=4, window="@NEW", pid=3200)
    assert wrote.startswith("config:seats row")
    outcome = rotate._commit_spawn_row(
        wt / ".agi", seat=seat, generation=4, session_id="sess-2",
        window="@NEW", pid=3200)
    assert outcome.startswith("spawn_row_commit: committed"), outcome
    assert wt_seats.read_bytes() == before_wt

    # the successor's wake act acks `continue` FROM the worktree; its own-row
    # gate and commit resolve against MAIN (the tree the writer wrote).
    monkeypatch.chdir(wt / ".agi")
    # mur-SL2.12 (3): the two-tree chain test points the registry at a
    # FIXTURE dir (never ~/.claude/sessions), so a fixture ack's join cannot
    # poll the real registry host.
    reg_fix = tmp_path / "reg-fixture"
    reg_fix.mkdir(exist_ok=True)
    code = rotate.cmd_ack(SimpleNamespace(
        seat=seat, gen=4, ref="new-ref", answer="continue", text="",
        wait=0, registry_dir=str(reg_fix), window_path=None), wt / ".agi")
    assert code == 0, capsys.readouterr().err
    assert wt_seats.read_bytes() == before_wt, \
        "a worktree ack must never write the worktree's own seats.md"

    # MAIN's seat row carried the spawn row AND the ack's back-fill, clean.
    row = next(r for r in rotate._load_seats(main / ".agi")
               if r.get("name") == seat)
    assert row["window"] == "@NEW"
    assert row["session_ref"] == "new-ref"
    st = subprocess.run(
        ["git", "-C", str(main), "status", "--porcelain", "--",
         ".agi/nodes/.geometry/seats.md"],
        capture_output=True, text=True).stdout.strip()
    assert st == "", "MAIN's seats.md must be clean after the ack"
    log = subprocess.run(
        ["git", "-C", str(main), "log", "--format=%h %s", "--",
         ".agi/nodes/.geometry/seats.md"],
        capture_output=True, text=True).stdout.splitlines()
    assert log[0].endswith(
        f"{seat} ack: gen 4, session_ref new-ref, window @NEW, pid 3200"), log
