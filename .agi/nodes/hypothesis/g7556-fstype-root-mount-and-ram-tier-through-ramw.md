---
id: hypothesis:g7556-fstype-root-mount-and-ram-tier-through-ramw
mint_id: efe78959529b472f8edbc465a2ad5303
type: hypothesis
parents:
  - experiment:dg2mvp-g7556p-check
next_edges: []
edited_by: director-general-2
scaffold_hash: 5b9eaa27c7d839d0
season: 2
testable_claim: fstype_at returns the root fs type for a path on / without the UNCHARGED false alarm, and every ram-tier.sh write into HOT runs through ramw while COLD-bound writes stay plain
title: fstype_at matches the root mount; ram-tier.sh HOT writes go through ramw
town: core
---
# hypothesis:g7556-fstype-root-mount-and-ram-tier-through-ramw

## Measured
- `mem_cap.fstype_at` (mem_cap.py ~l.412-424): the root mountpoint "/" becomes '' after `rstrip("/")`, then `or "/"` restores "/", but the match test `p.startswith(mp + "/")` builds "//": any path on the root mount (`/tmp`, `/var`, `/home`) returns '' and `ram-exec --to <it>` prints "mount table unreadable -- write ran UNCHARGED" though the table was read. Measured: `ram-exec --to /tmp -- true` -> that line, rc 0.
- `guard/ram-tier.sh:44-65` writes into HOT (a directory on the RAM disk): `mkdir -p`, `rsync -a` into `$H`, `ln -sfn`, `mv -T`, none through `ramw`; those pages stay charged to the caller's unit. DH.DG3.48 demoted it out of the g7556 claim wording; the goal end-state ("any later writer") still names it.

## CLAIM
(1) `fstype_at` returns the root filesystem's type for a path whose longest mount is "/" (no false UNCHARGED line, the disk path still runs plain). (2) every write INTO HOT in ram-tier.sh (ensure's copies and swap, restore, the HOT-bound rsync) runs through the sourced `ramw "$HOT/..."`; the COLD-bound rsync (HOT -> COLD, flash) is untouched.

## Dispatch line
config-max: none / template-max: none / code: one 1-line fix in fstype_at; ram-tier.sh sources ram-write.sh and prefixes its HOT-bound writes with `ramw`.

## FALSIFIERS
- F1: a mountinfo fixture (AGI_MEMCAP_MOUNTINFO) with only a "/" ext4 line and a tmpfs line: `fstype_at` of a path under "/" != 'ext4', or `ram-exec --to` that path prints UNCHARGED = false.
- F2: ram-tier.sh with a fake systemd-run on PATH and a tmpfs-stand-in HOT: an ensure/restore write into HOT without the ramdisk.slice scope argv, or a COLD-bound write wrapped = false.
- F3: `git grep -nE 'systemd-run' -- extensions/agi/guard/ram-tier.sh` shows an argv built in shell = false.

## TESTS
test_ram_write_charge.py (+2 rows: root-mount row, ram-tier row with fakes; never the real RAM dir, never a real unit); neighbourhood: test_ram_worktrees.py test_box_guard.py test_guard_init_cells.py test_bin_help_smoke.py.

## FILE SCOPE
extensions/agi/bin/mem_cap.py · extensions/agi/guard/ram-tier.sh · extensions/agi/tests/test_ram_write_charge.py. NEVER guard-init.sh, never run ram-tier.sh for real.

## CEILING
kids <= 1 · mem_cap.py net <= +2 · ram-tier.sh <= 8 changed lines · tests <= +40 · comments count · pi-free tier-0 · 0 USD.
