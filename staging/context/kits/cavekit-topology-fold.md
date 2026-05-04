---
created: "2026-05-04"
last_edited: "2026-05-04"
---

# Cavekit: Topology Fold

## Scope

Fold the previously separate `~/autoresearch-tree/` research loop harness repository into the canonical AGI graph code repository at `~/.hermes/agi/`, producing a single unified repo named `agi` ("artificial graph intelligence") that houses both the graph algorithms and the research loop harness. The fold preserves git history from both source repositories, relocates the engine extension and TypeScript bridge under the unified repo, and consolidates the hermes/agi root algorithm files under a clean module path. Two ASCII renderers continue to coexist during the transition; the legacy `~/autoresearch-tree/` directory and its github mirror remain untouched until verification clears.

## Requirements

### R1: Unified repo at ~/.hermes/agi/
**Description:** `~/.hermes/agi/` is the single canonical repository for the project. Its README declares the repo as "agi = artificial graph intelligence: graph algorithms + research loop harness". The top-level layout includes an `extensions/` directory containing the engine and bridge, a `skills/agi/SKILL.md`, a top-level `package.json` declaring `pi.extensions` and `pi.skills`, a `README.md`, and a `TODO.md`.
**Acceptance Criteria:**
- [ ] `~/.hermes/agi/README.md` exists and contains the literal phrase "artificial graph intelligence".
- [ ] `~/.hermes/agi/README.md` references both "graph algorithms" and "research loop harness" as the contents of the repo.
- [ ] `~/.hermes/agi/package.json` exists and contains a `pi.extensions` declaration and a `pi.skills` declaration.
- [ ] `~/.hermes/agi/extensions/agi/` exists as a directory.
- [ ] `~/.hermes/agi/extensions/agi-bridge/` exists as a directory.
- [ ] `~/.hermes/agi/skills/agi/SKILL.md` exists.
- [ ] `~/.hermes/agi/TODO.md` exists at the repo root.
**Dependencies:** None.

### R2: Engine extension folded into extensions/agi/
**Description:** The autoresearch-tree engine extension previously located at `~/autoresearch-tree/extensions/autoresearch-tree/` is folded into `~/.hermes/agi/extensions/agi/`. All engine subdirectories (`bin/`, `hooks/`, `lib/`, `src/`, `tests/`) and the engine entry points (`driver.sh`, `conftest.py`) are present under the new path. Engine code is preserved verbatim aside from path-rooting adjustments expressed through the existing `PLUGIN_ROOT` and `PROJECT_ROOT` environment variable convention.
**Acceptance Criteria:**
- [ ] `~/.hermes/agi/extensions/agi/driver.sh` exists and is executable.
- [ ] `~/.hermes/agi/extensions/agi/conftest.py` exists.
- [ ] `~/.hermes/agi/extensions/agi/bin/` exists and contains `snapshot.py`, `render.py`, `dispatch.py`, `heal.py`, `zoom.py`, and `cli.py`.
- [ ] `~/.hermes/agi/extensions/agi/hooks/cc-session-start.sh` exists.
- [ ] `~/.hermes/agi/extensions/agi/lib/find-root.sh` exists.
- [ ] `~/.hermes/agi/extensions/agi/lib/agent-prompt.md` exists.
- [ ] `~/.hermes/agi/extensions/agi/src/` exists and contains the previously present subdirectories.
- [ ] `~/.hermes/agi/extensions/agi/tests/` exists and contains the previously present test files.
- [ ] No file under `~/.hermes/agi/extensions/agi/` references absolute paths under `~/autoresearch-tree/`.
**Dependencies:** R1.

### R3: Bridge extension folded into extensions/agi-bridge/
**Description:** The TypeScript bridge extension previously located at `~/autoresearch-tree/extensions/autoresearch-tree-bridge/` is folded into `~/.hermes/agi/extensions/agi-bridge/`. Its `index.ts` continues to register a `before_agent_start` hook with pi.
**Acceptance Criteria:**
- [ ] `~/.hermes/agi/extensions/agi-bridge/index.ts` exists.
- [ ] `~/.hermes/agi/extensions/agi-bridge/README.md` exists.
- [ ] The bridge's `index.ts` registers a `before_agent_start` hook (the literal string `before_agent_start` appears in the file).
- [ ] No file under `~/.hermes/agi/extensions/agi-bridge/` references absolute paths under `~/autoresearch-tree/`.
**Dependencies:** R1.

