---
id: hypothesis:l3w4-master-director-kid-worktrees
mint_id: b2ff94a42a064215989b5162473c30cf
type: hypothesis
parents:
  - goal:g17
next_edges: []
edited_by: self-perpetuating
scaffold_hash: 51cf50659a181254
season: 2
testable_claim: After the change, sanctuary-master and master-sensei can each spawn a director-kid into its own git worktree cut from the seat checkout, reusing dispatch.py --branch machinery rather than a second mechanism, with model claude-sonnet-5 per the owner; proven by a live spawn under each master seat landing a real commit on its own branch, verified from outside the agent with git rev-list --count base..branch > 0; quorum parent-spawning is unaffected and out of scope.
thought_session: 3066c544-b046-4b05-a372-c9986c07d0a5
title: Sanctuary Master and Master Sensei each need an always-on director-kid, spawned into its own worktree, since the owner has barred them from building directly
---
<!-- BODY:BEGIN -->
# hypothesis:l3w4-master-director-kid-worktrees

## Hypothesis

What is the testable claim? What would prove it? What would disprove it?

## Agent Notes
BUILD, NOT A PROBE. Owner, 2026-09-08, relayed by liaison: sanctuary-master and master-sensei are now BARRED from building anything themselves (config/prose only) -- their build path is one ALWAYS-ON director-kid each, spawned under its own worktree, to do all build work. Owner verbatim: "that means we will be hitting our cap of 2 director-kids plus the rest of the staff early, but that's fine. The quorum can keep spawning parents as is, and the director kids are for the masters and work under the masters' worktrees." Quorum parent-spawning is explicitly UNAFFECTED -- this is only about giving the two masters a build arm they don't have yet, since they are now blocked without one.

WHAT TO BUILD, concretely. Do not invent a second spawn mechanism -- dispatch.py's `--branch` flag already does almost exactly this for a quorum parent: it runs the spawn in its own git worktree on `loop/<slug>-<agent>@s<N>`, cut from the spawner's checked-out branch, and the lease/record carries branch/base_branch/worktree (see `--help` on dispatch.py). A "director-kid" is the same shape, spawned BY a master seat instead of a quorum seat, with two differences worth checking rather than assuming: (1) it should be ALWAYS-ON / long-lived rather than one-shot-per-round -- check whether dispatch.py has (or needs) a persistent/supervised mode, or whether "always-on" just means the master re-dispatches it each time it has work, same as a quorum parent does today. Read hypothesis:l3w4-seat-rotation-loops and hypothesis:l3w4-seat-sessions-and-tiling before assuming either way -- this project has already measured that "no live tmux rotation has ever been observed" for one adjacent claim, so verify rather than take the always-on framing at face value. (2) model: the owner has separately named SONNET for director-kids (not opus, not GLM) -- confirmed in hypothesis:l3w4-master-sensei's body. Use claude-sonnet-5 unless a fresher owner statement overrides it.

WHO USES IT. Exactly two callers today: sanctuary-master and master-sensei, both tier-1 director seats per config:seats (.agi/nodes/.geometry/seats.md). Neither currently has a worktree/director-kid field on its seat row -- sanctuary-master is the one seat permitted to write that file (see its recent room posts on config:seats authority), so if the row needs a new field, propose it in the node body as a request addressed to sanctuary-master rather than writing seats.md directly (same rule master-sensei was corrected on earlier today for the same file).

SCOPE. This is spawn mechanism + worktree wiring only -- not a redesign of what either master does with the director-kid once it exists. Do not touch quorum parent-spawning (dispatch.py --tier parent for a quorum seat is explicitly unaffected and out of scope). Do not write .agi/nodes/.geometry/seats.md directly. Do not touch moral:* nodes.

PROVE IT. A live spawn: one director-kid dispatched as if by sanctuary-master (or master-sensei) into its own worktree, landing a real reviewed commit on its own branch -- the same external verification this project has just spent a whole session learning to insist on for --branch rounds (git rev-list --count <base>..<branch> > 0, checked from OUTSIDE the agent, not trusted from its own report). Cite that command's output as evidence, not a description of it.
