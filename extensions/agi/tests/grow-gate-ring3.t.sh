#!/bin/sh
# grow-gate-ring3.t.sh [TRUNK] [GITDIR]: RING.3 (SM return 05:12Z + DG1 05:17Z; the demotes SM found on dg3-ring 9abc7c690): the INTEGRATED grow-gate must hold on the four ways round the ring that grow-gate-ab.t.sh does not walk:
#   D1 a TREESAME merge: a merge whose tree IS one parent's (here the pre-ring tree) shows NO change to a combined diff, so a gate that reads only `diff-tree -c` never sees the ring deleted; once the ring is gone the bootstrap must stay CLOSED (the ring existed in that history)
#   D2 a NON-CANONICAL ring line: the ring is `post keytype b64`, one canonical shape; any other shape (a leading space, a tab, a trailing field, an upper-case name, a CR, a keytype outside the five) is a line whose NAME no ruler check sees
#   D3 a posts.md NAME off [a-z][a-z0-9-]* (a newline, a space, upper case) or a garbled tree: a name is a word the ruler walk splits on
#   R5 the FIRST ring (the receiving trunk has none, in no history): a SIGNED, SINGLE-FILE, canonical ring lands; unsigned, a directory ring/<f>, an off-shape line do not
# One file, written from the gate's own rule (the ring's ruler = ancestor-or-self of every name a change removes or adds; no date is read), NOT from run.sh. It tests grow-gate's pre-receive interface (GROW_GATE=<file> = the candidate; default `sect grow-gate` of TRUNK): AGI_ALLOWED is OVER-PERMISSIVE on purpose (every key made), so only the ring at the receiving tip can refuse.
# A control (ok-lane) beside each refusal proves the gate is not simply refusing everything. Scratch repo borrowing GITDIR's objects (0 shared refs written), scratch keys at run time (no armoured block in this file), no network, nothing pushed. One ok/FAIL line per case; exit = FAIL count.
T=${1:-local-maxxing/season2/main};G=${2:-$(git rev-parse --path-format=absolute --git-common-dir)};D=$(mktemp -d);trap 'rm -rf $D' EXIT;mkdir $D/b $D/k;f=0
ok(){ if eval "$2";then echo "ok $1";else echo "FAIL $1 [rc=$r $(tail -1 $D/out 2>/dev/null|cut -c1-90)]";f=$((f+1));fi;}
r=0
o=$(git rev-parse $T)||exit 1;for x in sect grow-check grow-gate agi-fill;do git ls-tree --full-tree --name-only $o .agi/nodes/.geometry/|grep '/engine[^/]*\.md$'|sed "s|^|$o:|"|git cat-file --batch --follow-symlinks|sed -n "/^###* $x /,/^###* /{/^~~~/,/^~~~/{//!p}}">$D/b/$x;done
[ "$GROW_GATE" ]&&cp $GROW_GATE $D/b/grow-gate;chmod +x $D/b/*;[ -s $D/b/grow-gate ]||{ echo "FAIL no grow-gate at $T";exit 99;}
unset GIT_AUTHOR_NAME GIT_AUTHOR_EMAIL GIT_COMMITTER_NAME GIT_COMMITTER_EMAIL GIT_DIR GIT_WORK_TREE AGI_RULES AGI_TRUNK;export GIT_CONFIG_GLOBAL=/dev/null GIT_CONFIG_SYSTEM=/dev/null
for n in belam1 alive1 sm1 dg1 dg1b dg2 atk;do ssh-keygen -qN "" -ted25519 -f$D/k/$n -C $n>/dev/null;done
pk(){ cut -d' ' -f1,2 $D/k/$1.pub;}
: >$D/over;for n in belam1 alive1 sm1 dg1 dg2 atk;do p=${n%[0-9]};echo "$p@agi namespaces=\"git\" $(pk $n)">>$D/over;done   # OVER-PERMISSIVE: every key made
git init -q $D/r;echo $G/objects>$D/r/.git/objects/info/alternates;cd $D/r;export PATH=$D/b:$PATH
GEO=.agi/nodes/.geometry;RG=$GEO/ring
printf -- '---\n---\n  - {"name": "belam", "parent": "owner"}\n  - {"name": "council", "parent": "belam"}\n  - {"name": "keep", "parent": "belam"}\n  - {"name": "alive", "parent": "council"}\n  - {"name": "sm", "parent": "keep"}\n  - {"name": "dg1", "parent": "sm"}\n  - {"name": "dg2", "parent": "sm"}\n  - {"name": "dg9", "parent": "sm"}\n'>$D/posts.md
printf 'belam %s\nalive %s\nsm %s\ndg1 %s\ndg2 %s\n' "$(pk belam1)" "$(pk alive1)" "$(pk sm1)" "$(pk dg1)" "$(pk dg2)">$D/ring
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
# --- D1: the ring deleted by a merge that is TREESAME to the pre-ring parent
M=$(mkm $R1 $P0 $P0 dg1);gate $R1 $M;ok "d1a-treesame-merge-dg1-refused a merge of R1 (P0 + the ring only) and P0 (its tree IS the pre-ring parent's: a combined diff shows NO change) signed by dg1 deletes the ring: refused" 'refused'
M=$(mkm $R1 $P0 $P0 sm1);gate $R1 $M;ok "d1b-treesame-merge-sm-refused the same merge signed by sm (above dg1, NOT above belam or alive, whose lines it removes): refused" 'refused'
M=$(env GIT_COMMITTER_NAME=u GIT_COMMITTER_EMAIL=u@agi GIT_AUTHOR_NAME=u GIT_AUTHOR_EMAIL=u@agi git commit-tree -m merge -p $R1 -p $P0 $(git rev-parse $P0^{tree}));gate $R1 $M;ok "d1c-treesame-merge-unsigned-refused the same merge UNSIGNED: refused" 'refused'
git show $o:.agi/nodes/moral/antifragility.md>$D/af;echo 'plain-edit'>>$D/af;S=$(mkc $R dg1 .agi/nodes/moral/antifragility.md:$D/af);MG=$(mkm $R $S $S dg1);gate $R $MG;ok "d1d-merge-keeping-ring-admitted control: a dg1-signed merge of R and a dg1 edit of an unringed node (the ring untouched) is admitted" '[ $r = 0 ]'
M=$(mkm $R1 $P0 $P0 belam1);gate $R1 $M;ok "d1e-treesame-merge-belam-admitted control: the same merge signed by belam (ancestor-or-self of every line it removes) is admitted [$(tail -2 $D/out|tr '\n' ' '|cut -c1-120)]" '[ $r = 0 ]'
mku $R .agi/nodes/moral/antifragility.md:$D/af>$D/u2;gate $R $(cat $D/u2);ok "d1k-unsigned-under-a-ring-refused an UNSIGNED commit (the edit of an unringed node d1d admits when dg1 signs it) under a trunk that holds a ring is refused (no ring signer, no landing)" 'refused'
# bootstrap stays closed: the ring existed in this history, then belam (above every line) deleted it; no ring at the tip now
x=$D/i;GIT_INDEX_FILE=$x git read-tree $R;GIT_INDEX_FILE=$x git update-index --force-remove $RG;DEL=$(env GIT_COMMITTER_NAME=belam GIT_COMMITTER_EMAIL=belam@agi GIT_AUTHOR_NAME=belam GIT_AUTHOR_EMAIL=belam@agi git -c gpg.format=ssh -c user.signingkey=$D/k/belam1 commit-tree -S -p $R -m del $(GIT_INDEX_FILE=$x git write-tree));rm -f $x;gate $R $DEL;ok "d1f-owner-deletion-answers-to-every-name belam (ancestor-or-self of every line the deletion removes) deleting the whole ring in a plain commit is admitted (the control: d1a-d1c refuse for WHO signs)" '[ $r = 0 ]'
mku $DEL $RG:$D/ring>$D/t1;gate $DEL $(cat $D/t1);ok "d1g-bootstrap-closed-unsigned an UNSIGNED commit adding a ring on top of the deletion is refused (the ring existed in this history: no bootstrap)" 'refused'
gate $DEL $(mkc $DEL atk $RG:$D/ring);ok "d1h-bootstrap-closed-any-key a commit signed by ANY key the box lists (AGI_ALLOWED over-permissive) adding a ring on top of the deletion is refused" 'refused'
EMP=$(mkc $R belam1 $RG:/dev/null);gate $R $EMP;ok "d1i-emptied-ring-answers-too belam EMPTYING the ring (not deleting it) is admitted; the ring existed" '[ $r = 0 ]'
EMP2=$(mkc $R dg1 $RG:/dev/null);gate $R $EMP2;ok "d1j-emptied-by-dg1-refused dg1 emptying the ring is refused (it removes belam's line)" 'refused'
# --- D2: a non-canonical ring line, signed by dg1 (a ring signer that is NOT above belam)
for c in "sp: belam ssh-ed25519 $(echo $ATK|cut -d' ' -f2)\n" "tab:belam\tssh-ed25519\t$(echo $ATK|cut -d' ' -f2)\n" "tail:belam ssh-ed25519 $(echo $ATK|cut -d' ' -f2) extra\n" "upper:Belam ssh-ed25519 $(echo $ATK|cut -d' ' -f2)\n" "cr:belam ssh-ed25519 $(echo $ATK|cut -d' ' -f2)\r\n" "rsa:belam ssh-rsa $(echo $ATK|cut -d' ' -f2)\n" "opts:belam namespaces=\"git\" ssh-ed25519 $(echo $ATK|cut -d' ' -f2)\n" "own-tail:dg1 ssh-ed25519 $(echo $ATK|cut -d' ' -f2) belam@agi\n";do
 n=${c%%:*};l=${c#*:};[ $n = sp ]&&l=" belam ssh-ed25519 $(echo $ATK|cut -d' ' -f2)\n";ringadd $R "$l";gate $R $(mkc $R dg1 $RG:$D/e);ok "d2-$n-refused dg1 adds a ring line off shape ($n): refused, never read as a name" 'refused';done
ringadd $R "belam ssh-ed25519 $(echo $ATK|cut -d' ' -f2)\n";gate $R $(mkc $R dg1 $RG:$D/e);ok "d2-canonical-belam-refused-by-ruling dg1 adds a CANONICAL line under belam's name (an attacker key): refused by the ring's ruling" 'refused'
ringadd $R "dg1 ssh-ed25519 $(echo $ATK|cut -d' ' -f2)\n";gate $R $(mkc $R dg1 $RG:$D/e);ok "d2-canonical-own-admitted control: dg1 adds a CANONICAL second line of ITS OWN: admitted" '[ $r = 0 ]'
edit $R $RG "s|^dg2 .*|dg2 ssh-ed25519 $(echo $ATK|cut -d' ' -f2) x|";gate $R $(mkc $R dg1 $RG:$D/e);ok "d2-replace-sibling-off-shape-refused dg1 REPLACES dg2's line with an off-shape one (a sibling's line, a trailing field): refused" 'refused'
# --- D3: a posts.md name off [a-z][a-z0-9-]* (sm moves rows in its own subtree)
pr(){ { sh_ $R $GEO/posts.md;printf "$1";}>$D/e;}
pr '  - {"name": "dg9\\nbelam", "parent": "sm"}\n';gate $R $(mkc $R sm1 $GEO/posts.md:$D/e);ok "d3a-newline-name-refused sm adds a posts.md row whose name holds a newline: refused" 'refused'
pr '  - {"name": "dg 9", "parent": "sm"}\n';gate $R $(mkc $R sm1 $GEO/posts.md:$D/e);ok "d3b-space-name-refused a name with a space: refused" 'refused'
pr '  - {"name": "Dg9x", "parent": "sm"}\n';gate $R $(mkc $R sm1 $GEO/posts.md:$D/e);ok "d3c-upper-name-refused a name with upper case: refused" 'refused'
pr '  - {"name": "dgq", "parent": "sm\\nbelam"}\n';gate $R $(mkc $R sm1 $GEO/posts.md:$D/e);ok "d3d-newline-parent-refused a row whose PARENT holds a newline (it would name belam as a second parent): refused" 'refused'
pr '  - {"name": "dg10", "parent": "sm"\n';gate $R $(mkc $R sm1 $GEO/posts.md:$D/e);ok "d3e-garbled-tree-refused a posts.md row that is not JSON: refused (fail closed)" 'refused'
pr '  - {"name": "dg10", "parent": "sm"}\n';gate $R $(mkc $R sm1 $GEO/posts.md:$D/e);ok "d3f-canonical-row-admitted control: sm adds a canonical row under itself: admitted" '[ $r = 0 ]'
pr '  - {"name": "dg10", "parent": "sm"}\n';gate $R $(mkc $R dg1 $GEO/posts.md:$D/e);ok "d3g-sibling-adds-under-sm-refused control: dg1 adds a row under sm (dg1 is not sm): refused by the ruling" 'refused'
# --- R5: the FIRST ring (base = the trunk with NO ring, in no history)
gate $o $(mkc $o dg1 $RG:$D/ring);ok "r5a-first-ring-signed-admitted a SIGNED single-file canonical first ring on a trunk that never had one: admitted (the bootstrap)" '[ $r = 0 ]'
mku $o $RG:$D/ring>$D/u1;gate $o $(cat $D/u1);ok "r5b-first-ring-unsigned-refused the same ring in an UNSIGNED commit: refused" 'refused'
gate $o $(mkc $o dg1 $RG/dg1:$D/ring);ok "r5c-first-ring-directory-refused the first ring as a DIRECTORY (ring/dg1): refused (the ring is one file)" 'refused'
printf 'belam %s extra\n' "$(pk belam1)">$D/bad;gate $o $(mkc $o dg1 $RG:$D/bad);ok "r5d-first-ring-off-shape-refused a signed first ring with an off-shape line: refused" 'refused'
# --- RING.4 (mur sm18 demoted RING.3 952787f32 on four bypasses; SM 05:43Z, DG1 05:44Z): each lane beside an admitted control
# (1) a merge whose FIRST parent is IN the push and whose tree IS an old parent's (P0, the ring-less tree): a gate that diffs only the parents OUTSIDE the push never sees the ring go; an octopus the same
git show $o:.agi/nodes/moral/antifragility.md>$D/af;echo 'plain-edit'>>$D/af;S1=$(mkc $R1 dg1 .agi/nodes/moral/antifragility.md:$D/af);echo 'second-edit'>>$D/af;S2=$(mkc $R1 dg2 .agi/nodes/moral/antifragility.md:$D/af)
gate $R1 $S1;ok "g1a-control-plain-push dg1's edit of an unringed node alone is admitted (the push the merge rides on)" '[ $r = 0 ]'
M=$(mkm $S1 $P0 $P0 dg1);gate $R1 $M;ok "g1b-first-parent-in-push-refused a merge of S1 (IN the push) and P0 whose tree is P0's (the ring deleted) signed by dg1: refused" 'refused'
M=$(env GIT_COMMITTER_NAME=dg1 GIT_COMMITTER_EMAIL=dg1@agi GIT_AUTHOR_NAME=dg1 GIT_AUTHOR_EMAIL=dg1@agi git -c gpg.format=ssh -c user.signingkey=$D/k/dg1 commit-tree -S -p $S1 -p $S2 -p $P0 -m octo $(git rev-parse $P0^{tree}));gate $R1 $M;ok "g1c-octopus-refused an OCTOPUS of S1, S2 (both IN the push) and P0 with P0's tree: refused" 'refused'
M=$(mkm $S1 $S2 $S1 dg1);gate $R1 $M;ok "g1d-control-merge-keeping-ring an in-push merge of S1 and S2 (both signed, both IN the push) that KEEPS the ring (its tree is S1's) signed by dg1 is admitted" '[ $r = 0 ]'
# (2) an ORPHAN root (no ring in ITS history) signed by a ring line, then an UNSIGNED merge of it and the receiving tip whose tree is the orphan's: the bootstrap must open only for a ring path with no history on the RECEIVING tip's ancestry
echo orphan>$D/or;x=$D/i;GIT_INDEX_FILE=$x git read-tree --empty;GIT_INDEX_FILE=$x git update-index --add --cacheinfo 100644,$(git hash-object -w $D/or),zz-orphan.txt;C1=$(GIT_INDEX_FILE=$x git write-tree);rm -f $x
C1=$(env GIT_COMMITTER_NAME=belam GIT_COMMITTER_EMAIL=belam@agi GIT_AUTHOR_NAME=belam GIT_AUTHOR_EMAIL=belam@agi git -c gpg.format=ssh -c user.signingkey=$D/k/belam1 commit-tree -S -m orphan $C1)
M=$(env GIT_COMMITTER_NAME=u GIT_COMMITTER_EMAIL=u@agi GIT_AUTHOR_NAME=u GIT_AUTHOR_EMAIL=u@agi git commit-tree -p $C1 -p $R1 -m um $(git rev-parse $C1^{tree}));gate $R1 $M;ok "g2a-orphan-then-unsigned-merge-refused a ring-signed (by BELAM: a ring line open at the tip) ORPHAN root, then an UNSIGNED merge of it and the receiving tip whose tree is the orphan's (the ring deleted): refused (the bootstrap does not reopen from the push's own history)" 'refused'
gate $R1 $C1;ok "g2b-orphan-root-alone the ring-signed orphan root ALONE (a tree with one innocuous file) is not what is refused: rc $r (the lane above is the verdict; this one records whether the root itself lands)" 'true'
# (3) a posts.md name or parent with a TRAILING LF: jq's \$ matches before it, and the ancestor map is poisoned
pr '  - {"name": "x\\n", "parent": "sm"}\n';gate $R $(mkc $R sm1 $GEO/posts.md:$D/e);ok "g3a-trailing-lf-name-refused sm adds a row whose name is x + LF: refused" 'refused'
pr '  - {"name": "dg10", "parent": "sm\\n"}\n';gate $R $(mkc $R sm1 $GEO/posts.md:$D/e);ok "g3b-trailing-lf-parent-refused a row whose PARENT is sm + LF: refused" 'refused'
pr '  - {"name": "dg10", "parent": "sm"}\n';gate $R $(mkc $R sm1 $GEO/posts.md:$D/e);ok "g3c-control-canonical-row sm adds a canonical row: admitted" '[ $r = 0 ]'
# (4) a ring with a NUL byte (own line, or NUL-separated whole): a binary ring matches no shape and locks the owner out
ringadd $R "dg1 ssh-ed25519 $(echo $ATK|cut -d' ' -f2)\000\n";gate $R $(mkc $R dg1 $RG:$D/e);ok "g4a-nul-in-own-line-refused dg1 adds a line of its own with a NUL byte: refused" 'refused'
{ sh_ $R $RG|tr '\n' '\000';}>$D/e;gate $R $(mkc $R belam1 $RG:$D/e);ok "g4b-nul-separated-ring-refused the whole ring NUL-separated, even signed by belam: refused (it would parse as no line: nobody could sign)" 'refused'
ringadd $R "dg1 ssh-ed25519 $(echo $ATK|cut -d' ' -f2)\n";gate $R $(mkc $R dg1 $RG:$D/e);ok "g4c-control-clean-own-line dg1 adds a clean second line of its own: admitted" '[ $r = 0 ]'
# (5) .gitattributes 'ring -diff' LANDED earlier: in a BARE repo (the land gate's) git reads attributes from the receiving HEAD's tree, so a text diff of the ring prints 'Binary files differ' and names no line
printf '%s -diff\n' $RG>$D/ga;git init -q --bare $D/rb;echo $D/r/.git/objects>$D/rb/objects/info/alternates;git --git-dir=$D/rb symbolic-ref HEAD refs/heads/trunk
gate2(){ git --git-dir=$D/rb update-ref refs/heads/trunk $1;echo "$1 $2 refs/heads/x"|GIT_DIR=$D/rb AGI_ALLOWED=$D/over AGI_TRUNK=refs/heads/trunk AGI_NOT=$1 timeout 60 grow-gate>$D/out 2>&1;r=$?;}
RA=$(mkc $R1 dg1 .gitattributes:$D/ga)   # the SETUP push is built WITHOUT the gate (a gate that rules .gitattributes by the owner refuses dg1 landing it: DG3 06:4xZ); g5b / g5c keep RA as a bare tip
edit $RA $RG "s|^dg2 .*|dg2 ssh-ed25519 $(echo $ATK|cut -d' ' -f2)|";gate2 $RA $(mkc $RA dg1 $RG:$D/e);ok "g5b-ring-diff-blind-refused with that attribute in force dg1 replaces dg2's line (a sibling's) with an attacker key: refused (the ruler reads the ring as text, whatever its attributes)" 'refused'
edit $RA $RG "s|^dg1 .*|dg1 ssh-ed25519 $(pk dg1b|cut -d' ' -f2)|";gate2 $RA $(mkc $RA dg1 $RG:$D/e);ok "g5c-control-own-line-under-attribute with the attribute in force dg1 replaces ITS OWN line: admitted" '[ $r = 0 ]'
echo "grow-gate-ring3: $f FAIL"
exit $f
