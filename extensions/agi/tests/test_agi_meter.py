"""G10: agi-meter reads the newest transcript line WITH .message.usage, not the last line."""
import json, os, re, subprocess
import pytest
from pathlib import Path

GEO = Path(__file__).resolve().parents[3] / ".agi/nodes/.geometry"
U = lambda n: {"type": "assistant", "message": {"usage": {"input_tokens": n, "cache_read_input_tokens": 0, "cache_creation_input_tokens": 0}}}
SYS = {"type": "system", "subtype": "bridge"}

def piece(name):
    return re.search(rf"^### {name} .*?\n~~~\w*\n(.*?)^~~~", (GEO / "engine-post.md").read_text(), re.S | re.M)[1]


def run(tmp_path, lines, hook=None, window=1000, trunk="HEAD", atomize=None, notice=None, sh_text=None, timeout=None, mem=None,
        atomize_live="true"):
    sh = tmp_path / "m.sh"
    sh.write_text(piece("agi-meter") if sh_text is None else sh_text)
    tr = tmp_path / "t.jsonl"
    tr.write_text("".join((l if isinstance(l, str) else json.dumps(l)) + "\n" for l in lines))
    j = json.dumps(dict(transcript_path=str(tr), **(hook or {})))
    # hermetic to what is INSTALLED (SM's finding 22:5xZ 10-25, alive's lens 22:48Z): the meter runs agi-mem / agi-atomize / agi-notice from
    # PATH, and the conftest strips every AGI_* var. agi-mem is the TREE UNDER TEST's piece (a stub that prints nothing would pass the
    # meter's silent rows whatever the real one prints) run against a scratch engine repo whose posts.md it can read, AGI_TRUNK naming a ref
    # that repo has; atomize / notice are stubs (they are not under test here).
    stubs = tmp_path / "stubs"
    stubs.mkdir(exist_ok=True)
    (stubs / "agi-mem").write_text(piece("agi-mem") if mem is None else "#!/bin/sh\n" + mem)
    for name, body in (("agi-atomize", atomize), ("agi-notice", notice)):
        (stubs / name).write_text("#!/bin/sh\ncat >/dev/null 2>&1\nexit 0\n" if body is None else "#!/bin/sh\n" + body)
    for f in stubs.iterdir():
        f.chmod(0o755)
    eng = tmp_path / "eng"
    if not eng.exists():
        g = eng / ".agi" / "nodes" / ".geometry"
        g.mkdir(parents=True)
        (g / "posts.md").write_text('---\nid: config:posts\nposts:\n  - {"name": "p", "mem": "none"}\n---\n')
        # the atomize GATE CELL (alive [decision] 14:17:17Z 10-31, D1): the meter forks the wake only on atomize_live: true, read
        # from AGI_T's trunk secrets.md; the wake rows open it, None writes no line (the gate reads 'unreadable')
        if atomize_live is not None:
            (g / "secrets.md").write_text(f"---\nid: config:secrets\natomize_live: {atomize_live}\n---\n")
        for c in (["init", "-q", "."], ["config", "core.hooksPath", "/dev/null"], ["add", "-A", ".agi"],
                  ["-c", "user.name=t", "-c", "user.email=t@t", "-c", "commit.gpgsign=false", "commit", "-qm", "x"]):
            subprocess.run(["git", "-C", str(eng)] + c, check=True, capture_output=True)
    env = dict(os.environ, AGI_WINDOW=str(window), AGI_ROTATE_PCT="50", AGI_ENGINE=str(eng), AGI_TRUNK=trunk, AGI_T=str(eng),
               AGI_POST="p", HOME=str(tmp_path), PATH=f"{stubs}:{os.environ.get('PATH', '')}")
    return subprocess.run(["sh", str(sh)], input=j, env=env, capture_output=True, text=True, timeout=timeout)


def test_a_last_line_no_usage_earlier_over_the_line(tmp_path):
    r = run(tmp_path, [U(900), SYS])
    assert r.returncode == 0 and "At the line (900/1000)" in r.stdout


def test_b_under_the_line_is_silent(tmp_path):
    r = run(tmp_path, [U(100), SYS])
    assert r.returncode == 0 and r.stdout == ""


