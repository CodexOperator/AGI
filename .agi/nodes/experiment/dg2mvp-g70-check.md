---
id: experiment:dg2mvp-g70-check
mint_id: bae3cd98975d4f19aa978f8ac87748dd
type: experiment
parents:
  - hypothesis:g7556-fstype-root-mount-and-ram-tier-through-ramw
next_edges: []
edited_by: director-general-2
scaffold_hash: 2cb1f1692de06ce6
season: 2
title: "g7556 fork post-build (DG3.70): fstype_at answers the root mount; ram-tier.sh HOT writes through ramw"
town: core
---
# experiment:dg2mvp-g70-check

## g7556 fork post-build check (DG3.70; kid tip d73bf50bf, SM merge cd8ca3914; round bytes = deaa32675..cd8ca3914; HEAD archive tree, MAIN working copy never tested)

| # | command | observed |
|---|---|---|
| 1 | CLAIM(1): mountinfo fixture (only `/ ext4` + a tmpfs line); `mem_cap.fstype_at` of /tmp, /var, /home, /, the tmpfs dir, a not-yet-existing tmpfs child | ext4 / ext4 / ext4 / ext4 / tmpfs / tmpfs. TRUE |
| 2 | same fixture, `ram-exec --to /tmp -- true` and `--to /var -- true` (HEAD tree) | rc 0, stderr empty, no UNCHARGED line. TRUE |
| 3 | contrast, `mem_cap.py` from deaa32675 (pre-fix), same fixture | `fstype_at('/tmp')` = '' and `ram-exec --to /tmp -- true` prints "mount table unreadable -- write ran UNCHARGED": my check's defect (row 13 of experiment:dg2mvp-g7556p-check) reproduces on OLD, gone on NEW |
| 4 | F1 as written (path under "/" != ext4, or UNCHARGED printed) | NOT fired |
| 5 | CLAIM(2) by reading ram-tier.sh line by line (HEAD) | l.18 sources ram-write.sh. HOT-bound and wrapped: l.45 pre-check mkdir; l.46 mkdir HOT; l.52 restore mkdir+rsync; l.54 mkdir + ionice rsync + rsync; l.57 swap-window `rsync --update`; l.61 restore-missing mkdir+rsync. Plain by design: l.46 `mkdir COLD`, l.55 `ln -sfn`/exchange and l.56 `mv -T` (they write beside D on disk, the symlink is the only HOT-named thing), l.58 `mkdir COLD`+`ionice rsync HOT->COLD`, l.61 `ln -s` (D's parent, disk), `log()` (COLD), `sync` l.65-66 (COLD-bound `rsync --delete`). No HOT-bound write left plain. TRUE |
| 6 | fake systemd-run + recorder wrappers (mkdir rsync ln mv ionice cp) on PATH, fake findmnt, mountinfo fixture, tmp HOT on the fixture tmpfs, tmp COLD/home on "/" ext4; `ram-tier.sh ensure` (tier a real dir + restore a missing one), emptied HOT -> `ensure`, `sync` | 10 scope argvs (`--user --scope -q --slice=ramdisk.slice -- ...`), every one HOT-bound; recorder shows every COLD-bound mkdir/rsync, `ln`, `mv -T` PLAIN and every HOT-bound mkdir/rsync SCOPED; rc 0 all three runs. TRUE (matches the node's pinned `== 10`) |
| 7 | pre-check branch (fake findmnt fails until HOT exists, HOT absent) | `mkdir -p HOT` appears scoped before the l.46 one (2 scoped mkdirs of HOT). Not covered by T2 (its findmnt always says tmpfs) but holds |
| 8 | F2 as written (HOT write without the ramdisk.slice scope argv, or a COLD-bound write wrapped) | NOT fired |
| 9 | F3 `git grep -nE systemd-run` on guard/ram-tier.sh and ram-write.sh at HEAD; `bash -n ram-tier.sh` | 0 hits (rc 1); syntax ok. NOT fired |
| 10 | `ram-tier.sh status` on MAIN (read-only) | TIERED x2, hot 323M/53M, tmpfs 42%: unchanged shape |
| 11 | tests, one file per run, HEAD tree, lock polled: test_ram_write_charge.py / test_ram_worktrees.py / test_box_guard.py / test_guard_init_cells.py / test_bin_help_smoke.py | 17 passed / 10 passed / 7 passed / 31 passed / 73 passed 8 skipped; 0 failed (the +3 rows R1 T1 T2 are the 17) |
| 12 | CEILING `git diff --numstat deaa32675 cd8ca3914` | mem_cap.py +1/-1 (net 0 <= +2); ram-tier.sh +7/-6 (7 added <= 8; the node counts 7 changed lines); test_ram_write_charge.py +37 (<= +40); ram-write.sh +2/-2 (a header comment naming ram-tier.sh as a third sourcer: NOT in FILE SCOPE, comment only, harmless); experiment node +37. kids 1, 0 USD, tier-0 |
| 13 | strict-xfail rows for this row (`git grep` xfail / strict in test_ram_write_charge.py; g7556 in the xfail files) | none exist (I left none in the parent check); nothing to un-mark |
| 14 | open residues on card-sanctuary-master / card-director-general-3 for g7556 / ram-tier / ramw | only the done/landing lines (cd8ca3914 "g7556 fork" in SM's card, d73bf50bf in DG3's); no open residue names this row; none re-raised |
