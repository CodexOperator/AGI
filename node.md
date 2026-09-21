---
id: goal:g7.8
mint_id: 742ccf8373584908912f0350b6b8366a
type: goal
parents:
  - goal:g7
confidence: 1.0
edited_by: season.py
goal_id: G7.8
goal_kind: subgoal
heading_level: 3
origin: goals-doc
season: 1
seeds: []
status: horizon
tags:
  - goal
  - subgoal
thought_session: season
title: "G7.8: A generator mints parent ids it never checks exist"
---
Found 2026-08-25 while sweeping G7.1. **Corpus side resolved the same day; the
missing validation is what keeps this `active`.**

**First, a correction worth keeping, because the wrong framing nearly bought an
engine change that was not needed.** This was initially written up as "cannot be
fixed by editing a node", as though the graph had a region the normal rules did
not reach. That is backwards. `task:t-090` and `task:t-092` carry
`origin: build-site` — they are **derived nodes, exactly like `nodes/goal/` is
derived from this file.** "Edit the source, not the output" is not an exception
to how this system works, it *is* how it works; the only real question was which
source. Nothing here contradicts the philosophy, and the rule that already
covers it is the one at the top of this document.

`snapshot-build-site.py:371` derives a task's parent from its cavekit
requirement by string construction:

```python
domain, rnum = t["cavekit_req"].split("/", 1)
rnum = rnum.split(".")[0]          # R1.2 → R1
parent_hyp = f"hyp:{domain}-{rnum.lower()}"
```

**Nothing checks that the id it just built names a real node.** `build-site.md`
declares `graph-core/R11` for T-090 and T-092, so both get
`parents: [hyp:graph-core-r11]` — and the graph-core hypothesis family stops at
`hyp:graph-core-r10`. Two references that never resolved and never will.

**Why this is a generator defect and not a corpus defect, stated precisely:**
`parents` is a snapshot-owned key. `write_frontmatter`'s `preserve` merge
carries forward only fields the snapshot does *not* own (`{k: v for k, v in
preserve.items() if k not in fm}`), so a hand-corrected `parents:` on T-090 is
overwritten on the very next `--smoke` run. **The node is downstream of the
bug; the only durable edit is upstream of it.** This is 1ead9c965's rule —
fix the duplicate at its generator, not its output — arriving a second time
through a different door, which is the argument for treating it as structural
rather than incidental.

**The real root cause was in the kit, and the generator was reporting it
honestly.** `parse_kits()` mints one hypothesis per `### Rn:` block found in
`context/kits/cavekit-<domain>.md`. `cavekit-graph-core.md` contained
**R1 through R10 and stopped there.** Meanwhile `build-site.md` opens the same
domain with `### Domain: graph-core (11 R, 47 criteria, T-001..T-018, T-090,
T-092)` and gives both tasks `Cavekit Requirement: graph-core/R11` with eight
acceptance criteria named individually (R11.1 `traverse_bfs` … R11.8
`detect_cycle`). **The plan declared eleven requirements; the kit defined ten.**
`hyp:graph-core-r11` was never minted because there was nothing to mint it from.

So the dangling reference was not noise — it was the only symptom of a
**genuine inconsistency between two cavekit inputs**, and it pointed straight at
it. That is the integrity check doing precisely its job.

**Fixed 2026-08-25 at the input**: added the missing `### R11: Traversal and
Query API` block to `cavekit-graph-core.md`, transcribing the eight criteria
`build-site.md` already spelled out. The generator minted `hyp:graph-core-r11`
on the next run and both task references resolve. **Node count went up, not
down; nothing was hand-written into `nodes/`, and no reference was invented** —
R11 was always a real, documented requirement with a title and eight criteria.

Two things worth carrying forward from the fix:

- **It took two `--smoke` passes.** The first run minted the hypothesis *after*
  the integrity check had already read the corpus, so the check still reported
  both references as unresolved against a node that existed on disk by the time
  it printed. This is **S7**'s two-pass wiring defect, and S7 describes it only
  for `snapshot-goals.py` — it applies to `snapshot-build-site.py` identically.
  Anyone reading a single post-edit run will believe a fix failed when it
  succeeded.
- **Editing the kit is safe here specifically because cavekit is frozen.** No
  cavekit updates are being pulled pending its phase-out (below), so there is no
  upstream to clobber the edit. **This would be the wrong fix on a live
  dependency** — there it would have to go upstream or the generator would have
  to tolerate the gap.

**What remains open, and it is the part that matters:** the generator still
builds `f"hyp:{domain}-{rnum.lower()}"` and writes it as a parent **without ever
checking the id resolves.** The kit is consistent again, so nothing dangles
today — but the next task citing a requirement with no `### Rn:` block
reintroduces this silently, and the fixture is gone. Resolve `parent_hyp`
against the loaded corpus before writing; on a miss emit `parents: []` plus a
`WARN:` naming the task, the `cavekit_req` and the unresolved id —
warn-by-default, matching G7.1/G7.2/G7.5. **Do not mint the missing hypothesis
and do not drop the task**: an unattributed task is a real state, and a
fabricated ancestor is worse than a visible gap.

**Phase-out context (stated 2026-08-25, not yet a goal of its own).** The
intent is that this graph replaces `context/kits/` outright — the kits are a
smaller, weaker graph living inside a directory, which is the thing `agi-tree`
exists to be. Until that lands, `context/kits/` and
`context/plans/build-site.md` remain load-bearing generator inputs for 163
`origin: build-site` nodes, and **H0i still applies with full force: deleting or
emptying either one prunes every one of those nodes on the next run.** Retire
them by deprecating the nodes first. When the phase-out is committed to, it
wants its own goal — it subsumes this one, since a generator that no longer
exists cannot mint an unvalidated parent.

## A concrete instance, found 2026-08-27 — and it survives hand-repair

`context/plans/build-site.md` declares `T-020: Schema removal handling` in
three places — the per-tier summary (line 857), the T3 tier table (line 972)
and the mermaid dependency graph (`T-019 --> T-020`, `T-020 --> T-012`) — but
gives it **no `#### T-020:` definition block**. `snapshot-build-site.py`
mints nodes only from definition blocks, so `task:t-020` is never created,
while `task:t-012` is minted carrying `blocked_by: [task:t-011, task:t-019,
task:t-020]`. The generator writes a reference to a node it does not create
and checks nothing.

**The instructive part is what happened next.** The dangling ref was removed
by hand from `task:t-012` during the 2026-08-27 integrity pass, verified
gone, and was **back after the next `driver.sh --smoke`** — because `task`
nodes are `origin: build-site` and the generator re-derived the node from the
unchanged input. That is H0i's mechanism observed from the other side: not
data loss this time, but a hand-repair silently reverted.

So this class of defect has a property worth stating: **it cannot be fixed in
the graph at all.** The only durable fix is in the generator or its input.
Which of the two is a real decision, and neither branch is free:

- **Define T-020** in `build-site.md` and it mints. But the input supplies
  only a title and one blocker — `cavekit_req`, `acceptance_criteria` and
  `effort` would have to be invented, and inventing acceptance criteria for a
  task nobody wrote is worse than a dangling edge.
- **Drop T-020** from T-012's `blockedBy` and the reference resolves. But the
  dependency is stated three times and is plainly intended; deleting it
  discards a real design statement to satisfy a checker.

Left dangling on purpose, pending that decision. What this goal actually
asks for is upstream of both: the generator should **refuse to mint a
reference it cannot resolve**, or emit it and fail loudly, rather than
writing a broken edge and exiting 0. Pairs with **G7.5** and **G7.9**.