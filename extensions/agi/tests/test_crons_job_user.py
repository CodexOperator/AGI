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
    users.mkdir(exist_ok=True)                                                       # S3: a fixture dir that does not exist is refused
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
    job = [l for l in theirs if "echo board" in l]
    assert len(job) == 1 and not any("echo plain" in l for l in theirs)                   # an unbound job is never duplicated
    assert ">> /tmp/board.log 2>&1" in job[0]
    assert len(theirs) == 2 and " caps --root " in theirs[1]                                 # the block's ONE cap line, below


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


def test_a_plain_apply_leaves_a_foreign_user_unread_and_the_own_block_still_installs(tmp_path, monkeypatch):
    fake = tmp_path / "fakebin"
    fake.mkdir()
    sudo = fake / "sudo"
    sudo.write_text("#!/bin/sh\necho 'sudo: a password is required' >&2\nexit 1\n")
    sudo.chmod(sudo.stat().st_mode | stat.S_IXUSR)
    monkeypatch.setenv("PATH", f"{fake}:{os.environ['PATH']}")
    root = make_project(tmp_path, cadences={**CADENCES})
    own = tmp_path / "own.cron"
    got = crons.cmd_apply(root, own)                                                 # no user_crontab_dir, no --sudo: the foreign table is NOT read (C-2)
    st = got["foreign_users"][OTHER]
    assert st["status"].startswith("unread: run apply --sudo") and st["changed"] is None
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


def test_a_disabled_job_on_a_plain_apply_is_a_named_unread_not_a_silence(tmp_path, monkeypatch):
    fake = tmp_path / "fakebin"
    fake.mkdir()
    sudo = fake / "sudo"
    sudo.write_text("#!/bin/sh\necho 'sudo: a password is required' >&2\nexit 1\n")
    sudo.chmod(sudo.stat().st_mode | stat.S_IXUSR)
    monkeypatch.setenv("PATH", f"{fake}:{os.environ['PATH']}")
    root = make_project(tmp_path, cadences={**CADENCES, "board": {**CADENCES["board"], "enabled": False}})
    got = crons.cmd_apply(root, tmp_path / "own.cron")
    st = got["foreign_users"][OTHER]
    assert st["status"].startswith("unread: run apply --sudo") and st["managed_lines"] == []


def test_mutant_the_enabled_filter_back_leaves_the_users_line_live(tmp_path, monkeypatch):
    root = make_project(tmp_path, cadences={**CADENCES})
    got, own, users = _apply(root, tmp_path)
    write_crons_node(root, True, {**CADENCES, "board": {**CADENCES["board"], "enabled": False}})
    monkeypatch.setattr(crons, "_foreign_users", _old_foreign_users)
    crons.cmd_apply(root, own, user_crontab_dir=users)
    assert "echo board" in (users / f"{OTHER}.crontab").read_text()      # RED: the real filter empties it (the first row above)


LIVE_CRONS = Path(__file__).resolve().parents[3] / ".agi/nodes/.geometry/crons.md"


def _belam_lines(project, node_root):
    """Every line the crontab of agi-belam would carry, rendered as `crons.py apply --sudo` renders it."""
    return crons.render_managed_lines(node_root, project, project, crons.load_crons_node(node_root),
                                      box_name="encryption-town", user="agi-belam", only_bound=True)


