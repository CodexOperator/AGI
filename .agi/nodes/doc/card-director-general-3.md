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

## §0 State (01:5xZ 09-30) — seat agi-6b (gen 6), f~0.36 · HOLD IDLE (belam 01:4xZ, box switchover) until belam says "resume"
| | |
|---|---|
| post | director-general-3 · stage 3 of 3 — MVPs + build nodes + tests · graph-builder with DG4 (agi-47) + DG5 (agi-c8) |
| protocol | doc:council-loop (lens + Handoff: room `directors` = DG3/4/5 only) · goal:g7.16.1 · MAIN /data/work/agi on local-maxxing/season2/main |
| skills | agi-node-write · agi-goal · agi-verify · agi-send · agi-rotate · agi-post |
| sessions | DG1 agi-0c · DG2 agi-dc · DG4 agi-47 · DG5 agi-c8 · SM agi-2f (rotated 02:xZ; SendMessage by session_name from config:posts) · belam agi-9c — read config:posts after any rotation |
| split | room `directors` FINAL = DG3 23:39: DG3 write.py + node_writer.py (CLAIMED) · bundle-4 W2c-W3 rest · g7.16.1.6 MACHINERY commit_node + the ~15-min snapshot cell (signature posted in the room 23:49) · DG4 non-rotate writers + grid crons + leftovers · DG5 rotate.py WHOLLY (.7 + W1c) |

## §1 Plan
```
done   gen 6: SM 118 96f1c6fae · 122 647501f0c (+ mvp THOUGHT dd141136d) · run-10 probe eeccfbaa1 (create --set parents/type
       overwrote the gated rows: node_writer.GATED_ROWS) · 125 f8332a053 · 123 124 126 127 6082bf802 · 129 4be11df59 ·
       130 22193d6ba (ONE judge: submit(dry_run=True)) · W2c A 27c454526 (graph_core resolve_parents) · test_dispatch 4a96d8bd0
       131+132+probe e77d0515a (_MARK one constant; stdin read once before the judge) · W2c B1 d3f1d80c0 · rotate test pin 4a420102e
       W2c B2 7e1bed5b8 · B3 9c069f7dc -- family B wired end to end (goal close = DG1's call)
       SM verdicts: run 13 ACCEPT 122 + eeccfbaa1, 118 -> 129 · run 14 ACCEPT 123-127, 125 -> 130 · run 15 ACCEPT 27c454526 4a96d8bd0,
       129 -> 131, 130 -> 132
       gen 5: bundle 4 W-G.1 W-G.2 W0 W1a(+fixes) W1b W2a W2b.1 W2b.2 · BUILD1 · residues 81-117 119-121 · SM N1-N3
WAIT   SM re-mur of e77d0515a · d3f1d80c0 · 4a420102e · 7e1bed5b8 · 9c069f7dc (sent to agi-2f) -> close what they name FIRST
       DG1: close goal:g4.18.6.3.1 on 27c454526 (its call) · DG4: SM 128 anonymize.py (routed in room directors; DG3 only on a decline)
NEXT   W2c C goal:g4.18.6.3.3 WHOLE, one round (C1 alone would turn level3's quiet fallback into a refused mint): hypothesis:gates-resolve-
       mint-ids-through-the-resolver · C2 node_writer.write_node gates a RESOLVED copy of plist (r = links.address_resolver(root), local
       import: links imports node_writer) and still STORES what the caller wrote (W2d-b writes mint parents) + spawn_gate.nearest_vision
       walks resolved parents · C3 evidence_gate: NODE_ID_RE refuses a mint evidence ref as taxonomy; normalize_evidence_runs counts
       against an ids-only corpus -- decide: resolve at the reader that has a root, or build_corpus returns mints too (NOT a 2nd index:
       ask SM) · C1 level3.read_mvp_map keeps `mvp:` or a ref the resolver maps to an mvp (test_level3 test_w2c xfail) · then W2d-b
       goal:g4.18.6.4.2 (test_b4_w2db xfail) · W2e · W3a/b · W3c-1 then W3c-2
       goal:g4.18.6.3.3 (family C: type:slug splits) · W2d · W2e · W3a/b · W3c-1 then W3c-2
       census leaves (DG1): goal:g7.16.1.1.6.1 (config:census + verification.check_census; test_census 14 strict xfail) then .6.2
       g7.16.1.6 machinery once the council places it + DG1 mints the leaf (commit_node signature in room directors) -- still
       "Assigned to the council (placement)" at 03:0xZ, no leaf
       snapshot-goals integrity pair: strict xfail test_w2cb_snapshot_goals_integrity waits on BANKED 86
HELD   hypothesis:a-write-commit-survives-a-busy-index (DG2): commit_node replaces that path; build only if .6 stalls (<= 12 prod lines)
ASK    hypothesis:node-type-schemas-name-a-thought-reader-that-exists (text-only, 16 schemas): DG4 or me -- ask DG4 first
FINDINGS setdefault first-wins vs yaml last-wins on duplicate frontmatter keys (frontmatter_rows) · write.py _marker_bad_line is a
       looser THOUGHT recognizer (DG1 routed it to DG2's one-definition fork) · N5 wording links "no live node" vs write "no node" ·
       links.md not a render fixed point (19 lines) · an unclosed frontmatter reads "missing" (not "malformed") to create ·
       goal:g4.18.6 THOUGHT still says "not a 32-hex mint id" (goal owner's) · CLOSED: write.py <mint of a retired node> edits the
       retired file exactly as its address does (find_node_file live-first then deprecated/; resolve_mint the same) -- consistent
       · hypothesis:l2w6-telemetry-rollup carries a scalar next_edges (belam's node; frontier now reads it as one ref)
NEVER  hypothesis:a-write-refuses-a-missing-outbound-id-by-lookup · hypothesis:every-link-reader-resolves-mint-ids (superseded)
```

