#!/bin/sh
# grow-gate-ring5e-dg3.t.sh [TRUNK] [GITDIR]: RING.5e (DG1 09:05Z order, mur sm19 dg3-ring-5d D1/R2/R4), TEST ONLY, in the harness of grow-gate-ring5d.t.sh (GROW_GATE=<candidate piece>):
#   r1h/r1i an OURS-merge M1 = merge(R1, X) with R1's own tree makes the outside, unlanded X an ancestor (same push: of h; next push: of R); C1 = merge(M1, X) with X's tree, signed by dg1 (a non-owner), carries X's OWNER-ringed node N: refused both ways (RED on d1832b29f: rc 0) · r1j-control M1 alone: admitted (an ours-merge changes no path)
#   r1k a node path with a SPACE that is a SYMLINK, signed by the owner: refused as a symlink node (the unquoted ls-tree pathspec went blind) · r1l-control the same spaced path as a regular valid node: admitted
#   r1m ls-tree failing on a node path refuses it ("ls-tree failed", RED on d1832b29f: admitted) · r1n git show of the node failing refuses it ("unreadable")
# Scratch repo borrowing GITDIR's objects (0 shared refs written), scratch keys at run time (no armoured block in this file), no network, nothing pushed. One ok/FAIL line per case; exit = FAIL count.
T=${1:-local-maxxing/season2/main};G=${2:-$(git rev-parse --path-format=absolute --git-common-dir)};D=$(mktemp -d);trap 'rm -rf $D' EXIT;mkdir $D/b $D/k;f=0
ok(){ if eval "$2";then echo "ok $1";else echo "FAIL $1 [rc=$r $(tail -1 $D/out 2>/dev/null|cut -c1-90)]";f=$((f+1));fi;}
r=0
o=$(git rev-parse $T)||exit 1;for x in sect grow-check grow-gate agi-fill;do git ls-tree --full-tree --name-only $o .agi/nodes/.geometry/|grep '/engine[^/]*\.md$'|sed "s|^|$o:|"|git cat-file --batch --follow-symlinks|sed -n "/^###* $x /,/^###* /{/^~~~/,/^~~~/{//!p}}">$D/b/$x;done
[ "$GROW_GATE" ]&&cp $GROW_GATE $D/b/grow-gate;chmod +x $D/b/*;[ -s $D/b/grow-gate ]||{ echo "FAIL no grow-gate at $T";exit 99;}
unset GIT_AUTHOR_NAME GIT_AUTHOR_EMAIL GIT_COMMITTER_NAME GIT_COMMITTER_EMAIL GIT_DIR GIT_WORK_TREE AGI_RULES AGI_TRUNK;export GIT_CONFIG_GLOBAL=/dev/null GIT_CONFIG_SYSTEM=/dev/null
for n in owner1 belam1 alive1 sm1 dg1 dg1b dg2 atk;do ssh-keygen -qN "" -ted25519 -f$D/k/$n -C $n>/dev/null;done
pk(){ cut -d' ' -f1,2 $D/k/$1.pub;}
: >$D/over;for n in owner1 belam1 alive1 sm1 dg1 dg2 atk;do p=${n%[0-9]};echo "$p@agi namespaces=\"git\" $(pk $n)">>$D/over;done   # OVER-PERMISSIVE: every key made
git init -q $D/r;echo $G/objects>$D/r/.git/objects/info/alternates;cd $D/r;export PATH=$D/b:$PATH
GEO=.agi/nodes/.geometry;RG=$GEO/ring
printf -- '---\n---\n  - {"name": "belam", "parent": "owner"}\n  - {"name": "council", "parent": "belam"}\n  - {"name": "keep", "parent": "belam"}\n  - {"name": "alive", "parent": "council"}\n  - {"name": "sm", "parent": "keep"}\n  - {"name": "dg1", "parent": "sm"}\n  - {"name": "dg2", "parent": "sm"}\n  - {"name": "dg9", "parent": "sm"}\n'>$D/posts.md
printf 'owner %s\nbelam %s\nalive %s\nsm %s\ndg1 %s\ndg2 %s\n' "$(pk owner1)" "$(pk belam1)" "$(pk alive1)" "$(pk sm1)" "$(pk dg1)" "$(pk dg2)">$D/ring
git show $o:.agi/nodes/moral/antifragility.md|sed 's/^id: moral:antifragility/id: moral:zz-r3-sm/;s/^mint_id: .*/mint_id: 3123456789abcdef0123456789abcdef/;s/^type: moral/type: moral\nring: [sm]/'>$D/n-sm
NS=.agi/nodes/moral/zz-r3-sm.md
# mkc BASE KEYNAME [path:file ...]: a signed commit on BASE; mku = the same UNSIGNED; mkm P1 P2 TREEFROM KEYNAME = a signed MERGE of P1 and P2 whose tree is TREEFROM's
mkc(){ b=$1;k=$2;shift 2;x=$D/i;GIT_INDEX_FILE=$x git read-tree $b;for a in "$@";do GIT_INDEX_FILE=$x git update-index --add --cacheinfo 100644,$(git hash-object -w "${a#*:}"),"${a%%:*}";done;tr=$(GIT_INDEX_FILE=$x git write-tree);rm -f $x
 pn=${k%[0-9]};env GIT_COMMITTER_NAME=$pn GIT_COMMITTER_EMAIL=$pn@agi GIT_AUTHOR_NAME=$pn GIT_AUTHOR_EMAIL=$pn@agi git -c gpg.format=ssh -c user.signingkey=$D/k/$k commit-tree -S -p $b -m r3 $tr;}
