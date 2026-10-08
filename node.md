---
id: hypothesis:l4-town-scoped-goal-numbering-the-address-carries-the-town-tag
mint_id: abde8f5a608a47a78c963972f959896c
type: hypothesis
parents:
  - goal:g6.16
next_edges: []
edited_by: belam
scaffold_hash: 9c5a213eb98a867d
season: 2
testable_claim: "Owner 2026-09-16 06:02Z (doc:l4-owner-decisions tail): a goal that breaks off into a town drops its global season number -- each town hosts its own g1, g2 and so on. Claim: identity stays the mint_id (never changes), and the goal ADDRESS carries the town, derived from the town tag, so two townscoped g1 goals never collide in goal: address space. Ladder towns at mint time: core, streaming-suite, web-app-suite, local-maxxing -- no collision found by the grep the owner ordered (1 hit, schemas/[config].md:21, enc columns)."
thought_session: dissolve-legacy-2026-09-19
title: L4 town scoped goal numbering the address carries the town tag
town: core
---
<!-- BODY:BEGIN -->
# hypothesis:l4-town-scoped-goal-numbering-the-address-carries-the-town-tag

## Hypothesis

What is the testable claim? What would prove it? What would disprove it?

## Agent Notes
L4 CLOSE TRIAGE (belam gen 24, 2026-09-16 16:3xZ; workflow g15-close-triage wf_b1179398-7ab, reader + adversarial refuter on season2/main eb21d601f): KEEP for the next stream (KEEP) -- live defect: Owner ruling at doc:l4-owner-decisions.md:821 ("each town hosts its own g1, g2, g3") explicitly DEFERRED out of L4 close at :894 ("(5) town goal numbering are DEFERRED"); MEASURED no later line re-rules it (grep past :894 = 0); goal files still number globally (g18.md:19 town: web-app-suite, g18.1.md:19 town: streaming-suite, `ls .agi/nodes/goal/` all g<N> global); snapshot-goals.py:713-716 groups by town for rendering only, no town-scoped address. Deferred is not retired. EVIDENCE: doc:l4-owner-decisions.md:821, :894; goal/g18.md:19; goal/g18.1.md:19; snapshot-goals.py:713-716 Never rounded at close (owner 14:1xZ).
