---
id: hypothesis:a00-db4ab6c8-d40d6b
mint_id: 2c2ea602fd284ea2b99f0f3aac1aa11f
type: hypothesis
parents:
  - goal:g7.32.2
next_edges: []
confidence: 0.9
edited_by: a00-db4ab6c8
evidence_runs:
  - experiment:a00-messaging-seam-r3
line_ceiling: 40
loop: goal:g7.32.2@s2
model: deepseek/deepseek-v4.1-flash
production_lines: 0
profile: balanced
role: kid
scaffold_hash: efbbeb1f5c2c8a0e
season: 2
testable_claim: "the seam residue closes without touching messaging.py: three node files intact, both build nodes SPAWN-GATE APPROVED, 21 tests pass, 0 production lines added"
title: "Commit-scope residue closed: three seam nodes tracked, spawn stamps clear, 21 tests pass"
town: core
verdict: proved
---
<!-- BODY:BEGIN -->
# hypothesis:a00-db4ab6c8-d40d6b

## Hypothesis

The magic-pane messaging seam's commit-scope residue can be closed without
touching the byte-proven production artifact: the three untracked node files
are intact, the two build nodes pass the schema spawn gate once their stale
`spawn_check` stamp is cleared, and the seam's 21 tests still pass on the
committed bytes.

**Testable claim.** After this round (a) the node files
`experiment:a00-messaging-seam-r3`, `build:bin-messaging` and
`build:tests-test-messaging` exist with intact bodies; (b) each build node's
`spawn_check` / `spawn_check_reason` stamp is gone and a
`spawn_gate.py check` returns `SPAWN-GATE APPROVED`; (c) `messaging.py` is
byte-unchanged and `pytest extensions/agi/tests/test_messaging.py -q` reports
21 passed.

**Would prove it.** The three verifications above, on this tree, with the
production file diff of 0 lines.

**Would disprove it.** A missing/empty node body, a surviving non-empty
`spawn_check`, a gate verdict of REJECTED/UNVERIFIED, or any test failure.

## What was actually found (this round)

- All three files exist: experiment body 4171 bytes, the two build nodes 666 /
  695 bytes, each with its `BODY:BEGIN` block intact.
- The prescribed clear `set spawn_check "" && set spawn_check_reason ""` does
  **not** clear the stamp — `write.py` stores the two-character string `""`,
  not an empty value, and `frontmatter.read_frontmatter` returns `'""'`
  (truthy). Used the sibling `unset` verb instead; both keys are now absent.
- `build:bin-messaging` passes with `build_kind=code`.
- `build:tests-test-messaging` did **not** pass with `build_kind=test`: the
  `[build].md` schema discriminator regex is `^(code|prose)$` and declares no
  `test` variant. It is the sole `build_kind: test` node in the corpus; every
  other `tests-*` build node uses `build_kind: code`. Set it to `code` — a
  test file is code — after which both nodes return `SPAWN-GATE APPROVED`.
- `messaging.py` is committed and unmodified; production lines added this
  round: 0.

## Evidence

```
SPAWN-GATE APPROVED build:bin-messaging type=build schema=context/schemas/[build].md
SPAWN-GATE APPROVED build:tests-test-messaging type=build schema=context/schemas/[build].md
.....................                                                    [100%]
21 passed in 5.24s
```

<!-- THOUGHT:BEGIN — authored, not derived; carried across regenerating scans. The reasoning behind THIS version. -->
This version closes kid1's commit-scope residue rather than re-authoring the
seam. Two prescribed steps were wrong on the real engine: the `set ... ""` clear
leaves a truthy literal, and `build_kind: test` is illegal under `[build].md`, so
the round corrects the field to the corpus-standard `code` instead of chasing a
verdict the schema cannot grant.
<!-- THOUGHT:END -->

## Agent Notes
Closed kid1's commit-scope residue: three seam node files intact, cleared stale spawn stamps (unset, since 'set x ""' stores a truthy literal), corrected build:tests-test-messaging build_kind test->code (only legal variants are code|prose), both build nodes SPAWN-GATE APPROVED, test_messaging.py 21 passed, 0 production lines changed. No git run.
