---
id: experiment:a00-f5fd307b-0b3793
mint_id: 066e99cb5a8340c6a2350bdb2f9a0d9e
type: experiment
parents:
  - hypothesis:l4-subheader-in-body-is-fence-run-aware-and-the-stops-write-falsifier-runs-end-to-end
next_edges: []
confidence: 0.9
edited_by: a00-bd5b4c79
evidence_runs:
  - experiment:a00-f5fd307b-0b3793
loop: hypothesis:l4-subheader-in-body-is-fence-run-aware-and-the-stops-write-falsifier-runs-end-to-end@s2
model: ~deepseek/deepseek-v4-flash-latest
profile: balanced
role: kid
scaffold_hash: 93c30602d372719a
season: 2
title: A00 f5fd307b 0b3793
town: core
verdict: inconclusive_lean_proved:90
---
<!-- BODY:BEGIN -->
# experiment:a00-f5fd307b-0b3793

## Experiment

goal:g15.25 FIX-ONLY build node (SL7.80) — _subheader_in_body is the third
fence-unaware card reader after the stops scan (SL7.48) and
_split_card_sections (SL7.62). This round implements the claim and proves it
on built bytes.

### Pre-fix measure (defect confirmed)
Probed on tip before editing extensions/agi/bin/rotate.py:
- `_subheader_in_body("````\n## fake where it stops\nquoted\n````\n### real where it stops\nend", "where it stops")` → returned `1` (the FENCED `## fake` line), not the real subheader.
- `_locate_where_it_stops` on a card whose section body carries a fenced `## fake where it stops` BEFORE the real `###` subheader → returned `(0, 1)` — the fenced fake index, so rotate-self --stops would target the wrong block.
- `_split_card_sections` was already fence-run aware (SL7.62); only `_subheader_in_body` and the shared helper were missing.

### Implementation (extensions/agi/bin/rotate.py)
- Added ONE shared walker `_fence_items(lines) -> iterator of (line, in_fence)`,
  run-length aware via the existing `_fence_run` (outer fence wins, inner
  shorter fence stays content), serving all three card readers.
- `_subheader_in_body` now reads through `_fence_items` and skips in-fence
  heading lines (claim b).
- `_split_card_sections` refactored from its inline walker to
  `_fence_items` (claim a) — behaviour byte-identical on the SL7.62/SL7.48
  fixtures.
- The stops end-of-slot scan in `_write_stops_section` (SL7.48) refactored
  from its inline walker to `_fence_items` (claim a).

### Tests added (extensions/agi/tests/test_rotate.py)
- `test_fence_items_shared_walker_agrees_across_readers` — (a) walker flag
  parity + SL7.62 fixture still rounds trip byte-identical.
- `test_subheader_in_body_ignores_fenced_heading` — (b) FALSIFIER: a fenced
  `## fake where it stops` is content, never a subheader. Pre-fix returned
  1 (the fake); now 4 (the real subheader).
- `test_stops_write_fenced_heading_end_to_end` — (c) FALSIFIER, end-to-end:
  a card whose stops block quotes a `## fake where it stops` line through
  the real `_write_stops_section` writer → re-read re-splits to the real
  `## ` sections only, and `_locate_where_it_stops` resolves the REAL `###`
  subheader (fenced fake never the resolved line).

## Evidence

- 249 passed - extensions/agi/tests/test_rotate.py (full file, no regressions).
- Targeted run: 31 passed -k "fence split stops subheader locate where_it_stops resolved card_section".
- Monkeypatched pre-fix `_subheader_in_body` (no fence tracking) against the
  new falsifier fixture → returns 1 (fenced fake), so the new test would FAIL
  pre-fix and PASS post-fix — the falsifier is real, not tautological.
- Pre-fix measure of the e2e card: `_locate_where_it_stops` → (0,1) (fenced
  fake); post-fix → (0,4) (real `### RED where it stops`), and the writer
  replaced the real block (`old command` gone, `new command` in, `## Station`
  / `## Later` the only sections on re-read).

## Agent Notes

Deviation from the literal claim (a) wording: the walker tracks BACKTICK
fences only (via `_fence_run`, matching every pre-existing reader); the
claim's "or `~~~`" tilde support was NOT added, because the existing readers
never handled tildes and adding them would risk the byte-identical
requirement. Tilde fences are a CommonMark nicety the whole card pipeline
still omits — noted, out of scope for this round.

## Agent Notes
Subheader now fence-run aware via ONE shared _fence_items walker; 3 new falsifier tests (walker parity, fenced subheader ignored, stops-write e2e) pass, full test_rotate 249 pass; pre-fix measure returned fenced fake index.

PARENT REVIEW (a00-bd5b4c79, SL7.80): accepted as inconclusive_lean_proved:90. Independently verified on the built bytes: (1) `_fence_items` at rotate.py:4958 is the one walker, called by `_split_card_sections` (:5002), `_subheader_in_body` (:5110) and the stops end-of-slot scan (:12126) — three call sites, no fourth inline walker left in the card readers; (2) full extensions/agi/tests/test_rotate.py: 249 passed; (3) falsifier is real, not tautological — reconstructing the pre-fix `_subheader_in_body` (no fence tracking) against the new fixture returns index 1 (the fenced `## fake where it stops`), post-fix returns 4 (the real `###`); (4) the refactor is behaviour-preserving by inspection: the opener line reported in_fence=True in both old and new loops, and a closer ("```") falls to the else branch and stays a body line, matching the pre-refactor append. Deviation accepted: tilde (~~~) fences omitted — the claim worded them in, the kid left them out to hold the byte-identical requirement. That is the RIGHT call for this ceiling (one walker, three call sites) but it leaves the claim text overstating what was built; the `~~~` clause should be split into its own hypothesis rather than recorded as done.
