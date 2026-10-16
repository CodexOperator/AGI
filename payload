#!/bin/sh
# box-mail.t.sh: AA1.M falsifiers for the trunk's `box` piece (hypotheses g716111-aa1m-box-send-..., ...-no-worktree-hop-...): sh + git + jq, scratch only,
# throwaway keys, no live ref. One ok/FAIL line per case; exit = number of FAILs. The file under test is the PIECE: `sect box` from the .geometry engine*.md of ROOT
# (default: the working tree this file sits in), exactly as box-carry.t.sh reads its pieces; case b0 pins that the box under test IS that piece, byte for byte.
# BOX=<file>  a box to test instead (b0 then FAILs unless it is byte-equal to the piece); ROOT=<repo> where the piece is read; CEIL=<bytes> the piece's size ceiling (default 2904)
# BRSED=<sed script> scratch knob: mutate the box under test (b0 goes RED by design: how the cap numbers on experiment:dg2-aa1m-m3 were measured). To prove a PIECE edit turns a case RED,
#   run on a scratch ROOT whose engine-post.md carries the edit.
# M3M/M3RUNS = sends per writer / runs for the realistic M3 cases (default 100/5); M3BM/M3BRUNS the same for the 6-on-one-ref BOUND (150/3).
# FIT (goal:g7.16.1.11.11.1.1): the gate kills a lane at 600 s and this one took 475 s at load 1.5, so unless M3M/M3BM are set the m3 sizes follow the box's OWN
#   speed: a 48-send pilot of the overlap shape gives sends/s, and the m3 sizes shrink (bound runs/size first, then the run count down to 2, then sends per writer down to 50 =
#   n >= 300 per overlap run, council 00:08Z: a smaller n makes the P percent line vacuous) so that lane-so-far + pilot + m3 + mutants fit BUDGET_S (270): a COMPARISON against
#   the measured rate, not a wall clock, so load shrinks m3 instead of killing the lane. The chosen sizes are printed. Any of M3M/M3BM/M3RUNS/M3BRUNS set = that size exactly, no fit.
# M3_UNSENT_PCT (5) = the overlap case's tolerance for LOUD [unsent] (the 5-try CAS cap against sign+commit time; 2.33 percent measured solo at low load on 10-12,
#   always lost 0 dup 0): the STRICT rows are lost 0, dup 0, and every unsent LOUD ([unsent] on stderr, counted); the rate row is the cap's regression guard.
# The fixture rows follow the piece's rule: THE LEVEL RULE (owner 19:5xZ, belam 20:0xZ; a() = |level(a)-level(b)| <= 1, level = count of non-inert rows up to owner).
# The no-retry mutation (c3) is derived FROM THE PIECE (its retry cap cut to 1 attempt), never from a doc.
T=$(mktemp -d);trap 'rm -rf $T' 0;f=0;L0=$(date +%s);G=/usr/bin/git;R0=${ROOT:-$(cd "$(dirname "$0")/../../.." && pwd)}
sect(){ cat $R0/.agi/nodes/.geometry/engine*.md|sed -n "/^###* $1 /,/^###* /{/^~~~/,/^~~~/{//!p}}";}
[ -n "$BOX" ]||{ sect box>$T/box;BOX=$T/box;}
[ -s $BOX ]||{ echo "FAIL extract: box $(wc -c<$BOX)";exit 99;}
[ -n "$BRSED" ]&&{ sed "$BRSED" $BOX>$T/boxm;BOX=$T/boxm;}
BR=$BOX;CEIL=${CEIL:-2904};P=${M3_UNSENT_PCT:-5}
sed 's/\[ \$k -lt 5 \]/[ $k -lt 1 ]/' $BR>$T/box1
sed 's/\[unsent\]/[gone]/' $T/box1>$T/boxs   # the silent-unsent mutant: the cap cut to one attempt AND a failed send that does not say [unsent]
# keys + signers + per-post git config + a repo whose trunk (HEAD) holds the fixture matrix
mkdir $T/k $T/c;: >$T/signers
for u in belam sm alive dg5 dg1 dg2 dg3 all-is-one sp tm dt1 dg4;do
 ssh-keygen -q -t ed25519 -N '' -f $T/k/$u -C $u>/dev/null
 echo "$u@agi namespaces=\"git\" $(cut -d' ' -f1,2 $T/k/$u.pub)">>$T/signers
 printf '[user]\n\tname=%s\n\temail=%s@agi\n\tsigningkey=%s\n[gpg]\n\tformat=ssh\n[gpg "ssh"]\n\tallowedSignersFile=%s\n[commit]\n\tgpgsign=false\n' $u $u $T/k/$u $T/signers>$T/c/$u
