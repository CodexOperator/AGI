---
id: hypothesis:a00-0d182e77-3f4501
mint_id: e92746414a884a889f27bb02cc92c8ed
type: hypothesis
parents:
  - goal:s22
next_edges:
  - experiment:a00-788f8d7f-f11472
confidence: 0.85
edited_by: season.py
evidence_runs: 0
scaffold_hash: 9998df62558bd57b
season: 1
thought_session: season
title: A00 0d182e77 3f4501
verdict: pending
wired_at: 1788244944
wired_from: a00-0d182e77
---
# hypothesis:a00-0d182e77-3f4501

## Hypothesis

**Claim.** Removing `goal` from `spawn.allowed_parents` in `[mvp].md`
(`[verdict, goal, experiment, hypothesis]` → `[verdict, experiment, hypothesis]`)
and `[experiment].md`
(`[hypothesis, verdict, goal, task, idea, experiment, build]` →
`[hypothesis, verdict, task, idea, experiment, build]`), and updating the
zoom.py kid contract (lines 594, 691) to remove `mvp from exp` and add
`verdict from exp`, makes `spawn_gate` mechanically reject a `goal → mvp`
or `goal → experiment` spawn while leaving every other route in the corpus
intact.

**What would prove it.**

1. `spawn_gate.py check --type mvp --parent goal:g13` exits 2 (rejected),
   naming `goal` as an unallowed parent.
2. `spawn_gate.py check --type experiment --parent goal:s22` exits 2
   (rejected).
3. `spawn_gate.py check --type hypothesis --parent goal:s22` exits 0
   (approved) — the intended route still works.
4. `spawn_gate.py check --type cron --parent goal:s22` exits 0 (approved) —
   the structural exception is untouched.
5. `spawn_gate.py rules --root <graph>` shows the updated lists with `goal`
   absent from both.
6. `zoom.py` grep confirms neither line 594 nor 691 still advertises
   `mvp from exp`.
7. Active node count unchanged — no existing node is invalidated.

**What would disprove it.**

- `spawn_gate` still accepts a `goal → mvp` or `goal → experiment` spawn
  after the two schema edits (the gate is not actually reading the changed
  `allowed_parents`, e.g. a cached `.pyc` or a second schema source).
- A `cron` node with a `goal` parent is rejected (over-stripped the rule).
- The node count drops (an existing valid node became invalid).

**Scope.** Two schema files, one source file (`zoom.py`), one test. The
change is the two lines the goal audit identified; no new code paths are
required because `spawn_gate.py` already reads `allowed_parents` from
schemas generically.

<!-- THOUGHT:BEGIN — authored, not derived; carried across regenerating scans. The reasoning behind THIS version. -->
First hypothesis spawned under goal:s22. The goal's falsifier section
already named the exact commands to run, so this hypothesis is a
restatement of those as a testable claim with explicit proof and
disproof criteria — the node the experiment will reference. Kept tight:
no scope expansion to the parent-variant resolution open item the goal
defers.
<!-- THOUGHT:END -->

## Agent Notes
Hypothesis restating goal:s22's falsifier as testable claim with 7 proof and 3 disproof criteria