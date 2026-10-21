"""post-move-checks.sh (goal:g7.16.1.11.45 S2): belam's per-move proof, run on a stub root + stub users, nothing live touched.

Council 3/3 14:44Z 10-21, the two MUTANTS that must go RED: usermod without groupmod (the gid check) and the key left in the home (the read
check). Each source mutant below removes ONE guard of the script and a world that guard exists for then PASSES: the test has teeth.
"""
import calendar
import json
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
# systemctl show [--timestamp=utc] -p PROP [--value] UNIT: the value is read from $STUB/show/UNIT.PROP (absent = the empty value of a unit that never ran)
case $1 in is-enabled)s=$(cat "$STUB/enabled/$2" 2>/dev/null)||s=disabled;echo "$s";[ "$s" = enabled ];exit;;is-active);;
 show)shift;v=;for a in "$@";do [ "$a" = --value ]&&v=1;done;ps=;u=;while [ $# -gt 0 ];do case $1 in -p)ps="$ps $2";shift;; -*);; *)u=$1;; esac;shift;done
  for p in $ps;do f="$STUB/show/$u.$p";x=$(cat "$f" 2>/dev/null);if [ -n "$v" ];then echo "$x";else [ -z "$x" ]||echo "$p=$x";fi;[ ! -f "$f.then" ]||mv "$f.then" "$f";done;exit 0;;*)exit 2;;esac
