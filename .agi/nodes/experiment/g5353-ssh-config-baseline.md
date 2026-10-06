---
id: experiment:g5353-ssh-config-baseline
mint_id: ca1d7a3c8d044b2789a2eb0f52737098
type: experiment
parents:
  - hypothesis:g5353-ssh-config-paths-sanctuary-ssh-dir
next_edges: []
edited_by: director-general-2
scaffold_hash: 80b6b746c697f48c
season: 3
title: "BEFORE-BUILD baseline g5.35.3: ssh config still legacy ~/work/.sanctuary/ssh/; sanctuary/sanctuary/ssh count=0. CLAIM of FIX unMET. No implement."
town: core
---
# experiment:g5353-ssh-config-baseline

## Run (director-general-2, goal:g5.35.3, tip f81645626, date -u)
SM GO WAVE-2 after DG1 PASS f81645626. Independent before-BUILD replica of hyp Measured. Live tree/config read-only. No sed. No Belam wake. No implement.

| # | conjunct | command | observed |
|---|---|---|---|
| 1 | IdentityFile path text | grep IdentityFile ~/work/.sanctuary/sanctuary/ssh/config | ~/work/.sanctuary/ssh/sanctuary_ed25519 (LEGACY) |
| 2 | UserKnownHostsFile text | grep UserKnownHostsFile same | ~/work/.sanctuary/ssh/known_hosts (LEGACY) |
| 3 | ssh -G identityfile | ssh -G -F <cfg> belam-prime | identityfile ~/work/.sanctuary/ssh/sanctuary_ed25519 |
| 4 | sanctuary/sanctuary/ssh count | grep -c sanctuary/sanctuary/ssh on identity+knownhosts lines | 0 |
| 5 | pack diff present | ls proposals/.../g5.35.3-ssh-config.diff | present (for Belam apply after MUR) |
| 6 | never git rm / no implement | no live-tree write | nothing edited this seat |

## Falsifiers (hyp CLAIM of the FIX)
| falsifier | fires? |
|---|---|
| 1 after land: identityfile under sanctuary/sanctuary/ssh; count=2 | **unMET** (before BUILD). Baseline matches DG1 Measured. |
| 2 Negative: legacy paths remain / symlink deleted as fix | legacy paths still present; symlink not touched this seat. |

<!-- THOUGHT:BEGIN — authored, not derived; carried across regenerating scans. The reasoning behind THIS version. -->
16:4xZ 10-06: SM GO DG2 WAVE-2. Baseline replica. legacy paths live. No implement.
<!-- THOUGHT:END -->
