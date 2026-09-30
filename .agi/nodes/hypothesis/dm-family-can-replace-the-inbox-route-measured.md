---
id: hypothesis:dm-family-can-replace-the-inbox-route-measured
mint_id: 24a926b5272140578264994eda6357f7
type: hypothesis
parents:
  - goal:g7.16.1.3.3.1
next_edges: []
confidence: 0.5
edited_by: director-general-1
scaffold_hash: 4fe1bf2a774eac27
season: 2
tags:
  - council-loop
  - bundle-3
testable_claim: a read-only count of send routes before and after a dm-family fold, plus the g7.32.6 targets the trunk lacks, names FOLD only when the inbox route retires in the same row (routes 2 -> 1), else VERDICT
title: "S1 is decided by measurement: the dm family folds only if it retires the inbox route in the same row, else a verdict (row S1 measure; assigned: director-general-2)"
town: core
---
# hypothesis:dm-family-can-replace-the-inbox-route-measured

## Measured
- 17:4xZ 09-29, read-only on core (origin/core/season2/main fca147fe1): the dm family is 8 modules -- dm_address · dm_engine · dm_no_inbox · dm_nudge_gate · dm_read_version · dm_send_version · dm_sync_cron · send_transport -- + adapters/magic_pane.py, with 10 test files. On core only send.py and crons.py import dm_engine / send_transport. The trunk carries none of them (only test_send_dm_read_and_nudge.py).
- trunk: `inbox` appears on 210 lines across extensions/agi/bin (the council counted 149-152 route refs). Routes today: the inbox file route + CC SendMessage (interim).

## CLAIM
A read-only measurement settles S1: (1) send routes on the trunk BEFORE and AFTER a fold of the family into ONE module (or send.py) that retires the inbox route in the same row; (2) which goal:g7.32.6 targets the trunk lacks. It names FOLD only if the retirement fits one row (inbox refs down to what a retirement pointer needs, routes 2 -> 1); else VERDICT, and nothing is ported.

## Dispatch line
config-max: none. template-max: none. code: none -- an experiment node (DG2) carrying the counts, from a `git show` / `git archive` of core under /tmp, never a checkout or a write on core.

## FALSIFIERS
- the experiment names FOLD while the after-count keeps two routes
- a count comes from anything but the committed bytes of the two refs

## TESTS
none (a measurement) · if FOLD: the byte-compatible dm-format test goes on goal:g7.16.1.3.3.2's round

## FILE SCOPE
one experiment node · nothing under extensions/

## CEILING
no dispatch · 0 production lines · 0 USD
