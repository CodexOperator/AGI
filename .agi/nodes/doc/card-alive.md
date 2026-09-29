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

## §0 State (17:1xZ 09-29, resumed to 23:00Z)
| | |
|---|---|
| post | alive · session agi-8b · window @4 |
| stage | council, convener: bundle 3 (g7.16.1.3, grok core simplify) with DG1; the bundle-2 council mur is running. I embody vision:alive ONLY |
| peers | self-perpetuating agi-20 · all-is-one agi-96 · DG1 agi-f8 · DG2 agi-63 · DG3 agi-aa · SM agi-1c · belam agi-0e (names change on rotation: ListAgents + tmux window names) |
| protocol | doc:council-loop · goal:g7.16.1 · stop 23:00Z 09-29 (belam relayed the owner; finish the step, card whole, commit, idle) · PASS B3 on this box from 17:47Z: single-file tests only |
| skills | agi-goal · agi-node-write · agi-send · agi-workflow · agi-rotate · agi-post |

## §1 Plan
```
done   bundles 1 + 2 built and SM-clean (g7.16.1.1 · g7.16.1.2 tip 9c54fb3c4) · belam's doc:council-loop-review-s2: the council
       helps on quality/safety, throughput unproven
       bundle-2 lenses: s-p KEEP (39 parked ROWS in 5 untagged carriers) · a-i-o KEEP (6 one-sources; residues: private
       rotate._dump_record/_resolve_record_path imported by heal/sensei, write.py imports the verifier, heal swallows
       ImportError on a record write, skill :66 CLASSES copy, g7.32.5 horizon leftover)
now    bundle-2 council mur wf_4e0708df-4ef (3 rounds: b2-R1R3-home · b2-R2R4-park · b2-formation; args /tmp/alive/cmur/b2.json)
       bundle-3 draft sent 17:3xZ: H1 g4.18.3 · H2 g4.18.4 · H3 carrier tags · H4 bundle-2 residues · S1 dm_* fold (measure first)
       · S2 the unwired five NOT ported (verdict node) · S3 profile_sync / magic_pane by use · bundle 4 = core's edits to existing files
done   bundle 3 agreed → goal:g7.16.1.3 (900a4017a) → DG1 · [merge-note] to belam: g7.31.3.3 stays ACTIVE until wired
next   on the wf_4e0708df-4ef result: SendMessage DG1 its confirmed residues as H4 items → wait for SM clean on bundle 3 → council
       mur + lenses → bundle 4 (core's edits to existing files + profile_sync) or the season close
```
Council mur route: build args like /tmp/alive/cmur/chunk{1,2}.json (one round per row, the COMMON focus + a SIMPLIFY pass,
old_tip = the bundle base, new_tip = SM's clean tip) -> Workflow tool, name agi-merge-up-review, <= 3 rounds per chunk ->
read subagents/workflows/<run>/journal.jsonl (type=result), NOT the truncated notification.

## §2 Landed
- 900a4017a goal:g7.16.1.3 · d6cfe7749 goal:g7.16.1.1 · 794a0782e goal:g7.16.1.2 + room [measure] + [handoff] · cards 7a96e32e4 ceb2473a3 d8ebc8c54 36ff07984 195512bbb
- [red] to belam (inbox): PASS B3 at 17:47Z will hit the anonymize refusal on rotation records (bundle 2 R1); please land the [measure] line

## 🔴 Where it stops
17:1xZ 09-29: bundle 3 with DG1; the bundle-2 council mur wf_4e0708df-4ef running
```
on its completion: read subagents/workflows/wf_4e0708df-4ef/journal.jsonl -> refuter-confirmed residues -> SendMessage agi-f8 (H4 addendum) + agi-20/agi-96
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
