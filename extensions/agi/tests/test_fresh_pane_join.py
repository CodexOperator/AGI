"""goal:g7.31.1.4 -- a FRESH launch of a registry-none harness writes the HARNESS pid and its -s session id to the row.

F1 run 5 of goal:g7.31.1.2 (belam 06:04Z 11-11): on a fresh stand-up heal._recover_seat got pid None from the launcher
and wrote the PANE pid (a bash) with an empty session_id; only the resume branch joined; a grok seat never acks. Rows:

  fresh grok-bot launch, the pane join HITS  -> row pid = the harness pid, session_id = its -s value, a 'joined' line
  fresh grok-bot launch, the pane join MISSES -> row pid EMPTY (0), a line naming the miss kind, never the pane pid
  CONTROL: a fresh claude-code launch -> the pane pid as today, no pane join called
  target 4 (aio 06:11:59Z): a registry-none row with an EMPTY pid and an open window is re-joined each pass; a hit
  writes the row, a miss names the row (the seat-dead scan keeps only pid > 0 rows, so it would vanish silently)

Each of the first two and the target-4 rows carries a source-text mutant that reads RED.
"""
from __future__ import annotations

import importlib.util
import sys
from pathlib import Path

BIN = Path(__file__).resolve().parents[1] / "bin"
sys.path.insert(0, str(BIN))


def _load(name, path=None):
    spec = importlib.util.spec_from_file_location(name, path or BIN / f"{name}.py")
    mod = importlib.util.module_from_spec(spec)
    spec.loader.exec_module(mod)
    return mod


heal = _load("heal")
SID = "11111111-2222-4333-8444-555555555555"
FRESH_BLOCK_HEAD = "    fresh_sid = \"\"\n    if (not resume and not failed and window_id and _hid\n"


def _mut(tmp_path, old, new):
    src = (BIN / "heal.py").read_text()
    assert src.count(old) == 1, old
    d = tmp_path / "mut"
    d.mkdir(exist_ok=True)
    p = d / "heal_mut_fresh.py"
    p.write_text(src.replace(old, new))
    return _load("heal_mut_fresh", p)


def _seed(gdir):
    geo = Path(gdir) / "nodes" / ".geometry"
    geo.mkdir(parents=True, exist_ok=True)
    (geo / "rotations.md").write_text(
        "---\nid: config:rotations\ntype: config\nrecovery_ack:\n"
        "  default: {recovered: \"RECOVERED SEAT {seat}\", resumed: \"RESUMED SEAT {seat}\"}\n---\n")
    (Path(gdir) / "config.json").write_text(
        '{"harnesses": {"grok-bot": {"adapter": "grok_bot", "model": "grok-4"}}}')


def _fresh(tmp_path, monkeypatch, *, harness="grok-bot", join=None, heal_mod=heal):
    """A row with NO session_id (a fresh spawn), every outside read seamed: the pane pid 555 (the shell), the
    pane join's answer, the row write captured."""
    gdir = tmp_path / "main" / ".agi"
    gdir.mkdir(parents=True, exist_ok=True)
    _seed(gdir)
    lines: list = []
    monkeypatch.setattr(heal_mod, "_watch_log", lambda m: lines.append(m))
    monkeypatch.setattr(heal_mod, "_resume_sleep", lambda s: None)
    monkeypatch.setattr(heal_mod, "_pane_pid_of", lambda w, p=None: 555)
    rotate = _load("rotate")
    monkeypatch.setattr(rotate, "CC_PROJECTS_DIR", tmp_path / "projects")
    calls: list = []

    def _join(**kw):
        calls.append(kw)
        return dict(join or {"found": True, "pid": 4242, "session_id": SID})
    monkeypatch.setattr(rotate, "_join_by_pane", _join)
    rows: list = []
    monkeypatch.setattr(rotate, "_successor_row_write", lambda root, **kw: rows.append(kw) or "row ok")

    def launch(root, name, shell_cmd, window_path=None, cwd=None):
        return None, "@9"
    wf = tmp_path / "w.txt"
    wf.write_text("\n")
    row = {"name": "fseat", "role": "director", "pid": 111, "worktree": "", "generation": 1,
           "session_id": "", "recover": True, "harness": harness,
           "model": "grok-4" if harness == "grok-bot" else "claude-opus-5-5"}
    if harness == "claude-code":
        row.pop("harness")
    heal_mod._recover_seat(gdir, row, "pid gone", rotate, windows=[], window_path=str(wf),
                           launcher=launch, now=0.0)
    return rows, lines, calls


