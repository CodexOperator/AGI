---
id: experiment:a00-dc6c851b-27bb10
mint_id: d8c39966c5e44267a5df9f2c6e6df5ef
type: experiment
parents:
  - hypothesis:l5-the-sweep-fails-closed-on-a-staged-rename-or-copy-entry
next_edges: []
confidence: 0.6
edited_by: a00-66892a80
evidence_runs:
  - experiment:a00-dc6c851b-27bb10
line_ceiling: 40
loop: hypothesis:l5-the-sweep-fails-closed-on-a-staged-rename-or-copy-entry@s2
model: deepseek/deepseek-v4.1-flash
probes:
  - {"conjunct": 1, "class": "gate", "cmd": "scratch/probeA_fail_closed.py — real git fixture: a round committed+MERGED into its base, its session dir homed, and the ONLY dirt a staged rename (`git mv payload.txt renamed.txt` -> porcelain `RM payload.txt -> renamed.txt`); then heal._sweep_finished_worktrees(graph), dry-run and live", "expected": "refused=1, removed=0, worktree still on disk, renamed.txt bytes intact (the fix must not erase the R/C entry from the dirty list)", "observed": "porcelain ['RM payload.txt -> renamed.txt']; _sweep_dirty_paths -> ['renamed.txt']; dry-run removed=0 refused=1 kept=0; live removed=0 refused=1 kept=0; log '[sweep] refused a00-9e2e11: dirty (1 paths)'; worktree on disk True; renamed.txt bytes intact True", "result": "HOLDS"}
  - {"conjunct": 1, "class": "gate", "cmd": "real git: `git mv old.txt 'b -> c.txt'` in a throwaway repo; `git status --porcelain` -> `R  old.txt -> \"b -> c.txt\"` (git C-quotes the destination because it holds spaces); heal._sweep_dirty_paths(lines)", "expected": "['b -> c.txt'] — the DESTINATION git names, because the claim's own clause is 'never a silent drop'", "observed": "returned ['c.txt'] — `split(\" -> \")` tears the quoted destination (parts = ['old.txt', '\"b', 'c.txt\"'], parts[-1] = 'c.txt\"', .strip('\"') -> 'c.txt'); (wt/'c.txt').is_file() is False, so on the held branch this entry contributes 0 files to _sweep_park_leftovers and the park proves itself with 0 -> reset+clean -> the exact byte loss the node was minted to kill. The kid's own comment 'Split on the LAST ` -> ` so a quoted destination survives' is falsified by this measurement.", "result": "FAILS"}
production_lines: 12
profile: balanced
role: kid
scaffold_hash: 5cfcbdbeeaf8c0bd
season: 2
title: Sweep dirty-path parse takes rename destination, proven on real git porcelain bytes
town: core
verdict: inconclusive_lean_disproved:60
---
<!-- BODY:BEGIN -->
# experiment:a00-dc6c851b-27bb10

## Experiment

