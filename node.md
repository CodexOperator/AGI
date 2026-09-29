---
id: doc:card-self-perpetuating
mint_id: 05887a05d0054eee9adcf7d0658dfe2b
type: doc
parents:
  - goal:g7.16.1
next_edges: []
edited_by: belam
scaffold_hash: c808a090daec9950
season: 2
title: Card self perpetuating
town: core
---
# doc:card-self-perpetuating

# doc:card-self-perpetuating — self-perpetuating's card (council loop, goal:g7.16.1): the ONE scratch

Replaced whole, never appended; ≤ 100 lines; written DURING the work so a dead session is resumable.

## §0 State (18:1xZ 09-29 · resumed to 23:00Z by the owner via belam)
| | |
|---|---|
| post | self-perpetuating · CC session agi-20 |
| stage | council — you embody vision:self-perpetuating ONLY (read it whole first); every review speaks from that vision alone, never alive or all-is-one |
| protocol | doc:council-loop (read it first) · goal:g7.16.1 (the owner's words) |
| place | local-town · MAIN /data/work/agi on local-maxxing/season2/main · claude-code Opus 5.5 high · seated 10:3xZ 09-29 by belam |
| sessions | alive agi-8b · all-is-one agi-96 · DG1 agi-f8 · DG2 agi-63 · DG3 agi-aa · SM agi-1c · belam agi-0e — SendMessage; room council-loop for the record |
| skills | agi-node-write · agi-send · agi-workflow · agi-rotate · agi-post |

## §1 Plan
```
done   bundles 1 + 2 built, SM CLEAN (80c1c245d · 9c54fb3c4) + lens reviews · bundle 3 = goal:g7.16.1.3 (900a4017a) handed to DG1 18:0xZ — bytes checked: S1 dm-format test · S2 goal+sha+test+pass count, "not wired" as a BODY status line, g7.31.3.3 stays active
next   idle until SM returns bundle 3 clean (DG1 -> DG2 -> DG3 -> SM); bundle-2 council mur residues join H4
then   bundle 3 built + SM clean -> batched mur + ONE lens review · stop 23:00Z: finish the step, card whole, idle
```

## §2 Landed
- bundle 1 lens: KEEP 5, 0 red · conditions carried into bundle 2 (one `~` resolver, caller-grep parking test, generic home regex, park count gate)
- bundle 2 lens (17:2xZ): test_rotation_record_home 10 passed · anonymize over 794a0782e..9c54fb3c4 exit 0 · 8 park tags, 0 THOUGHT marks · of 16 parks: 8 PARK / 8 LIVE, 7 of the 8 un-parks record their caller reason · F (config:rotations formation line) still owed
- FINDING: 39 parked rows in body tables whose carrier has no tag (g7.33.19 11 · pass10 11 · pass11 3 · pass12 8 · passb1 6): a g7.16.2 switch wakes none. Proposed: tag the carriers + the check FAILs on an untagged row-park
- bundle 3 votes: g4.18.3/.4 first · simplify on our trunk; each folded node names its core module + sha (pointer on OUR trunk: core is read-only, conceded to all-is-one) · every fold carries its test
- bundle-3 draft reply: KEEP H1-H4 S1-S3 · S1 ADD a test reading a real committed dm file through the folded module · S2 ADD per module: its goal + core sha + test as the start point + "built, not wired". 4 of the unwired five (parent_slots, needs_rotate, spawn_refusal, kid_write_gate) = g7.31.3.3 seeds .1-.5, COMPLETE on core but unwired (0 non-test importers, measured on origin/core/season2/main)
- S2 settled with all-is-one: g7.31.3.3 stays ACTIVE until wired (core says complete); leaves land active, "built at <sha>, not wired" in each leaf BODY (state), never THOUGHT

## 🔴 Where it stops
18:1xZ 09-29 bundle 3 (goal:g7.16.1.3) is with DG1 agi-f8; the council waits for SM's clean return
```
python3 extensions/agi/bin/send.py --from self-perpetuating read self-perpetuating
```

## §4 Traps
| trap | rule |
|---|---|
| MAIN is shared by every post | commit by exact path; never switch branches, stash or reset |
| `grep -r` / `find` over .agi/ or the repo root io-stalls the box | `git grep PATTERN -- <paths>` |
| `send.py read self-perpetuating` exits 2 ('not you: unknown') | pass `--from self-perpetuating` before the verb |

## §5 Verification: `python3 extensions/agi/bin/links.py links` 0 broken · `snapshot-goals.py --render --check`

## §6 BANKED
(none)
