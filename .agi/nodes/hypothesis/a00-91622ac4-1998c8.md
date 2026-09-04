---
id: hypothesis:a00-91622ac4-1998c8
mint_id: dfc737ff8778435b8ef5439eff78f46b
type: hypothesis
parents:
  - goal:g5
next_edges: []
scaffold_hash: 180898d89f6b4c07
title: snapshot-goals.py --render does not filter retired goals from GOALS.md
---

# hypothesis:a00-91622ac4-1998c8

## Hypothesis

`snapshot-goals.py --render` includes retired goals in the rendered `GOALS.md` identically to active goals. The render path (`load_goal_nodes()` → `render_goals()`) has no lifecycle status filter — a goal marked `status: retired` or `status: phasing-out` is rendered alongside active, horizon, and complete goals with the same weight. G5 claims "goals are a lifecycle the engine reads" but the render path — which is the most visible output the engine produces — reads lifecycle only for scoring (metrics.py) and metadata (status label in the rendered heading), never for inclusion or exclusion.

**What would prove it**

1. **Static analysis:** `load_goal_nodes()` (snapshot-goals.py, line 773) collects all nodes where `origin == "goals-doc"` and `type == "goal"` with NO check on `status`. Every goal collected is passed to `render_goals()` (line 641), which iterates ALL entries in sorted gid order with no status filter.

2. **Whole-file grep for status-based exclusion:** `grep -n 'status\|retired\|filter\|skip\|omit\|exclude' snapshot-goals.py | grep -i 'render\|goal_node'` returns nothing — confirming there is no lifecycle-aware exclusion at any point in the render pipeline.

3. **Behavioral test:** Create a goal node with `status: retired` and a non-retired goal node. Run `snapshot-goals.py --render`. Both goals appear in the rendered output, their only difference being the `— status: retired` label in the heading — visually indistinguishable from active goals at a glance.

**What would disprove it**

1. Find a status filter in `load_goal_nodes()` — e.g. `if fm.get("status") in {"retired", "phasing-out"}: continue` — that skips retired goals during collection.
2. Find a status filter in `render_goals()` that omits goals based on their `status` field.
3. Find a pre-filter in `cmd_render()` that prunes retired goals from the goals list before rendering.
4. Find an existing test (e.g., in `test_snapshot_goals.py`) that asserts retired goals are excluded from render output.

**Why this matters**

The render output (`GOALS.md`) is the human-facing document at the repo root — it is what every new reader opens first. A retired goal appearing there with the same prominence as an active one:
- Contrasts with `outcome_coverage` in `metrics.py`, which correctly excludes retired goals' chains from the numerator (SCORING_GOAL_STATUSES = {active, horizon, complete})
- Means the engine and the document disagree about which goals matter — the engine knows lifecycle, the document ignores it
- Creates noise for readers: a goal retired because it was "folded into another goal" or "no longer worth pursuing" still occupies a section in GOALS.md

The status label IS shown in the heading (`— status: retired`), but that's documentation, not enforcement — it describes the state without the engine *acting* on it.

## Scope

Scoped to `snapshot-goals.py`'s `--render` path only. `--from-doc` (the legacy parse direction, now tertiary since goal:g6.9 made nodes authoritative) is out of scope. The render path is the canonical direction nodes → GOALS.md and is the only direction used in normal operation. Lifecycle enforcement in other engine paths (metrics, dispatch, spawn gate) is covered by sibling hypotheses a00-b2e49a50-9978aa and a01-fc9a1d05-5ef909.