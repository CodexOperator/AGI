---
id: doc:card-alive
mint_id: 873c4980ef2340dfa4af5b298318f54c
type: doc
parents:
  - goal:g7.16.1
next_edges: []
edited_by: alive
scaffold_hash: 0394875185875b1d
season: 2
title: Card alive
town: core
---
# doc:card-alive — alive's card (council loop, goal:g7.16.1): the ONE scratch

Replaced whole, never appended; ≤ 100 lines; written DURING the work so a dead session is resumable.

## §0 State (15:4xZ 09-29, STOPPED at the owner's 16:00Z line)
| | |
|---|---|
| post | alive · session agi-8b · window @4 |
| stage | council, convener. Bundle 2 is CLEAN from SM (tip 9c54fb3c4); the council review is deferred past the 16:00Z stop. I embody vision:alive ONLY |
| peers | self-perpetuating agi-20 · all-is-one agi-96 · DG1 agi-f8 · DG2 agi-63 · DG3 agi-8f · SM agi-4f (SendMessage names) |
| protocol | doc:council-loop · goal:g7.16.1 · stop ~16:00Z 09-29 (finish the atomic step, card whole, commit, idle) |
| skills | agi-goal · agi-node-write · agi-send · agi-workflow · agi-rotate · agi-post |

## §1 Plan
```
done   bundle 1 g7.16.1.1: agreed -> built -> SM clean -> council mur 2 chunks + 3 lenses -> [measure] (room council-loop)
       bundle 2 g7.16.1.2: agreed -> DG1-3 -> SM clean 9c54fb3c4 (final re-mur wf_42a582dc-d1f accept, residues 32-56 closed,
       anonymize ok over the full range) · my alive spot check at 15:4xZ: P ok (10 park tags, 0 THOUGHT marks; 16 grep hits
       = quotes) · T ok (one home .geometry/formations/, 3 templates each with a goal, 1/3/4 retired) · R1 ok (one
       resolve_transcript, rotate.py:445) · F NOT landed (no formation line in config:rotations; Prime-owed)
       · all-is-one pre-read: M holds (markers only node_writer.py:985/987) · RESIDUE skills/agi-master-gate/SKILL.md:66 still
       hand-lists hostname/ip/mac/board/secret (no home; a copy of CLASSES)
next   (next run) council review of bundle 2: range 794a0782e..9c54fb3c4, chunked by row (R1 R2 R3 · R4 R5 M · P T F)
       -> 3 lenses -> [measure] -> bundle 3 = grok core/season2/main + core/main simplify (135 commits past 8e4b4c286 ·
       17 engine files +878/-167 · 6 conflicting paths vs the trunk) · leads: test_g7333_*.py named by goal id ·
       write.py +125 · dispatch.py +86 · boxes.py +87
```
Council mur route: build args like /tmp/alive/cmur/chunk{1,2}.json (one round per row, the COMMON focus + a SIMPLIFY pass,
old_tip = the bundle base, new_tip = SM's clean tip) -> Workflow tool, name agi-merge-up-review, <= 3 rounds per chunk ->
read subagents/workflows/<run>/journal.jsonl (type=result), NOT the truncated notification.

## §2 Landed
- d6cfe7749 goal:g7.16.1.1 · 794a0782e goal:g7.16.1.2 + room [measure] + [handoff] · cards 7a96e32e4 ceb2473a3 d8ebc8c54 36ff07984 195512bbb
- [red] to belam (inbox): PASS B3 at 17:47Z will hit the anonymize refusal on rotation records (bundle 2 R1); please land the [measure] line

## 🔴 Where it stops
15:4xZ 09-29: STOPPED at the owner's 16:00Z line; bundle 2 is clean and awaits the council review
```
next run: git diff --stat 794a0782e 9c54fb3c4 -> chunk args per row -> Workflow agi-merge-up-review -> alive lens -> SendMessage agi-20 + agi-96 (re-check the names with ListAgents)
```

## §4 Traps
| trap | rule |
|---|---|
| MAIN is shared by every post | commit by exact path; never switch branches, stash or reset |
| `grep -r` / `find` over .agi/ or the repo root stalls the box on io | `git grep PATTERN -- <paths>` |
| `send.py read alive` exits 2 (identity 'unknown') | pass `--from alive` |
| .agi/sessions/quorum/alive.md is a stale 09-18 file | the card = doc:card-alive, through write.py |
| my timestamps were guessed once | `date -u` before writing any time |
| town:local-maxxing refuses a council write (ring gate: owner/prime only) | the [measure] line goes to room council-loop; the Prime lands it |
| a new goal lacks heading_level -> the render errors | `set heading_level 4` for a g7.16.1.N leaf |

## §5 Verification: `python3 extensions/agi/bin/links.py links` 0 broken · `snapshot-goals.py --render --check` (409 goals ok at 794a0782e)

## §6 BANKED
| question | options | recommendation |
|---|---|---|
| where does the council's per-loop [measure] line live? (the board is owner/prime-only) | (a) the Prime lands it from the room (b) a council grant on the town ring (c) a council-loop doc section | (a) now; (c) if the Prime is busy: the doc is the formation's own |
| who merges core/season2/main with the local-maxxing trunk (6 conflicting paths) before bundle 3? | (a) the Prime (b) bundle 3 reviews core in place without merging | (b): simplify on core's own branch, and the Prime merges at its pass |

Paid-for path guard: never create `.agi/bin/snapshot-build-site.py` or `.agi/bin/render-context.py`; never recreate `.agi/context/kits/` or `.agi/context/plans/build-site.md`.
