#!/bin/sh
# grow-gate-ring5f.t.sh [TRUNK] [GITDIR]: RING.5f (SM 09:44Z return on RING.5e 68c170a81, mur sm19 dg3-ring-5e R1 R2), TEST ONLY, in the harness of grow-gate-ring5e.t.sh (GROW_GATE=<candidate piece>), each lane RED on the 5e piece, GREEN on a piece that closes it, beside a control:
#   f1 (DG1 09:46Z r1p) `lg` compares two UNCHECKED rev-parse outputs: when BOTH fail, "" = "" reads as LANDED: the r1h launder [M1, C1] signed dg1 with `git rev-parse` shimmed to fail on the node path must be REFUSED (f1a); one side failing (the reads of the receiving tip only, f1b) and no shim (f1c) stay refused
#   f2 (DG1 r2a-r2d) agi-fill EXISTS but FAULTS (rc 1, 2, 127; invalid is rc 3): a corrupting edit by dg1 (the type line deleted) must be REFUSED (the checker's crash is never read as an invalid version, so `! k p` must not excuse it); NAMED CONTROL f2n: agi-fill exiting 3 everywhere (invalid by its OWN contract) is a legacy-baseline ADMIT BY DESIGN (expected ADMIT, not a FAIL); f2d the real agi-fill refuses the corrupting edit, f2e admits a valid one; f2r an agi-fill exiting 3 ONLY on the new version (0 on the baseline): refused (the existing ratchet)
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
# gateX TIP COMMIT NOT FAILPAT FAILNTH FAILCMD: gate with the git shim ($D/sh) failing the FAILCMD subcommands whose args contain FAILPAT, and AGI_NOT = NOT (more than the tip: an outside parent)
gateX(){ rm -f $D/cnt;git update-ref refs/heads/trunk $1;echo "$1 $2 refs/heads/x"|PATH=$D/sh:$PATH FAILPAT="$4" FAILNTH="$5" FAILCMD="$6" FAILCNT=$D/cnt AGI_ALLOWED=$D/over AGI_TRUNK=refs/heads/trunk AGI_NOT="$3" timeout 60 grow-gate>$D/out 2>&1;r=$?;}
# --- f1: the launder shape [M1, C1] (X outside the push holds the valid owner-ringed N): the tip R1 lacks N, so the two reads of lg differ unless BOTH fail
M1=$(mkr $R1 $X $R1 dg1);C1=$(mkr $M1 $X $X dg1)
gateX $R1 $C1 "$R1 $X" "$NN" "" rev-parse;ok "f1a-lg-both-reads-fail-refused the one-push launder [M1, C1] signed by dg1 with \`git rev-parse\` failing on the node path (BOTH of lg's reads fail: the receiving tip's and the commit's): refused (two failed reads are never 'equal blobs', never 'landed')" 'refused'
gateX $R1 $C1 "$R1 $X" "$R1:$NN" "" rev-parse;ok "f1b-lg-tip-read-fails-refused only the receiving tip's read ($R1:path) fails: refused" 'refused'
gateX $R1 $C1 "$R1 $X" "$NN" "" show;ok "f1c-control-no-rev-parse-shim-refused the same shape with no rev-parse failing (a git show shim on the path that no lg read uses): refused" 'refused'
gateN $R1 $M1 "$R1 $X";ok "f1d-control-ours-merge-alone-admitted M1 alone (changes no path): admitted" '[ $r = 0 ]'
# --- f2: agi-fill exists but faults
E0=$(mkc $R1 dg1 $AFB:$D/af);CC=$(mkc $R1 dg1 $AFB:$D/af-bad)
for rc in 1 2 3 127;do mkdir -p $D/af$rc;for x in $D/b/*;do [ ${x##*/} = agi-fill ]||ln -sf $x $D/af$rc/${x##*/};done;printf '#!/bin/sh\necho "agi-fill: traceback (shim)" >&2\nexit %s\n' $rc>$D/af$rc/agi-fill;chmod +x $D/af$rc/agi-fill;done
gateE $R1 $CC $D/b;ok "f2d-control-real-agi-fill-refuses-corrupting-edit dg1's CORRUPTING edit (the type line deleted) of a valid node with the real agi-fill: refused" 'refused'
gateE $R1 $E0 $D/b;ok "f2e-control-real-agi-fill-admits-valid-edit dg1's VALID edit with the real agi-fill: admitted" '[ $r = 0 ]'
for rc in 1 2 127;do gateE $R1 $CC $D/af$rc;ok "f2-agi-fill-fault-rc$rc-refused the corrupting edit when agi-fill EXISTS but exits $rc (a crash: a python import error, a KeyError; invalid is rc 3): refused (a crashed checker never reads the new version as invalid and the old as invalid too)" 'refused';done
gateE $R1 $CC $D/af3;ok "f2n-NAMED-CONTROL-exit-3-everywhere-admitted BY DESIGN agi-fill exiting 3 for every call (invalid, by agi-fill's own contract) on both the new version and the baseline: the corrupting edit is a legacy-baseline ADMIT (a node that was already invalid stays editable); this is pinned as the expected ADMIT, not a defect: only a CRASH (rc other than 0 / 3) is refused above" '[ $r = 0 ]'
mkdir -p $D/afr;for x in $D/b/*;do [ ${x##*/} = agi-fill ]||ln -sf $x $D/afr/${x##*/};done;printf '#!/bin/sh\n[ "$2" = n ]&&exit 3\nexec %s/b/agi-fill "$@"\n' $D>$D/afr/agi-fill;chmod +x $D/afr/agi-fill
gateE $R1 $E0 $D/afr;ok "f2r-invalid-new-version-refused agi-fill exiting 3 ONLY on the new version (check n) and the real verdict (valid) on the baseline (check p): a valid edit of a valid node read as invalid: refused (the existing ratchet: the version it replaces passed)" 'refused'
gateX $R1 $C1 "$R1 $X" "$C1:$NN" "" rev-parse;ok "f1b2-lg-commit-read-fails-refused only the COMMIT's read (<C1>:path) fails: refused" 'refused'
R2=$(mkc $R1 owner1 $NN:$D/nv);D1=$(mkc $R1 dg1 $AFB:$D/af)
gateN $R2 $(mkr $R2 $D1 $R2 sm1 $AFB:$D/af) "$R2";ok "f1e-control-standard-merge-up-admitted the standard merge-up M = merge(R2 holding the owner node, D1) signed by sm: admitted" '[ $r = 0 ]'
# --- f3 (SM 10:20Z R1, DG3 10:27Z: NAMED, REFUSED): the agi-fill sentinel reads [moral].md AT THE RECEIVING TIP, so an owner-landed [moral].md that breaks it (required: [] or removed) refuses EVERY later push 'agi-fill sentinel', the owner's repair push included (the repair is a root-side re-land): pinned as the documented outcome
MS=.agi/context/schemas/[moral].md;git show $o:$MS|sed 's/^  required: \[.*\]/  required: []/'>$D/moral-empty;grep -q '^  required: \[\]' $D/moral-empty||{ echo "FAIL fixture: [moral].md has no required line";f=$((f+1));}
TE=$(mkc $R1 owner1 "$MS:$D/moral-empty")
x=$D/i;GIT_INDEX_FILE=$x git read-tree $R1;GIT_INDEX_FILE=$x git update-index --force-remove "$MS";TR=$(GIT_INDEX_FILE=$x git write-tree);rm -f $x;TD=$(sgn owner1 -p $R1 -m r5f $TR)
gate $R1 $E0;ok "f3c-control-intact-moral-schema-admitted the tip with the INTACT [moral].md: dg1's valid edit is admitted (the sentinel reads rc 3)" '[ $r = 0 ]'
gate $TE $(mkc $TE dg1 $AFB:$D/af);ok "f3a-moral-required-empty-refuses-every-push the tip holds [moral].md with required: [] (landed by the owner): dg1's valid edit is refused 'agi-fill sentinel' (named, by design)" 'refused&&grep -q "agi-fill sentinel" $D/out'
gate $TE $(mkc $TE owner1 $MS:$(git show $o:$MS>$D/moral-ok;echo $D/moral-ok));ok "f3a2-owner-repair-push-also-refused the OWNER's repair push (restoring the intact [moral].md) on that tip is refused too: the sentinel reads the RECEIVING tip's schema (the repair path is a root-side re-land)" 'refused&&grep -q "agi-fill sentinel" $D/out'
gate $TD $(mkc $TD dg1 $AFB:$D/af);ok "f3b-moral-removed-refuses-every-push the tip has NO [moral].md (removed): dg1's valid edit is refused 'agi-fill sentinel' (named, by design)" 'refused&&grep -q "agi-fill sentinel" $D/out'
echo "grow-gate-ring5f: $f FAIL"
exit $f
