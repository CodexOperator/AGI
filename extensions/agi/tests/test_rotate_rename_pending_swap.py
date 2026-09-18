# test_rotate_rename_pending_swap.py -- L5.16, kid 2 under
# hypothesis:l5-spawn-mints-the-successor-key-under-the-row-name-not-the-
# renamed-seat. The RESIDUAL kid 1 named and the parent confirmed as probe G:
# at a RENAME rotation whose season-branch push FAILED, the successor's
# deferred `<new>.key.pending` could never be completed, because
# `_complete_pending_key_swap`/`_signing_key_obj` look the seat up with
# `send._seat_row_in`, which does NOT resolve the ONE `aliases:` table -- and
# at a rename boundary the committed row keeps the OLD name while the
# successor runs as the NEW one. Three claims:
#   1. the deferred swap COMPLETES as the NEW name (aliases old->new);
#   2. `_sign_line` as the NEW name VERIFIES under the committed row's pubkey
#      THROUGH the deferred window (the g15.26 (c) falsifier, on the rename
#      path);
#   3. a pending whose pub_hex does NOT match the committed row is still left
#      alone (no refusal weakened), and a seat with no alias is unchanged.
import argparse
import contextlib as _c
import io
import json
import os
import sys
from pathlib import Path
from types import SimpleNamespace

sys.path.insert(0, str(Path(__file__).resolve().parents[2]))
from agi.bin import rotate  # noqa: E402
from agi.bin import send  # noqa: E402


def _geo(root, rows, aliases=None):
    """`nodes/.geometry/posts.md` -- the ONE geometry config: the `posts:`
    rows AND the Prime-written `aliases:` table (old -> new)."""
    geo = root / "nodes" / ".geometry"
    geo.mkdir(parents=True, exist_ok=True)
    lines = ["---", "id: config:posts", "posts:"]
    for r in rows:
        lines.append("  - " + json.dumps(r, sort_keys=True))
    if aliases:
        lines.append("aliases:")
        for k, v in aliases.items():
            lines.append(f"  {k}: {v}")
    lines += ["---", "# body"]
    (geo / "posts.md").write_text("\n".join(lines) + "\n", encoding="utf-8")


def _graph_ready(tmp_path):
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


def _sessions(root, old):
    for parent, name in [
        (root / "sessions" / "seats", f"{old}.key"),
        (root / "sessions" / "seats", f"{old}.handoff.md"),
        (root / "sessions" / "quorum", f"{old}.md"),
        (root / "sessions" / "inbox", f"{old}.md"),
    ]:
        parent.mkdir(parents=True, exist_ok=True)
        (parent / name).write_text(f"content {name}\n", encoding="utf-8")


def _stage(root, old, new):
    ns = argparse.Namespace(old_name=old, new_name=new, dry_run=False,
                            now=False, apply=False, root=None)
    assert rotate.cmd_rename_post(ns, root) == 0
    return root / "sessions" / "seats" / f"{old}.rename.json"


def _mk_real_key(root, seat):
    d = send._seats_dir(root)
    d.mkdir(parents=True, exist_ok=True)
    sch = send.seatsig.get("ed25519")
    priv, pub = sch.keygen()
    p = d / f"{seat}.key"
    p.write_text(json.dumps({"scheme": "ed25519",
                             "priv_hex": priv.hex()}), encoding="utf-8")
    os.chmod(p, 0o600)
    return p, priv.hex(), pub.hex()


def _rotate_self_args(**over):
    base = dict(name="adv-alive", force=False, timeout=5, debug_file=None,
                model=None, effort=None, settings=None, prompt_file=None,
                tmux_session="t", window_path=None, dry_run=False,
                throwaway=False, successor_argv=None, role="parent")
    base.update(over)
    return SimpleNamespace(**base)


def _err(fn):
    buf = io.StringIO()
    with _c.redirect_stderr(buf):
        rc = fn()
    return rc, buf.getvalue()


def _push_failed_rotation(tmp_path, monkeypatch):
    """Run `cmd_rotate_self` through a rename boundary with the season-branch
    push FAILING, and return (root, succ_pub, stage_path, committed_rows).
    The committed row keeps the OLD name and names the SUCCESSOR pubkey --
    exactly the state a push FAILED leaves behind (the row write committed,
    origin did not receive it)."""
    _graph_ready(tmp_path)
    _geo(tmp_path, [{"name": "adv-alive", "role": "parent",
                     "model": "x", "effort": "max", "settings": "",
                     "pubkey": "0" * 64, "sig_scheme": "ed25519"}],
         aliases={"adv-alive": "adv-new"})
    _sessions(tmp_path, "adv-alive")
    _, pred_priv, pred_pub = _mk_real_key(tmp_path, "adv-alive")
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
    # the push FAILED seam: the commit reached the push leg and it failed.
    monkeypatch.setattr(
        rotate, "_commit_spawn_row",
        lambda *a, **k: ("spawn_row_commit: committed (sha deadbee, "
                         "retried 0) -- own-row only: ok\n"
                         "push: push: FAILED -- simulated"))
    rc, err = _err(lambda: rotate.cmd_rotate_self(
        _rotate_self_args(window_path=str(win), session_ref="adv-alive-9"),
        tmp_path))
    assert rc == 0, err
    assert not stage.exists(), "stage must be consumed by the boundary"
    pend = send._seat_key_path(tmp_path, "adv-new")
    assert Path(str(pend) + ".pending").is_file(), "pending must be persisted"
    pobj = json.loads(Path(str(pend) + ".pending").read_text())
    succ_pub = str(pobj["pub_hex"])
    assert succ_pub and succ_pub != pred_pub
    # MAIN's committed row still reads the OLD name and names the successor.
    committed = [{"name": "adv-alive", "role": "parent", "pubkey": succ_pub,
                  "sig_scheme": "ed25519"}]
    _patch_committed_rows(monkeypatch, committed)
    return tmp_path, succ_pub, pred_priv, pred_pub


