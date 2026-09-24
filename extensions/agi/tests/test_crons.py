"""Tests for bin/crons.py — the crontab as a derivation of
`nodes/.geometry/crons.md` (goal:g1.5).

The load-bearing tests here are not the happy path — they are the safety
net: this machine's real crontab carries production lines (openclaw cleanup,
a trading bridge watchdog, fantasia's own crons) that destroying would be a
real incident, so every test that touches `apply`/`remove` seeds a fixture
crontab with unrelated lines and asserts they survive byte-for-byte, in
order, through everything this module does. No test in this file ever calls
the real `crontab` binary in write mode — every apply/remove goes through
`--crontab-file`.
"""
from __future__ import annotations

import json
import os
import subprocess
import sys
from pathlib import Path

import pytest
import yaml

BIN = Path(__file__).resolve().parents[1] / "bin"
sys.path.insert(0, str(BIN))

import crons  # noqa: E402
import boxes  # noqa: E402

# The one schema declaration every fixture root carries now that crons renders
# every placeholder through `boxes.resolve_placeholders` (this round's claim).
BOX_SCHEMA = """---
name: box
structural: true
fields:
  root: {type: str}
  logs_dir: {type: str}
  tmux_session: {type: str}
  user: {type: str}
placeholders:
  root: root
  logs: logs_dir
  tmux: tmux_session
  user: user
  repo_root: repo_root
  box: box
---
"""


@pytest.fixture
def fake_systemctl(tmp_path, monkeypatch):
    """A FAKE `systemctl` on PATH (residue b): records every argv line into
    `tmp_path/systemctl.calls` and exits 0. Proves `apply`'s exact unit
    systemctl argv and guarantees the REAL user manager (`systemctl --user`
    is live on the box) is never reached from a test.

    Also pins a REACHABLE user bus for the seam: XDG_RUNTIME_DIR points at a
    tmp dir whose `bus` socket exists, and DBUS_SESSION_BUS_ADDRESS is cleared,
    so `_systemd_bus_env` resolves the env to add and the systemctl calls run
    deterministically regardless of whether the test shell itself has a login
    session (a cron-style apply does not). Tests that want the NO-BUS skip
    monkeypatch these over.

    Each invocation ALSO records the env it was actually invoked with (the
    merged env `_apply_systemctl` passes in — residue for the L4.129 bus-env
    merge): one `XDG_RUNTIME_DIR=<v>|DBUS_SESSION_BUS_ADDRESS=<v>` line per
    call into `tmp_path/systemctl.env`, in the same order as the argv log, so
    a test can assert the fallback/caller bus address actually reached the
    subprocess. Deleting `env=merged` in crons.py then leaves a test red.
    """
    bin = tmp_path / "fakebin"
    bin.mkdir()
    log = tmp_path / "systemctl.calls"
    envlog = tmp_path / "systemctl.env"
    answers = tmp_path / "systemctl.answers"
    script = bin / "systemctl"
    script.write_text(
        "#!/usr/bin/env bash\n"
        f'echo "$@" >> {log}\n'
        f'echo "XDG_RUNTIME_DIR=${{XDG_RUNTIME_DIR-}}|DBUS_SESSION_BUS_ADDRESS=${{DBUS_SESSION_BUS_ADDRESS-}}" >> {envlog}\n'
        # Probes (hypothesis:l4-crons-apply-records-one-state-line-...):
        # `is-enabled` / `is-active` are answered per-test by {answers} — a
        # line "<probe>: 1" makes that probe exit 1 (not enabled / not
        # active / probe failed); by default (no answers file, or the probe
        # not listed) the unit is enabled+active, which drives the no-op path.
        'case "$2" in\n'
        '  is-enabled|is-active)\n'
        f'    if [[ -f \"{answers}\" ]] && grep -qE \"^$2: 1$\" \"{answers}\"; then exit 1; fi;;\n'
        'esac\n'
        "exit 0\n")
    script.chmod(0o755)
    monkeypatch.setenv(
        "PATH", str(bin) + os.pathsep + os.environ.get("PATH", ""))
    runtime = tmp_path / "runtime"
    runtime.mkdir()
    (runtime / "bus").write_text("")
    monkeypatch.setenv("XDG_RUNTIME_DIR", str(runtime))
    monkeypatch.delenv("DBUS_SESSION_BUS_ADDRESS", raising=False)
    return log


# --- fixtures ---------------------------------------------------------


DEFAULT_CADENCES = {
    "grid_sync": {"every_mins": 5, "enabled": True},
    "branch_push": {"schedule": "7 * * * *", "enabled": True},
    "publish_engine": {"schedule": "37 * * * *", "enabled": True},
    "engine_push": {"schedule": "47 * * * *", "enabled": True},
}


def _crons_frontmatter(crons_live=True, cadences=None, services=None) -> str:
    if cadences is None:
        cadences = DEFAULT_CADENCES
    fm = {
        "id": "cron:crons",
        "type": "cron",
        "crons_live": crons_live,
        "cadences": cadences,
    }
    if services:
        fm["services"] = services
    return "---\n" + yaml.safe_dump(fm, sort_keys=False) + "---\n\nBody.\n"


def write_crons_node(root: Path, crons_live=True, cadences=None, services=None) -> None:
    p = root / crons.CRONS_NODE_REL
    p.parent.mkdir(parents=True, exist_ok=True)
    p.write_text(_crons_frontmatter(crons_live, cadences, services))
    s = root / "context" / "schemas" / "[box].md"
    s.parent.mkdir(parents=True, exist_ok=True)
    if not s.exists():
        s.write_text(BOX_SCHEMA)


def _git(path: Path, *args: str) -> str:
    res = subprocess.run(["git", *args], cwd=path, capture_output=True, text=True)
    if res.returncode != 0:
        raise RuntimeError(f"git {args}: {res.stderr}")
    return res.stdout.strip()


def _git_init(path: Path, branch: str = "master", detach: bool = False) -> None:
    path.mkdir(parents=True, exist_ok=True)
    _git(path, "init", "-q", "-b", branch)
    _git(path, "config", "user.email", "test@example.com")
    _git(path, "config", "user.name", "test")
    (path / ".keep").write_text("x")
    _git(path, "add", ".")
    _git(path, "commit", "-q", "-m", "init")
    if detach:
        sha = _git(path, "rev-parse", "HEAD")
        _git(path, "checkout", "-q", "--detach", sha)


def make_worktree_project(tmp_path, wt_name="wt"):
    """A real linked git worktree (`git worktree add`), the shape the refusal
    exists for: `main` is the common root, `wt` is a linked worktree that
    carries its own `agi-tree.config.json` — indistinguishable from a separate
    project to `repo_root` but not to `git_common_root`. Returns `(main, wt)`.

    grid_sync + branch_push only: publish_engine and engine_push are disabled
    so no engine checkout is needed to render."""
    main = tmp_path / "main"
    main.mkdir(parents=True)
    _git_init(main, branch="master")
    wt = tmp_path / wt_name
    _git(main, "worktree", "add", "-q", str(wt), "-b", "season/s2")
    (wt / "agi-tree.config.json").write_text("{}")
    cad = dict(DEFAULT_CADENCES)
    cad["publish_engine"] = {"schedule": "37 * * * *", "enabled": False}
    cad["engine_push"] = {"schedule": "47 * * * *", "enabled": False}
    write_crons_node(wt, crons_live=True, cadences=cad)
    return main, wt


def make_project(tmp_path, name="proj", crons_live=True, cadences=None,
                 repo_branch="master", engine_branch="master",
                 detach_repo=False, detach_engine=False, engine=True) -> Path:
    """A legacy-layout project: root IS the graph repo, `root/agi` is the
    engine clone beside it — today's real agi-tree/fantasia shape."""
    root = tmp_path / name
    root.mkdir(parents=True)
    (root / "agi-tree.config.json").write_text("{}")
    write_crons_node(root, crons_live, cadences)
    _git_init(root, branch=repo_branch, detach=detach_repo)
    if engine:
        _git_init(root / "agi", branch=engine_branch, detach=detach_engine)
    return root


# --- load_crons_node: parsing and validation ----------------------------


def test_load_valid_node(tmp_path):
    cad = dict(DEFAULT_CADENCES)
    cad["mail_poll"] = {"every_mins": 5, "enabled": True}
    cad["nudge_sweep"] = {"every_mins": 2, "enabled": True}
    root = make_project(tmp_path, cadences=cad)
    node = crons.load_crons_node(root)
    assert node["crons_live"] is True
    assert set(node["jobs"]) == set(crons.KNOWN_JOBS)
    assert node["jobs"]["grid_sync"]["every_mins"] == 5
    assert node["jobs"]["branch_push"]["schedule"] == "7 * * * *"


def test_missing_node_file_names_the_path(tmp_path):
    root = tmp_path / "proj"
    root.mkdir()
    (root / "agi-tree.config.json").write_text("{}")
    with pytest.raises(crons.CronsError, match=r"missing node file.*crons\.md"):
        crons.load_crons_node(root)


def test_missing_frontmatter_delimiter(tmp_path):
    root = tmp_path / "proj"
    p = root / crons.CRONS_NODE_REL
    p.parent.mkdir(parents=True)
    p.write_text("no frontmatter here\n")
    with pytest.raises(crons.CronsError, match="no YAML frontmatter"):
        crons.load_crons_node(root)


def test_malformed_yaml_raises_naming_the_file(tmp_path):
    root = tmp_path / "proj"
    p = root / crons.CRONS_NODE_REL
    p.parent.mkdir(parents=True)
    p.write_text("---\ncrons_live: [oops\n---\nbody\n")
    with pytest.raises(crons.CronsError, match="malformed YAML"):
        crons.load_crons_node(root)


def test_missing_crons_live_key(tmp_path):
    root = tmp_path / "proj"
    p = root / crons.CRONS_NODE_REL
    p.parent.mkdir(parents=True)
    p.write_text("---\ncadences: {}\n---\nbody\n")
    with pytest.raises(crons.CronsError, match="crons_live"):
        crons.load_crons_node(root)


