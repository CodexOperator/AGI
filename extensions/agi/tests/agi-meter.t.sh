#!/bin/sh
# agi-meter.t.sh: T1 of goal:g7.16.1.11.16 — shell twin of test_agi_meter.py
# (agi-meter reads newest transcript line WITH .message.usage, not the last line).
# One ok/FAIL line per named case; exit = FAIL count. sh + jq; no python.
R0=${ROOT:-$(cd "$(dirname "$0")/../../.." && pwd)}
f=0
ok(){ if eval "$2";then echo "ok $1";else echo "FAIL $1";f=$((f+1));fi;}
command -v jq >/dev/null || { echo "FAIL jq-absent"; exit 99; }
D=$(mktemp -d)
trap 'rm -rf "$D"' 0
sect(){ cat $R0/.agi/nodes/.geometry/engine*.md|sed -n "/^###* $1 /,/^###* /{/^~~~/,/^~~~/{//!p}}";}
sect agi-meter >"$D/m.sh"
[ -s "$D/m.sh" ] || { echo "FAIL extract agi-meter"; exit 99; }
U(){ printf '{"type":"assistant","message":{"usage":{"input_tokens":%s,"cache_read_input_tokens":0,"cache_creation_input_tokens":0}}}\n' "$1"; }
SYS='{"type":"system","subtype":"bridge"}'
# run WINDOW [HOOK_JSON]: reads transcript from $D/t.jsonl, prints meter stdout
run(){
  w=${1:-1000}; hook=${2:-{}}
  j=$(printf '%s\n' "$hook" | jq -c --arg p "$D/t.jsonl" '. + {transcript_path:$p}')
  printf '%s\n' "$j" | env AGI_WINDOW=$w AGI_ROTATE_PCT=50 sh "$D/m.sh"
}
tr(){ cat >"$D/t.jsonl"; }

tr <<EOF
$(U 900)
$SYS
EOF
out=$(run 1000)
ok "a_last_line_no_usage_earlier_over_the_line" 'printf %s "$out" | grep -q "At the line (900/1000)"'

tr <<EOF
$(U 100)
$SYS
EOF
out=$(run 1000)
ok "b_under_the_line_is_silent" '[ -z "$out" ]'

tr <<EOF
$(U 100)
$SYS
EOF
out=$(run 1000 '{"tokens":900}')
ok "c_tokens_in_hook_wins_over" 'printf %s "$out" | grep -q "(900/1000)"'

tr <<EOF
$(U 900)
$SYS
EOF
out=$(run 1000 '{"tokens":100}')
ok "c_tokens_in_hook_wins_under" '[ -z "$out" ]'

tr <<EOF
$SYS
{"type":"user"}
not json
EOF
out=$(run 1000)
ok "d_no_usage_line_is_silent_exit_0" '[ -z "$out" ]'

tr <<EOF
$(U 900)
{"type":"assistant","message":{"content":[{"type":"text","text":"the usage word"}]}}
$SYS
EOF
out=$(run 1000)
ok "e_text_mentioning_usage_is_skipped" 'printf %s "$out" | grep -q "(900/1000)"'

tr <<EOF
{"message":{"usage":{"input_tokens":900,"cache_read_input_tokens":null}}}
EOF
out=$(run 1000)
ok "null_field_counts_as_zero" 'printf %s "$out" | grep -q "(900/1000)"'

tr <<EOF
$(U 900)
{"message":{"usage":"x"}}
{"message":{"usage":[1]}}
{"message":{"usage":7}}
{"message":"s"}
5
$SYS
EOF
out=$(run 1000)
ok "non_object_usage_is_skipped" 'printf %s "$out" | grep -q "(900/1000)"'

poison='{"message":{"usage":{"input_tokens":"a","cache_read_input_tokens":"b"}}}'
tr <<EOF
$poison
$poison
$poison
$SYS
$(U 900)
EOF
out=$(run 1000)
ok "scan_stops_at_first_valid_usage_line" 'printf %s "$out" | grep -q "(900/1000)"'

tr <<EOF
$(U 900)
$poison
$SYS
EOF
out=$(run 1000 2>"$D/err")
ok "poison_reached_first_is_skipped_not_fatal" 'printf %s "$out" | grep -q "(900/1000)" && [ ! -s "$D/err" ]'

tr <<EOF
$(U 100)
{"message":{"usage":{"input_tokens":900,"cache_read_input_tokens":"b","cache_creation_input_tokens":5}}}
EOF
: >"$D/err"
out=$(run 1800 2>"$D/err")
ok "string_cache_field_counts_zero" 'printf %s "$out" | grep -q "(905/1800)" && [ ! -s "$D/err" ]'
exit $f
