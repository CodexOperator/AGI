#!/bin/sh
# agi-kid-flow-p.t.sh: W-1 residue R2 (DG1 04:16Z), the part DG3's guard file does not pin: the output PREFIX P is EXTENDED per nested call, so a sub-flow named by TWO stages runs ONCE PER CALL with SEPARATE outputs (a runner that forgets to extend P makes the second call find the first call's output "done" and launch nothing).
# Same harness as agi-kid-flow-guard.t.sh (sh + git + jq + ssh-keygen, scratch HOME, a stub pi/box, 0 USD). PIECE = the file under test (default: `sect agi-kid` of ROOT; a mutation = PIECE=<edited copy>). One ok/FAIL line per case; exit = number of FAILs.
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
w sub '{"name":"sub","stages":[{"label":"x","prompt":"SUBX"}]}'
w twice '{"name":"twice","stages":[{"label":"a","flow":"sub"},{"label":"b","flow":"sub"}]}'
w once '{"name":"once","stages":[{"label":"a","flow":"sub"}]}'
w deep '{"name":"deep","stages":[{"label":"a","flow":"mid"},{"label":"b","flow":"mid"}]}'
w mid '{"name":"mid","stages":[{"label":"m","flow":"sub"}]}'
$G -C $H/t add -A;$G -C $H/t -c commit.gpgsign=false commit -qm fixture
flow(){ (cd $T;HOME=$H GIT_CONFIG_GLOBAL=$H/.gitconfig GIT_CONFIG_SYSTEM=/dev/null PATH=$T/bin:$PATH LOG=$LOG AGI_POST=inv sh $PIECE -m "$1" "$2");}
nl(){ wc -l<$1|tr -d ' ';}
refs(){ $G -C $H/t for-each-ref --format='%(refname)' refs/spawn/;}
: >$LOG;flow once '{}'>/dev/null 2>&1;rc=$?
ok "p0-control-once a flow that names the sub-flow ONCE launches it once and signs one ref (rc=$rc, launches $(nl $LOG))" '[ $rc = 0 ]&&[ "$(nl $LOG)" = 1 ]'
: >$LOG;flow twice '{}'>/dev/null 2>&1;rc=$?
ok "p1-same-subflow-twice a flow whose TWO stages name the same sub-flow launches it once per call (rc=$rc, launches $(nl $LOG), want 2)" '[ $rc = 0 ]&&[ "$(nl $LOG)" = 2 ]'
r=$(refs|grep twice|head -1);fl=$($G -C $H/t ls-tree -r --name-only $r 2>/dev/null)
ok "p2-separate-outputs the result ref of that run holds TWO separate sub-flow outputs (files: $(echo $fl|tr '\n' ' '))" '[ "$(echo "$fl"|grep -c "x$")" = 2 ]'
: >$LOG;flow deep '{}'>/dev/null 2>&1;rc=$?
ok "p3-nested-twice two stages each naming a mid flow that names the sub-flow launch the leaf once per path (rc=$rc, launches $(nl $LOG), want 2)" '[ $rc = 0 ]&&[ "$(nl $LOG)" = 2 ]'
echo "agi-kid-flow-p: $f FAIL"
exit $f
