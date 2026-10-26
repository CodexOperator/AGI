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


# ---- S1 vs the gate's basetemp (GATE274 council, 10-26): a fixture project sits under an agi-suite-* part of its OWN inside tmp_path
def test_the_crons_fixture_helpers_build_the_project_under_their_own_seam_part(tmp_path):
    import test_crons_apply_cell as ac
    for root in (make_project(tmp_path), ac.make_project(tmp_path, ac.fm_with(), name="repo2").parent):
        assert any(p.startswith("agi-suite-") for p in root.relative_to(tmp_path).parts), root


def test_mutant_a_root_built_at_tmp_path_directly_is_red_under_any_basetemp(tmp_path):
    from test_crons import assert_own_seam_part
    with pytest.raises(AssertionError):
        assert_own_seam_part(tmp_path, tmp_path)                                  # the root IS the base
    with pytest.raises(AssertionError):
        assert_own_seam_part(tmp_path / "proj", tmp_path)                         # no agi-suite-* part below the base
    assert_own_seam_part(tmp_path / "agi-suite-fixture" / "proj", tmp_path)


# ---- S1 refusal, as PATH STRINGS (no tmp_path: /tmp is itself a seam root, so a row built inside it would pass for the wrong reason)
def test_s1_a_project_outside_every_seam_shape_with_an_existing_fixture_dir_is_refused_naming_the_seam(tmp_path):
    d = tmp_path / "users"
    d.mkdir()
    why = crons._seam_refused(Path("/data/work/gate-x/bt/repo"), d)
    assert why and "honoured only for a throwaway project" in why, why
    assert crons._seam_path_ok(Path("/data/work/agi")) is False
    for good in ("/tmp/x", "/var/tmp/y", "/dev/shm/q", "/var/lib/agi/box/agi-suite-ab12/repo", "/data/work/pytest-of-x/pytest-3/repo0"):
        assert crons._seam_path_ok(Path(good)) is True, good


def test_mutant_a_predicate_that_always_says_yes_breaks_the_path_string_row(tmp_path):
    d = tmp_path / "users"
    d.mkdir()
    m = mutant(tmp_path, "def _seam_path_ok(repo_root: Path) -> bool:", "def _seam_path_ok(repo_root: Path) -> bool:\n    return True")
    assert m._seam_refused(Path("/data/work/gate-x/bt/repo"), d) is None, "the mutant lets the real-path project through (the row above would be RED)"
    assert m._seam_path_ok(Path("/data/work/agi")) is True


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
    m = mutant(tmp_path, "            why = None if allow_temp else _temp_project(repo_root)\n        if why:   # C-3 (3)", "            why = None\n        if why:   # C-3 (3)")
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
    (tmp_path / "users").mkdir()                                                   # S3: the dir must exist (a missing one reads as empty tables and is refused)
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


# ---- C-3 (3) on the other two `--user` doors (council all-is-one 01:34Z 10-26: the guard is in the goal's own title)
def _seeded(tmp_path, sudo_log):
    """a project whose managed block is already in the foreign table (installed through the allow_temp seam), and the call log cleared."""
    calls, state = sudo_log
    root, own = project(tmp_path)
    crons.cmd_apply(root, own, sudo=True, allow_temp=True)
    assert "echo board" in (state / OTHER).read_text()
    before = (state / OTHER).read_text()
    n = len(calls())
    return root, own, state, calls, before, n


def test_remove_user_from_a_temp_project_is_refused_before_any_sudo_call_and_the_table_is_untouched(tmp_path, sudo_log, capsys):
    root, own, state, calls, before, n = _seeded(tmp_path, sudo_log)
    with pytest.raises(crons.CronsError, match="refused: .*changed only for the real project"):
        crons.cmd_remove(root, user=OTHER)
    assert len(calls()) == n and (state / OTHER).read_text() == before            # not even the `-l` read
    assert crons.main(["remove", "--root", str(root), "--user", OTHER]) == 1
    assert "refused:" in capsys.readouterr().err and len(calls()) == n and (state / OTHER).read_text() == before


def test_marked_user_from_a_temp_project_is_refused_before_any_sudo_call(tmp_path, sudo_log, capsys):
    root, own, state, calls, before, n = _seeded(tmp_path, sudo_log)
    with pytest.raises(crons.CronsError, match="refused: .*read only for the real project"):
        crons.cmd_marked(root, user=OTHER)
    assert crons.main(["marked", "--root", str(root), "--user", OTHER]) == 1
    assert "refused:" in capsys.readouterr().err and len(calls()) == n


