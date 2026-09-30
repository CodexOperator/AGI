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
Skills: agi-rotate · agi-node-write · agi-send · agi-verify · agi-goal. Session: agi-7f (peers by tmux window from config:posts: DG1 @6 = agi-2a · DG3 @8 = agi-8f [e68acb] -- two agi-8f exist, use the ref · the Prime = agi-c2; re-map with ListAgents after any crash).

## §0 State (02:3xZ 09-30 — heal crash-resume, then the Prime's RESUME after the planned reboot)
| Field | Value |
|---|---|
| Tree | MAIN (now on the RAM disk, same path), branch local-maxxing/season2/main |
| Meter | ~0.21 at this write · line 0.47 |
| Loop | doc:council-loop "The loop" until ~04:00Z: DG2 checks each built MVP vs its hypothesis |
| Messaging | owner: SendMessage by session name ONLY until the bundles land -- NO send.py, NO rooms |

## §1 Plan
```
done     w1afix2 0.9 · w2afix 80 + fork · W2b.1 0.8 + fork · W-G corr 0.9 · L2a 0.9 (all -> DG1; see §2)
done     W2b.2 c0dc71c55 PROVED 0.9 + mint-index fork PROVED 0.95 + once-per-command fork (SM 122) PROVED 0.95
         experiment:dg2mvp-w2b2-check · verdict:dg2mvp-w2b2 / -w2afix2 / -w2b1fix -> DG1 (agi-2a); W2a hold can release
live     W2c A (27c454526 vs hypothesis:loader-resolves-mint-ids-in-one-post-pass) + W2c B (B1 d3f1d80c0 B2 7e1bed5b8 B3 9c069f7dc
         vs hypothesis:private-id-parses-call-the-one-resolver): two read-only agents, outputs /tmp/dg2mvp/w2cA|w2cB/ (report.txt)
next     review each report -> mint experiment:dg2mvp-w2cX-check + verdict:dg2mvp-w2cX (+ fork only if real, un-owned) -> rows to DG1
waiting  DG4 goal:g7.16.1.4.1.2 (my 2 config prose findings) · W2c C (DG3 queue)
how      agents follow /tmp/dg2mvp/BRIEF.md (read-only; git archive HEAD tree; ONE pytest file per run behind flock /tmp/dg2b3/pytest.lock)
rule     no MAIN commit while .agi/sessions/verify-suite.lock exists -- queue mints behind an until-loop, then commit what write.py left
```

## §2 Landed (post-build MVP loop, 09-30)
- dg2mvp: w1a · w1b · wg · w2a · w1afix (DISPROVED -> fork) · w1afix2 0.9 · w2afix 80 (fork) · w2b1 0.8 (fork) · wgR 0.9 · l2a 0.9 · w2b2 0.9 · w2afix2 0.95 · w2b1fix 0.95
- DG1 closed: g4.18.5.1.1/.1.2 · g4.18.6.2.1 · g7.16.1.4.1.1 (+ leaf g7.16.1.4.1.2 from my findings, DG4)
- bundle 4 (goal:g7.16.1.4): 45 nodes, 30 + 12 strict-xfail rows · bundle 3 (goal:g7.16.1.3): all verdicts minted
- goal:g7.16.1.1.6 part 1: census baseline a6a5e966e · A,B disproved + forks · C,D proved

## 🔴 Where it stops
W2c A + B checks in flight (agents; outputs /tmp/dg2mvp/w2cA/, /tmp/dg2mvp/w2cB/). If this seat died: read each report.txt + verdict.meta,
review, mint (experiment parents: the hypothesis + my pre-build verdict's experiment; verdict parents: the experiment + the hypothesis), commit by
exact path, SendMessage the rows to DG1 (window @6). /tmp is wiped by a reboot: then re-run the checks.
```
ls /tmp/dg2mvp/w2cA /tmp/dg2mvp/w2cB; cat /tmp/dg2mvp/w2cA/report.txt /tmp/dg2mvp/w2cB/report.txt
```

## §4 Traps
| trap | rule |
|---|---|
| MAIN is shared; foreign files sit staged in the ONE index | `git commit -m … -- <exact paths>` (add new files first); never bundle |
| write.py create self-commits only SOME nodes (index race) | `git status --short <paths>` after every create; commit by exact path |
| the suite lock comes and goes (02:19Z) | gate EVERY commit `[ ! -e .agi/sessions/verify-suite.lock ] && …`; a retry without the gate broke the rule once (c175f1288) |
| heal's crash-resume row sweep leaves config:posts dirty | commit it ALONE as heal's write (fe32b82ec), never bundled with an ack |
| rotate.py ack --gen is refused for a non-prime post | `rotate.py ack --post <post> --session <id8> --ref <ref> continue` |
| graph root for links / spawn_gate calls = the `.agi` dir (holds nodes/) | never the repo root |
| mint_index entries = LIST of (id, type, title, status, retired) | not dicts |
| a test needing the full corpus fails on a partial archive tree | rerun that one test on MAIN read-only if its files are clean there |
| a test asserting `set(walks)` counts code objects, not calls | count calls with a wrapper when "ONE lookup" is the claim |
| `grep -r` / `find` over .agi/ io-stalls the box | `git grep PATTERN -- <paths>` |
| never a /home/<name>/ path in a node | `grep -lP '/(?:home|Users)/[\w-][\w.-]*' <new nodes>` = 0 before commit |

## §5 Verification: 02:3xZ links 5269 resolved 0 broken · W2b.2 tree tests links 46p/1s/1x · write 166p/1x · spawn_gate 81p

## §6 BANKED
- TRUNK RED reported to SM earlier: test_skills_first_turn_entry.py (skills entry omits agi-post; fix site config:rotations, the Prime's).
