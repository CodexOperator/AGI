"""E2a (goal:g7.16.1.11.13, hypothesis g716111-aa3-the-crontab-applier-survives-
grid-syncs-retirement, V3): retiring `grid_sync` must not lose the crontab
self-heal. Today the only line that runs `crons.py apply` is the TAIL of the
`grid_sync` line, so disabling grid_sync alone silently stops the heal. The
fix is ONE cell, `cadences.crons_apply` on cron:crons (0 engine bytes: a
generic `cmd` row already exists), that runs `crons.py apply` on its own.

Two groups. R = renderer pins over a fixture node (green today: they prove the
rendering a cell relies on, and each is paired with a one-edit mutant of
crons.py). L = the LIVE node: it must declare the cell, and the cell must
render, converge a hand-edited crontab and stop units, under a FAKE `crontab`
and a FAKE `systemctl` on PATH, never the real ones. L is RED until the cell
lands. The cell is BOXLESS (SM RE5/RE6): no `box` key, no `why_box`, so it
renders on any box including one with AGI_BOX unset and no default_box cell;
a BOXED cell is pinned only as the thing to avoid (R5/R6: the audit and the
CronsError safeguards). Override the units under test: CRONS_PY=<crons.py copy> (a mutant of
the renderer), CRONS_NODE=<crons.md copy> (a mutant of the cell); both default
to the checkout's own.
"""
from __future__ import annotations

import importlib.util
import os
import re
import shutil
import subprocess
import sys
from pathlib import Path

import pytest
import yaml

HERE = Path(__file__).resolve()
BIN = HERE.parents[1] / "bin"
REPO = HERE.parents[3]
sys.path.insert(0, str(BIN))

CRONS_PY = Path(os.environ.get("CRONS_PY") or BIN / "crons.py")
LIVE_NODE = Path(os.environ.get("CRONS_NODE")
                 or REPO / ".agi" / "nodes" / ".geometry" / "crons.md")
BOX_SCHEMA = REPO / ".agi" / "context" / "schemas" / "[box].md"

if CRONS_PY.resolve() == (BIN / "crons.py").resolve():
    import crons
else:
    _spec = importlib.util.spec_from_file_location("crons", CRONS_PY)
    crons = importlib.util.module_from_spec(_spec)
    sys.modules["crons"] = crons
    _spec.loader.exec_module(crons)

BOX = "local-town"
# The shape the brief names, as a SYNTHETIC cell for the renderer pins (R rows).
SYNTH_CELL = {   # BOXLESS: renders on every box, AGI_BOX unset included
    "every_mins": 5, "enabled": True,
    "cmd": "python3 {repo_root}/extensions/agi/bin/crons.py apply "
           "--unit-dir $HOME/.config/systemd/user",
}
BOXED_CELL = {**SYNTH_CELL, "box": BOX, "why_box": "the one crontab that exists is this box's"}
STANDALONE_CMD = re.compile(
    r"^python3 (?P<py>/\S+)/extensions/agi/bin/crons\.py apply "
    r"--unit-dir (?P<udir>\$HOME/\.config/systemd/user)$")


# --- fixtures ---


def _frontmatter(text: str) -> dict:
    return yaml.safe_load(text.split("---\n", 2)[1])


def _live_fm() -> dict:
    return _frontmatter(LIVE_NODE.read_text())


def _git(path: Path, *args: str) -> None:
    subprocess.run(["git", *args], cwd=path, check=True, capture_output=True)


