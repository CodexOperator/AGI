#!/bin/sh
# grow-gate-keys.t.sh [TRUNK] [GITDIR]: AA2 private-key gate (hypothesis g716111-aa2-the-trunk-refuses-every-node-that-carries-a-private-key-block, falsifiers 1-7 incl. 4b / 4c / 5): the trunk is pushed hourly to a PUBLIC origin, so
# grow-gate refuses EVERY commit that adds or changes ANY path (node, script, payload, binary, deprecated node, a path with spaces; a merge's own changes included) whose bytes hold a private key block, whatever the ring says; it never prints the key
# and never parses one (no ssh-keygen: an encrypted block must refuse inside a timeout, not hang). Scratch repo borrowing GITDIR's objects (0 shared refs written), scratch keys GENERATED AT RUN TIME (4c: this file holds no armoured block;
# every header below is assembled from parts). Tools from TRUNK by sect; GROW_GATE=<file> tests a candidate grow-gate. One ok/FAIL line per case; exit = number of FAILs.
SELF=$(cd "$(dirname "$0")" && pwd)/$(basename "$0");T=${1:-local-maxxing/season2/main};G=${2:-$(git rev-parse --path-format=absolute --git-common-dir)};D=$(mktemp -d);trap 'rm -rf $D' EXIT;mkdir $D/b $D/k $D/f;f=0;CEIL=${CEIL:-5450}
o=$(git rev-parse $T)||exit 1;for x in sect grow-check grow-gate agi-fill;do git ls-tree --full-tree --name-only $o .agi/nodes/.geometry/|grep '/engine[^/]*\.md$'|sed "s|^|$o:|"|git cat-file --batch --follow-symlinks|sed -n "/^###* $x /,/^###* /{/^~~~/,/^~~~/{//!p}}">$D/b/$x;done
[ "$GROW_GATE" ]&&cp $GROW_GATE $D/b/grow-gate;chmod +x $D/b/*;[ -s $D/b/grow-gate ]||{ echo "FAIL no grow-gate at $T";exit 99;}
unset GIT_AUTHOR_NAME GIT_AUTHOR_EMAIL GIT_COMMITTER_NAME GIT_COMMITTER_EMAIL GIT_DIR GIT_WORK_TREE
for p in owner director-general-1;do ssh-keygen -qN "" -ted25519 -f$D/k/$p>/dev/null;echo "$p@agi namespaces=\"git\" $(cut -d' ' -f1,2 $D/k/$p.pub)">>$D/ring;done
git init -q $D/r;echo $G/objects>$D/r/.git/objects/info/alternates;cd $D/r;git update-ref refs/heads/trunk $o;export PATH=$D/b:$PATH
# the valid ADDED node of the ring lane (a moral with a key), and the armour pieces: five dashes, assembled at run time
git show $o:.agi/nodes/moral/antifragility.md|sed 's/^id: moral:antifragility/id: moral:zz-key-lane/;s/^mint_id: .*/mint_id: 0123456789abcdef0123456789abcdef/;s/^type: moral/type: moral\nkey: 2fe50ba43c479d67/'>$D/n
DD=-----;hdr(){ printf '%sBEGIN %sPRIVATE KEY%s\n' $DD "${1:+$1 }" $DD;};ftr(){ printf '%sEND %sPRIVATE KEY%s\n' $DD "${1:+$1 }" $DD;}
body(){ head -c 120 /dev/urandom|base64 -w 64;}
blk(){ hdr "$1";cat;ftr "$1";}   # blk LABEL < body
# real keys at run time: live (in the ring), retired (its ring line CLOSED), unknown (not in the ring), encrypted OpenSSH, and a retired+live pair
for u in live retired unknown encr;do ssh-keygen -qN "$([ $u = encr ]&&echo hunter2)" -ted25519 -C $u -f$D/f/$u>/dev/null;done
echo "live@agi namespaces=\"git\" $(cut -d' ' -f1,2 $D/f/live.pub)">>$D/ring;echo "retired@agi namespaces=\"git\",valid-before=\"20200101000000Z\" $(cut -d' ' -f1,2 $D/f/retired.pub)">>$D/ring
# --- commit builders: mkc "P1[,P2]" path:file ... = a signed commit whose tree is TRUNK + those files (a path:- removes nothing: add only)
mkc(){ ps=$1;shift;x=$D/i;GIT_INDEX_FILE=$x git read-tree $o;for a in "$@";do GIT_INDEX_FILE=$x git update-index --add --cacheinfo 100644,$(git hash-object -w "${a#*:}"),"${a%%:*}";done;tr=$(GIT_INDEX_FILE=$x git write-tree);rm -f $x
 pa=;for q in $(echo $ps|tr , ' ');do pa="$pa -p $q";done
 GIT_COMMITTER_NAME=owner GIT_COMMITTER_EMAIL=owner@agi GIT_AUTHOR_NAME=owner GIT_AUTHOR_EMAIL=owner@agi git -c gpg.format=ssh -c user.signingkey=$D/k/owner commit-tree -S $pa -m k $tr;}
