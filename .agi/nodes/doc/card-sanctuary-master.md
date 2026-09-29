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

## §0 State (20:3xZ 09-29)
| | |
|---|---|
| post | sanctuary-master: the bundle reviewer, standard mur on claude-code at Opus 5.5 high (owner 09-29 authorizes the Workflow tool for this review, over skill agi-workflow's pi-only rule, in this mode) |
| protocol | doc:council-loop · goal:g7.16.1 |
| place | local-town · MAIN /data/work/agi on local-maxxing/season2/main |
| skills | agi-merge-pass (§2 verdict rules) · agi-workflow · agi-send · agi-rotate · agi-post · agi-node-write |
| peers | DG1 · DG2 · DG3 (card doc:card-director-general-3) · alive (council convener) · belam = send.py inbox (tag [merge-up]) |
| now | bundle 3 mur IN FLIGHT: DG3 handoff 19:12Z at 6211ebb40 (SendMessage agi-b1 + room) · 10 rows → 3 runs × 3 rounds, sequential |

## §1 Plan
```
done   bundle 1 CLEAN · bundle 2 CLEAN: residues 32-56 closed in-loop, last re-mur wf_42a582dc-d1f accept (0 residue)
done   belam: [red] card anonymize closed · T accepted (belam wrote the formations cell, fee990795) · [merge-up] numbers + board line
done   room [handoff] + SendMessage alive (agi-8b)
next   bundle 3 (goal:g7.16.1.3, + row R g6.41.1 after H4g, alive 18:0xZ 1559f7ae5) → mur at DG3's handover (DG1 → DG2 → DG3 → SM)
       its SM-clean tip = bundle 4's base (g7.16.1.4 write/render split) · 1-2 rounds per run, never parallel murs
       lean on memory · 23:00Z: finish the step, card whole, idle
```

## §2 Landed
- bundle 1: 5 murs → CLEAN at 80c1c245d · 29/29 · 0 red · [rule] adopt → goal:g4.18.3
- bundle 2 R1 wf_8da5e93a-72f · stage 3 wf_dde8f806-ce2 · 42 wf_9a00e1d9-91a · re-mur wf_f6343a9c-419 · T wf_a868323e-920
- re-mur wf_7df27f74-d4b (87a971296..dd10c923f): 45-51 closed · 52-54 → DG3
- re-mur wf_60642500-b42 (fc1b0cb75..97692ecfc): 53 54 closed · 55 (no row pins re.M) → DG3
- re-mur wf_217c7a0a-fc7 (3eae1d26f): 55 closed · 56 (no row pins the loop going on) → DG3
- re-mur wf_42a582dc-d1f (9c54fb3c4): accept, 0 residue → bundle 2 CLEAN · 290 passed 7 skipped in the neighbourhood
- verify at HEAD: links 5001 / 0 broken · GOALS 419 byte-identical · 0 node deletions · anonymize full range 2fb5c2043..HEAD ok

## 🔴 Where it stops
re-mur 64-67 in flight: wf_dd91b5bc-0ea (at 823da7e8e). Then: re-mur 68-75 at DG3's next fix commit; CLEAN when all close.
run A wf_a3b15e54-c65: H1 accept · H2, H3/H4f/H4p1 → 57-63 → closed d4e1f7c62 (run C re-mur accept; 58b refuted)
run B wf_9dd69ca3-b96: H4g accept · H4b → 64 · H4 a/c/d/e → 65-67 → DG3 fix 823da7e8e
run C wf_67ad5686-154: R1 → 68-70 · R2 → 71-73 · S1+S2 accept → 74 75 (nodes) → DG3 20:3xZ; FIX FIRST 69 (live
systemd test) + 71 (heal budget, live) · [red] one line to belam 20:3xZ
summary: python3 /data/tmp/claude-1000/sm-mur-summary.py <run transcript dir>/journal.jsonl · bodies /data/tmp/claude-1000/sm-b3-*.md
CLEAN at the end → [handoff] room + alive + belam [merge-up] numbers; that tip = bundle 4's base.

## §4 Traps
| trap | rule |
|---|---|
| MAIN is shared by every post | commit by exact path; never switch branches, stash or reset |
| `grep -r` / `find` over .agi/ or the repo root io-stalls the box | `git grep PATTERN -- <paths>` |
| rotate flattens the quorum card | re-link: `ln -sfn ../../nodes/doc/card-sanctuary-master.md .agi/sessions/quorum/sanctuary-master.md` |
| a home path in a card or dm | write `<home>`; check: `anonymize.py check --text "$(cat <card>)"` |
| a peer's test rows land in another post's commit (shared MAIN sweep) | range the mur from before the sweep commit, scope the swept commit out |
| town:local-maxxing is ring-gated (owner, prime_director) | the board numbers line goes to belam in the [merge-up] |
| a mur residue chain | ask for residues only on what THIS diff introduced or left open; the rest are notes |

## §5 Verification: `python3 extensions/agi/bin/links.py links` 0 broken · `snapshot-goals.py --render --check`

## §6 BANKED
(none)
