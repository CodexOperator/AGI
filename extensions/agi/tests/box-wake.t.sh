#!/bin/sh
# box-wake.t.sh: goal:g7.16.1.11.20 (DG1 16:14Z; design = doc:rse-aa1-boxes AA1 wake line + AA1.M, council placement 14:54Z): messaging is box mail in the AA1.M math. A v5 post is WOKEN by polling its box (`box n|wc -l` grows -> the pane is typed `mail: box read`), in the agi-run piece (claude / pi panes) AND in the cccc.ts piece (the pi extension); the unread count is right and falls to 0 after the read; the ~/o cap is KEPT; send.py is neither touched nor left dangling.
# THE BUG (council 10-07 15:02Z, alive): the pilot's cccc.ts poll is `let s=0;setInterval(()=>{...n=+x("box n|wc -l"...);n>s&&(s=n,p.sendUserMessage("mail: box read",...))},5e3)`: s moves only UP, so after a read drops the count the NEXT mail (n <= the old maximum) never wakes the pane. agi-run's line (`...;s=$n;done`) resets s every tick and is right. Lane w4 is the bug itself: send 2, read both, send 1 = exactly ONE more wake.
# sh + git + jq + ssh-keygen + node (v24, no TypeScript syntax in the piece: the driver loads a .mjs copy) on a SCRATCH repo, throwaway keys, no live ref, no network, 0 USD. It runs the REAL pieces extracted with `sect` from the .geometry/engine*.md of ROOT (the box-mail.t.sh recipe): `box` (the AA1 sender/reader), `agi-run` (under stubs: strace, stty, a harness that idles; a `sleep` shim that divides every sleep by DIV so the 5 s poll is 0.2 s) and `cccc.ts` (under a driver.mjs that gives it a fake pi API: p.on records the handlers, p.sendUserMessage logs the wake; setInterval is divided by DIV). Wakes are counted, never assumed: agi-run's typed text goes into a FIFO this file reads; cccc.ts's sendUserMessage goes to a log.
# AGIRUN=<file> CCCC=<file> BOX=<file> test other pieces than ROOT's (mutants / the pilot's); ROOT=<repo> where the pieces are read; DIV=<n> time scale (default 25). One ok/FAIL line per case; exit = FAIL count.
# Lanes: w1 one message wakes ONCE (and not again while it stays unread) · w2 a burst of 3 = ONE wake and the unread count is 3, then 0 after the read · w3 no mail = no wake · w4 THE BUG: send 2, read both, send 1 = exactly ONE more wake (w4b: send 1, read, send 1) · w5 a successor wakes on mail its predecessor never read (s=0 at start) · w6 an off-matrix send never wakes · w7 (agi-run) the typed line is followed by the Enter · w8 (agi-run) a PI harness (H=pi-x) wakes with the same counts as claude-x · c1-c3 the ~/o cap is KEPT (over the cap trimmed to HALF keeping the TAIL; under it untouched; the default is 64 MiB) · s1-s3 send.py: the two pieces carry no send.py and no sessions/inbox reference (no dangling caller), the typed line is `mail: box read`, and send.py itself still resolves (control). Each lane runs on agi-run (a*) and on cccc.ts (p*) where it applies.
# Honest limits: the poll interval and the 1 s typing pause are scaled, so the lanes pin the COMPARISON, not the wall-clock cadence; a wake is counted by the text typed / sent, not by a model turn. cccc.ts is run with node as an ES module (the real expression, not a transcription); the harness stub idles, it is not claude.
T=$(mktemp -d);trap 'for p in $(cat $T/pids 2>/dev/null);do kill -TERM -$p 2>/dev/null;kill $p 2>/dev/null;done;rm -rf $T' 0;f=0;G=/usr/bin/git;R0=${ROOT:-$(cd "$(dirname "$0")/../../.." && pwd)};DIV=${DIV:-25}
sect(){ cat $R0/.agi/nodes/.geometry/engine*.md|sed -n "/^###* $1 /,/^###* /{/^~~~/,/^~~~/{//!p}}";}
ok(){ if eval "$2";then echo "ok $1";else echo "FAIL $1";f=$((f+1));fi;}
wt(){ /bin/sleep $1;}
unset GIT_AUTHOR_NAME GIT_AUTHOR_EMAIL GIT_COMMITTER_NAME GIT_COMMITTER_EMAIL GIT_DIR GIT_WORK_TREE AGI_TRUNK AGI_SEAT AGI_POST AGI_PANE_MAX_MB
mkdir -p $T/bin $T/c $T/k $T/run $T/hm/.claude
[ -n "$BOX" ]||{ sect box>$T/bin/box;BOX=$T/bin/box;};[ "$BOX" = $T/bin/box ]||cp $BOX $T/bin/box
[ -n "$AGIRUN" ]||{ sect agi-run>$T/agi-run;AGIRUN=$T/agi-run;}
[ -n "$CCCC" ]||{ sect cccc.ts>$T/cccc.mjs;CCCC=$T/cccc.mjs;};case $CCCC in *.mjs);;*)cp $CCCC $T/cccc.mjs;CCCC=$T/cccc.mjs;;esac
[ -s $BOX ]&&[ -s $AGIRUN ]&&[ -s $CCCC ]||{ echo "FAIL extract: box $(wc -c<$BOX) agi-run $(wc -c<$AGIRUN) cccc.ts $(wc -c<$CCCC)";exit 99;}
chmod +x $T/bin/box
# keys + signers + per-post git config (the box-mail.t.sh fixture, two posts): belam <- council (inert) <- alive; sm is a stranger two levels away
: >$T/signers
for u in belam alive dg9;do
 ssh-keygen -q -t ed25519 -N '' -f $T/k/$u -C $u>/dev/null
 echo "$u@agi namespaces=\"git\" $(cut -d' ' -f1,2 $T/k/$u.pub)">>$T/signers
 printf '[user]\n\tname=%s\n\temail=%s@agi\n\tsigningkey=%s\n[gpg]\n\tformat=ssh\n[gpg "ssh"]\n\tallowedSignersFile=%s\n[commit]\n\tgpgsign=false\n' $u $u $T/k/$u $T/signers>$T/c/$u
