#!/bin/sh
# cred-piece.t.sh: goal:g7.16.1.11.46.20 (V2) falsifier 2: the `cred` / `slot` cells of config:posts. A row naming another login while it runs in the director's slot is refused BY NAME;
# an owner-facing row never takes a login of its own; a bad cell and an unreadable input are refused, never passed. sh + python3 (credpiece.py) on a SCRATCH posts.md; no network, no root, 0 USD.
# One ok/FAIL line per case; exit = number of FAILs. ROOT=<tree> (default: the tree this file sits in). A mutant is ONE edit of a scratch copy of the check; the same refusal row must then FAIL.
T=$(mktemp -d);trap 'rm -rf $T' 0;f=0;R0=${ROOT:-$(cd "$(dirname "$0")/../../.." && pwd)};CP=$R0/extensions/agi/bin/credpiece.py;N=$R0/.agi/nodes/.geometry/posts.md
[ -f $CP ]&&[ -f $N ]||{ echo "FAIL inputs: $CP $N";exit 99;}
ok(){ if eval "$2";then echo "ok $1";else echo "FAIL $1";f=$((f+1));fi;}
C1=0123456789abcdef0123456789abcdef
row(){ printf '%s\n' "  - $1";}
chk(){ python3 $CP $1 >$T/o 2>$T/e;rc=$?;}
posts(){ { printf -- '---\nid: config:posts\nposts:\n';cat;} >$T/p.md;}
# --- the real node reads clean
chk $N
ok "cred-a-the-real-posts-node-passes rc $rc: $(cat $T/o|cut -c1-60)" '[ $rc = 0 ]&&grep -q "^\[cred\] ok: [0-9]* rows" $T/o'
# --- clean shapes
row '{"name": "kid-a", "cred": "'$C1'", "slot": "own"}'|posts;chk $T/p.md
ok "cred-b-another-login-in-its-own-slot-passes rc $rc" '[ $rc = 0 ]'
row '{"name": "kid-b", "cred": "inherit", "slot": "inherit"}'|posts;chk $T/p.md
ok "cred-b-the-directors-login-in-the-directors-slot-passes rc $rc" '[ $rc = 0 ]'
row '{"name": "kid-c"}'|posts;chk $T/p.md
ok "cred-b-a-row-with-neither-cell-passes rc $rc" '[ $rc = 0 ]'
# --- refusals, each names the row and the cell, rc 1
BAD='{"name": "kid-d", "cred": "'$C1'", "slot": "inherit"}'
row "$BAD"|posts;chk $T/p.md
ok "cred-c-another-login-with-slot-inherit-is-refused-by-name rc $rc: $(sed -n 1p $T/e|cut -c1-90)" '[ $rc = 1 ]&&grep -q "kid-d: .cred. names another login but .slot. is inherit" $T/e'
row '{"name": "owner-seat", "faces": "owner", "cred": "'$C1'", "slot": "own"}'|posts;chk $T/p.md
ok "cred-c-an-owner-facing-row-with-its-own-login-is-refused rc $rc: $(sed -n 1p $T/e|cut -c1-90)" '[ $rc = 1 ]&&grep -q "owner-seat: an owner-facing row keeps the login" $T/e'
K=sk-an;K=${K}t-oat01-CANARYCANARYCANARY
row '{"name": "kid-e", "cred": "'$K'", "slot": "own"}'|posts;chk $T/p.md
ok "cred-c-a-token-shaped-cred-is-refused-and-never-printed rc $rc canary lines: $(cat $T/o $T/e|grep -c CANARY) (want 0)" '[ $rc = 1 ]&&grep -q "kid-e: .cred. is not inherit or a 32-hex" $T/e&&[ "$(cat $T/o $T/e|grep -c CANARY)" = 0 ]'
row '{"name": "kid-f", "cred": "inherit", "slot": "root"}'|posts;chk $T/p.md
ok "cred-c-a-bad-slot-is-refused rc $rc" '[ $rc = 1 ]&&grep -q "kid-f: .slot. is not own or inherit" $T/e'
# --- unreadable: never rc 0
chk $T/nope.md
ok "cred-d-a-missing-file-prints-unread-rc-1 rc $rc: $(cat $T/e|cut -c1-60)" '[ $rc = 1 ]&&grep -q "unread" $T/e'
printf -- '---\nid: config:posts\nposts:\n'>$T/p.md;chk $T/p.md
ok "cred-d-a-node-with-no-rows-prints-unread-rc-1 rc $rc" '[ $rc = 1 ]&&grep -q "unread" $T/e'
# --- R1 (regression guard, not a claim that a secret is read): --help prints and exits 0 BEFORE any input is touched. aud.py runs the script under an audit hook that counts opens of ONE path;
# the path is the one a reader would take for argv[1] (a file named --help in the cwd), so a script that reads its input first is seen.
cat >$T/aud.py <<'P'
import runpy, sys
t = sys.argv[1]; hits = []
sys.addaudithook(lambda e, a: hits.append(1) if e == "open" and a and str(a[0]) == t else None)
sys.argv = sys.argv[2:]; rc = 0
try:
    runpy.run_path(sys.argv[0], run_name="__main__")
