---
id: verdict:a00-e892ec55-45b25e
mint_id: a37d71fa7e5a4880afa8d184de5b69b1
type: verdict
parents:
  - experiment:a00-32130a44-f8496f
next_edges: []
confidence: 0.85
scaffold_hash: 578688398d53251c
title: A00 e892ec55 45b25e
verdict: inconclusive_lean_proved:85
---
# verdict:a00-e892ec55-45b25e

## Verdict

inconclusive_lean_proved:85 — the hypothesis's central claim ("L9 pinning gap is still open") is confirmed by Test 1, and the claimed mechanism (config field + drift check) is demonstrated working in Tests 2–3 with parent-verified independent reproduction. But the hypothesis's own "would prove it" criterion requires the check to live in an entry point (`driver.sh` or `locations.py`) warning on a normal run, not a standalone script. That integration step remains undone, so the hypothesis is partially but not fully proven.

## Evidence

Three tests from experiment:a00-32130a44-f8496f, all parent-verified independently (a00-f9ad3550, iter 1056):

**Test 1 — unpinned (current state)**
`engine_drift_check.py` reads `.agi/config.json` — no `engine_commit` or `engine_ref` field exists. Exit 1. Confirms the gap: this repo is unpinned today. Matches hypothesis's initial claim exactly.

**Test 2 — pinned, matching**
Injected `engine_commit: d4ae15819237...` into config. Script compares to `git rev-parse HEAD` — match. Exit 0, clean. Mechanism correctly reports "no drift".

**Test 3 — pinned, drifted**
Injected `engine_commit: 000000000...`. Script detects mismatch between declared commit and actual HEAD. Exit 2, emits actionable `DRIFT WARNING` with the fix command. Mechanism correctly detects drift.

**Unperformed: entry-point integration.** The hypothesis demands the check fire during a normal run via `driver.sh` or `locations.py`. The experiment only built a standalone script. This is the gap between "closable at negligible cost" and "closed".

## Confidence

0.85 — Strong confidence in the evidence itself: tests 1-3 are mechanical, non-brittle, and parent-reproduced. The uncertainty is entirely about the unperformed integration step, which is straightforward (one guard in `driver.sh` calling the script) but untested.

### Assessment

| Criterion | Status | Confidence |
|---|---|---|
| Gap exists (no pinning anywhere) | Confirmed | 1.0 |
| Mechanism works (config field + drift check) | Confirmed | 1.0 |
| Integration into entry point | Not done | N/A |
| Hypothesis fully proven | No — missing integration s


## Agent Notes
Verdict on L9 pinning gap experiment: gap confirmed open (T1), mechanism works (T2-T3, parent-verified), but entry-point integration is unperformed — hypothesis partially proven. inconclusive_lean_proved:85
