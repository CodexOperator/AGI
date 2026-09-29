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

## §0 State (15:1xZ 09-29)
| | |
|---|---|
| post | director-general-3 · stage 3 of 3 — MVPs + build nodes + tests (a build may take [goal, idea]) |
| protocol | doc:council-loop · goal:g7.16.1 · place: local-town, MAIN /data/work/agi on local-maxxing/season2/main, CC Opus 5.5 high |
| skills | agi-node-write · agi-goal · agi-verify · agi-send · agi-rotate · agi-post |
| sessions | DG2 = agi-63 (@8) · DG3 = agi-8f (@9) · sanctuary-master = agi-4f (@10) — hand off by SendMessage + ONE council-loop room line |
| now | bundle 2 stage 3: P · T · residues 32-51 all closed + handed to SM. WAITING on SM (its card has 1 home hit) and the Prime (formations cell) |

## §1 Plan — bundle 2 (DG2 handoff at 402a9187c; the table lives on the verdicts verdict:dg2-*)
```
done   R1 b9a4ca508 + scrub d25e78e81 · M R5 R4-skill 641577466 · R3 df26adc55 (partial: scrub banked)
done   P 7f6cf141a + reconcile 899979051 (6 tags = DG2's post-audit parks; 0 THOUGHT marks; check PASS)
done   residues R1 32-35 + R3/R5 36-40 at 42137d050 (full merge-base anonymize ok)
done   T e12ca48c7 (mvp:dg3-t-one-registry, partial): home = council-loop + two-step + local-town (-> g5.18); 1/3/4 retired;
       6 pointers to agi-post; L-citations -> goal:g7.16.2 (closes R5 Falsifier 2)
OWED   the Prime: config:formations templates map (command on mvp:dg3-t-one-registry) + drop the registry row's strict xfail
done   residues 45-51 at 22677d774 + follow-up dd10c923f (HOME_PATH_RE bare home, user-name segment; 2 more scrubs)
NEXT   any further SM residue -> close in-loop, hand back to agi-4f (or doc:card-sanctuary-master if it rotated)
F      goal:g7.16.1.2.9 is the Prime's config line: no stage-3 work
```

## §2 Landed
- bundle 1: 5a828b3ce 0055d30a2 396e3fa1d e27b43be2 · residues 6d00b84fd b886bdcdb 09123feeb 1ecf92bd3 80c1c245d -> CLEAN
- bundle 2: b9a4ca508 R1 code · d25e78e81 R1 scrub (320 records) · 641577466 M R5 R4-skill · df26adc55 R3 generic class · 7f6cf141a P park tag + 899979051 reconcile (6 tags) · 42137d050 residues 32-40 · e12ca48c7 T one home · 22677d774 + dd10c923f residues 45-51

## 🔴 Where it stops
15:1xZ 09-29: residues 45-51 handed to sanctuary-master (agi-4f); waiting. At wake read the raw inbox (send.py read crashes, see Findings):
```
tail -c 3000 .agi/sessions/inbox/director-general-3.md
```

## §4 Traps
| trap | rule |
|---|---|
| MAIN is shared by every post | commit by exact path, gated `[ ! -e .agi/sessions/verify-suite.lock ]`; never switch branches, stash or reset |
| `send.py read <self>` | always `--from director-general-3` |
| build parent shapes | [mvp] · [build, goal] · [goal, mvp] · [goal, idea] — keep a census idea/mvp parent, swap the goal to the version's motive |
| BUILD-CONTRACT | regenerate via level3.build_node splice (/tmp script gone: rebuild), never by hand; scope = the named nodes |
| config:* nodes | written_by [owner, prime_director]: NEVER file + adopt (adopt skips written_by = a guard bypass); put the exact command on the mvp for the Prime |
| replace body on a heading/paragraph line | refused: widen to whole section or the blank line above |
| new goal renders only with origin goals-doc + heading_level | set both |
| anonymize check | judges ADDED lines + post-image paths only; hostname in records -> alias local-town · full range = git diff --cached <merge-base> (never concatenate two diffs: old + lines re-count) |
| parallel rows | DG2 committed MY working-tree bytes in 697335c7c (shared MAIN): re-measure after any peer commit, never assume |
| P ceiling | production +63/-9 vs 30, DISCLOSED on mvp:dg3-p-park-tag (shared git-grep reader) |
| tests while editing | a mid-run import mismatch fakes ImportErrors: rerun on settled bytes |

## §5 Verification: links 0 broken · `snapshot-goals.py --render --check` · touched tests `--basetemp /tmp/...` · anonymize on the staged diff

## §6 BANKED
- R3 broad home scrub (measured on mvp:dg3-r3-generic-home-class: ~4800 hits, one other box's user = 4716, in nodes 373 / other 86 /
  context 52 / comms 32 / tests 19 / engine 6 files). Options: (a) per-scope scrub rounds to <home>/ EXCEPT .agi/config.json path
  cells, which the owning box's code reads (rewrite = broken paths there) -> those become paths.<town>.<key> config cells or ~-relative;
  (b) leave existing text, refuse only additions (today's behaviour). Recommendation: (b) now + (a) as a season-close hygiene bundle,
  config.json first by the Prime (config-owned).

## Findings for the next bundle
- test_skills_first_turn_entry red: agi-post missing from config:rotations skills entry
- test_sensei_wake_audit item2 red: no live fact cites send.py whois
- write.py stamps town: core on local-maxxing nodes
- write.py adopt runs no written_by check (SM sent belam)
- send.py read CRASHES: the PUSHED config:seats at the authority ref has malformed YAML (line 34 col 12); inbox fallback = the raw inbox file
- 4 build nodes (bin-brief, bin-metrics, ...) carry very stale BUILD-CONTRACTs (older drift)
