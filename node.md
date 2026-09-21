---
id: goal:g6.5
mint_id: 1144ba54807845f2b7dfa655e7f47571
type: goal
parents:
  - goal:g6
confidence: 1.0
edited_by: season.py
goal_id: G6.5
goal_kind: subgoal
heading_level: 3
origin: goals-doc
season: 1
seeds: []
status: retired
tags:
  - goal
  - subgoal
thought_session: season
title: "G6.5: The cron rebuilds agi from agi-tree, then commits and pushes it"
---
**The shape being committed to: `agi-tree` is the development environment,
`agi` is the shippable package.** Work happens in the graph; the engine repo is
what falls out of it. When the grid cron runs it should re-derive the census,
re-scan level 3, `stitch` the result into the engine tree, and — once that is
trustworthy — **commit and push the engine repo too**, so `agi` is always a
published build of `agi-tree` rather than a thing edited in parallel.

**Answering the question directly: today the two repos' commits are NOT the
same work, and that is the defect.** This session's engine changes were edited
directly in `agi`, and the level-3 nodes merely *describe* the result through
`payload_ref`. The graph trails the code. G6.3 reverses the arrow (a fix lands
as a build-node version), G6.4 gives it provenance (a non-build chain produces
the next version), and only then is an automatic rebuild-and-push safe — at
that point the engine commit is a *derivation*, and its message can cite the
node and verdict that caused it.

**Sequencing, and it is not negotiable:**
1. **Now — verify only.** Cron runs the generators and `stitch --verify`, and
   reports drift. It writes nothing to the engine.
2. **After G6.3** — cron may stitch and commit the engine.
3. **After G6.4** — the engine commit message carries the node → verdict →
   version chain that produced it.

A cron that writes the engine from the graph before the version layer is
trusted is a data-loss defect waiting to happen, and this project has already
paid for that class twice (H0, H0b). Report drift; never silently reconcile it.

**Step 2 is unblocked as of 2026-08-25 and the writer exists, un-croned on
purpose.** G6.3 is complete, so `stitch.py --out <engine> --from-grid
--publish` is now a legitimate operation and has been run twice on real
changes. It is gated on three things at once, because this project has paid
three times for a script that wrote a tree it had no independent record of:
`--publish` explicitly (never a side effect of `--force`), `--from-grid`
(publishing the engine from itself cannot add information), and **a clean
engine working tree** — which is the gate that makes the write *recoverable*
rather than merely intended, since every overwritten byte is then already in
the engine's own history and `git checkout .` undoes the entire publish.

What is deliberately **not** done: putting it in the cron. Step 2 says cron
*may* stitch and commit; it does not say it should do so the same day the
mechanism first ran. The honest sequence is to publish by hand until the
reverse direction closes (**G6.1**'s residual — `--verify` still reads the
engine tree, so an unattended cron could publish a payload whose contract had
never been re-derived), then automate.

**The generality worth preserving:** `agi` already has the tooling to run
against *any* project, including itself. Pointing it at itself is what makes
this loop closed; pointing it at fantasia is what makes it a product. Neither
should require a different engine — see **G8.2**.

Pairs with **S2** (done) and **S5** (the engine repo has no sync at all yet).

**Step 2 landed 2026-08-25: `bin/publish-engine.sh`.** Four steps, every one a
gate rather than a stage — re-derive contracts from the grid, `grid commit`
them, `stitch --verify --from-grid --strict`, then publish and commit the
engine citing the graph commit that produced it.

It refuses more often than it acts, and each refusal has a named reason:
- the graph has uncommitted changes under `nodes/` or `GOALS.md` (the engine
  commit message would cite a graph state that exists nowhere)
- the graph disagrees with its own contracts (publishing that would put drift
  into the engine atomically and cleanly, which is **G6.7**'s argument about an
  atomic publisher of corrupt content arriving here first)
- the engine working tree is dirty (`stitch --publish`'s own gate — it is what
  makes every overwritten byte recoverable with `git checkout .`)

**It does not push.** The existing hourly cron already owns remote traffic;
this only commits, so a bad publish never leaves the machine.

