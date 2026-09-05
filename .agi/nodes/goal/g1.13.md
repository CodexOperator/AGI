---
id: goal:g1.13
mint_id: 342e5f9d459f493da11c73fa2dcbab24
type: goal
parents:
  - goal:g1
  - build:COMPLETE.md
next_edges: []
confidence: 1.0
edited_by: director
goal_id: G1.13
goal_kind: subgoal
heading_level: 3
origin: goals-doc
scaffold_hash: 6ec14427d97ab1b5
seeds:
  - build:COMPLETE.md
  - build:CLAUDE.md
  - build:bin-snapshot-goals
  - build:tests-test-snapshot-goals
status: horizon
tags:
  - goal
  - subgoal
thought_session: L1.13
title: "G1.13: A loop ends with a completion report, and the report is generated, not remembered"
---
# goal:g1.13

## Agent Notes
**Owner ask, 2026-09-04.** `HANDOFF.md` is the bridge *between* sessions and is
replaced wholesale. Nothing closes a loop. So a loop ends with its gaps written
in prose that the next director deletes, and the same gaps come back — measured:
16 hazards carried out of L1 in a handoff table became `goal:s34`, and of them
roughly two closed.

**A completed loop writes `COMPLETE.md`.** Standing shape:

1. What ran — waves, dispatch counts, harness, spend.
2. The scoreboard — node counts, primary metric, evidence fraction, suite, links.
3. **Per active goal, how far it got**, grounded in commits and node diffs rather
   than recollection.
4. **How many goals actually closed**, and any `complete` marking the report
   cannot substantiate (L1 found one: `goal:g4.6` was marked complete two days
   before the adapter existed).
5. **For everything that did not close, a completion-failure category** —
   saturation, ceiling-found-by-dying, late minting, hazard carry-over,
   banked-to-owner, verification blindness, attribution void. A decision banked
   to the owner counts as a failure here: not the model's, the harness's, for not
   giving the director enough to decide with.
6. What was minted or changed in response, linked as graph edges.

**`COMPLETE.md` is a payload, `HANDOFF.md`'s peer, and the opposite of it in one
respect: it is never replaced.** A loop appends its section; the grid versions
it; `GOALS.md` stays the tracker.

**The end state is that none of this is prompt text.** Today the shape lives in
`skills/agi/SKILL.md` and a director follows it. The categories above are exactly
the kind of judgement a small classifier can make over a parent's report and a
goal's diff — see `goal:g14`. This goal is the scaffold that makes that training
data exist in a fixed format.

Falsifier: two consecutive loops close with a `COMPLETE.md`, and the second one's
carried-hazard list is shorter than the first's rather than a copy of it.

CORRECTION 2026-09-05, owner: COMPLETE.md is NOT append-only. It follows the same rule as HANDOFF.md -- replaced whole by default, appended only when the owner asks, which they do when the next loop continues directly off the last one and both reports must be readable at once. The body above says never replaced; that is wrong and the rule here supersedes it. Replacing is safe for the reason it is safe for the handoff: grid.py payload build:COMPLETE.md --version N returns every prior report, so accumulation costs future context and buys nothing.
