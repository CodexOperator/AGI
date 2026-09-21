---
id: verdict:the-bound-is-structural-now
mint_id: ecd72eedace74054b6725a498a138584
type: verdict
parents:
  - experiment:lease-bound-under-five-spawners
next_edges: []
confidence: 0.97
edited_by: season.py
evidence_runs:
  - experiment:lease-bound-under-five-spawners
scaffold_hash: 01f83522f862b78d
season: 1
thought_session: season
title: A bound in shared state holds the tree; a bound in a number never could
verdict: proved
---
# verdict:the-bound-is-structural-now

## Verdict

proved

## Evidence

`experiment:lease-bound-under-five-spawners` ran five independent OS processes
through one lease directory, five slots each — 25 would-be agents — at caps of
1, 3 and 5, plus a non-binding control:

| cap | admissions | peak live |
|---|---|---|
| 1 | 2 | 1 |
| 3 | 5 | 3 |
| 5 | 10 | 5 |
| 999 (control) | 25 | 24 |

The peak **equals** the cap in every bounded run and never exceeds it. The
control, running the identical harness at a cap that does not bind, admitted
all 25 and peaked at 24 — so the bounded rows measure the bound rather than an
accident of the rig.

Twelve tests in `test_spawn_budget.py` and three in `test_dispatch.py` carry
the falsifier, including the two disproof conditions the hypothesis named:
reclamation without a cleanup step (a `kill`ed agent's slot returns), and
non-blocking refusal (admission returns in under 0.5s when full, so the
parents-hold-every-lease deadlock cannot form).

## What is proved, at the level it actually holds

**A concurrency bound must live in shared state mutated at the spawn site, and
one that does holds the whole tree.** `spawn.parallel` bounds one invocation's
slots and cannot bound grandchildren, because a parent gets its kids by running
`dispatch.py` again and that second invocation reads its own copy of the same
number. `experiment:a00-5f927203-8a66a2` disproved the alternative — a parent
carefully *enforcing* the number — and this proves the replacement.

The mechanism is one lease file per live agent, created under an exclusive lock
over the lease directory immediately before `Popen`, reclaimed by liveness
rather than by any release path. There is no separate grandchild code path to
bound: **the same admission path entered twice is the entire fix.**

## What is NOT proved — read this before citing it

- **`goal:g4.8`'s falsifier is not satisfied by this node.** That falsifier
  requires two parents on the parent model spawning real kids on the kid model,
  both completing, with four clauses of which this proves one. **Clause 2 — the
  live process count never exceeds the declared bound — is proved. Clauses 1, 3
  and 4 are untouched here.**
- **No pi agent was spawned.** The processes were sleeping interpreters. A live
  run at cap 5 is a separate confirmation and has not happened.
- **Fairness is unmeasured.** At cap 1, two of twenty-five admissions
  succeeded. Nothing here says refusals were spread evenly, and a parent
  starved of every slot would satisfy every assertion above.
- **The cap is a policy, not a finding.** 5 is the owner's number for this
  session. Nothing measured says 5 is right; what is measured is that whatever
  number is declared is the number that holds.

## Consequence for the loop

`spawn.parallel` may now be raised past 1 without the population becoming
unbounded — which is what `goal:g4.8` item 3 was blocking. The two remaining
in-flight items are the parent brief (`goal:g1.9` owns it) and completion as a
graph event (`goal:g4.6`'s fourth falsifier).

<!-- THOUGHT:BEGIN — authored, not derived; carried across regenerating scans. The reasoning behind THIS version. -->
The "what is NOT proved" section is longer than the evidence section on
purpose. This node is going to be cited as the reason it became safe to run
five parents, and the gap between "the admission path bounds a population of
sleeping interpreters" and "`goal:g4.8`'s falsifier is satisfied" is exactly
the gap a downstream reader will close by accident if nobody writes it down.
This project has already had a `proved` @0.99 sit unevidenced because a report
described a field the node did not contain; overclaiming at the verdict is the
same failure one tier up.

Confidence is 0.97 rather than 0.99 because the mechanism is proved against
processes that do nothing. Real agents take longer to start, die in more ways,
and can be `SIGSTOP`ped — a stopped process is alive to `os.kill(pid, 0)` and
holds its slot forever, which is correct behaviour and might still be a
surprise at cap 5.

Naming the cap as policy rather than finding, because the alternative is a
future reader treating 5 as measured. It is not. What is measured is that the
declared number is the number that holds.
<!-- THOUGHT:END -->