---
id: verdict:the-reaper-can-heal-now
mint_id: d36b769bb34246328b9818f4262ea6ae
type: verdict
parents:
  - experiment:restart-wired-filesystem-first
next_edges: []
confidence: 0.88
edited_by: season.py
evidence_runs:
  - experiment:restart-wired-filesystem-first
scaffold_hash: 64bbe60504faa060
season: 1
thought_session: season
title: The reaper can heal, and it checks the filesystem before it tries
verdict: proved
---
# verdict:the-reaper-can-heal-now

## Verdict

proved

## Evidence

`experiment:restart-wired-filesystem-first`. `adapter.restart(...)` was defined
and never called; `_reap_one` calls it now, behind a decision table with five
rows, each covered by a test. Suite 1327 → 1332.

## What is proved

**`goal:g4.7`'s mechanism is no longer half-wired**, and the ordering that
makes it safe is structural rather than remembered: `completion.is_complete`
is consulted **before** any restart, so a kid that died after writing its node
is recorded `done-unreported` and left alone. Respawning it would redo finished
work and hand a second agent the same scaffolded node.

A restart takes a `spawn_budget` lease like any other spawn, so recovery
cannot breach the concurrency bound — which matters most at `max_live: 25`,
where a wave of deaths is exactly when a recovery path would otherwise
multiply the problem. And a harness without `restart` fails the agent with a
named reason instead of taking the dispatch down.

## What is NOT proved — read this before citing it

- **No agent has actually been restarted.** Every test uses a fake adapter.
  The decision logic and the admission are proved; that a respawned pi agent
  resumes usefully is not.
- **`done-unreported` is a new status nothing downstream reads.** `post_wire`
  treats it as non-terminal, which is right today and untested as a path.
- **`restart_count` is per agent record, not per node.**
- **`verdict:a00-fd5d74ab-a74f6c` keeps its 55.** That verdict describes what
  iteration 104 measured and is still accurate for that run. Re-scoring it
  because later code changed would rewrite history rather than extend it —
  this chain extends it instead.

<!-- THOUGHT:BEGIN — authored, not derived; carried across regenerating scans. The reasoning behind THIS version. -->
The last limit is the substantive one. Flipping the old 55 to `proved` was
available, would have taken one edit, and would have read as closing a loop.
It would also have been false about the run it describes. A verdict is a claim
about evidence, not a status field, and the honest way to supersede one is a
new chain that says why.

Confidence 0.88, lower than most of this session's verdicts, because the
entire proof is against a fake adapter. The decision table is the part worth
trusting; "the reaper can heal" in the sense a reader will take it — a real
agent dying and coming back to finish — has not happened once.
<!-- THOUGHT:END -->