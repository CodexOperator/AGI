#!/bin/sh
# grow-gate-ab.t.sh [TRUNK] [GITDIR]: AA2.54 (hypothesis g716111-ab-the-ring-is-a-trunk-node-and-a-commit-lands-only-if-its-signer-is-ancestor-or-self-of-every-name-ruling-its-paths): the INTEGRATED grow-gate admits a commit only if its signer is a ring line open at the
# RECEIVING tip and an ancestor-or-self of every name that rules each path it changes (a ring line: its post · a node: its `ring:` cell · schemas / growth.tsv / .github: the rules cell · a posts.md tree move: BOTH the old and the new parent); no date is read.
# ONE FILE, written from section AB's table (C / E rows) directly (DG1 04:06Z: self-perpetuating's run.sh was returned at 84/2 and is not leaned on; take its cases over later as one script line each once it reads 86/0 on the trunk). It tests the INTEGRATED gate (grow-gate's pre-receive interface, GROW_GATE=<file> = the candidate):
# the box's AGI_ALLOWED is made OVER-PERMISSIVE on purpose (every key ever made, retired ones included), so today's gate admits every signed commit and
# every refusal lane below is RED on it; the integrated gate must refuse by the ring AT THE RECEIVING TIP, never by that file. Scratch repo borrowing GITDIR's objects (0 shared refs written), scratch keys made at run time (no armoured block in this file), no network, nothing pushed.
# SEAMS pinned (a builder may not move them; DG2 flags each): the ring is .agi/nodes/.geometry/ring, plain lines `post keytype b64`, no frontmatter, one line per post (the scratch ring is written by each fixture); the receiving trunk is AGI_TRUNK; the rules cell is env AGI_RULES (default owner;
# option B = belam) until it is a graph cell; under option B the ring has NO owner line, belam is above every post. One ok/FAIL line per case; exit = FAIL count.
T=${1:-local-maxxing/season2/main};G=${2:-$(git rev-parse --path-format=absolute --git-common-dir)};SELF=$(cd "$(dirname "$0")" && pwd);R0=${ROOT:-$(cd "$SELF/../../.." && pwd)};D=$(mktemp -d);trap 'rm -rf $D' EXIT;mkdir $D/b $D/k;f=0;CEIL=${CEIL:-4705}
ok(){ if eval "$2";then echo "ok $1";else echo "FAIL $1 [rc=$r $(tail -1 $D/out 2>/dev/null|cut -c1-90)]";f=$((f+1));fi;}
r=0
# --- the section's own verdicts, by self-perpetuating's landed fixture runner (86 PASS / 0 FAIL on the trunk): ONE line, RUNSH=<path> overrides, a missing runner is a FAIL
RUNSH=${RUNSH:-$R0/.agi/context/local-maxxing/ab/run.sh}
if [ -f "$RUNSH" ];then (cd $(dirname "$RUNSH")&&timeout 600 sh $RUNSH ${AB_REV:-HEAD}>$D/run.out 2>&1);rr=$?;else echo "no runner at $RUNSH">$D/run.out;rr=99;fi
ok "ab-runner the section's fixture runner ($(basename "$RUNSH")) exits 0 with 0 FAIL ($(tail -1 $D/run.out|cut -c1-60))" '[ $rr = 0 ]&&tail -1 $D/run.out|grep -q " 0 FAIL"'
# --- the integrated grow-gate
o=$(git rev-parse $T)||exit 1;for x in sect grow-check grow-gate agi-fill;do git ls-tree --full-tree --name-only $o .agi/nodes/.geometry/|grep '/engine[^/]*\.md$'|sed "s|^|$o:|"|git cat-file --batch --follow-symlinks|sed -n "/^###* $x /,/^###* /{/^~~~/,/^~~~/{//!p}}">$D/b/$x;done
[ "$GROW_GATE" ]&&cp $GROW_GATE $D/b/grow-gate;chmod +x $D/b/*;[ -s $D/b/grow-gate ]||{ echo "FAIL no grow-gate at $T";exit 99;}
unset GIT_AUTHOR_NAME GIT_AUTHOR_EMAIL GIT_COMMITTER_NAME GIT_COMMITTER_EMAIL GIT_DIR GIT_WORK_TREE AGI_RULES AGI_TRUNK
for n in belam1 belam2 alive1 alive2 sm1 dg1 dg2;do ssh-keygen -qN "" -ted25519 -f$D/k/$n -C $n>/dev/null;done
pk(){ cut -d' ' -f1,2 $D/k/$1.pub;}
: >$D/over;for n in belam1 belam2 alive1 alive2 sm1 dg1 dg2;do p=${n%[0-9]};case $p in sm)p=sm;;esac;echo "$p@agi namespaces=\"git\" $(pk $n)">>$D/over;done   # OVER-PERMISSIVE: every key ever made
git init -q $D/r;echo $G/objects>$D/r/.git/objects/info/alternates;cd $D/r;export PATH=$D/b:$PATH
GEO=.agi/nodes/.geometry
printf -- '---\n---\n  - {"name": "belam", "parent": "owner"}\n  - {"name": "council", "parent": "belam"}\n  - {"name": "keep", "parent": "belam"}\n  - {"name": "alive", "parent": "council"}\n  - {"name": "sm", "parent": "keep"}\n  - {"name": "dg1", "parent": "sm"}\n  - {"name": "dg2", "parent": "sm"}\n  - {"name": "dg9", "parent": "sm"}\n'>$D/posts.md
printf 'belam %s\nalive %s\nsm %s\ndg1 %s\ndg2 %s\n' "$(pk belam1)" "$(pk alive1)" "$(pk sm1)" "$(pk dg1)" "$(pk dg2)">$D/ring
git show $o:.agi/nodes/moral/antifragility.md|sed 's/^id: moral:antifragility/id: moral:zz-ab-sm/;s/^mint_id: .*/mint_id: 1123456789abcdef0123456789abcdef/;s/^type: moral/type: moral\nring: [sm]/'>$D/n-sm
git show $o:.agi/nodes/moral/antifragility.md|sed 's/^id: moral:antifragility/id: moral:zz-ab-alive/;s/^mint_id: .*/mint_id: 2123456789abcdef0123456789abcdef/;s/^type: moral/type: moral\nring: [alive]/'>$D/n-alive
SCH=$(git ls-tree --name-only $o .agi/context/schemas/|head -1)
# mkc BASE KEYNAME [path:file ...]: a signed commit on BASE whose tree is BASE + those files
mkc(){ b=$1;k=$2;shift 2;x=$D/i;GIT_INDEX_FILE=$x git read-tree $b;for a in "$@";do GIT_INDEX_FILE=$x git update-index --add --cacheinfo 100644,$(git hash-object -w "${a#*:}"),"${a%%:*}";done;tr=$(GIT_INDEX_FILE=$x git write-tree);rm -f $x
 pn=${k%[0-9]};env GIT_COMMITTER_NAME=$pn GIT_COMMITTER_EMAIL=$pn@agi GIT_AUTHOR_NAME=$pn GIT_AUTHOR_EMAIL=$pn@agi ${CD:+"GIT_COMMITTER_DATE=$CD" "GIT_AUTHOR_DATE=$CD"} git -c gpg.format=ssh -c user.signingkey=$D/k/$k commit-tree -S -p $b -m ab $tr;}
