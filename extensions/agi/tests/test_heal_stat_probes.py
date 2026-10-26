"""goal:g7.16.1.11.45.6 -- heal.py's `is_dir()` / `is_file()` / `is_symlink()` probes never raise on EACCES
and never read "cannot see" as "gone" (the sibling of goal:g7.16.1.11.45.5, same raise class).

On Python 3.12 these three raise PermissionError behind an unreadable (0o000) parent, exactly as
`Path.exists()` does. heal.py had 33 raw calls; this leaf routes them:

  is_dir   -> `_sweep_is_dir` (True / False / None, goal:g7.16.1.11.45.4)
  is_file  -> `_is_file3`     (same shape); the three recovery-path sites share `_proven_file`
  is_symlink -> `_is_symlink3` (same shape)

R1 every site that must never raise is routed, with the fail direction named in its row below.
R2 never `except OSError: False` for an answer whose "False" means "gone".
R3 a mutant per site where a behaviour row can reach it: the BARE mutant (the raw call back) reads RED on a
   raise; the FALSE-WRAP mutant (`except OSError: False`) reads RED only where None and False differ.
R4 the census: every is_dir / is_file / is_symlink call in heal.py is routed or on `ALLOW` with a reason,
   compared BOTH ways (a new raw call, or a stale entry, reads RED).
R5 (fix-forward from GATE275) `_all_windows` RAISES on an unreadable seam file as before .45.5 (an unread
   window list must never read as "no windows"); `_pane_pid_of` / `_pane_pid_map` answer UNKNOWN (0 / {}),
   the values their docstrings define as "unknown, never dead".

The rows need a non-root uid (root stats a 0o000 dir). The skip says so; `pytest -rs` prints it.
Sites with no behaviour row are named in `CENSUS_ONLY` (the census is their only guard).
"""
from __future__ import annotations

import ast
import importlib.util
import os
import sys
import types
from pathlib import Path

import pytest

BIN = Path(__file__).resolve().parents[1] / "bin"
sys.path.insert(0, str(BIN))
sys.path.insert(0, str(Path(__file__).resolve().parent))    # the seat-watch fixture helpers of test_heal_seats.py


def _load(name):
    spec = importlib.util.spec_from_file_location(name, BIN / f"{name}.py")
    mod = importlib.util.module_from_spec(spec)
    spec.loader.exec_module(mod)
    return mod


heal = _load("heal")
import rotate  # noqa: E402

NOT_ROOT = pytest.mark.skipif(
    os.geteuid() == 0,
    reason="root can stat a 0o000 dir: the falsifier needs a non-root uid (uid %d)" % os.geteuid())


class closed_dir:
    """A directory that is 0o000 (or `mode`) for the duration of the block (restored on exit)."""

    def __init__(self, path: Path, mode: int = 0o000):
        self.path, self.mode = path, mode

    def __enter__(self):
        self.path.chmod(self.mode)
        return self.path

    def __exit__(self, *exc):
        self.path.chmod(0o700)


@pytest.fixture(autouse=True)
def _log(tmp_path, monkeypatch):
    monkeypatch.setenv("AGI_REAPER_LOG", str(tmp_path / "reaper.log"))
    monkeypatch.setattr(heal, "_sweep_pressure_ok", lambda root: (True, "test"))
    heal._SWEEP_SKIP.clear()
    heal._SWEEP_ORPHAN.clear()
    yield
    heal._SWEEP_SKIP.clear()
    heal._SWEEP_ORPHAN.clear()


def _text(tmp_path) -> str:
    p = tmp_path / "reaper.log"
    return p.read_text() if p.exists() else ""


def _closed(tmp_path, *parts) -> Path:
    """`tmp/closed/<parts>`: the leaf exists; the PARENT is what the test will close."""
    d = tmp_path / "closed"
    (d.joinpath(*parts) if parts else d).mkdir(parents=True, exist_ok=True)
    return d


# ---- the mutants --------------------------------------------------------------------------------------
_PROBE = {"_sweep_is_dir": "is_dir", "_is_file3": "is_file", "_is_symlink3": "is_symlink"}


def _bare(name):
    attr = _PROBE[name]
    return lambda p: getattr(p, attr)()


