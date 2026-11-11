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
# (.46.35) the host's two hub files, every post on a SERVING hub B and never stale, so s1-s18 and m1-m8 read as landed
HUBDIR=$T/hub;HUBMAX=1000000000;export HUBDIR HUBMAX;mkdir -p $T/hub
hroute(){ { echo "written ${HW:-$NOW}";printf '%s\n' "$@";} >$T/hub/route;};hstate(){ { echo "written ${HW:-$NOW}";for l in "$@";do set -- $l;[ $# = 4 ]&&l="$l ${HL:-$NOW}";echo "$l";done;} >$T/hub/state;}   # LAST (field 5) = HL, default NOW
hroute 'alpha B claude-opus-5-5' 'beta B claude-opus-5-5' 'gamma B claude-opus-5-5' 'delta B claude-opus-5-5' 'belam direct';hstate "B claude-opus-5-5 ok $NOW"
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
# .46.35 HUB rows (goal:g7.16.1.11.46.35 at ba1e5e9e35: F2-F5, F8; the file shape agreed DG2 + belam 06:5xZ 11-11): fixture
# route/state files stand in for the host's; hub_quota.py (HQ=<file>, a mutant) says target (a)'s lines. No hub, 0 USD.
HQ=${HQ:-$R0/extensions/agi/bin/hub_quota.py};RS=$((NOW+3600));RH=$(date -u -d @$RS +%H:%MZ)
hq(){ python3 ${HQF:-$HQ} say --state $T/hub/state --memory $T/hqmem --said $T/said --spool $T/hspool --to sanctuary-master --now ${HNOW:-$NOW} "$@";}
for p in alpha beta gamma delta;do echo active>$T/sv/$p;echo 1 >$T/sv/$p.claude;done
mail delta alpha $((NOW-1800)) >/dev/null;mail delta gamma $((NOW-1800)) >/dev/null;for p in alpha beta gamma;do scr $p $((NOW-900));done
# s19 (F2 + sp/alive): hub A cools claude-opus-5-5. alpha (A, opus) = quota; beta (A, fable) and gamma (B, opus) keep mail:
hroute 'alpha A claude-opus-5-5' 'beta A claude-fable-5-2' 'gamma B claude-opus-5-5' 'delta B claude-opus-5-5' 'belam direct'
hstate "A claude-opus-5-5 quota $RS" "A claude-fable-5-2 ok $NOW" "B claude-opus-5-5 ok $NOW";rm -rf $T/st/*;o=$(run)
ok s19a-quota-named-not-mail 'echo "$o" | grep -q "alpha: quota: hub A (claude-opus-5-5) until $RH" && ! echo "$o" | grep -q "alpha: mail:"'
ok s19b-other-model-same-hub-not-quota 'echo "$o" | grep -q "beta: mail:" && ! echo "$o" | grep -q "beta: quota"'
ok s19c-same-model-other-hub-not-quota 'echo "$o" | grep -q "gamma: mail:" && ! echo "$o" | grep -q "gamma: quota"'
hstate "A claude-opus-5-5 quota 0";rm -rf $T/st/*;o=$(run)
ok s19d-no-reset-until-unknown 'echo "$o" | grep -q "alpha: quota: hub A (claude-opus-5-5) until unknown"'
hstate "A claude-opus-5-5 quota $((NOW-60))";rm -rf $T/st/*;o=$(run);PH=$(date -u -d @$((NOW-60)) +%H:%MZ)
ok s19e-past-reset-not-confirmed 'echo "$o" | grep -q "alpha: quota: hub A (claude-opus-5-5) reset $PH passed, not confirmed" && ! echo "$o" | grep -q "until $PH"'
# s20 (F3): a cooldown in the state -> ONE line (hub, model, reset) in the said file AND the spool; seen again = no 2nd line;
# reset 0 -> `until unknown`, never a guessed time
rm -f $T/hqmem $T/said $T/hspool;hstate "A claude-opus-5-5 quota $RS" "D claude-opus-5-5 quota 0";hq >/dev/null;hq >/dev/null
L="hub A (claude-opus-5-5) out of quota until $RH"
ok s20a-cooldown-said-once-human-and-spool '[ "$(grep -c "$L" $T/said)" = 1 ] && [ "$(grep -c "$L" $T/hspool)" = 1 ] && grep -q "\"job\":\"hub-quota\"" $T/hspool'
ok s20b-no-reset-until-unknown '[ "$(grep -c "hub D (claude-opus-5-5) out of quota until unknown" $T/said)" = 1 ]'
# s21 (F4): a host file unreadable / stale, no route row, or a hub route with no model id -> NAMED unread-hub:, rc 1, never quota
hstate "A claude-opus-5-5 quota $RS";rm -rf $T/st/*;mv $T/hub/state $T/hub/state.x;o=$(run);rc=$?;mv $T/hub/state.x $T/hub/state
ok s21a-state-missing-unread-hub-rc1 'echo "$o" | grep -q "alpha: unread-hub: $T/hub/state not readable" && [ $rc = 1 ] && ! echo "$o" | grep -q "alpha: quota"'
rm -rf $T/st/*;chmod 000 $T/hub/route;o=$(run);rc=$?;chmod 644 $T/hub/route
if [ "$(id -u)" = 0 ];then echo "ok s21b-route-mode-000-unread-hub-rc1 # SKIP root reads mode 000";else
ok s21b-route-mode-000-unread-hub-rc1 'echo "$o" | grep -q "alpha: unread-hub: $T/hub/route" && [ $rc = 1 ]';fi
HW=$((NOW-600)) hstate "A claude-opus-5-5 quota $RS";rm -rf $T/st/*;o=$(HUBMAX=180 run);rc=$?;hstate "A claude-opus-5-5 quota $RS"
ok s21c-stale-state-unread-hub-rc1 'echo "$o" | grep -q "alpha: unread-hub: $T/hub/state" && [ $rc = 1 ] && ! echo "$o" | grep -q "alpha: quota"'
hroute 'beta A claude-fable-5-2' 'gamma B claude-opus-5-5' 'delta B claude-opus-5-5' 'belam direct';rm -rf $T/st/*;o=$(run);rc=$?
ok s21d-no-route-row-unread-hub-rc1 'echo "$o" | grep -q "alpha: unread-hub: no route row for alpha" && [ $rc = 1 ]'
hroute 'alpha A' 'beta A claude-fable-5-2' 'gamma B claude-opus-5-5' 'delta B claude-opus-5-5' 'belam direct';rm -rf $T/st/*;o=$(run);rc=$?
ok s21e-unmapped-model-unread-hub-rc1 'echo "$o" | grep -q "alpha: unread-hub: alpha on hub A with no model id" && [ $rc = 1 ]'
hroute 'alpha A claude-opus-5-5' 'beta A claude-fable-5-2' 'gamma B claude-opus-5-5' 'delta B claude-opus-5-5' 'belam direct'
HW=$((NOW-600)) hstate "A claude-opus-5-5 ok $NOW";n0=$(wc -l <$T/said);hq >/dev/null 2>&1;rc=$?;hstate "A claude-opus-5-5 quota $RS"
ok s21f-say-on-stale-state-unread-rc1 '[ $rc = 1 ] && [ "$(wc -l <$T/said)" = "$n0" ]'
# s22 (F5): a recorded 200 after the cooldown -> ONE back line, then quiet; a reset passing with no 200 -> ONE not-confirmed, never back
B2=$((NOW+120));BH=$(date -u -d @$B2 +%H:%MZ);HW=$B2 hstate "A claude-opus-5-5 ok $B2";HNOW=$B2 hq >/dev/null;HNOW=$((B2+60)) HW=$B2 hq >/dev/null
ok s22a-back-said-once-then-quiet '[ "$(grep -c "hub A (claude-opus-5-5) back $BH" $T/said)" = 1 ] && [ "$(grep -c "hub A (claude-opus-5-5) back" $T/hspool)" = 1 ]'
rm -f $T/hqmem $T/said;E1=$((NOW+60));EH=$(date -u -d @$E1 +%H:%MZ);hstate "E claude-opus-5-5 quota $E1";hq >/dev/null
HW=$B2 hstate "E claude-opus-5-5 quota $E1";HNOW=$B2 hq >/dev/null;HNOW=$((B2+30)) hq >/dev/null
ok s22b-reset-passed-not-confirmed-once-no-back '[ "$(grep -c "hub E (claude-opus-5-5) reset $EH passed, not confirmed: no call since" $T/said)" = 1 ] && ! grep -q "hub E (claude-opus-5-5) back" $T/said'
# s23 (F8): hub A down (no upstream; the hub-wide `-` line, read FIRST) -> alpha (opus, a quota line too) and beta (fable, no line) read hub-down
hstate "A - hub-down $((NOW-600))" "A claude-opus-5-5 quota $RS";rm -rf $T/st/*;o=$(run);DH=$(date -u -d @$((NOW-600)) +%H:%MZ)
ok s23a-hub-down-named-not-quota-not-mail 'echo "$o" | grep -q "alpha: hub-down: hub A (no upstream) since $DH" && ! echo "$o" | grep -q -E "alpha: (quota|mail)"'
ok s23b-hub-down-any-model-on-the-hub 'echo "$o" | grep -q "beta: hub-down: hub A (no upstream) since $DH"'
# s24: a post routed `direct` keeps its symptom (mail:)
hroute 'alpha direct' 'beta A claude-fable-5-2' 'gamma B claude-opus-5-5' 'delta B claude-opus-5-5' 'belam direct';rm -rf $T/st/*;o=$(run)
ok s24-direct-route-keeps-mail 'echo "$o" | grep -q "alpha: mail: 1 unread"'
hroute 'alpha A claude-opus-5-5' 'beta A claude-fable-5-2' 'gamma B claude-opus-5-5' 'delta B claude-opus-5-5' 'belam direct';hstate "A claude-opus-5-5 quota $RS" "B claude-opus-5-5 ok $NOW"
# s25 (alive 06:50Z, LAST): the state's own age, not the timer's: LAST older than HUBMAX adds `, last seen HH:MMZ`; a quota line
# with no LAST is malformed = unread-hub; hub_quota says nothing on it (rc 1)
LH=$(date -u -d @$((NOW-600)) +%H:%MZ);HL=$((NOW-600)) hstate "A claude-opus-5-5 quota $RS";rm -rf $T/st/*;o=$(HUBMAX=180 run)
ok s25a-stale-last-adds-last-seen 'echo "$o" | grep -q "alpha: quota: hub A (claude-opus-5-5) until $RH, last seen $LH"'
hstate "A claude-opus-5-5 quota $RS";rm -rf $T/st/*;o=$(HUBMAX=180 run)
ok s25b-fresh-last-no-suffix 'echo "$o" | grep -q "alpha: quota: hub A (claude-opus-5-5) until $RH" && ! echo "$o" | grep -q "alpha: quota.*last seen"'
printf 'written %s\nA claude-opus-5-5 quota %s\n' $NOW $RS >$T/hub/state;rm -rf $T/st/*;o=$(run);rc=$?
ok s25c-no-last-unread-hub-rc1 'echo "$o" | grep -q "alpha: unread-hub: hub A (claude-opus-5-5) quota line not" && [ $rc = 1 ]'
n0=$(wc -l <$T/said);hq >/dev/null 2>&1;rc=$?
ok s25d-say-on-malformed-line-unread-rc1 '[ $rc = 1 ] && [ "$(wc -l <$T/said)" = "$n0" ]'
# s26 (F9, third child 667abfb390): the hub-wide `-` line appears -> ONE `hub A down (no upstream) since HH:MMZ` (said + spool);
# it goes with a 200 recorded -> ONE `hub A back HH:MMZ`; each then quiet
rm -f $T/hqmem $T/said $T/hspool;D0=$((NOW-600));DH=$(date -u -d @$D0 +%H:%MZ);hstate "A - hub-down $D0" "A claude-opus-5-5 ok $((NOW-900))";hq >/dev/null;hq >/dev/null
ok s26a-hub-down-said-once-human-and-spool '[ "$(grep -c "hub A down (no upstream) since $DH" $T/said)" = 1 ] && [ "$(grep -c "hub A down (no upstream)" $T/hspool)" = 1 ]'
HW=$B2 hstate "A claude-opus-5-5 ok $B2";HNOW=$B2 hq >/dev/null;HNOW=$((B2+60)) HW=$B2 hq >/dev/null
ok s26b-hub-back-said-once-then-quiet '[ "$(grep -c "hub A back $BH" $T/said)" = 1 ] && [ "$(grep -c "hub A back" $T/hspool)" = 1 ]'
# s27 (sp 06:49Z): still down but no hub log line for HUBMAX (LAST old) -> ONE `no failed dial since HH:MMZ, not confirmed back`, never back
rm -f $T/hqmem $T/said;hstate "A - hub-down $D0";hq >/dev/null;HW=$B2 HL=$D0 hstate "A - hub-down $D0";HNOW=$B2 hq >/dev/null;HNOW=$((B2+30)) HW=$B2 HL=$D0 hq >/dev/null
ok s27-no-failed-dial-not-confirmed-once-never-back '[ "$(grep -c "hub A no failed dial since $DH, not confirmed back" $T/said)" = 1 ] && ! grep -q "hub A back" $T/said'
L3=$((NOW-300));L3H=$(date -u -d @$L3 +%H:%MZ);rm -rf $T/st/*;HL=$L3 hstate "A - hub-down $D0";o=$(HUBMAX=180 run)
ok s23c-hub-down-stale-last-seen 'echo "$o" | grep -q "alpha: hub-down: hub A (no upstream) since $DH, last seen $L3H"'
hstate "A claude-opus-5-5 quota $RS" "B claude-opus-5-5 ok $NOW"
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
 # .46.35 mutants: each one a reader rule dropped; the row it names must read the wrong thing (= RED caught)
 echo active>$T/sv/alpha;rm -rf $T/st/*
 mk 'case ${c%%:*} in mail|unread-screen|no-claude)c=$(hub "$p" "$c");;esac' m9 ':'
 o=$(mr m9);ok m9-mutant-hub-read-dropped-reads-mail-RED 'echo "$o" | grep -q "alpha: mail:"'
 mk '$1==h&&$2==md&&$3=="quota"' m10 '$1==h&&$3=="quota"';rm -rf $T/st/*;hstate "A claude-opus-5-5 quota $RS" "B claude-opus-5-5 ok $NOW"
 o=$(mr m10);ok m10-mutant-model-ignored-beta-quota-RED 'echo "$o" | grep -q "beta: quota"'
 mk '$1==h&&$2==md&&$3=="quota"' m11 '$2==md&&$3=="quota"';rm -rf $T/st/*
 o=$(mr m11);ok m11-mutant-hub-ignored-gamma-quota-RED 'echo "$o" | grep -q "gamma: quota"'
 mk 'else echo "quota: hub $3 ($4) reset $(hz "$5") passed, not confirmed$(ls1 "$6")";fi' m12 'else echo "quota: hub $3 ($4) until $(hz "$5")$(ls1 "$6")";fi';hstate "A claude-opus-5-5 quota $((NOW-60))";rm -rf $T/st/*
 o=$(mr m12);ok m12-mutant-past-until-kept-RED 'echo "$o" | grep -q "alpha: quota: hub A (claude-opus-5-5) until $PH"'
 mk 'echo "unread-hub: $HUBDIR/$x not readable, unwritten or older than ${HUBMAX}s ($2)";return;' m13 'echo "$2";return;';hstate "A claude-opus-5-5 quota $RS";mv $T/hub/state $T/hub/state.x;rm -rf $T/st/*
 o=$(mr m13);rc=$?;mv $T/hub/state.x $T/hub/state;ok m13-mutant-unreadable-state-skipped-RED '! echo "$o" | grep -q "alpha: unread-hub" && [ $rc = 0 ]'
 mk '&&[ $((now-w2)) -lt "$HUBMAX" ];}' m14 ';}';HW=$((NOW-600)) hstate "A claude-opus-5-5 quota $RS";rm -rf $T/st/*
 o=$(HUBMAX=180 mr m14);hstate "A claude-opus-5-5 quota $RS";ok m14-mutant-stale-state-trusted-RED 'echo "$o" | grep -q "alpha: quota"'
 mk '[ -n "$4" ]||{ echo "unread-hub: $1 on hub $3 with no model id ($2)";return;}' m15 ':';hroute 'alpha A' 'beta A claude-fable-5-2' 'gamma B claude-opus-5-5' 'delta B claude-opus-5-5' 'belam direct';rm -rf $T/st/*
 o=$(mr m15);rc=$?;ok m15-mutant-unmapped-model-silent-RED '! echo "$o" | grep -q "alpha: unread-hub"'
 hroute 'alpha A claude-opus-5-5' 'beta A claude-fable-5-2' 'gamma B claude-opus-5-5' 'delta B claude-opus-5-5' 'belam direct'
 mk '$2=="-"&&$3=="hub-down"' m16 '$2=="-"&&$3=="never"';hstate "A - hub-down $((NOW-600))";rm -rf $T/st/*
 o=$(mr m16);ok m16-mutant-hub-down-ignored-reads-mail-RED 'echo "$o" | grep -q "alpha: mail:"'
 mk 'echo "hub-down: hub $3 (no upstream) since $(hz "$5")$(ls1 "$6")"' m17 'echo "quota: hub $3 ($4) until unknown"';rm -rf $T/st/*
 o=$(mr m17);ok m17-mutant-500-read-as-quota-RED 'echo "$o" | grep -q "alpha: quota"'
 hstate "A claude-opus-5-5 quota $RS" "B claude-opus-5-5 ok $NOW"
 mq(){ mkdir -p $T/$2;cp $R0/extensions/agi/bin/alarm_spool.py $T/$2/;python3 -c "import sys;s=open(sys.argv[1]).read();a=sys.argv[2];assert a in s;open(sys.argv[3],'w').write(s.replace(a,sys.argv[4],1))" $HQ "$1" $T/$2/hub_quota.py "$3";}
 mq 'say.append(f"{who} out of quota until' q1 'None and say.append(f"';rm -f $T/hqmem $T/said;HQF=$T/q1/hub_quota.py hq >/dev/null
 ok q1-mutant-cooldown-line-dropped-RED '! grep -q "hub A" $T/said 2>/dev/null'
 mq "hhmm(t) if t else 'unknown'" q2 'hhmm(t or now + 3600)';rm -f $T/hqmem $T/said;hstate "D claude-opus-5-5 quota 0";HQF=$T/q2/hub_quota.py hq >/dev/null
 ok q2-mutant-reset-invented-RED '! grep -q "hub D (claude-opus-5-5) out of quota until unknown" $T/said'
 mq 'say.append(f"{who} back {hhmm(t)}")' q3 'pass';rm -f $T/hqmem $T/said;hstate "A claude-opus-5-5 quota $RS";hq >/dev/null
 HW=$B2 hstate "A claude-opus-5-5 ok $B2";HNOW=$B2 HQF=$T/q3/hub_quota.py hq >/dev/null
 ok q3-mutant-back-never-sent-RED '! grep -q "hub A (claude-opus-5-5) back" $T/said'
 mq '            del mem[key]
            say.append(f"{who} back' q4 '            say.append(f"{who} back';rm -f $T/hqmem $T/said;hstate "A claude-opus-5-5 quota $RS";hq >/dev/null
 HW=$B2 hstate "A claude-opus-5-5 ok $B2";HNOW=$B2 HQF=$T/q4/hub_quota.py hq >/dev/null;HNOW=$((B2+60)) HW=$B2 HQF=$T/q4/hub_quota.py hq >/dev/null
 ok q4-mutant-back-repeats-RED '[ "$(grep -c "hub A (claude-opus-5-5) back" $T/said)" -gt 1 ]'
 mq 'say.append(f"{who} reset {hhmm(t)} passed, not confirmed: no call since")' q5 'say.append(f"{who} back {hhmm(t)}")';rm -f $T/hqmem $T/said
 hstate "E claude-opus-5-5 quota $E1";hq >/dev/null;HW=$B2 hstate "E claude-opus-5-5 quota $E1";HNOW=$B2 HQF=$T/q5/hub_quota.py hq >/dev/null
 ok q5-mutant-back-on-reset-passing-RED 'grep -q "hub E (claude-opus-5-5) back" $T/said'
 mk '[ -z "$5" ]||{ num "$5"&&num "$6";}||' m18 '[ -z "$5" ]||num "$5"||';printf 'written %s\nA claude-opus-5-5 quota %s\n' $NOW $RS >$T/hub/state;rm -rf $T/st/*
 o=$(mr m18);ok m18-mutant-last-unchecked-reads-quota-RED 'echo "$o" | grep -q "alpha: quota"';hstate "A claude-opus-5-5 quota $RS" "B claude-opus-5-5 ok $NOW"
 mk 'ls1(){ [ $((now-$1)) -ge "$HUBMAX" ]&&echo' m19 'ls1(){ false&&echo';HL=$((NOW-600)) hstate "A claude-opus-5-5 quota $RS";rm -rf $T/st/*
 o=$(HUBMAX=180 mr m19);ok m19-mutant-stale-last-unsaid-RED '! echo "$o" | grep -q "last seen"';hstate "A claude-opus-5-5 quota $RS" "B claude-opus-5-5 ok $NOW"
 mk '$2=="-"&&$3=="hub-down"{print $4,$5,"x";exit}' m20 '$2=="-"&&$3=="hub-down"{print $4,$4,"x";exit}';rm -rf $T/st/*;HL=$L3 hstate "A - hub-down $D0"   # sp 06:56Z: LAST by NAME
 o=$(HUBMAX=180 mr m20);ok m20-mutant-T-read-as-LAST-RED '! echo "$o" | grep -q "last seen $L3H"'
 mk '$2==md&&$3=="quota"{print $4,$5,"x";exit}' m21 '$2==md&&$3=="quota"{print $4,$4,"x";exit}';rm -rf $T/st/*;HL=$((NOW-600)) hstate "A claude-opus-5-5 quota $RS"
 o=$(HUBMAX=180 mr m21);ok m21-mutant-reset-read-as-LAST-RED '! echo "$o" | grep -q "last seen $LH"';hstate "A claude-opus-5-5 quota $RS" "B claude-opus-5-5 ok $NOW"
 mq 'say.append(f"hub {hub} down (no upstream) since {hhmm(t)}")' q6 'pass';rm -f $T/hqmem $T/said;hstate "A - hub-down $D0";HQF=$T/q6/hub_quota.py hq >/dev/null
 ok q6-mutant-hub-down-not-said-RED '! grep -q "hub A down" $T/said 2>/dev/null'
 mq '                mem[key] = {"since": t, "said": "down"}
' q7 '';rm -f $T/hqmem $T/said;HQF=$T/q7/hub_quota.py hq >/dev/null;HQF=$T/q7/hub_quota.py hq >/dev/null
 ok q7-mutant-down-line-repeats-RED '[ "$(grep -c "hub A down" $T/said)" -gt 1 ]'
 mq 'elif m["said"] == "down" and now - last >= max_age:' q8 'elif False:';rm -f $T/hqmem $T/said;hstate "A - hub-down $D0";HQF=$T/q8/hub_quota.py hq >/dev/null
 HW=$B2 HL=$D0 hstate "A - hub-down $D0";HNOW=$B2 HQF=$T/q8/hub_quota.py hq >/dev/null
 ok q8-mutant-down-kept-no-failed-dial-RED '! grep -q "not confirmed back" $T/said'
 hstate "A claude-opus-5-5 quota $RS" "B claude-opus-5-5 ok $NOW"
fi
echo "stall-watch: FAIL=$f";[ $f = 0 ]
