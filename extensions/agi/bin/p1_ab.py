"""goal:g7.16.1.11.46.9 (P1) -- pi 1.x beside 0.73.1, and the paired A/B's guards.

Pieces, each one a clause of the leaf's PART 2 RULES or falsifier, none of them a runner:

- `check_pin` / `check_tree` / `seal`  the side prefix holds exactly the pinned package (version + lockfile
                 integrity) AND the bytes sealed at install (a tree digest), re-verified before EVERY arm.
- `old_pi_untouched`  /usr/local/bin/pi still resolves into the 0.73.1 package and prints 0.73.1.
- `mint_capped`  the ONLY way a P1 kid key is minted (run by belam's uid, the only reader of the provisioning
                 key): a frozen leaf id, a cap on the call, the cap AND a non-null expires_at inside the run
                 window read BACK from the provisioning API, exposure kept under the cell, one key per
                 (arm, leaf) ever (a capped kid is a counted red, never retried).
- `write_key_file` / `acl_problems`  a key lives only in its own 0600 file in a 0700 dir, readable by exactly
                 the kid uid through two ACL entries (file r, dir x with no r); never in argv, env, a repo or mail.
- `arm_preflight`  the arm's refusals: leaf off the frozen list, pin/tree mismatch, kid as the key holder,
                 kid worktree not on the frozen base.
- `end_arm`      every key disabled and read back as disabled, its file removed.
- `kid_key` / `kid_done`  belam's thin driver, one kid at a time: mint + write the kid's key file just before the kid
                 starts (at most `max_live` files exist), and after the kid exits read its spend, disable the key,
                 read it back as disabled and remove the file. The kid runs in the director's post uid (agi-kid's
                 model), never belam or root; the secret is in that one file and nowhere else.
- `kid_plan` / `run_kid` / `record_result`  MY side of a kid (the director's post uid): the node >= node_min check
                 (the system node can be too old for pi 1.x), the models.json whose only secret is a PATH
                 (apiKey "!cat <keyfile>"), a whitelisted env without any key, the pinned pi1 command, one
                 bounded run, and one row per (arm, leaf) in the committed results file. NO kid-to-kid key
                 isolation under one uid (council Q-K1): the real bounds are the $0.50 cap with the TTL read back,
                 max_live = 2 key files, and disable + read back + remove at kid end.
- `may_start`    the spawn gate (at most `max_live`, none while agi.slice is above `slice_gb_max`).
- `render_segment` / `merge_pick`  the committed results file -> the `| p1: ...` metrics_line segment text (the
                 ONE metrics writer calls it) and the one-run-per-leaf merge rule. This module never writes a
                 town node.

Cells: `.agi/config.json` `p1` (pin, the frozen leaf ids, the base sha, caps) and `harnesses.pi1` (bin + the arm
rows; NO default row: a spawn naming pi1 without a row is refused at $0).
"""
from __future__ import annotations

import datetime
import hashlib
import json
import math
import os
import re
import shutil
import signal
import stat
import subprocess
import sys
from pathlib import Path

sys.path.insert(0, str(Path(__file__).resolve().parent))

import provisioning  # noqa: E402

#: The arm that is Messages on credits (Anthropic Console), not an OpenRouter key: it is not mintable here.
CREDITS_ARM = "credits"
SLICE_MEMORY = "/sys/fs/cgroup/agi.slice/memory.current"
TREE_FILE = ".p1-tree"
#: Slack between the TTL asked for and the expires_at the API may answer with (clock skew, rounding).
EXPIRY_SLACK = datetime.timedelta(minutes=5)


class P1Refused(RuntimeError):
    """A P1 guard said no. Every message names the guard and the numbers."""


def cell(cfg: dict) -> dict:
    p = cfg.get("p1")
    if not isinstance(p, dict) or not p.get("pin"):
        raise P1Refused("config cell `p1` (pin, caps) is absent: nothing to check against")
    return p


def leaves(cfg: dict) -> list[str]:
    """The ONE source of the leaf set: the frozen goal ids in the cell. n = len(leaves(cfg))."""
    ids = cell(cfg).get("leaves")
    if not isinstance(ids, list) or not ids or not all(isinstance(i, str) and i.startswith("goal:") for i in ids):
        raise P1Refused("config cell `p1.leaves` is not a non-empty list of goal ids")
    return list(ids)


def frozen_problems(cfg: dict, node_text: str) -> list[str]:
    """[] when the cell's leaf list and base equal what goal:g7.16.1.11.46.9 froze: the `FROZEN LIST (...): a · b`
    line of its PART 2 RULES and the `FROZEN BASE (p1.base): <sha>` line of its THOUGHT. One source of truth,
    two places that must agree; a drift in either reads RED."""
    out: list[str] = []
    m = re.search(r"FROZEN LIST \([^)]*\): ((?:goal:[\w.-]+(?: · )?)+)", node_text)
    node_ids = re.findall(r"goal:[\w.-]+", m.group(1)) if m else []
    if not node_ids:
        out.append("the node has no `FROZEN LIST (...): goal:.. · goal:..` line")
    elif node_ids != leaves(cfg):
        out.append(f"cell p1.leaves {leaves(cfg)} != the node's frozen list {node_ids}")
    b = re.search(r"FROZEN BASE \(p1\.base\): ([0-9a-f]{40})", node_text)
    if not b:
        out.append("the node's THOUGHT has no `FROZEN BASE (p1.base): <40 hex>` line")
    elif b.group(1) != cell(cfg).get("base"):
        out.append(f"cell p1.base {cell(cfg).get('base')!r} != the node's frozen base {b.group(1)}")
    return out


def _now() -> datetime.datetime:
    return datetime.datetime.now(datetime.timezone.utc)


# --- the pin and the sealed tree ----------------------------------------------

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


def tree_digest(prefix: str | Path) -> str:
    """sha256 over every file's (relative path, content hash) and every symlink's (path, target) under the
    prefix, sorted; the seal file itself is left out. One changed byte anywhere in the install changes it."""
    prefix = Path(os.path.expanduser(str(prefix)))
    h = hashlib.sha256()
    for dirpath, dirnames, filenames in os.walk(prefix, followlinks=False):
        dirnames.sort()
        for name in sorted(filenames + [d for d in dirnames if os.path.islink(os.path.join(dirpath, d))]):
            p = Path(dirpath) / name
            rel = p.relative_to(prefix).as_posix()
            if rel == TREE_FILE:
                continue
            if p.is_symlink():
                h.update(f"L {rel} {os.readlink(p)}\n".encode())
            else:
                h.update(f"F {rel} {hashlib.sha256(p.read_bytes()).hexdigest()}\n".encode())
    return h.hexdigest()


