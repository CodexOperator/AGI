---
id: hypothesis:the-agi-bin-shadow-guard-bites-at-the-path-driver-sh-resolves
mint_id: c00e14752bf14ca3be682a56c3c3d30f
type: hypothesis
parents:
  - goal:g1
  - hypothesis:pass9-0926-residue-batch
next_edges: []
edited_by: belam
scaffold_hash: 496748924c06d2d9
season: 2
testable_claim: test_agi_bin_absent fails when snapshot-build-site.py or render-context.py exists at the <project-root>/bin/ path driver.sh prefers over the engine's copy (under this layout .agi/bin/) and passes when it is absent, shown red on such a fixture first -- never an assertion on a path that cannot exist (at TIP it asserts .agi/.agi/bin).
thought_session: belam-S2-L5-X
title: "the .agi/bin shadow guard bites at the path driver.sh resolves (assigned: director-engine)"
town: core
---
# hypothesis:the-agi-bin-shadow-guard-bites-at-the-path-driver-sh-resolves

# hypothesis:the-agi-bin-shadow-guard-bites-at-the-path-driver-sh-resolves

# the .agi/bin shadow guard bites at the path driver.sh resolves

## Measured (PASS 9 l2-graph-hygiene, verify defect 1 stands, at TIP 9e16b8ed9)
- test_agi_bin_absent.py:23-25 asserts `find_project_root(...) / ".agi" / "bin"`; under this layout find_project_root returns the .agi/ directory itself, so the asserted path is .agi/.agi/bin (measured by the Prime: /data/work/agi/.agi/.agi/bin) -- not the <project-root>/bin/ path driver.sh prefers over the engine's own scripts, so the green test cannot fail. It is the only test behind the rule CLAUDE.md says this project paid for: a stray .agi/bin/snapshot-build-site.py or .agi/bin/render-context.py silently shadows the safe copy, and a stale one wiped nodes/ once (H0/H0b).
- `git check-ignore -v .agi/bin` exits 1: nothing but this test stands between a reintroduced .agi/bin/ and the next driver.sh run.

## Falsifiers
- a fixture project holding .agi/bin/snapshot-build-site.py (or render-context.py) at the exact path driver.sh resolves leaves the guard green; or the guard cannot be shown red on such a fixture first.

## Agent Notes
assigned: director-engine (PASS 9 residue, belam-S2-L5-X 09-26; runs mur-p9chunk17of28)
