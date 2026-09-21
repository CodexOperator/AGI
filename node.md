---
id: goal:g11
mint_id: 5fb040638ce5429e9240a07b47fb5195
type: goal
parents: []
confidence: 1.0
edited_by: season.py
goal_id: G11
goal_kind: long-term
heading_level: 2
origin: goals-doc
season: 1
seeds:
  - goal:g11.1
status: complete
tags:
  - goal
  - root
thought_session: season
title: "G11: One repo: the graph lives inside what it builds"
---
<!-- THOUGHT:BEGIN — authored, not derived; carried across regenerating scans. The reasoning behind THIS version. -->
Marked complete in the 2026-09-01 sweep. The repo IS one repo: source,
`.agi/` graph and `refs/grid/*` in a single tree, `payloads/` gone,
`grid.py checkout` retired, `agi-tree` archived and read-only. The goal has
been done since 2026-08-29 and stayed `active` only because nothing swept.

Kept as evidence rather than restated: the migration was rehearsed four times
at 807 nodes in / 807 out, zero bytes changed, before the real cut ran.
<!-- THOUGHT:END -->

**The two-repo split is the tax every other goal pays.** `agi-tree` holds the
thoughts, `agi` holds the code, and because the bytes live in one and must
arrive in the other, a whole pipeline exists to carry them: `payloads/` as a
staged checkout, `grid.py checkout`, `stitch.py --publish`, and
`publish-engine.sh` with four gates in front of it. None of that machinery
computes anything. **It is entirely the cost of the boundary**, and the
boundary was never load-bearing — it was inherited.

This goal removes the boundary. One repo holds the source, the graph, and the
grid refs. A `payload_ref` becomes a path to a tracked file in the same
worktree; a single `git commit` carries the thought and the code it produced
together.

## The layout

```
agi/                        ONE repo
  GOALS.md                  rendered here, at the root, visible
  extensions/ skills/ src/  the live source
  .agi/
    config.json
    nodes/  context/
    nodes/.geometry/
  refs/grid/*               same repo, unchanged namespace

fantasia/                   drop in the engine, run init, same shape
  GOALS.md   <game source>
  .agi/                     fantasia's graph        (committed)
  agi/                      engine clone            (gitignored, one line)
    GOALS.md .agi/          the engine's own graph, live in place
```

**`.agi` is a dot directory on purpose.** It files the graph with `.git`,
`.github` and `.claude` — the tooling a repo carries but does not itself run —
rather than in the middle of the source tree. The install story becomes: drop
`agi` into any project, run init, and it creates `<repo>/.agi` beside the
source. **`GOALS.md` is the deliberate exception and renders to the repo root**,
because the one document a human opens first must not be hidden in a dot
directory.

## Two graphs in one checkout, and neither needs a flag

A project that has the engine cloned into it holds two graphs: `repo/.agi` and
`repo/agi/.agi`. Which one you get is decided by where you are standing —
**nearest enclosing `.agi/` wins.** Run from `fantasia/` and you are working on
fantasia; run from `fantasia/agi/` and you are working on the engine. That is
what lets the engine improve itself from inside a project that is using it,
which is the recursion **G8** wants, arriving as a consequence of the layout
rather than as a feature.

It also keeps **G8.2**'s invariant intact: the engine still never knows which
project it is running, because the answer is a property of the filesystem
rather than of a name.

## What this closes, narrows, or deletes

| Goal | Effect |
|---|---|
| **G6.1**'s residual | Deleted. Contract derivation reads the source tree; under one repo the payload *is* the source, so there is no stale window to close. |
| **G6.5** step 3 | Free. The engine commit carries the node chain because it *is* the same commit. |
| **G6.7** | Narrowed to nothing. An atomic publisher of a written tree has no tree to write. |
| **S5** | Closed. One repo has one sync. |
| **G8.1** | Decided in favour of shape 1, with the tree inside the project rather than beside it. |
| **G4.1** | Fixable for the first time — see below. |
| `payloads/`, `stitch --publish`, `publish-engine.sh` | Retired. They exist only to move bytes across the boundary. |

**G4.1 is the one worth naming separately.** Its unfixed half is that a
*whole-tree command* — `grid.py checkout --all` — is scoped by no statement of
file ownership, and it silently reverted another agent's uncommitted work
twice in one session. Under one repo a `git worktree` isolates the source, the
graph and the tests *together*, which is the first arrangement in which an
agent can be given a genuinely private copy. Today isolating the tree does not
isolate the engine the tests run against, so the isolation is not real.

## Measured before starting, 2026-08-29

| | |
|---|---|
| tree repo | 14.8 MiB, 483 commits, 1063 grid refs |
| engine repo | 154 KiB, 203 commits |
| `payload_ref` values to rewrite | **0** — see below; the first estimate of 375 was wrong |
| top-level name collisions between the two repos | 2 — `.gitignore`, `context/` |
| crons hard-coding `/home/ubuntu/work/agi-tree` | 4 (`*/5`, `:07`, `:37`, `:47`) |
| baseline corpus | 792 nodes, `outcome_coverage` 0.255 |

Both collisions disappear once the tree sits in `.agi/` rather than at a repo
root. The four crons are the live hazard: they race any surgery, which is why
the kill-switch lands before the move and not after.

### No `payload_ref` needs rewriting, and the reason is the whole design

The first version of this table said **375 values to rewrite**. That was an
estimate, not a measurement, and it was wrong — the correct number is **zero**.

A `payload_ref` is already stored relative to the *engine root*
(`extensions/agi/bin/grid.py`, not an absolute path and not tree-relative).
Under the `.agi` layout `source_root` resolves to the enclosing repo, which
*is* the engine root. So every stored value resolves unchanged, before and
after the move:

