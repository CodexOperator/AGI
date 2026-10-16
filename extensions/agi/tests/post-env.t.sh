#!/bin/sh
# post-env.t.sh: goal:g7.16.1.11.37 (owner 10-11 02:4xZ: "agi seat shouldn't be used anymore unless absolutely needed. The post should include all relevant info including box location"; council spec, SM 02:44Z): AGI_SEAT is retired. A post unit carries AGI_POST=%i and gets AGI_BOX from THIS box's own env file (/etc/agi/carry.env, ONE source: boxes.py names this box from AGI_BOX and rotate._stamp_row_box stamps the row from it, so the unit never sets it from the row); the unit REFUSES a start whose row box is not this box: "[wrong-box] row=<x> here=<y>" (exit 2).
# sh + git + jq + ssh-keygen on SCRATCH repos, throwaway keys, no live ref, no network, 0 USD. The post env is NEVER hand-written: it is the words of the agi-post@.service `Environment=` line (minus PATH) plus AGI_BOX from the unit's EnvironmentFile (a scratch carry.env, CARRY=<file>), and AGI_SEAT is in NO env of this lane. UNITFILE=<file> reads another unit text; ROOT=<repo> where the pieces are read.
# LIVE (belam, after the re-render; two GOs, never the drop-in first): `ENVFROM=/proc/<pid of the running post's claude/agi-run>/environ sh extensions/agi/tests/post-env.t.sh` builds the post env from that REAL environ (AGI_* + SHELL/DISABLE_AUTOUPDATER only) instead of the unit text, and row l1 asserts it holds AGI_POST=<name>, a non-empty AGI_BOX and NO AGI_SEAT; the e-rows then run the real pieces in it. Without ENVFROM, l1 is skipped.
# Rows: u1 the unit's Environment= line holds AGI_POST=<name>, no AGI_SEAT, no AGI_BOX literal · u2 the unit does NOT load /etc/agi/carry.env as an EnvironmentFile (that file also carries a PINNED 40-hex AGI_TRUNK, AGI_REPO, AGI_HUB, GIT_CONFIG_*, and an EnvironmentFile overrides the per-post h.conf's AGI_TRUNK) and ExecStart exports AGI_BOX from it ALONE · u5 the env the unit hands a post (the REAL ExecStart body run with a stub `script`) holds AGI_BOX=<this box> and none of AGI_TRUNK/AGI_REPO/AGI_HUB/GIT_CONFIG_VALUE_0 · f6 the drop-ins are folded in: the unit holds the agi-signers-repoint ExecStartPre (after agi-signers) and DBUS_SESSION_BUS_ADDRESS=disabled:, engine-root.md's list of host drop-ins says none, and (HOSTDIR=<dir>, default /etc/systemd/system/agi-post@.service.d, LIVE only) any *.conf there is RED · u3 the fenced pieces of every engine*.md hold 0 AGI_SEAT (falsifier 1) · e1 box n lists the signed sender, box read advances the held ref · e2 agi-at commits `alive: f.txt` onto posts/alive (witness: without AGI_POST rc 5 [no-branch]) · e3 agi-turn rc 0 with no [no-branch] (witness: without AGI_POST rc 5) · e4 agi-captive passes one agi-fill, refuses a chain (rc 2) · w1..w4 the [wrong-box] ExecCondition (it reads THIS box from carry.env itself): match rc 0 · another box rc 2 + the message · no AGI_BOX in the file rc 2 · no row rc 2 · MUTANTS (each RED on the real pieces, made with sed on copies): m1 a start on another box goes ahead (the check's exit 2 -> 0) · m2 the whole carry.env loaded again as an EnvironmentFile (a post env with no AGI_TRUNK of its own carries the 40-hex pin) · m2b ExecStart exports no AGI_BOX · m6 a re-render without the DBUS line · m3 agi-at reads AGI_SEAT again · m4 agi-turn reads AGI_SEAT again.
# PYTHON (tip 2): u4 `git grep AGI_SEAT` over bin/*.py adapters/*.py hooks/*.py hits ONLY geometry_config.py (falsifier 2; skipped when ROOT is not a git tree) · p1 the ONE helper geometry_config.resolved_seat_env(): AGI_POST wins when both are set, the v4 fallback answers when only the retired name is set, None when neither · m5 MUTANT: the helper reading the retired name first -> p1's both-set row is RED.
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
printf '#!/bin/sh\nexit 0\n'>$T/bin/agi-fill;chmod +x $T/bin/agi-fill   # g7.16.1.11.20.3: with NO agi-fill on PATH the captive gate RELEASES the window; e4 tests the gate that bites, so agi-fill is present
HERE=encryption-town;PIN=c70e3ef31338fff0f375b9bebae6091b12337b7b;[ -n "$CARRY" ]||{ printf 'AGI_BOX=%s\nAGI_HUB=\nAGI_REPO=/data/work/agi\nAGI_TRUNK=%s\nGIT_CONFIG_VALUE_0=/data/work/agi\n' $HERE $PIN>$T/carry.env;CARRY=$T/carry.env;}
# the post env as words: LIVE = the running post's real environ (AGI_* + two unit words); else = what systemd would hand the post: the unit's Environment= words (minus PATH) + the words of any EnvironmentFile naming carry.env (a mutant), then the REAL ExecStart body run under `env -i` of those words with a stub `script` that prints its environment (that is where AGI_BOX comes from)
mkdir -p $T/bin2;printf '#!/bin/sh\nenv\n'>$T/bin2/script;chmod +x $T/bin2/script
penv(){ if [ -n "$LIVE" ];then tr '\0' '\n' <$ENVFROM|grep -E '^(AGI_[A-Z_]+|SHELL|DISABLE_AUTOUPDATER)=';return;fi
  n=$1;w=$(grep '^Environment=' $T/unit|sed 's/^Environment=//'|tr ' ' '\n'|grep -E '^(AGI_|SHELL=|DISABLE_)'|sed "s/%i/$n/g")
  ef=;grep -q '^EnvironmentFile=-/etc/agi/carry.env$' $T/unit&&ef=$(grep -E '^[A-Z_]+=' $CARRY)
  body=$(grep '^ExecStart=sh -c ' $T/unit|sed "s/^ExecStart=sh -c '//;s/'\$//;s|/etc/agi/carry.env|$CARRY|g;s|%t/agi-%i/i|$T/fifo|g;s/%i/$n/g");: >$T/fifo
  env -i PATH=$T/bin2:/usr/bin:/bin HOME=$T/hm $w $ef sh -c "$body" 2>/dev/null|grep -E '^(AGI_[A-Z_]+|SHELL|DISABLE_AUTOUPDATER)=';}
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
case $P in alive|belam|council|dg2);;*)   # LIVE as any other post: it needs a row and a seat on the council, or the sender is [off-matrix]
 printf '  - {"name":"%s","parent":"council","harness":"claude","box":"encryption-town"}\n' $P>>$T/r/.agi/nodes/.geometry/posts.md
 sed -i "s/\"members\":\[\"alive\"\]/\"members\":[\"alive\",\"$P\"]/" $T/r/.agi/nodes/.geometry/posts.md;;