# mkz "P1[,P2]" mode:file:path ... = as mkc, any mode (120000 = a symlink whose target text is the file) and a path with a newline; mode 0 = a blob oid the store LACKS (file only names the text hashed, never written)
mkz(){ ps=$1;shift;x=$D/i;GIT_INDEX_FILE=$x git read-tree $o;for a in "$@";do m=${a%%:*};a=${a#*:};fl=${a%%:*};pt=${a#*:};if [ $m = 0 ];then m=100644;h=$(git hash-object $fl);else h=$(git hash-object -w $fl);fi;printf '%s %s 0\t%s\0' $m $h "$pt"|GIT_INDEX_FILE=$x git update-index -z --index-info;done;tr=$(GIT_INDEX_FILE=$x git write-tree --missing-ok);rm -f $x
 pa=;for q in $(echo $ps|tr , ' ');do pa="$pa -p $q";done
 GIT_COMMITTER_NAME=owner GIT_COMMITTER_EMAIL=owner@agi GIT_AUTHOR_NAME=owner GIT_AUTHOR_EMAIL=owner@agi git -c gpg.format=ssh -c user.signingkey=$D/k/owner commit-tree -S $pa -m k $tr;}
# gate TIP: the receiving trunk is TRUNK; refused = non-zero. Output in $D/out; rc in $r
gate(){ echo "$o $1 refs/heads/x"|AGI_ALLOWED=$D/ring AGI_TRUNK=refs/heads/trunk AGI_NOT=$o timeout ${GT:-60} grow-gate>$D/out 2>&1;r=$?;}
ok(){ if eval "$2";then echo "ok $1";else echo "FAIL $1 [rc=$r $(tail -1 $D/out|cut -c1-80)]";f=$((f+1));fi;}
node(){ cat $D/n;echo;cat;}            # node < text appended: a valid ADDED node carrying that text
refused(){ [ $r != 0 ]&&[ $r != 124 ];}
# --- 4c fixture rule: this file itself holds no armoured block, and neither does the run's own output
hdr OPENSSH>$D/ctl;ok "4c-no-literal-armour this test file holds no matching header line (assembled at run time); the check itself works (a positive control matches)" 'grep -q -e "$DD"BEGIN\ [A-Z0-9\ ]*PRIVATE\ KEY"$DD" $D/ctl&&! grep -q -e "$DD"BEGIN\ [A-Z0-9\ ]*PRIVATE\ KEY"$DD" "$SELF"'
# --- 1: a live, a retired (ring line closed) and an unknown OpenSSH key, each in a NEW node: all refused, the output names the file; the ring is not consulted
for u in live retired unknown;do node <$D/f/$u>$D/nn.$u;done
for u in live retired unknown;do gate $(mkc $o .agi/nodes/moral/zz-key-lane.md:$D/nn.$u);ok "f1-$u-openssh-in-new-node refused, names the file ($u: a closed or unknown ring line does not admit it)" 'refused&&grep -q zz-key-lane $D/out';done
# --- 2: every label
for L in "" RSA EC DSA ENCRYPTED OPENSSH;do body|blk "$L"|node>$D/nl;gate $(mkc $o .agi/nodes/moral/zz-key-lane.md:$D/nl);ok "f2-label-[${L:-bare}] a ${L:-bare} PRIVATE KEY block in a new node is refused" 'refused&&grep -q zz-key-lane $D/out';done
# --- 3: a passphrase-encrypted OpenSSH key is refused INSIDE a timeout (no ssh-keygen -y waiting for a passphrase)
node <$D/f/encr>$D/ne;GT=20 gate $(mkc $o .agi/nodes/moral/zz-key-lane.md:$D/ne);ok "f3-encrypted-openssh-no-hang an encrypted OpenSSH key is refused and the gate returns inside timeout 20 (rc=$r; 124 = a HANG)" 'refused'
# --- 4: a retired AND a live key in ONE node; the same block added to an EXISTING node (CHANGED, not ADDED)
{ cat $D/n;echo;cat $D/f/retired;cat $D/f/live;}>$D/n2;gate $(mkc $o .agi/nodes/moral/zz-key-lane.md:$D/n2);ok "f4-retired-and-live-in-one-node refused" 'refused'
{ git show $o:.agi/nodes/moral/antifragility.md;echo;cat $D/f/unknown;}>$D/ch;gate $(mkc $o .agi/nodes/moral/antifragility.md:$D/ch);ok "f4-changed-existing-node the block ADDED to an existing node (a CHANGED path) is refused" 'refused&&grep -q antifragility $D/out'
# --- 4b: the paths a node loop misses
cp $D/f/unknown $D/plain
gate $(mkc $o extensions/x.sh:$D/plain);ok "f4b-non-node-path a key in extensions/x.sh is refused" 'refused&&grep -q extensions/x.sh $D/out'
gate $(mkc $o ".agi/nodes/deprecated/moral/zz-old.md:$D/nn.unknown");ok "f4b-deprecated-node a key in a DEPRECATED node is refused" 'refused'
gate $(mkc $o ".agi/nodes/.geometry/zz-lane.tsv:$D/plain");ok "f4b-geometry-tsv a key in a .geometry .tsv is refused" 'refused'
{ printf 'bin\000\001\002 junk\n';cat $D/f/unknown;printf '\000tail\377\n';} >$D/bin;gate $(mkc $o extensions/blob.bin:$D/bin);ok "f4b-binary a key INSIDE a binary file (NULs around it) is refused" 'refused'
gate $(mkc $o "extensions/a b/zz key.sh:$D/plain");ok "f4b-path-with-spaces a key in a path with spaces is refused" 'refused&&grep -q "zz key.sh" $D/out'
printf 'benign one\n'>$D/b1;printf 'benign two\n'>$D/b2
p1=$(mkc $o extensions/m1.txt:$D/b1);p2=$(mkc $o extensions/m2.txt:$D/b2)
mm=$(mkc $p1,$p2 extensions/m1.txt:$D/b1 extensions/m2.txt:$D/b2 extensions/evil.sh:$D/plain);gate $mm;ok "f4b-evil-merge a merge whose own tree adds a key file present in NEITHER parent is refused (the parents themselves are clean)" 'refused&&grep -q evil.sh $D/out'
mc=$(mkc $p1,$p2 extensions/m1.txt:$D/b1 extensions/m2.txt:$D/b2);gate $mc;ok "f4b-clean-merge a CLEAN merge of the same two parents passes" '[ $r = 0 ]'
# a public key, an SSH signature block and prose that says private key without the header: all pass
{ cat $D/f/unknown.pub;printf '%sBEGIN SSH SIGNATURE%s\nU1NIU0lH\n%sEND SSH SIGNATURE%s\nthe private key never leaves the post\n' $DD $DD $DD $DD;}>$D/pub;gate $(mkc $o extensions/pub.txt:$D/pub);ok "f4b-public-and-signature-pass a public key, an SSH SIGNATURE block and the words private key (no header) land" '[ $r = 0 ]'
# --- R1/R2 (DG1 rule 04:02Z, option B): the paths and blobs a name-list loop misses
NL=$(printf 'extensions/zz-nl\nkey.sh')
gate $(mkz $o 100644:$D/plain:"$NL");ok "r1-newline-path a key in a file whose PATH holds a newline is refused, the output names the path" 'refused&&grep -q zz-nl $D/out'
gate $(mkz $o 100644:$D/b1:"$NL");ok "r1b-newline-path-clean a clean file at a newline path lands" '[ $r = 0 ]'
gate $(mkz $o 120000:$D/plain:.agi/nodes/moral/antifragility.md);ok "r2-type-change a trunk file REPLACED by a symlink (T) whose target text is the key block is refused, names the path" 'refused&&grep -q antifragility $D/out'
gate $(mkz $o 120000:$D/plain:extensions/zz-new-link);ok "r2a-new-symlink a NEW symlink whose target text is the key block is refused" 'refused&&grep -q zz-new-link $D/out'
printf 'extensions/benign-target\n'>$D/lt;gate $(mkz $o 120000:$D/lt:.agi/nodes/moral/antifragility.md);r2=$r;ok "r2c-type-change-clean a file replaced by a symlink with a benign target is not refused by the key gate (rc=$r2: a node refusal other than the key line may follow)" '! grep -q "private key" $D/out'
head -c 40 /dev/urandom|base64>$D/miss;git cat-file -e $(git hash-object $D/miss) 2>/dev/null&&echo 'fixture: the missing blob exists'>&2
gate $(mkz $o 0:$D/miss:extensions/zz-missing.sh);ok "r2b-unreadable-blob a path whose blob the store cannot read REFUSES (never lands), naming the exact path" 'refused&&grep -q zz-missing $D/out'
gate $(mkz $o 0:$D/miss:"$NL");ok "r2b-unreadable-newline-path an unreadable blob at a newline path refuses too" 'refused&&grep -q zz-nl $D/out'
# --- FAIL CLOSED (DG1 04:40Z): a git error in the commit walk refuses the land, naming the commit; a gate that reads an error as "no changes" is RED here
C=$(mkc $o extensions/fc.txt:$D/b1);t=$(git rev-parse $C^{tree});rm -f $D/r/.git/objects/${t%${t#??}}/${t#??};gate $C;ok "fc-a-diff-tree-fails a commit whose tree object is missing (git diff-tree fails) is REFUSED, rc non-zero, naming the commit" 'refused&&grep -q $C $D/out'
C1=$(mkc $o extensions/fc1.txt:$D/b1);C2=$(mkc $C1 extensions/fc2.txt:$D/b2);rm -f $D/r/.git/objects/${C1%${C1#??}}/${C1#??};gate $C2;ok "fc-b-rev-list-fails a range whose parent commit is unreadable (git rev-list fails) is REFUSED, rc non-zero (an error is not an empty range)" 'refused'
# --- 5: prose that quotes the armour WITH DOTS lands (no key body); the EXACT header quote is refused by design
printf 'the gate refuses a block that starts with %sBEGIN ... PRIVATE KEY%s and nothing else\n' $DD $DD|node>$D/dots;gate $(mkc $o .agi/nodes/moral/zz-key-lane.md:$D/dots);ok "f5-dotted-armour-prose-lands a node quoting the armour with dots in place of the label lands" '[ $r = 0 ]'
printf 'quoted exactly: %s\n' "$(hdr OPENSSH)"|node>$D/exact;gate $(mkc $o .agi/nodes/moral/zz-key-lane.md:$D/exact);ok "f5-exact-header-refused prose that quotes the header EXACTLY (one line, five dashes) is refused, by design" 'refused'
# --- 5b: a plain valid node lands; the public-key lane above covers the rest
node </dev/null>$D/plainnode;gate $(mkc $o .agi/nodes/moral/zz-key-lane.md:$D/plainnode);ok "f5b-valid-node-lands a valid node with no armour lands as today (the ring lane's own case)" '[ $r = 0 ]'
# --- 6: the refusal never prints a slice of the key body
body|blk OPENSSH|node>$D/ns;sl=$(sed -n '/BEGIN/{n;p;q}' $D/ns|cut -c1-24);gate $(mkc $o .agi/nodes/moral/zz-key-lane.md:$D/ns);ok "f6-no-key-in-output the refusal output holds no 24-char slice of the key body ('$(echo $sl|cut -c1-6)...')" 'refused&&[ -n "$sl" ]&&! grep -qF -- "$sl" $D/out'
# --- 7: bytes
sz=$(wc -c<$D/b/grow-gate);ok "f7-bytes grow-gate <= $CEIL B ($sz B; the ring round, DG1 ruling 04:5xZ: bar 4,705 B with the ring build; the key-gate-only bar is 1,851 B)" '[ $sz -le $CEIL ]'
echo "grow-gate-keys: $f FAIL"
exit $f
