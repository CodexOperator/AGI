#!/bin/sh
# lanes.sh [TRUNK] [GITDIR]: AA3.3's 17 lanes on a throwaway repo borrowing GITDIR's objects (0 shared refs written). One line per lane: ok | FAIL; exit = the number of FAILs.
# EVERY tool, agi-land included, comes from TRUNK by sect (reviewed engine nodes, never a prose doc); $GROW_GATE / $AGI_LAND test a candidate. Keys are scratch keys named as the real posts.
# Committed as extensions/agi/tests/aa3-lanes.t.sh (AA2's runner admits `sh extensions/agi/tests/<name>.t.sh`); exit = the number of FAILs, 17 = agi-land not built.
T=${1:-local-maxxing/season2/main};G=${2:-$(git rev-parse --path-format=absolute --git-common-dir)};D=$(mktemp -d);trap 'rm -rf $D' EXIT;mkdir $D/b $D/k
o=$(git rev-parse $T)||exit 1;for x in sect grow-check grow-gate agi-fill agi-gate agi-project agi-land;do git ls-tree --full-tree --name-only $o .agi/nodes/.geometry/|grep '/engine[^/]*\.md$'|sed "s|^|$o:|"|git cat-file --batch --follow-symlinks|sed -n "/^###* $x /,/^###* /{/^~~~/,/^~~~/{//!p}}">$D/b/$x;done
[ "$GROW_GATE" ]&&cp $GROW_GATE $D/b/grow-gate;[ "$AGI_LAND" ]&&cp $AGI_LAND $D/b/agi-land;chmod +x $D/b/*;[ -s $D/b/agi-land ]||{ echo "FAIL all 17 lanes: no ### agi-land in .geometry/engine*.md at $T (not built; AGI_LAND=<file> tests a candidate)";exit 17;};[ -s $D/b/ckpt ]||{ printf '#!/bin/sh\nexit 0\n'>$D/b/ckpt;chmod +x $D/b/ckpt;}
for p in sanctuary-master director-general-1 alive all-is-one belam thought-master;do ssh-keygen -qN "" -ted25519 -f$D/k/$p;echo "$p@agi namespaces=\"git\" $(cut -d' ' -f1,2 $D/k/$p.pub)">>$D/ring;done
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
L refuse "3i peer TM lands SM" thought-master sanctuary-master $m
L land "3j belam lands TM through the inert keep" belam thought-master $(mk thought-master thought-master $o $C $D/c)
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
