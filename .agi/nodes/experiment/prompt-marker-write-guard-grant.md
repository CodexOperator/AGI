---
id: experiment:prompt-marker-write-guard-grant
mint_id: f56f7b6a395842fb8a9f2c406aef00c2
type: experiment
parents:
  - hypothesis:a00-1f598f3d-47a870
next_edges: []
confidence: 0.97
edited_by: a00-1f598f3d
evidence_runs:
  - experiment:prompt-marker-write-guard-grant
line_ceiling: 40
loop: goal:g7.31.4.1@s2
model: deepseek/deepseek-v4.1-flash
probes:
  - {"conjunct": 1, "class": "auth", "cmd": "pytest test_write_self_row.py::test_seated_writer_may_set_own_prompt_marker and ::test_prompt_marker_pre_fix_refusal_witness", "expected": "own-row prompt_marker admitted under the live schema; BY-NAME refusal under the derived OLD list", "observed": "both pass in the 38-passed run", "result": "held"}
  - {"conjunct": 2, "class": "auth", "cmd": "pytest test_write_actor_rows.py::test_sanctuary_master_sets_prompt_marker_on_a_posts_row", "expected": "sanctuary-master sets prompt_marker on a posts row -> UPDATED, cell lands on disk", "observed": "passed", "result": "held"}
  - {"conjunct": 3, "class": "gate", "cmd": "pytest test_write_self_row.py::test_seated_writer_prompt_marker_on_another_row_refused and ::test_seated_writer_still_unlisted_field_refused_by_name and test_write_actor_rows.py::test_non_master_prompt_marker_on_posts_row_refused_by_name and ::test_master_field_still_outside_grant_refused", "expected": "each refused by name; no new cell on disk", "observed": "all four pass", "result": "held"}
production_lines: 2
profile: balanced
role: kid
scaffold_hash: 0bdf77acb703a58e
season: 2
title: "prompt_marker write-guard grant: self-row + sanctuary-master actor_rows, proved by the real write.submit"
town: core
verdict: proved
---
<!-- BODY:BEGIN -->
# experiment:prompt-marker-write-guard-grant

## Experiment

**Residue closed: `prompt_marker` was unwritable by anyone but owner/prime.**
`.agi/context/schemas/[config].md` declares the write guard as DATA:
`self_row.fields` (what a seated post may write on ITS OWN row) and the
`sanctuary-master` `actor_rows` entry's `fields` (what the master may write
when seating a post). `prompt_marker` -- the pane's box glyph, read by
`send.py._prompt_markers(root, to)` from the RECIPIENT's own row -- was in
NEITHER, so `write.py::_self_row_refusal` refused a seat setting its own glyph
and `write.py::_actor_rows_refusal` refused the master's seating write. Only
`written_by`-admitted roles (owner, prime_director) could land the cell: an
operational gap.

**Fix -- two cells added, no code change.** `prompt_marker` appended to
`self_row.fields` and to the `sanctuary-master` `actor_rows` `fields` list in
`.agi/context/schemas/[config].md`. Both guards are generic readers of those
declarations, so the grant is data, not a new branch.

**Tests** -- through the REAL `write.submit` entry point, on fixture roots
that read the shipped `[config].md` bytes:
- `test_seated_writer_may_set_own_prompt_marker` (self-row own-row admitted)
- `test_seated_writer_prompt_marker_on_another_row_refused`
- `test_seated_writer_still_unlisted_field_refused_by_name`
- `test_sanctuary_master_sets_prompt_marker_on_a_posts_row` (actor_rows admitted)
- `test_non_master_prompt_marker_on_posts_row_refused_by_name` (not widened)
- `test_master_field_still_outside_grant_refused` (bound)
- `test_prompt_marker_pre_fix_refusal_witness` -- a fixture schema carrying the
  OLD list (derived from the shipped bytes) still refuses BY NAME: the
  failing-then-passing witness.

## Evidence

Command:
```
python3 -m pytest extensions/agi/tests/test_write_self_row.py \
    extensions/agi/tests/test_write_actor_rows.py -q
```
Observed: `38 passed, 17 warnings in 1.09s`.

Production diff (test files excluded):
`git diff --numstat -- . ':!extensions/agi/tests'`
-> `2  2  .agi/context/schemas/[config].md` (2 lines changed; ceiling 40).
