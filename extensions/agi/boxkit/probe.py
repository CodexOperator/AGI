#!/usr/bin/env python3
"""probe.py -- goal:g7.33.18's READ-ONLY read-back: prints (layer, value on THIS
box, value SIZING wants, ok|drift|unknown) for every layer the director listed and
exits non-zero on any drift.  Only file reads under the boxkit install_root, a
`systemctl show` / `systemctl is-active` read, and graph/config reads: no write, no
sudo, no unit change.  Paths are paths.boxkit cells; the SIZING ratios are below.

MANAGER (the DH.434 bug): the SYSTEM manager owns user@<uid>.service, user.slice,
user-<uid>.slice, system.slice, oomd.* and every plain system unit; asking the USER
manager for those returns `infinity` on a real box and silently blanks the table.
The USER manager owns agi.slice and the other per-user units.  Every row carries
its manager; nothing is asked of the wrong one.
"""
from __future__ import annotations
import argparse, json, os, pathlib, re, subprocess, sys

HERE = pathlib.Path(__file__).resolve().parent
sys.path.insert(0, str(HERE.parent / "bin"))
import mem_cap  # noqa: E402
import crons  # noqa: E402

SCALERS = {"": 1 / 1048576.0, "K": 1 / 1024.0, "M": 1.0, "G": 1024.0, "T": 1048576.0}
OK_TOL = 0.05                      # MiB: the installer writes whole MiB, off-by-one IS drift
OOMD_DROPIN = "oomd.conf.d/50-sanctuary-guard.conf"

# (row, unit, manager "s"|"u", prop, kind, target)  kind: ratio | present | eq | is-active
UNITS = [
    ("user@ MemoryMax", "user@{uid}.service", "s", "MemoryMax", "ratio", 1.00),
    ("user@ MemoryHigh", "user@{uid}.service", "s", "MemoryHigh", "ratio", 0.90),
    ("user@ MemorySwapMax", "user@{uid}.service", "s", "MemorySwapMax", "ratio", "swap"),
    ("user@ MemoryLow", "user@{uid}.service", "s", "MemoryLow", "present", None),
    ("user@ TasksMax", "user@{uid}.service", "s", "TasksMax", "present", None),
    ("user.slice MemoryLow", "user.slice", "s", "MemoryLow", "present", None),
    ("user-<uid>.slice MemoryLow", "user-{uid}.slice", "s", "MemoryLow", "present", None),
    ("system.slice MemoryMin", "system.slice", "s", "MemoryMin", "present", None),
    ("agi.slice MemoryHigh", "agi.slice", "u", "MemoryHigh", "ratio", 0.63),
    ("agi.slice MemoryMax", "agi.slice", "u", "MemoryMax", "ratio", 0.70),
    ("agi-memguard.service active", "agi-memguard.service", "s", None, "is-active", "active"),
    ("OOMPolicy claude-remote-control", "claude-remote-control.service", "u", "OOMPolicy", "eq", "continue"),
    ("OOMPolicy streamer-stub", "streamer-stub.service", "u", "OOMPolicy", "eq", "continue"),
    ("OOMPolicy streamer-stub-watch", "streamer-stub-watch.service", "u", "OOMPolicy", "eq", "continue"),
]
# (row, dest_cell, dest_rel or "" when the cell is the file, key, kind, target)
FILES = [
    ("user@ drop-in", "systemd_system_dir", "user@{uid}.service.d/50-sanctuary-guard.conf", None, "present", None),
    ("oomd SwapUsedLimit", "systemd_conf_dir", OOMD_DROPIN, "SwapUsedLimit", "eq", "90%"),
    ("oomd DefaultMemoryPressureLimit", "systemd_conf_dir", OOMD_DROPIN, "DefaultMemoryPressureLimit", "eq", "60%"),
    ("oomd DefaultMemoryPressureDurationSec", "systemd_conf_dir", OOMD_DROPIN, "DefaultMemoryPressureDurationSec", "eq", "20s"),
    ("user.slice drop-in MemoryLow", "systemd_system_dir", "user.slice.d/50-sanctuary-guard.conf", "MemoryLow", "present", None),
    ("user-<uid>.slice drop-in MemoryLow", "systemd_system_dir", "user-{uid}.slice.d/50-sanctuary-guard.conf", "MemoryLow", "present", None),
    ("system.slice drop-in MemoryMin", "systemd_system_dir", "system.slice.d/50-sanctuary-guard.conf", "MemoryMin", "present", None),
    ("agi.slice drop-in", "user_systemd_dir", "agi.slice.d/50-agi.conf", None, "present", None),
    ("watchdog.conf test-binary", "watchdog_conf", "", "test-binary", "present", None),
    ("memguard script", "sbin_dir", "agi-memguard.py", None, "present", None),
]