done
$G init -q $T/r;mkdir -p $T/r/.agi/nodes/.geometry
cat >$T/r/.agi/nodes/.geometry/posts.md<<'EOF'
  - {"name":"belam","parent":"owner","harness":"claude","box":"tw"}
  - {"name":"council","parent":"belam","members":["alive","all-is-one","sp","dg5"]}
  - {"name":"keep","parent":"belam","members":["sm","tm"]}
  - {"name":"alive","parent":"council","harness":"claude","box":"tw"}
  - {"name":"all-is-one","parent":"council","harness":"claude"}
  - {"name":"sp","parent":"council","harness":"claude"}
  - {"name":"dg5","parent":"council","harness":"claude"}
  - {"name":"sm","parent":"keep","harness":"claude","box":"tw"}
  - {"name":"tm","parent":"keep","harness":"claude"}
  - {"name":"dg1","parent":"sm","harness":"claude","box":"tw"}
  - {"name":"dg2","parent":"sm","harness":"claude","box":"tw"}
  - {"name":"dg3","parent":"sm","harness":"claude","box":"tw"}
  - {"name":"dt1","parent":"tm","harness":"claude"}
  - {"name":"dg4","parent":null,"harness":"claude","box":"xx"}
EOF
$G -C $T/r add -A;$G -C $T/r -c user.name=x -c user.email=x@x commit -qm fixture
# as U SCRIPT ARGS...: run the box script as post U in the scratch repo (dash, like #!/bin/sh)
as(){ u=$1;s=$2;shift 2;(cd $T/r&&AGI_POST=$u AGI_TRUNK=HEAD GIT_CONFIG_GLOBAL=$T/c/$u GIT_CONFIG_SYSTEM=/dev/null sh $s "$@");}
ok(){ if eval "$2";then echo "ok $1";else echo "FAIL $1";f=$((f+1));fi;}
cnt(){ grep -c "$1" "$2" 2>/dev/null||true;}
ok3(){ if eval "$3";then echo "ok $1 $2";else echo "FAIL $1 $2";f=$((f+1));fi;}   # name, a text built at run time, the condition

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

# --- c2/c3: 2 writers on the SAME channel (two sessions of belam) x 50: with the retry nearly all arrive and every one that does not is LOUD; without it the case splits, 0 silent.
# (2026-10-12: '100/100, 0 stderr' was the m3 overlap claim under another name: the 5-try CAS cap loses ~2.3% of these sends, LOUDLY, even solo at load 1.5; a clean 100 was ~10% likely.
# STRICT: delivered + [unsent] reported = 100, stderr holds nothing but [unsent] lines. RATE: delivered >= 100 - M3_UNSENT_PCT. And the retry must BEAT the no-retry mutant, which is what it is for.)
two(){ v=$1;o=$2;e=$3;n=50;rm -f $o $e;$G -C $T/r update-ref -d refs/box/belam/dg5 2>/dev/null
 for w in a b;do (i=1;while [ $i -le $n ];do echo "$w $i"|as belam $v send dg5 2>>$e;i=$((i+1));done)&done;wait
 as dg5 $BR read>$o 2>&1;}
