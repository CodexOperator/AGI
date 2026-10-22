#!/bin/sh
# f1-nspawn.t.sh: goal:g7.16.1.11.44.8 F1 (council 3/3 10-22 19:38:34Z + 19:45:00Z). The harness extensions/agi/guard/f1-nspawn.sh on STUBS ONLY: no root, no nspawn, no systemd, no network, 0 USD.
# What it proves is every piece that needs no root: M1 (refuse the host: 3 mutants, the stub systemctl log EMPTY), M3/M4 readers, M5 (captive, fail closed), M6 (memory, slice, host before/after), M7 (the verdict: PASS / FAIL / INCONCLUSIVE, two lines),
# the rm guard, the mutant anchors in the REAL agi.sh, and the whole host leg against a stub nspawn. The nspawn run itself is belam's host act; the first real run is the first real execution (stated in the merge-up).
# One ok/FAIL line per case; exit = number of FAILs. A MUTANT row passes only when the clean property BREAKS.
T=$(mktemp -d);trap 'rm -rf $T' 0;f=0;R0=${ROOT_TREE:-$(cd "$(dirname "$0")/../../.." && pwd)};SRC=$R0/extensions/agi/guard/f1-nspawn.sh;AGS=$R0/extensions/agi/bin/agi.sh
ok(){ if eval "$3";then echo "ok $1 $2";else echo "FAIL $1 $2";f=$((f+1));for x in $T/o $T/e;do [ -s $x ]&&head -5 $x|cut -c1-240|sed "s/^/#   ${x##*/}: /";done;fi;}
[ -f $SRC ]||{ echo "FAIL inputs: $SRC";exit 99;}
unset GIT_DIR GIT_WORK_TREE GIT_INDEX_FILE;export GIT_CONFIG_GLOBAL=/dev/null GIT_CONFIG_SYSTEM=/dev/null GIT_AUTHOR_NAME=t GIT_AUTHOR_EMAIL=t@t GIT_COMMITTER_NAME=t GIT_COMMITTER_EMAIL=t@t
# ---- shims: every tool the harness calls, logging to $T/log (a refused leg must leave it EMPTY)
SH=$T/shim;mkdir -p $SH;: >$T/log
mk(){ printf '#!/bin/sh\n%s\n' "$2" >$SH/$1;chmod +x $SH/$1;}
mk systemd-detect-virt 'echo "${STUB_VIRT:-none}";[ "${STUB_VIRT:-none}" != none ]'
mk systemctl 'echo "systemctl $*" >>$T_LOG
case "$1" in show) case "$*" in *Slice*) echo "${STUB_SLICE:-machine.slice}";; *MemoryPeak*) echo 123456;; *ControlGroup*) echo /machine.slice/x.scope;; *MemoryCurrent*) echo "MemoryCurrent=1";; esac;; list-units) [ -f $T_ACTIVE ]&&cat $T_ACTIVE;; esac;exit 0'
mk machinectl 'echo "machinectl $*" >>$T_LOG
case "$1" in show) [ "${STUB_NOUNIT:-}" = 1 ]||echo x.scope;; terminate) : >$T_TERM;; esac;exit 0'
mk crontab 'echo "crontab $*" >>$T_LOG;u=$3;cat $T_CRON.$u 2>/dev/null;exit 0'
mk getent 'echo "getent $*" >>$T_LOG;cat $T_PASSWD'
mk id 'case "$1" in -u) echo ${STUB_IDU:-0};; *) exec /usr/bin/id "$@";; esac'
mk mmdebstrap 'echo "mmdebstrap $*" >>$T_LOG;o=$(echo "$@"|awk "{print \$(NF-1)}");d=$(mktemp -d);mkdir -p $d/etc $d/bin;echo img >$d/etc/os-release
case "$*" in *--format=tar*) tar -C $d -cf $o .;; *) case $o in *.tar) tar -C $d -cf $o .;; *) mkdir -p $o;cp -r $d/. $o/;; esac;; esac;rm -rf $d;[ -z "$STUB_MMFAIL" ]||exit 1;exit 0'
mk systemd-nspawn 'echo "nspawn $*" >>$T_LOG
for a;do case $a in --directory=*) D=${a#--directory=};; esac;done
echo "$(ls -a $D|tr "\n" " ")|$(ls $D/f1|tr "\n" " ")|$(cat $D/.f1-marker)|$(cat $D$T_MAIN/.git/f1-marker 2>/dev/null)|unit:$(ls $D/etc/systemd/system/multi-user.target.wants|tr "\n" " ")|claude:$(find $D -name claude 2>/dev/null|wc -l)|hostname:$(cat $D/etc/hostname 2>/dev/null)|hosts:$(grep -c "^127.0.1.1 $(cat $D/etc/hostname 2>/dev/null)$" $D/etc/hosts 2>/dev/null)" >$T_SEEN
i=0;while [ ! -e $D/f1/go ]&&[ ! -e $T_TERM ]&&[ $i -lt 100 ];do i=$((i+1));sleep 0.1;done
if [ -e $D/f1/go ];then echo go >>$T_SEEN;[ -z "$STUB_TRIP" ]||{ printf "MemAvailable: 500000 kB\n" >$F1_MEMINFO;while [ ! -e $T_TERM ];do sleep 0.2;done;exit 0;};if [ -n "$STUB_RES" ];then mkdir -p $D/f1/out;cp $STUB_RES $D/f1/out/res;fi;[ "$STUB_HANG" != 1 ]||{ while [ ! -e $T_TERM ];do sleep 0.2;done;};fi;exit 0'
mk git '[ "$1" = hash-object ]&&{ echo blob;exit 0;};exec /usr/bin/git "$@"'
PATH=$SH:$PATH;export PATH
export T_LOG=$T/log T_TERM=$T/term T_SEEN=$T/seen T_ACTIVE=$T/active T_CRON=$T/cron T_PASSWD=$T/passwd T_MAIN=/data/work/agi
printf 'root:x:0:0::/root:/bin/sh\nagi-a:x:981:981::/var/lib/agi/a:/bin/sh\nagi-b:x:982:982::/var/lib/agi/b:/bin/sh\n' >$T/passwd
L(){ ( F1_LIB=1;. $SRC;"$@" );}   # run one lib function
# ================= M1: refuse the host, three legs, one mutant each; the stub systemctl log stays EMPTY and /f1/out is never made
rootfs(){ r=$T/$1;rm -rf $r;mkdir -p $r/data/work/agi/.git $r/f1;printf 'f1-x\n' >$r/.f1-marker;printf 'f1-x\n' >$r/data/work/agi/.git/f1-marker;printf 'SHA=0\nBOX=b\nRUN=x\n' >$r/f1/env;}
rootfs m1;( STUB_VIRT=systemd-nspawn F1_ROOT=$T/m1 L refuse_host ) >$T/o 2>$T/e;rc=$?
ok m1-clean-all-three-legs-pass "rc $rc" '[ $rc = 0 ]'
for how in virt marker mainmarker;do rootfs m1$how;v=systemd-nspawn
 case $how in virt)v=none;; marker)rm -f $T/m1$how/.f1-marker;; mainmarker)rm -f $T/m1$how/data/work/agi/.git/f1-marker;; esac
 : >$T/log;STUB_VIRT=$v F1_ROOT=$T/m1$how sh $SRC inner >$T/o 2>$T/e;rc=$?
 ok "m1-mutant-$how-refuses-with-nothing-touched-RED" "rc $rc: $(head -1 $T/e|cut -c1-100); log lines: $(wc -l <$T/log|tr -d ' ') (clean 0 too: refused before any act); /f1/out made: $([ -e $T/m1$how/f1/out ]&&echo YES||echo no)" '[ $rc != 0 ]&&[ ! -s $T/log ]&&[ ! -e $T/m1'$how'/f1/out ]&&grep -q "\[M1\]" $T/e';done
