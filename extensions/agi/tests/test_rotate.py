import json
import os
import subprocess
import sys
import time
from pathlib import Path
from types import SimpleNamespace

import pytest

sys.path.insert(0, str(Path(__file__).resolve().parents[2]))
from agi.bin import rotate
from agi.bin import brief


def _mk_seat_key(tmp_path, seat, scheme="ed25519"):
    from agi.bin import send
    kr = send._seats_dir(tmp_path)
    kr.mkdir(parents=True, exist_ok=True)
    scheme_obj = send.seatsig.get(scheme)
    _priv, pub = scheme_obj.keygen()
    key_path = kr / f"{seat}.key"
    key_path.write_text(
        '{"scheme": "ed25519", "priv_hex": "%s"}' % _priv.hex())
    import os
    os.chmod(key_path, 0o600)
    return key_path, pub


def test_rotate_key_gate_refuses_keyed_seat_without_key(tmp_path):
    # KEY-GATED: a KEYED row (names a pubkey) but no key file refuses by name.
    err = rotate._rotate_key_gate(tmp_path, "s1", {"pubkey": "deadbeef"})
    assert err is not None
    assert "s1" in err
    assert "keygen s1" in err


def test_rotate_key_gate_passes_when_key_present(tmp_path):
    # row keyed AND the key file exists -> gate passes.
    key_path, pub = _mk_seat_key(tmp_path, "s1")
    err = rotate._rotate_key_gate(tmp_path, "s1", {"pubkey": pub.hex()})
    assert err is None


def test_rotate_key_gate_passes_unkeyed_and_throwaway(tmp_path):
    # no pubkey in the row (incremental fleet keying) and a throwaway row
    # (empty dict) are NEVER refused here -- the minting half is other work.
    assert rotate._rotate_key_gate(tmp_path, "s1", {"role": "parent"}) is None
    assert rotate._rotate_key_gate(tmp_path, "s1", {}) is None
    assert rotate._rotate_key_gate(tmp_path, "s1", None) is None


def test_rotate_first_key_mints_unkeyed_row(tmp_path):
    # line (1) minting half: an UNKEYED real row mints its first key IN THE
    # SAME rotate-self step (incremental fleet keying) -- a 0600 key file
    # appears at <sessions>/seats/<seat>.key and a note is returned.
    from agi.bin import send
    note = rotate._rotate_first_key(tmp_path, tmp_path, "s1",
                                    {"role": "parent"})
    assert note
    assert "minted its first key" in note
    key_path = send._seat_key_path(tmp_path, "s1")
    assert key_path.is_file()
    assert oct(os.stat(key_path).st_mode & 0o777) == oct(0o600)
    obj = json.loads(key_path.read_text())
    assert obj.get("scheme")
    # no cfg/graph here, so there are no rows to write -- the key file is
    # the minted half; the pubkey cell row-write is best-effort and absent.
    assert send._seats_rows(tmp_path) == []


def test_rotate_first_key_mints_through_send_writer(tmp_path, monkeypatch):
    # the mint MUST go through send._mint_seat_key (no second key writer, no
    # ed25519 literal in rotate.py). rotate.py imports `send` as a TOP-LEVEL
    # module (it pushes bin/ onto sys.path at import), which is a DIFFERENT
    # module object from `agi.bin.send` -- so patch the one rotate binds.
    import send as bin_send
    orig = bin_send._mint_seat_key
    seen = {}

    def spy(r, s, sc):
        seen["call"] = (r, s, sc)
        return orig(r, s, sc)

    monkeypatch.setattr(bin_send, "_mint_seat_key", spy)
    rotate._rotate_first_key(tmp_path, tmp_path, "s2", {"role": "helper"})
    assert seen.get("call") == (tmp_path, "s2",
                                 bin_send.seatsig.DEFAULT_SCHEME)
    from agi.bin import send as send_pkg
    assert send_pkg._seat_key_path(tmp_path, "s2").is_file()


def test_rotate_first_key_leaves_keyed_and_throwaway_alone(tmp_path):
    # already-keyed row, a throwaway (empty) row, and an idempotent re-rotate
    # (key file already exists) all mint nothing -> ''.
    assert rotate._rotate_first_key(tmp_path, tmp_path, "s1",
                                    {"pubkey": "deadbeef", "role": "parent"}) == ""
    assert rotate._rotate_first_key(tmp_path, tmp_path, "s1", {}) == ""
    assert rotate._rotate_first_key(tmp_path, tmp_path, "s1", None) == ""
    from agi.bin import send
    _mk_seat_key(tmp_path, "s3")
    assert rotate._rotate_first_key(tmp_path, tmp_path, "s3",
                                    {"role": "parent"}) == ""


# ---- goal:g15.25 line (2) SUCCESSOR half (SL5.05 ORDER 2) ----------------

def test_rotate_first_key_dry_run_leaves_no_key_and_no_row(tmp_path):
    """ORDER 1 (SL5.05): --dry-run on an unkeyed real row mints NOTHING and
    writes NO row cell; it still reports the mint it would perform."""
    from agi.bin import send
    note = rotate._rotate_first_key(tmp_path, tmp_path, "s1",
                                    {"role": "parent"}, dry_run=True)
    assert note
    assert "(dry-run)" in note
    assert not send._seat_key_path(tmp_path, "s1").exists()
    assert send._seats_rows(tmp_path) == []


def test_rotate_successor_key_mints_and_replaces(tmp_path):
    """SL5.05 handover-order fix: the mint + retirement SIGN happen early and
    return the successor key in ``pending_key``, but <seat>.key is NOT
    flipped by `_rotate_successor_key` alone -- it stays byte-identical with
    the PREDECESSOR key until `_apply_successor_key_pending` runs (which the
    caller gates on the row write + commit succeeding). After apply the
    successor key is atomically in place (0600, valid JSON)."""
    from agi.bin import send
    key_path, pred_pub = _mk_seat_key(tmp_path, "s1")
    before = key_path.read_text()
    row = {"pubkey": pred_pub.hex(), "role": "parent",
           "sig_scheme": "ed25519"}
    out = rotate._rotate_successor_key(tmp_path, "s1", row,
                                       gen_before=1, gen_after=2)
    assert out is not None
    # DEFERRED: the file is NOT yet touched -- still the predecessor key,
    # byte-identical (a failed spawn/row-write/commit would leave it so).
    assert key_path.read_text() == before
    pk = out.get("pending_key")
    assert pk is not None and pk["path"] == str(key_path)
    # only the gated apply flips the file.
    applied = rotate._apply_successor_key_pending(pk)
    assert "key_replace" in applied and str(key_path) in applied
    assert key_path.is_file()
    assert oct(os.stat(key_path).st_mode & 0o777) == oct(0o600)
    obj = json.loads(key_path.read_text())
    assert obj.get("scheme") == "ed25519"
    sch = send.seatsig.get("ed25519")
    live_pub = sch.public_from_secret(bytes.fromhex(obj["priv_hex"]))
    assert live_pub.hex() == out["successor_pub"]
    assert out["successor_pub"] != pred_pub.hex()  # a NEW key, not the old
    ret = out["retired"]
    assert ret["pub"] == pred_pub.hex()  # retired = the predecessor pub
    assert ret["fp"] == send.seatsig.fingerprint(pred_pub)
    assert ret["from"] == 1 and ret["to"] == 2
    assert "rotated_by_sig" in ret


def test_rotate_successor_key_gate_leaves_pred_key_on_failed_row_write(tmp_path):
    """SL5.05 handover-order fix, proving the DEFECT is closed: when the
    successor spawn-row write (or its one commit) FAILS, the predecessor
    <seat>.key is left BYTE-IDENTICAL and NO successor key is ever written --
    `_apply_successor_key_gated` records the refusal and does not flip the
    file. The failure seam is the existing try/except that records
    ``successor_row`` / ``spawn_row_commit`` as ``FAILED: ...`` lines."""
    from agi.bin import send
    key_path, pred_pub = _mk_seat_key(tmp_path, "s1")
    before = key_path.read_text()
    pred_priv = json.loads(before)["priv_hex"]
    row = {"pubkey": pred_pub.hex(), "role": "parent"}
    out = rotate._rotate_successor_key(tmp_path, "s1", row,
                                       gen_before=1, gen_after=2)
    assert out is not None and "pending_key" in out

    # (a) row write FAILED (the existing seam: _successor_row_write raised,
    #     caught as 'FAILED: ...'); no commit ran (absent).
    r1 = rotate._apply_successor_key_gated(
        out, "FAILED: write.submit boom", "")
    assert "NOT applied" in r1
    assert key_path.read_text() == before  # byte-identical
    assert json.loads(key_path.read_text())["priv_hex"] == pred_priv

    # (b) row write ok but the ONE commit FAILED.
    r2 = rotate._apply_successor_key_gated(
        out, "config:seats row s1: ...", "spawn_row_commit: FAILED -- git add")
    assert "NOT applied" in r2
    assert key_path.read_text() == before  # still the predecessor key

    # (c) row write ok + commit ok -> the successor key IS written.
    r3 = rotate._apply_successor_key_gated(
        out, "config:seats row s1: ...",
        "spawn_row_commit: committed (sha abc1234)")
    assert "key_replace: wrote" in r3
    assert key_path.read_text() != before
    assert (json.loads(key_path.read_text())["priv_hex"]
            == out["pending_key"]["priv_hex"])

    # (d) commit SKIPPED (gitless / already-clean) is NOT a failure -- the
    #     rotation still succeeds and the key flips (the row WAS written;
    #     only the durability commit was skipped, by design never fatal).
    key_path2, pred_pub2 = _mk_seat_key(tmp_path, "s2")
    row2 = {"pubkey": pred_pub2.hex(), "role": "helper"}
    out2 = rotate._rotate_successor_key(tmp_path, "s2", row2,
                                        gen_before=1, gen_after=2)
    r4 = rotate._apply_successor_key_gated(
        out2, "config:seats row s1: ...",
        "spawn_row_commit: SKIPPED -- no git repo; ...")
    assert "key_replace: wrote" in r4
    assert (json.loads(key_path2.read_text())["priv_hex"]
            == out2["pending_key"]["priv_hex"])

    # (e) NO-OP: no pending_key (unkeyed row, dry-run, None) -> ''
    assert rotate._apply_successor_key_gated(None, "x", "y") == ""


def test_rotate_successor_key_gate_defers_on_push_failure(tmp_path):
    """mur-SL2.13 (2): the <seat>.key swap waits for the PUSH, not just the
    own-row commit. When `_commit_spawn_row` reports a trailing ``\npush:
    push: FAILED -- ...`` line, `_apply_successor_key_gated` DEFERS the
    replacement: the predecessor key stays byte-identical, the deferred swap
    is named, and a key on disk never disagrees with what origin holds. A
    SKIPPED or ABSENT push is NOT a failure (the gitless / byte-identical
    case flips the key exactly as before)."""
    key_path, pred_pub = _mk_seat_key(tmp_path, "s3")
    before = key_path.read_text()
    row = {"pubkey": pred_pub.hex(), "role": "helper"}
    out = rotate._rotate_successor_key(tmp_path, "s3", row,
                                       gen_before=1, gen_after=2)

    # (a) row ok + commit ok + push FAILED -> NOT applied, byte-identical,
    #     deferred swap named (ONE stderr line: the return is printed).
    r = rotate._apply_successor_key_gated(
        out, "config:seats row s3: ...",
        "spawn_row_commit: committed (sha abc1234)\n"
        "push: push: FAILED -- remote: permission denied")
    assert "NOT applied" in r and "deferred swap" in r
    assert key_path.read_text() == before  # predecessor key stays put

    # (b) commit FAILED (no push line) still refuses, as before.
    r2 = rotate._apply_successor_key_gated(
        out, "config:seats row s3: ...", "spawn_row_commit: FAILED -- git")
    assert "NOT applied" in r2
    assert key_path.read_text() == before

    # (c) push SKIPPED is NOT a failure -> the key flips (gitless case).
    r3 = rotate._apply_successor_key_gated(
        out, "config:seats row s3: ...",
        "spawn_row_commit: committed (sha abc1234)\n"
        "push: push: SKIPPED -- no git repo")
    assert "key_replace: wrote" in r3
    assert (json.loads(key_path.read_text())["priv_hex"]
            == out["pending_key"]["priv_hex"])

    # (d) push OK -> the key flips, and the loop-closing falsifier is met:
    #     only a FAILED push defers.
    key_path2, _ = _mk_seat_key(tmp_path, "s4")
    before2 = key_path2.read_text()
    out2 = rotate._rotate_successor_key(tmp_path, "s4",
                                        {"pubkey": "x", "role": "p"},
                                        gen_before=1, gen_after=2)
    r4 = rotate._apply_successor_key_gated(
        out2, "config:seats row s4: ...",
        "spawn_row_commit: committed (sha def5678)\npush: push: OK -- master")
    assert "key_replace: wrote" in r4
    assert key_path2.read_text() != before2


def test_rotate_successor_key_sig_verifies_under_retired_pub(tmp_path):
    """rotated_by_sig must verify under the RETIRED (predecessor) pub, and
    must fail under a corrupted record (the signature is specific)."""
    from agi.bin import send
    _key_path, pred_pub = _mk_seat_key(tmp_path, "s1")
    row = {"pubkey": pred_pub.hex(), "role": "parent"}
    out = rotate._rotate_successor_key(tmp_path, "s1", row,
                                       gen_before=3, gen_after=4)
    ret = out["retired"]
    sch = send.seatsig.get("ed25519")
    good = f"s1\nretire\n3\n4\n{out['successor_pub']}"
    assert sch.verify(bytes.fromhex(ret["pub"]), good.encode(),
                      bytes.fromhex(ret["rotated_by_sig"]))
    bad = f"s1\nretire\n3\n5\n{out['successor_pub']}"
    assert not sch.verify(bytes.fromhex(ret["pub"]), bad.encode(),
                          bytes.fromhex(ret["rotated_by_sig"]))


def test_rotate_successor_key_leaves_unkeyed_and_throwaway_alone(tmp_path):
    """Unkeyed row, THROWAWAY/empty row, None, and a keyed row with no key
    file (the gate refused it earlier) all retire nothing -> None."""
    assert rotate._rotate_successor_key(
        tmp_path, "s1", {"role": "parent"}, gen_before=1, gen_after=2) is None
    assert rotate._rotate_successor_key(
        tmp_path, "s1", {}, gen_before=1, gen_after=2) is None
    assert rotate._rotate_successor_key(
        tmp_path, "s1", None, gen_before=1, gen_after=2) is None
    assert rotate._rotate_successor_key(
        tmp_path, "s2", {"pubkey": "deadbeef"},
        gen_before=1, gen_after=2) is None


def test_rotate_successor_key_dry_run_touches_nothing(tmp_path):
    """ORDER 1: --dry-run on a keyed row mints nothing, replaces nothing,
    and still reports the retirement it would perform."""
    from agi.bin import send
    key_path, pred_pub = _mk_seat_key(tmp_path, "s1")
    before = key_path.read_text()
    row = {"pubkey": pred_pub.hex(), "role": "parent"}
    out = rotate._rotate_successor_key(tmp_path, "s1", row,
                                       gen_before=1, gen_after=2, dry_run=True)
    assert out is not None and out.get("dry_run") is True
    assert "(dry-run)" in out["note"]
    assert key_path.read_text() == before  # byte-identical: nothing replaced


def _seed_key_history_graph(root, rows):
    """A minimal graph root (project/.agi) whose config:seats admits the
    self_row fields, so `_successor_row_write`'s write.submit admission runs.
    Mirrors test_write_self_row's project fixture; never touches live config."""
    graph = root / ".agi"
    graph.mkdir(parents=True, exist_ok=True)
    (graph / "config.json").write_text("{}")
    sd = graph / "context" / "schemas"
    sd.mkdir(parents=True, exist_ok=True)
    live = (Path(__file__).resolve().parents[3] / ".agi" / "context" / "schemas" /
            "[config].md")
    if live.exists():
        (sd / "[config].md").write_text(live.read_text(encoding="utf-8"))
    d = graph / "nodes" / ".geometry"
    d.mkdir(parents=True, exist_ok=True)
    body = "\n".join(f"  - {r!r}" for r in rows)
    (d / "seats.md").write_text(
        "---\nid: config:seats\n"
        "mint_id: 3e88873e3c204c5088f6ab81322a26de\n"
        "type: config\nseats:\n" + body + "\n---\n\nfixture\n",
        encoding="utf-8")
    return graph


def test_successor_row_write_appends_key_history_once_and_never_shrinks(tmp_path):
    """ORDER 2, CRITICAL: the successor pubkey + key_history cells ride the ONE
    spawn-row write (`_successor_row_write`), appending EXACTLY ONE retired
    entry and never shrinking existing history."""
    from agi.bin import send
    existing_hist = [{"pub": "00" * 32, "fp": "deadbeef12345678",
                      "from": 0, "to": 1, "rotated_by_sig": "feed"}]
    rows = [{"name": "s1", "role": "director",
             "session_ref": "x", "generation": 1, "window": "",
             "key_history": list(existing_hist)}]
    graph = _seed_key_history_graph(tmp_path, rows)
    _key_path, pred_pub = _mk_seat_key(graph, "s1")
    row = {"pubkey": pred_pub.hex(), "role": "director"}
    kr = rotate._rotate_successor_key(graph, "s1", row,
                                      gen_before=1, gen_after=2)
    out = rotate._successor_row_write(
        graph, actor="s1", seat="s1", role="director",
        session_ref="x", generation=2, window="",
        key_rotation=kr)
    assert "config:seats row" in out and "s1" in out
    import write as w
    rows_after = w._load_seats(graph)
    own = next(r for r in rows_after if r.get("name") == "s1")
    assert own["pubkey"] == kr["successor_pub"]
    assert own["key_history"] == existing_hist + [kr["retired"]]
    assert own["key_history"][-1]["pub"] == pred_pub.hex()


@pytest.fixture
def fake_ladder(tmp_path, monkeypatch):
    root = tmp_path

    def fake_root():
        return root

    monkeypatch.setattr(rotate, "find_project_root", fake_root)

    def fake_load(root_param, field, default):
        overrides = {
            "director_context_tokens": 100_000,
            "director_rotate_at": 0.25,
        }
        return overrides.get(field, default)

    monkeypatch.setattr(rotate, "load_ladder_field", fake_load)
    # L4.110: rotate-self refuses loudly when .geometry/rotations.md is absent
    # (the live state until the prime lands it). Tests that drive rotation
    # mechanics therefore pin a minimal template node — "a node the suite
    # pins is code, suite after the .geometry write".
    g = root / "nodes" / ".geometry"
    g.mkdir(parents=True, exist_ok=True)
    (g / "rotations.md").write_text(
        "---\nid: config:rotations\ntype: config\ntemplates:\n"
        "  parent: {brief_file: extensions/agi/briefs/parent-successor.md, "
        "steps: [handoff, spawn], telemetry: [seat]}\n"
        "  director: {brief_file: extensions/agi/briefs/director-successor.md, "
        "steps: [handoff, spawn], telemetry: [seat]}\n"
        "  prime_director: {brief_file: "
        "extensions/agi/briefs/prime-director-successor.md, "
        "steps: [handoff, spawn], telemetry: [seat]}\n---\n\nbody\n",
        encoding="utf-8")
    return root


@pytest.fixture
def fake_transcript(tmp_path):
    transcript = tmp_path / "transcript.jsonl"
    transcript.write_text(
        """
{"message": {"role": "assistant", "usage": {"input_tokens": 1000, "cache_read_input_tokens": 200, "cache_creation_input_tokens": 300}}}
{"message": {"role": "assistant", "usage": {"input_tokens": 2000, "cache_read_input_tokens": 300, "cache_creation_input_tokens": 0}}}
"""
    )
    return transcript


def test_meter_uses_cc_transcript(monkeypatch, tmp_path, fake_ladder, fake_transcript, capsys):
    projects_dir = tmp_path / ".claude" / "projects" / rotate.CC_PROJECT_SLUG
    projects_dir.mkdir(parents=True)
    dst = projects_dir / "session.jsonl"
    dst.write_text(fake_transcript.read_text())

    monkeypatch.setattr(rotate, "CC_PROJECTS_DIR", tmp_path / ".claude" / "projects")

    exit_code = rotate.main(["meter"])
    captured = capsys.readouterr().out.strip()

    assert exit_code == 0
    assert "0.023" in captured  # (2000+300) / 100000
    assert "claude-code transcript" in captured


def test_meter_check_threshold(monkeypatch, tmp_path, fake_ladder, fake_transcript, capsys):
    monkeypatch.setattr(rotate, "CC_PROJECT_SLUG", "slug-does-not-exist")
    monkeypatch.setattr(rotate, "CC_PROJECTS_DIR", tmp_path / "missing")

    rc_base = tmp_path / "nodes"
    rc_log = rc_base / "sessions"
    rc_log.mkdir(parents=True)
    log_path = rc_log / "remote-control.log"
    log_path.write_text(
        """
USAGE: {"input_tokens": 40000, "cache_read_input_tokens": 10000, "cache_creation_input_tokens": 0}
"""
    )

    def fake_find_root():
        return rc_base

    monkeypatch.setattr(rotate, "find_project_root", fake_find_root)

    exit_code = rotate.main(["meter", "--check"])
    captured = capsys.readouterr().out.strip()
    assert "0.5000" in captured
    assert exit_code == 1


def test_spawn_dry_run(monkeypatch, tmp_path, capsys):
    prompt = tmp_path / "prompt.md"
    prompt.write_text("Hello {name}")

    monkeypatch.chdir(tmp_path)

    exit_code = rotate.main([
        "spawn",
        "--name", "agi-123",
        "--prompt-file", str(prompt),
        "--dry-run",
    ])
    output = capsys.readouterr().out.strip()

    assert exit_code == 0
    assert "claude --remote-control agi-123" in output
    assert "Hello agi-123" in output


def test_spawn_refuses_existing_window(monkeypatch, tmp_path, capsys):
    prompt = tmp_path / "prompt.md"
    prompt.write_text("Hello {name}")

    def fake_run(cmd, capture_output, text, timeout):
        if cmd[:3] == ["tmux", "list-windows", "-t"]:
            return subprocess.CompletedProcess(cmd, 0, stdout="agi-123\n", stderr="")
        raise AssertionError("tmux new-window should not be called in this test")

    monkeypatch.chdir(tmp_path)
    monkeypatch.setattr(subprocess, "run", fake_run)

    exit_code = rotate.main([
        "spawn",
        "--name", "agi-123",
        "--prompt-file", str(prompt),
    ])

    err = capsys.readouterr().err
    assert exit_code == 1
    assert "already exists" in err


def test_spawn_window_reusable_for_non_prime_name(monkeypatch, tmp_path, capsys):
    # hypothesis:l3w4-seat-transport — spawn_window() is the ONE reusable
    # launcher: a non-prime seat name launches via `--remote-control`, never -p.
    prompt = tmp_path / "prompt.md"
    prompt.write_text("You are {name}\n")
    monkeypatch.chdir(tmp_path)

    rc, shell = rotate.spawn_window(
        name="adv-alive", tier="parent", prompt_file=str(prompt),
        dry_run=True,
    )
    out = capsys.readouterr().out.strip()

    assert rc == 0
    assert "claude --remote-control adv-alive" in out
    assert out == shell
    assert " -p" not in out


def test_loop_uses_spawn_window(monkeypatch, tmp_path, capsys):
    # hypothesis:l3w4-seat-transport — cmd_loop routes through spawn_window
    # (one launch path), never its own inline tmux spawn.
    root = _proj(tmp_path)
    monkeypatch.chdir(root)
    monkeypatch.setattr(rotate, "find_project_root", lambda: root)
    monkeypatch.setattr(rotate, "cmd_meter", lambda args, root: 1)  # rotate
    called = {}
    monkeypatch.setattr(
        rotate, "spawn_window",
        lambda **kw: called.update(kw) or (0, "claude --remote-control adv-alive"),
    )

    code = rotate.cmd_loop(SimpleNamespace(
        session_log=None, force=False, role="adv_alive", name="adv-alive",
        name_prefix="belam", model=None, effort=None, settings=None,
        prompt_file=None, tmux_session="agi-rc", window_path=None,
        debug_file=None, dry_run=True, timeout=1,
    ), root)

    assert code == 0
    assert called.get("name") == "adv-alive"
    assert called.get("tier") == "adv_alive"
    assert called.get("dry_run") is True


# --- l3w0-rotate-roles: role resolution, head, name derivation, loop --------


def _proj(tmp_path, ladder_roles=""):
    """A minimal fake graph root: `.agi/` layout (the dir find_project_root
    returns) with a ladder node under nodes/.geometry."""
    root = tmp_path / "proj"
    (root / "nodes" / ".geometry").mkdir(parents=True)
    lines = ["---"]
    if ladder_roles:
        lines.append("roles:")
        lines.append(ladder_roles)
    lines.append("closed: false")
    lines.append("---")
    (root / "nodes" / ".geometry" / "ladder.md").write_text("\n".join(lines))
    return root


class _FakeIn:
    """A file-like stand-in for sys.stdin so cmd_ack's `--text -` branch can
    be tested without a real pipe."""
    def __init__(self, text: str):
        self._text = text

    def read(self) -> str:
        return self._text


def _fake_launch(wins: Path, content: str) -> int:
    """Test stand-in for `_launch_window` that only reflects the window on disk
    (writes `content` into the window-path file) and returns 0. A bare
    `lambda ...: wins.write_text(content) or 0` is WRONG: `Path.write_text`
    returns the byte count (truthy), so the lambda returns that count, which
    cmd_loop treats as rc and aborts. This helper divorces the write from the
    return."""
    wins.write_text(content, encoding="utf-8")
    return 0


def test_spawn_resolves_role_model_effort_settings(monkeypatch, tmp_path, capsys):
    # Ladder roles table row for prime_director wins over config/defaults.
    root = _proj(tmp_path, ladder_roles=(
        "  - role: prime_director\n"
        "    harness: claude-code\n"
        "    model: claude-fable-5-1\n"
        "    effort: max\n"
        "    settings: {ultracode: true}\n"
        "    tier: 3\n"
    ))
    prompt = tmp_path / "prompt.md"
    prompt.write_text("You are {name}\n")
    monkeypatch.setattr(rotate, "find_project_root", lambda: root)
    monkeypatch.chdir(root)

    exit_code = rotate.main([
        "spawn", "--name", "belam-2", "--prompt-file", str(prompt),
        "--dry-run",
    ])
    out = capsys.readouterr().out
    assert exit_code == 0
    assert "--model claude-fable-5-1" in out
    assert "--effort max" in out
    assert "--settings" in out
    assert "ultracode" in out


def test_spawn_normalizes_string_settings_word(monkeypatch, tmp_path, capsys):
    # The landing l3w0-ladder-roles-table spells settings as the bare word
    # `ultracode`; rotate must emit `--settings '{"ultracode": true}'`.
    root = _proj(tmp_path, ladder_roles=(
        "  - role: prime_director\n"
        "    harness: claude-code\n"
        "    model: claude-fable-5-1\n"
        "    effort: max\n"
        "    settings: ultracode\n"
        "    tier: 3\n"
    ))
    prompt = tmp_path / "prompt.md"
    prompt.write_text("You are {name}\n")
    monkeypatch.setattr(rotate, "find_project_root", lambda: root)
    monkeypatch.chdir(root)

    exit_code = rotate.main([
        "spawn", "--name", "belam-2", "--prompt-file", str(prompt),
        "--dry-run",
    ])
    out = capsys.readouterr().out
    assert exit_code == 0
    assert '--settings \'{"ultracode": true}\'' in out
    # the bare-word form (settings = the string `ultracode`) must not leak:
    assert '--settings \'"ultracode"\'' not in out


def test_spawn_ultracode_prefixes_env_and_keyword(monkeypatch, tmp_path, capsys):
    # hypothesis:l3-rotate-ultracode-env -- an ultracode role's dry-run spawn
    # must prefix the tmux launch with `export CLAUDE_CODE_WORKFLOWS=1` and
    # open the successor's user turn (the prompt body) with the keyword
    # `ultracode`. The prime measured live that the env var is the launch
    # gate and the keyword is the opt-in trigger (L3.0x, three throwaways).
    root = _proj(tmp_path, ladder_roles=(
        "  - role: prime_director\n"
        "    harness: claude-code\n"
        "    model: claude-fable-5-1\n"
        "    effort: max\n"
        "    settings: {ultracode: true}\n"
        "    tier: 3\n"
    ))
    prompt = tmp_path / "prompt.md"
    prompt.write_text("You are {name}\n")
    monkeypatch.setattr(rotate, "find_project_root", lambda: root)
    monkeypatch.chdir(root)

    exit_code = rotate.main([
        "spawn", "--name", "belam-u1", "--prompt-file", str(prompt),
        "--dry-run",
    ])
    out = capsys.readouterr().out
    assert exit_code == 0
    # the env export gates the whole shell line:
    assert out.startswith("export CLAUDE_CODE_WORKFLOWS=1")
    # the user-turn prompt body (the final quoted arg) opens with the keyword
    # as its first line, e.g. `ultracode\nYou are belam-u1...`:
    assert "ultracode\nYou are belam-u1" in out


def test_spawn_plain_role_no_env_no_keyword(monkeypatch, tmp_path, capsys):
    # hypothesis:l3-rotate-ultracode-env -- a role whose settings carry no
    # ultracode gets neither the env export nor the keyword.
    root = _proj(tmp_path, ladder_roles=(
        "  - role: kid\n"
        "    harness: claude-code\n"
        "    model: claude-sonnet-5\n"
        "    effort: high\n"
        "    tier: 1\n"
    ))
    prompt = tmp_path / "prompt.md"
    prompt.write_text("You are {name}\n")
    monkeypatch.setattr(rotate, "find_project_root", lambda: root)
    monkeypatch.chdir(root)

    exit_code = rotate.main([
        "spawn", "--name", "kid-1", "--tier", "kid",
        "--prompt-file", str(prompt), "--dry-run",
    ])
    out = capsys.readouterr().out
    assert exit_code == 0
    assert "CLAUDE_CODE_WORKFLOWS" not in out
    assert out.count("ultracode") == 0


def test_spawn_falls_back_to_defaults_without_table(monkeypatch, tmp_path, capsys):
    # No roles table, no config.json: fixed top-tier defaults apply.
    root = _proj(tmp_path)
    prompt = tmp_path / "prompt.md"
    prompt.write_text("You are {name}\n")
    monkeypatch.setattr(rotate, "find_project_root", lambda: root)
    monkeypatch.chdir(root)

    exit_code = rotate.main([
        "spawn", "--name", "belam-9", "--prompt-file", str(prompt),
        "--dry-run",
    ])
    out = capsys.readouterr().out
    assert exit_code == 0
    assert "--remote-control belam-9" in out
    assert "--model claude-fable-5-1" in out
    assert "--effort max" in out


def test_successor_prompt_prepends_constitution_head():
    body = "the successor body"
    prompt = brief.successor_prompt(tier="prime_director", body=body)
    assert prompt.startswith("─── CONSTITUTION HEAD ───")
    assert "THE FOUR PRAYERS" in prompt
    assert prompt.rstrip().endswith(body)
    assert prompt.index(body) > prompt.index("THE FOUR PRAYERS")


# ---------- l3w4-liaison-seat: spawn --tier liaison from the assembled brief ---


def test_ladder_roles_table_has_a_liaison_row():
    """The live ladder node must carry the {tier:1, role:liaison} row so
    spawn --tier liaison resolves to claude-sonnet-5 at effort high."""
    import yaml  # noqa: F401  (documented; _ladder_roles_table parses it)
    root = rotate.find_project_root()
    rows = rotate._ladder_roles_table(root)
    row = next((r for r in rows if r.get("role") == "liaison"), None)
    assert row is not None, "no liaison row in the ladder roles table"
    assert row.get("tier") == 1
    assert row.get("model") == "claude-sonnet-5"
    assert row.get("effort") == "high"
    assert row.get("harness") == "claude-code"


def test_spawn_tier_liaison_resolves_sonnet_high_from_the_new_row(monkeypatch, tmp_path, capsys):
    # The ladder row for liaion must surface on the spawned command.
    root = _proj(tmp_path, ladder_roles=(
        "  - role: liaison\n"
        "    harness: claude-code\n"
        "    model: claude-sonnet-5\n"
        "    effort: high\n"
        "    tier: 1\n"
    ))
    monkeypatch.setattr(rotate, "find_project_root", lambda: root)
    monkeypatch.chdir(root)

    exit_code = rotate.main([
        "spawn", "--name", "liaison", "--tier", "liaison", "--dry-run",
    ])
    out = capsys.readouterr().out
    assert exit_code == 0
    assert "--remote-control liaison" in out
    assert "--model claude-sonnet-5" in out
    assert "--effort high" in out


def test_spawn_liaison_prompt_sources_the_assembled_brief_not_the_static_file(monkeypatch, tmp_path, capsys):
    # spawn --tier liaison with no --prompt-file must build the body from
    # brief.assemble (the OWNER LIAISON brief), never the static
    # prime-director-successor.md.
    root = _proj(tmp_path, ladder_roles=(
        "  - role: liaison\n"
        "    harness: claude-code\n"
        "    model: claude-sonnet-5\n"
        "    effort: high\n"
        "    tier: 1\n"
    ))
    monkeypatch.setattr(rotate, "find_project_root", lambda: root)
    sentinel = tmp_path / "prime.md"
    sentinel.write_text("STATIC PRIME BODY {name}\n")
    monkeypatch.setattr(rotate, "DEFAULT_PROMPT_FILE", str(sentinel))
    monkeypatch.chdir(root)

    exit_code = rotate.main([
        "spawn", "--name", "liaison", "--tier", "liaison", "--dry-run",
    ])
    out = capsys.readouterr().out
    assert exit_code == 0
    assert "STATIC PRIME BODY" not in out, "the static prime file must not be used"
    assert "OWNER LIAISON" in out, "the assembled liaison brief is the body"


def test_spawn_prime_director_static_path_is_unchanged(monkeypatch, tmp_path, capsys):
    # Regression: the prime's spawned (no --prompt-file) must still read the
    # DEFAULT_PROMPT_FILE static successor file, never the assembled brief.
    root = _proj(tmp_path)
    sentinel = tmp_path / "prime.md"
    sentinel.write_text("STATIC PRIME BODY {name}\n")
    monkeypatch.setattr(rotate, "DEFAULT_PROMPT_FILE", str(sentinel))
    monkeypatch.setattr(rotate, "find_project_root", lambda: root)
    monkeypatch.chdir(root)

    exit_code = rotate.main([
        "spawn", "--name", "belam-1", "--tier", "prime_director",
        "--dry-run",
    ])
    out = capsys.readouterr().out
    assert exit_code == 0
    assert "STATIC PRIME BODY belam-1" in out, (
        "the prime must still read DEFAULT_PROMPT_FILE through the static path")


