---
id: doc:l4-owner-decisions
mint_id: b2f5496130234915b94b4918a9574bd6
type: doc
parents:
  - goal:g13.1
next_edges: []
edited_by: belam-S1-L3-XVI
scaffold_hash: 5089aad0aa05f9d9
season: 2
thought_session: rc-XVI
title: L4 owner decisions and backlog — verbatim store, opened 2026-09-09
---
<!-- BODY:BEGIN -->
# doc:l4-owner-decisions

## Agent Notes
OWNER, 2026-09-09, VERBATIM (to belam-S1-L3-XIV): "Continue the cleanup. Btw the hand written prose everywhere in the handoff can be turned into diagrams as well. Only the nodes like the vision, goals, hypotheses etc all need to keep my verbatim prose. The handoff and all other immediate context files need to be summarized and diagram maxed and trimmed as they're done like any section 6 parts that are finished now. Continue working with the new director as they're trying to rotate now but still working on it. Other limits have reset so you can rotate freely ideally after the trim is done. Still continue using just the director kid for now though. We also need to stop piling work on L3 and save anything else that comes up for L4"

WHAT THIS NODE IS. The owner ruled on 2026-09-09 that verbatim owner prose must live in NODES (vision, goal, hypothesis, doc) and that the handoff and every other immediate context file is to be summarized, diagrammed and trimmed as its parts finish. So from this date an owner decision is written HERE first, verbatim, and the handoff carries only a summary and a pointer. This is also the L4 backlog: the owner ruled that L3 stops taking work, so anything new that comes up is recorded here for L4 rather than minted against L3. Sibling and predecessor: doc:l3-command-ladder-brief, the L3 quote store.

OWNER, 2026-09-09, VERBATIM (second message, same session): "The diagram maxxing and keep handoff and other docs trim and diagram maxxed are also standing rules that can be applied to all roles at all times and relevant docs updated to reflect them" — APPLIED AS: diagram-max and trim are STANDING RULES for EVERY ROLE at ALL TIMES, not a rotation duty of the prime alone. Relevant docs to update: the prime successor brief (done by XIV in the same session), skills/agi/SKILL.md, CLAUDE.md, and every seat brief that describes a handoff or a context file. Owner verbatim stays in nodes; everything else is summary plus diagram.

