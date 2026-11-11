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
    m = _mut(tmp_path, "    for r in rows:\n        name = (r.get(\"name\") or \"\").strip()\n        hid = str(r.get(\"harness\") or \"\").strip()",
             "    for r in []:\n        name = (r.get(\"name\") or \"\").strip()\n        hid = str(r.get(\"harness\") or \"\").strip()")
    joined, writes, lines = _retry(tmp_path, monkeypatch, join={"found": False, "miss": "absent"}, heal_mod=m)
    assert joined == [] and writes == [] and not any("has no pid" in x for x in lines)


def test_the_watch_pass_calls_the_retry_before_its_pid_scan():
    """The retry is wired into _watch_seats ahead of the pid > 0 loop (a removed call reads RED here)."""
    src = (BIN / "heal.py").read_text()
    body = src[src.index("def _watch_seats("):]
    body = body[:body.index("\ndef ", 1)]
    assert "_retry_empty_pid_joins(root, rows, windows, _rotate)" in body
    assert body.index("_retry_empty_pid_joins(") < body.index("for row in pid_rows:")


def test_retry_skips_rows_it_must_not_touch(tmp_path, monkeypatch):
    """A row with a pid, a claude row, a closed window: none is joined or named."""
    rows_in = [{"name": "a", "harness": "grok-bot", "pid": 7, "window": "@9"},
               {"name": "b", "pid": "", "window": "@9"},
               {"name": "c", "harness": "grok-bot", "pid": "", "window": "@8"}]
    joined, writes, lines = _retry(tmp_path, monkeypatch, join={"found": True, "pid": 1}, rows_in=rows_in)
    assert joined == [] and writes == [] and lines == []
