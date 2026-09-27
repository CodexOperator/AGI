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


# --- hypothesis:a-zero-usd-lane-prints-the-cap-it-mints --------------------
# The banner resolved one cap and the mint forced another (0.01), so every
# zero-USD key on DH.533-536 was capped BELOW what the round was told. Driven
# through dispatch.main() with the network stubbed; the graph skeleton is
# test_dispatch's (its own openrouter kid project), nothing here mints for real.

sys.path.insert(0, str(Path(__file__).resolve().parent))
from test_dispatch import _cap_project, dispatch, BIN  # noqa: E402


class _StubProc:
    pid = 7777
    args = ["stub"]

    def poll(self):
        return None

    def wait(self, timeout=None):
        return 0

    def kill(self):
        pass

    def communicate(self, *a, **k):
        return ("ctx\n", "")

    terminate = send_signal = kill

    def __enter__(self):
        return self

    def __exit__(self, *a):
        return False


class _Minted:
    secret, key_hash, name, expires_at = "sk-x", "h", "n", "Z"
    limit_usd = 0.01


def _zero_usd_dispatch(tmp_path, monkeypatch, *extra, rtk=(True, None),
                       key_floor=(False, "drained key below floor"),
                       balance=None, keys=(), real_rtk=False):
    """Run one zero-USD kid round with provisioning + Popen stubbed. The
    key floor is REFUSING by default: a lane that skips it must still spawn,
    a lane that runs it must not. `balance`/`keys` put the lane on the
    MEASURED `cap_headroom` path (a readable credit_balance + key listing)
    instead of its fail-open one; `real_rtk` keeps the REAL
    `check_runtime_key_usable` with provisioning ABSENT, so the pre-flight
    under test is the function, not a stub."""
    import sys as _sys
    project = _cap_project(tmp_path)
    cfgp = project / ".agi" / "config.json"
    cfg = json.loads(cfgp.read_text())
    cfg["harnesses"]["pi"]["zero_usd"] = True
    cfg["provisioning"]["zero_usd_key_limit_usd"] = 0.01
    cfgp.write_text(json.dumps(cfg))
    prov, calls = dispatch.provisioning, []
    monkeypatch.setattr(prov, "available", lambda root=None: not real_rtk)
    monkeypatch.setattr(prov, "mint",
                        lambda **kw: (calls.append(kw), _Minted())[1])
    if real_rtk:  # the REAL pre-flight: absent provisioning, a 401 runtime key
        monkeypatch.setattr(prov.envfile, "_verify_provider_key",
                            lambda key: ("dead", "HTTP 401 unauthorized"))
        monkeypatch.setenv(prov.RUNTIME_KEY_VAR, "sk-or-v1-" + "0" * 40)
    else:
        monkeypatch.setattr(prov, "check_runtime_key_usable",
                            lambda cfg, root=None: rtk)
    monkeypatch.setattr(prov, "check_key_floor",
                        lambda cfg, root=None, iter_n=None: key_floor)
    monkeypatch.setattr(prov, "check_account_floor",
                        lambda cfg, root=None: (False, "account drained"))
    monkeypatch.setattr(prov, "credit_balance", lambda root=None: balance)
    monkeypatch.setattr(prov, "list_all_keys", lambda root=None: list(keys))
    monkeypatch.setattr(dispatch.subprocess, "Popen", lambda *a, **k: _StubProc())
    monkeypatch.setattr(dispatch, "_GRACE_SLEEP", lambda s: None)
    for k in ("AGI_TREE_PROJECT_ROOT", "AGI_PROJECT_ROOT", "AGI_AGENT_ID",
              "AGI_ACTOR", "AGI_HARNESS", "AGI_SEAT"):
        monkeypatch.delenv(k, raising=False)
    monkeypatch.setattr(_sys, "argv", [
        str(BIN / "dispatch.py"), str(project), "1", "--level", "small",
        "--harness", "pi", "--tier", "kid", "--target", "hypothesis:x",
        *extra])
    return dispatch.main(), calls


def test_zero_usd_banner_prints_the_cap_the_mint_forces(tmp_path, monkeypatch,
                                                        capsys):
    """The standing limit is 1.5 and `--cap 2` says 2.0; the minted key is
    capped at the cell (0.01). The banner must name 0.01 -- the cap the key
    carries -- not the number the resolution happened to land on."""
    code, mints = _zero_usd_dispatch(tmp_path, monkeypatch, "--cap", "2.00")
    out = capsys.readouterr().out
    assert code == 0
    assert "limit=$0.01" in out, out
    assert [m["limit_usd"] for m in mints] == [0.01], mints


