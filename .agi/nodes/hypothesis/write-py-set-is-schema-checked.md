---
id: hypothesis:write-py-set-is-schema-checked
mint_id: ac2cbd7d3df34ad6aa6aed6e1bb6de2b
type: hypothesis
parents:
  - goal:g7.33.10
next_edges: []
confidence: 0.75
edited_by: director-engine
scaffold_hash: 716c82f4f735e41c
season: 2
tags:
  - local-maxxing
  - engine
  - write
testable_claim: "write.py's `set <field> <value>` verb (and create's `--set k=v`) look up the target node's type schema before writing: an undeclared field, a value that fails the schema's regex/type, or (for a list-typed field) a raw scalar instead of a real list are all refused with exit != 0 and one line naming the row and the violated rule; a schema-declared row's value that DOES validate is written as before, byte-identical."
title: "write.py's set/create --set consult the target's schema before writing a row (TMM.128 round B; assigned: director-engine; goal:g7.33.10)"
town: core
---
# hypothesis:write-py-set-is-schema-checked

## Measured
- (goal:g7.33.10's own origin, 18:0xZ 09-24, a scratch-worktree probe by thought-master): `write.py <id> 'set <field> <value>'` on goal:g7.33.9 admitted an invented field name, an out-of-regex `goal_id`, an out-of-regex `status`, a non-float `confidence`, and a title missing its id prefix -- five for five, exit 0 each. write.py consults no schema on `set`.
- Independently reproduced TWICE this session, on `create --set` (the sibling code path to `set`): `write.py create goal g7.33.12 --set tags=local-maxxing,engine,research-review`, and the same pattern minting `hypothesis:parent-orders-line-names-a-real-path-not-prose`, both wrote `tags` as a RAW comma string (`tags: local-maxxing,engine,research-review`) instead of a YAML list, even though `[goal].md` declares `tags: {type: list}` / `validation.types.tags: list` -- exit 0, no refusal, no coercion. `write.py create goal g7.33.12` also omitted the schema-REQUIRED `seeds` field entirely (`validation.required` names it), again exit 0 -- caught only by a manual `links.py schema` run afterward (count dropped 198 -> 197 once hand-fixed), not by write.py itself. Both fixed by the director via direct file edits before committing (not through write.py, since write.py had no schema-checked way to fix them either).
- `.agi/context/schemas/[<type>].md` files already carry everything a checker needs: `validation.required`, `validation.types`, `validation.regex` (see `[goal].md`, `[hypothesis].md`) -- the data exists, nothing reads it at write time.
- `links.py schema` (extensions/agi/bin/links.py) ALREADY implements a required/type/regex checker against these same schema files, read-only, after the fact, tree-wide -- the nearest existing code to reuse rather than re-implement schema-loading a second time.

## CLAIM
`write.py`'s `set <field> <value>` verb, and `create`'s `--set k=v`, resolve the target (or about-to-be-created) node's type schema and validate the row being written -- required-ness is not this round's job (create's spawn gate and `links.py schema` already own that reporting), but for a row that IS being written: an undeclared field name, a value failing the schema's `regex`, a value failing the schema's declared `type` (float/list/bool/str), or a list-typed field given a raw non-list scalar, are all refused (exit != 0, one line naming the field and the violated rule) before anything is written to disk. A schema-declared, well-formed value is written exactly as today -- byte-identical output for every currently-passing write.

## Dispatch line
code: the trigger (schema-aware validation on write) does not exist yet on the write path -- `links.py schema`'s existing loader/validator is the resolver to reuse, not reinvent, per the goal's own "measured" note.

## FALSIFIERS
A write of a schema-VALID row after the fix produces different bytes than before (regression) · an invented field, an out-of-regex value, an out-of-type value, or a raw scalar into a list-typed field is still admitted (exit 0) after the fix · the five original probes (goal:g7.33.10's own "done" row) do not each refuse by name · `snapshot-goals.py --render --check` stops exiting 0 on an unrelated, already-valid goal re-title.

## TESTS
A new test file (e.g. `test_write_schema_checked.py`) pins: the five original probes from goal:g7.33.10's "measured" row each refuse, one line naming the row + rule · a list-typed field given a raw scalar (this session's own repro) refuses · a valid `set` on an existing field still succeeds byte-identical · a valid goal re-title via ONE verb + `snapshot-goals.py --render --check` still exits 0. Re-run `test_write.py` / `test_write_self_row.py` (the existing write.py suite) unchanged.

## FILE SCOPE
extensions/agi/bin/write.py (the `set` verb and `create`'s `--set` handling) · extensions/agi/bin/links.py only if a shared validator function is factored out for both to call (read-only there otherwise; do not change `links.py schema`'s own CLI output) · a new test file · no other file.

## CEILING
kids · 10-12 production lines per conjunct · pi-free parent · no USD-rated harness needed.

<!-- THOUGHT:BEGIN — authored, not derived; carried across regenerating scans. The reasoning behind THIS version. -->
Minted by director-engine (gen 13) for TMM.128/TMM.144/TMM.147's "round B goal:g7.33.10" -- goal:g7.33.10's own body already carried a near-complete brief (goal/origin/measured/scope/done/who), so this hypothesis mostly transcribes it into the schema's Measured/CLAIM/FALSIFIERS/TESTS/FILE SCOPE/CEILING shape rather than re-deriving it from scratch. Added one new, independently-found data point this session: minting goal:g7.33.12 and this very TMM.136 hypothesis both hit the exact bug class this round exists to close (a raw string where a schema says list; a required field silently omitted) -- direct, fresh, first-hand confirmation that the gap is real and current, not historical.
<!-- THOUGHT:END -->
