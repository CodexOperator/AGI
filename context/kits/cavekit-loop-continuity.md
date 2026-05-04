---
created: "2026-05-04"
last_edited: "2026-05-04"
---

# Cavekit: Loop Continuity

## Scope

After the topology fold lands, the research loop must continue to function end-to-end against the unified `~/.hermes/agi/` repository: existing tests pass, a smoke iteration runs to completion, no LLM-quota leaks occur, the pi bridge extension still loads, the SessionStart hook still injects context, and — critically — the loop is able to research the AGI codebase itself, producing graph nodes that reference real files under `~/.hermes/agi/extensions/agi/`.

## Requirements

### R1: All existing tests pass post-fold
**Description:** The full pytest suite under the unified engine extension's test directory passes after the fold lands, with the same count of passing tests as the pre-fold baseline.
**Acceptance Criteria:**
- [ ] A pre-fold baseline file exists under `context/refs/` recording the pre-fold passing test count.
- [ ] Running pytest against `~/.hermes/agi/extensions/agi/tests/` exits with status code 0.
- [ ] The pytest summary line reports a passing count equal to or greater than the recorded baseline.
- [ ] No test is skipped or xfailed for a reason that did not already apply pre-fold.
**Dependencies:** cavekit-topology-fold.md R2.

### R2: Single-iteration smoke run succeeds
**Description:** Invoking the loop with a one-iteration cap against the live research data project completes without error and produces the expected manifest artifact. Either CLI name (`agi` or the transition alias `autoresearch-tree`) is accepted.
**Acceptance Criteria:**
- [ ] `agi --max-iters 1` against `~/.hermes/agi-tree/` exits with status code 0.
- [ ] `autoresearch-tree --max-iters 1` against `~/.hermes/agi-tree/` exits with status code 0.
- [ ] An iter-NNN session manifest file is created under the project's session directory after the run.
- [ ] The manifest contains at least one agent record entry.
**Dependencies:** cavekit-topology-fold.md R8.

### R3: No LLM-quota leak
**Description:** The agent run does not accidentally invoke the user's Claude Code subscription quota; pi falls back to its real default provider.
**Acceptance Criteria:**
- [ ] Agent output logs collected during R2's smoke run do not contain the literal substring `api.anthropic.com`.
- [ ] Agent output logs do not contain the literal string `Token Plan`.
- [ ] Agent output logs do not contain HTTP 429 error markers.
- [ ] The provider field recorded in the session manifest is the pi default (minimax) and not anthropic.
**Dependencies:** R2.

### R4: Pi bridge extension still loads
**Description:** The bridge extension at `~/.hermes/agi/extensions/agi-bridge/` continues to be loaded by pi at startup, and its `before_agent_start` hook still injects the auto-generated map header into agent system prompts.
**Acceptance Criteria:**
- [ ] Pi startup logs contain a marker indicating the agi-bridge extension was loaded.
- [ ] When an agent is launched via `/autoresearch`, that agent's system prompt contains the auto-injected map header.
- [ ] The injected content is regenerated each agent turn (the timestamp or content hash differs across consecutive turns).
**Dependencies:** cavekit-topology-fold.md R3, R9.

### R5: SessionStart hook still injects context
**Description:** The `~/.hermes/agi/extensions/agi/hooks/cc-session-start.sh` hook continues to inject the per-project context map (INJECTION.md or its equivalent) into Claude Code sessions launched in any directory containing the autoresearch-tree config file.
**Acceptance Criteria:**
- [ ] Launching a Claude Code session in a directory that contains the autoresearch-tree config file results in the SessionStart hook executing.
- [ ] The session's initial context contains the contents of the project's INJECTION.md (or equivalent context map).
- [ ] Launching a Claude Code session in a directory without the config file does not trigger the injection.
**Dependencies:** cavekit-topology-fold.md R2.

### R6: Loop researches its own AGI code
**Description:** Pointed at `~/.hermes/agi/` as the project root, the loop produces graph nodes that correspond to real files or functions inside the unified AGI codebase. The loop is dogfooding both the algorithms and the harness.
**Acceptance Criteria:**
- [ ] Running the loop with `~/.hermes/agi/` as project root for at least one iteration exits with status code 0.
- [ ] At least one node written by that iteration has a source field whose value is a path under `~/.hermes/agi/extensions/agi/`.
- [ ] The path referenced in that source field corresponds to an existing file on disk.
- [ ] The node's type is one of the recognised autoresearch-tree node types (verifiable through the type registry).
**Dependencies:** R1, R2.

## Out of Scope

- Actually fixing whatever bug-sweep finds (handled in a separate cycle).
- Replacing the primary loop metric (deferred to TODO).
- Migrating loop state from filesystem to sqlite (deferred to TODO).
- Adding new node types or new agent roles.
- Performance tuning beyond what is required to keep tests green.

## Cross-References

- See also: cavekit-topology-fold.md (the fold creates the surface this kit verifies remains live).
- See also: cavekit-bug-sweep.md (R1–R6 here define the surface that bug-sweep verifies).

## Changelog

_(empty)_
