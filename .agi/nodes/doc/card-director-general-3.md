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

## §0 State (14:1xZ 09-30, gen 9) — f~0.40 (captive capture fired at 0.40) (line 0.47) — RESUMED on belam's [rule] until 18:00Z (a STOP comes then)
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
LIVE   (parents exit WITHOUT merging their kid: harvest from the KID branch; engine row on goal:g7.33.19)
       g133 chain: LANDED 5f1e8092f2 by SM 15:23Z (tip 1d8fd19b90); goal:g1.33 COMPLETE f701f063bc; RAM tree removed
       dg6-04 chain: re-mur dg6-04e FAILED (verify timed out 3600 s at 14:52Z); review accept_with_residue triaged -> CORRECTIVE DH.DG3.52 on the
          loop tip a7ab2dba47 (3 test residues: no-CWD order, project-less row, email skip loop; +77/60 test cap ACCEPTED; 4 notes demoted)
          -> DG3.52 HARVESTED 15:10Z tip 3ea1e5543e -> mur dg6-04f DONE 15:31Z accept_with_residue (verify upheld 5 + 2 missed) -> director scrub of
          DH.DG3.55 tip 21a1caf3b1 -> mur dg6-04g (verify timed out; review accept_with_residue: order-dependent row + node verdict) -> DIRECT fixes (owner
          16:4xZ rule) 86d7f40b63 + 1aa701b525 -> Sonnet review ACCEPT (cosmetic line closed 7d2680889e) -> trunk merged INTO the loop branch
          e81201ebf2 (test_boxkit_templates conflict: trunk-derived fake + word-shaped hardware fake; 280p/1s/1x) -> Sonnet review of the
          resolution ACCEPT (docstrings closed 4dd121c405) -> gate vs fd87ce0466 rc 0, 16 files, 0 D -> [merge-up] half a SENT to SM 17:0xZ, WAIT for GO (tip 4dd121c405)
          -> GO -> land -> goal:g1.31.3.2 complete; email_allow cell (systemd-unit address shape) owed by the Prime -> SM/Prime with the merge-up
              g7556: DG3.50 tip 574a307b1c -> mur g7556d FAILED 15:51Z (memcap verify timed out; review + shell verify accept_with_residue) ->
          director moved the ram-recharge conjunct out of the hypothesis (-> goal:g7.16.1.5.5.6.1) -> CORRECTIVE DH.DG3.57 on loop tip 2d76bf17b4
          (liveness not presence, fail-open fstype_at/execvp, mount escapes, one ramw file, node verdicts) -> HARVESTED 16:07Z tip 2f46e5f159
          (131p/8s, caps met, item-5 nodes landed by director) -> mur g7556e FAILED 17:23Z (memcap verify timed out; accept_with_residue) -> Sonnet
          fix 7bd9e89964 + nodes + build node 99778019c2 (132p/8s, mem_cap +2, tests +1) -> director title/claim 8534ab1b8f -> trunk merged in
          6b444e66f1 (hypothesis keeps DH.DG3.48/.50/.57) -> gate vs 08b1ca1c94 rc 0, 11 files, 0 D -> Sonnet review of 2f46e5f159..8534ab1b8f RUNNING -> [merge-up]
       g7.16.1.10.3 (queue 1, CLAIMED active 9a8b4559cc): hypothesis:g716103-reds-py-checks-a-range-mechanically-before-any-model 5a6fecd879 ->
          DG3.51 HARVESTED 14:59Z tip 2f375f5154 -> mur h10103 DONE 15:29Z: both slices accept_with_residue, verify upheld 12 items -> CORRECTIVE
          DH.DG3.54 on the loop tip 8725ffca96 (findings rows 39 + 40) -> parent a00-9ed505e4 from /mnt/agi-ram/worktrees/de-base-DG3.54
          -> harvest -> re-mur 8725ffca96..tip -> residues 0 -> [merge-up] -> GO -> land -> g7.16.1.10.3 complete; cell merge_gate.red_classes -> SM/Prime
       g1.31.4.1 (DG5.01): re-mur g1314c DONE 15:33Z: both slices DEMOTE (verify upheld: vacuous --branch dry check-root, chain prod +40 vs +10,
          node verdict vs parent demote, split cell x2, cites, source-string tests) -> CORRECTIVE DH.DG3.56 on loop tip 7e014c3646 -> parent
          a00-22bc89b4 -> HARVESTED (parent exited silently): dispatch.py NET -2, tests NET +41 (cap 20), 294p + 1 INHERITED red (test_pre_fix_reaper);
          unlogged node edit re-applied by director via write.py 5908d4f98e -> Sonnet review DEMOTE (vacuous worktree row, no live-path split row, swallowed ZoomUnavailable + no load count, tests +41/20) -> Sonnet fix c2143b2aef (tests +19/20, mutation red) -> trunk merged in e22a38df4c (156p) -> gate rc 0, 0 D -> [merge-up] SENT to SM 17:10Z, WAIT for GO
          -> residues 0 -> [merge-up] to SM -> GO -> land -> goal:g1.31.4.1 + g7.16.1.5.4 complete
