"""Tests for the meter hook's IMPERATIVE block + FORCE capture (conjuncts 1/2).

hypothesis:l5-the-meter-captures-the-final-card-and-forces-the-rotation-itself

Red-first, build-order:
  (1) a payload at f >= line prints the imperative block (exact string);
  (2) an unread `rotate now` from the holder prints it BELOW the line;
  (3) a stale card N minutes after the first imperative -> handoff + rotate-self
      --force invoked, argv recorded, NOTHING spawned under AGI_HOOK_NO_SPAWN;
  (4) the captured card carries AUTO-CAPTURED and a non-empty stops line.
"""
import importlib.util
import io
import json
import os
import subprocess
import sys
from pathlib import Path

import pytest

HOOK = Path(__file__).resolve().parents[1] / "hooks" / "rotation_alert.py"
spec = importlib.util.spec_from_file_location("rotation_alert_cap", HOOK)
hook = importlib.util.module_from_spec(spec)
spec.loader.exec_module(hook)

#: every argv the capture WOULD run through the ONE `_Popen` seam.
_SPAWNS: list[list[str]] = []


@pytest.fixture(autouse=True)
def _no_inherited_seat(monkeypatch):
    monkeypatch.delenv("AGI_SEAT", raising=False)


@pytest.fixture(autouse=True)
def _no_real_spawn(monkeypatch):
    monkeypatch.delenv("AGI_HOOK_NO_SPAWN", raising=False)
    _SPAWNS.clear()
    hook._CAPTURE_LOGGED.clear()

    class _FakeProc:
        pid = 2 ** 24

    monkeypatch.setattr(hook, "_Popen",
                        lambda argv, **_kw: (_SPAWNS.append(argv), _FakeProc())[1])


@pytest.fixture
def run_hook():
    def _run(payload, state_dir, monkeypatch, capsys):
        monkeypatch.setenv("AGI_ROTATION_STATE_DIR", str(state_dir))
        monkeypatch.setattr(sys, "stdin", io.StringIO(json.dumps(payload)))
        code = hook.main([])
        cap = capsys.readouterr()
        return code, cap.out, cap.err
    return _run


def _graph(tmp_path, extra=""):
    graph = tmp_path / "outer" / "proj" / ".agi"
    (graph / "nodes" / ".geometry").mkdir(parents=True)
    (graph / "config.json").write_text("{}")
    (graph / "nodes" / ".geometry" / "ladder.md").write_text(
        "---\ndirector_context_tokens: 100000\ndirector_rotate_at: 0.25\n"
        "capture_chain_log: capture-chain.log\n" + extra + "---\n")
    (graph / "nodes" / ".geometry" / "seats.md").write_text(
        "---\nseats:\n"
        "  - {\"name\": \"probe-director\", \"role\": \"director\", "
        "\"worktree\": \".agi/worktrees/seat-probe-director\", "
        "\"rotated_by\": \"sanctuary-director\", "
        "\"rotate_at\": 0.4}\n---\n")
    cwd = graph / "worktrees" / "seat-probe-director"
    cwd.mkdir(parents=True, exist_ok=True)
    return graph, cwd


def _transcript(path, tokens):
    path.write_text(json.dumps({"message": {"role": "assistant", "usage": {
        "input_tokens": tokens, "cache_read_input_tokens": 0,
        "cache_creation_input_tokens": 0}}}) + "\n")


def _payload(graph, tp, session, cwd):
    return {"hook_event_name": "UserPromptSubmit", "session_id": session,
            "transcript_path": str(tp), "cwd": str(cwd)}


EXPECTED = ("ROTATE NOW: (a) write the card wholesale now, (b) run python3 "
            "extensions/agi/bin/rotate.py rotate; nothing else this turn")


def test_imperative_at_or_over_the_line(tmp_path, run_hook, monkeypatch, capsys):
    """Conjunct 1: f >= line prints the imperative block verbatim, and the
    [meter] line stays the LAST stdout line."""
    graph, cwd = _graph(tmp_path)
    monkeypatch.setenv("AGI_SEAT", "probe-director")
    tp = tmp_path / "over.jsonl"
    _transcript(tp, 45_000)                     # 0.45 >= 0.4 -> over the line
    state_dir = tmp_path / "state-over"
    state_dir.mkdir()
    code, out, err = run_hook(_payload(graph, tp, "s-over", cwd), state_dir,
                              monkeypatch, capsys)
    assert code == 0, err
    assert EXPECTED in out, out
    assert out.strip().splitlines()[-1].startswith("[meter]"), out


