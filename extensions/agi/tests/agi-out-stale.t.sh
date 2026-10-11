#!/bin/sh
# agi-out-stale.t.sh [TRUNK]: OUT.7 (belam 15:1xZ, DG1 15:13Z): a post whose t is STALE (no agi-out piece in t, so none in ~/bin, none on the unit's PATH) must still START. Today the unit's `ExecStartPre=sh -c 'agi-out'` exits 127 on every start and Restart=always loops (DG3 193 cycles, DG2 176). The unit is read from TRUNK's engine-root.md (UNIT=<file> tests a candidate unit text), and its ExecCondition / ExecStartPre / ExecStart lines are run IN ORDER as the unit runs them (sh -c with the unit's PATH, in a scratch HOME): the root `+` steps (agi-signers) and the /proc/pressure awk are stubs (they are not t-resident and the awk reads the host). Lanes: O7a stale t, O7b a 5-cycle Restart loop, O7c piece present (its own exit code passes through), O7d present but unrunnable (only ABSENT skips), O7e a restart through a conflicting t, O7f every other step on a stale t. sh + git, no network, nothing pushed
T=${1:-local-maxxing/season2/main};D=$(mktemp -d);trap 'rm -rf $D' EXIT;f=0;GEO=.agi/nodes/.geometry
o=$(git rev-parse $T)||exit 1
if [ "$UNIT" ];then cp $UNIT $D/unit;else git show $o:$GEO/engine-root.md|sed -n '/^### agi-post@.service/,/^~~~$/p'>$D/unit;fi
[ -s $D/unit ]||{ echo "FAIL no agi-post@.service at $T";exit 99;}
ok(){ if eval "$2";then echo "ok $1";else echo "FAIL $1";f=$((f+1));fi;}
unset GIT_AUTHOR_NAME GIT_AUTHOR_EMAIL GIT_COMMITTER_NAME GIT_COMMITTER_EMAIL GIT_DIR GIT_WORK_TREE;export GIT_CONFIG_GLOBAL=/dev/null GIT_CONFIG_SYSTEM=/dev/null
GIT=$(command -v git)
# the start sequence, %i = post1, %t = a scratch run dir: ExecCondition, ExecStartPre, ExecStart, in unit order. s.N = the sh -c script of line N, k.N = its kind, t.N = its type
grep -E '^(ExecCondition|ExecStartPre|ExecStart)=' $D/unit|sed "s|%i|post1|g;s|%t|$D/run|g">$D/seq;nl=0
while IFS= read -r l;do nl=$((nl+1));echo "${l%%=*}">$D/k.$nl;v=${l#*=};case $v in "+"*)echo plus>$D/t.$nl;;"awk "*)echo awk>$D/t.$nl;;"sh -c '"*)echo sh>$D/t.$nl;s=${v#"sh -c '"};printf '%s' "${s%"'"}">$D/s.$nl;;*)echo other>$D/t.$nl;;esac;done<$D/seq
AO=$(grep -n 'agi-out' $D/seq|cut -d: -f1);[ "$(echo "$AO"|wc -w)" = 1 ]||{ echo "FAIL the unit has not exactly one agi-out step ($AO)";exit 99;}
# mkh N: a scratch HOME with a STALE t (a git repo whose engine-post.md carries agi-flush + agi-run and NO agi-out), an empty /opt/agi/bin stand-in, no bin/agi-out
mkh(){ H=$D/h$1;rm -rf $H $D/opt;mkdir -p $H/t/$GEO $H/bin $D/run/agi-post1 $D/opt $D/orig;SHIM=
 printf '### agi-flush (stub)\n~~~sh\n#!/bin/sh\ngit -C t merge "${AGI_TRUNK:-trunk}" >/dev/null||echo "agi-flush: merge conflict, t left as it was" >&2\nexit 0\n~~~\n### agi-run (stub)\n~~~sh\n#!/bin/sh\nexit 0\n~~~\n'>$H/t/$GEO/engine-post.md
 (cd $H/t;$GIT init -q;$GIT add -A;$GIT -c user.name=x -c user.email=x@x -c commit.gpgsign=false commit -qm stale);rm -f $D/run/agi-post1/i;}
pu(){ echo ${SHIM:+$SHIM:}$H/bin:$D/opt:/usr/local/bin:/usr/bin:/bin;}
# one N: step N alone (rc in sr, stdout so.N, stderr se.N)
one(){ (cd $H&&env -i PATH=$(pu) HOME=$H O=$D/orig AGI_TRUNK=trunk AGI_SEAT=post1 GIT_CONFIG_SYSTEM=/dev/null GIT_TEST_ASSUME_DIFFERENT_OWNER=1 sh -c "$(cat $D/s.$1)")>$D/so.$1 2>$D/se.$1;sr=$?;echo $sr>$D/rc.$1;}
# cyc: ONE start of the unit (steps in order; a failing ExecStartPre aborts the start = systemd's Restart= loop; ALL=1 runs on past a failure to fill the table). creach = ExecStart reached, cfail = "N:rc" of the first failing step, pl = the root stubs that ran
cyc(){ creach=0;cfail=;: >$D/pl;n=0;while [ $n -lt $nl ];do n=$((n+1));k=$(cat $D/k.$n);ty=$(cat $D/t.$n)
  [ $k = ExecStart ]&&{ creach=1;break;}
  case $ty in plus)echo $n>>$D/pl;continue;;awk|other)continue;;esac
  one $n;if [ $sr != 0 ];then [ $k = ExecCondition ]&&break;[ -z "$cfail" ]&&cfail="$n:$sr";[ -z "$ALL" ]&&break;fi;done;}