The publish cadence is now declared as graph content rather than installed by
a subcommand: `nodes/.geometry/crons.md` (**G10.2**) lists `publish_engine`
under `cadences` at `:37`, after the :07 branch push, so a publish never races
the push of the graph commit it cites. `bin/crons.py apply` renders that
declaration into the real crontab's managed block; the old
`grid.py cron install --publish-engine`, which added the line directly and
defaulted it off, is retired in practice on this project.

**Enabled on this project's declaration as of 2026-08-29**
(`publish_engine: {schedule: "37 * * * *", enabled: true}`), which is the
first time the sequence above has been allowed to complete. `crons.py apply`
renders it as:

```
37 * * * * cd <tree> && bash <engine>/extensions/agi/bin/publish-engine.sh
```

inside the managed `agi-crons` block. Editing `enabled` on `publish_engine` in
the node and letting the graph get committed reaches the real crontab within
5 minutes, via the `grid_sync` job re-running `crons.py apply` on every tick.
`--dry-run` passed every gate before it went live. What that buys, concretely:
`agi` stops being a repo anyone edits and becomes a published build of
`agi-tree`, hourly, with each commit naming the graph commit it derives from.
What it deliberately does not buy: a push. If an hour's publish is wrong it is
wrong on one machine, and `git reset` is the whole remedy.

This goal stays `active` for step 3 — the engine commit message should carry
the node -> verdict -> version chain that produced it (**G6.4**), not just the
graph commit sha. Today it cites `published from the graph @ <sha>`, which is
attribution without argument.

## The cron was refusing silently, every hour — found 2026-08-27

Gate 1 ("the graph has uncommitted changes under `nodes/` or `GOALS.md`") is
the right gate and it was doing its job. What it was refusing on is the
problem: **one node held a contract value that `level3.py` does not emit.**

`nodes/level3/tests-schema-registry-test-brackets.md` stored a `how:` field
quoted `f''---\n...''` where the derivation produces `f"---\n..."` — which is
what the source actually says. So every scan re-derived the correct value,
left the file modified, and the graph was never clean at `:37`. The cron
refused, correctly, for a reason no one was reading.

**The failure mode is worth naming because the gate cannot distinguish it.**
"The graph has uncommitted work" and "the graph has a node that can never be
clean" produce identical output and opposite required actions. The first says
*commit and retry*; the second says *nothing you commit will help until the
derivation and the stored value agree*. A cron that refuses every hour for
weeks looks exactly like a cron that has nothing to do.

Two consequences already acted on:

- Fixed the value; two consecutive `level3.py` runs now leave the graph clean,
  and `publish-engine.sh` published and committed on the next attempt
  (`agi @ 0ebd5fa`, "published from the graph @ 3b580e5cc").
- `CLAUDE.md` documented `stitch.py --publish` as the final step of an engine
  edit. That is the layer *underneath* this script: it writes the bytes and
  never commits, so following the documented path leaves the engine dirty and
  the next publish refuses. Rewritten to point here, with the failure and its
  recovery recorded.

What this goal should still grow: **a refusal that distinguishes the two
cases.** Gate 1 could re-run the derivation and say "the graph is dirty *and*
re-deriving does not clean it — node X disagrees with its own contract",
which is a different sentence demanding different work. Pairs with **G7.9**
(a scan must not be quiet about what it changes) and **G7.5**.

<!-- THOUGHT:BEGIN — authored, not derived; carried across regenerating scans. The reasoning behind THIS version. -->
Marked `phasing-out` in the 2026-09-01 sweep rather than complete, because it
was never done — it was made meaningless.

The goal describes a cron that rebuilds `agi` from `agi-tree`, commits and
pushes it. `goal:g11` deleted the boundary that job existed to cross: there is
no second repo to rebuild from, `publish-engine.sh` has nothing to run, and
`engine_push` duplicates `branch_push` against the same remote. Both are
expected to stay disabled rather than be deleted from the cron schema.

Retired by marking, not by deleting, and the seed nodes stay as prior art —
this chain is the record of what the two-repo era cost.
<!-- THOUGHT:END -->