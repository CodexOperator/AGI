"""alarm-first-start.sh (goal:g7.16.1.11.20.2 item 5): belam's one host act proves the path before the first real alarm."""
import os
import stat
import subprocess
import sys
from pathlib import Path

import pytest

REPO = Path(__file__).resolve().parents[3]
SCRIPT = REPO / "extensions" / "agi" / "guard" / "alarm-first-start.sh"
BIN = REPO / "extensions" / "agi" / "bin"

STUB_BOX = r"""#!/bin/sh
[ "$1" = send ] || exit 2
[ -z "$BOX_FAIL" ] || { echo "$BOX_FAIL" >&2; exit 1; }
msg=$(cat)
t=$(git hash-object -w -t tree /dev/null)
o=$(git rev-parse -q --verify refs/box/$AGI_POST/$2)
c=$(printf '%s\n' "$msg" | GIT_AUTHOR_NAME=x GIT_AUTHOR_EMAIL=$AGI_POST@agi GIT_COMMITTER_NAME=x GIT_COMMITTER_EMAIL=$AGI_POST@agi git commit-tree ${o:+-p $o} $t)
git update-ref refs/box/$AGI_POST/$2 $c
"""
WRAP = f"""import os, sys
sys.path.insert(0, {str(BIN)!r})
import alarm_spool as a
a._uid_name = lambda: os.environ["RUNUSER_AS"]            # what runuser -u agi-<seat> makes the process
sys.exit(a.main(sys.argv[1:]))
"""


def _exe(path, text):
    path.write_text(text); path.chmod(path.stat().st_mode | stat.S_IXUSR)
    return path


@pytest.fixture
def box(tmp_path):
    stores = tmp_path / "stores"
    for seat in ("sanctuary-master", "belam"):
        (stores / seat / "t").mkdir(parents=True)
        subprocess.run(["git", "init", "-q", str(stores / seat / "t")], check=True)
    sbin, optbin = tmp_path / "sbin", tmp_path / "optbin"; sbin.mkdir(); optbin.mkdir()
    import shutil
    shutil.copy(BIN / "alarm_spool.py", optbin / "alarm_spool.py")                              # what host act 1 INSTALLS there, prose and all
    shutil.copy(REPO / "extensions" / "agi" / "guard" / "quiet-watch" / "agi-quiet-watch", sbin / "agi-quiet-watch")
    shutil.copy(REPO / "extensions" / "agi" / "tests" / "fixtures" / "boxkit" / "memguard-script.fixture", sbin / "agi-memguard.py")
    (sbin / "agi-clean").write_text("#!/bin/sh\n# box send is mentioned only in this comment\n   # and ssh-keygen -Y sign in this one\necho fine\n")
    (optbin / "box").write_text("#!/bin/sh\n# box send TO <msg>\nsend)echo x;;\n")
    env = {"PATH": os.environ["PATH"], "SBIN": str(sbin), "OPTBIN": str(optbin), "STORES": str(stores),
           "AS": str(_exe(tmp_path / "wrap.py", WRAP)),
           "RUNUSER": str(_exe(tmp_path / "runuser", '#!/bin/sh\nexport RUNUSER_AS="$2"\nshift 3\nexec "$@"\n')),
           "BOXBIN": str(_exe(tmp_path / "boxstub", STUB_BOX)),
           "VERIFY": str(_exe(tmp_path / "verify-ok", '#!/bin/sh\necho "Good signature for $AGI_POST@agi with ED25519 key"\n'))}
    return env, sbin, optbin, stores


def _run(env, **over):
    return subprocess.run(["sh", str(SCRIPT)], env={**env, **over}, capture_output=True, text=True, timeout=120)


def test_a_clean_install_passes_r1_and_both_drain_rows_deliver_a_signed_line_with_both_trailers(box):
    env, sbin, optbin, stores = box
    r = _run(env)
    assert r.returncode == 0, r.stdout + r.stderr
    assert "ok r1:" in r.stdout and "ok sanctuary-master -> belam:" in r.stdout and "ok belam -> sanctuary-master:" in r.stdout, r.stdout
    for seat, reader in (("sanctuary-master", "belam"), ("belam", "sanctuary-master")):
        msg = subprocess.run(["git", "-C", str(stores / seat / "t"), "log", "-1", f"refs/box/{seat}/{reader}", "--format=%B"], capture_output=True, text=True).stdout
        assert msg.startswith("[alarm first-start] first-start-") and "Alarm-job: first-start" in msg and "Alarm-id: " in msg, msg
        assert not (stores / seat / "alarm.spool").exists()                                   # the seat's drain emptied it


def test_r1_comment_lines_are_skipped_but_a_live_box_send_or_signing_line_is_red(box):
    env, sbin, optbin, stores = box
    (sbin / "agi-bad").write_text("#!/bin/sh\nrunuser -u x -- sh -c 'cd ~/t && box send \"$1\"' _ y\n")        # MUTANT: the old quiet-watch:24
    r = _run(env)
    assert r.returncode == 1 and "RED r1" in r.stdout and "agi-bad:2:" in r.stdout and "agi-clean" not in r.stdout and "optbin/box" not in r.stdout, r.stdout
    (sbin / "agi-bad").write_text("ssh-keygen -Y sign -f k -n box f\n")
    assert _run(env).returncode == 1


def test_a_drain_that_sends_nothing_or_an_unsigned_commit_is_red(box):
    env, *_ = box
    r = _run(env, BOX_FAIL="[off-matrix] x")                                                   # the box refuses: no commit on the out-ref
    assert r.returncode == 2 and "no commit with first-start-" in r.stdout, r.stdout
    unsigned = Path(env["VERIFY"]); unsigned.write_text("#!/bin/sh\necho 'error: no signature'\n")
    stores2 = Path(env["STORES"]).parent / "stores2"                                            # a fresh store: the first run's commits must not satisfy this one
    for seat in ("sanctuary-master", "belam"):
        (stores2 / seat / "t").mkdir(parents=True); subprocess.run(["git", "init", "-q", str(stores2 / seat / "t")], check=True)
    r = _run(env, STORES=str(stores2))
    assert r.returncode == 2 and r.stdout.count("is not signed by") == 2, r.stdout            # delivered, with trailers, but not signed by the seat


def test_the_shipped_install_is_green_and_todays_old_prose_in_alarm_spool_is_red(box):
    env, sbin, optbin, stores = box
    assert (optbin / "alarm_spool.py").read_text() == (BIN / "alarm_spool.py").read_text()      # the fixture really carries the real installed file
    r = _run(env, ROWS="")
    assert r.returncode == 0 and "ok r1:" in r.stdout, r.stdout                                  # the shipped agi-quiet-watch + alarm_spool.py + memguard render: GREEN
    text = (optbin / "alarm_spool.py").read_text()
    old = "for every spooled line the box tool, run from ~/t, mails it to <to> with"
    assert text.count(old) == 1
    (optbin / "alarm_spool.py").write_text(text.replace(old, "for every spooled line `cd ~/t && box send <to>` with"))      # MUTANT: the docstring as it was at e8b68385a1
    r = _run(env, ROWS="")
    assert r.returncode == 1 and "alarm_spool.py:10:" in r.stdout, r.stdout


def test_an_empty_rows_skips_the_drain_rows_and_only_r1_runs(box):
    env, *_ = box
    r = _run(env, ROWS="")
    assert r.returncode == 0 and "ok r1:" in r.stdout and "->" not in r.stdout, r.stdout