rcao(){ cat $D/rc.$AO 2>/dev/null;}
# --- O7a: a STALE t (no agi-out anywhere): the step exits 0, ONE loud line on stderr naming the piece, saying skipped and stale t, and the NEXT steps still run (the post starts)
mkh 1;rm -f $D/rc.*;cyc
ok "o7a-stale-exit-0 no bin/agi-out in t, none on the unit's PATH: the agi-out step exits 0 (got $(rcao); 127 = the restart loop of today)" '[ "$(rcao)" = 0 ]'
ok "o7a-one-loud-line the step prints ONE line on stderr that names agi-out, says skipped and says stale t, and nothing on stdout (stderr $(wc -l <$D/se.$AO) line: $(head -1 $D/se.$AO|cut -c1-110))" '[ "$(wc -l <$D/se.$AO)" = 1 ]&&grep -qi agi-out $D/se.$AO&&grep -qi skipped $D/se.$AO&&grep -qi "stale t" $D/se.$AO&&[ ! -s $D/so.$AO ]'
ok "o7a-next-steps-run the steps AFTER agi-out still run (the second root step, agi-signers: $(wc -l <$D/pl) root steps ran, want 2) and the unit reaches ExecStart (reached=$creach, first failure: ${cfail:-none})" '[ $creach = 1 ]&&[ "$(wc -l <$D/pl)" = 2 ]'
# --- O7b: Restart=always simulated, 5 starts with the stale t: zero 127, one loud line per start, ExecStart reached each time
mkh 2;reach=0;n127=0;nl_=0;for i in 1 2 3 4 5;do rm -f $D/rc.*;cyc;reach=$((reach+creach));[ "$(rcao)" = 127 ]&&n127=$((n127+1));nl_=$((nl_+$(wc -l <$D/se.$AO)));done
ok "o7b-loop-5-starts 5 starts with the stale t: ExecStart reached $reach times (want 5), agi-out exits 127 $n127 times (want 0), $nl_ stderr lines from the step (want 5: ONE per start)" '[ $reach = 5 ]&&[ $n127 = 0 ]&&[ $nl_ = 5 ]'
# --- O7c: agi-out PRESENT: the step runs it as today and ITS exit code passes through (a skip never masks a present piece that fails)
for x in 3 0 127;do mkh 3;printf '#!/bin/sh\necho ran>>$HOME/ran\nexit %s\n' $x>$H/bin/agi-out;chmod +x $H/bin/agi-out;rm -f $D/rc.*;cyc;want=0;[ $x = 0 ]&&want=1
 ok "o7c-present-exit-$x a present bin/agi-out exiting $x: the step exits $x (got $(rcao)), the piece ran ONCE ($(wc -l <$H/ran) time), no skipped line (stderr: $(head -1 $D/se.$AO|cut -c1-60)), and the start reaches ExecStart only on 0 (reached=$creach)" '[ "$(rcao)" = $x ]&&[ "$(wc -l <$H/ran)" = 1 ]&&! grep -qi skipped $D/se.$AO&&[ $creach = $want ]';done
