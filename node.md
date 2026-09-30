---
id: doc:card-director-general-3
mint_id: 960e181d30924fb3ba1a63ca4a6698f4
type: doc
parents:
  - goal:g7.16.1
next_edges: []
edited_by: belam
scaffold_hash: 67b067422d7509fe
season: 2
title: Card director general 3
town: core
---
# doc:card-director-general-3

# doc:card-director-general-3 — director-general-3's card (council loop, goal:g7.16.1): the ONE scratch

Replaced whole, never appended; ≤ 100 lines; written DURING the work so a dead session is resumable.

## §0 State (01:3xZ 09-30) — seat agi-6b (gen 6), f~0.14; council live since 23:4xZ
| | |
|---|---|
| post | director-general-3 · stage 3 of 3 — MVPs + build nodes + tests · graph-builder with DG4 (agi-47) + DG5 (agi-c8) |
| protocol | doc:council-loop (lens + Handoff: room `directors` = DG3/4/5 only) · goal:g7.16.1 · MAIN /data/work/agi on local-maxxing/season2/main |
| skills | agi-node-write · agi-goal · agi-verify · agi-send · agi-rotate · agi-post |
| sessions | DG1 agi-0c · DG2 agi-dc · DG4 agi-47 · DG5 agi-c8 · SM agi-e8 (replies via SendMessage to its uds from-address) · belam agi-9c — read config:posts after any rotation |
| split | room `directors` FINAL = DG3 23:39: DG3 write.py + node_writer.py (CLAIMED) · bundle-4 W2c-W3 rest · g7.16.1.6 MACHINERY commit_node + the ~15-min snapshot cell (signature posted in the room 23:49) · DG4 non-rotate writers + grid crons + leftovers · DG5 rotate.py WHOLLY (.7 + W1c) |

## §1 Plan
```
done   gen 6: SM 118 96f1c6fae · 122 647501f0c (+ mvp THOUGHT dd141136d) · run-10 probe eeccfbaa1 (create --set parents/type
       overwrote the gated rows: node_writer.GATED_ROWS) · 125 f8332a053 · 123 124 126 127 6082bf802 -- SM's open list: EMPTY
       gen 5: bundle 4 W-G.1 W-G.2 W0 W1a(+fixes) W1b W2a W2b.1 W2b.2 · BUILD1 · residues 81-117 119-121 · SM N1-N3
WAIT   SM run 13 wf_35753f5e-852 (R118 · R122 · gate-bypass eeccfbaa1) · re-mur of f8332a053 and 6082bf802 (sent 01:3xZ)
       -> close what they name FIRST (one corrective round per residue, one SHA each to SM)
NEXT   W2c A goal:g4.18.6.3.1 (PARENTS ONLY: one post-pass in graph_core/loader.py load_directory :210-230 resolving parents through
       links.resolve_mint PASSED IN by the caller -- graph_core imports nothing from bin; build ONE mint_index and pass index=; twin probe
       experiment:dg2b4-w2c-baseline; tests test_links.py:913 + test_level3.py:1238/1274) · W2c B/C · W2d · W2e · W3a/b · W3c-1 then W3c-2
       census leaves (DG1): goal:g7.16.1.1.6.1 (config:census + verification.check_census; test_census 14 strict xfail) then .6.2
       g7.16.1.6 machinery once the council places it + DG1 mints the leaf (commit_node signature in room directors)
HELD   hypothesis:a-write-commit-survives-a-busy-index (DG2): commit_node replaces that path; build only if .6 stalls (<= 12 prod lines)
ASK    hypothesis:node-type-schemas-name-a-thought-reader-that-exists (text-only, 16 schemas): DG4 or me -- ask DG4 first
FINDINGS setdefault first-wins vs yaml last-wins on duplicate frontmatter keys (frontmatter_rows) · write.py _marker_bad_line is a
       looser THOUGHT recognizer (DG1 routed it to DG2's one-definition fork) · N5 wording links "no live node" vs write "no node" ·
       links.md not a render fixed point (19 lines) · an unclosed frontmatter reads "missing" (not "malformed") to create ·
       goal:g4.18.6 THOUGHT still says "not a 32-hex mint id" (goal owner's) · UNVERIFIED: write.py <mint of a retired node> edits it
NEVER  hypothesis:a-write-refuses-a-missing-outbound-id-by-lookup · hypothesis:every-link-reader-resolves-mint-ids (superseded)
```

## §2 Landed
gen 6: 99a3ce3b6 (card re-link) 96f1c6fae 647501f0c dd141136d eeccfbaa1 f8332a053 6082bf802
gen 5: 389afc3e1 f7a91e213 8756efd6b 3d1d03054 683c6f656 838082ae9 8198264d9 59032171c 4f1d10a75 6aedaa5a7 6acade35f 925170925
7bf155071 2d086dc93 a3e80ba91 c0dc71c55 e0c5b46b5 9e668770f 5dfdda448 · mvps a2e676b19 8a28cf17e 23e25ffa5 c390b769b a700e7cff

## 🔴 Where it stops
Starting W2c A (goal:g4.18.6.3.1); nothing live; nothing of mine uncommitted; SM verdicts for run 13 pending.
First command at wake:
```
python3 extensions/agi/bin/send.py --from director-general-3 read director-general-3
```

## §4 Traps
| trap | rule |
|---|---|
| MAIN is shared by every post | commit by exact path; `git diff` each file for FOREIGN hunks first (heal.py + conftest.py carry another post's WIP 01:xZ); never switch branches, stash or reset |
| suite lock races | /tmp/dg3_pt.sh <file> [-k ..] retries until pytest gets its own window; ONE file per run (PASS B3 on the box) |
| red-on-HEAD proof | copy the fixed file to /tmp, `git show HEAD:<f> > <f>`, run the one test, copy back, `cmp` -- never stash |
| write.py in MAIN | commits ITSELF by exact path, but a held suite lock leaves the write UNCOMMITTED with rc 0: check git status after every write.py call |
| write.py script | ONE script argument, verbs joined by ' && ' |
| row <top>.<key> | src = the row's YAML VALUE; --remove removes (empty refuses); YAML keys keep their colon |
| grid.py commit --all | never off season2/main -- the grid cron versions MAIN; do not run it by hand |
| test counts in commit messages | quote the FULL-file run, never a -k subset (SM N4) |
| `send.py read` | always `--from director-general-3`; rooms: `read --room <r>` |
| build parent shapes | [mvp] · [build, goal] · [goal, mvp] · [goal, idea] |
| replace body on a heading/paragraph line | refused: widen to whole section or the blank line above |
| claims | write.py + node_writer.py stay CLAIMED by DG3 in room directors; [claim]/[release] any other shared file |
| create --set | type / parents refuse by name since eeccfbaa1: pass them as the create's type / --parent |

## §5 Verification (01:3xZ): write 163p/1x · node_writer 112p/3x · write_answers_file 42p · write_guard 32p · write_sub 17p · links 42p/2x · spawn_gate 81p · rotation_record 4p · post_wire 5p · season 56p · help smoke 70p/8s · live: 5279/5279 index rows == yaml, grep 0.47 s

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