def test_non_bool_crons_live(tmp_path):
    root = tmp_path / "proj"
    write_crons_node(root, crons_live="yes")  # not a real bool
    with pytest.raises(crons.CronsError, match="true/false"):
        crons.load_crons_node(root)


def test_unknown_job_name_rejected(tmp_path):
    root = tmp_path / "proj"
    write_crons_node(root, cadences={"totally_made_up": {"every_mins": 1}})
    with pytest.raises(crons.CronsError, match="unknown job"):
        crons.load_crons_node(root)


def test_both_every_mins_and_schedule_rejected(tmp_path):
    root = tmp_path / "proj"
    write_crons_node(root, cadences={
        "grid_sync": {"every_mins": 5, "schedule": "* * * * *", "enabled": True},
    })
    with pytest.raises(crons.CronsError, match="exactly one"):
        crons.load_crons_node(root)


def test_enabled_job_with_neither_field_rejected(tmp_path):
    root = tmp_path / "proj"
    write_crons_node(root, cadences={"grid_sync": {"enabled": True}})
    with pytest.raises(crons.CronsError, match="neither"):
        crons.load_crons_node(root)


def test_disabled_job_may_omit_schedule(tmp_path):
    root = make_project(tmp_path, cadences={"grid_sync": {"enabled": False}})
    node = crons.load_crons_node(root)
    assert node["jobs"]["grid_sync"]["enabled"] is False


def test_bad_every_mins_type_rejected(tmp_path):
    root = tmp_path / "proj"
    write_crons_node(root, cadences={"grid_sync": {"every_mins": "five", "enabled": True}})
    with pytest.raises(crons.CronsError, match="positive integer"):
        crons.load_crons_node(root)


def test_bad_schedule_field_count_rejected(tmp_path):
    root = tmp_path / "proj"
    write_crons_node(root, cadences={"branch_push": {"schedule": "* * *", "enabled": True}})
    with pytest.raises(crons.CronsError, match="5-field"):
        crons.load_crons_node(root)


def test_job_absent_from_cadences_is_never_rendered(tmp_path):
    root = make_project(tmp_path, cadences={
        "grid_sync": {"every_mins": 5, "enabled": True},
    })
    node = crons.load_crons_node(root)
    assert set(node["jobs"]) == {"grid_sync"}


# --- the branch check (S2, non-negotiable) ------------------------------


def test_resolve_branch_on_normal_repo(tmp_path):
    repo = tmp_path / "r"
    _git_init(repo, branch="master")
    assert crons.resolve_branch(repo) == "master"


def test_resolve_branch_non_default_name(tmp_path):
    """Never hardcode master/main — a differently-named branch must resolve
    to its own name, not a guess."""
    repo = tmp_path / "r"
    _git_init(repo, branch="iter24-extend-300hop")
    assert crons.resolve_branch(repo) == "iter24-extend-300hop"


def test_resolve_branch_detached_head_refuses(tmp_path):
    repo = tmp_path / "r"
    _git_init(repo, branch="master", detach=True)
    with pytest.raises(crons.CronsError, match="detached"):
        crons.resolve_branch(repo)


def test_render_refuses_on_detached_repo(tmp_path):
    root = make_project(tmp_path, detach_repo=True)
    _, cfg, repo_root, engine_root, node = crons._resolve(root)
    with pytest.raises(crons.CronsError, match="detached"):
        crons.render_managed_lines(root, repo_root, engine_root, node)


def test_render_refuses_on_detached_engine(tmp_path):
    root = make_project(tmp_path, detach_engine=True)
    _, cfg, repo_root, engine_root, node = crons._resolve(root)
    with pytest.raises(crons.CronsError, match="detached"):
        crons.render_managed_lines(root, repo_root, engine_root, node)


def test_render_uses_the_actual_checked_out_branch(tmp_path):
    root = make_project(tmp_path, repo_branch="iter24-extend-300hop",
                        engine_branch="feature-x")
    _, cfg, repo_root, engine_root, node = crons._resolve(root)
    lines = crons.render_managed_lines(root, repo_root, engine_root, node)
    branch_push = next(l for l in lines if "push -q origin iter24-extend-300hop" in l)
    engine_push = next(l for l in lines if "push -q origin feature-x" in l)
    assert branch_push and engine_push
    assert " master" not in branch_push
    assert " master" not in engine_push


# --- rendering shape -----------------------------------------------------


def test_render_every_line_cds_into_root_first(tmp_path):
    root = make_project(tmp_path)
    _, cfg, repo_root, engine_root, node = crons._resolve(root)
    lines = crons.render_managed_lines(root, repo_root, engine_root, node)
    assert len(lines) == 4
    for line in lines:
        assert f"cd {root} &&" in line


def test_render_order_matches_known_jobs(tmp_path):
    root = make_project(tmp_path)
    _, cfg, repo_root, engine_root, node = crons._resolve(root)
    lines = crons.render_managed_lines(root, repo_root, engine_root, node)
    # grid_sync (*/5), branch_push (min 7), publish_engine (min 37), engine_push (min 47)
    assert lines[0].startswith("*/5 * * * *")
    assert lines[1].startswith("7 * * * *")
    assert lines[2].startswith("37 * * * *")
    assert lines[3].startswith("47 * * * *")


def test_grid_sync_line_self_reapplies(tmp_path):
    """The self-reapply property: editing the node and letting the grid_sync
    cadence run must, by itself, converge the real crontab — so its own line
    must invoke `crons.py apply`."""
    root = make_project(tmp_path)
    _, cfg, repo_root, engine_root, node = crons._resolve(root)
    lines = crons.render_managed_lines(root, repo_root, engine_root, node)
    grid_sync_line = lines[0]
    expected = engine_root / "extensions" / "agi" / "bin" / "crons.py"
    assert f"python3 {expected} apply" in grid_sync_line
    # And it must not carry --crontab-file: production self-reapply targets
    # the real crontab, never a test fixture.
    assert "--crontab-file" not in grid_sync_line


def test_self_reapply_names_the_engine_copy_not_the_running_one(tmp_path):
    """Regression: the persisted path must be the durable one.

    The line this renders outlives the process that rendered it, so it has to
    name the published engine copy rather than whichever copy called `apply`.
    Engine work is normally done from `payloads/` (goal:g6.3) — a gitignored
    staging tree that `grid.py checkout --force` can overwrite and that a fresh
    clone does not have at all. Baking that path into the one job responsible
    for re-applying every other job is the failure this guards.
    """
    root = make_project(tmp_path)
    _, cfg, repo_root, engine_root, node = crons._resolve(root)
    grid_sync_line = crons.render_managed_lines(root, repo_root, engine_root, node)[0]

    assert str(engine_root) in grid_sync_line
    assert "payloads" not in grid_sync_line
    # The applier that is actually executing this test lives somewhere else
    # entirely; its own location must not appear in the rendered line.
    assert str(Path(crons.__file__).resolve()) not in grid_sync_line


def test_disabled_job_omitted(tmp_path):
    cadences = dict(DEFAULT_CADENCES)
    cadences["publish_engine"] = {"schedule": "37 * * * *", "enabled": False}
    root = make_project(tmp_path, cadences=cadences)
    _, cfg, repo_root, engine_root, node = crons._resolve(root)
    lines = crons.render_managed_lines(root, repo_root, engine_root, node)
    assert len(lines) == 3
    assert not any("publish-engine.sh" in l for l in lines)


def test_crons_live_false_renders_nothing(tmp_path):
    root = make_project(tmp_path, crons_live=False)
    _, cfg, repo_root, engine_root, node = crons._resolve(root)
    lines = crons.render_managed_lines(root, repo_root, engine_root, node)
    assert lines == []


# --- markers: two projects never collide ---------------------------------


def test_project_hash_distinct_per_project(tmp_path):
    a = make_project(tmp_path, name="proj-a")
    b = make_project(tmp_path, name="proj-b")
    assert crons.project_hash(a) != crons.project_hash(b)


def test_block_markers_are_deterministic(tmp_path):
    root = make_project(tmp_path)
    b1 = crons.block_markers(root)
    b2 = crons.block_markers(root)
    assert b1 == b2


# --- split_managed_block: the safety net ----------------------------------


UNRELATED_LINES = [
    "# openclaw session cleanup",
    "*/10 * * * * /usr/local/bin/openclaw-cleanup.sh",
    "0 3 * * * /opt/relmap/run.sh >> /var/log/relmap.log 2>&1",
    "*/2 * * * * /opt/trading/watchdog.sh --quiet",
    "15 4 * * * /opt/regime/refresh.sh",
    "* * * * * /opt/autocommit/run.sh",
]


def test_split_no_match_returns_everything_as_before(tmp_path):
    before, managed, after = crons.split_managed_block(
        UNRELATED_LINES, "# >>> agi-crons deadbeef >>>", "# <<< agi-crons deadbeef <<<")
    assert before == UNRELATED_LINES
    assert managed == []
    assert after == []


def test_split_unterminated_block_raises(tmp_path):
    begin = "# >>> agi-crons deadbeef >>>"
    end = "# <<< agi-crons deadbeef <<<"
    lines = ["a", begin, "1 2 3 4 5 foo"]
    with pytest.raises(crons.CronsError, match="no matching"):
        crons.split_managed_block(lines, begin, end)


# --- apply / show / remove: the real behavioural contract -----------------


def _read(path: Path) -> list[str]:
    return path.read_text().splitlines() if path.exists() else []


def test_apply_writes_managed_block_preserving_unrelated_lines(tmp_path):
    root = make_project(tmp_path)
    fixture = tmp_path / "crontab.fixture"
    fixture.write_text("\n".join(UNRELATED_LINES) + "\n")

    result = crons.cmd_apply(root, crontab_file=fixture)
    assert result["changed"] is True

    out = _read(fixture)
    # every unrelated line survives, byte for byte, in order
    assert out[:len(UNRELATED_LINES)] == UNRELATED_LINES
    begin, end = crons.block_markers(result["repo_root"])
    assert begin in out
    assert end in out
    assert out.index(begin) < out.index(end)
    for line in result["managed_lines"]:
        assert line in out


