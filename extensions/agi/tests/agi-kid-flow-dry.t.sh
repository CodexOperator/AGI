#!/bin/sh
# agi-kid-flow-dry.t.sh: W-1.11 mur residues R1/R2 (DG1 05:29Z), the DRY PASS: `agi-kid -m` walks the whole manifest ONCE without launching or mailing (V=1), THEN runs it; what the dry pass must catch it must catch BEFORE a paid stage is launched, and what it must not touch it must not touch.
# (a) a chained_from that names no label of the manifest refuses with launches 0 (a paid stage 'a', then 'b' chained_from 'nothere': today 'a' is paid for and THEN the run dies);
# (b) a paid stage followed by an UNMET post: gate = exactly 1 paid launch, 1 mail, rc 75 (the dry pass SKIPS the post: line; the live pass hands off once);
# (c) the lane that goes RED when the dry pass stops skipping the post: line is (b) (the dry pass would hand off and stop at 75 BEFORE the paid stage: 0 launches).
# Same harness as agi-kid-flow-guard.t.sh / agi-kid-flow-p.t.sh (sh + git + jq + ssh-keygen, scratch HOME, a stub pi/box, 0 USD). PIECE = the file under test (default: `sect agi-kid` of ROOT; a mutation = PIECE=<edited copy>). One ok/FAIL line per case; exit = number of FAILs.
T=$(mktemp -d);trap 'rm -rf $T' 0;f=0;G=/usr/bin/git;R0=${ROOT:-$(cd "$(dirname "$0")/../../.." && pwd)}
sect(){ cat $R0/.agi/nodes/.geometry/engine*.md|sed -n "/^###* $1 /,/^###* /{/^~~~/,/^~~~/{//!p}}";}
[ -n "$PIECE" ]||{ sect agi-kid>$T/piece;PIECE=$T/piece;}
[ -s $PIECE ]||{ echo "FAIL extract: agi-kid $(wc -c<$PIECE) B";exit 99;}
ok(){ if eval "$2";then echo "ok $1";else echo "FAIL $1";f=$((f+1));fi;}
unset GIT_AUTHOR_NAME GIT_AUTHOR_EMAIL GIT_COMMITTER_NAME GIT_COMMITTER_EMAIL GIT_DIR GIT_WORK_TREE;H=$T/home;mkdir -p $H/.ssh $T/bin;LOG=$T/log;: >$LOG;MAIL=$T/mail;: >$MAIL
ssh-keygen -q -t ed25519 -N '' -f $H/.ssh/id_ed25519 -C inv>/dev/null;echo "inv@agi namespaces=\"git\" $(cut -d' ' -f1,2 $H/.ssh/id_ed25519.pub)">$T/allowed
printf '[user]\n\tname=inv\n\temail=inv@agi\n\tsigningkey=%s\n[gpg]\n\tformat=ssh\n[gpg "ssh"]\n\tallowedSignersFile=%s\n[commit]\n\tgpgsign=true\n[safe]\n\tdirectory=*\n' $H/.ssh/id_ed25519 $T/allowed>$H/.gitconfig
cat >$T/bin/pi<<'XX2'
#!/bin/sh
p=;while [ $# -gt 0 ];do [ "$1" = -p ]&&p=$2;shift;done
echo "launch $(echo "$p"|head -1)">>$LOG;echo "result($(echo "$p"|head -1))"
XX2
printf '#!/bin/sh\necho "$*">>%s\n' $MAIL>$T/bin/box;chmod +x $T/bin/*
export GIT_CONFIG_GLOBAL=$H/.gitconfig GIT_CONFIG_SYSTEM=/dev/null
mkdir -p $H/t/extensions/agi/workflows $H/t/.agi/nodes/goal;$G init -q $H/t
w(){ printf '%s\n' "$2">$H/t/extensions/agi/workflows/$1.json;}
printf -- '---\nid: goal:gk-later\ntype: goal\nstatus: active\n---\n# goal:gk-later\n\n## Falsifier\n$ test -e GROWN\n\n## Out of scope\nnothing\n'>$H/t/.agi/nodes/goal/gk-later.md
w chain-ok '{"name":"chain-ok","stages":[{"label":"a","prompt":"PAID-A"},{"label":"b","chained_from":"a","prompt":"PAID-B"}]}'
w chain-miss '{"name":"chain-miss","stages":[{"label":"a","prompt":"PAID-A"},{"label":"b","chained_from":"nothere","prompt":"PAID-B"}]}'
w chain-miss-sub '{"name":"chain-miss-sub","stages":[{"label":"a","prompt":"PAID-A"},{"label":"s","flow":"chain-miss-in"}]}'
w chain-miss-in '{"name":"chain-miss-in","stages":[{"label":"x","chained_from":"nothere","prompt":"PAID-X"}]}'
w paid-post '{"name":"paid-post","stages":[{"label":"a","prompt":"PAID-A"},{"label":"p","post":"director-general-1","goal":"gk-later"}]}'
$G -C $H/t add -A;$G -C $H/t -c commit.gpgsign=false commit -qm fixture
flow(){ (cd $T;HOME=$H GIT_CONFIG_GLOBAL=$H/.gitconfig GIT_CONFIG_SYSTEM=/dev/null PATH=$T/bin:$PATH LOG=$LOG AGI_POST=inv sh $PIECE -m "$1" "$2");}
nl(){ wc -l<$1|tr -d ' ';}
refs(){ $G -C $H/t for-each-ref --format='%(refname)' refs/spawn/;}
fresh(){ rm -rf $H/t/.git/refs/spawn $H/s $H/t/GROWN;: >$LOG;: >$MAIL;}
fresh;flow chain-ok '{}'>/dev/null 2>&1;rc=$?
ok "y0-control-chain-ok a stage 'b' chained_from the label 'a' runs both: 2 launches, rc 0, one ref (rc=$rc, launches $(nl $LOG))" '[ $rc = 0 ]&&[ "$(nl $LOG)" = 2 ]&&[ "$(refs|wc -l|tr -d " ")" = 1 ]'
fresh;flow chain-miss '{}'>/dev/null 2>&1;rc=$?
ok "a1-chained-from-no-label-refuses-before-paying a paid 'a' then 'b' chained_from 'nothere': nonzero, ZERO launches (the dry pass refuses before 'a' is paid for), no mail, no ref (rc=$rc, launches $(nl $LOG), mail $(nl $MAIL))" '[ $rc != 0 ]&&[ "$(nl $LOG)" = 0 ]&&[ "$(nl $MAIL)" = 0 ]&&[ -z "$(refs)" ]'
fresh;flow chain-miss-sub '{}'>/dev/null 2>&1;rc=$?
ok "a2-same-in-a-subflow the same bad chained_from inside a SUB-flow stage after a paid 'a' also refuses before 'a' is paid: nonzero, 0 launches (rc=$rc, launches $(nl $LOG))" '[ $rc != 0 ]&&[ "$(nl $LOG)" = 0 ]&&[ -z "$(refs)" ]'
fresh;flow paid-post '{}'>/dev/null 2>&1;rc=$?
ok "b1-paid-then-unmet-post a paid 'a' then a post: stage whose goal is unmet: exactly 1 paid launch, 1 mail, rc 75 (rc=$rc, launches $(nl $LOG), mail $(nl $MAIL))" '[ $rc = 75 ]&&[ "$(nl $LOG)" = 1 ]&&[ "$(nl $MAIL)" = 1 ]'
ok "b2-pending-no-ref the pending run signed no ref" '[ -z "$(refs)" ]'
flow paid-post '{}'>/dev/null 2>&1;rc=$?
ok "b3-rerun-pending-no-second-launch-or-mail the same run again while the goal is still unmet: rc 75, still 1 launch and 1 mail in all (the paid 'a' is DONE, the hand-off is once)" '[ $rc = 75 ]&&[ "$(nl $LOG)" = 1 ]&&[ "$(nl $MAIL)" = 1 ]'
: >$H/t/GROWN;flow paid-post '{}'>/dev/null 2>&1;rc=$?
ok "b4-goal-met-finishes once the goal reads met the run again finishes: rc 0, still 1 launch in all, one ref (rc=$rc, launches $(nl $LOG))" '[ $rc = 0 ]&&[ "$(nl $LOG)" = 1 ]&&[ "$(refs|wc -l|tr -d " ")" = 1 ]'
echo "agi-kid-flow-dry: $f FAIL"
exit $f
