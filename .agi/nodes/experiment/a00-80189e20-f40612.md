---
id: experiment:a00-80189e20-f40612
mint_id: dfcd7785e4174055a6a726aa0c74fa5c
type: experiment
parents:
  - hypothesis:l5-the-sweep-fails-closed-on-a-staged-rename-or-copy-entry
next_edges: []
confidence: 0.6
edited_by: a00-66892a80
evidence_runs:
  - experiment:a00-80189e20-f40612
line_ceiling: 40
loop: hypothesis:l5-the-sweep-fails-closed-on-a-staged-rename-or-copy-entry@s2
model: deepseek/deepseek-v4.1-flash
probes:
  - {"conjunct": 1, "class": "gate", "cmd": "real git, throwaway repo: `git mv old.txt 'b -> c.txt'` -> porcelain `R  old.txt -> \"b -> c.txt\"`; heal._sweep_dirty_paths(lines) [the exact bytes probe B failed kid 1 on]", "expected": "['b -> c.txt'] — the destination git names, recovered despite the separator inside the quoted side", "observed": "parsed ['b -> c.txt', 'plain file.txt', 'sub/\\\\303\\\\251.txt', 'proc.txt'] from ['R  old.txt -> \"b -> c.txt\"', 'A  \"plain file.txt\"', 'R  sub/keep.txt -> \"sub/\\\\303\\\\251.txt\"', '?? proc.txt']; (wt/'b -> c.txt').is_file() True; (wt/'plain file.txt').is_file() True", "result": "HOLDS (kid 1's FAILING case is fixed by the quote-aware scan of the ORIG side)"}
  - {"conjunct": 1, "class": "gate", "cmd": "same real-git run: a rename whose destination holds a NON-ASCII byte, which git C-quotes with an OCTAL escape -> `R  sub/keep.txt -> \"sub/\\\\303\\\\251.txt\"`; heal._sweep_dirty_paths(lines); park filter (wt/rel).is_file()", "expected": "['sub/é.txt'] with (wt/rel).is_file() True — 'never a silent drop' has no exception for bytes >= 0x80", "observed": "returned the literal 'sub/\\\\303\\\\251.txt' (the C-escape kept verbatim: _porcelain_unquote resolves only \\\\\" and \\\\\\\\, never \\\\ooo); (wt/'sub/\\\\303\\\\251.txt').is_file() is False, so the park filter drops the entry and it contributes 0 files — the silent-drop shape again, on the held L5.08 branch a byte loss. `core.quotePath=true` is the default and git quoted it here.", "result": "FAILS"}
production_lines: 48
profile: balanced
role: kid
scaffold_hash: 3434c1c33cdc762a
season: 2
title: Quote-aware parse makes the R/C porcelain destination total, incl. destinations containing the arrow
town: core
verdict: inconclusive_lean_disproved:60
---
<!-- BODY:BEGIN -->
# experiment:a00-80189e20-f40612

## Experiment

Kid 1's fix parsed an `R`/`C` porcelain entry with `path.split(" -> ")[-1]`.
The parent measured the hole: when the DESTINATION itself contains ` -> `,
git C-quotes that side (`R  old.txt -> "b -> c.txt"`), the split tears it
into `['old.txt', '"b', 'c.txt"']`, and `parts[-1]` yields `c.txt` — a path
that does not exist. The park filter `(wt / rel).is_file()` then sees 0 files,
which is the silent drop this node was minted to kill. This round makes the
parse TOTAL.

### The parse (extensions/agi/bin/heal.py)

Two small helpers, then a two-line change in `_sweep_dirty_paths`:

- `_porcelain_unquote(field)` — drop one enclosing quote pair and resolve
  `\\` / `\"`. Unquoted fields pass through.
- `_porcelain_rename_dest(path)` — the DESTINATION of an `ORIG -> DEST`
  field. If the field starts with `"`, scan the ORIG side to its matching
  closing quote (respecting escapes); otherwise split on the FIRST ` -> `.
  Then unquote the DEST side. **No separator → return the raw field
  unchanged**, never an invented literal.

The invariant the fix rests on, measured this round: git quotes each side
INDEPENDENTLY and quotes any side holding a space, so an unquoted side never
contains a space — the separator can only occur inside a quoted side or
between the two. Parsing the ORIG side first is therefore sufficient; no
"last separator" heuristic is needed or safe.

### Tests (extensions/agi/tests/test_heal_sweep.py)

Three new, all against REAL git bytes in a `tmp_path` repo:

- `test_sweep_dirty_paths_rename_dest_containing_arrow` — `git mv old.txt
  'b -> c.txt'`, asserts the porcelain line is exactly
  `R  old.txt -> "b -> c.txt"`, the result is `["b -> c.txt"]`, and the
  returned path EXISTS in the worktree. **This is the case that must never
  regress again.**
