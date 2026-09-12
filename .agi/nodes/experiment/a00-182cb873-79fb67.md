---
id: experiment:a00-182cb873-79fb67
mint_id: 5c16941ac05648cbb66ac6acfd99e59f
type: experiment
parents:
  - hypothesis:l4-the-own-row-cut-classifies-each-changed-line-by-row-identity-and-owns-the-edited-by-stamp-only-beside-an-own-row-change
next_edges: []
confidence: 0.95
edited_by: a00-64e88bf7
evidence_runs:
  - experiment:a00-182cb873-79fb67
loop: hypothesis:l4-the-own-row-cut-classifies-each-changed-line-by-row-identity-and-owns-the-edited-by-stamp-only-beside-an-own-row-change@s2
model: ~deepseek/deepseek-v4-flash-latest
profile: balanced
role: kid
scaffold_hash: a4736eec6cafdc15
season: 2
title: A00 182cb873 79fb67
town: core
verdict: proved
---
<!-- BODY:BEGIN -->
# experiment:a00-182cb873-79fb67

## Experiment

g15 BUILD claim (mur-SL2.15 lines (3)+(4)): implement the own-row cut fix in
`rotate.py`, then prove it on the built bytes. HEAD target 2451606d0, worktree
`a00-64e88bf7`; base line numbers per the hypothesis (5618-5690, 5432-5466,
5469, 5589-5615, 5909-5917, 10268).

**Pre-fix state (already measured by the parent):** `_seats_ownrow_content`
walked each difflib opcode and PAIRED `removed[k]` with `added[k]` BY INDEX,
with `is_own = own(old) or own(new)` — an own deleted line paired with a
foreign inserted/edited line at the same k staged the FOREIGN line as own.

**What I changed** (all in `extensions/agi/bin/rotate.py`):

1. `_own_row_line(line, seat, session_owns=False)` — a row line is own by its
   `name` cell ALONE (never by pairing); the frontmatter `edited_by:`
   stamp counts own ONLY when `session_owns` (clause b/c). Single definition,
   no re-spelling.
2. `_diff_owns_row` — gathers changed lines, computes `session_owns` = any
   own-row name-cell change, returns that (frontmatter alone never owns → a
   foreign-only `edited_by:` restamp reads FOREIGN).
3. `_seats_ownrow_content` — replaced the index `for k in range(...)` loop
   with `_merge_region`, which classifies each removed/added line ON ITS OWN
   by ROW IDENTITY: own removed → dropped, own added → kept, foreign removed
   → restored from HEAD, foreign added → never staged. Rows pair across a
   replace opcode by their `name` identity (diff never reorders), so an own
   and a foreign row edited in ONE opcode keep the own change and the foreign
   row byte-identical to HEAD in either order. Structural/frontmatter lines
   match positionally; equal opcodes are carried verbatim (the old code's
   `staged.extend(base_lines[b:i1])` was always empty because opcodes tile the
   sequences contiguously — equal lines had been re-emitted by the k-loop).
   `any_own` now skips `equal` opcodes in its own-line scan.

**Two real bugs found while building** (both fixed):
- the rewritten staging loop dropped equal (unchanged) frontmatter/context
  once the k-loop was removed — equal opcodes must be emitted explicitly;
- `session_owns` was computed over ALL opcodes including `equal`, so a
  foreign-only restamp (next to an unchanged own row) was read as OWN via the
  unchanged row line — the collector must skip `equal` regions.

## Evidence

**Verification (all green):** `pytest extensions/agi/tests/test_rotate.py
test_write_self_row.py test_session_start_seat_pre_spawn.py
test_session_start_bootstrap.py test_bin_help_smoke.py` → 271 passed, 3
skipped. Plus `test_rotate_identity_main.py test_rotate_first_decision.py
test_rotate_complete.py test_sensei_rotate_out_audit.py` (238 passed) and the
rest of `test_rotate*` (276 passed) to cover the SL6.09 / SL7.09 clause (4)
regression surface — all existing own-row assertions stay byte-identical and
green (hypothesis clause (d)).

**Direct clause checks (added 4 tests to test_rotate.py, all pass):**

- `test_own_row_cut_classifies_by_row_identity_not_index` — own + foreign row
  edited in ONE replace opcode, BOTH orders: staged content carries exactly
  the own change; the foreign row is byte-identical to HEAD (base blob);
  a foreign `"edited_by": "x"` cell is never staged.
- `test_own_row_cut_own_deletion_plus_foreign_change_and_insert` — own row
  DELETED + foreign row CHANGED + foreign row INSERTED: own deletion dropped,
  foreign change restored to HEAD bytes, foreign insert never staged.
- `test_own_row_cut_foreign_only_frontmatter_restamp_reads_foreign` — a
  foreign-only `edited_by:` restamp: `_diff_owns_row` False AND
  `_seats_ownrow_content` None (clause b negative).
- `test_own_row_cut_own_write_keeps_its_frontmatter_stamp` — own row change +
  its own `edited_by:` restamp stage BOTH (clause b positive / SL7.09 clause
  (4) regression guard: tree stays clean, no `M seats.md`).

The pre-fix defect (belam deleted, `other ... edited_by x` staged as own) is
verbatim the first clause-(a) test body; the built bytes now stage
`other` restored to HEAD and never the foreign line.

## Agent Notes
g15 build: reworked rotate.py own-row cut to classify each line by row identity (never index-pairing) and own the frontmatter edited_by stamp only beside an own-row change; 4 new clause tests + 271+238+276 green.

<!-- THOUGHT:BEGIN — authored, not derived; carried across regenerating scans. The reasoning behind THIS version. -->
PARENT REVIEW (a00-64e88bf7, SL7.20) — accepted as proved. Reviewed the ARTIFACT, not the report: git diff HEAD shows the three clause edits in extensions/agi/bin/rotate.py: (a) _seats_ownrow_content replaced the per-index `for k in range(max(len(removed),len(added)))` pairing with `_merge_region`, which classifies each removed/added line on its own by `"name"` row identity (own removed dropped, own added kept, foreign removed restored from HEAD, foreign added never staged, rows paired across a replace opcode by name); (b) _own_row_line now owns the frontmatter `edited_by:` stamp only when `session_owns` (same-diff own-row name-cell change), with _diff_owns_row computing that context and skipping `equal` opcodes; (c) both predicates still route through the single _own_row_line. Verified the pre-fix defect is gone on the parent's own repro (own belam row deleted + foreign other edited + foreign third inserted): staged content is HEAD-belam-dropped-free, foreign edited_by never staged, foreign insert never staged, foreign other row byte-identical to HEAD. Ran the claimed suites myself: test_rotate.py+write_self_row+session_start_seat_pre_spawn+session_start_bootstrap+bin_help_smoke+rotate_identity_main = 279 passed, 3 skipped; and the four new clause tests green. Gate: parents resolve, verdict proved, evidence_runs is a real LIST (self-cite is legal for an experiment).
<!-- THOUGHT:END -->
