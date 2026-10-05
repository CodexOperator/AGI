#!/bin/sh
# agi-run-strace.t.sh: T1 of goal:g7.16.1.11.16 — shell twin of test_agi_run_strace.py
# (agi-run strace line detaches at each child exec: -b execve, not seccomp).
# One ok/FAIL line per named case; exit = FAIL count. sh + strace; no python.
R0=${ROOT:-$(cd "$(dirname "$0")/../../.." && pwd)}
WRAP=$R0/.agi/nodes/.geometry/engine-wrap.md
f=0
ok(){ if eval "$2";then echo "ok $1";else echo "FAIL $1";f=$((f+1));fi;}
line=$(grep -E '^exec strace ' "$WRAP" | head -1)
ok "f1_line_detaches_at_exec_not_seccomp" 'printf %s "$line" | grep -q -- "-b execve" && printf %s "$line" | grep -vq -- "--seccomp-bpf"'
command -v strace >/dev/null || { echo "FAIL strace-absent"; exit 99; }
# flags up to -o sink (same cut as the py twin: tokens after strace until -o)
flags=$(printf '%s\n' "$line" | awk '{
  for (i=2;i<=NF;i++) { if ($i ~ /^-o/) break; printf "%s ", $i }
}')
D=$(mktemp -d)
trap 'rm -rf "$D"' 0
printf x >"$D/direct-a.txt"
printf x >"$D/exec-child-b.txt"
# trailing : keeps sh forking cat, not execing it
strace $flags -o "$D/trace" sh -c ": <$D/direct-a.txt; cat $D/exec-child-b.txt >/dev/null; :" 2>/dev/null
ok "f2_direct_command_open_in_stream" 'grep -E "open(at)?\\(" "$D/trace" | grep -q "direct-a.txt"'
ok "execd_grandchild_open_not_in_stream" 'grep -E "open(at)?\\(" "$D/trace" | grep -q "direct-a.txt" && ! grep -E "open(at)?\\(" "$D/trace" | grep -q "exec-child-b.txt"'
exit $f
