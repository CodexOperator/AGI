"""goal:g7.16.1.7.1.1.3 (goal:g6.41.1 P2): a dead post RESUMES its own session.

heal._recover_seat resumes a dead seat whose row carries a session_id with a
transcript under the seat's tree: `--resume <sid>` from the harness template,
the row's model, the SAME name and generation, the session_id kept on the row.
Without a transcript it is today's fresh spawn. A harness whose template has
no resume slot refuses by name rather than fresh-spawning under a resume.
Every launch goes to a fake launcher; no tmux is touched.
"""
from __future__ import annotations

import importlib.util
import sys
from pathlib import Path

BIN = Path(__file__).resolve().parents[1] / "bin"
sys.path.insert(0, str(BIN))


def _load(name):
    spec = importlib.util.spec_from_file_location(name, BIN / f"{name}.py")
    mod = importlib.util.module_from_spec(spec)
    spec.loader.exec_module(mod)
    return mod


heal = _load("heal")
SID = "0f0f0f0f-1111-2222-3333-444444444444"
ROW = {"name": "mainseat", "role": "director", "pid": 111, "worktree": "",
       "model": "claude-opus-5-5", "effort": "high", "generation": 4,
       "session_id": SID, "recover": True}


def _seed_recovery_ack(gdir):
    """config:rotations `recovery_ack` -- the recovered-seat ack wording
    (hypothesis:heal-ack-line-comes-from-config-rotations-by-role)."""
    geo = Path(gdir) / "nodes" / ".geometry"
    geo.mkdir(parents=True, exist_ok=True)
    (geo / "rotations.md").write_text(
        "---\nid: config:rotations\ntype: config\nrecovery_ack:\n"
        "  prime_director: {recovered: \"RECOVERED SEAT {seat} --gen {gen}\","
        " resumed: \"RESUMED SEAT {seat} --gen {gen}\"}\n"
        "  default: {recovered: \"RECOVERED SEAT {seat}\","
        " resumed: \"RESUMED SEAT {seat}\"}\n---\n")


def _recover(tmp_path, monkeypatch, *, transcript: bool, row=None):
    rotate = _load("rotate")
    gdir = tmp_path / "main" / ".agi"
    gdir.mkdir(parents=True, exist_ok=True)
    _seed_recovery_ack(gdir)
    monkeypatch.setattr(rotate, "CC_PROJECTS_DIR", tmp_path / "projects")
    tree = heal._seat_tree_dir(gdir, {"worktree": ""})
    if transcript:
        tp = Path(rotate.transcript_from_registry_dict(
            {"cwd": str(tree), "session_id": SID}))
        tp.parent.mkdir(parents=True, exist_ok=True)
        tp.write_text("{}\n")
    seen: list = []

    def launch(root, name, shell_cmd, window_path=None, cwd=None):
        seen.append((name, shell_cmd))
        return None, "@9"

    wf = tmp_path / "w.txt"
    wf.write_text("\n")
    out = heal._recover_seat(gdir, dict(row or ROW), "pid gone", rotate,
                             windows=[], window_path=str(wf),
                             launcher=launch, now=0.0)
    return out, seen


def test_a_dead_post_with_a_transcript_resumes_the_same_session(tmp_path, monkeypatch):
    out, seen = _recover(tmp_path, monkeypatch, transcript=True)
    assert out["respawned"] and out["resumed"] is True, out
    assert out["generation"] == 4 and out["name"] == "mainseat", out   # same gen, same name
    (_name, cmd), = seen
    assert f"--resume {SID}" in cmd and "--model claude-opus-5-5" in cmd, cmd
    assert "RESUMED SEAT" in cmd, cmd


def test_no_transcript_is_a_fresh_spawn(tmp_path, monkeypatch):
    out, seen = _recover(tmp_path, monkeypatch, transcript=False)
    assert out["respawned"] and out["resumed"] is False, out
    assert out["generation"] == 5, out   # the fresh rule: generation + 1
    (_name, cmd), = seen
    assert "--resume" not in cmd, cmd


