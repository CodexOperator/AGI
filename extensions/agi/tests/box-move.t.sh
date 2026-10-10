#!/bin/sh
# box-move.t.sh: goal:g1.42 row 14 -- the host-act move's exit must stop box-move.sh's remote step (a failed move never starts the post).
# It extracts the REAL `$E "cd /data/work/agi ..."` line of guard/box-move.sh, points the cd at a scratch repo, and runs it with STUBS on PATH:
# sudo (drops -n), systemctl (logs its argv; is-active = inactive), a host-act that exits HOSTACT_RC, a scratch repo whose carry/trunk is ahead (ff) or diverged.
# SRC = the script under test (default guard/box-move.sh of ROOT); a mutation = SRC=<edited copy>. One ok/FAIL line per case; exit = FAIL count.
T=$(mktemp -d);trap 'rm -rf $T' 0;f=0;R0=${ROOT:-$(cd "$(dirname "$0")/../../.." && pwd)};SRC=${SRC:-$R0/extensions/agi/guard/box-move.sh}
ok(){ if eval "$2";then echo "ok $1";else echo "FAIL $1";f=$((f+1));fi;}
export GIT_AUTHOR_NAME=t GIT_AUTHOR_EMAIL=t@t GIT_COMMITTER_NAME=t GIT_COMMITTER_EMAIL=t@t GIT_CONFIG_GLOBAL=/dev/null GIT_CONFIG_SYSTEM=/dev/null
P=post1;TO=encryption-town;W=$T/w;B=$T/bin;mkdir -p $B $W/extensions/agi/guard
printf '#!/bin/sh\nwhile [ "$1" = -n ];do shift;done\nexec "$@"\n' >$B/sudo
printf '#!/bin/sh\necho "$*" >>%s/ctl.log\ncase "$1" in is-active)exit 1;; show)echo "running 0";; esac\nexit 0\n' $T >$B/systemctl
printf '#!/bin/sh\nexec sh -c "$1"\n' >$B/ssh-stub;chmod +x $B/*
printf 'echo move line one\necho move line two\necho move line three\nexit ${HOSTACT_RC:-0}\n' >$W/extensions/agi/guard/host-act-$TO.sh
(cd $W&&git init -q -b main .&&git add .&&git commit -q -m base&&git tag base&&git branch carry/trunk&&git checkout -q carry/trunk&&echo x>x&&git add x&&git commit -q -m ahead&&git checkout -q main)
line(){ grep -F '$E "cd /data/work/agi' "$1"|sed "s#/data/work/agi#$W#;s#;;\$##";}
# drive FILE RC: run the extracted remote command in the scratch repo; sets rc, and out/err/ctl.log
drive(){ : >$T/ctl.log;(cd $W&&git checkout -q -f main&&git reset -q --hard base;E=$B/ssh-stub;eval "$(line "$1")") >$T/out 2>$T/err;rc=$?; }
line $SRC >/dev/null;[ -n "$(line $SRC)" ]||{ echo "FAIL extract: no remote line in $SRC";exit 99;}
PATH=$B:$PATH;export PATH
HOSTACT_RC=0;export HOSTACT_RC;drive $SRC;ok "move-ok-starts-the-post a host act that exits 0 ends rc 0 and starts agi-post@$P (rc $rc; ctl: $(tr '\n' '|' <$T/ctl.log))" '[ $rc = 0 ]&&grep -q "^start agi-post@$P" $T/ctl.log'
HOSTACT_RC=3;export HOSTACT_RC;drive $SRC
ok "move-fail-stops-rc-carried a host act that exits 3 ends rc 3 (got $rc), not 0" '[ $rc = 3 ]'
ok "move-fail-never-starts-the-post and agi-post@$P is NOT started, enabled or reset after it (ctl: $(tr '\n' '|' <$T/ctl.log))" '! grep -q -E "start agi-post|enable|reset-failed" $T/ctl.log'
ok "move-fail-says-so the failure names the rc on stderr ($(tr '\n' ' ' <$T/err))" 'grep -q "host-act move failed rc=3" $T/err'
ok "move-fail-still-shows-the-act-tail the last 2 lines of the act's output are still printed" 'grep -q "move line two" $T/out&&grep -q "move line three" $T/out&&! grep -q "move line one" $T/out'
HOSTACT_RC=0;export HOSTACT_RC;(cd $W&&git checkout -q -f main&&git reset -q --hard base&&echo y>y&&git add y&&git commit -q -m diverge)
: >$T/ctl.log;(cd $W&&E=$B/ssh-stub;eval "$(line $SRC)") >$T/out 2>$T/err;rc=$?
ok "merge-fail-stops a carry/trunk that is not a fast-forward ends nonzero (rc $rc) and starts nothing (ctl: $(tr '\n' '|' <$T/ctl.log))" '[ $rc != 0 ]&&! grep -q "start agi-post" $T/ctl.log'
# the witness: the PRE-FIX line (the act piped through tail -2, then `;`) with the same stubs -- the failed act still starts the post, so the rows above can fail
cat >$T/old.sh <<'OLD'
$E "cd /data/work/agi&&git merge -q --ff-only carry/trunk&&sudo -n env PIN=\$(git rev-parse HEAD) sh extensions/agi/guard/host-act-$TO.sh move $P 2>&1|tail -2;sudo -n test -f /run/systemd/system/agi-post@$P.service.d/h.conf&&sudo -n systemctl enable --now agi-carry@$P.path&&sudo -n systemctl reset-failed agi-post@$P 2>/dev/null;sudo -n systemctl is-active -q agi-post@$P||sudo -n systemctl start agi-post@$P;systemctl show agi-post@$P -p SubState -p NRestarts --value|tr '\n' ' '";;
OLD
HOSTACT_RC=3;export HOSTACT_RC;drive $T/old.sh
ok "witness-old-line the pre-fix line with a failing act ends rc $rc (want 0) and DOES start the post (ctl: $(tr '\n' '|' <$T/ctl.log))" '[ $rc = 0 ]&&grep -q "^start agi-post@$P" $T/ctl.log'
echo "box-move: $f FAIL";exit $f
