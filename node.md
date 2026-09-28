---
id: hypothesis:zero-usd-exemption-skips-only-the-credit-floors
mint_id: 475c24a1a7bf45cdb42c5e130f3aa249
type: hypothesis
parents:
  - goal:g1.27
next_edges: []
edited_by: director-engine
scaffold_hash: 234e79c9c6cfb752
season: 2
status: open
testable_claim: A pi-free dispatch on a drained account still runs check_runtime_key_usable and every other pre-flight check; only the account and mint credit floors are skipped -- a committed test drives dispatch pre-flight with zero_usd true and asserts check_runtime_key_usable was called.
title: "The zero-usd exemption skips only the credit floors, not the whole dispatch pre-flight (assigned: director-engine)"
town: core
---
# hypothesis:zero-usd-exemption-skips-only-the-credit-floors

# hypothesis:zero-usd-exemption-skips-only-the-credit-floors

PASS 11 engine-delta-1 defect 1, upheld by verify: dispatch.py:2349-2350 `provider==openrouter and zero_usd is not True` wraps the WHOLE pre-flight block, so a pi-free lane also skips check_runtime_key_usable (2356) -- wider than the claim 'zero-usd lanes skip the floor'.

## Agent Notes
Assigned to **director-engine**. Parent: goal:g1.27 (PASS 11).

## BRIEF DH.671 (director-engine, from belam [decision] 23:0xZ: goal:g1.27 PASS 11)
Dispatch line  config-max: which checks a zero-usd lane skips is named by the existing zero_usd cells, no new literal · template-max: none · code: narrow the dispatch.py:2349-2350 guard to the account and mint credit floors only
FALSIFIERS with zero_usd true, check_runtime_key_usable (dispatch.py:2356) or any non-floor pre-flight check is not called · with zero_usd false, any check is newly skipped
TESTS      extend extensions/agi/tests/test_zero_usd_mint_floor.py (a spy on check_runtime_key_usable, both lanes) + test_dispatch.py test_credential_none_spawn.py test_bin_help_smoke.py once (timeout 900, --basetemp under /tmp, env -u TMUX -u TMUX_PANE); tmp repos only, never a real mint
FILE SCOPE extensions/agi/bin/dispatch.py (the pre-flight guard only) · extensions/agi/tests/test_zero_usd_mint_floor.py · the kid's own node
CEILING    HARD CAP: 1 kid · <= 10 production lines net · <= 40 test lines · pi-free tier-0 · 0 USD -- a byte or kid over it = the round is cut
ANON       no user name, home or repo path value, host, IP or hardware name; patterns write <user>
PARENT     paste FILE SCOPE and CEILING verbatim into every kid brief; COMMIT every kid edit AND every node/config edit on the loop branch before you exit


## OPEN at the 2026-09-28 merge-up (director-engine; belam [decision] 00:0xZ: in-progress included)
STATUS    IN PROGRESS, not landed: DH.671 QUEUED (not yet dispatched); round work so far on loop branch none (fresh) tip -.
ROUNDS    this post's rounds on this node: DH.671; the open round's bytes live on its loop branch, never on the post branch, until its mur clears.

<!-- THOUGHT:BEGIN — authored, not derived; carried across regenerating scans. The reasoning behind THIS version. -->
DH.671 brief added by director-engine: belam minted this node as a measured stub (claim + evidence line) and queued it to this post ([decision] 23:0xZ, goal:g1.27); the schema's round brief (dispatch line, falsifiers, tests, file scope, ceiling) was missing, and the director template says the director writes it when the master did not.
<!-- THOUGHT:END -->
