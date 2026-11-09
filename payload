"""goal:g7.31.1.2 ACT 2b -- the registry-free seat join, template-declared.

A harness whose template declares `[session] registry = "none"` (grok-bot)
keeps no `~/.claude/sessions/<pid>.json`, so its seat is joined through the
tmux pane's process tree: the ONE process launched as the template's `bin`
at the SHALLOWEST depth under (and including) the pane pid, and the session
id read back from that same process's argv. Council terms (alive [decision]
17:59:23Z 11-07): (sp) the HARNESS pid, never the pane shell; (T1) the pane
pid is itself a candidate (an inline launch execs the harness AS the pane
pid; the launch-file path makes it a child); (T2) argv[0] AS LAUNCHED, never
/proc/<pid>/exe; none or >1 at the shallowest depth -> pid EMPTY + ONE loud
line; (sp) session AND resume together refused by name. Claude's registry
join stays the default, byte-identical.

The process rows are REAL trees (`bash` + `exec -a grok-bot python3 ...`),
read through the real `ps -e` table and /proc; only tmux's pane-pid read is
stubbed. Each mutant row loads a source-text copy of the module with one
change and reads RED on the row it guards.
"""
import importlib.util
import os
import re
import signal
import subprocess
import sys
import time
from pathlib import Path

import pytest

BIN = Path(__file__).resolve().parents[1] / "bin"
sys.path.insert(0, str(Path(__file__).resolve().parents[2]))
sys.path.insert(0, str(BIN))
from agi.bin import harness_template  # noqa: E402
from agi.bin import rotate  # noqa: E402

UUID = "0f0f0f0f-1111-2222-3333-444444444444"
UUID_RE = re.compile(r"^[0-9a-f]{8}-[0-9a-f]{4}-4[0-9a-f]{3}-[89ab][0-9a-f]{3}-[0-9a-f]{12}$")
# a stand-in "harness": a sleeping python whose argv[0] is grok-bot
FAKE = "exec -a grok-bot python3 -c 'import time; time.sleep(60)' --model m -s " + UUID


def _mutant(tmp_path, src: Path, old: str, new: str, name: str):
    text = src.read_text()
    assert text.count(old) == 1, old
    d = tmp_path / "mut"
    d.mkdir(exist_ok=True)
    (d / f"{name}.py").write_text(text.replace(old, new))
    spec = importlib.util.spec_from_file_location(name, d / f"{name}.py")
    m = importlib.util.module_from_spec(spec)
    spec.loader.exec_module(m)
    return m


@pytest.fixture
def tree():
    """Start `bash -c <line>` in its own process group; yield (pid, kids());
    kill the whole group after."""
    procs = []

    def start(line: str) -> int:
        p = subprocess.Popen(["bash", "-c", line], start_new_session=True,
                             stdin=subprocess.DEVNULL,
                             stdout=subprocess.DEVNULL,
                             stderr=subprocess.DEVNULL)
        procs.append(p)
        return p.pid

    yield start
    for p in procs:
        try:
            os.killpg(p.pid, signal.SIGKILL)
        except ProcessLookupError:
            pass
        p.wait(timeout=5)


def _settle(pane: int, want_depth_hits: int = 1, timeout: float = 5.0):
    """Wait until the tree under `pane` holds the expected grok-bot count."""
    end = time.time() + timeout
    while time.time() < end:
        table = rotate._read_ps_parent_table()
        under = [pane] + [p for p in rotate._descendant_chain(pane)]
        if sum(rotate._argv0_is(p, "grok-bot") for p in under if p in table or p == pane) >= want_depth_hits:
            return
        time.sleep(0.05)


# --- rows: T1, the pane pid is a candidate and the SHALLOWEST match wins -----------------------------------------------

def test_inline_exec_the_harness_IS_the_pane_pid(tree):
    """`bash -c 'exec ...'` (rotate.py's inline `cd <dir> && <line>`
    under bash) replaces the pane shell: the harness pid == the pane pid."""
    pane = tree(FAKE)
    _settle(pane)
    pid, why = rotate._pane_harness_pid(pane, "grok-bot")
    assert pid == pane and why == "depth 0", (pid, why)


def test_launch_file_the_harness_is_a_child_of_the_pane_shell(tree):
    """The launch-FILE path keeps the shell and runs the harness under it:
    the harness pid is the CHILD, never the pane shell (sp's term)."""
    pane = tree(f"({FAKE}); sleep 60")
    _settle(pane)
    pid, why = rotate._pane_harness_pid(pane, "grok-bot")
    assert pid is not None and pid != pane and why == "depth 1", (pid, why)
    assert rotate._read_ps_parent_table()[pid] == pane