def seal(prefix: str | Path, cfg: dict) -> None:
    """Record the tree digest AFTER a clean pin check; refuses to seal a prefix that does not hold the pin."""
    problems = check_pin(prefix, cfg)
    if problems:
        raise P1Refused("refusing to seal a prefix that does not hold the pin: " + "; ".join(problems))
    (Path(os.path.expanduser(str(prefix))) / TREE_FILE).write_text(tree_digest(prefix) + "\n")


def check_tree(prefix: str | Path) -> list[str]:
    """[] when the install's bytes equal the sealed digest. An unsealed prefix is a problem, not a pass."""
    prefix = Path(os.path.expanduser(str(prefix)))
    try:
        sealed = (prefix / TREE_FILE).read_text().strip()
    except OSError:
        return [f"{prefix} is not sealed (no {TREE_FILE}): run `p1_ab.py seal` after a clean install"]
    now = tree_digest(prefix)
    return [] if now == sealed else [f"tree digest {now[:12]}... != sealed {sealed[:12]}...: the install changed"]


def install(prefix: str | Path, cfg: dict) -> list[str]:
    """`npm --prefix` the pinned version, scripts OFF, check the pin, seal the tree. Returns the problems."""
    pin = cell(cfg)["pin"]
    prefix = Path(os.path.expanduser(str(prefix)))
    prefix.mkdir(parents=True, exist_ok=True)
    subprocess.run(["npm", "--prefix", str(prefix), "install", "--ignore-scripts", "--no-audit", "--no-fund",
                    "--save-exact", f"{pin['package']}@{pin['version']}"], check=True)
    problems = check_pin(prefix, cfg)
    if not problems:
        seal(prefix, cfg)
    return problems


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


def main_env_denied(path: str | Path) -> list[str]:
    """After P1: the main tree's .env must still be unreadable from THIS uid (no scoped read was ever granted)."""
    try:
        with open(path, "rb"):
            pass
    except PermissionError:
        return []
    except OSError as exc:
        return [f"{path}: {type(exc).__name__}, not the EACCES the rule expects"]
    return [f"{path} is READABLE from uid {os.getuid()}: the provisioning key must stay belam's alone"]


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


def _parse_expiry(raw) -> datetime.datetime | None:
    if not isinstance(raw, str) or not raw:
        return None
    try:
        return datetime.datetime.fromisoformat(raw.replace("Z", "+00:00"))
    except ValueError:
        return None


def mint_capped(*, arm: str, leaf: str, cfg: dict, ledger: str | Path,
                root: str | Path | None = None, workspace_id: str | None = None,
                ttl_minutes: int = 90, limit_usd: float | None = None):
    """Mint the ONE capped kid key of (arm, frozen leaf id). Raises `P1Refused` rather than mint outside the cell."""
    p = cell(cfg)
    key_cap = float(p["key_cap_usd"])
    if arm == CREDITS_ARM:
        raise P1Refused("the credits arm is Messages on Console credits, not an OpenRouter key: it waits "
                        "for the org link (card-belam §6) and C1-C3; nothing is minted for it here")
    arm_caps = p["arm_cap_usd"]
    if arm not in arm_caps:
        raise P1Refused(f"arm {arm!r} is not one of {sorted(a for a in arm_caps if a != CREDITS_ARM)}")
    frozen = leaves(cfg)
    if leaf not in frozen:
        raise P1Refused(f"leaf {leaf!r} is not in the frozen list {frozen}")
    limit = key_cap if limit_usd is None else limit_usd
    if (isinstance(limit, bool) or not isinstance(limit, (int, float)) or not math.isfinite(limit)
            or limit <= 0 or limit > key_cap):
        raise P1Refused(f"key cap {limit!r} refused at mint: a P1 key carries a finite cap in (0, {key_cap}]")
    rows = _ledger(Path(ledger))
    if any(r["arm"] == arm and r["leaf"] == leaf for r in rows):
        raise P1Refused(f"({arm}, {leaf}) already minted a key: a capped kid is a counted red, never retried")
    if exposure(rows, arm) + limit > float(arm_caps[arm]) + 1e-9:
        raise P1Refused(f"arm {arm}: committed ${exposure(rows, arm):.2f} + ${limit:.2f} would pass the "
                        f"${float(arm_caps[arm]):.2f} arm cap")
    if exposure(rows) + limit > float(p["cash_total_usd"]) + 1e-9:
        raise P1Refused(f"cash: committed ${exposure(rows):.2f} + ${limit:.2f} would pass the "
                        f"${float(p['cash_total_usd']):.2f} cash total")

    started = _now()
    minted = provisioning.mint(iter_n="p1", agent_id=f"{arm}-l{frozen.index(leaf) + 1}", tier="kid",
                               limit_usd=float(limit), ttl_minutes=ttl_minutes, workspace_id=workspace_id, root=root)
    if minted is None:
        raise P1Refused("no provisioning key readable by this uid: nothing minted (absence is not a fallback "
                        "to a shared key)")
    # Read BACK: the response to a mint is the caller's own claim, the listing is the API's.
    seen = next((r for r in provisioning.list_keys(root, workspace_id) if r.get("hash") == minted.key_hash), None)
    got = None if seen is None else seen.get("limit")
    if got is None or float(got) > key_cap:
        provisioning.revoke(minted.key_hash, root)
        raise P1Refused(f"cap read back as {got!r} for {minted.name}: an uncapped or over-cap key is "
                        f"revoked and refused (cell {key_cap})")
    expires = _parse_expiry(seen.get("expires_at"))
    window_end = started + datetime.timedelta(minutes=ttl_minutes) + EXPIRY_SLACK
    if expires is None or expires.tzinfo is None or expires <= started or expires > window_end:
        provisioning.revoke(minted.key_hash, root)
        raise P1Refused(f"expires_at read back as {seen.get('expires_at')!r} for {minted.name}: it must be a "
                        f"non-null time inside the {ttl_minutes} min run window; the key is revoked and refused")
    Path(ledger).write_text(json.dumps(rows + [{"arm": arm, "leaf": leaf, "hash": minted.key_hash,
                                                "cap": float(got)}], indent=1))
    return minted


# --- the key files ------------------------------------------------------------