s=$(cat "$STUB/active/$2" 2>/dev/null)||s=inactive
echo "$s";[ "$s" = active ]
"""
# stat -c %u PATH and find DIR -maxdepth 1 -uid N -name GLOB: the owner of a path under WORK is the number in $STUB/owner/<basename> (absent = nobody)
STAT = r"""#!/bin/sh
[ "$1" = -c ]&&[ "$2" = %u ]||exit 2;[ -e "$3" ]||exit 1;cat "$STUB/owner/$(basename "$3")" 2>/dev/null||echo 0
"""
FIND = r"""#!/bin/sh
d=$1;shift;[ "$1" = -maxdepth ]&&[ "$3" = -uid ]&&[ "$5" = -name ]||exit 2;n=$4;g=$6
for f in "$d"/$g;do [ -e "$f" ]||continue;[ "$(cat "$STUB/owner/$(basename "$f")" 2>/dev/null)" = "$n" ]&&echo "$f";done;exit 0
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
        for d in ("etc/sudoers.d", "etc/polkit-1", "etc/systemd", "run/systemd/system", "etc/agi", "var/spool/cron"):
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
        self.env = {"PATH": os.environ["PATH"], "ROOT": str(self.root), "STUB": str(self.stub), "TOP": str(tmp), "STAYS_S": "0", "WORK": str(tmp / "work"),
            "STAT": str(_exe(self.bin / "stat", STAT)), "FIND": str(_exe(self.bin / "find", FIND)), "ROOTUSER": subprocess.run(
            ["id", "-un"], capture_output=True, text=True).stdout.strip(),
            "ID": str(_exe(self.bin / "id", ID)), "GETENT": str(_exe(self.bin / "getent", GETENT)),
            "RUNUSER": str(_exe(self.bin / "runuser", RUNUSER)),
            "SYSTEMCTL": str(_exe(self.bin / "systemctl", SYSTEMCTL))}
        (self.stub / "active").mkdir()
        (self.stub / "enabled").mkdir()
        (self.stub / "active" / f"agi-carry@{NEW}.path").write_text("active\n")      # the renamed post's mail wake, after 4b
        (self.stub / "enabled" / f"agi-carry@{NEW}.path").write_text("enabled\n")
        (self.stub / "show").mkdir()
        self.up(0)
        (tmp / "work").mkdir()
        (self.stub / "owner").mkdir()
        self.gate(NEW, UID)                                                       # the moved post's gate dir, renamed with it (step 3)
        self.main = self.root / "data/work/agi"                                          # MAIN: the repo the mail refs live in (R7)
        self.main.mkdir(parents=True)
        self.git("init", "-q")
        self.keys = 0
        (self.home / ".claude.json").write_text(json.dumps({"projects": {                # trust is keyed by MAIN's root; the old home's key is dead (R10, R11)
            "/data/work/agi": {"hasTrustDialogAccepted": True}, f"{self.home.parent / OLD}/t": {"hasTrustDialogAccepted": True}}}))
        (self.home / ".claude/projects").mkdir(parents=True)
        (self.home / ".claude/projects/s.jsonl").write_text(f"cwd {self.home.parent / OLD}/t\n")  # transcripts are not hits
        self.carry = self.root / "etc/agi/carry.env"                                       # 4b's write at 15:01:00Z, the projection started at 15:01:30Z, success
        self.carry.write_text("AGI_BOX=encryption-town\nAGI_TRUNK=" + "a" * 40 + "\n")
        self.wrote("20261021150100")
        self.projected("Wed 2026-10-21 15:01:30 UTC")

    def git(self, *a, **kw):
        env = {**os.environ, "GIT_CONFIG_GLOBAL": "/dev/null", "GIT_CONFIG_SYSTEM": "/dev/null", **kw.pop("env", {})}
        return subprocess.run(["git", "-C", str(self.main), *a], check=True, capture_output=True, text=True, env=env).stdout.strip()

    def principal(self, name):
        """a fresh key for NAME@agi, an OPEN line in the ring; returns the private key path"""
        self.keys += 1
        k = self.tmp / f"k{self.keys}"
        pub = _key(k)
        with open(self.ring, "a") as f:
            f.write(f'{name}@agi namespaces="git",valid-after="20261021150500Z" {pub}\n')
        return k

    def mail(self, ref, signer=None, key=None):
        """a commit on REF (refs/box/..., refs/held/..., refs/heads/posts/...); signed as SIGNER with the private key KEY, or unsigned"""
        tree = self.git("hash-object", "-w", "-t", "tree", "/dev/null")
        e = {"GIT_AUTHOR_NAME": signer or "x", "GIT_AUTHOR_EMAIL": f"{signer or 'x'}@agi", "GIT_COMMITTER_NAME": signer or "x", "GIT_COMMITTER_EMAIL": f"{signer or 'x'}@agi"}
        sig = ["-c", "gpg.format=ssh", "-c", f"user.signingkey={key}", "-S"] if key else []
        c = self.git(*sig[:4], "commit-tree", *sig[4:], "-m", "x", tree, env=e)
        self.git("update-ref", ref, c)
        return c

    def gate(self, name, uid, prefix="gate-"):
        """a dir WORK/<prefix><name> owned (by the stub's sidecar) by UID"""
        d = self.tmp / "work" / f"{prefix}{name}"
        d.mkdir(exist_ok=True)
        (self.stub / "owner" / d.name).write_text(f"{uid}\n")
        return d

    def up(self, restarts=0, active="active", sub="running"):
        """agi-post@NEW as `systemctl show` sees it"""
        for k, v in (("ActiveState", active), ("SubState", sub), ("NRestarts", restarts)):
            (self.stub / "show" / f"agi-post@{NEW}.{k}").write_text(f"{v}\n")

    def wrote(self, stamp):
        t = calendar.timegm((int(stamp[:4]), int(stamp[4:6]), int(stamp[6:8]), int(stamp[8:10]), int(stamp[10:12]), int(stamp[12:14])))
        os.utime(self.carry, (t, t))

    def projected(self, started, result="success"):
        (self.stub / "show" / "agi-project.service.ExecMainStartTimestamp").write_text(started + "\n")
        (self.stub / "show" / "agi-project.service.Result").write_text(result + "\n")

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
                  "ring-old": "ok", "ring-new": "wait", "grep-old": "ok", "old-post-inactive": "ok", "old-boxwake-inactive": "ok",
                  "new-carry-path": "ok", "projected": "ok", "refs-left": "ok", "outbox-signer": "ok", "flags": "ok", "sweep": "ok",
                  "new-boxwake": "wait"}, out


def test_after_the_first_start_ring_new_needs_one_fresh_open_line_and_wait_becomes_red_under_the_flag(w):
    _red(w.check("--first-start"), "ring-new")
    w.first_start()
    (w.stub / "active" / f"agi-boxwake@{NEW}").write_text("active\n")      # the start brought the wake up with the post (Wants=)
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


