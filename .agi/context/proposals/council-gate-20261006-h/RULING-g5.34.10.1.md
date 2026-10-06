# ONE ruling — goal:g5.34.10.1 — DESIGN

**Pen:** self-perpetuating · **Lenses:** alive · all-is-one  
**Design:** `g5.34.10.1-grid-sync.md`  
**Leaf tip:** posts/sanctuary-master `282b236cd` (parent goal:g5.34.10 `d291fa3ab`)  
**Ask boxes (re-queue if consumed by concurrent g5.4.1.3.1):** see ready-for-gate

## Verdict

**PASS** — design sufficient for a later DG build leaf. **DG held** until parent SM gate.

## Must-carry (short)

1. **Flip only** `cron:crons` frontmatter: `cadences.grid_sync.enabled` false→true; `cadences.branch_push.enabled` false→true (schedule `7 * * * *` + `every_mins: 5` / `mirror_towns: true` already set). Evidence: 2026-10-05 policy-off thoughts.
2. **Keep** `grid.storage_trunk=refs/grid/et-grok-pilot` in `.agi/config.json`; never write `refs/grid/local-maxxing`.
3. **Apply** from main checkout `/data/work/agi` via `crons.py apply --unit-dir ~/.config/systemd/user` after MUR land — not from linked worktree; no invent ramdisk/agi-ram-main.
4. **Built-in lines:** `*/5` = `grid.py commit --all` + `push-changed` + self-reapply; `:07` = `git push origin <branch>`.
5. **Post-land catch-up:** Prime/ops `grid.py commit --all` under `refs/grid/et-grok-pilot` until NEW falls; falsifier via `grid.py status` + crontab presence.
6. **NOT AA3** — do not retire grid writes; do not fight g5.4.1.3 encapsulate-slice.
7. **Loop-only / NO-run now** — no Prime-direct flip; leave season3 tip; no wave-2 / g5.4.1.3.1 coupling; never git rm.

## Residues (non-blocking)

- Whether mirror_towns lines are noisy on a box with no `refs/heads/<town>/*` yet → already inert by design (rc0); DG may note in build.
- Exact operator identity for catch-up (Prime vs Belam ops) → parent SM gate / Belam land notes.
- Concurrent g5.4.1.3.1 council may have held original ask tips — re-queue is SM's; does not reopen this ruling.

## Ready-for-gate

Council PASS complete. **Parent runs SM gate next.** This package does **not** mint DG leaves, does **not** wake Belam, does **not** touch wave-2 / g5.35.* / season3 tip / g5.4.1.3.1.

## Out of scope

goal:g5.4.1.2 · goal:g5.4.1.3 / g5.4.1.3.1 · AA3 · season rollover run · agi-ram-main invent · wave-2
