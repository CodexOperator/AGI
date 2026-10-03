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

## AA3.2 agi-land (1,829 B, AA3.14 version, root-side, so it belongs in config:engine-root, not the zygote)
```sh
#!/bin/sh
# agi-land <sender> <post> <sha>: root ff-lands <post>'s <sha> on the trunk, ONE parent edge up: sender = parent(post); a parent with a members cell is an inert group: the land passes to ITS parent; a parent-owner post lands itself; a `lands` cell on the parent narrows which children it takes (absent = all, [] = none).
# each commit in $o..$n signed (root's ring) by the sender or a post under <post> on the parent cells · grow-gate on $o..$n · agi-gate · CAS ff
T=${AGI_TRUNK:-refs/heads/trunk};A=${AGI_RING:?};o=$(git rev-parse -q --verify $T)||exit 1;n=$(git rev-parse -q --verify "$3^{commit}")||exit 1
git merge-base --is-ancestor $o $n||{ echo "refused: not ff";exit 1;};t=$(mktemp -d);trap 'rm -rf $t' EXIT
git show $o:.agi/nodes/.geometry/posts.md|sed -n 's/^  - {/{/p'|jq -r '"\(.name) \(.parent//"")",(select(.members)|"I \(.name)"),(.name as $n|.lands|select(.)|"\($n)>",(.[]|"\($n)>\(.)"))'>$t/p
u(){ x=$1;while [ "$x" ];do [ $x = $2 ]&&return;x=$(awk -v n=$x '$1==n{print $2}' $t/p);done;return 1;}
q(){ awk -v n=$1 '$1==n{print $2}' $t/p;};Q=$(q $2);P=$Q;grep -qx "I $Q" $t/p&&P=$(q $Q)
{ [ "$P" != owner ]&&[ "$1" = "$P" ];}||{ [ $1 = $2 ]&&[ "$P" = owner ];}||{ echo "refused: $1 is not the parent of $2";exit 1;}
grep -q "^$Q>" $t/p&&! grep -qx "$Q>$2" $t/p&&{ m=$(sed -n "s/^$Q>\(.\)/\1/p" $t/p|tr '\n' ' ');echo "refused: $Q lands only ${m:-nothing}";exit 1;}
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
| 3c | all-is-one (council) lands SM | refuse (SHIPPED, AA3.14: the inert keep passes the land through to belam; the first design said land) | "all-is-one is not the parent of sanctuary-master" |
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

## AA3.9 lanes.sh — the falsifier as bytes (4,931 B, 17 lanes, AA3.14, exit = FAIL count, 17 = agi-land not built; for goal:g7.16.1.11.13 falsifier 1, DG1 00:0xZ 10-02)
Run from a worktree: `sed -n '/^## AA3.9/,$p' .agi/nodes/doc/rse-aa3-land.md | sed -n '/^```sh/,/^```$/{//!p}' > /tmp/lanes.sh; sh /tmp/lanes.sh`. Writes 0 shared refs (alternates); scratch keys named as the real posts.
TODAY (trunk 1517e4b7d, 14:1xZ 10-02): exit 13 = agi-land is NOT BUILT (every tool, agi-land included, now comes from the trunk's engine nodes, never from this prose doc: self-perpetuating 14:0xZ, agi-frontier's whitelist refuses code sliced out of an editable doc). `AGI_LAND=<AA3.2 extracted> sh lanes.sh` = 11 ok + FAIL 4m + FAIL 4v, exit 2; with all FOUR AA3.4 fixes too (`GROW_GATE=<fixed>`): 13/13, exit 0. 4m + 4v ARE the blocking order DG1 wrote.
RUNNER (AA2): the build commits this block VERBATIM as extensions/agi/tests/aa3-lanes.t.sh; goal:g7.16.1.11.13 falsifier 1 = `sh extensions/agi/tests/aa3-lanes.t.sh` (17 now -> 2 once agi-land is built -> 0 once the byte fixes land).
```sh
#!/bin/sh
# lanes.sh [TRUNK] [GITDIR]: AA3.3's 17 lanes on a throwaway repo borrowing GITDIR's objects (0 shared refs written). One line per lane: ok | FAIL; exit = the number of FAILs.
# EVERY tool, agi-land included, comes from TRUNK by sect (reviewed engine nodes, never a prose doc); $GROW_GATE / $AGI_LAND test a candidate. Keys are scratch keys named as the real posts.
# Committed as extensions/agi/tests/aa3-lanes.t.sh (AA2's runner admits `sh extensions/agi/tests/<name>.t.sh`); exit = the number of FAILs, 17 = agi-land not built.
T=${1:-local-maxxing/season2/main};G=${2:-$(git rev-parse --path-format=absolute --git-common-dir)};D=$(mktemp -d);trap 'rm -rf $D' EXIT;mkdir $D/b $D/k
o=$(git rev-parse $T)||exit 1;for x in sect grow-check grow-gate agi-fill agi-gate agi-project agi-land;do git ls-tree --full-tree --name-only $o .agi/nodes/.geometry/|grep '/engine[^/]*\.md$'|sed "s|^|$o:|"|git cat-file --batch --follow-symlinks|sed -n "/^###* $x /,/^###* /{/^~~~/,/^~~~/{//!p}}">$D/b/$x;done
[ "$GROW_GATE" ]&&cp $GROW_GATE $D/b/grow-gate;[ "$AGI_LAND" ]&&cp $AGI_LAND $D/b/agi-land;chmod +x $D/b/*;[ -s $D/b/agi-land ]||{ echo "FAIL all 17 lanes: no ### agi-land in .geometry/engine*.md at $T (not built; AGI_LAND=<file> tests a candidate)";exit 17;}
for p in sanctuary-master director-general-1 alive all-is-one belam thought-master-new;do ssh-keygen -qN "" -ted25519 -f$D/k/$p;echo "$p@agi namespaces=\"git\" $(cut -d' ' -f1,2 $D/k/$p.pub)">>$D/ring;done
git init -q $D/r;echo $G/objects>$D/r/.git/objects/info/alternates;cd $D/r;git update-ref refs/heads/trunk $o;export PATH=$D/b:$PATH AGI_RING=$D/ring AGI_TRUNK=refs/heads/trunk
mk(){ x=$D/i;GIT_INDEX_FILE=$x git read-tree $3;GIT_INDEX_FILE=$x git update-index --add --cacheinfo 100644,$(git hash-object -w $5),$4;t=$(GIT_INDEX_FILE=$x git write-tree);rm -f $x
GIT_COMMITTER_NAME=$2 GIT_COMMITTER_EMAIL=$2@agi GIT_AUTHOR_NAME=$2 GIT_AUTHOR_EMAIL=$2@agi git -c gpg.format=ssh -c user.signingkey=$D/k/$1 commit-tree -S -p $3 -m lane $t;}
C=.agi/nodes/doc/card-director-general-1.md;git show $o:$C>$D/c;echo lane>>$D/c;printf -- '---\nid: hypothesis:zz-lane\ntype: hypothesis\ntitle: lane\n---\n# lane\n'>$D/h
L(){ git update-ref refs/heads/trunk $o;w=$1;n=$2;shift 2;agi-land "$@">$D/out 2>&1;[ $(git rev-parse trunk) != $o ]&&v=land||v=refuse;[ $v = $w ]&&echo "ok   $n  [$(tail -1 $D/out|cut -c1-60)]"||{ F=$((F+1));echo "FAIL $n (want $w, got $v: $(tail -1 $D/out|cut -c1-80))";};}
g=$(mk director-general-1 director-general-1 $o $C $D/c);m=$(mk sanctuary-master sanctuary-master $o $C $D/c);q=$(mk belam belam $o $C $D/c)
L land "1 SM lands DG1" sanctuary-master director-general-1 $g
L refuse "2 forged: alive's key, committer DG1" sanctuary-master director-general-1 $(mk alive director-general-1 $o $C $D/c)
L refuse "3 SM lands alive" sanctuary-master alive $(mk alive alive $o $C $D/c)
L refuse "3b DG1 lands itself" director-general-1 director-general-1 $g
L refuse "3c member all-is-one lands SM (inert keep passes through to belam)" all-is-one sanctuary-master $m
L land "3d belam lands SM through the inert keep" belam sanctuary-master $m
L refuse "3h SM lands itself (a member of its parent group)" sanctuary-master sanctuary-master $m
L refuse "3i peer TM-new lands SM" thought-master-new sanctuary-master $m
L land "3j belam lands TM-new through the inert keep" belam thought-master-new $(mk thought-master-new thought-master-new $o $C $D/c)
L refuse "3e DG1 lands its parent SM" director-general-1 sanctuary-master $m
L refuse "3g belam lands alive (council's lands mask)" belam alive $(mk alive alive $o $C $D/c)
L refuse "3k council member all-is-one lands alive (council lands [])" all-is-one alive $(mk alive alive $o $C $D/c)
L land "3f belam (parent owner) lands itself" belam belam $q
b=$(mk director-general-1 director-general-1 $o .agi/nodes/hypothesis/zz-lane.md $D/h);L refuse "4 parentless hypothesis" sanctuary-master director-general-1 $b
s2=$(mk director-general-1 director-general-1 $o .agi/nodes/doc/card-sanctuary-master.md $D/c);x=$D/j;GIT_INDEX_FILE=$x git read-tree $(git merge-tree --write-tree $g $s2);GIT_INDEX_FILE=$x git update-index --add --cacheinfo 100644,$(git hash-object -w $D/h),.agi/nodes/hypothesis/zz-lane.md;e=$(GIT_INDEX_FILE=$x git write-tree);rm -f $x
L refuse "4m a signed merge adding a node in NEITHER parent (diff-tree skips merges before AA3.4 fix 4)" sanctuary-master director-general-1 $(GIT_COMMITTER_EMAIL=director-general-1@agi GIT_AUTHOR_EMAIL=director-general-1@agi git -c gpg.format=ssh -c user.signingkey=$D/k/director-general-1 commit-tree -S -p $g -p $s2 -m lane $e)
L refuse "5 not ff (on trunk~1)" sanctuary-master director-general-1 $(mk director-general-1 director-general-1 $(git rev-parse $o~1) $C $D/c)
git update-ref refs/heads/posts/director-general-1 $b;L refuse "4v lane 4 with posts/<p> pointing at it (vacuous before AA3.4)" sanctuary-master director-general-1 $b
exit ${F:-0}
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

## AA3.12 Landing from a post's OWN object store (belam ruling 2, 00:35Z = the owner's option (b); measured 00:4xZ)
Owner: "store a git object store per user instead ... post node updates to maybe also store a filesystem pointer to where a given posts object store is at."
Shape (AA1 alive, sizes measured on real data): ONE trunk-only COMMONS readable by all (the trunk is public: it goes to GitHub); each post's store = a bare ~/git whose objects/info/alternates -> the commons, holding ONLY its own unlanded objects (31-159 KB; alive's real store 856 KB; commons 207 MB once). Alternates point at the COMMONS, never at MAIN: today's MAIN holds every posts/* branch, so alternates into it would expose them all.
The land path: root FETCHES the post's branch from its store into the commons, then every AA3 check runs unchanged. The asked sha must be ON that branch.
```diff
4c4,6
< T=${AGI_TRUNK:-refs/heads/trunk};A=${AGI_RING:?};o=$(git rev-parse -q --verify $T)||exit 1;n=$(git rev-parse -q --verify "$3^{commit}")||exit 1
---
> T=${AGI_TRUNK:-refs/heads/trunk};A=${AGI_RING:?};o=$(git rev-parse -q --verify $T)||exit 1
> s=$(git show $o:.agi/nodes/.geometry/posts.md|sed -n 's/^  - {/{/p'|jq -r --arg p $2 'select(.name==$p)|.store//empty');git fetch -q ${s:-${AGI_HOMES:-/var/lib/agi}/$2/git} posts/$2||{ echo "refused: no store for $2";exit 1;}
> n=$(git rev-parse -q --verify "$3^{commit}")&&git merge-base --is-ancestor $n FETCH_HEAD||{ echo "refused: $3 is not on $2's branch";exit 1;}
```
The row cell `store` is the owner's pointer, graph-led: absent = the unit's fixed home path /var/lib/agi/<p>/git, so a local post needs no cell; a post on another box names its store there.
+313 B in agi-land (1,797 -> 2,110) · +22 B unit (`StateDirectoryMode=0750`: homes are 755 today, so any post reads any home) · whole (b) shape ~1,053 B expansion (AA1 sum), 0 B in the zygote.
| lane (scratch: receiving repo + one --shared post store) | got |
|---|---|
| before the land, the receiving repo has the post's commit? | NO (private until landed) |
| SM lands DG1's tip from DG1's store | land |
| a DG1-signed sha NOT on posts/director-general-1 | refused "is not on director-general-1's branch" |
| a post with no store | refused "no store for alive" |
NOT tested without root: the uid barrier itself (0750 homes). Risk: an alternates store breaks if the commons loses objects it references; the commons only grows by lands and never deletes a ref, so maint_gc must never prune it.

## AA3.13 The gate side as shell tests (owner 14:0xZ 10-02: "can the tests also be shell scripts"; council split: AA1.T alive = true state · AA3 = gates · AA2 = test as a matrix row)
MEASURED (trunk 1517e4b7d, 14:1xZ): ZERO pytest tests guard grow-gate, grow-check, agi-gate or agi-land (the only test file naming those pieces, test_agi_boot.py, covers agi-boot). Their ONLY test is AA3.9 lanes.sh: 13 lanes, 4.06 s wall end to end (5 ssh keygens, a throwaway alternates repo, the real trunk tools by sect, agi-gate's full unit projection).
It needs no pytest: sh · git · jq · awk · ssh-keygen · python3 (agi-fill alone is python; `import pytest` fails for a v5 uid, AA1.T).
SHAPE (common with AA1.T's agi-meter.t.sh, agreed 14:0xZ): one file per piece, extracted from its node by sed, one `ok <case>` / `FAIL <case>` line each, exit = the number of FAILs. lanes.sh now exits 2 on today's trunk (4m + 4v, the byte-fix witnesses) and 0 with all four AA3.4 fixes, measured.
For DG1: a gate change lands only with its lanes green (exit 0); the lanes run as the row `sh extensions/agi/tests/aa3-lanes.t.sh` (AA3.9 RUNNER line), never as code sliced from this doc; the 7,917 old-setup tests retire with their code, never ported (AA1.T).


## AA3.14 The keep round, part (2): an inert group passes a land through to its parent; `lands: []` = none (belam [decision] 20:0xZ 10-02; pass-through + null-vs-[] = self-perpetuating 19:59Z / 20:03Z, AA2; council cell = alive 20:02Z)
RULE: a row with a `members` cell is an INERT group (no branch, no level, sends nothing). For post p with parent Q: Q non-inert -> the lander is Q; Q inert -> the lander is parent(Q). The mask is ALWAYS lands(Q), the immediate parent's cell: ABSENT = all children, [] = NONE (jq emits a "Q>" marker for any cell; select(.) keeps [], drops null), so no post name is magic. No member lookup is left, so a group member can never land itself or a peer (the members path would have let SM land itself once parent(SM) = keep). The literal "council" is gone. 1,797 -> 1,829 B (+32).
```diff
@@ -1,12 +1,13 @@
 #!/bin/sh
-# agi-land <sender> <post> <sha>: root ff-lands <post>'s <sha> on the trunk, ONE parent edge up: sender = parent(post); parent "council" (inert row) = a name in its members cell (absent = nobody); a parent-owner post lands itself; a `lands` cell on the parent narrows which children it takes (AA2: council lands only SM).
+# agi-land <sender> <post> <sha>: root ff-lands <post>'s <sha> on the trunk, ONE parent edge up: sender = parent(post); a parent with a members cell is an inert group: the land passes to ITS parent; a parent-owner post lands itself; a `lands` cell on the parent narrows which children it takes (absent = all, [] = none).
 # each commit in $o..$n signed (root's ring) by the sender or a post under <post> on the parent cells · grow-gate on $o..$n · agi-gate · CAS ff
 T=${AGI_TRUNK:-refs/heads/trunk};A=${AGI_RING:?};o=$(git rev-parse -q --verify $T)||exit 1;n=$(git rev-parse -q --verify "$3^{commit}")||exit 1
 git merge-base --is-ancestor $o $n||{ echo "refused: not ff";exit 1;};t=$(mktemp -d);trap 'rm -rf $t' EXIT
-git show $o:.agi/nodes/.geometry/posts.md|sed -n 's/^  - {/{/p'|jq -r '"\(.name) \(.parent//"")",(select(.name=="council")|.members[]?|"M \(.)"),(.name as $n|.lands[]?|"\($n)>\(.)")'>$t/p
+git show $o:.agi/nodes/.geometry/posts.md|sed -n 's/^  - {/{/p'|jq -r '"\(.name) \(.parent//"")",(select(.members)|"I \(.name)"),(.name as $n|.lands|select(.)|"\($n)>",(.[]|"\($n)>\(.)"))'>$t/p
 u(){ x=$1;while [ "$x" ];do [ $x = $2 ]&&return;x=$(awk -v n=$x '$1==n{print $2}' $t/p);done;return 1;}
-grep -qx "$2 $1" $t/p||{ grep -qx "$2 council" $t/p&&grep -qx "M $1" $t/p;}||{ [ $1 = $2 ]&&grep -qx "$1 owner" $t/p;}||{ echo "refused: $1 is not the parent of $2";exit 1;}
-P=$(awk -v n=$2 '$1==n{print $2}' $t/p);grep -q "^$P>" $t/p&&! grep -qx "$P>$2" $t/p&&{ echo "refused: $P lands only $(sed -n "s/^$P>//p" $t/p|tr '\n' ' ')";exit 1;}
+q(){ awk -v n=$1 '$1==n{print $2}' $t/p;};Q=$(q $2);P=$Q;grep -qx "I $Q" $t/p&&P=$(q $Q)
+{ [ "$P" != owner ]&&[ "$1" = "$P" ];}||{ [ $1 = $2 ]&&[ "$P" = owner ];}||{ echo "refused: $1 is not the parent of $2";exit 1;}
+grep -q "^$Q>" $t/p&&! grep -qx "$Q>$2" $t/p&&{ m=$(sed -n "s/^$Q>\(.\)/\1/p" $t/p|tr '\n' ' ');echo "refused: $Q lands only ${m:-nothing}";exit 1;}
 for c in $(git rev-list $o..$n);do s=$(git -c gpg.ssh.allowedSignersFile=$A verify-commit --raw $c 2>&1|sed -n 's/.*signature for \([^@]*\)@agi with.*/\1/p')
 [ "$s" ]&&{ [ $s = $1 ]||u $s $2;}||{ echo "refused: $c signed by ${s:-nobody}: not $1, not under $2";exit 1;};done
 echo "$o $n $T"|AGI_ALLOWED=$A AGI_TRUNK=$o AGI_NOT=$o grow-gate||exit 1;agi-gate $n||{ echo "refused: engine would not regrow";exit 1;}
