#!/bin/sh
# mail-alert-retired.t.sh [ROOT]: goal:g7.16.1.11.20 cut C (SM; DG4's order, DG2's lane FIRST): mail_alert.py, hooks/mail-alert.sh and test_mail_alert.py are RETIRED -- the three files are gone, no LIVE path names them, the v5 settings piece registers no mail-alert hook, and the commands manifest has no row for it while every path it still lists resolves. sh + grep + sed on a TREE (ROOT=<tree> or $1, default the working tree); no git, no network, no root, 0 USD. One ok/FAIL line per case; exit = FAIL count.
# Rows: r1 the three files are ABSENT (one row per file) · r2 NO LIVE NAME: grep -rlE 'mail_alert|mail-alert' over the LIVE paths only (extensions skills src .claude CLAUDE.md AGENTS.md .agi/nodes/.geometry), minus THIS lane file, is EMPTY · r3 NO REGISTRATION: the `### settings.json` fence of .agi/nodes/.geometry/engine-wrap.md and every .claude/settings*.json name no mail-alert (non-vacuous: the same extraction finds the 4 live hooks agi-captive agi-brief agi-meter agi-turn) · r4 commands.md has no `mail_alert.py::` registry key AND every `<engine>/...` path the manifest lists exists in ROOT (non-vacuous: >= 20 paths found).
# SCOPE of r2, stated: "outside datasets/ = only the retirement's THOUGHT" cannot hold -- the name is in ~73 files and 60+ are historical experiment / hypothesis / build / comms / dm nodes (retire, never delete: they are the record). So r2 reads the LIVE paths listed above; a node under .agi/nodes outside .geometry is history, not a caller.
R0=${ROOT:-${1:-$(cd "$(dirname "$0")/../../.." && pwd)}};f=0;ME=mail-alert-retired.t.sh
ok(){ if eval "$2";then echo "ok $1";else echo "FAIL $1";f=$((f+1));fi;}
[ -f $R0/.agi/nodes/.geometry/engine-wrap.md ]&&[ -f $R0/.agi/nodes/.geometry/commands.md ]&&[ -d $R0/extensions/agi/bin ]||{ echo "FAIL inputs: not an agi tree: $R0";exit 99;}
for p in extensions/agi/bin/mail_alert.py extensions/agi/hooks/mail-alert.sh extensions/agi/tests/test_mail_alert.py;do
 ok "r1-absent-$(basename $p) $p: $([ -e $R0/$p ]&&echo PRESENT||echo absent) (want absent)" '[ ! -e $R0/$p ]';done
L=$(cd $R0&&for p in extensions skills src .claude CLAUDE.md AGENTS.md .agi/nodes/.geometry;do [ -e $p ]&&echo $p;done)
npath=$(echo "$L"|wc -l|tr -d ' ')
live=$(cd $R0&&grep -rlE 'mail_alert|mail-alert' --exclude=$ME $L 2>/dev/null|sort|tr '\n' ' ')
ok "r2-no-live-name $npath live path(s) searched (want >= 4); files naming mail_alert / mail-alert: [${live% }] (want none)" '[ "$npath" -ge 4 ]&&[ -z "$live" ]'
S=$(sed -n '/^### settings.json /,/^### /{/^~~~json/,/^~~~$/{//!p}}' $R0/.agi/nodes/.geometry/engine-wrap.md)
cmds=$(echo "$S"|grep -o '"command":"[^"]*"'|sed 's/"command":"//;s/"$//'|sort|tr '\n' ' ')
nl=0;for h in agi-captive agi-brief agi-meter agi-turn;do case " $cmds" in *" $h "*)nl=$((nl+1));;esac;done
nm=$(echo "$S"|grep -ciE 'mail_alert|mail-alert')
ok "r3-settings-piece-registers-no-mail-alert the settings piece's hook commands [${cmds% }] (want the 4 live hooks: found $nl of 4), lines naming mail-alert: $nm (want 0)" '[ "$nl" = 4 ]&&[ "$nm" = 0 ]'
sj=$(cd $R0&&ls .claude/settings*.json 2>/dev/null|tr '\n' ' ');sn=0;for j in $sj;do sn=$((sn+$(grep -ciE 'mail_alert|mail-alert' $R0/$j)));done
ok "r3b-claude-settings-files-register-no-mail-alert .claude/settings*.json found [${sj% }] (want >= 1), lines naming mail-alert: $sn (want 0)" '[ -n "$sj" ]&&[ "$sn" = 0 ]'
C=$R0/.agi/nodes/.geometry/commands.md
rk=$(grep -c '^  mail_alert\.py::' $C);np=$(grep -o '<engine>/[^ ]*' $C|sort -u|wc -l|tr -d ' ');miss=$(grep -o '<engine>/[^ ]*' $C|sort -u|sed 's|<engine>/||'|while read p;do [ -e "$R0/$p" ]||echo $p;done|tr '\n' ' ')
ok "r4-manifest-has-no-mail-alert-row-and-still-resolves 'mail_alert.py::' keys: $rk (want 0); $np manifest path(s) (want >= 20), missing from the tree: [${miss% }] (want none)" '[ "$rk" = 0 ]&&[ "$np" -ge 20 ]&&[ -z "$miss" ]'
echo "mail-alert-retired: $f FAIL"
exit $f