esac
(cd $T/r&&$G add -A&&$G -c user.name=t -c user.email=t@t commit -q -m fixture)
TR=$($G -C $T/r rev-parse HEAD)
BASE="HOME=$T/hm PATH=$T/bin:/usr/bin:/bin:/usr/local/bin GIT_TEST_ASSUME_DIFFERENT_OWNER=1 GIT_CONFIG_SYSTEM=/dev/null"
(cd $T/r&&printf 'hello\n'|env -i HOME=$T PATH=$T/bin:/usr/bin:/bin AGI_TRUNK=HEAD GIT_TEST_ASSUME_DIFFERENT_OWNER=1 GIT_CONFIG_GLOBAL=$T/c/belam GIT_CONFIG_SYSTEM=/dev/null AGI_POST=belam sh $T/bin/box send $P)   # mail for the post under test (alive in unit mode; the running post when LIVE)
[ -n "$($G -C $T/r for-each-ref refs/box/belam/$P)" ]||{ echo "FAIL fixture: no signed refs/box/belam/$P";exit 99;}
# the post's ~/t: a repo whose branch posts/<P> holds one commit
$G init -q -b posts/$P $T/hm/t;(cd $T/hm/t&&echo base>base&&$G add -A&&$G -c user.name=t -c user.email=t@t commit -q -m base)
# run as the post: env -i + the post env + AGI_TRUNK/GIT config of the fixture; "$@" = [env words] cmd...; $T/bin is the piece dir
as(){ (cd $T/r&&env -i $BASE $(penv $P) AGI_TRUNK=HEAD GIT_CONFIG_GLOBAL=$T/c/alive "$@");}   # the fixture words LAST: a running post carries its own AGI_TRUNK (its branch name), which the scratch repo does not have
ast(){ (cd $T/hm/t&&env -i $BASE GIT_CONFIG_GLOBAL=$T/c/alive AGI_WT=$T/wt $(penv $P) "$@");}   # from ~/t, the pieces' cwd
# ---- l1 (LIVE only)
if [ -n "$LIVE" ];then pe=$(penv)
 ok "l1-the-running-posts-env $ENVFROM holds AGI_POST=$P, a non-empty AGI_BOX [$(echo "$pe"|sed -n 's/^AGI_BOX=//p')] and NO AGI_SEAT [$(echo "$pe"|grep -c '^AGI_SEAT=')]" '[ -n "$P" ]&&echo "$pe"|grep -q "^AGI_BOX=.\+"&&! echo "$pe"|grep -q "^AGI_SEAT="'
