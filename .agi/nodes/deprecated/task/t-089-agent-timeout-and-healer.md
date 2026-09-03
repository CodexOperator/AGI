---
id: task:t-089
mint_id: a46e1855de464277a5d2ba81175cfb78
type: task
parents:
  - hyp:autoresearch-tree-skill-r9
acceptance_criteria:
  - R9.1 (agent process exceeding agent_timeout_mins terminated with SIGTERM
  - then SIGKILL if unresponsive after 30s)
  - {"R9.2 (healer subagent dispatched on timeout receives": "original task"}
  - elapsed time
  - partial output from session dir)
blocked_by:
  - task:t-078
  - task:t-081
cavekit_req: autoresearch-tree-skill/R9
edited_by: l1.09-execution-parent
effort: M
origin: build-site
status: deprecated
tags:
  - M
  - tier--1
thought_session: L1.09
tier: "-1"
title: "T-089: Agent timeout and healer dispatch mechanism"
---
**Description:** Implement heal.py monitoring agent PIDs, graceful termination (SIGTERM → SIGKILL), healer subagent dispatch with partial output context, and verdict emission with calibrated confidence. Partial results from timed-out agents flow into manifest.json alongside successful agents.

**Files:** `extensions/autoresearch-tree/bin/heal.py`, `extensions/autoresearch-tree/lib/agent-prompt.md`

**Test Strategy:** Mock agent processes that sleep beyond timeout; assert heal.py dispatches healer and produces partial manifest entry with inconclusive_lean_proved:N verdict.

- T-001: Generic node primitive structure → graph-core/R1

- T-003: Generic edge primitive → graph-core/R2 (depends only on T-001 → moved to Tier 1)

- T-001: Generic node primitive structure

- T-088: Skill repository scaffolding

- T-002: Node parent/child invariant guards (blockedBy: T-001)

- T-003: Generic edge primitive (blockedBy: T-001)

- T-005: Identity scheme (blockedBy: T-001)

- T-006: Node file frontmatter persistence (blockedBy: T-001)

- T-004: Graph DAG insertion with cycle rejection (blockedBy: T-002, T-003)

- T-007: Lazy body loading (blockedBy: T-006)

- T-008: Frontmatter error isolation (blockedBy: T-006)

- T-019: Schema as file with naming convention (blockedBy: T-006)

- T-060: Shared internal representation (blockedBy: T-001, T-003)

- T-069: Per-node Node2Vec vector generation (blockedBy: T-001, T-003)

- T-009: Recursive node bodies (blockedBy: T-007, T-004)

- T-011: Directory-walking loader (blockedBy: T-006, T-005)

- T-020: Schema removal handling (blockedBy: T-090)

- T-021: Bracket convention for active schemas (blockedBy: T-090)

- T-061: ASCII renderer — bounded 200x200 (blockedBy: T-060)

- T-063: Mermaid renderer (blockedBy: T-060)

- T-065: Git-diff renderer (blockedBy: T-060)

- T-070: UMAP projection to 2D (blockedBy: T-069)

- T-073: Similarity query API (blockedBy: T-069)

- T-010: Uniform renderer input contract (blockedBy: T-009)

- T-013: Warm-load cache (blockedBy: T-011)

- T-015: Pluggable persistence backend contract (blockedBy: T-006, T-011)

- T-022: Schemas as meta_node (blockedBy: T-021, T-001, T-005)

- T-024: Optional validation hook engine (blockedBy: T-021)

- T-025: Cascade step 1 — bracket name match (blockedBy: T-021)

- T-026: Cascade step 2 — fingerprint similarity (blockedBy: T-025)

- T-028: Pluggable LM hook (blockedBy: T-021)

- T-062: ASCII renderer — type counts and edge summary (blockedBy: T-061)

- T-064: Git-tree renderer (blockedBy: T-060, T-049 → moves later; revised)

- T-014: Cache state lives under context dir (blockedBy: T-013)

- T-023: Validating edges from meta-nodes (blockedBy: T-022, T-003)

- T-027: Cascade step 3 — LM fallback (blockedBy: T-026, T-028)

- T-031: Built-in schemas for autoresearch types (blockedBy: T-021, T-024, T-018)

- T-067: Renderer plugin contract (blockedBy: T-061, T-063, T-064, T-065)

- T-072: Cache invalidation on graph change (blockedBy: T-069, T-013)

- T-012: Subdirectory→subgraph type resolution (blockedBy: T-011, T-019, T-020)

- T-016: Portability contract (blockedBy: T-014, T-015)

- T-029: Cascade step 4 — generic fallback (blockedBy: T-027)

- T-030: Generated schemas land inactive (blockedBy: T-027)

- T-047: Chain definition (blockedBy: T-031, T-004)

- T-053: Chain configuration file (blockedBy: T-018)

- T-054: Verdict taxonomy state validation (blockedBy: T-031)

- T-068: Pure-function guarantees (blockedBy: T-067)

- T-074: Scatter rendering plugin (blockedBy: T-067, T-070)

