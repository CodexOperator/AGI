---
id: doc:card-sanctuary-master
mint_id: 9a4a831c938a4501b30d37248ad319c0
type: doc
parents:
  - goal:g7.16.1
next_edges: []
edited_by: belam
scaffold_hash: 3e856c7e9b80c2ab
season: 2
title: Card sanctuary master
town: core
---
# doc:card-sanctuary-master

# doc:card-sanctuary-master — sanctuary-master's card (council loop, goal:g7.16.1): the ONE scratch

Replaced whole, never appended; ≤ 100 lines; written DURING the work so a dead session is resumable.

## §0 State (00:0xZ 09-30) — gen 7, woke 23:38Z; NEW LOOP (owner 23:5xZ, doc:council-loop "The loop"); STOP ~04:00Z 09-30
| | |
|---|---|
| post | sanctuary-master: the bundle reviewer, standard mur on claude-code at Opus 5.5 high (owner 09-29 authorizes the Workflow tool for this review, over skill agi-workflow's pi-only rule, in this mode) |
| protocol | doc:council-loop "The loop" · goal:g7.16.1 |
| place | local-town · MAIN /data/work/agi on local-maxxing/season2/main · gen 7 |
| skills | agi-merge-pass (§2 verdict rules) · agi-workflow · agi-send · agi-rotate · agi-post · agi-node-write |
| peers | DG1 (outcomes) · DG2 · DG3 · DG4 · DG5 (room `directors`) · alive · all-is-one · self-perpetuating (council) · belam |
| duty | the bundle arrives AFTER the directors' inner loops (DG2 MVP-vs-hypotheses forks · DG1 builds-vs-goals nested subgoals · DG1 one OUTCOME per goal) ─► mur through my lens ─► residues back to the directors ─► nothing left to dispatch ─► I write the BIGGER_OUTCOME nodes ([bigger_outcome].md: parents outcome|verdict, 1-4) ─► hand the grown chain to the council |
| now | run 5 DONE: 96 · 91+92 · 97 closed → 106 107 sent to DG3 (agi-6b) · waiting: DG3 fix SHAs · DG1 (agi-77) outcomes for bundles 1+2 |

## §1 Plan
```
done   bundle 1 CLEAN 80c1c245d · bundle 2 CLEAN 9c54fb3c4 · bundle 3 CLEAN 1f39ffb1c (outcome:g7-16-1-3-bundle-3-closed exists)
done   bundle 4 murs runs 1-4 (see §2)
done   run 5 wf_884739ac-f61: 96 CLOSED · 91 92 CLOSED (→106) · 97 CLOSED (→107) · sent DG3 + room
NEXT   bundles 1 + 2: goals still `active`, no outcome → DG1 writes their outcomes (new loop) → then I write the bigger_outcome
       tying bundles 1-3 (parents: the 3 outcomes; judged_against goal:g7.16.1; lens = the council's)
       bundle 4: re-mur 98-105 fixes as DG3/DG4 land them · W1c / W2b-e / W3 · CLEAN → DG1 outcome → bigger_outcome
       .6 / .7 bundles (DG4 / DG5) as they deliver
```

## §2 Landed
- bundle 3: A wf_a3b15e54-c65 · B wf_9dd69ca3-b96 · C wf_67ad5686-154 · wf_dd91b5bc-0ea · wf_2cd1c504-7cc · C1 wf_0696f122-7f0 ·
  council wf_868fe677-21c · wf_4fa09963-e62 → CLEAN 1f39ffb1c · 1 red (R2 heal budget) closed 0d33b10f4
- bundle 4: wf_55fc5dde-0e5 · wf_8ce06028-a81 · wf_e6561265-419 · wf_7da1e726-280 (18 CC opus agents, 0 err)
  closed: 81 83 84 87 88 89(part) 90(mostly) 91 92 93 95 · owner line for the GOALS.md retirement verified (goal:g7.16.1.md:72)
- gen 7 wake: quorum card re-linked c2e2fd14c · alive's key-row [red] = adjacency-only, synced by belam 93f4567b5
- run 5 wf_884739ac-f61 (6 CC opus, 0 err): closed 91 92 96 97 · opened 106 107 (body /data/tmp/claude-1000/sm-b4-run5.md)

## 🔴 Where it stops
```
Nothing running. Waiting on DG3 fix SHAs (re-mur one round per commit) and DG1's bundle 1+2 OUTCOMES (then bigger_outcome over 1-3).
Open with DG3 (bodies /data/tmp/claude-1000/sm-b4-run{2,3,4,5}.md):
106 falsifier 2 of g4.18.5.2: payload-only / adopt / create --payload untested · 107 commands.md:3044 reason unresolvable + guard eats 5-part goal ids
98 write.py _commit_write ignores reset rc · 99 [config].md:227 config_path claim · 100 tests that cannot fail (95 93 90)
101 g4.19 F1 missing test file · 102 links.py mint GrepError rc 1 · 103 resolve_mint counts .md.bak · 104 deprecated/ excluded · 105 mvp rc claim
banked on DG3's card (theirs): 86 report_integrity/s26 re-wire · 94 subprocess auto-commit opt-out · W1c
First command at wake: python3 extensions/agi/bin/send.py --from sanctuary-master read sanctuary-master
Summary: python3 /data/tmp/claude-1000/sm-mur-summary.py <run dir>/journal.jsonl · round args pattern: /data/tmp/claude-1000/sm-b4-run3.json
```
## §4 Traps
| trap | rule |
|---|---|
| MAIN is shared by every post | commit by exact path; never switch branches, stash or reset |
| `grep -r` / `find` over .agi/ or the repo root io-stalls the box | `git grep PATTERN -- <paths>` |
| rotate flattens the quorum card | re-link: `ln -sfn ../../nodes/doc/card-sanctuary-master.md .agi/sessions/quorum/sanctuary-master.md` |
| a home path in a card or dm | write `<home>`; check: `anonymize.py check --text "$(cat <card>)"` |
| a peer's commits land between a row's commits | one round per commit, never a range across a foreign commit |
| a mur residue chain | ask for residues only on what THIS diff introduced or left open; the rest are notes |
| a claim that names a message ("prints X") | the round also checks the rc and what was written (C1) |
| a dotted goal id like g7.16.1.4.1 in a rendered manifest | the dotted-quad guard reads 16.1.4.1 as an IP (97) |
| verify-suite.lock held by a live runner | a test run ERRORs at setup: retry, never read it as a code red |
| write.py self-commits since 14cf86000 (W1b) | card edits through write.py commit themselves |
| a bigger_outcome before the directors' outcomes | never: DG1 writes one OUTCOME per goal first; mine ties them (max 4 parents) |
| card stamps | read `date -u`, never estimate |

## §5 Verification: links.py links 5165 / 0 broken (gen 6) · test_commands_manifest 181/181 at HEAD (run 5 R97) · test_write 146p/5x at 389afc3e1

## §6 BANKED
(none)
