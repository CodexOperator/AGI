---
id: hypothesis:l4-no-role-template-documents-a-hand-setup-step-every-per-spawn-setup-is-a-first-turn-after-join-entry-or-a-spawn-write
mint_id: 1b0212006e584fbfad67f36cd340617f
type: hypothesis
parents:
  - goal:g15
next_edges: []
edited_by: sensei-director
scaffold_hash: b3ae189b98485c2f
season: 2
testable_claim: "goal:g15 FIX-ONLY node (owner order 15:4xZ relayed by master-sensei gen 4 (15:41Z; verbatim at doc:l4-owner-decisions latest note); cite at seat tip 290644b2b, re-measure on your base. line (3); owner verbatim to the Sensei: 'meter pin and the other 2 calls sound like something that can happen automatically as part of rotation for every role'). MEASURED: the meter pin IS written at spawn (F8; master-sensei.meter mtime 15:33:13Z = its rotation) yet the Sensei's card still said 'one setup call' and gen 4 paid it — the documented step outlived the code. nodes/.geometry/rotations.md holds the role templates (startup: at :52/:91, first_turn: at :54/:93, after_join: at :64/:105 for the first two roles; four roles in all). CLAIM: an audit of all four templates (their startup/first_turn/after_join lists AND the prose fields a post reads at wake) finds every remaining 'run X once at wake / by hand / setup' instruction and turns each into a first_turn or after_join entry (or a spawn-time write in rotate-self) or deletes it as already automatic; the kid node lists each finding with its disposition; a test asserts no template field matches the hand-step vocabulary (setup call, by hand, run once, pin the meter, ListAgents once) except inside a first_turn/after_join command string. FALSIFIERS: a template prose field still tells a post to run a setup command; a first_turn entry added refuses under _producing_refusal (F12: judge in-process); the guard test passes on a template that says 'by hand'. TESTS: test_rotate_templates.py — the vocabulary guard; every added entry judged with _resolve_startup_placeholders + _producing_refusal == None. FILE SCOPE: nodes/.geometry/rotations.md (the four templates); extensions/agi/bin/rotate.py only if a spawn-time write is needed; extensions/agi/tests/test_rotate_templates.py. EXCLUDED: the seats' own cards, the F-facts prose beyond the audited sentences, the meter hook (its own node). CEILING: one audit pass over four templates, one guard test."
thought_session: sensei-director-genXIII-L13
title: the four role templates in config:rotations carry no documented hand setup — every per-spawn setup a post needs is a first_turn/after_join entry or a spawn-time write, audited and closed with a test that greps the templates for hand-step wording
town: core
---
<!-- BODY:BEGIN -->
# hypothesis:l4-no-role-template-documents-a-hand-setup-step-every-per-spawn-setup-is-a-first-turn-after-join-entry-or-a-spawn-write

## Hypothesis

What is the testable claim? What would prove it? What would disprove it?