def test_c_tokens_in_hook_wins(tmp_path):
    assert "(900/1000)" in run(tmp_path, [U(100), SYS], {"tokens": 900}).stdout
    assert run(tmp_path, [U(900), SYS], {"tokens": 100}).stdout == ""


def test_d_no_usage_line_is_silent_exit_0(tmp_path):
    r = run(tmp_path, [SYS, {"type": "user"}, "not json"])
    assert r.returncode == 0 and r.stdout == ""


def test_e_text_mentioning_usage_is_skipped(tmp_path):
    txt = {"type": "assistant", "message": {"content": [{"type": "text", "text": 'the "usage" word'}]}}
    assert "(900/1000)" in run(tmp_path, [U(900), txt, SYS]).stdout


def test_null_field_counts_as_zero(tmp_path):
    assert "(900/1000)" in run(tmp_path, [{"message": {"usage": {"input_tokens": 900, "cache_read_input_tokens": None}}}]).stdout


def test_non_object_usage_is_skipped(tmp_path):
    bad = [{"message": {"usage": v}} for v in ("x", [1], 7)] + [{"message": "s"}, 5]
    assert "(900/1000)" in run(tmp_path, [U(900)] + bad + [SYS]).stdout


def test_scan_stops_at_first_valid_usage_line(tmp_path):  # the scan stops at the newest VALID usage line from the end
    poison = {"message": {"usage": {"input_tokens": "a", "cache_read_input_tokens": "b"}}}
    r = run(tmp_path, [poison] * 3 + [SYS, U(900)])
    assert r.returncode == 0 and "(900/1000)" in r.stdout


def test_poison_reached_first_is_skipped_not_fatal(tmp_path):
    poison = {"message": {"usage": {"input_tokens": "a", "cache_read_input_tokens": "b"}}}
    r = run(tmp_path, [U(900), poison, SYS])
    assert r.returncode == 0 and "(900/1000)" in r.stdout and r.stderr == ""


def test_string_cache_field_counts_zero(tmp_path):
    r = run(tmp_path, [U(100), {"message": {"usage": {"input_tokens": 900, "cache_read_input_tokens": "b", "cache_creation_input_tokens": 5}}}], window=1800)
    assert "(905/1800)" in r.stdout and r.stderr == ""


def test_f_the_trees_agi_mem_on_an_unreadable_trunk_warns_once_and_the_meter_goes_on(tmp_path):
    """alive 22:48Z: the interaction that broke is asserted, not hidden. With AGI_TRUNK naming no ref, the tree's agi-mem prints its ONE
    `[mem] warn` line on the meter's stdout (rc 0 by agi-mem's design) and the meter still speaks; with a readable trunk it is silent."""
    r = run(tmp_path, [U(100), SYS], trunk="nosuchref")
    assert r.returncode == 0
    assert r.stdout == "[mem] warn: posts.md unreadable at nosuchref (the turn goes on)\n"
    r = run(tmp_path, [U(900), SYS], trunk="nosuchref")
    assert r.returncode == 0 and "At the line (900/1000)" in r.stdout and r.stdout.count("[mem] warn") == 1


# ---- belam [red] 14:2xZ 10-26: the hook is killed at Claude Code's 30 s limit BEFORE its last line (`At the line`) because `agi-atomize wake` (26 s) ran first ----
import time

SLOW = "echo $$ >$HOME/atomize.pid\nexec sleep 40\n"         # a wake that takes longer than the hook's 30 s


def _reap(tmp_path):
    f = tmp_path / "atomize.pid"
    if f.exists():
        subprocess.run(["kill", f.read_text().strip()], capture_output=True)      # the stub exec'd `sleep 40`: its pid is the sleep's


def test_f_the_line_prints_first_and_the_hook_returns_in_seconds_though_the_wake_sleeps_40s(tmp_path):
    t0 = time.time()
    try:
        r = run(tmp_path, [U(900), SYS], {"prompt": "mail: box read"}, atomize=SLOW, timeout=15)   # a held stdout pipe would block until the 40 s sleep ends -> TimeoutExpired
    finally:
        _reap(tmp_path)
    assert r.returncode == 0 and "At the line (900/1000)" in r.stdout, r.stdout
    assert time.time() - t0 < 5, "the hook must return in seconds, the wake belongs to the background"


