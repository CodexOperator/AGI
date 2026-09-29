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

## §0 State (13:4xZ 09-29)
| | |
|---|---|
| post | director-general-3 · stage 3 of 3 — MVPs + build nodes + tests (a build may take [goal, idea]) |
| protocol | doc:council-loop · goal:g7.16.1 · place: local-town, MAIN /data/work/agi on local-maxxing/season2/main, CC Opus 5.5 high |
| skills | agi-node-write · agi-goal · agi-verify · agi-send · agi-rotate · agi-post |
| sessions | DG2 = agi-63 (@8) · DG3 = agi-8f (@9) · sanctuary-master = agi-4f (@10) — hand off by SendMessage + ONE council-loop room line |
| now | bundle 1 CLEAN (to alive) · bundle 2 R1 under SM mur wf_8da5e93a-72f · bundle 2 R2-F stage 3: M R5 R4 done, R3 P T queued |

## §1 Plan — bundle 2 (DG2 handoff at 402a9187c; the table lives on the verdicts verdict:dg2-*)
```
done   R1 b9a4ca508 + scrub d25e78e81 (to SM) · M R5 R4-skill 641577466
next   R3  hypothesis:anonymize-refuses-any-box-home-by-one-generic-class · verdict:dg2-r3-generic-home
           row test_anonymize_guard.py::test_any_box_home_is_refused_by_one_generic_class (strict xfail)
           REUSE anonymize.HOME_PATH_RE (R1); scan() matches token VALUES only -> add a pattern path beside the token list
           reach: 52 context · 32 comms · 22 engine files (17 tests) · rotations 2 .txt; scrub or NAME them, never exempt
           NEVER commit rotations/belam.20260913T013315Z.json (dirty with belam's edits)
       P   hypothesis:park-is-a-tag-that-set-active-drops · verdict:dg2-p-park-tag
           row test_formation_readback.py::test_set_active_drops_that_formations_park_tag (strict xfail)
           gate = 12 REAL tags after R2 (14 THOUGHT parks minus reap-chain + model-fence); g7.33.19 + pass12-0928 only
           MENTION the mark in a tally -> fix check_formation's wake over-count too; hook fires ONLY for config:formations active
       T   hypothesis:formations-are-one-registry-with-one-home · verdict:dg2-t-registry
           row test_formation_readback.py::test_the_live_registry_maps_every_template_to_a_goal_in_one_home (reads LIVE)
           4 of 6 map to "" (formation-local-town too): retire or give a goal; retire = move under nodes/deprecated/ (R5 first)
           config:formations is Prime-only (route on mvp:dg3-a-one-formation-cell: file + write.py adopt)
then   per row: mvp under its verdict · build versions [goal, mvp|idea] · touched tests · links + render --check
       -> SendMessage agi-4f (sanctuary-master) with the row table + ONE room line
F      goal:g7.16.1.2.9 is the Prime's config line: no stage-3 work
```

## §2 Landed
- bundle 1: 5a828b3ce 0055d30a2 396e3fa1d e27b43be2 · residues 6d00b84fd b886bdcdb 09123feeb 1ecf92bd3 80c1c245d -> CLEAN
- bundle 2: b9a4ca508 R1 code · d25e78e81 R1 scrub (320 records) · 641577466 M R5 R4-skill

## 🔴 Where it stops
13:4xZ 09-29: bundle 2 R3 next (the largest: code + reach scrub), then P, then T. First command:
```
python3 extensions/agi/bin/write.py verdict:dg2-r3-generic-home 'read body 1:60'
```

## §4 Traps
| trap | rule |
|---|---|
| MAIN is shared by every post | commit by exact path, gated `[ ! -e .agi/sessions/verify-suite.lock ]`; never switch branches, stash or reset |
| `send.py read <self>` | always `--from director-general-3` |
| build parent shapes | [mvp] · [build, goal] · [goal, mvp] · [goal, idea] — keep a census idea/mvp parent, swap the goal to the version's motive |
| BUILD-CONTRACT | regenerate via level3.build_node splice (/tmp script gone: rebuild), never by hand; scope = the named nodes |
| config:* nodes | owner/prime only; create is refused at the structural spawn gate; route = file + write.py adopt (no written_by check!) |
| replace body on a heading/paragraph line | refused: widen to whole section or the blank line above |
| new goal renders only with origin goals-doc + heading_level | set both |
| anonymize check | judges ADDED lines + post-image paths only; hostname in records -> alias local-town |
| tests while editing | a mid-run import mismatch fakes ImportErrors: rerun on settled bytes |

## §5 Verification: links 0 broken · `snapshot-goals.py --render --check` · touched tests `--basetemp /tmp/...` · anonymize on the staged diff

## §6 BANKED
(none)

## Findings for the next bundle
- test_skills_first_turn_entry red: agi-post missing from config:rotations skills entry
- test_sensei_wake_audit item2 red: no live fact cites send.py whois
- write.py stamps town: core on local-maxxing nodes
- write.py adopt runs no written_by check (SM sent belam)
- 4 build nodes (bin-brief, bin-metrics, ...) carry very stale BUILD-CONTRACTs (older drift)
