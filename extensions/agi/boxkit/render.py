#!/usr/bin/env python3
"""render.py -- the boxkit render helper (hyp:box-memory-guard-pieces-are-repo-templates-that-render-to-the-live-bytes).
One template per live piece under the cell paths.boxkit.templates_dir, one manifest row per piece. No literal
path and no host token lives here: a destination is the cell named by dest_cell joined under install_root, the
kit's own knobs come from values.boxkit.* (config -- the ONE source; there is no defaults.json), the per-box
inputs are ARGUMENTS (measured, never a cell), and the identity tokens come from host_tokens() -- the running
engine checkout and the paths.boxkit.guard_dir cell. An unfilled placeholder is refused BY NAME."""
from __future__ import annotations
import json, os, pwd, re
from pathlib import Path

HERE = Path(__file__).resolve().parent
PH = re.compile(r"\{\{([A-Z][A-Z0-9_]*)\}\}")
PER_BOX = ("MEM_TOTAL", "SYS_RESERVE", "HELD_OUT", "SWAP_TOTAL")
RATIOS = (("USER_HIGH", "user_high_ratio"), ("AGI_HIGH", "agi_high_ratio"),
          ("AGI_MAX", "agi_max_ratio"), ("WORK_HIGH", "work_high_ratio"),
          ("WORK_MAX", "work_max_ratio"))

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

def values(cfg, per_box=None, overrides=None):
    """values.boxkit.* is the ONE source for the kit's knobs; the per-box inputs are
    ARGUMENTS (measured on this box, never a cell); caller overrides win over both."""
    v = dict(cfg.get("values", {}).get("boxkit", {}) or {})
    v.update(per_box or {})
    if missing := [k for k in PER_BOX if k not in v]:
        raise KitError("boxkit: per-box input(s) %s are ARGUMENTS, not cells: pass "
                       "values(cfg, per_box={...}) with the measured values" % ", ".join(missing))
    v.update(overrides or {})
    v["USER_MAX"] = v["MEM_TOTAL"] - v["SYS_RESERVE"] - v["HELD_OUT"]
    for name, ratio in RATIOS:
        v[name] = int(v[ratio] * v["USER_MAX"])
    v["USER_SWAP"] = int(v["swap_ratio"] * v["SWAP_TOTAL"])
    for k in ("USER_MAX", "USER_HIGH", "USER_SWAP", "AGI_HIGH", "AGI_MAX", "WORK_HIGH", "WORK_MAX"):
        v[k] = "%dM" % v[k]          # systemd sizes carry the M suffix; the ratios truncate
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
