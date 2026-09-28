---
id: hypothesis:dispatch-credential-banner-states-the-real-key-cap
mint_id: c09dc0d1f1ed4b3c8b8c18b1f8e72b67
type: hypothesis
parents:
  - goal:g1.27
next_edges: []
edited_by: director-engine
scaffold_hash: 1f031b1041e62229
season: 2
status: open
testable_claim: On a zero_usd lane the dispatch banner prints the zero_usd_key_limit the key is minted with (0.01), never the pre-mint cred_limit; test_dispatch pins the banner for both lanes.
title: "The dispatch credential banner states the key cap actually minted (assigned: director-engine)"
town: core
---
# hypothesis:dispatch-credential-banner-states-the-real-key-cap

# hypothesis:dispatch-credential-banner-states-the-real-key-cap

PASS 11 engine-delta-1 missed 3: dispatch.py:2196 prints 'credentials: minting per spawn, limit=$cred_limit' from the PRE-mint value while provisioning.py:873-874 overrides limit_usd to zero_usd_key_limit on a free lane -- the banner reports $1.5 (or --cap) for a key capped at $0.01.

## Agent Notes
Assigned to **director-engine**. Parent: goal:g1.27 (PASS 11).

## BRIEF DH.672 (director-engine, from belam [decision] 23:0xZ: goal:g1.27 PASS 11)
Dispatch line  config-max: the banner reads the provisioning.zero_usd_key_limit cell the mint uses, never a literal 0.01 · template-max: the banner text, if a template carries it · code: the banner takes the post-override limit
FALSIFIERS on a zero-usd lane the banner prints cred_limit or --cap instead of the minted limit · on a paid lane the banner changes
TESTS      test_dispatch.py (pin the banner for both lanes) + test_provisioning.py test_zero_usd_mint_floor.py test_bin_help_smoke.py once (timeout 900, --basetemp under /tmp, env -u TMUX -u TMUX_PANE); never a real mint
FILE SCOPE extensions/agi/bin/dispatch.py (the banner at :2196 only) · extensions/agi/tests/test_dispatch.py · the kid's own node
CEILING    HARD CAP: 1 kid · <= 8 production lines net · <= 30 test lines · pi-free tier-0 · 0 USD -- a byte or kid over it = the round is cut
ANON       no user name, home or repo path value, host, IP or hardware name; patterns write <user>
PARENT     paste FILE SCOPE and CEILING verbatim into every kid brief; COMMIT every kid edit AND every node/config edit on the loop branch before you exit


## OPEN at the 2026-09-28 merge-up (director-engine; belam [decision] 00:0xZ: in-progress included)
STATUS    IN PROGRESS, not landed: DH.672 QUEUED (not yet dispatched); round work so far on loop branch none (fresh) tip -.
ROUNDS    this post's rounds on this node: DH.672; the open round's bytes live on its loop branch, never on the post branch, until its mur clears.

<!-- THOUGHT:BEGIN — authored, not derived; carried across regenerating scans. The reasoning behind THIS version. -->
DH.672 brief added by director-engine: belam minted this node as a measured stub (claim + evidence line) and queued it to this post ([decision] 23:0xZ, goal:g1.27); the schema's round brief (dispatch line, falsifiers, tests, file scope, ceiling) was missing, and the director template says the director writes it when the master did not.
<!-- THOUGHT:END -->
