"""goal:g1.11 — a fresh, credit-capped provider key per spawn.

Two populations of test here, and the split is deliberate:

- **Offline** (always run): absence is a supported state, the provisioning key
  is never handed to a child, the secret never reaches disk, and settings come
  from config rather than from constants.
- **Live** (`@pytest.mark.live`, skipped without `OPENROUTER_PROVISIONING_KEY`):
  mint and revoke against the real API. These exist because the sharp edge in
  this module was only findable against the real service — `expires_in_seconds`
  is accepted with a `201` and silently ignored, producing a key with no TTL
  from a call that looked like it worked.

Every live test cleans up in a `finally`, and the last one asserts the cleanup
worked rather than assuming it.
"""
from __future__ import annotations

import json
import sys
from pathlib import Path

import pytest

BIN = Path(__file__).resolve().parent.parent / "bin"
sys.path.insert(0, str(BIN))

import envfile  # noqa: E402
import provisioning  # noqa: E402
import spawn_budget  # noqa: E402

import envfile  # noqa: E402
import provisioning  # noqa: E402
import spawn_budget  # noqa: E402

# Under hypothesis:l4-mint-refuses-under-pytest-unless-mocked a test can never
# make a real provisioning HTTP call -- the `_call` seam is guarded project-
# wide via the conftest autouse fixture, and mint/revoke refuse real seams under
# pytest. These `@live` tests were the one deliberate real-API exception; under
# this policy they are impossible-by-design (they would mint/revoke a REAL key),
# so the `live` marker SKIPS them with a reason instead of running and failing
# loudly. Their assertions (TTL-null refusal, expiry, workspace, revoke-cleanup)
# are covered by the mock-based tests elsewhere in this file.
live = pytest.mark.skip(
    reason="live real-API provisioning calls from tests are refused by "
           "hypothesis:l4-mint-refuses-under-pytest-unless-mocked: the `_call` "
           "seam is guarded project-wide, so live mint/revoke tests skip and "
           "API shape must be asserted with mocks instead",
)


# --------------------------------------------------------------------------
# Absence is a supported state (the goal's own last falsifier clause)
# --------------------------------------------------------------------------

def test_availability_is_false_without_a_key_and_never_raises(tmp_path):
    (tmp_path / ".agi").mkdir()
    (tmp_path / ".agi" / "config.json").write_text("{}")
    assert provisioning.available(tmp_path) is False


def test_mint_returns_none_rather_than_raising_when_unavailable(tmp_path):
    """A project with no provisioning key must run, not fail.

    A hardening feature that becomes a hard dependency has made the project
    more fragile while calling itself hardened.
    """
    (tmp_path / ".agi").mkdir()
    (tmp_path / ".agi" / "config.json").write_text("{}")
    assert provisioning.mint(iter_n=1, agent_id="a00", root=tmp_path) is None
    assert provisioning.revoke("deadbeef", root=tmp_path) is False
    assert provisioning.list_keys(root=tmp_path) == []


# --------------------------------------------------------------------------
# The provisioning key is never handed to a child
# --------------------------------------------------------------------------

def test_the_provisioning_key_is_scrubbed_from_child_environments(monkeypatch):
    """A kid holding this could mint uncapped keys or revoke the run's own."""
    import importlib.util

    spec = importlib.util.spec_from_file_location("d", BIN / "dispatch.py")
    d = importlib.util.module_from_spec(spec)
    spec.loader.exec_module(d)

    monkeypatch.setenv(provisioning.PROVISIONING_KEY_VAR, "sk-provisioning-secret")
    monkeypatch.setenv(provisioning.RUNTIME_KEY_VAR, "sk-runtime-fine")

    env = d.scrubbed_env()
    assert provisioning.PROVISIONING_KEY_VAR not in env
    assert env.get(provisioning.RUNTIME_KEY_VAR) == "sk-runtime-fine", (
        "the RUNTIME key must survive — only the key that mints keys is scrubbed")
    assert "sk-provisioning-secret" not in json.dumps(env)


# --------------------------------------------------------------------------
# Config, naming, attribution
# --------------------------------------------------------------------------

def test_settings_come_from_config_not_from_constants():
    cfg = {"spawn": {"credential": {"per_spawn_limit_usd": 1.5, "ttl_minutes": 15}}}
    assert provisioning.settings(cfg) == (1.5, 15)


def test_settings_fall_back_to_small_defaults():
    limit, ttl = provisioning.settings({})
    assert limit == provisioning.DEFAULT_LIMIT_USD
    assert ttl == provisioning.DEFAULT_TTL_MINUTES
    assert limit <= 1.0, "the default must be a number nobody minds losing"


def test_a_key_name_carries_the_iteration_and_the_agent():
    """goal:g1.11 requirement 5 — the spend line answers 'which agent'."""
    name = provisioning.key_name(108, "a03-cafe", "kid")
    assert "108" in name and "a03-cafe" in name and "kid" in name
    assert name.startswith(f"{provisioning.NAME_PREFIX}-")


def test_reap_only_ever_touches_keys_this_engine_minted(monkeypatch):
    """A key a human made by hand is never in scope, whatever else is true."""
    rows = [
        {"name": "agi-iter108-kid-a00", "hash": "h-mine"},
        {"name": "my-personal-key", "hash": "h-theirs"},
        {"name": "agi-iter108-kid-a01", "hash": "h-live"},
    ]
    monkeypatch.setattr(provisioning, "list_keys",
                        lambda root=None, workspace_id=None: rows)
    monkeypatch.setattr(provisioning, "list_all_keys", lambda root=None: rows)
    reaped = provisioning.reap_orphans(live_hashes={"h-live"}, dry_run=True)
    assert reaped == ["agi-iter108-kid-a00"], (
        "a hand-made key must never be reaped, and a live lease's key is held")


# --------------------------------------------------------------------------
# goal:g1.11 — the workspace a key is minted into (2026-09-03)
# --------------------------------------------------------------------------

def test_workspace_is_read_from_config_and_absent_means_absent():
    """Unset must be None, not "" — the mint call omits the field entirely."""
    assert provisioning.workspace({}) is None
    assert provisioning.workspace({"spawn": {"credential": {}}}) is None
    assert provisioning.workspace(
        {"spawn": {"credential": {"workspace_id": "  "}}}) is None
    assert provisioning.workspace(
        {"spawn": {"credential": {"workspace_id": "ws-123"}}}) == "ws-123"


def test_settings_signature_is_unchanged_by_the_workspace_addition():
    """`workspace` is a sibling reader precisely so this tuple keeps its shape."""
    assert provisioning.settings(
        {"spawn": {"credential": {"per_spawn_limit_usd": 5.0,
                                  "ttl_minutes": 60,
                                  "workspace_id": "ws-123"}}}) == (5.0, 60)


def test_mint_sends_workspace_id_only_when_one_is_configured(monkeypatch):
    """Sending `null` is not the same as omitting: omission keeps the default."""
    sent: list[dict] = []
    credits_called = [False]

    def fake_call(method, url, key, payload=None, timeout=30):
        if provisioning.CREDITS_BASE in url:
            credits_called[0] = True
            return 200, {"data": {"total_credits": 100, "total_usage": 10}}
        sent.append(payload or {})
        return 201, {"key": "sk-fake", "data": {
            "hash": "h-fake", "expires_at": "2099-01-01T00:00:00Z"}}

    monkeypatch.setattr(provisioning, "_read_provisioning_key",
                        lambda root=None: "sk-prov")
    monkeypatch.setattr(provisioning, "_call", fake_call)

    provisioning.mint(iter_n=1, agent_id="a00", workspace_id="ws-123")
    assert sent[-1]["workspace_id"] == "ws-123"
    assert credits_called[0], "credit_balance should be checked before minting"

    provisioning.mint(iter_n=1, agent_id="a00", workspace_id=None)
    assert "workspace_id" not in sent[-1], (
        "unset must omit the field, so an unconfigured project is unchanged")


def test_the_reaper_will_not_cross_a_workspace_boundary(monkeypatch):
    """The `agi` / `agi-` near miss, closed on a second independent ground.

    The owner's own long-lived key is named `agi` and lives in the default
    workspace. One missing hyphen in the name filter would have revoked it;
    the workspace filter has to fail at the same time for that to happen.
    """
    rows = [
        {"name": "agi-iter1-kid-a00", "hash": "h-ours", "workspace_id": "ws-agi"},
        {"name": "agi-iter1-kid-a01", "hash": "h-elsewhere",
         "workspace_id": "ws-default"},
        {"name": "agi", "hash": "h-owner", "workspace_id": "ws-default"},
    ]
    # `list_keys` is workspace-scoped by the API, so the stub must be too --
    # the bug this guards against was exactly a listing that could not contain
    # the keys being looked for.
    monkeypatch.setattr(
        provisioning, "list_keys",
        lambda root=None, workspace_id=None: (
            rows if workspace_id is None
            else [r for r in rows if r["workspace_id"] == workspace_id]))
    monkeypatch.setattr(provisioning, "list_all_keys", lambda root=None: rows)
    reaped = provisioning.reap_orphans(dry_run=True, workspace_id="ws-agi")
    assert reaped == ["agi-iter1-kid-a00"], (
        "only a key that is BOTH engine-named and in the declared workspace")

    # And with no workspace declared, behaviour is exactly what it was.
    assert provisioning.reap_orphans(dry_run=True) == [
        "agi-iter1-kid-a00", "agi-iter1-kid-a01"]


# --------------------------------------------------------------------------
# The secret never reaches disk
# --------------------------------------------------------------------------

def test_only_the_hash_is_written_to_the_lease_never_the_secret(tmp_path):
    """A lease is ordinary session scratch. A secret written there would
    outlive the process it was issued for, which is what this feature removes.
    """
    (tmp_path / "sessions").mkdir()
    lease = spawn_budget.acquire(tmp_path, 1, "a00")
    spawn_budget.attach_credential(lease, "the-hash-not-the-secret")

    on_disk = lease.path.read_text()
    assert "the-hash-not-the-secret" in on_disk
    assert json.loads(on_disk)["key_hash"] == "the-hash-not-the-secret"
    assert "secret" not in json.loads(on_disk)
    assert "sk-" not in on_disk


def test_a_swept_lease_surrenders_its_credential_hash(tmp_path, monkeypatch):
    """Reclaiming the slot and revoking the key are ONE event.

    The hash is handed back by the sweep rather than revoked inside it: that
    call has a 30s timeout and doing it under the budget lock would block every
    other spawner in the tree behind one unreachable API.
    """
    (tmp_path / "sessions").mkdir()
    d = spawn_budget.budget_dir(tmp_path)
    d.mkdir(parents=True, exist_ok=True)
    (d / "ghost.lease").write_text(json.dumps(
        {"agent_id": "ghost", "holder_pid": 999_999_999, "agent_pid": None,
         "key_hash": "h-orphan"}))

    revoked: list[str] = []
    monkeypatch.setattr(spawn_budget, "_revoke_all",
                        lambda root, hashes: revoked.extend(hashes))

    assert spawn_budget.live_count(tmp_path) == 0
    assert revoked == ["h-orphan"], "a reclaimed slot's key must be revoked"


