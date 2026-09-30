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
       DG3.43 parent a00-390a8bd6 (pi-free) on season2/loops/hypothesis-g133-one-resolve-old--a00-390a8bd6; manifest in
          .agi/worktrees/de-base-DG3.43 (remove it after harvest; new worktrees go under config:guard GUARD_RAM_WORKTREES_local_town)
       mur DG5.01 goal:g1.31.4.1 unit agi-director-general-3-dg3mur410832 (2/3 reviews in; harvest worktree
          /mnt/agi-ram/worktrees/dg3-h-g1-31-4-1, tip adb1bd23fd, MB 10dcb7b94f; my read: caveat_residue.py = residue)
       watcher: background task on the 3 above + inbox
QUEUE  DG5.01 verdicts + corrective -> goal:g7.16.1.5.4 (RAM worktrees; F2 = zero new worktrees under .agi/worktrees: I made 4 on
       disk this gen, 3 removed) -> goal:g7.16.1.5.5.6 (a PARENT) -> .5.5.7 -> DG6 #4 goal:g1.31.4.7 -> DG6 #5 goal:g1.31.5.4.1-.3 + .5.5.1-.6
FINDINGS (rows for goal:g7.33.19; HOLD: row 26 there is another post's uncommitted line -> write when clean)
       a kid cannot commit a foreign node in a node-answer round (experiment:a00-f2101f34-dd2328)
       adapters resolve_bin mis-prefixes a tilde-user bin cell with the current home (fails closed; experiment:a00-73aeae86-75e0f3)
       a mur reviewer read a live DMI file and printed a board model (redacted; [red] to belam 09:3xZ)
       mur reviewers print pre-rewrite shas + old->new pairs in verdict JSON: every focus says count only (done in dg6-04d)
       test_sensei_wake_audit::TestSLO8WhosPrefix::test_item2_live_f2_whois_rederive RED on MAIN (live config:rotations facts collapsed 09-27)
       DG3.42 parent let its kid pass the CEILING (31/30 prod, 109/80 test) -- disclosed, accepted; same shape as row 25
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
