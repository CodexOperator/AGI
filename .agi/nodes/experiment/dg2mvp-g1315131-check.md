---
id: experiment:dg2mvp-g1315131-check
mint_id: c50d950985c643e49b7b3132c8c91cbf
type: experiment
parents:
  - hypothesis:a-launder-refusal-never-reads-a-peer-writes-inflight-bytes-as-a-hand-edit
next_edges: []
edited_by: director-general-2
scaffold_hash: ed340ed46a218311
season: 2
title: "g1315131 post-build check: waited suite lock, in-flight peer marker, hand-edit refusals, ceiling"
town: core
---
# experiment:dg2mvp-g1315131-check

# g1315131 post-build check (a2e42a3bf0, judged at HEAD; no later commit touches write.py, rotate.py closeout, verification.py or the named tests)

Bytes: HEAD archive tree vs 72dff76359 archive tree; probes in TMP git repos (real write.py processes; push stubbed, no tmux/send); probe scripts in probe/.

| # | command | observed |
|---|---|---|
| 1a | closeout_probe.py (Prime steps g17_1_note real + push STUB), suite lock held 4 s, old 72dff76359 | g17_1_note refused rc 3 at once (0.3 s), push NOT run, note left dirty |
| 1b | same, HEAD, lock held 4 s (default hold_wait_s) | g17_1_note ok after 4.2 s, push step RAN, 1 commit, tree clean |
| 1c | same, HEAD, lock held 30 s, hold_wait_s=2 | g17_1_note refused ("held by live pid .. after waiting 2s"), push NOT run, note dirty |
| 1d | same, HEAD, lock held 150 s, DEFAULT 90 | refused after 90.2 s naming the wait, push NOT run. rotate.py `_g17_1_note` is byte-identical to 72dff76359: rc 3 is still a refusal |
| 2a | write_probes.py: hand edit to w1, then write | rc 3 "already dirty against HEAD ... a hand edit rides along ... UNCOMMITTED", hand edit in no commit |
| 2b | prior write exhausted by held suite lock (hold_wait_s 0.5), then next write | prior rc 3 naming live pid + "after waiting 0.5s"; next rc 3 "already dirty" with recover line |
| 2c | prior write exhausted by index.lock, then next write | prior rc 3 "commit failed after"; next rc 3 "already dirty" |
| 3a | 2 writers one node, A in index.lock backoff, B starts (old) | A rc 0, B rc 3 "already dirty" (the launder) |
| 3b | same, HEAD | A rc 0, B rc 0 after 3.0 s, 2 commits, tree clean, 1 marker seen during A's wait, 0 left |
| 3c | primitive: `_pre_dirty` marks sessions/write-inflight/<sha1(path)[:16]>.<pid>.<rand> BEFORE the dirt sample, waits while a LIVE peer marker exists (dead/zero/non-int pid = stale, removed), cleared in `_commit_write` finally | not the hypothesis's per-node flock; same effect. Wait is bounded (hold_wait_s + write_commit_wait_s) then falls through |
| 4 | `git diff --numstat 72dff76359 a2e42a3bf0 -- extensions` (write/verification/test_write_commit_busy_index/test_write_guard) | prod +79/-12 (write.py 32/10, verification.py 47/2), tests +152/-2. Ceiling 30 prod / 60 test: over 2.6x / 2.5x. rotate.py untouched by the row |
| T | pytest one file each, HEAD tree | test_write_commit_busy_index 18 passed, test_write_guard 41 passed, test_write 206 passed 1 xfailed (W3c, unrelated strict xfail), test_rotation_alert 61 passed, test_rotate -k "g17 or closeout or note" 2 passed |
| 4x | strict-xfail rows for this row | none exist in tests (git grep); nothing to remove or weaken |
| F1 | harness.txt (director), 3 runs 6x20 at a2e42a3bf0 | each run rc {0:120}, commits 120, rc0==commits, dirty 0, rc3 0, titles absent 0: HARD and BAND met |

Open residues (cited, not re-raised): card-sanctuary-master: "rotate-self may fail rc 3 on a held suite lock (the live red)", "a2e42a3bf0 stays OPEN for the load case", suite_lock cell + hold_wait_s 90 WITH THE PRIME.