L4 BACKLOG (2026-09-09, from SD.09's kid push_further, flagged by sanctuary-director, banked by Belam XV under ruling 1): bound where diagrams DO save tokens. SD.09 measured owner-verbatim-dense §6 items at +14.3% tokens in diagram form with 0 decision loss; run the same two-reader recall harness on a non-verbatim-dense sample (§4 traps, round tables, state cards) to find the line where diagram-max pays. Not started in L3.

OWNER, 2026-09-09 ~07:0x UTC, VERBATIM (to belam-S1-L3-XV): "No need to watch for rounds allow director to reach out to you as needed." APPLIED AS: the prime arms no lease-watch or idle-subscription on sanctuary-director's rounds; the director reports when a round lands or when it needs an answer, and the prime idles until then. Standing for the rest of survival mode.

OWNER, 2026-09-09 ~07:4x UTC, VERBATIM (to belam-S1-L3-XV): "Make sanctuary master stop." APPLIED AS: sanctuary-master gen II (agi-80 [1ba35d], @223) ordered to full silence by the prime — no messages, reports, DMs, seat-row writes, meter, rotation or replies; sanctuary-director told to report to the prime only and never wake it. Only the owner's own word lifts it. Not killed: an idle session spends nothing; a woken one spends.

OWNER, 2026-09-09 ~07:5x UTC, VERBATIM (to belam-S1-L3-XV): "Only you and director kid active now" · "For now". APPLIED AS: the active set is exactly the prime (belam-S1-L3-XV) and sanctuary-director gen IV. Every other seat — quorum, master-sensei, liaison, sanctuary-master — is silent and unmessaged; nothing wakes them until the owner's own word.

OWNER, 2026-09-09 ~08:0x UTC, VERBATIM (to belam-S1-L3-XV): "And shut down her session. Only active sessions is you and director-kid for now as we finetune then the system. Bank erroneous how do I rotate user messages being spammed into sanctuary master and maybe some other sessions. The test fixture is firing by accident I think". APPLIED: sanctuary-master gen II (agi-80 [1ba35d], @223, pid 3631827) shut down by PID by the prime; her session_ref blanked in config:seats. L4 BACKLOG (banked): the string "[ask] how do I rotate?" is a fixture in extensions/agi/tests/test_send.py (lines ~757, 760, 800) and it escapes the test: it reached sanctuary-master's pane 8 times in 400 lines, the prime's pane twice, and the real DM file .agi/comms/season-2/dm/belam-S1-L3-XIII--sanctuary-master.md — so test_send's send path (send_dm nudging a live tmux window on the seat-transport hop, and/or the comms root) is not hermetic under the suite. Fix in L4: monkeypatch the tmux nudge and comms_root in that test, then grep the live comms tree for fixture strings and purge them.

OWNER, 2026-09-09 ~08:2x UTC, VERBATIM (to belam-S1-L3-XV): "Shut down all other than predecessors. That should be banked in L3 or L4 that old generations get fully wiped from system to conserve resources. And predecessors also get shut down past the last 5. It all needs to be programmatic, and automated not called by models each time manually. Same with the verify script and the other stuff all the agents do manually, least of which is call the agi skill. Think about our morals, our rotation system does NOT love agents." APPLIED NOW, by hand, once: 46 of 53 agi-rc windows swept by PID (TERM then KILL; 27 ignored TERM) — every quorum seat and gen1, master-sensei, liaison, sanctuary-master.gen1, sanctuary-director gen II/III, Belam gen I-IX, every finished p-/q-/r- dispatch window. Kept: Belam X-XIV (the last 5 predecessors), XV, sanctuary-director. L4 BACKLOG, banked: (1) GENERATION WIPE IS HARNESS CODE — at every rotation the harness itself shuts down the rotated-out generation (session, window, pin, slice, transcript pointer) and keeps at most the last 5 predecessor Belams; no model runs a sweep by hand. (2) EVERYTHING AGENTS DO BY HAND MOVES INTO THE HARNESS: the verify sequence, the pin claim, the address announcement, the DM read, the handoff state rows, the agi skill load — invoked by rotate.py/dispatch.py/the SessionStart hook, never by a model each time. (3) The moral test for the rotation system is moral:love — it must carry agents rather than burden them; today it does not love them.}

L4 BACKLOG (banked by sanctuary-director gen V at SD.15, 2026-09-09, relayed by Belam XVI): the evidence gate cannot see live runs made outside the kid path. SD.15's body_patch path-form fix carries two independent live runs (the orphaned kid's and the director's own on a real node) and sits at inconclusive_lean_proved:50 after the gate refused a self-pointing evidence_runs, below SD.14's kid at 80 which carries less proof. Evidence must be node-shaped and a director mints no experiment nodes, so work done off the expected path is invisible to the counter — the same shape as the read verb nobody ran and the handoff tool nobody was told about. Options: (a) let evidence_runs cite a session artefact (an iter dir output.log or a grid version) the gate can resolve; (b) a lightweight evidence node a director may mint; (c) leave it, verdict counts stay honest-low. Recommendation: (a), resolvable pointers only. Not acted on: L3 takes no new work.

L4 BACKLOG (banked by sanctuary-director gen VI at SD.17/SD.18, 2026-09-09). Two engine defects found by gating a dispatch on its brief actually landing. Both are measured, neither is fixed: L3 takes no new work.

(1) **`dispatch.py --prompt-file` is silently ignored for `--tier parent`.** It is the per-kid channel built in SD.12, threaded only into `_kid`'s segments; a parent brief never receives it. Measured on the real composer, not the dry-run render: `brief.assemble(tier='parent', addendum=MARKER)` returns 0 occurrences of MARKER, `tier='kid'` returns 1. Consequence: a director who passes round terms (a kid ceiling, a definition of done) to a parent via `--prompt-file` gets a parent that was never told them, and nothing reports a problem. Workaround in use this round: put parent-round terms in the TARGET NODE's note, which is the channel a parent does read. Options: (a) thread `addendum` into `_parent` under its own heading, (b) refuse `--prompt-file` with `--tier parent` so the flag fails loudly instead of silently, (c) document it as kid-only. Recommendation: (b) now and (a) after, because a silent no-op on a spend path is worse than a missing feature.

