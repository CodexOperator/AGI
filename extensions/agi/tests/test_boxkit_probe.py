"""probe.py -- the READ-ONLY read-back of goal:g7.33.18's table (g7.33.18.3).

The stub systemctl answers PER (manager, unit) and returns `infinity` for a
wrong-manager ask -- the DH.434 defect -- so asking user@<uid>.service of the
USER manager is a red test, not a silent blank row.  It RECORDS every argv, so
"only read verbs are ever called" is checked on bytes, not prose.
"""
from __future__ import annotations
import hashlib, json, os, pathlib, subprocess, sys

import pytest

HERE = pathlib.Path(__file__).resolve().parent
BOXKIT = HERE.parents[0] / "boxkit"
sys.path.insert(0, str(BOXKIT))
sys.path.insert(0, str(HERE / "fixtures" / "boxkit_probe"))
import probe  # noqa: E402
import fake_systemctl  # noqa: E402

CELLS = {"install_root": "/", "sbin_dir": "usr/local/sbin",
         "systemd_system_dir": "etc/systemd/system", "systemd_conf_dir": "etc/systemd",
         "user_systemd_dir": "{home}/.config/systemd/user", "watchdog_conf": "etc/watchdog.conf"}
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
        "agi.slice": {"MemoryHigh": f"{round(BASE * 0.63)}M", "MemoryMax": f"{round(BASE * 0.70)}M"},
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


def test_clean_table_exits_zero(tmp_path, monkeypatch, capsys):
    agi, root, shim = _fixture(tmp_path, monkeypatch)
    assert probe.main(["--root", str(agi), "--install-root", str(root), "--systemctl", shim]) == 0
    out = capsys.readouterr().out
    assert "DRIFT" not in out and "UNKNOWN" not in out, out
    assert "user@ MemoryHigh" in out and "oomd SwapUsedLimit" in out
    assert "memory_alarm (config:crons)" in out and "mem_cap.systemd_run_usable" in out


def test_one_drift_exits_one_naming_the_row(tmp_path, monkeypatch, capsys):
    agi, root, shim = _fixture(tmp_path, monkeypatch)
    fact = json.loads(os.environ["PROBE_FACTORY"])
    fact["system"][f"user@{os.getuid()}.service"]["MemoryHigh"] = f"{int(BASE * 0.9) + 1}M"
    os.environ["PROBE_FACTORY"] = json.dumps(fact)
    assert probe.main(["--root", str(agi), "--install-root", str(root), "--systemctl", shim]) == 1
    assert "DRIFT: user@ MemoryHigh" in capsys.readouterr().out


def test_a_drifted_drop_in_file_is_its_own_row(tmp_path, monkeypatch, capsys):
    agi, root, shim = _fixture(tmp_path, monkeypatch)
    (root / f"etc/systemd/system/user@{os.getuid()}.service.d/50-sanctuary-guard.conf").write_text("")
    assert probe.main(["--root", str(agi), "--install-root", str(root), "--systemctl", shim]) == 1
    assert "DRIFT: user@ drop-in" in capsys.readouterr().out


def test_user_at_is_asked_of_the_system_manager(tmp_path, monkeypatch):
    """THE DH.434 DEFECT.  The USER manager answers `infinity` for user@<uid>,
    which blanks every ratio row.  Assert the manager, not just the outcome."""
    agi, root, shim = _fixture(tmp_path, monkeypatch)
    probe.rows(agi, root, shim)
    unit = f"user@{os.getuid()}.service"
    asks = [c for c in _calls(tmp_path) if c[-1] == unit and _verb(c) == "show"]
    assert asks and all("--user" not in c for c in asks), asks
    assert probe.main(["--root", str(agi), "--install-root", str(root), "--systemctl", shim]) == 0


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
    table = _by_name(probe.rows(agi, root, shim))
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
    assert probe.main(["--root", str(agi), "--install-root", str(root), "--systemctl", shim]) == 1
    table = _by_name(probe.rows(agi, root, shim))
    assert table["reserve (derived, informational)"][0] == pytest.approx(942.0)
    assert probe.as_mib(table["user@ MemoryMax"][0]) == pytest.approx(6912.0)


def test_only_read_verbs_reach_systemctl_and_nothing_is_written(tmp_path, monkeypatch):
    agi, root, shim = _fixture(tmp_path, monkeypatch)

    def tree_hash(p: pathlib.Path) -> str:
        h = hashlib.sha256()
        for f in sorted(p.rglob("*")):
            h.update(str(f.relative_to(p)).encode() + (f.read_bytes() if f.is_file() else b""))
        return h.hexdigest()

    before = tree_hash(root)
    probe.main(["--root", str(agi), "--install-root", str(root), "--systemctl", shim])
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
    assert probe.main(["--root", str(agi), "--install-root", str(root), "--systemctl", shim]) == 1
    table = _by_name(probe.rows(agi, root, shim))
    assert table["user@ MemoryHigh"][1] is None
    assert table["user@ MemoryHigh"][2] in ("DRIFT", "UNKNOWN")
    assert table["reserve (derived, informational)"][0] is None


def test_missing_drop_in_is_a_drift(tmp_path, monkeypatch):
    agi, root, shim = _fixture(tmp_path, monkeypatch)
    (root / f"etc/systemd/system/user@{os.getuid()}.service.d/50-sanctuary-guard.conf").unlink()
    table = _by_name(probe.rows(agi, root, shim))
    assert table["user@ drop-in"][2] == "DRIFT"


def test_mem_cap_row_comes_from_the_cache_not_a_spawn(tmp_path, monkeypatch):
    monkeypatch.delenv("AGI_MEMCAP_SYSTEMD_RUN", raising=False)
    monkeypatch.setattr(probe.mem_cap, "_read_cached_probe", lambda cfg: True)
    agi, root, shim = _fixture(tmp_path, monkeypatch)
    table = _by_name(probe.rows(agi, root, shim))
    assert table["mem_cap.systemd_run_usable"] == (True, True, "ok")
