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

## §0 State (02:3xZ 10-01) — f~0.26 · LANES (belam 02:27Z, owner): DG3 = Opus 5.5 subagents at effort MEDIUM for everything, up to 3; free lane ENDED (pi-free stays a lane)
| | |
|---|---|
| post | director-general-3 · stage 3 of 3 — MVPs + build nodes + tests · graph-builder with DG4 + DG5 |
| protocol | doc:council-loop · goal:g7.16.1 |
| skills | agi-node-write · agi-goal · agi-verify · agi-send · agi-rotate · agi-corrective · agi-master-gate · agi-post · agi-workflow · agi-dispatch |
| SM board rule | send the [merge-up] and WAIT for SM's GO; SM gates one at a time and LANDS |
| lanes | FROM 21:00Z: every NEW round + review on pi-free (workflow.py run merge-up-review --harness pi-free, detached systemd-run) |

## §1 Plan
```
BUILD   goal:g7.16.1.11 (belam [decision] 01:58Z, owner 01:0xZ 'Stages 1-2 now, stop before 3'): source config:engine v2 @50eda68b1f (read sect)
  S1    PASS 02:0xZ, reported to belam [delivered]: agi-project dry -> 10 units = the 10 live local-town posts; evidence /tmp/agi-stage1/REPORT.txt
        gaps: 1 system-shaped unit in the user manager · 2 H undefined (no env) · 3 no users projected · 4 project.sh 28 vs agi-project 10 · 5 fresh key per user
  S2    PASS 7/7 (run 02:49-02:58Z, 0 USD), result on doc:g716111-stage2-rootplan 92cd0739be; teardown re-verified clean by me;
        [decision] to belam 03:0xZ [delivered]; disclosed R1 52 s early + R13 clone-ownership corrective; 6 council findings on the node
  S2.5  (owner 02:55Z, belam signed): AFTER S2 passes + belam relays: ONE live post on the LIVE repo under config:engine, picked WITH belam;
        bar = PARITY TABLE (every capability today -> new mechanism -> proved) incl (a) node<->code auto-link (b) per-node tiny worktree at a
        config location, pulled on version, purged from RAM; root acts + undo first; one-command rollback. PREP DONE: doc:g716111-stage25-parity 2e6fca914e
        (42 rows: 12 at/above parity, ~2.9 KB to close; candidate director-general-6); 5 calls sent to belam 03:2xZ [delivered] -- wait for the relay + calls
  STOP  before stage 3 (migration, retiring Python): the owner's word through belam
HELD    key / identity / signing / rotate / spawn-row / write-gate work + goal:g7.16.1.7 (this build replaces it)
LIVE
  row60   hypothesis:g73360-a-workflow-stage-stops-its-own-scope-on-exit: DH.DG3.66 pi parent a00-cd04d946 CUT 03:4xZ (idle 2h45m, 0 CPU; its scope
          stopped, worktree reaped); kid tip e81f782a19 over caps -> FINISHED by an Opus subagent 8abfaf9e9d on de-base-DG3.69: prod +52/+58, test 260/260,
          json line 4 restored, items 1-6 done; 213p/8s/3f (3 = stray /tmp/.agi, red on trunk too; [red] to SM 04:0xZ) -> mur h60c RUNNING -> [merge-up]
  g7556f  hypothesis:g7556-fstype-root-mount-and-ram-tier-through-ramw: BUILT 0d7a379694 on de-base-DG3.70 (136p/8s, caps met) -> mur h7556f RUNNING -> [merge-up]
  crmur   hypothesis:council-report-reads-the-mur-args-shape-per-round: BUILT 2634a61987 on de-base-DG3.71 (483p/8s/1x, +22/+40; lean 85: flat
          shape w/o tips still ?..?) -> mur hcr RUNNING (unit agi-director-general-3-mur-hcr) -> [merge-up] -> SM tells the Prime the cells may be set
  .10.7   goal:g7.16.1.10.7 THE MERGE GATE: [merge-up] SENT to SM 03:4xZ [delivered] -- tip 27042fc3cf (branch de-base-DG3.68), mb 8523e5e563,
          merge-tree vs trunk 22dcca1f34 rc 0, 12 files +1134/-5, 305p/8s; murs h107..h107f all closed in-loop (h107f prose closed by me, no re-mur)
          SM 03:30Z COORDINATOR CALL: land under OPTION A after its full suite (GO or return pending); cells wait for crmur; SM carries the [rule]
LANDED  .10.5 2ed4492434 (SM 21:17Z) · g7556 627c94a040 · .10.3 521ebaa951 -> goals .10.5 + .5.5.6 + .10.3 COMPLETE; RAM trees removed
DONE    goal:g1.31.3.2.1 COMPLETE e585436f87 (node scrub, Sonnet ACCEPT); [done] line to SM [undelivered-yet] 20:53Z (sweep retries; check send.py status sanctuary-master)
        parent goal:g1.31.3.2 falsifiers 1+2 pass -- its completion = its owner's call (director-general-6 on the node)
QUEUE   goal:g7.16.1.10.7 (THE MERGE GATE) -- start only after .10.3 + .10.5 LAND; mint its hypothesis, dispatch a pi-free parent (dispatch.py, tier parent)
QUEUE   goal:g7.33.19 row 60 (the Prime's red: stage scopes leave repo-wide grep orphans) -- ONE round, NOT ahead of .10.5 / .10.7 (SM 20:45Z)
HEADS-UP SM 18:57Z: DG4's g1.31.4.2.1 lineage (tip 4620846a3f) adds +22 to dispatch.py (_seat_kwarg gate) -- read it before any round touching _seat_kwarg
MOVED   hypothesis:g73320-... -> DG2 · g6.41.1.1 -> DG1
FINDINGS goal:g7.33.19 rows 38-67 (51-67 this session; 65 blind harvest x2, 66 grace literal, 67 four no-grep carriers)
PRIVACY the scrub commit-map is local-only: NEVER track, print or copy an old sha / old->new pair
NEVER   hypothesis:a-write-refuses-a-missing-outbound-id-by-lookup · hypothesis:every-link-reader-resolves-mint-ids
```

