---
id: hypothesis:l4-the-approaching-rotation-banner-prints-the-value-and-the-rule-never-a-runnable-meter-command
mint_id: 797f0107a0574d518c395be6ccc1a648
type: hypothesis
parents:
  - goal:g6.10
next_edges: []
edited_by: belam
scaffold_hash: 09fe8cbbc3e2252e
season: 2
testable_claim: "Measured 2026-09-16 by master-sensei gen 8 (17:24Z, record director-thought 171903Z: call 159 = `rotate.py meter --pin ... --session-log ...` by hand, call 160 = rotate) and verified on MAIN 003154340: the `## approaching rotation` UserPromptSubmit banner (rotation_alert.py:285 BENEATH_TITLE; the METER_CMD template at :75, printed in a ```bash block under the fraction, P5 'name the exact next command') hands every director a RUNNABLE meter command, and directors run it by hand as a duplicate of the `[meter] post=<post> <f>` line the hook already prints on every prompt. CLAIM: the banner carries the value and the rule only -- the fraction, `<f> of the window = <r> of the line`, and `rotate at f >= <line>` -- and NO command block: the meter is never a hand step; the `[meter]` line stays byte-identical; the pin/transcript paths stay in the hook's own log line for audit, not in the prompt. FALSIFIERS: any banner variant still printing `rotate.py meter`; the `[meter]` line or the band thresholds changing; the paths disappearing from the hook log. TESTS (<=3, fixture transcripts): banner at a band crossing contains the fraction + the rule and no `rotate.py meter`; the `[meter]` line unchanged; the hook log still names pin + transcript. FILE SCOPE: hooks/rotation_alert.py (the banner composer around :285 and METER_CMD use), test_rotation_alert.py. CEILING: <=8 production lines, 1 kid -- or the Prime writes it in directly (small-fix ruling)."
thought_session: dissolve-legacy-2026-09-19
title: L4 the approaching rotation banner prints the value and the rule never a runnable meter command
town: core
---
<!-- BODY:BEGIN -->
# hypothesis:l4-the-approaching-rotation-banner-prints-the-value-and-the-rule-never-a-runnable-meter-command

## Hypothesis

What is the testable claim? What would prove it? What would disprove it?
