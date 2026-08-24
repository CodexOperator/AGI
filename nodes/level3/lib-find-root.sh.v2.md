---
confidence: 0.85
id: "level3:lib-find-root.sh@v2"
origin: build-version
version: 2
supersedes: "level3:lib-find-root.sh"
parents:
  - goal:g8.2
payload_ref: extensions/agi/lib/find-root.sh
tags:
  - level3
  - build-version
  - g8.2
title: "Level-3 v2: extensions/agi/lib/find-root.sh — descend into <project>/agi/<name>-tree"
type: level3
---

`extensions/agi/lib/find-root.sh` v2 — adds a descend fallback to `find_project_root` so the engine also works when a generic project embeds its graph as a subdirectory repo instead of being the graph repo itself.

**What changed.** v1 only walked *up* from `$PWD` for `agi-tree.config.json` (or the legacy `autoresearch-tree.config.json`), which is correct for today's agi-tree layout where the config and `nodes/` sit at the repo root. It is wrong for the layout G8.2 is adopting: `<project-repo>/agi/<project-repo>-tree/` as its own repo with its own config, `GOALS.md`, and `nodes/`. Standing at `<project-repo>` and walking up finds nothing there, so the loop refused to run even with the tree present one level down. v2 keeps the up-walk exactly as-is and tries it *first*; only if it fails does it fall back to a descend phase that looks under `$start/agi/` for a `*-tree` directory carrying a config file. The order is not negotiable: every existing project (agi-tree included, where the tree is the root) must keep resolving via the up-walk with zero behavior change, and up-first is also strictly cheaper to reason about — a hit on the way up is unambiguous by construction, while a descend hit requires the disambiguation rule below.

**Ambiguity rule.** Preferred match is the unambiguous case: `$start/agi/$(basename $start)-tree/<config>`. If that's absent, it globs `$start/agi/*-tree/<config>` and collects every directory that actually has a config file. Exactly one candidate wins. Two or more is a hard error — every candidate path is printed to stderr and the function returns 1. Guessing (e.g. "pick the first" or "pick the newest") would be strictly worse than refusing: a wrong silent guess sends the loop reading and writing a stranger's node graph, which is unrecoverable in a way a loud failure is not. An explicit error the user can resolve by renaming or removing a stray `*-tree` dir is the safe failure mode.

**Why this doesn't violate g8.2.** No project name is hardcoded anywhere in the new code path — there is no `if project == "..."` branch, canonical or otherwise. The descend target is derived purely from `basename "$start"` (whatever directory the caller happens to be standing in) plus a `*-tree` glob; the function has no notion of "agi-tree" as a distinguished project, only of the shape `<dir>/agi/<name>-tree/<config>`. Running it from inside agi-tree itself never reaches phase 2 at all, since phase 1 already succeeds there.

**Implementation notes.** `agi_tree_config_path()` (the single place that knows the two config filenames, canonical then legacy) is unchanged and reused by both phases — no duplicated name list. The new `_agi_find_root_descend()` helper uses `shopt -s nullglob` / `shopt -u nullglob` bracketing the glob so a no-match expands to nothing instead of the literal `*-tree` pattern, and it always runs inside a `$(...)` command substitution (so even if the shopt toggle were skipped, it can't leak into a sourcing caller's shell). Every fallible statement (`agi_tree_config_path` calls, the glob, the final `return 1`) sits inside an `if`/`case`/command-substitution-tested context, never as a bare statement, so `set -euo pipefail` callers (`driver.sh`, `hooks/cc-session-start.sh`) can't be killed by an internal miss — only by their own explicit handling of `find_project_root`'s final nonzero return, which both already have (`|| { ... }` and `|| exit 0` respectively, unchanged from v1).

**Verification.** Built a throwaway tree under `/tmp/frt-test` (not in either repo, not under `nodes/`) with five fixtures and ran each against the patched script by sourcing it fresh in a subshell:
1. Up-walk from a subdirectory of a classic project (config at the top) → resolved to the project root. PASS.
2. Descend, exact basename match (`fantasia/agi/fantasia-tree/agi-tree.config.json` from `fantasia/`) → resolved correctly. PASS.
3. Descend, single non-matching `*-tree` name (`widget/agi/some-other-tree/`) → resolved via the glob path. PASS.
4. Two `*-tree` dirs both carrying a config → exit 1, both candidate paths present on stderr, empty stdout. PASS.
5. No tree at all, invoked from inside a `bash -c 'set -euo pipefail; ...'` subshell that sources the file and handles the nonzero return with `||` → exited 0 via the caller's own handling, script itself did not abort the caller. PASS.

5/5 synthetic checks passed. Then ran the real regression: `cd /home/ubuntu/work/agi-tree && bash agi/extensions/agi/driver.sh --smoke --max-iters 1`, which printed `[driver] PROJECT_ROOT=/home/ubuntu/work/agi-tree` — the up-walk path, unchanged from before this edit. 6/6 total checks passed; nothing failed.

**Parent review, same version.** Re-running the five fixtures independently surfaced a defect this version had inherited from v1 rather than introduced: the executed-mode failure branch printed `$(pwd)`, so a run given an explicit path argument blamed the caller's working directory for a failure somewhere else entirely (`bash find-root.sh /tmp/x/barren` reported "under /home/ubuntu/work/agi-tree"). Fixed in this same version — the argument is captured once and the error names the directory actually searched, with `$PWD` used only as the default. Re-verified in both modes: with an argument and with none. This is recorded here rather than as a v3 because it is the same payload edit under review, not a later change branching off an accepted one.

**Known limitation — deliberately out of scope here.** The Python entry points (`bin/cli.py`, `bin/zoom.py`, `bin/metrics.py`, `bin/benchmark.py`, `bin/dispatch.py`, `bin/post_wire.py`, `bin/grid.py`, `bin/dashboard.py`) each carry their own private copy of project-root discovery and were not touched by this change — they still only walk up. Until they're pointed at this shared bash implementation (or gain an equivalent descend fallback of their own), a project using the new `<project>/agi/<project>-tree/` layout will resolve correctly for `driver.sh` and the Claude Code session-start hook, but not yet for any of those Python tools invoked directly from `<project-repo>`. That unification is remaining work, not covered by this node.