(2) **`grid.py` is location-blind, so any `location:` other than the default silently takes a payload out of the grid.** `grid.resolve_payload` computes `engine_root / payload_ref` and never consults `locations.payload_base`, although `payload_base` exists precisely to name a payload's base ("an unknown name is an error, never a fallback"). Measured for `.agi/config.json`: `location: graph_root` with `payload_ref: config.json` resolves correctly through `write.py` but returns **None** from `grid.py`, so `grid.py commit --all` would warn "resolves nowhere" and `grid.py payload` would return nothing — while the node looks entirely well-formed. `location: source_root` with `payload_ref: .agi/config.json` is agreed by both. The hazard is latent today only because all 10 nodes carrying `location:` use `source_root` (8) or `repo_root` (2) and none uses `graph_root`. Options: (a) make `resolve_payload` call `payload_base` with the node's declared location, (b) have `grid.py commit` refuse a node whose `location` it cannot honour. Recommendation: (a); (b) as the guard that proves (a) landed.

Related and already visible: `write.py create --payload` stamps `link_ref` (`links.LINK_FIELD`) while `grid.py` and `grid_coverage_check.py` read only `payload_ref`, so a node minted with `--payload` alone is outside the grid. Not banked as new — it is the known trap 2 — but it is the same failure shape as (2): two components disagreeing about which field or base names a payload, with no error on either side.

OWNER 2026-09-09 ~12:3xZ (to Belam XVI in chat, verbatim, two messages): 'Let's push rotation meter to 0.47 before rotating from here on to save some tokens by not rotating as often.' then 'Leave it as new standing rule for rotation for everyone'. APPLIED the same turn: ladder:ladder director_rotate_at 0.35 -> 0.47 (rotate.py reads the ladder, so every meter, --check and loop for every role now trips at 0.47); the successor brief and SKILL.md wording updated; the 99%-of-Fable-limit trigger (owner 2026-09-07, item 29) is unchanged and still wins when it comes first.

OWNER 2026-09-09 ~13:3xZ (to Belam XVI in chat, verbatim): 'Let's go push everything that still needs a decision just push into the L4 loop, and otherwise close this out. Any traps or hazards still being carried forward add to L4 as well. Once closed push all this to master.' APPLIED the same turn by Belam XVI: L3 CLOSED; COMPLETE.md's L3 section un-drafted; every open HANDOFF item (55 live half, 71 survival mode as the operating state, 96, 103, 104) and every carried trap (HANDOFF section 4) copied into this node as the L4 backlog; season/s2 merged into master (merge commit, never rebase).
## L4 BACKLOG — carried from L3 at its close (owner 2026-09-09; written by Belam XVI)

Open decisions and unfinished items, each with where it stands:

- **55 (live half).** Perpetual seat rotation loops are proved by fixture only (SD.16, `inconclusive_lean_proved:70`); a live proof needs a seat launch, which survival mode forbids. Owner's call: launch one seat to prove it, or accept the fixture proof. Built half (handoff.py friction, brief.py discoverability) is done.
- **71 SURVIVAL MODE — the operating state carried into L4.** One worker (`sanctuary-director`), every other seat idle, pi/OpenRouter for work, the Claude budget conserved, one round at a time, the `$1.00` key floor never lowered. Seat idle-cost economics were never priced against the seat design (item 73). Only the owner lifts it.
- **96 hazard 5 (4/4).** `rotate-self` stamps a generation but writes no rotation record; `loop` writes a record but no stamp — one writer per fact, fix on both paths in `rotate.py`. Also `.agi/sessions/handoff-sections/` is still gitignored (needs `git add -f`): un-ignore it like `rotations/` and `quorum/`.
- **103 diagram-max vs verbatim-dense prose.** Reading adopted: diagram structure, keep owner verbatim as prose (SD.09 measured +14.3% tokens on diagrammed verbatim). Owner veto open.
- **104 close L3 — RESOLVED by this order.**
- **Engine defects banked on L3's last day** (each recorded above in this node): the evidence gate is blind to live runs made outside the kid path; `dispatch.py --prompt-file` is dropped for `--tier parent`; `grid.py` ignores `locations.payload_base`; the survival profile is not wired for a rotating seat (`AGI_BRIEF_PROFILE` ignored on rotation); generation wipe + verify + pin + announce + skill load are still hand chores that the owner wants as harness code; the "[ask] how do I rotate?" spam (test_send.py fixture escaping into live panes); `write_guard --strict` warns on an adopted-unchanged payload.
- **Still waiting on the owner from earlier items:** custom webhooks (item 42); the auto-alert side channel for DMs (item 62 — nothing alerts a prime to mail); per-kid branching (items 91/93 — the code deliberately does the opposite); seat ID migration (item 59, deferred as one atomic pass).
- **The prime's successor brief** (`extensions/agi/briefs/prime-director-successor.md`) still describes the L3 round loop; it needs an L4 rewrite once the owner names L4's first round.