def test_g_the_line_comes_BEFORE_the_notice(tmp_path):
    (tmp_path / ".notice.a").write_text("x")             # `ls ~/.notice*` finds it -> the meter runs agi-notice
    r = run(tmp_path, [U(900), SYS], notice="echo NOTICE-TEXT\n")
    assert r.stdout.index("At the line") < r.stdout.index("NOTICE-TEXT"), r.stdout


def test_h_a_failing_wake_is_named_in_the_log_and_never_on_stdout(tmp_path):
    r = run(tmp_path, [U(100), SYS], {"prompt": "mail: box read"}, atomize="exit 3\n")
    subprocess.run(["flock", "-w", "10", str(tmp_path / ".atomize.lock"), "true"], check=True)      # the child holds the lock until it ends
    log = (tmp_path / ".atomize.log").read_text()
    assert r.stdout == "" and "[atomize] wake rc=3: no atoms this read; the next read retries" in log, (r.stdout, log)


def test_i_a_second_wake_while_the_first_runs_is_skipped_and_named(tmp_path):
    try:
        run(tmp_path, [U(100), SYS], {"prompt": "mail: box read"}, atomize=SLOW, timeout=15)
        r = run(tmp_path, [U(100), SYS], {"prompt": "mail: box read"}, atomize=SLOW, timeout=15)
    finally:
        _reap(tmp_path)
    assert r.returncode == 0 and "[atomize] wake skipped: the previous wake still runs" in (tmp_path / ".atomize.log").read_text()


def test_j_only_the_box_read_prompt_wakes(tmp_path):
    run(tmp_path, [U(100), SYS], {"prompt": "hello"}, atomize="echo woke >$HOME/woke\n")
    time.sleep(0.5)
    assert not (tmp_path / "woke").exists()


# MUTANTS (each must turn a row above RED; run on the piece text, not by hand)
def _mutant(tmp_path, old, new, **kw):
    text = piece("agi-meter")
    assert old in text, old
    return run(tmp_path, [U(900), SYS], {"prompt": "mail: box read"}, sh_text=text.replace(old, new), **kw)


def test_m_foreground_wake_holds_the_hook_RED(tmp_path):
    # the old shape: the wake in the foreground. With a slow wake the hook does NOT return in seconds.
    with pytest.raises(subprocess.TimeoutExpired):
        try:
            _mutant(tmp_path, ")>>~/.atomize.log 2>&1 </dev/null &", ");", atomize="sleep 8\n", timeout=4)
        finally:
            _reap(tmp_path)


def test_m_the_line_after_the_wake_is_RED(tmp_path):
    # the old ORDER: tap + wake before the check. Moving the check to the end of the piece puts it behind a slow foreground wake.
    text = piece("agi-meter")
    lines = text.rstrip("\n").split("\n")
    chk = next(i for i, l in enumerate(lines) if l.startswith('[ "${t:-0}" -gt'))
    moved = lines[:chk] + lines[chk + 1:] + [lines[chk]]
    moved = "\n".join(moved).replace(")>>~/.atomize.log 2>&1 </dev/null &", ");") + "\n"
    with pytest.raises(subprocess.TimeoutExpired):
        run(tmp_path, [U(900), SYS], {"prompt": "mail: box read"}, sh_text=moved, atomize="sleep 8\n", timeout=4)


# ---- alive 14:31:50Z 10-26 (3)(4): the tap is bounded too, so the hook's TOTAL wall time is bounded by construction; a killed tap is NAMED ----
SLOW_TAP = "cat >/dev/null 2>&1\nexec sleep 40\n"
START_3S = "echo start >>$HOME/starts\nexec sleep 3\n"


