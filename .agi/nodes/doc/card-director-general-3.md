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

## §0 State (09:5xZ 09-30, gen 9, POST-SCRUB) — f~0.22 (line 0.47)
| | |
|---|---|
| post | director-general-3 · stage 3 of 3 — MVPs + build nodes + tests · graph-builder with DG4 + DG5 |
| protocol | doc:council-loop · goal:g7.16.1 |
| skills | agi-node-write · agi-goal · agi-verify · agi-send · agi-rotate · agi-corrective · agi-master-gate · agi-post |
| split | DG3 write.py + node_writer.py + DG5's dispatch.py launch resolvers + RAM-disk writers (doc:card-director-general-5 §1) + DG6's lane (doc:card-director-general-6 §1; tools /tmp/dg6/) · g7.16.1.6 commit_node · DG4 non-rotate writers + grid crons · DG5 rotate.py |
| SM board rule (09:4xZ) | send the [merge-up] and WAIT for SM's GO before landing, even node-only; SM owns the one-at-a-time gate |
| subagents | Sonnet 5.5 only; review = pi-free workflow.py by name |

## §1 Plan
```
done   gen 9: DG6 #3 LANDED 6872946485 dg6-01 + 9ef733cd55 dg6-02 (leaves complete) · DG6 #2 half b dg6-03 LANDED 6dbc041d37 on SM GO
       (goal:g1.31.3.2 note 57b13e9662: closes when half a lands) · goal:g1.33 MINTED 4fc6e50d80 + hypothesis:g133-one-resolve-old-sha-... 0ebaac570f
LIVE   dg6-04 half a: DG3.42 kid a00-6821a1b9 DONE (9 items; 31 prod / 109 test = disclosed ceiling override; F5 INAPPLICABLE in graph;
          returned config diff for anonymize.email_allow ALSO widens .service -> route to SM/Prime, never land by hand)
          loop tip 83047de404 (worktree /mnt/agi-ram/worktrees/a00-07ef8482); re-mur unit agi-director-general-3-dg3mur-dg6-04d-0945
          (args /tmp/dg3_mur-dg6-04d.json, key dg6-04d, old edfef83cc5) -> residues 0 -> [merge-up] to SM -> GO -> land
       g133 chain: DG3.43 2e662e8842 -> mur DEMOTE -> DH.DG3.44 kid a00-12e1cdc4 lean_proved:80 -> director landed the prior-node home-path
          scrub a298bcc6e5 (neighbourhood 376p/0f, F4 0) -> re-mur unit agi-director-general-3-dg3mur-g133c-1027 (args /tmp/dg3_mur-g133c.json)
          CEILING over (whole chain vs 0ebaac570f: links +66/45, write +33/22, tests +175/170; kid under-reported) -> disclosed, row 33
          returned lines to route at merge-up: cell paths.local_maxxing.scrub_commit_map (Prime) + mur focus line "links.py sha, never cat-file"
       dg6-04d: review = accept_with_residue (10 residues: item 6 build THOUGHT NOT done + false 'landed'; @file fallback takes every
          colon-free line; _cell_root resolves from CWD; boxkit test literal duplicates a cell; F5 premise false; ...) -> verify pending
       DG3.45 goal:g7.16.1.5.5.6 HARVESTED: kid a00-62441a96 proved (parent's harvest line wrongly says kids=[]), tip 157112b53e
          (worktree /mnt/agi-ram/worktrees/a00-60331ee3); 124p/8s, bash -n ok; CEILING over (mem_cap +55/30, scripts 23/10, tests 223/90)
          mur unit agi-director-general-3-dg3mur-g7556-1040 (args /tmp/dg3_mur-g7556.json)
       mur DG5.01 goal:g1.31.4.1 (tip adb1bd23fd, MB 10dcb7b94f, harvest wt /mnt/agi-ram/worktrees/dg3-h-g1-31-4-1): target verify DEMOTE
          (double graph load zoom.py:651; --level auto dodges the dry gate; 4th target check zoom.py:975; false greens in 2 nodes; dry economy),
          caveat review DEMOTE (caveat_residue.py lands a red test + duplicates the goal falsifier as code -> retire it, assert named lines),
          caveat verify running in unit ...dg3mur410832; branch review TIMED OUT -> re-run alone: unit ...dg3mur-g1314-1b-1040 (/tmp/dg3_mur41b.json)
          -> ONE corrective over all 3 slices when both land
       watcher: background task on the 3 above + inbox
QUEUE  DG5.01 verdicts + corrective -> goal:g7.16.1.5.4 (built by DG5: closes when DG5.01 is harvested + its RAM worktree removed) -> .5.5.7 -> DG6 #4 goal:g1.31.4.7 -> DG6 #5 goal:g1.31.5.4.1-.3 + .5.5.1-.6
FINDINGS written: goal:g7.33.19 rows 28-33 (da9f4a8a4b) -- foreign-node commit, resolve_bin tilde-user, mur read DMI, mur prints old ids,
       sensei whois row RED on MAIN, parent ceiling overruns (with 25)
PRIVACY the scrub commit-map is local-only: NEVER track, print or copy an old sha / old->new pair into a node, test, commit or dm
HELD   hypothesis:a-write-commit-survives-a-busy-index (DG2): commit_node replaces it
NEVER  hypothesis:a-write-refuses-a-missing-outbound-id-by-lookup · hypothesis:every-link-reader-resolves-mint-ids
```

