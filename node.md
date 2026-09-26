---
id: hypothesis:cron-layer-keeps-its-disk-footprint-bounded
mint_id: fd0dc6705ba9424b8b1496d7b2a3084a
type: hypothesis
parents:
  - goal:g6.49
next_edges: []
edited_by: belam
scaffold_hash: c144c27994697466
season: 2
testable_claim: "On local-town the cron layer keeps its own disk footprint bounded without a human: a declared maintenance job holds .git/objects within 1.5x of a fresh full repack, every ~/logs file stays under a declared cap with declared rotations, a no-op cycle writes at most one line per command, and the 09-23 07:35Z full re-fetch has a reproduced cause and a guard."
thought_session: belam-S2-L5-VIII
title: "the cron layer keeps its own disk footprint bounded -- logs capped, objects repacked, no-op cycles quiet (assigned: director-engine)"
town: core
---
# hypothesis:cron-layer-keeps-its-disk-footprint-bounded

assigned: director-engine. OWNER 01:3x-01:4xZ 09-26 in the Prime's pane, verbatim: "Can we check to make sure the grid cron is healthy and not piling up logs again" · "Also the grid cron should only version nodes that genuinely changed right and use git commit compression to eliminate wasted storage right" · on the Prime's two offers (a one-off git gc; one clean-up hypothesis to director-engine): "Go on both."

## Measured (belam-S2-L5-VIII, 01:3x-01:5xZ 09-26, local-town)
- HEALTHY, not a defect: config:crons installed == declared (`crons.py show`: up to date); one grid_sync per 5 min; 0 overlapping grid.py processes; a quiet cycle prints `grid: 0 new version(s), 0 error(s)` + `grid push: 0 changed ref(s)`. grid.py:858-872 versions only on a changed tree (node.md + payload vs the ref tip): the 40 newest versions = 20 first, 18 body/payload, 2 frontmatter-only on data keys, 0 identical (971 versions in 24 h).
- LOGS: crons.py:450 sends every managed line to ONE file, `~/logs/agi-crons-<repo>-<hash8>.log`; nothing caps or rotates it or the reaper log (no logrotate entry; no cap in crons.py). At 01:3xZ: crons log 134 MB (content from 09-20 05Z; 1510 grid cycles), reaper log 31 MB (~7 MB/day).
- NO-OP NOISE, every 5-min cycle (~10 KB, ~3 MB/day): `crons.py apply` re-prints all 10 crontab lines on `crontab already matched (no-op)` (~2.6 KB); grid commit prints 18 `WARN: build:<x> payload_ref ... resolves neither` lines for retired build nodes (~3.6 KB); 18 `mail_poll: skipped foreign-box post` + 8 `warn: no pin/usage for seat` lines; the */2 wake prints 7 lines when nothing is pending.
- BURSTS (all stopped, for the record): 225k `! [rejected] refs/grid/node/* (fetch first)` lines (last ~09-21 06Z); 133k push-protection `[remote rejected] refs/grid/local-maxxing/*` lines (last ~09-25 03Z); 8.7 MB of heal re-seat prompt dumps on the evening of 09-25 (owned by hypothesis:heal-lands-a-reseat-after-a-tmux-server-restart).
- OBJECT STORE: no gc/maintenance config, no maintenance timer, no gc cron line. The grid writes with plumbing (grid.py:16-17), which never runs gc --auto; the */5 fetch does, but gc --auto only packs loose objects past 6700 and merges packs past gc.autoPackLimit=50. Before the one-off gc: 38 packs 191.5 MiB holding 45% duplicate entries (280,858 entries, 154,673 unique) + 4,686 loose objects 62.2 MiB = 258 MiB on disk; a dry-run full repack (`pack-objects --stdout | wc -c`) measured 72.8 MiB.
- THE RE-FETCH: the pack created 09-23 07:35Z (59.4 MB, 120,442 objects) held 99.6% objects already in older packs; the reflog window 07:14-07:36Z shows `fetch -q origin` x2, `update by push` x2 and `merge local-maxxing/season2/sync/core-0923`.
- ONE-OFF DONE by the Prime on the owner's go (01:50:41-01:51:13Z): `git gc` with reflog, worktree and rerere expiry disabled -> 2 packs 77.8 MiB (70.9 MB + a 2.6 MB cruft pack), 0 loose, du .git/objects 258 -> 80 MiB, refs/grid 8196 -> 8196, `git fsck --connectivity-only` exit 0.

## CLAIM
On local-town the cron layer keeps its own disk footprint bounded without a human: (1) a declared maintenance job holds .git/objects within 1.5x of a fresh full repack; (2) every file under ~/logs, the reaper log included, stays under a declared size cap with a declared number of rotations; (3) a cycle that changes nothing writes at most one line per command; (4) the 09-23 07:35Z full re-fetch has a reproduced cause and the smallest guard that stops a repeat.

## Dispatch line
config-max: the log cap, rotation count and maintenance cadence as declared cells (config:crons or .agi/config.json), never code literals / template-max: none / code: crons.py (the maintenance line, rotation, the quiet no-op), grid.py (a retired node's unresolved payload warned once, not every cycle), send.py (mail_poll + pin warnings summarized to one line); the re-fetch is measured before it is fixed.

## FALSIFIERS
7 days after landing, a fresh full-repack dry run is below 2/3 of `du .git/objects`; a ~/logs file passes its cap; a no-op cycle writes more than one line for any command; the re-fetch cause is asserted without a reproduction.

## TESTS
extensions/agi/tests/test_crons*.py · test_grid.py · the send.py mail_poll tests; a fixture no-op cycle that counts its log lines.

## FILE SCOPE
extensions/agi/bin/crons.py · extensions/agi/bin/grid.py · extensions/agi/bin/send.py (the mail_poll / pin warning lines only) · .agi/nodes/.geometry/crons.md · .agi/config.json (cells only) · extensions/agi/tests/

## CEILING
1 parent (pi-free) · <= 2 kids · 0 USD · after DE's stale-session round (card 2c): nothing here is urgent now that the one-off gc ran (53 GB free on /).
