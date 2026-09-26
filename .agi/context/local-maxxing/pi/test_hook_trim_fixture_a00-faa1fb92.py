"""Fixture-only check of the context-hook trim claim (agent a00-faa1fb92).

NO pi, NO subprocess, NO model. Reads committed bytes only:
  paths.local_maxxing.brain_swap_out_dir/<run>-request-log.json   (read via paths.get_local)
  paths.local_maxxing.brain_swap_out_dir/<run>-context-trim.js    (TEXT ONLY, never executed)

Claim under test (hypothesis:lm-pi-context-hook-trim-keeps-one-prompt-loops-under-the-slot):
  with_extension  -> 40 requests, none over 60,000 proxy tokens, no 400, no abort
  without_extension -> a request past 65,536 before request 20
Proxy tokens are re-derived as bytes/3.80 exactly as the claim defines them.

TWO SCALES, both measured (PASS 8 items 3 + 5): the claim's stub accounting is
bytes/3.80 against WINDOW=60,000; the extension's own gate is
  limit     = (contextWindow ?? 60000) - 16384            = 43,616
  estimate  = (JSON.stringify(messages).length + systemPrompt.length) / 4
all parsed out of the committed JS below, never hard-coded. Request BYTES are an
UPPER BOUND on the hook's own estimate (the serialized request carries the messages
plus schemas, tool arguments and framing), so bytes/4 over the limit would prove the
gate was not honoured even though the /3.80 scale passes.

INDEPENDENCE (PASS 8 item 6): a00-3c370e1e is a byte twin of a00-cdde7530 (only
wall_seconds differ, asserted below), so it is excluded from the claim tests. Two
independent confirmations, not three.
"""
import importlib.util
import json
import os
import re
from pathlib import Path

import pytest

# paths.py is found by __file__ (sibling module), never by a new absolute literal.
_spec = importlib.util.spec_from_file_location(
    "lm_paths", Path(__file__).resolve().parents[1] / "paths.py"
)
paths = importlib.util.module_from_spec(_spec)
_spec.loader.exec_module(paths)

LOG_DIR = Path(paths.get_local("brain_swap_out_dir"))
AGI_DIR = Path(os.path.dirname(paths.config_path()))
HYPOTHESIS = AGI_DIR / "nodes" / "hypothesis" / "lm-pi-context-hook-trim-keeps-one-prompt-loops-under-the-slot.md"

RUNS = ["a00-54d3d9b0", "a00-cdde7530", "a00-3c370e1e"]
# item 6: the twin is measured byte-wise, never counted as a second confirmation.
TWIN_OF = {"a00-3c370e1e": "a00-cdde7530"}
INDEP_RUNS = [r for r in RUNS if r not in TWIN_OF]

# The claim's constants, held INDEPENDENTLY of the node -- and cross-checked against
# the node's testable_claim below (PASS 8 item 4), so a claim edit cannot leave this
# file green against stale numbers.
WINDOW = 60000
SLOT = 65536
BYTES_PER_TOKEN = 3.80
N_REQUESTS = 40
BEFORE = 20
RESERVE = 16384
LIMIT = WINDOW - RESERVE  # 43,616 -- the gate the claim actually names


def log(run):
    return json.loads((LOG_DIR / f"{run}-request-log.json").read_text())


def arms(run):
    out = {}
    for arm in log(run)["arms"]:
        out[arm["arm"]] = arm
    return out


def hook_js(run):
    return LOG_DIR / f"{run}-context-trim.js"


def hook_gate(run):
    """(contextWindow default, reserve, divisor, MARK) parsed out of the committed JS."""
    text = hook_js(run).read_text()
    # two committed shapes, both parsed: the 54d3d9b0 hook reads
    # `(usage?.contextWindow ?? N) - M` with a /4 estimate, the cdde7530 hook
    # writes `const LIMIT = N - M` and divides the serialized messages by 4.
    win = re.search(r"contextWindow \?\? (\d+)", text) or re.search(
        r"const LIMIT = (\d+) - (\d+)", text
    )
    reserve = re.search(r"\) - (\d+);", text) or re.search(
        r"const LIMIT = \d+ - (\d+)", text
    )
    div = re.search(r"getSystemPrompt\(\)\.length\) / (\d+)", text) or re.search(
        r"\.length / (\d+) < LIMIT", text
    )
    mark = re.search(r'MARK = "([^"]+)"', text)
    oldest_first = re.search(r"for \(const message of \w+\)", text)
    return {
        "window": int(win.group(1)) if win else None,
        "reserve": int(reserve.group(1)) if reserve else None,
        "divisor": int(div.group(1)) if div else None,
        "mark": mark.group(1) if mark else None,
        "oldest_first": bool(oldest_first),
    }


