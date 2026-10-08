---
id: verdict:g11-migration-rehearsal
mint_id: 469b6ce3ffac489fb279c903282eca99
type: verdict
parents:
  - exp:g11-migration-rehearsal
confidence: 0.95
edited_by: season.py
evidence_runs:
  - exp:g11-migration-rehearsal
season: 1
status: open
subgraph: false
tags:
  - g11
  - migration
  - grid
thought_session: season
title: The merge is lossless and reversible, and it must be preceded by a publish
verdict: proved
---
<!-- THOUGHT:BEGIN — authored, not derived; carried across regenerating scans. The reasoning behind THIS version. -->
v1 withheld 0.1 of confidence for one named reason: no migration had ever been
reversed, so reversibility was reasoned about rather than performed. Run 4
performed it — migrate, then reverse, post-rollback fingerprint byte-identical
across 682 lines covering refs, tree, modes and working files. The reason for
the discount is gone, so it is removed rather than left as a hedge.

Confidence moves to 0.95, not 1.0, and the remaining gap is now a different
claim than before: run 4 reversed a *clone*. The real target has a published
remote, and a rollback after a push needs a force push — a materially worse
operation. That is why "do not push until verified" is now a stated condition
of this verdict rather than a note in the experiment.
<!-- THOUGHT:END -->

**VERDICT: proved** — merging `agi-tree` into `agi` under `.agi/` loses
nothing, on the real corpus, checked by a tool that did not write the
migration. **With one precondition that the rehearsal discovered and that the
plan did not contain: publish first.**

## The claim that holds

807 nodes in, 807 out, zero bytes changed. 1078 grid refs in, 1078 out, none
missing, none diverged. The graph's 488 commits arrive as genuine ancestors of
the unified HEAD, not as a squashed import. 199 of 199 `payload_ref` values
resolve unchanged. `find_project_root` on the result returns `<repo>/.agi`, and
`GOALS.md` lands at the repo root rather than inside the dot directory.

Stated at the level it actually holds: **for this one repo pair, on three runs,
against a checker whose author never read the migrator.** Two independently
written tools agreeing is stronger than one tool reporting success, and it is
weaker than a reversed migration. See "not endorsed" below.

## The precondition, which is the useful half of this verdict

`unify.py` builds the unified repo from a clone of the **engine**, and the
engine is only as current as its last publish. Run 2 failed with four
unresolved `payload_ref`s — `unify.py`, `verify_unified.py` and their tests —
all of which existed only in `payloads/` (gitignored) and in their grid refs,
because the graph was three commits ahead of the last publish.

**Nothing was lost:** the bytes were readable via `grid.py payload` throughout,
and the refs transferred intact. What broke is narrower and easy to miss — the
migrated *working tree* was missing four files the graph correctly described.
A migration run at that moment would have produced a repo that is complete in
its refs and incomplete on disk, which is the most confusing possible state to
debug later.

So the iteration-4 sequence gains a step, and the order is not negotiable:

1. `crons_live: false` — stop the four crons racing the move
2. **`publish-engine.sh` — the engine tree must carry every payload the graph knows about**
3. migrate
4. `verify_unified.py`, expecting 8/8
5. `crons_live: true` with rewritten paths

`unify.py` should refuse, not warn, when the graph is ahead of the last publish.
That gate does not exist yet and is the one concrete change this verdict asks
for before step 3 runs for real.

## What is explicitly NOT endorsed

- **That the real migration is safe to run unattended.** Reversibility is now
  demonstrated (run 4), but on a clone, and with a human reading the output at
  each step. An unattended run is a different claim and is not made here.
- **That a rollback works after a push.** Run 4 reversed a repo whose remote
  had never seen the migration. Once the migrated engine is pushed, rollback
  needs a force push against published history — materially worse. **Condition
  of this verdict: do not push the migrated engine until `verify_unified.py`
  reports 8/8.**
- **That this generalises to another project.** Only the `agi`/`agi-tree` pair
  was tested. `fantasia` has its own clone, its own grid refs and its own cron,
  and G8.2's falsifier — a third project reaching the same result with no engine
  change — has not been run against this layout.
- **The cron interaction.** Every run happened with the live crontab untouched
  and `publish-engine.sh` invoked by hand. The `:37` job publishing *during* a
  migration is exactly the race `crons_live` exists to prevent and it has not
  been observed, only designed against.

## Rollback, and the step that reasoning had missed

Run 4 migrated a clone and then reversed it. Refs 7 -> 1087 -> 7, commits
206 -> 698 -> 206, and a 682-line fingerprint — HEAD, every ref with its sha,
the tracked tree with file modes, the working-tree file list, remotes and
status — **byte-identical before and after**.

The rehearsal earned its cost by turning up a step that reasoning about
`git reset` had missed: **`reset --hard` does nothing to `refs/grid/*`.** Those
arrive by fetch, survive a branch reset, and would leave a rolled-back repo
holding 1,080 refs from a migration that supposedly did not happen — neither
the old state nor the new one. The rollback sequence is therefore four
operations, not one:

```
git reset --hard <pre-migration HEAD>
git for-each-ref --format='delete %(refname)' refs/grid/ | git update-ref --stdin
git clean -fd
<remove the temporary remote, if the migrator did not>
```

**Record the pre-migration HEAD before starting.** The whole recovery hangs off
a sha that stops being reachable from any branch the moment the migration
commits.

## Why confidence is 0.95 and not 1.0

The lossless claim is measured across eight invariants on real content and the
reversibility claim is now demonstrated rather than argued. What remains is
scope: every run was against a disposable clone whose remote had never seen the
migration. The real cut happens once, against a repo with published history, and
the property that has not been exercised is recovery *after* that history has
been shared.