LIVE   g7.16.1.10.5 (CLAIMED 66443d8fa8): hypothesis:g716105-council-report-py-writes-one-row-per-round-and-routes-residues 50603f2b1e ->
          DG3.53 HARVESTED 16:03Z tip 79500d258c: parent DEMOTED (residue rows keyed by round), council_report.py 218/120, 2 kids/1 (row 41);
          doc:council-report landed by director 1077e45cb1 (bytes == log) -> CORRECTIVE DH.DG3.58 HARVESTED 16:25Z: item 1 MET, size 177/150
          ACCEPTED (disclosed, THOUGHT 62de7b8491); kid merged by director 995302b2d6 (467p/8s/1x) -> chain mur unit
          agi-director-general-3-dg3mur-h10105-1628 (/tmp/dg3_mur-h10105.json, 66443d8fa8..62de7b8491) worktree /mnt/agi-ram/worktrees/a00-f43e8762
          -> residues 0 -> [merge-up] -> GO -> land -> g7.16.1.10.5 complete; cell council.residue_leaves -> SM/Prime
QUEUE  (council ruling 13:5xZ, agi-53) after the live chains: goal:g7.16.1.10.3 (mechanical REDs) -> .10.5 (ONE council report node)
       MOVED to DG2 by SM 16:5xZ (its leak hunt runs): hypothesis:g73320-write-rows-pass-in-the-full-suite-once-the-poisoning-leak-is-fixed -- do NOT start it
       -> .10.7 (THE MERGE GATE: refusal logic + retire skills/agi-merge-pass §2 steps 2-4 + 6 by name in the same commit; §2 step 5 stays
       the Prime's; negative tests: missing row, planted RED, unreviewed:budget rows without the Prime's word naming the count). All horizon:
       claim each (status active) only when its round starts.
       DG5.01 verdicts + corrective -> goal:g7.16.1.5.4 (built by DG5: closes when DG5.01 is harvested + its RAM worktree removed) -> .5.5.7 -> DG6 #4 goal:g1.31.4.7 -> DG6 #5 goal:g1.31.5.4.1-.3 + .5.5.1-.6
FINDINGS written: goal:g7.33.19 rows 28-33 (da9f4a8a4b) + 35-37 (ee133ab745: anonymize --root, diff-text email, parents never merge kids) -- foreign-node commit, resolve_bin tilde-user, mur read DMI, mur prints old ids,
       sensei whois row RED on MAIN, parent ceiling overruns (with 25)
PRIVACY the scrub commit-map is local-only: NEVER track, print or copy an old sha / old->new pair into a node, test, commit or dm
HELD   hypothesis:a-write-commit-survives-a-busy-index (DG2): commit_node replaces it
NEVER  hypothesis:a-write-refuses-a-missing-outbound-id-by-lookup · hypothesis:every-link-reader-resolves-mint-ids
```

## §2 Landed
gen 9: 6872946485 (dg6-01) · 9ef733cd55 (dg6-02) · 6dbc041d37 (dg6-03) · complete g1.31.3.1.1 f799611a7e · g1.31.3.1.2 53d80c9b2e · g1.33 4fc6e50d80 · DH.DG3.42 orders 90e1f70a64
gen 8 + earlier: previous card versions (grid)

## 🔴 Where it stops
g133 LANDED 15:23Z;LIVE: re-murs dg6-04g + g7556e + h10105, parents DG3.54 a00-9ed505e4 + DG3.56 a00-22bc89b4. First command on wake:
```
python3 extensions/agi/bin/send.py read director-general-3; python3 extensions/agi/bin/spawn_budget.py status; systemctl --user list-units 'agi-director-general-3-*' --all --no-legend; df --output=pcent /mnt/agi-ram
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
| RAM hold | dispatch holds a round when the RAM disk >= GUARD_RAM_WT_HOLD_PCT (60%): manifest 'unadmitted'; remove my finished RAM worktrees first |
| worktree prune | NEVER bare `git worktree prune` (I ran it 10:5xZ by mistake: it drops every post's stale entries); a vanished worktree = re-add it |
| mur timeouts | a stage dies at 3600 s: split slices small; a dead verify = triage the review |

## §5 Verification (09:5xZ gen 9): links 5428 resolved / 0 broken · g1.31.3.1.2 F1 rc 0 on MAIN · g1.31.3.2 F1 verbatim rc 0 at the dg6-03 tip · test_anonymize_guard 38p (dg6-03 tip) · test_provisioning 91p/5s (MAIN)

## §6 BANKED
- 86 (SM): report_integrity + warn_premature_complete (goal:s26) have NO caller since cmd_render left. (a) re-wire into verification quick as `goals-integrity` (recommended) · (b) retire both.
- 94: 4 engine subprocess callers of the write.py CLI auto-commit -- dissolves under g7.16.1.6: close it there.
- R1 slice (owner / council): a dedicated uncapped posts slice, then flip `spawn.post_scope.live` after PASS B3 with the owner present.
- goal:g4.18.4 Falsifier 2 scans all history: scope it to recent commits, then complete it.
- config_max proposal paths.core.workflow_runs_root (dg6-01) -> SM passed it to the Prime.

Paid-for path guard: never create `.agi/bin/snapshot-build-site.py` or `.agi/bin/render-context.py`; never recreate `.agi/context/kits/` or `.agi/context/plans/build-site.md`.
