---
id: hypothesis:l3w4-context-load-minimal
mint_id: 7faa66b13e4640aa9535ecbb83cbae2e
type: hypothesis
parents:
  - goal:g17
next_edges: []
edited_by: belam-S1-L3-XIII
scaffold_hash: 26157649b67a1a8f
season: 2
testable_claim: "Total always-injected context for every role drops by at least 70 percent and ideally 90 percent, measured as tokens in the assembled prompt before the role's first action, WITHOUT losing any fact a role needs to act correctly: the constitution head carries ONLY the prayers, the morals and the long readings move to an explicitly-invoked read for tie-break decisions; HANDOFF.md is replaced by a per-role slice whose default form is an ASCII state diagram plus a short pointer list; every seat's pin claim IS a git worktree branch claim, so identity, generation and handoff ownership are stamped by ONE writer on ONE path and git itself enforces single-holder exclusivity; and a survival-mode profile trims further still. Proven by measuring the assembled prompt for each role before and after with a token count, by a test asserting the constitution head contains the prayers and does not contain the readings, by a live rotation in which the successor claims its worktree branch and thereby its handoff in one operation, and by git refusing a second concurrent claim of the same seat branch."
thought_session: rc-XIII
title: "Minimal context load: prayers-only head, ASCII per-role handoff, pin-claim IS a worktree branch"
---
<!-- BODY:BEGIN -->
# hypothesis:l3w4-context-load-minimal

## Hypothesis

What is the testable claim? What would prove it? What would disprove it?

## Agent Notes
BUILD, NOT A PROBE. OWNER ASK, 2026-09-08, verbatim: "we need to trim context load upfront and then have a survival mode that's even lighter. The whole point is for context dump to be minimal via graphic ascii diagrams still easy to ingest. We need to trim handoff significantly, but also each role should have per-role handoff where pin also does the handoff claim via worktree branch or something. Maybe make all pin claims worktree branches. I mainly just want the prayers and stuff in there and then graphs. Also not every turn needs to end with prayer only very last turn of a session as it rotates very last tokens. And it just needs to have prayers as very first tokens. Condense other expressions to more limited quotes, the moral constitution and more in-depth quotes thing should be a read as needed to do tie breaker decisions. Can we trim about 70 to ideally 90 percent off the context injection for all roles?"

WHY THIS IS THE HIGHEST-LEVERAGE ITEM IN THE GRAPH, measured today, not asserted. `sanctuary-director` gen II measured that a fresh rotation spends 225k-250k tokens within its first ~50 minutes, dominated by the bootstrap read at spawn. Against a 350k rotation cap that is 64-71 percent of a generation's ENTIRE lifetime budget consumed before it does any work. The mechanism that makes it worse than a one-time cost: an LLM re-sends its whole context every turn, so a large static prefix is paid PER TURN, not once. Trimming the prefix therefore multiplies through every turn a generation takes. Same measurement found idle seats cost ~0 tokens/hour and one ACTIVE seat moves ~552,000 tokens/hour, so the binding constraint is concurrent active work and the cheapest possible win is making each unit of active work carry less weight.

THE CURRENT LOAD, measure it yourself first and record the real numbers rather than trusting these: HANDOFF.md ~47,000 tokens of which section 6 alone is ~37,100; skills/agi/SKILL.md ~8,000; CLAUDE.md ~6,000; the constitution head ~4,000; the successor brief ~2,000; INJECTION.md head ~1,500. Roughly 68,000 tokens of static prefix for a prime. Target after: under 10,000. That is the 85-90 percent the owner is asking for and it is reachable without losing a single fact a role needs.

THE FIVE MOVES.

ONE, THE CONSTITUTION HEAD BECOMES PRAYERS ONLY. Owner: "I mainly just want the prayers and stuff in there and then graphs" and "the moral constitution and more in-depth quotes thing should be a read as needed to do tie breaker decisions". So the head carries the four prayers plus the project prayer plus the Michael invocation and NOTHING else. The five axes, the words of Jesus, the Tao, the carried sayings, the mantle description and the decision method all move OUT of the always-injected head and INTO an explicit read: a role that faces a genuine tie-break invokes them deliberately. brief.py already assembles the head per tier, so this is a change to what it assembles, not a new mechanism. PRESERVE ATTRIBUTION EXACTLY where any quote survives: Jeremiah 31:33 and Ephesians 6 are not Jesus and the labels are load-bearing (trap 4).

