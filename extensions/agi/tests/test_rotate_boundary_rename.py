# test_rotate_boundary_rename.py -- L5.02: rotate.py WIRES the already-
# defined-but-never-called `_apply_staged` into the ROTATION BOUNDARY
# (hypothesis:l5-rotate-wires-apply-staged-into-the-rotation-boundary).
# Fixture-proven with a fake tmux seam, no live pane, throwaway tmp_path:
#   1. boundary apply re-derives the fresh table, seats the successor under
#      the NEW name, consumes the stage; a second call is a no-op.
#   2. drift (a surface appears after staging) refuses by name, stage intact.
#   3. a dirty tree refuses by name, stage intact, nothing applied.
#   4. a missing `view-<old>` tmux session counts `skipped`, never a red.
#   5. the rotation record carries `applied_rename`.
#   6. WIRE PROOF: `cmd_rotate_self`'s boundary callsite reaches the changed
#      bytes (a stage is visible to it) -- a helper-only unit test is not
#      wire proof.
import argparse
import contextlib as _c
import io
import json
import os
import subprocess
import sys
from pathlib import Path
from types import SimpleNamespace

sys.path.insert(0, str(Path(__file__).resolve().parents[2]))
from agi.bin import rotate  # noqa: E402


def _seats(root, rows=None):
    geo = root / "nodes" / ".geometry"
    geo.mkdir(parents=True, exist_ok=True)
    lines = ["---", "id: config:seats", "seats:"]
    for r in (rows or [{"name": "old", "role": "kid"}]):
        lines.append("  - " + json.dumps(r, sort_keys=True))
    lines += ["---", "# body"]
    (geo / "seats.md").write_text("\n".join(lines) + "\n", encoding="utf-8")


def _sessions(root, old):
    made = []
    for parent, name in [
        (root / "sessions" / "seats", f"{old}.key"),
        (root / "sessions" / "seats", f"{old}.handoff.md"),
        (root / "sessions" / "quorum", f"{old}.md"),
        (root / "sessions" / "inbox", f"{old}.md"),
    ]:
        parent.mkdir(parents=True, exist_ok=True)
        p = parent / name
        p.write_text(f"content {name}\n", encoding="utf-8")
        made.append(p)
    return made


def _stage(root, old, new):
    ns = argparse.Namespace(old_name=old, new_name=new, dry_run=False,
                            now=False, apply=False, root=None)
    assert rotate.cmd_rename_post(ns, root) == 0
    return root / "sessions" / "seats" / f"{old}.rename.json"


def _fake_tmux(windows=(), sessions=()):
    calls = []

    def run(*a):
        calls.append(a)
        if a[0] == "list-windows":
            return "\n".join(f"@{i} {n}" for i, n in enumerate(windows))
        if a[0] == "list-sessions":
            return "\n".join(f"${i} {n}" for i, n in enumerate(sessions))
        return ""

    return run, calls


def _err(fn):
    buf = io.StringIO()
    with _c.redirect_stderr(buf):
        rc = fn()
    return rc, buf.getvalue()


def test_boundary_apply_seats_new_name_consumes_stage(tmp_path):
    _seats(tmp_path)
    made = _sessions(tmp_path, "old")
    _stage(tmp_path, "old", "new")
    tmux, calls = _fake_tmux(windows=["old"], sessions=["view-old"])
    rec = {}
    rc, err = _err(lambda: rotate._apply_staged(
        tmp_path, "old", boundary=True, run_tmux=tmux, record=rec))
    assert rc == 0, err
    for p in made:
        assert not p.exists(), f"old surface left: {p}"
        assert (p.parent / p.name.replace("old", "new", 1)).exists()
    # stage consumed; a second boundary call is a no-op
    assert not (tmp_path / "sessions" / "seats" / "old.rename.json").exists()
    assert rotate._apply_staged(tmp_path, "old") == 0
    # the fake tmux seam renamed by resolved @id / $id
    assert ("rename-window", "-t", "@0", "new") in calls
    assert ("rename-session", "-t", "$0", "view-new") in calls
    ar = rec["applied_rename"]
    assert ar["old"] == "old" and ar["new"] == "new"
    assert ar["applied"] > 0
    assert any(s["kind"] == "tmux window" for s in ar["surfaces"])
    assert all(set(s) == {"kind", "src", "dst", "action"}
               for s in ar["surfaces"])


