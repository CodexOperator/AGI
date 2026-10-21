#!/bin/sh
# agi-town-start.t.sh: goal:g7.16.1.11.44.8 S2b (council 3/3 10-15 19:36Z + 10-16 09:20Z + 10-21 residues, 08:37Z word): agi.sh START on STUBS ONLY. systemctl (STATEFUL: enabled / active / masked in files), sudo, getent, gh, visudo, box and crons.py are shims; the host is a ROOT=<scratch> rehearsal of the REAL `agi.sh host`;
# MAIN is a scratch git repo holding the real geometry (engine*.md: the real matrix row), the real config and a fixture posts.md. NEVER the live town: no root, no systemd, no network, 0 USD.
# One ok/FAIL line per case; exit = number of FAILs. Every MUTANT is one edit on the code under test (pm) or on the fixture, and its row passes only when the clean property BREAKS.
T=$(mktemp -d);trap 'rm -rf $T' 0;f=0;R0=${ROOT_TREE:-$(cd "$(dirname "$0")/../../.." && pwd)};G=/usr/bin/git;GEO=$R0/.agi/nodes/.geometry
ok(){ if eval "$3";then echo "ok $1 $2";else echo "FAIL $1 $2";f=$((f+1));for x in $T/o $T/e;do [ -s $x ]&&head -5 $x|cut -c1-240|sed "s/^/#   ${x##*/}: /";done;fi;}
SRC=$R0/extensions/agi/bin/agi.sh;[ -f $SRC ]||{ echo "FAIL inputs: $SRC";exit 99;}
mkdir -p $T/bin $T/mut;cp $SRC $T/bin/agi.sh;AG=$T/bin/agi.sh;AGSH=
# a fake crons.py beside every copy of agi.sh (its own lane tests crons.py): show / apply / apply --sudo / marked / remove keep a count in $SD/cronn and log every call
for d in $T/bin $T/mut;do cat >$d/crons.py <<'EOF'
import os,sys
sd=os.environ["STUB_SD"];a=sys.argv[1:]
open(sd+"/crons.calls","a").write(" ".join(a)+"\n")
n=int(open(sd+"/cronn").read()) if os.path.exists(sd+"/cronn") else 0
if a[0]=="show": print("status: up to date" if n else "status: DRIFT")
elif a[0]=="apply": open(sd+"/cronn","w").write("3")
elif a[0]=="marked": print(n if "--foreign" not in a else "",end="\n" if "--foreign" not in a else "")
elif a[0]=="remove": open(sd+"/cronn","w").write("0")
EOF
done
sect(){ cat $GEO/engine*.md|sed -n "/^###* $1 /,/^###* /{/^~~~/,/^~~~/{//!p}}";}
# --- shims
SH=$T/shim;SD=$T/sd;mkdir -p $SH $SD $T/home $T/wants $T/sudoers.d $T/sudol
cat >$SH/id <<'EOF'
#!/bin/sh
case $1 in -u)echo ${STUB_IDU:-0};; *)exec /usr/bin/id "$@";;esac
EOF
cat >$SH/getent <<'EOF'
#!/bin/sh
if [ "$1" = passwd ];then if [ $# = 1 ];then cat $STUB_SD/passwd;exit 0;fi;grep "^$2:" $STUB_SD/passwd;exit $?;fi;exec /usr/bin/getent "$@"
EOF
cat >$SH/systemctl <<'EOF'
#!/bin/sh
# a STATEFUL stub: $STUB_SD/active, enabled, masked (unit per line). STUB_ENABLE_NOOP=U,U makes `enable U` succeed WITHOUT enabling it. Every call is logged with the town.state / flag-file facts at that moment.
a=$STUB_SD/active;e=$STUB_SD/enabled;m=$STUB_SD/masked;touch $a $e $m
echo "$* state=$([ -s "$STUB_STATE" ]&&echo yes||echo no) flags=$(ls $STUB_HOMES/*/.claude.json 2>/dev/null|wc -l|tr -d ' ')" >>$STUB_SD/calls
q=;[ "$2" = -q ]&&{ q=1;set -- $1 $3;}
# STUB_SIGTERM=p: a post that rewrites its in-memory ~/.claude.json copy on SIGTERM (stop / restart while up) - Claude Code's write-back on exit
case $1 in stop|restart)[ -n "$STUB_SIGTERM" ]&&[ "$2" = "agi-post@$STUB_SIGTERM.service" ]&&grep -qx "$2" $a&&echo '{"stale":true}' >$STUB_HOMES/$STUB_SIGTERM/.claude.json;; esac
# STUB_START_FAIL=U,U: `start U` exits 1; STUB_START_NOOP=U,U: it exits 0 but U does not come up
case $1 in start)case ",$STUB_START_FAIL," in *,$2,*)exit 1;; esac;case ",$STUB_START_NOOP," in *,$2,*)exit 0;; esac;; esac
case $1 in
list-units)st=active;for x in "$@";do case $x in --state=*)st=${x#--state=};;esac;done
 case ",$st," in *,active,*)awk '{print $1" loaded active running stub"}' $a;;esac;;
is-active)if grep -qx "$2" $a;then [ -n "$q" ]||echo active;else [ -n "$q" ]||echo inactive;exit 3;fi;;
is-enabled)if grep -qx "$2" $m;then echo masked;exit 1;fi;if grep -qx "$2" $e;then echo enabled;exit 0;fi;echo disabled;exit 1;;
enable)shift;[ "$1" = --now ]&&{ shift;echo "$1">>$a;};case ",$STUB_ENABLE_NOOP," in *,$1,*)exit 0;;esac;grep -qx "$1" $e||echo "$1">>$e;;
disable)grep -vxF "$2" $e>$e.n;mv $e.n $e;;
stop)grep -vxF "$2" $a>$a.n;mv $a.n $a;;
show)case "$*" in *TriggeredBy*)awk -v u="$2" '$1==u{print $2}' $STUB_SD/triggers 2>/dev/null;;
  *-p\ Type*)grep -qx "$2" $STUB_SD/oneshots 2>/dev/null&&echo oneshot||echo simple;;
  *RemainAfterExit*)grep -qx "$2" $STUB_SD/remain 2>/dev/null&&echo yes||echo no;; esac;;
start|restart)grep -qx "$2" $a||echo "$2">>$a;case $2 in agi-boot.service)for p in $(cat $STUB_SD/bootposts 2>/dev/null);do grep -qx "agi-post@$p.service" $a||echo "agi-post@$p.service">>$a;done;;esac;;
*)exit 0;;esac
EOF
printf '#!/bin/sh\necho "$*">>$STUB_SD/analyze.calls\nexit 0\n' >$SH/systemd-analyze
cat >$SH/sudo <<'EOF'
#!/bin/sh
# -n -H -u USER cmd...  |  -l -U USER (prints the fixture grants of USER)
while [ "$1" = -n ]||[ "$1" = -H ];do shift;done
if [ "$1" = -l ];then shift;[ "$1" = -U ]&&{ [ -f $STUB_SOL/$2 ]&&cat $STUB_SOL/$2||echo "User $2 is not allowed to run sudo on stub.";exit 0;};fi
if [ "$1" = -u ];then export STUB_AS=$2;shift 2;fi
exec "$@"
EOF
cat >$SH/gh <<'EOF'
#!/bin/sh
exit ${STUB_GH_RC:-0}
EOF
cat >$SH/visudo <<'EOF'
#!/bin/sh
[ "$1" = -cf ]||exit 2;grep -q BAD "$2"&&{ echo "visudo stub: syntax error" >&2;exit 1;};exit 0
EOF
cat >$SH/box <<'EOF'
#!/bin/sh
# town up|down SHA: one commit per post of the box on refs/box/belam/<p> (the message is the town line), refs/held/<p>/belam the same commit (the post read it); every call logged
[ "$1" = town ]||exit 2;echo "$*" >>$STUB_SD/box.calls;v=$2;sha=$3
for p in $(git show $AGI_TRUNK:.agi/nodes/.geometry/posts.md 2>/dev/null|sed -n 's/^  - {/{/p'|jq -r --arg x "$AGI_BOX" 'select(has("harness") and .box==$x)|.name');do
 c=$(git -c user.name=belam -c user.email=belam@agi commit-tree -m "[town] $v $sha" $(git rev-parse HEAD^{tree}) -p HEAD);git update-ref refs/box/belam/$p $c;git update-ref refs/held/$p/belam $c;done
