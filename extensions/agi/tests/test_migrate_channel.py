# test_migrate_channel.py -- SM.123 QUICK-MIGRATE, source-side slice.
#
# The ONE cross-box `migrate` record kind plus `rotate.py migrate`'s plan:
# one record dict, one signed file under the season comms root, refusals by
# name, and a --dry-run that touches nothing. The carryover commit, the ref
# push, the target receive and the seated line are named steps, not this
# round's bytes.
import argparse
import importlib
import os
import subprocess
import sys
from pathlib import Path

import pytest

sys.path.insert(0, str(Path(__file__).resolve().parents[2]))
from agi.bin import migrate_channel, rotate  # noqa: E402
import send  # noqa: E402 -- the module rotate's lazy `import send` resolves


def _rec(**kw):
    base = dict(post="p", mode="rotate", source_box="boxA", target_box="boxB",
                branch="refs/agi/posts/p", tip="abc123",
                session_id=None, ts="2026-09-18T12:00:00+00:00")
    base.update(kw)
    return migrate_channel.record(**base)


def _ns(**kw):
    base = dict(post=None, to=None, mode="rotate", session_id=None, tip=None,
                dry_run=False, root=None)
    base.update(kw)
    return argparse.Namespace(**base)


def test_record_refuses_unknown_mode_by_name():
    with pytest.raises(ValueError, match="unknown migrate mode"):
        _rec(mode="teleport")


def test_record_name_is_aliases_only():
    name = migrate_channel.record_name(_rec())
    assert name.endswith("-p--boxB.md")
    assert "/" not in name and ":" not in name


def test_format_parse_roundtrips_all_fields_and_rejects_other_kinds():
    rec = _rec(session_id="sess-1")
    parsed = migrate_channel.parse_record(migrate_channel.format_record(rec))
    assert parsed == rec
    assert migrate_channel.parse_record("---\nkind: dm\nmode: rotate\n---\n") is None
    assert migrate_channel.parse_record("no frontmatter") is None


def test_signed_record_verifies_and_a_tampered_byte_does_not(tmp_path):
    minted = send._mint_seat_key(tmp_path, "p", "ed25519")
    assert minted is not None
    _path, pub = minted
    text = migrate_channel.format_record(_rec(), sign_root=tmp_path, signer="p")
    assert "sig: ed25519:" in text
    assert migrate_channel.verify_record(text, pub.hex()) is True
    assert migrate_channel.verify_record(text.replace("rotate", "fork", 1),
                                         pub.hex()) is False
    assert migrate_channel.verify_record(
        migrate_channel.format_record(_rec()), pub.hex()) is False


def test_dry_run_prints_every_step_and_touches_nothing(tmp_path, monkeypatch,
                                                       capsys):
    monkeypatch.setenv("AGI_BOX", "boxA")
    rc = rotate.main(["migrate", "--post", "p", "--to", "boxB", "--dry-run",
                      "--root", str(tmp_path)])
    out = capsys.readouterr().out
    assert rc == 0
    assert "step 1:" in out and "step 6:" in out
    assert "dry-run: nothing touched" in out
    assert not (tmp_path / "comms").exists()


def test_same_box_refused_by_name(tmp_path, monkeypatch, capsys):
    monkeypatch.setenv("AGI_BOX", "boxA")
    rc = rotate.main(["migrate", "--post", "p", "--to", "boxA", "--dry-run",
                      "--root", str(tmp_path)])
    assert rc == 1
    assert "REFUSED" in capsys.readouterr().out


def test_unknown_mode_refused_by_name(tmp_path, monkeypatch, capsys):
    monkeypatch.setenv("AGI_BOX", "boxA")
    rc = rotate.cmd_migrate(_ns(post="p", to="boxB", mode="teleport"), tmp_path)
    assert rc == 1
    assert "unknown mode" in capsys.readouterr().out