# K-a (council 16:24Z): the unit INSTANCE paths of the old name, measured on this box for director-general-1: the projected wants link and the two .service.d drop-ins
# under /run/systemd/system, the enabled agi-carry@<old>.path under /etc/systemd/system. Each was invisible to the word grep and the file-NAMED-agi-<old> leg.
INSTANCE_PATHS = [
    f"run/systemd/system/multi-user.target.wants/agi-post@{OLD}.service",
    f"run/systemd/system/agi-post@{OLD}.service.d",
    f"run/systemd/system/agi-boxwake@{OLD}.service.d",
    f"etc/systemd/system/paths.target.wants/agi-carry@{OLD}.path",
]


@pytest.mark.parametrize("rel", INSTANCE_PATHS)
def test_MUTANT_a_unit_instance_of_the_old_name_is_red_in_run_and_in_etc(w, rel):
    p = w.root / rel
    p.parent.mkdir(parents=True, exist_ok=True)
    if rel.endswith(".d"):
        p.mkdir()
        (p / "h.conf").write_text("[Service]\nEnvironment=X=1\n")                    # a drop-in with no name of the old user inside: only its path says it
    else:
        p.symlink_to("../agi-post@.service")
    _red(w.check(), "grep-old")


def test_a_unit_instance_of_a_different_name_or_a_longer_one_is_not_a_hit(w):
    for rel in (f"run/systemd/system/agi-post@{NEW}.service.d", f"run/systemd/system/agi-post@{OLD}0.service.d", f"run/systemd/system/agi-post@x{OLD}.service.d"):
        (w.root / rel).mkdir(parents=True)
    assert w.check()[1]["grep-old"] == "ok"


def test_the_instance_leg_has_a_world_only_it_catches(w, tmp_path):
    (w.root / f"run/systemd/system/agi-post@{OLD}.service.d").mkdir(parents=True)
    (w.root / f"etc/systemd/system/paths.target.wants").mkdir(parents=True)
    (w.root / f"etc/systemd/system/paths.target.wants/agi-carry@{OLD}.path").symlink_to("../agi-carry@.path")
    m = _mutant(tmp_path, 'find $SCAN -name "*@$OLD.*";', "")                              # today's two legs
    assert w.check(script=m)[1]["grep-old"] == "ok" and w.check()[1]["grep-old"] == "FAIL"


# K-c: C7 said a missing scan dir FAILs; the code counted dirs and skipped one missing of five
def test_one_missing_scan_dir_of_six_is_red_and_named(w):
    shutil.rmtree(w.root / "etc/polkit-1")
    rc, st, out = w.check()
    assert rc == 1 and st["grep-old"] == "FAIL" and "MISSING scan dir(s): " in out and "etc/polkit-1" in out, out


def test_the_missing_dir_guard_has_a_world_only_it_catches(w, tmp_path):
    shutil.rmtree(w.root / "var/spool/cron")
    m = _mutant(tmp_path, 'test -z "$miss" -a -z "$hits"', 'test "$(echo $SCAN|wc -w)" -gt "$(echo $miss|wc -w)" -a -z "$hits"')      # today: at least one dir exists
    assert w.check(script=m)[1]["grep-old"] == "ok" and w.check()[1]["grep-old"] == "FAIL"


# K-b: the renamed post's mail wake. Nothing enables agi-carry@<new>.path but `systemctl enable --now` in host-act-encryption-town.sh move
@pytest.mark.parametrize("enabled,active", [("disabled", "active"), ("enabled", "inactive"), ("enabled", "activating"), ("", "")])
def test_MUTANT_a_new_carry_path_that_is_not_both_enabled_and_active_is_red(w, enabled, active):
    (w.stub / "enabled" / f"agi-carry@{NEW}.path").write_text(enabled + "\n")
    (w.stub / "active" / f"agi-carry@{NEW}.path").write_text(active + "\n")
    _red(w.check(), "new-carry-path")


def test_a_systemctl_that_does_not_answer_is_red_on_the_carry_row_too(w):
    _exe(w.bin / "systemctl", "#!/bin/sh\nexit 1\n")
    _red(w.check(), "new-carry-path")


def test_the_carry_row_has_a_world_only_it_catches(w, tmp_path):
    (w.stub / "enabled" / f"agi-carry@{NEW}.path").unlink()                                 # the move never enabled it
    m = _mutant(tmp_path, "carry(){ [", "carry(){ return 0; [")
    assert w.check(script=m)[1]["new-carry-path"] == "ok" and w.check()[1]["new-carry-path"] == "FAIL"


