#!/bin/sh
# agi-project-harness.t.sh: goal:g7.31.1.7.1 (DG1 11-12; the plan-master umbrella's leaf 1). agi-project (config:engine, sect agi-project) decides each v4 row's H by its
# `harness`: ^pi and ^claude as before, grok-bot -> `grok-bot --model <model>` (NO approval flag), ANYTHING ELSE (a harness it does not know, none, copilot-cli) -> NO unit and ONE
# named skip line on stderr; and it removes the h.conf of every agi-post@/agi-boxwake@ instance it did not write THIS run (agi-project.path re-runs into the same /run dir), FAIL CLOSED:
# an unreadable / empty posts.md, a row that does not parse, a row line the sed does not read, AGI_BOX unset / empty / named by no row -> rc != 0, nothing removed.
# sh + git + jq on SCRATCH repos (a copy of the engine*.md under test), no systemd, no root, no network, 0 USD. The section is run the way config:engine :73 runs it:
# `sect agi-project | AGI_BOX=<box> sh -s $o $R`. ROOT=<repo> where engine*.md is read (default: this checkout); BASE=<rev in ROOT> the trunk's engine*.md for the byte-identical rows
# (default: HEAD's first parent, else HEAD). Each row has a MUTANT of the section text that must read RED for that row (a mutant that changes nothing is itself a FAIL).
T=$(mktemp -d);f=0;R0=${ROOT:-$(cd "$(dirname "$0")/../../.." && pwd)};trap 'rm -rf $T' 0
ok(){ if (eval "$2");then echo "ok $1";else echo "FAIL $1";f=$((f+1));fi;}
G=/usr/bin/git;GD=.agi/nodes/.geometry
sec(){ cat $1/engine*.md|sed -n '/^### agi-project /,/^##/{/^~~~/,/^~~~/{//!p}}';}
mkdir -p $T/cur $T/base;cp $R0/$GD/engine*.md $T/cur/;sec $T/cur>$T/sec
B=${BASE:-$($G -C $R0 rev-parse -q --verify HEAD^ 2>/dev/null||$G -C $R0 rev-parse HEAD)}
for x in $($G -C $R0 ls-tree --name-only $B $GD/|sed -n 's|.*/\(engine[^/]*\.md\)$|\1|p');do $G -C $R0 show $B:$GD/$x>$T/base/$x;done;sec $T/base>$T/sec.base
[ -s $T/sec ]&&[ -s $T/sec.base ]||{ echo "FAIL extract: section $(wc -c<$T/sec) B, base $(wc -c<$T/sec.base) B";exit 99;}
row(){ printf '  - {"name":"%s","role":"parent","tier":3,"box":"%s","engine":{"v":4%s,"model":"%s","effort":"high"}}\n' "$1" "$3" "${2:+,\"harness\":\"$2\"}" "${4:-m1}";}
hdr(){ printf -- '---\nid: config:posts\nposts:\n';}
# repo NAME: a scratch repo with the engine*.md under test (or $2 = a dir holding the base's) and the posts body on stdin
repo(){ d=$T/$1;$G init -q $d;mkdir -p $d/$GD;cp ${2:-$T/cur}/engine*.md $d/$GD/;cat>$d/$GD/posts.md;$G -C $d add -A;$G -C $d -c user.name=x -c user.email=x@x commit -qm f;}
FULL(){ hdr;row c1 claude-code bx m1;row p1 pi bx m2;row g1 grok-bot bx grok-4.7;row f1 foo bx;row n1 "" bx;row k1 copilot-cli bx;row o1 claude-code ox;row l1 claude-code local-town;printf -- 'end: 1\n---\n';}
pj(){ s=$1;r=$2;o=$3;b=$4;mkdir -p $o;if [ "$b" = UNSET ];then (cd $r&&env -u AGI_BOX sh $s $o HEAD) 2>$o.err;else (cd $r&&AGI_BOX=$b sh $s $o HEAD) 2>$o.err;fi;rc=$?;}
# the rows, against a section file ($1); each prints ok/FAIL lines; fails are counted in the caller
rows(){ S=$1;L=$2;t=$T/run.$L;rm -rf $t;mkdir -p $t
 pj $S $T/full $t/a bx;rA=$rc
 ok "$L-grok-h-is-exactly-grok-bot-model" '[ "$(sed -n "s/^Environment=\"H=\([^\"]*\)\".*/\1/p" $t/a/agi-post@g1.service.d/h.conf)" = "grok-bot --model grok-4.7" ]'
 ok "$L-grok-no-approval-flag" '[ -f $t/a/agi-post@g1.service.d/h.conf ]&&! grep -q -e bypassPermissions -e permission-mode -e always-approve $t/a/agi-post@g1.service.d/h.conf'
 ok "$L-unknown-harness-makes-no-unit" '[ $rA = 0 ]&&for p in f1 n1 k1;do [ ! -e $t/a/agi-post@$p.service.d ]&&[ ! -e $t/a/agi-boxwake@$p.service.d ]&&! grep -q "agi-$p\b" $t/a/agi-users.conf&&[ -z "$(ls $t/a/multi-user.target.wants|grep "@$p\.")" ]||exit 1;done'
 ok "$L-each-skip-is-one-named-line" '[ $(grep -c "skipped post f1: harness foo has no unit arm" $t/a.err) = 1 ]&&[ $(grep -c "skipped post n1: harness none has no unit arm" $t/a.err) = 1 ]&&[ $(grep -c "skipped post k1: harness copilot-cli has no unit arm" $t/a.err) = 1 ]&&! grep -qi "jq: error" $t/a.err'
 ok "$L-claude-and-pi-h-conf-equal-the-trunks" '[ -f $t/b/agi-post@c1.service.d/h.conf ]||{ pj $T/sec.base $T/full $t/b bx;};for p in c1 p1;do cmp -s $t/a/agi-post@$p.service.d/h.conf $t/b/agi-post@$p.service.d/h.conf&&cmp -s $t/a/agi-boxwake@$p.service.d/h.conf $t/b/agi-boxwake@$p.service.d/h.conf||exit 1;done'
 # STALE: the post first claude-code, then foo, into ONE out dir
 pj $S $T/s1 $t/s bx;pj $S $T/s2 $t/s bx;rS=$rc
 ok "$L-stale-claude-h-conf-is-removed-when-the-row-turns-foo" '[ $rS = 0 ]&&[ ! -e $t/s/agi-post@c1.service.d/h.conf ]&&[ ! -e $t/s/agi-boxwake@c1.service.d/h.conf ]&&[ -f $t/s/agi-post@p1.service.d/h.conf ]'
 # THE HOLD: an empty and an absent posts.md after a good projection
 pj $S $T/full $t/e bx;nw=$(ls $t/e/multi-user.target.wants|wc -l);nu=$(grep -c . $t/e/agi-users.conf);for v in empty absent;do pj $S $T/$v $t/e bx;eval r_$v=$rc;done
 ok "$L-hold-empty-posts-md-fails-and-removes-nothing" '[ $r_empty != 0 ]&&[ -f $t/e/agi-post@c1.service.d/h.conf ]&&[ $(ls $t/e/multi-user.target.wants|wc -l) = $nw ]&&[ $(grep -c . $t/e/agi-users.conf) = $nu ]&&[ -f $t/e/agi-post@g1.service.d/h.conf ]&&[ -f $t/e/agi-boxwake@c1.service.d/h.conf ]'
 ok "$L-hold-absent-posts-md-fails-and-removes-nothing" '[ $r_absent != 0 ]&&[ $(ls $t/e/multi-user.target.wants|wc -l) = $nw ]&&[ $(grep -c . $t/e/agi-users.conf) = $nu ]&&[ -f $t/e/agi-post@c1.service.d/h.conf ]&&[ -f $t/e/agi-post@g1.service.d/h.conf ]'
 # SCOPE: a box named by rows of which none is v4 (core-town's shape): rc 0; its stale drop-in goes, nothing else
 pj $S $T/c1 $t/c ct;pj $S $T/c2 $t/c ct;rC=$rc
 ok "$L-scope-box-with-no-v4-row-exits-0-and-cleans-its-own" '[ $rC = 0 ]&&[ ! -e $t/c/agi-post@t1.service.d/h.conf ]'
 pj $S $T/c2 $t/c0 ct
 ok "$L-scope-fresh-box-with-no-v4-row-exits-0" '[ $rc = 0 ]'
 # DOUBT: a broken row line BEFORE a good row; AGI_BOX unset / empty / misspelled; the box whose last row moved away
 pj $S $T/full $t/d bx;pj $S $T/broken $t/d bx;rD=$rc
 ok "$L-doubt-broken-row-fails-and-removes-nothing" '[ $rD != 0 ]&&[ -f $t/d/agi-post@c1.service.d/h.conf ]&&[ -f $t/d/agi-post@g1.service.d/h.conf ]&&[ -f $t/d/agi-post@p1.service.d/h.conf ]'
 pj $S $T/mangled $t/m bx;pj $S $T/full $t/m bx;pj $S $T/mangled $t/m bx;rM=$rc
 ok "$L-doubt-mangled-row-prefix-fails-and-removes-nothing" '[ $rM != 0 ]&&[ -f $t/m/agi-post@c1.service.d/h.conf ]'
 for v in UNSET "" bxx;do pj $S $T/full $t/u bx;pj $S $T/full2 $t/u "$v";eval "ru_${v:-empty}=$rc";done
 ok "$L-doubt-box-unset-fails-and-removes-nothing" '[ $ru_UNSET != 0 ]&&[ -f $t/u/agi-post@c1.service.d/h.conf ]&&[ -f $t/u/agi-post@g1.service.d/h.conf ]'
 ok "$L-doubt-box-empty-or-misspelled-fails-and-removes-nothing" '[ $ru_empty != 0 ]&&[ $ru_bxx != 0 ]&&[ -f $t/u/agi-post@c1.service.d/h.conf ]'
 pj $S $T/full $t/l bx;pj $S $T/moved $t/l bx;rL=$rc
 ok "$L-doubt-box-whose-last-row-moved-away-fails-and-keeps-its-drop-in" '[ $rL != 0 ]&&[ -f $t/l/agi-post@c1.service.d/h.conf ]'
 for v in tab noindent;do pj $S $T/lastok $t/z$v bx;pj $S $T/last$v $t/z$v bx;eval rz_$v=$rc;done
 ok "$L-doubt-last-row-with-a-tab-fails-and-removes-nothing" '[ $rz_tab != 0 ]&&[ -f $t/ztab/agi-post@p1.service.d/h.conf ]&&[ -f $t/ztab/agi-boxwake@p1.service.d/h.conf ]&&[ -f $t/ztab/agi-post@g2.service.d/h.conf ]'
 ok "$L-doubt-last-row-with-no-indent-fails-and-removes-nothing" '[ $rz_noindent != 0 ]&&[ -f $t/znoindent/agi-post@g2.service.d/h.conf ]&&[ -f $t/znoindent/agi-boxwake@g2.service.d/h.conf ]'
 # aio's rows: the template-wide dir survives; an extra file beside a stale h.conf survives and its dir stays
 pj $S $T/s1 $t/x bx;mkdir -p $t/x/agi-post@.service.d;echo T>$t/x/agi-post@.service.d/h.conf;echo keep>$t/x/agi-post@c1.service.d/50-host.conf;pj $S $T/s2 $t/x bx
 ok "$L-template-wide-dir-survives-a-projection" '[ -f $t/x/agi-post@.service.d/h.conf ]'
 ok "$L-extra-file-beside-a-stale-h-conf-survives" '[ ! -e $t/x/agi-post@c1.service.d/h.conf ]&&[ -f $t/x/agi-post@c1.service.d/50-host.conf ]&&[ ! -e $t/x/agi-boxwake@c1.service.d ]';}
