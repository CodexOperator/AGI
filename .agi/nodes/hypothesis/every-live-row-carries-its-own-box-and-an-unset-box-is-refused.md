---
id: hypothesis:every-live-row-carries-its-own-box-and-an-unset-box-is-refused
mint_id: 812b7aa1f51f4fb881bc9a69df812b74
type: hypothesis
parents:
  - goal:send-is-hub-only-dm-file-versions-synced-every-30s
next_edges: []
confidence: 0.75
edited_by: director-engine
scaffold_hash: 6fcee7280f2effca
season: 2
tags:
  - engine
  - send
  - boxes
testable_claim: "(1) seating writes the row box cell from AGI_BOX (2) this_box refuses an unset AGI_BOX and an empty or unknown row box is never local (3) the foreign-row refusal prints once per row+cause, names the box, and sends no keys (assigned: director-engine)"
title: "every live row carries its own box from AGI_BOX; an unset or unknown box is refused on every box, once per row+cause (send-is-hub-only, belam 00:35Z; assigned: director-engine)"
town: core
---
# hypothesis:every-live-row-carries-its-own-box-and-an-unset-box-is-refused

## OWNER, verbatim (on the parent goal)
21:0xZ 09-26: "Can we not have the local box name be a global env variable that gets set as part of the ini routine somehow? Like the box label in the network or something. Then just check that."
belam 00:35Z 09-27 on the owner's go: done = (1) every live row carries its own box, written at seating from AGI_BOX (2) empty/unknown box refused on EVERY box, once per row+cause, naming the box (3) no send-keys into such a row's window.

## Measured
- extensions/agi/bin/boxes.py:153 `this_box` = AGI_BOX from the env, else the .env file, else the posts node's `default_box` (= core-town on this graph): an unset AGI_BOX silently becomes core-town.
- boxes.py:168 `row_is_local`: a row with NO box cell takes `default_box` (core-town), so on local-town every such row is FOREIGN; send.py:2198 refuses it as a nudge target, printing 'box (default)', on every sweep (belam 00:35Z: 6 rows).
- No seating path is known to write the row's `box` cell from AGI_BOX (the kid measures the seat-row writer and names it file:line before any code).

## CLAIM
(1) seating writes the row's own `box` cell from AGI_BOX (the one seat-row writer), so a newly seated live row always carries it (2) `this_box` REFUSES when AGI_BOX is unset (no silent default) and `row_is_local` treats an empty or unknown row box as NOT local on every box -- '(default)' is never a match (3) send.py's foreign-row refusal is printed ONCE per row+cause (not every sweep), names the box, and sends no keys into that row's window.

## Dispatch line
config-max: the box label is env AGI_BOX (set by the box init, never a config literal); default_box stays only as the posts node's documentation, never a locality fallback. template-max: none. code: the seat-row writer, boxes.py's two readers, the refusal's once-only memo.

## FALSIFIERS
- a temp graph with AGI_BOX unset: `this_box` returns any value instead of refusing.
- a row with box '' or an unknown label is local on some box.
- two sweeps over one foreign row print the refusal twice, or any send-keys reaches its window.
- a fresh seat on a temp graph leaves the row without `box`.

## TESTS
extensions/agi/tests/test_box_identity.py (new; temp graphs, monkeypatched env, a fake tmux runner -- never the live pane). Neighbourhood (send): test_send.py test_seatsig.py test_heal.py test_bin_help_smoke.py test_write_self_row.py. Every pytest under `timeout 600`, --basetemp under /tmp, env -u TMUX -u TMUX_PANE.

## FILE SCOPE
extensions/agi/bin/boxes.py · the ONE seat-row writer (named by the kid, file:line) · extensions/agi/bin/send.py (the foreign refusal at ~2198 only) · extensions/agi/tests/test_box_identity.py.

## CEILING
2 kids · <= 50 production lines · pi-free tier-0 · 0 USD. No test spawns pytest; kids never launch real claude; never the live .env.
