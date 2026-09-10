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
import os
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

#: OpenRouter's single-key endpoint — the RUNTIME key's OWN limit/usage/remaining.
#: The account/credits endpoints read the ACCOUNT balance; this endpoint reads the
#: one key the loop actually authenticates with. They are not the same number,
#: and the key is the one that kills rounds (hypothesis:l3-openrouter-key-
#: headroom-invisible, measured L3.29 2026-09-07: a sub-key with its own dollar
#: cap crossed it and OpenRouter reported the cross as "401 API key expired").
RUNTIME_KEY_BASE = "https://openrouter.ai/api/v1/key"
#: Default floor on the runtime key's remaining balance before dispatch refuses
#: to spend a budget slot on a spawn. Configured per project under
#: `provisioning.min_key_remaining_usd`. The default must be small enough that a
#: box whose owner has not set it does not freeze a round on a minor tick, yet
#: large enough to be noticed BEFORE the key crosses its cap mid-kid.
DEFAULT_MIN_KEY_REMAINING_USD = 1.00


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


def _read_runtime_key(root: Path | str | None = None) -> str | None:
    """The runtime key (`OPENROUTER_API_KEY`) or None.

    Read through the graph (envfile) first, falling back to `os.environ`:
    `dispatch.py` injects a freshly minted key into the child environment
    under this exact name, and a live box also carries it in `.env`. Never
    raising — absence is a supported state, and the provisioning key's scrub
    discipline is about the PROVISIONING secret, not this one.
    """
    try:
        res = envfile.resolve(str(root) if root is not None else None)
        if res.env_file.is_file():
            val = envfile.read_env(res.env_file).get(RUNTIME_KEY_VAR, "")
            if val:
                return val
    except Exception:
        pass
    return os.environ.get(RUNTIME_KEY_VAR) or None


def key_usage(root: Path | str | None = None) -> tuple[str, float | None, float | None] | None:
    """(label, limit, remaining) for the runtime key, from `GET /api/v1/key`.

    Returns None when there is no runtime key at all (absence is supported).
    Raises `ProvisioningError` on a failed API call WITH the key present, so
    a caller that asked for the number knows the answer is missing rather than
    silently zero.

    `limit` is None when the key has no dollar cap — callers print "unlimited"
    and a floor check must pass (no cap means no headroom to guard).
    """
    rk = _read_runtime_key(root)
    if rk is None:
        return None
    status, body = _call("GET", RUNTIME_KEY_BASE, rk)
    if status != 200:
        raise ProvisioningError(
            f"key_usage failed: HTTP {status} {body.get('error', body)}")
    data = body.get("data") or {}
    label = str(data.get("label") or "(unlabelled)")
    limit_raw = data.get("limit")
    limit = float(limit_raw) if limit_raw is not None else None
    used = float(data.get("usage") or 0)
    remaining = None if limit is None else limit - used
    return label, limit, remaining


def min_key_remaining_floor(cfg: dict) -> float:
    """The runtime key's remaining-balance floor from config, defaulted.

    Read from `provisioning.min_key_remaining_usd`, defaulting to
    `DEFAULT_MIN_KEY_REMAINING_USD`. Declared rather than improvised (goal:g1):
    how low the runtime key may sink before the loop stops spending slots on
    it is a run parameter, not a buried constant.
    """
    prov = ((cfg.get("provisioning") or {}))
    return float(prov.get("min_key_remaining_usd", DEFAULT_MIN_KEY_REMAINING_USD))


def check_runtime_key_floor(cfg: dict, root: Path | str | None = None) -> tuple[bool, str | None]:
    """(ok, message) — the pre-flight before a spawn takes a budget slot.

    Refuses **only** when the runtime key is readable, IS capped, and its
    remaining balance is below the configured floor. Otherwise it is True / no
    message — and crucially it is *fail-open* on a network error: an
    unreachable API must never block a round, and the refusal is reserved for
    the one measured condition (a genuine near-exhausted sub-key).
    """
    try:
        usage = key_usage(root)
    except ProvisioningError:
        return True, None  # fail-open: a network error must never block a round
    if usage is None:
        return True, None  # no runtime key to guard
    label, limit, remaining = usage
    if limit is None:
        return True, None  # uncapped key: no headroom to guard
    floor = min_key_remaining_floor(cfg)
    if remaining >= floor:
        return True, None
    patch = (f"curl -X PATCH {RUNTIME_KEY_BASE}"
             f" -H 'Authorization: Bearer ${RUNTIME_KEY_VAR}'"
             f" -H 'Content-Type: application/json'"
             f" -d '{{\"limit\": 10.00}}'")
    return False, (
        f"runtime key {label!r} remaining ${remaining:.2f} is below the configured "
        f"floor ${floor:.2f} (provisioning.min_key_remaining_usd); spending a "
        f"budget slot risks the key crossing its cap mid-round. Raise it on "
        f"OpenRouter, then PATCH: {patch}")


