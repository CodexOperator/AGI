---
id: doc:g716111-44-capsule-pack
mint_id: 34a0300067214ec5ad1fb8edcfe3a0dd
type: doc
parents:
  - goal:g7.16.1.11.44
next_edges: []
edited_by: all-is-one
model: claude-opus-5-5
role: council
season: 2
tags:
  - council
  - design
  - g7.16.1.11.44
  - g7.16.1.11.4
title: "Design (goal .44 of g7.16.1.11 + the capsule .4): ONE capsule carries any graph slice or secret -- a signed ref at rest, a git bundle in transit, attached by mint id; season rollover and box moves are the same pack / unpack"
town: core
---
# doc:g716111-44-capsule-pack -- one capsule for slices and secrets

The council's design for goal:g7.16.1.11.44 (owner 20:2x-20:4xZ 10-11, verbatim in .44; it lives on posts/sanctuary-master
until SM lands it, so this doc hangs on goal:g7.16.1.11 and SM re-parents it to .44 at that landing). Drafted by all-is-one;
folded: self-perpetuating's 5 points (S1-S5) + the tension ruling, alive's measures (M1-M4) + points (P1-P6, sig coverage);
v2 folds the council's review of v1 ab9f438bf4: alive aA1-aA4 + sp sA1-sA4 (21:0xZ), and section 9's answers.
REVERSES D2's `nest:` cell and D4's "drop the bundle" (doc:radically-simple-engine §AC.2 l.2574, §AC.5 l.2588), by owner ruling.

```
             AT REST                                 IN TRANSIT                         ON THE TARGET
  refs/capsule/<cid>  = ONE signed commit    git bundle <cid>.bundle             bundle verify -> open (if sealed)
    tree: MANIFEST + members at their paths   = refs/capsule/<cid> + every    -> MANIFEST G by packer + heads == ref lines
          (or cred/k/ring/ for a secret)        carried ref, --not <base>     -> attach mint present -> fetch --atomic
    attach <mint_id>  (re-point = new commit)   sealed OUTSIDE when flagged      (nothing moves unless everything does)
```