EOF
printf '#!/bin/sh\nexit 0\n' >$SH/crontab;for t in strace script claude pi python3x;do :;done;for t in strace script claude;do printf '#!/bin/sh\nexit 0\n' >$SH/$t;done;chmod +x $SH/*;cp $SH/box $T/box
# --- the world: MAIN (HEAD = PIN) inside a ROOT scratch, three posts p1 p2 p3 on box tw (+ far on box xx), homes under $T/h, the passwd, the host act already run
PUSER=$(id -un);X=$T/root;M=$X/data/work/agi;PM=/data/work/agi
posts(){ printf '%s\n' '---' 'posts:';for p in p1 p2 p3;do printf '  - {"name":"%s","parent":"belam","harness":"claude","box":"tw","boot":%s,"engine":{"v":4,"name":"%s","harness":"claude","model":"m","effort":"low"}}\n' $p $([ $p = p3 ]&&echo false||echo true) $p;done
 printf '  - {"name":"far","parent":"belam","harness":"claude","box":"xx","engine":{"v":4,"name":"far","harness":"claude","model":"m","effort":"low"}}\n';printf '%s\n' '---';}
world(){ AGSH=;rm -rf $X $T/h $SD/* $T/state $T/state.* $T/starting $T/env $T/sudoers.d/* $T/sudol/*;mkdir -p $M/.agi/nodes/.geometry $X/opt/agi/bin $X/etc/systemd/system $X/etc/polkit-1/rules.d $X/usr/local $X/mnt $X/var/lib $T/h/belam
 cp $GEO/engine*.md $M/.agi/nodes/.geometry/;posts >$M/.agi/nodes/.geometry/posts.md;cp $R0/.agi/config.json $M/.agi/config.json;mkdir -p $M/.agi/comms/season-2/dm;echo x>$M/.agi/comms/season-2/dm/a--b.md
 $G init -q -b fx/trunk $M;$G -C $M add -A;$G -C $M -c user.name=t -c user.email=t@t -c commit.gpgsign=false commit -qm fx;PIN=$($G -C $M rev-parse HEAD)
 printf '#!/bin/sh\n' >$X/opt/agi/bin/pi;chmod +x $X/opt/agi/bin/pi
 { printf 'agi-belam:x:2:2::%s:/bin/sh\n' $T/h/belam;for p in p1 p2 p3;do mkdir -p $T/h/$p;printf 'agi-%s:x:1%s:1%s::%s:/bin/sh\n' $p ${p#p} ${p#p} $T/h/$p;done;} >$SD/passwd;: >$SD/active;: >$SD/enabled;printf 'p1\np2\n' >$SD/bootposts
 printf '[user]\n\tname=belam\n[credential "https://github.com"]\n\thelper = \n\thelper = !sudo -n -u %s /usr/bin/gh auth git-credential\n' $PUSER >$T/h/belam/.gitconfig
 jq -r '.values.local_maxxing.agi_town.sudoers_line' $M/.agi/config.json >$T/sudoers.d/90-agi-belam;chmod 440 $T/sudoers.d/90-agi-belam
 echo '0.10 0.10 0.10 1/1 1' >$T/loadavg;echo 'some avg10=0.00 avg60=0.10 avg300=0.00 total=0' >$T/psi
 printf '#!/bin/sh\nexit 0\n' >$T/guard-init.sh
 : >$SD/calls;rm -f $T/rcs;}
# hact: the ROOT=<scratch> rehearsal of the real host act (the live tail on the stub systemctl, so agi-boot is enabled and the stopped-town rules are live)
hact(){ env -i PATH=$SH:/usr/bin:/bin HOME=$T/home ROOT=$X PIN=$PIN AGI_REPO=$PM AGI_BOX=tw PRIME_USER=$PUSER SKIP_PREREQ=1 AGI_HOST_UNITS=$SH AGI_TOWN_STATE=$T/state AGI_TOWN_STARTING=$T/starting STUB_SD=$SD STUB_STATE=$T/state STUB_HOMES=$T/h sh ${AGSH:-$AG} host;}
# st [VAR=val ...]: agi.sh start on the stubs (the host check is live through AGI_HOST_UNITS)
st(){ echo '== start' >>$SD/calls;env -i PATH=${SPATH:-$SH:/usr/bin:/bin} HOME=$T/home ROOT=$X AGI_MAIN=$M AGI_BOX=tw PIN=$PIN PRIME_USER=$PUSER AGI_HOST_UNITS=$SH AGI_TOWN_ENV=$T/env AGI_TOWN_STATE=$T/state AGI_TOWN_STARTING=$T/starting AGI_CARRY_ENV=$X/etc/agi/carry.env AGI_WANTS_DIR=$T/wants \
 AGI_TOWN_BOXBIN=$T/box AGI_SUDOERS=$T/sudoers.d/90-agi-belam AGI_SYSGITCONFIG=$T/gitconfig.sys AGI_GUARD_INIT=$T/guard-init.sh AGI_LOADAVG=$T/loadavg AGI_PSI_IO=$T/psi AGI_ORIGIN=$T/origin.git STUB_SD=$SD STUB_STATE=$T/state STUB_HOMES=$T/h STUB_SOL=$T/sudol "$@" sh ${AGSH:-$AG} ${CMD:-start};}
# stp: agi.sh stop on the same stubs (root check by the id stub)
stp(){ CMD=stop st "$@";}
login(){ for p in p1 p2 p3;do mkdir -p $T/h/$p/.claude;echo '{}' >$T/h/$p/.claude/.credentials.json;done;}
up3(){ printf '%s\n' agi-post@p1.service agi-post@p2.service agi-post@p3.service agi-boot.service agi-quiet-watch.timer >$SD/active;printf '%s\n' agi-boot.service agi-quiet-watch.timer >$SD/enabled;}
snapd(){ { $G -C $M for-each-ref|md5sum;(cd $X/etc&&tar -c agi 2>/dev/null|md5sum);sort $SD/active|md5sum;sort $SD/enabled|md5sum;} 2>/dev/null|tr '\n' ' ';}
pm(){ MUT=$T/mut/agi.sh A="$1" B="$2" AGF=${PMBASE:-$AG} python3 -c "
import os,sys
s=open(os.environ['AGF']).read();a=os.environ['A']
if s.count(a)<1: print('# NO EDIT for ['+a[:60]+']');sys.exit(0)
open(os.environ['MUT'],'w').write(s.replace(a,os.environ['B']))";cmp -s $AG $T/mut/agi.sh 2>/dev/null&&echo "# NO EDIT (identical) for [$1]";AGSH=$T/mut/agi.sh;}
calls(){ awk -v re="$1" '/^== start/{c=0;next} $0 ~ re{c++} END{print c+0}' $SD/calls;}
firstflags(){ sed -n '/^== start/,$p' $SD/calls|grep -m1 "^enable agi-boot.service"|sed -n 's/.* flags=\([0-9]*\)$/\1/p';}

# ===== the table, the arms, the inputs =====
ROWN=$(sect matrix|awk -F'\t' '$1=="town"&&$2=="start"{print $3}');TBL=$(grep '^steps(){' $SRC|grep -o "'S[0-9] [a-z]*'"|tr -d "'"|awk '{print $2}'|sort -u|grep -vx pre|tr '\n' ' ')
ok st2-cond6-one-table-every-step-names-a-row-name "the row [$ROWN] vs the table's names [$TBL]" '[ "$(echo $ROWN|tr " " "\n"|sort|tr "\n" " ")" = "$TBL" ]'
arms=1;for n in $ROWN;do for k in sk_ su_ ck_ dn_;do grep -q "^$k$n()" $SRC||arms=0;done;done
ok st2-cond6-every-row-name-has-an-up-arm-a-check-and-a-down-arm "sk_ su_ ck_ dn_ for each of: $ROWN" '[ $arms = 1 ]'
world;CMD=start;st AGI_BOX= PIN= >$T/o 2>$T/e;rc=$?
ok st2-S1-no-box-is-one-ask-rc-20 "start with no AGI_BOX: rc $rc (want 20), [ask] lines: $(grep -c '^\[ask\] AGI_BOX' $T/o)" '[ $rc = 20 ]&&[ "$(grep -c "^\[ask\]" $T/o)" = 1 ]&&grep -q "^\[ask\] AGI_BOX:" $T/o'
world;st PIN= >$T/o 2>$T/e;rc=$?
ok st2-S1-no-pin-is-one-ask-rc-20 "start with a box and no pin: rc $rc, asks: $(grep -c '^\[ask\] PIN' $T/o) (the tip is shown as 40 hex: $(grep -c '[0-9a-f]\{40\}' $T/o))" '[ $rc = 20 ]&&[ "$(grep -c "^\[ask\]" $T/o)" = 1 ]&&grep -q "^\[ask\] PIN:.*[0-9a-f]\{40\}" $T/o'
world;st PIN=zz >$T/o 2>$T/e;rc=$?
ok st2-S1-a-bad-pin-is-refused-by-name "pin zz: rc $rc, [pin] named, nothing started: $(calls '^(start|enable|restart)')" '[ $rc != 0 ]&&grep -q "^\[pin\]" $T/e&&[ "$(calls "^(start|enable|restart)")" = 0 ]'
# S0
world;mkdir -p $T/nostrace;for ff in /usr/bin/* /bin/*;do b=${ff##*/};[ "$b" = strace ]||[ -e $T/nostrace/$b ]||ln -s $ff $T/nostrace/$b;done
mkdir -p $T/shim2;cp $SH/* $T/shim2/;rm -f $T/shim2/strace;SPATH=$T/shim2:$T/nostrace st AGI_HOST_UNITS=$T/shim2 >$T/o 2>$T/e;rc=$?;SPATH=
ok st2-S0-a-missing-dep-is-owner-do-rc-21-with-the-apt-line "no strace on PATH: rc $rc, line: $(grep '^\[owner-do\]' $T/o|head -1)" '[ $rc = 21 ]&&grep -qx "\[owner-do\] sudo apt-get install -y strace" $T/o'
world;mkdir -p $M/bin;echo x>$M/bin/render-context.py;st >$T/o 2>$T/e;rc=$?
ok st2-S0-a-main-bin-py-is-refused "MAIN/bin/*.py: rc $rc, [shadow] named" '[ $rc != 0 ]&&grep -q "^\[shadow\]" $T/e'
world;printf '#!/bin/sh\nexit 1\n' >$T/guard-init.sh;st >$T/o 2>$T/e;rc=$?
ok st2-S0-a-degraded-guard-is-owner-do-never-run "guard-init --status exits 1: rc $rc, line: $(grep '^\[owner-do\]' $T/o|head -1|cut -c1-90)" '[ $rc = 21 ]&&grep -q "^\[owner-do\] sudo sh .*guard-init.sh apply" $T/o'

# ===== a fresh box: host act done, nothing else =====
world;hact >$T/h.out 2>&1;ref0=$($G -C $M for-each-ref refs/heads|md5sum)
st >$T/o 2>$T/e;rc=$?
ok st2-cond7-the-first-start-stops-at-S6-rc-21-after-S5-started-the-posts "rc $rc (want 21): [owner-do] lines $(grep -c '^\[owner-do\]' $T/o) (want 3, one per post), posts up $(grep -c 'agi-post@' $SD/active) (want 3)" '[ $rc = 21 ]&&[ "$(grep -c "^\[owner-do\].*box-move.sh url p" $T/o)" = 3 ]&&[ "$(grep -c "^agi-post@" $SD/active)" = 3 ]'
ok st2-cond7-town-starting-is-root-600-and-holds-a-UTC "$(cat $T/starting 2>/dev/null) mode $(stat -c %a $T/starting 2>/dev/null)" '[ -s $T/starting ]&&[ "$(stat -c %a $T/starting)" = 600 ]&&grep -qE "^[0-9]{4}-[0-9]{2}-[0-9]{2}T[0-9:]{8}Z$" $T/starting'
ok st2-F4a-every-flag-file-is-600-with-the-four-flags "$(ls $T/h/*/.claude.json|wc -l) .claude.json, $(ls $T/h/*/.claude/settings.json|wc -l) settings.json; modes: $(stat -c %a $T/h/p*/.claude.json $T/h/p*/.claude/settings.json|sort -u|tr '\n' ' ')" 'for p in p1 p2 p3;do h=$T/h/$p;[ "$(stat -c %a $h/.claude.json)" = 600 ]&&[ "$(stat -c %a $h/.claude/settings.json)" = 600 ]&&jq -e --arg m /data/work/agi ".hasCompletedOnboarding==true and .fullscreenUpsellSeenCount>=3 and .projects[\$m].hasTrustDialogAccepted==true" $h/.claude.json >/dev/null&&jq -e ".skipDangerousModePermissionPrompt==true and .tui==\"default\"" $h/.claude/settings.json >/dev/null||exit 1;done'
ok st2-2-the-fresh-box-start-brings-every-post-up-only-after-all-three-flag-files "first start/restart call of the run saw $(sed -n '/^== start/,$p' $SD/calls|grep -m1 -E '^(start|restart) '|sed 's/ state=.*flags=/ flags=/') (want flags=3)" '[ "$(sed -n "/^== start/,\$p" $SD/calls|grep -m1 -E "^(start|restart) "|sed "s/.* flags=//")" = 3 ]'
ok st2-B1-agi-boot-is-enabled-and-read-back-exactly "agi-boot enabled: $(grep -cx agi-boot.service $SD/enabled)" 'grep -qx agi-boot.service $SD/enabled'
ok st2-cond5-the-trunk-and-every-town-start-ref-are-unchanged "refs/heads before == after; town-start refs: $($G -C $M for-each-ref refs/heads/town-start|wc -l)" '[ "$($G -C $M for-each-ref refs/heads|md5sum)" = "$ref0" ]&&[ -z "$($G -C $M for-each-ref refs/heads/town-start)" ]'
ok st2-ring-no-ring-at-the-pin-is-ONE-line-and-says-unverified "$(grep -c '^\[ring\]' $T/o $T/e|tr '\n' ' ') [ring] lines: $(grep -h '^\[ring\]' $T/o $T/e|head -2)" '[ "$(cat $T/o $T/e|grep -c "^\[ring\]")" = 1 ]&&grep -qx "\[ring\] no ring at '$PIN': the old gate, nothing to verify" $T/o&&! grep -q "unread\|WARNING\|checked" $T/o $T/e'
ok st2-F4b-MAIN-has-no-local-signing-key "git config --local signing: $($G -C $M config --local --get-regexp signing|wc -l)" '[ -z "$($G -C $M config --local --get-regexp signing)" ]'
ok st2-F5-no-token-shaped-string-in-town-env-carry-env-or-main-git-config "count: $(cat $T/env $X/etc/agi/carry.env $M/.git/config 2>/dev/null|grep -cE 'gh[pousr]_[A-Za-z0-9]{20,}|[A-Za-z0-9_-]{41,}')" '[ "$(cat $T/env $X/etc/agi/carry.env $M/.git/config 2>/dev/null|grep -E "gh[pousr]_[A-Za-z0-9]{20,}|[A-Za-z0-9_-]{41,}"|wc -l)" = 0 ]'
# stop refuses while a start is in progress, and the town.state it would have read is byte-identical
printf 'boot enabled\nrunning p1\nstopped tw 2026-10-15T20:00:00Z\n' >$T/state;s0=$(md5sum <$T/state);stp >$T/o 2>$T/e;rc=$?
ok st2-cond7-stop-during-a-start-says-the-TRUE-line-and-keeps-town-state "rc $rc: $(grep -o '^\[start-in-progress\].*finish it with agi.sh start' $T/e|cut -c1-120)" '[ $rc != 0 ]&&grep -q "^\[start-in-progress\] a start is in progress since .*: finish it with agi.sh start" $T/e&&[ "$(md5sum <$T/state)" = "$s0" ]&&! grep -q "stale-state" $T/e'
rm -f $T/state
# the re-run resumes at S6: with the logins done it ends with no town.starting and the blast sent ONCE
login;st >$T/o 2>$T/e;rc=$?;s1=$(snapd);bc=$(wc -l <$SD/box.calls)
ok st2-cond7-the-re-run-resumes-at-S6-and-ends-clean "rc $rc, town.starting gone: $([ ! -e $T/starting ]&&echo yes||echo NO), box up sent: $bc" '[ $rc = 0 ]&&[ ! -e $T/starting ]&&[ "$bc" = 1 ]&&grep -qx "town up '$PIN'" $SD/box.calls'
ok st2-F3-crons-were-applied-once-with-and-without-sudo "$(tr '\n' '|' <$SD/crons.calls)" '[ "$(grep -c "^apply" $SD/crons.calls)" = 2 ]&&grep -q "^apply --sudo" $SD/crons.calls'
st >$T/o 2>$T/e;rc=$?
ok st2-cond4-F3-a-second-start-changes-nothing-and-sends-no-box-mail "rc $rc, box calls $(wc -l <$SD/box.calls) (want 1), snapshot same: $([ "$(snapd)" = "$s1" ]&&echo yes||echo NO), agi-boot calls: $(calls '^(enable|start|restart) agi-boot')" '[ $rc = 0 ]&&[ "$(wc -l <$SD/box.calls)" = 1 ]&&[ "$(snapd)" = "$s1" ]&&[ "$(calls "^(enable|start|restart) agi-boot")" = 0 ]'
# mutants of the above
world;hact >/dev/null 2>&1;login;st >/dev/null 2>&1;pm 'sent_all(){ for p' 'sent_all(){ return 1;for p';world;hact >/dev/null 2>&1;login;st >/dev/null 2>&1;AGSH=$T/mut/agi.sh st >/dev/null 2>&1;st AGSH=x >/dev/null 2>&1
mutsend=$(wc -l <$SD/box.calls)
ok st2-cond4-mutant-a-blast-that-never-reads-the-refs-sends-twice-RED "box up calls after two starts with the check dropped: $mutsend (want 2; the clean row wants 1)" '[ "$mutsend" -ge 2 ]'
# a stopped town whose posts never had their flags: the start enables agi-boot ONLY after the flag files exist (B1)
sw(){ world;hact >/dev/null 2>&1;login;printf 'boot enabled\nrunning p1\nrunning p2\nrunning p3\nstopped tw 2026-10-15T20:00:00Z\n' >$T/state;: >$SD/active;grep -vx agi-boot.service $SD/enabled>$SD/enabled.n;mv $SD/enabled.n $SD/enabled;}
sw;st >$T/o 2>$T/e;rc=$?
ok st2-B1-the-first-agi-boot-enable-of-a-start-comes-after-the-flag-files "rc $rc: the first enable agi-boot call saw $(firstflags) flag files (want 3)" '[ "$(firstflags)" = 3 ]'
sw;pm ' for p in $nf;do flags_do $p;done' ' bootok||systemctl enable agi-boot.service;for p in $nf;do flags_do $p;done';st >/dev/null 2>&1
ok st2-B1-mutant-agi-boot-enabled-before-the-flags-is-RED "the first enable agi-boot call saw $(firstflags) flag files (clean: 3)" '[ "$(firstflags)" != 3 ]'
world;hact >/dev/null 2>&1;login;pm 'chmod 600 "$f"' 'chmod 644 "$f"';st >/dev/null 2>&1
ok st2-F4a-mutant-a-flag-written-644-is-RED "flag modes with the chmod edited: $(stat -c %a $T/h/p1/.claude.json 2>/dev/null)" '[ "$(stat -c %a $T/h/p1/.claude.json)" != 600 ]'
ok st2-F4b-mutant-a-local-signing-key-is-seen "a planted local signingkey makes the detector fire" '$G -C $M config --local user.signingkey x;[ -n "$($G -C $M config --local --get-regexp signing)" ]'
$G -C $M config --local --unset user.signingkey
ok st2-F5-mutant-a-stored-token-is-seen "a planted token in town.env: the scan counts $(printf 'T=ghp_%s\n' abcdefghijklmnopqrstuvwxyz0123|grep -cE 'gh[pousr]_[A-Za-z0-9]{20,}')" '[ "$(printf "T=ghp_%s\n" abcdefghijklmnopqrstuvwxyz0123|grep -cE "gh[pousr]_[A-Za-z0-9]{20,}")" = 1 ]'

