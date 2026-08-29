---
confidence: 1.0
goal_id: G11
goal_kind: long-term
heading_level: 2
id: "goal:g11"
mint_id: 5fb040638ce5429e9240a07b47fb5195
order: 64
origin: goals-doc
parents: []
seeds: []
status: active
tags:
  - goal
  - root
title: "G11: One repo: the graph lives inside what it builds"
type: goal
---

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
| `payload_ref` values to rewrite | 375 |
| top-level name collisions between the two repos | 2 — `.gitignore`, `context/` |
| crons hard-coding `/home/ubuntu/work/agi-tree` | 4 (`*/5`, `:07`, `:37`, `:47`) |
| baseline corpus | 792 nodes, `outcome_coverage` 0.255 |

Both collisions disappear once the tree sits in `.agi/` rather than at a repo
root. The four crons are the live hazard: they race any surgery, which is why
the kill-switch lands before the move and not after.

## The ancestor walk existed thirteen times

Found while starting: `bin/` carried **twelve** byte-identical copies of "walk
up from cwd looking for `agi-tree.config.json`", and `lib/find-root.sh` a
thirteenth in bash. That is the real reason this goal cannot begin with the
migration. **A resolver duplicated thirteen times cannot be given a new rule —
only thirteen new rules that drift.**

`bin/locations.py` is the single Python rule, `lib/find-root.sh` the single
bash one, and they are checked against each other rather than trusted to agree.
Both layouts now resolve from one binary, so the migration is a config value
rather than a rewrite, and it is reversible.

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
