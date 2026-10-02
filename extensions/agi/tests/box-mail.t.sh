#!/bin/sh
# box-mail.t.sh: AA1.M / M1 falsifiers for `box send` (hypothesis g716111-aa1m-box-send-...): sh + git + jq, scratch only,
# throwaway keys, no live ref. One ok/FAIL line per case; exit = number of FAILs.
# BOX=<file>  the box script under test (default: extracted from DOC, the `box` whole + alive's retry send arm)
# DOC=<file>  rse-aa1-boxes.md (default: the trunk's copy, else git show posts/alive:...); ROOT=<repo> where to look
# BRSED=<sed script> scratch knob: mutate the built box (how the cap numbers on experiment:dg2-aa1m-m3 were measured)
# M3M/M3RUNS = sends per writer / runs for the realistic M3 cases (default 100/5); M3BM/M3BRUNS the same for the 6-on-one-ref BOUND (150/3)
# NOTE: the mutation case (c4) needs the no-retry variant, which only the doc-extracted default provides.
D=${DOC:-};T=$(mktemp -d);trap 'rm -rf $T' 0;f=0;G=/usr/bin/git;R0=${ROOT:-$(cd "$(dirname "$0")/../../.." && pwd)}
# the doc: DOC, else the trunk's copy, else alive's branch (until the doc lands on the trunk)
[ -n "$D" ]||{ D=$T/doc.md;[ -f $R0/.agi/nodes/doc/rse-aa1-boxes.md ]&&cp $R0/.agi/nodes/doc/rse-aa1-boxes.md $D||$G -C $R0 show posts/alive:.agi/nodes/doc/rse-aa1-boxes.md>$D;}
# the piece, extracted whole from the doc: the first fenced sh block after "### `box` whole"
sed -n '/^### `box` whole/,/^`agi-run`/{/^```sh/,/^```$/{//!p}}' $D>$T/box0
# alive's retry send arm = the fenced block that begins `send)a`
sed -n '/^### AA1.M/,$p' $D|sed -n '/^send)a /,/^```$/{/^```$/!p}'>$T/send.r
[ -s $T/box0 ]&&[ -s $T/send.r ]||{ echo "FAIL extract: box0 $(wc -c<$T/box0) send.r $(wc -c<$T/send.r)";exit 99;}
# box with retry = box0 with its 2-line send arm replaced by the retry arm
awk -v R=$T/send.r 'BEGIN{while((getline l<R)>0)s=s l "\n"} /^send\)a /{printf "%s",s;next} {print}' $T/box0>$T/boxr
[ -n "$BRSED" ]&&sed -i "$BRSED" $T/boxr  # scratch knob: mutate the built box (cap experiments)
B0=$T/box0;BR=${BOX:-$T/boxr}
# keys + signers + per-post git config + a repo whose trunk (HEAD) holds the fixture matrix
mkdir $T/k $T/c;: >$T/signers
for u in belam sm alive dg5 dg1;do
 ssh-keygen -q -t ed25519 -N '' -f $T/k/$u -C $u>/dev/null
 echo "$u@agi namespaces=\"git\" $(cut -d' ' -f1,2 $T/k/$u.pub)">>$T/signers
 printf '[user]\n\tname=%s\n\temail=%s@agi\n\tsigningkey=%s\n[gpg]\n\tformat=ssh\n[gpg "ssh"]\n\tallowedSignersFile=%s\n[commit]\n\tgpgsign=false\n' $u $u $T/k/$u $T/signers>$T/c/$u
done
$G init -q $T/r;mkdir -p $T/r/.agi/nodes/.geometry
cat >$T/r/.agi/nodes/.geometry/posts.md<<'EOF'
  - {"name":"belam","parent":"","harness":"claude"}
  - {"name":"council","parent":"belam"}
  - {"name":"alive","parent":"council","harness":"claude"}
  - {"name":"dg5","parent":"council","harness":"claude"}
  - {"name":"sm","parent":"council","harness":"claude"}
  - {"name":"dg1","parent":"sm","harness":"claude"}
EOF
$G -C $T/r add -A;$G -C $T/r -c user.name=x -c user.email=x@x commit -qm fixture
# as U SCRIPT ARGS...: run the box script as post U in the scratch repo (dash, like #!/bin/sh)
as(){ u=$1;s=$2;shift 2;(cd $T/r&&AGI_POST=$u AGI_TRUNK=HEAD GIT_CONFIG_GLOBAL=$T/c/$u GIT_CONFIG_SYSTEM=/dev/null sh $s "$@");}
ok(){ if eval "$2";then echo "ok $1";else echo "FAIL $1";f=$((f+1));fi;}
cnt(){ grep -c "$1" "$2" 2>/dev/null||true;}

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
# the mutation: drop the retry (the doc's own no-retry send) and the same case must split, loudly, never silently
sp=0;for t in 1 2 3;do two $B0 $T/c3.out $T/c3.err;d=$(grep -c '^\[belam\] ' $T/c3.out);l=$(grep -c 'cannot lock ref' $T/c3.err);echo "# c3 try $t (no retry) delivered=$d reported=$l";[ $d -gt 0 ]&&[ $d -lt 100 ]&&sp=1;[ $((d+l)) = 100 ]||break;done
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
ok m3-overlap-lost-0-x$NR '[ $TL = 0 ]';ok m3-overlap-unsent-0 '[ $TU = 0 ]';ok m3-overlap-dup-refused-0 '[ $TD = 0 ]&&[ $TX = 0 ]'
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

# --- negative: size, no Python, no inbox path
ok n1-bytes-le-1927 '[ "$(wc -c<$BR)" -le 1927 ]'
echo "# box (retry) bytes=$(wc -c<$BR) box0 bytes=$(wc -c<$B0)"
ok n2-no-python '! grep -qi python $BR'
ok n3-no-inbox-path '! grep -q "sessions/inbox" $BR'
exit $f