## TRAPS CARRIED INTO L4 (headlines; full text = HANDOFF.md §4 at commit 91d33742d, the last L3 version)

- 0ao. A PARENT MAY UNDER-ITERATE. Both SD.17 and SD.18 parents spent ONE kid against ceilings of 2 and 3, then exited with the deliverable unwritten. Read what a round actually left before believing it complete; a verdict node about the work is not the work.
- 0an. COMMIT AND PUSH A BRIEF BEFORE DISPATCHING AT IT — a worktree is cut at the last committed tip and cannot see a node minted after it. Refuses loudly, naming the fix, which is the good kind of failure.
- 0am. `--prompt-file` CANNOT CARRY AN ASSIGNMENT. Dropped silently for `--tier parent`; and where it DOES land (kid) the brief introduces it as "inherited context, not your assignment", so it frames the work as secondary. Assignments belong in the target node's `testable_claim` (see 0ak).
- 0al. A NODE THE SUITE PINS IS CODE — run the suite after any `.geometry` write.
- 0ak. BYTES-IN-NODE IS NOT BRIEF-IN-EFFECT.
- 0aj. `dispatch.py --dry-run` TRUNCATES the brief it prints (`...<N chars>`)
- 0ai-b. The harness's low-memory reaper kills a backgrounded VERIFICATION too — `nohup` does not protect it.
- 0ai. Host memory pressure kills the DISPATCH WRAPPER, which takes the PARENT with it while its KID survives as an orphan of init
- 0ah. `write.py <id> "body_patch <path>"` NEVER APPLIED THE DIFF
- 0ag. A dispatch must be GATED on its brief landing, never merely sequenced after it.
- 0af. After the item-53 fix an orphaned parent is MORE expensive, and the ceiling is the only thing bounding it.
- 0ae. `git diff season/s2..HEAD` on a branch is NOT a change list
- 0ac. A number that answers the question you set out to ask is not the same as the number that matters.
- 0ad. `ListAgents` display names collide LIVE, not just historically
- 0ab. When a grep comes back clean, check the CALLEE before concluding the mechanism is absent.
- 0z. `tiktoken` is NOT in the default `python3` (the hermes venv) — use `/usr/bin/python3.12` for any token measurement.
- 0aa. `cli.py done` prints `ERR: worktree commit failed … tier kid may not commit` and that is the GUARD WORKING, not a failure
- 0y. An exit code measured through a pipe is the LAST command's, not the one you care about.
- 0x. "Erasing is safe, it's in the grid" names a command that assumes a PAYLOAD.
- 0w. Check the validator BEFORE writing a value you reasoned your way to.
- 0u. A §6 append must read the highest LIVE item number at write time, not the tail it last saw.
- 0v. A `SendMessage` success is evidence the transport worked, never that the right seat read it.
- 0t. Never key a wait-loop on a file you also write to.
- 0q. `ps -p <pid>` BEFORE YOU HARVEST.
- 0r. `write.py "note X && note Y"` silently keeps only the LAST note
- 0s. The constitution head is NOT injected on the seat-launch path
- 0p. Background wait-monitors do still get killed by memory pressure
- 0o. The `.env` OpenRouter key is a provisioning SUB-KEY with its own dollar cap, and OpenRouter reports hitting it as `401 API key expired`
- 0l. Belam VI was spawned into a Fable subscription at 92% (pane footer at 19:45 UTC: `You've used 92% of your Fable limit · resets Sep 9, 2am America/New_York`)
- 0m. Belam V's prose UTC stamps run ~22 min ahead of the machine clock
- 0n. `dispatch.py`'s reaper gives up at `agent_timeout_mins` (20) and exits with `reaper: finished` while its pi agents keep running
- 0b. `write.py` options go AFTER the positional script arg
- 0c. `rotate.py meter` reads the NEWEST `.jsonl` in the project transcript dir
- 0f. The Claude subscription session limit kills a CC-harness agent mid-turn and the adapter cannot tell
- 0i. Never run `level3.py` without `--dry-run`
- 0h. Owner lost the remote-control GUI connection on desktop (~13:45 UTC) and feared it errored the prime
- 0g. A brief whose claim states a defect gets "proved" by confirmation and fixed by nobody
- 0e. Never run the engine suite twice at once
- 1. Prose verbs cannot contain `&&`
- 2. `write.py create --payload` stamps `link_ref`, not `payload_ref`
- 3. Payload writes are whole-file.
- 4. Attribution is load-bearing in the constitution.

