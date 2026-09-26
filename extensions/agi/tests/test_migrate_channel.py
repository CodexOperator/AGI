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
    path, text = _place(fake, _request(), signer="p", root=tmp_path)
    monkeypatch.setattr(rotate, "_migrate_row", lambda root, post: {
        "name": "p", "role": "director", "pubkey": pub.hex()})
    monkeypatch.setattr(rotate, "_migrate_seating_actor",
                        lambda root: "sanctuary-master")
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
    assert len(cell_calls) == 2          # session (post) + seating (master)
    assert cell_calls[0]["actor"] == "p"
    assert cell_calls[0]["cells"]["pid"] == 4242
    assert "box" not in cell_calls[0]["cells"]   # seating is the master's
    assert cell_calls[1]["actor"] == "sanctuary-master"
    assert cell_calls[1]["cells"] == {"box": "boxB"}
    assert len(_acks(fake)) == 1
    assert "seated p on boxB" in out
    assert path.read_text(encoding="utf-8") == text


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
    wt = tmp_path / ".agi" / "worktrees" / "post-p"
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
    monkeypatch.setattr(rotate, "_migrate_seating_actor",
                        lambda root: "sanctuary-master")
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
    monkeypatch.setattr(rotate, "_migrate_seating_actor",
                        lambda root: "sanctuary-master")
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


def test_migrate_transcript_dest_is_the_path_resume_reads(tmp_path, monkeypatch):
    """SHOULD FIX (a)+(b): dest is the projects path (never a copy in the
    worktree) and the slug canonicalizes BOTH '/' and '.'.

    The oracle is INDEPENDENT of the module global the code derives from:
    CC_PROJECTS_DIR is redirected to a separately built tmp path, so a mutant
    that derives dest from the wrong root is caught."""
    fixture = tmp_path / ".claude" / "projects"
    monkeypatch.setattr(rotate, "CC_PROJECTS_DIR", fixture)
    dest = rotate._migrate_transcript_dest(
        Path("/home/x/.agi/worktrees/p"), "sess-1")
    assert dest.name == "sess-1.jsonl"
    assert dest.parent.name == "-home-x--agi-worktrees-p"
    assert ".migrate-transcript.jsonl" not in str(dest)
    assert dest == fixture / "-home-x--agi-worktrees-p" / "sess-1.jsonl"


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
    assert (repo / ".agi" / "worktrees" / "post-p" / "f").is_file()
    assert (repo / ".git" / "worktrees" / "post-p").is_dir()  # a real link
    assert spawns and spawns[-1][1].endswith("rotate.py")
    assert cells["box"] == "boxB"
    assert cells["worktree"] == ".agi/worktrees/post-p"


def _real_repo(tmp_path):
    """A real git repo with a pushed refs/agi/posts/p -- the target box's
    bytes for a genuine `git worktree add`."""
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
    # SM.123 slice 5: the seating actor is resolved from a REAL [config].md
    # grant, so `_migrate_seating_actor` (not a mock) answers.
    import json
    root = Path(__file__).resolve().parents[3]
    (repo / ".agi" / "context" / "schemas").mkdir(parents=True)
    (repo / ".agi" / "nodes" / ".geometry").mkdir(parents=True)
    (repo / ".agi" / "context" / "schemas" / "[config].md").write_text(
        (root / ".agi" / "context" / "schemas" / "[config].md")
        .read_text(encoding="utf-8"), encoding="utf-8")
    rows = [{"name": "p", "role": "director", "town": "core"},
            {"name": "sanctuary-master", "role": "director",
             "town": "sanctuary"}]
    body = "\n".join(f"  - {json.dumps(r)}" for r in rows)
    (repo / ".agi" / "nodes" / ".geometry" / "posts.md").write_text(
        "---\nid: config:posts\nmint_id: 3e88873e3c204c5088f6ab81322a26de\n"
        "type: config\nparents:\n  - goal:g17\nposts:\n" + body +
        "\n---\n\n# config:posts\n\nfixture\n", encoding="utf-8")
    return repo


