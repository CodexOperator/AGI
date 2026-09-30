"""probe.py -- the READ-ONLY read-back of goal:g7.33.18's table (g7.33.18.3).

The stub systemctl answers PER (manager, unit) and returns `infinity` for a
wrong-manager ask -- the DH.434 defect -- so asking user@<uid>.service of the
USER manager is a red test, not a silent blank row.  It RECORDS every argv, so
"only read verbs are ever called" is checked on bytes, not prose.
"""
from __future__ import annotations
import hashlib, json, os, pathlib, subprocess, sys, tempfile

import pytest

HERE = pathlib.Path(__file__).resolve().parent
BOXKIT = HERE.parents[0] / "boxkit"
sys.path.insert(0, str(BOXKIT))
sys.path.insert(0, str(HERE / "fixtures" / "boxkit_probe"))
import probe  # noqa: E402
import fake_systemctl  # noqa: E402
sys.path.insert(0, str(HERE.parents[1] / "bin"))  # mem_cap, the ONE spawn-block owner
import mem_cap  # noqa: E402

CELLS = {"install_root": "/", "sbin_dir": "usr/local/sbin",
         "systemd_system_dir": "etc/systemd/system", "systemd_conf_dir": "etc/systemd",
         "user_systemd_dir": "{home}/.config/systemd/user", "watchdog_conf": "etc/watchdog.conf"}
# the kit's non-memory cells; every MEMORY target is render.sizing() over config:guard
# (goal:g7.16.1.5.5.4) -- this tmp root has no guard node, so guard-init's defaults apply
VALUES = {"USER_TASKS": "16384", "OOM_POLICY": "continue"}
HELD = 0.0                  # MiB held outside user@ on the fixture box
HELD_FLAG = ["--held-outside-user-mib", str(HELD)]
BASE = 7365.0                 # MiB, the INSTALLED user@ MemoryMax the stub reports
MEMTOTAL = BASE + 1911.0      # MiB, MemTotal the fixture /proc carries
SWAP = 4095.0                 # MiB

# unit -> property -> value, per manager.  system manager owns user@/user.slice/
# system.slice/plain units; the user manager owns agi.slice and the OOMPolicy units.
FACTORY = {
    "system": {
        "user@{uid}.service": {"MemoryMax": f"{int(BASE)}M", "MemoryHigh": f"{int(BASE * 0.9)}M",
                               "MemorySwapMax": f"{int(SWAP * 0.5)}M", "MemoryLow": "1024M",
                               "TasksMax": "16384"},
        "user.slice": {"MemoryLow": "1024M"},
        "user-{uid}.slice": {"MemoryLow": "1024M"},
        "system.slice": {"MemoryMin": "128M"},
        "agi-memguard.service": {"active": True},
    },
    "user": {
        # guard-init truncates at each step: max = BASE*70//100, high = max*90//100
        "agi.slice": {"MemoryHigh": f"{int(BASE) * 70 // 100 * 90 // 100}M",
                      "MemoryMax": f"{int(BASE) * 70 // 100}M"},
        "claude-remote-control.service": {"OOMPolicy": "continue"},
        "streamer-stub.service": {"OOMPolicy": "continue"},
        "streamer-stub-watch.service": {"OOMPolicy": "continue"},
    },
}
STUB = ('#!/usr/bin/env python3\n'
        'import os, sys\n'
        f'sys.path.insert(0, {str(HERE / "fixtures" / "boxkit_probe")!r})\n'
        'import fake_systemctl\n'
        'sys.stdout.write(fake_systemctl.answer(sys.argv[1:], os.environ["PROBE_CALLS"]))\n')


def _shim(tmp: pathlib.Path) -> str:
    path = tmp / "systemctl"
    path.write_text(STUB)
    path.chmod(0o755)
    return str(path)


def _can_fork() -> bool:
    """False on a box whose live process count is at/over RLIMIT_NPROC: every
    fork then returns EAGAIN and the tests drive the SAME stub in-process."""
    try:
        subprocess.run(["/bin/true"], capture_output=True)
        return True
    except (BlockingIOError, OSError):
        return False


