---
id: doc:l4-owner-decisions
mint_id: b2f5496130234915b94b4918a9574bd6
type: doc
parents:
  - goal:g13.1
next_edges: []
edited_by: belam-S1-L3-XV
scaffold_hash: 5089aad0aa05f9d9
season: 2
thought_session: rc-XV
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
