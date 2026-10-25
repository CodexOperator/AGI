#!/bin/sh
# stall-watch.t.sh: config:crons stall_watch (owner 01:1xZ 10-25). Runs extensions/agi/bin/stall_watch.sh (or SW=<file>, a
# mutant) on a SCRATCH repo with mail refs made by plain commits, a fake wants dir, fake ~/o files dated with touch -d, and
# systemctl/pgrep stubs on PATH (state from files under $T). NOW is fixed; no live ref, no network, no root, 0 USD.
# Lanes: s1 no unread = silent · s2 mail stall (old unread, still screen) = one named line + one spool line · s3 a busy
# screen (fresh ~/o) is not flagged · s4 young mail (< U) is not flagged · s5 held mail is read, not unread · s6 a unit not
# active = down · s7 no claude past G = no-claude, within G silent · s8 SELF is never listed · s9 the same condition inside
# GAP is quiet, after GAP it repeats · s10 cleared then back = re-alert · s11 a missing wants dir = unread, rc 1 ·
# s12 DRY prints and writes no spool. MUTANTS (MUT=1): the screen gate dropped (s3 must go RED) and the GAP gate dropped
# (s9 must go RED).
T=$(mktemp -d);f=0;R0=$(cd "$(dirname "$0")/../../.." && pwd);SW=${SW:-$R0/extensions/agi/bin/stall_watch.sh}
trap "[ -n \"$KEEP\" ] || rm -rf $T" 0
ok(){ if eval "$2";then echo "ok $1";else echo "FAIL $1";f=$((f+1));fi;}
unset GIT_DIR GIT_WORK_TREE AGI_TRUNK AGI_POST DRY
NOW=2000000000;export NOW
mkdir -p $T/bin $T/w $T/st $T/s $T/sv
for p in belam alpha beta gamma;do touch $T/w/agi-post@$p.service;mkdir -p $T/s/$p;echo active>$T/sv/$p;echo 1 >$T/sv/$p.claude;done
# stubs: systemctl show agi-post@P.service -p ActiveState|ActiveEnterTimestamp --value ; pgrep -u agi-P -x claude
cat >$T/bin/systemctl <<EOF
#!/bin/sh
p=\${2#agi-post@};p=\${p%.service}
case \$4 in ActiveState)cat $T/sv/\$p;;ActiveEnterTimestamp)date -u -d @\$(cat $T/sv/\$p.since 2>/dev/null||echo 1000000000) '+%a %Y-%m-%d %H:%M:%S UTC';;esac
EOF
cat >$T/bin/pgrep <<EOF
#!/bin/sh
p=\${2#agi-};[ "\$(cat $T/sv/\$p.claude)" = 1 ]&&echo 4242
EOF
chmod +x $T/bin/*;PATH=$T/bin:$PATH;export PATH
git init -q $T/r;G="git -C $T/r -c user.name=t -c user.email=t@t"
mail(){ c=$(GIT_COMMITTER_DATE="@$3 +0000" GIT_AUTHOR_DATE="@$3 +0000" $G commit-tree -m "m" $($G hash-object -w -t tree /dev/null) ${4:+-p $4});$G update-ref refs/box/$1/$2 $c;echo $c;}
scr(){ touch -d @$2 $T/s/$1/o;}
for p in alpha beta gamma belam;do scr $p $NOW;done
run(){ AS=$R0/extensions/agi/bin/alarm_spool.py STORES=$T/s WANTS=$T/w STATE=$T/st SPOOL=$T/spool SELF=belam TO=sanctuary-master U=1200 W=600 G=300 GAP=3600 sh $SW --repo $T/r 2>$T/err;}
# s1
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
if [ -n "$MUT" ];then
 sed 's/&&\[ \$((now-s)) -ge "\$W" \]//' $SW>$T/m1;rm -rf $T/st/*;o=$(SW=$T/m1;STORES=$T/s WANTS=$T/w STATE=$T/st SPOOL=$T/spool SELF=belam U=1200 W=600 G=300 GAP=3600 sh $T/m1 --repo $T/r 2>/dev/null)
 ok m1-mutant-no-screen-gate-flags-busy-beta-RED 'echo "$o" | grep -q "beta: mail"'
 sed 's/\[ "\$kind" = "\$lk" \]&&\[ \$((now-lt)) -lt "\$GAP" \]&&continue//' $SW>$T/m2;echo failed>$T/sv/alpha;rm -rf $T/st/*
 AS=$R0/extensions/agi/bin/alarm_spool.py STORES=$T/s WANTS=$T/w STATE=$T/st SPOOL=$T/spool SELF=belam GAP=3600 sh $T/m2 --repo $T/r >/dev/null 2>&1
 o=$(NOW=$((NOW+600)) AS=$R0/extensions/agi/bin/alarm_spool.py STORES=$T/s WANTS=$T/w STATE=$T/st SPOOL=$T/spool SELF=belam GAP=3600 sh $T/m2 --repo $T/r 2>/dev/null)
 ok m2-mutant-no-gap-gate-repeats-RED 'echo "$o" | grep -q "alpha: down"'
fi
echo "stall-watch: FAIL=$f";[ $f = 0 ]