except SystemExit as x:
    rc = x.code or 0
print(len(hits)); sys.exit(rc)
P
r1(){ (cd $T;python3 $T/aud.py "$T/--help" $1 --help >$T/o 2>$T/e);r1rc=$?;r1n=$(tail -1 $T/o);}
r1 $CP
ok "cred-f-R1-help-rc-0-usage-and-0-opens-of-the-input rc $r1rc opens $r1n" '[ $r1rc = 0 ]&&[ "$r1n" = 0 ]&&grep -q "^usage: credpiece.py" $T/o'
# --- R2: the id is checked for FORMAT only and the ok line says so, counting the ids it did not resolve
row '{"name": "kid-a", "cred": "'$C1'", "slot": "own"}'|posts;chk $T/p.md
ok "cred-g-R2-the-ok-line-says-format-only-1-id-not-resolved: $(cut -c1-120 $T/o|sed "s|$T|\$T|")" '[ $rc = 0 ]&&grep -q "(format only: 1 capsule ids not resolved)" $T/o'
chk $N
ok "cred-g-R2-the-real-node-says-format-only-0-ids: $(sed 's|.* rows in .*(|(|' $T/o)" '[ $rc = 0 ]&&grep -q "(format only: 0 capsule ids not resolved)" $T/o'
# --- R3: the default input is a RELATIVE path; every result line names the ABSOLUTE path it read, so a stale worktree is visible
mkdir -p $T/stale/.agi/nodes/.geometry;cp $N $T/stale/.agi/nodes/.geometry/posts.md
r3(){ (cd $T/stale;python3 $1 >$T/o 2>$T/e);r3rc=$?;}
r3 $CP
ok "cred-h-R3-the-default-input-line-names-the-absolute-path-it-read rc $r3rc" '[ $r3rc = 0 ]&&grep -q " rows in $T/stale/.agi/nodes/.geometry/posts.md (" $T/o'
(cd $T/stale;python3 $CP $T/nope.md >$T/o 2>$T/e);
ok "cred-h-R3-an-unread-line-names-the-absolute-path rc $?" 'grep -q "unread: $T/nope.md" $T/e'
# --- MUTANTS: one edit of the check; the refusal rows above must then not hold (the row below passes only when the mutant is caught)
mutant(){ # name, old, new, then the posts row to feed and the grep that proves the refusal
 python3 - "$CP" "$T/mut.py" "$2" "$3" <<'P'
import sys
s=open(sys.argv[1]).read();assert sys.argv[3] in s,'mutant target absent';open(sys.argv[2],'w').write(s.replace(sys.argv[3],sys.argv[4],1))
P
 [ $? = 0 ]||{ echo "FAIL mutant $1: target absent";f=$((f+1));return;}
 row "$4"|posts;python3 $T/mut.py $T/p.md >$T/o 2>$T/e;mrc=$?
 ok "cred-e-MUTANT-$1-reads-RED (the refusal is gone: rc $mrc, refusal line present $(grep -c "$5" $T/e))" '! { [ $mrc = 1 ]&&grep -q "$5" $T/e;}'
}
mutant check-removed 'if cred != "inherit" and slot == "inherit":' 'if False:' "$BAD" 'names another login'
mutant owner-rule-removed 'row.get("faces") == "owner"' 'False' '{"name": "owner-seat", "faces": "owner", "cred": "'$C1'", "slot": "own"}' 'owner-facing'
mutant cid-shape-loosened '_CID = re.compile(r"[0-9a-f]{32}")' '_CID = re.compile(r".+")' '{"name": "kid-e", "cred": "'$K'", "slot": "own"}' '32-hex'
# the R-row mutants: ONE edit of the script, then the row's own assertion must not hold
mscript(){ python3 - "$CP" "$T/mut.py" "$1" "$2" <<'P'
import sys
s=open(sys.argv[1]).read();assert sys.argv[3] in s,'mutant target absent';open(sys.argv[2],'w').write(s.replace(sys.argv[3],sys.argv[4],1))
P
}
mscript 'if len(argv) > 1 and argv[1] in ("-h", "--help"):' 'if len(argv) > 1 and argv[1] in ("-h", "--help") and Path(argv[1]).exists():'||{ echo "FAIL mutant R1: target absent";f=$((f+1));}
r1 $T/mut.py
ok "cred-i-MUTANT-R1-input-read-before-help-reads-RED (rc $r1rc opens $r1n)" '! { [ $r1rc = 0 ]&&[ "$r1n" = 0 ];}'
mscript '(format only: {ids} capsule ids not resolved)' '(ok)'||{ echo "FAIL mutant R2: target absent";f=$((f+1));}
row '{"name": "kid-a", "cred": "'$C1'", "slot": "own"}'|posts;python3 $T/mut.py $T/p.md >$T/o 2>$T/e
ok "cred-i-MUTANT-R2-ok-line-without-the-format-only-wording-reads-RED" '! grep -q "(format only: 1 capsule ids not resolved)" $T/o'
mscript '.resolve()' ''||{ echo "FAIL mutant R3: target absent";f=$((f+1));}
r3 $T/mut.py
ok "cred-i-MUTANT-R3-a-relative-path-line-reads-RED (line: $(cut -c1-80 $T/o))" '! grep -q " rows in $T/stale/.agi/nodes/.geometry/posts.md (" $T/o'
# r3 (the census, sp's condition): the two helpers' guards are RUN rows -- a target that is absent fails closed with its name; with the guard dropped the mutant is an unmutated copy and its own row reads RED
x=$(f=0;mutant selftest 'NO-SUCH-LITERAL-XYZ' q "$BAD" 'names another login' 2>/dev/null;echo "f=$f")
ok "cred-r3-mutant-an-absent-target-fails-closed-and-names-itself: $(echo "$x"|tr '\n' '|'|cut -c1-110)" 'echo "$x"|grep -q "^FAIL mutant selftest: target absent"&&echo "$x"|grep -qx "f=1"&&! echo "$x"|grep -q "^ok \|^FAIL cred-e-MUTANT"'
mscript 'NO-SUCH-LITERAL-XYZ' q >/dev/null 2>&1;m3rc=$?
ok "cred-r3-mscript-an-absent-target-exits-non-zero (rc $m3rc)" '[ $m3rc != 0 ]'
python3 - "$CP" "$T/mut.py" 'NO-SUCH-LITERAL-XYZ' q <<'P'
import sys
s=open(sys.argv[1]).read();open(sys.argv[2],'w').write(s.replace(sys.argv[3],sys.argv[4],1))
P
row "$BAD"|posts;python3 $T/mut.py $T/p.md >$T/o 2>$T/e;m3=$?
ok "cred-r3-mutant-the-assert-dropped-leaves-an-unmutated-copy-whose-own-row-reads-RED (rc $m3, the refusal is still there: $(grep -c 'names another login' $T/e))" '[ $m3 = 1 ]&&grep -q "names another login" $T/e'
echo "cred-piece: $f FAIL";exit $f