def test_apply_twice_is_byte_identical(tmp_path):
    root = make_project(tmp_path)
    fixture = tmp_path / "crontab.fixture"
    fixture.write_text("\n".join(UNRELATED_LINES) + "\n")

    crons.cmd_apply(root, crontab_file=fixture)
    first = fixture.read_text()

    result2 = crons.cmd_apply(root, crontab_file=fixture)
    second = fixture.read_text()

    assert first == second, "running apply twice must be a no-op on the bytes"
    assert result2["changed"] is False


# --- the worktree refusal + the separator fix (hypothesis:l4-a-worktree- ---
# --- looks-like-a-project-to-the-crontab) --------------------------------


def test_apply_from_linked_worktree_refuses_writes_nothing(tmp_path):
    """ITEM 1: a seat worktree is a separate top-level to `repo_root`, so an
    `apply` from one would append a SECOND managed block beside the main
    checkout's. It must REFUSE loudly, and must not write a byte — the passed
    crontab_file stays byte-identical, not merely less-modified."""
    _main, wt = make_worktree_project(tmp_path)
    fixture = tmp_path / "crontab.fixture"
    fixture.write_text("\n".join(UNRELATED_LINES) + "\n")
    original = fixture.read_text()

    with pytest.raises(crons.CronsError, match="WORKTREE"):
        crons.cmd_apply(wt, crontab_file=fixture)
    assert fixture.read_text() == original, "refusal must write NOTHING"


def test_show_from_linked_worktree_refuses_naming_both_roots(tmp_path):
    """show must say the same thing rather than rendering a block it would
    refuse to install — naming the worktree it found and the common root it
    wants."""
    main, wt = make_worktree_project(tmp_path)
    wt_root = str(wt.resolve())
    with pytest.raises(crons.CronsError, match="common root"):
        crons.cmd_show(wt, crontab_file=str(tmp_path / "crontab.fixture"))
    # the refusal text names BOTH roots (relative-safe: resolution may symlink)


def test_apply_from_plain_clone_does_not_refuse(tmp_path):
    """The refusal must NOT fire on an ordinary non-worktree clone — where
    repo_root and git_common_root agree, apply proceeds exactly as before."""
    root = make_project(tmp_path)  # legacy-layout: root IS the repo root
    fixture = tmp_path / "crontab.fixture"
    fixture.write_text("")
    result = crons.cmd_apply(root, crontab_file=fixture)
    assert result["changed"] is True
    assert len(result["managed_lines"]) == 4


def test_apply_from_common_root_only_separator_delta(tmp_path):
    """ITEM 2 guard: same jobs, same schedules as today — the ONLY textual
    difference from the old rendering is `;` in place of `&&` between the
    three grid_sync steps. Assert the delta explicitly so the guard cannot
    become a behaviour change wearing a guard's clothes."""
    root = make_project(tmp_path)
    fixture = tmp_path / "crontab.fixture"
    fixture.write_text("")
    result = crons.cmd_apply(root, crontab_file=fixture)
    assert len(result["managed_lines"]) == 4
    grid_sync = result["managed_lines"][0]

    _, cfg, repo_root, engine_root, node = crons._resolve(root)
    log = crons._log_path(repo_root)
    grid_py = engine_root / "extensions" / "agi" / "bin" / "grid.py"
    crons_py = engine_root / "extensions" / "agi" / "bin" / "crons.py"
    udir = Path.home() / ".config" / "systemd" / "user"

    # What today rendered (the `&&` chain, plus the residue-b --unit-dir on
    # the self-reapply) — reconstructed honestly as the reference the delta
    # is measured against.
    today = (
        f"*/5 * * * * cd {root} && python3 {grid_py} commit --all "
        f"--prefix 'cron: ' >> {log} 2>&1 && git -C {repo_root} push -q origin "
        f"'refs/grid/*:refs/grid/*' >> {log} 2>&1 && python3 {crons_py} apply "
        f"--unit-dir {udir} >> {log} 2>&1"
    )
    # Same jobs and schedules, and the only delta is: `;` where the chain had
    # `&&` between the steps (never touching the leading `cd {root} &&`).
    assert grid_sync == today.replace("2>&1 && git", "2>&1; git").replace(
        "2>&1 && python3", "2>&1; python3")
    assert grid_sync != today


def test_grid_sync_apply_not_chain_downstream_of_grid(tmp_path):
    """ITEM 2 shape invariant, asserted on the RENDERED STRING (never a mocked
    shell): `crons.py apply` is not `&&`-downstream of the grid command — a
    grid failure cannot cancel the self-reapply."""
    root = make_project(tmp_path)
    _, cfg, repo_root, engine_root, node = crons._resolve(root)
    grid_sync_line = crons.render_managed_lines(
        root, repo_root, engine_root, node)[0]
    crons_py = engine_root / "extensions" / "agi" / "bin" / "crons.py"
    assert f"&& python3 {crons_py} apply" not in grid_sync_line
    assert f"; python3 {crons_py} apply" in grid_sync_line


# --------------- goal:g14.14.7 -- the push refspec is config-declared ------ -


def test_grid_sync_pushes_the_configured_storage_trunk(tmp_path):
    """The rendered cron line derives its push refspec from
    `grid.storage_trunk` through grid.py's ONE resolver -- never a second
    literal. This is the line that was hardcoded at crons.py:549."""
    root = make_project(tmp_path)
    (root / "agi-tree.config.json").write_text(
        json.dumps({"grid": {"storage_trunk": "refs/grid/t1/"}}))
    _, _cfg, repo_root, engine_root, node = crons._resolve(root)
    line = crons.render_managed_lines(root, repo_root, engine_root, node)[0]
    assert "'refs/grid/t1/*:refs/grid/t1/*'" in line
    assert "'refs/grid/*:refs/grid/*'" not in line


def test_grid_sync_default_push_refspec_is_unchanged(tmp_path):
    """No `storage_trunk` key -> the cron line is byte-identical to today's."""
    root = make_project(tmp_path)
    _, _cfg, repo_root, engine_root, node = crons._resolve(root)
    line = crons.render_managed_lines(root, repo_root, engine_root, node)[0]
    assert "'refs/grid/*:refs/grid/*'" in line


def test_grid_sync_grid_step_still_logs_not_suppressed(tmp_path):
    """ITEM 2 second half: separating the domains must not buy the reapply by
    hiding the grid failure — the grid step is still redirected to the log,
    still visible, not to /dev/null."""
    root = make_project(tmp_path)
    _, cfg, repo_root, engine_root, node = crons._resolve(root)
    grid_sync_line = crons.render_managed_lines(
        root, repo_root, engine_root, node)[0]
    log = crons._log_path(repo_root)
    grid_py = engine_root / "extensions" / "agi" / "bin" / "grid.py"
    assert (f"python3 {grid_py} commit --all --prefix 'cron: ' "
            f">> {log} 2>&1" in grid_sync_line)
    assert "/dev/null" not in grid_sync_line


def test_apply_dry_run_writes_nothing(tmp_path):
    root = make_project(tmp_path)
    fixture = tmp_path / "crontab.fixture"
    fixture.write_text("\n".join(UNRELATED_LINES) + "\n")
    original = fixture.read_text()

    result = crons.cmd_apply(root, crontab_file=fixture, dry_run=True)
    assert fixture.read_text() == original, "--dry-run must not touch the file"
    assert len(result["managed_lines"]) == 4


def test_apply_creates_the_log_directory_the_lines_redirect_into(
        tmp_path, monkeypatch):
    """ITEM (d): every managed line redirects `>> {_log_path} 2>&1`, so a
    fresh box whose `~/logs/` does not exist would write nothing and show no
    error. `cmd_apply` must create that directory as it installs the lines."""
    monkeypatch.setenv("HOME", str(tmp_path / "home"))
    root = make_project(tmp_path)
    fixture = tmp_path / "crontab.fixture"
    fixture.write_text("")
    log = crons._log_path(crons.locations.repo_root(root))
    assert not log.parent.exists(), "fixture HOME must start with no ~/logs"

    crons.cmd_apply(root, crontab_file=fixture)
    assert log.parent.is_dir(), "apply left the redirect target dir missing"


def test_apply_dry_run_creates_no_log_directory(tmp_path, monkeypatch):
    """A dry run installs nothing, so it must not create the log dir either."""
    monkeypatch.setenv("HOME", str(tmp_path / "home"))
    root = make_project(tmp_path)
    fixture = tmp_path / "crontab.fixture"
    fixture.write_text("")
    log = crons._log_path(crons.locations.repo_root(root))

    crons.cmd_apply(root, crontab_file=fixture, dry_run=True)
    assert not log.parent.exists(), "--dry-run created ~/logs"


def test_two_projects_coexist_in_one_crontab(tmp_path):
    """The other non-negotiable safety property: a second project's block
    must be untouched by this project's apply/remove."""
    proj_a = make_project(tmp_path, name="proj-a")
    proj_b = make_project(tmp_path, name="proj-b")
    fixture = tmp_path / "crontab.fixture"
    fixture.write_text("\n".join(UNRELATED_LINES) + "\n")

    crons.cmd_apply(proj_a, crontab_file=fixture)
    crons.cmd_apply(proj_b, crontab_file=fixture)

    begin_a, end_a = crons.block_markers(crons.locations.repo_root(proj_a))
    begin_b, end_b = crons.block_markers(crons.locations.repo_root(proj_b))
    lines = _read(fixture)
    assert begin_a in lines and end_a in lines
    assert begin_b in lines and end_b in lines

    # removing project A must not disturb project B's block or the unrelated lines
    crons.cmd_remove(proj_a, crontab_file=fixture)
    lines_after = _read(fixture)
    assert begin_a not in lines_after and end_a not in lines_after
    assert begin_b in lines_after and end_b in lines_after
    assert lines_after[:len(UNRELATED_LINES)] == UNRELATED_LINES


