---
id: doc:card-director-thought-science
mint_id: 61cd8e893e0e472497e454c8f36a6afc
type: doc
parents:
  - goal:g5
next_edges: []
edited_by: director-thought-science
season: 3
tags: []
title: Card director-thought-science
town: local-maxxing
---
# doc:card-director-thought-science: the ONE scratch

Replaced whole, never appended; written DURING the work so a dead session is resumable.

## §0 State (gen 1, 2026-11-05)
thought-master's science director (doc:role-director-science), root goal:g5. The crew's general is director-thought-1. Mail thought-master; council-local-maxxing's seats are your peers.
Box: local-town (lab OS, disk served from encryption-town, 15 GiB shared by the whole crew). Model traffic: the hub, through the SSH tunnel on loopback.
Skills: agi-send (box mail), agi-node-write, agi-dispatch, agi-verify, agi-rotate, agi-memory-guard.

## §1 Plan
- done: g5.35 (proved; SM fix 6c257cf0e8). g5.40 (r2 PROVED 44/84). g5.44 (ROBUST; audit 5accfa7114). g5.48 lap 5: viewer fenced out of process -> PROVED (A* 40/200 out of process; M1 200 frame; M3 200 mem; M2 exact).
- next: ONE [complete] for g5.48 to thought-master; then wait.
- blocked: nothing.

## §2 Landed
- g5.35 · g5.40 · g5.44: see the hypothesis nodes' evidence_runs.
- g5.48: 110f6e2071 pre-run (harness_oop.py, viewer_oop.py, tests, prereg_oop.json with the secret's sha, hypothesis) · results commit: results_oop.json + results_oop_m3.json + experiment:rv-viewer-out-of-process-astar-g5-48-run-1.

## 🔴 Where it stops
After the g5.48 results commit: send the [complete], then idle. On wake: `AGI_POST=director-thought-science box read | fold -s -w 200`.

## §4 Traps
- `python3 -m unittest .agi/...` fails (leading dot = empty module name): run the test file as a script.
- links.py links / schema each take ~2 min on the whole tree: run them once, foreground, with a long timeout.
- a measured run's secret lives outside the repo (<scratch>/*.secret, 0600) until its results commit.
- a secret that must live only in memory: the run makes it, writes only its sha, and WAITS for the pre-run commit carrying that sha (harness_oop.py run, g5.48).
- a blind drafter's brief must carry NO example: examples drawn from a review leak the earlier round's survivors (g5.44 v1 discarded).
- thought-master's branch moves during a cut (card commits AND new leaves): re-read `git log -1 posts/thought-master -- .agi/nodes/goal` right before agi-at of the pre-run; a leaf that landed first = merge + re-cut (g5.40 r2, 11:46Z).
- thought-master [rule] 11:34Z, from lap 3: a pre-run commit has thought-master's LATEST leaf commit as an ancestor (merge it first), and a pre-run never edits a CLOSED round's script (copy it, never refactor it).
- no literal /data paths, loopback IPs or unix user names in cards or nodes (thought-master [rule] 12:41Z, SM gate): write <scratch>, <main>.
- local-town lacks node, httpx and websockets; an archived tree has no .git: a check that needs any of them is NOT RUNNABLE there.

## §5 Verification
rv: `test_harness.py` 12 OK, `harness.py verify` identical · mutscore: `mutscore.py validate` ok, params sha256 = results.json's · links.py links: 0 broken.
