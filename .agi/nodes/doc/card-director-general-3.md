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

## §0 State (21:4xZ 09-29) — gen 4 seat (agi-b1); owner: "Keep working till 7pm" → stop 23:00Z
| | |
|---|---|
| post | director-general-3 · stage 3 of 3 — MVPs + build nodes + tests (a build may take [goal, idea]) |
| protocol | doc:council-loop · goal:g7.16.1 · place: local-town, MAIN /data/work/agi on local-maxxing/season2/main, CC Opus 5.5 high |
| skills | agi-node-write · agi-goal · agi-verify · agi-send · agi-rotate · agi-post |
| sessions | DG3 = agi-b1 · DG2 = agi-40 · DG1 = agi-77 · sanctuary-master = agi-b8 · alive = agi-13 · belam = agi-f0 — hand off by SendMessage + ONE council-loop room line |
| now | bundle 3 CLOSED (SM re-confirmed at 1f39ffb1c). Bundle 4 HOLD lifted 21:1xZ, base 1f39ffb1c: W-G.1 + W0 landed, sent to SM for review; building W-G.2 |

## §1 Plan — bundle 3 (goal:g7.16.1.3 + goal:g6.41.1) → bundle 4 (goal:g7.16.1.4)
```
done   bundle 3 build + SM residues 57-79 (grid history of this card)
done   council chunk 2 CM1-CM4 528115210 · chunk 1 CM5 CM6 CM8 cfe5a6aca
done   CM7 3f5b2f455: check_formation ROW rule reads every live node; MARK rule stays goal/hypothesis (+2 test rows, doc node)
done   CM9 e2ae6d5a5: --successor-argv stand-in wrapped by mem_cap.scope_argv(bash -c, post_scope slice, _post_unit(seat)); cell off = verbatim
done   CM10 e2ae6d5a5: hypothesis:row-parks-carry-a-carrier-tag 39 -> 38 rows (7d928ffe4 moved pass10 row 6 parked -> keep), THOUGHT
done   + e2ae6d5a5: rotation_record.py added to test_bin_help_smoke NO_HELP (bundle 3 H4 library; was red)
done   SendMessage agi-13 + agi-b8 + council-loop room line (21:2xZ)
done   residue 80 1f39ffb1c (autopsy test asserts the CM4 home-relative line) -> bundle 3 CLOSED
done   W-G.1 41107692f + mvp 0a58fe968 + build:GOALS.md retired e6bbc6527: all 6 callers + gate + readers + git rm GOALS.md, smoke exit 0
done   W0 82fce8a34: goal:g4.19 retitled (Read -> render path); sent to agi-b8 for review 21:4xZ; leaf falsifier self-match -> DG1
NOW    W-G.2 (goal:g7.16.1.4.1, dead code): snapshot-goals --from-doc + unlink + cmd_render/--render/--check; locations DEFAULT_GOALS_FILE +
       goals_path + goals_file cell + readers (locations :1186, verify_unified :340, unify comments); test_snapshot_goals render/from-doc rows;
       flips test_wg_from_doc_and_goals_file_retire. snapshot-goals.py STAYS (write_frontmatter imported by level3, build-site, backfill, decompose, post_wire)
then   W1 (.5.1-.3) -> W2a (.6.1) -> W2b/c/e -> W3a/b -> W3c-1 additive before W3c-2 atomic cut (SM checks: never two read paths taught)
NEVER  hypothesis:a-write-refuses-a-missing-outbound-id-by-lookup · hypothesis:every-link-reader-resolves-mint-ids (superseded, 68d4c8504) ·
       goal:g4.18.6.4.1 + the W2d migration (HELD on belam's mint-id [decision], d4a186957)
DG1 re-scope 2 (d4a186957): g4.18.6.3.1 PARENTS ONLY post-pass at loader.py:210-230, resolver passed in · g4.18.6.3.2 owns every next_edges reader ·
       g4.18.6.4.2 = 10 writers (ceiling 50) · g4.18.7.3 ceiling 125, one row. DG2 table (703b4c07b, b8d667880): verdict:dg2b4-w2b1/w2b2/w2cA2/w2cB/w2cC/w2d2/w3cR2
       Order hint: W1a before W3a, W2a before W3a; W1b commits in main() never submit(); W3 B3 moves GrepError too.
```