def make_project(tmp_path: Path, fm: dict, name: str = "repo") -> Path:
    """The G11 layout the live checkout has: root = repo/.agi, repo_root =
    engine_root = repo, crons.py reachable at repo/extensions/agi/bin (a dir of
    symlinks to the real modules, crons.py being the unit under test)."""
    repo = tmp_path / name
    repo.mkdir(parents=True)
    _git(repo, "init", "-q", "-b", "master")
    _git(repo, "config", "user.email", "t@t")
    _git(repo, "config", "user.name", "t")
    root = repo / ".agi"
    (root / "nodes" / ".geometry").mkdir(parents=True)
    (root / "config.json").write_text("{}")
    (root / "nodes" / ".geometry" / "crons.md").write_text(
        "---\n" + yaml.safe_dump(fm, sort_keys=False) + "---\n\nBody.\n")
    schema = root / "context" / "schemas" / "[box].md"
    schema.parent.mkdir(parents=True)
    schema.write_text(BOX_SCHEMA.read_text())
    eb = repo / "extensions" / "agi" / "bin"
    eb.mkdir(parents=True)
    for p in BIN.iterdir():
        if p.is_file() and p.name != "crons.py":
            (eb / p.name).symlink_to(p)
    (eb / "crons.py").symlink_to(CRONS_PY.resolve())
    (repo / "k").write_text("x")
    _git(repo, "add", "k")
    _git(repo, "commit", "-qm", "init")
    return root


def fm_with(cell=None, grid_sync=None, live=True, drop_cell=False, services=False) -> dict:
    """The LIVE node's frontmatter, edited: `cell` replaces cadences.crons_apply,
    `drop_cell` removes it, `grid_sync` overrides its `enabled`."""
    fm = _live_fm()
    cad = fm.setdefault("cadences", {})
    if drop_cell:
        cad.pop("crons_apply", None)
    if cell is not None:
        cad["crons_apply"] = cell
    if grid_sync is not None:
        cad["grid_sync"]["enabled"] = grid_sync
    fm["crons_live"] = live
    if not services:
        fm.pop("services", None)
    return fm


def render(root: Path, box: str = BOX) -> list[str]:
    _, _, repo_root, engine_root, node = crons._resolve(root)
    return crons.render_managed_lines(root, repo_root, engine_root, node, box_name=box)


def is_apply_line(line: str) -> bool:
    return "crons.py apply" in line


def standalone(lines: list[str]) -> list[str]:
    """Lines whose WHOLE command is `crons.py apply` (not the tail of another job)."""
    out = []
    for ln in lines:
        parts = ln.split(" ", 5)
        if len(parts) < 6 or " && " not in parts[5]:
            continue
        cmd = re.sub(r" >> \S+ 2>&1$", "", parts[5].split(" && ", 1)[1])
        if re.match(r"^python3 \S+/crons\.py apply( |$)", cmd) and ";" not in cmd and "&&" not in cmd:
            out.append(ln)
    return out


def norm(lines: list[str], repo: Path) -> list[str]:
    """Lines with the project path and the per-project log name made equal."""
    return [re.sub(r"agi-crons-\S+?\.log", "LOG", l.replace(str(repo), "R")) for l in lines]


@pytest.fixture(autouse=True)
def _home(tmp_path, monkeypatch):
    h = tmp_path / "home"
    h.mkdir()
    monkeypatch.setenv("HOME", str(h))
    monkeypatch.delenv("AGI_BOX", raising=False)
    return h


