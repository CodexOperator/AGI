#!/bin/sh
# verify-land.t.sh: VL (council 3/3, alive 21:31:33Z 10-25): the land check on a scratch repo signed by a throwaway ssh key. A clean land reads `verify-land: OK` rc 0;
# each hostile land HOLDS that check (tree != merge-tree, an unsigned commit, a D path, a home-path literal, a stray email), the installed copy != the pin's blob
# is `unread`, and PATH not resolving to the installed copy or a live ~/tools copy is RED. No root, no network. One ok/FAIL line per case; exit = number of FAILs.
T=$(mktemp -d);trap 'rm -rf $T' 0;f=0;R0=${ROOT:-$(cd "$(dirname "$0")/../../.." && pwd)};VL=${VL:-$R0/extensions/agi/guard/verify-land.sh}
ok(){ if eval "$2";then echo "ok $1";else echo "FAIL $1";f=$((f+1));fi;}
[ -s "$VL" ]||{ echo "FAIL no verify-land at $VL";exit 99;}
ssh-keygen -q -t ed25519 -N '' -C t@t -f $T/k||exit 99;printf 't@t namespaces="git" %s\n' "$(cut -d' ' -f1,2 $T/k.pub)" >$T/allowed
R=$T/r;git init -q $R;g(){ git -C $R "$@";}
g config user.name t;g config user.email t@t;g config gpg.format ssh;g config user.signingkey $T/k;g config gpg.ssh.allowedSignersFile $T/allowed;g config commit.gpgsign true
mkdir -p $R/extensions/agi/guard $R/docs $R/.agi;echo '{}' >$R/.agi/config.json;cp "$VL" $R/extensions/agi/guard/verify-land.sh;echo a >$R/docs/a;echo keep >$R/docs/keep;g add -A;g commit -qm base;BASE=$(g rev-parse HEAD)
mkdir -p $T/bin;cp "$VL" $T/bin/verify-land;chmod 755 $T/bin/verify-land;printf 'AGI_TRUNK=%s\n' $BASE >$T/carry.env
# gate(NAME, edit...): a gate tip on BASE (signed unless UNSIGNED=1), then the land = merge(BASE, tip) signed, held as NAME
gate(){ n=$1;shift;g checkout -q --detach $BASE;eval "$*";g add -A;if [ -n "$UNSIGNED" ];then g -c commit.gpgsign=false commit -qm "tip $n";else g commit -qm "tip $n";fi;GT=$(g rev-parse HEAD)
 tr=$(g merge-tree --write-tree $BASE $GT|head -1);[ -z "$XTRA" ]||{ g checkout -q --detach $GT;echo x >$R/docs/smuggled;g add -A;tr=$(g write-tree);g reset -q --hard $GT;}
 LD=$(g commit-tree -S -p $BASE -p $GT -m "land $n" $tr);g update-ref refs/heads/vl/$n $LD;g update-ref refs/held/sanctuary-master/$n $LD;}
