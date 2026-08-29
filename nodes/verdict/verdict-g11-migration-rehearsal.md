---
confidence: 0.9
evidence_runs:
  - exp:g11-migration-rehearsal
id: "verdict:g11-migration-rehearsal"
mint_id: 469b6ce3ffac489fb279c903282eca99
parents:
  - exp:g11-migration-rehearsal
status: open
subgraph: false
tags:
  - g11
  - migration
  - grid
title: "The merge is lossless on real content, and it must be preceded by a publish"
verdict: proved
type: verdict
---

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

- **That the real migration is safe to run unattended.** Three rehearsals on
  throwaway clones are not a reversed migration. Nothing here was rolled back;
  the clones were discarded, which proves only that a bad run is cheap when the
  target is disposable.
- **That this generalises to another project.** Only the `agi`/`agi-tree` pair
  was tested. `fantasia` has its own clone, its own grid refs and its own cron,
  and G8.2's falsifier — a third project reaching the same result with no engine
  change — has not been run against this layout.
- **The cron interaction.** Every run happened with the live crontab untouched
  and `publish-engine.sh` invoked by hand. The `:37` job publishing *during* a
  migration is exactly the race `crons_live` exists to prevent and it has not
  been observed, only designed against.

## Why confidence is 0.9 and not higher

The lossless claim is measured across eight invariants on real content, so the
uncertainty is not in whether the merge preserves data. It is that a rehearsal
on clones cannot exercise the one property that matters most at the moment of
the real cut: that the operation is **reversible**. Until a migration is run and
then undone, the recovery story is `git reset` reasoned about rather than
performed.
