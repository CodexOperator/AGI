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

Replaced whole, never appended; ≤ 100 lines; written DURING the work so a dead session is resumable.

## §0 State (00:0xZ 09-30) — seat agi-6b (gen 5); council RESUMED 23:4xZ (owner: "Restart council including DG5 stand up")
| | |
|---|---|
| post | director-general-3 · stage 3 of 3 — MVPs + build nodes + tests · graph-builder with DG4 (agi-47) + DG5 (agi-c8) |
| protocol | doc:council-loop (lens + Handoff: room `directors` = DG3/4/5 only) · goal:g7.16.1 · MAIN /data/work/agi on local-maxxing/season2/main |
| skills | agi-node-write · agi-goal · agi-verify · agi-send · agi-rotate · agi-post |
| sessions | DG1 agi-0c · DG2 agi-40 · DG4 agi-47 · DG5 agi-c8 · SM agi-e8 · belam agi-9c — look up session_name in config:posts after any rotation |
| split | room `directors` FINAL = DG3 23:39 (DG4 retracted its own): DG3 write.py + node_writer.py (CLAIMED) · bundle-4 W1/W2/W3 rest · g7.16.1.6 MACHINERY commit_node + the ~15-min snapshot cell (signature posted in the room) · DG4 .6 fill-in (non-rotate writers, grid crons, leftovers) · DG5 rotate.py WHOLLY (.7 + W1c) |

## §1 Plan
```
done   bundle 4: W-G.1 · W-G.2 · W0 · W1a · W1b · W2a · residues 81-100 102-107 (101 -> DG1) · BUILD1 8756efd6b (+ fix 838082ae9)
done   683c6f656 write.py refuses a 2nd positional script arg on an edit (it was silently dropped: 2 lost THOUGHTs)
WAIT   SM re-mur of 8198264d9 59032171c 4f1d10a75 838082ae9 683c6f656 8756efd6b (+ b8d232fc6's guard hunk) -> close what it names FIRST
QUEUE  (DG2 correctives, each a forked hypothesis with CEILING -- read the node before building):
       1 hypothesis:row-refuses-thought-markers-and-resolves-a-table-name (W1a disproved: a mid-body THOUGHT row duplicates; row name:<NAME>)
       2 hypothesis:a-write-commit-survives-a-busy-index (W1b: retry add/commit on index.lock <= 5x / 2 s, never a hook refusal)
         -- NOTE g7.16.1.6 replaces the branch commit with commit_node; build 2 only if .6 is not placed yet, keep it <= 12 prod lines
       3 hypothesis:one-per-read-mint-index-carries-type (W2a; W2b.2 depends on it; trap: a BODY line mint_id: in experiment:a00-3e7b260e-2cce33)
       4 hypothesis:node-type-schemas-name-a-thought-reader-that-exists (text-only, 16 schemas; DG4 may take it -- ask first)
NEXT   W2b.1 (.6.2.1 set refuses a missing id: strict xfail test_w2b1_set_refuses...) · W2b.2 (.6.2.2 after QUEUE 3) · W2c A-C · W2d · W2e ·
       W3a/b · W3c-1 then W3c-2 · then g7.16.1.6 machinery once the council places it and DG1 mints the leaf (NOT before)
FINDINGS SM N1 --dry-run skips submit's "replace body is standalone" (row N + note) · N2 dry-run reads body while submit reads replace_target ·
       N3 no dry-run test for row n:i-j refusal · links.md is NOT a render fixed point (19 lines) · banked 86 94 (§6)
NEVER  hypothesis:a-write-refuses-a-missing-outbound-id-by-lookup · hypothesis:every-link-reader-resolves-mint-ids (superseded)
```

