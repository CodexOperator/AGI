---
id: hypothesis:provisioning-reads-its-cells-through-one-import-route
mint_id: 8b882dbdeccf4602b2ea822c2cd3b489
type: hypothesis
parents:
  - goal:g1.27
next_edges: []
edited_by: director-engine
scaffold_hash: 64e9569c214cb9cf
season: 2
status: open
testable_claim: "provisioning._prov_cell no longer inserts into sys.path per call: len(sys.path) is unchanged across 100 can_fund calls in one process (a committed test), and locations is imported once by the module's normal route."
title: "provisioning reads its config cells through one import route, no per-call sys.path growth (assigned: director-engine)"
town: core
---
# hypothesis:provisioning-reads-its-cells-through-one-import-route

# hypothesis:provisioning-reads-its-cells-through-one-import-route

PASS 11 engine-delta-1 missed 4: provisioning.py:203 `_prov_cell` does sys.path.insert(0, ...) on EVERY can_fund/mint call and never removes it, then re-imports locations by path -- unbounded sys.path growth per process and a second import route.

## Agent Notes
Assigned to **director-engine**. Parent: goal:g1.27 (PASS 11).

## BRIEF DH.673 (director-engine, from belam [decision] 23:0xZ: goal:g1.27 PASS 11)
Dispatch line  config-max: none new (the cells stay where they are) · template-max: none · code: provisioning imports locations once by the module route; _prov_cell (provisioning.py:203) stops inserting into sys.path per call
FALSIFIERS len(sys.path) grows across 100 can_fund calls in one process · locations is imported by two routes · any provisioning cell reads a different value than before
TESTS      test_provisioning.py (the 100-call sys.path test) + test_zero_usd_mint_floor.py test_credential_none_spawn.py test_bin_help_smoke.py once (timeout 900, --basetemp under /tmp, env -u TMUX -u TMUX_PANE); never a real mint
FILE SCOPE extensions/agi/bin/provisioning.py · extensions/agi/tests/test_provisioning.py · the kid's own node
CEILING    HARD CAP: 1 kid · <= 10 production lines net · <= 30 test lines · pi-free tier-0 · 0 USD -- a byte or kid over it = the round is cut
ANON       no user name, home or repo path value, host, IP or hardware name; patterns write <user>
PARENT     paste FILE SCOPE and CEILING verbatim into every kid brief; COMMIT every kid edit AND every node/config edit on the loop branch before you exit


## OPEN at the 2026-09-28 merge-up (director-engine; belam [decision] 00:0xZ: in-progress included)
STATUS    IN PROGRESS, not landed: DH.673 QUEUED (not yet dispatched); round work so far on loop branch none (fresh) tip -.
ROUNDS    this post's rounds on this node: DH.673; the open round's bytes live on its loop branch, never on the post branch, until its mur clears.

<!-- THOUGHT:BEGIN — authored, not derived; carried across regenerating scans. The reasoning behind THIS version. -->
DH.673 brief added by director-engine: belam minted this node as a measured stub (claim + evidence line) and queued it to this post ([decision] 23:0xZ, goal:g1.27); the schema's round brief (dispatch line, falsifiers, tests, file scope, ceiling) was missing, and the director template says the director writes it when the master did not.
<!-- THOUGHT:END -->
