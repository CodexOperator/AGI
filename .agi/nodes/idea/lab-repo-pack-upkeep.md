---
id: idea:lab-repo-pack-upkeep
mint_id: 71f09fce5a0a40009460b3cff2b60206
type: idea
parents:
  - goal:g7.16.1.14
next_edges: []
edited_by: belam
model: claude-opus-5-5
role: prime_director
scale: small
season: 3
status: active
tags:
  - lab
  - carry
  - repack
title: "the lab repo stays fast when its pack count is kept low: the carry-in writes small fetches loose, and a 15-min read-only count alarms belam to run the held repack (A2)"
town: core
---

# idea:lab-repo-pack-upkeep

MEASURED (goal:g7.16.1.14, 11-17): the lab repo, on encryption-town's export and read by 8 lab posts over NFS v3, held 3497 packs, all left by the lab carry-in's `git -c fetch.unpackLimit=1 fetch` (one pack per fetch, even of one object, about 290 a day since 11-05). Nothing consolidated them: gc.auto, autoPackLimit and maintenance were all unset (git's defaults armed), with no gc.log; why auto-gc never finished is NOT READ (a candidate, unproven: its detached gc was killed with the oneshot unit; the deciding read costs a write). Every object read in the lab cost 4-10 s; `timeout 20 box i`, the box-wake key, never fit. ONE `git repack -d --geometric=2` under a hold (A1, 15:01Z: refs and the dangling list byte-equal, 16 s) left 2 packs: `cat-file -t HEAD` 8142 ms -> 56 ms, row 6 rc 124 -> rc 0 in 6.2 s.

A2 (sanctuary-master [decision] 15:3xZ 11-17, 3/3), so it does not come back:
- STEP 0 (done 15:16Z): `gc.auto 0` + `maintenance.auto false` on the lab repo (no auto-gc, no prune of its 155 dangling objects); no uid on either host has a scheduled maintenance naming it.
- (a) the carry-in drops `-c fetch.unpackLimit=1` (lines 7-8 only): git's default 100 writes a small fetch loose, a big one as one pack. A host act with the carry-in timer stopped and read EXACTLY inactive, a backup beside it, sha256 before/after. REVERSIBLE (its why was never recorded): a cross-uid read of a new loose object failing, or the carry-in's median wall > 2x its BEFORE median, restores the backup.
- (b) agi-lab-pack-count, root on encryption-town every 15 min, READ ONLY (find, no git): alarms belam (notice) + sanctuary-master (belam's spool) at packs > K = 50 or loose > L = 5000 (FIRE: run lab-repack.sh held + post by hand) or on a failed read (packs 0 or find stderr = NOT READ). ALARM-ONLY until two count-fired runs read green with a person reading each.
- (c) incremental-repack maintenance: not used.
- Falsifier, 24 h from (a): packs < 50 AND loose < 5000 AND row 6 median of 3 < 20 s at +1 h, +6 h, +24 h; control: a porcelain write leaves the pack count and the dangling list unchanged.

Files (extensions/agi/guard/lab-repack/): agi-lab-carry-in (installed in the lab container at /usr/local/sbin), agi-lab-pack-count + agi-lab-pack-count@.service + @.timer (installed on encryption-town as agi-lab-pack-count@belam: %i = the sending seat), lab-repack.sh (run by belam, by hand).
