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
from types import SimpleNamespace

import pytest

HOOK = Path(__file__).resolve().parents[1] / "hooks" / "rotation_alert.py"
spec = importlib.util.spec_from_file_location("rotation_alert_cap", HOOK)
hook = importlib.util.module_from_spec(spec)
spec.loader.exec_module(hook)

# the REAL handoff writer, imported once so the capture's field files are
# driven through exactly the argv the capture would spawn (tmp card only)
_REPO = Path(__file__).resolve().parents[3]
sys.path.insert(0, str(_REPO / "extensions" / "agi" / "bin"))
import rotate  # noqa: E402  (the module the hook itself lazily imports)

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


#: the LIVE card shape a director card carries: a `## ... Where it stops`
#: section whose slot is a FOUR-backtick fence wrapping a THREE-backtick
#: block, a `## Banked` section, and a state section (so the driven §0 has
#: somewhere declared to land and the diff is about the two slots only).
LIVE_SHAPE_CARD = """# probe-director card

## 🔴 STATE
- gen 4->5, f 0.41

## 🔴 Where it stops -- successor's owed list
````
```
DONE  one landed thing; a second line of the same entry
NEXT  (1) first owed step
      (2) second owed step, continued on this very line
```
````

## Banked
(b) a model scope outside the owner -- the owner's call.
"""


def _section(text, title):
    for header, body in rotate._split_card_sections(text)[1]:
        if title in header.lower():
            return header, body
    return None


def _fields_of(argv):
    out = []
    for i, a in enumerate(argv):
        if a == "--field":
            out.append([argv[i + 1], argv[i + 2]])
    return out


def test_capture_appends_its_line_and_keeps_the_slot_and_banked(
        tmp_path, run_hook, monkeypatch, capsys):
    """hypothesis:captive-capture-keeps-the-slot-and-banked-and-appends-its-
    line: the driven handoff the capture spawns must APPEND its one capture
    line to the card's own where-it-stops slot and leave BANKED byte-
    identical. The pre-fix bytes passed the SAME one-line file as both s3 and
    s6, so the writer REPLACED the fenced slot payload (the successor's whole
    owed list) and the whole BANKED section -- and the old test only asserted
    the line was PRESENT, so the destruction was green (RED-FIRST)."""
    graph, cwd = _graph(tmp_path, extra="card_capture_minutes: 10\n")
    monkeypatch.setenv("AGI_SEAT", "probe-director")
    monkeypatch.setenv("AGI_HOOK_NO_SPAWN", "1")
    monkeypatch.setattr(hook, "_work_last_ts", lambda *a, **k: 2_000_000_000)
    state_dir = tmp_path / "state-keep"
    card = _stale_state(tmp_path, graph, state_dir)
    card.write_text(LIVE_SHAPE_CARD, encoding="utf-8")   # the LIVE shape
    before = card.read_text(encoding="utf-8")
    tp = tmp_path / "keep.jsonl"
    _transcript(tp, 45_000)                     # over the line
    code, out, err = run_hook(_payload(graph, tp, "s-keep", cwd), state_dir,
                              monkeypatch, capsys)
    assert code == 0, err
    assert len(hook._CAPTURE_LOGGED) == 2, hook._CAPTURE_LOGGED
    rc = rotate.cmd_handoff(
        SimpleNamespace(driven=True, seat="probe-director",
                        field=_fields_of(hook._CAPTURE_LOGGED[0]), dry_run=False),
        graph)
    assert rc == 0, capsys.readouterr().err
    after = card.read_text(encoding="utf-8")

    # (1) the owed list survives, and the fences are neither broken nor doubled
    stop_head, stop_after = _section(after, "where it stops")
    _stop_head, stop_before = _section(before, "where it stops")
    for owed in ("DONE  one landed thing; a second line of the same entry",
                 "NEXT  (1) first owed step",
                 "      (2) second owed step, continued on this very line"):
        assert owed in stop_after, owed
    assert after.count("````") == before.count("````") == 2, after
    assert after.count("\n```\n") == before.count("\n```\n"), after

    # (2) the ONLY change in the slot is the appended capture line (the
    # writer's own trailing-blank normalisation is not a content change)
    def _content(lines):
        return [ln for ln in lines if ln.strip()]

    b_lines = _content(stop_before.splitlines())
    a_all = stop_after.splitlines()
    a_lines = _content(a_all)
    added = [ln for ln in a_all if "auto-captured at f=" in ln]
    assert len(added) == 1, a_all
    assert a_all.index(added[0]) > a_all.index("NEXT  (1) first owed step")
    assert [ln for ln in a_lines if ln not in added] == b_lines, (
        b_lines, a_lines)

    # (3) BANKED is byte-identical -- nothing appended, nothing replaced
    assert _section(after, "banked") == _section(before, "banked"), after


