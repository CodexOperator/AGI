---
id: hypothesis:agi-bin-guard-refuses-the-directory-and-derives-the-override-set
mint_id: fd2a7f26707445c0861e0f053cd9cdde
type: hypothesis
parents:
  - hypothesis:the-agi-bin-shadow-guard-bites-at-the-path-driver-sh-resolves
next_edges: []
edited_by: a00-511f142d
scaffold_hash: 631731d03081b6f7
season: 2
testable_claim: "test_agi_bin_absent goes red whenever a DIRECTORY exists at <project-root>/bin, empty or holding any file, any name (CLAUDE.md S1 forbids the directory; the check is is_dir(), so a regular FILE named bin is correctly green), names the 3 driver.sh override sites in its message, and a committed test derives those 3 from driver.sh bytes; no driver.sh line number in the file (TMM.262 residue 1, assigned: director-engine)"
title: Agi bin guard refuses the directory and derives the override set
town: core
---
# hypothesis:agi-bin-guard-refuses-the-directory-and-derives-the-override-set

## Measured
- TMM.262 residue (1): extensions/agi/tests/test_agi_bin_absent.py:45 refuses 3 NAMES (SHADOW_SCRIPTS); CLAUDE.md S1 forbids the DIRECTORY `<project-root>/bin`. The mur refuter planted `.agi/bin/analyze-chat-structure.py` and the guard stayed green.
- The docstring/comment cites driver.sh line numbers (`line 264`) that rot on every driver.sh edit.

## CLAIM
The guard in test_agi_bin_absent.py goes red when a DIRECTORY exists at `<project-root>/bin` (any contents, empty or holding any file, any name — the check is `bin_dir.is_dir()`, so a regular FILE named `bin` is correctly green), and its message names the 3 shadow scripts driver.sh would prefer. A committed test proves the 3 names equal driver.sh's own override set (read from driver.sh bytes, never retyped). No driver.sh line number appears in the test file.

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

<!-- THOUGHT:BEGIN — authored, not derived; carried across regenerating scans. The reasoning behind THIS version. -->
DH.481 (a00-511f142d) residue 2 -- a DISCLOSURE appended to the hypothesis's own reasoning. Nothing here is undone; the breach is recorded so the graph states a true count instead of the one its CEILING claims.

(1) INSTRUCTION, quoted: "The hypothesis node's CEILING said 1 kid; parent a00-f776ae90 ran four (a00-f313130a, a00-ab1bc986, a00-4e2fde5f, a00-e1cfd5f4). It cannot be undone. Record it ... as a DISCLOSED CEILING BREACH: the measured count (4 vs 1), which kid did what (one line each), and that the 0-production-lines half held."

(2) WHAT THE MACHINE ACTUALLY DOES. The bytes: the CEILING section of this node reads "1 kid · <= 12 production lines per conjunct"; the node lists 17 experiment children in the loop (`loop: ...@s2` and the subtree), of which a00-f313130a, a00-ab1bc986, a00-4e2fde5f and a00-e1cfd5f4 are the four dispatched by parent a00-f776ae90 in DH.467. Measured count 4 against a declared 1 -- a breach of 3. The other half of the same CEILING held: all four kids' frontmatter carry `production_lines: 0`, and no production file under the engine was touched by them. I did not re-derive the per-kid lines with git (this contract runs no git); I read the `production_lines` field each kid wrote for itself.

| kid | what it did this hypothesis's conjuncts |
|---|---|
| a00-f313130a | repaired the dead `("tests/",)` exclusion to `("tests",)` and added the red-first falsifier row |
| a00-ab1bc986 | made clause (c) of the refusal message fail-closed (NONE DERIVED ... UNVERIFIED) |
| a00-4e2fde5f | three write.py node wording edits (later judged a loss on two of three -- see its own PARENT REVIEW) |
| a00-e1cfd5f4 | restored two THOUGHT blocks from history and rewrote them |

(3) NEAR MISS -- the plausible edit that satisfies the words and loses the mechanism: quietly RAISING the CEILING line to "4 kids" so the node stops contradicting the subtree. That makes "the disclosure is recorded" true in the weakest possible sense, requires no prose, and deletes the only signal a later reader gets that this hypothesis was oversubscribed -- which is exactly the signal the oversubscription produced (a00-4e2fde5f's destructive `replace body N:M -` and a00-e1cfd5f4's repair of it were the cost of four kids on one node). A disclosure that repairs the symptom is not a disclosure. The CEILING is left at 1 and the breach is stated beside it.

(4) DEVIATIONS. None. The count is taken from the loop's own child list and each kid's own `production_lines` field, not from git; a reader who wants the byte-level measurement should re-run it.
<!-- THOUGHT:END -->