@pytest.mark.parametrize("extra", [False, True], ids=["live-node", "live-node-plus-more-agi-belam-rows"])
def test_the_rendered_board_line_writes_under_the_applying_users_own_home(tmp_path, monkeypatch, extra):
    """The RENDERED form (belam's landing guard 00:1xZ): `~` is a shell word in the cron line, so agi-belam's cron expands it to agi-belam's
    home. The board line is selected BY CONTENT (the stack adds agi-belam rows: alarm_drain_belam, a user@ alarm row), exactly one carries
    `board_job.py commit`, and NO rendered agi-belam line, whichever job it is, carries a state-root path."""
    monkeypatch.setenv("HOME", str(tmp_path / "renderer-home"))                # the uid running crons.py: its home must appear in NO agi-belam line
    monkeypatch.setattr(crons, "_invoking_user", lambda: "agi-test-runner")    # a FIXTURE runner: agi-belam's block is FOREIGN whoever runs the suite (when the runner IS agi-belam it is the OWN block: no mkdir, no cap line)
    live = yaml.safe_load(LIVE_CRONS.read_text().split("---")[1])["cadences"]
    if extra:
        more = {"alarm_drain_x": {"schedule": "*/5 * * * *", "cmd": "echo drain", "user": "agi-belam", "box": "encryption-town"},
                "alarm_user_y": {"schedule": "1 * * * *", "cmd": "echo y", "user": "agi-belam", "box": "encryption-town", "log": "~/logs/y.log"}}
        proj = make_project(tmp_path, cadences={**live, **more})
        lines = _belam_lines(proj, proj)
        assert len(lines) >= 3                                                  # the row is not alone: this is what the first cut could not take
    else:
        proj = Path(__file__).resolve().parents[3]
        lines = _belam_lines(proj, proj / ".agi")
    board = [l for l in lines if "board_job.py commit" in l]
    assert len(board) == 1
    line = board[0]
    assert line.endswith(">> ~/logs/board_job.log 2>&1") and "mkdir -p ~/logs &&" in line and " --work ~/board-work -- " in line
    for l in lines:
        assert "/var/lib/agi/" not in l.replace(str(proj), "") and str(tmp_path / "renderer-home") not in l, l


def test_a_foreign_users_default_log_is_a_tilde_word_not_the_renderers_home(tmp_path, monkeypatch):
    """SM 00:21Z: the default log (and {logs}) was the home of the uid RUNNING crons.py, so a user-bound row without a log: cell redirected into
    the APPLYING uid's ~/logs, where the row's own uid cannot write: the redirect fails and the job never runs. A FOREIGN row now gets
    `~/logs/agi-crons-...` (expanded by that user's own cron); the own-user path is unchanged."""
    renderer_home = tmp_path / "renderer-home"
    monkeypatch.setenv("HOME", str(renderer_home))
    root = make_project(tmp_path, cadences={**GENERIC_ONLY,
        "drain": {"schedule": "1 * * * *", "cmd": "echo drain {logs}/x", "user": OTHER},
        "mine": {"schedule": "2 * * * *", "cmd": "echo mine {logs}/x", "user": ME},
        "plain": {"schedule": "3 * * * *", "cmd": "echo plain {logs}/x"}})
    node = crons.load_crons_node(root)
    (theirs,) = [l for l in crons.render_managed_lines(root, root, root, node, user=OTHER, only_bound=True) if "echo drain" in l]
    assert f">> ~/logs/{crons._log_path(root).name} 2>&1" in theirs and "echo drain ~/logs/x" in theirs     # default log AND {logs}
    assert str(renderer_home) not in theirs
    mine = crons.render_managed_lines(root, root, root, node)
    for job in ("echo mine", "echo plain"):                                                              # own-user: today's behaviour, byte for byte
        (l,) = [x for x in mine if job in x]
        assert f"{job} {renderer_home}/logs/x" in l and f">> {crons._log_path(root)} 2>&1" in l and "~/logs" not in l


# ---- the council's two ordered fix-forwards (00:28Z): the CAP of a foreign user's logs, and the MKDIR of its ~/logs

import json
import subprocess


def _foreign_project(tmp_path, monkeypatch, cap_mb=1):
    """A project whose node binds two jobs to OTHER (one with the default log, one with a custom ~/logs/ name), a 1 MB cap, and HOME redirected."""
    home = tmp_path / "otherhome"
    home.mkdir()
    monkeypatch.setenv("HOME", str(home))
    root = make_project(tmp_path, cadences={**GENERIC_ONLY,
        "drain": {"schedule": "1 * * * *", "cmd": "echo drain-ran", "user": OTHER},
        "board": {"schedule": "2 * * * *", "cmd": "echo board-ran", "user": OTHER, "log": "~/logs/board.log"}})
    (root / "agi-tree.config.json").write_text(json.dumps({"logs": {"cap_mb": cap_mb, "rotations": 2, "mode": "copytruncate"}}))
    node = crons.load_crons_node(root)
    engine = Path(__file__).resolve().parents[3]                                       # the real crons.py the cap line runs
    lines = crons.render_managed_lines(root, root, engine, node, user=OTHER, only_bound=True)
    return root, home, lines


