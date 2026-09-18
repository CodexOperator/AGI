---
id: experiment:a00-9231dba2-10b8ef
mint_id: c663bd49372f41ebae3ca676bf9785ec
type: experiment
parents:
  - hypothesis:l4-the-formation-owner-writes-config-posts-rows-and-the-town-master-cell-through-a-schema-declared-actor-row-grant-never-a-role-literal
next_edges: []
confidence: 0.9
edited_by: a00-9231dba2
evidence_runs:
  - experiment:a00-9231dba2-10b8ef
line_ceiling: 40
loop: hypothesis:l4-the-formation-owner-writes-config-posts-rows-and-the-town-master-cell-through-a-schema-declared-actor-row-grant-never-a-role-literal@s2
model: deepseek/deepseek-v4.1-flash
production_lines: 80
profile: balanced
role: kid
scaffold_hash: d361add26e2b3fba
season: 2
title: "Generic actor_rows grant: sanctuary-master writes config:posts rows and the town master cell"
town: core
verdict: proved
---
<!-- BODY:BEGIN -->
# experiment:a00-9231dba2-10b8ef

## What was built

The CODE HALF of `hypothesis:l4-the-formation-owner-writes-config-posts-rows-and-the-town-master-cell-through-a-schema-declared-actor-row-grant-never-a-role-literal`: a generic `actor_rows:` resolver in `extensions/agi/bin/write.py` plus the two schema declarations and one new test file. A future grant is now ONE schema line, not a new branch in the enforcement path.

- `write._actor_rows_refusal` (called from `_enforce_written_by`, the SAME
  unadmitted-writer position as the master-sensei carve-out): reads the
  schema frontmatter LIST `actor_rows:` and resolves EVERY entry for the
  actor's RESOLVED seat name (`_resolve_seat`), never a role literal and
  never the free-text `--actor` string. Two shapes: `list_key`+`match_key`
  (rows of `set_fm[list_key]`, `fields` writable, `ops` create/set/retire,
  `deny_roles` naming rows) and `field` (one top-level cell). An op, field
  or row outside the grant refuses BY NAME. The old row list is read through
  `geometry_config`/`_load_seats`; no file name is hardcoded.
- `.agi/context/schemas/[config].md`: `actor_rows:` gains the migrated
  master-sensei entry (first) and the sanctuary-master posts grant
  (verbatim as briefed). The legacy `master_sensei_row` key stays and its
  dedicated resolver (dict-of-templates + producing judge) is untouched, so
  `test_write_master_sensei.py` is green unchanged.
- `.agi/context/schemas/[town].md`: `actor_rows:` grants sanctuary-master the
  top-level `master` field. `branches` is untouched and stays refused at
  mint (create field-level `refuse:`) and at read (`towns.load_towns`).
- `extensions/agi/tests/test_write_actor_rows.py` (NEW, 12 tests) drives the
  REAL `write.submit` / `write.main` on a fixture root.

## Acceptance

1. set a posts row `town` cell / create a row / retire a row by
   `sanctuary-master` -> each WRITTEN.
2. `director-belam` and a kid actor on the same edit -> REFUSED by name
   (the seated self_row gate fires first and names the reason).
3. a field outside the grant (`owning_goal`) by `sanctuary-master` ->
   REFUSED by name, the message naming both the field and `actor_rows`.
4. `sanctuary-master` sets the town `master` cell -> WRITTEN; another town
   field refused by name; `branches` refused at mint (rc=2) and at read
   (`towns.TownError`).
5. legacy master-sensei admits its templates edit and refuses a
   prime_director touch — asserted in the same new file.

## Evidence

Main suite (the brief's five files plus the schema/town files this touches):

```
$ python3 -m pytest extensions/agi/tests/test_write_master_sensei.py \
    extensions/agi/tests/test_write.py extensions/agi/tests/test_write_self_row.py \
    extensions/agi/tests/test_town_cell_write.py extensions/agi/tests/test_write_actor_rows.py -q
145 passed, 89 warnings in 1.35s

$ python3 -m pytest extensions/agi/tests/test_town_schema.py \
    extensions/agi/tests/test_town_mint.py extensions/agi/tests/test_town_mint_final.py \
    extensions/agi/tests/test_town_rows_readers.py extensions/agi/tests/test_towns.py \
    extensions/agi/tests/test_no_literal_town.py -q
45 passed, 14 warnings in 3.65s
```

Production lines (`git diff --numstat`, test file excluded):

```
3	0	.agi/context/schemas/[config].md
2	0	.agi/context/schemas/[town].md
75	0	extensions/agi/bin/write.py
= 80 lines
```

## Dead-grant observation (flagged, NOT fixed)

The briefed `[config].md` field list for the sanctuary-master posts grant
includes `quiet` and `status`, which NO live `posts.md` row carries (the live
rows carry `settings: "quiet"`). The grant is implemented exactly as declared;
widening it is the master's call, not this kid's. A `set status ...` on a live
row would be admitted by the grant and would land a NEW key on the row — worth
the master's eye at review.

<!-- THOUGHT:BEGIN — authored, not derived; carried across regenerating scans. The reasoning behind THIS version. -->
Why this version differs: before it, the only seat with a schema-declared
narrow write path on a config node was `master-sensei`, and that path was a
hard-NAMED resolver reading ONE `master_sensei_row` dict. The formation owner's
grant (sanctuary-master writes config:posts rows + the town `master` cell)
would have needed a THIRD hard-named branch. Instead the resolver is generic:
the schema carries a LIST, write.py loops it, identity is the RESOLVED seat,
and the next grant is a schema line. Judgement calls: (1) the legacy
`master_sensei_row` key is kept AND its behaviour is migrated into `actor_rows`
as the first entry, but the dict-of-templates shape and the producing judge
stay in the dedicated `_master_sensei_templates_refusal` — the generic resolver
skips an entry with no `match_key`/`field`, so behaviour is byte-identical and
`test_write_master_sensei.py` is green unchanged; (2) the top-level `field`
shape refuses ANY frontmatter write by the granted seat that is not exactly the
granted field, so `set season` by sanctuary-master fails in the actor_rows gate
rather than only in the written_by gate; (3) production lines are 80 — at the
2x-of-40 boundary, so no re-brief was raised, but the round is not cheap.
<!-- THOUGHT:END -->

## Agent Notes
Generic actor_rows resolver in write.py (75 prod lines) + [config]/[town] grants (5 lines): sanctuary-master writes config:posts rows (create/set/retire, declared fields) and the town master cell through the resolved-seat identity; every other seat and any out-of-grant field/op refuses by name; branches stays refused at mint and read; legacy master_sensei_row green unchanged. 12 new tests, 145 passed in the brief's five-file suite, 45 passed in the town/schema suite. FLAGGED: briefed field list carries quiet/status, which no live posts row carries.
