"""alarm_spool.py (goal:g7.16.1.11.20.2): one spool per sending seat; the seat's own uid signs; exactly once."""
import json
import os
import subprocess
import sys
import threading
import types
from pathlib import Path

import pytest

sys.path.insert(0, str(Path(__file__).resolve().parents[1] / "bin"))
import alarm_spool as a  # noqa: E402

SRC = Path(a.__file__)

#: a stand-in `box send TO` with the real box's observable effect: ONE commit on refs/box/$AGI_POST/TO whose message is stdin
STUB_BOX = r"""#!/bin/sh
[ "$1" = send ] || exit 2
[ -z "$BOX_HOOK" ] || eval "$BOX_HOOK"
[ -z "$BOX_FAIL" ] || { echo "$BOX_FAIL" >&2; exit 1; }
msg=$(cat)
t=$(git hash-object -w -t tree /dev/null)
o=$(git rev-parse -q --verify refs/box/$AGI_POST/$2)
c=$(printf '%s\n' "$msg" | GIT_AUTHOR_NAME=x GIT_AUTHOR_EMAIL=$AGI_POST@agi GIT_COMMITTER_NAME=x GIT_COMMITTER_EMAIL=$AGI_POST@agi git commit-tree ${o:+-p $o} $t)
git update-ref refs/box/$AGI_POST/$2 $c
echo "$AGI_POST $2 $PWD" >> "$BOX_LOG"
"""
STUB_NOTICE = "#!/bin/sh\n[ \"$1\" = add ] || exit 2\nprintf '%s\\n' \"$2\" >> \"$NOTICE_OUT\"\n"


@pytest.fixture
def seat(tmp_path, monkeypatch):
    home = tmp_path / "home"
    (home / "t").mkdir(parents=True); (home / "bin").mkdir()
    subprocess.run(["git", "init", "-q", str(home / "t")], check=True)
    box = tmp_path / "box"; box.write_text(STUB_BOX); box.chmod(0o755)
    nb = home / "bin" / "agi-notice"; nb.write_text(STUB_NOTICE); nb.chmod(0o755)
    monkeypatch.setenv("HOME", str(home)); monkeypatch.setenv("BOX_LOG", str(tmp_path / "box.log"))
    monkeypatch.setenv("NOTICE_OUT", str(tmp_path / "notice.out"))
    for k in ("BOX_FAIL", "BOX_HOOK"):
        monkeypatch.delenv(k, raising=False)
    monkeypatch.setattr(a, "_uid_name", lambda: "agi-sanctuary-master")
    return types.SimpleNamespace(home=home, tree=home / "t", box=box, log=tmp_path / "box.log", notice=tmp_path / "notice.out",
                                 spool=home / "alarm.spool", tmp=tmp_path)


def _sent(s):
    return s.log.read_text().splitlines() if s.log.exists() else []


def _refmsgs(s):
    r = subprocess.run(["git", "-C", str(s.tree), "log", "refs/box/sanctuary-master/belam", "--format=%B%x00"], capture_output=True, text=True)
    return [m.strip() for m in r.stdout.split("\0") if m.strip()] if r.returncode == 0 else []


def _fresh(src):
    mod = types.ModuleType("alarm_spool_probe"); mod.__file__ = str(SRC)
    exec(compile(src, str(SRC), "exec"), mod.__dict__)
    mod._uid_name = lambda: "agi-sanctuary-master"
    return mod


# --- the SeatAction wiring (trunk red 06:3xZ 10-12: test_seat_alias_notice) must not break the INSTALLED single-file copy ---------------------

