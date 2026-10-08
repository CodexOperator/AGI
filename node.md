---
id: experiment:a00-6e0b0336-5fe614
mint_id: e8ea0aed3df94dd89c41634aada8eda4
type: experiment
parents:
  - hypothesis:a00-dbd82e32-0b294f
next_edges: []
edited_by: season.py
scaffold_hash: 527a697de4332191
season: 1
thought_session: season
title: A00 6e0b0336 5fe614
---
# experiment:a00-6e0b0336-5fe614

## Experiment

Tested claim that grid layer versions body-rich and payload-rich nodes identically.

**Method.** Enumerated all `refs/grid/node/<mint-id>` refs; compared tree structure of a goal (body-rich) node vs a build (payload-rich) node; ran grid.py log/diff/versions against both; read commit_file/build_tree source to verify no branch on body strategy.

**Commands.**
```bash
git for-each-ref refs/grid/node/ --format='%(refname)' | wc -l
git ls-tree <goal-ref-tip>  # body-rich: 1 entry (node.md)
git ls-tree <build-ref-tip> # payload-rich: 2 entries (node.md + payload)
grid.py log <mint-id>       # both: same column format
grid.py diff <mint-id> --back 1  # both: diff on node.md
grid.py versions <mint-id>  # both: integer count
```

**Result.** All 5 proof requirements passed.

## Evidence

1. **Same ref namespace.** All 1281 nodes under `refs/grid/node/<mint-id>` — confirmed by `for-each-ref`. Body-rich (goal:g1) and payload-rich (build:AGENTS.md) both use the same naming.

2. **Same tree shape.** Body-rich: 1 entry `100644 blob <sha> node.md`. Payload-rich: same `node.md` entry plus `120000 blob <sha> payload`. No structural fork — payload is an additive entry.

3. **Same grid.py tools identical.** Both produce same column count and heading in `log`; both `diff` on `node.md`; both `versions` return integer count. No divergence in output shape.

4. **commit_file has no branch on body strategy.** Source confirms `payload: Path | None` param with one extra `tree_entries` entry when not None. No grid-level branch on body strategy.

5. **Write-path asymmetry confirmed.** The grid would version a build node body edit identically to a goal node body edit — the gap is on the writer side (update_node edits node.md always), not the grid side.

Grid claim proven; the gap goal:g13 names is indeed on the write side only.