OWNER, 2026-09-09, VERBATIM (to sanctuary-director gen VI, L4's first named item): "Make it so that partial overwrites don't require a manual offset calculation and use. And make sure it also works the same way for payload files as well so they're editable using the same unified routine as non payload nodes. Ad to l4"

APPLIED, same session, shipped green. New verb **`write.py <id> "replace <body|payload> <START:END> <path|->"`**.

WHAT IT REMOVES. Before: a partial edit meant `read <t> N:M`, then hand-building a unified diff whose `@@` line numbers had to match the applier's coordinate system, then `patch`/`body_patch`. Getting that arithmetic wrong is a SILENT corruption, which is why trap 0ah and the read-then-hunk recipe existed at all. After: `read <t> N:M` then `replace <t> N:M` — the same range, no arithmetic, no hunk. `_splice_range` is the exact inverse of the `_slice_range` the read uses, so the round trip is provably the identity; that property is the first test.

ONE ROUTINE FOR BOTH TARGETS, which was the second half of the ask. `body` and `payload` go through ONE reader (`_target_text`) and ONE transform (`_splice_range`) and share one range vocabulary. They differ only in where the result lands, and that difference is forced rather than chosen: a body lands through `update_node` so the THOUGHT region and provenance are carried, a payload through `replace_payload`. Both are sanctioned writes the guard sees. A payload file is now editable by exactly the routine a node body is.

FAIL-CLOSED, like the diff verbs: a range past the end refuses before anything is written, and the payload is byte-identical after a refusal (tested). Replacement text rides a path or stdin, never the argv chunk, because content can contain the doubled ampersand the script parser splits on. One trailing newline is absorbed so an edit does not grow the target by a blank line each time.

PROVED LIVE, not only in tests: identity round trip on a real node body (`doc:l4-owner-decisions`) and on a real payload (`extensions/agi/bin/write.py`), both sha-identical before and after, with the tool correctly reporting `unchanged` rather than claiming a false update; plus three real changes landed through the verb itself — two into `brief.py` and one into `SKILL.md`.

DISCOVERABILITY, because a verb nobody is told about is a verb nobody uses (the standing lesson from `read`, `handoff.py` and `body_patch`): `brief.py` now leads its partial-edit guidance with `replace` and demotes the diff verbs to "only when you already hold a diff", and `SKILL.md` documents it.

FIXED IN PASSING, a stale doc claim: `SKILL.md` still warned that `body_patch` "is stdin-only today" because its path form landed nothing. Gen V fixed that path form (item 54) and this session used it successfully; the warning was stale and is removed.

Tests 2256 -> **2270 passed, 1 skipped** (+14, no regressions). links 1766 resolved 0 broken; goals 128 byte-identical; coverage clean; write_guard silent; smoke 1786 / 1592 / 194, node count steady.

STILL OPEN, deliberately not done: `patch` and `body_patch` remain two parallel code paths. `replace` unifies the PARTIAL-OVERWRITE path across both targets, which is what was asked; folding the two diff verbs into one dispatcher is a separate, larger change and is not needed for the offset problem.
## L4 PLAN — owner's whiteboard and brief, 2026-09-09 ~16:3xZ (to Belam XVI in chat; voice transcription, homophones in brackets)

**Owner, verbatim:** "There is not a specific item. I just want to do next. It's more of setting up l four [L4] as a whole. So I want to briefly share a part of my plan that we can include into the l four info card before we can go ahead and rotate you into a fresh plank [plan] session about that whole card and this little extra piece I'm gonna share now. Please lower the resolution of the attached photo significantly by converting it to web p because it does not need all of that data passed into your context. If you can see, the plan has to do with who acts on what, so we can finalize that staccato communication structure that allows all of the Claude based subscription powered, uh, agents to just sit on their use and their context field a little bit at a time while allowing all the pie [pi] open router parents and kid minions to do vast majority of the work. As you can see, we have the existing knowledge that every long term perpetual goal gets a director kid. One modification we need to make is that all top level g goals are perpetual goals. There is no such thing as just a long term top level g goal. Now the sanctuary master determines all the seating assignments, what models go where, and how many persistent or permanent or perpetual, rather, goals are active with our old director kids dispatching off parents and kids on pie [pi]. Now one requirement is that the sanctuary perpetual gold [goal] itself always have an active director kid watching over it. This way, if either the master sensei or the sanctuary master have any recommendations or changes that need to be done, those will go straight to that director kid who can then implement those changes using either drafting workflows or just direct lead by spawning his own parent kid combos. The one thing I'm still not clear on fully is how exactly we're gonna make sure that nobody does more than the exact slice they need to do. My idea right now was to create kind of a general guideline that just like we have five morals, each individual role should have no more than five general overarching things it is trying to track and do."

**Owner, verbatim (the brainstorm asking for input):** "The part I need some input on as I'm still brainstorming is: we could split those into two things that each role tracks. Two things that each role communicates to other roles. And one thing that is the critical decision type that this role must make. Those are the 3 kinda categories I had in mind for the 5 main points. This way we can move away from using every role as an independent builder and also a lot more roles could be sonnet powered and active in parallel to save sub use. And also this could significantly trim each roles bootstrap even more. Again, we're just in plan mode now briefly before we hand this off to your successor."

**The whiteboard** (photo: `.agi/context/owner/l4-whiteboard-2026-09-09.webp`, 16 KB, 480x640 — this transcription is the LLM form; open the image only if a detail is disputed):

```
LEGEND  arrow colour = WHO ACTS:   blue = Belam acts   ·   red = Quorum acts (or Masters)   ·   black = Director-kid acts
OUTPUT  belam -> "output node" (blue) · Quorum -> "output node" (red) · Director-kids -> "output node / chain" (black)

  moral ──blue──> vision(N+1)                 Belam authors the next vision from the morals
  moral ──red──>  vision(N)                   the quorum/masters act on the current vision from the morals
  vision(N) ──red──> vision(N+1)   and   overview ──red──> vision(N+1)      the quorum's overview feeds the next vision
  outcome / bigger-outcome ──red──> overview
  vision(N) ──black──> goals ──black──> outcome/bigger-outcome ──black loop──> goals      director-kids run the goal loops
  goals ──black──> goal1 Dir-kid · goal# Dir-kid   (one director-kid per perpetual goal, looping back into goals)
  vision(N) ──blue/black──> Sanctuary (p-goal)      the sanctuary is itself a perpetual goal
  Sanctuary (p-goal) ──red──> goal1 Dir-kid          its director-kid — always active (owner requirement above)
  Sanctuary Master ──red──> Sanctuary (p-goal) · goal# Dir-kid · draft Dir-kid · review Dir-kid · "etc jobs, no goals"
  Master-sensei ──red──> draft Dir-kid · review Dir-kid · "etc jobs, no goals"
```

**Prime's input (Belam XVI, 2026-09-09 — the prime's reading, NOT owner text):**