def _getfacl(path: Path) -> list[str]:
    r = subprocess.run(["getfacl", "-n", "-p", str(path)], capture_output=True, text=True)
    if r.returncode:
        raise P1Refused(f"getfacl {path} failed: {r.stderr.strip()[:200]}")
    return [ln.strip() for ln in r.stdout.splitlines() if ln.strip() and not ln.startswith("#")]


def acl_problems(keyfile: str | Path, keydir: str | Path, kid_uid: int) -> list[str]:
    """[] when the pair reads as the council wrote it: the file carries exactly user:<kid>:r-- (and nothing named
    else), the dir exactly user:<kid>:--x (x, no r: the kid can open the file by name but never list the dir),
    and group/other have nothing on either."""
    out: list[str] = []
    want = {"file": (Path(keyfile), f"user:{kid_uid}:r--"), "dir": (Path(keydir), f"user:{kid_uid}:--x")}
    for what, (path, entry) in want.items():
        try:
            lines = _getfacl(path)
        except P1Refused as exc:
            out.append(str(exc))
            continue
        named = [ln for ln in lines if re.match(r"^(user|group):[^:]+:", ln)]
        if named != [entry]:
            out.append(f"{what} {path.name}: named ACL entries {named} != [{entry!r}]")
        for base in ("group::", "other::"):
            row = next((ln for ln in lines if ln.startswith(base)), None)
            if row != f"{base}---":
                out.append(f"{what} {path.name}: {row!r} is not {base}---")
        if what == "file" and "user::rw-" not in lines:
            out.append(f"file {path.name}: owner entry is not user::rw-")
        if what == "dir" and "user::rwx" not in lines:
            out.append(f"dir {path.name}: owner entry is not user::rwx")
    return out


def write_key_file(keydir: str | Path, name: str, secret: str, kid_uid: int) -> Path:
    """Write one key into its own 0600 file under the 0700 dir, grant the kid uid file r + dir x, verify the pair
    by reading the ACLs back, and remove the file if the verify fails. The secret is never returned or logged."""
    keydir = Path(keydir)
    if not re.fullmatch(r"[A-Za-z0-9._-]{1,80}", name) or name in (".", ".."):
        raise P1Refused(f"key file name {name!r} is not a plain file name")
    if not isinstance(kid_uid, int) or isinstance(kid_uid, bool) or kid_uid <= 0 or kid_uid == os.geteuid():
        raise P1Refused(f"kid uid {kid_uid!r} must be a positive uid other than the key holder's own ({os.geteuid()})")
    keydir.mkdir(mode=0o700, exist_ok=True)
    os.chmod(keydir, 0o700)
    path = keydir / name
    fd = os.open(path, os.O_WRONLY | os.O_CREAT | os.O_EXCL, 0o600)
    try:
        with os.fdopen(fd, "w") as fh:
            fh.write(secret)
        for target, spec in ((path, f"u:{kid_uid}:r"), (keydir, f"u:{kid_uid}:x")):
            r = subprocess.run(["setfacl", "-m", spec, str(target)], capture_output=True, text=True)
            if r.returncode:
                raise P1Refused(f"setfacl {spec} failed: {r.stderr.strip()[:200]}")
        problems = acl_problems(path, keydir, kid_uid)
        if problems:
            raise P1Refused("key file ACL does not read as the council wrote it: " + "; ".join(problems))
    except BaseException:
        path.unlink(missing_ok=True)
        raise
    return path


# --- the arm's refusals and end ------------------------------------------------

def arm_preflight(*, arm: str, leaf: str, prefix: str | Path, cfg: dict, kid_uid: int,
                  keydir: str | Path, worktree: str | Path) -> None:
    """Raise `P1Refused` unless this kid may start: a frozen leaf, the pin AND the sealed bytes of ~/pi1 intact,
    a kid uid that is not the key holder's, and a worktree sitting exactly on the frozen base."""
    if leaf not in leaves(cfg):
        raise P1Refused(f"leaf {leaf!r} is not in the frozen list {leaves(cfg)}")
    if arm not in cell(cfg)["arm_cap_usd"]:
        raise P1Refused(f"arm {arm!r} is not a P1 arm")
    problems = check_pin(prefix, cfg) + check_tree(prefix)
    if problems:
        raise P1Refused("pi1 prefix refused: " + "; ".join(problems))
    holder = os.stat(keydir).st_uid
    if kid_uid == holder or kid_uid == 0:
        raise P1Refused(f"kid uid {kid_uid} is the key holder's or root: the kid runs in the director's post uid, never belam or root")
    base = cell(cfg).get("base")
    got = subprocess.run(["git", "-C", str(worktree), "rev-parse", "HEAD"], capture_output=True, text=True)
    if got.returncode or got.stdout.strip() != base:
        raise P1Refused(f"worktree {worktree} is at {got.stdout.strip() or '?'}, not the frozen base {base}")


def disable_key(key_hash: str, root: str | Path | None = None) -> bool:
    prov = provisioning._read_provisioning_key(root)
    if prov is None or not key_hash:
        return False
    provisioning._mutation_guard("disable")
    status, _ = provisioning._call("PATCH", f"{provisioning.API_BASE}/{key_hash}", prov, {"disabled": True})
    return status == 200


def end_arm(rows: list[dict], *, root: str | Path | None = None, workspace_id: str | None = None) -> list[str]:
    """Disable every key of the arm, read each back as disabled, remove its file. rows: {"hash", "file"}.
    Returns the problems; a key that cannot be shown disabled is a red, and its file is removed regardless."""
    out: list[str] = []
    for r in rows:
        if not disable_key(r["hash"], root):
            out.append(f"key {r['hash']}: the disable call did not succeed")
    listed = {k.get("hash"): k for k in provisioning.list_keys(root, workspace_id)}
    for r in rows:
        k = listed.get(r["hash"])
        if k is None or k.get("disabled") is not True:
            out.append(f"key {r['hash']}: read back {'absent' if k is None else k.get('disabled')!r}, not disabled")
        try:
            Path(r["file"]).unlink()
        except FileNotFoundError:
            pass
        except OSError as exc:
            out.append(f"key file {Path(r['file']).name}: not removed ({type(exc).__name__})")
    return out