def test_the_single_file_copy_under_opt_agi_bin_still_appends_and_the_drain_takes_post_and_seat(tmp_path):
    """/opt/agi/bin/alarm_spool.py has no engine beside it, so `import geometry_config` falls back to a plain store: a root source's `append` still works there,
    and `drain` accepts --post (silent) and the literal --seat (the cron rows still say it) alike. MUTANT: a bare top-level import = the copy dies on import."""
    lone = tmp_path / "opt"; lone.mkdir(); (lone / "alarm_spool.py").write_text(SRC.read_text())
    home = tmp_path / "h"; home.mkdir()
    env = {"PATH": os.environ["PATH"], "HOME": str(home)}
    r = subprocess.run([sys.executable, "-I", str(lone / "alarm_spool.py"), "append", "--job", "j", "--to", "belam", "--text", "t", "--max-lines", "5", "--spool", str(home / "s")],
                       capture_output=True, text=True, env=env, cwd=lone)
    assert r.returncode == 0 and len((home / "s").read_text().splitlines()) == 1, (r.stdout, r.stderr)
    for flag in ("--post", "--seat"):
        r = subprocess.run([sys.executable, "-I", str(lone / "alarm_spool.py"), "drain", flag, "nobody", "--max-tries", "1", "--spool", str(home / "none")],
                           capture_output=True, text=True, env=env, cwd=lone)
        assert "unrecognized arguments" not in r.stderr and "required" not in r.stderr and "Traceback" not in r.stderr, (flag, r.stderr)     # parsed; it then refuses a uid that is not the seat's
    bare = (lone / "alarm_spool.py")
    src = SRC.read_text(); i = src.index("try:\n    import geometry_config"); j = src.index("class SeatAction")
    bare.write_text(src[:i] + "import geometry_config\n" + src[src.index("\n", src.index("setattr(namespace, self.dest, values)")) + 1:])
    r = subprocess.run([sys.executable, "-I", str(bare), "append", "--job", "j", "--to", "belam", "--text", "t", "--max-lines", "5", "--spool", str(home / "s2")],
                       capture_output=True, text=True, env=env, cwd=lone)
    assert r.returncode != 0 and "geometry_config" in r.stderr, (r.returncode, r.stderr)           # the mutant: a bare import kills the installed copy


# --- append: a plain line, bounded, atomic ------------------------------------------------------------------

def test_append_writes_one_plain_json_line_without_a_key_or_a_box(seat):
    assert a.append("memory_alarm_posts", "belam", "WARN memory warn: x\nsecond line", max_lines=10) is None
    (line,) = seat.spool.read_text().splitlines()
    rec = json.loads(line)
    assert rec["job"] == "memory_alarm_posts" and rec["to"] == "belam" and rec["text"] == "WARN memory warn: x second line", rec
    assert rec["id"] and rec["ts"].endswith("Z") and not seat.log.exists()           # nothing was sent: append has no box in it
    assert (seat.spool.stat().st_mode & 0o777) == 0o600


def test_append_refuses_beyond_the_cap_and_says_why(seat):
    for _ in range(3):
        assert a.append("j", "belam", "t", max_lines=3) is None
    why = a.append("j", "belam", "t", max_lines=3)
    assert why and "max-lines 3" in why and len(seat.spool.read_text().splitlines()) == 3


def test_concurrent_appenders_never_interleave_a_line(seat):
    ts = [threading.Thread(target=lambda i=i: a.append("j", "belam", f"alarm {i} " + "x" * 3000, max_lines=1000)) for i in range(40)]
    [t.start() for t in ts]; [t.join() for t in ts]
    recs = [json.loads(l) for l in seat.spool.read_text().splitlines()]                # every line parses = none torn
    assert len(recs) == 40 and len({r["id"] for r in recs}) == 40


def test_an_over_long_text_is_cut_to_one_atomic_write(seat):
    assert a.append("j", "belam", "y" * 9000, max_lines=5) is None
    assert len(seat.spool.read_bytes()) <= a.LINE_MAX + 1


# --- drain: the SENDING seat's own uid signs ----------------------------------------------------------------

def test_the_drain_sends_as_the_seat_from_its_own_tree_with_subject_and_trailers(seat):
    a.append("memory_alarm_posts", "belam", "[memory-alarm-warn] WARN memory warn: x", max_lines=10)
    assert a.drain("sanctuary-master", box_bin=seat.box, max_tries=60) == 0
    assert _sent(seat) == [f"sanctuary-master belam {seat.tree}"]                      # AS the seat, from ITS ~/t, to the reader
    (msg,) = _refmsgs(seat)
    first, *rest = msg.splitlines()
    assert first.startswith("[alarm memory_alarm_posts] [memory-alarm-warn] WARN"), first
    assert "Alarm-job: memory_alarm_posts" in rest and any(l.startswith("Alarm-id: ") for l in rest), rest
    assert not seat.spool.exists() and not (seat.home / "alarm.spool.draining").exists()


