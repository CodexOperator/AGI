---
id: hyp:a01-7031af17-449ecb
mint_id: a2f2765bcca64ff3b993d3f4ae29d4aa
type: hypothesis
parents:
  - idea:domain-graph-core
next_edges:
  - verdict:a01-7031af17-449ecb-r11
  - mvp:a01-7031af17-449ecb-r11
confidence: 0.95
edited_by: season.py
season: 1
subgraph: false
tags:
  - graph-core
  - R11
testable_claim: Path Safety and Project-Root Sandboxing
thought_session: season
title: "graph-core/R11: Path Safety and Project-Root Sandboxing"
---
## Hypothesis

The `PathValidator` in `src/graph_core/paths.py` provides correct project-root sandboxing for all graph-core file-system operations. The PathValidator class itself is correct (rejects escapes, accepts valid paths), but it is NOT wired into the `load_directory` function — the loader reads files without sandboxing. This gap means a malicious or misconfigured node file could reference paths outside the project root.

**What would prove it:** Loader calls `safe_path()` or equivalent before opening files; a `payload_ref` pointing outside the project root raises `PathOutsideProjectError` at load time.

**What would disprove it:** (a) PathValidator methods reject valid paths or accept escape paths; (b) loader does not use PathValidator — file reads proceed without validation.

## Acceptance Criteria

- [x] `PathValidator.validate("../escape")` raises `PathOutsideProjectError` ✅
- [x] `PathValidator.validate("./nodes/idea/test.md")` returns resolved path without error ✅
- [x] `PathValidator.validate_relative("/absolute/path")` raises `PathOutsideProjectError` ✅
- [x] `PathValidator.validate_relative("subdir/node.md")` returns resolved path without error ✅
- [x] `safe_path()` module function delegates to PathValidator correctly ✅
- [ ] Loader calls safe_path() before opening a file ❌ — **NOT wired in**
- [ ] A node with `payload_ref: "../../etc/passwd"` raises `PathOutsideProjectError` ❌ — **NOT enforced**

## Result

**verdict: inconclusive_lean_disproved:35**

PathValidator class is correct (5/7 criteria pass). Criteria 6-7 fail: loader does NOT call `safe_path()`. A `payload_ref` pointing outside the project root is silently accepted.

**Fix needed:** Add `safe_path(p)` call in `load_node_file()` or `load_directory()` before each file open operation.

## Dependencies

- `graph-core/R4` (frontmatter file persistence must work for `payload_ref` to be readable)
- `graph-core/R6` (directory walking must be implemented for loader to use the validator)