# base R: the receiving trunk = the real trunk tree + the fixture ring, posts tree, two ringed nodes
x=$D/i;GIT_INDEX_FILE=$x git read-tree $o;for a in $GEO/ring:$D/ring $GEO/posts.md:$D/posts.md .agi/nodes/moral/zz-ab-sm.md:$D/n-sm .agi/nodes/moral/zz-ab-alive.md:$D/n-alive;do GIT_INDEX_FILE=$x git update-index --add --cacheinfo 100644,$(git hash-object -w "${a#*:}"),"${a%%:*}";done
R=$(GIT_AUTHOR_NAME=g GIT_AUTHOR_EMAIL=g@g GIT_COMMITTER_NAME=g GIT_COMMITTER_EMAIL=g@g git commit-tree -m ab-base -p $o $(GIT_INDEX_FILE=$x git write-tree));rm -f $x
sh_(){ git show $1:$2; }                    # sh_ BASE PATH
# gate BASE TIP: BASE is the receiving trunk. refused = non-zero (124 = a hang)
gate(){ git update-ref refs/heads/trunk $1;echo "$1 $2 refs/heads/x"|AGI_ALLOWED=$D/over AGI_TRUNK=refs/heads/trunk AGI_NOT=$1 timeout 60 grow-gate>$D/out 2>&1;r=$?;}
refused(){ [ $r != 0 ]&&[ $r != 124 ];}
edit(){ sh_ $1 $2|sed "$3">$D/e;}           # edit BASE PATH 'sed expr' -> $D/e
NS=.agi/nodes/moral/zz-ab-sm.md;NA=.agi/nodes/moral/zz-ab-alive.md
# C1 C4: a post's CURRENT key edits a node ringed to it: admitted (and a plain edit to a node ringed [sm] by sm)
edit $R $NA '$a\
edit-a';gate $R $(mkc $R alive1 $NA:$D/e);ok "c1-current-key-admitted alive's current key edits a node ringed [alive]" '[ $r = 0 ]'
edit $R $NS '$a\
edit-s';gate $R $(mkc $R sm1 $NS:$D/e);ok "c11-ring-member-admitted sm edits a node ringed [sm]" '[ $r = 0 ]'
# C2 C18a: a generation hands off (its own ring line, signed by the outgoing key): admitted. The landed handoff is the new receiving tip R2.
edit $R $GEO/ring "s|^alive .*|alive $(pk alive2)|";H=$(mkc $R alive1 $GEO/ring:$D/e);gate $R $H;ok "c2-handoff-admitted alive gen1 replaces its own ring line with gen2, signed by gen1" '[ $r = 0 ]'
R2=$H
# C3: the RETIRED generation after the handoff has landed: refused, though the box's allowed-signers file still holds its key (over-permissive on purpose)
edit $R2 $NA '$a\
late';gate $R2 $(mkc $R2 alive1 $NA:$D/e);ok "c3-retired-generation-refused alive gen1 after its handoff landed is refused (AGI_ALLOWED still lists it: the ring at the receiving tip decides)" 'refused'
CD="$(date -d '-1 day' -R)";gate $R2 $(mkc $R2 alive1 $NA:$D/e);unset CD;ok "c3b-backdated-refused the same commit BACKDATED a day is refused (no date is read)" 'refused'
edit $R2 $NA '$a\
now';gate $R2 $(mkc $R2 alive2 $NA:$D/e);ok "c4-new-generation-admitted alive gen2 edits the node" '[ $r = 0 ]'
# C5: SM merges an OLD-BASE side commit signed by the retired generation: the side commit meets the receiving ring and is refused
edit $R $NA '$a\
side';SIDE=$(mkc $R alive1 $NA:$D/e);MG=$(GIT_COMMITTER_NAME=sm GIT_COMMITTER_EMAIL=sm@agi GIT_AUTHOR_NAME=sm GIT_AUTHOR_EMAIL=sm@agi git -c gpg.format=ssh -c user.signingkey=$D/k/sm1 commit-tree -S -p $R2 -p $SIDE -m merge $(git rev-parse $R2^{tree}));gate $R2 $MG;ok "c5-old-base-side-commit-refused sm merges a side commit signed by alive's retired gen1: the side commit is refused" 'refused'
# C6 C9: who may write whose ring line
edit $R $GEO/ring "s|^alive .*|alive $(pk dg1)|";gate $R $(mkc $R dg1 $GEO/ring:$D/e);ok "c6-not-above-refused dg1 rewrites alive's ring line (dg1 is not above alive)" 'refused'
sh_ $R $GEO/ring>$D/e;echo "dg9 $(pk alive1)">>$D/e;gate $R $(mkc $R alive2 $GEO/ring:$D/e);ok "c9-stand-up-by-non-ancestor-refused alive stands up dg9's line (alive is not above dg9)" 'refused'
edit $R $GEO/ring "s|^alive .*|alive $(pk alive2)|";gate $R $(mkc $R belam1 $GEO/ring:$D/e);ok "c7-revouch-by-ancestor-admitted belam re-vouches alive's line (an ancestor)" '[ $r = 0 ]'
sh_ $R $GEO/ring>$D/e;echo "dg9 $(pk dg2)">>$D/e;gate $R $(mkc $R sm1 $GEO/ring:$D/e);ok "c8-stand-up-by-parent-admitted sm stands up dg9's line (its parent)" '[ $r = 0 ]'
# C10 C11 C12 C13: a node ringed [sm]
edit $R $NS '$a\
x';gate $R $(mkc $R dg1 $NS:$D/e);ok "c10-below-the-ring-refused dg1 edits a node ringed [sm]" 'refused'
gate $R $(mkc $R belam1 $NS:$D/e);ok "c12-closure-admits-the-above belam edits it (an ancestor of sm: the closure)" '[ $r = 0 ]'
gate $R $(mkc $R alive1 $NS:$D/e);ok "c13-outside-the-subtree-refused alive edits it" 'refused'
# C14 C16: a schema: rules = owner by default (belam's plain key refused); option B (AGI_RULES=belam) admits belam
edit $R $SCH '$a\
s';gate $R $(mkc $R belam1 $SCH:$D/e);ok "c14-schema-rules-owner belam's plain key changes a schema: refused (rules = owner)" 'refused'
export AGI_RULES=belam;gate $R $(mkc $R belam1 $SCH:$D/e);ok "c16-option-b belam changes it under AGI_RULES=belam: admitted" '[ $r = 0 ]';gate $R $(mkc $R sm1 $SCH:$D/e);ok "c16b-option-b-only-belam-and-above sm changes it under AGI_RULES=belam: refused" 'refused';unset AGI_RULES
# C20 C21: the owner line is ruled by owner alone (when a line exists: written into this fixture's ring as a plain line)
{ cat $D/ring;echo "owner $(pk belam1)";}>$D/ring2;gate $R $(mkc $R sm1 $GEO/ring:$D/ring2);ok "c20-sm-cannot-add-the-owner-line sm adds an owner line: refused" 'refused'
O1=$(mkc $R belam1 $GEO/ring:$D/ring2);gate $R $O1;ok "c21a-belam-cannot-add-the-owner-line belam adds an owner line: refused (only owner is above owner)" 'refused'
# E1-E8: the tree-move rule
edit $R $GEO/posts.md 's|"name": "belam", "parent": "owner"|"name": "belam", "parent": "sm"|';gate $R $(mkc $R sm1 $GEO/posts.md:$D/e);ok "e1-lift-above-ancestors-refused sm re-parents belam under itself: refused (ruled by owner, belam's old parent)" 'refused'
edit $R $GEO/posts.md 's|"name": "dg2", "parent": "sm"|"name": "dg2", "parent": "dg1"|';gate $R $(mkc $R sm1 $GEO/posts.md:$D/e);ok "e2-move-within-subtree-admitted sm moves dg2 under dg1 (both parents under sm)" '[ $r = 0 ]'
edit $R $GEO/posts.md 's|"name": "dg2", "parent": "sm"|"name": "dg2", "parent": "keep"|';gate $R $(mkc $R sm1 $GEO/posts.md:$D/e);ok "e3-move-out-above-refused sm moves dg2 out to keep (keep is above sm): refused" 'refused'
gate $R $(mkc $R belam1 $GEO/posts.md:$D/e);ok "e4-the-same-move-by-belam belam makes that move: admitted" '[ $r = 0 ]'
edit $R $GEO/posts.md 's|"name": "dg1", "parent": "sm"|"name": "dg1", "parent": "sm", "tier": 2|';gate $R $(mkc $R sm1 $GEO/posts.md:$D/e);ok "e5-field-edit-admitted sm edits dg1's tier (no parent changes)" '[ $r = 0 ]'
edit $R $GEO/posts.md 's|"name": "dg1", "parent": "sm"|"name": "dg1", "parent": "belam"|';gate $R $(mkc $R dg1 $GEO/posts.md:$D/e);ok "e6-self-lift-refused dg1 moves ITSELF under belam: refused" 'refused'
edit $R $GEO/posts.md '$a\
  - {"name": "dg8", "parent": "sm"}';gate $R $(mkc $R sm1 $GEO/posts.md:$D/e);ok "e7-stand-up-under-self-admitted sm stands up a row under itself" '[ $r = 0 ]'