def _false_wrap(name):
    attr = _PROBE[name]

    def probe(p):
        try:
            return getattr(p, attr)()
        except OSError:
            return False
    return probe


# ---- the probes (R1/R2) ---------------------------------------------------------------------------------
@NOT_ROOT
def test_the_probes_are_tri_state_and_never_raise(tmp_path):
    here = tmp_path / "f"
    here.write_text("x")
    (tmp_path / "d").mkdir()
    (tmp_path / "ln").symlink_to(here)
    closed = _closed(tmp_path, "inner")
    (closed / "inner" / "f").write_text("x")
    with closed_dir(closed):
        assert heal._sweep_is_dir(tmp_path / "d") is True
        assert heal._is_file3(here) is True and heal._is_file3(tmp_path / "d") is False
        assert heal._is_symlink3(tmp_path / "ln") is True and heal._is_symlink3(here) is False
        assert heal._is_file3(tmp_path / "nope") is False
        assert heal._is_symlink3(tmp_path / "nope") is False
        for fn, p in ((heal._sweep_is_dir, closed / "inner"), (heal._is_file3, closed / "inner" / "f"),
                      (heal._is_symlink3, closed / "inner" / "f")):
            assert fn(p) is None, f"{fn.__name__}: unreadable is UNKNOWN, not gone"
        with pytest.raises(PermissionError):
            (closed / "inner").is_dir()          # the premise: the stdlib probes raise here
        with pytest.raises(PermissionError):
            (closed / "inner" / "f").is_file()
        with pytest.raises(PermissionError):
            (closed / "inner" / "f").is_symlink()


@NOT_ROOT
def test_proven_file_is_true_only_for_a_file_and_names_the_unread_one(tmp_path):
    f = tmp_path / "f"
    f.write_text("x")
    closed = _closed(tmp_path, "inner")
    (closed / "inner" / "f").write_text("x")
    with closed_dir(closed):
        assert heal._proven_file(f, "s", "card", "no card") is True
        assert heal._proven_file(tmp_path / "nope", "s", "card", "no card") is False
        assert _text(tmp_path) == "", "an absent file is silent"
        assert heal._proven_file(closed / "inner" / "f", "s", "card", "no card") is False
    assert "watch: seat s card unread (EACCES): no card" in _text(tmp_path)


# ---- the sites: each returns the list of ways its contract is broken ------------------------------------
def _stub_rot(tmp_path, monkeypatch, parent: str = "rot"):
    """`rotate` with its records dir and sessions dir under the (to-be-closed) `closed/<parent>`."""
    closed = _closed(tmp_path, parent)
    monkeypatch.setattr(rotate, "_rotations_dir", lambda root: closed / parent / "rotations")
    monkeypatch.setattr(rotate, "_sessions_dir", lambda root: closed / parent / "sessions")
    return closed


def _guard(fn):
    """Run `fn`; a raise is a broken contract, never an error."""
    try:
        return fn(), None
    except Exception as e:  # noqa: BLE001 -- a mutant raises; the verdict reads it
        return None, f"raised {type(e).__name__}"


def s_discover_rounds(tmp_path, monkeypatch):
    closed = _closed(tmp_path, "main", "worktrees")
    with closed_dir(closed):
        got, bad = _guard(lambda: heal._discover_rounds(closed / "main"))
    if bad:
        return [bad]
    out = [] if got == [] else [f"rounds {got!r}"]
    if "watch: worktrees dir unread (EACCES): the rounds under it are not discovered" not in _text(tmp_path):
        out.append("no `worktrees dir unread` line")
    return out


def s_registry_now_has(tmp_path, monkeypatch):
    closed = _closed(tmp_path, "reg")
    with closed_dir(closed):
        got, bad = _guard(lambda: heal._registry_now_has(
            types.SimpleNamespace(REGISTRY_DEFAULT_DIR="/nonexistent"), "@1", str(closed / "reg")))
    if bad:
        return [bad]
    out = [] if got is None else [f"matched {got!r}"]
    if "watch: registry unread (EACCES): no successor matched" not in _text(tmp_path):
        out.append("no `registry unread` line")
    return out


