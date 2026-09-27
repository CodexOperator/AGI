"""TasksMax on the same scope that carries MemoryMax (DH.421,
hypothesis:a00-1ff9316d-177aae -- "a round's kid cannot fan out processes
past the box's bound"). The cell is `spawn.tasks_max`, the one that sits
beside `spawn.memory_max`; the two shipped defaults live in
`mem_cap._DEFAULT_TASKS_MAX` / `mem_cap._DEFAULT_MEMORY_CAP`, so a config with
no cell keeps working (a round may never commit `.agi/config.json`) and this
file never types either number.

THE FAN-OUT ROWS BELOW NEVER SPAWN (DH.453, closing the residue DH.421 left):
they used to build a real argv and hand it to `subprocess.run`, reaching the
REAL `agi-memcap-probe` / user scope and forking a real process tree inside a
pytest. They now BUILD an argv and assert on it. `wrap_argv` is pure: it
returns a list and launches nothing itself.

THERE IS NO SPAWN SEAM INSIDE mem_cap (DH.464, residue 1 closed). The old
docstring here called `subprocess.run` "the one seam every mem_cap spawn
passes". That was FALSE and the sites are nameable -- the cap is applied by
the CALLER, never inside the module:

  * dispatch.py  -- wraps the argv, then `subprocess.Popen`
  * heal.py      -- wraps `heal_argv`, then `subprocess.Popen`
  * workflow.py  -- wraps `cmd`; `subprocess.run` only inside its INJECTED
                    seam branch, `subprocess.Popen` otherwise

The only `subprocess.run` calls inside mem_cap are the PROBE's own
(`_PROBE_UNIT`), not a spawn. So the stub recorder, `_Recorded` and the
`calls == []` assertions are DELETED: a seam no production site passes proves
nothing but the fiction that it does. No scope, no unit, no forked child, no
`shutil.which` gate, and no patch of a seam that does not exist.

NAMED COVERAGE RESIDUE, accepted rather than hidden: the real scope REFUSING a
fan-out past TasksMax is exercised nowhere in the fast suite. The three
production spawn sites (dispatch.py, heal.py, workflow.py) are unchanged and
call `wrap_argv`; what this file asserts is the bound ON THE ARGV.
"""
from __future__ import annotations

import json
import sys
from pathlib import Path

import pytest

sys.path.insert(0, str(Path(__file__).resolve().parents[1] / "bin"))
import locations  # noqa: E402
import mem_cap  # noqa: E402

#: An argv TOKEN, not a process count: no row forks anything (every row is a
#: pure call to `wrap_argv`), so the number is here to make the built argv
#: readable and to keep the fan-out SHAPE (`<script> <flag> <n>`) honest. The
#: old comment claimed "18 < 20 processes" -- a live fork count this file no
#: longer makes.
WANTED = 18


@pytest.fixture(autouse=True)
def _no_ambient_tasks_max(monkeypatch):
    """No row reads the DEVELOPER's env: `AGI_TASKS_MAX` outranks the cell in
    `resolve_tasks_max`, so a shell that exports it would red the rows that
    never mention it. Rows that WANT the override set it themselves."""
    monkeypatch.delenv("AGI_TASKS_MAX", raising=False)


def _cfg(**spawn):
    return {"spawn": spawn}


def _live_config():
    """The live config THROUGH THE ONE RESOLVER (goal:g11, config-max).

    It used to walk `parents[3]` and join `.agi/config.json` by hand -- a
    path literal that silently reads the wrong file under the legacy layout
    or an engine clone, and a second copy of the rule `locations` already
    owns. `find_project_root` + `config_path` is that rule; a missing config
    is an AssertionError that says which cell is missing, never a KeyError
    from a bare `["spawn"]` (DH.453)."""
    root = locations.find_project_root(Path(__file__).resolve())
    assert root is not None, \
        "spawn.tasks_max: no project graph above this test file"
    path = locations.config_path(root)
    assert path is not None, f"spawn.tasks_max: no live config under {root}"
    with open(path) as fh:
        cfg = json.load(fh)
    assert isinstance(cfg, dict), \
        f"spawn.tasks_max: live config is not an object: {cfg!r}"
    return cfg


