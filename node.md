---
id: experiment:a00-26810cc8-02c0d8
mint_id: 8d304460a4d9425a9ca078e6e029c68d
type: experiment
parents:
  - hypothesis:loop-scoped-iteration-ids-cannot-clobber
next_edges: []
confidence: 0.85
edited_by: season.py
scaffold_hash: f5b838fb8abda805
season: 1
thought_session: season
title: Loop-scoped ids are implemented, dead code, no tests
verdict: inconclusive_lean_disproved:85
---
# experiment:a00-26810cc8-02c0d8

## Experiment

Verified current state of the loop-scoped iteration id implementation after the hypothesis was disproved, then the code landed.

**Static code reading of `extensions/agi/bin/locations.py`:**
- `iteration_id()` — parses int, digit string, `L<loop>.<nn>`, and `iter-`-prefixed dir names. Returns canonical int or str.
- `format_loop_iteration(loop, counter)` — formats `"L1.08"`
- `iteration_dirname(id)` — returns `"iter-007"` for int, `"iter-L1.08"` for loop-scoped str
- `iteration_dir(root, id)` — single path resolver: `<root>/sessions/<iteration_dirname>`
- `list_iterations(root)` — discovers all sessions dirs (both numeric and loop-scoped)
- `next_free_iteration(root, loop, after=)` — allocator: `loop=None` for numeric, `loop="L1"` for loop-scoped. Returns lowest free id
- `claim_iteration(root, loop=, explicit=, after=, dry_run=)` — atomic claim: explicit raises `IterationOccupied` if dir holds data; auto-loop iterates `next_free` with `mkdir` race handling
- `loop_label(root, explicit, config)` — resolves which loop: flag > `$AGI_LOOP` env var > config `loop` key > newest on disk > `"L1"` default
- `IterationOccupied` exception — raised when explicit id targets a non-empty dir
- `_occupancy(d)` — checks what a dir holds: manifest > entries > None

**Live allocator test (2026-09-04):**
```
next free numeric: 1 (type=int)
next free L1: 'L1.01'
claimed: 1
claim_iteration(explicit=1) on empty dir -> returns 1 (empty dir accepted)
next auto after claim: 2
occupancy with manifest.json: 'a manifest'
```

**Live driver.sh check (`extensions/agi/driver.sh:239`):**
```
for i in $(seq 1 "$MAX_ITERS"); do
  iter_run "$i"
```
The allocator (`claim_iteration`) is never called. `iter_run` passes plain ints starting at 1 each time.

**Test coverage check (`grep -rn "next_free_iteration\|claim_iteration\|loop_label\|IterationOccupied\|format_loop_iteration" extensions/agi/tests/`):**
Zero matches. None of the allocator functions have test coverage.

**Callers check (`grep -rn "claim_iter\|next_free_iter\|IterationOccupied" extensions/agi/ --include="*.py" --include="*.sh"`):**
Only in `locations.py` itself (definition) and `locations.py`'s own `main` CLI. No real caller uses the allocator.

**Full test suite:** 1453 passed, 1 flaky failure (test in test_publish_alarm.py, passes in isolation). All existing iteration-formatting tests pass.

## Evidence

### 1. Full allocator exists in `extensions/agi/bin/locations.py`

Lines 345–595 contain the complete implementation: `iteration_id`, `format_loop_iteration`, `iteration_dirname`, `iteration_dir`, `list_iterations`, `next_free_iteration`, `claim_iteration`, `loop_label`, `IterationOccupied`, `_occupancy`. All referenced from `# --- iterations ---` section comment (goal:g11, resolving the hypothesis).

### 2. `driver.sh:239` still uses `seq 1 "$MAX_ITERS"`

```bash
for i in $(seq 1 "$MAX_ITERS"); do
  iter_run "$i"
```
Passes plain `$i` (1, 2, 3…) to `iter_run`, which passes it as positional arg `$n` to `dispatch.py`, `post_wire.py`, `cli.py status`. No call to `locations.py --claim-iter` or equivalent.

### 3. `dispatch.py:316` uses `locations.iteration_dir(root, args.iter_n)`

The single resolver supports loop-scoped ids at the path level — it would produce `iter-L1.01` if a loop-scoped str arrived. But `args.iter_n` is always a plain int from driver.sh, so paths are always `iter-001`, `iter-002`…

### 4. Zero test coverage for the allocator

`rg "next_free_iteration|claim_iteration|loop_label|IterationOccupied|format_loop_iteration" extensions/agi/tests/` returns no results. The allocator functions are exercised only by `locations.py`'s own `main` CLI (`--claim-iter`).

### 5. `iter-NNN-graph.json` is still a plain overwrite

`extensions/agi/bin/post_wire.py:516`:
```python
graph_path = iter_dir / f"{iter_dir.name}-graph.json"
graph_path.write_text(json.dumps(graph_data, indent=2), encoding="utf-8")
```
No merge guard. The dispatch.py `_merge_manifest` guard (goal:s28) protects `manifest.json` only.

### 6. Full test suite pass

`python3 -m pytest extensions/agi/tests/ -q` → 1453 passed, 1 flaky (test_publish_alarm.py, passes in isolation). No regressions.


## Agent Notes
Verified locations.py has full loop-scoped allocator (next_free_iteration, claim_iteration, IterationOccupied, loop_label) but 0 test coverage and driver.sh still uses seq 1 N — dead code, never wired. post_wire.py graph.json is still plain overwrite. Existing verdict stands.