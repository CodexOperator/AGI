#!/bin/sh
# post-env.t.sh: goal:g7.16.1.11.37 (owner 10-11 02:4xZ: "agi seat shouldn't be used anymore unless absolutely needed. The post should include all relevant info including box location"; council spec, SM 02:44Z): AGI_SEAT is retired. A post unit carries AGI_POST=%i and gets AGI_BOX from THIS box's own env file (/etc/agi/carry.env, ONE source: boxes.py names this box from AGI_BOX and rotate._stamp_row_box stamps the row from it, so the unit never sets it from the row); the unit REFUSES a start whose row box is not this box: "[wrong-box] row=<x> here=<y>" (exit 2).
# sh + git + jq + ssh-keygen on SCRATCH repos, throwaway keys, no live ref, no network, 0 USD. The post env is NEVER hand-written: it is the words of the agi-post@.service `Environment=` line (minus PATH) plus AGI_BOX from the unit's EnvironmentFile (a scratch carry.env, CARRY=<file>), and AGI_SEAT is in NO env of this lane. UNITFILE=<file> reads another unit text; ROOT=<repo> where the pieces are read.
# LIVE (belam, after the re-render; two GOs, never the drop-in first): `ENVFROM=/proc/<pid of the running post's claude/agi-run>/environ sh extensions/agi/tests/post-env.t.sh` builds the post env from that REAL environ (AGI_* + SHELL/DISABLE_AUTOUPDATER only) instead of the unit text, and row l1 asserts it holds AGI_POST=<name>, a non-empty AGI_BOX and NO AGI_SEAT; the e-rows then run the real pieces in it. Without ENVFROM, l1 is skipped.
# Rows: u1 the unit's Environment= line holds AGI_POST=<name>, no AGI_SEAT, no AGI_BOX literal · u2 the unit reads /etc/agi/carry.env as an EnvironmentFile BEFORE the post's own file, and the Environment= lines set no AGI_BOX (one source) · u3 the fenced pieces of every engine*.md hold 0 AGI_SEAT (falsifier 1) · e1 box n lists the signed sender, box read advances the held ref · e2 agi-at commits `alive: f.txt` onto posts/alive (witness: without AGI_POST rc 5 [no-branch]) · e3 agi-turn rc 0 with no [no-branch] (witness: without AGI_POST rc 5) · e4 agi-captive passes one agi-fill, refuses a chain (rc 2) · w1..w4 the [wrong-box] ExecCondition: match rc 0 · another box rc 2 + the message · AGI_BOX unset rc 2 · no row rc 2 · MUTANTS (each RED on the real pieces, made with sed on copies): m1 a start on another box goes ahead (the check's exit 2 -> 0) · m2 the unit sets no AGI_BOX (the carry.env line gone) · m3 agi-at reads AGI_SEAT again · m4 agi-turn reads AGI_SEAT again.
# agi-out and agi-brief are proven by the lanes that already run them: agi-outline.t.sh (85 rows, agi-out) and agi-turn.t.sh (brf, x11), whose envs no longer carry AGI_SEAT. (SM's "agi-captive :23" is agi-brief's `p=`; agi-captive itself never read it.)
T=$(mktemp -d);trap 'rm -rf $T' 0;f=0;G=/usr/bin/git;R0=${ROOT:-$(cd "$(dirname "$0")/../../.." && pwd)};GEO=$R0/.agi/nodes/.geometry
sect(){ cat $GEO/engine*.md|sed -n "/^###* $1 /,/^###* /{/^~~~/,/^~~~/{//!p}}";}
ok(){ if eval "$2";then echo "ok $1";else echo "FAIL $1";f=$((f+1));fi;}
unset GIT_AUTHOR_NAME GIT_AUTHOR_EMAIL GIT_COMMITTER_NAME GIT_COMMITTER_EMAIL GIT_DIR GIT_WORK_TREE GIT_INDEX_FILE AGI_POST AGI_SEAT AGI_BOX AGI_WT AGI_TRUNK AGI_ROLE AGI_FILL
mkdir -p $T/bin $T/hm $T/wt $T/k $T/c
[ -n "$UNITFILE" ]||UNITFILE=$GEO/engine-root.md
[ -n "$ENVFROM" ]||LIVE=
[ -z "$ENVFROM" ]||LIVE=1
# the unit text: the agi-post@.service piece of UNITFILE (UNITFILE=<file> may be just that piece)
unit(){ if [ "$UNITFILE" = "$GEO/engine-root.md" ];then sect 'agi-post@.service';else cat $UNITFILE;fi;}
unit>$T/unit;[ -s $T/unit ]||{ echo "FAIL extract: the unit piece is empty";exit 99;}
for n in box agi-at agi-turn agi-captive;do sect $n>$T/bin/$n;[ -s $T/bin/$n ]||{ echo "FAIL extract: $n";exit 99;};chmod +x $T/bin/$n;done
printf '#!/bin/sh\nexit 0\n'>$T/bin/grow.py;chmod +x $T/bin/grow.py
HERE=encryption-town;[ -n "$CARRY" ]||{ printf 'AGI_BOX=%s\nAGI_HUB=\n' $HERE>$T/carry.env;CARRY=$T/carry.env;}
# the post env as words: live = the running post's real environ (AGI_* + two unit words); else = the unit's Environment= words (minus PATH) + AGI_BOX from the carry file, but only when the unit reads it
penv(){ if [ -n "$LIVE" ];then tr '\0' '\n' <$ENVFROM|grep -E '^(AGI_[A-Z_]+|SHELL|DISABLE_AUTOUPDATER)=';else
  grep '^Environment=' $T/unit|sed 's/^Environment=//'|tr ' ' '\n'|grep -E '^(AGI_|SHELL=|DISABLE_)'|sed "s/%i/$1/g"
  grep -q '^EnvironmentFile=-/etc/agi/carry.env$' $T/unit&&grep '^AGI_BOX=' $CARRY;fi;}
