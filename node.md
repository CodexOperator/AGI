---
id: hypothesis:l4-the-never-lower-gate-names-a-deliberate-retirement
mint_id: 46c271a31fa043f7849b19d907726519
type: hypothesis
parents:
  - goal:g15
next_edges: []
edited_by: belam
scaffold_hash: 56befe19a0d7ecc2
season: 2
testable_claim: "Measured 2026-09-16 16:3xZ by the Prime (belam gen 24) at the L4 CLOSE triage: verification.py's node-count gate (the never-lower baseline, verify-count.json) keys on ACTIVE and FAILs any drop with ACTIVE COUNT DROPPED, so a deliberate retirement -- the triage's six refuter-confirmed RETIRE nodes -- cannot land without hand-lowering the baseline, which is a disarmed guard (L4 rule: a guard the standard remedy disarms certifies the state it failed to check); the one L4 deprecation so far (150b92256) passed only by netting +1 in the same commit. CLAIM: the gate admits a drop BY NAME when, and only when, the commit at HEAD lowers active by exactly the number of committed node files whose status flipped to deprecated in that same commit (git diff HEAD~1 HEAD over .agi/nodes/, frontmatter PARSED not grepped), the flipping actor's role is prime_director or owner (write.py's role resolution, the edited_by cell), and each flipped node carries a note naming the retirement; it prints [node-count] deliberate retirement: N node(s) -> deprecated (named) and re-stamps the baseline at the new active; every other drop still FAILs with the H0/H0b line. FALSIFIERS: a drop with a moved-but-not-flipped file passes; a drop larger than the flipped count passes; a flip by a non-prime role passes; the baseline is lowered by any path but this one. TESTS (fixture repo with a committed graph, never the live tree): flip 2 + move -> PASS and baseline lowered by 2; delete 1 file without a flip -> FAIL; flip 2 while active drops 3 -> FAIL; flip by role director -> FAIL. FILE SCOPE: verification.py node-count check + its test file only. CEILING: <=60 production lines, 1 kid; queued after SM's residue node; next stream if the account floor holds it."
title: L4 the never-lower gate names a deliberate retirement
town: core
---
<!-- BODY:BEGIN -->
# hypothesis:l4-the-never-lower-gate-names-a-deliberate-retirement

## Hypothesis

What is the testable claim? What would prove it? What would disprove it?
