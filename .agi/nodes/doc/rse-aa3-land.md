---
id: doc:rse-aa3-land
mint_id: b1731b02854c49b988a635ea662859c3
type: doc
parents:
  - goal:g7.16.1.11
next_edges: []
edited_by: all-is-one
model: claude-opus-5-5
role: director
scaffold_hash: 517ba118802a2ce1
season: 2
tags:
  - council
  - design
  - g7.16.1.11
title: "AA3 land: a land is mail one parent edge up (council design bundle, all-is-one)"
town: core
---
# doc:rse-aa3-land

AA3 of the council's design bundle (belam [decision] 23:34Z + owner 23:0xZ / 23:2xZ). Siblings: AA1 boxes = doc:rse-aa1-boxes (alive) · AA2 keys = doc:radically-simple-engine §AA2 (self-perpetuating). Measured, not argued: 11 lanes on a scratch repo that borrows MAIN's objects (alternates), 0 shared refs written.

## AA3.1 The rule — a land is mail going ONE parent edge up
Owner 23:2xZ: "protocol needs to be a mathematical matrix rotation or projection. So things could only go where they must go."
```
root ff-lands <post>'s <sha> on the trunk  iff  ALL hold at the RECEIVING tip $o (never read from the branch):
  edge     sender = parent(post) on config:posts parent cells   (parent "council" = a name in the council row's members cell;
                                                                  a post whose parent is "owner" lands itself)
  signers  every commit in $o..$sha verifies on ROOT'S RING (AA2) as the sender or a post under <post>
  growth   grow-gate over $o..$sha (matrix + schemas + agi-fill ratchet, §Y1 v3)
  body     agi-gate $sha (the engine still regrows)
  ff       $o is an ancestor of $sha; the move is compare-and-swap
```
The request travels as AA1 mail to root: refs/box/<sender>/root, body `land <post> <sha>`; root reads its box as itself.
No master role, no human gate step: authority = the tree, which is a projection of the parent cells.

## AA3.2 agi-land (1,797 B, root-side, so it belongs in config:engine-root, not the zygote)
```sh
#!/bin/sh
# agi-land <sender> <post> <sha>: root ff-lands <post>'s <sha> on the trunk, ONE parent edge up: sender = parent(post); parent "council" (inert row) = a name in its members cell (absent = nobody); a parent-owner post lands itself; a `lands` cell on the parent narrows which children it takes (AA2: council lands only SM).
# each commit in $o..$n signed (root's ring) by the sender or a post under <post> on the parent cells · grow-gate on $o..$n · agi-gate · CAS ff
T=${AGI_TRUNK:-refs/heads/trunk};A=${AGI_RING:?};o=$(git rev-parse -q --verify $T)||exit 1;n=$(git rev-parse -q --verify "$3^{commit}")||exit 1
git merge-base --is-ancestor $o $n||{ echo "refused: not ff";exit 1;};t=$(mktemp -d);trap 'rm -rf $t' EXIT
git show $o:.agi/nodes/.geometry/posts.md|sed -n 's/^  - {/{/p'|jq -r '"\(.name) \(.parent//"")",(select(.name=="council")|.members[]?|"M \(.)"),(.name as $n|.lands[]?|"\($n)>\(.)")'>$t/p
u(){ x=$1;while [ "$x" ];do [ $x = $2 ]&&return;x=$(awk -v n=$x '$1==n{print $2}' $t/p);done;return 1;}
grep -qx "$2 $1" $t/p||{ grep -qx "$2 council" $t/p&&grep -qx "M $1" $t/p;}||{ [ $1 = $2 ]&&grep -qx "$1 owner" $t/p;}||{ echo "refused: $1 is not the parent of $2";exit 1;}
P=$(awk -v n=$2 '$1==n{print $2}' $t/p);grep -q "^$P>" $t/p&&! grep -qx "$P>$2" $t/p&&{ echo "refused: $P lands only $(sed -n "s/^$P>//p" $t/p|tr '\n' ' ')";exit 1;}
for c in $(git rev-list $o..$n);do s=$(git -c gpg.ssh.allowedSignersFile=$A verify-commit --raw $c 2>&1|sed -n 's/.*signature for \([^@]*\)@agi with.*/\1/p')
[ "$s" ]&&{ [ $s = $1 ]||u $s $2;}||{ echo "refused: $c signed by ${s:-nobody}: not $1, not under $2";exit 1;};done
echo "$o $n $T"|AGI_ALLOWED=$A AGI_TRUNK=$o AGI_NOT=$o grow-gate||exit 1;agi-gate $n||{ echo "refused: engine would not regrow";exit 1;}
git update-ref $T $n $o
```
Production difference (one line): MAIN has the trunk CHECKED OUT, so root's last step is `git -C <MAIN> merge --ff-only $n`, not update-ref. merge refuses when the trunk moved to a non-ancestor, which makes it the compare-and-swap.

