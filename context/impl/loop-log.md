---
created: "2026-05-04"
last_edited: "2026-05-04"
---

# Loop Log

Build site: /home/ubuntu/autoresearch-tree/context/plans/build-site.md

### Iteration 1 — 2026-05-04 (Tier 0 baselines + setup)

- T-001: pytest baseline — DONE. Files: `context/refs/pytest-baseline-prefold.md`. 166 pass / 1 known fail. Build P, Tests baseline-only.
- T-002: gh auth — DONE. CodexOperator authenticated.
- T-003: agi-unification branch — DONE. Created in `~/.hermes/agi/` from master `3d550de`.
- T-004: agi-tree remote — DONE. origin → CodexOperator/agi-tree. NOT pushed. Dirty tree flagged.
- T-005: commit style — DONE. Files: `context/refs/commit-style-conventions.md`. agi freeform, ar-tree prefixed.
- T-006: legacy prestate — DONE. Files: `context/refs/legacy-prestate.md`. ar-tree dir+repo unarchived.
- Tier 0 status: 6/6 DONE. Risks flagged: dirty agi-tree, master vs main, pytest count discrepancy.
- Next: Tier 1 frontier — T-007 (subtree merge, depends T-003+T-005).