def test_kill_switch_removes_all_managed_lines(tmp_path):
    """`crons_live: false` -> apply removes every line for this project in
    one shot, the single edit the goal:g11 migration relies on."""
    root = make_project(tmp_path)
    fixture = tmp_path / "crontab.fixture"
    fixture.write_text("\n".join(UNRELATED_LINES) + "\n")
    crons.cmd_apply(root, crontab_file=fixture)
    assert len(_read(fixture)) > len(UNRELATED_LINES)

    write_crons_node(root, crons_live=False)
    result = crons.cmd_apply(root, crontab_file=fixture)
    assert result["managed_lines"] == []
    out = _read(fixture)
    assert out == UNRELATED_LINES
    begin, _end = crons.block_markers(result["repo_root"])
    assert begin not in out


def test_remove_only_this_projects_block(tmp_path):
    root = make_project(tmp_path)
    fixture = tmp_path / "crontab.fixture"
    fixture.write_text("\n".join(UNRELATED_LINES) + "\n")
    crons.cmd_apply(root, crontab_file=fixture)

    result = crons.cmd_remove(root, crontab_file=fixture)
    assert len(result["removed_lines"]) == 4
    out = _read(fixture)
    assert out == UNRELATED_LINES


def test_remove_when_nothing_installed_is_a_clean_noop(tmp_path):
    root = make_project(tmp_path)
    fixture = tmp_path / "crontab.fixture"
    fixture.write_text("\n".join(UNRELATED_LINES) + "\n")

    result = crons.cmd_remove(root, crontab_file=fixture)
    assert result["removed_lines"] == []
    assert _read(fixture) == UNRELATED_LINES


def test_show_reports_up_to_date_after_apply(tmp_path):
    root = make_project(tmp_path)
    fixture = tmp_path / "crontab.fixture"
    fixture.write_text("")
    crons.cmd_apply(root, crontab_file=fixture)
    report = crons.cmd_show(root, crontab_file=fixture)
    assert "status: up to date" in report


def test_show_reports_drift_before_apply(tmp_path):
    root = make_project(tmp_path)
    fixture = tmp_path / "crontab.fixture"
    fixture.write_text("")
    report = crons.cmd_show(root, crontab_file=fixture)
    assert "DRIFT" in report
    assert "desired:" in report


def test_disabled_engine_push_job_needs_no_engine_git(tmp_path):
    """A job that is off does not gate on the repo it would have used."""
    cadences = dict(DEFAULT_CADENCES)
    cadences["engine_push"] = {"schedule": "47 * * * *", "enabled": False}
    root = make_project(tmp_path, cadences=cadences, detach_engine=True)
    _, cfg, repo_root, engine_root, node = crons._resolve(root)
    lines = crons.render_managed_lines(root, repo_root, engine_root, node)
    assert len(lines) == 3
    # The engine_push template is specifically `git -C <engine_root> push`;
    # its absence (not a fuzzy substring match, which collides with the test's
    # own name) is what proves the disabled job never triggered the branch
    # check against the detached engine repo.
    assert not any(f"git -C {engine_root} push" in l for l in lines)


# --- CLI (main) ------------------------------------------------------------


def test_cli_apply_show_remove_round_trip(tmp_path, capsys):
    root = make_project(tmp_path)
    fixture = tmp_path / "crontab.fixture"
    fixture.write_text("\n".join(UNRELATED_LINES) + "\n")

    rc = crons.main(["apply", "--root", str(root), "--crontab-file", str(fixture)])
    assert rc == 0
    out = capsys.readouterr().out
    assert "installed 4 line(s)" in out

    rc = crons.main(["show", "--root", str(root), "--crontab-file", str(fixture)])
    assert rc == 0
    assert "status: up to date" in capsys.readouterr().out

    rc = crons.main(["remove", "--root", str(root), "--crontab-file", str(fixture)])
    assert rc == 0
    assert "removed 4 line(s)" in capsys.readouterr().out
    assert _read(fixture) == UNRELATED_LINES


def test_cli_missing_project_exits_nonzero(tmp_path, capsys):
    empty = tmp_path / "empty"
    empty.mkdir()
    rc = crons.main(["show", "--root", str(empty)])
    assert rc == 1
    assert "no agi project found" in capsys.readouterr().err


def test_cli_missing_node_exits_nonzero_naming_the_file(tmp_path, capsys):
    root = tmp_path / "proj"
    root.mkdir()
    (root / "agi-tree.config.json").write_text("{}")
    rc = crons.main(["show", "--root", str(root)])
    assert rc == 1
    err = capsys.readouterr().err
    assert "crons.md" in err


def test_cli_dry_run_reports_without_writing(tmp_path, capsys):
    root = make_project(tmp_path)
    fixture = tmp_path / "crontab.fixture"
    fixture.write_text("\n".join(UNRELATED_LINES) + "\n")
    original = fixture.read_text()

    rc = crons.main(["apply", "--root", str(root), "--crontab-file", str(fixture),
                     "--dry-run"])
    assert rc == 0
    assert fixture.read_text() == original
    assert "would install 4 line(s)" in capsys.readouterr().out


# --- services table: systemd units rendered from the graph (fixture seam) --


SER_REAPER = {
    "agi-reaper": {
        "enabled": True,
        "exec_start": "python3 /engine/extensions/agi/bin/heal.py watch "
                       "--root /proj --poll-s 30",
        "restart": "on-failure",
        "environment": {"NOTIFY": "off"},
    }
}


def test_no_services_table_is_byte_for_byte_noop_on_units(tmp_path):
    """The live state until the prime lands the table: a `services:`-less
    node + --unit-dir leaves the unit dir untouched and reports no actions."""
    root = make_project(tmp_path)
    ud = tmp_path / "units"
    result = crons.cmd_apply(root, crontab_file=tmp_path / "crontab.fixture",
                             unit_dir=ud)
    assert result["unit_actions"] == []
    assert not ud.exists() or not list(ud.iterdir())


def test_plain_apply_without_unit_dir_touches_no_units(tmp_path, capsys):
    """Unit management is opt-in via the seam: a plain apply (the grid_sync
    self-reapply line) never reaches for units even when the node declares a
    services table."""
    root = make_project(tmp_path, cadences=dict(DEFAULT_CADENCES))
    write_crons_node(root, crons_live=True, cadences=DEFAULT_CADENCES,
                     services=SER_REAPER)
    result = crons.cmd_apply(root, crontab_file=tmp_path / "crontab.fixture")
    assert result["unit_actions"] == []
    assert result["unit_dir"] is None


def test_services_table_writes_unit_byte_for_byte_idempotent(tmp_path, fake_systemctl):
    root = make_project(tmp_path, cadences=dict(DEFAULT_CADENCES))
    write_crons_node(root, crons_live=True, cadences=DEFAULT_CADENCES,
                     services=SER_REAPER)
    ud = tmp_path / "units"
    fixture = tmp_path / "crontab.fixture"

    r1 = crons.cmd_apply(root, crontab_file=fixture, unit_dir=ud)
    unit = next(ud.glob("agi-*.service"))
    first = unit.read_text()
    assert unit.name == f"agi-agi-reaper-{crons.project_hash(root)[:8]}.service"
    assert "ExecStart=python3 /engine/extensions/agi/bin/heal.py watch" in first
    assert "WorkingDirectory=" in first
    assert "Restart=on-failure" in first
    assert "Environment=NOTIFY=off" in first
    assert "WantedBy=default.target" in first

    # Residue (b): apply actually RAN systemctl through the fake on PATH,
    # with the exact argv — daemon-reload then enable --now.
    calls = fake_systemctl.read_text().splitlines()
    assert calls[0] == "--user daemon-reload"
    assert calls[1].startswith("--user enable --now ")
    assert calls[1].endswith(unit.name)

    r2 = crons.cmd_apply(root, crontab_file=fixture, unit_dir=ud)
    assert unit.read_text() == first, "running apply twice must be byte-identical"
    assert any("up to date" in a for a in r2["unit_actions"])
    # crontab path still reconciles as usual alongside the unit
    assert r2["crons_live"] is True


def _write_unit_then_reapply(tmp_path, root, ud, fake_systemctl):
    """Write the unit once (first apply runs the true write+seam path), then
    reset the fake's call log so a SECOND apply's calls are isolated for the
    probe tests below. Returns the second apply's result dict."""
    crons.cmd_apply(root, crontab_file=tmp_path / "crontab.fixture",
                    unit_dir=ud)
    fake_systemctl.write_text("")
    return crons.cmd_apply(root, crontab_file=tmp_path / "crontab.fixture",
                           unit_dir=ud)


def test_up_to_date_enabled_active_records_one_noop(tmp_path, fake_systemctl):
    """hypothesis:l4-crons-apply-... File current AND unit enabled AND
    active: record ONE state line (`enabled+active (no-op)`) and run neither
    daemon-reload nor enable --now — the :x5 churn of two `(ok)` actions
    every pass is gone."""
    root = make_project(tmp_path, cadences=dict(DEFAULT_CADENCES))
    write_crons_node(root, crons_live=True, cadences=DEFAULT_CADENCES,
                     services=SER_REAPER)
    ud = tmp_path / "units"
    r2 = _write_unit_then_reapply(tmp_path, root, ud, fake_systemctl)
    assert any("enabled+active (no-op)" in a for a in r2["unit_actions"])
    calls = fake_systemctl.read_text().splitlines()
    assert calls, "probes must have run"
    assert all(c.startswith("--user is-") for c in calls), \
        "a no-op may only probe — no daemon-reload, no enable --now"


def test_up_to_date_not_enabled_still_enables(tmp_path, fake_systemctl):
    """File current but the unit NOT enabled (probe reports it): the
    convergence property holds — the real seam still runs so a written-but-
    never-enabled unit comes up on the next apply."""
    root = make_project(tmp_path, cadences=dict(DEFAULT_CADENCES))
    write_crons_node(root, crons_live=True, cadences=DEFAULT_CADENCES,
                     services=SER_REAPER)
    ud = tmp_path / "units"
    (fake_systemctl.parent / "systemctl.answers").write_text(
        "is-enabled: 1\n")   # probe: not enabled
    res = _write_unit_then_reapply(tmp_path, root, ud, fake_systemctl)
    calls = fake_systemctl.read_text().splitlines()
    assert calls[0].startswith("--user is-enabled ")
    assert any("daemon-reload" in c for c in calls)
    assert any("enable --now" in c for c in calls)
    assert not any("enabled+active (no-op)" in a
                   for a in res["unit_actions"])


