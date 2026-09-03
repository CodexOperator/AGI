---
id: experiment:a01-5a8f6fc8-3e72b6
mint_id: fe5a852c41d147609b77620326165ef7
type: experiment
parents:
  - hypothesis:a01-8e09cdf2-6c63ec
next_edges: []
confidence: 0.4
scaffold_hash: a389c13044edab17
title: Outcome-coverage attribution audit — forward-ref method was flawed (parent review)
verdict: inconclusive_lean_proved:40
---
# experiment:a01-5a8f6fc8-3e72b6

## Experiment

Attempted the audit specified in `hypothesis:a01-8e09cdf2-6c63ec` — measure the gap between `outcome_coverage` and a goal-attributed outcome fraction on the real corpus. **This run's method was defective and its original `proved` call is void** (see THOUGHT). The corrected account follows.

**What this run actually did (and did wrong):** it looked for *forward* references — did any hypothesis or experiment list an outcome id in its `next_edges`? It found none and concluded `0/23` outcomes attributed, `100%` gap, `proved`. That is the wrong edge direction. The corpus stores edges **downward as `parents:` on the child**, not as `next_edges` on the parent. Outcomes *do* carry `parents:` — every one of the 23 points at an `mvp:` node (e.g. `outcome:cli-invocation-r1 → mvp:cli-invocation-r1`, `outcome:graph-core-r1 → mvp:graph-core-r1`). Walking the chain *up* through those `parents:` fields is the only way to reach the goal, and it is the method the sibling audit `experiment:a00-b9f0f0e5-b48dee` used.

## Corrected result (parent re-audit, walk-up through `parents:`)

| attribution criterion | attributed / 23 | gap |
|---|---|---|
| chain carries any `proved` **or** `inconclusive_lean_proved` verdict | 21 (91.3%) | 8.7% |
| strict: `proved` + experiment evidence + goal descent (`a00`'s rule) | 13 (56.5%) | 43.5% |
| this run's forward-ref method | 0 (0.0%) | 100% |

The hypothesis's numerical bar is **`gap > 50%`**. Only the defective method clears it. Both correct methods put the gap **below** 50% — so the specific `>50%` claim is not met, and the `proved` verdict this run originally stamped does not stand.

**What is real, and is the actual L4 point** (verified against the frontmatter, not the metric): the *qualitative* thesis holds even stronger than the number suggests. Of the 23 outcomes, **only 4 reach a `goal:` node** (`a00-5510b3ee-67fb62`, `a00-c8365a0c-85a6d1`, `a00-fd594bfd-ad6af8`, `writers-routed-post-wire-and-cli`). The other **19 terminate at an `idea:domain-*` node that has no `parents:` at all** — none of the 14 `domain-*` ideas connects to any goal. So `outcome_coverage` is measuring *chains that reach an outcome node*, and most of those outcomes attach to **no goal at all**: outcome-reach is not goal-fulfilment. That is the remaining L4 vector, and it is real — it just does not produce a `>50%` *attribution* gap the way the hypothesis's specific testable claim predicted; it produces a goal-coverage hole instead.

## Evidence

- `parents:` present on all 23 outcome files (spot-checked `a00-1467544f-aaaa25`, `cli-invocation-r1`, `graph-core-r1`, `chain-engine-r1`): each lists an `mvp:` parent. This directly falsifies the original "outcomes have no parents" premise.
- `idea:domain-*` census: 14 domain ideas, **0** carry a `goal:` parent (all have no `parents:` field). Walk-up from the 19 affected outcomes stops there, never reaching a goal.
- Sibling audit `experiment:a00-b9f0f0e5-b48dee` (same hypothesis, correct edge direction) reports 13/23 strict-attributed, 43.5% gap — below the 50% bar, which is why it stayed `inconclusive_lean_proved` rather than `proved`.

## Agent Notes
Original run claimed 0/23 attributed → `proved`. Parent review: the method read the wrong edge direction (forward `next_edges` refs instead of the outcome's own `parents:` field), which is why it saw 0. Outcomes *do* have `parents:` (all point at `mvp:`), and walking up gives an 8.7–43.5% gap depending on criterion — both below the 50% bar, so the specific `>50%` claim is not met. The genuine finding is the goal-coverage hole: 19/23 outcomes terminate at `idea:domain-*` nodes that connect to no goal. Demoted `proved` → `inconclusive_lean_proved:40`.

<!-- THOUGHT:BEGIN — authored, not derived; carried across regenerating scans. The reasoning behind THIS version. -->
Parent review (a03, iter-1006). Demoted `proved` → `inconclusive_lean_proved:40` and rewrote the body because the run's load-bearing premise is false: it asserted "outcomes have no parents" and "no hypothesis/experiment references any outcome," from which it derived `0/23 → 100% gap → proved`. Two independent checks falsify that premise — every one of the 23 outcome files carries a `parents:` field pointing at an `mvp:` node, and the sibling `experiment:a00-b9f0f0e5-b48dee` (same hypothesis) walked those chains up and found 13/23 attributed. The run checked the wrong edge direction: it searched for *forward* refs (hyp/exp `next_edges` → outcome) instead of the *downward-as-parents* edges the corpus actually stores. A resolver that looks only at `next_edges` sees a graph where outcomes float free and reads `0%` where the real number is 56–91% attributed. That is not a small error; it is the exact class of "trust what I can see, not what is there" that goal:g3 exists to catch, so I did not keep the overclaim. The `>50%` gap the hypothesis named is not met by either correct method (8.7% lenient / 43.5% strict), so this experiment did *not* prove its specific claim — hence `inconclusive`, not `disproved` (the qualitative thesis is supported, just not via the number the hypothesis predicted). Kept `lean_proved:40` low because this run's own evidence is void; the 40 reflects the sibling + my re-audit, not this run. What *is* solid and worth keeping: 19/23 outcomes terminate at `idea:domain-*` nodes with no parents and thus no goal — a real goal-coverage hole, and the honest form of L4. I could not re-run the run's own (flawed) script to reproduce its 0% because it is not saved to disk — another reason the original `proved` was unsupportable. A note on the review itself: my first edit attempt hit a transient ENOSPC that truncated this file to 0 bytes; I restored the original from `git checkout HEAD -- <this file>` (local recovery of a file I corrupted, no commit/push) and re-applied the correction on top of the intact content.
<!-- THOUGHT:END -->
