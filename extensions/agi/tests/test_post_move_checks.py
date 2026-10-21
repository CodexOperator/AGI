"""post-move-checks.sh (goal:g7.16.1.11.45 S2): belam's per-move proof, run on a stub root + stub users, nothing live touched.

Council 3/3 14:44Z 10-21, the two MUTANTS that must go RED: usermod without groupmod (the gid check) and the key left in the home (the read
check). Each source mutant below removes ONE guard of the script and a world that guard exists for then PASSES: the test has teeth.
"""
import os
import shutil
import stat
import subprocess
from pathlib import Path

import pytest

REPO = Path(__file__).resolve().parents[3]
SCRIPT = REPO / "extensions" / "agi" / "guard" / "post-move-checks.sh"
OLD, NEW, UID, T = "director-general-3", "director-general-1", "1003", "20261021150000Z"

ID = r"""#!/bin/sh
u=${2#agi-};f=$(grep "^agi-$u:" $STUB/passwd) || exit 1
case $1 in -u) echo "$f"|cut -d: -f3;; -g) echo "$f"|cut -d: -f4;;
 -gn) g=$(echo "$f"|cut -d: -f4);grep ":x:$g:" $STUB/group|cut -d: -f1|head -n1;; *) exit 2;; esac
"""
GETENT = r"""#!/bin/sh
grep "^$2:" $STUB/$1
exit 0
"""
# systemctl is-active UNIT: the state is read from $STUB/active/UNIT (absent = a unit that never ran)
SYSTEMCTL = r"""#!/bin/sh
[ "$1" = is-active ]||exit 2
s=$(cat "$STUB/active/$2" 2>/dev/null)||s=inactive
echo "$s";[ "$s" = active ]
"""
# runuser -u U -- test -r F: U reads what is under its own home, else only what is o+r behind o+x dirs (a stub: the test is not root)
RUNUSER = r"""#!/bin/sh
u=$2;shift 3;[ "$1" = test ]&&[ "$2" = -r ]||exit 125;f=$3
home=$(grep "^$u:" $STUB/passwd|cut -d: -f6)
case $f in "$home"|"$home"/*)[ -r "$f" ];exit $?;; esac
[ -e "$f" ]||exit 1;[ $(( $(stat -c %a "$f") % 10 & 4 )) != 0 ]||exit 1
d=$(dirname "$f");while [ "$d" != "$TOP" ]&&[ "$d" != / ];do [ $(( $(stat -c %a "$d") % 10 & 1 )) != 0 ]||exit 1;d=$(dirname "$d");done
"""


def _exe(path, text):
    path.write_text(text)
    path.chmod(path.stat().st_mode | stat.S_IXUSR)
    return path


def _key(path):
    subprocess.run(["ssh-keygen", "-q", "-t", "ed25519", "-N", "", "-C", "k", "-f", str(path)], check=True)
    return " ".join(Path(f"{path}.pub").read_text().split()[:2])


