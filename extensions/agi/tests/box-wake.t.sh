#!/bin/sh
# box-wake.t.sh: goal:g7.16.1.11.20 (DG1 16:14Z; design = doc:rse-aa1-boxes AA1 wake line + AA1.M, council placement 14:54Z): messaging is box mail in the AA1.M math. A v5 post is WOKEN by polling its box (`box n|wc -l` grows -> the pane is typed `mail: box read`), in the agi-run piece (claude / pi panes) AND in the cccc.ts piece (the pi extension); the unread count is right and falls to 0 after the read; the ~/o cap is KEPT; send.py is neither touched nor left dangling.
# THE BUG (council 10-07 15:02Z, alive): the pilot's cccc.ts poll is `let s=0;setInterval(()=>{...n=+x("box n|wc -l"...);n>s&&(s=n,p.sendUserMessage("mail: box read",...))},5e3)`: s moves only UP, so after a read drops the count the NEXT mail (n <= the old maximum) never wakes the pane. agi-run's line (`...;s=$n;done`) resets s every tick and is right. Lane w4 is the bug itself: send 2, read both, send 1 = exactly ONE more wake.
# sh + git + jq + ssh-keygen + node (v24, no TypeScript syntax in the piece: the driver loads a .mjs copy) on a SCRATCH repo, throwaway keys, no live ref, no network, 0 USD. It runs the REAL pieces extracted with `sect` from the .geometry/engine*.md of ROOT (the box-mail.t.sh recipe): `box` (the AA1 sender/reader), `agi-run` (under stubs: strace, stty, a harness that idles; a `sleep` shim that divides every sleep by DIV so the 5 s poll is 0.2 s) and `cccc.ts` (under a driver.mjs that gives it a fake pi API: p.on records the handlers, p.sendUserMessage logs the wake; setInterval is divided by DIV). Wakes are counted, never assumed: agi-run's typed text goes into a FIFO this file reads; cccc.ts's sendUserMessage goes to a log.
# AGIRUN=<file> CCCC=<file> BOX=<file> AGIKID=<file> test other pieces than ROOT's (mutants / the pilot's); ROOT=<repo> where the pieces are read; DIV=<n> time scale. DEFAULT 10, NOT 25 (DG1 10-11, goal:g7.16.1.11.32; SM council 3/3): at 25 the scaled poll is 0.2 s and a burst of 3 SIGNED sends (each a git commit + ssh signing, hundreds of ms under load) spans two polls, so w2 (burst = ONE wake) and w4 (send 2, read, send 1) went RED in two solo runs and in one beside parallel lanes while the box load average was 6.8 / 7.5 / 6.3 (uptime 10:30Z 10-11) - a timing artefact, not a defect: the same tree gave 40 ok 0 FAIL at DIV=10 (poll 0.5 s). A red w2/w4 on a busy box is met by RERUNNING SOLO at the default, never by loosening the rows or lowering DIV again; a LOWER DIV (a longer poll) is the only safe direction. One ok/FAIL line per case; exit = FAIL count.
# Lanes: w1 one message wakes ONCE (and not again while it stays unread) · w2 a burst of 3 = ONE wake and the unread count is 3, then 0 after the read · w3 no mail = no wake · w4 THE BUG: send 2, read both, send 1 = exactly ONE more wake (w4b: send 1, read, send 1) · w5 a successor wakes on mail its predecessor never read (s=0 at start) · w6 an off-matrix send never wakes · w7 (agi-run) the typed line is followed by the Enter · w8 (agi-run) a PI harness (H=pi-x) wakes with the same counts as claude-x · c1-c3 the ~/o cap is KEPT (over the cap trimmed to HALF keeping the TAIL; under it untouched; the default is 64 MiB) · s1 s2 s4 DUAL ROUTE (DG1 17:54Z): the inbox file growing wakes with `mail: send.py read <seat>`, box n growing wakes with `mail: box read`, each source types its OWN line, both at once = one wake each; s3 send.py itself still resolves (control). Each lane runs on agi-run (a*) and on cccc.ts (p*) where it applies.
# DEADLINE POLLS (SM 01:0xZ 10-11: 14-15 FAIL at load 52, none at load 3): no row waits a FIXED time for an event any more. A positive event (a wake, the Enter, the trimmed file) is polled every 0.1 s up to a 40 s ceiling (until_/wk/swk); a quiet period is counted in POLLS OF THE WATCHER (box n is wrapped to log each call into $T/polls: arm = the watcher has finished one poll, so its baseline is set; tick N = N more polls started), so a loaded box stretches the wait instead of cutting it; a burst of sends is made ATOMIC by freezing the watchers (SIGSTOP, frz/thw) so it can never straddle a poll tick. Honest limit: the quiet-period checks can only be false-green (never flaky-red) under load.
# Honest limits: the poll interval and the 1 s typing pause are scaled, so the lanes pin the COMPARISON, not the wall-clock cadence; a wake is counted by the text typed / sent, not by a model turn. cccc.ts is run with node as an ES module (the real expression, not a transcription); the harness stub idles, it is not claude.
T=$(mktemp -d);f=0;G=/usr/bin/git;R0=${ROOT:-$(cd "$(dirname "$0")/../../.." && pwd)};DIV=${DIV:-25};ME=$(cd "$(dirname "$0")" && pwd)/$(basename "$0");w=
# REAP (SM 01:0xZ 10-11: a killed or timed-out run left 341 procs, 2.6 GB, in /tmp/tmp.*/r): every process the lane starts has its cwd under $T (the watchers cd there; the fifo reader too), so EVERY exit path ends by killing whatever has a cwd under $T (CONT first: a frozen one still dies; TERM, then KILL after 6 passes), then rm -rf $T. EXIT covers the normal end; INT TERM HUP exit through it (a trap is the only way a dash script runs code on a signal; SIGKILL cannot be caught by anything)
reap(){ i=0;while :;do q=;for d in /proc/[0-9]*;do case $(readlink $d/cwd 2>/dev/null) in $T|$T/*)q="$q ${d#/proc/}";;esac;done;[ -n "$q" ]||return 0;i=$((i+1));if [ $i -gt 6 ];then kill -KILL $q 2>/dev/null;else kill -CONT $q 2>/dev/null;kill -TERM $q 2>/dev/null;fi;[ $i -gt 12 ]&&return 1;/bin/sleep 0.2;done;}
trap 'reap;rm -rf $T' 0;trap 'kill $w 2>/dev/null;exit 129' HUP;trap 'kill $w 2>/dev/null;exit 130' INT;trap 'kill $w 2>/dev/null;exit 143' TERM
sect(){ cat $R0/.agi/nodes/.geometry/engine*.md|sed -n "/^###* $1 /,/^###* /{/^~~~/,/^~~~/{//!p}}";}
ok(){ if eval "$2";then echo "ok $1";else echo "FAIL $1";f=$((f+1));fi;}
wt(){ /bin/sleep $1 & w=$!;wait $w;w=;}   # interruptible: a trapped signal ends the wait at once, not after the sleep
unset GIT_AUTHOR_NAME GIT_AUTHOR_EMAIL GIT_COMMITTER_NAME GIT_COMMITTER_EMAIL GIT_DIR GIT_WORK_TREE AGI_TRUNK AGI_POST AGI_PANE_MAX_MB
mkdir -p $T/bin $T/c $T/k $T/run $T/hm/.claude
[ -n "$BOX" ]||{ sect box>$T/bin/box;BOX=$T/bin/box;};[ "$BOX" = $T/bin/box ]||cp $BOX $T/bin/box
[ -n "$AGIRUN" ]||{ sect agi-run>$T/agi-run;AGIRUN=$T/agi-run;}
[ -n "$CCCC" ]||{ sect cccc.ts>$T/cccc.mjs;CCCC=$T/cccc.mjs;};case $CCCC in *.mjs);;*)cp $CCCC $T/cccc.mjs;CCCC=$T/cccc.mjs;;esac
[ -s $BOX ]&&[ -s $AGIRUN ]&&[ -s $CCCC ]||{ echo "FAIL extract: box $(wc -c<$BOX) agi-run $(wc -c<$AGIRUN) cccc.ts $(wc -c<$CCCC)";exit 99;}
mv $T/bin/box $T/bin/box.real;printf '#!/bin/sh\n[ "$1" = n ]&&{ [ -n "$BW_UNIT" ]&&echo >>%s/boxn||echo >>%s/polls;}\nexec sh %s/bin/box.real "$@"\n' $T $T $T >$T/bin/box
# goal:g7.16.1.11.32 B (fingerprint): the unit's idle ticks no longer run `box n`, so the unit's POLL is its tick: a git shim logs the loop's one `git for-each-ref refs/box ...` per iteration (the fingerprint, $2 = refs/box; box's own call has --format as $2) into polls when the loop runs with BW_UNIT; its `box n` calls go to boxn
printf '#!/bin/sh\n[ -n "$BW_UNIT" ]&&[ "$1" = for-each-ref ]&&[ "$2" = refs/box ]&&echo >>%s/polls\nexec /usr/bin/git "$@"\n' $T >$T/bin/git;chmod +x $T/bin/git   # the poll log: one line per `box n` the watchers (or anyone) run through $T/bin
# goal:g7.16.1.11.32: the box-wake loop is the loop of agi-boxwake@.service (engine-root.md), not a background of agi-run: its body is the unit's ExecStart with %t/agi-%i -> the lane's run dir and %i -> alive; UGATE is its ExecCondition
sect agi-boxwake@.service>$T/unit;UBODY=$(sed -n "s/^ExecStart=sh -c '\(.*\)'\$/\1/p" $T/unit|sed "s,%t/agi-%i,$T/run,g;s,%i,alive,g");UGATE=$(sed -n "s/^ExecCondition=sh -c '\(.*\)'\$/\1/p" $T/unit)
[ -s $T/unit ]&&[ -n "$UBODY" ]&&[ -n "$UGATE" ]||{ echo "FAIL extract: wake unit $(wc -c<$T/unit) B, loop body $(printf %s "$UBODY"|wc -c) B, gate $(printf %s "$UGATE"|wc -c) B";exit 99;}
chmod +x $T/bin/box
# keys + signers + per-post git config (the box-mail.t.sh fixture, two posts): belam <- council (inert) <- alive; sm is a stranger two levels away
: >$T/signers
for u in belam alive dg9;do
 ssh-keygen -q -t ed25519 -N '' -f $T/k/$u -C $u>/dev/null
 echo "$u@agi namespaces=\"git\" $(cut -d' ' -f1,2 $T/k/$u.pub)">>$T/signers
 printf '[user]\n\tname=%s\n\temail=%s@agi\n\tsigningkey=%s\n[gpg]\n\tformat=ssh\n[gpg "ssh"]\n\tallowedSignersFile=%s\n[commit]\n\tgpgsign=false\n[safe]\n\tdirectory=*\n' $u $u $T/k/$u $T/signers>$T/c/$u
done
$G init -q $T/r;mkdir -p $T/r/.agi/nodes/.geometry
cat >$T/r/.agi/nodes/.geometry/posts.md<<'EOF'
  - {"name":"belam","parent":"owner","harness":"claude"}
  - {"name":"council","parent":"belam","members":["alive"]}
  - {"name":"alive","parent":"council","harness":"claude"}
  - {"name":"dg9","parent":"alive","harness":"claude"}
EOF
$G -C $T/r add -A;$G -C $T/r -c user.name=x -c user.email=x@x commit -qm fixture
# a post's environment (DG1 04:15Z: the REAL ownership): its git identity + safe.directory=* (agi-post@.service ExecStartPre #4 runs `git config --global safe.directory "*"` in the post's own HOME before any box call) under git's different-owner seam + the matrix trunk; PATH = the scratch bin (box, the stubs)
as(){ u=$1;shift;(cd $T/r&&AGI_POST=$u AGI_TRUNK=HEAD GIT_TEST_ASSUME_DIFFERENT_OWNER=1 GIT_CONFIG_GLOBAL=$T/c/$u GIT_CONFIG_SYSTEM=/dev/null PATH=$T/bin:$PATH "$@");}
snd(){ printf '%s\n' "$3"|as $1 sh $T/bin/box send $2;}        # snd FROM TO MSG
unread(){ as $1 sh $T/bin/box n|wc -l|tr -d ' ';}
rd(){ as $1 sh $T/bin/box read >/dev/null 2>&1;}
# the stubs agi-run needs: strace (drops its 5 option words, execs the harness), stty (no tty), the harness (idles), and the sleep shim
printf '#!/bin/sh\nshift 5\nexec "$@"\n'>$T/bin/strace;printf '#!/bin/sh\nexit 0\n'>$T/bin/stty;printf '#!/bin/sh\nexec tail -f /dev/null\n'>$T/bin/claude-x
printf '#!/bin/sh\ncase $1 in *[!0-9]*|"")exec /bin/sleep "$@";esac\nexec /bin/sleep $(awk "BEGIN{print $1/%s}")\n' $DIV>$T/bin/sleep
chmod +x $T/bin/strace $T/bin/stty $T/bin/claude-x $T/bin/sleep;ln -s $T/bin/claude-x $T/bin/pi-x;ln -s $T/r $T/hm/t
echo '{"hooks":{}}'>$T/hm/.claude/settings.json
# the cccc.ts driver: a fake pi API; setInterval scaled
cat >$T/drv.mjs <<'EOF'
import { pathToFileURL } from "node:url";
const real = globalThis.setInterval, div = Number(process.env.DIV || 25);
real(() => {}, 1e6);   // pi stays alive between turns; a piece with no interval of its own must not let node exit under the lane
import fs from "node:fs"; import { syncBuiltinESMExports } from "node:module";
const rw = fs.watchFile; fs.watchFile = (f, o2, cb) => rw(f, { ...o2, interval: (o2.interval || 5007) / div }, cb); syncBuiltinESMExports();
globalThis.setInterval = (f, ms, ...a) => real(f, ms / div, ...a);
const mod = await import(pathToFileURL(process.argv[2]).href), h = {};
mod.default({ on: (e, f) => { h[e] = f; }, sendUserMessage: (t) => { console.log("WAKE " + t); } });
h.session_start({ reason: "new" });
EOF
# start NAME KIND [env...]: one wake-watcher for post alive. KIND = agirun | cccc. Wakes accumulate in $T/typed.NAME (agirun: the FIFO's text) / $T/wakes.NAME (cccc: one WAKE line each)
unitloop(){ (cd $T/hm/t&&env BW_UNIT=1 HOME=$T/hm H=claude-x O=$T/r AGI_POST=alive AGI_TRUNK=HEAD GIT_TEST_ASSUME_DIFFERENT_OWNER=1 GIT_CONFIG_GLOBAL=$T/c/alive GIT_CONFIG_SYSTEM=/dev/null PATH=$T/bin:$PATH "$@" setsid sh -c "$UBODY" >$OUT 2>&1 &echo $! >>$T/pids);}
start(){ nm=$1;kd=$2;shift 2;: >$T/typed.$nm;: >$T/wakes.$nm;: >$T/polls;: >$T/boxn
 case $kd in
 agirun)rm -f $T/run/i;mkfifo $T/run/i;exec 3<>$T/run/i;(cd $T/run&&cat <&3 >>$T/typed.$nm &echo $! >>$T/pids)
  (cd $T/hm&&env HOME=$T/hm H=claude-x RUNTIME_DIRECTORY=$T/run O=$T/r AGI_POST=alive AGI_TRUNK=HEAD GIT_TEST_ASSUME_DIFFERENT_OWNER=1 GIT_CONFIG_GLOBAL=$T/c/alive GIT_CONFIG_SYSTEM=/dev/null PATH=$T/bin:$PATH "$@" setsid sh $AGIRUN >$T/ar.out.$nm 2>&1 &echo $! >>$T/pids);;
 unit)rm -f $T/run/i;mkfifo $T/run/i;exec 3<>$T/run/i;(cd $T/run&&cat <&3 >>$T/typed.$nm &echo $! >>$T/pids);OUT=$T/ar.out.$nm unitloop "$@";;
 both)start $nm agirun "$@";kd=both;OUT=$T/ar.out.$nm.u unitloop "$@";;      # start() assigns the global kd, which is also the caller's loop variable: restore it
 cccc)(cd $T/r&&env HOME=$T/hm DIV=$DIV O=$T/r AGI_POST=alive AGI_TRUNK=HEAD GIT_TEST_ASSUME_DIFFERENT_OWNER=1 GIT_CONFIG_GLOBAL=$T/c/alive GIT_CONFIG_SYSTEM=/dev/null PATH=$T/bin:$PATH "$@" node $T/drv.mjs $CCCC >$T/wakes.$nm 2>$T/node.err.$nm &echo $! >>$T/pids);;
 esac;}
stop(){ for p in $(cat $T/pids 2>/dev/null);do kill -TERM -$p 2>/dev/null;kill $p 2>/dev/null;done;: >$T/pids;exec 3<&-;/bin/sleep 0.3;}
wakes(){ case $1 in a*|u*)grep -o 'mail: box read' $T/typed.$1|wc -l|tr -d ' ';;*)grep -c '^WAKE mail: box read' $T/wakes.$1|tr -d ' ';;esac;}
reset(){ stop;rm -rf $T/r/.git/refs/box $T/r/.git/refs/held;}
until_(){ i=0;while [ $i -lt ${2:-400} ];do eval "$1"&&return 0;/bin/sleep 0.1;i=$((i+1));done;return 1;}   # until_ 'CMD' [TENTHS]: poll every 0.1 s, ceiling 40 s
polls(){ wc -l <$T/polls 2>/dev/null|tr -d ' ';}
wk(){ until_ "[ \$(wakes $1) -ge $2 ]";}      # wk NAME N: wait (deadline) until NAME has woken N times
arm(){ until_ '[ $(polls) -ge 2 ]';}            # the watcher has FINISHED one poll (the second began): its baseline is set, a send now is a change
tick(){ p0=$(polls);until_ "[ \$(polls) -ge $((p0+$1)) ]";}   # tick N: N more polls of the watcher have started (a loaded box stretches it)
frz(){ fz=;j=0;while [ $j -lt 2 ];do for d in /proc/[0-9]*;do case $(readlink $d/cwd 2>/dev/null) in $T|$T/*)kill -STOP ${d#/proc/} 2>/dev/null&&fz="$fz ${d#/proc/}";;esac;done;/bin/sleep 0.1;j=$((j+1));done;}   # freeze every watcher process (two sweeps: a child forked during the first is caught by the second)
thw(){ kill -CONT $fz 2>/dev/null;fz=;}
[ -n "$BW_LEAK" ]&&{ reset;start L1 agirun;start L2 cccc;: >$T/up;wt 600;exit 0;}   # the leak row below runs THIS lane in this mode: two watchers up, then idle until it is killed
for kd in unit cccc;do case $kd in unit)N=u;;*)N=p;;esac
# ---- w3: no mail = no wake
reset;start ${N}3 $kd;arm;tick 8;ok "w3-$kd-no-mail-no-wake no mail for 2 s of polling: $(wakes ${N}3) wake(s) (want 0); the watcher is up (typed/wake file exists)" '[ "$(wakes ${N}3)" = 0 ]'
# ---- w1: one message wakes ONCE, and not again while it stays unread
snd belam alive "hello one";wk ${N}3 1;tick 3;w1a=$(wakes ${N}3);tick 6;w1b=$(wakes ${N}3)
ok "w1-$kd-one-message-wakes-once belam -> alive (adjacent, level a()): ONE wake after the send ($w1a) and still one after 1.5 s more of polling ($w1b: an unread message never re-wakes); the unread count is $(unread alive) (want 1)" '[ "$w1a" = 1 ]&&[ "$w1b" = 1 ]&&[ "$(unread alive)" = 1 ]'
# ---- w2: a burst of 3 = ONE wake; count 3, then 0 after the read
reset;start ${N}2 $kd;arm;frz;snd belam alive m1;snd belam alive m2;snd belam alive m3;thw;u3=$(unread alive);wk ${N}2 1;tick 8;w2=$(wakes ${N}2);rd alive;u0=$(unread alive)
ok "w2-$kd-unread-count-and-burst three sends: the unread count is $u3 (want 3), ONE wake for the burst ($w2), and after box read the count is $u0 (want 0)" '[ "$u3" = 3 ]&&[ "$w2" = 1 ]&&[ "$u0" = 0 ]'
# ---- w4: THE BUG. send 2, read both, send 1 = exactly ONE more wake for that 1
reset;start ${N}4 $kd;arm;frz;snd belam alive a1;snd belam alive a2;thw;wk ${N}4 1;tick 3;w4a=$(wakes ${N}4);rd alive;tick 3;u4=$(unread alive);snd belam alive b1;wk ${N}4 2;tick 4;w4b=$(wakes ${N}4)
ok "w4-$kd-wake-after-read send 2 (wakes $w4a, want 1), read both (count $u4, want 0), send 1: the next mail wakes the pane, exactly ONE more wake (total $w4b, want 2); the pilot's n>s&&(s=n,...) never fires here because s stays at 2" '[ "$w4a" = 1 ]&&[ "$u4" = 0 ]&&[ "$w4b" = 2 ]'
# ---- w4b: the simplest shape of the same bug: send 1, read, send 1
reset;start ${N}5 $kd;arm;snd belam alive c1;wk ${N}5 1;rd alive;tick 3;snd belam alive c2;wk ${N}5 2;tick 4;w5=$(wakes ${N}5)
ok "w4b-$kd-same-count-again send 1 (wake), read it, send 1 again (the count is back to 1, equal to the old maximum): the second mail wakes too, total $w5 (want 2)" '[ "$w5" = 2 ]'
# ---- w5: a successor wakes on mail its predecessor never read (s=0 at start)
reset;snd belam alive pre1;snd belam alive pre2;start ${N}6 $kd;wk ${N}6 1;tick 6;w6=$(wakes ${N}6)
ok "w5-$kd-successor-wakes-on-unread two messages unread BEFORE the watcher starts: it wakes at once, once ($w6, want 1)" '[ "$w6" = 1 ]'
# ---- w6: an off-matrix send (dg9 -> belam: levels 3 and 1) is refused by level a() and never wakes
reset;start ${N}7 $kd;arm;snd dg9 belam nope >/dev/null 2>&1;snd dg9 alive adj >/dev/null 2>&1;wk ${N}7 1;tick 6;w7=$(wakes ${N}7)
ok "w6-$kd-adjacent-wakes-off-matrix-does-not dg9 -> belam is off-matrix (nothing sent, no wake for belam's box); dg9 -> alive is adjacent: alive's watcher wakes once ($w7, want 1)" '[ "$w7" = 1 ]&&[ "$(unread belam)" = 0 ]'
[ $kd = unit ]&&{ reset;start u11 unit;arm;snd belam alive e1;wk u11 1;until_ '[ $(tr -cd "\r" <$T/typed.u11|wc -c|tr -d " ") -ge 1 ]';tick 4;w8=$(wakes u11);cr=$(tr -cd '\r' <$T/typed.u11|wc -c|tr -d ' ')
ok "w7-unit-types-the-Enter after the typed line the poll presses Enter (a CR): $w8 wake(s), $cr CR(s) typed (want equal and 1); without it the pane holds the line unsent" '[ "$w8" = 1 ]&&[ "$cr" = 1 ]';}
[ $kd = unit ]&&{ g1=$(H=claude-x sh -c "$UGATE" >/dev/null 2>&1;echo $?);g2=$(H='claude --remote-control alive --model m --effort high --permission-mode bypassPermissions' sh -c "$UGATE" >/dev/null 2>&1;echo $?);g3=$(H='node /opt/pi/pi --provider openrouter --model m --thinking high --skill skills -e ../bin/cccc.ts' sh -c "$UGATE" >/dev/null 2>&1;echo $?);g4=$(H=pi-x sh -c "$UGATE" >/dev/null 2>&1;echo $?);g5=$(env -u H sh -c "$UGATE" >/dev/null 2>&1;echo $?);g6=$(H= sh -c "$UGATE" >/dev/null 2>&1;echo $?)
ok "w8-unit-gates-itself-on-the-harness (goal:g7.16.1.11.32; replaces the old pi-x row, a green row on a dead branch: production never sets such an H) the unit's ExecCondition exits 0 for claude-x ($g1) and for a real claude command line ($g2) and 2 (a SKIP, not a failure) for a REAL pi post's H, which starts 'node ' ($g3) and for pi-x ($g4): a pi post is woken by the cccc.ts interval alone, never twice; with NO H ($g5) or an EMPTY H ($g6) it exits 255, a FAILED unit that is seen, never a silent skip (council condition, SM 11:0xZ)" '[ "$g1" = 0 ]&&[ "$g2" = 0 ]&&[ "$g3" = 2 ]&&[ "$g4" = 2 ]&&[ "$g5" = 255 ]&&[ "$g6" = 255 ]';}
done
# ---- DUAL ROUTE (DG1 17:54Z, SM's catch on 954522af59): send.py never writes box mail, so the inbox poll stays until its callers are on box. The wake has TWO sources, each types its OWN line: the inbox file growing -> 'mail: send.py read alive', box n growing -> 'mail: box read'. agi-run (claude-x) and cccc.ts (the watchFile interval is scaled by the driver like setInterval).
ibf=$T/r/.agi/sessions/inbox/alive.md;mkdir -p $T/r/.agi/sessions/inbox
ib(){ printf 'ts: x\nfrom: belam\n\n%s\n' "$1">>$ibf;}   # a send.py-style append: it writes ONLY the inbox file
sw(){ case $1 in a*|u*)grep -o 'mail: send.py read alive' $T/typed.$1|wc -l|tr -d ' ';;*)grep -c '^WAKE mail: send.py read alive' $T/wakes.$1|tr -d ' ';;esac;}
swk(){ until_ "[ \$(sw $1) -ge $2 ]";}      # swk NAME N: wait (deadline) until NAME has typed the send.py line N times
for kd in both cccc;do case $kd in both)N=a;;*)N=p;;esac
# s1: the inbox route is a CONTROL now: growth wakes ONCE with the send.py line, not again while unchanged, and a further append wakes again
reset;rm -f $ibf;start ${N}20 $kd;arm;ib one;swk ${N}20 1;tick 3;i1=$(sw ${N}20);tick 6;i1b=$(sw ${N}20);ib two;swk ${N}20 2;tick 3;i2=$(sw ${N}20);: >$ibf;tick 6;i3=$(sw ${N}20);ib three;swk ${N}20 3;tick 3;i4=$(sw ${N}20);b0=$(wakes ${N}20)
ok "s1-$kd-inbox-growth-wakes-send-py-read an append to sessions/inbox/alive.md (nothing else) types 'mail: send.py read alive': ONE wake ($i1), still one later ($i1b), a second append wakes again ($i2, want 2), the inbox SHRINKING (truncated to 0) never wakes ($i3, want 2) and an append after it wakes again ($i4, want 3: the counter follows the size down); and NO 'mail: box read' for it ($b0, want 0)" '[ "$i1" = 1 ]&&[ "$i1b" = 1 ]&&[ "$i2" = 2 ]&&[ "$i3" = 2 ]&&[ "$i4" = 3 ]&&[ "$b0" = 0 ]'
# s2: box mail types ITS line only (the inbox already holds old bytes: the box counter is not the inbox size)
reset;rm -f $ibf;ib "old mail already in the inbox, long enough to exceed any box count";start ${N}21 $kd;arm;snd belam alive bx1;wk ${N}21 1;tick 3;x1=$(wakes ${N}21);y1=$(sw ${N}21);tick 6;x1b=$(wakes ${N}21)
ok "s2-$kd-box-mail-types-box-read a box send (nothing in the inbox file moves; the inbox already holds old bytes) types 'mail: box read' ONCE ($x1, still $x1b) and never 'mail: send.py read' ($y1, want 0)" '[ "$x1" = 1 ]&&[ "$x1b" = 1 ]&&[ "$y1" = 0 ]'
# s4: both sources grow in the same window: one wake per source, neither lost, at most two
reset;rm -f $ibf;start ${N}22 $kd;arm;ib both;snd belam alive bboth;wk ${N}22 1;swk ${N}22 1;tick 6;z1=$(wakes ${N}22);z2=$(sw ${N}22)
ok "s4-$kd-both-sources-one-wake-each an inbox append AND a box send in the same window: $z1 box-read wake(s) and $z2 send.py-read wake(s) (want 1 and 1: two at most, neither lost, neither counted for the other)" '[ "$z1" = 1 ]&&[ "$z2" = 1 ]'
done
reset;rm -f $ibf
# ---- F2 (goal:g7.16.1.11.32): every loop survives a KILLED sleep and fires on the next tick. The kill is scoped to ONE setsid group (pkill -g): a sleep of the box's real posts is never touched
killsl(){ g=$(tail -1 $T/pids);for k in 1 2 3 4 5 6;do pkill -KILL -x sleep -g $g 2>/dev/null;/bin/sleep 0.1;done;}
reset;start u50 unit;wt 0.6;killsl;ua=$(kill -0 $(tail -1 $T/pids) 2>/dev/null&&echo up||echo DEAD);snd belam alive k1;wk u50 1;tick 3;u50=$(wakes u50)
ok "f2-unit-loop-survives-a-killed-sleep the wake unit's loop body, its sleep SIGKILLed six times over 0.6 s: the loop is $ua (want up) and a box send afterwards still types the line ONCE ($u50, want 1); a 'while sleep' loop ends at the first kill" '[ "$ua" = up ]&&[ "$u50" = 1 ]'
reset;rm -f $ibf;start a51 agirun;wt 0.6;killsl;ib killed;swk a51 1;tick 3;i50=$(sw a51)
ok "f2-agi-run-inbox-loop-survives-a-killed-sleep agi-run's send.py inbox loop (goal:g7.16.1.11.27 retires it later), its sleep SIGKILLed: an inbox append afterwards still types 'mail: send.py read alive' ONCE ($i50, want 1)" '[ "$i50" = 1 ]'
reset;rm -f $ibf
# ---- w9 (council remark 11:46Z): a HUNG `box n` (timeout 20, scaled by DIV) neither loses the wake nor repeats it: s is KEPT on a failed count. A hang that set n=0 and s=0 re-typed 'mail: box read' for mail already announced.
mkdir -p $T/binH;printf '#!/bin/sh\n[ "$1" = n ]&&[ -e %s/hang ]&&exec /bin/sleep 60\nexec %s/bin/box "$@"\n' $T/hm $T >$T/binH/box;printf '#!/bin/sh\nt=$1;shift\nexec /usr/bin/timeout $(awk "BEGIN{print $t/%s}") "$@"\n' $DIV >$T/binH/timeout;chmod +x $T/binH/box $T/binH/timeout
reset;rm -f $T/hm/hang;start u70 unit PATH=$T/binH:$T/bin:/usr/bin:/bin;arm;snd belam alive h1;wk u70 1;tick 3;h1=$(wakes u70)
: >$T/hm/hang;wt 5;h2=$(wakes u70);rm -f $T/hm/hang;wt 2;h3=$(wakes u70);snd belam alive h2;wk u70 2;tick 3;h4=$(wakes u70)
ok "w9-unit-a-hung-box-n-neither-loses-nor-repeats-the-wake one send: $h1 wake (want 1); the box hung for 5 s (every count times out): still $h2 (want 1); the box back: still $h3 (want 1: the hang did not reset s, so the announced mail is not re-announced); a second send wakes ($h4, want 2: the loop lived through the hang)" '[ "$h1" = 1 ]&&[ "$h2" = 1 ]&&[ "$h3" = 1 ]&&[ "$h4" = 2 ]'
reset;rm -f $T/hm/hang
# ---- w9b (goal:g7.16.1.11.32 B): the fingerprint changes while the box HANGS: the mail is neither lost nor announced early. A send during the hang changes the refs, every tick then tries `box n` (timeout, scaled), `||continue` keeps p and s, and when the box answers the wake comes ONCE.
reset;rm -f $T/hm/hang;start u71 unit PATH=$T/binH:$T/bin:/usr/bin:/bin;arm;snd belam alive g1;wk u71 1;tick 3;c0=$(wakes u71)
: >$T/hm/hang;snd belam alive g2;wt 4;c1=$(wakes u71);rm -f $T/hm/hang;wk u71 2;tick 4;c2=$(wakes u71)
ok "w9b-unit-a-send-during-a-hang-wakes-once-when-the-box-answers one send: $c0 wake (want 1); a second send while every box n hangs (4 s): still $c1 (want 1: no wake before the count exists); the box back: $c2 (want 2: ONE wake for it, not lost, not repeated)" '[ "$c0" = 1 ]&&[ "$c1" = 1 ]&&[ "$c2" = 2 ]'
reset;rm -f $T/hm/hang
# ---- w10 (goal:g7.16.1.11.32 B, belam: ~3% of a core per unit x 12): an IDLE unit loop runs `box n` once per twelve ticks (the bounded refresh: the matrix and the signers are not in the fingerprint), not once per tick. 24 ticks with nothing changing: at most 3 box n (2 by design), at least 1; MUTANT: the fingerprint compare removed = a box n every tick.
reset;start u80 unit;arm;tick 1;b0=$(wc -l <$T/boxn|tr -d ' ');tick 24;b1=$(wc -l <$T/boxn|tr -d ' ');idle=$((b1-b0));stop
UB0=$UBODY;UBODY=$(printf '%s' "$UBODY"|sed 's/\[ "\$f" = "\$p" \]&&\[ \$k -lt 12 \]&&continue;//');[ "$UBODY" != "$UB0" ]&&mut=cut||mut=NOT-CUT
reset;start u81 unit;arm;tick 1;m0=$(wc -l <$T/boxn|tr -d ' ');tick 24;m1=$(wc -l <$T/boxn|tr -d ' ');midle=$((m1-m0));stop;UBODY=$UB0
ok "w10-unit-an-idle-loop-runs-box-n-once-per-twelve-ticks 24 idle ticks ran box n $idle time(s) (want 1..3); the mutant without the skip line ($mut) ran it $midle (want >= 20: a box n every tick)" '[ "$idle" -ge 1 ]&&[ "$idle" -le 3 ]&&[ "$mut" = cut ]&&[ "$midle" -ge 20 ]'
reset
# ---- F4b: the unit's loop on the REAL box piece with the env agi-project WRITES (H, AGI_TRUNK, AGI_BOX from agi-boxwake@alive.service.d/h.conf, never set by hand), plus the unit's OWN Environment= lines, under env -i: a silent count of 0 (a wrong cwd, a missing variable) cannot pass
mkdir -p $T/pr/.agi/nodes/.geometry $T/pj $T/fk;cp $R0/.agi/nodes/.geometry/engine*.md $T/pr/.agi/nodes/.geometry/
{ printf -- '---\nposts:\n';printf '  - {"name": "alive", "boot": true, "engine": {"v": 4, "harness": "claude-code", "model": "m", "effort": "high", "trunk": "HEAD"}, "role": "director", "tier": 1, "box": "local-town"}\n';} >$T/pr/.agi/nodes/.geometry/posts.md
$G init -q $T/pr;$G -C $T/pr add -A;$G -C $T/pr -c user.name=x -c user.email=x@x commit -qm p;PRR=$($G -C $T/pr rev-parse HEAD);sect agi-project>$T/proj.sh
(cd $T/pr&&env -i PATH=$T/fk:/usr/bin:/bin HOME=$T/hm GIT_CONFIG_GLOBAL=$T/c/alive GIT_CONFIG_SYSTEM=/dev/null AGI_BOX=local-town GIT_TEST_ASSUME_DIFFERENT_OWNER=1 timeout 60 sh -s $T/pj $PRR <$T/proj.sh >$T/pj.out 2>$T/pj.err);pjrc=$?
hc=$T/pj/agi-boxwake@alive.service.d/h.conf;UENV=$(sed -n 's/^Environment=//p' $T/unit|sed "s,%i,alive,g;s,PATH=[^ ]*,PATH=$T/bin:/usr/bin:/bin,"|tr '\n' ' ')
reset;rm -f $T/run/i;mkfifo $T/run/i;exec 3<>$T/run/i;: >$T/typed.u60;cat <&3 >>$T/typed.u60 &echo $! >>$T/pids
(cd $T/hm/t&&eval "set -- $(sed -n 's/^Environment=//p' $hc 2>/dev/null)"&&env -i BW_UNIT=1 HOME=$T/hm "$@" O=$T/r $UENV GIT_TEST_ASSUME_DIFFERENT_OWNER=1 GIT_CONFIG_GLOBAL=$T/c/alive GIT_CONFIG_SYSTEM=/dev/null setsid sh -c "$UBODY" >$T/ar.out.u60 2>&1 &echo $! >>$T/pids)
hh=$(sed -n 's/^Environment="\(H=[^"]*\)".*/\1/p' $hc 2>/dev/null);hgate=$(env -i PATH=/usr/bin:/bin "$hh" sh -c "$UGATE" >/dev/null 2>&1;echo $?);htr=$(grep -c '"AGI_TRUNK=HEAD"' $hc 2>/dev/null);hbx=$(grep -c 'AGI_BOX=local-town' $hc 2>/dev/null)
arm;snd belam alive real1;wk u60 1;tick 3;ur=$(wakes u60);stop
ok "f4b-unit-loop-on-the-real-box-in-the-env-agi-project-wrote agi-project (rc $pjrc, want 0) wrote agi-boxwake@.service ($([ -s $T/pj/agi-boxwake@.service ]&&echo yes||echo NO)) and the wake drop-in h.conf ($([ -s $hc ]&&echo yes||echo NO)): its H passes the unit's own ExecCondition (rc $hgate, want 0), it carries AGI_TRUNK=HEAD ($htr) and AGI_BOX=local-town ($hbx) (want 1 1); the loop body under env -i plus that file plus the unit's Environment lines, with the REAL box piece and one unread message, types 'mail: box read' ONCE ($ur, want 1)" '[ "$pjrc" = 0 ]&&[ -s $T/pj/agi-boxwake@.service ]&&[ -s $hc ]&&[ "$hgate" = 0 ]&&[ "$htr" = 1 ]&&[ "$hbx" = 1 ]&&[ "$ur" = 1 ]'
reset
# ---- R6 R7 N10 N11 (DG1 19:27Z, SM's final on d926526a71): the RECEIVER pieces run on the REAL unit env: engine-root.md then set only the retired identity variable (the box piece wants AGI_POST), so start() above no longer exports AGI_POST (as() still does: it models the SENDER / the agent reading its mail, which is the box piece's own env, banked). binF = a `box` that fails with stderr text; binA = NO box at all (PATH without any host bin dir)
mkdir -p $T/binF $T/binA;cp $T/bin/strace $T/bin/stty $T/bin/claude-x $T/bin/sleep $T/binF/;cp $T/bin/strace $T/bin/stty $T/bin/claude-x $T/bin/sleep $T/binA/;ln -sf $T/binF/claude-x $T/binF/pi-x;ln -sf $T/binA/claude-x $T/binA/pi-x;printf '#!/bin/sh\necho "box: boom, the refs are unreadable" >&2\nexit 1\n'>$T/binF/box;chmod +x $T/binF/box
for kd in unit cccc;do case $kd in unit)N=u;;*)N=p;;esac
# r6: the unit's env as it is (goal:g7.16.1.11.37 retired the old identity variable from it; the box piece REQUIRES AGI_POST and dies without it): a box send wakes ONCE
reset;start ${N}30 $kd;arm;snd belam alive r6;wk ${N}30 1;tick 3;r6a=$(wakes ${N}30);tick 6;r6b=$(wakes ${N}30);r6p=$(tr '\0' '\n' </proc/$(cat $T/pids|tail -1)/environ 2>/dev/null|grep -c '^AGI_POST=')
ok "r6-$kd-wakes-on-the-unit-env the watcher in the unit's own env (AGI_POST set; for the unit kind /proc environ carries $r6p AGI_POST entries, want 1) a box send wakes ONCE ($r6a, still $r6b later); the box piece needs AGI_POST and dies silently without it" '[ "$r6a" = 1 ]&&[ "$r6b" = 1 ]&&{ [ $kd != unit ]||[ "$r6p" = 1 ]; }'
# r7: box failing / absent: 0 wakes and 0 bytes of error over ~12 ticks
reset;start ${N}31 $kd PATH=$T/binF:/usr/local/bin:/usr/bin:/bin;wt 2.5;f7=$(wakes ${N}31);case $kd in unit)e7=$(wc -c <$T/ar.out.${N}31);;*)e7=$(wc -c <$T/node.err.${N}31);esac;stop
reset;start ${N}32 $kd PATH=$T/binA:/usr/local/bin:/usr/bin:/bin;wt 2.5;f8=$(wakes ${N}32);case $kd in unit)e8=$(wc -c <$T/ar.out.${N}32);;*)e8=$(wc -c <$T/node.err.${N}32);esac;stop
ok "r7-$kd-a-failing-or-absent-box-is-silent over ~12 ticks a box that exits 1 with stderr text: $f7 wake(s), $e7 byte(s) of error output; NO box at all: $f8 wake(s), $e8 byte(s) (want 0 wakes and 0 bytes both: a 5 s poll must not fill the pane / stderr with noise)" '[ "$f7" = 0 ]&&[ "$e7" = 0 ]&&[ "$f8" = 0 ]&&[ "$e8" = 0 ]'
# n11: a forged / off-matrix ref (refs/box/ghost/alive: 'ghost' is no post) makes `box n` print '[off-matrix] ghost': that line is NOT a message
reset;git -C $T/r update-ref refs/box/ghost/alive $(git -C $T/r rev-parse HEAD);start ${N}33 $kd;arm;tick 8;g1=$(wakes ${N}33);snd belam alive real1;wk ${N}33 1;tick 3;g2=$(wakes ${N}33)
ok "n11-$kd-off-matrix-line-is-not-mail a forged ref refs/box/ghost/alive ('box n' prints '[off-matrix] ghost'): $g1 wake(s) for it (want 0), and a real message right after wakes ONCE ($g2, want 1)" '[ "$g1" = 0 ]&&[ "$g2" = 1 ]'
done
reset
# n10: cccc.ts's own timers must not keep node alive (agi-kid runs `pi -e cccc.ts -p`; pi drains, the process must exit): the driver WITHOUT its keep-alive line exits on its own
grep -v '^real(() => {}, 1e6);' $T/drv.mjs >$T/drv-nokeep.mjs
(cd $T/r&&env HOME=$T/hm DIV=$DIV O=$T/r AGI_TRUNK=HEAD GIT_TEST_ASSUME_DIFFERENT_OWNER=1 GIT_CONFIG_GLOBAL=$T/c/alive GIT_CONFIG_SYSTEM=/dev/null PATH=$T/bin:$PATH timeout 40 node $T/drv-nokeep.mjs $CCCC >$T/nk.out 2>&1);nkrc=$?
ok "n10-cccc-timers-alone-do-not-keep-node-alive the fake pi driver WITHOUT its own keep-alive, after the last event: node exits by itself (rc $nkrc, want 0; 124 = still running at the 6 s limit: the poll interval keeps a drained pi alive)" '[ $nkrc = 0 ]'
# ---- R9 (DG1 20:37Z, SM mur residue on f8c0ba9ef2): in a KID started BEFORE goal:g7.16.1.11.24 (a pre-cut agi-kid) the env carried AGI_POST=<parent> (inherited) AND the retired variable =<kid>; since that cut agi-kid sets AGI_POST=$k itself (the p44/p45 rows below take the kid env FROM agi-kid's own text), and these p40..p43 rows stay as the ORDER guard of cccc.ts (the kid variable first, never flipped). The cccc.ts poll had to ask `box n` as the KID (the kid variable before AGI_POST, ruled), not AGI_POST first, which asks as the parent and wakes the kid for the parent's mail. The stub box answers n>0 ONLY for the asker named in $T/who; in a post (POST=SEAT) and a pre-unit post (SEAT only) both orders agree
mkdir -p $T/binK;cp $T/bin/strace $T/bin/stty $T/bin/claude-x $T/bin/sleep $T/binK/
printf '#!/bin/sh\n[ "$1" = n ]&&[ "$AGI_POST" = "$(cat %s/who)" ]&&echo from-someone\nexit 0\n' $T >$T/binK/box;chmod +x $T/binK/box
# r9 p40-p43 (RETIRED, goal:g7.16.1.11.32): they modelled a KID whose env carried AGI_POST=<parent> AND the retired variable =<kid>, with cccc.ts choosing it over AGI_POST. cccc.ts no longer reads it (it polls with the inherited env and the box piece needs AGI_POST) and goal:g7.16.1.11.37 retired it from the engine, so a row that sets it tests nothing that runs. The kid's env is taken FROM agi-kid's own text below (p44/p45), the one place it is built.
# ---- goal:g7.16.1.11.24 (belam-s2-II 02:4xZ 10-10): the kid env is TAKEN FROM agi-kid's own text, never hand-written -- the words of its `exec pi` line that read AGI_*=$k, $k = kid9. The cccc.ts poll in that env asks `box n` as the KID: a box that answers ONLY for the parent 'alive' wakes it 0 times; one that answers for 'kid9' wakes it once
[ -n "$AGIKID" ]||{ sect agi-kid>$T/agi-kid;AGIKID=$T/agi-kid;}
grep 'exec pi' $AGIKID|tr ' ' '\n'|grep -E '^AGI_[A-Z_]+=\$k$'|sed 's/\$k/kid9/'>$T/kidenv;KENV=$(cat $T/kidenv)
reset;echo alive >$T/who;start p44 cccc $KENV PATH=$T/binK:$PATH;wt 2.5;k5=$(wakes p44);stop
reset;echo kid9 >$T/who;start p45 cccc $KENV PATH=$T/binK:$PATH;wk p45 1;wt 1;k6=$(wakes p45);stop
ok "r9-kid-env-from-agi-kid-sets-AGI_POST agi-kid's own exec line carries AGI_POST=\$k (the words read: [$(echo $KENV)]; want AGI_POST=kid9: goal:g7.16.1.11.37 retired the old variable), so no identity reader in a kid's env resolves to the parent" '[ "$(echo $KENV)" = "AGI_POST=kid9" ]'
ok "r9-kid-env-from-agi-kid-asks-as-the-kid cccc.ts in the env agi-kid builds, a box that answers n>0 ONLY for the parent 'alive': $k5 wake(s) (want 0); ONLY for 'kid9': $k6 wake (want 1)" '[ "$k5" = 0 ]&&[ "$k6" = 1 ]'
# ---- the ~/o cap (agi-run only): the 5-minute loop trims ~/o to HALF the cap keeping the TAIL when it is over AGI_PANE_MAX_MB (default 64); DIV scales the 300 s
capsz(){ stat -c%s $T/hm/o 2>/dev/null||echo 0;}
mkbig(){ rm -f $T/hm/o;awk -v n=$1 'BEGIN{for(i=0;i<n;i++)printf "%07d line of the pane log, padding padding padding padding padding\n", i}' >$T/hm/o;}
printf '#!/bin/sh\ncase $1 in *[!0-9]*|"")exec /bin/sleep "$@";esac\nexec /bin/sleep $(awk "BEGIN{print $1/100}")\n'>$T/bin/sleep   # the cap loop sleeps 300 s: scale it harder
mkbig 50000;cp $T/hm/o $T/o.orig;sz0=$(capsz);start a8 agirun AGI_PANE_MAX_MB=1;until_ '[ $(capsz) = 524288 ]';sz1=$(capsz);stop
tailn=$((1<<19));tail -c $tailn $T/o.orig >$T/o.tail
ok "c1-cap-trims-to-half-keeping-the-tail ~/o of $sz0 B with AGI_PANE_MAX_MB=1: after one loop it is $sz1 B (want $tailn = half the cap) and holds the LAST $tailn bytes of the original (cmp: $(cmp -s $T/hm/o $T/o.tail&&echo same||echo DIFFERENT))" '[ "$sz1" = $tailn ]&&cmp -s $T/hm/o $T/o.tail'
awk 'BEGIN{for(i=0;i<500;i++)printf "%07d small\n", i}' >$T/hm/o;cp $T/hm/o $T/o.small;start a9 agirun AGI_PANE_MAX_MB=1;wt 5;stop
ok "c2-under-the-cap-untouched a ~/o under the cap is byte-identical after the loop ($(cmp -s $T/hm/o $T/o.small&&echo same||echo CHANGED), $(capsz) B)" 'cmp -s $T/hm/o $T/o.small'
rm -f $T/hm/o;truncate -s 70M $T/hm/o;start a10 agirun;until_ '[ $(capsz) = 33554432 ]';sz2=$(capsz);stop;rm -f $T/hm/o
ok "c3-default-cap-is-64-MiB with AGI_PANE_MAX_MB unset a 70 MiB ~/o is trimmed to $sz2 B (want $((32<<20)) = half of 64 MiB)" '[ "$sz2" = $((32<<20)) ]'

