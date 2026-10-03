#!/bin/sh
# agi-land-bounds.t.sh [TRUNK] [GITDIR]: agi-land follow-ups on a throwaway repo (0 shared refs written), scratch keys; tools from TRUNK by sect ($AGI_LAND tests a candidate). One ok/FAIL line per case; exit = number of FAILs.
# l1 a parent CYCLE in posts.md ends (the signer walk is bounded: a refusal, never a hang) · l2 the lands-mask refusal names EVERY allowed child
T=${1:-local-maxxing/season2/main};G=${2:-$(git rev-parse --path-format=absolute --git-common-dir)};D=$(mktemp -d);trap 'rm -rf $D' EXIT;mkdir $D/b $D/k;f=0
o=$(git rev-parse $T)||exit 1;for x in sect grow-check grow-gate agi-fill agi-gate agi-project agi-land;do git ls-tree --full-tree --name-only $o .agi/nodes/.geometry/|grep '/engine[^/]*\.md$'|sed "s|^|$o:|"|git cat-file --batch --follow-symlinks|sed -n "/^###* $x /,/^###* /{/^~~~/,/^~~~/{//!p}}">$D/b/$x;done
[ "$AGI_LAND" ]&&cp $AGI_LAND $D/b/agi-land;chmod +x $D/b/*;[ -s $D/b/agi-land ]||{ echo "FAIL no agi-land at $T";exit 99;}
for p in cyc2 par;do ssh-keygen -qN "" -ted25519 -f$D/k/$p>/dev/null;echo "$p@agi namespaces=\"git\" $(cut -d' ' -f1,2 $D/k/$p.pub)">>$D/ring;done
git init -q $D/r;echo $G/objects>$D/r/.git/objects/info/alternates;cd $D/r;export PATH=$D/b:$PATH AGI_RING=$D/ring AGI_TRUNK=refs/heads/trunk
P=.agi/nodes/.geometry/posts.md;C=.agi/nodes/doc/card-director-general-1.md
{ git show $o:$P;printf '%s\n' '  - {"name":"cyc1","parent":"cyc2","harness":"claude"}' '  - {"name":"cyc2","parent":"cyc1","harness":"claude"}' '  - {"name":"zz","parent":"cyc1","harness":"claude"}' '  - {"name":"par","parent":"belam","harness":"claude","lands":["aa","bb"]}' '  - {"name":"aa","parent":"par","harness":"claude"}' '  - {"name":"bb","parent":"par","harness":"claude"}' '  - {"name":"cc","parent":"par","harness":"claude"}';}>$D/p
x=$D/i;GIT_INDEX_FILE=$x git read-tree $o;GIT_INDEX_FILE=$x git update-index --add --cacheinfo 100644,$(git hash-object -w $D/p),$P;t=$(GIT_INDEX_FILE=$x git write-tree);rm -f $x
b=$(GIT_COMMITTER_NAME=x GIT_COMMITTER_EMAIL=x@x GIT_AUTHOR_NAME=x GIT_AUTHOR_EMAIL=x@x git commit-tree -p $o -m fixture $t);git update-ref refs/heads/trunk $b
mk(){ x=$D/i;GIT_INDEX_FILE=$x git read-tree $b;git show $b:$C>$D/c;echo lane>>$D/c;GIT_INDEX_FILE=$x git update-index --add --cacheinfo 100644,$(git hash-object -w $D/c),$C;t=$(GIT_INDEX_FILE=$x git write-tree);rm -f $x
 GIT_COMMITTER_NAME=$1 GIT_COMMITTER_EMAIL=$1@agi GIT_AUTHOR_NAME=$1 GIT_AUTHOR_EMAIL=$1@agi git -c gpg.format=ssh -c user.signingkey=$D/k/$1 commit-tree -S -p $b -m lane $t;}
ok(){ if eval "$2";then echo "ok $1";else echo "FAIL $1 [$(tail -1 $D/out|cut -c1-90)]";f=$((f+1));fi;}
timeout 10 agi-land cyc1 zz $(mk cyc2)>$D/out 2>&1;rc=$?;ok l1-parent-cycle-refuses-not-hangs '[ $rc != 124 ]&&[ $rc != 0 ]&&grep -q "^refused" $D/out'
git update-ref refs/heads/trunk $b;agi-land par cc $(mk par)>$D/out 2>&1;ok l2-lands-mask-names-every-child 'grep -q "par lands only aa bb" $D/out'
exit $f