def test_zero_usd_lane_runs_the_runtime_key_gate_and_the_cap_guard(
        tmp_path, monkeypatch, capsys):
    """The two gates a zero-USD lane must NOT skip: the runtime-key
    pre-flight (a 401 refuses before a slot is taken) and the `--cap` guard
    (a non-positive cap never reaches headroom). FALSIFIERS: `--cap 0` is
    accepted, or a dead runtime key spawns anyway."""
    code, mints = _zero_usd_dispatch(tmp_path, monkeypatch, "--cap", "0")
    err = capsys.readouterr().err
    assert code == 1 and mints == [], (code, mints, err)
    assert "ERR: --cap must be > 0, got 0" in err, err
    code2, mints2 = _zero_usd_dispatch(tmp_path / "dead", monkeypatch,
                                       rtk=(False, "runtime key rejected: 401"))
    err2 = capsys.readouterr().err
    assert code2 == 1 and mints2 == [], (code2, mints2, err2)
    assert "runtime key rejected: 401" in err2, err2


def test_zero_usd_lane_skips_the_two_dollar_floors(tmp_path, monkeypatch):
    """The refusing key floor and the refusing account floor (both stubbed
    above) must not stop a zero-USD lane: it minted, and the round spawned."""
    code, mints = _zero_usd_dispatch(tmp_path, monkeypatch, "--cap", "2.00")
    assert code == 0
    assert len(mints) == 1, mints
    # discriminating vs the pre-image (it minted the flag's 2.00, not 0.01)
    assert mints[0]["limit_usd"] == 0.01, mints


def test_zero_usd_cap_guard_measures_the_cap_the_lane_can_spend(
        tmp_path, monkeypatch, capsys):
    """A READABLE balance puts this lane on the MEASURED `cap_headroom` path
    (the helper's fail-open `credit_balance -> None` covered no such case, so
    the near-miss survived). Pool $0.606, account floor $1.00, `--cap 1.00`:
    the floor alone makes that cap unfit, yet the key this lane mints is hard
    capped at $0.01, which fits. The guard must price what is MINTED, and must
    not charge a lane the account floor it is exempt from at check_account_floor.
    MEASURED pre-fix: `ERR: round cap $1.00 exceeds pool headroom $-0.39
    (pool $0.61 - floor $1.00 - live $0.00)`, exit 1, no mint."""
    code, mints = _zero_usd_dispatch(tmp_path, monkeypatch, "--cap", "1.00",
                                    balance=(10.0, 9.394, 0.606))
    err = capsys.readouterr().err
    assert code == 0, err
    assert [m["limit_usd"] for m in mints] == [0.01], mints


def test_zero_usd_cap_guard_runs_and_names_a_live_sibling_key(
        tmp_path, monkeypatch, capsys):
    """THE VACUITY FALSIFIER, now pinned. Every other test here stays green
    if `cap_headroom` is never CALLED on a zero-USD lane (only `code == 0`
    and `limit_usd == 0.01` hold, and `mint` forces the cap on its own).
    GATE PROBE: pool $0.606, a live `agi-` sibling at limit 5.0 / usage 4.0
    (spendable $1.00), floor EXEMPT, `--cap 1.00` — the guard must RUN,
    refuse on the live headroom, and NAME it. FALSIFIER: exit 0, a mint, or
    an ERR without the live term (i.e. the guard de-indented into the
    `zero_usd` skip at dispatch.py:2372)."""
    sibling = {"name": "agi-iter9-kid-a", "limit": 5.0, "usage": 4.0,
               "disabled": False, "expires_at": "2999-01-01T00:00:00Z"}
    code, mints = _zero_usd_dispatch(tmp_path, monkeypatch, "--cap", "1.00",
                                     balance=(10.0, 9.394, 0.606),
                                     keys=[sibling])
    err = capsys.readouterr().err
    assert code == 1 and mints == [], (code, mints, err)
    assert "pool headroom $-0.39" in err, err
    assert "live $1.00" in err, err
    # ITEM 4: the exempt floor is MARKED, so this refusal cannot be read as a
    # project that never declared one (paid path unchanged: see probeB).
    assert "floor $0.00 (exempt)" in err, err


def test_zero_usd_lane_refuses_a_dead_runtime_key_with_provisioning_absent(
        tmp_path, monkeypatch, capsys):
    """Item 5: the REAL `check_runtime_key_usable` (provisioning ABSENT, a 401
    runtime key), not a stub that merely proves the call ran. FALSIFIER: the
    pre-flight passes, or a key is minted anyway."""
    code, mints = _zero_usd_dispatch(tmp_path, monkeypatch, real_rtk=True)
    err = capsys.readouterr().err
    assert code == 1 and mints == [], (code, mints, err)
    assert "is present but NOT USABLE" in err, err
