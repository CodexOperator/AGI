#!/usr/bin/env python3
"""render.py -- the boxkit render helper (hyp:box-memory-guard-pieces-are-repo-templates-that-render-to-the-live-bytes).
One template per live piece under the cell paths.boxkit.templates_dir, one manifest row per piece. No literal
path and no host token lives here: a destination is the cell named by dest_cell joined under install_root, the
kit's own knobs come from values.boxkit.* (config -- the ONE source; there is no defaults.json), every memory
number comes from config:guard through guard-init.sh's own arithmetic (sizing(), goal:g7.16.1.5.5.4), the per-box
inputs are ARGUMENTS (measured, never a cell), and the identity tokens come from host_tokens() -- the running
engine checkout and the paths.boxkit.guard_dir cell. An unfilled placeholder is refused BY NAME."""
from __future__ import annotations
import json, os, pwd, re
from pathlib import Path

HERE = Path(__file__).resolve().parent
PH = re.compile(r"\{\{([A-Z][A-Z0-9_]*)\}\}")
PER_BOX = ("MEM_TOTAL", "SYS_RESERVE", "HELD_OUT", "SWAP_TOTAL")
GUARD_INIT = HERE.parent / "guard" / "guard-init.sh"
# guard-init's `num_cell VAR NAME DEFAULT ...` / `size_cell VAR NAME DEFAULT` lines
CELL = re.compile(r"\b(?:num|size)_cell [A-Z][A-Z0-9_]* ([A-Z][A-Z0-9_]*) ([0-9][0-9.]*[MG]?)(?=[\s;]|$)", re.M)
#: every placeholder sizing() fills: values.boxkit carries none of them
MEMORY = ("USER_HIGH", "USER_SWAP", "AGI_MAX", "AGI_HIGH", "ENGINE_MAX", "ENGINE_HIGH", "WORK_MAX",
          "WORK_HIGH", "MEM_LOW", "SYSTEM_MIN", "SSH_MIN", "ENGINE_SWAP", "USER_OOM_PCT", "AGI_OOM_PCT",
          "OOMD_SWAP_PCT", "OOMD_PRESSURE_PCT", "OOMD_PRESSURE_SEC", "HEALTH_LIMIT", "HEALTH_GRACE")

class KitError(Exception):
    """A refusal: unfilled placeholder, unknown dest cell, unlisted placeholder."""

def manifest(templates_dir=None):
    return json.loads((Path(templates_dir or HERE / "templates") / "manifest.json").read_text(encoding="utf-8"))

def cell(cfg, name):
    """A committed cell paths.boxkit.<name> (else values.boxkit.<name>), or a refusal naming it."""
    for section in ("paths", "values"):
        got = (cfg.get(section, {}).get("boxkit", {}) or {}).get(name)
        if got:
            return str(got)
    raise KitError("boxkit: paths.boxkit.%s is not a committed cell; the director must commit it "
                   "(the kit never guesses a root)" % name)

def engine_checkout():
    """The MAIN checkout this engine copy belongs to, from the engine's own __file__.

    A linked worktree's `.git` FILE points at <main>/.git/worktrees/<name>; the kit
    resolves through it (reading a file, never shelling out to git) so a render from a
    worktree carries the same roots the live bytes were installed with."""
    root = HERE.parents[2]
    dot = root / ".git"
    if dot.is_file():
        head = dot.read_text(encoding="utf-8").strip()
        if head.startswith("gitdir:"):
            work = Path(head.split(":", 1)[1].strip())
            if not work.is_absolute():
                work = (root / work).resolve()
            return work.parents[2]          # <main>/.git/worktrees/<name> -> <main>
    return root

def expand(cells, value, repo):
    """{home} and {repo_parent} in a path cell, expanded at read time."""
    return Path(str(value).replace("{home}", str(Path.home()))
                .replace("{repo_parent}", str(Path(repo).parent))).expanduser()

def host_tokens(cfg, repo_root=None, guard_dir=None):
    """The identity placeholders: the running engine checkout, the committed guard_dir
    cell, and the box's own user/uid. A caller may pass an explicit root (a probe, another
    box); nothing here walks the checkout by hand."""
    repo = Path(repo_root) if repo_root else engine_checkout()
    guard = Path(guard_dir) if guard_dir else expand(cfg["paths"]["boxkit"],
                                                     cell(cfg, "guard_dir"), repo)
    return {"OWNER_USER": pwd.getpwuid(os.getuid()).pw_name, "UID": str(os.getuid()),
            "REPO_ROOT": str(repo), "GUARD_SRC": str(guard / "guard-init.sh")}