# ===== the host step: B2 / B3 =====
world;st >$T/o 2>$T/e;rc=$?;bk=$(ls -d $X/var/backups/agi-act-* 2>/dev/null|wc -l|tr -d ' ')
ok st2-B3-start-on-a-fresh-root-refuses-at-host-and-never-runs-the-act "rc $rc: $(grep -c 'host: not met; run agi.sh host' $T/e) line(s), backups $bk, carry.env $([ -e $X/etc/agi/carry.env ]&&echo written||echo absent)" '[ $rc = 1 ]&&grep -qx "host: not met; run agi.sh host" $T/e&&[ "$bk" = 0 ]&&[ ! -e $X/etc/agi/carry.env ]&&[ "$(calls "^(start|enable|restart)")" = 0 ]'
world;pm 'su_host(){ up_host check >/dev/null 2>&1||exit 1' 'su_host(){ up_host check >/dev/null 2>&1||{ up_host;exit 1;};';st >$T/o 2>$T/e;bk2=$(ls -d $X/var/backups/agi-act-* 2>/dev/null|wc -l|tr -d ' ')
ok st2-B3-mutant-start-running-the-act-on-not-met-grows-a-backup-RED "backups after the mutant start on a fresh root: $bk2 (the clean row: 0)" '[ "$bk2" -ge 1 ]'
world;pm 'sk_host(){ up_host check||return 1;creds_ok||return 1;sudo_note;}' 'sk_host(){ return 0;}';st >$T/o 2>$T/e;rc=$?
ok st2-B2-mutant-a-host-check-that-says-met-lets-start-past-host-RED "start with sk_host true on a fresh root: rc $rc (the clean row refuses with 1 and the host line)" '! grep -qx "host: not met; run agi.sh host" $T/e'
# a stopped town with agi-boot MASKED: start must refuse at host (R-c on a stopped town)
world;hact >/dev/null 2>&1;printf 'boot enabled\nrunning p1\nstopped tw 2026-10-15T20:00:00Z\n' >$T/state;echo agi-boot.service>$SD/masked;grep -vx agi-boot.service $SD/enabled>$SD/enabled.n;mv $SD/enabled.n $SD/enabled;st >$T/o 2>$T/e;rc=$?
ok st2-Rc-stub-masked-on-a-stopped-town-makes-start-refuse-at-host "rc $rc: $(grep -c 'host: not met' $T/e)" '[ $rc = 1 ]&&grep -qx "host: not met; run agi.sh host" $T/e'
pm '[ "$o" = disabled ]||return 1;fi' '[ -n "$o" ]||return 1;fi';st >$T/o 2>$T/e;rc=$?
ok st2-Rc-mutant-unitsmet-accepting-any-word-while-stopped-is-RED "masked accepted: start got past host: $(grep -c 'host: not met' $T/e) refusals (clean: 1)" '! grep -qx "host: not met; run agi.sh host" $T/e'
# a start IN PROGRESS (town.starting exists) has begun enabling: either exact word is met, masked still is not
world;hact >/dev/null 2>&1;printf 'boot enabled\nrunning p1\nstopped tw 2026-10-15T20:00:00Z\n' >$T/state;date -u +%Y-%m-%dT%H:%M:%SZ >$T/starting;st >$T/o 2>$T/e;rc=$?
ok st2-Rc-a-start-in-progress-accepts-agi-boot-enabled-at-host "stopped + town.starting + agi-boot enabled: start got past host: $(grep -c 'start: host met' $T/o)" 'grep -q "^start: host met" $T/o'
echo agi-boot.service>$SD/masked;grep -vx agi-boot.service $SD/enabled>$SD/enabled.n;mv $SD/enabled.n $SD/enabled;st >$T/o 2>$T/e;rc=$?
ok st2-Rc-a-start-in-progress-with-agi-boot-masked-is-still-refused "rc $rc" '[ $rc = 1 ]&&grep -qx "host: not met; run agi.sh host" $T/e'
# ringcheck (council 10-21 Q=1): reads the ring row at the pin against each post's own key, writes NO commit, lists every difference and every unreadable read
ringworld(){ world;for p in p1 p2;do mkdir -p $T/h/$p/.ssh;ssh-keygen -q -t ed25519 -N '' -f $T/h/$p/.ssh/id_ed25519;done
 { echo "p1 ssh-ed25519 $(cut -d' ' -f2 $T/h/p1/.ssh/id_ed25519.pub)";echo "p2 ssh-ed25519 AAAAWRONGKEY";} >$M/.agi/nodes/.geometry/ring;$G -C $M add -A;$G -C $M -c user.name=t -c user.email=t@t -c commit.gpgsign=false commit -qm ring;PIN=$($G -C $M rev-parse HEAD);hact >/dev/null 2>&1;login;}
