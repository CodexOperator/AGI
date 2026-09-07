---
id: hypothesis:a05-bc3ad321-131bbc
mint_id: 7e153a281e8949c7baec0aa53d2dab73
type: hypothesis
parents:
  - goal:g4.8
next_edges: []
confidence: 0.0
edited_by: season.py
scaffold_hash: 175eabbd5377d980
season: 1
testable_claim: A parent-tier agent reviewing its kid deliverables detects and demotes an unevidenced verdict (proved/disproved with no backing evidence_runs, experiment log or test output) without the delegator intervening
thought_session: season
title: A parent demotes an unevidenced verdict unaided -- goal:g4.8 clause 2, never yet observed
verdict: pending
---
# hypothesis:a05-bc3ad321-131bbc

## Hypothesis

**A parent-tier agent reviewing its kid's deliverables will detect and demote an unevidenced verdict (claimed `proved`/`disproved` without backing `evidence_runs`, experiment logs, or test output) without the delegator intervening.** This tests falsifier clause 3 of `goal:g4.8` — the clause that makes the entire parent tier earn its keep: "each parent's review gate demotes at least one unevidenced verdict without the delegator intervening."

### Testable claim

A parent, given a review package containing a kid's node with verdict=`proved` @confidence=0.95 but **no** `evidence_runs` list, **no** experiment logs, and **no** test output — the shape of a confident claim backed by nothing — will identify the missing evidence during review and either:
- Demote the verdict to a lean/pending state (e.g., `inconclusive_lean_proved:N` or `pending`), or
- Flag the gap explicitly in its review notes with a clear "I cannot verify this because..." statement
- Do all of this without requiring any delegator cue

### What would prove it

An experiment where:
1. A simulated kid node is created with `verdict: proved`, `confidence: 0.95`, `evidence_runs: []` (empty — or absent), and a plausible but unsupported body
2. A parent-tier agent is tasked with reviewing it, given only the standard parent brief (no hidden "check for evidence" instruction beyond what the brief already says)
3. The parent's review output shows either a demoted verdict or an explicit "cannot verify — no evidence" finding
4. The delegator did not intervene at any point

**Bonus proof**: three different parent agents (different sessions, different brief phrasings) all catch the same missing evidence, demonstrating the detection is reliable rather than a lucky hit.

### What would disprove it

- The parent accepts the unevidenced verdict at its claimed strength (passes `proved` through without comment)
- The parent notices missing evidence but reports "not my job to verify" or "trusting the kid" rather than demoting
- The parent flags something irrelevant (typos, formatting) while missing the evidence gap entirely
- The parent requires a delegator prompt to look for evidence at all ("did you check if they actually ran the experiment?") — proving the review gate is ineffective without human steering

### Relation to goal:g4.8

Falsifier clause 3 is the **value proposition of the tier system**: a parent must catch low-quality output so the delegator only reviews exceptions. If a parent cannot spot an unevidenced verdict — the cheapest possible failure — then the tier has bought nothing for clause 3 and the delegator must read every node anyway. This hypothesis isolates that clause so it can be disproved or proved independently of whether clause 4 (sub-linear token spend) holds.

**Known risk:** the parent brief may already instruct the parent to check evidence. If it does, this hypothesis tests whether the instruction is *effective*, not whether it exists. The experiment must account for what the brief actually says.

### Downstream from the lease-bound verdict

`verdict:the-bound-is-structural-now` proves clause 2. This hypothesis targets clause 3 as the next isolatable falsifier clause. A passed experiment here means the parent tier can perform its primary quality gate; a failed one means the tier structure for clause 3 needs redesign before scaling to N parents.


## Agent Notes
Parent review gate hypothesis: tests whether a parent-tier agent can detect and demote unevidenced verdicts without delegator intervention (goal:g4.8 falsifier clause 3). Downstream from the proved lease-bound verdict (clause 2). No experiments run yet.