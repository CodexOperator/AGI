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

    def fake_call(method, url, key, payload=None, timeout=30):
        sent.append(payload or {})
        return 201, {"key": "sk-fake", "data": {
            "hash": "h-fake", "expires_at": "2099-01-01T00:00:00Z"}}

    monkeypatch.setattr(provisioning, "_read_provisioning_key",
                        lambda root=None: "sk-prov")
    monkeypatch.setattr(provisioning, "_call", fake_call)

    provisioning.mint(iter_n=1, agent_id="a00", workspace_id="ws-123")
    assert sent[-1]["workspace_id"] == "ws-123"

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