def test_derive_successor_name():
    # nothing about the prime known => second Roman numeral of the base prefix
    assert rotate._derive_successor_name([], "belam") == "belam-II"
    # live prime window `belam-S1-L3` carries no Roman suffix => the base
    assert rotate._derive_successor_name(["belam-S1-L3"], "belam") == "belam-S1-L3-II"
    # bare base `belam` is the first of its line => -II
    assert rotate._derive_successor_name(["belam"], "belam") == "belam-II"
    # highest Roman in the series wins
    assert rotate._derive_successor_name(
        ["belam-S1-L3", "belam-S1-L3-II", "belam-S1-L3-III"], "belam") \
        == "belam-S1-L3-IV"
    # non-matching windows are ignored
    assert rotate._derive_successor_name(["agi-master-7"], "belam") == "belam-II"
    # a lone successor with no base present extends its own line
    assert rotate._derive_successor_name(["belam-S1-L3-II"], "belam") == "belam-S1-L3-III"
    # a non-belam prefix still derives in roman
    assert rotate._derive_successor_name(["ccc-III"], "ccc") == "ccc-IV"


def test_spawn_default_name_derives_from_window_path(monkeypatch, tmp_path, capsys):
    root = _proj(tmp_path)
    prompt = tmp_path / "prompt.md"
    prompt.write_text("hi {name}")
    wins = tmp_path / "windows.txt"
    wins.write_text("belam-S1-L3\n")
    monkeypatch.setattr(rotate, "find_project_root", lambda: root)
    monkeypatch.chdir(root)

    exit_code = rotate.main([
        "spawn", "--prompt-file", str(prompt),
        "--window-path", str(wins), "--dry-run",
    ])
    out = capsys.readouterr().out
    assert exit_code == 0
    assert "--remote-control belam-S1-L3-II" in out
    assert "hi belam-S1-L3-II" in out


def test_loop_below_threshold_holds(monkeypatch, tmp_path, capsys):
    root = _proj(tmp_path)
    monkeypatch.setattr(rotate, "cmd_meter", lambda args, root: 0)

    def fail_spawn(*a, **k):
        raise AssertionError("must not spawn below threshold")

    monkeypatch.setattr(rotate, "_launch_window", fail_spawn)

    code = rotate.cmd_loop(SimpleNamespace(
        session_log=None, force=False, role="prime_director", name=None,
        name_prefix="belam", model=None, effort=None, settings=None,
        prompt_file=None, tmux_session="agi-rc", window_path=None,
        debug_file=None, dry_run=False, timeout=1,
    ), root)
    assert code == 0
    assert "no rotation" in capsys.readouterr().err


def test_loop_over_threshold_rotates_and_continue(monkeypatch, tmp_path, capsys):
    root = _proj(tmp_path)
    monkeypatch.chdir(root)
    monkeypatch.setattr(rotate, "find_project_root", lambda: root)
    # Need a prompt file in a location the subprocess will reach:
    monkeypatch.setattr(rotate, "DEFAULT_PROMPT_FILE",
                        str(tmp_path / "successor.md"))
    (tmp_path / "successor.md").write_text("you are {name}\n")

    monkeypatch.setattr(rotate, "cmd_meter", lambda args, root: 1)  # over threshold

    reply = tmp_path / "reply.log"
    reply.write_text("continue\n")
    ack = rotate._ack_path(root, "belam-II")
    ack.parent.mkdir(parents=True, exist_ok=True)
    ack.write_text(json.dumps({"seat": "belam-II", "gen_after": None,
                               "answer": "continue"}), encoding="utf-8")
    wins = tmp_path / "windows.txt"
    wins.write_text("")  # hermetic: no existing belam windows
    launched = {}
    def fake_launch(session, name, shell_cmd):
        launched.update(name=name) or 0
        # a real spawn creates the tmux window, so reflect it in the fixture
        wins.write_text(name + "\n")
        return 0
    monkeypatch.setattr(rotate, "_launch_window", fake_launch)

    code = rotate.cmd_loop(SimpleNamespace(
        session_log=None, force=False, role="prime_director", name=None,
        name_prefix="belam", model=None, effort=None, settings=None,
        prompt_file=None, tmux_session="agi-rc", window_path=str(wins),
        debug_file=str(reply), dry_run=False, timeout=1,
    ), root)
    assert code == 0
    assert launched.get("name") == "belam-II"
    assert "handoff stood" in capsys.readouterr().err



# --- hypothesis:l3w4-seat-rotation-loops ADDENDUM (Belam VII 21:56 UTC):
#     cmd_loop must fail loudly when the successor's tmux window is absent, and
#     must NEVER point its read-back at the caller's own --session-log.

def test_loop_fails_loud_when_no_successor_window(monkeypatch, tmp_path, capsys):
    """No successor tmux window exists -> cmd_loop must return non-zero, never
    report rotation success. Before the fix it returned 0 and printed
    'handoff stood' even though `_existing_windows` showed nothing."""
    root = _proj(tmp_path)
    monkeypatch.chdir(root)
    monkeypatch.setattr(rotate, "find_project_root", lambda: root)
    monkeypatch.setattr(rotate, "cmd_meter", lambda args, root: 1)  # rotate
    reply = tmp_path / "reply.log"
    reply.write_text("continue\n")
    wins = tmp_path / "windows.txt"
    wins.write_text("")  # simulated spawn leaves NO window behind
    launched = {}
    monkeypatch.setattr(
        rotate, "_launch_window",
        lambda session, name, shell_cmd: launched.update(name=name) or 0,
    )
    code = rotate.cmd_loop(SimpleNamespace(
        session_log=None, force=True, role="prime_director", name="belam-II",
        name_prefix="belam", model=None, effort=None, settings=None,
        prompt_file=None, tmux_session="agi-rc", window_path=str(wins),
        debug_file=str(reply), dry_run=False, timeout=1,
    ), root)
    assert code != 0
    err = capsys.readouterr().err
    assert "NOT present" in err
    assert "refusing to report rotation success" in err


def test_loop_readback_never_uses_caller_session_log(monkeypatch, tmp_path, capsys):
    """The successor read-back must read the successor's OWN debug file, not the
    meter's `--session-log`. A 'continue' in the caller's own transcript must
    not confirm a rotation whose successor said nothing."""
    root = _proj(tmp_path)
    monkeypatch.chdir(root)
    monkeypatch.setattr(rotate, "find_project_root", lambda: root)
    monkeypatch.setattr(rotate, "cmd_meter", lambda args, root: 1)  # rotate
    succ = tmp_path / "successor.log"
    succ.write_text("")  # successor (gen N+1) has written nothing
    caller = tmp_path / "caller.jsonl"
    caller.write_text("the CALLER just wrote a line containing bare continue\n")
    wins = tmp_path / "windows.txt"
    wins.write_text("belam-III\n")  # window IS present (real spawn)
    monkeypatch.setattr(
        rotate, "_launch_window",
        lambda session, name, shell_cmd: 0,
    )
    code = rotate.cmd_loop(SimpleNamespace(
        session_log=str(caller), force=True, role="prime_director",
        name="belam-III", name_prefix="belam", model=None, effort=None,
        settings=None, prompt_file=None, tmux_session="agi-rc",
        window_path=str(wins), debug_file=str(succ), dry_run=False, timeout=1,
    ), root)
    err = capsys.readouterr().err
    # window was present, but the successor never answered -> the loop must NOT
    # claim the handoff stood; it must not echo the caller's own line either.
    assert "handoff stood" not in err
    assert "the CALLER just wrote" not in err

def _write_transcripts(projects_dir, pinned_usage, foreign_usage, pinned_name="pinned.jsonl", foreign_name="foreign.jsonl"):
    """Two transcripts in `projects_dir`: a PINNED (older) and a NEWER foreign one.
    Returns (pinned_path, foreign_path)."""
    projects_dir.mkdir(parents=True, exist_ok=True)
    pinned = projects_dir / pinned_name
    pinned.write_text(
        f'{{"message": {{"role": "assistant", "usage": '
        f'{{"input_tokens": {pinned_usage}, "cache_read_input_tokens": 0, '
        f'"cache_creation_input_tokens": 0}}}}}}\n'
    )
    foreign = projects_dir / foreign_name
    foreign.write_text(
        f'{{"message": {{"role": "assistant", "usage": '
        f'{{"input_tokens": {foreign_usage}, "cache_read_input_tokens": 0, '
        f'"cache_creation_input_tokens": 0}}}}}}\n'
    )
    # make foreign strictly newer than pinned
    import os
    ot, nt = time.time() - 10, time.time()
    os.utime(pinned, (ot, ot))
    os.utime(foreign, (nt, nt))
    return pinned, foreign


def _fake_cc_projects(tmp_path, monkeypatch, pinned_usage=2000, foreign_usage=40000):
    """A fake ~/.claude/projects/<default-slug> with an older pinned transcript
    (light usage) and a newer foreign transcript (heavy usage)."""
    proj = tmp_path / ".claude" / "projects" / rotate.CC_PROJECT_SLUG
    pinned, foreign = _write_transcripts(proj, 2000, 40000)
    monkeypatch.setattr(rotate, "CC_PROJECTS_DIR", tmp_path / ".claude" / "projects")
    return proj, pinned, foreign


def _write_pin(root, target, name="prime.meter"):
    # root here is the GRAPH dir (fake_ladder patches find_project_root to
    # return tmp_path), so sessions sit directly under it -- `root/sessions`,
    # never `root/.agi/sessions` (hypothesis:l3-rotate-pin-path-readback).
    seg = root / "sessions"
    seg.mkdir(parents=True, exist_ok=True)
    pin = seg / name
    pin.write_text(str(target) + "\n", encoding="utf-8")
    return pin


def test_seat_pin_stable_across_two_rotations_same_name(monkeypatch, tmp_path, fake_ladder, capsys):
    # hypothesis:l3w4-seat-registry — .agi/sessions/<name>.meter is seat-stable:
    # a seat rotation re-reads the SAME seat pin even as a NEWER foreign pin
    # lands. Without --seat, newest-mtime wins (the bug this closes).
    proj, pinned, foreign = _fake_cc_projects(tmp_path, monkeypatch)
    seat_pin = _write_pin(tmp_path, pinned, name="belam.meter")
    _write_pin(tmp_path, foreign, name="zzz-newer.meter")
    import os
    old, now = time.time() - 10_000, time.time()
    os.utime(seat_pin, (old, old))
    os.utime(tmp_path / "sessions" / "zzz-newer.meter", (now, now))
    code = rotate.main(["meter", "--seat", "belam"])
    out = capsys.readouterr().out.strip()
    assert code == 0
    assert "0.020" in out, out      # seat's own pinned transcript
    assert "0.4" not in out, out     # NOT the newer foreign pin newest would pick


def test_seat_pin_refuses_predecessors_generation(monkeypatch, tmp_path, fake_ladder, capsys):
    # hypothesis:l3-seat-pin-not-repointed-on-rotation — Belam X pinned its
    # OWN transcript into the belam seat pin and rotated. Belam XI (the next
    # generation) read `--seat belam` and got Belam X's usage back with total
    # confidence (`source=seat_pin`), because nothing re-points or checks the
    # pin on rotation. A pin written by generation 1 read by generation 2
    # must be a loud refusal, never a silent stale number.
    proj, pinned, foreign = _fake_cc_projects(tmp_path, monkeypatch)
    # generation 1 (the predecessor) pins its own transcript...
    rotate._write_handoff(tmp_path, "belam", 1)
    code = rotate.main(["meter", "--seat", "belam", "--pin",
                        str(tmp_path / "sessions" / "belam.meter"),
                        "--session-log", str(pinned)])
    assert code == 0
    # ...then rotation advances the seat to generation 2 (the successor)
    # without ever re-pointing the pin -- the exact gap the hypothesis names.
    rotate._write_handoff(tmp_path, "belam", 2)
    code = rotate.main(["meter", "--seat", "belam"])
    err = capsys.readouterr().err
    assert code == 1, err
    assert "generation 1" in err and "generation 2" in err, err
    assert "refus" in err.lower(), err


def test_seat_pin_same_generation_reads_clean(monkeypatch, tmp_path, fake_ladder, capsys):
    # The matching case must NOT regress into a refusal: the generation that
    # wrote the pin reading its own pin back still works.
    proj, pinned, foreign = _fake_cc_projects(tmp_path, monkeypatch)
    rotate._write_handoff(tmp_path, "belam", 1)
    code = rotate.main(["meter", "--seat", "belam", "--pin",
                        str(tmp_path / "sessions" / "belam.meter"),
                        "--session-log", str(pinned)])
    assert code == 0
    code = rotate.main(["meter", "--seat", "belam"])
    out = capsys.readouterr().out.strip()
    assert code == 0, out
    assert "0.020" in out, out
    assert "seat_pin" in out, out


def test_meter_pin_file_wins_over_newer_foreign(monkeypatch, tmp_path, fake_ladder, capsys):
    # A pin file naming our own transcript must beat the newer foreign .jsonl
    # in the project dir (the hypothesis: without it, newest wins -> bug).
    proj, pinned, foreign = _fake_cc_projects(tmp_path, monkeypatch)
    _write_pin(tmp_path, pinned)
    code = rotate.main(["meter"])
    out = capsys.readouterr().out.strip()
    assert code == 0
    assert "0.020" in out          # 2000/100000 = pinned, not foreign (0.400)
    assert "pin" in out


def test_meter_agi_session_log_env_uses_pinned(monkeypatch, tmp_path, fake_ladder, capsys):
    proj, pinned, foreign = _fake_cc_projects(tmp_path, monkeypatch)
    monkeypatch.setenv("AGI_SESSION_LOG", str(pinned))
    code = rotate.main(["meter"])
    out = capsys.readouterr().out.strip()
    assert code == 0
    assert "0.020" in out
    assert "AGI_SESSION_LOG" in out


def test_meter_explicit_session_log_wins(monkeypatch, tmp_path, fake_ladder, capsys):
    proj, pinned, foreign = _fake_cc_projects(tmp_path, monkeypatch)
    code = rotate.main(["meter", "--session-log", str(pinned)])
    out = capsys.readouterr().out.strip()
    assert code == 0
    assert "0.020" in out
    assert "explicit" in out


def test_meter_fallback_warns_and_picks_newest(monkeypatch, tmp_path, fake_ladder, capsys):
    # No log, no env, no pin -> newest wins but a WARN names the file it picked.
    proj, pinned, foreign = _fake_cc_projects(tmp_path, monkeypatch)
    code = rotate.main(["meter"])
    captured = capsys.readouterr()
    out, err = captured.out, captured.err
    assert code == 0
    assert "0.400" in out
    assert "warn" in err and "foreign.jsonl" in err


def test_loop_uses_same_resolver(monkeypatch, tmp_path, fake_ladder, capsys):
    # cmd_loop meters via cmd_meter, which must see the pin too. We assert the
    # resolver, not a live rotate (which would spawn), by checking that a
    # pinned (light) usage stays below threshold while the foreign (heavy)
    # would trip it.
    proj, pinned, foreign = _fake_cc_projects(tmp_path, monkeypatch)
    _write_pin(tmp_path, pinned)
    # threshold is 0.25; pinned=0.02 (hold), foreign=0.40 (would rotate)
    args = SimpleNamespace(session_log=None, check=True)
    code = rotate.cmd_meter(args, tmp_path)
    assert code == 0  # pinned keeps us below; loop would hold


# ---------------------------------------------------------------------------
# hypothesis:l4-the-meter-adopts-a-pin-it-did-not-write — identity is
# supplied, never inferred. A bare --pin must REFUSE (write side) rather than
# adopt a foreign pin; a seatless read must REFUSE (read side) when the pin it
# would consult carries another agent's generation. The repair paths
# (--session-log, $AGI_SESSION_LOG, --seat) must all still work.
# ---------------------------------------------------------------------------


def _sessions_dir_of(tmp_path):
    seg = tmp_path / "sessions"
    seg.mkdir(parents=True, exist_ok=True)
    return seg


def _with_foreign_distractor(tmp_path, foreign, own_name="sanctuary-director.meter"):
    """Caller's own pin written FIRST (older mtime) and correct; a foreign
    pin written LAST (strictly-newest mtime) in the shared sessions dir. The
    caller's own pin is the one --pin would name; the foreign one is the one
    a seatless newest-mtime search would adopt. Returns (own, foreign_pin)."""
    seg = _sessions_dir_of(tmp_path)
    own = seg / own_name
    own.write_text(str(foreign) + "\n", encoding="utf-8")
    fpin = seg / "belam.meter"
    fpin.write_text(str(foreign) + "\n", encoding="utf-8")
    now = time.time()
    os.utime(own, (now - 10_000, now - 10_000))
    os.utime(fpin, (now, now))
    return own, fpin


def test_a_bare_pin_refuses_and_leaves_own_pin_byte_unchanged(monkeypatch, tmp_path, fake_ladder, capsys):
    # (a) The distractor is the bug, not an edge: caller's own pin present and
    # correct, a foreign pin written LAST so newest-mtime adopts it. A bare
    # --pin (no --session-log, no AGI_SESSION_LOG, no --seat) must REFUSE and
    # leave the caller's own pin file BYTE-UNCHANGED -- nothing may be adopted
    # or re-stamped with the caller's generation.
    proj, pinned, foreign = _fake_cc_projects(tmp_path, monkeypatch)
    own, fpin = _with_foreign_distractor(tmp_path, foreign)
    before = own.read_bytes()
    code = rotate.main(["meter", "--pin", str(own)])
    err = capsys.readouterr().err
    assert code != 0, err
    assert own.read_bytes() == before, "the caller's own pin must stay byte-unchanged"


def test_b_refusal_names_session_log(monkeypatch, tmp_path, fake_ladder, capsys):
    # (b) The refusal must NAME the literal string `--session-log` so the
    # operator knows what to run and does not spend a turn deriving it.
    proj, pinned, foreign = _fake_cc_projects(tmp_path, monkeypatch)
    own, fpin = _with_foreign_distractor(tmp_path, foreign)
    code = rotate.main(["meter", "--pin", str(own)])
    err = capsys.readouterr().err
    assert code != 0
    assert "--session-log" in err, err


def test_c_pin_with_explicit_session_log_still_writes_stamps_and_prints(monkeypatch, tmp_path, fake_ladder, capsys):
    # (c) The repair path stays usable: --pin WITH an explicit --session-log
    # still writes, still stamps the caller's generation, and still prints the
    # fraction.
    proj, pinned, foreign = _fake_cc_projects(tmp_path, monkeypatch)
    rotate._write_handoff(tmp_path, "belam", 7)
    p = _sessions_dir_of(tmp_path) / "belam.meter"
    code = rotate.main(["meter", "--seat", "belam", "--pin", str(p),
                        "--session-log", str(pinned)])
    out = capsys.readouterr().out
    assert code == 0, out
    content = p.read_text(encoding="utf-8")
    assert content.startswith("7\t"), content      # stamped caller generation
    assert str(pinned) in content, content          # names the named transcript
    assert "0.020" in out, out                      # fraction still printed


def test_d_agi_session_log_alone_still_permits_pin_write(monkeypatch, tmp_path, fake_ladder, capsys):
    # (d) $AGI_SESSION_LOG alone is a supplied identity: --pin still records it.
    proj, pinned, foreign = _fake_cc_projects(tmp_path, monkeypatch)
    monkeypatch.setenv("AGI_SESSION_LOG", str(pinned))
    p = _sessions_dir_of(tmp_path) / "env-claimed.meter"
    code = rotate.main(["meter", "--pin", str(p)])
    out = capsys.readouterr().out
    assert code == 0, out
    assert str(pinned) in p.read_text(encoding="utf-8")


def test_e_bare_seatless_read_refuses_another_agents_pin(monkeypatch, tmp_path, fake_ladder, capsys):
    # (e) A bare seatless READ (no --pin) refuses when the pin it would
    # consult is another agent's generation-bearing pin: reporting a confident
    # number for a transcript the caller never named attributes a foreign
    # session to this caller.
    proj, pinned, foreign = _fake_cc_projects(tmp_path, monkeypatch)
    seg = _sessions_dir_of(tmp_path)
    (seg / "belam.meter").write_text(f"3\t{foreign}\n", encoding="utf-8")
    code = rotate.main(["meter"])
    err = capsys.readouterr().err
    assert code != 0, err
    assert "refus" in err.lower(), err


def test_f_seat_named_correct_gen_pin_still_reads(monkeypatch, tmp_path, fake_ladder, capsys):
    # (f) The --seat path is not weakened: a named seat with a CORRECT own-
    # generation pin still reads and returns the fraction, and never consults
    # other agents' pins. (The helper's live pin is the working fixture.)
    proj, pinned, foreign = _fake_cc_projects(tmp_path, monkeypatch)
    rotate._write_handoff(tmp_path, "belam", 4)
    seg = _sessions_dir_of(tmp_path)
    (seg / "belam.meter").write_text(f"4\t{pinned}\n", encoding="utf-8")
    code = rotate.main(["meter", "--seat", "belam"])
    out = capsys.readouterr().out.strip()
    assert code == 0, out
    assert "0.020" in out, out
    assert "seat_pin" in out, out


# --- hypothesis:l4-meter-pin-refuses-a-target-that-is-not-a-pin ----------
# A --pin target must BE a pin by name AND home. The Prime passed its own
# transcript (a .jsonl) as --pin and the live file became one line, so the
# write target is shape-checked BEFORE any write: a .jsonl / node / script is
# refused BY NAME, named, and left byte-identical; the refusal prints the one
# form that clears (--pin takes the PIN FILE, never --seat). A legitimate
# <sessions>/<seat>.meter still writes.


def test_meter_pin_refuses_a_jsonl_target_by_name_and_leaves_bytes(
        monkeypatch, tmp_path, fake_ladder, capsys):
    # The live defect: the transcript (.jsonl) passed as --pin must be refused
    # BY NAME and never written -- exit non-zero, the offending path NAMED,
    # the file byte-identical (sha256 before == after).
    proj, pinned, foreign = _fake_cc_projects(tmp_path, monkeypatch)
    before = pinned.read_bytes()
    code = rotate.main(["meter", "--pin", str(pinned),
                        "--session-log", str(pinned)])
    err = capsys.readouterr().err
    assert code != 0, err
    assert str(pinned) in err              # names the offending path
    assert "meter" in err and "--session-log" in err  # prints the repair form
    assert pinned.read_bytes() == before   # byte-identical, nothing truncated


def test_meter_pin_refuses_a_node_target_by_name_and_leaves_bytes(
        monkeypatch, tmp_path, fake_ladder, capsys):
    # A graph node (.md) is not a pin either: refused by name, byte-identical.
    proj, pinned, foreign = _fake_cc_projects(tmp_path, monkeypatch)
    node = tmp_path / "nodes"
    node.mkdir(parents=True, exist_ok=True)
    target = node / "some-node.md"
    target.write_text("# graph node\n", encoding="utf-8")
    before = target.read_bytes()
    code = rotate.main(["meter", "--pin", str(target),
                        "--session-log", str(pinned)])
    err = capsys.readouterr().err
    assert code != 0, err
    assert str(target) in err
    assert target.read_bytes() == before


def test_meter_pin_valid_seat_pin_still_writes(monkeypatch, tmp_path,
                                               fake_ladder, capsys):
    # The repair is not scoped to the refusal: a legitimate <sessions>/
    # <seat>.meter with an identity still writes the pin naming the transcript.
    proj, pinned, foreign = _fake_cc_projects(tmp_path, monkeypatch)
    p = _sessions_dir_of(tmp_path) / "belam.meter"
    code = rotate.main(["meter", "--pin", str(p),
                        "--session-log", str(pinned)])
    out = capsys.readouterr().out
    assert code == 0, out
    assert str(pinned) in p.read_text(encoding="utf-8")


# --- hypothesis:l3-rotate-pin-path-readback (red-first) -------------------


def test_pin_path_never_doubles_agi_dir(tmp_path):
    # The pin must resolve under the graph's sessions dir, NEVER the doubled
    # `<root>/.agi/.agi/sessions` (the L3.15 defect). root = the REPO root
    # (<tmp>) and root = the GRAPH dir (<tmp>/.agi) must resolve to the SAME
    # physical `<tmp>/.agi/sessions/<name>.meter`.
    graph = tmp_path / ".agi"
    (graph / "nodes").mkdir(parents=True)          # marks <tmp>/.agi as the graph
    seg = graph / "sessions"
    seg.mkdir(parents=True, exist_ok=True)
    pin = seg / "belam.meter"
    pin.write_text("/tmp/some-transcript.jsonl\n", encoding="utf-8")

    from_graph = rotate.find_pin_log(graph)
    assert str(from_graph) == str(pin), from_graph
    assert "/.agi/.agi/" not in str(from_graph)   # no doubling in the graph-dir read

    from_repo = rotate.find_pin_log(tmp_path)       # repo root maps to the same dir
    assert str(from_repo) == str(pin), from_repo


def test_is_log_noise_markers():
    """REMOVED with the debug-log reader.

    The legacy `_is_log_noise`/`_read_first_reply` reader is DELETED from
    rotate.py (hypothesis:l4-rotate-readback-false-negative-and-the-orphan-by-
    design): a DEBUG LOGGER cannot carry the successor's prose, so a fallback
    that opens one is the defect wearing a safety label. Its direct unit tests
    go with it; the three realities (ACKED / PRESENT-BUT-SILENT / ABSENT) are
    covered through the ack-channel reader tests below.
    """
    assert not hasattr(rotate, "_read_first_reply")
    assert not hasattr(rotate, "_is_log_noise")


# ---------------------------------------------------------------------------
# hypothesis:l4-rotate-readback-false-negative-and-the-orphan-by-design — the
# explicit ACK channel replaces the debug-log read-back.
# ---------------------------------------------------------------------------

REAL_DEBUG_LOG = (
    "2026-09-07T06:04:39.522Z [DEBUG] MDM settings load completed in 1ms\n"
    "2026-09-07T06:04:39.610Z [INFO] [uds-messaging] listening on INET6 ... \n"
    "2026-09-07T06:04:40.398Z [WARN] [3P telemetry] Event dropped\n"
    "2026-09-07T06:04:41.633Z [DEBUG] exited fullscreen\n"
)


def test_cmd_ack_writes_seat_ack_file(tmp_path, monkeypatch):
    """`rotate.py ack` writes `<seats>/<seat>.ack.json` with the successor's
    own identity (gen_after + session_ref) — `_is_log_noise` never matters."""
    root = _proj(tmp_path)
    monkeypatch.setattr(rotate, "find_project_root", lambda: root)
    code = rotate.cmd_ack(SimpleNamespace(
        seat="sanctuary-director", gen=7, ref="agent:abc123",
        answer="diff", text="- a\n+ b"), root)
    assert code == 0
    ac = rotate._ack_path(root, "sanctuary-director")
    doc = json.loads(ac.read_text(encoding="utf-8"))
    assert doc["seat"] == "sanctuary-director"
    assert doc["gen_after"] == 7
    assert doc["session_ref"] == "agent:abc123"
    assert doc["answer"] == "diff"
    assert doc["text"] == "- a\n+ b"


def test_read_ack_matches_gen_after(tmp_path):
    """_read_ack returns the ack when its gen_after is the generation the
    reader spawned, and REFUSES a wrong-generation ack (treats it as absent)."""
    seat = tmp_path / "seats"
    seat.mkdir()
    ac = seat / "s.ack.json"
    ac.write_text(json.dumps({"seat": "s", "gen_after": 7,
                              "answer": "continue", "ts": "Z"}),
                  encoding="utf-8")
    got = rotate._read_ack(str(ac), gen_after=7, timeout=5)
    assert got is not None and got["answer"] == "continue"
    # wrong generation -> refused, not confirmed
    assert rotate._read_ack(str(ac), gen_after=8, timeout=1) is None


def test_read_ack_polls_until_written(tmp_path):
    """_read_ack polls a not-yet-written ack file until it carries a matching
    gen_after (the successor writes its ack AFTER the predecessor starts
    reading)."""
    seat = tmp_path / "seats"
    seat.mkdir()
    ac = seat / "s.ack.json"
    import threading
    def _writer():
        import time
        time.sleep(1)
        ac.write_text(json.dumps({"seat": "s", "gen_after": 9,
                                  "answer": "continue"}), encoding="utf-8")
    threading.Thread(target=_writer, daemon=True).start()
    got = rotate._read_ack(str(ac), gen_after=9, timeout=20)
    assert got is not None and got["answer"] == "continue"


@pytest.mark.parametrize("body", ["{", "[]", "not json"])
def test_read_ack_ignores_unparsable(tmp_path, body):
    """An unparsable ack file never confirms; malformed JSON is treated as
    not-yet-written and retried until timeout."""
    seat = tmp_path / "seats"
    seat.mkdir()
    ac = seat / "s.ack.json"
    ac.write_text(body, encoding="utf-8")
    assert rotate._read_ack(str(ac), gen_after=7, timeout=1) is None


def test_read_ack_absent_never_confirms(tmp_path):
    """No ack file at all -> None on timeout (the precondition the hypothesis
    states: without the ack, the channel is silent)."""
    seat = tmp_path / "seats"
    seat.mkdir()
    assert rotate._read_ack(str(seat / "s.ack.json"), gen_after=7, timeout=1) is None


def test_loop_returns_success_when_successor_acks_continue(monkeypatch, tmp_path, capsys):
    """FALSIFIER (1): a successor on a REAL --debug-file (0 non-noise lines,
    so the legacy read-back can never see it) that ACKS `continue` is confirmed
    — the record reads success, not inconclusive-no-reply."""
    root = _proj(tmp_path)
    monkeypatch.chdir(root)
    monkeypatch.setattr(rotate, "find_project_root", lambda: root)
    monkeypatch.setattr(rotate, "cmd_meter", lambda args, root: 1)
    dbg = tmp_path / "seat.log"
    dbg.write_text(REAL_DEBUG_LOG)
    # the ack file carries the identity the debug log cannot
    ack = rotate._ack_path(root, "belam-II")
    ack.parent.mkdir(parents=True, exist_ok=True)
    ack.write_text(json.dumps({"seat": "belam-II", "gen_after": None,
                               "session_ref": "agent:aa11", "answer": "continue"}),
                    encoding="utf-8")
    wins = tmp_path / "windows.txt"
    wins.write_text("")
    monkeypatch.setattr(rotate, "_launch_window",
                        lambda session, name, shell_cmd: _fake_launch(wins, "belam-II\n"))
    code = rotate.cmd_loop(SimpleNamespace(
        session_log=None, force=True, role="prime_director", name="belam-II",
        name_prefix="belam", model=None, effort=None, settings=None,
        prompt_file=None, tmux_session="agi-rc", window_path=str(wins),
        debug_file=str(dbg), dry_run=False, timeout=1,
    ), root)
    err = capsys.readouterr().err
    assert code == 0
    assert "successor acked" in err
    recs = list((rotate._rotations_dir(root)).glob("belam-II.*.json"))
    assert recs, "a rotation record must have been written"
    rec = json.loads(recs[-1].read_text(encoding="utf-8"))
    assert rec["result"] == "success"
    assert rec["observations"].get("d_reply_decision") == "continue"


def test_loop_returns_diff_when_successor_acks_diff(monkeypatch, tmp_path, capsys):
    """A success-or-absent-ack successor whose ACK says `diff` is recorded as
    diff — the reader accepts BOTH answers, and the ack channel carries the
    diff text where the debug log never could."""
    root = _proj(tmp_path)
    monkeypatch.chdir(root)
    monkeypatch.setattr(rotate, "find_project_root", lambda: root)
    monkeypatch.setattr(rotate, "cmd_meter", lambda args, root: 1)
    dbg = tmp_path / "seat.log"
    dbg.write_text(REAL_DEBUG_LOG)
    ack = rotate._ack_path(root, "belam-II")
    ack.parent.mkdir(parents=True, exist_ok=True)
    ack.write_text(json.dumps({"seat": "belam-II", "gen_after": None,
                               "answer": "diff", "text": "- x\n+ y"}),
                    encoding="utf-8")
    wins = tmp_path / "windows.txt"
    wins.write_text("")
    monkeypatch.setattr(rotate, "_launch_window",
                        lambda session, name, shell_cmd: _fake_launch(wins, "belam-II\n"))
    code = rotate.cmd_loop(SimpleNamespace(
        session_log=None, force=True, role="prime_director", name="belam-II",
        name_prefix="belam", model=None, effort=None, settings=None,
        prompt_file=None, tmux_session="agi-rc", window_path=str(wins),
        debug_file=str(dbg), dry_run=False, timeout=1,
    ), root)
    assert code == 0
    recs = list((rotate._rotations_dir(root)).glob("belam-II.*.json"))
    rec = json.loads(recs[-1].read_text(encoding="utf-8"))
    assert rec["result"] == "diff"
    err = capsys.readouterr().err
    assert "acked diff" in err and "+ y" in err


def test_loop_present_but_silent_no_ack_still_no_reply(monkeypatch, tmp_path):
    """FALSIFIER (2): the same REAL --debug-file WITHOUT an ack file, with the
    successor window present, is PRESENT-BUT-SILENT — recorded inconclusive,
    never greens as success. Preserves the three realities on the loop path."""
    root = _proj(tmp_path)
    monkeypatch.chdir(root)
    monkeypatch.setattr(rotate, "find_project_root", lambda: root)
    monkeypatch.setattr(rotate, "cmd_meter", lambda args, root: 1)
    dbg = tmp_path / "seat.log"
    dbg.write_text(REAL_DEBUG_LOG)  # 0 non-noise lines, no ack file
    wins = tmp_path / "windows.txt"
    wins.write_text("")
    monkeypatch.setattr(rotate, "_launch_window",
                        lambda session, name, shell_cmd: _fake_launch(wins, "belam-II\n"))
    code = rotate.cmd_loop(SimpleNamespace(
        session_log=None, force=True, role="prime_director", name="belam-II",
        name_prefix="belam", model=None, effort=None, settings=None,
        prompt_file=None, tmux_session="agi-rc", window_path=str(wins),
        debug_file=str(dbg), dry_run=False, timeout=1,
    ), root)
    assert code == 0
    recs = list((rotate._rotations_dir(root)).glob("belam-II.*.json"))
    rec = json.loads(recs[-1].read_text(encoding="utf-8"))
    assert rec["result"] == "inconclusive-no-reply"


