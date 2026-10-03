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

## §0 State (03:07Z 10-03) -- gen 8; AA1.C + home mode LANDED (a7705f2d2); key story = sp's §AB; nothing running, nothing pending
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
       10-02 20:0x-22:2xZ CLOSED: level rule accepted + LANDED 3a33c71b9 (council lands [], keep lands SM + TM-new; ack owed even on an accept) · rse-aa1-boxes
       carried byte-equal at a0bbc7202 · SM g7.16.1.11.13: skip AA3.4 item 1, keep grow-gate item 3 (+7 B)
       02:1xZ owner (via belam [owner] 01:5xZ): "everyone is waiting on someone else" -> council split (all-is-one 02:11Z, first to land):
       all-is-one = GRID + K2/K3 + flow rotation · self-perpetuating = K1 · alive = DG3 install + the roll-up
       A6 was ALSO on alive: act1.sh (sha 90cdb304) lived only in the old scratchpad -> alive/aa1m-act1 @bd3960e23 -> LANDED 9778def43 (verified)
       02:19Z belam took the roll-up: A1 A2 A4 A5 RAN (d57b52bd4); W -> DG1; K leaf = all-is-one; host acts = belam GO each as ONE line; relayed
       02:3xZ HOME MODE ruled (AA1, asked by all-is-one): homes stay 0755 until AA1.V's own-store switch (MAIN worktree-prune hazard at 0750; secrets
       already 0600/0700) -> node + merge-up alive/aa1-home-mode @3d35aa268 to SM; council told
       02:34Z belam: .17 (3)+(4) design -> split (alive 02:35Z, taken): alive = AA1.C in rse-aa1-boxes: per-node ring: cell read at R on CHANGED+DELETED
       nodes (10/10), anchor line restored WITH -c (6/6; RSE line without -c passes an evil merge), freshness AGI_FRESH_S (8/8; agi-land reuses it via grow-gate)
       02:40Z SM A3 order: ruled (3) key step BEFORE +agi-signers, rest after (measured: root-first = every generation U, keygen-first = G G G)
       02:37-02:54Z owner: ONE key story (LEAD sp, §AB; AA1.C = its ring column) + inputs: DAG checkpoints as trusted time (supersede AGI_FRESH_S) · drop-in crypto (AA1.C 0 literals)
       · layered blocks = signers pairwise a()-adjacent (levels 1 belam / 2 council+keep / 3 DGs+DT-1; top = belam + level 2)
       02:55Z sp folded AA1.C into §AB; alive's IN-OR-ABOVE escalation flag CLOSED 03:01Z (tree move ruled by old AND new parent; checked)
       03:0xZ LANDED a7705f2d2 (SM; verified: 25280db35 on trunk, AA1 node == my tree; A3.2 put the key step BEFORE +agi-signers, engine-root:33-34)
       03:12-15Z owner: provable revocation (5th input), POC on ROOT-READABLE keys; alive measured: GitHub reads v5 commits verified:false no_user;
       origin is PUBLIC-READABLE -> POC keys stay OFF every remote (belam ruled 03:17Z)
       03:17Z belam ACCEPTED the private-key gate line as its own round; alive then found 3 defects in its own 490 B line (RSA PEM passed, 2nd block
       unchecked, encrypted key HANG) -> AA1.K corrected 630 B 12/12; merge-up alive/aa1k @385dff5d2; belam + DG1 told: build from AA1.K
WAITS  SM lands alive/aa1k (send queued: pane busy, sweep retries); mail
```

## §2 Landed (AA1 node commits on posts/alive; the trunk takes them through SM's gate)
- doc:rse-aa1-boxes: AA1 8ddf79715 · AA1.V e06828689..f62efcfcf · AA1.R / L / T / W / F / M / level rule = later agi-turn commits (posts/alive tip at rotation)
- belam ACCEPTED: AA1 bundle -> DG1 · shell-tests [rule] · AA1.M + both deviations · the figure-eight edge (then SUPERSEDED by the level rule)

## 🔴 Where it stops
Idle on mail: everything of alive's is on the trunk (a7705f2d2); the key story is sp's (§AB); alive answers seams only.
```
next: AGI_POST=alive python3 extensions/agi/bin/send.py read alive (WHOLE output) -> act on that mail only
  -> the meter is /var/lib/agi/alive/bin/agi-meter (UserPromptSubmit); at the line: card whole, commit by path, touch ~/.fresh; kill $PPID
```

## §4 Traps
| trap | rule |
|---|---|
| MAIN is shared by every post | commit by exact path; never switch branches, stash or reset; `git diff --cached --name-only` = ONLY your path before a commit |
| a file a DG names as 'on alive' | it is a wait on YOU: scratchpads die with the session; commit it into the tree (cut on the trunk tip, F4), never leave it in /tmp |
| belam's [decision] that ACCEPTS | still ack: ONE [rule] line by send.py (gen 8 skipped it; belam chased the route at 20:09Z) |
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
| a heredoc for python with backticks or $; a send text with apostrophes | ALWAYS quoted (<<'EOF'), values by argv or env; build send texts in python (shell quoting broke 03:15Z) |

## §5 Verification: links 5,658 resolved / 0 broken (10-01 23:4xZ) · every AA1 scratch suite green at its last run (box 25/25, grid 19/19, flow 13/13, level 21/21 on trunk rows)

## §6 BANKED
| question | options | recommendation |
|---|---|---|
| none open for alive | -- | -- |

Paid-for path guard: never create `.agi/bin/snapshot-build-site.py` or `.agi/bin/render-context.py`; never recreate `.agi/context/kits/` or `.agi/context/plans/build-site.md`.

<!-- THOUGHT:BEGIN — authored, not derived; carried across regenerating scans. The reasoning behind THIS version. -->
alive gen 8, 02:13Z 10-03 (date -u): the owner's "everyone is waiting on someone else" was true of alive too: DG3's A6 row had named alive's act1.sh as BLOCKED since 23:0xZ and alive's card never carried it. Filed it as a one-file commit cut on the trunk tip (F4: a post-tree commit can carry .agi/keys), and said so in the roll-up. Stopped my own GRID measurement when all-is-one's split landed first; SM had already measured it.
<!-- THOUGHT:END -->
