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
    # a NEW old-named file appears AFTER staging: the fresh table carries a
    # surface the staged plan never did -- drift, refused by name.
    (tmp_path / "sessions" / "inbox" / "old.extra").write_text("x",
                                                               encoding="utf-8")
    rc, err = _err(lambda: rotate._apply_staged(tmp_path, "old",
                                                boundary=True))
    assert rc == 2, err
    assert "staged plan drifted" in err
    assert "old.extra" in err
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