- T-075: Optional in-graph embedding storage (blockedBy: T-072, T-006)

- T-017: Portability self-test command (blockedBy: T-016)

- T-018: Bootstrap command (blockedBy: T-016)

- T-032: Indexer invocation command (blockedBy: T-018, T-019)

- T-048: Chains are virtual (blockedBy: T-047)

- T-051: Fork mechanics (blockedBy: T-047)

- T-052: Attractiveness function (blockedBy: T-053)

- T-055: Verdict supporting fields (blockedBy: T-054)

- T-066: Recursive rendering (blockedBy: T-061, T-063, T-064, T-065, T-009)

- T-071: Coordinate isomorphism (blockedBy: T-070, T-060)

- T-033: Filesystem tree indexer (blockedBy: T-032, T-031, T-005)

- T-034: Code symbol indexer — node emission (blockedBy: T-032, T-031)

- T-037: Python dependency indexer — packages (blockedBy: T-032, T-031)

- T-039: API dependency indexer — endpoints (blockedBy: T-032, T-031)

- T-041: Container observation indexer (blockedBy: T-032, T-031)

- T-049: Longest-chain attractor + ranking (blockedBy: T-047, T-052)

- T-077: Big-idea-vs-small-idea decision (blockedBy: T-053)

- T-035: Code symbol indexer — call edges (blockedBy: T-034)

- T-040: API dependency indexer — schema reuse edges (blockedBy: T-039)

- T-050: Mid-chain join candidate sampling (blockedBy: T-049, T-053)

- T-064: Git-tree renderer (blockedBy: T-060, T-049)

- T-078: Parallel Claude builder dispatch (blockedBy: T-077)

- T-036: Code symbol indexer — warm-load + upgrade markers (blockedBy: T-035, T-013)

- T-038: Python dependency indexer — internal-import edges (blockedBy: T-037, T-034)

- T-056: longest_n chain query (blockedBy: T-049)

- T-057: branching_factor query (blockedBy: T-051)

- T-058: mid_chain_candidates query (blockedBy: T-050)

- T-081: Verdict emission with validation (blockedBy: T-031, T-024, T-054, T-055)

- T-042: One-file-per-indexer layout (blockedBy: T-033, T-034, T-037, T-039, T-041)

- T-043: Per-path result caching (blockedBy: T-032, T-013)

- T-059: All chain queries are read-only (blockedBy: T-056, T-057, T-058)

- T-079: Per-agent briefing — chain stats (blockedBy: T-049, T-051, T-052, T-056)

- T-082: Benchmark harness — metrics (blockedBy: T-056, T-057)

- T-044: Per-indexer documentation (blockedBy: T-042)

- T-080: Per-agent briefing — actions (blockedBy: T-079, T-058)

- T-083: outcome_coverage definition (blockedBy: T-082)

- T-084: bench timestamps + iteration recording (blockedBy: T-082)

- T-045: Upgrade markers grep-discoverable (blockedBy: T-044)

- T-085: Driver script — single iteration (blockedBy: T-077, T-078, T-080, T-081, T-084)

- T-046: Indexer documentation self-check (blockedBy: T-045)

- T-086: Driver — error handling and summary (blockedBy: T-085)

- T-087: Skill drop-in portability self-test (blockedBy: T-086, T-017)

- T-076: Skill installation in forked skill repository (blockedBy: T-088, T-087 — see correction below)

- T-001: Generic node primitive structure → graph-core/R1

- T-088: Skill repository scaffolding → autoresearch-tree-skill/R1 (structural prep)

- The predecessor at `/home/ubuntu/.hermes/agi/` is FROZEN. Read `agi/graph_builder.py` only for inspiration on warm-load `lru_cache` patterns and gitnexus-port lessons; re-implement under the schema-registry contracts defined here.

- Every node payload field beyond the seven in T-001 belongs to a schema, not graph-core.

- No task crosses kit boundaries beyond the explicit `Dependencies:` declared in each kit; the tier ordering enforces this.

- Tasks marked `[CONDITIONAL]` or `[DYNAMIC]` are not present in this plan; all 88 tasks have determinate scope.

- Tier 3 widths (9 tasks) and Tier 4 widths (9 tasks) are the prime parallelization opportunities; the 5-builder pool can pull continuously from those tiers.

<!-- THOUGHT:BEGIN — authored, not derived; carried across regenerating scans. The reasoning behind THIS version. -->
Deprecated 2026-09-03 in L1.09 per the build-site survey (`.agi/sessions/L1.09-mining/report.md` §E); task `autoresearch-tree-skill/R9` under `hyp:autoresearch-tree-skill-r9`, whose disposition is disposition CLOSE-BY-CITATION -- closed by `verdict:autoresearch-tree-skill-r9-by-citation` citing `build:bin-heal`: `heal.py` is SIGTERM-then-SIGKILL-after-grace, healer dispatch on hung agents, manifest-based partial results -- a strong match; the build-site's own `verdict:autoresearch-tree-skill-r1` is hollow and is not cited (§F R1).
<!-- THOUGHT:END -->