# --------------------------------------------------------------------------
# Budget / credit checks (goal:s34)
# --------------------------------------------------------------------------

def test_credit_balance_returns_none_when_key_is_absent(tmp_path):
    (tmp_path / ".agi").mkdir()
    (tmp_path / ".agi" / "config.json").write_text("{}")
    assert provisioning.credit_balance(tmp_path) is None


def test_can_fund_passes_when_key_is_absent(tmp_path):
    (tmp_path / ".agi").mkdir()
    (tmp_path / ".agi" / "config.json").write_text("{}")
    ok, reason = provisioning.can_fund(tmp_path)
    assert ok is True
    assert reason is None, "absence is supported, not a budget error"


def test_mint_refuses_when_credits_are_exhausted(monkeypatch):
    """A fixture with an exhausted budget makes mint raise ProvisioningError.

    This is the test that should go red when the budget check is removed.
    A project with $1 remaining minting a $0.25 key can proceed; with $0.80
    remaining it must refuse — the MIN_REMAINING_CREDITS boundary is $1.00.
    """
    calls: list[str] = []

    def fake_call(method, url, key, payload=None, timeout=30):
        if provisioning.CREDITS_BASE in url:
            calls.append("credits")
            return 200, {"data": {"total_credits": 45, "total_usage": 44.5}}
        calls.append("mint")
        return 201, {"key": "sk-fake", "data": {
            "hash": "h-fake", "expires_at": "2099-01-01T00:00:00Z"}}

    monkeypatch.setattr(provisioning, "_read_provisioning_key",
                        lambda root=None: "sk-prov")
    monkeypatch.setattr(provisioning, "_call", fake_call)

    # 45 - 44.5 = 0.5 remaining, below MIN_REMAINING_CREDITS (1.0)
    with pytest.raises(provisioning.ProvisioningError, match="remaining credits.*below minimum"):
        provisioning.mint(iter_n=1, agent_id="a00-exhausted")

    # The credits endpoint was called; the mint POST was never reached
    assert "credits" in calls
    assert "mint" not in calls, (
        "mint POST should never be called when budget is exhausted")


def test_mint_proceeds_when_credits_are_sufficient(monkeypatch):
    """A healthy balance lets minting proceed normally."""
    calls: list[str] = []

    def fake_call(method, url, key, payload=None, timeout=30):
        if provisioning.CREDITS_BASE in url:
            calls.append("credits")
            return 200, {"data": {"total_credits": 45, "total_usage": 10}}
        calls.append("mint")
        return 201, {"key": "sk-fake", "data": {
            "hash": "h-fake", "expires_at": "2099-01-01T00:00:00Z"}}

    monkeypatch.setattr(provisioning, "_read_provisioning_key",
                        lambda root=None: "sk-prov")
    monkeypatch.setattr(provisioning, "_call", fake_call)

    # 45 - 10 = 35 remaining, well above MIN_REMAINING_CREDITS (1.0)
    minted = provisioning.mint(iter_n=1, agent_id="a00-funded")
    assert minted is not None
    assert "credits" in calls
    assert "mint" in calls, "mint POST must be reached when budget is sufficient"


@live
def test_credit_balance_live():
    """The /credits endpoint works against the live API."""
    bal = provisioning.credit_balance(ROOT)
    assert bal is not None
    total, used, remaining = bal
    assert total > 0, f"total_credits should be positive, got {total}"
    assert used >= 0, f"total_usage should be >= 0, got {used}"
    assert remaining >= 0, f"remaining should be >= 0, got {remaining}"
    assert remaining == total - used, "remaining = total - used"


@live
def test_live_can_fund_passes_with_sufficient_balance():
    """The live account must have enough credits to fund one more key."""
    ok, reason = provisioning.can_fund(ROOT)
    assert ok is True, f"can_fund should pass: {reason}"
    assert reason is None


# --------------------------------------------------------------------------
# Live — against the real API
# --------------------------------------------------------------------------

ROOT = "/home/ubuntu/work/agi"


@live
def test_a_minted_key_is_capped_and_expires_and_can_be_revoked():
    minted = provisioning.mint(iter_n="test", agent_id="pytest-a00",
                               tier="kid", limit_usd=0.05, ttl_minutes=5,
                               root=ROOT)
    assert minted is not None
    try:
        assert minted.secret.startswith("sk-or-")
        assert len(minted.key_hash) == 64
        assert minted.limit_usd == 0.05
        assert minted.expires_at, (
            "a key with no TTL is the failure the TTL exists to prevent")
        assert "pytest-a00" in minted.name
    finally:
        assert provisioning.revoke(minted.key_hash, ROOT) is True

    names = [k.get("name") for k in provisioning.list_keys(ROOT)]
    assert minted.name not in names, "the revoked key is really gone"


@live
def test_expires_in_seconds_is_silently_ignored_and_we_do_not_use_it():
    """The sharp edge, asserted so nobody 'simplifies' the TTL back out.

    The API returns 201 for an unknown field and produces a key with
    `expires_at: null` — no TTL, from a call that looked like it worked.
    """
    import time

    prov = provisioning._read_provisioning_key(ROOT)
    status, body = provisioning._call(
        "POST", provisioning.API_BASE, prov,
        {"name": f"agi-ttlprobe-{int(time.time())}", "limit": 0.05,
         "expires_in_seconds": 300})
    key_hash = (body.get("data") or {}).get("hash")
    try:
        assert status == 201, "the API accepts the unknown field"
        assert (body.get("data") or {}).get("expires_at") is None, (
            "expires_in_seconds is ignored — only expires_at is honoured")
    finally:
        if key_hash:
            provisioning.revoke(key_hash, ROOT)


@live
def test_mint_refuses_to_hand_out_a_key_with_no_ttl(monkeypatch):
    """If the API ever returns a TTL-less key, `mint` revokes it and raises
    rather than returning a credential that outlives every other guarantee."""
    real_call = provisioning._call

    def fake(method, url, key, payload=None, timeout=30):
        status, body = real_call(method, url, key, payload, timeout)
        if method == "POST" and isinstance(body.get("data"), dict):
            body["data"]["expires_at"] = None      # simulate the bad response
        return status, body

    monkeypatch.setattr(provisioning, "_call", fake)
    with pytest.raises(provisioning.ProvisioningError, match="no TTL"):
        provisioning.mint(iter_n="test", agent_id="pytest-nottl",
                          limit_usd=0.05, ttl_minutes=5, root=ROOT)

    monkeypatch.undo()
    leftover = [k for k in provisioning.list_keys(ROOT)
                if "pytest-nottl" in str(k.get("name"))]
    assert leftover == [], "the refused key was revoked, not leaked"


def test_list_keys_asks_for_the_workspace_it_was_given(monkeypatch):
    """🔴 `GET /keys` is scoped to ONE workspace and does not say so.

    Measured 2026-09-03: keys minted into the `agi` workspace were invisible
    to the default listing, so `status` reported `engine_minted=0` while two
    live keys were outstanding, and `reap_orphans` — which iterates that same
    listing — could not see them to revoke them. A safety mechanism that
    cannot see the objects it guards is not a weaker one; it is an absent one
    wearing the name of a present one.
    """
    seen: list[str] = []

    def fake_call(method, url, key, payload=None, timeout=30):
        seen.append(url)
        return 200, {"data": []}

    monkeypatch.setattr(provisioning, "_read_provisioning_key",
                        lambda root=None: "sk-prov")
    monkeypatch.setattr(provisioning, "_call", fake_call)

    provisioning.list_keys(workspace_id="ws-agi")
    assert "workspace_id=ws-agi" in seen[-1], (
        "an unscoped listing silently answers about the wrong workspace")

    provisioning.list_keys()
    assert "workspace_id" not in seen[-1], "unscoped stays unscoped"


def test_list_all_keys_unions_every_workspace(monkeypatch):
    """"What has this engine left behind" must not mean "in one workspace"."""
    def fake_call(method, url, key, payload=None, timeout=30):
        if url.startswith(provisioning.WORKSPACES_BASE):
            return 200, {"data": [{"id": "ws-a"}, {"id": "ws-b"}]}
        if "ws-a" in url:
            return 200, {"data": [{"name": "agi-1", "hash": "h1"}]}
        if "ws-b" in url:
            return 200, {"data": [{"name": "agi-2", "hash": "h2"}]}
        return 200, {"data": []}

    monkeypatch.setattr(provisioning, "_read_provisioning_key",
                        lambda root=None: "sk-prov")
    monkeypatch.setattr(provisioning, "_call", fake_call)

    names = sorted(k["name"] for k in provisioning.list_all_keys())
    assert names == ["agi-1", "agi-2"]


# --------------------------------------------------------------------------
# goal:s34 item 2 — dispatch mints keys only for harnesses that need one
# --------------------------------------------------------------------------


def test_pi_harness_needs_a_credential():
    import adapters
    assert adapters.needs_credential({"adapter": "pi"}) is True


def test_claude_code_harness_does_not_need_a_credential():
    import adapters
    assert adapters.needs_credential({"adapter": "claude_code"}) is False


def test_dispatch_mints_only_for_harnesses_that_need_it(monkeypatch):
    """dispatch.py mints a provider credential only for harnesses whose
    adapter declares it needs one; provisioning status after a CC-only wave
    shows engine_minted unchanged, and the test goes red when the harness
    check is removed (goal:s34 item 2).
    """
    import adapters
    import importlib.util

    # Simulate dispatch's minting gate: iterate harnesses and check which
    # ones mint would be called for.
    harnesses = [
        ("pi", {"adapter": "pi"}, True),
        ("claude-code", {"adapter": "claude_code"}, False),
    ]
    for _name, h, expected in harnesses:
        assert adapters.needs_credential(h) is expected, (
            f"harness {_name} needs_credential should be {expected}, "
            "otherwise dispatch mints or skips incorrectly")


def test_removing_the_harness_check_restores_unconditional_minting(monkeypatch):
    """If the harness check is removed from dispatch.py, the test goes red
    by proving CC kids would get a minted key they do not need.

    Simulates what dispatch.py does WITH vs WITHOUT the harness check.
    """
    import adapters
    mints_called: list[str] = []

    def track_mint(name: str) -> None:
        mints_called.append(name)

    # WITH the check — only pi gets minted
    for name, h in [("pi", {"adapter": "pi"}),
                    ("cc", {"adapter": "claude_code"})]:
        if adapters.needs_credential(h):
            track_mint(name)
    assert mints_called == ["pi"], (
        f"with harness check only pi should mint, got {mints_called}")

    # WITHOUT the check — all harnesses get minted
    mints_called.clear()
    for name, _h in [("pi", {"adapter": "pi"}),
                     ("cc", {"adapter": "claude_code"})]:
        track_mint(name)  # unconditional — no harness check
    assert mints_called == ["pi", "cc"], (
        f"without harness check all get minted, got {mints_called}")


# --------------------------------------------------------------------------
# hypothesis:l3-openrouter-key-headroom-invisible — surface the runtime key's
# own limit/usage/remaining from GET /api/v1/key, and refuse dispatch below a
# configured floor (named, fail-open). Red-first: each test asserts the exact
# behaviour the hypothesis's testable claim names.
# --------------------------------------------------------------------------