def _run(line, home):
    """Run a rendered cron line the way cron does: the 5 schedule fields dropped, /bin/sh, HOME = the row's user's home, a bare env."""
    cmd = line.split(" ", 5)[5]
    return subprocess.run(["/bin/sh", "-c", cmd], env={"HOME": str(home), "PATH": os.environ["PATH"]}, capture_output=True, text=True, timeout=60)


def test_the_foreign_block_caps_its_own_logs_in_its_own_uid_after_one_tick(tmp_path, monkeypatch):
    """CAP (council 00:28Z fix-forward 1): `apply` caps only the applying uid's logs and a foreign user never runs apply, so its default log and
    its custom log grew forever. The block now ends with ONE cap line that runs `crons.py caps` as that uid (no sudo, no key); one tick bounds both."""
    root, home, lines = _foreign_project(tmp_path, monkeypatch)
    cap = [l for l in lines if " caps --root " in l]
    assert len(cap) == 1 and lines[-1] == cap[0] and cap[0].startswith("*/5 * * * * ") and " --name board.log " in cap[0]
    (home / "logs").mkdir()
    over = b"x" * (1024 * 1024 + 8192)
    default = home / "logs" / crons._log_path(root).name
    custom = home / "logs" / "board.log"
    other = home / "logs" / "unrelated.log"
    for f in (default, custom, other):
        f.write_bytes(over)
    r = _run(cap[0], home)
    assert r.returncode == 0, r.stderr
    assert default.stat().st_size <= 1024 * 1024 and custom.stat().st_size <= 1024 * 1024
    assert other.stat().st_size == len(over)                                              # the scope is the DECLARED names, never a glob


def test_a_block_with_no_job_has_no_cap_line_and_the_kill_switch_stays_empty(tmp_path, monkeypatch):
    root, home, lines = _foreign_project(tmp_path, monkeypatch)
    node = crons.load_crons_node(root)
    assert crons.render_managed_lines(root, root, root, node, user="agi-nobody", only_bound=True) == []
    node["crons_live"] = False
    assert crons.render_managed_lines(root, root, root, node, user=OTHER, only_bound=True) == []


def test_an_absent_home_logs_dir_still_runs_the_foreign_job(tmp_path, monkeypatch):
    """MKDIR (council 00:28Z fix-forward 2): the redirect `>> ~/logs/x` fails as silently on a MISSING dir as on an unwritable one, and the only
    mkdirs were the invoking uid's. Every foreign line makes ~/logs first."""
    root, home, lines = _foreign_project(tmp_path, monkeypatch)
    assert not (home / "logs").exists()
    for l in lines:
        assert " && mkdir -p ~/logs && " in l
    r = _run([l for l in lines if "drain-ran" in l][0], home)
    assert r.returncode == 0 and "drain-ran" in (home / "logs" / crons._log_path(root).name).read_text()
    r = _run([l for l in lines if "board-ran" in l][0], home)
    assert r.returncode == 0 and "board-ran" in (home / "logs" / "board.log").read_text()


# ---- SM 00:34Z: a successful `apply --sudo` of a foreign block must not print `pending`; a real refusal still does

STATEFUL_SUDO = """#!/bin/sh
# a fake `sudo [-n] crontab -u USER (-l | -)` over a dir of per-user crontabs: the real tool's contract (stdout the crontab, `no crontab for U` rc 1)
[ "$1" = -n ] && shift
[ "$1" = crontab ] && shift
shift; u=$1; shift; f=$FAKE_CRON_DIR/$u
case $1 in
-l) [ -f $f ] && { cat $f; exit 0; }; echo "no crontab for $u" >&2; exit 1;;
-) cat > $f; exit 0;;
esac
exit 2
"""


def _stateful_sudo(tmp_path, monkeypatch):
    fake, state = tmp_path / "fakebin", tmp_path / "crontabs"
    fake.mkdir()
    state.mkdir()
    sudo = fake / "sudo"
    sudo.write_text(STATEFUL_SUDO)
    sudo.chmod(sudo.stat().st_mode | stat.S_IXUSR)
    monkeypatch.setenv("PATH", f"{fake}:{os.environ['PATH']}")
    monkeypatch.setenv("FAKE_CRON_DIR", str(state))
    return state