class World:
    """A box AFTER a clean move director-general-3 -> director-general-1 (uid 1003 kept), before the new key exists."""

    def __init__(self, tmp):
        self.tmp = tmp
        self.root, self.stub, self.bin = tmp / "root", tmp / "stub", tmp / "bin"
        for d in (self.root, self.stub, self.bin):
            d.mkdir()
        self.home = tmp / "home" / NEW
        (self.home / ".ssh").mkdir(parents=True)
        (self.stub / "passwd").write_text(f"agi-{NEW}:x:{UID}:{UID}::{self.home}:/bin/sh\n")
        (self.stub / "group").write_text(f"agi-{NEW}:x:{UID}:\n")
        self.rk = self.root / "var/lib/agi/retired/keys" / f"{OLD}-{T}"
        self.rk.mkdir(parents=True, mode=0o700)
        self.rk.chmod(0o700)
        self.pub = _key(self.rk / "id_ed25519")
        for d in ("etc/sudoers.d", "etc/polkit-1", "etc/systemd", "etc/agi", "var/spool/cron"):
            (self.root / d).mkdir(parents=True)
        (self.root / "etc/sudoers.d/agi").write_text(f"agi-belam ALL=(agi-{NEW}) NOPASSWD: ALL\n")
        self.other = _key(tmp / "other")                       # a key OLD never held
        self.ring = self.root / "var/lib/agi/allowed_signers"
        self.ring.parent.mkdir(parents=True, exist_ok=True)
        self.ring.write_text(
            f'{OLD}@agi namespaces="git",valid-after="20261008000000Z",valid-before="20261015000000Z" {self.other}\n'
            f'{OLD}@agi namespaces="git",valid-after="20261015000000Z",valid-before="{T}" {self.pub}\n'
            # an earlier holder of the name director-general-1 (the old DG1, moved to goals-1 at 10-21 14:00Z): closed
            f'{NEW}@agi namespaces="git",valid-after="20261001000000Z",valid-before="20261021140000Z" {self.other}\n')
        self.env = {"PATH": os.environ["PATH"], "ROOT": str(self.root), "STUB": str(self.stub), "TOP": str(tmp), "ROOTUSER": subprocess.run(
            ["id", "-un"], capture_output=True, text=True).stdout.strip(),
            "ID": str(_exe(self.bin / "id", ID)), "GETENT": str(_exe(self.bin / "getent", GETENT)),
            "RUNUSER": str(_exe(self.bin / "runuser", RUNUSER)),
            "SYSTEMCTL": str(_exe(self.bin / "systemctl", SYSTEMCTL))}
        (self.stub / "active").mkdir()

    def first_start(self, key=None):
        with open(self.ring, "a") as f:
            f.write(f'{NEW}@agi namespaces="git",valid-after="20261021150500Z" {key or _key(self.tmp / "fresh")}\n')

    def check(self, *args, script=SCRIPT, **env):
        r = subprocess.run(["sh", str(script), "check", OLD, NEW, UID, T, *args], env={**self.env, **env}, capture_output=True, text=True, timeout=60)
        return r.returncode, {ln.split(":")[0].split(" ", 1)[1]: ln.split(" ", 1)[0] for ln in r.stdout.splitlines()}, r.stdout


@pytest.fixture
def w(tmp_path):
    return World(tmp_path)


def _red(res, *names):
    rc, st, out = res
    assert rc == 1 and all(st[n] == "FAIL" for n in names), out


def test_a_clean_move_before_the_first_start_is_green_and_ring_new_waits(w):
    rc, st, out = w.check()
    assert rc == 0, out
    assert st == {"uid": "ok", "gid": "ok", "old-name-free": "ok", "key-held": "ok", "key-unreadable": "ok", "key-not-in-home": "ok",
                  "ring-old": "ok", "ring-new": "wait", "grep-old": "ok", "old-post-inactive": "ok", "old-boxwake-inactive": "ok"}, out


def test_after_the_first_start_ring_new_needs_one_fresh_open_line_and_wait_becomes_red_under_the_flag(w):
    _red(w.check("--first-start"), "ring-new")
    w.first_start()
    rc, st, out = w.check("--first-start")
    assert rc == 0 and st["ring-new"] == "ok" and "wait" not in out, out


def test_MUTANT_usermod_without_groupmod_is_red_on_the_gid_check_and_the_old_group_name(w):
    (w.stub / "group").write_text(f"agi-{OLD}:x:{UID}:\n")            # the user was renamed, the group was not: gid still 1003, name wrong
    rc, st, out = w.check()
    _red((rc, st, out), "gid", "old-name-free")
    assert st["uid"] == "ok", out                                     # usermod -l alone keeps the uid: only the group checks see it


def test_MUTANT_the_key_left_in_the_home_is_red_on_the_read_side(w):
    shutil.copy(w.rk / "id_ed25519", w.home / ".ssh" / "id_ed25519")                  # cp, not mv: the new uid owns a copy
    _red(w.check(), "key-not-in-home")
    shutil.rmtree(w.rk)                                                                # the key never reached retired/: only the home holds it
    (w.rk).mkdir(mode=0o700)
    _red(w.check(), "key-held", "key-unreadable")


def test_a_retired_dir_anyone_can_read_is_red_on_both_key_checks(w):
    w.rk.chmod(0o755)
    (w.rk / "id_ed25519").chmod(0o644)
    _red(w.check(), "key-held", "key-unreadable")


def test_a_runuser_that_cannot_act_as_the_new_user_is_red_not_a_vacuous_pass(w):
    _exe(w.bin / "runuser", "#!/bin/sh\nexit 1\n")                    # what a non-root runuser does
    _red(w.check(), "key-unreadable")


