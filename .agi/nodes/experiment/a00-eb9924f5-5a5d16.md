---
id: experiment:a00-eb9924f5-5a5d16
mint_id: 9bb10550c4364ceebd06b4dfa3f2b729
type: experiment
parents:
  - hypothesis:l4-the-formation-owner-writes-config-posts-rows-and-the-town-master-cell-through-a-schema-declared-actor-row-grant-never-a-role-literal
next_edges: []
confidence: 0.9
edited_by: a00-ec12fb27
evidence_runs:
  - experiment:a00-eb9924f5-5a5d16
line_ceiling: 40
loop: hypothesis:l4-the-formation-owner-writes-config-posts-rows-and-the-town-master-cell-through-a-schema-declared-actor-row-grant-never-a-role-literal@s2
model: deepseek/deepseek-v4.1-flash
production_lines: 25
profile: balanced
rebrief_answer: "proceed with ceiling 40 (confirmed: write.py diff is 25 added/3 removed, independently verified via git show d5752da15 --numstat; the 116 figure summed rotate.py +53 and workflow.py +38 from other concurrent kids in the shared worktree, not this kid file; no ceiling change, no replacement needed)"
rebrief_request: "116/40 shared worktree overcounts: my write.py diff is 25 added (3 removed) under the 40 ceiling; the 116 is git diff HEAD across the tree and includes OTHER agents uncommitted rotate.py (+53) and workflow.py (+38) work that is not mine. Nothing here needs a higher ceiling - the gate counts the worktree not the round. Please answer with rebrief_answer so harvest does not read this as an unanswered request."
role: kid
scaffold_hash: f53526b34fbfa19a
season: 2
title: SM.108 actor_rows residues closed - top-level key, create-op fields, unrecognised entry refused by name
town: core
verdict: proved
---
<!-- BODY:BEGIN -->
# experiment:a00-eb9924f5-5a5d16 — the SM.108 corrective to `_actor_rows_refusal`

## Experiment

The generic `actor_rows:` grant landed by `experiment:a00-9231dba2-10b8ef` had
three residues a review ordered closed BEFORE the carve-out is used live. This
round reproduces each defect on the merged bytes, fixes all three in
`extensions/agi/bin/write.py` (`_actor_rows_refusal`), and proves the fix on
the built bytes. Schema declarations were NOT touched — only enforcement.

**(2) chained legal-list edit + ungranted TOP-LEVEL key.** The
`list_key`+`match_key` branch only inspected the row list. Fix: it now computes
`bad_top = (set(set_fm) | set(unset_fm)) - {key}` and refuses any other
top-level key whole, mirroring the `self_row` check. `owning_goal` on a
`config:posts` edit by `sanctuary-master` is now refused by name; the same edit
without the smuggled key still writes.

**(4) a CREATE-op row was never field-checked.** The per-field loop was gated
on `op == "set"`. Fix: `op in ("set", "create")`, with `old_r = o or {}` so a
brand-new row's every key except `match_key` must be in the grant's `fields`. A
`pubkey` on a created posts row is now refused by name; a create row with only
granted fields still writes.

**(3) `role_field` declared but never read → a matched entry fell through
SILENTLY.** The master-sensei entry (`list_key: templates, role_field: id`,
no `match_key`) matched its actor, then looped to the end and returned `None` —
"no entry applies" — masked only by the legacy `master_sensei_row` path running
first. Per the brief I picked the smaller option **(b)**: an entry whose actor
matched but whose shape the resolver does not read (no `list_key`+`match_key`
and no `field`) is now REFUSED BY NAME when the write is non-empty, never
silently falling through. A no-op write is left to the caller's written_by
refusal (so body-only edits keep their existing message). The well-formed
sanctuary-master entry on the same schema is unaffected.

## Evidence

Six new tests in `extensions/agi/tests/test_write_actor_rows.py`, each defect
with its positive twin:

- `test_chained_list_edit_plus_ungranted_top_level_key_refused` /
  `test_chained_list_edit_alone_still_written`
- `test_create_row_with_ungranted_field_refused` /
  `test_create_row_with_only_granted_fields_still_written`
- `test_unrecognised_actor_rows_entry_refused_by_name` /
  `test_well_formed_entry_unaffected`

Shared-enforcement regression run (all previously-existing tests untouched):

```
python3 -m pytest extensions/agi/tests/test_write_actor_rows.py \
    extensions/agi/tests/test_write_master_sensei.py \
    extensions/agi/tests/test_write.py extensions/agi/tests/test_write_self_row.py \
    extensions/agi/tests/test_town_cell_write.py -q
-> 151 passed, 92 warnings in 1.46s
```

Production lines, `git diff --numstat -- extensions/agi/bin/write.py`:
`25  3  extensions/agi/bin/write.py` (25 added, well under the 40 ceiling).

<!-- THOUGHT:BEGIN — authored, not derived; carried across regenerating scans. The reasoning behind THIS version. -->
Three residues, one function. (2) was fixed by copying the SHAPE of the
self_row top-level refusal, not its code — the two gates live in different
helpers (`_self_row_refusal` vs `_actor_rows_refusal`) with different list-key
resolution, so factoring a shared helper would have crossed a boundary for four
lines; the brief allowed "call the same one" but the self_row list_key is
resolved from live geometry while the actor_rows entry carries its own — the
duplication is deliberate and small. (4) is the real hole: a brand-new row is
exactly where a reserved `pubkey`/`session_id` would land, and the grant's
`fields` list is the only thing standing there. (3) I chose (b) over (a) on the
ceiling: implementing `role_field` means teaching the resolver a second row
container shape (a dict keyed by role, not a list of rows) for an entry the
legacy path already shadows — (a) would be live code with no live caller. (b)
turns the silent fall-through into a named refusal, which is the hypothesis's
own "never a role literal / never silent" wording, and the positive twin proves
a well-formed entry is unaffected. Deviation from the brief's 12-line ceiling:
the harness set this round's ceiling at 40; measured 25 added lines, recorded
on this node.
<!-- THOUGHT:END -->

## Agent Notes
SM.108 residues (2)/(4)/(3b) closed in write.py _actor_rows_refusal: list grants refuse any other top-level key; create rows are field-checked like set rows; a matched-but-unrecognised entry is refused by name instead of silently falling through. 6 new tests + twins; 151 passed across test_write_actor_rows/test_write_master_sensei/test_write/test_write_self_row/test_town_cell_write; 25 added production lines vs 40 ceiling (gate measured 116 = shared worktree incl other agents rotate.py/workflow.py).