## §2 Landed
this session (on loop branches, sent): .10.3 residue fixes 2ff6ab966d 9112f3b823 d5ad04aa18 ebff97679f · .10.5 harvest d89b77ae74 + fixes 90b0d8af50 f26ab6d7f1 be3ea3028a 9a861b4fd3
this session (trunk, MAIN): card re-link a3f74cbfb7 · findings rows 51-60 · goal:g1.31.3.2.1 scrub db7642e2e8..2aacad7697 + complete e585436f87
earlier: dg6-04 LANDED 08b1ca1c94 · g1314 LANDED 88ddd2ca08 · goal:g1.33 LANDED 5f1e8092f2 (previous card versions: grid)

## 🔴 Where it stops
LIVE: corrective parents a00-cd04d946 (row 60 DH.DG3.66) + a00-46e3ab5f (.10.7 DH.DG3.67). Next: each exits -> harvest (traps: kids=[] dm lies, dirty logged node writes, reaped worktree) -> touched tests + neighbourhood -> re-mur (h60c / h107e, pi-free, detached) -> residues 0 = [merge-up] to SM, else a corrective. First command on wake:
```
python3 extensions/agi/bin/send.py read director-general-3; python3 extensions/agi/bin/send.py status sanctuary-master; python3 extensions/agi/bin/spawn_budget.py status; df --output=pcent /mnt/agi-ram
```

## §4 Traps
| trap | rule |
|---|---|
| MAIN is shared | commit by exact path; check each file for FOREIGN hunks first; never switch branches, stash or reset |
| landing | SM lands; a chain whose merge-tree vs HEAD is rc 1: merge the trunk INTO the loop branch in its worktree, resolve (node sections: keep both sides' CORRECTIVE sections, the newer THOUGHT), re-test, re-gate |
| parents may not commit | write.py refuses 'tier parent may not commit (goal:s27)': at harvest, land the dirty node bytes ONLY if sha256 == the last write-log entry, then merge the KID branch into the loop branch yourself; unlogged bytes: re-apply the content as the director via write.py |
| vanishing worktrees | a round worktree can be pruned under you: re-add it on its loop branch (git worktree add <path> <branch>) |
| write.py sub | strips leading whitespace off BOTH sides: anchor on a non-indented start, --dry-run first on frontmatter; >1 occurrence = sub! |
| pi-free mur verify | times out at 3600 s on the memcap/dispatch slices: a dead verify = triage the review; small re-reviews go to a Sonnet 5.5 subagent (owner 16:4xZ) |
| mur verdict JSON | read masked (hex -> <h>, emails, home paths); unstructured review = parse the defects text |
| edited_by | pass --actor director-general-3 --role director on EVERY write.py call |
| RAM hold | dispatch holds at the RAM disk >= 60%: remove finished RAM worktrees (never bare git worktree prune) |

| manifest row | write.py row manifest.<key> refuses an ABSENT key: set manifest <whole mapping as JSON> via a python subprocess (single quotes in the JSON; 77 KB < argv cap); --dry-run first; the diff must be the new row only |
| the old units | agi-director-general-3-dg3mur-* units read failed: the earlier murs whose verify timed out, already triaged -- not live work |
| round worktrees vanish | the RAM reaper removes a round worktree once its parent exits (both did at 20:4xZ, mid-command): commits are safe on the branch; re-add with git worktree add <path> <branch> |
| links MALFORMED | links.py links prints 13 MALFORMED FILE SCOPE lines on lm-* hypotheses: pre-existing off-shape, not damage (broken stays 0) |

## §5 Verification (20:5xZ): .10.3 tip ebff97679f 269p/8s (reds + manifest + help) · .10.5 tip 9a861b4fd3 476p/8s/1x (council + write + manifest + help) · g7556 tip 132p/8s · links 5533 resolved 0 broken

## §6 BANKED
- 86 (SM): report_integrity + warn_premature_complete (goal:s26) have NO caller since cmd_render left. (a) re-wire into verification quick as `goals-integrity` (recommended) · (b) retire both.
- R1 slice (owner / council): a dedicated uncapped posts slice, then flip `spawn.post_scope.live` after PASS B3 with the owner present.
- goal:g4.18.4 Falsifier 2 scans all history: scope it to recent commits, then complete it.
- config_max proposals routed via SM: paths.core.workflow_runs_root · merge_gate.red_classes · council.residue_leaves · anonymize.email_allow (RFC 2606 + non-numeric systemd local part).

Paid-for path guard: never create `.agi/bin/snapshot-build-site.py` or `.agi/bin/render-context.py`; never recreate `.agi/context/kits/` or `.agi/context/plans/build-site.md`.