def _fixture(tmp: pathlib.Path, monkeypatch, factory=None, base=BASE, memtotal=MEMTOTAL):
    (tmp / "templates").mkdir()
    (tmp / "templates" / "manifest.json").write_text(json.dumps({"pieces": []}))
    agi = tmp / ".agi"
    (agi / "nodes" / ".geometry").mkdir(parents=True)
    (agi / "config.json").write_text(json.dumps({
        "paths": {"boxkit": dict(CELLS, templates_dir="templates")},
        "values": {"boxkit": dict(VALUES), "memcap": {}},
        "spawn": {"memory_max": "2G", "tasks_max": 150}}))
    (agi / "nodes" / ".geometry" / "crons.md").write_text(
        "---\nid: cron:crons\ntype: cron\ncadences:\n  memory_alarm:\n"
        "    every_mins: 1\n    enabled: true\n    cmd: memory_alarm.py --root {root}\n"
        "crons_live: true\n---\n")
    root = tmp / "install"
    (root / "proc").mkdir(parents=True)
    (root / "proc" / "meminfo").write_text(
        f"MemTotal:       {int(memtotal * 1024)} kB\nMemFree: 1 kB\n"
        f"SwapTotal:      {int(SWAP * 1024)} kB\nSwapFree: 1 kB\n")
    conf = {
        "etc/systemd/system/user@{uid}.service.d/50-sanctuary-guard.conf":
            f"[Service]\nMemoryHigh={int(BASE * 0.9)}M\nMemoryMax={int(BASE)}M\n",
        "etc/systemd/system/user.slice.d/50-sanctuary-guard.conf": "[Slice]\nMemoryLow=1024M\n",
        "etc/systemd/system/user-{uid}.slice.d/50-sanctuary-guard.conf": "[Slice]\nMemoryLow=1024M\n",
        "etc/systemd/system/system.slice.d/50-sanctuary-guard.conf": "[Slice]\nMemoryMin=128M\n",
        "etc/systemd/oomd.conf.d/50-sanctuary-guard.conf":
            "[OOM]\nSwapUsedLimit=90%\nDefaultMemoryPressureLimit=60%\n"
            "DefaultMemoryPressureDurationSec=20s\n",
        ".config/systemd/user/agi.slice.d/50-agi.conf": None,   # {home} -> tmp, see below
        "usr/local/sbin/agi-memguard.py": "# guard\n",
    }
    for rel, text in conf.items():
        if text is None:
            continue
        where = root / rel.replace("{uid}", str(os.getuid()))
        where.parent.mkdir(parents=True, exist_ok=True)
        where.write_text(text)
    # the user_systemd_dir cell carries {home}, which expands ABSOLUTE: the agi.slice
    # drop-in lives under HOME, not under install_root.
    user_conf = tmp / ".config" / "systemd" / "user" / "agi.slice.d"
    user_conf.mkdir(parents=True)
    user_conf.joinpath("50-agi.conf").write_text(
        f"[Slice]\nMemoryHigh={round(BASE * 0.63)}M\nMemoryMax={round(BASE * 0.70)}M\n")
    (root / "etc").mkdir(parents=True, exist_ok=True)
    (root / "etc" / "watchdog.conf").write_text(
        "watchdog-timeout = 60\ninterval = 10\ntest-binary = /usr/local/sbin/sanctuary-health\n")
    fact = json.loads(json.dumps(factory if factory is not None else FACTORY).replace(
        "{uid}", str(os.getuid())))
    log = str(tmp / "systemctl.calls")
    monkeypatch.setenv("PROBE_CALLS", log)
    monkeypatch.setenv("PROBE_FACTORY", json.dumps(fact))
    monkeypatch.setenv("HOME", str(tmp))
    monkeypatch.setenv("AGI_MEMCAP_SYSTEMD_RUN", "1")
    shim = _shim(tmp)
    if not _can_fork():
        monkeypatch.setattr(probe, "run", lambda systemctl, argv: fake_systemctl.answer(argv, log))
    return agi, root, shim


def _by_name(table):
    return {name: (got, want, ok) for name, got, want, ok in table}


def _calls(tmp):
    p = tmp / "systemctl.calls"
    return [json.loads(ln) for ln in p.read_text().splitlines()] if p.is_file() else []


def _verb(argv):
    """`--user` is a manager flag, not the verb; the verb follows it."""
    return argv[argv.index("--user") + 1] if "--user" in argv else argv[0]


def _run(agi, root, shim, extra=()):
    """The one way the tests call the probe: the held-outside flag is passed
    explicitly, so a missing one is a test's own doing and never a default."""
    return probe.main(["--root", str(agi), "--install-root", str(root),
                       "--systemctl", str(shim)] + HELD_FLAG + list(extra))


def test_clean_table_exits_zero(tmp_path, monkeypatch, capsys):
    agi, root, shim = _fixture(tmp_path, monkeypatch)
    assert _run(agi, root, shim) == 0
    out = capsys.readouterr().out
    assert "DRIFT" not in out and "UNKNOWN" not in out, out
    assert "user@ MemoryHigh" in out and "oomd SwapUsedLimit" in out
    assert "memory_alarm (config:crons)" in out and "mem_cap.systemd_run_usable" in out


def test_one_drift_exits_one_naming_the_row(tmp_path, monkeypatch, capsys):
    agi, root, shim = _fixture(tmp_path, monkeypatch)
    fact = json.loads(os.environ["PROBE_FACTORY"])
    fact["system"][f"user@{os.getuid()}.service"]["MemoryHigh"] = f"{int(BASE * 0.9) + 1}M"
    os.environ["PROBE_FACTORY"] = json.dumps(fact)
    assert _run(agi, root, shim) == 1
    assert "DRIFT: user@ MemoryHigh" in capsys.readouterr().out