def s_late_reap(tmp_path, monkeypatch):
    closed = _closed(tmp_path, "rot")
    rot = types.SimpleNamespace(_load_seats=lambda root: [], _rotations_dir=lambda root: closed / "rot")
    with closed_dir(closed):
        _, bad = _guard(lambda: heal._late_reap_skipped_pass(tmp_path, rot=rot))
    if bad:
        return [bad]
    return [] if "watch: rotations dir unread (EACCES): late reap skipped" in _text(tmp_path) else ["no `rotations dir unread` line"]


def s_sweep_base(tmp_path, monkeypatch):
    closed = _closed(tmp_path, "graph", "worktrees")
    with closed_dir(closed):
        got, bad = _guard(lambda: heal._sweep_finished_worktrees(closed / "graph"))
    if bad:
        return [bad]
    out = [] if got == (0, 0, 0) else [f"swept {got!r}"]
    if "[sweep] worktrees dir unread (EACCES): nothing swept" not in _text(tmp_path):
        out.append("no `worktrees dir unread` line")
    return out


def s_sweep_worktree_base(tmp_path, monkeypatch):
    closed = _closed(tmp_path, "wt")
    with closed_dir(closed):
        got, bad = _guard(lambda: heal._sweep_worktree_base(tmp_path, closed / "wt", None))
    return [bad] if bad else ([] if got is None else [f"base {got!r} (the tree would be REMOVED)"])


def s_iter_home(tmp_path, monkeypatch):
    src = tmp_path / "iter-1"
    src.mkdir()
    (src / "a.txt").write_text("a")
    closed = _closed(tmp_path, "home")
    with closed_dir(closed):
        got, bad = _guard(lambda: heal._sweep_iter_home(src, closed / "home"))
    return [bad] if bad else ([] if got is False else ["an unreadable home was judged HOME"])


def s_cold_link_toctou(tmp_path, monkeypatch):
    """The parent closes BETWEEN the exists probe and the is_symlink probe: the second must not raise."""
    closed = _closed(tmp_path, "main")
    monkeypatch.setattr(locations_mod(), "guard_cell", lambda root, name: str(tmp_path / "cold"))
    monkeypatch.setattr(heal, "_exists3", lambda p: False)
    with closed_dir(closed):
        got, bad = _guard(lambda: heal._sweep_cold_link(tmp_path, closed / "main", "iter-9"))
    if bad:
        return [bad]
    out = []
    if got is not None:
        out.append("a link was created behind an unreadable parent")
    if "cold link refused" in _text(tmp_path):
        out.append("the unreadable parent went on to the mkdir (a `cold link refused` line): it was read as 'no link'")
    return out


def locations_mod():
    import locations
    return locations


def s_sweep_link_state(tmp_path, monkeypatch):
    """A worktrees dir that can be LISTED but not searched: every entry's lstat is EACCES."""
    graph = tmp_path / "repo" / ".agi"
    base = graph / "worktrees"
    (base / "a00-zlink").mkdir(parents=True)
    monkeypatch.setenv("AGI_REAPER_LOG", str(tmp_path / "reaper.log"))
    with closed_dir(base, 0o444):
        _, bad = _guard(lambda: heal._sweep_finished_worktrees(graph))
    if bad:
        return [bad]
    t = _text(tmp_path)
    return [] if "[sweep] left a00-zlink: link state unread (EACCES)" in t else ["no `link state unread` line"]


def s_seat_geometry(tmp_path, monkeypatch):
    closed = _closed(tmp_path, "g")
    monkeypatch.setattr(heal, "_seat_worktree_gdir", lambda root, row: closed / "g")
    with closed_dir(closed):
        got, bad = _guard(lambda: heal._seat_geometry_dir(tmp_path, {"name": "s"}))
    return [bad] if bad else ([] if got is None else ["an unreadable geometry dir was ANSWERED"])


def s_crash_recorded(tmp_path, monkeypatch):
    closed = _stub_rot(tmp_path, monkeypatch)
    with closed_dir(closed):
        got, bad = _guard(lambda: heal._crash_recovery_recorded(tmp_path, "s", rotate, now=1.0))
    if bad:
        return [bad]
    out = []
    if got is not True:
        out.append(f"answered {got!r}: an unread record dir was read as 'no earlier respawn'")
    if "seat s rotations dir unreadable (EACCES): respawn held" not in _text(tmp_path):
        out.append("no `respawn held` line")
    return out