def _below_floor_message(which: str, label: str, remaining: float,
                         floor: float) -> str:
    """The shared refusal wording for a key reading below the floor."""
    return (
        f"{which} {label!r} remaining ${remaining:.2f} is below the configured "
        f"floor ${floor:.2f} (provisioning.min_key_remaining_usd); spending a "
        f"budget slot risks the key crossing its cap mid-round. Raise the key "
        f"on OpenRouter or revoke the drained key before the next spawn")


def check_key_floor(cfg: dict, root: Path | str | None = None) -> tuple[bool, str | None]:
    """(ok, message) — the pre-flight before a spawn takes a budget slot.

    Consults BOTH the runtime key and every outstanding engine-minted key, and
    refuses when ANY readable one is below the configured floor. This is the
    fix for hypothesis:l4-the-floor-guards-the-key-that-drains: rounds bill to
    minted per-spawn keys, so a floor that read only the runtime key could not
    move however much the loop spent. Now a drained outstanding minted key
    refuses a spawn the same way a drained runtime key does, and the runtime
    check (`check_runtime_key_floor`) still runs FIRST, unchanged.

    Fail-open is preserved for EVERY key consulted: a network error reading
    the runtime key, or the key listing, returns (True, None) — an unreachable
    API is not evidence of exhaustion and must never block a round. A minted
    key with no `limit` (uncapped) or no `usage` (unreadable/absent) passes:
    no headroom to guard, and an absent reading is not a refusal. Only keys
    THIS engine minted (`agi-` prefix) are in scope — the owner's long-lived
    key, named `agi`, and any hand-made key are never refused here.
    """
    ok, msg = check_runtime_key_floor(cfg, root)
    if not ok:
        return False, msg
    try:
        listing = list_all_keys(root)
    except ProvisioningError:
        return True, None  # fail-open: an unreachable API must never block a round
    if not listing:
        return True, None
    floor = min_key_remaining_floor(cfg)
    for rec in listing:
        name = str(rec.get("name") or "")
        if not name.startswith(f"{NAME_PREFIX}-"):
            continue  # only keys THIS engine minted are in scope
        limit = rec.get("limit")
        used = rec.get("usage")
        if limit is None or used is None:
            continue  # uncapped or unreadable → fail-open, no headroom to guard
        remaining = float(limit) - float(used)
        if remaining < floor:
            return False, _below_floor_message(
                "outstanding minted key", name, remaining, floor)
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


def _num(v) -> float | None:
    """Float, or None when absent — never 0.0 for a missing reading."""
    return None if v is None else float(v)


def capture(root: Path | str | None = None) -> dict:
    """One snapshot of every spend-visible number. READ-ONLY — never mints,
    revokes or modifies.

    Returns a dict with three sub-structures, each `None` exactly when its
    source could not be read or has nothing to read, never `0`:

      account  {total, used, remaining}  from `credit_balance` (the whole
               account balance). None on a failed API call, and when no
               provisioning key is set.
      keys     [ {name, limit, usage}, ... ] from `list_all_keys`. None when
               the listing fails (unreadable), [] when there is no
               provisioning key.
      runtime  {label, limit, usage, remaining} from `key_usage`. None when
               the runtime key is unset OR its read fails.

    The whole point (`hypothesis:l4-an-estimate-wearing-a-measurements-
    clothes`) is that a missing reading is UNKNOWN and must never be rendered
    as "nothing changed" — which is the exact reading that produced the
    hypothesis, and why an unreadable API yields None here, not 0.
    """
    account = None
    try:
        bal = credit_balance(root)
        if bal is not None:
            total, used, remaining = bal
            account = {"total": total, "used": used, "remaining": remaining}
    except ProvisioningError:
        account = None  # unreadable stays unreadable, never 0

    keys = None
    try:
        keys = []
        for rec in list_all_keys(root) or []:
            keys.append({"name": str(rec.get("name") or "(unnamed)"),
                         "limit": _num(rec.get("limit")),
                         "usage": _num(rec.get("usage"))})
    except ProvisioningError:
        keys = None  # unreadable listing, never []

    runtime = None
    try:
        ku = key_usage(root)
        if ku is not None:
            label, limit, remaining = ku
            used = None if remaining is None else (limit - remaining)
            runtime = {"label": label, "limit": limit,
                       "usage": used, "remaining": remaining}
    except ProvisioningError:
        runtime = None  # unreadable, never 0

    return {"captured_at":
            datetime.datetime.now(datetime.timezone.utc).isoformat(),
            "account": account, "keys": keys, "runtime": runtime}