def test_a_drifted_drop_in_file_is_its_own_row(tmp_path, monkeypatch, capsys):
    agi, root, shim = _fixture(tmp_path, monkeypatch)
    (root / f"etc/systemd/system/user@{os.getuid()}.service.d/50-sanctuary-guard.conf").write_text("")
    assert _run(agi, root, shim) == 1
    assert "DRIFT: user@ drop-in" in capsys.readouterr().out


def test_user_at_is_asked_of_the_system_manager(tmp_path, monkeypatch):
    """THE DH.434 DEFECT.  The USER manager answers `infinity` for user@<uid>,
    which blanks every ratio row.  Assert the manager, not just the outcome."""
    agi, root, shim = _fixture(tmp_path, monkeypatch)
    probe.rows(agi, root, shim)
    unit = f"user@{os.getuid()}.service"
    asks = [c for c in _calls(tmp_path) if c[-1] == unit and _verb(c) == "show"]
    assert asks and all("--user" not in c for c in asks), asks
    assert _run(agi, root, shim) == 0


def test_agi_slice_is_asked_of_the_user_manager(tmp_path, monkeypatch):
    agi, root, shim = _fixture(tmp_path, monkeypatch)
    probe.rows(agi, root, shim)
    asks = [c for c in _calls(tmp_path) if c[-1] == "agi.slice" and _verb(c) == "show"]
    assert asks and all("--user" in c for c in asks), asks


def test_a_wrong_manager_answer_can_never_read_ok(tmp_path, monkeypatch):
    """If the probe DID ask the user manager for user@, base is None and NO ratio
    row may report ok -- the blank table is a loud failure, not a green one."""
    agi, root, shim = _fixture(tmp_path, monkeypatch)
    monkeypatch.setattr(probe, "run", lambda systemctl, argv: (
        "infinity\n" if "--user" in argv else "infinity\n"))
    table = _by_name(probe.rows(agi, root, shim, HELD))
    assert table["user@ MemoryHigh"][1] is None
    assert table["user@ MemoryHigh"][2] != "ok"


def test_the_stub_answers_infinity_for_a_wrong_manager(tmp_path, monkeypatch):
    """The shim itself is the falsifier: same unit, both managers, different answers."""
    _, _, shim = _fixture(tmp_path, monkeypatch)
    out = {m: probe.show(shim, f"user@{os.getuid()}.service", "MemoryMax", m == "user")
           for m in ("system", "user")}
    assert probe.mib(out["system"]) == BASE and out["user"] == "infinity"


def test_judging_uses_the_installed_max_not_a_constant(tmp_path, monkeypatch):
    """A box whose reserve is 942 MiB sizes the same ratios on its own numbers."""
    agi, root, shim = _fixture(tmp_path, monkeypatch, base=6912.0, memtotal=6912.0 + 942.0)
    fact = json.loads(os.environ["PROBE_FACTORY"])
    for prop, frac in (("MemoryMax", 1.0), ("MemoryHigh", 0.9)):
        fact["system"][f"user@{os.getuid()}.service"][prop] = f"{int(BASE * frac)}M"
    fact["system"][f"user@{os.getuid()}.service"]["MemoryMax"] = f"{int(6912.0)}M"
    os.environ["PROBE_FACTORY"] = json.dumps(fact)
    assert _run(agi, root, shim) == 1
    table = _by_name(probe.rows(agi, root, shim, HELD))
    assert table["reserve (derived)"][0] == pytest.approx(942.0)
    assert probe.as_mib(table["user@ MemoryMax"][0]) == pytest.approx(6912.0)


def test_only_read_verbs_reach_systemctl_and_nothing_is_written(tmp_path, monkeypatch):
    agi, root, shim = _fixture(tmp_path, monkeypatch)

    def tree_hash(p: pathlib.Path) -> str:
        h = hashlib.sha256()
        for f in sorted(p.rglob("*")):
            h.update(str(f.relative_to(p)).encode() + (f.read_bytes() if f.is_file() else b""))
        return h.hexdigest()

    before = tree_hash(root)
    _run(agi, root, shim)
    calls = _calls(tmp_path)
    assert calls and all(_verb(c) in ("show", "is-active") for c in calls), calls
    assert tree_hash(root) == before, "the probe wrote under install_root"


def test_no_finite_base_is_not_ok(tmp_path, monkeypatch, capsys):
    """A dropped user@ cap leaves nothing to judge the ratios against: the ratio
    rows read UNKNOWN-worthy (want None) and the table does not read green."""
    agi, root, shim = _fixture(tmp_path, monkeypatch)
    fact = json.loads(os.environ["PROBE_FACTORY"])
    fact["system"][f"user@{os.getuid()}.service"].pop("MemoryMax")
    os.environ["PROBE_FACTORY"] = json.dumps(fact)
    assert _run(agi, root, shim) == 1
    table = _by_name(probe.rows(agi, root, shim, HELD))
    assert table["user@ MemoryHigh"][1] is None
    assert table["user@ MemoryHigh"][2] in ("DRIFT", "UNKNOWN")
    assert table["reserve (derived)"][0] == "UNKNOWN"