def s_in_flight(tmp_path, monkeypatch):
    closed = _stub_rot(tmp_path, monkeypatch)
    monkeypatch.setattr(heal, "_success_record_rotated", lambda *a, **k: (None, None))
    with closed_dir(closed):
        got, bad = _guard(lambda: heal._rotation_in_flight(tmp_path, "s", rotate, 1.0, row={}))
    if bad:
        return [bad]
    out = []
    if got is not True:
        out.append(f"answered {got!r}: an unread record dir was read as 'no rotation in flight'")
    if "seat s rotations dir unreadable (EACCES): treated as in flight" not in _text(tmp_path):
        out.append("no `treated as in flight` line")
    return out


def s_abort_crashed(tmp_path, monkeypatch):
    closed = _stub_rot(tmp_path, monkeypatch)
    with closed_dir(closed):
        got, bad = _guard(lambda: heal._abort_crashed_rotations(
            tmp_path, "s", {"pid": 7}, [], rotate, 1.0, lambda pid: False))
    return [bad] if bad else ([] if got == [] else [f"aborted {got!r}"])


def s_pin_table(tmp_path, monkeypatch):
    closed = _stub_rot(tmp_path, monkeypatch)
    with closed_dir(closed):
        got, bad = _guard(lambda: heal._pin_table(tmp_path, [{"name": "s"}]))
    if bad:
        return [bad]
    pins, skipped = got
    reasons = [r.get("reason", "") for r in skipped]
    return [] if any(r.startswith("pin unread (EACCES)") for r in reasons) else [f"skipped {reasons!r}: the unread pin was read as absent"]


def s_seat_sessions(tmp_path, monkeypatch):
    """F1: an unreadable registry is UNREAD (a distinct value), never `[]` = "no sessions"; a MISSING dir stays `[]`."""
    closed = _closed(tmp_path, "reg")
    with closed_dir(closed):
        got, bad = _guard(lambda: heal._seat_sessions(str(closed / "reg"), []))
    if bad:
        return [bad]
    out = []
    if got is not heal.UNREAD:
        out.append(f"answered {got!r}: an unread registry was read as 'no sessions'")
    if "watch: registry unreadable (EACCES): liveness unknown" not in _text(tmp_path):
        out.append("no `registry unreadable` line")
    missing, bad = _guard(lambda: heal._seat_sessions(str(tmp_path / "no-such-registry"), []))
    if bad or missing != []:
        out.append(f"a MISSING registry dir answered {missing!r} ({bad}); it is a legal []")
    return out


def s_seat_session_file(tmp_path, monkeypatch):
    """One registry FILE that cannot be read makes the whole table UNREAD (it may be a live seat session)."""
    reg = tmp_path / "reg"
    reg.mkdir()
    f = reg / "123.json"
    f.write_text('{"session_id": "s", "tmux": "x:@5.%5"}')
    f.chmod(0o000)
    try:
        got, bad = _guard(lambda: heal._seat_sessions(str(reg), [("@5", "seat-a")]))
    finally:
        f.chmod(0o600)
    if bad:
        return [bad]
    return [] if got is heal.UNREAD else [f"answered {got!r}: an unreadable session file was skipped"]


def s_judge_leases(tmp_path, monkeypatch):
    """belam with a predecessor-pin chain whose pin dir is unreadable: the chain is NOT complete."""
    closed = _stub_rot(tmp_path, monkeypatch)
    monkeypatch.setattr(heal, "_rotation_in_flight", lambda *a, **k: False)
    monkeypatch.setattr(heal, "_is_seat_current", lambda row, s: True)
    monkeypatch.setattr(heal, "_is_alive", lambda s, p: True)
    rows = [{"name": "belam", "predecessor_pins": 1, "pid": 1}]
    sess = [{"window_name": "belam-2", "session_id": "sid", "pid": 1}]
    with closed_dir(closed):
        got, bad = _guard(lambda: heal._judge_leases({}, sess, rows, tmp_path, now=1.0, pid_alive=lambda p: True))
    if bad:
        return [bad]
    v = [r.get("verdict") for r in got]
    return [] if v == ["BELAM-UNPINNED"] else [f"verdicts {v!r}: an unread predecessor pin read as complete"]


