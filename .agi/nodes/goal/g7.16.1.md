---
id: goal:g7.16.1
mint_id: 78b3255532744b4fa8e13c02cec6609f
type: goal
parents:
  - goal:g7.16
next_edges: []
confidence: 0.6
edited_by: belam
goal_id: G7.16.1
goal_kind: subgoal
heading_level: 3
origin: goals-doc
scaffold_hash: 85dbe599464d7a10
season: 2
seeds: []
status: active
tags:
  - formation
  - council-loop
title: "G7.16.1: The council loop -- directors build the graph directly, a sanctuary master reviews, a three-lens council re-bundles (local-town)"
town: core
---
# goal:g7.16.1

# goal:g7.16.1

## Why this exists
goal:g7.16 (formations): the owner, 09-29 09:3x-10:1xZ (verbatim below), set a new run mode for local-town / local-maxxing: directors build the graph directly (no parent/kid dispatch), a sanctuary master reviews, a three-lens council reviews and re-bundles. What made it a leaf of g7.16: formations are subgoals nested under g7.16, each carried by a template build node, and choosing a run mode = activating one template and deactivating all others in the same call (owner 10:1xZ). Measured context: the 04:50Z 09-29 reboot (systemd-oomd 67 kills, then the sanctuary-health watchdog) came under the parent/kid pi load; the pi-free lane was dead 20:0xZ-04:0xZ.

## Target end-state
- Seats on local-town, town local-maxxing, all claude-code on claude-opus-5-5, effort high: belam (Prime) · sanctuary-master · director-general-1 (goals + hypotheses) · director-general-2 (experiments + verdicts) · director-general-3 (MVPs + build nodes + tests) · council alive · all-is-one · self-perpetuating (each embodies ONE vision node, not the others). thought-master, director-thought, director-engine are down and stay down.
- The loop: the council checks the bundle and modifies it after discussion -> director-general-1 -> -2 -> -3 grow the graph and run the tests -> sanctuary-master reviews (standard mur on claude-code Opus 5.5 high) and returns residues until clean -> the council reviews the completed bundle (batched mur in chunks, then one manual review per vision lens, in a group chat) -> the next bundle.
- Order of work: (1) the current town bundle, first; (2) grok's work on core/season2/main and core/main (probably overbuilt: simplify); (3) ONLY when nothing is left to simplify in (1) and (2): wind season 2 down -- grow the graph out to the nodes that let overview nodes be written (outcomes -> bigger outcomes -> overviews) and hand them to the Prime.
- Whatever machinery the formation lacks (formation templates as build nodes, the activate-one-template call, the post stand-up/take-down skill) is built by the directors as part of the town bundle, in dependency order.
- Chain growth may use the build-mode parent sets that include ideas (a build node on [goal, idea]).
- Measured over a few loops: does the council materially improve the results; the Prime reviews season 2's result by embodying the five morals.
- Stop around noon ET 09-29 (16:00Z) if still active.

## Invariants
- No parent/kid dispatch while this mode runs; every node is written through write.py.
- One director works a given bundle at a time (the chain order above).
- Only the Prime merges into season2/main (skill agi-merge-pass).

## Falsifier
1. `python3 extensions/agi/bin/spawn_budget.py status` lists no tier=parent or tier=kid spawn while the mode is active, and config:posts rows of the eight seats read box local-town + model claude-opus-5-5.
2. Negative: `git log --since=2026-09-29T10:30Z --format=%s | grep -c 'dispatch.py'` prints 0.

## Out of scope
goal:g7.16 (the umbrella: its retitle and the two-step formation's own subgoal are director-general-1's) · goal:g1 (PASS residues)

## Agent Notes
Assigned to **belam**.