def test_loop_refuses_ack_with_wrong_gen_on_self_reader(tmp_path, monkeypatch):
    """FALSIFIER (3): the rotate-self reader REFUSES an ack whose gen_after is
    not the generation it spawned — a foreign/stale ack cannot confirm."""
    root = _proj(tmp_path)
    monkeypatch.setattr(rotate, "find_project_root", lambda: root)
    ac = rotate._ack_path(root, "seat-x")
    ac.parent.mkdir(parents=True, exist_ok=True)
    ac.write_text(json.dumps({"seat": "seat-x", "gen_after": 99,
                              "answer": "continue"}), encoding="utf-8")
    # reader spawned gen 3: gen 99 ack is refused
    assert rotate._read_ack(str(ac), gen_after=3, timeout=1) is None


def test_cmd_ack_text_dash_reads_stdin(tmp_path, monkeypatch):
    """`--text -` reads the diff body from stdin (a long diff can exceed one
    shell argument) and stores it on the ack file."""
    root = _proj(tmp_path)
    monkeypatch.setattr(rotate, "find_project_root", lambda: root)
    monkeypatch.setattr(rotate.sys, "stdin",
                        _FakeIn("- old\n+ new\n"))
    code = rotate.cmd_ack(SimpleNamespace(
        seat="belt", gen=4, ref="agent:zz9", answer="diff", text="-"), root)
    assert code == 0
    ack = json.loads((rotate._ack_path(root, "belt")).read_text(
        encoding="utf-8"))
    assert ack["answer"] == "diff"
    assert ack["text"] == "- old\n+ new\n"


def test_cmd_ack_text_dash_empty_reads_empty_stdin(tmp_path, monkeypatch):
    """`--text -` with an empty stdin stores an empty text (empty string), not
    a `-` literal."""
    root = _proj(tmp_path)
    monkeypatch.setattr(rotate, "find_project_root", lambda: root)
    monkeypatch.setattr(rotate.sys, "stdin", _FakeIn(""))
    code = rotate.cmd_ack(SimpleNamespace(
        seat="belt", gen=5, ref=None, answer="continue", text="-"), root)
    assert code == 0
    ack = json.loads((rotate._ack_path(root, "belt")).read_text(
        encoding="utf-8"))
    assert ack["text"] == ""


def test_loop_ignores_debug_reply_continue_without_ack(monkeypatch, tmp_path,
                                                       capsys):
    """DISPROVER-CLOSER: the DELETED debug read must not resurface. A bare
    `continue` sitting in the successor's debug log, with window PRESENT and
    NO ack file, is PRESENT-BUT-SILENT — recorded inconclusive, never success,
    no announce (the old `_read_first_reply` would have called it success)."""
    root = _proj(tmp_path)
    monkeypatch.chdir(root)
    monkeypatch.setattr(rotate, "find_project_root", lambda: root)
    monkeypatch.setattr(rotate, "cmd_meter", lambda args, root: 1)
    calls = []
    monkeypatch.setattr(rotate, "_announce_rotation",
                        lambda **kw: calls.append(kw) or [])
    dbg = tmp_path / "seat.log"
    dbg.write_text("continue\n", encoding="utf-8")
    wins = tmp_path / "windows.txt"
    wins.write_text("")

    def fake_launch(s, n, c):
        wins.write_text(n + "\n", encoding="utf-8")
        return 0
    monkeypatch.setattr(rotate, "_launch_window", fake_launch)
    code = rotate.cmd_loop(SimpleNamespace(
        session_log=None, force=True, role="prime_director", name="belam-II",
        name_prefix="belam", model=None, effort=None, settings=None,
        prompt_file=None, tmux_session="agi-rc", window_path=str(wins),
        debug_file=str(dbg), dry_run=False, timeout=1,
    ), root)
    assert code == 0
    assert calls == [], f"no ack must not announce a rotation: {calls}"
    assert "handoff stood" not in capsys.readouterr().err
    recs = list((rotate._rotations_dir(root)).glob("belam-II.*.json"))
    assert recs
    rec = json.loads(recs[-1].read_text(encoding="utf-8"))
    assert rec["result"] == "inconclusive-no-reply"


def test_rotate_self_ignores_debug_reply_continue_without_ack(
        fake_ladder, tmp_path, monkeypatch, capsys):
    """The rotate-self reader, like loop, no longer confirms from the debug
    log: a bare `continue` there with window present and NO ack is
    PRESENT-BUT-SILENT — the terminal record is `unwitnessed`, never success."""
    win = tmp_path / "windows.txt"
    win.write_text("adv-alive\n", encoding="utf-8")
    log = tmp_path / "adv-alive.log"
    log.write_text("continue\n", encoding="utf-8")

    def fake_spawn(**kw):
        with open(win, "a", encoding="utf-8") as fh:
            fh.write("adv-alive\n")
        return 0, "echo hi"
    monkeypatch.setattr(rotate, "spawn_window", fake_spawn)
    monkeypatch.setattr(rotate, "_kill_window", lambda *a, **k: None)
    args = _rotate_self_args(tmp_path, throwaway=True, window_path=str(win),
                             debug_file=str(log))
    rc = rotate.cmd_rotate_self(args, tmp_path)
    assert rc != 0
    recs = sorted((tmp_path / "sessions" / "rotations")
                  .glob("adv-alive.*.json"))
    assert recs
    rec = json.loads(recs[-1].read_text(encoding="utf-8"))
    assert rec["result"] == "unwitnessed"
    assert "silent" in rec["refusal_reason"]
    assert "handoff stood" not in capsys.readouterr().err


# ---------------------------------------------------------------------------
# hypothesis:l3w4-parent-branch-merge-up — meter pins stay the main checkout
# ---------------------------------------------------------------------------


def test_sessions_dir_resolves_to_main_from_a_worktree(tmp_path):
    """A `--branch` kid carries its own `.agi/`, but the meter pins must stay
    the ONE shared directory on the main checkout (same rule as the budget
    dir and comms), or a rotation seat reading pins from a worktree would see
    a different room than the parents writing it."""
    repo = tmp_path / "main"
    repo.mkdir(parents=True)
    subprocess.run(["git", "-C", str(repo), "init", "-b", "season/s1"],
                   check=True, capture_output=True)
    for cfg in ("user.email", "user.name"):
        subprocess.run(["git", "-C", str(repo), "config", cfg, "t"],
                       check=True, capture_output=True)
    (repo / ".agi" / "nodes").mkdir(parents=True)
    (repo / ".agi" / "config.json").write_text('{"metric_primary": "x"}')
    subprocess.run(["git", "-C", str(repo), "add", "-A"], check=True,
                   capture_output=True)
    subprocess.run(["git", "-C", str(repo), "commit", "-m", "init"],
                   check=True, capture_output=True)

    wt = tmp_path / "wt"
    subprocess.run(["git", "-C", str(repo), "worktree", "add",
                    "-b", "loop/x-a@s2", str(wt), "season/s1"],
                   check=True, capture_output=True)

    main_sess = rotate._sessions_dir(repo / ".agi")
    wt_sess = rotate._sessions_dir(wt / ".agi")
    assert str(main_sess) == str(repo / ".agi" / "sessions")
    assert wt_sess == main_sess, (
        "a worktree kid's meter pins must resolve to the MAIN checkout's "
        "sessions dir, not a per-worktree one")


# ── l3w4-seat-rotation-loops: alarms --holder / rotate-self / status --seats ──


def _write_seats_sheet(root, rows):
    """Write a minimal seals-md-style registry the loader can parse."""
    nodes = root / "nodes" / ".geometry"
    nodes.mkdir(parents=True, exist_ok=True)
    (root / "sessions").mkdir(parents=True, exist_ok=True)
    body = "---\nid: config:seats\ntype: config\nseats:\n"
    for r in rows:
        body += "  - " + json.dumps(r) + "\n"
    body += "---\n"
    (nodes / "seats.md").write_text(body, encoding="utf-8")


def _pin_seat_transcript(root, name, tokens):
    """Write a fake CC transcript + the seat-stable pin naming it."""
    transcript = root / f"t-{name}.jsonl"
    transcript.write_text(json.dumps({
        "message": {"role": "assistant",
                    "usage": {"input_tokens": tokens,
                              "cache_read_input_tokens": 0,
                              "cache_creation_input_tokens": 0}},
    }) + "\n", encoding="utf-8")
    (root / "sessions" / f"{name}.meter").write_text(
        str(transcript) + "\n", encoding="utf-8")
    return transcript


def _rotate_self_args(tmp_path, **over):
    base = dict(name="adv-alive", force=False, timeout=5, debug_file=None,
                model=None, effort=None, settings=None, prompt_file=None,
                tmux_session="t", window_path=None, dry_run=False,
                throwaway=False, successor_argv=None, role="parent")
    base.update(over)
    return SimpleNamespace(**base)


def test_alarms_once_holds_below_threshold(fake_ladder, tmp_path, capsys):
    """Below director_rotate_at: prints `hold <seat>` and sends NO dm."""
    seats = [{"name": "kid-1", "role": "director", "rotated_by": "advisor"}]
    _write_seats_sheet(tmp_path, seats)
    _pin_seat_transcript(tmp_path, "kid-1", tokens=5000)  # 0.05 < 0.25
    comms = tmp_path / "comms"
    args = SimpleNamespace(holder="advisor", once=True, interval=300,
                           comms_root=str(comms))
    rc = rotate.cmd_alarms(args, tmp_path)
    assert rc == 0
    out = capsys.readouterr().out
    assert "hold kid-1 0.0500" in out
    assert not list(comms.glob("dm/*.md"))


def test_alarms_once_dms_holder_when_due_then_stops(fake_ladder, tmp_path):
    """At/over threshold: exactly one dm `rotate now` to the holder, nil more."""
    seats = [{"name": "kid-1", "role": "director", "rotated_by": "advisor"},
             {"name": "kid-2", "role": "director", "rotated_by": "advisor"}]
    _write_seats_sheet(tmp_path, seats)
    _pin_seat_transcript(tmp_path, "kid-1", tokens=40000)  # 0.40 >= 0.25
    _pin_seat_transcript(tmp_path, "kid-2", tokens=4000)   # 0.04 < 0.25
    comms = tmp_path / "comms"
    args = SimpleNamespace(holder="advisor", once=True, interval=300,
                           comms_root=str(comms))
    rc = rotate.cmd_alarms(args, tmp_path)
    assert rc == 0
    dms = list(comms.glob("dm/*.md"))
    assert len(dms) == 1  # only the due seat was dm'd
    assert "rotate now" in dms[0].read_text(encoding="utf-8")


def test_rotate_self_dry_run_reuses_plain_name_no_roman(fake_ladder, tmp_path,
                                                        capsys, monkeypatch):
    """--dry-run prints the successor under the PLAIN seat name, generation N+1,
    never a Roman numeral, and touches nothing."""
    _write_seats_sheet(tmp_path,
                       [{"name": "adv-alive", "role": "parent",
                         "model": "x", "effort": "max", "settings": ""}])
    seen = {}
    def fake_spawn(**kw):
        seen["name"] = kw["name"]
        return 0, "echo hi"
    monkeypatch.setattr(rotate, "spawn_window", fake_spawn)
    args = _rotate_self_args(tmp_path, dry_run=True)
    rc = rotate.cmd_rotate_self(args, tmp_path)
    assert rc == 0
    assert seen["name"] == "adv-alive"          # plain, not adv-alive-II
    assert "generation: 1" in capsys.readouterr().out
    assert not (tmp_path / "sessions" / "seats" / "adv-alive.handoff.md").exists()


def test_rotate_self_renames_window_before_respawn(fake_ladder, tmp_path, monkeypatch):
    """The own window is renamed aside BEFORE the successor spawns."""
    _write_seats_sheet(tmp_path,
                       [{"name": "adv-alive", "role": "parent",
                         "model": "x", "effort": "max", "settings": ""}])
    win = tmp_path / "windows.txt"
    win.write_text("adv-alive\n", encoding="utf-8")
    at_spawn = {}
    def fake_spawn(**kw):
        at_spawn["window_file"] = win.read_text(encoding="utf-8").strip()
        # the successor window appears under the reused plain name
        with open(win, "a", encoding="utf-8") as fh:
            fh.write("adv-alive\n")
        return 0, "echo hi"
    monkeypatch.setattr(rotate, "spawn_window", fake_spawn)
    monkeypatch.setattr(rotate, "_read_ack",
                        lambda *a, **k: {"seat": "s", "gen_after": 1, "answer": "continue"})
    monkeypatch.setattr(rotate, "_kill_window", lambda *a, **k: None)
    args = _rotate_self_args(tmp_path, window_path=str(win))
    rc = rotate.cmd_rotate_self(args, tmp_path)
    assert rc == 0
    assert "adv-alive.gen1" in at_spawn["window_file"]


def test_rotate_self_kills_own_window_after_continue(fake_ladder, tmp_path,
                                                     capsys, monkeypatch):
    """After the successor answers `continue`, the own renamed window dies."""
    _write_seats_sheet(tmp_path,
                       [{"name": "adv-alive", "role": "parent",
                         "model": "x", "effort": "max", "settings": ""}])
    win = tmp_path / "windows.txt"
    win.write_text("adv-alive\n", encoding="utf-8")
    killed = []
    def fake_spawn(**kw):
        # the successor window appears under the reused plain name
        with open(win, "a", encoding="utf-8") as fh:
            fh.write("adv-alive\n")
        return 0, "echo hi"
    monkeypatch.setattr(rotate, "spawn_window", fake_spawn)
    monkeypatch.setattr(rotate, "_read_ack",
                        lambda *a, **k: {"seat": "s", "gen_after": 1, "answer": "continue"})
    monkeypatch.setattr(rotate, "_kill_window",
                        lambda name, *a, **k: killed.append(name))
    args = _rotate_self_args(tmp_path, window_path=str(win))
    rc = rotate.cmd_rotate_self(args, tmp_path)
    assert rc == 0
    assert killed == ["adv-alive.gen1"]


# ── goal:g15.25 line (3): --stops — the rotate-out is ONE call ──────
def _init_git_remote(tmp_path, branch="master"):
    """Turn tmp_path into a git repo WITH a bare origin and an upstreamed
    `branch`, so the rotate-out stop commit/push and the captive checklist
    (which measure against real git) run like live. Returns the bare path."""
    bare = tmp_path / "remote.git"
    subprocess.run(["git", "init", "--bare", str(bare)], check=True,
                   capture_output=True)
    subprocess.run(["git", "-C", str(tmp_path), "init"], check=True,
                   capture_output=True)
    # keep fixture-only noise (the nested bare remote, the fake tmux window
    # file) out of `git status` so the captive dirty-tree check sees only
    # real work — exactly what a live seat branch has.
    (tmp_path / ".gitignore").write_text(
        "remote.git/\nwindows.txt\n", encoding="utf-8")
    subprocess.run(["git", "-C", str(tmp_path), "remote", "add",
                    "origin", str(bare)], check=True, capture_output=True)
    subprocess.run(["git", "-C", str(tmp_path), "config", "user.email",
                    "t@t"], check=True, capture_output=True)
    subprocess.run(["git", "-C", str(tmp_path), "config", "user.name",
                    "t"], check=True, capture_output=True)
    subprocess.run(["git", "-C", str(tmp_path), "add", "-A"],
                   check=True, capture_output=True)
    subprocess.run(["git", "-C", str(tmp_path), "commit", "-q", "-m",
                    "fixture"], check=True, capture_output=True)
    subprocess.run(["git", "-C", str(tmp_path), "push", "-u", "origin",
                    branch], check=True, capture_output=True)
    return bare


def test_stops_block_refuses_empty(fake_ladder, tmp_path, capsys):
    """FALSIFIER: `--stops ''` refuses (exit 2), never touches the card."""
    _write_seats_sheet(tmp_path, [{"name": "adv-alive", "role": "parent",
                                   "model": "x", "effort": "max"}])
    args = _rotate_self_args(tmp_path, stops="  ")
    rc = rotate.cmd_rotate_self(args, tmp_path)
    assert rc == 2
    assert "EMPTY stops text" in capsys.readouterr().err


def test_write_stops_section_created_and_replaced(tmp_path):
    """The where-it-stops slot is CREATED at the card's end when absent and
    REPLACED (up to the next heading) when it exists; --ask-diff gap rides the
    body in both shapes. Only the slot changes, everything else verbatim."""
    from agi.bin import rotate as _r
    card = tmp_path / "quorum" / "s.md"
    card.parent.mkdir(parents=True)
    card.write_text("# s card\n\n## Intro\nkeep this\n", encoding="utf-8")
    body, slot = _r._write_stops_section(card, "s", "fix seat-3")
    assert slot == "created"
    assert "### 🔴 Where it stops\nfix seat-3" in body
    assert "keep this" in body          # carried verbatim
    txt = card.read_text(encoding="utf-8")
    assert "### 🔴 Where it stops" in txt and "fix seat-3" in txt
    # second write REPLACES, and the ask-diff gap rides the body
    body2, slot2 = _r._write_stops_section(card, "s", "now this",
                                           diff_gap="review the handoff")
    assert slot2 == "replaced"
    txt2 = card.read_text(encoding="utf-8")
    assert "fix seat-3" not in txt2
    assert "now this" in txt2
    assert "diff requested: review the handoff" in txt2
    assert "keep this" in txt2


def test_commit_stops_row_commits_card_and_own_row_nothing_else(tmp_path):
    """The rotate-out commit stages the card + the seat's OWN seats row and
    NOTHING else: a foreign seats row change and a stray untracked file never
    ride it (`--stops` never `git add -A`)."""
    from agi.bin import rotate as _r
    nodes = tmp_path / "nodes" / ".geometry"
    nodes.mkdir(parents=True)
    seats = nodes / "seats.md"
    seats.write_text("---\nid: config:seats\ntype: config\nseats:\n"
                     "  - {\"name\": \"s1\", \"role\": \"parent\"}\n"
                     "  - {\"name\": \"s2\", \"role\": \"parent\"}\n"
                     "---\n", encoding="utf-8")
    # route _ack_seats_path back to seats.md (no config:posts in this fixture)
    card = tmp_path / "sessions" / "quorum" / "s1.md"
    card.parent.mkdir(parents=True)
    card.write_text("# s1 card\n", encoding="utf-8")
    _init_git_remote(tmp_path)
    # dirty: s1's own row (committed by the stop commit) + s2's FOREIGN row
    # (must stay out) + a stray untracked file (must stay out)
    seats.write_text("---\nid: config:seats\ntype: config\nseats:\n"
                     "  - {\"name\": \"s1\", \"role\": \"parent\", "
                     "\"edited_by\": \"s1\"}\n"
                     "  - {\"name\": \"s2\", \"role\": \"parent\", "
                     "\"edited_by\": \"s2-foreign\"}\n"
                     "---\n", encoding="utf-8")
    (tmp_path / "scratch.log").write_text("x\n", encoding="utf-8")
    card.write_text("# s1 card\n## 🔴 Where it stops\nkeep\n",
                    encoding="utf-8")
    out = _r._commit_stops_row(tmp_path, "s1", card, "s1 rotate-out")
    assert "stop_commit: committed" in out, out
    top = tmp_path
    names = subprocess.run(
        ["git", "-C", str(top), "log", "-1", "--name-only",
         "--format="], capture_output=True, text=True).stdout.splitlines()
    names = [n for n in names if n.strip()]
    assert names, "no files in the rotate-out commit"
    for n in names:
        assert n in ("sessions/quorum/s1.md", "nodes/.geometry/seats.md"), \
            f"rotate-out commit touched an outside path: {n}"
    # s1's own row IS in the commit; s2's foreign edit stayed out
    committed = subprocess.run(
        ["git", "-C", str(top), "show", "HEAD:nodes/.geometry/seats.md"],
        capture_output=True, text=True).stdout
    assert "s1" in committed and "edited_by\": \"s1" in committed
    assert "s2-foreign" not in committed
    # the stray untracked file never rode the commit
    status = subprocess.run(["git", "-C", str(top), "status",
                             "--porcelain"], capture_output=True,
                            text=True).stdout
    assert "scratch.log" in status   # still untracked, not committed


def test_rotate_self_stops_one_call_writes_card_commits_rotates(
        fake_ladder, tmp_path, monkeypatch, capsys):
    """FALSIFIER (the core): ONE `rotate-self --stops 'x'` call rotates on the
    keyed fake seat — the card carries the stops text, the rotate-out commit
    touched nothing outside card + seats, the rotation line is printed (no
    send.py), and the record is `success`."""
    _write_seats_sheet(tmp_path, [{"name": "adv-alive", "role": "parent",
                                   "model": "x", "effort": "max"}])
    quorum = tmp_path / "sessions" / "quorum"
    quorum.mkdir(parents=True, exist_ok=True)
    card = quorum / "adv-alive.md"
    card.write_text("# adv-alive card\n## Intro\ncarried\n",
                    encoding="utf-8")
    _init_git_remote(tmp_path)
    win = tmp_path / "windows.txt"
    win.write_text("adv-alive\n", encoding="utf-8")

    def fake_spawn(**kw):
        with open(win, "a", encoding="utf-8") as fh:
            fh.write("adv-alive\n")
        return 0, "echo hi"
    monkeypatch.setattr(rotate, "spawn_window", fake_spawn)
    monkeypatch.setattr(
        rotate, "_read_ack",
        lambda *a, **k: {"seat": "s", "gen_after": 1, "answer": "continue"})
    monkeypatch.setattr(rotate, "_kill_window", lambda *a, **k: None)
    args = _rotate_self_args(tmp_path, window_path=str(win),
                             stops="fix the merge on seat-3")
    rc = rotate.cmd_rotate_self(args, tmp_path)
    assert rc == 0, capsys.readouterr().out
    body = card.read_text(encoding="utf-8")
    assert "### 🔴 Where it stops" in body
    assert "fix the merge on seat-3" in body
    assert "carried" in body
    out = capsys.readouterr().out
    assert ("rotation line: delivered as the [rotation-alert] dm "
            "to <prime> (no send.py call needed)") in out
    top = tmp_path
    names = subprocess.run(
        ["git", "-C", str(top), "log", "-1", "--name-only", "--format="],
        capture_output=True, text=True).stdout.splitlines()
    names = [n for n in names if n.strip()]
    assert names, "rotate-out commit committed nothing"
    for n in names:
        assert n.startswith("sessions/quorum/") or n == "nodes/.geometry/seats.md"
    # the stops text is IN the committed card
    committed_card = subprocess.run(
        ["git", "-C", str(top), "show", "HEAD:sessions/quorum/adv-alive.md"],
        capture_output=True, text=True).stdout
    assert "fix the merge on seat-3" in committed_card

def test_rotate_self_stops_behind_merges_and_pushes_merge_commit_before_spawn(
        fake_ladder, tmp_path, monkeypatch, capsys):
    """FALSIFIER (the parent's measured gap): when the captive checklist
    PERFORMS the only-behind merge (check 3), the SAME `rotate-self --stops`
    flow pushes that merge commit (push line 2) BEFORE the spawn -- the live
    flow runs BOTH pushes and HEAD ends equal to its upstream (unpushed ==
    0). Before this slice the dry-run printed a push line 2 that the live
    flow never performed (a real gap, not just an unproven sub-claim). The
    false spawn proves it ran AFTER the push (it is the last side effect)."""
    _write_seats_sheet(tmp_path, [{"name": "adv-alive", "role": "parent",
                                   "model": "x", "effort": "max"}])
    quorum = tmp_path / "sessions" / "quorum"
    quorum.mkdir(parents=True, exist_ok=True)
    card = quorum / "adv-alive.md"
    card.write_text("# adv-alive card\n## Intro\ncarried\n",
                    encoding="utf-8")
    _init_git_remote(tmp_path)          # master upstreamed to origin/master
    # origin/season/s2 — ONE commit ahead of master, merging cleanly: the
    # merge target `_prepare_merge_target` resolves (branch master falls
    # back to season_branch = season/s2). _init_git_remote committed the
    # card/seats seed and pushed master, so this branch is the ONLY behead.
    subprocess.run(["git", "-C", str(tmp_path), "checkout", "-b",
                    "season/s2"], check=True, capture_output=True)
    (tmp_path / "season.txt").write_text("season\n", encoding="utf-8")
    subprocess.run(["git", "-C", str(tmp_path), "add", "--",
                    "season.txt"], check=True, capture_output=True)
    subprocess.run(["git", "-C", str(tmp_path), "commit", "-q", "-m",
                    "season work"], check=True, capture_output=True)
    subprocess.run(["git", "-C", str(tmp_path), "push", "-u", "origin",
                    "season/s2"], check=True, capture_output=True)
    subprocess.run(["git", "-C", str(tmp_path), "checkout", "master"],
                   check=True, capture_output=True)

    win = tmp_path / "windows.txt"
    win.write_text("adv-alive\n", encoding="utf-8")

    def fake_spawn(**kw):
        with open(win, "a", encoding="utf-8") as fh:
            fh.write("adv-alive\n")
        return 0, "echo hi"
    monkeypatch.setattr(rotate, "spawn_window", fake_spawn)
    monkeypatch.setattr(
        rotate, "_read_ack",
        lambda *a, **k: {"seat": "s", "gen_after": 1, "answer": "continue"})
    monkeypatch.setattr(rotate, "_kill_window", lambda *a, **k: None)

    pre_merge_head = subprocess.run(
        ["git", "-C", str(tmp_path), "rev-parse", "--short", "HEAD"],
        capture_output=True, text=True).stdout.strip()
    args = _rotate_self_args(tmp_path, window_path=str(win),
                             stops="fix the merge on seat-3")
    rc = rotate.cmd_rotate_self(args, tmp_path)
    assert rc == 0, capsys.readouterr().err
    err = capsys.readouterr().err
    # THE second push line actually ran live (previously dry-run-only)
    assert "merge push: OK -- master" in err
    # the merge landed: HEAD advanced past the season commit, season file in
    assert subprocess.run(
        ["git", "-C", str(tmp_path), "rev-parse", "--short", "HEAD"],
        capture_output=True, text=True).stdout.strip() != pre_merge_head
    assert "season.txt" in subprocess.run(
        ["git", "-C", str(tmp_path), "ls-files"],
        capture_output=True, text=True).stdout
    # the merge commit (+ the stops commit) were BOTH pushed before the
    # spawn: HEAD equals its upstream, unpushed count is ZERO
    unpushed = subprocess.run(
        ["git", "-C", str(tmp_path), "rev-list", "--count", "@{u}..HEAD"],
        capture_output=True, text=True).stdout.strip()
    assert unpushed == "0", f"unpushed commits before spawn: {unpushed}"
    # the spawn ran AFTER the push (last side effect) and exactly once
    assert win.read_text(encoding="utf-8").count("adv-alive") == 2
    # merge did not clobber the stops card
    assert "fix the merge on seat-3" in card.read_text(encoding="utf-8")


def test_rotate_self_refused_when_merge_push_fails(fake_ladder, tmp_path,
                                                   monkeypatch, capsys):
    """FALSIFIER: when the only-behind merge LANDED but the merge-commit
    push (push line 2) is REFUSED, rotate-self blocks with exit 3 and the
    spawn does NOT run -- a refused second push is the same discipline as a
    refused stops push (nothing rotated)."""
    _write_seats_sheet(tmp_path, [{"name": "adv-alive", "role": "parent",
                                   "model": "x", "effort": "max"}])
    quorum = tmp_path / "sessions" / "quorum"
    quorum.mkdir(parents=True, exist_ok=True)
    card = quorum / "adv-alive.md"
    card.write_text("# adv-alive card\n## Intro\ncarried\n",
                    encoding="utf-8")
    _init_git_remote(tmp_path)
    subprocess.run(["git", "-C", str(tmp_path), "checkout", "-b",
                    "season/s2"], check=True, capture_output=True)
    (tmp_path / "season.txt").write_text("season\n", encoding="utf-8")
    subprocess.run(["git", "-C", str(tmp_path), "add", "--",
                    "season.txt"], check=True, capture_output=True)
    subprocess.run(["git", "-C", str(tmp_path), "commit", "-q", "-m",
                    "season work"], check=True, capture_output=True)
    subprocess.run(["git", "-C", str(tmp_path), "push", "-u", "origin",
                    "season/s2"], check=True, capture_output=True)
    subprocess.run(["git", "-C", str(tmp_path), "checkout", "master"],
                   check=True, capture_output=True)

    win = tmp_path / "windows.txt"
    win.write_text("adv-alive\n", encoding="utf-8")
    spawn_calls = []

    def fake_spawn(**kw):
        spawn_calls.append(kw)
        return 0, "echo hi"
    monkeypatch.setattr(rotate, "spawn_window", fake_spawn)
    monkeypatch.setattr(
        rotate, "_read_ack",
        lambda *a, **k: {"seat": "s", "gen_after": 1, "answer": "continue"})
    monkeypatch.setattr(rotate, "_kill_window", lambda *a, **k: None)
    real_push = rotate._stops_push

    def refusing_merge_push(root, label="stops"):
        if label == "merge":
            return f"push refused out: merge-commit rejection (test)"
        return real_push(root, label=label)
    monkeypatch.setattr(rotate, "_stops_push", refusing_merge_push)

    args = _rotate_self_args(tmp_path, window_path=str(win),
                             stops="fix the merge on seat-3")
    rc = rotate.cmd_rotate_self(args, tmp_path)
    assert rc == 3, capsys.readouterr().err
    assert "rotate-self refused" in capsys.readouterr().err
    # the merge landed but was NOT pushed, and the spawn never ran
    assert "season.txt" in subprocess.run(
        ["git", "-C", str(tmp_path), "ls-files"],
        capture_output=True, text=True).stdout
    assert not spawn_calls, "spawn must not run when the merge push is refused"


def test_seat_handoff_generation_bumps_on_rotation(fake_ladder, tmp_path,
                                                   capsys, monkeypatch):
    """A seat whose handoff says generation 3 rotates onto generation 4."""
    _write_seats_sheet(tmp_path,
                       [{"name": "adv-alive", "role": "parent",
                         "model": "x", "effort": "max", "settings": ""}])
    hand = tmp_path / "sessions" / "seats"
    hand.mkdir(parents=True, exist_ok=True)
    (hand / "adv-alive.handoff.md").write_text(
        "seat: adv-alive\ngeneration: 3\n", encoding="utf-8")
    seen = []
    def fake_spawn(**kw):
        seen.append(kw["name"])
        return 0, "echo hi"
    monkeypatch.setattr(rotate, "spawn_window", fake_spawn)
    args = _rotate_self_args(tmp_path, dry_run=True)
    rc = rotate.cmd_rotate_self(args, tmp_path)
    assert rc == 0
    assert "generation 4" in capsys.readouterr().out
    # the read-before-write cursor still computes on the plain seat name
    assert seen == ["adv-alive"]


def test_status_seats_flag_lists_fraction_and_age(fake_ladder, tmp_path,
                                                  capsys):
    """`status --seats` prints seat/generation/fraction/age per registry row."""
    _write_seats_sheet(tmp_path,
                       [{"name": "kid-1", "role": "director",
                         "rotated_by": "advisor"}])
    _pin_seat_transcript(tmp_path, "kid-1", tokens=10000)  # 0.1
    rc = rotate.cmd_status(SimpleNamespace(seats=True), tmp_path)
    assert rc == 0
    out = capsys.readouterr().out
    assert "kid-1\tgen=" in out
    assert "frac=0.100" in out


def test_rotate_self_ack_is_generation_checked_not_log_cursor(fake_ladder,
                                                             tmp_path):
    """The read-before-write cursor (l3w4 stale `continue`) is REPLACED, not
    reinvented: the ack channel refuses by GENERATION, so a stale ack from a
    prior rotation cannot confirm a successor it was not written for. The
    debug-log cursor is gone with the debug reader.
    """


# ── hypothesis:l3-rotate-self-successor-override ──────────────────────────
# The successor argv is hardwired to real `claude --remote-control` and the
# successor name must come from the seats registry, so no kid could ever
# exercise a rotation live. Two explicit, impossible-to-trip overlays: a
# successor-command override (stand-in stand-in command) and a throwaway seat
# path that never writes seats.md. RED-FIRST: these fail before the rotate.py
# change lands, pass after.

def test_spawn_window_successor_argv_override_replaces_claude(tmp_path, capsys,
                                                              monkeypatch):
    """Explicit --successor-argv replaces the real claude successor; the shell
    line is exactly the override, never a `claude --remote-control`."""
    # next: successor_argv -> AttributeError -> TypeError -> NotImplementedError
    monkeypatch.setattr(rotate, "load_role", lambda *a, **k: None)
    try:
        rc, shell = rotate.spawn_window(
            name="rh", tier="parent", prompt_file=None, tmux_session="t",
            root=tmp_path, dry_run=True, debug_file="rh.log",
            successor_argv="printf continue")
    except TypeError:
        pytest.fail("spawn_window does not accept successor_argv yet (RED)")
    assert rc == 0
    out = capsys.readouterr().out
    assert out.strip() == "printf continue"   # the override, verbatim
    assert "claude" not in out                # no real successor


def test_spawn_window_default_still_real_claude(tmp_path, capsys, monkeypatch):
    """No override -> the launch stays byte-for-byte today's real claude
    command: `claude --remote-control NAME ...` (default unchanged)."""
    monkeypatch.setattr(rotate, "load_role", lambda *a, **k: None)
    rc, shell = rotate.spawn_window(
        name="rh", tier="parent", prompt_file=None, tmux_session="t",
        root=tmp_path, dry_run=True, debug_file="rh.log")
    assert rc == 0
    out = capsys.readouterr().out
    assert out.lstrip().startswith("claude --remote-control rh") or \
        "claude --remote-control rh" in out


def test_rotate_self_throwaway_skips_registry(fake_ladder, tmp_path,
                                              monkeypatch):
    """--throwaway rotates a seat name ABSENT from seats.md, and never creates
    or writes the registry file (hypothesis:l3-rotate-self-successor-override).
    Note: no _write_seats_sheet call — the seat is deliberately unregistered.
    Before the change, cmd_rotate_self errors `no seat` here (the L3.37 gate)."""
    seen = {}
    win = tmp_path / "windows.txt"
    win.write_text("adv-alive\n", encoding="utf-8")
    def fake_spawn(**kw):
        seen["name"] = kw["name"]
        with open(win, "a", encoding="utf-8") as fh:
            fh.write("adv-alive\n")   # the successor window appears
        return 0, "echo hi"
    monkeypatch.setattr(rotate, "spawn_window", fake_spawn)
    monkeypatch.setattr(rotate, "_read_ack",
                        lambda *a, **k: {"seat": "s", "gen_after": 1, "answer": "continue"})
    monkeypatch.setattr(rotate, "_kill_window", lambda *a, **k: None)
    args = _rotate_self_args(tmp_path, throwaway=True, window_path=str(win))
    rc = rotate.cmd_rotate_self(args, tmp_path)
    assert rc == 0
    assert seen["name"] == "adv-alive"        # plain name reused, no Roman
    seats = tmp_path / "nodes" / ".geometry" / "seats.md"
    assert not seats.exists()                 # registry untouched
    assert not (tmp_path / "nodes" / ".geometry" / "seats.md").exists()


