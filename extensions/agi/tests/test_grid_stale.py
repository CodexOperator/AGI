"""goal:g7.16.1.11.20.4 (alive [decision] 08:20:17Z 10-31, 3/3): grid_stale, the grid staleness alarm in sanctuary-master's uid.

One row per council term, each with its mutant (an edit of grid_stale.py, or of the crons node, that the row must catch):
S1 threshold from the cell · S2 as amended by (Q) · S3 one id per episode, key = class + anchor (E) · S4 interval · S5 per-node read ·
(b) behind / ahead / in-flight (by time after the tip, B3; else by content) · (C) the grid's own mint class · (D) grid_sync off ·
(F) an underivable trunk or a read exception is a fault · (P) spool == the same uid's drain · F5 path-free · F8 read-only ·
the read-back line · `crons off`."""
from __future__ import annotations

import importlib.util
import os
import shutil
import stat
import subprocess
import sys
from pathlib import Path

import pytest
import yaml

BIN = Path(__file__).resolve().parents[1] / "bin"
SRC = BIN / "grid_stale.py"
CRONS = Path(__file__).resolve().parents[3] / ".agi" / "nodes" / ".geometry" / "crons.md"
sys.path.insert(0, str(BIN))

import grid_stale  # noqa: E402

T0 = 1_790_000_000
MINT_A, MINT_B = "a" * 32, "b" * 32


def _git(repo, *a, when=None, inp=None):
    env = {**os.environ, "GIT_AUTHOR_NAME": "t", "GIT_AUTHOR_EMAIL": "t@t", "GIT_COMMITTER_NAME": "t", "GIT_COMMITTER_EMAIL": "t@t"}
    if when is not None:
        env["GIT_AUTHOR_DATE"] = env["GIT_COMMITTER_DATE"] = f"@{when} +0000"
    r = subprocess.run(["git", "-C", str(repo), *a], capture_output=True, text=True, env=env, input=inp, check=True)
    return r.stdout.strip()


def _crons(every=30, live="true", on="true"):
    return f"---\ncadences:\n  grid_sync:\n    every_mins: {every}\n    enabled: {on}\ncrons_live: {live}\n---\nbody\n"


def _node(mint, text):
    return f"---\nid: doc:{mint[:4]}\nmint_id: {mint}\n---\n{text}\n"


class Repo:
    """A fixture trunk (refs/heads/main) and a grid namespace (refs/grid/node/<mint>), every commit at a fixed time."""

    def __init__(self, path, every=30, live="true", on="true"):
        self.p = path
        _git(path, "init", "-q", "-b", "main")
        self.write(T0, crons=_crons(every, live, on), A=_node(MINT_A, "a1"), B=_node(MINT_B, "b1"))

    def write(self, when, crons=None, **nodes):
        if crons is not None:
            (self.p / ".agi/nodes/.geometry").mkdir(parents=True, exist_ok=True)
            (self.p / ".agi/nodes/.geometry/crons.md").write_text(crons)
        for k, v in nodes.items():
            (self.p / ".agi/nodes/doc").mkdir(parents=True, exist_ok=True)
            (self.p / f".agi/nodes/doc/{k.lower()}.md").write_text(v)
        _git(self.p, "add", "-A")
        _git(self.p, "commit", "-q", "-m", f"trunk {when}", when=when)

    def version(self, when, mint, text, subject):
        blob = _git(self.p, "hash-object", "-w", "--stdin", inp=text)
        tree = _git(self.p, "mktree", inp=f"100644 blob {blob}\tnode.md\n")
        ref = f"refs/grid/node/{mint}"
        parent = subprocess.run(["git", "-C", str(self.p), "rev-parse", "-q", "--verify", ref], capture_output=True, text=True).stdout.strip()
        c = _git(self.p, "commit-tree", tree, *(["-p", parent] if parent else []), "-m", subject, when=when)
        _git(self.p, "update-ref", ref, c)
        return c