```
LANES: AA3.9 -> 17 lanes for the new rows. 3c turns to refuse; 3d = belam lands SM; 3g = belam lands alive (council lands []); NEW 3h SM lands itself, 3i peer TM-new lands SM, 3j belam lands TM-new, 3k a council member lands alive:
```diff
@@ -1,11 +1,11 @@
-# lanes.sh [TRUNK] [GITDIR]: AA3.3's 13 lanes on a throwaway repo borrowing GITDIR's objects (0 shared refs written). One line per lane: ok | FAIL; exit = the number of FAILs.
+# lanes.sh [TRUNK] [GITDIR]: AA3.3's 17 lanes on a throwaway repo borrowing GITDIR's objects (0 shared refs written). One line per lane: ok | FAIL; exit = the number of FAILs.
-# Committed as extensions/agi/tests/aa3-lanes.t.sh (AA2's runner admits `sh extensions/agi/tests/<name>.t.sh`); exit = the number of FAILs, 13 = agi-land not built.
+# Committed as extensions/agi/tests/aa3-lanes.t.sh (AA2's runner admits `sh extensions/agi/tests/<name>.t.sh`); exit = the number of FAILs, 17 = agi-land not built.
-[ "$GROW_GATE" ]&&cp $GROW_GATE $D/b/grow-gate;[ "$AGI_LAND" ]&&cp $AGI_LAND $D/b/agi-land;chmod +x $D/b/*;[ -s $D/b/agi-land ]||{ echo "FAIL all 13 lanes: no ### agi-land in .geometry/engine*.md at $T (not built; AGI_LAND=<file> tests a candidate)";exit 13;}
-for p in sanctuary-master director-general-1 alive all-is-one belam;do ssh-keygen -qN "" -ted25519 -f$D/k/$p;echo "$p@agi namespaces=\"git\" $(cut -d' ' -f1,2 $D/k/$p.pub)">>$D/ring;done
+[ "$GROW_GATE" ]&&cp $GROW_GATE $D/b/grow-gate;[ "$AGI_LAND" ]&&cp $AGI_LAND $D/b/agi-land;chmod +x $D/b/*;[ -s $D/b/agi-land ]||{ echo "FAIL all 17 lanes: no ### agi-land in .geometry/engine*.md at $T (not built; AGI_LAND=<file> tests a candidate)";exit 17;}
+for p in sanctuary-master director-general-1 alive all-is-one belam thought-master-new;do ssh-keygen -qN "" -ted25519 -f$D/k/$p;echo "$p@agi namespaces=\"git\" $(cut -d' ' -f1,2 $D/k/$p.pub)">>$D/ring;done
@@ -16,10 +16,14 @@
-L land "3c member all-is-one lands SM" all-is-one sanctuary-master $m
-L land "3d member alive lands SM" alive sanctuary-master $m
+L refuse "3c member all-is-one lands SM (inert keep passes through to belam)" all-is-one sanctuary-master $m
+L land "3d belam lands SM through the inert keep" belam sanctuary-master $m
+L refuse "3h SM lands itself (a member of its parent group)" sanctuary-master sanctuary-master $m
+L refuse "3i peer TM-new lands SM" thought-master-new sanctuary-master $m
+L land "3j belam lands TM-new through the inert keep" belam thought-master-new $(mk thought-master-new thought-master-new $o $C $D/c)
-L refuse "3g member all-is-one lands alive (council lands only SM; FAIL until AA2 writes the cell)" all-is-one alive $(mk alive alive $o $C $D/c)
+L refuse "3g belam lands alive (council's lands mask)" belam alive $(mk alive alive $o $C $D/c)
+L refuse "3k council member all-is-one lands alive (council lands [])" all-is-one alive $(mk alive alive $o $C $D/c)
```
MEASURED 20:0xZ on scratch trunks = 77e90611b + the Q2 rows (keep{SM, TM-new} lands [SM, TM-new], SM + TM-new parent -> keep; objects only, NO ref):
| agi-land | lanes | rows | result |
|---|---|---|---|
| AA3.14 | 17 | Q2 + council lands [] | 15 ok + FAIL 4m + 4v (exit 2; the pre-existing AA3.4 grow-gate witnesses). 3g: "refused: council lands only nothing" |
| AA3.14 | 17 | Q2 + council lands [SM] or ["none"] | the same 15 ok |
| AA3.14 without the null-vs-[] check | 17 | Q2 + council lands [] | + FAIL 3g: belam LANDS alive ([] read as no cell = all children: the trap) |
| AA3.2 (today) | 16 | Q2 rows | + FAIL 3d, 3j: SM and TM-new landable by NOBODY (belam: "the keep row alone makes SM unlandable") |
| AA3.14 | 13 | today's trunk | + FAIL 3c, 3d: council members no longer land SM. So code + rows + lanes move in ONE update (the atomic round) |
THE ROUND'S ROWS (part 4, belam writes): keep {parent belam, members [sanctuary-master, thought-master-new], lands [sanctuary-master, thought-master-new]} · SM + TM-new parent -> keep · council lands [] (council docs keep reaching the trunk through SM's gate; belam landing members directly = a new trunk writer nobody asked for, alive 20:02Z).
FOR DG1: the round commits AA3.14 agi-land in place of AA3.2 and the 17-lane block as extensions/agi/tests/aa3-lanes.t.sh; the falsifier at the merge-up = 17 lanes on the trunk tip, exit 2 until the AA3.4 grow-gate fixes, then 0.

ROUND RESULT (DG1, 10-02 ~21:3xZ, the atomic level round, scratch tip 376aba3a5 = round files + the keep rows; an object only, no ref): AA3.2 and AA3.9 above are now the AA3.14 text (1,829 B, 17 lanes; extensions/agi/tests/aa3-lanes.t.sh is the AA3.9 block verbatim, cmp-checked). `AGI_LAND=<AA3.2 as committed> sh extensions/agi/tests/aa3-lanes.t.sh <tip>` = 15 ok + FAIL 4m + FAIL 4v, exit 2 (the AA3.4 grow-gate witnesses, unchanged). WITHOUT the candidate the lanes exit 17: agi-land is still NOT an engine node (no `### agi-land` in .geometry/engine*.md), so the root-side build stays DG3's lane. The rows (belam writes): keep {parent belam, members + lands = [sanctuary-master, thought-master-new], role council, no harness cell}, SM + TM-new parent -> keep, council lands []. The a() line in the box piece (engine-post.md) is alive's 444 B level line; box 1,927 -> 2,005 B (the comment is shorter by 38 B than the line it replaces).



## AA3.15 Rule edits on v5, the LAND side of goal:g7.16.1.11.17 (3) config ring + (4) anchor (belam [rule] 02:34Z 10-03; council split 02:35Z: alive = the gate lines, AA1.C · self-perpetuating = keys and custody, LEAD of the one story (AA2 §AB, owner 02:37Z) · all-is-one = the land side + review; DESIGN ONLY, owner hold 21:3xZ stands)
TRUE STATE (built pieces, trunk 82eef92e7, 02:4xZ): grow-gate rings only ADDED nodes; a CHANGED node gets the agi-fill ratchet and NO signer check; .agi/context/schemas/* and growth.tsv are never scanned (.agi/nodes, *.md only). agi-land admits a commit only if its signer is the sender or a post UNDER the landed post, so every edit signed from ABOVE (an anchor, the owner, belam re-vouching a post) is refused at the land before any gate reads it.
THE LAND RULE (§AB form, 03:0xZ): ANCESTOR-OR-SELF. A commit in the range passes agi-land's signer check iff its signer is under the landed post OR the post is under its signer (the sender is an ancestor, so it is subsumed; the inert-group pass-through too). Which PATHS an ancestor may change is the gate's job (§AB ring-gate: each changed path is admitted only if the signer rules it or is above its ruler; schemas + growth.tsv ruled by the owner). This REPLACES the earlier AGI_ANCHOR line of this section (02:4xZ: an anchor allowed-signers file + path scope, +232 B): §AB retires the separate anchor file. 1,855 -> 1,857 B (+2, the refusal text):
```diff
@@ -9,6 +9,6 @@
 { [ "$P" != owner ]&&[ "$1" = "$P" ];}||{ [ $1 = $2 ]&&[ "$P" = owner ];}||{ echo "refused: $1 is not the parent of $2";exit 1;}
 grep -q "^$Q>" $t/p&&! grep -qx "$Q>$2" $t/p&&{ m=$(sed -n "s/^$Q>\(.\)/\1/p" $t/p|tr '\n' ' ');echo "refused: $Q lands only ${m:-nothing}";exit 1;}
 for c in $(git rev-list $o..$n);do s=$(git -c gpg.ssh.allowedSignersFile=$A verify-commit --raw $c 2>&1|sed -n 's/.*signature for \([^@]*\)@agi with.*/\1/p')