def _live_spawn_tasks_max():
    """(cfg, the RESOLVED number, parsed exactly as `resolve_tasks_max` does).

    The number lives in `.agi/config.json` ONLY, and the resolver accepts
    more than an int: it does `int(str(raw).strip())`. The old helper
    asserted `isinstance(val, int)`, so an owner editing the cell from `150`
    to `"150"` -- which the resolver reads as 150 -- reddened this file with
    "cell is not an int" while production was fine. So: parse the cell the
    way the resolver does, assert `resolve_tasks_max(cfg) ==` that parsed
    value and that it is a positive int. A cell that does not parse, or
    parses below 1, fails HERE BY NAME -- never a KeyError, and never a
    silent disagreement between the row and the resolver.

    IDENTITY IS NOT EQUALITY (DH.475, residue 1). The comparison was `is`,
    which holds only because CPython interns small ints in -5..256: the
    resolver REBUILDS the number with `int(str(raw).strip())`, so every
    planted cell above 256 -- and an owner editing `spawn.tasks_max` to a
    real value like 1000 -- reddened a green test with "resolver disagrees
    with the cell: 1000" while production was right. `==` is what this row
    means. Red-first proof: a planted cfg dict of 1000 reds the `is` form
    and greens the `==` form (measured, recorded in
    experiment:a00-36f071dc-154d29)."""
    cfg = _live_config()
    spawn = cfg.get("spawn")
    assert isinstance(spawn, dict), \
        f"spawn.tasks_max: live config has no spawn block: {spawn!r}"
    assert "tasks_max" in spawn, \
        f"spawn.tasks_max: live config carries no tasks_max cell: {sorted(spawn)}"
    raw = spawn["tasks_max"]
    try:                                    # the resolver's own spelling
        parsed = int(str(raw).strip())
    except (TypeError, ValueError):
        raise AssertionError(
            f"spawn.tasks_max: cell does not parse as a number: {raw!r}")
    assert parsed >= 1, f"spawn.tasks_max: cell is below 1: {raw!r}"
    resolved = mem_cap.resolve_tasks_max(cfg)
    assert resolved == parsed, \
        f"spawn.tasks_max: resolver disagrees with the cell: {resolved!r}"
    return cfg, parsed


# ---- (1) the cell and the shipped default ----------------------------------

def test_default_is_shipped_when_no_cell_is_present():
    assert mem_cap.resolve_tasks_max() == mem_cap._DEFAULT_TASKS_MAX
    assert mem_cap.resolve_tasks_max({}) == mem_cap._DEFAULT_TASKS_MAX
    assert mem_cap.resolve_tasks_max({"spawn": {}}) == mem_cap._DEFAULT_TASKS_MAX
    assert mem_cap.resolve_tasks_max({"spawn": "2G"}) == \
        mem_cap._DEFAULT_TASKS_MAX


def test_the_live_config_carries_the_owners_own_value():
    """`spawn.tasks_max` is the owner's own number (TMM.263 (2)), so a real
    round is bounded at what the config says -- read from the config, never
    pinned here."""
    cfg, cell = _live_spawn_tasks_max()   # the helper already proved equality
    assert mem_cap.resolve_tasks_max(cfg) == cell, cell


def test_the_old_cell_is_read_nowhere():
    """`values.memcap.tasks_max` is not a second spelling of the same bound."""
    cfg, cell = _live_spawn_tasks_max()
    other = cell + 1  # a value that can never equal the live cell
    cfg.setdefault("values", {}).setdefault("memcap", {})["tasks_max"] = other
    assert mem_cap.resolve_tasks_max(cfg) == cell, (other, cell)


def test_the_cell_wins_when_it_is_readable():
    assert mem_cap.resolve_tasks_max(_cfg(tasks_max=8)) == 8
    assert mem_cap.resolve_tasks_max(_cfg(tasks_max="12")) == 12


def test_an_unreadable_cell_falls_back_and_never_uncaps(monkeypatch):
    for bad in (None, "", "abc", 0, -3, {}, []):
        assert mem_cap.resolve_tasks_max(_cfg(tasks_max=bad)) is not None
        assert mem_cap.resolve_tasks_max(_cfg(tasks_max=bad)) == \
            mem_cap._DEFAULT_TASKS_MAX, bad
    # the OTHER direction, and it is proven here: the ENV outranks the cell
    monkeypatch.setenv("AGI_TASKS_MAX", "5")
    assert mem_cap.resolve_tasks_max(_cfg(tasks_max=8)) == 5
    # BOTH behaviours are proven in this file: `AGI_TASKS_MAX` overrides the
    # cell (this row), and the cell alone carries the bound on the argv
    # (`test_the_wrapped_argv_carries_both_bounds`), where the autouse
    # `_no_ambient_tasks_max` fixture leaves the variable UNSET.


