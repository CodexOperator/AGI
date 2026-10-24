"""goal:g7.16.1.11.46.9 (P1) -- pi 1.x beside 0.73.1, and the paired A/B's guards.

Four small pieces, each one a falsifier clause of the leaf, none of them a runner:

- `check_pin`    the side prefix holds exactly the pinned package version + integrity (cell `p1.pin`).
- `old_pi_untouched`  /usr/local/bin/pi still resolves into the 0.73.1 package and prints 0.73.1.
- `mint_capped`  the ONLY way a P1 kid key is minted: a cap on the call, the cap read BACK from
                 the provisioning API, the arm's and the cash total's exposure kept under the cell,
                 one key per (arm, leaf) ever (a capped kid is a counted red, never retried).
- `may_start` / `board_line`  the spawn gate (at most `max_live` live, none while agi.slice is
                 above `slice_gb_max`) and the one board line per arm.

The long-lived provisioning key never leaves `provisioning.mint`; a kid is handed `MintedKey.secret`
only. Cells: `.agi/config.json` `p1` (numbers, pin) and `harnesses.pi1` (the bin + the three arm rows).
"""
from __future__ import annotations

import json
import math
import os
import subprocess
import sys
from pathlib import Path

sys.path.insert(0, str(Path(__file__).resolve().parent))

import provisioning  # noqa: E402

#: The arm that is Messages on credits (Anthropic Console), not an OpenRouter key: it is not mintable here.
CREDITS_ARM = "credits"
SLICE_MEMORY = "/sys/fs/cgroup/agi.slice/memory.current"


class P1Refused(RuntimeError):
    """A P1 guard said no. Every message names the guard and the numbers."""


def cell(cfg: dict) -> dict:
    p = cfg.get("p1")
    if not isinstance(p, dict) or not p.get("pin"):
        raise P1Refused("config cell `p1` (pin, caps) is absent: nothing to check against")
    return p


# --- the pin ---------------------------------------------------------------

def check_pin(prefix: str | Path, cfg: dict) -> list[str]:
    """Problems with the side prefix against the pinned cell; [] = the pin holds.

    Reads the lockfile the install wrote and the installed package.json: the version AND the integrity
    must equal the cell, so a re-resolved or swapped tarball is a problem, not a silent upgrade."""
    pin = cell(cfg)["pin"]
    prefix = Path(os.path.expanduser(str(prefix)))
    out: list[str] = []
    try:
        lock = json.loads((prefix / "package-lock.json").read_text())
        row = lock["packages"][f"node_modules/{pin['package']}"]
    except (OSError, ValueError, KeyError) as exc:
        return [f"no lockfile row for {pin['package']} under {prefix}: {type(exc).__name__}"]
    if row.get("version") != pin["version"]:
        out.append(f"lock version {row.get('version')!r} != pinned {pin['version']!r}")
    if row.get("integrity") != pin["integrity"]:
        out.append(f"lock integrity {row.get('integrity')!r} != pinned integrity")
    try:
        have = json.loads((prefix / "node_modules" / pin["package"] / "package.json").read_text())["version"]
    except (OSError, ValueError, KeyError) as exc:
        out.append(f"installed package.json unreadable: {type(exc).__name__}")
    else:
        if have != pin["version"]:
            out.append(f"installed version {have!r} != pinned {pin['version']!r}")
    return out


def install(prefix: str | Path, cfg: dict) -> list[str]:
    """`npm --prefix` the pinned version, scripts OFF, then `check_pin`. Returns the problems."""
    pin = cell(cfg)["pin"]
    prefix = Path(os.path.expanduser(str(prefix)))
    prefix.mkdir(parents=True, exist_ok=True)
    subprocess.run(["npm", "--prefix", str(prefix), "install", "--ignore-scripts", "--no-audit", "--no-fund",
                    "--save-exact", f"{pin['package']}@{pin['version']}"], check=True)
    return check_pin(prefix, cfg)


def old_pi_untouched(bin_path: str = "/usr/local/bin/pi") -> list[str]:
    """Falsifier 3: the old pi still resolves into the 0.73.1 package and prints 0.73.1."""
    real = os.path.realpath(bin_path)
    out: list[str] = []
    if "@mariozechner/pi-coding-agent" not in real:
        out.append(f"{bin_path} resolves to {real}, not into the @mariozechner 0.73.1 package")
    try:
        ver = subprocess.run([bin_path, "--version"], capture_output=True, text=True, timeout=60)
        said = (ver.stdout + ver.stderr).strip()
    except (OSError, subprocess.SubprocessError) as exc:
        return out + [f"{bin_path} --version did not run: {type(exc).__name__}"]
    if said != "0.73.1":
        out.append(f"{bin_path} --version printed {said!r}, not '0.73.1'")
    return out


# --- the mint ----------------------------------------------------------------

def _ledger(path: Path) -> list[dict]:
    try:
        rows = json.loads(Path(path).read_text())
    except FileNotFoundError:
        return []
    except (OSError, ValueError) as exc:
        raise P1Refused(f"ledger {path} unreadable ({type(exc).__name__}): minting stops, nothing is guessed")
    return rows if isinstance(rows, list) else []


def exposure(rows: list[dict], arm: str | None = None) -> float:
    """Committed dollars: the SUM OF CAPS of every key ever minted (spent or not), for one arm or all cash arms."""
    return sum(float(r["cap"]) for r in rows
               if (arm is None and r["arm"] != CREDITS_ARM) or r["arm"] == arm)


