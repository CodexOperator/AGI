#!/bin/sh
# grow-gate-bootstrap.t.sh: the ring gate opens ONLY while the ring has never existed in the receiving history (git rev-list -1 TIP -- ring prints nothing). Scratch repo borrowing the common gitdir objects, scratch keys; tools from TRUNK by sect, GROW_GATE=<file> tests a candidate. One ok/FAIL line per case; exit = number of FAILs.
T=local-maxxing/season2/main;G=$(git rev-parse --path-format=absolute --git-common-dir);D=$(mktemp -d);trap 'rm -rf $D' EXIT;mkdir $D/b $D/k;f=0
o=$(git rev-parse $T)||exit 1;for x in sect grow-check grow-gate agi-fill;do git ls-tree --full-tree --name-only $o .agi/nodes/.geometry/|grep '/engine[^/]*\.md$'|sed "s|^|$o:|"|git cat-file --batch --follow-symlinks|sed -n "/^###* $x /,/^###* /{/^~~~/,/^~~~/{//!p}}">$D/b/$x;done
[ "$GROW_GATE" ]&&cp $GROW_GATE $D/b/grow-gate;chmod +x $D/b/*;[ -s $D/b/grow-gate ]||{ echo "FAIL no grow-gate";exit 99;}
for p in owner legacy;do ssh-keygen -qN "" -ted25519 -f$D/k/$p>/dev/null;done
echo "legacy@agi namespaces=\"git\" $(cut -d' ' -f1,2 $D/k/legacy.pub)">$D/allowed
printf 'owner ssh-ed25519 %s\n' "$(cut -d' ' -f2 $D/k/owner.pub)">$D/ringfile
git init -q $D/r;echo $G/objects>$D/r/.git/objects/info/alternates;cd $D/r;git update-ref refs/heads/trunk $o;export PATH=$D/b:$PATH;[ -s $D/b/ckpt ]||{ printf '#!/bin/sh\nexit 0\n'>$D/b/ckpt;chmod +x $D/b/ckpt;}
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
# --- DG1 04:40Z (SM landing note): a git error in the commit walk REFUSES the land (dash has no pipefail: an empty loop would admit). A shim `git` fails ONE subcommand (FAILSUB); the old bytes read RED.
mkdir $D/shim;printf '#!/bin/sh\nskip=;for a in "$@";do [ -n "$skip" ]&&{ skip=;continue;};case $a in -C|-c)skip=1;continue;;-*)continue;;*)sub=$a;break;;esac;done\n[ "$sub" = "$FAILSUB" ]&&{ echo "shim: $sub failed" >&2;exit 1;}\nexec /usr/bin/git "$@"\n' >$D/shim/git;chmod +x $D/shim/git
fgate(){ echo "$1 $2 refs/heads/x"|(FAILSUB=$3 PATH=$D/shim:$PATH AGI_ALLOWED=$D/allowed AGI_TRUNK=refs/heads/trunk AGI_NOT=$1 grow-gate)>$D/out 2>&1;}
git update-ref refs/heads/trunk $o;c9=$(mk $o legacy none nine)
fgate $o $c9 rev-list;ok f-rev-list-error-refuses '[ $? != 0 ]&&grep -q "git rev-list failed" $D/out'
fgate $o $c9 diff-tree;ok g-diff-tree-error-refuses '[ $? != 0 ]&&grep -q "git diff-tree failed" $D/out'
fgate $o $c9 none;ok h-control-no-failure-lands '[ $? = 0 ]'
git update-ref refs/heads/trunk $c1;c10=$(mk $c1 owner del ten)
fgate $c1 $c10 diff;ok i-ring-diff-error-refuses '[ $? != 0 ]&&grep -q "git diff failed" $D/out'
fgate $c1 $c10 none;ok j-control-ring-delete-by-owner-lands '[ $? = 0 ]'
# --- RING.3 (SM mur sm17 on 9abc7c690, D1-D3 + R5): each lane is RED on the demoted piece. Ring names are real posts: owner (top) and all-is-one (under council under belam).
ssh-keygen -qN "" -ted25519 -f$D/k/aio>/dev/null
pkb(){ awk '{print $2}' $D/k/$1.pub;}
printf 'owner ssh-ed25519 %s\nall-is-one ssh-ed25519 %s\n' "$(pkb owner)" "$(pkb aio)">$D/ring2
mkx(){ ps=$1;sg=$2;shift 2;x=$D/i2;GIT_INDEX_FILE=$x git read-tree ${ps%% *}
 for a in "$@";do pa=${a%%:*};fa=${a#*:};if [ "$fa" = - ];then GIT_INDEX_FILE=$x git update-index --force-remove $pa;else GIT_INDEX_FILE=$x git update-index --add --cacheinfo 100644,$(git hash-object -w $fa),$pa;fi;done
 tr=${MTREE:-$(GIT_INDEX_FILE=$x git write-tree)};rm -f $x;pa=;for q in $ps;do pa="$pa -p $q";done
 if [ "$sg" = - ];then git commit-tree $pa -m x $tr;else GIT_COMMITTER_NAME=$sg GIT_COMMITTER_EMAIL=$sg@agi GIT_AUTHOR_NAME=$sg GIT_AUTHOR_EMAIL=$sg@agi git -c gpg.format=ssh -c user.signingkey=$D/k/$sg commit-tree -S $pa -m x $tr;fi;}
g2(){ git update-ref refs/heads/trunk $1;echo "$1 $2 refs/heads/x"|(AGI_ALLOWED=$D/allowed AGI_TRUNK=refs/heads/trunk AGI_NOT=$1 grow-gate)>$D/out 2>&1;}
RG=.agi/nodes/.geometry/ring;PM=.agi/nodes/.geometry/posts.md
C1=$(mkx "$o" legacy $RG:$D/ring2);g2 $o $C1;ok k-first-ring-signed-by-an-allowed-key-lands '[ $? = 0 ]'
M=$(MTREE=$(git rev-parse $o^{tree}) mkx "$C1 $o" aio);g2 $C1 $M;ok l-merge-bypass-refused '[ $? != 0 ]'
C2=$(mkx "$M" legacy $RG:$D/ring2);g2 $M $C2;ok m-bootstrap-stays-closed-through-a-merge '[ $? != 0 ]'
cp $D/ring2 $D/ring3;printf 'owner@agi namespaces="git" ssh-ed25519 %s\n' "$(pkb aio)">>$D/ring3;C3=$(mkx "$C1" aio $RG:$D/ring3);g2 $C1 $C3;ok n-ring-line-off-shape-refused '[ $? != 0 ]'
git show $o:$PM>$D/posts2;printf '  - {"name": "x\\nowner", "parent": "all-is-one"}\n'>>$D/posts2;C4=$(mkx "$C1" aio $PM:$D/posts2);g2 $C1 $C4;ok o-posts-name-injection-refused '[ $? != 0 ]'
C5=$(mkx "$o" - $RG:$D/ring2);g2 $o $C5;ok p-first-ring-unsigned-refused '[ $? != 0 ]'
C6=$(mkx "$o" legacy $RG/x:$D/ring2);g2 $o $C6;ok q-ring-directory-refused '[ $? != 0 ]'
echo "grow-gate-bootstrap: $f FAIL";exit $f
