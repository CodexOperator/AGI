---
id: goal:g7.10
mint_id: e69b4b0c3ba343078354a045bb1c7b26
type: goal
parents:
  - goal:g7
confidence: 1.0
edited_by: season.py
goal_id: G7.10
goal_kind: subgoal
heading_level: 3
origin: goals-doc
season: 1
seeds: []
status: complete
tags:
  - goal
  - subgoal
thought_session: season
title: "G7.10: The publish cron must never fail silently, and a refusal must not strand work"
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
of that build**. Both shipped on 2026-08-28 (below), which is what closes this
goal.

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
Part 4 followed the same day, below.

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

## Part 4 built 2026-08-28 — a refusal that changes nothing

The last part, and the one that makes "it refused" mean what every reader
already assumes it means. Derivation now happens in a throwaway `git worktree`
of the graph; `nodes/` and the grid are written only after gate 2 has passed.
The owner's choice, over rollback: a `git checkout -- nodes/` on the way out is
a second write that has to be correct while something has already gone wrong,
and in a worktree two agents share (**G4.1**) it would discard whatever the
other one wrote in the meantime. Never mutating has no such window.

**A worktree, not a copy.** `stitch.py --verify --from-grid` resolves every
payload out of `refs/grid/node/<mint-id>`, which lives in the graph repo's
object store. A `cp -r` has no `.git`, so `--from-grid` cannot read a single
payload there and the gate would degrade to checking nothing while still
exiting 0. `git worktree add --detach` shares the object store and every ref,
so the scratch tree sees exactly the grid the real repo does — measured: 186 of
186 contracts derived `from the grid, 0 from the engine tree`. It is created
outside both repos for the same reason part 3's is.

**The grid commit moved below the gate, and its old comment was wrong.** It sat
between step 1 and gate 2, explained as "the publish reads the new node versions
back out". It does not. `stitch.py --from-grid` reads only the `payload` tree
entry from each ref (`_grid_payload` → `grid.read_tree_entry(..., PAYLOAD_ENTRY)`)
and reads node bodies off disk, so a node-body rewrite never reaches the
published tree at all. Measured on the live corpus, 186 build nodes and 1061
grid refs: a scratch derivation followed by
`stitch --verify --from-grid --strict` reports `missing_payload: 0,
orphan_files: 0, duplicate_payload_ref: 0, stale_contracts: 0` **with no grid
commit anywhere in front of it**, and both the node tree hash and all 1061 ref
tips are unchanged afterwards.

**The real dependency is narrower, and it is `missing_payload`.** A file
authored under `payloads/` and not yet published is in neither the engine tree
nor the grid, so the node `level3.py` mints for it reads as `missing_payload` —
drift by `stitch.py`'s own definition, which `--strict` turns into a refusal.
Confirmed by construction: adding one `newthing.py` to `payloads/` took the same
scratch verify from `[1] missing_payload: 0` to
`[1] missing_payload: 1  build:bin-newthing -> extensions/agi/bin/newthing.py`.
Holding that node in the scratch would strand it forever — it would never reach
`nodes/`, so the ungated `*/5` grid cron would never see it, so its payload
would never enter the grid, so the gate would refuse again next hour. That is
**G6.1**'s deadlock with a new door. So a *newly minted* node, and only a newly
minted one (`git ls-files --others --exclude-standard -- nodes/` in the scratch),
is copied across and grid-committed before the gate is retried. A new node is
not junk: it is the correct, idempotent outcome of a real new file, its mint id
is stable once on disk, and any ordinary scan mints it too. Rewritten bodies —
which is what the 184 junk nodes were — are never treated this way.

**Cleanup composes, it does not replace.** One `trap on_exit_cleanup EXIT`
registered beside the existing `trap on_unexpected_error ERR`, calling
`_scratch_cleanup` and then part 3's `_fb_cleanup`; both are no-ops when their
state variables are empty, so the ordinary path pays nothing and every abnormal
path is covered exactly once. Part 3's fallback code is byte-identical — its
tmp-root selection is deliberately **duplicated rather than factored out**,
because it landed 40 minutes earlier under its own tests and refactoring a
working safety mechanism to save five lines is not a trade this file should
make. Bash restores `$?` across an EXIT trap (verified), so cleaning up cannot
change the exit code the caller sees. The graph repo gets its own
`git worktree prune`; part 3's prunes the engine, and neither substitutes for
the other.

**Two cleanup defects found by killing runs, not by reading.** First: a signal
reaches the shell but not the `python3` child, and bash runs the EXIT trap
immediately — so `level3.py` re-created `nodes/build/` a tenth of a second after
`rm -rf`, leaving a temp dir behind on every killed run. Fixed with a
`pkill -TERM -P $$` and a bounded retry loop; three SIGTERMs at 1 s, 2 s and 3 s
now leave `worktrees=1 tmpdirs=0 nodes-dirty=0` every time. Second: `SIGKILL`
runs no trap at all, and `git worktree prune` will not reclaim a worktree whose
directory still exists — so a startup sweep removes `agi-publish-derive.*` trees
older than **six hours**, bounded by age rather than by name alone because a run
takes ~25 s and the cron is hourly, so nothing live can be six hours old.
`SIGKILL` still orphans the python child; that is unfixable from here and is
named rather than papered over.

**Falsifier, run for real**, against `git clone --local` copies of both repos
with the real 1061 grid refs fetched — real script, real 191-node corpus. A
`build:ghost` node claiming a payload that exists nowhere forces
`contracts-disagree` with the graph committed and clean:

