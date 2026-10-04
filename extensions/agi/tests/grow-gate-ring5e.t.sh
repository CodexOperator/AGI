#!/bin/sh
# grow-gate-ring5e.t.sh [TRUNK] [GITDIR]: RING.5e (DG1 09:05Z order, SM 09:05Z return DEMOTE, mur sm19 dg3-ring-5d D1 R2-R4), TEST ONLY, in the harness of grow-gate-ring5d.t.sh (GROW_GATE=<candidate piece>), each lane RED on RING.5d d1832b29f where named, GREEN on a piece that anchors `lg` to the RECEIVING TIP's tree, beside a control:
#   r1h the ONE-PUSH LAUNDER: X outside the push holds an agi-fill-valid owner-ringed N; push [M1 = merge(R, X) with R's own tree (an ours-merge: changes no path), C1 = merge(M1, X) with X's tree], both signed dg1: C1 refused, M1 itself admitted (r1h0)
#   r1i the TWO-PUSH shape: push 1 = [M1] lands (tip = M1), push 2 = [C1]: refused; the same C1 signed by the owner admitted (r1i0)
#   r1j a SPACED node path (.agi/nodes/moral/zz r5e.md): a symlink with valid node text over it refused; a valid plain edit admitted (r1j0)
#   r1k `git ls-tree` shimmed to fail on a symlink node with valid text: refused (the unchecked ls-tree); no shim: refused (r1k0)
#   r1l agi-fill missing from PATH: an edit is refused; with it, admitted (r1l0)
#   r1m a posts.md ruler jq failure (jq shimmed on its --slurpfile call): refused; no shim: a ring signer's own row admitted (r1m0)
#   r1n an OCTOPUS [P1, P2, X] merge: refused while X is unlanded; admitted when the parents hold only what the tip holds (r1n0)
#   r1o-control the standard merge-up: M = merge(R2 holding an owner node, D1) signed sm: admitted
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
# mkl BASE KEY path:target ... = SYMLINK entries (mode 120000, the blob = the target text); mklt BASE KEY path:file ... = the same with the blob = the FILE's content (a symlink whose text is a valid node); trw BASE path:file ... = a tree; mko KEY TREE P1 P2 P3... = a signed octopus
mkl(){ b=$1;k=$2;shift 2;x=$D/i;GIT_INDEX_FILE=$x git read-tree $b;for a in "$@";do GIT_INDEX_FILE=$x git update-index --add --cacheinfo 120000,$(printf %s "${a#*:}"|git hash-object -w --stdin),"${a%%:*}";done;tr=$(GIT_INDEX_FILE=$x git write-tree);rm -f $x;sgn $k -p $b -m r5e $tr;}
mklt(){ b=$1;k=$2;shift 2;x=$D/i;GIT_INDEX_FILE=$x git read-tree $b;for a in "$@";do GIT_INDEX_FILE=$x git update-index --add --cacheinfo 120000,$(git hash-object -w "${a#*:}"),"${a%%:*}";done;tr=$(GIT_INDEX_FILE=$x git write-tree);rm -f $x;sgn $k -p $b -m r5e $tr;}
trw(){ b=$1;shift;x=$D/i;GIT_INDEX_FILE=$x git read-tree $b;for a in "$@";do GIT_INDEX_FILE=$x git update-index --add --cacheinfo 100644,$(git hash-object -w "${a#*:}"),"${a%%:*}";done;GIT_INDEX_FILE=$x git write-tree;rm -f $x;}
mko(){ k=$1;tr=$2;shift 2;ps=;for p in "$@";do ps="$ps -p $p";done;sgn $k $ps -m r5e $tr;}
# gateE TIP COMMIT PATHPREFIX: gate with PATHPREFIX put in front of PATH (the push is [COMMIT], AGI_NOT = TIP)
gateE(){ git update-ref refs/heads/trunk $1;echo "$1 $2 refs/heads/x"|PATH=$3:$PATH AGI_ALLOWED=$D/over AGI_TRUNK=refs/heads/trunk AGI_NOT=$1 timeout 60 grow-gate>$D/out 2>&1;r=$?;}
# X = R1 + the valid owner-ringed N, built by BELAM (a ring signer above all: only so that X != R2 when both are the same bytes); R2 = the trunk after the fork holding N
R2=$(mkc $R1 owner1 $NN:$D/nv);X=$(mkc $R1 belam1 $NN:$D/nv);D1=$(mkc $R1 dg1 $AFB:$D/af);D1e=$(mkc $R1 dg1)
# --- r1h / r1i: the OURS-merge launder of `lg` (mur sm19 D1): ancestry of X must not make X's node the trunk's
M1=$(mkr $R1 $X $R1 dg1)
gateN $R1 $M1 "$R1 $X";ok "r1h0-control-ours-merge-alone-admitted M1 = merge(R1, X) with R1's own tree signed by dg1 (it changes no path): admitted" '[ $r = 0 ]'
gateN $R1 $(mkr $M1 $X $X dg1) "$R1 $X";ok "r1h-ours-merge-launder-one-push-refused ONE push [M1, C1]: M1 = the ours-merge (X outside the push, now an ancestor of h), C1 = merge(M1, X) with X's tree signed by dg1: N is in no first-pass diff and X is an ancestor of h, but X is NOT landed (N is not in the receiving tip's tree): refused (a non-owner never lands an owner-ringed node)" 'refused'
gateN $M1 $(mkr $M1 $X $X dg1) "$M1";ok "r1i-ours-merge-launder-two-push-refused TWO pushes: M1 is LANDED (the tip is M1, X is an ancestor of the tip), the next push [C1] = merge(M1, X) with X's tree signed by dg1: refused (landed = the node is in the receiving tip's tree, not that a parent is an ancestor)" 'refused'
gateN $M1 $(mkr $M1 $X $X owner1) "$M1";ok "r1i0-control-owner-lands-it-admitted the same C1 signed by the OWNER (the node's own ring) is admitted: the lane refuses the signer, not the shape" '[ $r = 0 ]'
gateN $R2 $(mkr $R2 $D1 $R2 sm1 $AFB:$D/af) "$R2";ok "r1o-control-standard-merge-up-admitted the standard merge-up M = merge(R2 holding the owner node, D1) signed by sm: admitted" '[ $r = 0 ]'
# --- r1j: a SPACED node path (mur R4: \$f unquoted in phase 3 word-splits and blinds the symlink guard)
SP=".agi/nodes/moral/zz r5e.md";sed 's/^id: moral:zz-r4b/id: moral:zz-r5e/;s/^mint_id: .*/mint_id: 5123456789abcdef0123456789abcdef/' $D/nv>$D/nsp;cp $D/nsp $D/nsp2;echo edit>>$D/nsp2
R5=$(mkc $R1 owner1 "$SP:$D/nsp")
gate $R5 $(mkc $R5 dg1 "$SP:$D/nsp2");ok "r1j0-control-spaced-path-valid-edit-admitted a valid plain edit of the node at the spaced path is admitted" '[ $r = 0 ]'
gate $R5 $(mklt $R5 dg1 "$SP:$D/nsp2");ok "r1j-spaced-path-symlink-refused a SYMLINK entry whose text is a valid node, over the spaced path: refused (a word-split path must not blind the symlink guard)" 'refused'
# --- r1k: git ls-tree fails on a symlink node with valid text
SL=$(mklt $R1 dg1 $AFB:$D/af)
gate $R1 $SL;ok "r1k0-control-symlink-with-valid-text-refused no shim: a symlink over a valid node, its text a valid node: refused" 'refused'
gateS $R1 $SL "$AFB" "" ls-tree;ok "r1k-ls-tree-failure-refused \`git ls-tree\` of that path fails (a shim): refused (an unreadable type is never read as a regular file)" 'refused'
# --- r1l: agi-fill missing from PATH
mkdir $D/nf;for x in $D/b/*;do [ ${x##*/} = agi-fill ]||ln -s $x $D/nf/${x##*/};done;NP=$D/nf;PATH=${PATH#$D/b:}
E0=$(mkc $R1 dg1 $AFB:$D/af);PATH=$D/b:$PATH
gateE $R1 $E0 $D/b;ok "r1l0-control-agi-fill-present-edit-admitted dg1's valid edit with agi-fill on PATH: admitted" '[ $r = 0 ]'
PATH=${PATH#$D/b:};gateE $R1 $E0 $NP;PATH=$D/b:$PATH;ok "r1l-agi-fill-missing-refused the same edit with agi-fill MISSING from PATH: refused (a missing checker never reads as a valid or an invalid node)" 'refused'
# --- r1m: the posts.md ruler jq fails (only its --slurpfile call)
{ cat $D/posts.md;printf '  - {"name": "dg8", "parent": "dg1"}\n';}>$D/posts2;PM=$(mkc $R1 dg1 $GEO/posts.md:$D/posts2)
mkdir $D/jq;J=$(command -v jq);printf '#!/bin/sh\ncase "$*" in *slurpfile*)echo "shim: jq failed" >&2;exit 2;;esac\nexec %s "$@"\n' $J>$D/jq/jq;chmod +x $D/jq/jq
gate $R1 $PM;ok "r1m0-control-own-row-admitted dg1 adds a posts.md row UNDER ITSELF (the ruler is dg1): admitted" '[ $r = 0 ]'
gateE $R1 $PM $D/jq;ok "r1m-ruler-jq-failure-refused the same commit when the ruler jq (the --slurpfile call) fails (a shim): refused (no ruler is never read as an open path)" 'refused'
# --- r1n: an OCTOPUS through the excuse
O1=$(mko dg1 $(git rev-parse $X^{tree}) $D1 $D1e $X)
gateN $R1 $O1 "$R1 $X";ok "r1n-octopus-unlanded-parent-refused the octopus [D1, D1e, X] with X's tree signed by dg1, X outside the push and unlanded: refused" 'refused'
O2=$(mko dg1 $(trw $R2 $AFB:$D/af) $D1 $D1e $R2)
gateN $R2 $O2 "$R2";ok "r1n0-octopus-landed-parents-admitted the octopus [D1, D1e, R2] (R2 = the tip, holding N; the tree carries D1's edit) signed by dg1: admitted" '[ $r = 0 ]'
echo "grow-gate-ring5e: $f FAIL"
exit $f
