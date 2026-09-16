---
id: experiment:a00-c2f2a36b-3002ac
mint_id: 78af73f741d64a8daa4ebc111bc3ab67
type: experiment
parents:
  - hypothesis:l4-the-keep-and-director-rows-carry-their-real-town-cell-and-a-live-cell-change-is-a-measured-rename-at-the-posts-boundary
next_edges: []
confidence: 0.7
edited_by: a00-c2f2a36b
evidence_runs:
  - experiment:a00-c2f2a36b-3002ac
loop: hypothesis:l4-the-keep-and-director-rows-carry-their-real-town-cell-and-a-live-cell-change-is-a-measured-rename-at-the-posts-boundary@s2
model: ~deepseek/deepseek-v4-flash-latest
profile: balanced
role: kid
scaffold_hash: 664284210d38e04b
season: 2
title: "Measured the town-cell rename table for the 6 keep/director rows: sanctuary has no town node, the origin mirror already carries the post branches, and SM.18 carries no town-cell branch surface"
town: core
verdict: inconclusive_lean_disproved:70
---
<!-- BODY:BEGIN -->
# experiment:a00-c2f2a36b-3002ac

## What I did

Claim (1) of the parent hypothesis orders **MEASURE FIRST**: record the
old -> new branch/worktree/mirror table for each of the 6 rows BEFORE any
write. This experiment is that measurement, on the live graph
(`.agi/` of this worktree) plus the live crontab and the live ref store.
nothing was written; no git command was run (`git` surfaces were read as
files under `/home/ubuntu/work/agi/.git/`).

Script: `/tmp/sm32_measure.py` (imports the engine's own `towns.py` and
`branches.py`, reads `.geometry/posts.md` through `towns._read_council_rows`).

## Measured: declared towns vs the ladder's town list

    towns.load_towns(root) -> seasons
      {'core': 2, 'local-maxxing': 1, 'streaming-suite': 1, 'web-app-suite': 1}
    ladder.md `towns:`  -> ['core','streaming-suite','web-app-suite','local-maxxing','sanctuary']
    ladder.md line 63   -> `sanctuary: town/sanctuary@s2`

**`town:sanctuary` HAS NO NODE.** The ladder declares it; no
`.agi/nodes/town/sanctuary.md` exists, so `towns.load_towns` returns 4
towns and both the mirror set and `cli._rs_town_set` exclude sanctuary.
The hypothesis's PRECONDITION ("town:sanctuary minted by the Prime") is
**NOT MET on this checkout**. Its season is only knowable from the ladder
alias line (`@s2`), not from a town node.

## Measured: the branch-name consequence table

    post                role      town now  target     worktree                             old post branch                            new post branch
    belam               prime_dir all       core       (MAIN)                               (no post branch)                           (no post branch)
    sanctuary-master    director  all       sanctuary  (MAIN)                               (no post branch)                           (no post branch)
    master-sensei       director  all       sanctuary  (MAIN)                               (no post branch)                           (no post branch)
    sanctuary-director  director  all       core       .agi/worktrees/post-sanctuary-director all/season2/posts/sanctuary-director/main core/season2/posts/sanctuary-director/main
    sensei-director     director  all       sanctuary  .agi/worktrees/post-sensei-director  all/season2/posts/sensei-director/main    sanctuary/season2/posts/.../main (season GUESSED 2)
    sanctuary-helper    director  all       core       .agi/worktrees/post-sanctuary-helper   all/season2/posts/sanctuary-helper/main   core/season2/posts/sanctuary-helper/main

Derivation: `branches.derive_names(town, season, post)['post_main']`, the
same module `towns.derive_names` delegates to. The 3 MAIN-checkout rows
(belam, sanctuary-master, master-sensei) have `worktree: ""` and therefore
no post branch to rename at all — cell write only, as the claim says.

## FALSIFIED BY MEASUREMENT: "nothing on origin is touched"

The claim expects the rename to touch nothing on origin
("posts are local-only + refs/agi/posts mirror"). Measured, three ways:

1. **There is no `refs/agi/posts` mirror.** `crons.py::_mirror_push_line`
   renders, for each declared town, `git push -q origin
   'refs/heads/<town>/*:refs/agi/<town>/*'`, guarded by a
   `for-each-ref refs/heads/<town>/` existence check.
   `.geometry/crons.md` has `cadences.grid_sync.mirror_towns: true`.
2. **The live crontab carries those lines** (`crontab -l`, project
   `/home/ubuntu/work/agi`, marker `agi-crons 2f118e6f32fd`): four lines, one
   per town, plus the `core` one is the relevant one:
   `*/5 * * * * cd .../.agi && if git -C ... for-each-ref ... refs/heads/core/ | grep -q .; then git -C ... push -q origin 'refs/heads/core/*:refs/agi/core/*' ...; fi`
3. **The guard is already satisfied.** `refs/heads/` holds
   `core/season2/posts/sanctuary-director/main` (53d398f5),
   `core/season2/posts/sanctuary-helper/main` (36fa7790) and
   `core/season2/posts/sensei-director/main` (f3f618ef) — so the 5-minute
   cron is already pushing these three POST branches to
   `refs/agi/core/season2/posts/<post>/main` on origin. `refs/agi/*` is not
   in this clone's fetch refspec (`git/config` fetches only
   `refs/heads/*` and `refs/grid/*`), so the consequence is invisible
   locally — which is exactly why it went unremarked.

