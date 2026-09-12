---
id: hypothesis:l4-a-veto-freezes-never-frees
mint_id: b18c1640c16e4fa0a5b532218815f144
type: hypothesis
parents:
  - goal:g15
next_edges: []
edited_by: sanctuary-director
scaffold_hash: bb7993f1c93b3bce
season: 2
testable_claim: "OWNER 2026-09-11 20:3x-21:4xZ (the eight rungs, verbatim in doc:l4-owner-decisions; vision:web-app-suite db436e1f1: 'Rungs 1-4 are live as goal lines under goal:g15 at the Sanctuary director'). Proposed by sanctuary-director 214458Z 01:33Z, ACCEPTED by Prime XIII 01:33Z: 'mint the three hypothesis nodes now (parents goal:g15, town all) but do NOT dispatch until rung 1's F1-F4 land at the sensei-director (rung 2 sits behind enforcing)'. HELD -- not dispatched. RUNG 3, owner verbatim: 'Veto / human gate. Council + Keep majority flips `human_gate` on the Prime's scope; vetoes expire, are rate-limited and logged; an unanswered gate freezes, never frees.' CLAIM: (1) `human_gate` is a cell on the Prime's config row (owner-written) that, when set, makes every Prime-scope act that the ladder marks gated (a merge-up push, a config:posts edit outside self_row, a rotation of another post) wait for an owner line in a named room; (2) a VETO is a signed decision record (rung 2's shape) from a council + Keep majority that SETS human_gate for a stated scope with an expiry; a veto past its expiry is inert, a post may file at most N vetoes per window (rate-limited by the geometry node), and every veto/expiry/answer is logged to one file; (3) an UNANSWERED gate FREEZES the gated act -- it is never auto-released by a timeout, a restart, or a rotation -- and the freeze is visible in `viewport --live` and the rotation record; (4) tests on fixtures: a majority veto gates; a minority does not; an expired veto is inert; the rate limit refuses the N+1th; an unanswered gate stays frozen across a simulated rotation. Ceiling and file scope are set when the round is cut; serial behind rung 2."
title: "RUNG 3 (held): veto / human gate -- council + Keep majority flips human_gate on the Prime's scope; vetoes expire, are rate-limited and logged; an unanswered gate freezes, never frees"
town: all
---
<!-- BODY:BEGIN -->
# hypothesis:l4-a-veto-freezes-never-frees

## Hypothesis

What is the testable claim? What would prove it? What would disprove it?

## Agent Notes
GO (Prime XVI 49ddab, 14:20Z, signed): rungs 2-4 released; this rung (3) is cut AFTER L4.324 (rung 2) lands, because a veto is a rung-2 decision record. FILE SCOPE at that time: not cli.py / branches.py / the four rename test files (L4.322/L4.323); fixtures only against posts.md, the real tree is read, not written.

CUT (sanctuary-director 114003Z, 15:16:12Z) as L4.325, a pi parent, after rung 2 landed on the seat (d3d8ae24f: src/seatsig/rings.py -- canonical_bytes, decision_cell, load_rings, ring_by_name, verify_ring; the veto record IS a rings.decision_cell of kind veto over the FULL decision fields, verified by rings.verify_ring, never new crypto). FILE SCOPE: src/seatsig/ (a veto module may be added beside rings.py), write.py (the human_gate cell on the Prime's row + the config-edit gate), verification.py (the merge-up push gate), rotate.py (rotating ANOTHER post is a gated act), viewport.py (the freeze is visible in --live), send.py (the named room + the veto verb), one geometry node for rate limits/expiry, the rotation record field, and NEW test files only (test_veto.py or similar) -- do NOT edit test_rings.py, cli.py, branches.py, dispatch.py's ring gate, or any rename test file; rung 4 (L4.326) follows this round serially and owns send.py keygen --onboard, dispatch.py's spawner refusal and the tier/budget cells -- leave those untouched. Fixtures only: never set human_gate, file a veto or write a room against the real posts.md/seats.md; the real tree is read, not written. PROOF/DISPROOF as the claim states; a kid stops at lean_proved when a conjunct is fixture-proved but not live-exercised, and says so.
