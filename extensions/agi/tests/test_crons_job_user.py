"""goal:g7.16.1.11.42 C1 -- a crons.md job may name the uid whose crontab carries it (`user:`), and crons.py apply is
the ONE home that installs it.

Fixture crontabs only: the applying user's file (--crontab-file) and a dir of <user>.crontab files
(--user-crontab-dir); the real `crontab` and `sudo` are never reached (the sudo row puts a FAKE sudo on PATH).
"""
from __future__ import annotations

import os
import stat
import sys
from pathlib import Path

import pytest
import yaml

sys.path.insert(0, str(Path(__file__).resolve().parent))
sys.path.insert(0, str(Path(__file__).resolve().parents[1] / "bin"))

import crons  # noqa: E402
from test_crons import GENERIC_ONLY, make_project, write_crons_node  # noqa: E402

ME = crons._invoking_user()
OTHER = "agi-someone"
CADENCES = {
    **GENERIC_ONLY,
    "board": {"schedule": "23 * * * *", "cmd": "echo board", "user": OTHER, "log": "/tmp/board.log"},
    "plain": {"schedule": "28 * * * *", "cmd": "echo plain"},
}


def _apply(root, tmp_path, **kw):
    own, users = tmp_path / "own.cron", tmp_path / "users"
    own.write_text("MAILTO=x\n0 1 * * * unrelated\n")
    got = crons.cmd_apply(root, own, user_crontab_dir=users, **kw)
    return got, own, users


def test_user_loads_and_a_bad_one_is_refused_by_name(tmp_path):
    root = make_project(tmp_path, cadences={**CADENCES})
    assert crons.load_crons_node(root)["jobs"]["board"]["user"] == OTHER
    root2 = make_project(tmp_path, name="p2", cadences={**GENERIC_ONLY, "x": {"schedule": "1 * * * *", "cmd": "true", "user": "Bad User"}})
    with pytest.raises(crons.CronsError, match=r"cadences\.x\.user must be a login name"):
        crons.load_crons_node(root2)


def test_a_built_in_job_may_not_name_a_user(tmp_path):
    root = make_project(tmp_path, cadences={"grid_sync": {"every_mins": 5, "enabled": True, "user": OTHER}})
    with pytest.raises(crons.CronsError, match=r"not allowed on a built-in job"):
        crons.load_crons_node(root)


def test_the_applying_users_block_has_no_foreign_job_and_the_foreign_block_only_its_own(tmp_path):
    root = make_project(tmp_path, cadences={**CADENCES})
    node = crons.load_crons_node(root)
    mine = crons.render_managed_lines(root, root, root, node)
    assert any("echo plain" in l for l in mine) and not any("echo board" in l for l in mine)
    theirs = crons.render_managed_lines(root, root, root, node, user=OTHER, only_bound=True)
    assert len(theirs) == 1 and "echo board" in theirs[0] and "echo plain" not in theirs[0]   # an unbound job is never duplicated
    assert ">> /tmp/board.log 2>&1" in theirs[0]


def test_apply_installs_the_foreign_block_beside_their_own_lines_and_is_idempotent(tmp_path):
    root = make_project(tmp_path, cadences={**CADENCES})
    users = tmp_path / "users"
    users.mkdir()
    (users / f"{OTHER}.crontab").write_text("# theirs\n5 5 * * * their-own-job\n")
    got, own, users = _apply(root, tmp_path)
    assert got["foreign_users"][OTHER]["status"] == "installed"
    text = (users / f"{OTHER}.crontab").read_text()
    assert "their-own-job" in text and "echo board" in text and "echo plain" not in text
    assert "0 1 * * * unrelated" in own.read_text() and "echo board" not in own.read_text()
    again = crons.cmd_apply(root, own, user_crontab_dir=users)
    assert again["foreign_users"][OTHER]["status"] == "unchanged" and again["changed"] is False
    assert (users / f"{OTHER}.crontab").read_text() == text                         # byte-identical


def test_the_kill_switch_empties_the_foreign_block_and_keeps_their_other_lines(tmp_path):
    root = make_project(tmp_path, cadences={**CADENCES})
    got, own, users = _apply(root, tmp_path)
    assert "echo board" in (users / f"{OTHER}.crontab").read_text()
    (users / f"{OTHER}.crontab").write_text("5 5 * * * their-own-job\n" + (users / f"{OTHER}.crontab").read_text())
    write_crons_node(root, False, {**CADENCES})                                       # the SAME project: the same marker hash
    off = crons.cmd_apply(root, own, user_crontab_dir=users)
    text = (users / f"{OTHER}.crontab").read_text()
    assert "echo board" not in text and "their-own-job" in text
    assert off["foreign_users"][OTHER]["status"] == "installed"


