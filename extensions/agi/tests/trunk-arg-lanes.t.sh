#!/bin/sh
# trunk-arg-lanes.t.sh [TESTS_DIR]: a lane that extracts the piece under test from a TRUNK ref owns "what is under test" -- never the runner (SM gen 36 / council 3/3 08:22Z, AA1.V: a runner that passed no arg read the PRE-.37 trunk = a vacuous green). So a TRUNK-arg lane REFUSES a bare run, and a lane that builds a scratch repo owns its git env (council 10:10Z: an inherited GIT_DIR made aa3-lanes / agi-out-states write MAIN under aio's harness, 09:56Z). Rows: t1 no *.t.sh gives its arg 1 a REF default -- ANY ${1:-word} whose default is a plain word (a branch name, HEAD, a sha), not a path computed by $( ) -- outside a helper function's own line; t2 each of the 17 named TRUNK-arg lanes exits 2 with '[no-candidate]' when run with no arg; t3 every file that holds '[no-candidate]' is one of the 17; t4 each of them that runs git init / update-ref unsets GIT_DIR GIT_WORK_TREE GIT_INDEX_FILE on a line BEFORE the first one. MUTANTS (scratch copies of agi-out-stale): m1 a trunk default put back = t1 RED; m2 the same copy run bare = no refusal = t2 RED; m3 a ${1:-HEAD} default = t1 RED; m4 the unset line removed = t4 RED. Sh (dash), bare env -i, git-free, nothing is written outside a mktemp dir.
D=$(mktemp -d);trap 'rm -rf $D' EXIT;f=0;TD=${1:-$(cd "$(dirname "$0")" && pwd)}
ok(){ if eval "$2";then echo "ok $1";else echo "FAIL $1";f=$((f+1));fi;}
L="aa3-lanes agi-land-bounds agi-out-stale agi-out-states ckpt grow-gate-ab grow-gate-bootstrap grow-gate-keys grow-gate-ring grow-gate-ring3 grow-gate-ring4 grow-gate-ring4b grow-gate-ring5c grow-gate-ring5d grow-gate-ring5e-dg3 grow-gate-ring5e grow-gate-ring5f"
P1='[$]{1:-[^$(}]+}';NC='[[]no-candidate[]]'   # the patterns are built so this file never matches itself
# dflt DIR: the lanes whose line N (not a `name(){` helper definition) holds ${1:-<plain word>}; the scanner itself names the shape in its text and mutants, so it is not scanned
dflt(){ for x in "$1"/*.t.sh;do [ "${x##*/}" = trunk-arg-lanes.t.sh ]&&continue;grep -vE '^[A-Za-z0-9_]+\(\)[{]' "$x"|grep -qE "$P1"&&echo "${x##*/}";done|tr '\n' ' ';}
bare(){ (cd $D&&env -i PATH=/usr/bin:/bin HOME=$D timeout 20 sh "$1" >$D/so 2>$D/se</dev/null);echo $?;}
# envfix FILE: empty when FILE has no git init / update-ref, or an unset of the three vars on an EARLIER line; else the offending line numbers
envfix(){ awk 'BEGIN{u=0;i=0} /^unset .*GIT_DIR/&&/GIT_WORK_TREE/&&/GIT_INDEX_FILE/&&!u{u=NR} /git init|[$]GIT init|update-ref/&&!i{i=NR} END{if(i&&(!u||u>i))print "init@" i " unset@" u+0}' "$1";}
d=$(dflt $TD)
ok "t1-no-lane-gives-arg-1-a-ref-default every tests/*.t.sh: the files holding a \${1:-<plain word>} default (a trunk, HEAD, a sha): [$d] (want none)" '[ -z "$d" ]'
miss=;bad=;for l in $L;do [ -f $TD/$l.t.sh ]||{ miss="$miss $l";continue;};r=$(bare $TD/$l.t.sh);{ [ "$r" = 2 ]&&grep -qE "$NC" $D/se;}||bad="$bad $l:$r";done
ok "t2-each-named-lane-refuses-a-bare-run the 17 TRUNK-arg lanes with no arg: exit 2 and '[no-candidate]' on stderr; missing [$miss] (want none), not refusing [$bad] (want none)" '[ -z "$miss" ]&&[ -z "$bad" ]'
g=$(grep -lE "$NC" $TD/*.t.sh|xargs -n1 basename|sed 's/\.t\.sh$//'|grep -v '^trunk-arg-lanes$');x=;for n in $g;do case " $L " in *" $n "*);;*)x="$x $n";;esac;done
ok "t3-a-guarded-lane-is-named-here every file holding '[no-candidate]' is in this lane's list of 17; unnamed [$x] (want none)" '[ -z "$x" ]'
e=;for l in $L;do [ -f $TD/$l.t.sh ]&&{ r=$(envfix $TD/$l.t.sh);[ -z "$r" ]||e="$e $l($r)";};done
ok "t4-a-lane-that-builds-a-repo-unsets-the-git-env each of the 17 that runs git init / update-ref has an 'unset GIT_DIR GIT_WORK_TREE GIT_INDEX_FILE' line before the first: offenders [$e] (want none)" '[ -z "$e" ]'
# m1 / m2 / m3 / m4: scratch copies of ONE lane
mkdir $D/m $D/m3 $D/m4;cp $TD/agi-out-stale.t.sh $D/m/;cp $TD/agi-out-stale.t.sh $D/m3/;cp $TD/agi-out-stale.t.sh $D/m4/
sed -i 's#^T=[$]1;.*exit 2;}#T=${1:-some/trunk}#' $D/m/agi-out-stale.t.sh
sed -i 's#^T=[$]1;.*exit 2;}#T=${1:-HEAD}#' $D/m3/agi-out-stale.t.sh
sed -i '/^unset GIT_DIR GIT_WORK_TREE GIT_INDEX_FILE/d' $D/m4/agi-out-stale.t.sh
for c in m m3 m4;do cmp -s $TD/agi-out-stale.t.sh $D/$c/agi-out-stale.t.sh&&{ echo "FAIL mutant-$c-did-not-change-the-text";f=$((f+1)); };done
md=$(dflt $D/m);mr=$(bare $D/m/agi-out-stale.t.sh);m3d=$(dflt $D/m3);m4e=$(envfix $D/m4/agi-out-stale.t.sh)
ok "mutant-m1-a-trunk-default-put-back-is-RED the scratch agi-out-stale with a branch-name default: t1's scan finds [$md] (want agi-out-stale.t.sh)" '[ "$md" = "agi-out-stale.t.sh " ]'
ok "mutant-m2-a-lane-that-no-longer-refuses-is-RED the same scratch lane run bare: exit $mr (want NOT 2: it ran against the default trunk, which t2 forbids)" '[ "$mr" != 2 ]'
ok "mutant-m3-a-HEAD-default-is-RED the scratch agi-out-stale with a \${1:-HEAD} default: t1's scan finds [$m3d] (want agi-out-stale.t.sh)" '[ "$m3d" = "agi-out-stale.t.sh " ]'
ok "mutant-m4-a-lane-without-the-unset-is-RED the scratch agi-out-stale with the unset line removed: t4's check says [$m4e] (want it to name the git init line)" '[ -n "$m4e" ]'
echo "trunk-arg-lanes: $f FAIL";exit $f
