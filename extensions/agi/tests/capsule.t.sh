#!/bin/sh
# capsule.t.sh: goal:g7.16.1.11.44.1-.4 (DG4): the capsule verbs pack · out · verify · in of doc:g716111-44-capsule-pack section 5, each its own rows, each with a mutant RED.
# sh + git + ssh-keygen on a scratch tree, throwaway keys, ONE uid, no network, no root, 0 USD. One ok/FAIL line per case; exit = number of FAILs.
# CAPSULE = the piece under test (default: `sect capsule` of the .geometry/engine*.md of ROOT, the working tree). A MUTANT row runs the piece with one check turned off and passes only when the clean row's condition is FALSE for it (the row would be RED).
T=$(mktemp -d);trap 'rm -rf $T' 0;f=0;G=/usr/bin/git;R0=${ROOT:-$(cd "$(dirname "$0")/../../.." && pwd)}
[ -n "$CAPSULE" ]||{ cat $R0/.agi/nodes/.geometry/engine*.md|sed -n "/^###* capsule /,/^###* /{/^~~~/,/^~~~/{//!p}}">$T/cap;CAPSULE=$T/cap;};[ -s $CAPSULE ]||{ echo "FAIL extract: capsule $(wc -c<$CAPSULE)";exit 99;}
ok(){ if eval "$2";then echo "ok $1";else echo "FAIL $1";f=$((f+1));fi;}
mut(){ sed "$1" $CAPSULE>$T/mut;cmp -s $CAPSULE $T/mut&&echo "FAIL mutant $2 changed nothing";}   # mut SED NAME: writes $T/mut
# --- fixture: keys (dg4 and other are in the ring, mal is not), per-user gitconfig, one repo with a goal tree, a payload, three post refs
mkdir $T/k $T/c;: >$T/allowed
for u in dg4 other mal;do ssh-keygen -q -t ed25519 -N '' -f $T/k/$u -C $u>/dev/null
 [ $u = mal ]||echo "$u@agi namespaces=\"git\" $(cut -d' ' -f1,2 $T/k/$u.pub)">>$T/allowed
 printf '[user]\n\tname=%s\n\temail=%s@agi\n\tsigningkey=%s\n[gpg]\n\tformat=ssh\n[commit]\n\tgpgsign=false\n[safe]\n\tdirectory=*\n' $u $u $T/k/$u>$T/c/$u;done
