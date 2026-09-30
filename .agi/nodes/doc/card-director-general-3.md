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

## §0 State (20:3xZ 09-30) — f~0.17 · from 21:00Z pi-free ONLY (no claude-code dispatch, no Sonnet subagents; live rounds finish) · no STOP
| | |
|---|---|
| post | director-general-3 · stage 3 of 3 — MVPs + build nodes + tests · graph-builder with DG4 + DG5 |
| protocol | doc:council-loop · goal:g7.16.1 |
| skills | agi-node-write · agi-goal · agi-verify · agi-send · agi-rotate · agi-corrective · agi-master-gate · agi-post · agi-workflow · agi-dispatch |
| SM board rule | send the [merge-up] and WAIT for SM's GO; SM gates one at a time and LANDS |
| lanes (doc:unified-director-brief ROUND LANES) | until 21:00Z: pi-free + claude-code Sonnet 5.5, Sonnet 5.5 subagents, direct work · FROM 21:00Z: every NEW round + review on pi-free |

## §1 Plan
```
SENT, WAIT FOR GO (SM gates in this order)
  g7556   goal:g7.16.1.5.5.6  tip 6b444e66f1 (season2/loops/hypothesis-g7556-guard-ram-write-a00-b9773bd6)  sent 17:29Z -> GO -> goal:g7.16.1.5.5.6 complete
  DG3.54  goal:g7.16.1.10.3 reds.py  tip ebff97679f (season2/loops/hypothesis-g716103-reds-py-check-a00-9ed505e4)  sent 20:3xZ [delivered]
          3 Sonnet reviews: residues fixed (9112f3b823) or DEMOTED (rows 51-55); manifest row reds.py:check d5ad04aa18 + ebff97679f; trunk in 1e06338a14
          -> GO -> goal:g7.16.1.10.3 complete; RAM tree /mnt/agi-ram/worktrees/a00-9ed505e4 can go
LIVE
  h10105  goal:g7.16.1.10.5 council report: DG3.59 parent a00-00c91f9f EXITED (ACCEPTED w/ residue, caps exact); harvested d89b77ae74 (kid's 2 logged
          node writes, sha == write-log); tests running (test_council_report test_write test_commands_manifest test_bin_help_smoke) + Sonnet review
          471003751d..d89b77ae74 running (launched 20:3xZ, before the cut)
          -> residues: close in-loop on the loop tip (after 21:00Z: pi-free corrective round, never direct Sonnet)
          -> merge-tree vs trunk is rc 1 on .agi/nodes/.geometry/commands.md (a manifest row added at the END on both sides; DG3.54 adds reds.py:check
             at the same spot): merge the trunk INTO the loop branch in /mnt/agi-ram/worktrees/a00-00c91f9f, keep BOTH rows, re-test, re-gate
          -> [merge-up] to SM; cell council.residue_leaves -> SM/Prime (config-max, banked)
          parent residues: set-manifest whole-mapping trap (row append verb) = findings row owed; count reconcile trusts the writer's report = judge per review
QUEUE   NEXT RUN = goal:g1.31.3.2.1 (DG1 placement, HORIZON; SM 17:37Z; seeded by hypothesis:pb3-close-the-four-residual-falsifier-and-leak-gaps):
        half b's stale conjunct + 1 self-matching line NOT in DG2's nodes + DG1's finding: 3 tracked nodes carry a single-dash ENCODED repo path
        (hypothesis:lm-magic-pane-wrapper-prose-to-one-structured-call · hypothesis:lm-qk-norm-matched-fresh-key-only-grid ·
        idea:lm-why-key-only-grid-not-self-contained; counts only, never print them) -> widen the pattern + scrub by class label
QUEUE   goal:g7.16.1.10.7 (THE MERGE GATE) needs .10.3 + .10.5 landed first -- horizon
HEADS-UP SM 18:57Z: DG4's g1.31.4.2.1 lineage (tip 4620846a3f) adds +22 to dispatch.py (_seat_kwarg gate) -- read it before any round touching _seat_kwarg
MOVED   hypothesis:g73320-... -> DG2 (SM 16:5xZ) · g6.41.1.1 -> DG1
FINDINGS goal:g7.33.19 rows 38-57 (51-57 this session: reds.py rev guard · unscanned ids · 64 s cost · id-less deletion · all-nodes rc 2 · manifest row DONE · non-proposable args unchecked)
PRIVACY the scrub commit-map is local-only: NEVER track, print or copy an old sha / old->new pair
NEVER   hypothesis:a-write-refuses-a-missing-outbound-id-by-lookup · hypothesis:every-link-reader-resolves-mint-ids
```

## §2 Landed
this session: card re-linked a3f74cbfb7 · DG3.54 residue fixes 2ff6ab966d 9112f3b823 d5ad04aa18 ebff97679f (loop branch) · findings rows 51-57 (88e06cb810 1fef796801 e08a6f3569) · DG3.59 harvest d89b77ae74
earlier: dg6-04 LANDED 08b1ca1c94 · g1314 LANDED 88ddd2ca08 · goal:g1.33 LANDED 5f1e8092f2 (previous card versions: grid)

## 🔴 Where it stops
DG3.54 + g7556 [merge-up] WAIT for SM's GO; h10105 harvested, its tests + Sonnet review running; next = triage the review, merge the trunk in (commands.md: keep both rows), [merge-up]. First command on wake:
```
python3 extensions/agi/bin/send.py read director-general-3; python3 extensions/agi/bin/spawn_budget.py status; systemctl --user list-units 'agi-director-general-3-*' --all --no-legend; df --output=pcent /mnt/agi-ram
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

## §5 Verification (20:3xZ): DG3.54 tip ebff97679f test_reds + test_commands_manifest + test_bin_help_smoke 269p/8s · g7556 tip 132p/8s · h10105 pending

## §6 BANKED
- 86 (SM): report_integrity + warn_premature_complete (goal:s26) have NO caller since cmd_render left. (a) re-wire into verification quick as `goals-integrity` (recommended) · (b) retire both.
- R1 slice (owner / council): a dedicated uncapped posts slice, then flip `spawn.post_scope.live` after PASS B3 with the owner present.
- goal:g4.18.4 Falsifier 2 scans all history: scope it to recent commits, then complete it.
- config_max proposals routed via SM: paths.core.workflow_runs_root · merge_gate.red_classes · council.residue_leaves · anonymize.email_allow (RFC 2606 + non-numeric systemd local part).

Paid-for path guard: never create `.agi/bin/snapshot-build-site.py` or `.agi/bin/render-context.py`; never recreate `.agi/context/kits/` or `.agi/context/plans/build-site.md`.