def test_a_non_dict_spawn_container_reads_as_absent_for_bOTH_readers():
    """One shared guard: `{"spawn": 42}` raised TypeError out of
    resolve_memory_cap while resolve_tasks_max already defaulted. The
    shipped memory default is READ as `mem_cap._DEFAULT_MEMORY_CAP`, not
    typed here, so the two readers' defaults are named in one place."""
    for bad in (42, 0, [], "x", None, True):
        cfg = {"spawn": bad}
        assert mem_cap.resolve_tasks_max(cfg) == mem_cap._DEFAULT_TASKS_MAX, bad
        assert mem_cap.resolve_memory_cap(cfg) == \
            mem_cap._DEFAULT_MEMORY_CAP, bad
    # a dict with the real cell still reads through the SAME helper
    assert mem_cap.resolve_tasks_max({"spawn": {"tasks_max": 7}}) == 7
    assert mem_cap.resolve_memory_cap({"spawn": {"memory_max": "1G"}}) == "1G"
    assert mem_cap._spawn_block({"spawn": 42}) == {}


# ---- (2) the argv ----------------------------------------------------------

def test_systemd_run_argv_carries_both_bounds(monkeypatch):
    monkeypatch.setattr(mem_cap, "systemd_run_usable", lambda cfg=None: True)
    out = mem_cap.wrap_argv(["echo", "x"], "256M", _cfg(tasks_max=8))
    assert out[0] == "systemd-run", out
    assert "--property=MemoryMax=256M" in out, out
    assert "--property=TasksMax=8" in out, out
    assert out[-1] == "x", out


def test_no_cell_means_the_shipped_default_on_the_argv(monkeypatch):
    monkeypatch.setattr(mem_cap, "systemd_run_usable", lambda cfg=None: True)
    out = mem_cap.wrap_argv(["echo", "x"], "256M")
    assert f"--property=TasksMax={mem_cap._DEFAULT_TASKS_MAX}" in out, out


def test_cap_none_is_still_the_same_argv_object():
    argv = ["echo", "hi"]
    assert mem_cap.wrap_argv(argv, None, _cfg(tasks_max=8)) is argv


def test_the_prlimit_fallback_names_no_process_bound_it_cannot_enforce(
        monkeypatch):
    """RLIMIT_NPROC is per-USER, so the fallback has NO per-tree cap. That is
    a NAMED residual in `wrap_argv`'s comment, not a silent hole -- and this
    test fails the day someone pretends otherwise."""
    monkeypatch.setattr(mem_cap, "systemd_run_usable", lambda cfg=None: False)
    out = mem_cap.wrap_argv(["echo", "x"], "256M", _cfg(tasks_max=8))
    assert out[:2] == ["prlimit", f"--as={256 * 1024 ** 2}"], out
    assert not [a for a in out if "TasksMax" in a or "nproc" in a], out


# ---- (3) the fan-out: the BOUND is on the argv, and nothing is launched ---

def test_the_wrapped_argv_carries_both_bounds(monkeypatch):
    """Was: a real `systemd-run` scope forked 18 children under
    TasksMax=8 and a real user manager counted the refusals -- the ONE row
    that ever tested that the scope REFUSES a fan-out past the bound.
    Now: the same argv, and the bound on it, with no launch at all.

    THE BOUND COMES FROM THE CELL, not from the env (DH.464, residue 2).
    This row used to `setenv("AGI_TASKS_MAX", "8")` AND pass
    `_cfg(tasks_max=8)` -- the same 8 on both sides, so a cell of 99999
    would still have produced `--property=TasksMax=8` and the cell was
    unfalsifiable. `resolve_tasks_max` reads the env FIRST, so here the
    autouse `_no_ambient_tasks_max` fixture leaves `AGI_TASKS_MAX` UNSET
    (do not re-set it) and the argv's bound is carried by the cell alone.
    The opposite direction -- env over cell -- is proven in
    `test_an_unreadable_cell_falls_back_and_never_uncaps`.

    NAMED COVERAGE RESIDUE (accepted, not hidden): the real refusal is no
    longer exercised anywhere in the fast suite. What this row proves is
    that `wrap_argv` carries both bounds onto the argv. The three
    production spawn sites (dispatch.py, heal.py, workflow.py) call it and
    are untouched by this file."""
    monkeypatch.setattr(mem_cap, "systemd_run_usable", lambda cfg=None: True)
    inner = ["fanout.py", "marks", str(WANTED)]
    argv = mem_cap.wrap_argv(inner, "512M", _cfg(tasks_max=8))
    assert argv[0] == "systemd-run", argv
    assert "--property=MemoryMax=512M" in argv, argv
    assert "--property=TasksMax=8" in argv, argv
    assert "--" in argv and argv[argv.index("--") + 1:] == inner, argv


def test_the_unwrapped_path_is_unchanged(monkeypatch):
    """`cap is None` -> the SAME argv, so a caller's fan-out is untouched:
    the bound is a property of the wrapped scope, never a behaviour change
    for a caller that asked for no cap."""
    monkeypatch.setattr(mem_cap, "systemd_run_usable", lambda cfg=None: True)
    inner = ["fanout.py", "marks", str(WANTED)]
    argv = mem_cap.wrap_argv(inner, None)
    assert argv is inner, argv
