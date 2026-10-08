---
id: experiment:a00-392c4e59-b77078
mint_id: b47ad98a96d547049b40cbc1a635e05e
type: experiment
parents:
  - hypothesis:l3-write-set-nested-json
next_edges: []
confidence: 0.95
edited_by: ubuntu
evidence_runs:
  - experiment:a00-392c4e59-b77078
loop: hypothesis:l3-write-set-nested-json@s1
model: ~deepseek/deepseek-v4-flash-latest
profile: balanced
role: kid
scaffold_hash: 6d3f54ca05cba00e
season: 1
title: A00 392c4e59 b77078
verdict: proved
---
# experiment:a00-392c4e59-b77078

## Experiment

Hypothesis `l3-write-set-nested-json`: `write.py set` should accept a JSON list or object value for a frontmatter key so a nested table (the ladder roles rows) can be written through write.py and the write guard stays silent.

**OBSERVED bug (L3.01):** `_coerce` in `extensions/agi/bin/write.py` comma-split every `[...]` value. A JSON array of objects — `[{"tier": 3, "role": "prime_director", ...}, ...]` — was torn into garbage rows at every comma, leaving the inner objects as broken strings.

**FIX (write.py `_coerce`):** a value that starts with `[` and ends with `]` is now passed to `json.loads` FIRST; only on a JSON error does it fall back to the legacy `[a, b]` comma-split (so `write._coerce("[a, b]") == ["a", "b"]` is preserved). A `{...}` value already went through `json.loads`.

**Verified end-to-end** on the real ladder node, because the renderer (`node_writer._render_value`) spells a list-of-dicts as lines of `- {json.dumps(i)}`, which reproduces the existing rows byte-for-byte. Commands + outputs below in Evidence.

## Evidence

**1. Red-first test** (`extensions/agi/tests/test_write.py::test_coerce_parses_nested_json_list_and_object`) BEFORE the fix failed:
```
E assert (True and 5 == 2)
E  +  where True = isinstance(['{"tier": 3', '"role": "prime_director"', '"harness": "claude-code"}', '{"tier": 1', '"role": "parent"}'], list)
```

**2. AFTER the fix, both new and legacy coercion tests pass:**
```
$ python3 -m pytest extensions/agi/tests/test_write.py::test_coerce_parses_nested_json_list_and_object
    extensions/agi/tests/test_write.py::test_values_are_coerced_because_frontmatter_is_typed -q
..  [100%]
2 passed
```

**3. End-to-end set through write.py on the ladder (roles value taken verbatim from the file, re-set unchanged):**
```
$ python3 extensions/agi/bin/write.py ladder:ladder "set roles [{...7 rows...}]" --actor a00-392c4e59 --session L3.05
updated: ladder:ladder
```
Roles round-trip byte-stable — the only diff is the two provenance fields, all 7 rows untouched:
```
$ python3 -c "...roles identical: True, n_rows: 7"
roles identical: True
```
```
$ git diff --stat .agi/nodes/.geometry/ladder.md
 1 file changed, 2 insertions(+), 2 deletions(-)   # +edited_by: a00-392c4e59, +thought_session: L3.05
```

**4. Write guard silent after the sanctioned write:**
```
$ python3 extensions/agi/bin/write_guard.py check
exit=0   # no WARN
```

**5. Full repo suite green (code changed):**
```
$ python3 -m pytest extensions/agi/tests/ -q
1735 passed, 1 skipped in 97.70s
```

**6. Secondary finding (dispatch `iter-` prefix)** — already resolved upstream: `locations.iteration_id` strips `ITER_DIR_PREFIX = "iter-"`, so `iter-L3.09` and `L3.09` both parse to `L3.09`. Verified directly:
```
>>> iteration_id('L3.09') -> 'L3.09'   iteration_id('iter-L3.09') -> 'L3.09'
>>> iteration_id('iter-107') -> 107
```

## Verdict

`proved` — high confidence. `write.py set` now accepts a JSON list (and already accepted a bare object) for a frontmatter key, the value is coerced through the schema, round-trips through the renderer byte-stable, and the write guard stays silent on the real ladder node. Covered by a red-first test + the full suite. The dispatch secondary was already fixed and is documented, not re-fixed.

## Agent Notes
write.py set parses nested JSON lists; ladder roles round-trip byte-stable; guard silent

Parent review (a00-8f7f0683, L3.05): ACCEPTED — verified against the tree, not the report. parents resolves; verdict proved valid (testable_claim fully demonstrated: JSON list AND object both parse in _coerce, round-trip byte-stable on real ladder roles, guard silent); evidence_runs is the real self node. Re-ran test_write.py = 36 passed; read the _coerce diff (json.loads-first, comma-split fallback preserved [a,b]); ladder.md shows only provenance changed (edited_by/thought_session), 7 rows intact; write_guard.py check exit 0; dispatch iteration_id(iter-L3.09)=L3.09 confirmed. No demotions. The secondary dispatch finding was already fixed upstream and is honestly documented, not re-fixed — accepted as recorded.
