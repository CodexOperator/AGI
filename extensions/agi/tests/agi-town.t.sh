#!/bin/sh
# agi-town.t.sh: goal:g7.16.1.11.44.8 S1 (council 3/3 10-15 19:36Z + 19:41Z + 19:44Z + 19:45Z): agi.sh status + stop on STUBS ONLY. systemctl, crontab, sudo, id and getent are shims on PATH that keep their state in files under a
# scratch dir; MAIN is a scratch git repo; the box under test is the PIECE (`sect box`) of the tree this file sits in, so the blast is the real one. NEVER the live town, never a real stop: no root, no systemd, no network, 0 USD.
# ROOT=<tree> (default: the tree this file sits in) is read for agi.sh, crons.py, engine.md (the real matrix row), .agi/config.json (the real agi_town cell) and the guard script sanctuary-watch.
# One ok/FAIL line per case; exit = number of FAILs. Every MUTANT is one edit on the code under test (rep) or on the fixture, and its row passes only when the clean property BREAKS.
T=$(mktemp -d);trap 'rm -rf $T' 0;f=0;R0=${ROOT:-$(cd "$(dirname "$0")/../../.." && pwd)};G=/usr/bin/git
ok(){ if eval "$3";then echo "ok $1 $2";else echo "FAIL $1 $2";f=$((f+1));for x in $T/o $T/e;do [ -s $x ]&&head -4 $x|cut -c1-220|sed "s/^/#   ${x##*/}: /";done;fi;}
AG=$R0/extensions/agi/bin/agi.sh;CRONS=$R0/extensions/agi/bin;[ -f $AG ]||{ echo "FAIL inputs: $AG";exit 99;}
sect(){ cat $R0/.agi/nodes/.geometry/engine*.md|sed -n "/^###* $1 /,/^###* /{/^~~~/,/^~~~/{//!p}}";}
sect box >$T/box;chmod +x $T/box;[ -s $T/box ]||{ echo "FAIL extract: box";exit 99;}
# --- shims
SH=$T/shim;SD=$T/sd;mkdir -p $SH $SD/cron $T/home $T/wants
cat >$SH/id <<'EOF'
#!/bin/sh
case $1 in -un)echo ${STUB_UID:-nobody};; -u)echo ${STUB_IDU:-0};; *)exec /usr/bin/id "$@";;esac
EOF
cat >$SH/getent <<'EOF'
#!/bin/sh
[ "$1" = passwd ]&&[ $# = 1 ]&&{ cat $STUB_SD/passwd;exit 0;};exec /usr/bin/getent "$@"
EOF
cat >$SH/systemctl <<'EOF'
#!/bin/sh
# state: $STUB_SD/active (unit per line), $STUB_SD/enabled; STUB_FAIL=stop:U|disable:U fails that call; STUB_NOOP=stop:U succeeds without stopping; every mutating call is logged with whether town.state existed
a=$STUB_SD/active;e=$STUB_SD/enabled;touch $a $e
case $1 in
list-units)awk '{print $1" loaded active running stub"}' $a;;
is-enabled)grep -qx "$2" $e&&{ echo enabled;exit 0;};echo disabled;exit 1;;
stop|disable)echo "$1 $2 state=$([ -s "$STUB_STATE" ]&&echo yes||echo no)">>$STUB_SD/calls
 case ",$STUB_FAIL," in *,$1:$2,*)echo "stub: $1 $2 failed">&2;exit 1;;esac
 case ",$STUB_NOOP," in *,$1:$2,*)exit 0;;esac
 if [ $1 = stop ];then grep -vxF "$2" $a>$a.n;mv $a.n $a;else grep -vxF "$2" $e>$e.n;mv $e.n $e;fi;;