def _stale_town(tmp_path, every=30):
    """A recorded by grid_sync at T0+60 ('cron: v1'), then changed on the trunk at T0+120 and never re-versioned."""
    (tmp_path / "r").mkdir(parents=True)
    r = Repo(tmp_path / "r", every=every)
    r.version(T0 + 60, MINT_A, _node(MINT_A, "a1"), "cron: v1 doc:aaaa")
    r.version(T0 + 60, MINT_B, _node(MINT_B, "b1"), "cron: v1 doc:bbbb")
    r.write(T0 + 120, A=_node(MINT_A, "a2"))
    return r


def _mutant(tmp_path, old, new, name="gs_mut"):
    text = SRC.read_text()
    assert text.count(old) == 1, old
    d = tmp_path / "mut"
    d.mkdir(exist_ok=True)
    (d / f"{name}.py").write_text(text.replace(old, new))
    for f in ("alarm_spool.py", "geometry_config.py"):
        if (BIN / f).exists() and not (d / f).exists():
            (d / f).symlink_to(BIN / f)
    spec = importlib.util.spec_from_file_location(name, d / f"{name}.py")
    m = importlib.util.module_from_spec(spec)
    spec.loader.exec_module(m)
    return m


def _alarms(mod, repo, now):
    return mod.alarm(mod.read(repo.p, "refs/heads/main", now))


CHANGE = T0 + 120


# --- S1: the threshold is 2 x the grid_sync cell's every_mins, read at run time -----------------------------------------------

def test_s1_threshold_rows(tmp_path):
    r = _stale_town(tmp_path)
    assert _alarms(grid_stale, r, CHANGE + 2 * 30 * 60 - 60) is None                 # 2I - 1 min -> 0
    assert _alarms(grid_stale, r, CHANGE + 2 * 30 * 60 + 60) is not None             # 2I + 1 min -> exactly 1


def test_s1_a_changed_cell_moves_the_threshold_and_its_mutant(tmp_path):
    r = _stale_town(tmp_path, every=10)
    now = CHANGE + 25 * 60                                                           # 25 min: past 2 x 10, inside 2 x 30
    assert _alarms(grid_stale, r, now) is not None
    m = _mutant(tmp_path, "limit = 2 * every * 60", "limit = 2 * 30 * 60")
    assert _alarms(m, r, now) is None                                                # a literal threshold misses it: RED


# --- S5: the anchor is grid_sync's own newest 'cron: ' version, never any writer's -------------------------------------------

def test_s5_a_later_split_version_does_not_hide_the_stale_change_and_its_mutant(tmp_path):
    r = _stale_town(tmp_path)
    r.version(T0 + 200, MINT_B, _node(MINT_B, "b1"), "v2 doc:bbbb")                  # a split version on ANOTHER node, after the change
    now = CHANGE + 2 * 30 * 60 + 60
    al = _alarms(grid_stale, r, now)
    assert al is not None and "1 node(s)" in al[1]
    m = _mutant(tmp_path, "        if b in held:\n",                                # a SHARED window opened at any writer's newest version
                "        if b in held or int(git(repo, 'log', '-1', '--format=%ct', t, '--', p).stdout) <= max(c for _, c in tips.values()):\n")
    assert _alarms(m, r, now) is None                                                # it reads FRESH: RED


def test_s5_a_grid_sync_run_that_versions_other_nodes_after_the_change_does_not_hide_it(tmp_path):
    r = _stale_town(tmp_path)
    r.version(T0 + 300, MINT_B, _node(MINT_B, "b1"), "cron: v2 doc:bbbb")            # grid_sync ran AFTER the change; A not recorded
    al = _alarms(grid_stale, r, CHANGE + 2 * 30 * 60 + 60)
    assert al is not None and "1 node(s)" in al[1]


# --- (b) behind / ahead / in-flight: by time where the trunk changed after the tip (B3), else by content (sp) -------------------

LATE = CHANGE + 2 * 30 * 60 + 60