def tokens(trace):
    return [round(row["bytes"] / BYTES_PER_TOKEN, 1) for row in trace]


def hook_estimate_upper(row, gate):
    """Upper bound on the hook's own estimate: request bytes are >= its JSON length."""
    return row["bytes"] / gate["divisor"]


def first_over(trace, limit):
    for row, tok in zip(trace, tokens(trace)):
        if tok > limit:
            return row["seq"], tok
    return None


ARMS = [f"{r}:{a}" for r in RUNS for a in ("without_extension", "with_extension")]


@pytest.mark.parametrize("key", ARMS)
def test_log_is_committed_and_declares_both_arms(key):
    run, arm = key.split(":")
    assert LOG_DIR.is_dir(), f"paths.local_maxxing.brain_swap_out_dir -> {LOG_DIR} is not a dir"
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


def test_claim_constants_still_match_the_node_testable_claim():
    """item 4: this file's copy of the claim is checked against the node, both ways."""
    text = HYPOTHESIS.read_text()
    claim = re.search(r'^testable_claim: "(.*)"$', text, re.M)
    assert claim, "hypothesis frontmatter has no testable_claim"
    c = claim.group(1)
    for name, val in (("60,000", WINDOW), ("65,536", SLOT), ("3.80", BYTES_PER_TOKEN)):
        assert name in c, f"claim no longer mentions {name} (this file still tests {val})"
    assert f"{N_REQUESTS} requests" in c, f"claim no longer states {N_REQUESTS} requests"
    assert f"request {BEFORE}" in c, f"claim no longer states request {BEFORE}"


@pytest.mark.parametrize("run", INDEP_RUNS)
def test_with_extension_request_count_is_40(run):
    arm = arms(run)["with_extension"]
    assert arm.get("requests") == N_REQUESTS, f"{run}: {arm.get('requests')} requests, claim says {N_REQUESTS}"
    assert len(arm["trace"]) == N_REQUESTS, f"{run}: trace holds {len(arm['trace'])} rows, not {N_REQUESTS}"


@pytest.mark.parametrize("run", INDEP_RUNS)
def test_with_extension_never_exceeds_declared_window(run):
    arm = arms(run)["with_extension"]
    mx = max(tokens(arm["trace"]))
    assert mx < WINDOW, f"{run}: max {mx} proxy tokens over declared window {WINDOW}"


@pytest.mark.parametrize("run", INDEP_RUNS)
def test_with_extension_has_no_400(run):
    arm = arms(run)["with_extension"]
    if "400s" not in arm:
        pytest.xfail(f"{run}/with_extension: missing field '400s'")
    assert arm["400s"] == [], f"{run}: 400s at seq {arm['400s']}"
    bad = [r["seq"] for r in arm["trace"] if r.get("status", 200) >= 400]
    assert bad == [], f"{run}: trace rows with status>=400: {bad}"


@pytest.mark.parametrize("run", INDEP_RUNS)
def test_with_extension_no_abort_recorded(run):
    """The claim's 'no abort' conjunct.

    item 1: this asserted nothing. An abort field (`aborted` / `abort`) is REQUIRED
    for the conjunct to be measured; `timed_out` records a TIMEOUT, not an abort, so
    it can never stand in for one. No abort field in the corpus -> xfail, which is
    the honest outcome and is why the round is a lean, not a proof.
    """
    arm = arms(run)["with_extension"]
    present = [f for f in ("aborted", "abort") if f in arm]
    if not present:
        pytest.xfail(
            f"{run}/with_extension: no abort field (aborted/abort) in the log; "
            f"timed_out={arm.get('timed_out')!r} is a timeout, not an abort -- "
            "the 'no abort' conjunct is UNMEASURED by this corpus"
        )
    for field in present:
        assert not arm[field], f"{run}: {field}={arm[field]!r}"


@pytest.mark.parametrize("run", INDEP_RUNS)
def test_without_extension_crosses_the_slot_before_request_20(run):
    arm = arms(run)["without_extension"]
    hit = first_over(arm["trace"], SLOT)
    assert hit is not None, f"{run}: without_extension never passed {SLOT} proxy tokens"
    assert hit[0] < BEFORE, f"{run}: first request past {SLOT} is seq {hit[0]}, not before {BEFORE}"


@pytest.mark.parametrize("run", RUNS)
def test_extension_js_is_committed_text_not_evaluated(run):
    js = hook_js(run)
    if not js.exists():
        pytest.xfail(f"{run}: missing artifact context-trim.js")
    gate = hook_gate(run)
    assert gate["window"] is not None, f"{run}: no `contextWindow ?? <n>` default in the hook"
    assert gate["reserve"] == RESERVE, f"{run}: hook reserve {gate['reserve']} != {RESERVE}"
    assert gate["divisor"] == 4, f"{run}: hook estimate divisor {gate['divisor']} != 4"
    assert gate["mark"], f"{run}: no MARK placeholder in the hook"
    assert gate["oldest_first"], f"{run}: hook does not walk messages oldest-first"


