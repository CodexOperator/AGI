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
# t11 (DG1 12:52Z, optional): the grace set's `git rev-list` (the ring changes no holding block contains: --not <holding tips> -- the ring path) FAILS (a git shim): the whole push is refused 'git rev-list failed' (it fails SAFE for a retired signer, but a gen2 edit would be admitted by a gate that ignores the failure)
mkdir -p $D/shg;printf '#!/bin/sh\n[ "$1" = rev-list ]&&case "$*" in *--reverse*);;*--not*geometry/ring*)echo "shim: rev-list failed" >&2;exit 1;;esac\nexec /usr/bin/git "$@"\n'>$D/shg/git;chmod +x $D/shg/git
PATH=$D/shg:$PATH;gate $H1 $(mkc $H1 dg1b .agi/nodes/doc/y.md:$E.y);PATH=${PATH#$D/shg:};ok "t11-grace-rev-list-failure-refused the grace set's git rev-list fails (a shim on the --not ... ring path call only): DG1 gen2's plain edit (current, would otherwise be admitted, t7) is REFUSED 'git rev-list failed' (a failed read is never an empty grace set)" 'refused&&grep -q "rev-list failed" $D/out'
mk OLD $R0 $now L3b -- dg1:dg1 dg2:dg2;ok "t8-older-tip-no a block over an OLDER tip than the block it seals does not hold" '! holds OLD';git update-ref -d refs/agi/block/OLD
# --- T9 T10 (and C18/C19): an owner window cert on belam's key; expiry is read at the newest holding block's time
cd $K;for n in x y;do rm -f b$n b$n.pub b$n-cert.pub;cp belam1 b$n;cp belam1.pub b$n.pub;done;ssh-keygen -qs ca -I w-old -n owner@agi -V -3h:-2h -z 31 bx.pub;ssh-keygen -qs ca -I w-now -n owner@agi -V -1m:+30m -z 32 by.pub;cd $D/r
git show $H1:.agi/context/schemas/s.md>$E.s;echo e>>$E.s;CD="$(date -d '-150 min' -R)";gate $H1 $(mkc $H1 bx-cert.pub .agi/context/schemas/s.md:$E.s);unset CD;ok "t9-expired-cert-backdated-refused an owner cert expired before the newest block's time, a commit BACKDATED into its window, is refused" 'refused'
gate $H1 $(mkc $H1 by-cert.pub .agi/context/schemas/s.md:$E.s);ok "t10-valid-cert-admitted an owner cert valid at that time changes a schema (the rules cell = owner) and is admitted" '[ $r = 0 ]'
# t10p (DG1 10:5xZ round gate: a PYTHON-FREE owner-cert expiry read): the same valid-cert push with python and python3 SHIMMED to exit 127 (a box without python): still admitted; the gate may not shell out to python for the cert
mkdir -p $D/nopy;for x in python python3;do printf '#!/bin/sh\necho "shim: $0 not found" >&2\nexit 127\n'>$D/nopy/$x;chmod +x $D/nopy/$x;done
PATH=$D/nopy:$PATH;gate $H1 $(mkc $H1 by-cert.pub .agi/context/schemas/s.md:$E.s);PATH=${PATH#$D/nopy:};ok "t10p-valid-cert-admitted-without-python the valid owner cert push with python and python3 absent from PATH (shimmed to exit 127): admitted (the cert read is python-free)" '[ $r = 0 ]'
# t10q: the cert is checked AT THE NEWEST HOLDING BLOCK'S TIME (git itself verified it at the commit date): ONE holding block, time = now - 150 min; the cert by is valid [-1m, +30m], i.e. valid NOW and at the commit date but NOT YET valid at the block's time: refused. A gate that verifies at the wall clock (no -Overify-time) admits it
git for-each-ref --format='%(objectname) %(refname)' refs/agi/block>$D/blk.save;while read ob rf;do git update-ref -d $rf;done<$D/blk.save
mk BQ $R0 $((now-9000)) -- dg1:dg1 dg2:dg2;gate $H1 $(mkc $H1 by-cert.pub .agi/context/schemas/s.md:$E.s);rq=$r;git update-ref -d refs/agi/block/BQ;while read ob rf;do git update-ref $rf $ob;done<$D/blk.save
r=$rq;ok "t10q-cert-not-yet-valid-at-block-time-refused an owner cert valid NOW (and at the commit date) but NOT YET valid at the newest holding block's time (now - 150 min) is refused: the cert is read at the block's time, never the wall clock" 'refused'
# t10r (DG1 13:09Z): TWO holding blocks at DIFFERENT times (the old L-chain blocks at now, BO at now - 150 min): the cert bx is valid [-3h, -2h]: valid at the OLDER block's time, expired at the NEWER one: a commit dated -150 min (git verifies at the commit date: valid) is REFUSED, because the expiry is read at the NEWEST holding block's time (a sort | head -1 read takes the older time and admits it)
mk BO $R0 $((now-9000)) -- dg1:dg1 dg2:dg2;CD="$(date -d '-150 min' -R)";gate $H1 $(mkc $H1 bx-cert.pub .agi/context/schemas/s.md:$E.s);unset CD;ro=$r;git update-ref -d refs/agi/block/BO;r=$ro
ok "t10r-two-blocks-newest-time-refused two holding blocks (times now and now - 150 min): a cert valid at the OLDER block's time and expired at the NEWER one is refused: the cert is read at the NEWEST holding block's time" 'refused'
# --- H1-H5: the hybrid cell and the hash (blocks over the genesis tip R0; DG1/DG2 hold ed25519 AND ecdsa columns in the ring)
export AGI_SIGN="ED25519 ECDSA"
mk HA $R0 $now -- dg1:dg1 dg2:dg2;ok "h1-hybrid-ed-only-no under a two-column cell the ed25519-only level-3 block does not hold" '! holds HA'
mk HB $R0 $now -- dg1:dg1 dg1:dg1q dg2:dg2 dg2:dg2q;ok "h2-hybrid-both-columns-holds DG1 + DG2 in both columns hold" 'holds HB'
mk HC $R0 $now -- dg1:dg1 dg1:dg1q dg2:dg2;ok "h3-hybrid-missing-column-no DG2 missing its second column does not hold" '! holds HC'
unset AGI_SIGN;MKH=sha512 mk HS $R0 $now -- dg1:dg1 dg2:dg2;ok "h4-sha512-holds a block naming sha512 holds under the default AGI_HASHES" 'holds HS'
ok "h5-hash-not-allowed a block naming sha512 does not hold when AGI_HASHES is sha256 only" '! (AGI_HASHES=sha256;export AGI_HASHES;holds HS)'
MKH=md5 mk HM $R0 $now -- dg1:dg1 dg2:dg2 2>/dev/null;ok "h6-unknown-hash a block naming a hash outside the cell (md5) does not hold" '! holds HM'
# --- CORRECTIVE (DG1 13:32Z; SM mur sm20-dg3-ckpt-1 R1 R3 n1 n2): written BEFORE the fix, each lane isolated (iso clears refs/agi/block, rst restores the earlier ones); ckc = a DIRECT `ckpt check` run (rc in ckrc)
git for-each-ref --format='%(objectname) %(refname)' refs/agi/block>$D/blk.all
iso(){ git for-each-ref --format='%(refname)' refs/agi/block|while read rf;do git update-ref -d $rf;done;}
rst(){ iso;while read ob rf;do git update-ref $rf $ob;done<$D/blk.all;}
ckc(){ sh $AGI_CKPT check>$D/ck.out 2>$D/ck.err;ckrc=$?;}
OLD='1000000000 +0000'
# mkraw NAME TIP TIME [HASH] [DATE] [SIGSTREE]: a block with the given RAW tip / time / hash text (an empty sigs tree unless SIGSTREE), committer date DATE
mkraw(){ nm=$1;hb=$(printf '%s' "${4:-sha256 0}"|git hash-object -w --stdin);st=${6:-$(git mktree </dev/null)};tr=$(printf '100644 blob %s\thash\n040000 tree %s\tsigs\n100644 blob %s\ttime\n100644 blob %s\ttip\n' $hb $st $(printf '%s' "$3"|git hash-object -w --stdin) $(printf '%s' "$2"|git hash-object -w --stdin)|git mktree);[ -n "$5" ]&&export GIT_COMMITTER_DATE="$5";git update-ref refs/agi/block/$nm $(echo "block $nm"|git commit-tree $tr);unset GIT_COMMITTER_DATE;}
git show $R0:.agi/nodes/doc/y.md>$E.cy;echo cr>>$E.cy;CE=$(mkc $R0 dg1 .agi/nodes/doc/y.md:$E.cy)
# R1a: the LAST block listed is non-holding: the exit status must not be that of the loop's last test
iso;mk HB $R0 $now -- dg1:dg1 dg2:dg2;GIT_COMMITTER_DATE="$OLD";export GIT_COMMITTER_DATE;mk NB $R0 $now -- dg1:dg1;unset GIT_COMMITTER_DATE;ckc;gate $R0 $CE
ok "r1a-nonholding-last-exit-0 two blocks, ONE holding (HB) and ONE non-holding (NB: one signer under k = 2) that rev-list visits LAST (committer date 2001): ckpt check exits 0 (got $ckrc), lists HB and not NB, and the gate admits a plain edit (rc $r)" '[ $ckrc = 0 ]&&holds HB&&! holds NB&&[ $r = 0 ]'
iso;GIT_COMMITTER_DATE="$OLD";export GIT_COMMITTER_DATE;mk HB2 $R0 $now -- dg1:dg1 dg2:dg2;unset GIT_COMMITTER_DATE;mk NB2 $R0 $now -- dg1:dg1;ckc;gate $R0 $CE
ok "r1a-mirror-nonholding-first-exit-0 the MIRROR (control): the non-holding block visited FIRST, the holding one last: exit 0, HB2 listed, NB2 not, the gate admits" '[ $ckrc = 0 ]&&holds HB2&&! holds NB2&&[ $r = 0 ]'
# R1b / n2: a ckpt that cannot READ stays NON-ZERO and the gate refuses (a fix of R1 must not become exit 0 always)
iso;mk HB $R0 $now -- dg1:dg1 dg2:dg2;mkdir -p $D/shl;printf '#!/bin/sh\n[ "$1" = for-each-ref ]&&{ echo "shim: for-each-ref failed" >&2;exit 128;}\nexec /usr/bin/git "$@"\n'>$D/shl/git;chmod +x $D/shl/git
PATH=$D/shl:$PATH;ckc;rb=$ckrc;gate $R0 $CE;rg=$r;PATH=${PATH#$D/shl:}
ok "r1b-listing-failure-nonzero the block LISTING step (git for-each-ref) fails (a shim): ckpt check exits NON-ZERO (got $rb), not 0 with an empty list, and the gate refuses the plain edit (rc $rg)" '[ "$rb" != 0 ]&&[ "$rg" != 0 ]&&[ "$rg" != 124 ]'
GIT_DIR=$D/nogit ckc;rb=$ckrc
ok "r1b2-bad-gitdir-nonzero GIT_DIR names no repository: ckpt check exits NON-ZERO (got $rb)" '[ "$rb" != 0 ]'
printf '#!/bin/sh\n[ "$1" = rev-list ]&&case "$2" in -*);;*)echo "shim: rev-list failed" >&2;exit 128;;esac\nexec /usr/bin/git "$@"\n'>$D/shl/git;PATH=$D/shl:$PATH;ckc;rb=$ckrc;PATH=${PATH#$D/shl:}
ok "r1b3-revlist-failure-nonzero the block rev-list over the holding tips fails (a shim, ckpt's own call only): ckpt check exits NON-ZERO (got $rb)" '[ "$rb" != 0 ]'
# R3a: a tip file that is an OPTION for git archive must not run: --output=FILE HEAD
iso;mk HB $R0 $now -- dg1:dg1 dg2:dg2;mkraw PW "--output=$D/pwn HEAD" $now;ckc
ok "r3a-tip-option-output-not-run a block whose tip file is '--output=<FILE> HEAD' (FILE does not exist) is SKIPPED: ckpt check exits 0 (got $ckrc), lists HB, and FILE was NOT created" '[ $ckrc = 0 ]&&holds HB&&[ ! -e $D/pwn ]'
echo keep>$D/pkeep;mkraw PK "--output=$D/pkeep HEAD" $now;ckc
ok "r3a2-tip-option-output-existing-file-kept the same with an EXISTING file: its bytes stay 'keep' (git archive --output would truncate it)" '[ "$(cat $D/pkeep)" = keep ]'
# R3b: option-shaped / non-hex tip, a glob and an option-shaped time: each block skipped, exit 0, nothing created; HB (a valid 40-hex tip, digit time) still listed
iso;mk HB $R0 $now -- dg1:dg1 dg2:dg2;ls -A $D/r>$D/ls0;mkraw T1 zzzz $now;mkraw T2 --version $now;mkraw T3 $(git rev-parse $R0) '*';mkraw T4 $(git rev-parse $R0) --x;mkraw T5 "-h" $now;ckc;ls -A $D/r>$D/ls1
ok "r3b-nonhex-option-glob-skipped tip 'zzzz', tip '--version', tip '-h', time '*' (a glob) and time '--x' (an option): each block skipped, ckpt check exits 0 (got $ckrc), the control block HB (a 40-hex tip, a digit time) is listed, nothing was created in the repo's work dir" '[ $ckrc = 0 ]&&holds HB&&cmp -s $D/ls0 $D/ls1&&! holds T1&&! holds T2&&! holds T3&&! holds T4&&! holds T5'
# R3c: a valid-looking hex that names NO object: skipped, not a crash for the others
iso;mkraw NX 0123456789abcdef0123456789abcdef01234567 $now;GIT_COMMITTER_DATE="$OLD";export GIT_COMMITTER_DATE;mk HB $R0 $now -- dg1:dg1 dg2:dg2;unset GIT_COMMITTER_DATE;ckc
ok "r3c-hex-no-object-skipped a tip that is 40 hex characters naming NO object: the block is skipped and the OTHER block (visited after it) is still listed, exit 0 (got $ckrc)" '[ $ckrc = 0 ]&&holds HB&&! holds NX'
# R3d (DG1 13:39Z): r3b is green only because the hash compare skips a tip that carries extra words. r3d = tips that START like a real object and carry more, with the hash line MATCHED to what `d` prints for the CLEAN 40-hex (the digest of git archive of the hex alone), so ONLY a validation of the tip can refuse them. Each lane: block not listed, the FILE (inside $D) NOT created, the control HB still listed. SIGNED variants (mks: dg1 + dg2 sign the message `ckpt sign` builds from the SPLIT tip words, exactly what check verifies) show whether the block would HOLD
hx=$(git rev-parse $R0);mh="sha256 $(git archive --format=tar $hx|sha256sum|cut -d' ' -f1)"
mks(){ nm=$1;tp=$2;shift 2;i=$(mktemp);j=0;for a in "$@";do j=$((j+1));p=${a%%:*};k=${a#*:};b=$(ckpt sign $p $K/$k $tp $now|git hash-object -w --stdin);printf '100644 blob %s\t%s.%s\n' $b $p $j;done>$i;mkraw $nm "$tp" $now "$mh" "" $(git mktree<$i);rm -f $i;}
wr(){ find "$D"/$1* -type f 2>/dev/null|wc -l;}
mkdir -p "$D/w1:$GEO" "$D/w2:$GEO" "$D/w3:$GEO" "$D/w4:$GEO"
iso;mk HB $R0 $now -- dg1:dg1 dg2:dg2;mkraw A1 "$hx --output=$D/w1" $now "$mh";ckc
ok "r3d-a-hex-space-output a block whose tip is a valid 40-hex of an EXISTING commit + a space + '--output=FILE' (hash line matched to the clean hex): skipped, exit 0 (got $ckrc), HB listed, and no file was written at FILE (the unquoted tip splits into git show's arguments: --output=FILE:<path> would open it). Observed: A1 $(holds A1&&echo LISTED||echo not-listed), files written $(wr w1)" '[ $ckrc = 0 ]&&holds HB&&! holds A1&&[ "$(wr w1)" = 0 ]'
iso;mk HB $R0 $now -- dg1:dg1 dg2:dg2;mks A2 "$hx --output=$D/w2" dg1:dg1 dg2:dg2;ckc
ok "r3d-a-signed-hex-space-output the same tip, SIGNED by dg1 + dg2 over what check verifies: not listed, exit 0 (got $ckrc), HB listed, no file written at FILE. Observed: A2 $(holds A2&&echo LISTED||echo not-listed), files written $(wr w2)" '[ $ckrc = 0 ]&&holds HB&&! holds A2&&[ "$(wr w2)" = 0 ]'
iso;mk HB $R0 $now -- dg1:dg1 dg2:dg2;mkraw B1 "$hx
--output=$D/w3" $now "$mh";mks B2 "$hx
--output=$D/w4" dg1:dg1 dg2:dg2;ckc
ok "r3d-b-hex-newline-second-word a tip that is a valid 40-hex + a NEWLINE + '--output=FILE' (raw, and signed by dg1 + dg2): neither is listed, exit 0 (got $ckrc), HB listed, no file written at FILE. Observed: B1 $(holds B1&&echo LISTED||echo not-listed) files $(wr w3), B2 $(holds B2&&echo LISTED||echo not-listed) files $(wr w4)" '[ $ckrc = 0 ]&&holds HB&&! holds B1&&! holds B2&&[ "$(wr w3)" = 0 ]&&[ "$(wr w4)" = 0 ]'
# r3d-b3: the second word is a REF: git show would read the ring from THAT revision instead of the tip's (git show hex dg1:<path>), and lv reads the second word as the post name
iso;sed "s|^dg1 ssh-ed25519 .*|dg1 $(pk dg1b)|" $GEO/ring>$E.ring3;TR=$(mkc $R0 dg1 $GEO/ring:$E.ring3);git update-ref refs/heads/dg1 $TR
mk HB $R0 $now -- dg1:dg1 dg2:dg2;mks RC "$hx" dg1:dg1b dg2:dg2;mks RR "$hx
dg1" dg1:dg1b dg2:dg2;mk RT $TR $now -- dg1:dg1b dg2:dg2;ckc
ok "r3d-b3-second-word-ref-redirects-the-ring a tip '<R0 hex> NEWLINE dg1' where a branch named dg1 holds a ring in which dg1's key is dg1b's: signed by dg1b + dg2 it must NOT hold (the ring is the tip's, R0 has dg1's own key). Controls in the same repo: the CLEAN tip R0 signed the same way does not hold (RC), the clean tip of the commit with that ring does hold (RT), HB holds. Observed: RR $(holds RR&&echo LISTED||echo not-listed), RC $(holds RC&&echo LISTED||echo not-listed), RT $(holds RT&&echo LISTED||echo not-listed)" '[ $ckrc = 0 ]&&holds HB&&holds RT&&! holds RC&&! holds RR'
git update-ref -d refs/heads/dg1
# r3d-c: a lone star (a glob over the hook's cwd) and a star after a valid hex; files in the cwd whose names are options for git archive; default hash (d runs BEFORE the compare)
iso;mk HB $R0 $now -- dg1:dg1 dg2:dg2;ls -A $D/r>$D/ls0;: >"$D/r/--output=cs";mkraw S1 '*' $now;ckc;ls -A $D/r>$D/ls1;rm -f "$D/r/--output=cs" $D/r/cs
ok "r3d-c-lone-star a tip that is '*' with a file named '--output=cs' in the hook's cwd (a glob would expand it into git archive): skipped, exit 0 (got $ckrc), HB listed, nothing created in the cwd besides the planted file. Observed: S1 $(holds S1&&echo LISTED||echo not-listed), new names in the cwd $(diff $D/ls0 $D/ls1|grep -c '^>') (want 1 = the planted file)" '[ $ckrc = 0 ]&&holds HB&&! holds S1&&[ "$(diff $D/ls0 $D/ls1|grep -c "^>")" = 1 ]'
iso;mk HB $R0 $now -- dg1:dg1 dg2:dg2;: >"$D/r/${hx}x";mkraw S2 "$hx*" $now "$mh";mks S3 "$hx*" dg1:dg1 dg2:dg2;ckc;rm -f "$D/r/${hx}x"
ok "r3d-c-star-after-hex a tip that is a valid 40-hex + '*' (raw with the matched hash, and signed) with a file '<hex>x' in the cwd: neither listed, exit 0 (got $ckrc), HB listed. Observed: S2 $(holds S2&&echo LISTED||echo not-listed), S3 $(holds S3&&echo LISTED||echo not-listed)" '[ $ckrc = 0 ]&&holds HB&&! holds S2&&! holds S3'
# R3e (DG1 15:28Z, GAP 1): with the quotes kept, NOTHING pinned the tip validation. The real tip is exactly '--output=FILE' (no space, no hex, nothing for the quotes to turn into an odd name): git archive with an option and no tree-ish still creates / truncates FILE. The hash line is MATCHED to the digest of an EMPTY archive (what archive prints on stdout then), so only the validation refuses; raw and signed; FILE is a name relative to the hook's cwd (the repo work dir). A signer's own `ckpt sign` runs the same archive, so FILE is removed after signing
eh="sha256 $(printf ''|sha256sum|cut -d' ' -f1)";mh0=$mh;mh=$eh;L40=$(printf 'k%.0s' $(seq 1 31))
iso;mk HB $R0 $now -- dg1:dg1 dg2:dg2;ls -A $D/r>$D/ls0;mkraw E1 '--output=e3a' $now "$eh";mks E2 '--output=e3b' dg1:dg1 dg2:dg2;rm -f $D/r/e3a $D/r/e3b;ckc;ls -A $D/r>$D/ls1
ok "r3e-a-bare-output-option-no-tree-ish a block whose tip is exactly '--output=e3a' (no space, no hex; the hash line matched to an EMPTY archive), raw and SIGNED by dg1 + dg2 (E2: --output=e3b): neither is listed, exit 0 (got $ckrc), HB listed, no new FILE in the repo work dir. Observed: E1 $(holds E1&&echo LISTED||echo not-listed), E2 $(holds E2&&echo LISTED||echo not-listed), new names $(diff $D/ls0 $D/ls1|grep -c '^>')" '[ $ckrc = 0 ]&&holds HB&&! holds E1&&! holds E2&&cmp -s $D/ls0 $D/ls1'
iso;mk HB $R0 $now -- dg1:dg1 dg2:dg2;mkraw E3 '--output=ekeep' $now "$eh";mks E4 '--output=ekeep2' dg1:dg1 dg2:dg2;rm -f $D/r/ekeep $D/r/ekeep2;echo keep>$D/r/ekeep;echo keep>$D/r/ekeep2;ckc;ek1=$(cat $D/r/ekeep);ek2=$(cat $D/r/ekeep2)
ok "r3e-b-existing-file-bytes-kept the same with an EXISTING file (E3: --output=ekeep raw; E4: --output=ekeep2 signed; each holds 'keep'): the bytes are unchanged (git archive --output with no tree-ish truncates them), neither listed, HB listed, exit 0 (got $ckrc). Observed: ekeep '$ek1' ($(holds E3&&echo LISTED||echo not-listed)), ekeep2 '$ek2' ($(holds E4&&echo LISTED||echo not-listed))" '[ $ckrc = 0 ]&&holds HB&&! holds E3&&! holds E4&&[ "$ek1" = keep ]&&[ "$ek2" = keep ]'
rm -f $D/r/ekeep $D/r/ekeep2
iso;mk HB $R0 $now -- dg1:dg1 dg2:dg2;ls -A $D/r>$D/ls0;mkraw E5 "--output=$L40" $now "$eh";mks E6 "--output=${L40}j" dg1:dg1 dg2:dg2;rm -f $D/r/$L40 $D/r/${L40}j;mkraw E7 "--output=${L40%k}" $now "$eh";ckc;ls -A $D/r>$D/ls1
ok "r3e-c-forty-char-option-tip option-shaped tips of 40 and 41 characters ('--output=' + a 31-char name: E5 raw; E6 signed one longer) and 39 (E7): none listed, HB listed, exit 0 (got $ckrc), no new FILE (a length case alone, 40 or 64, lets the 40-char option through to git archive). Observed: E5 $(holds E5&&echo LISTED||echo not-listed), E6 $(holds E6&&echo LISTED||echo not-listed), E7 $(holds E7&&echo LISTED||echo not-listed), new names $(diff $D/ls0 $D/ls1|grep -c '^>')" '[ $ckrc = 0 ]&&holds HB&&! holds E5&&! holds E6&&! holds E7&&cmp -s $D/ls0 $D/ls1'
mh=$mh0
# R3f (DG1 15:28Z, GAP 2): a SIGNED block with a non-digit time (dg1 + dg2 sign tip / time / hash / digest with time abc or 1e9) must not be listed: listed, the gate dies on EVERY push ("a holding block names a non-numeric time"), a DoS by two level-3 signers
iso;mk HB $R0 $now -- dg1:dg1 dg2:dg2;mk TA $R0 abc -- dg1:dg1 dg2:dg2;mk TB $R0 1e9 -- dg1:dg1 dg2:dg2;ckc;gate $R0 $CE
ok "r3f-signed-nondigit-time-not-listed two blocks SIGNED by dg1 + dg2 over time 'abc' (TA) and '1e9' (TB): neither is listed, exit 0 (got $ckrc), the control HB is listed, and the gate admits a plain edit (rc $r). Observed: TA $(holds TA&&echo LISTED||echo not-listed), TB $(holds TB&&echo LISTED||echo not-listed)" '[ $ckrc = 0 ]&&holds HB&&! holds TA&&! holds TB&&[ $r = 0 ]'
# R4 (DG1 15:53Z, SM mur sm20-dg3-ckpt-2 D1 D2, on 0d57750d7): D1 the ring text reaches allowed_signers UNFILTERED (the gate greps the canonical shape first). A tip whose ring carries an off-shape line beside the canonical ones: a block signed with that key is NOT listed; controls: the canonical keys of the same ring still hold, a key under a CANONICAL name holds. A RAW (empty sigs) block can never hold, so every lane here is SIGNED. attacker keys atk1 atk2 are in NO canonical line
for n in atk1 atk2;do ssh-keygen -qN "" -ted25519 -f$K/$n -C $n>/dev/null;done
ringt(){ cp $GEO/ring $E.rg;printf '%s\n' "$@">>$E.rg;mkc $R0 dg1 $GEO/ring:$E.rg;}
d1(){ bn=$1;shift;iso;mk HB $R0 $now -- dg1:dg1 dg2:dg2;TR=$(ringt "$@");mk RK $TR $now -- dg1:dg1 dg2:dg2;mk $bn $TR $now -- $SG;ckc;}
SG="dg1:dg1 dg2:atk1";d1 W1 "* $(pk atk1)"
ok "r4-d1a-wildcard-principal-one-key the tip ring holds a wildcard line '* ssh-ed25519 KEY' (ONE attacker key atk1): a block signed by dg1 (canonical) + dg2 = atk1 is NOT listed (the wildcard would let ONE key verify as ANY post). Controls: the canonical dg1 + dg2 block on the same tip (RK) and HB are listed. Observed: W1 $(holds W1&&echo LISTED||echo not-listed), RK $(holds RK&&echo ok||echo LOST)" '[ $ckrc = 0 ]&&holds HB&&holds RK&&! holds W1'
SG="dg1:atk1 dg2:atk2";d1 W2 "* $(pk atk1)" "* $(pk atk2)"
ok "r4-d1b-wildcard-principal-two-keys two wildcard lines (atk1, atk2): a block signed by atk1 as dg1 + atk2 as dg2, NO canonical key at all, is NOT listed. Observed: W2 $(holds W2&&echo LISTED||echo not-listed), RK $(holds RK&&echo ok||echo LOST)" '[ $ckrc = 0 ]&&holds HB&&holds RK&&! holds W2'
SG="dg1:dg1 dg2:atk1";d1 W3 "dg2@agi $(pk atk1)"
ok "r4-d1c-presuffixed-principal a line already in allowed_signers form 'dg2@agi ssh-ed25519 KEY' (no namespace option; the sed leaves it as it is): a block signed by dg1 + dg2 = atk1 is NOT listed. Observed: W3 $(holds W3&&echo LISTED||echo not-listed), RK $(holds RK&&echo ok||echo LOST)" '[ $ckrc = 0 ]&&holds HB&&holds RK&&! holds W3'
SG="dg1:dg1 dg2:atk1";d1 W4 " dg2@agi $(pk atk1)"
ok "r4-d1d-leading-space-before-name a line with SPACES before the name ' dg2@agi ssh-ed25519 KEY': not listed. Observed: W4 $(holds W4&&echo LISTED||echo not-listed), RK $(holds RK&&echo ok||echo LOST)" '[ $ckrc = 0 ]&&holds HB&&holds RK&&! holds W4'
SG="dg1:dg1 dg2:atk1";d1 W5 "$(printf 'dg2@agi\t%s' "$(pk atk1)")"
ok "r4-d1e-tab-in-line a line with a TAB between the principal and the key: not listed. Observed: W5 $(holds W5&&echo LISTED||echo not-listed), RK $(holds RK&&echo ok||echo LOST)" '[ $ckrc = 0 ]&&holds HB&&holds RK&&! holds W5'
SG="dg1:dg1 dg2:atk1";d1 W6 "DG2@agi $(pk atk1)" "Dg2 $(pk atk1)" "dg2 namespaces=\"git\" $(pk atk1)"
ok "r4-d1f-uppercase-and-options-harmless uppercase names (DG2@agi, Dg2) and a name followed by an option are off shape too; ssh-keygen does not match them as dg2@agi, so they are GREEN BY LUCK today (named; the lane pins that a filter fix keeps them out): not listed. Observed: W6 $(holds W6&&echo LISTED||echo not-listed), RK $(holds RK&&echo ok||echo LOST)" '[ $ckrc = 0 ]&&holds HB&&holds RK&&! holds W6'
SG="dg1:dg1 dg2:atk1";d1 W7 "dg2 $(pk atk1)"
ok "r4-d1g-canonical-name-holds CONTROL: the key under a CANONICAL name ('dg2 ssh-ed25519 KEY' beside dg2's own line) holds: the filter must not drop canonical lines. Observed: W7 $(holds W7&&echo listed||echo NOT-LISTED)" '[ $ckrc = 0 ]&&holds W7'
# D2: lv (jq over posts.md at the tip) fails -> the row becomes ' FP ' and the awk reads the fingerprint as the level (a string = 0). A tip whose posts.md makes jq reject: no block holds there; one signer unreadable among good ones does not count
pst(){ cp $GEO/posts.md $E.ps;"$@">>$E.ps;mkc $R0 dg1 $GEO/posts.md:$E.ps;}
badline(){ printf '%s\n' "$BL";}
d2(){ bn=$1;bs=$2;iso;mk HB $R0 $now -- dg1:dg1 dg2:dg2;TP=$(pst badline);mk $bn $TP $now -- $bs;ckc;}
BL='  - {"name": "zz", "parent": ';d2 P1 "dg1:dg1 dg2:dg2"
ok "r4-d2a-posts-invalid-json a tip whose posts.md carries an invalid JSON row (jq rejects the whole file): the dg1 + dg2 block on that tip is NOT listed (no level is readable), exit 0 (got $ckrc), HB listed. Observed: P1 $(holds P1&&echo LISTED||echo not-listed)" '[ $ckrc = 0 ]&&holds HB&&! holds P1'
BL='  - {"parent": "sm", "harness": "x"}';d2 P2 "dg1:dg1 dg2:dg2"
ok "r4-d2b-posts-row-without-name a posts.md row WITHOUT a name (jq: object keys must be strings): not listed. Observed: P2 $(holds P2&&echo LISTED||echo not-listed)" '[ $ckrc = 0 ]&&holds HB&&! holds P2'
BL='  - {"name": "lpa", "parent": "lpb"}
  - {"name": "lpb", "parent": "lpa"}';d2 P3 "dg1:dg1 dg2:dg2"
ok "r4-d2c-posts-parent-loop a parent LOOP in posts.md (lpa <-> lpb): the dg1 + dg2 rows are unaffected, so the block on that tip still holds (the loop only hurts a signer INSIDE it: level -99). CONTROL for the rows: P3 $(holds P3&&echo listed||echo NOT-LISTED)" '[ $ckrc = 0 ]&&holds HB&&holds P3'
# one signer's row unreadable (dg2's parent is a NUMBER: jq errors only on dg2's chain)
pst2(){ sed 's|^  - {"name": "dg2", "parent": "sm"|  - {"name": "dg2", "parent": 5|' $GEO/posts.md>$E.ps2;mkc $R0 dg1 $GEO/posts.md:$E.ps2;}
iso;mk HB $R0 $now -- dg1:dg1 dg2:dg2;TQ=$(pst2);mk Q1 $TQ $now -- belam:belam1 dg2:dg2;mk Q2 $TQ $now -- alive:alive1 aio:aio1 sm:sm1 dg2:dg2;mk Q3 $TQ $now -- dg1:dg1 dg2:dg2;ckc
ok "r4-d2d-one-signer-level-unreadable posts.md at the tip where ONLY dg2's row is unreadable (parent 5): Q1 belam (level 1) + dg2 (unreadable) must NOT hold (k = 2 not met: the unreadable signer does not count; today its fingerprint reads as level 0, adjacent to 1); Q3 dg1 + dg2 must NOT hold; Q2 alive + all-is-one + sm + dg2 (three good level-2 signers) MUST hold (the rest still reach k). Observed: Q1 $(holds Q1&&echo LISTED||echo not-listed), Q3 $(holds Q3&&echo LISTED||echo not-listed), Q2 $(holds Q2&&echo listed||echo NOT-LISTED)" '[ $ckrc = 0 ]&&holds HB&&! holds Q1&&! holds Q3&&holds Q2'
iso;mk HB $R0 $now -- dg1:dg1 dg2:dg2;mkdir -p $D/jqs;printf '#!/bin/sh\necho "shim: jq failed" >&2\nexit 5\n'>$D/jqs/jq;chmod +x $D/jqs/jq;PJ=$PATH;PATH=$D/jqs:$PATH;ckc;PATH=$PJ
ok "r4-d2e-jq-fails-for-the-run jq shimmed to fail for the whole run: NOTHING is listed (HB not either), ckpt check exits 0 (got $ckrc: a failed level read is a skipped signer, not a crash). Observed: $(wc -l <$D/ck.out) lines listed" '[ $ckrc = 0 ]&&[ ! -s $D/ck.out ]'
# n1: ONE key listed under two post names counts ONCE (distinct KEYS, not names)
iso;sed "s|^dg2 .*|dg2 $(pk dg1)|" $GEO/ring>$E.ring2;T1=$(mkc $R0 dg1 $GEO/ring:$E.ring2);mk SH $T1 $now -- dg1:dg1 dg2:dg1;mk CTRL $R0 $now -- dg1:dg1 dg2:dg2
ok "n1-one-key-two-names-no the ring lists ONE key under two post names (dg1 and dg2, a parent writing its own key as a child's line) and two signatures from that key under the two names, k = 2: the block does NOT hold (distinct keys count, not names); control: two DISTINCT keys (CTRL) hold" '! holds SH&&holds CTRL'
# n2: ONE unreadable block among good ones is skipped, the others are listed, exit 0
iso;mk HB $R0 $now -- dg1:dg1 dg2:dg2;mb=$(printf '100644 blob 0123456789abcdef0123456789abcdef01234567\ttip\n'|git mktree --missing);GIT_COMMITTER_DATE="$OLD";export GIT_COMMITTER_DATE;git update-ref refs/agi/block/UNR $(echo "block UNR"|git commit-tree $mb);unset GIT_COMMITTER_DATE;ckc
ok "n2-unreadable-block-skipped one block whose tip blob is MISSING from the object store (visited last) among a good one: it is skipped, HB is listed, exit 0 (got $ckrc)" '[ $ckrc = 0 ]&&holds HB&&! holds UNR'
rst
echo "ckpt: $f FAIL"
exit $f