def guard_defaults(src=None):
    """Every memory cell's default, read from guard-init.sh's own cell lines -- never copied here."""
    return dict(CELL.findall(Path(src or GUARD_INIT).read_text(encoding="utf-8")))

def guard_cells(root=None):
    """THIS box's config:guard cells (locations.guard_cell) over guard-init's defaults; an
    empty cell takes the default, as guard-init's hostvar does."""
    import sys
    sys.path.insert(0, str(HERE.parent / "bin"))
    import locations
    root = Path(root) if root else engine_checkout()
    return {k: locations.guard_cell(root, k, d) or d for k, d in guard_defaults().items()}

def _mib(size):
    """guard-init's to_mib: 512M | 2G | 1.5G | bare MiB -> whole MiB, truncated."""
    s = str(size).upper()
    return int(float(s[:-1]) * 1024) if s.endswith("G") else int(float(s.rstrip("M")))

#: the cells sizing() reads -- a guard-init line the CELL regex cannot parse is refused by name
SIZING_CELLS = ("USER_HIGH_PCT", "USER_SWAP_PCT", "USER_SWAP_CAP", "AGI_MAX_PCT", "AGI_HIGH_PCT",
                "ENGINE_MAX", "ENGINE_HIGH_PCT", "WORK_HIGH_PCT", "ENGINE_SWAP_MAX", "CLAUDE_LOW_DIV",
                "CLAUDE_LOW_CAP", "SYSTEM_MIN", "SSH_MIN", "OOMD_LIMIT", "AGI_OOMD_LIMIT",
                "OOMD_SWAP_USED_PCT", "OOMD_PRESSURE_PCT", "OOMD_PRESSURE_S", "PSI_FULL", "GRACE")
#: the placeholders derived from user@'s max: blank (never guessed) when it is unknown
FROM_BASE = ("USER_HIGH", "AGI_MAX", "AGI_HIGH", "WORK_MAX", "WORK_HIGH", "MEM_LOW")

