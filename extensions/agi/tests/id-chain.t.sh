#!/bin/sh
# id-chain.t.sh [ROOT]: goal:g7.16.1.11.46.19 (V1a) falsifier 1: `agi-id check refs/id/<mint>` (the leaf's 'id check', renamed off /usr/bin/id) walks an identity chain and names the FIRST bad link: a swap of every piece but slot passes; a link signed by a foreign key fails by name; a self-signed birth (an unlisted key) fails by name; each lane has its MUTANT read RED.
# sh + git + ssh-keygen + python3 on a scratch repo with scratch keys and a SCRATCH root signer (allowed-signers with valid-after); the REAL agi-id piece (sect agi-id engine-grow.md of ROOT); no network, no root, 0 USD. ROOT = the tree whose engine-grow.md carries the piece. exit = the FAIL count.
# Lanes: k1 a birth signed by the root + a version signed by the birth's key, every piece but slot swapped -> ok; k2 the version signed by a FOREIGN key -> BAD link 2 by name; k3 a self-signed birth (its own unlisted key) -> BAD link 1 by name; k4 a slot change -> BAD by name; k5 a path that is no piece -> BAD by name; k6 no key.pub -> BAD; k7 a birth older than the root's valid-after -> BAD link 1; k8 an unread ref / an unread root file -> `id: unread`, rc 1; k9 a three-link chain -> ok, 3 links; mutants m1 (the version's signer check cut) m2 (the birth checked against its own key) m3 (the slot test cut) m4 (the piece test cut) each read RED. RE-CUT 1 (alive [decision] 22:02:20Z): k0 the name agi-id resolves nowhere on the system PATH (mutant: the same check on id -> /usr/bin/id); k5b a directory entry (card/notes) and k6b the tip's key.pub a directory -> BAD 'not a plain file' (m5: the mode test cut); k2b an OpenPGP-signed link with its key in the verifier's keyring -> BAD 'not an SSH signature' (m6: the header test cut); k8c an EMPTY root file -> 'id: unread root signers', rc 1 (m7: the -s test cut). RE-CUT 2 (alive [decision] 22:18:14Z): k2c (the SSH line in a PGP link's message, m8 whole-object grep) + k2d (a second gpgsig header line, m9 any-line header grep); m5b (k6b's own mutant); k5c 'brief card' + k5d 'role ' (m10 the substring test).
R0=${ROOT:-${1:-$(cd "$(dirname "$0")/../../.." && pwd)}};D=$(mktemp -d);trap 'rm -rf "${D:?}"' 0;f=0
unset GIT_DIR GIT_WORK_TREE GIT_INDEX_FILE AGI_TRUNK AGI_ID_PIECES;export GIT_CONFIG_GLOBAL=/dev/null GIT_CONFIG_SYSTEM=/dev/null
ok(){ if eval "$2";then echo "ok $1";else echo "FAIL $1 [$(cat $D/out 2>/dev/null|cut -c1-120)]";f=$((f+1));fi;}
sect(){ awk -v n="$1" '$0~"^### "n" "{h=1;next}h&&/^~~~/{if(z)exit;z=1;next}h&&z' $R0/.agi/nodes/.geometry/$2;}
sect agi-id engine-grow.md>$D/id;[ -s $D/id ]||{ echo "FAIL inputs: no agi-id piece in $R0's engine-grow.md";exit 99;}
mkdir $D/k;for u in root a b c evil;do ssh-keygen -q -t ed25519 -N '' -f $D/k/$u -C $u>/dev/null;done
echo "root namespaces=\"git\",valid-after=\"20260101\" $(cut -d' ' -f1,2 $D/k/root.pub)">$D/root
G=$D/r;git init -q --bare $G;git -C $G config core.hooksPath /dev/null
# LINK KEY PARENT DATE PIECE=VALUE...: a commit whose tree is the pieces (key.pub=@<name> reads that public key), signed by KEY; prints its sha
LINK(){ k=$1;p=$2;dt=$3;shift 3;: >$D/ix;rm -f $D/ix;for kv;do n=${kv%%=*};v=${kv#*=};case $v in @*)b=$(git -C $G hash-object -w $D/k/${v#@}.pub);;*)b=$(printf '%s\n' "$v"|git -C $G hash-object -w --stdin);;esac;GIT_INDEX_FILE=$D/ix git -C $G update-index --add --cacheinfo 100644,$b,$n;done
 tr=$(GIT_INDEX_FILE=$D/ix git -C $G write-tree);echo link|GIT_COMMITTER_DATE="$dt" GIT_AUTHOR_DATE="$dt" git -C $G -c user.name=id -c user.email=id@agi -c gpg.format=ssh -c user.signingkey=$D/k/$k commit-tree -S ${p:+-p $p} $tr;}
NOW="2026-10-31T12:00:00Z"
B1(){ LINK root "" "$NOW" key.pub=@a role=director harness=claude model=opus brief=b1 card=c1 perms=p1 slot=dg2 cred=k1;}
ID(){ (cd $G&&sh ${MP:-$D/id} check "$1" ${2-$D/root})>$D/out 2>&1;}
MUT(){ python3 -I -c 'import sys;s=open(sys.argv[1]).read();a,b=sys.argv[2],sys.argv[3];assert s.count(a)==1,a;open(sys.argv[4],"w").write(s.replace(a,b))' $D/id "$1" "$2" $D/mut||{ echo "FAIL inputs: mutant text not found once: $1";exit 99;};}

# k1 a swap of every piece but slot passes
b=$(B1);v=$(LINK a $b "$NOW" key.pub=@b role=reviewer harness=pi model=sonnet brief=b2 card=c2 perms=p2 slot=dg2 cred=k2);git -C $G update-ref refs/id/m1 $v;ID refs/id/m1;r=$?
ok "k1-swap-all-but-slot-passes birth signed by the root, version signed by the birth's key with every piece but slot swapped: rc $r, '$(cat $D/out)'" '[ $r = 0 ]&&grep -qx "id: ok refs/id/m1 2 link(s)" $D/out'
# k2 a link signed by a foreign key fails by name
v=$(LINK evil $b "$NOW" key.pub=@b role=director slot=dg2);git -C $G update-ref refs/id/m2 $v;ID refs/id/m2;r=$?
ok "k2-foreign-key-fails-by-name the version signed by a key that is not link 1's: rc $r, names link 2 and the reason" '[ $r = 1 ]&&grep -q "^id: BAD refs/id/m2 link 2 [0-9a-f]\{12\}: not signed by link 1.s key.pub$" $D/out'
MUT 'b "not signed by link $((i-1))'"'"'s key.pub";}' ':;}';MP=$D/mut ID refs/id/m2;r=$?;MP=
ok "m1-signer-check-cut-RED the mutant that skips the version's signer check passes the foreign link (rc $r): the k2 lane catches it" '[ $r = 0 ]'
# k3 a self-signed birth (an unlisted key) fails by name
s=$(LINK a "" "$NOW" key.pub=@a role=director slot=dg2);git -C $G update-ref refs/id/m3 $s;ID refs/id/m3;r=$?
ok "k3-self-signed-birth-fails-by-name a birth signed by its own key a (not in the root file): rc $r, names link 1 and the reason" '[ $r = 1 ]&&grep -q "^id: BAD refs/id/m3 link 1 [0-9a-f]\{12\}: the birth is not signed by a root signer$" $D/out'
MUT 'sed -E '"'"'s/^[^ #][^ ]* /* /'"'"' $t/root>$t/a' '{ printf '"'"'* namespaces="git" '"'"';git show $(echo $L|cut -d" " -f1):key.pub|cut -d" " -f1,2;}>$t/a';MP=$D/mut ID refs/id/m3;r=$?;MP=
ok "m2-birth-checked-against-its-own-key-RED the mutant that trusts the birth's own key.pub passes the self-signed birth (rc $r): the k3 lane catches it" '[ $r = 0 ]'
# k4 a slot change is a new identity, never a version
v=$(LINK a $b "$NOW" key.pub=@b role=director slot=other);git -C $G update-ref refs/id/m4 $v;ID refs/id/m4;r=$?
ok "k4-slot-change-fails-by-name a version that changes slot: rc $r, names the slot change" '[ $r = 1 ]&&grep -q "link 2 [0-9a-f]\{12\}: the slot changed (dg2 -> other)" $D/out'
MUT '[ "$s" = "$sl" ]||b' 'true||b';MP=$D/mut ID refs/id/m4;r=$?;MP=
ok "m3-slot-test-cut-RED the mutant without the slot test passes the slot change (rc $r): the k4 lane catches it" '[ $r = 0 ]'
# k5 a path that is no piece; k6 no key.pub
v=$(LINK a $b "$NOW" key.pub=@b slot=dg2 notes=x);git -C $G update-ref refs/id/m5 $v;ID refs/id/m5;r=$?
ok "k5-non-piece-path-fails-by-name a version holding 'notes': rc $r, names it" '[ $r = 1 ]&&grep -q "link 2 [0-9a-f]\{12\}: '"'"'notes'"'"' is not an allowed piece" $D/out'
MUT '[ "$w" ]||b' 'true||b';MP=$D/mut ID refs/id/m5;r=$?;MP=
ok "m4-piece-test-cut-RED the mutant without the piece test passes 'notes' (rc $r): the k5 lane catches it" '[ $r = 0 ]'
v=$(LINK a $b "$NOW" role=director slot=dg2);git -C $G update-ref refs/id/m6 $v;ID refs/id/m6;r=$?
ok "k6-no-key-pub-fails a version without key.pub: rc $r, named" '[ $r = 1 ]&&grep -q "link 2 [0-9a-f]\{12\}: no key.pub" $D/out'
# k7 the root's valid-after binds the birth
o=$(LINK root "" "2025-06-01T12:00:00Z" key.pub=@a slot=dg2);git -C $G update-ref refs/id/m7 $o;ID refs/id/m7;r=$?
ok "k7-birth-before-valid-after-fails a birth dated before the root's valid-after (20260101): rc $r, names link 1" '[ $r = 1 ]&&grep -q "link 1 [0-9a-f]\{12\}: the birth is not signed by a root signer" $D/out'
# k8 unread
ID refs/id/none;r=$?;ok "k8-unread-ref a ref that does not exist: 'id: unread refs/id/none', rc $r" '[ $r = 1 ]&&grep -qx "id: unread refs/id/none" $D/out'
ID refs/id/m1 $D/no-such-file;r=$?;ok "k8b-unread-root an unreadable root file: 'id: unread root signers ...', rc $r" '[ $r = 1 ]&&grep -q "^id: unread root signers" $D/out'
# k9 a three-link chain
v2=$(LINK a $b "$NOW" key.pub=@b slot=dg2 role=director);v3=$(LINK b $v2 "$NOW" key.pub=@c slot=dg2 role=reviewer);git -C $G update-ref refs/id/m9 $v3;ID refs/id/m9;r=$?
ok "k9-three-links-ok root -> a -> b -> c: rc $r, 3 links" '[ $r = 0 ]&&grep -qx "id: ok refs/id/m9 3 link(s)" $D/out'
v3x=$(LINK a $v2 "$NOW" key.pub=@c slot=dg2);git -C $G update-ref refs/id/m9x $v3x;ID refs/id/m9x;r=$?
ok "k9b-third-link-signed-by-the-grandparent-key link 3 signed by a (link 1's key, not link 2's b): rc $r, BAD link 3" '[ $r = 1 ]&&grep -q "link 3 [0-9a-f]\{12\}: not signed by link 2.s key.pub" $D/out'
# --- RE-CUT 1 (alive [decision] 22:02:20Z 10-31)
# k0 the name: agi-id resolves nowhere on the system PATH (id does: /usr/bin/id, which agi-gate's root drop calls)
x=$(PATH=/usr/sbin:/usr/bin:/sbin:/bin command -v agi-id);ok "k0-the-name-shadows-nothing 'agi-id' on PATH=/usr/sbin:/usr/bin:/sbin:/bin resolves to '${x:-nothing}'" '[ -z "$x" ]'
x=$(PATH=/usr/sbin:/usr/bin:/sbin:/bin command -v id);ok "m-k0-the-old-name-RED the same check on the name 'id' resolves to '$x': the k0 lane catches it" '[ -n "$x" ]'
# (1) every tree entry a plain file: k5b card/ a directory holding notes; k6b the tip's key.pub a directory
v=$(LINK a $b "$NOW" key.pub=@b slot=dg2 card/notes=x);git -C $G update-ref refs/id/m5b $v;ID refs/id/m5b;r=$?
ok "k5b-directory-entry-fails-by-name link 2 carries card/ as a DIRECTORY holding notes: rc $r, names 'card' as not a plain file" '[ $r = 1 ]&&grep -q "link 2 [0-9a-f]\{12\}: '"'"'card'"'"' is not a plain file (040000 tree)" $D/out'
v=$(LINK a $b "$NOW" key.pub/x=@b slot=dg2);git -C $G update-ref refs/id/m6b $v;ID refs/id/m6b;r=$?
ok "k6b-tip-key-pub-a-directory-fails the TIP's key.pub is a directory: rc $r, names it" '[ $r = 1 ]&&grep -q "link 2 [0-9a-f]\{12\}: '"'"'key.pub'"'"' is not a plain file (040000 tree)" $D/out'
MUT '[ "$m $ty" = "100644 blob" ]||b' 'true||b';MP=$D/mut ID refs/id/m5b;r1=$?;MP=$D/mut ID refs/id/m6b;r2=$?;MP=
ok "m5-mode-test-cut-RED the mutant reading names only passes card/ ($r1) or fails it only by luck, and lets the directory key.pub through to a later test ($r2, '$(cut -c1-60 $D/out)'): the k5b/k6b lanes catch it" '[ $r1 = 0 ]&&! grep -q "not a plain file" $D/out'
# (2) the backend pinned to ssh: link 2 signed by an OpenPGP key that IS in the verifier's keyring
if command -v gpg>/dev/null;then export GNUPGHOME=$D/g;mkdir -m 700 $GNUPGHOME;gpg --batch -q --passphrase '' --quick-gen-key 'pgp <pgp@agi>' ed25519 sign never 2>/dev/null
 : >$D/ix;rm -f $D/ix;for kv in key.pub=@b slot=dg2;do n=${kv%%=*};w=${kv#*=};case $w in @*)o=$(git -C $G hash-object -w $D/k/${w#@}.pub);;*)o=$(printf '%s\n' "$w"|git -C $G hash-object -w --stdin);;esac;GIT_INDEX_FILE=$D/ix git -C $G update-index --add --cacheinfo 100644,$o,$n;done
 v=$(echo link|git -C $G -c user.name=id -c user.email=pgp@agi -c gpg.format=openpgp -c user.signingkey=pgp@agi commit-tree -S -p $b $(GIT_INDEX_FILE=$D/ix git -C $G write-tree));git -C $G update-ref refs/id/m2b $v
 git -C $G verify-commit $v>/dev/null 2>&1;kr=$?;ID refs/id/m2b;r=$?
 ok "k2b-openpgp-signature-fails-by-name link 2 signed by an OpenPGP key in the verifier's keyring (git verify-commit alone: rc $kr): rc $r, names the backend" '[ $kr = 0 ]&&[ $r = 1 ]&&grep -q "link 2 [0-9a-f]\{12\}: not an SSH signature (the backend is pinned to ssh)" $D/out'
 MUT " [ \"\$(git cat-file commit \$c|sed '/^\$/q'|grep '^gpgsig')\" = 'gpgsig -----BEGIN SSH SIGNATURE-----' ]||b \"not an SSH signature (the backend is pinned to ssh)\"" ' :';MP=$D/mut ID refs/id/m2b;r=$?;MP=
 ok "m6-header-test-cut-RED the mutant without the ssh pin passes the OpenPGP link (rc $r): the k2b lane catches it" '[ $r = 0 ]'
 # k2c: a PGP-signed link whose SIGNED MESSAGE holds the SSH line; k2d: k2b's PGP link with ONE extra 'gpgsig -----BEGIN SSH SIGNATURE-----' HEADER line (git hash-object -t commit)
 v=$(printf 'link\n\ngpgsig -----BEGIN SSH SIGNATURE-----\n'|git -C $G -c user.name=id -c user.email=pgp@agi -c gpg.format=openpgp -c user.signingkey=pgp@agi commit-tree -S -p $b $(GIT_INDEX_FILE=$D/ix git -C $G write-tree));git -C $G update-ref refs/id/m2c $v;ID refs/id/m2c;r=$?
 ok "k2c-ssh-line-in-the-message-fails a PGP-signed link whose message holds the SSH line: rc $r, not an SSH signature" '[ $r = 1 ]&&grep -q "link 2 [0-9a-f]\{12\}: not an SSH signature" $D/out'
 MUT " [ \"\$(git cat-file commit \$c|sed '/^\$/q'|grep '^gpgsig')\" = 'gpgsig -----BEGIN SSH SIGNATURE-----' ]||b" " git cat-file commit \$c|grep -qx 'gpgsig -----BEGIN SSH SIGNATURE-----'||b";MP=$D/mut ID refs/id/m2c;r=$?;MP=
 ok "m8-whole-object-grep-RED the mutant grepping the WHOLE object finds the message's line and passes k2c (rc $r): the k2c lane catches it" '[ $r = 0 ]'
 git -C $G cat-file commit $(git -C $G rev-parse refs/id/m2b)|awk 'BEGIN{d=0}!d&&/^$/{print "gpgsig -----BEGIN SSH SIGNATURE-----";d=1}{print}'>$D/c2d;v=$(git -C $G hash-object -t commit -w $D/c2d);git -C $G update-ref refs/id/m2d $v
 ng=$(git -C $G cat-file commit $v|sed '/^$/q'|grep -c '^gpgsig');git -C $G verify-commit $v>/dev/null 2>&1;kr=$?;ID refs/id/m2d;r=$?
 ok "k2d-a-second-gpgsig-header-fails k2b's PGP link + ONE extra SSH gpgsig header line ($ng header lines start gpgsig; plain verify-commit rc $kr): rc $r, not an SSH signature" '[ $ng = 2 ]&&[ $r = 1 ]&&grep -q "link 2 [0-9a-f]\{12\}: not an SSH signature" $D/out'
 MUT " [ \"\$(git cat-file commit \$c|sed '/^\$/q'|grep '^gpgsig')\" = 'gpgsig -----BEGIN SSH SIGNATURE-----' ]||b" " git cat-file commit \$c|sed '/^\$/q'|grep -qx 'gpgsig -----BEGIN SSH SIGNATURE-----'||b";MP=$D/mut ID refs/id/m2d;r=$?;MP=
 ok "m9-header-grep-any-line-RED the mutant accepting ANY header line equal to the SSH line passes k2d (rc $r): the k2d lane catches it" '[ $r = 0 ]'
 gpgconf --kill all 2>/dev/null;unset GNUPGHOME
else echo "FAIL k2b no gpg on this host: the OpenPGP row cannot run";f=$((f+1));fi
# (1) m5b, k6b's OWN mutant: the mode test cut AND key.pub back to 'cat-file -e' -> the directory key.pub reads ok
MUT '[ "$m $ty" = "100644 blob" ]||b' 'true||b';cp $D/mut $D/mut1;python3 -I -c 'import sys;s=open(sys.argv[1]).read();a="[ \"$(git cat-file -t $c:key.pub 2>/dev/null)\" = blob ]||b";assert s.count(a)==1;open(sys.argv[1],"w").write(s.replace(a,"git cat-file -e $c:key.pub 2>/dev/null||b"))' $D/mut1;MP=$D/mut1 ID refs/id/m6b;r=$?;MP=
ok "m5b-mode-and-blob-cut-RED the mutant without the mode test and with key.pub back to cat-file -e reads the directory key.pub ok (rc $r, '$(cat $D/out)'): the k6b lane catches it" '[ $r = 0 ]&&grep -qx "id: ok refs/id/m6b 2 link(s)" $D/out'
# (5) a name equals ONE word of AGI_ID_PIECES, untrimmed: k5c 'brief card' (two words), k5d 'role ' (a trailing space); the entries are written with the name QUOTED and checked in ls-tree first
QL(){ : >$D/ix;rm -f $D/ix;for kv in key.pub=@b slot=dg2;do n=${kv%%=*};w=${kv#*=};case $w in @*)o=$(git -C $G hash-object -w $D/k/${w#@}.pub);;*)o=$(printf '%s\n' "$w"|git -C $G hash-object -w --stdin);;esac;GIT_INDEX_FILE=$D/ix git -C $G update-index --add --cacheinfo 100644,$o,$n;done
 o=$(echo x|git -C $G hash-object -w --stdin);GIT_INDEX_FILE=$D/ix git -C $G update-index --add --cacheinfo "100644,$o,$1";echo link|git -C $G -c user.name=id -c user.email=id@agi -c gpg.format=ssh -c user.signingkey=$D/k/a commit-tree -S -p $b $(GIT_INDEX_FILE=$D/ix git -C $G write-tree);}
v=$(QL 'brief card');git -C $G update-ref refs/id/m5c $v;has=$(git -C $G ls-tree --name-only $v|grep -cx 'brief card');ID refs/id/m5c;r=$?
ok "k5c-two-word-name-fails a link holding the entry 'brief card' (ls-tree shows it: $has): rc $r, named" '[ $has = 1 ]&&[ $r = 1 ]&&grep -q "link 2 [0-9a-f]\{12\}: '"'"'brief card'"'"' is not an allowed piece" $D/out'
v=$(QL 'role ');git -C $G update-ref refs/id/m5d $v;has=$(git -C $G ls-tree --name-only $v|grep -cx 'role ');ID refs/id/m5d;r=$?
ok "k5d-trailing-space-name-fails a link holding the entry 'role ' (ls-tree shows it: $has): rc $r, named untrimmed" '[ $has = 1 ]&&[ $r = 1 ]&&grep -q "link 2 [0-9a-f]\{12\}: '"'"'role '"'"' is not an allowed piece" $D/out'
MUT 'w=;for q in $P;do [ "$x" = "$q" ]&&w=1;done;[ "$w" ]||b' 'case "$P" in *" $x "*);;*)false;;esac||b';MP=$D/mut ID refs/id/m5c;r=$?;MP=
ok "m10-substring-test-RED the mutant matching names as a SUBSTRING of the piece list passes 'brief card' (rc $r): the k5c lane catches it" '[ $r = 0 ]'
# (4) an EMPTY root file reads unread, never BAD on the chain
: >$D/empty;ID refs/id/m1 $D/empty;r=$?
ok "k8c-empty-root-unread a 0-byte root file: 'id: unread root signers ...', rc $r, never a BAD birth" '[ $r = 1 ]&&grep -q "^id: unread root signers" $D/out'
MUT 'fi&&[ -s $t/root ]||{' 'fi||{';MP=$D/mut ID refs/id/m1 $D/empty;r=$?;MP=
ok "m7-empty-test-cut-RED the mutant without the -s test names the birth BAD instead (rc $r, '$(cut -c1-60 $D/out)'): the k8c lane catches it" '[ $r = 1 ]&&grep -q "^id: BAD" $D/out'
echo "id-chain: $f FAIL";exit $f