def test_remove_and_marked_user_still_work_through_a_fixture_dir_and_the_allow_temp_seam(tmp_path, sudo_log):
    root, own, state, calls, before, n = _seeded(tmp_path, sudo_log)
    assert crons.cmd_marked(root, user=OTHER, allow_temp=True) > 0 and len(calls()) > n       # positive control: the seam reaches sudo
    crons.cmd_remove(root, user=OTHER, allow_temp=True)
    assert "echo board" not in (state / OTHER).read_text()
    d = tmp_path / "users"; d.mkdir()
    crons.cmd_apply(root, own, user_crontab_dir=d)
    assert crons.cmd_marked(root, user=OTHER, user_crontab_dir=d) > 0                          # a fixture dir is the other seam, no allow_temp needed
    crons.cmd_remove(root, user=OTHER, user_crontab_dir=d)
    assert crons.cmd_marked(root, user=OTHER, user_crontab_dir=d) == 0


def test_mutant_without_the_guard_remove_user_from_a_temp_project_rewrites_the_real_table(tmp_path, sudo_log):
    root, own, state, calls, before, n = _seeded(tmp_path, sudo_log)
    m = mutant(tmp_path, '        _refuse_user_door(repo_root, user, user_crontab_dir, allow_temp, "changed")\n', "")
    m.cmd_remove(root, user=OTHER)
    assert len(calls()) > n and (state / OTHER).read_text() != before, "the mutant must reach and write the table (the row above would then be RED)"


def test_mutant_without_the_guard_marked_user_from_a_temp_project_reads_the_real_table(tmp_path, sudo_log):
    root, own, state, calls, before, n = _seeded(tmp_path, sudo_log)
    m = mutant(tmp_path, '        _refuse_user_door(repo_root, user, user_crontab_dir, allow_temp, "read")\n', "")
    m.cmd_marked(root, user=OTHER)
    assert len(calls()) > n, "the mutant must reach sudo (the row above would then be RED)"


# ---- S1-S3 (council 3/3 03:10Z 10-26, alive gen 20): ONE predicate for every --user-crontab-dir caller (apply, remove, marked), path facts only
REAL = Path("/srv/real-main")                                    # a project path no fact makes throwaway; locations.repo_root is pointed at it (nothing on disk needs to exist)


def _real_main(monkeypatch, where=REAL):
    monkeypatch.setattr(crons.locations, "repo_root", lambda root: Path(where))


def test_the_seam_predicate_is_path_facts_only_and_resolves_symlinks(tmp_path, monkeypatch):
    for ok in ("/tmp/x", "/var/tmp/y/z", "/dev/shm/q", "/data/work/agi-suite-ab12/repo", "/data/work/bt/pytest-of-u/pytest-3/repo0"):
        assert crons._seam_path_ok(Path(ok)), ok
    for bad in ("/data/work/agi", "/srv/real-main", "/opt/agi", "/data/work/pytest/x"):          # `pytest` alone is not a `pytest-*` part
        assert not crons._seam_path_ok(Path(bad)), bad
    monkeypatch.setenv("TMPDIR", "/srv"); monkeypatch.setenv("PYTEST_CURRENT_TEST", "x")             # the env that fails OPEN must not move it
    assert not crons._seam_path_ok(REAL)
    link = tmp_path / "link"; link.symlink_to(REAL)                                                  # a pytest-shaped STRING that is a real project underneath
    assert not crons._seam_path_ok(link)


def test_m1_a_fixture_dir_on_a_real_main_is_refused_before_any_read_or_write_on_all_three_doors(tmp_path, sudo_log, monkeypatch):
    calls, state = sudo_log
    d = tmp_path / "users"; d.mkdir()
    (d / f"{OTHER}.crontab").write_text("5 5 * * * theirs\n")
    _real_main(monkeypatch)
    with pytest.raises(crons.CronsError, match="refused: .*honoured only for a throwaway project"):
        crons.cmd_marked(REAL, user=OTHER, user_crontab_dir=d)
    with pytest.raises(crons.CronsError, match="refused: .*honoured only for a throwaway project"):
        crons.cmd_remove(REAL, user=OTHER, user_crontab_dir=d)
    assert crons._seam_refused(REAL, d)                                            # apply asks the same predicate (its row: m4's nonexistent dir, and the mutant below)
    assert (d / f"{OTHER}.crontab").read_text() == "5 5 * * * theirs\n" and calls() == []


def test_m2_the_inherited_env_does_not_lift_it(tmp_path, sudo_log, monkeypatch):
    calls, _ = sudo_log
    d = tmp_path / "users"; d.mkdir()
    _real_main(monkeypatch)
    monkeypatch.setenv("TMPDIR", str(REAL.parent)); monkeypatch.setenv("PYTEST_CURRENT_TEST", "x")
    with pytest.raises(crons.CronsError, match="refused:"):
        crons.cmd_marked(REAL, user=OTHER, user_crontab_dir=d)
    assert calls() == []