def kid_key(*, arm: str, leaf: str, cfg: dict, keydir: str | Path, ledger: str | Path, kid_uid: int,
            root: str | Path | None = None, workspace_id: str | None = None, ttl_minutes: int = 90) -> dict:
    """belam's step BEFORE a kid: mint the (arm, leaf) key, put it in its own ACL'd file for `kid_uid`.

    Returns {"arm", "leaf", "hash", "file"} -- the secret is in the file only, never in the return value. At most
    `max_live` key files exist at once; a failed write revokes the key (the ledger still counts it: a red, no retry)."""
    keydir = Path(keydir)
    frozen = leaves(cfg)
    if leaf not in frozen:
        raise P1Refused(f"leaf {leaf!r} is not in the frozen list {frozen}")
    live = sorted(keydir.glob("*.key")) if keydir.is_dir() else []
    if len(live) >= int(cell(cfg)["max_live"]):
        raise P1Refused(f"{len(live)} key files already exist in {keydir.name}: at most {cell(cfg)['max_live']} at once")
    minted = mint_capped(arm=arm, leaf=leaf, cfg=cfg, ledger=ledger, root=root, workspace_id=workspace_id,
                         ttl_minutes=ttl_minutes)
    try:
        path = write_key_file(keydir, f"{arm}-l{frozen.index(leaf) + 1}.key", minted.secret, kid_uid)
    except BaseException:
        provisioning.revoke(minted.key_hash, root)
        raise
    return {"arm": arm, "leaf": leaf, "hash": minted.key_hash, "file": str(path)}


def kid_done(*, key_hash: str, keyfile: str | Path, ledger: str | Path, root: str | Path | None = None,
             workspace_id: str | None = None) -> dict:
    """belam's step AFTER a kid exits: read the key's spend from the provisioning listing (the $/landed source),
    disable it, read it back as disabled, remove its file, record the spend in the ledger row.

    Returns {"arm", "leaf", "hash", "usd", "problems"}; `problems` empty = disabled + file gone."""
    rows = _ledger(Path(ledger))
    row = next((r for r in rows if r.get("hash") == key_hash), None)
    if row is None:
        raise P1Refused(f"key {key_hash!r} is not in the ledger: only a key this driver minted is disabled here")
    listed = next((k for k in provisioning.list_keys(root, workspace_id) if k.get("hash") == key_hash), None)
    usd = None if listed is None else float(listed.get("usage") or 0.0)
    problems = end_arm([{"hash": key_hash, "file": str(keyfile)}], root=root, workspace_id=workspace_id)
    if usd is None:
        problems.append(f"key {key_hash}: absent from the listing, its spend is unknown")
    row["usd"], row["done"] = usd, not problems
    Path(ledger).write_text(json.dumps(rows, indent=1))
    return {"arm": row["arm"], "leaf": row["leaf"], "hash": key_hash, "usd": usd, "problems": problems}


# --- my side of a kid: the launch ---------------------------------------------------

#: The only environment a kid gets. No key, no provisioning variable, nothing inherited.
KID_ENV_KEYS = ("PATH", "HOME", "PI_CODING_AGENT_DIR", "PI_OFFLINE", "LANG")


def _node_version(path: str) -> tuple[int, ...] | None:
    try:
        r = subprocess.run([path, "--version"], capture_output=True, text=True, timeout=20)
    except (OSError, subprocess.SubprocessError):
        return None
    m = re.fullmatch(r"v(\d+)\.(\d+)\.(\d+)", r.stdout.strip())
    return tuple(int(x) for x in m.groups()) if m else None


def node_for_pi(cfg: dict) -> str:
    """The first node (cell `node_candidates`, then PATH) at or above `node_min`: pi 1.x needs node >= 22.19 and
    the system node of this box is older, so a bare `node` on PATH is NOT assumed. Raises naming each one tried."""
    p = cell(cfg)
    need = tuple(p["node_min"])
    tried = []
    for cand in list(p.get("node_candidates") or []) + [shutil.which("node") or ""]:
        if not cand or cand in [t[0] for t in tried]:
            continue
        ver = _node_version(cand)
        if ver is not None and ver >= need:
            return cand
        tried.append((cand, ver))
    raise P1Refused(f"no node >= {'.'.join(map(str, need))} found; tried {tried}")


def pi_cli(prefix: str | Path, cfg: dict) -> str:
    """The real file behind `<prefix>/node_modules/.bin/pi`, which must sit inside the pinned package: a bin link
    retargeted elsewhere is refused (the tree seal catches a changed link; this is the second lock)."""
    pin = cell(cfg)["pin"]
    prefix = Path(os.path.expanduser(str(prefix)))
    real = os.path.realpath(prefix / "node_modules" / ".bin" / "pi")
    pkg = os.path.realpath(prefix / "node_modules" / pin["package"])
    if not real.startswith(pkg + os.sep):
        raise P1Refused(f"pi bin resolves to {real}, outside the pinned package {pkg}")
    return real


def write_models_json(agent_dir: str | Path, provider: str, keyfile: str | Path,
                      base_url: str | None = None) -> Path:
    """<agent_dir>/models.json whose ONLY credential is the key file's path: apiKey "!cat <keyfile>" (pi runs it at
    request time). `base_url` is for the offline smoke only; a P1 arm never sets it."""
    key = str(keyfile)
    if not os.path.isabs(key) or not re.fullmatch(r"[A-Za-z0-9_./-]+", key):
        raise P1Refused(f"key file path {key!r} must be absolute and made of plain path characters")
    entry: dict = {"apiKey": f"!cat {key}"}
    if base_url:
        entry["baseUrl"] = base_url
    agent_dir = Path(agent_dir)
    agent_dir.mkdir(parents=True, exist_ok=True)
    path = agent_dir / "models.json"
    fd = os.open(path, os.O_WRONLY | os.O_CREAT | os.O_TRUNC, 0o600)
    with os.fdopen(fd, "w") as fh:
        json.dump({"providers": {provider: entry}}, fh)
    return path


BRIEF_SECTIONS = ("Target end-state", "Falsifier", "Invariants", "Out of scope")


def _git_show(repo: str | Path, rev: str, path: str) -> str:
    r = subprocess.run(["git", "-C", str(repo), "show", f"{rev}:{path}"], capture_output=True, text=True)
    if r.returncode:
        raise P1Refused(f"git show {rev[:10]}:{path} failed: the frozen base cannot be read")
    return r.stdout


def frozen_rules(repo: str | Path, cfg: dict) -> dict[str, str]:
    """The standing rules a kid brief carries, read from the PREREGISTERED text of .46.9 AT THE FROZEN BASE (the
    council's own words: "The kid brief for <leaf> carries the standing rule: <rule>."), never from the working
    tree or a cell a later trunk edit could move."""
    text = _git_show(repo, cell(cfg)["base"], ".agi/nodes/goal/g7.16.1.11.46.9.md")
    return {f"goal:{m.group(1)}": m.group(2).strip()
            for m in re.finditer(r"The kid brief for (?:goal:)?(g[\w.]+) carries the standing rule: (.*?)\. \(Q3\)", text, re.S)}