def test_apply_writes_one_signed_record(tmp_path, monkeypatch, capsys):
    monkeypatch.setenv("AGI_BOX", "boxA")
    # Patch the module object the code under test imports at CALL time, not
    # the name bound when this file was imported. In a full-suite run another
    # module can leave a DIFFERENT `send` in sys.modules than the one bound
    # here; patching the stale object silently misses and the record lands in
    # the real comms root. (hypothesis:l4-quick-migrate-... receive-side round)
    live_send = importlib.import_module("send")
    assert live_send._mint_seat_key(tmp_path, "p", "ed25519") is not None
    fake_comms = tmp_path / "comms"
    monkeypatch.setattr(live_send, "comms_root",
                        lambda root, override=None: fake_comms)
    rc = rotate.main(["migrate", "--post", "p", "--to", "boxB",
                      "--root", str(tmp_path)])
    out = capsys.readouterr().out
    assert rc == 0
    files = sorted((fake_comms / migrate_channel.SUBDIR).glob("*.md"))
    assert len(files) == 1
    parsed = migrate_channel.parse_record(files[0].read_text())
    assert parsed["mode"] == "rotate"
    assert parsed["source_box"] == "boxA" and parsed["target_box"] == "boxB"
    assert "signed with the p key" in out


# --- SM.123 slice 2: the TARGET side (`migrate --receive`) -------------------
#
# The mail_poll tick's half: a verified `stage: request` record addressed to
# THIS box seats the successor once, writes the identity cells through the ONE
# writer, and answers with ONE `stage: seated` line on the SAME channel. An
# unsigned/tampered record or a row already live is refused BY NAME.
#
# A "post" never touches the real graph here: `_migrate_row`, `_migrate_seat`
# and `_write_identity_cells` are the seams, so no test reads or writes the
# live checkout. The comms root is redirected the same way the apply test does.


def _rns(**kw):
    base = dict(post=None, dry_run=False, receive=True)
    base.update(kw)
    return argparse.Namespace(**base)


def _fake_comms(tmp_path, monkeypatch):
    """Redirect the live `send` module's comms_root (the module receive
    imports at call time) to a tmp path; return (module, fake_root)."""
    live = importlib.import_module("send")
    fake = tmp_path / "comms"
    monkeypatch.setattr(live, "comms_root",
                        lambda root, override=None: fake)
    return live, fake


def _request(**kw):
    base = dict(post="p", mode="rotate", source_box="boxA", target_box="boxB",
                branch="refs/agi/posts/p", tip="abc", session_id=None,
                ts="2026-09-18T12:00:00+00:00")
    base.update(kw)
    return migrate_channel.record(**base)


def _place(fake, rec, *, signer=None, root=None):
    cdir = fake / migrate_channel.SUBDIR
    cdir.mkdir(parents=True, exist_ok=True)
    text = migrate_channel.format_record(rec, sign_root=root, signer=signer)
    path = cdir / migrate_channel.record_name(rec)
    path.write_text(text, encoding="utf-8")
    return path, text


def _acks(fake):
    cdir = fake / migrate_channel.SUBDIR
    out = []
    for p in sorted(cdir.glob("*.md")):
        rec = migrate_channel.parse_record(p.read_text(encoding="utf-8"))
        if rec is not None and rec.get("stage") == "seated":
            out.append(rec)
    return out


def test_receive_seats_once_and_writes_the_cells_through_the_one_writer(
        tmp_path, monkeypatch, capsys):
    monkeypatch.setenv("AGI_BOX", "boxB")
    live, fake = _fake_comms(tmp_path, monkeypatch)
    _p, pub = live._mint_seat_key(tmp_path, "p", "ed25519")
    _place(fake, _request(), signer="p", root=tmp_path)
    monkeypatch.setattr(rotate, "_migrate_row", lambda root, post: {
        "name": "p", "role": "director", "pubkey": pub.hex()})
    seated = []
    monkeypatch.setattr(rotate, "_migrate_seat", lambda root, *, post, rec, row, box: (
        seated.append((post, rec["mode"], box)) or
        {"box": box, "window": "w1", "pid": 4242, "session_id": "s1",
         "session_name": "n1"}))
    cell_calls = []
    monkeypatch.setattr(rotate, "_write_identity_cells", lambda root, **kw: (
        cell_calls.append(kw) or "wrote identity cells for seat 'p'"))
    rc = rotate.cmd_migrate_receive(_rns(), tmp_path)
    out = capsys.readouterr().out
    assert rc == 0
    assert seated == [("p", "rotate", "boxB")]
    assert len(cell_calls) == 1          # the ONE writer, called once
    assert cell_calls[0]["cells"]["pid"] == 4242
    assert cell_calls[0]["cells"]["box"] == "boxB"
    acks = _acks(fake)
    assert len(acks) == 1
    assert acks[0]["stage"] == "seated"
    assert acks[0]["source_box"] == "boxB" and acks[0]["target_box"] == "boxA"
    assert "seated p on boxB" in out


