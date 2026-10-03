#!/bin/sh
# grow-gate-ring4b.t.sh [TRUNK] [GITDIR]: RING.4b (DG1 06:40Z order, SM 06:34Z return on RING.4 0d58fa0ae, mur sm18 accept_with_residue): falsifiers, TEST ONLY, in the harness of grow-gate-ring3.t.sh (GROW_GATE=<candidate piece>), each lane RED on the 0d58fa0ae piece (named where it is not), GREEN on the candidate, beside an ADMIT control:
#   L1 an EVIL MERGE: a merge whose combined diff status is AM (the node is ABSENT in parent 1, a valid add in parent 2) landing an INVALID node (key none); the plain non-merge add of the same invalid node is refused (control); a merge adding a VALID node is admitted
#   L2 a PATH shim that makes `git show <c>^:<node>` fail on a ratchet edit of an existing node: refused; the same edit with no shim, valid, is admitted; and a CORRUPTING edit with the shim is refused
#   L3 a .gitattributes (root AND .agi/nodes/.geometry/) with export-ignore on the schemas / growth.tsv by a ring signer that is not the owner: refused; owner-signed: admitted; a BRICK lane (a valid added node on a tip that carries those attributes is admitted: git archive would drop the schemas and refuse it); and the safety property when the attributes are already at the tip
#   L4 a shim failing `git ls-tree` and `git show` on the ring path while the tip HOLDS a ring and the commit is signed by an UNLISTED key: refused; control: a tip with no ring at all stays the bootstrap
#   L5 (R1 of the mur) a shim failing ONLY the read of the just-landed first ring: refused
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
# --- L1: the EVIL MERGE (combined status AM)
P1=$(mkc $R1 dg1 $AFB:$D/af);P2=$(mkc $R1 owner1 $NN:$D/nv)
mgt(){ x=$D/i;GIT_INDEX_FILE=$x git read-tree $P1;GIT_INDEX_FILE=$x git update-index --add --cacheinfo 100644,$(git hash-object -w $1),$NN;t=$(GIT_INDEX_FILE=$x git write-tree);rm -f $x;sgn owner1 -p $P1 -p $P2 -m merge $t; }
gate $R1 $P2;ok "l1a-control-valid-add-admitted a plain add of a VALID keyed node by its ring (a moral node: the owner) is admitted" '[ $r = 0 ]'
gate $R1 $(mkc $R1 owner1 $NN:$D/ni);ok "l1b-control-invalid-add-refused the plain (non-merge) add of the same node with its key removed is refused" 'refused'
gateN $R1 $(mgt $D/ni) "$R1 $P2";ok "l1c-evil-merge-refused P2 (the valid node) is ALREADY LANDED (AGI_NOT = the tip + P2, not in the push); the push [P1, M]: M merges P1 (no node) and P2 and lands the INVALID version (key none), combined status AM: refused" 'refused'
gateN $R1 $(mgt $D/nv) "$R1 $P2";ok "l1d-control-valid-merge-admitted the same push landing the VALID node is admitted" '[ $r = 0 ]'
# --- L2: a shim fails `git show <c>^:<node>` on a ratchet edit (a VALID edit never reads its parent: only the corrupting one does, so only that one is pinned)
E=$(mkc $R1 dg1 $AFB:$D/af);CC=$(mkc $R1 dg1 $AFB:$D/af-bad)
gate $R1 $E;ok "l2a-control-valid-ratchet-edit-admitted dg1's valid edit of an existing node (no shim) is admitted" '[ $r = 0 ]'
gateS $R1 $CC "$CC^:$AFB" 1 show;ok "l2b-baseline-unreadable-at-the-parent-refused a CORRUPTING edit when \`git show <c>^:<node>\` (the ratchet's baseline when it is read from the commit's first parent) fails (a shim): refused. The file carries BOTH shim forms (this one and l2c/l2d on <tip>:<node>) so it does not depend on which shape of the piece wins" 'refused'
gateS $R1 $CC "$R1:$AFB" 2 show;ok "l2c-baseline-unreadable-at-the-tip-refused a CORRUPTING edit when \`git show <receiving tip>:<node>\` (the ratchet's baseline, read from the LANDED tip h) fails (a shim): refused (an unreadable baseline is never read as an invalid one)" 'refused'
E1=$(mkc $R1 dg1 $AFB:$D/af);echo more>>$D/af-bad;CC2=$(mkc $E1 dg1 $AFB:$D/af-bad)
gateS $R1 $CC2 "$E1:$AFB" 3 show;ok "l2d-baseline-unreadable-at-an-inpush-h-refused the push [E1 (a valid edit), CC2 (a corrupting edit on top)]: E1 is h for CC2, and the read \`git show <E1>:<node>\` for the baseline fails (a shim): refused" 'refused'
# --- L3: .gitattributes with export-ignore on the schemas and growth.tsv
printf '.agi/context/schemas export-ignore\n.agi/nodes/.geometry/growth.tsv export-ignore\n'>$D/ga2;GAG=.agi/nodes/.geometry/.gitattributes
gate $R1 $(mkc $R1 dg1 .gitattributes:$D/ga2);ok "l3a-root-attributes-by-non-owner-refused a ring signer that is not the owner lands a ROOT .gitattributes with export-ignore on the schemas / growth.tsv: refused" 'refused'
gate $R1 $(mkc $R1 dg1 $GAG:$D/ga2);ok "l3b-geometry-attributes-by-non-owner-refused the same in .agi/nodes/.geometry/.gitattributes: refused" 'refused'
gate $R1 $(mkc $R1 owner1 .gitattributes:$D/ga2);ok "l3c-root-attributes-by-owner-admitted the OWNER lands the root .gitattributes: admitted" '[ $r = 0 ]'
gate $R1 $(mkc $R1 owner1 $GAG:$D/ga2);ok "l3d-geometry-attributes-by-owner-admitted the OWNER lands the geometry .gitattributes: admitted" '[ $r = 0 ]'
# l3e / l3f DROPPED (DG1 06:47Z): once only the owner may land the attribute, an owner-landed export-ignore is the owner's act; a blob-read scratch copy (+266 B) is a NAMED LIMIT of the piece, not a lane. (Measured earlier: a valid add on a tip carrying the attributes is refused by a git-archive scratch copy and admitted by a blob-read one.)
# --- L4: a shim fails git ls-tree AND git show on the ring path while the tip HOLDS a ring; the commit is signed by an UNLISTED key
gateS $R1 $(mkc $R1 atk $AFB:$D/af) .geometry/ring "" "show ls-tree";ok "l4a-ring-reads-fail-unlisted-signer-refused the tip holds a ring, every ring read fails (a shim), the commit is signed by atk (in AGI_ALLOWED, NOT in the ring): refused" 'refused'
gateS $o $(mkc $o atk $AFB:$D/af) .geometry/ring "" "show";ok "l4b-control-no-ring-tip-stays-bootstrap a tip with NO ring in any history, the shim failing \`git show\` of the ring only (a missing ring is a natural show failure; a failing ls-tree refuses, fail closed): the unlisted-key commit is admitted (the bootstrap, as before)" '[ $r = 0 ]'
# --- L5: a shim fails ONLY the read of the just-landed FIRST ring (mur R1)
x=$D/i;GIT_INDEX_FILE=$x git read-tree $P0;GIT_INDEX_FILE=$x git update-index --add --cacheinfo 100644,$(git hash-object -w $D/n-sm),$NS;B0=$(GIT_AUTHOR_NAME=g GIT_AUTHOR_EMAIL=g@g GIT_COMMITTER_NAME=g GIT_COMMITTER_EMAIL=g@g git commit-tree -m r4b-b0 -p $P0 $(GIT_INDEX_FILE=$x git write-tree));rm -f $x
C1=$(mkc $B0 dg1 $RG:$D/ring);sh_ $B0 $NS|sed '$a\
dg1-edit'>$D/e;C2=$(mkc $C1 dg1 $NS:$D/e)
gate $B0 $C1;ok "l5a-control-first-ring-lands dg1 lands the FIRST ring on a trunk that never had one: admitted" '[ $r = 0 ]'
gate $B0 $C2;ok "l5b-control-ruling-after-first-ring the push plus dg1's edit of a node ringed [sm]: refused by the ring just landed" 'refused'
gateS $B0 $C2 "$C1:$RG" 2 show;ok "l5c-first-ring-read-error-is-not-absence the same push when ONLY the SECOND \`git show <first-ring commit>:ring\` (the read of the landed ring for the next commit) fails: refused" 'refused'
echo "grow-gate-ring4b: $f FAIL"
exit $f