def test_b_ahead_a_grid_blob_the_trunk_never_had_is_counted_never_an_alarm_and_its_mutant(tmp_path):
    r = _stale_town(tmp_path)
    r.version(T0 + 300, MINT_A, _node(MINT_A, "a3-on-disk"), "cron: v2 doc:aaaa")     # grid_sync versioned MAIN's disk before the trunk
    rd = grid_stale.read(r.p, "refs/heads/main", LATE)
    assert rd["differ"] == 1 and rd["ahead"] == 1 and rd["stale"] == [] and grid_stale.alarm(rd) is None
    m = _mutant(tmp_path, "    return None                                                     # AHEAD\n",
                "    return changes[0][0] if changes else None                       # the first cut's fallback\n")
    assert m.alarm(m.read(r.p, "refs/heads/main", LATE)) is not None                 # a 'stale' with a trunk age: RED


def test_b_behind_a_late_version_of_an_older_trunk_blob_is_stale_and_its_mutant(tmp_path):
    r = _stale_town(tmp_path)
    r.version(T0 + 300, MINT_A, _node(MINT_A, "a1"), "cron: v2 doc:aaaa")            # a late writer records the OLDER trunk blob
    rd = grid_stale.read(r.p, "refs/heads/main", LATE)
    assert rd["ahead"] == 0 and len(rd["stale"]) == 1                                # dated from the trunk change after a1 (T0+120)
    m = _mutant(tmp_path, "            return min(c for c, _ in changes[:i]) if i else None    # BEHIND",
                "            return None                                             # (i) by time")
    assert m.alarm(m.read(r.p, "refs/heads/main", LATE)) is None                     # BEHIND silenced: RED


def test_b_in_flight_a_version_never_on_the_trunk_then_a_trunk_change_is_stale_and_its_mutant(tmp_path):
    (tmp_path / "r").mkdir()
    r = Repo(tmp_path / "r")
    r.version(T0 + 60, MINT_B, _node(MINT_B, "b1"), "cron: v1 doc:bbbb")
    r.version(T0 + 100, MINT_A, _node(MINT_A, "a-in-flight"), "v2 doc:aaaa")         # a post's in-flight edit, never on the trunk
    r.write(T0 + 120, A=_node(MINT_A, "a2"))                                         # the trunk lands a DIFFERENT A
    rd = grid_stale.read(r.p, "refs/heads/main", LATE)
    assert rd["ahead"] == 0 and len(rd["stale"]) == 1
    m = _mutant(tmp_path, "    if after:\n        return min(after)", "    if False:\n        return min(after)")
    assert m.alarm(m.read(r.p, "refs/heads/main", LATE)) is None                     # the content read unconditional: silent: RED


# --- (C) the grid's own mint class; unminted counted ---------------------------------------------------------------------------

HEX_ONLY = r'''MINT = re.compile(r"^mint_id:\s*['\"]?([0-9a-f]{8,64})['\"]?\s*$", re.M)'''


def test_c_the_mint_regex_is_the_grids_own():
    import grid
    assert grid_stale.MINT.pattern == grid.MINT_ID_RE.pattern and grid_stale.MINT.flags == grid.MINT_ID_RE.flags


def test_c_a_non_hex_mint_changed_and_not_re_versioned_alarms_and_its_mutant(tmp_path):
    (tmp_path / "r").mkdir()
    r = Repo(tmp_path / "r")
    r.write(T0 + 10, X=_node("TBD", "x1"))                                           # a live experiment node carries mint_id: TBD
    r.version(T0 + 60, MINT_A, _node(MINT_A, "a1"), "cron: v1 doc:aaaa")
    r.version(T0 + 60, MINT_B, _node(MINT_B, "b1"), "cron: v1 doc:bbbb")
    r.version(T0 + 60, "TBD", _node("TBD", "x1"), "cron: v1 doc:x")
    r.write(T0 + 120, X=_node("TBD", "x2"))
    rd = grid_stale.read(r.p, "refs/heads/main", LATE)
    assert rd["unminted"] == 1 and [m for m, _ in rd["stale"]] == ["TBD"]           # crons.md has no mint line: counted, not silent
    line = next(ln for ln in SRC.read_text().splitlines() if ln.startswith("MINT = re.compile("))
    m = _mutant(tmp_path, line, HEX_ONLY)
    assert m.alarm(m.read(r.p, "refs/heads/main", LATE)) is None                     # the first cut's hex-only class skips it: RED