run(){ env -i PATH=$T/bin:/usr/bin:/bin HOME=$T VL_T=$R VL_MAIN=$R VL_OUT=$T/out VL_ANON=$R0/extensions/agi/bin/anonymize.py VL_CARRY=${CARRY:-$T/carry.env} VL_INSTALLED=$T/bin/verify-land VL_TOOLS=$T/tools/verify-land.sh ${XPATH:+PATH=$XPATH} sh ${SELF:-$T/bin/verify-land} "$@" >$T/o 2>&1;rc=$?;}
v(){ tail -1 $T/o;}
# --- clean
gate c 'echo b >$R/docs/b';run c $LD $BASE $GT
ok "c-a-clean-signed-land-reads-OK rc $rc, $(v)" '[ $rc = 0 ]&&[ "$(v)" = "verify-land: OK" ]'
ok "c-b-the-readings-are-all-printed $(grep -c -E '^(held|parents|tree|sigs|D|anon-diff|anon-msg|home hits|gpu|self)' $T/o) of 10" '[ "$(grep -c -E "^(held|parents|tree|sigs|D|anon-diff|anon-msg|home hits|gpu|self)" $T/o)" = 10 ]'
# --- one hostile land per existing check
XTRA=1 gate t 'echo b >$R/docs/b';run t $LD $BASE $GT
ok "h1-tree-not-merge-tree-HOLDS rc $rc, $(v)" '[ $rc = 1 ]&&v|grep -q "HOLD (.*tree"'
UNSIGNED=1 gate u 'echo b >$R/docs/b';run u $LD $BASE $GT
ok "h2-an-unsigned-commit-HOLDS rc $rc, $(grep ^sigs $T/o), $(v)" '[ $rc = 1 ]&&v|grep -q "HOLD (.*sigs"'
gate d 'git -C $R rm -q docs/keep';run d $LD $BASE $GT
ok "h3-a-D-path-HOLDS rc $rc, $(grep -o '^D: [0-9]*' $T/o), $(v)" '[ $rc = 1 ]&&v|grep -q "HOLD (.*D"'
hm=$(getent passwd "$(id -un)"|cut -d: -f6);gate m 'echo "see $hm/notes" >$R/docs/m';run m $LD $BASE $GT
ok "h4-a-home-path-literal-HOLDS rc $rc, $(grep -c '^home hits \[.\+\]' $T/o) hit line, $(v)" '[ $rc = 1 ]&&v|grep -q "HOLD (.*home"'
gate e 'echo b2 >$R/docs/b2';LE=$(g commit-tree -S -p $BASE -p $GT -m "land e
leak: someone@""example.org" $(g rev-parse $LD^{tree}));g update-ref refs/held/sanctuary-master/e $LE;run e $LE $BASE $GT
ok "h5-a-stray-email-in-the-message-HOLDS rc $rc, $(grep -o 'emails: .*' $T/o), $(v)" '[ $rc = 1 ]&&v|grep -q "HOLD (.*msg-email"'
gate c 'echo b >$R/docs/b';run WRONG $LD $BASE $GT
ok "h6-a-held-ref-that-is-not-the-land-HOLDS rc $rc, $(v)" '[ $rc = 1 ]&&v|grep -q "HOLD (held"'
# --- self: installed == the pin's blob, PATH, the retired ~/tools copy
gate c 'echo b >$R/docs/b';echo '# drift' >>$T/bin/verify-land;run c $LD $BASE $GT;cp "$VL" $T/bin/verify-land
ok "s1-an-installed-copy-that-is-not-the-pin-blob-is-unread rc $rc, $(grep -o 'verify-land: unread.*' $T/o|cut -c1-40), $(v)" '[ $rc = 1 ]&&grep -q "verify-land: unread (installed != repo" $T/o&&v|grep -q "HOLD (.*self"'
mkdir -p $T/tools;cp "$VL" $T/tools/verify-land;chmod 755 $T/tools/verify-land;XPATH=$T/tools:$T/bin:/usr/bin:/bin;run c $LD $BASE $GT;XPATH=
ok "s2-PATH-resolving-to-another-copy-is-RED rc $rc, $(v)" '[ $rc = 1 ]&&grep -q "RED PATH resolves" $T/o&&v|grep -q "HOLD (.*path"'
cp "$VL" $T/tools/verify-land.sh;run c $LD $BASE $GT;rm -f $T/tools/verify-land.sh
ok "s3-a-live-tools-copy-is-RED rc $rc, $(v)" '[ $rc = 1 ]&&grep -q "RED the box-local copy" $T/o&&v|grep -q "HOLD (.*tools-copy"'
rm -rf $T/tools;run c $LD $BASE $GT
ok "s4-and-clean-again rc $rc, $(v)" '[ $rc = 0 ]'
echo "verify-land: $f FAIL";exit $f