def test_missing_drop_in_is_a_drift(tmp_path, monkeypatch):
    agi, root, shim = _fixture(tmp_path, monkeypatch)
    (root / f"etc/systemd/system/user@{os.getuid()}.service.d/50-sanctuary-guard.conf").unlink()
    table = _by_name(probe.rows(agi, root, shim, HELD))
    assert table["user@ drop-in"][2] == "DRIFT"


def test_mem_cap_row_comes_from_the_cache_not_a_spawn(tmp_path, monkeypatch):
    monkeypatch.delenv("AGI_MEMCAP_SYSTEMD_RUN", raising=False)
    agi, root, shim = _fixture(tmp_path, monkeypatch)
    run = tmp_path / "rt" / "agi-memcap"
    run.mkdir(parents=True)
    run.joinpath("probe").write_text(f"{probe.mem_cap._boot_id()} 1\n")
    monkeypatch.setenv("XDG_RUNTIME_DIR", str(tmp_path / "rt"))
    table = _by_name(probe.rows(agi, root, shim, HELD))
    assert table["mem_cap.systemd_run_usable"] == (True, True, "ok")


# --- the four closes of DH.439 --------------------------------------------

def test_reserve_is_unknown_without_the_flag_and_never_passes(tmp_path, monkeypatch, capsys):
    """`held_outside_user_mib` is a PER-BOX INPUT with no config cell, so it is a
    required flag: absent -> the row is UNKNOWN, prints no number, exits 3."""
    agi, root, shim = _fixture(tmp_path, monkeypatch)
    rc = probe.main(["--root", str(agi), "--install-root", str(root), "--systemctl", str(shim)])
    out = capsys.readouterr().out
    assert rc == 3, out
    assert "reserve (derived)" in out and "UNKNOWN" in out
    got = _by_name(probe.rows(agi, root, shim))["reserve (derived)"]
    assert got == ("UNKNOWN", "UNKNOWN", "UNKNOWN"), got


def test_the_reserve_is_memtotal_minus_held_minus_the_installed_max(tmp_path, monkeypatch):
    agi, root, shim = _fixture(tmp_path, monkeypatch)
    table = _by_name(probe.rows(agi, root, shim, 2000.0))
    assert table["reserve (derived)"][0] == pytest.approx(MEMTOTAL - 2000.0 - BASE)


def test_a_negative_reserve_is_drift_and_reaches_the_exit_code(tmp_path, monkeypatch, capsys):
    """An OVER-COMMITTED box (user@ capped above MemTotal - held) is DRIFT, not
    information: the table must name it and exit 1.  A healthy reserve stays
    informational, and a MISSING input stays UNKNOWN with exit 3."""
    agi, root, shim = _fixture(tmp_path, monkeypatch)
    assert _by_name(probe.rows(agi, root, shim, 0.0))["reserve (derived)"][2] == "info"
    rc = probe.main(["--root", str(agi), "--install-root", str(root), "--systemctl", str(shim),
                     "--held-outside-user-mib", str(MEMTOTAL)])
    out = capsys.readouterr().out
    assert rc == 1, out
    assert "DRIFT: reserve (derived)" in out, out


# --- the four closes of DH.450 --------------------------------------------

class _Spy:
    """Every write-shaped call a READ-ONLY probe must not make, INSTALLED AND
    RECORDED (never raised on -- a spy observes, a gate blocks; the read-only
    path is proved by the empty list, never by a crash).  Exactly what is
    installed: `builtins.open(..., w|a|x|+)`, `Path.write_text`,
    `Path.write_bytes`, `os.mkdir`, `os.chmod`, `os.replace`, `os.rename`,
    `os.unlink`, `os.remove`, `tempfile.mkstemp`, `tempfile.NamedTemporaryFile`."""

    def __init__(self, monkeypatch):
        self.calls = []
        import builtins, tempfile as _tf
        real_open, real_mkdir, real_chmod = builtins.open, os.mkdir, os.chmod
        real_write_text, real_write_bytes = pathlib.Path.write_text, pathlib.Path.write_bytes
        monkeypatch.setattr(builtins, "open", self._open(real_open))
        monkeypatch.setattr(os, "mkdir", self._wrap(real_mkdir, "os.mkdir"))
        monkeypatch.setattr(os, "chmod", self._wrap(real_chmod, "os.chmod"))
        monkeypatch.setattr(pathlib.Path, "write_text", self._wrap(real_write_text, "write_text"))
        monkeypatch.setattr(pathlib.Path, "write_bytes", self._wrap(real_write_bytes, "write_bytes"))
        # the atomic-write family: a read-only probe that "only" replaced a file
        # wrote exactly as much as one that created it.
        for name in ("replace", "rename", "unlink", "remove"):
            if hasattr(os, name):
                monkeypatch.setattr(os, name, self._wrap(getattr(os, name), f"os.{name}"))
        for name in ("mkstemp", "NamedTemporaryFile"):
            if hasattr(_tf, name):
                monkeypatch.setattr(_tf, name, self._wrap(getattr(_tf, name), f"tempfile.{name}"))
        self._mkstemp = _tf.mkstemp
        if hasattr(_tf, "TemporaryFile"):
            monkeypatch.setattr(_tf, "TemporaryFile", self._wrap(_tf.TemporaryFile, "tempfile.TemporaryFile"))

    def _wrap(self, real, what):
        def call(*a, **k):
            self.calls.append((what, a[0] if a else None))
            return real(*a, **k)
        return call

    def _open(self, real):
        def call(file, mode="r", *a, **k):
            if set(mode) & set("wax+"):
                self.calls.append(("open-w", file))
            return real(file, mode, *a, **k)
        return call