FULL|repo full
FULL|sed 's/"name":"c1","role":"parent","tier":3,"box":"bx","engine":{"v":4,"harness":"claude-code"/"name":"c1","role":"parent","tier":3,"box":"bx","engine":{"v":4,"harness":"foo"/'|repo s2
FULL|repo s1;cp -r $T/full $T/full2
hdr|{ cat;printf -- 'end: 1\n---\n';}|repo empty
{ :; }|{ mkdir -p $T/absent;$G init -q $T/absent;mkdir -p $T/absent/$GD;cp $T/cur/engine*.md $T/absent/$GD/;$G -C $T/absent add -A;$G -C $T/absent -c user.name=x -c user.email=x@x commit -qm f; }
{ hdr;row c1 claude-code bx;echo '  - {"name":"zz","box":"bx", broken';row p1 pi bx m2;row g1 grok-bot bx grok-4.7;printf -- 'end: 1\n---\n'; }|repo broken
{ hdr;row c1 claude-code bx|sed 's/^  - {/  -{/';row p1 pi bx m2;row g1 grok-bot bx grok-4.7;printf -- 'end: 1\n---\n'; }|repo mangled
{ hdr;row c1 claude-code ox;row o1 claude-code ox;row l1 claude-code local-town;printf -- 'end: 1\n---\n'; }|repo moved
{ hdr;row c1 claude-code bx;row p1 pi bx m2;row g1 grok-bot bx grok-4.7;row g2 grok-bot bx;printf 'end: 1\n---\n'; }|repo lastok
{ hdr;row c1 claude-code bx;row p1 pi bx m2;row g1 grok-bot bx grok-4.7;row g2 grok-bot bx|sed 's/^  - {/\t- {/';printf -- 'end: 1\n---\n'; }|repo lasttab
{ hdr;row c1 claude-code bx;row p1 pi bx m2;row g1 grok-bot bx grok-4.7;row g2 grok-bot bx|sed 's/^  - {/- {/';printf -- 'end: 1\n---\n'; }|repo lastnoindent
{ hdr;row t1 claude-code ct;printf -- 'end: 1\n---\n'; }|repo c1
{ hdr;printf '  - {"name":"t1","role":"parent","tier":3,"box":"ct"}\n';printf -- 'end: 1\n---\n'; }|repo c2
# full2 (the misspell / unset / empty box rows reuse FULL: the section sees only AGI_BOX differ)
ok "extract-the-repos-hold-the-rows" '[ $(grep -c "^  - {" $T/full/$GD/posts.md) = 8 ]&&[ ! -e $T/absent/$GD/posts.md ]'
echo "== the section under test"
rows $T/sec cur
echo "== mutants (each must read RED on the row it names)"
mut(){ # mut NAME ROW SEDEXPR : the mutant of the section; its row must FAIL, and the file must differ
 sed "$3" $T/sec>$T/sec.$1;if cmp -s $T/sec $T/sec.$1;then echo "FAIL mutant-$1-changes-nothing";f=$((f+1));return;fi
 out=$(rows $T/sec.$1 m_$1 2>&1|grep "^FAIL m_$1-$2");if [ -n "$out" ];then echo "ok mutant-$1 reads RED on $2";else echo "FAIL mutant-$1 did not read red on $2";f=$((f+1));fi;}
