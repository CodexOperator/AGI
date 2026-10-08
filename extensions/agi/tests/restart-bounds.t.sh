#!/bin/sh
# restart-bounds.t.sh: goal:g1.41 A3 + A4 (DG1 21:49Z; hypothesis:g141-a2-a4-root-pieces-fail-closed-...): (A3) a missing agi-run no longer loops: agi-post@.service SKIPS (an ExecCondition that exits 2, no failure, no root agi-signers) and agi-carry@.service stops restarting a post that is absent at the pinned trunk (box-carry exits 0 for it, a finite StartLimitBurst instead of StartLimitIntervalSec=0); (A4) agi-project projects only rows whose .name matches ^[a-z][a-z0-9-]{0,27}$ and skips any other BY NAME on stderr (rc 0, the rest of the town stays up), so a name never reaches a path, a sed replacement or a sysusers field.
# sh + git + jq on SCRATCH repos, no systemd, no root, no /etc, no network, 0 USD. The REAL pieces (`sect <piece>` from the .geometry/engine*.md of ROOT, default the working tree): the agi-post@.service and agi-carry@.service unit TEXT, box-carry, agi-project. None of this touches A1's lines (the pin), so the lane holds on the trunk, on trunk + A1 and on the A2-A4 reference.
# Lanes: a3-post-* the ExecCondition lines run under sh: agi-run absent from PATH -> one exits 2 and none exits another code; a stub agi-run on PATH -> all exit 0. a3-carry-unit-* no StartLimitIntervalSec=0 / infinity in the [Unit] of agi-carry@.service, a finite StartLimitBurst >= 1. a3-box-carry-* the real box-carry for a post ABSENT at the pin exits 0; a present post exits 0; a bad pin and a matrix missing at the pin STILL exit 1 (a guard against over-correction, beyond the brief). a4-* a posts.md of hostile names: only the good three project, each printable bad name is on stderr, rc 0, nothing written outside the out dir, the out dir holds only the good shape, users.conf only the good users; every one of the 33 live post names projects.
# Honest limits: the lane reads unit TEXT and runs the pieces' shell, never systemd (whether Restart=always honours an ExecCondition skip is systemd's rule, not read here); a3-post reads agi-run through PATH only (a hard-coded path would not be found); a name holding a quote or a control character is checked for ABSENCE from every output, not for its spelling on stderr.
T=$(mktemp -d);trap 'rm -rf $T' 0;f=0;G=/usr/bin/git;R0=${ROOT:-${1:-$(cd "$(dirname "$0")/../../.." && pwd)}}
ok(){ if eval "$2";then echo "ok $1";else echo "FAIL $1";f=$((f+1));fi;}
sect(){ cat $R0/.agi/nodes/.geometry/engine*.md|sed -n "/^###* $1 /,/^###* /{/^~~~/,/^~~~/{//!p}}";}
unset GIT_AUTHOR_NAME GIT_AUTHOR_EMAIL GIT_COMMITTER_NAME GIT_COMMITTER_EMAIL GIT_DIR GIT_WORK_TREE AGI_TRUNK AGI_SEAT AGI_POST AGI_BOX AGI_RAM AGI_STORES AGI_REPO AGI_HUB AGI_CARRY AGI_RUN
sect agi-post@.service >$T/up;sect agi-carry@.service >$T/uc;sect box-carry >$T/carry;sect agi-project >$T/proj.sh
[ -s $T/up ]&&[ -s $T/uc ]&&[ -s $T/carry ]&&[ -s $T/proj.sh ]||{ echo "FAIL extract: post unit $(wc -c <$T/up) carry unit $(wc -c <$T/uc) box-carry $(wc -c <$T/carry) agi-project $(wc -c <$T/proj.sh)";exit 99;}
mkdir -p $T/cap $T/hm $T/cwd $T/nobin $T/withrun $T/bin
printf '#!/bin/sh\nexit 0\n' >$T/withrun/agi-run;chmod +x $T/withrun/agi-run
printf '[user]\n\tname=t\n\temail=t@t\n[commit]\n\tgpgsign=false\n[safe]\n\tdirectory=*\n' >$T/gitconfig;export GIT_CONFIG_GLOBAL=$T/gitconfig GIT_CONFIG_SYSTEM=/dev/null
# --- a3-post: every ExecCondition line of the post unit, run as sh would run the value (%i -> x), cwd without .ssh/out-refused
grep '^ExecCondition=' $T/up|sed 's/^ExecCondition=//;s/%i/x/g' >$T/conds
conds(){ rcs=;while IFS= read -r l;do (cd $T/cwd&&env -i PATH=$1:/usr/bin:/bin HOME=$T/hm sh -c "$l" >/dev/null 2>&1);rcs="$rcs $?";done <$T/conds;rcs=${rcs# };}
conds $T/nobin;absent="$rcs";conds $T/withrun;present="$rcs";nc=$(wc -l <$T/conds|tr -d ' ')
two=0;other=0;for r in $absent;do case $r in 0);;2)two=$((two+1));;*)other=$((other+1));;esac;done
ok "a3-post-skips-when-agi-run-is-absent the $nc ExecCondition line(s) of agi-post@.service with agi-run NOT on PATH exit [$absent]: $two exit 2 (want >= 1: a skip), $other exit another code (want 0: not a failure)" '[ $two -ge 1 ]&&[ $other = 0 ]'
nz=0;for r in $present;do [ $r = 0 ]||nz=$((nz+1));done
ok "a3-post-runs-when-agi-run-is-present the same line(s) with a stub agi-run on PATH exit [$present]: $nz non-zero (want 0)" '[ $nz = 0 ]&&[ $nc -ge 1 ]'
# --- RA11 (DG1 02:23Z): the agi-run ExecCondition is exactly as wide as the extraction that follows it (ExecStartPre reads engine.md and engine-[pw]*.md of t): agi-run in ANY of engine.md, engine-post.md, engine-wrap.md of t (or, with no t yet, of the trunk the unit will build t from) exits 0; in none, and not on PATH, exits 2. A condition narrower than the extraction skips a post that could start (a stale-t fixture carries agi-run only in engine-post.md).
grep '^ExecCondition=.*agi-run' $T/up|sed 's/^ExecCondition=//;s/%i/x/g' >$T/rcond;nrc=$(grep -c . $T/rcond)
RUNSTUB='### agi-run (stub)\n~~~sh\n#!/bin/sh\nexit 0\n~~~\n'
# cond_t FILE: t exists in the unit's cwd and holds agi-run ONLY in FILE (empty = nowhere), agi-run not on PATH
cond_t(){ rm -rf $T/ct;mkdir -p $T/ct/t/.agi/nodes/.geometry;printf '### other (stub)\n~~~sh\nexit 0\n~~~\n' >$T/ct/t/.agi/nodes/.geometry/engine-grow.md;[ -z "$1" ]||printf "$RUNSTUB" >$T/ct/t/.agi/nodes/.geometry/$1
 (cd $T/ct&&env -i PATH=$T/nobin:/usr/bin:/bin HOME=$T/hm sh -c "$(cat $T/rcond)" >/dev/null 2>&1);crc=$?;}
