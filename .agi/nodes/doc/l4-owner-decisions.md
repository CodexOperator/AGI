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