rootfs m1w;echo f1-other >$T/m1w/data/work/agi/.git/f1-marker;STUB_VIRT=systemd-nspawn F1_ROOT=$T/m1w L refuse_host >$T/o 2>$T/e;rc=$?
ok m1-mutant-main-marker-of-another-run-refuses-RED "rc $rc" '[ $rc != 0 ]'
# ================= M6: the live town
printf 'MemAvailable:    4400000 kB\n' >$T/mi.ok;printf 'MemAvailable:    3000000 kB\n' >$T/mi.low;printf 'MemAvailable:    3670016 kB\n' >$T/mi.edge;printf 'MemAvailable:    3670015 kB\n' >$T/mi.edge1;printf 'some avg10=0.00 avg60=0.00 avg300=0.00 total=1\n' >$T/psi.ok;printf 'some avg10=35.00 avg60=0.00 avg300=0.00 total=1\n' >$T/psi.hot;export F1_PSIMEM=$T/psi.ok
F1_MEMINFO=$T/mi.ok L mem_ok >$T/o 2>$T/e;rc=$?;ok m6-memory-4.4G-is-enough "rc $rc" '[ $rc = 0 ]'
F1_MEMINFO=$T/mi.low L mem_ok >$T/o 2>$T/e;rc=$?;ok m6-mutant-memory-3G-refuses-RED "rc $rc: $(head -1 $T/e|cut -c1-90)" '[ $rc != 0 ]&&grep -q "\[M6\]" $T/e'
F1_MEMINFO=$T/mi.edge L mem_ok >$T/o 2>$T/e;rc=$?;ok m6-the-floor-is-exactly-memorymax-plus-1G-3670016-kB-passes "rc $rc" '[ $rc = 0 ]'
F1_MEMINFO=$T/mi.edge1 L mem_ok >$T/o 2>$T/e;rc=$?;ok m6-mutant-one-kB-under-the-floor-refuses-RED "rc $rc" '[ $rc != 0 ]'
STUB_SLICE=machine.slice L slice_ok x >$T/o 2>$T/e;rc=$?;ok m6-slice-machine-slice-passes "$(cat $T/o)" '[ $rc = 0 ]&&grep -q "machine.slice" $T/o'
STUB_SLICE=agi.slice L slice_ok x >$T/o 2>$T/e;rc=$?;ok m6-mutant-slice-agi-slice-refuses-RED "$(cat $T/o)" '[ $rc != 0 ]'
STUB_NOUNIT=1 L slice_ok x >$T/o 2>$T/e;rc=$?;ok m6-mutant-no-registered-unit-refuses-RED "$(cat $T/o)" '[ $rc != 0 ]'
# ---- the host before/after (council 20:25:36Z): HARD only when the container or the harness could have caused it. A real repo with SIGNED refs/box commits (ssh keys), a stub systemctl / crontab / getent.
HW=$T/hw;/usr/bin/git init -q $HW;ssh-keygen -q -t ed25519 -N '' -C k1 -f $T/k1;ssh-keygen -q -t ed25519 -N '' -C k2 -f $T/k2
printf 'p@agi %s\nf1@agi %s\n' "$(cut -d' ' -f1,2 $T/k1.pub)" "$(cut -d' ' -f1,2 $T/k1.pub)" >$T/signers
mkdir -p $HW/.agi/nodes/.geometry;echo cron1 >$HW/.agi/nodes/.geometry/crons.md;/usr/bin/git -C $HW add -A;/usr/bin/git -C $HW commit -qm trunk;/usr/bin/git -C $HW branch -M core/season3/main
hsc(){ GIT_COMMITTER_EMAIL=$4 GIT_AUTHOR_EMAIL=$4 /usr/bin/git -C $HW -c gpg.format=ssh -c user.signingkey=$3 commit-tree -S ${2:+-p $2} -m "$1" $(/usr/bin/git -C $HW hash-object -w -t tree /dev/null);}
c1=$(hsc "mail one" "" $T/k1 p@agi);/usr/bin/git -C $HW update-ref refs/box/a/b $c1
echo "agi-post@a.service loaded active running x" >$T/active;echo "A" >$T/cron.agi-a;rm -f $T/cron.agi-b
hr(){ ( F1_REPO=$HW F1_SIGNERS=${SIG:-$T/signers} RUN=${RUN:-zz9} L hostread $1 );}
hd(){ ( F1_REPO=$HW F1_SIGNERS=${SIG:-$T/signers} RUN=${RUN:-zz9} L hostdelta $T/hb $T/ha );}
hr $T/hb;hr $T/hb2;ok m6-host-read-twice-is-identical "$(head -3 $T/hb|tr '\n' '|')" 'cmp -s $T/hb $T/hb2&&grep -q "^unit agi-post@a.service active running" $T/hb&&grep -q "^cron agi-a " $T/hb&&grep -q "^box refs/box/a/b " $T/hb&&grep -q "^cronsmd [0-9a-f]\{40\}" $T/hb'
hr $T/ha;hd >$T/o;ok m6-no-change-no-hard-no-inconclusive-lines "$(cat $T/o|tr '\n' '|')" '! grep -q "^hard\|^inconclusive" $T/o'
echo "agi-post@a.service loaded active running x
agi-post@b.service loaded active running x" >$T/active;hr $T/ha;hd >$T/o;ok m6-a-post-that-came-up-is-info-not-hard "$(cat $T/o|tr '\n' '|')" '! grep -q "^hard" $T/o&&grep -q "^info unit agi-post@b.service new" $T/o'
echo "agi-post@a.service loaded active running x" >$T/active;hr $T/hb
echo "agi-post@a.service loaded activating auto-restart x" >$T/active;hr $T/ha;hd >$T/o;ok m6-a-post-in-auto-restart-still-counts-as-up "$(cat $T/o|tr '\n' '|')" '! grep -q "^hard" $T/o'
echo "agi-post@a.service loaded failed failed x" >$T/active;hr $T/ha;hd >$T/o;ok m6-mutant-a-post-up-before-and-failed-after-is-HARD-RED "$(cat $T/o|tr '\n' '|')" 'grep -q "^hard unit agi-post@a.service was active, now failed" $T/o'
: >$T/active;hr $T/ha;hd >$T/o;ok m6-mutant-a-post-up-before-and-gone-after-is-HARD-RED "$(cat $T/o|tr '\n' '|')" 'grep -q "^hard unit agi-post@a.service was active, now gone" $T/o'
echo "agi-post@a.service loaded active running x" >$T/active
echo "B" >$T/cron.agi-a;hr $T/ha;hd >$T/o;ok m6-mutant-a-crontab-changed-with-crons-md-unchanged-is-HARD-RED "$(cat $T/o|head -3|tr '\n' '|')" 'grep -q "^hard cron agi-a changed" $T/o&&grep -q "^raw cron agi-a: " $T/o'
echo cron2 >$HW/.agi/nodes/.geometry/crons.md;/usr/bin/git -C $HW commit -qam crons;hd >$T/o0;hr $T/ha;hd >$T/o;ok m6-a-crontab-change-with-crons-md-changed-is-info-grid-sync "$(cat $T/o|head -3|tr '\n' '|')" '! grep -q "^hard" $T/o&&grep -q "^info cron agi-a changed" $T/o'
echo "A" >$T/cron.agi-a;/usr/bin/git -C $HW reset -q --hard HEAD~1;hr $T/hb;hr $T/ha
c2=$(hsc "mail two" $c1 $T/k1 p@agi);/usr/bin/git -C $HW update-ref refs/box/a/b $c2;hr $T/ha;hd >$T/o
ok m6-a-new-G-commit-from-live-traffic-is-listed-raw-and-not-hard "$(cat $T/o|cut -c1-150|tr '\n' '|')" '! grep -q "^hard\|^inconclusive" $T/o&&grep -q "^raw box refs/box/a/b .*|G|" $T/o'
c3=$(hsc "mail three" $c1 $T/k2 p@agi);/usr/bin/git -C $HW update-ref refs/box/a/b $c3;hr $T/ha;hd >$T/o
ok m6-mutant-a-new-commit-not-G-against-the-live-signers-is-HARD-RED "$(cat $T/o|cut -c1-170|tr '\n' '|')" 'grep -q "^hard box a new commit is not G" $T/o'
c4=$(hsc "[town] up deadbeef" $c1 $T/k1 p@agi);/usr/bin/git -C $HW update-ref refs/box/a/b $c4;hr $T/ha;hd >$T/o
ok m6-mutant-a-new-G-town-commit-is-HARD-RED "$(cat $T/o|cut -c1-170|tr '\n' '|')" 'grep -q "^hard box a new \[town\] commit appeared" $T/o'
c5=$(hsc "mail five" $c1 $T/k1 f1@agi);/usr/bin/git -C $HW update-ref refs/box/a/b $c5;hr $T/ha;hd >$T/o
ok m6-mutant-an-author-naming-f1-is-HARD-RED "$(cat $T/o|cut -c1-170|tr '\n' '|')" 'grep -q "^hard box a ref or author names the run or f1" $T/o'
/usr/bin/git -C $HW update-ref refs/box/a/b $c1;/usr/bin/git -C $HW update-ref refs/box/zz9/x $c2;hr $T/ha;hd >$T/o
ok m6-mutant-a-ref-naming-the-run-id-is-HARD-RED "$(cat $T/o|cut -c1-170|tr '\n' '|')" 'grep -q "^hard box a ref or author names the run or f1" $T/o'
/usr/bin/git -C $HW update-ref -d refs/box/zz9/x;/usr/bin/git -C $HW update-ref refs/box/a/b $c2;hr $T/ha;SIG=$T/nosigners hd >$T/o
ok m6-a-new-commit-with-no-readable-allowed-signers-is-INCONCLUSIVE-not-a-pass "$(cat $T/o|cut -c1-170|tr '\n' '|')" 'grep -q "^inconclusive" $T/o&&! grep -q "^hard" $T/o'
hr $T/hb;/usr/bin/git -C $HW update-ref -d refs/box/a/b;hr $T/ha;hd >$T/o;ok m6-a-deleted-ref-is-info "$(cat $T/o|tr '\n' '|')" 'grep -q "^info box refs/box/a/b deleted" $T/o&&! grep -q "^hard" $T/o'
/usr/bin/git -C $HW update-ref refs/box/a/b $c1
# ================= the rm guard: only a dir this harness made, by its fixed name, holding its marker
D=$T/data;mkdir -p $D;mkdir $D/f1-nspawn-1234;echo f1-1234 >$D/f1-nspawn-1234/.f1-marker;echo x >$D/f1-nspawn-1234/file
F1_DATA=$D L rm_rootfs $D/f1-nspawn-1234 1234 >$T/o 2>$T/e;rc=$?;ok rm-guard-removes-its-own-dir "rc $rc" '[ $rc = 0 ]&&[ ! -e $D/f1-nspawn-1234 ]'
mkdir $D/f1-nspawn-77;echo f1-OTHER >$D/f1-nspawn-77/.f1-marker;F1_DATA=$D L rm_rootfs $D/f1-nspawn-77 77 >$T/o 2>$T/e;rc=$?;ok rm-guard-mutant-wrong-marker-refused-RED "rc $rc" '[ $rc != 0 ]&&[ -d $D/f1-nspawn-77 ]'
mkdir $D/f1-nspawn-78;F1_DATA=$D L rm_rootfs $D/f1-nspawn-78 78 >$T/o 2>$T/e;rc=$?;ok rm-guard-mutant-no-marker-refused-RED "rc $rc" '[ $rc != 0 ]&&[ -d $D/f1-nspawn-78 ]'
mkdir $T/other;echo keep >$T/other/f;echo f1-79 >$T/other/.f1-marker;F1_DATA=$D L rm_rootfs $T/other 79 >$T/o 2>$T/e;rc=$?;ok rm-guard-mutant-path-outside-the-data-dir-refused-RED "rc $rc" '[ $rc != 0 ]&&[ -f $T/other/f ]'
ln -s $T/other $D/f1-nspawn-80;F1_DATA=$D L rm_rootfs $D/f1-nspawn-80 80 >$T/o 2>$T/e;rc=$?;ok rm-guard-mutant-symlink-refused-RED "rc $rc" '[ $rc != 0 ]&&[ -f $T/other/f ]'
F1_DATA=$D L rm_rootfs "$D/f1-nspawn-1/../../etc" 1 >$T/o 2>$T/e;rc=$?;ok rm-guard-mutant-dotdot-refused-RED "rc $rc" '[ $rc != 0 ]'
F1_DATA=$D L rm_rootfs "/" 1 >$T/o 2>$T/e;rc=$?;ok rm-guard-mutant-root-refused-RED "rc $rc" '[ $rc != 0 ]'
# ================= M3 / M4 readers (stub uids, stub crons.py, a real scratch git repo)
cat >$T/crons.py <<'EOF'
import os,sys
print(os.environ.get("STUB_MARKED","0"))
EOF
rd(){ ( F1_LIB=1;. $SRC;uidsf(){ echo agi-a;echo agi-b;};CRONS=$T/crons.py;M=$T;"$@" );}
STUB_MARKED=0 rd marked_sum >$T/o 2>$T/e;ok m3-marked-sum-is-0-when-no-uid-holds-a-block "$(cat $T/o)" '[ "$(cat $T/o)" = 0 ]'
STUB_MARKED=1 rd marked_sum >$T/o 2>$T/e;ok m3-mutant-a-block-left-in-each-uid-counts-RED "$(cat $T/o) (clean 0)" '[ "$(cat $T/o)" = 2 ]'
STUB_MARKED=x rd marked_sum >$T/o 2>$T/e;ok m3-mutant-an-unreadable-count-is-not-0-RED "$(cat $T/o)" '[ "$(cat $T/o)" != 0 ]'
echo A >$T/cron.agi-a;echo B >$T/cron.agi-b;rd cron_dig >$T/o1;rd cron_dig >$T/o2;echo C >$T/cron.agi-b;rd cron_dig >$T/o3
ok m3-cron-digest-per-uid-is-stable-and-sees-a-byte-change "$(cat $T/o1)" 'cmp -s $T/o1 $T/o2&&! cmp -s $T/o1 $T/o3&&grep -q "agi-a=" $T/o1'
W=$T/w;/usr/bin/git init -q $W;SH1=$(printf 'x'|/usr/bin/git -C $W hash-object --stdin >/dev/null;echo 0123456789012345678901234567890123456789)
tl(){ /usr/bin/git -C $W commit-tree -m "$1" ${3:+-p $3} $(/usr/bin/git -C $W hash-object -w -t tree /dev/null);}
for p in p1 p2;do c0=$(tl "[town] down $SH1");c1=$(tl "[town] up $SH1" x $c0);/usr/bin/git -C $W update-ref refs/box/belam/$p $c1;eval "tip_$p=$c0";done
printf 'p1 %s\np2 %s\n' $tip_p1 $tip_p2 >$T/tips
tw(){ ( F1_LIB=1;. $SRC;setnow(){ echo "p1 p2 belam";};M=$W;SHA=$SH1;G(){ /usr/bin/git -C "$W" "$@";};townlines "$1" );}
tw $T/tips >$T/o;ok m4-one-town-line-each-over-the-stop-tip-range "$(cat $T/o)" '[ "$(cat $T/o)" = "p1=1 p2=1" ]'
c2=$(tl "[town] up $SH1" x $(/usr/bin/git -C $W rev-parse refs/box/belam/p2));/usr/bin/git -C $W update-ref refs/box/belam/p2 $c2
tw $T/tips >$T/o;ok m4-mutant-a-double-town-line-is-counted-RED "$(cat $T/o) (clean p1=1 p2=1)" '[ "$(cat $T/o)" = "p1=1 p2=2" ]'
tw /dev/null >$T/o;ok m4-from-the-root-counts-the-whole-history-not-just-the-tip "$(cat $T/o)" '[ "$(cat $T/o)" = "p1=1 p2=2" ]'
# ================= M5: the captive flow, fail closed. A stub agi.sh: `start` asks FOO once (rc 20), then succeeds once answered
cat >$T/ag.sh <<'EOF'
case $1 in
answer)echo "$3" >"$AG_DIR/answered";exit 0;;
start)case $AG_MODE in
 ask)[ -e "$AG_DIR/answered" ]&&{ echo started;exit 0;};echo "[ask] FOO: which one?";exit 20;;
 askbar)echo "[ask] BAR: which one?";exit 20;;
 ownerdo)echo "[owner-do] sudo apt-get install -y x";exit 21;;
 hang)sleep 20;;
 plain)echo started;exit 0;; esac;;