def test_r2_a_drain_in_any_other_uid_signs_and_sends_nothing(seat, monkeypatch, capsys):
    a.append("j", "belam", "t", max_lines=5)
    for uid in ("root", "agi-belam", "agi-director-general-1"):
        monkeypatch.setattr(a, "_uid_name", lambda uid=uid: uid)
        assert a.drain("sanctuary-master", box_bin=seat.box, max_tries=60) == 2
        assert f"uid {uid} cannot drain sanctuary-master's spool" in capsys.readouterr().err
    assert _sent(seat) == [] and len(seat.spool.read_text().splitlines()) == 1         # untouched, still spooled


def test_r3_a_spooled_line_is_sent_exactly_once(seat):
    a.append("j", "belam", "one", max_lines=5)
    assert a.drain("sanctuary-master", box_bin=seat.box, max_tries=60) == 0
    assert a.drain("sanctuary-master", box_bin=seat.box, max_tries=60) == 0                          # nothing left: nothing sent
    assert len(_sent(seat)) == 1 and len(_refmsgs(seat)) == 1


def test_r3_a_crash_between_the_send_and_the_unlink_never_sends_it_twice(seat, monkeypatch):
    a.append("j", "belam", "one", max_lines=5)
    real = Path.unlink
    def boom(self, *x, **k):
        if self.name == a.DRAINING:
            raise OSError("killed before the unlink")
        return real(self, *x, **k)
    monkeypatch.setattr(Path, "unlink", boom)
    with pytest.raises(OSError):
        a.drain("sanctuary-master", box_bin=seat.box, max_tries=60)
    monkeypatch.setattr(Path, "unlink", real)
    assert len(_sent(seat)) == 1 and (seat.home / a.DRAINING).exists()                 # sent, but the line is still there
    assert a.drain("sanctuary-master", box_bin=seat.box, max_tries=60) == 0                          # the next run finds its Alarm-id on the seat's ref
    assert len(_sent(seat)) == 1 and len(_refmsgs(seat)) == 1 and not (seat.home / a.DRAINING).exists()


def test_a_failed_send_stays_spooled_notices_once_and_is_retried_then_sent_once(seat, monkeypatch, capsys):
    a.append("j", "belam", "one", max_lines=5)
    monkeypatch.setenv("BOX_FAIL", "[off-matrix] sanctuary-master -> belam: not adjacent, nothing sent")
    assert a.drain("sanctuary-master", box_bin=seat.box, max_tries=60) == 0
    assert "NOT sent, kept" in capsys.readouterr().err and _sent(seat) == []
    assert len(seat.spool.read_text().splitlines()) == 1                               # kept, with its try counted
    note = seat.notice.read_text()
    assert note.startswith("[alarm-unsent] ") and "[off-matrix]" in note              # a ~/.notice line: never silent
    monkeypatch.delenv("BOX_FAIL")
    assert a.drain("sanctuary-master", box_bin=seat.box, max_tries=60) == 0                          # retried next run
    assert len(_sent(seat)) == 1 and not seat.spool.exists()
    assert a.drain("sanctuary-master", box_bin=seat.box, max_tries=60) == 0 and len(_sent(seat)) == 1


def test_a_line_that_fails_max_tries_times_is_dead_lettered_with_one_notice_and_never_retried(seat, monkeypatch, capsys):
    a.append("j", "belam", "one", max_lines=5)
    monkeypatch.setenv("BOX_FAIL", "[squatted] refs/box/sanctuary-master/belam x: not mine, nothing sent")
    for n in (1, 2):
        assert a.drain("sanctuary-master", box_bin=seat.box, max_tries=3) == 0
        assert json.loads(seat.spool.read_text().splitlines()[0])["tries"] == n          # counted on the line, still spooled
    assert "[alarm-dead]" not in (seat.notice.read_text() if seat.notice.exists() else "")
    assert a.drain("sanctuary-master", box_bin=seat.box, max_tries=3) == 0
    assert not seat.spool.exists()
    (dead,) = (seat.home / "alarm.spool.dead").read_text().splitlines()
    assert json.loads(dead)["tries"] == 3 and "DEAD after 3 tries" in capsys.readouterr().err
    assert seat.notice.read_text().count("[alarm-dead] ") == 1                           # ONE line, not one per pass
    monkeypatch.delenv("BOX_FAIL")
    assert a.drain("sanctuary-master", box_bin=seat.box, max_tries=3) == 0 and _sent(seat) == []