#: the slot shapes the SECOND writer must preserve, named here and RESOLVED
#: inside the row below: the LIVE fenced card, the live cards' HYBRID shape
#: and the two UNFENCED prose shapes (their fixtures are declared further down
#: this file, so the mapping cannot be a module constant). Closes
#: STEP2_CARDS_UNCOVERED, the DH.569 residue.
#: the UNFENCED prose shapes FAIL the same conjunct through the SECOND writer
#: -- a real defect in rotate.py, which is OUT OF THIS ROUND'S FILE SCOPE, so
#: the rows are `xfail(strict=True)`: they track the defect, and they ARM
#: themselves (XPASS = suite RED) the day rotate.py is fixed. Reasons name the
#: measured bytes, not a guess.
STEP2_XFAIL = {
    "h2": "rotate._write_stops_section WRAPS the unfenced prose slot in a "
          "``` fence: every owed byte survives, but two lines are ADDED beyond "
          "the one capture line (rotate.py:18091, _render_stops_block)",
    "h3": "rotate._replace_stops_body returns the whole body (`return s3`, "
          "sub_offset is None on this shape) and the `### Where it stops` "
          "subheader is GONE from the card afterwards -- the section this row "
          "diffs is not even there (rotate.py:8080-8103)",
}
STEP2_PARAMS = [
    pytest.param(s, marks=pytest.mark.xfail(strict=True, reason=r))
    for s, r in sorted(STEP2_XFAIL.items())
] + [pytest.param(s) for s in ("live", "hybrid")]


@pytest.mark.parametrize("shape", STEP2_PARAMS)
def test_capture_rotate_self_step_keeps_the_owed_slot(
        shape, tmp_path, run_hook, monkeypatch, capsys):
    """The chain's SECOND writer, not just the first: argv[1]'s --stops must
    carry the owed list too, because `rotate._write_stops_section` REPLACES the
    whole fenced region. Pre-fix it was `_stops_line` -- `stops: <subject> |
    last dm:` with no owed list -- so rotate-self destroyed the slot the
    handoff had just preserved (RED-FIRST). Parametrised over the LIVE fenced
    shape AND the hybrid/unfenced prose shapes, so the second writer is not
    green on the fenced card alone (DH.569 residue, STEP2_CARDS_UNCOVERED)."""
    shape_card = {"live": LIVE_SHAPE_CARD, "hybrid": HYBRID_SLOT_CARD,
                  "h2": UNFENCED_SLOT_CARDS["h2"][0],
                  "h3": UNFENCED_SLOT_CARDS["h3"][0]}[shape]
    graph, cwd = _graph(tmp_path, extra="card_capture_minutes: 10\n")
    monkeypatch.setenv("AGI_SEAT", "probe-director")
    monkeypatch.setenv("AGI_HOOK_NO_SPAWN", "1")
    monkeypatch.setattr(hook, "_work_last_ts", lambda *a, **k: 2_000_000_000)
    state_dir = tmp_path / f"state-step2-{shape}"
    card = _stale_state(tmp_path, graph, state_dir)
    card.write_text(shape_card, encoding="utf-8")
    tp = tmp_path / f"step2-{shape}.jsonl"
    _transcript(tp, 45_000)
    code, out, err = run_hook(_payload(graph, tp, f"s-step2-{shape}", cwd),
                              state_dir, monkeypatch, capsys)
    assert code == 0, err
    _handoff, rot = hook._CAPTURE_LOGGED
    assert rotate.cmd_handoff(
        SimpleNamespace(driven=True, seat="probe-director",
                        field=_fields_of(hook._CAPTURE_LOGGED[0]),
                        dry_run=False), graph) == 0
    stops = rot[rot.index("--stops") + 1]
    full, slot = rotate._write_stops_section(card, "probe-director", stops)
    assert full, slot
    # EXACT, not substring (a substring passes on a mangled line): every
    # non-blank line but the one capture line EQUALS the before list.
    a_all = _section(card.read_text(encoding="utf-8"), "where it stops")[1].splitlines()
    added = [ln for ln in a_all if "auto-captured at f=" in ln]
    assert len(added) == 1, a_all
    assert [ln for ln in a_all if ln not in added and ln.strip()] == [
        ln for ln in _section(shape_card, "where it stops")[1].splitlines()
        if ln.strip()], a_all