## OWNER 2026-09-29 09:3x-10:1xZ, verbatim
"Message didn’t deliver I don’t think due to failure of your post not being stood up. Might need to stand it up first. But also do we not have a fix for this? If not, what if we have the directors writ the actual graph directly as a trial to see if it can work after that way. I have a lot of subscription left and not a lot of time. I’d rather stand up the core council but on local-town and local-maxxing branch. Then as the town board completes, I’d like them to review it in a group chat by each embodying one of the vision nodes specifically, not including the other, and re-dispatch new board bundles for further simplification or refinement. I’m fine to have it loop autonomously until I hit 85% of my CC subscription use, currently at like 10 or 20%. Let me know if this plan makes sense. Basically skip the parents and kids and let directors build directly. In this way we could stand up a few directors even, all designated as director-engine-1,2,3. Maybe start with 3 directors, one sanctuary master, and 3 core council members who embody the vision nodes. Council reviews results once the directors finish their board using graph building skills, and we can have one director responsible for goals and hypothesis minting, one for doing experiments and verdicts, and one for doing MVPs and build nodes. Set up templates and configs as needed before standing up. Let me know if the plan makes sense or if you need anything else."

"We are trying the following loop: bundle is checked by council, modified after discussion - bundle handed off to first director and the chain grows through the rest - directors do all their graph growing and tests when done - hands the completion to the sanctuary master for review. Sanctuary master runs review using standard mur but on CC opus 5.5 high as it should be way less reviews and sends back any residuals and this loops until done. Then the completed bundle is given to the council for review using the batched mur process in chunks, then another manual review through the vision lenses. They should also try to wind down season 2 and go through building up all their outcomes and bigger outcomes and overviews before handing those off to the prime or pause of CC sub hits 85% first."

"You can lean on more of the CC internal tooling like messages etc until the redesigns are more build up and robust."

Answers to the Prime's five questions (1 council = alive / all-is-one / self-perpetuating · 2 the current seats · 3 the 85% stop · 4 bundle 1 · 5 models Opus 5.5 high): "1. Yes 2. de and dt and TM go down. SM comes up. Three other general directors come online, director-general-1, 2, and 3. Each responsible for their portion of the graph growth. 3. Just stop around noon if still active by then in EST 4. Current set then keep going from there. There are likely many parts of the system that could use a pass. They could also check what grok has been doing on the core/season2/main and core/main repo branches and see how that could be improved. 5. Yes."

"Also we must try to close season 2" · "So all the nodes we need to build to close a season mainly the ones needed to finally write overview nodes" · "Need a post stand up/takedown skill"

"Goal g17 is stale strike that wherever you found that reference. We nest more now. Also the bundle currently up is priority. Then season close. But only if the bundle has no optimizations or reductions in complexity left. If absolutely nothing left to simplify based on bundle and related grok stuff then wind down the season by growing graph out to overview nodes. But only after town bundle and core branch stuff is done. It’s probably way overbuilt on core. Just see what the overall flow yields over a few loops. That’s the key part. Does the council materially improve the results, and can you improve it further by truly doing your job of embodying the five morals as you review the result of season 2."

"Formations that are live are under .geometry,  while having formations overall should be a goal like 7.16, then the formations themselves as subgoals nested under 7.16. They can go straight into template build nodes, and picking a run mode is just a matter of setting a specific template active, setting all others inactive as part of that call. But again have directors build this if needed for whatever is missing as part of the town bundle but following the dependency queue" · "Use build mode parent sets that can include ideas as your path to shortcut chain growth."

OWNER 16:5xZ 09-29, verbatim (Prime pane): "let the team know we can Keep working till 7pm next and I'll check my CC sub then" -- the council loop resumes after the 16:00Z stop and runs to 23:00Z (7 pm EDT); the next bundle per this goal's order = grok's core simplify.

OWNER 17:3xZ 09-29, verbatim (Prime pane): "Go ahead and retire GOALS.md. We don't need it anymore stop bothering with it or the render byte round trip script" -- handed to the council as a bundle-3 simplification row (verify goals-check, driver --smoke render, snapshot-goals.py --render/--check, CLAUDE.md + skill citations); GOALS.md itself retires in git history, never hand-deleted mid-bundle.