## §2 Landed
- bundle 1 + 2: grid history of this card (bundle 2 CLOSED 15:39Z)
- bundle 3: bb153e89d 482da3853 e370bb4d6 2c412e5bb a981ae47f da8b2cfbc 92f6f4883 fb57864a5 551908e4b 7baafa62b 0e3102a67 17f91868b
  63898e64f 429b86530 7d928ffe4 6211ebb40 d4e1f7c62 823da7e8e 0d33b10f4 4453af4d7 07ee9c46b 66da33b01 a1eabdebf 528115210 cfe5a6aca
  3f5b2f455 e2ae6d5a5 1f39ffb1c
- bundle 4: 41107692f 0a58fe968 e6bbc6527 82fce8a34

## 🔴 Where it stops
Building bundle 4 W-G.2 (plan NOW row); W-G.1 + W0 await SM's review. Stop 23:00Z. PASS B3 on this box: ONE test file at a time.
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
| pkill -f / pgrep -f <pattern> | match their own shell line: exit 144 kills the rest of the command; find by ppid chain instead |
| pytest takes verify-suite.lock | conftest holds it for EVERY session, even one file: never two pytest at once (a 2nd one ERRORs 'LIVE runner') |
| derive-commands --all | appends the retired command table to CLAUDE.md (tables lag command:commands): edit the derived row by hand |
| build parent shapes | [mvp] · [build, goal] · [goal, mvp] · [goal, idea] |
| BUILD-CONTRACT | regenerated via level3, never by hand |
| config:* nodes | written_by [owner, prime_director]: put the exact command on the mvp for the Prime |
| replace body on a heading/paragraph line | refused: widen to whole section or the blank line above |
| anonymize check | judges ADDED lines: a touched line's hostname -> alias local-town |
| tests while editing | a mid-run import mismatch fakes ImportErrors: rerun on settled bytes |

## §5 Verification (21:4xZ): links 5156/0 · smoke exit 0 node_count 5189 · W-G files one at a time green (mvp:dg3b4-wg1 lists them)

## §6 BANKED
- R1 slice (owner / council): agi.slice shares MemoryHigh 9.26G / MemoryMax 10.29G with agi-work + agi-engine; the remote-control
  service holds 8.4G of posts. Options: (a) a dedicated uncapped posts slice (no '-' in its name), (b) raise agi.slice, (c) as is.
  Recommend (a), then flip `spawn.post_scope.live` (the one edit) after PASS B3 with the owner present.
- goal:g4.18.4 Falsifier 2 scans all history (pre-fix e4aaef794 = 1 forever): scope it to commits after 2c412e5bb, then complete it.

## Findings for the next bundle
- goal:g7.16.1.3.1 title still says 39 parked rows (alive's copy; told agi-13)
- derived command tables (QUICKSTART, skills/agi, CLAUDE.md) lag command:commands; derive-commands --all re-grows CLAUDE.md
- .agi/nodes/.geometry/commands.md.bak is TRACKED (09-18) and carries id command:commands too
- test_workflow's leak detector flags --basetemp /tmp dirs as the real sessions dir (1 teardown error)
- goal:g7.16.1.4.2 falsifier 2 matches its own title (told DG1)
- test_sensei_wake_audit item2 red (pre-existing): no live fact cites send.py whois
- test_skills_first_turn_entry red: agi-post missing from config:rotations skills entry
- write.py stamps town: core on local-maxxing nodes · 4 build nodes carry very stale BUILD-CONTRACTs · memory_alarm.py has no build node
- R1 latent: unit names unique per second only (same-second rotate + recover collide once the switch is ON) · R2 Prime-first sorts on the MAIN row
- H4g: own-HOME -> ~ on the composer path unpinned; a Path arg bypasses home_rel (latent) · rotate ~3237 handoff path raw in the alert
- tests that call heal._watch_seats unstubbed read the box's live PSI (flaky under pressure > 40)

Paid-for path guard: never create `.agi/bin/snapshot-build-site.py` or `.agi/bin/render-context.py`; never recreate `.agi/context/kits/` or `.agi/context/plans/build-site.md`.
