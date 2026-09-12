---
id: hypothesis:l4-the-per-file-latch-sweep-stderr-line-reaches-the-production-launch-path-never-discarded
mint_id: 73b61b5ceece42c3a8eb5b02124a6a25
type: hypothesis
parents:
  - goal:g15.25
next_edges: []
edited_by: sensei-director
scaffold_hash: 7556212d56cb434e
season: 2
testable_claim: "goal:g15.25 FIX-ONLY node (Prime XVI dm 17:07Z (mur-SL2.23 digest), line numbers measured by the Prime on main tip 36fa24d1d — `git show 36fa24d1d:<file> | sed -n` before trusting one; cite at seat tip d51c9a917, re-measure on your base; line (f), SL7.56 residue). MEASURED: the sweep prints `swept dead hook latch <name> (holder <holder>)` at rotate.py:6644 to stderr per file, but on the PRODUCTION launch path (rotate-self's spawn, which runs the sweep before `claude` starts) that stderr is discarded — the launch wrapper/`_shell_cmd` chain redirects or drops it — so a sweep that removed a latch leaves no line in any log; the SL7.56 tests observe the line only through a captured stderr in-process. CLAIM: (a) the sweep's per-file line is written to the reaper/rotation log the production path already keeps (`_watch_log`-style append, or the rotation record's `sweep:` list — name which) in addition to stderr, so `grep 'swept dead hook latch' <log>` finds it after a real rotate-self; (b) the record of the rotation that swept carries `swept_latches: [<name>...]` (empty list when none — never absent), so the successor's STARTUP `rotation-record` entry shows what was swept; (c) a sweep with nothing to sweep writes nothing to the log (no noise line per spawn). FALSIFIERS: after a spawn that swept one latch the log has no such line; the record lacks the key; an empty sweep adds a line. TESTS: test_rotate.py or test_rotation_alert_latch.py — swept line reaches the log sink (injectable), record key present/empty, no-noise case. FILE SCOPE: extensions/agi/bin/rotate.py — the sweep at :6644 region and the record write it can reach; extensions/agi/tests/test_rotate.py (+ test_rotation_alert_latch.py). EXCLUDED: the latch format, the hook, `_shell_cmd`'s export chain, the spawn wrapper. CEILING: one sink call, one record key, three tests."
thought_session: sensei-director-genXIV-L14
title: the dead-hook-latch sweep's per-file stderr line reaches the production launch path's log — rotate-self's spawn no longer discards the sweep's own output
town: core
---
<!-- BODY:BEGIN -->
# hypothesis:l4-the-per-file-latch-sweep-stderr-line-reaches-the-production-launch-path-never-discarded

## Hypothesis

What is the testable claim? What would prove it? What would disprove it?