def test_receive_marks_the_moved_post_as_a_worktree_never_main(
        tmp_path, monkeypatch, capsys):
    """SLICE 4 R1: the seating writes the REAL post-worktree convention; a
    post left with no worktree cell is classified MAIN and the next rotation
    silently runs in MAIN."""
    repo = _real_repo(tmp_path)
    monkeypatch.setenv("AGI_BOX", "boxB")
    live, fake = _fake_comms(tmp_path, monkeypatch)
    _p, pub = live._mint_seat_key(tmp_path, "p", "ed25519")
    _place(fake, _request(), signer="p", root=tmp_path)
    monkeypatch.setattr(rotate, "_migrate_row", lambda root, post: {
        "name": "p", "role": "director", "pubkey": pub.hex()})
    real_run = subprocess.run
    spawns = []

    def fake_run(argv, **kw):
        if argv and argv[0] == "git":
            return real_run(argv, **kw)
        spawns.append(argv)

    monkeypatch.setattr(rotate.subprocess, "run", fake_run)
    calls = []
    monkeypatch.setattr(rotate, "_write_identity_cells",
                        lambda root, **kw: calls.append(kw) or "ok")
    rc = rotate.cmd_migrate_receive(_rns(), repo)
    assert rc == 0
    seating = next(c for c in calls if "worktree" in c["cells"])
    assert seating["actor"] == "sanctuary-master"
    assert seating["cells"]["worktree"] == ".agi/worktrees/post-p"
    row = {"name": "p", "worktree": seating["cells"]["worktree"]}
    assert not (bool(row) and not row["worktree"].strip())   # NOT a MAIN post
    assert rotate._seat_worktree_cwd(repo, row) == str(
        repo / ".agi" / "worktrees" / "post-p")


def test_auto_mode_fork_supplies_the_posts_own_session_id(
        tmp_path, monkeypatch, capsys):
    """SLICE 4 R2: when the meter is the chooser, fork must not be blocked
    by the --session-id refusal -- the post's live id IS the thing to fork."""
    monkeypatch.setenv("AGI_BOX", "boxA")
    live_send = importlib.import_module("send")
    live_send._mint_seat_key(tmp_path, "p", "ed25519")
    fake_comms = tmp_path / "comms"
    monkeypatch.setattr(live_send, "comms_root",
                        lambda root, override=None: fake_comms)
    monkeypatch.setattr(rotate, "_migrate_default_mode",
                        lambda root, post: "fork")
    monkeypatch.setattr(rotate, "_migrate_row",
                        lambda root, post: {"name": "p",
                                            "session_id": "sess-9"})
    rc = rotate.main(["migrate", "--post", "p", "--to", "boxB",
                      "--root", str(tmp_path)])
    assert rc == 0, capsys.readouterr().out
    files = sorted((fake_comms / migrate_channel.SUBDIR).glob("*.md"))
    parsed = migrate_channel.parse_record(files[0].read_text())
    assert parsed["mode"] == "fork"
    assert parsed["session_id"] == "sess-9"


def test_auto_mode_fork_with_no_session_id_anywhere_is_refused(
        tmp_path, monkeypatch, capsys):
    monkeypatch.setenv("AGI_BOX", "boxA")
    monkeypatch.setattr(rotate, "_migrate_default_mode",
                        lambda root, post: "fork")
    monkeypatch.setattr(rotate, "_migrate_row", lambda root, post: {})
    rc = rotate.main(["migrate", "--post", "p", "--to", "boxB",
                      "--root", str(tmp_path)])
    out = capsys.readouterr().out
    assert rc == 1
    assert "REFUSED" in out and "session-id" in out


