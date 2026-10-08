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

## §0 State (03:10Z 10-08) -- gen 9; ONE merge-up at SM (alive/d1-nest 4538c62506 = doc:rse-d1-nest v3); A1b boot design REPLACED (agi-vstore) and sent to DG1 + belam
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
done   10-01/02 AA1 bundle (doc:rse-aa1-boxes: boxes, grid commit, stores, tests, one-shot/flow, M1 mail, the level rule) · level rule 3a33c71b9
       10-03 (all LANDED): act1.sh (DG3 A6) · home mode 0755 until own stores · AA1.C config ring + anchor (-> sp's §AB) · AA1.K private-key gate
       (AA3.15 option B) · rulings: A3 key step BEFORE +agi-signers · inputs to sp's §AB (checkpoints, drop-in crypto, layered blocks, revocation, sealer)
       10-07 after the CC pause (owner: continue; council split alive 14:40Z, taken): D1 = AA1.N recursive node nesting (ONE grid commit: tree +
       nest/<mint>, parents = members' tips; nest() 552 B; g7 = 1,330 nodes in one commit) + the TANGLE (goal chains: 457 nodes / 7.9% under >=2 top
       goals, 52% g6 x g7; overviews cover 1.8%) · grid.py seams G1-G3 (nest dropped next tick / version jump / no CAS) + tested 11-line fix -> goal g4.13.1
       · D4 pilot rows judged (slice DROP code; cccc.ts unread-count bug; belam-SSH wakes DROP; raw-shell = season 3) · ONE placement to DG1 (14:54Z) ->
       goals g4.13.1 -> .19 verify-as-v5 -> g3.8 metrics -> .20 box mail (DG3 builds in that order) · g3.8 DESIGN = AA1.S (one belam cron graph_metrics,
       success_metrics --line, nulls named, metrics.py refuses a root with no nodes/; formatter fix after DG2's lane: an absent key is NAMED)
       · belam's retired-key signing found (15:05Z) -> fixed by belam 15:5xZ (signer id f077dbc5 = sha256(row pubkey 31a98b62) checked)
       10-08 01:57Z belam [rule]: owner retires grid commit; 01:58Z CORRECTION (owner: "It's already decided"): NO new design, it runs on
       rse:82 + AA1.V (aa1-boxes:125) + AA3 (aa3-land:152) + g7.16.1.6:71; cites verified on trunk; acked 01:58Z ([rule], one line)
       10-08 02:02Z owner trajectory: town:local-maxxing '#### Engine rework trajectory' E1-E5 (a mover rewrites ITS row in place at landing)
       02:09Z D1 restated off the retiring grid: doc:rse-d1-nest (nest: subtree | list in the container's front matter; collapse = one one-node
       commit; history = one first-parent -M walk, 1.5 s; reader 2,415 B + 7/7 tests quoted whole) -> merge-up at SM; notes sent: belam,
       DG1 (retire g4.13.1), all-is-one (D3 rests on the grid ref), self-perpetuating (D2)
       02:11Z DG1 RETIRED g4.13.1 (rides d71b26a06e); mints the D1 leaf when rse-d1-nest is on the trunk (DG2 pytest first, DG3 builds)
       02:12Z v2 on sp's D2 ask: `nest: subtree` DESCENDS through nest-less members, stops (inclusive) at one with its own nest:; 8/8;
       tip 43755c0227 sent to SM, DG1, sp
       02:14Z sp: §AC restated on v2 (merge-up 18 7b8098104 at SM), nothing open · 02:18Z all-is-one: D3 v2 on D1; my 'you lifted v1'
       was WRONG (cmp equal to 43755c0227, 02:20Z); they added descend + stop cases, 11/11; -34 VOID, merge-up-35 7b16a7db4 cites v2
       02:4xZ SM RETURNED 43755c0227 (R1: links.py:772 is verdict-class, the nest check is NEW code; R2: walk missed nodes/ -> 12 not 13;
       --follow's 14th is a COPY into build/src-init.md) -> v3 4538c62506 (walk -- .agi/nodes nodes; inline lists; t_nest.py quoted, 10/10
       from the node's bytes) -> SM, DG1, all-is-one, sp · DG1 02:45Z: g4.13.1 is COMPLETE (not retired); node restated
       03:06Z DG1 asked for A1b's bytes + flagged agi-project's 2nd root sh -s -> 03:09Z SUPERSEDED my digest: it also missed data reads,
       and the install act hashes the same forgeable store. NEW = agi-vstore (756 B root-owned file beside agi-boot.service): file:// fetch of
       the pin into /run/agi-v.git (index-pack re-hashes; depth 1, blob:none, then the 26 .geometry + config.json blobs); GIT_DIR there for
       every root read; no new cell. Fixture V1-V5 + forged tree refused; real MAIN 0.18 s / 804 KB, bytes == MAIN. (The mail says 'tested
       03:1xZ': it was ~03:08Z.) Bytes live ONLY in DG1's + belam's inbox mail; scratch bootd/ dies with this session
       02:10Z E4 answer to belam (now superseded by agi-vstore): boot hash = AGI_BOOT_SHA256 in carry.env, capture once/hash/run (392 B, dash-tested: forged loose blob
       refused = RA8 closed); external attestation = the LATER digest mover, never a boot dependency
NEXT   successor: read mail (WHOLE output) and act on that only. Nothing to build: DG3 builds g4.13.1 -> .19 -> g3.8 -> .20; alive answers design seams
WAITS  none of alive's. Banked (belam/alive): crons.md duplicate YAML key is silently last-wins for every job (DG2 g3.8 lane)
```

## §2 Landed (each verified with merge-base --is-ancestor; while origin pushes fail, check refs/heads/local-maxxing/season2/main)
- 10-02: 3a33c71b9 level rule · 10-03: 9778def43 act1.sh · a7705f2d2 home mode + AA1.C · ba2a399d6 / 21629a697 / 1b4fdbe13 AA1.K
- 10-07: 5a1760e82 AA1.N + grid seams · 0b95e3bd8 AA1.S · 01fb4669a3 AA1.S formatter fix (alive/aa1s-fix 967e250cc)

## 🔴 Where it stops
Waiting on SM to land alive/d1-nest tip 4538c62506 (3 commits, 1 file; sp mu18 + all-is-one mu35 land with it); when it lands, rewrite trajectory row E1 on town:local-maxxing in place (D1 = doc:rse-d1-nest + the landing sha; D2 stays self-perpetuating's). No scratch needed: the reader + tests are quoted whole in the node.
```
successor: read this card -> AGI_POST=alive python3 extensions/agi/bin/send.py read alive (WHOLE output) -> act on that mail only
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
| the live grid | refs/grid/local-maxxing/node/<mint> (refs/grid/node/* is frozen 09-21, ~2,000 short); version counts must read --first-parent |
| grid.py commit --all as a v5 uid | PermissionError on .grid.lock: version by PATH (`grid.py commit .agi/nodes/doc/<node>.md`) |
| AGI_TRUNK is set in this unit | a scratch test inherits it: export AGI_TRUNK=HEAD in fixtures |
| a check run as yourself over root-owned paths | "Permission denied" is not "absent" |
| scratch | the session scratchpad holds box/ (25-case suite), grid/, flow/, level/, fig8/, act1/; none of it is needed to resume |
| .agi/sessions/quorum/alive.md | a SYMLINK to this node (re-link at wake if rotate flattens it: agi-rotate §3) |
| a merge-up tip that MOVES | cc EVERY post that may have read the old tip, not only the ones that asked (02:18Z: I ASSUMED all-is-one lifted v1; it had v2. Ask for the cmp, do not assert) |
| a heredoc for python with backticks or $; a send text with apostrophes | ALWAYS quoted (<<'EOF'), values by argv or env; build send texts in python (shell quoting broke 03:15Z) |

## §5 Verification: links 5,658 resolved / 0 broken (10-01 23:4xZ) · every AA1 scratch suite green at its last run (box 25/25, grid 19/19, flow 13/13, level 21/21 on trunk rows)

## §6 BANKED
| question | options | recommendation |
|---|---|---|
| none open for alive | -- | -- |

Paid-for path guard: never create `.agi/bin/snapshot-build-site.py` or `.agi/bin/render-context.py`; never recreate `.agi/context/kits/` or `.agi/context/plans/build-site.md`.

<!-- THOUGHT:BEGIN — authored, not derived; carried across regenerating scans. The reasoning behind THIS version. -->
alive gen 9, 02:11Z 10-08 (date -u): the trajectory ask made E1 D1 alive's open work; D1 had landed but on the grid E2 retires, so it was restated (doc:rse-d1-nest) and cut as a one-node merge-up. belam's E4 question was weighed by test, not taste: an in-box digest closes RA8, the external source only moves the digest.
<!-- THOUGHT:END -->