def _readings(cap: dict) -> dict[str, float | None]:
    """Flatten a capture into `{label: value}` readings, with labels shared
    across captures so a diff can align them. Keys are indexed by NAME so a
    key that appears or disappears between two captures is still a bump the
    diff can see, not a silent re-alignment."""
    out: dict[str, float | None] = {}
    acc = cap.get("account")
    out["account.total"] = None if acc is None else acc.get("total")
    out["account.used"] = None if acc is None else acc.get("used")
    for k in cap.get("keys") or []:
        out[f"key:{k['name']}.usage"] = k.get("usage")
    key_names = {k.get("name") for k in cap.get("keys") or []}
    rt = cap.get("runtime")
    if rt is not None and rt.get("label") not in key_names:
        # The runtime key is almost always the `agi` key already listed, so a
        # separate `runtime.usage` row would double-count one reading and turn
        # the four-delta control (account + 3 keys) into five. Emit it only
        # when it is a distinct credential the listing cannot see.
        out["runtime.usage"] = rt.get("usage")
    return out


def diff_capture(saved: dict, now: dict) -> list[tuple[str, float | None, float | None]]:
    """`[(label, old, new), ...]` for every reading in either capture.

    A reading missing on EITHER side is `None` on that side and renders
    UNKNOWN — the diff must never turn an unreadable into a zero, because a
    zero reads as "nothing was spent" and that is the exact fabricator this
    instrument exists to remove.
    """
    old = _readings(saved)
    new = _readings(now)
    labels = list(dict.fromkeys([*old.keys(), *new.keys()]))
    rows = []
    for label in labels:
        # 🔴 `account.used` MUST BE HERE. The first version of this filter read
        # `startswith("account.total") or endswith(".usage")`, which dropped
        # `account.used` — the ONLY number on this account that has ever been
        # observed to move. `account.total` is the LIMIT ($92, constant); the
        # prime watched `used` go 87.048 -> 87.466 -> 87.798 across nine
        # dispatched rounds while all three key usages stayed byte-identical.
        # So the instrument built to end an argument about spend was blind to
        # the one reading in the argument. Caught by running it against the
        # live account rather than by its tests, which is the fourth time this
        # session that step found what a green suite could not.
        if label not in ("account.total", "account.used") \
                and not label.endswith(".usage"):
            continue  # the account limit and used, plus per-key/runtime usage
        rows.append((label, old.get(label), new.get(label)))
    return rows


def _fmt(v: float | None) -> str:
    """USD with four decimals, or UNKNOWN for a missing reading — never 0."""
    return "UNKNOWN" if v is None else f"${v:,.4f}"


def _fmt_delta(old: float | None, new: float | None) -> str:
    if old is None or new is None:
        return "UNKNOWN"  # a missing side must never read as no change
    d = new - old
    return f"${d:+,.4f}"


def _captures_dir(root: Path | str) -> Path:
    """Where capture JSON files live: the MAIN checkout's `sessions/` dir, so
    a diff in any worktree reads the same file (the same anchor `spawn_budget`
    uses for leases — captures are spend state, shared across worktrees)."""
    sys.path.insert(0, str(Path(__file__).resolve().parent))
    import locations  # noqa: E402
    graph = locations.find_project_root(Path(root).resolve()) or Path(root)
    return graph / locations.SESSIONS_DIR_NAME / ".spend-captures"


