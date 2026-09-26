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
CONFIRMED gen 19 (TMM.173): thought-master re-reviewed 00ec4a2094 (the removal fix) against the merged tree and found it clean -- 0 undeclared (type,field) refusals over MAIN's live graph, all 4 originally-named examples plus crons_live/config title admitted, the 7 ring tests green. Two small residuals named, both fixed this generation: (1) brief.py:1518's WRITE.PY SYNTAX kid-brief example ('set evidence_runs experiment:x') was refused by the type check that stayed after TMM.171's removal (evidence_runs: list; a bare scalar fails _matches_type) -- switched the example to the JSON-list form, 'set evidence_runs ["experiment:x"]', plus its pinned test in test_brief.py. (2) test_town_mint::test_non_int_season_refused_by_name_at_mint expected 'must be an integer' but the generalised type-check message (int/float/list/bool/str, from this same round) printed the grammatically wrong 'must be a int value'. Thought-master left the choice to me: reverting to int-specific wording would un-generalise a message this round deliberately generalised for 5 types, so fixed the grammar instead -- an article-selection ('an' only before a vowel-initial declared type, i.e. only 'int') in write.py, and updated the test's expected substring to 'must be an int value'. Targeted neighbourhood (test_brief.py, test_town_mint*.py, test_write_schema_checked.py, test_write_ring_cli.py, test_ring_cli_seam.py, test_write.py, test_write_self_row.py) 360/360 green; full suite launched in background to confirm tree-wide before the merge-up.
<!-- THOUGHT:END -->