def test_mutant_A_always_the_pane_pid_reads_RED_on_the_launch_file_row(tree, tmp_path):
    m = _mutant(tmp_path, BIN / "rotate.py",
                "    if parent_of is None:\n        parent_of = _read_ps_parent_table()\n"
                "    children: dict[int, list[int]] = {}\n",
                "    return pane_pid, 'depth 0'\n", "rot_mutA")
    pane = tree(f"({FAKE}); sleep 60")
    _settle(pane)
    assert m._pane_harness_pid(pane, "grok-bot")[0] == pane          # the SHELL: RED
    assert rotate._pane_harness_pid(pane, "grok-bot")[0] != pane     # the real code: the child


def test_mutant_B_descendants_only_reads_RED_on_the_inline_exec_row(tree, tmp_path):
    m = _mutant(tmp_path, BIN / "rotate.py",
                "    level, seen, depth = [pane_pid], {pane_pid}, 0\n",
                "    level, seen, depth = sorted(c for c, pp in parent_of.items() if pp == pane_pid), {pane_pid}, 1\n",
                "rot_mutB")
    pane = tree(FAKE)
    _settle(pane)
    assert m._pane_harness_pid(pane, "grok-bot")[0] is None           # the pane pid never read: RED
    assert rotate._pane_harness_pid(pane, "grok-bot")[0] == pane


# --- rows: T2, argv[0] AS LAUNCHED; none or more than one at the shallowest depth is EMPTY ------------------------------

def test_two_matches_at_the_shallowest_depth_is_EMPTY_never_a_pick(tree):
    pane = tree(f"({FAKE}) & ({FAKE}) & wait")
    _settle(pane, 2)
    pid, why = rotate._pane_harness_pid(pane, "grok-bot")
    assert pid is None and why.startswith("2 processes launched as 'grok-bot' at depth 1"), why


def test_no_match_is_EMPTY_and_names_what_it_looked_for(tree):
    pane = tree("sleep 60; :")
    time.sleep(0.2)
    pid, why = rotate._pane_harness_pid(pane, "grok-bot")
    assert pid is None and why == f"no process launched as 'grok-bot' under pane pid {pane}"


def test_argv0_is_read_as_launched_not_the_exe(tree):
    """The stand-in's exe is python3 and its comm is python3; only argv[0]
    says grok-bot. Matching the exe would miss it (T2)."""
    pane = tree(FAKE)
    _settle(pane)
    assert Path(os.readlink(f"/proc/{pane}/exe")).name.startswith("python")
    assert rotate._argv0_is(pane, "grok-bot")
    assert not rotate._argv0_is(pane, "grok")


# --- rows: the join -- one lookup gives pid AND session; a miss is ONE loud line, pid EMPTY ----------------------------

def _grok_join(monkeypatch, pane, poll=0):
    monkeypatch.setattr(rotate, "_pane_pid", lambda w: pane)
    return rotate._join_by_pane(seat="g1", window_id="@77", harness="grok-bot",
                                poll_secs=poll)


def test_join_reads_the_harness_pid_and_its_own_session_argv(tree, monkeypatch):
    pane = tree(f"({FAKE}); sleep 60")
    _settle(pane)
    j = _grok_join(monkeypatch, pane)
    assert j["found"] and j["pid"] != pane and j["session_id"] == UUID, j
    assert rotate._read_ps_parent_table()[j["pid"]] == pane


def test_join_reads_a_restart_session_from_the_resume_flag(tree, monkeypatch):
    pane = tree(FAKE.replace(" -s ", " -r "))
    _settle(pane)
    j = _grok_join(monkeypatch, pane)
    assert j["found"] and j["pid"] == pane and j["session_id"] == UUID, j


def test_join_miss_prints_ONE_loud_line_and_leaves_pid_EMPTY(tree, monkeypatch, capsys):
    pane = tree(f"({FAKE}) & ({FAKE}) & wait")
    _settle(pane, 2)
    j = _grok_join(monkeypatch, pane)
    err = capsys.readouterr().err.strip().splitlines()
    assert not j["found"] and "pid" not in j, j
    assert len(err) == 1 and err[0].startswith("join: miss (seat 'g1', harness 'grok-bot': 2 processes"), err


def test_the_harness_exits_while_its_shell_lingers_the_joined_pid_reads_dead(tree, monkeypatch, capsys):
    """sp's term: the committed pid is the HARNESS's, so when it exits under a
    lingering pane shell, a liveness read of the row pid reads DEAD."""
    pane = tree(f"({FAKE}); sleep 60")
    _settle(pane)
    j = _grok_join(monkeypatch, pane)
    os.kill(j["pid"], signal.SIGKILL)
    end = time.time() + 5
    while not rotate._pid_gone(j["pid"]) and time.time() < end:
        time.sleep(0.05)
    assert rotate._pid_gone(j["pid"]) and not rotate._pid_gone(pane)
    assert not _grok_join(monkeypatch, pane)["found"]


