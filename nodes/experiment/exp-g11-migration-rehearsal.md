---
confidence: 1.0
evidence_runs: 3
id: "exp:g11-migration-rehearsal"
mint_id: 58b01e6669b249ff83fb439a4c2bd6b3
parents:
  - goal:g11
status: complete
subgraph: false
tags:
  - g11
  - migration
  - grid
title: "Three rehearsals of the two-repo merge on throwaway clones, checked by a tool that did not write it"
type: experiment
---

**Question.** Does merging `agi-tree` into `agi` under `.agi/` lose anything —
a node, a grid ref, a history, or a payload?

**Method, and the part that makes it evidence rather than a self-report.** Two
tools were written by two agents working in parallel, with the checker's author
barred from reading the migrator. `bin/unify.py` performs the merge;
`bin/verify_unified.py` compares a pre-migration graph repo against a
post-migration unified repo across eight named invariants and exits non-zero if
any fail. Neither imports the other. A bug shared between them would have to be
arrived at independently.

Each run: fresh `git clone` of both real repos into `/tmp`, push the grid refs
into the tree clone, run `unify.py --dry-run`, assert the target's HEAD is
unchanged, run `unify.py --yes`, then run `verify_unified.py` against the real
graph repo as `--before`. The real repos were never a migration target; their
HEADs were checked before and after every run.

## Runs

| run | graph @ | result |
|---|---|---|
| 1 (`/tmp/u3`) | `2ff2ef7ec` | 7/8 — `no_node_bytes_changed` failed, 1 path |
| 2 (`/tmp/u4`) | `f8ccb14e5` | 7/8 — `payload_refs_resolve` failed, 4 unresolved |
| 3 (`/tmp/u5`) | `f8ccb14e5` + publish | **8/8 — "OK — nothing lost"** |

Both failures were real and neither was a defect in the migration.

**Run 1** named exactly one offending path out of 803:
`goal/g11-one-repo-the-graph-lives-inside.md`. The clone's copy was
byte-identical to `HEAD`; the working tree's was not, because the parent had
edited that node after the clone was taken. A 1-in-803 difference, detected and
named. That is the byte check working on real content, which is the only place
it had been exercised outside fixtures.

**Run 2 is the finding worth carrying into the migration itself.** Four
`payload_ref` values did not resolve: `unify.py`, `verify_unified.py` and their
two test files. All four existed only under `payloads/` — the gitignored
staging checkout — and in their grid refs. **Nothing was lost**; `grid.py
payload build:bin-unify` reads the bytes back. But the engine tree did not
contain them, because the last publish was from graph commit `78a95fa89` and
the graph was three commits past it.

So the migration inherits the publish lag. `unify.py` clones the *engine* to
build the unified repo, and the engine is only as current as its last publish.
Any payload authored but not yet published is absent from the migrated working
tree even though its bytes ride along in the grid refs that transfer intact.

**Run 3 tested the remedy** — `publish-engine.sh` first, then migrate — and all
eight checks passed.

## Result, run 3

```
[PASS] no_node_lost             807 before, 807 after
[PASS] no_node_bytes_changed    807 hashed, 0 missing, 0 extra, 0 diverged
[PASS] no_grid_ref_lost         1078 before, 1078 after, 0 diverged
[PASS] both_histories_present   f8ccb14e579a is an ancestor of 10c95f3bb993
[PASS] payload_refs_resolve     199 checked, 0 unresolved, 199 before
[PASS] resolver_agrees          find_project_root -> <repo>/.agi
[PASS] goals_at_repo_root       at the root, absent from .agi/
[PASS] config_at_expected_path  .agi/config.json exists and parses
OK — nothing lost
```

Commits `206 -> 697`, the graph's 488 arriving as real ancestors rather than a
squashed import.

## The zero-rewrite property, confirmed on real content

199 of 199 `payload_ref` values resolved **unchanged**. `G11` originally
estimated 375 would need rewriting; the corrected claim is zero, and this is
the measurement behind it. A `payload_ref` is stored relative to the engine
root; under the `.agi` layout `source_root` resolves to that same directory.
The migration touches history, refs and two file locations, and rewrites no
node.

## What this does not test

- **A second project.** Only the `agi`/`agi-tree` pair was rehearsed. `fantasia`
  has its own clone and its own grid refs and is untouched by any of this.
- **Rollback.** No run was reversed. The clones were discarded instead, which is
  not the same as proving the real migration can be undone.
- **The crons.** Every run happened with the live crontab untouched. Run 3's
  `publish-engine.sh` was invoked by hand, not observed firing at `:37`.
