#!/bin/sh
# grow-gate-ring5d.t.sh [TRUNK] [GITDIR]: RING.5d (DG1 08:11Z order, SM 08:10Z return, mur sm19 dg3-ring-5c R1 REGRESSION): the standard MERGE-UP shape, TEST ONLY, in the harness of grow-gate-ring5c.t.sh (GROW_GATE=<candidate piece>), each lane beside a control:
#   the trunk R1 forks F (= R1); the trunk adds an OWNER-ringed node N (a valid moral node, key right) at R2 after F, signed by the owner; the in-push DG commit D1 on F is a plain valid edit of ANOTHER node; M = merge(R2, D1) signed by SM (a non-owner ring signer), the tip being R2, so the push is [D1, M] and N reaches the second phase-3 pass (h = D1, not a parent of M) as an ADD in diff(D1, M)
#   r1a M admitted (RED on the 5c piece: refused `ring owner, signed by sm`) · r1b the same with the parents swapped, merge(D1, R2): admitted · r1c-control an in-push commit that ADDS the owner-ringed node, signed by sm: refused (unchanged) · r1d-control the same merge shape but N INVALID on the trunk (agi-fill-invalid, the owner's key and ring right) while D1 touches nothing: the combined pass lists nothing, pass 2 must still refuse an INVALID node: refused · r1e-control the same shape with a VALID N and D1 touching nothing, merge signed by sm: admitted
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
gateN $R2 $(mkr $R2 $D1 $R2 sm1 $AFB:$D/af) "$R2" ;ok "r1a-merge-up-admitted M = merge(R2, D1) SIGNED BY SM: R2 (trunk) added the owner-ringed N after the fork F, D1 (in the push) edits AFB; M carries both: admitted (the trunk's node is not the push's add)" '[ $r = 0 ]'
gateN $R2 $(mkr $D1 $R2 $R2 sm1 $AFB:$D/af) "$R2" ;ok "r1b-merge-up-swapped-admitted the same with the parents swapped, merge(D1, R2): admitted" '[ $r = 0 ]'
gate $R1 $(mkc $R1 sm1 $NN:$D/nv);ok "r1c-control-inpush-owner-add-by-sm-refused an in-push commit that ADDS the owner-ringed N, signed by sm: refused (ring owner, signed by sm; unchanged)" 'refused'
# N INVALID for agi-fill ONLY (the axis line deleted: grow-check reads the type and the key, which stay right), D1e = an EMPTY commit on F (touches nothing): the combined pass lists nothing, pass 2 reads N as an ADD in diff(D1e, M)
sed '/^axis:/d' $D/nv>$D/nbad;D1e=$(mkc $R1 dg1)
R2b=$(mkc $R1 owner1 $NN:$D/nbad)
gateN $R2b $(mkr $R2b $D1e $R2b sm1) "$R2b";ok "r1d-control-invalid-trunk-node-refused the trunk R2b holds an INVALID N (axis deleted; the owner's key and ring right), D1e touches nothing, M = merge(R2b, D1e) signed by sm: pass 2 must still refuse an INVALID node (agi-fill, not the ring): refused" 'refused'
gateN $R2 $(mkr $R2 $D1e $R2 sm1) "$R2";ok "r1e-control-valid-trunk-node-admitted the same shape with the VALID N (R2): admitted" '[ $r = 0 ]'
# --- r1f/r1g (DG1 08:21Z, a gap in the real piece: `lg` -> `true` was RED in no lane): a parent excuses a pass-2 add only if it is LANDED (an ancestor of the receiving tip or of h). X = R1 + the VALID owner-ringed N (agi-fill-valid, key right), signed by the owner
X=$(mkc $R1 owner1 $NN:$D/nv)
gateN $R1 $(mkr $R1 $X $X dg1) "$R1 $X";ok "r1f-outside-parent-never-excuses-refused X is OUTSIDE the push (in AGI_NOT) and NOT landed (the tip is R1) and holds the valid owner-ringed N; M = merge(R1, X) with X's tree signed by dg1 (a non-owner): N is in no first-pass diff (equal to X's blob), pass 2 reads it as an ADD, and X, not landed, must NOT excuse it: refused (a non-owner never lands an owner-ringed node)" 'refused'
gateN $X $(mkr $D1 $X $X sm1 $AFB:$D/af) "$X";ok "r1g-control-landed-parent-excuses-admitted the same node already LANDED (the tip is X): the push [D1, M], M = merge(D1, X) signed by sm (a non-owner) carrying D1's edit: X is landed and its blob equals M's, so the node is the trunk's, not the push's add: admitted" '[ $r = 0 ]'
# --- r1h/r1i (SM 09:05Z, mur sm19 D1: `lg` decided LANDED by ANCESTRY of R or h, which an OURS-merge launders): M1 = merge(R, X) with R's tree changes no path and passes every phase for any ring signer, but makes the OUTSIDE, unlanded X an ancestor; C1 = merge(M1, X) with X's tree then reads N as an add whose parent X is now an ancestor: a non-owner must still be refused
M1=$(mkr $R1 $X $R1 dg1)
gateN $R1 $M1 "$R1 $X";ok "r1h0-control-ours-merge-alone-admitted M1 = merge(R1, X) with R1's tree signed by dg1 (it changes no path): admitted" '[ $r = 0 ]'
gateN $R1 $(mkr $M1 $X $X dg1) "$R1 $X";ok "r1h-ours-merge-launder-one-push-refused ONE push [M1, C1]: M1 = the ours-merge above (X outside the push, now an ancestor of h), C1 = merge(M1, X) with X's tree signed by dg1: N is in no first-pass diff and X is an ancestor of h, but X is NOT landed (not in the receiving tip's tree): refused (a non-owner never lands an owner-ringed node)" 'refused'
gateN $M1 $(mkr $M1 $X $X dg1) "$M1";ok "r1i-ours-merge-launder-two-push-refused TWO pushes: M1 is LANDED (the tip is M1, X is now an ancestor of the tip), the next push [C1] = merge(M1, X) with X's tree signed by dg1: refused (landed means the node is in the receiving tip's tree, not that a parent is an ancestor)" 'refused'
gateN $M1 $(mkr $M1 $X $X owner1) "$M1";ok "r1i0-control-owner-lands-it-admitted the same C1 signed by the OWNER (the node's own ring) is admitted: the lane refuses the signer, not the shape" '[ $r = 0 ]'
echo "grow-gate-ring5d: $f FAIL"
exit $f