P=alive;[ -z "$LIVE" ]||P=$(penv|sed -n 's/^AGI_POST=//p')
# keys + a signed refs/box/belam/alive (the setup sender, not the subject)
: >$T/signers
for u in belam alive;do
 ssh-keygen -q -t ed25519 -N '' -f $T/k/$u -C $u>/dev/null;echo "$u@agi namespaces=\"git\" $(cut -d' ' -f1,2 $T/k/$u.pub)">>$T/signers
 printf '[user]\n\tname=%s\n\temail=%s@agi\n\tsigningkey=%s\n[gpg]\n\tformat=ssh\n[gpg "ssh"]\n\tallowedSignersFile=%s\n[commit]\n\tgpgsign=false\n[safe]\n\tdirectory=*\n' $u $u $T/k/$u $T/signers>$T/c/$u
done
$G init -q $T/r;mkdir -p $T/r/.agi/nodes/.geometry
cat >$T/r/.agi/nodes/.geometry/posts.md<<'POSTS'
  - {"name":"belam","parent":"owner","harness":"claude","box":"encryption-town"}
  - {"name":"council","parent":"belam","members":["alive"]}
  - {"name":"alive","parent":"council","harness":"claude","box":"encryption-town"}
  - {"name":"dg2","parent":"belam","harness":"claude","box":"core-town"}
