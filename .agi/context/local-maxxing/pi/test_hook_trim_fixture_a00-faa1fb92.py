"""Fixture-only check of the context-hook trim claim (agent a00-faa1fb92).

NO pi, NO subprocess, NO model. Reads committed bytes only:
  datasets/brain-swap/2026-09-24/<run>-request-log.json
  datasets/brain-swap/2026-09-24/<run>-context-trim.js   (TEXT ONLY, never executed)

Claim under test (hypothesis:lm-pi-context-hook-trim-keeps-one-prompt-loops-under-the-slot):
  with_extension  -> 40 requests, none over 60,000 proxy tokens, no 400, no abort
  without_extension -> a request past 65,536 before request 20
Proxy tokens are re-derived as bytes/3.80 exactly as the claim defines them.
"""
import json
import re
from pathlib import Path

import pytest

REPO = Path(__file__).resolve().parents[4]
LOG_DIR = REPO / "datasets/brain-swap/2026-09-24"
RUNS = ["a00-54d3d9b0", "a00-cdde7530", "a00-3c370e1e"]
WINDOW = 60000
SLOT = 65536
BYTES_PER_TOKEN = 3.80
N_REQUESTS = 40
BEFORE = 20


def log(run):
    return json.loads((LOG_DIR / f"{run}-request-log.json").read_text())


def arms(run):
    out = {}
    for arm in log(run)["arms"]:
        out[arm["arm"]] = arm
    return out


def tokens(trace):
    return [round(row["bytes"] / BYTES_PER_TOKEN, 1) for row in trace]


def first_over(trace, limit):
    for row, tok in zip(trace, tokens(trace)):
        if tok > limit:
            return row["seq"], tok
    return None


ARMS = [f"{r}:{a}" for r in RUNS for a in ("without_extension", "with_extension")]


@pytest.mark.parametrize("key", ARMS)
def test_log_is_committed_and_declares_both_arms(key):
    run, arm = key.split(":")
    assert arm in arms(run), f"{run} log has no {arm} arm"


@pytest.mark.parametrize("key", ARMS)
def test_stored_proxy_tokens_equal_bytes_over_3_80(key):
    """The stored field is not trusted: it is re-derived and compared."""
    run, arm = key.split(":")
    trace = arms(run)[arm].get("trace")
    if trace is None:
        pytest.xfail(f"{run}/{arm}: missing field 'trace'")
    for row, tok in zip(trace, tokens(trace)):
        if "proxy_tokens" not in row:
            pytest.xfail(f"{run}/{arm}: missing field 'proxy_tokens'")
        assert row["proxy_tokens"] == tok, f"{run}/{arm} seq {row['seq']}: {row['proxy_tokens']} != {tok}"


@pytest.mark.parametrize("run", RUNS)
def test_with_extension_request_count_is_40(run):
    arm = arms(run)["with_extension"]
    assert arm.get("requests") == N_REQUESTS, f"{run}: {arm.get('requests')} requests, claim says {N_REQUESTS}"
    assert len(arm["trace"]) == N_REQUESTS, f"{run}: trace holds {len(arm['trace'])} rows, not {N_REQUESTS}"


@pytest.mark.parametrize("run", RUNS)
def test_with_extension_never_exceeds_declared_window(run):
    arm = arms(run)["with_extension"]
    mx = max(tokens(arm["trace"]))
    assert mx < WINDOW, f"{run}: max {mx} proxy tokens over declared window {WINDOW}"


@pytest.mark.parametrize("run", RUNS)
def test_with_extension_has_no_400(run):
    arm = arms(run)["with_extension"]
    if "400s" not in arm:
        pytest.xfail(f"{run}/with_extension: missing field '400s'")
    assert arm["400s"] == [], f"{run}: 400s at seq {arm['400s']}"
    bad = [r["seq"] for r in arm["trace"] if r.get("status", 200) >= 400]
    assert bad == [], f"{run}: trace rows with status>=400: {bad}"


@pytest.mark.parametrize("run", RUNS)
def test_with_extension_no_abort_recorded(run):
    """The claim's 'no abort' conjunct: xfail unless the log records aborts at all."""
    arm = arms(run)["with_extension"]
    for field in ("aborted", "abort", "timed_out"):
        if field in arm:
            assert not arm[field], f"{run}: {field}={arm[field]!r}"
            return
    pytest.xfail(f"{run}/with_extension: no field among aborted/abort/timed_out in the log")


@pytest.mark.parametrize("run", RUNS)
def test_without_extension_crosses_the_slot_before_request_20(run):
    arm = arms(run)["without_extension"]
    hit = first_over(arm["trace"], SLOT)
    assert hit is not None, f"{run}: without_extension never passed {SLOT} proxy tokens"
    assert hit[0] < BEFORE, f"{run}: first request past {SLOT} is seq {hit[0]}, not before {BEFORE}"


@pytest.mark.parametrize("run", RUNS)
def test_extension_js_is_committed_text_not_evaluated(run):
    js = LOG_DIR / f"{run}-context-trim.js"
    if not js.exists():
        pytest.xfail(f"{run}: missing artifact context-trim.js")
    text = js.read_text()
    assert "context" in text, f"{run}: context-trim.js does not mention context"


def test_3c370e1e_and_cdde7530_differ_only_in_wall_seconds():
    """Reconciliation of a00-3c370e1e against a00-cdde7530."""
    a, b = log("a00-3c370e1e"), log("a00-cdde7530")
    diffs = []
    for arm_a, arm_b in zip(a["arms"], b["arms"]):
        assert arm_a["arm"] == arm_b["arm"]
        for k in arm_a:
            if arm_a[k] != arm_b[k]:
                diffs.append(f"{arm_a['arm']}.{k}: {arm_a[k]!r} vs {arm_b[k]!r}")
    assert diffs == [
        "without_extension.wall_seconds: 2.78 vs 3.63",
        "with_extension.wall_seconds: 2.35 vs 3.88",
    ], f"unexpected divergence between the two logs: {diffs}"


def test_report_table(capsys):
    rows = []
    for run in RUNS:
        for arm_name in ("without_extension", "with_extension"):
            arm = arms(run)[arm_name]
            tks = tokens(arm["trace"])
            hit = first_over(arm["trace"], SLOT)
            n400 = len(arm["400s"]) if "400s" in arm else "xfail"
            abort = "no aborted/abort field (timed_out=%r)" % arm.get(
                "timed_out", "absent"
            )
            rows.append(
                f"{run} | {arm_name} | {arm['requests']} | {max(tks)} | "
                f"{hit[0] if hit else '-'} | {n400} | abort={abort}"
            )
    header = "log | arm | n_requests | max proxy tokens | first > 65536 | 400s | abort"
    print("\n" + header + "\n" + "\n".join(rows))
    assert len(rows) == 6
