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

## §0 State (18:5xZ 09-29) — RECOVERED seat (gen 3, agi-b1, @8); owner: "Keep working till 7pm" → runs until 23:00Z, then the same stop
| | |
|---|---|
| post | director-general-3 · stage 3 of 3 — MVPs + build nodes + tests (a build may take [goal, idea]) |
| protocol | doc:council-loop · goal:g7.16.1 · place: local-town, MAIN /data/work/agi on local-maxxing/season2/main, CC Opus 5.5 high |
| skills | agi-node-write · agi-goal · agi-verify · agi-send · agi-rotate · agi-post |
| sessions | DG3 = agi-b1 · DG2 = agi-40 (handoff 18:2xZ) · others: `send.py whois <post>` — hand off by SendMessage + ONE council-loop room line |
| now | bundle 3 = goal:g7.16.1.3 + goal:g6.41.1 (DG2 handoff at e019d63b0; verdicts verdict:dg2-h*/r*/s*). H rows BUILT; R1/R2 next; then mvps + build nodes, then -> sanctuary-master |

## §1 Plan — bundle 3 (the table lives on the verdicts)
```
done   H3 + H4 f + H4 p1 bb153e89d (rotation_record.py: dump/resolve/grep_live/parked_carriers; grep fails closed; 5 carrier tags)
done   H4 g 482da3853 · H1 e370bb4d6 (goal:g4.18.3) · H2 2c412e5bb (goal:g4.18.4: insert after last row, lone-row refusal, one load gate x4)
done   H4 b a981ae47f da8b2cfbc 92f6f4883 fb57864a5 551908e4b 7baafa62b 0e3102a67 17f91868b (415 -> 0; grid 330 versions, 0 demoted)
NEXT   R1 (verdict:dg2-r1-per-post-scope, test_rotate.py 5x) · R2 (verdict:dg2-r2-psi-admission, test_heal_watch.py 4x): code + dummies ONLY;
       the LIVE cutover is the owner's word after PASS B3 (doc:card-belam §6) — never run it here
then   mvps (one per row, parent the dg2 verdict) + build:bin-rotation-record ([mvp] shape) + grid commit; room line + SendMessage -> SM
n/a    S1 / S2 = verdicts (proved), nothing to build · G landed by alive (30f4db55f, e662637ac)
open   H4 (a)(c)(d)(e) + g7.32.5 status: not in DG2's table -> check whether DG1/DG2 closed them before the handoff to SM
```

## §2 Landed
- bundle 1 + 2: see grid history of this card (bundle 2 CLOSED, SM mur clean 15:39Z)
- bundle 3: bb153e89d · 482da3853 · e370bb4d6 · 2c412e5bb · H4 b x8 (above)

## 🔴 Where it stops
18:5xZ 09-29: H rows built + pushed. Next command: read verdict:dg2-r1-per-post-scope, then the 5 xfails in test_rotate.py.
PASS B3 runs on this box: run ONE test file at a time. First command at wake:
```
python3 extensions/agi/bin/send.py --from director-general-3 read director-general-3
```

## §4 Traps
| trap | rule |
|---|---|
| MAIN is shared by every post | commit by exact path, gated `[ ! -e .agi/sessions/verify-suite.lock ]`; never switch branches, stash or reset; a dirty foreign file: scrub HEAD into the index, keep its edit |
| `send.py read <self>` | always `--from director-general-3` |
| build parent shapes | [mvp] · [build, goal] · [goal, mvp] · [goal, idea] |
| BUILD-CONTRACT | regenerated via level3, never by hand |
| config:* nodes | written_by [owner, prime_director]: adopt NOW runs the gate too (H1) — put the exact command on the mvp for the Prime |
| replace body on a heading/paragraph line | refused: widen to whole section or the blank line above |
| anonymize check | judges ADDED lines: a touched line's hostname -> alias local-town |
| sub! on frontmatter | re-validates the field: a legacy wrong shape refuses (probes str -> list fixed on 2 experiments) |
| tests while editing | a mid-run import mismatch fakes ImportErrors: rerun on settled bytes |

## §5 Verification: links 0 broken · touched tests one file at a time `--basetemp /tmp/...` · anonymize on the staged diff · live check_formation PASS

## §6 BANKED
- (none open for this post)

## Findings for the next bundle
- test_sensei_wake_audit item2 red (pre-existing): no live fact cites send.py whois
- test_skills_first_turn_entry red: agi-post missing from config:rotations skills entry
- write.py stamps town: core on local-maxxing nodes
- 4 build nodes (bin-brief, bin-metrics, ...) carry very stale BUILD-CONTRACTs
