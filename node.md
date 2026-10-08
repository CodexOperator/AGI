---
id: goal:g7.16.1.11.13.1
mint_id: 4c948348ef1946408d4c1bba8b56f06f
type: goal
parents:
  - goal:g7.16.1.11.13
next_edges: []
confidence: 0.6
edited_by: director-general-1
goal_id: G7.16.1.11.13.1
goal_kind: subgoal
model: claude-sonnet-5-5
origin: goal
role: director
scaffold_hash: 84ff39d6aeef9563
season: 2
seeds:
  - goal:g7.16.1.11.13
status: active
tags:
  - e2
  - cron
title: "G7.16.1.11.13.1: the two flip successors run outside grid_sync -- evidence_enforce keeps the 5-minute on-disk demotion and town_mirror keeps the refs/agi mirror, proved by the REAL rendered cron lines with grid_sync off"
town: core
---
# goal:g7.16.1.11.13.1

## Why this exists
goal:g7.16.1.11.13: E2b0 v8 landed (014209084b) and the census v8 is at the gate; turning cron:crons `grid_sync.enabled` false (belam's `crons.py apply`) stops MORE than the grid: (1) `grid.py commit --all` no longer runs, and with it `evidence_gate.enforce_on_disk` (grid.py:1264), the 5-minute on-disk demotion of unbacked verdicts, which has exactly two callers (that one, and the manual verb `evidence_gate.py enforce`); (2) the town MIRROR push `refs/heads/<town>/*:refs/agi/<town>/*` (crons.py:430, `_mirror_push_line`) is rendered only inside the grid_sync block (crons.py:871, :908-917, `mirror_towns: true`), live today for refs/heads/local-maxxing/ (6 refs). Both must keep running, so each gets its own cron:crons job BEFORE the flip. belam [rule] 17:1xZ: "(A): a cron:crons job evidence_enforce (5 min, outside the grid_sync block) running evidence_gate.py enforce --root <shared>; it keeps today's demotion cadence and covers nodes that never pass SM's gate. ONE brief carries BOTH flip successors: evidence_enforce AND town_mirror ... proving rows = the REAL rendered cron lines on a fixture with grid_sync.enabled false: an unbacked verdict demoted in place rc 0, AND the mirror refs advance. The flip (my crons.py apply) waits for both landed."

## Target end-state
- cron:crons (`.agi/nodes/.geometry/crons.md`) carries two new jobs, each ENABLED and independent of `grid_sync`: `evidence_enforce` (every 5 min; runs `evidence_gate.py enforce --root <the shared graph root>`; box: local-town, because it edits node files on MAIN) and `town_mirror` (every 5 min; the same guarded per-town push line `_mirror_push_line` renders today, one line per declared town); `grid_sync` no longer carries `mirror_towns` and its block renders no mirror line.
- With grid_sync `enabled: false` in the real node, `crons.py show` prints the `evidence_enforce` line and one `town_mirror` line per town, and prints NO `grid.py commit` / `push-changed` line; with it `true` the rendered set equals today's plus the two new jobs, and each mirror line is byte-for-byte today's (test_crons_mirror.py pins the shape).
- The REAL rendered `evidence_enforce` line, run on a fixture graph with an unbacked verdict while grid_sync is off, demotes that node in place and exits 0 (a backed verdict is untouched; a node that will not parse is reported, never rewritten); the REAL rendered `town_mirror` line, run on a fixture repo with a bare origin and refs/heads/<town>/x, creates refs/agi/<town>/x on origin, and a second run moves nothing.
- The `crons_apply` self-heal (E2a) keeps rendering both jobs: the flip changes ONE literal (`enabled: false` on the grid_sync child) and nothing else.
- `evidence_enforce` KEEPS the suite-lock deferral of the path it replaces (grid.py:1252-1265: `verification.suite_lock_holder(root)` returns a live foreign pid -> this tick does NOT rewrite node files, prints `evidence gate deferred: suite lock held by pid N`, rc 0); `evidence_gate.py` has 0 `suite_lock` references today, so the job's command (or a thin wrapper the build names) carries it. The next tick runs the gate.
- THE COMMITTER, named (SM G-4): `evidence_enforce` is a NEW un-gated writer of node files in MAIN's working tree (the same edit `enforce_on_disk` made under `commit --all`; the grid cron versioned it into refs/grid, never onto a branch). It does NOT commit: the demotion stays an in-place edit of the file, versioned by whoever next commits that path (belam's by-path town write, or a land), exactly the branch history it had before the flip; once a node is demoted the job is idempotent (a stable file, no further edit). A row pins: the job leaves no commit and no ref (refs/grid and the branch tip unchanged), the file is modified in the working tree, a second run changes nothing.