# O7c2: agi-out on the unit's PATH but NOT in bin/ (the /opt/agi/bin stand-in): present on the PATH, so it must RUN and its exit code pass through (a skip keyed on bin/ alone masks a present root-owned piece)
for x in 3 0;do mkh 3;printf '#!/bin/sh\necho ran>>$HOME/ran\nexit %s\n' $x>$D/opt/agi-out;chmod +x $D/opt/agi-out;rm -f $D/rc.*;cyc
 ok "o7c2-on-path-not-in-bin-exit-$x agi-out only on the unit's PATH (the /opt/agi/bin stand-in), exiting $x: the step runs it ONCE ($(wc -l <$H/ran 2>/dev/null) times) and exits $x (got $(rcao)), no skipped line (stderr: $(head -1 $D/se.$AO|cut -c1-60))" '[ "$(rcao)" = $x ]&&[ "$(wc -l <$H/ran)" = 1 ]&&! grep -qi skipped $D/se.$AO';done
# --- O7d (DG1 ruling: only ABSENT skips; present-and-broken fails as today, loud, never 0). Run on the STEP alone (the unit's line-36 `chmod +x bin/*` runs first in a real start and repairs a mode: named below)
mkh 4;printf '#!/bin/sh\nexit 0\n'>$H/bin/agi-out;chmod -x $H/bin/agi-out;one $AO
ok "o7d-not-executable bin/agi-out present but not executable: the step fails (rc $sr), loud (stderr: $(head -1 $D/se.$AO|cut -c1-70)), no skip. Green today by luck (every absence fails today too)" '[ $sr != 0 ]&&[ -s $D/se.$AO ]&&! grep -qi skipped $D/se.$AO'
mkh 4;mkdir $H/bin/agi-out;one $AO
ok "o7d-directory bin/agi-out is a DIRECTORY: the step fails (rc $sr), loud (stderr: $(head -1 $D/se.$AO|cut -c1-70)), no skip" '[ $sr != 0 ]&&[ -s $D/se.$AO ]&&! grep -qi skipped $D/se.$AO'
mkh 4;ln -s $D/nowhere $H/bin/agi-out;one $AO
ok "o7d-dangling-symlink bin/agi-out is a DANGLING symlink: the step fails (rc $sr), loud (stderr: $(head -1 $D/se.$AO|cut -c1-70)), no skip" '[ $sr != 0 ]&&[ -s $D/se.$AO ]&&! grep -qi skipped $D/se.$AO'
mkh 4;printf '#!/bin/sh\nexit 0\n'>$H/bin/agi-out;chmod -x $H/bin/agi-out;rm -f $D/rc.*;cyc
ok "o7d-chmod-repairs-in-a-start the same non-executable file through a whole start: line 36's chmod +x bin/* runs BEFORE agi-out, the piece runs and exits 0 (rc $(rcao), reached=$creach): a not-executable piece cannot arise through the unit" '[ "$(rcao)" = 0 ]&&[ $creach = 1 ]'
# --- O7e (belam): a restart through an out-line, t NOT merged. The stop path (ExecStopPost agi-flush) tries to merge the trunk into t and CONFLICTS (a shim git: every `merge` fails); the unit restarts on the SAME stale t: it starts, ONE loud line, no loop
mkh 5;mkdir -p $D/shim;printf '#!/bin/sh\ncase " $* " in *" merge "*)echo "CONFLICT (content): automatic merge failed" >&2;: >%s;exit 1;;esac\nexec %s "$@"\n' $D/merged $GIT>$D/shim/git;chmod +x $D/shim/git;SHIM=$D/shim;rm -f $D/merged
rm -f $D/rc.*;cyc;r1=$creach;h0=$($GIT -C $H/t rev-parse HEAD);(cd $H&&env -i PATH=$(pu) HOME=$H AGI_TRUNK=trunk sh -c agi-flush>/dev/null 2>$D/flush.err);h1=$($GIT -C $H/t rev-parse HEAD);rm -f $D/rc.*;cyc
ok "o7e-restart-through-conflicting-t start, stop (agi-flush: the merge was tried=$( [ -e $D/merged ]&&echo yes||echo no ) and conflicted, t HEAD $( [ $h0 = $h1 ]&&echo unchanged||echo CHANGED )), restart on the same stale t: both starts reach ExecStart (first $r1, second $creach), agi-out exits $(rcao) (want 0), stderr $(wc -l <$D/se.$AO) line (want 1)" '[ -e $D/merged ]&&[ $h0 = $h1 ]&&[ $r1 = 1 ]&&[ $creach = 1 ]&&[ "$(rcao)" = 0 ]&&[ "$(wc -l <$D/se.$AO)" = 1 ]'
# --- O7f: every OTHER step of the unit on a stale t (t present, no ring file, no engine pieces beyond the stubs): one lane per ExecCondition / sh -c ExecStartPre, the table in the output (tbl lines); a nonzero rc = the step would ALSO loop
mkh 6;rm -f $D/rc.*;ALL=1;cyc;unset ALL
n=0;while [ $n -lt $nl ];do n=$((n+1));k=$(cat $D/k.$n);ty=$(cat $D/t.$n);lb=$(echo "$k $(cat $D/s.$n 2>/dev/null)"|cut -c1-60);[ $k = ExecStart ]&&{ echo "tbl ExecStart line $n: the main process, not a Pre step (see the info row)";continue;};case $ty in plus|awk)echo "tbl $k line $n: STUBBED ($ty: root-owned /opt or a host read, not t-resident)";continue;;esac
 r=$(cat $D/rc.$n 2>/dev/null);echo "tbl $lb... line $n rc=$r";[ $n = $AO ]&&continue
 ok "o7f-line-$n-stale-t [$lb...] on a stale t (no ring file, no engine pieces beyond the stubs) exits 0 (got $r): it does not loop" '[ "$r" = 0 ]';done
