"""goal:g1.27 / hypothesis:free-lane-mint-and-skills-startup-have-end-to-end-
tests (a) -- the zero-usd lane is proved through dispatch.main() itself.
FALSIFIERS: a drained account + a `zero_usd: true` row does NOT mint a key at
the CELL `provisioning.zero_usd_key_limit_usd`; a PAID row on the same balance
is not refused BY THE ACCOUNT FLOOR. A dispatch-path proof with every I/O
boundary faked: adapters.load, subprocess.Popen/run, _GRACE_SLEEP,
provisioning.credit_balance/available/_read_provisioning_key/_mutation_guard/
check_runtime_key_usable/check_key_floor/check_account_floor and the _call.
"""
from __future__ import annotations

import json
import sys
from pathlib import Path

BIN = Path(__file__).resolve().parent.parent / "bin"
sys.path.insert(0, str(BIN))

import dispatch  # noqa: E402
import provisioning  # noqa: E402

MODEL = "~deepseek/deepseek-v4-flash-latest"
# CAP_USD != provisioning.DEFAULT_ZERO_USD_KEY_LIMIT_USD on purpose: a literal
# 0.01 baked into the mint site then turns this suite RED.
CAP_USD = 0.03  # < REMAINING; the free lane never mints past zero
FLOOR_MINT_USD = 1.0
FLOOR_ACCOUNT_USD = 1.6
REMAINING = 0.05


def _project(tmp_path: Path, *, zero_usd: bool) -> Path:
    root = tmp_path / ("free" if zero_usd else "paid")
    graph = root / ".agi"
    (graph / "nodes" / "hypothesis").mkdir(parents=True)
    (graph / "nodes" / "hypothesis" / "x.md").write_text(
        "---\nid: hypothesis:x\ntype: hypothesis\ntestable_claim: \"x\"\n---\n")
    (graph / "config.json").write_text(json.dumps({
        "metric_primary": "outcome_coverage",
        "provisioning": {"zero_usd_key_limit_usd": CAP_USD,
                          "min_mint_remaining_usd": FLOOR_MINT_USD,
                          "min_account_remaining_usd": FLOOR_ACCOUNT_USD},
        "spawn": {"harness": "pi", "parallel": 1,
                  "credential": {"per_spawn_limit_usd": 1.0}},
        "harnesses": {"pi": {"adapter": "pi", "provider": "openrouter",
                             "zero_usd": zero_usd,
                             "models": {"kid": MODEL},
                             "allowed_models": [MODEL]}}}))
    return root


def _harness(monkeypatch, tmp_path, *, zero_usd, mints, calls):
    _Proc = type("P", (), {"pid": 4242, "poll": lambda self: None})
    _Run = type("R", (), {"returncode": 0, "stdout": "ctx\n", "stderr": ""})

    class _Adapter:
        def build_command(self, **kw):
            return [sys.executable, "-c", "pass"]

        def child_env(self, **kw):
            return {}

        def needs_credential(self, *a, **k):
            return True

        def is_alive(self, pid):
            return True
    monkeypatch.setattr(dispatch.adapters, "load", lambda name: _Adapter())
    monkeypatch.setattr(dispatch.subprocess, "Popen", lambda *a, **k: _Proc())
    monkeypatch.setattr(dispatch.subprocess, "run", lambda *a, **k: _Run())
    monkeypatch.setattr(dispatch, "_GRACE_SLEEP", lambda s: None)
    monkeypatch.delenv("AGI_AGENT_ID", raising=False)
    monkeypatch.delenv("AGI_SEAT", raising=False)

    # the account IS drained: below every PAID floor above, above the free cap.
    monkeypatch.setattr(dispatch.provisioning, "credit_balance",
                        lambda root=None: (10.0, 10.0 - REMAINING, REMAINING))
    monkeypatch.setattr(dispatch.provisioning, "available", lambda root=None: True)
    monkeypatch.setattr(dispatch.provisioning, "_read_provisioning_key",
                        lambda r=None: "pk-test")
    monkeypatch.setattr(dispatch.provisioning, "_mutation_guard", lambda op: None)
    monkeypatch.setattr(dispatch.provisioning, "check_runtime_key_usable",
                        lambda cfg, r=None: calls.append("runtime_key") or (True, None))
    monkeypatch.setattr(dispatch.provisioning, "check_key_floor",
                        lambda cfg, r=None, iter_n=None: calls.append("key_floor") or (True, None))
    # the REAL account floor, only its call recorded -- so the refusal reason
    # the paid test asserts is the one the CELL floor produces.
    _acc = dispatch.provisioning.check_account_floor
    monkeypatch.setattr(dispatch.provisioning, "check_account_floor",
                        lambda cfg, r=None: (calls.append("account_floor") or _acc(cfg, r)))

    def _call(method, url, key, payload=None, *a, **k):
        mints.append(payload or {})
        return 201, {"key": "sk-test", "data": {"hash": "h1",
                                                "expires_at": "2027-01-01T00:00:00Z"}}

    monkeypatch.setattr(dispatch.provisioning, "_call", _call)
    return _project(tmp_path, zero_usd=zero_usd)