def test_a_harness_without_a_resume_slot_refuses_by_name():
    rotate = _load("rotate")
    try:
        rotate._build_harness_command("copilot-cli", name="n", prompt_text="p",
                                      debug_file="d", resume=SID)
    except rotate.harness_template.HarnessTemplateError as exc:
        assert "no resume slot" in str(exc)
    else:
        raise AssertionError("a resume on a slot-less harness built an argv")


# ------------------------------- the row's harness on recover (goal:g7.16.1.7.1.1.5)
def _fresh_cmd(tmp_path, monkeypatch, **cells):
    gdir = tmp_path / "main" / ".agi"
    gdir.mkdir(parents=True, exist_ok=True)
    # The project declares copilot-cli, as the live config.json does, so the
    # recover's harness passes `_validate_harness` by name.
    (gdir / "config.json").write_text(
        '{"harnesses": {"copilot-cli": {"adapter": "copilot_cli"}}}')
    row = {k: v for k, v in ROW.items() if k != "harness"}
    row.update(cells)
    out, seen = _recover(tmp_path, monkeypatch, transcript=False, row=row)
    assert out["respawned"], out
    (_name, cmd), = seen
    return cmd


def test_a_copilot_row_recovers_on_the_copilot_template(tmp_path, monkeypatch):
    """RED before the fix: _recover_seat passed no harness= to spawn_window,
    so a copilot-cli seat came back as a CLAUDE argv."""
    cmd = _fresh_cmd(tmp_path, monkeypatch, harness="copilot-cli")
    argv = cmd.split(" -- ", 1)[1]          # after rotate.py launch-wrapper
    assert argv.startswith("copilot --model "), argv[:120]
    assert "--remote-control" not in argv, argv[:120]


def test_an_absent_or_empty_harness_renders_the_claude_argv_unchanged(tmp_path, monkeypatch):
    """The fix moves no live row: today's 45 rows are claude-code 38, absent 3,
    '' 4 (council 19:49Z 11-06). Absent and '' render byte-identical to an
    explicit claude-code row."""
    explicit = _fresh_cmd(tmp_path / "a", monkeypatch, harness="claude-code")
    absent = _fresh_cmd(tmp_path / "b", monkeypatch)
    empty = _fresh_cmd(tmp_path / "c", monkeypatch, harness="")
    norm = lambda c, d: c.replace(str(tmp_path / d), "<T>")   # noqa: E731
    assert explicit.split(" -- ", 1)[1].startswith("claude --remote-control "), explicit
    assert norm(absent, "b") == norm(explicit, "a") == norm(empty, "c")


# ------------------------------- the resume proof is template-declared (goal:g7.31.1.2 ACT 2c)
def _grok_recover(tmp_path, monkeypatch, heal_mod=heal):
    gdir = tmp_path / "main" / ".agi"
    gdir.mkdir(parents=True, exist_ok=True)
    (gdir / "config.json").write_text(
        '{"harnesses": {"grok-bot": {"adapter": "grok_bot", "model": "grok-4"}}}')
    lines: list = []
    monkeypatch.setattr(heal_mod, "_watch_log", lambda m: lines.append(m))
    monkeypatch.setattr(heal_mod, "_resume_sleep", lambda s: None)          # 2c-2's window
    rotate = _load("rotate")
    _seed_recovery_ack(gdir)
    monkeypatch.setattr(rotate, "CC_PROJECTS_DIR", tmp_path / "projects")   # no transcript anywhere
    monkeypatch.setattr(rotate, "_join_by_pane", lambda **kw: {"found": True, "pid": 77})
    seen: list = []

    def launch(root, name, shell_cmd, window_path=None, cwd=None):
        seen.append((name, shell_cmd))
        return None, "@9"

    wf = tmp_path / "w.txt"
    wf.write_text("\n")
    row = dict(ROW, harness="grok-bot", model="grok-4")
    out = heal_mod._recover_seat(gdir, row, "pid gone", rotate, windows=[],
                                 window_path=str(wf), launcher=launch, now=0.0)
    return out, seen, lines


