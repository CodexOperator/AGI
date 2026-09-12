---
id: hypothesis:l4-the-rotation-alert-hook-prints-one-compact-meter-line-on-every-prompt
mint_id: 4facb0ef08194dc6bcd1a719ed78d40b
type: hypothesis
parents:
  - goal:g15.25
next_edges: []
edited_by: sensei-director
scaffold_hash: 8a22a0bf84df6da4
season: 2
testable_claim: "goal:g15.25 FIX-ONLY node (owner order 15:4xZ relayed by master-sensei gen 4 (15:41Z; verbatim at doc:l4-owner-decisions latest note); cite at seat tip 290644b2b, re-measure on your base. second order, verbatim: 'the meter pinning should automatically print your context meter once everything else loads into it as part of what the model receives before it starts its turn'). MEASURED: extensions/agi/hooks/rotation_alert.py is the UserPromptSubmit hook (the last stdout a model sees per prompt); it computes the fraction on every prompt but P3 band-gates the output (BANDS :287-288, silent below the first band and once per band after; _emit :1040), and on turn 1 of a fresh spawn (no assistant usage yet) it returns 0 with nothing printed (the early returns at :950-:1008), so a wake shows no meter and every post runs rotate.py meter by hand — a class-(a) call per generation. CLAIM: on EVERY prompt the hook prints exactly one compact line '[meter] post=<post> <fraction 0.NNNN> (<tokens>/<window>) line=<threshold>' as its LAST stdout line, unconditionally; the existing band/escalation block is printed ABOVE it only when a band is crossed, exactly as today; on turn 1 with no assistant usage the fraction is ESTIMATED as (len(prompt from hook stdin) + transcript bytes) / 4 / window and labelled 'est.' so a wake never shows a blank; P6 stays fail-closed: no pin or no post prints the refusal reason line in place of a fraction, never a number; the F-facts and briefs that say 'read the meter' may then drop the sentence (name them in the kid node, edit none). FALSIFIERS: a prompt below the first band prints no [meter] line; the line is not the last stdout line; turn 1 prints blank or 0.0000 unlabelled; a missing pin prints a fraction; the band block is printed on a prompt that crossed no band. TESTS: test_rotation_alert.py — below-band prompt prints the line; band-crossing prompt prints block then line; turn-1 est.; missing pin refusal; existing tests unchanged. FILE SCOPE: extensions/agi/hooks/rotation_alert.py — main's emit path only; extensions/agi/tests/test_rotation_alert.py. EXCLUDED: the spawn/latch path (SL7.45/56/65), rotate.py meter, the ladder threshold source. CEILING: one always-on line, four tests."
thought_session: sensei-director-genXIII-L13
title: the UserPromptSubmit rotation-alert hook prints ONE compact meter line on every prompt unconditionally — '[meter] post=<post> <fraction> (<tokens>/<window>) line=<threshold>' — with the band block only at bands as now, a labelled est. on turn 1, and P6 fail-closed
town: core
---
<!-- BODY:BEGIN -->
# hypothesis:l4-the-rotation-alert-hook-prints-one-compact-meter-line-on-every-prompt

## Hypothesis

What is the testable claim? What would prove it? What would disprove it?
