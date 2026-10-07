#!/bin/sh
# host-act-2-ghost.sh (ROOT, scratch only): the one line host act 2 could not measure (its mkdir ran as the row user under a root-owned /tmp/m2).
# A per-sender PathChanged unit starts while its dir does NOT exist; the dir is then created by ROOT and a file appears as the row user: does the waiting unit attach and fire?
# Throwaway unit in /run/systemd/system, stub service, /tmp/m3; no live store. Rolls itself back at the end.
D=/tmp/m3;U=/run/systemd/system;A=alive;s(){ systemctl show -p ActiveState,SubState,Result agi-act2g@ghost.path|tr '\n' ' ';}
install -d -m 755 $D;printf '[Path]\nPathChanged=/tmp/m3/%%i/refs/box/%%i\n'>$U/agi-act2g@.path
printf "[Service]\nType=oneshot\nExecStart=/bin/sh -c 'echo fired >>/tmp/m3/fired.%%i'\n">$U/agi-act2g@.service
systemctl daemon-reload;systemctl start agi-act2g@ghost.path;echo "GHOST before its dir exists: $(s)"
install -d -o agi-$A -g agi-$A -m 755 $D/ghost $D/ghost/refs $D/ghost/refs/box $D/ghost/refs/box/ghost
runuser -u agi-$A -- touch $D/ghost/refs/box/ghost/x;sleep 2
echo "GHOST after the dir (root) + a file (row user) appear: fired=$([ -f $D/fired.ghost ]&&wc -l<$D/fired.ghost||echo 0) [expect >=1]  $(s)"
runuser -u agi-$A -- touch $D/ghost/refs/box/ghost/y;sleep 2
echo "GHOST a 2nd write later: fired=$([ -f $D/fired.ghost ]&&wc -l<$D/fired.ghost||echo 0) [expect more than the line above]"
systemctl stop agi-act2g@ghost.path;rm -f $U/agi-act2g@.path $U/agi-act2g@.service;systemctl daemon-reload;systemctl reset-failed 'agi-act2g*' 2>/dev/null;rm -rf $D
echo "ROLLED BACK: units=$(systemctl list-units --all --no-legend 'agi-act2g*'|wc -l) /tmp/m3=$(ls -d $D 2>/dev/null|wc -l) [expect 0 0]"