## 1 · The format: ONE object, two encodings (alive P1, M1, M2)
- **At rest** a capsule is a ref, `refs/capsule/<cid>`, `<cid>` = a fresh mint id (uuid4 hex, never changes). Its tip is ONE commit
  signed by the packing seat; its tree is `MANIFEST` plus the members at their REPO PATHS (`.agi/nodes/<type>/<f>.md`, each
  member's payload file). No binary is committed: the tree entries name the SAME blobs the trunk already holds (0 bytes stored twice;
  this answers D4's "second store", which was a separate chain of copied `nodes/<mint>` blobs, rse-d4-grok-pilot l.39).
- **In transit** it is one file: `git bundle create <cid>.bundle refs/capsule/<cid> <carried refs> --not <base>` (thin; the target
  holds `<base>`). Custom namespaces ride a bundle (M1); a two-part ref (`refs/stash`) cannot (M4) and is a BOUNDARY line (S5).
- **MANIFEST** (text, one key per line, the ONLY place each fact lives):
```
capsule 1
cid <cid>
kind slice|secret
attach <mint_id>                     # the node it renders at (owner: "carries inside it which graph node it needs to attach to")
encrypt none|box:<box>|post:<post>|quorum
packer <post>@agi
base <trunk sha>                     # the bundle's prerequisite
member <mint_id> <path>              # one per node and per payload file; the TREE is the one home of the bytes (aA1)
ref <refname> <sha>                  # EVERY ref the bundle carries besides refs/capsule/<cid> (alive: sig coverage)
not <what> <reason>                  # the boundary: what this capsule does NOT carry (S5)
```
- **Signed ALWAYS** (no flag): the commit is `-S` by the packer. One signature pins every byte: the commit pins its tree (MANIFEST +
  members); MANIFEST's `ref` lines pin every other carried tip, and unpack requires the bundle's `list-heads` == those lines EXACTLY
  (no extra, none missing, same shas), and the TREE minus MANIFEST == the `member` paths EXACTLY, both directions (aA1: an
  unlisted file would otherwise regrow silently). Verified like .42's land: `git -c gpg.ssh.allowedSignersFile=/var/lib/agi/allowed_signers`,
  `%G? == G AND %GS == <packer>` (a uid with no git config verifies; any other ring key is refused).
- **Encrypt is OUTSIDE, sign is INSIDE** (alive): `encrypt box:<b>|post:<p>` seals the bundle FILE to a key the RECEIVER already holds;
  open first, then verify the inner signature. `quorum` = .4's seal: the payload (`cred`, `k`, `ring/<h>@<w>`) is the capsule's tree,
  popped only by `capsule-pop` (doc:g716111-capsule-build, the patched O.2).

## 2 · The tension, ruled by name (S-ruling; belam's reading)
goal:g7.16.1.11.4's title says "always-encrypted, popped only by the weighted MUTUAL quorum". RULING: that holds for `kind secret`
(deploy + signing keys) and ONLY for it. `kind slice` = signed always, encrypted only to a receiver key, NEVER quorum-popped:
a slice is what a successor or a moved post REGROWS from, and a regrow that waits on a quorum that is dead or split strands a post.
`pack --kind slice --encrypt quorum` is REFUSED at pack time (`[class] a slice is never quorum-popped`, rc 2), and `kind secret`
without `encrypt quorum` is refused the same way, so the two classes cannot blur. .4's title gains one word at its next touch
("secret payloads always-encrypted"): a fix-forward, not a second goal. .4 stays in the .11 HOLD for keys; this format can land first.

## 3 · Attach and re-point by mint id (alive P2, S3)
- ONE home: MANIFEST `attach <mint_id>`. Mint ids never change, so an attach survives every address change and every box.
- **Re-point** = a NEW capsule commit, parent = the old tip, MANIFEST differing in `attach` only, signed: the history is the record
  (retire, never delete). The update rule on `refs/capsule/*`: a `slice` tip may move only to a signed child of itself; a `secret`
  tip moves only by a pop (.4's rule: same tree, one parent, `C H old`). Create-only for both; delete never.
- **The rule's enforcer, at READ** (aA2, sA3; posts write MAIN's refs locally, so no pre-receive runs, and the .38.1 ref-guard is a
  fail-open mistake guard, not a wall): `capsule verify` walks the tip's FIRST-PARENT chain and refuses unless every commit is G by a
  ring principal and each child differs from its parent in `attach` only (slice) or is a pop (secret). A GATE LANE runs it over every
  `refs/capsule/*` at each landing; a capsule ref gone = the lane's count drop = RED. The ref-guard piece gains `refs/capsule/*` as the
  mistake guard. Row: a tip force-moved to an unsigned or tree-changing commit -> verify refuses.
- **Attach to an absent mint** on the target = `[attach-absent] <cid> <mint>`, rc 3, NOTHING fetched (a capsule is never a silent orphan).

## 4 · Render at the attach node (alive P2)
- The index is DERIVED, never authored: one pass `git for-each-ref refs/capsule` + `cat-file --batch` of each `<tip>:MANIFEST`,
  `attach -> [cid]`. viewport.py and `brief.py` show ONE suffix at the attach node, `⊃ <cid8> <n> members` (the llm view and the terminal
  identical, .22's L3), and `capsule show <cid> [path]` = `git show refs/capsule/<cid>:<path>`.
- goal:g7.16.1.11.22's legacy mark reads capsule members in place of `nest:` (its rows keep their shape; only the member source changes).

## 5 · The verbs: ENGINE SHELL pieces in ONE new home, `engine-capsule.md` (owner 10-07: "a wrapper on git operations")
| verb | does | falsifier row (each its own) |
|---|---|---|
| `capsule pack ATTACH SEL [--ref GLOB].. [--kind K] [--encrypt E]` | SEL = `subtree <mint>` (the parents walk, D2's (a') goal tree) · `post <p>` = its REFS only (`refs/heads/posts/<p>`, `refs/box/<p>/*`, `refs/held/<p>/*`, `refs/archive/posts/<p>*`), `member` lines EMPTY: its nodes ride the trunk, a second copy could diverge (aA4); members are for rollover slices · `list <mint>..`; writes MANIFEST, `commit-tree -S`, `update-ref` create-only; prints cid | P1 the ref is created once (a second pack of the same cid rc 128) · P2 class refusals (S-ruling) · P3 every `not` line present for RAM trees, untracked mints, host files, crontabs, refs/stash, refs/remotes |
| `capsule out CID > FILE` | the bundle (+ the outer seal when flagged) | O1 `git bundle verify` passes on a repo holding `base`, fails on one that does not |
| `capsule verify FILE` | open · bundle verify · the first-parent chain (section 3) · heads == `ref` lines · tree == `member` paths · attach mint present | SIGNATURE: ONE flipped byte (in MANIFEST, a member, or a carried ref swapped to another sha) -> refused, the repo byte-identical; untouched -> passes · TREE: an unlisted file added -> refused |
| `capsule in FILE` | verify, then `git fetch --atomic FILE <exactly the listed refs>` | ATOMIC (M3): one non-ff ref -> rc != 0 and NOTHING moved; the mutant without `--atomic` -> a sibling advanced = RED |
| `capsule regrow CID DIR` | `git archive refs/capsule/<cid>` into DIR | REGROW below |
| `capsule repoint CID MINT` | the signed child with a new `attach` | R1 the old tip is the new tip's parent; R2 an absent MINT rc 3 |
| (no `move` verb) | the box move is box-move.sh's: it CALLS pack/out/verify/in (section 6); drafter's ruling 01:5xZ 10-12, the piece stays the slice verbs under its 8,192 B bar | MOVE below |
Budget: MEASURED at DG4's cut 2 (c0bb3f05ef, 01:4xZ 10-12): ONE piece `capsule` (pack out verify in regrow repoint, one case arm
each) = 7,418 B in config:engine-capsule, 2.8x my ~2.6 KB estimate, above the pilot's 5,234 B and under the 8,192 B rail; `move` is
not in it yet. An engine-sizes row holds engine-capsule.md's fenced bytes <= 8,192 (asked 01:4xZ). engine.md's fence is untouched.
Deviations ACCEPTED by the drafter (01:4xZ, stack 7): D1 a carried ref BEHIND base: cut 2 fattens the WHOLE bundle (`[fat]`, ~287 MiB here, mark on stderr
only), so the council's fix-forward (alive FF1, 01:40Z) rides it as its MANIFEST `ref` line ONLY: verify = heads == the `ref` lines
minus the behind-base ones, each of those `cat-file -e` + `merge-base --is-ancestor <sha> <base>` on the target, set in the same
atomic transaction as the rest; D2 `out`
writes the `^<base>` prerequisite itself; D3 `verify` judges inside a scratch BARE repo whose alternates point at MAIN (0 objects
copied, MAIN byte-identical); D4 `out` refuses `[moved]` when a carried tip moved since `pack`.

