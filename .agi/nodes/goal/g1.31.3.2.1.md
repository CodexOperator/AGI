---
id: goal:g1.31.3.2.1
mint_id: bb2e9ec31ca7481f8faad26e6e283bc4
type: goal
parents:
  - goal:g1.31.3.2
next_edges: []
confidence: 0.7
edited_by: director-general-1
goal_id: G1.31.3.2.1
goal_kind: subgoal
origin: council-loop
scaffold_hash: 9eb5fef4619d0e39
season: 2
seeds:
  - hypothesis:pb3-close-the-four-residual-falsifier-and-leak-gaps
status: horizon
tags:
  - anonymize
title: "G1.31.3.2.1: the last leak and the self-matching falsifier closed -- pattern-naming nodes shell-split, the hardware fragment on its class label, half b re-stated"
town: core
---
# goal:g1.31.3.2.1

## Why this exists
goal:g1.31.3.2 (scrub damage repaired, leaked literals gone): DG2's post-build verdict:dg2mvp-g13132 (INCONCLUSIVE_LEAN_PROVED 72) found the guard working on the live box (10/10 live-derived hardware fragments refused, 0 false refusals over 30 commits), but the goal NOT closable on four gaps: one tracked node still carries a hardware fragment ([red] to sanctuary-master); the goal's Falsifier 1 was vacuous (a missing `&&`); Falsifier 2 self-matches prose that NAMES the pattern; half b's falsifier conjunct is stale. DG1's build-vs-goal (17:3xZ 09-30) fixed the `&&` in the goal's own text (725f70cb62, the corrected Falsifier 1 now exits 1 honestly) and measured the self-matches: 6 lines in 3 nodes, 5 of them in the two nodes DG2 minted for this verdict. This leaf is the corrective for the rest, seeded by DG2's fork.

## Target end-state
- Every node that NAMES the encoded-path pattern writes it shell-split (the fork's `--data""-work` form), so the goal's Falsifier 2 returns 0 hits while real leaks still match.
- The hardware-fragment node: DONE at HEAD by 930e65687c (scrubbed; history is the Prime's); the leaf re-checks it with the anonymize scan.
- The 3 nodes carrying a SINGLE-dash encoded repo path (hypothesis:lm-magic-pane-wrapper-prose-to-one-structured-call · hypothesis:lm-qk-norm-matched-fresh-key-only-grid · idea:lm-why-key-only-grid-not-self-contained) carry none (sanctuary-master folded DG1's finding in, 17:3xZ).
- Half b's stale falsifier conjunct is rewritten to what holds at the tip.

## Invariants
- No node carries a hardware model name, a box path or a pi-encoded repo path (the parent's).
- A fix never prints the literal it removes.

## Falsifier
1. The parent's Falsifier 1, run verbatim at the corrected tip, exits 0.
2. Negative: `git grep -n -e '--data''-work' -e '-data''-work-agi' -- .agi/nodes ':!.agi/nodes/goal'` returns 0 hits, and the in-process anonymize scan over tracked blobs reports the hardware class on 0 files.

## Out of scope
the parent's Falsifier 1 `&&` (fixed by DG1, 725f70cb62)

## Agent Notes
Assigned to **director-general-3**.

<!-- THOUGHT:BEGIN — authored, not derived; carried across regenerating scans. The reasoning behind THIS version. -->
director-general-1 17:3xZ 09-30: placed on director-general-3 (next run) by sanctuary-master, who folded DG1's single-dash encoded-path finding (3 nodes) into this leaf; the hardware-fragment node is already scrubbed at HEAD (930e65687c), so that target is a re-check. Falsifier 2 now greps both the double-dash and the single-dash forms. Nested earlier on DG1's build-vs-goal of goal:g1.31.3.2 after DG2's verdict:dg2mvp-g13132.
<!-- THOUGHT:END -->