else echo "skip l1 (no ENVFROM)";fi
# ---- u: the unit text
ue=$(grep '^Environment=' $T/unit|sed 's/^Environment=//'|tr ' ' '\n'|grep -v '^PATH=')
ok "u1-the-units-environment-is-AGI_POST-only the unit's Environment= words (minus PATH) [$(echo $ue)]: AGI_POST=%i present $(echo "$ue"|grep -cx 'AGI_POST=%i') (want 1), AGI_SEAT $(echo "$ue"|grep -c AGI_SEAT) (want 0), a literal AGI_BOX $(echo "$ue"|grep -c AGI_BOX) (want 0)" '[ "$(echo "$ue"|grep -cx "AGI_POST=%i")" = 1 ]&&! echo "$ue"|grep -q "AGI_SEAT\|AGI_BOX"'
u2ok(){ ! grep -q '^EnvironmentFile=.*carry.env' $T/unit&&grep -q "^ExecStart=.*export AGI_BOX=\$(sed -n .s/^AGI_BOX=//p. /etc/agi/carry.env" $T/unit;}
u2ok;u2=$?
ok "u2-the-unit-takes-AGI_BOX-from-carry.env-alone the unit loads carry.env as an EnvironmentFile: $(grep -c '^EnvironmentFile=.*carry.env' $T/unit) (want 0: the file also holds a pinned AGI_TRUNK/AGI_REPO/AGI_HUB/GIT_CONFIG_*); ExecStart exports AGI_BOX with one named sed read of it: $(grep -c '^ExecStart=.*export AGI_BOX=' $T/unit) (want 1)" '[ $u2 = 0 ]'
u5ok(){ pe=$(penv $P);echo "$pe"|grep -qx "AGI_BOX=$HERE"&&! echo "$pe"|grep -q '^\(AGI_TRUNK\|AGI_REPO\|AGI_HUB\|GIT_CONFIG_VALUE_0\)=';}
if [ -z "$LIVE" ];then u5ok;u5=$?;pe=$(penv $P)
 ok "u5-the-env-the-unit-hands-a-post-has-the-box-and-no-pin the post env from the real Environment= + ExecStart: AGI_BOX [$(echo "$pe"|sed -n 's/^AGI_BOX=//p')] (want $HERE), keys among AGI_TRUNK/AGI_REPO/AGI_HUB/GIT_CONFIG_VALUE_0: [$(echo "$pe"|grep -o '^\(AGI_TRUNK\|AGI_REPO\|AGI_HUB\|GIT_CONFIG_VALUE_0\)'|tr '\n' ' ')] (want none: a post with no AGI_TRUNK of its own must not receive the 40-hex pin)" '[ $u5 = 0 ]';fi
