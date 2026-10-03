#!/bin/sh
# agi-kid-flow-guard.t.sh: W-1 CORRECTIVE (security mur sm17 DEMOTE D1-D5 + multi-line prompts) beside DG2's agi-kid-flow.t.sh (the happy path, untouched): the runner `agi-kid -m MANIFEST ARGS` must fail CLOSED.
# sh + git + jq + ssh-keygen only, scratch HOME, throwaway keys, 0 USD. PIECE = the file under test (default: `sect agi-kid` of ROOT). One ok/FAIL line per case; exit = number of FAILs.
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
n=$(wc -l<$LOG);echo "$p">$LOG.p$((n+1));echo "launch $(echo "$p"|head -1)">>$LOG;echo "result"
XX2
printf '#!/bin/sh\necho "$*">>%s\n' $MAIL>$T/bin/box;chmod +x $T/bin/*
export GIT_CONFIG_GLOBAL=$H/.gitconfig GIT_CONFIG_SYSTEM=/dev/null
mkdir -p $H/t/extensions/agi/workflows $H/t/.agi/nodes/goal;$G init -q $H/t
w(){ printf '%s\n' "$2">$H/t/extensions/agi/workflows/$1.json;}
gl(){ printf -- '---\nid: goal:%s\ntype: goal\nstatus: active\n---\n# goal:%s\n\n## Falsifier\n%s\n\n## Out of scope\nnothing\n' $1 $1 "$2">$H/t/.agi/nodes/goal/$1.md;}
gp(){ w g-$1 '{"name":"g-'$1'","stages":[{"label":"grow","post":"director-general-1","goal":"gk-'$1'"},{"label":"after","prompt":"SHOULD-NOT-RUN"}]}';}
# D1 a literal backslash-n in the line (dash echo expands it), D2 the writing / executing git forms, a git form that IS whitelisted and met
gl gk-bs '$ ls x\n; touch pwn-bs';gl gk-log '$ git log --output=pwn-log -1';gl gk-grep "\$ git grep -O'touch pwn-grep' x";gl gk-diff '$ git diff --no-index --output=pwn-diff /dev/null /dev/null';gl gk-ok '$ git ls-files extensions'
for g in bs log grep diff ok;do gp $g;done
w one '{"name":"one","stages":[{"label":"solo","prompt":"LINE1\nLINE2 tab\there"}]}'
w fan '{"name":"fan","stages":[{"label":"review","repeat":{"of":"rounds","label_template":"review:{key}"},"prompt":"REVIEW {key}"}]}'
w empty '{"name":"empty","stages":[]}'
w selfie '{"name":"selfie","stages":[{"label":"a","flow":"selfie"}]}'
w cyc-a '{"name":"cyc-a","stages":[{"label":"p","prompt":"P"},{"label":"b","flow":"cyc-b"}]}'
w cyc-b '{"name":"cyc-b","stages":[{"label":"a","flow":"cyc-a"}]}'
$G -C $H/t add -A;$G -C $H/t -c commit.gpgsign=false commit -qm fixture
flow(){ (cd $T;HOME=$H GIT_CONFIG_GLOBAL=$H/.gitconfig GIT_CONFIG_SYSTEM=/dev/null PATH=$T/bin:$PATH LOG=$LOG AGI_POST=inv sh $PIECE -m "$1" "$2");}
nl(){ wc -l<$1|tr -d ' ';}
refs(){ $G -C $H/t for-each-ref --format='%(refname)' refs/spawn/;}
pwn(){ ls $H/t/pwn-* $T/pwn-* $H/pwn-* 2>/dev/null;}
# --- D1/D2: a goal line that smuggles a command (backslash-n, git --output, git grep -O, --no-index) is NOT met: rc 75, nothing launched, no file written, no ref
for g in bs log grep diff;do : >$LOG;flow g-$g '{}'>/dev/null 2>&1;rc=$?
 ok "d12-$g the goal line of g-$g is refused, never run: rc 75, no launch, no pwn-* file, no ref (rc=$rc)" '[ $rc = 75 ]&&[ "$(nl $LOG)" = 0 ]&&[ -z "$(pwn)" ]&&[ -z "$(refs)" ]'
done
# the whitelisted read-only git form still reads as met: the flow passes the post phase and runs the next stage
: >$LOG;flow g-ok '{}'>/dev/null 2>&1;rc=$?
ok "d2-whitelisted-met a whitelisted read-only line (git ls-files) is run and reads met: the flow goes on (rc=$rc, launches $(nl $LOG))" '[ $rc = 0 ]&&[ "$(nl $LOG)" = 1 ]'
# --- D3: a missing manifest, unparseable ARGS and a manifest with no rows fail closed: nonzero, no spawn, NO ref
: >$LOG;n0=$(refs|wc -l|tr -d ' ')
flow nomanifest '{}'>/dev/null 2>&1;rc1=$?;flow one 'not json'>/dev/null 2>&1;rc2=$?;flow empty '{}'>/dev/null 2>&1;rc3=$?
ok "d3-fail-closed missing manifest (rc=$rc1), bad ARGS (rc=$rc2) and zero rows (rc=$rc3) all exit nonzero, launch nothing and write no ref" '[ $rc1 != 0 ]&&[ $rc2 != 0 ]&&[ $rc3 != 0 ]&&[ "$(nl $LOG)" = 0 ]&&[ "$(refs|wc -l|tr -d " ")" = $n0 ]'
# --- D4: keys with a space, a glob and a newline: one launch per key, each DONE only after it ran, no forged rows, a re-run launches nothing
: >$LOG;A='{"rounds":[{"key":"a b"},{"key":"c*"},{"key":"x\nstage"}]}'
flow fan "$A">/dev/null 2>&1;rc=$?;L1=$(grep -c '^launch REVIEW' $LOG)
ok "d4-odd-keys three odd keys (space, glob, newline) give exactly three launches and one ref (rc=$rc, launches $L1)" '[ $rc = 0 ]&&[ "$L1" = 3 ]&&[ "$(refs|wc -l|tr -d " ")" = $((n0+1)) ]'
rm -rf $H/t/.git/refs/spawn;$G -C $H/t update-ref -d $(refs|head -1) 2>/dev/null;flow fan "$A">/dev/null 2>&1
ok "d4-resume-launches-nothing with the state kept and the ref gone, the re-run launches nothing new (launches $(grep -c '^launch REVIEW' $LOG), want 3)" '[ "$(grep -c "^launch REVIEW" $LOG)" = 3 ]'
# --- multi-line prompt: a prompt holding a newline and a tab reaches the kid whole, in ONE launch
: >$LOG;flow one '{}'>/dev/null 2>&1;rc=$?
ok "ml-prompt a manifest prompt with a newline and a tab is ONE launch and the kid sees both lines (rc=$rc)" '[ $rc = 0 ]&&[ "$(nl $LOG)" = 1 ]&&grep -q "^LINE2 tab	here" $LOG.p1'
# --- recursion: a flow that names itself, or two that name each other, stops at the depth guard: nonzero, inside timeout 20 (124 = a runaway), no ref
: >$LOG;n1=$(refs|wc -l|tr -d ' ')
( cd $T;HOME=$H GIT_CONFIG_GLOBAL=$H/.gitconfig GIT_CONFIG_SYSTEM=/dev/null PATH=$T/bin:$PATH LOG=$LOG AGI_POST=inv timeout 20 sh $PIECE -m selfie '{}' )>/dev/null 2>&1;rc1=$?
( cd $T;HOME=$H GIT_CONFIG_GLOBAL=$H/.gitconfig GIT_CONFIG_SYSTEM=/dev/null PATH=$T/bin:$PATH LOG=$LOG AGI_POST=inv timeout 20 sh $PIECE -m cyc-a '{}' )>/dev/null 2>&1;rc2=$?
ok "rec-guard a self-naming flow (rc=$rc1) and a 2-cycle (rc=$rc2) stop nonzero and not by the 20 s timeout (124), and write no ref" '[ $rc1 != 0 ]&&[ $rc1 != 124 ]&&[ $rc2 != 0 ]&&[ $rc2 != 124 ]&&[ "$(refs|wc -l|tr -d " ")" = $n1 ]'
# --- D5: a manifest name outside [a-z0-9-] is refused before anything is created
rm -rf $H/s;flow '../t' '{}'>/dev/null 2>&1;rc1=$?;flow 'One' '{}'>/dev/null 2>&1;rc2=$?;flow 'a b' '{}'>/dev/null 2>&1;rc3=$?
ok "d5-name-refused names '../t', 'One' and 'a b' exit nonzero and create nothing under ~/s (rc $rc1 $rc2 $rc3)" '[ $rc1 != 0 ]&&[ $rc2 != 0 ]&&[ $rc3 != 0 ]&&[ ! -e $H/s ]'
ok "bytes the piece is <= ${CEIL:-1856} B ($(wc -c<$PIECE) B)" '[ $(wc -c<$PIECE) -le ${CEIL:-1856} ]'
echo "agi-kid-flow-guard: $f FAIL"
exit $f
