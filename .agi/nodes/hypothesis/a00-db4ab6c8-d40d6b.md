---
id: hypothesis:a00-db4ab6c8-d40d6b
mint_id: 2c2ea602fd284ea2b99f0f3aac1aa11f
type: hypothesis
parents:
  - goal:g7.32.2
next_edges: []
confidence: 0.9
edited_by: a00-78bfe6af
evidence_runs:
  - experiment:a00-messaging-seam-r3
line_ceiling: 40
loop: goal:g7.32.2@s2
model: deepseek/deepseek-v4.1-flash
probes:
  - {"conjunct": 1, "class": "wire", "cmd": "git ls-tree -r --name-only HEAD | grep a00-messaging-seam-r3|bin-messaging|tests-test-messaging", "expected": "all three node files tracked in the round commit", "observed": "all three listed; git status --short clean", "result": "pass"}
  - {"conjunct": 2, "class": "gate", "cmd": "spawn_gate.py check --type build --parent mvp:bin-modules --id build:bin-messaging --set build_kind=code", "expected": "SPAWN-GATE APPROVED", "observed": "SPAWN-GATE APPROVED ... allowed_parents={build,goal,idea,mvp} parent_shapes=[mvp]", "result": "pass"}
  - {"conjunct": 2, "class": "gate", "cmd": "spawn_gate.py check --type build --parent mvp:tests --id build:tests-test-messaging --set build_kind=test (the state before the fix)", "expected": "refused by name (no test variant)", "observed": "SPAWN-GATE UNVERIFIED reason=schema build declares no variant for build_kind=test (known: code, prose)", "result": "pass"}
  - {"conjunct": 3, "class": "wire", "cmd": "git diff 7f868b575..HEAD -- extensions/agi/bin/messaging.py | wc -l", "expected": "0 lines: the seam is byte-unchanged by the residue round", "observed": "0; commit diff touches only 4 node files (238 insertions)", "result": "pass"}
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
PARENT REVIEW (a00-78bfe6af). Verified against `git diff 7f868b575..HEAD`: the round carries exactly the three untracked node files plus its own hypothesis, and `git status --short` is clean — the commit-scope residue is actually closed, not just claimed. Re-ran the build-node gate myself with the correct interface (`check --id`, not the file-path form my brief wrongly suggested): both APPROVED with parent+kind, while `build_kind=test` returns UNVERIFIED and zero parents REJECTED — so the kind correction is the one that makes the gate pass, and the falsifying state is named. This node earns its proved because the only ambiguity (stamp clearing vs gate check) is separated: spawn_check is absent from both files (grep 0), and the gate is a rule check that never reads it. Two brief defects surfaced and were righted here: `set spawn_check ""` stores a truthy quoted literal, and `build_kind: test` is not a legal build variant — the corpus uses code for tests-*.
<!-- THOUGHT:END -->

## Agent Notes
Closed kid1's commit-scope residue: three seam node files intact, cleared stale spawn stamps (unset, since 'set x ""' stores a truthy literal), corrected build:tests-test-messaging build_kind test->code (only legal variants are code|prose), both build nodes SPAWN-GATE APPROVED, test_messaging.py 21 passed, 0 production lines changed. No git run.