mku(){ b=$1;shift;x=$D/i;GIT_INDEX_FILE=$x git read-tree $b;for a in "$@";do GIT_INDEX_FILE=$x git update-index --add --cacheinfo 100644,$(git hash-object -w "${a#*:}"),"${a%%:*}";done;tr=$(GIT_INDEX_FILE=$x git write-tree);rm -f $x
 env GIT_COMMITTER_NAME=u GIT_COMMITTER_EMAIL=u@agi GIT_AUTHOR_NAME=u GIT_AUTHOR_EMAIL=u@agi git commit-tree -m r3 -p $b $tr;}
mkm(){ pn=${4%[0-9]};env GIT_COMMITTER_NAME=$pn GIT_COMMITTER_EMAIL=$pn@agi GIT_AUTHOR_NAME=$pn GIT_AUTHOR_EMAIL=$pn@agi git -c gpg.format=ssh -c user.signingkey=$D/k/$4 commit-tree -S -p $1 -p $2 -m merge $(git rev-parse $3^{tree});}
# base R: the real trunk tree + the fixture ring, posts tree and one ringed node (R's parent is $o, the tree WITHOUT a ring)
x=$D/i;GIT_INDEX_FILE=$x git read-tree $o;for a in $RG:$D/ring $GEO/posts.md:$D/posts.md $NS:$D/n-sm;do GIT_INDEX_FILE=$x git update-index --add --cacheinfo 100644,$(git hash-object -w "${a#*:}"),"${a%%:*}";done
R=$(GIT_AUTHOR_NAME=g GIT_AUTHOR_EMAIL=g@g GIT_COMMITTER_NAME=g GIT_COMMITTER_EMAIL=g@g git commit-tree -m r3-base -p $o $(GIT_INDEX_FILE=$x git write-tree));rm -f $x
# P0 = the trunk + the fixture posts tree (NO ring); R1 = P0 + the ring and NOTHING else: a merge of R1 and P0 whose tree is P0's deletes ONLY the ring and is TREESAME to P0 (so the ruler walk reads the fixture tree)
x=$D/i;GIT_INDEX_FILE=$x git read-tree $o;GIT_INDEX_FILE=$x git update-index --add --cacheinfo 100644,$(git hash-object -w $D/posts.md),$GEO/posts.md;P0=$(GIT_AUTHOR_NAME=g GIT_AUTHOR_EMAIL=g@g GIT_COMMITTER_NAME=g GIT_COMMITTER_EMAIL=g@g git commit-tree -m r3-posts -p $o $(GIT_INDEX_FILE=$x git write-tree));GIT_INDEX_FILE=$x git update-index --add --cacheinfo 100644,$(git hash-object -w $D/ring),$RG;R1=$(GIT_AUTHOR_NAME=g GIT_AUTHOR_EMAIL=g@g GIT_COMMITTER_NAME=g GIT_COMMITTER_EMAIL=g@g git commit-tree -m r3-ring-only -p $P0 $(GIT_INDEX_FILE=$x git write-tree));rm -f $x
sh_(){ git show $1:$2; }
gate(){ git update-ref refs/heads/trunk $1;echo "$1 $2 refs/heads/x"|AGI_ALLOWED=$D/over AGI_TRUNK=refs/heads/trunk AGI_NOT=$1 timeout 60 grow-gate>$D/out 2>&1;r=$?;}
refused(){ [ $r != 0 ]&&[ $r != 124 ];}
edit(){ sh_ $1 $2|sed "$3">$D/e;}
# ringadd BASE LINE: the ring at BASE + LINE (printf format, one argument) written to $D/e
ringadd(){ { sh_ $1 $RG;printf "$2";}>$D/e;}
ATK=$(pk atk)
# --- the shim: a `git` that fails the subcommands in FAILCMD (default show) whose arguments contain FAILPAT, only the FAILNTH-th such call (every one when FAILNTH is empty)
printf '#!/bin/sh\ncase " ${FAILCMD:-show} " in *" $1 "*)case "$*" in *"$FAILPAT"*)n=$(cat $FAILCNT 2>/dev/null||echo 0);n=$((n+1));echo $n>$FAILCNT;{ [ -z "$FAILNTH" ]||[ $n = "$FAILNTH" ]; }&&{ echo "shim: failed" >&2;exit 128;};;esac;;esac\nexec /usr/bin/git "$@"\n'>$D/sh_git;mkdir -p $D/sh;mv $D/sh_git $D/sh/git;chmod +x $D/sh/git
gateS(){ rm -f $D/cnt;git update-ref refs/heads/trunk $1;echo "$1 $2 refs/heads/x"|PATH=$D/sh:$PATH FAILPAT="$3" FAILNTH="$4" FAILCMD="$5" FAILCNT=$D/cnt AGI_ALLOWED=$D/over AGI_TRUNK=refs/heads/trunk AGI_NOT=$1 timeout 60 grow-gate>$D/out 2>&1;r=$?;}
gateN(){ git update-ref refs/heads/trunk $1;echo "$1 $2 refs/heads/x"|AGI_ALLOWED=$D/over AGI_TRUNK=refs/heads/trunk AGI_NOT="$3" timeout 60 grow-gate>$D/out 2>&1;r=$?;}
AFB=.agi/nodes/moral/antifragility.md;NN=.agi/nodes/moral/zz-r4b.md
git show $o:$AFB>$D/af;echo 'plain-edit'>>$D/af;sed '/^type:/d' $D/af>$D/af-bad
git show $o:$AFB|sed 's/^id: moral:antifragility/id: moral:zz-r4b/;s/^mint_id: .*/mint_id: 4123456789abcdef0123456789abcdef/;s/^type: moral/type: moral\nkey: 2fe50ba43c479d67/'>$D/nv;sed '/^key:/d' $D/nv>$D/ni
sgn(){ sk=$1;shift;env GIT_COMMITTER_NAME=${sk%[0-9]} GIT_COMMITTER_EMAIL=${sk%[0-9]}@agi GIT_AUTHOR_NAME=${sk%[0-9]} GIT_AUTHOR_EMAIL=${sk%[0-9]}@agi git -c gpg.format=ssh -c user.signingkey=$D/k/$sk commit-tree -S "$@"; }
# mkr PARENT1 PARENT2 TREEBASE KEY [path:file ...]: a signed MERGE of PARENT1 and PARENT2 whose tree is TREEBASE's with the paths set
mkr(){ p1=$1;p2=$2;b=$3;k=$4;shift 4;x=$D/i;GIT_INDEX_FILE=$x git read-tree $b;for a in "$@";do GIT_INDEX_FILE=$x git update-index --add --cacheinfo 100644,$(git hash-object -w "${a#*:}"),"${a%%:*}";done;tr=$(GIT_INDEX_FILE=$x git write-tree);rm -f $x;sgn $k -p $p1 -p $p2 -m r5d $tr;}
# R2 = the trunk after the fork: R1 + the valid owner-ringed N (signed by the owner); D1 = a plain valid edit of AFB on F = R1
R2=$(mkc $R1 owner1 $NN:$D/nv);D1=$(mkc $R1 dg1 $AFB:$D/af)
# X = R1 + the VALID owner-ringed N, signed by the owner (outside the push, never landed)
X=$(mkc $R1 owner1 $NN:$D/nv)
M1=$(mkr $R1 $X $R1 dg1);C1=$(mkr $M1 $X $X dg1)
gateN $R1 $C1 "$R1 $X";ok "r1h-ours-merge-launder-one-push-refused push [M1, C1] on tip R1 (X outside, unlanded): M1 = merge(R1, X) with R1's tree, C1 = merge(M1, X) with X's tree lands the owner-ringed N signed by dg1: refused" 'refused'
gateN $R1 $M1 "$R1 $X";ok "r1j-control-ours-merge-alone-admitted M1 alone (the tip R1, X outside): changes no path: admitted" '[ $r = 0 ]'
gateN $M1 $C1 "$M1";ok "r1i-ours-merge-launder-two-push-refused the next push [C1] on tip M1 (X now an ancestor of the tip, not landed by tree): refused" 'refused'
SP=".agi/nodes/moral/zz spaced.md"
mkl(){ x=$D/i;GIT_INDEX_FILE=$x git read-tree $1;GIT_INDEX_FILE=$x git update-index --add --cacheinfo $4,$(git hash-object -w $3),"$2";tr=$(GIT_INDEX_FILE=$x git write-tree);rm -f $x;sgn $5 -p $1 -m r5e $tr;}
gate $R1 $(mkl $R1 "$SP" $D/nv 120000 owner1);ok "r1k-spaced-symlink-node-refused a SYMLINK node at a path with a space, signed by the owner: refused as a symlink node" 'refused&&grep -q symlink $D/out'
gate $R1 $(mkl $R1 "$SP" $D/nv 100644 owner1);ok "r1l-control-spaced-regular-node-admitted the same spaced path as a regular valid node (owner, key right): admitted" '[ $r = 0 ]'
gateS $R1 $(mkc $R1 owner1 $NN:$D/nv) "$NN" "" ls-tree;ok "r1m-ls-tree-failure-refuses git ls-tree failing on the added node path: refused (ls-tree failed)" 'refused&&grep -q "ls-tree failed" $D/out'
gateS $R1 $(mkc $R1 owner1 $NN:$D/nv) ":$NN" "" show;ok "r1n-show-failure-refuses git show of the added node failing: refused (unreadable)" 'refused&&grep -q unreadable $D/out'
# --- RING.5f (SM mur sm19 on RING.5e, R1/R2): r1o lg compares two reads: BOTH failing (rev-parse shimmed on the node path) must refuse the launder [M1, C1], not read "" = "" as landed · r1p/r1q an agi-fill that EXISTS but crashes (rc 1) makes k n and k p both fail: a corrupting edit (r1p) and a valid one (r1q) are refused with `agi-fill rc 1`
gateR(){ git update-ref refs/heads/trunk $1;echo "$1 $2 refs/heads/x"|PATH=$D/sh:$PATH FAILPAT="$4" FAILNTH= FAILCMD=rev-parse FAILCNT=$D/cnt AGI_ALLOWED=$D/over AGI_TRUNK=refs/heads/trunk AGI_NOT="$3" timeout 60 grow-gate>$D/out 2>&1;r=$?;}
gateR $R1 $C1 "$R1 $X" ":$NN";ok "r1o-lg-both-reads-fail-refused the launder [M1, C1] (r1h) with git rev-parse failing on the node path (both reads of lg fail): refused, never admitted as landed" 'refused'
mkdir -p $D/crash;printf '#!/bin/sh\nexit 1\n'>$D/crash/agi-fill;chmod +x $D/crash/agi-fill
gateC(){ git update-ref refs/heads/trunk $1;echo "$1 $2 refs/heads/x"|PATH=$D/crash:$PATH AGI_ALLOWED=$D/over AGI_TRUNK=refs/heads/trunk AGI_NOT=$1 timeout 60 grow-gate>$D/out 2>&1;r=$?;}
gateC $R1 $(mkc $R1 dg1 $AFB:$D/af-bad);ok "r1p-agi-fill-crash-corrupting-edit-refused agi-fill exits 1 (a crash, not invalid = 3) and dg1 deletes a node's type: line: refused (agi-fill rc 1), not admitted because both checks failed" 'refused&&grep -q "agi-fill rc 1" $D/out'
gateC $R1 $(mkc $R1 dg1 $AFB:$D/af);ok "r1q-agi-fill-crash-valid-edit-refused the same crash on a VALID edit: refused too (the gate cannot judge it)" 'refused&&grep -q "agi-fill rc 1" $D/out'
gate $R1 $(mkc $R1 dg1 $AFB:$D/af);ok "r1q0-control-valid-edit-admitted the same valid edit with the real agi-fill: admitted" '[ $r = 0 ]'
echo "grow-gate-ring5e-dg3: $f FAIL"
exit $f
