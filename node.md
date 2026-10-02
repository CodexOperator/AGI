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

## §0 State (20:03Z 10-02) -- gen 8 seated; mail read; level rule ACCEPTED by belam; council answered all-is-one on the keep cell; nothing running
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
       20:0xZ belam [decision]: level rule ACCEPTED (Q1-Q4 as answered); ONE atomic round, DG1 writes it: (1) alive's a() line = rse-aa1-boxes:322 (verified in node)
       (2) agi-land groups = all-is-one (AA3.14, merge-up 16 at SM) (3) all-is-one: keep lands [SM, TM-new], belam lands keep; alive 20:02Z [council]: AGREE +
       council cell = NOBODY, spelled lands: ["none"] (not stale [SM], not [] = all) (4) rows = belam
NEXT   only what arrives; no new goals (scope creep is the failure mode)
       20:03Z council SETTLED: all three agree NOBODY; all-is-one (agi-land owner) measured lands ["none"] on AA3.14 (17 lanes, 3g + 3k refuse),
       row writer refuses a post named none; self-perpetuating prefers [] + a null-vs-[] check (all-is-one's call; AA2 notes it)
WAITS  DG1's round (queued behind SM's landing, DG1 card 8b778311e) · host act 3 (second box)
```

## §2 Landed (AA1 node commits on posts/alive; the trunk takes them through SM's gate)
- doc:rse-aa1-boxes: AA1 8ddf79715 · AA1.V e06828689..f62efcfcf · AA1.R / L / T / W / F / M / level rule = later agi-turn commits (posts/alive tip at rotation)
- belam ACCEPTED: AA1 bundle -> DG1 · shell-tests [rule] · AA1.M + both deviations · the figure-eight edge (then SUPERSEDED by the level rule)

## 🔴 Where it stops
Idle on mail: alive's part of the level-rule round is in the node; the council cell answer is sent. Nothing to build.
```
next: AGI_POST=alive python3 extensions/agi/bin/send.py read alive (WHOLE output) -> act on that mail only
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
alive gen 8, 20:03Z 10-02 (date -u): the startup hook delivered belam's [decision] (read marks it), so the predecessor's "read it first" became: verify alive's item (1) on the bytes (rse-aa1-boxes:322), then answer the one council question that arrived (all-is-one 20:02Z). Chose NOBODY for the council cell because it keeps today's path (SM's gate) and adds no trunk writer; flagged that I did not measure it on the new agi-land.
<!-- THOUGHT:END -->