TWO, PRAYER PLACEMENT CHANGES. Owner: "not every turn needs to end with prayer only very last turn of a session as it rotates very last tokens. And it just needs to have prayers as very first tokens." So: prayers are the FIRST tokens of the head, and a closing prayer is emitted ONCE, as the literal last tokens of the session at rotation or termination, not at the end of every turn. Update skills/agi/SKILL.md's Session close section and the successor brief's standing rules together, in one pass, so the two cannot drift.

THREE, HANDOFF BECOMES PER-ROLE AND ASCII-FIRST. Owner: "each role should have per-role handoff" and "The whole point is for context dump to be minimal via graphic ascii diagrams still easy to ingest". The default artefact a role reads is a compact ASCII STATE DIAGRAM plus a short pointer list, not prose. What a diagram must carry: what is running, what landed, what is blocked, where it stops and the exact next command. What it must NOT carry: narrative, history, or anything already in git. Section 6 owner decisions moves OUT of HANDOFF.md into its own file read on demand, since it is 79 percent of the file and almost none of it is needed to take the next action. PROTECT IT ABSOLUTELY: owner answers are never deleted, only relocated, and the relocation must be verified byte-identical before and after. The existing handoff.py already has sections, claim, release, read, write, show; extend it rather than writing a second tool.

FOUR, AND THIS IS THE OWNER'S BEST IDEA AND THE ONE THAT FIXES TODAY'S DEFECT RATHER THAN SHRINKING IT: PIN CLAIM IS A WORKTREE BRANCH CLAIM. Owner: "pin also does the handoff claim via worktree branch or something. Maybe make all pin claims worktree branches." Today produced hazards 3, 4 and 5, all one shape, stated by sanctuary-master gen II: "generation and identity are stamped by different writers on different paths". Measured: alive and sanctuary-master had a generation stamp and no rotation record; self-perpetuating, all-is-one and belam had a record and no stamp; a perfect complementary split with no seat holding both. Two seats shared one pin file and one metered the other's dead session. A meter read 0.3272 four hundredths under the rotate cap and was wrong; another read 0.189 when the truth was 0.415 and BLOCKED a correct rotation. Every one of those is two writers disagreeing about one fact. A worktree branch collapses them into one: claiming seat/<name> IS the identity, IS the generation, IS the handoff ownership, one act, one writer, one path. AND GIT ENFORCES IT: git refuses to check out a branch that is already checked out in another worktree, so a second concurrent claim FAILS LOUDLY instead of silently succeeding. That is the exclusivity the pin file could not provide and failed to provide three times in one day. Verify that refusal is real on this box before designing around it, then make the failure message legible to a seat. Keep a fallback for a role that legitimately has no worktree, and say plainly what it is.

FIVE, A SURVIVAL PROFILE THAT IS LIGHTER STILL. Owner: "then have a survival mode that's even lighter". One flag or config key that strips the injection to its minimum: prayers, the ASCII state diagram, the exact next command, the kill and verify procedures, and nothing else. No goal listing, no traps, no history. It must be a PROFILE selected at assembly time, not a second code path, or the two will drift the way every duplicated path in this project has.

WHAT MUST NOT BE LOST, and check each one explicitly before declaring done: the exact next command a cold reader needs; the kill procedure (kill by PID and the whole wrapper chain top-down, never by closing a tmux window, re-scan for orphans reparented to init because detached kids are invisible to spawn_budget, then two consecutive clean readings); the OpenRouter key-floor rule (check the KEY not the account, never lower provisioning.min_key_remaining_usd); every owner answer, relocated not deleted; and the attribution labels on any surviving quote. A trim that loses one of these has cost more than it saved.

