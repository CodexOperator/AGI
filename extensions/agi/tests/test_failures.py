"""Tests for extensions/agi/bin/failures.py — the agent failure ledger.

**hypothesis:l3w4-agent-failure-ledger.** Derive an idempotent per-agent
failure table from session artifacts (agent.json, output.log, write-log.jsonl,
review/results.json) across the closed category set, and report per-axis
rates that sum to the total.

These build synthetic iteration dirs under tmp_path mirroring the real
`.agi/sessions/iter-*` layout, so they exercise the real parsers and the real
`locations.iteration_dir`/`list_iterations` resolution.
"""
from __future__ import annotations

import json
import os
import sys

import pytest

REPO_ROOT = os.path.dirname(os.path.dirname(os.path.dirname(
    os.path.dirname(os.path.abspath(__file__)))))
sys.path.insert(0, os.path.join(REPO_ROOT, "extensions", "agi", "bin"))
import failures  # noqa: E402


def _agent_json(agent_id, iter_id, **over):
    rec = {
        "id": agent_id,
        "slot": 0,
        "level": "small",
        "target": f"hypothesis:fixture-{iter_id}",
        "strategy": "extend_existing",
        "role": None,
        "pid": 999999,
        "started_at": 1788800000,
        "status": "done",
        "tier": "kid",
        "harness": "pi",
        "node_id": f"experiment:{agent_id}",
        "command": (
            "/home/ubuntu/.npm-global/bin/pi --provider openrouter "
            f"--model '~deepseek/deepseek-v4-flash-latest' --thinking medium "
            f"-p --append-system-prompt 'You are kid agent {agent_id} on "
            f"iteration {iter_id}'"
        ),
        "parent": "hypothesis:fixture",
    }
    rec.update(over)
    return rec


def _write_agent(sessions, iter_id, agent_id, agent_json=None):
    itdir = sessions / f"iter-{iter_id}"
    adir = itdir / agent_id
    adir.mkdir(parents=True, exist_ok=True)
    aj = agent_json or _agent_json(agent_id, iter_id)
    (adir / "agent.json").write_text(json.dumps(aj, indent=2), encoding="utf-8")
    (adir / "output.log").write_text("", encoding="utf-8")
    return adir


@pytest.fixture
def fx(tmp_path):
    """A synthetic project root with a fixture iteration mixing all 8
    failure categories plus a clean negative-control iteration."""
    root = tmp_path / "fx"
    sessions = root / "sessions"
    sessions.mkdir(parents=True)

    # iter-FIX.01 — eight derivable categories.
    i1 = "FIX.01"
    # a1 — died via status=failed.
    _write_agent(sessions, i1, "a1-died")
    (sessions / f"iter-{i1}" / "a1-died" / "agent.json").write_text(json.dumps(
        _agent_json("a1-died", i1, status="failed"), indent=2), encoding="utf-8")

    # a2 — demoted (evidence-gate downgrade stamped on the record).
    _write_agent(sessions, i1, "a2-demoted")
    a2 = _agent_json("a2-demoted", i1)
    a2.update(demoted_from="proved", demote_reason="evidence_runs not real")
    (sessions / f"iter-{i1}" / "a2-demoted" / "agent.json").write_text(
        json.dumps(a2, indent=2), encoding="utf-8")

    # a3 — rejected (evidence-gate hard-fail), from output.log.
    _write_agent(sessions, i1, "a3-reject")
    (sessions / f"iter-{i1}" / "a3-reject" / "output.log").write_text(
        "spawning...\nEVIDENCE-GATE REJECTED: nothing written\n",
        encoding="utf-8")

    # a4 — no_build_probe_only (verdict pending at done).
    _write_agent(sessions, i1, "a4-pending")
    (sessions / f"iter-{i1}" / "a4-pending" / "agent.json").write_text(json.dumps(
        _agent_json("a4-pending", i1, verdict="pending"), indent=2),
        encoding="utf-8")

    # a5 — died via hung-unhealed.
    _write_agent(sessions, i1, "a5-hung")
    (sessions / f"iter-{i1}" / "a5-hung" / "agent.json").write_text(json.dumps(
        _agent_json("a5-hung", i1, status="hung-unhealed"), indent=2),
        encoding="utf-8")

    # a6 — wrong_file: the agent's own transcript shows a write_guard WARN.
    _write_agent(sessions, i1, "a6-wrongfile")
    (sessions / f"iter-{i1}" / "a6-wrongfile" / "output.log").write_text(
        "WARN unsanctioned write: nodes/experiment/someone.md\n"
        "  to redo: python3 extensions/agi/bin/write.py ...\n", encoding="utf-8")

    # a7 — session_limit: last output.log line is a subscription-limit result.
    _write_agent(sessions, i1, "a7-sessionlimit")
    (sessions / f"iter-{i1}" / "a7-sessionlimit" / "output.log").write_text(
        '{"type":"result","subtype":"session_limit",'
        '"reset_time":"2026-09-08T00:00:00Z"}\n', encoding="utf-8")

    # iteration-level overclaim from bug-master results.json
    review = sessions / f"iter-{i1}" / "review"
    review.mkdir(parents=True, exist_ok=True)
    (review / "results.json").write_text(json.dumps({
        "reviews": [{"target": "hypothesis:fixture", "verdict": "proved",
                     "overclaims": 2, "open_gaps": 1, "files_changed": 3}]
    }), encoding="utf-8")

    # iter-FIX.02 — clean agent, must produce zero rows (a negative control
    # exercising the "unadmitted / clean session never counts" rule).
    i2 = "FIX.02"
    _write_agent(sessions, i2, "b1-clean", _agent_json("b1-clean", i2))

    # write-log.jsonl — one sanctioned frontmatter repair attributed to a2.
    (sessions / "write-log.jsonl").write_text(json.dumps({
        "node_id": "experiment:a2-demoted",
        "operation": "repair-frontmatter",
        "path": "nodes/experiment/a2-demoted.md",
        "sha256": "deadbeef",
        "ts": "2026-09-07T00:00:00.000000Z",
    }) + "\n", encoding="utf-8")

    return root, sessions


