#!/bin/sh
# settings-tui.t.sh: goal:g7.16.1.11.36 (reopened, SM 10:1xZ) -- the post's settings.json pins the CLASSIC renderer with "tui":"default", which makes Claude Code 2.1.295 decide the "Try the new fullscreen renderer?" dialog is not shown
# (DG1's bytes: the gate returns false when `ft().tui !== void 0` BEFORE the fullscreenUpsellSeenCount test; harness proof on a scratch HOME: {"tui":"default"} -> alternate_on 0, the classic renderer posts run today).
# sh + jq, no claude, no network. The piece is the ### settings.json fence of the .geometry engine*.md of ROOT (SETTINGS=<file> tests another text). One ok/FAIL line per case; exit = FAIL count.
# Cases: a the piece parses as JSON · b .tui is EXACTLY the string "default" (not "Default", not "bogus", not absent: an invalid value makes Claude Code skip the WHOLE file, hooks included) · c the 4 live hooks are still there (agi-captive agi-brief agi-meter agi-turn) ·
#   d the piece names no other renderer / dialog key.
T=$(mktemp -d);trap 'rm -rf $T' 0;f=0;R0=${ROOT:-$(cd "$(dirname "$0")/../../.." && pwd)}
sect(){ cat $R0/.agi/nodes/.geometry/engine*.md|sed -n "/^###* $1 /,/^###* /{/^~~~/,/^~~~/{//!p}}";}
ok(){ if eval "$2";then echo "ok $1";else echo "FAIL $1";f=$((f+1));fi;}
[ -n "$SETTINGS" ]||{ sect settings.json>$T/s.json;SETTINGS=$T/s.json;}
[ -s $SETTINGS ]||{ echo "FAIL extract: settings.json piece $(wc -c<$SETTINGS) B";exit 99;}
ok "a-the-piece-parses the settings.json piece is valid JSON ($(wc -c<$SETTINGS|tr -d ' ') B)" 'jq -e . $SETTINGS>/dev/null 2>&1'
tui=$(jq -r '.tui // "<absent>"' $SETTINGS 2>/dev/null)
ok "b-tui-is-exactly-default .tui = [$tui] (want exactly: default)" '[ "$tui" = default ]&&jq -e ".tui == \"default\"" $SETTINGS>/dev/null 2>&1'
hk=$(jq -r '[.hooks[][].hooks[].command]|sort|join(" ")' $SETTINGS 2>/dev/null)
ok "c-the-live-hooks-survive the hook commands are [$hk] (want: agi-brief agi-captive agi-mem tap agi-meter agi-turn; agi-mem tap is the M6 Stop hook, goal:g7.16.1.11.46.13)" '[ "$hk" = "agi-brief agi-captive agi-mem tap agi-meter agi-turn" ]'
ok "d-no-other-renderer-key the piece names no fullscreen / altScreen / renderer key besides tui" '! jq -r "keys[]" $SETTINGS 2>/dev/null|grep -i -E "fullscreen|altscreen|renderer"'
echo "settings-tui: $f FAIL";exit $f
