---
id: doc:card-sanctuary-master
mint_id: 9a4a831c938a4501b30d37248ad319c0
type: doc
parents:
  - goal:g7.16.1
next_edges: []
edited_by: sanctuary-master
scaffold_hash: 3e856c7e9b80c2ab
season: 2
title: Card sanctuary master
town: core
---
# doc:card-sanctuary-master

# doc:card-sanctuary-master — sanctuary-master's card (council loop, goal:g7.16.1): the ONE scratch

Replaced whole, never appended; ≤ 100 lines; written DURING the work so a dead session is resumable.

## §0 State (21:1xZ 09-29)
| | |
|---|---|
| post | sanctuary-master: the bundle reviewer, standard mur on claude-code at Opus 5.5 high (owner 09-29 authorizes the Workflow tool for this review, over skill agi-workflow's pi-only rule, in this mode) |
| protocol | doc:council-loop · goal:g7.16.1 |
| place | local-town · MAIN /data/work/agi on local-maxxing/season2/main · gen 6 (crash-recovery 17:33Z, agi-b8) |
| skills | agi-merge-pass (§2 verdict rules) · agi-workflow · agi-send · agi-rotate · agi-post · agi-node-write |
| peers | DG1 agi-77 · DG2 agi-40 · DG3 gen 4 agi-c5 (card doc:card-director-general-3) · alive agi-13 (council convener) · belam = send.py inbox (tag [merge-up]) |
| now | bundle 3 CLEAN re-confirmed at 1f39ffb1c (= bundle 4's base), 21:1xZ, to room + alive + belam · alive lifts the bundle-4 build HOLD |

## §1 Plan
```
done   bundle 1 CLEAN · bundle 2 CLEAN · bundle 3 CLEAN at 1f39ffb1c: SM 57-80 24/24 + council C1, CM1-CM10 11/11 closed, 1 red closed
next   bundle 4 (goal:g7.16.1.4 write/render split, re-scoped by DG1 68d4c8504) → mur at DG3's handover
       3-4 rounds per run, never parallel murs · 23:00Z: finish the step, card whole, idle
```

## §2 Landed
- bundle 3 murs: A wf_a3b15e54-c65 · B wf_9dd69ca3-b96 · C wf_67ad5686-154 · wf_dd91b5bc-0ea · wf_2cd1c504-7cc (→ 9966e3050)
- council reopen: C1 wf_0696f122-7f0 (66da33b01, +78 79 a1eabdebf) · CM1-6 CM8 wf_868fe677-21c · CM7 CM9 CM10 wf_4fa09963-e62
  + 80 1f39ffb1c (bytes read, 22p) → CLEAN 1f39ffb1c · links 5143/0 · live check_formation PASS · anonymize ok
- red: R2 recovery budget spent before _recover_seat (live) → belam [red] → closed 0d33b10f4
- SM miss, owned: the H4f round took "prints unpark FAILED" as the claim, never the rc (council C1 caught it)
- bundle 1: 5 murs → CLEAN 80c1c245d · bundle 2: → CLEAN 9c54fb3c4 (residues 32-56)

## 🔴 Where it stops
21:1xZ: idle, waiting on bundle 4's handover (DG1 → DG2 → DG3 → SM) after alive lifts the HOLD. Nothing running. At the handover:
Workflow tool, name agi-merge-up-review, rounds = the bundle's rows (old = row commit^, new = row commit; commits interleaved
with other posts' → one round per commit) · summary: python3 /data/tmp/claude-1000/sm-mur-summary.py <run dir>/journal.jsonl
next-bundle goal-leaf candidates: /data/tmp/claude-1000/sm-b3-clean.md + room [handoff] 21:1xZ (parked_carriers docstring,
stand-in lacks launch-wrapper/env, autopsy reaper/service log paths raw, CM6 timeout untested)

## §4 Traps
| trap | rule |
|---|---|
| MAIN is shared by every post | commit by exact path; never switch branches, stash or reset |
| `grep -r` / `find` over .agi/ or the repo root io-stalls the box | `git grep PATTERN -- <paths>` |
| rotate flattens the quorum card | re-link: `ln -sfn ../../nodes/doc/card-sanctuary-master.md .agi/sessions/quorum/sanctuary-master.md` |
| a home path in a card or dm | write `<home>`; check: `anonymize.py check --text "$(cat <card>)"` |
| a peer's commits land between a row's commits | one round per commit, never a range across a foreign commit |
| town:local-maxxing is ring-gated (owner, prime_director) | the board numbers line goes to belam in the [merge-up] |
| a mur residue chain | ask for residues only on what THIS diff introduced or left open; the rest are notes |
| a claim that names a message ("prints X") | the round also checks the rc and what was written (C1) |
| verify-suite.lock held by a live runner | a test run ERRORs at setup: retry, never read it as a code red |
| card stamps | read `date -u`, never estimate |

## §5 Verification: `python3 extensions/agi/bin/links.py links` 0 broken · live check_formation PASS · GOALS render --check = row G → g7.16.1.4 W-G

## §6 BANKED
(none)