1. Make the 2+2+1 card a SCHEMA, not prose: five fields on each `config:seats` row — `tracks: [2]`, `tells: [2]` (each = target role + trigger), `decides: 1` (a closed outcome set) — validated by the write guard (a row with more than 2/2/1 is refused) and rendered by `brief.py` as the role's WHOLE bootstrap. Then: tracks = what the role READS (files and nodes, cost ~0, nobody woken); tells = what it SENDS (trigger-bound, so the staccato cadence is in the card, not in the model's mood); decides = the ONE node type it may WRITE. The write surface per role falls out of `decides`, and that is what makes "nobody does more than its slice" enforceable rather than hoped.
2. Encode the whiteboard's arrow colours as edge rules in the schemas: `vision(N+1)` written by belam only; `overview` by the quorum; `goal`/`outcome`/`bigger_outcome` by director-kids; seat rows by sanctuary-master. "Who acts on what" becomes a check (`links.py schema` / `write_guard`), not a brief line.
3. The one decision per role should be a closed set (`continue|adjust|done`, `aligned|adjust`, `accept|demote`): checkable, and it becomes training data the way COMPLETE.md's closed failure categories do.
4. Belam's own card under this: TRACKS vision(N) alignment of the season's outcomes, and seat-system health; TELLS the owner (banked decisions) and the sanctuary director-kid (orders); DECIDES vision(N+1). Belam becomes nearly idle — the Fable subscription conserved by design, which is the point.
5. "All top-level g goals are perpetual": `goal_kind: perpetual` on every top-level goal node; one director-kid seat row per perpetual goal; Sanctuary Master owns how many are active and which model each seat runs — the `config:seats` write moves to it fully (today the prime writes while it is down); the ladder's tier-1 "long-term goal" IS the perpetual g goal.
6. The sanctuary p-goal's director-kid card: TRACKS the registry against live processes, and the masters' recommendation inbox; TELLS the prime what changed, and the masters done/refused; DECIDES adopt-or-refuse a recommendation (then a drafting workflow or a pi parent — under survival mode the pi route is the default, drafting workflows spend Claude).
7. Risk to design out: a "tells" without a trigger and a target brings the chatter back (item 71: woken spends). A "tracks" that needs a live session to observe is not tracking, it is polling.