def test_a_grok_row_resumes_on_its_session_id_and_names_the_proof_PROVISIONAL(tmp_path, monkeypatch):
    """grok-bot.toml declares resume_proof = "session_id": the row's sid is
    resumed with NO transcript, and heal's log names the proof PROVISIONAL +
    UNMEASURED every time (council 11-06 19:49:54Z (A)(3)); never a pass."""
    out, seen, lines = _grok_recover(tmp_path, monkeypatch)
    assert out["respawned"] and out["resumed"] is True, out
    (_name, cmd), = seen
    argv = cmd.split(" -- ", 1)[1]
    assert f" -r {SID}" in argv and " -s " not in argv, argv[:200]
    prov = [m for m in lines if "resume proof PROVISIONAL" in m]
    assert prov == [f"watch: seat mainseat resume proof PROVISIONAL "
                    f"(session_id present; UNMEASURED): resuming {SID}"], lines


def test_the_claude_transcript_proof_is_unchanged_for_a_claude_row(tmp_path, monkeypatch):
    """The same row on claude-code with no transcript stays a FRESH spawn and
    logs no PROVISIONAL line: the default proof did not move."""
    lines: list = []
    monkeypatch.setattr(heal, "_watch_log", lambda m: lines.append(m))
    out, seen = _recover(tmp_path, monkeypatch, transcript=False,
                         row=dict(ROW, harness="claude-code"))
    assert out["resumed"] is False and "--resume" not in seen[0][1], out
    assert not any("PROVISIONAL" in m for m in lines), lines


def test_mutant_heal_reads_only_the_transcript_proof_RED_on_the_grok_row(tmp_path, monkeypatch):
    src = (BIN / "heal.py").read_text()
    old = '        if _proof == "session_id":\n'
    assert src.count(old) == 1
    d = tmp_path / "mut"
    d.mkdir()
    (d / "heal_mut.py").write_text(src.replace(old, '        if False:\n'))
    spec = importlib.util.spec_from_file_location("heal_mut", d / "heal_mut.py")
    m = importlib.util.module_from_spec(spec)
    spec.loader.exec_module(m)
    out, seen, _lines = _grok_recover(tmp_path, monkeypatch, heal_mod=m)
    assert out["resumed"] is False and " -r " not in seen[0][1]     # a fresh spawn: RED


# ------------------------------- ACT 2c-2: the failed -r (alive [decision] 10:56:03Z 11-09, sp T1-T3, aio)
NEW = "11111111-2222-4333-8444-555555555555"


def _mut_heal(tmp_path, old, new):
    src = (BIN / "heal.py").read_text()
    assert src.count(old) == 1, old
    d = tmp_path / "mut"
    d.mkdir(exist_ok=True)
    (d / "heal_mut2.py").write_text(src.replace(old, new))
    spec = importlib.util.spec_from_file_location("heal_mut2", d / "heal_mut2.py")
    m = importlib.util.module_from_spec(spec)
    spec.loader.exec_module(m)
    return m


def _c2(tmp_path, monkeypatch, *, joins=None, store=None, windows="\n",
        launches=None, heal_mod=heal):
    """A grok row recovered with every outside read seamed: the pane joins
    in order, the session store path, the open windows, each launch's pid."""
    gdir = tmp_path / "main" / ".agi"
    gdir.mkdir(parents=True, exist_ok=True)
    (gdir / "config.json").write_text(
        '{"harnesses": {"grok-bot": {"adapter": "grok_bot", "model": "grok-4"}}}')
    _seed_recovery_ack(gdir)
    lines: list = []
    monkeypatch.setattr(heal_mod, "_watch_log", lambda m: lines.append(m))
    monkeypatch.setattr(heal_mod, "_resume_sleep", lambda s: None)
    monkeypatch.setattr(heal_mod, "_pane_pid_of", lambda w, p=None: 555)
    rotate = _load("rotate")
    monkeypatch.setattr(rotate, "CC_PROJECTS_DIR", tmp_path / "projects")
    q = list(joins or [{"found": True, "pid": 77}, {"found": True, "pid": 77}])
    monkeypatch.setattr(rotate, "_join_by_pane", lambda **kw: q.pop(0))
    if store is not None:
        monkeypatch.setattr(rotate, "_harness_session_store", lambda hid: store)
    rows: list = []
    monkeypatch.setattr(rotate, "_successor_row_write",
                        lambda root, **kw: rows.append(kw) or "row ok")
    rotate._rows = rows                                                   # the row write, read back below
    pids = list(launches or [None, None])
    seen: list = []

    def launch(root, name, shell_cmd, window_path=None, cwd=None):
        seen.append(shell_cmd.split(" -- ", 1)[1])
        return pids.pop(0), f"@{9 + len(seen) - 1}"

    wf = tmp_path / "w.txt"
    wf.write_text(windows)
    row = dict(ROW, harness="grok-bot", model="grok-4")
    out = heal_mod._recover_seat(gdir, row, "pid gone", rotate, windows=[],
                                 window_path=str(wf), launcher=launch, now=0.0)
    return out, seen, lines, rotate


