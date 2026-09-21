---
created: "2026-05-04"
last_edited: "2026-05-04"
---

# Pytest Baseline — Pre-Fold

Captured for cavekit-loop-continuity R1 (post-fold pytest must not regress against this baseline).

## Command

```
cd /home/ubuntu/autoresearch-tree && pytest extensions/autoresearch-tree/tests/ -q --tb=no -p no:cacheprovider
```

## Result (2026-05-04)

```
1 failed, 166 passed in 0.38s
```

- **Total tests collected:** 167
- **Passing:** 166
- **Failing (known, pre-existing):** 1 — `extensions/autoresearch-tree/tests/graph_core/test_node.py::test_field_set_is_exactly_six`

## Baseline Acceptance Criteria for R1

Post-fold pytest run must satisfy:
- Passing count ≥ 166
- Failing count ≤ 1 (and the one failure must be the same `test_field_set_is_exactly_six` test or fewer; no new regressions)
- No new skips or xfails introduced by the fold

## Note on prior handoff discrepancy

`~/.hermes/HANDOFF-autoresearch-2026-05-01.md` line 9 reports "274 tests still pass" after iter 37. Current baseline is 167 collected. Difference likely due to:
- Different test config (pytest collection flags, conftest path)
- Tests added/removed in iter 38+ (no handoff for that work)
- Possible separate test suite in another path not captured here

The baseline captured here is the operative one for R1 verification.