POSTS
(cd $T/r&&$G add -A&&$G -c user.name=t -c user.email=t@t commit -q -m fixture)
TR=$($G -C $T/r rev-parse HEAD)
BASE="HOME=$T/hm PATH=$T/bin:/usr/bin:/bin:/usr/local/bin GIT_TEST_ASSUME_DIFFERENT_OWNER=1 GIT_CONFIG_SYSTEM=/dev/null"
(cd $T/r&&printf 'hello\n'|env -i HOME=$T PATH=$T/bin:/usr/bin:/bin AGI_TRUNK=HEAD GIT_TEST_ASSUME_DIFFERENT_OWNER=1 GIT_CONFIG_GLOBAL=$T/c/belam GIT_CONFIG_SYSTEM=/dev/null AGI_POST=belam sh $T/bin/box send alive)
[ -n "$($G -C $T/r for-each-ref refs/box/belam/alive)" ]||{ echo "FAIL fixture: no signed refs/box/belam/alive";exit 99;}
# the post's ~/t: a repo whose branch posts/<P> holds one commit
$G init -q -b posts/$P $T/hm/t;(cd $T/hm/t&&echo base>base&&$G add -A&&$G -c user.name=t -c user.email=t@t commit -q -m base)
# run as the post: env -i + the post env + AGI_TRUNK/GIT config of the fixture; "$@" = [env words] cmd...; $T/bin is the piece dir
as(){ (cd $T/r&&env -i $BASE AGI_TRUNK=HEAD GIT_CONFIG_GLOBAL=$T/c/alive $(penv $P) "$@");}
ast(){ (cd $T/hm/t&&env -i $BASE GIT_CONFIG_GLOBAL=$T/c/alive AGI_WT=$T/wt $(penv $P) "$@");}   # from ~/t, the pieces' cwd
# ---- l1 (LIVE only)
if [ -n "$LIVE" ];then pe=$(penv)
 ok "l1-the-running-posts-env $ENVFROM holds AGI_POST=$P, a non-empty AGI_BOX [$(echo "$pe"|sed -n 's/^AGI_BOX=//p')] and NO AGI_SEAT [$(echo "$pe"|grep -c '^AGI_SEAT=')]" '[ -n "$P" ]&&echo "$pe"|grep -q "^AGI_BOX=.\+"&&! echo "$pe"|grep -q "^AGI_SEAT="'
