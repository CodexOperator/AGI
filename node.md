---
id: doc:card-director-general-3
mint_id: 960e181d30924fb3ba1a63ca4a6698f4
type: doc
parents:
  - goal:g7.16.1
next_edges: []
edited_by: director-general-3
scaffold_hash: 67b067422d7509fe
season: 2
title: Card director general 3
town: core
---
# doc:card-director-general-3

# doc:card-director-general-3 — director-general-3's card (council loop, goal:g7.16.1): the ONE scratch

Role: doc:unified-director-brief (the director TEMPLATE) + this card. Post director-general-3 · master: the council (SM = coordinator) · MAIN /data/work/agi on local-maxxing/season2/main.

## §0 State (06:4xZ 09-30) — gen 8, seat agi-34 [e82e60]; f~0.29 (line 0.47)
| | |
|---|---|
| post | director-general-3 · stage 3 of 3 — MVPs + build nodes + tests · graph-builder with DG4 + DG5 |
| protocol | doc:council-loop · goal:g7.16.1 |
| skills | agi-node-write · agi-goal · agi-verify · agi-send · agi-rotate · agi-post |
| sessions (06:0xZ) | SM agi-5c · DG2 agi-e3 [78fffb] · DG4 agi-c8 [6d9f0c] · Prime agi-23 · names shift on every rotation: the seat's latest rotation record (rotate.py status --post <p> --record latest: session_name + window) + ListAgents' tmux window pick the ref |
| split | DG3 write.py + node_writer.py (CLAIMED) + (owner via SM 06:3xZ: DG5/DG6 stood down) dispatch.py launch resolvers + the RAM-disk writers -- handover table = doc:card-director-general-5 e4f52f044 · bundle-4 W2c rest · g7.16.1.6 MACHINERY commit_node · DG4 non-rotate writers + grid crons · DG5 rotate.py WHOLLY |
| subagents | Sonnet 5.5 only (owner 04:4xZ): Agent tool model sonnet, isolation worktree; they die with this session, commits survive on their branches |

## §1 Plan
```
done   gen 8: A 7d10fc7c7 + C bd15f4e6e (W2c C, SM ACCEPTED 0 residues: 0 of 5049 twins differ) · B 03acdf602 (g1.31.4.3 #37 #12)
       D 699dc47c6 (g4.18.1.6 R1-R4 + _commit_message guard + g1.31.4.3 rows placed; SM Sonnet review RUNNING)
       E 7d4ff6a84 census code (check_census; the Prime mints config:census from f2d6ad468's bytes now that it is on HEAD)
       leaf goal:g7.33.20 minted (1bbe89ee2 0de3a32a0)
LIVE   G Sonnet: goal:g7.33.20.2 (_default_actor -> resolved seat) + goal:g7.33.20.3 (config create gate D1-D3), 2 commits,
          based on F (dd4372795) -> harvest: MAIN files == G's base blobs, `git diff <G base> <G tip> | git apply`
       DG5.01 (goal:g1.31.4.1) HARVESTED IN PLACE: parent ended ~06:2xZ, its RAM worktree was gone -> detached harvest worktree
          /mnt/agi-ram/worktrees/dg3-h-g1-31-4-1 at ddb71cb15 (remove it after landing: git worktree remove); MB d48156e2f
          tests there: dispatch_dry_run 31p · dispatch 139p · cli 75p · heal_watch 88p · zoom 41p · 5 fixture files green ·
          test_caveat_residue 1 FAIL (its live-graph row: the round's own nodes quote the phrase)
          mur pi-free RUNNING: unit agi-director-general-3-dg3mur410624, args /tmp/dg3_mur41.json, slices g1-31-4-1-{branch,target,caveat}
          my read: caveat_residue.py = residue (falsifier-2 scope belongs in the goal's text); _compose_small loads the graph twice (perf?)
          -> verdicts from .agi/sessions/workflows/runs/<key>/{review,verify}_g1-31-4-1-*.json; residues -> skill agi-corrective
QUEUE  (SM order) DG5.01 mur + corrective -> goal:g7.16.1.5.4: judge by ITS falsifiers (F1 every LIVE round worktree under the RAM
       path: true 06:2xZ; F2 zero worktrees created under .agi/worktrees after the change: DG5's harvest worktree de-h-dg5-421
       06:10 breaks it literally) -- NOT the handover's `agi-ram == 0` -> goal:g7.16.1.5.5.6 (ram-main.sh + session-sweep.sh via locations.ram_write_argv
       + one-shot recharge: dispatch a PARENT, spawn_budget.py status first) -> goal:g7.16.1.5.5.7 (horizon, per-post MemoryHigh)
HARVEST MAIN files == the kid's base blob (git hash-object vs git rev-parse <base>:<f>) -> `git diff <base> <sha> | git apply`
       (cherry-pick REFUSES: foreign staged rotation JSONs) -> touched files WHOLE via /tmp/dg3_pt.sh (ONE run at a time:
       two share /tmp/dg3pt and collide) -> re-verify blobs + commit by exact path -> SHAs to SM agi-5c
THEN   goal:g4.18.1.6 complete once SM accepts eff6255e3's R1b (everything else closed on 699dc47c6) · g7.33.20 + g1.31.5.2 complete on SM accept
       then census .6.2 (the home-path row) · DG1's goal:g6.41.1.1 (hypothesis:a-session-resumed-outside-heal-gets-one-after-join-wake)
       PASS B3 rows beyond n60/n84: SM relays as DG6 mints them
HELD   hypothesis:a-write-commit-survives-a-busy-index (DG2): commit_node replaces it
NEVER  hypothesis:a-write-refuses-a-missing-outbound-id-by-lookup · hypothesis:every-link-reader-resolves-mint-ids
```

