---
id: hypothesis:l4-the-window-reply-and-harvest-or-cut-are-captive-steps
mint_id: 8ad2b2575b944e0cb92088629ebd047e
type: hypothesis
parents:
  - goal:g15.14
  - hypothesis:harvest-table-subcommand
next_edges: []
edited_by: sensei-director
scaffold_hash: 7c3ed8c77a71b19f
season: 2
testable_claim: "OWNER 2026-09-11 15:5xZ (doc:l4-owner-decisions): 'propose any additional captive or driven steps the rotate.py script needs so that LLM's are properly prompted through parts needing their input, not just write and read things raw'. Goal goal:g15.14 (parents + '## Why this exists' there; steps 3+4 of its four). DESIGN RULE: where an LLM's judgement is needed the script PRINTS the exact bounded question with every measurable value pre-filled; where it is not, the script PERFORMS the step. Never remove a decision from the LLM. MEASURE FIRST: in the Prime's transcript (belam 140328Z record: handover.join.transcript) count the calls a merge-up window reply costs today (the lock read, the tip read, the baseline read, the message) and in the point's successor transcript (sanctuary-director 135144Z record) the calls between the ack and the first harvest/cut decision (71 harvest calls measured by the Sensei at 122528Z) — the pre-fix numbers are the evidence line, written BEFORE the code. STEP 3 — CAPTIVE MERGE-UP WINDOW REPLY: one subcommand in the tool that OWNS the lock and the baseline (verification.py, which holds SUITE_LOCK verify-suite.lock and STATE_FILE verify-count.json; rotate.py only if verification.py cannot host it; never a new bin/ file): verification.py window [--grant SEAT] prints the reply in the shape the point holds for (§Merge-up step 2 of .agi/sessions/quorum/sanctuary-director.md: 'lock state + tip + baseline'): lock = free|held by <pid/seat since ts>, tip = origin/season/s2 sha (fetched, not guessed) + whether MAIN's HEAD equals it, baseline = the never-lower counts + their stamping sha/reason; --grant SEAT additionally names the seat in the reply text so the line is paste-ready — the DECISION to grant stays the Prime's (the command prints, it does not send). STEP 4 — THE POINT's CAPTIVE HARVEST-OR-CUT: rotate.py first-decision --seat S (or a flag of the landed harvest-table subcommand — find where L4.236 landed; extend it, never duplicate): per open round of the seat's worktree the harvest-table row (branch, parent, kids, verdicts, merge-base, behind) pre-filled, then ONE bounded prompt per row: 'harvest <round> | cut <next queued node> | hold' — printed, never answered by the script; a --answers FILE replays the LLM's choices into the named next command per row (the git merge line with the EXACT branch name from git branch --list, the dispatch line for a cut) without running them. RED-FIRST TESTS test_verification_window.py + test_rotate_first_decision.py on fixture roots: window prints held-by when the fixture lock exists, free when not, the fixture baseline sha; first-decision prints one row per fixture round with the exact branch name and refuses to run a merge; an answers file yields the merge line for 'harvest' and the dispatch line for 'cut'. Neighbours test_verification*.py, test_rotate.py, test_bin_help_smoke.py stay green. FALSIFIER: a step that sends the window reply or runs the merge/dispatch itself — refused, not landed. FILE SCOPE: extensions/agi/bin/verification.py (window subcommand only), extensions/agi/bin/rotate.py (first-decision / harvest-table region ONLY — nothing in handoff/prepare (goal:g15.14 steps 1+2, parallel) or first_turn/bootstrap/spawn (goal:g15.15, parallel)), + the two new test files. EXCLUDED: season.py merges (HELD verb), config:*, hooks, send.py. CEILING: up to 2 kids PARALLEL (step 3 / step 4), the parent merges every kid branch into the round branch before done:. Report: per step the calls removed, pre vs post."
thought_session: sensei-director-genI-L1
title: "the merge-up window reply and the point's harvest-or-cut are captive steps: pre-filled by the script, decided by the LLM"
town: core
---
<!-- BODY:BEGIN -->
# hypothesis:l4-the-window-reply-and-harvest-or-cut-are-captive-steps

## Hypothesis

What is the testable claim? What would prove it? What would disprove it?

## Agent Notes
DIRECTOR sensei-director 16:2xZ (Sensei package e8a7df41b, lines 7-8, measured): the window reply prints lock state + season/s2 tip + kept-merge baseline + the exact GO <n> line to send (prime 140328Z calls 40-45 did it by hand: 6 calls); the point's first decision is the F5 shape, 9-12 calls per turn today — harvest-table output + harvest <round> | cut <node> as the exact next tokens. Drafts are gitignored under MAIN: /home/ubuntu/work/agi/.agi/sessions/sensei/drafts/ — read there, read-only.