def test_boundary_drift_refuses_and_leaves_stage(tmp_path):
    _seats(tmp_path)
    _sessions(tmp_path, "old")
    stage = _stage(tmp_path, "old", "new")
    # TWO new old-named files appear AFTER staging: the fresh table carries
    # surfaces the staged plan never did -- drift, refused by name.
    for extra in ("old.extra", "old.second"):
        (tmp_path / "sessions" / "inbox" / extra).write_text(
            "x", encoding="utf-8")
    rc, err = _err(lambda: rotate._apply_staged(tmp_path, "old",
                                                boundary=True))
    assert rc == 2, err
    assert "staged plan drifted" in err
    assert err.count("rename-post REFUSED: staged plan drifted") == 1, err
    # the claim is a count of LINES, not of one substring: a future edit
    # that split the refusal across two stderr lines would fool the
    # substring count above.
    refusal_lines = [ln for ln in err.splitlines()
                     if "rename-post REFUSED" in ln]
    assert len(refusal_lines) == 1, err
    # and "once" must not be bought by gutting the message: both drifted
    # surfaces are still named in that single line.
    assert "old.extra" in refusal_lines[0], err
    assert "old.second" in refusal_lines[0], err
    assert stage.exists(), "stage must stay intact on drift"
    assert (tmp_path / "sessions" / "seats" / "old.key").exists()
    assert not (tmp_path / "sessions" / "seats" / "new.key").exists()


def test_boundary_dirty_tree_refuses_by_name(tmp_path):
    _seats(tmp_path)
    _sessions(tmp_path, "old")
    stage = _stage(tmp_path, "old", "new")
    tracked = tmp_path / "tracked.txt"
    tracked.write_text("a\n", encoding="utf-8")
    for cmd in (["init", "-q", "."], ["config", "user.email", "t@t"],
                ["config", "user.name", "t"], ["add", "-A"],
                ["commit", "-qm", "init"]):
        subprocess.run(["git", "-C", str(tmp_path), *cmd], check=True,
                       capture_output=True)
    tracked.write_text("a\nb\n", encoding="utf-8")     # a REAL dirt
    rc, err = _err(lambda: rotate._apply_staged(tmp_path, "old",
                                                boundary=True))
    assert rc == 2, err
    assert "dirty tree" in err and "tracked.txt" in err
    assert stage.exists(), "stage must stay intact on a dirty tree"
    assert (tmp_path / "sessions" / "seats" / "old.key").exists()
    assert not (tmp_path / "sessions" / "seats" / "new.key").exists()


def test_missing_view_session_is_skipped_not_a_red(tmp_path):
    _seats(tmp_path)
    _sessions(tmp_path, "old")
    _stage(tmp_path, "old", "new")
    # the fake tmux knows the window but NO `view-old` session (no livestream)
    tmux, calls = _fake_tmux(windows=["old"], sessions=[])
    rec = {}
    rc, err = _err(lambda: rotate._apply_staged(
        tmp_path, "old", boundary=True, run_tmux=tmux, record=rec))
    assert rc == 0, err
    assert not any(c[0] == "rename-session" for c in calls)
    assert rec["applied_rename"]["skipped"] >= 1
    assert (tmp_path / "sessions" / "seats" / "new.handoff.md").exists()
    assert not (tmp_path / "sessions" / "seats" / "old.rename.json").exists()


