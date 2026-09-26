"""Fixture-only check of pi's auto-compaction call sites (agent a00-6cbe5da1).

No pi process, no subprocess, no model. Reads the committed excerpt of the
INSTALLED pi (0.67.68) plus the committed request logs of three prior probes.

PASS 8 residue round a00-5728f5a0: per-ARM skip instead of a whole-test abort
(items 1/4/5), the lookback shortfall is reported (item 6), and both dataset
locations come from the config cell paths.local_maxxing.brain_swap_out_dir plus
a glob, never a date literal (items 8/10).
"""
import json
import re
import sys
from pathlib import Path

import pytest

sys.path.insert(0, str(Path(__file__).resolve().parents[1]))
import paths  # .agi/context/local-maxxing/paths.py, discovered from __file__

REPO = Path(paths.config_path()).resolve().parents[1]
# config cell (config.json paths.local_maxxing.brain_swap_out_dir) for the logs,
# and the SAME parent family for the excerpt: the date segment is a glob, so the
# excerpt and the logs can never drift apart silently behind two literals.
LOG_DIR = Path(paths.get_local("brain_swap_out_dir"))
_EXCERPT_GLOB = "pi-agent-session-compaction-excerpt-a00-6cbe5da1.txt"
_excerpts = sorted(REPO.joinpath(LOG_DIR.relative_to(REPO).parent).glob("*/" + _EXCERPT_GLOB))
assert len(_excerpts) == 1, f"expected exactly one committed excerpt, found {_excerpts}"
EXCERPT = _excerpts[0]
LOGS = ["a00-d0e2727c", "a00-b6ec457f", "a00-3a7f8962"]
CLAIM_VERSION = "0.67.68"
SLOT = 65536
LOOKBACK = 45


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
    body = [n for n, t in lines if "async _checkCompaction(" in t][0]
    assert all(body < t <= 1928 for t in triggers), "a trigger lives outside _checkCompaction"


def test_no_compaction_check_sits_inside_the_tool_call_loop():
    """(b) no call site lies between a tool result being appended and the next request.

    PASS 8 item 6: the lookback is min(45, lines available). Where the excerpt
    starts later than 45 lines above a call site, the shortfall is PRINTED, not
    silently clamped -- the node no longer claims a full 45 lines at every site.
    """
    lines = excerpt_lines()
    call_sites = [i for i, (n, t) in enumerate(lines) if re.search(r"await this\._checkCompaction\(", t)]
    assert len(call_sites) == 2
    shortfalls = []
    for i in call_sites:
        window = [t for _, t in lines[max(0, i - LOOKBACK):i]]
        if len(window) < LOOKBACK:
            shortfalls.append((lines[i][0], len(window)))
        # each site is guarded by a non-loop boundary, never by tool-result handling
        assert not any("toolResult" in w and "appendMessage" in w for w in window), (
            "call site is inside tool-result handling")
        boundary = [w for w in window if 'event.type === "agent_end"' in w
                    or "Check if we need to compact before sending" in w]
        assert boundary, "call site has no agent_end / pre-prompt boundary in the excerpt"
    if shortfalls:
        print(f"lookback shortfall (excerpt starts mid-window), (source lineno, lines available): {shortfalls}")
    else:
        print("lookback: full 45 lines above both call sites")


def _rows(name):
    log = json.loads((LOG_DIR / f"{name}-request-log.json").read_text())
    return log, log.get("arms", [])


COLS = ("| source | arm | n_requests | max proxy tokens | first index past W | first past 65,536 |"
        " compaction index | 400 index | note |")
SEP = "| --- | --- | --- | --- | --- | --- | --- | --- | --- |"


@pytest.mark.parametrize("name", LOGS)
def test_log_records(name):
    """(c) per arm: max request size vs W and vs the slot; compaction vs 400 ordering.

    PASS 8 items 1/4/5: an UNMEASURED arm is a row of dashes with a reason, never a
    whole-test xfail -- so a fully-read arm still reaches the ordering assert below.
    """
    def emit(line):
        print(line, file=sys.__stdout__)

    emit(COLS)
    emit(SEP)
    log, arms = _rows(name)
    if not arms:
        note = f"no arms ({log.get('status')}: {log.get('selftest')})"
        emit(f"| {name} | (no arms) | - | - | - | - | - | - | {note} |")
        pytest.xfail(f"{name}: log carries no arms ({note})")
    measured = []
    for arm in arms:
        label = arm.get("arm")
        reqs = arm.get("requests") or []

        def gap(reason):
            emit(f"| {name} | {label} | - | - | - | - | - | - | {reason} |")
            return None

        if not reqs:
            gap("no request rows (probe did not run)")
            continue
        idx_key = "seq" if "seq" in reqs[0] else ("request" if "request" in reqs[0] else None)
        if idx_key is None:
            gap(f"no request index field {sorted(reqs[0])}")
            continue
        w = arm.get("declared_window")
        toks = [r["estimated_tokens"] for r in reqs]
        past_w = next((i for i, t in enumerate(toks) if w and t > w), None)
        past_slot = next((i for i, t in enumerate(toks) if t > SLOT), None)
        if "is_compaction" not in reqs[0]:
            # the field is ABSENT, so the compaction index is unknown, not null: the
            # rest of the row is still measured and the ordering assert is skipped
            # for this arm only.
            row = (name, label, len(reqs), max(toks), past_w, past_slot, "-",
                   next((r[idx_key] for r in reqs if r.get("status") == 400), None),
                   "no is_compaction field")
        else:
            row = (name, label, len(reqs), max(toks), past_w, past_slot,
                   next((r[idx_key] for r in reqs if r.get("is_compaction")), None),
                   next((r[idx_key] for r in reqs if r.get("status") == 400), None), "measured")
        measured.append(row)
        emit("| " + " | ".join(str(c) for c in row) + " |")
    assert measured, f"{name}: no arm produced a measured row"
    for r in measured:
        # A declared window did NOT stop the over-ceiling request; compaction followed the 400.
        assert r[5] is not None, f"{r[0]}/{r[1]}: never crossed the slot, log cannot judge the claim"
        assert r[6] == "-" or r[7] is None or r[6] > r[7], (
            f"{r[0]}/{r[1]}: compaction index {r[6]} did not follow 400 index {r[7]}")
