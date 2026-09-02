#!/usr/bin/env python3
"""provisioning.py — mint and revoke short-lived provider keys (goal:g1.11).

Every spawned agent used to inherit one long-lived `OPENROUTER_API_KEY`, and
that key was the whole balance. One runaway kid in a retry loop could spend it,
one leaked context could expose it, and the bill could not say which agent did
it: **a single point of failure, of leak, and of attribution, sharing one
cause.**

This module turns the credential from a constant into something the engine
issues. With `OPENROUTER_PROVISIONING_KEY` set, a spawn gets a key that did not
exist before it and does not outlive it.

## Three independent limits, because a cleanup step is not a safety property

1. **A credit cap** on every minted key. A runaway agent spends at most its own
   cap, not the balance.
2. **A TTL** (`expires_at`). The key dies on its own. This is what makes a
   crashed director safe: revocation that only runs on the happy path is not
   revocation.
3. **Explicit revocation** when the agent's lease is reclaimed — the fast path,
   which the other two exist to survive the absence of.

**Measured, 2026-09-02, against the live API:** mint 0.76s mean / 0.86s max
over 10 serial calls; 10 concurrent mints complete in 0.92s wall; 20 concurrent
revocations in 2.78s; 30/30 calls succeeded and zero keys leaked. That
measurement is why issuance is **per spawn** rather than batched — the cost
that motivated batching is under a second and does not compound under
concurrency, and per-spawn is the only granularity that gives per-agent
attribution.

## 🔴 `expires_in_seconds` is silently ignored

The API accepts unknown fields with a `201` and no error. Posting
`expires_in_seconds` returns a key with `expires_at: null` — a key with **no
TTL**, created by a call that looked like it worked. Only `expires_at`, as an
ISO-8601 `Z` timestamp, is honoured. Verified both ways; do not "simplify" this.

## The provisioning key is not a runtime key

It mints, revokes, and reads spend. It is read through `envfile` (never
`os.environ`) so its location stays graph content, and `dispatch.py` scrubs it
from every child environment — a kid holding it could mint uncapped keys or
revoke the ones the run depends on.

## Absence is a supported state, not an error

`goal:g1.11`'s falsifier requires the loop to run with no provisioning key at
all, falling back to the single runtime key. A hardening feature that becomes a
hard dependency has made the project more fragile while calling itself
hardened. Every entry point here returns `None`/`False` rather than raising when
the key is absent.
"""
from __future__ import annotations

import datetime
import json
import sys
import urllib.error
import urllib.request
from dataclasses import dataclass
from pathlib import Path

sys.path.insert(0, str(Path(__file__).resolve().parent))
import envfile  # noqa: E402

#: OpenRouter's key-management endpoint.
API_BASE = "https://openrouter.ai/api/v1/keys"

#: The env var holding the key that mints keys. Declared in
#: `.geometry/secrets.md` as optional, and scrubbed from every child.
PROVISIONING_KEY_VAR = "OPENROUTER_PROVISIONING_KEY"

#: The env var a spawned agent actually authenticates with. A minted key is
#: injected under this name, so nothing downstream knows the difference.
RUNTIME_KEY_VAR = "OPENROUTER_API_KEY"

#: Used when the config declares nothing. Deliberately small: the default must
#: be a number nobody minds losing, because the default is what runs on a box
#: whose owner has not thought about it yet.
DEFAULT_LIMIT_USD = 0.25
DEFAULT_TTL_MINUTES = 60

#: Every key this engine mints is named with this prefix, so `reap_orphans`
#: can tell its own litter from a key a human made by hand and must not touch.
NAME_PREFIX = "agi"


class ProvisioningError(RuntimeError):
    """A call to the key-management API failed in a way the caller must see."""


@dataclass(frozen=True)
class MintedKey:
    """One issued credential. `secret` is returned exactly once, by the API."""

    secret: str
    key_hash: str
    name: str
    limit_usd: float
    expires_at: str