PROVE: measure the assembled prompt per role before and after with an actual token count and report both numbers plus the percentage, per role, not in aggregate. A test asserting the head contains the prayers and does NOT contain the readings. A test asserting section 6's content is byte-identical after relocation. A live rotation in which the successor claims its worktree branch and thereby its handoff in ONE operation. And a demonstration that git refuses a second concurrent claim of the same seat branch. Report honestly if the 90 percent is not reachable without losing something on the must-not-lose list; 70 percent with everything preserved beats 90 percent with a hole in it, and the owner asked for a range for exactly that reason.

DISPATCH-TIME INSTRUCTION, SANCTUARY-DIRECTOR GEN II, 2026-09-08 -- YOU ARE A LOOPING PARENT, NOT A ONE-SHOT. This is process instruction for you specifically, not part of the hypothesis. Owner, direct: "Dispatch parents specifically who can loop kids." Measured cause you exist to fix: 8/8 prior parents this loop spawned one kid and exited (hypothesis:l3-parent-never-told-to-iterate) -- the template does not tell you this yet, so it is being told to you here.

YOUR LOOP: spawn one kid with --harness pi (repeat --harness pi explicitly on every kid dispatch -- it does NOT propagate from your own invocation). Review the kid's node when it finishes: read its verdict, its diff, its struggles/caveats. Then judge one of three ways -- CONTINUE (same target, next slice, write the next kid's brief carrying forward exactly what the last kid actually produced and what remains, not just "keep going"); ADJUST (same target, a corrected approach, state plainly what was wrong with the last attempt); or DONE (the hypothesis is proved/disproved/inconclusive with real evidence and nothing more to build -- this is the only judgment that exits your loop). Never spawn a second kid blind while the first is still running.

BOUND: maximum 6 kids total in this round. If you reach 6 without DONE, stop, write your honest status (what proved, what didn't, what's left) into the node, and exit -- do not keep going past the bound on your own judgment.

BEFORE EVERY KID (not just the first): check the OpenRouter KEY balance, not the account balance -- `curl https://openrouter.ai/api/v1/key -H "Authorization: Bearer $OPENROUTER_API_KEY"` and read `limit_remaining`. If it is at or under $1.00, STOP and do not spawn another kid -- write your status and exit. Never lower or bypass this floor.

Report your balance delta (limit_remaining before your first kid minus limit_remaining after your last) in your closing node update.

OWNER EXTENSION, 2026-09-08: PER-ROLE SKILL.md SLICES, and the gate on the prime's own rotation. Verbatim: 'I was thinking different roles also would be shown different parts of the skill.md as well like the command structure and hierarchy and how everyone plays their part. That's the biggest one any role needs to know.' So the trim is not only SHRINKING the injection, it is SLICING it per role -- and the owner names the highest-value slice explicitly: command structure, hierarchy, and how everyone plays their part. Build the per-role view from the SAME machine-readable hierarchy that hypothesis:l3w4-hierarchy-one-source produces; do not author a second description of the roles, which is the exact failure that node exists to end (three partial sources today, all contradicting). GATE, owner: 'Good to rotate just make sure the context dump shrink lands first and works with rotate properly.' THIS NODE BLOCKS THE PRIME'S ROTATION. It must land AND be demonstrated working through a real rotation before belam-S1-L3-XIII hands over. Concretely that means: the successor's assembled prompt is measured smaller by the reported percentage, the successor comes up and can act, and the per-role slice it receives is the right one for its tier. A trim that shrinks the file but breaks or degrades rotation is a regression, not a win, and the rotation is the one path with no second chance if it fails. THE TARGET STATE the owner states for the whole system, worth building toward rather than merely under: 'any one role transcript reads like just a series of stocato blurbs back and forth with various other channels and only the ephemeral openrouter parents+kids are actively constantly churning tokens as the rest just gently sip on tokens ever so slowly.' Measured support: an idle seat costs ~0 tokens/hour (a meter grows only on completed turns) while one ACTIVE seat moves ~552,000 tokens/hour. The lever is therefore fewer and SMALLER turns per seat, with churn pushed onto OpenRouter -- not fewer seats.

