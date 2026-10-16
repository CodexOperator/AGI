#!/bin/sh
# captive-release.t.sh: goal:g7.16.1.11.20.3 (council 3/3, alive [decision] 05:35:44Z 10-16; SM spec 05:36Z): the agi-captive gate (engine-wrap.md) is never a lock. With a fill window open it still passes ONLY one agi-fill command (rc 2 otherwise), but it RELEASES the window -- ONE "[captive] <path> released: <reason>" line on stderr, the window renamed <path>.released-<UTC>, kept, rc 0 -- when (a) agi-fill is not on PATH or (b) the window's mtime is older than ${AGI_FILL_WINDOW:-900} s.
# sh + jq + awk on a STUB HOME and a STUB PATH with a PreToolUse JSON on stdin; no live ~/.fill, no git, no network, 0 USD. ROOT=<tree> (or $1) = the tree whose engine-wrap.md is read. The piece is EXTRACTED from engine-wrap.md, never retyped.
# Rows: fc1 window present, no agi-fill on PATH, `ls`: rc 0, ONE [captive] line, .released-* = 1, window gone (mutant: today's gate = rc 2, locked) · fc2 fresh window + a stub agi-fill on PATH, `ls`: rc 2, window kept (mutant: always pass) · fc3 window older than AGI_FILL_WINDOW + a stub agi-fill: rc 0 + the line + renamed (mutant: no lifetime read) · fc4 the line names the window file and the reason, grep -c = 1 per reason (mutant: a silent pass = 0) · e1..e5 the unchanged gate (one agi-fill passes, chained refused, no window passes silently), AGI_FILL_WINDOW overrides the 900, the release keeps the bytes and a second call is silent, the line is on stderr only.
# Honest limits: stat -c %Y and date are the GNU ones (the box is Linux); the claude / pi call path of the hook is not run, only the piece.
R0=${ROOT:-${1:-$(cd "$(dirname "$0")/../../.." && pwd)}};GEO=$R0/.agi/nodes/.geometry;T=$(mktemp -d);trap 'rm -rf $T' 0;f=0
sect(){ cat $GEO/engine*.md|sed -n "/^###* $1 /,/^###* /{/^~~~/,/^~~~/{//!p}}";}
ok(){ if eval "$2";then echo "ok $1";else echo "FAIL $1";f=$((f+1));fi;}
unset AGI_FILL AGI_FILL_WINDOW
sect agi-captive >$T/piece;[ -s $T/piece ]||{ echo "FAIL extract: agi-captive";exit 99;}
mkdir -p $T/bin $T/fillbin $T/hm
printf '#!/bin/sh\nexit 0\n'>$T/fillbin/agi-fill;chmod +x $T/fillbin/agi-fill
SYS=/usr/bin:/bin
# gate PIECE PATHPREFIX COMMAND [env words]: the piece on a stub HOME, a stub PATH, the PreToolUse JSON; stderr -> $T/err, stdout -> $T/out
gate(){ p=$1;pp=$2;c=$3;shift 3;printf '{"tool_input":{"command":"%s"}}' "$c"|env -i HOME=$T/hm PATH=$pp$SYS "$@" sh $p 2>$T/err >$T/out;}
win(){ rm -f $T/hm/.fill $T/hm/.fill.released-*;printf 'window\n'>$T/hm/.fill;[ -z "$1" ]||touch -d "$1 seconds ago" $T/hm/.fill;}
nrel(){ ls $T/hm/.fill.released-* 2>/dev/null|wc -l|tr -d ' ';}
ncap(){ grep -c '^\[captive\] ' $T/err;}
# the mutants: each a copy of the REAL piece with one thing changed
mut(){ sed "$2" $T/piece >$T/$1;cmp -s $T/piece $T/$1&&{ echo "FAIL mutant $1 changed nothing";exit 99;};}
mut m-old.sh '/^w=/c\
w=${AGI_FILL:-$HOME/.fill};[ -e "$w" ]||exit 0
/^\[ -z "\$r" \]/d'
mut m-pass.sh 's/;exit 2$/;exit 0/'
mut m-life.sh 's/-gt \${AGI_FILL_WINDOW:-900}/-gt 999999999/'
mut m-silent.sh 's/echo "\[captive\][^;]*;//'
PIECE=$T/piece
ok "w0-witness-no-agi-fill-on-the-stub-path the stub PATH (no fillbin) resolves agi-fill: [$(env -i PATH=$SYS sh -c 'command -v agi-fill')] (want none), the fillbin PATH does: [$(env -i PATH=$T/fillbin:$SYS sh -c 'command -v agi-fill'|sed "s|$T/||")]" '[ -z "$(env -i PATH=$SYS sh -c "command -v agi-fill")" ]&&[ -n "$(env -i PATH=$T/fillbin:$SYS sh -c "command -v agi-fill")" ]'
# fc1: no agi-fill on PATH
win;gate $PIECE "" ls;rc=$?;n=$(ncap);r=$(nrel)
ok "fc1-no-agi-fill-on-PATH-releases-the-window window present, no agi-fill, command ls: rc $rc (want 0), [captive] lines $n (want 1), .released-* $r (want 1), window left: $([ -e $T/hm/.fill ]&&echo yes||echo no) (want no)" '[ $rc = 0 ]&&[ $n = 1 ]&&[ $r = 1 ]&&[ ! -e $T/hm/.fill ]'
win;gate $T/m-old.sh "" ls;rc=$?
ok "fc1-mutant-today's-gate-locks the SAME with today's gate: rc $rc (want 2, locked), [captive] lines $(ncap) (want 0), .released-* $(nrel) (want 0): so fc1 can fail" '[ $rc = 2 ]&&[ $(ncap) = 0 ]&&[ $(nrel) = 0 ]'
# fc2: fresh window + agi-fill present -> the gate bites
win;gate $PIECE $T/fillbin: ls;rc=$?
ok "fc2-a-live-window-and-agi-fill-still-bite fresh window + agi-fill on PATH, command ls: rc $rc (want 2), [captive] lines $(ncap) (want 0), window kept: $([ -e $T/hm/.fill ]&&echo yes||echo no) (want yes)" '[ $rc = 2 ]&&[ $(ncap) = 0 ]&&[ -e $T/hm/.fill ]'
win;gate $T/m-pass.sh $T/fillbin: ls;rc=$?
ok "fc2-mutant-always-pass the SAME with the gate always passing: rc $rc (want 0): fc2 would be RED" '[ $rc = 0 ]'
# fc3: an expired window with agi-fill present
win 1000;gate $PIECE $T/fillbin: ls;rc=$?;n=$(ncap);r=$(nrel)
ok "fc3-an-expired-window-is-released window 1000 s old (> 900), agi-fill on PATH, command ls: rc $rc (want 0), [captive] lines $n (want 1), .released-* $r (want 1)" '[ $rc = 0 ]&&[ $n = 1 ]&&[ $r = 1 ]'
win 1000;gate $T/m-life.sh $T/fillbin: ls;rc=$?
ok "fc3-mutant-no-lifetime-read the SAME with no lifetime read: rc $rc (want 2, locked), .released-* $(nrel) (want 0): so fc3 can fail" '[ $rc = 2 ]&&[ $(nrel) = 0 ]'
# fc4 (NEGATIVE): the line names the window file and the reason, once
win;gate $PIECE "" ls;a=$(grep -c "^\[captive\] $T/hm/.fill released: agi-fill not on PATH (engine defect)\$" $T/err)
win 1000;gate $PIECE $T/fillbin: ls;b=$(grep -c "^\[captive\] $T/hm/.fill released: window expired\$" $T/err)
ok "fc4-the-line-names-the-window-and-the-reason the stderr line for the PATH release matches path + 'agi-fill not on PATH (engine defect)': $a (want 1); for the expiry: path + 'window expired': $b (want 1)" '[ $a = 1 ]&&[ $b = 1 ]'
win;gate $T/m-silent.sh "" ls;rc=$?;a=$(grep -c "^\[captive\] " $T/err)
ok "fc4-mutant-a-silent-pass the SAME with a silent pass: rc $rc (want 0), [captive] lines $a (want 0): so fc4 can fail" '[ $rc = 0 ]&&[ $a = 0 ]'
# e1..e5: the gate otherwise unchanged
win;gate $PIECE $T/fillbin: 'agi-fill open';a=$?;gate $PIECE $T/fillbin: 'agi-fill open; rm -rf x';b=$?
ok "e1-one-agi-fill-passes-a-chained-command-does-not live window + agi-fill: 'agi-fill open' rc $a (want 0), chained rc $b (want 2), window kept: $([ -e $T/hm/.fill ]&&echo yes||echo no) (want yes)" '[ $a = 0 ]&&[ $b = 2 ]&&[ -e $T/hm/.fill ]'
win;rm -f $T/hm/.fill;gate $PIECE "" ls;rc=$?
ok "e2-no-window-passes-silently no window, command ls: rc $rc (want 0), stderr bytes $(wc -c <$T/err|tr -d ' ') (want 0), .released-* $(nrel) (want 0)" '[ $rc = 0 ]&&[ ! -s $T/err ]&&[ $(nrel) = 0 ]'
win 30;gate $PIECE $T/fillbin: ls;a=$?;win 30;gate $PIECE $T/fillbin: ls AGI_FILL_WINDOW=10;b=$?;r=$(nrel)
ok "e3-AGI_FILL_WINDOW-overrides-the-900 a 30 s old window: default rc $a (want 2), with AGI_FILL_WINDOW=10 rc $b (want 0), .released-* $r (want 1)" '[ $a = 2 ]&&[ $b = 0 ]&&[ $r = 1 ]'
win;printf 'keep me\n'>$T/hm/.fill;gate $PIECE "" ls;k=$(cat $T/hm/.fill.released-* 2>/dev/null);gate $PIECE "" ls;rc=$?
ok "e4-the-release-keeps-the-bytes-and-the-second-call-is-silent renamed window holds [$k] (want 'keep me'); the next call: rc $rc (want 0), stderr bytes $(wc -c <$T/err|tr -d ' ') (want 0)" '[ "$k" = "keep me" ]&&[ $rc = 0 ]&&[ ! -s $T/err ]'
win;gate $PIECE "" ls
ok "e5-the-line-is-on-stderr-only stdout bytes $(wc -c <$T/out|tr -d ' ') (want 0), [captive] on stderr $(ncap) (want 1)" '[ ! -s $T/out ]&&[ $(ncap) = 1 ]'
echo "captive-release: $f FAIL";[ $f = 0 ]