# (B)(1) before the launch: present / absent / UNREAD, never 'absent' for a read that cannot happen
def test_b1_the_entry_present_resumes(tmp_path, monkeypatch):
    st = tmp_path / "store"
    st.mkdir()
    (st / SID).mkdir()
    out, seen, lines, _r = _c2(tmp_path, monkeypatch, store=str(st))
    assert out["resumed"] and f" -r {SID}" in seen[0], (out, seen)
    assert not any("UNREAD" in m or "absent from" in m for m in lines), lines


def test_b1_a_readable_store_without_the_entry_is_fresh_with_its_line(tmp_path, monkeypatch):
    st = tmp_path / "store"
    st.mkdir()
    out, seen, lines, _r = _c2(tmp_path, monkeypatch, store=str(st))
    assert out["resumed"] is False and " -r " not in seen[0], (out, seen)
    assert f"watch: seat mainseat session {SID} absent from {st}: fresh spawn, no resume" in lines


def test_b1_a_missing_store_is_UNREAD_the_resume_launched_and_its_mutant(tmp_path, monkeypatch):
    gone = tmp_path / "no-such-store"
    out, seen, lines, _r = _c2(tmp_path, monkeypatch, store=str(gone))
    assert out["resumed"] and f" -r {SID}" in seen[0], (out, seen)
    unread = [m for m in lines if "session store UNREAD" in m]
    assert len(unread) == 1 and f"{gone}: ENOENT" in unread[0] and "read as uid " in unread[0], lines
    m = _mut_heal(tmp_path, '        return "unread", (f"{p}: "', '        return "absent", (f"{p}: "')
    out2, seen2, _l, _r = _c2(tmp_path / "m", monkeypatch, store=str(gone), heal_mod=m)
    assert out2["resumed"] is False and " -r " not in seen2[0]          # fresh: RED


def test_b1_grok_bot_declares_no_store_today_so_every_read_is_UNREAD(tmp_path, monkeypatch):
    out, seen, lines, rot = _c2(tmp_path, monkeypatch)
    assert rot._harness_session_store("grok-bot") == ""
    assert out["resumed"] and any(
        "session store UNREAD (no session store declared by the template (UNMEASURED)" in m
        for m in lines), lines


# (B)(2) + 2c-3 (council 3/3 11:22Z-11:25Z; DG1's pick (b): no in-pass fresh launch)
GONE = [{"found": True, "pid": 77}, {"found": False, "miss": "no-pane", "why": "no pane pid for window @9"}]
OPEN = [{"found": True, "pid": 77}, {"found": False, "miss": "absent"}]


def test_b2_a_harness_that_exits_inside_the_window_reads_FAILED_and_its_mutant(tmp_path, monkeypatch):
    """The common exit: the launch-file bash ends with the harness, the
    window closes -> no-pane at the END of the window = a FAILED resume. ONE
    launch only (no in-pass fresh launch), the id leaves the row, the row
    keeps its dead pid (heal scans only pid > 0), respawned False."""
    out, seen, lines, rot = _c2(tmp_path, monkeypatch, joins=list(GONE))
    assert len(seen) == 1 and f" -r {SID}" in seen[0], seen
    assert out["respawned"] is False and out["resumed"] is False, out
    assert rot._rows[-1]["session_id"] == "" and rot._rows[-1]["pid"] is None, rot._rows
    rf = out["resume_failed"]
    assert rf == {"session_id": SID, "read": "the pane join read no-pane at the end of the 30 s "
                  "window after the -r launch (no pane pid for window @9)"}, rf
    assert sum("FAILED" in m and SID in m for m in lines) == 1, lines
    m = _mut_heal(tmp_path, "                                poll_secs=0)\n    if end.get",
                  "                                poll_secs=0)\n    end = first\n    if end.get")
    out2, _s, _l, rot2 = _c2(tmp_path / "m", monkeypatch, joins=list(GONE), heal_mod=m)
    assert out2["resumed"] and rot2._rows[-1]["session_id"] == SID          # the first hit read as resumed: RED


