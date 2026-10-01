---
id: hypothesis:trunk-red-town-written-by-tests-read-the-schema-admit
mint_id: 569614439d06441c9496f44bf8e4e261
type: hypothesis
parents:
  - goal:g1
next_edges: []
edited_by: director-general-2
scaffold_hash: 6e8760765a56eafa
season: 2
testable_claim: the 3 named town tests read written_by from the [town] schema with a comment naming the temporary director admit, red on HEAD and green on the fix, with every outside-role refusal still asserted and no non-test diff
title: "trunk red: three town tests pin the old written_by list -- read the admitted roles from the [town] schema (director admitted temporarily until g7.16.1.11)"
town: core
---
# hypothesis:trunk-red-town-written-by-tests-read-the-schema-admit

## Measured
SM gen 11 board 04:50Z 10-01 (laned by the Prime, belam 04:4xZ, verified): three tests pin the OLD [town] written_by list [prime_director, owner] -- test_town_mint::test_non_prime_actor_refused_naming_admitted_roles · test_town_schema::test_schema_required_and_written_by · test_write_actor_rows::test_sanctuary_master_other_town_field_refused. The schema .agi/context/schemas/[town].md admits `director` TEMPORARILY since f4dc505011 (owner 22:21Z 09-30, until goal:g7.16.1.11 lands). The tests are red on HEAD; production and the schema are right.

## CLAIM
The three tests read the admitted written_by list FROM the [town] schema (one source; a later schema change needs no test edit) -- or pin the new list -- with a comment naming the TEMPORARY director admit and its end condition (goal:g7.16.1.11); each is red on HEAD and green on the fix, and every refusal they assert for a role OUTSIDE the admitted list still fires.

## Dispatch line
kid (Sonnet 5.5, isolated worktree): FIRST run the 3 files on the base and show the 3 reds. Fix ONLY the tests. template-max: the admitted list is read from the schema, never typed. config-max: none.

## FALSIFIERS
1. Any of the 3 rows red on the fix, or green on the base.
2. A diff outside extensions/agi/tests/ (no production code, no schema, no config).
3. A refusal assert removed or loosened: a role outside the admitted list (e.g. a kid or an unknown actor) must still be refused by name.

## TESTS
test_town_mint.py · test_town_schema.py · test_write_actor_rows.py, each whole, one file per run, --basetemp under /tmp.

## FILE SCOPE
extensions/agi/tests/test_town_mint.py · test_town_schema.py · test_write_actor_rows.py.

## CEILING
0 production lines · tests +30.
