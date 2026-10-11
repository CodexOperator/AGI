#!/bin/sh
# trunk-arg-lanes.t.sh [TESTS_DIR]: a lane that extracts the piece under test from a TRUNK ref owns "what is under test" -- never the runner (SM gen 36 / council 3/3 08:22Z, AA1.V: a runner that passed no arg read the PRE-.37 trunk = a vacuous green). So a TRUNK-arg lane REFUSES a bare run. Rows: t1 no *.t.sh holds a trunk DEFAULT (${1:-...season2/main}); t2 each of the 17 named TRUNK-arg lanes exits 2 with '[no-candidate]' when run with no arg; t3 every file that holds '[no-candidate]' is one of the 17 (a new guarded lane is named here too). MUTANTS (scratch copies): m1 a default put back in agi-out-stale = t1 RED; m2 the same copy run bare = no refusal = t2 RED. Sh (dash), bare env -i, git-free, nothing is written outside a mktemp dir.
D=$(mktemp -d);trap 'rm -rf $D' EXIT;f=0;TD=${1:-$(cd "$(dirname "$0")" && pwd)}
ok(){ if eval "$2";then echo "ok $1";else echo "FAIL $1";f=$((f+1));fi;}
L="aa3-lanes agi-land-bounds agi-out-stale agi-out-states ckpt grow-gate-ab grow-gate-bootstrap grow-gate-keys grow-gate-ring grow-gate-ring3 grow-gate-ring4 grow-gate-ring4b grow-gate-ring5c grow-gate-ring5d grow-gate-ring5e-dg3 grow-gate-ring5e grow-gate-ring5f"
P1='[$]{1:-[^}]*season2/main';NC='[[]no-candidate[]]'   # the patterns are built so this file never matches itself
dflt(){ grep -lE "$P1" "$1"/*.t.sh 2>/dev/null|xargs -n1 basename 2>/dev/null|grep -v '^trunk-arg-lanes.t.sh$'|tr '\n' ' ';}   # this file names the default in its own text and mutants: it is the scanner, not scanned
bare(){ (cd $D&&env -i PATH=/usr/bin:/bin HOME=$D timeout 20 sh "$1" >$D/so 2>$D/se</dev/null);echo $?;}
d=$(dflt $TD)
ok "t1-no-lane-holds-a-trunk-default every tests/*.t.sh: the files holding a \${1:-...season2/main} default: [$d] (want none)" '[ -z "$d" ]'
miss=;bad=;for l in $L;do [ -f $TD/$l.t.sh ]||{ miss="$miss $l";continue;};r=$(bare $TD/$l.t.sh);{ [ "$r" = 2 ]&&grep -qE "$NC" $D/se;}||bad="$bad $l:$r";done
ok "t2-each-named-lane-refuses-a-bare-run the 17 TRUNK-arg lanes with no arg: exit 2 and '[no-candidate]' on stderr; missing [$miss] (want none), not refusing [$bad] (want none)" '[ -z "$miss" ]&&[ -z "$bad" ]'
g=$(grep -lE "$NC" $TD/*.t.sh|xargs -n1 basename|sed 's/\.t\.sh$//'|grep -v '^trunk-arg-lanes$');x=;for n in $g;do case " $L " in *" $n "*);;*)x="$x $n";;esac;done
ok "t3-a-guarded-lane-is-named-here every file holding '[no-candidate]' is in this lane's list of 17; unnamed [$x] (want none)" '[ -z "$x" ]'
# m1 / m2: a scratch tests dir with ONE lane whose default is put back
mkdir $D/m;cp $TD/agi-out-stale.t.sh $D/m/;sed -i 's#^T=[$]1;.*exit 2;}#T=${1:-local-maxxing/season2/main}#' $D/m/agi-out-stale.t.sh
cmp -s $TD/agi-out-stale.t.sh $D/m/agi-out-stale.t.sh&&{ echo "FAIL mutant-did-not-change-the-text";f=$((f+1)); }
md=$(dflt $D/m);mr=$(bare $D/m/agi-out-stale.t.sh)
ok "mutant-m1-a-default-put-back-is-RED the scratch agi-out-stale with \${1:-local-maxxing/season2/main}: t1's scan finds [$md] (want agi-out-stale.t.sh)" '[ "$md" = "agi-out-stale.t.sh " ]'
ok "mutant-m2-a-lane-that-no-longer-refuses-is-RED the same scratch lane run bare: exit $mr (want NOT 2: it ran against the default trunk, which t2 forbids)" '[ "$mr" != 2 ]'
echo "trunk-arg-lanes: $f FAIL";exit $f
