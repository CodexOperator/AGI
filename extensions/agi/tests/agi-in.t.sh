#!/bin/sh
# agi-in.t.sh: goal:g7.16.1.11.46.21 U3 (doc:brainstorm-unify §3, §24): ONE kid spawn verb, `agi-in <capsule> <kid> <prompt>`, the capsule's MANIFEST `pull` picks the class; `agi-wt pull` honours its `reach`.
# sh + git + jq + ssh-keygen only, scratch HOME, throwaway key, a STUB pi (logs one line per launch), no network, no root, 0 USD. One ok/FAIL line per case; exit = number of FAILs; 99 = the fixture itself is broken.
# PIECE = agi-in under test (default: `sect agi-in` of ROOT's .geometry), WT = agi-wt (default: `sect agi-wt`). A mutant row runs an edited copy and passes only when the clean row's condition is FALSE for it.
# Rows: r1-r3 one launch per pull value · r4-r7 the reach arm of agi-wt · r8 an unreadable capsule · r9 atoms round-trip · r10 no scratch dir · rb an unknown pull · rc a missing / unknown reach · rd pack refuses bad values · n1 n2 the repo bytes (F2).
T=$(mktemp -d);trap 'rm -rf $T' 0;f=0;G=/usr/bin/git;R0=${ROOT:-$(cd "$(dirname "$0")/../../.." && pwd)}
sect(){ cat $R0/.agi/nodes/.geometry/engine*.md|sed -n "/^###* $1 /,/^###* /{/^~~~/,/^~~~/{//!p}}";}
[ -n "$PIECE" ]||{ sect agi-in>$T/agi-in;PIECE=$T/agi-in;};[ -n "$WT" ]||{ sect agi-wt>$T/agi-wt;WT=$T/agi-wt;}
[ -s $PIECE ]&&[ -s $WT ]&&[ -n "$(sect capsule)" ]||{ echo "FAIL extract: agi-in $(wc -c<$PIECE) B, agi-wt $(wc -c<$WT) B, capsule $(sect capsule|wc -c) B";exit 99;}
ok(){ if eval "$3";then echo "ok $1: $2";else echo "FAIL $1: $2";f=$((f+1));fi;}   # 3-arg: name, description, condition
mut(){ sed "$2" $1>$3;cmp -s $1 $3&&{ echo "FAIL fixture: mutant $4 matched nothing: $2";exit 99;};:;}   # mut SRC SED OUT NAME (measured: a drifted literal is a broken fixture, never a green)
unset GIT_AUTHOR_NAME GIT_AUTHOR_EMAIL GIT_COMMITTER_NAME GIT_COMMITTER_EMAIL GIT_DIR GIT_WORK_TREE;H=$T/home;mkdir -p $H/.ssh $T/bin $T/run;LOG=$T/log;: >$LOG
ssh-keygen -q -t ed25519 -N '' -f $H/.ssh/id_ed25519 -C inv>/dev/null;echo "inv@agi namespaces=\"git\" $(cut -d' ' -f1,2 $H/.ssh/id_ed25519.pub)">$T/allowed
printf '[user]\n\tname=inv\n\temail=inv@agi\n\tsigningkey=%s\n[gpg]\n\tformat=ssh\n[gpg "ssh"]\n\tallowedSignersFile=%s\n[safe]\n\tdirectory=*\n' $H/.ssh/id_ed25519 $T/allowed>$H/.gitconfig
cat >$T/bin/pi<<'XX'
#!/bin/sh
echo "launch|$*|post=$AGI_POST|cap=$AGI_CAPSULE|home=$HOME|git=$(git rev-parse --is-inside-work-tree 2>/dev/null||echo no)">>$LOG
XX
printf '#!/bin/sh\ncat %s/.agi/nodes/.geometry/engine*.md|sed -n "/^###* $1 /,/^###* /{/^~~~/,/^~~~/{//!p}}"\n' $R0>$T/bin/sect;chmod +x $T/bin/*
export GIT_CONFIG_GLOBAL=$H/.gitconfig GIT_CONFIG_SYSTEM=/dev/null HOME=$H PATH=$T/bin:$PATH LOG RUNTIME_DIRECTORY=$T/run AGI_ALLOWED=$T/allowed AGI_KID_MODEL=stub AGI_TRUNK=HEAD AGI_WT_HOLD=101   # the disk hold is not under test here
# the invoker's repo ~/t: goal:a (root) > goal:b; goal:x elsewhere; the kids' own cards
M1=11111111111111111111111111111111;M2=22222222222222222222222222222222;M3=33333333333333333333333333333333;M4=44444444444444444444444444444444;M5=55555555555555555555555555555555
$G init -q $H/t;cd $H/t;mkdir -p .agi/nodes/goal .agi/nodes/doc
node(){ printf -- '---\nid: %s\nmint_id: %s\ntype: %s\nparents:\n  - %s\nnext_edges: []\n---\nbody\n' "$1" "$2" "${1%%:*}" "$3">.agi/nodes/${1%%:*}/${1#*:}.md;}
node goal:a $M1 goal:root;node goal:b $M2 goal:a;node goal:x $M3 goal:root;node doc:card-g1 $M4 goal:root;node doc:card-d1 $M5 goal:root
$G add -A;$G commit -qm base;for p in g1 d1 o1 x1 j1;do $G branch -q posts/$p;done;cd $T
pk(){ AGI_POST=inv sh $PIECE pack $M1 subtree $M1 "$@";}                 # agi-in pack: the one writer of the spawn lines
raw(){ (cd $H/t&&AGI_POST=inv AGI_MF="$1" sh -c 'sect capsule|sh -s -- pack '$M1' subtree '$M1);}   # the capsule piece alone: a MANIFEST agi-in pack would refuse to write
CG=$(pk --pull graph --reach closed);CD=$(pk --pull director --reach closed);CN=$(pk --pull none);CO=$(pk --pull graph --reach open);CX=$(pk --pull graph)
CU=$(raw 'pull graf');CR=$(raw 'pull graph
reach ajar');C0=$(raw '')
for c in CG CD CN CO CX CU CR C0;do eval v=\$$c;[ ${#v} = 32 ]||{ echo "FAIL fixture: capsule $c not packed [$v]";exit 99;};done
mf(){ $G -C $H/t show refs/capsule/$1:MANIFEST;}
ok r0-pack-writes-the-spawn-lines "CG's MANIFEST reads pull graph + reach closed, CN's pull none and no reach, C0 (no AGI_MF) neither line" 'mf $CG|grep -qx "pull graph"&&mf $CG|grep -qx "reach closed"&&mf $CN|grep -qx "pull none"&&! mf $CN|grep -q "^reach "&&! mf $C0|grep -qE "^(pull|reach|scope|at) "'
# launches: run agi-in, count the stub's lines
L(){ : >$LOG;sh ${P:-$PIECE} "$@" >$T/o 2>$T/e;echo $? >$T/rc;}
n(){ grep -c '^launch|' $LOG;}
L $CG g1 "do g";G1=$(cat $LOG)
ok r1-pull-graph-launches-ONE-pi-kid "1 launch (got $(n)) as post g1 in its own tree, carrying AGI_CAPSULE=CG, --skill + cccc.ts" '[ $(n) = 1 ]&&echo "$G1"|grep -q "post=g1|cap=$CG|home=$H/k/g1|git=true"&&echo "$G1"|grep -q -- "--skill skills -e"&&[ -d $H/k/g1/t ]'
L $CD d1 "do d";D1=$(cat $LOG)
ok r2-pull-director-launches-ONE-pi-kid "1 launch (got $(n)) as post d1, AGI_CAPSULE=CD" '[ $(n) = 1 ]&&echo "$D1"|grep -q "post=d1|cap=$CD|home=$H/k/d1|git=true"'
L $CN n1 "one question";N1=$(cat $LOG)
ok r3-pull-none-is-ONE-request-no-tools-no-tree "1 launch (got $(n)) with --no-tools, no --skill, no repo, no kid home" '[ $(n) = 1 ]&&echo "$N1"|grep -q -- "--no-tools -p one question"&&! echo "$N1"|grep -q -- "--skill"&&echo "$N1"|grep -q "git=no"&&[ ! -d $H/k/n1 ]'
# reach: agi-wt pull under AGI_CAPSULE, as the kid
W(){ (cd $T;AGI_POST=$1 AGI_CAPSULE=$2 AGI_WT=$T/wt-$1-$3 sh ${Q:-$WT} pull $3 >$T/wo 2>$T/we;echo $? >$T/wrc);cat $T/wrc;}
ok r4-closed-reach-pulls-a-member "goal:b is a member of CG: rc $(W g1 $CG goal:b) (want 0)" '[ $(W g1 $CG goal:b) = 0 ]&&[ -f $T/wt-g1-goal:b/$M2/.agi/nodes/goal/b.md ]'
ok r5-closed-reach-refuses-a-non-member-by-name "goal:x is not a member: rc $(W g1 $CG goal:x) (want 3), stderr [$(cat $T/we)]" '[ $(W g1 $CG goal:x) = 3 ]&&grep -qx "agi-wt: refused: goal:x outside closed reach $CG" $T/we&&[ ! -d $T/wt-g1-goal:x/$M3 ]'
ok r6-closed-reach-pulls-the-posts-own-card "doc:card-g1 under CG as g1: rc $(W g1 $CG doc:card-g1) (want 0)" '[ $(W g1 $CG doc:card-g1) = 0 ]'
ok r7-pull-director-pulls-nothing "goal:b (a member) under CD: rc $(W d1 $CD goal:b) (want 3), stderr [$(cat $T/we)]" '[ $(W d1 $CD goal:b) = 3 ]&&grep -q "capsule $CD is not pull graph (ask over box)" $T/we'
ok r7b-open-reach-pulls-any-mint "goal:x under CO: rc $(W o1 $CO goal:x) (want 0)" '[ $(W o1 $CO goal:x) = 0 ]'
# unreadable
B=99999999999999999999999999999999;L $B u1 "x"
ok r8-an-unreadable-capsule-is-unread-rc-1-no-launch "a CID with no ref: rc $(cat $T/rc) (want 1), [$(cat $T/o)], $(n) launch(es)" '[ $(cat $T/rc) = 1 ]&&grep -qx "unread: capsule $B" $T/o&&[ $(n) = 0 ]'
ok r8b-agi-wt-under-an-unreadable-capsule-is-unread "rc $(W j1 $B goal:b) (want 1)" '[ $(W j1 $B goal:b) = 1 ]&&grep -qx "unread: capsule $B" $T/we'
L $C0 u2 "x"
ok r8c-a-capsule-with-no-pull-line-launches-nothing "rc $(cat $T/rc) (want 1), [$(cat $T/o)], $(n) launch(es)" '[ $(cat $T/rc) = 1 ]&&grep -qx "unread: pull in $C0" $T/o&&[ $(n) = 0 ]'
# atoms
printf '{"atoms":[{"id":"a1","src":"owner 10-08","slice":"one","sha":"0123456789ab"},{"id":"a2","src":"belam","slice":"two","sha":"ba9876543210"}]}\n'>$T/args.json
CA=$(pk --pull none --atoms $T/args.json);want=$(printf 'atoms:\n'; jq -r '.atoms[]|"  \(.id) \(.src) \(.sha)"' $T/args.json)
ok r9-atoms-round-trip-byte-equal "the MANIFEST's atoms: block equals the ARGS' atoms, line for line" '[ "$(mf $CA|sed -n "/^atoms:$/,\$p"|grep -E "^(atoms:|  )")" = "$want" ]'
# sp's fail-closed rows
L $CU u3 "x"
ok rb-an-unknown-pull-is-unread-rc-1-no-launch "pull graf: rc $(cat $T/rc) (want 1), [$(cat $T/o)], $(n) launch(es)" '[ $(cat $T/rc) = 1 ]&&grep -qx "unread: pull in $CU" $T/o&&[ $(n) = 0 ]'
ok rc-a-missing-reach-reads-closed "CX (no reach line) pulls goal:x: rc $(W x1 $CX goal:x) (want 3)" '[ $(W x1 $CX goal:x) = 3 ]'
ok rc2-an-unknown-reach-reads-closed "CR (reach ajar) pulls goal:x: rc $(W x1 $CR goal:x) (want 3)" '[ $(W x1 $CR goal:x) = 3 ]'
pk --pull graf >/dev/null 2>&1;p1=$?;pk --pull graph --reach ajar >/dev/null 2>&1;p2=$?;pk --pull graph --at 'x;y' >/dev/null 2>&1;p3=$?;pk --pull graph --at 0zz >/dev/null 2>&1;p4=$?;pk --pull graph --scope 0zz >/dev/null 2>&1;p5=$?
ok rd-pack-refuses-a-bad-value "pull graf rc $p1, reach ajar rc $p2, at 'x;y' rc $p3, at 0zz rc $p4, scope 0zz rc $p5 (want 2 2 2 2 2: a non-hex char ANYWHERE in --at / --scope, alive R3)" '[ "$p1 $p2 $p3 $p4 $p5" = "2 2 2 2 2" ]'
mkdir -p $T/nomk;printf '#!/bin/sh\nexit 1\n'>$T/nomk/mktemp;chmod +x $T/nomk/mktemp   # mktemp fails, nothing else does (a missing TMPDIR also stops the capsule's ssh signature check first)
(export PATH=$T/nomk:$PATH;L $CN n2 "q")
ok r10-pull-none-without-a-scratch-dir-is-unread "mktemp fails: rc $(cat $T/rc) (want 1), [$(cat $T/o)], $(n) launch(es) (want 0; alive R2)" '[ $(cat $T/rc) = 1 ]&&grep -qx "unread: no scratch dir" $T/o&&[ $(n) = 0 ]'
# F2, over the REPO bytes: the installer reads every ### fence of engine.md + engine-[pw]*.md (engine-root.md's AGI_PIECE_GLOB)
fence(){ (cd $1/.agi/nodes/.geometry&&cat engine.md engine-[pw]*.md)|grep -c '^### agi-kid ';}
ok n1-no-agi-kid-fence-over-the-installers-glob "$(fence $R0) fence(s) (want 0)" '[ $(fence $R0) = 0 ]'
dsk(){ grep -c 'agi-in <capsule>' $1;}
ok n2-the-dispatch-skill-names-agi-in "skills/agi-dispatch names 'agi-in <capsule>' $(dsk $R0/skills/agi-dispatch/SKILL.md) time(s) (want >= 1)" '[ $(dsk $R0/skills/agi-dispatch/SKILL.md) -ge 1 ]'
# mutants: each must make its clean row's condition FALSE
mut $WT 's/= open ]||echo/!= open ]||echo/' $T/m1 reach-forced-open
ok m1-reach-forced-open-pulls-the-non-member-RED "mutant rc $(Q=$T/m1 W g1 $CG goal:x) (r5 wants 3)" '[ "$(Q=$T/m1 W g1 $CG goal:x)" != 3 ]'
mut $PIECE 's/case $(echo "$M"|sed -n .s\/^pull \/\/p.) in/case graph in/' $T/m2 pull-ignored
P=$T/m2 L $CN m2 "q";ok m2-pull-ignored-launches-a-kid-for-none-RED "mutant: $(n) launch(es), [$(cat $LOG)]" '! grep -q -- "--no-tools" $LOG'
P=$T/m2 L $CU m2b "q";ok m2b-pull-ignored-launches-on-an-unknown-pull-RED "mutant: $(n) launch(es) (rb wants 0)" '[ $(n) != 0 ]'
mut $PIECE 's/AGI_CAPSULE=$c exec pi/AGI_CAPSULE=$c pi $K -p again<\/dev\/null;exec pi/' $T/m3 second-launch
P=$T/m3 L $CG m3 "q";ok m3-a-second-launch-per-call-RED "mutant: $(n) launch(es) (r1 wants 1)" '[ $(n) != 1 ]'
mut $PIECE 's/echo "unread: capsule $c";exit 1/echo "unread: capsule $c";exit 0/' $T/m4 unread-exits-0
P=$T/m4 L $B m4 "q";ok m4-the-unread-exiting-0-RED "mutant rc $(cat $T/rc) (r8 wants 1)" '[ $(cat $T/rc) != 1 ]'
mut $PIECE 's/\*)echo "unread: pull in $c";exit 1;;/*);;/' $T/m5 default-arm-graph
P=$T/m5 L $CU m5 "q";ok m5-the-default-arm-launching-RED "mutant: $(n) launch(es) on pull graf (rb wants 0)" '[ $(n) != 0 ]'
mut $WT 's/= open ]||echo/!= closed ]||echo/' $T/m6 reach-default-open
ok m6-reach-defaulting-open-pulls-RED "mutant: CX rc $(Q=$T/m6 W x1 $CX goal:x), CR rc $(Q=$T/m6 W x1 $CR goal:x) (rc wants 3 3)" '[ "$(Q=$T/m6 W x1 $CX goal:x)" != 3 ]&&[ "$(Q=$T/m6 W x1 $CR goal:x)" != 3 ]'
mut $PIECE 's/W=$(mktemp -d)||{ echo "unread: no scratch dir";exit 1;};/W=$(mktemp -d);/' $T/m9 scratch-guard-dropped
(export PATH=$T/nomk:$PATH;P=$T/m9 L $CN m9 "q");ok m9-the-scratch-guard-dropped-launches-RED "mutant: $(n) launch(es) (r10 wants 0)" '[ $(n) != 0 ]'
mkdir -p $T/r7/.agi/nodes;cp -r $R0/.agi/nodes/.geometry $T/r7/.agi/nodes/;printf '\n### agi-kid (2 B)\n~~~sh\nx\n~~~\n'>>$T/r7/.agi/nodes/.geometry/engine-wrap.md
ok m7-the-fence-re-added-RED "mutant tree: $(fence $T/r7) fence(s) (n1 wants 0)" '[ $(fence $T/r7) != 0 ]'
grep -v 'agi-in <capsule>' $R0/skills/agi-dispatch/SKILL.md>$T/m8;cmp -s $T/m8 $R0/skills/agi-dispatch/SKILL.md&&{ echo "FAIL fixture: mutant m8 removed nothing";exit 99;}
ok m8-the-dispatch-line-removed-RED "mutant skill: $(dsk $T/m8) (n2 wants >= 1)" '[ $(dsk $T/m8) = 0 ]'
echo "agi-in: $f FAIL";exit $f
