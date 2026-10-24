#!/bin/sh
# card-cap.t.sh [ROOT]: goal:g7.16.1.11.46.2 (M1) falsifier 2: rotate.py's card guard counts §0-§6 ONLY (HANDOFF_CARD_LIMIT_LINES = 100) -- 101 lines in §0-§6 is refused, 500 lines in §7 passes; mutant m (a guard that counts the WHOLE card) reads RED on the second lane.
# python3 -I drives the driven-handoff writer (cmd_handoff) on a scratch graph root, no git, no network, 0 USD. ROOT = the tree whose extensions/agi/bin/rotate.py is read; MUT=1 swaps in the whole-card count. exit = the FAIL count.
R0=${ROOT:-${1:-$(cd "$(dirname "$0")/../../.." && pwd)}};D=$(mktemp -d);trap 'rm -rf $D' 0;f=0
ok(){ if eval "$2";then echo "ok $1";else echo "FAIL $1";f=$((f+1));fi;}
[ -f $R0/extensions/agi/bin/rotate.py ]||{ echo "FAIL inputs: no rotate.py under $R0";exit 99;}
cat >$D/drive.py <<'PY'
import sys,os,json,io,importlib
from pathlib import Path
from types import SimpleNamespace
R0,s0,s7,mut=sys.argv[1],int(sys.argv[2]),int(sys.argv[3]),sys.argv[4]=="1"
b=R0+"/extensions/agi/bin";sys.path.insert(0,b);p=b+"/rotate.py";src=open(p).read()
if mut:
    k="line_count = _card_guard_lines(full)";assert k in src;src=src.replace(k,'line_count = full.count("\\n")')
ns={"__file__":p,"__name__":"rot_under_test"};exec(compile(src,p,"exec"),ns)
root=Path(sys.argv[5]);(root/"nodes").mkdir(parents=True);ss=root/"sessions";(ss/"rotations").mkdir(parents=True);(ss/"quorum").mkdir()
(ss/"verify-count.json").write_text(json.dumps({"active":1,"deprecated":0,"total":1,"sha":"a","stamped_at":0.0,"reason":"t"}))
(ss/"rotations"/"adv-alive.20260911T120000Z.json").write_text(json.dumps({"rotation":"rotate-self","seat":"adv-alive","recorded_at":"2026-09-11T12:00:00Z","result":"success","observations":{"b_generation":{"before":4,"after":5}},"handover":{"join":{"found":True,"window_id":"@1","pid":1,"name":"w"},"model_confirm":{"expected":{"model":"x"},"live":{"model":"x"},"verdict":"ok"}}}))
card="# SESSION HANDOFF\n\n## §0 STATE (old)\nold\n\n## §1 CARRIED\n"+"".join("l%d\n"%i for i in range(s0))+"\n## §3 🔴 NEXT COMMAND\nold next\n\n## §6 BANKED\nold banked\n\n## §7 ATOMS\n"+"".join("| a%d | \"s\" | src:doc | target:x | lap1 |\n"%i for i in range(s7))
(ss/"quorum"/"adv-alive.md").write_text(card)
sys.stdin=io.StringIO("bash next\nbanked\n")
rc=ns["cmd_handoff"](SimpleNamespace(driven=True,seat="adv-alive",field=[["s3","-"],["s6","-"]]),root)
print("rc",rc)
PY
run(){ python3 -I $D/drive.py "$R0" $1 $2 $3 $D/r$4 2>$D/e$4|tail -1;}
a=$(run 60 0 0 1);ok "base-small-card-passes a card well under 100 lines is written (got: $a)" '[ "$a" = "rc 0" ]'
b=$(run 120 0 0 2);ok "s0-s6-101-lines-REFUSED more than 100 lines in §0-§6 is refused (got: $b; $(head -c 90 $D/e2))" '[ "$b" = "rc 2" ]'
c=$(run 40 500 0 3);ok "s7-500-lines-passes 500 atom rows in §7 beside a 40-line body: written (got: $c)" '[ "$c" = "rc 0" ]&&[ $(wc -l <$D/r3/sessions/quorum/adv-alive.md) -gt 500 ]'
d=$(run 120 500 0 4);ok "s7-does-not-pay-for-s0-s6 §7 present, §0-§6 over 100 lines: still refused (got: $d)" '[ "$d" = "rc 2" ]'
e=$(python3 -I $D/drive.py "$R0" 40 500 1 $D/r5 2>$D/e5|tail -1);ok "m-whole-card-count-RED a guard that counts the whole card refuses the 500-row §7 lane (got: $e, want rc 2): the s7-500-lines lane catches it" '[ "$e" = "rc 2" ]'
echo "card-cap.t.sh: $f FAIL";exit $f