def test_over_line_payload_is_imperative_without_the_band(tmp_path, run_hook,
                                                          monkeypatch, capsys):
    """Residue 1: at/over the line the hook's additional context is the
    IMPERATIVE block, NOT a number and a band. The pre-fix bytes printed the
    imperative and THEN `{f} of {t} window (N% of the line)` -- exactly the
    form conjunct 1 forbids. The deferral reason (if any) is not the band and
    stays; the [meter] line stays LAST."""
    graph, cwd = _graph(tmp_path)
    monkeypatch.setenv("AGI_SEAT", "probe-director")
    tp = tmp_path / "over-band.jsonl"
    _transcript(tp, 45_000)                     # 0.45 >= 0.4 -> over the line
    state_dir = tmp_path / "state-over-band"
    state_dir.mkdir()
    code, out, err = run_hook(_payload(graph, tp, "s-over-band", cwd),
                              state_dir, monkeypatch, capsys)
    assert code == 0, err
    assert EXPECTED in out, out
    assert "% of the line" not in out, out
    assert "of 0.250 window" not in out, out
    assert out.strip().splitlines()[-1].startswith("[meter]"), out


def test_imperative_on_unread_rotate_now_below_the_line(tmp_path, run_hook,
                                                        monkeypatch, capsys):
    """Conjunct 1: an UNREAD `rotate now` in the seat's inbox prints the
    imperative block even below the line (0.10 < 0.25)."""
    graph, cwd = _graph(tmp_path)
    monkeypatch.setenv("AGI_SEAT", "probe-director")
    inbox = graph / "sessions" / "inbox" / "probe-director.md"
    inbox.parent.mkdir(parents=True, exist_ok=True)
    inbox.write_text("---\nfrom: sanctuary-director\nrotate now\n")
    tp = tmp_path / "below.jsonl"
    _transcript(tp, 10_000)                     # 0.10 < 0.25
    state_dir = tmp_path / "state-below"
    state_dir.mkdir()
    code, out, err = run_hook(_payload(graph, tp, "s-below", cwd), state_dir,
                              monkeypatch, capsys)
    assert code == 0, err
    assert EXPECTED in out, out
    assert out.strip().splitlines()[-1].startswith("[meter]"), out


def _stale_state(tmp_path, graph, state_dir, minutes_ago=600):
    card = graph / "sessions" / "quorum" / "probe-director.md"
    card.parent.mkdir(parents=True, exist_ok=True)
    card.write_text("# probe-director card\n")
    os.utime(card, (1, 1))
    state_dir.mkdir(exist_ok=True)
    (state_dir / "capture-probe-director.json").write_text(
        json.dumps({"first": int(__import__("time").time()) - minutes_ago}))
    return card


def test_force_capture_after_n_minutes_records_argv(tmp_path, run_hook,
                                                    monkeypatch, capsys):
    """Conjunct 2: card stale 10 min after the first imperative -> the driven
    handoff AND rotate-self --force --stops are invoked; under
    AGI_HOOK_NO_SPAWN nothing is spawned, the argv is RECORDED."""
    graph, cwd = _graph(tmp_path, extra="card_capture_minutes: 10\n")
    monkeypatch.setenv("AGI_SEAT", "probe-director")
    monkeypatch.setenv("AGI_HOOK_NO_SPAWN", "1")
    monkeypatch.setattr(hook, "_work_last_ts", lambda *a, **k: 2_000_000_000)
    state_dir = tmp_path / "state-cap"
    _stale_state(tmp_path, graph, state_dir)
    tp = tmp_path / "cap.jsonl"
    _transcript(tp, 45_000)                     # over the line
    code, out, err = run_hook(_payload(graph, tp, "s-cap", cwd), state_dir,
                              monkeypatch, capsys)
    assert code == 0, err
    assert [a for a in _SPAWNS if "rotate-self" in a or "handoff" in a] == []
    assert len(hook._CAPTURE_LOGGED) == 2, hook._CAPTURE_LOGGED
    handoff, rot = hook._CAPTURE_LOGGED
    assert handoff[2:5] == ["handoff", "--driven", "--seat"], handoff
    assert handoff[handoff.index("--seat") + 1] == "probe-director"
    assert "s3" in handoff and "s6" in handoff
    assert "rotate-self" in rot and "--force" in rot
    stops = rot[rot.index("--stops") + 1]
    assert "auto-captured at f=" in stops, stops
    assert "10 min without a self-rotate" in stops, stops


