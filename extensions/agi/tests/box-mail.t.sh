#!/bin/sh
# box-mail.t.sh: AA1.M falsifiers for the trunk's `box` piece (hypotheses g716111-aa1m-box-send-..., ...-no-worktree-hop-...): sh + git + jq, scratch only,
# throwaway keys, no live ref. One ok/FAIL line per case; exit = number of FAILs. The file under test is the PIECE: `sect box` from the .geometry engine*.md of ROOT
# (default: the working tree this file sits in), exactly as box-carry.t.sh reads its pieces; case b0 pins that the box under test IS that piece, byte for byte.
# BOX=<file>  a box to test instead (b0 then FAILs unless it is byte-equal to the piece); ROOT=<repo> where the piece is read; CEIL=<bytes> the piece's size ceiling (default 2005)
# BRSED=<sed script> scratch knob: mutate the box under test (b0 goes RED by design: how the cap numbers on experiment:dg2-aa1m-m3 were measured). To prove a PIECE edit turns a case RED,
#   run on a scratch ROOT whose engine-post.md carries the edit.
# M3M/M3RUNS = sends per writer / runs for the realistic M3 cases (default 100/5); M3BM/M3BRUNS the same for the 6-on-one-ref BOUND (150/3)
# The fixture rows follow the piece's rule: THE LEVEL RULE (owner 19:5xZ, belam 20:0xZ; a() = |level(a)-level(b)| <= 1, level = count of non-inert rows up to owner).
# The no-retry mutation (c3) is derived FROM THE PIECE (its retry cap cut to 1 attempt), never from a doc.
T=$(mktemp -d);trap 'rm -rf $T' 0;f=0;G=/usr/bin/git;R0=${ROOT:-$(cd "$(dirname "$0")/../../.." && pwd)}
sect(){ cat $R0/.agi/nodes/.geometry/engine*.md|sed -n "/^###* $1 /,/^###* /{/^~~~/,/^~~~/{//!p}}";}
[ -n "$BOX" ]||{ sect box>$T/box;BOX=$T/box;}
[ -s $BOX ]||{ echo "FAIL extract: box $(wc -c<$BOX)";exit 99;}
[ -n "$BRSED" ]&&{ sed "$BRSED" $BOX>$T/boxm;BOX=$T/boxm;}
BR=$BOX;CEIL=${CEIL:-2005}
sed 's/\[ \$k -lt 5 \]/[ $k -lt 1 ]/' $BR>$T/box1
# keys + signers + per-post git config + a repo whose trunk (HEAD) holds the fixture matrix
mkdir $T/k $T/c;: >$T/signers
for u in belam sm alive dg5 dg1 dg2 dg3 all-is-one sp tm dt1 dg4;do
 ssh-keygen -q -t ed25519 -N '' -f $T/k/$u -C $u>/dev/null
 echo "$u@agi namespaces=\"git\" $(cut -d' ' -f1,2 $T/k/$u.pub)">>$T/signers
 printf '[user]\n\tname=%s\n\temail=%s@agi\n\tsigningkey=%s\n[gpg]\n\tformat=ssh\n[gpg "ssh"]\n\tallowedSignersFile=%s\n[commit]\n\tgpgsign=false\n' $u $u $T/k/$u $T/signers>$T/c/$u
done
$G init -q $T/r;mkdir -p $T/r/.agi/nodes/.geometry
cat >$T/r/.agi/nodes/.geometry/posts.md<<'EOF'
  - {"name":"belam","parent":"owner","harness":"claude"}
  - {"name":"council","parent":"belam","members":["alive","all-is-one","sp","dg5"]}
  - {"name":"keep","parent":"belam","members":["sm","tm"]}
  - {"name":"alive","parent":"council","harness":"claude"}
  - {"name":"all-is-one","parent":"council","harness":"claude"}
  - {"name":"sp","parent":"council","harness":"claude"}
  - {"name":"dg5","parent":"council","harness":"claude"}
  - {"name":"sm","parent":"keep","harness":"claude"}
  - {"name":"tm","parent":"keep","harness":"claude"}
  - {"name":"dg1","parent":"sm","harness":"claude"}
  - {"name":"dg2","parent":"sm","harness":"claude"}
  - {"name":"dg3","parent":"sm","harness":"claude"}
  - {"name":"dt1","parent":"tm","harness":"claude"}
  - {"name":"dg4","parent":null,"harness":"claude"}
