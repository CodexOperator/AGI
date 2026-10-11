S=$1;K=$S/k;G=.agi/nodes/.geometry;export AGI_CKPT=$S/ckpt;rm -rf $S/r3;git init -q $S/r3;cd $S/r3;git config user.name t;git config user.email t@t;git config gpg.format ssh;mkdir -p $G .agi/context/schemas .agi/nodes/doc
pk(){ cut -d' ' -f1,2 $K/$1.pub; }
h='"harness": "claude-code"'
printf -- "---\nring: [sanctuary-master]\n---\n  - {\"name\": \"belam\", \"parent\": \"owner\", $h}\n  - {\"name\": \"council\", \"parent\": \"belam\"}\n  - {\"name\": \"keep\", \"parent\": \"belam\"}\n  - {\"name\": \"alive\", \"parent\": \"council\", $h}\n  - {\"name\": \"all-is-one\", \"parent\": \"council\", $h}\n  - {\"name\": \"sanctuary-master\", \"parent\": \"keep\", $h}\n  - {\"name\": \"director-general-1\", \"parent\": \"sanctuary-master\", $h}\n  - {\"name\": \"director-general-2\", \"parent\": \"sanctuary-master\", $h}\n">$G/posts.md
printf 'owner cert-authority %s\nowner %s\nbelam %s\nalive %s\nall-is-one %s\nsanctuary-master %s\ndirector-general-1 %s\ndirector-general-2 %s\n' "$(pk ca)" "$(pk ca)" "$(pk belam1)" "$(pk alive1)" "$(pk aio1)" "$(pk sm1)" "$(pk dg1)" "$(pk dg2)">$G/ring
echo s>.agi/context/schemas/s.md;git add -A;git -c user.signingKey=$K/belam1.pub commit -q -S -m genesis;git branch -f trunk HEAD;git checkout -q --detach trunk
cm(){ k=$1;m=$2;shift 2;mkdir -p .agi/nodes/doc;sh -c "$*";git add -A;git -c user.signingKey=$K/$k commit -q -S -m "$m" --allow-empty; }
case_(){ n=$1; want=$2; o=$(sh $S/ring-gate trunk HEAD 2>&1); rc=$?; v=$([ $rc = 0 ] && echo ADMIT || echo REFUSE); [ $v = $want ] && r=PASS || r=FAIL; printf '%-4s %-6s %-70s %s\n' $r $v "$n" "$(echo $o|sed 's/[0-9a-f]\{40\}/<c>/'|cut -c1-70)"; [ $rc = 0 ] && [ "$3" != keep-out ] && git branch -f trunk HEAD; git checkout -q --detach trunk; }
# mk NAME TIP TIME [parents-of-ref ...] -- post:keyfile ...   (a lane fixture writes a block exactly so)
mk(){ nm=$1;x=$(git rev-parse $2);y=$3;shift 3;pp=;while [ "$1" != -- ];do pp="$pp -p $(git rev-parse refs/agi/block/$1)";shift;done;shift;H=${MKH:-sha256};i=$(mktemp);j=0
 for a in "$@";do j=$((j+1));p=${a%%:*};f=${a#*:};b=$(AGI_HASH=$H sh $S/ckpt sign $p $K/$f $x $y|git hash-object -w --stdin);printf '100644 blob %s\t%s.%s\n' $b $p $j;done>$i
 st=$(git mktree<$i);hb=$(echo "$H $(git archive --format=tar $x|${H}sum|cut -d' ' -f1)"|git hash-object -w --stdin)
 tr=$(printf '100644 blob %s\thash\n040000 tree %s\tsigs\n100644 blob %s\ttime\n100644 blob %s\ttip\n' $hb $st $(echo $y|git hash-object -w --stdin) $(echo $x|git hash-object -w --stdin)|git mktree)
 git update-ref refs/agi/block/$nm $(echo "block $nm"|git commit-tree $tr $pp);rm $i; }
holds(){ sh $S/ckpt check|grep -q " $(git rev-parse refs/agi/block/$1)$"&&echo HOLDS||echo NO; }
bk(){ n=$1;want=$2;v=$(holds $3);[ $v = $want ]&&r=PASS||r=FAIL;printf '%-4s %-6s %s\n' $r $v "$n"; }
now=$(date +%s)
# --- LAYERS: who may seal together (levels: belam 1 · alive, all-is-one, SM 2 · DG1 DG2 3 · owner 0)
mk L3 trunk $now -- director-general-1:dg1 director-general-2:dg2;   bk "L1 DG1 + DG2 (level 3 among themselves)" HOLDS L3
mk L23 trunk $now L3 -- sanctuary-master:sm1 director-general-1:dg1; bk "L2 SM + DG1 (levels 2+3), sealing L3" HOLDS L23
mk L2 trunk $now L23 -- alive:alive1 all-is-one:aio1 sanctuary-master:sm1; bk "L3 council + SM (level 2), sealing L23" HOLDS L2
mk BAD1 trunk $now -- belam:belam1 director-general-1:dg1;          bk "L4 belam + DG1 (levels 1 and 3: two apart)" NO BAD1
mk L1 trunk $now L2 -- belam:belam1 alive:alive1;                   bk "L5 the rare top: belam + level 2, sealing L2 (DGs in it transitively)" HOLDS L1
mk L0 trunk $now L1 -- owner:ca belam:belam1;                       bk "L6 the anchor block: owner (the CA itself) + belam" HOLDS L0
mk BAD2 trunk $now -- owner:ca alive:alive1;                        bk "L7 owner + alive (levels 0 and 2)" NO BAD2
mk BAD3 trunk $now -- director-general-1:dg1;                       bk "L8 one signer (k = 2)" NO BAD3
for b in BAD1 BAD2 BAD3;do git update-ref -d refs/agi/block/$b;done
# --- TIME: grace + seal (blocks above)
cm dg1.pub h1 "sed -i 's|^director-general-1 .*|director-general-1 $(pk dg1b)|' $G/ring"; case_ "T1 DG1 gen1 hands off to gen2" ADMIT
cm dg1.pub a "echo a>>.agi/nodes/doc/y.md"; case_ "T2 retired DG1 gen1: no holding block contains the handoff yet (GRACE)" ADMIT keep-out
mk L3b trunk $now L3 -- director-general-1:dg1b director-general-2:dg2; bk "T3 the next level-3 block over the handoff tip (DG1 gen2 + DG2)" HOLDS L3b
mk L3x trunk $now L3 -- director-general-1:dg1 director-general-2:dg2;  bk "T4 a block the RETIRED gen1 signs over that tip" NO L3x; git update-ref -d refs/agi/block/L3x
cm dg1.pub b "echo b>>.agi/nodes/doc/y.md"; case_ "T5 retired gen1 once the LOWEST block (level 3) seals its handoff" REFUSE
D=$(date -d '-1 day' -R); mkdir -p .agi/nodes/doc; echo c>>.agi/nodes/doc/y.md; git add -A; GIT_COMMITTER_DATE="$D" GIT_AUTHOR_DATE="$D" git -c user.signingKey=$K/dg1.pub commit -q -S -m bd; case_ "T6 the same, BACKDATED a day" REFUSE
cm dg1b.pub d "echo d>>.agi/nodes/doc/y.md"; case_ "T7 DG1 gen2 plain edit" ADMIT
mk ORD trunk $now L3b -- director-general-1:dg1b director-general-2:dg2; git update-ref refs/agi/block/ORD2 $(git cat-file commit refs/agi/block/L3|sed '/^parent/d'|git hash-object -t commit -w --stdin); 
o=$(git rev-parse refs/agi/block/ORD2);t2=$(git cat-file commit $o|git hash-object -t commit -w --stdin);:
mk OLD $(git rev-parse trunk~3) $now ORD -- director-general-1:dg1 director-general-2:dg2; bk "T8 a block over an OLDER tip than the block it seals" NO OLD; for b in ORD ORD2 OLD;do git update-ref -d refs/agi/block/$b;done
cd $K;rm -f bx*;cp belam1 bx;cp belam1.pub bx.pub;ssh-keygen -q -s ca -I w-old -n owner@agi -V -3h:-2h -z 31 bx.pub;rm -f by*;cp belam1 by;cp belam1.pub by.pub;ssh-keygen -q -s ca -I w-now -n owner@agi -V -1m:+30m -z 32 by.pub;cd $S/r3
D=$(date -d '-150 min' -R); echo e>>.agi/context/schemas/s.md; git add -A; GIT_COMMITTER_DATE="$D" GIT_AUTHOR_DATE="$D" git -c user.signingKey=$K/bx-cert.pub commit -q -S -m old; case_ "T9 owner cert expired before the newest block's time, backdated" REFUSE
cm by-cert.pub f "echo f>>.agi/context/schemas/s.md"; case_ "T10 owner cert valid at that time" ADMIT keep-out
# --- ESCALATION through posts.md (alive 02:55Z)
cm sm1.pub e1 "sed -i 's|\"name\": \"belam\", \"parent\": \"owner\"|\"name\": \"belam\", \"parent\": \"sanctuary-master\"|' $G/posts.md"; case_ "E1 SM (posts.md ring member) re-parents belam under itself" REFUSE
cm sm1.pub e2 "sed -i 's|\"name\": \"director-general-2\", \"parent\": \"sanctuary-master\"|\"name\": \"director-general-2\", \"parent\": \"director-general-1\"|' $G/posts.md"; case_ "E2 SM moves DG2 under DG1 (inside its own subtree)" ADMIT keep-out
cm sm1.pub e3 "sed -i 's|\"name\": \"director-general-2\", \"parent\": \"sanctuary-master\"|\"name\": \"director-general-2\", \"parent\": \"keep\"|' $G/posts.md"; case_ "E3 SM moves DG2 out to keep (above SM)" REFUSE
cm belam1.pub e4 "sed -i 's|\"name\": \"director-general-2\", \"parent\": \"sanctuary-master\"|\"name\": \"director-general-2\", \"parent\": \"keep\"|' $G/posts.md"; case_ "E4 belam does the same move" ADMIT keep-out
cm sm1.pub e5 "sed -i 's|\"model\"|\"model\"|;s|\"name\": \"director-general-1\", \"parent\": \"sanctuary-master\", |&\"tier\": 3, |' $G/posts.md"; case_ "E5 SM edits a non-tree cell (tier) on DG1's row" ADMIT keep-out
cm dg1b.pub e6 "sed -i 's|\"name\": \"director-general-1\", \"parent\": \"sanctuary-master\", |&\"tier\": 3, |' $G/posts.md"; case_ "E6 DG1 edits its own row (posts.md ring = [SM])" REFUSE
cm sm1.pub e7 "echo '  - {\"name\": \"director-general-9\", \"parent\": \"sanctuary-master\", $h}' >> $G/posts.md"; case_ "E7 SM stands up DG9 under itself" ADMIT keep-out
cm sm1.pub e8 "echo '  - {\"name\": \"director-general-9\", \"parent\": \"belam\", $h}' >> $G/posts.md"; case_ "E8 SM stands up a row under belam" REFUSE
# --- ALGORITHMS on blocks
export AGI_SIGN="ED25519 ECDSA"
bk "H1 hybrid cell: the ed25519-only level-3 block" NO L3b
printf 'director-general-1 %s\ndirector-general-2 %s\n' "$(pk dg1pq)" "$(pk dg2pq)" >> $G/ring; git add -A; git -c user.signingKey=$K/sm1.pub commit -q -S -m pqcol; sh $S/ring-gate trunk HEAD >/dev/null && git branch -f trunk HEAD
mk HY trunk $now L3b -- director-general-1:dg1b director-general-1:dg1pq director-general-2:dg2 director-general-2:dg2pq; bk "H2 hybrid: DG1 + DG2 in both columns" HOLDS HY
mk HY2 trunk $now L3b -- director-general-1:dg1b director-general-1:dg1pq director-general-2:dg2; bk "H3 hybrid: DG2 missing its 2nd column" NO HY2
unset AGI_SIGN
MKH=sha512 mk HS trunk $now L3b -- director-general-1:dg1b director-general-2:dg2; bk "H4 a block naming sha512" HOLDS HS
AGI_HASHES=sha256 bk "H5 sha512 dropped from AGI_HASHES" NO HS