# --- S2 as amended by (Q): print what was READ; a read that cannot be made is the alarm; 0 compared is healthy ----------------

def test_q_healthy_quiet_town_compares_0_and_alarms_none(tmp_path, capsys):
    r = _stale_town(tmp_path)
    r.version(T0 + 180, MINT_A, _node(MINT_A, "a2"), "cron: v2 doc:aaaa")            # grid_sync recorded the change
    rc = grid_stale.main(["run", "--repo", str(r.p), "--trunk", "refs/heads/main", "--to", "belam", "--max-lines", "9",
                          "--spool", str(tmp_path / "sp"), "--now", str(T0 + 99_999)])
    out = capsys.readouterr().out
    assert rc == 0 and "differ=0" in out and "ahead=0" in out and "unminted=1" in out and "compared=3" in out and "refs=2" in out and "newest_grid_sync=" in out and "trunk=" in out
    assert not (tmp_path / "sp").exists()


def test_q_a_change_the_grid_already_holds_through_a_split_version_is_fresh(tmp_path):
    r = _stale_town(tmp_path)
    r.version(T0 + 180, MINT_A, _node(MINT_A, "a2"), "v2 doc:aaaa")                  # recorded, but not by grid_sync
    rd = grid_stale.read(r.p, "refs/heads/main", T0 + 99_999)
    assert rd["differ"] == 0 and rd["stale"] == [] and grid_stale.alarm(rd) is None


@pytest.mark.parametrize("case,fault,mutant", [
    ("empty", "0 grid node refs", ('out["fault"] = "0 grid node refs"', "pass")),
    ("no-cron", "no grid_sync version", ('out["fault"] = "no grid_sync version"', "pass")),
    ("trunk", "trunk unresolved", ('out["fault"] = "trunk unresolved"', "pass")),
    ("cell", "grid_sync cell unread", ('out["fault"] = "grid_sync cell unread"', "pass")),
])
def test_s2_an_unreadable_grid_is_the_alarm_never_a_silent_pass(tmp_path, case, fault, mutant):
    (tmp_path / "r").mkdir()
    r = Repo(tmp_path / "r", every='"x"' if case == "cell" else 30)
    if case == "no-cron":
        r.version(T0 + 60, MINT_A, _node(MINT_A, "a1"), "v1 doc:aaaa")
    elif case in ("trunk", "cell"):
        r.version(T0 + 60, MINT_A, _node(MINT_A, "a1"), "cron: v1 doc:aaaa")
    trunk = "refs/heads/nope" if case == "trunk" else "refs/heads/main"
    al = grid_stale.alarm(grid_stale.read(r.p, trunk, T0 + 99_999))
    assert al is not None and fault in al[1]
    m = _mutant(tmp_path, *mutant)
    assert m.alarm(m.read(r.p, trunk, T0 + 99_999)) is None                          # the fault dropped: a silent pass: RED


# --- S3: one alarm per episode --------------------------------------------------------------------------------------------------

def test_s3_same_episode_same_id_new_anchor_new_id_and_its_mutant(tmp_path):
    r = _stale_town(tmp_path)
    now = CHANGE + 2 * 30 * 60 + 60
    m = _mutant(tmp_path, '        key = f"stale|{asha}"', '        key = "stale"')
    first, again, m_first = _alarms(grid_stale, r, now), _alarms(grid_stale, r, now + 600), _alarms(m, r, now)
    assert first[0] == again[0] and first[0].startswith("gs-")
    r.version(T0 + 300, MINT_B, _node(MINT_B, "b1"), "cron: v2 doc:bbbb")            # grid_sync ran again; A is still stale
    later = _alarms(grid_stale, r, now + 600)
    assert later is not None and later[0] != first[0]
    assert _alarms(m, r, now + 600)[0] == m_first[0]                                  # an id blind to the anchor never re-alarms: RED