-[ "$s" ]&&{ [ $s = $1 ]||u $s $2;}||{ echo "refused: $c signed by ${s:-nobody}: not $1, not under $2";exit 1;};done
+[ "$s" ]&&{ u $s $2||u $2 $s;}||{ echo "refused: $c signed by ${s:-nobody}: neither above nor under $2";exit 1;};done
 echo "$o $n $T"|AGI_ALLOWED=$A AGI_TRUNK=$o AGI_NOT=$o grow-gate||exit 1;agi-gate $n||{ echo "refused: engine would not regrow";exit 1;}
 git update-ref $T $n $o
```
The tree is read ONCE, from posts.md at the receiving tip $o: a range cannot raise its own signer inside one land. Across lands it can (alive 02:55Z: a posts.md ring member re-parents itself above a post, then signs as its ancestor), so a tree-cell change (parent, members, lands) must be a RULES edit (alive's lean, backed here).
MEASURED (scratch, objects only; the throwaway repo's own refs):
| lane | want | built agi-land | AA3.15 agi-land |
|---|---|---|---|
| the 17 AA3 lanes (1-5, 3b-3k, 4m, 4v) | as AA3.14 | ok | ok |
| 6u an owner-signed card edit inside DG1's range (owner = an ancestor) | land | REFUSE (FAIL) | land |
| 6v an alive-signed card edit inside DG1's range (neither above nor under) | refuse | refuse | refuse |
| 6c a belam-signed edit inside DG1's range | land (§AB closure, C13) | REFUSE | land at agi-land; the path rule is ring-gate's |
AA2.57, the K lanes THROUGH agi-land with §AB ring-gate (729227ae5e4e1504) as its gate (a 3-line shim: agi-land pipes "o n T", ring-gate takes R N) and ckpt (ce310b2268792c67); fixture = trunk + a ring file (belam, SM, DG1 gen1) = R0, DG1's gen1-signed handoff to gen2 = R1, checkpoints signed belam + SM (k = 2):
| lane | want | built agi-land | AA3.15 agi-land |
|---|---|---|---|
| K0 GRACE: retired gen1 signs after its handoff, newest checkpoint BELOW the handoff | land | land | land |
| K1 the new gen2 key signs after the handoff | land | land | land |
| K2 retired gen1 signs, newest checkpoint ABOVE its handoff | refuse | refuse | refuse "not signed by a ring line open above the latest checkpoint" |
| K3 the same commit BACKDATED 10 days | refuse | refuse | refuse (no date is read) |
| K4 gen2 signs after that checkpoint | land | land | land |
| K-anc belam (an ancestor of DG1) signs a card edit inside DG1's range | land | REFUSE (FAIL) | land |
BLOCK SHAPE (self-perpetuating mu5 b784f9847, 03:0xZ: refs/agi/block/<name>, a DAG; ring-gate 668cc669efdf796c, ckpt b944222c7681ba26, both UNCHANGED), the same fixture ported (k0 = belam + SM over R0; k1 seals k0, over R1) + an owner CA in the ring. Every owner cert is issued ON belam's current ring key: by design (C18) a cert counts only on a key that IS a current ring line, so it dies with its subject's generation:
| lane | want | built agi-land | AA3.15 agi-land |
|---|---|---|---|
| K0 K1 K2 K3 K4 | as above | as above | as above |
| K-anc belam (an ancestor of DG1) signs inside DG1's range | land | REFUSE (FAIL) | land |
| T9 an owner cert (on belam's key) expired before the newest block, commit backdated into its window | refuse | refuse | refuse "owner cert expired before the newest holding block" |
| T10 an owner cert (on belam's key) valid at the newest block | land | REFUSE (FAIL) | land |
| T11 an owner@agi cert from a CA NOT in the ring, on belam's key | refuse | refuse | refuse |
| E1 SM (posts.md ring member) re-parents belam under itself; belam lands SM | refuse | refuse | refuse "ruled by owner" |
Exit 0 with ring-gate 668cc669 + the AA3.15 agi-land; the built agi-land fails K-anc + T10, both for the one reason this section fixes (a signer ABOVE the landed post). RETRACTED (03:1xZ): a first run issued the certs on FRESH keys and read T10's refusal as a ring-gate bug; it is the C18 binding working, and the proposed "+40 B" line would have re-admitted a cert on a RETIRED generation (self-perpetuating measured: C18 then FAILs). ring-gate stays 668cc669.
Fixture trap: a cert signs only through `ssh-keygen -Y sign -f <key>-cert.pub` (git: user.signingkey = the -cert.pub path); `-f <key>` with the cert beside it signs as the bare key (measured, OpenSSH 9.6p1).
So the land side of §AB is ONE rule (+2 B). NOT run here: §AB's K5/K6 (owner cert expiry) need a CA fixture; the AA1.C-integrated measurement of 02:5xZ (27 lanes: built 6 / AA1.C 1 / both 0, with an anchor file and AGI_FRESH_S) stands as the record of a design §AB superseded.
COMMIT SIGNATURES (measured 02:5xZ): a git commit carries ONE signature slot (gpgsig; gpgsig-sha256 only in a sha256 repo; this repo = sha1). agi-land reads the signer from git's SSH verify text, which is key-type agnostic (ED25519 and ECDSA both parse). So a hybrid (classical AND PQ) commit is ONE composite blob verified by the program the sign cell names (gpg.ssh.program, which git calls for sign AND verify), and a k-of-n block is k signature blobs beside the commit (§AB's ckpt: sigs/<post>.<n>), never k signatures on one commit.
AA2.71 THE PRIVATE-KEY LINE (v1; SUPERSEDED by v2 below: two fail-opens) (the trunk is pushed to a PUBLIC origin, so a range carrying ANY private key block, live or retired, is refused AT the land; a publication lives only on refs/revoked, ruled by self-perpetuating's revoke; pattern = alive's AA1.K, placement = this section, alive 03:25Z). One line per commit in grow-gate, beside the signer read (283 B; grow-gate 1,465 -> 1,748 B): every path the commit adds or changes, binaries and merges included (-z + tr: no path quoting; -c: a merge's own paths; grep -a: binaries; the ':' keeps a no-match iteration from failing the loop):
```text
 git diff-tree -r -c -z --root --no-commit-id --diff-filter=AM --name-only $c|tr '\0' '\n'|while IFS= read -r f;do git show "$c:$f"|grep -aq -e '-----BEGIN [A-Z0-9 ]*PRIVATE KEY-----'&&{ echo "refused: $c $f carries a private key block (the trunk is public)";exit 1;};:;done||exit 1
