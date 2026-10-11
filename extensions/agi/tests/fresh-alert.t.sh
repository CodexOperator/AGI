#!/bin/sh
# fresh-alert.t.sh: goal:g7.16.1.11.20 v5 placement (belam RULED 10-10 22:xxZ, SM 10-11 01:0xZ): a v5 post rotates by the meter hook (touch ~/.fresh; kill), so cut B's rotate.py site never runs on this box. The alert is sent by agi-run's .fresh branch (the line that runs when `c=` is empty): a BACKGROUNDED `timeout 20` fail-soft `box send <recv>` AS the post, receivers = config:rotations alerts (audit + edges[post] - silent - self) read from the trunk (AGI_TRUNK:-HEAD), NO liveness filter (the box matrix is the only adjacency check).
# sh + git + awk + timeout on a SCRATCH repo, a STUB box (records who sent what), stub strace/stty, no network, 0 USD. It runs the REAL agi-run piece from engine*.md. AGIRUN=<file> tests another copy (the mutants below are made from the real one with sed). ROOT=<repo> where the pieces are read.
# Lanes: a-the-restart-never-waits a HUNG box (sleeps 60) does not delay the exec of the successor (mutant: the send in the foreground goes RED) · b-unreadable-alerts-cell-warns-once garbled / missing alerts cell and a missing file: no box call, ONE warn line, the exec still happens (mutant: the parse failure ignored goes RED) · c-silent-and-self-excluded audit + edges[post] sent, silent and the post itself dropped, no duplicate (mutants: silent not dropped / self not dropped go RED) · d-continue-sends-nothing a `-c` start (no ~/.fresh) sends nothing · e-sender-and-body each send runs AS the post and carries the [rotation-alert] block.
T=$(mktemp -d);trap 'for p in $(cat $T/pids $T/boxpid 2>/dev/null);do kill -TERM -$p 2>/dev/null;kill -TERM $p 2>/dev/null;done;rm -rf $T' 0;f=0;R0=${ROOT:-$(cd "$(dirname "$0")/../../.." && pwd)}
sect(){ cat $R0/.agi/nodes/.geometry/engine*.md|sed -n "/^###* $1 /,/^###* /{/^~~~/,/^~~~/{//!p}}";}
ok(){ if eval "$2";then echo "ok $1";else echo "FAIL $1";f=$((f+1));fi;}
unset GIT_DIR GIT_WORK_TREE AGI_TRUNK AGI_SEAT AGI_POST
mkdir -p $T/bin $T/run $T/hm
[ -n "$AGIRUN" ]||{ sect agi-run>$T/agi-run;AGIRUN=$T/agi-run;}
[ -s $AGIRUN ]||{ echo "FAIL extract: agi-run $(wc -c<$AGIRUN)";exit 99;}
printf '[safe]\n\tdirectory=*\n[user]\n\tname=x\n\temail=x@x\n[commit]\n\tgpgsign=false\n'>$T/gitcfg
G="git -c safe.directory=*"
export GIT_CONFIG_GLOBAL=$T/gitcfg GIT_CONFIG_SYSTEM=/dev/null
git init -q $T/r;mkdir -p $T/r/.agi/nodes/.geometry;ln -s $T/r $T/hm/t
# stubs: strace records that the harness was exec'd and with which args; stty is inert; box records "<AGI_POST> <argv> :: <stdin>"; BOXHANG makes it hang
printf '#!/bin/sh\nshift 5\necho "$@">%s/exec\n' $T>$T/bin/strace
printf '#!/bin/sh\nexit 0\n'>$T/bin/stty
printf '#!/bin/sh\nb=$(cat)\necho "$AGI_POST $* :: $b">>%s/boxlog\necho $$ >>%s/boxpid\n[ -e %s/BOXHANG ]&&exec sleep 60\nexit 0\n' $T $T $T>$T/bin/box
chmod +x $T/bin/strace $T/bin/stty $T/bin/box
# rotations.md on the trunk: $1 = the body of the front matter (after the first ---)
rot(){ { echo '---';cat;echo '---';echo '# config:rotations'; }>$T/r/.agi/nodes/.geometry/rotations.md;$G -C $T/r add -A;$G -C $T/r commit -qm r --allow-empty;}
# go FRESH(1|0) [AGIRUN-file]: run agi-run as dg4 in a pane; wait up to 6 s for the exec marker; leaves the box log
go(){ rm -f $T/exec $T/boxlog $T/boxpid $T/run/alert $T/hm/.fresh;[ "$1" = 1 ]&&: >$T/hm/.fresh;a=${2:-$AGIRUN}
 (cd $T/hm&&exec setsid env HOME=$T/hm H=x RUNTIME_DIRECTORY=$T/run O=$T/r AGI_POST=dg4 AGI_TRUNK=HEAD PATH=$T/bin:$PATH sh $a 2>$T/err) &
 echo $! >>$T/pids;i=0;while [ ! -e $T/exec ]&&[ $i -lt 60 ];do sleep 0.1;i=$((i+1));done
 if [ "${WANT:-0}" -gt 0 ];then i=0;while [ "$(wc -l <$T/boxlog 2>/dev/null||echo 0)" -lt $WANT ]&&[ $i -lt 100 ];do sleep 0.1;i=$((i+1));done;else sleep 0.5;fi;}
box_to(){ sed -n 's/^[^ ]* send \([^ ]*\) ::.*/\1/p' $T/boxlog 2>/dev/null|sort|tr '\n' ' ';}
warns(){ grep -c '^warn: rotation alert' $T/run/alert 2>/dev/null;}
said(){ grep -c "\$1" $T/run/alert 2>/dev/null;}

