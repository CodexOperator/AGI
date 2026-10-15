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
sys.path.insert(0, str(HERE))
import render  # noqa: E402  the kit's sizing(): the ONE memory arithmetic

SCALERS = {"": 1 / 1048576.0, "K": 1 / 1024.0, "M": 1.0, "G": 1024.0, "T": 1048576.0}
OK_TOL = 0.05                      # MiB: the installer writes whole MiB, off-by-one IS drift
READ_VERBS = ("show", "is-active")  # the ONLY verbs this probe may ever call

# (row, unit, manager "s"|"u", prop, kind, target)  kind: ratio | swap | mem | eq |
# is-active | present.  A target is a DSL over the `values.boxkit.*` cells and the
# memory targets render.sizing() derives from config:guard on the installed user@
# max (goal:g7.16.1.5.5.4) -- no sizing constant is written in this file:  "base"
# the installed user@ max itself, "mem:<cell>" a systemd memory string, "eq:<cell>" an exact string, "lit:<v>" a
# fact with no cell behind it, None no target at all.  No cell -> INFORMATION.
UNITS = [
    ("user@ MemoryMax", "user@{uid}.service", "s", "MemoryMax", "ratio", "base"),
    ("user@ MemoryHigh", "user@{uid}.service", "s", "MemoryHigh", "ratio", "mem:USER_HIGH"),
    ("user@ MemorySwapMax", "user@{uid}.service", "s", "MemorySwapMax", "swap", "mem:USER_SWAP"),
    ("user@ MemoryLow", "user@{uid}.service", "s", "MemoryLow", "mem", "mem:MEM_LOW"),
    ("user@ TasksMax", "user@{uid}.service", "s", "TasksMax", "eq", "eq:USER_TASKS"),
    ("user.slice MemoryLow", "user.slice", "s", "MemoryLow", "mem", "mem:MEM_LOW"),
    ("user-<uid>.slice MemoryLow", "user-{uid}.slice", "s", "MemoryLow", "mem", "mem:MEM_LOW"),
    ("system.slice MemoryMin", "system.slice", "s", "MemoryMin", "mem", "mem:SYSTEM_MIN"),
    ("agi.slice MemoryHigh", "agi.slice", "u", "MemoryHigh", "ratio", "mem:AGI_HIGH"),
    ("agi.slice MemoryMax", "agi.slice", "u", "MemoryMax", "ratio", "mem:AGI_MAX"),
    ("agi-memguard.service active", "agi-memguard.service", "s", None, "is-active", "lit:active"),
    ("OOMPolicy claude-remote-control", "claude-remote-control.service", "u", "OOMPolicy", "eq", "eq:OOM_POLICY"),
    ("OOMPolicy streamer-stub", "streamer-stub.service", "u", "OOMPolicy", "eq", "eq:OOM_POLICY"),
    ("OOMPolicy streamer-stub-watch", "streamer-stub-watch.service", "u", "OOMPolicy", "eq", "eq:OOM_POLICY"),
]
# (row, dest_cell, dest_rel or "" when the cell is the file, key, kind, target)
# MANIFEST SWAP (KIT CONTRACT): every `dest_rel` below is the manifest's
# `dest_cell` + `dest_rel` pair for that piece -- ONE table, no literal
# anywhere else in this file.  When g7.33.18.1's manifest.json lands, each
# row here reads ITS OWN manifest row (name/template/dest_cell/dest_rel) and
# this table collapses into the index that says which manifest row is which.
FILES = [
    ("user@ drop-in", "systemd_system_dir", "user@{uid}.service.d/50-sanctuary-guard.conf", None, "present", None),
    ("oomd SwapUsedLimit", "systemd_conf_dir", "oomd.conf.d/50-sanctuary-guard.conf", "SwapUsedLimit", "eq", "eq:OOMD_SWAP_PCT"),
    ("oomd DefaultMemoryPressureLimit", "systemd_conf_dir", "oomd.conf.d/50-sanctuary-guard.conf", "DefaultMemoryPressureLimit", "eq", "eq:OOMD_PRESSURE_PCT"),
    ("oomd DefaultMemoryPressureDurationSec", "systemd_conf_dir", "oomd.conf.d/50-sanctuary-guard.conf", "DefaultMemoryPressureDurationSec", "eq", "eq:OOMD_PRESSURE_SEC"),
    ("user.slice drop-in MemoryLow", "systemd_system_dir", "user.slice.d/50-sanctuary-guard.conf", "MemoryLow", "mem", "mem:MEM_LOW"),
    ("user-<uid>.slice drop-in MemoryLow", "systemd_system_dir", "user-{uid}.slice.d/50-sanctuary-guard.conf", "MemoryLow", "mem", "mem:MEM_LOW"),
    ("system.slice drop-in MemoryMin", "systemd_system_dir", "system.slice.d/50-sanctuary-guard.conf", "MemoryMin", "mem", "mem:SYSTEM_MIN"),
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
    """One READ-ONLY systemctl ask, and the ONLY door to systemctl in this file.
    A verb outside READ_VERBS raises here rather than reaching the box: the
    read-only claim is fail-closed in code, not in a reviewer's good intentions.
    A value that smuggled a command in is DATA below and is never executed."""
    verb = argv[argv.index("--user") + 1] if "--user" in argv else argv[0]
    if verb not in READ_VERBS:
        raise ValueError(f"probe.py refuses a non-read systemctl verb: {verb!r}")
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


def resolve(vals, spec, base, swap):
    """A target DSL -> (want, informational).  Every want comes from a
    `values.boxkit.*` cell read at runtime and UNIT-NORMALISED: a "1024M" cell
    PARSES, it never string-compares against a parsed value.  A cell the kit
    does not carry is INFORMATION (flag True) -- never `ok`."""
    if spec is None:
        return None, True
    mode, _, arg = spec.partition(":")
    if mode == "base":
        return base, False
    if mode == "lit":
        return arg, True
    cell = vals.get(arg)
    if cell is None:
        return None, True                   # no cell for this row
    if cell == "":
        return None, False                  # a sized target whose BASE is missing: UNKNOWN
    return cell, False                      # mem / eq: a systemd string, parsed later


def _same(a: str, b: str) -> bool:
    """Equality in the UNIT the cell is written in: the config's percent cell is
    '90' and the drop-in systemd reads is '90%' -- the same target, so a string
    compare that drifts on the '%' is the bug this whole change is about."""
    return a == b or (a.rstrip("%") == b.rstrip("%") and a.rstrip("%").isdigit())


def judge(got, want, kind, tol: float = OK_TOL, info: bool = False) -> str:
    """Three states, never two: a row that cannot be JUDGED is UNKNOWN and
    UNKNOWN is NOT ok.  A read-back that cannot read back must not report clean.
    A row that cannot be READ (nothing installed, empty answer) is DRIFT.
    `info` = the kit has no target cell here: a healthy row prints `info` and
    NEVER `ok`; an unhealthy one is still DRIFT."""
    if got is None or got == "":
        return "DRIFT"                      # the layer is not installed here
    if want is None or want == "":
        return "info" if info else "UNKNOWN"
    if kind in ("eq", "is-active"):
        good = _same(str(got).strip(), str(want).strip())
    elif kind in ("mem", "ratio", "swap"):
        g, w = as_mib(got), as_mib(want)
        if g is None or w is None:
            return "UNKNOWN"                # infinity, or no base to judge against
        good = abs(g - w) <= tol
    else:
        good = True                         # presence row: an answer == present
    return ("info" if info else "ok") if good else "DRIFT"


def cached_usable(cfg: "dict | None" = None):
    """mem_cap's boot-cached verdict, READ WITHOUT TOUCHING THE BOX.

    mem_cap._read_cached_probe() is NOT read-only: it goes through
    _probe_cache_path -> _private_dir, which `mkdir(parents=True, mode=0o700)`
    and `os.chmod(0o700)`s under $XDG_RUNTIME_DIR before any read, so a
    read-only caller CREATED a directory on the box.  This takes the path from
    mem_cap._cache_path_pure -- ONE place computes it, and that function
    creates nothing -- and then only READS: `_trusted_cache_file` (a regular
    file we own; a symlink or a foreign file is not followed), the boot-id
    check, and the value parse.  No mkdir, no chmod, no write, no spawn."""
    path = mem_cap._cache_path_pure(cfg)
    if path is None:
        return None
    path = mem_cap._trusted_cache_file(path)      # a symlink or a foreign file is not read
    if path is None:
        return None
    try:
        boot, _, val = path.read_text().strip().partition(" ")
    except OSError:
        return None
    return val == "1" if val in ("0", "1") and boot == mem_cap._boot_id() else None


def run_usable(cfg: "dict | None" = None):
    """The mem_cap row, READ-ONLY: env force or the cached verdict, never a spawn."""
    forced = (os.environ.get("AGI_MEMCAP_SYSTEMD_RUN") or "").strip()
    return (forced not in ("0", "false", "False", "no") if forced else cached_usable(cfg))


def rows(root: pathlib.Path, install_root: pathlib.Path, systemctl: str = "systemctl",
         held_outside_user_mib: "float | None" = None) -> list:
    pb, home = cells(root), os.path.expanduser("~")
    uid = os.getuid()
    sub = {"uid": uid, "home": home}
    def dest(cell: str, rel: str) -> pathlib.Path:
        return install_root / pb[cell].replace("{home}", home) / rel

    base = mib(show(systemctl, f"user@{uid}.service", "MemoryMax", False))
    swap = meminfo(install_root, "SwapTotal")
    total = meminfo(install_root, "MemTotal")
    cfg_all = json.loads((root / "config.json").read_text())
    vals = dict((cfg_all.get("values") or {}).get("boxkit") or {})
    # goal:g7.16.1.5.5.4: every memory target is guard-init's own arithmetic over THIS
    # box's config:guard cells on the INSTALLED user@ max -- never a boxkit number. No
    # base (or no SwapTotal) empties only the targets derived from it: they judge
    # UNKNOWN, never ok, and every base-independent target is still judged.
    sizing_refused = None
    try:                                    # no base -> only the base-derived targets blank
        sized = render.sizing(base, swap, render.guard_cells(root), total)
    except render.KitError as err:
        sized, sizing_refused = {}, str(err)    # its targets read UNKNOWN; the row below names why
    vals.update({k: sized.get(k, "") for k in render.MEMORY})
    # g7.33.18 9b03554ac: the reserve is DERIVED, never a fixed 2 GiB and never
    # a default.  `held_outside_user_mib` is a PER-BOX INPUT with no config cell
    # yet, so it is a REQUIRED flag: without it the reserve is UNKNOWN -- never
    # a number, never a pass, and a non-zero exit.
    if held_outside_user_mib is not None and total is not None and base is not None:
        # A NEGATIVE reserve is not information: user@ has been committed more
        # than the box has left after everything held outside it -- an
        # OVER-COMMITTED box is DRIFT and must reach the exit code.  Only a
        # healthy margin stays informational, and a MISSING input stays
        # UNKNOWN (never a number, never a pass).
        res = total - float(held_outside_user_mib) - base
        out = [("reserve (derived)", res, "info", "DRIFT" if res < 0 else "info")]
    else:
        out = [("reserve (derived)", "UNKNOWN", "UNKNOWN", "UNKNOWN")]
    # g7.33.18.1's manifest: a layer this table does not cover is not covered, and
    # saying so is information, not a verdict.  No row here is manifest-only, so
    # this probe never exits 2 -- every layer is read from the live installed bytes.
    man = root.parent / pathlib.Path(pb["templates_dir"]) / "manifest.json"
    out.append(("kit manifest (g7.33.18.1)", "present" if man.is_file() else "absent", "info", "info"))
    if sizing_refused:
        out.append(("config:guard sizing", sizing_refused, "every line sized", "UNKNOWN"))
    for name, unit_t, mgr, prop, kind, spec in UNITS:
        unit = unit_t.format(**sub)
        # user@'s caps were installed as WHOLE MiB, so 0.05 still catches an
        # off-by-one there; the rest got 1 MiB of slack.
        tol = OK_TOL if (kind != "swap" and unit.startswith("user@")) else 1.0
        if kind == "is-active":
            got = run(systemctl, (["--user"] if mgr == "u" else []) + ["is-active", unit]).strip()
        else:
            raw = show(systemctl, unit, prop, mgr == "u")
            got = mib(raw) if kind in ("mem", "ratio", "swap") else raw
        want, info = resolve(vals, spec, base, swap)
        out.append((name, got, want, judge(got, want, kind, tol, info)))
    for name, cell, rel_t, key, kind, spec in FILES:
        where = dest(cell, rel_t.format(**sub))
        got = key_in(where.read_text() if where.is_file() else "", key)
        want, info = resolve(vals, spec, base, swap)
        out.append((name, got, want, judge(got, want, kind, 1.0, info)))
    try:
        jobs = crons.load_crons_node(root)["jobs"]
        alarm = jobs.get("memory_alarm") or {}
        got = "present" if alarm.get("enabled") else "absent"
    except Exception:
        got = None
    out.append(("memory_alarm (config:crons)", got, "present",
                judge(got, "present", "present", OK_TOL, True)))
    # The spawn cells ARE the target: the row asks whether the config parses and
    # whether mem_cap's resolvers return it -- not whether it equals a literal.
    # ...and a container that is not a dict is ABSENT, not a crash. The reader
    # owns that guard (mem_cap._spawn_block) and the probe CALLS it rather than
    # re-deciding `isinstance(spawn, dict)` here: one source per rule, and the
    # same reuse the cache rows above already make of mem_cap privates. A second
    # copy would let the two readers drift -- a shape the reader learns to guard
    # would still kill the table.
    spawn_cfg = mem_cap._spawn_block(cfg_all)
    for cell, resolved in (("memory_max", mem_cap.resolve_memory_cap(cfg_all)),
                           ("tasks_max", mem_cap.resolve_tasks_max(cfg_all))):
        want = spawn_cfg.get(cell)
        out.append((f"spawn.{cell}", want, resolved,
                    "info" if want is None else
                    judge(str(want), str(resolved), "eq")))
    usable = run_usable(cfg_all)
    out.append(("mem_cap.systemd_run_usable", usable, True,
                "UNKNOWN" if usable is None else judge(usable, True, "eq")))
    return out


def main(argv=None) -> int:
    ap = argparse.ArgumentParser(prog="probe.py")
    ap.add_argument("--root", default=str(HERE.parents[2] / ".agi"))  # graph root
    ap.add_argument("--install-root", default=None)                  # else the cell's
    ap.add_argument("--systemctl", default="systemctl")
    ap.add_argument("--held-outside-user-mib", type=float, default=None,
                    help="this box's non-user resident set in MiB; REQUIRED for the "
                         "reserve row (no config cell yet), and the row is UNKNOWN without it")
    a = ap.parse_args(argv)
    root = pathlib.Path(a.root)
    table = rows(root, pathlib.Path(a.install_root or cells(root)["install_root"]),
                 a.systemctl, a.held_outside_user_mib)
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