# cond_trunk FILE: no t yet; $O is a repo whose trunk commit holds agi-run ONLY in FILE (empty = nowhere)
cond_trunk(){ rm -rf $T/ct $T/co;mkdir -p $T/ct $T/co/.agi/nodes/.geometry;printf '### other (stub)\n~~~sh\nexit 0\n~~~\n' >$T/co/.agi/nodes/.geometry/engine-grow.md;[ -z "$1" ]||printf "$RUNSTUB" >$T/co/.agi/nodes/.geometry/$1
 $G init -q $T/co;$G -C $T/co add -A;$G -C $T/co commit -qm trunk;TK=$($G -C $T/co rev-parse HEAD)
 (cd $T/ct&&env -i PATH=$T/nobin:/usr/bin:/bin HOME=$T/hm GIT_CONFIG_GLOBAL=$T/gitconfig GIT_CONFIG_SYSTEM=/dev/null O=$T/co AGI_TRUNK=$TK sh -c "$(cat $T/rcond)" >/dev/null 2>&1);crc=$?;}
ok "ra11-the-agi-run-condition-is-one-line the unit has exactly one ExecCondition that mentions agi-run: $nrc (want 1)" '[ "$nrc" = 1 ]'
for fn in engine-post.md engine.md engine-wrap.md;do cond_t $fn
 ok "ra11-t-has-agi-run-only-in-$fn t exists, agi-run only in t/.agi/nodes/.geometry/$fn, not on PATH: the condition exits $crc (want 0: the extraction finds it)" '[ $crc = 0 ]';done