def test_e_a_stale_set_that_grows_under_one_anchor_keeps_one_id_and_its_mutant(tmp_path):
    r = _stale_town(tmp_path)
    m = _mutant(tmp_path, '        key = f"stale|{asha}"', '        key = "|".join(sorted(m for m, _ in r["stale"])) + f"|{asha}"')
    first, m_first = _alarms(grid_stale, r, LATE), _alarms(m, r, LATE)
    r.write(T0 + 200, B=_node(MINT_B, "b2"))                                         # the next board, grid_sync still dead
    later = LATE + 2 * 30 * 60
    grown, m_grown = _alarms(grid_stale, r, later), _alarms(m, r, later)
    assert "2 node(s)" in grown[1] and grown[0] == first[0]                          # one episode, one mail to belam
    assert m_grown[0] != m_first[0]                                                  # the set in the key: a 2nd mail: RED


# --- F5: path-free by construction -----------------------------------------------------------------------------------------------

def test_f5_the_alarm_text_carries_no_path_and_its_mutant(tmp_path):
    r = _stale_town(tmp_path)
    now = CHANGE + 2 * 30 * 60 + 60
    for mod_text in (_alarms(grid_stale, r, now)[1],
                     grid_stale.alarm(grid_stale.read(r.p, "refs/heads/nope", now))[1]):
        assert "/" not in mod_text and str(tmp_path) not in mod_text
    m = _mutant(tmp_path, '"trunk": t[:10] if t else "UNRESOLVED"', '"trunk": (str(repo) + ":" + t[:10]) if t else "UNRESOLVED"')
    assert "/" in _alarms(m, r, now)[1]                                              # a leaked root is caught: RED


# --- the read-back names uid + spool path (stdout only); F8 read-only on MAIN ----------------------------------------------------

def _snapshot(git_dir):
    return sorted((str(p.relative_to(git_dir)), p.stat().st_size, p.stat().st_mtime_ns) for p in git_dir.rglob("*") if p.is_file())


def _run(script, repo, spool, now):
    return subprocess.run([sys.executable, str(script), "run", "--repo", str(repo), "--trunk", "refs/heads/main", "--to", "belam",
                           "--max-lines", "9", "--spool", str(spool), "--now", str(now)], capture_output=True, text=True)


def test_f8_runs_on_a_read_only_git_and_reads_back_uid_and_spool(tmp_path):
    import pwd
    r = _stale_town(tmp_path)
    git_dir = r.p / ".git"
    modes = {p: p.stat().st_mode for p in [git_dir, *git_dir.rglob("*")]}
    try:
        for p in modes:
            p.chmod(modes[p] & ~(stat.S_IWUSR | stat.S_IWGRP | stat.S_IWOTH))
        p = _run(SRC, r.p, tmp_path / "sp", CHANGE + 2 * 30 * 60 + 60)
    finally:
        for p_, m in sorted(modes.items(), key=lambda kv: len(kv[0].parts)):
            p_.chmod(m)
    assert p.returncode == 0, p.stderr
    assert "differ=1" in p.stdout and "stale=1" in p.stdout
    assert f"as uid {pwd.getpwuid(os.getuid()).pw_name}" in p.stdout and str(tmp_path / "sp") in p.stdout
    line = (tmp_path / "sp").read_text()
    assert '"job":"grid_stale"' in line and '"to":"belam"' in line and str(tmp_path) not in line


def test_f8_a_run_leaves_the_git_dir_byte_for_byte_and_a_writing_mutant_is_red(tmp_path):
    r = _stale_town(tmp_path)
    git_dir = r.p / ".git"
    before = _snapshot(git_dir)
    assert _run(SRC, r.p, tmp_path / "sp", CHANGE + 4000).returncode == 0
    assert _snapshot(git_dir) == before
    m = tmp_path / "mut"
    m.mkdir()
    (m / "grid_stale.py").write_text(SRC.read_text().replace(
        '    t = rev(repo, trunk)\n', '    t = rev(repo, trunk)\n    git(repo, "update-ref", "refs/x", t)\n', 1))
    (m / "alarm_spool.py").symlink_to(BIN / "alarm_spool.py")
    assert _run(m / "grid_stale.py", r.p, tmp_path / "sp2", CHANGE + 4000).returncode == 0
    assert _snapshot(git_dir) != before                                              # a write in MAIN is seen: RED


