---
created: "2026-05-04"
last_edited: "2026-05-04"
---

# Cavekit Overview

## Project description

Fold the autoresearch-tree research loop harness into the canonical AGI graph code repo at `~/.hermes/agi/`. Make the loop dogfood by researching its own algorithms and harness as graph nodes. Stage DB-driven evolution and other deferred work in a TODO file. Push three remotes: `CodexOperator/agi` (unified), `CodexOperator/agi-tree` (data), and archive `CodexOperator/autoresearch-tree` post-verification with a README pointer to the new canonical home.

## Domain index

| # | Cavekit | Status | Description |
|---|---------|--------|-------------|
| 1 | [cavekit-topology-fold.md](cavekit-topology-fold.md) | DRAFT | Fold autoresearch-tree harness into the unified `~/.hermes/agi/` repo, preserving both git histories; relocate hermes/agi root algorithm files under `extensions/agi/src/agi_algos/`. |
| 2 | [cavekit-loop-continuity.md](cavekit-loop-continuity.md) | DRAFT | Tests pass, smoke loop runs, no LLM-quota leak, bridge and SessionStart hooks still work, loop researches its own AGI code. |
| 3 | [cavekit-bug-sweep.md](cavekit-bug-sweep.md) | DRAFT | Parallel read-only verification agents and aggregate report gating the merge and the legacy cleanup. |
| 4 | [cavekit-deferred-todo.md](cavekit-deferred-todo.md) | DRAFT | Persistent register of work intentionally not done in this cycle, captured in `~/.hermes/agi/TODO.md`. |
| 5 | [cavekit-git-remote.md](cavekit-git-remote.md) | DRAFT | Feature-branch hygiene, remote initialisation for the unified and data repos, archival of the legacy github mirror, push verification under the `CodexOperator` user. |

## Cross-reference map

- topology-fold ↔ loop-continuity: the fold creates the surface that loop-continuity verifies remains live; tests, smoke run, and dogfood loop must still pass after the fold.
- topology-fold ↔ bug-sweep: bug-sweep verifies that the fold landed cleanly; topology-fold R10 (legacy cleanup) is gated on bug-sweep clearance.
- topology-fold ↔ git-remote: subtree-merged history (topology-fold R6) is realised by the push hygiene under git-remote R2; legacy archive (topology-fold R10) is realised by git-remote R4.
- topology-fold ↔ deferred-todo: items deferred during the fold (ASCII unification, pi-extension symlink decision, legacy cleanup, downstream algorithm and harness work) are recorded under deferred-todo.
- loop-continuity ↔ bug-sweep: bug-sweep verifies exactly the surface that loop-continuity declares; bug-sweep R4 corresponds to loop-continuity R6 (loop researches its own AGI code).
- git-remote ↔ all: every cavekit's filesystem outcomes are made durable through the git-remote kit's push and verification requirements.

## Dependency graph

```
topology-fold
       |
       v
loop-continuity
       |
       v
bug-sweep

deferred-todo  (parallel / cross-cutting)
git-remote     (parallel / cross-cutting)
```

`deferred-todo` and `git-remote` are not in the linear chain — they apply across every other kit and are evaluated in parallel.

## Coverage summary

- Total kits: 5.
- Total requirements: 31 (topology-fold=10, loop-continuity=6, bug-sweep=5, deferred-todo=4, git-remote=6).
- Total acceptance criteria: 152 (topology-fold=51, loop-continuity=22, bug-sweep=24, deferred-todo=29, git-remote=26).

## Changelog

_(empty)_
