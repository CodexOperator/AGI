---
id: experiment:lease-bound-under-five-spawners
mint_id: 4edb4c4c5f534ab2a72b13b09694fe9e
type: experiment
parents:
  - hypothesis:shared-lease-bounds-the-tree
next_edges:
  - verdict:the-bound-is-structural-now
confidence: 0.97
edited_by: season.py
evidence_runs:
  - experiment:lease-bound-under-five-spawners
scaffold_hash: 05b6ef7d188857cc
season: 1
thought_session: season
title: Five independent spawners, five slots each, one lease directory
verdict: proved
---
# experiment:lease-bound-under-five-spawners

## Experiment

**What.** Five independent OS processes — the shape of five parents each
running `dispatch.py` for itself — race through one lease directory, taking
five slots each. Twenty-five would-be agents against one tree. Every successful
admission samples the live count immediately after committing its lease, so the
recorded peak is the population as an admitted agent actually observed it, not
a count taken afterwards.

Run at caps 1, 3 and 5, plus a **negative control** at a cap of 999 — the cap
that does not bind, which is the pre-fix behaviour: every spawner opening its
own population against the same tree.

**Code under test:** `extensions/agi/bin/spawn_budget.py`.
**Harness:** `extensions/agi/tests/test_spawn_budget.py::test_the_live_population_never_exceeds_the_bound_under_concurrency`, `multiprocessing` fork context, 5 processes, 5 slots each.

### Results

| cap | admissions | peak live | distinct samples | verdict |
|---|---|---|---|---|
| 1 | 2 | **1** | {1} | at bound, never over |
| 3 | 5 | **3** | {2, 3} | at bound, never over |
| 5 | 10 | **5** | {3, 4, 5} | at bound, never over |
| **999 (control)** | **25** | **24** | — | unbounded, as before the fix |

**The peak equals the cap in every bounded run.** That is the clause that
matters second-most: a bound test which passes because nothing was admitted is
the cheapest possible false green, and this project has already recorded a
smoke check that passed on a traceback because absent output and a crash look
identical to `grep`. These runs sat *on* the boundary and did not cross it.

**The control is what makes the other three mean anything.** At a cap of 999
the identical harness admitted all 25 and peaked at 24 — so the assertion is
measuring the bound and not some accidental serialization in the test rig. A
cap-5 assertion applied to the control run fails.

### The grandchild property, isolated

`test_a_second_independent_spawner_counts_against_the_first` runs the smallest
version: one process takes a lease at cap 2, then a **separate interpreter**
is started and asked for two. It gets exactly one. The second spawner was cut
off at the shared bound rather than at its own — which is the whole difference
from `spawn.parallel`, where the second invocation reads the same number and
opens a fresh population.

### Reclamation, which the hypothesis named as a disproof condition

- `test_a_dead_agents_lease_is_reclaimed_without_anyone_releasing_it` — a real
  child is spawned, committed to a lease, then `kill`ed. The live count returns
  to 0 and the next agent is admitted, **with no cleanup step run anywhere**.
- `test_a_lease_whose_holder_died_before_spawning_is_reclaimed` — a lease
  reserved by a process that died before `Popen` is swept, closing the window
  between reserving a slot and having a pid to hand it to.
- `test_a_corrupt_lease_cannot_wedge_the_budget_shut` — an unparseable lease is
  dropped rather than believed forever.

So the bound does not degrade into an outage, which the hypothesis listed as a
way of holding the cap while still failing.

### Non-blocking, which the hypothesis also named

`test_refusal_is_not_a_wait` asserts admission returns in under 0.5s when full.
Blocking is the tempting alternative and it deadlocks this exact topology:
parents holding every lease, each waiting on a kid that cannot be admitted
until a parent finishes. The bound degrades to *fewer agents*, never to a stall.

### What this experiment does NOT show

- **No pi agents were spawned.** The processes are `python3 -c 'time.sleep'`
  and the harness is the admission path, not the loop. The claim proved is
  about the bound; a live run at cap 5 is the separate confirmation and has
  not been done yet.
- **Fairness is unmeasured.** At cap 1 only two of twenty-five admissions
  succeeded, which is the bound working, but nothing here says the refusals
  were distributed evenly across spawners. A parent starved of every slot
  would still satisfy every assertion above.

<!-- THOUGHT:BEGIN — authored, not derived; carried across regenerating scans. The reasoning behind THIS version. -->
The negative control is the part of this experiment that was not in the brief
and is the reason it can carry a `proved`. Without it, "peak never exceeded 5"
is consistent with a harness that never got five processes running at once for
reasons having nothing to do with the code under test. Running the identical
rig at a cap of 999 and watching it reach 24 turns the other three rows from
observations into a comparison.

Recording the two limits explicitly, rather than only the results, because
`goal:g4.8`'s falsifier is about a live run of parents and kids and this is
not that. The bound is proved; the loop at cap 5 is not yet observed, and a
verdict that blurred those would overclaim in exactly the way this project's
evidence gate exists to prevent.
<!-- THOUGHT:END -->