ringworld;ref0=$($G -C $M for-each-ref refs/heads|md5sum);st >$T/o 2>$T/e;rc=$?
ok st2-ring-a-matching-key-is-silent-a-differing-key-is-listed-an-unreadable-one-too "$(grep '^\[ring\]' $T/o $T/e|sed 's/^[^:]*://'|tr '\n' '|')" 'grep -q "^\[ring\] checked 2 of 3 posts" $T/o&&grep -qx "\[ring\] p2: key differs" $T/e&&grep -q "^\[ring\] p3: unread (no readable key file" $T/e&&! grep -q "^\[ring\] p1" $T/e&&[ $rc = 0 ]&&[ "$($G -C $M for-each-ref refs/heads|md5sum)" = "$ref0" ]'
ringworld;pm 'echo "[ring] $p: key differs" >&2' ':';st >$T/o 2>$T/e
ok st2-ring-mutant-a-differing-key-with-no-line-is-RED "p2 differs and nothing was said: $(grep -c 'p2: key differs' $T/e) line(s) (clean: 1)" '! grep -q "p2: key differs" $T/e'
# S4 helper absent: agi.sh writes the two lines (an empty helper first) to agi-belam's own global config, once
world;hact >/dev/null 2>&1;login;printf '[user]\n\tname=belam\n' >$T/h/belam/.gitconfig;st >$T/o 2>$T/e;rc=$?;st >$T/o2 2>$T/e2
ok st2-F5-helper-absent-is-written-once-in-belams-order "rc $rc: [$(tail -3 $T/h/belam/.gitconfig|tr '\n\t' '| ')], sections: $(grep -c 'credential "https://github.com"' $T/h/belam/.gitconfig)" '[ "$(grep -c git-credential $T/h/belam/.gitconfig)" = 1 ]&&[ "$(grep -c "credential \"https://github.com\"" $T/h/belam/.gitconfig)" = 1 ]&&[ "$(sed -n "/credential/{n;p}" $T/h/belam/.gitconfig|od -c|head -1|tr -d " ")" = "$(printf "\thelper = \n"|od -c|head -1|tr -d " ")" ]'
# F5 credentials
world;hact >/dev/null 2>&1;login;rm -f $T/sudoers.d/90-agi-belam;st >$T/o 2>$T/e;rc=$?
ok st2-F5-sudoers-absent-writes-ONLY-the-narrow-line-0440 "rc $rc, file: [$(cat $T/sudoers.d/90-agi-belam 2>/dev/null)] mode $(stat -c %a $T/sudoers.d/90-agi-belam 2>/dev/null)" '[ "$(cat $T/sudoers.d/90-agi-belam)" = "agi-belam ALL=('$PUSER') NOPASSWD: /usr/bin/gh auth git-credential" ]&&[ "$(stat -c %a $T/sudoers.d/90-agi-belam)" = 440 ]&&! grep -q "ALL$" $T/sudoers.d/90-agi-belam&&[ "$(ls $T/sudoers.d|wc -l|tr -d " ")" = 1 ]'
world;hact >/dev/null 2>&1;login;rm -f $T/sudoers.d/90-agi-belam;pm "narrow(){ printf 'agi-belam ALL=(%s) NOPASSWD: /usr/bin/gh auth git-credential' \"\$PU\";}" "narrow(){ printf 'agi-belam ALL=(ALL) NOPASSWD: ALL';}";st >$T/o 2>$T/e
ok st2-F5-mutant-a-written-line-containing-ALL-is-RED "the mutant wrote: [$(cat $T/sudoers.d/90-agi-belam 2>/dev/null)]" 'grep -q "ALL$" $T/sudoers.d/90-agi-belam'
world;hact >/dev/null 2>&1;login;rm -f $T/sudoers.d/90-agi-belam;d0=$(ls -la $T/sudoers.d|md5sum);pm "printf 'agi-belam ALL=(%s) NOPASSWD: /usr/bin/gh auth git-credential' \"\$PU\"" "printf 'BAD'";st >$T/o 2>$T/e;rc=$?
ok st2-cond3-a-malformed-line-is-refused-and-the-sudoers-dir-is-byte-identical "visudo shim refused: rc $rc, dir listing same: $([ "$(ls -la $T/sudoers.d|md5sum)" = "$d0" ]&&echo yes||echo NO), line: $(grep -o '\[sudoers\] visudo refused[^:]*' $T/e)" '[ $rc != 0 ]&&grep -q "^\[sudoers\] visudo refused" $T/e&&[ "$(ls -la $T/sudoers.d|md5sum)" = "$d0" ]'
world;hact >/dev/null 2>&1;login;st >$T/o 2>$T/e;rc=$?
ok st2-F5-a-present-broad-line-byte-equal-to-the-cell-passes-with-the-BROAD-notice "rc $rc: $(grep -c 'BROAD grant (ALL), owner ruling pending' $T/o) notice(s); file untouched: $(cat $T/sudoers.d/90-agi-belam)" '[ $rc = 0 ]&&grep -qx "\[sudoers\] present, byte-equal to the cell; BROAD grant (ALL), owner ruling pending" $T/o'
world;hact >/dev/null 2>&1;login;rm -f $T/sudoers.d/90-agi-belam;echo 'agi-belam ALL=(ALL) NOPASSWD: /bin/true' >$T/sudoers.d/90-agi-belam;h0=$(md5sum <$T/sudoers.d/90-agi-belam);st >$T/o 2>$T/e;rc=$?
ok st2-F5-a-present-line-that-differs-from-the-cell-is-refused-and-untouched "rc $rc: $(grep -o '\[sudoers\][^:]*differs[^:]*' $T/e|head -1|cut -c1-80)" '[ $rc != 0 ]&&grep -q "^\[sudoers\].*differs" $T/e&&[ "$(md5sum <$T/sudoers.d/90-agi-belam)" = "$h0" ]'
world;hact >/dev/null 2>&1;login;echo 'agi-p2 ALL=('$PUSER') NOPASSWD: ALL' >$T/sudol/agi-p2;sed -i 's/^/    /' $T/sudol/agi-p2;st >$T/o 2>$T/e;rc=$?
ok st2-F5-another-uid-with-a-grant-that-runs-as-belam-is-refused "agi-p2 holds (belam): rc $rc: $(grep -o '\[sudoers\] agi-p2[^:]*' $T/e|cut -c1-70)" '[ $rc != 0 ]&&grep -q "^\[sudoers\] agi-p2 holds a sudo grant" $T/e'
world;hact >/dev/null 2>&1;login;printf '[credential "https://github.com"]\n\thelper = !x git-credential\n' >$T/h/p3/.gitconfig;st >$T/o 2>$T/e;rc=$?
ok st2-F5-a-second-global-config-with-the-helper-is-refused "p3 has a git-credential helper too: rc $rc: $(grep -o '\[creds\][^;]*' $T/e|head -1|cut -c1-90)" '[ $rc != 0 ]&&grep -q "^\[creds\]" $T/e'
world;hact >/dev/null 2>&1;login;st STUB_GH_RC=1 >$T/o 2>$T/e;rc=$?
ok st2-S4-a-gh-that-is-not-logged-in-is-owner-do-rc-21 "gh auth status fails: rc $rc: $(grep '^\[owner-do\]' $T/o|head -1)" '[ $rc = 21 ]&&grep -qx "\[owner-do\] sudo -u '$PUSER' gh auth login   # the token stays in uid '$PUSER'" $T/o'