def leaf_brief(leaf: str, repo: str | Path, cfg: dict) -> str:
    """The kid's brief, FROZEN WITH THE BASE: the leaf node read by `git show <p1.base>:<path>` (Target end-state,
    Falsifier, Invariants, Out of scope, verbatim) plus the standing rule .46.9 preregistered for that leaf. A later
    trunk edit to the leaf or to a cell changes nothing here; `brief_digest` is in every result row."""
    if leaf not in leaves(cfg):
        raise P1Refused(f"leaf {leaf!r} is not in the frozen list {leaves(cfg)}")
    text = _git_show(repo, cell(cfg)["base"], f".agi/nodes/goal/{leaf.split(':', 1)[1]}.md")
    parts = []
    for head in BRIEF_SECTIONS:
        m = re.search(rf"^## {head}\n(.*?)(?=^## |\Z|^<!--)", text, re.S | re.M)
        if m:
            parts.append(f"## {head}\n{m.group(1).strip()}")
    rule = frozen_rules(repo, cfg).get(leaf)
    return (f"You are a kid on leaf {leaf} in this repository (cwd). Make its falsifier pass with the smallest change; "
            f"edit files only, do not commit, push or run the full test suite. Stop when the falsifier holds.\n\n"
            + "\n\n".join(parts) + (f"\n\nStanding rule: {rule}" if rule else ""))


def brief_digest(text: str) -> str:
    return hashlib.sha256(text.encode()).hexdigest()


def kid_plan(*, arm: str, leaf: str, cfg: dict, keyfile: str | Path, worktree: str | Path, kid_home: str | Path,
             prompt: str, prefix: str | Path = "~/pi1", base_url: str | None = None) -> dict:
    """The kid's command, cwd and environment, with no side effect. The environment is exactly KID_ENV_KEYS."""
    import adapters  # noqa: PLC0415
    if arm == CREDITS_ARM or arm not in cell(cfg)["arm_cap_usd"]:
        raise P1Refused(f"arm {arm!r} cannot launch an OpenRouter kid")
    if leaf not in leaves(cfg):
        raise P1Refused(f"leaf {leaf!r} is not in the frozen list {leaves(cfg)}")
    h = adapters.harness_block(cfg, f"pi1:{arm}")
    if not h:
        raise P1Refused(f"no harness row pi1:{arm}")
    node = node_for_pi(cfg)
    kid_home = str(kid_home)
    agent_dir = f"{kid_home}/.p1-agent"
    argv = [node, pi_cli(prefix, cfg), "--provider", h["provider"], "--model", h["models"]["kid"],
            "--thinking", h.get("thinking", "medium"), "-p", prompt, "--no-session", "--no-extensions",
            "--no-skills", "--no-prompt-templates", "--no-themes", "--no-mcp", "--offline"]
    env = {"PATH": f"{os.path.dirname(node)}:/usr/bin:/bin", "HOME": kid_home, "PI_CODING_AGENT_DIR": agent_dir,
           "PI_OFFLINE": "1", "LANG": "C.UTF-8"}
    return {"argv": argv, "env": env, "cwd": str(worktree), "agent_dir": agent_dir, "provider": h["provider"],
            "prompt": prompt,
            "model": h["models"]["kid"], "keyfile": str(keyfile), "base_url": base_url,
            "log": f"{kid_home}/p1-{arm}-{leaves(cfg).index(leaf) + 1}.log", "timeout": int(cell(cfg)["kid_timeout_s"])}


def _ancestors() -> set[int]:
    out, pid = {os.getpid()}, os.getppid()
    while pid > 1 and pid not in out:
        out.add(pid)
        try:
            pid = int(Path(f"/proc/{pid}/stat").read_text().rsplit(")", 1)[1].split()[1])
        except (OSError, ValueError, IndexError):
            break
    return out


def proc_sweep(paths: list[str | Path], *, spare: set[int] | None = None) -> list[int]:
    """SIGKILL every process of THIS uid whose cwd or any open fd lies under one of `paths`; returns the pids.
    This is the check behind the process-group kill: a kid that escaped its session (`setsid`) still has its
    cwd or a fd in the kid's worktree or home. This process and its ancestors are never touched."""
    real = [os.path.realpath(p) for p in paths]
    spare = (spare or set()) | _ancestors()
    me, hit = os.getuid(), []
    for ent in os.listdir("/proc"):
        if not ent.isdigit() or int(ent) in spare:
            continue
        try:
            if os.stat(f"/proc/{ent}").st_uid != me:
                continue
        except OSError:
            continue
        links = []
        try:
            links.append(os.readlink(f"/proc/{ent}/cwd"))
            for fd in os.listdir(f"/proc/{ent}/fd"):
                try:
                    links.append(os.readlink(f"/proc/{ent}/fd/{fd}"))
                except OSError:
                    pass
        except OSError:
            pass
        if any(l == p or l.startswith(p + os.sep) for l in links for p in real):
            hit.append(int(ent))
    for pid in hit:
        try:
            os.kill(pid, signal.SIGKILL)
        except ProcessLookupError:
            pass
    return sorted(hit)


def run_kid(plan: dict, cfg: dict, *, live: int, gb: float | None) -> dict:
    """Spawn gate, models.json, ONE bounded run in its own session, models.json removed. The kid's whole process
    group is SIGKILLed at the timeout AND at normal exit, then a /proc sweep kills anything of this uid still
    holding the kid's worktree or home; a sweep hit counts the run red. Returns {"rc", "secs", "timed_out",
    "sweep"}: never the log's content and never the key. A kid at the timeout is a counted red, not retried."""
    ok, why = may_start(live, gb, cfg)
    if not ok:
        raise P1Refused(f"kid not started: {why}")
    if set(plan["env"]) - set(KID_ENV_KEYS):
        raise P1Refused(f"kid env carries {sorted(set(plan['env']) - set(KID_ENV_KEYS))}: only {KID_ENV_KEYS} are allowed")
    models = write_models_json(plan["agent_dir"], plan["provider"], plan["keyfile"], plan.get("base_url"))
    start = _now()
    timed_out = False
    rc: int | None
    sweep: list[int] = []
    try:
        fd = os.open(plan["log"], os.O_WRONLY | os.O_CREAT | os.O_TRUNC, 0o600)
        with os.fdopen(fd, "w") as log:
            proc = subprocess.Popen(plan["argv"], cwd=plan["cwd"], env=plan["env"], stdin=subprocess.DEVNULL,
                                    stdout=log, stderr=subprocess.STDOUT, start_new_session=True)
            try:
                rc = proc.wait(timeout=plan["timeout"])
            except subprocess.TimeoutExpired:
                rc, timed_out = None, True
            finally:
                try:
                    os.killpg(proc.pid, signal.SIGKILL)       # at the timeout AND at a normal exit
                except ProcessLookupError:
                    pass
                proc.wait()
        sweep = proc_sweep([plan["cwd"], plan["agent_dir"].rsplit("/", 1)[0]])
    finally:
        models.unlink(missing_ok=True)
    return {"rc": rc, "secs": round((_now() - start).total_seconds(), 1), "timed_out": timed_out, "sweep": sweep}