def _graph_ready(tmp_path):
    """Make `tmp_path` itself a graph root (a legacy config marker is enough:
    write.py's API resolves root descend-only) and declare the config schema
    so the `self_row` carve-out admits the seated row write."""
    (tmp_path / "agi-tree.config.json").write_text(
        '{"metric_primary": "x"}', encoding="utf-8")
    schemas = tmp_path / "context" / "schemas"
    schemas.mkdir(parents=True, exist_ok=True)
    (schemas / "[config].md").write_text(
        "---\nname: config\nwritten_by: [owner, prime_director]\n"
        "self_row: {list_key: seats, match_key: name, fields: [session_ref, "
        "session_name, session_id, generation, window, pid, pubkey, "
        "sig_scheme, enc_scheme, key_history, session_label]}\n---\nbody\n",
        encoding="utf-8")


def _rotate_self_args(tmp_path, **over):
    base = dict(name="adv-alive", force=False, timeout=5, debug_file=None,
                model=None, effort=None, settings=None, prompt_file=None,
                tmux_session="t", window_path=None, dry_run=False,
                throwaway=False, successor_argv=None, role="parent")
    base.update(over)
    return SimpleNamespace(**base)


def _ladder(tmp_path, monkeypatch):
    monkeypatch.setattr(rotate, "find_project_root", lambda: tmp_path)
    monkeypatch.setattr(rotate, "load_ladder_field",
                        lambda r, f, d: {"director_context_tokens": 100_000,
                                         "director_rotate_at": 0.25}.get(f, d))
    g = tmp_path / "nodes" / ".geometry"
    g.mkdir(parents=True, exist_ok=True)
    (g / "rotations.md").write_text(
        "---\nid: config:rotations\ntype: config\ntemplates:\n"
        "  parent: {brief_file: extensions/agi/briefs/parent-successor.md, "
        "steps: [handoff, spawn], telemetry: [seat]}\n---\n\nbody\n",
        encoding="utf-8")


def test_cmd_rotate_self_dry_run_shows_boundary_and_touches_nothing(
        tmp_path, monkeypatch, capsys):
    """WIRE PROOF (D6): with a stage present, `cmd_rotate_self --dry-run`
    takes the boundary branch at the live callsite and touches NOTHING (no
    apply, no stage unlink)."""
    _seats(tmp_path, [{"name": "adv-alive", "role": "parent"}])
    _sessions(tmp_path, "adv-alive")
    stage = _stage(tmp_path, "adv-alive", "adv-new")
    _ladder(tmp_path, monkeypatch)
    rc, err = _err(lambda: rotate.cmd_rotate_self(
        _rotate_self_args(tmp_path, dry_run=True), tmp_path))
    out = capsys.readouterr().out
    assert rc == 0, (err, out)
    assert "(0.9) rename boundary" in out, (out, err)
    assert stage.exists(), "dry-run must touch nothing"
    assert (tmp_path / "sessions" / "seats" / "adv-alive.key").exists()


def test_cmd_rotate_self_boundary_seats_new_name_and_consumes_stage(
        tmp_path, monkeypatch, capsys):
    """WIRE PROOF (D6), the non-dry-run callsite: with a stage present,
    `cmd_rotate_self` applies it before the spawn, CONSUMES the stage and
    hands `spawn_window` the NEW name -- so the successor is seated under the
    new name, never the old one."""
    import send as _send
    _graph_ready(tmp_path)
    _seats(tmp_path, [{"name": "adv-alive", "role": "parent",
                       "model": "x", "effort": "max", "settings": ""}])
    _sessions(tmp_path, "adv-alive")
    (tmp_path / "sessions" / "seats").mkdir(parents=True, exist_ok=True)
    _send._seat_key_path(tmp_path, "adv-alive").write_text(
        json.dumps({"scheme": "ed25519", "priv_hex": "00",
                    "pub_hex": "00"}), encoding="utf-8")
    _ladder(tmp_path, monkeypatch)
    (tmp_path / "sessions" / "quorum").mkdir(parents=True, exist_ok=True)
    (tmp_path / "sessions" / "quorum" / "adv-alive.md").write_text(
        "# card\n", encoding="utf-8")
    stage = _stage(tmp_path, "adv-alive", "adv-new")
    win = tmp_path / "windows.txt"
    win.write_text("adv-alive\n", encoding="utf-8")
    seen = {}

    def fake_spawn(**kw):
        seen["name"] = kw["name"]
        with open(win, "a", encoding="utf-8") as fh:
            fh.write("adv-new\n")
        return 0, "echo hi"

    monkeypatch.setattr(rotate, "spawn_window", fake_spawn)
    monkeypatch.setattr(rotate, "_read_ack",
                        lambda *a, **k: {"seat": "s", "gen_after": 1,
                                         "answer": "continue"})
    monkeypatch.setattr(rotate, "_kill_window", lambda *a, **k: None)
    rc, err = _err(lambda: rotate.cmd_rotate_self(
        _rotate_self_args(tmp_path, window_path=str(win),
                          session_ref="adv-alive-9"), tmp_path))
    assert rc == 0, err
    assert seen.get("name") == "adv-new", seen
    assert not stage.exists(), "stage must be consumed by the boundary"
    assert (tmp_path / "sessions" / "seats" / "adv-new.handoff.md").exists()
    # D4: the rotation record carries the applied surfaces.
    recs = sorted(p for p in (tmp_path / "sessions" / "rotations")
                  .glob("*.json") if p.name != "sequence.json")
    assert recs, "no rotation record"
    rec = json.loads(recs[-1].read_text(encoding="utf-8"))
    assert rec.get("applied_rename", {}).get("new") == "adv-new", rec
    assert rec["applied_rename"]["applied"] >= 0