def _no_systemctl(tmp_path, monkeypatch, agi, root):
    """rows() with the systemctl door answered IN-PROCESS and NOT recorded, so
    the only thing that can write during the spy window is the probe."""
    def fake_run(systemctl, argv):
        mgr = "user" if "--user" in argv else "system"
        rest = [a for a in argv if a != "--user"]
        unit, prop = rest[-1], (rest[rest.index("-p") + 1] if "-p" in rest else "active")
        fact = json.loads(os.environ["PROBE_FACTORY"]).get(mgr, {}).get(unit, {})
        if rest[0] == "is-active":
            return "active\n" if fact.get(prop) else "inactive\n"
        return f"{fact.get(prop, 'infinity')}\n"
    monkeypatch.setattr(probe, "run", fake_run)


def test_the_real_cached_probe_path_creates_nothing_and_reports_unknown(tmp_path, monkeypatch):
    """THE DH.450 DEFECT, red first: mem_cap._read_cached_probe(None) mkdirs a
    0700 dir under $XDG_RUNTIME_DIR and chmods it, so the 'read-only' probe
    WROTE on the box.  The row must now come from a real READ of the cache
    FILE: an empty runtime dir is UNKNOWN, and nothing is created."""
    agi, root, shim = _fixture(tmp_path, monkeypatch)
    rt = tmp_path / "rt"
    rt.mkdir()
    monkeypatch.delenv("AGI_MEMCAP_SYSTEMD_RUN", raising=False)
    monkeypatch.delenv("AGI_MEMCAP_CACHE", raising=False)
    monkeypatch.setenv("XDG_RUNTIME_DIR", str(rt))
    _no_systemctl(tmp_path, monkeypatch, agi, root)
    spy = _Spy(monkeypatch)
    table = _by_name(probe.rows(agi, root, shim, HELD))
    assert table["mem_cap.systemd_run_usable"] == (None, True, "UNKNOWN"), table
    assert spy.calls == [], spy.calls
    assert list(rt.iterdir()) == [], "the probe CREATED something under $XDG_RUNTIME_DIR"


def test_one_pure_resolver_and_the_writer_never_drift(tmp_path, monkeypatch):
    """RESIDUE 1: the cache path is computed in ONE place.  mem_cap's WRITER
    still creates its private dir; the PURE resolver the probe uses creates
    nothing and returns the same file -- with and without XDG_RUNTIME_DIR, and
    with the AGI_MEMCAP_CACHE override.

    RESIDUE (DH.468): the (override=None, use_runtime=False) case falls
    through to tempfile.gettempdir() -- the REAL $TMPDIR -- so the WRITER half
    mkdirs + chmods <real tmp>/capdir OUTSIDE tmp_path.  A read-only guarantee
    was tested by a test that writes outside its own sandbox.  So the
    gettempdir() base BOTH resolvers can reach is pointed INSIDE tmp_path, and
    the proof is a per-case `is_relative_to(tmp_path)` on every value either
    resolver returns -- checked on bytes, not claimed in a comment."""
    cfg = {"values": {"memcap": {"probe_cache_dir_name": "capdir",
                                 "probe_cache_file": "verdict"}}}
    fake_tmp = tmp_path / "faketmp"          # stands in for the box's $TMPDIR
    monkeypatch.setattr(tempfile, "gettempdir", lambda: str(fake_tmp))
    for override in (None, str(tmp_path / "fixed-cache")):
        for use_runtime in (True, False):
            monkeypatch.delenv("AGI_MEMCAP_CACHE", raising=False)
            monkeypatch.delenv("XDG_RUNTIME_DIR", raising=False)
            if override:
                monkeypatch.setenv("AGI_MEMCAP_CACHE", override)
            fresh = tmp_path / f"rt-{bool(override)}-{use_runtime}"
            if use_runtime:                      # a dir that DOES NOT EXIST yet
                monkeypatch.setenv("XDG_RUNTIME_DIR", str(fresh))
            pure = probe.mem_cap._cache_path_pure(cfg)
            assert pure is not None
            if use_runtime and not override:
                assert not fresh.exists(), "the PURE resolver created a directory"
            writer = probe.mem_cap._probe_cache_path(cfg)
            assert pure == writer, "the two resolvers drifted"
            for label, path in (("pure", pure), ("writer", writer)):
                assert pathlib.Path(path).is_relative_to(tmp_path), (
                    f"the {label} resolver reached OUTSIDE tmp_path: {path}")


