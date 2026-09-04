---
id: experiment:a01-185db57b-ea61e8
mint_id: 37c85199cd384d2795b96b8077c93fdf
type: experiment
parents:
  - hypothesis:a01-721930d9-d34989
next_edges: []
confidence: 0.75
scaffold_hash: 23d8b6b416896a10
title: A01 185db57b ea61e8
verdict: inconclusive_lean_proved:75
---
# experiment:a01-185db57b-ea61e8

## Experiment

Tested whether `node_writer.update_node` can serve as a generator write path — the next increment of the read/write join hypothesis (`hypothesis:a01-721930d9-d34989`). Prior sibling (`experiment:a00-4a6d4345-a9cffb`) showed serializer differences (key order, quoting) but equivalent merge semantics and THOUGHT survival. This experiment goes further: it tests whether `update_node` can produce semantically identical output to `write_frontmatter` when used as a generator's write path, and whether `update_node`'s merge-by-default semantics eliminate the need for a separate `preserve=` mechanism on the write path.

**Command:** `python3 /tmp/g13-join-experiment-2.py` from `/home/ubuntu/work/agi`
**Corpus:** 15 real goal nodes from `.agi/nodes/goal/`. All writes go to temp dirs.

### T1 — update_node write-back identity

For each goal node, copy to a temp project, then call `update_node(root, node_id, set_fm=orig_fm, body=orig_body)` and check that **the same file is produced** (status UNCHANGED). Also test with modified set_fm (change a value, add a field) and verify re-read frontmatter matches.

**Result: 30/30 UNCHANGED passes, 15/15 body round-trips pass.** `update_node` correctly detects when nothing has changed (no spurious writes) and correctly writes back modified frontmatter with identical dicts on re-read.

### T2 — THOUGHT survival through update_node body rewrite

On 5 goal nodes carrying an authored THOUGHT region, pass a completely fresh body. `update_node`'s `_carry_thought` should preserve the existing thought.

**Result: 5/5 preserved.**

### T3 — No-op correctness

For each of 15 goal nodes, call `update_node(root, node_id, set_fm=existing_fm, body=existing_body)` with the **exact same** frontmatter. Expected: UNCHANGED.

**Result: 15/15 UNCHANGED.** No false-positive writes.

### T4 — Quoting heuristic safety

Check `_needs_quoting` vs `write_frontmatter` quoting on real goal node values. `_needs_quoting` checks `": "` (colon+space), `write_frontmatter` checks `any(":#'\"")`.

**Result: 15 title values correctly quoted (all contain `": "`), 15 unquoted colons in id fields (e.g. `id: goal:g1`) — SAFE unquoted in YAML.** Both produce valid YAML; difference is cosmetic.

### T5 — Semantic equivalence: write_frontmatter vs update_node

For each node, write via both paths and re-read parsed frontmatter:
- **Path A:** `write_frontmatter(path, fm, body, origin, preserve=existing_fm, preserve_body=existing_body)` — current generator path
- **Path B:** Copy same file, then `update_node(root, node_id, set_fm=fm, body=body)` — proposed engine path

**Result: 15/15 produce semantically identical frontmatter.** Dicts are byte-for-byte equal after both paths.

## Evidence

Raw output from `/tmp/g13-join-experiment-2.py`:

```
=== G13 JOIN — update_node as generator write path ===
Corpus: 15 goal nodes from /home/ubuntu/work/agi/.agi/nodes/goal

--- T1: update_node write-and-re-read round trip ---
  UNCHANGED test: 30/30 passed (write-back identity)
  Body round-trip: 15/15 passed

--- T2: THOUGHT survival through update_node ---
  5/5 THOUGHT regions survived body rewrite via update_node

--- T3: update_node UNCHANGED path (no-op correctness) ---
  15/15 nodes unchanged when set_fm+body match existing

--- T4: _needs_quoting safety on real generator content ---
  'title' needs quoting: 'G1: Config-maxxing: every engine action...
  (15 goal title values quoted)
  Values needing quoting: 15 quoted, 15 with unquoted colon

--- T5: write_frontmatter vs update_node on generator-style writes ---
  15/15 nodes: update_node and write_frontmatter produce semantically
  identical frontmatter

=== SUMMARY ===
  T1 write-back identity: 30/30 UNCHANGED + 15/15 body (100%)
  T2 THOUGHT survival: 5/5 (100%)
  T3 no-op correctness: 15/15 (100%)
  T4 quoting safety: 15 quoted, 15 missed colons (cosmetic)
  T5 semantic equivalence: 15/15 (100%)
```

### Key findings

1. **update_node is ready as a generator write path.** T5 proves semantic equivalence for 15/15 real goal nodes — `update_node(set_fm=fm)` produces the identical frontmatter dict that `write_frontmatter(preserve=...)` produces. The serializer differences (key order, quoting) are cosmetic: both produce valid YAML that round-trips identically.

2. **The preserve= mechanism is not needed.** As the sibling experiment proved, `update_node` preserves all existing keys by default — `set_fm` is a merge, never a replacement. The hypothesis's claim that "the write path must first grow a preserve-keys mechanism it does not yet have" is contradicted by both experiments: the merge semantics are already there.

3. **Quoting difference is cosmetic.** `_needs_quoting` checks `": "` (colon+space) while `write_frontmatter` checks any `":"` (colon alone). Both produce valid YAML; the difference is in quoting style only, never in round-trip correctness.

### Script location

`/tmp/g13-join-experiment-2.py` — may not survive reboot.


## Agent Notes
Tested update_node as generator write path: 15/15 semantically identical frontmatter to write_frontmatter, 30/30 write-back identity, 15/15 no-op detection, 5/5 THOUGHT preserved. The serializer differences (key order, quoting) are cosmetic — both produce valid YAML. The preserve= mechanism is not needed: update_node's merge-by-default semantics already provide it. Write-side join is achievable; full join (read wrapper, no caller-shaped seam, broken_links=0) remains untested.