def sizing(user_max, swap_total, g, ram=None):
    """guard-init.sh's arithmetic over the cells `g`, on user@'s max and the box's swap ->
    the kit's memory placeholders. `user_max` None (a probe with no installed user@ cap)
    leaves out only FROM_BASE, `swap_total` None only USER_SWAP; every other target stands.
    Bash $(( )) truncates toward zero and // floors: the two agree on the operands here,
    which are never negative -- a derived line <= 0 or > `ram` is refused before any value
    is returned, as guard-init refuses it (goal:g7.16.1.5.5.8)."""
    if missing := [k for k in SIZING_CELLS if k not in g]:
        raise KitError("boxkit: guard-init cell line(s) %s not parsed from %s"
                       % (", ".join(missing), GUARD_INIT.name))
    n = lambda k: int(g[k])
    engine_max, engine_swap = _mib(g["ENGINE_MAX"]), _mib(g["ENGINE_SWAP_MAX"])
    sizes = {"ENGINE_MAX": engine_max, "ENGINE_HIGH": engine_max * n("ENGINE_HIGH_PCT") // 100,
             "SYSTEM_MIN": _mib(g["SYSTEM_MIN"]), "SSH_MIN": _mib(g["SSH_MIN"])}
    if swap_total is not None:
        sizes["USER_SWAP"] = min(int(swap_total) * n("USER_SWAP_PCT") // 100, _mib(g["USER_SWAP_CAP"]))
    if user_max is not None:
        u = int(user_max)
        if u <= 0:
            raise KitError("boxkit: user@'s max is %dM: config:guard leaves it nothing" % u)
        agi_max = u * n("AGI_MAX_PCT") // 100
        work_max = agi_max - engine_max
        sizes.update(USER_HIGH=u * n("USER_HIGH_PCT") // 100, AGI_MAX=agi_max,
                     AGI_HIGH=agi_max * n("AGI_HIGH_PCT") // 100, WORK_MAX=work_max,
                     WORK_HIGH=max(work_max, 0) * n("WORK_HIGH_PCT") // 100,
                     MEM_LOW=min(u // n("CLAUDE_LOW_DIV"), _mib(g["CLAUDE_LOW_CAP"])))
    bad = sorted(k for k in ("USER_HIGH", "AGI_MAX", "AGI_HIGH", "ENGINE_MAX", "ENGINE_HIGH",
                             "WORK_MAX", "WORK_HIGH", "MEM_LOW")
                 if k in sizes and (sizes[k] <= 0 or (ram is not None and sizes[k] > int(ram))))
    bad += [k for k in ("SYSTEM_MIN", "SSH_MIN")             # MemoryMin: 0 legal, > RAM not
            if ram is not None and sizes[k] > int(ram)]
    if bad:
        raise KitError("boxkit: config:guard sizes %s to <= 0 or more than RAM: %s"
                       % (", ".join(bad), {k: sizes[k] for k in bad}))
    out = {k: "%dM" % x for k, x in sizes.items()}
    out.update(ENGINE_SWAP="%dM" % engine_swap if engine_swap else "0",
               USER_OOM_PCT=str(n("OOMD_LIMIT")), AGI_OOM_PCT=str(n("AGI_OOMD_LIMIT")),
               OOMD_SWAP_PCT=str(n("OOMD_SWAP_USED_PCT")), OOMD_PRESSURE_PCT=str(n("OOMD_PRESSURE_PCT")),
               OOMD_PRESSURE_SEC="%ds" % n("OOMD_PRESSURE_S"),
               HEALTH_LIMIT=str(n("PSI_FULL")), HEALTH_GRACE=str(n("GRACE")))
    return out

def values(cfg, per_box=None, overrides=None, guard=None):
    """values.boxkit.* is the ONE source for the kit's knobs; the per-box inputs are
    ARGUMENTS (measured on this box, never a cell); caller overrides win over both.
    Every memory number is sizing() over config:guard: `guard` None = THIS box's cells,
    a dict = those cells over guard-init's defaults (another box, a fixture)."""
    v = dict(cfg.get("values", {}).get("boxkit", {}) or {})
    v.update(per_box or {})
    if missing := [k for k in PER_BOX if k not in v]:
        raise KitError("boxkit: per-box input(s) %s are ARGUMENTS, not cells: pass "
                       "values(cfg, per_box={...}) with the measured values" % ", ".join(missing))
    v.update(overrides or {})
    user_max = v["MEM_TOTAL"] - v["SYS_RESERVE"] - v["HELD_OUT"]
    g = guard_cells() if guard is None else {**guard_defaults(), **guard}
    v.update(sizing(user_max, v["SWAP_TOTAL"], g, v["MEM_TOTAL"]), USER_MAX="%dM" % user_max)
    cells = cfg["paths"]["boxkit"]
    v.update(SBIN_ABS="/" + cells["sbin_dir"].lstrip("/"),
             WATCHDOG_CONF="/" + cells["watchdog_conf"].lstrip("/"),
             HEALTH_BIN="/" + cells["sbin_dir"].lstrip("/") + "/sanctuary-health")
    return {k: str(x) for k, x in v.items()}

def render(text, v, name="<text>"):
    missing = sorted(set(PH.findall(text)) - set(v))
    if missing:
        raise KitError("%s: unfilled placeholder(s): %s" % (name, ", ".join(missing)))
    return PH.sub(lambda m: v[m.group(1)], text)

def destination(piece, cells, v, install_root="/"):
    cell = piece["dest_cell"]
    if cell not in cells:
        raise KitError("piece %s names dest_cell %r, not a paths.boxkit cell" % (piece["name"], cell))
    base = str(expand(cells, cells[cell], engine_checkout()))
    return Path(install_root) / base.lstrip("/") / render(piece["dest_rel"], v, piece["name"])

def rendered(piece, v, templates_dir=None):
    text = (Path(templates_dir or HERE / "templates") / piece["template"]).read_text(encoding="utf-8")
    if unlisted := sorted(set(PH.findall(text)) - set(piece["placeholders"])):
        raise KitError("%s: template uses placeholders the manifest does not list: %s"
                       % (piece["name"], ", ".join(unlisted)))
    return render(text, v, piece["name"])

def install(pieces, v, cells, install_root):
    """Write the rendered bytes under a tmp install_root ONLY (the fences).

    There is deliberately no CLI here: a writer aimed at the live cell is a
    foot-gun this kit does not ship until the installer node lands."""
    out = {}
    for piece in pieces:
        dest = destination(piece, cells, v, install_root)
        dest.parent.mkdir(parents=True, exist_ok=True)
        dest.write_text(rendered(piece, v), encoding="utf-8")
        dest.chmod(int(piece["mode"], 8))
        out[piece["name"]] = dest
    return out