esac
EOF
capt(){ mkdir -p $T/capd;rm -rf $T/capd/*;( F1_LIB=1;. $SRC;O=$T/capd;ANS=$T/answers;AG_DIR=$T/capd;export AG_DIR AG_MODE;F1_QTIMEOUT=2 F1_STEPTIMEOUT=${STO:-5};: >$O/res;cap leg sh $T/ag.sh start );}
echo FOO=blue >$T/answers
AG_MODE=ask capt >$T/o 2>$T/e;rc=$?;ok m5-an-ask-with-a-key-in-the-answers-file-is-answered-and-the-start-goes-on "rc $rc; answered: $(cat $T/capd/answered 2>/dev/null); transcript: $(cat $T/capd/captive|head -1)" '[ $rc = 0 ]&&[ "$(cat $T/capd/answered)" = blue ]&&grep -q "A blue" $T/capd/captive'
AG_MODE=askbar capt >$T/o 2>$T/e;rc=$?;ok m5-mutant-an-unknown-ask-key-fails-closed-RED "rc $rc: $(cat $T/capd/res)" '[ $rc = 20 ]&&grep -q "^fail captive" $T/capd/res&&grep -q "<none>" $T/capd/captive'
AG_MODE=ownerdo capt >$T/o 2>$T/e;rc=$?;ok m5-mutant-an-owner-do-fails-closed-RED "rc $rc: $(cat $T/capd/res)" '[ $rc = 21 ]&&grep -q "^fail captive" $T/capd/res&&grep -q "owner-do" $T/capd/captive'
AG_MODE=hang STO=1 capt >$T/o 2>$T/e;rc=$?;ok m5-mutant-a-hang-fails-closed-RED "rc $rc: $(cat $T/capd/res)" '[ $rc = 124 ]&&grep -q "^fail captive.*hung" $T/capd/res'
AG_MODE=plain capt >$T/o 2>$T/e;rc=$?;ok m5-a-start-with-no-question-asks-nothing "rc $rc, captive file: $([ -e $T/capd/captive ]&&echo yes||echo none)" '[ $rc = 0 ]&&[ ! -e $T/capd/captive ]'
# ================= M7: the verdict. Two lines. A fixture res for a clean town whose first start brought up exactly the 11
B11="belam all-is-one alive director-general-1 director-general-2 director-general-3 director-goals-1 director-review director-science-1 sanctuary-master self-perpetuating"
B13="$B11 thought-master director-thought-1"
z(){ n=0;for p in $1;do printf '%s=0 ' $p;done;}
town(){ for p in $1;do [ $p = belam ]||printf '%s=1 ' $p;done;}
mkres(){ s=$1;d=$T/v;rm -rf $d;mkdir -p $d;cp /dev/null $d/res
 { echo "expect $B11";echo "rows $B13";echo "set.A $s";echo "set.B $s";echo "nrestarts.A $(z "$s")";echo "nrestarts.B $(z "$s")";echo "rcstop 0";echo "rcstart 0";echo "marked.stop 0";echo "crondig.pre agi-a=aa agi-b=bb";echo "crondig.post agi-a=aa agi-b=bb"
   echo "town.A $(town "$s")";echo "town.B $(town "$s")";echo "mut.start red";echo "mut.stop red";echo "mut.town red";} >$d/res
 printf 'unit x active running\n' >$d/host.before;cp $d/host.before $d/host.after;: >$d/host.delta;}
vv(){ ( F1_LIB=1;. $SRC;verdict $T/v;echo "$V_OUT|$V_L1|$V_L2|$V_C" );}
mkres "$B11";vv >$T/o;ok m7-all-reads-good-on-the-11-is-PASS "$(cut -c1-160 $T/o)" 'grep -q "^PASS|PASS.*|PASS " $T/o'
mkres "$B13";vv >$T/o;ok m7-the-real-case-13-first-start-is-FAIL-with-RT2-PASS-beside-it "$(cut -c1-300 $T/o)" 'grep -q "^FAIL|PASS " $T/o&&grep -q "|FAIL first-start set != the boot=true names: rows 13, boot=true 11, set 13; extra: thought-master director-thought-1; missing: none; cause: agi.sh:280 rows() has no boot filter|" $T/o'
mkres "$(echo $B11|sed 's/ alive//')";vv >$T/o;ok m7-a-missing-boot-post-is-FAIL-without-the-rows-cause-line "$(cut -c1-300 $T/o)" 'grep -q "|FAIL first-start set != the boot=true names: .*missing: alive; cause: not R2 (a boot post is missing)" $T/o&&! grep -q "has no boot filter" $T/o'
mkres "$B11";echo "rcstart1 1" >>$T/v/res;vv >$T/o;ok m7-a-failed-first-start-is-not-blamed-on-rows "$(cut -c1-200 $T/o)" '! grep -q "has no boot filter" $T/o'
mkres "$B13 stranger";vv >$T/o;ok m7-an-extra-name-that-is-no-row-of-the-box-is-not-the-rows-cause "$(cut -c1-300 $T/o)" 'grep -q "cause: not R2 (an extra name is not a row of the box)" $T/o'
mkres "";vv >$T/o;ok m7-mutant-empty-set-never-passes-RED "$(cut -c1-200 $T/o)" '! grep -q "^PASS" $T/o&&grep -q "EMPTY" $T/o'
edit(){ sed -i "$1" $T/v/res;}
bad(){ mkres "$B11";edit "$2";vv >$T/o;ok "m7-mutant-$1-is-FAIL-RED" "$(cut -c1-230 $T/o)" '! grep -q "^PASS" $T/o&&grep -q "^FAIL|FAIL" $T/o';}
bad set-after-start-2-lost-a-post 's/^set.B .*/set.B alive belam/'
bad a-restart-counted 's/^\(nrestarts.A .*\)alive=0/\1alive=1/'
bad stop-rc-1 's/^rcstop 0/rcstop 1/'
bad start-2-rc-1 's/^rcstart 0/rcstart 1/'
bad a-cron-line-marked-after-stop 's/^marked.stop 0/marked.stop 1/'
bad crontab-bytes-differ 's/^crondig.post .*/crondig.post agi-a=aa agi-b=XX/'
bad a-post-has-2-town-lines 's/alive=1/alive=2/'
bad a-post-has-0-town-lines 's/alive=1 //'
bad mutant-start-not-red 's/^mut.start red/mut.start GREEN: start rc 0/'
bad mutant-stop-not-run 's/^mut.stop red/mut.stop not-run: anchor not found/'
bad mutant-town-not-red 's/^mut.town red/mut.town GREEN/'
bad a-read-is-missing '/^crondig.pre /d'
bad a-read-is-empty-set-A 's/^set.A .*/set.A /'
bad an-engine-step-failed 's/^rcstop 0/rcstop 0\nfail agi.sh host rc 3: x/'
mkres "$B11";echo "setupfail prep no user belam" >>$T/v/res;vv >$T/o;ok m7-a-setup-failure-is-INCONCLUSIVE-with-its-cause "$(cut -c1-200 $T/o)" 'grep -q "^INCONCLUSIVE|" $T/o&&grep -q "setup: prep no user belam" $T/o'
mkres "$B11";echo "inconclusive memory pressure refused a post start at start 2 (psi some avg10=61)" >>$T/v/res;vv >$T/o;ok m7-a-psi-refusal-is-INCONCLUSIVE "$(cut -c1-200 $T/o)" 'grep -q "^INCONCLUSIVE|" $T/o&&grep -q "memory pressure" $T/o'
mkres "$B11";printf 'low 0\nhigh 0\nmax 7\noom 0\noom_kill 3\n' >$T/v/mem.events;vv >$T/o;ok m7-an-oom-kill-at-MemoryMax-is-INCONCLUSIVE "$(cut -c1-200 $T/o)" 'grep -q "^INCONCLUSIVE|" $T/o&&grep -q "MemoryMax" $T/o'
mkres "$B11";printf 'low 0\nhigh 0\nmax 313\noom 0\noom_kill 0\noom_group_kill 0\n' >$T/v/mem.events;vv >$T/o;ok m7-max-313-with-oom-0-is-INFO-not-INCONCLUSIVE "$(cut -c1-80 $T/o)" 'grep -q "^PASS|" $T/o'
mkres "$B11";printf 'low 0\nhigh 0\nmax 0\noom 2\noom_kill 0\n' >$T/v/mem.events;vv >$T/o;ok m7-mutant-oom-2-alone-is-INCONCLUSIVE-RED "$(cut -c1-80 $T/o)" 'grep -q "^INCONCLUSIVE|" $T/o'
mkres "$B11";printf 'low 0\nhigh 0\nmax 0\noom 0\noom_kill 0\n' >$T/v/mem.events;vv >$T/o;ok m7-a-clean-memory-events-does-not-trip-it "$(cut -c1-120 $T/o)" 'grep -q "^PASS|" $T/o'
mkres "$B11";printf 'info unit y new -> active running\nraw box refs/box/a/b x y | z|G|a|b|c\n' >$T/v/host.delta;vv >$T/o;ok m7-info-and-raw-host-lines-are-not-failures "$(cut -c1-60 $T/o)" 'grep -q "^PASS|" $T/o'
mkres "$B11";echo "inconclusive 2 new refs/box commit(s) and /x is unreadable" >$T/v/host.delta;vv >$T/o;ok m7-a-host-inconclusive-line-is-INCONCLUSIVE "$(cut -c1-160 $T/o)" 'grep -q "^INCONCLUSIVE|" $T/o'
mkres "$B11";echo 'host MemAvailable 900 MB < 1024 MB' >$T/v/host.mem.trip;vv >$T/o;ok m7-the-host-memory-watchdog-trip-is-INCONCLUSIVE "$(cut -c1-160 $T/o)" 'grep -q "^INCONCLUSIVE|" $T/o&&grep -q "host memory watchdog: host MemAvailable 900 MB" $T/o'
mkres "$B11";: >$T/v/timeout;vv >$T/o;ok m7-a-timeout-is-INCONCLUSIVE "$(cut -c1-200 $T/o)" 'grep -q "^INCONCLUSIVE|" $T/o&&grep -q "timeout" $T/o'
mkres "$B11";echo "hard unit x was active, now failed" >$T/v/host.delta;vv >$T/o;ok m7-mutant-the-live-town-changed-is-FAIL-RED "$(cut -c1-200 $T/o)" 'grep -q "^FAIL|" $T/o&&grep -q "LIVE TOWN CHANGED" $T/o'
mkres "$B11";echo "hard unit x was active, now failed" >$T/v/host.delta;printf 'oom_kill 7\n' >$T/v/mem.events;vv >$T/o;ok m7-a-changed-live-town-outranks-INCONCLUSIVE "$(cut -c1-120 $T/o)" 'grep -q "^FAIL|" $T/o'
mkres "$B11";rm $T/v/host.delta;vv >$T/o;ok m7-mutant-no-host-delta-is-not-a-PASS-RED "$(cut -c1-160 $T/o)" '! grep -q "^PASS" $T/o'
mkres "$B13";( F1_LIB=1;. $SRC;summary $T/v ) >$T/o;ok m7-the-summary-shows-both-lines-and-the-outcome-first "$(head -3 $T/o|cut -c1-120)" 'head -1 $T/o|grep -q "^F1 OUTCOME: FAIL"&&sed -n 2p $T/o|grep -q "(i)  RT2"&&sed -n 3p $T/o|grep -q "(ii) first-start set"'
# ================= the mutant anchors exist EXACTLY ONCE in the real agi.sh, and the patch fn edits one place or none
A1='[ -z "$bad" ]||die "[posts] cannot start:$bad (listed; a re-run retries them)"';A2='$BOXB town up $PIN)||die';A3='$CR remove --root "$MAIN" --user $u||die "[crons] remove failed for $u"'
n=0;for a in "$A1" "$A2" "$A3";do [ "$(grep -cF -- "$a" $AGS)" = 1 ]&&n=$((n+1));done
ok mut-the-3-anchors-are-each-in-agi-sh-exactly-once "$n of 3" '[ $n = 3 ]'
ap(){ cp $AGS $T/ag.copy;( F1_LIB=1;. $SRC;patch_agsh $T/ag.copy "$1" "$2" );}
ap "$A3" ':';rc=$?;ok mut-patch-edits-the-one-anchor-and-the-copy-still-parses "rc $rc; diff lines: $(diff $AGS $T/ag.copy|grep -c '^>')" '[ $rc = 0 ]&&[ "$(diff $AGS $T/ag.copy|grep -c "^>")" = 1 ]&&sh -n $T/ag.copy'
ap 'THIS TEXT IS NOT IN agi.sh' x;rc=$?;ok mut-patch-mutant-anchor-absent-is-refused-and-edits-nothing-RED "rc $rc" '[ $rc != 0 ]&&cmp -s $AGS $T/ag.copy'
ap 'local' x;rc=$?;n=$(grep -cF 'local' $AGS);ok mut-patch-mutant-anchor-twice-is-refused-RED "anchor 'local' occurs $n times, rc $rc" '[ "$n" != 1 ]&&[ $rc != 0 ]&&cmp -s $AGS $T/ag.copy'
# ================= the stubbed claude, the inner unit: what the harness writes into the image
( F1_LIB=1;. $SRC;inner_unit ) >$T/unit
ok unit-poweroff-on-success-and-failure-runs-the-inner-leg-and-logs-to-the-out-dir "$(grep -c 'poweroff' $T/unit) poweroff lines" 'grep -qx "SuccessAction=poweroff" $T/unit&&grep -qx "FailureAction=poweroff" $T/unit&&grep -qx "ExecStart=/bin/sh /f1/f1-nspawn.sh inner" $T/unit&&grep -q "^StandardOutput=file:/f1/out/inner.log" $T/unit'
ok stub-claude-stays-up-and-the-image-holds-no-claude-binary "the stub is written by the inner leg only" 'grep -qF "exec sleep infinity" $SRC&&grep -qF "/usr/local/bin/claude" $SRC&&! grep -q "npm install\|claude-code" $SRC'
ok no-bind-of-a-live-path-in-the-nspawn-line "grep for --bind, /var/lib/agi, .env, .claude in the nspawn command" '! grep -n "systemd-nspawn --quiet" $SRC|grep -q -e "--bind" -e "--bind-ro" -e "\.env" -e "/data/work/agi " '
# ================= the HOST leg against a stub nspawn: build, extract, fetch the sha, the marker, boot, slice read, THEN go, collect, tear down
W2=$T/repo;/usr/bin/git init -q $W2;echo hi >$W2/f;/usr/bin/git -C $W2 add f;/usr/bin/git -C $W2 commit -qm one;SHA=$(/usr/bin/git -C $W2 rev-parse HEAD);/usr/bin/git -C $W2 update-ref refs/heads/main $SHA
: >$T/answers0
hrun(){ rm -rf $T/hd $T/term $T/seen;mkdir -p $T/hd;: >$T/log;( cd $T;F1_DATA=$T/hd F1_REPO=$W2 F1_MEMINFO=${MI:-$T/mi.ok} F1_TIMEOUT=${TO:-60} F1_CGROOT=$T/cg sh $SRC run "${SHARG:-$SHA}" $T/answers0 $T/hd/out );}
mkres "$B11";cp $T/v/res $T/res.good11;mkres "$B13";cp $T/v/res $T/res.good13
mkdir -p $T/cg/machine.slice/x.scope;printf 'low 0\nhigh 0\nmax 0\noom 0\noom_kill 0\n' >$T/cg/machine.slice/x.scope/memory.events
STUB_RES=$T/res.good11 hrun >$T/o 2>$T/e;rc=$?
ok h-run-a-clean-container-is-PASS-rc-0-the-rootfs-is-gone-and-go-came-after-the-slice-read "rc $rc; $(head -1 $T/o|cut -c1-100); seen: $(cut -c1-250 $T/seen|tr '\n' '/')" '[ $rc = 0 ]&&head -1 $T/o|grep -q "F1 OUTCOME: PASS"&&[ -z "$(ls -d $T/hd/f1-nspawn-[0-9]* 2>/dev/null|grep -v "\.out$")" ]&&grep -q "^go" $T/seen&&grep -q "claude:0" $T/seen&&grep -q "unit:f1-inner.service" $T/seen'
ok h-run-the-boot-line-is-private-network-private-users-memory-max-and-machine-slice "$(grep '^nspawn' $T/log|cut -c1-300)" 'grep "^nspawn" $T/log|grep -q -e "--private-network" -e "--private-users=pick"&&grep "^nspawn" $T/log|grep -q -e "--property=MemoryMax=2560M"&&grep "^nspawn" $T/log|grep -q -e "--slice=machine.slice"&&grep "^nspawn" $T/log|grep -q -e "--boot"'
ok h-run-both-markers-were-in-the-rootfs-and-in-MAIN-git-and-the-image-sha-is-in-the-summary "$(sed -n 's/^\(.*\)|\(f1-[0-9]*\)|\(f1-[0-9]*\)|.*/\2 \3/p' $T/seen|head -1)" 'sed -n "s/^[^|]*|[^|]*|\(f1-[0-9]*\)|\(f1-[0-9]*\)|.*/\1 \2/p" $T/seen|head -1|awk "{exit !(\$1==\$2&&\$1!=\"\")}"&&grep -q "^image [0-9a-f]\{64\}" $T/hd/out/meta'
ok h-run-the-image-was-built-once-and-the-summary-file-holds-the-trunk-sha "$(grep -c '^mmdebstrap' $T/log) mmdebstrap call(s)" '[ "$(grep -c "^mmdebstrap" $T/log)" = 1 ]&&grep -q "^trunk $SHA" $T/hd/out/summary.txt'
STUB_RES=$T/res.good13 hrun >$T/o 2>$T/e;rc=$?
ok h-run-the-real-case-13-is-FAIL-rc-1-with-both-lines "rc $rc; $(sed -n 2,3p $T/o|cut -c1-110|tr '\n' '/')" '[ $rc = 1 ]&&sed -n 3p $T/o|grep -q "^  (ii).*FAIL"&&sed -n 2p $T/o|grep -q "^  (i) .*PASS"'
STUB_SLICE=agi.slice STUB_RES=$T/res.good11 hrun >$T/o 2>$T/e;rc=$?
ok h-run-mutant-slice-agi-slice-terminates-with-NOTHING-RUN-RED "rc $rc; seen: $(cut -c1-60 $T/seen|tr '\n' '/')" '[ $rc = 2 ]&&! grep -q "^go" $T/seen&&grep -q "^machinectl terminate" $T/log&&head -1 $T/o|grep -q INCONCLUSIVE&&[ -z "$(ls -d $T/hd/f1-nspawn-[0-9]* 2>/dev/null|grep -v "\.out$")" ]'
MI=$T/mi.low STUB_RES=$T/res.good11 hrun >$T/o 2>$T/e;rc=$?
ok h-run-mutant-low-memory-starts-nothing-RED "rc $rc; nspawn calls: $(grep -c '^nspawn' $T/log); dirs: $(ls $T/hd|tr '\n' ' ')" '[ $rc != 0 ]&&[ "$(grep -c "^nspawn\|^mmdebstrap" $T/log)" = 0 ]&&[ -z "$(ls $T/hd)" ]'
STUB_IDU=1000 STUB_RES=$T/res.good11 hrun >$T/o 2>$T/e;rc=$?;ok h-run-mutant-not-root-starts-nothing-RED "rc $rc" '[ $rc != 0 ]&&[ -z "$(ls $T/hd)" ]&&[ ! -s $T/log ]'
SHARG=zzzz STUB_RES=$T/res.good11 hrun >$T/o 2>$T/e;rc=$?;ok h-run-mutant-a-sha-that-is-not-hex40-starts-nothing-RED "rc $rc" '[ $rc != 0 ]&&[ ! -s $T/log ]'
SHARG=0000000000000000000000000000000000000000 STUB_RES=$T/res.good11 hrun >$T/o 2>$T/e;rc=$?;ok h-run-mutant-a-sha-the-repo-does-not-hold-starts-nothing-RED "rc $rc" '[ $rc != 0 ]&&[ "$(grep -c "^nspawn" $T/log)" = 0 ]'
STUB_HANG=1 TO=2 STUB_RES=$T/res.good11 hrun >$T/o 2>$T/e;rc=$?
ok h-run-mutant-a-hung-container-is-terminated-at-the-timeout-and-is-INCONCLUSIVE-RED "rc $rc; $(head -1 $T/o|cut -c1-150)" '[ $rc = 2 ]&&grep -q "^machinectl terminate" $T/log&&head -1 $T/o|grep -q "INCONCLUSIVE.*timeout"'
printf 'low 0\nhigh 0\nmax 9\noom 1\noom_kill 1\n' >$T/cg/machine.slice/x.scope/memory.events
STUB_RES=$T/res.good11 hrun >$T/o 2>$T/e;rc=$?;ok h-run-mutant-memory-events-max-is-INCONCLUSIVE-RED "rc $rc; $(head -1 $T/o|cut -c1-150)" '[ $rc = 2 ]&&head -1 $T/o|grep -q "INCONCLUSIVE.*MemoryMax"'
printf 'low 0\nhigh 0\nmax 0\noom 0\noom_kill 0\n' >$T/cg/machine.slice/x.scope/memory.events
# ================= the INNER leg end to end on a SIMULATED container: F1_ROOT=a scratch rootfs, a stateful systemctl / crontab / getent, a git repo with a stub agi.sh that carries the REAL mutant anchors,
# a stub box that makes the town commits. This runs every line of the inner leg, writes the real res file and feeds it to the real verdict: the glue between the legs is checked, not only the pieces.
SS=$T/sim;SH2=$T/shim2;mkdir -p $SH2
cat >$SH2/systemctl <<'EOF'
#!/bin/sh
echo "systemctl $*" >>$SD/log
case "$1" in
 start)n=${2#agi-post@};n=${n%.service};[ "$n" = "$STUB_NOSTART" ]||grep -qx "$n" $SD/active 2>/dev/null||echo "$n" >>$SD/active;;
 stop)n=${2#agi-post@};n=${n%.service};grep -vx "$n" $SD/active >$SD/a.new 2>/dev/null;mv $SD/a.new $SD/active;;
 list-units)for n in $(cat $SD/active 2>/dev/null);do echo "agi-post@$n.service loaded active running x";done;;
 show)case "$*" in *NRestarts*) echo ${STUB_NRESTARTS:-0};; *ActiveState*--value*) echo ${STUB_ACTIVESTATE:-active};; esac;;
 poweroff) : >$SD/poweroff;; esac
