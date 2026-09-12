---
id: hypothesis:l4-the-rotation-alert-hook-prints-one-compact-meter-line-on-every-prompt
mint_id: 4facb0ef08194dc6bcd1a719ed78d40b
type: hypothesis
parents:
  - goal:g15.25
next_edges: []
edited_by: a00-84f091be
scaffold_hash: 8a22a0bf84df6da4
season: 2
testable_claim: "goal:g15.25 FIX-ONLY node (owner order 15:4xZ relayed by master-sensei gen 4 (15:41Z; verbatim at doc:l4-owner-decisions latest note); cite at seat tip 290644b2b, re-measure on your base. second order, verbatim: 'the meter pinning should automatically print your context meter once everything else loads into it as part of what the model receives before it starts its turn'). MEASURED (pre-fix): extensions/agi/hooks/rotation_alert.py is the UserPromptSubmit hook (the last stdout a model sees per prompt); it computes the fraction on every prompt but P3 band-gates the output (BANDS :287-288, silent below the first band and once per band after; _emit :1040), and on turn 1 of a fresh spawn (no assistant usage yet) it returned 0 with nothing printed, so a wake showed no meter and every post ran rotate.py meter by hand — a class-(a) call per generation. CLAIM (BUILT SL7.70 by experiment:a00-7cee97dc-f7add2, 40/40 green, parent re-ran and re-probed): on every prompt INSIDE AN AGI PROJECT WITH A READABLE TRANSCRIPT the hook prints exactly one compact line '[meter] post=<post> <fraction 0.NNNN> (<tokens>/<window>) line=<threshold>' as its LAST stdout line; the existing band/escalation block is printed ABOVE it only when a band is crossed, exactly as today; on turn 1 with no assistant usage the fraction is ESTIMATED as (len(prompt from hook stdin) + transcript bytes) / 4 / window and labelled 'est.' so a wake never shows a blank, with no band block fired from an estimate; P6 stays fail-closed: no pin or no post prints the refusal reason line in place of a fraction, never a number. SCOPE, MEASURED BY THE PARENT AT SL7.70 (three live payloads against the built hook): the word 'unconditionally' is FALSE on exactly the paths the hook's own P7 requires to be silent — a transcript_path that does not exist on disk prints nothing on stdout (rc 0), and cwd outside an agi project prints nothing (rc 0). That silence is architecture, not a defect; experiment:a00-83d5d0e0-bcf35b pins it with tests so no later kid 'fixes' it into a meter line emitted into every session on this box. the F-facts and briefs that say 'read the meter' may then drop the sentence (name them in the kid node, edit none). FALSIFIERS: a prompt below the first band prints no [meter] line; the line is not the last stdout line; turn 1 prints blank or 0.0000 unlabelled; a missing pin prints a fraction; the band block is printed on a prompt that crossed no band. TESTS: test_rotation_alert.py — below-band prompt prints the line; band-crossing prompt prints block then line; turn-1 est.; missing pin refusal; P7 silence pin; existing tests unchanged. FILE SCOPE: extensions/agi/hooks/rotation_alert.py — main's emit path only; extensions/agi/tests/test_rotation_alert.py. EXCLUDED: the spawn/latch path (SL7.45/56/65), rotate.py meter, the ladder threshold source. CEILING: one always-on line, four tests."
thought_session: sensei-director-genXIII-L13
title: the UserPromptSubmit rotation-alert hook prints ONE compact meter line on every prompt unconditionally — '[meter] post=<post> <fraction> (<tokens>/<window>) line=<threshold>' — with the band block only at bands as now, a labelled est. on turn 1, and P6 fail-closed
town: core
---
<!-- BODY:BEGIN -->
# hypothesis:l4-the-rotation-alert-hook-prints-one-compact-meter-line-on-every-prompt

## Hypothesis

What is the testable claim? What would prove it? What would disprove it?