else echo "skip l1 (no ENVFROM)";fi
# ---- u: the unit text
ue=$(grep '^Environment=' $T/unit|sed 's/^Environment=//'|tr ' ' '\n'|grep -v '^PATH=')
ok "u1-the-units-environment-is-AGI_POST-only the unit's Environment= words (minus PATH) [$(echo $ue)]: AGI_POST=%i present $(echo "$ue"|grep -cx 'AGI_POST=%i') (want 1), AGI_SEAT $(echo "$ue"|grep -c AGI_SEAT) (want 0), a literal AGI_BOX $(echo "$ue"|grep -c AGI_BOX) (want 0)" '[ "$(echo "$ue"|grep -cx "AGI_POST=%i")" = 1 ]&&! echo "$ue"|grep -q "AGI_SEAT\|AGI_BOX"'
u2ok(){ ci=$(grep -n '^EnvironmentFile=-/etc/agi/carry.env$' $T/unit|head -1|cut -d: -f1);pi=$(grep -n '^EnvironmentFile=-/var/lib/agi/%i.env$' $T/unit|head -1|cut -d: -f1);[ -n "$ci" ]&&[ -n "$pi" ]&&[ "$ci" -lt "$pi" ];}
u2ok;u2=$?
ok "u2-the-unit-reads-AGI_BOX-from-the-box-env-file the unit has EnvironmentFile=-/etc/agi/carry.env at line [${ci:-none}] BEFORE the post's own file at [${pi:-none}], so the post's file may override and the row never sets the box" '[ $u2 = 0 ]'
n=0;for e in $GEO/engine*.md;do c=$(awk '/^~~~/{z=!z;next} z&&/AGI_SEAT/{n++} END{print n+0}' $e);n=$((n+c));done
ok "u3-the-fenced-pieces-name-no-AGI_SEAT the ~~~ bodies of every engine*.md hold $n AGI_SEAT hit(s) (want 0; the prose history rows are not counted)" '[ "$n" = 0 ]'
# ---- e: the pieces in the post env (no AGI_SEAT anywhere)
o=$(as sh $T/bin/box n 2>$T/err);rc=$?
ok "e1-box-n-finds-its-post box n as the post [$P]: rc $rc (want 0), lists [$o] (want belam, the signed sender), 'parameter not set' $(grep -c 'parameter not set' $T/err) (want 0)" '[ $rc = 0 ]&&[ "$o" = belam ]&&! grep -q "parameter not set" $T/err'
as sh $T/bin/box read >/dev/null 2>&1;h=$($G -C $T/r for-each-ref refs/held|wc -l|tr -d ' ')
ok "e1b-box-read-advances-the-held-ref box read as the post leaves $h held ref (want 1)" '[ "$h" = 1 ]'
echo f>$T/hm/t/f.txt;ast sh $T/bin/agi-at f.txt 2>$T/err;rc=$?
m=$($G -C $T/hm/t log -1 --format=%s refs/heads/posts/$P);cnt=$($G -C $T/hm/t rev-list --count refs/heads/posts/$P)
ok "e2-agi-at-commits-as-the-post agi-at f.txt: rc $rc (want 0), subject [$m] (want '$P: f.txt'), $cnt commit(s) on posts/$P (want 2), stderr [$(head -c 60 $T/err)]" '[ $rc = 0 ]&&[ "$m" = "$P: f.txt" ]&&[ "$cnt" = 2 ]'
echo g>$T/hm/t/g.txt;(cd $T/hm/t&&env -i $BASE GIT_CONFIG_GLOBAL=$T/c/alive $(penv $P|grep -v '^AGI_POST=') sh $T/bin/agi-at g.txt 2>$T/err);wrc=$?
ok "e2w-witness-agi-at-needs-AGI_POST the SAME agi-at with AGI_POST removed: rc $wrc (want 5), [no-branch] $(grep -c '^\[no-branch\]' $T/err) (want 1): so e2 can fail" '[ $wrc = 5 ]&&grep -q "^\[no-branch\]" $T/err'
ast sh $T/bin/agi-turn 2>$T/err;rc=$?
ok "e3-agi-turn-runs-as-the-post agi-turn (no trees): rc $rc (want 0), [no-branch] $(grep -c '^\[no-branch\]' $T/err) (want 0)" '[ $rc = 0 ]&&! grep -q "^\[no-branch\]" $T/err'
(cd $T/hm/t&&env -i $BASE GIT_CONFIG_GLOBAL=$T/c/alive AGI_WT=$T/wt $(penv $P|grep -v '^AGI_POST=') sh $T/bin/agi-turn 2>$T/err);wrc=$?
ok "e3w-witness-agi-turn-needs-AGI_POST the SAME agi-turn with AGI_POST removed: rc $wrc (want 5), [no-branch] $(grep -c '^\[no-branch\]' $T/err) (want 1)" '[ $wrc = 5 ]&&grep -q "^\[no-branch\]" $T/err'
: >$T/hm/.fill
cap(){ printf '{"tool_input":{"command":"%s"}}' "$1"|env -i $BASE HOME=$T/hm $(penv $P) sh $T/bin/agi-captive 2>/dev/null;}
cap 'agi-fill open';a=$?;cap 'agi-fill open; rm -rf x';b=$?
ok "e4-agi-captive-in-the-post-env one agi-fill passes rc $a (want 0), a chained command is refused rc $b (want 2)" '[ $a = 0 ]&&[ $b = 2 ]'
# ---- w: the [wrong-box] ExecCondition, the body exactly as systemd hands it to sh (the quoted word, %i substituted)
body(){ grep '^ExecCondition=sh -c "set -f' $T/unit|sed 's/^ExecCondition=sh -c "//;s/"$//';}
wb(){ b=$(body|sed "s/%i/$1/g");[ -n "$b" ]||return 99;(cd $T/r&&env -i PATH=/usr/bin:/bin O=$T/r AGI_TRUNK=$TR ${2:+AGI_BOX=$2} GIT_CONFIG_GLOBAL=/dev/null sh -c "$b" 2>$T/err);}
wb alive $HERE;w1=$?;wb alive core-town;w2=$?;m2=$(cat $T/err);wb alive "";w3=$?;m3=$(cat $T/err);wb nobody $HERE;w4=$?
ok "w1-the-right-box-starts the row says encryption-town, this box is encryption-town: rc $w1 (want 0)" '[ $w1 = 0 ]'
ok "w2-another-box-is-refused-by-name the row says encryption-town, this box is core-town: rc $w2 (want 2), says [$m2] (want '[wrong-box] row=encryption-town here=core-town')" '[ $w2 = 2 ]&&[ "$m2" = "[wrong-box] row=encryption-town here=core-town" ]'
ok "w3-an-unset-box-is-refused AGI_BOX empty: rc $w3 (want 2), says [$m3] (want '[wrong-box] row=encryption-town here=')" '[ $w3 = 2 ]&&[ "$m3" = "[wrong-box] row=encryption-town here=" ]'
ok "w4-a-post-with-no-row-is-refused no row for nobody: rc $w4 (want 2)" '[ $w4 = 2 ]'
# ---- mutants of the REAL unit / pieces: each must go RED on the lane's own row for it
mut(){ cp $2 $T/m.$1;sed -i "$3" $T/m.$1;cmp -s $2 $T/m.$1&&{ echo "FAIL mutant-$1-did-not-change-the-text";f=$((f+1));return 1;};return 0;}
# m1: a start on another box goes ahead
cp $T/unit $T/unit.good;mut m1 $T/unit.good 's/echo \[wrong-box\] row=$b here=$AGI_BOX>&2;exit 2;}/echo \[wrong-box\] row=$b here=$AGI_BOX>\&2;exit 0;}/'&&{ cp $T/m.m1 $T/unit;wb alive core-town;r=$?;cp $T/unit.good $T/unit;ok "mutant-m1-a-wrong-box-start-goes-ahead-is-RED the check's exit 2 -> 0: another box now exits $r (want 0 = it starts anyway, which w2 forbids)" '[ $r = 0 ]'; }
# m2: the unit sets no AGI_BOX (the carry.env line gone): u2's own predicate must fail on the mutated unit
mut m2 $T/unit.good '/^EnvironmentFile=-\/etc\/agi\/carry.env$/d'&&{ cp $T/m.m2 $T/unit;u2ok;r=$?;cp $T/unit.good $T/unit;ok "mutant-m2-no-AGI_BOX-source-is-RED the unit without the carry.env line: u2's predicate exits $r (want non-zero)" '[ $r != 0 ]'; }
# m3 / m4: the pieces read AGI_SEAT again
mut m3 $T/bin/agi-at 's/P=$AGI_POST;/P=$AGI_SEAT;/'&&{ git -C $T/hm/t reset -q --hard posts/$P 2>/dev/null;echo h>$T/hm/t/h.txt;ast sh $T/m.m3 h.txt 2>$T/err;r=$?;ok "mutant-m3-agi-at-reads-AGI_SEAT-is-RED agi-at with P=\$AGI_SEAT in the post env (no AGI_SEAT): rc $r (want 5 = it commits nothing, which e2 forbids)" '[ $r = 5 ]'; }
mut m4 $T/bin/agi-turn 's/P=$AGI_POST;/P=$AGI_SEAT;/'&&{ ast sh $T/m.m4 2>$T/err;r=$?;ok "mutant-m4-agi-turn-reads-AGI_SEAT-is-RED agi-turn with P=\$AGI_SEAT in the post env: rc $r (want 5, which e3 forbids)" '[ $r = 5 ]'; }
echo "post-env: $f FAIL";exit $f