# the projection: agi-project.path was never active on this box (council 17:58Z 10-21), so 4b = `agi.sh host` + `systemctl start agi-project.service`
@pytest.mark.parametrize("started,result", [
    ("Wed 2026-10-21 15:00:59 UTC", "success"),     # the last start was BEFORE 4b's carry.env write: the host's /run is the old pin's
    ("", "success"),                                # never started (an empty ExecMainStartTimestamp, as on a unit that never ran)
    ("Wed 2026-10-21 15:01:30 UTC", "exit-code"),   # started after the write and failed
    ("Wed 2026-10-21 15:01:30 UTC", ""),            # no Result at all
    ("not a time", "success"),                      # an unreadable stamp is never a pass
])
def test_MUTANT_a_projection_not_started_after_the_pin_write_or_not_successful_is_red(w, started, result):
    w.projected(started, result)
    _red(w.check(), "projected")


def test_a_start_in_the_same_second_as_the_write_or_later_is_green(w):
    w.projected("Wed 2026-10-21 15:01:00 UTC")
    assert w.check()[1]["projected"] == "ok"
    w.projected("Thu 2026-10-22 03:00:00 UTC")
    assert w.check()[1]["projected"] == "ok"


def test_a_carry_env_written_after_the_projection_is_red_and_a_missing_one_is_red(w):
    w.wrote("20261021153000")                                      # a second `agi.sh host` after the start: /run is one pin behind again
    _red(w.check(), "projected")
    w.carry.unlink()
    _red(w.check(), "projected")


def test_a_systemctl_that_does_not_answer_is_red_on_the_projected_row_too(w):
    _exe(w.bin / "systemctl", "#!/bin/sh\nexit 1\n")
    _red(w.check(), "projected")


def test_the_projected_row_has_a_world_only_each_of_its_guards_catches(w, tmp_path):
    w.projected("Wed 2026-10-21 15:00:59 UTC")                     # started before the write
    m = _mutant(tmp_path, '[ "$ps" -ge "$pc" ]&&', "")
    assert w.check(script=m)[1]["projected"] == "ok" and w.check()[1]["projected"] == "FAIL"
    w.projected("Wed 2026-10-21 15:01:30 UTC", "exit-code")        # started after, failed
    m = _mutant(tmp_path, '&&[ "$($SYSTEMCTL show -p Result --value agi-project.service 2>/dev/null)" = success ]', "")
    assert w.check(script=m)[1]["projected"] == "ok" and w.check()[1]["projected"] == "FAIL"
    w.projected("", "success")                                     # never started: `date -d ""` is today's midnight, which a carry.env from long ago precedes
    w.wrote("20000101000000")
    m = _mutant(tmp_path, '[ -n "$ps" ]||return 1;', "")
    assert w.check(script=m)[1]["projected"] == "ok" and w.check()[1]["projected"] == "FAIL"
    w.projected("not a time", "success")                           # an unparsable stamp
    m = _mutant(tmp_path, 'ps=$(date -u -d "$ps" +%s 2>/dev/null)||return 1', 'ps=$(date -u -d "$ps" +%s 2>/dev/null||echo 9999999999)')
    assert w.check(script=m)[1]["projected"] == "ok" and w.check()[1]["projected"] == "FAIL"
    w.carry.unlink()                                               # no carry.env to compare against
    w.projected("Wed 2026-10-21 15:01:30 UTC")
    m = _mutant(tmp_path, 'pc=$(stat -c %Y "$CARRY" 2>/dev/null)||return 1', 'pc=$(stat -c %Y "$CARRY" 2>/dev/null||echo 0)')
    assert w.check(script=m)[1]["projected"] == "ok" and w.check()[1]["projected"] == "FAIL"


# R7 (council 18:13Z): the inbox moved with the agent, the OUTBOX and the peers' marks of the old name were retired, never moved
LEFT = [f"refs/heads/posts/{OLD}", f"refs/box/{OLD}/sanctuary-master", f"refs/box/belam/{OLD}", f"refs/held/{OLD}/belam", f"refs/held/alive/{OLD}"]


@pytest.mark.parametrize("ref", LEFT)
def test_MUTANT_a_ref_of_the_old_name_left_behind_is_red(w, ref):
    w.mail(ref)
    _red(w.check(), "refs-left")


