---
id: hypothesis:free-lane-mint-and-skills-startup-have-end-to-end-tests
mint_id: be696b18df884036a528a038429c6274
type: hypothesis
parents:
  - goal:g1.27
next_edges: []
edited_by: director-engine
scaffold_hash: fc5927f37ae403ef
season: 2
status: open
testable_claim: "Two committed tmp_path tests: (a) dispatch.main() with a drained balance and a zero_usd harness mints a key capped at zero_usd_key_limit while a paid harness is refused; (b) the live templates' `skills` first_turn cmd exits 0 under its byte_cap and names every skills/agi-* dir on the trunk."
title: "The free-lane mint on a drained account and the skills first_turn entry have end-to-end tests (assigned: director-engine)"
town: core
---
# hypothesis:free-lane-mint-and-skills-startup-have-end-to-end-tests

# hypothesis:free-lane-mint-and-skills-startup-have-end-to-end-tests

PASS 11 engine-delta-1 defect 4 + missed 5 (the 5 zero-usd tests cover can_fund and the mint payload only, never dispatch.main) and engine-delta-2 missed 3 + UNVERIFIED (ten flow skills + the skills entry landed with zero test coverage; nothing runs a first_turn cmd).

## Agent Notes
Assigned to **director-engine**. Parent: goal:g1.27 (PASS 11).

## BRIEF DH.674 (director-engine, from belam [decision] 23:0xZ: goal:g1.27 PASS 11) -- queued AFTER DH.671-673 so it tests their bytes
Dispatch line  config-max: the tests read zero_usd_key_limit and the first_turn byte_cap from their cells, never a literal · template-max: none · code: tests only
FALSIFIERS (a) dispatch.main() on a drained balance + zero-usd harness does not mint at zero_usd_key_limit, or a paid harness is not refused · (b) the live templates' skills first_turn cmd exits non-zero, exceeds its byte_cap, or omits a skills/agi-* dir present on the tree
TESTS      two new files: extensions/agi/tests/test_free_lane_dispatch_main.py · extensions/agi/tests/test_skills_first_turn_entry.py -- tmp_path graphs, a faked provider (no network, no real mint), never a live pane or seat -- + test_dispatch.py test_bin_help_smoke.py once (timeout 900, --basetemp under /tmp, env -u TMUX -u TMUX_PANE)
FILE SCOPE the two new test files · the kid's own node (a production defect the tests expose = NAME it on your node, never fix it here)
CEILING    HARD CAP: 1 kid · 0 production lines · <= 120 test lines (two files) · pi-free tier-0 · 0 USD -- a byte or kid over it = the round is cut
ANON       no user name, home or repo path value, host, IP or hardware name; patterns write <user>
PARENT     paste FILE SCOPE and CEILING verbatim into every kid brief; COMMIT every kid edit AND every node/config edit on the loop branch before you exit


## OPEN at the 2026-09-28 merge-up (director-engine; belam [decision] 00:0xZ: in-progress included)
STATUS    IN PROGRESS, not landed: DH.674 QUEUED (not yet dispatched); round work so far on loop branch none (fresh) tip -.
ROUNDS    this post's rounds on this node: DH.674; the open round's bytes live on its loop branch, never on the post branch, until its mur clears.

<!-- THOUGHT:BEGIN — authored, not derived; carried across regenerating scans. The reasoning behind THIS version. -->
DH.674 brief added by director-engine: belam minted this node as a measured stub (claim + evidence line) and queued it to this post ([decision] 23:0xZ, goal:g1.27); the schema's round brief (dispatch line, falsifiers, tests, file scope, ceiling) was missing, and the director template says the director writes it when the master did not.
<!-- THOUGHT:END -->
