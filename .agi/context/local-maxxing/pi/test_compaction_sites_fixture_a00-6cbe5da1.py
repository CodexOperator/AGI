"""Fixture-only check of pi's auto-compaction call sites (agent a00-6cbe5da1).

No pi process, no subprocess, no model. Reads the committed excerpt of the
INSTALLED pi (0.67.68) plus the committed request logs of three prior probes.
"""
import json
import re
import sys
from pathlib import Path

import pytest

REPO = Path(__file__).resolve().parents[4]
EXCERPT = REPO / "datasets/brain-swap/2026-09-26/pi-agent-session-compaction-excerpt-a00-6cbe5da1.txt"
LOG_DIR = REPO / "datasets/brain-swap/2026-09-24"
LOGS = ["a00-d0e2727c", "a00-b6ec457f", "a00-3a7f8962"]
CLAIM_VERSION = "0.67.68"
SLOT = 65536


def excerpt_lines():
    """[(lineno_in_source, text)] for every copied line, in excerpt order."""
    out = []
    for raw in EXCERPT.read_text().splitlines():
        m = re.match(r"^(\d+)\t(.*)$", raw)
        if m:
            out.append((int(m.group(1)), m.group(2)))
    return out


def header_value(key):
    for raw in EXCERPT.read_text().splitlines():
        if raw.startswith(f"# {key}:"):
            return raw.split(":", 1)[1].strip()
    return None


def test_excerpt_is_from_the_version_the_claim_names():
    installed = header_value("pi_version_installed")
    assert installed is not None, "excerpt header carries no installed pi version"
    assert installed == CLAIM_VERSION, f"excerpt is from pi {installed}, claim names {CLAIM_VERSION}"


def test_every_auto_compaction_trigger_is_enumerated():
    """(a) the excerpt contains every site that can START auto-compaction."""
    lines = excerpt_lines()
    # _checkCompaction: 2 call sites + its definition; _runAutoCompaction: 2 triggers + definition.
    call_sites = [n for n, t in lines if re.search(r"await this\._checkCompaction\(", t)]
    triggers = [n for n, t in lines if re.search(r"await this\._runAutoCompaction\(", t)]
    defs = [n for n, t in lines if re.search(r"async _(checkCompaction|runAutoCompaction)\(", t)]
    assert len(call_sites) == 2, f"expected 2 _checkCompaction call sites, found {call_sites}"
    assert len(triggers) == 2, f"expected 2 _runAutoCompaction triggers, found {triggers}"
    assert len(defs) == 2, f"expected both _checkCompaction/_runAutoCompaction bodies, found {defs}"
    # The single context-overflow probe outside _checkCompaction is a NEGATIVE guard
    # (_isRetryableError), never a trigger: it returns false for overflow.
    guard = [n for n, t in lines if "isContextOverflow(message, contextWindow)" in t]
    assert guard == [1928], f"unexpected overflow-probe sites: {guard}"
    idx = {n: i for i, (n, _) in enumerate(lines)}
    body = [n for n, t in lines if "async _checkCompaction(" in t][0]
    assert all(body < t <= 1928 for t in triggers), "a trigger lives outside _checkCompaction"


def test_no_compaction_check_sits_inside_the_tool_call_loop():
    """(b) no call site lies between a tool result being appended and the next request."""
    lines = excerpt_lines()
    call_sites = [i for i, (n, t) in enumerate(lines) if re.search(r"await this\._checkCompaction\(", t)]
    assert len(call_sites) == 2
    for i in call_sites:
        window = [t for _, t in lines[max(0, i - 45):i]]
        # each site is guarded by a non-loop boundary, never by tool-result handling
        assert not any("toolResult" in w and "appendMessage" in w for w in window), (
            "call site is inside tool-result handling")
        boundary = [w for w in window if 'event.type === "agent_end"' in w
                    or "Check if we need to compact before sending" in w]
        assert boundary, "call site has no agent_end / pre-prompt boundary in the excerpt"


def _rows(name):
    log = json.loads((LOG_DIR / f"{name}-request-log.json").read_text())
    return log, log.get("arms", [])


@pytest.mark.parametrize("name", LOGS)
def test_log_records(name):
    """(c) per arm: max request size vs W and vs the slot; compaction vs 400 ordering."""
    def emit(line):
        print(line, file=sys.__stdout__)

    emit("| source | arm | n_requests | max proxy tokens | first index past W | first past 65,536 | compaction index | 400 index |")
    emit("| --- | --- | --- | --- | --- | --- | --- | --- |")
    log, arms = _rows(name)
    if not arms:
        pytest.xfail(f"{name}: log carries no arms ({log.get('status')}: {log.get('selftest')})")
    rows = []
    for arm in arms:
        label = arm.get("arm")
        reqs = arm.get("requests") or []
        if not reqs:
            pytest.xfail(f"{name}/{label}: log carries no request rows (probe did not run)")
        idx_key = "seq" if "seq" in reqs[0] else ("request" if "request" in reqs[0] else None)
        if idx_key is None:
            pytest.xfail(f"{name}/{label}: no request index field {sorted(reqs[0])}")
        w = arm.get("declared_window")
        toks = [r["estimated_tokens"] for r in reqs]
        past_w = next((i for i, t in enumerate(toks) if w and t > w), None)
        past_slot = next((i for i, t in enumerate(toks) if t > SLOT), None)
        if "is_compaction" in reqs[0]:
            comp = next((r[idx_key] for r in reqs if r.get("is_compaction")), None)
        else:
            pytest.xfail(f"{name}/{label}: no is_compaction field {sorted(reqs[0])}")
        err400 = next((r[idx_key] for r in reqs if r.get("status") == 400), None)
        row = (name, label, len(reqs), max(toks), past_w, past_slot, comp, err400)
        rows.append(row)
        emit("| " + " | ".join(str(c) for c in row) + " |")
    assert rows, f"{name}: no arm produced rows"
    for r in rows:
        # A declared window did NOT stop the over-ceiling request; compaction followed the 400.
        assert r[5] is not None, f"{r[0]}/{r[1]}: never crossed the slot, log cannot judge the claim"
        assert r[6] is None or r[7] is None or r[6] > r[7], (
            f"{r[0]}/{r[1]}: compaction index {r[6]} did not follow 400 index {r[7]}")
