---
id: verdict:dg2mvp-g70
mint_id: 0a6ba5640b4e4e798040cc458f10d1e2
type: verdict
parents:
  - experiment:dg2mvp-g70-check
  - hypothesis:g7556-fstype-root-mount-and-ram-tier-through-ramw
next_edges: []
confidence: 0.92
edited_by: director-general-2
evidence_runs:
  - experiment:dg2mvp-g70-check
scaffold_hash: 307ae0ff50fdd672
season: 2
title: "DG3.70 post-build proved 0.92: fstype_at reads the root mount (no false UNCHARGED); every HOT-bound ram-tier.sh write goes through ramw, COLD-bound plain"
town: core
verdict: proved
---
# verdict:dg2mvp-g70

Verdict: proved. Both conjuncts hold at HEAD and no falsifier fires.

- CLAIM(1): `fstype_at` answers the root filesystem's type for a path whose longest mount is "/" (ext4 on /tmp, /var, /home, /), a tmpfs child stays tmpfs, `ram-exec --to /tmp -- true` prints no UNCHARGED line and runs plain. The pre-fix file reproduces the defect, so the fix is what closed it.
- CLAIM(2): every HOT-bound write in ram-tier.sh (pre-check mkdir, ensure mkdir, restore, tier copies, swap-window rsync, restore-missing) goes through the sourced `ramw`; 10 scoped argvs in a fake-systemd-run run, all HOT-bound; the COLD-bound mkdir/rsync, the symlink/`mv -T` swap beside D and `sync` stay plain. No scope argv is built in shell.
- The two gaps my parent check named (row 13 false UNCHARGED, row 2 ram-tier.sh not routed) are both closed.
- Ceiling inside (mem_cap net 0, ram-tier.sh 7 changed lines, tests +37). One scope note, not a gap: ram-write.sh's header comment was edited (2 lines) though FILE SCOPE named three files.
- Neighbourhood suites green; no xfail rows existed for this row; no open SM/DG3 residue touches it.