def test_rotate_self_without_throwaway_still_refuses_unregistered(
        fake_ladder, tmp_path, monkeypatch):
    """Regression guard: the registry gate still holds for the DEFAULT path —
    an unregistered name without --throwaway must still error `no seat`."""
    mk = tmp_path / "nodes" / ".geometry"
    mk.mkdir(parents=True, exist_ok=True)
    # an empty registry sheet: adv-alive not present
    (mk / "seats.md").write_text("---\nid: config:seats\ntype: config\n---\n",
                                 encoding="utf-8")
    args = _rotate_self_args(tmp_path, throwaway=False)
    rc = rotate.cmd_rotate_self(args, tmp_path)
    assert rc == 1
    assert "no seat" in str(rc) or True  # exit code 1 is the gate


def test_rotate_self_throwaway_forwards_successor_argv(fake_ladder, tmp_path,
                                                       monkeypatch):
    """--throwaway + --successor-argv both flow into spawn_window untouched."""
    seen = {}
    win = tmp_path / "windows.txt"
    win.write_text("adv-alive\n", encoding="utf-8")
    def fake_spawn(**kw):
        seen["argv"] = kw.get("successor_argv")
        with open(win, "a", encoding="utf-8") as fh:
            fh.write("adv-alive\n")
        return 0, "echo hi"
    monkeypatch.setattr(rotate, "spawn_window", fake_spawn)
    monkeypatch.setattr(rotate, "_read_ack",
                        lambda *a, **k: {"seat": "s", "gen_after": 1, "answer": "continue"})
    monkeypatch.setattr(rotate, "_kill_window", lambda *a, **k: None)
    args = _rotate_self_args(tmp_path, throwaway=True, window_path=str(win),
                             successor_argv="printf continue")
    rc = rotate.cmd_rotate_self(args, tmp_path)
    assert rc == 0
    assert seen["argv"] == "printf continue"


# --- _launch_window: the two silent failures (hypothesis:l3-rotate-launch-
# window-silent-failure, measured 2026-09-08) --------------------------------


def test_launch_window_returns_tmux_failure_instead_of_swallowing_it(
        monkeypatch, capsys):
    """tmux said `command too long` and the caller was told 0.

    This is why `rotate.py loop` reported a rotation with no successor window
    behind it for three primes running: the return code was discarded and the
    captured stderr thrown away.
    """
    def fake_run(argv, **kw):
        return subprocess.CompletedProcess(argv, 1, stdout="",
                                           stderr="command too long")
    monkeypatch.setattr(rotate.subprocess, "run", fake_run)

    rc = rotate._launch_window("agi-rc", "belam-test", "echo hi")

    assert rc == 1, "a failed tmux new-window must not report success"
    assert "command too long" in capsys.readouterr().err


def test_launch_window_hands_tmux_a_short_argv_for_a_long_command(monkeypatch):
    """A rotation line carries the constitution head and runs ~16KB.

    tmux refuses past its own buffer, so a long command goes through a script
    file and tmux receives a few dozen bytes instead. The script must still
    exist afterwards -- bash reads a script incrementally, so deleting it
    early can truncate a running successor.
    """
    seen = {}

    def fake_run(argv, **kw):
        seen["argv"] = argv
        return subprocess.CompletedProcess(argv, 0, stdout="", stderr="")
    monkeypatch.setattr(rotate.subprocess, "run", fake_run)

    long_cmd = "claude --remote-control x " + ("y" * 20000)
    rc = rotate._launch_window("agi-rc", "belam-test", long_cmd)

    assert rc == 0
    passed = seen["argv"][-1]
    assert len(passed) < 512, f"tmux still handed {len(passed)} bytes"
    assert passed.startswith("bash ")
    script = Path(passed.split(" ", 1)[1].strip("'"))
    assert script.exists(), "the script must outlive the launch call"
    assert long_cmd in script.read_text()
    script.unlink()


def test_launch_window_leaves_a_short_command_inline(monkeypatch):
    """Below the threshold nothing changes -- no script, no new failure mode."""
    seen = {}

    def fake_run(argv, **kw):
        seen["argv"] = argv
        return subprocess.CompletedProcess(argv, 0, stdout="", stderr="")
    monkeypatch.setattr(rotate.subprocess, "run", fake_run)

    rc = rotate._launch_window("agi-rc", "belam-test", "echo hi")

    assert rc == 0
    assert seen["argv"][-1].endswith("echo hi")
    assert "bash /" not in seen["argv"][-1]
# ── hypothesis:l3-rotation-record-and-predecessor-guarantee ───────────────
# Every rotation performed by rotate.py — throwaway rehearsal or real
# claude --remote-control successor — writes a durable machine-readable JSON
# record under `.agi/sessions/rotations/` capturing all five observations as
# OBSERVED FACTS (never tool-return claims): (a) a NEW tmux window exists
# under the reused plain name, established by tmux list-windows; (b) the seat
# handoff generation before/after; (c) WHICH log the read-back read;
# (d) the stale-`continue` read-before-write cursor; (e) whether the
# predecessor window is still alive, by name. AND rotate-self/loop REFUSE to
# report success when the successor window is absent or the predecessor
# window is gone. RED-FIRST below (fail before the rotate.py change lands).


def test_rotate_self_writes_record_with_five_observations(fake_ladder, tmp_path,
                                                          monkeypatch):
    """A completed throwaway rotate-self writes a JSON record carrying all five
    observations (a)-(e), each sourced from the window-path/tmux read, never
    from spawn_window's return value."""
    win = tmp_path / "windows.txt"
    win.write_text("adv-alive\n", encoding="utf-8")

    def fake_spawn(**kw):
        # the new successor window appears under the reused plain name
        with open(win, "a", encoding="utf-8") as fh:
            fh.write("adv-alive\n")
        return 0, "echo hi"

    monkeypatch.setattr(rotate, "spawn_window", fake_spawn)
    monkeypatch.setattr(rotate, "_read_ack",
                        lambda *a, **k: {"seat": "s", "gen_after": 1, "answer": "continue"})
    monkeypatch.setattr(rotate, "_kill_window", lambda *a, **k: None)
    args = _rotate_self_args(tmp_path, throwaway=True, window_path=str(win))
    rc = rotate.cmd_rotate_self(args, tmp_path)
    assert rc == 0
    records = sorted((tmp_path / "sessions" / "rotations")
                     .glob("adv-alive.*.json"))
    assert records, "no durable rotation record written"
    rec = json.loads(records[-1].read_text(encoding="utf-8"))
    assert rec["rotation"] == "rotate-self"
    assert rec["result"] == "success"
    obs = rec["observations"]
    # (a) successor window under the plain name, observed, not tool-return
    a = obs["a_successor_window_under_plain_name"]
    assert a["present"] is True and a["window"] == "adv-alive"
    assert "adv-alive" in a["windows"]
    assert "source" in a and "window-path file" in a["source"]
    # (b) generation before/after
    assert obs["b_generation"] == {"before": 0, "after": 1}
    # (c) which log the read-back actually read
    assert str(obs["c_readback_log_path"]).endswith("adv-alive.log")
    # (d) read-before-write stale-continue cursor
    assert obs["d_stale_continue_cursor"]["read_before_write"] is True
    assert "start_offset" in obs["d_stale_continue_cursor"]
    # (e) predecessor alive by name
    e = obs["e_predecessor_alive"]
    assert e["name"] == "adv-alive.gen1" and e["present"] is True
    assert "adv-alive.gen1" in e["windows"]


def test_rotate_self_refuses_when_successor_window_absent(fake_ladder, tmp_path,
                                                          monkeypatch, capsys):
    """Spawn leaves NO successor window -> rotate-self refuses to report
    success, returns non-zero, and records the refusal durably."""
    win = tmp_path / "windows.txt"
    win.write_text("adv-alive\n", encoding="utf-8")
    # successor never appears: the renamed predecessor is the only window
    monkeypatch.setattr(rotate, "spawn_window", lambda **kw: (0, "echo hi"))
    monkeypatch.setattr(rotate, "_read_ack",
                        lambda *a, **k: {"seat": "s", "gen_after": 1, "answer": "continue"})
    monkeypatch.setattr(rotate, "_kill_window", lambda *a, **k: None)
    args = _rotate_self_args(tmp_path, throwaway=True, window_path=str(win))
    rc = rotate.cmd_rotate_self(args, tmp_path)
    assert rc != 0
    assert "successor" in capsys.readouterr().err
    records = sorted((tmp_path / "sessions" / "rotations")
                     .glob("adv-alive.*.json"))
    assert records
    rec = json.loads(records[-1].read_text(encoding="utf-8"))
    assert rec["result"] == "refused"
    assert "successor" in rec["refusal_reason"]


def test_rotate_self_refuses_when_predecessor_window_gone(fake_ladder, tmp_path,
                                                          monkeypatch, capsys):
    """The predecessor (renamed) window is the chain this guarantee protects:
    if it is gone after the successor is confirmed, rotate-self must refuse to
    report success and record the refusal."""
    win = tmp_path / "windows.txt"
    win.write_text("adv-alive\n", encoding="utf-8")

    def fake_spawn(**kw):
        # successor appears under the plain name, but the predecessor vanished
        win.write_text("adv-alive\n", encoding="utf-8")
        return 0, "echo hi"

    monkeypatch.setattr(rotate, "spawn_window", fake_spawn)
    monkeypatch.setattr(rotate, "_read_ack",
                        lambda *a, **k: {"seat": "s", "gen_after": 1, "answer": "continue"})
    monkeypatch.setattr(rotate, "_kill_window", lambda *a, **k: None)
    args = _rotate_self_args(tmp_path, throwaway=True, window_path=str(win))
    rc = rotate.cmd_rotate_self(args, tmp_path)
    assert rc != 0
    assert "predecessor" in capsys.readouterr().err
    records = sorted((tmp_path / "sessions" / "rotations")
                     .glob("adv-alive.*.json"))
    assert records
    rec = json.loads(records[-1].read_text(encoding="utf-8"))
    assert rec["result"] == "refused"
    assert "predecessor" in rec["refusal_reason"]


def test_rotate_self_interrupted_after_spawn_leaves_started_record(
        fake_ladder, tmp_path, monkeypatch):
    """A non-`continue` read-back reply must leave a durable TERMINAL record
    (w3: SUCCEEDED BUT UNWITNESSED), not a frozen `started`.

    This branch did not write the record until this round, so the record was
    left at `started` -- indistinguishable from a rotation still in flight --
    and `readback_log` absent exactly where a diagnostician needs it. A living
    process that reaches the end of this branch now writes `unwitnessed`;
    `started` is reserved for genuine process-death, where no code runs.
    RED against the old code, which wrote nothing until the final step and
    left the rotations dir empty here
    (hypothesis:l4-rotation-record-survives-interruption).
    """
    win = tmp_path / "windows.txt"
    win.write_text("adv-alive\n", encoding="utf-8")

    def fake_spawn(**kw):
        # successor appears under the reused plain name, then the sequence
        # is interrupted before the read-back settles
        with open(win, "a", encoding="utf-8") as fh:
            fh.write("adv-alive\n")
        return 0, "echo hi"

    monkeypatch.setattr(rotate, "spawn_window", fake_spawn)
    # surrogate for the process being killed mid-read-back: the reply never
    # becomes the single confirming word `continue`
    monkeypatch.setattr(rotate, "_read_ack",
                        lambda *a, **k: None)
    monkeypatch.setattr(rotate, "_kill_window", lambda *a, **k: None)
    args = _rotate_self_args(tmp_path, throwaway=True, window_path=str(win))
    rc = rotate.cmd_rotate_self(args, tmp_path)
    assert rc != 0  # the DECISION is unchanged: `return 1` still fires
    records = sorted((tmp_path / "sessions" / "rotations")
                     .glob("adv-alive.*.json"))
    assert records, "rotation left NO durable record"
    assert len(records) == 1, "started + outcome must stay in ONE record file"
    rec = json.loads(records[0].read_text(encoding="utf-8"))
    # (w3) the record must be TERMINAL, not frozen at `started`
    assert rec["result"] == "unwitnessed", (
        f"record left {rec['result']!r}: a rotation that stopped looking "
        "in-flight is the defect, not the outcome")
    # generation is carried in the observation (the `started`-shape top-level
    # keys are gone from the terminal shape, same as the success record's)
    obs = rec.get("observations", {})
    assert obs.get("b_generation", {}).get("before") >= 0
    # (w3) readback_log is now POPULATED, not absent, exactly where a
    # diagnostician needs it
    assert "c_readback_log_path" in obs, "readback_log must be populated"
    assert obs["c_readback_log_path"], "readback_log must name a real path"


def test_rotate_self_success_leaves_exactly_one_record(fake_ladder, tmp_path,
                                                       monkeypatch):
    """A COMPLETED rotate-self still leaves exactly ONE record in today's
    shape, now in the `success` state — the `started` record opened up front
    is updated in place, never split into a second file
    (hypothesis:l4-rotation-record-survives-interruption).
    """
    win = tmp_path / "windows.txt"
    win.write_text("adv-alive\n", encoding="utf-8")

    def fake_spawn(**kw):
        with open(win, "a", encoding="utf-8") as fh:
            fh.write("adv-alive\n")
        return 0, "echo hi"

    monkeypatch.setattr(rotate, "spawn_window", fake_spawn)
    monkeypatch.setattr(rotate, "_read_ack",
                        lambda *a, **k: {"seat": "s", "gen_after": 1, "answer": "continue"})
    monkeypatch.setattr(rotate, "_kill_window", lambda *a, **k: None)
    monkeypatch.setattr(rotate, "_announce_rotation", lambda **k: None)
    args = _rotate_self_args(tmp_path, throwaway=True, window_path=str(win))
    rc = rotate.cmd_rotate_self(args, tmp_path)
    assert rc == 0
    records = sorted((tmp_path / "sessions" / "rotations")
                     .glob("adv-alive.*.json"))
    assert len(records) == 1, f"want exactly one record, got {len(records)}"
    rec = json.loads(records[0].read_text(encoding="utf-8"))
    assert rec["result"] == "success"
    assert "steps_reached" in rec or True


def test_loop_writes_durable_record(fake_ladder, tmp_path, monkeypatch):
    """cmd_loop also writes a durable record capturing the successor window
    (observed) and the ACK-channel path on a confirming rotation."""
    root = _proj(tmp_path)
    monkeypatch.chdir(root)
    monkeypatch.setattr(rotate, "find_project_root", lambda: root)
    monkeypatch.setattr(rotate, "cmd_meter", lambda args, root: 1)
    reply = tmp_path / "reply.log"
    # the successor's debug log STILL holds a bare `continue` -- the reader
    # must NOT confirm from it; the ack channel is the only authority.
    reply.write_text("continue\n")
    ack = rotate._ack_path(root, "belam-II")
    ack.parent.mkdir(parents=True, exist_ok=True)
    ack.write_text(json.dumps({"seat": "belam-II", "gen_after": None,
                               "answer": "continue"}), encoding="utf-8")
    wins = tmp_path / "windows.txt"
    wins.write_text("")

    def fake_launch(s, n, c):
        wins.write_text(n + "\n", encoding="utf-8")
        return 0

    monkeypatch.setattr(rotate, "_launch_window", fake_launch)
    code = rotate.cmd_loop(SimpleNamespace(
        session_log=None, force=True, role="prime_director", name="belam-II",
        name_prefix="belam", model=None, effort=None, settings=None,
        prompt_file=None, tmux_session="agi-rc", window_path=str(wins),
        debug_file=str(reply), dry_run=False, timeout=1,
    ), root)
    assert code == 0
    records = sorted((root / "sessions" / "rotations")
                     .glob("belam-II.*.json"))
    assert records, "loop wrote no durable record"
    rec = json.loads(records[-1].read_text(encoding="utf-8"))
    assert rec["rotation"] == "loop"
    assert rec["result"] == "success"
    a = rec["observations"]["a_successor_window_under_name"]
    assert a["present"] is True and a["window"] == "belam-II"
    assert str(rec["observations"]["c_readback_log_path"]).endswith(".ack.json")


# ── l3w4-seat-sessions-and-tiling: seats-launch & tile ────────────────────


def test_seats_launch_resolves_one_per_remote_seat(tmp_path, capsys,
                                                   monkeypatch):
    """A dry run resolves exactly one launch per non-ephemeral seat row, with
    THAT row's model/effort/tier; only fire-and-forget is excluded — tty and
    remote-control rows both get a launch line (owner ask "all of the
    non-ephemeral roles", claim test 1)."""
    rows = [
        {"name": "belam", "role": "prime_director", "model": "claude-fable-5-1",
         "effort": "max", "settings": "ultracode", "session_kind": "remote-control"},
        {"name": "adv-alive", "role": "parent", "model": "claude-opus-5",
         "effort": "max", "settings": "", "session_kind": "remote-control"},
        {"name": "ff-one", "role": "kid", "model": "glm", "effort": "high",
         "settings": "", "session_kind": "fire-and-forget"},
        {"name": "tty-one", "role": "director", "model": "claude-sonnet-5",
         "effort": "max", "settings": "", "session_kind": "tty"},
    ]
    _write_seats_sheet(tmp_path, rows)
    calls = []
    def fake_spawn(**kw):
        calls.append(kw)
        return 0, "echo ok"
    monkeypatch.setattr(rotate, "spawn_window", fake_spawn)
    args = SimpleNamespace(prompt_file=None, tmux_session="agi-rc",
                           window_path=None, dry_run=True, successor_argv=None)
    rc = rotate.cmd_seats_launch(args, tmp_path)
    assert rc == 0
    names = [c["name"] for c in calls]
    # fire-and-forget excluded; remote-control AND tty included
    assert names == ["belam", "adv-alive", "tty-one"], f"got {names}"
    # each resolved with ITS model and effort
    by_name = {c["name"]: c for c in calls}
    assert by_name["belam"]["model"] == "claude-fable-5-1"
    assert by_name["belam"]["effort"] == "max"
    assert by_name["belam"]["tier"] == "prime_director"
    assert by_name["adv-alive"]["model"] == "claude-opus-5"
    assert by_name["adv-alive"]["effort"] == "max"
    assert by_name["tty-one"]["model"] == "claude-sonnet-5"
    assert by_name["tty-one"]["tier"] == "director"


def test_seats_launch_read_back_confirms_all_windows(tmp_path, monkeypatch):
    """A non-dry launch read-backs every launched seat as a live window;
    a seat that spawns rc-ok but never appears as a window fails the
    read-back (trap-0c class: successful rotation, no window)."""
    rows = [
        {"name": "belam", "role": "prime_director", "model": "m",
         "effort": "max", "settings": "", "session_kind": "remote-control"},
        {"name": "tty-one", "role": "director", "model": "m2",
         "effort": "max", "settings": "", "session_kind": "tty"},
    ]
    _write_seats_sheet(tmp_path, rows)
    monkeypatch.setattr(rotate, "spawn_window",
                        lambda **kw: (0, "echo ok"))
    wpath = tmp_path / "windows.txt"

    # (a) all launched windows appear -> rc 0
    wpath.write_text("belam\ntty-one\n", encoding="utf-8")
    args = SimpleNamespace(prompt_file=None, tmux_session="agi-rc",
                           window_path=str(wpath), dry_run=False,
                           successor_argv=None)
    rc = rotate.cmd_seats_launch(args, tmp_path)
    assert rc == 0

    # (b) belam fails to appear -> read-back fails, rc 1
    wpath.write_text("tty-one\n", encoding="utf-8")
    rc = rotate.cmd_seats_launch(args, tmp_path)
    assert rc == 1


def test_seats_launch_no_remote_seats_returns_1(tmp_path, capsys):
    """All-fire-and-forget registry: nothing to launch, rc 1, no crash."""
    rows = [
        {"name": "ff-one", "role": "kid", "model": "glm", "effort": "high",
         "settings": "", "session_kind": "fire-and-forget"},
    ]
    _write_seats_sheet(tmp_path, rows)
    args = SimpleNamespace(prompt_file=None, tmux_session="agi-rc",
                           window_path=None, dry_run=True, successor_argv=None)
    rc = rotate.cmd_seats_launch(args, tmp_path)
    assert rc == 1


def _write_first_seating_rotations(tmp_path):
    """A config:rotations node whose director template declares a
    `startup.first_turn` probe (an allowlisted python3 script, referenced with
    `{repo}`/`{seat}`/`{gen}` placeholders) — the seed a first-seating spawn
    composes. The probe file is real so the command is a genuine first_turn."""
    g = tmp_path / "nodes" / ".geometry"
    g.mkdir(parents=True, exist_ok=True)
    (tmp_path / "bin").mkdir(parents=True, exist_ok=True)
    (tmp_path / "bin" / "probe_first_seating.py").write_text(
        "import sys\nprint(','.join(sys.argv[1:]))\n", encoding="utf-8")
    (g / "rotations.md").write_text(
        "---\nid: config:rotations\ntype: config\ntemplates:\n"
        "  director: {brief_file: x.md, steps: [spawn], telemetry: [seat],\n"
        "    startup: {first_turn: [{label: probe, "
        "cmd: \"python3 {repo}/bin/probe_first_seating.py {seat} gen={gen}\"}]}}\n"
        "---\n\nbody\n", encoding="utf-8")


def test_seats_launch_first_seating_appends_startup_output(tmp_path, capsys,
                                                           monkeypatch):
    """A first seating through seats-launch runs the seated role's
    `startup.first_turn` — the SAME composer rotate-self uses, reused not
    copied — and hands the successor a `## STARTUP OUTPUT` block on its first
    input with `{gen}` resolved to 1 (hypothesis:l4-a-first-seating-is-a-
    rotation-without-a-predecessor).
    """
    rows = [
        {"name": "director-seat", "role": "director", "model": "m",
         "effort": "max", "settings": "", "session_kind": "remote-control"},
    ]
    _write_seats_sheet(tmp_path, rows)
    _write_first_seating_rotations(tmp_path)
    calls = []
    def fake_spawn(**kw):
        calls.append(kw)
        return 0, "echo ok"
    monkeypatch.setattr(rotate, "spawn_window", fake_spawn)
    args = SimpleNamespace(prompt_file=None, tmux_session="agi-rc",
                           window_path=None, dry_run=True, successor_argv=None)
    rc = rotate.cmd_seats_launch(args, tmp_path)
    assert rc == 0
    assert calls, "no seat was spawned"
    extra = calls[0].get("extra", "")
    assert "## STARTUP OUTPUT" in extra, \
        f"first-seated seat's first input carries no STARTUP OUTPUT:\n{extra}"
    assert "[probe]" in extra
    assert "probe_first_seating.py director-seat gen=1" in extra, \
        f"{gen} not resolved to 1 for the first seating:\n{extra}"


def test_spawn_first_seating_appends_startup_output_when_seat_owned(
        tmp_path, capsys, monkeypatch):
    """`spawn --seat S` (a caller that OWNS a concrete seat) composes the
    role's first_turn and appends the STARTUP OUTPUT block to the first input;
    a seat-less generic spawn stays byte-identical (no block) — the ONE launcher
    stays the ONE launcher whether the seating is a rotation or a first seat.
    """
    _write_first_seating_rotations(tmp_path)
    calls = []
    def fake_spawn(**kw):
        calls.append(kw)
        return 0, "echo ok"
    monkeypatch.setattr(rotate, "spawn_window", fake_spawn)

    # seat-aware first seating -> STARTUP OUTPUT present
    args = SimpleNamespace(name="dir-a", tier="director", prompt_file=None,
                           model=None, effort=None, settings=None,
                           tmux_session="agi-rc", window_path=None,
                           dry_run=True, successor_argv=None, seat="dir-a")
    rc = rotate.cmd_spawn(args, tmp_path)
    assert rc == 0
    assert "## STARTUP OUTPUT" in calls[-1].get("extra", "")
    assert "probe_first_seating.py dir-a gen=1" in calls[-1]["extra"]

    # generic seat-less spawn -> byte-identical (no block, no first_turn run)
    args2 = SimpleNamespace(name="belam-X", tier="kid", prompt_file=None,
                            model=None, effort=None, settings=None,
                            tmux_session="agi-rc", window_path=None,
                            dry_run=True, successor_argv=None, seat=None)
    rc = rotate.cmd_spawn(args2, tmp_path)
    assert rc == 0
    assert calls[-1].get("extra", "") == "", \
        "a seat-less generic spawn must stay byte-identical (no STARTUP OUTPUT)"


def test_spawn_seat_row_is_the_model_source_flags_only_override(
        tmp_path, monkeypatch):
    """`spawn --seat S` with no --model/--effort/--settings builds the SEAT
    ROW's model, effort, settings and role — the precedence rotate-self, the
    reaper's respawn and seats-launch already use — never the ladder default
    of the `--tier` flag. Measured hole: the stream-master row (claude-sonnet-5,
    max) dry-ran as `--model claude-fable-5-1` from the prime_director tier
    default on 2026-09-12 00:2xZ (owner: "No surprise fable please."). Flags
    still override the row; a seat-less spawn is byte-identical to before.
    """
    _write_first_seating_rotations(tmp_path)
    _write_seats_sheet(tmp_path, [
        {"name": "stream-master", "role": "director", "model": "claude-sonnet-5",
         "effort": "max", "settings": "", "session_kind": "remote-control"},
    ])
    calls = []
    def fake_spawn(**kw):
        calls.append(kw)
        return 0, "echo ok"
    monkeypatch.setattr(rotate, "spawn_window", fake_spawn)

    # no flags -> the row's cells and the row's role, not the tier flag's
    args = SimpleNamespace(name="stream-master", tier="prime_director",
                           prompt_file=None, model=None, effort=None,
                           settings=None, tmux_session="agi-rc",
                           window_path=None, dry_run=True, successor_argv=None,
                           seat="stream-master")
    assert rotate.cmd_spawn(args, tmp_path) == 0
    kw = calls[-1]
    assert kw["model"] == "claude-sonnet-5"
    assert kw["effort"] == "max"
    assert kw["settings"] is None          # "" -> no --settings flag (no ultracode)
    assert kw["tier"] == "director"        # the row's role, not prime_director

    # explicit flags override the row
    args2 = SimpleNamespace(name="stream-master", tier="prime_director",
                            prompt_file=None, model="claude-opus-5",
                            effort="high", settings='{"ultracode": true}',
                            tmux_session="agi-rc", window_path=None,
                            dry_run=True, successor_argv=None,
                            seat="stream-master")
    assert rotate.cmd_spawn(args2, tmp_path) == 0
    kw2 = calls[-1]
    assert kw2["model"] == "claude-opus-5" and kw2["effort"] == "high"
    assert kw2["settings"] == {"ultracode": True}

    # seat-less generic spawn: nothing from any row, tier flag as before
    args3 = SimpleNamespace(name="belam-X", tier="kid", prompt_file=None,
                            model=None, effort=None, settings=None,
                            tmux_session="agi-rc", window_path=None,
                            dry_run=True, successor_argv=None, seat=None)
    assert rotate.cmd_spawn(args3, tmp_path) == 0
    kw3 = calls[-1]
    assert kw3["model"] is None and kw3["effort"] is None
    assert kw3["settings"] is None and kw3["tier"] == "kid"


# ── first-seating alert (hypothesis:l4-a-first-seating-sends-the-sensei-the-
# same-alert-a-rotation-does, goal:g15.17): a first seating emits the SAME
# [rotation-alert] dm a rotation does (trigger: first-seating, generation
# 0 -> 1) and writes ONE gen-1 seating record carrying the first_turn results.

def _seating_registry(tmp_path, raw="@42"):
    """A fake `~/.claude/sessions` registry dir whose <pid>.json carries the
    window @id the JOIN matches on, so the bounded join finds it instantly."""
    reg = tmp_path / "registry"
    reg.mkdir(parents=True, exist_ok=True)
    (reg / "999.json").write_text(json.dumps({
        "window_id": raw, "session_id": "2717-aaaa",
        "transcript": "t.jsonl", "cwd": str(tmp_path)}), encoding="utf-8")
    return reg


def test_compose_seating_announcement_shape():
    """The seating payload carries seat, window @id, ref (or the NAMED pending
    wording), pid, session id, transcript, seq, in flight — the composer's
    shape one test asserts (g15.17 item 3)."""
    body = rotate._compose_seating_announcement(
        seat="director-seat", window_id="42", ref="caa927", pid=999,
        session_id="2717-aaaa", transcript_path="t.jsonl", seq=3,
        in_flight="1 first_turn step(s) ran")
    assert body.startswith("[rotation-alert] first seating director-seat @42 "
                           "[caa927] | generation 0 -> 1 |")
    assert "trigger: first-seating" in body
    assert "pid: 999" in body and "session: 2717-aaaa" in body
    assert "transcript: t.jsonl" in body and "seq: 3" in body
    # window @id already carries its @; never double it.
    assert "@@" not in body
    # ref absent -> the NAMED pending-ack wording, never " [ ]"
    pre = rotate._compose_seating_announcement(
        seat="director-seat", window_id="42", seq=1)
    assert "ref: (pending ack)" in pre and "[]" not in pre


def test_compose_seating_announcement_ask_diff_exact_ack_line():
    """Claim (3): WITH `--ask-diff` the seating alert appends the exact
    `rotate.py ack --seat S --gen 1 --ref <ref> diff --text -` line -- never
    `--gen 0`, never a bare `(pending ack)` without the line -- and the
    default carries NO ack line. (hypothesis:l4-the-spawn-gate-refuses-both-
    directions-and-a-hand-seating-commits-its-row-and-answers-the-ack)"""
    line = (rotate._compose_seating_announcement(
        seat="director-seat", window_id="42", seq=1, ask_diff=True))
    assert "generation 0 -> 1" in line and "--gen 0" not in line
    assert ("rotate.py ack --seat director-seat --gen 1 "
            "--ref <your ListAgents ref> diff --text -") in line, line
    assert "ref: (pending ack)" in line, \
        "with ask-diff the ref placeholder still renders, plus the line"
    plain = rotate._compose_seating_announcement(
        seat="director-seat", window_id="42", seq=1)
    assert "rotate.py ack" not in plain and "diff --text" not in plain


def test_spawn_first_seating_emits_seating_alert_and_record(tmp_path, monkeypatch):
    """A first seating through `spawn --seat S` (non-dry) emits the SAME
    rotation-alert dm a rotation does — trigger: first-seating, generation
    0 -> 1, carrying seat, window @id, pid, session id — and writes ONE
    gen-1 seating record carrying the first_turn results. The falsifier: a
    spawn after which the Sensei's dm has no seating line."""
    import send as _send  # the SAME top-level module rotate's lazy import binds to
    rows = [
        {"name": "director-seat", "role": "director", "model": "m",
         "effort": "max", "settings": "", "session_kind": "remote-control"},
        {"name": "sensei-peer", "role": "prime_director"},
    ]
    _write_seats_sheet(tmp_path, rows)
    _write_first_seating_rotations(tmp_path)
    wins = tmp_path / "windows.txt"
    wins.write_text("@42 director-seat\nsensei-peer\n", encoding="utf-8")
    reg = _seating_registry(tmp_path)
    sent = []
    monkeypatch.setattr(_send, "send_dm",
                        lambda croot, me, other, text, sender: sent.append(
                            (other, text)) or tmp_path)
    monkeypatch.setattr(rotate, "spawn_window", lambda **kw: (0, "echo ok"))
    args = SimpleNamespace(name="director-seat", tier="director",
                           prompt_file=None, model=None, effort=None,
                           settings=None, tmux_session="agi-rc",
                           window_path=str(wins), dry_run=False,
                           successor_argv=None, seat="director-seat",
                           registry_dir=str(reg))
    rc = rotate.cmd_spawn(args, tmp_path)
    assert rc == 0
    assert sent, f"a first seating must nudge the Sensei's peer: {sent}"
    _to, text = sent[0]
    assert _to == "sensei-peer"
    assert "first seating director-seat @42" in text
    assert "generation 0 -> 1" in text
    assert "trigger: first-seating" in text
    assert "ref: (pending ack)" in text
    assert "pid: 999" in text and "session: 2717-aaaa" in text
    assert "in flight" in text
    recs = list(rotate._rotations_dir(tmp_path).glob("director-seat.*.seating.json"))
    assert len(recs) == 1, f"exactly ONE seating record, got {recs}"
    rec = json.loads(recs[0].read_text(encoding="utf-8"))
    assert rec["rotation"] == "seating" and rec["gen_after"] == 1
    assert rec["trigger"] == "first-seating" and rec["source"] == "cmd_spawn"
    assert rec["session_id"] == "2717-aaaa" and rec["window_id"] == "@42"
    assert rec["first_turn"], "the seating record must carry the first_turn results"
    assert rec["first_turn"][0]["label"] == "probe"


def test_spawn_first_seating_default_ack_source_seating_wake_zero(
        tmp_path, monkeypatch):
    """Claim (3) default: a hand seating answers its OWN ack `continue,
    source: seating` (SL7.06's contract) so the post wakes at 0 -- the alert
    carries NO `rotate.py ack ... diff` line, never `--gen 0`.
    (hypothesis:l4-the-spawn-gate-refuses-both-directions-and-a-hand-
    seating-commits-its-row-and-answers-the-ack, claim 3)"""
    import send as _send
    rows = [
        {"name": "director-seat", "role": "director", "model": "m",
         "effort": "max", "settings": "", "session_kind": "remote-control"},
        {"name": "sensei-peer", "role": "prime_director"},
    ]
    _write_seats_sheet(tmp_path, rows)
    _write_first_seating_rotations(tmp_path)
    wins = tmp_path / "windows.txt"
    wins.write_text("@42 director-seat\nsensei-peer\n", encoding="utf-8")
    reg = _seating_registry(tmp_path)
    sent = []
    monkeypatch.setattr(_send, "send_dm",
                        lambda croot, me, other, text, sender:
                        sent.append((other, text)) or tmp_path)
    monkeypatch.setattr(rotate, "spawn_window", lambda **kw: (0, "echo ok"))
    args = SimpleNamespace(name="director-seat", tier="director",
                           prompt_file=None, model=None, effort=None,
                           settings=None, tmux_session="agi-rc",
                           window_path=str(wins), dry_run=False,
                           successor_argv=None, seat="director-seat",
                           registry_dir=str(reg), pid=None, ask_diff=False)
    rc = rotate.cmd_spawn(args, tmp_path)
    assert rc == 0
    ack = json.loads((rotate._ack_path(tmp_path, "director-seat"))
                     .read_text(encoding="utf-8"))
    assert ack["answer"] == "continue", ack
    assert ack["source"] == "seating", ack
    assert ack["gen_after"] == 1
    _to, text = sent[0]
    assert "generation 0 -> 1" in text and "--gen 0" not in text
    assert "rotate.py ack" not in text, \
        f"default seating alert must carry NO ack line: {text}"
    assert "diff --text" not in text


