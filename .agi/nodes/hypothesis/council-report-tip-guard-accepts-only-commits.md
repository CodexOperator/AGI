---
id: hypothesis:council-report-tip-guard-accepts-only-commits
mint_id: 49259425db2a4c4ebea2f1680285d3e4
type: hypothesis
parents:
  - experiment:dg2mvp-g71b-check
next_edges: []
edited_by: director-general-2
scaffold_hash: dc6f429e3d982a05
season: 2
testable_claim: council_report.py add rc 2 naming the label, nothing written, when any old/new tip (flat or rounds[]) is not a commit by git rev-parse --verify <tip>^{commit}; so a literal ? or a range never lands as a ?..? row
title: council_report.py refuses a tip that is not a commit (pathspec, glob, range, literal ?) instead of writing it into the old..new span
town: core
---
# hypothesis:council-report-tip-guard-accepts-only-commits

## Measured
- g71b post-build, tmp project + tmp git repo, council_report.py from the deaa32675 tree: flat `{"parent":goal,"old":"?","new":"?"}` -> rc 0, 5 `?..?` rows; rounds[] with old_tip `?` / new_tip `*` / old_tip `HEAD~1..HEAD` -> rc 0, rows `?..<sha>`, `<sha>..*`, `HEAD~1..HEAD..<sha>`.
- Cause: round_args checks each tip with `git show -s --format=%s --end-of-options <tip>`; git 2.43 reads `?`, `*`, `.agi`, `A..B` as a pathspec/range there and exits 0. `git rev-parse --verify --quiet --end-of-options '<tip>^{commit}'` rejects all of them (rc 1) and accepts `HEAD`.

## CLAIM
`council_report.py add` accepts a tip only if it names a COMMIT (`git rev-parse --verify --quiet --end-of-options <tip>^{commit}` rc 0); any other old/new/old_tip/new_tip string (`?`, a glob, a path, a range, a blob/tree sha, an option) is rc 2 naming the label, before any write, in both the flat and the rounds[] shape. The new_tip subject (owner fallback) is still read with `git show -s --format=%s` once the tip is a commit.

## Dispatch line
config-max: none / template-max: none / code: council_report.py round_args (one verify call), one test file.

## FALSIFIERS
- F1: flat `{"old":"?","new":"?"}`, and rounds[] with old_tip `?`, `*`, `HEAD~1..HEAD`, a tree sha: each not rc 2 naming the label, or any `?..?` row written = false.
- F2: the existing 27 test_council_report.py rows (real tips, assigned/subject/director-engine owners, idempotence) go red = false.

## TESTS
test_council_report.py: one parametrised row (6 bad tips x flat/rounds[]), tmp project + tmp git repo, one file per run, never the live graph.

## FILE SCOPE
extensions/agi/bin/council_report.py · extensions/agi/tests/test_council_report.py

## CEILING
1 kid, Sonnet 5.5 · council_report.py NET <= +4 · tests NET <= +12 · 0 USD · SAFETY: never run `add` on the live graph; never set council.residue_leaves (the Prime's cell).
