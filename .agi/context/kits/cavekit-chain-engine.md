---
created: 2026-04-30
last_edited: 2026-04-30
---

# Cavekit: chain-engine

## Scope

The autoresearch-specific layer that sits on top of graph-core. It defines what a chain is, how chains are scored and selected, how agents join, fork, or hop between them, and what verdicts look like. It contains all the autoresearch semantics so graph-core can remain a generic substrate. Chains are virtual: they are computed from the underlying graph rather than stored as separate first-class objects.

## Requirements

### R1: Chain Definition

**Description:** A chain is an ordered path through the autoresearch node types: idea, hypothesis (one or more), experiment (one or more), verdict, mvp, outcome, bigger_outcome, app_purpose.

**Acceptance Criteria:**
- [ ] A chain is defined as an ordered sequence of node ids whose types appear in the documented order
- [ ] A chain may include multiple consecutive hypothesis or experiment nodes between an idea and a verdict
- [ ] A path that skips a required type (for example reaching mvp without an experiment) is not recognized as a chain
- [ ] Two chains may share any prefix, and shared-prefix chains are not deduplicated

**Dependencies:** schema-registry (R8 built-in schemas), graph-core (R1, R2)

### R2: Chains Are Virtual

**Description:** Chains are computed by traversing the graph; they are not stored as separate persistent records.

**Acceptance Criteria:**
- [ ] No chain object is written to disk as part of normal operation
- [ ] Adding a node that completes a new chain makes that chain queryable without a graph rebuild
- [ ] Removing a node that participated in a chain makes that chain disappear from queries on next traversal
- [ ] A chain query produces the same result whether or not earlier chain queries were run in the same session

### R3: Longest-Chain Attractor

**Description:** Among current chains, longer chains are preferred but not exclusive. Attractiveness is a weighted score and short chains may still be selected if their score is competitive.

**Acceptance Criteria:**
- [ ] When asked to rank chains, the engine returns them sorted by attractiveness with ties broken deterministically
- [ ] The longest chain is among the top-ranked results when no other factor dominates
- [ ] Short chains can rank above longer chains when their non-length scores are sufficiently higher
- [ ] The ranking function is pure: equal inputs produce equal outputs across runs

### R4: Mid-Chain Join

**Description:** An agent may attach to any node mid-chain rather than at the end. The probability of joining mid-chain is a tunable parameter.

**Acceptance Criteria:**
- [ ] A query for join candidates returns nodes from anywhere along candidate chains, not only chain tails
- [ ] The engine applies the configured mid-chain join probability when sampling a join target
- [ ] A minimum-chain-length parameter prevents joining chains shorter than the configured threshold
- [ ] Disabling mid-chain join (probability zero) produces only tail nodes as join candidates

### R5: Fork Mechanics

**Description:** Any node may have multiple children of the same type, allowing arbitrary forks.

**Acceptance Criteria:**
- [ ] Adding a second child of the same type to an existing parent does not raise an error
- [ ] After a fork, both child branches appear as candidates in subsequent chain queries
- [ ] Fork count per parent is reported in chain statistics
- [ ] Forks compound: a forked branch may itself fork without special handling

### R6: Attractiveness Function

**Description:** The score that ranks chains is a weighted combination of length, depth, recency, and mvp count.

**Acceptance Criteria:**
- [ ] The score is computed from exactly four documented inputs: chain length, chain depth, recency of the latest node, and count of mvp nodes reached
- [ ] Each weight is supplied through configuration, not hard-coded
- [ ] When all weights are zero, the function returns a stable constant rather than raising
- [ ] Two chains with identical inputs produce identical scores

### R7: Configuration File

**Description:** Tunable parameters live in a single chain-configuration file at a documented path inside the project context. The file declares the join, fork, fresh-start, idea-split, and weight parameters.

**Acceptance Criteria:**
- [ ] The configuration file declares the keys `chain_min_join_length`, `mid_chain_join_prob`, `fresh_start_prob`, `big_idea_vs_small_idea_split`, and `attractiveness_weights` with the four documented sub-keys (`length`, `depth`, `recency`, `mvp_count`)
- [ ] When the file is missing, documented defaults apply and a warning identifies the absent file
- [ ] When a key is missing or out of range, the engine raises a structured error naming the offending key
- [ ] Editing the file changes engine behavior on next run without code changes

### R8: Verdict Taxonomy

**Description:** A verdict is a finite-state value drawn from a closed taxonomy and accompanied by confidence, evidence, and cross-references to other verdicts.

**Acceptance Criteria:**
- [ ] A verdict's state is exactly one of `proved`, `disproved`, `inconclusive_lean_proved:N`, `inconclusive_lean_disproved:N`, or `pending`
- [ ] When the state is one of the inconclusive forms, the value `N` is an integer between 0 and 100 inclusive; otherwise no `N` is present
- [ ] A verdict carries a `confidence` value between 0.0 and 1.0 inclusive, an `evidence_runs` list of run identifiers, a `contradicts` list of verdict identifiers, and a `supports` list of verdict identifiers
- [ ] A verdict whose state or numeric ranges fall outside the taxonomy is rejected at insert time with a structured error

### R9: Chain Query API

**Description:** A documented set of queries over chains is available without requiring callers to traverse the graph by hand.

**Acceptance Criteria:**
- [ ] A `longest_n` query returns the top-N chains ranked by attractiveness with score and length
- [ ] A `branching_factor` query returns the average and per-node count of out-edges across chain participants
- [ ] A `mid_chain_candidates` query accepts a minimum chain length and a maximum recency and returns join targets matching both
- [ ] All chain queries are read-only and never mutate the graph

## Out of Scope

- Storage of nodes and edges — see graph-core
- Schema validation of frontmatter for autoresearch types — see schema-registry
- Visual rendering of chains — see renderers
- Vector embedding of chain participants — see embeddings
- Agent dispatch and per-iteration choice between extending, forking, hopping, or starting fresh — see autoresearch-tree-skill

## Cross-References

- See also: cavekit-graph-core.md (DAG substrate)
- See also: cavekit-schema-registry.md (R8 built-in autoresearch schemas)
- See also: cavekit-renderers.md (renders chains as multi-format views)
- See also: cavekit-embeddings.md (embeds nodes including chain participants)
- See also: cavekit-autoresearch-tree-skill.md (consumes chain queries to drive iterations)