def test_rc_label_and_stored_row_cell_carry_the_new_name(tmp_path, monkeypatch):
    """L5.02 CLOSE of the `--remote-control` label conjunct: after a boundary
    rename the successor's app-GUI identity is the NEW name -- the exact
    parent probe that FAILED (`rc_name == 'adv-alive'`). The stored row's
    `session_label` cell must AGREE with it, because the seats ROW `name`
    itself stays a printed `ship` line (the round never writes config); the
    row lookup resolves through the `old -> new` `aliases:` bridge while the
    label is passed explicitly."""
    import send as _send
    _graph_ready(tmp_path)
    _seats(tmp_path, [{"name": "adv-alive", "role": "parent",
                       "model": "x", "effort": "max", "settings": ""}])
    _sessions(tmp_path, "adv-alive")
    (tmp_path / "sessions" / "seats").mkdir(parents=True, exist_ok=True)
    _send._seat_key_path(tmp_path, "adv-alive").write_text(
        json.dumps({"scheme": "ed25519", "priv_hex": "00",
                    "pub_hex": "00"}), encoding="utf-8")
    _ladder(tmp_path, monkeypatch)
    (tmp_path / "sessions" / "quorum").mkdir(parents=True, exist_ok=True)
    (tmp_path / "sessions" / "quorum" / "adv-alive.md").write_text(
        "# card\n", encoding="utf-8")
    _stage(tmp_path, "adv-alive", "adv-new")
    win = tmp_path / "windows.txt"
    win.write_text("adv-alive\n", encoding="utf-8")
    seen = {}

    def fake_spawn(**kw):
        seen["name"] = kw["name"]
        seen["rc_name"] = kw.get("rc_name")
        with open(win, "a", encoding="utf-8") as fh:
            fh.write("adv-new\n")
        return 0, "echo hi"

    monkeypatch.setattr(rotate, "spawn_window", fake_spawn)
    monkeypatch.setattr(rotate, "_read_ack",
                        lambda *a, **k: {"seat": "s", "gen_after": 1,
                                         "answer": "continue"})
    monkeypatch.setattr(rotate, "_kill_window", lambda *a, **k: None)
    rc, err = _err(lambda: rotate.cmd_rotate_self(
        _rotate_self_args(tmp_path, window_path=str(win),
                          session_ref="adv-alive-9"), tmp_path))
    assert rc == 0, err
    # THE PROBE THAT FAILED: the --remote-control name is the NEW name.
    assert seen.get("rc_name") == "adv-new", seen
    assert seen.get("name") == "adv-new", seen
    # the stored cell AGREES; the row `name` itself stays the old name.
    rows = [r for r in rotate._load_seats(tmp_path) if r.get("name") == "adv-alive"]
    assert rows and rows[0].get("session_label") == "adv-new", rows
    assert not any(r.get("name") == "adv-new"
                   for r in rotate._load_seats(tmp_path))