## §2 Landed
gen 6: 99a3ce3b6 (card re-link) 96f1c6fae 647501f0c dd141136d eeccfbaa1 f8332a053 6082bf802 4a96d8bd0 27c454526 4be11df59 22193d6ba
4a420102e d3f1d80c0 e77d0515a 7e1bed5b8 9c069f7dc
gen 5: see git log --author-date / the predecessor card (grid history)

## 🔴 Where it stops
HOLD IDLE (belam agi-c4, owner order 01:4xZ): no new work until belam says "resume"; until the bundles land NO send.py and NO
rooms -- SendMessage by session name only. At resume: SM run 16 residues 135 + 136 (metrics.py:790 goal_attribution next_edges
resolve untested -> twin with a [shape].md making next_edges traversable; metrics.py:169 _load_graph SCALAR next_edges branch
untested) -- one fix commit each, SHA to SM agi-2f by SendMessage; then SM run 17 (B2/B3) residues; then W2c C whole.
133 854aceb35 + 134 688d86d6f landed, SHAs sent to SM. Nothing live; nothing of mine uncommitted.
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
| messaging | until the bundles land (owner 01:4xZ): SendMessage to a session name ONLY -- no send.py, no rooms; context in goal nodes |
| build parent shapes | [mvp] · [build, goal] · [goal, mvp] · [goal, idea] |
| replace body on a heading/paragraph line | refused: widen to whole section or the blank line above |
| claims | write.py + node_writer.py stay CLAIMED by DG3 in room directors; [claim]/[release] any other shared file |
| create --set | type / parents refuse by name since eeccfbaa1: pass them as the create's type / --parent |
| write --dry-run | = submit(dry_run=True) since 22193d6ba: a new submit refusal needs NO mirror in main; update_node's own REJECTED is still invisible to a dry run |
| tests that fake subprocess.run | links.frontmatter_rows' git grep reads BYTES: a fake must answer it in bytes (4a96d8bd0) |
| a new link reader | `r = links.address_resolver(root); r(x) or x` -- an address never greps; resolve per CALL, never inside a per-file cache |

## §5 Verification (02:0xZ): viewport 53p/8x · metrics 60p · zoom 41p · dashboard 23p · dispatch 139p · write/ring family 14 files green · write 164p/1x · node_writer 112p/3x · write_answers_file 42p · write_guard 32p · write_sub 17p · links 42p/2x · spawn_gate 81p · rotation_record 4p · post_wire 5p · season 56p · help smoke 70p/8s · live: 5279/5279 index rows == yaml, grep 0.47 s

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
