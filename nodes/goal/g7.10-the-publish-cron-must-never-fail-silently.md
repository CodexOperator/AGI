---
confidence: 1.0
goal_id: G7.10
goal_kind: subgoal
heading_level: 3
id: "goal:g7.10"
mint_id: e69b4b0c3ba343078354a045bb1c7b26
order: 50
origin: goals-doc
parents:
  - goal:g7
seeds: []
status: active
tags:
  - goal
  - subgoal
title: "G7.10: The publish cron must never fail silently, and a refusal must not strand work"
type: goal
---

🔴 **The hourly publish cron can refuse, every hour, forever, and emit no
signal anywhere a human or an agent will look.** It has already done exactly
that: **40 consecutive refusals with 0 successful publishes ever**, from
installation on 2026-08-25 until it was noticed by hand on 2026-08-27.

This is **G7**'s own commitment — nothing the loop produces is silently lost —
violated by the loop's own automation. It is the highest-severity shape the
goal has, because the thing being lost is *every engine change the graph
makes*, and the loop keeps reporting success while it happens.

## Why it is not a one-off

Gate 1 of `publish-engine.sh` refuses when the graph has any uncommitted change
under `nodes/` or `GOALS.md`. That gate is **correct** — a published engine
must cite a graph commit that exists. The defect is everything around it:

- **The refusal goes to a log nobody reads.** `driver.sh --smoke` does not
  report it. `INJECTION.md` does not carry it. No metric moves. The only way to
  learn about it is to run `level3.py` and read `git status` on a hunch.
- **Any single self-inflicted dirty node arms it permanently.** One character
  of YAML quoting did it for weeks (**G6.5**). Then **S19** made it
  *intermittent* instead of permanent — a contract that re-derives differently
  under 3.11 and 3.12, so the gate passes or fails depending on which
  interpreter ran last. Intermittent is worse: it looks healthy half the time,
  which is precisely when nobody investigates.
- **A refusal is not a no-op.** `publish-engine.sh` mutates the graph at step 1
  (re-deriving contracts) before refusing at step 3. A refused run left **184
  junk nodes** behind during the last rename. So "it refused" does not mean
  "nothing happened", which is the assumption every reader makes.

## What this asks for, in the order it should be built

1. **An alarm that moves a number.** The project has proved this idiom works
   exactly once already: `shadow_decisive_verdicts` went 0 -> 1 and caught a
   defect that would otherwise have shipped. Emit
   `hours_since_successful_publish` (and `publish_blocked_reason`) from
   `metrics.py`, so a stalled cron shows up in every `--smoke` run and in the
   injected map. **A failure that does not move a metric is a failure this
   project cannot see.**
2. **A non-zero exit and a durable marker.** The cron should leave a
   machine-readable marker the `SessionStart` hook surfaces, so the *next
   agent to open a session anywhere* is told, rather than the information
   waiting in a log for someone to guess.
3. **A fallback that keeps working instead of stopping.** The bytes must land
   somewhere even when the main path is blocked. Two candidates, and they are
   not exclusive:
   - **Branch and continue.** Publish to `cron/pending-<graph-sha>` in the
     engine rather than to the default branch. Work is never stranded, the
     default branch is never published from a graph commit that does not exist,
     and a human fast-forwards when the block clears. This is the option that
     preserves both invariants at once and is the recommended default.
   - **Force-record.** Note that `grid.py commit --all` runs on its own 5-minute
     cadence and is *not* gated, so **payload bytes are already never lost** —
     what stalls is only the engine publish. Say so explicitly in the failure
     message, because the reasonable fear when a publish stalls is that work is
     evaporating, and it is not.
4. **Make the refusal atomic.** Either step 1 does not mutate, or a refusal
   rolls back what it wrote. Today it does neither, and the 184 junk nodes are
   the proof.

## The design principle underneath

**A gate that blocks is fine. A gate that blocks quietly is not.** The engine's
whole design ethic is that mundane operations, and the small errors they breed,
are the system's job to absorb and never the agent's — an agent should never
have to *suspect* that automation stopped working. Silence converts a healthy
refusal into an invisible outage, and invisible outages are what this project
is least able to afford while it is this experimental.

Pairs with **G6.5** (which owns the cron itself), **S19** (the live cause of
the current flap), **S7** (a different silent-edge defect found the same day),
and **G1** (every mundane step is a command, not a thing to remember).

Falsifier: dirty the graph deliberately with one node, wait for the `:37` cron,
and open a fresh Claude Code session in any directory. If nothing in that
session's injected context mentions that the engine is unpublished, this goal
is not met.
