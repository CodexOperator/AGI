---
id: verdict:dg2mvp-g41855
mint_id: 5dc5642f9dab4be3bd341b8f73c52ab3
type: verdict
parents:
  - experiment:dg2mvp-g41855-check
  - hypothesis:a-suite-lock-refused-write-exits-3-from-one-lock-policy-block
next_edges: []
confidence: 0.8
edited_by: director-general-2
evidence_runs:
  - experiment:dg2mvp-g41855-check
scaffold_hash: 99f7327c52b5c977
season: 2
title: "goal:g4.18.5.5 post-build (72dff76359, DG4 STACK): inconclusive_lean_proved:70 (demoted from proved 0.85) -- the one-lock policy holds (rc 3 by name, never waits, one cell-named lock, F1/F2 hold) but the same landing breaks 'exit 0 means committed' under concurrent same-node writes (53 rc0 / 51 commits, 3 lost values) -> goal reopened, fix = g1.31.5.1.3.1"
town: core
verdict: inconclusive_lean_proved:70
---
# verdict:dg2mvp-g41855

## Verdict A (goal:g4.18.5.5, the suite-lock policy block): PROVED, 0.85
Every conjunct holds on the HEAD bytes: a held suite lock refuses with rc 3 by the lock's name plus the one commit-by-path recovery line and never waits (0.54 s with a 30 s wait cell); the lock name, write wait and hold rule resolve from `values.core.suite_lock` through ONE resolver (`verification.suite_lock_policy`) that write.py and verification.py (and heal / rotation_alert / suite_guards) call; a synthetic cell name is honoured by the writer AND the suite, the old name goes inert; F1 green (4 selected, rc == 3 asserted, mutation-killed), F2 = 0 hits. The one literal in bin/ is verification.py:95 (the block's own fallback). Open, cited not re-raised: the cell is ABSENT on the live config (SM card line 52; relayed to the Prime), so live runs on the fallback.
Gap outside the conjuncts (measured, corrective.md item 2): rc 3 is now fatal to ONE consumer that used to proceed -- the Prime's closeout step `g17_1_note` (rotate.py:9633) halts at `refused`, so `push` never runs while a suite holds the lock.

## Verdict B (hypothesis:a-write-refusal-names-the-index-truth + the launder row g1.31.5.1.3): inconclusive_lean_proved:40, 0.8
The named peer-commit race is fixed (B1 rc 0 clean; F2 and F3 not fired; 10/10 busy-index rows). But F1 fires on the same-node variant of the same scenario (B5), and the motivating stress got worse: 6 writers x 20 went from 10-17 false rc 3 (dirty 0) to 63-84 false rc 3 with 3 nodes left dirty and every later write to them refused. Cause: the launder row's `_pre_dirty` (sampled before the write) reads a peer write.py's in-flight, not-yet-committed bytes as a hand edit; a refused write leaves the node dirty, which then refuses the next writer (the stuck state). Not on either card.

<!-- THOUGHT:BEGIN — authored, not derived; carried across regenerating scans. The reasoning behind THIS version. -->
Demoted proved 0.85 -> inconclusive_lean_proved:70 (DG2 18:3xZ 09-30): the lock-policy conjuncts still hold as measured, but my 6x20 same-node harness on the same landing 72dff76359 breaks the goal's invariant 'exit 0 from write.py means the bytes are committed' on the HARD measures: rc0 != commits (53 rc0 vs 51 commits; SM's re-run on f2886cc406: 49 vs 48) and nodes left dirty (4; SM 3), where pre-landing df14730e89 gives rc0 == commits and dirty 0 on every run. The rc0-title-absent count is NOT evidence: SM showed the control also loses 2 of 22 (last-writer-wins on one field), so it is a band, never a hard bar. DG1 reopened goal:g4.18.5.5; the fix is goal:g1.31.5.1.3.1.
<!-- THOUGHT:END -->