def test_a_wrong_uid_is_red(w):
    (w.stub / "passwd").write_text(f"agi-{NEW}:x:2000:2000::{w.home}:/bin/sh\n")
    (w.stub / "group").write_text(f"agi-{NEW}:x:2000:\n")
    _red(w.check(), "uid")


def test_ring_old_must_be_closed_at_T_and_ring_new_must_have_no_stale_open_line_and_not_the_retired_key(w):
    ring = w.ring.read_text()
    w.ring.write_text(ring.replace(f',valid-before="{T}"', ""))        # the move never stamped the old principal
    _red(w.check(), "ring-old")
    w.ring.write_text(ring.replace(f',valid-before="{T}"', ',valid-before="20261021150001Z"'))
    _red(w.check(), "ring-old")                                       # closed, but not at T
    w.ring.write_text(ring.replace(',valid-before="20261021140000Z"', ""))             # the earlier holder's key is still open for the name
    _red(w.check(), "ring-new")
    w.ring.write_text(ring)
    w.first_start(key=w.pub)                                          # a "fresh" key that is the carried one
    _red(w.check("--first-start"), "ring-new")


def test_grep_old_is_red_for_a_content_hit_and_for_a_file_named_after_the_old_user(w):
    (w.root / "etc/sudoers.d/old").write_text(f"agi-{OLD} ALL=(ALL) NOPASSWD: ALL\n")
    _red(w.check(), "grep-old")
    (w.root / "etc/sudoers.d/old").unlink()
    (w.root / f"var/spool/cron/agi-{OLD}").write_text("")
    _red(w.check(), "grep-old")
    (w.root / f"var/spool/cron/agi-{OLD}").unlink()
    (w.root / "etc/systemd/x.service").write_text(f"User=agi-{OLD}x\nGroup=notagi-{OLD}\n")     # not a word match: -w
    assert w.check()[0] == 0


def test_missing_scan_dirs_are_red_not_an_empty_pass(w):
    _red(w.check(SCAN=str(w.root / "nowhere")), "grep-old")


def test_pre_prints_the_uid_and_proves_the_new_name_is_free(w):
    (w.stub / "passwd").write_text(f"agi-{OLD}:x:{UID}:{UID}::/h:/bin/sh\n")
    (w.stub / "group").write_text(f"agi-{OLD}:x:{UID}:\n")
    r = subprocess.run(["sh", str(SCRIPT), "pre", OLD, NEW], env=w.env, capture_output=True, text=True)
    assert r.returncode == 0 and r.stdout.splitlines()[-1] == f"uid {UID}", r.stdout
    with open(w.stub / "group", "a") as f:
        f.write(f"agi-{NEW}:x:555:\n")                                # a group of the target name is left over
    r = subprocess.run(["sh", str(SCRIPT), "pre", OLD, NEW], env=w.env, capture_output=True, text=True)
    assert r.returncode == 1 and "FAIL pre-new-free" in r.stdout, r.stdout
    (w.stub / "passwd").write_text(f"agi-{OLD}:x:{UID}:2000::/h:/bin/sh\n")      # gid != uid before the move
    r = subprocess.run(["sh", str(SCRIPT), "pre", OLD, NEW], env=w.env, capture_output=True, text=True)
    assert "FAIL pre-old-user" in r.stdout, r.stdout


def test_bad_arguments_are_refused_with_rc_2(w):
    for args in (["check", OLD, NEW, "10x3", T], ["check", OLD, NEW, UID, "2026-10-21"], ["check", "A;rm", NEW, UID, T], ["bogus", OLD, NEW]):
        r = subprocess.run(["sh", str(SCRIPT), *args], env=w.env, capture_output=True, text=True)
        assert r.returncode == 2, (args, r.stdout, r.stderr)


def _mutant(tmp, old, new):
    src = SCRIPT.read_text()
    assert src.count(old) == 1, old
    p = tmp / "mutant.sh"
    p.write_text(src.replace(old, new))
    return p


