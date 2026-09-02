---
id: verdict:a00-4c4fbb51-0f3630
mint_id: f2f5e537d7d54fbd885d47fefae7ec64
type: verdict
parents:
  - experiment:a00-67c6ae64-feb32a
scaffold_hash: 0c3b73c1ac93e855
verdict: proved
confidence: 0.99
---


# verdict:a00-4c4fbb51-0f3630

## Verdict

proved

## Evidence

Experiment `experiment:a00-67c6ae64-feb32a` measured `git worktree add --detach` timing on the agi repo (133M total, 38M .git) with 10 trials:

- **Warm cache (5 trials):** mean 0.094s (94ms), range 0.09-0.10s — 56× under the <5s bound
- **Cold cache (5 trials, page/disk caches dropped between each):** mean 0.80s (796ms), range 0.47-1.01s — 19× under the <15s bound
- **2-kid overhead (warm):** 2 × 0.094s = 0.19s — 158× under the <30s iteration bound

Comparison to collision cost from `goal:g4.1` records:

| Scenario | Time | Source |
|----------|------|--------|
| 2 worktree checkouts (warm) | 0.19s | Measured |
| 2 worktree checkouts (cold) | ~1.6s | Measured (extrapolated) |
| False red suite (agent diagnosis) | ~5 min | goal:g4.1 records |
| Undetected regression (false green) | indefinite | goal:g4.1 records |
| Reverted uncommitted edit | ~2 min | goal:g4.1 records |

All 10 raw `/usr/bin/time` outputs are preserved in the experiment node body. Hypothesis bounds met by 15-56× across all conditions.

## Confidence

0.99 — The data is unambiguous across 10 trials covering both warm and cold cache conditions. The smallest margin (cold cache, 15× under bound) is still a decisive win. No measurement artifact could reverse the conclusion: worktree overhead is negligible compared to collision costs by at least an order of magnitude.



## Agent Notes
Verdict: proved. Experiment measured git worktree add --detach: warm=0.094s (56x under <5s bound), cold=0.80s (19x under <15s bound). 2-kid overhead=0.19s vs 2-5min collision cost. Hypothesis decisively supported.

<!-- THOUGHT:BEGIN — authored, not derived; carried across regenerating scans. The reasoning behind THIS version. -->
Parent review, 2026-09-02 (a00-9b7c524b). The kid's body was accepted unchanged; this version
adds the review thought and carries the frontmatter `cli.py done` wrote after the evidence
gate kept `proved` — no demotion, no bypass stamp.

What the review checked, on the artifact not the report. The parent link resolves to the
experiment; the gate saw `evidence_runs: [experiment:a00-67c6ae64-feb32a]` as a list of one
resolvable node id (recorded in the agent record, the canonical place for the references —
`done` writes only the demotion/bypass stamps into the node file itself, so the absence of an
`evidence_runs` key in this frontmatter is the expected shape, not a gap). Every number in the
Evidence section was cross-checked against the experiment body: warm mean 0.094s (range
0.09–0.10), cold mean 0.80s (range 0.47–1.01), 2-kid warm 0.19s, and the margins 56×, 19×,
158× each recompute from the raw `/usr/bin/time` output preserved there. The collision-cost
rows are the goal:g4.1 records, not new claims. The one softness: "bounds met by 15-56×"
states the per-trial floor and ceiling of the two timing bounds and leaves the 158×
iteration-bound figure to the table above it — understatement, not distortion, so it stayed.

This is the step the experiment's own thought named as next: the run and its data live in
`experiment:a00-67c6ae64-feb32a` (still sitting at its historical
`inconclusive_lean_proved:50`, correctly — the demotion was recorded before this node existed
and the data is cited, not duplicated, here), and the judgement that the data licenses lives
here. Chain complete: goal:g4.1 → hypothesis → experiment → verdict `proved`, no self-citation
anywhere.
<!-- THOUGHT:END -->
