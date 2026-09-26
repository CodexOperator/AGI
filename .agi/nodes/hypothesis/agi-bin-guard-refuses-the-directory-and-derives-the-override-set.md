---
id: hypothesis:agi-bin-guard-refuses-the-directory-and-derives-the-override-set
mint_id: fd2a7f26707445c0861e0f053cd9cdde
type: hypothesis
parents:
  - hypothesis:the-agi-bin-shadow-guard-bites-at-the-path-driver-sh-resolves
next_edges: []
edited_by: director-engine
scaffold_hash: 631731d03081b6f7
season: 2
testable_claim: "test_agi_bin_absent goes red on ANY file under <project-root>/bin (CLAUDE.md S1 forbids the directory), names the 3 driver.sh override scripts in its message, and a committed test derives those 3 from driver.sh bytes; no driver.sh line number in the file (TMM.262 residue 1, assigned: director-engine)"
title: Agi bin guard refuses the directory and derives the override set
town: core
---
# hypothesis:agi-bin-guard-refuses-the-directory-and-derives-the-override-set

## Measured
- TMM.262 residue (1): extensions/agi/tests/test_agi_bin_absent.py:45 refuses 3 NAMES (SHADOW_SCRIPTS); CLAUDE.md S1 forbids the DIRECTORY `<project-root>/bin`. The mur refuter planted `.agi/bin/analyze-chat-structure.py` and the guard stayed green.
- The docstring/comment cites driver.sh line numbers (`line 264`) that rot on every driver.sh edit.

## CLAIM
The guard in test_agi_bin_absent.py goes red when `<project-root>/bin` EXISTS at all (any file, any name), and its message names the 3 shadow scripts driver.sh would prefer. A committed test proves the 3 names equal driver.sh's own override set (read from driver.sh bytes, never retyped). No driver.sh line number appears in the test file.

## Dispatch line
config-max: none (the 3 names are driver.sh's; the test DERIVES them from driver.sh, never a new cell) / template-max: none / code: the directory assertion + the derivation test.

## FALSIFIERS
- a fixture with `<root>/bin/anything.py` (not one of the 3) and the guard green;
- the override-set test passes with a name removed from driver.sh;
- `grep -n 'line [0-9]' test_agi_bin_absent.py` hits.

## TESTS
extensions/agi/tests/test_agi_bin_absent.py (+ neighbourhood test_bin_help_smoke.py). Red-first: plant `bin/other.py` in the tmp fixture, show green before, red after.

## FILE SCOPE
extensions/agi/tests/test_agi_bin_absent.py · extensions/agi/tests/fixtures/make_shadow_fixture.sh (only if the fixture must plant the extra file). Nothing else.

## CEILING
1 kid · <= 12 production lines per conjunct · pi parents (tier-0) · 0 USD. Every test that spawns python/pytest runs under `timeout` + a process cap; never a pytest that can re-collect its own dir; kids never launch real claude.

## Agent Notes
DIRECTOR DH.428 (corrective, mur-director-engine-3 DH.425 residues 1-4): the dead SHADOW_SCRIPTS constant goes; RULING -- the guard is red when <project-root>/bin EXISTS at all (S1 forbids the directory; the fixture makes bin/ only to plant); the line-citation guard also catches the colon form; the message states exactly what is checked. DH.428 merges the DH.425 loop branch first and is reviewed as one branch.