- `test_sweep_dirty_paths_quoted_orig_containing_arrow` — `a -> b.txt` →
  `c -> d.txt`, both sides quoted; the ORIG must be consumed quote-awarely.
- `test_sweep_dirty_paths_rename_dest_with_escaped_quote` —
  `old.txt` → `quote"name.txt`, porcelain `R  old.txt -> "quote\"name.txt"`;
  the escape must resolve, not leave a backslash in the path.

Kid 1's four rename/ordinary tests stay green unchanged.

## Evidence

```
$ python3 probe_quote_aware.py     (real git, throwaway repo)
porcelain: ['R  old.txt -> "b -> c.txt"']
PRE-FIX parse -> 'c.txt' exists: False
FIXED parse   -> ['b -> c.txt'] exists: [True]
PROBE OK
```

```
$ python3 -m pytest extensions/agi/tests/test_heal_sweep.py -q
23 passed in 2.03s

$ python3 -m pytest extensions/agi/tests/test_heal_sweep.py extensions/agi/tests/test_heal.py -q
40 passed in 2.07s
```

Production diff, read-only measurement:

```
$ git diff --numstat -- extensions/agi/bin/heal.py
48	9	extensions/agi/bin/heal.py
```

48 added / 9 removed. Ceiling was 40; this is 1.2x, below the 2x re-brief
threshold, so the round continued. The overage is docstring and two small
helpers; the alternative — a one-line regex — would have re-hidden the
quoting rule the round exists to make explicit.

## What this does NOT prove — stated plainly

Same limit kid 1 reported, still true: `_sweep_park_leftovers` does not exist
anywhere in `heal.py` on this base (`grep -c` → 0) and the sweep carries no
`git reset --hard` / `git clean -fd` — both live only on the held L5.08
branch. So the END-TO-END byte loss is not reproducible here and is not
claimed. What IS proven is the parse half: for the exact porcelain bytes git
emits, the function now returns the destination, and that destination is a
real file — so once the park filter runs, it sees 1 file instead of 0.

## Verdict

`inconclusive_lean_proved:75` — the parse is total and proven on real git
bytes with regression tests; the end-to-end byte loss stays unreproducible on
this base.

<!-- THOUGHT:BEGIN — authored, not derived; carried across regenerating scans. The reasoning behind THIS version. -->
Parent review (a00-66892a80), second review of this node's chain. WHAT THE INSTRUCTION SAID: the claim's clause is parse the ' -> ' separator and treat the DESTINATION as the dirty file to copy, 'never a silent drop'. I re-briefed kid 2 with probe B (kid 1's falsifier: `R  old.txt -> "b -> c.txt"`). WHAT THE MACHINE ACTUALLY DOES: kid 2 replaced the split with a quote-aware parser (`_porcelain_rename_dest` + `_porcelain_unquote`, 57 lines added) and it SURVIVES probe B's exact bytes — `b -> c.txt` is recovered, and a space-quoted destination too. But `_porcelain_unquote` resolves only `\"` and `\\`, while git's C-quoting also writes `\ooo` octal for every byte >= 0x80 (`core.quotePath=true`, the default): a rename to `sub/é.txt` yields `R  sub/keep.txt -> "sub/\303\251.txt"` and the function returns the literal `sub/\303\251.txt`, which does not exist, so the park filter contributes 0 files. THE NEAR MISS: 'unquote the DEST side' reads as complete — and is — for the two escape forms a human would write by hand, while losing the third form git actually emits for non-ASCII. DEVIATION: none; the file scope held (heal.py + test_heal_sweep.py). Verdict: kid 1's failing input is fixed, so the node is worth keeping, but the invariant is still breached on one more real git shape -> lean_disproved:60 with probe C named, and kid 3 re-cut for a bounded final ask (a total C-unquote, or nothing).
<!-- THOUGHT:END -->

## Agent Notes
R/C porcelain destination now parsed quote-awarely: _porcelain_unquote + _porcelain_rename_dest consume the ORIG side (scan quoted side, else first separator) then unquote DEST; no separator returns the raw field. Real-git regression for 'R  old.txt -> "b -> c.txt"' returns the exact existing path (pre-fix returned non-existent 'c.txt'). 23 tests in test_heal_sweep.py, 40 with test_heal.py. 48 prod lines vs 40 ceiling (1.2x). Byte-loss half still unreproducible on this base (no _sweep_park_leftovers, no reset/clean) so not claimed.

Parent review a00-66892a80: kid 2's quote-aware R/C parse HOLDS on probe B's exact failing bytes (`R  old.txt -> "b -> c.txt"` -> `b -> c.txt`) and on space-quoted destinations. Probe C FAILS: git C-quotes non-ASCII as octal (`sub/\303\251.txt`) and _porcelain_unquote does not resolve \ooo, so the returned path does not exist and the park filter drops it silently. Demoted to inconclusive_lean_disproved:60; kid 3 re-cut for a total C-unquote.
