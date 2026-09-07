---
id: goal:g7.2
mint_id: cd0a9c2ecab64141bdc4938c4d3892ae
type: goal
parents:
  - goal:g7
confidence: 1.0
edited_by: season.py
goal_id: G7.2
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
title: "G7.2: Duplicate node ids silently hide files on disk"
---
Found 2026-08-22 by the G9.1 dashboard on its first run, which is the argument
for G9 in miniature: **17 node ids are declared by two files each.** The loader
keeps one and drops the other, so 17 files sit on disk fully invisible to every
tool that reads this graph — the renderer, the metrics, the chain finder, and
the dashboard itself.

The dropped file is frequently the *larger* one: `app-purpose:graph-core` keeps
a 276-byte file and hides a 575-byte one; `bigger-outcome:graph-core-r1` keeps
315 bytes and hides 1,217. This is not a cosmetic duplicate — it is content
loss that has already happened and that nothing reported.

Fix: id uniqueness must be checked at load and at write. A second file claiming
a live id is an error, not a silent preference for whichever sorts first.
**Do not resolve the existing 17 by deleting either side** — merge or re-id
them deliberately, the G7 rule.

**Second consequence, found 2026-08-23, and it breaks the backup rather than
the render: a duplicated id forks its grid ref and the fork cannot be pushed.**
`grid.py commit --all` walks node *files*, so both claimants get committed to
the single ref `refs/grid/node/<id>` — each run picking whichever it reaches
first as the new tip. The ref's history therefore alternates between two
divergent lines, and `git push` correctly refuses it as non-fast-forward.

Observed on `verdict:schema-registry-r2` and `verdict:session-management-r1`:
both rejected on push while the other 29 refs in the same run went through.
**Those two nodes' version history has stopped syncing to the remote** and has
been doing so silently — the push prints a rejection among a wall of successful
ref updates, and nothing else reports it.

This raises the priority. G7.2 was previously "17 files are invisible to
readers", which is bad but static. It is now also **an ongoing backup hole in
the one mechanism G7 exists to guarantee** — the grid is what makes it safe to
stop mid-sprint, and for these ids it is not running. Note the resolution
order this forces: the ref cannot be repaired by force-pushing either side
(that destroys one history, which is the G7 rule again), so **the duplicate ids
must be resolved first and the refs rebuilt afterwards.**