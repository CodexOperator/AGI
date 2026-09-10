---
id: hypothesis:l4-a-seats-live-model-is-measured-not-assumed
mint_id: 6149a46331184ea9aa4f5b177b8c8aa9
type: hypothesis
parents:
  - goal:g17
next_edges: []
edited_by: belam-S1-L4-V
scaffold_hash: 3eda959c7dc5adbe
season: 2
testable_claim: "OWNER 2026-09-10 ('Go for both a and b as described'; measurement on goal:g17.1). THE DEFECT: sanctuary-director gen VII was spawned with --model claude-opus-5 from its config:seats row, ran 129 turns on it, then the harness logged system/model_refusal_fallback (scope session, apiRefusalCategory cyber, a false positive on a dispatch tool result) and ran 191 turns on claude-opus-4-8 — while the row, the spawn argv and every green check kept saying opus-5. The graph's claim about a seat's model was falsified underneath it with no signal. CLAIM: the seat's LIVE model is measured from the newest assistant turn of its own transcript (the message.model field, the same .jsonl rotate.py meter already resolves) and compared with the row's model; DRIFT IS REPORTED, NEVER REPAIRED (detect, do not repair). Three surfaces, one reader: (1) rotate.py meter prints a model line beside the fraction — model=<live> row=<declared> and DRIFT when they differ — so every seat that pins its meter sees it for free; (2) commands.py run verify gains a check, seat-model, that walks config:seats rows with a live session_ref, resolves each transcript, and FAILS (not warns) on any drift, naming seat, live model, row model and the timestamp of the first drifted turn — because a green verify on a downgraded seat is the exact shape this project keeps paying for, a check that guards a proxy; (3) the model_refusal_fallback system event itself is surfaced: the reader also reports the last such event's timestamp, category and requestId so the cause travels with the symptom. The bootstrap record of hypothesis:l4-startup-is-one-script-or-a-driven-prompt carries the live model too, once it exists. PROVED BY: (a) a fixture transcript built from the REAL gen VII .jsonl (opus-5 for 129 turns, the fallback event, opus-4-8 after) makes meter print DRIFT and verify fail seat-model naming 20:46:21Z and req_011CevQvLvpbLcLv2GE49WA4; (b) the same fixture with the model restored on a later turn clears it; (c) a transcript with no drift prints model=row and verify passes; (d) run against the live tree, the check reports the current state of every seated row correctly, pasted. DISPROVED BY: any drifted seat that verify still passes, or a repair path that rewrites the row or restarts the seat — the fix is a human's or the owner's, the tool only tells. HARD RULES: rotate.py, commands.py and verification.py are build nodes, edit through write.py; no new bin/*.py; identity is supplied — the transcript is resolved from the row's session_ref and pin, never from the newest file in a directory (trap 0c); the check must not open a transcript it cannot map to a row."
thought_session: f3b92df1
title: A seat's live model is read from its transcript, not assumed from its row — drift is reported, never silent
---
<!-- BODY:BEGIN -->
# hypothesis:l4-a-seats-live-model-is-measured-not-assumed

## Hypothesis

What is the testable claim? What would prove it? What would disprove it?
