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

## §0 State (00:4xZ 09-30) — seat agi-6b (gen 5); council RESUMED 23:4xZ (owner: "Restart council including DG5 stand up")
| | |
|---|---|
| post | director-general-3 · stage 3 of 3 — MVPs + build nodes + tests · graph-builder with DG4 (agi-47) + DG5 (agi-c8) |
| protocol | doc:council-loop (lens + Handoff: room `directors` = DG3/4/5 only) · goal:g7.16.1 · MAIN /data/work/agi on local-maxxing/season2/main |
| skills | agi-node-write · agi-goal · agi-verify · agi-send · agi-rotate · agi-post |
| sessions | DG1 agi-0c · DG2 agi-40 · DG4 agi-47 · DG5 agi-c8 · SM agi-e8 · belam agi-9c — look up session_name in config:posts after any rotation |
| split | room `directors` FINAL = DG3 23:39 (DG4 retracted its own): DG3 write.py + node_writer.py (CLAIMED) · bundle-4 W1/W2/W3 rest · g7.16.1.6 MACHINERY commit_node + the ~15-min snapshot cell (signature posted in the room) · DG4 .6 fill-in (non-rotate writers, grid crons, leftovers) · DG5 rotate.py WHOLLY (.7 + W1c) |

## §1 Plan
```
done   bundle 4: W-G.1 · W-G.2 · W0 · W1a · W1b · W2a · residues 81-100 102-107 109-113 115 (101 -> DG1 closed; 108 ruled rc 0, reason on mvp:dg3b4-w1b-write-is-a-commit)
done   BUILD1 8756efd6b + 838082ae9 + 925170925 · 683c6f656 (2nd script arg refused)
done   DG2 forks: W1a corrective 6aedaa5a7 -> DISPROVED narrow -> corrective 2 2d086dc93 (mvp:dg3b4-w1a-fix2-one-thought-separator) ·
       W2a mint index 6acade35f (mvp:dg3b4-w2a-fix-mint-index)
WAIT   SM re-mur of 7bf155071 925170925 2d086dc93 6acade35f · DG2 verdicts on 2d086dc93 + 6acade35f -> close what they name FIRST
       routed: 114 -> DG2 (its hypothesis's falsifier 1) · 113's falsifier grep -> DG1 (goal:g7.16.1.2.7)
NEXT   W2b.1 goal:g4.18.6.2.1 (set parents/next_edges refuse a missing id with create's ONE lookup; strict xfail test_w2b1_set_refuses...)
       W2b.2 goal:g4.18.6.2.2 (create's gate reads mint_index ONCE per create) · W2c A-C · W2d · W2e · W3a/b · W3c-1 then W3c-2
       census leaves from DG1: goal:g7.16.1.1.6.1 (config:census + verification.check_census, test_census 14 strict xfail) then .6.2 (home-path rule)
       g7.16.1.6 machinery once the council places it + DG1 mints the leaf (commit_node signature posted in room directors)
HELD   hypothesis:a-write-commit-survives-a-busy-index (DG2): commit_node replaces that path; build only if .6 stalls (<= 12 prod lines)
ASK    hypothesis:node-type-schemas-name-a-thought-reader-that-exists (text-only, 16 schemas): DG4 or me -- ask DG4 first
FINDINGS SM N1-N3 (dry-run vs submit parity) · N5 links "no live node" vs write "no node" wording · N6 fm row re-renders the frontmatter
       (links.md not a fixed point) · N7 -> DG4 (verification.py:4-8 names verify_unified) · UNVERIFIED: write.py <mint of a retired node> edits it: decide
NEVER  hypothesis:a-write-refuses-a-missing-outbound-id-by-lookup · hypothesis:every-link-reader-resolves-mint-ids (superseded)
```

## §2 Landed (this seat)
389afc3e1 f7a91e213 8756efd6b 3d1d03054 683c6f656 838082ae9 8198264d9 59032171c 4f1d10a75 6aedaa5a7 a2e676b19 6acade35f 925170925
7bf155071 2d086dc93 1fa18de27 2a983695f 8a28cf17e 23e25ffa5 29f5fdbfb (+ my 107 hunk inside b8d232fc6) · cards c8ca9c52d 8ca4c24e6

## 🔴 Where it stops
Next: W2b.1 (NEXT row 1); nothing live; nothing uncommitted of mine (heal.py / rotate.py dirt in MAIN is DG5's).
First command at wake:
```
python3 extensions/agi/bin/send.py --from director-general-3 read director-general-3
```

## §4 Traps
| trap | rule |
|---|---|
| MAIN is shared by every post | commit by exact path; `git diff` each file for FOREIGN hunks first (DG4's b8d232fc6 swept my uncommitted edit); never switch branches, stash or reset |
| suite lock races | the lock flips between check and run: /tmp/dg3_pt.sh <file> [-k ..] retries until pytest gets its own window; ONE file per run (PASS B3 on the box) |
| write.py in MAIN | commits ITSELF by exact path, but a held suite lock leaves the write UNCOMMITTED with rc 0 (note on stderr): never tail it -- check git status after every write.py call |
| write.py script | ONE script argument, verbs joined by ' && ' (a 2nd argv refuses since 683c6f656) |
| row <top>.<key> | src = the row's YAML VALUE; --remove removes (empty refuses); YAML keys keep their colon (unify.py:) |
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
