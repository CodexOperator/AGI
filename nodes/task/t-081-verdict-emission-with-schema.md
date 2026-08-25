---
acceptance_criteria:
  - R5.1 (emitted verdict node passes schema-registry validation against built-in verdict schema)
  - R5.2 (state ∈ five taxonomy values
  - inconclusive carries N ∈ [0
  - 100])
  - R5.3 (carries confidence/evidence_runs/contradicts/supports)
blocked_by:
  - task:t-031
  - task:t-024
  - task:t-054
  - task:t-055
cavekit_req: autoresearch-tree-skill/R5
effort: M
id: "task:t-081"
mint_id: d3ca272ed79c44b390d16dd1016ae322
origin: build-site
parents:
  - hyp:autoresearch-tree-skill-r5
status: pending
tags:
  - M
  - tier--1
tier: -1
title: "T-081: Verdict emission with schema-registry validation"
type: task
---

**Description:** Implement `emit_verdict(payload)` that runs through schema-registry validation and verdict-taxonomy validation before insertion. On rejection, raise `VerdictRejectedError(payload, reason)`; do not insert.

**Files:** `agi-tree/src/skill/verdict_emit.py`, `agi-tree/tests/skill/test_verdict_emit.py`

**Test Strategy:** Tests for valid emission, each rejection path, and graph-snapshot equality on rejection.
