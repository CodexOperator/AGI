---
id: experiment:a00-e4a74ff1-789283
mint_id: 5d38b51e4cb449da801a38f265a9579c
type: experiment
parents:
  - hypothesis:the-agi-bin-shadow-guard-bites-at-the-path-driver-sh-resolves
next_edges: []
confidence: 0.85
edited_by: a00-15ec9a67
evidence_runs:
  - experiment:a00-e4a74ff1-789283
loop: hypothesis:the-agi-bin-shadow-guard-bites-at-the-path-driver-sh-resolves@s2
model: stealth/space-bunny-alpha
production_lines: 0
profile: balanced
role: kid
scaffold_hash: 1165714ccdd98a0d
season: 2
title: ship the shadow-fixture beside the guard test so the bite survives a clean checkout
town: core
verdict: proved
---
<!-- BODY:BEGIN -->
# experiment:a00-e4a74ff1-789283

## Experiment

What did you do? What happened? Include command/inputs and actual outputs.
# ship the fixture, not just the guard

Parent probe: kid 1's guard MECHANISM held but its WIRE was dead — the fixture
builder lived at `.agi/sessions/iter-DH.416/a00-729b9124/make_shadow_fixture.sh`,
a per-round scratch dir absent from any clean checkout, so 3 of 4 tests died
ENOENT. Fix = move the builder next to the test.

| change | where |
|---|---|
| new `make_shadow_fixture.sh` (finds `lib/find-root.sh` from `BASH_SOURCE`, no env var) | `extensions/agi/tests/fixtures/make_shadow_fixture.sh` |
| `FIXTURE = Path(__file__).parent/"fixtures"/...`; `AGI_PLUGIN_ROOT` env threading dropped; `import os` dropped | `extensions/agi/tests/test_agi_bin_absent.py` |

## Evidence
- in-repo: `pytest extensions/agi/tests/test_agi_bin_absent.py` -> 4 passed
- with neighbours: `test_agi_bin_absent.py test_locations.py test_snapshot_build_site.py` -> 96 passed
- clean-checkout simulation (copy of `extensions/agi` into a fresh tmp project with
  NO `.agi/sessions/` at all): 4 passed — the case that killed kid 1
- production lines over non-test paths: 0 (test files excluded from the ceiling)

## Verdict
The parent's testable claim now holds on bytes that ship: the guard asserts the
path `driver.sh:245,263-265` actually consults (`<project-root>/bin/` with
`project_root` = the graph dir), is shown RED on a fixture holding
snapshot-build-site.py / render-context.py, and is green once the shadow is gone.

## Agent Notes
shipped the shadow fixture as extensions/agi/tests/fixtures/make_shadow_fixture.sh; guard test now passes in a clean checkout (4 passed) and with neighbours (96 passed)

<!-- THOUGHT:BEGIN — authored, not derived; carried across regenerating scans. The reasoning behind THIS version. -->
Parent review a00-15ec9a67 (DH.416): ACCEPTED, claim accepted on bytes, not on the report. (1) What the instruction said: the shipped guard must bite in a clean checkout, so the fixture must ship with the test. (2) What the machine does: grep for "sessions" in test_agi_bin_absent.py and fixtures/make_shadow_fixture.sh returns NOTHING -- FIXTURE is now Path(__file__).parent/"fixtures"/"make_shadow_fixture.sh" (test file lines 36-40), and the builder locates lib/find-root.sh from BASH_SOURCE, so no env var and no absolute path is threaded. Measured by me, not by the kid: copying extensions/ into /tmp/clone2 with a .agi/config.json and NO .agi/sessions at all, `pytest extensions/agi/tests/test_agi_bin_absent.py` = 4 passed; with test_locations + test_snapshot_build_site = 96 passed; the gate probe guard(<tmp>/proj/.agi) with an executable render-context.py planted by the in-tree builder raises AssertionError naming the file. (3) The near miss this closes: leaving the builder in the round scratch dir satisfies "the fixture resolves PROJECT_ROOT by sourcing find-root.sh" and loses everything else -- kid 1 passed its own suite in its own worktree and shipped a guard that dies ENOENT the moment the session dir is gone. (4) No standing rule deviated. caveat recorded: the guard uses .exists() where driver.sh:245-265 uses -x, so a non-executable bin/snapshot-build-site.py turns the guard red although driver.sh would ignore it (probe C, measured) -- fail-closed, deliberate, noted not fixed. probes: gate=refusal by name on a real resolved <project-root>/bin/ shadow; wire=clean checkout with no .agi/sessions, 4 passed.
<!-- THOUGHT:END -->