EOF
$G -C $T/r add -A;$G -C $T/r -c user.name=x -c user.email=x@x commit -qm fixture
# as U SCRIPT ARGS...: run the box script as post U in the scratch repo (dash, like #!/bin/sh)
as(){ u=$1;s=$2;shift 2;(cd $T/r&&AGI_POST=$u AGI_TRUNK=HEAD GIT_CONFIG_GLOBAL=$T/c/$u GIT_CONFIG_SYSTEM=/dev/null sh $s "$@");}
ok(){ if eval "$2";then echo "ok $1";else echo "FAIL $1";f=$((f+1));fi;}
cnt(){ grep -c "$1" "$2" 2>/dev/null||true;}

# --- b0: the box under test IS the trunk piece, byte for byte (an edit to the piece can never pass unseen)
ok b0 '[ "$(md5sum<$BR)" = "$(sect box|md5sum)" ]'
# --- sanity: the retry build is the box whole with a different send arm only
ok sane-b1 '[ "$(echo order1|as belam $BR send alive;as alive $BR n|wc -l)" = 1 ]&&as alive $BR read|grep -qF "[belam] order1"&&[ "$(as alive $BR n|wc -l)" = 0 ]'

# --- c1: 2 senders x 100 to one reader that reads the whole time = 200/200, 0 dup, 0 refused, per-sender order kept
N=100;: >$T/c1.out;rm -f $T/done
(while [ ! -e $T/done ];do as alive $BR read>>$T/c1.out 2>&1;done)&R=$!
pids=;for s in belam sm;do (i=1;while [ $i -le $N ];do echo "$s $i"|as $s $BR send alive 2>>$T/c1.err||echo "unsent $s $i">>$T/c1.err;i=$((i+1));done)&pids="$pids $!";done
wait $pids;touch $T/done;wait $R;as alive $BR read>>$T/c1.out 2>&1
d=$(grep -c '^\[\(belam\|sm\)\] ' $T/c1.out);u=$(grep '^\[\(belam\|sm\)\] ' $T/c1.out|sort|uniq -d|wc -l);x=$(grep -c '^\[refused\]\|^\[off-matrix\]' $T/c1.out)
o=$(for s in belam sm;do grep "^\[$s\] " $T/c1.out|awk '{print $3}'|awk 'NR>1&&$1!=p+1{b=1}{p=$1}END{print b+0}';done|awk '{t+=$1}END{print t+0}')
echo "# c1 delivered=$d dup=$u refused=$x out_of_order=$o stderr=$(wc -c<$T/c1.err 2>/dev/null||echo 0)B"
ok c1-delivered '[ $d = $((2*N)) ]'
ok c1-no-dup '[ $u = 0 ]'
ok c1-no-refused '[ $x = 0 ]'
ok c1-order '[ $o = 0 ]'
ok c1-held-moved '[ "$(as alive $BR n|wc -l)" = 0 ]'

# --- c2/c3: 2 writers on the SAME channel (two sessions of belam) x 50: with the retry 100/100, 0 stderr; without it split, 0 silent
two(){ v=$1;o=$2;e=$3;n=50;rm -f $o $e;$G -C $T/r update-ref -d refs/box/belam/dg5 2>/dev/null
 for w in a b;do (i=1;while [ $i -le $n ];do echo "$w $i"|as belam $v send dg5 2>>$e;i=$((i+1));done)&done;wait
 as dg5 $BR read>$o 2>&1;}
two $BR $T/c2.out $T/c2.err;d=$(grep -c '^\[belam\] ' $T/c2.out);e=$(wc -c<$T/c2.err)
echo "# c2 (retry) delivered=$d stderr=${e}B";ok c2-retry-100of100 '[ $d = 100 ]';ok c2-retry-0-stderr '[ $e = 0 ]'
# the mutation: the piece with its retry cap cut to ONE attempt: the same case must split, loudly ([unsent]), never silently
sp=0;for t in 1 2 3;do two $T/box1 $T/c3.out $T/c3.err;d=$(grep -c '^\[belam\] ' $T/c3.out);l=$(grep -c '^\[unsent\]' $T/c3.err);echo "# c3 try $t (no retry) delivered=$d reported=$l";[ $d -gt 0 ]&&[ $d -lt 100 ]&&sp=1;[ $((d+l)) = 100 ]||break;done
ok c3-mutation-splits '[ $sp = 1 ]'
ok c3-mutation-0-silent '[ $((d+l)) = 100 ]'

