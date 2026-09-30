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

## §0 State (08:5xZ 09-30, POST-SCRUB: every sha rewritten 07:xZ; old -> new = grep ^<old> /data/scrub/union.git/filter-repo/commit-map) — gen 8, seat agi-34 [e82e60]; f~0.34 (line 0.47)
| | |
|---|---|
| post | director-general-3 · stage 3 of 3 — MVPs + build nodes + tests · graph-builder with DG4 + DG5 |
| protocol | doc:council-loop · goal:g7.16.1 |
| skills | agi-node-write · agi-goal · agi-verify · agi-send · agi-rotate · agi-post |
| sessions (06:0xZ) | SM agi-5c · DG2 agi-e3 [78fffb] · DG4 agi-c8 [6d9f0c] · Prime agi-23 · names shift on every rotation: the seat's latest rotation record (rotate.py status --post <p> --record latest: session_name + window) + ListAgents' tmux window pick the ref |
| split | DG3 write.py + node_writer.py (CLAIMED) + (owner via SM 06:3xZ: DG5/DG6 stood down) dispatch.py launch resolvers + the RAM-disk writers -- handover = doc:card-director-general-5 §1 · + DG6's lane (owner: DG6 stood down; SM board 08:3xZ, handover doc:card-director-general-6 §1, tools /tmp/dg6/{harvest.py,land.sh,murwait.sh}) · bundle-4 W2c rest · g7.16.1.6 MACHINERY commit_node · DG4 non-rotate writers + grid crons · DG5 rotate.py WHOLLY |
| subagents | Sonnet 5.5 only (owner 04:4xZ): Agent tool model sonnet, isolation worktree; they die with this session, commits survive on their branches |

## §1 Plan
```
done   gen 8 (NEW shas): W2c C ff549a1757 + 9bd36310a4 (SM + DG2 w2cD PROVED) · g1.31.4.3 9bd4c4a89f + 91be4d21dc, complete 6a20d689a5
       census e85d367ca4 + 404f1b6980, complete 3d52008060 · g4.18.1.6 R1-R4 91be4d21dc · F 04d765c817 (g7.33.20 + R1b + g1.31.5.2)
       leaves g7.33.20 c287fee398 · .20.2 887bcc716b · .20.3 3858116557
       SM on 04d765c817: C (g1.31.5.2) ACCEPTED; B = REGRESSION (own-id refusal hits 126 alias exp:/hyp: nodes by long form); R1c open
LIVE   J Sonnet: goal:g7.33.20.2 (VERIFY G's surviving 95c436aff3, merged from worktree-agent-aee4a573c1ee7cd85) +
          goal:g7.33.20.3 (config create gate D1-D3) + B3 (rule 3 same-type only, no tree-wide fallback; /tmp/sm9/cc_b2.json)
       mur pi-free RUNNING (3 units, `systemctl --user list-units 'agi-director-general-3-*'`), verdicts in
          .agi/sessions/workflows/runs/mur-season2-loops-<branch with / -> ->/{review,verify}_<key>.json:
          DG5.01 goal:g1.31.4.1 unit ...dg3mur410832 (args /tmp/dg3_mur41.json; harvest worktree /mnt/agi-ram/worktrees/dg3-h-g1-31-4-1,
             tip adb1bd23fd, MB 10dcb7b94f; my read: caveat_residue.py = residue; remove the worktree after landing)
          DG6 dg6-03 hw-name-scrubbed a00-dbbb2896 + dg6-04 anonymize-refuses a00-fb71a5f6 (units ...dg3mur-dg6-0{3,4}-0833,
             args /tmp/dg3_mur-dg6-0{3,4}.json) -> merge the clean ones (DG6 rule: --no-ff, one at a time, merge-tree vs trunk first)
          dg6-01 / dg6-02: review done pre-freeze, verify stage missing -> re-run like 03/04 (remap tips: current merge-base)
HARVEST MAIN files == kid base blobs -> `git diff <base> <tip> | git apply` (cherry-pick refuses: foreign staged files) -> files
       WHOLE via /tmp/dg3_pt.sh ONE at a time -> re-verify blobs -> commit by exact path (a pre-commit hook refuses privacy tokens:
       redact, never --no-verify) -> [landed] to SM agi-5c
QUEUE  (SM order 08:3xZ) J harvest -> DG6 #2 goal:g1.31.3.2 (hw-model
       fragment + hw-name scrub: murs dg6-04 / dg6-03 -> /tmp/dg6/murwait.sh, merge clean ones; (a) decide by the SHIM rule) ->
       DG6 #3 goal:g1.31.3.1.1 + .1.2 (murs dg6-01 / dg6-02; a00-6b761b8c edited by dg6-01 AND dg6-03: merge-tree first) ->
       DG5 rows: DG5.01 mur verdicts + corrective -> goal:g7.16.1.5.4 (by ITS falsifiers; F2 broken literally by de-h-dg5-421) ->
       goal:g7.16.1.5.5.6 (dispatch a PARENT) -> .5.5.7 -> DG6 #4 goal:g1.31.4.7 (free-lane red; suspect links.frontmatter_rows
       bytes grep vs a str fake) -> DG6 #5 goal:g1.31.5.4.1-.3 + .5.5.1-.6 (46 rows, leaves minted, NO briefs: brief per [hypothesis])
       merge rule (DG6's): only a mur-clean round merges, --no-ff, one at a time, merge-tree vs trunk first; ONE [merge-up] per batch
HELD   hypothesis:a-write-commit-survives-a-busy-index (DG2): commit_node replaces it
NEVER  hypothesis:a-write-refuses-a-missing-outbound-id-by-lookup · hypothesis:every-link-reader-resolves-mint-ids
```

## §2 Landed
gen 8 (NEW shas): ff549a1757 · 9bd4c4a89f · 9bd36310a4 · 91be4d21dc · e85d367ca4 · 404f1b6980 · 04d765c817 · 30175ea7e9 (privacy #1 email class) · 6894c783f3 (B regression fix + R1c)
       complete: g7.16.1.1.6.1 3d52008060 · g1.31.4.3 6a20d689a5 · g1.31.5.1.2 5ec3265589 · g4.18.1.6 fb54ed0f23 · g7.33.20 f86698bd49 · g1.31.5.2 a350c2318d
gen 7 + 6: pre-scrub card versions (grid)

## 🔴 Where it stops
Waiting on Sonnet round J and 3 murs (LIVE above). If this session is gone, F's commits survive on its
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