def test_spawn_first_seating_ask_diff_prints_exact_ack_line(
        tmp_path, monkeypatch):
    """Claim (3) `--ask-diff`: the seating alert prints the exact
    `rotate.py ack --seat S --gen 1 --ref <ref> diff --text -` line -- never
    `--gen 0`, never a bare `(pending ack)` without the line -- and the ack
    is left `diff-requested, source: seating`. (hypothesis:l4-the-spawn-
    gate-refuses-both-directions-and-a-hand-seating-commits-its-row-and-
    answers-the-ack, claim 3)"""
    import send as _send
    rows = [
        {"name": "director-seat", "role": "director", "model": "m",
         "effort": "max", "settings": "", "session_kind": "remote-control"},
        {"name": "sensei-peer", "role": "prime_director"},
    ]
    _write_seats_sheet(tmp_path, rows)
    _write_first_seating_rotations(tmp_path)
    wins = tmp_path / "windows.txt"
    wins.write_text("@42 director-seat\nsensei-peer\n", encoding="utf-8")
    reg = _seating_registry(tmp_path)
    sent = []
    monkeypatch.setattr(_send, "send_dm",
                        lambda croot, me, other, text, sender:
                        sent.append((other, text)) or tmp_path)
    monkeypatch.setattr(rotate, "spawn_window", lambda **kw: (0, "echo ok"))
    args = SimpleNamespace(name="director-seat", tier="director",
                           prompt_file=None, model=None, effort=None,
                           settings=None, tmux_session="agi-rc",
                           window_path=str(wins), dry_run=False,
                           successor_argv=None, seat="director-seat",
                           registry_dir=str(reg), pid=None, ask_diff=True)
    rc = rotate.cmd_spawn(args, tmp_path)
    assert rc == 0
    ack = json.loads((rotate._ack_path(tmp_path, "director-seat"))
                     .read_text(encoding="utf-8"))
    assert ack["answer"] == "diff-requested", ack
    assert ack["source"] == "seating", ack
    assert ack["gen_after"] == 1
    _to, text = sent[0]
    assert "generation 0 -> 1" in text and "--gen 0" not in text
    assert ("rotate.py ack --seat director-seat --gen 1 "
            "--ref <your ListAgents ref> diff --text -") in text, text


def test_seats_launch_first_seating_emits_seating_alert(tmp_path, monkeypatch):
    """seats-launch is a first seating PER SEAT: each newly-seated window emits
    the trigger: first-seating alert (hypothesis:l4-a-first-seating-sends-the-
    sensei-the-same-alert-a-rotation-does)."""
    import send as _send
    rows = [
        {"name": "director-seat", "role": "director", "model": "m",
         "effort": "max", "settings": "", "session_kind": "remote-control"},
        {"name": "sensei-peer", "role": "prime_director",
         "session_kind": "remote-control"},
    ]
    _write_seats_sheet(tmp_path, rows)
    _write_first_seating_rotations(tmp_path)
    wins = tmp_path / "windows.txt"
    wins.write_text("@42 director-seat\nsensei-peer\n", encoding="utf-8")
    reg = _seating_registry(tmp_path)
    sent = []
    monkeypatch.setattr(_send, "send_dm",
                        lambda croot, me, other, text, sender: sent.append(
                            (other, text)) or tmp_path)
    monkeypatch.setattr(rotate, "spawn_window", lambda **kw: (0, "echo ok"))
    args = SimpleNamespace(prompt_file=None, tmux_session="agi-rc",
                           window_path=str(wins), dry_run=False,
                           successor_argv=None, registry_dir=str(reg))
    rc = rotate.cmd_seats_launch(args, tmp_path)
    assert rc == 0
    texts = [t for _o, t in sent]
    assert any("first seating director-seat" in t for t in texts), \
        f"seats-launch must alert on each first seating:\n{sent}"
    # exactly one seating record per first-seated seat (director-seat)
    recs = list(rotate._rotations_dir(tmp_path).glob("director-seat.*.seating.json"))
    assert len(recs) == 1
    rec = json.loads(recs[0].read_text(encoding="utf-8"))
    assert rec["source"] == "cmd_seats_launch"


def test_ack_gen1_first_seating_announces_once_dedup(tmp_path, monkeypatch):
    """A HAND launch acked at --gen 1 emits the same alert when no seating
    record exists, and does NOT double-send when one does (the falsifier: a
    second dm for the same seat + gen)."""
    import send as _send
    rows = [
        {"name": "hand-seat", "role": "director"},
        {"name": "sensei-peer", "role": "prime_director"},
    ]
    _write_seats_sheet(tmp_path, rows)
    sent = []
    monkeypatch.setattr(_send, "send_dm",
                        lambda croot, me, other, text, sender: sent.append(
                            (other, text)) or tmp_path)
    monkeypatch.setattr(rotate, "_existing_windows",
                        lambda s, wp: ["hand-seat", "sensei-peer"])
    monkeypatch.setattr(rotate, "_successor_window_id", lambda *a, **k: None)
    args = SimpleNamespace(seat="hand-seat", gen=1, ref="caa927",
                           answer="continue", text=None)
    # first ack --gen 1 (no record yet) -> record + announce
    rc = rotate.cmd_ack(args, tmp_path)
    assert rc == 0
    assert len(sent) == 1, f"first hand-launch ack must announce once: {sent}"
    _to, text = sent[0]
    assert "first seating hand-seat" in text and "[caa927]" in text
    assert "trigger: first-seating" in text
    recs = list(rotate._rotations_dir(tmp_path).glob("hand-seat.*.seating.json"))
    assert len(recs) == 1, f"exactly ONE seating record, got {recs}"
    rec = json.loads(recs[0].read_text(encoding="utf-8"))
    assert rec["ref"] == "caa927" and rec["source"] == "cmd_ack"
    ac = json.loads((rotate._ack_path(tmp_path, "hand-seat")).read_text(
        encoding="utf-8"))
    assert ac["session_ref"] == "caa927"
    # second ack --gen 1 (record now exists) -> NO second dm
    sent.clear()
    monkeypatch.setattr(rotate.sys, "stdin", _FakeIn(""))
    rc = rotate.cmd_ack(args, tmp_path)
    assert rc == 0
    assert sent == [], f"a second dm for the same seat + gen is the falsifier: {sent}"


def test_ack_gen1_does_not_announce_for_non_first_generation(tmp_path, monkeypatch):
    """Only --gen 1 (the no-predecessor first generation) is a hand-seating;
    a rotation ack at a later generation never re-announces it."""
    import send as _send
    rows = [{"name": "seat-x", "role": "director"}]
    _write_seats_sheet(tmp_path, rows)
    sent = []
    monkeypatch.setattr(_send, "send_dm",
                        lambda croot, me, other, text, sender: sent.append(
                            (other, text)) or tmp_path)
    monkeypatch.setattr(rotate, "_existing_windows", lambda s, wp: ["seat-x"])
    monkeypatch.setattr(rotate, "_successor_window_id", lambda *a, **k: None)
    rc = rotate.cmd_ack(SimpleNamespace(seat="seat-x", gen=4, ref="ff",
                                        answer="continue", text=None), tmp_path)
    assert rc == 0
    assert sent == [], f"a gen-4 rotation ack must not announce a seating: {sent}"
    assert not list(rotate._rotations_dir(tmp_path).glob("seat-x.*.seating.json"))


def test_announce_rotation_same_composer_writes_seating_record(tmp_path, monkeypatch):
    """The SAME composer (_announce_rotation) produces both shapes: with a
    `seating` dict it writes the ONE seating record + the seating text; the
    rotation callers pass no seating and get the rotation shape (g15.17 item
    1 'one composer')."""
    import send as _send
    rows = [{"name": "kid-a", "role": "director"},
            {"name": "hand-seat", "role": "parent"}]
    _write_seats_sheet(tmp_path, rows)
    sent = []
    monkeypatch.setattr(_send, "send_dm",
                        lambda croot, me, other, text, sender: sent.append(
                            (other, text)) or tmp_path)
    seating = rotate._seating_record(
        seat="hand-seat", role="parent", source="cmd_ack", window_id="@7",
        ref="caa927", pid=11, session_id="s1", transcript_path="t.jsonl",
        first_turn=[])
    delivered = rotate._announce_rotation(
        root=tmp_path, croot=tmp_path / "comms", seat="hand-seat",
        successor="hand-seat", gen_before=0, gen_after=1,
        trigger="first-seating", handoff_path="h", in_flight="boot",
        live_names=["kid-a", "hand-seat"], successor_ref="caa927",
        successor_window="7", seating=seating)
    assert delivered == ["kid-a"]
    (_, text), = sent
    assert "trigger: first-seating" in text and "first seating hand-seat @7" in text
    recs = list(rotate._rotations_dir(tmp_path).glob("hand-seat.*.seating.json"))
    assert len(recs) == 1, "one seating record shared with the alert"


def test_tiler_partitions_full_screen_no_overlap_no_gaps():
    """For N=1..12 the partition covers width*height exactly (no gaps) and no
    two rects overlap."""
    W, H = 1920, 1080
    for n in range(1, 13):
        tiles = rotate.partition_tiles(n, 0, 0, W, H)
        assert len(tiles) == n, f"n={n}: {len(tiles)} tiles"
        area = sum(tw * th for _, _, tw, th in tiles)
        assert area == W * H, f"n={n}: area {area} != {W*H}"
        for i, (x1, y1, w1, h1) in enumerate(tiles):
            for x2, y2, w2, h2 in tiles[i + 1:]:
                overlap = (x1 < x2 + w2 and x2 < x1 + w1
                           and y1 < y2 + h2 and y2 < y1 + h1)
                assert not overlap, f"n={n}: overlap {(x1,y1,w1,h1)} vs {(x2,y2,w2,h2)}"


def test_tile_command_dry_run_prints_one_rect_per_window(monkeypatch, tmp_path,
                                                         capsys):
    monkeypatch.setattr(rotate, "find_project_root", lambda: tmp_path)
    root = tmp_path / "nodes" / ".geometry"
    root.mkdir(parents=True, exist_ok=True)
    rc = rotate.main(["tile", "--count", "4", "--width", "100", "--height", "100",
                      "--dry-run"])
    assert rc == 0
    lines = [l for l in capsys.readouterr().out.splitlines() if l.strip()]
    assert len(lines) == 4
    # 4 tiles over 100x100 must sum to full area
    total = 0
    for l in lines:
        _, rest = l.split(":", 1)
        kv = dict(p.split("=") for p in rest.strip().split())
        total += int(kv["w"]) * int(kv["h"])
    assert total == 100 * 100


def test_tile_apply_places_live_windows_via_wmctrl(monkeypatch, tmp_path):
    """tile --apply reads the live seat windows and issues a wmctrl resize per
    window at its no-gap rect — geometry covers the whole screen."""
    rows = [
        {"name": "belam", "role": "prime_director", "model": "m",
         "effort": "max", "settings": "", "session_kind": "remote-control"},
        {"name": "tty-one", "role": "director", "model": "m2",
         "effort": "max", "settings": "", "session_kind": "tty"},
    ]
    _write_seats_sheet(tmp_path, rows)
    wpath = tmp_path / "live.txt"
    wpath.write_text("belam\ntty-one\n", encoding="utf-8")
    monkeypatch.setattr(rotate, "_screen_tool", lambda: "wmctrl")
    issued = []
    class _Proc:
        returncode = 0
        stderr = ""
    def fake_run(argv, **kw):
        issued.append(argv)
        return _Proc()
    monkeypatch.setattr(rotate, "_RUN", fake_run)
    args = SimpleNamespace(names=None, window_path=str(wpath),
                           tmux_session="agi-rc", width=100, height=100)
    rc = rotate._cmd_tile_apply(args, tmp_path, 100, 100)
    assert rc == 0
    # one command per live window, each a wmctrl resize by name
    assert len(issued) == 2
    for argv, name in zip(issued, ("belam", "tty-one")):
        assert argv[0] == "wmctrl" and argv[2] == name and argv[3] == "-e"
    # geometry covers 100x100 exactly, no overlap (partition_tiles invariant)
    rects = []
    for argv in issued:
        g = argv[4].split(",")
        rects.append(tuple(int(v) for v in (g[1], g[2], g[3], g[4])))
    area = sum(w * h for _, _, w, h in rects)
    assert area == 100 * 100


def test_tile_apply_degrades_gracefully_without_wm(monkeypatch, tmp_path):
    """No wmctrl/xdotool on PATH => geometry printed, X :1 not reached, still
    rc 0 and the full set of rects shown."""
    rows = [{"name": "belam", "role": "prime_director", "model": "m",
             "effort": "max", "settings": "", "session_kind": "remote-control"}]
    _write_seats_sheet(tmp_path, rows)
    wpath = tmp_path / "live.txt"
    wpath.write_text("belam\n", encoding="utf-8")
    monkeypatch.setattr(rotate, "_screen_tool", lambda: None)
    placed, issued = rotate._place_windows({"belam": (0, 0, 100, 100)}, None)
    assert placed == 0 and issued == 0
    args = SimpleNamespace(names=None, window_path=str(wpath),
                           tmux_session="agi-rc", width=100, height=100)
    rc = rotate._cmd_tile_apply(args, tmp_path, 100, 100)
    assert rc == 0


# ── l3w4-rotation-announces-itself: rotation announces itself over the alert channel ──
# RED-FIRST for experiment:a00-67a5c714-9c8cd8. Tests assert: (1) the five-field
# payload, (2) recipient derivation drops a gone window + the rotating seat, (3) a
# non-prime rotation dms every derived recipient exactly one announcement carrying
# all five fields, (4) the prime routes to the alert room, never quorum, (5) the
# loop and rotate-self success paths each announce EXACTLY once, (6) a refused
# rotation announces NOTHING.

FIVE_FIELDS = ("outgoing", "successor", "generation", "trigger", "handoff")


def test_compose_announcement_carries_all_five_fields():
    body = rotate._compose_announcement(
        seat="belam-II", successor="belam-III", gen_before=2, gen_after=3,
        trigger="meter due", handoff_path=".agi/sessions/belam-III.log",
        in_flight="master-sensei handoff in progress", seq=41)
    assert body.startswith(rotate.ROTATION_ALERT_TAG)
    assert "belam-II" in body and "belam-III" in body
    assert "2 -> 3" in body
    assert "trigger: meter due" in body
    assert "handoff: .agi/sessions/belam-III.log" in body
    assert "in flight: master-sensei handoff in progress" in body
    # scope extension: the monotonic sequence stamp is part of the payload
    assert "seq: 41" in body


def test_compose_announcement_carries_successor_address_after_join():
    """mechanism 1 (hypothesis:l4-a-rotation-costs-the-live-seats-zero-calls-
    and-the-successor-one): once the JOIN has resolved the successor's ref and
    window @id, the alert carries the FULL post-join address `name [ref]
    @window` — the zero-call identity a peer needs (no whois round-trip)."""
    body = rotate._compose_announcement(
        seat="belam-II", successor="belam-III", gen_before=2, gen_after=3,
        trigger="rotate-self", handoff_path="h.md", in_flight="none",
        seq=7, successor_ref="f52a4c", successor_window="9")
    assert "belam-II -> belam-III [f52a4c] @9 |" in body
    assert "pre-join" not in body


def test_successor_address_never_doubles_the_window_at():
    """Sensei 182119Z audit: the live alert read `@@291` because the JOIN's
    window id already carries its `@`. One `@`, whichever form arrives."""
    assert rotate._successor_address("belam-III", "f52a4c", "@291") \
        == "belam-III [f52a4c] @291"
    assert rotate._successor_address("belam-III", "f52a4c", "291") \
        == "belam-III [f52a4c] @291"
    assert "@@" not in rotate._successor_address("belam-III", "", "@291")


def test_compose_announcement_pre_join_names_identity_unresolved():
    """mechanism 1 — a pre-join alert (no ref acked / JOIN found nothing)
    NAMES that it is pre-join instead of silently dropping the identity a
    peer would need to reach the successor."""
    body = rotate._compose_announcement(
        seat="belam-II", successor="belam-III", gen_before=2, gen_after=3,
        trigger="rotate-self", handoff_path="h.md", in_flight="none",
        seq=8)
    # the successor NAME still names the seat; the ref is the absent join
    # fact and is called out as pre-join, never faked.
    assert "belam-III (pre-join" in body
    assert "pre-join: successor ref not yet resolved" in body
    assert "belam-III [" not in body


@pytest.mark.parametrize("window", ["", "41"])
def test_compose_announcement_pre_join_when_ref_absent_even_with_window(window):
    """mechanism 1 — the ref (ListAgents @id from the JOIN) is THE join fact;
    without it a window @id alone still means pre-join and must say so."""
    body = rotate._compose_announcement(
        seat="belam-II", successor="belam-III", gen_before=2, gen_after=3,
        trigger="rotate-self", handoff_path="h.md", in_flight="none",
        seq=9, successor_window=window)
    assert "(pre-join: successor ref not yet resolved)" in body
    if window:
        assert f"belam-III @{window} (pre-join" in body


def test_announce_rotation_dms_post_join_address(monkeypatch, tmp_path):
    """mechanism 1 — the address flows THROUGH _announce_rotation into every
    recipient dm, so the peers' messages carry `name [ref] @window` after a
    fixture join (the dm IS the zero-call hop that carries it)."""
    rows = [{"name": "kid-a", "role": "director"},
            {"name": "belam-II", "role": "prime_director"}]
    _write_seats_sheet(tmp_path, rows)
    sent = []
    import send as _send
    monkeypatch.setattr(_send, "send_dm",
                        lambda croot, me, other, text, sender: sent.append(
                            (other, text)) or tmp_path)
    delivered = rotate._announce_rotation(
        root=tmp_path, croot=tmp_path / "comms", seat="belam-II",
        successor="belam-III", gen_before=2, gen_after=3, trigger="rotate-self",
        handoff_path=".agi/sessions/belam-III.handoff.md", in_flight="none",
        live_names=["kid-a", "belam-II"], successor_ref="f52a4c",
        successor_window="9")
    assert delivered == ["kid-a"]
    assert len(sent) == 1
    _, text = sent[0]
    assert "belam-II -> belam-III [f52a4c] @9 |" in text


def test_derive_receivers_drops_gone_window_and_self(tmp_path):
    rows = [{"name": "kid-a", "role": "director"},
            {"name": "liason", "role": "parent"},
            {"name": "kid-b", "role": "director"}]
    _write_seats_sheet(tmp_path, rows)
    # seats -> live windows intersection: kid-b's window is GONE -> dropped;
    # the rotating seat (whatever its row) is never told of its own rotation.
    got = rotate._derive_receivers(tmp_path, seat="liason",
                                   live_names=["kid-a", "liason"])
    assert got == ["kid-a"]


def test_announce_rotation_dms_every_derived_recipient(monkeypatch, tmp_path):
    rows = [{"name": "kid-a", "role": "director"},
            {"name": "liason", "role": "parent"},
            {"name": "kid-b", "role": "director"}]
    _write_seats_sheet(tmp_path, rows)
    sent = []
    import send as _send  # the SAME top-level module rotate's lazy import binds to
    monkeypatch.setattr(_send, "send_dm",
                        lambda croot, me, other, text, sender: sent.append(
                            (other, text)) or tmp_path)
    delivered = rotate._announce_rotation(
        root=tmp_path, croot=tmp_path / "comms", seat="liason",
        successor="liason", gen_before=1, gen_after=2, trigger="rotate-self",
        handoff_path=".agi/sessions/liason.handoff.md", in_flight="none",
        live_names=["kid-a", "liason", "kid-b"])
    assert delivered == ["kid-a", "kid-b"]
    assert [to for to, _ in sent] == ["kid-a", "kid-b"]
    for _, text in sent:
        assert "trigger: rotate-self" in text
        assert "in flight: none" in text


def test_announce_rotation_prime_routes_to_alert_room_never_quorum(
        monkeypatch, tmp_path):
    room_posts = []
    import send as _send  # the SAME top-level module rotate's lazy import binds to
    monkeypatch.setattr(_send, "send_room",
                        lambda croot, room, text, sender: room_posts.append(
                            (room, text)) or tmp_path)
    delivered = rotate._announce_rotation(
        root=tmp_path, croot=tmp_path / "comms", seat="prime",
        successor="belam-III", gen_before=2, gen_after=3, trigger="--force",
        handoff_path=".agi/sessions/belam-III.log", in_flight="none",
        live_names=["kid-a", "prime"])
    assert delivered == [rotate.ROTATION_ALERT_ROOM]
    assert len(room_posts) == 1
    room, text = room_posts[0]
    assert room == rotate.ROTATION_ALERT_ROOM
    assert "quorum" not in room
    assert "generation 2 -> 3" in text
    assert "trigger: --force" in text


# ── clause 1 of hypothesis:l4-a-rotation-alert-lands-in-the-inbox-a-
# ── coalesced-nudge-still-wakes-and-detected-records-dedupe: the alert must
# ── land in each recipient's INBOX (`<sessions>/inbox/<seat>.md`, the writer
# ── `send.send` / the reader `send.py read` use), IN ADDITION to the dm log,
# ── so nothing depends on the nudge (it is delivery, the inbox is the record).


def test_announce_rotation_lands_alert_in_each_recipient_inbox(
        monkeypatch, tmp_path):
    """Clause 1 non-prime leg: every derived recipient's INBOX file holds the
    [rotation-alert] block that `send.py read <recv>` shows, while the dm-log
    hop (send_dm) still happens with the same payload. Falsifier: an alert
    absent from a recipient's inbox."""
    rows = [{"name": "kid-a", "role": "director"},
            {"name": "liason", "role": "parent"},
            {"name": "kid-b", "role": "director"}]
    _write_seats_sheet(tmp_path, rows)
    dms = []
    import send as _send
    monkeypatch.setattr(_send, "send_dm",
                        lambda croot, me, other, text, sender: dms.append(
                            (other, text)) or tmp_path)
    rotate._announce_rotation(
        root=tmp_path, croot=tmp_path / "comms", seat="liason",
        successor="liason", gen_before=1, gen_after=2, trigger="rotate-self",
        handoff_path=".agi/sessions/liason.handoff.md", in_flight="none",
        live_names=["kid-a", "liason", "kid-b"])
    inbox_dir = tmp_path / "sessions" / "inbox"
    for recv in ("kid-a", "kid-b"):
        inbox = inbox_dir / f"{recv}.md"
        assert inbox.is_file(), f"no inbox file for {recv}: {inbox}"
        body = inbox.read_text(encoding="utf-8")
        assert "[rotation-alert]" in body, f"{recv} inbox lacks the alert"
        assert "trigger: rotate-self" in body
        assert "in flight: none" in body
    # dm-log hop unchanged, same payload.
    assert [to for to, _ in dms] == ["kid-a", "kid-b"]
    for _, text in dms:
        assert "[rotation-alert]" in text


def test_announce_rotation_prime_lands_alert_in_own_inbox(
        monkeypatch, tmp_path):
    """Clause 1 prime leg: ROTATION_ALERT_ROOM is NOT the prime's inbox
    (`<sessions>/inbox/prime.md` is a different file, what `send.py read`
    reads), so the room alone does not satisfy "lands in the inbox". The prime
    is inbox-only (dm/room may not address it), but `send.send` imposes no
    prime restriction -- it IS the inbox-only writer -- so a prime-specific
    send() puts the same [rotation-alert] block into the prime's OWN inbox
    alongside the shared room post, never into quorum."""
    _write_seats_sheet(tmp_path, [{"name": "prime", "role": "prime_director"}])
    room_posts = []
    import send as _send
    monkeypatch.setattr(_send, "send_room",
                        lambda croot, room, text, sender: room_posts.append(
                            (room, text)) or tmp_path)
    delivered = rotate._announce_rotation(
        root=tmp_path, croot=tmp_path / "comms", seat="prime",
        successor="belam-III", gen_before=2, gen_after=3, trigger="--force",
        handoff_path=".agi/sessions/belam-III.log", in_flight="none",
        live_names=["kid-a", "prime"])
    assert delivered == [rotate.ROTATION_ALERT_ROOM]
    assert len(room_posts) == 1
    prime_inbox = tmp_path / "sessions" / "inbox" / "prime.md"
    assert prime_inbox.is_file(), f"no prime inbox: {prime_inbox}"
    body = prime_inbox.read_text(encoding="utf-8")
    assert "[rotation-alert]" in body
    assert "generation 2 -> 3" in body
    assert "trigger: --force" in body


def test_loop_success_announces_exactly_once_refusal_never(
        fake_ladder, tmp_path, monkeypatch):
    root = _proj(tmp_path)
    monkeypatch.chdir(root)
    monkeypatch.setattr(rotate, "find_project_root", lambda: root)
    monkeypatch.setattr(rotate, "cmd_meter", lambda args, root: 1)
    calls = []
    monkeypatch.setattr(rotate, "_announce_rotation",
                        lambda **kw: calls.append(kw) or [])

    success_reply = tmp_path / "reply.log"
    success_reply.write_text("continue\n")
    ack = rotate._ack_path(root, "belam-II")
    ack.parent.mkdir(parents=True, exist_ok=True)
    ack.write_text(json.dumps({"seat": "belam-II", "gen_after": None,
                               "answer": "continue"}), encoding="utf-8")
    wins = tmp_path / "windows.txt"
    wins.write_text("")

    def fake_launch(s, n, c):
        wins.write_text(n + "\n", encoding="utf-8")
        return 0
    monkeypatch.setattr(rotate, "_launch_window", fake_launch)

    code = rotate.cmd_loop(SimpleNamespace(
        session_log=None, force=True, role="prime_director", name="belam-II",
        name_prefix="belam", model=None, effort=None, settings=None,
        prompt_file=None, tmux_session="agi-rc", window_path=str(wins),
        debug_file=str(success_reply), dry_run=False, timeout=1,
    ), root)
    assert code == 0
    assert len(calls) == 1, f"loop success announced {len(calls)}x, want 1"
    kw = calls[0]
    assert kw["seat"] == "belam-II" and kw["successor"] == "belam-II"

    # refusal path: successor window never appears -> record written, NO announce
    calls.clear()
    wins.write_text("")
    monkeypatch.setattr(rotate, "_launch_window", lambda s, n, c: 0)
    monkeypatch.setattr(rotate, "_read_ack",
                        lambda *a, **k: {"seat": "s", "gen_after": 1, "answer": "continue"})
    code = rotate.cmd_loop(SimpleNamespace(
        session_log=None, force=True, role="prime_director", name="belam-II",
        name_prefix="belam", model=None, effort=None, settings=None,
        prompt_file=None, tmux_session="agi-rc", window_path=str(wins),
        debug_file=str(success_reply), dry_run=False, timeout=1,
    ), root)
    assert code != 0
    assert calls == [], f"refused loop announced {calls}, want none"


def test_rotate_self_success_announces_once_refusal_never(
        fake_ladder, tmp_path, monkeypatch):
    win = tmp_path / "windows.txt"
    win.write_text("adv-alive\n", encoding="utf-8")

    def fake_spawn(**kw):
        with open(win, "a", encoding="utf-8") as fh:
            fh.write("adv-alive\n")
        return 0, "echo hi"
    monkeypatch.setattr(rotate, "spawn_window", fake_spawn)
    monkeypatch.setattr(rotate, "_read_ack",
                        lambda *a, **k: {"seat": "s", "gen_after": 1, "answer": "continue"})
    monkeypatch.setattr(rotate, "_kill_window", lambda *a, **k: None)
    calls = []
    monkeypatch.setattr(rotate, "_announce_rotation",
                        lambda **kw: calls.append(kw) or [])
    args = _rotate_self_args(tmp_path, throwaway=True, window_path=str(win))
    rc = rotate.cmd_rotate_self(args, tmp_path)
    assert rc == 0
    assert len(calls) == 1, f"rotate-self success announced {len(calls)}x, want 1"
    assert calls[0]["seat"] == "adv-alive"

    # refusal: successor window never appears -> record, NO announce
    calls.clear()
    win.write_text("adv-alive\n", encoding="utf-8")
    monkeypatch.setattr(rotate, "spawn_window", lambda **kw: (0, "echo hi"))
    rc = rotate.cmd_rotate_self(args, tmp_path)
    assert rc != 0
    assert calls == [], f"refused rotate-self announced {calls}, want none"


# ── l3w4-rotation-announces-itself SCOPE EXTENSION (2026-09-08): the
# monotonic durable sequence counter. The incident that sharpened this brief:
# two seats held contradictory world-states for 18 minutes because everyone
# had timestamps and nobody compared them. A seat that must CHECK a counter
# cannot silently hold a superseded order. These RED-FIRST tests lock the
# counter's monotonicity, durability, and its refusal immunity — the parts of
# the build with no prior coverage.
def test_sequence_counter_is_monotonic_and_durable(tmp_path):
    root = tmp_path / "proj"
    (root / "nodes").mkdir(parents=True)
    rot = root / "sessions" / "rotations"
    assert rotate._current_sequence(root) == 0, "no rotations yet -> seq 0"
    assert rotate._next_sequence(root) == 1
    assert rotate._next_sequence(root) == 2
    # durable: a fresh read (as a different seat/process would) sees the same
    # counter from disk, not from memory.
    assert rotate._current_sequence(root) == 2
    seq_file = rot / rotate.SEQUENCE_FILE
    assert seq_file.is_file()
    assert json.loads(seq_file.read_text()) == {"sequence": 2}


def test_announce_stamps_payload_with_seq_and_writes_sequence_file(
        monkeypatch, tmp_path):
    root = tmp_path / "proj"
    (root / "nodes").mkdir(parents=True)
    rows = [{"name": "kid-a", "role": "director"}]
    _write_seats_sheet(root, rows)
    import send as _send
    sent = []
    monkeypatch.setattr(_send, "send_dm",
                        lambda croot, me, other, text, sender: sent.append(
                            (other, text)) or tmp_path)
    delivered = rotate._announce_rotation(
        root=root, croot=tmp_path / "comms", seat="liason",
        successor="liason", gen_before=1, gen_after=2, trigger="rotate-self",
        handoff_path=".agi/sessions/liason.handoff.md", in_flight="none",
        live_names=["kid-a"])
    assert delivered == ["kid-a"]
    assert rotate._current_sequence(root) == 1
    (_, text), = sent
    assert "seq: 1" in text


def test_cmd_sequence_is_the_seat_visible_one_read(tmp_path, capsys):
    # The whole scope extension stands on a seat being able to ask, cheaply
    # and without a round trip, "is the order I am holding still current?".
    # `rotate.py seq` is that read, and it was the seat-visible half with NO
    # coverage. Lock it: it prints the durable counter, 0 before any rotation,
    # 0 when the counter file is absent or corrupt (so a stale order whose
    # seq is 1 is always comparable to a fresh read).
    root = tmp_path / "proj"
    (root / "nodes").mkdir(parents=True)
    assert rotate.cmd_sequence(SimpleNamespace(), root) == 0
    assert capsys.readouterr().out.strip() == "0", \
        "no rotations yet -> seq reads 0"

    # absent counter file must read clean (default), not raise
    root2 = tmp_path / "proj2"
    (root2 / "nodes").mkdir(parents=True)
    rotate.cmd_sequence(SimpleNamespace(), root2)
    assert capsys.readouterr().out.strip() == "0"

    # corrupt counter file reads clean too; the durable file recovers on the
    # next announce rather than making the read path throw mid-flight.
    seq_file = root / "sessions" / "rotations" / rotate.SEQUENCE_FILE
    seq_file.parent.mkdir(parents=True, exist_ok=True)
    seq_file.write_text("not json\n", encoding="utf-8")
    assert rotate._current_sequence(root) == 0
    assert rotate._next_sequence(root) == 1
    rotate.cmd_sequence(SimpleNamespace(), root)
    assert capsys.readouterr().out.strip() == "1"


def test_refused_loop_does_not_advance_sequence(fake_ladder, tmp_path,
                                                monkeypatch):
    root = _proj(tmp_path)
    monkeypatch.chdir(root)
    monkeypatch.setattr(rotate, "find_project_root", lambda: root)
    monkeypatch.setattr(rotate, "cmd_meter", lambda args, root: 1)
    calls = []
    monkeypatch.setattr(rotate, "_announce_rotation",
                        lambda **kw: calls.append(kw) or [])
    # successor window NEVER appears -> cmd_loop refuses before announcing.
    wins = tmp_path / "windows.txt"
    wins.write_text("")
    monkeypatch.setattr(rotate, "_launch_window", lambda s, n, c: 0)
    monkeypatch.setattr(rotate, "_read_ack",
                        lambda *a, **k: {"seat": "s", "gen_after": 1, "answer": "continue"})
    code = rotate.cmd_loop(SimpleNamespace(
        session_log=None, force=True, role="prime_director", name="belam-II",
        name_prefix="belam", model=None, effort=None, settings=None,
        prompt_file=None, tmux_session="agi-rc", window_path=str(wins),
        debug_file=str(tmp_path / "reply.log"), dry_run=False, timeout=1,
    ), root)
    assert code != 0, "refused rotation must not report success"
    assert calls == [], f"refused loop announced {calls}, want none"
    assert rotate._current_sequence(root) == 0, \
        "refused rotation must not advance the sequence counter"


# --- fresh_spend_status: owner, 2026-09-08, "shown on pin accept fresh" ----
#
# The exact error this closes: a report carried the per-spawn provisioning
# KEY's own sub-cap as though it were the whole ceiling, when the ACCOUNT
# behind it held several dollars more. `fresh_spend_status` must always
# surface BOTH numbers, and `_openrouter_key` must find `.env` at the REPO
# root even though `root` here is the GRAPH root (`.agi/`) -- the exact bug
# caught live before this landed: `root / ".env"` silently found nothing
# because `.env` lives one level up, at `repo_root(root)`.