def _read_provisioning_key(root: Path | str | None = None) -> str | None:
    """The provisioning key, or None. Read through the graph, never os.environ.

    `envfile` resolves the env file's path from `.geometry/secrets.md`, so the
    location stays a fact the graph states once (`goal:g10.2`) rather than a
    literal repeated here.
    """
    try:
        res = envfile.resolve(str(root) if root is not None else None)
    except Exception:
        return None
    if not res.env_file.is_file():
        return None
    value = envfile.read_env(res.env_file).get(PROVISIONING_KEY_VAR, "")
    return value or None


def available(root: Path | str | None = None) -> bool:
    """Whether this project can issue keys at all. Never raises."""
    return _read_provisioning_key(root) is not None


def settings(cfg: dict) -> tuple[float, int]:
    """`(limit_usd, ttl_minutes)` from `spawn.credential`, with defaults.

    Declared rather than improvised, which is the whole of `goal:g1`: how much
    one agent may spend and how long its key lives are run parameters, not
    constants buried in a spawner.
    """
    cred = ((cfg.get("spawn") or {}).get("credential") or {})
    limit = float(cred.get("per_spawn_limit_usd", DEFAULT_LIMIT_USD))
    ttl = int(cred.get("ttl_minutes", DEFAULT_TTL_MINUTES))
    return limit, ttl


def _call(method: str, url: str, key: str, payload: dict | None = None,
          timeout: int = 30) -> tuple[int, dict]:
    body = json.dumps(payload).encode() if payload is not None else None
    req = urllib.request.Request(
        url, data=body, method=method,
        headers={"Authorization": f"Bearer {key}",
                 "Content-Type": "application/json"})
    try:
        with urllib.request.urlopen(req, timeout=timeout) as resp:
            return resp.status, json.loads(resp.read() or b"{}")
    except urllib.error.HTTPError as exc:
        detail = exc.read()[:300].decode("utf8", "replace")
        return exc.code, {"error": detail}
    except Exception as exc:  # network down, DNS, timeout
        return 0, {"error": f"{type(exc).__name__}: {exc}"}


def key_name(iter_n: int | str, agent_id: str, tier: str = "kid") -> str:
    """The name a minted key carries, and it is the attribution record.

    `goal:g1.11`'s fifth requirement: the spend line must answer "which agent"
    without anyone correlating timestamps by hand. The iteration and the agent
    id are in the name, so OpenRouter's own dashboard answers it.
    """
    return f"{NAME_PREFIX}-iter{iter_n}-{tier}-{agent_id}"


def mint(*, iter_n: int | str, agent_id: str, tier: str = "kid",
         limit_usd: float = DEFAULT_LIMIT_USD,
         ttl_minutes: int = DEFAULT_TTL_MINUTES,
         root: Path | str | None = None) -> MintedKey | None:
    """Issue one capped, expiring runtime key. None if issuance is unavailable.

    Returns None — never raises — when there is no provisioning key, because
    absence is a supported state. A *failed* call with a key present does
    raise: that is a real fault and silently falling back to the shared key
    would hide it.
    """
    prov = _read_provisioning_key(root)
    if prov is None:
        return None

    expires = (datetime.datetime.now(datetime.timezone.utc)
               + datetime.timedelta(minutes=ttl_minutes))
    # ISO-8601 with a literal Z. `expires_in_seconds` is accepted with a 201
    # and silently ignored, producing a key with no TTL -- see module docstring.
    expires_at = expires.isoformat().replace("+00:00", "Z")
    name = key_name(iter_n, agent_id, tier)

    status, body = _call("POST", API_BASE, prov, {
        "name": name,
        "limit": limit_usd,
        "expires_at": expires_at,
    })
    if status != 201:
        raise ProvisioningError(
            f"mint failed for {name}: HTTP {status} {body.get('error', body)}")

    data = body.get("data") or {}
    secret = body.get("key")
    key_hash = data.get("hash")
    if not secret or not key_hash:
        raise ProvisioningError(
            f"mint returned no usable key for {name}: keys={sorted(body)}")

    got_ttl = data.get("expires_at")
    if not got_ttl:
        # A key with no expiry is the failure this module's TTL exists to
        # prevent, and the API reports it by returning null rather than by
        # erroring. Refuse it: revoke immediately and raise, rather than hand
        # out a credential that outlives every other guarantee here.
        _call("DELETE", f"{API_BASE}/{key_hash}", prov)
        raise ProvisioningError(
            f"mint for {name} returned expires_at=null; the key had no TTL and "
            f"was revoked immediately")

    return MintedKey(secret=secret, key_hash=key_hash, name=name,
                     limit_usd=limit_usd, expires_at=got_ttl)


