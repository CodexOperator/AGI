"""goal:g7.16.1.11.13 C-2 + C-3 (council 06:30-06:33Z 10-24): a throwaway project's managed block once reached agi-sanctuary-master's REAL crontab
(`sudo -n crontab -u U` from a plain apply; sudo resets PATH to secure_path, which finds the real /usr/bin/crontab).

C-2  a plain apply (no --sudo, no --user-crontab-dir) makes ZERO sudo calls, reads NO foreign table, and says `unread: run apply --sudo` per foreign user.
C-3  (1) the fixtures that run `crons.py apply` pass --user-crontab-dir and carry a logging FAKE sudo (test_crons_apply_cell.py, test_grid_gate.py);
     (3) on the real sudo path (--sudo, no fixture dir) a project under a temp dir / pytest basetemp / agi-suite-* is REFUSED, named, rc 1, nothing written.
A fake `sudo` first on PATH logs every call. MUTANTS are in-process copies of crons.py with one edit; each must break the row it names.
"""
from __future__ import annotations

import importlib.util
import os
import stat
import sys
from pathlib import Path

import pytest

sys.path.insert(0, str(Path(__file__).resolve().parent))
sys.path.insert(0, str(Path(__file__).resolve().parents[1] / "bin"))

import crons  # noqa: E402
from test_crons import GENERIC_ONLY, make_project  # noqa: E402

OTHER = "agi-someone"
CADENCES = {**GENERIC_ONLY,
            "board": {"schedule": "23 * * * *", "cmd": "echo board", "user": OTHER, "log": "/tmp/board.log"},
            "plain": {"schedule": "28 * * * *", "cmd": "echo plain"}}
SRC = Path(crons.__file__)

LOGGING_SUDO = """#!/bin/sh
echo "$@" >> $SUDO_LOG
[ "$1" = -n ] && shift
[ "$1" = crontab ] && shift
shift; u=$1; shift; f=$FAKE_CRON_DIR/$u
case $1 in
-l) [ -f $f ] && { cat $f; exit 0; }; echo "no crontab for $u" >&2; exit 1;;
-) cat > $f; exit 0;;
esac
exit 2
"""


@pytest.fixture
def sudo_log(tmp_path, monkeypatch):
    fake, state, log = tmp_path / "fakebin", tmp_path / "crontabs", tmp_path / "sudo.calls"
    fake.mkdir()
    state.mkdir()
    sudo = fake / "sudo"
    sudo.write_text(LOGGING_SUDO)
    sudo.chmod(sudo.stat().st_mode | stat.S_IXUSR)
    monkeypatch.setenv("PATH", f"{fake}:{os.environ['PATH']}")
    monkeypatch.setenv("SUDO_LOG", str(log))
    monkeypatch.setenv("FAKE_CRON_DIR", str(state))
    return lambda: (log.read_text().splitlines() if log.exists() else []), state


def mutant(tmp_path: Path, old: str, new: str):
    text = SRC.read_text()
    assert text.count(old) == 1, f"mutant anchor not unique: {old!r}"
    p = tmp_path / "crons_mutant.py"
    p.write_text(text.replace(old, new))
    spec = importlib.util.spec_from_file_location("crons_mutant", p)
    mod = importlib.util.module_from_spec(spec)
    spec.loader.exec_module(mod)
    return mod


def project(tmp_path):
    root = make_project(tmp_path, cadences={**CADENCES})
    own = tmp_path / "own.cron"
    own.write_text("")
    return root, own


# ---- C-2
def test_a_plain_apply_makes_zero_sudo_calls_and_says_unread(tmp_path, sudo_log):
    calls, _ = sudo_log
    root, own = project(tmp_path)
    got = crons.cmd_apply(root, own, allow_temp=True)
    st = got["foreign_users"][OTHER]
    assert calls() == [], calls()
    assert st["status"].startswith("unread: run apply --sudo") and st["changed"] is None
    assert "echo plain" in own.read_text()                                           # the own block still installs


def test_a_plain_apply_through_main_prints_unread_and_exits_0(tmp_path, sudo_log, capsys):
    calls, _ = sudo_log
    root, own = project(tmp_path)
    assert crons.main(["apply", "--root", str(root), "--crontab-file", str(own)]) == 0
    out = capsys.readouterr().out
    assert f"crons: user {OTHER}: unread: run apply --sudo" in out and calls() == []


def test_mutant_without_the_c2_branch_a_plain_apply_calls_sudo(tmp_path, sudo_log):
    calls, _ = sudo_log
    root, own = project(tmp_path)
    m = mutant(tmp_path, "if user_crontab_dir is None and not sudo:", "if False:")
    m.cmd_apply(root, own, allow_temp=True)
    assert calls(), "the mutant must reach sudo (the row above would then be RED)"


