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
n=$(wc -l<$LOG);echo "$p">$LOG.p$((n+1));echo "launch $(echo "$p"|head -1)">>$LOG;echo "result($(echo "$p"|head -1))"
XX2
printf '#!/bin/sh\necho "$*">>%s\n' $MAIL>$T/bin/box;chmod +x $T/bin/*
export GIT_CONFIG_GLOBAL=$H/.gitconfig GIT_CONFIG_SYSTEM=/dev/null
mkdir -p $H/t/extensions/agi/workflows $H/t/.agi/nodes/goal;$G init -q $H/t
w(){ printf '%s\n' "$2">$H/t/extensions/agi/workflows/$1.json;}
gl(){ printf -- '---\nid: goal:%s\ntype: goal\nstatus: active\n---\n# goal:%s\n\n## Falsifier\n%s\n\n## Out of scope\nnothing\n' $1 $1 "$2">$H/t/.agi/nodes/goal/$1.md;}
gp(){ w g-$1 '{"name":"g-'$1'","stages":[{"label":"grow","post":"director-general-1","goal":"gk-'$1'"},{"label":"after","prompt":"SHOULD-NOT-RUN"}]}';}
# D1 a literal backslash-n in the line (dash echo expands it), D2 the writing / executing git forms, a git form that IS whitelisted and met
gl gk-bs '$ ls x\n; touch pwn-bs';gl gk-log '$ git log --output=pwn-log -1';gl gk-grep "\$ git grep -O'touch pwn-grep' x";gl gk-diff '$ git diff --no-index --output=pwn-diff /dev/null /dev/null';gl gk-ok '$ git ls-files extensions'
gl gk-unmet '$ test -e nothere-unmet'
for g in bs log grep diff ok;do gp $g;done
w one '{"name":"one","stages":[{"label":"solo","prompt":"LINE1\nLINE2 tab\there"}]}'
w fan '{"name":"fan","stages":[{"label":"review","repeat":{"of":"rounds","label_template":"review:{key}"},"prompt":"REVIEW {key}"}]}'
w empty '{"name":"empty","stages":[]}'
w chain-miss '{"name":"chain-miss","stages":[{"label":"a","chained_from":"nothere","prompt":"MISS"}]}'
w chain-rep '{"name":"chain-rep","stages":[{"label":"review","repeat":{"of":"rounds","label_template":"review:{key}"},"prompt":"REVIEW {key}"},{"label":"verify","repeat":{"of":"rounds","label_template":"verify:{key}"},"chained_from":"review","prompt":"VERIFY {key}"}]}'
w chain-lazy '{"name":"chain-lazy","stages":[{"label":"a","prompt":"PAID-A"},{"label":"b","chained_from":"nothere","prompt":"PAID-B"}]}'
w chain-flow '{"name":"chain-flow","stages":[{"label":"f","flow":"cap3"},{"label":"b","chained_from":"f","prompt":"PAID-B"}]}'
w chain-fwd '{"name":"chain-fwd","stages":[{"label":"a","prompt":"PAID-A"},{"label":"b","chained_from":"c","prompt":"PAID-B"},{"label":"c","prompt":"PAID-C"}]}'
w chain-self2 '{"name":"chain-self2","stages":[{"label":"a","prompt":"PAID-A"},{"label":"b","chained_from":"b","prompt":"PAID-B"}]}'
w chain-self '{"name":"chain-self","stages":[{"label":"a","chained_from":"a","prompt":"PAID-A"}]}'
w unmet-post '{"name":"unmet-post","stages":[{"label":"a","prompt":"PAID-A"},{"label":"p","post":"director-general-1","goal":"gk-unmet"},{"label":"c","prompt":"SHOULD-NOT-RUN"}]}'
w lazy-field '{"name":"lazy-field","stages":[{"label":"ok","prompt":"PAID-OK"},{"label":"bad","post":"director-general-1","goal":"g.md --output=victim zz"}]}'
w sub-bad '{"name":"sub-bad","stages":[{"label":"review","repeat":{"of":"rounds","label_template":"review:{key}"},"prompt":"SUB {key}"}]}'
w lazy-sub '{"name":"lazy-sub","stages":[{"label":"ok","prompt":"PAID-OK"},{"label":"sub","flow":"sub-bad"}]}'
w sub-badfield '{"name":"sub-badfield","stages":[{"label":"bad","post":"director-general-1","goal":"gk-ok x"}]}'
w mid '{"name":"mid","stages":[{"label":"m","flow":"sub-badfield"}]}'
w lazy-deep '{"name":"lazy-deep","stages":[{"label":"ok","prompt":"PAID-OK"},{"label":"deep","flow":"mid"}]}'
w dash-p '{"name":"dash-p","stages":[{"label":"ok","prompt":"PAID-OK"},{"label":"d","prompt":"--model=x"}]}'
w at-p '{"name":"at-p","stages":[{"label":"ok","prompt":"PAID-OK"},{"label":"d","prompt":"@/etc/hostname"}]}'
w key-p '{"name":"key-p","stages":[{"label":"ok","prompt":"PAID-OK"},{"label":"r","repeat":{"of":"rounds","label_template":"r:{key}"},"prompt":"{key}"}]}'
w cap0 '{"name":"cap0","stages":[{"label":"h","flow":"cap1"}]}'
w cap1 '{"name":"cap1","stages":[{"label":"h","flow":"cap2"}]}'
w cap2 '{"name":"cap2","stages":[{"label":"leaf","prompt":"LEAF2"},{"label":"h","flow":"cap3"}]}'
w cap3 '{"name":"cap3","stages":[{"label":"leaf","prompt":"LEAF3"}]}'
w hop2 '{"name":"hop2","stages":[{"label":"h","flow":"hop2b"}]}'
w hop2b '{"name":"hop2b","stages":[{"label":"h","flow":"hop2c"}]}'
w hop2c '{"name":"hop2c","stages":[{"label":"leaf","prompt":"LEAF-HOP2"}]}'
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
# --- chained_from (mur sm17 W-1.4 R1): a MISSING predecessor refuses before any spawn; the repeat form (predecessor output kept as o.<label>:<key>) is pinned
: >$LOG;flow chain-miss '{}'>/dev/null 2>&1;rc=$?
ok "chain-missing-refused a chained stage whose predecessor has no output exits nonzero and launches NOTHING (rc=$rc, launches $(nl $LOG))" '[ $rc != 0 ]&&[ "$(nl $LOG)" = 0 ]'
: >$LOG;flow chain-rep '{"rounds":[{"key":"k1"},{"key":"k2"}]}'>/dev/null 2>&1;rc=$?
ok "chain-repeat-fallback review:{key} then verify:{key} chained_from review: each verify launch sees ITS review output (rc=$rc, launches $(nl $LOG))" '[ $rc = 0 ]&&[ "$(nl $LOG)" = 4 ]&&grep -q "^result(REVIEW k1)" $LOG.p3&&grep -q "^result(REVIEW k2)" $LOG.p4&&! grep -q "result(REVIEW k2)" $LOG.p3'
# --- W-1.12 (mur sm18 W-1.11 R1, DG1 04:4xZ + 05:29Z): a chained_from naming NO label of the manifest is refused in the DRY pass: a good PAID stage before it is never launched
: >$LOG;: >$MAIL;n4=$(refs|wc -l|tr -d " ");flow chain-lazy '{}'>/dev/null 2>&1;rc=$?
ok "w12-chain-dry-pass [good paid a, then b chained_from nothere] refuses with 0 launches, 0 mail, no ref (rc=$rc, launches $(nl $LOG), was 1 paid launch on W-1.11)" '[ $rc != 0 ]&&[ "$(nl $LOG)" = 0 ]&&[ "$(nl $MAIL)" = 0 ]&&[ "$(refs|wc -l|tr -d " ")" = $n4 ]'
: >$LOG;flow chain-rep '{"rounds":[{"key":"k1"}]}'>/dev/null 2>&1;rc=$?
ok "w12-chain-label-ok control: a chained_from that names a manifest label (the repeat form review -> review:k1) still runs (rc=$rc, launches $(nl $LOG), want 2)" '[ $rc = 0 ]&&[ "$(nl $LOG)" = 2 ]'
# --- W-1.12 (mur sm18 R2 + R3, DG1 05:29Z): the post: gate after a PAID stage is the RUNTIME-STATE gate, BY DESIGN (BOUNDS): the paid stage launches, the unmet gate hands off ONCE and stops, rc 75.
# The dry pass SKIPS the post: line (`[ "$V" ]&&return;`): if it evaluated the gate it would hand off and stop BEFORE the paid launch (launches 0), so launches = 1 pins the skip.
: >$LOG;: >$MAIL;n5=$(refs|wc -l|tr -d " ");flow unmet-post '{}'>/dev/null 2>&1;rc=$?
ok "w12-unmet-post-after-paid [paid a, then an unmet post: gate, then c] = 1 paid launch, 1 hand-off mail, rc 75, c never runs, no ref (rc=$rc, launches $(nl $LOG), mail $(nl $MAIL))" '[ $rc = 75 ]&&[ "$(nl $LOG)" = 1 ]&&[ "$(nl $MAIL)" = 1 ]&&grep -q "^send director-general-1 handoff" $MAIL&&! grep -q SHOULD-NOT-RUN $LOG&&[ "$(refs|wc -l|tr -d " ")" = $n5 ]'
# --- W-1.13 (mur sm18 W-1.12 R1'): a chained_from must name an EARLIER stage: a FORWARD or a SELF label exists but has no output yet, so it is refused in the dry pass with 0 launches
for m in chain-fwd chain-self2 chain-self;do : >$LOG;: >$MAIL;n6=$(refs|wc -l|tr -d " ");flow $m '{}'>/dev/null 2>&1;rc=$?
 ok "w13-chain-order-$m [paid stage(s), a chained_from naming a LATER or its OWN label] ($m) refuses with 0 launches, 0 mail, no ref (rc=$rc, launches $(nl $LOG))" '[ $rc != 0 ]&&[ "$(nl $LOG)" = 0 ]&&[ "$(nl $MAIL)" = 0 ]&&[ "$(refs|wc -l|tr -d " ")" = $n6 ]'
done
# a chained_from naming a flow: stage passes the dry pass (an earlier label) but that stage leaves NO output file: the wet-pass read refuses (`||exit 1`), the sub-flow's leaf is the only launch
: >$LOG;flow chain-flow '{}'>/dev/null 2>&1;rc=$?
ok "w13-chain-flow-pred a stage chained_from a flow: stage (no output file) launches the sub-flow leaf, then refuses b: nonzero, 1 launch, b never runs (rc=$rc, launches $(nl $LOG))" '[ $rc != 0 ]&&[ "$(nl $LOG)" = 1 ]&&! grep -q PAID-B $LOG'
# --- W-1.13 (mur sm18 N1): a flow whose result ref exists is DONE: with the state dir GONE the re-run launches NOTHING (only the ref test says so). This lane pins an EXISTING ref = DONE (the `false&&exit` mutant); it does NOT pin the exact match: `show-ref -q` (tail-matching) leaves this file GREEN, DG2's agi-kid-flow-dry.t.sh r2-tail-match-is-not-done pins that, BOUNDS (10)
: >$LOG;flow one '{"n":"w13"}'>/dev/null 2>&1;rc1=$?;l1=$(nl $LOG);rm -rf $H/s;: >$LOG;flow one '{"n":"w13"}'>/dev/null 2>&1;rc2=$?
ok "w13-done-ref-resume a flow run twice with its state dir removed between: the 2nd run launches nothing (rc $rc1 $rc2, launches $l1 then $(nl $LOG))" '[ $rc1 = 0 ]&&[ $rc2 = 0 ]&&[ "$l1" = 1 ]&&[ "$(nl $LOG)" = 0 ]'
# --- recursion (mur sm17 W-1.4 R2, DG1 04:16Z): the depth cap is PINNED by counting paid launches. cyc-a launches one one-shot then names cyc-b which names cyc-a: with no cap the run goes until a system limit (63 launches measured), with the depth cap (${#d} -lt 2: the deepest real nesting over the manifests is 0, plus 2) it stops after 2 levels.
# The cost is bounded by the cap: a cyclic manifest spends at most 3 paid one-shots (BOUND 3). An EXPORTED P (or d) must not seed the prefix (P= and d= at -m entry): the same run with a 150-byte P in the environment launches the same number.
LP=$(head -c 150 /dev/zero|tr '\0' x);fl2(){ ( cd $T;env $1 HOME=$H GIT_CONFIG_GLOBAL=$H/.gitconfig GIT_CONFIG_SYSTEM=/dev/null PATH=$T/bin:$PATH LOG=$LOG AGI_POST=inv timeout 30 sh $PIECE -m $2 "${3:-{\}}" )>/dev/null 2>&1;rc=$?;}
n1=$(refs|wc -l|tr -d ' ');: >$LOG;fl2 X=1 selfie;rs=$rc;ls1=$(nl $LOG);: >$LOG;fl2 X=1 cyc-a;rc2=$rc;lc=$(nl $LOG);: >$LOG;fl2 "P=$LP d=.." cyc-a '{"state":"fresh"}';rp=$rc;lp=$(nl $LOG)
ok "rec-guard-stops a self-naming flow (rc=$rs) and a 2-cycle (rc=$rc2) stop nonzero, not by the 30 s timeout (124), and write no ref" '[ $rs != 0 ]&&[ $rs != 124 ]&&[ $rc2 != 0 ]&&[ $rc2 != 124 ]&&[ "$(refs|wc -l|tr -d " ")" = $n1 ]'
ok "rec-guard-counted a cyclic manifest launches NOTHING (W-1.11: the dry pass walks every flow before the first paid launch and hits the depth cap; 2-cycle $lc, self-naming $ls1, no cap = 63 paid one-shots)" '[ $lc = 0 ]&&[ $ls1 = 0 ]'
ok "rec-guard-p-not-seeded an exported 150-byte P and an exported depth d=.. do not change the count (cap run $lc, with P exported $lp, rc=$rp)" '[ $lp = $lc ]'
# --- W-1.11 (mur sm17 W-1.10 R1, DG1's paid-spend rule): EVERY row of the manifest and of every sub-flow (recursively) is checked BEFORE the first launch: a bad row after a good paid stage launches NOTHING
printf keep>$H/t/victim;n3=$(refs|wc -l|tr -d " ")
for m in lazy-field lazy-sub lazy-deep dash-p at-p;do : >$LOG;: >$MAIL;flow $m '{}'>/dev/null 2>&1;rc=$?
 ok "w11-nothing-launched-$m [good paid stage, then a bad row] ($m) refuses with 0 launches, 0 mail, no ref, victim intact (rc=$rc, launches $(nl $LOG))" '[ $rc != 0 ]&&[ "$(nl $LOG)" = 0 ]&&[ "$(nl $MAIL)" = 0 ]&&[ "$(refs|wc -l|tr -d " ")" = $n3 ]&&[ "$(cat $H/t/victim)" = keep ]'
done
: >$LOG;flow key-p '{"rounds":[{"key":"-rf"}]}'>/dev/null 2>&1;rc=$?
ok "w11-key-templated-prompt a prompt that BECOMES '-rf' through the key template refuses with 0 launches (rc=$rc, launches $(nl $LOG))" '[ $rc != 0 ]&&[ "$(nl $LOG)" = 0 ]'
: >$LOG;flow key-p '{"rounds":[{"key":"fine"}]}'>/dev/null 2>&1;rc=$?
ok "w11-key-templated-ok control: the same manifest with a plain key runs both stages (rc=$rc, launches $(nl $LOG))" '[ $rc = 0 ]&&[ "$(nl $LOG)" = 2 ]'
# the depth cap pinned by NESTING, not by cost: two sub-flow hops run, three are refused before any launch
: >$LOG;flow hop2 '{}'>/dev/null 2>&1;rc=$?
ok "w11-cap-two-hops a flow that nests two sub-flows deep runs its leaf (rc=$rc, launches $(nl $LOG))" '[ $rc = 0 ]&&[ "$(nl $LOG)" = 1 ]'
: >$LOG;flow cap0 '{}'>/dev/null 2>&1;rc=$?
ok "w11-cap-three-hops a flow that nests THREE sub-flows deep is refused with 0 launches though its other stages are valid (rc=$rc, launches $(nl $LOG))" '[ $rc != 0 ]&&[ "$(nl $LOG)" = 0 ]'
# --- D5: a manifest name outside [a-z0-9-] is refused before anything is created
rm -rf $H/s;flow '../t' '{}'>/dev/null 2>&1;rc1=$?;flow 'One' '{}'>/dev/null 2>&1;rc2=$?;flow 'a b' '{}'>/dev/null 2>&1;rc3=$?
ok "d5-name-refused names '../t', 'One' and 'a b' exit nonzero and create nothing under ~/s (rc $rc1 $rc2 $rc3)" '[ $rc1 != 0 ]&&[ $rc2 != 0 ]&&[ $rc3 != 0 ]&&[ ! -e $H/s ]'
# --- R1 (mur sm17 W-1.8): a goal / flow / post field is a WORD, never an option: option-looking or off-charset values are refused, nothing runs, no victim file is touched
printf keep>$H/t/victim;gp2(){ w r1-$1 '{"name":"r1-'$1'","stages":[{"label":"x","post":"'"$2"'","goal":"'"$3"'","flow":"'"$4"'"}]}';}
gp2 goal director-general-1 'g.md --output=victim zz' '';gp2 post '--help' gk-ok '';gp2 dash director-general-1 '-p' '';gp2 flow '' '' 'a --output=victim'
$G -C $H/t add -A;$G -C $H/t -c commit.gpgsign=false commit -qm r1
for g in goal post dash flow;do : >$LOG;: >$MAIL;r0=$(refs|wc -l|tr -d " ");flow r1-$g '{}'>/dev/null 2>&1;rc=$?
 ok "r1-$g the $g field of r1-$g is refused: rc 75, no launch, no mail, victim file intact, no ref (rc=$rc, 75 like any not-met line)" '[ $rc = 75 ]&&[ "$(nl $LOG)" = 0 ]&&[ "$(nl $MAIL)" = 0 ]&&[ "$(cat $H/t/victim)" = keep ]&&[ "$(refs|wc -l|tr -d " ")" = $r0 ]'
done
# --- R2: a repeat stage whose repeat.of is absent from ARGS refuses (it must not drop its phase and sign DONE)
w miss-of '{"name":"miss-of","stages":[{"label":"a","prompt":"BEFORE"},{"label":"review","repeat":{"of":"rounds","label_template":"review:{key}"},"prompt":"REVIEW {key}"}]}'
$G -C $H/t add -A;$G -C $H/t -c commit.gpgsign=false commit -qm r2
n2=$(refs|wc -l|tr -d ' ');: >$LOG;flow miss-of '{"other":[{"key":"k"}]}'>/dev/null 2>&1;rc=$?
ok "r2-absent-of a repeat whose repeat.of is missing from ARGS exits nonzero, launches nothing and signs NO ref (rc=$rc, launches $(nl $LOG))" '[ $rc != 0 ]&&[ "$(nl $LOG)" = 0 ]&&[ "$(refs|wc -l|tr -d " ")" = $n2 ]'
for v in '{"rounds":"abc"}' '{"rounds":{"a":{"key":"k"}}}' '{"rounds":null}' '{"rounds":7}';do : >$LOG;flow miss-of "$v">/dev/null 2>&1;rc=$?
 ok "r2-non-array repeat.of=$v (a string, an object, null, a number) is not a list: nonzero, nothing launched, no ref (rc=$rc, launches $(nl $LOG))" '[ $rc != 0 ]&&[ "$(nl $LOG)" = 0 ]&&[ "$(refs|wc -l|tr -d " ")" = $n2 ]'
done
: >$LOG;flow miss-of '{"rounds":[]}'>/dev/null 2>&1;rc=$?
ok "r2-empty-of an EMPTY rounds list is a real list: the flow runs its other stage and signs (rc=$rc, launches $(nl $LOG))" '[ $rc = 0 ]&&[ "$(nl $LOG)" = 1 ]'
ok "bytes the piece is <= ${CEIL:-2052} B ($(wc -c<$PIECE) B)" '[ $(wc -c<$PIECE) -le ${CEIL:-2052} ]'
echo "agi-kid-flow-guard: $f FAIL"
exit $f
