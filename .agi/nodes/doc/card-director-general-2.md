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

## §0 State (23:00Z 09-29 — IDLE at the owner's 23:00Z stop, relayed by belam via the council)
| | |
|---|---|
| post | director-general-2 · gen 2 · session agi-40 (@7) · re-seated 17:34Z after the 17:33Z crash-recovery respawn |
| stage | bundle 3 DONE · bundle 4 DONE (round 1 + re-scope + 4 re-verdicts) · nothing owed |
| protocol | doc:council-loop (read it first) · goal:g7.16.1 (the owner's words) |
| place | local-town · MAIN /data/work/agi on local-maxxing/season2/main · claude-code Opus 5.5 high |
| skills | agi-node-write · agi-verify · agi-send · agi-rotate · agi-post |
| meter | 0.29 of the 0.47 line at the stop |

## §1 Plan
```
done     bundle 1 · 2 (+ residues) · 3 (11 rows) · 4 (12 rows + 7 re-scope hyps + 4 re-verdicts)
next     on wake: read the inbox; act only on a [handoff] / residue addressed to director-general-2
how      read-only measurement agents -> drafts in /tmp/<scratch>/<key>/ -> I review, mint experiment + verdict,
         apply strict-xfail rows, ONE test file per run behind a flock, commit by EXACT PATH -> [handoff] DG3 + room line
rule     no MAIN commit while .agi/sessions/verify-suite.lock exists (tests refuse too: suite_guards.py)
```

## §2 Landed (bundle 4, goal:g7.16.1.4 + re-scope)
- 3cc155a3e input proved (12/12 core hunks named) · 67cf26452 W-G lean60 (6 live callers) · addcc01da W2a lean70 · W2b lean-dis55
- 708a463d8 W3a lean65 · W3 B3 lean85 · W3c lean-dis55 · aa4a1ff1c W2c lean-dis55 · W2d lean-dis60 · a1eafd484 W1a 70 · W1b 75 · W1 B2 55
- re-scope (DG1 68d4c8504): 6a47bdd09 W2b.1 85 · W2b.2 65 (round-1 neighbourhood row retired) · b7fc4ea86 W3c re 70
- c1bab835c W2d .4.1 dis80 · .4.2 65 · migration dis65 · 75218add6 W2c A dis60 · B 55 · C 70
- b8d667880 re-verdicts after DG1 d4a186957: W2c A (parents only) 80 · W3c (ceiling 125) 75
- a855d3758 re-verdicts after the Prime's mint [decision] (a): W2d .4.1 75 · migration 65
- totals: 45 nodes (24 round 1 + 17 re-scope + 4 re-verdicts) · 30 round-1 + 12 re-scope strict-xfail rows (1 round-1 row retired)

## §2b Landed (bundle 3, goal:g7.16.1.3 + goal:g6.41.1)
- 46077247b H1 90 · 25aba7ebc H2 80 · b8646c6fc H3 85 · H4f 85 · f4de8103f H4p1 75 · H4g 90 · 30329d8a7 H4b 80
- e019d63b0 R1 65 · R2 80 (dummies only, units dg2-r-dummy-*) · 65576ac93 S1 proved (VERDICT, not FOLD) · S2 proved

## 🔴 Where it stops
23:00Z 09-29: IDLE at the owner's stop. Nothing live, nothing owed. DG3 (agi-c5) holds bundle 4's builds; DG1's leaves carry
the Prime's mint ruling (7cf590f0d). Scratch drafts (not evidence): /tmp/dg2b3/, /tmp/dg2b4/. On wake:
```
python3 extensions/agi/bin/send.py --from director-general-2 read director-general-2
```

## §4 Traps
| trap | rule |
|---|---|
| MAIN is shared; other posts stage files in the ONE index (a foreign GOALS.md sat staged 21:2xZ) | `git commit -m … -- <exact paths>` (add new files first); never bundle |
| a lock check that only PRINTS the lock does not stop the commit | gate every commit: `[ ! -e .agi/sessions/verify-suite.lock ] && …`; wait with an until-loop in the background |
| write.py now tries its own commit and refuses under the suite lock | its write still lands: commit the node by exact path after the lock clears |
| replace body refuses a range that splits a paragraph/heading section | replace the whole paragraph, or `sub` |
| two agents appending to one test file | patches conflict only at EOF: append the `+` lines of the hunk |
| `grep -r` / `find` over .agi/ io-stalls the box | `git grep PATTERN -- <paths>` |
| a peer session name dies with its rotation (agi-b1 -> agi-c5) | read the post's `session_name` in posts.md, or ListAgents |
| never a /home/<name>/ path in a node | `git grep -lP '/(?:home|Users)/[\w-][\w.-]*' -- <new nodes>` = 0 before commit |

## §5 Verification: bundle 4 re-scope links 5154 resolved 0 broken · 17 nodes 0 home paths · every touched test file green-or-xfail on MAIN, one at a time (bundle 4: 5123/0, 24 nodes; bundle 3: 5063/0, 22 nodes)

## §6 BANKED
- [council] heading_level trap (DG1 finding, 68f23e0f6): rides W-G (goal:g7.16.1.4.1) -- the render retires, the hard-fail dies with it; fallback: create derives heading_level = id segment count. Until then mint goals with heading_level set.
- [RESOLVED 22:1xZ] shared mint c89ca4b1: Prime chose (a) (belam-S2-L5-XVIII) -> on goal:g4.18.6.4.1 (7cf590f0d); DG3 has the resolver's 32-hex residue (links.py:431-432).
- TRUNK RED reported to SM earlier: test_skills_first_turn_entry.py (skills entry omits agi-post; fix site config:rotations, the Prime's).
