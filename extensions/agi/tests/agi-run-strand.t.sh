#!/bin/sh
# agi-run-strand.t.sh [ROOT]: the agi-run STRAND (council [decision] alive 19:32:42Z 10-26): the unit's MainPID must end when claude exits, whatever state the strace -o consumer (agi-track) is in.
# The REAL chain: script -qfaO -> agi-run -> strace -qqf -b execve -o'|agi-track' -> a STUB claude, in a scratch HOME (RUNTIME_DIRECTORY, AGI_POST, a git ~/t in tmp); nothing live, no post identity. Pieces come from `sect NAME` of ROOT's .geometry (agi-run: engine-wrap.md, agi-track: engine-post.md), or PIECES_WRAP / PIECES_POST (a candidate file).
# THE CONDITION (measured, DG2 10-26, 18-20 of 20 runs on the pre-fix bytes): with the -o consumer DEAD (agi-track killed, or ~/track unwritable as at ENOSPC) the stub exits and strace stays in do_wait with only agi-run's two background loops left -- they were strace's OWN children (the old last line was `exec strace`). Killing the loops ended it; killing the orphan grep/awk did not.
#   s0 no fault: the unit ends when the stub exits (clean exit, and the out-line path: a CHILD of claude runs `touch ~/.fresh; kill $PPID`)
#   s1 the consumer KILLED mid-run, both exit paths: MainPID ends within N s and NO process of the run is left (the loops die with the unit)
#   s2 ~/track UNWRITABLE (a directory), both exit paths: MainPID ends, 0 `Broken pipe` lines in ~/o, the ONE named line `agi-track: append failed (...), draining` per run
#   s4 agi-run run BARE (no pty): the stub exits -> the two loops are killed by pid, 0 processes left (the claim 'kills its two loops', independent of any hangup)
#   NOT COUNTED, by design: (1) a killed loop's pending `sleep` (sleep 300 / sleep 5) is orphaned when its loop shell dies and ends by itself; it holds no pipe and no unit; (2) the FRESH-start [rotation-alert] job (agi-run line 5, only when ~/.fresh was there at start) is a THIRD background job agi-run does not kill: it is bounded by its own `timeout -k 2 20`; every run here starts with no ~/.fresh, so it never forks in the lane
#   s3 ~/.fresh written by the stub survives its exit: consumed at START only (agi-run line 2), the exit path never touches it
# MUTANTS (each sed asserted to change its piece): m1 `exec strace` back and no loop kill -> s1 RED (MainPID stays up)   m2 the loop kill dropped -> s4 RED (the loops remain)   m3 the drain dropped (the old one-line agi-track) -> s2 RED (Broken pipe lines)
# THE KILL IS A CHECKED CLAIM, not the hangup's side effect (alive's pre-read 20:25:38Z): s4 runs agi-run BARE (no script, no pty: stdout/stderr to a file) and the stub exits -> 0 processes of the run left within N s; m2 (the kill dropped) -> the two loops remain -> RED. `kill $(jobs -p)` was a no-op (jobs -p prints nothing in a non-interactive dash), which is why the first cut's dropped-kill mutant could not go RED: the loops then ended only by the pty hangup. The loops' pids are captured where they are forked (L1, L2).
# STRAND_NOMUT=1 skips the mutants (run the CANDIDATE/OLD pieces as they are: the pre-fix bytes read RED on s1 s2). STRAND_RUNS (default 2) runs per cell; N = STRAND_N s (default 8) is the bound. A box without strace or script prints `SKIP ... (unread, not a pass)` and exits 2: a silent pass would read green.
f=0;R0=${ROOT:-${1:-$(cd "$(dirname "$0")/../../.." && pwd)}};RUNS=${STRAND_RUNS:-2};N=${STRAND_N:-8}
ok(){ if eval "$2";then echo "ok $1";else echo "FAIL $1";f=$((f+1));fi;}
command -v strace >/dev/null&&command -v script >/dev/null||{ echo "SKIP agi-run-strand: strace or script absent (unread, not a pass)";exit 2;}
T=$(mktemp -d "${TMPDIR:-/tmp}/ars.XXXXXX");trap 'rm -rf $T' 0
sect(){ awk -v n="$1" '$0~"^### "n" "{h=1;next}h&&/^~~~/{if(z)exit;z=1;next}h&&z' $2;}
W=${PIECES_WRAP:-$R0/.agi/nodes/.geometry/engine-wrap.md};P=${PIECES_POST:-$R0/.agi/nodes/.geometry/engine-post.md}
mkdir -p $T/b;sect agi-run $W >$T/b/agi-run;sect agi-track $P >$T/b/agi-track;chmod +x $T/b/*
ok x0-pieces-extracted '[ -s $T/b/agi-run ]&&[ -s $T/b/agi-track ]'
# mine: pids whose environ carries HOME=$1 (the run's scratch home) -- never a pattern over argv
mine(){ for p in /proc/[0-9]*;do [ -r $p/environ ]||continue;{ tr '\0' '\n' <$p/environ;} 2>/dev/null|grep -qx "HOME=$1"&&echo ${p#/proc/};done;}   # a pid that exits between the -r and the read is silent (the redirect, not tr, printed "cannot open")
# RUN <bindir> <exit path term|clean> <fault none|killtrack|trackro> [bare]: one run of the chain; sets RS (ended|STRAND) RL (processes of the run left) RB (Broken pipe lines in ~/o) RN (the named agi-track line) RF (y if ~/.fresh is still there)
RUN(){ b=$1;D=$(mktemp -d $T/r.XXXXXX);h=$D/h;mkdir -p $h/t $h/bin $D/rt;cp $b/agi-run $b/agi-track $h/bin/;git -C $h/t init -q 2>/dev/null
 [ $3 = trackro ]&&mkdir $h/track
 case $2 in term)x='sh -c '"'"'touch $HOME/.fresh; kill $PPID'"'"';sleep 1';; *)x='touch $HOME/.fresh;exit 0';;esac
 printf '#!/bin/sh\nsleep 2\n%s\n' "$x" >$h/bin/claude-stub;chmod +x $h/bin/claude-stub
 if [ "$4" = bare ];then ( env -i PATH=$h/bin:/usr/bin:/bin HOME=$h O=$h/t AGI_POST=stub H=claude-stub RUNTIME_DIRECTORY=$D/rt TERM=dumb timeout -k 2 $((N+20)) $h/bin/agi-run </dev/null >$h/o 2>&1 ) &
 else ( env -i PATH=$h/bin:/usr/bin:/bin HOME=$h O=$h/t AGI_POST=stub H=claude-stub RUNTIME_DIRECTORY=$D/rt TERM=dumb timeout -k 2 $((N+20)) script -qfaO$h/o -c "$h/bin/agi-run" </dev/null >/dev/null 2>&1 ) &
 fi
 g=$!;[ $3 = killtrack ]&&{ j=0;while [ $j -lt 30 ];do v=;for q in $(mine $h);do [ "$(cat /proc/$q/comm 2>/dev/null)" = agi-track ]&&{ kill -9 $q;v=1;};done;[ "$v" ]&&break;sleep 0.1;j=$((j+1));done;}   # kill the consumer once it exists (the stub runs 2 s)
 i=0;while [ $i -lt $((N*10)) ]&&kill -0 $g 2>/dev/null;do sleep 0.1;i=$((i+1));done
 if kill -0 $g 2>/dev/null;then RS=STRAND;else RS=ended;fi
 j=0;while [ $j -lt $((N*10)) ];do n=0;for q in $(mine $h);do [ "$(cat /proc/$q/comm 2>/dev/null)" = sleep ]||n=$((n+1));done;[ $n = 0 ]&&break;sleep 0.1;j=$((j+1));done   # the settle POLLS the run's pids (council 22:51Z 10-26): done at the first read with no process but a sleep, else N s, then counted
 RL=0;RLN=;for q in $(mine $h);do c=$(cat /proc/$q/comm 2>/dev/null);[ "$c" = sleep ]||{ RL=$((RL+1));RLN="$RLN $c";};done;   # a killed loop's pending `sleep` ends by itself (<= 300 s): not a loop, not counted
 RB=$(grep -c 'Broken pipe' $h/o 2>/dev/null);RN=$(grep -c 'agi-track: append failed (.*), draining' $h/o 2>/dev/null);RF=$([ -e $h/.fresh ]&&echo y||echo n);RB=${RB:-0};RN=${RN:-0}
 for q in $(mine $h);do kill -9 $q 2>/dev/null;done;wait 2>/dev/null;rm -rf $D;}
# CELL <bindir> <path> <fault> [bare]: RUNS runs; sets E (ended) ST (strand) LF (left) BQ (broken pipe lines) NQ (named lines) FY (runs with ~/.fresh kept)
CELL(){ M=$4;LN=;E=0;ST=0;LF=0;BQ=0;NQ=0;FY=0;k=0;while [ $k -lt $RUNS ];do RUN $1 $2 $3 $M;[ $RS = ended ]&&E=$((E+1))||ST=$((ST+1));LF=$((LF+RL));LN="$LN$RLN";BQ=$((BQ+RB));NQ=$((NQ+RN));[ $RF = y ]&&FY=$((FY+1));k=$((k+1));done;}
# mutants: m1 exec back + no loop kill   m3 the one-line agi-track (no drain)
cp -r $T/b $T/mut1;cp -r $T/b $T/mut2;cp -r $T/b $T/mut3
sed -i "s/^strace -qqf -b execve -e%file -o'|agi-track' \$H \$c go;r=.*\$/exec strace -qqf -b execve -e%file -o'|agi-track' \$H \$c go/" $T/mut1/agi-run
sed -i 's/;kill \$L1 \$L2 2>\/dev\/null;exit \$r$/;exit $r/' $T/mut2/agi-run
printf '#!/bin/sh\ngrep --line-buffered -o '"'"'"/[^"]*"'"'"'|awk '"'"'!s[$0]++{print;fflush()}'"'"'>>$HOME/track\n' >$T/mut3/agi-track
[ -n "$STRAND_NOMUT" ]||{ cmp -s $T/b/agi-run $T/mut2/agi-run&&{ echo "FAIL inputs: mutant m2 changed nothing in agi-run";exit 99;};cmp -s $T/b/agi-run $T/mut1/agi-run&&{ echo "FAIL inputs: mutant m1 changed nothing in agi-run";exit 99;};cmp -s $T/b/agi-track $T/mut3/agi-track&&{ echo "FAIL inputs: mutant m3 changed nothing in agi-track";exit 99;};}
for p in clean term;do
 CELL $T/b $p none;ok s0-$p-no-fault-the-unit-ends-when-the-stub-exits "[ $E = $RUNS ]&&[ $LF = 0 ]"
 CELL $T/b $p killtrack;ok s1-$p-consumer-killed-MainPID-ends-and-nothing-of-the-run-is-left "[ $E = $RUNS ]&&[ $LF = 0 ]  # ended $E strand $ST left $LF of $RUNS runs"
 CELL $T/b $p trackro;ok s2-$p-track-unwritable-ends-0-broken-pipe-the-named-line-once-per-run "[ $E = $RUNS ]&&[ $LF = 0 ]&&[ $BQ = 0 ]&&[ $NQ = $RUNS ]  # ended $E left $LF broken-pipe $BQ named $NQ"
 ok s3-$p-fresh-written-by-the-stub-survives-the-exit "[ $FY = $RUNS ]"
done
for p in clean term;do CELL $T/b $p none bare;ok s4-$p-bare-run-the-loops-are-killed-by-pid-0-left "[ $E = $RUNS ]&&[ $LF = 0 ]  # ended $E left $LF:$LN";[ $LF = 0 ]||echo "  s4-$p left ($LF):$LN (ended $E of $RUNS)";done
if [ -z "$STRAND_NOMUT" ];then
RU=$RUNS;RUNS=4;CELL $T/mut1 clean killtrack;RUNS=$RU;ok m1-exec-back-no-kill-reads-RED-the-unit-stays-up "[ $ST -ge 1 ]  # strand $ST of $RUNS"
CELL $T/mut2 clean none bare;ok m2-loop-kill-dropped-reads-RED-the-loops-remain "[ $LF -ge 1 ]  # left $LF"
CELL $T/mut3 term trackro;ok m3-drain-dropped-reads-RED-broken-pipe-lines "[ $BQ -ge 1 ]  # broken-pipe lines $BQ"
fi
echo "agi-run-strand: $f FAIL";exit $f
