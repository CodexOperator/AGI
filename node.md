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

## §0 State (16:5xZ 09-29 — RESUMED by belam on the owner's word, until 23:00Z)
| | |
|---|---|
| post | director-general-2 · gen 2 · session agi-40 (@7) · re-seated 17:34 Z after the 17:33Z crash-recovery respawn |
| stage | bundle 3 stage 2 (experiments + verdicts + the tests they need) IN FLIGHT since 17:55Z |
| protocol | doc:council-loop (read it first) · goal:g7.16.1 (the owner's words) |
| place | local-town · MAIN /data/work/agi on local-maxxing/season2/main · claude-code Opus 5.5 high |
| skills | agi-node-write · agi-verify · agi-send · agi-rotate · agi-post |
| bundle | 1 closed · 2 stage 2 DONE 402a9187c + residues 42 · 43 · 44 CLOSED (sanctuary-master ack at b593b296f): nothing owed by DG2 |

## §1 Plan
```
done     bundle 1 + bundle 2 stage 2 + residues (all CLOSED)
now      bundle 3 (goal:g7.16.1.3) stage 2 -- DG1 handoff 9181cee26 (17:53Z): 9 hypotheses
         H1 adopt gate · H2 key row · H3 row parks · H4f grep error (FIRST in H4) · H4p1 shared module
         H4b home scrub · H4g seating transcript · S1 dm family (measure) · S2 core unwired five (verdict)
how      6 read-only measurement agents -> drafts in /tmp/dg2b3/<key>/ (experiment.md, verdict.md, tests.patch)
         -> I review, mint experiment:dg2-<key>-* + verdict:dg2-<key>-*, apply the strict-xfail rows,
            ONE test file per run, commit by exact path -> [handoff] to director-general-3
rule     PASS B3 on this box: single test files only · at 23:00Z: finish the step, card whole, idle
```

## §2 Landed (bundle 3 stage 2 -- 9 of 11 rows; R1 + R2 measuring)
- 46077247b H1 lean90 (kid adopt mints; 6-line gate call) · 25aba7ebc H2 lean80 (insert lands after trailing keys: lone row + unloadable file)
- f4de8103f H4p1 lean75 (9 grep lines not 8; _grep_live must go public) · H4g lean90
- 65576ac93 S1 proved = VERDICT not FOLD (routes 3 -> 3) · S2 proved (25/25 core tests, 0 callers, nothing ported)
- b8646c6fc H3 lean85 (39 rows / 5 carriers; tags BEFORE the rule) · H4f lean85 (exit 128 fails OPEN; no-repo case unreachable)
- 30329d8a7 H4b lean80 (415 files, 7 rounds; CORRECTION: write.py has no home refusal)
- R (goal:g6.41.1, after H4g before S1): R1 v2 014912b17 dummy cutover on dg2-r-dummy-* units only · R2 PSI admission
  NEVER claude-remote-control.service / the live tmux server; live cutover = owner's word after PASS B3 (doc:card-belam §6)

## §2b Landed (bundle 2)
- 145f77e2f R1 experiment + verdict:dg2-r1-rotation-home (lean80) + test_rotation_record_home.py (DG3 built R1 b9a4ca508 + d25e78e81)
- 8d2802ed9 R3 verdict:dg2-r3-generic-home (lean75) + row; R1 addendum (another box's home in 323 records -> one generic pattern)
- d60c54e7f R5 (lean85, + a green switch pin) · P (lean70, count gate 12) · M (lean90) · T (lean70, local-town unmapped) + 4 strict-xfail rows
- af4f50b3a R2: PARKING TEST on THE TRIAGE RULE; reap-chain + model-fence keep; pass10 17/12/1
- b593b296f residue 44: empty-provider + zero-usd-lane re-parked (tag), 6 why fixes; tagged parks = 8 (7 hyps + g7.32.5), 0 THOUGHT marks
- 697335c7c residue 43: parked:g7.16.2 dropped from the 6 re-marked nodes; tagged parks = 6
- 391a36a5c residue 42 (mur wf_dde8f806-ce2): PARKING TEST over all 11 parks -> 5 keep · 1 retired · 5 parked; post-audit parks = 6 (P's gate)
- 402a9187c R4: .2.1 F1 anchored · .2/.2.1/.2.2 complete · 26 -> 24 · 3 doubled ENDs collapsed · g4.18.1 falsifier output in body
- bundle 1: 951056229 · 53ab755d4 · 6ff0e0aa1 · 3e0e340cb · e008169dc

## 🔴 Where it stops
18:0xZ 09-29: bundle 3 stage 2 IN FLIGHT. Drafts land in /tmp/dg2b3/<key>/ (BRIEF.md there). If this seat died: read each
report.txt, re-run any missing key from BRIEF.md, then mint + commit per §1 `how`. Inbox:
```
python3 extensions/agi/bin/send.py --from director-general-2 read director-general-2
```

## §4 Traps
| trap | rule |
|---|---|
| MAIN is shared by every post; another post's in-flight edits sit in it | commit by exact path; check `git diff --cached --name-only` count before commit; never switch branches, stash or reset |
| a lock check that only PRINTS the lock does not stop the commit (8d2802ed9 went in under a live suite lock) | gate every MAIN write/commit: `[ ! -e .agi/sessions/verify-suite.lock ] && ...` |
| `grep -r` / `find` over .agi/ or the repo root io-stalls the box | `git grep PATTERN -- <paths>` |
| a node quoting `/home/<name>/` trips R3's falsifier; a marker quote with its html-comment open counts under old detectors | write `<home>/`, `/home/<x>/`, "the BEGIN marker" |
| the test file loads anonymize via `_load` per import | probe a revert by calling the test function on the patched module, not via pytest.main |
| the harness clock, not a guess | stamp nodes from `date -u` |
| a peer session name dies with its rotation | ListAgents first; else `send.py --from director-general-2 send --to <seat> <body>` (durable) |

## §5 Verification: links 0 broken (4995) · `snapshot-goals.py --render --check` rc 0 · touched tests 120 passed, 7 skipped, 5 xfailed (bundle 2 rows)

## §6 BANKED
(none) · TRUNK RED reported to SM: test_skills_first_turn_entry.py (the skills entry omits agi-post; fix site config:rotations, the Prime's) · findings for a later bundle: 87 nodes carry the repo path · the writer stamps town: core for local-town posts · 8 nodes carry a surplus column-0 THOUGHT END (fence-gap quotations) · R3 reach outside its scopes (52 context · 32 comms · 22 engine files)

Paid-for path guard: never create `.agi/bin/snapshot-build-site.py` or `.agi/bin/render-context.py`; never recreate `.agi/context/kits/` or `.agi/context/plans/build-site.md`.
