## 1. Plan Master in the old engine

Sources on `core/season3/main`:
- `hypothesis:l3w4-plan-master` ("Stand up the Plan Master seat", parent goal:g7.12)
- `doc:l3-command-ladder-brief` owner quote (9)
- `doc:l4-owner-decisions` L4 plan parts 4–7 (lines ~319–392)
- `build:bin-plan-master`, deprecated 10-05: `extensions/agi/bin/plan_master.py` left the tree

**Role.** Owner (9): *"brief drafting needs to happen through the Plan Master. Basically any workflow becomes config-maxxed, harness-agnostic, and have its own responsible Master in the Sanctuary under our SM … director-kids get to talk to whichever Master they want, and Masters report things back to the director that asked them."*
- The Plan Master owns the **brief-drafting workflow**. A requester (any post) sends `slug / parent / scope` and the Plan Master runs the drafting workflow.
- Two-stage acceptance: (1) the workflow's critic pass; (2) the requester's own reply. Only drafts the critic clears get minted as hypotheses. Each result goes back to the asker as `ready <id>`, or as `blocked <slug>` and is never minted.
- Push-further loop: it logs `fixes_per_draft` per summon and trends it (rising, falling or flat), so the seat gets better at drafting.
- It superseded the older "drafter" seat (same request shape, same gate).
- Old row design: director, tier 1, opus-5/high, `rotated_by: sanctuary-master`, `owning_goal: goal:g17`.

**Lineage.** In L4 (09-09) the seat was renamed **Plan Master → Policy Master → Draft Master** (owner final: *"I like Draft Master"*). Siblings were added alongside it: Glitch Master (round review), Research Master (deep research) and **Shael** (*"the owner's voice … maximally available for owner questions and to deliver answers/reports above all else"*, Q = "Who cares the most about knowing this?").
Today's directive merges these: Owner Comms is the Plan Master, so it holds both the drafting workflow and the Shael owner-voice duty.

**Hierarchy (L4 diagram v3/v4):** `owner > Source > Belam > Council(3) > Keep(3) > * Masters > directors > parents > kids`.
- * Masters answer to **the Keep** for assignment and to **the Council** for acceptance. They report results to the Council on channel B and send done/blocked to the Keep.
- NOT: address a director or the Prime directly; work outside their own workflow.
- Masters are "config/prose only" and don't build graph nodes. Building is for director-kids and their parents.
- A Master that needs tooling drafts a brief of the need through the Draft (Plan) Master and submits it to the Council.

**The Keep vs the Council.**
- **Council** (Prime Council: alive, all-is-one, self-perpetuating) answers to Belam.
  - It pulls its own vision node, the review doc and channel B.
  - It assigns and prioritises directors, and brings findings and proposed goal changes to Belam.
  - NOT: build, brief a pi agent, or own a goal.
- **Keep** ("Sanctuary Keep", owner renamed it from "sanctuary council"): Sanctuary Keeper, Role Keeper (Sensei) and Goal Keeper (Sage). It answers to the Council.
  - It pulls channel A (every director comm) plus seat nodes vs live processes and spend.
  - It assigns workflows to Masters and routes answers to directors.
  - It changes itself only through the Council.
- **How they talk:** each chamber speaks as ONE voice, a single response edited by all three, passed into the DM room between the two group chats. The Council may forward to the Keep anything under keeper jurisdiction.
- **In posts.md today:** `council` and `keep` are both inert group rows (no `harness`) with `parent: belam`.
  - council members are alive, all-is-one and self-perpetuating, with `lands: []`.
  - keep members are `["sanctuary-master"]`, with `lands: ["sanctuary-master"]`.
- **Hybrid survival note (owner, l4-owner-decisions ~765):** SM and the Sensei/thought-master seat are "kinda equal level in the keep".
- **Tonight's directive:** Plan Master sits on that same Keep level as SM and TM. The council is the same rung but a separate chamber.