### R4: SKILL.md folded into skills/agi/
**Description:** The skill definition previously located at `~/autoresearch-tree/skills/autoresearch-tree/SKILL.md` is folded into `~/.hermes/agi/skills/agi/SKILL.md`. The propagation recipe that previously mirrored SKILL.md to five locations is updated to reference the new canonical source path, and the new target paths are recorded in TODO.
**Acceptance Criteria:**
- [ ] `~/.hermes/agi/skills/agi/SKILL.md` exists.
- [ ] The content of `~/.hermes/agi/skills/agi/SKILL.md` is non-empty.
- [ ] `~/.hermes/agi/TODO.md` contains an entry referencing the SKILL.md propagation recipe and listing the canonical source path `~/.hermes/agi/skills/agi/SKILL.md`.
**Dependencies:** R1.

### R5: hermes/agi root algorithm files moved into src/agi_algos/
**Description:** The algorithm files previously at the root of `~/.hermes/agi/` (`graph_builder.py`, `query_engine.py`, the previously underscore-prefixed `_benchmark.py` renamed to `benchmark.py`, `pi_tree_adapter.py`, and `asciirender.py`) are relocated under `~/.hermes/agi/extensions/agi/src/agi_algos/`. An `__init__.py` exports the public API of those modules. The previous root-level paths either contain a deprecated re-export stub for one transition cycle or are removed cleanly when no external import depends on them.
**Acceptance Criteria:**
- [ ] `~/.hermes/agi/extensions/agi/src/agi_algos/__init__.py` exists.
- [ ] `~/.hermes/agi/extensions/agi/src/agi_algos/graph_builder.py` exists.
- [ ] `~/.hermes/agi/extensions/agi/src/agi_algos/query_engine.py` exists.
- [ ] `~/.hermes/agi/extensions/agi/src/agi_algos/benchmark.py` exists.
- [ ] No file named `_benchmark.py` remains under `~/.hermes/agi/extensions/agi/src/agi_algos/`.
- [ ] `~/.hermes/agi/extensions/agi/src/agi_algos/pi_tree_adapter.py` exists.
- [ ] `~/.hermes/agi/extensions/agi/src/agi_algos/asciirender.py` exists.
- [ ] The `__init__.py` exports the public symbols of each of the five modules.
- [ ] Each prior root-level path under `~/.hermes/agi/` is either absent or contains only a re-export stub that imports from `agi_algos`.
**Dependencies:** R1, R2.

### R6: Subtree-merged history preserves both origins
**Description:** The git history of the unified repo includes commits originating from the prior `~/.hermes/agi/` repository AND commits originating from the prior `~/autoresearch-tree/` repository (mirrored at github.com/CodexOperator/autoresearch-tree). Running git log over the unified repo can surface commits from either origin.
**Acceptance Criteria:**
- [ ] The unified repo's git log contains at least one commit hash that was present in the prior `~/.hermes/agi/` history.
- [ ] The unified repo's git log contains at least one commit hash that was present in the prior `~/autoresearch-tree/` history.
- [ ] The unified repo's git log contains at least one commit message authored before the fold from each origin.
**Dependencies:** R1, R2, R3.

### R7: Two ASCII renderers coexist during transition
**Description:** Both ASCII renderers remain present and functional after the fold. The ar-tree-style renderer continues to live at `extensions/agi/src/renderers/ascii.py`. The hermes 35-type-style renderer continues to live at `extensions/agi/src/agi_algos/asciirender.py`. The `pi_tree_adapter.py` module continues to bridge between the two type systems. Unification is deferred to the TODO file.
**Acceptance Criteria:**
- [ ] `~/.hermes/agi/extensions/agi/src/renderers/ascii.py` exists.
- [ ] `~/.hermes/agi/extensions/agi/src/agi_algos/asciirender.py` exists.
- [ ] `~/.hermes/agi/extensions/agi/src/agi_algos/pi_tree_adapter.py` exists.
- [ ] `~/.hermes/agi/TODO.md` contains an entry that names both renderer paths and describes the deferred unification.
**Dependencies:** R2, R5.