two $BR $T/c2.out $T/c2.err;d=$(grep -c '^\[belam\] ' $T/c2.out);e=$(wc -c<$T/c2.err)
c2d=$d;c2l=$(grep -c '^\[unsent\]' $T/c2.err);c2o=$(grep -vc '^\[unsent\]' $T/c2.err)
echo "# c2 (retry) delivered=$c2d unsent-reported=$c2l other-stderr-lines=$c2o (${e}B)";ok c2-retry-0-silent '[ $((c2d+c2l)) = 100 ]';ok c2-retry-stderr-only-unsent '[ $c2o = 0 ]';ok c2-retry-delivered-ge-$((100-P)) '[ $c2d -ge $((100-P)) ]'
# the mutation: the piece with its retry cap cut to ONE attempt: the same case must split, loudly ([unsent]), never silently
c3max=0;sp=0;for t in 1 2 3;do two $T/box1 $T/c3.out $T/c3.err;d=$(grep -c '^\[belam\] ' $T/c3.out);l=$(grep -c '^\[unsent\]' $T/c3.err);echo "# c3 try $t (no retry) delivered=$d reported=$l";[ $d -gt $c3max ]&&c3max=$d;[ $d -gt 0 ]&&[ $d -lt 100 ]&&sp=1;[ $((d+l)) = 100 ]||break;done
ok c3-mutation-splits '[ $sp = 1 ]'
ok c3-mutation-0-silent '[ $((d+l)) = 100 ]'
ok c2-retry-beats-the-no-retry-mutant '[ $c2d -gt $c3max ]'
two $T/boxs $T/c2s.out $T/c2s.err;c2sd=$(grep -c '^\[belam\] ' $T/c2s.out);c2sl=$(grep -c '^\[unsent\]' $T/c2s.err)
ok c2-mutant-silent-unsent-is-caught '[ $((c2sd+c2sl)) != 100 ]'

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
m3run(){ lb=$1;SS=$2;WPS=$3;MM=$4;NR=$5;TL=0;TU=0;TD=0;TX=0;TLO=0;r=1;MB=${6:-$BR}
 while [ $r -le $NR ];do
  $G -C $T/r for-each-ref --format='%(refname)' refs/box|grep '/alive$'|while read h;do $G -C $T/r update-ref -d $h;done  # every channel INTO alive: no leftovers from an earlier case
  $G -C $T/r for-each-ref --format='%(refname)' refs/held/alive|while read h;do $G -C $T/r update-ref -d $h;done
  rm -f $T/m3.* $T/done;: >$T/m3.out
  (while [ ! -e $T/done ];do as alive $BR read>>$T/m3.out 2>&1;done)&rd=$!
  pids=;for s in $SS;do k=0;while [ $k -lt $WPS ];do (j=0;while [ $j -lt $MM ];do i="$s.$k-$j";if echo "$i"|as $s $MB send alive 2>>$T/m3.err.$s$k;then echo "$i">>$T/m3.ok.$s$k;else echo "$i">>$T/m3.uns.$s$k;fi;j=$((j+1));done)&pids="$pids $!";k=$((k+1));done;done
  wait $pids;touch $T/done;wait $rd;as alive $BR read>>$T/m3.out 2>&1
  cat $T/m3.ok.* 2>/dev/null|sort>$T/m3.want;grep -o '^\[[a-z0-9]*\] [a-z0-9]*\.[0-9]*-[0-9]*' $T/m3.out|cut -d' ' -f2|sort>$T/m3.seen
  l=$(comm -23 $T/m3.want $T/m3.seen|wc -l);u=$(cat $T/m3.uns.* 2>/dev/null|wc -l);lo=$(cat $T/m3.err.* 2>/dev/null|grep -c '^\[unsent\]');d=$(uniq -d $T/m3.seen|wc -l);x=$(grep -c '^\[refused\]\|^\[off-matrix\]' $T/m3.out)
  echo "# m3 $lb run $r: attempted=$(( $(echo $SS|wc -w)*WPS*MM )) sent_ok=$(wc -l<$T/m3.want) unsent=$u loud=$lo received=$(wc -l<$T/m3.seen) lost=$l dup=$d refused=$x"
  TL=$((TL+l));TU=$((TU+u));TLO=$((TLO+lo));TD=$((TD+d));TX=$((TX+x));r=$((r+1));done;}