def test_refs_of_the_new_name_of_a_retired_namespace_and_of_a_longer_name_are_not_left_behind(w):
    for ref in (f"refs/heads/posts/{NEW}", f"refs/box/{NEW}/belam", f"refs/box/belam/{NEW}", f"refs/held/{NEW}/belam", f"refs/retired/{OLD}-{T}/box/belam",
                f"refs/retired/{OLD}-{T}/held/alive", f"refs/remotes/origin/posts/{OLD}", f"refs/heads/posts/{OLD}x", f"refs/box/{OLD}x/belam", f"refs/box/belam/x{OLD}"):
        w.mail(ref)
    assert w.check()[1]["refs-left"] == "ok"


def test_an_unreadable_repo_is_red_on_both_ref_rows_never_an_empty_pass(w):
    _red(w.check(MAIN=str(w.tmp / "no-such-repo")), "refs-left", "outbox-signer")


def test_the_outbox_tip_must_verify_for_the_new_name_and_an_empty_outbox_is_fine(w):
    assert w.check()[1]["outbox-signer"] == "ok"
    k = w.principal(NEW)
    w.mail(f"refs/box/{NEW}/belam", NEW, k)
    w.mail(f"refs/box/{NEW}/alive", NEW, k)
    assert w.check()[1]["outbox-signer"] == "ok"
    w.mail(f"refs/box/{NEW}/sanctuary-master")                       # unsigned
    _red(w.check(), "outbox-signer")


def test_MUTANT_the_outbox_moved_from_the_old_name_is_red_on_the_signer_row(w, tmp_path):
    old_key = w.principal(OLD)                                      # a key the ring honours for the OLD name
    w.mail(f"refs/box/{OLD}/belam", OLD, old_key)
    w.git("update-ref", f"refs/box/{NEW}/belam", w.git("rev-parse", f"refs/box/{OLD}/belam"))   # the moved outbox
    w.git("update-ref", "-d", f"refs/box/{OLD}/belam")
    _red(w.check(), "outbox-signer")
    m = _mutant(tmp_path, 'grep -q "for $NEW@agi with"||bad=', 'grep -q "for .*@agi with"||bad=')
    assert w.check(script=m)[1]["outbox-signer"] == "ok"


# R10: the trust dialog (belam measured: every seat's .claude.json keys projects by MAIN's root)
@pytest.mark.parametrize("doc", [None, {}, {"projects": {}}, {"projects": {"/data/work/agi": {}}}, {"projects": {"/data/work/agi": {"hasTrustDialogAccepted": False}}},
                                 {"projects": {"/var/lib/agi/x/t": {"hasTrustDialogAccepted": True}}}])
def test_MUTANT_flags_skipped_or_wrong_is_red(w, doc):
    f = w.home / ".claude.json"
    f.unlink()
    if doc is not None:
        f.write_text(json.dumps(doc))
    _red(w.check(), "flags")


def test_the_flags_row_has_a_world_only_it_catches(w, tmp_path):
    (w.home / ".claude.json").write_text(json.dumps({"projects": {"/data/work/agi": {"hasTrustDialogAccepted": False}}}))
    m = _mutant(tmp_path, "hasTrustDialogAccepted==true", "hasTrustDialogAccepted!=null")
    assert w.check(script=m)[1]["flags"] == "ok" and w.check()[1]["flags"] == "FAIL"


# R11: the sweep of the old home path inside the new home
OLDHOME = lambda w: str(w.home.parent / OLD)       # noqa: E731


@pytest.mark.parametrize("rel", [".gitconfig", ".config/git/config", "bin/agi-x", ".claude/settings.json", ".claude/settings.local.json", "t/.git/hooks/pre-commit", "hooks/x"])
def test_MUTANT_the_old_home_in_a_file_the_post_executes_is_red_and_named(w, rel):
    f = w.home / rel
    f.parent.mkdir(parents=True, exist_ok=True)
    f.write_text(f"path = {OLDHOME(w)}/t\n")
    rc, st, out = w.check()
    assert st["sweep"] == "FAIL" and f"EXECUTED: {rel}" in out.replace("EXECUTED:", "EXECUTED: ").replace("  ", " "), out