# --- the fresh path ---------------------------------------------------------------------------------------------

def test_a_fresh_grok_launch_writes_the_harness_pid_and_its_session_id(tmp_path, monkeypatch):
    rows, lines, calls = _fresh(tmp_path, monkeypatch)
    assert rows[-1]["pid"] == 4242 and rows[-1]["session_id"] == SID
    assert calls and calls[0]["window_id"] == "@9" and calls[0]["harness"] == "grok-bot"
    assert any("fresh launch joined: grok-bot pid 4242" in m for m in lines)


def test_mutant_no_fresh_join_writes_the_pane_shell_pid_RED(tmp_path, monkeypatch):
    """The old write: the pane pid 555 (a shell) and an empty session_id -- run 5's wall."""
    m = _mut(tmp_path, FRESH_BLOCK_HEAD, "    fresh_sid = \"\"\n    if (False and not resume and not failed and window_id and _hid\n")
    rows, _lines, _calls = _fresh(tmp_path, monkeypatch, heal_mod=m)
    assert rows[-1]["pid"] == 555 and rows[-1]["session_id"] == ""


def test_a_fresh_grok_miss_writes_pid_EMPTY_and_names_the_kind(tmp_path, monkeypatch):
    rows, lines, _calls = _fresh(tmp_path, monkeypatch, join={"found": False, "miss": "absent",
                                                              "note": "pane join for @9 missed: no process"})
    # aio 06:18:45Z (a): pid EMPTY, but the minted -s uuid is KEPT from the launch line, marked not read back
    import re
    assert rows[-1]["pid"] == 0
    assert re.fullmatch(r"[0-9a-f]{8}-[0-9a-f]{4}-[0-9a-f]{4}-[0-9a-f]{4}-[0-9a-f]{12}", rows[-1]["session_id"])
    assert any("the pane join read absent" in m and "never the pane shell's" in m
               and rows[-1]["session_id"] + " kept from the launch line, NOT read back" in m for m in lines)


def test_mutant_a_miss_drops_the_minted_session_id_RED(tmp_path, monkeypatch):
    """(b) instead of (a): an empty id on a miss leaves the seat unresumable even after target 4 finds its pid."""
    m = _mut(tmp_path, "            fresh_sid = _launch_line_session(shell_cmd, _hid, _rotate)\n",
             "            fresh_sid = \"\"\n")
    rows, _lines, _calls = _fresh(tmp_path, monkeypatch, heal_mod=m, join={"found": False, "miss": "absent", "note": ""})
    assert rows[-1]["session_id"] == ""


def test_mutant_a_miss_keeps_the_pane_pid_RED(tmp_path, monkeypatch):
    m = _mut(tmp_path, "        else:\n            row_pid = 0\n            # aio 06:18:45Z, (a)",
             "        else:\n            # aio 06:18:45Z, (a)")
    rows, _lines, _calls = _fresh(tmp_path, monkeypatch, heal_mod=m,
                                  join={"found": False, "miss": "absent", "note": ""})
    assert rows[-1]["pid"] == 555


def test_control_a_fresh_claude_launch_is_unchanged_and_joins_no_pane(tmp_path, monkeypatch):
    rows, lines, calls = _fresh(tmp_path, monkeypatch, harness="claude-code")
    assert rows[-1]["pid"] == 555 and not calls
    assert not any("fresh launch" in m for m in lines)


# --- target 4: an EMPTY pid is re-joined each pass, or named --------------------------------------------------------

def _retry(tmp_path, monkeypatch, *, join, heal_mod=heal, rows_in=None):
    lines: list = []
    monkeypatch.setattr(heal_mod, "_watch_log", lambda m: lines.append(m))
    monkeypatch.setattr(heal_mod.boxes, "row_is_local", lambda root, r: True)
    rotate = _load("rotate")
    monkeypatch.setattr(rotate, "_join_by_pane", lambda **kw: dict(join))
    writes: list = []
    monkeypatch.setattr(rotate, "_successor_row_write", lambda root, **kw: writes.append(kw) or "row ok")
    rows = rows_in or [{"name": "gseat", "harness": "grok-bot", "pid": "", "window": "@9", "role": "director",
                        "generation": 2}]
    joined = heal_mod._retry_empty_pid_joins(tmp_path, rows, [("@9", "gseat")], rotate)
    return joined, writes, lines


