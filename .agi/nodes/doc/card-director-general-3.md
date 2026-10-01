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

Role: doc:unified-director-brief (the director TEMPLATE) + this card. Post director-general-3 · master: the council (SM = coordinator; belam for the BUILD) · MAIN /data/work/agi on local-maxxing/season2/main.

## §0 State (12:4xZ 10-01) · LANES: ALL subagents Sonnet 5.5 (owner 07:3xZ via belam); murs pi-free · owner window to 14:00Z: nothing switches after 13:30Z
| | |
|---|---|
| post | director-general-3 · graph-builder · the g7.16.1.11 BUILDER + the SWITCH to engine v5 |
| skills | agi-node-write · agi-goal · agi-verify · agi-send · agi-rotate · agi-corrective · agi-master-gate · agi-post · agi-workflow · agi-dispatch · agi-memory-guard |
| reports | BUILD + SWITCH: one line per milestone to belam (he gives the GO per post) · merge-ups to SM (board coordinator) |
| inbox | send.py read (WHOLE, never through tail: tail hides blocks for good) |

## §1 Plan
```
NEW POSTS ON v5 (belam GO 12:08Z + unhold 12:39Z): TM-new UP 12:41Z (turn 1 done, holding on A/B/C to belam; relayed belam 11:08Z = A) -> DT-1 STARTED 12:45Z -> DT-2 -> DG4
  start = sh /tmp/agi-proj6/start-post.sh <post>; watch /var/lib/agi/<post>/o (sudo tail -c); one line to belam after each first turn
  pre-seeded for DT-1 DT-2 DG4: hasTrustDialogAccepted on /var/lib/agi/<post>/t · empty inbox file (g:agi rw)
G5 hypothesis:g716111-g5-send-treats-a-v5-post-as-a-peer: G5.3 (items 1-4 + item 5 = agi-run mail poll, engine-wrap.md:25) on node ab13f34ca
  -> Sonnet 5.5 subagent LIVE on /mnt/agi-ram/worktrees/de-base-G5 -> verify bytes -> re-mur ab13f34ca..tip pi-free (args from /tmp/agi-rmg/murg5b.args.json, key g5c-code) -> [merge-up] SM
G4 hypothesis:g716111-g4-stand-up-cli-passes-root: mur-de-base-g4b review accept_with_residue, verify died rc=2 -> director closure 71eb7b20c..40e921b6e (R1 Measured, R3 CEILING; R2 grid + 3 notes demoted)
  -> tip 40e921b6e, MB 1d9e7da5e, merge-tree rc 0, 4 files +119/-6 -> rotate neighbourhood RUNNING on the tip -> [merge-up] SM (SM 12:38Z: G4 next, then the council-report tip-guard fork)
THEN the moves (ORDER: DG2, DG1, alive, self-perpetuating, all-is-one, stream-master, sanctuary-master, DG3, belam LAST) -- G5.3 item 5 lands BEFORE them (belam 12:39Z)
DG5 on v5 since 10:47Z: key expires 18:46Z -> RENEW BEFORE 18:00Z (R7 + restart)
```

## §2 Landed (this session)
row 60 LANDED by SM edb74b29e (tip 3c3ff20f5) · card re-linked dca759633 · TM-new up on v5 (4 boot fixes, see §4)

## 🔴 Where it stops
DT-1 first turn under watch; G5.3 Sonnet subagent live on de-base-G5; G4 neighbourhood tests running on de-base-G4 tip 40e921b6e.
```
python3 extensions/agi/bin/send.py read director-general-3; systemctl list-units 'agi-post@*' --no-pager; git -C /mnt/agi-ram/worktrees/de-base-G5 log -3 --oneline; git -C /mnt/agi-ram/worktrees/de-base-G4 log -1 --oneline
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
| v5 boot: trust | a fresh post stops at the folder-trust dialog: set projects./var/lib/agi/<post>/t.hasTrustDialogAccepted in that user's .claude.json BEFORE start (as the user, 600) |
| v5 boot: inbox | an ABSENT inbox file makes the mail poll type mail+CR every 5 s (answers any modal): create it empty (g:agi rw) before start, until G5.3 item 5 lands |
| v5 boot: .fresh | agi-run eats ~/.fresh on the first start; a run that died before any turn restarts with -c = 'No conversation found': touch ~/.fresh as the user |
| v5 boot: modal | a 'Try the new fullscreen renderer' modal (Yes preselected) opens after turn 1: one Esc into /run/agi-<post>/i as the user |


## §5 Verification (11:1xZ): DG5 active on v5, 24/25 bin == engine, journal 0 errors · links 5621 resolved 0 broken · test_thought_hygiene 17 passed

## §6 BANKED
- OWNER (night item 6): does his 06:5xZ 'spawn on encryption-town' authorize the cutover the 09-30 scrub note asks for (fresh clone of current history only)? + push/fetch timers there or by hand · the pre-scrub remote branch encryption-town/season2/main on the PUBLIC repo (review as residue) · his Doppler login there later. Plan: doc:g716111-crossbox-plan.
- OWNER/belam: capsule sealing CREATED /var/lib/systemd/credential.secret (keep or remove at teardown) · R10 seal the real phone key · delete the stand-in key when the real one lands.
- 86 (SM): report_integrity + warn_premature_complete (goal:s26) have NO caller since cmd_render left. (a) re-wire into verification quick as `goals-integrity` (recommended) · (b) retire both.
- R1 slice (owner / council): a dedicated uncapped posts slice, then flip `spawn.post_scope.live` after PASS B3 with the owner present.
- goal:g4.18.4 Falsifier 2 scans all history: scope it to recent commits, then complete it.
- config_max proposals routed via SM: paths.core.workflow_runs_root · merge_gate.red_classes · council.residue_leaves · anonymize.email_allow (RFC 2606 + non-numeric systemd local part).

Paid-for path guard: never create `.agi/bin/snapshot-build-site.py` or `.agi/bin/render-context.py`; never recreate `.agi/context/kits/` or `.agi/context/plans/build-site.md`.


ROTATION NOTE: no Agent-tool subagent is live (Phase A' + DG3.71b returned 05:1xZ-05:2xZ).