# ===== the round trip: a running town -> agi.sh stop -> agi.sh start (the stopped-town rules, the units, the blast, town.state aside) =====
world;hact >/dev/null 2>&1;login;st >/dev/null 2>&1;up3;printf 'agi-carry@a.path\n' >>$SD/active;rm -f $SD/box.calls
for p in p1 p2 p3;do mkdir -p $T/h/$p;done
$G -C $M checkout -q fx/trunk 2>/dev/null;echo "AGI_TRUNK=$PIN" >$X/etc/agi/carry.env.x;cp $X/etc/agi/carry.env $T/carry.keep
stp >$T/o 2>$T/e;rcs=$?
ok st2-RT-stop-on-the-same-stubs-ends-stopped "stop rc $rcs: $(tail -1 $T/o)" '[ $rcs = 0 ]&&grep -q "^stopped tw" $T/o&&! grep -q "^agi-post@" $SD/active&&! grep -qx agi-boot.service $SD/enabled'
cp $T/state $T/state.stopped;before=$(calls '^(enable --now|enable agi-boot|start agi-boot)')
st >$T/o 2>$T/e;rc=$?;sa=$(ls $T/state.* 2>/dev/null|grep -v stopped|head -1)
ok st2-RT-start-after-a-stop-ends-0-with-town-state-moved-aside-whole "rc $rc; $T/state gone: $([ ! -e $T/state ]&&echo yes||echo NO); aside: $(ls $T|grep '^state\.'|tr '\n' ' ')" '[ $rc = 0 ]&&[ ! -e $T/state ]&&[ ! -e $T/starting ]&&[ -n "$sa" ]&&cmp -s "$sa" $T/state.stopped'
ok st2-RT-the-recorded-running-set-and-the-agi-boot-are-back "active posts: $(grep -c '^agi-post@' $SD/active); agi-boot: $(grep -cx agi-boot.service $SD/enabled)" '[ "$(grep -c "^agi-post@" $SD/active)" = 3 ]&&grep -qx agi-boot.service $SD/enabled&&grep -qx "town up '$PIN'" $SD/box.calls'
ok st2-RT-the-stopped-unit-agi-quiet-watch-timer-came-back-enabled "enabled: $(grep -c quiet-watch $SD/enabled)" 'grep -qx agi-quiet-watch.timer $SD/enabled'
# S8 mutants: an enable that leaves the unit disabled must make start die; the read-back dropped lets it through
for how in units boot;do world;hact >/dev/null 2>&1;login;st >/dev/null 2>&1;up3;stp >/dev/null 2>&1
 if [ $how = units ];then st STUB_ENABLE_NOOP=agi-quiet-watch.timer >$T/o 2>$T/e;rc=$?;else st STUB_ENABLE_NOOP=agi-boot.service >$T/o 2>$T/e;rc=$?;fi
 ok "st2-Rc-an-enable-that-leaves-$how-disabled-makes-start-die" "rc $rc: $(grep -o 'want exactly .enabled.' $T/e|head -1)" '[ $rc != 0 ]&&grep -q "want exactly .enabled." $T/e&&[ -e $T/state ]'
 world;hact >/dev/null 2>&1;login;st >/dev/null 2>&1;up3;stp >/dev/null 2>&1
 if [ $how = units ];then pm '[ "$(systemctl is-enabled "$n" 2>/dev/null)" = enabled ]||{ echo "[units] $n reads' 'true||{ echo "[units] $n reads';st STUB_ENABLE_NOOP=agi-quiet-watch.timer >$T/o 2>$T/e;rc=$?
 else pm ';bootok||die "[posts] agi-boot.service reads' ';true||die "[posts] agi-boot.service reads';st STUB_ENABLE_NOOP=agi-boot.service >$T/o 2>$T/e;rc=$?;fi
 ok "st2-Rc-mutant-the-$how-read-back-dropped-lets-a-disabled-unit-through-RED" "rc $rc with the read-back dropped (the clean row dies)" '! grep -q "want exactly .enabled." $T/e';done