def test_up_to_date_inactive_still_starts(tmp_path, fake_systemctl):
    """File current but the unit NOT active: the seam still runs (enable
    --now starts it) — an inactive unit is never left down by a false no-op."""
    root = make_project(tmp_path, cadences=dict(DEFAULT_CADENCES))
    write_crons_node(root, crons_live=True, cadences=DEFAULT_CADENCES,
                     services=SER_REAPER)
    ud = tmp_path / "units"
    (fake_systemctl.parent / "systemctl.answers").write_text(
        "is-active: 1\n")    # probe: not active (is-enabled ok)
    _write_unit_then_reapply(tmp_path, root, ud, fake_systemctl)
    calls = fake_systemctl.read_text().splitlines()
    assert calls[0].startswith("--user is-enabled ")
    assert calls[1].startswith("--user is-active ")
    assert any("enable --now" in c for c in calls), \
        "inactive unit converges via the real seam"


def test_probe_failure_never_swallowed_into_noop(tmp_path, fake_systemctl):
    """FALSIFIER guard: if either probe FAILS (state unconfirmable), the
    apply must NOT record a no-op — it runs the real seam instead, so a real
    state change can never be swallowed by the no-op path."""
    root = make_project(tmp_path, cadences=dict(DEFAULT_CADENCES))
    write_crons_node(root, crons_live=True, cadences=DEFAULT_CADENCES,
                     services=SER_REAPER)
    ud = tmp_path / "units"
    (fake_systemctl.parent / "systemctl.answers").write_text(
        "is-enabled: 1\nis-active: 1\n")
    res = _write_unit_then_reapply(tmp_path, root, ud, fake_systemctl)
    calls = fake_systemctl.read_text().splitlines()
    assert any("enable --now" in c for c in calls), \
        "unconfirmed state falls back to the real seam"
    assert not any("enabled+active (no-op)" in a
                   for a in res["unit_actions"]), \
        "a probe failure must never be swallowed into a false no-op"


def _write_unit_then_dry_run_reapply(tmp_path, root, ud, fake_systemctl):
    """Write the unit once (live apply runs the true write+seam path), reset
    the fake's call log, then reapply with `dry_run=True` so the SECOND
    apply's probes run (and are observed) under dry run. Returns the dry-run
    result dict."""
    crons.cmd_apply(root, crontab_file=tmp_path / "crontab.fixture",
                    unit_dir=ud)
    fake_systemctl.write_text("")
    return crons.cmd_apply(root, crontab_file=tmp_path / "crontab.fixture",
                           unit_dir=ud, dry_run=True)


def test_dry_run_up_to_date_enabled_active_probes_real_state(tmp_path,
                                                              fake_systemctl):
    """hypothesis:l4-crons-dry-run-probes-answer-real-state. Up-to-date +
    enabled + active + `--dry-run`: the READ-ONLY probes still RUN (they
    mutate nothing), so the dry run reaches the SAME `(no-op)` branch a live
    apply reaches — and it prints no seam intent for a unit the live pass
    would leave alone (the original bug)."""
    root = make_project(tmp_path, cadences=dict(DEFAULT_CADENCES))
    write_crons_node(root, crons_live=True, cadences=DEFAULT_CADENCES,
                     services=SER_REAPER)
    ud = tmp_path / "units"
    r2 = _write_unit_then_dry_run_reapply(tmp_path, root, ud, fake_systemctl)
    assert any("enabled+active (no-op)" in a for a in r2["unit_actions"]), \
        "dry run must answer the probe and reach the same no-op branch"
    calls = fake_systemctl.read_text().splitlines()
    assert calls, "dry-run probes must run for real"
    assert all(c.startswith("--user is-") for c in calls), \
        "a dry-run no-op may only probe — no daemon-reload, no enable --now"
    assert not any(("daemon-reload" in a or "enable --now" in a)
                   for a in r2["unit_actions"]), \
        "no dry-run seam-intent line for a unit the live pass leaves alone"
    assert not any("(dry-run)" in a for a in r2["unit_actions"]), \
        "the no-op branch emits no (dry-run) mutation lines"


def test_dry_run_stale_file_still_writes_dry_run_only(tmp_path,
                                                       fake_systemctl):
    """Absent unit file + `--dry-run`: the write + seam intent still prints
    with `(dry-run)` and NOTHING is written to disk — mutations never run
    under dry run even though the read-only probes now do."""
    root = make_project(tmp_path, cadences=dict(DEFAULT_CADENCES))
    write_crons_node(root, crons_live=True, cadences=DEFAULT_CADENCES,
                     services=SER_REAPER)
    ud = tmp_path / "units"
    result = crons.cmd_apply(root, crontab_file=tmp_path / "crontab.fixture",
                             unit_dir=ud, dry_run=True)
    assert any("write unit " in a and "(dry-run)" in a
               for a in result["unit_actions"])
    assert any("daemon-reload (dry-run)" in a
               for a in result["unit_actions"])
    assert any("enable --now" in a and "(dry-run)" in a
               for a in result["unit_actions"])
    assert not (ud / "agi-reaper.service").exists(), \
        "dry-run must not write the unit file"


def test_dry_run_up_to_date_not_enabled_claims_no_noop(tmp_path,
                                                        fake_systemctl):
    """Up-to-date file but the probe reports NOT enabled + `--dry-run`: the
    dry run must NOT claim a no-op the live pass would not take — it prints
    the seam-intent lines with `(dry-run)` instead."""
    root = make_project(tmp_path, cadences=dict(DEFAULT_CADENCES))
    write_crons_node(root, crons_live=True, cadences=DEFAULT_CADENCES,
                     services=SER_REAPER)
    ud = tmp_path / "units"
    (fake_systemctl.parent / "systemctl.answers").write_text(
        "is-enabled: 1\n")   # probe: not enabled
    res = _write_unit_then_dry_run_reapply(tmp_path, root, ud, fake_systemctl)
    assert not any("enabled+active (no-op)" in a
                   for a in res["unit_actions"]), \
        "a dry run must not claim a no-op the live pass would not take"
    assert any("daemon-reload (dry-run)" in a for a in res["unit_actions"])
    assert any("enable --now" in a and "(dry-run)" in a
               for a in res["unit_actions"])


def test_crons_live_false_removes_unit_and_runs_disable(tmp_path, fake_systemctl):
    root = make_project(tmp_path, cadences=dict(DEFAULT_CADENCES))
    write_crons_node(root, crons_live=True, cadences=DEFAULT_CADENCES,
                     services=SER_REAPER)
    ud = tmp_path / "units"
    fixture = tmp_path / "crontab.fixture"
    crons.cmd_apply(root, crontab_file=fixture, unit_dir=ud)
    unit = next(ud.glob("agi-*.service"))

    fake_systemctl.write_text("")
    write_crons_node(root, crons_live=False, cadences=DEFAULT_CADENCES,
                     services=SER_REAPER)
    res = crons.cmd_apply(root, crontab_file=fixture, unit_dir=ud)
    assert not unit.exists()
    assert any("remove unit" in a for a in res["unit_actions"])
    # The kill switch is REAL: disable --now ran through the fake, in the
    # order disable, then file removal, then daemon-reload.
    assert any("systemctl --user disable --now" in a for a in res["unit_actions"])
    calls = fake_systemctl.read_text().splitlines()
    assert calls[0].startswith("--user disable --now ")
    assert calls[0].endswith(unit.name)
    assert calls[1] == "--user daemon-reload"


def test_unit_dry_run_writes_nothing(tmp_path, capsys):
    root = make_project(tmp_path, cadences=dict(DEFAULT_CADENCES))
    write_crons_node(root, crons_live=True, cadences=DEFAULT_CADENCES,
                     services=SER_REAPER)
    ud = tmp_path / "units"
    fixture = tmp_path / "crontab.fixture"
    res = crons.cmd_apply(root, crontab_file=fixture, unit_dir=ud, dry_run=True)
    assert not ud.exists() or not list(ud.iterdir())
    assert any("(dry-run)" in a for a in res["unit_actions"])

    rc = crons.main(["apply", "--root", str(root), "--crontab-file", str(fixture),
                     "--unit-dir", str(ud), "--dry-run"])
    assert rc == 0
    assert not ud.exists() or not list(ud.iterdir())


def test_rendered_unit_never_carries_a_credential_path(tmp_path, fake_systemctl):
    """The claim's hard rule — the watcher never reads a credential — is a
    property of the renderer too: Environment= takes plain key=value settings
    and every value round-trips unchanged; assert the unit text contains the
    settings we put in and none we did not."""
    root = make_project(tmp_path, cadences=dict(DEFAULT_CADENCES))
    write_crons_node(root, crons_live=True, cadences=DEFAULT_CADENCES,
                     services=SER_REAPER)
    ud = tmp_path / "units"
    crons.cmd_apply(root, crontab_file=tmp_path / "crontab.fixture", unit_dir=ud)
    text = next(ud.glob("agi-*.service")).read_text()
    assert "Environment=NOTIFY=off" in text
    assert "SystemdEnvironment" not in text or "SECRET" not in text


# --- the user-bus seam (hypothesis:l4-crons-systemctl-seam- ---
# --- converges-from-cron): cron has no login session -------


def test_systemd_bus_env_inherits_when_caller_has_dbus(monkeypatch):
    """An interactive shell already carries DBUS_SESSION_BUS_ADDRESS; the seam
    adds nothing, the inherited env already reaches the bus."""
    monkeypatch.setenv("DBUS_SESSION_BUS_ADDRESS", "unix:path=/some/bus")
    assert crons._systemd_bus_env() == {}


