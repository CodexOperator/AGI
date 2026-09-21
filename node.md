---
id: experiment:a00-4a6d4345-a9cffb
mint_id: 26274b9c702c419789217c564337e499
type: experiment
parents:
  - hypothesis:a01-721930d9-d34989
next_edges: []
edited_by: season.py
scaffold_hash: 80dfd5dc68a4d4e6
season: 1
thought_session: season
title: A00 4a6d4345 a9cffb
---
# experiment:a00-4a6d4345-a9cffb

## Experiment

Tested whether `node_writer.update_node` (the engine's write path) can serve as the generator write path in place of `snapshot-goals.write_frontmatter` — the core of the "read/write join" hypothesis (`hypothesis:a01-721930d9-d34989`).

**Command:** `python3 /tmp/g13-join-experiment.py` from `/home/ubuntu/work/agi`
**Corpus:** 50 real goal nodes from `.agi/nodes/goal/`. All reads only; writes go to temp dirs.

**Three tests:**

### T1 — Serializer output comparison
`node_writer.render_frontmatter` vs `snapshot-goals` inline YAML serializer on the same frontmatter dict.

**Result: 50/50 differ.** Two sources of difference:
1. **Key ordering.** Engine uses `LEADING_KEYS + sorted(rest)`, write_frontmatter uses `sorted(fm.keys())`. Example for `goal:g1`:
   - Engine: `id, mint_id, type, confidence, goal_id, goal_kind, ...`
   - WF: `confidence, goal_id, goal_kind, heading_level, id, ...`
2. **Quoting heuristic.** Engine's `_needs_quoting` checks `": "` (with trailing space); write_frontmatter checks `any(c in sval for c in ":#'\"")`. Result: engine writes `id: goal:g1` (unquoted), write_frontmatter writes `id: "goal:g1"` (quoted because of the colon).

Both are valid YAML; both round-trip identically. The diff is cosmetic but systematic.

### T2 — Merge semantics equivalence
`write_frontmatter(preserve=existing_fm, new_fm)` vs `update_node(set_fm=new_fm)` — does the merge produce the same frontmatter dict?

**Result: 50/50 identical.** The merge logic is semantically equivalent: write_frontmatter's `{**preserve, **new_fm}` and update_node's `existing.update(set_fm)` produce the exact same key-value pairs. The existing-keys-are-preserved-by-default semantics of `update_node` already provide the preserve-mechanism the hypothesis claims is missing — it does not need a separate `preserve=` parameter.

### T3 — THOUGHT survival through update_node body change
On 7 goal nodes carrying an authored `THOUGHT` region, `update_node` with a body change preserved the thought via `_carry_thought`.

**Result: 7/7 preserved.** The mechanism in `node_writer.update_node` works correctly: old thought is carried into new body unless new body brings its own.

### Key insight
The hypothesis's claim that "the write path must first grow a preserve-keys mechanism it does not yet have" is **contradicted by the code**: `update_node` already preserves all existing keys by default — `set_fm` is a *merge* into existing, never a replacement. The `preserve=` param exists in `write_frontmatter` because that function *reconstructs* the file from scratch; `update_node` starts from the existing file and merges selectively. No engine-level `preserve=` hook is needed — the required semantics are already there.

## Evidence

Full output from the experiment script:

```
=== T1: SERIALIZER DIFF ===
  Loaded 50 goal frontmatters
  Key order diff example (node goal:g1):
    engine: ['id', 'mint_id', 'type', 'confidence', 'goal_id', 'goal_kind', 'heading_level', 'origin', 'seeds', 'status', 'tags', 'title']
    wf:     ['confidence', 'goal_id', 'goal_kind', 'heading_level', 'id', 'mint_id', 'origin', 'seeds', 'status', 'tags', 'title', 'type']
  Serializer output diff (node goal:g1):
    line 0: engine='id: goal:g1' vs wf='confidence: 1.0'
    line 1: engine='mint_id: 556869f3f6454ffe9118a793e062aa5f' vs wf='goal_id: G1'
    ...
  [FAIL] T1 serializer output equivalence: serializer output differs in 50/50 fms
  [FAIL] T1 key order equivalence: key order differs in 50/50 fms

=== T2: MERGE SEMANTICS ===
  [OK] T2 merge semantics equivalence: 50/50 merges produce identical dicts

=== T3: THOUGHT SURVIVAL THROUGH UPDATE_NODE ===
  [OK] T3 THOUGHT survival: 7/7 THOUGHT regions survive update_node

=== SUMMARY ===
Tests: 2/4 passing
  [FAIL] T1 serializer output equivalence: serializer output differs in 50/50 fms
  [FAIL] T1 key order equivalence: key order differs in 50/50 fms
  [OK] T2 merge semantics equivalence: 50/50 merges produce identical dicts
  [OK] T3 THOUGHT survival: 7/7 THOUGHT regions survive update_node
```

### Quoting heuristic diff (illustrated)

For a frontmatter key `id: "goal:g1"`:
- **write_frontmatter** checks `any(c in sval for c in ":#'\"")` → `goal:g1` contains `:` → quoted.
- **render_frontmatter** checks `": " in sval or sval.endswith(":") or " #" in sval` → `goal:g1` contains `: ` (colon, no space) → not matched → unquoted.

### Script location

`/tmp/g13-join-experiment.py` — may not survive reboot. Core method reproduced below: load frontmatter via `fm_reader.load_node_file`, render with both serializers, compare line by line for T1; construct `{**preserve, **new_fm, **origin}` vs `dict(fm).update(derived_keys); fm["origin"] = ...` for T2; copy node to temp dir, `update_node(... body=...)`, re-read, `extract_thought` for T3.