def mint_capped(*, arm: str, leaf: int, cfg: dict, ledger: str | Path,
                root: str | Path | None = None, workspace_id: str | None = None,
                ttl_minutes: int = 90, limit_usd: float | None = None):
    """Mint the ONE capped kid key of (arm, leaf). Raises `P1Refused` rather than mint outside the cell."""
    p = cell(cfg)
    key_cap = float(p["key_cap_usd"])
    if arm == CREDITS_ARM:
        raise P1Refused("the credits arm is Messages on Console credits, not an OpenRouter key: it waits "
                        "for the org link (card-belam §6) and C1-C3; nothing is minted for it here")
    arm_caps = p["arm_cap_usd"]
    if arm not in arm_caps:
        raise P1Refused(f"arm {arm!r} is not one of {sorted(a for a in arm_caps if a != CREDITS_ARM)}")
    if not isinstance(leaf, int) or isinstance(leaf, bool) or not 1 <= leaf <= int(p["leaves"]):
        raise P1Refused(f"leaf {leaf!r} is not 1..{p['leaves']}")
    limit = key_cap if limit_usd is None else limit_usd
    if (isinstance(limit, bool) or not isinstance(limit, (int, float)) or not math.isfinite(limit)
            or limit <= 0 or limit > key_cap):
        raise P1Refused(f"key cap {limit!r} refused at mint: a P1 key carries a finite cap in (0, {key_cap}]")
    rows = _ledger(Path(ledger))
    if any(r["arm"] == arm and r["leaf"] == leaf for r in rows):
        raise P1Refused(f"({arm}, leaf {leaf}) already minted a key: a capped kid is a counted red, never retried")
    if exposure(rows, arm) + limit > float(arm_caps[arm]) + 1e-9:
        raise P1Refused(f"arm {arm}: committed ${exposure(rows, arm):.2f} + ${limit:.2f} would pass the "
                        f"${float(arm_caps[arm]):.2f} arm cap")
    if exposure(rows) + limit > float(p["cash_total_usd"]) + 1e-9:
        raise P1Refused(f"cash: committed ${exposure(rows):.2f} + ${limit:.2f} would pass the "
                        f"${float(p['cash_total_usd']):.2f} cash total")

    minted = provisioning.mint(iter_n="p1", agent_id=f"{arm}-l{leaf}", tier="kid", limit_usd=float(limit),
                               ttl_minutes=ttl_minutes, workspace_id=workspace_id, root=root)
    if minted is None:
        raise P1Refused("no provisioning key readable by this uid: nothing minted (absence is not a fallback "
                        "to a shared key)")
    # Read the cap BACK: the response to a mint is the caller's own claim, the listing is the API's.
    seen = next((r for r in provisioning.list_keys(root, workspace_id) if r.get("hash") == minted.key_hash), None)
    got = None if seen is None else seen.get("limit")
    if got is None or float(got) > key_cap:
        provisioning.revoke(minted.key_hash, root)
        raise P1Refused(f"cap read back as {got!r} for {minted.name}: an uncapped or over-cap key is "
                        f"revoked and refused (cell {key_cap})")
    Path(ledger).write_text(json.dumps(rows + [{"arm": arm, "leaf": leaf, "hash": minted.key_hash,
                                                "cap": float(got)}], indent=1))
    return minted


# --- the spawn gate and the board ---------------------------------------------

def slice_gb(path: str = SLICE_MEMORY) -> float | None:
    """agi.slice memory in GB; None when it cannot be read (the gate then refuses)."""
    try:
        return int(Path(path).read_text().strip()) / 1e9
    except (OSError, ValueError):
        return None


def may_start(live: int, gb: float | None, cfg: dict) -> tuple[bool, str]:
    p = cell(cfg)
    if live >= int(p["max_live"]):
        return False, f"{live} kids live, the bound is {p['max_live']}"
    if gb is None:
        return False, "agi.slice memory unreadable: the gate fails closed"
    if gb > float(p["slice_gb_max"]):
        return False, f"agi.slice {gb:.2f} GB is above {p['slice_gb_max']} GB"
    return True, "ok"


def board_line(model: str, kids: list[dict], leaves: int = 10) -> str:
    """`p1 <model> $/landed=<x> s/landed=<y> red=<r>/10`; `n/a` for both when 0 landed.

    kids: {"landed": bool, "usd": float (the key's provisioning usage read), "secs": float, "red": bool}.
    Every kid's spend counts, landed or not: the cost of an arm is what it burned."""
    landed = sum(1 for k in kids if k["landed"])
    red = sum(1 for k in kids if k["red"])
    if landed == 0:
        cost = secs = "n/a"
    else:
        cost = f"{sum(k['usd'] for k in kids) / landed:.4f}"
        secs = f"{sum(k['secs'] for k in kids) / landed:.0f}"
    return f"p1 {model} $/landed={cost} s/landed={secs} red={red}/{leaves}"


def main(argv: list[str]) -> int:
    root = Path(__file__).resolve().parents[3]
    cfg = json.loads((root / ".agi" / "config.json").read_text())
    cmd = argv[1] if len(argv) > 1 else ""
    if cmd in ("-h", "--help"):
        print(__doc__.strip().split("\n\n")[0])
        print("usage: p1_ab.py install|pin-check [prefix] | old-pi")
        return 0
    prefix = argv[2] if len(argv) > 2 else "~/pi1"
    if cmd == "install":
        problems = install(prefix, cfg)
    elif cmd == "pin-check":
        problems = check_pin(prefix, cfg)
    elif cmd == "old-pi":
        problems = old_pi_untouched()
    else:
        print("usage: p1_ab.py install|pin-check [prefix] | old-pi", file=sys.stderr)
        return 2
    for pr in problems:
        print(f"p1 {cmd}: {pr}")
    print(f"p1 {cmd}: {'OK' if not problems else 'RED'}")
    return 1 if problems else 0


if __name__ == "__main__":
    sys.exit(main(sys.argv))
