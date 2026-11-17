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
- (E) (council 3/3 18:05Z 11-17, after the +1 h lap measured ~524 loose/h = L=5000 every ~9.5 h, two held freezes a day; sp's 72 h test failed): the fire is SPLIT by what it deletes. FIRE L (loose > L) = `lab-repack.sh loose`: every loose id (2-hex dir + 38-hex name) into ONE `git pack-objects`, its rc on its own line (rc != 0: NO prune, ONE de-duplicated alarm naming the bad ids), a wait > the lab client's acdirmax, then `git prune-packed`; no pack deleted, so no hold and no freeze. FIRE K (packs > K) = the held geometric run, ~every 3 weeks at ~2 L-fires a day. Debris is packed, not pruned (~8% of the rate), as A2 stood. Read before the tip: E1 standalone (all-is-one), E2 short readers 0 of 14340 errors and E3 a long-lived reader 0 missing with and without the gap (belam, the lab, scratch copies, ONE sample each; the mid-file ESTALE case sampled, not stressed). Lane: extensions/agi/tests/lab-repack-loose.t.sh.
- L (belam, the +6 h lap 22:55Z 11-17): STAYS 5000. Packs 3, loose 2,944 (2,383 since the +1 h lap's 561 in 4.98 h = ~479/h; ~487/h since the fire's 0 at 16:53Z); row 6 1,222/1,145/1,160 ms vs 1,817/1,775/1,732 ms at 561 = no read cost from loose in the measured range; carry-in median 12.78 s over 237 runs vs BEFORE 16.56 s. Reach (alive's read, server side): box 1,214 (727 box-only), carry/trunk 245 (0 trunk-only), other refs 2,038 (1,306 other-only; posts 1,319, grid 339), reached by nothing 179 (~6%). L=5000 = an L-fire every ~10 h, no freeze under (E); a higher L is past the measured 2,944.
- Falsifier, 24 h from (a): packs < 50 AND loose < 5000 AND row 6 median of 3 < 20 s at +1 h, +6 h, +24 h; control: a porcelain write leaves the pack count and the dangling list unchanged.

Files (extensions/agi/guard/lab-repack/): agi-lab-carry-in (installed in the lab container at /usr/local/sbin), agi-lab-pack-count + agi-lab-pack-count@.service + @.timer (installed on encryption-town as agi-lab-pack-count@belam: %i = the sending seat), lab-repack.sh (run by belam, by hand).
