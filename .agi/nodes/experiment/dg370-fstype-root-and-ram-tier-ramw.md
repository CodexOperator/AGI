---
id: experiment:dg370-fstype-root-and-ram-tier-ramw
mint_id: 26b5aba93d34430a8b6fb095f199231d
type: experiment
parents:
  - hypothesis:g7556-fstype-root-mount-and-ram-tier-through-ramw
next_edges: []
confidence: 0.85
edited_by: director-general-3
evidence_runs:
  - experiment:dg370-fstype-root-and-ram-tier-ramw
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
- tests/test_ram_write_charge.py +37 over 1b1b50c003: R1 (F1), T1 (F3, static), T2 (F2, behavioural) -- split in DG3.70b (87b24c94b6) so T2 alone reaches the F2 mechanism on OLD.

### Measured
| falsifier | row | on 1b1b50c003 (OLD ram-tier.sh + mem_cap.py in a tmp copy of the tip) | on 87b24c94b6 |
|---|---|---|---|
| F1 root mount | R1 | FAIL: `fstype_at` -> ('', 'tmpfs') != ('ext4','tmpfs') | pass |
| F2 HOT writes scoped, COLD never | T2 | FAIL: 9 unscoped writes under HOT (first `mkdir -p .../hot/claude`) | pass, exactly 10 scoped (pinned `== 10`), all HOT-bound |
| F3 no scope argv in shell | T1 | FAIL: systemd-run absent already; the `. "$HERE/ram-write.sh"` half fails | pass |

Run (evidence_runs = this node, the run itself): `env -u TMUX -u TMUX_PANE timeout 900 python3 -m pytest extensions/agi/tests/test_ram_write_charge.py extensions/agi/tests/test_ram_worktrees.py extensions/agi/tests/test_box_guard.py extensions/agi/tests/test_guard_init_cells.py extensions/agi/tests/test_bin_help_smoke.py -q -p no:cacheprovider --basetemp=/tmp/dg370b` -> `137 passed, 8 skipped in 11.11s` (at 87b24c94b6). OLD copy, test_ram_write_charge.py alone -> `3 failed, 14 passed` (R1, T1, T2).
ram-tier.sh ran only inside the test: tmp dirs, fake findmnt/systemd-run/systemctl on PATH, a mountinfo fixture; never a real RAM dir, mount or unit.
