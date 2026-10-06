---
id: hypothesis:g5353-ssh-config-paths-sanctuary-ssh-dir
mint_id: f175f51a25d24ebbbbd12fe48b4462e9
type: hypothesis
parents:
  - goal:g5.35.3
next_edges: []
confidence: 0.6
edited_by: director-general-1
scaffold_hash: 8858093538b9832a
season: 3
testable_claim: ssh -G -F <cfg> belam-prime identityfile exists under ~/work/.sanctuary/sanctuary/ssh/; no legacy missing-path lines remain (symlink may stay).
title: ssh config paths resolve under sanctuary/ssh (goal:g5.35.3)
town: core
---
# hypothesis:g5353-ssh-config-paths-sanctuary-ssh-dir

## Measured
- 16:4xZ 10-06 (date -u), director-general-1. SM GO WAVE-2 owner Shael 12:38 — DG1 FIRST hyp/split only on g5.35.3–.6. Trunk core/season2/et-grok-pilot @ fa043cf21 (land bc7ffc430). posts/director-general-1 FF-synced. DG3–9 HELD until DG1 AND DG2 PASS.
- goal:g5.35.3 (SM PASS g5.35.1 item 6): ssh config IdentityFile/UserKnownHostsFile must resolve under ~/work/.sanctuary/sanctuary/ssh/. Live box has compat symlink ~/work/.sanctuary/ssh -> sanctuary/ssh; config still names legacy path in 3 lines. Pack ships g5.35.3-ssh-config.diff for Belam apply (config not in repo).
- Owner HOLD build: this seat mints hyps only; no GO to builders until DG1 AND DG2 PASS. Leave g5.4.1.3 / season3 tip alone.

## CLAIM
ssh -G -F <cfg> belam-prime identityfile path exists on disk under ~/work/.sanctuary/sanctuary/ssh/; config lines no longer point at missing legacy ~/work/.sanctuary/ssh/ locations (symlink may remain as fallback; never delete as part of this leaf).

## Dispatch line
config-max: none / template-max: none / code: Belam applies pack three-line sed on box sanctuary ssh config after MUR (not in-repo). Not this seat.

## FALSIFIERS
1. ssh -G -F <cfg> belam-prime | identityfile test -f green; grep -c sanctuary/sanctuary/ssh on identityfile+userknownhostsfile = 2.
2. Negative: paths still point at missing legacy locations (or symlink deleted as the "fix").

## TESTS
DG2 experiment designs against goal:g5.35.3 falsifier 1+2. Neighbourhood: g5.35.1 PASS item 6; pack g5.35.3-ssh.md. No live-tree write this mint.

## FILE SCOPE
this node. No ssh config edit. No Belam wake. No implement this seat.

## CEILING
0 production lines · 0 USD · DG2 experiment · no kids · no push
