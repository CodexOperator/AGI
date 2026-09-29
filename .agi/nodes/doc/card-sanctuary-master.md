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

## §0 State (22:4xZ 09-29) — STOPPED at the 23:00Z order, idle
| | |
|---|---|
| post | sanctuary-master: the bundle reviewer, standard mur on claude-code at Opus 5.5 high (owner 09-29 authorizes the Workflow tool for this review, over skill agi-workflow's pi-only rule, in this mode) |
| protocol | doc:council-loop · goal:g7.16.1 |
| place | local-town · MAIN /data/work/agi on local-maxxing/season2/main · gen 6 (crash-recovery 17:33Z) · meter 0.44 at stop |
| skills | agi-merge-pass (§2 verdict rules) · agi-workflow · agi-send · agi-rotate · agi-post · agi-node-write |
| peers | DG1 · DG2 · DG3 (gen 4 stopped; its successor reads doc:card-director-general-3 + its send.py inbox) · alive (council convener) · belam = send.py inbox ([merge-up] / [red]) |
| now | bundle 3 CLEAN at 1f39ffb1c · bundle 4 reviewed through W2a, residues 97-105 open with DG3's successor · nothing running |

## §1 Plan
```
done   bundle 1 CLEAN 80c1c245d · bundle 2 CLEAN 9c54fb3c4 · bundle 3 CLEAN 1f39ffb1c (SM 57-80 24/24 + council C1, CM1-CM10 11/11)
done   bundle 4 murs: run 1 W-G.1 + W0 · run 2 W-G.2 + re 81-85 · run 3 W1a + W1b · run 4 re 90/93/95/87/88 + re 89 + W2a
NEXT   re-mur (one round per commit) DG3-successor's fixes for 97-105 · formal round on fd8d74ab3 (91 92, bytes already read)
       then W1c / W2b-e / W3 as DG3 lands them; bundle 4 CLEAN → [handoff] room + alive + belam [merge-up]
```

## §2 Landed
- bundle 3: A wf_a3b15e54-c65 · B wf_9dd69ca3-b96 · C wf_67ad5686-154 · wf_dd91b5bc-0ea · wf_2cd1c504-7cc · C1 wf_0696f122-7f0 ·
  council wf_868fe677-21c · wf_4fa09963-e62 → CLEAN 1f39ffb1c · 1 red (R2 heal budget) closed 0d33b10f4
- bundle 4: wf_55fc5dde-0e5 · wf_8ce06028-a81 · wf_e6561265-419 · wf_7da1e726-280 (18 CC opus agents, 0 err)
  closed: 81 83 84 87 88 89(part) 90(mostly) 91 92 93 95 · owner line for the GOALS.md retirement verified (goal:g7.16.1.md:72)
- W1b [red] to belam 22:2xZ: a failed auto-commit left the node staged in MAIN's index → 90 fixed c13eec672, 98 still open
- SM miss, owned: bundle-3 H4f round took "prints unpark FAILED" as the claim, never the rc (council C1 caught it)
- [merge-up] to belam 22:4xZ: bundle 3 CLEAN, bundle 4 state, the new suite red (97)

## 🔴 Where it stops
Stopped at the owner's 23:00Z order; nothing running. Open with DG3's successor (bodies /data/tmp/claude-1000/sm-b4-run{2,3,4}.md):
97 FIX FIRST suite red on HEAD: test_commands_manifest names_no_box_detail (commands.md:3036 'g7.16.1.4.1.1' reads as an IP)
98 write.py _commit_write ignores reset rc (index.lock → still staged, message says unstaged) · 99 [config].md:227 config_path claim
100 tests that cannot fail (95 self-quoting THOUGHT, 93 stale lock, 90 index-lock case) · 101 g4.19 F1 missing test file, invariant unguarded
102 links.py mint GrepError rc 1 = not-found · 103 resolve_mint counts .md.bak · 104 deprecated/ excluded · 105 mvp rc claim + untested paths
banked on DG3's card (theirs): 86 report_integrity/s26 re-wire · 94 subprocess auto-commit opt-out · 96 row --dry-run · W1c
First command at wake: python3 extensions/agi/bin/send.py --from sanctuary-master read sanctuary-master
Round args pattern: /data/tmp/claude-1000/sm-b4-run3.json · summary: python3 /data/tmp/claude-1000/sm-mur-summary.py <run dir>/journal.jsonl

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
| a dotted goal id like g7.16.1.4.1 in a rendered manifest | the dotted-quad guard reads 16.1.4.1 as an IP (97) |
| verify-suite.lock held by a live runner | a test run ERRORs at setup: retry, never read it as a code red |
| write.py self-commits since 14cf86000 (W1b) | my card edits via Write/sed are NOT write.py: still commit by exact path |
| card stamps | read `date -u`, never estimate |

## §5 Verification: `python3 extensions/agi/bin/links.py links` 5165 / 0 broken · live check_formation PASS · test_commands_manifest RED on HEAD (97)

## §6 BANKED
(none)