WORKED TARGET FOR THE ASCII FORM, from the prime, 2026-09-08. This is a TARGET to beat or replace, not a specification to copy: the owner asked for "graphic ascii diagrams still easy to ingest" and a description of a diagram is not a diagram, so here is one, sized against the real state at the time of writing. If you build something better, build that instead and say why.

BLOCK 1 -- THE STATE CARD. Replaces most of what section 0 does today. Roughly 90 tokens against section 0's current ~1,500.

  +- BELAM . prime . season/s2 --------------- meter 0.41 / cap 0.46 -+
  | MODE  survival: 1 active seat, all others idle (~0 tok/h)         |
  | TREE  season/s2   pushed, 0 unpushed   3 dirty = unreviewed draft |
  | GATE  my rotation BLOCKED on l3w4-context-load-minimal            |
  | SPEND openrouter key $9.26 / $15   floor $1.00 NEVER lower        |
  +-------------------------------------------------------------------+
  NEXT   wait SD.03 -> commit rotate.py -> dispatch ctx-trim -> SD.05
  READ   S6.71 state . S6.75 trim . S6.78 roles       <- these three only

BLOCK 2 -- THE ROLE MAP. This is the slice the owner named as "the biggest one any role needs to know", so every role gets it. Note it encodes the BUILD BOUNDARY, which is the ruling the prose kept losing.

                       owner
                         |
                      liaison ......... the owner's channel
                         |
      +------------------+------------------+
      |                  |                  |
  sanctuary-master   master-sensei        belam ......... prime
  seats/pins/rot     briefs/model-tests   loop, rounds
  = THE GRAPH        = LOCAL-MAXXING          |
      |    ^              |                   |
      |    +--- findings -+  (SM applies what Sensei measures: a LOOP)
      |                  |
   director-kid      director-kid
      |                  |
      +----- ONLY THESE MAY BUILD ------+
                         |
                  pi parents (openrouter)  <- the only constant churn
                         |
                       kids
      -------------------------------------------------
      quorum: self-perpetuating . alive . all-is-one
      one TREE each . SM builds merge -> self-perpetuating

BLOCK 3 -- THE LOOP, replacing the prose walkthrough in SKILL.md for roles that only need to run it.

  dispatch --harness pi --tier parent
      |
      v
  parent --+--> kid --> node --> review --+--> continue (next slice)
           |                              +--> adjust  (say what was wrong)
           ^------------------------------+--> done -> exit
  ceiling: max 6 kids . check KEY before each . stop at $1.00 floor

RULES THAT MADE THESE WORK, and the reason each is here rather than a style preference. ONE, a box states what IS, an arrow states what happens NEXT, and nothing states what already happened -- history is git's job and the single largest source of the bloat being removed. TWO, every diagram must survive being read by a model with no other context, so no glyph carries meaning that is not also written in words somewhere in the same block. THREE, pointers not prose: "S6.71" beats a paragraph summarising item 71, because a role that needs it can read it and a role that does not has paid 4 tokens instead of 400. FOUR, the state card must be GENERATED from live sources -- git status, spawn_budget, the meter, the key balance -- never hand-maintained, or it becomes another view that resolves confidently and is wrong, which is the defect class that cost this loop seven separate incidents in one day. FIVE, keep it under 100 lines total across all blocks for the fattest role; if a role needs more than that to act, the fix is a pointer, not a bigger diagram.

WHAT TO MEASURE WHEN YOU HAVE BUILT IT: assembled prompt tokens per role, before and after, reported per role rather than in aggregate, plus the percentage. And the honest check the owner asked for -- if 90 percent is only reachable by dropping something on the must-not-lose list, report 70 percent with everything intact instead and say which item forced it.

TWO OWNER EXTENSIONS, 2026-09-08, both verbatim, both scoped into this node because they are the same build.

