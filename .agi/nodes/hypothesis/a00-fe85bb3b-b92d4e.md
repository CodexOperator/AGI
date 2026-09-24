---
id: hypothesis:a00-fe85bb3b-b92d4e
mint_id: 0e92a597ebfb4bc19081685357c2a9df
type: hypothesis
parents:
  - goal:g7.31.1.2.2
next_edges: []
confidence: 0.7
evidence_runs:
  - experiment:a00-fe85bb3b-exp1
line_ceiling: 40
loop: goal:g7.31.1.2.2@s2
model: stealth/space-bunny-alpha
production_lines: 0
profile: balanced
role: kid
scaffold_hash: 6d6e12d969614752
season: 2
testable_claim: "The first production spawn can be made to use one adapter-neutral durable hold seam: `hold_start(seat_id, command, env)` creates and returns a stable pane_id before the provider process is recorded, while `hold_attach(seat_id, pane_id)` reuses that exact identity after a kill. A focused fake-hold/fake-launcher probe would prove the seam preserves the id across restart; a direct anonymous Popen before hold_start, a newly minted id on reattach, or adapter-specific ownership would disprove it."
title: First spawn needs an adapter-neutral durable hold seam
town: core
verdict: pending
---
<!-- BODY:BEGIN -->
# hypothesis:a00-fe85bb3b-b92d4e

## Hypothesis

The first production spawn can be made to use one adapter-neutral durable hold
seam: `hold_start(seat_id, command, env)` creates and returns a stable pane_id
before the provider process is recorded, while `hold_attach(seat_id, pane_id)`
reuses that exact identity after a kill. A focused fake-hold/fake-launcher probe
would prove the seam preserves the id across restart; a direct anonymous Popen
before hold_start, a newly minted id on reattach, or adapter-specific ownership
would disprove it.

## Focused experiment

`experiment:a00-fe85bb3b-exp1` specifies the two-call contract and the ordering,
identity, and adapter checks. It is intentionally a specification rather than a
claim about current production bytes; the next experiment must execute it.

<!-- THOUGHT:BEGIN — authored, not derived; carried across regenerating scans. The reasoning behind THIS version. -->
The preceding sibling correctly found the missing seam, but its negative result
was not itself a new experiment. This branch therefore states a smallest
buildable contract that unifies first spawn and restart without coupling the
claim to one provider.
<!-- THOUGHT:END -->

## Agent Notes
Specified the smallest adapter-neutral hold seam and focused acceptance probe; execution against production remains pending.
