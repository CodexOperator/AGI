#!/bin/sh
# aa1m-probe5.sh (ROOT, scratch only): does systemd run a PathChanged oneshot AGAIN for events that land WHILE it runs? 3 sends 1 s apart into a 4 s service.
# Throwaway units in /run/systemd/system (gone at reboot), a stub service, a store under a fresh mktemp -d; no live store, no real carrier.
A=alive;U=/run/systemd/system;D=$(mktemp -d /tmp/m5.XXXXXX)||exit 1;chmod 755 $D
r(){ u=$1;shift;runuser -u agi-$u -- env HOME=/var/lib/agi/$u "$@";}
f(){ n=$(grep -c start $D/log 2>/dev/null);echo ${n:-0};}
snd(){ r $A sh -c "cd $D/$A/g.git&&git update-ref refs/box/$A/$1 \$(echo \$\$|GIT_AUTHOR_NAME=x GIT_AUTHOR_EMAIL=$A@agi GIT_COMMITTER_NAME=x GIT_COMMITTER_EMAIL=$A@agi git commit-tree \$(git hash-object -w -t tree /dev/null))";}
install -d -o agi-$A -g agi-$A -m 755 $D/$A;r $A git init -q --bare $D/$A/g.git;r $A mkdir -p $D/$A/g.git/refs/box/$A
printf '[Path]\nPathChanged=%s/%s/g.git/refs/box/%s\n' $D $A $A>$U/agi-act5.path
printf "[Service]\nType=oneshot\nExecStart=/bin/sh -c 'echo start >>$D/log;sleep 4;echo end >>$D/log'\n">$U/agi-act5.service
systemctl daemon-reload;systemctl start agi-act5.path
snd a;sleep 1;snd b;sleep 1;snd c;sleep 12;n=$(f)
echo "COALESCE 3 sends over 2 s into a 4 s oneshot: starts=$n [2 = one re-run after the first; 1 = events during a run are LOST (then the carrier re-scan + exit 75 + Restart=on-failure is the only cover); 0 = the path unit never fired: INCONCLUSIVE]"
echo "ROLLBACK: systemctl stop agi-act5.path;rm -f $U/agi-act5.path $U/agi-act5.service;systemctl daemon-reload;rm -rf $D"
