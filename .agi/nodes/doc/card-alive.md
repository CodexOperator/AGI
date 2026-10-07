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

## §0 State (14:55Z 10-07) -- gen 8; owner relays 14:3x/14:4xZ: D1 nesting DONE (AA1.N at SM), D4 rows judged, placement sent to DG1; metrics = alive's
| | |
|---|---|
| post | alive · council (members <- council (inert) <- belam) · v5 (claude-code, opus-5-5) · meter = /var/lib/agi/alive/bin/agi-meter at 47 pct |
| work | the council's design bundle: AA1 = alive's node `doc:rse-aa1-boxes` (boxes, versioning, stores, tests, flows, M1 mail, the level rule) · AA2 = self-perpetuating in doc:radically-simple-engine · AA3 + Z4 = all-is-one (doc:rse-aa3-land, doc:rse-z4-ladder-out) · DG1 turns them into goals; DG3 builds; SM gates |
| messaging | ONE route: `send.py --from alive send <post> '[tag] ...'`. To belam: [merge-up] [decision] [rotation] [red] [rule] [complete] [owner]; an ack = ONE [rule] line. Never SendMessage to a session name. No answer in 15 min = re-send ONCE (goal:g1.40) |
| reading | `send.py read alive` prints ONLY new blocks and marks them: read its WHOLE output, never filter it |
| council | split each owner line by mechanism owned; when splits cross, the first to LAND (inbox ts) stands |
| lens | vision:alive = the system reports its own TRUE state (measure, then say it; correct your own claims at once) |
| skills | agi-send · agi-rotate · agi-goal · agi-post · NODES = plain Read/Edit/Write + agi-turn's commit + `grid.py commit <path>` (write.py = old setup only) |

## §1 Plan
```
done   10-01/02 AA1 bundle in doc:rse-aa1-boxes (boxes, grid commit, stores, tests, one-shot/flow, M1 mail, the level rule; ACCEPTED) · level rule LANDED 3a33c71b9
       10-03 (all LANDED, verified on the trunk): act1.sh for DG3's A6 (9778def43) · HOME MODE: homes stay 0755 until AA1.V's own-store switch
       (a7705f2d2) · AA1.C v5 config ring + anchor line WITH -c (a7705f2d2; folded by sp into §AB) · AA1.K private-key gate (ba2a399d6, 21629a697)
       rulings given: A3 key step BEFORE +agi-signers (measured U U U vs G G G; built A3.2) · council lands [] · DG3 install waits = belam GOs
       inputs to sp's ONE key section §AB (owner 02:37-03:26Z, sp leads): DAG checkpoints, drop-in crypto, layered blocks = signers pairwise
       a()-adjacent, provable revocation (POC root-readable keys, OFF every remote), GitHub attestations sealer (master schedule; AGI_SUBJECT recipe)
       corrections alive owned: 490 B key line had 3 defects; told DG1 a line was in AA3.15 before it was; sp's IN-OR-ABOVE escalation (closed)
       10-07 owner (belam 14:40Z): nest graph slices into nodes for rollover; council split (alive 14:40Z, taken): alive D1 + tangle · sp D2 · aio D3 + lead D4
       D1 = AA1.N (merge-up alive/aa1n @5cc55defa at SM): collapse = ONE grid commit, tree + nest/<mint>, parents = members' tips; nest() 552 B;
       116/116, 2 levels, g7 = 1,330 in one commit; flat side F1 = grid-only + members retire at rollover (74 flat readers). TANGLE: overviews 1.8%;
       goal chains 457 (7.9%) under >=2 top goals, 52% g6 x g7. LIVE grid = refs/grid/local-maxxing/node/* (refs/grid/node/* frozen 09-21)
       D4 rows judged 14:48Z (slice DROP code/ADAPT ideas; cccc.ts unread-count bug; belam-SSH wakes DROP; raw-shell = season 3)
       14:45Z owner: old Python kept (keys/metrics/verify), metrics back on, .17 restated -> ONE placement to DG1 14:54Z (metrics: works, nothing runs it)
       15:00Z aio found G1 (nest/ dropped next tick) + G2 (version jump); alive found G3 (lost update, no CAS) -> 11-line grid.py fix tested in AA1.N;
       added to DG1's placement as a Python build (D3 legacy marker depends on it)
NEXT   mail only; if DG1 writes a metrics goal: design the ONE belam cron (metrics.py + success_metrics.py -> town line) + metrics.py refuse-on-no-nodes
WAITS  SM lands alive/aa1n · DG1's goals from the placement
```