# --- crons off: a kill-switch edit reads as a named state, never as a stale grid ------------------------------------------------

def test_crons_off_prints_and_appends_nothing_and_its_mutant(tmp_path, capsys):
    r = _stale_town(tmp_path)
    r.write(T0 + 130, crons=_crons(live="false"))
    rc = grid_stale.main(["run", "--repo", str(r.p), "--trunk", "refs/heads/main", "--to", "belam", "--max-lines", "9",
                          "--spool", str(tmp_path / "sp"), "--now", str(T0 + 99_999)])
    assert rc == 0 and "crons off" in capsys.readouterr().out and not (tmp_path / "sp").exists()
    m = _mutant(tmp_path, '    if live is False:\n        out["off"] = "crons off"\n        return out\n', "")
    assert m.alarm(m.read(r.p, "refs/heads/main", T0 + 99_999)) is not None          # the switch read as a fault: RED


# --- (D) grid_sync off: a decided switch, a named LIMIT --------------------------------------------------------------------------

def test_d_grid_sync_off_prints_and_appends_nothing_and_its_mutant(tmp_path, capsys):
    r = _stale_town(tmp_path)
    r.write(T0 + 130, crons=_crons(on="false"))
    rc = grid_stale.main(["run", "--repo", str(r.p), "--trunk", "refs/heads/main", "--to", "belam", "--max-lines", "9",
                          "--spool", str(tmp_path / "sp"), "--now", str(T0 + 99_999)])
    assert rc == 0 and "grid_sync off" in capsys.readouterr().out and not (tmp_path / "sp").exists()
    m = _mutant(tmp_path, '    if on is False:\n        out["off"] = "grid_sync off"\n        return out\n', "")
    assert m.alarm(m.read(r.p, "refs/heads/main", T0 + 99_999)) is not None          # the decided switch read as a fault: RED


# --- (F) a trunk the ladder cannot derive, or any read exception, is a fault -----------------------------------------------------

def test_f_no_ladder_and_no_trunk_is_the_unresolved_alarm_and_its_mutant(tmp_path, monkeypatch):
    r = _stale_town(tmp_path)
    monkeypatch.setattr(grid_stale, "default_trunk", lambda: sys.exit("prereq_notice: the ladder node has no current_season: pass --trunk"))
    rc = grid_stale.main(["run", "--repo", str(r.p), "--to", "belam", "--max-lines", "9", "--spool", str(tmp_path / "sp"), "--now", "1"])
    assert rc == 0 and "trunk unresolved" in (tmp_path / "sp").read_text()
    m = _mutant(tmp_path, "        except (SystemExit, Exception):  # noqa: BLE001", "        except ZeroDivisionError:  # noqa: BLE001")
    m.default_trunk = grid_stale.default_trunk                                       # the same failing ladder
    with pytest.raises(SystemExit):                                                  # the bare call: the 10-29 silence: RED
        m.read_safe(r.p, None, 1)


def _failing(mod, monkeypatch, *argv):
    """the one git read whose argv starts with `argv` fails as a lost object does (rc 128, empty stdout); every other read is real"""
    real = mod.git
    monkeypatch.setattr(mod, "git", lambda repo, *a, **k: subprocess.CompletedProcess(a, 128, "", "fatal") if a[:len(argv)] == argv else real(repo, *a, **k))


def _no_rc_check(tmp_path):
    return _mutant(tmp_path, "    if r.returncode:\n        raise RuntimeError(f\"git {a[0]} unread\")\n", "", name="gs_norc")


