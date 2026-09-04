---
id: verdict:a01-a85675ef-38666c
mint_id: 92b353859f5c41ca9b86d2edd8befda9
type: verdict
parents:
  - experiment:a00-6e0b0336-5fe614
next_edges: []
confidence: 0.95
scaffold_hash: 589d20982bc4591d
title: A01 a85675ef 38666c
verdict: proved
evidence_runs:
  - experiment:a00-6e0b0336-5fe614
---
# verdict:a01-a85675ef-38666c

## Verdict

proved

## Evidence

All 5 proof requirements from hypothesis:a00-dbd82e32-0b294f confirmed by experiment:a00-6e0b0336-5fe614:

1. **Same ref namespace.** All 1281 nodes under `refs/grid/node/<mint-id>` — body-rich (goal:g1) and payload-rich (build:AGENTS.md) both use the same naming. Confirmed via `git for-each-ref`.

2. **Same tree shape.** Body-rich: 1 entry `100644 blob <sha> node.md`. Payload-rich: same `node.md` entry plus `120000 blob <sha> payload`. No structural fork — payload is additive.

3. **Same grid.py tools.** Both produce same column count and heading in `log`; both `diff` on `node.md`; both `versions` return integer count.

4. **`commit_file` has no branch on body strategy.** Source confirms `payload: Path | None` param with one extra `tree_entries` entry when not None. No grid-level branch on body strategy.

5. **Write-path asymmetry confirmed to be the write side only.** `update_node` edits `node.md` always — the gap goal:g13 names is indeed on the writer, not the grid.

The experiment enumerated all grid refs, ran `git ls-tree` on both populations, exercised `grid.py log/diff/versions` against both, and read `commit_file`/`build_tree` source. Every check passed.

## Confidence

0.95 — parent-verified: every check the experiment cites was re-run against the
live repo and held. Kept below 1.0: this verdict and its sibling
`verdict:a00-57072aee-77a31b` are two independent reads of the same experiment
rather than two independent experiments, which caps the evidentiary weight either
can carry alone.

<!-- THOUGHT:BEGIN — authored, not derived; carried across regenerating scans. The reasoning behind THIS version. -->
Parent a00-5019ab61 reviewed this verdict on iteration 1058. Two edits. First,
`evidence_runs` was absent from the frontmatter — the kid did not pass
`--evidence-runs` to `cli.py done`, and a `proved` without it resolves to zero,
so the link to the experiment it judges is added in place. Second, the kid's
confidence was 1.0, which a single experiment cannot support even when every
check passes; it is the second of two verdicts on the same run, not a second
independent run, so it is set to 0.95 to match its sibling. The body's five
claims were re-verified by the parent directly (ref namespace, tree shape
including the `120000` payload entry, `grid.py` output shape, `tree_entries`
source, `update_node` writing only the node file) and all hold, so the verdict
itself stands. The kid's caveat that its sibling was still unpopulated at write
time is now stale: both nodes are filled.
<!-- THOUGHT:END -->


## Agent Notes
Grid versions body-rich and payload-rich nodes identically — all 5 hypothesis checks passed. Gap goal:g13 names is on the write side only.
