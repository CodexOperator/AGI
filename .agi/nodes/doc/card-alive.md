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
tags: []
title: Card alive
town: core
---
# doc:card-alive — alive's card (council loop, goal:g7.16.1): the ONE scratch

Replaced whole, never appended; ≤ 100 lines; written DURING the work so a dead session is resumable.

## §0 State (22:0xZ 10-10) -- gen 10 on encryption-town; NEW ROLE: council rules + approves gated tips (belam [rule] 22:0xZ, owner 21:5xZ)
| | |
|---|---|
| post | alive · council (members <- council (inert) <- belam) · v5 (claude-code, opus-5-5) · moving local-town -> encryption-town (owner 21:2xZ) |
| work | the council's design bundle. alive = AA1 (`doc:rse-aa1-boxes`) + D1 (`doc:rse-d1-nest`) + A1b's design (agi-vstore). sp = AA2/§AB/§AC (doc:radically-simple-engine) · all-is-one = AA3, Z4, D3, D4 · DG1 goals, DG2 falsifiers, DG3/DG4 build, SM gates |
| messaging | BOX ONLY (owner via SM [rule] 04:5xZ 10-09): `printf '%s\n' '[tag] ...' \| AGI_POST=alive ~/bin/box send <post>`; read `AGI_POST=alive box read` (`box n` = unread). NO send.py send, NO inbox .md, NO SendMessage. No answer = tell belam by box, never fall back |
| reading | `box read` prints and marks (refs/held/alive/*): read its WHOLE output; refs live in MAIN's git dir (shared by every post's worktree) |
| council | doc:council-loop §Rulings and landing: SM box [review <sha>] -> council group chat BY BOX (alive · all-is-one · self-perpetuating) -> ONE answers SM [approve <sha>] / [return <sha>: why]; split -> belam ties. Every [decision] comes to us, never belam. Answerer = first addressee, alive when SM sends to all three; others agree/object in 15 min. Rule top-down through vision:alive: SM did the byte gate |
| lens | vision:alive = the system reports its own TRUE state (measure, then say it; correct your own claims at once) |
| skills | agi-send · agi-rotate · agi-goal · agi-post · NODES = plain Read/Edit/Write + commit by path + `grid.py commit <path>` (write.py = old setup only) |

## §1 Plan
```
done   10-01..03 AA1 bundle + level rule + act1.sh + home mode + AA1.C ring/anchor + AA1.K key gate (all landed, §2)
       10-07 AA1.N nesting + tangle (457 / 5,813 nodes under >= 2 top goals) · AA1.S stats design (g3.8) + formatter fix
       10-08 E1 D1 RESTATED OFF THE GRID (grid commit retires, E2; owner "already decided"): doc:rse-d1-nest v3 LANDED 38986aa967.
             A slice = `nest: subtree | [ids]` in the container's front matter; subtree DESCENDS through nest-less members, stops
             (inclusive) at one with its own nest:; collapse = ONE one-node commit; history = one `git log --first-parent -M -- .agi/nodes
             nodes` walk (1.5 s); reader nest.py 3,034 B + t_nest.py 10/10 quoted WHOLE in the node. D2 §AC e92d251390 + D3 v2 05ccc3e20b
             landed on it; E1 row = SM's da90062217. goal:g4.13.1 = COMPLETE (DG1), not retired.
       10-08 A1b (RA8: root ran bytes from an agi-writable object store): my 02:10Z digest SUPERSEDED (missed agi-project + data reads;
             the install hash reads the same forgeable store) -> agi-vstore: root fetches the pin over file:// into a root-owned RAM store
             (index-pack re-hashes every object), all root reads via GIT_DIR, no new carry.env cell. Amended per belam 04:4xZ: the child
             upload-pack trusts ONLY MAIN's gitdir (-c safe.directory=$G, $M/.git non-bare | $M bare; never '*'), store built at $V.n and
             renamed on success. 856 B sha256 f60191fd12942280569156cc2308e3ab4ec0c82cbb366676d50e77717b2d1fcc. LANDED in A1b v3
             eb55f973e2 (engine-root.md piece + agi-vstore.t.sh, DG2 47/47 on the reference). Pin attestation = season-3 AUDIT only.
NEXT   successor: read mail (WHOLE output), act on that only. Builds are DG-owned: D1 = DG1 leaf -> DG2 t_nest.py -> DG3 nest.py +
       links.py nest_unresolved + optional nest field; A1b host act = belam's (install agi-vstore BEFORE the new agi-boot.service)
WAITS  none of alive's. Banked (belam/alive): crons.md duplicate YAML key is silently last-wins for every job (DG2 g3.8 lane)
```

## §2 Landed (verify with merge-base --is-ancestor against the fetched trunk local-maxxing/season2/main)
- 10-02: 3a33c71b9 level rule · 10-03: 9778def43 act1.sh · a7705f2d2 home mode + AA1.C · ba2a399d6 / 21629a697 / 1b4fdbe13 AA1.K
- 10-07: 5a1760e82 AA1.N + grid seams · 0b95e3bd8 AA1.S · 01fb4669a3 AA1.S formatter fix
- 10-08: 38986aa967 doc:rse-d1-nest v3 (D1) · eb55f973e2 A1b v3 (DG3 build of agi-vstore, 856 B f60191fd...)

## 🔴 Where it stops
Council queue (22:1xZ 10-10). Answerer = first addressee; SM to all three = alive; others agree/object in 15 min.
- 10-10/11 approved 3/3 (remarks in box + git log of this card): 7ac20cd62a (sp) · 107388a1b1 · cd0aa3d261 · 0d980eaa5e · 5504d4e6f6 · d50c519dde · c2c50e818b · 80a193ae73 · c6f2d759a5 · 8d47f62519 · 889a29eec4 (.37 v1; 5 remarks folded by 0a8aa43672) · 0a8aa43672 (.37 v2 + 4 loop-end outcomes -> .38/.39) · residue: box-wake.t.sh 14-15 FAIL at load 52, want DG4's cool number || 10-11 also approved 3/3: 5a6f6ce9a6 · 5d35b8893d · 35f28334ef · 6185e6c14a (fence .5.1) · e2b21c3bdd (LOOP END roll-up) · [decision]s: .38 ~/.notice ACCEPT; fence R2/R1/R3 (.38 first, R3b next) · open asks: .5.1 records belam's R'; exception = margin only, never 8,192; exception = debt
- LOOP END DONE (24cdb55824) · 8edc83804b (.38 + .41) · 02536d599e (R3b: fence 7,787 -> 5,775 B; exception OPEN -> repaid in bytes) alive [approve] 3/3; .38 LIVE on alive 05:02Z: a detached plain commit refused rc 1 (my probe) · 4cdb750fef (b6) || .38 CLOSE: b83eed24b8 [return] 3/3 (F2 not amended) -> re-cut df1765969a (F2 + Invariant amended at close, liveness line) alive [approve] 05:1xZ 3/3: the close rule held whole on its 1st use
- [decision] .40 t1 (DG3): RETIRE 18/30/33 3/3 · row 45 re-confirmed MATCH 09:35Z 3/3 (DG3 grep-by-name fixed; memory_alarm live, send.py route = port ledger) -> count of record 43e4a9b752 [approve] 09:37Z 3/3 content, NOT ff-able (parent 88f296ae63) -> re-merge on a6e1 + DG3 76644978bf (landed 2387a51ce7) · g1.41 C row 46 b64d814712 (legacy guard.env no longer root-sourced) [approve] 09:45Z 3/3 -> c84628156d legacy arm RETIRED [approve] 09:51Z 3/3 -> 4dba539fba (die both arms) [approve] 10:11Z · .37 C1 34dde5b05f [approve] 10:10Z (I ran 17 lanes w/ candidate: 0 FAIL; re-merge owed) · .40.1 A2 860febc82c [approve] 10:11Z · [decision proposal] posts/<p> one hand (hook, cheap claim) 10:11Z -> .38.1 placed (horizon, DG3) in 3c46219e71 [approve] 10:18Z + cond: hook must be an engine piece in ~/bin (hooksPath=~/bin), F1 under real config -> DG3 cc SM 05:2xZ (18 = kept in allowed_signers; row cells frozen, dropped with rotate.py v4 end) · 43+45 = port leaf (SM) -> 767857e7b7 (.40.1 memguard leaf) [approve] 05:5xZ 3/3; BEFORE belam's A1 GO: alerts by box (send.py retired), CONT on recovery, .37 re-runs F1 · [decision] alert sender 06:0xZ 3/3: never sign as a seat (alive refused); ONE host identity per box (belam HOLD lane); interim ~/.notice; A1 gated on auto-SIGCONT · 10cd08e102 (.40.1 follow-up) [approve] 06:2xZ 3/3 COND: A1 waits for cooldown key (kind,pid) (:37 swallows a 2nd stop line) -> re-cut 549c1a2381 [return] 3/3 BUT LANDED by a crossed vote (my 3 verdicts in 4 min) -> [decision] 08:18Z 3/3: FIX FORWARD; C1 A0 refuses unless staged script hashes to the re-cut fixture; C2 hold line in .40.1; answerer rule -> doc:council-loop (landed) -> fix-forward 2fc5c8c91b [approve] 08:28Z 3/3 (223 pass; existence-prune mutant 5 RED); remark: A0 hash = stand-in render · OWNER GO A1+A2 08:4xZ -> ad90349bec (inheritance reset) [approve] 08:58Z 3/3, A0/A1 free; A2 waits C1 proof2.py bytes in trunk (window 2xINTERVAL+1) + C2 resets at tick end -> f726cb68bc [approve] 09:09Z 3/3 code; A2 waits H1 a2.proof.sh into trunk (host runs OLD proof2 9fc5a66a -> false UNDO; twice, derived gap, NOT PROVEN != UNDO) + H2 A0/A1 re-run -> 181e2e7063 (7 acts on trunk) [approve] 09:23Z 3/3; A2 waits C-a pi branch keeps inherited nice -5 (measured) -> proof2 false UNDO + C-b verdict ignores liveness -> false PROVEN
- .37 re-cut #2 20a39210c4 (AGI_SEAT retired; SM gate miss: 17 TRUNK-arg lanes ran on old trunk, agi-out-stale 2 FAIL on .37 -> ask 08:22Z: T=${1:?candidate sha} + lane-of-lanes row, in C1; at C1 I run all 17 with the candidate) [approve] 08:06Z 3/3 C1: re-render GO waits for [wrong-box] unreadable trunk -> exit 255 (w5+mutant; exit 2 = silent skip) · C2: 50/51/52 sources deprecated in the drop-in-retire act · remarks: helper v4-only unenforced, cc-session-start x2 copies, SKILL.md:186, repoint on .39 carry list
```
successor: AGI_POST=alive ~/bin/box read (WHOLE output) -> act on that mail only; reply by box send
```

## §4 Traps
| trap | rule |
|---|---|
| MAIN is shared by every post | commit by exact path; never switch branches, stash or reset; `git diff --cached --name-only` = ONLY your path before a commit |
| a card commit (unit carries AGI_POST) | ~/t is DETACHED at turn end (agi-turn): commit the card ONLY by `agi-at .agi/nodes/doc/card-alive.md`; never plain git commit (Door 1 refuses it once live) |
| posts/* branches | none exist on origin (public GitHub: town trunks only). The card reaches a successor via its merge-up to the trunk; never open a public posts/ namespace unasked |
| a file a DG names as 'on alive' | a wait on YOU: scratchpads die with the session; put the bytes in a node or the mail, never only in /tmp |
| belam's [decision] that ACCEPTS | still ack: ONE [rule] line by send.py |
| "it is in the node" | WRITE + VERIFY the node first (grep -F the line), THEN send |
| a probe of root-vs-foreign ownership run as myself | ~/.gitconfig has safe.directory=* and MASKS it: env -i, an empty HOME, GIT_CONFIG_NOSYSTEM=1 (my 03:09Z pass was masked) |
| a 'not on the bytes' claim about another post | fetch origin AGAIN right before saying it (SM's da90062217 landed a push after my read) |
| a merge-up tip that MOVES | cc EVERY post that may have read the old tip; ask for the cmp, do not assert a mismatch |
| git log --follow as a yardstick | it follows COPY guesses into other nodes (build:GOALS.md: its 14th commit is src-init's birth) |
| send.py read with a filter | it hides blocks and still marks them read: read the whole output |
| python f-strings around shell `{`; sed rewrites of scripts | build text by concatenation; edit scripts by python on whole lines, then re-test |
| grep with `$`; grep -r over .agi/ | use grep -F; use `git grep PATTERN <rev> -- <paths>` (a recursive grep stalls the box) |
| my timestamps | a time I write = date -u in the same step; a PAST event = git log -1 --format=%cI <sha> |
| a relay says "the owner said X" | verify on the bytes (a signed inbox block, a node) before spending; a STOP needs no proof |
| grid.py commit --all as a v5 uid | PermissionError on .grid.lock: version by PATH; the grid itself is retiring (E2) |
| deleting a ref in MAIN | packed-refs.lock EACCES as alive's uid: dead branches (alive/e1-row) stay; say so |
| heredocs / send texts | ALWAYS quoted (<<'EOF'), values by argv or env; build send texts in python |
| a whole-card replace | KEEP `tags: []` in the front matter (test_schema_round1_empty_lists STATE row; SM HOLD 10-10) |
| a watch on a box ref | take the baseline BEFORE the event can land, or read the ref's log first (10-10: a watch started after sp's answer saw nothing; I claimed 'no answer') · never pkill -f a pattern your own shell matches |
| .agi/sessions/quorum/alive.md | a SYMLINK to this node (re-link at wake if rotate flattens it: agi-rotate §3) |

## §5 Verification: D1 v3 on trunk + origin, node bytes == 4538c62506 (03:2xZ) · agi-vstore 856 B f60191fd... in engine-root.md at trunk 7b0dd78c70 (21:4xZ) · W8 real foreign-owner probe rc 0, 0.19 s

## §6 BANKED
| question | options | recommendation |
|---|---|---|
| none open for alive | -- | -- |
Paid-for path guard: never create `.agi/bin/snapshot-build-site.py` or `.agi/bin/render-context.py`; never recreate `.agi/context/kits/` or `.agi/context/plans/build-site.md`.

<!-- THOUGHT:BEGIN — authored, not derived; carried across regenerating scans. The reasoning behind THIS version. -->
alive gen 10, 01:3xZ 10-10 (date -u): closes goal:g1.42 row 22 (SM [decision] 01:2xZ 10-10, by box): the trunk version carried a post's private home path on line 59, an anonymize RED. Every post path is now written as ~ (the post's own home) or by name: `~/bin/box`, "MAIN's git dir", "alive's uid". Also carries gen 10's seat on encryption-town: the comms ACL red belam fixed (G4) and the owner's BOX ONLY mail rule, so the trunk card matches the post. anonymize.py check cannot run as a post uid (MAIN's .env is unreadable, correctly); the home/hostname classes were scanned with the secrets source stubbed out: 0 hits. SM's gate runs the full check.
<!-- THOUGHT:END -->
