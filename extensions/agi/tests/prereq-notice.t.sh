#!/bin/sh
# prereq-notice.t.sh [ROOT]: goal:g7.16.1.11.46.12 (the prereq-cleared notice; owner 23:2xZ 10-23, council 3/3). The step extensions/agi/bin/prereq_notice.py diffs refs/notices/prereq/seen against the trunk and APPENDS one line per claimer per move to the uid's own alarm spool (alarm_spool.py append, DETERMINISTIC --id); the alarm_drain row signs and sends. The step never calls box.
# sh + git + python3 + ssh-keygen on SCRATCH repos (a throwaway key, a ring with sanctuary-master@agi, a stub `box send` that signs like the seat), the REAL alarm_spool.py drain (its uid check patched in-process: the drain must run as agi-<seat>). No network, no root, 0 USD.
# Rows: r1 replays L74 (835e014e75 -> 6b6f926c0d, the nine wave-1 leaves) through the real append + drain: director-general-2 / director-science-1 / director-general-3 / director-goals-1 each get exactly ONE [landed] commit on refs/box/sanctuary-master/<post>, naming exactly their leaf ids (4 in total), each G against the ring as sanctuary-master@agi
# r2.. the mutant table, each one-edit mutant RED where named: a second run appends 0 (m: no marker appends 4) · the same notice appended twice is sent once (m: no --id) · a dead-lettered notice gives sent < cleared and reads red · 3 board-only moves send 0 and leave lag=0 · an unclaimed leaf sends 0 · a leaf whose needs: is active sends 0 and sends 1 when it completes · a needs: id that names no node is refused at mint · the seen ref deleted exits non-zero and sends 0 · a stopped step makes lag grow and reads red (m: no lap check) · a marker keyed per tip re-sends on the next move · Assigned-to DG2 -> dg1 on a cleared leaf gives dg1 exactly 1 and DG2 0 more · n* the negative: the step is exactly ONE path under the glob and holds no `box send` (m: renamed outside the glob = RED, never a vacuous pass; m: a `box send` planted = RED).
# Exit = the number of FAIL lines (99 = the fixture could not be built).
G=/usr/bin/git
R0=${ROOT:-${1:-$(cd "$(dirname "$0")/../../.." && pwd)}}
BIN=$R0/extensions/agi/bin
T=$(mktemp -d);trap 'rm -rf $T' 0;f=0
ok(){ if eval "$2";then echo "ok $1";else echo "FAIL $1";f=$((f+1));fi;}
red(){ if eval "$2";then echo "FAIL $1 (the mutant read GREEN)";f=$((f+1));else echo "ok $1";fi;}
unset GIT_DIR GIT_WORK_TREE GIT_INDEX_FILE GIT_AUTHOR_NAME GIT_AUTHOR_EMAIL GIT_COMMITTER_NAME GIT_COMMITTER_EMAIL AGI_POST
export HOME=$T/hm GIT_CONFIG_GLOBAL=/dev/null GIT_CONFIG_SYSTEM=/dev/null
mkdir -p $T/hm $T/k $T/mbin
[ -f $BIN/prereq_notice.py ]&&[ -f $BIN/alarm_spool.py ]||{ echo "FAIL fixture: $BIN/prereq_notice.py or alarm_spool.py is missing";exit 99;}
ssh-keygen -q -t ed25519 -N '' -f $T/k/key -C sm >/dev/null||{ echo "FAIL fixture: ssh-keygen";exit 99;}
echo "sanctuary-master@agi namespaces=\"git\" $(cut -d' ' -f1,2 $T/k/key.pub)" >$T/ring
cat >$T/box <<'XX'
#!/bin/sh
[ "$1" = send ]||exit 2
[ -z "$BOX_FAIL" ]||{ echo "$BOX_FAIL" >&2;exit 1;}
msg=$(cat);t=$(git hash-object -w -t tree /dev/null);o=$(git rev-parse -q --verify refs/box/$AGI_POST/$2||:)
c=$(printf '%s\n' "$msg"|GIT_AUTHOR_NAME=sanctuary-master GIT_AUTHOR_EMAIL=sanctuary-master@agi GIT_COMMITTER_NAME=sanctuary-master GIT_COMMITTER_EMAIL=sanctuary-master@agi git -c gpg.format=ssh -c user.signingkey=$KEY commit-tree -S ${o:+-p $o} $t)||exit 1
git update-ref refs/box/$AGI_POST/$2 $c
XX
printf '#!/bin/sh\n[ "$1" = add ]||exit 2\nprintf "%%s\\n" "$2" >>"$NOTICE_OUT"\n' >$T/notice;chmod +x $T/box $T/notice
SP=$T/spool/alarm.spool
# ---- helpers
# the fixture geometry: posts.md rows (levels: belam 1, sanctuary-master 2, its directors 3, deep-post 4 = OFF SM's matrix) and the REAL box piece of $R0 (the matrix function is CALLED from it, never copied)
fixgeo(){ { printf -- '---\nid: config:posts\nmint_id: 00000000000000000000000000000005\ntype: config\n---\nposts:\n'
 for r in 'belam|owner|1' 'sanctuary-master|belam|1' 'director-goals-1|sanctuary-master|1' 'director-general-2|sanctuary-master|1' 'deep-post|director-goals-1|1' 'inert|sanctuary-master|0' 'old-retired|sanctuary-master|1';do n=${r%%|*};q=${r#*|};pa=${q%|*};h=${q#*|};if [ $h = 1 ];then printf '  - {"name": "%s", "parent": "%s", "harness": "claude-code"}\n' $n $pa;else printf '  - {"name": "%s", "parent": "%s"}\n' $n $pa;fi;done
 printf '  - {"name": "council", "parent": "belam", "role": "council", "members": []}\n';} >$R/.agi/nodes/.geometry/posts.md
 sed -n '/^### box (/,/^### [^b]/p' $R0/.agi/nodes/.geometry/engine-post.md >$R/.agi/nodes/.geometry/engine-post.md;}
newrepo(){ R=${1:-$T/r};rm -rf $R $T/spool;$G init -q -b core/season3/main $R;$G -C $R config user.name t;$G -C $R config user.email t@agi;$G -C $R config commit.gpgsign false;mkdir -p $R/.agi/nodes/goal $R/.agi/nodes/town $R/.agi/nodes/.geometry;fixgeo;printf -- '---\nid: goal:g1\nmint_id: 00000000000000000000000000000001\ntype: goal\nstatus: active\nparents: []\n---\nroot\n' >$R/.agi/nodes/goal/g1.md;printf 'town 0\n' >$R/.agi/nodes/town/board.md;commit base;seq=1;}
commit(){ $G -C $R add -A;$G -C $R commit -q --allow-empty -m "${1:-c}";}
leaf(){ s=$1;c=$2;st=$3;shift 3;seq=$((${seq:-1}+1));m=$(printf '%032x' $(( $(echo $s|cksum|cut -d' ' -f1) )) );p=$R/.agi/nodes/goal/$s.md
 { printf -- '---\nid: goal:%s\nmint_id: %s\ntype: goal\nstatus: %s\nparents:\n  - goal:g1\n' $s $m $st;[ $# = 0 ]||{ printf 'needs:\n';for n in "$@";do printf '  - %s\n' $n;done;};printf -- '---\n\n## Agent Notes\n';[ "$c" = - ]||printf 'Assigned to **%s**.\n' $c;} >$p;}
seed(){ python3 ${B:-$BIN}/prereq_notice.py seed --repo $R --at ${1:-$($G -C $R rev-parse HEAD)} >/dev/null 2>&1;}
step(){ python3 ${B:-$BIN}/prereq_notice.py run --repo $R --spool $SP >$T/so 2>$T/se;rc=$?;}
nsp(){ [ -f $SP ]&&wc -l <$SP|tr -d ' '||echo 0;}
drain(){ (cd $R&&KEY=$T/k/key BOX_FAIL="$BOX_FAIL" NOTICE_OUT=$T/notice.out python3 -c "
import sys;sys.path.insert(0,'$BIN');import alarm_spool as a;from pathlib import Path
a._uid_name=lambda:'agi-sanctuary-master'
sys.exit(a.drain('sanctuary-master',max_tries=${1:-60},spool=Path('$SP'),box_bin=Path('$T/box'),notice_bin=Path('$T/notice'),tree=Path('$R')))" >$T/do 2>&1);}
sentn(){ $G -C $R log refs/box/sanctuary-master/$1 --format=%B 2>/dev/null|grep -c '^Alarm-job: prereq_notice';}
lineo(){ python3 ${B:-$BIN}/prereq_notice.py line --repo $R $@ 2>/dev/null;}
mut(){ rm -rf $T/mbin;mkdir -p $T/mbin;cp $BIN/prereq_notice.py $BIN/alarm_spool.py $BIN/frontmatter.py $T/mbin/
 # control: the UNMUTATED copy must run from here, or every mutant would "read RED" because it cannot start
 python3 -c "import sys;sys.path.insert(0,'$T/mbin');import prereq_notice,alarm_spool" 2>/dev/null||{ echo "FAIL mutant control: the unmutated copy in $T/mbin does not import";f=$((f+1));return 1;}
 sed "$2" $BIN/$1 >$T/mbin/$1;if cmp -s $BIN/$1 $T/mbin/$1;then echo "FAIL mutant: the edit did not change $1 (anchor drifted)";f=$((f+1));return 1;fi;chmod +x $T/mbin/$1;}
# ---- r1: L74 replayed through the real append + drain
GC=$($G -C $R0 rev-parse --path-format=absolute --git-common-dir 2>/dev/null)
for c in 835e014e75 6b6f926c0d;do $G -C $R0 cat-file -e $c^{commit} 2>/dev/null||{ echo "FAIL fixture: L74 commit $c is not in $R0's objects";exit 99;};done
R=$T/r74;rm -rf $R;$G init -q -b core/season3/main $R;echo $GC/objects >$R/.git/objects/info/alternates;$G -C $R update-ref refs/heads/core/season3/main 6b6f926c0d;$G -C $R config user.name t;$G -C $R config user.email t@agi
seed 835e014e75;step;drain;a74=$rc
lid(){ for n in $@;do printf 'goal:g7.16.1.11.46.%s,' $n;done;}
names(){ $G -C $R log refs/box/sanctuary-master/$1 --format=%s%n%b 2>/dev/null|grep -o 'goal:g7[0-9.]*'|sort|tr '\n' ',';}
exp(){ for n in $@;do echo "goal:g7.16.1.11.46.$n";done|sort|tr '\n' ',';}
sg(){ $G -C $R -c gpg.ssh.allowedSignersFile=$T/ring log refs/box/sanctuary-master/$1 --format='%G? %ce' 2>/dev/null|sort -u|tr '\n' ';';}
tot=0
for pr in director-general-2:2.3.4.5 director-science-1:6.7.8 director-general-3:9 director-goals-1:10;do p=${pr%%:*};ids=$(echo ${pr#*:}|tr . ' ');n=$(sentn $p);tot=$((tot+n));got=$(names $p)
 ok "r1-L74-$p-gets-exactly-ONE-[landed]-naming-exactly-its-ids sent $n (want 1), names [$got] (want [$(exp $ids)]), signed [$(sg $p)] (want 'G sanctuary-master@agi;')" '[ "$n" = 1 ]&&[ "$got" = "$(exp $ids)" ]&&[ "$(sg $p)" = "G sanctuary-master@agi;" ]';done
ok "r1-L74-four-notices-in-total step rc $a74 (want 0), notices sent $tot (want 4), spool lines left $(nsp) (want 0)" '[ $a74 = 0 ]&&[ $tot = 4 ]&&[ "$(nsp)" = 0 ]'
# ---- r2: a second run appends 0; a crash before the seen ref moved is guarded by the markers (m: no marker appends 4 more)
unmark(){ $G -C $R for-each-ref --format='%(refname)' refs/notices/prereq/sent refs/notices/prereq/bundle|while read -r r;do $G -C $R update-ref -d $r;done;$G -C $R update-ref refs/notices/prereq/seen $1;}
r2(){ R=$T/r74;rm -rf $T/spool;unmark 835e014e75;step;first=$(nsp);$G -C $R update-ref refs/notices/prereq/seen 835e014e75;step;second=$(nsp);}
r2;ok "r2-a-run-after-a-crash-before-seen-moved-appends-0 first run +$first (want 4), the re-run +$((second-first)) (want 0)" '[ "$first" = 4 ]&&[ "$second" = "$first" ]'
if mut prereq_notice.py 's|git(repo, "update-ref", f"{SENT}/{claimer}/{k}", new, "")|pass|'; then B=$T/mbin;r2;B=;red "r2m-mutant-no-marker-appends-4-more (first +$first, re-run +$((second-first)))" '[ "$second" = "$first" ]';fi
# ---- r3: the same notice appended twice is sent once (m: no deterministic --id sends twice)
r3(){ newrepo;leaf l1 director-goals-1 active;seed;commit one;base=$($G -C $R rev-parse HEAD~1);step;unmark $base;step;l3=$(nsp);drain;s3=$(sentn director-goals-1);}
r3;ok "r3-the-same-notice-appended-twice-is-sent-once spool lines $l3 (want 2, one id), dg1 sent $s3 (want 1)" '[ "$l3" = 2 ]&&[ "$s3" = 1 ]'
if mut prereq_notice.py 's/, "--id", aid\]/]/'; then B=$T/mbin;r3;B=;red "r3m-mutant-no-deterministic-id-sends-twice (dg1 sent $s3)" '[ "$s3" = 1 ]';fi
# ---- r4: a dead-lettered notice: sent < cleared, red
newrepo;leaf l1 director-goals-1 active;commit one;seed;leaf l2 director-goals-1 active;commit two;step;BOX_FAIL="no route";drain 1;BOX_FAIL=;step
o=$(lineo);ok "r4-a-dead-lettered-notice-gives-sent-below-cleared-and-reads-red [$o]" 'echo "$o"|grep -q "cleared=1 sent=0" && echo "$o"|grep -q "red=.*dead-letter=1"'
# ---- r5: board-only moves send 0 and leave lag=0
newrepo;leaf l1 director-goals-1 active;commit one;seed;for i in 1 2 3;do printf 'town %s\n' $i >$R/.agi/nodes/town/board.md;commit "board $i";done;step;o=$(lineo)
ok "r5-three-board-only-moves-send-0-and-leave-lag-0 rc $rc, spool $(nsp) (want 0), [$o]" '[ $rc = 0 ]&&[ "$(nsp)" = 0 ]&&echo "$o"|grep -q "lag=0 red=none"'
# ---- r6: an unclaimed leaf sends 0
newrepo;seed;leaf u1 - active;commit unclaimed;step;ok "r6-an-unclaimed-leaf-sends-0 rc $rc, spool $(nsp) (want 0)" '[ $rc = 0 ]&&[ "$(nsp)" = 0 ]'
# ---- r7: needs: active sends 0, then 1 when it completes (event b), and not again
newrepo;leaf dep - active;commit dep;seed;leaf n1 director-goals-1 active goal:dep;commit n1;step;a=$(nsp)
ok "r7a-a-leaf-whose-needs-is-still-active-sends-0 rc $rc, spool $a (want 0)" '[ $rc = 0 ]&&[ "$a" = 0 ]'
leaf dep - complete;commit "dep complete";step;b=$(nsp);ok "r7b-and-sends-1-when-it-completes rc $rc, spool $b (want 1)" '[ $rc = 0 ]&&[ "$b" = 1 ]'
printf 'x\n' >>$R/.agi/nodes/goal/n1.md;commit "touch n1";step;ok "r7c-and-never-again-on-a-later-move spool $(nsp) (want 1)" '[ "$(nsp)" = 1 ]'
# ---- r8: a needs: id that names no node is refused at mint (spawn_gate, which write.py create and grow.py both run)
python3 - "$BIN" "$R0" >$T/o8 2>&1 <<'XX'
import sys;sys.path.insert(0,sys.argv[1]);import spawn_gate as g;from pathlib import Path
rules=g.load_spawn_rules(Path(sys.argv[2]).joinpath(".agi",*g.SCHEMAS_SUBDIR),root=Path(sys.argv[2])/".agi")
idx={"goal:g1":"goal","goal:dep":"goal"}
def chk(needs,nid="goal:new"):
    fm={"id":nid,"type":"goal","goal_kind":"subgoal","status":"active","parents":["goal:g1"]}
    if needs is not None: fm["needs"]=needs
    return g.check_spawn("goal",["goal:g1"],rules=rules,type_index=idx,fm=fm,node_id=nid).status
print("none",chk(None));print("known",chk(["goal:dep"]));print("unknown",chk(["goal:nope"]));print("self",chk(["goal:new"]));print("notlist",chk("goal:dep"))
XX
ok "r8-a-needs-id-that-names-no-node-is-refused-at-mint [$(tr '\n' ' ' <$T/o8)]" 'grep -q "^none approved" $T/o8&&grep -q "^known approved" $T/o8&&grep -q "^unknown rejected" $T/o8&&grep -q "^self rejected" $T/o8&&grep -q "^notlist rejected" $T/o8'
# ---- r9: the seen ref deleted: non-zero, sends 0, no re-seed
newrepo;leaf l1 director-goals-1 active;commit one;seed;$G -C $R update-ref -d refs/notices/prereq/seen;leaf l2 director-goals-1 active;commit two;step
ok "r9-the-seen-ref-deleted-exits-non-zero-and-sends-0 rc $rc (want 3), spool $(nsp) (want 0), re-seeded: $($G -C $R rev-parse -q --verify refs/notices/prereq/seen>/dev/null&&echo YES||echo no) (want no), says MISSING: $(grep -c MISSING $T/se)" '[ $rc = 3 ]&&[ "$(nsp)" = 0 ]&&! $G -C $R rev-parse -q --verify refs/notices/prereq/seen >/dev/null&&grep -q MISSING $T/se'
# ---- r10: a stopped step: lag grows and reads red, clocked by the OLDEST UNSEEN commit (N2) (m: no lag check never reads red)
cat_at(){ $G -C $R add -A;GIT_COMMITTER_DATE="$1" GIT_AUTHOR_DATE="$1" $G -C $R commit -q --allow-empty -m "${2:-c}";}
OLD="2026-01-01T00:00:00Z"
newrepo;leaf l1 director-goals-1 active;commit base;seed;for i in 1 2 3;do printf 'town %s\n' $i >$R/.agi/nodes/town/board.md;cat_at $OLD "board $i";done;o=$(lineo)
ok "r10-a-stopped-step-makes-lag-grow-and-reads-red [$o]" 'echo "$o"|grep -q "lag=3 red=lag>60min"'
if mut prereq_notice.py 's/            if age > lim:/            if False:/'; then B=$T/mbin;o=$(lineo);B=;red "r10m-mutant-no-lag-check-never-reads-red [$o]" 'echo "$o"|grep -q "red=lag>"';fi
# N2: an OLD seen tip with only a FRESH unseen commit is not red (the seen commit's own age says nothing); the mutant clocks the seen commit and reads red
newrepo;leaf l1 director-goals-1 active;cat_at $OLD base;seed;printf 'town 1\n' >$R/.agi/nodes/town/board.md;commit fresh;o=$(lineo)
ok "fx2-an-old-seen-tip-with-only-a-fresh-unseen-commit-is-not-red [$o]" 'echo "$o"|grep -q "lag=1 red=none"'
if mut prereq_notice.py 's/log", "-1", "--format=%ct", first\[0\]/log", "-1", "--format=%ct", seen/'; then B=$T/mbin;o=$(lineo);B=;red "fx2m-mutant-clocking-the-seen-commit-reads-red-on-a-fresh-move [$o]" 'echo "$o"|grep -q "red=none"';fi
# ---- n1: a trunk that does not resolve is RED, never "red=none" (N1)
o=$(lineo --trunk refs/heads/nope);ok "fx1-a-missing-trunk-reads-red-trunk-unresolved [$o]" 'echo "$o"|grep -q "lag=-1 red=trunk-unresolved"'
if mut prereq_notice.py 's/        red.append("trunk-unresolved") .*$/        pass/'; then B=$T/mbin;o=$(lineo --trunk refs/heads/nope);B=;red "fx1m-mutant-a-missing-trunk-with-no-red [$o]" 'echo "$o"|grep -q "trunk-unresolved"';fi
# ---- n3: a malformed claim is RED, never silently skipped (N3): one strict claim + one without the bold
newrepo;leaf l1 director-goals-1 active;commit one;seed;leaf l2 - active;printf 'Assigned to director-goals-1 (no bold)\n' >>$R/.agi/nodes/goal/l2.md;commit two;o=$(lineo)
ok "fx3-a-malformed-claim-reads-red-unparsed [$o]" 'echo "$o"|grep -q "claims=1 .*red=unparsed=1"'
if mut prereq_notice.py 's/    for kind in ("dead", "unreachable", "unparsed"):/    for kind in ("dead", "unreachable"):/'; then B=$T/mbin;o=$(lineo);B=;red "fx3m-mutant-no-unparsed-red [$o]" 'echo "$o"|grep -q "unparsed=1"';fi
# ---- n4: an undelivered bundle (a bundle ref past the limit whose Alarm-id never reached the outbox) is RED (N4)
newrepo;leaf l1 director-goals-1 active;cat_at $OLD base;seed;$G -C $R update-ref refs/notices/prereq/bundle/pn-lost HEAD "";o=$(lineo)
ok "fx4-a-bundle-past-the-limit-with-no-outbox-commit-reads-red-unsent [$o]" 'echo "$o"|grep -q "red=.*unsent=1"'
t4=$($G -C $R hash-object -w -t tree /dev/null);c4=$(printf 'x\n\nAlarm-job: prereq_notice\nAlarm-id: pn-lost\n'|$G -C $R commit-tree $t4);$G -C $R update-ref refs/box/sanctuary-master/director-goals-1 $c4;o=$(lineo)
ok "fx4b-and-green-once-its-alarm-id-is-in-the-outbox [$o]" '! echo "$o"|grep -q "unsent"'
$G -C $R update-ref -d refs/box/sanctuary-master/director-goals-1
if mut prereq_notice.py 's/    if unsent:/    if False:/'; then B=$T/mbin;o=$(lineo);B=;red "fx4m-mutant-no-unsent-red [$o]" 'echo "$o"|grep -q "unsent=1"';fi
# ---- n5: a re-claim is a NEW notice (N5): X -> Y -> X gives X 2 and Y 1; X unchanged across later moves gives nothing more
n5(){ newrepo;leaf l1 director-general-2 active;seed;commit "claim X";step;drain;leaf l1 director-goals-1 active;commit "claim Y";step;drain;leaf l1 director-general-2 active;commit "re-claim X";step;drain
 x5=$(sentn director-general-2);y5=$(sentn director-goals-1);printf 'town 1\n' >$R/.agi/nodes/town/board.md;commit later;step;drain;x6=$(sentn director-general-2);}
n5;ok "fx5-a-re-claim-is-a-new-notice X sent $x5 (want 2), Y sent $y5 (want 1), after an unrelated move X $x6 (want 2)" '[ "$x5" = 2 ]&&[ "$y5" = 1 ]&&[ "$x6" = 2 ]'
if mut prereq_notice.py 's/        extra = needs if event == "b" else \[intro(repo, new, p, claimer)\]/        extra = []/'; then B=$T/mbin;n5;B=;red "fx5m-mutant-a-key-that-ignores-the-claim-commit-sends-X-once (X sent $x5)" '[ "$x5" = 2 ]';fi
# ---- c*: the threshold is a CELL (notice_lag_red_min on the trunk's .agi/config.json), and the word "lap" is not in the step
cl(){ newrepo;leaf l1 director-goals-1 active;mkdir -p $R/.agi;printf '{"prereq_notice":{"notice_lag_red_min":%s}}\n' $1 >$R/.agi/config.json;commit base;seed;printf 'town 1\n' >$R/.agi/nodes/town/board.md;cat_at "$(date -u -d '5 minutes ago' +%FT%TZ)" mv;}
cl 1;o=$(lineo);ok "c1-the-cell-notice_lag_red_min-sets-the-limit (1 min, a 5 min old unseen commit) [$o]" 'echo "$o"|grep -q "red=lag>1min"'
cl 60;o=$(lineo);ok "c2-the-same-move-under-the-60-min-cell-is-not-red [$o]" 'echo "$o"|grep -q "red=none"'
o=$(lineo --lag-red-min 2);ok "c3-the-flag-overrides-the-cell [$o]" 'echo "$o"|grep -q "red=lag>2min"'
ok "c4-the-word-lap-is-in-no-line-of-the-step ($(grep -ci lap $BIN/prereq_notice.py) hits, want 0)" '[ "$(grep -ci lap $BIN/prereq_notice.py)" = 0 ]'
# ---- r11: a marker keyed per tip re-sends on the next move
newrepo;leaf l1 director-goals-1 active;seed;commit one;old=$($G -C $R rev-parse HEAD~1);step;n1=$(nsp)
$G -C $R update-ref refs/notices/prereq/seen $old;printf 'town 9\n' >$R/.agi/nodes/town/board.md;commit board;step;ok "r11-the-marker-is-per-claimer-leaf-event-not-per-tip spool $n1 -> $(nsp) (want 1 -> 1)" '[ "$n1" = 1 ]&&[ "$(nsp)" = 1 ]'
if mut prereq_notice.py 's/\*sorted(needs)\]/*sorted(needs), os.environ.get("PN_TIP", "")]/'; then B=$T/mbin;newrepo;leaf l1 director-goals-1 active;seed;commit one;old=$($G -C $R rev-parse HEAD~1);export PN_TIP=a;step;n1=$(nsp);$G -C $R update-ref refs/notices/prereq/seen $old;printf 'town 9\n' >$R/.agi/nodes/town/board.md;commit board;export PN_TIP=b;step;B=;unset PN_TIP;red "r11m-mutant-keyed-per-tip-re-sends (spool $n1 -> $(nsp))" '[ "$(nsp)" = 1 ]';fi
# ---- r12: Assigned-to director-general-2 -> director-goals-1 on a cleared leaf: dg1 exactly 1, DG2 0 more
newrepo;leaf l1 director-general-2 active;seed;commit "l1 for dg2";step;drain;d2a=$(sentn director-general-2);leaf l1 director-goals-1 active;commit reassign;step;drain
ok "r12-reassigning-a-cleared-leaf-notifies-the-new-claimer-once dg2 sent $d2a -> $(sentn director-general-2) (want 1 -> 1), dg1 sent $(sentn director-goals-1) (want 1)" '[ "$d2a" = 1 ]&&[ "$(sentn director-general-2)" = 1 ]&&[ "$(sentn director-goals-1)" = 1 ]'
# ---- k*: the READER (council 05:34Z, R-1..R-3): the prefix `Assigned to **name**` with anything after it, classified by BOX's own matrix function (called from the landed box piece)
cls1(){ # cls1 'RAWLINE' -> the board line for ONE active leaf whose Agent Notes carry RAWLINE
 newrepo;seed;leaf kk - active;printf '%s\n' "$1" >>$R/.agi/nodes/goal/kk.md;commit kk;lineo;}
k(){ o=$(cls1 "$2");ok "$1 [$o]" "$3";}
k k1-a-claim-with-trailing-prose-is-a-claim 'Assigned to **director-goals-1**. Parent: x' 'echo "$o"|grep -q "claims=1 held=0 self=0 .*red=none"'
k k2-a-name-then-a-parenthesis-is-a-claim 'Assigned to **director-goals-1 (point)**' 'echo "$o"|grep -q "claims=1 held=0 self=0 .*red=none"'
k k3-the-council-placement-is-held-and-never-red 'Assigned to **the council** (placement).' 'echo "$o"|grep -q "claims=0 held=1 self=0 .*red=none"'
k k3b-the-directors-placement-is-held-whole 'Assigned to **the directors, by their own split (room `directors`)**' 'echo "$o"|grep -q "claims=0 held=1 self=0 .*red=none"'
k k3c-a-council-role-row-is-held-not-dead 'Assigned to **council**.' 'echo "$o"|grep -q "claims=0 held=1 self=0 .*red=none"'
k k4-sanctuary-masters-own-leaf-is-self 'Assigned to **sanctuary-master**' 'echo "$o"|grep -q "claims=0 held=0 self=1 .*red=none"'
k k5-a-post-with-no-row-is-dead-naming-its-file 'Assigned to **ghost**.' 'echo "$o"|grep -q "red=dead=1\[kk\]"'
k k5b-a-row-with-no-harness-is-dead 'Assigned to **inert**.' 'echo "$o"|grep -q "red=dead=1\[kk\]"'
k k5c-a-retired-row-only-is-dead 'Assigned to **old**.' 'echo "$o"|grep -q "red=dead=1\[kk\]"'
k k6-a-live-row-off-sms-matrix-is-unreachable-naming-its-file 'Assigned to **deep-post**.' 'echo "$o"|grep -q "claims=0 .*red=unreachable=1\[kk\]"'
k k7-a-line-with-no-bold-is-unparsed 'Assigned to deep-post' 'echo "$o"|grep -q "red=unparsed=1\[kk\]"'
# mutants of the reader, each RED against its row
for m in 'k3|s/    if raw.lower().startswith(PLACEMENT):/    if False:/|Assigned to **the council** (placement).|held=1' 'k2|s/    name = re.split(r"\[ (\]", raw, maxsplit=1)\[0\]/    name = raw/|Assigned to **director-goals-1 (point)**|claims=1' 'k6|s/    return "claim" if self.ok(name) else "unreachable"/    return "claim"/|Assigned to **deep-post**.|unreachable=1' 'k5|s/        if name.endswith("-retired") or row is None or not row.get("harness"):/        if False:/|Assigned to **ghost**.|dead=1';do id=${m%%|*};r=${m#*|};sedx=${r%%|*};r=${r#*|};rawl=${r%%|*};want=${r#*|}
 if mut prereq_notice.py "$sedx";then B=$T/mbin;o=$(cls1 "$rawl");B=;red "k${id}m-mutant-of-the-reader-reads-RED [$o]" 'echo "$o"|grep -q "$want"';fi;done
# R-3: the census is built once, caught up per run on the CHANGED goal files only, and rebuilt when posts.md changes
newrepo;seed;leaf c1 director-goals-1 active;commit c1;step;c0=$($G -C $R rev-parse -q --verify refs/notices/prereq/census);o=$(lineo)
ok "k8-run-persists-the-census-and-line-reads-it [$o]" '[ -n "$c0" ]&&echo "$o"|grep -q "claims=1 "'
leaf c2 deep-post active;commit c2;o=$(lineo);ok "k8b-line-catches-the-census-up-on-the-one-changed-file-without-a-run [$o]" 'echo "$o"|grep -q "claims=1 .*red=unreachable=1\[c2\]"'
if mut prereq_notice.py 's/    names = r.stdout.split()/    names = []/'; then B=$T/mbin;o=$(lineo);B=;red "k8bm-mutant-no-catch-up-misses-the-new-leaf [$o]" 'echo "$o"|grep -q "unreachable=1"';fi
sed -i 's/{"name": "director-goals-1", "parent": "sanctuary-master", "harness": "claude-code"}/{"name": "director-goals-1", "parent": "sanctuary-master"}/' $R/.agi/nodes/.geometry/posts.md;commit "dg1 loses its harness";step;o=$(lineo)
ok "k8c-a-posts-md-change-rebuilds-the-census [$o]" 'echo "$o"|grep -q "red=dead=1\[c1\]"'
if mut prereq_notice.py 's/    if any(n in GEOMETRY for n in names):/    if False:/'; then B=$T/mbin;newrepo;seed;leaf c1 director-goals-1 active;commit c1;PNS=1;step;sed -i 's/{"name": "director-goals-1", "parent": "sanctuary-master", "harness": "claude-code"}/{"name": "director-goals-1", "parent": "sanctuary-master"}/' $R/.agi/nodes/.geometry/posts.md;commit "dg1 loses its harness";python3 $T/mbin/prereq_notice.py run --repo $R --spool $SP >/dev/null 2>&1;o=$(lineo);B=;red "k8cm-mutant-no-rebuild-keeps-a-stale-claim [$o]" 'echo "$o"|grep -q "dead=1"';fi
# ---- fa*..ff*: the board's root is the .agi DIR (council 05:47-05:49Z 10-24, F-a..F-f): the reader reads the same tree from any cwd, and a reader that read NOTHING is a NAMED red
fa(){ newrepo;leaf l1 director-goals-1 active;leaf l2 deep-post active;commit two;seed;$G -C $R update-ref -d refs/notices/prereq/census;}   # no persisted census: line builds the full one through its pathspecs
fa;a1=$(lineo);a2=$(python3 ${B:-$BIN}/prereq_notice.py line --repo $R/.agi 2>/dev/null)
ok "fa1-line-from-the-agi-dir-equals-line-from-the-repo-root [root $a1] [agi $a2]" '[ -n "$a1" ]&&[ "$a1" = "$a2" ]&&echo "$a1"|grep -q "claims=1 .*red=unreachable=1"'
if mut prereq_notice.py 's/    return tuple(":(top)" + p for p in paths)/    return tuple(paths)/'; then B=$T/mbin;fa;a1=$(lineo);a2=$(python3 $B/prereq_notice.py line --repo $R/.agi 2>/dev/null);B=;red "fa1m-mutant-a-pathspec-without-top-reads-the-agi-dir-DIFFERENTLY [root $a1] [agi $a2]" '[ "$a1" = "$a2" ]';fi
fa;o=$(python3 -c "
import sys;sys.path.insert(0,'$BIN');import success_metrics as s;from pathlib import Path;print(s._notices(Path('$R/.agi')))" 2>&1)
ok "fa2-the-metrics-segment-from-the-agi-dir-carries-claims [$o]" 'echo "$o"|grep -q "^notices: claims=1 "'
# F-b: nothing read is red. (1) no goal file at the trunk
newrepo;rm -f $R/.agi/nodes/goal/*.md;commit empty;seed;o=$(lineo)
ok "fb1-no-goal-files-at-the-trunk-is-a-named-red [$o]" 'echo "$o"|grep -q "red=.*no-goal-files-read"'
if mut prereq_notice.py 's/            red.append("no-goal-files-read")/            pass/'; then B=$T/mbin;o=$(lineo);B=;red "fb1m-mutant-no-goal-files-with-no-red [$o]" 'echo "$o"|grep -q "no-goal-files-read"';fi
# (2) goal files exist and an ACTIVE one is claimed, but the census read none (a pathspec that matches nothing on a non-empty goal dir)
CZ='s|"^Assigned to ", rev_, "--", \*top(\*LEAF_DIRS)|"^Assigned to ", rev_, "--", *top(".agi/nowhere")|'
if mut prereq_notice.py "$CZ"; then B=$T/mbin;newrepo;leaf l1 director-goals-1 active;commit one;seed;o=$(lineo);B=;ok "fb2-a-census-that-read-nothing-while-an-active-leaf-is-claimed-reads-no-claims-read [$o]" 'echo "$o"|grep -q "claims=0 .*red=.*no-claims-read"';fi
if mut prereq_notice.py "$CZ;"'s/            red.append("no-claims-read") .*$/            pass/'; then B=$T/mbin;newrepo;leaf l1 director-goals-1 active;commit one;seed;o=$(lineo);B=;red "fb2m-mutant-no-claims-read-with-no-red-reads-GREEN [$o]" 'echo "$o"|grep -q "no-claims-read"';fi
newrepo;leaf l1 director-goals-1 retired;commit retired;seed;o=$(lineo)
ok "fb3-a-goal-dir-with-no-ACTIVE-claim-is-not-no-claims-read [$o]" '! echo "$o"|grep -q "no-claims-read"'
# F-c / F-f: each ref is its own check. A clone has neither refs/notices/* nor the trunk branch; a repo with neither ref reads BOTH reds
newrepo;leaf l1 director-goals-1 active;commit one;o=$(lineo --trunk refs/heads/nope)
ok "ff1-a-repo-with-neither-ref-reads-BOTH-reds [$o]" 'echo "$o"|grep -q "lag=-1 red=seen-unresolved,trunk-unresolved"'
if mut prereq_notice.py 's/        red.append("trunk-unresolved") .*$/        pass/'; then B=$T/mbin;o=$(lineo --trunk refs/heads/nope);B=;red "ff1m-mutant-a-missing-seen-hides-the-missing-trunk [$o]" 'echo "$o"|grep -q "trunk-unresolved"';fi
newrepo;leaf l1 director-goals-1 active;commit one;seed;$G -C $R branch side;rm -rf $T/cl;$G clone -q --shared --no-checkout -b side $R $T/cl 2>/dev/null;o=$(python3 $BIN/prereq_notice.py line --repo $T/cl 2>/dev/null)
ok "fc1-a-shared-clone-without-refs-notices-or-the-trunk-branch-reads-named-reds-never-none [$o]" 'echo "$o"|grep -q "red=seen-unresolved,trunk-unresolved"&&! echo "$o"|grep -q "red=none"'
# F-e: the cron reads MAIN, never the clone (the writer's root is `{root}`; the settling row is test_board_notices.py)
# ---- n*: the negative (F3): ONE path under the glob, no `box send` in it
N=$T/n;rm -rf $N;$G init -q -b t $N;$G -C $N config user.email t@agi;$G -C $N config user.name t;mkdir -p $N/extensions/agi/bin;cp $BIN/prereq_notice.py $N/extensions/agi/bin/;$G -C $N add -A;$G -C $N commit -qm n
cnt(){ $G -C $N ls-files 'extensions/agi/bin/prereq_notice*'|wc -l|tr -d ' ';}
bs(){ $G -C $N grep -n 'box send' -- 'extensions/agi/bin/prereq_notice*'|wc -l|tr -d ' ';}
ok "n1-the-step-is-exactly-one-path-and-holds-no-box-send ls-files $(cnt) (want 1), 'box send' hits $(bs) (want 0)" '[ "$(cnt)" = 1 ]&&[ "$(bs)" = 0 ]'
$G -C $N mv extensions/agi/bin/prereq_notice.py extensions/agi/bin/prereqnotify.py;$G -C $N commit -qm rename;red "n1m-mutant-the-step-renamed-outside-the-glob-reads-RED (ls-files $(cnt))" '[ "$(cnt)" = 1 ]'
$G -C $N mv extensions/agi/bin/prereqnotify.py extensions/agi/bin/prereq_notice.py;echo '# box send x' >>$N/extensions/agi/bin/prereq_notice.py;$G -C $N commit -qam plant;red "n2m-mutant-a-box-send-planted-reads-RED ('box send' hits $(bs))" '[ "$(bs)" = 0 ]'
# ---- m1: the board segment is part of the metrics line
newrepo;leaf l1 director-goals-1 active;commit one;seed;o=$(python3 -c "
import sys;sys.path.insert(0,'$BIN');import success_metrics as s;from pathlib import Path;print(s._notices(Path('$R')))" 2>&1)
ok "m1-the-metrics-line-carries-the-notices-segment [$o]" 'echo "$o"|grep -Eq "^notices: claims=[0-9]+ held=[0-9]+ self=[0-9]+ cleared=[0-9]+ sent=[0-9]+ lag=-?[0-9]+ red=[a-z0-9>,=.-]+$"'
# ---- m2*: make_line carries BOTH segments, each counted by its KEY and content, never by position (council 04:23Z: reorder -> green, a segment twice or missing -> RED)
# (earlier text:) make_line carries BOTH segments in ONE RELATIVE order (re-cut on L84, SM 01:5xZ; SM 02:0xZ: NOT end-of-line, so the land order of the stacks does not matter and DG2's `intake:` may stay last): graph | success | p1 (DG3's, optional) ... notices (this leaf's, always); each segment's failure is NAMED, never fatal
mk2(){ # mk2 DIR: a copy of success_metrics.py (the mutants edit it) with the sibling modules still found in BIN
 mkdir -p $1;cp $BIN/success_metrics.py $1/;}
ml(){ # ml DIR MODE -> the make_line text for MODE: both | nop1 | p1dead | notdead
 python3 - "$1" "$BIN" "$R" "$2" <<'XX' 2>&1
import sys,types
d,b,repo,mode=sys.argv[1:5]
sys.path.insert(0,b);sys.path.insert(0,d)
import success_metrics as s;from pathlib import Path
s._run_metrics_once=lambda root:({}, "stub")
if mode=="both" or mode=="notdead": s.p1_segment=lambda r:"| p1: stub $/landed=1"
if mode=="nop1": s.p1_segment=lambda r:""
if mode=="notdead":
    import prereq_notice
    def boom(*a,**k): raise RuntimeError("refs gone")
    prereq_notice.line=boom
print(s.make_line(Path(repo)))
XX
}
newrepo;leaf l1 director-goals-1 active;commit one;seed;mk2 $T/mm0
cn(){ printf '%s' "$o"|grep -o "[|] $1:"|wc -l|tr -d ' ';}
segs(){ [ "$(cn p1)" = "$1" ]&&[ "$(cn notices)" = 1 ]&&[ "$(cn intake)" -le 1 ]&&[ "$(cn trajectory)" -le 1 ];}
o=$(ml $T/mm0 both);ok "m2a-p1-and-notices-each-once-with-their-content [p1 $(cn p1), notices $(cn notices): $(echo "$o"|grep -o '| notices:.*')]" 'segs 1&&echo "$o"|grep -q "[|] p1: stub [$]/landed=1"&&echo "$o"|grep -Eq "[|] notices: claims=[0-9]+ held=[0-9]+ self=[0-9]+ cleared=[0-9]+ sent=[0-9]+ lag=-?[0-9]+ red=[a-z0-9>,=.-]+"'
o2="$o | extra: 1"
o=$o2;ok "m2a2-a-later-segment-after-notices-changes-nothing (position is not pinned) [p1 $(cn p1), notices $(cn notices)]" 'segs 1'
o=$(ml $T/mm0 nop1);ok "m2b-no-p1-segment-means-no-p1-text-and-notices-still-present [p1 $(cn p1), notices $(cn notices)]" 'segs 0&&! echo "$o"|grep -q "p1:"'
mkdir -p $R/.agi/context/local-maxxing;cp $R0/.agi/config.json $R/.agi/config.json;printf '{bad' >$R/.agi/context/local-maxxing/p1-results.json
o=$(ml $T/mm0 p1dead);ok "m2c-a-dead-p1-reader-is-named-and-notices-still-present [$(echo "$o"|grep -o '| p1:[^|]*')]" 'segs 1&&echo "$o"|grep -Eq "[|] p1: UNMEASURED[(]results unreadable: P1Refused[)]"'
o=$(ml $T/mm0 notdead);ok "m2d-a-dead-notices-reader-is-named-and-p1-still-present [$(echo "$o"|grep -o '| notices:.*')]" 'segs 1&&echo "$o"|grep -Eq "[|] notices: UNMEASURED[(]source failed: RuntimeError[)]"&&! echo "$o"|grep -o "notices: UNMEASURED.*"|grep -q "[/]"'
mk2 $T/mm1;sed -i 's/    return f"{line} | {_notices(root)}"/    return f"{line.split(\" | p1:\")[0]} | {_notices(root)}{line[len(line.split(\" | p1:\")[0]):]}"/' $T/mm1/success_metrics.py
cmp -s $T/mm1/success_metrics.py $BIN/success_metrics.py&&{ echo "FAIL m2e: the reorder mutation did not change success_metrics.py";f=$((f+1));}
o=$(ml $T/mm1 both);ok "m2e-a-REORDER-reads-GREEN (notices before p1, [$(echo "$o"|grep -o '| success:.*'|cut -c1-100)])" 'segs 1&&echo "$o"|grep -q "[|] p1: stub"'
mk2 $T/mm2;sed -i 's/    return f"{line} | {_notices(root)}"/    return f"{line} | {_notices(root)} | {_notices(root)}"/' $T/mm2/success_metrics.py
cmp -s $T/mm2/success_metrics.py $BIN/success_metrics.py&&{ echo "FAIL m2m: the twice mutation did not change success_metrics.py";f=$((f+1));}
o=$(ml $T/mm2 both);red "m2m-mutant-a-segment-TWICE-reads-RED [notices x$(cn notices)]" 'segs 1'
mk2 $T/mm3;sed -i 's/    return f"{line} | {_notices(root)}"/    return line/' $T/mm3/success_metrics.py
cmp -s $T/mm3/success_metrics.py $BIN/success_metrics.py&&{ echo "FAIL m2n: the missing mutation did not change success_metrics.py";f=$((f+1));}
o=$(ml $T/mm3 both);red "m2n-mutant-a-segment-MISSING-reads-RED [notices x$(cn notices)]" 'segs 1'
# F-a on make_line: the board CLI's root is the .agi dir
fa;R_=$R;R=$R/.agi;o=$(ml $T/mm0 both);R=$R_
ok "fa3-make_line-of-the-agi-dir-carries-claims-in-the-notices-segment [$(echo "$o"|grep -o '| notices:.*'|cut -c1-60)]" 'echo "$o"|grep -q "[|] notices: claims=1 "'
exit $f
