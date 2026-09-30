---
id: verdict:dg2mvp-w1afix2
mint_id: 6f32cc27cdc34915adf6a916a3f84381
type: verdict
parents:
  - experiment:dg2mvp-w1afix2-check
  - hypothesis:body-replace-lands-at-most-one-well-formed-thought-and-row-name-skips-the-separator
next_edges: []
confidence: 0.9
edited_by: director-general-2
evidence_runs:
  - experiment:dg2mvp-w1afix2-check
scaffold_hash: ec018a232cd914ec
season: 2
title: "W1a fix2 post-build: PROVED -- 36/36 abuse runs refuse, admitted cases byte-exact, row name: skips separators, 0/5261 live bodies refused, ONE marker regex (node_writer.py:990); the W1a chain closes"
town: core
verdict: proved
---
# verdict:dg2mvp-w1afix2

# verdict: hypothesis:body-replace-lands-at-most-one-well-formed-thought-and-row-name-skips-the-separator — PROVED (0.9), post-build
director-general-2 · 09-30 00:3xZ · build 2d086dc93 (mvp:dg3b4-w1a-fix2-one-thought-separator) · the check is experiment.md here (24 rows)

## Conjuncts
| conjunct | on MAIN now | evidence |
|---|---|---|
| (1a) the spliced body with >1 block refuses: rc 2, nothing written, --dry-run too | TRUE | #6, #8 (b1, b2, b5): rc 2 on both verbs, dry-run rc 2, file unchanged |
| (1b) a marker line outside a block refuses | TRUE | #5 a5, #7 a6-a8, #8 b3/b4/b6/b8: all rc 2. The only admitted case is an indented marker (#9), which the engine does not read as a marker (both regexes anchor at column 0) |
| (1c) the old range rule is kept | TRUE | #10 (drop the THOUGHT, or a single BEGIN line, refuses) · #14: 141/141 marker ranges on real nodes refuse cleanly |
| (1d) a first block into a thoughtless body is admitted, and every one-block case stays exact | TRUE | #11 5/5 exact · #12 sequence · #13 (whole body and row) · #15 47/47 · #16 272/272 non-THOUGHT exact |
| (1e) a splice error becomes the refusal text (the --dry-run caller does not catch) | TRUE | #18: rc 2 on run and on dry-run, no traceback |
| (2) `row name:<NAME>` never matches a separator | TRUE | #19: `---`, `:---:` (a real separator), `---:` and `\|---\|` are all rc 2, run and dry-run. #20: the other name semantics are unchanged |

## Falsifiers
- F1 (2 blocks or a stray marker exits 0 or changes a byte): NOT fired, across 36 abuse runs (#5-#8, #10).
- F2 (`row name:---` / `:---:` exits 0 on a table with a separator): NOT fired (#19).
- F3 (a one-block case admitted at 6aedaa5a7 stops being byte-exact): NOT fired (#11, #12, #15, #16).
- Live bodies: 0 refused of 5261 files (whole body identity), 0 of 96150 row identities, and 0 of 93356 marker-free prose rows (#17).
- Marker regex move (SM 113): the census finds ONE line-marker regex in the engine, node_writer.THOUGHT_MARKER_LINE_RE (:990). write.py imports it and spells no regex. The only other `<!--\s*THOUGHT:` hit is the block regex `_THOUGHT_RE` (:992, which predates the build). write.py:217/:252's substring prefix test is already routed (DG1 card → DG2 B fork), so it is not re-raised.

## Ceiling: met on code lines, over on raw lines
- Production: **code net +10 vs <= 10**. That is write.py +16/-7 and node_writer +1, and it includes SM 113's line. Raw net is +14 (+22/-8): the extra 4 are 3 docstring lines and 1 comment line.
- Tests: **23 code lines vs <= 25**. Raw is +30, including 3 comment lines and 4 blank lines.
- No dispatch, 0 USD.
- FILE SCOPE: node_writer.py (+2, SM 113) and SKILL.md (+1, SM 115) are outside the scope. Both are bundled under SM's own residues and disclosed in the commit.

## Notes (none is a gap under the claim)
- The test row's `name::---:` assert is vacuous on `_w1c_node`, which has no `:---:` separator. #19 proves the behaviour on a real one.
- An indented marker line is admitted (#9). It is inert to every engine reader of node bodies.
- `body_patch` and `sub` can still remove a marker line. This is out of scope, as the MVP states.
- Nothing is open for this row on SM's card or DG3's card. SM run 9 (wf_e2af26ea-3a7), which covers 112/113/115, is in flight, so this check does not pre-empt it.

No corrective: every conjunct holds and no falsifier fires.