def test_a_stage_absent_record_is_read_as_a_request_and_verifies(
        tmp_path, monkeypatch):
    """SLICE 4 R3: the slice-1 writer had no `stage`; its record must not be
    silently dropped by an upgraded receiver, and its legacy signature (over
    the stageless key order) must still verify."""
    import yaml
    live_send = importlib.import_module("send")
    _p, pub = live_send._mint_seat_key(tmp_path, "p", "ed25519")
    rec = _rec()
    legacy = {k: rec.get(k, "") for k in migrate_channel._KEYS_LEGACY}
    line = live_send._sign_line(
        tmp_path, "p", rec["ts"], rec["target_box"],
        migrate_channel._canonical(rec, migrate_channel._KEYS_LEGACY))
    if line:
        legacy["sig"] = line.split(": ", 1)[1]
    text = ("---\n" + yaml.safe_dump(legacy, sort_keys=False)
            + "---\n\nbody\n")
    parsed = migrate_channel.parse_record(text)
    assert parsed is not None and parsed["stage"] == "request"
    assert migrate_channel.verify_record(text, pub.hex()) is True


def _config_root(tmp_path):
    """A REAL graph root ([config].md live bytes, ladder, posts rows) so the
    receive tick drives the REAL `_write_identity_cells` -> write.submit path,
    never a mock (SM.123 slice 5 binding rule)."""
    import json
    root = Path(__file__).resolve().parents[3]
    agi = tmp_path / ".agi"
    (agi / "context" / "schemas").mkdir(parents=True)
    (agi / "nodes" / ".geometry").mkdir(parents=True)
    (agi / "config.json").write_text("{}", encoding="utf-8")
    (agi / "context" / "schemas" / "[config].md").write_text(
        (root / ".agi" / "context" / "schemas" / "[config].md")
        .read_text(encoding="utf-8"), encoding="utf-8")
    (agi / "nodes" / ".geometry" / "ladder.md").write_text(
        "---\nid: ladder:ladder\ncurrent_season: 2\n"
        "towns: [core, sanctuary]\n---\n\n# ladder\n", encoding="utf-8")
    rows = [{"name": "p", "role": "director", "town": "core"},
            {"name": "sanctuary-master", "role": "director",
             "town": "sanctuary"}]
    body = "\n".join(f"  - {json.dumps(r)}" for r in rows)
    (agi / "nodes" / ".geometry" / "posts.md").write_text(
        "---\nid: config:posts\nmint_id: 3e88873e3c204c5088f6ab81322a26de\n"
        "type: config\nparents:\n  - goal:g17\nposts:\n" + body +
        "\n---\n\n# config:posts\n\nfixture\n", encoding="utf-8")
    return agi


def test_receive_writes_seating_cells_under_the_master_and_refuses_the_post(
        tmp_path, monkeypatch, capsys):
    """SM.123 slice 5 BINDING: the REAL writer lands box/worktree on the
    moved post's row through the schema-declared actor_rows grant, while the
    SAME seating write as the post itself is REFUSED by name."""
    import write as write_mod  # noqa: PLC0415
    agi = _config_root(tmp_path)
    monkeypatch.setenv("AGI_BOX", "boxB")
    live, fake = _fake_comms(tmp_path, monkeypatch)
    _p, pub = live._mint_seat_key(agi, "p", "ed25519")
    _place(fake, _request(), signer="p", root=agi)
    monkeypatch.setattr(rotate, "_migrate_row", lambda root, post: {
        "name": "p", "role": "director", "pubkey": pub.hex()})
    monkeypatch.setattr(rotate, "_migrate_seat",
                        lambda root, *, post, rec, row, box: {
                            "box": box, "worktree": ".agi/worktrees/post-p",
                            "window": "w1", "pid": 4242, "session_id": "s1",
                            "session_name": "n1"})
    rc = rotate.cmd_migrate_receive(_rns(), agi)
    out = capsys.readouterr().out
    assert rc == 0, out
    text = (agi / "nodes" / ".geometry" / "posts.md").read_text(
        encoding="utf-8")
    assert '"box": "boxB"' in text and "worktrees/post-p" in text
    assert "seated p on boxB" in out
    with pytest.raises(write_mod.EditError) as ei:
        rotate._write_identity_cells(
            agi, seat="p", actor="p", role="director",
            cells={"box": "boxC", "worktree": ".agi/worktrees/post-p"})
    assert "may update only its OWN row" in str(ei.value)