f6ok(){ a=$(grep -n 'agi-signers %i$' $T/unit|tail -1|cut -d: -f1);r=$(grep -n '^ExecStartPre=-+/usr/local/sbin/agi-signers-repoint %i$' $T/unit|head -1|cut -d: -f1);x=$(grep -n '^ExecStart=' $T/unit|head -1|cut -d: -f1);[ -n "$a" ]&&[ -n "$r" ]&&[ "$r" -gt "$a" ]&&[ "$r" -lt "$x" ]&&grep -q '^Environment=DBUS_SESSION_BUS_ADDRESS=disabled:$' $T/unit;}
f6ok;f6=$?
ok "f6a-the-drop-ins-are-folded-into-the-unit the unit holds ExecStartPre=-+/usr/local/sbin/agi-signers-repoint %i (after the last agi-signers ExecStartPre, before ExecStart) and Environment=DBUS_SESSION_BUS_ADDRESS=disabled: (what 50-signers-repoint and 51-no-session-bus did on the host)" '[ $f6 = 0 ]'
lst=$(grep -m1 '^Host drop-ins of agi-post@.service' $UNITFILE|sed 's/^[^:]*([^)]*): //')
ok "f6b-the-list-of-host-drop-ins-says-none engine-root.md's list line begins [$(echo "$lst"|cut -c1-24)] (want 'none.')" 'echo "$lst"|grep -q "^none\."'
# f6c: the list says "none." -> the host dir holds no *.conf (an unlisted drop-in = RED). The list names the folded drop-ins in prose, so this is the directory, not a name match.
f6cok(){ [ -z "$(ls $1/*.conf 2>/dev/null)" ]; }
mkdir -p $T/hd0 $T/hd1;: >$T/hd1/50-stray.conf
f6cok $T/hd0;w0=$?;f6cok $T/hd1;w1=$?
ok "f6w-witness-a-stray-drop-in-is-seen an empty dir passes ($w0, want 0), a dir holding one *.conf fails ($w1, want 1): so f6c can fail" '[ $w0 = 0 ]&&[ $w1 = 1 ]'
HD=${HOSTDIR:-/etc/systemd/system/agi-post@.service.d}
if [ -n "$LIVE" ]||[ -n "$HOSTDIR" ];then f6cok $HD;c=$?
 ok "f6c-no-host-drop-in $HD holds [$(ls $HD 2>/dev/null|tr '\n' ' ')] (want none: the list says none, so any *.conf = RED; run it AFTER belam's re-render and the drop-in retire)" '[ $c = 0 ]'
else echo "skip f6c (no HOSTDIR / not LIVE)";fi
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
# ---- u4 / p1: python (the one helper)
if $G -C $R0 rev-parse --git-dir >/dev/null 2>&1;then
 hits=$($G -C $R0 grep -n AGI_SEAT -- 'extensions/agi/bin/*.py' 'extensions/agi/bin/adapters/*.py' 'extensions/agi/hooks/*.py'|grep -v '^extensions/agi/bin/geometry_config.py:'|wc -l|tr -d ' ')
 ok "u4-only-the-helper-names-AGI_SEAT git grep AGI_SEAT over bin/*.py, adapters/*.py, hooks/*.py outside geometry_config.py: $hits hit(s) (want 0)" '[ "$hits" = 0 ]'
