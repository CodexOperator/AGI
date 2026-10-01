---
id: experiment:dg370-fstype-root-and-ram-tier-ramw
mint_id: 26b5aba93d34430a8b6fb095f199231d
type: experiment
parents:
  - hypothesis:g7556-fstype-root-mount-and-ram-tier-through-ramw
next_edges: []
confidence: 0.85
edited_by: director-general-3
scaffold_hash: deffefa20256c13c
season: 2
title: fstype_at answers the root mount and ram-tier.sh writes into HOT through ramw
town: core
verdict: proved
---
# experiment:dg370-fstype-root-and-ram-tier-ramw

## Round DG3.70 -- code 650b61e004 on trunk 1b1b50c003

Dispatch line answered: config-max none (no new cell: HOT/COLD/DIRS are already config:guard cells) · template-max none · code: one 1-line fix in `fstype_at` + ram-tier.sh sources ram-write.sh and prefixes its HOT-bound writes with `ramw`.

### What changed
- `mem_cap.fstype_at`: the match is `p.startswith(mp.rstrip("/") + "/")`, so the "/" mount no longer builds "//" (mem_cap.py net 0).
- `guard/ram-tier.sh`: `. "$HERE/ram-write.sh"`; `ramw` on every write INTO HOT -- the pre-check mkdir, ensure's mkdir HOT, the restore mkdir+rsync, the tier mkdir + both copies, the swap-window `rsync --update`, the restore-missing mkdir+rsync. The swap itself (`ln -sfn` / renameat2 / `mv -T`) writes beside D on disk, so it stays plain; the COLD-bound rsyncs (ensure seed, `sync`) are untouched. 7 changed lines (6 edited + 1 added).
- tests/test_ram_write_charge.py +34: R1 (F1), T1 (F2+F3).

### Measured
| falsifier | row | on 1b1b50c003 | on 650b61e004 |
|---|---|---|---|
| F1 root mount | R1 | FAIL: `fstype_at` -> ('', 'tmpfs') != ('ext4','tmpfs') | pass |
| F2 HOT writes scoped, COLD never | T1 | FAIL: 9 unscoped writes under HOT (first `mkdir -p .../hot/claude`), checked with the static assert removed | pass, >= 8 scoped, all HOT-bound |
| F3 no scope argv in shell | T1 (static) | systemd-run absent already; the `. "$HERE/ram-write.sh"` half fails | pass |

Neighbourhood: test_ram_write_charge + test_ram_worktrees + test_box_guard + test_guard_init_cells + test_bin_help_smoke -> 136 passed, 8 skipped in 16.25s.
ram-tier.sh ran only inside the test: tmp dirs, fake findmnt/systemd-run/systemctl on PATH, a mountinfo fixture; never a real RAM dir, mount or unit.