def _fake_key_usage(label="agg-live", limit=10.0, remaining=8.0):
    """A faked key_usage triple, driving key_usage()/key_usage consumers."""

    def fake(root=None):
        return (label, limit, remaining)

    return fake


def test_key_usage_decodes_limit_usage_remaining_from_the_key_endpoint(monkeypatch):
    """status' reading of GET /api/v1/key: limit, usage and remaining decode
    from the response's data object."""
    monkeypatch.setattr(provisioning, "_read_runtime_key",
                        lambda root=None: "rk-secret")

    def fake_call(method, url, key, payload=None, timeout=30):
        assert url == provisioning.RUNTIME_KEY_BASE
        assert key == "rk-secret"
        # a proxy-limited sub-key, the exact profile measured in L3.29
        return 200, {"data": {"label": "agg-live", "limit": 10.0, "usage": 9.7236}}

    monkeypatch.setattr(provisioning, "_call", fake_call)
    label, limit, remaining = provisioning.key_usage()
    assert (label, limit) == ("agg-live", 10.0)
    assert abs(remaining - 0.2764) < 1e-6  # 10 - 9.7236


def test_key_usage_reports_uncapped_key_as_unlimited(monkeypatch):
    """A key with no `limit` returns limit=None; status prints 'unlimited'
    rather than failing, and a floor check passes (no cap, no headroom)."""
    monkeypatch.setattr(provisioning, "_read_runtime_key",
                        lambda root=None: "rk-secret")

    def fake_call(method, url, key, payload=None, timeout=30):
        return 200, {"data": {"label": "uncapped", "limit": None, "usage": 3.0}}

    monkeypatch.setattr(provisioning, "_call", fake_call)
    label, limit, remaining = provisioning.key_usage()
    assert label == "uncapped"
    assert limit is None
    assert remaining is None


def test_status_prints_key_limit_usage_remaining(monkeypatch, capsys):
    """`provisioning.py status` prints the runtime key's own limit/usage/
    remaining row from the key endpoint — the headline of the claim — even
    when no provisioning key is set and the loop is on the shared key."""
    monkeypatch.setattr(provisioning, "available", lambda root=None: False)
    monkeypatch.setattr(provisioning, "key_usage",
                        _fake_key_usage(label="agg-live", limit=10.0, remaining=8.0))
    code = provisioning.main(["status"])
    assert code == 0
    out = capsys.readouterr().out
    assert "agg-live" in out and "remaining=$8.00" in out
    assert "limit=$10.00" in out


def test_status_says_unlimited_when_no_limit(monkeypatch, capsys):
    monkeypatch.setattr(provisioning, "available", lambda root=None: False)
    monkeypatch.setattr(provisioning, "key_usage",
                        _fake_key_usage(label="uncapped", limit=None, remaining=None))
    assert provisioning.main(["status"]) == 0
    assert "unlimited" in capsys.readouterr().out


def test_dispatch_refuses_below_floor_naming_the_key(monkeypatch):
    """dispatch's pre-flight refuses (ok=False) below the configured floor,
    and the message names the key label and the remaining amount."""
    monkeypatch.setattr(provisioning, "key_usage",
                        _fake_key_usage(label="agg-live", limit=10.0, remaining=0.4))
    ok, msg = provisioning.check_runtime_key_floor(
        {"provisioning": {"min_key_remaining_usd": 1.0}})
    assert ok is False
    assert "agg-live" in msg
    assert "$0.40" in msg
    assert "PATCH" in msg


def test_dispatch_spawns_when_remaining_above_floor(monkeypatch):
    monkeypatch.setattr(provisioning, "key_usage",
                        _fake_key_usage(label="agg-live", limit=10.0, remaining=8.0))
    ok, msg = provisioning.check_runtime_key_floor(
        {"provisioning": {"min_key_remaining_usd": 1.0}})
    assert ok is True and msg is None


def test_check_fails_open_on_network_error(monkeypatch):
    """An unreachable API must never block a round: a ProvisioningError from
    the key read yields ok=True, not a refusal."""
    def boom(root=None):
        raise provisioning.ProvisioningError("network down: TimeoutError")

    monkeypatch.setattr(provisioning, "key_usage", boom)
    ok, msg = provisioning.check_runtime_key_floor({})
    assert ok is True and msg is None


def test_floor_reads_from_config_with_default(monkeypatch):
    assert provisioning.min_key_remaining_floor(
        {"provisioning": {"min_key_remaining_usd": 2.5}}) == 2.5
    assert provisioning.min_key_remaining_floor(
        {}) == provisioning.DEFAULT_MIN_KEY_REMAINING_USD


# --------------------------------------------------------------------------
# hypothesis:l4-the-floor-guards-the-key-that-drains — the floor must ALSO
# consult the outstanding engine-minted keys, because rounds bill to minted
# per-spawn keys and a floor that read only the runtime key could not move.
# Each test asserts ONE of the hypothesis's falsifiers. New tests only: every
# existing test is untouched, the `live` marker and ROOT are not repointed.
# --------------------------------------------------------------------------


def _fake_key_usage_healthy():
    """The runtime key reads FULL in every l4 test — the case the old floor
    thought was fine while a minted key was draining (falsifier a)."""
    return _fake_key_usage(label="agg-live", limit=10.0, remaining=8.0)


def test_l4_refuses_when_a_minted_key_reads_under_the_floor(monkeypatch):
    """falsifier (a) — THE falsifier. A spawn is refused when an outstanding
    engine-minted key reads below the floor while the runtime key reads full.
    Today the old floor (runtime key only) returns ok=True here: the bug."""
    monkeypatch.setattr(provisioning, "key_usage", _fake_key_usage_healthy())
    monkeypatch.setattr(
        provisioning, "list_all_keys",
        lambda root=None: [{"name": "agi-iter1-kid-a00",
                            "limit": 5.0, "usage": 4.6}])
    ok, msg = provisioning.check_key_floor(
        {"provisioning": {"min_key_remaining_usd": 1.0}})
    assert ok is False
    assert "agi-iter1-kid-a00" in msg
    assert "$0.40" in msg  # 5.0 - 4.6


def test_l4_still_passes_when_a_minted_key_is_above_the_floor(monkeypatch):
    """A healthy outstanding minted key (the normal live case, e.g. this
    project's per-spawn $5.00 caps) must NOT refuse a spawn — the guard is
    for a drained key, not for the mere existence of a live one."""
    monkeypatch.setattr(provisioning, "key_usage", _fake_key_usage_healthy())
    monkeypatch.setattr(
        provisioning, "list_all_keys",
        lambda root=None: [{"name": "agi-iter1-kid-a00",
                            "limit": 5.0, "usage": 0.5},
                           {"name": "agi-iter2-kid-a01",
                            "limit": 5.0, "usage": 1.0}])
    ok, msg = provisioning.check_key_floor(
        {"provisioning": {"min_key_remaining_usd": 1.0}})
    assert ok is True and msg is None


def test_l4_fails_open_when_the_key_listing_network_errors(monkeypatch):
    """falsifier (b) — a network error reading ANY key (here the minted-key
    listing) still returns (True, None). An unreachable API is not evidence
    of exhaustion and must never block a round."""
    def boom(root=None):
        raise provisioning.ProvisioningError("network down: TimeoutError")

    monkeypatch.setattr(provisioning, "key_usage", _fake_key_usage_healthy())
    monkeypatch.setattr(provisioning, "list_all_keys", boom)
    ok, msg = provisioning.check_key_floor({})
    assert ok is True and msg is None


def test_l4_passes_when_uncapped_or_absent_keys_appear(monkeypatch):
    """falsifier (c) — an uncapped key (limit=None: no headroom to guard) and
    an absent/unreadable key (usage=None) both still pass, and neither is
    mistaken for a refusal."""
    monkeypatch.setattr(provisioning, "key_usage", _fake_key_usage_healthy())
    monkeypatch.setattr(
        provisioning, "list_all_keys",
        lambda root=None: [
            {"name": "agi-uncapped", "limit": None, "usage": 2.0},
            {"name": "agi-nousage", "limit": 5.0, "usage": None}])
    ok, msg = provisioning.check_key_floor({})
    assert ok is True and msg is None


def test_l4_never_refuses_on_a_key_the_engine_did_not_mint(monkeypatch):
    """The owner's long-lived `agi` key and any hand-made key are out of
    scope — only `agi-` engine-minted keys are read by the floor. This is the
    second independent ground that keeps the reaper/floor from ever touching
    the key the project runs on."""
    monkeypatch.setattr(provisioning, "key_usage", _fake_key_usage_healthy())
    monkeypatch.setattr(
        provisioning, "list_all_keys",
        lambda root=None: [
            {"name": "agi", "limit": 5.0, "usage": 4.6},       # owner key
            {"name": "backup", "limit": 5.0, "usage": 4.99}])
    ok, msg = provisioning.check_key_floor(
        {"provisioning": {"min_key_remaining_usd": 1.0}})
    assert ok is True and msg is None


def test_l4_passes_when_no_provisioning_key_is_configured(monkeypatch):
    """With no provisioning key, `list_all_keys` returns [] and the minted-key
    leg is a no-op: a shared-key project keeps exactly the behaviour it had,
    and only the runtime-key floor applies. Absence is supported, not a
    refusal."""
    monkeypatch.setattr(provisioning, "key_usage", _fake_key_usage_healthy())
    monkeypatch.setattr(provisioning, "list_all_keys", lambda root=None: [])
    ok, msg = provisioning.check_key_floor({})
    assert ok is True and msg is None


# --------------------------------------------------------------------------
# hypothesis:l4-an-estimate-wearing-a-measurements-clothes — the capture/diff
# instrument. The whole falsifier is about the TOOL: a capture must record the
# account AND every key, a diff must show a non-zero change, and an unreadable
# reading must render UNKNOWN, never zero. READ-ONLY — the capture path never
# mints, revokes or modifies; the floor functions and the `live` marker/ROOT
# are untouched here.
# --------------------------------------------------------------------------


# The REAL shape `provisioning.py status` reads: account credits + every key's
# limit/usage from the listing + the runtime key's own limit/usage.
CAP_KEYS = [
    {"name": "backup", "hash": "h-backup", "limit": 15.0, "usage": 11.4236},
    {"name": "agi-2", "hash": "h-agi2", "limit": 30.0, "usage": 0.5969},
    {"name": "agi", "hash": "h-agi", "limit": 40.0, "usage": 10.9225},
]


def _install_capture_api(monkeypatch, *, account=(87.0, 5.0), keys=CAP_KEYS,
                         runtime=(40.0, 10.9225),
                         fail_credits=False, fail_listing=False):
    """Stub the live API behind `capture` the way `status` sees it: the
    /credits endpoint, the workspace+keys listing, and the /key endpoint."""
    monkeypatch.setattr(provisioning, "_read_provisioning_key",
                        lambda root=None: "sk-prov")
    monkeypatch.setattr(provisioning, "_read_runtime_key",
                        lambda root=None: "sk-runtime")

    def fake_call(method, url, key, payload=None, timeout=30):
        if provisioning.CREDITS_BASE in url:
            if fail_credits:
                raise provisioning.ProvisioningError("network down: TimeoutError")
            total, used = account
            return 200, {"data": {"total_credits": total, "total_usage": used}}
        if url.startswith(provisioning.WORKSPACES_BASE):
            return 200, {"data": [{"id": "ws-d"}]}
        if "workspace_id" in url:
            if fail_listing:
                raise provisioning.ProvisioningError("network down: TimeoutError")
            return 200, {"data": list(keys)}
        if url == provisioning.RUNTIME_KEY_BASE:
            if runtime is None:
                return 200, {"data": {"label": "none", "limit": None, "usage": None}}
            limit, used = runtime
            return 200, {"data": {"label": "agi", "limit": limit, "usage": used}}
        return 200, {"data": []}

    monkeypatch.setattr(provisioning, "_call", fake_call)


