---
created: 2026-04-30
last_edited: 2026-04-30
---

# Cavekit: autoresearch-tree-skill

## Scope

The agent skill that drives the autoresearch loop on top of the rest of the system. It forks an existing autoresearch skill family rather than modifying it, picks between big-idea and small-idea exploration each iteration, dispatches parallel builder agents, accepts their experiment results as verdict emissions, and runs a benchmark harness that extends the predecessor harness with new chain-shaped metrics. The skill must be drop-in portable: it should run in any repository where the project context directory has been added.

## Requirements

### R1: Skill Lives in a Forked Skill Repository

**Description:** A new skill is added to the existing autoresearch skill repository alongside the existing skills, without modifying or removing them.

**Acceptance Criteria:**
- [ ] The new skill is added at a documented path inside the existing autoresearch skill repository
- [ ] No file under the existing autoresearch-create or autoresearch-finalize skills is modified or removed by this kit's installation
- [ ] Adding the skill is one new directory of files, not a patch to existing files
- [ ] After installation, both the new skill and the original skills are listed by the standard skill enumeration

### R2: Big-Idea-Versus-Small-Idea Decision Per Iteration

**Description:** Every iteration begins with an explicit decision between exploring a big idea or a small idea. The split is governed by a configuration parameter shared with chain-engine.

**Acceptance Criteria:**
- [ ] Each iteration emits a record naming the chosen path (big idea or small idea) before any agent is dispatched
- [ ] The probability of choosing the big-idea path equals the configured `big_idea_vs_small_idea_split`
- [ ] Two consecutive iterations with the same seed and configuration produce the same choice
- [ ] When the configuration value is missing or out of range, the iteration aborts with a structured error

**Dependencies:** chain-engine (R7 configuration file)

### R3: Parallel Claude Builder Dispatch

**Description:** Each iteration dispatches up to five builder agents in parallel using a Claude-class model. Equivalent Ollama dispatch is explicitly deferred.

**Acceptance Criteria:**
- [ ] An iteration dispatches at most five builder agents in parallel
- [ ] When fewer candidates are eligible than the maximum, the iteration runs only that many agents
- [ ] The kit explicitly documents that Ollama-based dispatch is a v2 scope item and is not required here
- [ ] Failure of one agent does not abort the others; partial results are collected and reported

### R4: Per-Agent Briefing Payload

**Description:** Each builder agent receives a briefing that contains the current chain statistics, the attractiveness scores for candidate chains, and the menu of available actions (extend, fork, hop, fresh start).

**Acceptance Criteria:**
- [ ] The briefing names the current set of chains under consideration with their length, depth, recency, and mvp count
- [ ] The briefing names each candidate chain's attractiveness score from the chain-engine
- [ ] The briefing lists the available actions per chain (extend at tail, fork at named node, hop to a mid-chain candidate, start fresh)
- [ ] The briefing is generated from chain-engine queries only and does not include implementation details of the engine

**Dependencies:** chain-engine (R3, R4, R6, R9)

### R5: Verdict Emission From Experiment Results

**Description:** After running an experiment, an agent emits a verdict node whose values conform to the verdict taxonomy.

**Acceptance Criteria:**
- [ ] An emitted verdict node passes schema-registry validation against the built-in verdict schema
- [ ] An emitted verdict's state is exactly one of the five taxonomy values and any inconclusive form carries a numeric `N` between 0 and 100
- [ ] An emitted verdict carries `confidence`, `evidence_runs`, `contradicts`, and `supports` fields
- [ ] An invalid verdict emission is rejected with a structured error and does not modify the graph

**Dependencies:** chain-engine (R8 verdict taxonomy), schema-registry (R4 validation)

### R6: Benchmark Harness Extension

**Description:** A benchmark harness extends the predecessor project's harness with new chain-shaped metrics. The new metrics are measured per run.

**Acceptance Criteria:**
- [ ] The harness produces, per run, the metrics `longest_chain_length`, `avg_chain_depth`, `mvp_count`, `outcome_coverage`, and `chain_branching_factor`
- [ ] `outcome_coverage` is defined as the fraction of `bigger_outcome` nodes traceable to at least one `mvp` node and is reported as a number between 0.0 and 1.0
- [ ] Each metric value is recorded with a timestamp and the iteration number
- [ ] Re-running the harness on the same graph produces the same metric values (within documented tolerance for any seeded randomness)

**Dependencies:** chain-engine (R9 chain query API)

### R7: Driver Script

**Description:** A driver script orchestrates one or more loop iterations analogously to the predecessor project's driver.

**Acceptance Criteria:**
- [ ] A single command starts the driver and runs at least one full iteration end-to-end
- [ ] The driver exits with a non-zero status when any iteration fails to record metrics
- [ ] The driver writes a per-iteration summary to a documented location inside the project context directory
- [ ] The driver respects the configuration file's parameters without code changes

### R8: Drop-In Portability

**Description:** The skill is portable: dropping the project context directory into any repository should be sufficient to run the skill there.

**Acceptance Criteria:**
- [ ] A self-test runs the skill in a fresh empty repository where only the project context directory has been copied in, and the first iteration completes successfully
- [ ] No code path inside the skill assumes the repository name, host path, or any environment beyond an optional model selector
- [ ] Removing the project context directory from a repository removes all skill-managed state from that repository
- [ ] The skill's documentation states the portability contract and the self-test command

**Dependencies:** graph-core (R9 portability)

## Out of Scope

- Ollama-based agent dispatch — deferred to v2
- An in-memory database backend (sqlite or duckdb) for swarm-scale read-write — deferred
- Domain-specific verdict-judging logic beyond emitting taxonomy-conformant values — out of scope
- Modification of the existing autoresearch-create or autoresearch-finalize skills — explicitly forbidden
- Cross-repository or multi-project orchestration — out of scope

### R9: Agent Timeout and Healing Mechanism

**Description:** When an agent exceeds the configured timeout, a healer subagent is dispatched to assess the situation, collect partial results, and signal completion with an appropriate verdict state.

**Acceptance Criteria:**
- [ ] An agent process exceeding `agent_timeout_mins` is terminated with SIGTERM, then SIGKILL if unresponsive after 30 seconds
- [ ] A healer subagent dispatched on timeout receives the original task, elapsed time, and any partial output from the session directory
- [ ] The healer produces a verdict node with state `inconclusive_lean_proved:N` where N reflects the proportion of remaining work
- [ ] The iteration continues with remaining agents; partial results from timed-out agents are included in the manifest
- [ ] Timeout handling does not corrupt session state for other running agents

**Dependencies:** chain-engine (R8 verdict taxonomy), skill/R3 (parallel dispatch)

## Cross-References

- See also: cavekit-graph-core.md (R9 portability, R10 bootstrap)
- See also: cavekit-schema-registry.md (R4 validation, R8 built-in schemas)
- See also: cavekit-environment-indexers.md (invoked as part of the loop)
- See also: cavekit-chain-engine.md (R3, R4, R6, R7, R8, R9 — chain ranking, queries, taxonomy, configuration)
- See also: cavekit-renderers.md (selected per iteration to brief agents and humans)
- See also: cavekit-embeddings.md (optional similarity input for dispatch)