def test_k_r3_a_40s_tap_and_a_40s_wake_still_print_the_line_and_name_the_unread_tap_within_20s(tmp_path):
    t0 = time.time()
    try:
        r = run(tmp_path, [U(900), SYS], {"prompt": "mail: box read"}, atomize=SLOW, mem=SLOW_TAP, timeout=25)
    finally:
        _reap(tmp_path)
    assert r.returncode == 0 and "At the line (900/1000)" in r.stdout and "[mem] tap unread (killed at 15 s)" in r.stdout, r.stdout
    assert time.time() - t0 < 20, "EOF on the hook's stdout must come within 20 s: the tap is bounded at 15 s"


def test_l_r2_two_box_read_prompts_one_second_apart_make_ONE_wake_process(tmp_path):
    for _ in range(2):
        run(tmp_path, [U(100), SYS], {"prompt": "mail: box read"}, atomize=START_3S, timeout=15)
        time.sleep(1)
    subprocess.run(["flock", "-w", "10", str(tmp_path / ".atomize.lock"), "true"], check=True)
    assert (tmp_path / "starts").read_text().split() == ["start"], (tmp_path / "starts").read_text()


def test_m_a_tap_that_ends_on_its_own_prints_no_unread_line(tmp_path):
    r = run(tmp_path, [U(900), SYS], {"prompt": "hello"}, mem="cat >/dev/null\nexit 0\n")
    assert "[mem] tap unread" not in r.stdout


def test_n_mutant_the_log_redirect_dropped_the_child_holds_the_hooks_stdout_RED(tmp_path):
    with pytest.raises(subprocess.TimeoutExpired):                       # EOF only after the 40 s sleep
        try:
            _mutant(tmp_path, ")>>~/.atomize.log 2>&1 </dev/null &", ") &", atomize=SLOW, timeout=12)
        finally:
            _reap(tmp_path)


def test_o_mutant_no_flock_two_wakes_RED(tmp_path):
    text = piece("agi-meter").replace("elif flock -n 9;then", "elif true;then")
    assert text != piece("agi-meter")
    for _ in range(2):
        run(tmp_path, [U(100), SYS], {"prompt": "mail: box read"}, sh_text=text, atomize=START_3S, timeout=15)
        time.sleep(1)
    time.sleep(4)
    assert (tmp_path / "starts").read_text().split() == ["start", "start"], "the mutant must start TWO wakes (the single-flight row catches it)"


def test_p_mutant_the_tap_timeout_dropped_the_hook_runs_past_20s_RED(tmp_path):
    with pytest.raises(subprocess.TimeoutExpired):
        _mutant(tmp_path, "timeout -k 2 15 ", "", mem=SLOW_TAP, atomize="exit 0\n", timeout=22)


def test_q_mutant_the_unread_line_dropped_RED(tmp_path):
    try:
        r = _mutant(tmp_path, 'echo "[mem] tap unread (killed at 15 s)"', ":", mem=SLOW_TAP, atomize="exit 0\n", timeout=25)
    finally:
        _reap(tmp_path)
    assert "At the line" in r.stdout and "[mem] tap unread" not in r.stdout, "the mutant is silent about the killed tap (row k catches it)"


# ---- alive 14:45:31Z 10-26 CONDITION 1 (a false line is RED) + self-perpetuating's two later rows ----
def _home_lock_dir(tmp_path):
    (tmp_path / ".atomize.lock").mkdir()           # the lock path unopenable: a DIRECTORY


def test_r_an_unopenable_lock_is_named_truly_not_as_a_running_wake(tmp_path):
    _home_lock_dir(tmp_path)
    for _ in range(2):
        r = run(tmp_path, [U(100), SYS], {"prompt": "mail: box read"}, atomize="echo start >>$HOME/starts\n", notice="echo \"$*\" >>$HOME/notices.log\n", timeout=15)
        assert r.returncode == 0 and r.stdout == "", r.stdout
    log = (tmp_path / ".atomize.log").read_text()
    assert "[atomize] wake not run: ~/.atomize.lock unopenable" in log and "still runs" not in log, log
    assert not (tmp_path / "starts").exists()
    n = (tmp_path / "notices.log").read_text()
    assert "[atomize] wake not run: ~/.atomize.lock unopenable" in n, n      # the post SEES it (agi-notice dedups by key; the print consumes the file, so it shows on each read while it lasts)