def test_g1_an_unread_path_history_is_a_fault_never_ahead_and_its_mutant(tmp_path, monkeypatch):
    r = _stale_town(tmp_path)
    _failing(grid_stale, monkeypatch, "log", "--first-parent", "--follow")
    al = grid_stale.alarm(grid_stale.read_safe(r.p, "refs/heads/main", LATE))
    assert al is not None and "read error RuntimeError" in al[1]
    m = _mutant(tmp_path, '    if not changes:\n        raise RuntimeError("path history empty")', "")
    text = (tmp_path / "mut" / "gs_mut.py").read_text()                             # the re-cut 2/3 shape: neither check
    rc_check = "    if r.returncode:\n        raise RuntimeError(f\"git {a[0]} unread\")\n"
    assert text.count(rc_check) == 1
    (tmp_path / "mut" / "gs_mut2.py").write_text(text.replace(rc_check, ""))
    spec = importlib.util.spec_from_file_location("gs_mut2", tmp_path / "mut" / "gs_mut2.py")
    m = importlib.util.module_from_spec(spec)
    spec.loader.exec_module(m)
    _failing(m, monkeypatch, "log", "--first-parent", "--follow")
    rd = m.read_safe(r.p, "refs/heads/main", LATE)
    assert rd["fault"] is None and rd["ahead"] == 1 and m.alarm(rd) is None          # read as AHEAD, silent: RED


@pytest.mark.parametrize("argv,benign", [(("cat-file", "blob"), "unminted"), (("ls-tree", "-r"), "compared")])
def test_g2_g3_an_unread_blob_or_tree_is_a_fault_and_its_mutant(tmp_path, monkeypatch, argv, benign):
    r = _stale_town(tmp_path)
    _failing(grid_stale, monkeypatch, *argv)
    al = grid_stale.alarm(grid_stale.read_safe(r.p, "refs/heads/main", LATE))
    assert al is not None and "read error RuntimeError" in al[1]
    m = _no_rc_check(tmp_path)
    _failing(m, monkeypatch, *argv)
    rd = m.read_safe(r.p, "refs/heads/main", LATE)
    assert rd["fault"] is None and m.alarm(rd) is None                               # read as '{benign}', silent: RED


def test_f_any_exception_in_the_read_is_a_fault_naming_its_class_only(tmp_path, monkeypatch):
    r = _stale_town(tmp_path)
    monkeypatch.setattr(grid_stale, "read", lambda *a: (_ for _ in ()).throw(RuntimeError("/a/secret/path")))
    al = grid_stale.alarm(grid_stale.read_safe(r.p, "refs/heads/main", 1))
    assert "read error RuntimeError" in al[1] and "/" not in al[1]


# --- (P) and S4 on the LIVE crons node ------------------------------------------------------------------------------------------

def _cadences(text):
    return yaml.safe_load(text.split("---")[1])["cadences"]


def p_ok(cad):
    """(P): grid_stale appends to its uid's DEFAULT spool (no --spool), and a drain row of the SAME uid drains that seat's default spool."""
    gs = cad["grid_stale"]
    drains = [j for j in cad.values() if isinstance(j, dict) and "alarm_spool.py drain" in str(j.get("cmd", ""))
              and "--spool" not in j["cmd"] and j.get("enabled") is True]
    return "--spool" not in gs["cmd"] and any(d.get("user") == gs.get("user") for d in drains)


def s4_ok(cad):
    return cad["grid_stale"]["every_mins"] >= cad["grid_sync"]["every_mins"]


def test_p_the_spool_appended_to_is_the_spool_a_drain_of_the_same_uid_reads_and_its_mutant():
    cad = _cadences(CRONS.read_text())
    assert cad["grid_stale"]["user"] == "agi-sanctuary-master" and p_ok(cad)
    bad = {**cad, "grid_stale": {**cad["grid_stale"], "user": "agi-belam-not-drained"}}
    assert not p_ok(bad)
    bad = {**cad, "grid_stale": {**cad["grid_stale"], "cmd": cad["grid_stale"]["cmd"] + " --spool /elsewhere"}}
    assert not p_ok(bad)


def test_s4_the_interval_is_no_shorter_than_grid_syncs_and_its_mutant():
    cad = _cadences(CRONS.read_text())
    assert s4_ok(cad) and "--to belam" in cad["grid_stale"]["cmd"]
    assert not s4_ok({**cad, "grid_stale": {**cad["grid_stale"], "every_mins": cad["grid_sync"]["every_mins"] - 1}})
