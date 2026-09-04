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
import urllib.parse
import urllib.request
from dataclasses import dataclass
from pathlib import Path

sys.path.insert(0, str(Path(__file__).resolve().parent))
import envfile  # noqa: E402

#: OpenRouter's key-management endpoint.
API_BASE = "https://openrouter.ai/api/v1/keys"
#: Workspace listing. `GET /keys` is scoped to ONE workspace (the default
#: unless asked otherwise), so enumerating everything means enumerating
#: workspaces first -- see `list_all_keys`.
WORKSPACES_BASE = "https://openrouter.ai/api/v1/workspaces"

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
#: Credits endpoint — account-level remaining budget. Not workspace-scoped.
CREDITS_BASE = "https://openrouter.ai/api/v1/credits"
#: Minimum remaining credits before refusing to mint a new key.
MIN_REMAINING_CREDITS = 1.0


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


def credit_balance(root: Path | str | None = None) -> tuple[float, float, float] | None:
    """(total, used, remaining) credits from the account-level endpoint.

    Returns None when the provisioning key is absent (absence is supported).
    Raises ProvisioningError on a failed API call with the key present, so a
    caller that cares about budget knows the answer is missing rather than zero.

    🔴 **Account-level, not workspace-scoped.** The `/credits` endpoint reports
    the whole account balance, not a single workspace's budget. A project that
    uses workspaces to isolate engine-minted keys from personal keys cannot
    distinguish the two balances here. For workspace-scoped budgets, OpenRouter
    does not expose an endpoint as of 2026-09-04.
    """
    prov = _read_provisioning_key(root)
    if prov is None:
        return None
    status, body = _call("GET", CREDITS_BASE, prov)
    if status != 200:
        raise ProvisioningError(
            f"credit_balance failed: HTTP {status} {body.get('error', body)}")
    data = body.get("data") or {}
    total = float(data.get("total_credits", 0))
    used = float(data.get("total_usage", 0))
    remaining = total - used
    return total, used, remaining


def can_fund(root: Path | str | None = None) -> tuple[bool, str | None]:
    """(ok, reason) — whether the remaining credits can fund one more key.

    The decision replaces a guess with a known threshold: a project with $1.00
    left can afford a $0.25 key. Below that boundary, the next mint risks a
    402 (insufficient credits) and leaves no escape path — the loop would need
    a key to mint keys, and no credits remain to create one.
    """
    bal = credit_balance(root)
    if bal is None:
        return True, None  # no provisioning key = shared key fallback
    _total, _used, remaining = bal
    if remaining < MIN_REMAINING_CREDITS:
        return False, (
            f"remaining credits (${remaining:.2f}) below minimum "
            f"(${MIN_REMAINING_CREDITS:.2f}) — minting a new key risks making "
            f"the loop unfundable")
    return True, None


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


def workspace(cfg: dict) -> str | None:
    """`spawn.credential.workspace_id`, or None to use the account default.

    Deliberately a **separate reader rather than a third slot in `settings`**:
    that tuple has callers, and widening it would break them to carry a value
    most projects never set. Absent means absent — the mint call omits the
    field entirely rather than sending null, so an unconfigured project keeps
    the exact behaviour it had before this existed.
    """
    cred = ((cfg.get("spawn") or {}).get("credential") or {})
    ws = str(cred.get("workspace_id") or "").strip()
    return ws or None


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
         workspace_id: str | None = None,
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

    # goal:s34 — check remaining credits before minting. Refuse to mint when
    # the remaining budget cannot fund the next key, so the loop does not paint
    # itself into a corner with no credits left to mint a key for the next
    # iteration.
    ok, reason = can_fund(root)
    if not ok:
        raise ProvisioningError(
            f"mint refused for {name}: {reason}")

    # goal:g1.11 / 2026-09-03 — `workspace_id` is honoured on create, asserted
    # against the live API before this line was written (201, and the returned
    # object carried the id back). It is omitted rather than sent as null when
    # unset, so a project that declares no workspace keeps the previous
    # behaviour exactly: the key lands in the provisioning key's default.
    #
    # This is a *safety* property, not tidiness. `reap_orphans` matches the
    # name prefix `agi-`, and the owner's own long-lived key is named `agi` —
    # one hyphen between a cleanup routine and revoking the key the project
    # runs on. Minting into a dedicated workspace makes the two sets disjoint
    # by construction instead of by string comparison.
    payload = {
        "name": name,
        "limit": limit_usd,
        "expires_at": expires_at,
    }
    if workspace_id:
        payload["workspace_id"] = workspace_id

    status, body = _call("POST", API_BASE, prov, payload)
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


