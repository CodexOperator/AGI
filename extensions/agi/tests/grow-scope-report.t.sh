#!/bin/sh
# grow-scope-report.t.sh [ROOT] | window: goal:g7.16.1.11.46.10 (U1, doc:brainstorm-unify §2 + §7). The grow gate's SCOPE check in REPORT mode: SCOPE(p) = grow(p) x G, every parent under closure(roots(p)); the ceiling is the post's row cells `grow` + `roots` in .geometry/posts.md, read at the TIP (never the staged tree). An add outside it LANDS, with a commit trailer `Scope: <post> <type> <parent>` and a [scope] notice; the gate's rc is unchanged (report mode never refuses).
# sh + git + ssh-keygen + jq on SCRATCH repos (a fixture trunk that carries the engine's own extensions/agi/{bin,src} and schemas, posts/<P> branches, a DETACHED ~/t, a throwaway key and ring). The pieces come from `sect agi-at|agi-turn|grow.py` of ROOT's .geometry/engine*.md (default the working tree), or PIECES=<file>; never from ~/bin. No network, no root, 0 USD.
# Rows: c* the cells on the REAL posts.md (every v4 row has both; the selection is non-vacuous: an engine key renamed reads RED) · s* agi-at: in scope = no trailer; parent outside roots / type outside grow = trailer + notice + the commit lands + rc 0; a parent walked through STAGED parents (a node added in the same tree; a two-step chain) is inside; `*` admits all; a row without cells and a post without a row admit nothing; the ceiling is read at the TIP (a post that widens itself in the same commit is still reported); a REFUSED add (growth-order) is rc 6 with no trailer; a failing report ([scope-report-broken]) never refuses · t* agi-turn writes the same trailer · m* mutants, each one-edit, each must read RED against the SAME row (a gate that refuses; trailers on in-scope adds; trailers never written; agi-at drops the trailer; the ceiling read from the staged tree; a closure that does not walk) · w* the 24 h window command (`sh grow-scope-report.t.sh window`, falsifier 3 of the leaf): every Scope: commit has a row in the leaf's explain table, and the window holds at least one hit.
# Exit = the number of FAIL lines (99 = the fixture could not be built).
G=/usr/bin/git
R0=${ROOT:-$(cd "$(dirname "$0")/../../.." && pwd)}
if [ "${1:-}" = window ];then   # falsifier 3: run in the real repo, against the leaf node
 L=$R0/.agi/nodes/goal/g7.16.1.11.46.10.md;[ -f "$L" ]||{ echo "FAIL window: $L is missing";exit 99;}
 n=0;bad=
 for h in $($G -C "$R0" log --since='24 hours ago' --grep='^Scope:' --format=%H);do n=$((n+1));grep -q "^| ${h%"${h#??????????}"} " "$L"||bad="$bad ${h%"${h#??????????}"}";done
 [ "$n" -ge 1 ]||{ echo "FAIL window: no commit with a Scope: trailer in the last 24 h (a gate that never writes the trailer cannot pass)";exit 1;}
 [ -z "$bad" ]||{ echo "FAIL window: $n hit(s), unexplained (no row in the leaf's explain table):$bad";exit 1;}
 echo "ok window $n hit(s), every one has an explain row";exit 0;fi
T=$(mktemp -d);trap 'rm -rf $T' 0;f=0
ok(){ if eval "$2";then echo "ok $1";else echo "FAIL $1";f=$((f+1));fi;}
# a row that must read RED: the SAME condition run against a mutated gate has to fail
red(){ if eval "$2";then echo "FAIL $1 (the mutant read GREEN)";f=$((f+1));else echo "ok $1";fi;}
unset GIT_AUTHOR_NAME GIT_AUTHOR_EMAIL GIT_COMMITTER_NAME GIT_COMMITTER_EMAIL GIT_DIR GIT_WORK_TREE GIT_INDEX_FILE AGI_POST AGI_WT RUNTIME_DIRECTORY AGI_TRUNK GROW_TRAILERS
export HOME=$T/hm GIT_CONFIG_GLOBAL=/dev/null GIT_CONFIG_SYSTEM=/dev/null
mkdir -p $T/hm $T/bin $T/mbin $T/run $T/k
sect(){ if [ -n "$PIECES" ];then cat "$PIECES";else cat $R0/.agi/nodes/.geometry/engine*.md;fi|sed -n "/^###* $1 /,/^###* /{/^~~~/,/^~~~/{//!p}}";}
# ---- c*: the cells on the real rows (falsifier 2 of the leaf)
PM=$R0/.agi/nodes/.geometry/posts.md
sel(){ sed -n 's/^  - {/{/p' "$1"|jq -c 'select(.engine.v==4)'; }
nv4=$(sel "$PM"|wc -l|tr -d ' ')
miss=$(sel "$PM"|jq -c 'select((has("grow") and has("roots"))|not)|.name')
ok "c1-every-v4-row-has-both-cells $nv4 v4 row(s); rows lacking grow or roots: [$miss] (want none)" '[ -z "$miss" ]'
ok "c2-the-selection-is-not-vacuous $nv4 v4 row(s) (want >= 15)" '[ "$nv4" -ge 15 ]'
sed 's/"engine": {"v": 4/"enginx": {"v": 4/' "$PM" >$T/pm.mut
red "c3-mutant-an-engine-key-renamed-reads-RED" '[ "$(sel $T/pm.mut|wc -l|tr -d " ")" -ge 15 ]'
tf=$(sel "$PM"|jq -c 'select((.grow|type)!="array" or (.roots|type)!="array" or (.grow|length)==0 or (.roots|length)==0)|.name')
ok "c4-every-cell-is-a-non-empty-list [$tf] (want none)" '[ -z "$tf" ]'
# ---- the pieces
for n in agi-at agi-turn grow.py;do sect $n >$T/bin/$n;[ -s $T/bin/$n ]&&chmod +x $T/bin/$n||{ echo "FAIL extract: $n";exit 99;};done
printf '#!/bin/sh\nexit 0\n' >$T/bin/agi-sync;printf '#!/bin/sh\ncat >/dev/null\nexit 0\n' >$T/bin/agi-notice;chmod +x $T/bin/agi-sync $T/bin/agi-notice
ssh-keygen -q -t ed25519 -N '' -f $T/k/key -C k >/dev/null||{ echo "FAIL fixture: ssh-keygen";exit 99;}
for p in alive wide nocells ghost;do echo "$p@agi namespaces=\"git\" $(cut -d' ' -f1,2 $T/k/key.pub)";done >$T/allowed
# ---- the fixture: PN = the post under test
MT=0000000000000000000000000000
node(){ # node TYPE ID MINT PARENT...  -> the file text
 t=$1;i=$2;m=$3;shift 3;printf -- '---\nid: %s:%s\nmint_id: %s\ntype: %s\nparents:\n' $t $i $m $t;for q in "$@";do printf '  - %s\n' $q;done;printf -- '---\nbody %s\n' $i;}
mk(){ PN=${1:-alive};rm -rf $T/g $T/hm/t;$G init -q -b trunk $T/g;g="$G -C $T/g";$g config user.name $PN;$g config user.email $PN@agi;$g config gpg.format ssh;$g config user.signingkey $T/k/key;$g config commit.gpgsign true
 mkdir -p $T/g/extensions/agi $T/g/.agi/context $T/g/.agi/nodes/goal $T/g/.agi/nodes/hypothesis $T/g/.agi/nodes/experiment $T/g/.agi/nodes/.geometry
 cp -r $R0/extensions/agi/bin $R0/extensions/agi/src $T/g/extensions/agi/;cp -r $R0/.agi/context/schemas $T/g/.agi/context/
 printf -- '---\nid: goal:g1\nmint_id: %s01\ntype: goal\nparents: []\n---\nroot one\n' $MT >$T/g/.agi/nodes/goal/g1.md
 printf -- '---\nid: goal:g2\nmint_id: %s02\ntype: goal\nparents: []\n---\nroot two\n' $MT >$T/g/.agi/nodes/goal/g2.md
 node hypothesis h1 ${MT}03 goal:g1 >$T/g/.agi/nodes/hypothesis/h1.md;node hypothesis h2 ${MT}04 goal:g2 >$T/g/.agi/nodes/hypothesis/h2.md
 printf -- '---\nid: config:posts\nmint_id: %s05\ntype: config\n---\nposts:\n' $MT >$T/g/.agi/nodes/.geometry/posts.md
 cat >>$T/g/.agi/nodes/.geometry/posts.md <<'XX'
  - {"name": "alive", "engine": {"v": 4}, "grow": ["goal", "hypothesis", "experiment"], "roots": ["goal:g1"]}
  - {"name": "wide", "engine": {"v": 4}, "grow": ["*"], "roots": ["*"]}
  - {"name": "nocells", "engine": {"v": 4}}
XX
 $g add -A;$g commit -qm trunk;$g branch posts/$PN trunk;$g worktree add -q --detach $T/hm/t posts/$PN;}
run(){ (cd $T/hm/t&&env -i PATH=${BINP:-$T/bin}:/usr/bin:/bin HOME=$T/hm GIT_CONFIG_GLOBAL=/dev/null GIT_CONFIG_SYSTEM=/dev/null AGI_POST=$PN RUNTIME_DIRECTORY=$T/run AGI_WT=$T/wt AGI_WT_HOLD=101 "$@");}
put(){ mkdir -p "$(dirname "$T/hm/t/$1")";cat >"$T/hm/t/$1";}
tip(){ $G -C $T/g rev-parse posts/$PN;}
msg(){ $G -C $T/g log -1 --format=%B posts/$PN;}
trl(){ msg|grep '^Scope: ';}
ncom(){ $G -C $T/g rev-list --count $1..posts/$PN;}
sig(){ $G -C $T/g -c gpg.ssh.allowedSignersFile=$T/allowed log -1 --format=%G? posts/$PN;}
# scenario: add ONE node by agi-at; sets rc / b0 / the stderr file $T/e
addat(){ b0=$(tip);run agi-at "$@" 2>$T/e;rc=$?;}
hyp(){ node hypothesis "$1" ${MT}1$2 $3 | put .agi/nodes/hypothesis/$1.md;}
# the rows run against whichever pieces PATH points at (BINP); a function so a mutant runs the SAME rows
rows(){ L=$1   # label prefix
 mk alive;hyp hn 1 goal:g1;addat .agi/nodes/hypothesis/hn.md
 ok "${L}s1-in-scope-add-lands-with-no-trailer rc $rc (want 0), $(ncom $b0) commit(s) (want 1), signed [$(sig)] (want G), trailers [$(trl)] (want none), [scope] notices $(grep -c '^\[scope\]' $T/e) (want 0)" '[ $rc = 0 ]&&[ "$(ncom $b0)" = 1 ]&&[ "$(sig)" = G ]&&[ -z "$(trl)" ]&&[ "$(grep -c "^\[scope\]" $T/e)" = 0 ]'
 mk alive;hyp hn 1 goal:g2;addat .agi/nodes/hypothesis/hn.md
 ok "${L}s2-a-parent-outside-roots-lands-with-the-trailer rc $rc (want 0), $(ncom $b0) commit(s) (want 1), trailer [$(trl)] (want 'Scope: alive hypothesis goal:g2'), the notice names it: $(grep -c '^\[scope\] alive hypothesis goal:g2: parent outside roots (reported, not refused)' $T/e) (want 1), signed [$(sig)]" '[ $rc = 0 ]&&[ "$(ncom $b0)" = 1 ]&&[ "$(trl)" = "Scope: alive hypothesis goal:g2" ]&&[ "$(grep -c "^\[scope\] alive hypothesis goal:g2: parent outside roots (reported, not refused)" $T/e)" = 1 ]&&[ "$(sig)" = G ]'
 ok "${L}s2b-the-trailer-is-the-last-paragraph-after-a-blank-line the commit message: [$(msg|tr '\n' '|')]" '[ "$(msg|sed -n 1p|cut -c1-6)" = "alive:" ]&&[ "$(msg|sed -n 2p)" = "" ]&&[ "$(msg|sed -n 3p)" = "Scope: alive hypothesis goal:g2" ]&&[ "$($G -C $T/g log -1 --format="%(trailers:key=Scope,valueonly)" posts/$PN|grep -c .)" = 1 ]'
 mk alive;node idea ix ${MT}16 goal:g1 | put .agi/nodes/idea/ix.md;addat .agi/nodes/idea/ix.md
 ok "${L}s3-a-type-outside-grow-lands-with-the-trailer rc $rc (want 0), $(ncom $b0) commit(s), trailer [$(trl)] (want 'Scope: alive idea goal:g1'), notice: $(grep -c 'type idea not in grow' $T/e) (want 1)" '[ $rc = 0 ]&&[ "$(ncom $b0)" = 1 ]&&[ "$(trl)" = "Scope: alive idea goal:g1" ]&&[ "$(grep -c "type idea not in grow" $T/e)" = 1 ]'
 mk alive;hyp hn 1 goal:g1;node experiment xn ${MT}17 hypothesis:hn | put .agi/nodes/experiment/xn.md;addat .agi/nodes/hypothesis/hn.md .agi/nodes/experiment/xn.md
 ok "${L}s4-a-parent-added-in-the-same-tree-is-walked rc $rc (want 0), $(ncom $b0) commit(s), trailers [$(trl)] (want none: hn is under goal:g1, xn under hn)" '[ $rc = 0 ]&&[ "$(ncom $b0)" = 1 ]&&[ -z "$(trl)" ]'
 mk alive;node experiment xe ${MT}18 hypothesis:h1 | put .agi/nodes/experiment/xe.md;addat .agi/nodes/experiment/xe.md
 ok "${L}s4b-a-two-step-chain-in-the-tip-is-walked rc $rc (want 0), trailers [$(trl)] (want none: experiment -> h1 -> goal:g1)" '[ $rc = 0 ]&&[ -z "$(trl)" ]'
 mk alive;node experiment xo ${MT}19 hypothesis:h2 | put .agi/nodes/experiment/xo.md;addat .agi/nodes/experiment/xo.md
 ok "${L}s4c-a-two-step-chain-leaving-the-roots-is-reported rc $rc (want 0), trailer [$(trl)] (want 'Scope: alive experiment hypothesis:h2')" '[ $rc = 0 ]&&[ "$(trl)" = "Scope: alive experiment hypothesis:h2" ]'
 mk wide;node idea iw ${MT}20 goal:g2 | put .agi/nodes/idea/iw.md;addat .agi/nodes/idea/iw.md
 ok "${L}s5-a-star-row-admits-everything rc $rc (want 0), $(ncom $b0) commit(s), trailers [$(trl)] (want none)" '[ $rc = 0 ]&&[ "$(ncom $b0)" = 1 ]&&[ -z "$(trl)" ]'
 mk nocells;hyp hn 1 goal:g1;addat .agi/nodes/hypothesis/hn.md
 ok "${L}s6-a-row-without-cells-admits-nothing rc $rc (want 0), $(ncom $b0) commit(s), trailer [$(trl)] (want 'Scope: nocells hypothesis goal:g1'), notice: $(grep -c 'no grow/roots cells on the row' $T/e) (want 1)" '[ $rc = 0 ]&&[ "$(ncom $b0)" = 1 ]&&[ "$(trl)" = "Scope: nocells hypothesis goal:g1" ]&&[ "$(grep -c "no grow/roots cells on the row" $T/e)" = 1 ]'
 mk ghost;hyp hn 1 goal:g1;addat .agi/nodes/hypothesis/hn.md
 ok "${L}s6b-a-post-with-no-row-admits-nothing rc $rc (want 0), $(ncom $b0) commit(s), trailer [$(trl)] (want 'Scope: ghost hypothesis goal:g1')" '[ $rc = 0 ]&&[ "$(ncom $b0)" = 1 ]&&[ "$(trl)" = "Scope: ghost hypothesis goal:g1" ]'
 mk alive;hyp hn 1 goal:g2;sed -i 's|"roots": \["goal:g1"\]|"roots": ["*"]|' $T/hm/t/.agi/nodes/.geometry/posts.md;addat .agi/nodes/hypothesis/hn.md .agi/nodes/.geometry/posts.md
 ok "${L}s7-the-ceiling-is-read-at-the-TIP-not-the-staged-tree a post that widens its own roots in the same commit is still reported: rc $rc (want 0), trailer [$(trl)] (want 'Scope: alive hypothesis goal:g2')" '[ $rc = 0 ]&&[ "$(trl)" = "Scope: alive hypothesis goal:g2" ]'
 mk alive;node experiment xr ${MT}21 goal:g1 | put .agi/nodes/experiment/xr.md;addat .agi/nodes/experiment/xr.md
 ok "${L}s8-a-refused-add-is-rc-6-with-no-commit-and-no-trailer rc $rc (want 6), the tip $([ $(tip) = $b0 ]&&echo unchanged||echo MOVED), growth-order lines $(grep -c '^\[growth-order\]' $T/e) (want 1), scope lines $(grep -c '^\[scope\]' $T/e) (want 0)" '[ $rc = 6 ]&&[ $(tip) = $b0 ]&&[ "$(grep -c "^\[growth-order\]" $T/e)" = 1 ]&&[ "$(grep -c "^\[scope\]" $T/e)" = 0 ]'
 mk alive;hyp hn 1 goal:g2;$G -C $T/g rm -q .agi/nodes/.geometry/posts.md;$G -C $T/g commit -qm "no posts.md";$G -C $T/g update-ref refs/heads/posts/alive trunk;$G -C $T/hm/t checkout -q --detach posts/alive;hyp hn 1 goal:g2;addat .agi/nodes/hypothesis/hn.md
 ok "${L}s9-no-posts-md-at-the-tip-is-silent rc $rc (want 0), $(ncom $b0) commit(s) (want 1), trailers [$(trl)] (want none), bracketed lines $(grep -c '^\[' $T/e) (want 0)" '[ $rc = 0 ]&&[ "$(ncom $b0)" = 1 ]&&[ -z "$(trl)" ]&&[ "$(grep -c "^\[" $T/e)" = 0 ]'
 mk alive;hyp hn 1 goal:g2;mkdir -p $T/shim;printf '#!/bin/sh\ncase "$*" in *"show "*posts.md*) echo "fatal: simulated show failure" >&2;exit 128;; esac\nexec /usr/bin/git "$@"\n' >$T/shim/git;chmod +x $T/shim/git;sb=$BINP;BINP=$T/shim:${BINP:-$T/bin};addat .agi/nodes/hypothesis/hn.md;BINP=$sb
 ok "${L}s9b-a-failing-report-never-refuses (posts.md unreadable at the tip) rc $rc (want 0), $(ncom $b0) commit(s) (want 1), [scope-report-broken] lines $(grep -c '^\[scope-report-broken\]' $T/e) (want 1)" '[ $rc = 0 ]&&[ "$(ncom $b0)" = 1 ]&&[ "$(grep -c "^\[scope-report-broken\]" $T/e)" = 1 ]'
}
# ---- t*: agi-turn writes the same trailer (a node tree in AGI_WT)
turn(){ L=$1;mk alive;rm -rf $T/wt;mkdir -p $T/wt/m1/.agi/nodes/hypothesis;node hypothesis ht ${MT}30 goal:g2 >$T/wt/m1/.agi/nodes/hypothesis/ht.md;echo .agi/nodes/hypothesis/ht.md >$T/wt/m1/.p;b0=$(tip);run agi-turn 2>$T/e;rc=$?
 ok "${L}t1-agi-turn-commits-the-out-of-scope-add-with-the-trailer rc $rc (want 0), $(ncom $b0) commit(s) (want 1), trailer [$(trl)] (want 'Scope: alive hypothesis goal:g2'), signed [$(sig)]" '[ $rc = 0 ]&&[ "$(ncom $b0)" = 1 ]&&[ "$(trl)" = "Scope: alive hypothesis goal:g2" ]&&[ "$(sig)" = G ]'
 mk alive;rm -rf $T/wt;mkdir -p $T/wt/m1/.agi/nodes/hypothesis;node hypothesis ht ${MT}31 goal:g1 >$T/wt/m1/.agi/nodes/hypothesis/ht.md;echo .agi/nodes/hypothesis/ht.md >$T/wt/m1/.p;b0=$(tip);run agi-turn 2>$T/e;rc=$?
 ok "${L}t2-agi-turn-in-scope-has-no-trailer rc $rc (want 0), $(ncom $b0) commit(s) (want 1), trailers [$(trl)] (want none)" '[ $rc = 0 ]&&[ "$(ncom $b0)" = 1 ]&&[ -z "$(trl)" ]';}
rows "";turn ""
# ---- m*: one-edit mutants; each runs the SAME rows and must make at least one FAIL (a mutant reads RED)
mut(){ # mut NAME PIECE 'sed-expr'  -> BINP = a copy of the pieces with ONE edit; counts the rows' FAILs
 rm -rf $T/mbin;mkdir -p $T/mbin;cp $T/bin/* $T/mbin/;sed "$3" $T/bin/$2 >$T/mbin/$2;chmod +x $T/mbin/$2
 if cmp -s $T/bin/$2 $T/mbin/$2;then echo "FAIL m-$1: the mutation did not change $2 (anchor drifted)";f=$((f+1));return;fi
 f0=$f;BINP=$T/mbin;rows "m-$1/" >$T/mo 2>&1;turn "m-$1/" >>$T/mo 2>&1;BINP=;nf=$(grep -c '^FAIL' $T/mo);f=$f0
 if [ "$nf" -ge 1 ];then echo "ok m-$1 reads RED ($nf row(s) failed: $(grep '^FAIL' $T/mo|cut -d' ' -f2|head -3|tr '\n' ' '))";else echo "FAIL m-$1 read GREEN";f=$((f+1));fi;}
mut a-gate-that-refuses-on-a-hit grow.py 's/(reported, not refused)"%(post,t,y,w),file=sys.stderr)/&;1\/0/;s/except BaseException as e:print("\[scope-report-broken\] "+repr(e)\[:120\],file=sys.stderr)/&;b=1/'
mut trailers-on-in-scope-adds grow.py 's/^  if w:$/  if 1:/'
mut trailers-never-written grow.py 's|open(os.environ\["GROW_TRAILERS"\],"a")|open("/dev/null","a")|'
mut agi-at-drops-the-trailer agi-at 's/\[ -s \$x\.s \]&&{ echo;cat \$x\.s;};//'
mut agi-turn-drops-the-trailer agi-turn 's/\[ -s \$x\.s \]&&{ echo;cat \$x\.s;};//'
mut ceiling-read-from-the-staged-tree grow.py 's|tip+":.agi/nodes/.geometry/posts.md"|":.agi/nodes/.geometry/posts.md"|'
mut a-closure-that-does-not-walk grow.py 's/  return any(up(z,s) for z in ((y or {}).get("parents") or \[\]))/  return 0/'
mut a-closure-that-admits-everything grow.py 's/if "\*" in R or x in R:return 1/return 1/'
# ---- w*: the window command, on a scratch repo + a fixture leaf
mkw(){ rm -rf $T/w;$G init -q -b trunk $T/w;mkdir -p $T/w/.agi/nodes/goal $T/w/extensions/agi/tests;$G -C $T/w config user.name w;$G -C $T/w config user.email w@agi;$G -C $T/w config commit.gpgsign false;cp "$0" $T/w/extensions/agi/tests/grow-scope-report.t.sh;printf '| row |\n' >$T/w/.agi/nodes/goal/g7.16.1.11.46.10.md;$G -C $T/w add -A;$G -C $T/w commit -qm base;}
win(){ ROOT=$T/w sh $T/w/extensions/agi/tests/grow-scope-report.t.sh window >$T/wo 2>&1;}
mkw;win;wr=$?;ok "w1-an-empty-window-is-RED (no commit with a Scope: trailer)" '[ $wr != 0 ]&&grep -q "no commit with a Scope: trailer" $T/wo'
printf 'x\n' >$T/w/x;$G -C $T/w add -A;$G -C $T/w commit -qm "alive: x

Scope: alive hypothesis goal:g2";h=$($G -C $T/w rev-parse HEAD);win;wr=$?;ok "w2-a-hit-with-no-explain-row-is-RED [$(cat $T/wo)]" '[ $wr != 0 ]&&grep -q "unexplained" $T/wo'
printf '| %s | alive | hypothesis | goal:g2 | planted |\n' "$(echo $h|cut -c1-10)" >>$T/w/.agi/nodes/goal/g7.16.1.11.46.10.md;win;wr=$?;ok "w3-a-hit-with-an-explain-row-is-GREEN [$(cat $T/wo)]" '[ $wr = 0 ]'
exit $f