#: the SECOND writer over the shapes the fenced row above cannot reach --
#: NAMED, NOT COVERED (the 40-line cap went to the M1 gate row and the
#: exact-line tightening above, per the brief's cut order):
STEP2_CARDS_UNCOVERED = ("HYBRID_SLOT_CARD", "UNFENCED_SLOT_CARDS[h2]", "UNFENCED_SLOT_CARDS[h3]")


def test_capture_warns_soft_when_the_warning_template_is_unreadable(
        tmp_path, monkeypatch, capsys):
    """M1 GATE ROW: `render` is fail-HARD and the warning used to print INSIDE
    `_capture_stops`' except-block, so a typo'd template name raised out of the
    every-prompt hook. Unreadable template: bare line back, nothing raised."""
    import prose_templates
    monkeypatch.setattr(prose_templates, "_TEMPLATE_ROOT", tmp_path / "gone")
    line = hook._capture_stops(tmp_path / "absent.md", "auto-captured at f=0.5")
    assert line == "auto-captured at f=0.5", line
    assert "absent.md" in capsys.readouterr().out


def test_unreadable_card_prints_the_slot_blind_warning(tmp_path, capsys):
    """ITEM 2a: the stdout warning is not silent — a card that cannot be read
    degrades to the bare line AND says so on stdout (the capture is the only
    warning channel the seat ever sees)."""
    line = hook._capture_stops(tmp_path / "absent.md", "auto-captured at f=0.5")
    assert line == "auto-captured at f=0.5", line
    assert "carries NO owed list" in capsys.readouterr().out


def test_rotate_self_argv_keeps_the_authorized_stops_line_byte_identical(
        tmp_path):
    """NEGATIVE CONTROL for the M3 guard, a ROW and not a probe: the guard at
    `_rotate_self_argv` is SHARED, so its one authorised caller -- the
    threshold path, whose value is `_stops_line()` -- must come out
    BYTE-IDENTICAL and still start with the literal "stops: ". No other row
    asserts that: making the guard unconditional leaves every committed row
    green, because a capture payload never starts with `-`."""
    value = hook._stops_line(tmp_path, "probe-director")
    assert value.startswith("stops: "), value
    argv = hook._rotate_self_argv(tmp_path / "bin", "probe-director", value)
    assert argv[argv.index("--stops") + 1] == value, argv


def test_rotate_self_argv_never_starts_with_a_bare_dash(tmp_path):
    """M3 GATE: a `--stops` value starting with a BARE `-` is an OPTION to
    argparse and exits 2 (measured -- the seat would not rotate)."""
    argv = hook._rotate_self_argv(tmp_path, "probe-director", "-dash\nsecond")
    assert argv[argv.index("--stops") + 1].startswith("\n"), argv