# ---- L5.16: the successor key is minted UNDER the NEW name ----------------
# hypothesis:l5-spawn-mints-the-successor-key-under-the-row-name-not-the-
# renamed-seat. Before the fix the successor key was written to the ROW's
# pre-rename path while the successor process ran with AGI_SEAT=<new>, so
# `send` resolved `<new>.key` and found the PREDECESSOR key (or nothing) and
# could not sign as the renamed seat. The Prime patched it by hand at 22:43Z.


def _mk_real_key(root, seat):
    """A REAL ed25519 seat key at `<sessions>/seats/<seat>.key` (0600)."""
    from agi.bin import send
    d = send._seats_dir(root)
    d.mkdir(parents=True, exist_ok=True)
    sch = send.seatsig.get("ed25519")
    priv, pub = sch.keygen()
    p = d / f"{seat}.key"
    p.write_text(json.dumps({"scheme": "ed25519",
                             "priv_hex": priv.hex()}), encoding="utf-8")
    os.chmod(p, 0o600)
    return p, priv.hex(), pub.hex()


def test_rotate_successor_key_mints_under_new_name_and_preserves_old(tmp_path):
    """UNIT: `key_seat` targets the successor file at the NEW name while the
    PREDECESSOR is read from the seat's own (old-name) key file; the
    predecessor bytes are PRESERVED beside it, never destroyed by the
    replace. A no-rename mint is byte-identical to before (no backup)."""
    from agi.bin import send
    old_key, pred_priv, pred_pub = _mk_real_key(tmp_path, "old")
    row = {"pubkey": pred_pub, "role": "parent", "sig_scheme": "ed25519"}
    out = rotate._rotate_successor_key(tmp_path, "old", row, key_seat="new",
                                       gen_before=3, gen_after=4)
    assert out is not None and out["pending_key"]["path"] == str(
        send._seat_key_path(tmp_path, "new"))
    # DEFERRED: the predecessor file is untouched by the mint alone.
    assert old_key.read_text() == json.dumps(
        {"scheme": "ed25519", "priv_hex": pred_priv})
    # the boundary's rename-file action moves old -> new; then the gated apply.
    os.replace(old_key, send._seat_key_path(tmp_path, "new"))
    applied = rotate._apply_successor_key_pending(out["pending_key"])
    new_key = send._seat_key_path(tmp_path, "new")
    assert str(new_key) in applied
    assert oct(os.stat(new_key).st_mode & 0o777) == oct(0o600)
    assert json.loads(new_key.read_text())["priv_hex"] == (
        out["pending_key"]["priv_hex"])
    bak = tmp_path / "sessions" / "seats" / "new.key.gen3-pre-rename"
    assert bak.is_file(), "predecessor key must be preserved"
    assert json.loads(bak.read_text())["priv_hex"] == pred_priv
    assert oct(os.stat(bak).st_mode & 0o777) == oct(0o600)


def test_rotate_successor_key_no_rename_is_unchanged(tmp_path):
    """The fix is a NO-OP without a rename: the successor lands at
    `<seat>.key` exactly as before and NO `-pre-rename` sibling appears."""
    from agi.bin import send
    key, pred_priv, pred_pub = _mk_real_key(tmp_path, "solo")
    out = rotate._rotate_successor_key(
        tmp_path, "solo", {"pubkey": pred_pub, "role": "helper"},
        gen_before=0, gen_after=1)
    assert out["pending_key"]["path"] == str(key)
    assert not out["pending_key"].get("pred_path")
    rotate._apply_successor_key_pending(out["pending_key"])
    assert json.loads(key.read_text())["priv_hex"] != pred_priv
    assert not list((tmp_path / "sessions" / "seats").glob(
        "*pre-rename")), "a no-rename rotation writes no backup"


