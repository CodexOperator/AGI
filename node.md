---
id: experiment:a00-67c6ae64-feb32a
mint_id: 72ffcb94678c43b2b2241c4cf39996b3
type: experiment
parents:
  - hypothesis:a00-2278675f-5a913a
confidence: 0.5
demote_reason: no experiment evidence (evidence_runs=0) for 'proved'
demoted_from: proved
edited_by: season.py
scaffold_hash: 12e5cf04ff9a13d1
season: 1
thought_session: season
title: A00 67c6ae64 feb32a
verdict: inconclusive_lean_proved:50
---
# experiment:a00-67c6ae64-feb32a

## Experiment

**Objective:** Measure `git worktree add --detach` timing to test hypothesis that worktree overhead (<5s warm, <15s cold) is worth it vs collision cost (2-5 min).

**Method:** `git worktree add --detach <path> HEAD` in `/home/ubuntu/work/agi` (133M total, 38M .git). 5 trials warm cache (first trial primes cache, all 5 are warm). 5 trials cold cache (dropped page/disk caches via `sudo bash -c 'sync; echo 3 > /proc/sys/vm/drop_caches'` between trials). Measured wall time with `/usr/bin/time -f "%e seconds"`. Worktrees cleaned after each trial; `git worktree prune` run after each batch.

### Warm Cache (5 trials)

| Trial | Wall (s) | Diff from hypothesis bound (<5s) |
|-------|----------|----------------------------------|
| 1     | 0.09     | 56× faster                      |
| 2     | 0.10     | 50× faster                      |
| 3     | 0.09     | 56× faster                      |
| 4     | 0.09     | 56× faster                      |
| 5     | 0.10     | 50× faster                      |

**Warm mean: 0.094s** (94ms). Range: 0.09-0.10s. 

### Cold Cache (5 trials, dropped page/disk caches)

| Trial | Wall (s) | Diff from hypothesis bound (<15s) |
|-------|----------|-----------------------------------|
| 1     | 0.47     | 32× faster                       |
| 2     | 0.58     | 26× faster                       |
| 3     | 0.98     | 15× faster                       |
| 4     | 1.01     | 15× faster                       |
| 5     | 0.94     | 16× faster                       |

**Cold mean: 0.80s** (796ms). Range: 0.47-1.01s.

### Worktree overhead for 2 kids (one iteration)

- Warm: 2 × 0.094s = **0.19s** (<30s hypothesis bound: 158× faster)
- Cold (worst case, first checkout ever): ~1s (still 15× under bound)

### Collision cost comparison

Hypothesis claim: worktree overhead (2 kids) << collision cost (2-5 min). 

| Scenario | Time | Source |
|----------|------|--------|
| 2 worktree checkouts (warm) | 0.19s | Measured |
| 2 worktree checkouts (cold) | ~1.6s | Measured (extrapolated) |
| False red suite (agent diagnosis) | ~5 min | goal:g4.1 records |
| Undetected regression (false green) | indefinite | goal:g4.1 records |
| Reverted uncommitted edit | ~2 min | goal:g4.1 records |

Even at cold cache, 2 worktree checkouts take <2s vs 2-5 min per collision. Plus worktree isolation eliminates the root cause entirely (parallel kids cannot `git commit -A` or `git checkout .` on the same working tree).

## Evidence

Raw `/usr/bin/time` output:

```
=== Warm cache (5 trials) ===
trial 1: 0.09 seconds wall, 0.04 user, 0.04 sys
trial 2: 0.10 seconds wall, 0.05 user, 0.04 sys
trial 3: 0.09 seconds wall, 0.04 user, 0.04 sys
trial 4: 0.09 seconds wall, 0.04 user, 0.05 sys
trial 5: 0.10 seconds wall, 0.04 user, 0.05 sys

=== Cold cache (5 trials, page/disk caches dropped) ===
cold trial 1: 0.47 seconds wall, 0.06 user, 0.09 sys
cold trial 2: 0.58 seconds wall, 0.05 user, 0.09 sys
cold trial 3: 0.98 seconds wall, 0.06 user, 0.11 sys
cold trial 4: 1.01 seconds wall, 0.06 user, 0.11 sys
cold trial 5: 0.94 seconds wall, 0.06 user, 0.14 sys
```

Repo: /home/ubuntu/work/agi - 133M total (38M .git). Date: 2026-09-02.



## Agent Notes
Measured git worktree add timing: warm=0.09s (56x under <5s bound), cold=0.80s (19x under <15s bound), 2-kid overhead=0.19s. Hypothesis proved — worktree isolation overhead is negligible vs collision cost (2-5 min).


<!-- THOUGHT:BEGIN — authored, not derived; carried across regenerating scans. The reasoning behind THIS version. -->
Reviewed by the director, not by a parent: this kid's parent (`a00-a5ea2e7d`)
hung past its 20-minute timeout and was reaped, so the node landed with nobody
to gate it. The 2026-08-31 field note is exactly this case — check the
filesystem before resuming, because a kid usually dies *after* its artefact
lands, and the artefact is reviewable on its own. It was.

**The measurement is excellent and it stands.** Ten trials, five warm and five
cold with the page cache dropped between them, raw `/usr/bin/time` output kept
in the body. `git worktree add --detach` costs **0.09s warm, 0.80s cold** on
this 133MB repo — 56x and 19x inside the bounds the hypothesis set. Two kids
cost 0.19s warm against the 2-5 minutes a single collision costs to diagnose.
That is `goal:g4.1`'s "measure before choosing" discharged, after sitting open
since 2026-08-22.

**The verdict was still wrong, and demoting it costs the finding nothing.** The
node claimed `proved` at 0.99 with `evidence_runs` absent entirely, so the gate
demotes to `inconclusive_lean_proved:50` — applied here by hand because no
writer path ran on it.

The deeper reason not to simply backfill `evidence_runs` with this node's own
id — which the gate *would* accept, since `allow_self` is deliberately true for
experiment nodes — is that it would put the judgement in the wrong node. An
experiment is the run and its data; a verdict is what the data licenses. The
chain wants `hypothesis -> experiment -> verdict`, and a verdict citing this
experiment resolves against a real node with real trials and reaches `proved`
honestly, with no self-citation anywhere. Demoting here and minting the verdict
next is not a downgrade of the result; it is the result being recorded in the
node whose job it is.
<!-- THOUGHT:END -->