def test_receive_refuses_an_unsigned_record_by_name(tmp_path, monkeypatch,
                                                    capsys):
    monkeypatch.setenv("AGI_BOX", "boxB")
    live, fake = _fake_comms(tmp_path, monkeypatch)
    _p, pub = live._mint_seat_key(tmp_path, "p", "ed25519")
    _place(fake, _request())            # unsigned
    monkeypatch.setattr(rotate, "_migrate_row", lambda root, post: {
        "name": "p", "pubkey": pub.hex()})
    seen = []
    monkeypatch.setattr(rotate, "_migrate_seat",
                        lambda root, **kw: seen.append(1) or {})
    rc = rotate.cmd_migrate_receive(_rns(), tmp_path)
    out = capsys.readouterr().out
    assert rc == 0
    assert seen == []
    assert "does not verify" in out and "nothing touched" in out
    assert _acks(fake) == []


def test_receive_refuses_a_tampered_record_by_name(tmp_path, monkeypatch,
                                                   capsys):
    monkeypatch.setenv("AGI_BOX", "boxB")
    live, fake = _fake_comms(tmp_path, monkeypatch)
    _p, pub = live._mint_seat_key(tmp_path, "p", "ed25519")
    path, text = _place(fake, _request(session_id="sess-1"), signer="p",
                        root=tmp_path)
    path.write_text(text.replace("rotate", "fork", 1), encoding="utf-8")
    monkeypatch.setattr(rotate, "_migrate_row", lambda root, post: {
        "name": "p", "pubkey": pub.hex()})
    seen = []
    monkeypatch.setattr(rotate, "_migrate_seat",
                        lambda root, **kw: seen.append(1) or {})
    rotate.cmd_migrate_receive(_rns(), tmp_path)
    assert seen == []
    assert "does not verify" in capsys.readouterr().out


def test_receive_refuses_two_live_on_one_row_by_name(tmp_path, monkeypatch,
                                                     capsys):
    monkeypatch.setenv("AGI_BOX", "boxB")
    live, fake = _fake_comms(tmp_path, monkeypatch)
    _p, pub = live._mint_seat_key(tmp_path, "p", "ed25519")
    _place(fake, _request(), signer="p", root=tmp_path)
    monkeypatch.setattr(rotate, "_migrate_row", lambda root, post: {
        "name": "p", "pubkey": pub.hex(), "pid": os.getpid(),
        "box": "boxB", "session_id": "already-live"})
    seen = []
    monkeypatch.setattr(rotate, "_migrate_seat",
                        lambda root, **kw: seen.append(1) or {})
    rotate.cmd_migrate_receive(_rns(), tmp_path)
    out = capsys.readouterr().out
    assert seen == []
    assert "already live on boxB" in out and "two live on one row" in out
    assert _acks(fake) == []


def test_receive_ignores_records_addressed_to_another_box(tmp_path,
                                                          monkeypatch, capsys):
    monkeypatch.setenv("AGI_BOX", "boxC")
    _live, fake = _fake_comms(tmp_path, monkeypatch)
    _place(fake, _request())            # target_box=boxB, we are boxC
    seen = []
    monkeypatch.setattr(rotate, "_migrate_seat",
                        lambda root, **kw: seen.append(1) or {})
    rotate.cmd_migrate_receive(_rns(), tmp_path)
    assert seen == []
    assert "no migrate records addressed here" in capsys.readouterr().out