def test_without_privilege_a_foreign_user_is_pending_and_the_own_block_still_installs(tmp_path, monkeypatch):
    fake = tmp_path / "fakebin"
    fake.mkdir()
    sudo = fake / "sudo"
    sudo.write_text("#!/bin/sh\necho 'sudo: a password is required' >&2\nexit 1\n")
    sudo.chmod(sudo.stat().st_mode | stat.S_IXUSR)
    monkeypatch.setenv("PATH", f"{fake}:{os.environ['PATH']}")
    root = make_project(tmp_path, cadences={**CADENCES})
    own = tmp_path / "own.cron"
    got = crons.cmd_apply(root, own)                                                 # no user_crontab_dir: the sudo path
    st = got["foreign_users"][OTHER]
    assert st["status"].startswith("pending") and "apply --sudo" in st["status"] and st["changed"] is None
    assert "echo plain" in own.read_text()                                          # the cron-run apply is never failed by it


def test_the_live_board_rows_are_the_option_e_shape():
    node = yaml.safe_load(
        (Path(__file__).resolve().parents[3] / ".agi/nodes/.geometry/crons.md").read_text().split("---")[1])["cadences"]
    commit, land = node["graph_metrics"], node["graph_metrics_land"]
    assert commit["user"] == "agi-belam" and "board_job.py commit" in commit["cmd"] and "@WROOT@" in commit["cmd"]
    assert "metrics_cell.py @WROOT@" in commit["cmd"] and "--line {root}" in commit["cmd"]    # writes the clone, measures MAIN
    assert commit["log"].startswith("~/") and "/var/lib/agi/" not in commit["cmd"] + commit["log"]   # agi-belam's own home, never a literal one
    assert "user" not in land and "board_job.py land" in land["cmd"] and "commit" not in land["cmd"]


# ---- council 18:06Z condition (a): reconcile EVERY user ANY job names (sp's probe: RED at both shas before)
def _old_foreign_users(node, root, me):
    """The filter the first cut had: only the users of ENABLED, on-this-box jobs."""
    own = crons._this_box(root)
    return sorted({j["user"] for j in node["jobs"].values()
                   if j.get("user") and j["user"] != me and j["enabled"] and crons._on_this_box(j, own)})


def test_a_disabled_job_empties_its_users_block(tmp_path):
    root = make_project(tmp_path, cadences={**CADENCES})
    got, own, users = _apply(root, tmp_path)
    f = users / f"{OTHER}.crontab"
    assert "echo board" in f.read_text()
    write_crons_node(root, True, {**CADENCES, "board": {**CADENCES["board"], "enabled": False}})
    off = crons.cmd_apply(root, own, user_crontab_dir=users)
    assert off["foreign_users"][OTHER]["status"] == "installed" and "echo board" not in f.read_text()   # the line is gone, not live forever


def test_a_job_moved_to_another_box_empties_its_users_block(tmp_path):
    root = make_project(tmp_path, cadences={**CADENCES})
    got, own, users = _apply(root, tmp_path)
    write_crons_node(root, True, {**CADENCES, "board": {**CADENCES["board"], "box": "some-other-box"}})
    crons.cmd_apply(root, own, user_crontab_dir=users)
    assert "echo board" not in (users / f"{OTHER}.crontab").read_text()


def test_a_disabled_job_without_privilege_is_a_named_pending_not_a_silence(tmp_path, monkeypatch):
    fake = tmp_path / "fakebin"
    fake.mkdir()
    sudo = fake / "sudo"
    sudo.write_text("#!/bin/sh\necho 'sudo: a password is required' >&2\nexit 1\n")
    sudo.chmod(sudo.stat().st_mode | stat.S_IXUSR)
    monkeypatch.setenv("PATH", f"{fake}:{os.environ['PATH']}")
    root = make_project(tmp_path, cadences={**CADENCES, "board": {**CADENCES["board"], "enabled": False}})
    got = crons.cmd_apply(root, tmp_path / "own.cron")
    st = got["foreign_users"][OTHER]
    assert st["status"].startswith("pending") and "apply --sudo" in st["status"] and st["managed_lines"] == []


def test_mutant_the_enabled_filter_back_leaves_the_users_line_live(tmp_path, monkeypatch):
    root = make_project(tmp_path, cadences={**CADENCES})
    got, own, users = _apply(root, tmp_path)
    write_crons_node(root, True, {**CADENCES, "board": {**CADENCES["board"], "enabled": False}})
    monkeypatch.setattr(crons, "_foreign_users", _old_foreign_users)
    crons.cmd_apply(root, own, user_crontab_dir=users)
    assert "echo board" in (users / f"{OTHER}.crontab").read_text()      # RED: the real filter empties it (the first row above)


def test_the_rendered_board_line_writes_under_the_applying_users_own_home():
    """The RENDERED form (belam's landing guard 00:1xZ): `~` is a shell word in the cron line, so agi-belam's cron expands it to agi-belam's
    home; the redirect target and --work are tilde words, mkdir has the same, and no literal state-root path is rendered."""
    root = Path(__file__).resolve().parents[3]
    node = crons.load_crons_node(root / ".agi")
    (line,) = crons.render_managed_lines(root / ".agi", root, root, node, box_name="encryption-town", user="agi-belam", only_bound=True)
    assert line.endswith(">> ~/logs/board_job.log 2>&1") and "mkdir -p ~/logs &&" in line and " --work ~/board-work -- " in line
    assert "/var/lib/agi/" not in line.replace(str(root), "")
