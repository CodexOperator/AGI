---
id: hypothesis:a00-abd94427-d2294b
mint_id: 0dba89737f224f7b852acc8f2af9e25e
type: hypothesis
parents:
  - goal:s33
next_edges: []
confidence: 0.0
scaffold_hash: a0d57dd8a52279e5
testable_claim: The falsifier grep can drive a single-pass doc sweep to zero, the stale-names gate (retired references in non-retired prose) is a tractable set under 20 targets, and no section contains a stale reference that is also semantically important enough to keep.
title: Doc sweep via falsifier-driven fix
verdict: pending
---
# hypothesis:a00-abd94427-d2294b

## Hypothesis

**Claim:** The falsifier grep test described in goal:s33 (grepping for retired names: `render-context.py`, `payloads/`, `grid.py checkout` as a live command, `context/kits` — failing on any hit outside a sentence that marks it retired) can drive a complete single-pass doc sweep across all four target files (QUICKSTART.md, CLAUDE.md, skills/agi/SKILL.md, HANDOFF.md §5) to zero stale references.

**What would prove it:**

1. Run the falsifier grep before any edits — record the full hit list per file.
2. Perform one targeted sweep: each hit is either (a) replaced with the current term/claim, (b) wrapped in a retired-marker sentence, or (c) deleted if the whole section is obsolete.
3. Run the falsifier again — zero hits outside retired-marker sentences.
4. Manual spot-check: no new inaccuracies were introduced by the sweep (each changed line is read and verified against the current tree).

If (3) and (4) both pass, the hypothesis is proved: the falsifier-driven approach works in one pass.

**What would disprove it:**

- The falsifier still returns non-zero hits after the sweep (missed or misclassified stale references).
- The sweep introduces new stale content (e.g. updating one section but missing a cross-reference in another doc).
- A stale reference is found that is semantically important (it documents a real, intentional historical decision and removing it loses meaning) — proving that some stale references are *content*, not drift.
- The hit list exceeds ~20 unique targets across all four files, indicating the drift is deeper than a tractable set of retired names and requires structural rewriting rather than targeted replacement.

**Why this hypothesis:** The goal's own falsifier is an explicit grep gate. The question is whether the drift is *shallow* (a few retired names scattered in otherwise-current prose) or *deep* (stale claims embedded in the structure). If shallow, a falsifier-driven fix in one pass is the most efficient approach and worth proving so future iterations reuse the pattern. If deep, the goal needs a different strategy (full rewrites per doc), and knowing that early prevents wasted effort.

<!-- THOUGHT:BEGIN — authored, not derived; carried across regenerating scans. The reasoning behind THIS version. -->
Initial hypothesis spawned from goal:s33. The goal body explicitly names a falsifier (grep for retired names) and asks for a sweep. This hypothesis tests whether the falsifier-driven approach is sufficient in one pass — the most actionable claim for the next step (experiment → verdict). If proved, a single experiment runs the sweep and checks the falsifier; if disproved, the experiment reveals what deeper structure needs rewriting.
<!-- THOUGHT:END -->


## Agent Notes
Hypothesis: falsifier-driven grep can drive single-pass doc sweep to zero under goal:s33. Tests whether drift is shallow (tractable set <20 retired names) or deep (needs structural rewrite). No experiment run yet — pending.