def test_fork_resume_command_is_exact_and_the_transcript_is_copied_before_spawn(
        tmp_path, monkeypatch):
    assert (rotate._fork_resume_command("sess-1")
            == "claude --resume sess-1 --fork-session")
    rec = _request(mode="fork", session_id="sess-1")
    runs = []
    monkeypatch.setattr(rotate.subprocess, "run",
                        lambda argv, **kw: runs.append(argv))
    wt = tmp_path / "worktrees" / "p"
    copied = []
    monkeypatch.setattr(rotate, "_migrate_copy_transcript",
                        lambda root, rec, worktree: (
                            copied.append(worktree / ".migrate-transcript.jsonl")
                            or worktree / ".migrate-transcript.jsonl"))
    monkeypatch.setattr(rotate, "_migrate_row", lambda root, post: {
        "window": "w", "pid": 7, "session_id": "sess-1",
        "session_name": "n"})
    cells = rotate._migrate_seat(tmp_path, post="p", rec=rec,
                                 row={"role": "director"}, box="boxB")
    assert copied == [wt / ".migrate-transcript.jsonl"]
    spawn = runs[-1]
    assert "claude --resume sess-1 --fork-session" in spawn
    assert cells["box"] == "boxB" and cells["session_id"] == "sess-1"


def test_fork_is_chosen_only_below_the_config_threshold(tmp_path, monkeypatch):
    monkeypatch.setattr(rotate, "_load_rotate_defaults",
                        lambda root: {"migrate_fork_below": 0.5})
    monkeypatch.setattr(rotate, "_migrate_row", lambda root, post: {"name": "p"})
    assert rotate._migrate_fork_below(tmp_path) == 0.5
    monkeypatch.setattr(rotate, "_seat_fraction", lambda root, row: 0.2)
    assert rotate._migrate_default_mode(tmp_path, "p") == "fork"
    monkeypatch.setattr(rotate, "_seat_fraction", lambda root, row: 0.8)
    assert rotate._migrate_default_mode(tmp_path, "p") == "rotate"
    monkeypatch.setattr(rotate, "_seat_fraction", lambda root, row: None)
    assert rotate._migrate_default_mode(tmp_path, "p") == "rotate"


def test_live_rotations_node_declares_the_fork_threshold():
    """A test of live config reads the LIVE node, never a copied list."""
    node = (Path(__file__).resolve().parents[3]
            / ".agi" / "nodes" / ".geometry" / "rotations.md")
    assert "migrate_fork_below" in node.read_text(encoding="utf-8")


def test_stage_is_part_of_the_one_record_kind():
    assert migrate_channel.record_name(migrate_channel.seat_record(
        _request(), ts="2026-09-18T13:00:00+00:00")).endswith("p--boxA.md")
    with pytest.raises(ValueError, match="unknown migrate stage"):
        migrate_channel.record(post="p", mode="rotate", source_box="a",
                               target_box="b", branch="r", tip="", 
                               session_id=None, ts="t", stage="seatedz")


# --- SM.123 slice 3: the corrective -----------------------------------------


def test_receive_seats_when_the_live_row_belongs_to_another_box(
        tmp_path, monkeypatch, capsys):
    """MUST FIX: every live row carries the SOURCE box's session_id, so the
    old unscoped check refused the exact post migrate exists to move."""
    monkeypatch.setenv("AGI_BOX", "boxB")
    live, fake = _fake_comms(tmp_path, monkeypatch)
    _p, pub = live._mint_seat_key(tmp_path, "p", "ed25519")
    _place(fake, _request(), signer="p", root=tmp_path)
    monkeypatch.setattr(rotate, "_migrate_row", lambda root, post: {
        "name": "p", "role": "director", "pubkey": pub.hex(),
        "box": "boxA", "pid": os.getpid(), "session_id": "source-live"})
    seated = []
    monkeypatch.setattr(rotate, "_migrate_seat",
                        lambda root, *, post, rec, row, box: (
                            seated.append(post) or {"box": box, "window": "w",
                            "pid": 1, "session_id": "s", "session_name": "n"}))
    monkeypatch.setattr(rotate, "_write_identity_cells", lambda root, **kw: "ok")
    rc = rotate.cmd_migrate_receive(_rns(), tmp_path)
    assert rc == 0
    assert seated == ["p"]          # the source box's live row does not block
    assert "two live on one row" not in capsys.readouterr().out