NR=${M3RUNS:-5};MM=${M3M:-100};BM=${M3BM:-150};BRUNS=${M3BRUNS:-3};P=${M3_UNSENT_PCT:-5}
if [ -z "$M3M$M3BM$M3RUNS$M3BRUNS" ];then
 p0=$(date +%s%N);m3run pilot "belam sm dg5" 2 8 1 >/dev/null;p1=$(date +%s%N)       # (m3run clobbers MM/NR: the defaults are restored below)
 NR=5;MM=100;BM=150;BRUNS=3
 pn=$(( (p1-p0)/1000000 ));[ $pn -gt 0 ]||pn=1                                         # pilot ms for 48 sends
 spent=$(( $(date +%s)-L0 ));left=$(( ${BUDGET_S:-270}-spent ))
 # sends the budget affords at the pilot's rate, keeping a third back for the mutant runs and the matrix rows
 afford=$(( left*1000*48*2/3/pn ))
 w(){ echo $(( 9*MM*NR+6*BM*BRUNS ));}                                                # distinct (3 senders) + overlap (6) + the bound
 # shrink in this order: the BOUND (informational) first, then the run count, then the sends per writer; NEVER below 50 per writer = n >= 300 per overlap run (council 00:08Z), or the P percent line cannot fail
 while [ "$(w)" -gt $afford ];do
  if [ $BRUNS -gt 1 ];then BRUNS=$((BRUNS-1))
  elif [ $BM -gt 30 ];then BM=$((BM/2));[ $BM -ge 30 ]||BM=30
  elif [ $NR -gt 2 ];then NR=$((NR-1))
  elif [ $MM -gt 50 ];then MM=$((MM-10));[ $MM -ge 50 ]||MM=50
  else break;fi
 done
 echo "# m3 fit: pilot 48 sends in ${pn}ms, ${spent}s spent of ${BUDGET_S:-270}s, afford $afford sends -> runs=$NR sends/writer=$MM (n=$((6*MM)) per overlap run) bound=${BM}x${BRUNS}"
fi
m3run distinct "belam sm dg5" 1 $MM $NR
ok m3-distinct-lost-0-x$NR '[ $TL = 0 ]';ok m3-distinct-unsent-0 '[ $TU = 0 ]';ok m3-distinct-dup-refused-0 '[ $TD = 0 ]&&[ $TX = 0 ]'
m3run overlap "belam sm dg5" 2 $MM $NR
# 2 sessions on one channel can exhaust the 5x CAS cap (an unsent is the cap's LOUD outcome; measured 2026-10-12 on encryption-town, solo at load 1.5: 70 of 3,000 = 2.33%, per run 15 8 19 15 13 of 600,
# lost 0 dup 0 refused 0; earlier: 0 of 3,000 on a quiet box, 2 of 600 at load 21). The model bounds one writer's unsent x5 by the other's successes, so the cap, not the load, sets the rate.
# STRICT: lost 0, dup 0, every unsent LOUD. RATE: <= M3_UNSENT_PCT (5) percent, the regression guard for the cap (the cap-1 mutant below must break it).
echo "# m3 overlap unsent=$TU of $((6*MM*NR)) loud=$TLO (tolerance ${P}%, measured $((TU*1000/(6*MM*NR)))/1000)"
ok m3-overlap-lost-0-x$NR '[ $TL = 0 ]';ok m3-overlap-unsent-all-loud '[ $TLO = $TU ]';ok m3-overlap-unsent-le-${P}pct '[ $((TU*100)) -le $((P*6*MM*NR)) ]';ok m3-overlap-dup-refused-0 '[ $TD = 0 ]&&[ $TX = 0 ]'
m3run bound "belam" 6 $BM $BRUNS
echo "# BOUND: 6 writers on ONE ref x $BM, $BRUNS runs: unsent=$TU of $((6*$BM*$BRUNS)) (loud; the cap-5 build's measured limit, never FAIL; goal g1.40's literal wording, see verdict:dg2-aa1m-m3)"
ok m3-bound-0-silent-loss '[ $TL = 0 ]&&[ $TD = 0 ]&&[ $TX = 0 ]'
ok m3-bound-unsent-all-loud '[ $TLO = $TU ]'
# the MUTANTS of the m3 rows, on small runs of the same shape: (1) the cap cut to one attempt must BREAK the rate bound (so a dropped retry cannot pass as '2 percent');
# (2) a box that fails a send WITHOUT saying [unsent] must break the all-loud row (a silent unsent cannot pass as loud)
m3run mut-cap1 "belam sm dg5" 2 20 1 $T/box1
ok m3-mutant-cap1-breaks-the-rate-bound '[ $((TU*100)) -gt $((P*6*20*1)) ]'
m3run mut-silent "belam sm dg5" 2 20 1 $T/boxs
ok m3-mutant-silent-unsent-is-caught '[ $TU -gt 0 ]&&[ $TLO -lt $TU ]'
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

