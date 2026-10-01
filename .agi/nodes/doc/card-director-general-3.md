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

## §0 State (09:3xZ 10-01) — rotating at f~0.43 · LANES (owner 07:3xZ via belam): ALL subagents Sonnet 5.5; murs pi-free · night ORDER to 14:00Z (goal @8c43a220c)
| | |
|---|---|
| post | director-general-3 · graph-builder · the g7.16.1.11 BUILDER |
| skills | agi-node-write · agi-goal · agi-verify · agi-send · agi-rotate · agi-corrective · agi-master-gate · agi-post · agi-workflow · agi-dispatch · agi-memory-guard |
| reports | BUILD: ONE [decision] per milestone to belam · merge-ups to SM (board coordinator) |
| inbox | send.py read; belam's lines also arrive as cross-session messages -- the dm file belam--director-general-3.md is the source |

## §1 Plan
```
DG5 LIVE on engine v4c, PI-FREE: unit agi-post@director-general-5 (system, agi.slice), user agi-director-general-5, home /var/lib/agi/director-general-5
  Phase C DONE (rootplan sections PHASE C RUN 915ba64d9 + LIVE PARITY 3249d62b8: 37/55 live, 12 not run, short 18 30 33 42 43 45)
  42 FIXED live: /run drop-in ident.conf (GIT_* = the post, @example.invalid); DG5's commits rebuilt as the post, signed G; NOTHING leaves the box until belam re-checks
  43 R-MG APPLIED live (DG5 pi adj -900); repo form de-base-DG3.73 9f3e0811a -> mur-de-base-dg3-73 DONE accept_with_residue (4: cell for POST_CG + pi comm · test one-source · exec kill/run reach · real post name) -> CORRECTIVE DG3.73b on doc:g716111-stage25-rootplan @5547f7762, parent a00-8649eb44 iter DG3.74 pi-free LIVE 09:36Z, base de-base-DG3.73b (wt /mnt/agi-ram/worktrees/de-base-DG3.73b), loop season2/loops/doc-g716111-stage25-rootplan-a00-8649eb44 -> harvest -> re-mur 9f3e0811a..tip pi-free -> residues 0 -> merge chain at LAST tip -> [merge-up] SM
  45 C3 + MAIN allowedSignersFile: prepared (/tmp/agi-rmg/C3.md, SIGNERS.md), sent to belam 09:2xZ -- his acts
  R7 KEY TTL: RENEW BEFORE 16:00Z (re-run R7 from the rootplan + sudo systemctl restart agi-post@director-general-5); owner window ends 14:00Z
  12 NOT-RUN parity rows: run tonight what needs a DG5 rotation / a landing / a kid
ENGINE (belam lands; CAP RULING: bootstrap <= 8,192 B; 20,480 B = ONE post's read set)
  Round 5 doc:g716111-round5-build 1e84c1d02 · Round 6 doc:g716111-round6-build (BUILD FROM §T.1 @3772d6ff7) · Round 7 doc:g716111-round7-build 0a0eda87e
  LAND-READY PACKAGE DONE: doc:g716111-land-package d18ca7571 (bodies /tmp/agi-land/asbuilt + split-pkg, land.sh) -> [decision] to belam 09:3xZ: his calls = as-built vs SPLIT (rec; post read set 20,374 B) · identity domain (guard refuses example.invalid -> %i@agi) · parents goal only · order expansions first
     belam LANDS; after his landing: the live parity re-measure on v5 (round5 doc rows; F36 snapshot /tmp/agi-parity/bin.v4c) + restart DG5 on the new engine
CAPSULE: rehearsal R1-R9 INSTALLED (doc:g716111-capsule-build 32426bb7d); stand-in key file DELETED (T9); R10 = owner's go
§U-§X: phase A DONE dry (doc:g716111-uvwx-build 324fc96d8, 10 holes); real-box sshd acts await belam (patched vs doc + tonight or after cutover)
CROSS-BOX (item 6): doc:g716111-crossbox-plan f227e5393 -- BLOCKED on the owner's cutover (banked)
OWNER SWITCH ORDER (after rounds 5-7 land + parity 0 gaps + DG5 ran on it): every post except belam / thought-master / director-thought, one at a time, rollback each; belam LAST, gen continues
MERGE-UPS: row60 855daaccd re-sent to SM 06:4xZ (awaiting GO) · crmur deaa32675 + g7556 cd8ca3914 LANDED
```

