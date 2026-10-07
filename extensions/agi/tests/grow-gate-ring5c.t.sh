#!/bin/sh
# grow-gate-ring5c.t.sh [TRUNK] [GITDIR]: RING.5c (SM 07:27Z return, mur sm18 accept_with_residue on RING.5b 083720981): falsifiers, TEST ONLY, in the harness of grow-gate-ring4b.t.sh (GROW_GATE=<candidate piece>), each lane RED on the 083720981 piece, GREEN on a candidate that closes it, beside an ADMIT control:
#   D1 a ring member turns a valid [sm]-ringed node into a SYMLINK (mode 120000): the node check runs on A and M only, so a type change T is never read; must refuse (by sm, whom the ring rules, and by the owner above it); a symlink ADDED as a node path; control: a regular valid edit of the same node by sm is admitted
#   D2 dg1 signs merge(V, X) with X's tree, X OUTSIDE the push (in AGI_NOT) and holding an agi-fill-INVALID version of a valid node: the combined diff of the merge does not list the node (it equals X's), so it is never checked; must refuse, in BOTH parent orders; controls: the plain (non-merge) add of the invalid version is refused; the same merge with a VALID X is admitted
# Scratch repo borrowing GITDIR's objects (0 shared refs written), scratch keys at run time (no armoured block in this file), no network, nothing pushed. One ok/FAIL line per case; exit = FAIL count.
T=${1:-local-maxxing/season2/main};G=${2:-$(git rev-parse --path-format=absolute --git-common-dir)};D=$(mktemp -d);trap 'rm -rf $D' EXIT;mkdir $D/b $D/k;f=0
ok(){ if eval "$2";then echo "ok $1";else echo "FAIL $1 [rc=$r $(tail -1 $D/out 2>/dev/null|cut -c1-90)]";f=$((f+1));fi;}
r=0
o=$(git rev-parse $T)||exit 1;for x in sect grow-check grow-gate agi-fill;do git ls-tree --full-tree --name-only $o .agi/nodes/.geometry/|grep '/engine[^/]*\.md$'|sed "s|^|$o:|"|git cat-file --batch --follow-symlinks|sed -n "/^###* $x /,/^###* /{/^~~~/,/^~~~/{//!p}}">$D/b/$x;done
[ "$GROW_GATE" ]&&cp $GROW_GATE $D/b/grow-gate;[ -s $D/b/ckpt ]||printf "#!/bin/sh\nexit 0\n">$D/b/ckpt;chmod +x $D/b/*;[ -s $D/b/grow-gate ]||{ echo "FAIL no grow-gate at $T";exit 99;}
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
# mkl BASE KEYNAME path:target ...: a signed commit on BASE whose paths are SYMLINK entries (mode 120000, the blob is the target text)
mkl(){ b=$1;k=$2;shift 2;x=$D/i;GIT_INDEX_FILE=$x git read-tree $b;for a in "$@";do GIT_INDEX_FILE=$x git update-index --add --cacheinfo 120000,$(printf %s "${a#*:}"|git hash-object -w --stdin),"${a%%:*}";done;tr=$(GIT_INDEX_FILE=$x git write-tree);rm -f $x;sgn $k -p $b -m r5c $tr;}
# --- D1: a symlink entry in place of a node (the node check reads A and M only, a type change T is never read)
gate $R1 $(mkc $R1 dg1 $AFB:$D/af);ok "d1a-control-valid-edit-admitted dg1's plain valid edit of an existing node is admitted" '[ $r = 0 ]'
gate $R1 $(mkl $R1 dg1 $AFB:antifragility.md);ok "d1b-symlink-over-node-by-ring-member-refused dg1 (a ring member) replaces the valid node with a mode-120000 symlink entry (target: a sibling name): refused" 'refused'
gate $R1 $(mkl $R1 dg1 $AFB:../../../../../../../etc/passwd);ok "d1c-symlink-out-of-tree-refused the same with a target that leaves the tree: refused" 'refused'
sh_ $R $NS|sed '$a\
sm-edit'>$D/e;gate $R $(mkc $R sm1 $NS:$D/e);ok "d1g-control-valid-edit-of-ringed-node-admitted sm's plain valid edit of the [sm] node is admitted" '[ $r = 0 ]'
gate $R $(mkl $R sm1 $NS:antifragility.md);ok "d1d-symlink-over-ringed-node-by-its-ring-refused sm (the ring of [sm] node) replaces it with a symlink: refused" 'refused'
gate $R1 $(mkl $R1 owner1 $AFB:antifragility.md);ok "d1e-symlink-over-node-by-owner-refused the OWNER, above every ring, does the same: refused" 'refused'
gate $R1 $(mkl $R1 dg1 .agi/nodes/moral/zz-r5c-new.md:antifragility.md);ok "d1f-symlink-added-as-node-refused a symlink ADDED at a new node path: refused" 'refused'
# --- D2: merge(V, X) with X's tree, X OUTSIDE the push (AGI_NOT) and holding an INVALID version (type line deleted) of a valid node
X=$(mkc $R1 dg1 $AFB:$D/af-bad);XV=$(mkc $R1 dg1 $AFB:$D/af)
gate $R1 $X;ok "d2a-control-plain-invalid-edit-refused the plain (non-merge) landing of the invalid version of the valid node is refused" 'refused'
gateN $R1 $(mkm $R1 $X $X dg1) "$R1 $X";ok "d2b-merge-with-outside-invalid-refused M = merge(R1, X) with X's tree, signed by dg1: the node equals X's, so the combined diff does not list it; refused" 'refused'
gateN $R1 $(mkm $X $R1 $X dg1) "$R1 $X";ok "d2c-merge-swapped-order-refused M = merge(X, R1) with X's tree (X is the FIRST parent: a baseline read from c^ is X's invalid blob): refused" 'refused'
gateN $R1 $(mkm $R1 $XV $XV dg1) "$R1 $XV";ok "d2d-control-merge-with-valid-outside-admitted the same merge(R1, XV) with a VALID blob admitted" '[ $r = 0 ]'
gateN $R1 $(mkm $XV $R1 $XV dg1) "$R1 $XV";ok "d2e-control-merge-swapped-valid-admitted merge(XV, R1) with the valid blob admitted" '[ $r = 0 ]'
# --- l1c pinned (DG1 07:28Z): both parents IN the push: the evil merge of the key-lock (P1 no node, P2 the valid node) landing the INVALID version
P1=$(mkc $R1 dg1 $AFB:$D/af);P2=$(mkc $R1 owner1 $NN:$D/nv)
mgt(){ x=$D/i;GIT_INDEX_FILE=$x git read-tree $P1;GIT_INDEX_FILE=$x git update-index --add --cacheinfo 100644,$(git hash-object -w $1),$NN;t=$(GIT_INDEX_FILE=$x git write-tree);rm -f $x;sgn owner1 -p $P1 -p $P2 -m merge $t; }
gateN $R1 $(mgt $D/nv) "$R1";ok "l1c-pin-control-inpush-valid-merge-admitted P1, P2 and the merge M ALL in the push; M lands the VALID node: admitted" '[ $r = 0 ]'
gateN $R1 $(mgt $D/ni) "$R1";ok "l1c-pin-inpush-key-lock-refused P1, P2 and M all in the push; M lands the INVALID version (key none): refused (the in-push key lock, 5c cannot trade it away)" 'refused'
# --- B: the ratchet baseline read UNCHECKED (DG1 07:36Z; `git show $b:$f>$t/p&&! k p||` -> `;! k p||`). The piece reads the baseline TWICE (pass 1 <c>^:<node>, pass 2 <h>:<node>, one shared line): in a linear push both are the same blob, so a shim failing ONE form is covered by the other pass (ring4b l2b/l2c/l2d); only a shim failing BOTH forms at once is RED on the unchecked read.
# shim2: fails `git show` when the args contain FAILPAT (every time) or FAILPAT2 (every match after the first FAILSKIP of them: the ruling read of rn, and in a push the reads of an earlier commit, are not the baseline)
printf '#!/bin/sh\n[ "$1" = show ]&&case "$*" in *"$FAILPAT"*)echo "shim: failed" >&2;exit 128;;*"$FAILPAT2"*)n=$(cat $FAILCNT 2>/dev/null||echo 0);n=$((n+1));echo $n>$FAILCNT;[ $n -gt "$FAILSKIP" ]&&{ echo "shim: failed" >&2;exit 128;};;esac\nexec /usr/bin/git "$@"\n'>$D/s2_git;mkdir -p $D/sh2;mv $D/s2_git $D/sh2/git;chmod +x $D/sh2/git
gateS2(){ rm -f $D/cnt;git update-ref refs/heads/trunk $1;echo "$1 $2 refs/heads/x"|PATH=$D/sh2:$PATH FAILPAT="$3" FAILPAT2="$4" FAILSKIP="$5" FAILCNT=$D/cnt AGI_ALLOWED=$D/over AGI_TRUNK=refs/heads/trunk AGI_NOT=$1 timeout 60 grow-gate>$D/out 2>&1;r=$?;}
gate $R1 $X;ok "b1a-control-corrupting-edit-no-shim-refused the CORRUPTING edit (type line deleted) of a valid node, no shim: refused as 'was valid' (the lane's refusal below is not the plain one)" 'refused'
gateS2 $R1 $XV "$XV^:$AFB" "$R1:$AFB" 1;ok "b1b-control-valid-edit-both-shims-admitted dg1's VALID edit with BOTH baseline forms shimmed (<c>^:<node> and <tip>:<node>, the first <tip>:<node> read skipped = rn's ruling read): admitted (a valid edit never reads its baseline)" '[ $r = 0 ]'
gateS2 $R1 $X "$X^:$AFB" "$R1:$AFB" 1;ok "b1c-baseline-both-forms-unreadable-refused the CORRUPTING edit when BOTH reads of its baseline fail at once (<c>^:<node> and <tip>:<node>, the first <tip>:<node> match, rn's ruling read, skipped): refused (an unreadable baseline is never read as an invalid one; RED on the unchecked read, whose pass 1 admits)" 'refused'
E1=$XV;echo more>>$D/af-bad;CC2=$(mkc $E1 dg1 $AFB:$D/af-bad)
gateS2 $R1 $CC2 "$CC2^:$AFB" "$E1:$AFB" 3;ok "b1d-baseline-both-forms-unreadable-inpush-refused the push [E1 (a valid edit), CC2 (a corrupting edit on top)] with both forms shimmed (<CC2>^:<node> = <E1>:<node> as pass 1 and pass 2 spell it; the three earlier <E1>:<node> reads skipped: E1's own two and rn's): refused" 'refused'
echo "grow-gate-ring5c: $f FAIL"
exit $f