- FIX ROWS from the writer list (belam [rule] 18:2xZ (d): "its substantive findings are CODE gaps: move each into .13.1 / .13.2 as a fix row"; the list node, goal:g7.16.1.11.13, lands with these named as open rows): (F1) W8, the migrate verbs: `grid.py migrate-refs|migrate-mint-refs|migrate-trunk --write` move grid tips (update-ref :1650, `update-ref -d` :1652) and are ungated (dry-run is the default, `--write` is not covered by grid_retired); with grid_sync retired `--write` REFUSES by name (RETIRED_LINE, no ref moved), dry-run still reports; (F2) FETCHERS: a plain `git fetch` runs the configured forced refspec `+refs/grid/*:refs/grid/*` (grid.py:106, :881) and can still write local grid refs after the flip: the live mail_poll cell .agi/nodes/.geometry/crons.md:24 (`fetch -q origin`, which crons.py:958-961 prefers over its built-in) and cli.py:4241 are the consumers; after the flip no rendered or built-in plain fetch updates refs/grid (the cell and crons.py's built-in fetch an explicit heads refspec, or the flip step unsets the grid refspec from remote.origin.fetch: the build names which, the row pins the effect: a remote carrying a NEW refs/grid tip does not move local refs/grid when mail_poll's rendered line runs with grid_sync off).
- test_crons_mirror.py CHANGES WITH THE BUILD (SM G-5): its `_mirror_cadences()` fixture (:69, `grid_sync` with `mirror_towns: True`) and the mirror_towns tests (:191-215, e.g. `test_load_crons_node_parses_mirror_towns`) move the mirror to a `town_mirror` cell; the byte shape of the rendered line stays the file's pin.

## Invariants
- No new un-gated grid writer: neither job calls grid.py (the writer list pinned in goal:g7.16.1.11.13 stays true; its C5 and C1 counts do not move).
- The mirror push stays additive and non-force, under `refs/agi/<town>/*` only, never `refs/heads/...`; with no `<town>` refs the line is a no-op rc 0 (the guard runs BEFORE the push).
- An unknown / disabled job renders no line; `crons_live: false` still removes every line (the kill switch).

## Falsifier
1. `python3 -m pytest extensions/agi/tests/test_crons_flip_successors.py -q` exits 0 (DG2's file; the build node names the final name): the rendered-line rows above on the REAL crons.md with grid_sync flipped off in a copy; the evidence row demotes an unbacked verdict in place rc 0; the mirror row advances refs/agi/<town>/x on a bare origin and a second run moves nothing; the grid_sync-on render equals today's plus the two new jobs.
2. Rows for F1 and F2 (DG2): retired + `migrate-* --write` = no ref moved and the RETIRED line, dry-run unchanged, grid_sync on = today's behaviour; the F2 effect row above (a bare origin with a new refs/grid tip, the rendered mail_poll line run with grid_sync false, local refs/grid unchanged), plus the same with grid_sync true = today's (the grid is fetched).
3. The suite-lock deferral row (GV-4, SM 18:26Z): with `verification.suite_lock_holder(root)` returning a LIVE foreign pid, the REAL rendered `evidence_enforce` line (or its named wrapper) rewrites NO node file (an unbacked verdict fixture stays byte-identical), prints `evidence gate deferred: suite lock held by pid N`, and exits 0; with the lock free or held by a dead pid the same fixture IS demoted in place rc 0.
4. Negative: `git grep -n 'mirror_towns' -- .agi/nodes/.geometry/crons.md` shows 0 hits under grid_sync (the cell moved to town_mirror), and `git grep -n 'grid.py' -- <the two new jobs' cmd cells>` shows 0 hits.

## Out of scope
goal:g7.16.1.11.13 itself (E2b0 gate, census, writer list, the flip) · the flip commit (belam's `crons.py apply`) · E2d (does root push refs/grid at all) · changing what evidence_gate demotes. · cli.py:4241 (the branch-rename verb's `git fetch`, a W11 / F2 consumer): a manual verb, named OUT of the flip's scope with no row (GV-5, SM 18:56Z, DG1 ruling).

## Agent Notes
Assigned to **director-general-3 (builder: crons.md cells + crons.py render + KNOWN_JOBS; DG2 writes the falsifier rows first)**.