cond_t "";ok "ra11-t-has-agi-run-nowhere t exists, agi-run in none of the three files, not on PATH: the condition exits $crc (want 2: a skip)" '[ $crc = 2 ]'
for fn in engine-post.md engine.md engine-wrap.md;do cond_trunk $fn
 ok "ra11-no-t-trunk-has-agi-run-only-in-$fn no t yet, the trunk commit holds agi-run only in $fn, not on PATH: the condition exits $crc (want 0: the worktree add will give t that file)" '[ $crc = 0 ]';done
cond_trunk "";ok "ra11-no-t-trunk-has-agi-run-nowhere no t yet, the trunk holds agi-run in none of the three files, not on PATH: the condition exits $crc (want 2)" '[ $crc = 2 ]'
# --- a3-carry-unit: the [Unit] of the service unit
iv=$(grep -Ec '^StartLimitIntervalSec=(0|infinity)[[:space:]]*$' $T/uc);bn=$(sed -n 's/^StartLimitBurst=\([0-9][0-9]*\)[[:space:]]*$/\1/p' $T/uc);nb=$(echo "$bn"|grep -c .)
ok "a3-carry-unit-has-no-unlimited-restart agi-carry@.service: $iv StartLimitIntervalSec=0/infinity line(s) (want 0)" '[ $iv = 0 ]'
ok "a3-carry-unit-has-a-finite-burst agi-carry@.service: StartLimitBurst lines $nb (want 1), value [$bn] (want a whole number >= 1)" '[ $nb = 1 ]&&[ "$bn" -ge 1 ]'
# --- a3-box-carry: the real piece, ONE uid (AGI_RUN=none), a scratch repo holding the matrix at the pin
$G init -q $T/r;mkdir -p $T/r/.agi/nodes/.geometry;cp $R0/.agi/nodes/.geometry/engine-post.md $T/r/.agi/nodes/.geometry/
printf '%s\n' '  - {"name":"alpha","parent":"owner","box":"A"}' '  - {"name":"bravo","parent":"owner","box":"B"}' >$T/r/.agi/nodes/.geometry/posts.md
$G -C $T/r add -A;$G -C $T/r commit -qm fixture;TR=$($G -C $T/r rev-parse HEAD)
$G init -q $T/r2;mkdir -p $T/r2/.agi/nodes/.geometry;cp $R0/.agi/nodes/.geometry/engine-post.md $T/r2/.agi/nodes/.geometry/;$G -C $T/r2 add -A;$G -C $T/r2 commit -qm nomatrix;TR2=$($G -C $T/r2 rev-parse HEAD)
cat >$T/bin/sect<<XX
#!/bin/sh
$G -C \${AGI_REPO:?} show \${2:-HEAD}:.agi/nodes/.geometry/engine-post.md|sed -n "/^###* \$1 /,/^###* /{/^~~~/,/^~~~/{//!p}}"
XX
chmod +x $T/bin/sect;mkdir -p $T/A;$G init -q --bare $T/A/alpha/g.git
# carry REPO PIN POST: the carrier as root of box A, no hub
carry(){ (cd $T&&env -i PATH=$T/bin:/usr/bin:/bin HOME=$T/hm GIT_CONFIG_GLOBAL=$T/gitconfig GIT_CONFIG_SYSTEM=/dev/null AGI_RUN=none AGI_BOX=A AGI_STORES=$T/A AGI_REPO=$1 AGI_TRUNK=$2 AGI_HUB= AGI_CARRY=$T/A/carry.git timeout 60 sh $T/carry $3 >$T/c.out 2>$T/c.err);crc=$?;}
carry $T/r $TR alpha;ok "a3-box-carry-a-present-post-exits-0 box-carry alpha (in the matrix at the pin): rc $crc (want 0)" '[ $crc = 0 ]'
carry $T/r $TR ghost;ok "a3-box-carry-an-absent-post-exits-0 box-carry ghost (NOT in the matrix at the pin): rc $crc (want 0: nothing to carry is a success, no restart); stderr lines $(wc -l <$T/c.err|tr -d ' ') (want 0)" '[ $crc = 0 ]&&[ ! -s $T/c.err ]'
carry $T/r $TR bravo;ok "a3-box-carry-a-post-of-another-box-exits-0 box-carry bravo (a row of box B): rc $crc (want 0)" '[ $crc = 0 ]'
carry $T/r gggggggggggggggggggggggggggggggggggggggg alpha;ok "a3-box-carry-a-non-hex-pin-still-exits-1 (guard) a 40-character pin that is not hex: rc $crc (want 1)" '[ $crc = 1 ]'
carry $T/r abc alpha;ok "a3-box-carry-a-bad-pin-still-exits-1 (guard) AGI_TRUNK=abc: rc $crc (want 1)" '[ $crc = 1 ]'
carry $T/r2 $TR2 alpha;ok "a3-box-carry-a-missing-matrix-still-exits-1 (guard) the pin has no posts.md: rc $crc (want 1: a matrix that cannot be read is not an absent post)" '[ $crc = 1 ]'
# --- a4: the real agi-project over a posts.md of names
row(){ printf '  - {"name": %s, "boot": true, "engine": {"v": 4, "harness": "claude-code", "model": "m", "effort": "high"}, "role": "director", "tier": 1, "box": "local-town"}\n' "$1";}
A28=a$(printf 'b%.0s' $(seq 1 27));A29=a$(printf 'b%.0s' $(seq 1 28))
proj(){ rm -rf $T/o4 $T/r4;mkdir -p $T/r4/.agi/nodes/.geometry;cp $R0/.agi/nodes/.geometry/engine*.md $T/r4/.agi/nodes/.geometry/;cat >$T/r4/.agi/nodes/.geometry/posts.md
 $G init -q $T/r4;$G -C $T/r4 add -A;$G -C $T/r4 commit -qm posts;PR=$($G -C $T/r4 rev-parse HEAD);mkdir -p $T/fk;find $T -path $T/o4 -prune -o -path $T/cap -prune -o -path $T/r4/.git -prune -o -print|sort >$T/cap/before
 (cd $T/r4&&env -i PATH=$T/fk:/usr/bin:/bin HOME=$T/hm GIT_CONFIG_GLOBAL=$T/gitconfig GIT_CONFIG_SYSTEM=/dev/null AGI_BOX=local-town timeout 60 sh -s $T/o4 $PR <$T/proj.sh >$T/cap/p.out 2>$T/cap/p.err);prc=$?;find $T -path $T/o4 -prune -o -path $T/cap -prune -o -path $T/r4/.git -prune -o -print|sort >$T/cap/after;}
{ printf -- '---\nposts:\n';row '"good"';row '"../../escape"';row '"a/b"';row '"a\tb"';row '"Good"';row "\"$A29\"";row '"q\"uote"';row '"ab\ncd"';row '"good\n"';row '"1abc"';row '"-x"';row "\"$A28\"";row '"a-b-1"';row '""';row '"good\nevil"';} >$T/cap/posts.in;proj <$T/cap/posts.in
dirs=$(ls -A $T/o4 2>/dev/null|sed -n 's/^agi-post@\(.*\)\.service\.d$/\1/p'|sort|tr '\n' ' ');want=$(printf '%s\n' a-b-1 $A28 good|sort|tr '\n' ' ')
ok "a4-only-the-good-names-project rc $prc (want 0: the rest of the town stays up), the projected names [$dirs] (want exactly [$want])" '[ $prc = 0 ]&&[ "$dirs" = "$want" ]'
miss=;for n in '../../escape' 'a/b' Good $A29 1abc -x;do grep -qF -- "$n" $T/cap/p.err||miss="$miss $n";done
ok "a4-every-printable-bad-name-is-named-on-stderr missing from stderr: [${miss# }] (want none)" '[ -z "$miss" ]'
d=$(diff $T/cap/before $T/cap/after|grep -c .);odd=$(ls -A $T/o4|grep -vxE "agi-post@\.service|agi-post@(good|$A28|a-b-1)\.service\.d|agi-project\.(service|path)|agi-users\.conf|multi-user\.target\.wants"|tr '\n' ' ')
ok "a4-nothing-is-written-outside-the-out-dir the tree around the out dir changed by $d line(s) (want 0), entries in the out dir that are not the good shape: [${odd% }] (want none)" '[ $d = 0 ]&&[ -z "$odd" ]'
wn=$(ls -A $T/o4/multi-user.target.wants 2>/dev/null|grep -vxE "agi-post@(good|$A28|a-b-1)\.service|agi-project\.path"|tr '\n' ' ');uc=$(grep -vcE "agi-(good|$A28|a-b-1)([^a-z0-9-]|\$)" $T/o4/agi-users.conf 2>/dev/null);nu=$(grep -c . $T/o4/agi-users.conf 2>/dev/null)
ok "a4-users-and-wants-hold-only-the-good-names wants entries outside the good set: [${wn% }] (want none); agi-users.conf lines $nu (want >= 3), lines naming a user outside the good set: $uc (want 0)" '[ -z "$wn" ]&&[ "$nu" -ge 3 ]&&[ "$uc" = 0 ]'
ok "a4-no-hostile-name-reaches-any-file no output file holds the traversal, the slash, the quote or an uppercase name: $(grep -rlE 'escape|a/b|q.?uote|Good|1abc' $T/o4 2>/dev/null|wc -l|tr -d ' ') file(s) (want 0)" '[ "$(grep -rlE "escape|a/b|q.?uote|Good|1abc" $T/o4 2>/dev/null|wc -l|tr -d " ")" = 0 ]'
# the boundary names one by one: 28 chars in, 29 out, a leading digit / hyphen out, a trailing hyphen in
for pair in "$A28:in" "$A29:out" "1abc:out" "-x:out" "a-:in" "a:in" "ab-c9:in" "A:out" "a_b:out" "a.b:out";do n=${pair%:*};w=${pair#*:};{ printf -- '---\nposts:\n';row "\"$n\"";} >$T/cap/posts.in;proj <$T/cap/posts.in;[ -d $T/o4/agi-post@$n.service.d ]&&g=in||g=out
 ok "a4-boundary-$w-$(echo $n|cut -c1-8)-len$(printf %s $n|wc -c|tr -d ' ') the name [$n] is $g (want $w), rc $prc (want 0)" '[ $g = $w ]&&[ $prc = 0 ]';done
# the 33 live names: every one projects (a posts.md rebuilt from the live names, each as a boot row)
sed -n 's/^  - {/{/p' $R0/.agi/nodes/.geometry/posts.md|jq -r '.name' >$T/live;nl=$(wc -l <$T/live|tr -d ' ')
{ printf -- '---\nposts:\n';while read -r n;do row "\"$n\"";done <$T/live;} >$T/cap/posts.in;proj <$T/cap/posts.in
got=$(ls -A $T/o4|sed -n 's/^agi-post@\(.*\)\.service\.d$/\1/p'|sort|tr '\n' ' ');exp=$(sort $T/live|tr '\n' ' ')
ok "a4-every-live-post-name-still-projects the $nl live names (want >= 30): rc $prc (want 0), projected = the live set: $([ "$got" = "$exp" ]&&echo yes||echo NO) (want yes), stderr lines $(wc -l <$T/cap/p.err|tr -d ' ') (want 0)" '[ $prc = 0 ]&&[ $nl -ge 30 ]&&[ "$got" = "$exp" ]&&[ ! -s $T/cap/p.err ]'
# --- RA10 (DG1 01:48Z): `.+.engine` lets a key engine.name OVERRIDE the name after the outer .name was checked, so a name reached a path unchecked. The rule: the name that reaches a path is the one checked (the MERGED name). Ruled: engine.name `other` projects as `other`; an outer BAD name with a good engine.name projects as the engine name; a merged name that is not a good string is skipped BY NAME on stderr.
rowen(){ printf '  - {"name": %s, "boot": true, "engine": {"v": 4, "name": %s, "harness": "claude-code", "model": "m", "effort": "high"}, "role": "director", "tier": 1, "box": "local-town"}\n' "$1" "$2";}
pdirs(){ ls -A $T/o4 2>/dev/null|sed -n 's/^agi-post@\(.*\)\.service\.d$/\1/p'|sort|tr '\n' ' ';}
outside(){ diff $T/cap/before $T/cap/after|grep -c .;}
odd(){ ls -A $T/o4 2>/dev/null|grep -vxE "agi-post@\.service|agi-post@($1)\.service\.d|agi-project\.(service|path)|agi-users\.conf|multi-user\.target\.wants"|tr '\n' ' ';}
{ printf -- '---\nposts:\n';row '"good"';rowen '"outer-ok"' '"../../escape"';row '"BAD"';} >$T/cap/posts.in;proj <$T/cap/posts.in
dirs=$(pdirs);d=$(outside);od=$(odd good);nu=$(grep -c . $T/o4/agi-users.conf 2>/dev/null);uc=$(grep -vcE "agi-good([^a-z0-9-]|\$)" $T/o4/agi-users.conf 2>/dev/null);lk=$(grep -rlE 'escape|outer-ok' $T/o4 2>/dev/null|wc -l|tr -d ' ')
ok "ra10-1-engine-name-traversal-is-not-projected outer name valid, engine.name ../../escape: rc $prc (want 0), projected [$dirs] (want exactly [good ]), out-dir entries of another shape [${od% }] (want none: the stray agi-post@.. dir and escape.service.d)" '[ $prc = 0 ]&&[ "$dirs" = "good " ]&&[ -z "$od" ]'
miss=;for n in '../../escape' BAD;do grep 'skipped post name' $T/cap/p.err|grep -qF -- "$n"||miss="$miss $n";done
ok "ra10-1-the-merged-name-and-the-bad-outer-name-are-each-named-on-a-skipped-line-on-stderr missing from stderr: [${miss# }] (want none)" '[ -z "$miss" ]'
ok "ra10-1-nothing-is-written-outside-the-good-shape the tree around the out dir changed by $d line(s) (want 0), entries in the out dir that are not the good shape: [${od% }] (want none)" '[ $d = 0 ]&&[ -z "$od" ]'
ok "ra10-1-users-hold-only-the-good-user agi-users.conf lines $nu (want >= 1), lines naming another user: $uc (want 0); output files holding escape or outer-ok: $lk (want 0)" '[ "$nu" -ge 1 ]&&[ "$uc" = 0 ]&&[ "$lk" = 0 ]'
{ printf -- '---\nposts:\n';row '"good"';rowen '"outer-ok"' '"other"';} >$T/cap/posts.in;proj <$T/cap/posts.in
dirs=$(pdirs);d=$(outside);od=$(odd 'good|other');uc=$(grep -vcE "agi-(good|other)([^a-z0-9-]|\$)" $T/o4/agi-users.conf 2>/dev/null);lk=$(grep -rlE 'outer-ok' $T/o4 2>/dev/null|wc -l|tr -d ' ')
ok "ra10-2-a-valid-different-engine-name-projects-as-the-engine-name (ruled) outer outer-ok, engine.name other: rc $prc (want 0), projected [$dirs] (want exactly [good other ]), nothing outside: $d (want 0), entries not of the good shape: [${od% }] (want none), users naming a third name: $uc (want 0), output files holding outer-ok: $lk (want 0)" '[ $prc = 0 ]&&[ "$dirs" = "good other " ]&&[ $d = 0 ]&&[ -z "$od" ]&&[ "$uc" = 0 ]&&[ "$lk" = 0 ]'
{ printf -- '---\nposts:\n';row '"good"';rowen '"same"' '"same"';} >$T/cap/posts.in;proj <$T/cap/posts.in
dirs=$(pdirs);d=$(outside);od=$(odd 'good|same')
ok "ra10-3-control-an-engine-name-equal-to-the-outer-name-projects and a row with no engine.name (good) projects: rc $prc (want 0), projected [$dirs] (want exactly [good same ]), stderr lines $(wc -l <$T/cap/p.err|tr -d ' ') (want 0), nothing outside: $d (want 0), entries not of the good shape: [${od% }] (want none)" '[ $prc = 0 ]&&[ "$dirs" = "good same " ]&&[ ! -s $T/cap/p.err ]&&[ $d = 0 ]&&[ -z "$od" ]'
{ printf -- '---\nposts:\n';row '"good"';rowen '"BAD"' '"fine"';} >$T/cap/posts.in;proj <$T/cap/posts.in
dirs=$(pdirs);d=$(outside);od=$(odd 'good|fine');lk=$(grep -rl 'BAD' $T/o4 2>/dev/null|wc -l|tr -d ' ')
ok "ra10-4-a-bad-outer-name-with-a-good-engine-name-projects-as-the-engine-name (ruled) outer BAD, engine.name fine: rc $prc (want 0), projected [$dirs] (want exactly [fine good ]), nothing outside: $d (want 0), entries not of the good shape: [${od% }] (want none), output files holding BAD: $lk (want 0)" '[ $prc = 0 ]&&[ "$dirs" = "fine good " ]&&[ $d = 0 ]&&[ -z "$od" ]&&[ "$lk" = 0 ]'
for pair in "$A28:in" "$A29:out" "1abc:out" "a-:in" "Fine:out" "a/b:out";do n=${pair%:*};w=${pair#*:};{ printf -- '---\nposts:\n';rowen '"outer-ok"' "\"$n\"";} >$T/cap/posts.in;proj <$T/cap/posts.in;d=$(outside);[ -d $T/o4/agi-post@$n.service.d ]&&g=in||g=out;[ $w = in ]&&gd=$n||gd=zzz;od=$(odd "$gd")
 ok "ra10-boundary-$w-$(echo $n|cut -c1-8)-len$(printf %s $n|wc -c|tr -d ' ') engine.name [$n] with a valid outer name is $g (want $w), rc $prc (want 0), nothing outside: $d (want 0), entries not of the good shape: [${od% }] (want none)" '[ $g = $w ]&&[ $prc = 0 ]&&[ $d = 0 ]&&[ -z "$od" ]';done
{ printf -- '---\nposts:\n';row '"good"';rowen '"outer-ok"' 'null';rowen '"outer-two"' '7';row '"last"';} >$T/cap/posts.in;proj <$T/cap/posts.in
dirs=$(pdirs);d=$(outside);od=$(odd 'good|last')
ok "ra10-5-an-engine-name-that-is-not-a-string-is-skipped engine.name null and 7 between two good rows (a jq error would abort the stream and drop the later post): rc $prc (want 0), projected [$dirs] (want exactly [good last ]), nothing outside: $d (want 0), entries not of the good shape: [${od% }] (want none), skipped-by-name stderr lines $(grep -c 'skipped post name' $T/cap/p.err) (want >= 2: a jq type error is not a skip named on stderr)" '[ $prc = 0 ]&&[ "$dirs" = "good last " ]&&[ $d = 0 ]&&[ -z "$od" ]&&[ "$(grep -c "skipped post name" $T/cap/p.err)" -ge 2 ]'
echo "restart-bounds: $f FAIL"
exit $f