## 6 · Box move = pack / carry / unpack, run BY box-move.sh (alive P5, S2; replaces its :32-:45, keeps :31 unit-paths and the row edit)
```
PRE-STOP  DRY pack in a JOB-OWNED `clone --shared` on the source (never MAIN's refs/capsule: delete-never would keep every dry run; sA1;
          row: a dry run leaves MAIN's refs/capsule/* count unchanged)
          -> out -> ssh TARGET: verify + in into a scratch clone ON MAIN'S FILESYSTEM + a write probe in MAIN's refs dir (aA3)
          + each carried refs/grid line checked against MAIN's own value: sha present, ff (section 8 row 5c, sp)
          any refusal -> rc 6, nothing touched                      <- NARROWS the .39 limit (aA3): the target judges the real bytes
STOP      systemctl stop agi-post@P ; row edit ; origin push (unchanged)
REAL      capsule pack in MAIN (the refs moved until the stop) -> out -> carry ONE file -> TARGET capsule in (--atomic)
AFTER     the .39 per-namespace counts + names (unchanged)
RESIDUAL  the seconds from STOP to the REAL `in`, plus what only MAIN's own refs dir can refuse (a hook, packed-refs.lock) after the probe;
          recovered by RECOVERY below.
RECOVERY  (sA2) the REAL `in` refused: pack never deletes a source ref, so it is lossless: one `[move-in-failed]` line to the master,
          the row edit reverted by a second commit, agi-post@P started on FROM. Row: target `in` refused after the stop -> the post
          runs on FROM, the row is back, FROM's refs are unchanged.
```

