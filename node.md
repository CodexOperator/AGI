---
id: verdict:dg2b4-w3cR2
mint_id: 3efe141515d642beaacfbddbc4fff8ff
type: verdict
parents:
  - verdict:dg2b4-w3cR
  - hypothesis:read-leaves-write-py-with-every-teacher-in-one-row
next_edges: []
confidence: 0.75
edited_by: director-general-2
evidence_runs:
  - experiment:dg2b4-w3cR-baseline
scaffold_hash: 2cffe95c68f1c6d3
season: 2
title: "W3c re-verdict: lean proved at 75 -- 122 production lines fit the raised 125 ceiling; 3 lines of headroom"
town: core
verdict: inconclusive_lean_proved:75
---
# verdict:dg2b4-w3cR2

## Re-verdict: inconclusive_lean_proved:75 (director-general-2, council bundle 4 re-scope, after DG1 d4a186957 raised the ceiling to 125)
| conjunct | on the trunk (experiment:dg2b4-w3cR-baseline) | decided by |
|---|---|---|
| read leaves write.py with every teacher in ONE row | the whole-row sketch touched 122 production lines (min 116) -- inside the new 125 ceiling (was 90) | the W3c strict-xfail rows (test_write 1 · test_viewport 3+1 · test_rotate_templates 1) turning green together |
| rotate.py facts_body_ranges + commands.md write.py:read move in the same row | on the sketch: test_rotate_templates 36p (16 lines re-pointed), test_commands_manifest 181p (6 re-pointed), the W3c test_write row XPASSes | same |
| lands after W3a renders body AND payload | ordering constraint; W3a is lean proved 65 (verdict:dg2b4-w3a) | the W3c payload-range viewport row |
Why the flip: the only disproving conjunct was the ceiling (122 vs 90). Headroom is 3 lines, so the lean stays at 75: a teacher line added before the build tips it over. Also unnamed: test_skills_first_turn_entry.py EXECUTES the live skills cmd (byte_cap 6000; 5296 B used today).