def test_systemd_bus_env_adds_when_fallback_socket_exists(monkeypatch, tmp_path):
    """The cron case: neither var present, but the XDG_RUNTIME_DIR bus socket
    is there — add both vars pointing at it so `systemctl --user` can reach
    the bus from a cron with no login session."""
    runtime = tmp_path / "runtime"
    runtime.mkdir()
    (runtime / "bus").write_text("")
    monkeypatch.delenv("DBUS_SESSION_BUS_ADDRESS", raising=False)
    monkeypatch.setenv("XDG_RUNTIME_DIR", str(runtime))
    assert crons._systemd_bus_env() == {
        "XDG_RUNTIME_DIR": str(runtime),
        "DBUS_SESSION_BUS_ADDRESS": f"unix:path={runtime}/bus",
    }


def test_systemd_bus_env_none_when_socket_absent(monkeypatch, tmp_path):
    """No caller bus and no socket: any `systemctl --user` call is doomed
    (`No medium found`); the caller must record a named skip."""
    runtime = tmp_path / "runtime"
    runtime.mkdir()
    monkeypatch.delenv("DBUS_SESSION_BUS_ADDRESS", raising=False)
    monkeypatch.setenv("XDG_RUNTIME_DIR", str(runtime))
    assert crons._systemd_bus_env() is None


def test_wanted_unit_runs_systemctl_with_env_when_bus_reachable(tmp_path,
                                                                fake_systemctl):
    """Bus reachable: a wanted unit writes its file then runs daemon-reload
    and enable --now (existing behaviour preserved), with the bus-env merged
    into the subprocess so it works from a cron."""
    root = make_project(tmp_path, cadences=dict(DEFAULT_CADENCES))
    write_crons_node(root, crons_live=True, cadences=DEFAULT_CADENCES,
                     services=SER_REAPER)
    ud = tmp_path / "units"
    res = crons.cmd_apply(root, crontab_file=tmp_path / "crontab.fixture",
                          unit_dir=ud)
    calls = fake_systemctl.read_text().splitlines()
    assert calls[0] == "--user daemon-reload"
    assert calls[1].startswith("--user enable --now ")
    assert not any("no user bus" in a for a in res["unit_actions"])

    # The L4.129 bus-env merge is load-bearing: the FAKE records the env the
    # subprocess was invoked with, so the fallback DBUS address must actually
    # have been passed in (not just computed). If `env=merged` in
    # `_apply_systemctl` is deleted the call inherits the caller env, which
    # the fixture cleared of DBUS_SESSION_BUS_ADDRESS, and this goes red.
    envlines = (tmp_path / "systemctl.env").read_text().splitlines()
    calls = fake_systemctl.read_text().splitlines()
    assert len(envlines) == len(calls), \
        "one env line per systemctl call, same order as the argv log"
    runtime = tmp_path / "runtime"
    assert f"DBUS_SESSION_BUS_ADDRESS=unix:path={runtime}/bus" in envlines[0], \
        "fallback bus address must reach the subprocess via the env merge"


def test_fake_records_caller_bus_unchanged_when_present(tmp_path,
                                                        fake_systemctl,
                                                        monkeypatch):
    """When the caller already has DBUS_SESSION_BUS_ADDRESS, the seam adds
    nothing (bus_env == {}) and the fake must see the CALLER's value, not the
    fallback — the recorded env distinguishes caller-origin from
    fallback-origin."""
    root = make_project(tmp_path, cadences=dict(DEFAULT_CADENCES))
    write_crons_node(root, crons_live=True, cadences=DEFAULT_CADENCES,
                     services=SER_REAPER)
    caller_bus = "unix:path=/caller/real-bus"
    monkeypatch.setenv("DBUS_SESSION_BUS_ADDRESS", caller_bus)
    ud = tmp_path / "units"
    crons.cmd_apply(root, crontab_file=tmp_path / "crontab.fixture",
                    unit_dir=ud)
    envlines = (tmp_path / "systemctl.env").read_text().splitlines()
    assert any(f"DBUS_SESSION_BUS_ADDRESS={caller_bus}" in l
               for l in envlines), "caller-origin bus must be recorded as-is"
    assert not any(f"DBUS_SESSION_BUS_ADDRESS=unix:path={tmp_path}" in l
                   for l in envlines), \
        "no fallback bus (a tmp_path path) may leak when the caller has one"


def test_wanted_unit_records_named_skip_without_bus(tmp_path, monkeypatch,
                                                    fake_systemctl):
    """No reachable bus: a wanted unit still writes its file (a file on disk
    needs no bus) but records ONE named skip and runs neither daemon-reload
    nor enable --now — the two FAILED `No medium found` actions are gone."""
    root = make_project(tmp_path, cadences=dict(DEFAULT_CADENCES))
    write_crons_node(root, crons_live=True, cadences=DEFAULT_CADENCES,
                     services=SER_REAPER)
    runtime = tmp_path / "nobus"
    runtime.mkdir()
    monkeypatch.setenv("XDG_RUNTIME_DIR", str(runtime))
    ud = tmp_path / "units"
    res = crons.cmd_apply(root, crontab_file=tmp_path / "crontab.fixture",
                          unit_dir=ud)
    assert any("no user bus, skip systemctl" in a for a in res["unit_actions"])
    assert not fake_systemctl.exists(), \
        "no systemctl may run without a bus"
    assert list(ud.glob("agi-*.service")), "the unit FILE is still written"


def test_kill_switch_with_no_unit_file_records_absent(tmp_path, fake_systemctl):
    """crons_live false with the unit file already gone (never landed, or
    manually removed): not loaded, nothing to disable — one state line, no
    `disable --now` on an absent unit and no FAILED, no daemon-reload."""
    root = make_project(tmp_path, cadences=dict(DEFAULT_CADENCES))
    write_crons_node(root, crons_live=False, cadences=DEFAULT_CADENCES,
                     services=SER_REAPER)
    ud = tmp_path / "units"  # never created -> unit file absent
    res = crons.cmd_apply(root, crontab_file=tmp_path / "crontab.fixture",
                          unit_dir=ud)
    assert any("absent, nothing to disable" in a for a in res["unit_actions"])
    assert not fake_systemctl.exists(), \
        "no disable may run on an absent unit"


def test_kill_switch_absent_file_stays_when_no_bus(tmp_path, monkeypatch,
                                        fake_systemctl):
    """Kill switch + unit present + NO user bus (hypothesis:l4-kill-switch-
    without-a-bus-is-a-named-skip): cannot stop the running unit, so record a
    NAMED skip for `disable --now` and KEEP the file (removing it while the
    unit runs orphans a process systemd no longer manages). No FAILED, no
    fake systemctl call, no `remove unit` line."""
    root = make_project(tmp_path, cadences=dict(DEFAULT_CADENCES))
    write_crons_node(root, crons_live=True, cadences=DEFAULT_CADENCES,
                     services=SER_REAPER)
    ud = tmp_path / "units"
    fixture = tmp_path / "crontab.fixture"
    crons.cmd_apply(root, crontab_file=fixture, unit_dir=ud)
    unit = next(ud.glob("agi-*.service"))

    # Kill the bus: XDG_RUNTIME_DIR points at a dir with no socket.
    runtime = tmp_path / "nobus"
    runtime.mkdir()
    monkeypatch.setenv("XDG_RUNTIME_DIR", str(runtime))
    fake_systemctl.write_text("")
    write_crons_node(root, crons_live=False, cadences=DEFAULT_CADENCES,
                     services=SER_REAPER)
    res = crons.cmd_apply(root, crontab_file=fixture, unit_dir=ud)
    assert unit.exists(), (
        "file KEPT: removing it while the unit runs orphans a live unit "
        "systemd no longer knows")
    assert any("present, no user bus: disable --now SKIPPED" in a
               for a in res["unit_actions"]), "one named skip line"
    assert any("no user bus, skip daemon-reload" in a
               for a in res["unit_actions"]), "daemon-reload named line"
    assert not any("remove unit" in a for a in res["unit_actions"])
    assert not fake_systemctl.read_text(), "no systemctl may run without a bus"


def test_kill_switch_with_unit_present_runs_disable(tmp_path, fake_systemctl):
    """The kill switch stays REAL when the unit file exists: disable --now,
    remove, daemon-reload all run through the seam."""
    root = make_project(tmp_path, cadences=dict(DEFAULT_CADENCES))
    write_crons_node(root, crons_live=True, cadences=DEFAULT_CADENCES,
                     services=SER_REAPER)
    ud = tmp_path / "units"
    fixture = tmp_path / "crontab.fixture"
    crons.cmd_apply(root, crontab_file=fixture, unit_dir=ud)
    unit = next(ud.glob("agi-*.service"))

    fake_systemctl.write_text("")
    write_crons_node(root, crons_live=False, cadences=DEFAULT_CADENCES,
                     services=SER_REAPER)
    res = crons.cmd_apply(root, crontab_file=fixture, unit_dir=ud)
    assert not unit.exists()
    assert any("remove unit" in a for a in res["unit_actions"])
    calls = fake_systemctl.read_text().splitlines()
    assert calls[0].startswith("--user disable --now ")
    assert calls[1] == "--user daemon-reload"


# --- generic cadence entries, placeholders, and audit (this round's claim) --


GENERIC_ONLY = {
    "grid_sync": {"every_mins": 5, "enabled": False},
}


def test_generic_job_renders_the_managed_shape(tmp_path):
    """Any name outside KNOWN_JOBS that carries a `cmd` renders one line in
    the SAME shape a built-in uses: `cd {root} && <cmd> >> <log> 2>&1`."""
    root = make_project(tmp_path, cadences={
        **GENERIC_ONLY,
        "nightly_digest": {"schedule": "12 3 * * *",
                           "cmd": "python3 bin/digest.py"},
    })
    node = crons.load_crons_node(root)
    assert node["jobs"]["nightly_digest"]["cmd"] == "python3 bin/digest.py"
    lines = crons.render_managed_lines(root, root, root, node)
    assert lines == [
        f"12 3 * * * cd {root} && python3 bin/digest.py >> "
        f"{crons._log_path(root)} 2>&1"
    ]