def _patch_committed_rows(monkeypatch, rows):
    """Patch `_seats_committed_rows` on BOTH module aliases: test files load
    `from agi.bin import send` while rotate.py's local `import send` resolves
    the top-level `send` -- two module objects for one file (conftest's
    documented two-alias trap). Patching one leaves the other reading the
    real (gitless, empty) rows."""
    monkeypatch.setattr(send, "_seats_committed_rows", lambda root: rows)
    try:
        import send as _top  # noqa: PLC0415
        monkeypatch.setattr(_top, "_seats_committed_rows", lambda root: rows)
    except ImportError:
        pass


def test_rename_deferred_swap_completes_and_signs_as_the_new_name(
        tmp_path, monkeypatch, capsys):
    """CLAIMS 1+2: through the deferred window the successor signs as the NEW
    name with the PENDING key and VERIFIES under the committed row's pubkey;
    `_complete_pending_key_swap` as the NEW name then atomically flips
    `<new>.key` to the pending key and deletes the `.pending`."""
    root, succ_pub, pred_priv, pred_pub = _push_failed_rotation(
        tmp_path, monkeypatch)
    sch = send.seatsig.get("ed25519")
    new_key = send._seat_key_path(root, "adv-new")
    pend = Path(str(new_key) + ".pending")
    # during the window `<new>.key` holds the PREDECESSOR (moved by the
    # boundary), so the un-fixed signer would sign with the wrong key.
    assert json.loads(new_key.read_text())["priv_hex"] == pred_priv
    ts, to, text = "2026-09-17T00:00:00Z", "belam", "hello"
    sig_line = send._sign_line(root, "adv-new", ts, to, text)
    assert sig_line and sig_line.startswith("sig: ed25519:"), sig_line
    sig_hex = sig_line.rsplit(":", 1)[1]
    assert sch.verify(bytes.fromhex(succ_pub),
                      send._canonical_msg(ts, "adv-new", to, text).encode(),
                      bytes.fromhex(sig_hex)), "must sign with the successor"
    # the deferred swap COMPLETES when addressed by the NEW name.
    done = rotate._complete_pending_key_swap(root, "adv-new")
    assert done.startswith("key swap completed"), done
    assert not pend.exists()
    assert json.loads(new_key.read_text())["priv_hex"] != pred_priv
    # the old name finds no key anymore (the boundary moved it aside).
    capsys.readouterr()


def test_wrong_pubkey_pending_is_still_left_alone(tmp_path, monkeypatch):
    """CLAIM 3 (the refusal is NOT weakened): a pending whose pub_hex does not
    match the committed row's pubkey leaves both `<new>.key` and the
    `.pending` byte-identical."""
    root, succ_pub, pred_priv, _pred_pub = _push_failed_rotation(
        tmp_path, monkeypatch)
    # the committed row names a DIFFERENT pubkey -> no match.
    _patch_committed_rows(monkeypatch, [{"name": "adv-alive",
                                         "role": "parent",
                                         "pubkey": "f" * 64,
                                         "sig_scheme": "ed25519"}])
    new_key = send._seat_key_path(root, "adv-new")
    pend = Path(str(new_key) + ".pending")
    before_key = new_key.read_bytes()
    before_pend = pend.read_bytes()
    out = rotate._complete_pending_key_swap(root, "adv-new")
    assert out.startswith("key swap NOT completed"), out
    assert new_key.read_bytes() == before_key
    assert pend.read_bytes() == before_pend


def test_no_alias_seat_row_lookup_is_unchanged(tmp_path, capsys):
    """CLAIM 3 (no-alias path): with no aliases table a seat row resolves
    exactly as `_seat_row_in` did, and no `deprecated alias used` line is
    printed."""
    _geo(tmp_path, [{"name": "solo", "role": "helper"}])
    rows = rotate._load_seats(tmp_path)
    assert send._seat_row_for(tmp_path, rows, "solo")["name"] == "solo"
    assert send._seat_row_for(tmp_path, rows, "solo-session") is None
    err = capsys.readouterr().err
    assert "deprecated alias used" not in err
