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

Scoped to the alarm and the marker; parts 3 and 4 were **deliberately left out
of that build**. Part 3 shipped on 2026-08-28 (below); **part 4 remains open and
is what keeps this goal `active`.**

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

## Part 3 built 2026-08-28 — a refusal that keeps working

Branch-and-continue, the option this goal named as the recommended default.
The force-record half was already shipped with parts 1–2 (`say_bytes_are_safe()`).
**Part 4 is still open and this goal stays `active`.**

**What it does.** When `publish-engine.sh` refuses for a reason that is about
*attribution* rather than *content*, it materialises the same tree it would have
published and commits it to `cron/pending-<graph-sha>` in the engine. **Local
only — it is never pushed**, and no `--push-fallback` flag exists. The header's
standing invariant, "push. Pushing is the existing hourly cron's job; this only
commits", is unchanged. The alarm is what tells a human to look; the branch is
what is there when they do.

**A detached worktree, not a branch switch.** `git checkout -b` in the engine's
own checkout, write, commit, switch back is racy against every other reader of
that tree, and this project has already lost work to that exact shape — commits
piled up on an `iter24-extend-300hop` branch while a cron pushed `master` and
published nothing. Instead: `git worktree add --detach` into a temporary
directory **outside both repos**, stitch into it, commit there, move the branch
ref, remove the worktree. Outside both repos is load-bearing — `stitch.py`
refuses to write into the graph repo at all, and treats any path inside the
engine repo as a `--publish`, which would gate parking on the engine's own
working tree being clean, a condition a private worktree has no business
needing. The engine's HEAD, branch and cleanliness are **asserted** unchanged
afterwards, not assumed; a mismatch is recorded as `parked-but-engine-moved`.

**Idempotency is a diff, not a clock.** This is the `:37` cron: a graph dirty
for three days is 72 runs, and 72 commits of identical bytes is manufactured
junk of the same kind as the 184 junk nodes a refused run once left behind. The
worktree is based on the pending branch's own tip when that tip already contains
the engine's HEAD, and a commit happens **only if `git status --porcelain` in the
worktree is non-empty**. A tip that no longer contains HEAD is stale and is
rebuilt from HEAD rather than extended, because otherwise the `merge --ff-only`
the commit message documents would silently stop working. The branch name is
keyed on the graph sha, which does not move while the graph is dirty — but the
grid does (an ungated 5-minute cron), so content genuinely changes between runs
and must still be parked; a test pins both directions.

**Gate 2 gets no fallback, and not as a special case.** The rule is *the fallback
never parks bytes that have not passed the same verification the real publish
requires*. Gate 2 has not run when gate 0 refuses, so the fallback runs
`stitch --verify --from-grid --strict` itself — read-only, no `level3.py`, no
grid commit, **nothing written into the graph repo at all**. A
`contracts-disagree` refusal is therefore ineligible by construction: its
precondition is precisely what failed. The eligibility list is written out
explicitly anyway (`graph-dirty` only; `unexpected-failure` excluded because
after an unknown failure nothing knows what state it is in), so the reasoning is
auditable, but verify-first would hold even if that list were widened by
mistake. The justification is the goal's own: a pending branch is one
`git merge --ff-only` from the default branch, so parking unverified bytes there
moves drift one command away instead of stopping it.

**The marker gained five keys, all additive:** `last_fallback_epoch`,
`last_fallback_status`, `last_fallback_branch`, `last_fallback_commit`,
`last_fallback_detail`. `schema` stays `1` — every existing reader keys on
presence, so bumping it would signal a break that did not happen. **Nothing
touches `last_success_epoch` or `last_success_graph_commit`, and
`last_run_status` stays `refused`.** A parked run is still a refusal:
`hours_since_successful_publish` keeps climbing and `publish_blocked_reason`
stays set. An alarm that goes quiet because the safety net caught something is
the exact mirror of the alarm that never fired, and parts 1–2 paid for that
lesson from the other direction when `never-run` was kept out of `STALLED`.

**Falsifier, run for real.** Both repos were already shared with other agents and
the graph was carrying 55 nodes of unrelated 3.11/3.12 quoting churn, so the run
was done against `git clone --local` copies of both repos with the real grid refs
fetched — real script, real 191-node corpus, real bytes. The engine was moved one
file behind the grid, one node was dirtied, and
`publish-engine.sh --engine-root <clone>` was run twice:

```
[publish-engine] REFUSING [graph-dirty]: the graph has uncommitted changes ...
[publish-engine]   fallback: checking the graph against its own contracts before parking anything
[publish-engine]   fallback: 3 file(s) parked on cron/pending-c1bd6e1ae @ ea2fff0 (local only, not pushed)
EXIT=1
```

All six checks pass:

| check | result |
|---|---|
| exits non-zero | `EXIT=1` |
| `cron/pending-<sha>` exists with the published bytes | `ea2fff0`, 3 files changed, 702 insertions; the engine-only line is on `master` and absent from the branch |
| `master` unchanged | `80fbb2f -> 80fbb2f` |
| engine checkout on its branch, at its commit, clean | `branch=master head=80fbb2f dirty='' worktrees=1 (was 1)` |
| marker still a refusal, `last_success_*` untouched | `last_run_status=refused`, `last_run_reason=graph-dirty`, `last_success_epoch=1000`, `last_success_graph_commit=deadbee`, `last_fallback_status=parked` |
| second run adds no second commit | `already carries exactly these bytes; no second commit` — commits `1 -> 1`, tip unchanged |

The documented `git merge --ff-only cron/pending-c1bd6e1ae` was checked to be
actually possible, and no remote pending branch exists. Two more real runs on
the same clones: the happy path published and committed the engine normally
(`published from the graph @ 5873b0240`, marker `ok`), and a deliberately
constructed gate-2 refusal produced
`fallback: not attempted — [contracts-disagree] is not a block the fallback may
route around`, with zero branches cut. Both clones were deleted; the real graph
and engine were verified byte-identical before and after, including worktree
count and branch list.

**The commit message does not launder the provenance gap.** Under a
`graph-dirty` refusal the bytes come from the grid, which runs ahead of the
graph's git HEAD, so the parked tree is attributable to no graph commit at all —
which is the whole reason the default branch refused. The message says
`READ THE BRANCH NAME AS AN ANCHOR, NOT AS PROVENANCE`, names the sha as "the
nearest COMMITTED state of the graph, not a description of what is in this
commit", and gives both landing paths: clear the block and let `:37` republish
with real provenance (`branch -D`), or take this commit knowingly
(`merge --ff-only`).

**One defect found and fixed mid-build.** The first implementation sent the
fallback's verify output to `/dev/null`. A run then declined `verify-failed`
while the ungated `*/5` grid cron was mid-flight, and there was no way afterwards
to tell real drift from a lost race — a decline whose evidence is gone, which is
the failure mode this goal is named after, reproduced inside its own fix. The
fallback now keeps that output, prints a bounded 12-line tail on failure, and
distinguishes `verify-crashed` (a `Traceback` in the log — the check never
finished, which is *not* evidence of drift) from `verify-failed`. The very next
falsifier run declined for a real reason and named the single drifting node in
one line.

Tests: 811 → **826 passed, 1 skipped**. 15 new, no existing test needed
changing. One new test failed on first run and the *fixture* was wrong, not the
code — it moved the engine's default branch by adding an unclaimed file, which
is orphan drift, so verify-first correctly declined and the test would have
passed for the wrong reason.

<!-- THOUGHT:BEGIN — authored, not derived; carried across regenerating scans. The reasoning behind THIS version. -->
The previous version's reasoning — why `never-run` was kept out of `STALLED`,
and why the marker is gitignored beside `INJECTION.md` rather than under
`nodes/` — is one grid version back, at the parts 1–2 commit. It still holds; it
is not restated here.

This version adds part 3, and the decision that took the longest was **gate 2**.
The brief left it open. The tempting answer is that a pending branch is a safe
place to put anything, because a human has to act before it reaches the default
branch. That is wrong by one command: `merge --ff-only` is the landing
instruction *written in the commit message*, and a human following documented
instructions is not an independent check. So the fallback is held to exactly the
gate the real publish is held to, and `contracts-disagree` becomes ineligible
without needing its own rule — its precondition is what failed. Deriving the
exclusion instead of listing it means a future widening of the eligibility list
cannot quietly undo it.

The second judgement is that **parking had to be made to feel like a refusal**,
not like a success with an unusual destination. Everything visible points the
same way — non-zero exit, `refused` status, frozen `last_success_*`, a climbing
clock — because the failure this goal exists to prevent has a mirror image, and
the mirror is easier to build by accident. A safety net that stops the alarm is
worse than no net: the work survives and nobody ever comes back for it.

The third thing is not a decision but a finding, and it is why the build took an
extra pass. The first version sent the fallback's verify output to `/dev/null`,
and a run then declined `verify-failed` during a collision with the ungated
`*/5` grid cron. There was no way afterwards to tell a real disagreement from a
lost race. That is this goal's own thesis — a failure whose evidence is gone —
reproduced inside the fix for it, at a smaller scale, by me. It is recorded
rather than quietly patched because the reflex that caused it (suppress the
noisy subprocess so the cron log stays tidy) is the same reflex that produced
the 40 silent refusals, and it will be back.

Deliberately not done: no push, no `--push-fallback`, and no touch of
`metrics.py` or the SessionStart hook. Parts 4 and 5 own those, and teaching the
alarm to *read* the new fallback keys is their call, not this one's — the keys
are additive and every existing reader ignores them, which is the property that
lets those iterations land independently.
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