def test_a_successful_sudo_apply_installs_and_never_says_pending(tmp_path, monkeypatch):
    """The `--sudo` path ran `sudo crontab -u U` WITHOUT capturing output: a user with no crontab (the first install) read as a refusal (`pending`,
    nothing installed) and a user WITH one crashed the reader on `None.splitlines()`. Both installs, then a second apply, say installed / unchanged."""
    state = _stateful_sudo(tmp_path, monkeypatch)
    root = make_project(tmp_path, cadences={**CADENCES})
    own = tmp_path / "own.cron"
    own.write_text("")
    first = crons.cmd_apply(root, own, sudo=True, allow_temp=True)["foreign_users"][OTHER]                  # no crontab yet
    assert first["status"] == "installed" and "echo board" in (state / OTHER).read_text()
    (state / OTHER).write_text("5 5 * * * their-own-job\n" + (state / OTHER).read_text())
    again = crons.cmd_apply(root, own, sudo=True, allow_temp=True)["foreign_users"][OTHER]                  # one WITH lines of its own
    assert again["status"] == "unchanged" and "their-own-job" in (state / OTHER).read_text()
    write_crons_node(root, False, {**CADENCES})                                              # the kill switch empties the block, keeps theirs
    off = crons.cmd_apply(root, own, sudo=True, allow_temp=True)["foreign_users"][OTHER]
    assert off["status"] == "installed" and "echo board" not in (state / OTHER).read_text() and "their-own-job" in (state / OTHER).read_text()
    for st in (first, again, off):
        assert "pending" not in st["status"]


def test_a_real_refusal_under_sudo_is_still_pending(tmp_path, monkeypatch):
    fake = tmp_path / "fakebin"
    fake.mkdir()
    sudo = fake / "sudo"
    sudo.write_text("#!/bin/sh\necho 'sudo: a password is required' >&2\nexit 1\n")
    sudo.chmod(sudo.stat().st_mode | stat.S_IXUSR)
    monkeypatch.setenv("PATH", f"{fake}:{os.environ['PATH']}")
    root = make_project(tmp_path, cadences={**CADENCES})
    own = tmp_path / "own.cron"
    own.write_text("")
    st = crons.cmd_apply(root, own, sudo=True, allow_temp=True)["foreign_users"][OTHER]
    assert st["status"].startswith("pending") and "a password is required" in st["status"] and st["changed"] is None


def test_when_the_runner_is_the_rows_user_the_block_is_the_own_block(tmp_path, monkeypatch):
    """The other branch of `foreign = me != _invoking_user()` (SM 02:14Z leaf note; the board-line row pins a FOREIGN fixture runner, so nothing pinned this): the
    runner IS agi-belam, so its block is the OWN block, as today: no `mkdir -p ~/logs` (apply made the dir), NO cap line (apply caps the applying uid's own logs),
    a row with no log: cell logs to the renderer's own home path (a real path, not a tilde word), and `{logs}` renders that path too."""
    home = tmp_path / "belam-home"
    monkeypatch.setenv("HOME", str(home))
    monkeypatch.setattr(crons, "_invoking_user", lambda: "agi-belam")
    live = yaml.safe_load(LIVE_CRONS.read_text().split("---")[1])["cadences"]
    more = {"alarm_drain_x": {"schedule": "*/5 * * * *", "cmd": "echo drain {logs}/x", "user": "agi-belam", "box": "encryption-town"}}
    proj = make_project(tmp_path, cadences={**live, **more})
    lines = _belam_lines(proj, proj)
    assert len(lines) >= 2 and not any(" caps --root " in l or "mkdir -p ~/logs" in l for l in lines)
    (drain,) = [l for l in lines if "echo drain" in l]
    assert f"echo drain {home}/logs/x" in drain and f">> {crons._log_path(proj)} 2>&1" in drain and "~/logs" not in drain
    (board,) = [l for l in lines if "board_job.py commit" in l]
    assert board.endswith(">> ~/logs/board_job.log 2>&1")                      # the row's OWN log: cell is used as written