# (site id, scenario, helper the site routes through, does the false-wrap mutant also read RED?)
SITES = [
    ("discover_rounds", s_discover_rounds, "_sweep_is_dir", True),
    ("registry_now_has", s_registry_now_has, "_sweep_is_dir", True),
    ("late_reap_skipped_pass", s_late_reap, "_sweep_is_dir", True),
    ("sweep_worktree_base", s_sweep_worktree_base, "_sweep_is_dir", False),
    ("sweep_iter_home", s_iter_home, "_sweep_is_dir", False),
    ("sweep_cold_link", s_cold_link_toctou, "_is_symlink3", True),
    ("sweep_link_state", s_sweep_link_state, "_is_symlink3", True),
    ("seat_geometry_dir", s_seat_geometry, "_sweep_is_dir", False),
    ("crash_recovery_recorded", s_crash_recorded, "_sweep_is_dir", True),
    ("rotation_in_flight", s_in_flight, "_sweep_is_dir", True),
    ("abort_crashed_rotations", s_abort_crashed, "_sweep_is_dir", False),
    ("pin_table", s_pin_table, "_is_file3", True),
    ("seat_sessions", s_seat_sessions, "_sweep_is_dir", True),
    ("sweep_base", s_sweep_base, "_sweep_is_dir", True),
    ("judge_leases", s_judge_leases, "_is_file3", False),
]
IDS = [s[0] for s in SITES]


@NOT_ROOT
@pytest.mark.parametrize("site", SITES, ids=IDS)
def test_the_routed_site_holds_its_contract(site, tmp_path, monkeypatch):
    assert site[1](tmp_path, monkeypatch) == []


@NOT_ROOT
@pytest.mark.parametrize("site", SITES, ids=IDS)
def test_mutant_the_raw_call_back_reads_red(site, tmp_path, monkeypatch):
    monkeypatch.setattr(heal, site[2], _bare(site[2]))
    assert site[1](tmp_path, monkeypatch) != [], f"{site[0]}: the raw call put back did not read RED"


@NOT_ROOT
@pytest.mark.parametrize("site", [s for s in SITES if s[3]], ids=[s[0] for s in SITES if s[3]])
def test_mutant_the_false_wrap_reads_red(site, tmp_path, monkeypatch):
    monkeypatch.setattr(heal, site[2], _false_wrap(site[2]))
    assert site[1](tmp_path, monkeypatch) != [], f"{site[0]}: `except OSError: False` did not read RED"


# ---- R5: the window seams (GATE275 fix-forward) ----------------------------------------------------------
@NOT_ROOT
def test_the_window_list_raises_on_an_unreadable_seam_file_and_the_pane_seams_answer_unknown(tmp_path):
    closed = _closed(tmp_path)
    w = closed / "windows"
    w.write_text("@1 main 42\n")
    with closed_dir(closed):
        with pytest.raises(PermissionError):
            heal._all_windows(str(w))                      # never [] = "no windows"
        assert heal._pane_pid_of("@1", str(w)) == 0        # 0 = UNKNOWN, never "dead"
        assert heal._pane_pid_map(str(w)) == {}            # absent from the map = UNKNOWN
    assert heal._pane_pid_of("@1", str(w)) == 42           # readable: the seam still answers
    assert heal._pane_pid_map(str(w)) == {"@1": 42}
    assert heal._all_windows(str(tmp_path / "absent")) == []


# ---- F1-F3 (GATE286 RETURN): the CONSUMER of an unread registry -------------------------------------------------
@NOT_ROOT
def test_an_unread_session_file_makes_the_table_unread(tmp_path, monkeypatch):
    assert s_seat_session_file(tmp_path, monkeypatch) == []


def _seat_world(tmp_path):
    """A stale seat row (pid + @id both gone, no pin) and a recording launcher: the exact shape where a table that
    reads "no sessions" licenses a recovery launch over a session that may be alive. Returns (graph, windows, spawns)."""
    from test_heal_seats import _write_seats, _seed_recovery_ack
    g = tmp_path / "repo" / ".agi"
    (g / "sessions").mkdir(parents=True)
    (g / "config.json").write_text('{"metric_primary": "x"}')
    _seed_recovery_ack(g)
    _write_seats(g, [{"name": "seat-a", "pid": 999999, "window": "@50", "generation": 3}])
    wf = g / "windows.txt"
    wf.write_text("@1 other\n")
    return g, wf, []