def test_a_blank_stage_record_reads_as_request_and_verifies(tmp_path):
    """SM.123 slice 5: a present-but-BLANK `stage: ""` is the legacy shape;
    parse reads it as request and verify must use the legacy key order."""
    import yaml
    live_send = importlib.import_module("send")
    _p, pub = live_send._mint_seat_key(tmp_path, "p", "ed25519")
    rec = _rec()
    legacy = {k: rec.get(k, "") for k in migrate_channel._KEYS_LEGACY}
    legacy["stage"] = ""
    line = live_send._sign_line(
        tmp_path, "p", rec["ts"], rec["target_box"],
        migrate_channel._canonical(rec, migrate_channel._KEYS_LEGACY))
    if line:
        legacy["sig"] = line.split(": ", 1)[1]
    text = ("---\n" + yaml.safe_dump(legacy, sort_keys=False)
            + "---\n\nbody\n")
    parsed = migrate_channel.parse_record(text)
    assert parsed is not None and parsed["stage"] == "request"
    assert migrate_channel.verify_record(text, pub.hex()) is True


def test_seating_uses_the_rows_own_worktree_cell_when_set(tmp_path, monkeypatch):
    """SM.123 slice 5: the row's OWN `worktree` cell chooses the directory;
    the `post-<seat>` convention is the EMPTY-cell fallback only."""
    repo = _real_repo(tmp_path)
    (repo / ".agi" / "worktrees" / "custom-p").mkdir(parents=True)
    monkeypatch.setattr(rotate, "_migrate_row", lambda root, post: {})
    monkeypatch.setattr(rotate, "_migrate_copy_transcript",
                        lambda root, rec, worktree: worktree)
    real_run = subprocess.run
    monkeypatch.setattr(rotate.subprocess, "run",
                        lambda argv, **kw: (real_run(argv, **kw)
                                            if argv and argv[0] == "git"
                                            else None))
    cells = rotate._migrate_seat(
        repo, post="p", rec=_request(),
        row={"role": "director", "worktree": ".agi/worktrees/custom-p"},
        box="boxB")
    assert cells["worktree"] == ".agi/worktrees/custom-p"
    assert (repo / ".agi" / "worktrees" / "custom-p").is_dir()


def test_receive_skips_a_record_it_cannot_seat_without_killing_the_tick(
        tmp_path, monkeypatch, capsys):
    """SLICE 4 R4: a `git worktree add` that left the worktree absent raises
    in the spawn's cwd=; skip that record by name, seat the next one."""
    monkeypatch.setenv("AGI_BOX", "boxB")
    live, fake = _fake_comms(tmp_path, monkeypatch)
    _p, pub = live._mint_seat_key(tmp_path, "p", "ed25519")
    _q, pubq = live._mint_seat_key(tmp_path, "q", "ed25519")
    _place(fake, _request(post="p", ts="2026-09-18T12:00:00+00:00"),
           signer="p", root=tmp_path)
    _place(fake, _request(post="q", ts="2026-09-18T12:01:00+00:00"),
           signer="q", root=tmp_path)
    rows = {"p": {"name": "p", "pubkey": pub.hex()},
            "q": {"name": "q", "pubkey": pubq.hex()}}
    monkeypatch.setattr(rotate, "_migrate_row", lambda root, post: rows.get(post, {}))
    monkeypatch.setattr(rotate, "_migrate_seating_actor",
                        lambda root: "sanctuary-master")
    seated = []

    def fake_seat(root, *, post, rec, row, box):
        if post == "p":
            raise FileNotFoundError("[Errno 2] no such file: worktrees")
        seated.append(post)
        return {"box": box, "worktree": f".agi/worktrees/post-{post}",
                "window": "w", "pid": 1, "session_id": "s",
                "session_name": "n"}

    monkeypatch.setattr(rotate, "_migrate_seat", fake_seat)
    monkeypatch.setattr(rotate, "_write_identity_cells", lambda root, **kw: "ok")
    rc = rotate.cmd_migrate_receive(_rns(), tmp_path)
    out = capsys.readouterr().out
    assert rc == 0
    assert "could not seat" in out and "tick lives" in out
    assert seated == ["q"]


