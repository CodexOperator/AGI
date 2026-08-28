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

## Parts 1 and 2 built 2026-08-27 — the failure now moves a number

Scoped to the alarm and the marker; **parts 3 and 4 are deliberately not
built** and are what keeps this goal `active`.

**The alarm.** `metrics.py` emits four new lines, verified live against the
real graph:

```
METRIC hours_since_successful_publish=99999.0
METRIC publish_blocked_reason=never-run
METRIC deprecated_node_count=5
METRIC active_node_count=784
```

`hours_since_successful_publish` uses a sentinel rather than `0` when nothing
has ever published, because higher is worse for this metric and `0` would read
as "just published" — the precise inversion this goal exists to stop. The cron
refused 40 times and published nothing; a metric that reported that as healthy
would have been worse than no metric. `publish_blocked_reason` is normalised to
a single token, since `METRIC k=v` is a whitespace-delimited line format and a
reason containing a space would truncate or corrupt the line.

**The marker.** `<project>/context/publish-state.json`, atomic write-then-rename,
gitignored beside `context/INJECTION.md` — machine state about one checkout, not
graph content. **It is deliberately not under `nodes/`:** gate 0 refuses on any
uncommitted change there, so a marker written into the graph would arm, on every
run, the exact gate it exists to report on. It carries `last_success_*` forward
across refusals, so a two-day outage stays distinguishable from a fresh install.

**The reach.** `publish-engine.sh` now exits non-zero on refusal (gate 2 and the
unexpected-failure path joined gate 0, which already did), and
`hooks/cc-session-start.sh` surfaces a stalled publish to the next agent to open
any session. The hook's **silent no-op outside a project is preserved and was
re-measured at 0 bytes** — that property is what makes global registration safe,
and an alarm is not worth breaking it for.

The failure message states the reassuring true thing, because the reasonable
fear when a publish stalls is that work is evaporating and it is wrong:
**payload bytes are never lost.** `grid.py commit --all` runs on its own ungated
5-minute cadence; only the engine publish is blocked.

**Also shipped here, from outside this goal's text:** `deprecated_node_count`
and `active_node_count`, node-level lifecycle counts kept strictly separate from
`retired_goal_nodes` (which answers a different question — goal attribution, not
node status). They exist because **G2.10** retired five nodes in place rather
than deleting them, which by design leaves `node_count` flat; without a second
number the retirement would itself have been a silent event.

Tests: 755 → **792 passed, 1 skipped**. 37 new, no existing test needed
changing.

<!-- THOUGHT:BEGIN — authored, not derived; carried across regenerating scans. The reasoning behind THIS version. -->
This version is the first half of the build, and the one judgement worth
recording is where the alarm was deliberately made *quieter* than first written.

The original warning said `the engine publish is STALLED` for every non-empty
blocked reason, including `never-run`. That is wrong in a way this goal should
have anticipated: a project that has simply never installed the publish cron is
not stalled, and a fresh clone would have greeted its first session with a
red-flagged outage that did not exist. The kid that built it caught this in its
own verification and reported it rather than smoothing it over; the fix was
three lines and is applied.

Worth keeping because it is this goal's own thesis turned one level up. The
premise here is that a failure nobody can see gets ignored — 40 refusals, zero
notice. The symmetric failure is an alarm that fires when nothing is wrong,
which gets ignored just as completely and takes the true positives with it. An
alarm's credibility is the asset; overstating `never-run` spends it for nothing.

The same instinct decided the marker's location. Putting it under `nodes/` would
have been the obvious place for graph-adjacent state and would have armed gate 0
on every single run — an alarm whose own operation triggers the condition it
reports. Gitignored beside `INJECTION.md` instead: this is machine state about
one checkout, and it does not survive a clone because it should not.

Parts 3 and 4 are untouched on purpose. Branch-and-continue changes where bytes
land and atomicity changes what a refusal leaves behind; both are behaviour
changes to the publish path, and neither should ride in on the commit whose job
was to make the existing behaviour visible. Visibility first — it is also what
will show whether the remaining two are working.
<!-- THOUGHT:END -->

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
