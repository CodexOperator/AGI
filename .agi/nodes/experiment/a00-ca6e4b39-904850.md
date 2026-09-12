---
id: experiment:a00-ca6e4b39-904850
mint_id: c89f54035d87417e847d6c00086554f1
type: experiment
parents:
  - hypothesis:l4-the-town-create-gate-refuses-what-the-loader-refuses-and-every-vision-id-must-exist
next_edges: []
confidence: 0.95
edited_by: a00-4895b300
evidence_runs:
  - experiment:a00-ca6e4b39-904850
loop: hypothesis:l4-the-town-create-gate-refuses-what-the-loader-refuses-and-every-vision-id-must-exist@s2
model: ~deepseek/deepseek-v4-flash-latest
profile: balanced
role: kid
scaffold_hash: e69b86ee56aed22c
season: 2
title: A00 ca6e4b39 904850
town: core
verdict: proved
---
<!-- BODY:BEGIN -->
# experiment:a00-ca6e4b39-904850

## Experiment

FIX round (g15 claim = behaviour to BUILD, not measure) on
`hypothesis:l4-the-town-create-gate-refuses-what-the-loader-refuses-and-every-vision-id-must-exist`.
Kid A's slice: make write.py's create gate refuse BY NAME, at mint, what the
loader refuses at read — driven GENERICALLY by the schema's field-level
`refuse:` annotation and declared `int` types — plus a non-int `season` refusal,
plus the corrected Prime create lines in `experiment:a00-80511a41-c96c9f`
(`--actor belam --role prime_director` = actor the seat, role explicit), plus
SUPERSEDED-in-place markers on the obsolete lines of `experiment:a00-061c8dfd-9c6c20`.

### The pre-fix defect (measured)

`extensions/agi/bin/write.py` create branch parsed `--set` values and went
straight to `node_writer.write_node`; NOTHING on that path consulted the
schema's field `refuse:` annotation. So `write.py create town ... --set
'branches=[core/main]'` minted a town node born with a `branches:` cell in its
frontmatter — a cell `towns.load_towns` then refused at READ time. The schema
file's `branches: {type: str, refuse: "DERIVED, never a cell …"}` was true of
the LOADER, not of the CREATE GATE. And `--set season=abc` coerced to the
string `"abc"` and minted a town whose OWN `season` counter is not an int.

### The fix (implemented, generic)

New helper `_enforce_create_schema_gate(root, node_type, set_fm)` in write.py
(the create-gate region only — no ring gate, no veto gate, no branches.py,
cli.py, ladder.md, posts.md, rotate.py, towns.py touched). It loads the node's
schema through `schema_registry` and, for every `--set` key, enforces two rules
driven by the schema itself, never a town special case:

1. a field carrying a `refuse:` annotation → refuse BY NAME, quoting the
   annotation's own ground (exit 2, one line); nothing is written.
2. a field the schema declares `int` whose value is not an int (`season=abc`,
   `season=true`, `season=2.5`) → refuse BY NAME ("must be an integer at mint"),
   never a traceback. A bool is refused (isinstance bool, a subclass of int,
   is not a season); a real int passes.

Called in `main()`'s create branch AFTER the `set_fm` loop and BEFORE the
`--dry-run` short-circuit — so a dry run of a refused cell refuses what the
real mint would refuse, closing the kid-1 dry-run-bypass corner for this gate.

### Item 5 — the corrected Prime create lines

Updated `experiment:a00-80511a41-c96c9f`'s `## Prime create lines (final)`
fence: each line now carries `--actor belam --role prime_director` (actor =
the SEAT, role explicit) instead of a bare `--actor prime_director`. The
fence-parsing test `extensions/agi/tests/test_town_mint_final.py` reads the
block out of the node (drift-proof) and runs each line through a real
subprocess on a fixture; a new test
`test_block_lines_carry_seat_actor_and_explicit_role` asserts the corrected
spelling (actor `belam`, role `prime_director`, `--role` after `--actor`), so
a regression to the old spelling fails.

### Item 7 — superseded lines marked in place

`experiment:a00-061c8dfd-9c6c20`'s obsolete DELIVERABLE block (the three
`write.py create town` lines with no `AGI_SEASON` control and a dry-run proof)
are marked SUPERSEDED in place — a `# SUPERSEDED (L4.338) …` comment line
inside the code fence plus a `**SUPERSEDED (L4.338):**` note under
`## Prime create lines` — never deleted.