def test_m3_a_symlink_in_tmp_to_a_real_main_is_refused_by_the_real_path(tmp_path, sudo_log, monkeypatch):
    calls, _ = sudo_log
    d = tmp_path / "users"; d.mkdir()
    link = tmp_path / "pytest-looking"; link.symlink_to(REAL)
    _real_main(monkeypatch, link)
    with pytest.raises(crons.CronsError, match="refused:"):
        crons.cmd_marked(link, user=OTHER, user_crontab_dir=d)


def test_m4_a_fixture_dir_that_does_not_exist_is_refused_never_read_as_empty(tmp_path, sudo_log):
    root, own = project(tmp_path)
    nope = tmp_path / "no-such-dir"
    with pytest.raises(crons.CronsError, match="refused: .*does not exist"):
        crons.cmd_marked(root, user=OTHER, user_crontab_dir=nope)
    with pytest.raises(crons.CronsError, match="refused: .*does not exist"):
        crons.cmd_remove(root, user=OTHER, user_crontab_dir=nope)
    assert crons.cmd_apply(root, own, user_crontab_dir=nope)["foreign_users"][OTHER]["status"].startswith("refused:") and not nope.exists()
    d = tmp_path / "there"; d.mkdir()                                              # a missing <user>.crontab inside an EXISTING dir stays an empty table
    assert crons.cmd_marked(root, user=OTHER, user_crontab_dir=d) == 0


def test_m5_a_temp_project_with_its_dir_works_and_says_so_on_stderr(tmp_path, sudo_log, capsys):
    root, own = project(tmp_path)
    d = tmp_path / "users"; d.mkdir()
    crons.cmd_apply(root, own, user_crontab_dir=d)
    err = capsys.readouterr().err
    assert f"[crons] fixture crontab dir {d} (test seam)" in err, err
    assert crons.cmd_marked(root, user=OTHER, user_crontab_dir=d) > 0
    crons.cmd_remove(root, user=OTHER, user_crontab_dir=d)
    assert crons.cmd_marked(root, user=OTHER, user_crontab_dir=d) == 0
    assert capsys.readouterr().err.count("(test seam)") == 3          # marked, remove, marked


def test_mutants_of_the_seam_predicate_each_break_a_row_above(tmp_path, sudo_log, monkeypatch):
    calls, _ = sudo_log
    d = tmp_path / "users"; d.mkdir()
    orig = crons.locations.repo_root
    _real_main(monkeypatch)
    cases = [("if not _seam_path_ok(repo_root):", "if False:"),                                        # m1: the predicate dropped
             ('    for t in _SEAM_ROOTS:', '    if os.environ.get("PYTEST_CURRENT_TEST"):\n        return True\n    for t in _SEAM_ROOTS:')]   # m2: an env clause (fail OPEN)
    for old, new in cases:
        m = mutant(tmp_path, old, new)
        monkeypatch.setattr(m.locations, "repo_root", lambda root: REAL)
        monkeypatch.setenv("PYTEST_CURRENT_TEST", "x")
        assert m.cmd_marked(REAL, user=OTHER, user_crontab_dir=d) == 0, old                              # the mutant serves a real project from fixtures
    m = mutant(tmp_path, "p = Path(os.path.realpath(repo_root))", "p = Path(repo_root)")                   # m3: the string, not the real path
    link = tmp_path / "pytest-looking"; link.symlink_to(REAL)
    monkeypatch.setattr(m.locations, "repo_root", lambda root: link)
    assert m.cmd_marked(link, user=OTHER, user_crontab_dir=d) == 0
    m = mutant(tmp_path, "    if not d.is_dir():\n        return f\"the fixture crontab dir", "    if False:\n        return f\"the fixture crontab dir")      # m4
    root, own = project(tmp_path / "q")
    monkeypatch.setattr(m.locations, "repo_root", orig)
    assert m.cmd_marked(root, user=OTHER, user_crontab_dir=tmp_path / "no-such-dir") == 0
    m = mutant(tmp_path, "            why = _seam_refused(repo_root, user_crontab_dir)   # S1/S3", "            why = None   # S1/S3")        # apply no longer asks the predicate
    ap_root, ap_own = project(tmp_path / "ap")
    assert not m.cmd_apply(ap_root, ap_own, user_crontab_dir=tmp_path / "no-such-dir")["foreign_users"][OTHER]["status"].startswith("refused")   # the mutant installs into a dir it made up
    m = mutant(tmp_path, '    print(f"[crons] fixture crontab dir {d} (test seam)", file=sys.stderr)\n', "")      # m5: silent
    assert m.cmd_marked(root, user=OTHER, user_crontab_dir=d) == 0