```
[publish-engine] verifying the scratch tree against its own payloads
  [1] missing_payload: 1
      build:ghost -> extensions/agi/bin/ghost.py (does not exist)
[publish-engine] REFUSING [contracts-disagree]: ... nothing published, and nothing
  written — nodes/ and the grid are exactly as this run found them
exit code: 1
```

| check | result |
|---|---|
| exits non-zero | `1` |
| `nodes/` byte-identical | sha256 over the whole tree, `bd96b636… -> bd96b636…` |
| no new grid versions | all 1061 ref tips identical, `git status` 0 lines |
| marker records the refusal | `last_run_status=refused`, `last_run_reason=contracts-disagree` |
| `last_success_*` untouched | `1000` / `deadbee`, unchanged |
| no worktree, temp dir or branch survives | `worktrees=1`, `tmpdirs=0`, `cron/*=0`, engine clean |

**Head-to-head, same refusal, identical pair.** Six payload contracts were moved
and recorded by a simulated `*/5` grid cron, so the derivation genuinely had
something to write, and both scripts were run on byte-identical clones:

```
OLD (part 3):  JUNK NODES LEFT IN nodes/: 6    GRID VERSIONS BURNED: 6
NEW (part 4):  JUNK NODES LEFT IN nodes/: 0    GRID VERSIONS BURNED: 0
```

Six rather than 184 only because six contracts were moved; the shape is the one
the rename produced. **Part 3 still parks**, on the same clones:
`fallback: 1 file(s) parked on cron/pending-e710968ee @ 336fc94 (local only, not
pushed)`, fast-forwardable from `master`, carrying the graph's bytes and not the
engine's stale ones, with `last_fallback_status=parked` and the alarm still
climbing. The happy path published and committed normally
(`applied the scratch tree: 0 added, 2 rewritten, 0 pruned` →
`committed 2 file(s) ... (graph @ 38450ee3e)`, marker `ok`), a file authored
under `payloads/` was minted, adopted, grid-committed, verified and shipped into
the engine in one run, and `--dry-run` left the node tree, all 1061 refs, the
marker and the engine untouched. Both clones deleted; the real engine is back to
4 worktrees and 0 `cron/*` branches, the real graph to 2 worktrees, both clean.

**Two things named rather than fixed.** (1) `grid.py commit` takes no
`--engine-root`, so `publish-engine.sh --engine-root X` does not reach it and it
resolves payloads against *its own location on disk*. In production
`<project>/payloads/` always exists and wins first, so this never fires — but
where it does, the node is committed with **the payload entry dropped**, and the
next publish then materialises nothing for it. It is a latent data-shaped hazard
in `grid.py`, not in this file, and it is what made the first success-path test
fail. (2) Gate 2 now certifies the tree **as derived**, not as published: if
`payloads/` is edited in the window between the scratch derivation and
`grid.py commit --all`, the publish ships bytes one derivation ahead of the
contract describing them. That is strictly better than the behaviour it
replaces — the old order turned the same race into a refusal *plus* the junk
nodes — the drift is a stale mechanical `how` block rather than wrong code, and
the next `:37` re-derives and converges it.

Tests: 826 → **837 passed, 1 skipped**. 11 new, no existing test changed;
`_pair` gained an opt-in `staged=` that lays down `<project>/payloads/` the way
every real project has it, because the success path is the first thing here that
ever needed it.

<!-- THOUGHT:BEGIN — authored, not derived; carried across regenerating scans. The reasoning behind THIS version. -->
Part 3's reasoning — why gate 2 gets no fallback, why parking had to feel like a
refusal, and the `/dev/null` finding — is one grid version back, at the part 3
commit. It still holds and is not restated.

This version adds part 4, and the decision that took the longest was **what the
grid commit was actually for**. The comment above it claimed the publish reads
node bodies back out of the grid, which sounds right and is false: `stitch.py
--from-grid` reads the `payload` entry and nothing else. I moved it below the
gate only after reading both call paths and then measuring — 186 nodes, 1061
refs, zero drift with no grid commit in front. Had I trusted the comment I would
have either left the commit where it was and shipped nothing, or moved it while
believing something untrue about why that was safe.

The second judgement is the **one exception I allowed through the gate**, and I
want it on the record as a choice rather than an oversight. A node minted this
run for a file that exists only in `payloads/` is adopted before gate 2 is
retried, so a refusal on that path is not a perfect no-op — it leaves one node
file and one v1 grid ref. The alternative was a clean rule and a permanent
deadlock: hold the node back, and its payload can never enter the grid, so the
gate refuses forever. G6.1 paid for that door once. The exception is bounded to
untracked-in-the-scratch node files, it is announced in the log and in
`last_run_detail`, and a test pins that it is the *whole* of what a refusal may
leave.

The third is a trade I made knowingly and would defend, but it is a trade.
Moving the grid commit below the gate means gate 2 certifies the tree as
derived, not as published, so a `payloads/` edit landing mid-run ships bytes one
derivation ahead of their contract. The old order caught that race — by turning
it into a refusal that left the junk nodes behind. Swapping a self-correcting
metadata lag for the failure this goal is named after is the right direction,
and if a later iteration disagrees the fix is one more verify before step 4, not
a return to mutating first.

What I did not do: touch `stitch.py`, whose `--from-grid` "nothing falls back to
disk" rule would have made the new-file case disappear if `payloads/` counted as
somewhere the graph holds bytes. That is a real argument — it is G6.1's own
argument one step further — but it widens what `--from-grid` means for every
caller, and it was not mine to decide inside a change to one shell script.
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