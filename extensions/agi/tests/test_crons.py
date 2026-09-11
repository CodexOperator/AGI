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

import os
import subprocess
import sys
from pathlib import Path

import pytest
import yaml

BIN = Path(__file__).resolve().parents[1] / "bin"
sys.path.insert(0, str(BIN))

import crons  # noqa: E402


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
    script = bin / "systemctl"
    script.write_text(
        "#!/usr/bin/env bash\n"
        f'echo "$@" >> {log}\n'
        f'echo "XDG_RUNTIME_DIR=${{XDG_RUNTIME_DIR-}}|DBUS_SESSION_BUS_ADDRESS=${{DBUS_SESSION_BUS_ADDRESS-}}" >> {envlog}\n'
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
    root = make_project(tmp_path)
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