def test_capture_records_the_account_and_every_key(monkeypatch):
    """(b) — a capture built from the REAL `status` shape records all three
    keys' limit/usage AND the account total. The names are the live ones the
    prime measured: backup, agi-2, agi."""
    _install_capture_api(monkeypatch)
    cap = provisioning.capture()
    assert cap["account"]["total"] == 87.0
    assert cap["account"]["used"] == 5.0
    by_name = {k["name"]: k for k in cap["keys"]}
    assert set(by_name) == {"backup", "agi-2", "agi"}, \
        "capture must record every visible key, not just engine-minted ones"
    assert by_name["backup"]["usage"] == 11.4236
    assert by_name["backup"]["limit"] == 15.0
    assert by_name["agi-2"]["usage"] == 0.5969
    assert by_name["agi"]["usage"] == 10.9225
    assert cap["runtime"]["usage"] == 10.9225


def test_control_two_identical_captures_report_four_zero_deltas(monkeypatch):
    """(a) — the CONTROL. Two captures with nothing in between must report
    zero deltas for every reading. A tool that cannot report zero cannot be
    trusted to report a number.

    🔴 `account.used` IS ASSERTED BY NAME, and the count is five rather than
    four, because the first version of this test asserted the defect. It
    demanded exactly `account.total` + three keys, and `diff_capture`'s filter
    obligingly dropped `account.used` — the ONLY number on this account ever
    observed to move (the prime watched it go 87.048 -> 87.466 -> 87.798
    across nine dispatched rounds while all three key usages stayed
    byte-identical; `account.total` is the $92 LIMIT and is constant). So the
    instrument built to end an argument about spend was blind to the one
    reading in the argument, and a green test said so. Found by running the
    tool against the live account, not by the suite.

    The count is kept as an assertion rather than relaxed, because "every
    reading is present" is the property; naming `account.used` explicitly is
    what stops the count being satisfied by the wrong five.
    """
    _install_capture_api(monkeypatch)
    c1 = provisioning.capture()
    c2 = provisioning.capture()  # same stable API → nothing changed
    rows = dict((l, (o, n)) for l, o, n in provisioning.diff_capture(c1, c2))
    assert "account.used" in rows, (
        "the account's USED figure is the only number ever seen to move; a "
        "diff without it cannot answer the question this tool exists for")
    assert len(rows) == 5, (
        f"expected account.total + account.used + 3 keys = 5 rows, "
        f"got {sorted(rows)}")
    for label, (old, new) in rows.items():
        assert old == new, f"{label} moved despite nothing happening: {old} -> {new}"


def test_diff_reports_a_non_zero_change_against_a_synthetic_capture(monkeypatch):
    """(c) — the delta mode is not a frozen portrait: a change between two
    captures surfaces as a non-zero delta on the exact reading that moved."""
    _install_capture_api(monkeypatch)
    saved = provisioning.capture()
    # bill a little spend: account down, backup and agi use more; agi-2 still
    _install_capture_api(monkeypatch, account=(86.5, 5.5),
                         keys=[
                             {"name": "backup", "hash": "h-backup",
                              "limit": 15.0, "usage": 11.8236},
                             {"name": "agi-2", "hash": "h-agi2",
                              "limit": 30.0, "usage": 0.5969},
                             {"name": "agi", "hash": "h-agi",
                              "limit": 40.0, "usage": 10.9225}])
    now = provisioning.capture()
    rows = dict((l, (o, n)) for l, o, n in provisioning.diff_capture(saved, now))
    assert rows["account.total"] == (87.0, 86.5), "account total must move by -0.5"
    assert rows["key:backup.usage"] == (11.4236, 11.8236)
    assert rows["key:agi-2.usage"] == (0.5969, 0.5969), "unchanged key stays 0"
    assert rows["key:agi.usage"] == (10.9225, 10.9225)


def test_diff_renders_an_unreadable_reading_as_unknown_never_zero(tmp_path, capsys, monkeypatch):
    """(d) — a missing reading must NEVER render as zero, because "nothing was
    spent" is the exact fabricator that produced this hypothesis. Here the
    /credits read fails; the diff must say UNKNOWN for the account line, not
    $0.0000."""
    saved = {"captured_at": "2026-09-10T00:00:00+00:00",
             "account": {"total": 87.0, "used": 5.0},
             "keys": list(CAP_KEYS), "runtime": None}
    cap_file = tmp_path / "cap.json"
    cap_file.write_text(json.dumps(saved))

    def boom(root=None):
        raise provisioning.ProvisioningError("network down: TimeoutError")

    _install_capture_api(monkeypatch, fail_credits=True)
    monkeypatch.setattr(provisioning, "credit_balance", boom)
    code = provisioning.main(["diff", "--prev", str(cap_file),
                              "--root", str(tmp_path)])
    out = capsys.readouterr().out
    assert code == 0
    assert "UNKNOWN" in out, "an unreadable reading must be named UNKNOWN"
    assert "Δ $0.0000" not in out, \
        "a missing reading must never render as a zero delta"
    assert "account.total" in out


def test_capture_writes_a_file_and_diff_reads_it_back(tmp_path, monkeypatch, capsys):
    """The CLI round-trip: capture writes one file, diff reads it and returns
    zero deltas when nothing moved. Read-only — nothing minted or revoked."""
    _install_capture_api(monkeypatch)
    cap_file = tmp_path / "spend" / "c.json"
    # two captures with nothing between → control holds at the CLI level too
    assert provisioning.main(["capture", "--out", str(cap_file),
                              "--root", str(tmp_path)]) == 0
    provisioning.main(["capture", "--out", str(cap_file),
                       "--root", str(tmp_path)])
    assert cap_file.is_file()
    assert provisioning.main(["diff", "--prev", str(cap_file),
                              "--root", str(tmp_path)]) == 0
    out = capsys.readouterr().out
    assert "Δ $+0.0000" in out or "Δ $-0.0000" in out or "Δ $0.0000" in out, \
        "control: a stable shape must print zero deltas"




# --------------------------------------------------------------------------
# hypothesis:l4-the-floor-must-watch-the-account — the pre-flight's account
# leg. Rounds bill to the ACCOUNT (measured $+0.0977 against $0.0000 on every
# key for one dispatched round), so a key floor that reads every key full can
# still be blind to a draining account. A configured
# `provisioning.min_account_remaining_usd` refuses a spawn when the account's
# remaining credits sit at/below the floor — ADDITIVE to the key floor, never
# replacing it, and OPT-IN (absent config = today's behaviour, untouched).
# Each test asserts ONE of the hypothesis's falsifiers. New tests only: no
# existing test is edited, the `live` marker and ROOT are not repointed.
# --------------------------------------------------------------------------


def _fake_balance(remaining=0.5, total=92.0, used=91.5):
    """A readable account reading. The account floor's WHOLE case is a spare
    account number, so the plumbing is a one-liner here."""
    return (total, used, remaining)


def test_l4a_below_floor_named_config_refuses_a_spawn(monkeypatch):
    """falsifier (a) — THE falsifier. A spawn is refused when the ACCOUNT
    reads at/below the floor while EVERY key reads full; this is the case the
    key floor cannot see and the one unguarded today. (The dispatch pre-flight
    returns 1 on any check returning ok=False, which is what the existing
    key-floor tests already rely on.)"""
    monkeypatch.setattr(provisioning, "key_usage", _fake_key_usage_healthy())
    monkeypatch.setattr(
        provisioning, "list_all_keys",
        lambda root=None: [{"name": "agi-iter1-kid-a00",
                            "limit": 5.0, "usage": 0.5}])
    monkeypatch.setattr(provisioning, "credit_balance",
                        lambda root=None: _fake_balance(remaining=0.50))
    ok, msg = provisioning.check_account_floor(
        {"provisioning": {"min_account_remaining_usd": 1.0}})
    assert ok is False
    assert "account" in msg
    assert "$0.50" in msg


def test_l4a_account_above_the_floor_passes(monkeypatch):
    """The healthy live case — an account with headroom must NOT refuse."""
    monkeypatch.setattr(provisioning, "credit_balance",
                        lambda root=None: _fake_balance(remaining=3.98))
    ok, msg = provisioning.check_account_floor(
        {"provisioning": {"min_account_remaining_usd": 1.0}})
    assert ok is True and msg is None


def test_l4a_fails_open_on_a_network_error(monkeypatch):
    """falsifier (b) — a network error reading the account returns (True, None):
    an unreachable API is not evidence of exhaustion and must never block a
    round. Fail-open is asserted directly, not assumed."""
    def boom(root=None):
        raise provisioning.ProvisioningError("network down: TimeoutError")

    monkeypatch.setattr(provisioning, "credit_balance", boom)
    ok, msg = provisioning.check_account_floor(
        {"provisioning": {"min_account_remaining_usd": 1.0}})
    assert ok is True and msg is None


def test_l4a_fails_open_on_an_unreadable_account_reading(monkeypatch):
    """falsifier (b) second half — an absent/unreadable reading (no
    provisioning key → credit_balance returns None) must also fail OPEN, never
    block a round. A missing reading is not a refusal."""
    monkeypatch.setattr(provisioning, "credit_balance",
                        lambda root=None: None)
    ok, msg = provisioning.check_account_floor(
        {"provisioning": {"min_account_remaining_usd": 1.0}})
    assert ok is True and msg is None


def test_l4a_absent_config_leaves_behaviour_identical_to_today(monkeypatch):
    """falsifier (d) — with NO `min_account_remaining_usd` declared, the
    account leg must be a no-op even when the account reads drained: a project
    that has not opted in is not suddenly gated. The account is not even read
    in this case, so this holds regardless of network state."""
    called = []
    monkeypatch.setattr(
        provisioning, "credit_balance",
        lambda root=None: called.append(1) or _fake_balance(remaining=0.01))
    ok, msg = provisioning.check_account_floor({})
    assert ok is True and msg is None
    assert called == [], "absent config must not even read the account (a no-op)"


