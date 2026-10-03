#!/bin/sh
# grow-gate-ring4.t.sh [TRUNK] [GITDIR]: RING.4 shape A (SM mur sm18 on dg3-ring 952787f32, five live bypasses of the 5,431 B grow-gate). Each lane is RED on 952787f32's piece (GROW_GATE=<that piece>) and GREEN on RING.4A, each beside an ADMITTED control:
#   d1 a push [P, M] where P is an IN-PUSH first parent and M = merge(P, o) holds tree(o) (o a pre-ring commit): P is skipped by the parent walk and `diff-tree -c` shows nothing for a tree-same merge, so the ring was deleted; also the octopus [P, o, o'] - every commit is now ruled by diff(landed tip, commit)
#   d2 the bootstrap reopened (ring3 g2 also walks an orphan with a tree): an orphan EMPTY-tree root X signed by a ring key has no ring in ITS history, so the per-commit bootstrap flag opened for the unsigned merge(R, X) that deletes the ring; the flag is now computed once, from the receiving tip
#   d3 a posts.md name/parent with a trailing LF ("zz\n" passes jq's `$`): the ancestor map lost an ancestor and the owner's revoke was refused; now \A..\z on every name AND parent, in the map and in the new-version check
#   d4 a NUL-joined ring line ("dg1 K3\0owner K4"): grep -v saw two lines, git diff printed "Binary files differ" (an EMPTY ruler): the ring is read with grep -a / git diff --text and every line must be exactly the canonical shape
#   d5 a ring attribute `-diff` (.git/info/attributes) blanks the ruler diff: --text overrides it
# Same harness as grow-gate-ring3.t.sh (scratch repo borrowing GITDIR's objects, scratch keys, AGI_ALLOWED OVER-PERMISSIVE so only the ring at the receiving tip can refuse). GROW_GATE=<file> = the candidate (default: sect grow-gate of TRUNK). One ok/FAIL line per case; exit = FAIL count.
T=${1:-local-maxxing/season2/main};G=${2:-$(git rev-parse --path-format=absolute --git-common-dir)};D=$(mktemp -d);trap 'rm -rf $D' EXIT;mkdir $D/b $D/k;f=0
ok(){ if eval "$2";then echo "ok $1";else echo "FAIL $1 [rc=$r $(tail -1 $D/out 2>/dev/null|cut -c1-90)]";f=$((f+1));fi;}
r=0
o=$(git rev-parse $T)||exit 1;for x in sect grow-check grow-gate agi-fill;do git ls-tree --full-tree --name-only $o .agi/nodes/.geometry/|grep '/engine[^/]*\.md$'|sed "s|^|$o:|"|git cat-file --batch --follow-symlinks|sed -n "/^###* $x /,/^###* /{/^~~~/,/^~~~/{//!p}}">$D/b/$x;done
[ "$GROW_GATE" ]&&cp $GROW_GATE $D/b/grow-gate;chmod +x $D/b/*;[ -s $D/b/grow-gate ]||{ echo "FAIL no grow-gate at $T";exit 99;}
unset GIT_AUTHOR_NAME GIT_AUTHOR_EMAIL GIT_COMMITTER_NAME GIT_COMMITTER_EMAIL GIT_DIR GIT_WORK_TREE AGI_RULES AGI_TRUNK;export GIT_CONFIG_GLOBAL=/dev/null GIT_CONFIG_SYSTEM=/dev/null
for n in belam1 sm1 dg1 dg2 atk;do ssh-keygen -qN "" -ted25519 -f$D/k/$n -C $n>/dev/null;done
pk(){ cut -d' ' -f1,2 $D/k/$1.pub;}
kb(){ pk $1|cut -d' ' -f2;}
: >$D/over;for n in belam1 sm1 dg1 dg2 atk;do echo "${n%[0-9]}@agi namespaces=\"git\" $(pk $n)">>$D/over;done
git init -q $D/r;echo $G/objects>$D/r/.git/objects/info/alternates;cd $D/r;export PATH=$D/b:$PATH
GEO=.agi/nodes/.geometry;RG=$GEO/ring;PM=$GEO/posts.md
printf -- '---\n---\n  - {"name": "belam", "parent": "owner"}\n  - {"name": "keep", "parent": "belam"}\n  - {"name": "sm", "parent": "keep"}\n  - {"name": "dg1", "parent": "sm"}\n  - {"name": "dg2", "parent": "sm"}\n'>$D/posts.md
printf 'belam ssh-ed25519 %s\nsm ssh-ed25519 %s\ndg1 ssh-ed25519 %s\ndg2 ssh-ed25519 %s\n' "$(kb belam1)" "$(kb sm1)" "$(kb dg1)" "$(kb dg2)">$D/ring
A1=.agi/nodes/moral/antifragility.md;A2=.agi/nodes/moral/beauty.md
for a in $A1 $A2;do git show $o:$a>$D/n$(basename $a);echo plain-edit>>$D/n$(basename $a);done
# mkx "P1 P2.." SIGNER|- TREEFROM path:file ...: a commit (signed by SIGNER's key, or unsigned) with those parents (- = orphan) whose tree is TREEFROM's tree + the path:file edits (path:- removes)
mkx(){ ps=$1;sg=$2;tf=$3;shift 3;x=$D/i;GIT_INDEX_FILE=$x git read-tree $tf^{tree}
 for a in "$@";do pa=${a%%:*};fa=${a#*:};if [ "$fa" = - ];then GIT_INDEX_FILE=$x git update-index --force-remove $pa;else GIT_INDEX_FILE=$x git update-index --add --cacheinfo 100644,$(git hash-object -w "$fa"),$pa;fi;done
 tr=$(GIT_INDEX_FILE=$x git write-tree);rm -f $x;pa=;for q in $ps;do [ $q = - ]||pa="$pa -p $q";done
 pn=${sg%[0-9]};if [ "$sg" = - ];then env GIT_COMMITTER_NAME=u GIT_COMMITTER_EMAIL=u@agi GIT_AUTHOR_NAME=u GIT_AUTHOR_EMAIL=u@agi git commit-tree $pa -m r4 $tr;else env GIT_COMMITTER_NAME=$pn GIT_COMMITTER_EMAIL=$pn@agi GIT_AUTHOR_NAME=$pn GIT_AUTHOR_EMAIL=$pn@agi git -c gpg.format=ssh -c user.signingkey=$D/k/$sg commit-tree -S $pa -m r4 $tr;fi;}
mkc(){ b=$1;s=$2;shift 2;mkx $b $s $b "$@";}
mkg(){ b=$1;shift;mkx $b - $b "$@";}   # an unsigned plain commit on b (fixtures)
# P0 = the trunk + the fixture posts tree (NO ring); R1 = P0 + the ring only; R = R1 (the receiving tip with a ring and a ring in history)
P0=$(mkg $o $PM:$D/posts.md);R1=$(mkg $P0 $RG:$D/ring)
# gate TIP NEWTIP: TIP is the receiving trunk; refused = non-zero (124 = a hang)
gate(){ git update-ref refs/heads/trunk $1;echo "$1 $2 refs/heads/x"|AGI_ALLOWED=$D/over AGI_TRUNK=refs/heads/trunk AGI_NOT=$1 timeout 60 grow-gate>$D/out 2>&1;r=$?;}
refused(){ [ $r != 0 ]&&[ $r != 124 ];}
# --- d1: in-push first parent
S=$(mkc $R1 dg1 $A1:$D/n$(basename $A1))
C=$(mkc $S dg1 $RG:-);gate $R1 $C;ok "d1a-nonmerge-ring-delete-refused control: [S, C] where C (dg1) deletes the ring on top of the in-push S: refused" 'refused'
M=$(mkx "$S $P0" dg1 $P0);gate $R1 $M;ok "d1b-inpush-first-parent-merge-refused [S, M=merge(S, pre-ring P0) with P0's tree] signed dg1 deletes the ring (S is in the push, P0 is not): refused" 'refused'
M=$(mkx "$S $P0 $o" dg1 $P0);gate $R1 $M;ok "d1c-octopus-refused the same as an octopus merge(S, P0, o): refused" 'refused'
M=$(mkx "$S $P0" dg1 $S);gate $R1 $M;ok "d1d-merge-keeping-ring-admitted control: [S, M=merge(S, P0) with S's tree] (the ring kept) signed dg1: admitted" '[ $r = 0 ]'
S2=$(mkc $R1 dg1 $A2:$D/n$(basename $A2));M=$(mkx "$S $S2" dg1 $S $A2:$D/n$(basename $A2));gate $R1 $M;ok "d1e-two-branch-merge-admitted control: [S, S2, merge(S, S2)] all dg1, two unringed node edits: admitted" '[ $r = 0 ]'
# --- d2: the bootstrap stays closed through an orphan root
X=$(mkx - dg1 $(git mktree </dev/null));M=$(mkx "$R1 $X" - $P0);gate $R1 $M;ok "d2a-orphan-empty-root-refused [X, M]: X an orphan root with the EMPTY tree signed dg1, M an UNSIGNED merge(R1, X) deleting the ring: refused" 'refused'
gate $P0 $(mkc $P0 dg1 $RG:$D/ring);ok "d2b-bootstrap-still-open control: a tip whose history never held a ring takes a first, canonical, signed ring: admitted" '[ $r = 0 ]'
# --- d3: a trailing LF in a posts.md name / parent
pr(){ { git show $R1:$PM;printf "$1";}>$D/e;}
pr '  - {"name": "zz\\n", "parent": "dg1"}\n';gate $R1 $(mkc $R1 dg1 $PM:$D/e);ok "d3a-trailing-lf-name-refused dg1 adds a posts.md row whose NAME ends in a LF (it would erase dg1's own ancestors in the map): refused" 'refused'
pr '  - {"name": "zz", "parent": "dg1\\n"}\n';gate $R1 $(mkc $R1 dg1 $PM:$D/e);ok "d3b-trailing-lf-parent-refused a row whose PARENT ends in a LF: refused" 'refused'
pr '  - {"name": "zz\\n", "parent": "dg1"}\n';RP=$(mkg $R1 $PM:$D/e)
git show $R1:$RG|grep -v '^dg1 '>$D/e;gate $RP $(mkc $RP sm1 $RG:$D/e);ok "d3c-revoke-with-poison-row-in-the-tip-admitted a poisoned row already in the tip: sm (dg1's parent) revoking dg1's ring line is still admitted (the poison row is out of the map)" '[ $r = 0 ]'
pr '  - {"name": "dg9", "parent": "dg1"}\n';gate $R1 $(mkc $R1 dg1 $PM:$D/e);ok "d3d-canonical-row-admitted control: dg1 adds a canonical row under itself: admitted" '[ $r = 0 ]'
# --- d4: a NUL in the ring
{ cat $D/ring;printf 'dg1 ssh-ed25519 %s\0owner ssh-ed25519 %s\n' "$(kb atk)" "$(kb atk)";}>$D/e;gate $R1 $(mkc $R1 dg1 $RG:$D/e);ok "d4a-nul-joined-line-refused dg1 adds 'dg1 K<NUL>owner K' (two canonical lines to grep, a binary diff = an empty ruler to git): refused" 'refused'
printf 'belam ssh-ed25519 %s\0sm ssh-ed25519 %s\n' "$(kb belam1)" "$(kb sm1)">$D/e;gate $P0 $(mkc $P0 dg1 $RG:$D/e);ok "d4b-nul-first-ring-refused the FIRST ring (bootstrap) holding a NUL: refused" 'refused'
{ cat $D/ring;printf 'dg1 ssh-ed25519 %s\n' "$(kb atk)";}>$D/e;gate $R1 $(mkc $R1 dg1 $RG:$D/e);ok "d4c-canonical-own-line-admitted control: dg1 adds a canonical second line of its own: admitted" '[ $r = 0 ]'
# --- d5: a ring -diff attribute blanks the ruler diff
printf '%s -diff\n' $RG>$D/r/.git/info/attributes
sed "s|^dg2 .*|dg2 ssh-ed25519 $(kb atk)|" $D/ring>$D/e;gate $R1 $(mkc $R1 dg1 $RG:$D/e);ok "d5a-diff-attribute-sibling-line-refused (.git/info/attributes: ring -diff) dg1 rewrites dg2's line: refused" 'refused'
{ cat $D/ring;printf 'dg1 ssh-ed25519 %s\n' "$(kb atk)";}>$D/e;gate $R1 $(mkc $R1 dg1 $RG:$D/e);ok "d5b-diff-attribute-own-line-admitted control: the same attribute, dg1 adds its own line: admitted" '[ $r = 0 ]'
rm -f $D/r/.git/info/attributes
echo "grow-gate-ring4: $f FAIL"
exit $f
