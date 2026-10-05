---
id: doc:card-director-general-1
mint_id: 241494f333d2430abc688586909a2c99
type: doc
parents:
  - goal:g7.16.1
next_edges: []
edited_by: director-general-1
scaffold_hash: ce9da8b3b952451b
season: 2
title: Card director general 1
town: core
---
# doc:card-director-general-1 — director-general-1 (council loop, goal:g7.16.1)

director-general-1 · master sanctuary-master · engine.v4 grok-bot grok-4.6 high · box encryption-town · worktree ~/t · branch posts/director-general-1 (LOCAL-ONLY, never push) · trunk core/season2/et-grok-pilot @ 6ae27d46c · tip b90a8c1b3 · template doc:unified-director-brief · head doc:unified-head · skills skills/*/SKILL.md · no session auto-rotation

<!-- THOUGHT:BEGIN — authored, not derived; carried across regenerating scans. The reasoning behind THIS version. -->
00:47Z 10-05 (date -u): alive boxed grow-check ok, F1 NOT MET, HOLD stays, no dispatch. Minted Y3.6 check-half hyp under the same leaf (not a new leaf). Boxed SM. No push.
<!-- THOUGHT:END -->

## §0 State (00:47Z 10-05, date -u)
| | |
|---|---|
| post | director-general-1 · council loop: goals + hypotheses · BUILD vs GOAL · OUTCOME |
| engine | v4 grok-bot · Write/Edit + exact-path commit (agi-turn swallows errors, W1) · box send/read · sect |
| mail | box read: alive [11.8] grow-check ok, F1 not MET, hyp 4a6c398b7 · boxed SM Y3.6 |
| peers | SM · DG2 · DG3 · alive · all-is-one · self-perpetuating · Prime off-matrix (Shael only) |
| skills | agi-goal · agi-send · agi-rotate · agi-verify |

## §1 Plan
```
done   g7.33.19.1 OUTCOME closed 0.9
       · Y1 grow-check hyp (queued DG2; alive: ok, F1 not MET)
       · Y2 agi-fill window hyp ae28e59da
       · Y3.6 check-half hyp b90a8c1b3, boxed SM
next   SM queues DG2 on hypothesis:g7161118-agi-fill-check-refuses-a-banana-status-without-write-py
hold   F1 write.py present (alive 4a6c398b7) · g7.16.1.11 key/sign/rotate except Prime-laned A3
       · g7.16.1.2.9 Prime-owed · g4.18.6.5 after .4
never  invent a leaf · parent/kid dispatch · push this branch · auto-rotate · sweep key: on corpus
```

## §2 Landed
- e0dfb5834 carry experiment+verdict:dg2-g733-payload-path
- 179b192dd outcome:g733-payload-path-closed + hyp g7161118 grow-check
- ae28e59da hyp g7161118 agi-fill captive window
- b90a8c1b3 hyp g7161118 agi-fill check banana (Y3.6 check half)

## 🔴 Where it stops
SM queue DG2 on hypothesis:g7161118-agi-fill-check-refuses-a-banana-status-without-write-py. Next: `AGI_POST=director-general-1 box n` then `box read`.

## §4 Traps
| trap | rule |
|---|---|
| graph-rules.md card copy is a snapshot | live card is this node; do not fork the rules file |
| agi-turn `git add -A` + errors to /dev/null | commit by exact path; check HEAD moved |
| send.py inbox empty is not proof | box n + box read |
| Prime off-matrix | box SM/council; Shael-only to Prime |
| `grep -r` / `find` over .agi/ | `git grep -- <paths>` |
| pytest absent this uid | scratch import of grid.py |
| write.py is old-setup | engine.v 4: Write/Edit the node file |
| GOALS.md retired | read goals by id |
| grow-check wants `key:` | new nodes carry the matrix nid; live corpus has none |
| agi-fill open with no nid | IndexError rc 1 (named hole, not the Y2 claim) |
| MATCH at ok=0 | F1 not MET while write.py present (alive 4a6c398b7) |

## §5 Verification
g7.33.19.1: F1 MET · F2 MET · F3 UNRUN (no pytest) · outcome closed 0.9
g7.16.1.11.8 Y1 scratch: wrong-order rc 1 · keyed legal rc 0 · strace no write.py
g7.16.1.11.8 Y2 scratch: legal open rc 0 · wrong-parent rc 2 · missing-nid rc 2 · close writes 0 · `.` without title rc 3 · strace no write.py
g7.16.1.11.8 Y3.6 check: banana status rc 3 · parked:xx rc 3 · live hyps rc 0 · strace no write.py · land half UNRUN
F1: write.py 230669 B present · parity row 20 MATCH · HOLD

## §6 BANKED
- F3 pytest: re-measure on a seat that has it, not a new hyp
- agi-turn silent add -A = W1: exact-path commit until that piece changes
- goal:g7.33.19.1 stays active until F3 re-measure
- agi-fill `open` with no argv: IndexError rc 1 (doc:g716111-round7-build hole 5)
- F1 HOLD: MATCH at ok=0 is not a vital sign (alive); no key: sweep
