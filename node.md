---
id: doc:card-director-general-2
mint_id: d55057fc5ba24e7ab2bb66cbf9d326bf
type: doc
parents:
  - goal:g7.16.1
next_edges: []
edited_by: director-general-2
scaffold_hash: b3449e9971f09f91
season: 2
title: Card director general 2
town: core
---
# doc:card-director-general-2

# doc:card-director-general-2 — director-general-2's card (council loop, goal:g7.16.1): the ONE scratch

Replaced whole, never appended; ≤ 100 lines; written DURING the work so a dead session is resumable.

## §0 State (10:3xZ 09-29)
| | |
|---|---|
| post | director-general-2 |
| stage | stage 2 of 3 — experiments + verdicts (and the tests they need) on director-general-1's hypotheses |
| protocol | doc:council-loop (read it first) · goal:g7.16.1 (the owner's words) |
| place | local-town · MAIN /data/work/agi on local-maxxing/season2/main · claude-code Opus 5.5 high · seated 10:3xZ 09-29 by belam |
| skills | agi-node-write · agi-verify · agi-send · agi-rotate · agi-post |
| bundle | 1 (goal:g7.16.1.1) · stage 2 DONE · SM mur residues 7-11 FIXED 3e0e340cb · re-mur residue 21 FIXED e008169dc · table passed to director-general-3 (rows 22-24) |

## §1 Plan
```
done   bundle 1 stage 2: B C D A experiments + verdicts + strict-xfail rows · E triage marks
next   idle until the next [handoff] addressed to director-general-2 (bundle 2, or residues back from sanctuary-master)
```

## §2 Landed
- 951056229 six strict-xfail falsifier rows: test_thought_hygiene.py x4 (B) · test_anonymize_guard.py x1 (C) · test_snapshot_build_site.py x1 (D)
- 53ab755d4 experiment:dg2-{b1,c1,d1,a1}-* + verdict:dg2-{b-thought-marker,c-home-path,d-mint-assigner,a-formation} (lean_proved 80 · 85 · 80 · 60)
- e008169dc residue 21 (re-mur wf_aa3f01d4-2aa): staged-branch anonymize row, revert probe red
- 3e0e340cb residues 7-11 (mur wf_a56d005b-d6b): E tallies + 2 retires · B corpus BEGIN count + widened regex guard · C live-path row · a00-f73695be END restored
- 6ff0e0aa1 row E: 27 nodes THOUGHT-marked (13 keep · 14 parked) · 94 table rows marked in place · goal:g7.32.5 horizon · GOALS.md

## 🔴 Where it stops
11:xxZ 09-29 re-mur residue 21 closed, the table passed to director-general-3 (agi-8f, rows 22-24); then sanctuary-master (agi-4f) re-murs the 6. Nothing live. Next: the next handoff.
```
python3 extensions/agi/bin/send.py --from director-general-2 read director-general-2
```

## §4 Traps
| trap | rule |
|---|---|
| MAIN is shared by every post | commit by exact path; never switch branches, stash or reset |
| `grep -r` / `find` over .agi/ or the repo root io-stalls the box | `git grep PATTERN -- <paths>` |
| a node body quoting the marker with its html-comment open counts as a THOUGHT block under the trunk detector | write "the BEGIN marker"; check the unanchored count before the `thought` verb |
| pytest's truncated diff line pollutes a grep over its output | count offenders in-process with the test's own regex |

## §5 Verification: `python3 extensions/agi/bin/links.py links` 0 broken (4957) · `snapshot-goals.py --render --check` rc 0 · touched files 96 passed · 6 xfailed · 1 failed (the pre-existing corpus row, 15 offenders, unchanged)

## §6 BANKED
(none) · findings for a later bundle: 87 nodes carry the repo path · the writer stamps town: core for local-town posts · 8 nodes carry a surplus column-0 THOUGHT END (fence-gap quotations)

Paid-for path guard: never create `.agi/bin/snapshot-build-site.py` or `.agi/bin/render-context.py`; never recreate `.agi/context/kits/` or `.agi/context/plans/build-site.md`.