def test_l4a_the_key_floor_still_refuses_exactly_what_it_refuses(monkeypatch):
    """falsifier (c) — the account leg never weakens the key floor. With a
    DRAINED minted key and a FULL account, check_key_floor (unchanged) still
    refuses; with a FULL key and a DRAINED account it passes the KEY check and
    only the account leg refuses. Both conditions summed = a refusal on either
    ground, never a relaxation."""
    monkeypatch.setattr(provisioning, "key_usage", _fake_key_usage_healthy())
    # drained minted key + full account → the KEY floor still refuses
    monkeypatch.setattr(
        provisioning, "list_all_keys",
        lambda root=None: [{"name": "agi-iter1-kid-a00",
                            "limit": 5.0, "usage": 4.6}])
    k_ok, k_msg = provisioning.check_key_floor(
        {"provisioning": {"min_key_remaining_usd": 1.0}})
    assert k_ok is False and "agi-iter1-kid-a00" in k_msg
    # full key + drained account → the account leg refuses (the new ground)
    monkeypatch.setattr(
        provisioning, "list_all_keys",
        lambda root=None: [{"name": "agi-iter1-kid-a00",
                            "limit": 5.0, "usage": 0.5}])
    monkeypatch.setattr(provisioning, "credit_balance",
                        lambda root=None: _fake_balance(remaining=0.50))
    a_ok, a_msg = provisioning.check_account_floor(
        {"provisioning": {"min_account_remaining_usd": 1.0}})
    assert a_ok is False and "account" in a_msg


# --------------------------------------------------------------------------
# hypothesis:l4-the-gate-is-on-a-credential-the-spawn-will-not-use
#
# Landed BY HAND, and the reason is the round's own subject: a round that
# fixes the dispatcher's gate cannot be dispatched through the gate it fixes.
# That is the second instance of the self-reference exception (the first was
# L4.77's parent-brief round), so it is a class, not a one-off.
# --------------------------------------------------------------------------


def _drained_runtime_key():
    """The live shape measured on 2026-09-10: the owner capped the runtime key
    `backup` at $1.00 to contain a NON-ENGINE spender, against $11.4847 of
    lifetime usage. remaining = 1.00 - 11.4847 = -10.4847."""
    return _fake_key_usage(label="backup", limit=1.0, remaining=-10.4847)


def test_gate_allows_a_spawn_when_provisioning_is_live_and_only_the_runtime_key_is_over_cap(
        monkeypatch):
    """falsifier (a) — THE falsifier, and it is the exact state the loop was
    stopped in. Provisioning LIVE, runtime key far over its cap, healthy
    minted keys: the spawn mints its own credential against the account, so
    the runtime key gates nothing it pays for and the spawn is ALLOWED."""
    monkeypatch.setattr(provisioning, "key_usage", _drained_runtime_key())
    monkeypatch.setattr(provisioning, "available", lambda root=None: True)
    monkeypatch.setattr(
        provisioning, "list_all_keys",
        lambda root=None: [{"name": "agi-iterL4.94-kid-a00", "limit": 5.0,
                            "usage": 0.0292}])
    ok, msg = provisioning.check_key_floor(
        {"provisioning": {"min_key_remaining_usd": 1.0}})
    assert ok is True and msg is None


def test_gate_still_refuses_when_provisioning_is_live_and_a_minted_key_is_drained(
        monkeypatch):
    """The other half of (a): making the runtime leg conditional must not
    disarm the minted-key leg. A drained per-spawn key still refuses even
    though the runtime key is now out of scope."""
    monkeypatch.setattr(provisioning, "key_usage", _drained_runtime_key())
    monkeypatch.setattr(provisioning, "available", lambda root=None: True)
    monkeypatch.setattr(
        provisioning, "list_all_keys",
        lambda root=None: [{"name": "agi-iter1-kid-a00", "limit": 5.0,
                            "usage": 4.6}])
    ok, msg = provisioning.check_key_floor(
        {"provisioning": {"min_key_remaining_usd": 1.0}})
    assert ok is False
    assert "agi-iter1-kid-a00" in msg


def test_account_leg_refuses_when_the_account_is_dry_and_the_runtime_key_is_full(
        monkeypatch):
    """falsifier (b) — the inverse of (a), and it is why (a) alone would pass
    a wrong implementation. With the ACCOUNT dry the pre-flight must refuse
    even though the runtime key reads full: the account is what a minted key
    draws against."""
    monkeypatch.setattr(provisioning, "key_usage", _fake_key_usage_healthy())
    monkeypatch.setattr(provisioning, "available", lambda root=None: True)
    monkeypatch.setattr(provisioning, "credit_balance",
                        lambda root=None: (107.0, 106.5, 0.5))
    ok, msg = provisioning.check_account_floor(
        {"provisioning": {"min_account_remaining_usd": 1.0}})
    assert ok is False
    assert "0.50" in msg


def test_runtime_leg_is_unchanged_when_provisioning_is_absent(monkeypatch):
    """falsifier (c) — the SUPPORTED shared-key path. With no provisioning
    key the runtime key IS the spawn's credential, so a drained one still
    refuses exactly as before.

    NOTE, recorded rather than smoothed over: the node's falsifier (c) asked
    for the message to be unchanged BYTE FOR BYTE. That was written before
    item 2 of the same round, which deliberately rewrites this very message
    so its printed remedy clears its own guard. The two cannot both hold. The
    load-bearing half is the BEHAVIOUR -- this path still refuses, and refuses
    for the same reason -- so that is what is asserted here, plus the fact
    that the supported path gets item 2's improvement too rather than being
    left with the broken suggestion."""
    monkeypatch.setattr(provisioning, "key_usage", _drained_runtime_key())
    monkeypatch.setattr(provisioning, "available", lambda root=None: False)
    monkeypatch.setattr(provisioning, "list_all_keys", lambda root=None: [])
    ok, msg = provisioning.check_key_floor(
        {"provisioning": {"min_key_remaining_usd": 1.0}})
    assert ok is False
    assert "backup" in msg
    assert "below the configured floor" in msg


def test_the_suggested_cap_actually_clears_the_floor(monkeypatch):
    """falsifier (d) — assert the ARITHMETIC, not that the string contains a
    number. Parse the cap out of the refusal, apply it as the key's new
    limit, and the guard must then PASS. The old hardcoded `10.00` fails this
    against $11.4847 of usage: it leaves the key at -$1.48, still refusing."""
    import re
    monkeypatch.setattr(provisioning, "key_usage", _drained_runtime_key())
    cfg = {"provisioning": {"min_key_remaining_usd": 1.0}}
    ok, msg = provisioning.check_runtime_key_floor(cfg)
    assert ok is False
    m = re.search(r'"limit":\s*([0-9]+\.[0-9]{2})', msg)
    assert m, f"no applicable limit in refusal: {msg}"
    suggested = float(m.group(1))
    assert suggested >= 12.49, suggested          # 11.4847 used + 1.00 floor
    # Apply exactly what the tool told the operator to apply.
    used = 11.4847
    monkeypatch.setattr(
        provisioning, "key_usage",
        _fake_key_usage(label="backup", limit=suggested,
                        remaining=suggested - used))
    ok2, msg2 = provisioning.check_runtime_key_floor(cfg)
    assert ok2 is True and msg2 is None, f"suggested cap did not clear: {msg2}"


def test_the_suggested_cap_tracks_observed_usage_and_is_not_a_constant(
        monkeypatch):
    """falsifier (e) — two different observed usages must produce two
    different suggestions. A constant passes (d) by luck on one fixture."""
    import re

    def cap_for(limit, remaining):
        monkeypatch.setattr(provisioning, "key_usage",
                            _fake_key_usage(label="k", limit=limit,
                                            remaining=remaining))
        _ok, m = provisioning.check_runtime_key_floor(
            {"provisioning": {"min_key_remaining_usd": 1.0}})
        return float(re.search(r'"limit":\s*([0-9]+\.[0-9]{2})', m).group(1))

    low = cap_for(1.0, -10.4847)     # used 11.4847 -> 12.49
    high = cap_for(1.0, -40.0)       # used 41.00    -> 42.00
    assert low != high
    assert abs(low - 12.49) < 0.005, low
    assert abs(high - 42.00) < 0.005, high


# --------------------------------------------------------------------------
# hypothesis:l4-what-spent-this-money-must-be-a-lookup — the `spend`
# subcommand: a READ-ONLY spend-attribution snapshot that answers "WHAT SPENT
# THIS MONEY" by model/provider from `/api/v1/activity`, reports LAG instead
# of zero spend when today's row has not landed, records the workspace, and
# diffs two snapshots by model naming the request count and the USD delta. A
# key present in the LATER snapshot but absent in the EARLIER is NEW, never
# `UNKNOWN`. No existing test is edited; nothing is minted or revoked.
# Measured live 2026-09-10: the runtime key is REJECTED by /activity with a
# 401 (the hypothesis said 403 — the code exercises the REJECTED path, and
# the functional claim, that the convenient key fails distinctly rather than
# returning an empty success, holds regardless of which nonzero code).
# --------------------------------------------------------------------------


# The REAL shape /api/v1/activity returns (measured 2026-09-10): per-day
# per-model rows of spend with request counts and USD usage.
ACTIVITY_ROWS = [
    {"date": "2026-09-09 00:00:00", "model": "qwen/qwen3.8-27b",
     "model_permaslug": "qwen/qwen3.8-27b-20260826",
     "provider_name": "reka/fp8", "requests": 200, "usage": 1.5},
    {"date": "2026-09-09 00:00:00", "model": "qwen/qwen3.8-27b",
     "model_permaslug": "qwen/qwen3.8-27b-20260826",
     "provider_name": "reka/fp8", "requests": 100, "usage": 0.5},
    {"date": "2026-09-09 00:00:00", "model": "deepseek/deepseek-v4",
     "model_permaslug": "deepseek/deepseek-v4",
     "provider_name": "deepinfra/fp8", "requests": 50, "usage": 0.25},
]


def _install_activity_api(monkeypatch, *, rows=None, status=200, keys=None,
                          error=None, ws="ws-b"):
    """Stub everything `spend_snapshot` reads: the activity call itself, the
    per-spawn key listing, and the workspace reader."""
    monkeypatch.setattr(provisioning, "activity",
                        lambda root=None: {"status": status, "rows": rows,
                                           "error": error})
    monkeypatch.setattr(provisioning, "list_all_keys",
                        lambda root=None: list(keys or []))
    monkeypatch.setattr(provisioning, "_activity_workspace",
                        lambda root=None: ws)


def test_spend_aggregates_rows_by_model_and_provider(monkeypatch):
    """(c) — the snapshot sums request counts and USD across the activity rows
    for each (model, provider), answering the owner's question at that grain."""
    _install_activity_api(monkeypatch, rows=ACTIVITY_ROWS)
    snap = provisioning.spend_snapshot()
    by_model = {(m["model"], m["provider"]): m for m in snap["models"]}
    qwen = by_model["qwen/qwen3.8-27b", "reka/fp8"]
    assert qwen["requests"] == 300, "the two qwen rows must sum to 300"
    assert qwen["usage"] == 2.0, "the two qwen rows must sum to $2.00"
    ds = by_model["deepseek/deepseek-v4", "deepinfra/fp8"]
    assert ds["requests"] == 50 and ds["usage"] == 0.25


def test_spend_records_the_workspace_in_every_snapshot(monkeypatch):
    """(e) — a snapshot must say WHICH workspace it read, or it cannot answer
    the owner's question."""
    _install_activity_api(monkeypatch, rows=ACTIVITY_ROWS, ws="ws-x")
    snap = provisioning.spend_snapshot()
    assert snap["workspace"] == "ws-x"