# --- c4/c5: a squatted tip stops at once (rc 1, no update-ref, tip unchanged); a 5x lost race prints [unsent] after exactly 5 tries
mkdir $T/shim;cat >$T/shim/git<<EOF
#!/bin/sh
if [ "\$1" = update-ref ]&&case "\$2" in refs/box/*)true;;*)false;;esac;then echo x>>$T/ur;[ -n "\$FAILCAS" ]&&{ echo "fatal: cannot lock ref '\$2': is at other but expected" >&2;exit 1;};fi
exec $G "\$@"
EOF
chmod +x $T/shim/git
# dash has no <<<: build the squat commit portably
sq=$(cd $T/r&&echo squat|AGI_POST=dg5 AGI_TRUNK=HEAD GIT_CONFIG_GLOBAL=$T/c/dg5 GIT_CONFIG_SYSTEM=/dev/null GIT_AUTHOR_EMAIL=dg5@agi GIT_COMMITTER_EMAIL=dg5@agi $G commit-tree -S $($G hash-object -w -t tree /dev/null))
$G -C $T/r update-ref -d refs/box/belam/sm 2>/dev/null;$G -C $T/r update-ref refs/box/belam/sm $sq
: >$T/ur;echo hi|PATH=$T/shim:$PATH as belam $BR send sm 2>$T/sq.err;rc=$?
ok c4-squat-rc1 '[ $rc = 1 ]'
ok c4-squat-message 'grep -q "^\[squatted\] refs/box/belam/sm" $T/sq.err'
ok c4-squat-tip-unchanged '[ "$($G -C $T/r rev-parse refs/box/belam/sm)" = $sq ]'
ok c4-squat-never-retried '[ ! -s $T/ur ]'
$G -C $T/r update-ref -d refs/box/belam/sm;: >$T/ur;echo hi|FAILCAS=1 PATH=$T/shim:$PATH as belam $BR send sm 2>$T/un.err;rc=$?
ok c5-unsent-rc1 '[ $rc = 1 ]'
ok c5-unsent-message 'grep -q "^\[unsent\] refs/box/belam/sm" $T/un.err'
ok c5-exactly-5-tries '[ "$(wc -l<$T/ur)" = 5 ]'
ok c5-no-tip '! $G -C $T/r rev-parse -q --verify refs/box/belam/sm>/dev/null'

# --- M3 (hypothesis ...-no-worktree-hop-and-the-g1-40-lost-append-cannot-happen): the g1.40 harness mapped onto box. g1.40's 6 writers all
# appended to ONE shared inbox file; box has one ref per (sender, channel), so the FAITHFUL mapping is DISTINCT senders to one recipient
# (+ 2 sessions of one post on one channel), each against a reader looping the whole time + a final read (DG1's correction 10-02 19:16Z).
# lost = a send that RETURNED ok and never arrived (silent); unsent = a send that reported [unsent] (the 5x CAS cap), loud, counted apart.
# The strict 6-writers-on-ONE-ref case stays as a labelled BOUND (prints unsent=N, never FAILs on it; silent loss still FAILs).
m3run(){ lb=$1;SS=$2;WPS=$3;MM=$4;NR=$5;TL=0;TU=0;TD=0;TX=0;r=1
 while [ $r -le $NR ];do
  $G -C $T/r for-each-ref --format='%(refname)' refs/box|grep '/alive$'|while read h;do $G -C $T/r update-ref -d $h;done  # every channel INTO alive: no leftovers from an earlier case
  $G -C $T/r for-each-ref --format='%(refname)' refs/held/alive|while read h;do $G -C $T/r update-ref -d $h;done
  rm -f $T/m3.* $T/done;: >$T/m3.out
  (while [ ! -e $T/done ];do as alive $BR read>>$T/m3.out 2>&1;done)&rd=$!
  pids=;for s in $SS;do k=0;while [ $k -lt $WPS ];do (j=0;while [ $j -lt $MM ];do i="$s.$k-$j";if echo "$i"|as $s $BR send alive 2>/dev/null;then echo "$i">>$T/m3.ok.$s$k;else echo "$i">>$T/m3.uns.$s$k;fi;j=$((j+1));done)&pids="$pids $!";k=$((k+1));done;done
  wait $pids;touch $T/done;wait $rd;as alive $BR read>>$T/m3.out 2>&1
  cat $T/m3.ok.* 2>/dev/null|sort>$T/m3.want;grep -o '^\[[a-z0-9]*\] [a-z0-9]*\.[0-9]*-[0-9]*' $T/m3.out|cut -d' ' -f2|sort>$T/m3.seen
  l=$(comm -23 $T/m3.want $T/m3.seen|wc -l);u=$(cat $T/m3.uns.* 2>/dev/null|wc -l);d=$(uniq -d $T/m3.seen|wc -l);x=$(grep -c '^\[refused\]\|^\[off-matrix\]' $T/m3.out)
  echo "# m3 $lb run $r: attempted=$(( $(echo $SS|wc -w)*WPS*MM )) sent_ok=$(wc -l<$T/m3.want) unsent=$u received=$(wc -l<$T/m3.seen) lost=$l dup=$d refused=$x"
  TL=$((TL+l));TU=$((TU+u));TD=$((TD+d));TX=$((TX+x));r=$((r+1));done;}
NR=${M3RUNS:-5};MM=${M3M:-100}
m3run distinct "belam sm dg5" 1 $MM $NR
ok m3-distinct-lost-0-x$NR '[ $TL = 0 ]';ok m3-distinct-unsent-0 '[ $TU = 0 ]';ok m3-distinct-dup-refused-0 '[ $TD = 0 ]&&[ $TX = 0 ]'
m3run overlap "belam sm dg5" 2 $MM $NR
# 2 sessions on one channel can exhaust the 5x CAS cap rarely when the machine is starved (measured: 0 of 3,000 on a quiet box, 2 of 600 = 0.33% at load average 21; always loud, 0 lost): unsent <= 1% is the claim, never silent loss
echo "# m3 overlap unsent=$TU of $((6*MM*NR)) (tolerance 1%)"
ok m3-overlap-lost-0-x$NR '[ $TL = 0 ]';ok m3-overlap-unsent-le-1pct '[ $((TU*100)) -le $((6*MM*NR)) ]';ok m3-overlap-dup-refused-0 '[ $TD = 0 ]&&[ $TX = 0 ]'
m3run bound "belam" 6 ${M3BM:-150} ${M3BRUNS:-3}
echo "# BOUND: 6 writers on ONE ref x ${M3BM:-150}, ${M3BRUNS:-3} runs: unsent=$TU of $((6*${M3BM:-150}*${M3BRUNS:-3})) (loud; the cap-5 build's measured limit, never FAIL; goal g1.40's literal wording, see verdict:dg2-aa1m-m3)"
ok m3-bound-0-silent-loss '[ $TL = 0 ]&&[ $TD = 0 ]&&[ $TX = 0 ]'
# no worktree hop: no file anywhere under the scratch tree is an inbox, and the repo's worktree stayed clean
ok m3-no-inbox-file '[ -z "$(find $T/r -path "*sessions/inbox*" -not -path "*/.git/*" 2>/dev/null)" ]'
ok m3-worktree-clean '[ -z "$($G -C $T/r status --porcelain)" ]'
# a forged or unsigned commit on an IN ref is refused at read, loud, and stays unread (B3)
$G -C $T/r update-ref -d refs/box/belam/dg5 2>/dev/null;$G -C $T/r update-ref -d refs/held/dg5/belam 2>/dev/null
fg=$(cd $T/r&&echo forged|AGI_TRUNK=HEAD GIT_CONFIG_GLOBAL=$T/c/dg5 GIT_CONFIG_SYSTEM=/dev/null GIT_AUTHOR_EMAIL=belam@agi GIT_COMMITTER_EMAIL=belam@agi $G commit-tree -S $($G hash-object -w -t tree /dev/null));$G -C $T/r update-ref refs/box/belam/dg5 $fg
as dg5 $BR read>$T/f1.out 2>&1;ok f1-forged-refused 'grep -q "^\[refused\] belam" $T/f1.out&&! grep -q forged $T/f1.out'
ok f1-forged-stays-unread '[ "$(as dg5 $BR n|wc -l)" = 1 ]'
un=$(cd $T/r&&echo unsigned|GIT_AUTHOR_EMAIL=belam@agi GIT_COMMITTER_EMAIL=belam@agi $G -c user.name=x -c user.email=x@x commit-tree $($G hash-object -w -t tree /dev/null));$G -C $T/r update-ref refs/box/belam/dg5 $un $fg
as dg5 $BR read>$T/f2.out 2>&1;ok f2-unsigned-refused 'grep -q "^\[refused\] belam" $T/f2.out'

# the matrix, ON/OFF through the real send (rc 0 + a ref, or rc 1 + [off-matrix] + no ref); the Q2 rows. 27 cases = alive's 21-case list + the inert rows
mx(){ $G -C $T/r update-ref -d refs/box/$1/$2 2>/dev/null;echo x|as $1 $BR send $2 2>$T/mx.err;rc=$?;h=$($G -C $T/r rev-parse -q --verify refs/box/$1/$2 2>/dev/null)
 if [ "$3" = ON ];then [ $rc = 0 ]&&[ -n "$h" ];else [ $rc = 1 ]&&[ -z "$h" ]&&grep -q '^\[off-matrix\] '"$1 -> $2" $T/mx.err;fi;}
# --- THE LEVEL RULE (owner 19:5xZ, belam 20:0xZ): mail iff |level(a)-level(b)| <= 1, level = count of NON-inert rows up to owner; inert rows (council, keep) send/receive nothing; an unplaced row (no parent chain to owner) is refused both ways; a post never mails itself. Alive's 21 cases on the Q2 rows (belam > council{alive, all-is-one, sp} + keep{sm, tm} > dg1-3 under sm, dt1 under tm; dg5 = a fixture-only council member, dg4 unplaced).
for c in dg1:dg2 dg2:dg1 dg3:dg1 dg1:dt1 dg1:sm sm:dg1 dg1:tm dg1:alive belam:alive alive:belam alive:sm alive:all-is-one sm:tm belam:sm sm:belam;do ok mx-lvl-${c%:*}-${c#*:}-ON "mx ${c%:*} ${c#*:} ON";done
for c in dg1:belam belam:dg1 belam:dt1 alive:council council:alive keep:sm sm:keep dg4:dg1 dg1:dg4 nobody:alive alive:nobody alive:alive;do ok mx-lvl-${c%:*}-${c#*:}-OFF "mx ${c%:*} ${c#*:} OFF";done
# the read side: a validly signed commit from an UNPLACED post is refused at read (the commit is real, the edge is not)
$G -C $T/r update-ref -d refs/box/dg4/dg1 2>/dev/null;$G -C $T/r update-ref -d refs/held/dg1/dg4 2>/dev/null
rv=$(cd $T/r&&echo unplaced|AGI_TRUNK=HEAD GIT_CONFIG_GLOBAL=$T/c/dg4 GIT_CONFIG_SYSTEM=/dev/null GIT_AUTHOR_EMAIL=dg4@agi GIT_COMMITTER_EMAIL=dg4@agi $G commit-tree -S $($G hash-object -w -t tree /dev/null));$G -C $T/r update-ref refs/box/dg4/dg1 $rv
as dg1 $BR read>$T/rv.out 2>&1;ok mx-lvl-read-unplaced-refused 'grep -q "^\[off-matrix\] dg4" $T/rv.out&&! grep -q unplaced $T/rv.out'
# R2: a PLACED pair two levels apart (dg1 is level 3, belam level 1): a validly signed dg1 -> belam commit is refused at belam's read
$G -C $T/r update-ref -d refs/box/dg1/belam 2>/dev/null;$G -C $T/r update-ref -d refs/held/belam/dg1 2>/dev/null
tw=$(cd $T/r&&echo twoapart|AGI_TRUNK=HEAD GIT_CONFIG_GLOBAL=$T/c/dg1 GIT_CONFIG_SYSTEM=/dev/null GIT_AUTHOR_EMAIL=dg1@agi GIT_COMMITTER_EMAIL=dg1@agi $G commit-tree -S $($G hash-object -w -t tree /dev/null));$G -C $T/r update-ref refs/box/dg1/belam $tw
as belam $BR read>$T/tw.out 2>&1;ok mx-lvl-read-two-apart-refused 'grep -q "^\[off-matrix\] dg1" $T/tw.out&&! grep -q twoapart $T/tw.out'

# --- negative: size, no Python, no inbox path
ok n1-bytes-le-ceiling '[ "$(wc -c<$BR)" -le $CEIL ]'
echo "# box (the piece) bytes=$(wc -c<$BR) ceiling=$CEIL"
ok n2-no-python '! grep -qi python $BR'
ok n3-no-inbox-path '! grep -q "sessions/inbox" $BR'
exit $f