@pytest.mark.parametrize("run", INDEP_RUNS)
def test_hook_limit_is_window_minus_reserve(run):
    """items 3 + 5: the LIMIT the claim names is parsed, not restated."""
    gate = hook_gate(run)
    limit = gate["window"] - gate["reserve"]
    assert limit == LIMIT, f"{run}: hook limit {limit} != {WINDOW} - {RESERVE} = {LIMIT}"


@pytest.mark.parametrize("run", INDEP_RUNS)
def test_hook_own_scale_stays_under_its_limit(run):
    """items 3 + 5: on the hook's OWN scale (bytes/{divisor}) every with_extension
    request is under the parsed limit -- including the /3.80 scale, which is NOT.

    The request byte count is an upper bound on the hook's serialized-messages
    length, so passing here means the gate was honoured; failing would refute it.
    """
    gate = hook_gate(run)
    limit = gate["window"] - gate["reserve"]
    trace = arms(run)["with_extension"]["trace"]
    worst_row = max(trace, key=lambda r: hook_estimate_upper(r, gate))
    upper = hook_estimate_upper(worst_row, gate)
    on_claim_scale = worst_row["bytes"] / BYTES_PER_TOKEN
    assert upper < limit, (
        f"{run}: seq {worst_row['seq']} request bytes {worst_row['bytes']} -> upper bound "
        f"{upper:.1f} hook tokens, NOT under the hook's own limit {limit}"
    )
    # the two scales disagree, and the claim only ever measured the second
    assert on_claim_scale > limit, (
        f"{run}: bytes/3.80 ({on_claim_scale:.1f}) is expected to sit ABOVE the hook's "
        f"limit {limit} -- if it does not, the divisor gap this test reconciles is gone"
    )


@pytest.mark.parametrize("run", INDEP_RUNS)
def test_extension_actually_elided_oldest_first(run):
    """Mechanism, not wording: the elide counter is monotonic over message order."""
    trace = arms(run)["with_extension"]["trace"]
    counts = [row.get("elided_results", 0) for row in trace]
    assert max(counts) > 0, f"{run}: no request records an elided tool result"
    assert all(b >= a for a, b in zip(counts, counts[1:])), f"{run}: elide count went down: {counts}"


def test_twin_run_is_excluded_from_the_independent_arms():
    """item 6: the corpus holds two independent confirmations, not three."""
    for twin, source in TWIN_OF.items():
        a, b = log(twin), log(source)
        diffs = []
        for arm_a, arm_b in zip(a["arms"], b["arms"]):
            assert arm_a["arm"] == arm_b["arm"]
            for k in arm_a:
                if arm_a[k] != arm_b[k]:
                    diffs.append(f"{arm_a['arm']}.{k}: {arm_a[k]!r} vs {arm_b[k]!r}")
        assert all(d.startswith(("without_extension.wall_seconds", "with_extension.wall_seconds"))
                   for d in diffs), f"{twin} differs from {source} beyond wall_seconds: {diffs}"
        assert diffs, f"{twin} and {source} are byte-identical; twin_of is stale"
    assert len(INDEP_RUNS) == 2, f"independent arms are {INDEP_RUNS}, expected 2"


def test_report_table(capsys):
    rows = []
    for run in RUNS:
        gate = hook_gate(run) if hook_js(run).exists() else None
        for arm_name in ("without_extension", "with_extension"):
            arm = arms(run)[arm_name]
            tks = tokens(arm["trace"])
            hit = first_over(arm["trace"], SLOT)
            n400 = len(arm["400s"]) if "400s" in arm else "xfail"
            fields = [f for f in ("aborted", "abort") if f in arm]
            abort = "recorded=%s" % fields if fields else "UNMEASURED (no abort field)"
            extra = ""
            if arm_name == "with_extension" and gate:
                lim = gate["window"] - gate["reserve"]
                ub = max(hook_estimate_upper(r, gate) for r in arm["trace"])
                extra = f" | hook upper {ub:.1f} < limit {lim} = {ub < lim}"
            rows.append(
                f"{run} | {arm_name} | {arm['requests']} | {max(tks)} | "
                f"{hit[0] if hit else '-'} | {n400} | abort={abort}{extra}"
            )
    header = ("log | arm | n_requests | max proxy tokens (bytes/3.80) | first > 65536 | "
              "400s | abort | hook's own scale")
    print("\n" + header + "\n" + "\n".join(rows))
    assert len(rows) == 6
