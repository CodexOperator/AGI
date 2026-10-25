#!/bin/sh
# stall-watch.t.sh: config:crons stall_watch (owner 01:1xZ 10-25). Runs extensions/agi/bin/stall_watch.sh (or SW=<file>, a
# mutant) on a SCRATCH repo with mail refs made by plain commits, a fake wants dir, fake ~/o files dated with touch -d, and
# systemctl/pgrep stubs on PATH (state from files under $T). NOW is fixed; no live ref, no network, no root, 0 USD.
# Lanes: s1 no unread = silent · s2 mail stall (old unread, still screen) = one named line + one spool line · s3 a busy
# screen (fresh ~/o) is not flagged · s4 young mail (< U) is not flagged · s5 held mail is read, not unread · s6 a unit not
# active = down · s7 no claude past G = no-claude, within G silent · s8 SELF is never listed · s9 the same condition inside
# GAP is quiet, after GAP it repeats · s10 cleared then back = re-alert · s11 a missing wants dir = unread, rc 1 ·
# s12 DRY prints and writes no spool · s13-s16 the four unread rows (council 01:4xZ 10-25). MUTANTS (MUT=1): the screen gate dropped (s3 must go RED), the GAP gate dropped,
# (s9 must go RED), each unread row dropped (m3-m6), N1 and N2 dropped (m7-m8). s17-s18 = N1/N2 (council 02:0xZ 10-25);
# the scratch repo runs with core.hooksPath=/dev/null (L), so the lane reads the same under every seat's uid.
T=$(mktemp -d);f=0;R0=$(cd "$(dirname "$0")/../../.." && pwd);SW=${SW:-$R0/extensions/agi/bin/stall_watch.sh}
trap "[ -n \"$KEEP\" ] || rm -rf $T" 0
ok(){ if eval "$2";then echo "ok $1";else echo "FAIL $1";f=$((f+1));fi;}
unset GIT_DIR GIT_WORK_TREE AGI_TRUNK AGI_POST DRY
NOW=2000000000;export NOW
mkdir -p $T/bin $T/w $T/st $T/s $T/sv
for p in belam alpha beta gamma delta;do touch $T/w/agi-post@$p.service;mkdir -p $T/s/$p;echo active>$T/sv/$p;echo 1 >$T/sv/$p.claude;done
# stubs: systemctl show agi-post@P.service -p ActiveState|ActiveEnterTimestamp --value ; pgrep -u agi-P -x claude
cat >$T/bin/systemctl <<EOF
#!/bin/sh
p=\${2#agi-post@};p=\${p%.service}
case \$4 in ActiveState)cat $T/sv/\$p;;ActiveEnterTimestamp)v=\$(cat $T/sv/\$p.since 2>/dev/null||echo 1000000000);[ "\$v" = empty ]||date -u -d @\$v '+%a %Y-%m-%d %H:%M:%S UTC';;esac
EOF
cat >$T/bin/pgrep <<EOF
#!/bin/sh
p=\${2#agi-};[ "\$(cat $T/sv/\$p.claude)" = 1 ]&&echo 4242
EOF
chmod +x $T/bin/*;PATH=$T/bin:$PATH;export PATH
git init -q $T/r;G="git -C $T/r -c core.hooksPath=/dev/null -c user.name=t -c user.email=t@t"   # (L) alive: the seats' global hooksPath ref-guard must not judge the scratch repo
mail(){ c=$(GIT_COMMITTER_DATE="@$3 +0000" GIT_AUTHOR_DATE="@$3 +0000" $G commit-tree -m "m" $($G hash-object -w -t tree /dev/null) ${4:+-p $4});$G update-ref refs/box/$1/$2 $c;echo $c;}
scr(){ touch -d @$2 $T/s/$1/o;}
for p in alpha beta gamma belam;do scr $p $NOW;done
mail alpha belam $NOW >/dev/null   # a box ref exists (row 3); mail to SELF is never read
run(){ AS=$R0/extensions/agi/bin/alarm_spool.py STORES=$T/s WANTS=$T/w STATE=$T/st SPOOL=$T/spool SELF=belam TO=sanctuary-master U=1200 W=600 G=300 GAP=3600 sh $SW --repo $T/r 2>$T/err;}
# s1 (delta has no ~/o at all; it has no mail yet, so it is not named)
o=$(run);ok s1-no-unread-is-silent '[ -z "$o" ] && [ ! -e $T/spool ]'
# s2: alpha has mail from belam 30 min old, screen 15 min still
mail belam alpha $((NOW-1800)) >/dev/null;scr alpha $((NOW-900))
o=$(run);ok s2-mail-stall-named 'echo "$o" | grep -q "alpha: mail: 1 unread, oldest 30m, screen still 15m" && [ "$(grep -c stall-watch $T/spool 2>/dev/null)" -ge 1 ]'
# s3: beta has old mail but a fresh screen (busy)
rm -rf $T/st/*;mail belam beta $((NOW-1800)) >/dev/null;scr beta $((NOW-30))
o=$(run);ok s3-busy-screen-not-flagged '! echo "$o" | grep -q "beta:"'
# s4: gamma has young mail (5 min), still screen
c=$(mail belam gamma $((NOW-300)));scr gamma $((NOW-3000))
o=$(run);ok s4-young-mail-not-flagged '! echo "$o" | grep -q "gamma:"'
# s5: alpha's mail is held (read)
$G update-ref refs/held/alpha/belam $($G rev-parse refs/box/belam/alpha);rm -rf $T/st/*
o=$(run);ok s5-held-mail-is-read '! echo "$o" | grep -q "alpha:"'
# s6: beta's unit failed
echo failed>$T/sv/beta;o=$(run);ok s6-down-unit 'echo "$o" | grep -q "beta: down: unit failed"';echo active>$T/sv/beta
# s7: gamma has no claude, unit active 2 min (silent), then 10 min (flagged)
echo 0 >$T/sv/gamma.claude;echo $((NOW-120))>$T/sv/gamma.since;rm -rf $T/st/*
o=$(run);ok s7a-no-claude-within-grace-silent '! echo "$o" | grep -q "gamma:"'
echo $((NOW-600))>$T/sv/gamma.since;o=$(run);ok s7b-no-claude-past-grace 'echo "$o" | grep -q "gamma: no-claude: unit active 10m"'
echo 1 >$T/sv/gamma.claude
# s8: belam (SELF) with an old unread and a still screen is never listed
mail alpha belam $((NOW-5000)) >/dev/null;scr belam $((NOW-5000));rm -rf $T/st/*
o=$(run);ok s8-self-never-listed '! echo "$o" | grep -q "belam:"'
# s9: the same condition inside GAP is quiet; after GAP it repeats
echo failed>$T/sv/alpha;rm -rf $T/st/*;run >/dev/null
o=$(NOW=$((NOW+600)) run);ok s9a-same-condition-inside-gap-quiet '! echo "$o" | grep -q "alpha:"'
o=$(NOW=$((NOW+3700)) run);ok s9b-after-gap-repeats 'echo "$o" | grep -q "alpha: down"'
# s10: cleared then back = re-alert at once
echo active>$T/sv/alpha;NOW=$((NOW+3800)) run >/dev/null;echo failed>$T/sv/alpha
o=$(NOW=$((NOW+3900)) run);ok s10-cleared-then-back-realerts 'echo "$o" | grep -q "alpha: down"';echo active>$T/sv/alpha
# s11: no wants dir = unread rc 1
STORES=$T/s WANTS=$T/nope STATE=$T/st sh $SW --repo $T/r >/dev/null 2>$T/err;rc=$?
ok s11-no-wants-dir-unread-rc1 '[ $rc = 1 ] && grep -q unread $T/err'
# s12: DRY prints, writes no spool
echo failed>$T/sv/beta;rm -rf $T/st/*;n0=$(wc -l <$T/spool)
o=$(DRY=1 run);ok s12-dry-prints-no-spool 'echo "$o" | grep -q "beta: down" && [ "$(wc -l <$T/spool)" = "$n0" ]';echo active>$T/sv/beta
# s13 (row 1): delta has old unread mail and NO ~/o -> named unread
rm -rf $T/st/*;mail belam delta $((NOW-1800)) >/dev/null
o=$(run);ok s13-unreadable-screen-log-named 'echo "$o" | grep -q "delta: unread-screen: screen log not readable (mail 1 unread, oldest 30m)"'
# s14 (row 2): gamma no claude, EMPTY unit start time -> named unread (not midnight-based no-claude)
echo 0 >$T/sv/gamma.claude;echo empty>$T/sv/gamma.since;rm -rf $T/st/*
o=$(run);ok s14-unreadable-start-time-named 'echo "$o" | grep -q "gamma: unread-start: unit start time not readable (no claude process)"';echo 1 >$T/sv/gamma.claude
# s15 (row 3): a repo with no refs/box -> unread rc 1
git init -q $T/r0;STORES=$T/s WANTS=$T/w STATE=$T/st sh $SW --repo $T/r0 >/dev/null 2>$T/err;rc=$?
ok s15-no-box-refs-unread-rc1 '[ $rc = 1 ] && grep -q "unread: no refs/box" $T/err'
# s16 (row 4): an empty wants dir -> unread rc 1
mkdir -p $T/w0;STORES=$T/s WANTS=$T/w0 STATE=$T/st sh $SW --repo $T/r >/dev/null 2>$T/err;rc=$?
ok s16-empty-boot-set-unread-rc1 '[ $rc = 1 ] && grep -q "unread: boot set empty besides belam" $T/err'
# s17 (N1): a wants dir holding ONLY SELF -> unread rc 1
mkdir -p $T/w1;touch $T/w1/agi-post@belam.service;STORES=$T/s WANTS=$T/w1 STATE=$T/st sh $SW --repo $T/r >/dev/null 2>$T/err;rc=$?
ok s17-boot-set-only-self-unread-rc1 '[ $rc = 1 ] && grep -q "boot set empty besides belam" $T/err'
# s18 (N2): delta flagged unread-screen, then inside GAP its ~/o reads again but its start time garbles -> named again
rm -rf $T/st/*;run >/dev/null;scr delta $((NOW-900));echo 0 >$T/sv/delta.claude;echo empty>$T/sv/delta.since
o=$(NOW=$((NOW+60)) run);ok s18-cause-change-inside-gap-realerts 'echo "$o" | grep -q "delta: unread-start"';echo 1 >$T/sv/delta.claude;rm -f $T/sv/delta.since $T/s/delta/o
if [ -n "$MUT" ];then
 mk(){ python3 -c "import sys;s=open(sys.argv[1]).read();a=sys.argv[2];assert a in s;open(sys.argv[3],'w').write(s.replace(a,sys.argv[4],1))" $SW "$1" $T/$2 "$3";}
 mr(){ AS=$R0/extensions/agi/bin/alarm_spool.py STORES=$T/s WANTS=${MW:-$T/w} STATE=$T/st SPOOL=$T/spool SELF=belam U=1200 W=600 G=300 GAP=3600 sh $T/$1 --repo ${MR:-$T/r} 2>$T/err;}
 mk 'elif [ $((now-s)) -ge "$W" ];then' m1 'elif true;then';rm -rf $T/st/*
 o=$(mr m1);ok m1-mutant-no-screen-gate-flags-busy-beta-RED 'echo "$o" | grep -q "beta: mail"'
 sed 's/\[ "\$kind" = "\$lk" \]&&\[ \$((now-lt)) -lt "\$GAP" \]&&continue//' $SW>$T/m2;echo failed>$T/sv/alpha;rm -rf $T/st/*
 AS=$R0/extensions/agi/bin/alarm_spool.py STORES=$T/s WANTS=$T/w STATE=$T/st SPOOL=$T/spool SELF=belam GAP=3600 sh $T/m2 --repo $T/r >/dev/null 2>&1
 o=$(NOW=$((NOW+600)) AS=$R0/extensions/agi/bin/alarm_spool.py STORES=$T/s WANTS=$T/w STATE=$T/st SPOOL=$T/spool SELF=belam GAP=3600 sh $T/m2 --repo $T/r 2>/dev/null)
 ok m2-mutant-no-gap-gate-repeats-RED 'echo "$o" | grep -q "alpha: down"'
 mk 'then c="unread: screen log not readable (mail $k unread, oldest $(m $((now-o))))"' m3 'then :';rm -rf $T/st/*
 o=$(mr m3);ok m3-mutant-row1-dropped-silent-on-delta-RED '! echo "$o" | grep -q "delta:"'
 mk '[ -n "$ts" ]&&t=$(date -d "$ts" +%s 2>/dev/null)' m4 't=$(date -d "$ts" +%s 2>/dev/null)';echo 0 >$T/sv/gamma.claude;rm -rf $T/st/*
 o=$(mr m4);ok m4-mutant-row2-dropped-midnight-not-unread-RED '! echo "$o" | grep -q "gamma: unread"';echo 1 >$T/sv/gamma.claude
 mk '[ -n "$(git -C "$R" for-each-ref --count=1 refs/box)" ]||' m5 'true||';MR=$T/r0 mr m5 >/dev/null;rc=$?
 ok m5-mutant-row3-dropped-rc0-RED '[ $rc = 0 ]'
 mk '[ -n "$PS" ]||' m6 'true||';MW=$T/w0 mr m6 >/dev/null;rc=$?
 ok m6-mutant-row4-dropped-rc0-RED '[ $rc = 0 ]'
 mk '|grep -vx "$SELF")' m7 ')';MW=$T/w1 mr m7 >/dev/null;rc=$?
 ok m7-mutant-N1-dropped-only-self-rc0-RED '[ $rc = 0 ]'
 sed 's/c="unread-start:/c="unread-screen:/' $SW >$T/m8;rm -rf $T/st/*;mr m8 >/dev/null;scr delta $((NOW-900));echo 0 >$T/sv/delta.claude;echo empty>$T/sv/delta.since
 o=$(NOW=$((NOW+60)) mr m8);ok m8-mutant-N2-one-kind-quiet-RED '! echo "$o" | grep -q "delta:"';echo 1 >$T/sv/delta.claude;rm -f $T/sv/delta.since $T/s/delta/o
fi
echo "stall-watch: FAIL=$f";[ $f = 0 ]
