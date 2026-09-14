---
id: doc:l4-formation-2-texas-two-step
mint_id: 42e5150cdcc34c7685f9939a362c1b2e
type: doc
parents:
  - goal:g15
next_edges: []
edited_by: sanctuary-master
origin: doc-version
scaffold_hash: 9f8e63a970fbb9cd
season: 2
tags:
  - formation
  - sanctuary
  - owner-verbatim
title: "Formation 2 — the Texas two-step: two director-kids on one brief, point + helper, under the Prime"
town: core
---
<!-- BODY:BEGIN -->
# doc:l4-formation-2-texas-two-step

## Owner text (the verbatim quotes that define this formation)

The base it stands on — survival mode, one Prime + one director:

> "Also for the next round we will still start small and use our survival mode arrangement where it's just the Prime and a single director-kid aimed at a loop brief as we can't be risking having our subscription getting cratered due to a dozen agents all running on it before they're all dialed in properly. That can be the survival mode: only two persistent seats active each helping the other to conserve the resource that matters most. They can drop down to ultimate survival where Prime is powered by opus and single remaining director runs off sonnet or even openrouter." (doc:l4-owner-decisions L265)

The order that made it a formation:

> "Let's gently dial up the concurrency: spawn a second director kid and let them collab together to split the work. Act after the workflow finishes. Let the current director take point though and the other one is like a helper to the first. Call it the Texas two step formation, goes under sanctuary goal as subgoal" · "And it's a new loop reset director kid generations" · "Helper director kid runs sonnet btw." · "Sonnet max effort just in case it wasn't clear" (goal:g17.1 L26)

> "also since this is just enhanced survival mode the director-kids aren't assigned a specific goal just the lead director gets the brief and splits the workload between himself and the helper director as they each get their own worktree and can merge at the end when both done. It's not a specific goal as the briefs right now go over more or less full system refactors and expansions. Once the actual persistent director system is up then they'll get pinned to a goal, for now they're free floating the way masters and keepers will be kinda free-floating. They're like the Council, the Keep, and the Masters all rolled into one role since this is survival mode" (goal:g17.1 L28)

How it runs — cheap parallel dispatch, terse reporting, verbatim relay:

> "We have two directors, one point and one helper, and the helper hasn't done anything, and I think a good few hours. So if we could dial up the concurrency of pie [pi] parents, that would be great because those are extremely cheap." (doc:l4-owner-decisions L541)

> "go for parallel rounds" · "always prefer dispatch over not" · "always" · "so you can parallelize properly" (goal:g17.1 L57)

> "That's a new standing order for all directors under the prime in survival mode" (goal:g17.1 L105)

> "You can relay this to prime as my input. Owner input warrants a message to Prime always in the two-step formation. Relay all verbatim" (doc:l4-owner-decisions L573)

Its place in the sequence:

> "Then under that town you have different formations. First it’s just Prime only. Then it’s the Texas two-step, then hybrid with gradual expansion. Then full activation but we aren’t ready for that yet. Each one helps bootstrap the next gradually so no one agent has to take on too much too suddenly, other than prime, who had the whole weight on his shoulders in season 1." (doc:l4-owner-decisions L775)

## The formation

```
owner ── types to the Prime, OR to either director seat (relayed verbatim up, always) ──┐
                                                                                        ▼
belam (Prime, Opus) ── the loop brief · rows/spawn · merge-up review · KEY floor · suite window
  └── sanctuary-director  = POINT  (receives the brief, splits the list, keeps half, merges at the end)
        └── sanctuary-helper = HELPER (claude-sonnet-5, max effort; takes the other half)
              reports done / blocked to the POINT only — the Prime never hears the helper
  each seat: its own session worktree · its own pi parents, several at once (cheap) · no owning goal
  upward traffic: a merge-up (numbers), a Prime-only decision, a rotation line, a red merge, a rule change
```

Prime/SM reading: two persistent Claude seats plus one Sonnet helper is the whole active set; every other post idle. Neither director is pinned to a goal — goal:g17.1 records the formation, nobody owns it (L28 above). The point is the helper's Keep: director-to-director talk is otherwise forbidden, and this is the one sanctioned exception (goal:g17.1 L41). Work lands per seat on `seat/<name>@s2` branches and is merged by the point at session complete, never per rotation (goal:g17.1 L53); grid commits run only on the season branch after that merge (goal:g17.1 L55).

## What it bootstraps in the next (doc:l4-formation-3-hybrid-gradual-expansion)

Prime/SM reading, each item traceable to a line above or in the sources:
- **The two-seat split-and-merge is the atom F3 repeats.** A master handing a brief to ONE director, who works in its own worktree and merges up for review by name, is the point/helper shape re-pointed one rung up. F3 was declared as exactly that: "a single director to do their bidding" per activated master (doc:l4-owner-decisions L765).
- **The relay path became the figure-eight.** Owner input entering at a director seat and reaching the Prime verbatim (L573) is the upward half of F3's loop — directors "circle around in a figure eight towards you, reporting their completion status" (doc:l4-owner-decisions L765).
- **The report rule is now standing for every director** (L105), so each F3 director arrives already bound to numbers-only merge-ups and reads-the-bytes review.
- **The helper seat survived as the first specialised post.** F3 opened by pulling the helper down (doc:l4-owner-decisions L725) and the same night the owner offered to keep him as director-review: "if you wanted to leave the director-helper up, you could make him your director-review and send mur's to him to execute and review the consolidate/verify workflow for you" (doc:l4-owner-decisions L729) — the Prime took it (L731). The merge-up review being run by name through the workflow router was itself a two-step ruling (goal:g17.1 L263).
- **Rotation as a monitor, not a memory.** The helper missing its own meter — "also helper is not rotating they forgot to track their context meter. This too is a coin flip action that needs a monitor and automated reminder to populate into a turn once its time to rotate" (goal:g17.1 L157) — is the defect that makes every F3 post rotate on a hook, not on recall.
- **Town branches.** The rule that other towns branch off core so "the two-step works in another town" without touching core (doc:l4-owner-decisions L585) is the branch grammar F3's town masters (stream, thought) inherit.

## Status

Ran. Ordered 2026-09-09 in the L4-I plan session (goal:g17.1 L26); first split round measured 2026-09-10 (goal:g17.1 L55); parallel rounds from 2026-09-10 (L57). Ended as a formation 2026-09-12 22:2xZ when the owner ordered the helper pulled down and the Sanctuary Master stood up (doc:l4-owner-decisions L725) — the point went on answering to the Prime direct with no helper, and the helper post was re-seated as director-review at 23:0xZ (L729, L731). Season 2 throughout. The predecessor is doc:l4-formation-1-prime-only; the successor doc:l4-formation-3-hybrid-gradual-expansion.

## Sources

- goal:g17.1 L24-L44 (the formation, owner verbatim L26/L28 and the seat diagram), L53-L57 (worktree protocol, parallel-rounds order), L103-L105 (seat protocol), L157 (meter/rotation), L263 (review by name), L392 (the pull-down applied).
- doc:l4-owner-decisions L265 (survival mode base), L311/L364/L391 (survival mode GO), L541 (dial up pi concurrency), L573 (two-step relay), L585 (town branches), L725/L729/L731 (F2 → F3 transition), L765-L767 (the figure-eight), L773-L775 (the formations order).
- goal:g15 (parent; the sanctuary goal the owner named as the formations' home).
- doc:l3-command-ladder-brief L338 (the 2026-09-08 owner text that began survival mode).
<!-- BODY:END -->