## §2 Landed (on local-maxxing/season2/main, each verified with merge-base --is-ancestor)
- 10-02: level rule 3a33c71b9 (rse-aa1-boxes byte-equal at a0bbc7202) · 10-03: 9778def43 act1.sh · a7705f2d2 home mode + AA1.C + seams ·
  ba2a399d6 AA1.K + per-commit line · 21629a697 AA1.K -> AA3.15 · 1b4fdbe13 AA1.K -> option B
- belam ACCEPTED: AA1 bundle -> DG1 · AA1.M · the level rule · the private-key gate as its own round (03:17Z)

## 🔴 Where it stops
Idle on mail: AA1.N at SM; placement with DG1. Scratch nest/ + d4/ hold the D1/D4 working files; nothing needed to resume (all in AA1.N + mail).
```
next: AGI_POST=alive python3 extensions/agi/bin/send.py read alive (WHOLE output) -> act on that mail only
  -> a merge-up = ONE node, cut on the trunk tip with plumbing (read-tree T; update-index; commit-tree -S -p T), branch alive/<name>, [merge-up] to SM
  -> the meter is /var/lib/agi/alive/bin/agi-meter (UserPromptSubmit); at the line: card whole, commit by path, touch ~/.fresh; kill $PPID
```

## §4 Traps
| trap | rule |
|---|---|
| MAIN is shared by every post | commit by exact path; never switch branches, stash or reset; `git diff --cached --name-only` = ONLY your path before a commit |
| a file a DG names as 'on alive' | it is a wait on YOU: scratchpads die with the session; commit it into the tree (cut on the trunk tip, F4), never leave it in /tmp |
| belam's [decision] that ACCEPTS | still ack: ONE [rule] line by send.py (gen 8 skipped it; belam chased the route at 20:09Z) |
| a message that says "it is in the node" / "it is in X's node" | WRITE + VERIFY the node first (grep -F the line), THEN send (missed twice 10-02: 19:4xZ, 19:5xZ) |
| a python f-string around shell code with `{` (`a(){`) | SyntaxError: build doc text by concatenation |
| a sed rewrite of a script | it mangled box send and the flow runner once each: edit by python on whole lines, then re-run the suite |
| send.py read with a filter | an awk filter hid belam's [owner] 14:01Z and the read marked it; read the whole output |
| grep with `$` in a pattern | it is an anchor: use grep -F for literal code |
| my timestamps | a time I write = date -u in the same step; a PAST event = git log -1 --format=%cI <sha> |
| a relay says "the owner said X" | verify on the bytes (a signed inbox block, a node) before spending; a STOP needs no proof |
| grep -r / find over .agi/ or the repo root | stalls the box: `git grep PATTERN -- <paths>` |
| grid.py commit --all as a v5 uid | PermissionError on .grid.lock: version by PATH (`grid.py commit .agi/nodes/doc/<node>.md`) |
| AGI_TRUNK is set in this unit | a scratch test inherits it: export AGI_TRUNK=HEAD in fixtures |
| a check run as yourself over root-owned paths | "Permission denied" is not "absent" |
| scratch | the session scratchpad holds box/ (25-case suite), grid/, flow/, level/, fig8/, act1/; none of it is needed to resume |
| .agi/sessions/quorum/alive.md | a SYMLINK to this node (re-link at wake if rotate flattens it: agi-rotate §3) |
| a heredoc for python with backticks or $; a send text with apostrophes | ALWAYS quoted (<<'EOF'), values by argv or env; build send texts in python (shell quoting broke 03:15Z) |

## §5 Verification: links 5,658 resolved / 0 broken (10-01 23:4xZ) · every AA1 scratch suite green at its last run (box 25/25, grid 19/19, flow 13/13, level 21/21 on trunk rows)

## §6 BANKED
| question | options | recommendation |
|---|---|---|
| none open for alive | -- | -- |

Paid-for path guard: never create `.agi/bin/snapshot-build-site.py` or `.agi/bin/render-context.py`; never recreate `.agi/context/kits/` or `.agi/context/plans/build-site.md`.

<!-- THOUGHT:BEGIN — authored, not derived; carried across regenerating scans. The reasoning behind THIS version. -->
alive gen 8, 06:04Z 10-03 (date -u): whole rewrite for the CC-usage pause (owner via belam 06:0xZ: "if you can't rotate on new system in the next couple hours it'll have to wait till next week"). §1 collapses the 10-03 log into what landed, what was ruled, what went to sp's §AB, and the corrections alive owned; the full record is in doc:rse-aa1-boxes, sp's §AB, the trunk and git. One merge-up is left at SM; nothing else is open.
<!-- THOUGHT:END -->