def test_rename_rotation_successor_signs_as_the_new_seat(
        tmp_path, monkeypatch, capsys):
    """WIRE PROOF, the whole chain through `cmd_rotate_self`: a keyed seat
    with a staged rename mints its successor key at `<new>.key`, the row's
    `pubkey` cell names that successor, and a signing call as
    `AGI_SEAT=<new>` (send._sign_line resolves `<new>.key`) VERIFIES under
    the row's pubkey. Fails on the unfixed code, where `<new>.key` holds the
    predecessor key moved there by the boundary."""
    from agi.bin import send
    _graph_ready(tmp_path)
    _sessions(tmp_path, "adv-alive")
    # AFTER `_sessions` (which lays down a throwaway `adv-alive.key`): a REAL
    # key, so the successor half actually mints.
    _, pred_priv, pred_pub = _mk_real_key(tmp_path, "adv-alive")
    _seats(tmp_path, [{"name": "adv-alive", "role": "parent",
                       "model": "x", "effort": "max", "settings": "",
                       "pubkey": pred_pub, "sig_scheme": "ed25519"}])
    _ladder(tmp_path, monkeypatch)
    (tmp_path / "sessions" / "quorum").mkdir(parents=True, exist_ok=True)
    (tmp_path / "sessions" / "quorum" / "adv-alive.md").write_text(
        "# card\n", encoding="utf-8")
    stage = _stage(tmp_path, "adv-alive", "adv-new")
    win = tmp_path / "windows.txt"
    win.write_text("adv-alive\n", encoding="utf-8")

    def fake_spawn(**kw):
        with open(win, "a", encoding="utf-8") as fh:
            fh.write("adv-new\n")
        return 0, "echo hi"

    monkeypatch.setattr(rotate, "spawn_window", fake_spawn)
    monkeypatch.setattr(rotate, "_read_ack",
                        lambda *a, **k: {"seat": "s", "gen_after": 1,
                                         "answer": "continue"})
    monkeypatch.setattr(rotate, "_kill_window", lambda *a, **k: None)
    rc, err = _err(lambda: rotate.cmd_rotate_self(
        _rotate_self_args(tmp_path, window_path=str(win),
                          session_ref="adv-alive-9"), tmp_path))
    assert rc == 0, err
    assert not stage.exists()
    new_key = send._seat_key_path(tmp_path, "adv-new")
    assert new_key.is_file(), "successor key must land under the NEW name"
    assert oct(os.stat(new_key).st_mode & 0o777) == oct(0o600)
    new_priv = json.loads(new_key.read_text())["priv_hex"]
    sch = send.seatsig.get("ed25519")
    new_pub = sch.public_from_secret(bytes.fromhex(new_priv)).hex()
    assert new_pub != pred_pub
    # the signing path AGREES with the row's pubkey cell.
    rows = rotate._load_seats(tmp_path)
    row = next(r for r in rows if r.get("name") == "adv-alive")
    assert row.get("pubkey") == new_pub, row
    # the predecessor key was preserved, not destroyed.
    baks = list((tmp_path / "sessions" / "seats").glob(
        "adv-new.key.gen*-pre-rename"))
    assert len(baks) == 1, baks
    assert json.loads(baks[0].read_text())["priv_hex"] == pred_priv
    # a process running as AGI_SEAT=adv-new can sign as that seat.
    ts, to, text = "2026-09-17T00:00:00Z", "belam", "hello"
    sig_line = send._sign_line(tmp_path, "adv-new", ts, to, text)
    assert sig_line and sig_line.startswith("sig: ed25519:"), sig_line
    sig_hex = sig_line.rsplit(":", 1)[1]
    assert sch.verify(bytes.fromhex(new_pub),
                      send._canonical_msg(ts, "adv-new", to, text).encode(),
                      bytes.fromhex(sig_hex))
    # the successor is NOT addressed by the old name any more.
    old_path = send._seat_key_path(tmp_path, "adv-alive")
    assert not old_path.exists() or json.loads(
        old_path.read_text())["priv_hex"] != new_priv
