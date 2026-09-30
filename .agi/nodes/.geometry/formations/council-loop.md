---
id: doc:council-loop
mint_id: 0e5025a7e24f4e459c30e50d82b8060e
type: doc
parents:
  - goal:g7.16.1
next_edges: []
edited_by: belam
scaffold_hash: e99976c6c09553f9
season: 2
title: Council loop
town: local-maxxing
---
# doc:council-loop

# doc:council-loop — the council loop (goal:g7.16.1): one protocol for every post in it

Seated 09-29 by belam-S2-L5-XV on the owner's word (goal:g7.16.1 holds it verbatim). Local-town · town local-maxxing · MAIN (the repo root; locations.py resolves it) on `local-maxxing/season2/main` · every post claude-code, Opus 5.5, effort high.

## Posts
| post | owns |
|---|---|
| alive · all-is-one · self-perpetuating (council) | check + modify each bundle after discussion (group chat); review the completed bundle: batched mur in chunks, then ONE manual review through YOUR vision node only, never the other two |
| director-general-1 | goals + hypotheses (skill agi-goal: nest leaves under the bundle's goal) |
| director-general-2 | experiments + verdicts, and the tests they need (skill agi-verify) |
| director-general-3 | MVPs + build nodes + tests; a build node may take the [goal, idea] parent set to shortcut chain growth. Owner 23:1xZ 09-29 SUGGESTION (the directors agree the final split themselves, room directors): builds the MACHINERY that accepts the new write form (a node write = one commit on its own refs/grid/<mint>, goal:g7.16.1.6), then moves to the spawn/rotate unification (goal:g7.16.1.7) |
| director-general-4 | side by side with DG3: FILLS IN the new write form (moves the writers onto it) while DG3 builds the machinery; before that, the leftovers lane (doc:card-director-general-4) |
| director-general-5 | the spawn/rotate unification + template/config gutting and streamlining: recursive linkable templates, formation -> post -> harness -> model (goal:g7.16.1.7) |
| sanctuary-master | review each finished bundle: standard mur (agi-merge-up-review) on claude-code, model claude-opus-5-5, effort high; residues back until clean |
| belam (Prime) | merges into season2/main (PASS); reviews season 2's result through the five morals |
| stream-master (SIDE post, town streaming-suite; template doc:stream-master-brief; skill agi-stream) | keeps the live stream: the Twitch relay of the private display :2 (the 3D dashboard or the masked feed), its delay, hold / cut / off; builds and reviews nothing (owner 09-29 16:5xZ: "It's more of a side post") |

## The council's lens (owner 2026-09-29 23:3xZ, verbatim -- a quote that lives on AS the quote)
"Can we also modify their overall briefs to where they're not so focused down to earth in the nitty gritty? Their purpose is to stay higher up towards the big picture view and look at the whole system from that point of view. Somewhere I have a quote about thinking not about what the system should do right now, but how the system would work across hundreds or thousands of generations and session rotations and graph iterations and just really try to project the whole possibility timeline space forward for the graph structure and feel out and let that latent space exploration and activation guide you towards the correct shape as you also continue discussing amongst each other. A similar quote is already somewhere in the graph, but I just wanted to reiterate that's what they should be doing. They need to be looking at really the bigger picture and thinking about the essence of what the vision is that they embody and what that means. And again, you need to be trying to approach it from a really top-down perspective. Like, how can the system as a whole be just more streamlined through the lens of whatever vision I embody? And again, remember that when directors deliver their bundles and the sanctuary master reviews them and hands them back, uh, one of the things that the council should do is then look over the submitted bundle and see how it aligns to the goals and see if it's good enough to go ahead and write an outcome on as is, or if not, go ahead and adjust the goal right now and start it again for another pass. But if it is good enough, they can go ahead and write an outcome node for the goal chain. Essentially, they should write an outcome node when any further redesign involves more structural or refactoring types of changes that should be saved for the next season, while we allow bigger outcomes and overview nodes to get built up next."

```
council post = its vision, top-down, never the nitty gritty (that is the directors')
  ask: how does the WHOLE system run across hundreds / thousands of generations, rotations and graph iterations?
       how is it more streamlined through the lens of the vision I embody?  -> the shape, then discuss with the other two
the council reads the grown chain at the END of the loop below: bigger outcomes in -> new goals / bundles / nested goals out; overview nodes cap the season
```
## The loop (owner 2026-09-29 23:5xZ; verbatim in this version's THOUGHT; supersedes the per-post lines above where they differ)
```
council places the bundle (group chat) ─► DG1 goals + hypotheses ─► DG2 experiments + verdicts ─► DG3 · DG4 · DG5 MVPs + builds + tests (room directors)
directors' inner loops, until NO residue is left:
  DG2 : the MVP results vs the hypotheses ─► its own correctives as FORKED hypothesis chains off the 1+ most relevant existing hypotheses
  DG1 : then the build nodes vs the goals ─► correctives as NESTED subgoals
  DG1 : no nested subgoal / hypothesis residue left ─► finalizes the OUTCOME node for EACH goal in the bundle ([outcome].md: parent = the goal)
sanctuary-master : automated reviews (mur) through her lens ─► residues / correctives back to the directors (loop)
                   nothing left to dispatch ─► writes the BIGGER_OUTCOME nodes tying the outcomes together
council : reviews the bigger outcomes ─► new goals / bundles / nested goals, at whatever level it sees fit (loop)
          none remain ─► writes the OVERVIEW nodes that cap the season's growth ─► hands them to belam
STOP ~ midnight ET = 04:00Z 09-30 (owner: "we just keep working full steam ahead until about midnight Eastern time")
```

## Order of work (owner 09-29)
1. The current town bundle (town:local-maxxing board) — first.
2. Grok's work on `core/season2/main` and `core/main` ("probably way overbuilt on core"): simplify.
3. ONLY when nothing is left to simplify in 1 and 2: close season 2 — grow the graph out to the nodes overview nodes need (outcomes → bigger outcomes → overviews) and hand them to the Prime.
What this formation lacks (formations as template build nodes under goal:g7.16, one call that activates one template and deactivates the rest, the rest of the council-loop machinery) is bundle work, built by the directors in dependency order.

## Handoff (lean on Claude Code messaging, owner 09-29)
- `ListAgents` → `SendMessage` to the next post (it wakes that session) + ONE room line for the record:
  `python3 extensions/agi/bin/send.py --from <you> send --room council-loop '[handoff] bundle <n> · <stage> done · <node ids> · tests <n passed>'`
- A post acts only on a handoff addressed to it; one director per bundle ROW at a time -- two bundles may run side by side (owner 23:1xZ 09-29: DG3 + DG4 on the write form, DG5 on spawn/rotate).
- Council group chat: SendMessage to the other two council posts; the room carries the agreed bundle.
- Directors group chat (owner 23:4xZ 09-29: "let the directors figure out the split for the work amongst the bundles themselves. Let the directors also share a DM room, just like the council."); owner 23:5xZ 09-29, verbatim: "Oh, specifically the director generals three, four, and five get a room as they are the ones doing a lot of the heavy graph building." -> director-general-3, -4 and -5 agree the split of the graph-building work among themselves by SendMessage to each other (DG1 goals+hypotheses and DG2 experiments+verdicts keep their stages); the room `directors` carries the agreed split: `python3 extensions/agi/bin/send.py --from <you> send --room directors "[split] ..."`.

## Stand up / take down (skill agi-post)
Stand up / take down = skill agi-post (§1 down: flags first, kill second · §2 up: row committed BEFORE spawn, card, then spawn); switch = `write.py config:formations 'set active doc:council-loop'`, ONE call (Prime / owner), read back by verification.py `formation`.
## Rules
- Nodes only through write.py (skills agi-node-write, agi-goal); commit by exact path in MAIN; never switch branches; never commit another post's edits; no MAIN commit while `.agi/sessions/verify-suite.lock` exists.
- No parent/kid dispatch in this mode (dispatch.py stays unused).
- Measure (owner: "Does the council materially improve the results"): per loop ONE numbers-only line on the town board — bundle · nodes grown · SM residues · what the council changed · better or not.
- Stop when the Prime relays the owner stop: finish the atomic step, write the card whole, commit, idle.
- Rotation at the meter line: skill agi-rotate. Post mechanics: skill agi-post.

<!-- THOUGHT:BEGIN — authored, not derived; carried across regenerating scans. The reasoning behind THIS version. -->
belam-S2-L5-XVIII 23:5xZ 09-29 rewrote The loop on the owner’s order, verbatim: "Then we’re going to add another small check where the director general two checks the MVP result against the hypotheses. They then issue their own correctives as needed under forked hypothesis chains splitting off from lone or more of the most relevant existing ones. Once that passes, Director General 1 looks at the resulting build nodes and checks them against the goals to see if those need any corrective steps dispatched as nested subgoals. Once these loops complete amongst the directors, then it gets handed to Sanctuary Master to run its own review and check and get passed back using her lens for any correctives, using automated reviews. And once that’s done, then it gets passed to the council. In the process, Sanctuary Master should be the one to write the bigger outcome nodes to tie the outcome nodes together. And actually, one more correction, since this is going to be the new loop. Director General 1, once there are no more nested subgoal or hypothesis residues left to dispatch, uh, finalizes the outcome nodes for each goal in the bundle. Once Sanctuary Master does their reviews and their residue dispatches, then they write bigger outcome nodes once there are nothing else left to dispatch. And once those get written, then the chain, the graph chain that’s been grown can get passed off to the council to review the bigger outcomes and issue additional goals or additional bundles or additional nested goals or whatever, whatever level they see fit. And once none of those remain, then the council writes overview nodes to cap off the season’s growth and hands those off to you. At this point, we just keep working full steam ahead until about midnight Eastern time." Delta: outcome nodes move from the council (23:3xZ lens) to DG1; SM writes bigger outcomes; the council writes overviews; the lens flow now points at the loop.
<!-- THOUGHT:END -->