done
$G init -q $T/r;mkdir -p $T/r/.agi/nodes/.geometry
cat >$T/r/.agi/nodes/.geometry/posts.md<<'EOF'
  - {"name":"belam","parent":"owner","harness":"claude"}
  - {"name":"council","parent":"belam","members":["alive"]}
  - {"name":"alive","parent":"council","harness":"claude"}
  - {"name":"dg9","parent":"alive","harness":"claude"}
EOF
$G -C $T/r add -A;$G -C $T/r -c user.name=x -c user.email=x@x commit -qm fixture
# a post's environment: its git identity + the matrix trunk; PATH = the scratch bin (box, the stubs)
as(){ u=$1;shift;(cd $T/r&&AGI_POST=$u AGI_TRUNK=HEAD GIT_CONFIG_GLOBAL=$T/c/$u GIT_CONFIG_SYSTEM=/dev/null PATH=$T/bin:$PATH "$@");}
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
globalThis.setInterval = (f, ms, ...a) => real(f, ms / div, ...a);
const mod = await import(pathToFileURL(process.argv[2]).href), h = {};
mod.default({ on: (e, f) => { h[e] = f; }, sendUserMessage: (t) => { console.log("WAKE " + t); } });
h.session_start({ reason: "new" });
EOF
# start NAME KIND [env...]: one wake-watcher for post alive. KIND = agirun | cccc. Wakes accumulate in $T/typed.NAME (agirun: the FIFO's text) / $T/wakes.NAME (cccc: one WAKE line each)
start(){ nm=$1;kd=$2;shift 2;: >$T/typed.$nm;: >$T/wakes.$nm
 case $kd in
 agirun)rm -f $T/run/i;mkfifo $T/run/i;exec 3<>$T/run/i;cat <&3 >>$T/typed.$nm &echo $! >>$T/pids
  (cd $T/hm&&env HOME=$T/hm H=claude-x RUNTIME_DIRECTORY=$T/run O=$T/r AGI_SEAT=alive AGI_POST=alive AGI_TRUNK=HEAD GIT_CONFIG_GLOBAL=$T/c/alive GIT_CONFIG_SYSTEM=/dev/null PATH=$T/bin:$PATH "$@" setsid sh $AGIRUN >$T/ar.out.$nm 2>&1 &echo $! >>$T/pids);;
 cccc)(cd $T/r&&env HOME=$T/hm DIV=$DIV AGI_SEAT=alive AGI_POST=alive AGI_TRUNK=HEAD GIT_CONFIG_GLOBAL=$T/c/alive GIT_CONFIG_SYSTEM=/dev/null PATH=$T/bin:$PATH "$@" node $T/drv.mjs $CCCC >$T/wakes.$nm 2>$T/node.err.$nm &echo $! >>$T/pids);;
 esac;}