## Evidence

Gate refusals, BY NAME, on a fresh fixture (tmp_path project, live `[town].md`
schema, `belam` as seat actor with explicit role):

```
$ env AGI_ROLE=prime_director AGI_SEASON=2 python3 write.py create town probe \
  --parent ladder:ladder --set council=council-core --set season=2 \
  --set 'visions=["vision:alive"]' --set 'branches=[core/main]' \
  --root <fixture> --actor belam --role prime_director
ERR: create town refused by name: 'branches' is not a settable cell — DERIVED, never a cell — towns.py refuses this key BY NAME at read time; see body (schema field-level `refuse:`, enforced generically at mint)
rc=2     # no node born

$ ... --set season=abc ...
ERR: create town refused by name: 'season' must be an integer at mint, got 'abc' (schema declares season: int)
rc=2     # no traceback, no node born
```

Tests — the gates fire by name on a FIXTURE, never the live tree; the
corrected lines mint:

```
$ python3 -m pytest extensions/agi/tests/test_town_mint.py -q
9 passed                    # incl. new test_branches_cell_refused_by_create_gate_by_name
                            # and test_non_int_season_refused_by_name_at_mint;
                            # dry-run+branches now refuses (gate pre-dry-run)
$ python3 -m pytest extensions/agi/tests/test_town_mint_final.py -q
5 passed                    # incl. new test_block_lines_carry_seat_actor_and_explicit_role;
                            # reads the corrected node block and mints it on the fixture
$ python3 -m pytest test_write.py test_write_guard.py test_write_master_sensei.py \
  test_write_ring_cli.py test_write_self_row.py test_node_writer.py \
  test_town_schema.py test_town_mint.py test_town_mint_lines.py \
  test_town_mint_final.py test_towns.py test_no_literal_town.py -q
283 passed                  # full write+town surface: gate change breaks nothing
```

The `tier-gate: phantom running record … (dead) -- skipped` line on the tree
is a leftover dead-pid record reported once by conftest; it skips, not fails.

## Agent Notes
Implemented the generic create gate in write.py: schema field-level `refuse:` and declared `int` types are now enforced BY NAME at mint (branches cell and non-int season both refuse rc=2, no node), before the dry-run short-circuit. Corrected a00-80511a41's Prime lines to `--actor belam --role prime_director` and added a drift test. Marked a00-061c8dfd's obsolete lines SUPERSEDED in place. 283 write+town tests green.

## Agent Notes
write.py create gate now enforces the schema's field-level refuse: annotation and declared int types GENERICALLY: a town branches: cell and a non-int season both refuse BY NAME at mint (rc=2, no node), before the dry-run short-circuit. Corrected a00-80511a41's Prime create lines to --actor belam --role prime_director (actor=seat, role explicit) + drift test in test_town_mint_final. Marked a00-061c8dfd's obsolete lines SUPERSEDED in place. 283 write+town tests green.

<!-- THOUGHT:BEGIN — authored, not derived; carried across regenerating scans. The reasoning behind THIS version. -->
PARENT REVIEW a00-4895b300 L4.338: accepted, proved stands. WHAT THE INSTRUCTION SAID: "the write.py create gate refuses BY NAME, at mint, what the loader refuses at read ... the schema refuse: annotation must become a gate rule the create path enforces, generically for any schema that declares one". WHAT THE MACHINE DOES: read write.py: _enforce_create_schema_gate at L1367-1422, called from main() create branch at L2128 AFTER the --set loop and BEFORE the --dry-run short-circuit, iterating set_fm keys against schema.fields and schema validation.types -- so the refusal is schema-driven, not a town literal, and a dry run refuses what the real mint refuses. NEAR MISS: a town-shaped special case keyed on branches would satisfy the words and lose the mechanism; the generic form is what survives a second schema declaring refuse:. No deviation from standing rule. EVIDENCE I RAN: pytest test_town_mint.py test_town_mint_final.py test_town_schema.py test_towns.py test_town_mint_lines.py -> 29 passed; items 5 and 7 verified in the two experiment node bodies.
<!-- THOUGHT:END -->