# --- the run ledger (mine) and the record that reads both ledgers ------------------------

def _runs(path: str | Path) -> list[dict]:
    try:
        rows = json.loads(Path(path).read_text())
    except FileNotFoundError:
        return []
    except (OSError, ValueError) as exc:
        raise P1Refused(f"run ledger {Path(path).name} unreadable ({type(exc).__name__})")
    return rows if isinstance(rows, list) else []


def live_kids(rows: list[dict], arm: str, leaf: str) -> int:
    """Kids that are live by the BELAM ledger: minted and no kid-done row, other than this (arm, leaf)."""
    return sum(1 for r in rows if not r.get("done") and (r["arm"], r["leaf"]) != (arm, leaf))


def run_logged(*, arm: str, leaf: str, cfg: dict, ledger: str | Path, runs: str | Path, repo: str | Path,
               plan: dict, gb: float | None) -> dict:
    """R1/R2: count live kids from the ledger (no default), refuse a second run of the pair, run, and write the run
    row {arm, leaf, rc, secs, timed_out, sweep, brief_sha256}. The row is what `record` later reads."""
    rows = _ledger(Path(ledger))
    if not any(r["arm"] == arm and r["leaf"] == leaf for r in rows):
        raise P1Refused(f"({arm}, {leaf}) has no mint row in the ledger: belam's kid-key comes first")
    runs_rows = _runs(runs)
    if any(r["arm"] == arm and r["leaf"] == leaf for r in runs_rows):
        raise P1Refused(f"({arm}, {leaf}) already has a run row: a kid runs once, never again")
    res = run_kid(plan, cfg, live=live_kids(rows, arm, leaf), gb=gb)
    row = {"arm": arm, "leaf": leaf, "rc": res["rc"], "secs": res["secs"], "timed_out": res["timed_out"],
           "sweep": res["sweep"], "brief_sha256": brief_digest(plan["prompt"])}
    tmp = Path(str(runs) + ".tmp")
    tmp.write_text(json.dumps(runs_rows + [row], indent=1))
    os.replace(tmp, runs)
    return row


def record_from_ledgers(results: str | Path, cfg: dict, *, arm: str, leaf: str, ledger: str | Path,
                        runs: str | Path, landed: bool, red: bool) -> dict:
    """R1: RECORD READS, NEVER TYPED. usd comes from the (arm, leaf) kid-done row of belam's ledger, secs and the brief
    sha from my run row; either absent = refused. A timed-out, non-zero or swept run is red and cannot be landed:
    a record that says otherwise is refused."""
    mint = next((r for r in _ledger(Path(ledger)) if r["arm"] == arm and r["leaf"] == leaf), None)
    if mint is None or not mint.get("done") or mint.get("usd") is None:
        raise P1Refused(f"({arm}, {leaf}) has no kid-done row (usd) in the ledger: belam's kid-done comes first")
    run = next((r for r in _runs(runs) if r["arm"] == arm and r["leaf"] == leaf), None)
    if run is None:
        raise P1Refused(f"({arm}, {leaf}) has no run row: run-kid comes first")
    forced = bool(run["timed_out"]) or run["rc"] != 0 or bool(run["sweep"])
    if forced and (landed or not red):
        raise P1Refused(f"({arm}, {leaf}) ran red (timed_out={run['timed_out']} rc={run['rc']} sweep={run['sweep']}): "
                        f"it records as red and not landed, not as landed={landed} red={red}")
    return record_result(results, cfg, arm=arm, leaf=leaf, landed=landed, usd=float(mint["usd"]),
                         secs=float(run["secs"]), red=red or forced, brief_sha256=run["brief_sha256"])


def record_result(path: str | Path, cfg: dict, *, arm: str, leaf: str, landed: bool, usd: float, secs: float,
                  red: bool, brief_sha256: str | None = None) -> dict:
    """Add the (arm, leaf) kid row to the committed results file (written atomically; one row per pair, ever).
    This is the file the one metrics writer renders; this function writes nothing else."""
    import adapters  # noqa: PLC0415
    if leaf not in leaves(cfg):
        raise P1Refused(f"leaf {leaf!r} is not in the frozen list {leaves(cfg)}")
    h = adapters.harness_block(cfg, f"pi1:{arm}")
    if not h:
        raise P1Refused(f"no harness row pi1:{arm}")
    if not isinstance(usd, (int, float)) or isinstance(usd, bool) or not math.isfinite(usd) or usd < 0:
        raise P1Refused(f"usd {usd!r} must be a finite number >= 0")
    path = Path(path)
    try:
        res = json.loads(path.read_text())
    except FileNotFoundError:
        res = {"base": cell(cfg)["base"], "arms": []}
    except (OSError, ValueError) as exc:
        raise P1Refused(f"results file {path} unreadable ({type(exc).__name__})")
    if res.get("base") != cell(cfg)["base"]:
        raise P1Refused(f"results file base {res.get('base')!r} != the frozen base")
    entry = next((a for a in res["arms"] if a["arm"] == arm), None)
    if entry is None:
        entry = {"arm": arm, "model": h["models"]["kid"], "kids": []}
        res["arms"].append(entry)
    if any(k["leaf"] == leaf for k in entry["kids"]):
        raise P1Refused(f"({arm}, {leaf}) already has a result row: one run per pair, never re-recorded")
    other = next((k.get("brief_sha256") for a in res["arms"] for k in a["kids"] if k["leaf"] == leaf and k.get("brief_sha256")), None)
    if brief_sha256 and other and other != brief_sha256:
        raise P1Refused(f"({arm}, {leaf}) brief sha {brief_sha256[:12]} != the other arm's {other[:12]}: one frozen brief per leaf")
    entry["kids"].append({"leaf": leaf, "landed": bool(landed), "usd": float(usd), "secs": float(secs), "red": bool(red),
                          "brief_sha256": brief_sha256})
    order = cell(cfg)["arm_order"]
    res["arms"].sort(key=lambda a: order.index(a["arm"]) if a["arm"] in order else len(order))
    tmp = path.with_suffix(".tmp")
    tmp.write_text(json.dumps(res, indent=1) + "\n")
    os.replace(tmp, path)
    return res