edit $R $GEO/posts.md '$a\
  - {"name": "dg8", "parent": "belam"}';gate $R $(mkc $R sm1 $GEO/posts.md:$D/e);ok "e8-stand-up-under-belam-refused sm stands up a row under belam: refused" 'refused'
# a signature by a key that is in NO ring line and in the over-permissive file: refused; the ring itself is only advanced by admitted commits
edit $R $NA '$a\
q';gate $R $(mkc $R alive1 $NA:$D/e);ok "x1-sanity a plain current-key edit still lands after all the above (the fixture is sound)" '[ $r = 0 ]'
# a private-key block still refused through the integrated gate (AA2.54b: the key line stays)
DDS=-----;{ cat $D/e;printf '%sBEGIN OPENSSH PRIVATE KEY%s\n%s\n%sEND OPENSSH PRIVATE KEY%s\n' $DDS $DDS "$(head -c 60 /dev/urandom|base64 -w 64)" $DDS $DDS;}>$D/kk;gate $R $(mkc $R alive1 $NA:$D/kk);ok "key54b-private-key-line-stays a private key block is still refused by the integrated gate" 'refused'
# --- RING BOOTSTRAP (DG1 04:29Z): the gate is open ONLY while the ring path has NEVER existed in the receiving tip's history; after that it stays on
mkd(){ b=$1;k=$2;shift 2;x=$D/i;GIT_INDEX_FILE=$x git read-tree $b;for a in "$@";do GIT_INDEX_FILE=$x git update-index --force-remove "$a";done;tr=$(GIT_INDEX_FILE=$x git write-tree);rm -f $x
 pn=${k%[0-9]};env GIT_COMMITTER_NAME=$pn GIT_COMMITTER_EMAIL=$pn@agi GIT_AUTHOR_NAME=$pn GIT_AUTHOR_EMAIL=$pn@agi git -c gpg.format=ssh -c user.signingkey=$D/k/$k commit-tree -S -p $b -m ab $tr;}