def mib(value):
    m = re.fullmatch(r"(\d+(?:\.\d+)?)\s*([KMGT]?)B?", str(value).strip())
    return float(m[1]) * SCALERS[m[2]] if m else None


def as_mib(value):
    """A number is already MiB; a systemd string is parsed.  Mixing the two is
    how a want of 7365.0 silently becomes 0.007 (bytes) and every row drifts."""
    return value if isinstance(value, (int, float)) and not isinstance(value, bool) else mib(value)


def cells(root: pathlib.Path) -> dict:
    return json.loads((root / "config.json").read_text())["paths"]["boxkit"]


def values(root: pathlib.Path) -> dict:
    return (json.loads((root / "config.json").read_text()).get("values") or {}).get("boxkit") or {}


def run(systemctl: str, argv) -> str:
    """One READ-ONLY systemctl ask.  `show` and `is-active` are read verbs; no
    mutation verb is ever reachable from here."""
    return subprocess.run([systemctl] + argv, capture_output=True, text=True, check=False).stdout


def show(systemctl: str, unit: str, prop: str, user: bool) -> str:
    argv = (["--user"] if user else []) + ["show", "--value", "-p", prop, unit]
    for line in run(systemctl, argv).splitlines():
        if line.strip():
            return line.strip()
    return ""


def key_in(text: str, key: "str | None") -> "str | None":
    if key is None:
        return "present" if text.strip() else None
    pat = re.compile(r"^\s*" + re.escape(key) + r"\s*=\s*(.*?)\s*$")   # watchdog.conf spaces its '='
    for line in text.splitlines():
        m = pat.match(line)
        if m:
            return m[1]
    return None


def meminfo(install_root: pathlib.Path, key: str):
    """MemTotal / SwapTotal from THIS box's own /proc, under install_root."""
    try:
        for line in (install_root / "proc" / "meminfo").read_text().splitlines():
            if line.startswith(key + ":"):
                return float(line.split()[1]) / 1024.0      # kB -> MiB
    except OSError:
        return None
    return None


def judge(got, want, kind, tol: float = OK_TOL) -> str:
    """Three states, never two: a row that cannot be JUDGED is UNKNOWN and
    UNKNOWN is NOT ok.  A read-back that cannot read back must not report clean.
    A row that cannot be READ (nothing installed, empty answer) is DRIFT."""
    if got is None or got == "":
        return "DRIFT"                      # the layer is not installed here
    if kind in ("eq", "is-active"):
        return "ok" if str(got) == str(want) else "DRIFT"
    if kind != "ratio":
        return "ok"                         # presence row: an answer == present
    g, w = as_mib(got), as_mib(want)
    if g is None or w is None:
        return "UNKNOWN"                    # infinity, or no base to judge against
    return "ok" if abs(g - w) <= tol else "DRIFT"


def run_usable():
    """The mem_cap row, READ-ONLY: env force or the cached verdict, never a spawn."""
    forced = (os.environ.get("AGI_MEMCAP_SYSTEMD_RUN") or "").strip()
    return (forced not in ("0", "false", "False", "no") if forced
            else mem_cap._read_cached_probe(None))