@pytest.fixture
def fakes(tmp_path, monkeypatch):
    """A FAKE `crontab` (a file-backed table) and a FAKE `systemctl` first on
    PATH; returns (env for a cron-style run, table file, systemctl call log)."""
    fb = tmp_path / "fakebin"
    fb.mkdir()
    table, calls = tmp_path / "crontab.table", tmp_path / "systemctl.calls"
    (fb / "crontab").write_text(
        "#!/bin/sh\n"
        f'T={table}\n'
        'case "$1" in\n'
        '  -l) if [ -f "$T" ]; then cat "$T"; else echo "no crontab" >&2; exit 1; fi;;\n'
        '  -) cat > "$T";;\n'
        '  *) exit 2;;\n'
        'esac\n')
    (fb / "systemctl").write_text(f'#!/bin/sh\necho "$@" >> {calls}\nexit 0\n')
    for p in fb.iterdir():
        p.chmod(0o755)
    (Path(os.environ["HOME"]) / "logs").mkdir(exist_ok=True)   # a box that was applied once: the line's `>> ~/logs/..` needs the dir
    rt = tmp_path / "runtime"
    rt.mkdir()
    (rt / "bus").write_text("")
    env = {"PATH": f"{fb}:/usr/bin:/bin", "HOME": os.environ["HOME"],
           "XDG_RUNTIME_DIR": str(rt),   # NO AGI_BOX: the boxless cell must work on a box that cannot name itself
           "GIT_CONFIG_GLOBAL": "/dev/null", "GIT_CONFIG_SYSTEM": "/dev/null",
           "PYTHONPATH": str(BIN)}   # a CRONS_PY copy outside bin/ still finds its sibling modules
    assert shutil.which("systemctl", path=env["PATH"]) == str(fb / "systemctl"), "the FAKE systemctl must shadow the real one wherever --unit-dir is passed"
    return env, table, calls


def cron_run(line: str, env: dict) -> subprocess.CompletedProcess:
    """Run one rendered cron line the way cron does: sh -c <everything after the
    5 schedule fields>, a minimal environment, no tty."""
    return subprocess.run(["sh", "-c", line.split(" ", 5)[5]], env=env,
                          capture_output=True, text=True, timeout=120)


def managed_block(table: Path) -> list[str]:
    ls = table.read_text().splitlines()
    b = [i for i, x in enumerate(ls) if x.startswith("# >>> agi-crons")]
    e = [i for i, x in enumerate(ls) if x.startswith("# <<< agi-crons")]
    assert len(b) == 1 and len(e) == 1, ls
    return ls[b[0]:e[0] + 1]


# --- R: renderer pins over a fixture node (green today) ---


def test_r1_without_the_cell_grid_sync_off_leaves_no_apply_line(tmp_path):
    """The witness: disabling grid_sync alone removes the self-heal."""
    root = make_project(tmp_path, fm_with(drop_cell=True, grid_sync=False))
    lines = render(root)
    assert lines, "the other managed jobs still render"
    assert not [l for l in lines if is_apply_line(l)], lines


def test_r2_grid_sync_on_carries_the_apply_as_the_last_semicolon_step(tmp_path):
    root = make_project(tmp_path, fm_with(drop_cell=True, grid_sync=True))
    gs = [l for l in render(root) if "grid.py commit" in l]
    assert len(gs) == 1
    cmd = gs[0].split(" && ", 1)[1]
    assert " && " not in cmd, "a failed grid step must not skip the heal"
    steps = [s.strip() for s in cmd.split(";")]
    assert len(steps) == 3, steps
    assert "grid.py commit" in steps[0] and "push-changed" in steps[1]
    assert "crons.py apply --unit-dir" in steps[2]


def test_r3_a_cell_in_the_brief_shape_renders_one_standalone_line(tmp_path):
    root = make_project(tmp_path, fm_with(cell=SYNTH_CELL, drop_cell=True, grid_sync=False))
    base = make_project(tmp_path, fm_with(drop_cell=True, grid_sync=False), name="base")
    with_cell, without = render(root), render(base)
    mine = standalone(with_cell)
    assert len(mine) == 1, with_cell
    assert mine[0].startswith("*/5 * * * * cd ")
    # the same lines otherwise (the two projects differ only in their paths)
    assert norm([l for l in with_cell if l != mine[0]], root.parent) == norm(without, base.parent)


@pytest.mark.parametrize("box", [BOX, "core-town", ""])
def test_r4_a_boxless_cell_renders_on_every_box(tmp_path, box):
    root = make_project(tmp_path, fm_with(cell=SYNTH_CELL, drop_cell=True, grid_sync=False))
    assert len(standalone(render(root, box=box))) == 1, box


