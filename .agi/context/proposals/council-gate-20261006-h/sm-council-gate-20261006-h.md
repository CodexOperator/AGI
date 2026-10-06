# SM council gate 2026-10-06-h — goal:g5.34.10.1 (ET grid_sync re-enable) PASS

**Gate:** sanctuary-master · **Base tip:** posts/sanctuary-master `e1912a41d` (after wave-2 council land -i; prior g5.4.1.3.1 @ c49966d07)  
**Ruling land:** `1611d451c` · design leaf `282b236cd` · parent `d291fa3ab`  
**Sources:** `RULING-g5.34.10.1.md` · `g5.34.10.1-grid-sync.md` · lenses · `sm-ready-for-gate-20261006-h.md` (proposals/council-gate-20261006-h/)  
**Council:** self-perpetuating (pen) · alive · all-is-one  
**Seat PASS boxes:** alive 903dd318d @ 639fb78cc · aio 0a8f5422e @ 88606e1fa · sp 8ae8126bc @ 9016f393e  
**Scope:** Wave-2 tip `528aed6f3` / DG4 `ae180ab6d` untouched. g5.4.1.3.1 / g5.4.1.3.2 untouched. `core/season3/main` tip untouched. Belam NOT contacted. Never git rm. Master untouched.

## OWNER CORRECTION (Shael 12:55 ET via plan-master, verbatim)
> "We don't need to do a grid commit the capsule wraps each filesystem wrote into a commit"

**DROP** post-land `grid.py commit --all` catch-up from g5.34.10 / g5.34.10.1 entirely. Capsule (g5.4.1.3.*) wraps each FS write into a commit — **no separate catch-up grid commit**. No Prime-vs-Belam-ops catch-up-operator decision (residue closed by owner).

**KEEP:** re-enable ET `grid_sync` (+ optional `branch_push` :07 like LT) via `crons.py apply`; NOT AA3.

## Verdict

| leaf | verdict |
|---|---|
| **goal:g5.34.10.1** | **PASS** — design sufficient (with owner correction above); DG hold lifted for build leaf below |
| **goal:g5.34.10.2** | **GO** — DG4 BUILD flip `cron:crons` cadences + post-land apply notes (no catch-up) |

## SM stamps (ACCEPT)

| id | stamp |
|---|---|
| **Must-carry 1** | ACCEPT — flip only `cron:crons` frontmatter: `cadences.grid_sync.enabled` false→true; `cadences.branch_push.enabled` false→true; keep `every_mins:5` / `mirror_towns:true` / `schedule: 7 * * * *` |
| **Must-carry 2** | ACCEPT — keep `grid.storage_trunk=refs/grid/et-grok-pilot` in `.agi/config.json`; never write `refs/grid/local-maxxing` |
| **Must-carry 3** | ACCEPT — apply from main checkout `/data/work/agi` via `crons.py apply --unit-dir ~/.config/systemd/user` after MUR land — not from linked worktree; no invent ramdisk/agi-ram-main |
| **Must-carry 4** | ACCEPT — built-in renderer lines stay: `*/5` = grid.py commit --all + push-changed + self-reapply; `:07` = git push origin \<branch\> (re-enable = flip flags; do not rewrite renderer) |
| **Must-carry 5 (WAS catch-up)** | **DROP** — owner Shael 12:55: no post-land `grid.py commit --all`; capsule wraps FS writes. Falsifier no longer requires NEW-count drain via operator catch-up |
| **Must-carry 6** | ACCEPT — NOT AA3; do not retire grid writes; do not fight g5.4.1.3 encapsulate-slice |
| **Must-carry 7** | ACCEPT — loop-only / NO-run now; no Prime-direct flip; leave season3 tip; no wave-2 / g5.4.1.3 coupling; never git rm |
| **R-mirror_towns** | ACCEPT as non-blocking residue — inert until `refs/heads/<town>/*` exist; DG may note in build |
| **R-catch-up-operator** | **CLOSED** by owner correction — no Belam/Prime decision |
| **Belam / MUR** | ACCEPT hold — DG builds first; parent may MUR later; this gate does not wake Belam |
| **Assignee** | ACCEPT **director-general-4** only — no fan-out map in graph/docs for this leaf; one builder |

## Must-carry (DG4 on g5.34.10.2)

| # | contract |
|---|---|
| C1 | Edit `.agi/nodes/.geometry/crons.md` (`cron:crons`): `cadences.grid_sync.enabled: true` and `cadences.branch_push.enabled: true` only — no other cadence flips |
| C2 | Do **not** change `grid.storage_trunk` (already `refs/grid/et-grok-pilot`) |
| C3 | Document post-MUR land apply: from `/data/work/agi` run `python3 extensions/agi/bin/crons.py apply --unit-dir ~/.config/systemd/user` (Belam/ops after land — not this build commit's runtime) |
| C4 | **No** post-land `grid.py commit --all` catch-up (owner 12:55); capsule path owns per-write commits |
| C5 | NOT AA3; never write `refs/grid/local-maxxing`; no invent agi-ram-main/ramdisk |
| C6 | Falsifier: live `crons.md` has both enabled:true; after apply, crontab contains `*/5` grid line and `:07` branch push; season3 tip unchanged; no catch-up script/docs invented |
| C7 | Engine.v4 Write/Edit + agi-turn (never write.py); never git rm; Master untouched; leave wave-2 / g5.4.1.3.* alone |

## Falsifiers (pack)
1. `git show HEAD:.agi/nodes/.geometry/crons.md` shows `grid_sync.enabled: true` and `branch_push.enabled: true`.
2. `grid.storage_trunk` still `refs/grid/et-grok-pilot` in `.agi/config.json`.
3. No new catch-up / `grid.py commit --all` operator runbook added under this leaf.
4. No AA3 / local-maxxing / ramdisk invent; `core/season3/main` tip unchanged.

## GO
**director-general-4** released on **goal:g5.34.10.2** (BUILD). Loop: DG commit on loop branch → box SM PASS → climb DG2→DG1 → SM MUR → council → Belam land. Do **not** wake Belam from this seat. Leave wave-2 / g5.4.1.3.* / season3 tip alone.

## Non-goals
AA3 · post-land catch-up grid commit · season3 tip rewrite · wave-2 coupling · g5.4.1.3.* edits · inventing multi-DG fan-out · Belam wake · Master · write.py · agi-ram-main invent