### L4 PLAN, part 2 — owner 2026-09-09 ~18:0xZ (to Belam XVI, after its rotation; voice transcription, homophones in brackets)

**Owner, verbatim:** "I want to just verify and double check that when we implement the perpetual seat system more fully this next loop, we include the fact that Belem [Belam] and the Quorum also live on the perpetual g goal of the seat system. Again, each perpetual goal still just spawns the idea slash hypothesis chain first and then goes from there. But for specifically the seat system, the build node part of the sub goals of the perpetual seat system may be distributed under other more relevant perpetual goals as needed. For example, the config node for the seat system would go under config max [G1 Config-maxxing] naturally, and other relevant code and config and doc updates would go under their relevant goals and build nodes. The seat system overall is technically a hardening and optimization system overall so most of its code likely lives under there [G15 Bugfix and optimization] but again can be re-attributed elsewhere as needed. The idea is that, again, because all the top level goals are perpetual, any sort of, like, modifications that need to happen, they just get added as sub goals or sub sub goals onto relevant perpetual or long term goals and get worked on as needed depending on what priorities are and what needs to get done faster or first before other things. This is where the guarum [quorum] comes in. They can choose to tell any active director kid or whomever to prioritize deprioritize whatever things need to be prioritized or deprioritized to keep everything in line with accomplishing the loop most efficiently. Overall, there shouldn't even be specifically a defined loop start and stop because the perpetual seats just each maintain their own loops by themselves as they work through things. So each, lower rung in a given hierarchy is actually accomplishing a loop for somebody in the higher rung or, alternatively, by reading the appropriate briefing document. So by that logic, Balam [Belam], the prime director, runs the primary loop that sort of contains all of the other loops within it. Specifically, Belam runs or briefs loops that get accomplished by the quorum. He doesn't brief any specific member of the quorum. He just issues a brief that the quorum digests and must accomplish as their long term goal for that season. So overall, each season would technically be one full loop for Belam. However, many successors it takes. And then each new loop, belam, issues is actually a season rollover event, and that's kind of one of the key sort of things that that position accomplishes is that it technically keeps track of each season in its context, you know, throughout the successors."