def test_the_real_cached_probe_path_reads_a_planted_verdict_and_writes_nothing(tmp_path, monkeypatch):
    """Same path with a trusted cache FILE present: the row is ok, the dir is
    untouched (no mkdir, no chmod), and the memcap cells drive WHERE it reads."""
    agi, root, shim = _fixture(tmp_path, monkeypatch)
    cfg = json.loads((agi / "config.json").read_text())
    cfg["values"]["memcap"].update({"probe_cache_dir_name": "capdir", "probe_cache_file": "verdict"})
    (agi / "config.json").write_text(json.dumps(cfg))
    rt = tmp_path / "rt"
    (rt / "capdir").mkdir(parents=True)
    (rt / "capdir" / "verdict").write_text(f"{probe.mem_cap._boot_id()} 0\n")
    monkeypatch.delenv("AGI_MEMCAP_SYSTEMD_RUN", raising=False)
    monkeypatch.delenv("AGI_MEMCAP_CACHE", raising=False)
    monkeypatch.setenv("XDG_RUNTIME_DIR", str(rt))
    _no_systemctl(tmp_path, monkeypatch, agi, root)
    spy = _Spy(monkeypatch)
    table = _by_name(probe.rows(agi, root, shim, HELD))
    assert table["mem_cap.systemd_run_usable"] == (False, True, "DRIFT"), table
    assert spy.calls == [], spy.calls


def test_a_cache_file_from_another_boot_is_unknown_not_false(tmp_path, monkeypatch):
    """A stale (pre-reboot) verdict is UNKNOWN, never a `False` that would read
    as DRIFT and send the caller down a path the box never took."""
    agi, root, shim = _fixture(tmp_path, monkeypatch)
    rt = tmp_path / "rt"
    (rt / "agi-memcap").mkdir(parents=True)
    (rt / "agi-memcap" / "probe").write_text("stale-boot-id 0\n")
    monkeypatch.setenv("XDG_RUNTIME_DIR", str(rt))
    assert probe.cached_usable(json.loads((agi / "config.json").read_text())) is None
    (rt / "agi-memcap" / "probe").unlink()
    (rt / "agi-memcap").rmdir()
    (rt / "agi-memcap").symlink_to(tmp_path / "nowhere")
    assert probe.cached_usable(json.loads((agi / "config.json").read_text())) is None


def test_the_only_dest_literals_left_live_in_one_table():
    """KIT CONTRACT: dest_rel belongs to the manifest; until g7.33.18.1 lands
    every one of them sits in ONE module-level table (FILES), not scattered.
    The shape of a dest literal is its SUFFIX, and the suffix set is READ FROM
    THE TABLE ITSELF (FILES+UNITS), so a new `.service`/`.timer`/`.slice` row is
    covered the day it is added -- no hand-kept list to rot.  A slashless
    `agi-memguard.py` outside the table is as much a defect as a `/usr/...`."""
    import ast
    tree = ast.parse(pathlib.Path(probe.__file__).read_text())
    tables = {getattr(n, "targets", None) and n.targets[0].id for n in tree.body
              if isinstance(n, ast.Assign)}
    assert "FILES" in tables and "UNITS" in tables
    suffixes = {pathlib.PurePosixPath(v).suffix for v in FILES_SRC if pathlib.PurePosixPath(v).suffix}
    assert {".conf", ".py", ".service"} <= suffixes, suffixes   # the shapes the kit ships today
    # prose and the tables' own docstrings are not dest literals
    skip = {ast.get_docstring(n, clean=False) for n in ast.walk(tree)
            if isinstance(n, (ast.Module, ast.FunctionDef, ast.ClassDef, ast.AsyncFunctionDef))}
    lits = set()
    for node in ast.walk(tree):
        if (isinstance(node, ast.Constant) and isinstance(node.value, str)
                and pathlib.PurePosixPath(node.value).suffix in suffixes
                and node.value not in skip
                and node.value != pathlib.Path(probe.__file__).name):   # argparse `prog=`
            lits.add((node.lineno, node.value))
    for lineno, val in lits:
        assert val in FILES_SRC, f"line {lineno}: {val!r} is a dest literal outside the table"


FILES_SRC = {r[2] for r in probe.FILES} | {r[1] for r in probe.UNITS}   # dest_rel | unit



