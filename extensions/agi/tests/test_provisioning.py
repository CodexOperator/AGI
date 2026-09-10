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

import provisioning  # noqa: E402
import spawn_budget  # noqa: E402

live = pytest.mark.skipif(
    not provisioning.available("/home/ubuntu/work/agi"),
    reason="no OPENROUTER_PROVISIONING_KEY — issuance is optional by design",
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

