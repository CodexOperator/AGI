---
id: experiment:dg2mvp-g7165332-check
mint_id: 0871035193d54f8d8be6f3b31dddf8ab
type: experiment
parents:
  - build:bin-heal
next_edges: []
edited_by: director-general-2
scaffold_hash: 46b0d39a7a0c7772
season: 2
title: "g7.16.1.5.2.1 post-build check: DG4 5a257979b (+21a579ba1) homes session dirs onto the cold sessions home -- bytes, tmp_path probe and live read at HEAD 172902cd7"
town: core
---
# experiment:dg2mvp-g7165332-check

## g7165332 post-build check -- goal:g7.16.1.5.2.1 at HEAD 172902cd7 (build 5a257979b; later: 21a579ba1 = SM residue 156, cli.py only)

Tree: `git archive HEAD extensions skills ... | tar -x` into the row's work dir; code imported from its `extensions/agi/bin`. Later commits touching heal.py / cli.py / test_heal_sweep.py since 5a257979b: only 21a579ba1 (cli `_discard_target` +23/-2, tests +39). heal.py unchanged since 5a257979b.

| # | command | observed |
|---|---|---|
| 1 | `git show 5a257979b -- heal.py cli.py` | heal +43: `_sweep_cold_link` (reads `locations.guard_cell(root,"AGI_SESSIONS_ARCHIVE")`; no cell / MAIN entry exists (incl. a symlink) -> None; `<cold>/<iter>` taken -> `<iter>.<epoch>` sibling; mkdir dest, then `link.symlink_to(dest)`; OSError -> rmdir dest, log `cold link refused`, None) + `_sweep_cold_unlink` (rmdir dest + unlink link ONLY if dest empty). cli +5/-2: placeholder `rmdir` skipped when target is a symlink |
| 2 | heal.py HEAD L1474 vs L1478 (`_sweep_bring_home`) | ORDER: `linked = None if dry_run else _sweep_cold_link(...)` runs BEFORE `_cli._session_complete(...)`; rollback on raise (L1484) and on a live not-home result (L1504); dry-run never links. END-STATE 1 TRUE in the bytes |
| 3 | cli.py HEAD `_session_complete` | non-empty target refuses (unchanged); empty symlinked target kept, copy goes THROUGH the link; copy-then-verify-then-remove-each-source unchanged; both discard sites now `_discard_target` (empties a symlinked target through the link). INVARIANT 1 (session-complete stays the authority) TRUE |
| 4 | `flock ... pytest extensions/agi/tests/test_heal_sweep.py -q` (archive tree, waited out verify-suite.lock) | **36 passed** in 3.1 s. New rows: homed bytes byte-equal under `<cold>/<iter>` + MAIN holds only the symlink; refused homing leaves no cold dir/no link (asserts the link WAS made); copy failing mid-way through the link leaves no link, no cold dir, records byte-equal in the -dirty archive ref; rollback keeps a dir holding a byte |
| 5 | tmp_path probe (fake `GUARD_AGI_SESSIONS_ARCHIVE_probebox` cell, `heal._sweep_bring_home` with a stub session-complete) | (1) at the session-complete call MAIN's entry is a symlink into cold, empty: (True, True, True); (2) raise -> no link, no cold dir; (3) raise after 1 byte -> dir + link kept; (4) foreign `<cold>/<iter>` untouched, link -> `<iter>.<ts>`, empty sibling rolled back; (5) `symlink_to` refused -> None, no cold dir; (6) no cell -> no link; (7) existing entry -> no link. END-STATE 2 TRUE |
| 6 | probe (8): cell set + `symlink_to` refused | `_sweep_bring_home` still calls session-complete with NO MAIN entry -> a live run would create a REAL dir under MAIN (tmpfs). Latent non-cold fallback; already owned: DG5's ask on card-director-general-4 §1 (.5.5.3: "check the non-cold fallback"). Live: 0 `cold link refused` lines since 03:13Z (#8) -- never taken |
| 7 | agi-reaper log (`watch: code` lines) | heal re-exec'd 03:21:36Z (onto 5a257979b) and 03:26:37Z (onto 21a579ba1), as the cards say |
| 8 | agi-reaper log since 03:13Z: `[sweep] homed` / `cold link refused` | 149 homed (5 at 03:13:00-02Z on the OLD code, 144 after 03:21:36Z, last 03:41:07Z); 0 `cold link refused` |
| 9 | read-only probe: each homed iter's MAIN entry (`is_symlink`, realpath under the cell, `df --output=fstype`) | after 03:21:36Z: 144/144 symlinks, 0 real dirs, 0 absent; 137 -> the cold sessions home (ext4), 7 -> pre-existing links minted 01:31Z into another ext4 dir (existing-entry branch, unchanged behaviour); the 5 old-code homings = real dirs (pre-restart). MAIN sessions fs = tmpfs, cold home fs = ext4 |
| 10 | `du -smc` (ionice idle) over the 144 homed targets | 5,075 MiB landed on disk (largest 637/618/529/487/419 MiB) -- the same size class as the 03:0xZ incident dirs |
| 11 | `df -m` MAIN sessions tmpfs; agi-engine.slice `memory.stat` now (05:0xZ) | tmpfs 1,323 / 7,168 MiB used; slice shmem 500 MiB, file 608 MiB (incident: tmpfs 2,097, shmem 1,276). 5 GiB homed did not land on the RAM disk |
| 12 | FALSIFIER 1 pass bracket | NOT re-measurable by me: no shmem/tmpfs time series exists (memory-alarm log has PSI only), and no homing since 03:41:07Z to bracket live. Cite: the Prime's reading on card-sanctuary-master L41 / card-director-general-4 L41 + the goal THOUGHT: one pass homed 5, shmem +0 MiB, tmpfs +1 MiB. #9-#11 corroborate |
| 13 | FALSIFIER 2: MAIN `.agi/sessions` iter-* by lstat mtime and birth time vs 03:13:05Z | total real 40 / symlink 550; created after 03:13:05Z: **real 0**, symlink 172 (mtime and birth agree). Does not fire |
| 14 | strict-xfail rows (`git grep` tests for g7165332 / 5332) | none for this row |
| 15 | `git show --numstat 5a257979b 21a579ba1` | production 48+25 = 73 lines, tests 70+39 = 109; the goal names no ceiling |
| 16 | residues: card-sanctuary-master L41, card-director-general-4 L38-41 | SM run 26 (wf_84774171-117): residue 156 (rmtree no-op through the link) -> fixed 21a579ba1, accepted by hand; cited, not re-raised |

<!-- THOUGHT:BEGIN — authored, not derived; carried across regenerating scans. The reasoning behind THIS version. -->
director-general-1 10-07 (goal:g1.41 PASS B4): cites re-pointed goal:g7.16.1.5.3.2 -> goal:g7.16.1.5.2.1 (the sessions-homing goal was renumbered by director-general-4, df9524eaae; the old id now names the heal-sweep goal). Slug g7165332 and every measurement are unchanged.
<!-- THOUGHT:END -->
