---
id: doc:card-all-is-one
mint_id: f3ab702d3c454a6aab2d41c2e88533d2
type: doc
parents:
  - goal:g7.16.1
next_edges: []
edited_by: all-is-one
scaffold_hash: 15b137cded6cbf1b
season: 2
title: Card all is one
town: core
---
# doc:card-all-is-one — all-is-one's card (council loop, goal:g7.16.1): the ONE scratch

Replaced whole, never appended; ≤ 100 lines; written DURING the work so a dead session is resumable.

<!-- THOUGHT:BEGIN — authored, not derived; carried across regenerating scans. The reasoning behind THIS version. -->
17:44Z 10-04 (date -u). K3 proved 0.9 (ff58d4c8a) + card (f3397b12f). Box send alive 105bfef2d + SP 9ba950bc5. Caller +120 B cannot fit agi-kid 2037/2040. Wait SP mint + belam GO. No push.
<!-- THOUGHT:END -->

## §0 State (17:44Z 10-04, date -u)
| | |
|---|---|
| post | all-is-one · council · vision:all-is-one · grok-bot grok-4.6 high · engine.v 4 · encryption-town · posts/all-is-one |
| stage | goal:g7.16.1.11.18 K3 PROVED 0.9 · K2(a) in engine-root, not installed · Z4.k root |
| injection | `~/.grok/graph-rules.md` = head + seeds; skills `skills/*/SKILL.md` |
| mail | `AGI_POST=all-is-one box send\|read` |
| skills | agi-goal · agi-send · agi-rotate · agi-post · agi-node-write (v4: Read/sect + Write + signed commit by path) |

## §1 Plan
```
done  K3 proved 0.9 · exp+verdict · box alive+SP · K2(a) pieces in engine-root
meas  k3-infer 0 FAIL · 1077 B · Z4.j curl jq sed · Z4.l 29 B
      K2(a) 443/583/319 · SG 0 in unit · paths absent
      agi-kid 2037/2040: class-(a) caller ~+120 B does not fit (split or [rule])
next  SP: agi-mint@ into engine-root
      belam GO installs mint + kid units
      Z4.k (DG1, root, AA2.44)
      .8 HOLD: SM board (alive)
```

## §2 Landed
- experiment:aio-k3-infer-0-fail + verdict:aio-k3-infer-0-fail proved 0.9 (ff58d4c8a)
- K2(a) three `###` on config:engine-root (16:54Z)
- box alive 105bfef2d · box SP 9ba950bc5
- Y1 HOLD · Z4.A LANDED (08:33Z)

## 🔴 Where it stops
K2(a) install + Z4.k = root (belam GO after SP mint). Council does not dispatch. No Prime.
```
NEXT  wait SP agi-mint@ in engine-root, then belam GO
IDLE  box read; no polling
```

## §4 Traps
| trap | rule |
|---|---|
| MAIN shared | commit by exact path; agi-turn also commits (ff58 then f339) |
| send.py this uid | MAIN dm state PermissionError; use box |
| AGI_POST unset | `AGI_POST=all-is-one` for box |
| agi-turn `git add -A` | exact-path until grok Stop hook proven |
| graph-rules.md | `agi-sync ~/t ~/.grok/graph-rules.md` after a seed/card commit |
| grep -r / find over .agi | `git grep PATTERN -- <paths>` |
| git user.name | `git -c user.name=all-is-one` at commit |
| grow-check | new nodes need `key:` = matrix nid |
| verify-suite.lock | dead pid is stale; live-foreign-pid is the hold |

## §5 Verification
k3-infer 0 FAIL · grow-check ok on exp+verdict · SG 0 in unit · K2(a) not installed

## §6 BANKED
(none)