# info rows (NOT counted): the ExecStart's agi-run and the ExecStopPost's agi-flush are t-resident pieces too; run with NO such piece in bin/ (a t that lacks the piece), what the unit would see
mkh 7;(cd $H&&env -i PATH=$(pu) HOME=$H sh -c agi-run>/dev/null 2>&1);ra=$?;(cd $H&&env -i PATH=$(pu) HOME=$H sh -c agi-flush>/dev/null 2>&1);rf=$?
echo "tbl info ExecStart's agi-run absent from bin/: rc=$ra; ExecStopPost's agi-flush absent: rc=$rf (nonzero = a failed main process / a failed stop, Restart=always restarts either way; not counted)"
# z1 (DG1 04:44Z re-scope: the real-ownership env is the DEFAULT of every A-range lane): this lane never reads a foreign-uid repo -- the unit lines run in a scratch HOME whose stale t is the post's OWN, and $O is an empty dir -- so the env is on by default and ONE row proves it: under the lane's env (empty config + git's different-owner seam) a plain git read of its t is REFUSED as dubious ownership, and the grant the unit gives (safe.directory=*) lifts it
mkh 8;sn=$(cd $H/t&&env -i PATH=$PATH HOME=$H GIT_CONFIG_GLOBAL=/dev/null GIT_CONFIG_SYSTEM=/dev/null GIT_TEST_ASSUME_DIFFERENT_OWNER=1 git rev-parse HEAD 2>&1|grep -c 'dubious ownership');gn=$(cd $H/t&&env -i PATH=$PATH HOME=$H GIT_CONFIG_GLOBAL=/dev/null GIT_CONFIG_SYSTEM=/dev/null GIT_TEST_ASSUME_DIFFERENT_OWNER=1 git -c safe.directory='*' rev-parse HEAD >/dev/null 2>&1;echo $?)
ok "z1-real-ownership-default-is-on a plain git read of t under an empty config + GIT_TEST_ASSUME_DIFFERENT_OWNER=1: $sn dubious-ownership line(s) (want 1: the seam bites on this lane's t); with the unit's safe.directory=* grant: rc $gn (want 0)" '[ "$sn" = 1 ]&&[ "$gn" = 0 ]'
echo "agi-out-stale: $f FAIL";exit $f
