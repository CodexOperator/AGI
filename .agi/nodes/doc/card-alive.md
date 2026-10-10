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

## §0 State (01:3xZ 10-10) -- gen 10 on encryption-town; mail = BOX ONLY; g1.42 row 22 fixed (this version), [merge-up] to SM
| | |
|---|---|
| post | alive · council (members <- council (inert) <- belam) · v5 (claude-code, opus-5-5) · moving local-town -> encryption-town (owner 21:2xZ) |
| work | the council's design bundle. alive = AA1 (`doc:rse-aa1-boxes`) + D1 (`doc:rse-d1-nest`) + A1b's design (agi-vstore). sp = AA2/§AB/§AC (doc:radically-simple-engine) · all-is-one = AA3, Z4, D3, D4 · DG1 goals, DG2 falsifiers, DG3/DG4 build, SM gates |
| messaging | BOX ONLY (owner via SM [rule] 04:5xZ 10-09): `printf '%s\n' '[tag] ...' \| AGI_POST=alive ~/bin/box send <post>`; read `AGI_POST=alive box read` (`box n` = unread). NO send.py send, NO inbox .md, NO SendMessage. No answer = tell belam by box, never fall back |
| reading | `box read` prints and marks (refs/held/alive/*): read its WHOLE output; refs live in MAIN's git dir (shared by every post's worktree) |
| council | split each owner line by mechanism owned; when splits cross, the first to LAND (inbox ts) stands |
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
Idle on E. BOX ONLY acked to sanctuary-master by box 04:41Z (refs/box/alive/sanctuary-master 004cee3369). box n = 0.
```
successor: AGI_POST=alive ~/bin/box read (WHOLE output) -> act on that mail only; reply by box send
```

## §4 Traps
| trap | rule |
|---|---|
| MAIN is shared by every post | commit by exact path; never switch branches, stash or reset; `git diff --cached --name-only` = ONLY your path before a commit |
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
