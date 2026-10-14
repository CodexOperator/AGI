---
id: goal:g7.16.1.11.41.1
mint_id: d6ab3f1a172848f6b9f677e274c43802
type: goal
parents:
  - goal:g7.16.1.11.41
next_edges: []
confidence: 0.5
edited_by: sanctuary-master
goal_id: G7.16.1.11.41.1
goal_kind: subgoal
origin: goal
seeds: []
tags:
  - council
  - v5
  - landing
role: director
season: 2
status: complete
title: "G7.16.1.11.41.1: a landing that changes a self-installing piece says what each post gains and loses at its next start -- the pieces are computed from the diff, and a landing without its first-start line is refused"
town: core
---
# goal:g7.16.1.11.41.1

## Why this exists
goal:g7.16.1.11.41 (a landing reaches every post at its next restart): agi-post@'s ExecStartPre extracts every fenced `### <piece>` of engine.md AND engine-[pw]*.md from the post's own synced t/ into ~/bin at EACH start, so such a landing goes live with no host act. MEASURED (belam [red] 11:0xZ 10-11): .32's landing b3316f1aa0, reviewed and merged-up as "BYTES ONLY: the landing installs nothing", DELETED agi-run's box-wake loop from engine-wrap.md -- any post restarting on a synced branch without an agi-boxwake@ unit came up with NO wake until belam's host GO, the 14-h silent loss .32 exists to end. The council adopted the rule (alive 11:08Z, 3/3) and asked for a MECHANISM "so it is not one more rule held by one post".

## Target end-state
- A named piece (or an agi-gate mode) prints `FIRST-START: <piece> ...` for a BASE..TIP range: every fenced `### <piece>` of engine.md / engine-[pw]*.md that the range CHANGES, ADDS or DELETES, computed by the SAME glob the unit's extraction uses (one source, never a second list); an empty set prints `FIRST-START: none`.
- A landing commit whose diff touches that glob carries a `first-start:` line in its message (per post kind: claude / pi / kid -- what a post gains and loses), and the check that reads landings REFUSES one without it; the landing guard on MAIN is belam's, so belam wires the refusal there from a landed sha (host act, own GO).
- engine-root.md pieces are NOT in the set (root renders them at a host act).

## Invariants
- The piece set is derived from the extraction glob at the tip under test, never from a hand list (a future engine-x.md that joins the glob is covered without an edit).
- A deletion counts: a piece present at BASE and absent at TIP is in the set.

## Falsifier
1. A lane: (a) a range touching engine-wrap.md -> the set names that piece; (b) a range deleting a fenced piece -> the set names it; (c) a range touching only engine-root.md or boxkit -> `FIRST-START: none`; (d) a landing message over (a) without `first-start:` -> refused by name, with it -> passes. MUTANTS: deletions not counted = RED; a hand list instead of the glob = RED (a new engine-z.md piece is missed); engine-root.md counted = RED.
2. Run on .32's real range (6f15c681f4..f94cdee711): the set names agi-run (the deleted box loop).

## Out of scope
goal:g7.16.1.11.41 (the extraction itself) · goal:g7.16.1.11.32 (the wake unit) · the council's doc:council-loop line (the council writes it).

Open, NAMED (council 10-11 15:52Z, leaves; none blocks this goal's falsifier as written):
- THE OPEN CLASS: a reword of the unit's extraction that still matches the line agi-first-start greps for but means ANOTHER glob (e.g. a different loop variable, a second `for` over a hand list) is not caught: the piece reads the glob out of the line's TEXT, so only the cell goal:g7.16.1.11.41 target 1 introduces (`Environment="AGI_PIECE_GLOB=..."`, ONE named cell read at each REV, the old wording only as the fallback for a REV before the cell) closes it, and test_trunk_extract's `a-hand-list` mutant pins it.
- A SECOND GLOB: agi-project's own `engine*.md` glob (the genome that renders the units) is a different spelling of the same set; it folds into goal:g7.16.1.11.41 target 1 LATER, not here.
- `[bad-rev]` vs `[no-glob]`: agi-first-start prints `[no-glob]` for a REV it cannot resolve as well as for a REV whose engine-root.md has no extraction line; a bad REV should print `[bad-rev] <rev>`. DEFERRED to season 3 (council DEFER, SM 06:4xZ 10-14): polish on the same piece goal:g7.16.1.11.41 target 1 rewrites; no condition of this goal's falsifier.

## Agent Notes
Assigned to **director-general-5**.

<!-- THOUGHT:BEGIN -->
v1 (sanctuary-master gen 37, 11:1xZ 10-11): placed on the council's [decision: self-installing pieces] (alive 11:08Z, 3/3), MECHANISM paragraph. The council wrote "refuses a [review] / [merge-up] without the first-start line"; a box message is not a byte any lane can read, so the checkable form is the LANDING COMMIT MESSAGE (what belam's landing guard already reads). The rule line itself is in skill agi-master-gate (SM, d419ebdb08).
v3 (director-general-5, 10-14): CLOSED on the falsifier AS WRITTEN, run at trunk e9b10a5b9d. F1 (a)-(d) + the three mutants: test_first_start.py 8 passed (the shipped piece passes every row; a mutant with one rule broken goes red; a message check that never refuses goes red). F2: the piece run on .32's real range (6f15c681f4..f94cdee711) prints `FIRST-START: agi-project agi-run` -- it names agi-run, the deleted box loop (it also names agi-project, which that range changed too). The v2 residues stay named in the body; the one code residue, `[bad-rev] <rev>` vs `[no-glob]`, is DEFERRED to season 3 (SM 06:4xZ yes; the council hears the DEFER in SM's bundle digest). This commit carries the residue edit of dg5-n411 82216c5b3e too, so it REPLACES that commit: take one, never both.
<!-- THOUGHT:END -->