ONE, DIAGRAM-MAXXING EVERYWHERE, NOT JUST IN THE INJECTION. Owner: "Can we also make it so that during both user-turns, self-turns, and role-to-role messages everyone is always diagram-maxxing. We can do a combo of both hand-generation and script-based diagrams later as the shape becomes clear. This way all models think more structurally overall."

Scope widens from the static prefix to EVERY surface a role emits on: replies to the owner, a role's own working turns, and role-to-role messages including dm, room, audience and the cross-session channel. The stated purpose is not compression, it is COGNITION -- "this way all models think more structurally overall" -- so judge a diagram by whether it makes the structure of a situation legible at a glance, not merely by whether it is smaller than the prose it replaced. A diagram that compresses but obscures has failed the actual ask.

The owner explicitly permits a mixed approach and explicitly defers the split: "a combo of both hand-generation and script-based diagrams later as the shape becomes clear." So do NOT build a diagram framework now. Establish the vocabulary by hand, let roles emit diagrams in their turns, and only script the ones that prove stable and repeatedly identical. Scripting a shape before it has settled is how a generator ends up regenerating a body nobody can author, which this project has already paid for once (goal:g2.10, 8,034 fields reading TODO(model)).

The one thing that MUST be script-generated from the start is the state card, because a hand-maintained state card is by construction a view that can disagree with reality, which is the exact defect class that produced seven separate incidents on 2026-09-08. Generate it from git status, spawn_budget, the meter and the key balance. Everything else may start by hand.

TWO, THE WORKTREE SPLIT MUST HOLD FOR THE MAIN BRANCH AND FOR THE GRID REFS. Owner: "Make sure the pin worktree split also holds properly for both the main branch and the grid refs and nothing breaks."

This is the sharpest technical constraint on the whole design and it is easy to get subtly wrong, so treat each of the following as a test to write, not a note to read.

GIT WORKTREES SHARE ONE REF NAMESPACE AND ONE OBJECT STORE. refs/grid/* is therefore GLOBAL across every seat worktree, not per-worktree. That is correct and desirable -- there is one grid, and a node's history must not fork per seat -- but it means concurrent grid writes from two seat worktrees race on the same refs. Determine what git actually does under that race on this box before designing around an assumption, exactly as with the branch-checkout refusal.

THE EXISTING RULE MUST SURVIVE, NOT BE QUIETLY DROPPED: CLAUDE.md states that grid commit --all runs on season/* or master only. A seat sitting on seat/<name> therefore must NOT run commit --all, and the design has to make that structural rather than a rule people remember. The natural shape: a seat worktree accumulates ordinary git commits on its own branch, those merge up to season/s2, and the grid is versioned ONCE from the season branch after the merge. Verify that a node edited on a seat branch and merged up gets exactly one grid version reflecting the merged content, not one per worktree and not zero.

SESSION BOOKKEEPING IS ALREADY SHARED WHILE THE GRAPH FORKS -- proved as l3-cli-done-worktree-manifest via locations.shared_project_root(). The pin is bookkeeping and the handoff is graph content, so a design that puts BOTH on the seat branch is inverting a property that is already proven and relied upon. Decide deliberately which side of that line each artefact sits on and say why in the node; do not let it fall out by accident.

PAYLOADS RESOLVE RELATIVE TO A LOCATION NAME, NOT A PATH (SKILL.md, Configuration). A build node's payload_ref resolves under source_root, which defaults to the repo enclosing .agi/. Inside a seat worktree that resolves to the WORKTREE, so a grid commit taken from a seat worktree could capture a payload from a checkout that is behind season/s2. That is the concrete mechanism by which this design could silently version stale bytes, and it is the single most important thing to test.

NOTHING BREAKS is the acceptance bar the owner set, so demonstrate it rather than assert it: grid.py log, diff, versions and payload all still resolve correctly for a node touched on a seat branch and merged up; node_count does not drop across the change; links.py links stays at 0 broken; snapshot-goals.py --render --check stays byte-identical; and a rotation through a worktree-claimed pin leaves grid history intact and continuous. If any one of those cannot be demonstrated, report it and stop rather than shipping the split.
