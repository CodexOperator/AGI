---
created: "2026-05-04"
last_edited: "2026-05-04"
---

# Cavekit: Bug Sweep

## Scope

After the topology fold lands, dispatch a small set of focused, parallel verification agents that confirm the unified repo is healthy along the surfaces declared in the loop-continuity kit. Each agent is read-only, has a single responsibility, and reports pass or fail with file:line evidence. The aggregate report gates whether the fold branch is allowed to merge into main and gates whether the legacy local directory and github mirror can be cleaned up.

## Requirements

### R1: Parallel verification agents dispatched post-fold
**Description:** Four to six parallel verification agents run after the fold lands. Each has one focused responsibility drawn from the following set: pytest run against the unified engine's test directory, smoke loop against the data project, env-leak audit, bridge-extension load check, render-output sanity (the project context map regenerates on agent turn), embeddings sanity (gensim plus UMAP imports plus a smoke run). Each agent reports pass or fail with file-and-line evidence.
**Acceptance Criteria:**
- [ ] At least four verification agents are dispatched.
- [ ] At most six verification agents are dispatched.
- [ ] At least one agent runs pytest against `~/.hermes/agi/extensions/agi/tests/` and reports pass or fail.
- [ ] At least one agent runs a smoke loop against `~/.hermes/agi-tree/` and reports pass or fail.
- [ ] At least one agent performs an env-leak audit and reports pass or fail.
- [ ] At least one agent performs a bridge-extension load check and reports pass or fail.
- [ ] Each agent's report includes at least one file:line evidence pointer for its verdict.
- [ ] The exact subset of agents chosen is documented in the aggregate report.
**Dependencies:** cavekit-topology-fold.md R2, R3.

### R2: Aggregate report committed
**Description:** A single aggregate report at `context/impl/bug-sweep-report.md` lists which agents ran, which checks passed, which failed, and the evidence each agent produced.
**Acceptance Criteria:**
- [ ] The file `context/impl/bug-sweep-report.md` exists in the unified repo.
- [ ] The report names every verification agent that ran.
- [ ] The report records pass or fail for each agent.
- [ ] For every failing agent, the aggregate report includes the file:line evidence the agent cited.
**Dependencies:** R1.

### R3: Failures block merge
**Description:** If any verification check in R1 fails, the fold branch is not merged into main. The loop is not declared green while any verification check is failing.
**Acceptance Criteria:**
- [ ] If the aggregate report records any failed check, the fold branch has not been merged into main.
- [ ] If the aggregate report records all checks passing, merge is permitted.
- [ ] No "loop green" declaration is published while a failed check is recorded in the most recent aggregate report.
**Dependencies:** R2.

### R4: Loop-against-self verification
**Description:** A dedicated verification agent dispatches one full iteration of the unified loop with `~/.hermes/agi/` as the project root and verifies the resulting graph contains nodes whose source field references files under `~/.hermes/agi/extensions/agi/`.
**Acceptance Criteria:**
- [ ] One verification agent runs the loop with `~/.hermes/agi/` as the project root.
- [ ] The agent's report states the iteration's exit code; the exit code is 0.
- [ ] The agent reports the count of graph nodes whose source field references a path under `~/.hermes/agi/extensions/agi/`.
- [ ] The reported count is greater than or equal to one.
- [ ] At least one path named in the report corresponds to an existing file on disk.
**Dependencies:** R1.

### R5: Verification agents are read-only
**Description:** Verification agents run scripts and emit reports; they do not modify code under test. Fixing what verification finds triggers a separate build cycle.
**Acceptance Criteria:**
- [ ] No file under `~/.hermes/agi/extensions/agi/src/`, `~/.hermes/agi/extensions/agi/bin/`, `~/.hermes/agi/extensions/agi/hooks/`, or `~/.hermes/agi/extensions/agi-bridge/` is modified during the verification phase.
- [ ] No file under `~/.hermes/agi-tree/` is modified during the verification phase.
- [ ] No commit is created in any of those repositories during the verification phase, except commits that add report output under `context/impl/`.
- [ ] Each verification agent's instructions explicitly forbid write operations against code under test.
**Dependencies:** R1.

## Out of Scope

- Actually performing any fixes for failed checks (separate cycle).
- Adding new verification responsibilities beyond the six described in R1.
- Running verification against any directory other than the unified repo and the agi-tree data project.
- Long-running stress tests or fuzz campaigns.

## Cross-References

- See also: cavekit-loop-continuity.md (R1–R6 there define the surface this sweep verifies).
- See also: cavekit-topology-fold.md (R10 — sweep clearance is a precondition for legacy cleanup).

## Changelog

_(empty)_