# --- FR-B2 (goal:g15.27.2): the grant is resolved BEFORE the seat -----------


def test_receive_without_a_grant_never_seats_and_a_later_record_still_seats(
        tmp_path, monkeypatch, capsys):
    """Conjunct A: an ungranted record gets no worktree, no spawn and no row
    cell (not even the session cells); it is skipped BY NAME, the request
    stays byte-identical and a later good record is seated in the same tick."""
    monkeypatch.setenv("AGI_BOX", "boxB")
    live, fake = _fake_comms(tmp_path, monkeypatch)
    _p, pub = live._mint_seat_key(tmp_path, "p", "ed25519")
    _q, pubq = live._mint_seat_key(tmp_path, "q", "ed25519")
    p_path, p_text = _place(
        fake, _request(post="p", ts="2026-09-18T12:00:00+00:00"),
        signer="p", root=tmp_path)
    _place(fake, _request(post="q", ts="2026-09-18T12:01:00+00:00"),
           signer="q", root=tmp_path)
    rows = {"p": {"name": "p", "pubkey": pub.hex()},
            "q": {"name": "q", "role": "director", "pubkey": pubq.hex()}}
    monkeypatch.setattr(rotate, "_migrate_row",
                        lambda root, post: rows.get(post, {}))
    # the grant is resolved once per record: empty on p's pass, present on q's.
    grants = iter(["", "sanctuary-master"])
    monkeypatch.setattr(rotate, "_migrate_seating_actor",
                        lambda root: next(grants))
    seated = []
    monkeypatch.setattr(rotate, "_migrate_seat",
                        lambda root, *, post, rec, row, box: (
                            seated.append(post) or {
                                "box": box,
                                "worktree": f".agi/worktrees/post-{post}",
                                "window": "w", "pid": 1, "session_id": "s",
                                "session_name": "n"}))
    writes = []
    monkeypatch.setattr(rotate, "_write_identity_cells",
                        lambda root, **kw: writes.append(kw) or "ok")
    rc = rotate.cmd_migrate_receive(_rns(), tmp_path)
    out = capsys.readouterr().out
    assert rc == 0
    assert seated == ["q"]                        # p was NEVER seated
    assert all(w["seat"] != "p" for w in writes)  # and no cell written for p
    assert "no actor_rows grant covers box/worktree for p" in out
    assert p_path.read_text(encoding="utf-8") == p_text   # byte-identical
    assert [a["post"] for a in _acks(fake)] == ["q"]      # the tick lived


def test_receive_identity_write_edit_error_skips_the_record_and_tick_lives(
        tmp_path, monkeypatch, capsys):
    """Conjunct B: a write.EditError from the ONE identity writer is caught
    explicitly (never a bare except); the record is skipped BY NAME and a
    later good record still seats."""
    import write as write_mod
    monkeypatch.setenv("AGI_BOX", "boxB")
    live, fake = _fake_comms(tmp_path, monkeypatch)
    _p, pub = live._mint_seat_key(tmp_path, "p", "ed25519")
    _q, pubq = live._mint_seat_key(tmp_path, "q", "ed25519")
    _place(fake, _request(post="p", ts="2026-09-18T12:00:00+00:00"),
           signer="p", root=tmp_path)
    _place(fake, _request(post="q", ts="2026-09-18T12:01:00+00:00"),
           signer="q", root=tmp_path)
    rows = {"p": {"name": "p", "pubkey": pub.hex()},
            "q": {"name": "q", "role": "director", "pubkey": pubq.hex()}}
    monkeypatch.setattr(rotate, "_migrate_row",
                        lambda root, post: rows.get(post, {}))
    monkeypatch.setattr(rotate, "_migrate_seating_actor",
                        lambda root: "sanctuary-master")
    monkeypatch.setattr(rotate, "_migrate_seat",
                        lambda root, *, post, rec, row, box: {
                            "box": box,
                            "worktree": f".agi/worktrees/post-{post}",
                            "window": "w", "pid": 1, "session_id": "s",
                            "session_name": "n"})

    def fake_write(root, *, seat, actor, role, cells):
        if seat == "p":
            raise write_mod.EditError(
                "refused by name: seat 'p' may update only its OWN row")
        return "ok"

    monkeypatch.setattr(rotate, "_write_identity_cells", fake_write)
    rc = rotate.cmd_migrate_receive(_rns(), tmp_path)
    out = capsys.readouterr().out
    assert rc == 0
    assert "identity write refused" in out and "tick lives" in out
    assert [a["post"] for a in _acks(fake)] == ["q"]