def _session_stamp(state_dir, seat, minutes_ago, session):
    """A capture stamp NAMING the session that wrote it. Pre-fix bytes wrote
    only `first`, so a successor session inherited the predecessor's grace."""
    (state_dir / f"capture-{seat}.json").write_text(json.dumps({
        "first": int(__import__("time").time()) - int(minutes_ago * 60),
        "session": session}) + "\n")


def test_successor_session_waits_the_full_capture_grace(
        tmp_path, run_hook, monkeypatch, capsys):
    """EF.22 conjunct 2: a stamp written by a PREDECESSOR session is NOT this
    session's grace. Session s-A crossed over the line (stamp 10 min old);
    session s-B's first crossing must WAIT -- the pre-fix reader ignored the
    session and force-captured at once (RED-FIRST)."""
    graph, cwd = _graph(tmp_path, extra="card_capture_minutes: 10\n")
    monkeypatch.setenv("AGI_SEAT", "probe-director")
    monkeypatch.setenv("AGI_HOOK_NO_SPAWN", "1")
    monkeypatch.setattr(hook, "_work_last_ts", lambda *a, **k: 2_000_000_000)
    state_dir = tmp_path / "state-sess"
    _stale_state(tmp_path, graph, state_dir)
    _session_stamp(state_dir, "probe-director", 10, "s-A")
    tp = tmp_path / "sessb.jsonl"
    _transcript(tp, 45_000)                     # over the line
    code, out, err = run_hook(_payload(graph, tp, "s-B", cwd), state_dir,
                              monkeypatch, capsys)
    assert code == 0, err
    assert hook._CAPTURE_LOGGED == [], hook._CAPTURE_LOGGED
    blob = json.loads((state_dir / "capture-probe-director.json").read_text())
    assert blob.get("session") == "s-B", blob


def test_same_session_old_stamp_still_captures(tmp_path, run_hook,
                                               monkeypatch, capsys):
    """EF.22 conjunct 2 complement: the session scoping must not over-block --
    a stamp NAMING the CURRENT session and 10 min old still captures."""
    graph, cwd = _graph(tmp_path, extra="card_capture_minutes: 10\n")
    monkeypatch.setenv("AGI_SEAT", "probe-director")
    monkeypatch.setenv("AGI_HOOK_NO_SPAWN", "1")
    monkeypatch.setattr(hook, "_work_last_ts", lambda *a, **k: 2_000_000_000)
    state_dir = tmp_path / "state-same"
    _stale_state(tmp_path, graph, state_dir)
    _session_stamp(state_dir, "probe-director", 10, "s-A")
    tp = tmp_path / "samea.jsonl"
    _transcript(tp, 45_000)
    code, out, err = run_hook(_payload(graph, tp, "s-A", cwd), state_dir,
                              monkeypatch, capsys)
    assert code == 0, err
    assert len(hook._CAPTURE_LOGGED) == 2, hook._CAPTURE_LOGGED


def test_captured_card_carries_auto_captured_marker(tmp_path, run_hook,
                                                    monkeypatch, capsys):
    """Conjunct 2 (4): the AUTO-CAPTURED record lands in the hook's OWN state
    dir (never in the card) and the generated stops line is non-empty.
    hypothesis:the-captive-capture-never-writes-into-the-live-card-..."""
    graph, cwd = _graph(tmp_path, extra="card_capture_minutes: 10\n")
    monkeypatch.setenv("AGI_SEAT", "probe-director")
    monkeypatch.setattr(hook, "_work_last_ts", lambda *a, **k: 2_000_000_000)
    state_dir = tmp_path / "state-marker"
    card = _stale_state(tmp_path, graph, state_dir)
    tp = tmp_path / "marker.jsonl"
    _transcript(tp, 45_000)
    code, out, err = run_hook(_payload(graph, tp, "s-marker", cwd), state_dir,
                              monkeypatch, capsys)
    assert code == 0, err
    text = card.read_text()
    assert not text.startswith(hook.AUTO_CAPTURED), text
    marker = state_dir / "capture-probe-director.captured"
    assert hook.AUTO_CAPTURED in marker.read_text()
    rots = [a for a in _SPAWNS if "rotate-self" in a]
    assert len(rots) == 1, _SPAWNS
    assert len([a for a in _SPAWNS if "handoff" in a]) == 1, _SPAWNS
    stops = rots[0][rots[0].index("--stops") + 1]
    assert stops.strip(), "stops line must never be empty"
    assert "auto-captured at f=" in stops, stops


