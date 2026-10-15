#!/bin/sh
# grid-payload-commit.t.sh: goal:g7.33.19.1 + hypothesis g733-grid-commit-of-a-payload-path-versions-the-build-node-that-carries-it-and-an-unowned-path-is-refused-by-name:
# `grid.py commit <payload path>` versions the build node whose payload_ref is that path (node.md + payload, ONE version); an unowned path is refused BY NAME with a non-zero exit and no ref written.
# sh + git + python3 (grid.py is python; no pytest: a v5 uid has none) on a SCRATCH repo: the engine's bin dir is COPIED under the scratch root so grid.py's own repo (its engine root) IS the scratch project, exactly the live one-repo layout. 0 USD, no live ref.
# BIN = the extensions/agi/bin dir under test (default: ROOT's); a mutation / reference = BIN=<an edited copy of that dir>. One ok/FAIL line per case; exit = FAIL count.
T=$(mktemp -d);trap 'rm -rf $T' 0;f=0;G=/usr/bin/git;R0=${ROOT:-$(cd "$(dirname "$0")/../../.." && pwd)};BIN=${BIN:-$R0/extensions/agi/bin}
ok(){ if eval "$2";then echo "ok $1";else echo "FAIL $1";f=$((f+1));fi;}
unset GIT_AUTHOR_NAME GIT_AUTHOR_EMAIL GIT_COMMITTER_NAME GIT_COMMITTER_EMAIL GIT_DIR GIT_WORK_TREE AGI_TRUNK
printf '[user]\n\tname=t\n\temail=t@t\n[commit]\n\tgpgsign=false\n[safe]\n\tdirectory=*\n' >$T/gitconfig;export GIT_CONFIG_GLOBAL=$T/gitconfig GIT_CONFIG_SYSTEM=/dev/null
P=$T/p;mkdir -p $P/.agi/nodes/build $P/extensions/agi;cp -r $BIN $P/extensions/agi/bin;find $P/extensions/agi/bin -name __pycache__ -prune -exec rm -rf {} +
$G init -q $P;echo '{}'>$P/.agi/config.json
printf '#!/bin/sh\necho x1\n'>$P/extensions/x.sh;printf '#!/bin/sh\necho z1\n'>$P/extensions/z.sh;mkdir -p $P/extensions/sub;printf 'echo w1\n'>$P/extensions/sub/w.sh
nd(){ printf -- '---\nid: build:%s\nmint_id: %s\ntype: build\nparents:\n  - idea:y\npayload_ref: %s\n---\nbody %s\n' $1 $2 $3 $1>$P/.agi/nodes/build/$1.md;}
MX=aaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaa;MZ=bbbbbbbbbbbbbbbbbbbbbbbbbbbbbbbb;MW=cccccccccccccccccccccccccccccccc
nd x $MX extensions/x.sh;nd z $MZ extensions/z.sh;nd w $MW extensions/sub/w.sh
$G -C $P add -A;$G -C $P commit -qm fixture
grid(){ (cd $P&&PYTHONDONTWRITEBYTECODE=1 PYTHONPATH=$R0/extensions/agi/src python3 extensions/agi/bin/grid.py "$@");}
n(){ $G -C $P rev-list --count refs/grid/node/$1 2>/dev/null||echo 0;}
nrefs(){ $G -C $P for-each-ref refs/grid|wc -l|tr -d ' ';}
grid init >/dev/null 2>&1;grid commit --all >$T/all.out 2>&1
ok "base-all commit --all versions the three build nodes once each (x $(n $MX), z $(n $MZ), w $(n $MW))" '[ "$(n $MX)" = 1 ]&&[ "$(n $MZ)" = 1 ]&&[ "$(n $MW)" = 1 ]'
ok "base-tree a node version is node.md + its payload in ONE tree (2 entries; the payload blob == the file)" '[ "$($G -C $P ls-tree -r refs/grid/node/$MX|wc -l|tr -d " ")" = 2 ]&&[ "$($G -C $P ls-tree -r refs/grid/node/$MX|awk "{print \$3}"|grep -c "$($G -C $P hash-object $P/extensions/x.sh)")" = 1 ]'
# --- falsifier 1: a payload-only edit, committed BY THE PAYLOAD PATH = v2, same node.md blob, the new payload
echo 'echo x2'>>$P/extensions/x.sh;nb=$($G -C $P rev-parse refs/grid/node/$MX:node.md)
grid commit extensions/x.sh >$T/c1.out 2>$T/c1.err;rc=$?
ok "payload-commit-rc grid.py commit extensions/x.sh exits 0 (rc=$rc)" '[ $rc = 0 ]'
ok "payload-v2 it made version 2 of build:x ($(n $MX))" '[ "$(n $MX)" = 2 ]'
ok "payload-v2-bytes v2 holds the NEW payload and the SAME node.md blob" '[ "$($G -C $P rev-parse refs/grid/node/$MX:node.md)" = "$nb" ]&&$G -C $P ls-tree -r refs/grid/node/$MX|grep -q "$($G -C $P hash-object $P/extensions/x.sh)"'
ok "payload-no-skip the old silent skip is gone: no 'skip (no id)' for the payload path" '! grep -q "skip (no id)" $T/c1.out $T/c1.err'
grid commit extensions/x.sh >/dev/null 2>&1;ok "payload-idempotent the same call twice = no new version ($(n $MX))" '[ "$(n $MX)" = 2 ]'
grid commit .agi/nodes/build/x.md >/dev/null 2>&1;ok "payload-then-node a node-file commit after it = no new version (identical tree) ($(n $MX))" '[ "$(n $MX)" = 2 ]'
# --- a path only ever versions the node that carries it; ONE version per node per commit
echo 'echo z2'>>$P/extensions/z.sh;echo 'echo x3'>>$P/extensions/x.sh;grid commit extensions/x.sh >/dev/null 2>&1
ok "only-its-node committing x's payload leaves z's version alone though z.sh changed (z $(n $MZ), x $(n $MX))" '[ "$(n $MZ)" = 1 ]&&[ "$(n $MX)" = 3 ]'
echo 'echo x4'>>$P/extensions/x.sh;grid commit extensions/x.sh .agi/nodes/build/x.md >/dev/null 2>&1
ok "one-version two paths naming the SAME node (its payload + its node file) make ONE version (x $(n $MX), want 4)" '[ "$(n $MX)" = 4 ]'
echo 'echo w2'>>$P/extensions/sub/w.sh;grid commit extensions/sub/w.sh >/dev/null 2>&1
ok "nested-path a payload in a subdirectory resolves to its node too (w $(n $MW))" '[ "$(n $MW)" = 2 ]'
echo 'echo z3'>>$P/extensions/z.sh;grid commit extensions/x.sh extensions/z.sh >/dev/null 2>&1
ok "two-payloads two payload paths of two nodes version both, once each (x $(n $MX), z $(n $MZ))" '[ "$(n $MX)" = 4 ]&&[ "$(n $MZ)" = 2 ]'
# --- falsifier 2: a path no node carries is refused BY NAME, non-zero, nothing written
before=$(nrefs);heads=$($G -C $P for-each-ref refs/heads refs/tags|md5sum)
printf 'echo q\n'>$P/extensions/nobody.sh;grid commit extensions/nobody.sh >$T/n.out 2>$T/n.err;rc=$?
ok "unowned-refused grid.py commit extensions/nobody.sh exits non-zero (rc=$rc)" '[ $rc != 0 ]'
ok "unowned-by-name the refusal names the path (ERR: no build node carries payload_ref extensions/nobody.sh)" 'cat $T/n.out $T/n.err|grep -q "extensions/nobody.sh"&&cat $T/n.out $T/n.err|grep -qi "no build node carries"'
ok "unowned-no-write the refusal wrote no ref: refs/grid count unchanged ($before -> $(nrefs))" '[ "$(nrefs)" = "$before" ]'
grid commit extensions/gone-and-never-was.sh >/dev/null 2>&1;rc=$?;ok "missing-path a path that does not exist and no node names is refused too (rc=$rc)" '[ $rc != 0 ]'
# a good path BESIDE an unowned one: refused as a whole, so a typo never half-commits
echo 'echo x5'>>$P/extensions/x.sh;b4=$(n $MX);grid commit extensions/x.sh extensions/nobody.sh >/dev/null 2>&1;rc=$?
ok "mixed-all-or-nothing a good payload beside an unowned path exits non-zero and commits NOTHING (rc=$rc, x $b4 -> $(n $MX))" '[ $rc != 0 ]&&[ "$(n $MX)" = "$b4" ]'
# --- invariants: plumbing only (the working tree and every non-grid ref are untouched); --all and a node-file commit behave as before
grid commit extensions/x.sh >/dev/null 2>&1
ok "plumbing-only the working tree is not touched by the payload commit (the edited files are still dirty, nothing staged or reverted)" '[ "$($G -C $P diff --name-only|sort|tr "\n" " ")" = "extensions/sub/w.sh extensions/x.sh extensions/z.sh " ]&&[ -z "$($G -C $P diff --cached --name-only)" ]'
ok "no-ref-outside-grid heads and tags are untouched" '[ "$($G -C $P for-each-ref refs/heads refs/tags|md5sum)" = "$heads" ]'
echo 'echo z4'>>$P/extensions/z.sh;echo 'echo w3'>>$P/extensions/sub/w.sh;grid commit --all >$T/all2.out 2>&1
ok "all-unchanged commit --all still versions every changed payload (z $(n $MZ) want 3, w $(n $MW) want 3) and does not re-version the unchanged x (x $(n $MX) want 5)" '[ "$(n $MZ)" = 3 ]&&[ "$(n $MW)" = 3 ]&&[ "$(n $MX)" = 5 ]'
echo 'node only'>>$P/.agi/nodes/build/z.md;grid commit .agi/nodes/build/z.md >/dev/null 2>&1;ok "node-file-unchanged a node-only edit committed by its node file still makes its own version (z $(n $MZ), want 4)" '[ "$(n $MZ)" = 4 ]'
echo "grid-payload-commit: $f FAIL"
exit $f