```
| lane (through the built agi-land) | want | built grow-gate | AA1.K pattern in grow-gate's node loop | the line above |
|---|---|---|---|---|
| P1 a LIVE ed25519 key in a card | refuse | LAND (FAIL) | refuse | refuse |
| P2 a RETIRED key in a card (revoke would admit it on refs/revoked) | refuse | LAND (FAIL) | refuse | refuse |
| P3 an RSA PEM key in a card | refuse | LAND (FAIL) | refuse | refuse |
| P4 a passphrase-ENCRYPTED key in a card | refuse, no hang | LAND (FAIL) | refuse | refuse |
| P5 control: PUBLIC KEY + SSH SIGNATURE blocks + prose naming a private key | land | land | land | land |
| P6 a live key in extensions/agi/zz-leak.txt | refuse | LAND (FAIL) | LAND (FAIL) | refuse |
| P7 a live key in .agi/nodes/deprecated/doc/zz-leak.md | refuse | LAND (FAIL) | LAND (FAIL) | refuse |
| P8 a live key in .agi/nodes/.geometry/zz-leak.tsv | refuse | LAND (FAIL) | LAND (FAIL) | refuse |
| P9 a DG1-signed MERGE adding a key file in NEITHER parent | refuse | LAND (FAIL) | LAND (FAIL) | refuse |
Exit: built 8 · node-loop placement 4 · this line 0; the 17 AA3 lanes stay exit 0 with it. The lane block (appended to aa3-lanes.t.sh; fixture keys are generated in the throwaway repo, never a real key):
```text
# AA2.71: a range carrying a PRIVATE KEY block anywhere is refused AT the land (the trunk is pushed to a public origin)
k(){ cat $D/c>$D/$1;cat $2>>$D/$1;}
ssh-keygen -qN "" -ted25519 -f$D/live;ssh-keygen -qN "" -ted25519 -f$D/ret;ssh-keygen -qN "" -trsa -b 2048 -m PEM -f$D/rsa;ssh-keygen -qN "pass phrase" -ted25519 -f$D/enc
printf -- '-----BEGIN PUBLIC KEY-----\nMCowBQYDK2VwAyEAx\n-----END PUBLIC KEY-----\n-----BEGIN SSH SIGNATURE-----\nU1NIU0lH\n-----END SSH SIGNATURE-----\nthe word PRIVATE KEY in prose\n'>$D/nk
k p1 $D/live;k p2 $D/ret;k p3 $D/rsa;k p4 $D/enc;k p5 $D/nk
for x in 1 2 3 4 5;do eval c$x=\$\(mk director-general-1 director-general-1 \$o \$C \$D/p$x\);done
L refuse "P1 a LIVE ed25519 key in a card" sanctuary-master director-general-1 $c1
L refuse "P2 a RETIRED key in a card (revoke would admit it on refs/revoked; the trunk is public)" sanctuary-master director-general-1 $c2
L refuse "P3 an RSA PEM key in a card" sanctuary-master director-general-1 $c3
L refuse "P4 a passphrase-ENCRYPTED key in a card (no hang)" sanctuary-master director-general-1 $c4
L land "P5 control: PUBLIC KEY + SSH SIGNATURE blocks + prose naming a private key" sanctuary-master director-general-1 $c5
L refuse "P6 a live key in a NON-node file (extensions/agi/zz-leak.txt)" sanctuary-master director-general-1 $(mk director-general-1 director-general-1 $o extensions/agi/zz-leak.txt $D/live)
L refuse "P7 a live key in a RETIRED node (.agi/nodes/deprecated/doc/zz-leak.md)" sanctuary-master director-general-1 $(mk director-general-1 director-general-1 $o .agi/nodes/deprecated/doc/zz-leak.md $D/p1)
L refuse "P8 a live key in a non-.md node file (.agi/nodes/.geometry/zz-leak.tsv)" sanctuary-master director-general-1 $(mk director-general-1 director-general-1 $o .agi/nodes/.geometry/zz-leak.tsv $D/live)
g9=$(mk director-general-1 director-general-1 $o $C $D/c);s9=$(mk director-general-1 director-general-1 $o .agi/nodes/doc/card-sanctuary-master.md $D/c)
x=$D/j9;GIT_INDEX_FILE=$x git read-tree $(git merge-tree --write-tree $g9 $s9);GIT_INDEX_FILE=$x git update-index --add --cacheinfo 100644,$(git hash-object -w $D/live),extensions/agi/zz-merge.txt;e9=$(GIT_INDEX_FILE=$x git write-tree);rm -f $x
L refuse "P9 a DG1-signed MERGE adding a key file in NEITHER parent" sanctuary-master director-general-1 $(GIT_COMMITTER_EMAIL=director-general-1@agi GIT_AUTHOR_EMAIL=director-general-1@agi git -c gpg.format=ssh -c user.signingkey=$D/k/director-general-1 commit-tree -S -p $g9 -p $s9 -m lane $e9)
```
AA2.71 v2 (REJECTED 04:09Z: fails open on a blob it cannot read, see OPTION B below; SM's Sonnet refuter on DG3's build 45d468f83, 03:4xZ, both REPRODUCED here through the built pieces): v1 fails open on (P10) a path holding a NEWLINE (tr '\0' '\n' splits it, git show finds neither half, the loop passes) and (P11) a file CHANGED to a symlink whose target bytes are the key block (type change T, dropped by --diff-filter=AM). v2 reads each entry's RESULT blob id from diff-tree's raw line (the field before the status, in the plain AND the combined -c form) and cats that blob: no path is ever re-parsed (git C-quotes a control character in a raw path, so one entry = one line), and only deletions are skipped (--diff-filter=d: A M T and any status git adds later are read; a gitlink has no blob here and is skipped). The refusal names the path as git quotes it, through printf %s (dash's echo would expand a backslash in a path). 326 B; grow-gate 1,465 -> 1,793 B:
```text
 git diff-tree -r -c --root --no-commit-id --diff-filter=d $c|awk -F'\t' '{n=split($1,a," ");print a[n-1],$2}'|while read -r o f;do git cat-file blob $o 2>/dev/null|grep -aq -e '-----BEGIN [A-Z0-9 ]*PRIVATE KEY-----'&&{ printf 'refused: %s %s carries a private key block (the trunk is public)\n' $c "$f";exit 1;};:;done||exit 1