# --- bs: a mail's body is FOREIGN text: read must print it BYTE-EQUAL to git log %B. dash's echo interprets backslashes (\b = 0x08, \c = TRUNCATES the rest of the mail, and held still advanced = fail-silent), so the read line is printf '%s'.
# The body carries \c and \b (and a second line after them); the mutant is the piece with that line back to `echo "[$f] ..."` and must go RED.
bsread(){ v=$1;o=$2;$G -C $T/r update-ref -d refs/box/belam/dg5 2>/dev/null;$G -C $T/r update-ref -d refs/held/dg5/belam 2>/dev/null
 printf '%s\n' 'head \bB \cC mid \\n tail' 'line2 after' 'last \c'|as belam $BR send dg5;as dg5 $v read>$o 2>&1;}
bsmut(){ sed 's/printf .\[%s\] %s\\n. "\$f" "/echo "[$f] /' $BR>$T/boxe;}
bsmut;ok bs-mutant-differs '! cmp -s $BR $T/boxe'
bsread $BR $T/bs.out;printf '[belam] %s\n' "$($G -C $T/r log -1 --format=%B refs/box/belam/dg5)">$T/bs.want
ok bs-read-byte-equal-to-git-log 'cmp -s $T/bs.out $T/bs.want'
ok bs-body-kept-backslashes 'grep -qF "\\cC mid" $T/bs.out&&grep -qF "line2 after" $T/bs.out&&grep -qF "last \\c" $T/bs.out&&[ "$(tr -d "\010"<$T/bs.out|wc -c)" = "$(wc -c<$T/bs.out)" ]'
ok bs-held-advanced '[ "$(as dg5 $BR n|wc -l)" = 0 ]'
bsread $T/boxe $T/bs.mut
ok bs-mutant-echo-back-RED '! cmp -s $T/bs.mut $T/bs.want'

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

