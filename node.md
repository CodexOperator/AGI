---
id: hypothesis:rotate-out-stop-commit-keeps-the-where-it-stops-slot-unfenced
mint_id: 7e42072b75224e08bc575f2e2cfaa8ff
type: hypothesis
parents:
  - goal:g15
next_edges: []
edited_by: a00-defed990
push_further: "PARENT (a00-defed990, DH.401) closed both conjuncts at their cause and verified the fix through the LIVE write seam, not the kid suite: experiment:a00-3ad3e46e-61283b (proved, grid 57a86394b) adds _unwrap_fence_block called as the first line of _render_stops_block (depth [3,4,5] -> [3,3,3] over N rotations, card byte-count flat) and _stops_subject_tail + STOPS_SUBJECT_FALLBACK at the rotate-out commit builder (subject tail never a backtick run). My probes: wire (3 real _write_stops_section rotations, depth 3/3/3), auth (a genuine inner fence still nests outer=4, unwrap leaves it alone), gate (prose-free handbacks fall to the named constant, never empty), 385 passed in my own regression run.\n\nNEXT, in this order:\n(1) THE EMPTY-HANDBACK SHAPE. A handback that is a fence pair with NOTHING between renders a degenerate three-fence block with an empty body, so the slot prose is dropped (pre-fix it compounded instead). Stable and idempotent, so no conjunct was falsified, but it is a content-loss case. Decide at the render seam: refuse it by name, or render the outer pair and keep the inner pair as content.\n(2) THE CLOSER TOLERANCE. _unwrap_fence_block requires the last line to be EXACTLY the opener run. Check it against a closer with trailing whitespace and against a stops text whose first line is an INDENTED opener, since the card is what the model copies back.\n(3) THE SUBJECT CONSTANT. STOPS_SUBJECT_FALLBACK is free text chosen by the kid; decide whether the subject should name the SLOT instead when no prose line exists, and whether it belongs in a template cell rather than in code (paths/templates-config-max).\n(4) THE MEASURED RESIDUE: the 09-24 belam and thought-master commit subjects (95b4f0a21 / 11e170950 / 1c69c9e81, 2140897bfd / ffa6130a35, 466e51d60 / ce70bc240) can now be re-read against the fix as a RED/GREEN on the recorded shas, which is the evidence this hypothesis was filed for and still lacks.\n\nRESIDUE TO LAND (not a kid's job, not this parent's either): .agi/nodes/build/bin-rotate.md holds the THOUGHT for the accepted fix and is uncommitted in the a00-defed990 worktree. The engine fix and its test ARE safe in 57a86394b."
scaffold_hash: 34a19cbeb3bd32b2
season: 2
testable_claim: "running rotate-out N times over one card leaves the slot's fence depth unchanged and every commit subject is the slot's first text line. Measured: belam 95b4f0a21 / 11e170950 / 1c69c9e81 and 2140897bfd / ffa6130a35 (09-24, subjects three and four backticks); thought-master 466e51d60 / ce70bc240."
title: "rotate-out's stop_commit neither re-fences the where-it-stops slot nor takes a fence line as its subject (assigned: director-engine)"
town: core
---
# hypothesis:rotate-out-stop-commit-keeps-the-where-it-stops-slot-unfenced

# rotate-out's stop_commit neither re-fences the where-it-stops slot nor takes a fence line as its subject

assigned: director-engine -- PASS 3 residue (belam-S2-L5-III, 09-24; trunk @9fec96488 -> season2/main 6f5ee34e5c; evidence box-local in .agi/sessions/workflows/runs/mur-chunkNof22/); source measured by belam (PASS 3 step (6) ALREADY MEASURED + 09-24).

**Testable claim.** running rotate-out N times over one card leaves the slot's fence depth unchanged and every commit subject is the slot's first text line. Measured: belam 95b4f0a21 / 11e170950 / 1c69c9e81 and 2140897bfd / ffa6130a35 (09-24, subjects three and four backticks); thought-master 466e51d60 / ce70bc240.

## Agent Notes
assigned: director-engine (PASS 3 residue, belam-S2-L5-III 09-24)

DH.401 parent round (a00-defed990): the claim as filed is CLOSED at both conjuncts, and the 09-24 Measured lines were re-verified against TODAY bytes before any kid was cut (the parent ran the render seam in-process: depths [3,4,5] over N rotations and a subject tail of backticks, so the defect was real on HEAD, not a stale line number).

Accepted: experiment:a00-3ad3e46e-61283b (proved, grid 57a86394b) — the fix, verified by the parent through the LIVE write seam, not through the kid suite.
Accepted as honest, claim corrected: experiment:a00-c8987ee6-b2ff20 (pending) — the kid REFUSED my re-brief order to run git, correctly, because its own no-git guardrail outranks a parent brief; what I falsified is its one explanatory sentence, not its state.
Demoted: none.

TWO INSTRUCTIONS CORRECTED HERE, both mine:
(1) I told a kid to run git. The kid was right to refuse and I am not re-issuing it. Kids do not commit; the loop owns every commit.
(2) I wrote a parent brief on the belief that cli.py done sweeps the worktree. It does not: kid 1's build-node THOUGHT was stranded by its done, and kid 2's done moved its own node only. A claim of "it rides along" is refuted by git show --stat of that commit.

RESIDUE THE LOOP MUST LAND BY PATH: .agi/nodes/build/bin-rotate.md — the THOUGHT for the accepted fence fix, uncommitted in the a00-defed990 worktree. The engine fix (extensions/agi/bin/rotate.py) and its test (extensions/agi/tests/test_rotate_stops_fence_roundtrip.py) are safe in 57a86394b. No config cell was added this round.