# --- P0: the readings that must be TRUE and READ before a first mint ---------------------

OPENROUTER_MODELS = "https://openrouter.ai/api/v1/models"


def live_prices(models: list[str], fetch=None) -> dict[str, dict[str, float]]:
    """Per-million-token prices of `models` from OpenRouter's public models list (no key)."""
    if fetch is None:
        import urllib.request  # noqa: PLC0415
        with urllib.request.urlopen(OPENROUTER_MODELS, timeout=30) as r:
            data = json.loads(r.read())["data"]
    else:
        data = fetch()
    by = {m["id"]: m.get("pricing") or {} for m in data}
    return {m: {"in_per_m": round(float(by[m]["prompt"]) * 1e6, 6), "out_per_m": round(float(by[m]["completion"]) * 1e6, 6)}
            for m in models if m in by and by[m].get("prompt") is not None and by[m].get("completion") is not None}


def p0_readings(*, cfg: dict, repo: str | Path, worktree: str | Path, main_env: str | Path | None = None,
                fetch=None, slice_path: str = SLICE_MEMORY) -> list[tuple[str, bool, str]]:
    """(name, ok, reading) for P0 a-f; the caller prints them (they are the 'written down'). Nothing here mints."""
    import tempfile  # noqa: PLC0415
    out: list[tuple[str, bool, str]] = []
    # (a) the p1_segment fix: from the graph dir of a scratch project with no results file, NO p1 text
    try:
        import success_metrics  # noqa: PLC0415
        with tempfile.TemporaryDirectory() as d:
            (Path(d) / ".agi").mkdir()
            (Path(d) / ".agi" / "config.json").write_text(json.dumps(cfg))
            seg = success_metrics.p1_segment(Path(d) / ".agi")
        out.append(("a p1_segment", seg == "", "no segment from the .agi dir of a project without results" if seg == "" else f"false segment {seg!r}"))
    except Exception as exc:  # noqa: BLE001
        out.append(("a p1_segment", False, f"cannot run: {type(exc).__name__}"))
    # (b) live prices equal the cell's, read now
    want = cell(cfg).get("prices", {}).get("models", {})
    try:
        got = live_prices(list(want), fetch)
        bad = [m for m in want if m not in got or any(abs(got[m][k] - want[m][k]) > 0.05 * want[m][k] + 1e-9 for k in ("in_per_m", "out_per_m"))]
        out.append(("b prices", bool(want) and not bad,
                    "; ".join(f"{m} in {got[m]['in_per_m']} out {got[m]['out_per_m']} per M" for m in got) + (f" -- differs from the cell: {bad}" if bad else "")))
    except Exception as exc:  # noqa: BLE001
        out.append(("b prices", False, f"live read failed: {type(exc).__name__}"))
    # (c) agi.slice under the bound
    gb = slice_gb(slice_path)
    mx = float(cell(cfg)["slice_gb_max"])
    out.append(("c agi.slice", gb is not None and gb <= mx, f"{'unreadable' if gb is None else f'{gb:.2f} GB'} (max {mx})"))
    # (d) MAIN .env is EACCES from this uid
    if main_env is None:
        common = subprocess.run(["git", "-C", str(repo), "rev-parse", "--git-common-dir"], capture_output=True, text=True).stdout.strip()
        main_env = (Path(repo) / common).resolve().parent / ".env"
    probs = main_env_denied(main_env)
    out.append(("d main .env", not probs, "EACCES" if not probs else "; ".join(probs)))
    # (e) the kid worktree is on the frozen base
    got_head = subprocess.run(["git", "-C", str(worktree), "rev-parse", "HEAD"], capture_output=True, text=True).stdout.strip()
    out.append(("e base", got_head == cell(cfg).get("base"), f"worktree {got_head[:10] or '?'} vs base {str(cell(cfg).get('base'))[:10]}"))
    # (f) R1-R4 are in this module
    have = [n for n in ("record_from_ledgers", "run_logged", "live_kids", "leaf_brief", "brief_digest", "proc_sweep") if callable(globals().get(n))]
    out.append(("f R1-R4", len(have) == 6, "present: " + ", ".join(have)))
    return out


def scratch_land_problems(paths: list[str], cfg: dict) -> list[str]:
    """RED when a kid's scratch land creates a path the engine forbids (the shadow bin files, CLAUDE.md)."""
    forbidden = set(cell(cfg).get("forbidden_paths") or [])
    return [f"scratch land creates {p}: forbidden" for p in paths if p in forbidden]


# --- the spawn gate and the results ---------------------------------------------

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


def render_segment(results: dict, cfg: dict) -> str:
    """The `| p1: <model> $/landed=<x> s/landed=<y> red=<r>/<n>` segments for the arms in a results file, one per
    arm that ran, joined by spaces; '' when none ran. n = the frozen leaf count; 0 landed prints
    `$/landed=n/a landed=0`. Every kid's spend counts, landed or not: the cost of an arm is what it burned.

    results: {"base": sha, "arms": [{"arm", "model", "kids": [{"leaf", "landed", "usd", "secs", "red"}]}]}."""
    n = len(leaves(cfg))
    segs = []
    for a in results.get("arms") or []:
        kids = a.get("kids") or []
        landed = sum(1 for k in kids if k["landed"])
        red = sum(1 for k in kids if k["red"])
        if landed == 0:
            body = f"$/landed=n/a landed=0 red={red}/{n}"
        else:
            body = (f"$/landed={sum(k['usd'] for k in kids) / landed:.4f} "
                    f"s/landed={sum(k['secs'] for k in kids) / landed:.0f} red={red}/{n}")
        segs.append(f"| p1: {a['model']} {body}")
    return " ".join(segs)


def merge_pick(results: dict, cfg: dict) -> dict[str, str | None]:
    """ONE run per leaf merges, after all arms: the first green run in the fixed arm order (cell `arm_order`),
    or None when no arm landed that leaf."""
    order = cell(cfg)["arm_order"]
    by = {a["arm"]: {k["leaf"]: k for k in a.get("kids") or []} for a in results.get("arms") or []}
    return {leaf: next((arm for arm in order if by.get(arm, {}).get(leaf, {}).get("landed")), None)
            for leaf in leaves(cfg)}