def test_a_line_appended_while_the_drain_sends_is_kept_for_the_next_run(seat, monkeypatch):
    a.append("j", "belam", "first", max_lines=5)
    monkeypatch.setenv("BOX_HOOK", f"""printf '%s\\n' '{json.dumps({"id": "ffffffff-0001", "job": "j", "to": "belam", "text": "late", "ts": "t"})}' >> {seat.spool}""")
    assert a.drain("sanctuary-master", box_bin=seat.box, max_tries=60) == 0
    assert [json.loads(l)["text"] for l in seat.spool.read_text().splitlines()] == ["late"]   # not lost to a rewrite
    monkeypatch.delenv("BOX_HOOK")
    assert a.drain("sanctuary-master", box_bin=seat.box, max_tries=60) == 0 and len(_sent(seat)) == 2 and not seat.spool.exists()


def test_a_held_lock_is_busy_and_does_nothing(seat, capsys):
    import fcntl, os
    a.append("j", "belam", "one", max_lines=5)
    fd = os.open(seat.home / "alarm.spool.lock", os.O_WRONLY | os.O_CREAT); fcntl.flock(fd, fcntl.LOCK_EX)
    try:
        assert a.drain("sanctuary-master", box_bin=seat.box, max_tries=60) == 0
    finally:
        os.close(fd)
    assert "[busy]" in capsys.readouterr().out and _sent(seat) == []


def test_an_unreadable_line_is_dropped_loudly_and_the_rest_is_sent(seat, capsys):
    seat.spool.write_text("this is not json\n")
    a.append("j", "belam", "good", max_lines=5)
    assert a.drain("sanctuary-master", box_bin=seat.box, max_tries=60) == 0
    assert "unreadable spool line dropped" in capsys.readouterr().err and len(_sent(seat)) == 1
    assert "[alarm-spool-bad]" in seat.notice.read_text()


# --- mutants: each is RED on the row meant for it -----------------------------------------------------------

def _crash_then_rerun(s, mod, monkeypatch):
    a.append("j", "belam", "one", max_lines=5)
    real = Path.unlink
    def boom(self, *x, **k):
        if self.name == a.DRAINING:
            raise OSError("killed")
        return real(self, *x, **k)
    monkeypatch.setattr(Path, "unlink", boom)
    with pytest.raises(OSError):
        mod.drain("sanctuary-master", box_bin=s.box, max_tries=60)
    monkeypatch.setattr(Path, "unlink", real)
    mod.drain("sanctuary-master", box_bin=s.box, max_tries=60)
    return len(_sent(s))


def _failed_then_fixed(s, mod, monkeypatch):
    a.append("j", "belam", "one", max_lines=5)
    monkeypatch.setenv("BOX_FAIL", "[unsent] x")
    mod.drain("sanctuary-master", box_bin=s.box, max_tries=60)
    monkeypatch.delenv("BOX_FAIL")
    mod.drain("sanctuary-master", box_bin=s.box, max_tries=60)
    return len(_sent(s))


def _dead_after_three(s, mod, monkeypatch):
    a.append("j", "belam", "one", max_lines=5)
    monkeypatch.setenv("BOX_FAIL", "[off-matrix] x")
    for _ in range(3):
        mod.drain("sanctuary-master", box_bin=s.box, max_tries=3)
    monkeypatch.delenv("BOX_FAIL")
    mod.drain("sanctuary-master", box_bin=s.box, max_tries=3)                           # the reader became reachable: a dead line is not retried
    return len(_sent(s))