def test_a_hit_in_a_file_nothing_executes_is_named_but_green_and_transcripts_and_dead_project_keys_are_not_hits(w):
    assert w.check()[1]["sweep"] == "ok"
    (w.home / "notes.txt").write_text(f"was {OLDHOME(w)}/t\n")
    rc, st, out = w.check()
    assert st["sweep"] == "ok" and "notes.txt" in out and "1 file(s)" in out, out
    d = json.loads((w.home / ".claude.json").read_text())
    d["lastCwd"] = f"{OLDHOME(w)}/t"                                  # a LIVE key naming the old home is a hit, though not executed
    (w.home / ".claude.json").write_text(json.dumps(d))
    rc, st, out = w.check()
    assert st["sweep"] == "ok" and ".claude.json" in out.split("sweep:")[1], out


def test_a_longer_home_name_is_not_a_hit(w):
    (w.home / "x.txt").write_text(f"{OLDHOME(w)}-2/t {OLDHOME(w)}x\n")
    assert "1 file" not in w.check()[2] and w.check()[1]["sweep"] == "ok" and "0 file(s)" in w.check()[2]


def test_the_sweep_row_has_a_world_only_its_executed_leg_catches(w, tmp_path):
    (w.home / ".gitconfig").write_text(f"[core]\n\thooksPath = {OLDHOME(w)}/hooks\n")
    m = _mutant(tmp_path, 'run="$run $h";; esac;done', ':;; esac;done')
    assert w.check(script=m)[1]["sweep"] == "ok" and w.check()[1]["sweep"] == "FAIL"


# R12: the live wake is agi-boxwake@<new>, started with agi-post@<new> (Wants=); agi-carry@.path watches a g.git no post has
def test_boxwake_waits_before_the_start_is_red_after_it_unless_active(w):
    rc, st, out = w.check()
    assert st["new-boxwake"] == "wait" and rc == 0 and "NOT the wake" in out, out
    w.first_start()
    _red(w.check("--first-start"), "new-boxwake")
    (w.stub / "active" / f"agi-boxwake@{NEW}").write_text("active\n")
    rc, st, out = w.check("--first-start")
    assert rc == 0 and st["new-boxwake"] == "ok" and "wait" not in st.values(), out


def test_a_carry_path_that_is_active_does_not_make_the_wake(w):
    w.first_start()
    _red(w.check("--first-start"), "new-boxwake")               # the world has new-carry-path enabled and active, and still no wake
    assert w.check("--first-start")[1]["new-carry-path"] == "ok"


def test_the_boxwake_row_has_a_world_only_its_first_start_leg_catches(w, tmp_path):
    w.first_start()
    m = _mutant(tmp_path, 'say FAIL new-boxwake', 'say ok new-boxwake')
    assert w.check("--first-start", script=m)[1]["new-boxwake"] == "ok" and w.check("--first-start")[1]["new-boxwake"] == "FAIL"


# G3's red (council 20:00Z): run 2 printed 18 ok over a post that crash-looped; `stays-up` looks twice, only with --first-start
def test_stays_up_is_absent_from_run_1_so_run_1_keeps_its_18_rows_and_present_in_run_2(w):
    rc, st, out = w.check()
    assert "stays-up" not in st and "name-dirs" not in st and len(st) == 18, out
    w.first_start()
    (w.stub / "active" / f"agi-boxwake@{NEW}").write_text("active\n")
    rc, st, out = w.check("--first-start")
    assert rc == 0 and st["stays-up"] == "ok" and st["name-dirs"] == "ok" and len(st) == 20, out


def _run2(w, script=SCRIPT):
    if not getattr(w, "started", False):                           # the first start happens once per world
        w.first_start()
        w.started = True
    (w.stub / "active" / f"agi-boxwake@{NEW}").write_text("active\n")
    return w.check("--first-start", script=script)


def test_MUTANT_a_post_that_exits_and_restarts_between_the_two_reads_is_red(w):
    (w.stub / "show" / f"agi-post@{NEW}.NRestarts.then").write_text("1\n")       # the second read sees one restart more
    _red(_run2(w), "stays-up")


@pytest.mark.parametrize("active,sub", [("activating", "auto-restart"), ("inactive", "dead"), ("failed", "failed"), ("active", "start"), ("", "")])
def test_MUTANT_a_post_that_is_not_active_and_running_is_red(w, active, sub):
    w.up(0, active, sub)
    _red(_run2(w), "stays-up")


