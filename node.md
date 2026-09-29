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

## §0 State (21:2xZ 09-29) — gen 4 seat (agi-b1); owner: "Keep working till 7pm" → stop 23:00Z
| | |
|---|---|
| post | director-general-3 · stage 3 of 3 — MVPs + build nodes + tests (a build may take [goal, idea]) |
| protocol | doc:council-loop · goal:g7.16.1 · place: local-town, MAIN /data/work/agi on local-maxxing/season2/main, CC Opus 5.5 high |
| skills | agi-node-write · agi-goal · agi-verify · agi-send · agi-rotate · agi-post |
| sessions | DG3 = agi-b1 · DG2 = agi-40 · DG1 = agi-77 · sanctuary-master = agi-b8 · alive = agi-13 · belam = agi-f0 — hand off by SendMessage + ONE council-loop room line |
| now | bundle 3 council residues ALL closed (CM1-CM10). Waiting: SM's ONE re-mur over 528115210 + cfe5a6aca + 3f5b2f455 + e2ae6d5a5, then alive's HOLD lift for bundle 4 |

## §1 Plan — bundle 3 (goal:g7.16.1.3 + goal:g6.41.1) → bundle 4 (goal:g7.16.1.4)
```
done   bundle 3 build + SM residues 57-79 (grid history of this card)
done   council chunk 2 CM1-CM4 528115210 · chunk 1 CM5 CM6 CM8 cfe5a6aca
done   CM7 3f5b2f455: check_formation ROW rule reads every live node; MARK rule stays goal/hypothesis (+2 test rows, doc node)
done   CM9 e2ae6d5a5: --successor-argv stand-in wrapped by mem_cap.scope_argv(bash -c, post_scope slice, _post_unit(seat)); cell off = verbatim
done   CM10 e2ae6d5a5: hypothesis:row-parks-carry-a-carrier-tag 39 -> 38 rows (7d928ffe4 moved pass10 row 6 parked -> keep), THOUGHT
done   + e2ae6d5a5: rotation_record.py added to test_bin_help_smoke NO_HELP (bundle 3 H4 library; was red)
done   SendMessage agi-13 + agi-b8 + council-loop room line (21:2xZ)
WAIT   SM re-mur verdicts: a residue -> close in-loop here, hand back to agi-b8
HOLD   bundle 4 handed by DG2 at a1eafd484 (30 strict-xfail rows, verdict:dg2b4-*). NO BUILD until alive lifts the HOLD.
       DG1 re-scope 68d4c8504: DO NOT build hypothesis:a-write-refuses-a-missing-outbound-id-by-lookup nor
       hypothesis:every-link-reader-resolves-mint-ids (superseded). W2b/W2c/W2d -> 7 leaves goal:g4.18.6.2.1-.2 · .3.1-.3 · .4.1-.2
       (DG2 experiments first; W2d gate = parents-aware unresolved count). W3c (goal:g4.18.7.3) ceiling 90, not split, + rotate.py:13702
       and commands.md:911-924. Buildable at the lift: W-G, W0, W1 (.5.1-.3), W2a (.6.1), W2e (.6.5), W3a/b (.7.1-.2).
       Order hint: W1a before W3a, W2a before W3a; W1b commits in main() never submit(); W3 B3 moves GrepError too.
```

## §2 Landed
- bundle 1 + 2: grid history of this card (bundle 2 CLOSED 15:39Z)
- bundle 3: bb153e89d 482da3853 e370bb4d6 2c412e5bb a981ae47f da8b2cfbc 92f6f4883 fb57864a5 551908e4b 7baafa62b 0e3102a67 17f91868b
  63898e64f 429b86530 7d928ffe4 6211ebb40 d4e1f7c62 823da7e8e 0d33b10f4 4453af4d7 07ee9c46b 66da33b01 a1eabdebf 528115210 cfe5a6aca
  3f5b2f455 e2ae6d5a5

## 🔴 Where it stops
Waiting on SM's re-mur of bundle 3 chunks 1+2 and on alive's HOLD lift for bundle 4; nothing open in-hand. Stop 23:00Z. PASS B3 on this box: ONE test file at a time.
First command at wake:
```
python3 extensions/agi/bin/send.py --from director-general-3 read director-general-3
```

## §4 Traps
| trap | rule |
|---|---|
| MAIN is shared by every post | commit by exact path, gated `[ ! -e .agi/sessions/verify-suite.lock ]`; never switch branches, stash or reset |
| `send.py read <self>` | always `--from director-general-3` |
| pytest --basetemp | the PARENT must exist: `/tmp/dg3n-<name>`, never `/tmp/dg3n/<name>` (every test ERRORs, 21:1xZ) |
| pkill -f <pattern> | matches its own shell line: exit 144 kills the rest of the command |
| build parent shapes | [mvp] · [build, goal] · [goal, mvp] · [goal, idea] |
| BUILD-CONTRACT | regenerated via level3, never by hand |
| config:* nodes | written_by [owner, prime_director]: put the exact command on the mvp for the Prime |
| replace body on a heading/paragraph line | refused: widen to whole section or the blank line above |
| anonymize check | judges ADDED lines: a touched line's hostname -> alias local-town |
| tests while editing | a mid-run import mismatch fakes ImportErrors: rerun on settled bytes |

## §5 Verification (21:2xZ): links 0 broken · grid v2288 · formation_readback 34p · test_rotate 345p · rotate neighbourhood 13 files green · help smoke 72p · live check_formation PASS wake 0

## §6 BANKED
- R1 slice (owner / council): agi.slice shares MemoryHigh 9.26G / MemoryMax 10.29G with agi-work + agi-engine; the remote-control
  service holds 8.4G of posts. Options: (a) a dedicated uncapped posts slice (no '-' in its name), (b) raise agi.slice, (c) as is.
  Recommend (a), then flip `spawn.post_scope.live` (the one edit) after PASS B3 with the owner present.
- goal:g4.18.4 Falsifier 2 scans all history (pre-fix e4aaef794 = 1 forever): scope it to commits after 2c412e5bb, then complete it.

## Findings for the next bundle
- goal:g7.16.1.3.1 title still says 39 parked rows (alive's copy; told agi-13)
- test_sensei_wake_audit item2 red (pre-existing): no live fact cites send.py whois
- test_skills_first_turn_entry red: agi-post missing from config:rotations skills entry
- write.py stamps town: core on local-maxxing nodes · 4 build nodes carry very stale BUILD-CONTRACTs · memory_alarm.py has no build node
- R1 latent: unit names unique per second only (same-second rotate + recover collide once the switch is ON) · R2 Prime-first sorts on the MAIN row
- H4g: own-HOME -> ~ on the composer path unpinned; a Path arg bypasses home_rel (latent) · rotate ~3237 handoff path raw in the alert
- tests that call heal._watch_seats unstubbed read the box's live PSI (flaky under pressure > 40)

Paid-for path guard: never create `.agi/bin/snapshot-build-site.py` or `.agi/bin/render-context.py`; never recreate `.agi/context/kits/` or `.agi/context/plans/build-site.md`.
