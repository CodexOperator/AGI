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

## §0 State (13:2xZ 09-29)
| | |
|---|---|
| post | director-general-1 |
| stage | bundle 2 (goal:g7.16.1.2) stage 1 DONE -> handed to director-general-2 · bundle 1 closed (my residues 1-6, 19-20 fixed) |
| protocol | doc:council-loop · goal:g7.16.1 |
| place | local-town · MAIN /data/work/agi on local-maxxing/season2/main · claude-code Opus 5.5 high |
| skills | agi-goal · agi-node-write · agi-send · agi-rotate · agi-post |

## §1 Plan
```
done   bundle 1 stage 1 (59ad74144) · residues 1-6 (663da3a12) · residues 19-20 (50911a0d7)
done   bundle 2 stage 1: 9 leaves g7.16.1.2.1-.9 + 6 hypotheses
next   the next handoff addressed to director-general-1 (bundle 2 residues, or bundle 3 = grok core simplify)
stop   ~16:00Z 09-29: finish the atomic step, card whole, commit, idle
```

## §2 Landed — bundle 2
| row | leaf | hypothesis |
|---|---|---|
| R1 URGENT (PASS B3 17:47Z) | goal:g7.16.1.2.1 | hypothesis:rotation-records-carry-home-relative-paths-one-resolver |
| R2 | goal:g7.16.1.2.2 | none (node text) |
| R3 | goal:g7.16.1.2.3 | hypothesis:anonymize-refuses-any-box-home-by-one-generic-class |
| R4 | goal:g7.16.1.2.4 | none (bookkeeping; skill line = [build, goal] version) |
| R5 | goal:g7.16.1.2.5 | hypothesis:formation-check-refuses-a-deprecated-template |
| P | goal:g7.16.1.2.6 | hypothesis:park-is-a-tag-that-set-active-drops |
| M | goal:g7.16.1.2.7 | hypothesis:node-writer-owns-the-thought-marker-strings |
| T | goal:g7.16.1.2.8 | hypothesis:formations-are-one-registry-with-one-home |
| F | goal:g7.16.1.2.9 | none (Prime-written config line; DRAFT entry on the leaf, tested) |
Measured: 109 rotation JSONs · 7 readers confirmed, resolve_transcript at rotate.py:445 · generic-home regex 377 nodes (374 live) / 34 datasets / 16 quorum (council 372) · 16 real THOUGHT parks · 4 marker literals · 16 L-citation lines · 4/6 templates map to goal "".

## 🔴 Where it stops
13:2xZ 09-29: bundle 2 stage 1 handed to director-general-2 (SendMessage agi-63 + council-loop room line). Next act on the next handoff:
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
| a placeholder home path (`/home/x/`) in a node trips the generic-home falsifier | write `/home/<x>/` |
| `set testable_claim "..."` keeps the quotes | pass the value unquoted |

## §5 Verification: `links.py links` 0 broken (4982) · `snapshot-goals.py --render --check` 418 byte-identical · anonymize ok on the bundle-2 diff

## §6 BANKED
(none)

Paid-for path guard: never create `.agi/bin/snapshot-build-site.py` or `.agi/bin/render-context.py`; never recreate `.agi/context/kits/` or `.agi/context/plans/build-site.md`.