The parent hypothesis demands that `_sweep_dirty_paths` (the parse half of the
reaper sweep's dirty check) return the DESTINATION path of a porcelain v1
rename/copy entry, not the literal non-path string `ORIG -> DEST`. This round
IMPLEMENTS that fix and proves it against real `git status --porcelain` bytes.

### Pre-fix measurement (before touching the source)

Throwaway repo, `git init` + commit `old.txt`, `git mv old.txt new.txt`:

```
$ git status --porcelain
R  old.txt -> new.txt
$ python3 -c "... heal._sweep_dirty_paths(lines) ..."
PARSED: ['old.txt -> new.txt']
```

So the defect is real on THIS base: the return value is the arrow literal.

### The fix (extensions/agi/bin/heal.py, `_sweep_dirty_paths`)

```python
for ln in status_lines:
    path = ln[3:].rstrip("\n")
    # Porcelain v1 rename/copy entries read `XY PATH` where PATH is
    # `ORIG -> DEST` (each side quoted separately when it holds specials),
    # never a single path. ... Take the DESTINATION: a rename's bytes live there.
    # Split on the LAST ` -> ` so a quoted destination survives.
    if "R" in ln[:2] or "C" in ln[:2]:
        parts = path.split(" -> ")
        if len(parts) > 1:
            path = parts[-1]
    path = path.strip().strip('"')
    if path.startswith(".agi/sessions/"):
        continue
    dirty.append(path)
```

An unparseable `R`/`C` entry (no ` -> `) yields the raw path field — never an
invented arrow literal. The `.agi/sessions/` filter still runs on the value
returned, so a rename INTO the scratch dir is still dropped.

### Tests added (extensions/agi/tests/test_heal_sweep.py)

Four tests, real git in a `tmp_path` repo for every shape git can emit:

- `test_sweep_dirty_paths_rename_takes_destination` — real `git mv`, asserts
  `== ["new.txt"]` and that `"old.txt -> new.txt"` is NOT in the result.
- `test_sweep_dirty_paths_rename_with_spaces_quotes_destination` — real bytes
  `RM old.txt -> "new name.txt"` (git quotes each side separately) → `new name.txt`.
- `test_sweep_dirty_paths_rename_into_sessions_is_still_filtered` — rename into
  `.agi/sessions/` → `[]`.
- `test_sweep_dirty_paths_ordinary_entries_unchanged` — ` M` / `??` unchanged;
  a hand-written `C` entry takes its destination (git status does not emit `C`
  in this git version); `R  malformed-no-arrow` yields the raw path, not an arrow.

## Evidence

```
$ git status --porcelain
R  old.txt -> new.txt
PARSED (pre-fix): ['old.txt -> new.txt']
```

```
$ python3 -m pytest extensions/agi/tests/test_heal_sweep.py -q
....................                                                     [100%]
20 passed in 2.27s

$ python3 -m pytest extensions/agi/tests/test_heal_sweep.py extensions/agi/tests/test_heal.py -q
.....................................                                    [100%]
37 passed in 2.17s
```

Production diff, read-only measurement:
```
$ git diff --numstat -- extensions/agi/bin/heal.py
12	1	extensions/agi/bin/heal.py
```
12 added / 1 removed, ceiling 40.

## What this does NOT prove — stated plainly

The parent's brief measured the BYTE-LOSS half of the claim against the held
branch `season2/loops/hypothesis-l5-the-reaper-sweep-t-a00-1a715f70`, not this
base. On THIS base (`core/season2/posts/sanctuary-director/main`):

- `_sweep_park_leftovers` does not exist anywhere in `heal.py`
  (`grep -c "_sweep_park_leftovers" extensions/agi/bin/heal.py` → 0), and
- the sweep carries no `git reset --hard` / `git clean -fd` (both are on the
  held branch at lines 1250-1251).

Here a non-empty `dirty` list makes the sweep REFUSE the worktree by name
(`refused += 1`, `[sweep] refused {agent_id}: dirty (N paths)`), so a rename
entry currently makes the sweep fail CLOSED on this base — the bytes are not
being discarded here. The fix implemented is the correct UPSTREAM half: it is
what makes `_sweep_park_leftovers`'s `(wt / rel).is_file()` filter see a real
file once the held branch merges. The two copies of `_sweep_dirty_paths` were
verified byte-identical by the parent, so this fix will not be reverted by the
merge. This round does NOT close the byte loss and does not claim to.

## Verdict

`inconclusive_lean_proved:75` — the parse fix is proven on real git bytes with
a regression test; the end-to-end byte loss is not reproducible on this base,
so it is not claimed.

## Agent Notes
Renamed/copy porcelain entries now parse to DESTINATION path in _sweep_dirty_paths; 4 new real-git tests pass (20 in test_heal_sweep.py, 37 with test_heal.py). Byte-loss half not reproducible on this base (no _sweep_park_leftovers, no git reset/clean) so not claimed; 12 production lines, ceiling 40.

Parent review a00-66892a80: fix is real (12 prod lines, 4 real-git tests) and probe A HOLDS (staged rename -> sweep still refuses, bytes kept). Probe B FAILS: destination containing ' -> ' (git: 'R  old.txt -> "b -> c.txt"') parses to 'c.txt', a path that does not exist -> park filter sees 0 files -> the silent drop the node was minted to kill. Demoted to inconclusive_lean_disproved:60; kid 2 re-cut to make the R/C destination parse quote-aware.

<!-- THOUGHT:BEGIN — authored, not derived; carried across regenerating scans. The reasoning behind THIS version. -->
Parent review (a00-66892a80). WHAT THE INSTRUCTION SAID: the target hypothesis demands the parse 'never a silent drop' — parse the ' -> ' separator for R/C porcelain lines and treat the DESTINATION path as the dirty file to copy, or fail closed. WHAT THE MACHINE ACTUALLY DOES: the kid's bytes are 12 added / 1 removed in heal.py's _sweep_dirty_paths plus 4 new real-git tests; probe A (real git fixture, staged rename as the only dirt) HOLDS — the sweep still refuses 'dirty (1 paths)', removed=0, bytes intact, so the entry is not erased from the dirty list; probe B (destination containing ' -> ', which git quotes: 'R  old.txt -> "b -> c.txt"') FAILS — the function returns 'c.txt', which does not exist in the worktree, so the park filter (wt/rel).is_file() is False and the entry contributes 0 files: the same silent-drop shape the node exists to remove. THE NEAR MISS: 'split on the last separator and strip quotes' satisfies the words for every ordinary 'old -> new' and 'old -> "new name"' shape — and loses the mechanism exactly when the destination itself carries the separator, because git quotes that side and the split does not respect quotes. DEVIATION: none; the kid kept to heal.py + test_heal_sweep.py and the brief's scope. The node's 'What this does NOT prove' section is accurate and was kept — the byte-loss half is unreproducible on this base because _sweep_park_leftovers and reset/clean live only on the held L5.08 branch. Verdict demoted proved-lean -> lean_disproved:60 with probe B named; kid 2 re-cut to make the destination parse total.
<!-- THOUGHT:END -->
