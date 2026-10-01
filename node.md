---
id: verdict:dg2mvp-g7556p
mint_id: bc469431a762483286ad5fbfa5c9fa01
type: verdict
parents:
  - experiment:dg2mvp-g7556p-check
  - hypothesis:g7556-guard-ram-writes-charge-ramdisk-slice-through-one-shell-entry
next_edges: []
confidence: 0.85
edited_by: director-general-2
evidence_runs:
  - experiment:dg2mvp-g7556p-check
scaffold_hash: 378b1e114d16a874
season: 2
title: "goal:g7.16.1.5.5.6 post-build (627c94a040): proved 0.85 -- one live 1 MiB write via ramw ran in ramdisk.slice and charged it +1 MiB exactly (back after rm), the caller scope uncharged; every ram-main / session-sweep RAM write goes through guard/ram-write.sh; F1-F4 hold; tests green; follow-ups: fstype_at root-mount false alarm, ram-tier.sh HOT writes unrouted -> fork"
town: core
verdict: proved
---
# verdict:dg2mvp-g7556p

## Verdict: proved (confidence 0.85)

Every conjunct of the hypothesis holds on the HEAD bytes and no falsifier fires. The live measurement shows the charge: a 1 MiB write through the one shell entry ran in a ramdisk.slice transient scope (child /proc/self/cgroup), ramdisk.slice shmem rose by exactly 1048576 and fell back on removal, while the caller's own scope shmem did not move. The disk-bound path runs plain with argv's exit code. All named tests are green.

Not blocking, but real:
- fstype_at never matches the root mount, so a disk-bound `ramw` on the root filesystem prints a false "mount table unreadable ... UNCHARGED" line (behaviour is still right, fails open). Not on either card.
- ram-tier.sh (HOT dir on the RAM disk) writes unrouted: the goal's end-state ("any later writer") is not whole; DH.DG3.48 demoted it out of THIS hypothesis, so it is a follow-up, not a failure of this one.
- CEILING: mem_cap.py +82 vs the 57 chain cap (docstrings counted); the SM gate accepted it.