export GIT_CONFIG_SYSTEM=/dev/null GIT_CONFIG_GLOBAL=$T/c/dg4
M1=11111111111111111111111111111111;M2=22222222222222222222222222222222;M3=33333333333333333333333333333333;M4=44444444444444444444444444444444;M5=55555555555555555555555555555555;M6=66666666666666666666666666666666
$G init -q $T/r;cd $T/r;mkdir -p .agi/nodes/goal .agi/nodes/build src
node(){ printf -- '---\nid: %s\nmint_id: %s\ntype: %s\nparents:\n%s\nnext_edges: []\n%s---\nbody\n' "$1" "$2" "${1%%:*}" "$3" "$4">.agi/nodes/${1%%:*}/${1#*:}.md;}
node goal:a $M1 '  - goal:root' '';node goal:b $M2 '  - goal:a' '';node goal:c $M3 '  - goal:zzz' '';node build:f $M4 '  - goal:b' 'payload_ref: src/f.py
';node goal:d $M5 '  - goal:other' '';mkdir -p .agi/nodes/deprecated/goal;printf -- '---\nid: goal:dep\nmint_id: %s\ntype: goal\nparents:\n  - goal:b\nnext_edges: []\nstatus: deprecated\n---\nretired\n' $M6>.agi/nodes/deprecated/goal/dep.md
sed -i 's/^parents:$/parents:/' .agi/nodes/goal/b.md;echo 'print(1)'>src/f.py
head -c 300000 /dev/urandom >src/ballast.bin;$G add -A;$G -c user.name=x -c user.email=x@x commit -qm ballast;$G rm -q src/ballast.bin;$G -c user.name=x -c user.email=x@x commit -qm base;BASE=$($G rev-parse HEAD)
$G -c user.name=x -c user.email=x@x commit -qm p1 --allow-empty;$G update-ref refs/heads/posts/p HEAD;$G update-ref refs/box/p/q HEAD;$G update-ref refs/held/p/x HEAD;$G update-ref refs/heads/posts/other HEAD;$G update-ref refs/grid/n1 HEAD
$G reset -q --hard $BASE;cd $T
cap(){ u=$1;r=$2;shift 2;(cd $r&&AGI_POST=$u AGI_TRUNK=HEAD AGI_ALLOWED=$T/allowed GIT_CONFIG_GLOBAL=$T/c/$u sh ${PIECE:-$CAPSULE} "$@");}
snap(){ (cd $1&&find . -type f -print0|sort -z|xargs -0 sha1sum|sha1sum);}
new(){ $G init -q --bare $T/$1.git;$G -C $T/$1.git fetch -q $T/r $BASE:refs/heads/main;}   # a target holding base only
new t
# --- P: pack
CID=$(cap dg4 $T/r pack $M1 subtree $M1 2>$T/p.err);ok p0-packs-and-prints-a-cid '[ ${#CID} = 32 ]&&[ ! -s $T/p.err ]'
MF=$($G -C $T/r show refs/capsule/$CID:MANIFEST)
ok p1-the-ref-is-created-once '! CID=$CID cap dg4 $T/r pack $M1 subtree $M1 2>/dev/null&&[ "$(CID=$CID cap dg4 $T/r pack $M1 subtree $M1 >/dev/null 2>&1;echo $?)" = 128 ]'
ok p1b-the-tip-is-one-signed-root-commit '[ "$($G -C $T/r rev-list --count refs/capsule/$CID)" = 1 ]&&[ "$($G -C $T/r -c gpg.ssh.allowedSignersFile=$T/allowed log -1 --format="%G? %GS" refs/capsule/$CID)" = "G dg4@agi" ]'
ok p2-subtree-members-are-the-tree-and-the-payload-not-the-rest 'echo "$MF"|grep -q "^member $M1 .agi/nodes/goal/a.md$"&&echo "$MF"|grep -q "^member $M2 "&&echo "$MF"|grep -q "^member $M4 .agi/nodes/build/f.md$"&&echo "$MF"|grep -q "^member $M4 src/f.py$"&&! echo "$MF"|grep -Eq "^member ($M3|$M5) "'
ok p2a-a-subtree-capsule-carries-no-ref-it-was-not-asked-for '! echo "$MF"|grep -q "^ref "'
ok p2b-the-tree-is-the-manifest-and-exactly-the-members '[ "$($G -C $T/r ls-tree -r --name-only refs/capsule/$CID|wc -l)" = "$(( $(echo "$MF"|grep -c "^member ")+1 ))" ]&&[ "$($G -C $T/r rev-parse refs/capsule/$CID:src/f.py)" = "$($G -C $T/r rev-parse $BASE:src/f.py)" ]'
ok p2c-the-manifest-names-attach-packer-base 'echo "$MF"|grep -qx "attach $M1"&&echo "$MF"|grep -qx "packer dg4@agi"&&echo "$MF"|grep -qx "base $BASE"&&echo "$MF"|grep -qx "kind slice"&&echo "$MF"|grep -qx "encrypt none"'
ok p3-every-boundary-line-is-present 'for w in ram-trees untracked-mints host-files crontabs refs/stash refs/remotes;do echo "$MF"|grep -q "^not $w ." || false;done'
cap dg4 $T/r pack $M1 subtree $M1 >/dev/null 2>$T/e1;r1=$?;cap dg4 $T/r pack $M1 subtree $M1 --kind slice --encrypt quorum >/dev/null 2>$T/e2;r2=$?;cap dg4 $T/r pack $M1 subtree $M1 --kind secret >/dev/null 2>$T/e3;r3=$?;cap dg4 $T/r pack $M1 subtree $M1 --encrypt box:x >/dev/null 2>$T/e4;r4=$?
ok p4-a-slice-is-never-quorum-popped '[ $r2 = 2 ]&&grep -qF "[class] a slice is never quorum-popped" $T/e2'
ok p4b-a-secret-without-quorum-is-refused-the-same-way '[ $r3 = 2 ]&&grep -qF "[class] a secret is always quorum-sealed" $T/e3'
ok p4c-a-seal-waits-for-the-hold '[ $r4 = 2 ]&&grep -qF "[seal]" $T/e4'
n0=$($G -C $T/r for-each-ref refs/capsule|wc -l)
ok p4d-a-refusal-writes-no-ref '[ "$n0" = 2 ]'
cap dg4 $T/r pack 00000000000000000000000000000000 subtree $M1 >/dev/null 2>$T/e5;r5=$?
ok p5-an-absent-attach-mint-is-rc-3 '[ $r5 = 3 ]&&grep -qF "[attach-absent]" $T/e5'
PC=$(cap dg4 $T/r pack $M1 post p --ref 'refs/heads/posts/o*' 2>/dev/null);PM=$($G -C $T/r show refs/capsule/$PC:MANIFEST)
ok p6-post-is-its-refs-only-and-no-member-lines 'echo "$PM"|grep -q "^ref refs/heads/posts/p "&&echo "$PM"|grep -q "^ref refs/box/p/q "&&echo "$PM"|grep -q "^ref refs/held/p/x "&&echo "$PM"|grep -q "^ref refs/heads/posts/other "&&! echo "$PM"|grep -q "^member "&&! echo "$PM"|grep -q "^ref refs/capsule/"'
ok p7-negative-the-piece-writes-no-grid-ref-and-no-nest-cell '! grep -q "refs/grid" $CAPSULE&&! grep -q "^nest:" $CAPSULE'
ok p8-pack-never-deletes-a-source-ref 'for r in refs/heads/posts/p refs/box/p/q refs/held/p/x;do $G -C $T/r rev-parse -q --verify $r>/dev/null||false;done'
mut 's/die 2 "\[class\] a slice/true 2 "[class] a slice/' p4;cp $T/mut $T/m-class
PIECE=$T/m-class cap dg4 $T/r pack $M1 subtree $M1 --encrypt quorum >/dev/null 2>$T/em;
ok p4-mutant-RED-the-class-check-turned-off-no-longer-names-the-class '! grep -qF "[class] a slice is never quorum-popped" $T/em'
# --- O: out
cap dg4 $T/r out $CID >$T/c.bundle 2>$T/o.err;ro=$?
ok o0-out-writes-a-bundle '[ $ro = 0 ]&&[ -s $T/c.bundle ]'
ok o1-bundle-verify-passes-where-base-is-held '$G -C $T/t.git bundle verify $T/c.bundle >/dev/null 2>&1'
$G init -q --bare $T/empty.git
ok o1b-bundle-verify-fails-where-base-is-not-held '! $G -C $T/empty.git bundle verify $T/c.bundle >/dev/null 2>&1'
cap dg4 $T/r out $PC >$T/p.bundle 2>$T/o2.err
ok o2-the-post-bundle-carries-exactly-the-ref-lines '[ "$($G bundle list-heads $T/p.bundle|sort)" = "$({ echo "$($G -C $T/r rev-parse refs/capsule/$PC) refs/capsule/$PC";echo "$PM"|sed -n "s/^ref \(.*\) \(.*\)/\2 \1/p";}|sort)" ]'
ok o3-out-refuses-a-ref-moved-since-pack '$G -C $T/r update-ref refs/box/p/q $BASE;! cap dg4 $T/r out $PC >/dev/null 2>$T/o3.err&&grep -qF "[moved] refs/box/p/q" $T/o3.err'
$G -C $T/r update-ref refs/box/p/q "$($G -C $T/r rev-parse refs/heads/posts/p)"
# FF1 (council 01:41Z): a post ref BEHIND base rides as its MANIFEST ref line ONLY: the bundle is THIN (no fat bundle, no `--not base` drop), verify = heads == the ref lines less
# the behind-base ones (each checked on the target by cat-file -e + merge-base --is-ancestor), and `in` sets it in the SAME atomic transaction as the carried refs
$G -C $T/r update-ref refs/archive/posts/old1 $BASE;FC=$(cap dg4 $T/r pack $M1 post old 2>/dev/null);cap dg4 $T/r out $FC >$T/thin.bundle 2>$T/thin.err
ok o4-a-ref-behind-base-is-a-line-not-a-head-and-the-bundle-is-thin '[ ! -s $T/thin.err ]&&! $G bundle list-heads $T/thin.bundle|grep -q " refs/archive/posts/old1$"&&$G -C $T/r show refs/capsule/$FC:MANIFEST|grep -q "^ref refs/archive/posts/old1 $BASE$"&&! $G -C $T/empty.git bundle verify $T/thin.bundle >/dev/null 2>&1'
PB=$(cap dg4 $T/r pack $M1 post p 2>/dev/null);cap dg4 $T/r out $PB >$T/pb.bundle
ok o4s-the-size-row-a-thin-bundle-leaves-the-base-history-out '[ $(wc -c <$T/thin.bundle) -lt 100000 ]&&[ $(wc -c <$T/pb.bundle) -lt 100000 ]'
mut 's/git bundle create \$d\/b refs\/capsule\/\$c \$K --not \$b/git bundle create $d\/b refs\/capsule\/$c $K/' o;ok o4s-mutant-RED-a-fat-bundle-carries-the-300-KB-of-history '! { PIECE=$T/mut cap dg4 $T/r out $PB >$T/fat.bundle 2>/dev/null;[ $(wc -c <$T/fat.bundle) -lt 100000 ];}'
new t3;ok o4b-a-behind-base-ref-and-a-thin-bundle-land-every-ref '(cd $T/t3.git&&AGI_ALLOWED=$T/allowed AGI_TRUNK=refs/heads/main sh $CAPSULE in $T/thin.bundle)&&[ "$($G -C $T/t3.git rev-parse refs/archive/posts/old1)" = "$BASE" ]&&$G -C $T/t3.git rev-parse -q --verify refs/capsule/$FC >/dev/null'
new t6;$G -C $T/t6.git update-ref refs/archive/posts/old1 $($G -C $T/t6.git commit-tree -m diverged $($G -C $T/t6.git rev-parse $BASE^{tree}));s6=$($G -C $T/t6.git for-each-ref)
ok o4c-a-non-ff-behind-base-ref-aborts-the-whole-transaction 'cd $T/t6.git;! AGI_ALLOWED=$T/allowed AGI_TRUNK=refs/heads/main sh $CAPSULE in $T/thin.bundle >/dev/null 2>$T/o4c.err;grep -qF "[non-ff] refs/archive/posts/old1" $T/o4c.err&&[ "$s6" = "$($G -C $T/t6.git for-each-ref)" ]'
# --- V: verify
ok v0-an-untouched-bundle-passes-and-the-target-is-byte-identical 's0=$(snap $T/t.git);(cd $T/t.git&&AGI_ALLOWED=$T/allowed AGI_TRUNK=refs/heads/main sh $CAPSULE verify $T/c.bundle)&&[ "$s0" = "$(snap $T/t.git)" ]'
vt(){ (cd $T/t.git&&AGI_ALLOWED=$T/allowed AGI_TRUNK=${TRK:-refs/heads/main} sh ${PIECE:-$CAPSULE} "$@");}
cp $T/c.bundle $T/flip.bundle;printf '\377' | dd of=$T/flip.bundle bs=1 seek=$(( $(wc -c <$T/flip.bundle) - 40 )) conv=notrunc 2>/dev/null
ok v1-one-flipped-byte-is-refused-and-the-target-is-byte-identical 's0=$(snap $T/t.git);! vt verify $T/flip.bundle >/dev/null 2>&1&&[ "$s0" = "$(snap $T/t.git)" ]'
# forged capsule commits in a copy of the source repo, bundled by raw git (out would refuse them)
forge(){ rm -rf $T/fr;$G clone -q --no-local $T/r $T/fr 2>/dev/null;$G -C $T/fr fetch -q $T/r "refs/capsule/*:refs/capsule/*" "refs/box/*:refs/box/*" "refs/held/*:refs/held/*" "refs/heads/posts/*:refs/heads/posts/*";}
forge;raw=$($G -C $T/fr cat-file commit refs/capsule/$CID);mf=$($G -C $T/fr rev-parse refs/capsule/$CID:MANIFEST);bad=$($G -C $T/fr show refs/capsule/$CID:MANIFEST|sed "s/^attach .*/attach $M2/"|$G -C $T/fr hash-object -w --stdin)
tr1=$($G -C $T/fr ls-tree refs/capsule/$CID|sed "s/$mf/$bad/"|$G -C $T/fr mktree);c1=$(echo "$raw"|sed "s/^tree .*/tree $tr1/"|$G -C $T/fr hash-object -t commit -w --stdin)
$G -C $T/fr update-ref refs/capsule/$CID $c1;$G -C $T/fr bundle create $T/f1.bundle refs/capsule/$CID --not $BASE 2>/dev/null
ok v2-a-manifest-edited-under-the-same-signature-is-refused '! vt verify $T/f1.bundle >/dev/null 2>$T/v2.err&&grep -qF "[sig]" $T/v2.err'
forge;pb=$($G -C $T/fr rev-parse refs/capsule/$PC);$G -C $T/fr update-ref refs/box/p/q $($G -C $T/fr commit-tree -p $BASE -m swapped $($G -C $T/fr rev-parse $BASE^{tree}));$G -C $T/fr bundle create $T/f2.bundle refs/capsule/$PC refs/heads/posts/p refs/box/p/q refs/held/p/x refs/heads/posts/other --not $BASE 2>/dev/null
ok v3-a-carried-ref-swapped-to-another-sha-is-refused '! vt verify $T/f2.bundle >/dev/null 2>$T/v3.err&&grep -qF "[heads]" $T/v3.err'
forge;$G -C $T/fr bundle create $T/f7.bundle refs/capsule/$PC refs/heads/posts/p refs/held/p/x refs/heads/posts/other --not $BASE 2>/dev/null
ok v3b-a-bundle-missing-an-ahead-ref-is-refused '! vt verify $T/f7.bundle >/dev/null 2>$T/v3b.err&&grep -qF "[heads]" $T/v3b.err'
forge;t0=$($G -C $T/fr rev-parse refs/capsule/$CID^{tree});ex=$($G -C $T/fr hash-object -w --stdin<<XX
x
XX
)
tr2=$({ $G -C $T/fr ls-tree refs/capsule/$CID;printf '100644 blob %s\tEXTRA\n' $ex;}|$G -C $T/fr mktree)
c2=$(cd $T/fr&&GIT_CONFIG_GLOBAL=$T/c/dg4 GIT_AUTHOR_NAME=dg4 GIT_AUTHOR_EMAIL=dg4@agi GIT_COMMITTER_NAME=dg4 GIT_COMMITTER_EMAIL=dg4@agi $G commit-tree -S -m forged $tr2);$G -C $T/fr update-ref refs/capsule/$CID $c2;$G -C $T/fr bundle create $T/f3.bundle refs/capsule/$CID --not $BASE 2>/dev/null
ok v4-an-unlisted-file-in-a-validly-signed-tree-is-refused '! vt verify $T/f3.bundle >/dev/null 2>$T/v4.err&&grep -qF "[tree]" $T/v4.err'
forge;for w in mal other;do c3=$(cd $T/fr&&GIT_CONFIG_GLOBAL=$T/c/$w GIT_AUTHOR_NAME=$w GIT_AUTHOR_EMAIL=$w@agi GIT_COMMITTER_NAME=$w GIT_COMMITTER_EMAIL=$w@agi $G commit-tree -S -m "by $w" $(git -C $T/fr rev-parse refs/capsule/$CID^{tree}));$G -C $T/fr update-ref refs/capsule/$CID $c3;$G -C $T/fr bundle create $T/f5$w.bundle refs/capsule/$CID --not $BASE 2>/dev/null;done
ok v5-a-key-outside-the-ring-is-refused '! vt verify $T/f5mal.bundle >/dev/null 2>&1'
ok v5b-a-ring-key-that-is-not-the-packer-is-refused '! vt verify $T/f5other.bundle >/dev/null 2>&1'
ok v6-an-attach-mint-absent-on-the-target-is-rc-3 'TRK=$(printf "" | $G -C $T/t.git commit-tree -m none $($G -C $T/t.git mktree </dev/null)) vt verify $T/c.bundle >/dev/null 2>$T/v6.err;[ $? = 3 ]&&grep -qF "[attach-absent]" $T/v6.err'
ok v7-the-in-place-form-verifies-the-source-ref "(cd $T/r&&AGI_TRUNK=HEAD AGI_ALLOWED=$T/allowed sh $CAPSULE verify $CID)"
mut 's/die 4 "\[sig\] /true 4 "[sig] /' v;cp $T/mut $T/m-sig;mut 's/die 4 "\[heads\] the bundle/true 4 "[heads] the bundle/' v;cp $T/mut $T/m-heads;mut 's/die 4 "\[tree\] \$2/true 4 "[tree] $2/' v;cp $T/mut $T/m-tree
ok v2-mutant-RED-without-the-signature-check-a-forged-manifest-passes 'PIECE=$T/m-sig vt verify $T/f1.bundle >/dev/null 2>&1'
ok v3-mutant-RED-without-the-heads-check-a-swapped-ref-passes 'PIECE=$T/m-heads vt verify $T/f2.bundle >/dev/null 2>&1'
ok v4-mutant-RED-without-the-tree-check-an-unlisted-file-passes 'PIECE=$T/m-tree vt verify $T/f3.bundle >/dev/null 2>&1'
# --- I: in
new t2;it(){ (cd $T/t2.git&&AGI_ALLOWED=$T/allowed AGI_TRUNK=refs/heads/main sh ${PIECE:-$CAPSULE} "$@");}
ok i0-in-lands-the-capsule-and-exactly-the-listed-refs 'it in $T/p.bundle&&[ "$($G -C $T/t2.git for-each-ref --format="%(objectname) %(refname)" refs/capsule refs/box refs/held refs/heads/posts|sort)" = "$({ echo "$($G -C $T/r rev-parse refs/capsule/$PC) refs/capsule/$PC";echo "$PM"|sed -n "s/^ref \(.*\) \(.*\)/\2 \1/p";}|sort)" ]'
ok i0b-in-twice-is-idempotent 's0=$(snap $T/t2.git);it in $T/p.bundle&&[ "$s0" = "$(snap $T/t2.git)" ]'
# atomic (refs, not bytes: a fetch leaves unreachable objects and FETCH_HEAD): one non-ff ref (the target holds a diverged refs/held/p/x) -> nothing moves; the mutant without --atomic advances a sibling
atom(){ new ta;$G -C $T/ta.git update-ref refs/held/p/x $($G -C $T/ta.git commit-tree -m diverged $($G -C $T/ta.git rev-parse $BASE^{tree}));s0=$($G -C $T/ta.git for-each-ref);(cd $T/ta.git&&AGI_ALLOWED=$T/allowed AGI_TRUNK=refs/heads/main sh $1 in $T/p.bundle >/dev/null 2>&1);ra=$?;[ $ra != 0 ]&&[ "$s0" = "$($G -C $T/ta.git for-each-ref)" ]&&! $G -C $T/ta.git rev-parse -q --verify refs/capsule/$PC >/dev/null;ra=$?;rm -rf $T/ta.git;return $ra;}
ok i1-atomic-one-non-ff-ref-moves-nothing 'atom $CAPSULE'
mut 's/echo "update \$r \$n \${o:-\$Z}">>\$s\/u/git update-ref $r $n ${o:-$Z}/' i;ok i1-mutant-RED-applied-one-by-one-a-sibling-advances-before-the-non-ff-ref-is-seen '! atom $T/mut'
mut 's/||git merge-base --is-ancestor \$o \$n||echo "\[non-ff\] \$r">>\$s\/e//' i;ok i1b-mutant-RED-without-the-non-ff-check-the-held-ref-is-clobbered '! atom $T/mut'

ok i2-in-refuses-a-tampered-bundle-and-moves-nothing 'new tb;s0=$(snap $T/tb.git);! (cd $T/tb.git&&AGI_ALLOWED=$T/allowed AGI_TRUNK=refs/heads/main sh $CAPSULE in $T/f2.bundle >/dev/null 2>&1)&&[ "$s0" = "$(snap $T/tb.git)" ]'
ok i3-in-needs-a-file '! it in $CID >/dev/null 2>&1'
# --- R: regrow (REGROW 1a files, 1b refs) and repoint (R1 parent, R2 absent mint)
cap dg4 $T/r pack $M1 subtree $M1 >$T/g.cid 2>/dev/null;GC=$(cat $T/g.cid);cap dg4 $T/r out $GC >$T/g.bundle;new t4;(cd $T/t4.git&&AGI_ALLOWED=$T/allowed AGI_TRUNK=refs/heads/main sh $CAPSULE in $T/g.bundle)
rg(){ rm -rf $T/rg;(cd $T/t4.git&&AGI_ALLOWED=$T/allowed AGI_TRUNK=refs/heads/main sh $1 regrow $GC $T/rg);}
files(){ $G -C $T/r show refs/capsule/$GC:MANIFEST|sed -n 's/^member [0-9a-f]* //p'|sort;}
same(){ [ "$(cd $T/rg&&find . -type f|sed 's|^\./||'|sort)" = "$({ files;echo MANIFEST;}|sort)" ]&&for x in $(files);do $G -C $T/r show $BASE:$x|cmp -s - $T/rg/$x||return 1;done;}
ok g1-regrow-1a-equals-the-slice-byte-for-byte-deprecated-members-included 'rg $CAPSULE&&same&&files|grep -q "deprecated/goal/dep.md"&&[ -f $T/rg/src/f.py ]'
mut 's/git archive refs\/capsule\/\$1/git archive $T/' g;ok g1-mutant-RED-regrow-of-the-wrong-rev-is-not-the-slice '! { rg $T/mut&&same;}'
ok g1b-regrow-refuses-a-capsule-that-does-not-verify '! (cd $T/r&&AGI_ALLOWED=$T/mal-none AGI_TRUNK=HEAD sh $CAPSULE regrow $GC $T/rg2 >/dev/null 2>&1)&&[ ! -e $T/rg2 ]'
GG=$(cap dg4 $T/r pack $M1 post p --ref "refs/grid/*" 2>/dev/null);cap dg4 $T/r out $GG >$T/gg.bundle;new t5;(cd $T/t5.git&&AGI_ALLOWED=$T/allowed AGI_TRUNK=refs/heads/main sh $CAPSULE in $T/gg.bundle)
ok g2-regrow-1b-refs-after-in-equal-the-ref-lines-none-missing-none-extra '[ "$($G -C $T/t5.git for-each-ref --format="%(objectname) %(refname)"|grep -v " refs/heads/main$"|sort)" = "$({ echo "$($G -C $T/r rev-parse refs/capsule/$GG) refs/capsule/$GG";$G -C $T/r show refs/capsule/$GG:MANIFEST|sed -n "s/^ref \(.*\) \(.*\)/\2 \1/p";}|sort)" ]&&$G -C $T/r show refs/capsule/$GG:MANIFEST|grep -q "^ref refs/grid/n1 "'
ok g3-the-carrier-writes-the-grid-ref-it-carries-without-a-writer-of-its-own '! grep -n "update-ref refs/grid\|refs/grid/" $CAPSULE | grep -q .'
o0=$($G -C $T/r rev-parse refs/capsule/$GC);N1=$(cap dg4 $T/r repoint $GC $M2 2>$T/rp.err);rp=$?
$G -C $T/r show $o0:MANIFEST>$T/mo;$G -C $T/r show $N1:MANIFEST>$T/mn
ok r1-the-old-tip-is-the-new-tips-parent-and-only-attach-differs '[ $rp = 0 ]&&[ "$($G -C $T/r rev-parse refs/capsule/$GC)" = "$N1" ]&&[ "$($G -C $T/r rev-parse $N1^)" = "$o0" ]&&[ "$(diff $T/mo $T/mn|grep -c "^[<>]")" = 2 ]&&$G -C $T/r show $N1:MANIFEST|grep -qx "attach $M2"'
ok r1b-the-repointed-capsule-verifies-and-its-history-is-two-commits '(cd $T/r&&AGI_TRUNK=HEAD AGI_ALLOWED=$T/allowed sh $CAPSULE verify $GC)&&[ "$($G -C $T/r rev-list --count refs/capsule/$GC)" = 2 ]'
cap dg4 $T/r repoint $GC 00000000000000000000000000000000 >/dev/null 2>$T/rp2.err;rp2=$?;t1=$($G -C $T/r rev-parse refs/capsule/$GC)
ok r2-an-absent-mint-is-rc-3-and-the-tip-does-not-move '[ $rp2 = 3 ]&&grep -qF "[attach-absent]" $T/rp2.err&&[ "$t1" = "$N1" ]'
cap other $T/r repoint $GC $M3 >/dev/null 2>$T/rp3.err;rp3=$?
ok r3-only-the-packer-repoints '[ $rp3 = 2 ]&&grep -qF "[packer]" $T/rp3.err&&[ "$($G -C $T/r rev-parse refs/capsule/$GC)" = "$N1" ]'
cap dg4 $T/r out $GC >$T/g2.bundle;ok r4-in-takes-the-repoint-as-a-fast-forward '(cd $T/t4.git&&AGI_ALLOWED=$T/allowed AGI_TRUNK=refs/heads/main sh $CAPSULE in $T/g2.bundle)&&[ "$($G -C $T/t4.git rev-parse refs/capsule/$GC)" = "$N1" ]'
# a signed child that changes a MEMBER (not attach) is refused by the chain rule; the mutant without it takes it
forge;cm=$($G -C $T/fr rev-parse refs/capsule/$GC:src/f.py);ex2=$(echo 'print(2)'|$G -C $T/fr hash-object -w --stdin);tr3=$($G -C $T/fr ls-tree refs/capsule/$GC|sed "s/$cm/$ex2/"|$G -C $T/fr mktree)
c4=$(cd $T/fr&&GIT_CONFIG_GLOBAL=$T/c/dg4 GIT_AUTHOR_NAME=dg4 GIT_AUTHOR_EMAIL=dg4@agi GIT_COMMITTER_NAME=dg4 GIT_COMMITTER_EMAIL=dg4@agi $G commit-tree -S -p refs/capsule/$GC -m "member swapped" $tr3);$G -C $T/fr update-ref refs/capsule/$GC $c4;$G -C $T/fr bundle create $T/f6.bundle refs/capsule/$GC 2>/dev/null
ok r5-a-signed-child-that-changes-a-member-is-refused '! vt verify $T/f6.bundle >/dev/null 2>$T/r5.err&&grep -qF "[tree]" $T/r5.err'
mut 's/die 4 "\[tree\] \$x differs/true 4 "[tree] $x differs/' r;ok r5-mutant-RED-without-the-chain-rule-the-member-swap-passes 'PIECE=$T/mut vt verify $T/f6.bundle >/dev/null 2>&1'
# --- L: the LANDING lane (goal .44.3): verify EVERY refs/capsule/* of a repo; a capsule ref is create-only, so a count below CAPSULE_FLOOR is RED too.
# the gate runs it on the real repo: LANDING_REPO=<repo> LAND_TRUNK=<ref> LAND_ALLOWED=<ring file, default /var/lib/agi/allowed_signers> CAPSULE_FLOOR=<count at the last landing> sh capsule.t.sh (the fixture rows ignore them)
land(){ n=0;b=0;for r in $($G -C $1 for-each-ref --format='%(refname)' refs/capsule);do n=$((n+1));(cd $1&&AGI_ALLOWED=${3:-/var/lib/agi/allowed_signers} AGI_TRUNK=${2:-HEAD} sh ${PIECE:-$CAPSULE} verify ${r#refs/capsule/}>/dev/null 2>&1)||b=$((b+1));done;LN=$n;LB=$b;[ $b = 0 ]&&[ $n -ge ${CAPSULE_FLOOR:-0} ];}
nc=$($G -C $T/r for-each-ref refs/capsule|wc -l|tr -d ' ')
ok l1-the-landing-lane-passes-over-every-capsule-ref 'CAPSULE_FLOOR=$nc land $T/r HEAD $T/allowed&&[ "$LN" = "$nc" ]&&[ "$nc" -ge 4 ]'
ok l2-a-capsule-ref-gone-is-a-count-drop-and-RED '! CAPSULE_FLOOR=$((nc+1)) land $T/r HEAD $T/allowed&&[ "$LB" = 0 ]'
rm -rf $T/lr;$G clone -q --no-local $T/r $T/lr;$G -C $T/lr fetch -q $T/r "refs/capsule/*:refs/capsule/*";lc=$($G -C $T/lr for-each-ref --format="%(refname)" refs/capsule|head -1)
$G -C $T/lr update-ref $lc "$($G -C $T/lr commit-tree -m forced $($G -C $T/lr rev-parse $lc^{tree}))"
ok l3-a-tip-force-moved-to-an-unsigned-commit-is-RED '! CAPSULE_FLOOR=$nc land $T/lr HEAD $T/allowed&&[ "$LB" = 1 ]'
[ -z "$LANDING_REPO" ]||ok l4-the-real-repo "CAPSULE_FLOOR=${CAPSULE_FLOOR:-0} land $LANDING_REPO ${LAND_TRUNK:-HEAD} ${LAND_ALLOWED:-/var/lib/agi/allowed_signers}"
# last: this mutant really re-points the capsule to an absent mint
mut 's/;at \$a||die 3 "\[attach-absent\] \$a";o=/;o=/' r;ok r2-mutant-RED-without-the-attach-check-an-absent-mint-is-taken '! { PIECE=$T/mut cap dg4 $T/r repoint $GC 00000000000000000000000000000000 >/dev/null 2>&1; test $? = 3;}'
echo "capsule: $f FAIL"
exit $f
