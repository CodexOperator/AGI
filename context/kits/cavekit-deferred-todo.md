---
created: "2026-05-04"
last_edited: "2026-05-04"
---

# Cavekit: Deferred TODO

## Scope

Explicit, persisted register of work that is intentionally not performed during the topology-fold cycle. The register lives in `~/.hermes/agi/TODO.md` at the root of the unified repo and is split into three sections covering algorithm-side work, harness-side work, and decisions deferred during the fold. Each entry carries enough metadata (description, rationale, evidence pointer, priority) for a future cycle to pick it up without rediscovery.

## Requirements

### R1: TODO file exists with three sections
**Description:** A single TODO file at `~/.hermes/agi/TODO.md` exists at the root of the unified repo and is split into three top-level sections: AGI-side algorithm work, harness-side work, and decisions deferred during the fold. Each entry across all sections includes a short description, a rationale, a source-of-truth evidence pointer (commit hash, file path, or handoff-line reference), and a priority label drawn from the set {P0, P1, P2}.
**Acceptance Criteria:**
- [ ] `~/.hermes/agi/TODO.md` exists.
- [ ] The file contains a section heading for AGI-side algorithm work.
- [ ] The file contains a section heading for harness-side work.
- [ ] The file contains a section heading for decisions deferred during the fold.
- [ ] Every entry under any section has a short description.
- [ ] Every entry has a rationale.
- [ ] Every entry has an evidence pointer that is a commit hash, an absolute file path, or a handoff-line reference.
- [ ] Every entry has a priority label whose value is exactly one of `P0`, `P1`, or `P2`.
**Dependencies:** cavekit-topology-fold.md R1.

### R2: TODO file covers required entries
**Description:** The TODO file covers, at minimum, the following entries.
**Acceptance Criteria:**
- [ ] An entry exists for the data-source-agnostic refactor of `graph_builder.py`.
- [ ] An entry exists for ASCII renderer unification, naming both `~/.hermes/agi/extensions/agi/src/renderers/ascii.py` and `~/.hermes/agi/extensions/agi/src/agi_algos/asciirender.py`.
- [ ] An entry exists for DB-only state migration, referencing `sqlite_backend.py`.
- [ ] An entry exists for parsing `~/.hermes/agi-tree/nodes/{type}/*.md` into the DB as importable nodes.
- [ ] An entry exists for replacing the `longest_chain_length` primary metric with a composite or evidence-fraction metric.
- [ ] An entry exists for the orphan-verdict gate that requires `evidence_runs > 0`.
- [ ] An entry exists for wiring the R11 loader path-safety bug, citing commit `141df8d6`.
- [ ] An entry exists for adding an `--iter-base N` flag to `dispatch.py`.
- [ ] An entry exists for shipping the gensim+UMAP embedding stack from research artifact to the production renderer path.
- [ ] An entry exists for removing the legacy local directory `~/autoresearch-tree/` after verification clears.
- [ ] An entry exists for archiving `github.com/CodexOperator/autoresearch-tree` after verification clears, including the README pointer to `CodexOperator/agi`.
- [ ] An entry exists for removing the old fallback at `~/.pi/agent/git/github.com/davebcn87/pi-autoresearch/extensions/autoresearch-tree/` after verification clears.
- [ ] An entry exists for modularNN worktree cleanup at `~/.hermes/belam-codex-modularnn-spike-viz/`.
- [ ] An entry exists for the SKILL.md propagation recipe (5-location sync) updated for new canonical paths.
- [ ] An entry exists recording whether pi requires `.pi/extensions/` symlinks or auto-discovers via the `package.json pi.extensions` glob.
**Dependencies:** R1.

### R3: TODO file committed to the unified repo
**Description:** The TODO file is committed to the unified repo so it survives across sessions and is visible to future agents and contributors.
**Acceptance Criteria:**
- [ ] `~/.hermes/agi/TODO.md` is tracked by git in `~/.hermes/agi/` (appears in `git ls-files`).
- [ ] The file is present at the tip of the branch that gets pushed to origin.
- [ ] The file is not listed in `.gitignore`.
**Dependencies:** R1.

### R4: TODO file is actionable as a checklist
**Description:** The TODO file is readable as a checklist; an agent can pick a P0 or P1 item and act on it without external context.
**Acceptance Criteria:**
- [ ] Every entry's description names the file paths or modules it touches, or includes the evidence pointer that does.
- [ ] No entry's description requires the reader to consult an external document not referenced from the entry.
- [ ] Items are sorted or grouped such that all P0 entries can be located without reading every entry.
**Dependencies:** R1, R2.

## Out of Scope

- Performing any of the deferred work in this cycle.
- Estimating effort or scheduling deferred items.
- Triaging deferred items into a project board or external tracker.

## Cross-References

- See also: cavekit-topology-fold.md (R5 motivates the agi_algos relocation, R7 motivates the ASCII unification entry, R9 motivates the pi-extension symlink decision entry, R10 motivates the legacy cleanup entries).
- See also: cavekit-loop-continuity.md (R3 — env-leak context referenced by harness-side entries).
- See also: cavekit-git-remote.md (the TODO file is pushed as part of the remote sync requirements).

## Changelog

_(empty)_
