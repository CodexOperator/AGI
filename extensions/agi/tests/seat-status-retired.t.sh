#!/bin/sh
# seat-status-retired.t.sh [ROOT]: goal:g7.16.1.11.46.16, owner atom 8.1 ("retire", belam's relay 05:1xZ 10-26): seat_status.py and test_seat_status.py are RETIRED -- the files are gone, no LIVE path imports or runs the module, the commands manifest has no row for it while every path it still lists resolves, and the seat view [R registry rows + M meter fraction] lives in hierarchy.py with the dropped answers [L ephemeral lease line, C cost roll-up line] in neither viewport head. sh + grep + sed on a TREE (ROOT=<tree> or $1, default the working tree); no git, no network, no root, 0 USD. One ok/FAIL line per case; exit = FAIL count.
# SCOPE of r2, stated: a node under .agi/nodes outside .geometry that names seat_status is history (retire, never delete), so r2 reads the LIVE paths only; it excludes THIS lane and test_hierarchy_seats.py, whose retirement test spells the module name inside its assertion.
R0=${ROOT:-${1:-$(cd "$(dirname "$0")/../../.." && pwd)}};f=0
ok(){ if eval "$2";then echo "ok $1";else echo "FAIL $1";f=$((f+1));fi;}
[ -f $R0/.agi/nodes/.geometry/commands.md ]&&[ -d $R0/extensions/agi/bin ]||{ echo "FAIL inputs: not an agi tree: $R0";exit 99;}
for p in extensions/agi/bin/seat_status.py extensions/agi/tests/test_seat_status.py;do
 ok "r1-absent-$(basename $p) $p: $([ -e $R0/$p ]&&echo PRESENT||echo absent) (want absent)" '[ ! -e $R0/$p ]';done
L=$(cd $R0&&for p in extensions skills src .claude CLAUDE.md AGENTS.md .agi/nodes/.geometry;do [ -e $p ]&&echo $p;done)
npath=$(echo "$L"|wc -l|tr -d ' ')
live=$(cd $R0&&grep -rlE 'import seat_status|from seat_status|seat_status\.(collect|to_compact|to_markdown|main)|bin/seat_status\.py|^  seat_status\.py:' --exclude-dir=__pycache__ --exclude=seat-status-retired.t.sh --exclude=test_hierarchy_seats.py $L 2>/dev/null|sort|tr '\n' ' ')
ok "r2-no-live-import $npath live path(s) searched (want >= 4); files that import or run seat_status: [${live% }] (want none)" '[ "$npath" -ge 4 ]&&[ -z "$live" ]'
C=$R0/.agi/nodes/.geometry/commands.md
rk=$(grep -c '^  seat_status\.py:' $C);np=$(grep -o '<engine>/[^ ]*' $C|sort -u|wc -l|tr -d ' ');miss=$(grep -o '<engine>/[^ ]*' $C|sort -u|sed 's|<engine>/||'|while read p;do [ -e "$R0/$p" ]||echo $p;done|tr '\n' ' ')
ok "r3-manifest-has-no-seat-status-row-and-still-resolves 'seat_status.py:' keys: $rk (want 0); $np manifest path(s) (want >= 20), missing from the tree: [${miss% }] (want none)" '[ "$rk" = 0 ]&&[ "$np" -ge 20 ]&&[ -z "$miss" ]'
H=$R0/extensions/agi/bin/hierarchy.py;V=$R0/extensions/agi/bin/viewport.py
nf=0;for fn in collect_seats seats_to_compact seats_to_markdown seat_fraction;do grep -q "^def $fn(" $H&&nf=$((nf+1));done
ok "r4-the-seat-view-lives-in-hierarchy $nf of 4 functions defined in hierarchy.py (collect_seats seats_to_compact seats_to_markdown seat_fraction); viewport reads hierarchy.collect_seats: $(grep -c 'collect_seats' $V) site(s) (want >= 3)" '[ "$nf" = 4 ]&&[ "$(grep -c collect_seats $V)" -ge 3 ]'
g=$(cat $H $V|grep -cE 'ephemeral live/cap|ephemeral \{|rollup:|rollup \$|cost_usd_total=')
ok "r5-no-ephemeral-or-rollup-line-in-either-head lines in hierarchy.py + viewport.py stating the dropped [L] / [C] answers: $g (want 0)" '[ "$g" = 0 ]'
echo "seat-status-retired: $f FAIL"
exit $f
