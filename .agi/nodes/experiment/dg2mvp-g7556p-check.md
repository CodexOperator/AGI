---
id: experiment:dg2mvp-g7556p-check
mint_id: a3b14314776344cea58a98b858933b6f
type: experiment
parents:
  - hypothesis:g7556-guard-ram-writes-charge-ramdisk-slice-through-one-shell-entry
next_edges: []
edited_by: director-general-2
scaffold_hash: 6baf7be2926b688a
season: 2
title: "g7556 post-build check: guard RAM writes charge ramdisk.slice through the one shell entry (measured live, 1 MiB write)"
town: core
---
# experiment:dg2mvp-g7556p-check

## g7556 post-build check (build 627c94a040; HEAD archive tree; MAIN's working copy never tested)

| # | command | observed |
|---|---|---|
| 1 | CLAIM(1): `mem_cap.py ram-exec --to P -- <argv>` -> `ram_argv` -> `locations.ram_write_argv` -> `scope_argv(.., RAM_SLICE)`; dry call of `ram_argv(['true'])` | TRUE: wrapped (7 tokens), `--scope`, `--slice=ramdisk.slice`; user_manager_reachable()=True |
| 2 | CLAIM(2) ONE entry: `git grep` for every RAM-dir write in guard/*.sh + bin | ram-main.sh (mkdir/touch/rsync x2, bind_in) and session-sweep.sh move() all go through `ramw` = guard/ram-write.sh (sourced by both); dispatch.py:822 uses `locations.ram_write_argv` (Python, same builder). TRUE for the two scripts. NOT routed: ram-tier.sh (HOT = a dir on the RAM disk; mkdir/rsync/ln/mv at :44-60 are plain) -- demoted at DH.DG3.48 ("out of claim wording"), cited not re-raised |
| 3 | LIVE write, 1 MiB (`ram-exec --to <scratch on RAM disk> -- sh -c 'cat /proc/self/cgroup; head -c 1048576 /dev/zero > <scratch>'`), then `rm` | child cgroup = `<user-slice>/ramdisk.slice/run-uNNNN.scope` (read from the child's own /proc/self/cgroup); rc 0; stderr empty |
| 4 | ramdisk.slice memory.current / shmem (bytes): before (x2) | 164511744 / 147804160 (stable) |
| 5 | ... immediately after the write | 166264832 / 148852736 = shmem +1048576 exactly; tmpfs used +1048576 |
| 6 | the CALLER's own scope (agent slice) shmem before / after | 6893568 / 6893568 = unchanged (not charged to the caller) |
| 7 | after `rm` (immediately, then +2 s) | ramdisk memory.current 164806656 then 164573184; shmem back to 147804160 (the slice freed on removal); file gone |
| 8 | dry: `ram-exec --to <disk dir> -- sh -c 'exit 7'` | rc 7, no stderr, ran plain (F2 holds) |
| 9 | dry: `ram-exec true` / `ram-exec --to X --` | rc 2 both, named usage (matches DH.DG3.48 item 5) |
| 10 | dry: `fstype_at` of RAM mount, an overmounted MAIN path, a not-yet-existing RAM child, a disk path | tmpfs / tmpfs / tmpfs / ext4 -- filesystem, not prefix |
| 11 | F4: `git grep systemd-run` in ram-main.sh, session-sweep.sh, ram-write.sh | no hit (0 lines) |
| 12 | `bash -n` on the three guard scripts | ok |
| 13 | DEFECT: `fstype_at('/tmp')`, `fstype_at('/var')`, `fstype_at('/home')` (paths on the root mount) | '' -> `ram-exec --to /tmp -- true` prints "mount table unreadable -- write ran UNCHARGED" (rc 0, argv ran plain). Cause: mountpoint "/" is `rstrip('/')`'d to '' -> `or "/"` -> compared as `p.startswith("//")`, never true. Harmless to the charge (fails open, disk write is plain either way) but a FALSE alarm on every root-fs disk-bound `ramw` |
| 14 | tests, one file per run (HEAD tree): test_ram_write_charge 14p; test_ram_worktrees 10p; test_mem_cap_{cache_config 10, override 8, probe_cache 13, tasks_max 14}p; test_heal_mem_cap 4p; test_box_guard 7p; test_guard_init_cells 31p; test_bin_help_smoke 72p/8s | all green, 0 failures |
| 15 | CEILING `git show --numstat 627c94a040`: mem_cap.py +82, ram-main.sh +5/-3, ram-write.sh +7 (new), session-sweep.sh +9/-6, test_ram_write_charge.py +258 | chain caps (DH.48 35 + DH.50 +6 + DH.57 +16 = 57): mem_cap.py +82 is OVER by 25 (docstrings count); guard scripts net +6 cap: +14 add / -9 del = net +5 (+7 file = +12, shared file was allowed for); tests 258 vs 220+40 = 260 under |
| 16 | strict-xfail rows (git grep w2c / g7556 / xfail in tests/) | none exist for this row (the w2c hits are the unrelated mint-twin rows) |
| 17 | open residues on card-sanctuary-master / card-director-general-3 | none name g7556 / ram-write; nothing cited to re-raise (DG3 card: "RAM trees removed", landed 627c94a040) |