## §2 Landed
gen 8: 7d10fc7c7 · 03acdf602 · bd15f4e6e · 699dc47c6 · 7d4ff6a84 · 123e892a3 (census xfail lift) · eff6255e3 (g7.33.20 + R1b + g1.31.5.2) · complete: g7.16.1.1.6.1 f506b75a7 · g1.31.4.3 b8ef5ac14 · leaves g7.33.20 1bbe89ee2 · .20.2 f63f501bf · .20.3 c72532c29 · card relink efb0a8f06
gen 7 + 6: see the grid version of this card at 95e3c8002

## 🔴 Where it stops
Waiting on Sonnet round G and the DG5.01 mur (LIVE above). If this session is gone, F's commits survive on its
worktree branch: harvest as in HARVEST. First command:
```
git -C /data/work/agi worktree list | grep agent- | tail -1
```

## §4 Traps
| trap | rule |
|---|---|
| MAIN is shared | commit by exact path; check each file for FOREIGN hunks first (guard-init.sh is another post's WIP); never switch branches, stash or reset |
| an agent may write MAIN too | gen-7 agent A left its hunks uncommitted in MAIN as well: compare MAIN bytes to the commit's blobs before applying |
| staged foreign index | cherry-pick refuses while other posts' rotation JSONs are staged: git apply (--3way) the commit's patch instead |
| stale .git/index.lock | clear ONLY when mtime unchanged 3-5 s AND fuser empty AND zero git procs |
| SHA reporting | read it off `git commit`'s own output line |
| suite lock | /tmp/dg3_pt.sh <bare test file> [-k ..] waits for the lock, one file per run, --basetemp /tmp/dg3pt; recreate after a reboot |
| red-on-HEAD proof | copy the file to /tmp, `git show HEAD:<f> > <f>`, run, copy back, `cmp` -- never stash |
| edited_by | AGI_ACTOR is unset in this session: pass --actor director-general-3 on EVERY write.py call (else it stamps belam; goal:g7.33.20.2) |
| write.py create | adds `# <id>` itself: a --body-file must NOT start with its own H1 (fix: `replace body 1:3 --force <file>` -- --force is a PREFIX of the source arg) · it scaffolds without confidence/origin/seeds/tags: `set` them right after |
| write.py in MAIN | self-commits by exact path; a held suite lock leaves it UNCOMMITTED at rc 0: check git status after every call |
| card | replace body 1:L <file> (L = current body length); then re-link .agi/sessions/quorum/director-general-3.md -> ../../nodes/doc/card-director-general-3.md |
| messaging | SendMessage to a session name ONLY; context in goal nodes |
| a new link reader | `r = links.address_resolver(root); r(x) or x`; a gate uses links.gate_resolver(nodes_dir) (never raises) |

## §5 Verification (06:1xZ gen 8, MAIN): census 13p/1x · verification 71p/2x · verification_kept_merge 19p · _manifest 11p · _seat_model 8p · _window 9p · help smoke 70p/8s · write 187p/1x · node_writer 130p/3x (live tree green after DG4's repair) · write_guard 32p · write_ring_cli 21p · thought_hygiene 17p · answers_file 42p · write_sub 17p · rings 51p · body_patch 6p · frontmatter 11p · evidence_gate 140p · level3 60p/1x · links 48p/1x · cli 76p · spawn_gate 83p · viewport 58p/7x

## §6 BANKED
- 86 (SM wf_8ce06028-a81): report_integrity + warn_premature_complete (goal:s26) have NO caller since cmd_render left.
  Options: (a) re-wire both into verification level quick as a `goals-integrity` command (recommended) · (b) retire both and re-point the W2c-B xfail row.
- 94: 4 engine subprocess callers of the write.py CLI auto-commit (rotate.py closeout · season.py:274 · sensei.py:2465 · failures.py:361) -- dissolves under g7.16.1.6: recommend closing it there.
- R1 slice (owner / council): a dedicated uncapped posts slice, then flip `spawn.post_scope.live` after PASS B3 with the owner present.
- goal:g4.18.4 Falsifier 2 scans all history: scope it to commits after 2c412e5bb, then complete it.

## Findings for the next bundle
- test_rings::test_suite_grant_nonreplay flaky (1 fail alice=FORGED, then 6/6 green) -- a findings row on goal:g7.33 when the lane allows
- config:* nodes: write.py create refuses a director (goal:g12, admitted owner + prime_director) -> a kid needing a cell: route via SM to the Prime; never land a hand-written cell
- rest: see the grid version of this card at 95e3c8002

Paid-for path guard: never create `.agi/bin/snapshot-build-site.py` or `.agi/bin/render-context.py`; never recreate `.agi/context/kits/` or `.agi/context/plans/build-site.md`.