# c: audit + edges[post], minus silent, minus self, no duplicates
rot <<'EOF'
alerts:
  audit:
    - sanctuary-master
    - dg4
    - stream-master
  edges:
    dg4:
      - dg2
      - sanctuary-master
    dg9:
      - nobody
  silent:
    - stream-master
    - thought-master
EOF
WANT=2 go 1
ok c-silent-and-self-excluded "[ \"\$(box_to)\" = 'dg2 sanctuary-master ' ]&&[ \$(warns) = 0 ]&&[ -e $T/exec ]"
# e: as the post, with the block
ok e-sender-and-body "[ \$(grep -c '^dg4 send ' $T/boxlog) = 2 ]&&[ \$(grep -c ':: \[rotation-alert\] dg4 restarted fresh 20[0-9-]*T[0-9:]*Z\$' $T/boxlog) = 2 ]&&! grep -q 'hook\|rotation)' $T/boxlog"
# d: a continue start sends nothing, and execs with -c
go 0
ok d-continue-sends-nothing "[ ! -s $T/boxlog ]&&[ \"\$(cat $T/exec)\" = 'x -c go' ]"
# a: a hung box does not delay the exec (the lane waits <= 6 s; foreground would take 20 s)
: >$T/BOXHANG
t0=$(date +%s);go 1;t1=$(date +%s)
ok a-the-restart-never-waits "[ -e $T/exec ]&&[ \$((t1-t0)) -le 4 ]&&[ \"\$(cat $T/exec)\" = 'x go' ]"
# a2: timeout -k 2 20 reaps the hung box child (the stub records its pid; it exec'd sleep 60): gone within 27 s
gone(){ b=$(tail -1 $T/boxpid);i=0;while kill -0 $b 2>/dev/null&&[ $i -lt 270 ];do sleep 0.1;i=$((i+1));done;! kill -0 $b 2>/dev/null;}
ok a2-a-hung-box-child-is-reaped-by-the-timeout "gone"
rm -f $T/BOXHANG
# b: garbled cell / no alerts key / unknown line inside alerts / file absent: nothing sent, ONE warn, exec happens
bad(){ go 1;[ ! -s $T/boxlog ]&&[ $(warns) = 1 ]&&[ -e $T/exec ]&&[ ! -s $T/err ];}   # the warn goes to the alert log, NEVER the pane's stderr
printf 'edited_by: belam\n'|rot;ok b-no-alerts-key-warns-once "bad"
printf 'alerts:\n  audit:\n    - sanctuary-master\n  edges: {}\n  surprise: 1\n'|rot;ok b-unknown-line-warns-once "bad"
printf 'alerts:\n  audit: [sanctuary-master]\n'|rot;ok b-flow-list-warns-once "bad"
rm -f $T/r/.agi/nodes/.geometry/rotations.md;$G -C $T/r add -A;$G -C $T/r commit -qm gone;ok b-file-absent-warns-once "bad"

# mutants of the REAL piece: each must go RED on its lane
rot <<'EOF'
alerts:
  audit:
    - sanctuary-master
    - dg4
    - stream-master
  edges: {}
  silent:
    - stream-master
EOF
mut(){ cp $AGIRUN $T/m.$1;sed -i "$2" $T/m.$1;cmp -s $AGIRUN $T/m.$1&&{ echo "FAIL mutant-$1-did-not-change-the-piece";f=$((f+1));return 1;};return 0;}
has(){ box_to|grep -qw -- "$1";}
# each mutant row asserts the mutant's ACTUAL wrong outcome, not merely "not the right list" (which a send-nothing mutant also satisfies)
# a: foreground send (drop the & that backgrounds the subshell)
mut fg 's/alert&$/alert/'&&{ : >$T/BOXHANG;t0=$(date +%s);go 1 $T/m.fg;t1=$(date +%s);rm -f $T/BOXHANG;ok mutant-a-foreground-send-is-RED "[ \$((t1-t0)) -gt 4 ]||[ ! -e $T/exec ]"; }
# a2: no timeout -> the hung box child outlives 27 s
mut notimeout 's/timeout -k 2 20 //'&&{ : >$T/BOXHANG;go 1 $T/m.notimeout;ok mutant-a2-no-timeout-is-RED "! gone";b=$(tail -1 $T/boxpid);kill $b 2>/dev/null;rm -f $T/BOXHANG; }
# c: self not dropped / silent not dropped
mut self 's/S\[p\];for/for/'&&{ WANT=2 go 1 $T/m.self;ok mutant-c-self-kept-is-RED "has dg4"; }
mut silent 's/z=split(L\["silent"\],y," ")/z=0/'&&{ WANT=2 go 1 $T/m.silent;ok mutant-c-silent-kept-is-RED "has stream-master"; }
# b: the parse failure ignored (no exit 1): the unknown-line cell is then SENT
printf 'alerts:\n  audit:\n    - sanctuary-master\n  edges: {}\n  surprise: 1\n'|rot
mut noexit 's/if(!s||b)exit 1;//'&&{ WANT=1 go 1 $T/m.noexit;ok mutant-b-failure-ignored-is-RED "has sanctuary-master"; }
# stderr: the alert's warn on the pane's stderr (the TUI's pty) instead of the alert log
mut pane 's/)2>>\$RUNTIME_DIRECTORY\/alert&$/)\&/'&&{ go 1 $T/m.pane;ok mutant-stderr-to-the-pane-is-RED "[ -s $T/err ]"; }
echo "fresh-alert: $f FAIL";[ $f = 0 ]
