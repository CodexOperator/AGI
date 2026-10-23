#!/bin/sh
# session-pin.t.sh: V0 of doc:brainstorm-unify §22 (belam 10-23) -- a claude post restarts into ITS OWN session: a fresh start runs `--session-id <uuid>` and writes ~/.session; every other start runs `--resume <id from ~/.session>`, never `-c` (which takes the NEWEST transcript: at the 03:45Z 10-23 reboot a fork in the same home came up as the Prime).
# sh + git + jq on a SCRATCH home whose ~/t is a SYMLINK (the project dir is named from the physical path), stub strace/stty/box, no claude, no network, 0 USD. It runs the REAL agi-run piece (sect agi-run of ROOT's .geometry/engine*.md); AGIRUN=<file> tests another copy.
# Cases: a fresh -> --session-id <uuid>, ~/.session = it, mode 600 · b own transcript + a NEWER foreign one -> --resume own (the done-when) · c no ~/.session -> the newest, pinned · d ~/.session names a missing transcript -> the newest ·
#   e a non-hex ~/.session (../x) -> ignored · f no transcript, no ~/.session -> -c (as before) · g a non-claude H -> -c, no ~/.session · h fresh then a fork's newer transcript -> --resume the minted id · m mutant: the line removed -> b is RED.
# Each run is its own session (setsid) and its group is killed after the run and at exit: agi-run backgrounds two endless loops.
# One ok/FAIL line per case; exit = FAIL count.
T=$(mktemp -d);trap 'for p in $(cat $T/pids 2>/dev/null);do kill -TERM -$p 2>/dev/null;done;rm -rf $T' 0;f=0;R0=${ROOT:-$(cd "$(dirname "$0")/../../.." && pwd)}
sect(){ cat $R0/.agi/nodes/.geometry/engine*.md|sed -n "/^###* $1 /,/^###* /{/^~~~/,/^~~~/{//!p}}";}
ok(){ if eval "$2";then echo "ok $1";else echo "FAIL $1";f=$((f+1));fi;}
unset GIT_DIR GIT_WORK_TREE AGI_TRUNK AGI_POST
[ -n "$AGIRUN" ]||{ sect agi-run>$T/agi-run;AGIRUN=$T/agi-run;}
[ -s $AGIRUN ]||{ echo "FAIL extract: agi-run $(wc -c<$AGIRUN)";exit 99;}
mkdir -p $T/bin $T/run $T/hm $T/r
printf '#!/bin/sh\nshift 5\necho "$@">%s/exec\n' $T>$T/bin/strace
printf '#!/bin/sh\nexit 0\n'>$T/bin/stty
printf '#!/bin/sh\ncat>/dev/null\nexit 0\n'>$T/bin/box
chmod +x $T/bin/*
git init -q $T/r;ln -s $T/r $T/hm/t
D=$T/hm/.claude/projects/$(cd $T/r&&pwd -P|sed 's/[^A-Za-z0-9]/-/g');mkdir -p $D
A=11111111-1111-4111-8111-111111111111;B=22222222-2222-4222-8222-222222222222
tx(){ echo '{}'>$D/$1.jsonl;touch -d "$2" $D/$1.jsonl;}
# go FRESH(1|0) [H]: run agi-run as a post would; leaves $T/exec = "<H> <args> go"
go(){ rm -f $T/exec $T/hm/.fresh;[ "$1" = 1 ]&&: >$T/hm/.fresh
 (cd $T/hm&&exec setsid env -i PATH=$T/bin:/usr/bin:/bin HOME=$T/hm H=${2:-claude-x} RUNTIME_DIRECTORY=$T/run O=$T/r AGI_POST=p1 AGI_TRUNK=HEAD sh $A_RUN </dev/null >/dev/null 2>$T/err) &
 g=$!;echo $g>>$T/pids;i=0;while [ ! -e $T/exec ]&&[ $i -lt 60 ];do sleep 0.1;i=$((i+1));done;sleep 0.2;kill -TERM -$g 2>/dev/null;}   # agi-run leaves its trim + inbox loops behind: end the run's whole group
A_RUN=$AGIRUN
ex(){ cat $T/exec 2>/dev/null;}
go 1;S=$(cat $T/hm/.session 2>/dev/null)
ok "a-fresh-mints-and-pins exec [$(ex)] (want claude-x --session-id <uuid> go), ~/.session [$S] mode $(stat -c %a $T/hm/.session 2>/dev/null) (want the same uuid, 600)" '[ "$(ex)" = "claude-x --session-id $S go" ]&&echo $S|grep -qE "^[0-9a-f]{8}-[0-9a-f-]{27}$"&&[ "$(stat -c %a $T/hm/.session)" = 600 ]'
rm -f $D/*;tx $A '2026-10-23 01:00';tx $B '2026-10-23 02:00';echo $A>$T/hm/.session;go 0
ok "b-own-session-beats-a-newer-fork own $A, a newer foreign $B -> exec [$(ex)] (want --resume $A)" '[ "$(ex)" = "claude-x --resume $A go" ]&&[ "$(cat $T/hm/.session)" = $A ]'
rm -f $T/hm/.session;go 0
ok "c-no-pin-takes-the-newest-and-pins-it exec [$(ex)] (want --resume $B, the old -c choice), ~/.session [$(cat $T/hm/.session 2>/dev/null)]" '[ "$(ex)" = "claude-x --resume $B go" ]&&[ "$(cat $T/hm/.session)" = $B ]'
echo 33333333-3333-4333-8333-333333333333>$T/hm/.session;go 0
ok "d-pin-without-a-transcript-falls-to-the-newest exec [$(ex)] (want --resume $B)" '[ "$(ex)" = "claude-x --resume $B go" ]'
echo ../x>$T/hm/.session;go 0
ok "e-non-hex-pin-ignored a ~/.session of ../x -> exec [$(ex)] (want --resume $B)" '[ "$(ex)" = "claude-x --resume $B go" ]'
rm -f $D/* $T/hm/.session;go 0
ok "f-nothing-at-all-keeps-c exec [$(ex)] (want claude-x -c go), no ~/.session" '[ "$(ex)" = "claude-x -c go" ]&&[ ! -e $T/hm/.session ]'
tx $A '2026-10-23 01:00';go 0 x
ok "g-non-claude-untouched H=x -> exec [$(ex)] (want x -c go), no ~/.session" '[ "$(ex)" = "x -c go" ]&&[ ! -e $T/hm/.session ]'
rm -f $D/*;go 1;S=$(cat $T/hm/.session);tx $S '2026-10-23 01:00';tx $B '2026-10-23 03:00';go 0
ok "h-fresh-then-a-fork minted $S, then a fork's newer $B -> exec [$(ex)] (want --resume $S)" '[ "$(ex)" = "claude-x --resume $S go" ]'
grep -v 'session-id' $AGIRUN>$T/m;A_RUN=$T/m;rm -f $D/*;tx $A '2026-10-23 01:00';tx $B '2026-10-23 02:00';echo $A>$T/hm/.session;go 0
ok "m-mutant-without-the-line-is-RED the piece minus the pin line -> exec [$(ex)] (want NOT --resume $A)" '[ "$(ex)" != "claude-x --resume $A go" ]'
echo "session-pin: $f FAIL";exit $f