## §2 Landed (this seat)
389afc3e1 f7a91e213 c8ca9c52d 21ee11c8b 8756efd6b 3d1d03054 683c6f656 838082ae9 8198264d9 59032171c 4f1d10a75 (+ my 107 hunk inside b8d232fc6)
earlier bundle 4: 41107692f 0a58fe968 e6bbc6527 82fce8a34 254f58ef7 08b921fd8 9eaf5992f 387359c62 5952b7131 14cf86000 82c4ec6d4 58332a732 fe0230f3f c13eec672 f9261c83e fd8d74ab3

## 🔴 Where it stops
Working the QUEUE after the residue batch; nothing live, nothing uncommitted of mine (heal.py / rotate.py dirt in MAIN is DG5's).
First command at wake:
```
python3 extensions/agi/bin/send.py --from director-general-3 read director-general-3
```

## §4 Traps
| trap | rule |
|---|---|
| MAIN is shared by every post | commit by exact path; `git diff` each file for FOREIGN hunks first (DG4's b8d232fc6 swept my uncommitted edit); never switch branches, stash or reset |
| suite lock races | the lock flips between check and run: /tmp/dg3_pt.sh <file> [-k ..] retries until pytest gets its own window; ONE file per run (PASS B3 on the box) |
| write.py in MAIN | commits ITSELF by exact path; a failed lock check skips a hand commit silently -- read git log -1 after every commit |
| write.py script | ONE script argument, verbs joined by ' && ' (a 2nd argv refuses since 683c6f656) |
| row <top>.<key> | src = the row's YAML VALUE; empty file = remove; YAML keys keep their colon (unify.py:) |
| grid.py commit --all | director template: never off season2/main -- the grid cron versions MAIN; do not run it by hand |
| test counts in commit messages | quote the FULL-file run, never a -k subset (SM N4) |
| `send.py read <self>` | always `--from director-general-3` |
| build parent shapes | [mvp] · [build, goal] · [goal, mvp] · [goal, idea] |
| replace body on a heading/paragraph line | refused: widen to whole section or the blank line above |
| posts row lookups | session names change at rotation: read config:posts (python yaml) -- send.py whois reads origin and may lag |

## §5 Verification (00:0xZ): write 151p/5x · node_writer 112p/3x · write_guard 32p · links 40p/2x · formation_readback 34p · verification 71p/2x · snapshot_goals 19p · commands_manifest 181p (b8d232fc6: 177) · links 5166/0 earlier

## §6 BANKED
- 86 (SM wf_8ce06028-a81): report_integrity + warn_premature_complete (goal:s26) have NO caller since cmd_render left; links.py does not check parents.
  Options: (a) re-wire both into verification level quick as a `goals-integrity` command (recommended) · (b) retire both and re-point the W2c-B xfail row.
- 94 ([red] with belam from SM): 4 engine subprocess callers of the write.py CLI auto-commit (rotate.py closeout · season.py:274 · sensei.py:2465 ·
  failures.py:361) -- DISSOLVES under g7.16.1.6 (a write is a grid-ref commit, no branch): recommend closing it there, not with an env opt-out.
- R1 slice (owner / council): a dedicated uncapped posts slice, then flip `spawn.post_scope.live` after PASS B3 with the owner present.
- goal:g4.18.4 Falsifier 2 scans all history: scope it to commits after 2c412e5bb, then complete it.

## Findings for the next bundle
- derived command tables (QUICKSTART, skills/agi) lag command:commands; .agi/nodes/.geometry/commands.md.bak is TRACKED with id command:commands
- test_workflow's leak detector flags --basetemp /tmp dirs as the real sessions dir · test_skills_first_turn_entry red: agi-post + agi-stream missing
- write.py stamps town: core on local-maxxing nodes · 4 build nodes carry stale BUILD-CONTRACTs · memory_alarm.py has no build node
- test_sensei_wake_audit item2 red (pre-existing) · heal._watch_seats tests read the live PSI (flaky under pressure)

Paid-for path guard: never create `.agi/bin/snapshot-build-site.py` or `.agi/bin/render-context.py`; never recreate `.agi/context/kits/` or `.agi/context/plans/build-site.md`.
