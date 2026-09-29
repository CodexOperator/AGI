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

## §0 State (19:1xZ 09-29) — RECOVERED seat (gen 3, agi-b1, @8); owner: "Keep working till 7pm" → runs until 23:00Z, then the same stop
| | |
|---|---|
| post | director-general-3 · stage 3 of 3 — MVPs + build nodes + tests (a build may take [goal, idea]) |
| protocol | doc:council-loop · goal:g7.16.1 · place: local-town, MAIN /data/work/agi on local-maxxing/season2/main, CC Opus 5.5 high |
| skills | agi-node-write · agi-goal · agi-verify · agi-send · agi-rotate · agi-post |
| sessions | DG3 = agi-b1 · DG2 = agi-40 · sanctuary-master = agi-b8 (@4) · alive = agi-13 — hand off by SendMessage + ONE council-loop room line |
| now | stage 3 DONE 6211ebb40 · run A 57-63 CLOSED d4e1f7c62 · run B 64-67 CLOSED 823da7e8e · waiting on run C (R1/R2/S1+S2 + re-mur 57-63) and the 64-67 re-mur |

## §1 Plan — bundle 3 (goal:g7.16.1.3 + goal:g6.41.1; the table lives on mvp:dg3-h*/r*)
```
done   H3 + H4 f + H4 p1 bb153e89d · H4 g 482da3853 · H1 e370bb4d6 (g4.18.3 COMPLETE) · H2 2c412e5bb (g4.18.4 stays active: F2 history)
done   H4 b 415 -> 0 in 8 rounds (a981ae47f .. 17f91868b) · H4 (a)(c)(d)(e) + g7.32.5 active 7d928ffe4
done   R1 63898e64f (P1 ensure live; P6 scope behind spawn.post_scope live:false) · R2 429b86530 (PSI gate, 1/pass, Prime first)
done   9 mvps + build:bin-rotation-record + grid 6211ebb40
done   SM run A (wf_a3b15e54-c65) residues 57-63 at d4e1f7c62
done   SM run B (wf_9dd69ca3-b96) residues 64-67 at 823da7e8e
NEXT   SM residues -> close in-loop, hand back to agi-b8
n/a    S1 / S2 verdicts (nothing to build) · G landed by alive
```

## §2 Landed
- bundle 1 + 2: grid history of this card (bundle 2 CLOSED, SM mur clean 15:39Z)
- bundle 3: bb153e89d 482da3853 e370bb4d6 2c412e5bb a981ae47f da8b2cfbc 92f6f4883 fb57864a5 551908e4b 7baafa62b 0e3102a67 17f91868b 63898e64f 429b86530 7d928ffe4 6211ebb40

## 🔴 Where it stops
19:4xZ 09-29: runs A + B residues closed (d4e1f7c62, 823da7e8e); waiting on agi-b8's run C (wf_67ad5686-154) and the re-murs. PASS B3 on this box: ONE test file at a time. First command at wake:
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
- R1 slice (owner / council): agi.slice shares MemoryHigh 9.26G / MemoryMax 10.29G with agi-work + agi-engine; the remote-control
  service holds 8.4G of posts. Options: (a) a dedicated uncapped posts slice (no '-' in its name), (b) raise agi.slice, (c) agi.slice
  as is. Recommend (a), then flip `spawn.post_scope.live` (the one edit) after PASS B3 with the owner present.
- goal:g4.18.4 Falsifier 2 scans all history (pre-fix e4aaef794 = 1 forever): scope it to commits after 2c412e5bb, then complete it.

## Findings for the next bundle
- test_sensei_wake_audit item2 red (pre-existing): no live fact cites send.py whois
- test_skills_first_turn_entry red: agi-post missing from config:rotations skills entry
- write.py stamps town: core on local-maxxing nodes
- 4 build nodes (bin-brief, bin-metrics, ...) carry very stale BUILD-CONTRACTs
- memory_alarm.py has no build node
- H4g: own-HOME -> ~ on the composer path unpinned; a Path arg bypasses home_rel (latent) · rotate ~3237 handoff path raw in the alert
- tests that call heal._watch_seats unstubbed read the box's live PSI (flaky under pressure > 40)
