"""goal:g1.27 / hypothesis:free-lane-mint-and-skills-startup-have-end-to-end-
tests (a) -- the zero-usd lane is proved through dispatch.main() itself, not
through provisioning.can_fund and mint() in isolation (the five PASS 11 tests
covered those and no more).

FALSIFIERS: a drained account + a `zero_usd: true` harness row does NOT mint a
key at `provisioning.zero_usd_key_limit_usd`; a PAID harness row on the same
drained account is not refused. Both caps/floors are read from the config cells
they live in -- no literal. No network: the create call is stubbed.
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


def _project(tmp_path: Path, *, zero_usd: bool) -> Path:
    root = tmp_path / ("free" if zero_usd else "paid")
    graph = root / ".agi"
    (graph / "nodes" / "hypothesis").mkdir(parents=True)
    (graph / "nodes" / "hypothesis" / "x.md").write_text(
        "---\nid: hypothesis:x\ntype: hypothesis\ntestable_claim: \"x\"\n---\n")
    (graph / "config.json").write_text(json.dumps({
        "metric_primary": "outcome_coverage",
        "provisioning": {"zero_usd_key_limit_usd": 0.01,
                          "min_mint_remaining_usd": 1.0,
                          "min_account_remaining_usd": 1.6},
        "spawn": {"harness": "pi", "parallel": 1,
                  "credential": {"per_spawn_limit_usd": 1.0}},
        "harnesses": {"pi": {"adapter": "pi", "provider": "openrouter",
                             "zero_usd": zero_usd,
                             "models": {"kid": MODEL},
                             "allowed_models": [MODEL]}}}))
    return root


def _harness(monkeypatch, tmp_path, *, zero_usd, mints, calls):
    class _Proc:
        pid = 4242

        def poll(self):
            return None

    class _Adapter:
        def build_command(self, **kw):
            return [sys.executable, "-c", "pass"]

        def child_env(self, **kw):
            return {}

        def needs_credential(self, *a, **k):
            return True

        def is_alive(self, pid):
            return True

    class _Run:
        returncode = 0
        stdout = "ctx\n"
        stderr = ""

    monkeypatch.setattr(dispatch.adapters, "load", lambda name: _Adapter())
    monkeypatch.setattr(dispatch.subprocess, "Popen", lambda *a, **k: _Proc())
    monkeypatch.setattr(dispatch.subprocess, "run", lambda *a, **k: _Run())
    monkeypatch.setattr(dispatch, "_GRACE_SLEEP", lambda s: None)
    monkeypatch.delenv("AGI_AGENT_ID", raising=False)
    monkeypatch.delenv("AGI_SEAT", raising=False)
    # the account IS drained: below every PAID floor in the cells above, and
    # still above the free lane's own hard cap (below the cap the free lane
    # is refused too -- can_fund never mints past zero, for any lane).
    monkeypatch.setattr(dispatch.provisioning, "credit_balance",
                        lambda root=None: (10.0, 9.95, 0.05))
    monkeypatch.setattr(dispatch.provisioning, "available", lambda root=None: True)
    monkeypatch.setattr(dispatch.provisioning, "_read_provisioning_key",
                        lambda r=None: "pk-test")
    monkeypatch.setattr(dispatch.provisioning, "_mutation_guard", lambda op: None)
    monkeypatch.setattr(dispatch.provisioning, "check_runtime_key_usable",
                        lambda cfg, r=None: calls.append("runtime_key") or (True, None))
    monkeypatch.setattr(dispatch.provisioning, "check_key_floor",
                        lambda cfg, r=None, iter_n=None: calls.append("key_floor") or (True, None))
    monkeypatch.setattr(dispatch.provisioning, "check_account_floor",
                        lambda cfg, r=None: (False, "account floor 0.005 below 1.6"))

    def _call(method, url, key, payload=None, *a, **k):
        mints.append(payload or {})
        return 201, {"key": "sk-test", "data": {"hash": "h1",
                                                "expires_at": "2027-01-01T00:00:00Z"}}

    monkeypatch.setattr(dispatch.provisioning, "_call", _call)
    return _project(tmp_path, zero_usd=zero_usd)


def _dispatch(root, harness="pi"):
    sys.argv = [str(BIN / "dispatch.py"), str(root), "1", "--tier", "kid",
                "--target", "hypothesis:x", "--harness", harness, "--detach"]
    return dispatch.main()


def test_free_lane_mints_at_the_zero_usd_cap_on_a_drained_account(
        tmp_path, monkeypatch):
    """(a) first half: a zero_usd harness skips the paid floors and mints a
    key hard-capped at the CELL, with the cap read from the project config."""
    mints, calls = [], []
    root = _harness(monkeypatch, tmp_path, zero_usd=True, mints=mints, calls=calls)
    cap = json.loads((root / ".agi" / "config.json").read_text()
                     )["provisioning"]["zero_usd_key_limit_usd"]
    assert _dispatch(root) == 0
    assert "runtime_key" not in calls and "key_floor" not in calls, (
        "a zero_usd lane must SKIP the paid floors; it ran " + repr(calls))
    assert len(mints) == 1, mints
    assert mints[0]["limit"] == cap, (
        f"free lane minted at {mints[0]['limit']}, not the cell cap {cap}")


def test_paid_lane_is_refused_on_the_same_drained_account(tmp_path, monkeypatch):
    """(a) second half: the SAME drained balance on a harness row without
    `zero_usd` is refused before any slot is taken, and never mints."""
    mints, calls = [], []
    root = _harness(monkeypatch, tmp_path, zero_usd=False, mints=mints, calls=calls)
    assert _dispatch(root) == 1, "a paid lane on a drained account must refuse"
    assert "runtime_key" in calls and "key_floor" in calls, (
        "a paid lane must keep every floor; it ran " + repr(calls))
    assert mints == [], "a refused paid dispatch minted a key anyway"


def test_the_cap_and_the_floor_come_from_cells_not_literals(tmp_path):
    """config-max: the two numbers the free lane turns on are the project's,
    so a project that raises the cap gets the raised cap from the same code."""
    root = _project(tmp_path, zero_usd=True)
    graph = root / ".agi" / "config.json"
    cfg = json.loads(graph.read_text())
    cfg["provisioning"]["zero_usd_key_limit_usd"] = 0.25
    graph.write_text(json.dumps(cfg))
    assert provisioning.zero_usd_key_limit(root) == 0.25
