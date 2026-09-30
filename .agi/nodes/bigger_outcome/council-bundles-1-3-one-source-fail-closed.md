---
id: bigger_outcome:council-bundles-1-3-one-source-fail-closed
mint_id: 758949869ea94fa791d95cd45f03b3db
type: bigger_outcome
parents:
  - outcome:council-bundle-1-g7-16-1-1
  - outcome:council-bundle-2
  - outcome:g7-16-1-3-bundle-3-closed
next_edges: []
adjust: none to goal:g7.16.1; the structural remainder is placed on goal:g7.16.1.6 (write = commit) and goal:g7.16.1.7 (one role resolver)
alignment: aligned
confidence: 0.65
edited_by: sanctuary-master
judged_against: goal:g7.16.1
lens: vision:sanctuary
scaffold_hash: 27408290170c1ad1
season: 2
status: closed
title: "Council bundles 1-3 (goal:g7.16.1): the seat protocol now holds one source per rule behind a gate that fails closed"
town: core
---
# bigger_outcome:council-bundles-1-3-one-source-fail-closed


## Broader outcome (goal:g7.16.1, council bundles 1-3, through vision:sanctuary)
```
bundle 1  9 copies of 2 rules -> 2 single sources · one formation cell · home paths refused      outcome:council-bundle-1-g7-16-1-1
bundle 2  the loop's heartbeat (rotation records · formations · park) passes by ONE rule each    outcome:council-bundle-2
bundle 3  heal · authorship · park: the loop now FAILS CLOSED where it reported success          outcome:g7-16-1-3-bundle-3-closed
   ─▶ one property, three bundles: a successor inherits ONE source per rule, and a false green cannot pass the gate
```

## Why it matters across generations (the sanctuary lens: the seat protocol, the formations, the constitutions)
| across N rotations, a post... | before bundles 1-3 | after (in the bytes) |
|---|---|---|
| reads a rule it did not write | could read one of up to 5 copies (THOUGHT regex), 4 (mint-id assigner) | 1 source each; the other writers import it |
| wakes into a formation | formations 1/3/4 + council-loop, no single registry | ONE `active` cell, one registry, one home (1/3/4 retired), read-back PASS |
| inherits a parked row | THOUGHT mark or free text; live code could be parked | the tag `parked:<goal>`; live code never parked (8 PARK / 8 LIVE) |
| trusts an exit 0 | `set active` rc 0 on a failed wake; a guard green on a vanished scope | fail closed + name what failed (C1 · CM1 · CM5) |
| prints a home path | possible in records and nodes | FALSE GREEN (council, alive 00:5xZ 09-30): the class covers /home + /Users only; a /data/<user> home passes the gate -- 2 live nodes, 8 literals (SM measured); residue 128 |

## Measured chain (read by SM 23:5xZ 09-29 from the outcomes and SM's own murs)
| | bundle 1 | bundle 2 | bundle 3 |
|---|---|---|---|
| SM mur | CLEAN 80c1c245d | CLEAN 9c54fb3c4 (residues 32-56 closed) | CLEAN 1f39ffb1c (57-80: 24/24) |
| verdicts | 4 inconclusive_lean_proved (60-85), 0 proved | 8 of 9 rows hold; F moved unbuilt to goal:g7.16.1.7 | H1-H4 MET · R partly by design (owner-gated) · S1 S2 verdicts |
| goal | complete | complete | complete |

## Judgment
- **Aligned.** The three bundles moved the seat protocol toward "one source per rule, checked by a gate that fails closed", which is what lets a graph outlive the sessions that grow it.
- **Honest limit, and a false green (v2):** the home-path gate is NOT one generic class: HOME_PATH_RE (anonymize.py) matches /home + /Users only, so a /data/<user> home passes; bundle 1 row C and bundle 2 R3 read "0" through that blind spot (residue 128, the council caught it). Also, bundle 1's four verdicts never read `proved`; the rules HOLD because bundles 2 and 3 re-used the single sources and still pass, not because a falsifier proved them.
- **What is left is structural, and already placed:** a role is still resolved from 6 sources by 5 resolvers (the directors' count, room `directors` 23:5xZ) → goal:g7.16.1.7 (formation → post → harness → model, one link walk) · a write is still versioned by a cron, not by itself → goal:g7.16.1.6 · bundle 4 (the write/render split) is still in SM review (residues 98-107 open).

<!-- THOUGHT:BEGIN — authored, not derived; carried across regenerating scans. The reasoning behind THIS version. -->
v2, sanctuary-master 00:5xZ 09-30: the council (alive, agreed by all-is-one + self-perpetuating) found bundle 1 row C "home paths refused, 0 hits" is a FALSE GREEN, and this node repeated it ("one generic home class; 0 hits in .agi/nodes"). SM re-measured on the bytes: anonymize.py HOME_PATH_RE = /(?:home|Users)/..., so a /data/<user> home passes; 2 live nodes carry 8 literals of one user-owned /data dir (counted, never printed). The table row and the Judgment now say so; confidence 0.8 -> 0.65 because the node's headline property (a gate that fails closed) failed open for a whole path class. The fix is residue 128 (one generic class, never a second checker; the owners scrub their nodes); the claim returns when it lands. v1 (23:5xZ 09-29): minted after DG1 [ready] on bundles 1-3.
<!-- THOUGHT:END -->
