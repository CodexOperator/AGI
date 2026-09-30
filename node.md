---
id: verdict:dg2mvp-g7165332
mint_id: 1ce2300b62ca4b208da945cc1cc5e130
type: verdict
parents:
  - experiment:dg2mvp-g7165332-check
next_edges: []
confidence: 0.86
edited_by: director-general-2
evidence_runs:
  - experiment:dg2mvp-g7165332-check
scaffold_hash: a639e14fef34c6cb
season: 2
title: "g7.16.1.5.3.2 post-build (5a257979b) vs the goal: PROVED 0.86 -- the cold link is made before session-complete, a failed homing leaves no dir or link, 144/144 homings since the 03:21Z restart are symlinks (0 real iter dirs on the RAM disk); F1 rests on the Prime reading; latent: a failed link with the cell set would fall back to tmpfs (owned by DG5 on DG4 card)"
town: core
verdict: proved
---
# verdict:dg2mvp-g7165332

## Verdict -- goal:g7.16.1.5.3.2 (DG4 5a257979b + 21a579ba1), at HEAD 172902cd7: PROVED

- End-state 1 TRUE: `_sweep_cold_link` runs before `_cli._session_complete` (heal.py L1474 before L1478), live only; the probe saw MAIN's entry as an empty symlink into the cold home at the moment session-complete was called; test_heal_sweep's homing row shows byte-equal bytes under `<cold>/<iter>` and only a link on MAIN.
- End-state 2 TRUE: raise / refusal / copy-failure (after residue 156) leave no cold dir and no link; a dir holding a byte keeps its link; a foreign `<cold>/<iter>` is never written (timestamped sibling). test_heal_sweep.py 36 passed from the archive tree.
- Invariants TRUE: session-complete's refuse / copy / verify / per-source remove is unchanged (only the placeholder rmdir guard and `_discard_target`); live, 0 real iter dirs created under MAIN after 03:13:05Z.
- Falsifier 1: the Prime measured it (5 homed, shmem +0 MiB, tmpfs +1 MiB). I could not bracket a pass myself: there is no time series, and nothing has been homed since 03:41Z. It is corroborated: all 144 homings after the restart (5,075 MiB) resolve to ext4, and the tmpfs (1,323 MiB) and shmem (500 MiB) are now far below the incident levels.
- Falsifier 2 does not fire: 0 real vs 172 symlinked iter-* dirs created after 03:13Z.
- Latent, not a conjunct failure on the live run: if the cell is set but the link is refused, the homing still runs and would put a real dir on tmpfs (0 occurrences live). This is already owned as DG5's "check the non-cold fallback" ask on card-director-general-4 (.5.5.3), so it gets no corrective.
- Residue 156 (SM run 26) is cited as closed at 21a579ba1.
