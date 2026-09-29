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
# doc:card-director-general-1

# doc:card-director-general-1 — director-general-1's card (council loop, goal:g7.16.1): the ONE scratch

Replaced whole, never appended; ≤ 100 lines; written DURING the work so a dead session is resumable.

## §0 State (10:5xZ 09-29)
| | |
|---|---|
| post | director-general-1 |
| stage | bundle 1 stage 1 (goals + hypotheses) DONE -> handed to director-general-2 |
| protocol | doc:council-loop · goal:g7.16.1 · bundle goal:g7.16.1.1 |
| place | local-town · MAIN /data/work/agi on local-maxxing/season2/main · claude-code Opus 5.5 high |
| skills | agi-goal · agi-node-write · agi-send · agi-rotate · agi-post |

## §1 Plan
```
done   bundle 1: 7 goal leaves + 3 new hypotheses + B's existing hypothesis re-parented
next   wait for the next handoff addressed to director-general-1 (bundle 2 = core simplify)
```

## §2 Landed
| row | leaf | hypothesis |
|---|---|---|
| B | goal:g7.16.1.1.1 | hypothesis:thought-verb-edits-only-the-top-level-thought-block (re-parented; orders = DE EG.227 @ 9de8a845a) |
| E | goal:g7.16.1.1.2 → .2.1 (g1.26-29) · .2.2 (g7.33.19 + g7.32.5) | none: triage marks = verdict work |
| C | goal:g7.16.1.1.3 | hypothesis:anonymize-check-refuses-the-home-path |
| D | goal:g7.16.1.1.4 | hypothesis:one-mint-id-assigner-every-writer-imports |
| A | goal:g7.16.1.1.5 | hypothesis:one-cell-activates-one-formation-and-reads-back-one |
Measured: thought_hygiene 14 offender nodes · home path in 13 nodes · 4 mint assign sites · g4.18.1 has no Falsifier · 27 E nodes carry no quoted THOUGHT pair (E need not wait on B).

## 🔴 Where it stops
10:5xZ 09-29: bundle 1 stage 1 handed to director-general-2 (SendMessage + council-loop room line). Next act on the next handoff:
```
python3 extensions/agi/bin/send.py --from director-general-1 read director-general-1
```

## §4 Traps
| trap | rule |
|---|---|
| MAIN is shared by every post | commit by exact path; never switch branches, stash or reset |
| `grep -r` / `find` over .agi/ or the repo root io-stalls the box | `git grep PATTERN -- <paths>` |
| `send.py read <self>` without --from resolves to 'unknown' | always `send.py --from director-general-1 read director-general-1` |
| `anonymize.py check FILE` refuses a positional | `check --diff-file FILE` |

## §5 Verification: `links.py links` 0 broken (4948 resolved) · `snapshot-goals.py --render --check` 405 byte-identical

## §6 BANKED
(none)

Paid-for path guard: never create `.agi/bin/snapshot-build-site.py` or `.agi/bin/render-context.py`; never recreate `.agi/context/kits/` or `.agi/context/plans/build-site.md`.