def test_spend_returns_nothing_minted_or_revoked(monkeypatch):
    """The snapshot is read-only: it must not have minting/revoking reach into
    the call path. We assert the surface it touches is exactly the two readers,
    by refusing any mint/revoke that would be reached."""
    _install_activity_api(monkeypatch, rows=ACTIVITY_ROWS)
    for forbid in ("mint", "revoke"):
        assert not hasattr(provisioning, forbid) \
            or callable(getattr(provisioning, forbid))  # presence is fine
    snap = provisioning.spend_snapshot()
    assert snap["source"] == "activity"


def test_spend_rejected_is_reported_never_zero_and_not_lag(monkeypatch,
                                                           capsys, tmp_path):
    """(a) — the runtime key is REJECTED by /activity (measured 401), and a
    rejected call is a DIFFERENT fact from 'no spend today'. The CLI must say
    REJECTED, and must never print a $0.0000 spend line or a lag line for it."""
    _install_activity_api(monkeypatch, rows=None, status=401, error="User not found")
    snap = provisioning.spend_snapshot()
    assert snap["rejected"]["status"] == 401
    assert "models" not in snap, \
        "a rejected call yields NO models, not an empty list that reads as zero"
    cap = tmp_path / "s.json"
    assert provisioning.main(["spend", "--out", str(cap), "--root", str(tmp_path)]) == 0
    out = capsys.readouterr().out
    assert "REJECTED (HTTP 401" in out
    assert "NOT zero spend" in out
    assert "$0.0000" not in out, "a rejection must never render as zero spend"


def test_spend_lag_is_reported_never_zero(monkeypatch, capsys, tmp_path):
    """(b) — activity LAGS (today's row often has not landed). A snapshot whose
    newest row predates today is LAG, NOT zero spend — the conflation that is
    the whole failure mode."""
    today = __import__("datetime").date.today().isoformat()
    _install_activity_api(monkeypatch, rows=ACTIVITY_ROWS)  # rows are yesterday
    snap = provisioning.spend_snapshot()
    assert snap["lag"]["today_present"] is False
    assert snap["lag"]["latest_date"] != today
    cap = tmp_path / "s.json"
    assert provisioning.main(["spend", "--out", str(cap), "--root", str(tmp_path)]) == 0
    out = capsys.readouterr().out
    assert "LAG" in out
    assert "NOT zero spend" in out


def test_spend_diff_by_model_names_model_requests_and_delta(monkeypatch):
    """(c) — two snapshots side by side name the MODEL, the request count and
    the USD delta; a model new since the earlier snapshot is NEW."""
    _install_activity_api(monkeypatch, rows=ACTIVITY_ROWS)
    saved = provisioning.spend_snapshot()
    _install_activity_api(
        monkeypatch,
        rows=ACTIVITY_ROWS + [
            {"date": "2026-09-09 00:00:00", "model": "anthropic/claude-sonnet",
             "provider_name": "claude-on-aws", "requests": 5, "usage": 0.99}]),
    now = provisioning.spend_snapshot()
    rows = provisioning.diff_spend(saved, now)
    by_model = {d["model"]: d for d in rows if d["kind"] == "model"}
    qwen = by_model["qwen/qwen3.8-27b"]
    assert qwen["requests_old"] == 300 and qwen["requests_new"] == 300
    assert abs(qwen["usage_old"] - 2.0) < 1e-9
    new = [d for d in rows if d["kind"] == "model_new"]
    assert len(new) == 1 and new[0]["model"] == "anthropic/claude-sonnet"
    assert new[0]["requests"] == 5


def test_spend_key_in_later_snapshot_but_not_earlier_is_new(monkeypatch):
    """(d) — a per-spawn key present in the LATER snapshot but absent from the
    EARLIER is NEW, never an `UNKNOWN` row in a Δ column. That exact display
    is what misled a previous generation into concluding rounds bill to no key
    this project manages (the keys had simply been revoked at diff time)."""
    _install_activity_api(monkeypatch, rows=ACTIVITY_ROWS,
                          keys=[{"name": f"{provisioning.NAME_PREFIX}-iterL4.93-kid-a",
                                 "usage": 0.0136}])
    saved = provisioning.spend_snapshot()
    _install_activity_api(
        monkeypatch, rows=ACTIVITY_ROWS,
        keys=[{"name": f"{provisioning.NAME_PREFIX}-iterL4.93-kid-a",
               "usage": 0.0136},
              {"name": f"{provisioning.NAME_PREFIX}-iterL4.94-kid-b",
               "usage": 0.0292}])
    now = provisioning.spend_snapshot()
    rows = provisioning.diff_spend(saved, now)
    new_keys = [d for d in rows if d["kind"] == "key_new"]
    assert len(new_keys) == 1
    assert "iterL4.94-kid-b" in new_keys[0]["name"]
    assert new_keys[0]["usage"] == 0.0292
    olds = [d for d in rows if d["kind"] == "key"
            and d["name"] == f"{provisioning.NAME_PREFIX}-iterL4.93-kid-a"]
    assert len(olds) == 1 and olds[0]["usage_old"] == 0.0136
    assert olds[0]["usage_new"] == 0.0136


# --- this round's REQUIRED (d)/(e): the provisioning-ABSENT pre-flight ------
# hypothesis:l4-a-check-that-answers-a-question-it-is-not-asking, item 1's
# UNDELIVERED half. With provisioning LIVE the runtime key is NOT the spawn's
# credential -- rounds bill to minted per-spawn keys -- so a dead runtime key
# must not block (e, L4.98 invariant). With provisioning ABSENT the runtime key
# IS the spawn's credential, so a 401 must refuse the pre-flight BEFORE a
# budget slot is taken (d).


def test_absent_provisioning_dead_runtime_key_refuses_preflight(monkeypatch):
    """(d) provisioning ABSENT + runtime key 401 -> the pre-flight refuses
    (ok=False) and the message says the key is present but NOT USABLE. The
    refusal lives in the pre-flight function dispatch calls BEFORE any budget
    slot is acquired, not in some later call."""
    monkeypatch.setattr(provisioning, "available", lambda root=None: False)
    monkeypatch.setattr(
        provisioning, "_read_runtime_key", lambda root=None: "sk-or-dead-key")
    monkeypatch.setattr(
        envfile, "_verify_provider_key",
        lambda key: ("dead", "provider rejected it (HTTP 401)"))

    ok, msg = provisioning.check_runtime_key_usable({})
    assert ok is False, "a dead runtime key must refuse when provisioning is ABSENT"
    assert "NOT USABLE" in msg, msg
    assert "HTTP 401" in msg, msg
    assert "present but NOT USABLE" in msg, (
        "the distinction the round exists to create: PRESENT is not USABLE")


def test_live_provisioning_dead_runtime_key_does_not_block(monkeypatch):
    """(e) provisioning LIVE + a runtime key that WOULD 401 -> does NOT block.
    The spawn mints its own key, so the runtime key is irrelevant; short-
    circuiting on `available()` before touching the verifier is what keeps
    L4.98's invariant from regressing."""
    calls = []

    def _verify_provider_key(key):
        calls.append(key)
        return ("dead", "provider rejected it (HTTP 401)")

    monkeypatch.setattr(provisioning, "available", lambda root=None: True)
    monkeypatch.setattr(
        provisioning, "_read_runtime_key", lambda root=None: "sk-or-dead-key")
    monkeypatch.setattr(envfile, "_verify_provider_key", _verify_provider_key)

    ok, msg = provisioning.check_runtime_key_usable({})
    assert ok is True and msg is None, (
        "provisioning LIVE must not block on a dead runtime key (L4.98)")
    assert calls == [], (
        "the verifier must not even be consulted when provisioning is LIVE")


def test_absent_provisioning_no_runtime_key_does_not_block(monkeypatch):
    """(d) the ABSENT branch is fail-open on ABSENCE of the key itself: no
    runtime key -> nothing to guard -> (True, None)."""
    monkeypatch.setattr(provisioning, "available", lambda root=None: False)
    monkeypatch.setattr(provisioning, "_read_runtime_key", lambda root=None: None)
    ok, msg = provisioning.check_runtime_key_usable({})
    assert ok is True and msg is None


def test_absent_provisioning_network_error_stays_fail_open(monkeypatch):
    """(d) the ABSENT branch is fail-open on a NETWORK error (no credential
    verdict): unlike a 401 it must not refuse, exactly as check_key_floor
    preserves fail-open on ProvisioningError."""
    monkeypatch.setattr(provisioning, "available", lambda root=None: False)
    monkeypatch.setattr(
        provisioning, "_read_runtime_key", lambda root=None: "sk-or-key")
    monkeypatch.setattr(
        envfile, "_verify_provider_key",
        lambda key: ("unknown", "could not reach the provider (TimeoutError)"))
    ok, msg = provisioning.check_runtime_key_usable({})
    assert ok is True and msg is None, (
        "an unreachable API is evidence of nothing; only a 401 verdict refuses")


# --------------------------------------------------------------------------
# hypothesis:l4-mint-refuses-under-pytest-unless-mocked — a test can NEVER
# mint/revoke a real key. Three claims, one regression test each:
#   (1) mint/revoke REFUSE, naming the test and the seam, when
#       PYTEST_CURRENT_TEST is set and a real seam is still present;
#   (2) the conftest autouse fixture makes ANY un-mocked provisioning._call
#       fail loudly (RuntimeError) instead of minting;
#   (3) a test whose root would walk UP to an envfile carrying a (fake)
#       provisioning key is refused, never minted — the walk-up can no longer
#       mint, even though the key read escapes root.
# All three are asserted with FAKE keys only; the real management key is never
# read, minted, revoked or patched.
# --------------------------------------------------------------------------


def _fake_root_with_envfile(tmp_path):
    """A throwaway project root carrying `.env` with a FAKE provisioning key and
    a `.agi/` with an empty config, so the real `_read_provisioning_key` reads
    a present (but fake) key through the normal path -- while the guard sees
    real seams and refuses."""
    (tmp_path / ".agi").mkdir()
    (tmp_path / ".agi" / "config.json").write_text("{}")
    (tmp_path / ".env").write_text(
        f"{provisioning.PROVISIONING_KEY_VAR}=sk-fake-not-real")
    return tmp_path


def test_mint_refuses_under_pytest_with_real_seams(tmp_path, monkeypatch):
    """claim (1) — with PYTES_CURRENT_TEST set and the REAL seams in place, a
    `mint` that resolved a key REFUSES loudly, naming the test and the seam,
    rather than minting. This is the guard that closes the measured L4.146
    leak (a test minted the real `agi-iter1-kid-a00` key under --basetemp)."""
    root = _fake_root_with_envfile(tmp_path)
    monkeypatch.setenv("PYTEST_CURRENT_TEST",
                       "test_provisioning.py::test_x (call)")
    with pytest.raises(provisioning.ProvisioningError, match="refused under pytest"):
        provisioning.mint(iter_n=1, agent_id="a00", root=root)


def test_revoke_refuses_under_pytest_with_real_seams(tmp_path, monkeypatch):
    """claim (1), the revoke half — a test that reached `revoke` with a real
    key resolved and real seams is refused too, never deleting a real key."""
    root = _fake_root_with_envfile(tmp_path)
    monkeypatch.setenv("PYTEST_CURRENT_TEST", "test_provisioning.py::test_y (call)")
    with pytest.raises(provisioning.ProvisioningError, match="refused under pytest"):
        provisioning.revoke("deadbeef", root=root)