#: the two UNFENCED slot shapes. `##`-level (doc:card-belam's own: a `##` heading
#: with a plain prose body) and `###`-level (a subheader inside a `##` section,
#: unfenced prose below it). Parent PROBE C lost the `###` header byte here:
#: `rotate._replace_stops_body` fell through to `return s3`, the WHOLE body
#: subheader included, so the prose survived and the heading did not.
UNFENCED_SLOT_CARDS = {
    "h2": ("""# probe-director card

## 🔴 STATE
- gen 4->5, f 0.41

## 🔴 Where it stops -- successor's owed list
DONE  one landed thing; a second line of the same entry
NEXT  (1) first owed step
      (2) second owed step, continued on this very line

## Banked
(b) a model scope outside the owner -- the owner's call.
(b) a second banked option, kept byte for byte.
""", "where it stops"),
    "h3": ("""# probe-director card

## 🔴 STATE
- gen 4->5, f 0.41

## 🔴 §5 The loop
### 🔴 Where it stops
DONE  one landed thing; a second line of the same entry
NEXT  (1) first owed step
      (2) second owed step, continued on this very line

## Banked
(b) a model scope outside the owner -- the owner's call.
(b) a second banked option, kept byte for byte.
""", "the loop"),
}


@pytest.mark.parametrize("shape", sorted(UNFENCED_SLOT_CARDS))
def test_capture_keeps_unfenced_stops_slot_and_banked(
        shape, tmp_path, run_hook, monkeypatch, capsys):
    """The same conjunct-1 claim on the UNFENCED slot shapes: the `##`-level
    prose slot and the `###`-level prose subheader. The capture still APPENDS
    its one line, and every other byte of the slot -- the heading line above
    all -- and of BANKED survives verbatim (RED-FIRST on `h3`: the
    `### 🔴 Where it stops` header was gone from the card afterwards)."""
    card_text, slot_title = UNFENCED_SLOT_CARDS[shape]
    graph, cwd = _graph(tmp_path, extra="card_capture_minutes: 10\n")
    monkeypatch.setenv("AGI_SEAT", "probe-director")
    monkeypatch.setenv("AGI_HOOK_NO_SPAWN", "1")
    monkeypatch.setattr(hook, "_work_last_ts", lambda *a, **k: 2_000_000_000)
    state_dir = tmp_path / f"state-unfenced-{shape}"
    card = _stale_state(tmp_path, graph, state_dir)
    card.write_text(card_text, encoding="utf-8")
    before = card.read_text(encoding="utf-8")
    tp = tmp_path / f"unfenced-{shape}.jsonl"
    _transcript(tp, 45_000)                     # over the line
    code, out, err = run_hook(_payload(graph, tp, f"s-{shape}", cwd), state_dir,
                              monkeypatch, capsys)
    assert code == 0, err
    assert len(hook._CAPTURE_LOGGED) == 2, hook._CAPTURE_LOGGED
    rc = rotate.cmd_handoff(
        SimpleNamespace(driven=True, seat="probe-director",
                        field=_fields_of(hook._CAPTURE_LOGGED[0]), dry_run=False),
        graph)
    assert rc == 0, capsys.readouterr().err
    after = card.read_text(encoding="utf-8")

    # (1) the heading line of the slot survives VERBATIM
    before_head, stop_before = _section(before, slot_title)
    after_head, stop_after = _section(after, slot_title)
    assert after_head == before_head, (before_head, after_head)

    # (2) the only change in the slot is the appended capture line
    a_all = stop_after.splitlines()
    added = [ln for ln in a_all if "auto-captured at f=" in ln]
    assert len(added) == 1, a_all
    keep = [ln for ln in a_all if ln not in added and ln.strip()]
    assert keep == [ln for ln in stop_before.splitlines() if ln.strip()], (
        stop_before, stop_after)

    # (3) BANKED is byte-identical
    assert _section(after, "banked") == _section(before, "banked"), after


#: the LIVE cards' HYBRID slot shape (doc:card-belam's own bytes): a `##`
#: heading, then a PROSE line carrying the timestamp+one-line state, then the
#: fenced owed list. NEITHER committed fixture has it -- `LIVE_SHAPE_CARD` is
#: fence-immediately-after-the-heading, the two `UNFENCED_SLOT_CARDS` have no
#: fence at all -- so the shape the live cards actually carry was covered by a
#: PARENT PROBE and by no committed row. Here the prose line is the byte at
#: risk: `_fenced_payload` starts at the fence, so the payload it builds carries
#: no prose, and only the WRITER keeping everything above the fence saves it.
HYBRID_SLOT_CARD = """# probe-director card

## State (13:1xZ 09-27)
| | |
|---|---|
| post | probe-S2-L5-XIII gen 13 |

## Where it stops -- successor's owed list
13:1xZ 09-27 probe-S2-L5-XIII: account drained, paid mur paths closed; resume waits on the zero-usd fix
```
0. RESUME (OWNER 13:0xZ, no funds): DE [decision] 13:1xZ -- zero_usd lanes mint below the floor.
   OWED after DH.501 merges up: F13 'Spend checked by hand' -> 'Spend by hand'.
1. CHECK every 4 h (cron f86b1cf9, skill agi-merge-pass).
```

## Banked
(b) a model scope outside the owner -- the owner's call.
(b) a second banked option, kept byte for byte.
"""