```
| lane (through the built agi-land) | want | v1 | v2 |
|---|---|---|---|
| P1-P9 (above) | as above | 9/9 | 9/9 |
| P10 a live key at a path holding a NEWLINE | refuse | LAND (FAIL: "path 'leak.txt' does not exist") | refuse |
| P11 a card CHANGED to a symlink whose target is a key block (T) | refuse | LAND (FAIL) | refuse |
| P12 a NEW symlink whose target is a key block | refuse | refuse | refuse |
| P13 control: a NEW symlink with a plain target | land | land | land |
Exit: v1 2 · v2 0. DG3's grow-gate-keys.t.sh (45d468f83) with v2: 0 FAIL but f7-bytes, whose bound moves 1,748 -> 1,793. The AA3 lane verdicts are identical v1 vs v2 (lanes.anc.sh, trunk 2c59fd5f6). The lanes appended to the block above:
```text
# v2: a path holding a newline, and a type change (T); mm = mk with a mode
mm(){ x=$D/i;GIT_INDEX_FILE=$x git read-tree $3;GIT_INDEX_FILE=$x git update-index --add --cacheinfo "$6,$(git hash-object -w $5),$4";t=$(GIT_INDEX_FILE=$x git write-tree);rm -f $x
GIT_COMMITTER_NAME=$2 GIT_COMMITTER_EMAIL=$2@agi GIT_AUTHOR_NAME=$2 GIT_AUTHOR_EMAIL=$2@agi git -c gpg.format=ssh -c user.signingkey=$D/k/$1 commit-tree -S -p $3 -m lane $t;}
L refuse "P10 a live key at a path holding a NEWLINE" sanctuary-master director-general-1 $(mm director-general-1 director-general-1 $o "extensions/agi/zz
leak.txt" $D/live 100644)
L refuse "P11 a card CHANGED to a symlink whose target is a key block (type change T)" sanctuary-master director-general-1 $(mm director-general-1 director-general-1 $o $C $D/live 120000)
L refuse "P12 a NEW symlink whose target is a key block" sanctuary-master director-general-1 $(mm director-general-1 director-general-1 $o extensions/agi/zz-ln $D/live 120000)
L land "P13 control: a NEW symlink with a plain target" sanctuary-master director-general-1 $(mm director-general-1 director-general-1 $o extensions/agi/zz-ln2 $D/nk 120000)
```
Honest limit (v1 and v2): the line refuses an ARMOURED block (-----BEGIN ... PRIVATE KEY-----). A key that is base64'd again, compressed, split across lines, or in a non-armoured format (a PuTTY .ppk, a raw hex seed) passes. Catching every encoding is not decidable from bytes; the line covers the paste and commit-the-file accidents, not a determined leaker.
AA2.71 THE RULED LINE = OPTION B (DG1 [rule] 04:02Z; built by DG3 on dg3-keygate eb6bee25e; grow-gate 1,465 -> 1,833 B = the bar; this line 366 B, its separator is a literal TAB). v2 fails open where B refuses: `git cat-file blob $o 2>/dev/null|grep` reads an unreadable blob (or a gitlink oid) as "no key" and lands it; B writes the blob to $t/b and REFUSES on a read error, naming the path (DG2 lanes r2b-unreadable-blob + r2b-unreadable-newline-path, measured by DG3 04:09Z: v2 2 FAIL, B 0). B's --diff-filter=AMT names every status diff-tree emits without -M/-C/-B, so it equals v2's d today. Consequence: a commit adding a submodule (gitlink, no blob here) is refused, owner lands. P1-P13 above through dg3-keygate's built pieces: 13/13 exit 0. Cosmetic: B's refusal is an echo, so dash expands the \n of a git-quoted newline path and the refusal prints on two lines (the path is still exact, the commit still refused):
```text
 git diff-tree -r -c --root --no-commit-id --diff-filter=AMT $c|while IFS= read -r l;do p=${l#*	};o=$(echo "${l%%	*}"|awk '{print $(NF-1)}');git cat-file blob $o>$t/b||{ echo "refused: $c $p unreadable";exit 1;};grep -aq -e '-----BEGIN [A-Z0-9 ]*PRIVATE KEY-----' $t/b&&{ echo "refused: $c $p carries a private key block (the trunk is public)";exit 1;};:;done||exit 1
```
REVIEW of the build (AA3.14 as built): agi-land on the trunk differs from AA3.14 v2 in ONE line, the 32-hop bound on the parent walk u() that SM's follow-up 55f502f95 already records (agi-land-bounds.t.sh). Confirmed: correct and fail-closed (a parent cycle or a chain deeper than 32 is refused, never a hang); all 17 AA3.14 lanes stay ok on the built pieces.
