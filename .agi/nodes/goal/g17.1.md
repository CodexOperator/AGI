---
id: goal:g17.1
mint_id: e4b3e68394164a47847333d1929c70df
type: goal
parents:
  - goal:g17
next_edges: []
edited_by: belam-S1-L4-I
goal_id: G17.1
goal_kind: subgoal
heading_level: 3
origin: goals-doc
scaffold_hash: a9c65ef0496021ea
season: 2
seeds: []
status: active
tags:
  - goal
  - subgoal
thought_session: rc-L4-I
title: "G17.1: The Texas two-step formation — two director-kids on one goal: point + helper"
---
<!-- BODY:BEGIN -->
**Two director-kids in formation under enhanced survival mode: one takes point, the other helps; neither is pinned to a goal yet.** Ordered by the owner on 2026-09-09 as the first deliberate step up from survival mode's single director, and the shape every later concurrency increase copies.

**Owner, verbatim (2026-09-09, in the L4-I plan session):** "Let's gently dial up the concurrency: spawn a second director kid and let them collab together to split the work. Act after the workflow finishes. Let the current director take point though and the other one is like a helper to the first. Call it the Texas two step formation, goes under sanctuary goal as subgoal" · "And it's a new loop reset director kid generations" · "Helper director kid runs sonnet btw." · "Sonnet max effort just in case it wasn't clear"

**Owner, verbatim (2026-09-09, later the same session):** "also since this is just enhanced survival mode the director-kids aren't assigned a specific goal just the lead director gets the brief and splits the workload between himself and the helper director as they each get their own worktree and can merge at the end when both done. It's not a specific goal as the briefs right now go over more or less full system refactors and expansions. Once the actual persistent director system is up then they'll get pinned to a goal, for now they're free floating the way masters and keepers will be kinda free-floating. They're like the Council, the Keep, and the Masters all rolled into one role since this is survival mode"

```
FORMATION   point  = sanctuary-director (L4 gen I; the lead: receives the brief from the Prime, splits the workload between itself and the helper)
            helper = sanctuary-helper (L4 gen I, claude-sonnet-5 at max effort — owner; answers to the point, never to the Prime)
GOALS       NEITHER is pinned to a goal in enhanced survival mode (owner) — owning_goal is empty on both rows until the persistent director system is up;
            this sub-goal RECORDS the formation, nobody owns it. In this mode a director is the Council, the Keep and the Masters rolled into one role (owner).
WORKTREES   each director works in its own tree: .agi/worktrees/seat-sanctuary-director (branch seat/sanctuary-director@s2) · .agi/worktrees/seat-sanctuary-helper (seat/sanctuary-helper@s2)
            both off season/s2; MERGE at the end when both are done (merge, never rebase; compare against the MERGE-BASE, never a moved season/s2); the point merges
SPLIT       the point splits the round's work list, hands the helper its half, keeps its own; each dispatches its own pi parents (one round at a time, hard ceiling each)
REPORT      helper -> point (done / blocked, per item) ; point -> Prime (the round's review) ; the Prime never hears the helper directly
RULES       unchanged for both: assignment IS the node's testable_claim · commit + push the brief before dispatching at it · check the KEY not the account · $1.00 floor never lowered
            write.py for every node write · never wake another seat · never write config:seats (bank it for the Prime) · never delete a node
EXCEPTION   director-to-director talk is otherwise forbidden (channel A via the Keep) — in this formation the point IS the helper's Keep, by the owner's order
```

Done when: one round has been split, dispatched by both seats from their own worktrees, merged by the point into season/s2, reviewed by the point and accepted by the Prime, with the helper's spend and node count recorded here.

<!-- THOUGHT:BEGIN — authored, not derived; carried across regenerating scans. The reasoning behind THIS version. -->
Version 2, 2026-09-09: the owner's clarification folded in verbatim — free-floating directors in enhanced survival mode (no owning goal until the persistent director system), one worktree each, merge at the end, the point is the helper's Keep. Seat rows and worktrees updated in the same commit.
<!-- THOUGHT:END -->