stop(){ for p in $(cat $T/pids 2>/dev/null);do kill -TERM -$p 2>/dev/null;kill $p 2>/dev/null;done;: >$T/pids;exec 3<&-;/bin/sleep 0.3;}
wakes(){ case $1 in a*)grep -o 'mail: box read' $T/typed.$1|wc -l|tr -d ' ';;*)grep -c '^WAKE mail: box read' $T/wakes.$1|tr -d ' ';;esac;}
reset(){ stop;rm -rf $T/r/.git/refs/box $T/r/.git/refs/held;}
for kd in agirun cccc;do case $kd in agirun)N=a;;*)N=p;;esac
# ---- w3: no mail = no wake
reset;start ${N}3 $kd;wt 2;ok "w3-$kd-no-mail-no-wake no mail for 2 s of polling: $(wakes ${N}3) wake(s) (want 0); the watcher is up (typed/wake file exists)" '[ "$(wakes ${N}3)" = 0 ]'
# ---- w1: one message wakes ONCE, and not again while it stays unread
snd belam alive "hello one";wt 1.5;w1a=$(wakes ${N}3);wt 1.5;w1b=$(wakes ${N}3)
ok "w1-$kd-one-message-wakes-once belam -> alive (adjacent, level a()): ONE wake after the send ($w1a) and still one after 1.5 s more of polling ($w1b: an unread message never re-wakes); the unread count is $(unread alive) (want 1)" '[ "$w1a" = 1 ]&&[ "$w1b" = 1 ]&&[ "$(unread alive)" = 1 ]'
# ---- w2: a burst of 3 = ONE wake; count 3, then 0 after the read
reset;start ${N}2 $kd;snd belam alive m1;snd belam alive m2;snd belam alive m3;u3=$(unread alive);wt 2;w2=$(wakes ${N}2);rd alive;u0=$(unread alive)
ok "w2-$kd-unread-count-and-burst three sends: the unread count is $u3 (want 3), ONE wake for the burst ($w2), and after box read the count is $u0 (want 0)" '[ "$u3" = 3 ]&&[ "$w2" = 1 ]&&[ "$u0" = 0 ]'
# ---- w4: THE BUG. send 2, read both, send 1 = exactly ONE more wake for that 1
reset;start ${N}4 $kd;snd belam alive a1;snd belam alive a2;wt 1.5;w4a=$(wakes ${N}4);rd alive;wt 1.2;u4=$(unread alive);snd belam alive b1;wt 1.5;w4b=$(wakes ${N}4)
ok "w4-$kd-wake-after-read send 2 (wakes $w4a, want 1), read both (count $u4, want 0), send 1: the next mail wakes the pane, exactly ONE more wake (total $w4b, want 2); the pilot's n>s&&(s=n,...) never fires here because s stays at 2" '[ "$w4a" = 1 ]&&[ "$u4" = 0 ]&&[ "$w4b" = 2 ]'
# ---- w4b: the simplest shape of the same bug: send 1, read, send 1
reset;start ${N}5 $kd;snd belam alive c1;wt 1.5;rd alive;wt 1.2;snd belam alive c2;wt 1.5;w5=$(wakes ${N}5)
ok "w4b-$kd-same-count-again send 1 (wake), read it, send 1 again (the count is back to 1, equal to the old maximum): the second mail wakes too, total $w5 (want 2)" '[ "$w5" = 2 ]'
# ---- w5: a successor wakes on mail its predecessor never read (s=0 at start)
reset;snd belam alive pre1;snd belam alive pre2;start ${N}6 $kd;wt 1.5;w6=$(wakes ${N}6)
ok "w5-$kd-successor-wakes-on-unread two messages unread BEFORE the watcher starts: it wakes at once, once ($w6, want 1)" '[ "$w6" = 1 ]'
# ---- w6: an off-matrix send (dg9 -> belam: levels 3 and 1) is refused by level a() and never wakes
reset;start ${N}7 $kd;snd dg9 belam nope >/dev/null 2>&1;snd dg9 alive adj >/dev/null 2>&1;wt 1.5;w7=$(wakes ${N}7)
ok "w6-$kd-adjacent-wakes-off-matrix-does-not dg9 -> belam is off-matrix (nothing sent, no wake for belam's box); dg9 -> alive is adjacent: alive's watcher wakes once ($w7, want 1)" '[ "$w7" = 1 ]&&[ "$(unread belam)" = 0 ]'
[ $kd = agirun ]&&{ reset;start a11 agirun;snd belam alive e1;wt 1.5;w8=$(wakes a11);cr=$(tr -cd '\r' <$T/typed.a11|wc -c|tr -d ' ')
ok "w7-agirun-types-the-Enter after the typed line the poll presses Enter (a CR): $w8 wake(s), $cr CR(s) typed (want equal and 1); without it the pane holds the line unsent" '[ "$w8" = 1 ]&&[ "$cr" = 1 ]';}
[ $kd = agirun ]&&{ reset;start a12 agirun H=pi-x;snd belam alive q1;wt 1.5;pw1=$(wakes a12);wt 1.5;pw1b=$(wakes a12)
 reset;start a13 agirun H=pi-x;snd belam alive q1;snd belam alive q2;wt 1.5;rd alive;wt 1.2;snd belam alive q3;wt 1.5;pw4=$(wakes a13)
ok "w8-agirun-pi-harness-wakes-the-same (DG1 16:29Z) the poll types for a PI harness too (case \$H in claude*|pi*): with H=pi-x one message wakes ONCE ($pw1, still $pw1b later; want 1 1) and send 2, read, send 1 gives 2 wakes ($pw4, want 2): the SAME counts as claude-x on w1 and w4" '[ "$pw1" = 1 ]&&[ "$pw1b" = 1 ]&&[ "$pw4" = 2 ]';}
done
reset
# ---- the ~/o cap (agi-run only): the 5-minute loop trims ~/o to HALF the cap keeping the TAIL when it is over AGI_PANE_MAX_MB (default 64); DIV scales the 300 s
capsz(){ stat -c%s $T/hm/o 2>/dev/null||echo 0;}
mkbig(){ rm -f $T/hm/o;awk -v n=$1 'BEGIN{for(i=0;i<n;i++)printf "%07d line of the pane log, padding padding padding padding padding\n", i}' >$T/hm/o;}
printf '#!/bin/sh\ncase $1 in *[!0-9]*|"")exec /bin/sleep "$@";esac\nexec /bin/sleep $(awk "BEGIN{print $1/100}")\n'>$T/bin/sleep   # the cap loop sleeps 300 s: scale it harder
mkbig 50000;cp $T/hm/o $T/o.orig;sz0=$(capsz);start a8 agirun AGI_PANE_MAX_MB=1;wt 5;sz1=$(capsz);stop
tailn=$((1<<19));tail -c $tailn $T/o.orig >$T/o.tail
ok "c1-cap-trims-to-half-keeping-the-tail ~/o of $sz0 B with AGI_PANE_MAX_MB=1: after one loop it is $sz1 B (want $tailn = half the cap) and holds the LAST $tailn bytes of the original (cmp: $(cmp -s $T/hm/o $T/o.tail&&echo same||echo DIFFERENT))" '[ "$sz1" = $tailn ]&&cmp -s $T/hm/o $T/o.tail'
awk 'BEGIN{for(i=0;i<500;i++)printf "%07d small\n", i}' >$T/hm/o;cp $T/hm/o $T/o.small;start a9 agirun AGI_PANE_MAX_MB=1;wt 5;stop
ok "c2-under-the-cap-untouched a ~/o under the cap is byte-identical after the loop ($(cmp -s $T/hm/o $T/o.small&&echo same||echo CHANGED), $(capsz) B)" 'cmp -s $T/hm/o $T/o.small'
rm -f $T/hm/o;truncate -s 70M $T/hm/o;start a10 agirun;wt 6;sz2=$(capsz);stop;rm -f $T/hm/o
ok "c3-default-cap-is-64-MiB with AGI_PANE_MAX_MB unset a 70 MiB ~/o is trimmed to $sz2 B (want $((32<<20)) = half of 64 MiB)" '[ "$sz2" = $((32<<20)) ]'
# ---- send.py: no dangling caller in the two pieces; send.py itself resolves
sc=$(cat $AGIRUN $CCCC|grep -c 'send\.py\|sessions/inbox')
ok "s1-no-send-py-in-the-wake-pieces agi-run and cccc.ts carry no send.py and no sessions/inbox reference ($sc occurrence(s), want 0): the wake no longer depends on the inbox file nor types 'mail: send.py read'" '[ "$sc" = 0 ]'
ok "s2-typed-line-is-box-read the line the poll types is 'mail: box read' (agi-run: $(grep -c 'mail: box read' $AGIRUN) occurrence(s); cccc.ts: $(grep -c 'mail: box read' $CCCC)), the old 'mail: send.py read' appears $(cat $AGIRUN $CCCC|grep -c 'mail: send.py read') times" 'grep -q "mail: box read" $AGIRUN&&grep -q "mail: box read" $CCCC&&! cat $AGIRUN $CCCC|grep -q "mail: send.py read"'
SP=$R0/extensions/agi/bin/send.py;python3 $SP --help >/dev/null 2>&1;sprc=$?
ok "s3-send-py-still-resolves (control) extensions/agi/bin/send.py is there ($([ -f $SP ]&&echo yes||echo NO)) and answers --help (rc $sprc): this goal retires no send.py caller it has not replaced" '[ -f $SP ]&&[ $sprc = 0 ]'
echo "box-wake: $f FAIL"
exit $f