def _guard(monkeypatch, **cells):
    """THIS box's config:guard cells, as the probe reads them (render.guard_cells)."""
    monkeypatch.setattr(probe.render, "guard_cells",
                        lambda root=None: {**probe.render.guard_defaults(), **cells})


def test_a_target_cell_is_read_from_the_config_and_unit_normalised(tmp_path, monkeypatch):
    """goal:g7.16.1.5.5.4: the target is config:guard's cell through guard-init's
    arithmetic.  The same size as "1G" and "1024M" is the same target: a size cell
    PARSES.  Change the cell and the row's want moves with it."""
    agi, root, shim = _fixture(tmp_path, monkeypatch)
    want = _by_name(probe.rows(agi, root, shim, HELD))["user@ MemoryLow"][1]
    assert probe.as_mib(want) == pytest.approx(1024.0), want
    _guard(monkeypatch, CLAUDE_LOW_CAP="1G")                          # 1G, not "1024M"
    assert _by_name(probe.rows(agi, root, shim, HELD))["user@ MemoryLow"][2] == "ok"
    _guard(monkeypatch, CLAUDE_LOW_CAP="2048M")       # min(7365 // 6, 2048) = 1227M
    assert _by_name(probe.rows(agi, root, shim, HELD))["user@ MemoryLow"][2] == "DRIFT"


def test_a_percent_cell_and_a_percent_drop_in_are_the_same_target(tmp_path, monkeypatch):
    """The live box's finding: the cell is '90', the drop-in writes '90%'.  A
    string compare drifts on the '%' and that drift is noise, not a fact."""
    agi, root, shim = _fixture(tmp_path, monkeypatch)
    row = _by_name(probe.rows(agi, root, shim, HELD))["oomd SwapUsedLimit"]
    assert (row[1], row[2]) == ("90", "ok")               # cell 90, drop-in 90%
    _guard(monkeypatch, OOMD_SWAP_USED_PCT="80")          # a real difference
    assert _by_name(probe.rows(agi, root, shim, HELD))["oomd SwapUsedLimit"][2] == "DRIFT"


def test_a_row_with_no_target_cell_is_info_and_never_ok(tmp_path, monkeypatch, capsys):
    """A cell the kit does not carry is INFORMATION.  It may not read `ok`."""
    agi, root, shim = _fixture(tmp_path, monkeypatch)
    cfg = json.loads((agi / "config.json").read_text())
    cfg["values"]["boxkit"].pop("USER_TASKS")     # a kit cell (memory targets always exist)
    (agi / "config.json").write_text(json.dumps(cfg))
    assert _run(agi, root, shim) == 0             # info does not fail the table
    table = _by_name(probe.rows(agi, root, shim, HELD))
    assert table["user@ TasksMax"][1] is None
    assert table["user@ TasksMax"][2] == "info"
    line = [ln for ln in capsys.readouterr().out.splitlines()
            if ln.startswith("user@ TasksMax ")][0]
    assert not line.endswith(" ok"), line


def test_spawn_rows_target_the_config_and_the_resolvers_not_a_literal(tmp_path, monkeypatch):
    """No "2G" literal here, and no UNSOURCED number: the row is declared
    cell vs mem_cap's resolver, so a config the resolvers do not honour is
    DRIFT.  150 below is the FIXTURE's own cell (written by _fixture), not
    a bound of the engine, and the fail-closed value is
    `mem_cap._DEFAULT_TASKS_MAX`, not a literal: a hardcoded 150/96 pair
    would keep passing after the cell or the shipped default moved."""
    agi, root, shim = _fixture(tmp_path, monkeypatch)
    assert _by_name(probe.rows(agi, root, shim, HELD))["spawn.memory_max"][2] == "ok"
    cfg = json.loads((agi / "config.json").read_text())
    cfg["spawn"]["memory_max"] = "3G"             # the cell IS the target: still ok
    (agi / "config.json").write_text(json.dumps(cfg))
    assert _by_name(probe.rows(agi, root, shim, HELD))["spawn.memory_max"][2] == "ok"
    # the ONE cell: with no override, the resolver returns spawn.tasks_max itself.
    # (a resolver reading values.memcap.tasks_max falls back to 96 and fails HERE.)
    monkeypatch.delenv("AGI_TASKS_MAX", raising=False)
    assert _by_name(probe.rows(agi, root, shim, HELD))["spawn.tasks_max"] == (150, 150, "ok")
    # the resolver disagrees with the cell, through a path PRODUCTION can take:
    # mem_cap.resolve_tasks_max honours AGI_TASKS_MAX.  The cell itself is 150.
    monkeypatch.setenv("AGI_TASKS_MAX", str(mem_cap._DEFAULT_TASKS_MAX))
    table = _by_name(probe.rows(agi, root, shim, HELD))
    assert table["spawn.tasks_max"] == (150, mem_cap._DEFAULT_TASKS_MAX, "DRIFT"), table["spawn.tasks_max"]
    assert _run(agi, root, shim) == 1