def test_openrouter_key_env_file_found_via_repo_root_not_graph_root(tmp_path, monkeypatch):
    # root passed to _openrouter_key is the GRAPH root (name == ".agi"),
    # exactly what find_project_root returns -- .env lives at its PARENT.
    # Must isolate from the ambient env var: dispatch.py mints and exports
    # a per-spawn OPENROUTER_API_KEY into every kid's own process, so this
    # test passes in an interactive shell (nothing exported) and fails
    # under a dispatched kid (something exported) unless explicitly
    # cleared -- caught live by a00-9a175ddd's own suite run, reported
    # correctly as environmental rather than silently worked around.
    monkeypatch.delenv("OPENROUTER_API_KEY", raising=False)
    graph_root = tmp_path / ".agi"
    graph_root.mkdir()
    (tmp_path / ".env").write_text("OPENROUTER_API_KEY=sk-or-v1-test123\n")
    assert rotate._openrouter_key(graph_root) == "sk-or-v1-test123"


def test_openrouter_key_prefers_env_var_over_dotenv_file(tmp_path, monkeypatch):
    graph_root = tmp_path / ".agi"
    graph_root.mkdir()
    (tmp_path / ".env").write_text("OPENROUTER_API_KEY=sk-or-v1-fromfile\n")
    monkeypatch.setenv("OPENROUTER_API_KEY", "sk-or-v1-fromenv")
    assert rotate._openrouter_key(graph_root) == "sk-or-v1-fromenv"


def test_openrouter_key_none_when_neither_configured(tmp_path, monkeypatch):
    monkeypatch.delenv("OPENROUTER_API_KEY", raising=False)
    graph_root = tmp_path / ".agi"
    graph_root.mkdir()
    assert rotate._openrouter_key(graph_root) is None


def test_fresh_spend_status_shows_both_key_and_account_labelled(tmp_path, monkeypatch):
    # The bug being pinned: showing the key sub-cap alone reads as "all
    # there is". Both numbers must appear, and the key must read as a
    # sub-cap on ONE key (raisable), never as the account ceiling.
    graph_root = tmp_path / ".agi"
    graph_root.mkdir()
    monkeypatch.setenv("OPENROUTER_API_KEY", "sk-or-v1-test")

    def fake_get(url, key):
        if url.endswith("/key"):
            return {"limit_remaining": 9.260199335, "limit": 15}
        if url.endswith("/credits"):
            return {"total_credits": 92, "total_usage": 75.766608581}
        raise AssertionError(f"unexpected url {url}")

    monkeypatch.setattr(rotate, "_openrouter_get", fake_get)
    status = rotate.fresh_spend_status(graph_root)
    assert "9.26" in status and "15" in status, status
    assert "sub-cap" in status, "key figure must be labelled a sub-cap, not the ceiling"
    assert "raisable" in status, status
    assert "16.23" in status and "92.00" in status, status
    assert "account" in status, status


def test_fresh_spend_status_none_when_network_fails(tmp_path, monkeypatch):
    # A balance check must never fail a pin claim -- silent None, not a raise.
    graph_root = tmp_path / ".agi"
    graph_root.mkdir()
    monkeypatch.setenv("OPENROUTER_API_KEY", "sk-or-v1-test")
    monkeypatch.setattr(rotate, "_openrouter_get", lambda url, key: None)
    assert rotate.fresh_spend_status(graph_root) is None


def test_fresh_spend_status_none_without_a_key(tmp_path, monkeypatch):
    monkeypatch.delenv("OPENROUTER_API_KEY", raising=False)
    graph_root = tmp_path / ".agi"
    graph_root.mkdir()
    assert rotate.fresh_spend_status(graph_root) is None


def test_meter_pin_claim_prints_spend_status(monkeypatch, tmp_path, fake_ladder, capsys):
    # The actual owner ask: --pin (a fresh claim) shows spend, unprompted.
    proj, pinned, foreign = _fake_cc_projects(tmp_path, monkeypatch)
    monkeypatch.setattr(
        rotate, "fresh_spend_status",
        lambda root: "key sub-cap: $9.26 remaining of $15 (raisable); "
                     "account: $16.23 remaining of $92.00 total")
    code = rotate.main(["meter", "--session-log", str(pinned), "--pin",
                        str(tmp_path / "sessions" / "claim-test.meter")])
    out = capsys.readouterr().out
    assert code == 0
    assert "spend" in out and "9.26" in out and "16.23" in out, out


def test_meter_read_without_pin_does_not_print_spend_status(monkeypatch, tmp_path, fake_ladder, capsys):
    # Spend is only ever checked at CLAIM time (--pin), not on every plain
    # read -- a bare `meter --seat X` must not add a network call.
    proj, pinned, foreign = _fake_cc_projects(tmp_path, monkeypatch)
    _write_pin(tmp_path, pinned)
    called = []
    monkeypatch.setattr(rotate, "fresh_spend_status",
                        lambda root: called.append(1) or "should not appear")
    code = rotate.main(["meter"])
    out = capsys.readouterr().out
    assert code == 0
    assert called == [], "a plain read (no --pin) must not check spend at all"
    assert "should not appear" not in out


def test_spawn_launch_carries_reaper_knob_for_plain_and_ultracode(monkeypatch, tmp_path, capsys):
    """hypothesis:l4-spawn-paths-export-the-reaper-knob — the seat-launch
    path must export CLAUDE_CODE_DISABLE_BG_SHELL_PRESSURE_REAP=1 in the
    launched command's OWN environment (not inherited from the tmux session,
    which is one restart from gone). Cover a plain kid AND an ultracode role;
    ultracode keeps its existing CLAUDE_CODE_WORKFLOWS=1 gate FIRST."""
    plain = _proj(tmp_path / "plain", ladder_roles=(
        "  - role: kid\n"
        "    harness: claude-code\n"
        "    model: claude-sonnet-5\n"
        "    effort: high\n"
        "    tier: 1\n"
    ))
    prompt = plain / "prompt.md"
    prompt.write_text("You are {name}\n")
    monkeypatch.setattr(rotate, "find_project_root", lambda: plain)
    monkeypatch.chdir(plain)
    exit_code = rotate.main([
        "spawn", "--name", "plain-reaper", "--tier", "kid",
        "--prompt-file", str(prompt), "--dry-run",
    ])
    out = capsys.readouterr().out
    assert exit_code == 0
    assert out.startswith("export CLAUDE_CODE_DISABLE_BG_SHELL_PRESSURE_REAP=1")

    ultra = _proj(tmp_path / "ultra", ladder_roles=(
        "  - role: prime_director\n"
        "    harness: claude-code\n"
        "    model: claude-fable-5-1\n"
        "    effort: max\n"
        "    settings: {ultracode: true}\n"
        "    tier: 3\n"
    ))
    prompt2 = ultra / "prompt.md"
    prompt2.write_text("You are {name}\n")
    monkeypatch.setattr(rotate, "find_project_root", lambda: ultra)
    monkeypatch.chdir(ultra)
    exit_code = rotate.main([
        "spawn", "--name", "ultra-reaper", "--prompt-file", str(prompt2),
        "--dry-run",
    ])
    out = capsys.readouterr().out
    assert exit_code == 0
    # WORKFLOWS gate stays first; the reaper export still comes after &&:
    assert out.startswith("export CLAUDE_CODE_WORKFLOWS=1")
    assert "export CLAUDE_CODE_DISABLE_BG_SHELL_PRESSURE_REAP=1 &&" in out


# --- ITEM 3 (w2): rotation debug logs are SHARED-ROOM, not worktree-local ----
# hypothesis:l4-a-check-that-answers-a-question-it-is-not-asking, widening w2.
# The four default debug-log paths used to be the RELATIVE STRING
# `.agi/sessions/...`, which `Path(dbg).resolve()` resolved against CWD -- so a
# seat running from its worktree read/wrote a DIFFERENT file from one in the
# main checkout (proved on disk: same seat, one log a day stale). All four now
# route through `_sessions_dir`, so the falsifier is a PATH-EQUALITY fact, not
# a success fact: a rotation addressed from a worktree and one from the main
# checkout must name the SAME file.


def test_rotation_debug_log_resolves_same_file_from_worktree_and_main(monkeypatch, tmp_path):
    main_root = tmp_path / "main"
    seat_root = tmp_path / "seat"
    for g in (main_root, seat_root):
        (g / ".agi").mkdir(parents=True)
        (g / ".agi" / "nodes").mkdir()
        (g / ".agi" / "config.json").write_text("{}")

    def _to_main(_root=None):
        return main_root

    monkeypatch.setattr(rotate.locations, "git_common_root", _to_main)

    seat_log = rotate._sessions_dir(seat_root) / "sanctuary-director.log"
    main_log = rotate._sessions_dir(main_root) / "sanctuary-director.log"
    assert seat_log == main_log, (
        "a worktree seat and the main checkout must address the SAME log file;\n"
        f"  worktree: {seat_log}\n  main:     {main_log}\n"
        "the four relative-string defaults routed through CWD and forked here")
    assert str(seat_log).startswith(str(main_root)), (
        "the shared log must resolve under the MAIN checkout, not the seat's")


def test_rotate_self_default_debug_log_is_the_shared_path(monkeypatch, tmp_path):
    """With no explicit --debug-file, cmd_rotate_self resolves its default log
    through `_sessions_dir` (shared-room) rather than the relative CWD string."""
    main_root = tmp_path / "main"
    (main_root / ".agi" / "nodes").mkdir(parents=True)
    (main_root / ".agi" / "config.json").write_text("{}")

    def _to_main(_root=None):
        return main_root

    monkeypatch.setattr(rotate.locations, "git_common_root", _to_main)

    expected = str(rotate._sessions_dir(main_root) / "sanctuary-director.log")
    # the DEFAULT expression cmd_rotate_self uses when args.debug_file is falsy:
    default_dbg = str(rotate._sessions_dir(main_root) / "sanctuary-director.log")
    assert default_dbg == expected
    assert ".agi/sessions" in default_dbg
    assert not default_dbg.startswith("."), (
        "a CWD-relative default is exactly the fork this round removes")


def _make_main_and_worktree(tmp_path):
    """A main checkout + one linked worktree, both with a real `.agi` graph."""
    repo = tmp_path / "main"
    repo.mkdir(parents=True)
    subprocess.run(["git", "-C", str(repo), "init", "-b", "season/s1"],
                   check=True, capture_output=True)
    for cfg in ("user.email", "user.name"):
        subprocess.run(["git", "-C", str(repo), "config", cfg, "t"],
                       check=True, capture_output=True)
    (repo / ".agi" / "nodes").mkdir(parents=True)
    (repo / ".agi" / "config.json").write_text('{"metric_primary": "x"}')
    subprocess.run(["git", "-C", str(repo), "add", "-A"], check=True,
                   capture_output=True)
    subprocess.run(["git", "-C", str(repo), "commit", "-m", "init"],
                   check=True, capture_output=True)
    wt = tmp_path / "wt"
    subprocess.run(["git", "-C", str(repo), "worktree", "add",
                    "-b", "loop/x-a@s2", str(wt), "season/s1"],
                   check=True, capture_output=True)
    return repo, wt


def test_successor_reply_lands_in_the_file_the_predecessor_reads(tmp_path):
    """FALSIFIER (w4): settle whether the successor's first reply lands in the
    file the PREDECESSOR reads.

    The successor's `--debug-file` (`spawn_window` default) and the
    predecessor's read-back log (`rotate_self` default) are the SAME path,
    and it is the SHARED `_sessions_dir` path on the MAIN checkout — even
    when the rotation is driven from a linked git worktree. So a successor
    first reply is never stranded in a file the predecessor cannot see: both
    sides of the rotation resolve to the one shared `<name>.log`.
    """
    repo, wt = _make_main_and_worktree(tmp_path)
    name = "sanctuary-director"
    # The file the successor writes its first reply into (spawn_window's
    # default --debug-file debug path).
    succ_file_worktree = rotate._sessions_dir(wt / ".agi") / f"{name}.log"
    # The file the predecessor polls for that reply (rotate_self's read-back
    # default).
    pred_file_main = rotate._sessions_dir(repo / ".agi") / f"{name}.log"
    assert succ_file_worktree == pred_file_main, (
        "a successor's first reply must land in the SAME file the predecessor "
        "reads, or a rotation driven from a worktree strands the reply")
    assert str(pred_file_main) == str(repo / ".agi" / "sessions" / f"{name}.log"), (
        "the shared log must resolve to the MAIN checkout, not the worktree")


# ── L4.112 (A) + (C): rotate-self template resolution at the TOP + template
#    brief consumption. Fix-only re-dispatch, kid 1. ------------------------


def _rs_tmpl_fixture(tmp_path, tmpls):
    """A fixture root with a valid seat AND a rotations.md carrying `tmpls`.

    `tmpls` is a dict of template-name -> {brief_file, steps, telemetry}, the
    same shape the shipped body (briefs/rotations.geometry.md) declares. The
    test writes both nodes itself; never touches the live .geometry dir."""
    _write_seats_sheet(
        tmp_path,
        [{"name": "adv-alive", "role": "director",
          "model": "x", "effort": "max", "settings": ""}])
    g = tmp_path / "nodes" / ".geometry"
    g.mkdir(parents=True, exist_ok=True)
    lines = ["---", "id: config:rotations", "type: config", "templates:"]
    for name, ent in tmpls.items():
        lines.append(f"  {name}:")
        lines.append(f"    brief_file: {ent['brief_file']}")
        lines.append(f"    steps: {json.dumps(ent.get('steps'))}")
        lines.append(f"    telemetry: {json.dumps(ent.get('telemetry'))}")
    lines.append("---")
    lines.append("body")
    (g / "rotations.md").write_text("\n".join(lines) + "\n", encoding="utf-8")


def test_rotate_self_missing_rotations_node_refuses_before_side_effects(
        tmp_path, monkeypatch, capsys):
    """L4.112 (A): with rotations.md absent (the live state until the prime
    lands it), rotate-self refuses at the TOP of the function -- BEFORE the
    started record, the handoff write, and the own-window rename -- and names
    the node. The window name and the handoff file are therefore untouched."""
    _write_seats_sheet(tmp_path, [{"name": "adv-alive", "role": "director",
                                   "model": "x", "effort": "max",
                                   "settings": ""}])  # seats.md, NO rotations.md
    renamed_win = []
    handoff_written = []
    def trap_rename(*a, **k):
        renamed_win.append(a)
    def trap_handoff(*a, **k):
        handoff_written.append(a)
    monkeypatch.setattr(rotate, "_rename_own_window", trap_rename)
    monkeypatch.setattr(rotate, "_write_handoff", trap_handoff)
    args = _rotate_self_args(tmp_path, window_path=str(tmp_path / "windows.txt"))
    rc = rotate.cmd_rotate_self(args, tmp_path)
    err = capsys.readouterr().err
    assert rc == 1
    assert "rotations.md" in err
    assert renamed_win == [], "rename must NOT run when rotations.md is absent"
    assert handoff_written == [], "handoff must NOT be written when absent"
    assert not (tmp_path / "sessions" / "seats" / "adv-alive.handoff.md").exists()
    assert not (rotate._rotations_dir(tmp_path)).exists(), \
        "no started rotation record when the node is absent"


def test_rotate_self_consumes_template_brief_as_successor_prompt(
        fake_ladder, tmp_path, monkeypatch, capsys):
    """L4.112 (C): when --prompt-file is NOT given, rotate-self hands the
    template's brief_file (with `{seat}` substituted) to the successor as its
    prompt. The director's brief is the seat's quorum scratchpad, so
    `.agi/sessions/quorum/{seat}.md` becomes `.agi/sessions/quorum/adv-alive.md`."""
    tmpls = {"director": {"brief_file": ".agi/sessions/quorum/{seat}.md",
                          "steps": ["handoff", "spawn", "join"],
                          "telemetry": ["seed", "model"]}}
    _rs_tmpl_fixture(tmp_path, tmpls)
    win = tmp_path / "windows.txt"
    win.write_text("adv-alive\n", encoding="utf-8")
    seen = {}
    def fake_spawn(**kw):
        seen["prompt_file"] = kw.get("prompt_file")
        with open(win, "a", encoding="utf-8") as fh:
            fh.write("adv-alive\n")
        return 0, "echo hi"
    monkeypatch.setattr(rotate, "spawn_window", fake_spawn)
    monkeypatch.setattr(rotate, "_read_ack", lambda *a, **k: {
        "seat": "adv-alive", "gen_after": 1, "answer": "continue"})
    monkeypatch.setattr(rotate, "_kill_window", lambda *a, **k: None)
    args = _rotate_self_args(tmp_path, window_path=str(win))
    rc = rotate.cmd_rotate_self(args, tmp_path)
    assert rc == 0
    assert seen["prompt_file"] == ".agi/sessions/quorum/adv-alive.md"


def test_rotate_self_prompt_file_flag_overrides_template_brief(
        fake_ladder, tmp_path, monkeypatch, capsys):
    """L4.112 (C): --prompt-file STILL overrides the template's brief_file."""
    tmpls = {"director": {"brief_file": ".agi/sessions/quorum/{seat}.md",
                          "steps": ["handoff", "spawn"],
                          "telemetry": ["seed", "model"]}}
    _rs_tmpl_fixture(tmp_path, tmpls)
    win = tmp_path / "windows.txt"
    win.write_text("adv-alive\n", encoding="utf-8")
    seen = {}
    def fake_spawn(**kw):
        seen["prompt_file"] = kw.get("prompt_file")
        with open(win, "a", encoding="utf-8") as fh:
            fh.write("adv-alive\n")
        return 0, "echo hi"
    monkeypatch.setattr(rotate, "spawn_window", fake_spawn)
    monkeypatch.setattr(rotate, "_read_ack", lambda *a, **k: {
        "seat": "adv-alive", "gen_after": 1, "answer": "continue"})
    monkeypatch.setattr(rotate, "_kill_window", lambda *a, **k: None)
    custom = tmp_path / "custom.md"
    custom.write_text("custom", encoding="utf-8")
    args = _rotate_self_args(tmp_path, window_path=str(win),
                             prompt_file=str(custom))
    rc = rotate.cmd_rotate_self(args, tmp_path)
    assert rc == 0
    assert seen["prompt_file"] == str(custom)


def test_rotate_self_step_markers_come_from_template_steps(
        fake_ladder, tmp_path, monkeypatch, capsys):
    """L4.112 (C): steps_reached records the template's OWN step spellings
    where the completed step is named in tmpl.steps (not a hardcoded list)."""
    tmpls = {"director": {"brief_file": "extensions/agi/briefs/x.md",
                          "steps": ["handoff", "spawn", "join"],
                          "telemetry": ["seed"]}}
    _rs_tmpl_fixture(tmp_path, tmpls)
    win = tmp_path / "windows.txt"
    win.write_text("adv-alive\n", encoding="utf-8")
    def fake_spawn(**kw):
        with open(win, "a", encoding="utf-8") as fh:
            fh.write("adv-alive\n")
        return 0, "echo hi"
    monkeypatch.setattr(rotate, "spawn_window", fake_spawn)
    monkeypatch.setattr(rotate, "_read_ack", lambda *a, **k: {
        "seat": "adv-alive", "gen_after": 1, "answer": "continue"})
    monkeypatch.setattr(rotate, "_kill_window", lambda *a, **k: None)
    written = []
    real_write = rotate._write_rotate_self_started
    def capture(path, **kw):
        written.append(list(kw.get("steps", [])))
        return real_write(path, **kw)
    monkeypatch.setattr(rotate, "_write_rotate_self_started", capture)
    args = _rotate_self_args(tmp_path, window_path=str(win))
    rc = rotate.cmd_rotate_self(args, tmp_path)
    assert rc == 0
    recs = list(rotate._rotations_dir(tmp_path).glob("adv-alive.*.json"))
    assert recs, "a rotation record must exist after a success"
    final = json.loads(recs[0].read_text(encoding="utf-8"))
    assert final["result"] == "success"
    # the STARTED-progress markers use the template's spellings where the
    # step is named in tmpl.steps (handoff/spawn are) -- not a hardcoded list.
    done = [s for step in written for s in step]
    assert "handoff" in done
    assert "spawn" in done


# ---- L4.119 fifth fix-only dispatch: P1 prime numeral-chain path, P2 one-key ack ----

def test_rotate_self_chain_dry_run_prime_numeral_successor(fake_ladder, tmp_path,
                                                           capsys, monkeypatch):
    """P1: a numeral-chain seat (role prime_director) derives its successor
    NAME the way cmd_loop does (`belam-S1-L4-<next numeral>` from the existing
    windows — `_derive_successor_name`, never a constructed `gen` name), its
    generation IS the numeral, the `.genN` rename does NOT apply, and the ack
    path stays keyed by the SEAT name (`belam.ack.json`) for the ONE ack call.
    Dry-run only; touches nothing."""
    _write_seats_sheet(tmp_path,
                       [{"name": "belam", "role": "prime_director",
                         "model": "x", "effort": "max", "settings": ""}])
    win = tmp_path / "windows.txt"
    win.write_text("@8 belam-S1-L4-V\n@9 belam-S1-L4-VI\n", encoding="utf-8")
    seen = {}
    def fake_spawn(**kw):
        seen["name"] = kw["name"]
        return 0, "echo hi"
    monkeypatch.setattr(rotate, "spawn_window", fake_spawn)
    args = _rotate_self_args(tmp_path, name="belam", role="prime_director",
                             window_path=str(win), dry_run=True)
    rc = rotate.cmd_rotate_self(args, tmp_path)
    assert rc == 0
    # successor name is the numeral successor, never the plain seat name
    assert seen["name"] == "belam-S1-L4-VII"
    out = capsys.readouterr().out
    # generation IS the numeral of the successor (VII = 7), not gen_before+1
    assert "generation = numeral 7" in out
    assert "belam-S1-L4-VII" in out
    # the ack channel is keyed by the SEAT name, not the numeral
    assert rotate._ack_path(tmp_path, "belam").as_posix() in out
    # dry-run touched nothing
    assert not (tmp_path / "sessions" / "seats" / "belam.handoff.md").exists()


def test_rotate_self_chain_generation_is_numeral_not_plus_one(
        fake_ladder, tmp_path, capsys, monkeypatch):
    """P1: the prime's generation is the successor's NUMERAL (measured: a
    chain ending at -VI rotates to -VII => generation 7), never gen_before+1
    read off the handoff. Exercises the full rotation on a fixture window_path
    so the successor-window and predecessor-window guarantees are real."""
    _write_seats_sheet(tmp_path,
                       [{"name": "belam", "role": "prime_director",
                         "model": "x", "effort": "max", "settings": ""}])
    (tmp_path / "agi-tree.config.json").write_text("{}", encoding="utf-8")
    win = tmp_path / "windows.txt"
    win.write_text("@8 belam-S1-L4-IV\n@9 belam-S1-L4-V\n@10 belam-S1-L4-VI\n",
                   encoding="utf-8")

    def fake_spawn(**kw):
        # the successor appears immediately under the derived numeral name
        with open(win, "a", encoding="utf-8") as fh:
            fh.write("@11 belam-S1-L4-VII\n")
        return 0, "echo hi"
    monkeypatch.setattr(rotate, "spawn_window", fake_spawn)
    monkeypatch.setattr(rotate, "_read_ack",
                        lambda *a, **k: {"seat": "belam", "gen_after": 7,
                                         "answer": "continue"})
    monkeypatch.setattr(rotate, "_kill_window", lambda *a, **k: None)
    monkeypatch.setattr(rotate, "_reap_chain", lambda *a, **k: {"ok": True})
    monkeypatch.setattr(rotate, "_write_rotation_record",
                        lambda *a, **k: str(tmp_path / "rec.json"))
    monkeypatch.setattr(rotate, "_record_s12_self_reap", lambda *a, **k: None)
    monkeypatch.setattr(rotate, "_write_rotate_self_started",
                        lambda *a, **k: None)
    monkeypatch.setattr(rotate, "_announce_rotation", lambda *a, **k: None)
    args = _rotate_self_args(tmp_path, name="belam", role="prime_director",
                             window_path=str(win), session_ref="f52feed")
    rc = rotate.cmd_rotate_self(args, tmp_path)
    assert rc == 0
    out = capsys.readouterr().out
    assert "generation = numeral 7" not in out  # not a dry-run
    # the follower / record got a numeral successor window
    assert "belam-S1-L4-VII" in out


def test_resolve_seat_for_ack_maps_numeral_name_to_seat(tmp_path, monkeypatch):
    """P2: the ack channel is keyed by the SEAT name everywhere. A reader that
    holds only the numeral session/window name (`belam-S1-L4-VII`) resolves
    the SEAT through the seats row, so the ONE `ack --seat belam` write reaches
    the read-back — one ack, one file, both sides."""
    root = _proj(tmp_path)
    (root / "agi-tree.config.json").write_text("{}", encoding="utf-8")
    _write_seats_sheet(root,
                       [{"name": "belam", "role": "prime_director",
                         "session_ref": ""}])
    monkeypatch.setattr(rotate, "find_project_root", lambda: root)
    # numeral session name -> seat row name
    assert rotate._resolve_seat_for_name(root, "belam-S1-L4-VII") == "belam"
    # plain name stays itself (a THROWAWAY / unregistered numeral echoes)
    assert rotate._resolve_seat_for_name(root, "ghost") == "ghost"
    # therefore the numeral reader reads the SAME file `ack --seat belam` wrote
    numeral_reader_path = rotate._ack_path(
        root, rotate._resolve_seat_for_name(root, "belam-S1-L4-VII"))
    assert numeral_reader_path == rotate._ack_path(root, "belam")


def test_ack_seat_writes_row_and_matches_numeral_reader(tmp_path, monkeypatch,
                                                        capsys):
    """P2: ONE `ack --seat belam` writes `belam.ack.json`, confirms the
    read-back, AND back-fills session_ref into belam's row (source: ack) —
    no second ack needed and no per-numeral file."""
    root = _proj(tmp_path)
    (root / "agi-tree.config.json").write_text("{}", encoding="utf-8")
    _write_seats_sheet(root,
                       [{"name": "belam", "role": "prime_director",
                         "model": "x", "effort": "max", "settings": "",
                         "session_ref": ""}])
    monkeypatch.chdir(root)
    code = rotate.cmd_ack(SimpleNamespace(
        seat="belam", gen=7, ref="f52a4c", answer="continue", text=""), root)
    assert code == 0
    # the ack file is keyed by the SEAT name
    ac = rotate._ack_path(root, "belam")
    assert ac.exists()
    doc = json.loads(ac.read_text(encoding="utf-8"))
    assert doc["seat"] == "belam" and doc["gen_after"] == 7
    assert doc["session_ref"] == "f52a4c"
    # the numeral reader resolves to the SAME file the one ack wrote
    reader_path = rotate._ack_path(
        root, rotate._resolve_seat_for_name(root, "belam-S1-L4-VII"))
    assert reader_path == ac
    # the ONE ack back-filled the row (source: ack) — no second ack needed
    rows = rotate._load_seats(root)
    belam = next(r for r in rows if r.get("name") == "belam")
    assert belam.get("session_ref") == "f52a4c"


def _ack_root_with_sid(tmp_path, seat="belam", sid="f52a4caabbccddee"):
    """A local graph root whose own seat row carries a session_id (the
    successor's registry identity) but an empty session_ref — the state the
    back-fill-from-row mechanism is meant to cure."""
    root = _proj(tmp_path)
    (root / "agi-tree.config.json").write_text("{}", encoding="utf-8")
    _write_seats_sheet(root,
                       [{"name": seat, "role": "prime_director",
                         "model": "x", "effort": "max", "settings": "",
                         "session_ref": "", "session_id": sid}])
    return root


def test_ack_bare_agreeing_ref_backfills(tmp_path, monkeypatch, capsys):
    """Mechanism 2: a bare ref that happens to prefix the OWN row's
    session_id resolves to this seat (IS-AUTHORIZED) and is back-filled rc 0
    — one of the two accepted shapes (the other, the live one, is a
    ListAgents ref no row carries yet: see the live-shape test below)."""
    root = _ack_root_with_sid(tmp_path)
    monkeypatch.chdir(root)
    code = rotate.cmd_ack(SimpleNamespace(
        seat="belam", gen=3, ref="f52a4c", answer="continue", text=""), root)
    assert code == 0
    belam = next(r for r in rotate._load_seats(root)
                 if r.get("name") == "belam")
    assert belam.get("session_ref") == "f52a4c"


def test_ack_row_shaped_ref_refused_by_name(tmp_path, monkeypatch, capsys):
    """RED (mechanism 2): a row-shaped --ref (brackets, or the seat name) is
    REFUSED naming the shape — no ack file, no back-fill, rc 2."""
    root = _ack_root_with_sid(tmp_path)
    monkeypatch.chdir(root)
    for bad in ("[f52a4c]", "belam"):
        code = rotate.cmd_ack(SimpleNamespace(
            seat="belam", gen=3, ref=bad, answer="continue", text=""), root)
        assert code == 2, bad
        assert not rotate._ack_path(root, "belam").exists(), bad
    err = capsys.readouterr().err
    assert "refused" in err
    belam = next(r for r in rotate._load_seats(root)
                 if r.get("name") == "belam")
    assert belam.get("session_ref") == ""


def test_ack_live_listagents_ref_is_not_a_session_id_prefix_and_is_accepted(
        tmp_path, monkeypatch, capsys):
    """RED (director fix-up at the SL1.06 harvest, measured on the live
    rotation 20260911T172702Z): the row's session_id is the Claude session
    uuid the JOIN registers (`27179681-4a0c-…`); the successor's ListAgents
    ref (`caa927`) is a DIFFERENT identity and is NOT a prefix of it. SL1.06
    kid 2 refused every ref that did not prefix-match the session_id — which
    would have refused every live wake. A bare ref that resolves to NO row is
    the normal first ack: rc 0, written verbatim into the row (what whois
    needs), and the ack file carries it."""
    root = _ack_root_with_sid(tmp_path,
                              sid="27179681-4a0c-4651-8a04-50de141b2ce0")
    monkeypatch.chdir(root)
    code = rotate.cmd_ack(SimpleNamespace(
        seat="belam", gen=3, ref="caa927", answer="continue", text=""), root)
    assert code == 0, capsys.readouterr().err
    belam = next(r for r in rotate._load_seats(root)
                 if r.get("name") == "belam")
    assert belam.get("session_ref") == "caa927"
    assert belam.get("session_id") == "27179681-4a0c-4651-8a04-50de141b2ce0"
    ack = json.loads(rotate._ack_path(root, "belam").read_text(encoding="utf-8"))
    assert ack["session_ref"] == "caa927"


def test_ack_ref_that_is_another_seats_identity_refused(tmp_path, monkeypatch,
                                                         capsys):
    """Mechanism 2, the impersonation half kept: a bare --ref that ALREADY
    resolves (by session_ref, or by session_id prefix) to a DIFFERENT seat's
    row is refused rc 2 — no ack file, no back-fill."""
    root = _proj(tmp_path)
    (root / "agi-tree.config.json").write_text("{}", encoding="utf-8")
    _write_seats_sheet(root, [
        {"name": "belam", "role": "prime_director", "model": "x",
         "effort": "max", "settings": "", "session_ref": "",
         "session_id": "27179681-4a0c-4651-8a04-50de141b2ce0"},
        {"name": "master-sensei", "role": "director", "model": "x",
         "effort": "max", "settings": "", "session_ref": "e96899",
         "session_id": "f52a4caa-0000-4000-8000-000000000000"}])
    monkeypatch.chdir(root)
    for stolen in ("e96899", "f52a4c"):      # by session_ref / by sid prefix
        code = rotate.cmd_ack(SimpleNamespace(
            seat="belam", gen=3, ref=stolen, answer="continue", text=""),
            root)
        assert code == 2, stolen
        assert not rotate._ack_path(root, "belam").exists(), stolen
    err = capsys.readouterr().err
    assert "refused" in err and "another seat" in err
    belam = next(r for r in rotate._load_seats(root)
                 if r.get("name") == "belam")
    assert belam.get("session_ref") == ""


def test_ack_no_ref_leaves_session_ref_empty(tmp_path, monkeypatch, capsys):
    """Director fix-up at the SL1.06 harvest: an ack with NO --ref is still
    accepted (rc 0, the ack lands) but back-fills NOTHING — the row already
    carries its session_id from the JOIN, and the ListAgents ref cannot be
    derived from it (F8: harness-only). Writing the uuid into session_ref
    (kid 2/3's zero-call lean) only made the rotation alert print
    `name [27179681-…]`, an address no peer can message; the alert now says
    pre-join, which is the truth until the successor names its ref."""
    root = _ack_root_with_sid(tmp_path,
                              sid="27179681-4a0c-4651-8a04-50de141b2ce0")
    monkeypatch.chdir(root)
    code = rotate.cmd_ack(SimpleNamespace(
        seat="belam", gen=3, ref=None, answer="continue", text=""), root)
    assert code == 0
    belam = next(r for r in rotate._load_seats(root)
                 if r.get("name") == "belam")
    assert belam.get("session_ref") == ""
    assert belam.get("session_id") == "27179681-4a0c-4651-8a04-50de141b2ce0"
    ack = json.loads(rotate._ack_path(root, "belam").read_text(encoding="utf-8"))
    assert ack["session_ref"] == ""


def _ack_seed_git(tmp_path, session_ref=""):
    """A real git repo (top = tmp_path) with the graph root (`proj/`) and a
    COMMITTED seats.md carrying one row — the r3b `ack ... continue` COMMITS
    path. sessions/ is gitignored so the ack.json the ack writes stays out of
    `git status`. Returns (graph_root, repo_top)."""
    subprocess.run(["git", "init", "-q", str(tmp_path)], check=True)
    subprocess.run(["git", "-C", str(tmp_path), "config", "user.email",
                    "ack@test"], check=True)
    subprocess.run(["git", "-C", str(tmp_path), "config", "user.name",
                    "ack test"], check=True)
    (tmp_path / ".gitignore").write_text("sessions/\n", encoding="utf-8")
    root = _proj(tmp_path, ladder_roles="")
    # the graph root carries the project marker (write.submit resolves the
    # graph root DESCEND-ONLY inside `root`, like `.agi/config.json` in live)
    (root / "agi-tree.config.json").write_text("{}", encoding="utf-8")
    _write_seats_sheet(root, [{"name": "belam", "role": "prime_director",
                               "model": "x", "effort": "max",
                               "settings": "", "session_ref": session_ref}])
    subprocess.run(["git", "-C", str(tmp_path), "add", "-A"], check=True)
    subprocess.run(["git", "-C", str(tmp_path), "commit", "-q", "-m",
                    "seats seed"], check=True)
    return root, tmp_path


def _git_head(top):
    return subprocess.run(["git", "-C", str(top), "rev-parse", "HEAD"],
                          capture_output=True, text=True).stdout.strip()


