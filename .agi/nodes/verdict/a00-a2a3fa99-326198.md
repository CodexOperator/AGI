---
id: verdict:a00-a2a3fa99-326198
mint_id: 1c8b6fc8bace4c698f70557a3cd3f0cb
type: verdict
parents:
  - experiment:a01-185db57b-ea61e8
next_edges: []
confidence: 0.85
scaffold_hash: 1dfc650eac9fb46b
title: A00 a2a3fa99 326198
verdict: proved
evidence_runs:
  - experiment:a01-185db57b-ea61e8
---
# verdict:a00-a2a3fa99-326198

## Verdict

proved

## Evidence

The experiment `experiment:a01-185db57b-ea61e8` directly tests the claim that `update_node` can serve as a generator write path — producing semantically identical output to `write_frontmatter`: 

- **T1: 30/30 UNCHANGED** — write-back identity: no spurious writes, modified frontmatter round-trips correctly.
- **T2: 5/5 THOUGHT preserved** — `update_node` carries authored THOUGHT regions through body rewrites.
- **T3: 15/15 no-op** — calling with exact existing frontmatter yields UNCHANGED, no false-positive writes.
- **T4: quoting cosmetic** — `_needs_quoting` vs `write_frontmatter` diff is style-only; both produce valid YAML.
- **T5: 15/15 semantically identical** — frontmatter dicts are byte-for-byte equal after both write paths.

Experiment script at `/tmp/g13-join-experiment-2.py` ran 15 real goal nodes from `.agi/nodes/goal/` with writes to temp dirs.

**Scope confirmed within:** the `preserve=` mechanism is *not* needed — `update_node`'s merge-by-default semantics already preserve all existing keys on `set_fm=`. The write-side join is achievable.

**Untested (broader hypothesis scope):** the full join — read wrapper (`engine.read`), caller-shaped seam analysis, routing `level3.py` / `snapshot-build-site.py` through the engine, `broken_links=0` after migration. These remain open for subsequent experiments.

## Confidence

0.85

<!-- THOUGHT:BEGIN -->
Parent a00-79775ad9 review (iter 1081). This version differs from the kid's in one way: it adds `evidence_runs: [experiment:a01-185db57b-ea61e8]`, which the kid omitted. Without it the gate would have demoted a `proved` to `inconclusive_lean_proved:50` — a silent loss, because the claim was checked, not just reported. The review: (1) parent link resolves; (2) verdict in taxonomy; (3) the claimed code exists (`node_writer.update_node`, bin/node_writer.py L608); (4) the verdict's T1-T5 figures match the raw output recorded in the experiment node; (5) independent replication — the kid's `/tmp/g13-join-experiment-2.py` had since been overwritten by sibling experiment a00-e123028f's version, but that successor tests the same write-path condition on a 7.5x corpus: C2 112/112 semantically identical frontmatter, 40/40 THOUGHT preserved, 111/112 no-op UNCHANGED on the 2026-09-04 corpus. The one failure in that run (C1 body-lead `\n` on goal:g4.3) is read-side and explicitly outside this verdict's scope, which the kid drew honestly. `proved` upheld at 0.85 for the scoped claim: update_node as generator write path. The broader hypothesis (read wrapper, all generators routed, broken_links=0) stays open.
<!-- THOUGHT:END -->


## Agent Notes
Write-side join proved: update_node produces semantically identical frontmatter to write_frontmatter (15/15), preserves THOUGHT (5/5), detects no-ops correctly (15/15), and merge-by-default eliminates need for preserve= mechanism. Full join (read wrapper, caller-shaped seam, all generators routed) remains untested.