# --- t: `box town up|down SHA` (goal:g7.16.1.11.44.8 S1; council 3/3 10-15 19:36Z + 19:41Z): belam's blast, a [town] commit is exactly ONE line `[town] (up|down) <40 hex>`, signed belam@agi; the sender checks AGI_POST=belam AND `id -un`=agi-belam (an `id` shim here), reaches every
# harness post of ITS box (AGI_BOX) except itself and never calls the adjacency rule; the receiver shows a [town] commit only for that regex + a belam signature, else `[town-dropped] <ref> <sha>` on stderr and the held ref advances. Every other subject keeps the adjacency rule.
mkdir -p $T/shim;printf '#!/bin/sh\n[ "$1" = -un ]&&echo ${STUB_UID:-nobody}||exec /usr/bin/id "$@"\n' >$T/shim/id;chmod +x $T/shim/id
TS=$(printf 'c%.0s' $(seq 40) | tr c 7)
tnb(){ bx=$1;shift;(cd $T/r&&PATH=$T/shim:$PATH AGI_POST=${TPOST:-belam} AGI_BOX=${TBOX-tw} AGI_TRUNK=HEAD GIT_CONFIG_GLOBAL=$T/c/belam GIT_CONFIG_SYSTEM=/dev/null STUB_UID=${TUID:-agi-belam} sh $bx town "$@");}
nref(){ $G -C $T/r for-each-ref --format='%(refname)' refs/box/belam|wc -l|tr -d ' ';}
tclr(){ for r in $($G -C $T/r for-each-ref --format='%(refname)' refs/box/belam refs/box/dg1 refs/held);do $G -C $T/r update-ref -d $r;done;}
rep(){ A=$1 B=$2 awk '{while((i=index($0,ENVIRON["A"]))>0)$0=substr($0,1,i-1) ENVIRON["B"] substr($0,i+length(ENVIRON["A"]));print}' $BR>$T/mut;}
fk(){ ( cd $T/r&&printf '%s' "$3"|AGI_TRUNK=HEAD GIT_CONFIG_GLOBAL=$T/c/$1 GIT_CONFIG_SYSTEM=/dev/null GIT_AUTHOR_EMAIL=$1@agi GIT_COMMITTER_EMAIL=$1@agi $G commit-tree -S $($G hash-object -w -t tree /dev/null)>$T/fk.sha&&$G update-ref $2 $(cat $T/fk.sha) );}
tclr;tnb $BR down $TS;rc=$?
ok3 t-down-rc0-one-commit-per-post-of-the-box "box town down: rc $rc (want 0), refs/box/belam/* = $(nref) (want 5: alive sm dg1 dg2 dg3; not dg4 of box xx, not belam, not the inert rows)" '[ $rc = 0 ]&&[ "$(nref)" = 5 ]&&! $G -C $T/r rev-parse -q --verify refs/box/belam/dg4 >/dev/null&&! $G -C $T/r rev-parse -q --verify refs/box/belam/council >/dev/null'
ok3 t-the-whole-message-is-one-template-line "the blast on each post: $(for q in alive sm dg1 dg2 dg3;do $G -C $T/r log -1 --format=%B refs/box/belam/$q|grep -c .;done|sort -u|tr '\n' ' ')line(s) (want 1), $(for q in alive sm dg1 dg2 dg3;do $G -C $T/r log -1 --format=%s refs/box/belam/$q;done|sort -u|wc -l|tr -d ' ') distinct subject (want 1: '[town] down SHA')" '[ "$(for q in alive sm dg1 dg2 dg3;do $G -C $T/r log -1 --format=%B refs/box/belam/$q|grep -c .;done|sort -u|tr -d "\n")" = 1 ]&&[ "$(for q in alive sm dg1 dg2 dg3;do $G -C $T/r log -1 --format=%s refs/box/belam/$q;done|sort -u)" = "[town] down $TS" ]'
ok3 t-signed-belam "git verify-commit on the dg2 blast reads 'for belam@agi with'" 'GIT_CONFIG_GLOBAL=$T/c/belam $G -C $T/r verify-commit --raw refs/box/belam/dg2 2>&1|grep -q "for belam@agi with"'
as dg2 $BR read>$T/t2.out 2>$T/t2.err
ok3 t-receiver-shows-it-past-the-adjacency-rule "dg2 (two levels from belam) reads: $(cat $T/t2.out) | stderr [$(cat $T/t2.err)] (want '[belam] [town] down $TS', no [off-matrix])" 'grep -qxF "[belam] [town] down $TS" $T/t2.out&&! grep -q "off-matrix" $T/t2.out $T/t2.err'
ok3 t-held-reached-the-down-commit "refs/held/dg2/belam is the down commit (the ack the stop reads): want it an ancestor-or-equal of the blast" '$G -C $T/r merge-base --is-ancestor refs/box/belam/dg2 refs/held/dg2/belam'
ok3 t-ordinary-mail-from-belam-keeps-the-adjacency-rule "belam -> dg2 with a non-[town] subject: rc $(echo x|as belam $BR send dg2 2>/dev/null;echo $?) (want 1, [off-matrix])" '[ "$(echo x|as belam $BR send dg2 2>/dev/null;echo $?)" = 1 ]'
n0=$(nref);TUID=dg2 tnb $BR down $TS 2>/dev/null;r1=$?;TPOST=dg2 tnb $BR down $TS 2>/dev/null;r2=$?
ok3 t-F6-a-non-belam-uid-or-post-is-refused-0-refs "uid dg2 rc $r1, post dg2 rc $r2 (want both != 0), refs/box/belam/* still $(nref) (want $n0)" '[ $r1 != 0 ]&&[ $r2 != 0 ]&&[ "$(nref)" = "$n0" ]'
tclr;r3=0;for a in "down $TS extra" "sideways $TS" "down ${TS}0" "down $(echo $TS|tr 7 C)" "down" "";do tnb $BR $a 2>/dev/null&&r3=1;done;TBOX= tnb $BR down $TS 2>/dev/null&&r3=1
ok3 t-F6-extra-text-or-a-bad-sha-or-no-box-is-refused-at-the-sender "7 bad calls (extra word, bad verb, 41 hex, uppercase, no sha, no args, AGI_BOX unset): all refused ($r3, want 0), refs = $(nref) (want 0)" '[ $r3 = 0 ]&&[ "$(nref)" = 0 ]'
echo "[town] down $TS"|as belam $BR send sm 2>$T/t3.err;r4=$?
ok3 t-F6-box-send-never-carries-a-town-subject "belam -> sm (adjacent) with a [town] body through send: rc $r4 (want 1, 'box town' named), ref = $(nref) (want 0)" '[ $r4 = 1 ]&&grep -q "box town" $T/t3.err&&[ "$(nref)" = 0 ]'
# the receiver: extra text (a body line, trailing text) and a non-belam sender are dropped, named on stderr, and the held ref goes past them
tclr;fk belam refs/box/belam/dg3 "[town] down $TS extra";as dg3 $BR read>$T/d1.out 2>$T/d1.err;as dg3 $BR read>$T/d1b.out 2>$T/d1b.err
ok3 t-F6-extra-text-is-dropped-at-the-receiver "dg3 reads a belam-signed '[town] down SHA extra': stdout [$(cat $T/d1.out)] (want empty), stderr [$(cut -c1-60 $T/d1.err)] (want [town-dropped] refs/box/belam/dg3 <sha>), second read stderr [$(cat $T/d1b.err)] (want empty: the held ref passed it)" '[ ! -s $T/d1.out ]&&grep -q "^\[town-dropped\] refs/box/belam/dg3 " $T/d1.err&&[ ! -s $T/d1b.err ]'
tclr;fk belam refs/box/belam/dg3 "[town] down $TS
second line";as dg3 $BR read>$T/d2.out 2>$T/d2.err
ok3 t-F6-a-second-line-is-dropped "a belam-signed two-line [town] commit: stdout [$(cat $T/d2.out)] (want empty), dropped named: $(grep -c town-dropped $T/d2.err) (want 1)" '[ ! -s $T/d2.out ]&&[ "$(grep -c "^\[town-dropped\]" $T/d2.err)" = 1 ]'
tclr;fk dg1 refs/box/dg1/dg3 "[town] down $TS";as dg3 $BR read>$T/d3.out 2>$T/d3.err
ok3 t-F6-the-template-from-a-non-belam-post-is-dropped "a dg1-signed exact '[town] down SHA': stdout [$(cat $T/d3.out)] (want empty), dropped named: $(grep -c town-dropped $T/d3.err) (want 1)" '[ ! -s $T/d3.out ]&&[ "$(grep -c "^\[town-dropped\]" $T/d3.err)" = 1 ]'
# the MUTANTS: each one edit on the piece, each makes its row above FAIL
mutrun(){ # $1 sed-free A $2 B ; sets MUT=1 when the edit changed the piece
 rep "$1" "$2";cmp -s $BR $T/mut&&MUT=0||MUT=1;}
