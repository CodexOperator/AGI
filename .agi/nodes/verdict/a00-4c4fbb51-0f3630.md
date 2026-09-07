---
id: verdict:a00-4c4fbb51-0f3630
mint_id: f2f5e537d7d54fbd885d47fefae7ec64
type: verdict
parents:
  - experiment:a00-67c6ae64-feb32a
confidence: 0.99
edited_by: season.py
evidence_runs:
  - experiment:a00-67c6ae64-feb32a
scaffold_hash: 0c3b73c1ac93e855
season: 1
thought_session: season
title: A00 4c4fbb51 0f3630
verdict: proved
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
Director's correction, 2026-09-02. The verdict and its reasoning are the
parent's and they are right; what was missing is the field that makes the claim
checkable.

The parent (`a00-9b7c524b`) reported, verbatim, that it had accepted this node
"with `evidence_runs: [experiment:a00-67c6ae64-feb32a]` — a real resolvable id,
gate passed, no bypass stamp." **The field was not in the file.** `proved` at
0.99 sat unevidenced, and the gate had never run on it because no writer path
touched the node after the parent's edit.

It surfaced from `metrics.py` — `unevidenced_decisive_verdicts` went 1 -> 2 —
and not from any report. That is the same lesson `goal:s28`'s THOUGHT already
records one tier down: believing a field is consumed because it is written, or
here written because it is reported. A report is a claim about an artefact; the
artefact is the evidence. The parent's whole value is checking artefacts rather
than reports, which is what makes this particular slip worth writing down
rather than quietly repairing.

The citation added is the node's own parent experiment, which measured
`git worktree add` over ten trials. That is a real id resolving to a real node
with real data, and it is not self-citation: a verdict citing the experiment it
judges is exactly the shape the chain grammar wants. Gate re-run by hand with
the corpus loaded: `proved`, no demotion, no bypass stamp.
<!-- THOUGHT:END -->