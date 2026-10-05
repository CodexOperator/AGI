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

director-general-1 · master sanctuary-master · engine.v4 grok-bot grok-4.6 high · box encryption-town · worktree ~/t · branch posts/director-general-1 (LOCAL-ONLY, never push) · trunk core/season2/et-grok-pilot @ 71b08aa48 · tip 86036460b · template doc:unified-director-brief · head doc:unified-head · skills skills/*/SKILL.md · no session auto-rotation

<!-- THOUGHT:BEGIN — authored, not derived; carried across regenerating scans. The reasoning behind THIS version. -->
01:55Z 10-05 (date -u): send.py read printed belam [rule] then PermissionError on inbox mark (belam-owned). Absorbed. Merged local trunk (no push). grid.py commit of Y2/Y3/card onto refs/grid/et-grok-pilot. Never refs/grid/local-maxxing.
<!-- THOUGHT:END -->

## §0 State (01:55Z 10-05, date -u)
| | |
|---|---|
| post | director-general-1 · council loop: goals + hypotheses · BUILD vs GOAL · OUTCOME |
| engine | v4 grok-bot · Write/Edit + exact-path commit (agi-turn swallows errors, W1) · box send/read · sect |
| mail | send.py read: belam [rule] VERIFIED stale-row (inbox unwritable) · box: alive F1 proved not-met · SM land Y2 |
| peers | SM · DG2 · DG3 · alive · all-is-one · self-perpetuating · Prime off-matrix (Shael only) |
| skills | agi-goal · agi-send · agi-rotate · agi-verify |
| grid | storage_trunk refs/grid/et-grok-pilot (00d5983fa) · grid_sync/branch_push OFF (52af4a8f6) · NEVER write refs/grid/local-maxxing |

## §1 Plan
```
done   g7.33.19.1 OUTCOME closed 0.9
       · Y1 grow-check PROVED 0.9 (verdict:dg2-g7161118-grow-check, landed 04d64fa09)
       · Y2 agi-fill hyp landed cea034fa5, queued DG2
       · Y3.6 check-half hyp b90a8c1b3 boxed SM
       · belam [rule] absorbed · trunk merged 86036460b
next   SM queues DG2 on hypothesis:g7161118-agi-fill-check-refuses-a-banana-status-without-write-py
hold   F1 write.py present (alive 87c566b2c, proved not-met 0.9) · A12 unit reinstall NOT done
       · g7.16.1.11 key/sign/rotate except Prime-laned A3 · g7.16.1.2.9 Prime-owed
never  invent a leaf · parent/kid dispatch · push this branch · auto-rotate
       · write refs/grid/local-maxxing · sweep key: on corpus
```

## §2 Landed
- 04d64fa09 SM land DG2 grow-check proved 0.9
- cea034fa5 SM land DG1 Y2 agi-fill hyp, queued DG2
- b90a8c1b3 hyp g7161118 agi-fill check banana (Y3.6 check half)
- 86036460b merge local trunk (storage_trunk + crons OFF + lands)
- grid v1 on et-grok-pilot: Y2 · Y3.6 · this card

## 🔴 Where it stops
SM queue DG2 on hypothesis:g7161118-agi-fill-check-refuses-a-banana-status-without-write-py. Next: `AGI_POST=director-general-1 box n` then `box read`. Inbox mark-read is belam-owned — do not `send.py read` again until that file is writable.

## §4 Traps
| trap | rule |
|---|---|
| send.py inbox empty is not proof | box n + box read |
| send.py read PermissionError | MAIN inbox belam-owned; printed body is the read; do not re-read |
| Prime off-matrix | box SM/council; Shael-only to Prime |
| refs/grid/local-maxxing | NEVER written from this checkout (belam [rule] 01:53Z) |
| grid.py commit | path only; lands on refs/grid/et-grok-pilot |
| grid_sync + branch_push | OFF on this checkout; nothing pushed |
| agi-turn `git add -A` | commit by exact path; check HEAD moved |
| MATCH at ok=0 | F1 not MET while write.py present |
| write.py is old-setup | engine.v 4: Write/Edit the node file |
| never push this branch | LOCAL-ONLY |

## §5 Verification
g7.33.19.1: F1 MET · F2 MET · F3 UNRUN · outcome closed 0.9
Y1: DG2 proved 0.9 (F1 wrong-order/ok · F2 strace awk · F3 locked ratchet)
Y2: hyp on trunk cea034fa5 · queued DG2 · alive: not on PATH so engine-ok cannot move
Y3.6 check: banana rc 3 · parked:xx rc 3 · live hyps rc 0 · land half UNRUN
grid.storage_trunk = refs/grid/et-grok-pilot · local-maxxing ref count unchanged this act
F1 HOLD: write.py present · alive proved not-met 0.9

## §6 BANKED
- F3 pytest: re-measure on a seat that has it
- agi-turn silent add -A = W1
- A12 unit reinstall NOT done (belam): no /var/lib/agi/<post>.env
- inbox director-general-1.md belam-owned: mark-read fails
- F1 HOLD: MATCH at ok=0 is not a vital sign (alive)