## 7 · Season rollover = the same verbs (alive P4, P6)
D2's (a') stays the SELECTOR (the goal tree covers 90.1 % of non-goal nodes, AC.1); the `nest:` CELL is replaced by the capsule.
CLOSE (unchanged) -> PACK one `kind slice` capsule per GOAL SUBTREE (Q1, council 3/3: the (a') selector partitions them; a build cone
stays a RENDER, D2(b), else the 76 multi-slice nodes return), `attach` = the subtree's goal until the owner rules the build node
(his "collapse ... into the relevant build nodes": then ONE `capsule repoint` per capsule, the attach is re-pointable) -> RETIRE members to `deprecated/` by normal gated landings -> CARRY -> CUT.
Members STAY files (deprecated/) after the pack; removing any member from the tip is a SEPARATE owner-ruled step, gated on links.py
counting capsule members, or "active + deprecated never drops" breaks. Retired by this design: nest.py and the `nest:` cell
(goal:g7.16.1.11.21's reader; 0 nodes carry `nest:`), the `nest:` line of the [doc] schema; `refs/slice` is never revived.

## 8 · Falsifiers (the design's, beside each verb's row)
1. REGROW (S4), in TWO rows (sA4: `git archive` carries files only, NO refs, measured):
   1a FILES: for a real rollover slice incl. deprecated members, `capsule regrow` after in(out(pack)) on a scratch repo == the slice's
      files byte for byte, apart from AC.4's named cells (path, `status:`, `season:` of a carried node). Diff beyond those = red.
   1b REFS: for one real post (`post <p>`, grid refs included via `--ref`), after `in` the target's refs named by the `ref` lines ==
      those lines, name + sha, none missing, none extra.
2. SIGNATURE: as section 5 (one flipped byte anywhere -> refused, byte-identical repo).
3. CLASS: a `secret` capsule never yields plaintext through `capsule in`; a `slice` with `encrypt quorum` never packs.
4. MOVE: the next box move after the verbs land runs section 6 and the .39 counts per namespace match.
5. GRID = TRANSPORT (council 3/3 (b), 03:2xZ 10-12; replaces a grep row that was VACUOUS: the piece holds 'refs/grid' 0 times, so it
   passed while `in` set any carried ref, alive): `in` never AUTHORS a grid version; it carries grid refs VERBATIM, each target sha ==
   its MANIFEST `ref` line, inside the one CAS transaction, ff-only, the same act box-move.sh's push does today (one carrier per move,
   not two: once box-move.sh calls the capsule, its own refs/grid push goes). ROWS: (a) after in(out(pack `post <p>` --ref
   'refs/grid/*')) every target refs/grid/* sha == its MANIFEST line and NO grid commit exists on the target that the source lacked;
   mutant `in` writes any other sha -> RED; (b) a grid line whose sha is in neither the bundle nor the target -> refused, every ref
   unchanged (aio); (c) FAIL BEFORE THE STOP (sp): the same grid-line checks (sha present, ff vs the target's current value) run in
   section 6's PRE-STOP target verify: a non-ff refs/grid line there -> rc != 0 named, the post still running on FROM.
   Also: `git grep '^nest:'` stays 0; and every engine-capsule.md ref writer (commit-tree -S of the MANIFEST commit, the
   `update-ref --stdin` transaction, the bundle fetch into verify's scratch repo) is CLASSIFIED in goal:g7.16.1.11.13's pinned C1/C7
   blocks, the `in` site as a TRANSPORT writer beside box-move's push (N7), never a grid AUTHOR: test_grid_writers green at the sha
   (added 03:1xZ 10-12: the drafter's miss let cut 2 land with .13 red from L7 on).

## 9 · The open questions, answered (council 21:0xZ) and what stays open
- Q1 ANSWERED (3/3): one capsule per GOAL SUBTREE; attach = its goal until the OWNER rules the build node (section 7). Owner's call: that re-point.
- Q2 ANSWERED (3/3, sp withdrew the host-key lean 21:0xZ): BOX MOVES TODAY = `encrypt none` (the ssh carry encrypts in transit; at
  rest the target is the same repo class). A seal for a capsule that rests OFF a box waits in the .11 HOLD (key work). If one is wanted
  later, the sshd ed25519 host key is the candidate, never a quorum-held key (a move must not wait on a pop, section 2), at a NAMED
  cost (alive): opening needs the host's PRIVATE key (root 600), so `capsule in` of a sealed slice runs as root, and the key rotates
  outside our ring.
- Q3 ANSWERED (3/3): `capsule-pop` STAYS in config:capsule (O.2) until the HOLD lifts; engine-capsule.md holds the slice verbs only.

<!-- THOUGHT:BEGIN — authored, not derived; carried across regenerating scans. The reasoning behind THIS version. -->
all-is-one gen 7 20:4xZ 10-11, first version: the owner's 20:2x-20:4xZ ruling makes the slice container and the capsule ONE envelope.
The pick that makes it one object: alive measured that a git bundle carries custom namespaces and a manifest commit, so the at-rest
form (a signed ref, the capsule's own shape since O.1) and the transit form (a bundle) are two encodings of the same commit; the
signature covers the bundle's other refs only through MANIFEST's `ref` lines (alive), so verify demands list-heads == those lines.
self-perpetuating's inheritance argument decides the .4 tension: quorum for secrets only. Nothing here is built; SM places one
build leaf per verb after the council answers.
v2 21:1xZ: the council's review of v1 found four rules without a check (tree vs member lines, the update rule, the dry pack vs
delete-never, the recovery after the stop), one claim larger than its proof ("closes" -> narrows), a vague selector (post = refs only)
and a falsifier archive cannot see (REGROW split into files + refs). Each is now a line with its row; Q1, Q2 (none for box moves today) and Q3 answered 3/3; the off-box seal banked to the HOLD.
v4 01:4xZ 10-12: the budget line said ~2.6 KB; DG4's cut 2 measured 7,418 B, so the line now carries the measured size, its rail and
the four deviations the drafter accepted, each better than or equal to the design's text (D3 especially).
v5 03:3xZ 10-12 (gen 8): may `in` SET refs/grid/*? 3/3 (b) (sp withdrew (a) 03:21Z: grid_sync's 5-min push leaves the move's last
window only on the source, a carry is its one path). Row 5's grep was vacuous (alive), so it is now a behaviour row with a mutant,
my refusal for a sha in neither repo, and sp's pre-stop check so a refused grid line fails while the post still runs.
<!-- THOUGHT:END -->
