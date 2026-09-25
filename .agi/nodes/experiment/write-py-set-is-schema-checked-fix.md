---
id: experiment:write-py-set-is-schema-checked-fix
mint_id: 4574857eb7df479ebe071f1a98f8f006
type: experiment
parents:
  - hypothesis:write-py-set-is-schema-checked
next_edges: []
confidence: 0.95
edited_by: director-engine
evidence_runs:
  - experiment:write-py-set-is-schema-checked-fix
scaffold_hash: 88c4901c6732d931
season: 2
tags:
  - local-maxxing
  - engine
  - write
testable_claim: write.py set and create --set refuse an undeclared field, a regex failure, a type failure, or a raw scalar into a list-typed field, by name; a schema-valid row still writes byte-identical.
title: write.py set and create --set now consult the target type schema before writing a row
town: core
verdict: proved
---
# experiment:write-py-set-is-schema-checked-fix

# experiment:write-py-set-is-schema-checked-fix

## Experiment

Implemented `hypothesis:write-py-set-is-schema-checked` (goal:g7.33.10 round B) directly rather
than dispatching a kid -- the round was already measured to file:line with a clear claim and
falsifier, the same discipline this project asks of every kid.

Production change in `extensions/agi/bin/write.py`:

- A new shared predicate, `_schema_field_refusal(schema, node_type, key, value, verb=...)`,
  judges one row against the target type's schema: the existing field-level `refuse:`
  annotation, an undeclared-field refusal (neither in the schema's own `fields:` nor in a new
  `_UNIVERSAL_FIELDS` allowlist of structural fields every node carries regardless of type --
  id/type/mint_id/parents/next_edges/edited_by/scaffold_hash/season/town/thought_session/
  loop/model/profile/role), a type check generalised from int-only to int/float/list/bool/str
  (`validation.types[key]`, falling back to `fields[key].type`), and a regex check
  (`validation.regex[key]`).
- `_enforce_create_schema_gate` (the existing create-time gate) now calls this shared predicate
  instead of its own narrower inline int-only check -- create is now checked exactly as
  thoroughly as set, by construction, not by two hand-kept copies.
- A new `_enforce_set_schema_gate(root, node_type, set_fm)` runs the same predicate over every
  row `set` accumulates, called from `main()` right after the verb script is parsed and before
  `submit()` -- so a refusal never reaches disk.
- `_UNIVERSAL_FIELDS` exists because most schemas (`[goal]`, `[hypothesis]`, ...) do not declare
  structural fields like `edited_by`/`season`/`town`/`thought_session` in their own `fields:`
  block even though every node carries them (confirmed by grepping all 30 schema files) -- a
  naive "undeclared key refused" rule would have wrongly refused routine writes to those keys
  on most types. The allowlist is the fix for that false-positive class.

The fifth probe from goal:g7.33.10's own "measured" row (a title with no id-prefix format) is
NOT covered: `[goal].md` declares no `title` regex, and adding one is a schema-file change
outside this hypothesis's stated FILE SCOPE (`write.py` + `links.py` only). Left open.

## Evidence

RED (reverted the fix via `git checkout`, saved diff as a patch first): 6 of 10 new tests fail
exactly as expected -- the 4 refusal-behavior probes plus both raw-scalar-into-list-field cases;
the 4 already-valid/gates-nothing tests still pass unchanged.

```text
$ python3 -m pytest extensions/agi/tests/test_write_schema_checked.py -q
6 failed, 4 passed
```

GREEN (patch re-applied):

```text
$ python3 -m pytest extensions/agi/tests/test_write_schema_checked.py extensions/agi/tests/test_write.py extensions/agi/tests/test_write_self_row.py extensions/agi/tests/test_write_dotted_key.py extensions/agi/tests/test_write_sub.py extensions/agi/tests/test_write_actor_rows.py extensions/agi/tests/test_write_guard.py extensions/agi/tests/test_node_writer.py -q
328 passed
$ python3 -m pytest extensions/agi/tests/ -k schema -q
100 passed, 6372 deselected
```

Manual dry-run smoke against the real repo's own `goal:g7.33.9` (writes nothing, `--dry-run`)
confirmed all 5 probes from goal:g7.33.10's "measured" row behave as claimed (4 refuse, the
title one is the known, documented gap), plus `create --set tags=a,b,c` on a scratch goal now
also refuses where it previously landed a raw string (this session's own g7.33.12 repro class).

Production-line delta: `git diff --numstat -- extensions/agi/bin/write.py` = 122 added, 18
deleted. Above the hypothesis's stated 10-12-lines-per-conjunct kid ceiling; this round was
implemented directly by the director rather than dispatched, and the extra lines are
documentation matching this file's own existing density (`_enforce_create_schema_gate`'s prior
docstring was comparably long) -- not undocumented control flow.

## Agent Notes
assigned: director-engine (goal:g7.33.10 round B, TMM.128)

<!-- THOUGHT:BEGIN — authored, not derived; carried across regenerating scans. The reasoning behind THIS version. -->
WHAT THE HYPOTHESIS ASKED: write.py's set and create --set consult the target's schema before
writing -- undeclared field, regex failure, type failure (float/list/bool/str), and a raw
scalar into a list-typed field all refused by name; a schema-valid row still writes
byte-identical. WHAT THE MACHINE ACTUALLY DOES: verified directly against the real goal schema
via --dry-run on goal:g7.33.9 (never touched -- dry-run writes nothing) and against a synthetic
fixture carrying a trimmed transcription of the real [goal].md validation block. All 4
in-scope probes refuse by name with the row and rule; the list-scalar repro (this session's own
goal:g7.33.12 bug) refuses on both set and create --set; two valid-set cases and a one-verb
retitle still succeed with the field landing correctly. RED/GREEN shown by reverting the
production diff via a saved patch and re-running the new test file, not by inspection. THE ONE
GAP: the title-format probe needs a schema regex this hypothesis's FILE SCOPE does not license
me to add -- named honestly rather than silently dropped or silently added out of scope.
<!-- THOUGHT:END -->