def test_r1_no_pane_clears_the_id_like_absent_and_its_mutant(tmp_path, monkeypatch):
    for seq, win in ((GONE, "\n"), (OPEN, "@9 mainseat\n")):
        out, seen, _l, rot = _c2(tmp_path / str(len(win)), monkeypatch, joins=list(seq), windows=win)
        assert len(seen) == 1 and rot._rows[-1]["session_id"] == "", (seq, rot._rows)
    m = _mut_heal(tmp_path, '            if kind == "ambiguous":\n',
                  '            if kind in ("ambiguous", "no-pane"):\n')
    _o, _s, _l, rot2 = _c2(tmp_path / "m", monkeypatch, joins=list(GONE), heal_mod=m)
    assert rot2._rows[-1]["session_id"] == SID                             # the dead id kept on no-pane: RED


def test_r1_ambiguous_keeps_the_id_pid_EMPTY_nothing_launched_and_its_mutant(tmp_path, monkeypatch):
    seq = [{"found": True, "pid": 77}, {"found": False, "miss": "ambiguous"}]
    out, seen, lines, rot = _c2(tmp_path, monkeypatch, joins=list(seq))
    assert len(seen) == 1 and rot._rows[-1]["session_id"] == SID and rot._rows[-1]["pid"] == 0, rot._rows
    assert "resume_failed" not in out and any("nothing launched" in m for m in lines), (out, lines)
    m = _mut_heal(tmp_path, '            if kind == "ambiguous":\n', '            if False:\n')
    _o, _s, _l, rot2 = _c2(tmp_path / "m", monkeypatch, joins=list(seq), heal_mod=m)
    assert rot2._rows[-1]["session_id"] == ""                              # the id dropped: RED


def test_nit2_a_pid_change_between_the_joins_reads_AMBIGUOUS_and_its_mutant(tmp_path, monkeypatch):
    seq = [{"found": True, "pid": 77}, {"found": True, "pid": 88}]
    out, seen, lines, rot = _c2(tmp_path, monkeypatch, joins=list(seq))
    assert len(seen) == 1 and rot._rows[-1]["session_id"] == SID and rot._rows[-1]["pid"] == 0, rot._rows
    assert any("read ambiguous" in m and "pid 77 at the launch, 88 at the end" in m for m in lines), lines
    m = _mut_heal(tmp_path, '            first.get("pid") != end.get("pid"):\n',
                  '            False:\n')
    _o, _s, _l, rot2 = _c2(tmp_path / "m", monkeypatch, joins=list(seq), heal_mod=m)
    assert rot2._rows[-1]["pid"] == 88                                     # the end join decides: RED


def test_term_a_failed_id_is_never_resumed_again_and_its_mutant(tmp_path, monkeypatch):
    """alive's TERM: once a -r reads no harness at the window's end, the next
    _recover_seat must not launch -r <that id>: the cleared row spawns fresh."""
    def twice(tp, mod):
        out, seen, _l, rot = _c2(tp, monkeypatch, joins=list(GONE), heal_mod=mod)
        nxt = dict(ROW, harness="grok-bot", model="grok-4",
                   session_id=rot._rows[-1]["session_id"])
        monkeypatch.setattr(rot, "_join_by_pane", lambda **kw: {"found": True, "pid": 99})
        seen2: list = []
        wf = tp / "w2.txt"
        wf.write_text("\n")
        mod._recover_seat(tp / "main" / ".agi", nxt, "pid gone", rot, windows=[],
                          window_path=str(wf), now=0.0,
                          launcher=lambda r, n, c, w=None, cwd=None: seen2.append(c) or (None, "@11"))
        return seen2[0].split(" -- ", 1)[1]
    second = twice(tmp_path, heal)
    assert " -r " not in second and SID not in second and " -s " in second, second
    m = _mut_heal(tmp_path, "                resume = None\n                failed = True\n",
                  "                failed = True\n")
    assert f" -r {SID}" in twice(tmp_path / "m", m)                        # -r <dead id> again: RED