# stuck dialogs: the S9 probe lists post name + title only, keeps town.state, and the mutant that drops the probe lets the start end
world;hact >/dev/null 2>&1;login;st >/dev/null 2>&1;up3;stp >/dev/null 2>&1;printf 'SECRETTAIL some text \033[1mTry the new fullscreen renderer\033[0m more\n' >$T/h/p2/o;st >$T/o 2>$T/e;rc=$?
ok st2-F4a-a-post-stuck-at-a-first-run-dialog-is-listed-by-name-and-title-only "rc $rc: $(grep '^\[dialog\]' $T/e|head -1)" '[ $rc = 1 ]&&grep -qx "\[dialog\] p2 is stuck at: Try the new fullscreen renderer" $T/e&&! grep -q SECRETTAIL $T/o $T/e&&[ -e $T/state ]'
world;hact >/dev/null 2>&1;login;st >/dev/null 2>&1;up3;stp >/dev/null 2>&1;printf 'Try the new fullscreen renderer\n' >$T/h/p2/o;pm 'stuck(){ for p' 'stuck(){ return 0;for p';st >$T/o 2>$T/e;rc=$?
ok st2-F4a-mutant-a-probe-that-sees-nothing-ends-the-start-RED "rc $rc with the probe dropped (the clean row exits 1)" '[ $rc = 0 ]'
# the clone path: MAIN absent -> the public clone, the pin checked out on the origin branch that holds it
world;hact >/dev/null 2>&1;$G clone -q --bare $M $T/origin.git;mv $M $T/main.away;st >$T/o 2>$T/e;rc=$?;mv $T/main.away $T/main.back 2>/dev/null
ok st2-S2-main-absent-clones-the-origin-at-the-pin "rc $rc (host not met is fine: it stops AT host): HEAD $($G -C $M rev-parse HEAD 2>/dev/null|cut -c1-12) branch $($G -C $M branch --show-current 2>/dev/null)" '[ "$($G -C $M rev-parse HEAD 2>/dev/null)" = "'$PIN'" ]&&[ "$($G -C $M branch --show-current)" = fx/trunk ]&&grep -q "^main: cloned" $T/o'
world;hact >/dev/null 2>&1;$G -C $M -c user.name=t -c user.email=t@t -c commit.gpgsign=false commit -q --allow-empty -m later;P2=$($G -C $M rev-parse HEAD);$G -C $M reset -q --hard HEAD~1;st PIN=$P2 >$T/o 2>$T/e;rc=$?
ok st2-S2-a-pin-that-is-not-an-ancestor-of-HEAD-is-refused "rc $rc: $(grep -o '\[main\][^;]*' $T/e|head -1|cut -c1-80)" '[ $rc != 0 ]&&grep -q "^\[main\].*not an ancestor" $T/e'
# cond 6: a row name without an up arm -> start refuses with 0 units started
world;hact >/dev/null 2>&1;sed -i 's/^town\tstart\tmain host/town\tstart\tmain zzz host/' $M/.agi/nodes/.geometry/engine.md;$G -C $M -c user.name=t -c user.email=t@t -c commit.gpgsign=false commit -qam row;P3=$($G -C $M rev-parse HEAD);: >$SD/calls;st PIN=$P3 >$T/o 2>$T/e;rc=$?
ok st2-cond6-start-refuses-a-row-name-without-an-up-arm-and-starts-nothing "rc $rc: $(grep -o "\[step\][^:]*" $T/e|head -1), service calls $(calls '^(start|enable|restart|stop)')" '[ $rc != 0 ]&&grep -q "^\[step\] .zzz. (matrix row) has no up arm" $T/e&&[ "$(calls "^(start|enable|restart|stop)")" = 0 ]'
# S2-a: answer exempts only a value that IS an existing path
world;: >$T/env;chmod 600 $T/env;CMD="answer X /no/such/aaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaa" st >$T/o 2>$T/e;ra=$?;CMD="answer X $T/env" st >$T/o2 2>$T/e2;rb=$?
ok st2-S2a-answer-refuses-a-path-shaped-token-that-is-no-file-and-takes-a-real-path "a /<36 chars> with no such file: rc $ra (want 1); a real path: rc $rb (want 0)" '[ $ra = 1 ]&&grep -q "^\[secret\]" $T/e&&[ $rb = 0 ]'
pm '[ -e "$v" ]||for w in' 'true||for w in';CMD="answer X /no/such/aaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaa" st >$T/o 2>$T/e;ra=$?
ok st2-S2a-mutant-every-slash-value-exempt-is-RED "the old exemption: rc $ra (the clean row refuses with 1)" '[ $ra = 0 ]'