def main(argv: list[str] | None = None) -> int:
    """`provisioning.py status|list|reap [--yes] | capture [--out FILE] | diff [--prev FILE]`

    `capture` writes one snapshot of every spend-visible number to a file;
    `diff` re-reads now and prints the deltas against a saved capture.
    Both are READ-ONLY (hypothesis:l4-an-estimate-wearing-a-measurements-
    clothes): the capture is the instrument, and an unreadable reading is
    UNKNOWN, never zero.
    """
    import argparse

    ap = argparse.ArgumentParser(description=__doc__.splitlines()[0])
    ap.add_argument("action", nargs="?", default="status",
                    choices=["status", "list", "reap", "capture", "diff"])
    ap.add_argument("--root", default=".", help="any path inside the project")
    ap.add_argument("--yes", action="store_true",
                    help="reap for real; without it, reap only reports")
    ap.add_argument("--out", default=None, help="capture: where to write the snapshot")
    ap.add_argument("--prev", default=None, help="diff: which saved capture to diff against")
    args = ap.parse_args(argv)

    if args.action in ("capture", "diff"):
        cap_file = Path(args.out if args.action == "capture" else args.prev
                        or _captures_dir(args.root) / "capture.json")
        if args.action == "capture":
            data = capture(args.root)
            cap_file.parent.mkdir(parents=True, exist_ok=True)
            cap_file.write_text(json.dumps(data, indent=2))
            print(f"capture: wrote {cap_file}  @ {data['captured_at']}")
            acc = data.get("account")
            if acc is None:
                print(f"  account: UNKNOWN (unreadable or no provisioning key)")
            else:
                print(f"  account: total={_fmt(acc['total'])} used={_fmt(acc['used'])}")
            if data.get("keys") is None:
                print(f"  keys: UNKNOWN (listing unreadable)")
            else:
                for k in data["keys"]:
                    print(f"  key {k['name']!r}: limit={_fmt(k['limit'])} "
                          f"usage={_fmt(k['usage'])}")
            rt = data.get("runtime")
            if rt is None:
                print(f"  runtime: UNKNOWN (unset or unreadable)")
            else:
                print(f"  runtime {rt['label']!r}: limit={_fmt(rt['limit'])} "
                      f"usage={_fmt(rt['usage'])}")
            return 0

        # diff
        if not cap_file.is_file():
            print(f"capture diff: no saved capture at {cap_file} — "
                  f"run 'provisioning.py capture' first")
            return 2
        saved = json.loads(cap_file.read_text())
        now = capture(args.root)
        rows = diff_capture(saved, now)
        print(f"capture diff: {cap_file}  vs  now")
        for label, old, new in rows:
            print(f"  {label:32} {_fmt(old):>10} -> {_fmt(new):>10}  "
                  f"\u0394 {_fmt_delta(old, new)}")
        return 0

    if not available(args.root):
        print(f"provisioning: unavailable ({PROVISIONING_KEY_VAR} not set) — "
              f"the loop falls back to the shared {RUNTIME_KEY_VAR}")
    else:
        # Both of these enumerate EVERY workspace. `status` reporting
        # `engine_minted=0` while two keys were live is exactly the failure this
        # command exists to prevent, and it happened (2026-09-03) because the
        # default listing is one workspace wide and does not say so.
        keys = list_all_keys(args.root)
        mine = [k for k in keys if str(k.get("name") or "").startswith(f"{NAME_PREFIX}-")]
        print(f"provisioning: available  keys_visible={len(keys)}  engine_minted={len(mine)}")
        for k in mine:
            print(f"  outstanding: {k.get('name')} used={k.get('usage')} "
                  f"expires={k.get('expires_at')}")

    # hypothesis:l3-openrouter-key-headroom-invisible — the RUNTIME key's own
    # headroom, printed whether or not a provisioning key exists. The account
    # credits line read the account; this is the one key the loop actually
    # authenticates with, and it is the one that kills a round. Measured
    # 2026-09-07: a sub-key crossing its dollar cap surfaced as "401 API key
    # expired" while the account line looked perfectly healthy. Unconditional
    # on provisioning availability because the runtime key exists regardless.
    try:
        usage = key_usage(args.root)
    except ProvisioningError as exc:
        print(f"  {RUNTIME_KEY_VAR}: unknown — {exc}")
    else:
        if usage is not None:
            label, limit, remaining = usage
            if limit is None:
                print(f"  {RUNTIME_KEY_VAR}: label={label}  limit=unlimited  "
                      f"remaining=${remaining if remaining is not None else 0:,.2f}")
            else:
                used = limit - remaining
                print(f"  {RUNTIME_KEY_VAR}: label={label}  limit=${limit:,.2f}  "
                      f"used=${used:,.2f}  remaining=${remaining:,.2f}")
        else:
            print(f"  {RUNTIME_KEY_VAR}: not set — no runtime-key headroom to report")

    if args.action == "status":
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