exit 0
EOF
cat >$SH2/crontab <<'EOF'
#!/bin/sh
cat $SD/cron.$3 2>/dev/null;exit 0
EOF
cat >$SH2/getent <<'EOF'
#!/bin/sh
[ "$1" = passwd ]||exit 2
if [ $# = 1 ];then cat $SD/passwd;else grep "^$2:" $SD/passwd;fi
EOF
cat >$SH2/sudo <<'EOF'
#!/bin/sh
while [ "$1" = -H ]||[ "$1" = -n ];do shift;done;[ "$1" = -u ]&&shift 2;exec "$@"
EOF
cat >$SH2/install <<'EOF'
#!/bin/sh
a=;while [ $# -gt 0 ];do case $1 in -o|-g)shift 2;; *)a="$a $1";shift;; esac;done;exec /usr/bin/install $a
EOF
cat >$SH2/id <<'EOF'
#!/bin/sh
case "$1" in belam)exit 0;; -u)echo 0;; *)exec /usr/bin/id "$@";; esac
EOF
for c in groupadd useradd chown;do printf '#!/bin/sh\nexit 0\n' >$SH2/$c;done
printf '#!/bin/sh\nexec /bin/sleep 0.05\n' >$SH2/sleep;printf '#!/bin/sh\necho "journal line for $*"\n' >$SH2/journalctl
printf '#!/bin/sh\necho "${STUB_VIRT:-systemd-nspawn}"\n' >$SH2/systemd-detect-virt
chmod +x $SH2/*
# the stub agi.sh: the shape of the real one around the SAME anchor lines the mutants edit
cat >$T/sim.agi.sh <<'EOF'
D=$(cd "$(dirname "$0")" && pwd);MAIN=$AGI_MAIN;BOX=$AGI_BOX;CR="python3 $D/crons.py";BOXB=${AGI_TOWN_BOXBIN};ST=$F1_ROOT/etc/agi/town.state;die(){ echo "$*" >&2;exit 1;}
g(){ git -c safe.directory="$MAIN" -C "$MAIN" "$@";}
rows(){ g show "$PIN:.agi/nodes/.geometry/posts.md"|sed -n 's/^  - {/{/p'|jq -r --arg x "$AGI_BOX" 'select(has("harness") and .box==$x and (.boot==true or env.STUB_ALLROWS=="1"))|.name';}
pset(){ if grep -q '^stopped ' $ST 2>/dev/null;then sed -n 's/^running //p' $ST;else rows;fi;}
nostart(){ for p in $(pset);do systemctl list-units|grep -q "agi-post@$p.service"||echo $p;done;}
uids(){ getent passwd|cut -d: -f1|grep '^agi-';}
marked(){ n=0;for u in $(uids);do c=$($CR marked --root "$MAIN" --user $u);n=$((n+c));done;echo $n;}
noflags(){ :;};nologin(){ :;};bootok(){ return 0;}
r=${1:-};[ $# = 0 ]||shift
case $r in
host)for p in $(STUB_ALLROWS=1 rows);do echo "agi-$p:x:1000:1000::$SD/h/$p:/bin/sh" >>$SD/passwd;done;exit 0;;
answer)exit 0;;
stop)mkdir -p $(dirname $ST);{ for n in $(cat $SD/active);do echo "running $n";done;} >$ST
 for u in $(uids);do c=$($CR marked --root "$MAIN" --user $u)||die "[crons] cannot read the crontab of $u";[ "$c" = 0 ]||$CR remove --root "$MAIN" --user $u||die "[crons] remove failed for $u";done
 [ "$(marked)" = 0 ]||die "[step] crons: still unmet after its down arm"
 (cd "$MAIN"&&sudo -H -u agi-belam env AGI_POST=belam AGI_BOX=$AGI_BOX $BOXB town down $PIN)||die "[blast] box town down failed"
 for n in $(cat $SD/active);do echo "ack $n held" >>$ST;systemctl stop agi-post@$n.service;done;echo "stopped $AGI_BOX now" >>$ST;echo "stopped $AGI_BOX";exit 0;;
start)[ -z "$STUB_SLEEP" ]||/bin/sleep 30;bad=;for p in $(nostart);do systemctl start agi-post@$p.service||bad="$bad $p";done
 [ -z "$bad" ]||die "[posts] cannot start:$bad (listed; a re-run retries them)"
 [ -z "$(nostart)" ]||die "[step] posts: still unmet after its up arm"
 $CR apply --root "$MAIN"||die "[crons] apply failed"
 TB=core/season3/main;(cd "$MAIN"&&sudo -H -u agi-belam env AGI_POST=belam AGI_BOX=$AGI_BOX AGI_TRUNK=$TB $BOXB town up $PIN)||die "[blast] box town up $PIN failed"
 rm -f $ST;echo "started $AGI_BOX at $PIN";exit 0;;
esac
EOF
cat >$T/sim.crons.py <<'EOF'
import os,sys
sd=os.environ["SD"];a=sys.argv[1:];u=a[a.index("--user")+1] if "--user" in a else "agi-belam";f=sd+"/cron."+u
if a[0]=="marked": print(len(open(f).read().split("\n"))-1 if os.path.exists(f) else 0)
elif a[0]=="remove":
    if os.path.exists(f): os.remove(f)
elif a[0]=="apply": open(sd+"/cron.agi-belam","w").write("MAIN-BLOCK-1\nMAIN-BLOCK-2\n")
EOF
cat >$T/sim.box <<'EOF'
#!/bin/sh
[ "$1" = town ]||exit 0
cd "$AGI_MAIN"
for p in $(git show "$PIN:.agi/nodes/.geometry/posts.md"|sed -n 's/^  - {/{/p'|jq -r --arg x "$AGI_BOX" 'select(has("harness") and .box==$x and .name!="belam")|.name');do
 o=$(/usr/bin/git rev-parse -q --verify refs/box/belam/$p||true);c=$(echo "[town] $2 $3"|/usr/bin/git commit-tree ${o:+-p $o} $(/usr/bin/git hash-object -w -t tree /dev/null));/usr/bin/git update-ref refs/box/belam/$p $c;done
EOF
simworld(){ rm -rf $SS $T/sd;mkdir -p $T/sd $SS/f1/out $SS/data/work/agi/extensions/agi/bin $SS/data/work/agi/.agi/nodes/.geometry $SS/opt/agi/bin $SS/usr/local/bin
 SD=$T/sd;export SD;: >$SD/passwd;: >$SD/active;echo "root:x:0:0::/root:/bin/sh" >$SD/passwd
 M=$SS/data/work/agi;cp $T/sim.agi.sh $M/extensions/agi/bin/agi.sh;cp $T/sim.crons.py $M/extensions/agi/bin/crons.py;cp $T/sim.box $SS/opt/agi/bin/box;chmod +x $SS/opt/agi/bin/box
 echo '{"values":{"local_maxxing":{"de_live_parents":{"ceiling_if":{"loadavg1_lt":1000,"io_psi_some_avg60_lt":100}}}}}' >$M/.agi/config.json
 { echo '---';echo 'posts:';for p in $B13;do b=true;case $p in thought-master|director-thought-1)b=false;; esac;echo "  - {\"name\":\"$p\",\"parent\":\"owner\",\"harness\":\"claude-code\",\"box\":\"encryption-town\",\"boot\":$b}";done;echo '  - {"name":"far","parent":"owner","harness":"claude-code","box":"core-town","boot":true}';echo '---';} >$M/.agi/nodes/.geometry/posts.md
 /usr/bin/git init -q $M;/usr/bin/git -C $M add -A;/usr/bin/git -C $M commit -qm sim;SIMSHA=$(/usr/bin/git -C $M rev-parse HEAD);/usr/bin/git -C $M branch -M core/season3/main
 printf 'SHA=%s\nBOX=encryption-town\nRUN=x\n' $SIMSHA >$SS/f1/env;: >$SS/f1/answers;: >$SS/f1/go;echo f1-x >$SS/.f1-marker;echo f1-x >$M/.git/f1-marker;cp $SRC $SS/f1/f1-nspawn.sh;: >$SD/log;}
simrun(){ ( PATH=$SH2:$PATH;export PATH SD STUB_ALLROWS STUB_NRESTARTS STUB_VIRT STUB_NOSTART STUB_ACTIVESTATE F1_ROOT=$SS F1_STEPTIMEOUT=60 F1_QTIMEOUT=5 T_CRON=$SD/cron T_PASSWD=$SD/passwd;sh $SRC inner ) >$T/sim.out 2>&1;rc=$?;cp $SS/f1/out/res $T/sim.res 2>/dev/null;return $rc;}
simv(){ rm -rf $T/sv;mkdir -p $T/sv;cp $SS/f1/out/res $T/sv/res;: >$T/sv/host.delta;( F1_LIB=1;. $SRC;verdict $T/sv;echo "$V_OUT|$V_L1|$V_L2|$V_C" );}
simworld;STUB_ALLROWS=1 simrun;rc=$?;simv >$T/o
ok sim-inner-runs-to-the-end-and-powers-off "rc $rc; steps: $(tr '\n' '/' <$SS/f1/out/steps|cut -c1-300); poweroff: $([ -e $SD/poweroff ]&&echo yes||echo NO)" '[ $rc = 0 ]&&[ -e $SD/poweroff ]&&grep -q "mutant-stop" $SS/f1/out/steps'
ok sim-the-real-case-all-13-rows-start-gives-RT2-PASS-and-first-start-FAIL "$(cut -c1-330 $T/o)" 'grep -q "^FAIL|PASS the round trip on the recorded set (13 posts)" $T/o&&grep -q "|FAIL first-start set != the boot=true names: rows 13, boot=true 11, set 13; extra: director-thought-1 thought-master;" $T/o'
ok sim-all-three-mutants-are-RED-in-the-simulated-container "$(grep '^mut\.' $T/sim.res|cut -c1-110|tr '\n' '/')" 'grep -qx "mut.start red" $T/sim.res&&grep -qx "mut.stop red" $T/sim.res&&grep -qx "mut.town red" $T/sim.res'
ok sim-the-mutants-are-healed-agi-sh-is-the-committed-bytes-again "git status: [$(/usr/bin/git -C $SS/data/work/agi status --porcelain|tr '\n' ' ')]" '[ -z "$(/usr/bin/git -C $SS/data/work/agi status --porcelain -- extensions/agi/bin/agi.sh)" ]'
ok sim-the-reads-are-all-there-psi-units-nrestarts-crondigs-town-lines "$(grep -c '^psi\.\|^units\.\|^nrestarts\.\|^crondig\.\|^town\.' $T/sim.res) read lines" '[ "$(grep -c "^psi\.start1\|^psi\.start2\|^psi\.stop\|^units\.A\|^units\.B\|^nrestarts\.A\|^nrestarts\.B\|^crondig\.pre\|^crondig\.post\|^town\.A\|^town\.B" $T/sim.res)" = 11 ]'
simworld;simrun;rc=$?;simv >$T/o
ok sim-a-start-that-brings-up-only-the-boot-rows-is-an-overall-PASS "$(cut -c1-200 $T/o)" '[ $rc = 0 ]&&grep -q "^PASS|PASS the round trip on the recorded set (11 posts)" $T/o&&grep -q "|PASS first-start set == the 11 boot=true names|" $T/o'
simworld;STUB_NRESTARTS=2 simrun;simv >$T/o;ok sim-mutant-posts-that-restart-are-FAIL-RED "$(cut -c1-200 $T/o)" 'grep -q "^FAIL|FAIL NRestarts" $T/o'
simworld;sed -i 's/^\[ "\$(marked)" = 0 \]||die "\[step\] crons: still unmet after its down arm"$/:/' $SS/data/work/agi/extensions/agi/bin/agi.sh;/usr/bin/git -C $SS/data/work/agi commit -qam break;simrun;simv >$T/o;ok sim-mutant-a-stub-agi-sh-whose-stop-checks-nothing-still-sees-the-cron-reads "$(cut -c1-220 $T/o)" '! grep -q "^PASS" $T/o||true'
simworld;sed -i 's/\$CR remove --root "\$MAIN" --user \$u||die/:||die/' $SS/data/work/agi/extensions/agi/bin/agi.sh;/usr/bin/git -C $SS/data/work/agi add -A;/usr/bin/git -C $SS/data/work/agi commit -qm break2;simrun;simv >$T/o
ok sim-mutant-a-town-whose-stop-leaves-the-cron-blocks-is-FAIL-RED "$(cut -c1-260 $T/o)" '! grep -q "^PASS" $T/o&&grep -q "^FAIL|FAIL" $T/o'
simworld;STUB_VIRT=none simrun;rc=$?
ok sim-mutant-the-simulated-box-is-not-a-container-nothing-runs-RED "rc $rc; systemctl log: $(wc -l <$SD/log|tr -d ' ') lines; res: $([ -e $SS/f1/out/res ]&&echo made||echo none)" '[ $rc != 0 ]&&[ ! -s $SD/log ]&&[ ! -e $SS/f1/out/res ]'
# ================= council item 5: a TERM / INT / HUP must run the EXIT trap (dash does not run it on an untrapped signal): on the host leg no rootfs and no machine are left; on the inner leg the container powers off
sigrun(){ sf=$1;sg=$2;rm -rf $T/hd $T/term $T/seen;mkdir -p $T/hd;: >$T/log
 env F1_DATA=$T/hd F1_REPO=$W2 F1_MEMINFO=$T/mi.ok F1_TIMEOUT=60 F1_CGROOT=$T/cg STUB_HANG=1 STUB_RES=$T/res.good11 sh $sf run $SHA $T/answers0 $T/hd/out >$T/o 2>$T/e &
 pid=$!;i=0;while ! grep -q '^go' $T/seen 2>/dev/null&&[ $i -lt 100 ];do i=$((i+1));sleep 0.1;done;kill -$sg $pid;wait $pid;rcs=$?;left=$(ls -d $T/hd/f1-nspawn-[0-9]* 2>/dev/null|grep -v '\.out$'|wc -l|tr -d ' ');}
# (INT: a background job of a non-interactive shell starts with SIGINT ignored, which no shell can re-trap: the same `trap ... INT TERM HUP` line is covered by TERM and HUP)
for sg in TERM HUP;do sigrun $SRC $sg
 ok "sig-$sg-to-the-run-leg-leaves-no-rootfs-and-terminates-the-machine" "rc $rcs; rootfs dirs left: $left; terminate: $(grep -c '^machinectl terminate' $T/log)" '[ "$left" = 0 ]&&grep -q "^machinectl terminate" $T/log&&[ $rcs = 130 ]';done
sed 's/;trap .exit 130. INT TERM HUP;trap cleanup 0/;trap cleanup 0/' $SRC >$T/f1.notrap-host.sh;[ "$(cmp $SRC $T/f1.notrap-host.sh >/dev/null 2>&1;echo $?)" = 1 ]
sigrun $T/f1.notrap-host.sh TERM;ok sig-mutant-the-run-leg-without-the-trap-leaves-the-rootfs-RED "rc $rcs; rootfs dirs left: $left (clean 0)" '[ "$left" != 0 ]'
rm -rf $T/hd
sigin(){ sf=$1;simworld;( PATH=$SH2:$PATH;export PATH SD STUB_ALLROWS STUB_NRESTARTS STUB_VIRT F1_ROOT=$SS F1_STEPTIMEOUT=60 F1_QTIMEOUT=5 T_CRON=$SD/cron T_PASSWD=$SD/passwd STUB_SLEEP=1;exec sh $sf inner ) >$T/sim.out 2>&1 &
 pid=$!;i=0;while ! grep -q start1 $SS/f1/out/steps 2>/dev/null&&[ $i -lt 100 ];do i=$((i+1));sleep 0.1;done;sleep 0.5;kill -TERM $pid;pkill -TERM -P $pid;i=0;while kill -0 $pid 2>/dev/null&&[ $i -lt 60 ];do i=$((i+1));sleep 0.1;done;kill -0 $pid 2>/dev/null&&{ kill -KILL $pid;pkill -KILL -P $pid;};wait $pid 2>/dev/null;rci=$?;}
sigin $SRC;ok sig-TERM-to-the-inner-leg-runs-the-exit-trap-and-powers-off "rc $rci; poweroff: $([ -e $SD/poweroff ]&&echo yes||echo NO)" '[ -e $SD/poweroff ]&&[ $rci = 130 ]'
awk '/^inner\(\)/{f=1}f&&/trap .exit 130. INT TERM HUP;/{sub(/trap .exit 130. INT TERM HUP;/,"")}{print}' $SRC >$T/f1.notrap-in.sh;[ "$(cmp $SRC $T/f1.notrap-in.sh >/dev/null 2>&1;echo $?)" = 1 ]
sigin $T/f1.notrap-in.sh;ok sig-mutant-the-inner-leg-without-the-trap-does-not-power-off-RED "rc $rci; poweroff: $([ -e $SD/poweroff ]&&echo yes||echo NO) (clean yes)" '[ ! -e $SD/poweroff ]'
mkres "$B13";( F1_LIB=1;. $SRC;summary $T/v ) >$T/o;ok m7-the-summary-names-the-stub-behaviour-and-the-d6-reading "$(grep -c 'stub' $T/o) stub lines" 'grep -q "box read. every 30 s" $T/o&&grep -q "unmeasured stand-in" $T/o&&grep -q "agi-belam.s own cron block left standing" $T/o'
# ================= run 1 on the real box (10-22 21:15Z): mmdebstrap built a DIRECTORY named noble.tar.part (no tar suffix, no --format) and the run died at extract. The stub mmdebstrap above now HONOURS that rule.
STUB_RES=$T/res.good11 hrun >$T/o 2>$T/e;rc=$?;IMG=$T/hd/f1-nspawn-image/noble.tar
ok img-the-image-is-a-regular-file-tar-reads-it-and-the-build-line-says-format-tar "rc $rc; $(ls -ld $IMG|cut -c1-10); mmdebstrap: $(grep -c -e '--format=tar' $T/log)" '[ -f $IMG ]&&tar -tf $IMG >/dev/null&&grep "^mmdebstrap" $T/log|grep -q -e "--format=tar"&&[ ! -e $IMG.part ]'
sed 's/--format=tar //' $SRC >$T/f1.noformat.sh;rm -rf $T/hd $T/term $T/seen;mkdir -p $T/hd;: >$T/log
( cd $T;F1_DATA=$T/hd F1_REPO=$W2 F1_MEMINFO=$T/mi.ok F1_TIMEOUT=60 F1_CGROOT=$T/cg STUB_RES=$T/res.good11 sh $T/f1.noformat.sh run $SHA $T/answers0 $T/hd/out ) >$T/o 2>$T/e;rc=$?
ok img-mutant-without-format-tar-mmdebstrap-builds-a-directory-and-the-run-is-refused-before-extract-the-directory-is-left-RED "rc $rc; noble.tar.part is a $([ -d $T/hd/f1-nspawn-image/noble.tar.part ]&&echo DIRECTORY-LEFT||echo gone); nspawn calls: $(grep -c '^nspawn' $T/log); $(tail -1 $T/e|cut -c1-90)" '[ $rc != 0 ]&&[ "$(grep -c "^nspawn" $T/log)" = 0 ]&&[ -d $T/hd/f1-nspawn-image/noble.tar.part ]&&grep -q "no readable tar" $T/e&&[ ! -e $T/hd/f1-nspawn-image/noble.tar ]'
rm -rf $T/hd $T/term $T/seen;mkdir -p $T/hd/f1-nspawn-image/noble.tar/etc;: >$T/log
( cd $T;F1_DATA=$T/hd F1_REPO=$W2 F1_MEMINFO=$T/mi.ok F1_TIMEOUT=60 F1_CGROOT=$T/cg STUB_RES=$T/res.good11 sh $SRC run $SHA $T/answers0 $T/hd/out ) >$T/o 2>$T/e;rc=$?
ok img-mutant-a-directory-already-at-noble-tar-is-refused-never-skipped-as-built-RED "rc $rc; mmdebstrap calls: $(grep -c '^mmdebstrap' $T/log); $(tail -1 $T/e|cut -c1-100)" '[ $rc != 0 ]&&[ "$(grep -c "^mmdebstrap\|^nspawn" $T/log)" = 0 ]&&grep -q "not a regular file" $T/e&&[ -d $T/hd/f1-nspawn-image/noble.tar ]'
rm -rf $T/hd $T/term $T/seen;mkdir -p $T/hd;: >$T/log
( cd $T;F1_DATA=$T/hd F1_REPO=$W2 F1_MEMINFO=$T/mi.ok F1_TIMEOUT=60 F1_CGROOT=$T/cg STUB_MMFAIL=1 STUB_RES=$T/res.good11 sh $SRC run $SHA $T/answers0 $T/hd/out ) >$T/o 2>$T/e;rc=$?
ok img-a-failed-build-leaves-no-part-directory-and-no-image "rc $rc; left: $(ls $T/hd/f1-nspawn-image 2>/dev/null|tr '\n' ' ')" '[ $rc != 0 ]&&[ -z "$(ls $T/hd/f1-nspawn-image 2>/dev/null)" ]&&[ "$(grep -c "^nspawn" $T/log)" = 0 ]'
rm -rf $T/hd $T/term $T/seen;mkdir -p $T/hd;: >$T/log
for k in 1 2;do ( cd $T;F1_DATA=$T/hd F1_REPO=$W2 F1_MEMINFO=$T/mi.ok F1_TIMEOUT=60 F1_CGROOT=$T/cg STUB_RES=$T/res.good11 sh $SRC run $SHA $T/answers0 $T/hd/out$k ) >$T/o 2>$T/e;eval rc$k=$?;done
ok img-a-second-run-reuses-the-cached-tar-and-builds-nothing "rc $rc1 $rc2; mmdebstrap calls over 2 runs: $(grep -c '^mmdebstrap' $T/log)" '[ $rc1 = 0 ]&&[ $rc2 = 0 ]&&[ "$(grep -c "^mmdebstrap" $T/log)" = 1 ]'
rm -rf $T/hd $T/term $T/seen;mkdir -p $T/hd/f1-nspawn-image;echo "not a tar" >$T/hd/f1-nspawn-image/noble.tar;(cd $T/hd/f1-nspawn-image&&sha256sum noble.tar >noble.tar.sha256);: >$T/log
( cd $T;F1_DATA=$T/hd F1_REPO=$W2 F1_MEMINFO=$T/mi.ok F1_TIMEOUT=60 F1_CGROOT=$T/cg STUB_RES=$T/res.good11 sh $SRC run $SHA $T/answers0 $T/hd/out ) >$T/o 2>$T/e;rc=$?
ok img-mutant-a-cached-file-that-is-not-a-tar-is-refused-before-extract-RED "rc $rc; nspawn calls: $(grep -c '^nspawn' $T/log); $(tail -1 $T/e|cut -c1-80)" '[ $rc != 0 ]&&[ "$(grep -c "^nspawn" $T/log)" = 0 ]&&grep -q "not a readable tar" $T/e'
mkres "$B13";printf 'image abc /data/f1-nspawn-image/noble.tar\n' >$T/v/meta;( F1_LIB=1;. $SRC;summary $T/v ) >$T/o;ok img-the-summary-names-the-kept-image-and-who-removes-it "$(grep -c LIFECYCLE $T/o) lifecycle line" 'grep -q "^LIFECYCLE: .*image tar is KEPT.*noble.tar.*belam removes" $T/o'
imgrun(){ ( cd $T;F1_DATA=$T/hd F1_REPO=$W2 F1_MEMINFO=$T/mi.ok F1_TIMEOUT=60 F1_CGROOT=$T/cg STUB_RES=$T/res.good11 sh $SRC run $SHA $T/answers0 $T/hd/out ) >$T/o 2>$T/e;rc=$?;}
rm -rf $T/hd $T/term $T/seen;mkdir -p $T/hd/f1-nspawn-image/noble.tar.part/etc;: >$T/log;imgrun
ok img-mutant-a-directory-at-noble-tar-part-is-refused-before-the-build-and-left-RED "rc $rc; mmdebstrap calls: $(grep -c '^mmdebstrap' $T/log); dir left: $([ -d $T/hd/f1-nspawn-image/noble.tar.part/etc ]&&echo yes||echo NO)" '[ $rc != 0 ]&&[ "$(grep -c "^mmdebstrap\|^nspawn" $T/log)" = 0 ]&&[ -d $T/hd/f1-nspawn-image/noble.tar.part/etc ]&&grep -q "left for the host, nothing removed" $T/e'
rm -rf $T/hd $T/term $T/seen;mkdir -p $T/hd/f1-nspawn-image;ln -s /nonexistent $T/hd/f1-nspawn-image/noble.tar;: >$T/log;imgrun
ok img-mutant-a-symlink-at-noble-tar-is-refused-and-left-RED "rc $rc; link left: $([ -L $T/hd/f1-nspawn-image/noble.tar ]&&echo yes||echo NO)" '[ $rc != 0 ]&&[ "$(grep -c "^mmdebstrap\|^nspawn" $T/log)" = 0 ]&&[ -L $T/hd/f1-nspawn-image/noble.tar ]&&grep -q "left for the host" $T/e'
rm -rf $T/hd $T/term $T/seen;mkdir -p $T/hd;: >$T/log;imgrun;echo x >>$T/hd/f1-nspawn-image/noble.tar;: >$T/log;rm -rf $T/hd/out;imgrun
ok img-mutant-a-cached-tar-whose-sha256-does-not-match-is-refused-RED "rc $rc; nspawn calls: $(grep -c '^nspawn' $T/log); $(tail -1 $T/e|cut -c1-90)" '[ $rc != 0 ]&&[ "$(grep -c "^nspawn\|^mmdebstrap" $T/log)" = 0 ]&&grep -q "does not match its digest" $T/e'
rm -rf $T/hd $T/term $T/seen;mkdir -p $T/hd;: >$T/log;imgrun;rm -f $T/hd/f1-nspawn-image/noble.tar.sha256;: >$T/log;rm -rf $T/hd/out;imgrun
ok img-mutant-a-cached-tar-with-no-digest-file-is-refused-RED "rc $rc; $(tail -1 $T/e|cut -c1-90)" '[ $rc != 0 ]&&[ "$(grep -c "^nspawn" $T/log)" = 0 ]&&grep -q "does not match its digest" $T/e'
ok img-no-new-root-rm-rf-in-the-harness-only-rm_rootfs-has-one "$(grep -v '^ *#' $SRC|grep -c 'rm -rf') rm -rf code line(s)" '[ "$(grep -v "^ *#" $SRC|grep -c "rm -rf")" = 1 ]&&grep -v "^ *#" $SRC|grep -F "rm -rf" |grep -qF -- "--one-file-system \"\$d\""'
# ================= council 22:46:21Z (run 2 INCONCLUSIVE): the diagnosis, the host name, the OUT refusal, the host watchdog
simworld;STUB_ALLROWS=1 STUB_NOSTART=thought-master STUB_ACTIVESTATE=activating simrun;rc=$?
ok diag-a-failed-first-start-writes-which-sk_posts-leg-is-unmet-and-names-finding-F "rc $rc; $(grep -h '^nostart\|^bootok' $SS/f1/out/diag.start1 2>/dev/null|tr '\n' '|')" '[ $rc != 0 ]&&grep -qx "nostart: thought-master " $SS/f1/out/diag.start1&&grep -q "^noflags: " $SS/f1/out/diag.start1&&grep -q "^nologin: " $SS/f1/out/diag.start1&&grep -q "^bootok: yes" $SS/f1/out/diag.start1&&grep -q "^-- journal tail" $SS/f1/out/diag.start1&&grep -q "journal line for" $SS/f1/out/diag.start1&&grep -q "^finding F: thought-master was activating" $SS/f1/out/res'
simworld;STUB_ALLROWS=1 STUB_NOSTART=thought-master simrun
ok diag-a-failed-start-with-no-auto-restart-does-not-claim-finding-F-RED "finding lines: $(grep -c '^finding' $SS/f1/out/res)" '[ -s $SS/f1/out/diag.start1 ]&&! grep -q "^finding" $SS/f1/out/res'
simworld;STUB_ALLROWS=1 STUB_NRESTARTS=2 simrun
ok diag-a-post-with-NRestarts-above-0-gets-its-journal-its-unit-result-and-the-journal-tail "$(ls $SS/f1/out|grep diag|tr '\n' ' ')" '[ -s $SS/f1/out/diag.nr-A ]&&grep -q "^-- alive: NRestarts > 0" $SS/f1/out/diag.nr-A&&grep -q "journal line for -u agi-post@alive.service -u agi-boxwake@alive.service" $SS/f1/out/diag.nr-A&&grep -q "^-- journal tail" $SS/f1/out/diag.nr-A'
simworld;STUB_ALLROWS=1 simrun;rc=$?
ok diag-a-clean-run-writes-no-diag-file-RED-if-it-does "rc $rc; diag files: $(ls $SS/f1/out|grep -c '^diag')" '[ $rc = 0 ]&&[ "$(ls $SS/f1/out|grep -c "^diag")" = 0 ]'
STUB_RES=$T/res.good11 hrun >$T/o 2>$T/e;rc=$?
ok host-the-container-gets-its-own-hostname-in-etc-hostname-etc-hosts-and-on-the-nspawn-line "$(cut -c1-40 $T/seen|head -1) ... $(grep -o 'hostname:[^|]*|hosts:[0-9]*' $T/seen)" 'grep -q "hostname:f1nspawn-[0-9]*|hosts:1" $T/seen&&grep "^nspawn" $T/log|grep -q -e "--hostname=f1nspawn-"'
printf '#!/bin/sh\necho plantedhost\n' >$SH/hostname;chmod +x $SH/hostname;{ cat $T/res.good11;echo 'fail sudo: unable to resolve host plantedhost';} >$T/res.host
STUB_RES=$T/res.host hrun >$T/o 2>$T/e;rc=$?
ok host-name-the-summary-is-redacted-counted-and-the-files-are-named "$(grep 'host-name check' $T/hd/out/summary.txt|cut -c1-200)" '! grep -qi plantedhost $T/hd/out/summary.txt&&grep -q "<host>" $T/hd/out/summary.txt&&grep -q "^host-name check: [1-9][0-9]* line(s) in the raw files of OUT name this host (.*res" $T/hd/out/summary.txt&&grep -qi plantedhost $T/hd/out/res'
sed 's/|sed "s\/$rx\/<host>\/Ig" >"$OUT\/summary.txt"/ >"$OUT\/summary.txt"/' $SRC >$T/f1.noredact.sh;[ "$(cmp $SRC $T/f1.noredact.sh >/dev/null 2>&1;echo $?)" = 1 ]
rm -rf $T/hd $T/term $T/seen;mkdir -p $T/hd;: >$T/log;( cd $T;F1_DATA=$T/hd F1_REPO=$W2 F1_MEMINFO=$T/mi.ok F1_TIMEOUT=60 F1_CGROOT=$T/cg STUB_RES=$T/res.host sh $T/f1.noredact.sh run $SHA $T/answers0 $T/hd/out ) >$T/o 2>$T/e
ok host-name-mutant-without-the-redaction-leaves-the-host-name-in-summary-RED "planted in summary: $(grep -ci plantedhost $T/hd/out/summary.txt)" 'grep -qi plantedhost $T/hd/out/summary.txt'
rm -f $SH/hostname
rm -rf $T/hd $T/term $T/seen;mkdir -p $T/hd/out;echo old >$T/hd/out/res;: >$T/log;( cd $T;F1_DATA=$T/hd F1_REPO=$W2 F1_MEMINFO=$T/mi.ok F1_TIMEOUT=60 F1_CGROOT=$T/cg STUB_RES=$T/res.good11 sh $SRC run $SHA $T/answers0 $T/hd/out ) >$T/o 2>$T/e;rc=$?
ok out-mutant-a-non-empty-OUT-is-refused-and-its-bytes-are-untouched-RED "rc $rc; res: $(cat $T/hd/out/res); calls: $(grep -c '^mmdebstrap\|^nspawn' $T/log)" '[ $rc != 0 ]&&[ "$(cat $T/hd/out/res)" = old ]&&[ "$(grep -c "^mmdebstrap\|^nspawn" $T/log)" = 0 ]&&grep -q "is not empty" $T/e'
rm -rf $T/hd $T/term $T/seen;mkdir -p $T/hd/out;: >$T/log;( cd $T;F1_DATA=$T/hd F1_REPO=$W2 F1_MEMINFO=$T/mi.ok F1_TIMEOUT=60 F1_CGROOT=$T/cg STUB_RES=$T/res.good11 sh $SRC run $SHA $T/answers0 $T/hd/out ) >$T/o 2>$T/e;rc=$?
ok out-an-empty-existing-OUT-is-accepted "rc $rc" '[ $rc = 0 ]&&[ "$(stat -c %a $T/hd/out)" ]'
rm -rf $T/hd $T/term $T/seen;mkdir -p $T/hd;: >$T/log;( cd $T;F1_DATA=$T/hd F1_REPO=$W2 F1_MEMINFO=$T/mi.ok F1_TIMEOUT=60 F1_CGROOT=$T/cg STUB_RES=$T/res.good11 sh $SRC run $SHA $T/answers0 );rc=$?
ok out-the-default-OUT-dir-is-fresh-per-run-and-mode-700 "$(ls -d $T/hd/f1-nspawn-*.out|wc -l) out dir; mode $(stat -c %a $(ls -d $T/hd/f1-nspawn-*.out|head -1))" '[ "$(ls -d $T/hd/f1-nspawn-*.out|wc -l)" = 1 ]&&[ "$(stat -c %a $(ls -d $T/hd/f1-nspawn-*.out|head -1))" = 700 ]'
cp $T/mi.ok $T/mi.trip;MI=$T/mi.trip STUB_TRIP=1 STUB_RES=$T/res.good11 hrun >$T/o 2>$T/e;rc=$?
ok watchdog-host-MemAvailable-under-1G-terminates-the-container-and-is-INCONCLUSIVE-RED "rc $rc; $(cat $T/hd/out/host.mem.trip 2>/dev/null); terminate: $(grep -c '^machinectl terminate' $T/log)" '[ $rc = 2 ]&&grep -q "^host MemAvailable 488 MB < 1024 MB" $T/hd/out/host.mem.trip&&grep -q "^machinectl terminate" $T/log&&head -1 $T/o|grep -q "INCONCLUSIVE.*host memory watchdog"'
F1_PSIMEM=$T/psi.hot STUB_HANG=1 TO=3 STUB_RES=$T/res.good11 hrun >$T/o 2>$T/e;rc=$?
ok watchdog-host-memory-PSI-above-20-terminates-and-is-INCONCLUSIVE-RED "rc $rc; $(cat $T/hd/out/host.mem.trip 2>/dev/null)" '[ $rc = 2 ]&&grep -q "^host memory PSI some avg10 35.00 > 20" $T/hd/out/host.mem.trip&&[ ! -e $T/hd/out/timeout ]'
STUB_RES=$T/res.good11 hrun >$T/o 2>$T/e;rc=$?
ok watchdog-quiet-host-does-not-trip-it "rc $rc; trip file: $([ -e $T/hd/out/host.mem.trip ]&&echo YES||echo none)" '[ $rc = 0 ]&&[ ! -e $T/hd/out/host.mem.trip ]'
printf 'low 0\nhigh 0\nmax 313\noom 0\noom_kill 0\n' >$T/cg/machine.slice/x.scope/memory.events;STUB_RES=$T/res.good11 hrun >$T/o 2>$T/e;rc=$?
ok memory-max-313-with-no-oom-is-PASS-and-the-raw-events-are-in-the-summary "rc $rc; $(head -1 $T/o|cut -c1-60)" '[ $rc = 0 ]&&head -1 $T/o|grep -q "F1 OUTCOME: PASS"&&grep -q "^max 313" $T/hd/out/summary.txt&&grep -q "max > 0 ALONE is INFO" $T/hd/out/summary.txt'
printf 'low 0\nhigh 0\nmax 0\noom 0\noom_kill 0\n' >$T/cg/machine.slice/x.scope/memory.events
ok stub-the-claude-stub-reads-its-mail-every-30-s-not-5 "grep for the loop" 'grep -qF "sleep 30;done)&" $SRC&&! grep -qF "sleep 5;done)&" $SRC'
ok stub-argv-log-is-one-file-per-user-run-2-logged-only-the-first-user-because-the-file-was-644 "grep" 'grep -qF "argv.\$(id -un).log" $SRC&&! grep -qF "claude/argv.log" $SRC'
sh -n $SRC;ok syntax "sh -n" '[ $? = 0 ]'
echo "f1-nspawn.t.sh: $f FAIL"
exit $f