mut else-claude unknown-harness-makes-no-unit 's/elif \$h=="grok-bot" then "grok-bot --model \\(.model)" else/else/;s/select((\$h|test("^(pi|claude)")) or \$h=="grok-bot" or (/select(true or (/'
mut silent-skip each-skip-is-one-named-line 's/(debug(@text "agi-project: skipped post \\(.name): harness \\(\$h) has no unit arm")|false)/false/'
mut perm-mode grok-no-approval-flag 's/grok-bot --model \\(.model)"/grok-bot --model \\(.model) --permission-mode bypassPermissions"/'
mut no-stale-removal stale-claude-h-conf-is-removed-when-the-row-turns-foo 's/^\[ -s \$o\/\.s \]&&while/[ -s $o\/.none ]\&\&while/'
mut no-hold-guard hold-empty-posts-md-fails-and-removes-nothing 's/^ok||{ ls/true||{ ls/'
mut box-fallback doubt-box-unset-fails-and-removes-nothing 's/ok(){ \[ "\$AGI_BOX" \]&&k=/ok(){ AGI_BOX=${AGI_BOX:-local-town};k=/'
mut sed-lines-only doubt-mangled-row-prefix-fails-and-removes-nothing 's/\&\&\[ \$(printf .%s\\n. "\$n"|grep -c \.) = \$(g posts.md|sed -n .*|grep -c \.) \]\&\&printf/\&\&printf/'
mut rm-rf-the-dir extra-file-beside-a-stale-h-conf-survives 's/rm -f \$d\/h.conf;rmdir \$d 2>\/dev\/null/rm -rf $d/'
mut guard-on-writes scope-box-with-no-v4-row-exits-0-and-cleans-its-own 's/ok(){ \[ "\$AGI_BOX" \]&&k=/ok(){ [ -s $o\/.w ]\&\&k=/'
mut broken-row-unchecked doubt-broken-row-fails-and-removes-nothing 's/k=\$(printf .%s\\n. "\$n"|jq -r \.box)/k=$(printf "%s\\n" "$n"|jq -r .box 2>\/dev\/null||:)/;s/\&\&\[ \$(printf .%s\\n. "\$n"|grep -c \.) = \$(printf .%s\\n. "\$k"|grep -c \.) \]//'
mut block-ends-at-any-unindented doubt-last-row-with-a-tab-fails-and-removes-nothing 's|sed -n ./^posts:/,/^\[A-Za-z_\]\[A-Za-z0-9_\]\*:/{[^}]*}.|sed -n "/^posts:/,/^[^ ]/{/^  /p}"|'
echo "agi-project-harness: $f FAIL";[ $f = 0 ]
