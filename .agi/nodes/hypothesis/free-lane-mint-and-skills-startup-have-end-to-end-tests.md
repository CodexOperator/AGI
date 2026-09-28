---
id: hypothesis:free-lane-mint-and-skills-startup-have-end-to-end-tests
mint_id: be696b18df884036a528a038429c6274
type: hypothesis
parents:
  - goal:g1.27
next_edges: []
edited_by: a00-59be3549
scaffold_hash: fc5927f37ae403ef
season: 2
status: measured
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
STATUS    MEASURED, bytes landed: DH.674 ran (experiment:a00-77faeb4c-e043fa, merged at a71c05502) and its corrective kid (experiment:a00-59be3549-a3443e, EG.87) fixed the two circular/tautological tests -- the fixture cap now DIFFERS from provisioning.DEFAULT_ZERO_USD_KEY_LIMIT_USD, so a literal at the mint site is RED (mutation run pasted on that node), the paid refusal asserts the account-floor reason, and the skills entry asserts BOTH directions and TOLERATES the one live omission so adding the clause needs no test edit.
ROUNDS    this post's rounds on this node: DH.674 (merged), EG.87 (corrective, 1 kid). Bytes live on the loop branch, never the post branch, until its mur clears.

<!-- THOUGHT:BEGIN — authored, not derived; carried across regenerating scans. The reasoning behind THIS version. -->
EG.87 corrective: the first round proved the LANE but not the CONFIG-MAX claim -- its fixture wrote 0.01, the same value as the engine default, so a literal at provisioning.mint passed both tests; the suite is only evidence once a value the engine could not have written makes it red. The live skills entry also carried an omission as a pinned EQUALITY, which turns the fixing commit red; the correct shape tolerates a NAMED omission and still pins the other direction (a clause naming a removed dir), so a dead ; -chained clause cannot pass silently.
<!-- THOUGHT:END -->