def test_migrate_refs_come_from_branches_mirror_ref(tmp_path, monkeypatch,
                                                    capsys):
    """Conjunct C: the migrate path's post ref is branches.mirror_ref's ONE
    spelling -- for cmd_migrate's record and _migrate_seat's fallback."""
    sentinel = "refs/agi/SENTINEL/p"
    calls = []
    monkeypatch.setattr(rotate.branches, "mirror_ref",
                        lambda season, kind, name: (
                            calls.append((kind, name)) or sentinel))
    assert rotate._migrate_post_ref(tmp_path, "p") == sentinel
    # _migrate_seat with no rec branch falls back to that same spelling.
    with monkeypatch.context() as m:
        runs = []
        m.setattr(rotate.subprocess, "run",
                  lambda argv, **kw: runs.append(argv))
        m.setattr(rotate, "_migrate_row", lambda root, post: {})
        rotate._migrate_seat(tmp_path, post="p", rec={"mode": "rotate"},
                             row={"role": "director"}, box="boxB")
        assert any(sentinel in argv for argv in runs)
    # cmd_migrate writes that same ref into its ONE record.
    monkeypatch.setenv("AGI_BOX", "boxA")
    live, fake = _fake_comms(tmp_path, monkeypatch)
    live._mint_seat_key(tmp_path, "p", "ed25519")
    rc = rotate.cmd_migrate(_ns(post="p", to="boxB"), tmp_path)
    assert rc == 0
    rec = migrate_channel.parse_record(
        sorted((fake / migrate_channel.SUBDIR).glob("*.md"))[0].read_text())
    assert rec["branch"] == sentinel
    assert ("posts", "p") in calls


def test_migrate_path_has_no_second_ref_literal():
    """Conjunct C falsifier: no `refs/agi/posts/` literal survives in the
    migrate functions -- the one spelling is branches.mirror_ref."""
    src = (Path(__file__).resolve().parents[1]
           / "bin" / "rotate.py").read_text(encoding="utf-8")
    start = src.index("def cmd_migrate(")
    end = src.index("def cmd_rotate(")
    assert "refs/agi/posts/" not in src[start:end]


