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
mkdir -p $R/extensions/agi/guard $R/docs $R/.agi;echo '{}' >$R/.agi/config.json;cp "$VL" $R/extensions/agi/guard/verify-land.sh;echo a >$R/docs/a;echo keep >$R/docs/keep;g add -A;g commit -qm base;BASE=$(g rev-parse HEAD)
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
run(){ env -i PATH=$T/bin:/usr/bin:/bin HOME=$T VL_T=$R VL_MAIN=$R VL_OUT=$T/out VL_ANON=$R0/extensions/agi/bin/anonymize.py VL_CARRY=${CARRY:-$T/carry.env} VL_INSTALLED=$T/bin/verify-land VL_TOOLS=$T/tools/verify-land.sh VL_RING=$T/allowed VL_RLAND_SINCE=${RSX:-$SINCE} ${XTMP:+TMPDIR=$XTMP} STUB_LOG=$T STUB_CITE_RC=${CRC:-0} ${XPATH:+PATH=$XPATH} sh ${SELF:-$T/bin/verify-land} "$@" >$T/o 2>&1;rc=$?;}
v(){ tail -1 $T/o;}
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
rlb rs 'echo "R-land: refused $2 (stub, base)";exit 1';BASE=$RB;gate rs 'printf "%s\n" "#!/bin/sh" "echo R-land: ok softened;exit 0" >$R/extensions/agi/guard/r-land';BASE=$B0;CARRY=$T/carry-rs.env;run rs $LD $RB $GT;CARRY=
ok "r4-a-tip-that-rewrites-r-land-never-softens-its-own-judge (BASE's blob runs) rc $rc, $(grep -c 'softened' $T/o) softened line, $(v)" '[ $rc = 1 ]&&! grep -q softened $T/o&&v|grep -q "HOLD (r-land)"'
# --- GATE272 (council 03:49-03:5xZ 10-26): V1 tmpfile, V3 an unresolvable BASE, V2' a deleted / emptied judge -> the LAST non-empty one, never none
gate c 'echo b >$R/docs/b';XTMP=$T/no-such-dir;run c $LD $BASE $GT;XTMP=
ok "v1-an-unwritable-TMPDIR-HOLDS-never-the-fail-open-line rc $rc, $(grep '^r-land' $T/o), $(v)" '[ $rc = 1 ]&&grep -qx "r-land: unread (tmpfile)" $T/o&&! grep -q "fail open" $T/o&&v|grep -q "HOLD (.*r-land"'
run c $LD deadbeef00deadbeef00deadbeef00deadbeef00 $GT
ok "v3-an-unresolvable-BASE-HOLDS rc $rc, $(grep '^r-land' $T/o), $(v)" '[ $rc = 1 ]&&grep -q "^r-land: unread (BASE deadbeef00)" $T/o&&! grep -q "fail open" $T/o&&v|grep -q "HOLD (.*r-land"'
# a deleting land on SINCE (judged by SINCE's own blob), then the restoring land on the deletion (judged by SINCE's blob, NOT held, never its own)
g checkout -q --detach $SINCE;g rm -q extensions/agi/guard/r-land;g commit -qm "del judge";DEL=$(g rev-parse HEAD);printf 'AGI_TRUNK=%s\n' $DEL >$T/carry-del.env
B0=$BASE;BASE=$SINCE;gate dl 'git -C $R rm -q extensions/agi/guard/r-land';BASE=$B0;printf 'AGI_TRUNK=%s\n' $SINCE >$T/carry-since.env;CARRY=$T/carry-since.env;run dl $LD $SINCE $GT;CARRY=
ok "v2-a-the-deleting-land-is-judged-by-the-pre-deletion-blob (its own HOLD is D, not r-land) $(grep -c 'judged by SINCE' $T/o) SINCE line, $(grep '^r-land=' $T/o), $(v)" 'grep -q "^R-land: judged by SINCE $SINCE..$LD" $T/o&&grep -qx "r-land=0" $T/o&&v|grep -q "HOLD (D)"'
BASE=$DEL;gate rr 'printf "%s\n" "#!/bin/sh" "echo R-land: own judge;exit 0" >$R/extensions/agi/guard/r-land';BASE=$B0;CARRY=$T/carry-del.env;run rr $LD $DEL $GT;CARRY=
ok "v2-b-the-restoring-land-runs-the-LAST-judge-and-is-NOT-held rc $rc, $(grep '^r-land: judge from' $T/o), $(v)" '[ $rc = 0 ]&&grep -qx "r-land: judge from $(echo $SINCE|cut -c1-10) (deleted at $(echo $DEL|cut -c1-10))" $T/o&&grep -q "^R-land: judged by SINCE $DEL..$LD" $T/o&&! grep -q "own judge" $T/o&&[ "$(v)" = "verify-land: OK" ]'
g checkout -q --detach $SINCE;: >$R/extensions/agi/guard/r-land;g add -A;g commit -qm "empty judge";EMP=$(g rev-parse HEAD);printf 'AGI_TRUNK=%s\n' $EMP >$T/carry-emp.env
BASE=$EMP;gate re 'echo r >$R/docs/r';BASE=$B0;CARRY=$T/carry-emp.env;run re $LD $EMP $GT;CARRY=
ok "v2-c-an-EMPTIED-judge-runs-the-last-non-empty-one-and-is-NOT-held rc $rc, $(grep '^r-land: judge from' $T/o), $(v)" '[ $rc = 0 ]&&grep -qx "r-land: judge from $(echo $SINCE|cut -c1-10) (emptied at $(echo $EMP|cut -c1-10))" $T/o&&[ "$(v)" = "verify-land: OK" ]'
gate c 'echo b >$R/docs/b';RSX=$BASE;run c $LD $BASE $GT;RSX=
ok "v2-d-a-post-L140-BASE-with-no-prior-judge-HOLDS rc $rc, $(grep '^r-land' $T/o), $(v)" '[ $rc = 1 ]&&grep -q "^r-land: unread (no prior judge at BASE" $T/o&&v|grep -q "HOLD (.*r-land"'
g checkout -q --detach $EMP;g rm -q extensions/agi/guard/r-land;g commit -qm "del after empty";DE=$(g rev-parse HEAD);printf 'AGI_TRUNK=%s\n' $DE >$T/carry-de.env
BASE=$DE;gate rd 'printf "%s\n" "#!/bin/sh" "echo R-land: own judge;exit 0" >$R/extensions/agi/guard/r-land';BASE=$B0;CARRY=$T/carry-de.env;run rd $LD $DE $GT;CARRY=
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
echo "verify-land: $f FAIL";exit $f