def _dispatch(monkeypatch, root, harness="pi"):
    monkeypatch.setattr(sys, "argv",
                        [str(BIN / "dispatch.py"), str(root), "1", "--tier", "kid",
                         "--target", "hypothesis:x", "--harness", harness, "--detach"])
    return dispatch.main()


def test_free_lane_mints_at_the_zero_usd_cell_cap_on_a_drained_account(
        tmp_path, monkeypatch):
    """(a) first half: a zero_usd harness skips the two DOLLAR floors (keeping
    the runtime-key pre-flight) and mints a key hard-capped at the CELL cap,
    never a literal."""
    mints, calls = [], []
    root = _harness(monkeypatch, tmp_path, zero_usd=True, mints=mints, calls=calls)
    cap = json.loads((root / ".agi" / "config.json").read_text()
                     )["provisioning"]["zero_usd_key_limit_usd"]
    assert cap != provisioning.DEFAULT_ZERO_USD_KEY_LIMIT_USD, (
        "fixture cap == DEFAULT: a literal at the mint site would pass")
    assert _dispatch(monkeypatch, root) == 0
    # the split is a DE-INDENT, not a free pass: the two DOLLAR floors are
    # absent, the provisioning-ABSENT runtime-key gate is PRESENT for every
    # openrouter lane (dispatch.py:2364 runs it ABOVE the zero_usd split at
    # :2372). Pinned here so a future de-indent that drops the gate for
    # zero-USD lanes is red.
    assert not [c for c in calls if c in ("key_floor", "account_floor")], \
        f"a zero_usd lane must SKIP both dollar floors; it ran {calls}"
    assert "runtime_key" in calls, (
        f"a zero_usd lane keeps the runtime-key pre-flight; it ran {calls}")
    assert len(mints) == 1, mints
    assert mints[0]["limit"] == cap, (
        f"free lane minted at {mints[0]['limit']}, not the cell cap {cap}")


def test_paid_lane_is_refused_by_the_account_floor_on_the_same_balance(
        tmp_path, monkeypatch, capsys):
    """(a) second half: the SAME balance on a row without `zero_usd` is refused
    BECAUSE the account floor read its cell -- the reason, not just rc == 1."""
    mints, calls = [], []
    root = _harness(monkeypatch, tmp_path, zero_usd=False, mints=mints, calls=calls)
    assert _dispatch(monkeypatch, root) == 1, "a paid lane on a drained account must refuse"
    err = capsys.readouterr().err
    assert f"${REMAINING:.2f}" in err and f"${FLOOR_ACCOUNT_USD:.2f}" in err, \
        f"the refusal must name the account floor the cell declares: {err[:300]}"
    assert set(calls) == {"runtime_key", "key_floor", "account_floor"}, \
        f"a paid lane must keep every floor; it ran {calls}"
    assert mints == [], "a refused paid dispatch minted a key anyway"


def test_a_dead_runtime_key_refuses_even_a_zero_usd_lane(tmp_path, monkeypatch):
    """The converse leg of the split: skipping the dollar floors is not
    skipping the gates. A zero_usd lane whose runtime key is unusable is
    refused BEFORE any budget slot, and mints nothing."""
    mints, calls = [], []
    root = _harness(monkeypatch, tmp_path, zero_usd=True, mints=mints, calls=calls)
    monkeypatch.setattr(dispatch.provisioning, "check_runtime_key_usable",
                        lambda cfg, r=None: (calls.append("runtime_key")
                                             or (False, "runtime key 401 expired")))
    assert _dispatch(monkeypatch, root) == 1, \
        "a dead runtime key must refuse a zero_usd lane too"
    assert mints == [], f"a refused zero_usd dispatch minted anyway: {mints}"
    assert not [c for c in calls if c in ("key_floor", "account_floor")], \
        f"the refusal must come from the runtime-key gate, not a floor; {calls}"


def test_the_paid_floor_comes_from_its_cell_not_a_literal(tmp_path, monkeypatch):
    """The PAID floors decide can_fund from their cells: lower the cell below
    the remaining balance and the SAME call now funds."""
    monkeypatch.setattr(provisioning, "credit_balance",
                        lambda root=None: (10.0, 10.0 - REMAINING, REMAINING))
    root = _project(tmp_path, zero_usd=True)
    graph = root / ".agi" / "config.json"
    assert not provisioning.can_fund(root)[0], "cell floor 1.00 > 0.05 remaining"
    cfg = json.loads(graph.read_text())
    cfg["provisioning"]["min_mint_remaining_usd"] = 0.001
    graph.write_text(json.dumps(cfg))
    assert provisioning.can_fund(root)[0] is True