@pytest.mark.parametrize("box,expect", [(BOX, True), ("core-town", False), ("", False)])
def test_r4b_a_boxed_cell_is_gated_the_thing_to_avoid(tmp_path, box, expect):
    root = make_project(tmp_path, fm_with(cell=BOXED_CELL, drop_cell=True, grid_sync=False))
    assert bool(standalone(render(root, box=box))) is expect, box


def test_r5_a_boxed_cell_without_why_box_is_named_by_audit(tmp_path):
    cell = {k: v for k, v in BOXED_CELL.items() if k != "why_box"}
    root = make_project(tmp_path, fm_with(cell=cell, drop_cell=True, grid_sync=False))
    found = crons.cmd_audit(root, crontab_file=tmp_path / "t.fixture", unit_dir=tmp_path / "u")
    assert any("crons_apply" in f and "why_box" in f for f in found), found


def test_r6_a_blank_why_box_raises(tmp_path):
    root = make_project(tmp_path, fm_with(cell={**BOXED_CELL, "why_box": "  "}, drop_cell=True, grid_sync=False))
    with pytest.raises(crons.CronsError, match="why_box"):
        crons._resolve(root)


# --- L: the LIVE cell (RED until cadences.crons_apply lands) ---


def _cell() -> dict:
    cell = (_live_fm().get("cadences") or {}).get("crons_apply")
    assert cell is not None, "cron:crons has no cadences.crons_apply cell"
    return cell


def live_root(tmp_path, **kw) -> Path:
    _cell()
    return make_project(tmp_path, fm_with(**kw))


def test_l1_the_cell_is_declared_every_5_min_and_boxless():
    cell = _cell()
    assert cell.get("enabled") is True
    assert cell.get("every_mins") == 5 and cell.get("schedule") is None
    assert "box" not in cell and "why_box" not in cell, "a box gate narrows the self-heal (SM RE5/RE6)"


def test_l2_the_block_holds_exactly_one_standalone_apply_line(tmp_path):
    root = live_root(tmp_path, grid_sync=False)
    lines = render(root)
    mine = standalone(lines)
    assert len(mine) == 1, lines
    assert mine[0].startswith("*/5 * * * * cd "), mine[0]
    assert len([l for l in lines if is_apply_line(l)]) == 1, "with grid_sync off, the cell is the ONLY apply"
    _, _, repo_root, engine_root, _ = crons._resolve(root)
    body = re.sub(r" >> (\S+) 2>&1$", "", mine[0].split(" && ", 1)[1])
    log = re.search(r" >> (\S+) 2>&1$", mine[0]).group(1)
    m = STANDALONE_CMD.match(body)
    assert m, body
    assert m["py"] == str(engine_root), "the DURABLE engine copy, not a staging path"
    assert "{" not in mine[0] and "}" not in mine[0], "an unresolved placeholder"
    assert log == str(crons._log_path(repo_root)), "the block's one log"
    assert "--crontab-file" not in mine[0]


def test_l3_the_cell_changes_no_other_managed_line(tmp_path):
    with_cell = render(live_root(tmp_path, grid_sync=True))
    without = render(make_project(tmp_path, fm_with(drop_cell=True, grid_sync=True), name="base"))
    mine = standalone(with_cell)
    assert len(mine) == 1
    rest = [l for l in with_cell if l != mine[0]]
    assert norm(rest, tmp_path / "repo") == norm(without, tmp_path / "base")


def test_l4_the_cell_is_one_command_not_a_chain(tmp_path):
    mine = standalone(render(live_root(tmp_path, grid_sync=False)))
    assert len(mine) == 1
    body = mine[0].split(" && ", 1)[1]
    assert ";" not in body and " && " not in body and "grid.py" not in body


