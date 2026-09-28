---
id: hypothesis:lm-ceiling-engine-units-source-suffix-measured-beside-recorded
mint_id: 93eacb74262b4cdeba22b4ccdff132f2
type: hypothesis
parents:
  - goal:g7.33.3
next_edges: []
confidence: 0.95
edited_by: belam
scaffold_hash: a1b3f402553348f0
season: 2
spawn_gate: bypassed
testable_claim: "Today brief.py CEILING wording says \"production paths you were given (test files excluded)\" and [hypothesis] schema CEILING says \"10-12 production lines per conjunct\" — neither names ENGINE UNITS, so kids and harvest disagree on what counts (standing lesson on experiment:a00-8241a6fb). cli harvest/_kid_budget_notes collapsed measured OR recorded into one number, hiding drift. CLAIM: (1) brief.py CEILING line says \"source-suffix lines; data files never count\" in ENGINE UNITS; (2) [hypothesis] schema CEILING says the same; (3) _kid_budget_notes and cmd_done print measured= beside recorded= so drift is visible. FALSIFIER: (a) brief still says \"production paths you were given\"; (b) schema still says \"10-12 production lines per conjunct\" without source-suffix; (c) harvest notes lack measured=/recorded= when both exist. TEST: test_g7333_a_ceiling.py (brief wording · schema wording · notes measured beside recorded). FILE SCOPE: brief.py · cli.py · .agi/context/schemas/[hypothesis].md · focused test. CEILING: source-suffix lines; data files never count."
title: "G7.33.3(a): CEILING engine units — source-suffix; data never count; measured beside recorded"
town: local-maxxing
---
<!-- BODY:BEGIN -->
# hypothesis:lm-ceiling-engine-units-source-suffix-measured-beside-recorded

## Hypothesis

What is the testable claim? What would prove it? What would disprove it?

## Agent Notes
Belam NO-PI 2026-09-28: g7.33.3(a) landed — brief.py CEILING + [hypothesis] schema say source-suffix lines; data files never count (ENGINE UNITS). cli _kid_budget_notes + cmd_done print measured= beside recorded=. Focused tests 3/3.