def _other_uid(s, mod, monkeypatch):
    a.append("j", "belam", "one", max_lines=5)
    mod._uid_name = lambda: "root"
    mod.drain("sanctuary-master", box_bin=s.box, max_tries=60)
    return len(_sent(s))


def _race(s, mod, monkeypatch, when):
    """The lost-line interleaving (alive 22:5xZ): an appender opened alarm.spool BEFORE the drain's rename and writes AFTER it.
    `when` = 'open': the whole drain runs between the appender's open and its write; 'write': between its write and its check.
    Returns how many times the line SECOND reached the reader after the dust settled."""
    mod.append("j", "belam", "first", max_lines=50)
    real_open, real_write, state = os.open, os.write, {"fired": False}
    def drain():
        state["fired"] = True
        assert mod.drain("sanctuary-master", box_bin=s.box, max_tries=60) == 0
    def op(path, flags, *x, **k):
        fd = real_open(path, flags, *x, **k)
        if when == "open" and not state["fired"] and flags & os.O_APPEND and str(path).endswith("alarm.spool"):
            drain()
        return fd
    def wr(fd, data):
        n = real_write(fd, data)
        if when == "write" and not state["fired"] and data.startswith(b'{"id"') and b"SECOND" in data:
            drain()
        return n
    monkeypatch.setattr(os, "open", op); monkeypatch.setattr(os, "write", wr)
    assert mod.append("j", "belam", "SECOND", max_lines=50) is None
    monkeypatch.setattr(os, "open", real_open); monkeypatch.setattr(os, "write", real_write)
    assert state["fired"]
    for _ in range(2):                                                                   # the drain cron's next minutes
        mod.drain("sanctuary-master", box_bin=s.box, max_tries=60)
    return sum("SECOND" in m for m in _refmsgs(s))


@pytest.mark.parametrize("when", ["open", "write"])
def test_a_line_written_through_an_fd_opened_before_the_drains_rename_is_sent_exactly_once(seat, monkeypatch, when):
    assert _race(seat, a, monkeypatch, when) == 1
    assert len(_refmsgs(seat)) == 2 and not seat.spool.exists()                           # first + SECOND, nothing left, nothing doubled


def test_a_failed_line_notices_once_per_episode_not_every_failed_minute(seat, monkeypatch):
    a.append("j", "belam", "one", max_lines=5)
    monkeypatch.setenv("BOX_FAIL", "[unsent] x")
    for _ in range(4):
        assert a.drain("sanctuary-master", box_bin=seat.box, max_tries=60) == 0
    assert seat.notice.read_text().count("[alarm-unsent] ") == 1                          # the first failure only
    assert json.loads(seat.spool.read_text().splitlines()[0])["tries"] == 4                # and it is still retried


def _race_open(s, mod, monkeypatch):
    return _race(s, mod, monkeypatch, "open")


@pytest.mark.parametrize("old,new,scenario,real", [
    ('if already_sent(tree, seat, rec["to"], rec["id"]):', "if False:", _crash_then_rerun, 1),   # M1: a drain that re-sends a sent line
    ('            kept.append(json.dumps(rec, separators=(",", ":")))\n', "            pass\n", _failed_then_fixed, 1),              # M2: a failed line is dropped, never retried
    ('if rec["tries"] >= max_tries:', "if False:", _dead_after_three, 0),                # M4: retries for ever
    ("            if same:\n                return None\n", "            return None\n", _race_open, 1),   # M5: today's append, no check after the write = the line is lost
    ("    if me != f\"agi-{seat}\":", "    if False:", _other_uid, 0),                          # M3: any uid may drain (root signing as a seat)
])
def test_each_mutant_goes_red_on_the_row_meant_for_it(seat, monkeypatch, old, new, scenario, real):
    src = SRC.read_text()
    assert src.count(old) == 1, old                                                      # anchor: 0 or 2 matches prove nothing
    mut = _fresh(src.replace(old, new))
    seat.log.unlink(missing_ok=True)
    got = scenario(seat, mut, monkeypatch)
    assert got != real, f"mutant {old!r} survived: {got} sends"