def test_receive_skips_a_non_numeric_pid_without_killing_the_tick(
        tmp_path, monkeypatch, capsys):
    """NEW (d): one bad pid must skip its record, never abort the loop."""
    monkeypatch.setenv("AGI_BOX", "boxB")
    live, fake = _fake_comms(tmp_path, monkeypatch)
    _p, pub = live._mint_seat_key(tmp_path, "p", "ed25519")
    _q, pubq = live._mint_seat_key(tmp_path, "q", "ed25519")
    _place(fake, _request(post="p", ts="2026-09-18T12:00:00+00:00"),
           signer="p", root=tmp_path)
    _place(fake, _request(post="q", ts="2026-09-18T12:01:00+00:00"),
           signer="q", root=tmp_path)
    rows = {"p": {"name": "p", "pubkey": pub.hex(), "pid": "not-a-pid"},
            "q": {"name": "q", "pubkey": pubq.hex()}}
    monkeypatch.setattr(rotate, "_migrate_row", lambda root, post: rows.get(post, {}))
    seated = []
    monkeypatch.setattr(rotate, "_migrate_seat",
                        lambda root, *, post, rec, row, box: (
                            seated.append(post) or {"box": box, "window": "w",
                            "pid": 1, "session_id": "s", "session_name": "n"}))
    monkeypatch.setattr(rotate, "_write_identity_cells", lambda root, **kw: "ok")
    rc = rotate.cmd_migrate_receive(_rns(), tmp_path)
    out = capsys.readouterr().out
    assert rc == 0
    assert "non-numeric pid" in out
    assert seated == ["q"]          # p skipped, q still seated: the tick lived


def test_fork_mode_without_session_id_is_refused_by_name(tmp_path, monkeypatch,
                                                         capsys):
    """NEW (c): a fork from the meter alone had a blank resume id."""
    monkeypatch.setenv("AGI_BOX", "boxA")
    rc = rotate.main(["migrate", "--post", "p", "--to", "boxB", "--mode",
                      "fork", "--root", str(tmp_path)])
    out = capsys.readouterr().out
    assert rc == 1
    assert "REFUSED" in out and "session-id" in out
    assert not (tmp_path / "comms").exists()


def test_migrate_transcript_dest_is_the_path_resume_reads(tmp_path):
    """SHOULD FIX (a)+(b): dest is the projects path (never a copy in the
    worktree) and the slug canonicalizes BOTH '/' and '.'."""
    dest = rotate._migrate_transcript_dest(
        Path("/home/x/.agi/worktrees/p"), "sess-1")
    assert dest.name == "sess-1.jsonl"
    assert dest.parent.name == "-home-x--agi-worktrees-p"
    assert ".migrate-transcript.jsonl" not in str(dest)
    assert str(dest).startswith(str(Path.home() / ".claude" / "projects"))


def test_seat_makes_a_real_worktree_from_the_pushed_ref(tmp_path, monkeypatch):
    """ALSO CLOSE conjunct 4: one minimal REAL-git test -- a real repo, a
    real ref, a real `git worktree add`; only the spawn is recorded."""
    repo = tmp_path / "repo"
    repo.mkdir()
    for argv in (["git", "init", "-q"],
                 ["git", "config", "user.email", "t@t"],
                 ["git", "config", "user.name", "t"]):
        subprocess.run(argv, cwd=repo, check=True)
    (repo / "f").write_text("x")
    subprocess.run(["git", "add", "f"], cwd=repo, check=True)
    subprocess.run(["git", "commit", "-qm", "i"], cwd=repo, check=True)
    subprocess.run(["git", "update-ref", "refs/agi/posts/p", "HEAD"],
                   cwd=repo, check=True)
    real_run = subprocess.run
    spawns = []

    def fake_run(argv, **kw):
        if argv and argv[0] == "git":
            return real_run(argv, **kw)
        spawns.append(argv)

    monkeypatch.setattr(rotate.subprocess, "run", fake_run)
    monkeypatch.setattr(rotate, "_migrate_row", lambda root, post: {})
    cells = rotate._migrate_seat(repo, post="p", rec=_request(),
                                 row={"role": "director"}, box="boxB")
    assert (repo / "worktrees" / "p" / "f").is_file()
    assert (repo / ".git" / "worktrees" / "p").is_dir()  # a real link
    assert spawns and spawns[-1][1].endswith("rotate.py")
    assert cells["box"] == "boxB"
