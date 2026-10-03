#!/bin/sh
# agi-kid-flow.t.sh: W-1 (hypothesis g716111-z4-phase-w-...; doc:radically-simple-engine AA2 ONE-SHOT SPAWN + FLOW ROTATION, doc:rse-z4-ladder-out Z4.8 + GUARD): the runner `agi-kid -m MANIFEST ARGS`.
# sh + git + jq + ssh-keygen only, scratch HOME, throwaway keys, 0 USD. THE SEAMS THIS TEST PINS (a builder may not move them): the kid is whatever `pi` resolves to on PATH (stubbed here), a hand-off is
# `box send POST "handoff ..."` (`box` on PATH, stubbed here), the invoker is $AGI_POST with its repo at ~/t (HEAD = its tip: manifests live at extensions/agi/workflows/<name>.json, goals at .agi/nodes/goal/<id>.md),
# the result ref lands in ~/t as refs/spawn/<manifest>/<sha256(ARGS)[:12]> (ARGS = the bytes of the 2nd argument). Where a runner keeps its phase outputs / markers is NOT pinned (a black box).
# PIECE = the file under test (default: `sect agi-kid` from .geometry/engine-wrap.md of ROOT); a mutation = PIECE=<edited copy>. One ok/FAIL line per case; exit = number of FAILs.
T=$(mktemp -d);trap 'rm -rf $T' 0;f=0;G=/usr/bin/git;R0=${ROOT:-$(cd "$(dirname "$0")/../../.." && pwd)};CEIL=${CEIL:-1856}
sect(){ cat $R0/.agi/nodes/.geometry/engine*.md|sed -n "/^###* $1 /,/^###* /{/^~~~/,/^~~~/{//!p}}";}
[ -n "$PIECE" ]||{ sect agi-kid>$T/piece;PIECE=$T/piece;}
[ -s $PIECE ]||{ echo "FAIL extract: agi-kid $(wc -c<$PIECE) B";exit 99;}
ok(){ if eval "$2";then echo "ok $1";else echo "FAIL $1";f=$((f+1));fi;}
unset GIT_AUTHOR_NAME GIT_AUTHOR_EMAIL GIT_COMMITTER_NAME GIT_COMMITTER_EMAIL GIT_DIR GIT_WORK_TREE;H=$T/home;mkdir -p $H/.ssh $T/bin;LOG=$T/log;: >$LOG;MAIL=$T/mail;: >$MAIL
ssh-keygen -q -t ed25519 -N '' -f $H/.ssh/id_ed25519 -C inv>/dev/null;echo "inv@agi namespaces=\"git\" $(cut -d' ' -f1,2 $H/.ssh/id_ed25519.pub)">$T/allowed
printf '[user]\n\tname=inv\n\temail=inv@agi\n\tsigningkey=%s\n[gpg]\n\tformat=ssh\n[gpg "ssh"]\n\tallowedSignersFile=%s\n[commit]\n\tgpgsign=true\n[safe]\n\tdirectory=*\n' $H/.ssh/id_ed25519 $T/allowed>$H/.gitconfig
# the stub kid: logs its first prompt line, probes what a one-shot may hold (Z4.g), prints a result derived from the prompt; FAILON=<first line> makes that one fail
cat >$T/bin/pi<<'XX'
#!/bin/sh
p=;while [ $# -gt 0 ];do [ "$1" = -p ]&&p=$2;shift;done;l=$(echo "$p"|head -1)
n=$(wc -l<$LOG);echo "$p">$LOG.p$((n+1))
git commit -q --allow-empty -m kid 2>/dev/null;kc=$?
echo "launch $l|ssh=$([ -e $HOME/.ssh ]&&echo present||echo absent)|gitdir=$([ -e .git ]&&echo present||echo absent)|kidcommit=$kc">>$LOG
[ "$l" = "$FAILON" ]&&exit 3
echo "result($l)"
XX
printf '#!/bin/sh\necho "$*">>%s\n' $MAIL>$T/bin/box;chmod +x $T/bin/*
export GIT_CONFIG_GLOBAL=$H/.gitconfig GIT_CONFIG_SYSTEM=/dev/null
# the invoker's repo ~/t: manifests + goals (committed = the tip), `grown` stays UNtracked until a case creates it
mkdir -p $H/t/extensions/agi/workflows $H/t/.agi/nodes/goal;$G init -q $H/t
w(){ printf '%s\n' "$2">$H/t/extensions/agi/workflows/$1.json;}
w flowfix '{"name":"flowfix","stages":[{"label":"grow","post":"director-general-1","goal":"gk-grow"},{"label":"review","repeat":{"of":"rounds","label_template":"review:{key}"},"prompt":"REVIEW {key}"},{"label":"fix","flow":"flowfix-sub"}]}'
w flowfix-sub '{"name":"flowfix-sub","stages":[{"label":"corrective","prompt":"CORRECTIVE"},{"label":"rereview","chained_from":"corrective","prompt":"REREVIEW"}]}'
gl(){ printf -- '---\nid: goal:%s\ntype: goal\nstatus: active\n---\n# goal:%s\n\n## Falsifier\n%s\n\n## Out of scope\nnothing\n' $1 $1 "$2">$H/t/.agi/nodes/goal/$1.md;}
gl gk-grow 'prose first, then the check:
$ test -e grown'
gl gk-none 'a falsifier with no check line at all'
gl gk-touch '$ touch x'
gl gk-empty '$ '
for g in none touch empty missing;do w g-$g '{"name":"g-'$g'","stages":[{"label":"grow","post":"director-general-1","goal":"gk-'$g'"},{"label":"after","prompt":"SHOULD-NOT-RUN"}]}';done
$G -C $H/t add -A;$G -C $H/t -c commit.gpgsign=false commit -qm fixture
# flow MANIFEST ARGS: the runner as the invoker would run it (rc printed by the caller)
flow(){ (cd $T;HOME=$H GIT_CONFIG_GLOBAL=$H/.gitconfig GIT_CONFIG_SYSTEM=/dev/null PATH=$T/bin:$PATH LOG=$LOG AGI_POST=inv FAILON=$FAILON sh $PIECE -m "$1" "$2");}
nl(){ wc -l<$1|tr -d ' ';}
refs(){ $G -C $H/t for-each-ref --format='%(refname)' refs/spawn/;}
A1='{"rounds":[{"key":"r1"}]}';S1=$(printf %s "$A1"|sha256sum|cut -c1-12)
# --- run 1: the perpetual phase `grow` is handed to its post ONCE and the flow STOPS (rc 75): nothing launched, no ref
flow flowfix "$A1">$T/o1 2>$T/e1;rc=$?
ok "run1-handoff run 1 stops at the post: phase (rc=$rc, expect 75)" '[ $rc = 75 ]'
ok "run1-one-mail exactly ONE 'box send director-general-1 handoff ...' ($(nl $MAIL) mail)" '[ "$(nl $MAIL)" = 1 ]&&grep -q "^send director-general-1 handoff" $MAIL'
ok "run1-nothing-else no kid launched, no result ref, no kid commit in the invoker repo" '[ "$(nl $LOG)" = 0 ]&&[ -z "$(refs)" ]&&[ "$($G -C $H/t rev-list --all --count)" = 1 ]'
# --- run 2 while paused: a decoy that SAYS the phase is done (a card, a mail, a marker file) must not count (Z4.i: the goal's falsifier row decides); no second hand-off
printf 'grow: met\nDONE\n'>$H/t/card.md;mkdir -p $H/t/.agi/sessions;echo met>$H/t/.agi/sessions/grow.done
flow flowfix "$A1">$T/o2 2>$T/e2;rc=$?
ok "run2-paused-mails-nothing a re-run while paused sends NO second hand-off and still stops (rc=$rc, mails $(nl $MAIL))" '[ $rc = 75 ]&&[ "$(nl $MAIL)" = 1 ]'
ok "z4i-card-never-counts a card / marker saying done does not make the phase DONE while its falsifier line reads red: 0 launches, 0 refs" '[ "$(nl $LOG)" = 0 ]&&[ -z "$(refs)" ]'
# --- the GUARD (Z4.8): an empty, missing, refused or absent done-check line is NOT met in every runner; a refused line is never run
for g in none touch empty missing;do : >$LOG;: >$MAIL;flow g-$g '{}'>/dev/null 2>&1;rc=$?
 ok "guard-$g a post: phase whose goal has $([ $g = none ]&&echo 'no check line'||{ [ $g = touch ]&&echo 'a WRITING line (\$ touch x)'||{ [ $g = empty ]&&echo 'an EMPTY check line'||echo 'no goal node'; }; }) is NOT met: rc 75, nothing launched, no ref (rc=$rc)" '[ $rc = 75 ]&&[ "$(nl $LOG)" = 0 ]&&[ -z "$(refs)" ]'
done
ok "guard-touch-refused the refused writing line was never run (no file x)" '[ ! -e $H/t/x ]&&[ ! -e $T/x ]'
: >$LOG;: >$MAIL
# --- run 3: the seed goal now reads met. ONE invocation walks the rest with the root idle (Z4.h): review, then the sub-flow fix: corrective, then rereview chained
touch $H/t/grown
flow flowfix "$A1">$T/o3 2>$T/e3;rc=$?
ok "run3-completes the whole flow completes in ONE run (rc=$rc)" '[ $rc = 0 ]'
ok "z4h-tail-fires-next the one-shots fired in manifest depth-first order from that one run, no further trigger: $(cut -d'|' -f1 $LOG|tr '\n' ',')" '[ "$(cut -d"|" -f1 $LOG)" = "launch REVIEW r1
launch CORRECTIVE
launch REREVIEW" ]'
ok "run3-no-second-handoff the met phase is not handed off again (mails $(nl $MAIL))" '[ "$(nl $MAIL)" = 0 ]'
ok "chained the stage with chained_from gets its predecessor's output for the same item; the predecessor does not get it" 'grep -q "result(CORRECTIVE)" $LOG.p3&&! grep -q "result(" $LOG.p2'
# --- the result: ONE signed commit at refs/spawn/<manifest>/<sha12(ARGS)>, written only now, verifying as the invoker; every stage's output is in its tree
R=refs/spawn/flowfix/$S1
ok "result-ref exactly ONE ref, named by the manifest and sha256(ARGS)[:12] ($(refs|tr '\n' ' '))" '[ "$(refs)" = $R ]'
ok "result-signed the ref's commit is signed by the invoker's key (%G? = G, author inv@agi) and verifies on the ring as inv@agi" '[ "$($G -C $H/t log -1 --format=%G? $R)" = G ]&&[ "$($G -C $H/t log -1 --format=%ae $R)" = inv@agi ]&&$G -C $H/t verify-commit $R 2>&1|grep -q "inv@agi"'
ok "result-holds-every-output the commit tree holds all three stage outputs" '$G -C $H/t grep -q "result(REVIEW r1)" $R&&$G -C $H/t grep -q "result(CORRECTIVE)" $R&&$G -C $H/t grep -q "result(REREVIEW)" $R'
# --- Z4.g: a one-shot holds no key and cannot produce a commit that verifies on the ring
ok "z4g-no-key every launch ran with NO ~/.ssh (in its own HOME) and no .git in its slice: $(grep -c 'ssh=absent|gitdir=absent' $LOG) of $(nl $LOG)" '[ "$(grep -c "ssh=absent|gitdir=absent" $LOG)" = "$(nl $LOG)" ]&&[ "$(nl $LOG)" = 3 ]'
ok "z4g-kid-cannot-commit no launch could commit (kidcommit != 0 each), and the invoker repo holds ONE commit on every branch (no kid commit reached it)" '! grep -q "kidcommit=0" $LOG&&[ "$($G -C $H/t rev-list --branches --count)" = 1 ]'
# --- resumable: run again = every phase DONE, nothing launched, the ref unchanged
tip=$($G -C $H/t rev-parse $R);flow flowfix "$A1">/dev/null 2>&1;rc=$?
ok "run4-launches-nothing a 4th run launches NOTHING and leaves the ref byte-equal (rc=$rc, launches $(nl $LOG), mails $(nl $MAIL))" '[ $rc = 0 ]&&[ "$(nl $LOG)" = 3 ]&&[ "$(nl $MAIL)" = 0 ]&&[ "$($G -C $H/t rev-parse $R)" = "$tip" ]'
# --- two different ARGS = two different refs (the run key is the ARGS bytes), each with its own outputs
A2='{"rounds":[{"key":"r2"},{"key":"r3"}]}';S2=$(printf %s "$A2"|sha256sum|cut -c1-12)
flow flowfix "$A2">/dev/null 2>&1;rc=$?
ok "args-two-refs a different ARGS gives a SECOND ref refs/spawn/flowfix/$S2 beside the first, which is unchanged (rc=$rc)" '[ $rc = 0 ]&&[ "$(refs|wc -l|tr -d " ")" = 2 ]&&[ "$S1" != "$S2" ]&&[ "$($G -C $H/t rev-parse $R)" = "$tip" ]&&$G -C $H/t rev-parse -q --verify refs/spawn/flowfix/$S2>/dev/null'
ok "args-fan-out repeat.of fans out one launch per item: REVIEW r2 and REVIEW r3, once each" '[ "$(grep -c "^launch REVIEW r[23]|" $LOG)" = 2 ]'
# --- a failing phase stops the flow with NO ref; the resume skips what has output (review) and relaunches only the failed phase onward
A3='{"rounds":[{"key":"r4"}]}';S3=$(printf %s "$A3"|sha256sum|cut -c1-12)
FAILON=CORRECTIVE flow flowfix "$A3">/dev/null 2>&1;rc=$?
ok "fail-no-ref a kid that fails stops the flow nonzero and writes NO result ref (rc=$rc)" '[ $rc != 0 ]&&[ $rc != 75 ]&&! $G -C $H/t rev-parse -q --verify refs/spawn/flowfix/$S3>/dev/null'
FAILON= flow flowfix "$A3">/dev/null 2>&1;rc=$?
ok "resume-skips-done the resume does NOT relaunch the finished review (REVIEW r4 launched $(grep -c '^launch REVIEW r4|' $LOG) x), runs corrective again and rereview, and writes the ref (rc=$rc)" '[ $rc = 0 ]&&[ "$(grep -c "^launch REVIEW r4|" $LOG)" = 1 ]&&[ "$(grep -c "^launch CORRECTIVE|" $LOG)" -ge 3 ]&&$G -C $H/t rev-parse -q --verify refs/spawn/flowfix/$S3>/dev/null'
# --- bounds
sz=$(wc -c<$PIECE)
ok "bytes the piece is <= $CEIL B ($sz B; the design's runner is 1,856 B)" '[ $sz -le $CEIL ]'
ok "bytes-sh the piece parses as POSIX sh" 'dash -n $PIECE 2>/dev/null||sh -n $PIECE'
ok "no-python the runner needs no python" '! grep -qi python $PIECE'
echo "agi-kid-flow: $f FAIL"
exit $f