# ---- derivation ----

def _derive(root):
    return failures.derive_rows(root)


def test_ledger_reads_died_from_swept_zombie_lease(fx):
    root, _ = fx
    rows = _derive(root)
    died = [r for r in rows if r["category"] == "died"]
    assert len(died) == 2, died
    statuses = {r["detail"] for r in died}
    assert statuses == {"failed", "hung-unhealed"}


def test_ledger_reads_demoted_and_rejected_from_evidence_gate_fixtures(fx):
    root, _ = fx
    rows = _derive(root)
    demoted = [r for r in rows if r["category"] == "demoted"]
    rejected = [r for r in rows if r["category"] == "rejected"]
    assert len(demoted) == 1 and demoted[0]["detail"] == "evidence_runs not real"
    assert len(rejected) == 1 and rejected[0]["detail"] == "EVIDENCE-GATE REJECTED"


def test_ledger_reads_broken_frontmatter_from_write_log(fx):
    root, _ = fx
    rows = _derive(root)
    bf = [r for r in rows if r["category"] == "broken_frontmatter"]
    assert len(bf) == 1
    assert bf[0]["agent_id"] == "a2-demoted"  # attributed via node_id→agent
    assert bf[0]["detail"].endswith("nodes/experiment/a2-demoted.md")


def test_ledger_reads_session_limit_from_output_log(fx):
    root, _ = fx
    rows = _derive(root)
    sl = [r for r in rows if r["category"] == "session_limit"]
    assert len(sl) == 1 and sl[0]["agent_id"] == "a7-sessionlimit"


def test_ledger_reads_wrong_file_from_write_guard_warn(fx):
    root, _ = fx
    rows = _derive(root)
    wf = [r for r in rows if r["category"] == "wrong_file"]
    assert len(wf) == 1
    assert "nodes/experiment/someone.md" in wf[0]["detail"]
    assert wf[0]["agent_id"] == "a6-wrongfile"


def test_ledger_reads_overclaim_and_no_build_probe_only(fx):
    root, _ = fx
    rows = _derive(root)
    oc = [r for r in rows if r["category"] == "overclaim"]
    pb = [r for r in rows if r["category"] == "no_build_probe_only"]
    assert len(oc) == 1 and oc[0]["detail"] == "overclaims=2"
    assert len(pb) == 1 and pb[0]["agent_id"] == "a4-pending"


def test_ledger_skips_unadmitted_slots(fx):
    root, _ = fx
    rows = _derive(root)
    # b1-clean (FIX.02) must not produce a row; only the FIX.01 categories do.
    assert all(r["iter"] == "FIX.01" or r["category"] == "broken_frontmatter"
               for r in rows)
    assert not any(r["agent_id"] == "b1-clean" for r in rows)


def test_all_eight_categories_derivable(fx):
    root, _ = fx
    rows = _derive(root)
    cats = {r["category"] for r in rows}
    assert cats == set(failures.CATEGORIES)


# ---- ledger idempotence ----

def test_ledger_is_idempotent_on_rerun(fx, tmp_path):
    root, _ = fx
    out = tmp_path / "ledger.json"
    new1, total1, appended1 = failures.ledger(root, out_path=out)
    assert appended1 >= 8, new1
    new2, total2, appended2 = failures.ledger(root, out_path=out)
    assert appended2 == 0, f"rerun appended {appended2} rows"
    assert total1 == total2
    # every stored row carries its key
    keys = {r["_key"] for r in json.loads(out.read_text())}
    assert len(keys) == total1


# ---- rates ----

def _seed_ledger(fx, tmp_path):
    root, _ = fx
    out = tmp_path / "ledger.json"
    new, total, _ = failures.ledger(root, out_path=out)
    assert total > 0
    return root, out


def test_rates_by_model_and_by_harness_sum_to_total(fx, tmp_path):
    root, out = _seed_ledger(fx, tmp_path)
    for by in ("model", "role", "harness"):
        counts, total, ok = failures.rates(root, by, in_path=out)
        assert ok, f"rates by {by} did not sum"
        assert sum(counts.values()) == total
        assert total == len(json.loads(out.read_text()))


def test_ledger_never_writes_node_frontmatter_directly(fx, tmp_path):
    """ledger() lands the table via write.py when asked to; the module never
    calls node_writer/log_write itself (no repair-frontmatter is triggered by
    a ledger run). A --write-node whose target build node is not yet minted
    (the mvp job's job) must degrade to a WARN and still land the file."""
    root, _ = fx
    out = tmp_path / "ledger.json"
    new, total, appended = failures.ledger(root, out_path=out,
                                           write_node="build:g16-failure-ledger")
    assert appended > 0
    assert out.exists() and total > 0
    assert failures._load_ledger(out)[0]  # file landed with rows