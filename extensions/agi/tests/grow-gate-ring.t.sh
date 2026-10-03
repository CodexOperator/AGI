#!/bin/sh
# grow-gate-ring.t.sh [TRUNK] [GITDIR]: AA3.4 fix 3 (hypothesis g716111-aa3-the-three-byte-fixes-...): a growth row whose ring cell names ONE post (moral: `owner`) matches the signer name WITHOUT "@agi".
# Scratch repo borrowing GITDIR's objects (0 shared refs written), scratch keys; tools from TRUNK by sect ($GROW_GATE tests a candidate grow-gate). One ok/FAIL line per case; exit = number of FAILs.
T=${1:-local-maxxing/season2/main};G=${2:-$(git rev-parse --path-format=absolute --git-common-dir)};D=$(mktemp -d);trap 'rm -rf $D' EXIT;mkdir $D/b $D/k;f=0
o=$(git rev-parse $T)||exit 1;for x in sect grow-check grow-gate agi-fill;do git ls-tree --full-tree --name-only $o .agi/nodes/.geometry/|grep '/engine[^/]*\.md$'|sed "s|^|$o:|"|git cat-file --batch --follow-symlinks|sed -n "/^###* $x /,/^###* /{/^~~~/,/^~~~/{//!p}}">$D/b/$x;done
[ "$GROW_GATE" ]&&cp $GROW_GATE $D/b/grow-gate;chmod +x $D/b/*;[ -s $D/b/grow-gate ]||{ echo "FAIL no grow-gate at $T";exit 99;}
for p in owner director-general-1;do ssh-keygen -qN "" -ted25519 -f$D/k/$p>/dev/null;echo "$p@agi namespaces=\"git\" $(cut -d' ' -f1,2 $D/k/$p.pub)">>$D/ring;done
git init -q $D/r;echo $G/objects>$D/r/.git/objects/info/alternates;cd $D/r;git update-ref refs/heads/trunk $o;export PATH=$D/b:$PATH;printf '#!/bin/sh\nexit 0\n'>$D/b/ckpt;chmod +x $D/b/ckpt
git show $o:.agi/nodes/moral/antifragility.md|sed 's/^id: moral:antifragility/id: moral:zz-ring-lane/;s/^mint_id: .*/mint_id: 0123456789abcdef0123456789abcdef/;s/^type: moral/type: moral\nkey: 2fe50ba43c479d67/'>$D/n
mk(){ x=$D/i;GIT_INDEX_FILE=$x git read-tree $o;GIT_INDEX_FILE=$x git update-index --add --cacheinfo 100644,$(git hash-object -w $D/n),.agi/nodes/moral/zz-ring-lane.md;t=$(GIT_INDEX_FILE=$x git write-tree);rm -f $x
 GIT_COMMITTER_NAME=$1 GIT_COMMITTER_EMAIL=$1@agi GIT_AUTHOR_NAME=$1 GIT_AUTHOR_EMAIL=$1@agi git -c gpg.format=ssh -c user.signingkey=$D/k/$1 commit-tree -S -p $o -m ring $t;}
gate(){ echo "$o $1 refs/heads/x"|AGI_ALLOWED=$D/ring AGI_TRUNK=refs/heads/trunk AGI_NOT=$o grow-gate>$D/out 2>&1;}
ok(){ if eval "$2";then echo "ok $1";else echo "FAIL $1 [$(tail -1 $D/out|cut -c1-90)]";f=$((f+1));fi;}
gate $(mk owner);ok r1-ring-owner-signed-by-owner-passes '[ $? = 0 ]'
gate $(mk director-general-1);ok r2-ring-owner-signed-by-another-refused '[ $? != 0 ]&&grep -q "ring owner, signed by director-general-1" $D/out'
exit $f