def test_c_the_dead_id_is_in_the_crash_recovery_record(tmp_path, monkeypatch):
    out, _seen, _lines, rot = _c2(tmp_path, monkeypatch, joins=list(GONE))
    gdir = tmp_path / "main" / ".agi"
    path = heal._write_crash_recovery(gdir, "mainseat", "pid gone",
                                      dict(ROW, harness="grok-bot"), rot, 0.0, out)
    import json
    rec = json.loads(Path(path).read_text())
    assert rec["result"] == "detected" and rec["resume_failed"]["session_id"] == SID, rec


# 2c-4 (R6, SM 11:44Z 11-09): an ABSENT read leaves the failed window open; the row must not keep its @id
def test_r6_an_absent_read_empties_the_row_window_so_the_next_pass_reaches_recover_and_its_mutant(tmp_path, monkeypatch):
    def run(tp, mod):
        out, _seen, _l, rot = _c2(tp, monkeypatch, joins=list(OPEN), windows="@9 mainseat\n", heal_mod=mod)
        row = dict(ROW, harness="grok-bot", window=rot._rows[-1]["window"], pid=999999,
                   session_id=rot._rows[-1]["session_id"])
        calls: list = []
        monkeypatch.setattr(mod, "_recover_seat", lambda *a, **k: calls.append(1) or {"respawned": False})
        gdir = tp / "main" / ".agi"
        mod._watch_one_seat(gdir, row, [("@9", "mainseat")], rot, now=0.0,
                            pid_alive=lambda p: False, pin_table={}, seat_sessions=[],
                            rows=[row], pane_pids={})
        return rot._rows[-1]["window"], bool(calls)
    window, reached = run(tmp_path, heal)
    assert window == "" and reached, (window, reached)                 # the next pass reaches _recover_seat
    m = _mut_heal(tmp_path, '                    row_window = ""\n', '                    pass\n')
    window2, reached2 = run(tmp_path / "m", m)
    assert window2 == "@9" and not reached2                            # @id kept -> (1b) NOT dead, a silent stall: RED


def test_r6_no_pane_keeps_writing_the_launch_window(tmp_path, monkeypatch):
    """The window is gone on no-pane: (1b) cannot vouch for it anyway, so the
    row records the -r launch's window as before."""
    out, _seen, _l, rot = _c2(tmp_path, monkeypatch, joins=list(GONE))
    assert rot._rows[-1]["window"] == "@9", rot._rows


def test_r6_the_next_pass_refuses_the_open_same_name_window_by_name(tmp_path, monkeypatch):
    """aio's 2c-4 row, end to end through the REAL _recover_seat: after an
    absent read, a second pass with the failed window still listed reaches
    _recover_seat, which refuses the same-name window and launches nothing."""
    out, seen, _l, rot = _c2(tmp_path, monkeypatch, joins=list(OPEN), windows="@9 mainseat\n")
    assert len(seen) == 1 and rot._rows[-1]["window"] == ""
    row = dict(ROW, harness="grok-bot", model="grok-4", window="",
               session_id=rot._rows[-1]["session_id"])
    launched: list = []
    wf = tmp_path / "w2.txt"
    wf.write_text("@9 mainseat\n")
    out2 = heal._recover_seat(tmp_path / "main" / ".agi", row, "pid gone", rot,
                              windows=[("@9", "mainseat")], window_path=str(wf), now=0.0,
                              launcher=lambda *a, **k: launched.append(1) or (None, "@12"))
    assert not launched and out2["respawned"] is False, out2
    assert "successor window 'mainseat' already exists" in out2["reason"], out2