def test_transcript_scp_argv_is_tilde_relative_never_literal_dollar_home(
        tmp_path, monkeypatch):
    """FR-B3: `_migrate_copy_transcript` builds a literal argv -- no shell --
    and scp's default since OpenSSH 9.0 is the SFTP protocol, which runs no
    remote shell either. So `$HOME` arrives at sftp-server as four literal
    characters, while a leading `~` is server-expanded via
    expand-path@openssh.com. Measured on OpenSSH_9.6p1 with an sshd-free
    `scp -D /usr/lib/openssh/sftp-server` fixture: `boxA:~/.claude/.../x.jsonl`
    copies, `boxA:$HOME/.claude/.../x.jsonl` is ENOENT. This pins the argv.

    Hygiene: `_migrate_transcript_dest` derives its dest under the module
    global `rotate.CC_PROJECTS_DIR` at CALL time, and `_migrate_copy_transcript`
    mkdirs `dest.parent`. Left unredirected that mkdir creates a REAL directory
    under the live `~/.claude/projects` on every run (seven empty leftovers
    were removed by hand once). So the global is pointed at `tmp_path` and the
    test asserts on THAT fixture — no live path is ever read."""
    fixture_projects = tmp_path / ".claude" / "projects"
    monkeypatch.setattr(rotate, "CC_PROJECTS_DIR", fixture_projects)
    seen = []
    monkeypatch.setattr(rotate.subprocess, "run",
                        lambda argv, **kw: seen.append(argv))
    dest = rotate._migrate_copy_transcript(
        tmp_path, {"source_box": "boxA", "session_id": "sess-1"},
        tmp_path / "fork-wt")
    assert len(seen) == 1
    argv = seen[0]
    assert argv[0] == "scp" and argv[1] == "-q"
    assert argv[2] == f"boxA:~/.claude/projects/{dest.parent.name}/{dest.name}"
    assert argv[2].endswith("/sess-1.jsonl")
    assert argv[3] == str(dest)
    assert "$HOME" not in " ".join(argv)
    # dest must have landed under the redirected root, never the real home,
    # and the fixture dir must actually have been created.
    assert str(dest).startswith(str(fixture_projects))
    assert (fixture_projects / dest.parent.name).is_dir()
    assert dest.parent.is_dir()


def test_a_real_grant_without_both_seating_cells_cuts_no_worktree_and_spawns(
        tmp_path, monkeypatch, capsys):
    """The gate is the REAL resolver, not a mock. `test_receive_without_a_
    grant_never_seats...` stubs `_migrate_seating_actor`, so it proves the
    ORDER but not that the real grant reader refuses. Here the live
    `[config].md` is copied into a real repo and its `actor_rows` entry keeps
    `box` but loses `worktree` -- an INADMISSIBLE grant -- and neither
    `_migrate_seating_actor` nor `_migrate_seat` is patched: the worktree add
    and the spawn are the genuine subprocesses, intercepted only to be
    recorded. Nothing may run, and the tick must still live."""
    repo = _real_repo(tmp_path)
    schema = repo / ".agi" / "context" / "schemas" / "[config].md"
    text = schema.read_text(encoding="utf-8")
    assert ", worktree]" in text, "the live grant must carry worktree to drop"
    schema.write_text(text.replace(", worktree]", "]"), encoding="utf-8")
    monkeypatch.setenv("AGI_BOX", "boxB")
    live, fake = _fake_comms(tmp_path, monkeypatch)
    _p, pub = live._mint_seat_key(tmp_path, "p", "ed25519")
    path, rec_text = _place(fake, _request(), signer="p", root=tmp_path)
    monkeypatch.setattr(rotate, "_migrate_row", lambda root, post: {
        "name": "p", "role": "director", "pubkey": pub.hex()})
    real_run = subprocess.run
    ran = []

    def fake_run(argv, **kw):
        ran.append(list(argv))
        return real_run(argv, **kw)

    monkeypatch.setattr(rotate.subprocess, "run", fake_run)
    writes = []
    monkeypatch.setattr(rotate, "_write_identity_cells",
                        lambda root, **kw: writes.append(kw) or "ok")
    # the REAL resolver answers -- and refuses, on the real schema bytes
    assert rotate._migrate_seating_actor(repo) == ""
    rc = rotate.cmd_migrate_receive(_rns(), repo)
    out = capsys.readouterr().out
    assert rc == 0
    assert not [a for a in ran if "worktree" in a]        # no worktree add
    assert not [a for a in ran if a and a[0] == "scp"]    # no fork copy
    assert not (repo / ".agi" / "worktrees" / "post-p").exists()
    assert writes == []                                     # no cell at all
    assert "no actor_rows grant covers box/worktree for p" in out
    assert path.read_text(encoding="utf-8") == rec_text    # byte-identical
    assert _acks(fake) == []                                # nothing seated