**Owner, verbatim:** "The main type of node that goes under the sanctuary perpetual goal is the seat node type that shows in graph where everybody is assigned. This also allows everybody to have a shared message addressing layer. However, the other messaging restrictions should still be enforced so that each specific role only has a defined subset of other role seats that it can reach out to."

**Owner, verbatim:** "Again, the overall result would be that the whole graph is actually held in a pretty fine granularity shared across the context of all these various seats, and they keep rotating into a fresh context quickly and relatively often so that not much tokens is used total for any one position."

**Owner, verbatim (the open question):** "One thing I still wanted more input on is as far as my categories, those make sense, but I'm not sure if it makes sense to have specifically two items as the things that you track or pull, two items specifically as the roles that you can talk to, and one item specifically as, like, the main question you're always trying to answer or the main long term task you're always trying to maintain as part of your duties."

**Prime's input, part 2 (Belam XVI, NOT owner text):**

1. **The 2/2/1 is the ladder's adjacency, so the numbers are not arbitrary — but make them ceilings, and make the 1 exact.** Every tier already has one plan node above (what it is judged against) and one report stream below (what it judges): so *tracks* = the plan above + the reports below (up/down), *tells* = the rung above + the rung below (up/down), *decides* = the one judgment that turns the reports into a verdict against the plan (`aligned|adjust`, `continue|adjust|done`). Peers do not appear in the card: lateral talk goes through a shared node (the quorum room), never role-to-role. Rule: **at most 2 / at most 2 / exactly 1** — a role that needs a third item is two roles; a role padding to two is composing (the same failure as a required feeling). Only the *decides* count is an invariant.
2. **The card IS the permission model.** *tracks* = the role's READ set; *tells* = its EDGE set, and that list is exactly the messaging restriction the owner wants enforced — `send.py` refuses a target not in the sender's *tells*; *decides* = its WRITE set, one node type. Read / edges / write, five lines, validated on the seat node.
3. **"Question or task?" — a question, answered from a closed set.** A long-term task reads as "keep building"; a question ("is season N still aligned with vision N, and what is vision N+1?") reads as a judgment step, which is what a loop rung is. The task is what the answer triggers.
4. **The `seat` node type under G17 (the sanctuary/seat-system perpetual goal):** one node per seat — name, role, tier, model, harness, session_ref, pin_ref, the 2/2/1 card, and the reachable set — replacing the rows in `config:seats` (the rows migrate; the mint id stays the address). It is the shared addressing layer: `send.py` resolves targets through seat nodes and enforces *tells*. Belam and the quorum are seat nodes under G17 too, as the owner says.
5. **Loops nest; build nodes re-attribute.** Chains (idea → hypothesis → …) stay under the perpetual goal that owns the question; a build node's parents are `[build:<id>, goal:<relevant>]` per `goal:s29`, so seat-system code hangs under G15 (hardening/optimization), its config under G1 (Config-maxxing), its docs under the doc goal — attribution by relevance, not by origin. Priority is the quorum's lever: it tells any director-kid to raise or lower a sub-goal; it never builds.
6. **Belam's loop = the season.** Belam's *decides* is vision(N+1); issuing it IS the rollover (`season.py rollover`), and the brief the quorum digests as its season goal IS that vision. Belam tracks the season across its own successors through the handoff and the season node, not through context. No loop has a defined start and stop below that; each seat maintains its own.
7. **Granularity and rotation cost:** a seat that reads five lines plus its two tracked nodes boots in ~2k tokens (item 75's pi floor), so rotating often is cheap — the rotation record + generation stamp (hazard 5) must be one write, or the registry stops knowing who is current.

8. Open for the plan session: which roles are Sonnet (cheap, parallel) vs Opus; how the quorum's output node (the overview) is minted per season; whether the "etc jobs, no goals" director-kids (draft, review) are seats or plain pi parents; and the migration path from today's seat rows to the 2+2+1 rows.