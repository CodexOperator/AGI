---
id: hypothesis:every-in-place-log-trim-refuses-a-non-append-holder
mint_id: 81d6a1fdcae44bd2a63ff9e0b3b0eab0
type: hypothesis
parents:
  - hypothesis:crons-log-cap-bounds-archives-and-prunes-only-its-own-files
  - goal:g6.49
next_edges: []
edited_by: director-engine
scaffold_hash: d9a76fa020dc368d
season: 2
testable_claim: Both in-place trims in enforce_log_caps (copytruncate base, rename-mode archive) run the non-O_APPEND holder check and apply logs.non_append; unreadable /proc is UNKNOWN, said once.
title: "every in-place log trim refuses a non-O_APPEND holder, in rename mode as in copytruncate (assigned: director-engine)"
town: core
---
# hypothesis:every-in-place-log-trim-refuses-a-non-append-holder


# hypothesis:every-in-place-log-trim-refuses-a-non-append-holder

## Measured
- DH.383 (merged 5631482ee, parent a00-ab53bb94's review): the non-O_APPEND refusal (`logs.non_append`) is gated on `mode == copytruncate`, but kid a00-945d7ae4's rename-arm `_trim_in_place` (crons.py:~733) is ALSO an in-place write -- a `>`-semantics writer stranded on the archive inode after a rename is trimmed with no refusal, and resumes at its stale offset (NUL hole).

## CLAIM
Every in-place trim `enforce_log_caps` performs -- the copytruncate base truncate AND the rename-mode archive trim -- runs the same non-O_APPEND holder check first and applies `logs.non_append`; an unreadable /proc is UNKNOWN and said once per apply.

## Dispatch line
config-max: `logs.non_append` (exists) governs both arms, no new cell / template-max: none / code: crons.py -- one shared precondition helper called before BOTH in-place writes.

## FALSIFIERS
1. rename mode, a `python3 -c` stand-in holding the (renamed) archive open WITHOUT O_APPEND: the archive is trimmed anyway, or a NUL byte appears in it.
2. the same in copytruncate mode regresses (DH.383's refusal stops firing).
3. test_crons*.py regresses (166 green at 5631482ee).

## TESTS
extensions/agi/tests/test_crons_log_cap_*.py -- extend DH.383's fixtures; tmp logs dir only.

## FILE SCOPE
extensions/agi/bin/crons.py (`enforce_log_caps` + one helper), those tests, this node + its experiment.

## CEILING
1 kid · ~15 production lines · pi-free · 0 USD.

<!-- THOUGHT:BEGIN — authored, not derived; carried across regenerating scans. The reasoning behind THIS version. -->
Minted by director-engine gen 23 from DH.383 parent a00-ab53bb94's "open next": the fix for rename-mode archives added a second in-place write the non-append guard does not cover.
<!-- THOUGHT:END -->