# --- rows: the branch is template-declared; claude's registry join is untouched ------------------------------------------

def test_a_grok_row_takes_the_pane_join_and_a_claude_row_the_registry(tmp_path, monkeypatch):
    calls = []
    monkeypatch.setattr(rotate, "_join_by_pane",
                        lambda **kw: calls.append(kw) or {"found": True, "pid": 1})
    monkeypatch.setattr(rotate, "_find_seat", lambda root, s: {"harness": "grok-bot"})
    assert rotate._join_successor(root=tmp_path, seat="g1", window_id="@5",
                                  poll_secs=0)["pid"] == 1
    assert calls and calls[0]["harness"] == "grok-bot"
    # a claude row (and a row with no harness cell) reads the registry
    reg = tmp_path / "reg"
    reg.mkdir()
    (reg / "4242.json").write_text('{"sessionId": "S", "cwd": "/x", "tmuxWindow": "@5"}')
    for row in ({"harness": "claude-code"}, {}, None):
        monkeypatch.setattr(rotate, "_find_seat", lambda root, s, row=row: row)
        calls.clear()
        j = rotate._join_successor(root=tmp_path, seat="c1", window_id="@5",
                                   registry_dir=str(reg), poll_secs=1)  # 0 never reads (today's loop)
        assert not calls and j["found"] and j["pid"] == 4242, (row, j)


def test_every_template_but_grok_bot_keeps_the_claude_registry():
    for hid in harness_template.available():
        want = "none" if hid == "grok-bot" else "claude"
        assert harness_template.session_registry(hid) == want, hid


def test_an_unknown_session_registry_is_refused_by_name(tmp_path, monkeypatch):
    (tmp_path / "x.toml").write_text('id = "x"\n[session]\nregistry = "grok"\n')
    monkeypatch.setattr(harness_template, "template_dir", lambda: tmp_path)
    with pytest.raises(harness_template.HarnessTemplateError, match="unknown session.registry 'grok'"):
        harness_template.load("x")


# --- rows: the mint, before launch; session AND resume together refused BY NAME -----------------------------------------

def _build(hid, **kw):
    return rotate._build_harness_command(hid, name="n", prompt_text="CARD",
                                         debug_file="/tmp/d", model="m",
                                         bin_path=f"/x/{hid}", **kw)


def test_a_grok_first_spawn_mints_a_fresh_uuid4_and_a_restart_never_does():
    a, b = _build("grok-bot"), _build("grok-bot")
    assert a[3] == "-s" and UUID_RE.match(a[4]) and a[4] != b[4], (a, b)
    r = _build("grok-bot", resume=UUID)
    assert "-s" not in r and r[r.index("-r") + 1] == UUID, r


def test_claude_code_argv_is_byte_identical_no_session_minted():
    """claude-code declares no `session` slot: the mint never reaches it."""
    got = _build("claude-code")
    assert got == harness_template.render(
        "claude-code", prompt="CARD", model="m", name="n", debug_file="/tmp/d",
        bin_path="/x/claude-code")
    assert not any(UUID_RE.match(t) for t in got)


def test_session_and_resume_together_are_refused_by_name_and_its_mutant(tmp_path):
    with pytest.raises(harness_template.HarnessTemplateError,
                       match=f"refusing to render session {UUID} AND resume {UUID} together"):
        harness_template.render("grok-bot", bin_path="/x/g", session=UUID, resume=UUID)
    m = _mutant(tmp_path, BIN / "harness_template.py", "    if session and resume:\n",
                "    if False:\n", "ht_mut")
    argv = m.render("grok-bot", bin_path="/x/g", session=UUID, resume=UUID)
    assert "-s" in argv and "-r" in argv                              # both rendered: RED


# --- ACT 2c carry-overs from the 2b words (council 10:37Z-10:46Z 11-09) -------------------------------------------------

def test_a_shebang_wrapper_named_like_the_bin_is_not_the_harness_and_its_mutant(tree, tmp_path):
    """alive: a `#!/bin/sh` script named grok-bot reads comm grok-bot but
    argv[0] '/bin/sh'. comm is read only when argv is empty, so the wrapper
    never matches; the old argv-or-comm form commits the SHELL."""
    w = tmp_path / "bin" / "grok-bot"
    w.parent.mkdir()
    w.write_text("#!/bin/sh\nsleep 60\n")
    w.chmod(0o755)
    pane = tree(f"{w}; :")
    end = time.time() + 5
    while time.time() < end and not any(
            rotate._proc_argv(p)[1] == "grok-bot" for p in rotate._descendant_chain(pane)):
        time.sleep(0.05)
    wrapper = [p for p in rotate._descendant_chain(pane) if rotate._proc_argv(p)[1] == "grok-bot"]
    assert wrapper and Path(rotate._proc_argv(wrapper[0])[0][0]).name == "sh"
    assert rotate._pane_harness_pid(pane, "grok-bot")[0] is None
    m = _mutant(tmp_path, BIN / "rotate.py",
                "    if argv:\n        return Path(argv[0]).name == want\n",
                "    if argv and Path(argv[0]).name == want:\n        return True\n", "rot_mutC")
    assert m._pane_harness_pid(pane, "grok-bot")[0] == wrapper[0]     # the shell committed: RED


