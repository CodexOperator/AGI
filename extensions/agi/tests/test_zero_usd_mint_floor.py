"""belam 09-27 13:1xZ (owner: account drained, 0.606 USD): a ZERO-USD lane mints
below the paid floor with a hard key cap; a paid lane keeps the floor, read
from a cell; nothing mints past zero. No network: credit_balance and the
create call are stubbed."""
import json
import sys
from pathlib import Path

import pytest

sys.path.insert(0, str(Path(__file__).resolve().parents[1] / "bin"))
import provisioning  # noqa: E402


def _project(tmp_path, prov):
    agi = tmp_path / ".agi"
    agi.mkdir()
    (agi / "config.json").write_text(json.dumps({"provisioning": prov}))
    return tmp_path


@pytest.fixture
def drained(monkeypatch):
    monkeypatch.setattr(provisioning, "credit_balance",
                        lambda root=None: (10.0, 9.394, 0.606))


def test_paid_lane_refused_below_the_cell_floor(tmp_path, drained):
    root = _project(tmp_path, {"min_mint_remaining_usd": 1.0})
    ok, why = provisioning.can_fund(root)
    assert not ok and "min_mint_remaining_usd" in why


def test_paid_floor_is_the_cell_not_the_literal(tmp_path, drained):
    root = _project(tmp_path, {"min_mint_remaining_usd": 0.5})
    assert provisioning.can_fund(root) == (True, None)


def test_zero_usd_lane_funds_below_the_paid_floor(tmp_path, drained):
    root = _project(tmp_path, {"min_mint_remaining_usd": 1.0,
                               "zero_usd_key_limit_usd": 0.01})
    assert provisioning.can_fund(root, zero_usd=True) == (True, None)


def test_zero_usd_lane_never_mints_past_zero(tmp_path, monkeypatch):
    monkeypatch.setattr(provisioning, "credit_balance",
                        lambda root=None: (10.0, 9.995, 0.005))
    root = _project(tmp_path, {"zero_usd_key_limit_usd": 0.01})
    ok, why = provisioning.can_fund(root, zero_usd=True)
    assert not ok and "zero-USD key cap" in why


def test_zero_usd_mint_forces_the_hard_key_cap(tmp_path, drained, monkeypatch):
    root = _project(tmp_path, {"zero_usd_key_limit_usd": 0.01})
    sent = {}
    monkeypatch.setattr(provisioning, "_read_provisioning_key", lambda r=None: "pk")
    monkeypatch.setattr(provisioning, "_mutation_guard", lambda op: None)

    def fake_call(method, url, key, payload=None, *a, **k):
        sent.update(payload or {})
        raise provisioning.ProvisioningError("stop after the payload is built")
    monkeypatch.setattr(provisioning, "_call", fake_call)
    with pytest.raises(provisioning.ProvisioningError):
        provisioning.mint(iter_n=1, agent_id="a00-test", limit_usd=1.0,
                          root=root, zero_usd=True)
    assert sent.get("limit") == 0.01