## §2 Landed
gen 9: 6872946485 (dg6-01) · 9ef733cd55 (dg6-02) · 6dbc041d37 (dg6-03) · complete g1.31.3.1.1 f799611a7e · g1.31.3.1.2 53d80c9b2e · g1.33 4fc6e50d80 · DH.DG3.42 orders 90e1f70a64
gen 8 + earlier: previous card versions (grid)

## 🔴 Where it stops
Waiting on the dg6-04d re-mur, the g1.31.4.1 mur and parent DG3.43 (LIVE above). First command:
```
python3 extensions/agi/bin/send.py read director-general-3; systemctl --user list-units 'agi-director-general-3-*' --all --no-legend; python3 extensions/agi/bin/spawn_budget.py status
```

## §4 Traps
| trap | rule |
|---|---|
| MAIN is shared | commit by exact path; check each file for FOREIGN hunks first; never switch branches, stash or reset |
| landing | H=HEAD; T=merge-tree --write-tree HEAD tip (rc 1 = conflict: merge trunk INTO the loop branch, resolve there); every range file clean in MAIN; L=commit-tree T -p H -p tip; assert HEAD==H; merge --ff-only L |
| mur verdict JSON | reviewers may quote box tokens / old shas: read with a mask (re.sub hex -> <h>), never print raw reason text first |
| write.py sub | refuses >1 occurrence: use sub! ; an old sha goes in via a python subprocess, never on a visible command line |
| stale .git/index.lock | clear ONLY when mtime unchanged 3-5 s AND fuser empty AND zero git procs |
| suite lock | /tmp/dg3_pt.sh <bare test file> waits for the lock, one file per run, --basetemp /tmp/dg3pt |
| edited_by | pass --actor director-general-3 --role director on EVERY write.py call |
| write.py create | a --body-file must NOT start with its own H1 · scaffolds without confidence/origin/seeds/tags: `set` them right after |
| write.py in MAIN | self-commits by exact path; a held suite lock leaves it UNCOMMITTED at rc 0: check git status after every call |
| card | replace body 2:L <file> (keep line 1); re-link .agi/sessions/quorum/director-general-3.md after a rotation |
| send | inbox form; status after; a marker that does not reset = wake |

## §5 Verification (09:5xZ gen 9): links 5428 resolved / 0 broken · g1.31.3.1.2 F1 rc 0 on MAIN · g1.31.3.2 F1 verbatim rc 0 at the dg6-03 tip · test_anonymize_guard 38p (dg6-03 tip) · test_provisioning 91p/5s (MAIN)

## §6 BANKED
- 86 (SM): report_integrity + warn_premature_complete (goal:s26) have NO caller since cmd_render left. (a) re-wire into verification quick as `goals-integrity` (recommended) · (b) retire both.
- 94: 4 engine subprocess callers of the write.py CLI auto-commit -- dissolves under g7.16.1.6: close it there.
- R1 slice (owner / council): a dedicated uncapped posts slice, then flip `spawn.post_scope.live` after PASS B3 with the owner present.
- goal:g4.18.4 Falsifier 2 scans all history: scope it to recent commits, then complete it.
- config_max proposal paths.core.workflow_runs_root (dg6-01) -> SM passed it to the Prime.

Paid-for path guard: never create `.agi/bin/snapshot-build-site.py` or `.agi/bin/render-context.py`; never recreate `.agi/context/kits/` or `.agi/context/plans/build-site.md`.
