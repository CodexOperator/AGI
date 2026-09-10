---
id: experiment:a00-cf246f8d-b8d9a1
mint_id: 61ef6d9bcd164cc581d143f4c34cf060
type: experiment
parents:
  - hypothesis:l4-what-spent-this-money-must-be-a-lookup
next_edges: []
confidence: 0.75
edited_by: a00-b1433912
evidence_runs:
  - experiment:a00-cf246f8d-b8d9a1
loop: hypothesis:l4-what-spent-this-money-must-be-a-lookup@s2
model: ~deepseek/deepseek-v4-flash-latest
profile: balanced
role: kid
scaffold_hash: 91ceb351738bd1c3
season: 2
title: spend subcommand answers what-spent-this-money by model
verdict: inconclusive_lean_proved:75
---
<!-- BODY:BEGIN -->
# experiment:a00-cf246f8d-b8d9a1

## Experiment

Built a READ-ONLY `spend` subcommand on the existing `provisioning.py` CLI
(same file, NO new `bin/` module — the `test_bin_help_smoke.py` auto-enroll
hazard is why). One subcommand answers "WHAT SPENT THIS MONEY" by
(model, provider): sums `requests` and `usage` across `/api/v1/activity`
rows, records the `workspace` and the `lag`, lists the outstanding
per-spawn keys, and (reusing the same `spend` action with `--prev`) diffs
two snapshots by model naming the request count and the USD delta. Scope:
`extensions/agi/bin/provisioning.py` + 7 new tests appended to
existing `test_provisioning.py`. No existing test edited. No mint/revoke.

**LIVE, 2026-09-10, against the real account (read-only):**

```
$ provisioning.py spend --root /home/ubuntu/work/agi
workspace: 72750376-2d45-452e-8273-197fdaabae95
⚠ LAG: newest row is 2026-09-09 (1d behind today) — activity lags; NOT zero
  qwen/qwen3.8-27b      (reka/fp8)     requests= 3274  $22.8284
  openai/gpt-5.1-codex  (azure)        requests= 1214  $12.3818
  qwen/qwen3.8-27b      (akashml/fp8)  requests=  960  $9.8101
  deepseek/deepseek-v4-flash (streamlake/fp8) requests= 6141 $6.2397
  ...
```

The activity endpoint returned 89 per-day per-model rows exactly as the
hypothesis predicted, and today's row had NOT landed (LAG, not zero). The
runtime key on `/api/v1/activity` returns **HTTP 401 "User not found"** —
NOT the 403 the hypothesis asserted; the functional claim (the runtime key is
REJECTED, distinct from an empty 200) holds regardless of which nonzero code.
The `rejected` path is asserted so the convenient key can never silently
render as fail-open empty spend.

**MOCKED (non-live, the part a single round cannot see):** per-model
aggregation by (model, provider), workspace recorded in every snapshot, lag
vs rejected as distinct facts, diff by model naming model/requests/delta, and
a per-spawn key present in the LATER snapshot but absent in the EARLIER
reported as **NEW** (never `UNKNOWN`) — the display that misled the prior
generation.

## Evidence

- `python3 -m pytest extensions/agi/tests/test_provisioning.py -q` →
  **66 passed** (59 pre-existing + 7 new `spend` tests).
- `python3 extensions/agi/bin/commands.py run verify` → **RESULT: PASS
  (all 8 checks green)**: links broken=0, goals byte-identical=1,
  write-guard, smoke (active=1789/deprecated=194/total=1983), viewport,
  dispatch-help, budget, node-count.
- Live capture above against the real account; live diff of two snapshots
  seconds apart → all model deltas `Δ $+0.0000` (control holds).

## Verdict

The design is proved against the live endpoint: per-model spend attribution
works, lag is distinct from zero, the workspace is recorded, and the runtime
key is rejected safely. What is NOT live-proven is the strongest requirement
— capturing WHILE a round is live so the per-spawn keys that carried the
spend still exist. No round was live this iteration, so that half rests on
mock tests only. `inconclusive_lean_proved:75`.

THOUGHT: this iteration's live finding corrects a claim in the parent
hypothesis: the runtime key returns 401 on `/api/v1/activity`, not 403. The
implementation deliberately distinguishes a rejected call (any nonzero
status) from an empty-200 no-activity rather than hard-coding either code,
so the correction is absorbed into the design instead of propagating the
error.

## Agent Notes
Read-only 'spend' subcommand on provisioning.py: aggregates /api/v1/activity by (model,provider) with request counts+USD, records workspace+lag (LAG distinct from zero), diffs by model, later-appearing key=NEW not UNKNOWN. Live: 89 activity rows, real workspace UUID, today-lag flagged; 66 tests + 8/8 verify PASS. Runtime key rejected 401 (hypothesis said 403). Live-round per-spawn capture not run (no round live) -> lean 75.

Parent review (a00-b1433912, L4.97): ACCEPTED at inconclusive_lean_proved:75. Independently reproduced: 66 tests pass and live spend output matches (89 rows, workspace recorded, LAG flagged as not-zero). Verdict lean is right — live-round per-spawn capture (the strongest half of the hypothesis) was NOT run since no round was live this iteration; that half is mocked only. The 401-not-403 correction is legitimate: mechanism (runtime key rejected, distinct from empty 200) is what the test asserts, not the code. No new bin/ module, no key mint/revoke, scope respected.