## AA3.3 Lanes (scratch, 23:5xZ 10-01, trunk c645f4e01; ring = 5 scratch keys as "<post>@agi")
| # | lane | expect | got |
|---|---|---|---|
| 1 | SM lands DG1 (DG1-signed card edit) | land | rc 0, moved |
| 2 | forged: alive's key, committer director-general-1 | refuse | "signed by alive: not SM, not under DG1" |
| 3 | SM lands alive (not its child) | refuse | "not the parent of alive" |
| 3b | DG1 lands itself | refuse | "not the parent of director-general-1" |
| 3c | all-is-one (council) lands SM | land | rc 0, moved |
| 3d | alive (council) lands SM | land | rc 0, moved |
| 3e | DG1 lands its parent SM | refuse | "not the parent of sanctuary-master" |
| 3f | belam (parent owner) lands itself | land | rc 0, moved |
| 4 | DG1 adds a parentless hypothesis | refuse | grow-gate: "wrong order: hypothesis (-) under [-]" |
| 5 | not ff (built on trunk~1) | refuse | "not ff" |
| 4v | lane 4 through TODAY's grow-gate with posts/<p> pointing at it | — | rc 0: VACUOUS PASS |
The first draft let lane 3b land: "every signer is the sender or under it" holds trivially when the sender signs everything. The edge check closed it.

## AA3.4 Three byte fixes the design NEEDS (each measured)
1. signers piece (engine-post): principal `<post>` vs the unit's GIT_COMMITTER_EMAIL=%i@agi -> `verify-commit`: "No principal matched" on EVERY v5 commit (HEAD of posts/all-is-one: signed, unverifiable; "<post>@agi" reads Good). Superseded by AA2's root ring, which writes "<post>@agi". AA1 writes the bare name: ONE form must be agreed.
2. grow-gate: `rev-list $n --not --all` is quarantine logic. Inside the shared repo the commits are already reachable from posts/<p>, so the gate checks nothing (lane 4v). Fix: `--not ${AGI_NOT:---all}` (+12 B); the hub keeps --all.
3. grow-gate's signer sed keeps "@agi", so a ring cell never equals it: strip it in the sed (+7 B).
4. grow-gate is BLIND TO MERGES: `git diff-tree -r` prints nothing for a merge commit, so a signed merge whose tree adds a node in NEITHER parent lands it unchecked (lane 4m: the parentless node reached the scratch trunk, even with fixes 1-3). AA1's down-merges (merge-tree + commit-tree) make merges routine on posts/<p>. Fix: `diff-tree -r -c` (combined: only paths that differ from EVERY parent; a clean merge lists nothing, an evil one lists `AA <path>`) + treat `AA` as an add (`[ $m = A -o $m = AA ]`): +14 B.

## AA3.5 Byte account and what it retires
+1,797 B agi-land (engine-root) · +33 B grow-gate (fixes 2-4) · 0 B in the zygote. config:engine itself = 8,283 B, already 91 B over 8,192 before this bundle: AA3 adds nothing to it.
Retires: the master's hand-gated merge-up (skill agi-master-gate's landing path) and the hub pre-receive as the ONLY gate.
OPEN for the owner: is the 8 KB "base install" config:engine alone (8,283 B) or every engine*.md (34,885 B)? The owner's 23:2xZ line ("the graph can hold as much as you want, just the engine itself needs to be tiny") reads as the zygote.

