---
id: exp:g5-lifecycle-enforcement
mint_id: 866e3a477f4840429fabb6ae38aed316
type: experiment
parents:
  - goal:g5
confidence: 0.65
edited_by: season.py
evidence_runs: []
provenance: direct-engine-edit
season: 1
subgraph: false
tags:
  - g5
  - g6.1
  - metrics
thought_session: season
title: "G5 lifecycle enforcement: scoring exclusion, L5 rotation, L18 degrade — landed as a direct engine edit"
---
**Provenance deviation, stated first:** this work was made as a direct,
uncommitted edit to `/home/ubuntu/work/agi` — no idea/hypothesis node preceded
it, no chain led here. That is exactly the defect `goal:g6.1` names: "a change
that appears in the engine without a node behind it is the open loop G6
exists to close." This node is written after the fact to record what
happened, not to manufacture the chain that should have come first. The code
is real and tested; the process that produced it skipped the graph.

**What was changed (verified against `git -C /home/ubuntu/work/agi diff`,
uncommitted at the time of writing):**

1. `extensions/agi/bin/metrics.py` — new `SCORING_GOAL_STATUSES = {"active",
   "horizon"}` and `goal_attribution()`. Walks each node's `parents` chain up
   to the goal(s) it descends from. A node under only `phasing-out`/`complete`
   goals is excluded from `outcome_coverage` but stays counted in whole-graph
   totals (`mvp_count`, `node_count`). A node under no goal at all still
   scores — a deliberately conservative default, called out in the code
   comment, because most of this corpus predates goal nodes. New emitted
   metrics: `scoring_mvp_count`, `scoring_hypothesis_count`,
   `retired_goal_nodes`, `unattributed_nodes`, `goals_active`,
   `goals_horizon`, `goals_retired`, `goal_count`.
2. `metrics.py` `emit()` — a `METRIC_WARNING goal_rotation=<active>/<max>` to
   stderr+stdout when `goals_active` exceeds `cc_dispatch.max_goals_active`.
   Warns, does not block. This is L5. `max_goals_active` previously existed
   in exactly one comment in the config and was read by nothing.
3. `extensions/agi/bin/snapshot-build-site.py` `main()` — returns 0
   immediately, before any read/write/prune, when `BUILD_SITE` does not
   exist. This is L18. Two real defects closed, not one: the prior
   `sys.exit(1)` aborted the entire driver under `set -euo pipefail`
   (`driver.sh` pipes this through `tee`), and the alternative of falling
   through with zero parsed tasks would have reached the stale-prune step
   that unlinks every `origin: build-site` node not rewritten this run —
   on this tree that is 159 of 661 nodes (H0i). Returning before any write
   is what makes the fix safe, not just quieter.
4. Tests — 10 new tests added across `tests/test_metrics.py` and
   `tests/test_snapshot_build_site.py`.

**Evidence, my own run, not inherited from any prior node:**

- `cd /home/ubuntu/work/agi && python3 -m pytest extensions/agi/tests/ -q`
  → **482 passed**, 0 failed.
- Metric effect, measured both ways on the live `agi-tree` graph
  (665 nodes, both engine copies pinned at the same base commit
  `1029ea8`; `/home/ubuntu/work/agi-tree/agi` is the clean pre-change clone,
  `/home/ubuntu/work/agi` is the working copy with the uncommitted diff):
  - Before: `outcome_coverage=0.196` (`mvp_count=20`, old `hypothesis_count`
    path).
  - After: `outcome_coverage=0.196` — **unmoved**. Not because the code is a
    no-op: `retired_goal_nodes=0`. Of the 3 goals currently `phasing-out`/
    `complete` (`goal:g6.2`, `goal:s6`, `goal:s2`), only `goal:g6.2` is
    referenced by any node's `parents` at all, and that one reference is
    `goal:g6` (a sibling goal node) pointing at it — goal-type nodes are
    skipped in the scoring walk by construction. So zero `mvp`/`hypothesis`
    nodes anywhere in this graph currently descend from a retired goal. The
    exclusion logic runs (`goals_retired=3`, `retired_goal_nodes=0` confirms
    it evaluated all three and found nothing under them), it just has
    nothing to exclude on this corpus yet.
  - Also observed: `goals_active=36`, `goals_horizon=18`, `goal_count=57`,
    `unattributed_nodes=490` (out of 665 non-goal nodes — most of the corpus,
    consistent with the "predates goal nodes" comment in the code).
  - Rotation warning **fires**: `cc_dispatch.max_goals_active=3` in
    `agi-tree.config.json`, `goals_active=36` → stderr line
    `!! METRIC-WARNING goals_active=36 exceeds cc_dispatch.max_goals_active=3`
    and `METRIC_WARNING goal_rotation=36/3` on stdout. The gap (36 vs 3) is
    itself informative — the config value has been meaningless for long
    enough that "active" drifted to mean "declared," exactly the failure
    mode the code comment names.

**G5 requirements — met / not met** (checked against
`/home/ubuntu/work/agi-tree/nodes/goal/g5-goals-are-a-lifecycle-the-engine.md`,
the canonical statement — `status` here is `horizon`, not `active`, worth
noting since the work proceeded anyway):

| Requirement | Status | Basis |
|---|---|---|
| Stop scoring `phasing-out`/`complete` goals, keep attributable | Met | `goal_attribution()` in `metrics.py`; verified `retired_goal_nodes` computed, currently 0 for lack of retired-goal work on this corpus |
| Fail loudly when a seed points at a nonexistent goal id | **Not met** | The check exists — `snapshot-goals.py` (`INTEGRITY: ... references unknown goal '<ref>'`) — but it predates this diff (G7.1, not G5) and by default only **warns** to stderr. `--strict` (exit 1) is the only path that fails; `extensions/agi/driver.sh` lines 78-80 invoke `snapshot-goals.py` with no flags at all. A bad goal id today logs a line in `$LOG` and the loop continues untouched. Nothing in this diff wires `--strict` into the default run path. |
| L5 — rotation the engine enforces | Met | `goal_rotation` warning in `metrics.py emit()`, confirmed firing at 36/3 above |
| L18 — ideation-only project degrades, doesn't abort | Met | early-return guard in `snapshot-build-site.py main()`, confirmed by the diff and by the 10 new tests |

**What the payload_ref drift means:** ran
`stitch.py --project /home/ubuntu/work/agi-tree --verify --engine-root /home/ubuntu/work/agi`
directly. It reports:

```
[4] stale_contracts: 2 (+ 0 unreadable)
    build:bin-metrics (extensions/agi/bin/metrics.py): drift in outputs
    build:bin-snapshot-build-site (extensions/agi/bin/snapshot-build-site.py): drift in outputs
```

`[1] missing_payload`, `[2] orphan_files`, `[3] duplicate_payload_ref` all
came back 0. So: yes, `--verify` detects this drift, precisely on the two
files this diff touched and on no others — `build:bin-metrics` and
`build:bin-snapshot-build-site` now point at files whose derived
input/output contract no longer matches what is stored in the level-3 node.
`--strict` turns that into exit 1 (confirmed). Nothing in this session ran
`--strict` as part of any automated gate — it was invoked here manually, for
this report. The mechanism that would have caught "engine changed, level-3
node didn't" is real and already exists; it simply hasn't run against this
diff as part of any enforced step, the same way `--strict` on
`snapshot-goals.py` exists but isn't wired into `driver.sh`. Until either the
level-3 nodes for these two files are regenerated or a node records this
change as its origin, `nodes/level3/bin-metrics.md` and
`nodes/level3/bin-snapshot-build-site.md` describe a version of these files
that no longer exists on disk.