def test_l5_the_cell_renders_on_any_box_and_with_agi_box_unset(tmp_path, monkeypatch):
    root = live_root(tmp_path, grid_sync=False)
    for box in (BOX, "core-town", ""):
        assert len(standalone(render(root, box=box))) == 1, box
    monkeypatch.delenv("AGI_BOX", raising=False)
    _, _, repo_root, engine_root, node = crons._resolve(root)   # no AGI_BOX, no default_box cell
    lines = crons.render_managed_lines(root, repo_root, engine_root, node)
    assert len(standalone(lines)) == 1, lines
    assert not [l for l in lines if "no AGI_BOX" in l and "crons_apply" in l], "the cell must not be among the refused box-gated jobs"


def test_l6_apply_twice_is_byte_identical(tmp_path, fakes):
    env, table, _ = fakes
    root = live_root(tmp_path, grid_sync=False)
    table.write_text("0 3 * * * /usr/bin/true\n")
    crons_py = [sys.executable, str(CRONS_PY), "apply", "--unit-dir", str(tmp_path / "u")]
    subprocess.run(crons_py, cwd=root, env=env, check=True, capture_output=True)
    first = table.read_text()
    subprocess.run(crons_py, cwd=root, env=env, check=True, capture_output=True)
    assert table.read_text() == first
    assert first.splitlines()[0] == "0 3 * * * /usr/bin/true"
    assert len(standalone(managed_block(table))) == 1


def test_l7_the_cell_line_undoes_a_hand_edit_and_keeps_a_hand_added_line(tmp_path, fakes):
    env, table, _ = fakes
    root = live_root(tmp_path, grid_sync=False)
    table.write_text("0 3 * * * /usr/bin/true\n")
    cell_line = standalone(render(root))[0]
    assert cron_run(cell_line, env).returncode == 0
    good = table.read_text()
    block = managed_block(table)
    victim = next(l for l in block if l.startswith("*/2 * * * * "))   # nudge_sweep
    edited = good.replace(victim, victim.replace("*/2 ", "*/9 ", 1), 1)
    assert edited != good
    edited += "30 6 * * * echo hand-added\n"
    table.write_text(edited)
    done = cron_run(cell_line, env)
    assert done.returncode == 0, done.stderr
    after = table.read_text()
    assert managed_block(table) == block, "the hand-edited managed line is undone"
    assert "30 6 * * * echo hand-added" in after.splitlines(), "a line outside the markers is left alone"
    assert "0 3 * * * /usr/bin/true" in after.splitlines()


def test_l8_the_cell_line_stops_units_when_crons_live_goes_false(tmp_path, fakes):
    env, table, calls = fakes
    svc = {"agi-e2a-fixture": {"enabled": True, "exec_start": "/usr/bin/true", "restart": "on-failure"}}
    root = live_root(tmp_path, grid_sync=False, services=True)
    # replace the live services with the one fixture service
    p = root / "nodes" / ".geometry" / "crons.md"
    fm = _frontmatter(p.read_text())
    fm["services"] = svc
    p.write_text("---\n" + yaml.safe_dump(fm, sort_keys=False) + "---\n\nBody.\n")
    cell_line = standalone(render(root))[0]
    udir = Path(env["HOME"]) / ".config" / "systemd" / "user"
    assert cron_run(cell_line, env).returncode == 0
    units = sorted(udir.glob("agi-agi-e2a-fixture-*.service")) or sorted(udir.glob("*e2a-fixture*.service"))
    assert units, f"the cell's apply wrote no unit file: {list(udir.glob('*'))}"
    fm["crons_live"] = False
    p.write_text("---\n" + yaml.safe_dump(fm, sort_keys=False) + "---\n\nBody.\n")
    calls.write_text("")
    done = cron_run(cell_line, env)
    assert done.returncode == 0, done.stderr
    assert not list(udir.glob("*e2a-fixture*.service")), "crons_live:false must stop and remove the unit"
    assert "disable" in calls.read_text(), calls.read_text()
    assert not [l for l in table.read_text().splitlines() if is_apply_line(l)]