else echo "skip u4 (ROOT is not a git tree)";fi
GC=$R0/extensions/agi/bin/geometry_config.py
helper(){ env -i PATH=/usr/bin:/bin "$@" python3 -c 'import sys;sys.path.insert(0,sys.argv[1]);import geometry_config as g;print(g.resolved_seat_env())' ${HDIR:-$R0/extensions/agi/bin} 2>/dev/null;}
h1=$(helper AGI_POST=newpost AGI_SEAT=oldseat);h2=$(helper AGI_SEAT=oldseat);h3=$(helper)
ok "p1-the-helper-is-post-first-then-the-v4-fallback AGI_POST+retired name both set -> [$h1] (want newpost); only the retired name -> [$h2] (want oldseat, the v4 fallback); neither -> [$h3] (want None)" '[ "$h1" = newpost ]&&[ "$h2" = oldseat ]&&[ "$h3" = None ]'
# ---- w: the [wrong-box] ExecCondition, the body exactly as systemd hands it to sh (the quoted word, %i substituted)
body(){ grep '^ExecCondition=sh -c "set -f' $T/unit|sed 's/^ExecCondition=sh -c "//;s/"$//';}
wb(){ if [ -n "$2" ];then printf 'AGI_HUB=\nAGI_BOX=%s\n' $2>$T/wcarry;else printf 'AGI_HUB=\n'>$T/wcarry;fi;b=$(body|sed "s/%i/$1/g;s|/etc/agi/carry.env|$T/wcarry|g");[ -n "$b" ]||return 99;(cd $T/r&&env -i PATH=/usr/bin:/bin O=$T/r AGI_TRUNK=${3:-$TR} GIT_CONFIG_GLOBAL=/dev/null sh -c "$b" 2>$T/err);}
wb alive $HERE;w1=$?;wb alive core-town;w2=$?;m2=$(cat $T/err);wb alive "";w3=$?;m3=$(cat $T/err);wb nobody $HERE;w4=$?
wb alive $HERE no-such-ref;w5=$?;m5=$(cat $T/err)
IDX=$T/idx6;BL=$(printf '  - {"name": "alive", "box"\n'|$G -C $T/r hash-object -w --stdin);GIT_INDEX_FILE=$IDX $G -C $T/r read-tree $TR;GIT_INDEX_FILE=$IDX $G -C $T/r update-index --cacheinfo 100644,$BL,.agi/nodes/.geometry/posts.md;BAD=$($G -C $T/r -c user.name=t -c user.email=t@t commit-tree -p $TR -m bad $(GIT_INDEX_FILE=$IDX $G -C $T/r write-tree))
wb alive $HERE $BAD;w6=$?;m6=$(tail -1 $T/err)
BL7=$(printf -- '- {"name": "alive", "harness": "claude", "box": "%s"}\n' $HERE|$G -C $T/r hash-object -w --stdin);GIT_INDEX_FILE=$IDX $G -C $T/r update-index --cacheinfo 100644,$BL7,.agi/nodes/.geometry/posts.md;BAD7=$($G -C $T/r -c user.name=t -c user.email=t@t commit-tree -p $TR -m moved-prefix $(GIT_INDEX_FILE=$IDX $G -C $T/r write-tree))
wb alive $HERE $BAD7;w7=$?;m7=$(tail -1 $T/err)
ok "w1-the-right-box-starts the row says encryption-town, this box is encryption-town: rc $w1 (want 0)" '[ $w1 = 0 ]'
ok "w2-another-box-is-refused-by-name the row says encryption-town, this box (carry.env) is core-town: rc $w2 (want 2), says [$m2] (want '[wrong-box] row=encryption-town here=core-town')" '[ $w2 = 2 ]&&[ "$m2" = "[wrong-box] row=encryption-town here=core-town" ]'
ok "w3-an-unnamed-box-is-refused carry.env has no AGI_BOX: rc $w3 (want 2), says [$m3] (want '[wrong-box] row=encryption-town here=')" '[ $w3 = 2 ]&&[ "$m3" = "[wrong-box] row=encryption-town here=" ]'
ok "w4-a-post-with-no-row-is-refused no row for nobody: rc $w4 (want 2)" '[ $w4 = 2 ]'
ok "w5-an-unreadable-trunk-FAILS-the-unit-it-does-not-skip-it AGI_TRUNK names no ref (git show fails): rc $w5 (want 255 = failed, not the exit-2 skip), says [$m5] (want [trunk-unreadable] posts.md unreadable at no-such-ref)" '[ $w5 = 255 ]&&[ "$m5" = "[trunk-unreadable] posts.md unreadable at no-such-ref" ]'
ok "w6-an-unparsable-trunk-FAILS-the-unit-too posts.md at the trunk is cut mid-row (git shows it, jq cannot parse it): rc $w6 (want 255, not b= and the exit-2 skip), says [$m6] as its LAST stderr line, after jq own parse error (want [trunk-unreadable] posts.md unparsable at <that trunk>)" '[ $w6 = 255 ]&&[ "$m6" = "[trunk-unreadable] posts.md unparsable at $BAD" ]'
ok "w7-a-trunk-whose-rows-sed-no-longer-finds-FAILS-the-unit posts.md is valid JSON per row but the '  - {' prefix moved (FORMAT change): sed finds 0 rows, jq gets EMPTY input and exits 0: rc $w7 (want 255, not b= and the exit-2 skip on EVERY post), says [$m7] (want [trunk-unreadable] posts.md has no rows at $BAD7)" '[ $w7 = 255 ]&&[ "$m7" = "[trunk-unreadable] posts.md has no rows at $BAD7" ]'
# ---- mutants of the REAL unit / pieces: each must go RED on the lane's own row for it. They mutate the unit TEXT / a piece, so they build the post env from the unit even in a LIVE call (a running post's real environ cannot carry a mutant: m2 would never fire, and m3 / m4 need an env with no AGI_SEAT, which a v4 post has); LIVE is cleared here, after every LIVE row
[ -z "$LIVE" ]||echo "info mutants m1-m8 run in UNIT mode (LIVE only reads the running post's environ; the LIVE rows are l1 u5-skip f6c e1-e4)"
LIVE=
mut(){ cp $2 $T/m.$1;sed -i "$3" $T/m.$1;cmp -s $2 $T/m.$1&&{ echo "FAIL mutant-$1-did-not-change-the-text";f=$((f+1));return 1;};return 0;}
# m1: a start on another box goes ahead
cp $T/unit $T/unit.good;mut m1 $T/unit.good 's/echo \[wrong-box\] row=$b here=$h>&2;exit 2;}/echo \[wrong-box\] row=$b here=$h>\&2;exit 0;}/'&&{ cp $T/m.m1 $T/unit;wb alive core-town;r=$?;cp $T/unit.good $T/unit;ok "mutant-m1-a-wrong-box-start-goes-ahead-is-RED the check's exit 2 -> 0: another box now exits $r (want 0 = it starts anyway, which w2 forbids)" '[ $r = 0 ]'; }
# m7: the unreadable-trunk probe exits 2 again (the old silent skip): w5 must fail on the mutated unit
mut m7 $T/unit.good 's/unreadable at $AGI_TRUNK>&2;exit 255;/unreadable at $AGI_TRUNK>\&2;exit 2;/'&&{ cp $T/m.m7 $T/unit;wb alive $HERE no-such-ref;r=$?;cp $T/unit.good $T/unit;ok "mutant-m7-an-unreadable-trunk-skipping-again-is-RED the probe's exit 255 -> 2: an unreadable trunk now exits $r (want 2 = the silent skip, which w5 forbids)" '[ $r = 2 ]'; }
# m8: the jq guard dropped (an unparsable posts.md is the silent b= skip again): w6 must fail on the mutated unit
mut m8 $T/unit.good 's/||{ echo \[trunk-unreadable\] posts.md unparsable at $AGI_TRUNK>&2;exit 255;}//'&&{ cp $T/m.m8 $T/unit;wb alive $HERE $BAD;r=$?;cp $T/unit.good $T/unit;ok "mutant-m8-an-unparsable-trunk-skipping-again-is-RED the jq guard removed: the cut posts.md now exits $r (want 2 = the silent skip, which w6 forbids)" '[ $r = 2 ]'; }
# m9: the row count dropped (0 rows = the exit-2 skip on every post again): w7 must fail on the mutated unit
mut m9 $T/unit.good 's/;\[ $(git -c safe.directory=$O -C $O show $AGI_TRUNK:.agi\/nodes\/.geometry\/posts.md|grep -c .^  - {.) -gt 0 \]||{ echo \[trunk-unreadable\] posts.md has no rows at $AGI_TRUNK>&2;exit 255;}//'&&{ cp $T/m.m9 $T/unit;wb alive $HERE $BAD7;r=$?;cp $T/unit.good $T/unit;ok "mutant-m9-the-row-count-dropped-is-RED the 0-rows guard removed: the moved-prefix trunk now exits $r (want 2 = the silent skip on every post, which w7 forbids)" '[ $r = 2 ]'; }
# m2: the WHOLE carry.env loaded again as an EnvironmentFile (before the post's own file): a post env with no AGI_TRUNK of its own carries the 40-hex pin -> u5's predicate AND u2's must fail on the mutated unit
mut m2 $T/unit.good 's/^EnvironmentFile=-\/var\/lib\/agi\/%i.env$/EnvironmentFile=-\/etc\/agi\/carry.env\n&/'&&{ cp $T/m.m2 $T/unit;u5ok;r5=$?;u2ok;r2=$?;pk=$(penv $P|sed -n 's/^AGI_TRUNK=//p');cp $T/unit.good $T/unit;ok "mutant-m2-the-whole-carry-env-is-RED loaded as an EnvironmentFile: the post env then carries AGI_TRUNK=[$pk] (the 40-hex pin) -> u5's predicate exits $r5 and u2's $r2 (want both non-zero)" '[ $r5 != 0 ]&&[ $r2 != 0 ]&&[ ${#pk} = 40 ]'; }
# m2b: ExecStart exports no AGI_BOX -> the post env has no box
mut m2b $T/unit.good 's/export AGI_BOX=$(sed -n "s\/^AGI_BOX=\/\/p" \/etc\/agi\/carry.env 2>\/dev\/null);//'&&{ cp $T/m.m2b $T/unit;u5ok;r=$?;cp $T/unit.good $T/unit;ok "mutant-m2b-no-AGI_BOX-export-is-RED ExecStart without the export: u5's predicate exits $r (want non-zero: the post env has no AGI_BOX)" '[ $r != 0 ]'; }
# m6: a re-render without the DBUS line
mut m6 $T/unit.good '/^Environment=DBUS_SESSION_BUS_ADDRESS=disabled:$/d'&&{ cp $T/m.m6 $T/unit;f6ok;r=$?;cp $T/unit.good $T/unit;ok "mutant-m6-a-render-without-the-DBUS-line-is-RED the unit minus Environment=DBUS_SESSION_BUS_ADDRESS=disabled: : f6a's predicate exits $r (want non-zero)" '[ $r != 0 ]'; }
# m3 / m4: the pieces read AGI_SEAT again
mut m3 $T/bin/agi-at 's/P=$AGI_POST;/P=$AGI_SEAT;/'&&{ git -C $T/hm/t reset -q --hard posts/$P 2>/dev/null;echo h>$T/hm/t/h.txt;ast sh $T/m.m3 h.txt 2>$T/err;r=$?;ok "mutant-m3-agi-at-reads-AGI_SEAT-is-RED agi-at with P=\$AGI_SEAT in the post env (no AGI_SEAT): rc $r (want 5 = it commits nothing, which e2 forbids)" '[ $r = 5 ]'; }
mut m4 $T/bin/agi-turn 's/P=$AGI_POST;/P=$AGI_SEAT;/'&&{ ast sh $T/m.m4 2>$T/err;r=$?;ok "mutant-m4-agi-turn-reads-AGI_SEAT-is-RED agi-turn with P=\$AGI_SEAT in the post env: rc $r (want 5, which e3 forbids)" '[ $r = 5 ]'; }
# m5: the helper reads the retired name FIRST: p1's both-set row must fail on the mutated module
mkdir -p $T/m5;sed -e 's/"AGI_POST"/"@@"/' -e 's/"AGI_SEAT"/"AGI_POST"/' -e 's/"@@"/"AGI_SEAT"/' $GC>$T/m5/geometry_config.py;cmp -s $GC $T/m5/geometry_config.py&&{ echo "FAIL mutant-m5-did-not-change-the-module";f=$((f+1)); }
mh=$(HDIR=$T/m5 helper AGI_POST=newpost AGI_SEAT=oldseat)
ok "mutant-m5-the-helper-reading-the-retired-name-first-is-RED the swapped helper with both set answers [$mh] (want oldseat = the wrong winner, which p1 forbids)" '[ "$mh" = oldseat ]'
echo "post-env: $f FAIL";exit $f