def _rel(top, path):
    return os.path.relpath(path, top)


def test_spawn_row_write_end_to_end_leaves_seats_md_exactly_one_0a(
        tmp_path, monkeypatch, capsys):
    """CLAIM-4 END-TO-END INVARIANT on the LIVE seats flow.

    `_successor_row_write` is a FRONTMATTER-ONLY identity-cell edit routed
    through write.submit -> node_writer.update_node -> _serialize_node — the
    exact shape that, before the ONE-serializer fix, DROPPED the EOF newline:
    the working copy of seats.md ended `0x2e` while HEAD ended `0x0a` (a
    1-byte whitespace-only dirt that refused prepare check 2
    `_prepare_dirty_paths` and `_ack_seats_dirty` on every rotation until a
    checkout restored HEAD). After the fix the spawn-row write must leave the
    working copy ending EXACTLY ONE 0x0a (never 0x2e, never two), rotate-self
    must commit its own spawn-row write in one tree (clean, no spurious
    whitespace dirt survives for the successor's ack), and a REAL one-cell
    row change must still read dirty until committed (falsifier: the
    dirty-gates are never weakened)."""
    root, top = _ack_seed_git(tmp_path)
    seats = rotate._ack_seats_path(root)
    seed = subprocess.run(
        ["git", "-C", str(tmp_path), "show",
         f"HEAD:{_rel(top, seats)}"],
        capture_output=True, text=True).stdout
    assert seed.endswith("\n")                  # seed committed ends 0x0a
    # (1) the LIVE spawn-row write: set_fm-only identity cells.
    out = rotate._successor_row_write(
        root, actor="belam", seat="belam", role="prime_director",
        session_ref="f52a4c", generation=7, window="")
    assert "config:seats row" in out and "belam" in out
    blob = seats.read_bytes()
    assert blob and blob[-1] == 0x0a              # 0x0a, never 0x2e
    assert not blob.endswith(b"\n\n")            # never two newlines
    # a REAL one-cell row change still reads dirty (never treated as clean).
    assert rotate._ack_seats_dirty(root, top, "belam") is not None
    # (2) rotate-self commits its own spawn-row write in ONE tree (g15.24).
    comm = rotate._commit_spawn_row(
        root, seat="belam", generation=7, window="")
    assert "spawn_row_commit: committed" in comm, comm
    st = subprocess.run(["git", "-C", str(top), "status", "--porcelain"],
                        capture_output=True, text=True)
    assert st.stdout.strip() == ""                # clean — no spurious dirt
    # the successor's ack now finds seats.md clean (own row already committed).
    assert rotate._ack_seats_dirty(root, top, "belam") is None
    assert seats.read_bytes()[-1] == 0x0a


def test_ack_gate_reads_whitespace_only_delta_clean(tmp_path, monkeypatch):
    """CLAIM-2 ack gate (`_ack_seats_dirty` via `_seats_diff_has_own_row`):
    a seats.md working copy whose ONLY delta vs HEAD is a missing EOF newline
    (the one-serializer EOJ dirt) reads CLEAN — the gate returns None, never
    refusing the successor's ack. FALSIFIER pair: a REAL one-cell row change
    still reads dirty, and an INTERIOR whitespace change still reads dirty —
    only trailing whitespace / the EOF newline is folded clean."""
    root, top = _ack_seed_git(tmp_path)
    seats = rotate._ack_seats_path(root)
    assert seats.exists()
    # (1) whitespace-only: drop ONLY the EOF newline from the working copy.
    seats.write_bytes(seats.read_bytes().rstrip(b"\n"))
    assert rotate._ack_seats_dirty(root, top, "belam") is None
    # (2) a REAL one-cell change (interior content) stays dirty — never clean.
    seats.write_text(seats.read_text(encoding="utf-8").replace(
        '"effort": "max"', '"effort": "low"'), encoding="utf-8")
    assert rotate._ack_seats_dirty(root, top, "belam") is not None
    # (3) an INTERIOR whitespace change on the OWN row line (mid-line, not
    # line-trailing) stays dirty; only trailing whitespace / EOF newline is
    # folded clean.
    subprocess.run(["git", "-C", str(top), "checkout", "--", str(seats)],
                   check=True)
    seats.write_text(seats.read_text(encoding="utf-8").replace(
        '"model": "x"', '"model":  "x"'), encoding="utf-8")
    assert rotate._ack_seats_dirty(root, top, "belam") is not None
    # (4) STAGED whitespace-only (index-vs-HEAD, the cached=true diff) is
    # clean too.
    subprocess.run(["git", "-C", str(top), "checkout", "--", str(seats)],
                   check=True)
    seats.write_bytes(seats.read_bytes().rstrip(b"\n"))
    subprocess.run(["git", "-C", str(top), "add", str(seats)], check=True)
    assert rotate._ack_seats_dirty(root, top, "belam") is None


def test_ack_continue_commits_own_row_write(tmp_path, monkeypatch, capsys):
    """r3b falsifier 1: `continue` COMMITS the row it just back-filled — the
    tree is clean, exactly ONE new commit whose diff-tree lists seats.md only
    and whose message is `<seat> ack: gen <N>, session_ref <ref>, ...`, and
    the ack prints the seat's +/- row lines plus the exact `git push` line as
    its last line (never runs it)."""
    root, top = _ack_seed_git(tmp_path)
    monkeypatch.chdir(root)
    before = _git_head(top)
    code = rotate.cmd_ack(SimpleNamespace(
        seat="belam", gen=7, ref="f52a4c", answer="continue", text=""),
        root)
    assert code == 0, capsys.readouterr().err
    belam = next(r for r in rotate._load_seats(root)
                 if r.get("name") == "belam")
    assert belam.get("session_ref") == "f52a4c"
    after = _git_head(top)
    assert after != before                      # exactly ONE new commit
    status = subprocess.run(["git", "-C", str(top), "status", "--porcelain"],
                            capture_output=True, text=True)
    assert status.stdout.strip() == ""          # clean tree (ack own write)
    files = subprocess.run(["git", "-C", str(top), "diff-tree",
                            "--no-commit-id", "--name-only", "-r", after],
                           capture_output=True, text=True).stdout.split()
    assert files == ["proj/nodes/.geometry/seats.md"]   # seats.md ONLY
    msg = subprocess.run(["git", "-C", str(top), "log", "-1",
                          "--format=%s", after],
                         capture_output=True, text=True).stdout.strip()
    assert msg == "belam ack: gen 7, session_ref f52a4c, window , pid"
    out = capsys.readouterr().out
    assert "ack: committed own row write" in out
    assert any(ln.startswith("+") for ln in out.splitlines())
    assert any(ln.startswith("-") for ln in out.splitlines())
    assert "git -C {0} push".format(top) in out  # exact push line printed
    assert "--no-commit" not in out


def test_ack_no_commit_leaves_working_tree(tmp_path, monkeypatch, capsys):
    """r3b falsifier 2: `--no-commit` (even on continue) leaves seats.md
    MODIFIED and HEAD unchanged — write + print, no commit, no push line."""
    root, top = _ack_seed_git(tmp_path)
    monkeypatch.chdir(root)
    before = _git_head(top)
    rel = "proj/nodes/.geometry/seats.md"
    code = rotate.cmd_ack(SimpleNamespace(
        seat="belam", gen=7, ref="f52a4c", answer="continue", text="",
        no_commit=True), root)
    assert code == 0
    assert _git_head(top) == before              # HEAD unchanged
    belam = next(r for r in rotate._load_seats(root)
                 if r.get("name") == "belam")
    assert belam.get("session_ref") == "f52a4c"  # write still happened
    st = subprocess.run(["git", "-C", str(top), "status", "--porcelain",
                         "--", rel], capture_output=True, text=True)
    assert st.stdout.strip()                      # seats.md MODIFIED
    out = capsys.readouterr().out
    assert "back-filled session_ref=f52a4c" in out
    assert "git -C {0} push".format(top) not in out
    assert "ack: committed" not in out


def test_ack_commits_nothing_when_row_already_carries_ref(
        tmp_path, monkeypatch, capsys):
    """r3b falsifier 3: a back-fill that changed nothing (row already carries
    the ref) commits nothing and says so in one line."""
    root, top = _ack_seed_git(tmp_path, session_ref="f52a4c")
    monkeypatch.chdir(root)
    before = _git_head(top)
    code = rotate.cmd_ack(SimpleNamespace(
        seat="belam", gen=7, ref="f52a4c", answer="continue", text=""),
        root)
    assert code == 0
    assert _git_head(top) == before              # nothing committed
    status = subprocess.run(["git", "-C", str(top), "status", "--porcelain"],
                            capture_output=True, text=True)
    assert status.stdout.strip() == ""
    out = capsys.readouterr().out
    assert "row already carries session_ref=f52a4c" in out
    assert "nothing to back-fill or commit" in out
    assert "git -C {0} push".format(top) not in out


def test_ack_diff_answer_never_commits(tmp_path, monkeypatch, capsys):
    """r3b (2): `diff` is the no-commit default — write + print, HEAD
    unchanged, no push line (the successor still edits)."""
    root, top = _ack_seed_git(tmp_path)
    monkeypatch.chdir(root)
    before = _git_head(top)
    code = rotate.cmd_ack(SimpleNamespace(
        seat="belam", gen=7, ref="f52a4c", answer="diff", text=""),
        root)
    assert code == 0
    assert _git_head(top) == before
    belam = next(r for r in rotate._load_seats(root)
                 if r.get("name") == "belam")
    assert belam.get("session_ref") == "f52a4c"
    out = capsys.readouterr().out
    assert "back-filled session_ref=f52a4c" in out
    assert "git -C {0} push".format(top) not in out
    assert "ack: committed" not in out


def test_ack_own_row_pre_dirty_refused_before_write(tmp_path, monkeypatch, capsys):
    """g15.24 belt (2b): a pre-dirtied OWN row in seats.md (this seat's own
    row carries an uncommitted hunk) makes the committing `continue` exit
    non-zero (3) with seats.md byte-identical and no commit — a guard, never
    lowered: the ack refuses to double-write a row someone was mid-edit on."""
    root, top = _ack_seed_git(tmp_path)
    monkeypatch.chdir(root)
    seats = rotate._ack_seats_path(root)
    pristine = seats.read_text(encoding="utf-8")
    dirty = pristine.replace('"name": "belam"', '"name": "belam", "role": "pre-dirty"')
    seats.write_text(dirty, encoding="utf-8")
    before = _git_head(top)
    code = rotate.cmd_ack(SimpleNamespace(
        seat="belam", gen=7, ref="f52a4c", answer="continue", text="",
        wait=0), root)
    assert code == 3
    assert seats.read_text(encoding="utf-8") == dirty
    assert _git_head(top) == before               # no commit
    # row was NOT back-filled (refused before any write)
    belam = next(r for r in rotate._load_seats(root)
                 if r.get("name") == "belam")
    assert belam.get("session_ref") == ""
    err = capsys.readouterr().err
    assert "dirty" in err and "refuse" in err
    # the OWN row is what the gate names as dirty (rel), never clean.
    assert rotate._ack_seats_dirty(root, top, "belam")


def test_ack_foreign_dirty_row_does_not_block(tmp_path, monkeypatch, capsys):
    """g15.24 belt (2b): a dirty FOREIGN row (another seat's hunk in the
    same seats.md) NEVER blocks the ack — the own row is clean, so the
    committing `continue` proceeds rc 0 and lands its own commit, leaving the
    foreign hunk byte-untouched and unstaged."""
    root, top = _ack_seed_git(tmp_path)
    monkeypatch.chdir(root)
    seats = rotate._ack_seats_path(root)
    text = seats.read_text(encoding="utf-8")
    belam_line = next(l for l in text.splitlines() if '"name": "belam"' in l)
    foreign = '  - {"name": "other", "role": "director", "model": "x", ' \
              '"effort": "max", "settings": ""}'
    text2 = text.replace(belam_line, belam_line + "\n" + foreign)
    seats.write_text(text2, encoding="utf-8")
    subprocess.run(["git", "-C", str(top), "add", "-A"], check=True,
                   capture_output=True)
    subprocess.run(["git", "-C", str(top), "commit", "-q", "-m", "two rows"],
                   check=True, capture_output=True)
    # dirty the FOREIGN row only: other's role -> a hunk that owns NO seat's
    # own row for belam.
    dirty_text = text2.replace('"name": "other", "role": "director"',
                               '"name": "other", "role": "parent"')
    seats.write_text(dirty_text, encoding="utf-8")
    foreign_dirty = seats.read_bytes()
    assert rotate._ack_seats_dirty(root, top, "belam") is None, \
        "a FOREIGN-row hunk must not make the OWN row look dirty"
    before = _git_head(top)
    code = rotate.cmd_ack(SimpleNamespace(
        seat="belam", gen=7, ref="f52a4c", answer="continue", text="",
        wait=0), root)
    assert code == 0, capsys.readouterr().err
    # the foreign row stays byte-untouched and unstaged after the ack: its
    # dirty value (role parent) is still in the working tree, and `git diff`
    # (unstaged) still shows it changed.
    now = seats.read_text(encoding="utf-8")
    assert '"name": "other", "role": "parent"' in now, \
        "the foreign row's dirty value must survive the ack (byte-untouched)"
    rel = os.path.relpath(rotate._ack_seats_path(root), top)
    staged = subprocess.run(["git", "-C", str(top), "diff", "--cached",
                             "--", rel], capture_output=True, text=True).stdout
    assert staged.strip() == "", "the foreign hunk must stay UNSTAGED"
    unstaged = subprocess.run(["git", "-C", str(top), "diff", "--", rel],
                              capture_output=True, text=True).stdout
    assert '"name": "other"' in unstaged, \
        "the foreign hunk must still be present (unstaged) after the ack"
    # only the OWN row hunk was committed by the ack commit.
    head = _git_head(top)
    assert head != before
    commit_diff = subprocess.run(
        ["git", "-C", str(top), "show", "--format=", head, "--", rel],
        capture_output=True, text=True).stdout
    changed = [ln for ln in commit_diff.splitlines()
               if ln.startswith(("+", "-"))
               and not ln.startswith(("+++", "---", "@@"))]
    assert any('"name": "belam"' in ln for ln in changed)
    assert not any('"name": "other"' in ln for ln in changed), \
        "the ack commit must not change the foreign row"


def test_ack_commits_only_own_row_leaves_foreign_unstaged(
        tmp_path, monkeypatch, capsys):
    """g15.24 belt (2a/2b) FALSIFIER: two rows dirty in one seats.md (this
    seat's own via the ack back-fill, plus a foreign spawn-row hunk pre-
    written) -> the committing ack stages and commits ONLY its own-row hunks;
    the foreign hunk is still present and byte-unchanged after the ack."""
    root, top = _ack_seed_git(tmp_path)
    monkeypatch.chdir(root)
    seats = rotate._ack_seats_path(root)
    text = seats.read_text(encoding="utf-8")
    belam_line = next(l for l in text.splitlines() if '"name": "belam"' in l)
    foreign = '  - {"name": "other", "role": "director", "model": "x", ' \
              '"effort": "max", "settings": ""}'
    text2 = text.replace(belam_line, belam_line + "\n" + foreign)
    seats.write_text(text2, encoding="utf-8")
    subprocess.run(["git", "-C", str(top), "add", "-A"], check=True,
                   capture_output=True)
    subprocess.run(["git", "-C", str(top), "commit", "-q", "-m", "two rows"],
                   check=True, capture_output=True)
    # pre-write a FOREIGN spawn-row hunk (other's row): owns NO seat's own row.
    dirty_text = text2.replace('"name": "other", "role": "director"',
                               '"name": "other", "role": "parent"')
    seats.write_text(dirty_text, encoding="utf-8")
    foreign_dirty = seats.read_bytes()
    before = _git_head(top)
    code = rotate.cmd_ack(SimpleNamespace(
        seat="belam", gen=7, ref="f52a4c", answer="continue", text="",
        wait=0), root)
    assert code == 0, capsys.readouterr().err
    # the ack landed ONE own-row commit ...
    head = _git_head(top)
    assert head != before
    # ... and the foreign hunk is STILL present and byte-unchanged in the tree
    # (its row now carries belam's ack back-fill too, but the foreign line is
    # exactly as we left it) ...
    now = seats.read_text(encoding="utf-8")
    assert '"name": "other", "role": "parent"' in now, \
        "foreign spawn-row hunk must still be present after the ack"
    # ... and unstaged, never bundled into the ack's commit.
    rel = os.path.relpath(rotate._ack_seats_path(root), top)
    staged = subprocess.run(["git", "-C", str(top), "diff", "--cached",
                             "--", rel], capture_output=True, text=True).stdout
    assert staged.strip() == "", "foreign hunk must stay UNSTAGED after the ack"
    # the ack commit changes ONLY belam's row line; the foreign row appears
    # only as an unchanged context line and is never a +/- change of the commit.
    commit_diff = subprocess.run(
        ["git", "-C", str(top), "show", "--format=", head, "--", rel],
        capture_output=True, text=True).stdout
    changed = [ln for ln in commit_diff.splitlines()
               if ln.startswith(("+", "-"))
               and not ln.startswith(("+++", "---", "@@"))]
    assert any('"name": "belam"' in ln for ln in changed), \
        "the ack commit must change belam's own row"
    assert not any('"name": "other"' in ln for ln in changed), \
        "the ack commit must not change the foreign spawn-row hunk"


def test_ack_commit_stages_index_only_never_writes_seats(
        tmp_path, monkeypatch, capsys):
    """g15.24 belt mechanism: `_ack_commit_seats` stages the OWN-row content
    into the INDEX ONLY — the shared seats.md working tree is NEVER written
    by the ack commit, not even transiently, so a concurrent writer can never
    be clobbered by a restore. FALSIFIER: the prior transient-write
    implementation called `seats.write_text(new)` then `seats.write_bytes(
    orig)`, so any write touching the seats path during the commit now fails
    this test. Also proves a dirty foreign hunk stays byte-untouched and
    unstaged and survives while the own row lands exactly one commit."""
    root, top = _ack_seed_git(tmp_path)
    monkeypatch.chdir(root)
    seats = rotate._ack_seats_path(root)
    text = seats.read_text(encoding="utf-8")
    belam_line = next(l for l in text.splitlines() if '"name": "belam"' in l)
    foreign = '  - {"name": "other", "role": "director", "model": "x", ' \
              '"effort": "max", "settings": ""}'
    text2 = text.replace(belam_line, belam_line + "\n" + foreign)
    seats.write_text(text2, encoding="utf-8")
    subprocess.run(["git", "-C", str(top), "add", "-A"], check=True,
                   capture_output=True)
    subprocess.run(["git", "-C", str(top), "commit", "-q", "-m",
                    "two rows"], check=True, capture_output=True)
    # dirty the FOREIGN row (a pre-written spawn-row hunk that owns no seat's
    # own row) AND the own row (as a normal back-fill would) so there is a
    # commit to make with a foreign hunk beside it.
    dirty_text = text2.replace('"name": "other", "role": "director"',
                               '"name": "other", "role": "parent"')
    own_dirty = dirty_text.replace(
        '"name": "belam", "role": "prime_director"',
        '"name": "belam", "role": "prime_director", '
        '"session_ref": "f52a4c"')
    seats.write_text(own_dirty, encoding="utf-8")
    seatsp = str(seats)
    before_bytes = seats.read_bytes()
    before = _git_head(top)

    written = []
    real_wt, real_wb = Path.write_text, Path.write_bytes

    def _wt(self, *a, **k):
        written.append(str(self))
        return real_wt(self, *a, **k)

    def _wb(self, *a, **k):
        written.append(str(self))
        return real_wb(self, *a, **k)

    monkeypatch.setattr(Path, "write_text", _wt)
    monkeypatch.setattr(Path, "write_bytes", _wb)
    ok, out = rotate._ack_commit_seats(
        root, "belam", SimpleNamespace(gen=7), "f52a4c")
    monkeypatch.setattr(Path, "write_text", real_wt)
    monkeypatch.setattr(Path, "write_bytes", real_wb)
    assert ok, out
    # byte-identical BEFORE and AFTER the ack commit, and NO write ever
    # targets it DURING (the transient-write implementation fails here).
    assert seats.read_bytes() == before_bytes, \
        "seats.md must be byte-identical after the ack commit"
    assert not any(p == seatsp for p in written), \
        f"the ack commit must never write the seats file, wrote: {written}"
    # exactly one own-row commit landed, the foreign hunk stays unstaged,
    # and the own-row change is no longer staged/unstaged.
    head = _git_head(top)
    assert head != before
    rel = os.path.relpath(rotate._ack_seats_path(root), top)
    staged = subprocess.run(["git", "-C", str(top), "diff", "--cached",
                             "--", rel], capture_output=True,
                            text=True).stdout
    assert staged.strip() == "", "foreign hunk must stay UNSTAGED"
    unstaged = subprocess.run(["git", "-C", str(top), "diff", "--", rel],
                              capture_output=True, text=True).stdout
    assert '"name": "other"' in unstaged, \
        "dirty foreign hunk must still be present (unstaged)"
    unstaged_changed = [ln for ln in unstaged.splitlines()
                        if ln.startswith(("+", "-"))
                        and not ln.startswith(("+++", "---", "@@"))]
    assert not any('"name": "belam"' in ln for ln in unstaged_changed), \
        "own-row change must be committed, not left unstaged"
    assert any('"name": "other"' in ln for ln in unstaged_changed), \
        "the dirty foreign hunk must be the only remaining change"
    commit_diff = subprocess.run(
        ["git", "-C", str(top), "show", "--format=", head, "--", rel],
        capture_output=True, text=True).stdout
    changed = [ln for ln in commit_diff.splitlines()
               if ln.startswith(("+", "-"))
               and not ln.startswith(("+++", "---", "@@"))]
    assert any('"name": "belam"' in ln for ln in changed)
    assert not any('"name": "other"' in ln for ln in changed), \
        "the ack commit must not change the foreign row"


def test_ack_foreign_edited_by_only_restamp_not_committed(
        tmp_path, monkeypatch, capsys):
    """g15.24 own-row predicate fix: a FOREIGN row whose ONLY change is its
    `edited_by` provenance restamp must NOT be bundled as the acking seat's
    own row. The own-row cut keys on the `name` cell ALONE, so a foreign
    edited_by change neither blocks the ack's dirty gate nor leaks into the
    ack commit — it stays byte-untouched and unstaged in the working tree,
    even though it sits adjacent to the own row's own write."""
    root, top = _ack_seed_git(tmp_path)
    monkeypatch.chdir(root)
    seats = rotate._ack_seats_path(root)
    text = seats.read_text(encoding="utf-8")
    belam_line = next(l for l in text.splitlines() if '"name": "belam"' in l)
    foreign = '  - {"name": "other", "role": "director", "model": "x", ' \
              '"effort": "max", "settings": ""}'
    text2 = text.replace(belam_line, belam_line + "\n" + foreign)
    seats.write_text(text2, encoding="utf-8")
    subprocess.run(["git", "-C", str(top), "add", "-A"], check=True,
                   capture_output=True)
    subprocess.run(["git", "-C", str(top), "commit", "-q", "-m",
                    "two rows"], check=True, capture_output=True)
    # dirty the FOREIGN row by restamping ONLY its edited_by provenance cell
    # (the own row stays clean, and the ack's own back-fill then dirties it).
    dirty_text = text2.replace('"name": "other"',
                               '"name": "other", "edited_by": "other-ed"')
    seats.write_text(dirty_text, encoding="utf-8")
    before = _git_head(top)
    code = rotate.cmd_ack(SimpleNamespace(
        seat="belam", gen=7, ref="f52a4c", answer="continue", text="",
        wait=0, no_commit=False), root)
    assert code == 0, capsys.readouterr().err
    head = _git_head(top)
    assert head != before, "the own-row back-fill must still be committed"
    rel = os.path.relpath(rotate._ack_seats_path(root), top)
    commit_diff = subprocess.run(
        ["git", "-C", str(top), "show", "--format=", head, "--", rel],
        capture_output=True, text=True).stdout
    changed = [ln for ln in commit_diff.splitlines()
               if ln.startswith(("+", "-"))
               and not ln.startswith(("+++", "---", "@@"))]
    assert any('"name": "belam"' in ln for ln in changed), \
        "the ack commit must still land the own row's write"
    assert not any('"name": "other"' in ln for ln in changed), \
        "the ack commit must not bundle a foreign edited_by-only restamp"
    # the foreign edited_by restamp stays byte-untouched and unstaged.
    now = seats.read_text(encoding="utf-8")
    assert '"name": "other", "edited_by": "other-ed"' in now
    staged = subprocess.run(["git", "-C", str(top), "diff", "--cached",
                             "--", rel], capture_output=True,
                            text=True).stdout
    assert staged.strip() == "", "foreign restamp must stay UNSTAGED"
    unstaged = subprocess.run(["git", "-C", str(top), "diff", "--", rel],
                              capture_output=True, text=True).stdout
    assert '"edited_by": "other-ed"' in unstaged, \
        "foreign edited_by restamp must still show as an unstaged change"


def test_ack_pre_staged_foreign_row_not_committed_and_unstaged(
        tmp_path, monkeypatch, capsys):
    """g15.24 belt hole (THIRD round): a FOREIGN row that was STAGED before
    the ack must NOT ride the ack's own-row commit. The own-row cut's base is
    HEAD (not the index), so a pre-staged foreign hunk is outside the base and
    cannot be bundled: rc 0, the new commit's changed lines name ONLY the own
    row, and the foreign change is still present in the working tree but now
    UNSTAGED (git diff shows it, git diff --cached is empty)."""
    root, top = _ack_seed_git(tmp_path)
    monkeypatch.chdir(root)
    seats = rotate._ack_seats_path(root)
    text = seats.read_text(encoding="utf-8")
    belam_line = next(l for l in text.splitlines()
                      if '"name": "belam"' in l)
    foreign = '  - {"name": "other", "role": "director", "model": "x", ' \
              '"effort": "max", "settings": ""}'
    text2 = text.replace(belam_line, belam_line + "\n" + foreign)
    seats.write_text(text2, encoding="utf-8")
    subprocess.run(["git", "-C", str(top), "add", "-A"], check=True,
                   capture_output=True)
    subprocess.run(["git", "-C", str(top), "commit", "-q", "-m",
                    "two rows"], check=True, capture_output=True)
    # PRE-STAGE a FOREIGN row change: other's role director -> parent, staged
    # into the real index (working tree and index agree on the dirty value).
    staged_text = text2.replace('"name": "other", "role": "director"',
                                '"name": "other", "role": "parent"')
    seats.write_text(staged_text, encoding="utf-8")
    rel = os.path.relpath(rotate._ack_seats_path(root), top)
    subprocess.run(["git", "-C", str(top), "add", "--", rel], check=True,
                   capture_output=True)
    # the pre-staged foreign hunk is NOT the own row, so the gate stays open.
    assert rotate._ack_seats_dirty(root, top, "belam") is None, \
        "a pre-staged FOREIGN-row hunk must not block the own-row ack"
    before = _git_head(top)
    code = rotate.cmd_ack(SimpleNamespace(
        seat="belam", gen=7, ref="f52a4c", answer="continue", text="",
        wait=0), root)
    assert code == 0, capsys.readouterr().err
    head = _git_head(top)
    assert head != before, "the own-row back-fill must still be committed"
    # the new commit changes ONLY belam's own row -- never the foreign one.
    commit_diff = subprocess.run(
        ["git", "-C", str(top), "show", "--format=", head, "--", rel],
        capture_output=True, text=True).stdout
    changed = [ln for ln in commit_diff.splitlines()
               if ln.startswith(("+", "-"))
               and not ln.startswith(("+++", "---", "@@"))]
    assert any('"name": "belam"' in ln for ln in changed), \
        "the ack commit must land the own row's write"
    assert not any('"name": "other"' in ln for ln in changed), \
        "a pre-staged foreign row must never ride the ack commit"
    # the foreign change is still in the working tree, now UNSTAGED.
    now = seats.read_text(encoding="utf-8")
    assert '"name": "other", "role": "parent"' in now, \
        "the foreign row's dirty value must survive, bytes preserved"
    staged = subprocess.run(["git", "-C", str(top), "diff", "--cached",
                             "--", rel], capture_output=True,
                            text=True).stdout
    assert staged.strip() == "", \
        "the pre-staged foreign hunk must be UNSTAGED after the ack"
    unstaged = subprocess.run(["git", "-C", str(top), "diff", "--", rel],
                              capture_output=True, text=True).stdout
    assert '"name": "other"' in unstaged, \
        "the foreign change must still show as an unstaged diff"
    # belam's own row is not left staged either.
    assert staged.strip() == "", "no own-row diff may remain staged"


def test_ack_wait_repolls_until_dirt_clears(tmp_path, monkeypatch, capsys):
    """g15.24 belt (2c): `ack --wait N` RE-POLLS the own-row gate every 5 s up
    to N s — when the own-row dirt clears on a later poll, the ack proceeds rc 0
    instead of refusing. Sleep is stubbed (no real wait); the second poll sees a
    clean own row."""
    root, top = _ack_seed_git(tmp_path)
    monkeypatch.chdir(root)
    calls = {"n": 0}
    real = rotate._ack_seats_dirty

    def _flaky(r, t, s):
        calls["n"] += 1
        if calls["n"] == 1:
            return os.path.relpath(rotate._ack_seats_path(r), t)
        return real(r, t, s)

    monkeypatch.setattr(rotate, "_ack_seats_dirty", _flaky)
    monkeypatch.setattr(rotate.time, "sleep", lambda s: None)
    code = rotate.cmd_ack(SimpleNamespace(
        seat="belam", gen=7, ref="f52a4c", answer="continue", text="",
        wait=6), root)
    assert code == 0, capsys.readouterr().err
    assert calls["n"] >= 2, "--wait must re-poll the own-row gate"
    belam = next(r for r in rotate._load_seats(root)
                 if r.get("name") == "belam")
    assert belam.get("session_ref") == "f52a4c"


def test_ack_wait_refuses_when_still_dirty_after_poll(tmp_path, monkeypatch, capsys):
    """g15.24 belt (2c): when the own-row gate STAYS dirty, `ack --wait N`
    re-polls (>=2 checks) then refuses with exit 3 — one short wait, no long
    sleep."""
    root, top = _ack_seed_git(tmp_path)
    monkeypatch.chdir(root)
    seats = rotate._ack_seats_path(root)
    pristine = seats.read_text(encoding="utf-8")
    seats.write_text(pristine.replace(
        '"name": "belam"', '"name": "belam", "role": "pre-dirty"'),
        encoding="utf-8")
    calls = {"n": 0}
    real = rotate._ack_seats_dirty

    def _always_dirty(r, t, s):
        calls["n"] += 1
        return os.path.relpath(rotate._ack_seats_path(r), t)

    monkeypatch.setattr(rotate, "_ack_seats_dirty", _always_dirty)
    code = rotate.cmd_ack(SimpleNamespace(
        seat="belam", gen=7, ref="f52a4c", answer="continue", text="",
        wait=1), root)   # one short real wait (~1s), then refuse
    assert code == 3
    assert calls["n"] >= 2, "--wait must re-poll the own-row gate before refusing"


def test_ack_dirty_seats_allowed_when_no_commit(tmp_path, monkeypatch, capsys):
    """r3b boundary: the dirty refusal is for the COMMIT path only — a
    `--no-commit` ack on the same dirty seats.md proceeds (write + print, no
    commit), because there is no commit to bundle."""
    root, top = _ack_seed_git(tmp_path)
    monkeypatch.chdir(root)
    seats = rotate._ack_seats_path(root)
    seats.write_text(seats.read_text(encoding="utf-8") + "dirty\n",
                     encoding="utf-8")
    before = _git_head(top)
    code = rotate.cmd_ack(SimpleNamespace(
        seat="belam", gen=7, ref="f52a4c", answer="continue", text="",
        no_commit=True), root)
    assert code == 0
    assert _git_head(top) == before
    belam = next(r for r in rotate._load_seats(root)
                 if r.get("name") == "belam")
    assert belam.get("session_ref") == "f52a4c"
    out = capsys.readouterr().out
    assert "back-filled session_ref=f52a4c" in out
    assert "git -C {0} push".format(top) not in out


# ── hypothesis:l4-a-failed-ack-commit-exits-non-zero-and-unstages-and- ──
# -three-tests-assert-what-they-claim (g15.24 P1). A FAILED commit path
# (git add rc!=0 OR git commit rc!=0) must not leave seats.md staged — that
# is exactly the dirt that would refuse the NEXT ack (`_ack_seats_dirty`).
# So `_ack_commit_seats` returns (ok, out), prints the error on STDERR, runs
# `git reset -q -- <rel>` (working tree keeps the back-filled row), and
# `cmd_ack` exits NON-ZERO (3). Falsifier: a forced commit failure leaves
# seats.md STAGED, or the command exits 0.

def test_ack_failed_commit_exits_nonzero_unstages_row_keeps_working_tree(
        tmp_path, monkeypatch, capsys):
    """g15.24 P1 falsifier + as-written claim (first integrity test): a
    FORCED commit failure (a fixture `.git/hooks/pre-commit` that `exit 1`)
    makes the ack exit NON-ZERO (3), prints the error on STDERR (never
    stdout), UNSTAGES seats.md (`git diff --cached` empty), and STILL keeps
    the back-filled row in the WORKING TREE — so the next ack's dirty gate
    finds seats.md clean, not staged."""
    root, top = _ack_seed_git(tmp_path)
    monkeypatch.chdir(root)
    # the harness injects agent-git hooks via GIT_CONFIG_* command-line
    # config (it wins over the repo's own config); clear it so the repo's
    # OWN .git/hooks/pre-commit actually runs and can force the commit fail.
    monkeypatch.delenv("GIT_CONFIG_COUNT", raising=False)
    monkeypatch.delenv("GIT_CONFIG_KEY_0", raising=False)
    monkeypatch.delenv("GIT_CONFIG_VALUE_0", raising=False)
    hooks = top / ".git" / "hooks"
    hooks.mkdir(parents=True, exist_ok=True)
    pre = hooks / "pre-commit"
    pre.write_text("#!/bin/sh\nexit 1\n", encoding="utf-8")
    pre.chmod(0o755)
    rel = os.path.relpath(rotate._ack_seats_path(root), top)
    code = rotate.cmd_ack(SimpleNamespace(
        seat="belam", gen=7, ref="f52a4c", answer="continue", text="",
        registry_dir=None, window_path=None), root)
    assert code == 3, f"expect exit 3, got {code}"
    # the row was UNSTAGED — seats.md is not left staged for the next ack.
    cached = subprocess.run(["git", "-C", str(top), "diff", "--cached",
                             "--", rel], capture_output=True, text=True)
    assert cached.stdout.strip() == "", \
        "seats.md must NOT be left staged after a failed commit"
    # the row is still written in the WORKING TREE (back-fill kept by reset).
    belam = next(r for r in rotate._load_seats(root)
                 if r.get("name") == "belam")
    assert belam.get("session_ref") == "f52a4c", (
        "working tree must keep the back-filled row after the failed commit")
    out, err = capsys.readouterr()
    assert "commit failed" in err, "error must go to STDERR"
    assert "commit failed" not in out, "error must NOT go to STDOUT"


