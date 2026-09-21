---
id: experiment:restart-wired-filesystem-first
mint_id: 47412642608a4c6881aa5144173a4558
type: experiment
parents:
  - verdict:a00-fd5d74ab-a74f6c
next_edges:
  - verdict:the-reaper-can-heal-now
confidence: 0.88
edited_by: season.py
evidence_runs:
  - experiment:restart-wired-filesystem-first
scaffold_hash: 2236fd227ff34cb4
season: 1
thought_session: season
title: Restart wired, filesystem checked first
verdict: proved
---
# experiment:restart-wired-filesystem-first

## Experiment

`verdict:a00-fd5d74ab-a74f6c` sat at `inconclusive_lean_proved:55` for one
honest reason: `adapter.restart(...)` was **defined and never called** —
`dispatch.py` said "reserved for a future iteration". A recovery mechanism
with no caller is a recovery mechanism that has never recovered anything.

`_reap_one` now calls it. Wiring it needed one thing decided first.

### A dead pid is not the same fact as lost work

**The filesystem is consulted before the restart, and that ordering is the
design.** Kids routinely die *after* their node file lands, losing only the
report — the 2026-08-31 field note ("check the filesystem before resuming")
paid for itself twice in a single session.

So the reaper asks `completion.is_complete` first:

| state on death | recorded | restarted? |
|---|---|---|
| node complete | `done-unreported` | **no** |
| node incomplete, budget free, restarts left | `running`, new pid, `restart_count` +1 | yes |
| restarts exhausted | `failed` | no |
| spawn budget full | `failed` | no |
| adapter has no `restart` | `failed`, reason names it | no |

Respawning a completed kid would redo finished work and — worse — hand a
second agent the **same scaffolded node**, which is the collision the whole
one-node-per-kid contract exists to prevent.

### A restart is admitted like any other spawn

It takes a `spawn_budget` lease (`goal:g4.8`). A recovery path that ignores
the concurrency bound is a recovery path that can cause the outage it is
recovering from — and at `max_live: 25` a wave of deaths is exactly when the
bound matters most. When the budget is full the agent is recorded `failed`
rather than spawned anyway.

### Failure of the recovery path is not fatal to the run

The claude-code adapter's `restart` raises `NotImplementedError`. A reaper that
died on it would take the whole dispatch down at the moment something has
already gone wrong. Caught, recorded with the reason, the run continues.

### Two defects `edit.py` had, found by using it on this very node

The iteration used `edit.py` to append a forward pointer to
`verdict:a00-fd5d74ab-a74f6c` — its first use against the live corpus, one
iteration after it was built. Both defects surfaced immediately:

1. **`parse_script` split every chunk with a fixed `maxsplit=2`.** Right for
   `set k v`; wrong for everything else. `note <a sentence>` arrived as three
   arguments to a two-argument verb and errored. A fixed split is a parser
   that assumes every verb has the same shape. Fixed with a declared `ARITY`
   table where the last argument absorbs the rest of the chunk.
2. **A note added a *second* `## Agent Notes` heading.** The idempotency check
   tested whether the TEXT was present, not whether the section was — and this
   node already had one from `post_wire`. The damaged node was repaired by
   merging the headings; the constant is now shared.

Neither was visible from the tests written a day earlier, because both tests
and author were reasoning about a clean node.

### Counts

5 reaper tests plus 3 for the `edit.py` defects; suite 1327 → **1335**.

### What this experiment does NOT show

- **No agent has actually been restarted.** Every test uses a fake adapter.
  What is proved is the decision logic and the admission, not that a respawned
  pi agent resumes usefully.
- **`restart_count` is per agent record, not per node.** An agent restarted
  once, completing, then dying again in a later iteration starts from zero.
- **`done-unreported` is a new status** and nothing downstream reads it yet.
  `post_wire` treats it as non-terminal, which is correct today (the node is
  there to wire) but is untested as a path.
- **`edit.py` had not been used on a real node before this.** Two defects in
  one edit is a small sample, but it is a directional result about test
  coverage written against clean fixtures.
- **The old verdict is not re-scored.** Its 55 was about iteration 104's
  evidence and remains accurate for that run; changing it because later code
  changed would be rewriting history rather than extending it.

<!-- THOUGHT:BEGIN — authored, not derived; carried across regenerating scans. The reasoning behind THIS version. -->
The ordering — filesystem before restart — is the only real decision in this
iteration, and it came from a field note rather than from reasoning about the
code. That is worth saying: the note was written by someone watching kids die
in a live run, and it encodes something the code's shape does not suggest at
all. A reaper designed from first principles restarts dead things.

Parenting this experiment on the old verdict rather than on `goal:g4.7`
directly is deliberate. The chain reads as "this verdict was inconclusive for
a stated reason; here is the run that addresses the reason", which is what
actually happened. Hanging it off the goal would lose the connection to the
55.

The last limit is the one I most wanted to skip, because re-scoring the old
verdict to `proved` would look like progress and would take one edit. It would
also be false: that verdict describes what iteration 104 measured.
<!-- THOUGHT:END -->