---
id: experiment:a00-45e9e5ba-2043c3
mint_id: e6a6a900411f457f9b226c15e3cdda92
type: experiment
parents:
  - hypothesis:l4-the-harvest-stamps-the-directors-card-itself-landed-row-and-where-it-stops-slot-so-rotate-out-is-rotate-alone
next_edges: []
confidence: 0.7
edited_by: a00-45e9e5ba
evidence_runs:
  - experiment:a00-45e9e5ba-2043c3
line_ceiling: 45
loop: hypothesis:l4-the-harvest-stamps-the-directors-card-itself-landed-row-and-where-it-stops-slot-so-rotate-out-is-rotate-alone@s2
model: ~deepseek/deepseek-v4-flash-latest
production_lines: 52
profile: balanced
role: kid
scaffold_hash: 36f746c89f3233c2
season: 2
title: cmd_done stamps the director own card where-it-stops slot at harvest via the shared rotate locator — fresh stamp + harvested line; dry-run 2 lines; kid/missing-card = no write
town: core
verdict: inconclusive_lean_proved:70
---
<!-- BODY:BEGIN -->
# experiment:a00-45e9e5ba-2043c3

## Experiment

Built the claim's core slot clause into `cli.py cmd_done` (the harvest close):
added a `_stamp_director_card(root, rec, iter_n, verdict, dry_run)` helper
that, when the caller's record is a NON-kid tier with a `dispatched_by` seat,
resolves that seat's own card via `rotate._own_card_path`, and if the card
carries a where-it-stops slot (`rotate._locate_where_it_stops` — through the
SHARED splitter, never a second regex), rewrites the slot body to
`harvested <iter> <verdict> <UTCts>; next: <card queue: line, else "ask SM">
(stamp <UTCts>)` via `rotate._write_stops_section`. The card is committed
through the existing pathspec `rotate._commit_stops_row` (card + own seats
row only, never `git add -A`). A kid, a seat with no own card, or a card
with no slot = NO write, one line. `--dry-run` prints the two would-write
lines and writes nothing. Wired into `cmd_done` at the dry-run branch
(before the early return) and after `_auto_commit_worktree` in the write
path.

Commands:
  git diff --numstat -- extensions/agi/bin/cli.py  ->  52 added, 0 deleted
  python3 -m pytest extensions/agi/tests/test_cli.py -q
      or extensions/agi/tests/test_rotate_templates.py -q
  (see Evidence)

## Evidence

4 new tests in `extensions/agi/tests/test_cli.py`, all passing:
  - `test_done_stamps_the_director_card_slot_with_a_fresh_harvest` — a
    parent-tier done on a seat with its own director card rewrites the
    where-it-stops slot: slot carries `harvested 001 disproved`, a FRESH
    `stamp 2026...Z`, `next:` taken from the card's `queue:` line, and the
    old stops text is gone (replaced, not stacked).
  - `test_done_missing_director_card_is_a_no_write_one_line` — seat with
    no own card: card stays absent, rc 0.
  - `test_done_kid_tier_never_touches_a_card` — a kid-tier done leaves the
    card byte-identical (falsifier: a non-director done touching any card).
  - `test_done_dry_run_prints_two_would_write_lines_writes_nothing` —
    `--dry-run` prints the two `[dry-run]` would-write lines and the card
    stays byte-identical.

Suite results on this tree:
  test_cli.py:                    53 passed
  test_cli.py + test_rotate_templates.py:  85 passed
  (test_rotate_templates exercises the shared `_split_card_sections` /
   `_write_stops_section` / `_locate_where_it_stops` machinery the helper
   imports; all green.)

Production lines measured with the ONE allowed read-only git
(`git diff --numstat -- extensions/agi/bin/cli.py`): 52 added, ceiling 45
(above 45 but below 2x=90 — no re-brief needed; recorded as
`production_lines: 52`).

COVERED: slot clause (fresh stamp + harvested line via the shared locator),
dry-run (two lines, nothing written), kid/missing-card/non-director no-write
falsifiers, and committed through the existing pathspec commit. NOT COVERED
here: the separate `| landed this gen |` row-CELL write (the harvested info
is folded into the slot body instead) and the merge-sha7 field — left as a
follow-up. Because the claim's clause (1) names both the landed row AND the
slot, the verdict below is a lean, not a full proved.

## Agent Notes
Built the harvest card-stamp into cmd_done: _stamp_director_card rewrites the director seat's own where-it-stops slot (fresh UTC stamp + harvested line, next: from the card queue: line or ask SM) through rotate._write_stops_section, committed via _commit_stops_row; dry-run=2 lines no write; kid/missing-card/non-director=no write. 4 tests, 85 pass (cli+rotate_templates). landed-row cell + merge-sha7 not done — folded into slot, hence lean.