def test_capture_is_one_ordered_child_handoff_then_rotate_self(
        tmp_path, run_hook, monkeypatch, capsys):
    """Residue 2: handoff must COMPLETE before rotate-self reads the card
    (`--stops` is built from the card). The pre-fix bytes Popen-ed handoff and
    rotate-self as two concurrent fire-and-forget children with no ordering
    guarantee. The built shape is ONE background child -- `bash -c` chains the
    two argvs with `&&`, argv passed positionally so nothing is shell-
    interpolated -- so rotate-self cannot start until handoff exits."""
    graph, cwd = _graph(tmp_path, extra="card_capture_minutes: 10\n")
    monkeypatch.setenv("AGI_SEAT", "probe-director")
    monkeypatch.setattr(hook, "_work_last_ts", lambda *a, **k: 2_000_000_000)
    state_dir = tmp_path / "state-order"
    _stale_state(tmp_path, graph, state_dir)
    tp = tmp_path / "order.jsonl"
    _transcript(tp, 45_000)
    code, out, err = run_hook(_payload(graph, tp, "s-order", cwd), state_dir,
                              monkeypatch, capsys)
    assert code == 0, err
    assert len(_SPAWNS) == 1, _SPAWNS
    argv = _SPAWNS[0]
    assert argv[0] == "bash" and argv[1] == "-c", argv
    assert hook._CHAIN_SCRIPT in argv[2], argv
    joined = " ".join(argv)
    assert "handoff" in joined and "rotate-self" in joined, argv
    assert joined.index("handoff") < joined.index("rotate-self"), argv
    assert "--stops" in argv, argv
    # The failure marker rides the child as its FIRST positional arg ($1).
    assert argv[4].endswith("capture-probe-director.failed"), argv


def _real_bash(monkeypatch):
    """The ONE `_Popen` seam back to the real subprocess: these two tests run
    the chain's OWN bash with STAND-IN argvs (never rotate.py, never a live
    seat, never the real /tmp state dir)."""
    monkeypatch.setattr(hook, "_Popen", subprocess.Popen)


def _stand_ins(tmp_path, refuse_first):
    """`python3 -c` stand-ins: a step that exits 1, and a step that touches a
    file so the probe can SEE it ran."""
    ran = tmp_path / ("ran-handoff" if refuse_first else "ran-rotate")
    handoff = ["python3", "-c", (f"open({str(ran)!r},'w').write('h');"
                                 "import sys; sys.exit(1)")] if refuse_first else [
        "python3", "-c", f"open({str(ran)!r},'w').write('h')"]
    rot_ran = tmp_path / "ran-rotate"
    rotate = ["python3", "-c", f"open({str(rot_ran)!r},'w').write('r')"]
    return handoff, rotate, ran, rot_ran


def _run_chain(tmp_path, monkeypatch, refuse_first):
    state_dir = tmp_path / "state-chain"
    state_dir.mkdir(exist_ok=True)
    handoff, rotate, _ran, rot_ran = _stand_ins(tmp_path, refuse_first)
    fail = state_dir / "capture-probe-director.failed"
    log = (state_dir / "capture-chain.log").open("ab")
    _real_bash(monkeypatch)
    hook._spawn_capture_chain(fail, log, handoff, rotate)
    log.close()
    for _ in range(100):
        if rot_ran.is_file():
            break
        __import__("time").sleep(0.05)
    __import__("time").sleep(0.3)   # the child's last append
    return fail, rot_ran, tmp_path / "ran-handoff"


def test_chain_rotates_even_after_a_refusing_handoff(tmp_path, monkeypatch):
    """Conjunct 1 (TMM.223): the pre-fix `&&` chain SKIPPED rotate-self when
    the driven handoff refused (the 100-line card guard), while the stamp had
    already latched `captured` -> no retry, no report, 3.5 h idle. The built
    chain runs rotate-self ANYWAY and records the refusing step's rc."""
    fail, rot_ran, _ = _run_chain(tmp_path, monkeypatch, refuse_first=True)
    assert rot_ran.is_file(), "rotate-self stand-in must run after a refusal"
    assert fail.read_text().strip() == "handoff rc=1", fail.read_text()


def test_chain_leaves_no_marker_when_both_steps_succeed(tmp_path, monkeypatch):
    """The success path is UNCHANGED: both steps run in order, nothing fails,
    and no marker is written (no line the seat does not need)."""
    state_dir = tmp_path / "state-ok"
    state_dir.mkdir()
    _handoff, _rotate, h_ran, rot_ran = _stand_ins(tmp_path, False)
    fail = state_dir / "capture-probe-director.failed"
    log = (state_dir / "capture-chain.log").open("ab")
    _real_bash(monkeypatch)
    hook._spawn_capture_chain(fail, log, _handoff, _rotate)
    log.close()
    for _ in range(100):
        if rot_ran.is_file():
            break
        __import__("time").sleep(0.05)
    __import__("time").sleep(0.3)
    assert h_ran.is_file() and rot_ran.is_file()
    assert not fail.exists(), fail.read_text()