```
today:      source_root = <tree>/agi   -> <tree>/agi/extensions/agi/bin/grid.py
unified:    source_root = <repo>       -> <repo>/extensions/agi/bin/grid.py
```

That is not luck. `payload_ref` was always a path *into the source tree*, and
G11 does not move the source tree — it moves the graph to sit beside it. The
migration therefore touches history, refs and two file locations, and does not
touch node content at all. **A migration that rewrites no node is a much
smaller and much safer operation than one that rewrites 375**, and it removes
the largest single risk this goal carried.

Recorded rather than quietly corrected, for the same reason as the count above:
this is the second unverified number in this node, and both were asserted
confidently. The pattern is the finding.

## The ancestor walk existed eleven times, not thirteen

Found while starting: `bin/` carried ten byte-identical copies of "walk up
from cwd looking for `agi-tree.config.json`", plus `lib/find-root.sh`, the
same rule's bash half — eleven sites, not thirteen. **This section originally
claimed "thirteen times — twelve `_find_root` copies under `bin/`, plus
`lib/find-root.sh` a thirteenth in bash," asserted without measuring.** It was
wrong in two ways at once: the Python count was off by two, and
`lib/find-root.sh` was miscounted as a residual when it is the deliberate bash
counterpart of the same rule, not a duplicate of it — `find_project_root` in
bash exists on purpose, and `tests/test_locations.py::test_bash_and_python_agree`
cross-checks it against `locations.py` rather than trusting the two to agree
on faith. The corrected count, measured against the engine at `ea65820`:

```
git grep -ln '^CONFIG_NAMES\s*=\s*(' ea65820 -- extensions/agi/bin extensions/agi/src
```

returns exactly 10 files: `benchmark.py`, `cli.py`, `dispatch.py`,
`metrics.py`, `post_wire.py`, `render-context.py`, `snapshot-build-site.py`,
`snapshot-goals.py`, `spawn_gate.py`, `zoom.py`.

| | Before iteration 1 | After iteration 1 |
|---|---|---|
| Canonical implementations | 0 | 2 — `bin/locations.py`, `lib/find-root.sh` |
| Python files with their own `CONFIG_NAMES` + walk | 10 | 10 (unchanged) |
| Bash implementations | 1 (`lib/find-root.sh`, deliberate) | 1 (unchanged, now cross-checked) |
| **Total sites stating the rule** | **11** | **11 canonical + 10 residual = same 10 duplicates, now with something to converge on** |

**`snapshot-goals.py` is a half-case, not a clean member of either side.** It
already calls `locations.goals_path()` — it is a consumer of the new
resolver — but it still declares its own `CONFIG_NAMES` and `config_path()`
alongside that call. It is simultaneously migrated and one of the ten
residuals. That half-state is exactly the kind of thing a summary count
flattens and gets wrong, which is what happened here.

`bin/locations.py` is the single Python rule, `lib/find-root.sh` the single
bash one, and they are checked against each other rather than trusted to agree.
Both layouts now resolve from one binary, so the migration is a config value
rather than a rewrite, and it is reversible. **The ten Python duplicates are
untouched** — `locations.py` existing does not by itself collapse anything
that calls it — and are now tracked separately as `goal:g11.1` rather than
carried as a paragraph in this node.

**This correction is left in rather than silently fixed**, because it is a
live instance of exactly what this goal argues against: an unverified number,
asserted with confidence, sitting in the node that makes the case for
collapsing duplication. The fix was to measure and split the residual into
its own goal — not to quietly overwrite the wrong number and move on.

One concrete before/after, and it is the whole goal in miniature — resolving
from inside the engine checkout:

```
$ find-root.sh /home/ubuntu/work/agi/extensions/agi/bin
ERR: no project found          # today: the engine is not in any graph
                               # after G11: <repo>/.agi, its own graph
```

## Sequencing, and the irreversible step is named

1. **One resolver, both layouts expressible.** `locations.py`, `find-root.sh`
   phase 0, `source_root` and `goals_file` in the config. Additive.
2. **The cron kill-switch** — `crons_live` in a `.geometry` config node, applied
   by a script and re-read every five minutes. This is **G10.2**'s first
   geometry node that real code reads, and it is the safety switch for step 4.
3. **Migration script, proven on a scratch clone.** Graft the history, fetch
   the grid refs, rewrite the `payload_ref` values, verify the node count does
   not drop.
4. **Execute, then demolish.** ⚠️ The one irreversible step.
5. **Worktree-per-agent isolation, `init`, and the G8.2 falsifier** on a third
   project.

## Falsifier

Clone the unified repo to an empty machine, run one command, and do engine work
end to end: edit a file, run its tests, commit. If that touches a second repo,
a staging directory, or a publish gate, the boundary was not removed — it was
renamed.

The measurable, in the Design Ethic's terms: **an engine change should cost one
commit.** Today it costs a checkout, an edit, a grid commit, a graph commit and
a publish script with four gates that refuses more often than it acts.

## Risks accepted

- **`GOALS.md` at a repo root can collide** with a document the project already
  ships. `goals_file` in the config overrides the name; both are kept, neither
  is overwritten.
- **`agi-tree` the remote becomes an archive, not a deletion.** **S4**'s rule
  applies with force here: both data-loss defects this project has paid for
  (H0, H0b) arrived as routine cleanup.
- **The grid refs must survive the move.** 1063 of them, and they are the only
  home of every payload byte. Verified on a scratch clone in step 3 before
  anything is moved for real.