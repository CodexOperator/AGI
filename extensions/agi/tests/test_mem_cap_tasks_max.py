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
pytest. They now go through a STUBBED RUNNER -- the one seam every mem_cap
spawn passes (`subprocess.run` as the module reaches it) -- installed so that
a spawn would be RECORDED instead of launched. The rows no longer CALL it:
`wrap_argv` builds argv and returns, so the claim is that it reaches NO spawn
seam at all (`calls == []`), which is a real property and breaks the day it
starts spawning. No scope, no unit, no forked child, no `shutil.which` gate.

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

#: An argv TOKEN, not a process count: no row forks anything (see
#: `_stub_spawn`), so the number is here to make the built argv readable and
#: to keep the fan-out SHAPE (`<script> <flag> <n>`) honest. The old comment
#: claimed "18 < 20 processes" -- a live fork count this file no longer makes.
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
    """(cfg, the cell value read from the live config).

    The number lives in `.agi/config.json` ONLY. This function asserts the
    cell EXISTS, is an int and is positive, and RETURNS it -- so a row can
    compare against what the owner configured without a `150` literal in
    this file redding on an owner edit (config-max, owner 09-23)."""
    cfg = _live_config()
    spawn = cfg.get("spawn")
    assert isinstance(spawn, dict), \
        f"spawn.tasks_max: live config has no spawn block: {spawn!r}"
    assert "tasks_max" in spawn, \
        f"spawn.tasks_max: live config carries no tasks_max cell: {sorted(spawn)}"
    val = spawn["tasks_max"]
    assert isinstance(val, int) and not isinstance(val, bool), \
        f"spawn.tasks_max: cell is not an int: {val!r}"
    assert val > 0, f"spawn.tasks_max: cell is not positive: {val!r}"
    return cfg, val


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
    cfg, cell = _live_spawn_tasks_max()
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
    monkeypatch.setenv("AGI_TASKS_MAX", "5")
    assert mem_cap.resolve_tasks_max(_cfg(tasks_max=8)) == 5


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


# ---- (3) the fan-out: the BOUND is on the argv, nothing is ever launched ---

class _Recorded:
    """What a real `subprocess.run` would have returned, for a caller that
    only reads `returncode` / `stdout` / `stderr`."""
    returncode = 0
    stdout = ""
    stderr = ""


def _stub_spawn(monkeypatch):
    """Replace the ONE seam every mem_cap spawn passes -- `subprocess.run`
    as the module reaches it -- with a recorder. Returns the call list.

    `wrap_argv` only BUILDS an argv, so this is the whole spawn surface:
    stubbed, no scope, no unit, no forked child, no `systemd-run` gate.

    The rows below do NOT call the runner themselves. They used to, and then
    asserted `calls == [argv]` -- the TEST was the caller, so the assertion
    proved the stub records, not that `mem_cap` spawns through it. Nothing
    invokes the seam, so the honest claim is the OPPOSITE one: building the
    argv launches NOTHING (`calls == []`), which is a real property of
    `wrap_argv` and would break the day it started spawning."""
    calls = []

    def _run(argv, *a, **kw):
        calls.append(list(argv))
        return _Recorded()

    monkeypatch.setattr(mem_cap.subprocess, "run", _run)
    return calls


def test_the_wrapped_argv_carries_both_bounds_and_launches_nothing(monkeypatch):
    """Was: a real `systemd-run` scope forked 18 children under
    TasksMax=8 and a real user manager counted the refusals -- the ONE row
    that ever tested that the scope REFUSES a fan-out past the bound.
    Now: the same argv, and the bound on it, with no launch at all.

    NAMED COVERAGE RESIDUE (accepted, not hidden): the real refusal is no
    longer exercised anywhere in the fast suite. What this row proves is
    that `wrap_argv` carries the bound AND spawns nothing -- the third
    production spawn sites (dispatch.py, heal.py, workflow.py) still call
    it and are untouched by this file."""
    calls = _stub_spawn(monkeypatch)
    monkeypatch.setattr(mem_cap, "systemd_run_usable", lambda cfg=None: True)
    monkeypatch.setenv("AGI_TASKS_MAX", "8")
    inner = ["fanout.py", "marks", str(WANTED)]
    argv = mem_cap.wrap_argv(inner, "512M", _cfg(tasks_max=8))
    assert argv[0] == "systemd-run", argv
    assert "--property=MemoryMax=512M" in argv, argv
    assert "--property=TasksMax=8" in argv, argv
    assert "--" in argv and argv[argv.index("--") + 1:] == inner, argv
    # building the argv reached NO spawn seam at all
    assert calls == [], calls


def test_the_unwrapped_path_is_unchanged(monkeypatch):
    """`cap is None` -> the SAME argv, so a caller's fan-out is untouched:
    the bound is a property of the wrapped scope, never a behaviour change
    for a caller that asked for no cap -- and still no launch."""
    calls = _stub_spawn(monkeypatch)
    monkeypatch.setattr(mem_cap, "systemd_run_usable", lambda cfg=None: True)
    inner = ["fanout.py", "marks", str(WANTED)]
    argv = mem_cap.wrap_argv(inner, None)
    assert argv is inner, argv
    assert calls == [], calls
