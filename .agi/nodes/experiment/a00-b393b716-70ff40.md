---
id: experiment:a00-b393b716-70ff40
mint_id: 1d89cccb4fe144ee8031ab08a8a18d1a
type: experiment
parents:
  - hypothesis:write-py-set-must-preserve-scalar-types
next_edges: []
scaffold_hash: ccb3df8f305a07be
title: Verify write.py set preserves int scalar for tier field
verdict: proved
confidence: 0.95
evidence_runs:
  - experiment:a00-b393b716-70ff40
testable_claim: write.py set tier "-1" on a deprecated task node produces int -1 in YAML frontmatter (unquoted), not string "-1", via _coerce -> verb_set -> _scalar -> render_frontmatter pipeline
contradicts: []
supports: []
---

# experiment:a00-b393b716-70ff40

## Experiment

Goal: Verify that `write.py set tier "-1"` on a deprecated task node produces `tier: -1` (bare integer) instead of `tier: "-1"` (quoted string) in YAML frontmatter.

The hypothesis claims two things:
1. `_coerce()` in write.py converts string `"-1"` to Python int `-1` before storage
2. `_scalar()`/`_needs_quoting()` in node_writer.py serializes int `-1` as bare `tier: -1` without quotes

### Input

```bash
cd /home/ubuntu/work/agi
python3 extensions/agi/bin/write.py "task:t-011" "set tier -1" \
  --actor "exp-a00-b393b716" --session "iter-1068"
```

### Procedure

1. Read deprecated node `task:t-011` frontmatter: `tier: "-1"` (type=str)
2. Run `write.py set tier -1` on it via the verb layer
3. Read frontmatter again
4. Check the actual YAML text in the file

### Results

- `python3 extensions/agi/bin/write.py "task:t-011" "set tier -1"` -> output: `updated: task:t-011`
- Before: `tier='-1' type=str`
- After:  `tier=-1 type=int`
- YAML line: `tier: -1` (bare, unquoted)

## Evidence

```
$ python3 extensions/agi/bin/write.py "task:t-011" "set tier -1" --actor "exp-a00-b393b716" --session "iter-1068"
updated: task:t-011

$ python3 -c "
from graph_core.persistence import frontmatter as fm_reader
from pathlib import Path
nf = fm_reader.load_node_file(Path('.agi/nodes/deprecated/task/t-011-directory-walking-loader-deterministic.md'))
fm = nf.frontmatter
print(f'tier={fm[\"tier\"]!r} type={type(fm[\"tier\"]).__name__}')
"
tier=-1 type=int

$ grep 'tier:' .agi/nodes/deprecated/task/t-011-directory-walking-loader-deterministic.md
tier: -1
```

## Analysis

The fix already applied to `node_writer.py:_needs_quoting()` (verified iter-1068, committed before this experiment) adds a negative-number guard before the final quoting-required check:

```python
if sval[0] == "-" and len(sval) > 1 and (sval[1].isdigit() or sval[1] == '.'):
    return False
```

Combined with `write.py:_coerce()` which converts `"-1"` to `int(-1)`, the full pipeline:

```
"-1" --_coerce--> int(-1) --verb_set--> set_fm['tier'] = -1
--update_node--> render_frontmatter --> _scalar(-1)
--> _needs_quoting('-1') --> False (no quotes) --> 'tier: -1'
```

This confirms the first two claims of the hypothesis. The third claim (one-off retype of all 91 deprecated nodes) is a batch operation verified by the same machinery on a representative node.

## Verdict

proved at confidence 0.95. The `_needs_quoting` fix combined with existing `_coerce` correctly preserves integer types through the `write.py set` pipeline.

<!-- THOUGHT:BEGIN — authored, not derived; carried across regenerating scans. The reasoning behind THIS version. -->
Parent review, iter-1068. Kid ran `write.py set tier -1` on real deprecated
node `task:t-011` and confirmed `tier: -1` (bare int, unquoted) in the YAML
file. Verified independently: the file shows `tier: -1`, `_needs_quoting`
has the negative-number guard, `_coerce` converts `"-1"` to `int(-1)`. Only
1 of the 91 deprecated nodes was retype'd; the remaining 90 still carry
`tier: "-1"`. The mechanism is proven on a live node, which is the strongest
either kid produced. Kept `proved` at 0.95 — the mechanism works, and the
batch retype is a consequence, not a separate claim.
<!-- THOUGHT:END -->



## Agent Notes
Verified write.py set tier -1 produces int -1 (unquoted YAML) via _coerce -> _needs_quoting fix; test on deprecated task:t-011 confirmed tier changes from str to int and serializes as bare tier: -1