def test_capture_keeps_the_hybrid_prose_then_fence_slot_and_banked(
        tmp_path, run_hook, monkeypatch, capsys):
    """The same conjunct-1 claim on the LIVE card's HYBRID shape: a PROSE
    line between the heading and the fence. The capture still APPENDS its one
    line, and the heading AND the prose line AND every owed byte survive
    verbatim, with the fence neither broken nor doubled. This row is
    LOAD-BEARING, not a green duplicate: with `hook._capture_stops` swapped
    back to its pre-fix bare-line form on this same card, 3 of the 4 owed
    lines are gone (the prose line above the fence survives only because the
    writer keeps everything above it) -- the appended line is then the whole
    slot, and the successor inherits nothing (RED-FIRST)."""
    graph, cwd = _graph(tmp_path, extra="card_capture_minutes: 10\n")
    monkeypatch.setenv("AGI_SEAT", "probe-director")
    monkeypatch.setenv("AGI_HOOK_NO_SPAWN", "1")
    monkeypatch.setattr(hook, "_work_last_ts", lambda *a, **k: 2_000_000_000)
    state_dir = tmp_path / "state-hybrid"
    card = _stale_state(tmp_path, graph, state_dir)
    card.write_text(HYBRID_SLOT_CARD, encoding="utf-8")
    before = card.read_text(encoding="utf-8")
    tp = tmp_path / "hybrid.jsonl"
    _transcript(tp, 45_000)                     # over the line
    code, out, err = run_hook(_payload(graph, tp, "s-hybrid", cwd), state_dir,
                              monkeypatch, capsys)
    assert code == 0, err
    assert len(hook._CAPTURE_LOGGED) == 2, hook._CAPTURE_LOGGED
    rc = rotate.cmd_handoff(
        SimpleNamespace(driven=True, seat="probe-director",
                        field=_fields_of(hook._CAPTURE_LOGGED[0]), dry_run=False),
        graph)
    assert rc == 0, capsys.readouterr().err
    after = card.read_text(encoding="utf-8")

    # (1) the heading AND the prose line above the fence survive VERBATIM
    before_head, stop_before = _section(before, "where it stops")
    after_head, stop_after = _section(after, "where it stops")
    assert after_head == before_head, (before_head, after_head)
    prose = stop_before.splitlines()[0]
    assert prose, stop_before
    assert prose in stop_after.splitlines(), (prose, stop_after)

    # (2) the owed list survives and the fence is neither broken nor doubled
    for owed in ("0. RESUME (OWNER 13:0xZ, no funds)",
                 "   OWED after DH.501 merges up",
                 "1. CHECK every 4 h (cron f86b1cf9, skill agi-merge-pass)."):
        assert owed in stop_after, owed
    assert after.count("\n```\n") == before.count("\n```\n") == 2, after

    # (3) the ONLY change in the slot is the appended capture line, and it
    # lands INSIDE the fence, after the last owed step
    a_all = stop_after.splitlines()
    added = [ln for ln in a_all if "auto-captured at f=" in ln]
    assert len(added) == 1, a_all
    assert a_all.index(added[0]) > a_all.index(
        "1. CHECK every 4 h (cron f86b1cf9, skill agi-merge-pass).")
    keep = [ln for ln in a_all if ln not in added and ln.strip()]
    assert keep == [ln for ln in stop_before.splitlines() if ln.strip()], (
        stop_before, stop_after)

    # (4) BANKED is byte-identical -- nothing appended, nothing replaced
    assert _section(after, "banked") == _section(before, "banked"), after
