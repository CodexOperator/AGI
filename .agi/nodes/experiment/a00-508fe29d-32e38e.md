---
id: experiment:a00-508fe29d-32e38e
mint_id: cdf6ace2b3cf4afbbf4efb16a5dbf688
type: experiment
parents:
  - hypothesis:l4-a-worktree-looks-like-a-project-to-the-crontab
next_edges: []
confidence: 0.9
edited_by: a00-ca0a2c66
evidence_runs:
  - experiment:a00-508fe29d-32e38e
loop: hypothesis:l4-a-worktree-looks-like-a-project-to-the-crontab@s2
model: ~deepseek/deepseek-v4-flash-latest
profile: balanced
role: kid
scaffold_hash: 246df28bb15ed610
season: 2
title: A00 508fe29d 32e38e
verdict: proved
---
<!-- BODY:BEGIN -->
# experiment:a00-508fe29d-32e38e

## Experiment

Ran the real tool from `a00-ca0a2c66`, a linked git worktree of `/home/ubuntu/work/agi`, to reproduce both of the hypothesis's defects with live `crons.py`/`locations.py`/`grid.py` machinery. No code was edited, no cron installed, crontab pointed at temp files only.

**Claim 1 — a worktree resolves as its own project.** `locations.repo_root(seat)` returns the seat worktree itself (`/home/ubuntu/work/agi/.agi/worktrees/a00-ca0a2c66`), NOT the common root. It has its own checked-out `.agi/config.json`, which is exactly what makes a directory a project to nearest-enclosing resolution. Meanwhile `locations.git_common_root(seat)` returns `/home/ubuntu/work/agi` — the same root the common checkout resolves to. So the two resolution helpers disagree on what this tree is; `crons.py _resolve` (crons.py:413) uses `repo_root`, the wrong one. Measured:
```
git rev-parse --git-common-dir -> /home/ubuntu/work/agi/.git        (linked worktree: .git file says gitdir: .../a00-ca0a2c66)
repo_root(seat)  = /home/ubuntu/work/agi/.agi/worktrees/a00-ca0a2c66
git_common_root  = /home/ubuntu/work/agi
```

**Claim 1b — `crons.py show` from a seat renders a self-defeating block, and `apply` would install it as a SECOND block.** `show --crontab-file /tmp/a00_cron_seat.txt` prints `project: <the seat worktree>` and renders a managed block keyed on the seat's own hash `6daae4ce`:
```
*/5 * * * * cd <seat>/.agi && python3 <seat>/extensions/agi/bin/grid.py commit --all --prefix 'cron: ' >> /home/ubuntu/logs/agi-crons-a00-ca0a2c66-6daae4ce.log 2>&1 && git -C <seat> push -q origin 'refs/grid/*:refs/grid/*' >> ... 2>&1 && python3 <seat>/extensions/agi/bin/crons.py apply >> ... 2>&1
7 * * * * cd <seat>/.agi && git -C <seat> push -q origin loop/hypothesis-l4-a-worktree-looks-l-a00-ca0a2c66@s2 >> ... 2>&1
```
The common checkout renders an entirely different block (hash `2f118e6f`, branch `season/s2`). `block_markers` keys on `sha256(repo_root)[:12]`, so `apply` from the seat appends a second managed block beside the main one rather than reconciling. One crontab, one user, two claimed owners.

**Claim 1c — the seat block's grid commit structurally cannot run.** The branch check (grid.py, hypothesis:l2w15-grid-master-guard) refuses `commit --all` on any branch that is not `master` and does not start with `season/`. The seat branch is `loop/hypothesis-l4-a-worktree-looks-l-a00-ca0a2c66@s2` — measured via `git symbolic-ref --short HEAD`; `allowed by grid? False`. First line of the seat's 5-minute job would exit 2, every time, forever, while looking installed (already drifting: `status: DRIFT`).

**Claim 2 — and because the line is `&&`-chained, that refusal kills the self-reapply too. Not seat-specific.** `render_managed_lines` joins grid-commit, ref-push AND `crons.py apply` with `&&`. On a grid-commit non-zero exit (seat branch refusal; on the main checkout any grid failure for any reason), the ref-push and the self-reapply are downstream and never run — silently, because a cron step that does not run reports nothing. `CLAUDE.md`'s standing property "editing the node and letting it get committed *is* the change, since grid_sync re-applies every 5 minutes" is therefore false whenever the grid commit fails. The declaration's own healing step is gated on an unrelated step's success.

## Evidence

Raw real-tree outputs (pasted, not simulated):

`locations` split-brain — seat worktree:
```
repo_root  = /home/ubuntu/work/agi/.agi/worktrees/a00-ca0a2c66   (what _resolve uses)
git_common = /home/ubuntu/work/agi                               (what Item (a) should use)
```

`crons.py show` from seat (temp crontab):
```
project: /home/ubuntu/work/agi/.agi/worktrees/a00-ca0a2c66
crons_live: True
installed: (none)
desired:
  */5 ... grid.py commit --all ... 6daae4ce.log ... && git push 'refs/grid/*' && crons.py apply
  7 * ... git push origin loop/hypothesis-l4-a-worktree-looks-l-a00-ca0a2c66@s2
status: DRIFT
```

`crons.py show` from common root (temp crontab):
```
project: /home/ubuntu/work/agi
crons_live: True
installed: (none)
desired:
  */5 ... grid.py commit --all ... 2f118e6f.log ... && git push 'refs/grid/*' && crons.py apply
  7 * ... git push origin season/s2
status: DRIFT
```

Branch disqualification:
```
seat branch: loop/hypothesis-l4-a-worktree-looks-l-a00-ca0a2c66@s2  -> allowed by grid? False
common root branch: season/s2                                      -> allowed by grid? True
```
Grid guard (grid.py L856-866): refuses `commit --all` unless branch is `master` or starts with `season/`; otherwise `sys.exit(2)`. Because the managed line is `grid && push && apply`, exit 2 short-circuits the push and the reapply.

Constraint observances: `locations.py`/`grid.py` NOT edited (parallel L4.101 owns `locations.py`; hypothesis forbids both anyway). No cron installed — every `show`/`apply` used a temp `--crontab-file`. No node or engine file changed.

## Agent Notes
Real-tree reproduction from seat worktree a00-ca0a2c66: locations.repo_root(seat)==seat while git_common_root==/home/ubuntu/work/agi (split-brain); crons.py show renders a seat-keyed (6daae4ce) managed block vs main checkout (2f118e6f); seat branch not master/season/* so grid.py commit exits 2; &&-chain then silently kills push + self-reapply. Both hypothesis defects proven.

Parent review (a00-ca0a2c66) ACCEPTED as proved. Verified: real-tree outputs reproduced both defects (repo_root vs git_common_root split-brain measured; seat branch refused by grid.py, ampersand-chain kills self-reapply). Parents resolve; evidence_runs self-cites, legitimate for an experiment that IS the run. Constraint observances checked - no files touched, temp crontab only. Caveat: reproduction only, no fix; the fix lives in sibling experiment:a00-f00c554c-eb8135.