def _run_watch(tmp_path, registry_dir):
    from test_heal_seats import _fake_launcher
    g, wf, spawns = _seat_world(tmp_path)
    acted = heal._watch_seats(g, pid_alive=lambda pid: False, window_path=str(wf),
                              launcher=_fake_launcher(spawns), registry_dir=str(registry_dir))
    return acted, spawns


def w_unread_registry_holds_the_recovery(tmp_path, monkeypatch):
    """F2/F3: stale row pid + an UNREAD registry + a recording launcher -> 0 launches, and the hold is named."""
    closed = _closed(tmp_path, "registry")
    with closed_dir(closed):
        (acted, spawns), bad = _guard(lambda: _run_watch(tmp_path, closed / "registry"))
    if bad:
        return [bad]
    out = []
    if spawns:
        out.append(f"{len(spawns)} recovery launch(es) over a seat whose liveness was UNKNOWN")
    if any(a.get("respawned") for a in acted):
        out.append("the pass reports a respawn")
    t = _text(tmp_path)
    if "watch: seat seat-a respawn held: registry unreadable, liveness unknown" not in t:
        out.append("no `respawn held` line")
    if "watch: registry unreadable (EACCES): liveness unknown" not in t:
        out.append("no `registry unreadable` line")
    return out


def w_missing_registry_still_recovers(tmp_path, monkeypatch):
    """CONTROL: a MISSING registry dir is a legal "no sessions": the dead seat is recovered as before."""
    (acted, spawns), bad = _guard(lambda: _run_watch(tmp_path, tmp_path / "no-such-registry"))
    if bad:
        return [bad]
    return [] if len(spawns) == 1 else [f"{len(spawns)} launches (want 1): the control no longer recovers"]


@NOT_ROOT
def test_an_unread_registry_holds_the_recovery(tmp_path, monkeypatch):
    assert w_unread_registry_holds_the_recovery(tmp_path, monkeypatch) == []


def test_control_a_missing_registry_dir_still_recovers_the_dead_seat(tmp_path, monkeypatch):
    assert w_missing_registry_still_recovers(tmp_path, monkeypatch) == []


def _unread_as_empty(real):
    return lambda *a, **k: [] if (r := real(*a, **k)) is heal.UNREAD else r


def _unread_as_none(real):
    return lambda *a, **k: None if (r := real(*a, **k)) is heal.UNREAD else r


@NOT_ROOT
@pytest.mark.parametrize("name,mk", [("unread-as-empty-list", _unread_as_empty), ("unread-as-None", _unread_as_none)])
def test_mutant_the_unread_table_folded_back_reads_red(name, mk, tmp_path, monkeypatch):
    """UNREAD read as `[]` licenses the launch; UNREAD returned as None is re-read by `_watch_one_seat`
    (`seat_sessions=None` means "not passed") and then handed to `_alive_via_pin` as a value: both launch."""
    monkeypatch.setattr(heal, "_seat_sessions", mk(heal._seat_sessions))
    assert w_unread_registry_holds_the_recovery(tmp_path, monkeypatch) != [], f"{name}: a launch over an unknown seat did not read RED"


@NOT_ROOT
def test_the_pin_reap_pass_judges_and_reaps_nothing_on_an_unread_registry(tmp_path, monkeypatch):
    closed = _closed(tmp_path, "registry")
    reaped = []
    from test_heal_seats import _write_seats
    g = tmp_path / "repo" / ".agi"
    (g / "sessions").mkdir(parents=True)
    (g / "config.json").write_text('{"reaper": {"pin_reap": "armed"}}')
    _write_seats(g, [{"name": "seat-a", "pid": 1, "window": "@5", "generation": 1}])
    wf = g / "windows.txt"
    wf.write_text("@5 seat-a\n")
    with closed_dir(closed):
        acted, bad = _guard(lambda: heal._pin_reap_pass(
            g, registry_dir=str(closed / "registry"), window_path=str(wf), pid_alive=lambda p: True,
            reaper=lambda *a, **k: reaped.append(a), mode="armed"))
    assert bad is None and acted == [] and reaped == []
    assert "watch: pin-reap pass skipped: registry unreadable, nothing judged and nothing reaped" in _text(tmp_path)