# ---- F2 for the pane-cap loop (agi-run, `while :;do sleep 300||:`): its sleep SIGKILLed at once, the loop still trims ~/o
mkbig 50000;start a53 agirun AGI_PANE_MAX_MB=1;killsl;wt 5;sz3=$(capsz);stop
ok "f2-pane-cap-loop-survives-a-killed-sleep ~/o of 50000 lines with AGI_PANE_MAX_MB=1, the loop's sleep SIGKILLed six times at the start: after 5 s it is $sz3 B (want $tailn = half the cap: the loop kept running); a 'while sleep 300' loop dies at the first kill and never trims" '[ "$sz3" = $tailn ]'
# ---- send.py: no dangling caller in the two pieces; send.py itself resolves
SP=$R0/extensions/agi/bin/send.py;python3 $SP --help >/dev/null 2>&1;sprc=$?
ok "s3-send-py-still-resolves (control) extensions/agi/bin/send.py is there ($([ -f $SP ]&&echo yes||echo NO)) and answers --help (rc $sprc): this goal retires no send.py caller it has not replaced" '[ -f $SP ]&&[ $sprc = 0 ]'
# z1 (DG1 04:44Z re-scope: the real-ownership env is the DEFAULT of every A-range lane): box and agi-run read the post's OWN repo under the post's OWN global (identity + safe.directory=*, what ExecStartPre #4 and the engine gitconfig piece give it), never a foreign-uid repo, so the env is on by default and ONE row proves it: with an empty config and git's different-owner seam a plain read of the lane's repo is refused as dubious ownership; with the post's lane config it works
sn=$(cd $T/r&&env -i PATH=$PATH HOME=$T/hm GIT_CONFIG_GLOBAL=/dev/null GIT_CONFIG_SYSTEM=/dev/null GIT_TEST_ASSUME_DIFFERENT_OWNER=1 git rev-parse HEAD 2>&1|grep -c 'dubious ownership');gn=$(cd $T/r&&env -i PATH=$PATH HOME=$T/hm GIT_CONFIG_GLOBAL=$T/c/belam GIT_CONFIG_SYSTEM=/dev/null GIT_TEST_ASSUME_DIFFERENT_OWNER=1 git rev-parse HEAD >/dev/null 2>&1;echo $?)
ok "z1-real-ownership-default-is-on a plain git read of the lane's repo under an empty config + GIT_TEST_ASSUME_DIFFERENT_OWNER=1: $sn dubious-ownership line(s) (want 1: the seam bites); with a post's lane config (safe.directory=*): rc $gn (want 0)" '[ "$sn" = 1 ]&&[ "$gn" = 0 ]'
# ---- LK (SM 01:0xZ 10-11): a KILLED run leaves no process behind. The lane re-runs ITSELF in BW_LEAK mode (two watchers up, then idle) under its own TMPDIR, is sent TERM / INT / HUP once the watchers are up, and must exit with 128+n, leave NO process whose cwd is under its temp dir and no temp dir. A launcher resets SIGINT and SIGHUP to default (a lane started under nohup or a CI job inherits SIGHUP ignored, and an ignored signal cannot be trapped) (an async job of a non-interactive shell ignores it, as does anything started with `&` from this lane; a ^C in a terminal does not)
cnt(){ c=0;for d in /proc/[0-9]*;do case $(readlink $d/cwd 2>/dev/null) in $1|$1/*)c=$((c+1));;esac;done;echo $c;}
for sg in TERM INT HUP;do
 LK=$T/lk$sg;mkdir -p $LK;env BW_LEAK=1 TMPDIR=$LK ROOT=$R0 DIV=$DIV python3 -I -c 'import os,signal,sys;signal.signal(signal.SIGINT,signal.SIG_DFL);signal.signal(signal.SIGHUP,signal.SIG_DFL);os.execv("/bin/sh",["sh"]+sys.argv[1:])' "$ME" >$T/lk$sg.out 2>&1 &
 lp=$!;until_ "ls $LK/tmp.*/up >/dev/null 2>&1&&[ \$(cnt $LK) -ge 4 ]" 600;pre=$(cnt $LK)
 kill -$sg $lp;until_ "[ \$(cnt $LK) = 0 ]&&[ -z \"\$(ls -A $LK)\" ]" 900;post=$(cnt $LK);left=$(ls -A $LK|wc -l|tr -d ' ');kill -KILL $lp 2>/dev/null;wait $lp;lrc=$?
 case $sg in TERM)want=143;; INT)want=130;; HUP)want=129;; esac
 ok "lk-$sg-a-killed-run-leaves-nothing the lane in BW_LEAK mode (an agi-run and a cccc watcher up): $pre process(es) with a cwd under its temp dir before the signal (want >= 4: the agi-run shell, the poll, the fifo reader, node), then $sg: exit $lrc (want $want), $post process(es) left (want 0), $left temp entr(ies) left (want 0)" '[ "$pre" -ge 4 ]&&[ "$lrc" = $want ]&&[ "$post" = 0 ]&&[ "$left" = 0 ]'
done
echo "box-wake: $f FAIL"
exit $f