def rows(root: pathlib.Path, install_root: pathlib.Path, systemctl: str = "systemctl") -> list:
    pb, home = cells(root), os.path.expanduser("~")
    uid = os.getuid()
    sub = {"uid": uid, "home": home}
    def dest(cell: str, rel: str) -> pathlib.Path:
        return install_root / pb[cell].replace("{home}", home) / rel

    base = mib(show(systemctl, f"user@{uid}.service", "MemoryMax", False))
    swap = meminfo(install_root, "SwapTotal")
    held = float(values(root).get("held_outside_user_mib", 0) or 0)
    total = meminfo(install_root, "MemTotal")
    # SIZING v2 (g7.33.18 9b03554ac): the reserve is DERIVED from the installed
    # user@ MemoryMax, never a fixed 2 GiB and never a default.
    reserve = None if (total is None or base is None) else total - held - base
    out = [("reserve (derived, informational)", reserve, "info", "info")]
    # g7.33.18.1's manifest: a layer this table does not cover is not covered, and
    # saying so is information, not a verdict.  No row here is manifest-only, so
    # this probe never exits 2 -- every layer is read from the live installed bytes.
    man = root.parent / pathlib.Path(pb["templates_dir"]) / "manifest.json"
    out.append(("kit manifest (g7.33.18.1)", "present" if man.is_file() else "absent", "info", "info"))
    for name, unit_t, mgr, prop, kind, tgt in UNITS:
        unit = unit_t.format(**sub)
        # user@'s caps were installed as WHOLE MiB, so 0.05 still catches an
        # off-by-one there; agi.slice and the swap cap were installed as the raw
        # ratio in BYTES (4864344064 B = 4639.95 MiB), so they get 1 MiB.
        tol = 1.0 if (tgt == "swap" or not unit.startswith("user@")) else OK_TOL
        # the installer writes WHOLE MiB, so the want is the rounded ratio: judged
        # against the same rounding, 0.05 MiB still catches a real off-by-one.
        if kind == "is-active":
            got = run(systemctl, (["--user"] if mgr == "u" else []) + ["is-active", unit]).strip()
            want: "str | float" = tgt
        else:
            raw = show(systemctl, unit, prop, mgr == "u")
            got = mib(raw) if kind == "ratio" else raw
            want = (tgt if kind == "eq" else
                    None if kind == "present" or base is None else
                    float(round(0.5 * swap)) if tgt == "swap" else float(round(tgt * base)))
        out.append((name, got, want, judge(got, want, kind, tol)))
    for name, cell, rel_t, key, kind, tgt in FILES:
        where = dest(cell, rel_t.format(**sub))
        got = key_in(where.read_text() if where.is_file() else "", key)
        out.append((name, got, tgt, judge(got, tgt, "eq" if kind == "eq" else "present")))
    try:
        jobs = crons.load_crons_node(root)["jobs"]
        alarm = jobs.get("memory_alarm") or {}
        got = "present" if alarm.get("enabled") else "absent"
    except Exception:
        got = None
    out.append(("memory_alarm (config:crons)", got, "present", judge(got, "present", "present")))
    cfg = json.loads((root / "config.json").read_text()).get("spawn") or {}
    for cell, want in (("memory_max", "2G"), ("tasks_max", 150)):
        got = cfg.get(cell)
        out.append((f"spawn.{cell}", got, want, judge(got, want, "eq")))
    usable = run_usable()
    out.append(("mem_cap.systemd_run_usable", usable, True,
                "UNKNOWN" if usable is None else "ok"))
    return out


def main(argv=None) -> int:
    ap = argparse.ArgumentParser(prog="probe.py")
    ap.add_argument("--root", default=str(HERE.parents[2] / ".agi"))  # graph root
    ap.add_argument("--install-root", default=None)                  # else the cell's
    ap.add_argument("--systemctl", default="systemctl")
    a = ap.parse_args(argv)
    root = pathlib.Path(a.root)
    table = rows(root, pathlib.Path(a.install_root or cells(root)["install_root"]), a.systemctl)
    for name, got, want, status in table:
        got_s = f"{got:.0f}" if isinstance(got, float) else str(got)
        want_s = f"{want:.0f}" if isinstance(want, float) else str(want)
        print(f"{name:44} {got_s:>12}  {want_s:>12}  {status}")
        if status in ("DRIFT", "UNKNOWN"):
            print(f"{status}: {name}")
    drift = [n for n, _, _, s in table if s == "DRIFT"]
    unknown = [n for n, _, _, s in table if s == "UNKNOWN"]
    return 1 if drift else 3 if unknown else 0


if __name__ == "__main__":
    raise SystemExit(main())
