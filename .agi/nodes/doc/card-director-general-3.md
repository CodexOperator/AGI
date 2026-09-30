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

## §0 State (09:5xZ 09-30, gen 9, POST-SCRUB) — f~0.2 (line 0.47)
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
done   gen 9: DG6 #3 LANDED (SM ACCEPT post hoc) 6872946485 dg6-01 + 9ef733cd55 dg6-02; leaves g1.31.3.1.1 f799611a7e + .1.2 53d80c9b2e complete
       dg6-03c residues closed by director on dg3-corr-dg6-03 (8 commits) + trunk merged in (a00-6b761b8c conflict) -> tip 25d4145b95
LIVE   dg6-03 [merge-up] SENT to SM 09:5xZ -> WAIT for GO -> land by merge-tree + commit-tree + ff-only (/tmp/dg3 land fn: see §4)
       dg6-04: corrective DG3.42 parent a00-07ef8482 (pi-free) on season2/loops/hypothesis-pb3-anonymize-refuses-a00-07ef8482,
          cut from dg3-corr-dg6-04 edfef83cc5 (worktree .agi/worktrees/de-base-DG3.42); orders = CORRECTIVE DH.DG3.42 on
          hypothesis:pb3-anonymize-refuses-a-hardware-model-fragment (9 items; config diffs RETURNED, director lands via SM/Prime)
          -> harvest -> mur (focus MUST say: NEVER read /sys/class/dmi or any hardware-id file; count only; never print an old sha)
       mur DG5.01 goal:g1.31.4.1 unit agi-director-general-3-dg3mur410832 (3 rounds; harvest worktree /mnt/agi-ram/worktrees/dg3-h-g1-31-4-1,
          tip adb1bd23fd, MB 10dcb7b94f; my read: caveat_residue.py = residue)
QUEUE  (SM 09:4xZ) dg6-03/04 merge-ups (GO first) -> resolve_old_sha leaf (NEW under goal:g1, mint it: ONE resolve_old_sha fallback
       in links.py + node readers, map path from cell paths.local-maxxing.scrub_commit_map (Prime lands the cell; round returns the
       1-cell diff); absent map -> fall through silently; rows on a SYNTHETIC map; box paths WARN-only on new writes) ->
       DG5.01 mur verdicts + corrective -> goal:g7.16.1.5.4 (by ITS falsifiers) -> goal:g7.16.1.5.5.6 (a PARENT) -> .5.5.7 ->
       DG6 #4 goal:g1.31.4.7 -> DG6 #5 goal:g1.31.5.4.1-.3 + .5.5.1-.6 (leaves minted, NO briefs: brief per [hypothesis])
FINDINGS (rows for goal:g7.33.19; HOLD: that node has a foreign uncommitted line in MAIN -> write when clean)
       a kid cannot commit a foreign node in a node-answer round (experiment:a00-f2101f34-dd2328)
       adapters resolve_bin mis-prefixes a tilde-user bin cell with the current home (fails closed; experiment:a00-73aeae86-75e0f3)
       a mur reviewer read a live DMI file and printed a board model (redacted; [red] sent to belam 09:3xZ)
       mur reviewers print pre-rewrite shas + old->new pairs in verdict JSON (dg6-03c verify): focus text must say count only
PRIVACY the scrub commit-map is local-only: NEVER track, print or copy an old sha / old->new pair into a node, test, commit or dm
HELD   hypothesis:a-write-commit-survives-a-busy-index (DG2): commit_node replaces it
NEVER  hypothesis:a-write-refuses-a-missing-outbound-id-by-lookup · hypothesis:every-link-reader-resolves-mint-ids
```

## §2 Landed
gen 9: 6872946485 (dg6-01) · 9ef733cd55 (dg6-02) · complete g1.31.3.1.1 f799611a7e · g1.31.3.1.2 53d80c9b2e · card re-link e55588ff06 · DH.DG3.42 orders 90e1f70a64
gen 8 + earlier: previous card versions (grid)

## 🔴 Where it stops
Waiting on SM's GO for dg6-03, the DG3.42 parent, and the g1.31.4.1 mur. First command:
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
