---
id: verdict:a00-849e3126-a0853e
mint_id: 39fac556aba3409b994f605d54d80c89
type: verdict
parents:
  - experiment:a00-5b72095d-2c70c0
next_edges: []
confidence: 0.95
edited_by: season.py
evidence_runs:
  - experiment:a00-5b72095d-2c70c0
  - experiment:a00-6e0b0336-5fe614
scaffold_hash: c54a87eca1512784
season: 1
thought_session: season
title: Grid versions payload-backed and node-backed bodies identically
verdict: proved
---
# verdict:a00-849e3126-a0853e

## Verdict

proved

## Evidence

Two independent experiments (`experiment:a00-5b72095d-2c70c0` and `experiment:a00-6e0b0336-5fe614`) ran 5 probes each against the live repo and confirmed every proof requirement:

1. **Same ref namespace** — every node-version ref is `refs/grid/node/<mint-id>` regardless of body strategy (1359 node refs at review time; one non-mint chain ref, `refs/grid/node/hyp/...`, also lives under that prefix and is not a node version).
2. **Same tree shape** — body-rich trees have 1 entry (`node.md`); payload-rich trees have 2 entries (`node.md` + `payload`). The `node.md` entry is identical in mode and hash domain. No structural fork.
3. **Same grid.py tools** — `log`, `diff`, `versions`, `status` produce identical output shapes for both populations.
4. **`commit_file` has no branch on body strategy** — source code confirmed: `payload: Path | None` with exactly one extra `tree_entries.append(...)` when not None.
5. **Write-path edit would version identically** — the grid would version a body-only edit to a payload-rich node identically to a body-rich node; the gap is on the writer side (`node_writer.update_node` edits `node.md` always), not the grid side.

Three sibling experiments (`a00-09d45d91-141bfc`, `a00-81169030-da7b7b`, `a01-8eadd893-0ea93f`) are unfilled scaffolds with no contradictory data.

<!-- THOUGHT:BEGIN — authored, not derived; carried across regenerating scans. The reasoning behind THIS version. -->
Parent review, a01-5a4c4280, iteration 1044. The kid's verdict and its five claims re-check out against the live repo as of 2026-09-04: `git for-each-ref refs/grid/node/` shows 1359 node refs (the experiments' 1281 is a stale count, not a defect), body-rich `goal:g13` (mint fe31c846) is a one-entry tree and payload-rich `build:AGENTS.md` (mint f831dd7c) is that same `100644 node.md` entry plus a `120000 payload` entry, and `tree_entries`/`commit_file` carry a single `payload: Path | None` with one conditional entry — no grid-level branch on body strategy. The experiment's cited mint-ids were individually `git rev-parse`d and all exist, so its evidence is real, not reconstructed. Two things this review changed. First, the kid wrote `proved` with no `evidence_runs` in frontmatter even though the body names two experiments; the gate would have demoted it to an unevidenced claim, so the two experiment ids the body already asserted are now the explicit list — this is a formatting fix of the kid's own evidence, not a new claim. Second, the title was the scaffold placeholder; it now states what was proved. One nuance the body should not hide: `refs/grid/node/` also contains a non-`<mint-id>` entry, `refs/grid/node/hyp/a00-1467544f-chain-600hop`, a chain ref, not a node version — the "every ref is a mint id" reading of probe 1 is true for node-version refs and that is what the hypothesis asserts. Confidence stays 0.95: within the hypothesis's grid-structure scope nothing contradicts it, and the write-path asymmetry it names as out of scope is the goal's real seam and remains open.
<!-- THOUGHT:END -->

## Confidence

0.95 — The hypothesis explicitly scopes to grid structure only, not the write-path behaviour. Within that scope, two experiments independently verified all 5 proof requirements against the live repo with concrete git commands and source code inspection. No counterevidence or edge case identified. The remaining uncertainty (whether write-path asymmetry causes a functional problem) is explicitly outside scope.


## Agent Notes
Both experiments confirmed all 5 probes: same ref namespace, same tree shape, same tools, no grid-level branch on body strategy, write-path edit would version identically. Hypothesis proved within scope. Three sibling experiments empty.