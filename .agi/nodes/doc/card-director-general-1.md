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

## §0 State (16:5xZ 09-29 — RESUMED by belam, owner 16:5xZ: "we can Keep working till 7pm next and I'll check my CC sub then"; stop at 23:00Z, same stop order)
| | |
|---|---|
| post | director-general-1 |
| stage | IDLE · bundle 1 closed (my residues 1-6, 19-20) · bundle 2 stage 1 done (82d64ffe7) + my residues 41, 36 closed by SM at 29babdf75 · nothing owed |
| protocol | doc:council-loop · goal:g7.16.1 |
| place | local-town · MAIN /data/work/agi on local-maxxing/season2/main · claude-code Opus 5.5 high |
| skills | agi-goal · agi-node-write · agi-send · agi-rotate · agi-post |

## §1 Plan
```
done   bundle 1 stage 1 (59ad74144) · residues 1-6 (663da3a12) · residues 19-20 (50911a0d7)
done   bundle 2 stage 1: 9 leaves g7.16.1.2.1-.9 + 6 hypotheses
done   bundle 2 residues 41 + 36 (29babdf75), SM ack: nothing more for DG1 on bundle 2
next   waiting for the council's next handoff (until 23:00Z; PASS B3 runs on this box at 17:47Z: single-file tests only) addressed to director-general-1 (bundle 3 = grok core/season2/main simplify)
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
16:5xZ 09-29: resumed, idle, waiting for the bundle 3 handoff; nothing in flight. Open (not mine): DG3 owes a commit of goal:g7.16.2 (its R3 scrub line is already in GOALS.md at 29babdf75; note in its inbox, sweep retrying). Next act on wake:
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
| a placeholder home path with a bare segment in a node trips the generic-home falsifier | write the segment as <name>, or ~/ |
| `set testable_claim "..."` keeps the quotes | pass the value unquoted |
| a GOALS.md render in MAIN picks up other posts' uncommitted goal edits | check `git status -- .agi/nodes/goal` before rendering; flag, never revert a scrub |
| `send.py send --dm` does not exist | inbox: `send.py --from <me> send <target> TEXT` (body via python subprocess) |

## §5 Verification: `links.py links` 0 broken (4999) · `snapshot-goals.py --render --check` 418 byte-identical (working tree) · anonymize ok on each diff

## §6 BANKED
(none)

Paid-for path guard: never create `.agi/bin/snapshot-build-site.py` or `.agi/bin/render-context.py`; never recreate `.agi/context/kits/` or `.agi/context/plans/build-site.md`.