*)exit 0;;esac
EOF
cat >$SH/crontab <<'EOF'
#!/bin/sh
u=$2;f=$STUB_SD/cron/$u
case $3 in -l)[ -f $f ]||{ echo "no crontab for $u">&2;exit 1;};cat $f;;-)cat >$f;;esac
EOF
cat >$SH/sudo <<'EOF'
#!/bin/sh
[ "$1" = -n ]&&shift;[ "$1" = -H ]&&shift
if [ "$1" = -u ];then STUB_UID=$2;shift 2;export STUB_UID;[ "$STUB_UID" = agi-belam ]&&GIT_CONFIG_GLOBAL=$STUB_BELAMCFG&&export GIT_CONFIG_GLOBAL;fi
[ "$1" = -H ]&&shift
exec "$@"
EOF
chmod +x $SH/*
printf 'agi-belam:x:2:2::/h/b:/bin/sh\nagi-director-general-2:x:3:3::/h/d:/bin/sh\nagi-alive:x:4:4::/h/a:/bin/sh\nliborum:x:1000:1000::/h/l:/bin/sh\n' >$SD/passwd
# --- keys + MAIN (a scratch repo whose HEAD holds the real engine.md, the real config cell and a fixture posts.md)
mkdir $T/k $T/c;: >$T/signers
for u in belam alive sm dg1 dg2 dg3;do ssh-keygen -q -t ed25519 -N '' -f $T/k/$u -C $u>/dev/null;echo "$u@agi namespaces=\"git\" $(cut -d' ' -f1,2 $T/k/$u.pub)">>$T/signers
 printf '[user]\n\tname=%s\n\temail=%s@agi\n\tsigningkey=%s\n[gpg]\n\tformat=ssh\n[gpg "ssh"]\n\tallowedSignersFile=%s\n[commit]\n\tgpgsign=false\n' $u $u $T/k/$u $T/signers>$T/c/$u;done
M=$T/main;$G init -q -b fx/trunk $M;mkdir -p $M/.agi/nodes/.geometry $M/.agi/nodes/doc
cat >$M/.agi/nodes/.geometry/posts.md <<'EOF'
  - {"name":"belam","parent":"owner","harness":"claude","box":"tw","boot":true}
  - {"name":"alive","parent":"belam","harness":"claude","box":"tw","boot":true}
  - {"name":"sm","parent":"belam","harness":"claude","box":"tw","boot":true}
  - {"name":"dg1","parent":"sm","harness":"claude","box":"tw"}
  - {"name":"dg2","parent":"sm","harness":"claude","box":"tw"}
  - {"name":"dg3","parent":"sm","harness":"claude","box":"tw"}
  - {"name":"far","parent":"belam","harness":"claude","box":"xx","boot":true}
EOF
jq '.values.local_maxxing.agi_town.ack_wait_s=3' $R0/.agi/config.json >$M/.agi/config.json
sed '/^town	start	/d' $R0/.agi/nodes/.geometry/engine.md >$M/.agi/nodes/.geometry/engine.md
cm(){ $G -C $M add -A;$G -C $M -c user.name=x -c user.email=x@x commit -q -m "$1";$G -C $M rev-parse HEAD;}
PIN0=$(cm norow);cp $R0/.agi/nodes/.geometry/engine.md $M/.agi/nodes/.geometry/engine.md;PIN=$(cm withrow)
grep -qP '^town\tstart\tposts crons units blast\tagi.sh$' $M/.agi/nodes/.geometry/engine.md||{ echo "FAIL inputs: the tree's engine.md has no 'town start' row";exit 99;}
echo "AGI_TRUNK=$PIN" >$T/carry.env
BLK=$(python3 -c "import sys;sys.path.insert(0,'$CRONS');import crons;from pathlib import Path;print(*crons.block_markers(Path('$M')),sep='\n')");CB=$(echo "$BLK"|sed -n 1p);CE=$(echo "$BLK"|sed -n 2p)
# --- the town: 6 posts + boxwakes running, the timers/services, the keep-list units, agi-boot enabled; crontabs with the managed block + a foreign line
town(){ rm -f $SD/calls $SD/state $T/state;printf 'AGI_BOX=tw\n' >$T/env;chmod 600 $T/env;rm -rf $T/wants/*;: >$SD/active
 for p in belam alive sm dg1 dg2 dg3;do echo agi-post@$p.service>>$SD/active;echo agi-boxwake@$p.service>>$SD/active;done
 printf '%s\n' agi-quiet-watch.timer agi-quiet-watch.service agi-rc-keepalive.timer agi-dbus-reap.timer agi-reaper.service agi-alarms-x.service agi-boot.service agi-carry@a.path agi-memguard.service agi-ram-main.service>>$SD/active
 printf '%s\n' agi-boot.service agi-quiet-watch.timer>$SD/enabled
 for u in agi-belam agi-director-general-2;do printf '# mine\n%s\n* * * * * cd %s && echo job\n%s\n' "$CB" "$M" "$CE">$SD/cron/$u;done;rm -f $SD/cron/agi-alive
 for r in $($G -C $M for-each-ref --format='%(refname)' refs/box refs/held refs/heads/posts);do $G -C $M update-ref -d $r;done;}
# ag [VAR=val ...] ARGS: run agi.sh (or $AGSH) on the stubs
ag(){ env -i PATH=$SH:/usr/bin:/bin HOME=$T/home TMPDIR=$T STUB_SD=$SD STUB_STATE=$T/state STUB_BELAMCFG=$T/c/belam AGI_MAIN=$M AGI_TOWN_ENV=$T/env AGI_TOWN_STATE=$T/state AGI_CARRY_ENV=${CARRYF:-$T/carry.env} AGI_WANTS_DIR=$T/wants AGI_TOWN_BOXBIN=$T/box "$@" sh ${AGSH:-$AG} ${ARGS};}
run(){ ARGS="$*";ag ${XENV};}
mark(){ n=0;for u in agi-belam agi-director-general-2 agi-alive;do [ -f $SD/cron/$u ]&&n=$((n+$(grep -c -F -e "$CB" -e "$CE" -e '&& echo job' $SD/cron/$u)));done;echo $n;}
posts_up(){ grep -cE '^agi-(post|boxwake)@' $SD/active;}
outside(){ grep -vE '^agi-(post|boxwake)@|^agi-boot.service$|^agi-carry@.*\.path$|^agi-memguard|^agi-ram-main' $SD/active|wc -l|tr -d ' ';}
reboot(){ keep=$(grep -E '^agi-(carry@.*\.path|memguard|ram-main)' $SD/active);: >$SD/active;for u in $(cat $SD/enabled);do echo $u>>$SD/active;done;printf '%s\n' $keep>>$SD/active
 grep -qx agi-boot.service $SD/enabled&&$G -C $M show $PIN:.agi/nodes/.geometry/posts.md|sed -n 's/^  - {/{/p'|jq -r 'select(.boot==true and .box=="tw")|"agi-post@"+.name+".service"'>>$SD/active;}
snap(){ { cat $SD/active|sort|md5sum;cat $SD/enabled|sort|md5sum;cat $SD/cron/*|md5sum;[ -e $T/state ]&&echo state||echo nostate;} 2>/dev/null|tr '\n' ' ';}
rep(){ A=$1 B=$2 awk '{o="";r=$0;while((i=index(r,ENVIRON["A"]))>0){o=o substr(r,1,i-1) ENVIRON["B"];r=substr(r,i+length(ENVIRON["A"]))}print o r}' ${3:-$AG}>$T/mut.sh;cmp -s ${3:-$AG} $T/mut.sh&&echo "# NO EDIT for [$1]";AGSH=$T/mut.sh;}
rd(){ ( cd $M&&AGI_POST=$1 AGI_TRUNK=fx/trunk GIT_CONFIG_GLOBAL=$T/c/$1 GIT_CONFIG_SYSTEM=/dev/null sh $T/box read );}
# the acks the stop reads: dg2 and dg3 read the blast while the stop waits (held); dg1 writes its card after t0 (card); sm and alive never answer (noack)
card(){ mkdir -p $M/.agi/nodes/doc;: ;}
card(){ w=$T/cw;rm -rf $w;$G -C $M worktree prune;$G -C $M worktree add -q --detach $w $PIN;mkdir -p $w/.agi/nodes/doc;echo later>$w/.agi/nodes/doc/card-dg1.md;$G -C $w add -A;GIT_COMMITTER_DATE="4000000000 +0000" $G -C $w -c user.name=dg1 -c user.email=dg1@agi commit -q -m card;$G -C $M update-ref refs/heads/posts/dg1 $($G -C $w rev-parse HEAD);$G -C $M worktree remove --force $w;}
ST(){ { sleep 1;rd dg2;rd dg3;sleep 1;rd dg2;rd dg3; }>/dev/null 2>&1 & }

# ===== the routes that touch nothing =====
town;s0=$(snap);XENV= run stop --pack /nope >$T/o 2>&1;rc=$?
ok st-pack-is-s3-not-yet "stop --pack OUT: rc $rc (want 1), says [S3, not yet]: $(grep -c 'S3, not yet' $T/o), the town unchanged: $([ "$(snap)" = "$s0" ]&&echo yes||echo NO)" '[ $rc = 1 ]&&grep -q "S3, not yet" $T/o&&[ "$(snap)" = "$s0" ]'
XENV=STUB_IDU=1000 run stop >$T/o 2>&1;rc=$?
ok st-needs-root "stop as uid 1000: rc $rc (want 1), [root] named, the town unchanged" '[ $rc = 1 ]&&grep -q "^\[root\]" $T/o&&[ "$(snap)" = "$s0" ]'
rm -f $T/env;XENV= run stop >$T/o 2>&1;rc=$?
ok st-asks-for-the-box-once "no AGI_BOX anywhere: rc $rc (want 20), $(grep -c '^\[ask\]' $T/o) [ask] line (want 1), the town unchanged" '[ $rc = 20 ]&&[ "$(grep -c "^\[ask\]" $T/o)" = 1 ]&&grep -q "^\[ask\] AGI_BOX" $T/o&&[ "$(snap)" = "$s0" ]'
XENV= run answer AGI_BOX tw >$T/o 2>&1;rc=$?;md=$(stat -c %a $T/env)
ok st-answer-writes-town-env-600 "answer AGI_BOX tw: rc $rc (want 0), $(cat $T/env | tr '\n' ' ') mode $md (want 600)" '[ $rc = 0 ]&&[ "$(cat $T/env)" = "AGI_BOX=tw" ]&&[ $md = 600 ]'
b0=$(md5sum <$T/env);bad=0
A1(){ XENV= run answer "$@" >/dev/null 2>&1&&bad=1;}
A1 lower x;A1 AGI_BOX "two words";A1 "A$(printf 'k%.0s' $(seq 40))" y;A1 TOK $(printf 'a%.0s' $(seq 40));A1 TOK2 'a$b';A1 TOK3 ghp_$(printf 'Z%.0s' $(seq 36));A1 TOK4 $(printf 'q%.0s' $(seq 129))
XENV= run answer onlyone >/dev/null 2>&1&&bad=1
ok st-answer-refuses-a-bad-key-a-bad-value-and-a-token-shaped-value "8 bad answers (lowercase key, a value with a space, a 41-char key, a 40-char token, a \$ value, a ghp_ token, a 129-char value, one argument): all refused ($bad, want 0), town.env unchanged: $([ "$b0" = "$(md5sum <$T/env)" ]&&echo yes||echo NO)" '[ $bad = 0 ]&&[ "$b0" = "$(md5sum <$T/env)" ]'
XENV= run status >$T/o 2>&1;rc=$?
ok st-status-reads-the-live-town-and-writes-nothing "status on the running town: rc $rc (want 1), $(tr '\n' ' ' <$T/o), the town unchanged: $([ "$(snap)" = "$s0" ]&&echo yes||echo NO)" '[ $rc = 1 ]&&grep -q "^posts-running 12$" $T/o&&grep -q "^agi-boot-enabled 1$" $T/o&&grep -q "^cron-lines 6$" $T/o&&[ "$(snap)" = "$s0" ]'
# deps: a PATH with every tool except jq
mkdir -p $T/nojq;for x in /usr/bin/* /bin/*;do [ -e $T/nojq/${x##*/} ]||[ ${x##*/} = jq ]||ln -s $x $T/nojq/ 2>/dev/null;done
env -i PATH=$T/nojq HOME=$T/home AGI_MAIN=$M AGI_TOWN_ENV=$T/env AGI_TOWN_STATE=$T/state AGI_CARRY_ENV=$T/carry.env sh -c "STUB_IDU=0 sh $AG stop" >$T/o 2>&1;rc=$?
ok st-owner-do-for-a-missing-dep "no jq on PATH: rc $rc (want 21), $(grep '^\[owner-do\]' $T/o)" '[ $rc = 21 ]&&grep -q "^\[owner-do\] sudo apt-get install -y jq" $T/o'
CARRYF=$T/carry0 ;echo "AGI_TRUNK=$PIN0" >$T/carry0;XENV= run stop >$T/o 2>&1;rc=$?
ok st-matrix-row-missing-refuses "the pin has no 'town start' row: rc $rc (want 1), [matrix] named, the town unchanged" '[ $rc = 1 ]&&grep -q "^\[matrix\]" $T/o&&[ "$(snap)" = "$s0" ]'
CARRYF=
printf 'AGI_TRUNK=zz\n' >$T/carry1;CARRYF=$T/carry1 XENV= run stop >$T/o 2>&1;rc=$?
ok st-bad-pin-refuses "a pin that is not 40 hex: rc $rc (want 1), [pin] named, the town unchanged" '[ $rc = 1 ]&&grep -q "^\[pin\]" $T/o&&[ "$(snap)" = "$s0" ]'
CARRYF=
touch $T/wants/agi-post@dg2.service;XENV= run stop >$T/o 2>&1;rc=$?
ok st-etc-wants-links-refuse-before-anything "an agi-post@ link left under the wants dir (belam's host act not done): rc $rc (want 1), [links] named, the town unchanged" '[ $rc = 1 ]&&grep -q "^\[links\]" $T/o&&[ "$(snap)" = "$s0" ]'
rm -f $T/wants/*

# ===== the stop =====
town;card;ST;XENV= run stop >$T/o 2>$T/e;rc=$?
ok st-stop-rc0 "stop on the stubs: rc $rc (want 0); stdout: $(tail -1 $T/o)" '[ $rc = 0 ]&&grep -q "^stopped tw: tw " $T/o'
ok st-town-state-lines "town.state: [$(tr '\n' '|' <$T/state)] mode $(stat -c %a $T/state) (want boot enabled, 6 running, the 3 'unit' lines of the stopped agi-* units, 5 ack/noack lines, no want line, ONE stopped tw line LAST, mode 644)" 'grep -qx "boot enabled" $T/state&&[ "$(grep -c "^running " $T/state)" = 6 ]&&! grep -q "^want" $T/state&&[ "$(sed -n "\$p" $T/state|cut -d" " -f1,2)" = "stopped tw" ]&&[ "$(grep -c "^stopped " $T/state)" = 1 ]&&[ "$(stat -c %a $T/state)" = 644 ]&&[ "$(grep -c "^unit " $T/state)" = 6 ]&&grep -qx "unit agi-quiet-watch.timer enabled" $T/state&&! grep -E "^unit agi-(post|boxwake|carry|memguard|ram-main|boot)" $T/state'
ok st-acks-by-the-down-sha "ack lines: [$(grep -E '^(ack|noack)' $T/state|sort|tr '\n' '|')] (want ack dg1 card, ack dg2 held, ack dg3 held, noack alive, noack sm); stderr names the noacks: $(grep -c noack $T/e)" '[ "$(grep -E "^(ack|noack)" $T/state|sort|tr "\n" "|")" = "ack dg1 card|ack dg2 held|ack dg3 held|noack alive|noack sm|" ]&&[ "$(grep -c "^\[blast\] noack" $T/e)" = 2 ]'
ok st-ONE-down-commit-per-post "refs/box/belam/*: $($G -C $M for-each-ref refs/box/belam|wc -l|tr -d ' ') (want 5: not belam, not the other box); commits on dg2: $($G -C $M rev-list --count refs/box/belam/dg2)" '[ "$($G -C $M for-each-ref refs/box/belam|wc -l|tr -d " ")" = 5 ]&&[ "$($G -C $M rev-list --count refs/box/belam/dg2)" = 1 ]'
ok st-the-town-is-down "running posts $(posts_up) (want 0), units outside the keep-list $(outside) (want 0), marked cron lines $(mark) (want 0), agi-boot enabled: $(grep -c agi-boot $SD/enabled) (want 0); the keep-list still active: $(grep -cE '^agi-(carry@a.path|memguard|ram-main)' $SD/active) (want 3)" '[ "$(posts_up)" = 0 ]&&[ "$(outside)" = 0 ]&&[ "$(mark)" = 0 ]&&! grep -q agi-boot $SD/enabled&&[ "$(grep -cE "^agi-(carry@a.path|memguard|ram-main)" $SD/active)" = 3 ]'
ok st-crons-only-the-block-goes "the foreign lines of each crontab stay: $(grep -c '^# mine' $SD/cron/agi-belam) '# mine' line in agi-belam's (want 1); crons_live and the graph untouched: $($G -C $M status --porcelain|wc -l|tr -d ' ') dirty path(s) in MAIN (want 0)" '[ "$(grep -c "^# mine" $SD/cron/agi-belam)" = 1 ]&&[ "$(grep -c "^# mine" $SD/cron/agi-director-general-2)" = 1 ]&&[ -z "$($G -C $M status --porcelain)" ]'
ok st-state-before-the-first-stop "the first stop/disable call saw town.state: $(head -1 $SD/calls) (want state=yes); every call did: $(grep -c 'state=yes' $SD/calls)/$(wc -l <$SD/calls|tr -d ' ')" 'head -1 $SD/calls|grep -q "state=yes"&&! grep -q "state=no" $SD/calls'
reboot
ok st-F2-after-a-stub-reboot-no-post-starts "after the stub reboot: running agi-post@ = $(grep -c '^agi-post@' $SD/active) (want 0), agi-* units outside the keep-list = $(outside) (want 0)" '[ "$(grep -c "^agi-post@" $SD/active)" = 0 ]&&[ "$(outside)" = 0 ]'
# a second stop is a no-op: no second blast, state kept
s1=$(snap);XENV= run stop >$T/o 2>&1;rc=$?
ok st-second-stop-is-a-noop "second stop: rc $rc (want 0), commits on dg2 still $($G -C $M rev-list --count refs/box/belam/dg2) (want 1), town.state keeps $(grep -c '^running ' $T/state) running lines (want 6)" '[ $rc = 0 ]&&[ "$($G -C $M rev-list --count refs/box/belam/dg2)" = 1 ]&&[ "$(grep -c "^running " $T/state)" = 6 ]'
ARGS=status;ag >$T/o 2>&1;rc=$?
ok st-status-after-the-stop-is-all-zero "status: rc $rc (want 0): $(tr '\n' ' ' <$T/o)" '[ $rc = 0 ]'

# ===== G, the static form: a stub that fails between steps leaves a town.state with no `stopped` line =====
town;ST;XENV=STUB_FAIL=disable:agi-boot.service run stop >$T/o 2>$T/e;rc=$?
ok st-G-a-failing-step-leaves-the-state-and-no-stopped-line "agi-boot cannot be disabled: rc $rc (want 1); town.state exists with $(grep -c '^running ' $T/state) running lines (want 6) and $(grep -c '^stopped' $T/state) stopped line (want 0)" '[ $rc = 1 ]&&[ "$(grep -c "^running " $T/state)" = 6 ]&&! grep -q "^stopped" $T/state'
town;ST;XENV=STUB_FAIL=stop:agi-quiet-watch.timer run stop >$T/o 2>$T/e;rc=$?
ok st-G-a-failing-unit-stop-leaves-the-state-and-no-stopped-line "agi-quiet-watch.timer cannot be stopped: rc $rc (want 1); town.state has $(grep -c '^running ' $T/state) running lines (want 6), no stopped line: $(grep -c '^stopped' $T/state), the posts are still up: $(posts_up) (want 12: nothing past the units step ran)" '[ $rc = 1 ]&&[ "$(grep -c "^running " $T/state)" = 6 ]&&! grep -q "^stopped" $T/state&&[ "$(posts_up)" = 12 ]'
town;ST;XENV=STUB_NOOP=stop:agi-quiet-watch.timer run stop >$T/o 2>$T/e;rc=$?
ok st-F2-a-unit-left-running-is-counted "quiet-watch left running: rc $rc (want 1, [step] units named), agi-* units outside the keep-list = $(outside) (want 1)" '[ $rc = 1 ]&&grep -q "^\[step\] units" $T/e&&[ "$(outside)" = 1 ]'

# ===== the order, from the matrix row =====
# posts before units: heal (agi-reaper*) would relaunch a stopped post, so the posts step refuses while it is up
town;ST;$G -C $M show $PIN:.agi/nodes/.geometry/engine.md|sed 's/^town	start	posts crons units blast	agi.sh$/town	start	units posts crons blast	agi.sh/'>$M/.agi/nodes/.geometry/engine.md;P2=$(cm reorder);echo "AGI_TRUNK=$P2" >$T/carry2
CARRYF=$T/carry2 XENV= run stop >$T/o 2>$T/e;rc=$?
ok st-reaper-refuses-posts-before-units "the row read as 'units posts crons blast' (posts runs before units): rc $rc (want 1), [reaper] named: $(grep -c '^\[reaper\]' $T/e), the posts still up: $(posts_up) (want 12), agi-boot still enabled: $(grep -c agi-boot $SD/enabled)" '[ $rc = 1 ]&&grep -q "^\[reaper\]" $T/e&&[ "$(posts_up)" = 12 ]&&grep -q agi-boot $SD/enabled'
CARRYF=
# a row that lacks `crons`: the crontabs keep their block, the stop says so and fails (F1: delete `crons` from the row -> crontab diff > 0)
town;ST;$G -C $M show $PIN:.agi/nodes/.geometry/engine.md|sed 's/^town	start	posts crons units blast	agi.sh$/town	start	posts units blast	agi.sh/'>$M/.agi/nodes/.geometry/engine.md;P3=$(cm nocrons);echo "AGI_TRUNK=$P3" >$T/carry3
CARRYF=$T/carry3 XENV= run stop >$T/o 2>$T/e;rc=$?
ok st-F1-mutant-crons-deleted-from-the-row-is-RED "row 'posts units blast': rc $rc (want 1), marked cron lines left = $(mark) (want > 0; the clean stop leaves 0)" '[ $rc = 1 ]&&[ "$(mark)" -gt 0 ]'
CARRYF=
# a row naming a step this agi.sh has no down arm for
$G -C $M show $PIN:.agi/nodes/.geometry/engine.md|sed 's/^town	start	posts crons units blast	agi.sh$/town	start	main host posts crons units blast	agi.sh/'>$M/.agi/nodes/.geometry/engine.md;P4=$(cm main);echo "AGI_TRUNK=$P4" >$T/carry4
town;s0=$(snap);CARRYF=$T/carry4 XENV= run stop >$T/o 2>$T/e;rc=$?
ok st-a-row-step-without-a-down-arm-refuses "the row lists 'main' and 'host' (S3): rc $rc (want 1), [step] named, the town unchanged: $([ "$(snap)" = "$s0" ]&&echo yes||echo NO)" '[ $rc = 1 ]&&grep -q "^\[step\]" $T/e&&[ "$(snap)" = "$s0" ]'
CARRYF=
$G -C $M reset -q --hard $PIN

# ===== MUTANTS of the code: one edit, the clean row above must BREAK =====
mk(){ town;ST;XENV= run stop >$T/o 2>$T/e;rc=$?;}
rep 'dn_crons(){' 'dn_crons(){ return 0;';mk
ok st-F2-mutant-skip-T2-is-RED "dn_crons returns at once: rc $rc (want 1), marked cron lines = $(mark) (want > 0)" '[ $rc = 1 ]&&[ "$(mark)" -gt 0 ]'
AGSH=
rep 'systemctl disable agi-boot.service||die "[posts] cannot disable agi-boot.service"' ':';mk;reboot
ok st-F2-mutant-agi-boot-left-enabled-is-RED "agi-boot never disabled: rc $rc (want 1); after the stub reboot $(grep -c '^agi-post@' $SD/active) agi-post@ unit(s) start (want > 0: the boot rows; the clean row wants 0)" '[ $rc = 1 ]&&[ "$(grep -c "^agi-post@" $SD/active)" -gt 0 ]'
AGSH=
rep 'ck_blast(){ [ -s "$STATE" ]||[ -e "$SCR/ack" ];}' 'ck_blast(){ false;}';town;ST;XENV= run stop >/dev/null 2>&1;XENV= run stop >/dev/null 2>&1;ST
ok st-F1-mutant-double-blast-is-RED "a blast that never checks the state: commits on dg2 = $($G -C $M rev-list --count refs/box/belam/dg2) (want 2: the clean row has 1)" '[ "$($G -C $M rev-list --count refs/box/belam/dg2)" = 2 ]'
AGSH=
# an interrupted stop resumes from the FIRST town.state (the lists of what was up), not from the half-stopped town it finds
town;ST;XENV=STUB_FAIL=stop:agi-rc-keepalive.timer run stop >/dev/null 2>&1;XENV= run stop >$T/o 2>$T/e;rc=$?
ok st-resume-keeps-the-first-state "a stop that failed at rc-keepalive, then re-run: rc $rc (want 0), town.state keeps $(grep -c '^unit ' $T/state) unit line(s) (want 6) and $(grep -c '^running ' $T/state) running (want 6), ONE stopped line: $(grep -c '^stopped' $T/state)" '[ $rc = 0 ]&&[ "$(grep -c "^unit " $T/state)" = 6 ]&&[ "$(grep -c "^running " $T/state)" = 6 ]&&[ "$(grep -c "^stopped" $T/state)" = 1 ]'
rep 'wstate(){ [ -s "$STATE" ]&&return 0;' 'wstate(){ ';town;ST;XENV=STUB_FAIL=stop:agi-rc-keepalive.timer run stop >/dev/null 2>&1;XENV= run stop >/dev/null 2>&1
ok st-mutant-state-rewritten-on-resume-is-RED "a state written on every run: after the failed stop and its re-run town.state holds $(grep -c '^unit ' $T/state) unit line(s) (want < 6: the re-run saw the half-stopped town; the clean row keeps 6)" '[ "$(grep -c "^unit " $T/state)" -lt 6 ]'
AGSH=
rep 'dn_units(){ wstate' 'dn_units(){ ';cp $T/mut.sh $T/mut1.sh;rep 'die "[units] cannot disable $u";done;}' 'die "[units] cannot disable $u";done;wstate;}' $T/mut1.sh
town;ST;XENV=STUB_FAIL=stop:agi-quiet-watch.timer run stop >$T/o 2>$T/e;rc=$?
ok st-G-mutant-state-written-after-the-stops-is-RED "town.state written after the unit stops: with a failing stop the state exists: $([ -s $T/state ]&&echo yes||echo NO) (want NO: the clean row leaves it), first call saw state=$(head -1 $SD/calls|sed 's/.*state=//')" '[ ! -s $T/state ]&&head -1 $SD/calls|grep -q "state=no"'
AGSH=
AGSH=

# ===== sanctuary-watch stands down on a stopped town =====
W=$R0/extensions/agi/guard/sanctuary-watch;[ -f $W ]||{ echo "FAIL inputs: $W";exit 99;}
mkdir -p $T/wh/work/.sanctuary $T/wh/.local/state/sanctuary-guard $T/wh/logs $T/wsh
printf '{"hub":{"name":"gw","overlay_ip":"10.0.0.1"},"towns":{"peer":{"host":"peerhost","overlay_ip":"10.0.0.2"}}}\n' >$T/wh/work/.sanctuary/hosts.json
for c in ping ssh journalctl;do printf '#!/bin/sh\n[ %s = ping ]&&case "$*" in *10.0.0.1*)exit 0;;esac\nexit 1\n' $c >$T/wsh/$c;done;printf '#!/bin/sh\nexit 0\n' >$T/wsh/journalctl
printf '#!/bin/sh\necho "$@" >>%s/launches\n' $T/wsh >$T/wsh/systemd-run;printf '#!/bin/sh\nexit 0\n' >$T/wsh/systemctl;chmod +x $T/wsh/*
sw(){ rm -f $T/wsh/launches;rm -rf $T/wh/.local/state/sanctuary-guard;mkdir -p $T/wh/.local/state/sanctuary-guard;echo "0 0 0 0" >$T/wh/.local/state/sanctuary-guard/peer.peer
 env -i PATH=$T/wsh:/usr/bin:/bin HOME=$T/wh XDG_STATE_HOME=$T/wh/.local/state SANCTUARY=$T/wh/work/.sanctuary FAILS=1 PEER_CLAUDE=1 COOLDOWN=1 TOWN_STATE=$1 bash $2 >$T/sw.out 2>&1;rc=$?;[ -f $T/wsh/launches ]&&wc -l <$T/wsh/launches|tr -d ' '||echo 0;}
printf 'boot enabled\nrunning dg2\n' >$T/ws.nostop;printf 'boot enabled\nrunning dg2\nstopped tw 2026-10-15T20:00:00Z\n' >$T/ws.stop
a=$(sw $T/ws.nostop $W);ok st-F2-watch-launches-a-recovery-agent-on-a-running-town "town.state without a stopped line, peer down, PEER_CLAUDE=1: recovery launches = $a (want 1)" '[ "$a" = 1 ]'
b=$(sw $T/ws.stop $W);ok st-F2-watch-stands-down-on-a-stopped-town "town.state WITH its stopped line: recovery launches = $b (want 0), the watch says so: $(grep -c 'stood down' $T/wh/logs/sanctuary-guard/watch.log 2>/dev/null)" '[ "$b" = 0 ]&&grep -q "stood down" $T/wh/logs/sanctuary-guard/watch.log'
sed 's#grep -q .\^stopped . "\$TOWN_STATE" 2>/dev/null#false#' $W >$T/watch.mut;cmp -s $W $T/watch.mut&&echo "# NO EDIT in the watch mutant"
c=$(sw $T/ws.stop $T/watch.mut);ok st-F2-mutant-the-watch-ignores-town-state-is-RED "the watch without the town.state read, on a stopped town: recovery launches = $c (want >= 1; the clean row wants 0)" '[ "$c" -ge 1 ]'
exit $f