# ---- R4: the census of every is_dir / is_file / is_symlink call in heal.py -------------------------------
#: (enclosing function, stripped source line) -> why this raw probe is safe. Everything else is routed.
ALLOW = {
    ("_sweep_is_dir", "return p.is_dir()"): "the probe itself, inside the try that turns OSError into None",
    ("_is_file3", "return p.is_file()"): "the probe itself, inside the try that turns OSError into None",
    ("_is_symlink3", "return p.is_symlink()"): "the probe itself, inside the try that turns OSError into None",
    ("_sweep_iter_home", "if p.is_file() and _cli._migratable(p.relative_to(wt_iter))]"):
        "inside `try: ... except Exception: return False` -- a raise fails CLOSED (not home), never 'absent'",
    ("_sweep_iter_home", "if loc.is_file() and loc.read_bytes() == sp.read_bytes():"):
        "inside `try: ... except OSError: return False` -- a raise fails CLOSED (not home)",
    ("_sweep_iter_home", "if loser.is_file() and loser.read_bytes() == sp.read_bytes():"):
        "inside `try: ... except OSError: return False` -- a raise fails CLOSED (not home)",
    ("_sweep_cold_unlink", "if link.is_symlink():"):
        "inside `with contextlib.suppress(OSError)` -- a raise leaves the link and its cold dir in place",
    ("_main_graph_root", 'if (graph / locations.GRAPH_DIR_NAME / "nodes").is_dir():'):
        "process-wide input; unreadable = no correct pass possible: it picks the root the seat identity cell is "
        "READ from, a guessed root names the wrong tree, and an unreadable graph dir breaks every read after it "
        "(council: kept LOUD, alive [decision] 10:03:07Z 10-26)",
    ("_load_launcher", "if p.is_file():"):
        "process-wide input; unreadable = no correct pass possible: AGI_RECOVER_LAUNCHER names a test launcher, "
        "and falling through to real tmux on an unread path would spawn FOR REAL (council: kept LOUD, alive "
        "[decision] 10:03:07Z 10-26)",
}
#: routed sites that no behaviour row above reaches (the census is their only guard):
CENSUS_ONLY = {
    "_sweep_finished_worktrees: `rm_rc == 0 and _is_symlink3(wt) is True` (None leaves the link; the next "
    "pass takes the gone-is-True branch)",
    "_clean_stale_layout_locks / _recover_seat (transcript, card): through `_proven_file`, rows above",
}

_ATTRS = ("is_dir", "is_file", "is_symlink")


def _stat_calls(src: str) -> set[tuple[str, str]]:
    tree = ast.parse(src)
    lines = src.splitlines()
    out: set[tuple[str, str]] = set()

    class V(ast.NodeVisitor):
        def __init__(self):
            self.stack: list[str] = []

        def visit_FunctionDef(self, n):
            self.stack.append(n.name)
            self.generic_visit(n)
            self.stack.pop()

        visit_AsyncFunctionDef = visit_FunctionDef

        def visit_Call(self, n):
            f = n.func
            if isinstance(f, ast.Attribute) and f.attr in _ATTRS:
                out.add((self.stack[-1] if self.stack else "<module>", lines[n.lineno - 1].strip()))
            self.generic_visit(n)

    V().visit(tree)
    return out


def test_census_every_stat_call_in_heal_py_is_routed_or_named_safe():
    found = _stat_calls((BIN / "heal.py").read_text())
    assert found == set(ALLOW), (
        f"unlisted raw probe(s): {sorted(found - set(ALLOW))}; stale allowlist entr(ies): {sorted(set(ALLOW) - found)}")


@pytest.mark.parametrize("attr", _ATTRS)
def test_mutant_a_new_raw_probe_reads_red(attr):
    src = (BIN / "heal.py").read_text() + f"\n\ndef _new_probe(p):\n    return p.{attr}()\n"
    assert _stat_calls(src) != set(ALLOW)


def test_the_census_ignores_comments_and_docstrings():
    src = 'def f(p):\n    """p.is_dir() p.is_file() p.is_symlink() in prose"""\n    # p.is_dir() in a comment\n    return 1\n'
    assert _stat_calls(src) == set()


def test_census_only_sites_are_named():
    assert len(CENSUS_ONLY) == 2