def test_a_restart_count_that_is_missing_or_a_silent_systemctl_is_red(w):
    (w.stub / "show" / f"agi-post@{NEW}.NRestarts").unlink()
    _red(_run2(w), "stays-up")
    _exe(w.bin / "systemctl", "#!/bin/sh\nexit 1\n")
    _red(_run2(w), "stays-up")


def test_a_post_that_restarted_before_the_first_read_but_is_stable_across_the_window_is_ok(w):
    w.up(3)                                                         # NRestarts 3 in both reads: the window is what matters
    assert _run2(w)[1]["stays-up"] == "ok"


def test_the_window_defaults_to_60_seconds(w):
    assert "${STAYS_S:-60}" in SCRIPT.read_text()


def test_the_stays_up_row_has_a_world_only_each_of_its_guards_catches(w, tmp_path):
    def restarts_then(n):                                           # a one-shot: the second read sees the new count
        (w.stub / "show" / f"agi-post@{NEW}.NRestarts").write_text("0\n")
        (w.stub / "show" / f"agi-post@{NEW}.NRestarts.then").write_text(f"{n}\n")
    m = _mutant(tmp_path, '[ -n "$n1" ]&&[ "$n1" = "$n2" ]', '[ -n "$n1" ]')
    restarts_then(1)
    assert _run2(w, m)[1]["stays-up"] == "ok"
    restarts_then(1)
    assert _run2(w)[1]["stays-up"] == "FAIL"
    w.up(0, "activating", "running")                                # only the ActiveState test sees this one
    m = _mutant(tmp_path, "grep -qx 'ActiveState=active'&&", "")
    assert _run2(w, m)[1]["stays-up"] == "ok" and _run2(w)[1]["stays-up"] == "FAIL"
    w.up(0, "active", "auto-restart")                               # only the SubState test sees this one
    m = _mutant(tmp_path, "printf '%s\\n' \"$r\"|grep -qx 'SubState=running'||return 1", "printf '%s\\n' \"$r\"|grep -qx 'SubState=running'||:")
    assert _run2(w, m)[1]["stays-up"] == "ok" and _run2(w)[1]["stays-up"] == "FAIL"


# G5 PREP (council 21:35Z): the dirs under /data/work are NAME-keyed; run 2 only, so run 1 keeps 18 rows and run 2 has 20
OLDGATE = lambda w: w.gate(OLD, UID)      # noqa: E731


def test_MUTANT_a_left_gate_dir_of_the_old_name_is_red_and_named(w):
    OLDGATE(w)
    rc, st, out = _run2(w)
    assert st["name-dirs"] == "FAIL" and f"gate-{OLD}" in out.split("name-dirs:")[1], out


def test_MUTANT_a_media_dir_named_for_the_old_name_and_owned_by_the_agent_is_red(w):
    w.gate(OLD + "-media", UID, prefix="")
    _red(_run2(w), "name-dirs")


def test_MUTANT_the_reused_names_gate_dir_owned_by_the_previous_holder_is_red(w):
    w.gate(NEW, 981)                                             # G5's collision: gate-director-general-1 is the previous holder's
    _red(_run2(w), "name-dirs")


def test_MUTANT_a_missing_gate_dir_for_the_new_name_is_red(w):
    (w.tmp / "work" / f"gate-{NEW}").rmdir()
    _red(_run2(w), "name-dirs")


def test_dirs_of_other_names_or_other_owners_are_not_left_overs(w):
    w.gate(OLD, 981)                                             # the old name's dir owned by someone else is not the mover's
    w.gate(OLD + "x", 981, prefix="")
    w.gate("director-general-9", UID, prefix="")                 # another post's dir named differently
    assert _run2(w)[1]["name-dirs"] == "ok"


def test_the_name_dirs_row_has_a_world_only_each_of_its_guards_catches(w, tmp_path):
    w.gate(NEW, 981)
    m = _mutant(tmp_path, 'test "$gown" = "$UID_" -a -z "$left"', 'test -z "$left"')
    assert _run2(w, m)[1]["name-dirs"] == "ok" and _run2(w)[1]["name-dirs"] == "FAIL"
    w.gate(NEW, UID)
    OLDGATE(w)
    m = _mutant(tmp_path, 'test "$gown" = "$UID_" -a -z "$left"', 'test "$gown" = "$UID_"')
    assert _run2(w, m)[1]["name-dirs"] == "ok" and _run2(w)[1]["name-dirs"] == "FAIL"
