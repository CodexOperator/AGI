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

## §0 State (17:3xZ 09-30) — f~0.41 (line 0.47) — until the 18:00Z STOP
| | |
|---|---|
| post | director-general-3 · stage 3 of 3 — MVPs + build nodes + tests · graph-builder with DG4 + DG5 |
| protocol | doc:council-loop · goal:g7.16.1 |
| skills | agi-node-write · agi-goal · agi-verify · agi-send · agi-rotate · agi-corrective · agi-master-gate · agi-post |
| SM board rule | send the [merge-up] and WAIT for SM's GO; SM gates one at a time and LANDS |
| owner rule 16:4xZ (via SM 16:51Z) | kids on claude-code Sonnet 5.5, or Sonnet 5.5 subagents, or direct work: knock the bundles out by 18:00Z; reviews may ride Sonnet 5.5 subagents |

## §1 Plan
```
SENT, WAIT FOR GO (SM gates in this order)
  dg6-04  goal:g1.31.3.2 half a  tip 4dd121c405 (season2/loops/hypothesis-pb3-anonymize-refuses-a00-11395b98)  in SM's gate + suite since 17:05Z
          -> GO -> goal:g1.31.3.2 complete; the email_allow cell (RFC 2606 + non-numeric systemd local part) SM relays to the Prime
  g1314   LANDED 88ddd2ca08 by SM 17:31Z; goal:g1.31.4.1 + goal:g7.16.1.5.4 COMPLETE 0a99ae625f; RAM trees removed; DG2 does the post-build
  g7556   goal:g7.16.1.5.5.6  tip 6b444e66f1 (season2/loops/hypothesis-g7556-guard-ram-write-a00-b9773bd6)  sent 17:29Z
          -> GO -> goal:g7.16.1.5.5.6 complete
LIVE
  h10105  goal:g7.16.1.10.5 council report: mur unit agi-director-general-3-dg3mur-h10105-1628 over 66443d8fa8..62de7b8491
          (tip season2/loops/hypothesis-g716105-council-repor-a00-f43e8762; council_report.py 177 lines ACCEPTED as disclosed override)
          -> read runs/mur-season2-loops-hypothesis-g716105-council-repor-a00-f43e8762/{review,verify}_h10105-*.json -> residues:
          direct/Sonnet fix on the loop tip -> merge the trunk IN if merge-tree rc 1 -> gate -> [merge-up]; cell council.residue_leaves -> SM/Prime
  DG3.54  goal:g7.16.1.10.3 reds.py corrective DH.DG3.54 (12 items), parent a00-9ed505e4 from de-base-DG3.54 (loop tip 8725ffca96)
          -> harvest (parents may not commit: land logged node bytes, merge the kid) -> review 8725ffca96..tip -> gate -> [merge-up];
          cell merge_gate.red_classes -> SM/Prime
QUEUE   NEXT RUN = goal:g1.31.3.2.1 (DG1 placement, HORIZON; SM 17:37Z; seeded by hypothesis:pb3-close-the-four-residual-falsifier-and-leak-gaps):
        half b's stale conjunct + 1 self-matching line NOT in DG2's nodes (DG2 splits its own 5) + DG1's finding: 3 tracked nodes carry a single-dash
        ENCODED repo path the goal's pattern never checked (hypothesis:lm-magic-pane-wrapper-prose-to-one-structured-call ·
        hypothesis:lm-qk-norm-matched-fresh-key-only-grid · idea:lm-why-key-only-grid-not-self-contained; counts only, never print them) ->
        widen the pattern + scrub by class label. DONE by others: hardware fragment 930e65687c · falsifier 1 && 725f70cb62 (DG1)
QUEUE   goal:g7.16.1.10.7 (THE MERGE GATE) needs .10.3 + .10.5 landed first -- horizon, do not start before both land
MOVED   hypothesis:g73320-write-rows-pass-in-the-full-suite-once-the-poisoning-leak-is-fixed -> DG2 (SM 16:5xZ); back to me only if the fix site is production write.py/node_writer.py
        g6.41.1.1 -> DG1
FINDINGS goal:g7.33.19 rows 38 (write.py sub strips leading whitespace), 39 + 41 (pi parents pass kid/test caps, self-answered rebriefs), 40 (a kid wrote its brief node)
PRIVACY the scrub commit-map is local-only: NEVER track, print or copy an old sha / old->new pair
NEVER   hypothesis:a-write-refuses-a-missing-outbound-id-by-lookup · hypothesis:every-link-reader-resolves-mint-ids
```

## §2 Landed
this session: goal:g1.33 LANDED 5f1e8092f2 by SM (tip 1d8fd19b90; links.py sha manifest row) · goal:g1.33 complete f701f063bc · goal:g1.31.4.1.1 minted 4f235b7bc1 · hypotheses minted g716103 (5a6fecd879), g716105 (50603f2b1e), g73320 (7773a02da9)
earlier: previous card versions (grid)

## 🔴 Where it stops
3 merge-ups WAIT for SM's GO (dg6-04 -> g1314 -> g7556); LIVE: mur h10105 + parent DG3.54 a00-9ed505e4. First command on wake:
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

## §5 Verification (17:2xZ): g7556 tip 132p/8s · g1314 tip 156p (1 INHERITED red in test_dispatch.py) · dg6-04 tip 280p/1s/1x · h10105 tip 467p/8s/1x

## §6 BANKED
- 86 (SM): report_integrity + warn_premature_complete (goal:s26) have NO caller since cmd_render left. (a) re-wire into verification quick as `goals-integrity` (recommended) · (b) retire both.
- R1 slice (owner / council): a dedicated uncapped posts slice, then flip `spawn.post_scope.live` after PASS B3 with the owner present.
- goal:g4.18.4 Falsifier 2 scans all history: scope it to recent commits, then complete it.
- config_max proposals routed via SM: paths.core.workflow_runs_root · merge_gate.red_classes · council.residue_leaves · anonymize.email_allow (RFC 2606 + non-numeric systemd local part).

Paid-for path guard: never create `.agi/bin/snapshot-build-site.py` or `.agi/bin/render-context.py`; never recreate `.agi/context/kits/` or `.agi/context/plans/build-site.md`.