def list_keys(root: Path | str | None = None,
              workspace_id: str | None = None) -> list[dict]:
    """Every key the provisioning key can see, in ONE workspace at a time.

    🔴 **`GET /keys` is scoped to the default workspace, and says nothing
    about it.** Measured 2026-09-03, the hard way: keys minted into the `agi`
    workspace were invisible here, so `status` reported `engine_minted=0`
    while two live keys were outstanding and `reap_orphans` — which iterates
    exactly this list — could not see them to revoke them.

    That is worse than the hazard the workspace was introduced to fix. The
    original risk was a reaper revoking *too much*; this was a reaper revoking
    **nothing**, silently, while reporting success. A safety mechanism that
    cannot see the objects it guards is not a weaker safety mechanism, it is
    an absent one wearing the name of a present one.

    So the workspace is passed explicitly, and every caller that cares about
    engine-minted keys passes the declared one.
    """
    prov = _read_provisioning_key(root)
    if prov is None:
        return []
    url = API_BASE
    if workspace_id:
        url = f"{API_BASE}?workspace_id={urllib.parse.quote(workspace_id)}"
    status, body = _call("GET", url, prov)
    if status != 200:
        raise ProvisioningError(f"list failed: HTTP {status} {body.get('error', body)}")
    data = body.get("data")
    return data if isinstance(data, list) else []


def list_all_keys(root: Path | str | None = None) -> list[dict]:
    """Every key in every workspace this provisioning key can reach.

    The only honest answer to "what has this engine left behind", now that
    "all keys" and "the keys `GET /keys` returns" are known to differ.
    """
    prov = _read_provisioning_key(root)
    if prov is None:
        return []
    status, body = _call("GET", WORKSPACES_BASE, prov)
    if status != 200:
        # Fall back to the default workspace rather than raising: a caller
        # asking "what is outstanding" is better served by a partial answer
        # than by an exception, PROVIDED it is not told the partial answer is
        # complete. Callers that need certainty pass an explicit workspace.
        return list_keys(root)
    seen: dict[str, dict] = {}
    for ws in (body.get("data") or []):
        ws_id = ws.get("id")
        if not ws_id:
            continue
        for rec in list_keys(root, workspace_id=ws_id):
            h = rec.get("hash")
            if h:
                seen[h] = rec
    return list(seen.values())


def reap_orphans(root: Path | str | None = None,
                 live_hashes: set[str] | None = None,
                 dry_run: bool = False,
                 workspace_id: str | None = None) -> list[str]:
    """Revoke engine-minted keys no live lease claims. Returns the names hit.

    The backstop for a director that died without sweeping. It only ever
    touches keys whose name carries `NAME_PREFIX`, so a key a human made by
    hand is never in scope no matter what else is true.

    **Two independent filters, on purpose (2026-09-03).** The name prefix was
    the only one, and it is one character wide: the owner's own long-lived key
    is named `agi`, this matches `agi-`, and a single missing hyphen would
    have revoked the key the project runs on. When a workspace is declared,
    a key must ALSO live in it to be reapable — so the owner's key, which sits
    in the default workspace, is out of scope on a second, independent ground.
    Two filters that fail differently beat one filter checked twice.

    🔴 **The listing must be scoped to the same workspace, and forgetting that
    made this function a no-op for one live run (2026-09-03).** `GET /keys`
    returns the *default* workspace; the keys being reaped are not in it. The
    first version of this filtered a list that could never contain a match, so
    it reported "0 orphaned keys" — truthfully, about the wrong set — while
    two minted keys sat outstanding. `list_all_keys` is the fallback when no
    workspace is declared, so "reap everything this engine made" stays
    answerable rather than silently meaning "reap the default workspace".
    """
    live = live_hashes or set()
    reaped: list[str] = []
    listing = (list_keys(root, workspace_id=workspace_id) if workspace_id
               else list_all_keys(root))
    for rec in listing:
        name = str(rec.get("name") or "")
        key_hash = rec.get("hash")
        if not name.startswith(f"{NAME_PREFIX}-") or not key_hash:
            continue
        if workspace_id and str(rec.get("workspace_id") or "") != workspace_id:
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

    # Both of these enumerate EVERY workspace. `status` reporting
    # `engine_minted=0` while two keys were live is exactly the failure this
    # command exists to prevent, and it happened (2026-09-03) because the
    # default listing is one workspace wide and does not say so.
    if args.action == "status":
        keys = list_all_keys(args.root)
        mine = [k for k in keys if str(k.get("name") or "").startswith(f"{NAME_PREFIX}-")]
        print(f"provisioning: available  keys_visible={len(keys)}  engine_minted={len(mine)}")
        for k in mine:
            print(f"  outstanding: {k.get('name')} used={k.get('usage')} "
                  f"expires={k.get('expires_at')}")
        return 0

    if args.action == "list":
        for rec in list_all_keys(args.root):
            print(f"{rec.get('name')!r:50} limit={rec.get('limit')} "
                  f"used={rec.get('usage')} expires={rec.get('expires_at')} "
                  f"disabled={rec.get('disabled')} ws={rec.get('workspace_id')}")
        return 0

    # reap
    sys.path.insert(0, str(Path(__file__).resolve().parent))
    import locations  # noqa: E402
    import spawn_budget  # noqa: E402

    root = locations.find_project_root(Path(args.root).resolve())
    live = set()
    cred_ws = None
    if root is not None:
        live = {rec.get("key_hash") for rec in spawn_budget.live_agents(root)
                if rec.get("key_hash")}
        # Scope the reaper to the declared workspace, so the CLI carries the
        # same second filter the library does rather than only the caller who
        # remembers to pass it.
        try:
            cred_ws = workspace(locations.load_config(root))
        except Exception:
            cred_ws = None
    reaped = reap_orphans(args.root, live_hashes=live, dry_run=not args.yes,
                          workspace_id=cred_ws)
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