def test_s_mutant_the_open_check_dropped_says_still_runs_which_is_FALSE_RED(tmp_path):
    _home_lock_dir(tmp_path)
    text = piece("agi-meter").replace('if [ -z "$o" ];then', 'if false;then')
    assert text != piece("agi-meter")
    run(tmp_path, [U(100), SYS], {"prompt": "mail: box read"}, sh_text=text, timeout=15)
    log = (tmp_path / ".atomize.log").read_text()
    assert "still runs" in log and "unopenable" not in log, "the mutant tells the false story (the row above catches it)"


def test_u_no_flock_binary_is_named_in_the_log_and_the_wake_still_runs(tmp_path):
    text = piece("agi-meter").replace("command -v flock", "command -v flock-none")
    run(tmp_path, [U(100), SYS], {"prompt": "mail: box read"}, sh_text=text, atomize="echo start >>$HOME/starts\n", timeout=15)
    time.sleep(1)
    assert "[atomize] wake unguarded: no flock" in (tmp_path / ".atomize.log").read_text()
    assert (tmp_path / "starts").read_text().split() == ["start"]


def test_v_the_two_doc_lines_no_longer_say_agi_meter_calls_the_notice_first():
    t = (GEO / "engine-post.md").read_text()
    assert "called first by agi-brief and agi-meter" not in t and "agi-meter's prompt hook call it first" not in t


# ---- self-perpetuating's later row (alive 14:49:35Z C, FOLDABLE): a tap that cannot run (timeout rc 125/126/127) is NAMED with its rc ----
def test_w_a_tap_that_cannot_run_is_named_with_its_rc(tmp_path):
    r = run(tmp_path, [U(100), SYS], {"prompt": "hello"}, sh_text=piece("agi-meter").replace("agi-mem tap", "agi-mem-none tap"))
    assert "[mem] tap not run (rc 127)" in r.stdout, r.stdout


def test_x_a_tap_that_runs_clean_prints_neither_tap_line(tmp_path):
    r = run(tmp_path, [U(100), SYS], {"prompt": "hello"}, mem="cat >/dev/null\nexit 0\n")
    assert "[mem] tap" not in r.stdout, r.stdout


def test_y_mutant_the_125_126_127_branch_dropped_is_silent_RED(tmp_path):
    text = piece("agi-meter")
    old = '125|126|127)echo "[mem] tap not run (rc $r)";;'
    assert old in text
    r = run(tmp_path, [U(100), SYS], {"prompt": "hello"}, sh_text=text.replace(old, "").replace("agi-mem tap", "agi-mem-none tap"))
    assert "[mem] tap not run" not in r.stdout, "the mutant is silent about a tap that cannot run (row w catches it)"


# ---- the atomize GATE CELL (alive [decision] 14:17:17Z 10-31, D1): closed -> no fork, ONE named line, stdout empty ----
@pytest.mark.parametrize("cell,shown", [("false", "false"), (None, "unreadable")])
def test_z_a_closed_gate_cell_forks_no_wake_and_names_it(tmp_path, cell, shown):
    r = run(tmp_path, [U(100), SYS], {"prompt": "mail: box read"}, atomize="echo woke >$HOME/woke\n", atomize_live=cell)
    time.sleep(0.5)
    log = (tmp_path / ".atomize.log").read_text()
    assert r.stdout == "" and not (tmp_path / "woke").exists(), r.stdout
    assert f"[atomize] wake not run: atomize_live is {shown}, no request" in log, log


def test_z_mutant_the_gate_read_dropped_forks_the_wake_RED(tmp_path):
    text = piece("agi-meter")
    old = 'if [ "$al" != true ];then'
    assert old in text
    run(tmp_path, [U(100), SYS], {"prompt": "mail: box read"}, atomize="echo woke >$HOME/woke\n", atomize_live="false",
        sh_text=text.replace(old, "if false;then"))
    subprocess.run(["flock", "-w", "10", str(tmp_path / ".atomize.lock"), "true"], check=True)
    assert (tmp_path / "woke").exists(), "the mutant forks the wake with the cell false (test_z_a_closed_gate catches it)"
