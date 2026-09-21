---
id: hypothesis:a00-07b2223d-b21977
mint_id: 694956c923504867a9f0cd20a4884033
type: hypothesis
parents:
  - goal:g4.8
next_edges:
  - experiment:parent-review-demotes-unevidenced
confidence: 0.0
edited_by: season.py
scaffold_hash: 7b6d1953a5af6c48
season: 1
testable_claim: "With a parent that spawns M kids on the kid model tier, each kid returning a verdict on its experiment: - Every kid with `proved` or `disproved` but no `evidence_runs` referencing existing experiment nodes gets demoted to `inconclusive_lean_proved:N` or `inconclusive_lean_disproved:N` respectively. - Kids whose verdict is `pending` or already a lean pass through unchanged. - The parent's review cost (in tokens) is sub-linear if M grows, because the review is structural (check evidence_runs, check verdict enum) rather than substantive (re-reading each hypothesis)."
thought_session: season
title: Parent review gate reliably demotes unevidenced verdicts
verdict: pending
---
# hypothesis:a00-07b2223d-b21977

## Hypothesis

A parent agent, reviewing its kids' verdicts on the parent model tier, can reliably detect and demote verdicts that lack backing experiment evidence ("unevidenced verdicts") — returning `pending` or `inconclusive_lean_*:N` — without the delegator (director) needing to intervene.

### Testable claim

With a parent that spawns M kids on the kid model tier, each kid returning a verdict on its experiment:
- Every kid with `proved` or `disproved` but no `evidence_runs` referencing existing experiment nodes gets demoted to `inconclusive_lean_proved:N` or `inconclusive_lean_disproved:N` respectively.
- Kids whose verdict is `pending` or already a lean pass through unchanged.
- The parent's review cost (in tokens) is sub-linear if M grows, because the review is structural (check evidence_runs, check verdict enum) rather than substantive (re-reading each hypothesis).

### What would prove it

An experiment running 1 parent that spawns 5 kids on `goal:g4.8`, where:
- Kid 1 returns `proved` with `--evidence-runs experiment:real-thing` (valid — pass through)
- Kid 2 returns `disproved` with `--evidence-runs experiment:real-thing` (valid — pass through)
- Kid 3 returns `proved` with no `--evidence-runs` (invalid — demoted to `inconclusive_lean_proved:A` where A≥50)
- Kid 4 returns `disproved` with no `--evidence-runs` (invalid — demoted to `inconclusive_lean_disproved:B` where B≥50)
- Kid 5 returns `pending` with no evidence (already correct — unchanged)

Result: parent correctly demotes kids 3 and 4, leaves 1, 2, 5 alone. Delegator inspects only the parent's brief, not the 5 kid nodes.

### What would disprove it

- Parent lets `proved` or `disproved` with empty `evidence_runs` through unchanged — clause 3 violated.
- Parent demotes a valid `proved`/`disproved` that has real evidence — false positive, breaks valid work.
- Parent's own review costs grow linearly with M because it reads every kid's full body — clause 4 advantage never materializes.
- Parent cannot parse the `evidence_runs` field from the YAML frontmatter — structural gate fails.

### Relation to g4.8

Directly tests g4.8 falsifier **clause 3** ("each parent's review gate demotes at least one unevidenced verdict without the delegator intervening"). Also informs clause 4 (sub-linear delegator spend) — if the parent's review itself is linear in M, only the delegator's savings are sub-linear, not the system's. A parent that can gate structurally (check frontmatter fields, not re-read hypotheses) achieves sub-linear review per kid.



## Agent Notes
Hypothesis: parent review gate (structural check of frontmatter evidence_runs field) can reliably demote unevidenced proved/disproved verdicts from kids, directly testing g4.8 falsifier clause 3. Targets remaining unproved falsifier clause: parent review without delegator intervention.