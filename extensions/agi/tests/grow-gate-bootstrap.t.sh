#!/bin/sh
# grow-gate-bootstrap.t.sh: the ring gate opens ONLY while the ring has never existed in the receiving history (git rev-list -1 TIP -- ring prints nothing). Scratch repo borrowing the common gitdir objects, scratch keys; tools from TRUNK by sect, GROW_GATE=<file> tests a candidate. One ok/FAIL line per case; exit = number of FAILs.
T=local-maxxing/season2/main;G=$(git rev-parse --path-format=absolute --git-common-dir);D=$(mktemp -d);trap 'rm -rf $D' EXIT;mkdir $D/b $D/k;f=0
o=$(git rev-parse $T)||exit 1;for x in sect grow-check grow-gate agi-fill;do git ls-tree --full-tree --name-only $o .agi/nodes/.geometry/|grep '/engine[^/]*\.md$'|sed "s|^|$o:|"|git cat-file --batch --follow-symlinks|sed -n "/^###* $x /,/^###* /{/^~~~/,/^~~~/{//!p}}">$D/b/$x;done
[ "$GROW_GATE" ]&&cp $GROW_GATE $D/b/grow-gate;chmod +x $D/b/*;[ -s $D/b/grow-gate ]||{ echo "FAIL no grow-gate";exit 99;}
for p in owner legacy;do ssh-keygen -qN "" -ted25519 -f$D/k/$p>/dev/null;done
echo "legacy@agi namespaces=\"git\" $(cut -d' ' -f1,2 $D/k/legacy.pub)">$D/allowed
printf 'owner ssh-ed25519 %s\n' "$(cut -d' ' -f2 $D/k/owner.pub)">$D/ringfile
git init -q $D/r;echo $G/objects>$D/r/.git/objects/info/alternates;cd $D/r;git update-ref refs/heads/trunk $o;export PATH=$D/b:$PATH
# commit on parent $1 with signer $2; $3 = add|del|none of the ring file; $4 = filler name
mk(){ x=$D/i;GIT_INDEX_FILE=$x git read-tree $1
 case $3 in add)GIT_INDEX_FILE=$x git update-index --add --cacheinfo 100644,$(git hash-object -w $D/ringfile),.agi/nodes/.geometry/ring;;del)GIT_INDEX_FILE=$x git update-index --force-remove .agi/nodes/.geometry/ring;;esac
 GIT_INDEX_FILE=$x git update-index --add --cacheinfo 100644,$(echo $4|git hash-object -w --stdin),.agi/context/zz-$4.txt;t=$(GIT_INDEX_FILE=$x git write-tree);rm -f $x
 GIT_COMMITTER_NAME=$2 GIT_COMMITTER_EMAIL=$2@agi GIT_AUTHOR_NAME=$2 GIT_AUTHOR_EMAIL=$2@agi git -c gpg.format=ssh -c user.signingkey=$D/k/$2 commit-tree -S -p $1 -m $4 $t;}
gate(){ echo "$1 $2 refs/heads/x"|AGI_ALLOWED=$D/allowed AGI_TRUNK=$3 AGI_NOT=$1 grow-gate>$D/out 2>&1;}
ok(){ if eval "$2";then echo "ok $1";else echo "FAIL $1 [$(tail -1 $D/out|cut -c1-110)]";f=$((f+1));fi;}
# trunk tip for gate = a ref we advance by hand (the gate reads the RECEIVING tip)
c1=$(mk $o legacy add one);gate $o $c1 refs/heads/trunk;ok a-first-ring-commit-lands '[ $? = 0 ]'
git update-ref refs/heads/trunk $c1
c2=$(mk $c1 owner del two);gate $c1 $c2 refs/heads/trunk;ok b-top-signer-deletes-ring-lands '[ $? = 0 ]'
git update-ref refs/heads/trunk $c2
c3=$(mk $c2 legacy none three);gate $c2 $c3 refs/heads/trunk;ok c-commit-after-ring-deleted-refused '[ $? != 0 ]'
c3b=$(mk $c2 owner none threeb);gate $c2 $c3b refs/heads/trunk;ok d-even-the-owner-is-not-open-after-deletion '[ $? != 0 ]'
# one push holding the deleting commit and an unsigned-by-ring follow-up: the follow-up is refused
c4=$(mk $c2 legacy none four);echo "$c1 $c4 refs/heads/x"|AGI_ALLOWED=$D/allowed AGI_TRUNK=refs/heads/trunk AGI_NOT=$c1 grow-gate>$D/out 2>&1;ok e-in-one-push-follow-up-after-deletion-refused '[ $? != 0 ]'
echo "grow-gate-bootstrap: $f FAIL";exit $f