def test_each_guard_of_the_script_has_a_world_that_only_it_catches(w, tmp_path):
    # no positive control: a runuser that cannot run passes the read check
    m = _mutant(tmp_path, '"$RUNUSER" -u "$n" -- test -r "$home" || return 1;', "")
    _exe(w.bin / "runuser", "#!/bin/sh\nexit 1\n")
    assert w.check(script=m)[1]["key-unreadable"] == "ok"
    assert w.check()[1]["key-unreadable"] == "FAIL"
    # no existence guard: a retired key that is not there passes the read check
    shutil.rmtree(w.rk)
    w.rk.mkdir(mode=0o700)
    _exe(w.bin / "runuser", RUNUSER)
    m = _mutant(tmp_path, '[ -f "$rk/id_ed25519" ]||return 1;', "")
    assert w.check(script=m)[1]["key-unreadable"] == "ok" and w.check()[1]["key-unreadable"] == "FAIL"


def test_the_gid_guard_has_a_world_only_it_catches(w, tmp_path):
    (w.stub / "group").write_text(f"agi-{OLD}:x:{UID}:\n")
    m = _mutant(tmp_path, 'test "$gn" = "$n" -a "$gi" = "$UID_"', 'test "$gi" = "$UID_"')
    assert w.check(script=m)[1]["gid"] == "ok" and w.check()[1]["gid"] == "FAIL"
    # and the home-copy guard: without it the cp'd key is invisible to every other check
    shutil.copy(w.rk / "id_ed25519", w.home / ".ssh" / "id_ed25519")
    m = _mutant(tmp_path, 'test -n "$pub" -a -z "$left"', "true")
    assert w.check(script=m)[1]["key-not-in-home"] == "ok" and w.check()[1]["key-not-in-home"] == "FAIL"


def test_MUTANT_a_projection_in_the_window_that_minted_a_fresh_old_user_is_red_on_the_name_check(w):
    with open(w.stub / "passwd", "a") as f:                                  # sysusers re-created agi-<old> between the usermod and the bump
        f.write(f"agi-{OLD}:x:998:998::/nonexistent:/usr/sbin/nologin\n")
    _red(w.check(), "old-name-free")
    (w.stub / "passwd").write_text(f"agi-{NEW}:x:{UID}:{UID}::{w.home}:/bin/sh\n")
    with open(w.stub / "group", "a") as f:                                   # or only its group
        f.write(f"agi-{OLD}:x:998:\n")
    _red(w.check(), "old-name-free")


@pytest.mark.parametrize("unit,check", [(f"agi-post@{OLD}", "old-post-inactive"), (f"agi-boxwake@{OLD}", "old-boxwake-inactive")])
def test_MUTANT_an_old_unit_that_is_active_or_starting_or_unanswered_is_red_one_row_each(w, unit, check):
    for state in ("active", "activating", "deactivating"):
        (w.stub / "active" / unit).write_text(state + "\n")
        rc, st, out = w.check()
        _red((rc, st, out), check)
        assert all(v != "FAIL" for k, v in st.items() if k.startswith("old-") and k != check and k.endswith("-inactive")), out    # the OTHER unit's row stays green
    (w.stub / "active" / unit).write_text("failed\n")                         # a unit that ended failed is not running
    assert w.check()[1][check] == "ok"
    _exe(w.bin / "systemctl", "#!/bin/sh\nexit 1\n")                          # no answer at all is not a pass
    _red(w.check(), "old-post-inactive", "old-boxwake-inactive")


def test_each_after_4b_row_has_a_world_only_it_catches(w, tmp_path):
    (w.stub / "active" / f"agi-post@{OLD}").write_text("active\n")
    (w.stub / "active" / f"agi-boxwake@{OLD}").write_text("active\n")
    m = _mutant(tmp_path, "inactive|failed)return 0;;esac;return 1;}", "*)return 0;;esac;return 1;}")
    st = w.check(script=m)[1]
    assert st["old-post-inactive"] == "ok" and st["old-boxwake-inactive"] == "ok"
    st = w.check()[1]
    assert st["old-post-inactive"] == "FAIL" and st["old-boxwake-inactive"] == "FAIL"
    with open(w.stub / "passwd", "a") as f:
        f.write(f"agi-{OLD}:x:998:998::/nonexistent:/usr/sbin/nologin\n")
    m = _mutant(tmp_path, '[ -z "$($GETENT passwd "agi-$1")" ]&&', "")
    assert w.check(script=m)[1]["old-name-free"] == "ok" and w.check()[1]["old-name-free"] == "FAIL"