### R8: Both CLI binaries resolve to the unified driver
**Description:** Both the `agi` command and the `autoresearch-tree` command resolve to the unified engine's `driver.sh`. During the transition window, invocations of either name behave identically.
**Acceptance Criteria:**
- [ ] `~/.local/bin/agi` exists and resolves (directly or through a symlink chain) to `~/.hermes/agi/extensions/agi/driver.sh`.
- [ ] `~/.local/bin/autoresearch-tree` exists and resolves to `~/.hermes/agi/extensions/agi/driver.sh`.
- [ ] Invoking `agi --help` and `autoresearch-tree --help` produces identical output.
**Dependencies:** R2.

### R9: Pi auto-discovery verified; symlinks created only if required
**Description:** Verification confirms whether pi reads the project-local `package.json` `pi.extensions` glob and discovers the agi engine and bridge without external symlinks. If pi auto-discovers the extensions, no `.pi/extensions/` symlinks are created. If pi requires global registration, symlinks `.pi/extensions/agi → ~/.hermes/agi/extensions/agi` and `.pi/extensions/agi-bridge → ~/.hermes/agi/extensions/agi-bridge` are created. The verification result is recorded in writing.
**Acceptance Criteria:**
- [ ] A verification record exists (committed to the unified repo under `context/` or referenced from `TODO.md`) stating whether pi auto-discovered the extensions.
- [ ] If the verification record states pi auto-discovers the extensions, no symlink exists at `.pi/extensions/agi` and no symlink exists at `.pi/extensions/agi-bridge`.
- [ ] If the verification record states pi requires global registration, `.pi/extensions/agi` resolves to `~/.hermes/agi/extensions/agi` and `.pi/extensions/agi-bridge` resolves to `~/.hermes/agi/extensions/agi-bridge`.
- [ ] Pi startup against a project that uses these extensions completes without an "extension not found" or equivalent error after the symlink decision is applied.
**Dependencies:** R2, R3.

### R10: Legacy directory and github mirror retained until verification clears
**Description:** The local directory `~/autoresearch-tree/` remains in place in a read-only state until the bug-sweep verification cycle passes. The github mirror at `github.com/CodexOperator/autoresearch-tree` is archived and updated to point at `CodexOperator/agi`, but only after bug-sweep clears. Both the local cleanup and the archive action are deferred entries in the TODO file.
**Acceptance Criteria:**
- [ ] Until bug-sweep clears, `~/autoresearch-tree/` exists on disk.
- [ ] Until bug-sweep clears, `github.com/CodexOperator/autoresearch-tree` is not in an archived state.
- [ ] After bug-sweep clears, the github repository `CodexOperator/autoresearch-tree` is in an archived state.
- [ ] After bug-sweep clears, the README of `CodexOperator/autoresearch-tree` contains a pointer to `CodexOperator/agi` as the new canonical home.
- [ ] `~/.hermes/agi/TODO.md` contains entries for removing the local `~/autoresearch-tree/` directory and for archiving the github mirror, each with a priority label.
**Dependencies:** R1, R6.

## Out of Scope

- Rewriting `graph_builder.py` to be data-source-agnostic (deferred to TODO).
- Unifying the two ASCII renderers into a single canonical renderer (deferred to TODO).
- Removing the local `~/autoresearch-tree/` directory before verification clears (deferred to TODO).
- Modifying the upstream `davebcn87/pi-autoresearch` runtime in any way.
- Renaming `CodexOperator/autoresearch-tree`; it is archived rather than renamed.

## Cross-References

- See also: cavekit-loop-continuity.md (tests, smoke run, and dogfood loop must still pass after the fold).
- See also: cavekit-bug-sweep.md (verifies the fold landed cleanly; clearance gates R10).
- See also: cavekit-git-remote.md (pushes the unified repo and the agi-tree data repo, archives the legacy mirror).
- See also: cavekit-deferred-todo.md (captures deferred ASCII unification, pi-extension symlink decision, legacy cleanup, and downstream algorithm/harness work).

## Changelog

_(empty)_
