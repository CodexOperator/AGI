#!/bin/sh
# verify-v5-uid.t.sh: goal:g7.16.1.11.19 (falsifier lanes, DG1 15:23Z): `commands.py run verify` / verification.py run as a v5 uid (NOT the uid that owns the shared files) must SKIP what it cannot read, with the path and the reason, instead of crashing; a skip is never a pass.
# sh + python3 on a SCRATCH project (git init, .agi/ with config:seats + config:commands nodes): no pytest, no network, 0 USD, nothing under the live repo. BIN = the extensions/agi/bin dir under test (default: ROOT's); a mutation / reference = BIN=<an edited copy of that dir>. One ok/FAIL line per case; exit = FAIL count.
# Needs a NON-ROOT uid: root reads a mode-000 file, so every unreadable-path lane would be VACUOUS; l0 fails loudly instead of letting them pass by luck.
# Seams pinned (no wording beyond what the goal names): STATUS of a CheckResult (SKIP is a status, as check_extra_suite already has), NOTE contains the path and the word permission (any case), a traceback / PermissionError count of 0 over stdout+stderr, the summary's RESULT line. HOW a subprocess check signals its skip is NOT pinned (L3 asserts at run_check level: status + note).
# Lanes: L1 a pin whose transcript sits under a MODE-000 dir: check_seat_model = SKIP with path + permission, no exception (+ mixed with a drifted seat: the drift still FAILs; mixed with a clean seat: not FAIL, the path is named) · L2 the same through run_level (the check after it still runs: a verdict exists) and through the CLI (the seat-model line is SKIP, the RESULT line printed) · L3 an unreadable .env: the credentials, secrets and (appended at every level) anonymize subprocess checks = SKIP at run_check level (+ a readable .env control: not SKIP) · L4 controls: a readable transcript still PASS (model=row) / DRIFT FAIL, a stale pin still prints its stale-pin line · L5 PermissionError + Traceback = 0 over stdout+stderr at --level rotation and --level full --verbose · L6 a skip is never a pass: render_summary of PASS+SKIP does not say all-green and names the skip, of only skips does not say PASS, all-PASS is unchanged, a FAIL stays FAIL · L7 a dangling symlink / a directory as the transcript path = SKIP naming it · L8 (DG3 15:26Z) a --suite run whose sessions dir this uid cannot write (the suite stamp, the verified stamp) completes with its RESULT line, no traceback · L9 (DG3 15:26Z) pytest absent for this uid (`No module named pytest`) = SKIP, not FAIL, for the `tests` check and for the declared second suite (l9b), and a --suite run without pytest completes (l9c: suite_guards imports pytest at module level, the crash a no-pytest uid hits first).
T=$(mktemp -d);trap 'chmod -R u+rwx $T 2>/dev/null;rm -rf $T' 0;f=0;R0=${ROOT:-$(cd "$(dirname "$0")/../../.." && pwd)};BIN=${BIN:-$R0/extensions/agi/bin};SRC=$R0/extensions/agi/src
ok(){ if eval "$2";then echo "ok $1";else echo "FAIL $1";f=$((f+1));fi;}
unset GIT_AUTHOR_NAME GIT_AUTHOR_EMAIL GIT_COMMITTER_NAME GIT_COMMITTER_EMAIL GIT_DIR GIT_WORK_TREE AGI_TRUNK AGI_SEAT AGI_POST
printf '[user]\n\tname=t\n\temail=t@t\n[commit]\n\tgpgsign=false\n[safe]\n\tdirectory=*\n' >$T/gitconfig;export GIT_CONFIG_GLOBAL=$T/gitconfig GIT_CONFIG_SYSTEM=/dev/null PYTHONDONTWRITEBYTECODE=1
M="claude-opus-5"
# the python driver: one command per call, every outcome printed as flat lines (STATUS, NOTE as a json string, EXC <type> when anything raised)
cat >$T/drv.py <<'PYEOF'
import json, os, sys
sys.path.insert(0, sys.argv[1]); sys.path.insert(0, sys.argv[2])
from pathlib import Path
import verification
cmd, groot = sys.argv[3], Path(sys.argv[4])
def show(r):
    print("STATUS", r.status); print("NOTE", json.dumps(r.note)); print("NUMBER", json.dumps(r.number))
try:
    if cmd == "seat":
        show(verification.check_seat_model(groot))
    elif cmd == "level":
        for r in verification.run_level(groot, "rotation", False, False):
            print("RES", r.name, r.status, json.dumps(r.note))
    elif cmd == "check":
        show(verification.run_check(groot, sys.argv[5], False))
    elif cmd == "count":
        if os.environ.get("FAKEUID"): os.geteuid = lambda: int(os.environ["FAKEUID"])
        show(verification.compare_count(groot, {"active": 5, "deprecated": 1, "total": 6}, stamp=True)); print("IOERR", len(verification._IO_ERRORS))
    elif cmd == "anon":
        show(verification.check_anonymize(groot))
    elif cmd == "extra":
        stub = sys.argv[5]; sys.executable = stub      # a python with no pytest: hermetic on a host that HAS pytest
        show(verification.check_extra_suite(groot))
    elif cmd == "summary":
        rs = [verification.CheckResult(n, s, 0.0) for n, s in (x.split(":") for x in sys.argv[5:])]
        print(verification.render_summary("rotation", False, rs))
except BaseException as e:   # noqa: BLE001
    print("EXC", type(e).__name__, str(e)[:160])