def test_a_failed_step_is_named_to_the_seat_and_cleared(tmp_path, run_hook,
                                                        monkeypatch, capsys):
    """Conjunct 2: any non-zero chain step leaves ONE line the seat READS --
    naming the step AND its rc -- not only the ladder's /tmp capture log. The
    hook reads and CLEARS the marker, so the line is read exactly once."""
    graph, cwd = _graph(tmp_path)
    monkeypatch.setenv("AGI_SEAT", "probe-director")
    state_dir = tmp_path / "state-note"
    state_dir.mkdir()
    fail = state_dir / "capture-probe-director.failed"
    fail.write_text("rotate-self rc=1\n")
    tp = tmp_path / "note.jsonl"
    _transcript(tp, 10_000)                     # 0.10 < 0.25 -> below the line
    payload = _payload(graph, tp, "s-note", cwd)
    code, out, err = run_hook(payload, state_dir, monkeypatch, capsys)
    assert code == 0, err
    named = [ln for ln in out.splitlines() if "capture-chain step FAILED" in ln]
    assert len(named) == 1, out
    assert "rotate-self" in named[0] and "rc=1" in named[0], named[0]
    assert not fail.exists(), "the marker must be CLEARED after being read"
    assert out.strip().splitlines()[-1].startswith("[meter]"), out
    _code, out2, _err = run_hook(payload, state_dir, monkeypatch, capsys)
    assert not [ln for ln in out2.splitlines() if "rc=" in ln], out2


def test_rotate_now_from_unrelated_sender_is_silent_below_the_line(
        tmp_path, run_hook, monkeypatch, capsys):
    """P1 regression (class auth): an unread `rotate now` from a sender that
    is neither the seat row's `rotated_by` holder nor the owner prints NO
    imperative — the claim restricts the triggering dm to the authoriser."""
    graph, cwd = _graph(tmp_path)
    monkeypatch.setenv("AGI_SEAT", "probe-director")
    inbox = graph / "sessions" / "inbox" / "probe-director.md"
    inbox.parent.mkdir(parents=True, exist_ok=True)
    inbox.write_text("---\nfrom: random-unrelated-seat\nrotate now\n")
    tp = tmp_path / "unrelated.jsonl"
    _transcript(tp, 10_000)                     # 0.10 < 0.25
    state_dir = tmp_path / "state-unrelated"
    state_dir.mkdir()
    code, out, err = run_hook(_payload(graph, tp, "s-unrel", cwd), state_dir,
                              monkeypatch, capsys)
    assert code == 0, err
    assert EXPECTED not in out, out


def test_below_line_holder_rotate_now_forces_capture(tmp_path, run_hook,
                                                     monkeypatch, capsys):
    """P4 regression (class wire): an unread `rotate now` from the HOLDER,
    BELOW the line, card stale N min after the first fire -> the capture runs
    (handoff + rotate-self --force argv recorded under AGI_HOOK_NO_SPAWN)."""
    graph, cwd = _graph(tmp_path, extra="card_capture_minutes: 10\n")
    monkeypatch.setenv("AGI_SEAT", "probe-director")
    monkeypatch.setenv("AGI_HOOK_NO_SPAWN", "1")
    monkeypatch.setattr(hook, "_work_last_ts",
                        lambda *a, **k: int(__import__("time").time()) - 60)
    inbox = graph / "sessions" / "inbox" / "probe-director.md"
    inbox.parent.mkdir(parents=True, exist_ok=True)
    inbox.write_text("---\nfrom: sanctuary-director\nrotate now\n")
    state_dir = tmp_path / "state-below-force"
    _stale_state(tmp_path, graph, state_dir)
    tp = tmp_path / "below-force.jsonl"
    _transcript(tp, 10_000)                     # 0.10 < 0.25 -> below the line
    code, out, err = run_hook(_payload(graph, tp, "s-below-force", cwd),
                              state_dir, monkeypatch, capsys)
    assert code == 0, err
    assert EXPECTED in out, out
    assert len(hook._CAPTURE_LOGGED) == 2, hook._CAPTURE_LOGGED
    handoff, rot = hook._CAPTURE_LOGGED
    assert handoff[2:5] == ["handoff", "--driven", "--seat"], handoff
    assert "rotate-self" in rot and "--force" in rot, rot
    assert "auto-captured at f=" in rot[rot.index("--stops") + 1]