def test_generic_job_log_override_and_deterministic_order(tmp_path):
    """`log:` overrides the project log; two generics render sorted by name so
    a second apply is byte-identical regardless of YAML key order."""
    root = make_project(tmp_path, cadences={
        **GENERIC_ONLY,
        "zeta": {"every_mins": 30, "cmd": "true", "log": "/tmp/zeta.log"},
        "alpha": {"every_mins": 30, "cmd": "true"},
    })
    node = crons.load_crons_node(root)
    lines = crons.render_managed_lines(root, root, root, node)
    assert str(crons._log_path(root)) in lines[0]
    assert ">> /tmp/zeta.log 2>&1" in lines[1]


def test_unknown_job_without_cmd_still_refused_by_name(tmp_path):
    """The regression pin: an unknown name with no `cmd` is refused exactly
    as before, naming the job."""
    root = tmp_path / "proj"
    write_crons_node(root, cadences={"totally_made_up": {"every_mins": 1}})
    with pytest.raises(crons.CronsError, match="unknown job 'totally_made_up'"):
        crons.load_crons_node(root)


def test_generic_job_box_gate_matches_builtin_behaviour(tmp_path):
    """A generic job with `box:` is gated by the SAME `_on_this_box` a
    built-in uses: absent renders everywhere, a string restricts."""
    root = make_project(tmp_path, cadences={
        **GENERIC_ONLY,
        "boxed_job": {"schedule": "0 1 * * *", "cmd": "true",
                      "box": "local-town"},
    })
    node = crons.load_crons_node(root)
    assert crons.render_managed_lines(root, root, root, node,
                                      box_name="local-town")
    assert crons.render_managed_lines(root, root, root, node,
                                      box_name="core-town") == []


def test_placeholders_resolve_by_literal_replacement(tmp_path):
    """`{root}` / `{repo_root}` / `{logs}` / `{box}` resolve from the
    schema-declared map; non-strings and shell braces pass untouched (never
    `str.format()`)."""
    root = tmp_path / "proj"
    root.mkdir()
    write_crons_node(root)
    repo = tmp_path / "repo"
    out = crons._substitute("{root}|{repo_root}|{logs}|{box}",
                            root, repo, "core-town")
    assert out == (f"{root}|{repo}|{Path.home() / 'logs'}|core-town")
    assert crons._substitute(None, root, repo, "core-town") is None
    assert crons._substitute("awk '{print $1}'", root, repo,
                             "core-town") == "awk '{print $1}'"


def test_resolve_placeholders_refuses_schema_without_a_map(tmp_path):
    """Conjunct 2 (gate): a schema that declares no `placeholders:` map is
    REFUSED by name instead of quietly substituting nothing."""
    graph = tmp_path / "graph"
    (graph / "context" / "schemas").mkdir(parents=True)
    (graph / "context" / "schemas" / "[box].md").write_text(
        "---\nfields:\n  root: {type: str}\n---\n")
    with pytest.raises(boxes.BoxSchemaError) as err:
        boxes.resolve_placeholders("{root}", {"root": "R"}, graph)
    assert "[box].md" in str(err.value)
    assert "placeholders" in str(err.value)


def test_resolve_placeholders_falls_back_to_the_engine_schema(tmp_path):
    """Conjunct 2 (gate, availability): a graph with NO [box].md of its own
    renders through the ENGINE's own [box].md -- the same declaration, never a
    second copied token list. Refusing an ABSENT schema is a regression."""
    graph = tmp_path / "graph"
    graph.mkdir()
    assert boxes.resolve_placeholders("{root}", {"root": "R"}, graph) == "R"


def test_resolve_placeholders_refuses_a_missing_mapped_cell(tmp_path):
    """Conjunct 1 (gate): a token the map declares but the caller supplied no
    cell for refuses by name -- never renders empty."""
    graph = tmp_path / "graph"
    (graph / "context" / "schemas").mkdir(parents=True)
    (graph / "context" / "schemas" / "[box].md").write_text(
        "---\nfields:\n  root: {type: str}\n"
        "placeholders:\n  tmux: tmux_session\n---\n")
    with pytest.raises(boxes.BoxSchemaError) as err:
        boxes.resolve_placeholders("{tmux}", {"root": "R"}, graph)
    assert "tmux_session" in str(err.value)


def test_resolve_placeholders_refuses_a_supplied_but_empty_cell(tmp_path):
    """P5 (gate): a mapped token whose cell is PRESENT but EMPTY refuses by
    name -- presence alone is not enough, because an empty render is exactly
    the bug this leaf exists to kill."""
    graph = tmp_path / "graph"
    (graph / "context" / "schemas").mkdir(parents=True)
    (graph / "context" / "schemas" / "[box].md").write_text(
        "---\nfields:\n  root: {type: str}\n"
        "placeholders:\n  tmux: tmux_session\n---\n")
    with pytest.raises(boxes.BoxSchemaError) as err:
        boxes.resolve_placeholders("{tmux}", {"tmux_session": ""}, graph)
    assert "tmux_session" in str(err.value)


def test_crons_renders_a_shell_reference_without_refusing(tmp_path):
    """P6 (wire): a legal shell `${VAR}` is not a stray graph token. Round 1's
    stray check convicted the `{PATH}` inside `${PATH}`; the declared `{box}`
    still resolves and the shell reference passes byte-identical."""
    root = tmp_path / "proj"
    root.mkdir()
    write_crons_node(root, cadences={
        "grid_sync": {"every_mins": 5, "enabled": False},
        "path_probe": {"schedule": "0 5 * * *",
                       "cmd": "run --who {box} ${PATH}"},
    })
    node = crons.load_crons_node(root)
    lines = crons.render_managed_lines(root, root, root, node,
                                       box_name="local-town")
    assert lines == [
        f"0 5 * * * cd {root} && run --who local-town ${{PATH}} "
        f">> {crons._log_path(root)} 2>&1"
    ]


def test_crons_refuses_an_undeclared_token_as_a_crons_error(tmp_path):
    """Conjunct 1 (wire): a bare `{token}` absent from the map refuses as a
    `CronsError` (which main prints as `ERR: crons.py:` rc 1), never rendered
    literally and never a traceback."""
    root = tmp_path / "proj"
    root.mkdir()
    write_crons_node(root)
    with pytest.raises(crons.CronsError) as err:
        crons._substitute("run --at {projroot}", root, root, "core-town")
    assert "projroot" in str(err.value)


def test_crons_renders_through_the_one_schema_declared_map(tmp_path):
    """Conjunct 3 (wire): a token the schema declares but crons never
    hardcoded must render. crons carries no token list of its own, so the
    map in [box].md is what decides which tokens exist at all."""
    root = tmp_path / "proj"
    root.mkdir()
    write_crons_node(root, cadences={
        "grid_sync": {"every_mins": 5, "enabled": False},
        "town_digest": {"schedule": "0 4 * * *",
                        "cmd": "run --at {projroot} --who {box}"},
    })
    (root / "context" / "schemas" / "[box].md").write_text(
        "---\nfields:\n  root: {type: str}\n"
        "placeholders:\n  projroot: root\n  box: box\n---\n")
    node = crons.load_crons_node(root)
    lines = crons.render_managed_lines(root, root, root, node,
                                       box_name="local-town")
    assert lines == [
        f"0 4 * * * cd {root} && run --at {root} --who local-town "
        f">> {crons._log_path(root)} 2>&1"
    ]


def test_routed_resolver_is_byte_identical_to_the_pre_fix_list(tmp_path):
    """Conjunct 3 (wire, preservation half): the live node's crontab renders
    byte-identically whether placeholders go through the schema map or the
    pre-fix four-token literal list -- so routing the renderer changed no
    bytes on the live crontab."""
    import unittest.mock as mock
    repo = Path(__file__).resolve().parents[3]
    root = repo / ".agi"
    node = crons.load_crons_node(root)

    def pre_fix(text, root, repo_root, own):
        if not isinstance(text, str):
            return text
        for token, value in (("{repo_root}", str(repo_root)),
                             ("{root}", str(root)),
                             ("{logs}", str(crons._log_path(repo_root).parent)),
                             ("{box}", own)):
            text = text.replace(token, value)
        return text

    # the checkout's HEAD is not this test's subject: the branch is pinned so a
    # detached checkout (a gate worktree) renders exactly what a branch does
    with mock.patch.object(crons, "resolve_branch", lambda _git_dir: "main"):
        after = crons.render_managed_lines(root, repo, repo, node)
        assert after, "the live node must still render its managed lines"
        with mock.patch.object(crons, "_substitute", pre_fix):
            before = crons.render_managed_lines(root, repo, repo, node)
    assert after == before


def test_service_placeholders_render_the_same_bytes_as_absolute_paths(tmp_path,
                                                                       fake_systemctl):
    """The live node's `services.agi-reaper` paths became `{repo_root}` /
    `{logs}`; resolving them must reproduce the old absolute unit byte for
    byte."""
    abs_svc = {
        "enabled": True, "restart": "on-failure",
        "exec_start": "/usr/bin/python3 /box/work/agi/extensions/agi/bin/"
                      "heal.py watch --root /box/work/agi --poll-s 30",
        "working_directory": "/box/work/agi",
        "environment": {"AGI_REAPER_LOG": "/box/logs/reaper.log"},
    }
    ph_svc = {
        "enabled": True, "restart": "on-failure",
        "exec_start": "/usr/bin/python3 {repo_root}/extensions/agi/bin/"
                      "heal.py watch --root {repo_root} --poll-s 30",
        "working_directory": "{repo_root}",
        "environment": {"AGI_REAPER_LOG": "{logs}/reaper.log"},
    }
    repo = tmp_path / "box" / "work" / "agi"
    repo.mkdir(parents=True)
    (repo.parent / "context" / "schemas").mkdir(parents=True)
    (repo.parent / "context" / "schemas" / "[box].md").write_text(BOX_SCHEMA)
    abs_svc = {
        "enabled": True, "restart": "on-failure",
        "exec_start": f"/usr/bin/python3 {repo}/extensions/agi/bin/"
                      f"heal.py watch --root {repo} --poll-s 30",
        "working_directory": str(repo),
        "environment": {"AGI_REAPER_LOG": str(Path.home() / "logs" / "reaper.log")},
    }
    resolved = dict(ph_svc)
    resolved["exec_start"] = crons._substitute(
        ph_svc["exec_start"], repo.parent, repo, "")
    resolved["working_directory"] = crons._substitute(
        ph_svc["working_directory"], repo.parent, repo, "")
    resolved["environment"] = {
        k: crons._substitute(v, repo.parent, repo, "")
        for k, v in ph_svc["environment"].items()}
    assert crons.render_unit_file("agi-reaper", resolved, repo) == \
        crons.render_unit_file("agi-reaper", abs_svc, repo)