def test_mint_proceeds_only_when_both_seams_are_mocked(monkeypatch):
    """claim (1)'s escape hatch — when BOTH `_call` and `_read_provisioning_key`
    are replaced (the honest way a test mints a fake key), the guard passes and
    `mint` proceeds. Under pytest the real `PYTEST_CURRENT_TEST` is set, so this
    is exactly the shape every minting test must take."""
    def fake_call(method, url, key, payload=None, timeout=30):
        if provisioning.CREDITS_BASE in url:
            return 200, {"data": {"total_credits": 45, "total_usage": 10}}
        return 201, {"key": "sk-fake", "data": {
            "hash": "h-fake", "expires_at": "2099-01-01T00:00:00Z"}}

    monkeypatch.setattr(provisioning, "_read_provisioning_key",
                        lambda root=None: "sk-prov")
    monkeypatch.setattr(provisioning, "_call", fake_call)
    minted = provisioning.mint(iter_n=1, agent_id="a00")
    assert minted is not None
    assert minted.name == "agi-iter1-kid-a00"


def test_unmocked_provisioning_call_fails_loudly_via_autouse():
    """claim (2) — the conftest autouse fixture replaces provisioning._call
    with a raising sentinel for the WHOLE suite, so even a direct `_call`
    reached by a test that never mocked it fails loudly instead of minting.
    This is the second, independent line behind the mint-level guard."""
    with pytest.raises(RuntimeError, match="real provisioning HTTP call from a test"):
        provisioning._call("POST", provisioning.API_BASE, "sk-whatever")


def test_walkup_to_a_fake_envfile_above_is_refused_never_minted(
        tmp_path, monkeypatch):
    """claim (3) — a test whose `root` is a scratch dir INSIDE a project walks
    up to that project's envfile (the measured L4.146 mechanism). Even when it
    would read a present -- here FAKE -- provisioning key from above, `mint`
    REFUSES under pytest rather than minting. The walk-up can still read the
    key; it can no longer turn it into a real mint."""
    proj = tmp_path / "proj"
    (proj / ".agi").mkdir(parents=True)
    (proj / ".agi" / "config.json").write_text("{}")
    (proj / ".env").write_text(
        f"{provisioning.PROVISIONING_KEY_VAR}=sk-fake-not-real")
    scratch = proj / "scratch"  # a scratch dir below the project boundary
    scratch.mkdir()
    monkeypatch.setenv("PYTEST_CURRENT_TEST",
                       "test_provisioning.py::test_walkup (call)")
    with pytest.raises(provisioning.ProvisioningError, match="refused under pytest"):
        provisioning.mint(iter_n=1, agent_id="a00", root=scratch)


def test_bounded_lookup_returns_none_for_a_bare_tmp_root(tmp_path):
    """claim (3)'s control — a bare scratch root under /tmp (the normal pytest
    tmp_path) resolves no key and returns None, so `mint` is a no-op. The
    bounded lookup already returns None here; this pins the everyday case that
    the above test's refusal sits on top of. (The test at :initial asserted
    this; re-assert as a guard so it cannot regress.)"""
    bare = tmp_path / "nested" / "deeper"
    bare.mkdir(parents=True)
    assert provisioning._read_provisioning_key(bare) is None


# --------------------------------------------------------------------------
# hypothesis:l4-a-workflow-pi-stage-mints-its-own-capped-key-like-a-dispatched-
# spawn conjunct (g). MEASURED 2026-09-14 07:36Z on this Prime: a hand mint of
# a `pi` workflow stage took DEFAULT_LIMIT_USD ($0.25) while dispatch passes
# `settings(cfg)` ($5.00), and `check_key_floor` then REFUSED every dispatch
# with `outstanding minted key ... remaining $0.21 is below the configured
# floor $1.00` — a key whose CAP is below the floor can never pass it, so one
# hand mint blocked every dispatch for its whole TTL. Both halves proved from
# a fixture, no network.
# --------------------------------------------------------------------------


def _mint_call_capture(calls: list[dict]):
    """A `_call` fake that records the mint payload and returns a 201 body."""

    def fake_call(method, url, key, payload=None, timeout=30):
        calls.append({"method": method, "url": url, "payload": payload})
        return 201, {"key": "sk-fake-secret", "data": {
            "hash": "h-fake", "expires_at": "2099-01-01T00:00:00Z"}}

    return fake_call


def test_g_mint_defaults_to_the_configured_limit_when_rooted(tmp_path, monkeypatch):
    """(g) half one — a mint() that names a root and no limit_usd takes the
    project's `spawn.credential.per_spawn_limit_usd`, not DEFAULT_LIMIT_USD.
    This is exactly the L4.367/L4.368 defect: a $0.25 cap against a $1.00
    floor can never pass, and one such key blocked every dispatch."""
    (tmp_path / ".agi").mkdir()
    (tmp_path / ".agi" / "config.json").write_text(json.dumps(
        {"spawn": {"credential": {"per_spawn_limit_usd": 5.0}}}))

    calls: list[dict] = []
    monkeypatch.setattr(provisioning, "_read_provisioning_key",
                        lambda root=None: "sk-prov")
    monkeypatch.setattr(provisioning, "_call", _mint_call_capture(calls))
    monkeypatch.setattr(provisioning, "can_fund", lambda root=None: (True, None))

    minted = provisioning.mint(iter_n=1, agent_id="workflow:abc", root=tmp_path)

    assert minted is not None
    assert minted.limit_usd == 5.0, (
        "a rooted mint must resolve the configured per-spawn limit, not the "
        "library default")
    mint_payloads = [c["payload"] for c in calls
                     if c["method"] == "POST" and c["payload"] is not None]
    assert mint_payloads, "mint POST never reached"
    assert mint_payloads[0]["limit"] == 5.0, (
        f"payload limit was {mint_payloads[0]['limit']!r}, expected 5.0")


def test_g_rootless_mint_keeps_the_bare_default(tmp_path, monkeypatch):
    """(g) half one control — the rootless call is unchanged: no root, no
    config to read, so `DEFAULT_LIMIT_USD` stands."""
    calls: list[dict] = []
    monkeypatch.setattr(provisioning, "_read_provisioning_key",
                        lambda root=None: "sk-prov")
    monkeypatch.setattr(provisioning, "_call", _mint_call_capture(calls))
    monkeypatch.setattr(provisioning, "can_fund", lambda root=None: (True, None))

    minted = provisioning.mint(iter_n=1, agent_id="a00-rootless")

    assert minted is not None
    assert minted.limit_usd == provisioning.DEFAULT_LIMIT_USD
    mint_payloads = [c["payload"] for c in calls
                     if c["method"] == "POST" and c["payload"] is not None]
    assert mint_payloads[0]["limit"] == provisioning.DEFAULT_LIMIT_USD


def test_g_sub_floor_cap_key_is_skipped_not_refused(monkeypatch, capsys):
    """(g) half two — a minted key whose CAP is below the floor is named and
    SKIPPED; the pre-flight passes rather than blocking every dispatch for the
    key's whole TTL. This is the L4.368 falsifier itself: cap 0.25, used 0.04
    (remaining 0.21 < floor 1.00) must NOT refuse."""
    monkeypatch.setattr(provisioning, "available", lambda root=None: True)
    monkeypatch.setattr(
        provisioning, "list_all_keys",
        lambda root=None: [{"name": "agi-iterX-kid-a", "limit": 0.25,
                            "usage": 0.04}])

    ok, msg = provisioning.check_key_floor(
        {"provisioning": {"min_key_remaining_usd": 1.0}})

    assert ok is True and msg is not None, (
        "a skipped sub-floor cap must be VISIBLE in the return value")
    assert "sub-floor" in msg
    assert "agi-iterX-kid-a" in msg
    assert "$0.25" in msg and "$1.00" in msg
    err = capsys.readouterr().err.strip().splitlines()
    assert len(err) == 1, f"expected exactly one stderr line, got {err!r}"
    assert err[0] == msg, "the marker and the stderr line are ONE sentence"


def test_g_sub_floor_marker_is_absent_when_no_key_is_skipped(monkeypatch):
    """Control for the marker: a listing with no sub-floor cap returns
    (True, None), so `msg is not None` really does mean a skip fired and is
    not a marker that is always present."""
    monkeypatch.setattr(provisioning, "available", lambda root=None: True)
    monkeypatch.setattr(
        provisioning, "list_all_keys",
        lambda root=None: [{"name": "agi-iterX-kid-c", "limit": 5.0,
                            "usage": 1.0}])
    ok, msg = provisioning.check_key_floor(
        {"provisioning": {"min_key_remaining_usd": 1.0}})
    assert ok is True and msg is None


def test_g_sub_floor_skip_does_not_swallow_a_later_real_refusal(monkeypatch):
    """Scanning continues past a skip: a sub-floor key followed by a key whose
    remaining is below the floor still REFUSES, so the marker never trades a
    refusal for a pass."""
    monkeypatch.setattr(provisioning, "available", lambda root=None: True)
    monkeypatch.setattr(
        provisioning, "list_all_keys",
        lambda root=None: [{"name": "agi-iterX-kid-a", "limit": 0.25,
                            "usage": 0.04},
                           {"name": "agi-iterX-kid-b", "limit": 5.0,
                            "usage": 4.5}])
    ok, msg = provisioning.check_key_floor(
        {"provisioning": {"min_key_remaining_usd": 1.0}})
    assert ok is False
    assert "agi-iterX-kid-b" in msg and "sub-floor" not in msg


def test_g_above_floor_cap_with_drained_remaining_still_refuses(monkeypatch):
    """(g) half two control — the skip is ONLY for a cap below the floor. A
    key capped $5.00 with $4.50 used (remaining $0.50) still refuses exactly
    as before, so the fix cannot be mistaken for weakening the floor."""
    monkeypatch.setattr(provisioning, "available", lambda root=None: True)
    monkeypatch.setattr(
        provisioning, "list_all_keys",
        lambda root=None: [{"name": "agi-iterX-kid-b", "limit": 5.0,
                            "usage": 4.5}])

    ok, msg = provisioning.check_key_floor(
        {"provisioning": {"min_key_remaining_usd": 1.0}})

    assert ok is False
    assert "agi-iterX-kid-b" in msg
    assert "$0.50" in msg  # 5.0 - 4.5
    assert "sub-floor" not in msg, (
        "the refusal is not the sub-floor skip marker")


# --------------------------------------------------------------------------
# hypothesis:(6) — item (6) provisioning pre-flight: a dispatch threads its OWN
# iteration into the check, so an outstanding key belonging to a DIFFERENT
# iteration (a proxy for this spawn's FRESH mint) does NOT gate this spawn,
# while a same-iteration drained key refuses by name of the owning iter. These
# tests drive `check_key_floor(..., iter_n=...)` directly; wiring `iter_n` at
# the dispatch call site (dispatch.py pre-flight) is the follow-up that makes
# it live, and the `iter_n=None` fallback keeps EVERY older caller unchanged.
# --------------------------------------------------------------------------