rep '[ "$(id -un)" = agi-belam ]&&' '';cmp -s $BR $T/mut&&echo "# mutant-uid: no edit made";tclr;TUID=dg2 tnb $T/mut down $TS 2>/dev/null;r=$?
ok3 t-mutant-no-uid-check-is-RED "the piece without the id -un check, run as uid dg2: rc $r and $(nref) ref(s) (the clean row wants rc != 0 and 0 new refs: this one must send)" '! cmp -s $BR $T/mut&&[ $r = 0 ]&&[ "$(nref)" -gt 0 ]'
rep '[ $# = 3 ]&&' '';tclr;tnb $T/mut down $TS extra 2>/dev/null;r=$?
ok3 t-mutant-no-argument-count-is-RED "the piece without the 3-argument check accepts 'down SHA extra': rc $r and $(nref) ref(s) (want rc 0 and > 0: the clean row refuses)" '! cmp -s $BR $T/mut&&[ $r = 0 ]&&[ "$(nref)" -gt 0 ]'
rep ' and .box==$x' '';tclr;tnb $T/mut down $TS 2>/dev/null;r=$?
ok3 t-mutant-no-box-filter-is-RED "the piece without the box filter also blasts dg4 (box xx): refs/box/belam/dg4 is $($G -C $T/r rev-parse -q --verify refs/box/belam/dg4 >/dev/null&&echo set||echo absent) (want set: the clean row has it absent)" '! cmp -s $BR $T/mut&&$G -C $T/r rev-parse -q --verify refs/box/belam/dg4 >/dev/null'
rep '[ $f = belam ]&&' '';tclr;fk dg1 refs/box/dg1/dg3 "[town] down $TS";as dg3 $T/mut read>$T/m1.out 2>/dev/null
ok3 t-mutant-no-sender-check-at-the-receiver-is-RED "the receiver without the belam check shows dg1's [town] commit: stdout [$(cat $T/m1.out)] (want it shown: the clean row drops it)" '! cmp -s $BR $T/mut&&grep -qF "[town] down $TS" $T/m1.out'
rep '[ "$(printf '"'"'%s\n'"'"' "$b"|wc -l)" = 1 ]&&' '';tclr;fk belam refs/box/belam/dg3 "[town] down $TS
second line";as dg3 $T/mut read>$T/m2.out 2>/dev/null
ok3 t-mutant-no-one-line-check-at-the-receiver-is-RED "the receiver without the one-line check shows a two-line [town] commit: stdout $(wc -l <$T/m2.out|tr -d ' ') line(s) (want >= 1: the clean row shows none)" '! cmp -s $BR $T/mut&&grep -qF "second line" $T/m2.out'
rep 'case $b in "[town]"*)echo "[town] is box town'"'"'s alone: nothing sent">&2;exit 1;;esac;' '';tclr;echo "[town] down $TS"|as belam $T/mut send sm 2>/dev/null;r=$?
ok3 t-mutant-send-carries-a-town-subject-is-RED "the piece without the send-side [town] refusal: belam -> sm rc $r, $(nref) ref(s) (want rc 0 and 1: the clean row refuses)" '! cmp -s $BR $T/mut&&[ $r = 0 ]&&[ "$(nref)" = 1 ]'
tclr

# --- negative: size, no Python, no inbox path
ok n1-bytes-le-ceiling '[ "$(wc -c<$BR)" -le $CEIL ]'
echo "# box (the piece) bytes=$(wc -c<$BR) ceiling=$CEIL"
ok n2-no-python '! grep -qi python $BR'
ok n3-no-inbox-path '! grep -q "sessions/inbox" $BR'
exit $f