def test_a_malformed_spawn_container_is_data_never_a_crash(tmp_path, monkeypatch):
    """The reader got this guard in _spawn_block (mem_cap.py); the probe -- the
    read-back of the WHOLE table -- still did `cfg.get("spawn") or {}` then
    `.get(cell)`, so a scalar container raised out of rows() instead of
    reporting.  A cell is data: the row must read as absent (info)."""
    agi, root, shim = _fixture(tmp_path, monkeypatch)
    cfg = json.loads((agi / "config.json").read_text())
    for bad in (42, "2G", ["x"], None):
        cfg["spawn"] = bad
        (agi / "config.json").write_text(json.dumps(cfg))
        table = _by_name(probe.rows(agi, root, shim, HELD))
        want_max, want_cap = mem_cap._DEFAULT_TASKS_MAX, mem_cap._DEFAULT_MEMORY_CAP
        assert table["spawn.tasks_max"] == (None, want_max, "info"), (bad, table["spawn.tasks_max"])
        assert table["spawn.memory_max"] == (None, want_cap, "info"), bad


def test_the_probe_reads_the_spawn_block_through_the_readers_one_guard(
        tmp_path, monkeypatch):
    """The malformed-container fix in probe.py used to be a HAND COPY of
    mem_cap._spawn_block's `isinstance(spawn, dict)` test.  A copy is a second
    rule: a shape the reader learns to guard would still kill the table.  The
    probe must CALL the shared guard -- proved by a sentinel, not by reading
    the source: if the probe decides for itself, the sentinel is never called
    FROM probe.py.  (Recording every caller is not enough -- the resolvers
    legitimately go through the same guard -- so it is the frame, not the call,
    that this asserts.)"""
    agi, root, shim = _fixture(tmp_path, monkeypatch)
    seen = []
    real = mem_cap._spawn_block

    def spy(cfg):
        seen.append(sys._getframe(1).f_code.co_filename)
        return real(cfg)

    monkeypatch.setattr(mem_cap, "_spawn_block", spy)
    table = _by_name(probe.rows(agi, root, shim, HELD))
    assert any(f.endswith("probe.py") for f in seen), seen
    assert ("spawn.tasks_max" in table and "spawn.memory_max" in table), sorted(table)


def test_a_write_shaped_answer_is_data_never_executed(tmp_path, monkeypatch, capsys):
    """The hostile systemctl: it answers a string cell with a command.  The
    probe must print it, judge it, and never run it -- the canary survives."""
    agi, root, shim = _fixture(tmp_path, monkeypatch)
    canary = tmp_path / "CANARY"
    payload = f"systemctl stop agi-memguard.service; touch {canary}"
    fact = json.loads(os.environ["PROBE_FACTORY"])
    fact["user"]["streamer-stub.service"]["OOMPolicy"] = payload
    os.environ["PROBE_FACTORY"] = json.dumps(fact)
    rc = _run(agi, root, shim)
    out = capsys.readouterr().out
    assert rc == 1 and "DRIFT: OOMPolicy streamer-stub" in out, out
    assert payload in out                      # printed as a value ...
    assert not canary.exists()                 # ... and never as a command


def test_a_mutation_verb_never_reaches_the_box():
    """Fail-closed in code: probe.run refuses any verb outside READ_VERBS, so a
    future row cannot smuggle a write through the one systemctl door.  No
    fixture: the guard fires BEFORE any subprocess, and on a box where fork is
    unavailable _fixture replaces probe.run with the in-process stub."""
    for bad in (["restart", "agi.slice"], ["--user", "set-property", "agi.slice", "x=y"],
                ["daemon-reload"], ["enable", "agi-memguard"], ["stop", "agi-memguard"]):
        with pytest.raises(ValueError):
            probe.run("/bin/false", bad)      # a verb that would fail if it ran
    assert probe.READ_VERBS == ("show", "is-active")


def test_memory_targets_come_from_the_guard_cells_not_the_kit(tmp_path, monkeypatch):
    """goal:g7.16.1.5.5.4 falsifier 2: a box guard-init sized with ITS cells reads
    clean -- here the owner's leeway cells (user@ high 95 %, engine 3G)."""
    agi, root, shim = _fixture(tmp_path, monkeypatch)
    _guard(monkeypatch, USER_HIGH_PCT="95", AGI_MAX_PCT="70", ENGINE_MAX="3G")
    fact = json.loads(os.environ["PROBE_FACTORY"])
    fact["system"][f"user@{os.getuid()}.service"]["MemoryHigh"] = f"{int(BASE) * 95 // 100}M"
    os.environ["PROBE_FACTORY"] = json.dumps(fact)
    table = _by_name(probe.rows(agi, root, shim, HELD))
    assert table["user@ MemoryHigh"][2] == "ok"
    assert not {k: v for k, v in table.items() if v[2] == "DRIFT"}
    assert not set(probe.render.MEMORY) & set(json.loads((agi / "config.json").read_text())
                                              ["values"]["boxkit"])