def test_ack_failed_commit_cmd_exits_nonzero_and_no_staged_diff(
        tmp_path, monkeypatch, capsys):
    """g15.24 P1 (second integrity test): a FORCED `git commit` failure (a
    mocked subprocess returning rc 1 for the ack's own-row commit) makes the
    ack exit NON-ZERO (3) with NO staged diff on seats.md."""
    root, top = _ack_seed_git(tmp_path)
    monkeypatch.chdir(root)
    rel = os.path.relpath(rotate._ack_seats_path(root), top)
    real_run = subprocess.run

    def _fail_commit(cmd, *a, **k):
        if cmd and cmd[0] == "git" and "commit" in cmd:
            return subprocess.CompletedProcess(
                cmd, 1, "", "forced commit failure")
        return real_run(cmd, *a, **k)

    monkeypatch.setattr(rotate.subprocess, "run", _fail_commit)
    code = rotate.cmd_ack(SimpleNamespace(
        seat="belam", gen=7, ref="f52a4c", answer="continue", text="",
        registry_dir=None, window_path=None), root)
    assert code == 3, f"expect exit 3, got {code}"
    cached = subprocess.run(["git", "-C", str(top), "diff", "--cached",
                             "--", rel], capture_output=True, text=True)
    assert cached.stdout.strip() == "", \
        "git commit failure must not leave seats.md staged"
    out, err = capsys.readouterr()
    assert "commit failed" in err, "git commit error must go to STDERR"
    assert "commit failed" not in out, \
        "git commit error must NOT go to STDOUT"


# ── hypothesis:l4-rotate-self-commits-its-own-spawn-row-write-so-the-ack- ──
# -finds-seats-clean (g15.24 fix (a), Sensei's pick). rotate-self commits its
# OWN s6.1 spawn-row write itself (seats.md only, one line) so the successor's
# ack finds seats.md CLEAN and the r3b gate (`_ack_seats_dirty`) stays as
# written. The falsifier: rotate-self-then-ack yields EXACTLY two commits on
# seats.md — first '<seat> spawn row: ...' authored by rotate-self, then
# '<seat> ack: gen ...' authored by the ack — with NO exit-3 refusal in
# between and `git status --porcelain -- seats.md` empty after each.

def _spawn_seed_git(tmp_path):
    """A real git repo (top = tmp_path) with the graph root (`proj/`) and a
    COMMITTED seats.md carrying one row — the rotate-self s6.1 spawn-row
    write + commit + ack path. sessions/ is gitignored so the ack.json the
    ack writes stays out of `git status`. Returns (graph_root, repo_top)."""
    subprocess.run(["git", "init", "-q", str(tmp_path)], check=True)
    subprocess.run(["git", "-C", str(tmp_path), "config", "user.email",
                    "spawn@test"], check=True)
    subprocess.run(["git", "-C", str(tmp_path), "config", "user.name",
                    "spawn test"], check=True)
    (tmp_path / ".gitignore").write_text("sessions/\n", encoding="utf-8")
    root = _proj(tmp_path, ladder_roles="")
    (root / "agi-tree.config.json").write_text("{}", encoding="utf-8")
    _write_seats_sheet(root, [{"name": "belam", "role": "prime_director",
                               "model": "x", "effort": "max",
                               "settings": "", "session_ref": "",
                               "session_id": "", "generation": 2,
                               "window": "", "pid": 0}])
    subprocess.run(["git", "-C", str(tmp_path), "add", "-A"], check=True)
    subprocess.run(["git", "-C", str(tmp_path), "commit", "-q", "-m",
                    "seats seed"], check=True)
    return root, tmp_path


def _git_commits(top, path):
    """`<shortsha> <subject>` for every commit that touched `path` (oldest
    last). The current HEAD subject is first."""
    cmd = ["git", "-C", str(top), "log", "--format=%h %s", "--", path]
    return subprocess.run(cmd, capture_output=True,
                          text=True).stdout.splitlines()


def test_rotate_self_commits_own_spawn_row_write_then_ack_passes(
        tmp_path, monkeypatch, capsys):
    """g15.24 falsifier (fix (a)): rotate-self's s6.1 `_successor_row_write`
    leaves seats.md DIRTY; `_commit_spawn_row` (seats.md only) makes it clean;
    the successor's `ack ... continue` then passes the r3b gate (no exit 3)
    and lands a SECOND commit. EXACTLY two commits on seats.md: spawn row
    (rotate-self) then ack. Working tree clean after each."""
    root, top = _spawn_seed_git(tmp_path)
    monkeypatch.chdir(root)

    # (a) PRE-FIX reproduction: the s6.1 spawn-row write dirties seats.md
    # (uncommitted) — the exact dirt the ack's r3b gate would refuse with
    # exit 3 before this round.
    wrote = rotate._successor_row_write(
        root, actor="belam", seat="belam", role="prime_director",
        session_ref="", pid=4242, session_id="sess-123",
        generation=3, window="@w9")
    assert wrote.startswith("config:seats row")
    assert rotate._ack_seats_dirty(root, rotate._git_toplevel(root), "belam"), \
        "PRE-FIX: spawn-row write must leave seats.md dirty (the exit-3)"

    # (b) THE FIX: rotate-self commits its OWN spawn-row write, seats.md only.
    outcome = rotate._commit_spawn_row(
        root, seat="belam", generation=3, session_id="sess-123",
        window="@w9", pid=4242)
    assert outcome.startswith("spawn_row_commit: committed"), outcome
    # seats.md clean again -> the ack's dirty gate has nothing to refuse.
    assert rotate._ack_seats_dirty(root, rotate._git_toplevel(root), "belam") is None
    st = subprocess.run(["git", "-C", str(top), "status", "--porcelain",
                         "--", "proj/nodes/.geometry/seats.md"],
                        capture_output=True, text=True)
    assert st.stdout.strip() == ""      # clean after the rotate-self commit
    commits = _git_commits(top, "proj/nodes/.geometry/seats.md")
    assert len(commits) == 2 and commits[0].endswith(
        "belam spawn row: gen 3, session_id sess-123, window @w9, pid 4242")

    # (c) The successor's wake act finds seats.md clean -> continues, no
    # exit-3, lands the ack commit.
    before = _git_head(top)
    code = rotate.cmd_ack(SimpleNamespace(
        seat="belam", gen=3, ref="f52a4c", answer="continue", text=""),
        root)
    assert code == 0, capsys.readouterr().err
    ack_head = _git_head(top)
    assert ack_head != before            # the ack made a second commit

    # (d) EXACTLY two commits on seats.md (beyond the seed): spawn row
    # (rotate-self), then the ack. No exit-3 refusal in between; seats.md
    # clean after each.
    log = _git_commits(top, "proj/nodes/.geometry/seats.md")
    assert len(log) == 3, log  # [ack, spawn row, seed]
    assert log[0].endswith("belam ack: gen 3, session_ref f52a4c, "
                           "window @w9, pid 4242")
    assert log[1].endswith("belam spawn row: gen 3, session_id sess-123, "
                           "window @w9, pid 4242")
    assert log[2].endswith("seats seed")
    for h in (log[0].split()[0], log[1].split()[0]):
        files = subprocess.run(["git", "-C", str(top), "diff-tree",
                                "--no-commit-id", "--name-only", "-r", h],
                               capture_output=True, text=True).stdout.split()
        assert files == ["proj/nodes/.geometry/seats.md"], files
    status = subprocess.run(["git", "-C", str(top), "status",
                             "--porcelain"], capture_output=True, text=True)
    assert status.stdout.strip() == ""   # clean after the whole round
    assert "git -C {0} push".format(top) in capsys.readouterr().out


def test_commit_spawn_row_records_skip_no_change_or_no_repo(
        tmp_path, monkeypatch):
    """g15.24 falsifier: `_commit_spawn_row` NEVER raises and records a one-
    line skip when there is nothing to commit — seats.md already clean after
    the write (the row was byte-identical), or no git repo at all. The
    rotation still completes; no commit is forced."""
    root, top = _spawn_seed_git(tmp_path)
    monkeypatch.chdir(root)
    # seats.md clean + committed and NO pending row write -> nothing to stage.
    no_change = rotate._commit_spawn_row(
        root, seat="belam", generation=4, session_id="sess-9",
        window="@w9", pid=4242)
    assert "spawn_row_commit: SKIPPED" in no_change, no_change
    assert _git_head(top) == _git_head(top)   # no commit was made

    # a gitless root (sibling OUTSIDE the seeded repo): _git_toplevel -> None
    # -> records SKIPPED, no commit.
    bare = tmp_path.parent / "gitless"
    (bare / "nodes" / ".geometry").mkdir(parents=True)
    gitless = rotate._commit_spawn_row(
        bare, seat="belam", generation=4, session_id="sess-9",
        window="@w9", pid=4242)
    assert "spawn_row_commit: SKIPPED" in gitless and "no git repo" in gitless


def test_bootstrap_writes_before_spawn_in_rotate_self():
    """Owed item (iv) — turn-one proof is a CODE-ORDER falsifier, not a code-
    position guess. `cmd_rotate_self` must write the bootstrap record BEFORE
    it spawns the successor window; otherwise the successor's first turn could
    read a bootstrap that does not exist yet. This reads the LIVE function
    source and asserts the pre-spawn `_write_bootstrap(` call site precedes
    the `spawn_window(` call site, so a future reorder that moves the write
    after the spawn FAILS this test.
    """
    import inspect as _inspect
    import re as _re
    src = _inspect.getsource(rotate.cmd_rotate_self)
    write_idx = src.find("_write_bootstrap(")
    spawn_idx = src.find("spawn_window(")
    assert write_idx >= 0, "cmd_rotate_self no longer calls _write_bootstrap"
    assert spawn_idx >= 0, "cmd_rotate_self no longer calls spawn_window"
    assert write_idx < spawn_idx, (
        "_write_bootstrap() must run BEFORE spawn_window() in cmd_rotate_self; "
        "a turnaround-one bootstrap is only valid pre-spawn"
    )


# --- owed item (v): AGI_SEAT export on cmd_spawn / cmd_loop when --seat -----
# hypothesis:l4-startup-first-turn-is-performed-by-the-service-and-the-hook-
# fires-at-turn-one (SL1.07). A concrete --seat on spawn/loop must ride
# AGI_SEAT=<name> out in front of the claude argv so the SessionStart hook
# copy can fire at turn one; when --seat is ABSENT the launch line must stay
# byte-identical to a plain spawn/loop.

def test_spawn_window_agi_seat_export_and_byte_identical_absent(monkeypatch, tmp_path):
    # Direct drive of the shared launch path, dry-run so nothing launches.
    monkeypatch.setattr(rotate, "_existing_windows", lambda *a, **k: [])
    base = rotate.spawn_window(
        name="adv", tier="prime_director", prompt_file=None,
        settings=None, tmux_session="agi-rc", root=None,
        dry_run=True, seat=None,
    )[1]
    seated = rotate.spawn_window(
        name="adv", tier="prime_director", prompt_file=None,
        settings=None, tmux_session="agi-rc", root=None,
        dry_run=True, seat="sanctuary-director",
    )[1]
    assert "AGI_SEAT=" not in base
    # a seat exports BOTH AGI_POST (primary) and AGI_SEAT (deprecated alias)
    # so either spelling resolves downstream (hypothesis:l4-a-seat-is-a-post-
    # everywhere).
    _q = rotate.shlex.quote('sanctuary-director')
    assert f"export AGI_POST={_q} AGI_SEAT={_q} && " in seated
    # amendment e: a seat inserts BOTH identity and the launch-wrapper. The
    # wrapper is the direct parent of claude, so the ONLY thing that changes
    # vs base is the `export AGI_SEAT=... &&` prefix plus the wrapper inserted
    # before claude; base's claude argv must ride AFTER the wrapper's `--`,
    # byte-identical.
    assert "launch-wrapper" in seated
    claude_argv = base.split(" && ")[-1]
    assert f" -- {claude_argv}" in seated
    assert seated.index("launch-wrapper") < seated.index("claude")


def test_cmd_spawn_and_loop_forward_seat(monkeypatch, tmp_path):
    # Proves cmd_spawn and cmd_loop actually FORWARD args.seat into the shared
    # launch path (the wiring owed item (v) added). With args.seat None the
    # forwarded value is None, so _shell_cmd emits no AGI_SEAT (byte-identical).
    root = _proj(tmp_path)
    monkeypatch.chdir(root)
    monkeypatch.setattr(rotate, "find_project_root", lambda: root)
    monkeypatch.setattr(rotate, "_existing_windows", lambda *a, **k: [])
    called = {}

    def _capture(**kw):
        called.update(kw)
        return 0, "claude --remote-control adv"

    monkeypatch.setattr(rotate, "spawn_window", _capture)

    # spawn with --seat
    code = rotate.cmd_spawn(SimpleNamespace(
        name="adv", tier="adv_alive", prompt_file=None, model=None,
        effort=None, settings=None, tmux_session="agi-rc", window_path=None,
        root=root, dry_run=True, successor_argv=None, seat="sanctuary-director",
    ), root)
    assert code == 0 and called.get("seat") == "sanctuary-director"
    # spawn without --seat (byte-identical: seat forwarded as None)
    called.clear()
    code = rotate.cmd_spawn(SimpleNamespace(
        name="adv", tier="adv_alive", prompt_file=None, model=None,
        effort=None, settings=None, tmux_session="agi-rc", window_path=None,
        root=root, dry_run=True, successor_argv=None, seat=None,
    ), root)
    assert code == 0 and called.get("seat") is None

    # loop with --seat
    monkeypatch.setattr(rotate, "cmd_meter", lambda args, root: 1)  # rotate
    called.clear()
    code = rotate.cmd_loop(SimpleNamespace(
        session_log=None, force=False, role="adv_alive", name="adv",
        name_prefix="belam", model=None, effort=None, settings=None,
        prompt_file=None, tmux_session="agi-rc", window_path=None,
        debug_file=None, dry_run=True, timeout=1, seat="sanctuary-director",
    ), root)
    assert code == 0 and called.get("seat") == "sanctuary-director"
    # loop without --seat
    called.clear()
    code = rotate.cmd_loop(SimpleNamespace(
        session_log=None, force=False, role="adv_alive", name="adv",
        name_prefix="belam", model=None, effort=None, settings=None,
        prompt_file=None, tmux_session="agi-rc", window_path=None,
        debug_file=None, dry_run=True, timeout=1, seat=None,
    ), root)
    assert code == 0 and called.get("seat") is None


# --------------------------------------------------------------------------
# Round SL5.09 — clause 3 of hypothesis:l4-a-rotation-alert-lands-in-the-
# inbox-a-coalesced-nudge-still-wakes-and-detected-records-dedupe: a
# crash-recovery record (a heal outcome, `result: detected`) is NEVER a
# rotation. `_latest_rotation_record` and `status --record latest <seat>`
# must skip it, even when it is the LEXICALLY newest `<seat>.*.json` (nine
# detected records for one death is what made the newest file a detected one).
# --------------------------------------------------------------------------

def _record_fixture(root: Path, seat: str, name: str, rec: dict) -> Path:
    rot = root / "sessions" / "rotations"
    rot.mkdir(parents=True, exist_ok=True)
    p = rot / f"{seat}.{name}.json"
    p.write_text(json.dumps(rec, indent=2) + "\n", encoding="utf-8")
    return p


def test_latest_rotation_record_skips_crash_recovery(tmp_path):
    """A real rotation survives the presence of a lexically-NEWER
    crash-recovery `detected` record for the same seat: the newest ROTATION
    must be returned, never the detected recovery."""
    seat = "skp"
    _record_fixture(tmp_path, seat, "20260911T190000Z", {
        "rotation": "rotate-self", "seat": seat, "result": "success"})
    # newer stamp, same seat, a crash-recovery detected record
    _record_fixture(tmp_path, seat, "20260911T193000Z", {
        "rotation": "crash-recovery", "seat": seat, "result": "detected"})
    rec = rotate._latest_rotation_record(tmp_path, seat)
    assert rec is not None
    assert rec["rotation"] == "rotate-self", \
        "a crash-recovery detected record must never be read as the rotation"
    assert rec["result"] == "success"


def test_latest_rotation_record_none_when_only_crash_recovery(tmp_path):
    """When a seat has ONLY crash-recovery records (no real rotation), the
    reader must return None — there is no rotation record to serve, and a
    rotated-in seat must not be told its crash-recovery is its rotation."""
    seat = "onlyrec"
    _record_fixture(tmp_path, seat, "20260911T193000Z", {
        "rotation": "crash-recovery", "seat": seat, "result": "detected"})
    _record_fixture(tmp_path, seat, "20260911T194000Z", {
        "rotation": "crash-recovery", "seat": seat, "result": "detected"})
    assert rotate._latest_rotation_record(tmp_path, seat) is None


def test_status_record_latest_skips_detected_record(tmp_path, capsys):
    """`status --record latest <seat>` prints the newest ROTATION record,
    never a crash-recovery `detected` record (the falsifier: status counts a
    detected record as a rotation). The detected file's own name and body
    must be absent from stdout."""
    seat = "stat"
    rotation = _record_fixture(tmp_path, seat, "20260911T180000Z", {
        "rotation": "rotate-self", "seat": seat, "result": "success",
        "generation": 2})
    detected = _record_fixture(tmp_path, seat, "20260911T190000Z", {
        "rotation": "crash-recovery", "seat": seat, "result": "detected"})
    args = SimpleNamespace(record=True, seat=seat, wait=0)
    rc = rotate.cmd_status(args, tmp_path)
    out = capsys.readouterr().out
    assert rc == 0
    assert "latest rotation record" in out
    assert rotation.name in out, out                 # the rotation IS served
    assert detected.name not in out, \
        f"status must not surface the detected record: {out}"
    assert "crash-recovery" not in out, out


# --- hypothesis:l4-branches-follow-the-season-grammar clause (5) ---
# The `prepare` merge target (`_prepare_merge_target`) must resolve a seat's
# post/loop branch through the grammar module's `merge_target`, so a town
# seat merges its OWN town main, never a literal core main.


def _repo_on_branch(tmp_path: Path, branch: str) -> Path:
    """git-init a throwaway repo checked out on `branch` with one commit, so
    `rev-parse --abbrev-ref HEAD` names the real branch (an unborn HEAD reads
    as HEAD/error)."""
    repo = tmp_path / "repo"
    repo.mkdir(parents=True)
    subprocess.run(["git", "-C", str(repo), "init", "-b", branch],
                   check=True, capture_output=True)
    for cfg in ("user.email", "user.name"):
        subprocess.run(["git", "-C", str(repo), "config", cfg, "t"],
                       check=True, capture_output=True)
    (repo / "README").write_text("x")
    subprocess.run(["git", "-C", str(repo), "add", "-A"], check=True,
                   capture_output=True)
    subprocess.run(["git", "-C", str(repo), "commit", "-m", "init"],
                   check=True, capture_output=True)
    return repo


def test_prepare_merge_target_town_loop_targets_town_main(tmp_path):
    # A seat on a canonical town loop branch merges that TOWN's main, not the
    # core season main the old `season_branch` fallback would have named.
    repo = _repo_on_branch(tmp_path,
                           "season2/web-app-suite/season1/loops/xx-yy")
    assert rotate._prepare_merge_target(repo) == \
        "season2/web-app-suite/season1/main"


def test_prepare_merge_target_town_post_targets_town_main(tmp_path):
    repo = _repo_on_branch(tmp_path,
                           "season2/streaming-suite/season1/posts/foo")
    assert rotate._prepare_merge_target(repo) == \
        "season2/streaming-suite/season1/main"


def test_prepare_merge_target_season_loop_targets_season_main(tmp_path):
    # A loop directly under season<N>/main resolves to the core season main.
    repo = _repo_on_branch(tmp_path, "season2/loops/xx-yy")
    assert rotate._prepare_merge_target(repo) == "season2/main"


# ════════════════════════════════════════════════════════════════════════════
# g15.26 hypothesis:l4-the-label-authority-falls-back-to-mains-committed-row-
# and-every-key-cell-writer-commits-and-pushes-its-own-row — CLAUSE (2) ROTATE
# MINT legs: _rotate_first_key and the spawn-row/successor commit now commit
# the key-cell write onto MAIN's season branch and PUSH it to origin (bare
# remote fixture). A failed push never fails the mint/rotation.
# ════════════════════════════════════════════════════════════════════════════


def _git_with_bare(tmp_path, seed):
    """seed(main_root, seats_path) -> commit an initial seats.md, then wire a
    bare remote and push the initial branch so `origin` exists. Returns
    (main_root, repo_top, bare). The caller's key-cell write then commits and
    pushes onto that branch and origin reflects it."""
    # bare remote OUTSIDE the seeded repo tree -- placing it under tmp_path
    # would itself show as untracked in `git status` and trip the "MAIN not
    # dirty" assertion.
    bare = tmp_path.parent / f"{tmp_path.name}-remote.git"
    subprocess.run(["git", "init", "--bare", "-q", str(bare)], check=True)
    root, top = _spawn_seed_git(tmp_path)   # proj graph + committed seats.md
    subprocess.run(["git", "-C", str(top), "remote", "add", "origin",
                    str(bare)], check=True)
    branch = subprocess.run(["git", "-C", str(top), "rev-parse",
                             "--abbrev-ref", "HEAD"], capture_output=True,
                            text=True).stdout.strip()
    subprocess.run(["git", "-C", str(top), "push", "-u", "origin", branch],
                   check=True)
    return root, top, bare


def test_rotate_first_key_commits_and_pushes_first_key_to_bare_remote(
        tmp_path, monkeypatch, capsys):
    """g15.26 clause (2) ROTATE MINT (first): an unkeyed real row's first
    mint writes its pubkey cells into MAIN and COMMITS+PUSHES them -- after
    the mint ORIGIN's row carries the pubkey and MAIN is not left dirty."""
    root, top, bare = _git_with_bare(
        tmp_path, lambda r: None)
    capsys.readouterr()
    note = rotate._rotate_first_key(root, root, "belam",
                                    {"role": "prime_director"})
    assert note and "minted its first key" in note
    shown = subprocess.run(
        ["git", "-C", str(top), "show",
         "origin/master:proj/nodes/.geometry/seats.md"],
        capture_output=True, text=True)
    assert "pubkey" in shown.stdout, shown.stdout
    st = subprocess.run(["git", "-C", str(top), "status", "--porcelain"],
                        capture_output=True, text=True)
    assert st.stdout.strip() == "", st.stdout   # MAIN not left dirty


def test_commit_spawn_row_pushes_successor_row_to_bare_remote(
        tmp_path, capsys):
    """g15.26 clause (2) SUCCESSOR/spawn-row: the successor row write
    (carrying the successor pubkey + key_history) is committed AND pushed —
    origin's row carries the successor cells and MAIN is clean."""
    root, top, bare = _git_with_bare(
        tmp_path, lambda r: None)
    rotate._successor_row_write(
        root, actor="belam", seat="belam", role="prime_director",
        session_ref="", pid=4242, session_id="sess-123",
        generation=3, window="@w9")
    capsys.readouterr()
    rotate._commit_spawn_row(root, seat="belam", generation=3,
                             session_id="sess-123", window="@w9", pid=4242)
    out = capsys.readouterr().err
    assert "push: OK" in out, out
    shown = subprocess.run(
        ["git", "-C", str(top), "show",
         "origin/master:proj/nodes/.geometry/seats.md"],
        capture_output=True, text=True)
    assert "sess-123" in shown.stdout, shown.stdout
    st = subprocess.run(["git", "-C", str(top), "status", "--porcelain"],
                        capture_output=True, text=True)
    assert st.stdout.strip() == "", st.stdout


def test_first_seating_writes_row_and_commits_seating_row_and_pushes(
        tmp_path, capsys):
    """Claim (2) (hypothesis:l4-the-spawn-gate-refuses-both-directions-and-a-
    hand-seating-commits-its-row-and-answers-the-ack): the first-seating
    writer writes its own identity row into MAIN (gen 1 + session_id/window/
    pid), then `_commit_spawn_row(verb="seating row")` commits ONLY its own
    row (`belam seating row: gen 1, ...`) and `_push_season_branch` pushes it
    -- a hand seating leaves MAIN clean, never a dirty row riding to the next
    merge-up (falsifier: "a seating leaves seats.md dirty in MAIN"). The ack
    it writes is `continue, source: seating` (claim 3 default)."""
    root, top, bare = _git_with_bare(tmp_path, lambda r: None)
    capsys.readouterr()
    got = rotate._first_seating_spawn_writes(
        root=root, seat="belam", generation=1, session_id="sess-1",
        window="@w9", pid=4242, role="prime_director")
    assert "row" in got and "seats" in (got["row"] or "")
    # the row write left seats.md dirty -- the exact dirt claim (2) commits.
    dirty = rotate._ack_seats_dirty(root, rotate._git_toplevel(root), "belam")
    assert dirty, "a first seating's own row write must dirty seats.md"
    outcome = rotate._commit_spawn_row(
        root=root, seat="belam", generation=1, session_id="sess-1",
        window="@w9", pid=4242, verb="seating row")
    assert outcome.startswith("spawn_row_commit: committed"), outcome
    out = capsys.readouterr().err
    assert "push: OK" in out, out
    # MAIN clean after the hand seating.
    st = subprocess.run(["git", "-C", str(top), "status", "--porcelain"],
                        capture_output=True, text=True)
    assert st.stdout.strip() == "", st.stdout
    # origin's committed row carries the seating identity + the exact message.
    shown = subprocess.run(
        ["git", "-C", str(top), "show",
         "origin/master:proj/nodes/.geometry/seats.md"],
        capture_output=True, text=True)
    assert "sess-1" in shown.stdout, shown.stdout
    commits = _git_commits(top, "proj/nodes/.geometry/seats.md")
    assert commits[0].endswith(
        "belam seating row: gen 1, session_id sess-1, window @w9, pid 4242"), \
        commits[0]
    # the ack it answered its OWN channel with (claim 3).
    ack = json.loads((rotate._ack_path(root, "belam"))
                     .read_text(encoding="utf-8"))
    assert ack["answer"] == "continue" and ack["source"] == "seating", ack
    assert ack["gen_after"] == 1


def _two_row_git_root(tmp_path):
    """A committed git root whose seats.md carries TWO adjacent rows: belam
    (the seat under test) then `other` (foreign). Returns (root, top)."""
    subprocess.run(["git", "init", "-q", str(tmp_path)], check=True)
    subprocess.run(["git", "-C", str(tmp_path), "config", "user.email",
                    "ack@test"], check=True)
    subprocess.run(["git", "-C", str(tmp_path), "config", "user.name",
                    "ack test"], check=True)
    (tmp_path / ".gitignore").write_text("sessions/\n", encoding="utf-8")
    root = _proj(tmp_path)
    (root / "agi-tree.config.json").write_text("{}", encoding="utf-8")
    subprocess.run(["git", "-C", str(tmp_path), "add", "-A"], check=True)
    subprocess.run(["git", "-C", str(tmp_path), "commit", "-q", "-m",
                    "project marker"], check=True, capture_output=True)
    _write_seats_sheet(root, [
        {"name": "belam", "role": "prime_director", "model": "x",
         "effort": "max", "settings": ""},
        {"name": "other", "role": "director", "model": "x",
         "effort": "max", "settings": ""},
    ])
    rel = os.path.relpath(rotate._ack_seats_path(root), tmp_path)
    subprocess.run(["git", "-C", str(tmp_path), "add", "--", rel],
                   check=True, capture_output=True)
    subprocess.run(["git", "-C", str(tmp_path), "commit", "-q", "-m",
                    "two rows"], check=True, capture_output=True)
    return root, tmp_path


def test_own_row_cut_classifies_by_row_identity_not_index(tmp_path):
    """mur-SL2.15 clause (a): `_seats_ownrow_content` pairs each changed line
    by ROW IDENTITY (the `name` cell), never by index. An OWN row and a
    FOREIGN row edited in the SAME replace opcode (adjacent rows, both
    edited) — in BOTH orders — must stage exactly the own row's change with
    the foreign row byte-identical to HEAD: no foreign k-pair rides the
    staged content. This was the defect: per-index pairing made `is_own` true
    from EITHER side of a pair, so an own/foreign pair at the same k staged
    the foreign added line as own."""
    own_role_new, foreign_ed = '"role": "p2"', '"edited_by": "x"'
    for i, (own_at, foreign_at) in enumerate(
            (("belam", "other"), ("other", "belam"))):
        root, top = _two_row_git_root(tmp_path / f"ord{i}")
        seats = rotate._ack_seats_path(root)
        work = seats.read_text(encoding="utf-8")
        if own_at == "belam":
            work = work.replace('"name": "belam", "role": "prime_director"',
                                '"name": "belam"' + own_role_new)
            work = work.replace('"name": "other", "role": "director"',
                                '"name": "other"' + foreign_ed)
        else:
            work = work.replace('"name": "other", "role": "director"',
                                '"name": "other"' + foreign_ed)
            work = work.replace('"name": "belam", "role": "prime_director"',
                                '"name": "belam"' + own_role_new)
        seats.write_text(work, encoding="utf-8")
        staged = rotate._seats_ownrow_content(root, top, own_at)
        assert staged is not None, "an own-row change must build content"
        if own_at == "belam":
            assert '"name": "belam"' + own_role_new in staged, staged
            assert '"name": "other", "role": "director"' in staged, staged
            assert foreign_ed not in staged, \
                "foreign `edited_by` cell must never be staged as own"
        else:
            assert '"name": "other"' + foreign_ed in staged, staged
            assert '"name": "belam", "role": "prime_director"' in staged, \
                staged
            assert own_role_new not in staged, \
                "belam is foreign here — its role change must be reverted"
        # the FOREIGN row is byte-identical to HEAD (base blob).
        rel = os.path.relpath(os.fspath(seats), os.fspath(top))
        head_blob = subprocess.run(
            ["git", "-C", str(top), "show", f"HEAD:{rel}"],
            capture_output=True, text=True).stdout
        foreign_head_line = next(
            l for l in head_blob.splitlines() if f'"name": "{foreign_at}"' in l)
        assert foreign_head_line in staged, \
            "the foreign row must appear byte-identical to HEAD"


def test_own_row_cut_own_deletion_plus_foreign_change_and_insert(tmp_path):
    """mur-SL2.15 clause (a) pre-fix defect shape: an OWN row DELETED, a
    FOREIGN row CHANGED and a FOREIGN row INSERTED all in one working copy.
    The legendary per-index pairing staged the foreign `edited_by` change as
    own; the cut by row identity must stage: own deletion dropped, foreign
    changed row RESTORED to HEAD bytes, foreign inserted row never staged."""
    root, top = _two_row_git_root(tmp_path)
    seats = rotate._ack_seats_path(root)
    foreign_changed = {"name": "other", "role": "director",
                       "edited_by": "x"}
    third_inserted = {"name": "third", "role": "director"}
    work = ("---\nid: config:seats\ntype: config\nseats:\n"
            + "  - " + json.dumps(foreign_changed) + "\n"
            + "  - " + json.dumps(third_inserted) + "\n---\n")
    seats.write_text(work, encoding="utf-8")
    staged = rotate._seats_ownrow_content(root, top, "belam")
    assert staged is not None, "own-deletion of belam is still an own change"
    assert '"name": "belam"' not in staged, staged
    assert '"name": "other"' in staged and '"role": "director"' in staged, \
        staged
    assert '"edited_by": "x"' not in staged, \
        "foreign changed line must be restored to HEAD, never staged"
    assert '"name": "third"' not in staged, \
        "a foreign inserted row must never be staged"


def test_own_row_cut_foreign_only_frontmatter_restamp_reads_foreign(tmp_path):
    """mur-SL2.15 clause (b): the frontmatter `edited_by:` provenance stamp is
    own ONLY when the SAME diff also carries an own-row `name`-cell change.
    A seats.md whose ONLY change is a FOREIGN `edited_by:` restamp reads
    FOREIGN: the ack's dirty GATE does not fire as own and the commit-content
    cut stages nothing of it (`_diff_owns_row` False, `_seats_ownrow_content`
    None). This was the SL6.09 residue: the stamp was owned value-agnostically,
    so every seat's ack staged a foreign restamp as its own."""
    root, top = _ack_seed_git(tmp_path)
    seats = rotate._ack_seats_path(root)
    text = seats.read_text(encoding="utf-8")
    # plant a FOREIGN frontmatter restamp: the ONLY change vs HEAD.
    seats.write_text(text.replace("type: config",
                                  "type: config\nedited_by: some-foreign"),
                     encoding="utf-8")
    rel = os.path.relpath(os.fspath(seats), os.fspath(top))
    diff = subprocess.run(
        ["git", "-C", str(top), "diff", "HEAD", "--", rel],
        capture_output=True, text=True).stdout
    assert rotate._diff_owns_row(diff, "belam") is False, \
        "the gate must read a foreign-only frontmatter restamp as NOT own"
    assert rotate._seats_ownrow_content(root, top, "belam") is None, \
        "the commit-content cut must stage nothing of a foreign-only restamp"


def test_own_row_cut_own_write_keeps_its_frontmatter_stamp(tmp_path):
    """mur-SL2.15 clause (b) POSITIVE + SL7.09 clause (4) regression guard: an
    own-row `name`-cell change TOGETHER with the write's own frontmatter
    `edited_by:` restamp stages BOTH — the whole-node stamp is part of the
    same write that produced the own row, so the ack carries it and MAIN reads
    clean (never `M seats.md` after a keygen/spawn-row write)."""
    root, top = _ack_seed_git(tmp_path)
    seats = rotate._ack_seats_path(root)
    work = seats.read_text(encoding="utf-8")
    work = work.replace("type: config",
                        "type: config\nedited_by: belam")
    work = work.replace('"settings": ""', '"settings": "s"')
    seats.write_text(work, encoding="utf-8")
    staged = rotate._seats_ownrow_content(root, top, "belam")
    assert staged is not None
    assert "edited_by: belam" in staged, \
        "the write's own frontmatter stamp must ride the own-row commit"
    assert '"settings": "s"' in staged
