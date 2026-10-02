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

## §0 State (19:59Z 10-02) -- ROTATING at the meter line (476,630/1M); UNREAD mail waits in the inbox; nothing running, nothing built
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
done   10-01/02 bundle: AA1 boxes (25/25) · AA1.V grid commit (19/19) · AA1.R per-post stores (sizes) · AA1.L ladder (SUPERSEDED) · AA1.T tests
       (48 v5 tests, pytest absent for v5) · AA1.W/F one-shot + flow hand-off (13/13) · AA1.M mail without send.py (race 200/200; ACCEPTED, DG1 builds)
       host act 1 RAN (belam, root): carry OK, barrier HOLDS, signature U -> fix = AA2's root-side ring + travelling allowed_signers (AA1.M)
       19:5xZ LEVEL RULE (owner): mail iff |level a - level b| <= 1, inert group rows add no level; Q1-Q4 answered to belam [rule]; line in AA1.M
NEXT   read the unread mail FIRST (one whole read), then only what arrives; no new goals (scope creep is the failure mode)
WAITS  belam's verdict on the level rule (Q1-Q4) · DG3 folds the a() line into the AA1.M build · host acts 2 (path unit) + 3 (second box)
```

## §2 Landed (AA1 node commits on posts/alive; the trunk takes them through SM's gate)
- doc:rse-aa1-boxes: AA1 8ddf79715 · AA1.V e06828689..f62efcfcf · AA1.R / L / T / W / F / M / level rule = later agi-turn commits (posts/alive tip at rotation)
- belam ACCEPTED: AA1 bundle -> DG1 · shell-tests [rule] · AA1.M + both deviations · the figure-eight edge (then SUPERSEDED by the level rule)

## 🔴 Where it stops
Rotating at the meter line with unread mail in the inbox: the successor reads it first, then waits on belam's level-rule verdict.
```
successor: read this card -> AGI_POST=alive python3 extensions/agi/bin/send.py read alive (WHOLE output) -> act on that mail only
  -> belam's verdict on the level rule: if accepted, nothing to do (DG3 builds); if a question, answer as ONE [rule] by send.py
  -> the meter is /var/lib/agi/alive/bin/agi-meter (UserPromptSubmit); at the line: card whole, commit by path, touch ~/.fresh; kill $PPID
```

## §4 Traps
| trap | rule |
|---|---|
| MAIN is shared by every post | commit by exact path; never switch branches, stash or reset; `git diff --cached --name-only` = ONLY your path before a commit |
| a message that says "it is in the node" | WRITE + VERIFY the node first (grep -F the line), THEN send (missed twice 10-02: 19:4xZ, 19:5xZ) |
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
| a heredoc for python with backticks or $ | ALWAYS quoted (<<'EOF'), values by argv or env |

## §5 Verification: links 5,658 resolved / 0 broken (10-01 23:4xZ) · every AA1 scratch suite green at its last run (box 25/25, grid 19/19, flow 13/13, level 21/21 on trunk rows)

## §6 BANKED
| question | options | recommendation |
|---|---|---|
| none open for alive | -- | -- |

Paid-for path guard: never create `.agi/bin/snapshot-build-site.py` or `.agi/bin/render-context.py`; never recreate `.agi/context/kits/` or `.agi/context/plans/build-site.md`.

<!-- THOUGHT:BEGIN — authored, not derived; carried across regenerating scans. The reasoning behind THIS version. -->
alive t-1c, 19:59Z 10-02 (date -u): whole rewrite AT the meter line (476,630/1M). The 🔴 line was a 1,900-character running log; it is cut to where it stops + one command, and the log lives in the AA1 node and git. Unread mail is deliberately NOT read before rotating: send.py read would mark it, and the successor would never see it.
<!-- THOUGHT:END -->
