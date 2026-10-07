#!/bin/sh
# act2.sh (ROOT, scratch only): does a PathChanged unit on a sender's own refs/box/<P> fire on EVERY send, and one on refs/box only on the first?
# Throwaway units in /run/systemd/system (gone at reboot), stub service, stores under /tmp/m2; no live store, no real carrier.
D=/tmp/m2;U=/run/systemd/system;A=alive;B=all-is-one
r(){ u=$1;shift;runuser -u agi-$u -- env HOME=/var/lib/agi/$u "$@";}
n(){ ls -l /proc/1/fd|grep -c anon_inode:inotify;}
f(){ [ -f $D/fired.$1 ]&&wc -l<$D/fired.$1||echo 0;}
snd(){ r $1 sh -c "cd $D/$1/g.git&&git update-ref refs/box/$1/$2 \$(echo \$\$|GIT_AUTHOR_NAME=x GIT_AUTHOR_EMAIL=$1@agi GIT_COMMITTER_NAME=x GIT_COMMITTER_EMAIL=$1@agi git commit-tree \$(git hash-object -w -t tree /dev/null))";sleep 1;}
install -d -m 755 $D;for u in $A $B;do install -d -o agi-$u -g agi-$u -m 755 $D/$u;r $u git init -q --bare $D/$u/g.git;done
r $A mkdir -p $D/$A/g.git/refs/box/$A;r $B mkdir -p $D/$B/g.git/refs/box
printf '[Path]\nPathChanged=/tmp/m2/%%i/g.git/refs/box/%%i\n'>$U/agi-act2@.path;printf '[Path]\nPathChanged=/tmp/m2/%%i/g.git/refs/box\n'>$U/agi-act2c@.path
for t in agi-act2 agi-act2c;do printf "[Service]\nType=oneshot\nExecStart=/bin/sh -c 'echo fired >>/tmp/m2/fired.%%i'\n">$U/$t@.service;done
systemctl daemon-reload;i0=$(n);systemctl start agi-act2@$A.path agi-act2c@$B.path agi-act2@ghost.path;i1=$(n)
echo "GHOST before its dir exists: $(systemctl show -p ActiveState,SubState,Result agi-act2@ghost.path|tr '\n' ' ')"
snd $A $B;snd $A $B;snd $A dg5;snd $B $A;snd $B $A;snd $B dg5;sleep 2
echo "ROW   $A (watch refs/box/$A, dir pre-created): sends=3 fired=$(f $A) [expect 3]"
echo "CTRL  $B (watch refs/box, sender dir NOT pre-created): sends=3 fired=$(f $B) [expect 1]"
x=$(f $A);r $A touch $D/$A/g.git/refs/heads/z;sleep 3;echo "NEG   no send + a write elsewhere, 3 s: fired $x -> $(f $A) [expect equal]"
r $A git -C $D/$A/g.git pack-refs --all;echo "PACK  pack-refs --all pruned the pre-created dir: $([ -d $D/$A/g.git/refs/box/$A ]&&echo no||echo YES)";snd $A $B;snd $A dg5;sleep 2
echo "PACK  2 more sends after the prune: fired=$(f $A) [expect 5; 3 = the watch died with the dir]"
r $A sh -c "mkdir -p $D/ghost/g.git/refs/box/ghost&&touch $D/ghost/g.git/refs/box/ghost/x";sleep 2
echo "GHOST after the dir + a file appear: fired=$(f ghost) $(systemctl show -p ActiveState,SubState agi-act2@ghost.path|tr '\n' ' ')"
echo "INOTIFY instances held by pid 1: before=$i0 after_start=$i1 now=$(n) limit(max_user_instances)=$(cat /proc/sys/fs/inotify/max_user_instances)"