gate $o $(mkc $o belam1 $GEO/ring:$D/ring);ok "bs-a-first-ring-commit-lands with no ring at the receiving tip and none in its history, belam's first ring commit lands (the gate behaves as today)" '[ $r = 0 ]'
gate $R $(mkd $R dg1 $GEO/ring);ok "bs-b-delete-by-non-top-refused once the ring exists, DG1 deleting it is refused (ruled by every name it removes)" 'refused'
A=$(mkd $R dg1 $GEO/ring);edit $R $NA '$a\
after-delete';B=$(mkc $A alive1 $NA:$D/e);gate $R $B;ok "bs-b2-commit-after-refused-delete-still-gated a push of [DG1 deletes the ring, then a valid ring member edits a node] is refused AS A WHOLE (the second commit does not ride the first)" 'refused'
gate $R $(mkc $R alive2 $NA:$D/e);ok "bs-b3-gate-still-on after that refusal the receiving tip still gates: a key that is no ring line at it (alive gen2 before its hand-off) is refused" 'refused'
: >$D/empty;EM=$(mkc $R belam1 $GEO/ring:$D/empty);gate $R $EM;ok "bs-c-empty-by-top-admitted belam (the top: an ancestor of every name the commit removes) empties the ring: admitted" '[ $r = 0 ]'
edit $EM $NA '$a\
after-empty';gate $EM $(mkc $EM dg1 $NA:$D/e);ok "bs-c2-no-reopen after the ring was emptied, a following DG1 commit is still refused (the ring existed in history: the bootstrap does not reopen)" 'refused'
gate $EM $(mkc $EM belam1 $NA:$D/e);ok "bs-c3-no-reopen-even-for-belam and so is belam's: an empty ring has no signer, and the gate is not off" 'refused'
DEL=$(mkd $R belam1 $GEO/ring);gate $R $DEL;ok "bs-e-delete-by-top-admitted belam (the top) DELETES the ring file: admitted (ruled by every name it removes, and belam is above them all)" '[ $r = 0 ]'
edit $R $NA '$a\
after-del';gate $DEL $(mkc $DEL dg1 $NA:$D/e);ok "bs-e2-no-reopen-after-delete after the ring file was deleted, a following DG1 commit is still refused (the path existed in history: the bootstrap stays shut)" 'refused'
gate $DEL $(mkc $DEL belam1 $NA:$D/e);ok "bs-e3-no-reopen-after-delete-belam and a following belam commit too" 'refused'
sed 's/^id: moral:zz-ab-sm/id: moral:zz-ab-sp/;s/^mint_id: .*/mint_id: 3123456789abcdef0123456789abcdef/' $D/n-sm>$D/n-sp;R2=$(mkc $R belam1 ".agi/nodes/moral/zz ab sp.md:$D/n-sp");git show "$R2:.agi/nodes/moral/zz ab sp.md"|sed '$a\
x'>$D/e;gate $R2 $(mkc $R2 dg1 ".agi/nodes/moral/zz ab sp.md:$D/e")
ok "bs-d-path-with-space a node whose PATH HAS A SPACE, ringed [sm], edited by DG1 is refused (a path git quotes does not slip past the ruler lookup)" 'refused'
# --- FAIL CLOSED (DG1 04:40Z): a git error in the commit walk refuses the land, naming the commit; RED on a gate that reads an error as 'no changes'
edit $R $NA '$a\
fc';FC=$(mkc $R alive1 $NA:$D/e);t=$(git rev-parse $FC^{tree});rm -f $D/r/.git/objects/${t%${t#??}}/${t#??};gate $R $FC
ok "fc-a-diff-tree-fails a commit whose tree object is missing (git diff-tree fails) is REFUSED, rc non-zero, naming the commit" 'refused&&grep -q $FC $D/out'
edit $R $NA '$a\
fc1';F1=$(mkc $R alive1 $NA:$D/e);edit $F1 $NA '$a\
fc2';F2=$(mkc $F1 alive1 $NA:$D/e);rm -f $D/r/.git/objects/${F1%${F1#??}}/${F1#??};gate $R $F2
ok "fc-b-rev-list-fails a range whose parent commit is unreadable (git rev-list fails) is REFUSED, rc non-zero (an error is not an empty range)" 'refused&&grep -q refused $D/out'
# --- AA2.54c: the size rails
sz=$(wc -c<$D/b/grow-gate);eng=$(git show $o:.agi/nodes/.geometry/engine.md|sed -n 's/^grow-gate *\([0-9]*\) B.*/\1/p;q')
ok "bytes-ceiling grow-gate is $sz B <= $CEIL B (the key-gate build's 1,833 B + a ring-gate delta strictly under the prototype's 2,855 B = 4,705 B; the builder reports the number and the engine.md before/after wc -c and per-line delta)" '[ $sz -le $CEIL ]'
ok "no-ssh-agent-no-python the integrated gate calls no python and no ssh-agent (the prototype's cert-date reader is python: a decision the build must name)" '! grep -qi "python\|ssh-agent" $D/b/grow-gate'
echo "grow-gate-ab: $f FAIL"
exit $f
