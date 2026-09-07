---
id: exp:g11-migration-rehearsal
mint_id: 58b01e6669b249ff83fb439a4c2bd6b3
type: experiment
parents:
  - goal:g11
confidence: 1.0
edited_by: season.py
evidence_runs: 4
season: 1
status: complete
subgraph: false
tags:
  - g11
  - migration
  - grid
thought_session: season
title: Four rehearsals of the two-repo merge on throwaway clones, including one reversed
---
<!-- THOUGHT:BEGIN — authored, not derived; carried across regenerating scans. The reasoning behind THIS version. -->
Adds run 4, the rollback rehearsal, which v1 listed under "what this does not
test". The owner asked for it before authorising the irreversible step, and it
was the right thing to ask for: it turned up a step that reasoning about
`git reset` had missed entirely — `reset --hard` does nothing to `refs/grid/*`,
so a rollback that omits an explicit ref deletion leaves the repo in a state
that is neither the old one nor the new one. That is now a named step rather
than something to remember.
<!-- THOUGHT:END -->

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
| 4 (`/tmp/rb`) | `daf4f287d` | **migrate, then reverse — byte-identical** |

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

## Run 4 — the rollback rehearsal

The gap run 3 left open. A full state fingerprint of the target was taken
before migrating — HEAD, every ref with its sha, the complete tracked tree
*with file modes*, the working-tree file list, remotes, and `status` — 682
lines. Then: migrate, then reverse.

```
git reset --hard <pre-migration HEAD>
git for-each-ref --format='delete %(refname)' refs/grid/ | git update-ref --stdin
git clean -fd
<remove any remote the migration added>
```

Refs went 7 -> 1087 -> 7. Commits 206 -> 698 -> 206. **The post-rollback
fingerprint is byte-identical to the pre-migration one**, all 682 lines.

Two things this establishes that reasoning about `git reset` did not:

- **The grid refs must be deleted explicitly.** `reset --hard` moves a branch
  tip; it does nothing to `refs/grid/*`, which arrive by fetch and would
  otherwise survive a rollback and leave the repo in a state that is neither
  the old one nor the new one. That is a real step, not a formality, and it is
  the step most likely to be forgotten under pressure.
- **`unify.py` leaves no stray remote.** The cleanup loop found nothing to
  remove, confirming the migrator removes its own temporary remote rather than
  relying on the rollback to do it.

Known residue, and it is benign: `reset --hard` plus ref deletion leaves the
migration's objects unreferenced in the object store until `git gc` collects
them. Disk only; nothing reachable, nothing that changes a fingerprint.

## What this does not test

- **A second project.** Only the `agi`/`agi-tree` pair was rehearsed. `fantasia`
  has its own clone and its own grid refs and is untouched by any of this.
- **Rollback of the *real* repo.** Run 4 reversed a clone. The real target has
  a remote with published history; a rollback after a push would need a force
  push, which is a different and worse operation. **Do not push the migrated
  engine until the result has been verified.**
- **The crons.** Every run happened with the live crontab untouched. Run 3's
  `publish-engine.sh` was invoked by hand, not observed firing at `:37`.