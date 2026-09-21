---
id: hypothesis:l4-an-undeclared-town-is-refused-not-capped
mint_id: cd25cd363ccc4a3eafd537ae3c7232d3
type: hypothesis
parents:
  - goal:g15
  - hypothesis:l4-write-path-vision-cap-reads-the-visions-own-town
next_edges: []
edited_by: sanctuary-director
scaffold_hash: ca7d832d090b3391
season: 2
testable_claim: "OWNER 2026-09-11 05:1xZ: bugfix/optimization findings are g15 hypothesis nodes fixed in-loop. Source: merge-up 29 review by name (wf_ad872f68-50a, 14 agents), goal:g15 newest note at f477e63bd/ee2000edc; line numbers on 2b4f33ed4. Proposed by the prime's ruling, minted by sanctuary-director gen XII 07:4xZ. g15-22: spawn_gate.py:1177 — the vision's own town cell is read without validating the town against the ladder's declared towns, so an undeclared town gets a fresh cap: reproduced by the review (`town: nowhere-declared` -> APPROVED). CLAIM: the write path refuses a vision whose `town` is absent from `.geometry/ladder.md`'s towns table with a named refusal (`town X not declared in ladder towns`); declared towns keep their own cell; the reproduction now reads REFUSED. TESTS: fixture ladder with two towns; vision town=nowhere -> REFUSED naming the town; town=streaming -> its own cell as before; no town -> the existing default. FALSIFIER: an undeclared town APPROVED. CEILING: 1 kid. FILE SCOPE: extensions/agi/bin/spawn_gate.py (the town-cell lookup ONLY) + its tests. EXCLUDED: everything else, incl. spawn_gate.py:705."
thought_session: sanctuary-director-gen12
title: "spawn_gate.py: a vision naming a town the ladder does not declare is REFUSED, not granted a fresh cap"
town: core
---
<!-- BODY:BEGIN -->
# hypothesis:l4-an-undeclared-town-is-refused-not-capped

## Hypothesis

What is the testable claim? What would prove it? What would disprove it?

## Agent Notes
OWNER 2026-09-11 05:1xZ: bugfix/optimization findings are g15 hypothesis nodes fixed in-loop. Source: merge-up 29 review by name (wf_ad872f68-50a, 14 agents), goal:g15 newest note at f477e63bd/ee2000edc; line numbers on 2b4f33ed4. Proposed by the prime's ruling, minted by sanctuary-director gen XII 07:4xZ. g15-22: spawn_gate.py:1177 — the vision's own town cell is read without validating the town against the ladder's declared towns, so an undeclared town gets a fresh cap: reproduced by the review (`town: nowhere-declared` -> APPROVED). CLAIM: the write path refuses a vision whose `town` is absent from `.geometry/ladder.md`'s towns table with a named refusal (`town X not declared in ladder towns`); declared towns keep their own cell; the reproduction now reads REFUSED. TESTS: fixture ladder with two towns; vision town=nowhere -> REFUSED naming the town; town=streaming -> its own cell as before; no town -> the existing default. FALSIFIER: an undeclared town APPROVED. CEILING: 1 kid. FILE SCOPE: extensions/agi/bin/spawn_gate.py (the town-cell lookup ONLY) + its tests. EXCLUDED: everything else, incl. spawn_gate.py:705.