def test_an_empty_pid_registry_none_row_is_rejoined_and_written(tmp_path, monkeypatch):
    joined, writes, lines = _retry(tmp_path, monkeypatch, join={"found": True, "pid": 4243, "session_id": SID})
    assert joined == ["gseat"] and writes[-1]["pid"] == 4243 and writes[-1]["session_id"] == SID
    assert any("had no pid; the pane join found grok-bot pid 4243" in m for m in lines)


def test_an_empty_pid_row_that_still_misses_is_named_every_pass(tmp_path, monkeypatch):
    for _ in range(2):
        joined, writes, lines = _retry(tmp_path, monkeypatch, join={"found": False, "miss": "absent"})
        assert joined == [] and writes == []
        assert any("seat gseat has no pid (grok-bot, window @9 open): the pane join read absent" in m for m in lines)


def test_mutant_the_pid_filter_alone_drops_the_row_silently_RED(tmp_path, monkeypatch):
    """Without the retry the seat-dead scan's pid > 0 filter is all there is: the row is neither joined nor named."""
    m = _mut(tmp_path, "    joined: list[str] = []\n    for r in rows:\n", "    joined: list[str] = []\n    for r in []:\n")
    joined, writes, lines = _retry(tmp_path, monkeypatch, join={"found": False, "miss": "absent"}, heal_mod=m)
    assert joined == [] and writes == [] and not any("has no pid" in x for x in lines)


def test_the_watch_pass_calls_the_retry_before_its_pid_scan():
    """The retry is wired into _watch_seats ahead of the pid > 0 loop (a removed call reads RED here)."""
    src = (BIN / "heal.py").read_text()
    body = src[src.index("def _watch_seats("):]
    body = body[:body.index("\ndef ", 1)]
    assert "_retry_empty_pid_joins(root, rows, windows, _rotate)" in body
    assert body.index("_retry_empty_pid_joins(") < body.index("for row in scan:")


ROWS_ABC = [{"name": "a", "harness": "grok-bot", "pid": 7, "window": "@9"},
            {"name": "b", "pid": "", "window": "@9"},
            {"name": "c", "harness": "grok-bot", "pid": "", "window": "@8"}]


def test_retry_skips_rows_it_must_not_touch_and_a_closed_window_is_a_dead_seat(tmp_path, monkeypatch):
    """A row with a pid and a claude row: the retry and the dead-seat hand-off both leave them. Row 'c' (grok-bot, pid
    EMPTY, window @8 CLOSED): the retry does not join it, and (B) names it a dead seat and hands it on, every pass."""
    joined, writes, lines = _retry(tmp_path, monkeypatch, join={"found": True, "pid": 1},
                                   rows_in=[dict(r) for r in ROWS_ABC])
    assert joined == [] and writes == [] and lines == []
    for _ in range(2):
        lines.clear()
        dead = heal._empty_pid_closed_window_rows(tmp_path, [dict(r) for r in ROWS_ABC], [("@9", "a")])
        assert [r["name"] for r in dead] == ["c"]
        assert lines == ["watch: seat c has no pid (grok-bot) and its window @8 is CLOSED: a dead seat, "
                         "handed to the dead-seat path"]


def test_mutant_a_closed_window_empty_pid_row_is_skipped_silently_RED(tmp_path, monkeypatch):
    """The tip's silent skip: the row is neither named nor handed on -- dead and never respawned."""
    m = _mut(tmp_path, "                or not win or win in present\n", "                or True\n")
    lines: list = []
    monkeypatch.setattr(m, "_watch_log", lambda x: lines.append(x))
    monkeypatch.setattr(m.boxes, "row_is_local", lambda root, r: True)
    assert m._empty_pid_closed_window_rows(tmp_path, [dict(r) for r in ROWS_ABC], [("@9", "a")]) == []
    assert lines == []


