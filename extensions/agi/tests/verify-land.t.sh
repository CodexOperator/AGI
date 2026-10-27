#!/bin/sh
# verify-land.t.sh: VL (council 3/3, alive 21:31:33Z 10-25): the land check on a scratch repo signed by a throwaway ssh key. A clean land reads `verify-land: OK` rc 0;
# each hostile land HOLDS that check (tree != merge-tree, an unsigned commit, a D path, a home-path literal, a stray email, BASE's r-land refusing), the installed copy != the pin's blob
# is `unread`, and PATH not resolving to the installed copy or a live ~/tools copy is RED. No root, no network. One ok/FAIL line per case; exit = number of FAILs.
export GIT_CONFIG_GLOBAL=/dev/null GIT_CONFIG_NOSYSTEM=1   # C4: hermetic (a uid's global ref-guard refuses the scratch refs/held/* writes)
T=$(mktemp -d);trap 'rm -rf $T' 0;f=0;R0=${ROOT:-$(cd "$(dirname "$0")/../../.." && pwd)};VL=${VL:-$R0/extensions/agi/guard/verify-land.sh}
ok(){ if eval "$2";then echo "ok $1";else echo "FAIL $1";f=$((f+1));fi;}
[ -s "$VL" ]||{ echo "FAIL no verify-land at $VL";exit 99;}
ssh-keygen -q -t ed25519 -N '' -C t@t -f $T/k||exit 99;printf 't@t namespaces="git" %s\n' "$(cut -d' ' -f1,2 $T/k.pub)" >$T/allowed
CA="Co-Authored-By: Claude Opus 5.5 <noreply@""anthropic.com>"   # every land message carries the real co-author trailer (C4)
R=$T/r;git init -q $R;g(){ git -C $R "$@";}
g config user.name t;g config user.email t@t;g config gpg.format ssh;g config user.signingkey $T/k;g config gpg.ssh.allowedSignersFile $T/allowed;g config commit.gpgsign true
mkdir -p $R/extensions/agi/guard $R/docs $R/.agi;echo '{"land": {"rules_paths": [".agi/context/schemas/", ".agi/nodes/.geometry/", ".github/", ":(glob).gitattributes", ":(glob)**/.gitattributes", "skills/agi-master-gate/", ".agi/config.json", "extensions/agi/guard/", "CLAUDE.md", "AGENTS.md", "QUICKSTART.md"]}, "anonymize": {"fixture_homes": ["fxuser"]}}' >$R/.agi/config.json;   # the live seed (council 06:06:56Z L2)
cp "$VL" $R/extensions/agi/guard/verify-land.sh;echo a >$R/docs/a;echo keep >$R/docs/keep;g add -A;g commit -qm base;BASE=$(g rev-parse HEAD)
# SINCE = the lane's L140: BASE + a judge stub; every pre-existing fixture base is a SIBLING (does not descend it: the fail-open reading)
g checkout -q --detach $BASE;printf '%s\n' '#!/bin/sh' 'echo "R-land: judged by SINCE $1..$2";exit 0' >$R/extensions/agi/guard/r-land;g add -A;g commit -qm since;SINCE=$(g rev-parse HEAD);g checkout -q --detach $BASE
mkdir -p $T/bin;cp "$VL" $T/bin/verify-land;chmod 755 $T/bin/verify-land
# the stub agi-mem: logs its argv and the AGI_ENGINE tree's OWNER files, exits $STUB_CITE_RC (the lane tests the WIRING; agi-mem cite has its own lane, owner-cite.t.sh)
printf '%s\n' '#!/bin/sh' 'echo "$* engine-owner-files=$(grep -rl "^## OWNER" "$AGI_ENGINE/.agi/nodes" 2>/dev/null|wc -l)" >>$STUB_LOG/cite.log' 'echo "owner-cite: stub rc ${STUB_CITE_RC:-0}"' 'exit ${STUB_CITE_RC:-0}' >$T/bin/agi-mem;chmod 755 $T/bin/agi-mem
printf 'AGI_TRUNK=%s\n' $BASE >$T/carry.env
# gate(NAME, edit...): a gate tip on BASE (signed unless UNSIGNED=1), then the land = merge(BASE, tip) signed, held as NAME
gate(){ n=$1;shift;g checkout -q --detach $BASE;eval "$*";g add -A;if [ -n "$UNSIGNED" ];then g -c commit.gpgsign=false commit -qm "tip $n";else g commit -qm "tip $n";fi;GT=$(g rev-parse HEAD)
 tr=$(g merge-tree --write-tree $BASE $GT|head -1);[ -z "$XTRA" ]||{ g checkout -q --detach $GT;echo x >$R/docs/smuggled;g add -A;tr=$(g write-tree);g reset -q --hard $GT;}
 LD=$(g commit-tree -S -p $BASE -p $GT -m "land $n${MSG:+
$MSG}" -m "$CA" $tr);g update-ref refs/heads/vl/$n $LD;g update-ref refs/held/sanctuary-master/$n $LD;}
run(){ env -i PATH=$T/bin:/usr/bin:/bin HOME=$T VL_T=$R VL_MAIN=$R VL_OUT=$T/out VL_ANON=$R0/extensions/agi/bin/anonymize.py VL_CARRY=${CARRY:-$T/carry.env} VL_INSTALLED=$T/bin/verify-land VL_TOOLS=$T/tools/verify-land.sh VL_RING=$T/allowed VL_RLAND_SINCE=${RSX:-$SINCE} VL_WRAP_SIGNER=${WSIG:-t@t} VL_LAND_SIGNER=t@t ${AGI_FIX:+AGI_ANONYMIZE_FIXTURE=$AGI_FIX} ${XLIT:+GIT_LITERAL_PATHSPECS=1} ${XTMP:+TMPDIR=$XTMP} ${VPW:+VL_PASSWD=$VPW} STUB_LOG=$T STUB_CITE_RC=${CRC:-0} ${XPATH:+PATH=$XPATH} sh ${SELF:-$T/bin/verify-land} "$@" >$T/o 2>&1;rc=$?;}
v(){ tail -1 $T/o;}
# wrun(NAME, LAND, BASE, GT): the WRAP step (`verify-land wrap`) then verify-land on what it printed: WS = the wrap sha (empty = plain)
wrun(){ run wrap "$@";cp $T/o $T/w;WS=$(sed -n 's/^land: wrap \([0-9a-f]*\) over .*/\1/p' $T/w);n=$1;shift;run $n ${WS:-$1} "$2" "$3";}
# --- clean
gate c 'echo b >$R/docs/b';run c $LD $BASE $GT
ok "c-a-clean-signed-land-with-a-real-co-author-trailer-reads-OK rc $rc, $(grep -o '^anon-msg=[0-9]*' $T/o), trailer lines $(git -C $R log -1 --format=%B $LD|grep -c '^Co-Authored-By: Claude'), $(v)" '[ $rc = 0 ]&&[ "$(v)" = "verify-land: OK" ]&&[ "$(git -C $R log -1 --format=%B $LD|grep -c "^Co-Authored-By: Claude")" = 1 ]'
ok "c-b-the-readings-are-all-printed $(grep -c -E '^(held|parents|tree|sigs|D|anon-diff|anon-msg|home hits|gpu|cite|r-land|ran as|self)' $T/o) of 13, cite n/a: $(grep -c '^cite: n/a' $T/o), r-land none: $(grep -c '^r-land: none at BASE' $T/o)" '[ "$(grep -c -E "^(held|parents|tree|sigs|D|anon-diff|anon-msg|home hits|gpu|cite|r-land|ran as|self)" $T/o)" = 13 ]&&grep -q "^cite: n/a" $T/o&&[ ! -s $T/cite.log ]&&grep -q "^r-land: none at BASE .* (a pre-L140 BASE: fail open, as the hook)" $T/o'
ok "c-c-ran-as-names-the-uid-it-ran-as (M2) $(grep '^ran as:' $T/o)" 'grep -qx "ran as: $(id -un) uid $(id -u)" $T/o'
# --- one hostile land per existing check
XTRA=1 gate t 'echo b >$R/docs/b';run t $LD $BASE $GT
ok "h1-tree-not-merge-tree-HOLDS rc $rc, $(v)" '[ $rc = 1 ]&&v|grep -q "HOLD (.*tree"'
UNSIGNED=1 gate u 'echo b >$R/docs/b';run u $LD $BASE $GT
ok "h2-an-unsigned-commit-HOLDS rc $rc, $(grep ^sigs $T/o), $(v)" '[ $rc = 1 ]&&v|grep -q "HOLD (.*sigs"'
gate d 'git -C $R rm -q docs/keep';run d $LD $BASE $GT
ok "h3-a-D-path-HOLDS rc $rc, $(grep -o '^D: [0-9]*' $T/o), $(v)" '[ $rc = 1 ]&&v|grep -q "HOLD (.*D"'
# --- goal:g7.16.1.11.46.23.1 (council (c) 09:55:09Z 10-26): a D is admitted ONLY by exact path from BASE's land.deletes_admitted; -M pinned; a node D never
# dab(NAME, JSON-cell): a base = BASE + .agi/nodes/doc/n.md + docs/x/y + the cell in .agi/config.json (rules_paths kept); DA = its sha, its own carry file
dab(){ g checkout -q --detach $BASE;mkdir -p $R/.agi/nodes/doc $R/docs/x;echo n >$R/.agi/nodes/doc/n.md;echo y >$R/docs/x/y
 python3 -I -c 'import json,sys;p=sys.argv[1];c=json.load(open(p));c["land"]["deletes_admitted"]=json.loads(sys.argv[2]);open(p,"w").write(json.dumps(c))' $R/.agi/config.json "$2"
 g add -A;g commit -qm "base $1";DA=$(g rev-parse HEAD);printf 'AGI_TRUNK=%s\n' $DA >$T/carry-$1.env;}
B0=$BASE;dab k '[{"path":"docs/keep","ruling":"owner r1"}]';BASE=$DA;gate dk 'git -C $R rm -q docs/keep';BASE=$B0;CARRY=$T/carry-k.env;run dk $LD $DA $GT;CARRY=
ok "da1-a-listed-code-D-at-BASE-reads-OK rc $rc, $(grep '^D admitted' $T/o), $(v)" '[ $rc = 0 ]&&grep -qx "D admitted: docs/keep (owner r1)" $T/o&&[ "$(v)" = "verify-land: OK" ]'
gate dt 'git -C $R rm -q docs/keep;python3 -I -c "import json;p=\"$R/.agi/config.json\";c=json.load(open(p));c[\"land\"][\"deletes_admitted\"]=[{\"path\":\"docs/keep\",\"ruling\":\"self\"}];open(p,\"w\").write(json.dumps(c))"';wrun dt $LD $BASE $GT
ok "da2-a-TIP-listing-its-own-delete-HOLDS (the cell is read from BASE) rc $rc, $(grep '^D not admitted' $T/o), $(v)" '[ $rc = 1 ]&&grep -qx "D not admitted: docs/keep" $T/o&&v|grep -q "HOLD (.*D"'
BASE=$DA;gate du 'git -C $R rm -q docs/a';BASE=$B0;CARRY=$T/carry-k.env;run du $LD $DA $GT;CARRY=
ok "da3-an-unlisted-D-HOLDS-and-the-stale-entry-is-read rc $rc, $(grep -c -E '^(D not admitted: docs/a|admitted but not deleted: docs/keep)$' $T/o) of 2, $(v)" '[ $rc = 1 ]&&grep -qx "D not admitted: docs/a" $T/o&&grep -qx "admitted but not deleted: docs/keep" $T/o&&v|grep -q "HOLD (.*D"'
dab dir '[{"path":"docs/x/","ruling":"r2"},{"path":"docs/x","ruling":"r3"}]';BASE=$DA;gate dd 'git -C $R rm -q docs/x/y';BASE=$B0;CARRY=$T/carry-dir.env;run dd $LD $DA $GT;CARRY=
ok "da4-a-listed-path-never-covers-another-deleted-path (docs/x/ and docs/x listed, docs/x/y deleted) rc $rc, $(grep '^D not admitted' $T/o), $(v)" '[ $rc = 1 ]&&grep -qx "D not admitted: docs/x/y" $T/o&&v|grep -q "HOLD (.*D"'
gate dr 'git -C $R mv docs/keep docs/kept';g config diff.renames false;run dr $LD $BASE $GT;g config --unset diff.renames
ok "da5-renames-pinned: diff.renames=false reads the SAME D set as the default (a pure rename = D 0) rc $rc, $(grep -o '^D: [0-9]*' $T/o), $(v)" '[ $rc = 0 ]&&grep -q "^D: 0 " $T/o&&[ "$(v)" = "verify-land: OK" ]'
dab node '[{"path":".agi/nodes/doc/n.md","ruling":"r4"}]';BASE=$DA;gate dn 'git -C $R rm -q .agi/nodes/doc/n.md';BASE=$B0;CARRY=$T/carry-node.env;run dn $LD $DA $GT;CARRY=
ok "da6-a-listed-node-D-HOLDS rc $rc, $(grep '^D not admitted' $T/o), $(v)" '[ $rc = 1 ]&&grep -qx "D not admitted: .agi/nodes/doc/n.md (a node: retire, never delete)" $T/o&&v|grep -q "HOLD (.*D"'
dab bad '"docs/keep"';BASE=$DA;gate db 'git -C $R rm -q docs/keep';BASE=$B0;CARRY=$T/carry-bad.env;run db $LD $DA $GT;CARRY=
ok "da7-a-malformed-cell-admits-nothing-and-says-so rc $rc, $(grep '^deletes_admitted unread' $T/o|cut -c1-40), $(v)" '[ $rc = 1 ]&&grep -q "^deletes_admitted unread at BASE" $T/o&&grep -qx "D not admitted: docs/keep" $T/o&&v|grep -q "HOLD (.*D"'
ok "da8-no-D-reading-diff-without--M (falsifier 2) $(grep -c 'name-status' $VL) name-status line(s), $(grep 'name-status' $VL|grep -vc -- '-M --name-status') without -M" '[ "$(grep "name-status" $VL|grep -vc -- "-M --name-status")" = 0 ]&&grep -q -- "-M --name-status" $VL'
hm=$(getent passwd "$(id -un)"|cut -d: -f6);gate m 'echo "see $hm/notes" >$R/docs/m';run m $LD $BASE $GT
ok "h4-a-home-path-literal-HOLDS rc $rc, $(grep -c '^home hits \[.\+\]' $T/o) hit line, $(v)" '[ $rc = 1 ]&&v|grep -q "HOLD (.*home"'
gate e 'echo b2 >$R/docs/b2';LE=$(g commit-tree -S -p $BASE -p $GT -m "land e
leak: someone@""example.org" $(g rev-parse $LD^{tree}));g update-ref refs/held/sanctuary-master/e $LE;run e $LE $BASE $GT
ok "h5-a-stray-email-in-the-message-HOLDS rc $rc, $(grep -o 'emails: .*' $T/o), $(v)" '[ $rc = 1 ]&&v|grep -q "HOLD (.*msg-email"'
MSG="ran on $(hostname) at $(hostname -I 2>/dev/null|awk '{print $1}')" gate i 'echo b3 >$R/docs/b3';run i $LD $BASE $GT
ok "h7-a-hostname-and-ip-in-the-land-message-HOLDS rc $rc, $(grep -o '^anon-msg=[0-9]*' $T/o), $(v)" '[ $rc = 1 ]&&v|grep -q "HOLD (anon-msg)"'
ip=$(hostname -I 2>/dev/null|awk '{print $1}');CA0=$CA;CA="Co-Authored-By: Claude Opus $ip <noreply@""anthropic.com>" gate j 'echo b4 >$R/docs/b4';CA=$CA0;run j $LD $BASE $GT
ok "h8-an-ip-inside-the-co-author-trailer-is-NOT-stripped-and-HOLDS rc $rc, $(grep -o '^anon-msg=[0-9]*' $T/o), $(v)" '[ $rc = 1 ]&&v|grep -q "HOLD (anon-msg)"'
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
# --- cite (M10 row b): an OWNER file in the land -> agi-mem cite on the LAND tree; its rc decides
own='mkdir -p $R/.agi/nodes/idea;printf "## OWNER 2026-10-25\\nthe ask\\n\\n## Idea\\nx\\n" >$R/.agi/nodes/idea/zz.md'
: >$T/cite.log;gate o "$own";CRC=1;run o $LD $BASE $GT;CRC=
ok "b1-a-new-OWNER-file-runs-cite-on-the-land-tree-and-a-violation-HOLDS rc $rc, called: $(cat $T/cite.log), $(v)" '[ $rc = 1 ]&&grep -qx "cite engine-owner-files=1" $T/cite.log&&v|grep -q "HOLD (cite)"'
: >$T/cite.log;gate o "$own";run o $LD $BASE $GT
ok "b2-the-same-land-with-cite-rc0-is-OK rc $rc, $(grep '^cite=' $T/o), $(v)" '[ $rc = 0 ]&&grep -q "^cite=0 (1 OWNER file(s))" $T/o'
g checkout -q --detach $BASE;eval "$own";g add -A;g commit -qm "base2 with an OWNER block";B2=$(g rev-parse HEAD);printf 'AGI_TRUNK=%s\n' $B2 >$T/carry2.env
g checkout -q --detach $B2;printf "## OWNER 2026-10-25\nthe ask, edited (no id now)\n\n## Idea\nx\n" >$R/.agi/nodes/idea/zz.md;g add -A;g commit -qm "tip body";GT=$(g rev-parse HEAD)
LD=$(g commit-tree -S -p $B2 -p $GT -m "land body" $(g merge-tree --write-tree $B2 $GT|head -1));g update-ref refs/held/sanctuary-master/bd $LD
: >$T/cite.log;CRC=1;CARRY=$T/carry2.env;run bd $LD $B2 $GT;CRC=;CARRY=
ok "b3-a-BODY-edit-in-an-OWNER-block-runs-cite-too (no heading changed) rc $rc, called: $(wc -l <$T/cite.log), $(v)" '[ $rc = 1 ]&&[ -s $T/cite.log ]&&v|grep -q "HOLD (cite)"'
# --- r-land (R4 site 2, council 02:11:54Z 10-26): BASE's guard/r-land blob runs on BASE..LAND with VL_RING; its rc decides, a report line is a reading
# rlb(NAME, body): a base = BASE + a stub r-land, pinned in carry-NAME.env (the self check reads the pin's verify-land blob, unchanged)
rlb(){ g checkout -q --detach $BASE;printf '%s\n' '#!/bin/sh' "$2" >$R/extensions/agi/guard/r-land;g add -A;g commit -qm "base rl $1";RB=$(g rev-parse HEAD);printf 'AGI_TRUNK=%s\n' $RB >$T/carry-$1.env;}
B0=$BASE;rlb no 'echo "R-land: refused $2 (stub)";exit 1';BASE=$RB;gate rn 'echo r >$R/docs/r';BASE=$B0;CARRY=$T/carry-no.env;run rn $LD $RB $GT;CARRY=
ok "r1-a-refusing-r-land-at-BASE-HOLDS rc $rc, $(grep -c '^R-land: refused' $T/o) refused line, $(grep '^r-land=' $T/o), $(v)" '[ $rc = 1 ]&&grep -q "^R-land: refused $LD (stub)" $T/o&&grep -qx "r-land=1" $T/o&&v|grep -q "HOLD (r-land)"'
rlb rp 'echo "R-land: would refuse $2 (stub, report)";echo "ring=$AGI_RING args=$1 $2";exit 0';BASE=$RB;gate rp 'echo r >$R/docs/r';BASE=$B0;CARRY=$T/carry-rp.env;run rp $LD $RB $GT;CARRY=
ok "r2-a-report-line-at-rc-0-is-a-reading-and-the-land-is-OK rc $rc, $(grep -c '^R-land: would refuse' $T/o) would-refuse line, $(v)" '[ $rc = 0 ]&&grep -q "^R-land: would refuse $LD (stub, report)" $T/o&&grep -qx "r-land=0" $T/o&&[ "$(v)" = "verify-land: OK" ]'
ok "r3-the-call-is-BASE-dot-dot-LAND-with-the-VL_RING-ring $(grep '^ring=' $T/o|sed "s#$T#T#")" 'grep -qx "ring=$T/allowed args=$RB $LD" $T/o'
rlb rs 'echo "R-land: refused $2 (stub, base)";exit 1';BASE=$RB;gate rs 'printf "%s\n" "#!/bin/sh" "echo R-land: ok softened;exit 0" >$R/extensions/agi/guard/r-land';BASE=$B0;CARRY=$T/carry-rs.env;wrun rs $LD $RB $GT;CARRY=
ok "r4-a-tip-that-rewrites-r-land-never-softens-its-own-judge (BASE's blob runs) rc $rc, $(grep -c 'softened' $T/o) softened line, $(v)" '[ -n "$WS" ]&&[ $rc = 1 ]&&! grep -q softened $T/o&&v|grep -q "HOLD (r-land)"'
# --- GATE272 (council 03:49-03:5xZ 10-26): V1 tmpfile, V3 an unresolvable BASE, V2' a deleted / emptied judge -> the LAST non-empty one, never none
gate c 'echo b >$R/docs/b';XTMP=$T/no-such-dir;run c $LD $BASE $GT;XTMP=
ok "v1-an-unwritable-TMPDIR-HOLDS-never-the-fail-open-line rc $rc, $(grep '^r-land' $T/o), $(v)" '[ $rc = 1 ]&&grep -qx "r-land: unread (tmpfile)" $T/o&&! grep -q "fail open" $T/o&&v|grep -q "HOLD (.*r-land"'
run c $LD deadbeef00deadbeef00deadbeef00deadbeef00 $GT
ok "v3-an-unresolvable-BASE-HOLDS rc $rc, $(grep '^r-land' $T/o), $(v)" '[ $rc = 1 ]&&grep -q "^r-land: unread (BASE deadbeef00)" $T/o&&! grep -q "fail open" $T/o&&v|grep -q "HOLD (.*r-land"'
# a deleting land on SINCE (judged by SINCE's own blob), then the restoring land on the deletion (judged by SINCE's blob, NOT held, never its own)
g checkout -q --detach $SINCE;g rm -q extensions/agi/guard/r-land;g commit -qm "del judge";DEL=$(g rev-parse HEAD);printf 'AGI_TRUNK=%s\n' $DEL >$T/carry-del.env
B0=$BASE;BASE=$SINCE;gate dl 'git -C $R rm -q extensions/agi/guard/r-land';BASE=$B0;printf 'AGI_TRUNK=%s\n' $SINCE >$T/carry-since.env;CARRY=$T/carry-since.env;wrun dl $LD $SINCE $GT;CARRY=
ok "v2-a-the-deleting-land-is-judged-by-the-pre-deletion-blob (its own HOLD is D, not r-land) $(grep -c 'judged by SINCE' $T/o) SINCE line, $(grep '^r-land=' $T/o), $(v)" '[ -n "$WS" ]&&grep -q "^R-land: judged by SINCE $SINCE..$WS" $T/o&&grep -qx "r-land=0" $T/o&&v|grep -q "HOLD (D)"'
BASE=$DEL;gate rr 'printf "%s\n" "#!/bin/sh" "echo R-land: own judge;exit 0" >$R/extensions/agi/guard/r-land';BASE=$B0;CARRY=$T/carry-del.env;wrun rr $LD $DEL $GT;CARRY=
ok "v2-b-the-restoring-land-runs-the-LAST-judge-and-is-NOT-held rc $rc, $(grep '^r-land: judge from' $T/o), $(v)" '[ $rc = 0 ]&&grep -qx "r-land: judge from $(echo $SINCE|cut -c1-10) (deleted at $(echo $DEL|cut -c1-10))" $T/o&&grep -q "^R-land: judged by SINCE $DEL..$WS" $T/o&&! grep -q "own judge" $T/o&&[ "$(v)" = "verify-land: OK" ]'
g checkout -q --detach $SINCE;: >$R/extensions/agi/guard/r-land;g add -A;g commit -qm "empty judge";EMP=$(g rev-parse HEAD);printf 'AGI_TRUNK=%s\n' $EMP >$T/carry-emp.env
BASE=$EMP;gate re 'echo r >$R/docs/r';BASE=$B0;CARRY=$T/carry-emp.env;run re $LD $EMP $GT;CARRY=
ok "v2-c-an-EMPTIED-judge-runs-the-last-non-empty-one-and-is-NOT-held rc $rc, $(grep '^r-land: judge from' $T/o), $(v)" '[ $rc = 0 ]&&grep -qx "r-land: judge from $(echo $SINCE|cut -c1-10) (emptied at $(echo $EMP|cut -c1-10))" $T/o&&[ "$(v)" = "verify-land: OK" ]'
gate c 'echo b >$R/docs/b';RSX=$BASE;run c $LD $BASE $GT;RSX=
ok "v2-d-a-post-L140-BASE-with-no-prior-judge-HOLDS rc $rc, $(grep '^r-land' $T/o), $(v)" '[ $rc = 1 ]&&grep -q "^r-land: unread (no prior judge at BASE" $T/o&&v|grep -q "HOLD (.*r-land"'
g checkout -q --detach $EMP;g rm -q extensions/agi/guard/r-land;g commit -qm "del after empty";DE=$(g rev-parse HEAD);printf 'AGI_TRUNK=%s\n' $DE >$T/carry-de.env
BASE=$DE;gate rd 'printf "%s\n" "#!/bin/sh" "echo R-land: own judge;exit 0" >$R/extensions/agi/guard/r-land';BASE=$B0;CARRY=$T/carry-de.env;wrun rd $LD $DE $GT;CARRY=
ok "v2-f-truncate-then-delete-then-restore-runs-the-pre-truncation-judge-NOT-held rc $rc, $(grep '^r-land: judge from' $T/o), $(v)" '[ $rc = 0 ]&&grep -qx "r-land: judge from $(echo $SINCE|cut -c1-10) (deleted at $(echo $DE|cut -c1-10))" $T/o&&! grep -q "own judge" $T/o&&[ "$(v)" = "verify-land: OK" ]'
# a LAND MERGE that deletes r-land: its side branch first REWRITES the judge (SIDE), then deletes it; the merge is TREESAME to its 2nd parent, so a walk
# without --first-parent leaves the trunk and runs SIDE (the range's own judge); --first-parent stays on the trunk and finds SINCE's
g checkout -q --detach $SINCE;printf '%s\n' '#!/bin/sh' 'echo "R-land: SIDE judge";exit 0' >$R/extensions/agi/guard/r-land;g add -A;g commit -qm side;g rm -q extensions/agi/guard/r-land;g commit -qm "side del";SX=$(g rev-parse HEAD)
LM=$(g commit-tree -S -p $SINCE -p $SX -m "land merge deleting the judge" $(g merge-tree --write-tree $SINCE $SX|head -1));printf 'AGI_TRUNK=%s\n' $LM >$T/carry-lm.env
BASE=$LM;gate rm 'echo r >$R/docs/r';BASE=$B0;CARRY=$T/carry-lm.env;run rm $LD $LM $GT;CARRY=
ok "v2-g-a-land-merge-that-deletes-r-land-keeps-the-walk-on-the-first-parent-chain rc $rc, $(grep '^r-land: judge from' $T/o), $(grep -c 'SIDE judge' $T/o) SIDE line, $(v)" '[ $rc = 0 ]&&grep -qx "r-land: judge from $(echo $SINCE|cut -c1-10) (deleted at $(echo $LM|cut -c1-10))" $T/o&&! grep -q "SIDE judge" $T/o&&[ "$(v)" = "verify-land: OK" ]'
# (e) a tip cut BEFORE a trunk r-land update deletes r-land and lands by merge: the land merge (delete wins) is TREESAME to the tip -> the judge is the
# trunk's NEWEST blob (SINCE2), `deleted at` the land merge; without --first-parent the walk runs the OLD SINCE blob
g checkout -q --detach $SINCE;g rm -q extensions/agi/guard/r-land;g commit -qm "tip del (cut before the update)";TD=$(g rev-parse HEAD)
g checkout -q --detach $SINCE;printf '%s\n' '#!/bin/sh' 'echo "R-land: NEWEST judge";exit 0' >$R/extensions/agi/guard/r-land;g add -A;g commit -qm "trunk updates the judge";S2=$(g rev-parse HEAD)
GIT_INDEX_FILE=$T/ie git -C $R read-tree $S2;GIT_INDEX_FILE=$T/ie git -C $R update-index --force-remove extensions/agi/guard/r-land;LE=$(g commit-tree -S -p $S2 -p $TD -m "land merge, delete wins" $(GIT_INDEX_FILE=$T/ie git -C $R write-tree));printf 'AGI_TRUNK=%s\n' $LE >$T/carry-le.env
BASE=$LE;gate re2 'echo r >$R/docs/r';BASE=$B0;CARRY=$T/carry-le.env;run re2 $LD $LE $GT;CARRY=
ok "v2-h-(e)-a-tip-cut-before-a-trunk-judge-update-deletes-it-by-merge-runs-the-trunk-NEWEST-judge rc $rc, $(grep '^r-land: judge from' $T/o), $(v)" '[ $rc = 0 ]&&grep -qx "r-land: judge from $(echo $S2|cut -c1-10) (deleted at $(echo $LE|cut -c1-10))" $T/o&&grep -q "NEWEST judge" $T/o&&! grep -q "judged by SINCE" $T/o'
# (f) soften-then-EMPTY on a side branch, merged --no-ff: the judge is the trunk's pre-merge blob (SINCE), never the softened one
g checkout -q --detach $SINCE;printf '%s\n' '#!/bin/sh' 'echo "R-land: ok SOFTENED";exit 0' >$R/extensions/agi/guard/r-land;g add -A;g commit -qm soften;: >$R/extensions/agi/guard/r-land;g add -A;g commit -qm empty;SE=$(g rev-parse HEAD)
LF=$(g commit-tree -S -p $SINCE -p $SE -m "land merge, soften then empty" $(g merge-tree --write-tree $SINCE $SE|head -1));printf 'AGI_TRUNK=%s\n' $LF >$T/carry-lf.env
BASE=$LF;gate rf 'echo r >$R/docs/r';BASE=$B0;CARRY=$T/carry-lf.env;run rf $LD $LF $GT;CARRY=
ok "v2-i-(f)-soften-then-empty-merged-runs-the-trunk-pre-merge-judge-never-the-softened-one rc $rc, $(grep '^r-land: judge from' $T/o), $(grep -c SOFTENED $T/o) SOFTENED line, $(v)" '[ $rc = 0 ]&&grep -qx "r-land: judge from $(echo $SINCE|cut -c1-10) (emptied at $(echo $LF|cut -c1-10))" $T/o&&! grep -q SOFTENED $T/o&&grep -q "judged by SINCE" $T/o'
mkdir -p $T/wg;printf '%s\n' '#!/bin/sh' '[ "$1" = cat-file ]&&[ "$2" = blob ]&&case $3 in *:extensions/agi/guard/r-land)exit 1;;esac' 'exec /usr/bin/git "$@"' >$T/wg/git;chmod 755 $T/wg/git
BASE=$SINCE;gate ru 'echo r >$R/docs/r';BASE=$B0;CARRY=$T/carry-since.env;XPATH=$T/wg:$T/bin:/usr/bin:/bin;run ru $LD $SINCE $GT;XPATH=;CARRY=
ok "v2-e-a-present-blob-whose-read-fails-HOLDS (a retry clears it) rc $rc, $(grep '^r-land' $T/o), $(v)" '[ $rc = 1 ]&&grep -q "^r-land: unread (unreadable at BASE" $T/o&&v|grep -q "HOLD (.*r-land"'
# --- the WRAP (owner ruling (1); council 05:18:24Z + 05:19:08Z, THE list 06:06:56Z): RULES = BASE's land.rules_paths; a RULES land lands as W, never plain
gate wg 'mkdir -p $R/.agi/nodes/.geometry;echo x >$R/.agi/nodes/.geometry/x.md';run wrap wg $LD $BASE $GT;cp $T/o $T/w;WS=$(sed -n 's/^land: wrap \([0-9a-f]*\) over .*/\1/p' $T/w)
ok "w1-a-RULES-range-wraps: W = L's tree, parents [BASE, L] in order, signed $(git -C $R log -1 --format='%G? %GS' ${WS:-HEAD} 2>/dev/null), $(cut -c1-90 $T/w)" '[ -n "$WS" ]&&[ "$(g rev-parse $WS^{tree})" = "$(g rev-parse $LD^{tree})" ]&&[ "$(g log -1 --format=%P $WS)" = "$BASE $LD" ]&&[ "$(g log -1 --format="%G? %GS" $WS)" = "G t@t" ]&&grep -q "(rules: .agi/nodes/.geometry/x.md)" $T/w'
run wg $WS $BASE $GT
ok "w2-verify-land-on-W-is-OK-and-prints-R3 rc $rc, $(grep -c '^R3' $T/o) R3 lines, $(grep '^wrap:' $T/o|cut -c1-60), $(v)" '[ $rc = 0 ]&&grep -q "^held=.* WRAP over held" $T/o&&grep -q "^R3 wrap tree = land tree" $T/o&&grep -q "^wrap: " $T/o&&[ "$(v)" = "verify-land: OK" ]'
run wg $LD $BASE $GT
ok "w3-the-same-RULES-range-landed-PLAIN-HOLDS-wrap-missing rc $rc, $(grep '^wrap:' $T/o|cut -c1-70), $(v)" '[ $rc = 1 ]&&v|grep -q "HOLD (.*wrap-missing"'
gate ws "python3 -c 'import json;p=\"$R/.agi/config.json\";d=json.load(open(p));d[\"land\"][\"rules_paths\"].remove(\"CLAUDE.md\");json.dump(d,open(p,\"w\"))'";run ws $LD $BASE $GT
ok "w4-a-range-that-SHRINKS-rules_paths-landed-plain-HOLDS rc $rc, $(v)" '[ $rc = 1 ]&&v|grep -q "HOLD (.*wrap-missing"'
wrun ws $LD $BASE $GT
ok "w5-the-same-shrink-under-W-is-OK rc $rc, $(v)" '[ -n "$WS" ]&&[ $rc = 0 ]'
gate wr 'echo "# x" >>$R/extensions/agi/guard/verify-land.sh';run wr $LD $BASE $GT
ok "w6-a-guard-edit-landed-plain-HOLDS rc $rc, $(v)" '[ $rc = 1 ]&&v|grep -q "HOLD (.*wrap-missing"'
gate wa 'echo "* text=auto" >$R/.gitattributes';run wa $LD $BASE $GT
ok "w7-a-gitattributes-only-range-landed-plain-HOLDS rc $rc, $(v)" '[ $rc = 1 ]&&v|grep -q "HOLD (.*wrap-missing"'
gate wb 'mkdir -p $R/extensions/agi/bin;echo "x=1" >$R/extensions/agi/bin/x.py';wrun wb $LD $BASE $GT
ok "w8-an-extensions-bin-py-only-range-is-PLAIN-and-OK rc $rc, wrap made: ${WS:-none}, $(v)" '[ -z "$WS" ]&&grep -q "^land: plain " $T/w&&[ $rc = 0 ]&&[ "$(v)" = "verify-land: OK" ]'
g checkout -q --detach $BASE;echo '{}' >$R/.agi/config.json;g add -A;g commit -qm "cell deleted";NC=$(g rev-parse HEAD);printf 'AGI_TRUNK=%s\n' $NC >$T/carry-nc.env
B0=$BASE;BASE=$NC;gate wn 'echo n >$R/docs/n';BASE=$B0;CARRY=$T/carry-nc.env;run wrap wn $LD $NC $GT;cp $T/o $T/w;run wn $LD $NC $GT;CARRY=
ok "w9-the-cell-DELETED-at-BASE-wraps-every-land-with-the-unread-line rc $rc, $(cut -c1-100 $T/w), $(v)" 'grep -q "^land: wrap .*(rules_paths unread at BASE $(echo $NC|cut -c1-10): wrapped)" $T/w&&[ $rc = 1 ]&&v|grep -q "HOLD (.*wrap-missing"'
# R3: a wrap whose tree differs, swapped parents, unsigned, signed by another principal
gate wg 'mkdir -p $R/.agi/nodes/.geometry;echo x >$R/.agi/nodes/.geometry/x.md';W1=$(g commit-tree -S -p $BASE -p $LD $(g rev-parse $BASE^{tree}) -m bad-tree);run wg $W1 $BASE $GT
ok "w10-R3-a-wrap-whose-tree-is-not-the-land-tree-HOLDS rc $rc, $(v)" '[ $rc = 1 ]&&v|grep -q "HOLD (.*r3-tree"'
W2=$(g commit-tree -S -p $LD -p $BASE $(g rev-parse $LD^{tree}) -m swapped);run wg $W2 $BASE $GT
ok "w11-R3-swapped-parents-HOLD rc $rc, $(v)" '[ $rc = 1 ]&&v|grep -q "HOLD (held"'
W3=$(g -c commit.gpgsign=false commit-tree -p $BASE -p $LD $(g rev-parse $LD^{tree}) -m unsigned);run wg $W3 $BASE $GT
ok "w12-R3-an-UNSIGNED-wrap-HOLDS rc $rc, $(grep '^R3 signers' $T/o), $(v)" '[ $rc = 1 ]&&v|grep -q "HOLD (.*r3-signer"&&v|grep -q "HOLD (.*sigs"'
ssh-keygen -q -t ed25519 -N '' -C x@x -f $T/k2;printf 'x@x namespaces="git" %s\n' "$(cut -d' ' -f1,2 $T/k2.pub)" >>$T/allowed
W4=$(g -c user.signingkey=$T/k2 commit-tree -S -p $BASE -p $LD $(g rev-parse $LD^{tree}) -m other-signer);run wg $W4 $BASE $GT
ok "w13-R3-a-wrap-signed-by-a-non-written_by-principal-HOLDS rc $rc, $(grep '^R3 signers' $T/o), $(v)" '[ $rc = 1 ]&&grep -q "^R3 signers: wrap \[G x@x\]" $T/o&&v|grep -q "HOLD (.*r3-signer"'
gate wt "python3 -c 'import json;p=\"$R/.agi/config.json\";d=json.load(open(p));d[\"land\"][\"rules_paths\"]=[\"nothing/\"];json.dump(d,open(p,\"w\"))';echo '# y' >>$R/extensions/agi/guard/verify-land.sh";run wt $LD $BASE $GT
ok "w17-the-list-is-read-from-BASE-never-TIP: a tip swapping rules_paths for an unrelated list + a guard edit, plain, HOLDS rc $rc, $(v)" '[ $rc = 1 ]&&v|grep -q "HOLD (.*wrap-missing"'
gate wg 'mkdir -p $R/.agi/nodes/.geometry;echo x >$R/.agi/nodes/.geometry/x.md';W5=$(g commit-tree -S -p $GT -p $LD $(g rev-parse $LD^{tree}) -m wrong-first-parent);run wg $W5 $BASE $GT
ok "w18-R3-a-wrap-whose-FIRST-parent-is-not-BASE-HOLDS rc $rc, $(grep '^R3 wrap parents' $T/o), $(v)" '[ $rc = 1 ]&&v|grep -q "HOLD (.*r3-parents"'
# R2 + R1's guard route, from BASE's r-land
rlb r2 'echo "config: lander not provable in history (RULES via unsigned ff): 1 change(s); leaf signers: t x1";exit 0';BASE=$RB;gate w2 'echo r >$R/docs/r';BASE=$B0;CARRY=$T/carry-r2.env;run w2 $LD $RB $GT;CARRY=
ok "w14-R2-config-lander-not-provable-HOLDS rc $rc, $(v)" '[ $rc = 1 ]&&v|grep -q "HOLD (.*lander-unprovable"'
rlb rc 'echo "config: changed (stub)";exit 0';BASE=$RB;gate w3 'echo r >$R/docs/r';BASE=$B0;CARRY=$T/carry-rc.env;run wrap w3 $LD $RB $GT;cp $T/o $T/w;run w3 $LD $RB $GT;CARRY=
ok "w15-R1-guard-route-r-land-judged-a-config-change: wrap mode wraps, plain HOLDS rc $rc, $(cut -c1-90 $T/w), $(v)" 'grep -q "^land: wrap .*(r-land judged a config change)" $T/w&&[ $rc = 1 ]&&v|grep -q "HOLD (wrap-missing)"'
gate wc 'echo w >$R/docs/w';WS=$(g commit-tree -S -p $BASE -p $LD $(g rev-parse $LD^{tree}) -m needless);run wc $WS $BASE $GT
ok "w16-a-NEEDLESS-wrap-is-OK-and-says-so rc $rc, $(grep '^wrap:' $T/o|cut -c1-80), $(v)" '[ $rc = 0 ]&&grep -q "^wrap: .*(needless: the range is not RULES)" $T/o'
# P1 + P2 (council 07:01:14Z + 07:01:25Z + 07:01:37Z): the pathspec env is CLEARED for every spec read; `rules: N of M specs match nothing at BASE (...)` is printed
gate pa 'echo "* text=auto" >$R/.gitattributes';XLIT=1;run wrap pa $LD $BASE $GT;cp $T/o $T/w;run pa $LD $BASE $GT;XLIT=
ok "p1-GIT_LITERAL_PATHSPECS=1-inherited: a gitattributes-only range still WRAPS and plain still HOLDS rc $rc, $(grep '^land:' $T/w|cut -c1-60), $(v)" 'grep -q "^land: wrap " $T/w&&[ $rc = 1 ]&&v|grep -q "HOLD (.*wrap-missing"'
gate c 'echo b >$R/docs/b';run c $LD $BASE $GT
ok "p2-a-the-match-nothing-reading-is-on-every-run: $(grep '^rules: [0-9]' $T/o|cut -c1-60)" 'grep -q "^rules: 9 of 11 specs match nothing at BASE (" $T/o'
g checkout -q --detach $BASE;mkdir -p $R/sub;echo "* text=auto" >$R/sub/.gitattributes;g add -A;g commit -qm "base with sub/.gitattributes";SG=$(g rev-parse HEAD);printf 'AGI_TRUNK=%s\n' $SG >$T/carry-sg.env
B0=$BASE;BASE=$SG;gate sg 'echo s >$R/docs/s';BASE=$B0;CARRY=$T/carry-sg.env;XLIT=1;run sg $LD $SG $GT;XLIT=;CARRY=
ok "p2-b-a-BASE-holding-sub/.gitattributes-under-GIT_LITERAL_PATHSPECS=1: the glob spec is NOT in the match-nothing list $(grep '^rules: [0-9]' $T/o|cut -c1-40)" 'grep -q "^rules: 8 of 11 specs match nothing at BASE (" $T/o&&! grep "^rules: [0-9]" $T/o|grep -qF "(glob)**/.gitattributes"'
# gpu = lines naming a box DEVICE (anonymize's hardware list), never the bare word
printf '{"hardware": ["Zeta Card 9990"]}\n' >$T/fix.json
gate gd 'echo "runs on a Zeta Card 9990 here" >$R/docs/gd';AGI_FIX=$T/fix.json;run gd $LD $BASE $GT;AGI_FIX=
ok "g1-a-real-device-name-in-any-file-reads-nonzero $(grep '^gpu:' $T/o|cut -c1-12)" 'grep -q "^gpu: [1-9]" $T/o'
gate gw 'echo "gpu cuda nvidia words only" >$R/docs/gw';AGI_FIX=$T/fix.json;run gw $LD $BASE $GT;AGI_FIX=
ok "g2-the-bare-word-gpu-reads-0 $(grep '^gpu:' $T/o|cut -c1-12)" 'grep -q "^gpu: 0 " $T/o'
# --- (c) the FIXTURE CLASS of the anon-diff (council 3/3 alive 18:25:50Z 10-26; belam's [hold] 18:15Z on L177+L178): a PINNED fixture user's /home/<name> in an ADDED line of a file under extensions/agi/tests/ is ONE named WARN, not a HOLD
# (BASE's anonymize.fixture_homes = ["fxuser"] here). Every other hit HOLDs. FAIL CLOSED: a missing / empty / malformed cell, an unreadable or empty passwd, a pinned name that is also a passwd home.
FH=/home   # the fixture home ROOT, spelled once at run time: every row below hands the guard a real `<root>/<name>` (the class keys on it), while the committed bytes carry no home literal (SM 00:21Z 10-27: the OLD guard reads this diff too)
cfgbase(){ n=$1;j=$2;g checkout -q --detach $BASE;printf '%s' "$j" >$R/.agi/config.json;g add -A;g commit -qm "base $n";eval "BASE_$n=$(g rev-parse HEAD)";g checkout -q --detach;}
RP='"land": {"rules_paths": [".agi/config.json"]}'
cfgbase empty "{$RP, \"anonymize\": {\"fixture_homes\": []}}";cfgbase str "{$RP, \"anonymize\": {\"fixture_homes\": \"fxuser\"}}";cfgbase none "{$RP}"
fx(){ n=$1;shift;gate $n "mkdir -p \$R/extensions/agi/tests;$*";eval "LD_$n=$LD;GT_$n=$GT";}
sw(){ sbase=$BASE;BASE=$1;shift;"$@";BASE=$sbase;}      # sw BASE_x fx ...: run a gate on another base
fx fa 'echo "see $FH/fxuser/a and $FH/fxuser/b" >$R/extensions/agi/tests/x.t.sh';run fa $LD $BASE $GT;cp $T/o $T/fa.o;rcfa=$rc
ok "f1-a-pinned-fixture-user-under-tests-is-one-named-WARN rc $rcfa, $(grep -c '^anon-diff WARN' $T/fa.o) WARN line: $(grep '^anon-diff WARN' $T/fa.o|cut -c1-120), $(tail -1 $T/fa.o)" '[ $rcfa = 0 ]&&[ "$(grep -c "^anon-diff WARN (fixture class)" $T/fa.o)" = 1 ]&&grep -q "^anon-diff WARN (fixture class): pinned /home/<fxuser> x2 in extensions/agi/tests/x.t.sh$" $T/fa.o&&grep -qx "anon-diff=0" $T/fa.o&&tail -1 $T/fa.o|grep -q "verify-land: OK"'
gate fb 'echo "see $FH/fxuser/a" >$R/docs/y';LD_fb=$LD;GT_fb=$GT;run fb $LD $BASE $GT
ok "f2-the-pinned-name-OUTSIDE-tests-HOLDS (the class is the diff path, not the line) rc $rc, $(v)" '[ $rc = 1 ]&&v|grep -q "HOLD (.*anon-diff"&&! grep -q "^anon-diff WARN" $T/o'
fx fc 'echo "see $FH/zzuser/a" >$R/extensions/agi/tests/x.t.sh';run fc $LD $BASE $GT
ok "f3-an-UNPINNED-name-under-tests-HOLDS rc $rc, $(v)" '[ $rc = 1 ]&&v|grep -q "HOLD (.*anon-diff"&&! grep -q "^anon-diff WARN" $T/o'
fx fd 'echo "a $FH/fxuser/a b $FH/zzuser/b" >$R/extensions/agi/tests/x.t.sh';run fd $LD $BASE $GT
ok "f4-a-line-with-a-pinned-AND-an-unpinned-name-HOLDS (the unpinned one stays) rc $rc, $(v)" '[ $rc = 1 ]&&v|grep -q "HOLD (.*anon-diff"'
printf 'fxuser:x:1000:1000::%s/fxuser:/bin/sh\n' "$FH" >$T/pw.fx;printf '' >$T/pw.empty
g show $GT_fa:extensions/agi/tests/x.t.sh >$T/fa.x;tk=$(python3 -I -c 'import sys;sys.path.insert(0,sys.argv[1]);import paths;print(" ".join(m for f in sys.argv[2:] for m in paths.HOME_RE.findall(open(f).read())))' $R0/extensions/agi/bin $T/fa.x $T/pw.fx)
ok "f14-the-assembled-root-reaches-the-file-under-test-AND-the-passwd-stub-as-the-REAL-home-token (paths.HOME_RE: $tk; f1 WARNs on it: $(grep -o 'pinned [^ ]* x2' $T/fa.o))" '[ "$tk" = "$FH/fxuser $FH/fxuser $FH/fxuser" ]&&grep -q "pinned $FH/<fxuser> x2" $T/fa.o'
VPW=$T/pw.fx;run fa $LD_fa $BASE $GT_fa;VPW=
ok "f5-a-pinned-name-that-IS-a-passwd-home-HOLDS rc $rc, $(v)" '[ $rc = 1 ]&&v|grep -q "HOLD (.*anon-diff"&&! grep -q "^anon-diff WARN" $T/o'
VPW=$T/nowhere;run fa $LD_fa $BASE $GT_fa;VPW=
ok "f6-an-UNREADABLE-passwd-HOLDS (fails closed) rc $rc, $(v)" '[ $rc = 1 ]&&v|grep -q "HOLD (.*anon-diff"&&! grep -q "^anon-diff WARN" $T/o'
VPW=$T/pw.empty;run fa $LD_fa $BASE $GT_fa;VPW=
ok "f7-an-EMPTY-passwd-HOLDS (fails closed) rc $rc, $(v)" '[ $rc = 1 ]&&v|grep -q "HOLD (.*anon-diff"&&! grep -q "^anon-diff WARN" $T/o'
for b in empty str none;do eval "bb=\$BASE_$b";sw $bb fx fe_$b 'echo "see $FH/fxuser/a" >$R/extensions/agi/tests/x.t.sh';run fe_$b $LD $bb $GT;echo "$rc $(tail -1 $T/o)" >$T/fe_$b.r;cp $T/o $T/fe_$b.o;done
ok "f8-an-EMPTY-allowlist-HOLDS $(cat $T/fe_empty.r)" 'grep -q "^1 verify-land: HOLD (.*anon-diff" $T/fe_empty.r&&! grep -q "^anon-diff WARN" $T/fe_empty.o'
ok "f9-a-MALFORMED-allowlist-(a-string)-HOLDS $(cat $T/fe_str.r)" 'grep -q "^1 verify-land: HOLD (.*anon-diff" $T/fe_str.r&&! grep -q "^anon-diff WARN" $T/fe_str.o'
ok "f10-an-ABSENT-allowlist-HOLDS $(cat $T/fe_none.r)" 'grep -q "^1 verify-land: HOLD (.*anon-diff" $T/fe_none.r&&! grep -q "^anon-diff WARN" $T/fe_none.o'
fx ft 'echo "see $FH/zzuser/a" >$R/extensions/agi/tests/x.t.sh;printf %s "{\"anonymize\": {\"fixture_homes\": [\"zzuser\"]}}" >$R/.agi/config.json';run ft $LD $BASE $GT
ok "f11-the-allowlist-is-read-from-BASE-never-TIP (a land adding its own name) rc $rc, $(v)" '[ $rc = 1 ]&&v|grep -q "HOLD (.*anon-diff"&&! grep -q "^anon-diff WARN" $T/o'
fx fg 'echo "~/x expanduser $FH/fxuser/a" >$R/extensions/agi/tests/x.t.sh';run fg $LD $BASE $GT
ok "f13-the-WARN-counts-SUBSTITUTIONS-never-tokens (3 paths.HOME_RE tokens, 1 pinned) rc $rc, $(grep '^anon-diff WARN' $T/o|cut -c1-120)" 'grep -q "^anon-diff WARN (fixture class): pinned /home/<fxuser> x1 in extensions/agi/tests/x.t.sh$" $T/o'
# mutants: the mutated copy runs as SELF; each row is green when the mutant misbehaves (the real row above would then be RED)
mutate(){ python3 -c '
import sys
s=open(sys.argv[1]).read();a,b=sys.argv[2],sys.argv[3]
assert s.count(a)==1,("mutant anchor",a)
open(sys.argv[1],"w").write(s.replace(a,b))' "$@";}
vmut(){ cp "$VL" $T/vm.sh;mutate $T/vm.sh "$1" "$2";SELF=$T/vm.sh;}
vmut "l=paths.HOME_RE.sub(fixture,l)" "l=l";run fa $LD_fa $BASE $GT_fa;SELF=
ok "m-substitution-dropped-reads-RED the fixture line HOLDs (rc $rc): f1's WARN is gone" '[ $rc = 1 ]&&tail -1 $T/o|grep -q "HOLD (.*anon-diff"'
vmut "cur and cur.startswith('extensions/agi/tests/') and l.startswith('+')" "cur and l.startswith('+')";run fb $LD_fb $BASE $GT_fb;SELF=
ok "m-path-class-dropped-reads-RED the pinned name in docs/y passes as a WARN (rc $rc, $(v) | $(grep -E "^anon-diff" $T/o|tr "\n" " "|cut -c1-90)): the class is no longer the diff path" 'grep -q "^anon-diff WARN" $T/o&&grep -qx "anon-diff=0" $T/o'
vmut "if t[:6]!='/home/' or t[6:] not in names or" "if t[:6]!='/home/' or";run fc $LD_fc $BASE $GT_fc;SELF=
ok "m-widened-to-any-nonpasswd-name-reads-RED the UNPINNED name under tests/ WARNs (rc $rc, $(v) | $(grep -E "^anon-diff" $T/o|tr "\n" " "|cut -c1-90))" 'grep -q "^anon-diff WARN" $T/o&&grep -qx "anon-diff=0" $T/o'
vmut "if not names or not dirs: return []" "if not names: return []";VPW=$T/pw.empty;run fa $LD_fa $BASE $GT_fa;VPW=;SELF=
ok "m-empty-passwd-tolerated-reads-RED an EMPTY passwd no longer HOLDs the pinned line (rc $rc, $(v) | $(grep -E "^anon-diff" $T/o|tr "\n" " "|cut -c1-90))" 'grep -q "^anon-diff WARN" $T/o&&grep -qx "anon-diff=0" $T/o'
vmut "except Exception: return []" "except Exception: return ['fxuser']";VPW=$T/nowhere;run fa $LD_fa $BASE $GT_fa;VPW=;SELF=
ok "m-passwd-error-swallowed-reads-RED an UNREADABLE passwd WARNs instead of HOLDing (rc $rc, $(v) | $(grep -E "^anon-diff" $T/o|tr "\n" " "|cut -c1-90))" 'grep -q "^anon-diff WARN" $T/o&&grep -qx "anon-diff=0" $T/o'
vmut 'git show "$B:.agi/config.json"' 'git show "$L:.agi/config.json"';run ft $LD_ft $BASE $GT_ft;SELF=
ok "m-allowlist-from-TIP-reads-RED a land that adds its own name gets anon-diff=0 ($(grep -c '^anon-diff=0' $T/o) line)" 'grep -qx "anon-diff=0" $T/o'
# f12 (all-is-one P3 00:05:18Z 10-27): the step's ONE source (paths.HOME_RE) UNIMPORTABLE -> the unfiltered diff HOLDs, NAMED (a guard copy whose sys.path misses paths.py; as SELF, so `self` holds too)
vmut "sys.path.insert(0,os.path.dirname(os.path.abspath(anon)))" "sys.path.insert(0,'/nonexistent')";run fa $LD_fa $BASE $GT_fa;SELF=
ok "f12-an-UNIMPORTABLE-paths-HOLDS-NAMED rc $rc, $(grep '^anon-diff fixture class' $T/o|cut -c1-90), $(v)" '[ $rc = 1 ]&&grep -qx "anon-diff fixture class: unread (the step failed): nothing pinned, every hit HOLDs" $T/o&&v|grep -q "HOLD (.*anon-diff"&&! grep -q "^anon-diff WARN" $T/o'
echo "verify-land: $f FAIL";exit $f