def test_comm_is_read_only_when_argv_is_empty(monkeypatch):
    long = "a-very-long-harness-bin"                                  # 23 chars; comm keeps 15
    monkeypatch.setattr(rotate, "_proc_argv", lambda pid: (["other-tool", "x"], long[:15]))
    assert not rotate._argv0_is(1, long)                              # another process's 15-char comm prefix
    monkeypatch.setattr(rotate, "_proc_argv", lambda pid: ([], long[:15]))
    assert rotate._argv0_is(1, long)                                  # argv unreadable: comm decides


@pytest.mark.parametrize("make", [
    lambda d: (d / "grok-bot.toml").write_text('id = "grok-bot"\n[session\n'),          # TOML parse error
    lambda d: (d / "grok-bot.toml").write_bytes(b'id = "\xff\xfe"\n'),                  # not UTF-8
    lambda d: (d / "grok-bot.toml").mkdir(),                                            # unreadable: OSError
])
def test_a_template_that_does_not_load_falls_back_to_the_registry_join(tmp_path, monkeypatch, make):
    """alive + aio: cmd_ack and run_after_join_for_seat render no template
    first, so a broken template must not kill their join."""
    d = tmp_path / "tpl"
    d.mkdir()
    make(d)
    monkeypatch.setattr(rotate.harness_template, "template_dir", lambda: d)   # rotate's own module object
    assert rotate._harness_session_registry("grok-bot") == "claude"
    assert rotate._harness_resume_proof("grok-bot") == "transcript"
    monkeypatch.setattr(rotate, "_find_seat", lambda root, s: {"harness": "grok-bot"})
    monkeypatch.setattr(rotate, "_join_by_pane", lambda **kw: pytest.fail("pane join on a broken template"))
    j = rotate._join_successor(root=tmp_path, seat="g1", window_id="@5",
                               registry_dir=str(tmp_path / "noreg"), poll_secs=0)
    assert j["found"] is False


def test_a_cyclic_parent_table_reads_EMPTY_and_its_mutant_spins(tmp_path, monkeypatch):
    """aio: `seen` is all that stops a cyclic table (10>11>12>10) from walking
    forever; the deadline in _join_by_pane is checked only between walks."""
    cyc = {11: 10, 12: 11, 10: 12}
    monkeypatch.setattr(rotate, "_argv0_is", lambda pid, want: False)
    assert rotate._pane_harness_pid(10, "x", parent_of=dict(cyc)) == (
        None, "no process launched as 'x' under pane pid 10")
    monkeypatch.setattr(rotate, "_argv0_is", lambda pid, want: pid == 12)
    assert rotate._pane_harness_pid(10, "x", parent_of=dict(cyc)) == (12, "depth 2")
    m = _mutant(tmp_path, BIN / "rotate.py",
                "                if c not in seen:\n                    seen.add(c)\n                    nxt.append(c)\n        level, depth = nxt, depth + 1\n",
                "                if True:\n                    seen.add(c)\n                    nxt.append(c)\n        level, depth = nxt, depth + 1\n",
                "rot_mutD")
    monkeypatch.setattr(m, "_argv0_is", lambda pid, want: False)

    def _alarm(*_a):
        raise TimeoutError
    old = signal.signal(signal.SIGALRM, _alarm)
    signal.alarm(1)
    try:
        with pytest.raises(TimeoutError):                             # never returns: RED
            m._pane_harness_pid(10, "x", parent_of=dict(cyc))
    finally:
        signal.alarm(0)
        signal.signal(signal.SIGALRM, old)


def test_resume_proof_is_template_declared_and_closed(tmp_path, monkeypatch):
    for hid in harness_template.available():
        want = "session_id" if hid == "grok-bot" else "transcript"
        assert harness_template.resume_proof(hid) == want, hid
    assert rotate._harness_resume_proof(None) == "transcript"
    (tmp_path / "x.toml").write_text('id = "x"\n[session]\nresume_proof = "maybe"\n')
    monkeypatch.setattr(harness_template, "template_dir", lambda: tmp_path)
    with pytest.raises(harness_template.HarnessTemplateError,
                       match="unknown session.resume_proof 'maybe'"):
        harness_template.load("x")