def read_results(root: str | Path, cfg: dict) -> dict | None:
    """The committed results file, or None when there is none; a malformed file raises P1Refused (named)."""
    path = Path(root) / cell(cfg)["results"]
    try:
        return json.loads(path.read_text())
    except FileNotFoundError:
        return None
    except (OSError, ValueError) as exc:
        raise P1Refused(f"results file {path} unreadable ({type(exc).__name__})")


def _driver(cmd: str, args: list[str], cfg: dict) -> int:
    """`kid-key ARM LEAF --kid-uid N --keydir D --ledger L` and `kid-done --hash H --file F --ledger L`, run as the
    provisioning key's holder. One JSON line on stdout, never the secret; rc 1 + a `p1 <cmd>: RED` line on refusal."""
    import argparse  # noqa: PLC0415
    ap = argparse.ArgumentParser(prog=f"p1_ab.py {cmd}")
    if cmd == "kid-key":
        ap.add_argument("arm")
        ap.add_argument("leaf")
        ap.add_argument("--kid-uid", type=int, required=True)
    else:
        ap.add_argument("--hash", required=True)
        ap.add_argument("--file", required=True)
    ap.add_argument("--keydir", required=cmd == "kid-key")
    ap.add_argument("--ledger", required=True)
    a = ap.parse_args(args)
    root = Path(__file__).resolve().parents[3]
    ws = provisioning.workspace(cfg)
    try:
        if cmd == "kid-key":
            out = kid_key(arm=a.arm, leaf=a.leaf, cfg=cfg, keydir=a.keydir, ledger=a.ledger, kid_uid=a.kid_uid,
                          root=root, workspace_id=ws)
        else:
            out = kid_done(key_hash=a.hash, keyfile=a.file, ledger=a.ledger, root=root, workspace_id=ws)
    except (P1Refused, provisioning.ProvisioningError) as exc:
        print(f"p1 {cmd}: {exc}")
        print(f"p1 {cmd}: RED")
        return 1
    print(json.dumps(out))
    return 1 if out.get("problems") else 0


def _mine(cmd: str, args: list[str], cfg: dict, root: Path) -> int:
    """My side, run as the director's post uid, one JSON line out, never a key.
    `run-kid ARM LEAF --key-file F --worktree W --kid-home H --ledger L --runs R`: preflight, the live count from
    belam's ledger L (there is no --live), ONE run, the run row into my run ledger R.
    `record ARM LEAF --ledger L --runs R --landed 0|1 --red 0|1`: usd from L's kid-done row, secs from R's run row.
    `p0 --worktree W --kid-home H [--main-env F]`: the readings that must be true before a first mint."""
    import argparse  # noqa: PLC0415
    ap = argparse.ArgumentParser(prog=f"p1_ab.py {cmd}")
    if cmd == "p0":
        ap.add_argument("--worktree", required=True)
        ap.add_argument("--main-env", default=None)
    else:
        ap.add_argument("arm")
        ap.add_argument("leaf")
        ap.add_argument("--ledger", required=True)
        ap.add_argument("--runs", required=True)
    if cmd == "run-kid":
        ap.add_argument("--key-file", required=True)
        ap.add_argument("--worktree", required=True)
        ap.add_argument("--kid-home", required=True)
    elif cmd == "record":
        ap.add_argument("--landed", type=int, choices=(0, 1), required=True)
        ap.add_argument("--red", type=int, choices=(0, 1), required=True)
    a = ap.parse_args(args)
    try:
        if cmd == "p0":
            rows = p0_readings(cfg=cfg, repo=root, worktree=a.worktree, main_env=a.main_env)
            for name, ok, detail in rows:
                print(f"P0 {name} {'ok ' if ok else 'RED'} {detail}")
            return 0 if all(ok for _, ok, _ in rows) else 1
        if cmd == "run-kid":
            arm_preflight(arm=a.arm, leaf=a.leaf, prefix="~/pi1", cfg=cfg, kid_uid=os.geteuid(),
                          keydir=os.path.dirname(a.key_file), worktree=a.worktree)
            plan = kid_plan(arm=a.arm, leaf=a.leaf, cfg=cfg, keyfile=a.key_file, worktree=a.worktree,
                            kid_home=a.kid_home, prompt=leaf_brief(a.leaf, root, cfg))
            out = run_logged(arm=a.arm, leaf=a.leaf, cfg=cfg, ledger=a.ledger, runs=a.runs, repo=root, plan=plan,
                             gb=slice_gb())
        else:
            record_from_ledgers(root / cell(cfg)["results"], cfg, arm=a.arm, leaf=a.leaf, ledger=a.ledger,
                                runs=a.runs, landed=bool(a.landed), red=bool(a.red))
            out = {"arm": a.arm, "leaf": a.leaf, "recorded": True}
    except P1Refused as exc:
        print(f"p1 {cmd}: {exc}")
        print(f"p1 {cmd}: RED")
        return 1
    print(json.dumps(out))
    return 0


def main(argv: list[str]) -> int:
    root = Path(__file__).resolve().parents[3]
    cfg = json.loads((root / ".agi" / "config.json").read_text())
    cmd = argv[1] if len(argv) > 1 else ""
    if cmd in ("-h", "--help"):
        print(__doc__.strip().split("\n\n")[0])
        print("usage: p1_ab.py install|seal|pin-check [prefix] | old-pi | kid-key | kid-done | run-kid | record | p0")
        return 0
    if cmd in ("kid-key", "kid-done"):
        return _driver(cmd, argv[2:], cfg)
    if cmd in ("run-kid", "record", "p0"):
        return _mine(cmd, argv[2:], cfg, root)
    prefix = argv[2] if len(argv) > 2 else "~/pi1"
    if cmd == "install":
        problems = install(prefix, cfg)
    elif cmd == "seal":
        try:
            seal(prefix, cfg)
            problems = []
        except P1Refused as exc:
            problems = [str(exc)]
    elif cmd == "pin-check":
        problems = check_pin(prefix, cfg) + check_tree(prefix)
    elif cmd == "old-pi":
        problems = old_pi_untouched()
    else:
        print("usage: p1_ab.py install|seal|pin-check [prefix] | old-pi | kid-key | kid-done | run-kid | record | p0", file=sys.stderr)
        return 2
    for pr in problems:
        print(f"p1 {cmd}: {pr}")
    print(f"p1 {cmd}: {'OK' if not problems else 'RED'}")
    return 1 if problems else 0


if __name__ == "__main__":
    sys.exit(main(sys.argv))
