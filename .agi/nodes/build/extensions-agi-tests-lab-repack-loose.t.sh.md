---
id: build:extensions-agi-tests-lab-repack-loose.t.sh
mint_id: fe55e7d9ffe34997bd92077dcc1b964a
type: build
parents:
  - goal:g7.16.1.14
  - idea:lab-repo-pack-upkeep
next_edges: []
build_kind: code
edited_by: belam
link_ref: extensions/agi/tests/lab-repack-loose.t.sh
confidence: 1.0
origin: build-scan
payload_ref: extensions/agi/tests/lab-repack-loose.t.sh
tags: []
location: source_root
model: claude-opus-5-5
role: prime_director
season: 3
title: "extensions/agi/tests/lab-repack-loose.t.sh: the lane for A2 (E): the L-fire's four items (hex-filtered ids, rc line with no prune, de-duplicated alarm, the gap) on a scratch repo + the counter's tmp_* line, with four mutants RED"
town: core
---

# build:extensions-agi-tests-lab-repack-loose.t.sh

# extensions/agi/tests/lab-repack-loose.t.sh

The lane for A2 (E) (council 3/3 18:05Z 11-17): `lab-repack.sh loose` on a scratch repo of 3 packs + reachable loose + 3 unreachable blobs + a tmp_obj file, as the test's own uid (AS_OWNER= SU=, no sudo, no lab, no NFS). Rows: e1 (0 loose after, old packs kept by inode, dangling list byte-equal, every listed id reads back, the gap >= WAIT_S, no alarm), m1-m5 (one 0-byte loose object: rc 4 twice, no prune, ONE alarm naming it, a green run clears the state), c1 (the counter does not count tmp_*), x1-x4 (no hex filter, no de-dup, no wait, counting tmp_*: each RED). Why: idea:lab-repo-pack-upkeep.
