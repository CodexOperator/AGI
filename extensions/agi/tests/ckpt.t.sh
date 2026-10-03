#!/bin/sh
# ckpt.t.sh [TRUNK] [GITDIR]: AB (3) the ckpt piece (hypothesis g716111-ab-a-block-holds-only-with-k-current-pairwise-level-adjacent-signers-and-grace-ends-when-the-lowest-block-seals-the-hand-off; AA2.58 L1-L8, AA2.57's T1-T10, AA2.59 H1-H5, AA2.58b B1/B2): a BLOCK = a commit under refs/agi/block/* whose tree is ONLY tip, time, hash, sigs/<post>.<n>;
# `ckpt check` prints "<tip> <time> <block>" for every block that HOLDS: signers current in the ring AT THE BLOCK'S TIP in every algorithm of AGI_SIGN (hybrid = AND), PAIRWISE level-adjacent, >= k (AGI_CKK, default 2) for the lowest level, every parent's tip an ancestor of its tip, the hash named in AGI_HASHES.
# Written from section AB's table (L / T / H / B rows) directly, NOT from run.sh: the piece comes from CKPT=<file>, else `sect ckpt` of the engine pieces of TRUNK (absent today = FAIL by design: RED on a tree without ckpt); the INTEGRATED gate for the T rows (grace, sealing, the retired key, the owner window cert) = GROW_GATE=<file>, else sect grow-gate,
# run with ckpt on PATH and AGI_CKPT set (the ring-gate delta's seam: it calls `ckpt check` and reads the holding tips). The box's AGI_ALLOWED is OVER-PERMISSIVE on purpose (every key made), so only the ring at the receiving tip and the holding blocks can refuse. Scratch repo, scratch keys at run time (no armoured block here), no network, nothing pushed.
# SEAMS pinned: ckpt sign POST KEY TIP TIME prints the signature text (namespace agi-checkpoint) and `ckpt check` runs in the repo that holds the refs; levels come from posts.md rows (a row with a "harness" key counts 1, an inert row 0, owner 0); the ring holds `owner cert-authority <CA>` AND `owner <CA>`. One ok/FAIL line per case; exit = FAIL count.
T=${1:-local-maxxing/season2/main};G=${2:-$(git rev-parse --path-format=absolute --git-common-dir)};SELF=$(cd "$(dirname "$0")" && pwd);D=$(mktemp -d);trap 'rm -rf $D' EXIT;mkdir $D/b $D/k;f=0;GEO=.agi/nodes/.geometry
o=$(git rev-parse $T)||exit 1;for x in ckpt grow-check grow-gate agi-fill;do git ls-tree --full-tree --name-only $o $GEO/|grep '/engine[^/]*\.md$'|sed "s|^|$o:|"|git cat-file --batch --follow-symlinks|sed -n "/^###* $x /,/^###* /{/^~~~/,/^~~~/{//!p}}">$D/b/$x;done
[ "$CKPT" ]&&cp $CKPT $D/b/ckpt;[ "$GROW_GATE" ]&&cp $GROW_GATE $D/b/grow-gate;chmod +x $D/b/*;[ -s $D/b/ckpt ]||{ echo "FAIL no ckpt piece at $T (set CKPT=<file> for a candidate)";exit 99;};[ -s $D/b/grow-gate ]||{ echo "FAIL no grow-gate at $T";exit 99;}
unset GIT_AUTHOR_NAME GIT_AUTHOR_EMAIL GIT_COMMITTER_NAME GIT_COMMITTER_EMAIL GIT_DIR GIT_WORK_TREE AGI_RULES AGI_TRUNK AGI_SIGN AGI_HASHES AGI_CKK;export GIT_CONFIG_GLOBAL=/dev/null GIT_CONFIG_SYSTEM=/dev/null GIT_AUTHOR_NAME=g GIT_AUTHOR_EMAIL=g@g GIT_COMMITTER_NAME=g GIT_COMMITTER_EMAIL=g@g
ok(){ if eval "$2";then echo "ok $1";else echo "FAIL $1 [rc=$r $(tail -1 $D/out 2>/dev/null|cut -c1-80)]";f=$((f+1));fi;}
K=$D/k;for n in ca belam1 belam2 alive1 aio1 sm1 dg1 dg1b dg2;do ssh-keygen -qN "" -ted25519 -f$K/$n -C $n>/dev/null;done;for n in dg1q dg1bq dg2q;do ssh-keygen -qN "" -tecdsa -b256 -f$K/$n -C $n>/dev/null;done
pk(){ cut -d' ' -f1,2 $K/$1.pub;}
git init -q $D/r;echo $G/objects>$D/r/.git/objects/info/alternates;cd $D/r;export PATH=$D/b:$PATH AGI_CKPT=$D/b/ckpt
h='"harness": "x"';mkdir -p $GEO .agi/nodes/doc .agi/context/schemas
printf -- '---\nring: [sm]\n---\n  - {"name": "belam", "parent": "owner", %s}\n  - {"name": "council", "parent": "belam"}\n  - {"name": "keep", "parent": "belam"}\n  - {"name": "alive", "parent": "council", %s}\n  - {"name": "aio", "parent": "council", %s}\n  - {"name": "sm", "parent": "keep", %s}\n  - {"name": "dg1", "parent": "sm", %s}\n  - {"name": "dg2", "parent": "sm", %s}\n' "$h" "$h" "$h" "$h" "$h" "$h">$GEO/posts.md
printf 'owner cert-authority %s\nowner %s\nbelam %s\nalive %s\naio %s\nsm %s\ndg1 %s\ndg2 %s\ndg1 %s\ndg2 %s\nghost %s\nghost2 %s\n' "$(pk ca)" "$(pk ca)" "$(pk belam1)" "$(pk alive1)" "$(pk aio1)" "$(pk sm1)" "$(pk dg1)" "$(pk dg2)" "$(pk dg1q)" "$(pk dg2q)" "$(pk dg2)" "$(pk aio1)">$GEO/ring
git archive $o .agi/context/schemas $GEO/growth.tsv|tar -x;echo s>.agi/context/schemas/s.md;echo d>.agi/nodes/doc/y.md;git add -A;git -c user.name=g -c user.email=g@g -c commit.gpgsign=false commit -qm genesis;R0=$(git rev-parse HEAD)
# --- builders: mkc BASE KEY path:file... = a signed commit on BASE (CD = a backdate); mk NAME TIP TIME [parent-block..] -- post:key... = a block exactly as the section writes it; holds NAME = the block is in `ckpt check`
mkc(){ b=$1;k=$2;shift 2;x=$D/i;GIT_INDEX_FILE=$x git read-tree $b;for a in "$@";do GIT_INDEX_FILE=$x git update-index --add --cacheinfo 100644,$(git hash-object -w "${a#*:}"),"${a%%:*}";done;tr=$(GIT_INDEX_FILE=$x git write-tree);rm -f $x
 pn=${k%%.*};env GIT_COMMITTER_NAME=$pn GIT_COMMITTER_EMAIL=$pn@agi GIT_AUTHOR_NAME=$pn GIT_AUTHOR_EMAIL=$pn@agi ${CD:+"GIT_COMMITTER_DATE=$CD" "GIT_AUTHOR_DATE=$CD"} git -c gpg.format=ssh -c user.signingkey=$K/$k commit-tree -S -p $b -m ab $tr;}
mk(){ nm=$1;x=$(git rev-parse $2);y=$3;shift 3;pp=;while [ "$1" != -- ];do pp="$pp -p $(git rev-parse refs/agi/block/$1)";shift;done;shift;H=${MKH:-sha256};i=$(mktemp);j=0
 for a in "$@";do j=$((j+1));p=${a%%:*};k=${a#*:};b=$(AGI_HASH=$H ckpt sign $p $K/$k $x $y|git hash-object -w --stdin);printf '100644 blob %s\t%s.%s\n' $b $p $j;done>$i
 st=$(git mktree<$i);hb=$(echo "$H $(git archive --format=tar $x|${H}sum|cut -d' ' -f1)"|git hash-object -w --stdin)
 tr=$(printf '100644 blob %s\thash\n040000 tree %s\tsigs\n100644 blob %s\ttime\n100644 blob %s\ttip\n%s' $hb $st $(echo $y|git hash-object -w --stdin) $(echo $x|git hash-object -w --stdin) "$XTRA"|git mktree);rm -f $i
 git update-ref refs/agi/block/$nm $(echo "block $nm"|git commit-tree $tr $pp);}
holds(){ ckpt check 2>/dev/null|grep -q " $(git rev-parse refs/agi/block/$1)\$";}
: >$D/over;for n in belam1 belam2 alive1 aio1 sm1 dg1 dg1b dg2 ca;do for p in belam alive aio sm dg1 dg2 owner;do echo "$p@agi namespaces=\"git\" $(pk $n)">>$D/over;done;done
gate(){ git update-ref refs/heads/trunk $1;echo "$1 $2 refs/heads/x"|AGI_ALLOWED=$D/over AGI_TRUNK=refs/heads/trunk AGI_NOT=$1 timeout 120 grow-gate>$D/out 2>&1;r=$?;}
refused(){ [ $r != 0 ]&&[ $r != 124 ];}
now=$(date +%s)
# --- L1-L8 (the layers: who may seal together; levels belam 1, alive/aio/sm 2, dg1/dg2 3, owner 0)
mk L3 $R0 $now -- dg1:dg1 dg2:dg2;ok "l1-level3-holds DG1 + DG2 (level 3) hold" 'holds L3'
mk L23 $R0 $now L3 -- sm:sm1 dg1:dg1;ok "l2-sm-dg1-seal-l3 SM + DG1 (levels 2 and 3) sealing the level-3 block hold" 'holds L23'
mk L2 $R0 $now L23 -- alive:alive1 aio:aio1 sm:sm1;ok "l3-council-sm-seal-l2 alive + all-is-one + SM (level 2) sealing it hold" 'holds L2'
mk BAD1 $R0 $now -- belam:belam1 dg1:dg1;ok "l4-two-levels-apart-no belam + DG1 (levels 1 and 3) do not hold" '! holds BAD1'
mk L1 $R0 $now L2 -- belam:belam1 alive:alive1;ok "l5-rare-top belam + alive (1 and 2) sealing L2 hold" 'holds L1'
mk L0 $R0 $now L1 -- owner:ca belam:belam1;ok "l6-anchor owner (the CA key itself) + belam hold" 'holds L0'
mk BAD2 $R0 $now -- owner:ca alive:alive1;ok "l7-owner-alive-no owner + alive (levels 0 and 2) do not hold" '! holds BAD2'
mk BAD3 $R0 $now -- dg1:dg1;ok "l8-one-signer-no a single signer under k = 2 does not hold" '! holds BAD3'
mk BAD4 $R0 $now -- dg1:dg1 dg1:dg1;ok "l8b-one-signer-twice one post's key twice is one signer: does not hold" '! holds BAD4'
mk BAD5 $R0 $now -- dg1:dg2 dg2:dg2;ok "l9-wrong-key a block whose 'dg1' signature is dg2's key does not hold" '! holds BAD5'
ok "l10-k-cell-lowers-level3 under AGI_CKK '3:1' a single level-3 signer holds (the cell is read per level)" '(AGI_CKK="3:1";export AGI_CKK;holds BAD3)'
ok "l11-k-cell-raises-level3 under AGI_CKK '3:3' DG1 + DG2 no longer hold" '! (AGI_CKK="3:3";export AGI_CKK;holds L3)'
mk BAD6 $R0 $now -- ghost:dg2 dg1:dg1;ok "l12-no-posts-row-no a signer with a ring line but NO row in the posts tree has no level: the block does not hold" '! holds BAD6'
mk BAD7 $R0 $now -- ghost:dg2 ghost2:aio1;ok "l12b-two-unknown-no two signers that both have NO posts row (an equal, unknown level) do not hold" '! holds BAD7'
for b in BAD1 BAD2 BAD3 BAD4 BAD5 BAD6 BAD7;do git update-ref -d refs/agi/block/$b;done
# --- B1 B2: a block's tree is ONLY tip, time, hash, sigs/<post>.<n>
XTRA=$(printf '100644 blob %s\tevil name\n' $(echo x|git hash-object -w --stdin)) mk BX $R0 $now -- dg1:dg1 dg2:dg2;ok "b1-extra-file a block with one extra file ('evil name') does not hold" '! holds BX';git update-ref -d refs/agi/block/BX
mk BY $R0 $now -- dg1:dg1 dg2:dg2;ok "b2-same-block-clean the same block without it holds" 'holds BY';git update-ref -d refs/agi/block/BY
# --- T1-T8: grace and sealing through the integrated gate; the trunk advances only on admitted commits
E=$D/e;sed "s|^dg1 ssh-ed25519 .*|dg1 $(pk dg1b)|" $GEO/ring>$E.r;H1=$(mkc $R0 dg1 $GEO/ring:$E.r);gate $R0 $H1;ok "t1-handoff-admitted DG1 gen1 hands off to gen2 (a ring line edit signed by the outgoing key)" '[ $r = 0 ]'
git show $R0:.agi/nodes/doc/y.md>$E.y;echo a>>$E.y;P2=$(mkc $H1 dg1 .agi/nodes/doc/y.md:$E.y);gate $H1 $P2;ok "t2-grace-admitted retired DG1 gen1 BEFORE any holding block contains its hand-off is still admitted (grace)" '[ $r = 0 ]'
mk L3b $H1 $now L3 -- dg1:dg1b dg2:dg2;ok "t3-next-block-holds the next level-3 block over the hand-off tip, signed by DG1 gen2 + DG2, holds" 'holds L3b'
mk L3x $H1 $now L3 -- dg1:dg1 dg2:dg2;ok "t4-retired-key-block-no a block over that tip signed by the RETIRED gen1 does not hold" '! holds L3x';git update-ref -d refs/agi/block/L3x
git show $H1:.agi/nodes/doc/y.md>$E.y;echo b>>$E.y;P5=$(mkc $H1 dg1 .agi/nodes/doc/y.md:$E.y);gate $H1 $P5;ok "t5-sealed-refused once the LOWEST block (level 3) seals the hand-off the retired gen1 is refused, at any date" 'refused'
CD="$(date -d '-1 day' -R)";gate $H1 $(mkc $H1 dg1 .agi/nodes/doc/y.md:$E.y);unset CD;ok "t6-backdated-refused the same commit BACKDATED a day is refused" 'refused'
echo c>>$E.y;gate $H1 $(mkc $H1 dg1b .agi/nodes/doc/y.md:$E.y);ok "t7-gen2-admitted DG1 gen2's plain edit is admitted" '[ $r = 0 ]'
mk OLD $R0 $now L3b -- dg1:dg1 dg2:dg2;ok "t8-older-tip-no a block over an OLDER tip than the block it seals does not hold" '! holds OLD';git update-ref -d refs/agi/block/OLD
# --- T9 T10 (and C18/C19): an owner window cert on belam's key; expiry is read at the newest holding block's time
cd $K;for n in x y;do rm -f b$n b$n.pub b$n-cert.pub;cp belam1 b$n;cp belam1.pub b$n.pub;done;ssh-keygen -qs ca -I w-old -n owner@agi -V -3h:-2h -z 31 bx.pub;ssh-keygen -qs ca -I w-now -n owner@agi -V -1m:+30m -z 32 by.pub;cd $D/r
git show $H1:.agi/context/schemas/s.md>$E.s;echo e>>$E.s;CD="$(date -d '-150 min' -R)";gate $H1 $(mkc $H1 bx-cert.pub .agi/context/schemas/s.md:$E.s);unset CD;ok "t9-expired-cert-backdated-refused an owner cert expired before the newest block's time, a commit BACKDATED into its window, is refused" 'refused'
gate $H1 $(mkc $H1 by-cert.pub .agi/context/schemas/s.md:$E.s);ok "t10-valid-cert-admitted an owner cert valid at that time changes a schema (the rules cell = owner) and is admitted" '[ $r = 0 ]'
# t10p (DG1 10:5xZ round gate: a PYTHON-FREE owner-cert expiry read): the same valid-cert push with python and python3 SHIMMED to exit 127 (a box without python): still admitted; the gate may not shell out to python for the cert
mkdir -p $D/nopy;for x in python python3;do printf '#!/bin/sh\necho "shim: $0 not found" >&2\nexit 127\n'>$D/nopy/$x;chmod +x $D/nopy/$x;done
PATH=$D/nopy:$PATH;gate $H1 $(mkc $H1 by-cert.pub .agi/context/schemas/s.md:$E.s);PATH=${PATH#$D/nopy:};ok "t10p-valid-cert-admitted-without-python the valid owner cert push with python and python3 absent from PATH (shimmed to exit 127): admitted (the cert read is python-free)" '[ $r = 0 ]'
# --- H1-H5: the hybrid cell and the hash (blocks over the genesis tip R0; DG1/DG2 hold ed25519 AND ecdsa columns in the ring)
export AGI_SIGN="ED25519 ECDSA"
mk HA $R0 $now -- dg1:dg1 dg2:dg2;ok "h1-hybrid-ed-only-no under a two-column cell the ed25519-only level-3 block does not hold" '! holds HA'
mk HB $R0 $now -- dg1:dg1 dg1:dg1q dg2:dg2 dg2:dg2q;ok "h2-hybrid-both-columns-holds DG1 + DG2 in both columns hold" 'holds HB'
mk HC $R0 $now -- dg1:dg1 dg1:dg1q dg2:dg2;ok "h3-hybrid-missing-column-no DG2 missing its second column does not hold" '! holds HC'
unset AGI_SIGN;MKH=sha512 mk HS $R0 $now -- dg1:dg1 dg2:dg2;ok "h4-sha512-holds a block naming sha512 holds under the default AGI_HASHES" 'holds HS'
ok "h5-hash-not-allowed a block naming sha512 does not hold when AGI_HASHES is sha256 only" '! (AGI_HASHES=sha256;export AGI_HASHES;holds HS)'
MKH=md5 mk HM $R0 $now -- dg1:dg1 dg2:dg2 2>/dev/null;ok "h6-unknown-hash a block naming a hash outside the cell (md5) does not hold" '! holds HM'
echo "ckpt: $f FAIL"
exit $f