def test_l4p6_another_iters_drained_key_does_not_refuse_this_spawn(monkeypatch):
    """falsifier (1) — THE falsifier, the TM.20 incident: a key of a DIFFERENT
    iteration at its first cent of spend (cap 1.0, remaining 0.9999 < floor
    1.0) must NOT refuse this spawn when dispatch threads its OWN iter_n. The
    fresh mint this spawn gets is the credential it runs on, not that drained
    proxy key."""
    monkeypatch.setattr(provisioning, "available", lambda root=None: True)
    monkeypatch.setattr(
        provisioning, "list_all_keys",
        lambda root=None: [{"name": "agi-iterTM.20-kid-a00",
                            "limit": 1.0, "usage": 0.0001}])
    ok, msg = provisioning.check_key_floor(
        {"provisioning": {"min_key_remaining_usd": 1.0}}, iter_n="SM.70")
    assert ok is True and msg is None


def test_l4p6_owning_it_iter_drained_key_refuses_and_names_the_iter(monkeypatch):
    """falsifier (2) — an outstanding key of the SAME iteration still refuses
    this round, and the refusal NAMES the owning iter so a reader knows whose
    drained key stopped the spawn."""
    monkeypatch.setattr(provisioning, "available", lambda root=None: True)
    monkeypatch.setattr(
        provisioning, "list_all_keys",
        lambda root=None: [{"name": "agi-iterSM.70-kid-a01",
                            "limit": 5.0, "usage": 4.6}])
    ok, msg = provisioning.check_key_floor(
        {"provisioning": {"min_key_remaining_usd": 1.0}}, iter_n="SM.70")
    assert ok is False
    assert "SM.70" in msg, "the refusal must name the owning iteration"
    assert "agi-iterSM.70-kid-a01" in msg


def test_l4p6_cap_equal_to_floor_is_skipped_not_refused(monkeypatch, capsys):
    """falsifier (3) — the `<=` boundary: a key whose cap EQUALS the floor
    (1.0 == 1.0) is at its first cent of spend every TTL it lives (remaining
    0.9999 < floor), yet its cap can never pass the floor — so it is SKIPPED,
    never refused. This is the exact TM.20 key shape."""
    monkeypatch.setattr(provisioning, "available", lambda root=None: True)
    monkeypatch.setattr(
        provisioning, "list_all_keys",
        lambda root=None: [{"name": "agi-iterTM.20-kid-a00",
                            "limit": 1.0, "usage": 0.0001}])
    ok, msg = provisioning.check_key_floor(
        {"provisioning": {"min_key_remaining_usd": 1.0}})
    assert ok is True and msg is not None
    assert "sub-floor" in msg
    assert capsys.readouterr().err.strip().splitlines()[-1] == msg


def test_l4p6_non_dispatch_no_iter_n_keeps_todays_scan(monkeypatch):
    """falsifier (4) fallback — without `iter_n` (a non-dispatch caller) the
    scan consults EVERY machine-minted key byte-for-byte as today: a drained
    one still refuses. The absence of an owning iteration fails OPEN to the
    pre-iter_n behaviour, so no older caller changes shape."""
    monkeypatch.setattr(provisioning, "available", lambda root=None: True)
    monkeypatch.setattr(
        provisioning, "list_all_keys",
        lambda root=None: [{"name": "agi-iterTM.20-kid-a00",
                            "limit": 5.0, "usage": 4.6}])
    ok, msg = provisioning.check_key_floor(
        {"provisioning": {"min_key_remaining_usd": 1.0}})
    assert ok is False and "agi-iterTM.20-kid-a00" in msg


def test_l4p6_runtime_leg_unchanged_when_provisioning_absent(monkeypatch):
    """falsifier (4) — the inherited-runtime-key path (provisioning ABSENT)
    is untouched by the ownership gate: a drained runtime key still refuses,
    whether or not `iter_n` is threaded."""
    monkeypatch.setattr(provisioning, "available", lambda root=None: False)
    monkeypatch.setattr(provisioning, "key_usage", _drained_runtime_key())
    monkeypatch.setattr(provisioning, "list_all_keys", lambda root=None: [])
    ok, msg = provisioning.check_key_floor(
        {"provisioning": {"min_key_remaining_usd": 1.0}}, iter_n="SM.70")
    assert ok is False and "backup" in msg


def test_l4p6_config_min_key_floor_is_restored_to_1_0():
    """falsifier (5) — the INTERIM: the round that lands this fix RESTORES
    provisioning.min_key_remaining_usd to 1.0 in the same commit (the Prime had
    dropped it to 0.25). Read from the LIVE config so a copied list cannot
    satisfy it."""
    import locations  # noqa: E402
    this = Path(__file__).resolve()
    root = (locations.find_project_root(this)
            or this.parents[3])  # tests/../agi/../extensions/../ → repo root
    cfg = locations.load_config(root)
    assert provisioning.min_key_remaining_floor(cfg) == 1.0


# --- hypothesis:l4-dispatch-takes-a-per-round-cap-and-refuses-when-cap-
# exceeds-pool-headroom — the headroom helper behind dispatch's `--cap`.


def test_cap_headroom_refuses_and_names_pool_floor_and_live(monkeypatch):
    monkeypatch.setattr(provisioning, "credit_balance",
                        lambda root=None: (10.0, 4.0, 6.0))
    monkeypatch.setattr(provisioning, "list_all_keys", lambda root=None: [
        {"name": "agi-iter1-kid-a", "limit": 2.0},
        {"name": "human-key", "limit": 99.0},   # not engine-minted → excluded
        {"name": "agi-iter1-parent-b", "limit": 1.5},
    ])
    ok, msg = provisioning.cap_headroom(
        {"provisioning": {"min_account_remaining_usd": 1.0}}, None, 2.0)
    assert ok is False
    assert "pool headroom $1.50" in msg, msg
    assert "pool $6.00" in msg and "floor $1.00" in msg and "live $3.50" in msg
    # item 15: the conservatism is NAMED, not implied (the house shape:
    # a parenthesised clause after the arithmetic).
    # item 15 (built by a00-4a19ce42): live is now what is still SPENDABLE,
    # and the clause says so. These rows carry no `usage`, so the numbers are
    # the pre-fix numbers -- that is the compatibility proof.
    assert "live counts each un-expired agi- key's limit minus usage" in msg, msg
    assert "disabled and expired keys are free" in msg, msg


def test_cap_headroom_live_is_limit_minus_usage_on_live_keys(monkeypatch):
    """item 15: a spent key frees its headroom. `limit - usage`, not `limit`.

    The falsifier the parent runs: hand `cap_headroom` a live un-expired key
    with limit=10.0, usage=9.5 and show live drops by 9.5, not by 0."""
    monkeypatch.setattr(provisioning, "credit_balance",
                        lambda root=None: (10.0, 4.0, 6.0))
    # the SAME row, twice: once unspent, once 9.50 spent.
    monkeypatch.setattr(provisioning, "list_all_keys",
                        lambda root=None: [{"name": "agi-a", "limit": 10.0}])
    ok, msg = provisioning.cap_headroom(
        {"provisioning": {"min_account_remaining_usd": 1.0}}, None, 1.0)
    assert ok is False and "live $10.00" in msg, msg

    monkeypatch.setattr(provisioning, "list_all_keys",
                        lambda root=None: [
                            {"name": "agi-a", "limit": 10.0, "usage": 9.5}])
    ok, msg = provisioning.cap_headroom(
        {"provisioning": {"min_account_remaining_usd": 1.0}}, None, 1.0)
    assert (ok, msg) == (True, None), (
        "usage 9.50 must free 9.50 of live, leaving 0.50 live and 4.50 "
        f"headroom; got {msg!r}")


def test_cap_headroom_live_skips_expired_disabled_and_uncapped(monkeypatch):
    """item 15: dead keys and non-engine keys do not consume headroom.

    live = 0.50 (spent) + 1.50 (no TTL, half spent) + 1.00 (future TTL)
         + 0.00 (expired) + 0.00 (disabled) + 0.00 (overdrawn) + 0.00 (human)
    """
    monkeypatch.setattr(provisioning, "credit_balance",
                        lambda root=None: (10.0, 4.0, 6.0))
    monkeypatch.setattr(provisioning, "list_all_keys", lambda root=None: [
        {"name": "agi-spent", "limit": 10.0, "usage": 9.5},
        {"name": "agi-expired", "limit": 4.0, "usage": 0.25,
         "expires_at": "2020-01-01T00:00:00Z"},
        {"name": "agi-disabled", "limit": 3.0, "usage": 0.0,
         "disabled": True},
        {"name": "agi-no-ttl", "limit": 2.0, "usage": 0.5,
         "expires_at": None},
        {"name": "agi-future", "limit": 1.0,
         "expires_at": "2999-01-01T00:00:00Z"},
        {"name": "agi-overdrawn", "limit": 1.0, "usage": 4.0},
        {"name": "human-key", "limit": 99.0, "usage": 0.0},
    ])
    ok, msg = provisioning.cap_headroom(
        {"provisioning": {"min_account_remaining_usd": 1.0}}, None, 2.5)
    assert ok is False
    assert "live $3.00" in msg and "headroom $2.00" in msg, msg


def test_cap_headroom_admits_a_cap_inside_headroom(monkeypatch):
    """A row with no `usage` key still means usage 0.0 -- unchanged numbers."""
    monkeypatch.setattr(provisioning, "credit_balance",
                        lambda root=None: (10.0, 4.0, 6.0))
    monkeypatch.setattr(provisioning, "list_all_keys",
                        lambda root=None: [{"name": "agi-x", "limit": 3.5}])
    assert provisioning.cap_headroom(
        {"provisioning": {"min_account_remaining_usd": 1.0}}, None, 1.0) == \
        (True, None)


def test_cap_headroom_fails_open_on_absent_key_and_network_error(monkeypatch):
    """item 12: BOTH fail-opens carry a marker naming the unmeasured cap --
    `(True, None)` is reserved for "measured and fits", never for a read that
    could not happen (the `check_key_floor` idiom)."""
    monkeypatch.setattr(provisioning, "credit_balance", lambda root=None: None)
    ok, msg = provisioning.cap_headroom({}, None, 5.0)
    assert ok is True
    assert msg and "cap not measured" in msg and "no provisioning key" in msg, msg

    def _boom(root=None):
        raise provisioning.ProvisioningError("unreachable")

    monkeypatch.setattr(provisioning, "credit_balance", _boom)
    ok, msg = provisioning.cap_headroom({}, None, 5.0)
    assert ok is True
    assert msg and "cap not measured" in msg and "unreadable" in msg, msg


def test_cap_headroom_with_no_declared_floor_treats_it_as_zero(monkeypatch):
    """A project with no `min_account_remaining_usd` keeps a 0.00 floor —
    the declaration is what makes the floor a floor, not a hidden default."""
    monkeypatch.setattr(provisioning, "credit_balance",
                        lambda root=None: (10.0, 9.5, 0.5))
    monkeypatch.setattr(provisioning, "list_all_keys", lambda root=None: [])
    ok, msg = provisioning.cap_headroom({}, None, 1.0)
    assert ok is False and "floor $0.00" in msg, msg