PYEOF
drv(){ (cd $P&&python3 $T/drv.py $BIN $SRC "$@" 2>&1);}
cli(){ (cd $P&&PYTHONPATH=$SRC python3 $BIN/verification.py "$@" 2>&1);}
st(){ sed -n 's/^STATUS //p' $1|head -1;}
nt(){ sed -n 's/^NOTE //p' $1|head -1;}
# ---- fixtures
mkdir -p $T/ok $T/drift $T/locked $T/adir/t.jsonl $T/gone $T/dang
tj(){ for m in "$@";do printf '{"type":"assistant","timestamp":"2026-09-10T20:30:00.0Z","message":{"role":"assistant","model":"%s"}}\n' $m;done;}
tj $M $M $M >$T/ok/t.jsonl;tj $M claude-opus-4-8 >$T/drift/t.jsonl;tj $M >$T/locked/t.jsonl;ln -s $T/gone/t.jsonl $T/dang/t.jsonl
chmod 000 $T/locked
# proj NAME: a scratch project; seat NAME MODEL TRANSCRIPT [PINGEN [RECGEN]] adds a row + its pin + its rotation record; seats writes the node
proj(){ P=$T/$1;G=$P/.agi;rm -rf $P;mkdir -p $G/nodes/.geometry $G/sessions/rotations;$(command -v git) init -q $P;echo '{}'>$G/config.json;ROWS=;}
seat(){ ROWS="$ROWS  - {name: $1, role: director, tier: 1, model: $2, session_ref: 4a9edc, pin_ref: .agi/sessions/$1.meter}
";printf '%s\t%s\n' ${4:-4} $3 >$G/sessions/$1.meter;echo "{\"rotation\":\"rotate-self\",\"seat\":\"$1\",\"gen_after\":${5:-4}}" >$G/sessions/rotations/$1.20260917T000000Z.rotation.json;}
seats(){ printf -- '---\ntype: config\nparents: [goal:g17]\nseats:\n%s---\n' "$ROWS" >$G/nodes/.geometry/seats.md;}
cmds(){ { printf -- '---\nid: command:commands\ntype: command\ncommands:\n';cat; printf -- '---\n'; } >$G/nodes/.geometry/commands.md;}
ENVCMDS='  credentials:
    argv: [python3, <engine>/extensions/agi/bin/provisioning.py, status]
  secrets:
    argv: [python3, <engine>/extensions/agi/bin/envfile.py, "--check"]'
ok "l0-non-root the unreadable-path lanes need a non-root uid (this one is $(id -u)): root reads a mode-000 file, so the lanes below would pass by luck" '[ "$(id -u)" != 0 ]'
# ---- L1 / L4: check_seat_model
proj p1;seat s1 $M $T/locked/t.jsonl;seats;drv seat $G >$T/l1.out
ok "l1-locked-transcript-skips a pin whose transcript sits under a mode-000 dir: check_seat_model returns STATUS SKIP ($(st $T/l1.out)) naming the path and the permission, no exception ($(grep -c '^EXC' $T/l1.out) EXC): $(nt $T/l1.out|cut -c1-150); today PermissionError at verification.py _seat_transcript (lp.exists())" '[ "$(st $T/l1.out)" = SKIP ]&&nt $T/l1.out|grep -q "locked/t.jsonl"&&nt $T/l1.out|grep -qi permission&&! grep -q "^EXC" $T/l1.out'
proj p1b;seat s1 $M $T/locked/t.jsonl;seat s2 $M $T/drift/t.jsonl;seats;drv seat $G >$T/l1b.out
ok "l1b-skip-never-masks-a-drift a locked seat beside a DRIFTED one: the check is still FAIL ($(st $T/l1b.out)) and names s2's drift (live=claude-opus-4-8), and the locked path is named too" '[ "$(st $T/l1b.out)" = FAIL ]&&nt $T/l1b.out|grep -q "s2: DRIFT live=claude-opus-4-8"&&nt $T/l1b.out|grep -q "locked/t.jsonl"&&! grep -q "^EXC" $T/l1b.out'
proj p1c;seat s1 $M $T/locked/t.jsonl;seat s2 $M $T/ok/t.jsonl;seats;drv seat $G >$T/l1c.out
ok "l1c-locked-beside-a-clean-seat a locked seat beside a clean one: no exception, not FAIL ($(st $T/l1c.out)), s2's own line is still model=row, and the locked path + permission are named (status not pinned: PASS or SKIP is the fix's call)" '[ -n "$(st $T/l1c.out)" ]&&[ "$(st $T/l1c.out)" != FAIL ]&&nt $T/l1c.out|grep -q "s2: model=$M row=$M"&&nt $T/l1c.out|grep -q "locked/t.jsonl"&&nt $T/l1c.out|grep -qi permission'
proj p4;seat s1 $M $T/ok/t.jsonl;seats;drv seat $G >$T/l4a.out
ok "l4a-readable-transcript-passes (control) a readable transcript with no drift is still PASS ($(st $T/l4a.out)) printing model=row: $(nt $T/l4a.out|cut -c1-90)" '[ "$(st $T/l4a.out)" = PASS ]&&nt $T/l4a.out|grep -q "s1: model=$M row=$M"'
proj p4b;seat s1 $M $T/drift/t.jsonl;seats;drv seat $G >$T/l4b.out
ok "l4b-readable-drift-fails (control) a readable drifted transcript is still FAIL ($(st $T/l4b.out)) with the DRIFT line: $(nt $T/l4b.out|cut -c1-110)" '[ "$(st $T/l4b.out)" = FAIL ]&&nt $T/l4b.out|grep -q "DRIFT live=claude-opus-4-8 row=$M"'
proj p4c;seat s1 $M $T/ok/t.jsonl;seat s2 $M $T/ok/t.jsonl 3 4;seats;drv seat $G >$T/l4c.out
ok "l4c-stale-pin-skip-line (control) a pin of generation 3 against a seat at generation 4 still prints its stale-pin skip line, beside a clean seat that still reads model=row (status $(st $T/l4c.out), not FAIL): $(nt $T/l4c.out|cut -c1-140)" '[ -n "$(st $T/l4c.out)" ]&&[ "$(st $T/l4c.out)" != FAIL ]&&nt $T/l4c.out|grep -q "s2: stale-pin (gen 3 vs current 4), skipped"&&nt $T/l4c.out|grep -q "s1: model=$M row=$M"'
# ---- L7: a dangling symlink / a directory as the transcript path
proj p7a;seat s1 $M $T/dang/t.jsonl;seats;drv seat $G >$T/l7a.out
ok "l7a-dangling-symlink-skips a pin whose transcript is a dangling symlink: STATUS SKIP ($(st $T/l7a.out)) naming the path, no exception: $(nt $T/l7a.out|cut -c1-130)" '[ "$(st $T/l7a.out)" = SKIP ]&&nt $T/l7a.out|grep -Eq "(dang|gone)/t.jsonl"&&! grep -q "^EXC" $T/l7a.out'
proj p7b;seat s1 $M $T/adir/t.jsonl;seats;drv seat $G >$T/l7b.out
ok "l7b-directory-as-transcript-skips a pin whose transcript path is a DIRECTORY: STATUS SKIP ($(st $T/l7b.out)) naming the path, no exception (today: 'no assistant turns with a model (skipped)', the path lost): $(nt $T/l7b.out|cut -c1-130)" '[ "$(st $T/l7b.out)" = SKIP ]&&nt $T/l7b.out|grep -q "adir/t.jsonl"&&! grep -q "^EXC" $T/l7b.out'
# ---- L2 / L5: through run_level and the CLI (the seat-model check sits before node-dirs / formation / census / node-count: the run must reach them)
proj p2;seat s1 $M $T/locked/t.jsonl;seats;drv level $G >$T/l2.out
sl=$(grep -n '^RES seat-model ' $T/l2.out|cut -d: -f1);nl=$(grep -c '^RES ' $T/l2.out)
ok "l2-run-level-reaches-the-last-check run_level at the rotation level returns every result instead of raising ($(grep -c '^EXC' $T/l2.out) EXC), seat-model is SKIP ($(sed -n 's/^RES seat-model \([A-Z]*\) .*/\1/p' $T/l2.out)) and a check AFTER it still ran (seat-model is result ${sl:-none} of $nl)" '[ -n "$sl" ]&&[ "$sl" -lt "$nl" ]&&grep -q "^RES seat-model SKIP " $T/l2.out&&! grep -q "^EXC" $T/l2.out'
cli --level rotation >$T/l2c.out;crc=$?
ok "l2b-cli-prints-the-skip-in-the-verdict verification.py --level rotation in the scratch project: the verdict is PRINTED (a RESULT line: $(grep -c '^RESULT:' $T/l2c.out)), the seat-model line is SKIP and carries the path ($(grep ' seat-model ' $T/l2c.out|cut -c1-120)), 0 Traceback" '[ "$(grep -c "^RESULT:" $T/l2c.out)" = 1 ]&&grep "^SKIP .*seat-model" $T/l2c.out|grep -q "locked/t.jsonl"&&[ "$(grep -c Traceback $T/l2c.out)" = 0 ]'
proj p5;seat s1 $M $T/locked/t.jsonl;seats;cmds <<EOF
$ENVCMDS
EOF
echo 'OPENROUTER_PROVISIONING_KEY=x'>$P/.env;chmod 000 $P/.env
cli --level full --verbose >$T/l5.out;cli --level rotation >$T/l5r.out
ok "l5-no-permissionerror-no-traceback stdout+stderr of --level rotation and of --level full --verbose (an unreadable transcript AND an unreadable .env): PermissionError $(cat $T/l5.out $T/l5r.out|grep -c PermissionError) (want 0), Traceback $(cat $T/l5.out $T/l5r.out|grep -c Traceback) (want 0)" '[ "$(cat $T/l5.out $T/l5r.out|grep -c PermissionError)" = 0 ]&&[ "$(cat $T/l5.out $T/l5r.out|grep -c Traceback)" = 0 ]'
# ---- L3: the .env readers are SUBPROCESS checks (provisioning.py status, envfile.py --check), asserted at run_check level
for c in credentials secrets;do drv check $G $c >$T/l3$c.out
ok "l3-$c-unreadable-env-skips $c over a mode-000 .env: run_check STATUS SKIP ($(st $T/l3$c.out)), the note names the path and the permission, no Traceback in it, no exception: $(nt $T/l3$c.out|cut -c1-120)" '[ "$(st $T/l3$c.out)" = SKIP ]&&nt $T/l3$c.out|grep -q "\.env"&&nt $T/l3$c.out|grep -qi permission&&! nt $T/l3$c.out|grep -q Traceback&&! grep -q "^EXC" $T/l3$c.out';done
drv anon $G >$T/l3anon.out
ok "l3-anonymize-unreadable-env-skips the anonymize check (appended at EVERY level) reads .env too: over a mode-000 .env its STATUS is SKIP ($(st $T/l3anon.out)), the note names the path and the permission, no Traceback in it: $(nt $T/l3anon.out|cut -c1-120); today FAIL with the PermissionError line" '[ "$(st $T/l3anon.out)" = SKIP ]&&nt $T/l3anon.out|grep -q "\.env"&&nt $T/l3anon.out|grep -qi permission&&! nt $T/l3anon.out|grep -q Traceback&&! grep -q "^EXC" $T/l3anon.out'
chmod 600 $P/.env;drv check $G credentials >$T/l3c.out;drv check $G secrets >$T/l3d.out
ok "l3c-readable-env-runs-the-check (control) the same two checks over a READABLE .env are not SKIPPED ($(st $T/l3c.out)/$(st $T/l3d.out)): the script's own verdict stands" '[ -n "$(st $T/l3c.out)" ]&&[ "$(st $T/l3c.out)" != SKIP ]&&[ "$(st $T/l3d.out)" != SKIP ]&&! grep -q "^EXC" $T/l3c.out $T/l3d.out'
# ---- L6: a skip is never a pass (render_summary is pure: it takes the results)
P=$T/p5;drv summary $G a:PASS b:SKIP >$T/l6a.out;drv summary $G a:SKIP b:SKIP >$T/l6b.out;drv summary $G a:PASS b:PASS >$T/l6c.out;drv summary $G a:FAIL b:SKIP >$T/l6d.out
ok "l6a-pass-plus-skip-is-not-all-green a summary of one PASS and one SKIP does not say 'all 2 checks green' and its RESULT line names the skip: $(grep '^RESULT' $T/l6a.out|cut -c1-90)" '! grep "^RESULT" $T/l6a.out|grep -q "all 2 checks green"&&grep "^RESULT" $T/l6a.out|grep -qi skip'
ok "l6b-only-skips-is-not-a-pass a summary of only SKIPs does not print RESULT: PASS: $(grep '^RESULT' $T/l6b.out|cut -c1-90)" '[ "$(grep -c "^RESULT" $T/l6b.out)" = 1 ]&&! grep "^RESULT" $T/l6b.out|grep -q PASS'
ok "l6c-all-pass-unchanged (control) two PASS = the old line: $(grep '^RESULT' $T/l6c.out)" 'grep -q "^RESULT: PASS (all 2 checks green)" $T/l6c.out'
ok "l6d-fail-plus-skip-stays-fail (control) a FAIL beside a SKIP is still RESULT: FAIL: $(grep '^RESULT' $T/l6d.out|cut -c1-90)" 'grep "^RESULT" $T/l6d.out|grep -q "^RESULT: FAIL"'
# ---- L8: the stamps live in the shared sessions dir; a uid that cannot write there still gets its verdict. Fixture: the quick level + a passing stub suite = all green, so BOTH stamps are written when they can be. A stub `pytest` module is on PYTHONPATH here ONLY so that the second-suite import (suite_guards does `import pytest`, lane l9c) cannot decide this lane
mkdir -p $T/stub;printf 'def fixture(*a, **k):\n    if a and callable(a[0]) and not k:\n        return a[0]\n    return lambda f: f\n'>$T/stub/pytest.py
proj p8;cmds <<'EOF'
  links:
    argv: [python3, -c, "print('0 broken')"]
  write-guard:
    argv: [python3, -c, pass]
  tests:
    argv: [python3, -c, "print('1 passed in 0.01s')"]
EOF
(cd $P&&PYTHONPATH=$T/stub:$SRC python3 $BIN/verification.py --level quick --suite) >$T/l8c.out 2>&1
ok "l8c-writable-sessions-dir-stamps (control) the SAME fixture with a writable sessions dir is all green ($(grep '^RESULT:' $T/l8c.out|cut -c1-60)) and writes the verified stamp ($(ls $G/sessions|tr '\n' ' ')): the lane below really reaches the write" 'grep -q "^RESULT: PASS" $T/l8c.out&&[ -e $G/sessions/verified.stamp ]'
rm -f $G/sessions/verified.stamp $G/sessions/verify-suite-ts.json;chmod 555 $G/sessions
(cd $P&&PYTHONPATH=$T/stub:$SRC python3 $BIN/verification.py --level quick --suite) >$T/l8.out 2>&1;chmod 755 $G/sessions
ok "l8-unwritable-sessions-dir-completes a --suite run whose sessions dir this uid cannot write (the suite stamp, the verified stamp): the RESULT line is printed ($(grep -c '^RESULT:' $T/l8.out)), 0 PermissionError ($(grep -c PermissionError $T/l8.out)), 0 Traceback ($(grep -c Traceback $T/l8.out)); a write that fails in a dir THIS uid owns is a named ERROR and rc 2 (D6, d6g), never a traceback: only the printed verdict and 0 PermissionError / Traceback are pinned HERE" '[ "$(grep -c "^RESULT:" $T/l8.out)" = 1 ]&&[ "$(grep -c PermissionError $T/l8.out)" = 0 ]&&[ "$(grep -c Traceback $T/l8.out)" = 0 ]'
# ---- L9: pytest absent for this uid = SKIP. The `tests` check runs a declared argv: the stub prints exactly what python prints without pytest. The declared second suite is run through sys.executable: the driver swaps in a python-without-pytest stub (hermetic on a host that HAS pytest)
proj p9;cmds <<'EOF'
  tests:
    argv: [python3, -c, "import sys;sys.stderr.write('/usr/bin/python3: No module named pytest\\n');sys.exit(1)"]
EOF
mkdir -p $P/tests;echo '{"paths":{"core":{"suite_roots":["tests"]}}}'>$G/config.json;G9=$G
printf '#!/bin/sh\necho "/usr/bin/python3: No module named pytest" >&2\nexit 1\n'>$T/nopytest;chmod +x $T/nopytest
drv check $G tests >$T/l9a.out;drv extra $G $T/nopytest >$T/l9b.out
ok "l9a-no-pytest-skips-the-suite the declared suite check on a uid with no pytest is STATUS SKIP ($(st $T/l9a.out)) naming pytest, not a FAIL: $(nt $T/l9a.out|cut -c1-110)" '[ "$(st $T/l9a.out)" = SKIP ]&&nt $T/l9a.out|grep -qi pytest&&! grep -q "^EXC" $T/l9a.out'
ok "l9b-no-pytest-skips-the-second-suite the declared second suite (context-suite) with no pytest is STATUS SKIP ($(st $T/l9b.out)) naming pytest: $(nt $T/l9b.out|cut -c1-110)" '[ "$(st $T/l9b.out)" = SKIP ]&&nt $T/l9b.out|grep -qi pytest&&! grep -q "^EXC" $T/l9b.out'
proj p9c;cmds <<'EOF'
  tests:
    argv: [python3, -c, "print('1 passed in 0.01s')"]
EOF
(cd $P&&PYTHONPATH=$SRC python3 $BIN/verification.py --level quick --suite) >$T/l9c.out 2>&1
ok "l9c-suite-run-without-pytest-completes a --suite run on a uid whose python has NO pytest still prints its verdict ($(grep -c '^RESULT:' $T/l9c.out) RESULT line, $(grep -c Traceback $T/l9c.out) Traceback): the second suite's import of suite_guards (import pytest at module level) must not crash the run. Green by luck on a host that HAS pytest (then l9b's stub is the guard)" '[ "$(grep -c "^RESULT:" $T/l9c.out)" = 1 ]&&[ "$(grep -c Traceback $T/l9c.out)" = 0 ]'
# ---- D (DG1 16:25Z, SM mur-sm21-dg3-verify5 DEMOTE of 23a6591f72; the 25 lanes above are kept): a SKIPPED suite is never a pass, the no-pytest SKIP is the exact import failure only, a stale stamp never survives a non-green run, the permission SKIP is owner-aware, a write failure on the writer uid is never PASS rc 0.
# dproj NAME: a quick-level project whose links / write-guard are stubs (links reads the LINKS text) and whose `tests` command comes from stdin; a stale verified.stamp is planted when STALE=1
dproj(){ proj $1;{ printf '  links:\n    argv: [python3, -c, "print(%s)"]\n  write-guard:\n    argv: [python3, -c, pass]\n' "'${LINKS:-0 broken}'";cat; }|cmds;[ "$STALE" = 1 ]&&echo stale >$G/sessions/verified.stamp;return 0;}
CS(){ (cd $P&&PYTHONPATH=$T/stub:$SRC python3 $BIN/verification.py "$@" 2>&1);}
NOPY="import sys;sys.stderr.write('/usr/bin/python3: No module named pytest\\n');sys.exit(1)"
cat >$T/t.skip <<'EOF'
  tests:
    argv: [python3, -c, "import sys;sys.stderr.write('/usr/bin/python3: No module named pytest\\n');sys.exit(1)"]
EOF
cat >$T/t.green <<'EOF'
  tests:
    argv: [python3, -c, "print('1 passed in 0.01s')"]
EOF
cat >$T/t.red <<'EOF'
  tests:
    argv: [python3, -c, "print('FAILED t.py::test_x - AssertionError: wanted No module named pytest');print('1 failed, 3 passed in 0.10s');import sys;sys.exit(1)"]
EOF
cat >$T/t.skip2 <<'EOF'
  tests:
    argv: [python3, -c, "import sys;sys.stderr.write('/opt/py/bin/python3.12: No module named pytest\\n');sys.exit(1)"]
EOF
# D1: a --suite run whose tests = SKIP and every other check PASS must NOT exit 0, and the merge-up reader (rotate._merge_up_suite: rc 0 = suite passed) must read it as NOT passed
LINKS='0 broken' STALE= dproj d1 <$T/t.skip;CS --level quick --suite >$T/d1.out;d1rc=$?;d1st=$([ -e $G/sessions/verified.stamp ]&&echo STAMP||echo none)
dproj d1g <$T/t.green;CS --level quick --suite >$T/d1g.out;d1grc=$?
ok "d1a-skipped-suite-is-not-rc-0 a --suite run with tests = SKIP and every other check PASS exits $d1rc (want != 0 and != 1: nothing FAILED, nothing was verified) and does not print an all-green RESULT ($(grep '^RESULT' $T/d1.out|cut -c1-70)); today rc 0 = a uid with no pytest merges with NO test run" '[ $d1rc != 0 ]&&[ $d1rc != 1 ]&&! grep "^RESULT" $T/d1.out|grep -q "all [0-9]* checks green"'
ok "d1f-mixed-skip-and-pass-pins-no-stamp the same mixed run (tests = SKIP, links + write-guard + the rest PASS) writes NO sessions/verified.stamp ($d1st): a SKIP among PASS rows certifies nothing for --delete-old (d4b pins the stale-stamp half)" '[ "$d1st" = none ]'
ok "d1c-green-suite-still-rc-0 (control) the same fixture with a passing suite exits $d1grc (want 0): $(grep '^RESULT' $T/d1g.out|cut -c1-70)" '[ $d1grc = 0 ]&&grep -q "^RESULT: PASS" $T/d1g.out'
mu(){ (cd $P&&python3 -c "
import sys;sys.path.insert(0,'$SRC');sys.path.insert(0,'$BIN')
from pathlib import Path
import rotate
try:
    ok,detail,counts=rotate._merge_up_suite(Path('$G'),Path('$P'));print('MU',ok,detail.split(';')[0][:40])
except BaseException as e: print('EXC',type(e).__name__,str(e)[:80])
" 2>&1|tail -1);}
dproj d1m <$T/t.skip;mus=$(PYTHONPATH=$T/stub:$SRC mu);dproj d1n <$T/t.green;mug=$(PYTHONPATH=$T/stub:$SRC mu)
ok "d1b-merge-up-reads-a-skipped-suite-as-not-passed rotate._merge_up_suite (the real function, rc 0 = passed) over the SKIPPED-suite fixture returns '$mus' (want MU False ...); a uid with no pytest merges nothing" 'case "$mus" in "MU False"*);;*)false;;esac'
ok "d1d-merge-up-passes-a-green-suite (control) the same function over a passing suite returns '$mug' (want MU True ...)" 'case "$mug" in "MU True"*);;*)false;;esac'
# D3: only the exact import failure of pytest itself is SKIP; a genuinely red suite that QUOTES the phrase is FAIL rc 1
LINKS='0 broken' dproj d3 <$T/t.red;CS --level quick --suite >$T/d3.out;d3rc=$?;drv check $G tests >$T/d3c.out
ok "d3a-red-suite-quoting-the-phrase-is-fail a suite that really failed ('1 failed') and whose output quotes 'No module named pytest' is FAIL (run_check STATUS $(st $T/d3c.out)) and the run exits $d3rc (want 1): $(grep '^RESULT' $T/d3.out|cut -c1-60)" '[ "$(st $T/d3c.out)" = FAIL ]&&[ $d3rc = 1 ]'
dproj d3b <$T/t.skip2;drv check $G tests >$T/d3d.out;dproj d3e <$T/t.skip;drv check $G tests >$T/d3e.out
ok "d3b-exact-import-failure-is-skip-whatever-the-interpreter the exact one-line import failure ('<any python path>: No module named pytest') is SKIP: /opt/py/bin/python3.12 -> $(st $T/d3d.out), /usr/bin/python3 -> $(st $T/d3e.out) (the control: the SKIP is not tied to one path)" '[ "$(st $T/d3d.out)" = SKIP ]&&[ "$(st $T/d3e.out)" = SKIP ]'
printf '#!/bin/sh\necho "FAILED c.py::test_y - AssertionError: No module named pytest" >&2\necho "2 failed, 1 passed in 0.2s" >&2\nexit 1\n' >$T/redpy;chmod +x $T/redpy;P=$T/p9;(cd $P&&PYTHONPATH=$T/stub:$SRC python3 $T/drv.py $BIN $SRC extra $G9 $T/redpy 2>&1) >$T/d3f.out   # the stub pytest on the path: suite_guards imports, so the SKIP cannot come from a missing pytest module
ok "d3c-second-suite-red-quoting-the-phrase-is-fail the declared second suite that really failed and quotes the phrase is STATUS $(st $T/d3f.out) (want FAIL), the exact import failure stays SKIP (l9b)" '[ "$(st $T/d3f.out)" = FAIL ]'
# D4: a stale verified.stamp never survives a non-green run: RED even when the suite is SKIP, and a SKIPPED-suite all-green run (rc != 0) certifies nothing and retracts the old stamp too
LINKS='3 broken' STALE=1 dproj d4 <$T/t.skip;CS --level quick --suite >$T/d4.out;d4rc=$?
ok "d4a-red-run-retracts-the-stamp-even-when-the-suite-is-skip a run with links FAIL and tests SKIP (rc $d4rc, want 1) leaves NO verified.stamp ($([ -e $G/sessions/verified.stamp ]&&echo STALE STAMP SURVIVES||echo gone))" '[ $d4rc = 1 ]&&[ ! -e $G/sessions/verified.stamp ]'
LINKS='0 broken' STALE=1 dproj d4b <$T/t.skip;CS --level quick --suite >$T/d4b.out
ok "d4b-skipped-suite-certifies-nothing a SKIPPED-suite all-green run neither writes a stamp nor leaves a stale one ($([ -e $G/sessions/verified.stamp ]&&echo STAMP PRESENT||echo none))" '[ ! -e $G/sessions/verified.stamp ]'
# D2: the permission SKIP is owner-aware: a PermissionError line naming a path THIS uid can read and write is a genuine failure (FAIL), a path it cannot read is SKIP. Checked for a run_check command (credentials) and for the anonymize check
echo mine >$T/mine.txt;chmod 644 $T/mine.txt;echo theirs >$T/theirs.txt;chmod 000 $T/theirs.txt
mkpe(){ printf '  credentials:\n    argv: [python3, -c, "import sys;sys.stderr.write(\\"PermissionError: [Errno 13] Permission denied: '"'"'%s'"'"'\\\\n\\");sys.exit(1)"]\n' $1;}
proj d2a;mkpe $T/mine.txt|cmds;drv check $G credentials >$T/d2a.out;proj d2b;mkpe $T/theirs.txt|cmds;drv check $G credentials >$T/d2b.out
ok "d2a-readable-path-is-a-genuine-failure a check that died with a PermissionError line naming a path this uid CAN read and write ($T/mine.txt) is FAIL (STATUS $(st $T/d2a.out)), not SKIP: the writer uid's own failure must stay red" '[ "$(st $T/d2a.out)" = FAIL ]'
ok "d2b-unreadable-path-is-skip (control) the same line naming a mode-000 file this uid cannot read is SKIP (STATUS $(st $T/d2b.out)) with the path in the note: $(nt $T/d2b.out|cut -c1-90)" '[ "$(st $T/d2b.out)" = SKIP ]&&nt $T/d2b.out|grep -q theirs.txt'
rm -rf $T/bin2;cp -r $BIN $T/bin2;proj d2c;for w in mine theirs;do printf '#!/usr/bin/env python3\nimport sys\nsys.stderr.write("PermissionError: [Errno 13] Permission denied: '"'"'%s'"'"'\\n")\nsys.exit(1)\n' $T/$w.txt >$T/bin2/anonymize.py;(cd $P&&python3 $T/drv.py $T/bin2 $SRC anon $G >$T/d2c.$w 2>&1);done
ok "d2c-anonymize-is-owner-aware-too the anonymize check (its own regex site) over a stub that dies naming a readable path is $(st $T/d2c.mine) (want FAIL), naming an unreadable one $(st $T/d2c.theirs) (want SKIP)" '[ "$(st $T/d2c.mine)" = FAIL ]&&[ "$(st $T/d2c.theirs)" = SKIP ]'
# D2 fail-closed (DG1 17:32Z N2): the permission SKIP needs a path that EXISTS and cannot be read / written; a PermissionError line naming a path that does not exist (vanished, never there) is a genuine failure
proj d2d;mkpe $T/vanished-nowhere.txt|cmds;drv check $G credentials >$T/d2d.out
ok "d2d-vanished-path-is-fail a check that died with a PermissionError line naming a path that does NOT exist ($([ -e $T/vanished-nowhere.txt ]&&echo EXISTS||echo absent)) is STATUS $(st $T/d2d.out) (want FAIL): nothing unreadable was found, so nothing may be skipped (d2b is the control: an existing mode-000 file stays SKIP)" '[ "$(st $T/d2d.out)" = FAIL ]'
# D2 refinement (DG1 17:40Z): 'vanished' is decided by stat, not exists(): a PermissionError naming a path under a mode-000 DIRECTORY (another uid's private dir, the core v5 case: stat itself fails) is a SKIP naming it; only a path that is really gone (FileNotFoundError / NotADirectoryError) is FAIL
mkdir $T/priv000;echo x >$T/priv000/file.txt;chmod 000 $T/priv000
proj d2e;mkpe $T/priv000/file.txt|cmds;drv check $G credentials >$T/d2e.out;proj d2f;mkpe $T/mine.txt/below.txt|cmds;drv check $G credentials >$T/d2f.out
ok "d2e-path-under-a-mode-000-dir-is-skip (control for the refinement) a PermissionError line naming a path under a mode-000 directory (stat fails; exists() would say absent) is STATUS $(st $T/d2e.out) (want SKIP) with the path in the note: $(nt $T/d2e.out|cut -c1-90); green on 0c6fc2d9a3, RED only on a plain exists() variant" '[ "$(st $T/d2e.out)" = SKIP ]&&nt $T/d2e.out|grep -q priv000'
ok "d2f-path-below-a-regular-file-is-fail a PermissionError line naming a path BELOW a regular file (NotADirectoryError: the path is really gone) is STATUS $(st $T/d2f.out) (want FAIL)" '[ "$(st $T/d2f.out)" = FAIL ]'
# D2 narrowing (DG1 17:50Z): only a PermissionError on the path's stat is 'behind another uid's wall'; ELOOP / ENAMETOOLONG / EIO on a path are the writer uid's own failure and stay FAIL (d2e and d2f are the controls on either side)
ln -s loopb $T/loopa;ln -s loopa $T/loopb;LONGN=$(printf 'n%.0s' $(seq 1 300))
proj d2g;mkpe $T/loopa|cmds;drv check $G credentials >$T/d2g.out;proj d2h;mkpe $T/$LONGN|cmds;drv check $G credentials >$T/d2h.out
ok "d2g-symlink-loop-path-is-fail a PermissionError line naming a SYMLINK-LOOP path (stat raises ELOOP, not a permission wall) is STATUS $(st $T/d2g.out) (want FAIL)" '[ "$(st $T/d2g.out)" = FAIL ]'
ok "d2h-overlong-name-is-fail a PermissionError line naming a path with a 300-character component (ENAMETOOLONG) is STATUS $(st $T/d2h.out) (want FAIL)" '[ "$(st $T/d2h.out)" = FAIL ]'
# D1 (all-SKIP, DG1 ruling 16:39Z): a --suite run in which EVERY result is SKIP (links + write-guard die naming the mode-000 file, tests = the exact no-pytest line, context-suite declares no roots, anonymize = a bin copy whose stub names the same file) is rc 3 and certifies nothing: no verified.stamp, fresh or stale
rm -rf $T/bin3;cp -r $BIN $T/bin3;printf '#!/usr/bin/env python3\nimport sys\nsys.stderr.write("PermissionError: [Errno 13] Permission denied: '"'"'%s'"'"'\\n")\nsys.exit(1)\n' $T/theirs.txt >$T/bin3/anonymize.py
cp $T/bin3/anonymize.py $T/pe.py
for st in fresh stale;do proj d1e$st;{ printf '  links:\n    argv: [python3, %s]\n  write-guard:\n    argv: [python3, %s]\n' $T/pe.py $T/pe.py;cat $T/t.skip;}|cmds;[ $st = stale ]&&echo stale >$G/sessions/verified.stamp;(cd $P&&PYTHONPATH=$T/stub:$SRC python3 $T/bin3/verification.py --level quick --suite >$T/d1e$st.out 2>&1);eval d1e${st}rc=$?;eval d1e${st}st='$([ -e $G/sessions/verified.stamp ]&&echo STAMP||echo none)';done
ok "d1e-all-skip-suite-run-is-rc-3-and-certifies-nothing a --suite run whose every result is SKIP (checks: $(grep -c '^SKIP' $T/d1efresh.out) SKIP rows, $(grep -c '^PASS' $T/d1efresh.out) PASS rows) exits $d1efreshrc fresh / $d1estalerc with a stale stamp (want 3 and 3) and leaves stamp: fresh $d1efreshst, stale $d1estalest (want none and none); 23a6591f72 already exits 3 here (its all-SKIP line) but leaves the STALE stamp the --delete-old gate reads as green. DG3/SM: test_verified_stamp_from_suite.py:69 test_skip_only_is_green_too becomes test_skip_only_is_not_green (rc 3, not stamp.exists()), a pytest edit not in this file" '[ $d1efreshrc = 3 ]&&[ $d1estalerc = 3 ]&&[ $d1efreshst = none ]&&[ $d1estalest = none ]'
# D6: an OSError on the stamp / state write on the WRITER uid (it owns the dir; the target is made unwritable by being a DIRECTORY: EISDIR, never /dev/full, whose read-merge would loop forever) is NOT PASS rc 0; on a dir another uid owns it is the named skip. Fixture: the all-green quick --suite project, the stamp / the state file replaced by a directory
LINKS='0 broken' STALE= dproj d6a <$T/t.green;mkdir $G/sessions/verified.stamp;CS --level quick --suite >$T/d6a.out;d6arc=$?
ok "d6a-stamp-write-failure-on-the-writer-uid-is-not-pass a green --suite run whose verified.stamp write fails (EISDIR) in a dir THIS uid owns exits $d6arc (want != 0), prints a named error ($(grep -ci 'is a directory\|cannot write' $T/d6a.out) line(s) naming it), 0 Traceback ($(grep -c Traceback $T/d6a.out)); today the OSError is swallowed and the run ends PASS rc 0" '[ $d6arc != 0 ]&&grep -qi "is a directory\|cannot write" $T/d6a.out&&[ "$(grep -c Traceback $T/d6a.out)" = 0 ]'
dproj d6b <$T/t.green;mkdir $G/sessions/verify-suite-ts.json;CS --level quick --suite >$T/d6b.out;d6brc=$?
ok "d6b-state-write-failure-on-the-writer-uid-is-not-pass the same with verify-suite-ts.json (the suite-completion record) made unwritable by being a directory (EISDIR; a /dev/full state file would make the read-merge loop forever): rc $d6brc (want != 0), named, 0 Traceback ($(grep -c Traceback $T/d6b.out))" '[ $d6brc != 0 ]&&grep -qi "no space\|cannot" $T/d6b.out&&[ "$(grep -c Traceback $T/d6b.out)" = 0 ]'
dproj d6c <$T/t.green;rm -rf $G/sessions;ln -s /usr/share $G/sessions;CS --level quick --suite >$T/d6c.out;d6crc=$?;rm -f $G/sessions
ok "d6c-foreign-owned-dir-is-the-named-skip (control) when the sessions dir belongs to another uid (a root-owned dir here) the write is the named 'skip: cannot write' line, the verdict is printed ($(grep -c '^RESULT:' $T/d6c.out)), no ERROR line for it ($(grep -c '^ERROR' $T/d6c.out)), 0 Traceback; the ONLY difference from d6a is who owns the dir" 'grep -q "skip: cannot" $T/d6c.out&&[ "$(grep -c "^RESULT:" $T/d6c.out)" = 1 ]&&[ "$(grep -c "^ERROR" $T/d6c.out)" = 0 ]&&[ "$(grep -c Traceback $T/d6c.out)" = 0 ]'
# D6 (DG1 17:32Z R1): the node-count BASELINE write (verify-count.json, written by --stamp on a committed tree) is the same class: a failure in a dir THIS uid owns is rc 2 with ONE named ERROR, never a swallowed skip with node-count PASS; in a dir another uid owns it is the named skip, rc as before (0). Fixture: smoke stub printing the METRIC counts, a committed scratch tree (so the stamp context is clean), verify-count.json made a directory (EISDIR)
dstampproj(){ { cat $T/t.green;printf '  smoke:\n    argv: [python3, -c, "print(\x27METRIC active_node_count=5\x27);print(\x27METRIC deprecated_node_count=1\x27);print(\x27METRIC node_count=6\x27)"]\n';} >$T/t.smoke;LINKS='0 broken' STALE= dproj $1 <$T/t.smoke;git -C $P add -A;git -C $P commit -qm fixture;}
dstampproj d6e;mkdir $G/sessions/verify-count.json;CS --level quick --stamp >$T/d6e.out;d6erc=$?
ok "d6e-baseline-write-failure-on-the-writer-uid-is-not-pass a --stamp run whose baseline write (verify-count.json, EISDIR) fails in a dir THIS uid owns exits $d6erc (want 2), prints ONE named error ($(grep -c '^ERROR: cannot write.*verify-count.json' $T/d6e.out) line(s); $(grep -c '^skip: cannot write.*verify-count.json' $T/d6e.out) skip line(s), want 0), 0 Traceback ($(grep -c Traceback $T/d6e.out)), and no 'baseline recorded' PASS is left standing ($(grep -c 'baseline recorded' $T/d6e.out) line(s); the file is $([ -d $G/sessions/verify-count.json ]&&echo still the directory||echo REPLACED))" '[ $d6erc = 2 ]&&[ "$(grep -c "^ERROR: cannot write.*verify-count.json" $T/d6e.out)" = 1 ]&&[ "$(grep -c "^skip: cannot write.*verify-count.json" $T/d6e.out)" = 0 ]&&[ "$(grep -c Traceback $T/d6e.out)" = 0 ]&&[ -d $G/sessions/verify-count.json ]'
dstampproj d6f;rm -rf $G/sessions;ln -s /usr/share $G/sessions;CS --level quick --stamp >$T/d6f.out;d6frc=$?;rm -f $G/sessions
ok "d6f-baseline-foreign-dir-is-the-named-skip (control) the same run when the sessions dir belongs to another uid (a root-owned dir): the named 'skip: cannot write' line for verify-count.json ($(grep -c '^skip: cannot write.*verify-count.json' $T/d6f.out)), no ERROR line for it ($(grep -c '^ERROR: cannot write.*verify-count.json' $T/d6f.out)), 0 Traceback, rc $d6frc as before (want 0: nothing FAILED)" '[ "$(grep -c "^skip: cannot write.*verify-count.json" $T/d6f.out)" = 1 ]&&[ "$(grep -c "^ERROR: cannot write.*verify-count.json" $T/d6f.out)" = 0 ]&&[ "$(grep -c Traceback $T/d6f.out)" = 0 ]&&[ $d6frc = 0 ]'
# D6 R2 (DG1 18:09Z, mur final on a159c558c6): the sessions dir itself MISSING under a parent this uid owns but made 555 (a mkdir that cannot happen): the mkdir sits inside the same try as the write, so a --stamp run (the baseline, _write_state) and a --suite run (the suite record, _record_suite_ts) end rc 2 with ONE named ERROR and no traceback. A parent another uid owns is the named skip; one uid cannot own a root-owned graph dir, so d6h flips the uid seam (os.geteuid) of the SAME process: the dir stays ours and 555, the code is told it is someone else's
dstampproj d6g1;rm -rf $G/sessions;chmod 555 $G;CS --level quick --stamp >$T/d6g1.out;d6g1rc=$?;chmod 755 $G
ok "d6g1-baseline-mkdir-failure-on-the-writer-uid-is-error-rc-2 a --stamp run whose sessions dir is MISSING under a parent this uid owns (555, so the mkdir fails) exits $d6g1rc (want 2), prints ONE named error for verify-count.json ($(grep -c '^ERROR: cannot write.*verify-count.json' $T/d6g1.out)), 0 Traceback ($(grep -c Traceback $T/d6g1.out)), the verdict is printed ($(grep -c '^RESULT:' $T/d6g1.out))" '[ $d6g1rc = 2 ]&&[ "$(grep -c "^ERROR: cannot write.*verify-count.json" $T/d6g1.out)" = 1 ]&&[ "$(grep -c Traceback $T/d6g1.out)" = 0 ]&&[ "$(grep -c "^RESULT:" $T/d6g1.out)" = 1 ]'
LINKS='0 broken' STALE= dproj d6g2 <$T/t.green;rm -rf $G/sessions;chmod 555 $G;CS --level quick --suite >$T/d6g2.out;d6g2rc=$?;chmod 755 $G
ok "d6g2-suite-record-mkdir-failure-on-the-writer-uid-is-error-rc-2 a green --suite run whose sessions dir is MISSING under a parent this uid owns (555): exits $d6g2rc (want 2), ONE named error for verify-suite-ts.json ($(grep -c '^ERROR: cannot write.*verify-suite-ts.json' $T/d6g2.out)), 0 Traceback ($(grep -c Traceback $T/d6g2.out)), the verdict is printed ($(grep -c '^RESULT:' $T/d6g2.out))" '[ $d6g2rc = 2 ]&&[ "$(grep -c "^ERROR: cannot write.*verify-suite-ts.json" $T/d6g2.out)" = 1 ]&&[ "$(grep -c Traceback $T/d6g2.out)" = 0 ]&&[ "$(grep -c "^RESULT:" $T/d6g2.out)" = 1 ]'
dstampproj d6h;rm -rf $G/sessions;chmod 555 $G;(cd $P&&FAKEUID=99999 PYTHONPATH=$T/stub:$SRC python3 $T/drv.py $BIN $SRC count $G) >$T/d6h.out 2>&1;chmod 755 $G
ok "d6h-baseline-mkdir-under-a-foreign-parent-is-the-named-skip (uid seam) the same missing sessions dir when the code is told the parent belongs to another uid (os.geteuid = 99999 in the driver; the dir stays ours and 555): the named 'skip: cannot write' for verify-count.json ($(grep -c '^skip: cannot write.*verify-count.json' $T/d6h.out)), no ERROR ($(grep -c '^ERROR' $T/d6h.out)), 0 recorded IO errors ($(sed -n 's/^IOERR //p' $T/d6h.out)), STATUS $(st $T/d6h.out) as before (want PASS), 0 EXC/Traceback ($(grep -c 'EXC\|Traceback' $T/d6h.out))" '[ "$(grep -c "^skip: cannot write.*verify-count.json" $T/d6h.out)" = 1 ]&&[ "$(grep -c "^ERROR" $T/d6h.out)" = 0 ]&&[ "$(sed -n "s/^IOERR //p" $T/d6h.out)" = 0 ]&&[ "$(st $T/d6h.out)" = PASS ]&&[ "$(grep -c "EXC\|Traceback" $T/d6h.out)" = 0 ]'
# D6 N4 (DG1 18:09Z, fail-closed): a run that exits non-zero from an IO error certifies nothing: no verified.stamp, and a stale one is retracted. d6j is the control (the same fixture without the failing baseline write DOES stamp, so the absence in d6i is not vacuous)
dstampproj d6j;CS --level quick --suite --stamp >$T/d6j.out;d6jrc=$?;d6jst=$([ -e $G/sessions/verified.stamp ]&&echo stamp||echo none)
ok "d6j-clean-suite-stamp-run-stamps (control) a green --suite --stamp run on the committed fixture exits $d6jrc (want 0) and writes verified.stamp ($d6jst, want stamp)" '[ $d6jrc = 0 ]&&[ "$d6jst" = stamp ]'
dstampproj d6i;mkdir -p $G/sessions;echo stale >$G/sessions/verified.stamp;mkdir $G/sessions/verify-count.json;CS --level quick --suite --stamp >$T/d6i.out;d6irc=$?;d6ist=$([ -e $G/sessions/verified.stamp ]&&echo STAMP||echo none)
ok "d6i-io-error-run-certifies-nothing the same green --suite --stamp run whose BASELINE write fails (EISDIR, as d6e) exits $d6irc (want 2) and leaves verified.stamp: $d6ist (want none: the stale stamp planted before the run is retracted, none is written)" '[ $d6irc = 2 ]&&[ "$d6ist" = none ]'
# D6 R2 wall (DG1 18:39Z, probe on e4d2bbdbc4): the sessions dir MISSING under an UNSEARCHABLE (mode-000) parent, the v5-uid case: the nearest-existing-ancestor walk must not raise (Path.exists() and stat() re-raise PermissionError). One uid cannot make the graph dir itself unsearchable and still run, so sessions is a symlink to <wall>/sessions with <wall> mode 000: every stat of it fails EACCES. Not provably ours = the named skip, no ERROR, rc as before, the verdict printed, no Traceback
dstampproj d6k1;rm -rf $G/sessions;mkdir $T/wall1;chmod 000 $T/wall1;ln -s $T/wall1/sessions $G/sessions;CS --level quick --stamp >$T/d6k1.out;d6k1rc=$?
ok "d6k1-baseline-write-behind-a-wall-is-the-named-skip a --stamp run whose sessions dir is missing under a MODE-000 parent: rc $d6k1rc (want 0), ONE 'skip: cannot write ...verify-count.json' ($(grep -c '^skip: cannot write.*verify-count.json' $T/d6k1.out)), 0 ERROR ($(grep -c '^ERROR' $T/d6k1.out)), 0 Traceback ($(grep -c Traceback $T/d6k1.out)), the verdict is printed ($(grep -c '^RESULT:' $T/d6k1.out))" '[ $d6k1rc = 0 ]&&[ "$(grep -c "^skip: cannot write.*verify-count.json" $T/d6k1.out)" = 1 ]&&[ "$(grep -c "^ERROR" $T/d6k1.out)" = 0 ]&&[ "$(grep -c Traceback $T/d6k1.out)" = 0 ]&&[ "$(grep -c "^RESULT:" $T/d6k1.out)" = 1 ]'
LINKS='0 broken' STALE= dproj d6k2 <$T/t.green;rm -rf $G/sessions;mkdir $T/wall2;chmod 000 $T/wall2;ln -s $T/wall2/sessions $G/sessions;CS --level quick --suite >$T/d6k2.out;d6k2rc=$?
ok "d6k2-suite-record-behind-a-wall-is-the-named-skip a green --suite run, same fixture: rc $d6k2rc (want 0), ONE 'skip: cannot write ...verify-suite-ts.json' ($(grep -c '^skip: cannot write.*verify-suite-ts.json' $T/d6k2.out)), 0 ERROR ($(grep -c '^ERROR' $T/d6k2.out)), 0 Traceback ($(grep -c Traceback $T/d6k2.out)), the verdict is printed ($(grep -c '^RESULT:' $T/d6k2.out))" '[ $d6k2rc = 0 ]&&[ "$(grep -c "^skip: cannot write.*verify-suite-ts.json" $T/d6k2.out)" = 1 ]&&[ "$(grep -c "^ERROR" $T/d6k2.out)" = 0 ]&&[ "$(grep -c Traceback $T/d6k2.out)" = 0 ]&&[ "$(grep -c "^RESULT:" $T/d6k2.out)" = 1 ]'
echo "verify-v5-uid: $f FAIL"
exit $f