# --- (B): the hand-off reaches the DEAD path, never pid_alive(0) (os.kill(0, 0) reads the process GROUP alive) -------

def _one(tmp_path, monkeypatch, *, empty_pid_dead, heal_mod=heal):
    gdir = tmp_path / "main" / ".agi"
    gdir.mkdir(parents=True, exist_ok=True)
    _seed(gdir)
    lines: list = []
    monkeypatch.setattr(heal_mod, "_watch_log", lambda m: lines.append(m))
    rotate = _load("rotate")
    row = {"name": "c", "harness": "grok-bot", "pid": "", "window": "@8", "role": "director", "generation": 2,
           "recover": False, "model": "grok-4"}
    out = heal_mod._watch_one_seat(gdir, row, [("@9", "a")], rotate, now=0.0, pid_alive=lambda p: True,
                                   pin_table={}, seat_sessions=[], rows=[row], pane_pids={},
                                   empty_pid_dead=empty_pid_dead)
    return out, lines


def test_a_handed_on_empty_pid_row_is_named_DEAD_like_a_dead_pid(tmp_path, monkeypatch):
    out, lines = _one(tmp_path, monkeypatch, empty_pid_dead=True)
    assert out.get("seat") == "c", (out, lines)
    assert any(m.startswith("watch: DEAD seat c ") for m in lines), lines
    assert any("c is recover:false; named only" in m for m in lines), lines


def test_control_an_empty_pid_row_not_handed_on_is_not_a_candidate(tmp_path, monkeypatch):
    out, lines = _one(tmp_path, monkeypatch, empty_pid_dead=False)
    assert out == {} and not any("DEAD" in m for m in lines)


def test_mutant_the_hand_off_asks_pid_alive_of_pid_0_RED(tmp_path, monkeypatch):
    m = _mut(tmp_path, "    _gone = (lambda: True) if _empty_dead else (lambda: not pid_alive(pid))\n",
             "    _gone = (lambda: not pid_alive(pid))\n")
    out, lines = _one(tmp_path, monkeypatch, empty_pid_dead=True, heal_mod=m)
    assert out == {} and not any("DEAD" in x for x in lines)


def test_the_watch_pass_hands_closed_window_rows_to_the_dead_path():
    src = (BIN / "heal.py").read_text()
    body = src[src.index("def _watch_seats("):]
    body = body[:body.index("\ndef ", 1)]
    assert "dead_empty = _empty_pid_closed_window_rows(root, rows, windows)" in body
    assert "scan = pid_rows + dead_empty" in body and "empty_pid_dead=id(row) in dead_ids" in body


# --- (A): a retry hit with no -s KEEPS the row's session_id ---------------------------------------------------------

def test_a_retry_hit_with_no_s_keeps_the_rows_session_id_and_says_so(tmp_path, monkeypatch):
    rows_in = [{"name": "gseat", "harness": "grok-bot", "pid": "", "window": "@9", "session_id": SID}]
    joined, writes, lines = _retry(tmp_path, monkeypatch, join={"found": True, "pid": 4244, "session_id": ""},
                                   rows_in=rows_in)
    assert joined == ["gseat"] and writes[-1]["session_id"] == SID
    assert any(f"the join read no -s; session_id {SID} KEPT from the row, NOT read back" in m for m in lines), lines


def test_mutant_a_retry_hit_with_no_s_writes_EMPTY_RED(tmp_path, monkeypatch):
    m = _mut(tmp_path, "            sid = read_sid or row_sid\n", "            sid = read_sid\n")
    rows_in = [{"name": "gseat", "harness": "grok-bot", "pid": "", "window": "@9", "session_id": SID}]
    _joined, writes, _lines = _retry(tmp_path, monkeypatch, join={"found": True, "pid": 4244, "session_id": ""},
                                     rows_in=rows_in, heal_mod=m)
    assert writes[-1]["session_id"] == ""


def test_a_retry_miss_line_carries_the_joins_note(tmp_path, monkeypatch):
    _joined, _writes, lines = _retry(tmp_path, monkeypatch, join={"found": False, "miss": "absent",
                                                                 "note": "pane join for @9 missed: x; saw: bash/bash, grok/grok"})
    assert any("the pane join read absent (pane join for @9 missed: x; saw: bash/bash, grok/grok)" in m for m in lines)