## §2 Landed (this session)
docs: g716111-stage25-engine-v4c 300c29e4d · capsule-build 0f59c0398/32426bb7d · round5 1e84c1d02 · round6 58ff49120 · round7 0a0eda87e · uvwx 324fc96d8 · crossbox f227e5393 · rootplan sections (A' delta, V-L1, PHASE C RUN, LIVE PARITY)
code: C2 bf5fb95c82 (landed by belam aa2f2e28a) · R-MG 9f3e0811a (loop branch, unreviewed) · trunk landings by SM: deaa32675 (crmur), cd8ca3914 (g7556)
box (root, each with undo): /opt/agi/{bin,pi,capsule} · DG5 unit + user + slice + polkit + ACLs (rootplan §3/§4) · capsule rehearsal (/tmp/agi-capsule/undo.sh) · agi-memguard R-MG (.pre-rmg backup)

## 🔴 Where it stops
DG5 live; package with belam; R-MG mur running (detached); R7 key renew before 16:00Z. First commands on wake:
```
python3 extensions/agi/bin/send.py read director-general-3; tail -c 3000 .agi/comms/season-2/dm/belam--director-general-3.md; systemctl is-active agi-post@director-general-5; ls /tmp/agi-land/ 2>/dev/null
```
then: mur rmg -> read .agi/sessions/workflows/runs/mur-de-base-dg3-73/{review,verify}_rmg-code.json (masked) -> residues 0 = [merge-up] SM (tip 9f3e0811a) · belam's calls on the package -> help him land / re-measure · before 16:00Z renew R7 · run the not-run parity rows (a DG5 rotation, a kid)

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


## §5 Verification (09:2xZ): DG5 active 0 restarts, N4 PASS, commits signed G + post identity · links 5594 resolved 0 broken · boxkit 206 passed on de-base-DG3.73

## §6 BANKED
- OWNER (night item 6): does his 06:5xZ 'spawn on encryption-town' authorize the cutover the 09-30 scrub note asks for (fresh clone of current history only)? + push/fetch timers there or by hand · the pre-scrub remote branch encryption-town/season2/main on the PUBLIC repo (review as residue) · his Doppler login there later. Plan: doc:g716111-crossbox-plan.
- OWNER/belam: capsule sealing CREATED /var/lib/systemd/credential.secret (keep or remove at teardown) · R10 seal the real phone key · delete the stand-in key when the real one lands.
- 86 (SM): report_integrity + warn_premature_complete (goal:s26) have NO caller since cmd_render left. (a) re-wire into verification quick as `goals-integrity` (recommended) · (b) retire both.
- R1 slice (owner / council): a dedicated uncapped posts slice, then flip `spawn.post_scope.live` after PASS B3 with the owner present.
- goal:g4.18.4 Falsifier 2 scans all history: scope it to recent commits, then complete it.
- config_max proposals routed via SM: paths.core.workflow_runs_root · merge_gate.red_classes · council.residue_leaves · anonymize.email_allow (RFC 2606 + non-numeric systemd local part).

Paid-for path guard: never create `.agi/bin/snapshot-build-site.py` or `.agi/bin/render-context.py`; never recreate `.agi/context/kits/` or `.agi/context/plans/build-site.md`.


ROTATION NOTE: no Agent-tool subagent is live (Phase A' + DG3.71b returned 05:1xZ-05:2xZ).