# ===== council 10-21 (S2b APPROVED): the follow-up commit B-6 / R-d / (2) / (3) / (4) =====
# (2) the host act ENABLES agi-boot and starts no post; start writes the flags with NO post of theirs up (Claude Code writes ~/.claude.json back on SIGTERM)
world;hact >$T/h.out 2>&1
ok st2-2-the-host-act-enables-agi-boot-and-starts-nothing "enabled agi-boot: $(grep -cx agi-boot.service $SD/enabled), units up: $(wc -l <$SD/active|tr -d ' '), start agi-boot calls: $(grep -c '^start agi-boot' $SD/calls)" 'grep -qx agi-boot.service $SD/enabled&&[ ! -s $SD/active ]&&! grep -q "^start agi-boot" $SD/calls'
world;hact >/dev/null 2>&1;login;printf 'agi-post@p1.service\n' >$SD/active;st STUB_SIGTERM=p1 >$T/o 2>$T/e;rc=$?
ok st2-2-a-post-that-rewrites-its-claude-json-on-SIGTERM-still-ends-with-the-flags "rc $rc: p1 .claude.json stale=$(jq -r '.stale' $T/h/p1/.claude.json 2>/dev/null) onboarding=$(jq -r '.hasCompletedOnboarding' $T/h/p1/.claude.json 2>/dev/null)" '[ $rc = 0 ]&&jq -e ".stale==true and .hasCompletedOnboarding==true and .fullscreenUpsellSeenCount>=3 and .projects[\"/data/work/agi\"].hasTrustDialogAccepted==true" $T/h/p1/.claude.json >/dev/null'
world;hact >/dev/null 2>&1;login;printf 'agi-post@p1.service\n' >$SD/active
A=$(sed -n '/cannot stop \$p before its flags/,/^ for p in \$nf;do flags_do \$p;done/p' $AG);[ "$(echo "$A"|wc -l|tr -d ' ')" = 2 ]||echo "# mutant text is not the two lines"
pm "$A" ' for p in $nf;do flags_do $p;done;for p in $nf;do isup $p&&systemctl restart "agi-post@$p.service";done';st STUB_SIGTERM=p1 >$T/o 2>$T/e;rc=$?
ok st2-2-mutant-the-old-order-flags-then-restart-loses-the-flags-RED "rc $rc with the old order: p1 flags $(jq -r '.hasCompletedOnboarding' $T/h/p1/.claude.json 2>/dev/null) (clean: true)" '! jq -e ".hasCompletedOnboarding==true" $T/h/p1/.claude.json >/dev/null 2>&1'
world;pm 'systemctl enable agi-boot.service||die "enable failed: sh $B/rollback.sh";fi' 'systemctl enable agi-boot.service&&systemctl start agi-boot.service||die "enable failed: sh $B/rollback.sh";fi';hact >/dev/null 2>&1
ok st2-2-mutant-the-act-tail-that-starts-agi-boot-is-seen "the act with start put back: start agi-boot calls $(grep -c '^start agi-boot' $SD/calls) (clean: 0)" '[ "$(grep -c "^start agi-boot" $SD/calls)" -ge 1 ]'
# (3) no ring at the pin = ONE line; a ring that exists but yields 0 keys keeps the WARNING; the mutant restores the M unread lines
world;hact >/dev/null 2>&1;login;pm '&&[ -z "$ro" ];then echo "[ring] no ring at' '&&[ -n "$ro" ];then echo "[ring] no ring at';st >$T/o 2>$T/e
ok st2-ring-mutant-the-no-ring-line-gone-brings-the-M-unread-lines-back-RED "unread lines: $(grep -c '^\[ring\] p[123]: unread' $T/e) (clean: 0), the one line: $(grep -c 'no ring at' $T/o)" '! grep -q "^\[ring\] no ring at" $T/o&&[ "$(grep -c "^\[ring\] p[123]: unread" $T/e)" = 3 ]'
world;echo "p1 ssh-ed25519 AAAA" >$M/.agi/nodes/.geometry/ring;$G -C $M add -A;$G -C $M -c user.name=t -c user.email=t@t -c commit.gpgsign=false commit -qm ring0;PIN=$($G -C $M rev-parse HEAD);hact >/dev/null 2>&1;login;st >$T/o 2>$T/e
ok st2-ring-a-ring-that-exists-with-0-keys-read-keeps-the-WARNING "$(grep -h '^\[ring\]' $T/o $T/e|sed -n '$p')" 'grep -q "^\[ring\] checked 0 of 3 posts" $T/o&&grep -q "^\[ring\] WARNING: 0 of 3" $T/e&&! grep -q "no ring at" $T/o'
# B-6: a recorded unit that does not start fails the step: rc != 0, no `started` line, the unit named, town.state and town.starting kept
b6(){ world;hact >/dev/null 2>&1;login;st >/dev/null 2>&1;up3;stp >/dev/null 2>&1;}
b6;st STUB_START_FAIL=agi-quiet-watch.timer >$T/o 2>$T/e;rc=$?
ok st2-B6-a-recorded-unit-whose-start-fails-ends-start-non-zero-with-no-started-line "rc $rc: $(grep -o '\[units\] cannot start [^ ]*' $T/e|head -1); started lines: $(grep -c '^started tw' $T/o); town.state $([ -e $T/state ]&&echo kept||echo GONE), town.starting $([ -e $T/starting ]&&echo kept||echo GONE)" '[ $rc != 0 ]&&! grep -q "^started tw" $T/o&&grep -q "^\[units\] cannot start agi-quiet-watch.timer" $T/e&&grep -q "^\[step\] units: still unmet" $T/e&&[ -e $T/state ]&&[ -e $T/starting ]'
st >$T/o 2>$T/e;rc=$?
ok st2-B6-the-re-run-after-the-unit-is-fixed-ends-clean "rc $rc, started: $(grep -c '^started tw' $T/o), town.starting $([ -e $T/starting ]&&echo kept||echo gone)" '[ $rc = 0 ]&&grep -q "^started tw" $T/o&&[ ! -e $T/starting ]'
b6;st STUB_START_NOOP=agi-quiet-watch.timer >$T/o 2>$T/e;rc=$?
ok st2-B6-a-unit-whose-start-returns-0-but-is-not-up-also-ends-start-non-zero "rc $rc: $(grep -o '\[units\] [^ ]* is not active[^(]*' $T/e|head -1); started lines: $(grep -c '^started tw' $T/o)" '[ $rc != 0 ]&&! grep -q "^started tw" $T/o&&grep -q "^\[units\] agi-quiet-watch.timer is not active after its start" $T/e'
b6;pm ';*)exit 1;;esac;done;}   # B-6' ';*);;esac;done;}   # B-6';st STUB_START_FAIL=agi-quiet-watch.timer >$T/o 2>$T/e;rc=$?
ok st2-B6-mutant-sk-units-without-the-is-active-read-gives-the-lying-last-line-RED "rc $rc, started lines $(grep -c '^started tw' $T/o) (clean: rc != 0, 0 lines)" '[ $rc = 0 ]&&grep -q "^started tw" $T/o'
# R-d: ROOT set => AGI_HOST_UNITS=<stub dir> holding systemctl sudo visudo gh crontab, else start dies before S0 with nothing written; the /etc defaults lie under $ROOT
world;hact >/dev/null 2>&1;login;st AGI_HOST_UNITS= >$T/o 2>$T/e;rc=$?
ok st2-Rd-ROOT-without-AGI_HOST_UNITS-dies-before-S0-and-writes-nothing "rc $rc: $(head -1 $T/e|cut -c1-80); service calls $(calls '^(start|enable|restart|stop)'), town.starting $([ -e $T/starting ]&&echo written||echo none), town.env $([ -e $T/env ]&&echo written||echo none)" '[ $rc != 0 ]&&grep -q "^\[root\] ROOT is set: AGI_HOST_UNITS=<stub dir>" $T/e&&[ "$(calls "^(start|enable|restart|stop)")" = 0 ]&&[ ! -e $T/starting ]&&[ ! -e $T/env ]&&[ ! -e $X/etc/agi/town.starting ]'
world;hact >/dev/null 2>&1;login;pm '[ -n "$AGI_HOST_UNITS" ]||die "[root] ROOT is set:' 'true||die "[root] ROOT is set:';st AGI_HOST_UNITS= >$T/o 2>$T/e;rc=$?
ok st2-Rd-mutant-the-ROOT-guard-gone-lets-the-rehearsal-run-RED "rc $rc with the guard dropped (the clean row dies at once): [root] lines $(grep -c '^\[root\]' $T/e), service calls $(calls '^(start|enable|restart|stop)')" '! grep -q "^\[root\] ROOT is set" $T/e&&[ "$(calls "^(start|enable|restart|stop)")" -ge 1 ]'
mkdir -p $T/shim3;cp $SH/* $T/shim3/;rm -f $T/shim3/crontab;world;hact >/dev/null 2>&1;login;SPATH=$T/shim3:/usr/bin:/bin st AGI_HOST_UNITS=$T/shim3 >$T/o 2>$T/e;rc=$?;SPATH=
ok st2-Rd-a-stub-dir-without-crontab-dies-naming-it "rc $rc: $(head -1 $T/e|cut -c1-90)" '[ $rc != 0 ]&&grep -q "^\[root\] AGI_HOST_UNITS needs stubs: crontab does not resolve inside" $T/e'
RDW(){ world;mkdir -p $X/etc/sudoers.d;rm -f $T/sudoers.d/90-agi-belam;hact >/dev/null 2>&1;}
RDW;st AGI_TOWN_ENV= AGI_TOWN_STATE= AGI_TOWN_STARTING= AGI_SUDOERS= AGI_SYSGITCONFIG= >$T/o 2>$T/e;rc=$?
ok st2-Rd-the-etc-defaults-lie-under-ROOT "rc $rc (21: no logins): town.starting under ROOT $([ -e $X/etc/agi/town.starting ]&&echo yes||echo NO), sudoers under ROOT $([ -e $X/etc/sudoers.d/90-agi-belam ]&&echo yes||echo NO), stray $T/starting $([ -e $T/starting ]&&echo YES||echo none)" '[ $rc = 21 ]&&[ -s $X/etc/agi/town.starting ]&&[ -s $X/etc/sudoers.d/90-agi-belam ]&&[ ! -e $T/starting ]&&[ ! -e $T/sudoers.d/90-agi-belam ]'
RDW;pm 'STARTING=${AGI_TOWN_STARTING:-$ROOT/etc/agi/town.starting}' 'STARTING=${AGI_TOWN_STARTING:-/nonexistent-live/etc/agi/town.starting}';st AGI_TOWN_ENV= AGI_TOWN_STATE= AGI_TOWN_STARTING= AGI_SUDOERS= AGI_SYSGITCONFIG= >$T/o 2>$T/e;rc=$?
ok st2-Rd-mutant-the-town-starting-default-off-ROOT-leaves-none-under-ROOT-RED "rc $rc: town.starting under ROOT $([ -e $X/etc/agi/town.starting ]&&echo yes||echo none) (clean: yes)" '[ ! -e $X/etc/agi/town.starting ]'
RDW;pm 'SUDOERS=${AGI_SUDOERS:-$ROOT/etc/sudoers.d/90-agi-belam}' 'SUDOERS=${AGI_SUDOERS:-/nonexistent-live/etc/sudoers.d/90-agi-belam}';st AGI_TOWN_ENV= AGI_TOWN_STATE= AGI_TOWN_STARTING= AGI_SUDOERS= AGI_SYSGITCONFIG= >$T/o 2>$T/e;rc=$?
ok st2-Rd-mutant-the-sudoers-default-off-ROOT-leaves-none-under-ROOT-RED "rc $rc: sudoers under ROOT $([ -e $X/etc/sudoers.d/90-agi-belam ]&&echo yes||echo none) (clean: yes)" '[ ! -e $X/etc/sudoers.d/90-agi-belam ]'
# (4) the blast prints how many dialog titles are unmeasured; the constant carries the comment naming the one measured title; the skill names the ring and the boot drift
world;hact >/dev/null 2>&1;login;st >$T/o 2>$T/e;rc=$?
ok st2-4-blast-prints-N-of-M-titles-unmeasured-and-the-constant-names-the-measured-one "rc $rc: $(grep '^\[blast\] dialog probe' $T/o)" '[ $rc = 0 ]&&grep -qx "\[blast\] dialog probe: 5 of 6 titles unmeasured" $T/o&&grep -B1 "^TITLES=" $SRC|grep -q "ONLY .Try the new fullscreen renderer. is a MEASURED title"'
world;hact >/dev/null 2>&1;login;pm "MEASURED='Try the new fullscreen renderer'" "MEASURED=''";st >$T/o 2>$T/e
ok st2-4-mutant-no-measured-title-prints-6-of-6-RED "$(grep '^\[blast\] dialog probe' $T/o) (clean: 5 of 6)" '! grep -qx "\[blast\] dialog probe: 5 of 6 titles unmeasured" $T/o'
ok st2-skill-names-ring-unverified-and-the-by-design-boot-disabled-drift "agi-town SKILL.md: ring-unverified $(grep -c 'ring: unverified' $R0/skills/agi-town/SKILL.md), boot-disabled $(grep -c 'boot disabled' $R0/skills/agi-town/SKILL.md)" 'grep -q "ring: unverified" $R0/skills/agi-town/SKILL.md&&grep -q "boot disabled" $R0/skills/agi-town/SKILL.md'

# ===== council 10-21 BIND on the follow-up: B-7 (a oneshot with an up trigger is not recorded). H1 (a heal guard) is GONE: heal.py never touches agi-post@ units =====
# the stub: `systemctl show U -p TriggeredBy --value` answers from $SD/triggers ("unit trigger" per line); STUB_START_NOOP=U is a Type=oneshot RemainAfterExit=no that runs to its end and reads inactive
b7(){ world;hact >/dev/null 2>&1;login;st >/dev/null 2>&1;up3;printf 'agi-quiet-watch.service agi-quiet-watch.timer\n' >$SD/triggers;}
b7;printf 'agi-quiet-watch.service\n' >>$SD/active;stp >$T/o 2>$T/e;rcs=$?;st STUB_START_NOOP=agi-quiet-watch.service >$T/o 2>$T/e;rc=$?
ok st2-B7-a-oneshot-caught-mid-run-with-its-timer-up-is-not-recorded-and-start-ends-0 "stop rc $rcs; town.state(aside) timer: $(cat $T/state.* 2>/dev/null|grep -c 'unit agi-quiet-watch.timer enabled'), service: $(cat $T/state.* 2>/dev/null|grep -c 'unit agi-quiet-watch.service'); start rc $rc, started: $(grep -c '^started tw' $T/o)" '[ $rcs = 0 ]&&[ $rc = 0 ]&&grep -q "^started tw" $T/o&&cat $T/state.*|grep -qx "unit agi-quiet-watch.timer enabled"&&! cat $T/state.*|grep -q "unit agi-quiet-watch.service"'
b7;pm 'trigup $u||echo $u' 'echo $u';printf 'agi-quiet-watch.service\n' >>$SD/active;stp >$T/o 2>$T/e;st STUB_START_NOOP=agi-quiet-watch.service >$T/o 2>$T/e;rc=$?
ok st2-B7-mutant-the-skip-dropped-records-the-oneshot-and-start-never-finishes-RED "state has the service: $(cat $T/state 2>/dev/null|grep -c 'unit agi-quiet-watch.service'); start rc $rc (clean: service not recorded, rc 0)" 'grep -q "^unit agi-quiet-watch.service" $T/state&&[ $rc != 0 ]'
b7;grep -vx agi-quiet-watch.timer $SD/active>$SD/a.n;mv $SD/a.n $SD/active;printf 'agi-quiet-watch.service\n' >>$SD/active;stp >$T/o 2>$T/e
ok st2-B7-a-hand-run-oneshot-whose-timer-is-off-stays-recorded "town.state: $(grep 'agi-quiet-watch' $T/state|tr '\n' '|')" 'grep -qx "unit agi-quiet-watch.service" $T/state'
b7;pm 'echo "$ACT"|grep -qxF "$t"&&return 0;' 'return 0;';grep -vx agi-quiet-watch.timer $SD/active>$SD/a.n;mv $SD/a.n $SD/active;printf 'agi-quiet-watch.service\n' >>$SD/active;stp >$T/o 2>$T/e
ok st2-B7-mutant-skip-without-the-trigger-is-up-test-loses-the-hand-run-oneshot-RED "town.state: $(grep 'agi-quiet-watch' $T/state|tr '\n' '|') (clean: the service line)" '! grep -q "agi-quiet-watch.service" $T/state'

# (iii) council 10-21: a Type=oneshot RemainAfterExit=no unit is never recorded and never stopped (mid-run at stop = runs to its own end); RemainAfterExit=yes stays recorded
os3(){ world;hact >/dev/null 2>&1;login;st >/dev/null 2>&1;up3;: >$SD/triggers;printf 'agi-hand.service\n' >$SD/oneshots;printf 'agi-hand.service\n' >>$SD/active;}
os3;stp >$T/o 2>$T/e;rcs=$?;st STUB_START_NOOP=agi-hand.service >$T/o 2>$T/e;rc=$?
ok st2-iii-a-hand-run-oneshot-mid-run-at-stop-is-not-recorded-not-stopped-and-start-ends-0 "stop rc $rcs; recorded: $(cat $T/state.* 2>/dev/null|grep -c 'agi-hand'); stop calls on it: $(grep -c '^stop agi-hand' $SD/calls); start rc $rc, started: $(grep -c '^started tw' $T/o)" '[ $rcs = 0 ]&&[ $rc = 0 ]&&grep -q "^started tw" $T/o&&! cat $T/state.*|grep -q agi-hand&&[ "$(grep -c "^stop agi-hand" $SD/calls)" = 0 ]'
os3;pm 'kept $u&&continue;oneshot $u&&continue;' 'kept $u&&continue;';stp >$T/o 2>$T/e;st STUB_START_NOOP=agi-hand.service >$T/o 2>$T/e;rc=$?
ok st2-iii-mutant-the-oneshot-rule-dropped-records-it-and-start-never-finishes-RED "recorded: $(cat $T/state 2>/dev/null|grep -c 'agi-hand'); start rc $rc (clean: not recorded, rc 0)" 'grep -q "^unit agi-hand.service" $T/state&&[ $rc != 0 ]'
os3;printf 'agi-hand.service\n' >$SD/remain;stp >$T/o 2>$T/e
ok st2-iii-a-oneshot-with-RemainAfterExit-yes-stays-recorded "town.state: $(grep 'agi-hand' $T/state|tr '\n' '|')" 'grep -qx "unit agi-hand.service" $T/state'
# sp's pid row: an engine.v 4 row of this box with pid != 0 is refused by start (and by stop in the agi-town lane), naming it
pidw(){ world;hact >/dev/null 2>&1;login;sed -i '/"name":"far"/i\  - {"name":"pv","parent":"belam","harness":"claude","box":"tw","pid":'$1',"engine":{"v":4,"name":"pv","harness":"claude","model":"m","effort":"low"}}' $M/.agi/nodes/.geometry/posts.md;$G -C $M add -A;$G -C $M -c user.name=t -c user.email=t@t -c commit.gpgsign=false commit -qm pid;PIN=$($G -C $M rev-parse HEAD);hact >/dev/null 2>&1;}
pidw 1;st >$T/o 2>$T/e;rc=$?
ok st2-pid-a-local-engine-v4-row-with-pid-1-is-refused-by-start-naming-it "rc $rc: $(grep -o '\[pid\][^:]*: pv' $T/e|head -1|cut -c1-90); service calls $(calls '^(start|enable|restart|stop)')" '[ $rc != 0 ]&&grep -q "^\[pid\] .*pv .*heal would see it" $T/e&&[ "$(calls "^(start|enable|restart|stop)")" = 0 ]'
pidw 0;st >$T/o 2>$T/e;rc=$?
ok st2-pid-a-local-engine-v4-row-with-pid-0-is-not-refused "rc $rc: [pid] lines $(grep -c '^\[pid\]' $T/e) (want 0)" '! grep -q "^\[pid\]" $T/e'
pidw 1;pm 'pidchk "nothing started"' ':';st >$T/o 2>$T/e;rc=$?
ok st2-pid-mutant-the-check-dropped-lets-start-past-a-pid-1-row-RED "rc $rc, [pid] lines $(grep -c '^\[pid\]' $T/e) (clean: refused)" '! grep -q "^\[pid\]" $T/e'
echo "agi-town-start: $f FAIL";exit $f