def test_mutant_an_unread_user_defaulting_to_ok_is_red(tmp_path, sudo_log):
    root, own = project(tmp_path)
    m = mutant(tmp_path, '"changed": None, "status": UNREAD}', '"changed": False, "status": "unchanged"}')
    st = m.cmd_apply(root, own, allow_temp=True)["foreign_users"][OTHER]
    assert not st["status"].startswith("unread"), "the mutant claims a reading that never happened"


def test_only_sudo_reads_and_writes_the_foreign_table(tmp_path, sudo_log):
    calls, state = sudo_log
    root, own = project(tmp_path)
    st = crons.cmd_apply(root, own, sudo=True, allow_temp=True)["foreign_users"][OTHER]
    assert st["status"] == "installed" and "echo board" in (state / OTHER).read_text()
    assert [c for c in calls() if " -l" in c] and [c for c in calls() if c.endswith(" -")]


# ---- C-3 (3): the real sudo path never serves a throwaway project
def test_a_temp_project_on_the_sudo_path_is_refused_nothing_written_and_rc_1(tmp_path, sudo_log, capsys):
    calls, state = sudo_log
    root, own = project(tmp_path)
    st = crons.cmd_apply(root, own, sudo=True)["foreign_users"][OTHER]       # tmp_path IS a pytest basetemp under /tmp
    assert st["status"].startswith("refused:") and st["changed"] is None
    assert calls() == [] and not (state / OTHER).exists()
    assert crons.main(["apply", "--root", str(root), "--crontab-file", str(own), "--sudo"]) == 1
    assert "refused:" in capsys.readouterr().out and calls() == []


def test_mutant_without_the_c3_guard_the_temp_project_reaches_the_foreign_table(tmp_path, sudo_log):
    calls, state = sudo_log
    root, own = project(tmp_path)
    m = mutant(tmp_path, "why = None if (user_crontab_dir is not None or allow_temp) else _temp_project(repo_root)", "why = None")
    st = m.cmd_apply(root, own, sudo=True)["foreign_users"][OTHER]
    assert st["status"] == "installed" and (state / OTHER).exists()          # RED for the real file's row above


def test_the_guard_names_temp_suite_and_pytest_paths_and_lets_the_real_project_through(monkeypatch):
    monkeypatch.delenv("PYTEST_CURRENT_TEST", raising=False)
    for bad in ("/tmp/x", "/var/tmp/y/z", "/dev/shm/q", "/var/lib/agi/box/agi-suite-ab12/repo", "/data/work/pytest-of-x/pytest-3/repo0"):
        assert crons._temp_project(Path(bad)), bad
    assert crons._temp_project(Path("/data/work/agi")) is None
    assert crons._temp_project(Path("/opt/agi")) is None


def test_a_fixture_dir_is_the_seam_and_needs_no_allow_temp(tmp_path, sudo_log):
    calls, _ = sudo_log
    root, own = project(tmp_path)
    got = crons.cmd_apply(root, own, user_crontab_dir=tmp_path / "users")
    assert got["foreign_users"][OTHER]["status"] == "installed" and calls() == []


# ---- belam's drift read (alive 06:35:19Z): `apply --sudo --dry-run` reads through sudo, reports, writes NOTHING
def test_sudo_dry_run_reads_only_and_says_would_install_for_a_drifted_table(tmp_path, sudo_log, capsys):
    calls, state = sudo_log
    root, own = project(tmp_path)
    (state / OTHER).write_text("5 5 * * * their-own-job\n")                                  # drifted: our block is absent
    got = crons.cmd_apply(root, own, sudo=True, dry_run=True, allow_temp=True)["foreign_users"][OTHER]
    assert got["status"] == "would install" and got["changed"] is True
    assert calls() and all(c.endswith(" -l") for c in calls()), calls()                       # reads only: no `crontab -u U -` write
    assert (state / OTHER).read_text() == "5 5 * * * their-own-job\n"
    crons.cmd_apply(root, own, sudo=True, allow_temp=True)                                    # now install it for real
    assert crons.cmd_apply(root, own, sudo=True, dry_run=True, allow_temp=True)["foreign_users"][OTHER]["status"] == "unchanged"


def test_mutant_dry_run_dropped_on_the_foreign_path_writes(tmp_path, sudo_log):
    calls, state = sudo_log
    root, own = project(tmp_path)
    m = mutant(tmp_path, "foreign[u] = reconcile_user_crontab(u, u_lines, begin, end, dry_run=dry_run,", "foreign[u] = reconcile_user_crontab(u, u_lines, begin, end, dry_run=False,")
    m.cmd_apply(root, own, sudo=True, dry_run=True, allow_temp=True)
    assert [c for c in calls() if c.endswith(" -")], "the mutant must write (the row above would then be RED)"