## Agent Notes
Owner, verbatim (2026-09-09): "also old worktrees that've been exhausted and aren't used anymore should be cleared out once the work is verifiably merged into whatever parent worktree owns it. So we don't develop a giant list of worktrees over time" — applied the same hour: 23 merged+clean L3 loop worktrees removed with their branches (git worktree remove + git branch -d, which refuses an unmerged branch); 4 merged-but-dirty and 5 unmerged (ahead=1) trees kept for review. Standing rule for the point director: prune a worktree only after its branch is an ancestor of the parent branch.

Owner, verbatim (2026-09-10 00:2xZ): "we should mint fresh worktrees per seat session and then merge them in and delete them as part of session complete after no actionable items left, not per rotation." — applied: .agi/worktrees/seat-sanctuary-director and seat-sanctuary-helper are the two seats' SESSION worktrees for this loop (branches seat/<name>@s2, minted 2026-09-09, fast-forwarded to 48575827f); a rotation (gen I -> II -> ...) continues in the SAME worktree; at session complete — no actionable items left — the point merges both into season/s2 (merge-base, never rebase) and deletes both worktrees and branches. Never per rotation.

Seat-worktree protocol, measured by the point in round 1 (2026-09-10): grid.py commit --all REFUSES on a seat branch (node refs are branch-blind: "merge to master first or pass --allow-branch"). Rule: never pass --allow-branch; on a seat branch a step ends at git commit + git push; grid.py commit --all runs ONLY on season/s2 after the point's merge. Round 1 point slice: 14 sub-goals (g5.3, g5.4, g9.11, g17.2-g17.12 with nesting to heading level 5, first use in this graph) on seat/sanctuary-director@s2 at dc1974a59, zero dispatches by documented judgement (exact structure, a wrong parent can only be deprecated), key untouched; chain round (idea -> hypothesis per sub-goal) ordered next.

Owner, verbatim, 2026-09-10 (to the Prime in chat): "go for parallel rounds" — the one-round-at-a-time rule is lifted for the formation: rounds run concurrently across and within both seats, several pi parents at once, inside the standing bounds (KEY checked before every dispatch, $1.00 floor, stop under $2.00, spawn budget 25 live, hard ceiling per parent, $3.00 key per round). Owner, verbatim, the same night (to the helper directly, relayed by the point and banked by it in doc:l4-owner-decisions): "always prefer dispatch over not" · "always" · "so you can parallelize properly" — the rule for work not yet done; work already landed and verified is not re-derived (point's reading, accepted by the Prime). Measured trap (point): dispatch.py refuses a non-numeric iteration suffix (L4.20b -> invalid iteration_id, fail-closed) — use L4.NN; ad-hoc rounds are numbered beyond the plan's L4.27.

Seat-worktree protocol, two more facts measured by the point in L4.02 (2026-09-10): (1) agent session dirs land in the MAIN checkout's .agi/sessions/iter-<id>/, not in the seat worktree — a seat harvesting its own round reads /home/ubuntu/work/agi/.agi/sessions/iter-<id>/ (its own tree holds only its p.log); (2) trap 0n reproduced: dispatch.py prints 'reaper: finished' while the parent is still alive — the reaper giving up is not the round ending; harvest off spawn_budget.py status. Also L4.02: a claim whose conjuncts contradict (schema-derived gate AND tests unchanged) was disproved by the kid with a clean-room reproduction; accepted lean_disproved:80, claim corrected IN PLACE (a version is a grid commit, no @v2), re-dispatched as L4.32.

STANDING RULE until L4.10 lands (point + helper, 2026-09-10, verified in the bytes: send.py:406 and :507 call _nudge_window(None, ...) with no test guard): a kid must NEVER run test_send.py unguarded while live seats exist — the fixture nudges REAL tmux windows on this box, and fixture text landing in the Prime's pane reads as a seat's message and can pollute the owner's conversation. The reproduction of L4.10 is READING those two lines, never firing them. The fix monkeypatches _nudge_window AND the comms root before any assertion runs. Corollary: neither seat runs the full suite without telling the Prime first (collision AND nudge risk); the Prime captures its own pane after any suite run.