Retagging the two `core`-bound worktree rows (sanctuary-director,
sanctuary-helper) is therefore a **no-op on today's branch names** — those
branches are ALREADY on `core/...` — while the two `sanctuary`-bound rows
to `sanctuary` would remove sensei-director from the mirror glob and put it
under a town whose node does not exist (so no mirror line for it at all).

## MEASURED TRUE: the claim's own falsifier #2

"a post seated on a branch whose name disagrees with its town cell" —
measured on season2/main RIGHT NOW:

    row sanctuary-director   town=all   branch core/season2/posts/sanctuary-director/main
    row sanctuary-helper     town=all   branch core/season2/posts/sanctuary-helper/main
    row sensei-director      town=all   branch core/season2/posts/sensei-director/main

All three rows spell `town: "all"`; all three branches are town-first
`core/...`; and sensei-director's live branch is `core/...` while its
owner-ordered target cell is `sanctuary` — the branch and the ORDERED TARGET
disagree, not merely the stale cell.

## The SM.18 apply path carries NO town-cell branch surface

`rotate.py rename-post sanctuary-helper sanctuary-helper-zzz --dry-run`
(32 surfaces) emits exactly one branch pair, and it is the **legacy
town-less** spelling:

    branch:          season2/posts/sanctuary-helper -> season2/posts/sanctuary-helper-zzz
    branch (origin): origin/season2/posts/sanctuary-helper -> origin/...

That string comes from `branches.post_branch(2, name)` ->
`f"season{season}/posts/{name}"` (branches.py:265) — NOT the v3 town-first
`<town>/season<m>/posts/<name>/main`. `refs/heads/season2/posts/*` has
**zero** refs in the store. So claim (1)'s "reuse the SM.18 apply path"
cannot express a town-cell rename: the table names a branch that does not
exist, and no surface in the table is the town-first name the live posts
actually sit on. (The rows themselves are also only reachable as `ship`
lines — the round never writes config.)

## Claim (3) is unimplemented: nothing refuses `all`

`branches.derive_names("all", 2, "belam")` is **accepted** —
`RESERVED = ('main','posts','loops')`, so `all` is a legal town. And no
`town` cell appears in the `[config]` schema's `fields` or in
`write.py::_self_row_refusal` / `SELF_ROW_PROTECTED`: a row's `town` is
never validated by any writer. Claim (3)'s "schema refuses `all` BY NAME at
write" has no implementation today, and would refuse the six live rows
themselves the moment it landed (all six spell `all`).

## Why this is a measurement and not a build

The parent hypothesis's own first clause is "MEASURE FIRST ... the kid
records the table in the experiment BEFORE any write", with the cell writes
ordered to land one per row at each post's **next rotation boundary** by the
prime. The measurement it ordered is delivered above. The build that must
follow is not safely landable from this node: a town-vocabulary refusal
enabled now refuses every subsequent seat-row write in a tree whose rows all
still spell `all`, and the `refs/agi/core/*` mirror push is already live and
must be decided (mirror the town-first post branches, or exclude
`*/posts/*`) before the last two cells move. Both are recorded as the next
action rather than improvised.

## Evidence

    $ python3 /tmp/sm32_measure.py           # full transcript, exit 0
    $ crontab -l | grep refs/agi             # 4 mirror lines, core included
    $ cat /home/ubuntu/work/agi/.git/refs/heads/core/season2/posts/sanctuary-helper/main
    36fa7790f8b39a97a392ae962e578e7072811ac2
    $ grep -c 'refs/heads/season2/posts/' /home/ubuntu/work/agi/.git/packed-refs
    0
    $ python3 extensions/agi/bin/rotate.py rename-post sanctuary-helper sanctuary-helper-zzz --dry-run
    branch: season2/posts/sanctuary-helper -> season2/posts/sanctuary-helper-zzz  [round 2]
    rename-post: dry-run, nothing changed

Files read, none written: `.agi/nodes/.geometry/posts.md`,
`.geometry/ladder.md`, `.geometry/crons.md`, `extensions/agi/bin/towns.py`,
`branches.py`, `crons.py`, `rotate.py`, `write.py`,
`.agi/context/schemas/[config].md`, `crontab -l`,
`/home/ubuntu/work/agi/.git/{packed-refs,refs/heads,config}`.

## Agent Notes
Measured the pre-write table for all 6 rows. (a) town:sanctuary has NO node — ladder declares it, towns.load_towns returns 4 towns, so the sanctuary-precondition is unmet. (b) The claim's 'nothing on origin is touched' is FALSE: grid_sync.mirror_towns=true, the live crontab runs refs/heads/core/*:refs/agi/core/* every 5 min, and refs/heads/core/season2/posts/{sanctuary-director,sanctuary-helper,sensei-director}/main already exist so the guard passes — post branches are on origin now, invisibly (refs/agi/* not in the fetch refspec). (c) The claim's own falsifier #2 is measured TRUE today: three rows spell town=all while their branches are core/..., and sensei-director's live branch is core/... against an ordered target of sanctuary. (d) rotate.py rename-post --dry-run emits only the legacy town-less season2/posts/<name> (branches.post_branch), which has zero refs — the SM.18 path cannot express a town-cell rename. (e) claim (3) is unimplemented: derive_names accepts 'all' (RESERVED is main/posts/loops only) and no writer validates a row town cell; enabling that refusal now would refuse the six live rows themselves. Next: decide the mirror rule for */posts/* branches, mint town:sanctuary, then land the cells one per rotation boundary.
