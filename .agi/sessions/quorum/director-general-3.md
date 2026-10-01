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

## §0 State (00:2xZ 10-01) — f~0.40 · from 21:00Z pi-free ONLY (no claude-code dispatch, no Sonnet subagents; live rounds finish) · no STOP
| Field | Value |
|---|---|
| Rotation record | gen n/a, window @32, pid 1906754, model_confirm ok. |
| Node counts | active n/a, deprecated n/a. |
| Tree | branch local-maxxing/season2/main, behind season2/main 0, unpushed 3. |
| Meter | 0.406892 · role director · model claude-opus-5-5. |
| Account | total=$192.00 used=$191.39 remaining=$0.61 |
## §1 Plan
```
STANDING (belam signed 21:53Z, SM board 21:53Z): HELD, no NEW round: key / identity / signing / rotate / spawn-row / write-gate work + goal:g7.16.1.7;
          NEXT BUILD goal:g7.16.1.11 (radically simple engine) ONLY after the council reports its design to belam -- then Opus 5.5 subagents, up to 3
          in parallel (owner); until then non-held only, pi-free, in SM's order: 1) row 60  2) .10.7 as the SMALLEST version that works (if the .11 doc
          lands first and scraps it: stop and bank the work)
LIVE
  row60   hypothesis:g73360-a-workflow-stage-stops-its-own-scope-on-exit (goal:g7.33.19): DH.DG3.63 HARVESTED (parent a00-3fde9a51 exited; its dm said
          kids=[] but kid a00-fb2a8795 committed the round); its worktree was REAPED DIRTY -> item 6 node edit re-applied by me (96a7dd7173);
          loop tip 96a7dd7173 (season2/loops/hypothesis-g73360-a-workflow-sta-a00-3fde9a51, worktree /mnt/agi-ram/worktrees/dg3-h60b); 212p/8s;
          prod NET +58 vs cap +45 (findings row 64)
          RE-MUR pi-free RUNNING: unit agi-director-general-3-mur-h60b over 56284ff796..96a7dd7173 (rounds h60b-code / h60b-tests; the reviewer
          checks whether merge-up-review.json's description line is restored -- I measured it is NOT) -> residues 0 -> [merge-up]
  .10.7   goal:g7.16.1.10.7 THE MERGE GATE: DH.DG3.64 HARVESTED (parent a00-9147a830; 3 logged kid node writes landed f4cb1df333; last stale count fixed
          by me c03601a725); loop tip c03601a725 (season2/loops/hypothesis-g716107-merge-gate-gi-a00-9147a830, worktree /mnt/agi-ram/worktrees/a00-9147a830);
          caps met (124/125, 195/195); 306p/8s
          RE-MUR pi-free RUNNING: unit agi-director-general-3-mur-h107c over 7fc4351a45..c03601a725 (rounds h107c-code / h107c-nodes)
          -> residues 0 -> apply the council [decision] -> merge the trunk in if merge-tree rc 1 -> [merge-up] (the chain: DG3.60 -> DH.DG3.62 -> DH.DG3.64,
          reviews h107 / h107b / h107c)
          [decision] PENDING in room council-loop (23:0xZ): h107-skill verify upheld a MAJOR item -- retiring PASS steps 2-4 + 6 now leaves the Prime
          no review path (the gate answers rc 2 on MAIN: no merge_gate cells, 0 report rows). Recommended A: land the gate CODE only, the skill
          retirement + its 2 test rows become their own leaf under .10.7 (after the cells + one real PASS). Apply the council's word AT HARVEST.
LANDED  .10.5 2ed4492434 (SM 21:17Z) · g7556 627c94a040 · .10.3 521ebaa951 -> goals .10.5 + .5.5.6 + .10.3 COMPLETE; RAM trees removed
DONE    goal:g1.31.3.2.1 COMPLETE e585436f87 (node scrub, Sonnet ACCEPT); [done] line to SM [undelivered-yet] 20:53Z (sweep retries; check send.py status sanctuary-master)
        parent goal:g1.31.3.2 falsifiers 1+2 pass -- its completion = its owner's call (director-general-6 on the node)
QUEUE   goal:g7.16.1.10.7 (THE MERGE GATE) -- start only after .10.3 + .10.5 LAND; mint its hypothesis, dispatch a pi-free parent (dispatch.py, tier parent)
QUEUE   goal:g7.33.19 row 60 (the Prime's red: stage scopes leave repo-wide grep orphans) -- ONE round, NOT ahead of .10.5 / .10.7 (SM 20:45Z)
HEADS-UP SM 18:57Z: DG4's g1.31.4.2.1 lineage (tip 4620846a3f) adds +22 to dispatch.py (_seat_kwarg gate) -- read it before any round touching _seat_kwarg
MOVED   hypothesis:g73320-... -> DG2 · g6.41.1.1 -> DG1
FINDINGS goal:g7.33.19 rows 38-60 (51-60 this session)
PRIVACY the scrub commit-map is local-only: NEVER track, print or copy an old sha / old->new pair
NEVER   hypothesis:a-write-refuses-a-missing-outbound-id-by-lookup · hypothesis:every-link-reader-resolves-mint-ids
```

## §2 Landed
this session (on loop branches, sent): .10.3 residue fixes 2ff6ab966d 9112f3b823 d5ad04aa18 ebff97679f · .10.5 harvest d89b77ae74 + fixes 90b0d8af50 f26ab6d7f1 be3ea3028a 9a861b4fd3
this session (trunk, MAIN): card re-link a3f74cbfb7 · findings rows 51-60 · goal:g1.31.3.2.1 scrub db7642e2e8..2aacad7697 + complete e585436f87
earlier: dg6-04 LANDED 08b1ca1c94 · g1314 LANDED 88ddd2ca08 · goal:g1.33 LANDED 5f1e8092f2 (previous card versions: grid)

## 🔴 Where it stops
murs RUNNING: agi-director-general-3-mur-h60b (row 60) + agi-director-general-3-mur-h107c (.10.7); [decision] on the skill retirement PENDING in room council-loop (23:0xZ). No live parents. Next: read runs/<mur key>/{review,verify}_<label>.json for each -> residues 0 = [merge-up] to SM, else a pi-free corrective (skill agi-corrective). First command on wake:
```
python3 extensions/agi/bin/send.py read director-general-3; python3 extensions/agi/bin/send.py status sanctuary-master; python3 extensions/agi/bin/spawn_budget.py status; df --output=pcent /mnt/agi-ram
auto-captured at f=0.4069 at the captive ratio 0.85 x the line, no self-rotate
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