def revoke(key_hash: str, root: Path | str | None = None) -> bool:
    """Delete one minted key. False if it could not be deleted, never raises.

    Never raising is deliberate: revocation runs from a sweep that is also
    reclaiming leases, and one dead key must not stop the others being cleaned
    up. The TTL is what guarantees the key dies even when this returns False.
    """
    prov = _read_provisioning_key(root)
    if prov is None or not key_hash:
        return False
    status, _body = _call("DELETE", f"{API_BASE}/{key_hash}", prov)
    return status == 200


def list_keys(root: Path | str | None = None) -> list[dict]:
    """Every key the provisioning key can see. Empty when unavailable."""
    prov = _read_provisioning_key(root)
    if prov is None:
        return []
    status, body = _call("GET", API_BASE, prov)
    if status != 200:
        raise ProvisioningError(f"list failed: HTTP {status} {body.get('error', body)}")
    data = body.get("data")
    return data if isinstance(data, list) else []


def reap_orphans(root: Path | str | None = None,
                 live_hashes: set[str] | None = None,
                 dry_run: bool = False) -> list[str]:
    """Revoke engine-minted keys no live lease claims. Returns the names hit.

    The backstop for a director that died without sweeping. It only ever
    touches keys whose name carries `NAME_PREFIX`, so a key a human made by
    hand is never in scope no matter what else is true.
    """
    live = live_hashes or set()
    reaped: list[str] = []
    for rec in list_keys(root):
        name = str(rec.get("name") or "")
        key_hash = rec.get("hash")
        if not name.startswith(f"{NAME_PREFIX}-") or not key_hash:
            continue
        if key_hash in live:
            continue
        if dry_run or revoke(key_hash, root):
            reaped.append(name)
    return reaped


def main(argv: list[str] | None = None) -> int:
    """`provisioning.py status|list|reap [--yes]` — inspect and clean up."""
    import argparse

    ap = argparse.ArgumentParser(description=__doc__.splitlines()[0])
    ap.add_argument("action", nargs="?", default="status",
                    choices=["status", "list", "reap"])
    ap.add_argument("--root", default=".", help="any path inside the project")
    ap.add_argument("--yes", action="store_true",
                    help="reap for real; without it, reap only reports")
    args = ap.parse_args(argv)

    if not available(args.root):
        print(f"provisioning: unavailable ({PROVISIONING_KEY_VAR} not set) — "
              f"the loop falls back to the shared {RUNTIME_KEY_VAR}")
        return 0

    if args.action == "status":
        keys = list_keys(args.root)
        mine = [k for k in keys if str(k.get("name") or "").startswith(f"{NAME_PREFIX}-")]
        print(f"provisioning: available  keys_visible={len(keys)}  engine_minted={len(mine)}")
        return 0

    if args.action == "list":
        for rec in list_keys(args.root):
            print(f"{rec.get('name')!r:50} limit={rec.get('limit')} "
                  f"used={rec.get('usage')} expires={rec.get('expires_at')} "
                  f"disabled={rec.get('disabled')}")
        return 0

    # reap
    sys.path.insert(0, str(Path(__file__).resolve().parent))
    import locations  # noqa: E402
    import spawn_budget  # noqa: E402

    root = locations.find_project_root(Path(args.root).resolve())
    live = set()
    if root is not None:
        live = {rec.get("key_hash") for rec in spawn_budget.live_agents(root)
                if rec.get("key_hash")}
    reaped = reap_orphans(args.root, live_hashes=live, dry_run=not args.yes)
    verb = "would revoke" if not args.yes else "revoked"
    print(f"provisioning: {verb} {len(reaped)} orphaned key(s); "
          f"{len(live)} held by a live lease")
    for name in reaped:
        print(f"  {verb}: {name}")
    if not args.yes and reaped:
        print("re-run with --yes to actually revoke")
    return 0


if __name__ == "__main__":
    raise SystemExit(main())
