#!/bin/sh
# w-move.t.sh: goal:g7.16.1.11.15.1 Falsifier 1 (SM 22:08Z: live workflow.py gone, 16 json remain).
# One ok/FAIL line per case; exit = FAIL count. sh + git; no python.
R0=${ROOT:-$(cd "$(dirname "$0")/../../.." && pwd)}
f=0
ok(){ if eval "$2";then echo "ok $1";else echo "FAIL $1";f=$((f+1));fi;}
cd "$R0" || exit 99
live=$(git ls-files -- extensions/agi/bin/workflow.py extensions/agi/hooks/workflow_note.py)
ok "live_workflow_py_gone" '[ -z "$live" ]'
ok "deprecated_workflow_py_present" 'git ls-files -- extensions/agi/deprecated/bin/workflow.py | grep -q .'
ok "deprecated_workflow_note_present" 'git ls-files -- extensions/agi/deprecated/hooks/workflow_note.py | grep -q .'
nj=$(git ls-files -- 'extensions/agi/workflows/*.json' | wc -l)
ok "json_live_16 (got $nj)" '[ "$nj" -eq 16 ]'
js=$(git ls-files -- 'extensions/agi/workflows/*.js' | wc -l)
ok "js_live_0 (got $js)" '[ "$js" -eq 0 ]'
jsd=$(git ls-files -- 'extensions/agi/deprecated/workflows/*.js' | wc -l)
ok "js_deprecated_14 (got $jsd)" '[ "$jsd" -eq 14 ]'
ok "spawn_chain_dir" '[ -d skills/agi-spawn-chain ]'
hits=$(git grep -l workflow.py -- skills/agi/SKILL.md skills/agi-corrective skills/agi-master-gate skills/agi-merge-pass skills/agi-dispatch 2>/dev/null)
ok "named_skills_no_workflow_py" '[ -z "$hits" ]'
exit $f