## AA3.6 Falsifiers for DG1's build
AA3.1 every lane in AA3.3 reproduces on the real ring + the real trunk (a scratch clone, never MAIN).
AA3.2 a land whose range holds one commit signed by a post outside <post>'s subtree moves nothing.
AA3.3 the trunk reflog shows ONLY root as the trunk writer after the switch (belam's write.py posts.md commits go through a land too).

## AA3.7 Skill deltas for engine.v 4 posts (owner 23:4xZ; split by alive 23:5xZ: AA3 = master-gate · merge-pass · dispatch · verify)
A DELTA, not a rewrite: what a v4 post does INSTEAD; the old-setup text stays for belam, SM, DG3 and old TM until each one moves.
| skill | old setup | v4 post instead |
|---|---|---|
| agi-master-gate §Land | merge-tree + commit-tree in a /tmp worktree, ff MAIN, push by hand | the parent mails root `land <post> <sha>` (AA1 box to root); agi-land checks the edge, ring signers, grow-gate on the range, agi-gate and ff. No staged merge: the child's agi-flush already merged the trunk into posts/<p>. A "not ff" refusal = mail the child to merge the trunk. The push is root's carrier (AA1), never a post's |
| agi-master-gate §Suites | the gate runs pytest on tmpfs, attributes reds | UNCHANGED: a parent's judgment BEFORE it mails `land`. Root runs no suite (the land path stays small and synchronous) |
| agi-merge-pass §2 PASS | pull, merge --no-ff TIP, verify, push season2/main, ff local-maxxing/main, grid --all | the town-trunk tip reaches season2/main as ONE land one edge up: the trunk is the receiving row's engine.trunk cell, the sender is its parent. CHECK cron + review/verdicts unchanged. grid.py by path, never --all (belam 23:49Z) |
| agi-dispatch §1-2 | write.py create goal · dispatch.py spawns a parent | goal = a plain node file in ~/t, committed by agi-turn. A parent = a child ROW (parent cell = me), so root starts its unit; a kid = agi-kid inside my unit. Spawn bound = the unit's PSI admission line. Reports come back as mail up the edge. season.py judge stays (it reads) |
| agi-verify §1 | commands.py run verify after a merge | the land's own checks are the gate BEFORE the move. `commands.py run verify` + `links.py links` run AFTER it, by root or the receiving parent, never in a child's tree |
| all four | write.py · grid.py commit --all | plain Read/Edit in ~/t · agi-turn signs the one commit · grid.py commit <path> |
Load matrix: agi-node-write leaves a v4 post's skills through AA2's per-worktree sparse-checkout (skip-worktree paths are never staged as deletions), never by deleting the committed .claude/skills link: agi-turn's `add -A` would land that deletion for everyone. agi-rotate's delta is AA2's (alive 23:5xZ correction).

## AA3.8 belam's ruling members<-council (1efd017e6, 23:51Z) and what it costs the land rule
Measured on trunk 1efd017e6+: alive, all-is-one, self-perpetuating, SM and TM-new now ALL sit under `council`. Parent cells alone can no longer tell a member from SM.
The first alias ("sender's parent is council") LET SM LAND ALIVE (lane 3 moved). Fixed fail-closed: council authority = a name in the council row's `members` cell, and an absent cell means nobody.
| trunk | lane 3 SM lands alive | 3c/3d a member lands SM |
|---|---|---|
| 1efd017e6 as is (no members cell) | refused | refused (fail closed) |
| + `"members": ["alive","all-is-one","self-perpetuating"]` on the council row (scratch commit) | refused | land |
| faabf9b7a: belam WROTE the cell (23:53Z), the REAL trunk | refused | land (11/11 lanes) |
The cell is written (belam faabf9b7a, 23:53Z): the fail-closed reading stands. The council's own docs reach the trunk through SM's gate until agi-land exists (belam 23:51Z).

## AA3.9 lanes.sh — the falsifier as bytes (4,213 B, 13 lanes; for goal:g7.16.1.11.13 falsifier 1, DG1 00:0xZ 10-02)
Run from a worktree: `sed -n '/^## AA3.9/,$p' .agi/nodes/doc/rse-aa3-land.md | sed -n '/^```sh/,/^```$/{//!p}' > /tmp/lanes.sh; sh /tmp/lanes.sh`. Writes 0 shared refs (alternates); scratch keys named as the real posts.
TODAY (trunk b6b2c33d3, 01:0xZ 10-02; belam wrote council `lands` there): 11 ok + `FAIL 4m` + `FAIL 4v` = the real grow-gate is vacuous at a land AND blind to merges. With all FOUR AA3.4 byte fixes (`GROW_GATE=<fixed> sh lanes.sh`): 13/13 ok, measured. 4m + 4v ARE the blocking order DG1 wrote.
```sh
#!/bin/sh
# lanes.sh [TRUNK] [GITDIR]: AA3.3's 13 lanes on a throwaway repo borrowing GITDIR's objects (0 shared refs written). One line per lane: ok | FAIL.
# Tools come from TRUNK by sect (grow-gate from $GROW_GATE if set); agi-land from $AGI_LAND, else AA3.2 of doc:rse-aa3-land in this tree. Keys are scratch keys named as the real posts.
T=${1:-local-maxxing/season2/main};G=${2:-$(git rev-parse --path-format=absolute --git-common-dir)};D=$(mktemp -d);trap 'rm -rf $D' EXIT;mkdir $D/b $D/k
o=$(git rev-parse $T)||exit 1;for x in sect grow-check grow-gate agi-fill agi-gate agi-project;do git ls-tree --full-tree --name-only $o .agi/nodes/.geometry/|grep '/engine[^/]*\.md$'|sed "s|^|$o:|"|git cat-file --batch --follow-symlinks|sed -n "/^###* $x /,/^###* /{/^~~~/,/^~~~/{//!p}}">$D/b/$x;done
[ "$GROW_GATE" ]&&cp $GROW_GATE $D/b/grow-gate;if [ "$AGI_LAND" ];then cp $AGI_LAND $D/b/agi-land;else sed -n '/^## AA3.2/,/^## AA3.3/{/^```sh/,/^```$/{//!p}}' .agi/nodes/doc/rse-aa3-land.md>$D/b/agi-land;fi;chmod +x $D/b/*
for p in sanctuary-master director-general-1 alive all-is-one belam;do ssh-keygen -qN "" -ted25519 -f$D/k/$p;echo "$p@agi namespaces=\"git\" $(cut -d' ' -f1,2 $D/k/$p.pub)">>$D/ring;done
git init -q $D/r;echo $G/objects>$D/r/.git/objects/info/alternates;cd $D/r;git update-ref refs/heads/trunk $o;export PATH=$D/b:$PATH AGI_RING=$D/ring AGI_TRUNK=refs/heads/trunk
mk(){ x=$D/i;GIT_INDEX_FILE=$x git read-tree $3;GIT_INDEX_FILE=$x git update-index --add --cacheinfo 100644,$(git hash-object -w $5),$4;t=$(GIT_INDEX_FILE=$x git write-tree);rm -f $x
GIT_COMMITTER_NAME=$2 GIT_COMMITTER_EMAIL=$2@agi GIT_AUTHOR_NAME=$2 GIT_AUTHOR_EMAIL=$2@agi git -c gpg.format=ssh -c user.signingkey=$D/k/$1 commit-tree -S -p $3 -m lane $t;}
C=.agi/nodes/doc/card-director-general-1.md;git show $o:$C>$D/c;echo lane>>$D/c;printf -- '---\nid: hypothesis:zz-lane\ntype: hypothesis\ntitle: lane\n---\n# lane\n'>$D/h
L(){ git update-ref refs/heads/trunk $o;w=$1;n=$2;shift 2;agi-land "$@">$D/out 2>&1;[ $(git rev-parse trunk) != $o ]&&v=land||v=refuse;[ $v = $w ]&&echo "ok   $n  [$(tail -1 $D/out|cut -c1-60)]"||echo "FAIL $n (want $w, got $v: $(tail -1 $D/out|cut -c1-80))";}
g=$(mk director-general-1 director-general-1 $o $C $D/c);m=$(mk sanctuary-master sanctuary-master $o $C $D/c);q=$(mk belam belam $o $C $D/c)
L land "1 SM lands DG1" sanctuary-master director-general-1 $g
L refuse "2 forged: alive's key, committer DG1" sanctuary-master director-general-1 $(mk alive director-general-1 $o $C $D/c)
L refuse "3 SM lands alive" sanctuary-master alive $(mk alive alive $o $C $D/c)
L refuse "3b DG1 lands itself" director-general-1 director-general-1 $g
L land "3c member all-is-one lands SM" all-is-one sanctuary-master $m
L land "3d member alive lands SM" alive sanctuary-master $m
L refuse "3e DG1 lands its parent SM" director-general-1 sanctuary-master $m
L refuse "3g member all-is-one lands alive (council lands only SM; FAIL until AA2 writes the cell)" all-is-one alive $(mk alive alive $o $C $D/c)
L land "3f belam (parent owner) lands itself" belam belam $q
b=$(mk director-general-1 director-general-1 $o .agi/nodes/hypothesis/zz-lane.md $D/h);L refuse "4 parentless hypothesis" sanctuary-master director-general-1 $b
s2=$(mk director-general-1 director-general-1 $o .agi/nodes/doc/card-sanctuary-master.md $D/c);x=$D/j;GIT_INDEX_FILE=$x git read-tree $(git merge-tree --write-tree $g $s2);GIT_INDEX_FILE=$x git update-index --add --cacheinfo 100644,$(git hash-object -w $D/h),.agi/nodes/hypothesis/zz-lane.md;e=$(GIT_INDEX_FILE=$x git write-tree);rm -f $x
L refuse "4m a signed merge adding a node in NEITHER parent (diff-tree skips merges before AA3.4 fix 4)" sanctuary-master director-general-1 $(GIT_COMMITTER_EMAIL=director-general-1@agi GIT_AUTHOR_EMAIL=director-general-1@agi git -c gpg.format=ssh -c user.signingkey=$D/k/director-general-1 commit-tree -S -p $g -p $s2 -m lane $e)
L refuse "5 not ff (on trunk~1)" sanctuary-master director-general-1 $(mk director-general-1 director-general-1 $(git rev-parse $o~1) $C $D/c)
git update-ref refs/heads/posts/director-general-1 $b;L refuse "4v lane 4 with posts/<p> pointing at it (vacuous before AA3.4)" sanctuary-master director-general-1 $b
```

## AA3.10 Versioning: the hourly snapshot + retiring the global grid (belam [decision] 00:25Z, owner 00:3x-00:4xZ; split settled 00:3xZ)
Split: AA1 alive = the grid commit surface (one node per turn from its tiny tree onto posts/<p>) · AA2 self-perpetuating = read/ff projections + tree lifetime · AA3 = land + snapshot + grid retirement.
TRUE STATE (00:3xZ 10-02): the global grid is LIVE (35 refs/grid/* written in the last hour, 189 in 24 h; 5,756 refs/grid/local-maxxing + 3,807 refs/grid/node = 9,563 of 11,779 refs, all pushed to origin) · cron:crons `grid_sync` every 5 min ALSO runs `crons.py apply` (the crontab self-heal) · `branch_push` "7 * * * *" pushes the CHECKED-OUT branch from belam's crontab · v5 uids hold no GitHub credential.
```
SNAPSHOT   = root's carrier (AA1, the one GitHub key "stored on root on box") pushes the TRUNK + refs/box/* hourly.
             No snapshot commit: every change already IS a commit (a grid commit per turn, a land per edge). The owner's
             "whole repo committed and pushed as a whole" = the trunk tip, which holds the whole graph. branch_push retires.
GRID       = per-turn commits on posts/<p> (AA1) reach the trunk ONLY by agi-land, so the trunk's history IS the grid:
             `git log -- <node path>` replaces refs/grid/node/<mint>. A land range checks node by node, one node per commit.
RETIRE     grid_sync: enabled false. refs/grid/* are NOT moved or deleted: they ARE the archive (a post cannot delete a ref,
             and moving 9.5k refs is a delete + create). grid.py's READ verbs keep working on them; `grid.py commit` retires
             with them (belam 23:49Z already: by path, never --all).
RE-HOME    the crontab applier: interim = its own cadence `crons_apply: every_mins 5` (0 engine bytes); target = the body
             follows the trunk: agi-project.path already fires on the trunk ref's log, so the crontab becomes one more
             projection of cron:crons at the trunk tip, with no polling.
```
Falsifiers (for DG1): V1 after the switch, `git for-each-ref refs/grid | wc -l` stays constant for 1 h while posts work · V2 the origin trunk tip is never older than 65 min · V3 a hand edit of the crontab is undone within 5 min (the applier survived grid_sync's retirement) · V4 `git log --format=%h -1 -- <node>` on the trunk names the land that carried that node's last per-turn commit.
OPEN for belam: whether refs/grid/* stay pushed to origin (they are history GitHub already holds) or are dropped from the carrier's refspec (an owner call: it is the GitHub copy).

## AA3.11 The `lands` mask (AA2 defines, AA3 enforces; self-perpetuating 00:4xZ)
AA2: ff(P) = UP-darts into P x a `lands` cell on P's row (no cell = all children); the owner's "council only from SM" = council row `lands: ["sanctuary-master"]`.
agi-land enforces it in ONE line after the edge check: the post's parent P has a `lands` cell and the post is not in it -> "refused: P lands only ...". +294 B (1,503 -> 1,797).
Measured: lane 3g (a member lands alive) on a scratch trunk carrying the cell = refused "council lands only sanctuary-master"; every other lane is unchanged. belam WROTE the cell (b6b2c33d3, 00:29Z): 3g reads ok on the real trunk.
