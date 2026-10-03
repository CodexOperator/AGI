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
git init -q $D/r;echo $G/objects>$D/r/.git/objects/info/alternates;cd $D/r;export PATH=$D/b:$PATH;printf '#!/bin/sh\nexit 0\n'>$D/b/ckpt;chmod +x $D/b/ckpt
GEO=.agi/nodes/.geometry;RG=$GEO/ring;PM=$GEO/posts.md
printf -- '---\n---\n  - {"name": "belam", "parent": "owner"}\n  - {"name": "keep", "parent": "belam"}\n  - {"name": "sm", "parent": "keep"}\n  - {"name": "dg1", "parent": "sm"}\n  - {"name": "dg2", "parent": "sm"}\n'>$D/posts.md
printf 'belam ssh-ed25519 %s\nsm ssh-ed25519 %s\ndg1 ssh-ed25519 %s\ndg2 ssh-ed25519 %s\n' "$(kb belam1)" "$(kb sm1)" "$(kb dg1)" "$(kb dg2)">$D/ring
A1=.agi/nodes/moral/antifragility.md;A2=.agi/nodes/moral/beauty.md
for a in $A1 $A2;do git show $o:$a>$D/n$(basename $a);echo plain-edit>>$D/n$(basename $a);done
# mkx "P1 P2.." SIGNER|- TREEFROM path:file ...: a commit (signed by SIGNER's key, or unsigned) with those parents (- = orphan) whose tree is TREEFROM's tree + the path:file edits (path:- removes)
mkx(){ ps=$1;sg=$2;tf=$3;shift 3;x=$D/i;GIT_INDEX_FILE=$x git read-tree $tf^{tree}
 for a in "$@";do md=100644;case $a in 120000+*)md=120000;a=${a#120000+};;esac;pa=${a%%:*};fa=${a#*:};if [ "$fa" = - ];then GIT_INDEX_FILE=$x git update-index --force-remove $pa;else GIT_INDEX_FILE=$x git update-index --add --cacheinfo $md,$(git hash-object -w "$fa"),$pa;fi;done
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
X=$(mkx - belam1 $(git mktree </dev/null));M=$(mkx "$R1 $X" - $P0);gate $R1 $M;ok "d2a-orphan-empty-root-refused [X, M]: X an orphan root with the EMPTY tree signed by BELAM (a ring key that can sign an orphan), M an UNSIGNED merge(R1, X) deleting the ring: refused" 'refused'
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
# --- RING.5 (mur sm18 on dg3-ring 0d58fa0ae: R1 R2 R3)
# d6 (R2) an EVIL MERGE: the tip H deleted a node, M = merge(H, R1) re-adds it with garbage: the COMBINED diff prints AM (absent in parent 1), phase 3 tested only A and the ratchet baseline c^ was empty, so an invalid unkeyed node landed; any status holding an A is now an add (and, since RING.5c, phase 3 ALSO runs on diff(landed tip, commit))
H=$(mkg $R1 $A2:-);EV=$D/evil;printf 'garbage, no front matter\n'>$EV
M=$(mkx "$H $R1" dg1 $H $A2:$EV);gate $H $M;ok "d6a-evil-merge-invalid-node-refused M=merge(H, R1) signed dg1 re-adds a node H deleted, with garbage (combined diff = AM): refused" 'refused'
M=$(mkx "$H $R1" dg1 $H);gate $H $M;ok "d6b-merge-adding-nothing-admitted control: the same merge(H, R1) keeping H's tree (no node re-added): admitted" '[ $r = 0 ]'
# d7 (R3) .gitattributes is ruled (default owner): a ring signer may not land export-ignore on schemas / growth.tsv (git archive would drop them and the node checks would run against nothing)
printf '.agi/context/schemas export-ignore\n.agi/nodes/.geometry/growth.tsv export-ignore\n'>$D/ga
gate $R1 $(mkc $R1 dg1 .gitattributes:$D/ga);ok "d7a-gitattributes-refused dg1 lands a root .gitattributes with export-ignore on the schemas: refused (ruled by owner)" 'refused'
gate $R1 $(mkc $R1 dg1 .agi/context/.gitattributes:$D/ga);ok "d7b-nested-gitattributes-refused the same in a subdirectory: refused" 'refused'
export AGI_RULES=dg1;gate $R1 $(mkc $R1 dg1 .gitattributes:$D/ga);unset AGI_RULES;ok "d7c-gitattributes-ruled-by-the-rules-cell control: with AGI_RULES=dg1 the same commit is admitted (the path is ruled by the rules cell like .github)" '[ $r = 0 ]'
# d8 (R1) an error reading the ring at the landed tip must REFUSE, never leave the bootstrap flag open: [S = first ring (dg1... belam), C = dg1 edits a node ringed [sm]] with a git shim that fails the 2nd `git show S:ring`
printf -- '---\nring: [sm]\n---\nbody\n'>$D/ringed;printf -- '---\nring: [sm]\n---\nbody edited\n'>$D/ringed2;NR=.agi/nodes/moral/zz-ringed.md
P1=$(mkg $P0 $NR:$D/ringed);S0=$(mkc $P1 belam1 $RG:$D/ring);C0=$(mkc $S0 dg1 $NR:$D/ringed2)
mkdir $D/shim;printf '#!/bin/sh\nif [ "$1" = show ]&&[ "$2" = %s ];then n=$(cat %s/cnt 2>/dev/null||echo 0);n=$((n+1));echo $n>%s/cnt;[ $n = 2 ]&&{ echo "fatal: shim: object unreadable">&2;exit 128;};fi\nexec /usr/bin/git "$@"\n' "$S0:$RG" $D/shim $D/shim>$D/shim/git;chmod +x $D/shim/git
rm -f $D/shim/cnt;PATH=$D/shim:$PATH gate $P1 $C0;ok "d8a-ring-read-error-refuses with the 2nd read of the ring at the landed tip failing, [S first ring, C dg1 edits a node ringed [sm]] is refused (the open bootstrap flag skipped every path rule: rc 0 on 0d58fa0ae)" 'refused'
rm -f $D/shim/cnt;gate $P1 $C0;ok "d8b-same-push-no-error-refused control: without the shim the same push is refused by the node's ring cell (dg1 is not sm or above it)" 'refused'
rm -f $D/shim/cnt;C1=$(mkc $S0 sm1 $NR:$D/ringed2);gate $P1 $C1;ok "d8c-same-push-sm-admitted control: sm (the ring cell's name) editing that node after the first ring: admitted" '[ $r = 0 ]'
# --- RING.5c (SM mur sm18 on RING.5b: D1 D2)
# d9 (D1) a TYPECHANGE: a ring member turns a valid node into a SYMLINK (mode 120000): phase 3 listed only A and M, so the symlink was never validated
SL=$D/sl;printf 'outside-the-tree\n'>$SL
gate $R1 $(mkc $R1 dg1 120000+$A1:$SL);ok "d9a-symlink-typechange-refused dg1 replaces the valid node $A1 by a symlink (mode 120000): refused" 'refused'
gate $R1 $(mkc $R1 dg1 $A1:$D/n$(basename $A1));ok "d9b-plain-edit-admitted control: dg1's plain valid edit of the same node: admitted" '[ $r = 0 ]'
# d10 (D2) a merge(V, X) with X OUTSIDE the push holding an agi-fill-INVALID version of a valid node and X's tree: diff-tree -c omits a path whose blob equals EITHER parent, so phase 3 never saw the node
gaten(){ git update-ref refs/heads/trunk $1;echo "$1 $2 refs/heads/x"|AGI_ALLOWED=$D/over AGI_TRUNK=refs/heads/trunk AGI_NOT="$1 $3" timeout 60 grow-gate>$D/out 2>&1;r=$?;}
sed '/^type:/d' $D/n$(basename $A1)>$D/af-bad
X=$(mkg $R1 $A1:$D/af-bad);M=$(mkx "$R1 $X" dg1 $X);gaten $R1 $M $X;ok "d10a-merge-with-outside-invalid-parent-refused M=merge(R1, X) signed dg1 with X's tree (X, outside the push, holds the INVALID version of a valid node): refused" 'refused'
M=$(mkx "$X $R1" dg1 $X);gaten $R1 $M $X;ok "d10b-either-parent-order-refused the same with the parents swapped: refused" 'refused'
M=$(mkx "$R1 $X" dg1 $R1);gaten $R1 $M $X;ok "d10c-merge-keeping-the-valid-tree-admitted control: merge(R1, X) with R1's own (valid) tree: admitted" '[ $r = 0 ]'
# --- RING.5d (SM mur sm19 on RING.5c: R1 the standard MERGE-UP shape; notes: symlink/submodule node)
# d11 the trunk gained an OWNER-ringed node after the fork: M = merge(R2, D1) signed sm, D1 (dg1, in the push) a plain edit: the second phase-3 pass (diff of the previous walked commit D1 against M) read the trunk's node as an ADD and refused sm (not the owner); a path whose blob equals a LANDED parent's is already landed
git show $o:$A1|sed 's/^id: moral:antifragility/id: moral:zz-r5d/;s/^mint_id: .*/mint_id: 4123456789abcdef0123456789abcdef/;s/^type: moral/type: moral\nkey: 2fe50ba43c479d67/'>$D/nv
R2=$(mkg $R1 .agi/nodes/moral/zz-r5d.md:$D/nv);D1=$(mkc $R1 dg1 $A2:$D/n$(basename $A2));M=$(mkx "$R2 $D1" sm1 $R2 $A2:$D/n$(basename $A2))
gate $R2 $M;ok "d11a-merge-up-with-trunk-owner-node-admitted [D1, M] M=merge(R2, D1) signed sm, R2 (the tip) added an owner-ringed node after the fork: admitted" '[ $r = 0 ]'
M=$(mkx "$R1 $D1" sm1 $D1);gate $R1 $M;ok "d11b-merge-up-without-new-trunk-node-admitted control: the same merge when the trunk gained nothing: admitted" '[ $r = 0 ]'
# d12 a symlink whose blob is VALID node text: no more power than a delete, now refused outright (120000 / 160000 under .agi/nodes)
git show $o:$A1>$D/validtxt;gate $R1 $(mkc $R1 dg1 120000+$A1:$D/validtxt);ok "d12a-symlink-with-valid-text-refused dg1 turns the node into a symlink whose blob IS valid node text: refused" 'refused'
echo "grow-gate-ring4: $f FAIL"
exit $f