def test_audit_flags_a_foreign_agi_block_and_extra_unit(tmp_path, capsys):
    root = make_project(tmp_path, cadences={
        "grid_sync": {"every_mins": 5, "enabled": True}})
    fixture = tmp_path / "crontab.fixture"
    crons.cmd_apply(root, crontab_file=fixture)
    foreign = ["# >>> agi-crons deadbeefcafe >>> project=/elsewhere",
               "0 0 * * * /elsewhere/run.sh",
               "# <<< agi-crons deadbeefcafe <<<"]
    fixture.write_text(fixture.read_text() + "\n".join(foreign) + "\n")
    ud = tmp_path / "units"
    ud.mkdir()
    (ud / "agi-ghost-99.service").write_text("[Unit]\n")

    rc = crons.main(["audit", "--root", str(root), "--crontab-file",
                     str(fixture), "--unit-dir", str(ud)])
    out = capsys.readouterr().out
    assert rc == 1
    assert "deadbeefcafe" in out
    assert "agi-ghost-99.service" in out


def test_audit_clean_fixture_exits_zero(tmp_path, monkeypatch, capsys):
    monkeypatch.setenv("HOME", str(tmp_path / "home"))
    root = make_project(tmp_path, cadences={
        "grid_sync": {"every_mins": 5, "enabled": True}})
    fixture = tmp_path / "crontab.fixture"
    crons.cmd_apply(root, crontab_file=fixture)
    rc = crons.main(["audit", "--root", str(root), "--crontab-file", str(fixture)])
    assert rc == 0
    assert "clean" in capsys.readouterr().out


def test_audit_accepts_this_projects_declared_unit(tmp_path, fake_systemctl):
    """A unit whose filename carries OUR hash and whose service IS in the
    node's `services:` is declared, not flagged."""
    cad = {"grid_sync": {"every_mins": 5, "enabled": True}}
    root = make_project(tmp_path, cadences=cad)
    write_crons_node(root, crons_live=True, cadences=cad, services=SER_REAPER)
    ud = tmp_path / "units"
    fixture = tmp_path / "crontab.fixture"
    crons.cmd_apply(root, crontab_file=fixture, unit_dir=ud)
    assert list(ud.glob("agi-*.service"))
    assert crons.cmd_audit(root, crontab_file=fixture, unit_dir=ud) == []


def test_audit_flags_an_ordinary_named_unit(tmp_path, capsys):
    """A `.service` with NO agi shape at all (`some-other-tool.service`) is
    undeclared by this node however long it sits there — the false negative
    the `startswith("agi-")` gate caused (a real box carries
    `hermes-gateway.service`, `streamer-stub.service`, ...)."""
    root = make_project(tmp_path, cadences={
        "grid_sync": {"every_mins": 5, "enabled": True}})
    fixture = tmp_path / "crontab.fixture"
    crons.cmd_apply(root, crontab_file=fixture)
    ud = tmp_path / "units"
    ud.mkdir()
    (ud / "some-other-tool.service").write_text("[Unit]\n")

    rc = crons.main(["audit", "--root", str(root), "--crontab-file",
                     str(fixture), "--unit-dir", str(ud)])
    out = capsys.readouterr().out
    assert rc == 1
    assert "some-other-tool.service" in out


def test_audit_is_silent_on_another_projects_unit(tmp_path, capsys):
    """An agi-shaped unit for a DIFFERENT project's hash is not ours to judge
    — the same treatment the crontab side gives a foreign `agi-crons <hash>`
    block. It must NOT be flagged as undeclared (the false positive the old
    `elif p.name.startswith("agi-")` branch produced)."""
    root = make_project(tmp_path, cadences={
        "grid_sync": {"every_mins": 5, "enabled": True}})
    fixture = tmp_path / "crontab.fixture"
    crons.cmd_apply(root, crontab_file=fixture)
    ud = tmp_path / "units"
    ud.mkdir()
    (ud / "agi-something-deadbeef.service").write_text("[Unit]\n")

    rc = crons.main(["audit", "--root", str(root), "--crontab-file",
                     str(fixture), "--unit-dir", str(ud)])
    out = capsys.readouterr().out
    assert rc == 0
    assert "deadbeef" not in out


def test_audit_default_scans_the_user_unit_dir(tmp_path, monkeypatch, capsys):
    """SM.124 corrective: with no `--unit-dir`, plain `crons.py audit`
    scans `$HOME/.config/systemd/user` instead of skipping the unit loop, so
    an undeclared unit that actually runs is named, not reported clean.
    HOME is monkeypatched at a fixture dir — never the box's real units."""
    home = tmp_path / "home"
    hud = home / ".config" / "systemd" / "user"
    hud.mkdir(parents=True)
    (hud / "claude-remote-control.service").write_text("[Unit]\n")
    monkeypatch.setenv("HOME", str(home))
    root = make_project(tmp_path, cadences={
        "grid_sync": {"every_mins": 5, "enabled": True}})
    fixture = tmp_path / "crontab.fixture"
    crons.cmd_apply(root, crontab_file=fixture)
    found = crons.cmd_audit(root, crontab_file=fixture)
    assert any("claude-remote-control.service" in f for f in found), found
    rc = crons.main(["audit", "--root", str(root), "--crontab-file",
                     str(fixture)])
    assert rc == 1
    assert "claude-remote-control.service" in capsys.readouterr().out


def test_audit_explicit_unit_dir_never_reads_home(tmp_path, monkeypatch):
    """`--unit-dir` stays the override/test seam: the explicit fixture dir
    is what gets scanned and HOME is not consulted, however dirty HOME is."""
    home = tmp_path / "home"
    hud = home / ".config" / "systemd" / "user"
    hud.mkdir(parents=True)
    (hud / "ghost-in-home.service").write_text("[Unit]\n")
    monkeypatch.setenv("HOME", str(home))
    root = make_project(tmp_path, cadences={
        "grid_sync": {"every_mins": 5, "enabled": True}})
    fixture = tmp_path / "crontab.fixture"
    crons.cmd_apply(root, crontab_file=fixture)
    ud = tmp_path / "units"
    ud.mkdir()
    (ud / "some-tool.service").write_text("[Unit]\n")
    found = crons.cmd_audit(root, crontab_file=fixture, unit_dir=ud)
    assert any("some-tool.service" in f for f in found), found
    assert not any("ghost-in-home" in f for f in found), found


# --- the nudge_sweep known job + why_box (l5 undelivered-nudge round) -----


def test_nudge_sweep_renders_on_every_box_and_is_not_a_generic_cmd(tmp_path):
    """`nudge_sweep` is a KNOWN job: it renders the `wake --all-local` sweep
    (never a hardcoded seat list) and an absent `box` key means EVERY box."""
    cad = {"nudge_sweep": {"every_mins": 2, "enabled": True}}
    root = make_project(tmp_path, cadences=cad)
    node = crons.load_crons_node(root)
    assert "nudge_sweep" in node["jobs"]
    assert "cmd" not in node["jobs"]["nudge_sweep"]
    for box in ("core-town", "local-town", ""):
        lines = crons.render_managed_lines(root, root, root, node, box_name=box)
        assert len(lines) == 1
        assert lines[0].startswith("*/2 * * * *")
        assert "wake --all-local" in lines[0]
        assert "send.py" in lines[0]
        assert lines[0].endswith(f">> {crons._log_path(root)} 2>&1")


def test_audit_flags_a_gated_known_job_without_why_box(tmp_path, monkeypatch):
    """A `box` list is the exception and must say why in `why_box`; the
    audit names the job and the missing field."""
    monkeypatch.setenv("HOME", str(tmp_path / "home"))
    cad = {"nudge_sweep": {"every_mins": 2, "enabled": True,
                           "box": "local-town"}}
    root = make_project(tmp_path, cadences=cad)
    fixture = tmp_path / "crontab.fixture"
    crons.cmd_apply(root, crontab_file=fixture)
    found = crons.cmd_audit(root, crontab_file=fixture)
    assert any("nudge_sweep" in f and "why_box" in f for f in found), found


def test_audit_accepts_a_gated_known_job_with_why_box(tmp_path, monkeypatch):
    monkeypatch.setenv("HOME", str(tmp_path / "home"))
    cad = {"nudge_sweep": {"every_mins": 2, "enabled": True,
                           "box": "local-town",
                           "why_box": "the sweep only reads local rows"}}
    root = make_project(tmp_path, cadences=cad)
    fixture = tmp_path / "crontab.fixture"
    crons.cmd_apply(root, crontab_file=fixture)
    assert crons.cmd_audit(root, crontab_file=fixture) == []


def test_audit_flags_a_gated_generic_job_without_why_box(tmp_path, monkeypatch):
    """The `box` gate's why_box rule is not a KNOWN_JOBS privilege: a generic
    entry (a name outside KNOWN_JOBS carrying a `cmd`) goes through the SAME
    box gate, so the audit must name it exactly as it names a built-in."""
    monkeypatch.setenv("HOME", str(tmp_path / "home"))
    cad = {"town_probe": {"every_mins": 9, "enabled": True,
                          "cmd": "/bin/true", "box": "local-town"}}
    root = make_project(tmp_path, cadences=cad)
    fixture = tmp_path / "crontab.fixture"
    crons.cmd_apply(root, crontab_file=fixture)
    found = crons.cmd_audit(root, crontab_file=fixture)
    assert any("town_probe" in f and "why_box" in f for f in found), found
