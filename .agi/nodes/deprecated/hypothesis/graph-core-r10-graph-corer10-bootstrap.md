---
id: hyp:graph-core-r10
mint_id: 3721a5b0b1ad481888ad4e54c3864a1f
type: hypothesis
parents:
  - idea:domain-graph-core
confidence: 0.5
edited_by: l1.09-execution-parent
origin: build-site
status: deprecated
subgraph: false
tags:
  - graph-core
  - R10
testable_claim: Bootstrap Command
thought_session: L1.09
title: "graph-core/R10: Bootstrap Command"
---
**Description:** A command initializes a new project so a fresh directory becomes a valid graph root.

**Acceptance Criteria:**
- [ ] Running the bootstrap command in an empty directory produces a `context/` skeleton with subdirectories for schemas, kits, and node storage
- [ ] Running the bootstrap command twice on the same directory is a no-op and does not overwrite existing files
- [ ] The skeleton includes a minimal example node and a minimal example schema sufficient to load a one-node graph
- [ ] The bootstrap reports the created paths to the user in a single summary

<!-- THOUGHT:BEGIN — authored, not derived; carried across regenerating scans. The reasoning behind THIS version. -->
Deprecated 2026-09-03 in L1.09 per the build-site survey (`.agi/sessions/L1.09-mining/report.md` §C/§E); disposition GENUINELY-OPEN, not run: no `bootstrap.py` or CLI subcommand exists; `agi`'s real bootstrap story is `QUICKSTART.md` plus the `init`/scaffolding half `goal:g1.5` still owes, not this generic-library command -- noted on `goal:g1.5`.
<!-- THOUGHT:END -->
