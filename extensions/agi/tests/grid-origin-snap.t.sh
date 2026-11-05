#!/bin/sh
# grid-origin-snap.t.sh: goal:g7.16.1.11.46.16 -- the THIRD history (council 07:47Z 10-26, belam's G1a [red]): origin's refs/grid/node holds tips
# this repo never fetched, so push-changed is rejected on every name whose origin tip is not in MAIN.
# O1 `grid.py origin-snap`: a forced fetch into the PRIVATE mirror refs/grid/origin-snap (never a shared ref, never pushed); a fetch that errors or lists
#    0 refs is `unread`, rc 1.
# O2 liveness: a second run one lap later diffs the tips; a tip moved (or a name appeared) to a commit that is NOT inside this repo's own history is a LIVE
#    second writer (rc 2, no QUIET verdict); this repo's own push landing is not.
# O3 `unify --into refs/grid/node --legacy refs/grid/origin-snap --write` only on a QUIET mirror; a diverged pair merges only when the trees are EQUAL and
#    is a CONFLICT (listed by mint, nothing written) otherwise; a name in all three histories keeps all three tips reachable; `--check` counts the UNION.
# sh + git + python3 on a SCRATCH repo (the grid-namespace.t.sh recipe). `--lap 0` stands for "one lap later" so the lane never sleeps. Every mutant (m*) must read RED.
T=$(mktemp -d);trap 'rm -rf $T' 0;f=0;nrows=0;G=/usr/bin/git;R0=${ROOT:-$(cd "$(dirname "$0")/../../.." && pwd)};BIN=${BIN:-$R0/extensions/agi/bin}
ok(){ nrows=$((nrows+1));if eval "$2";then echo "ok $1";else echo "FAIL $1";f=$((f+1));fi;}
unset GIT_AUTHOR_NAME GIT_AUTHOR_EMAIL GIT_COMMITTER_NAME GIT_COMMITTER_EMAIL GIT_DIR GIT_WORK_TREE AGI_TRUNK
printf '[user]\n\tname=t\n\temail=t@t\n[commit]\n\tgpgsign=false\n[safe]\n\tdirectory=*\n' >$T/gitconfig;export GIT_CONFIG_GLOBAL=$T/gitconfig GIT_CONFIG_SYSTEM=/dev/null
export PYTHONDONTWRITEBYTECODE=1 PYTHONPATH=$R0/extensions/agi/src
NS=refs/grid/node;SNAP=refs/grid/origin-snap;LNS=refs/grid/local-maxxing/node;CFG='{"grid":{"storage_trunk":"refs/grid","push_batch_limit":7}}'
mintn(){ printf '%032x' $1;}
nodemd(){ printf -- '---\nid: idea:n%s\nmint_id: %s\ntype: idea\nstatus: %s\nparents:\n  - goal:g\n---\nbody %s\n' $1 $(mintn $1) $2 "$3";}
mk(){ d=$1;n=$2;st=$3;tx=$4;shift 4;b=$(nodemd $n $st "$tx"|$G -C $d hash-object -w --stdin);t=$(printf '100644 blob %s\tnode.md\n' $b|$G -C $d mktree);pa=;for x;do pa="$pa -p $x";done;echo "$tx"|$G -C $d commit-tree $t $pa;}
mut(){ python3 - "$1" "$2" "$3" <<'PY'
import sys
s=open(sys.argv[1]).read();a,b=sys.argv[2],sys.argv[3]
assert s.count(a)==1,("mutant anchor",a)
open(sys.argv[1],"w").write(s.replace(a,b))
PY
}
grid(){ (cd $P&&python3 extensions/agi/bin/grid.py "$@");}
refs(){ $G -C $P for-each-ref --format='%(refname) %(objectname)' "$@";}
sha(){ $G -C $P rev-parse -q --verify "$1" 2>/dev/null;}
push(){ $G -C $P push -q $REM "$1:refs/grid/node/$2" 2>&1;}   # push a commit by sha to the remote's ref (the "other box's" write)
# the fixture: MAIN (P) with the ONE namespace, and a bare REMOTE whose refs/grid/node is the third history
#  m1 equal | m2 origin AHEAD of ours | m3 origin BEHIND ours | m4 diverged, EQUAL trees | m5 diverged, UNEQUAL trees | m6 origin-ONLY
mkfix(){ P=$1;REM=$1.rem.git;rm -rf $P $REM;mkdir -p $P/.agi/nodes/idea $P/extensions/agi;$G init -q $P;$G init -q --bare $REM;cp -r $BIN $P/extensions/agi/bin;find $P/extensions/agi/bin -name __pycache__ -prune -exec rm -rf {} +
 echo "$CFG">$P/.agi/config.json;$G -C $P remote add origin $REM
 for i in 1 2 3 4 5 6;do eval "c0_$i=$(mk $P $i active root-$i)";done
 c1=$(mk $P 1 active a1 $c0_1);$G -C $P update-ref $NS/$(mintn 1) $c1;push $c1 $(mintn 1)
 a=$(mk $P 2 active a2 $c0_2);b=$(mk $P 2 active b2 $a);$G -C $P update-ref $NS/$(mintn 2) $a;push $b $(mintn 2)
 a=$(mk $P 3 active a3 $c0_3);b=$(mk $P 3 active b3 $a);$G -C $P update-ref $NS/$(mintn 3) $b;push $a $(mintn 3)
 a=$(mk $P 4 active same4 $c0_4);b=$(mk $P 4 active same4 $a);p=$(mk $P 4 active mid4 $c0_4);o=$(mk $P 4 active same4 $p);$G -C $P update-ref $NS/$(mintn 4) $b;push $o $(mintn 4)
 a=$(mk $P 5 active ns5 $c0_5);o=$(mk $P 5 active or5 $c0_5);$G -C $P update-ref $NS/$(mintn 5) $a;push $o $(mintn 5)
 o=$(mk $P 6 active only6 $c0_6);push $o $(mintn 6)
 $G -C $P add -A >/dev/null 2>&1;$G -C $P commit -qm fixture;}
snap(){ grid origin-snap origin --lap 0;}
mkfix $T/base;P=$T/base;REM=$T/base.rem.git
ok "base-fixture MAIN holds 5 refs in refs/grid/node, the remote 6 (the sixth is origin-only), and no origin-snap exists" '[ "$(refs $NS|wc -l|tr -d " ")" = 5 ]&&[ "$($G -C $P ls-remote origin "refs/grid/node/*"|wc -l|tr -d " ")" = 6 ]&&[ -z "$(refs $SNAP)" ]'
# --- o1: the snapshot is private and forced
cp_(){ src=${2:-base};rm -rf $T/$1 $T/$1.rem.git;cp -a $T/$src $T/$1;cp -a $T/$src.rem.git $T/$1.rem.git;P=$T/$1;REM=$T/$1.rem.git;$G -C $P remote set-url origin $REM;}
cp_ pa;refs $NS >$T/pa.ns0;snap >$T/o1.out 2>&1;o1=$?;refs $NS >$T/pa.ns1
ok "o1a-the-snapshot-fills-the-private-mirror-and-moves-no-shared-ref origin-snap fetched 6 refs into $SNAP (rc $o1: first look, no verdict); refs/grid/node is byte-identical before and after: $(tr '\n' ' ' <$T/o1.out|cut -c1-170)" '[ $o1 = 0 ]&&[ "$(refs $SNAP/node|wc -l|tr -d " ")" = 6 ]&&cmp -s $T/pa.ns0 $T/pa.ns1&&grep -q "first look" $T/o1.out&&[ ! -e $P/.agi/sessions/origin-snap/quiet ]'
ok "o1b-the-newest-tip-is-named its committer date and name are printed so a human can see who wrote last" 'grep -q "newest tip [0-9-]*T[0-9:]*[+-][0-9:]* by t " $T/o1.out'
rm -rf $T/pb;cp_ pb;$G -C $P remote set-url origin $T/nowhere.git;snap >$T/o2.out 2>&1;o2=$?
ok "r1a-a-fetch-that-errors-is-unread the remote is not there: unread, rc $o2, no mirror ref written" '[ $o2 = 1 ]&&grep -q "unread (fetch from origin failed" $T/o2.out&&[ -z "$(refs $SNAP)" ]'
rm -rf $T/pc $T/pc.rem.git;cp_ pc;rm -rf $REM;$G init -q --bare $REM;snap >$T/o3.out 2>&1;o3=$?
ok "r1b-an-empty-remote-is-unread a remote that lists 0 refs/grid/node refs is unread rc $o3 (an empty side would 'succeed' with 0 merged), and unify against the empty mirror writes nothing" 'grid unify --into refs/grid --legacy '$SNAP' --write >$T/o3u.out 2>&1;u=$?;[ $o3 = 1 ]&&grep -q "unread" $T/o3.out&&[ $u = 1 ]&&grep -q "unread" $T/o3u.out&&[ "$(refs $NS|wc -l|tr -d " ")" = 5 ]'
cp_ pd;mut $P/extensions/agi/bin/grid.py '    if not have:
        print(f"grid origin-snap: unread ({remote} lists no' '    if False:
        print(f"grid origin-snap: unread ({remote} lists no';rm -rf $REM;$G init -q --bare $REM;snap >$T/o4.out 2>&1;o4=$?
ok "m-empty-check-cut-reads-RED with the empty check removed an empty remote reads 'first look' rc $o4 instead of unread" '[ $o4 = 0 ]'
# --- o2: liveness
cp_ pe;snap >/dev/null 2>&1;snap >$T/q.out 2>&1;q=$?
ok "o2a-a-quiet-lap-writes-the-verdict the second run finds no foreign move: QUIET, rc $q, the verdict names the mirror's digest: $(grep -o 'QUIET[^:]*' $T/q.out|head -1)" '[ $q = 0 ]&&grep -q "QUIET for the lap" $T/q.out&&[ -s $P/.agi/sessions/origin-snap/quiet ]&&grep -q "0 foreign move" $T/q.out'
cp_ pf;snap >/dev/null 2>&1;x=$(mk $P 1 active foreign-edit $(sha $NS/$(mintn 1)));push $x $(mintn 1) >/dev/null;snap >$T/l.out 2>&1;l=$?
ok "o2b-a-foreign-move-is-a-live-second-writer origin's m1 moved to a commit that is NOT in our history: rc $l, MOVED m1 listed, no QUIET verdict" '[ $l = 2 ]&&grep -q "LIVE second writer" $T/l.out&&grep -q "MOVED $(mintn 1)" $T/l.out&&[ ! -e $P/.agi/sessions/origin-snap/quiet ]'
grid unify --into refs/grid --legacy $SNAP --write >$T/lu.out 2>&1;lu=$?
ok "o2c-a-live-mirror-refuses-the-write unify --write on the mirror without a QUIET verdict: unread rc $lu, no shared ref moved" '[ $lu = 1 ]&&grep -q "is not QUIET" $T/lu.out&&[ "$(refs $NS|wc -l|tr -d " ")" = 5 ]'
cp_ pg;snap >/dev/null 2>&1;$G -C $P push -q origin $NS/$(mintn 3):$NS/$(mintn 3) 2>&1;snap >$T/w.out 2>&1;w=$?
ok "o2d-our-own-push-is-not-a-second-writer origin's m3 (it was BEHIND ours) moved to OUR tip: the push-changed landing: own, not foreign: rc $w, QUIET" '[ $w = 0 ]&&grep -q "0 foreign move(s), 1 landing" $T/w.out&&grep -q "QUIET" $T/w.out'
cp_ ph;mut $P/extensions/agi/bin/grid.py '        if ours and _is_ancestor(root, t, ours):' '        if False:'
snap >/dev/null 2>&1;$G -C $P push -q origin $NS/$(mintn 3):$NS/$(mintn 3) 2>&1;snap >$T/wm.out 2>&1;wm=$?
ok "m-own-push-counted-as-foreign-reads-RED with every move foreign, our own push lands as a LIVE second writer (rc $wm): the lane's own-push row catches it" '[ $wm = 2 ]'
cp_ pi;snap >/dev/null 2>&1;y=$(mk $P 5 active forced-rewind $(mk $P 5 active other-root));$G -C $P push -q -f $REM $y:refs/grid/node/$(mintn 5) 2>&1;snap >$T/f.out 2>&1;f2=$?
ok "o1c-a-rewritten-origin-tip-still-fetches-and-reads-live the remote force-moved m5 (a non-fast-forward for the mirror): the forced fetch lands it, and it is a LIVE second writer rc $f2" '[ $f2 = 2 ]&&grep -q "MOVED $(mintn 5)" $T/f.out'
cp_ pj;mut $P/extensions/agi/bin/grid.py '"fetch", "--no-tags", "--prune", "-q", "--refmap=", remote, f"+{ns}/node/*:{ORIGIN_SNAP_NS}/node/*"' '"fetch", "--no-tags", "--prune", "-q", "--refmap=", remote, f"{ns}/node/*:{ORIGIN_SNAP_NS}/node/*"'
snap >/dev/null 2>&1;y=$(mk $P 5 active forced-rewind $(mk $P 5 active other-root));$G -C $P push -q -f $REM $y:refs/grid/node/$(mintn 5) 2>&1;snap >$T/fm.out 2>&1;fm=$?
ok "m-unforced-fetch-reads-RED without the + the mirror cannot follow a rewritten origin tip: rc $fm instead of 2" '[ $fm != 2 ]'
# --- o3: the merge
cp_ pk;snap >/dev/null 2>&1;snap >/dev/null 2>&1;refs $NS >$T/k.ns0;grid unify --into refs/grid --legacy $SNAP >$T/kd.out 2>&1;kd=$?;refs $NS >$T/k.ns1
ok "o3a-the-dry-run-counts-and-lists-the-conflict dry run: 1 merged (m4, equal trees), 2 adopted (m2 ahead, m6 origin-only), 2 unchanged (m1, m3), 1 CONFLICT (m5, unequal trees) listed by mint, rc $kd, no ref written: $(grep 'dry-run' $T/kd.out|cut -c1-150)" '[ $kd = 1 ]&&grep -q "1 merged, 2 adopted, 2 unchanged, 1 conflict, 0 unread of 6" $T/kd.out&&grep -q "CONFLICT $(mintn 5)" $T/kd.out&&cmp -s $T/k.ns0 $T/k.ns1'
grid unify --into refs/grid --legacy $SNAP --write >$T/kw.out 2>&1;kw=$?
ok "o3b-the-write-merges-all-it-may-and-leaves-the-conflict the write on the QUIET mirror: same tallies, rc $kw (the conflict stays RED); m5's ref is untouched, m6 now exists ($(refs $NS|wc -l|tr -d ' ') refs)" '[ $kw = 1 ]&&grep -q "1 merged, 2 adopted, 2 unchanged, 1 conflict" $T/kw.out&&[ "$(sha $NS/$(mintn 5))" = "$($G -C $P rev-parse $NS/$(mintn 5))" ]&&[ "$(refs $NS|wc -l|tr -d " ")" = 6 ]&&$G -C $P cat-file -p $NS/$(mintn 5):node.md|grep -q ns5'
ok "o3c-every-origin-version-is-reachable for the 5 mints that took the origin tip in: the origin tip is an ancestor of ours (m1..m4, m6); m5's origin tip is NOT (the conflict kept it out)" 'for i in 1 2 3 4 6;do $G -C $P merge-base --is-ancestor $(sha $SNAP/node/$(mintn $i)) $(sha $NS/$(mintn $i))||exit 1;done;! $G -C $P merge-base --is-ancestor $(sha $SNAP/node/$(mintn 5)) $(sha $NS/$(mintn 5))'
grid unify --into refs/grid --legacy $SNAP --write >$T/kw2.out 2>&1;refs $NS >$T/k.ns2
ok "o3d-idempotent a second write merges nothing more: $(grep 'write' $T/kw2.out|cut -c1-140)" 'grep -q "0 merged, 0 adopted, 5 unchanged, 1 conflict" $T/kw2.out'
cp_ pl;mut $P/extensions/agi/bin/grid.py '    if lns == ORIGIN_SNAP_NS and git(root, "rev-parse", f"{ltip}^{{tree}}", check=False) != git(' '    if False and git(root, "rev-parse", f"{ltip}^{{tree}}", check=False) != git('
snap >/dev/null 2>&1;snap >/dev/null 2>&1;grid unify --into refs/grid --legacy $SNAP --write >$T/ml.out 2>&1
ok "m-tree-pick-reads-RED with the equal-tree rule cut, m5 (unequal trees) is merged automatically: the ORIGIN tree wins silently ($(grep -c "^  CONFLICT" $T/ml.out) conflicts listed, want 0 = RED)" '! grep -q "^  CONFLICT" $T/ml.out'
cp_ pm;mut $P/extensions/agi/bin/grid.py '    if write and ORIGIN_SNAP_NS in listing:' '    if False and ORIGIN_SNAP_NS in listing:'
snap >/dev/null 2>&1;x=$(mk $P 1 active foreign-edit $(sha $NS/$(mintn 1)));push $x $(mintn 1) >/dev/null;snap >/dev/null 2>&1;grid unify --into refs/grid --legacy $SNAP --write >$T/mg.out 2>&1
ok "m-gate-cut-reads-RED with the QUIET gate cut, a LIVE mirror is merged anyway ($(grep -c 'not QUIET' $T/mg.out) refusals, want 0 = RED)" '! grep -q "not QUIET" $T/mg.out'
# --- the three-way name: frozen F, local L, origin O (one name, three tips) and the union check
cp_ pn;x=$(mintn 7);c=$(mk $P 7 active root-7);F=$(mk $P 7 active frozen7 $c);L=$(mk $P 7 active same7 $c);O=$(mk $P 7 active same7 $(mk $P 7 active mid7 $c));$G -C $P update-ref $NS/$x $F;$G -C $P update-ref $LNS/$x $L;push $O $x >/dev/null
l1=$(mk $P 8 active l8);$G -C $P update-ref $LNS/$(mintn 8) $l1
refs $NS >$T/n.before;snap >/dev/null 2>&1;snap >/dev/null 2>&1
grid unify --into refs/grid --legacy refs/grid/local-maxxing --write >$T/n1.out 2>&1;n1=$?
grid unify --into refs/grid --legacy $SNAP --write >$T/n2.out 2>&1;n2=$?
ok "n1-three-histories-keep-every-tip one name in the frozen, local and origin histories: after the local pass then the origin pass the final tip holds F, L and O ($(grep write $T/n1.out|cut -c1-80) | rc $n1/$n2)" 'T7=$(sha $NS/$x);$G -C $P merge-base --is-ancestor $F $T7&&$G -C $P merge-base --is-ancestor $L $T7&&$G -C $P merge-base --is-ancestor $O $T7&&[ "$($G -C $P rev-list --merges --count $T7)" = 2 ]'
grid unify --into refs/grid --legacy $SNAP --write >$T/n3.out 2>&1
ok "n2-the-three-way-merges-once a second origin write adds no merge: $(grep write $T/n3.out|cut -c1-110)" 'T7=$(sha $NS/$x);[ "$($G -C $P rev-list --merges --count $T7)" = 2 ]&&grep -q "0 merged, 0 adopted" $T/n3.out'
grid unify --check --into refs/grid --legacy refs/grid/local-maxxing --legacy $SNAP >$T/n4.out 2>&1;n4=$?
ok "r2-the-check-counts-the-union --check over both namespaces prints the UNION: $(grep union $T/n4.out)" 'grep -q "union of 2 namespaces" $T/n4.out&&[ $n4 = 1 ]'
# (n4 is 1 here: m5 is still a CONFLICT, so the union is 1 short of whole -- the count below proves the arithmetic)
ok "r2b-the-union-is-names-not-the-first-namespace the union is the 8 distinct names (m1..m8; m5 RED): $(grep union $T/n4.out|grep -o '[0-9]*/[0-9]*')" 'grep -q "unified 7/8 (union" $T/n4.out'
cp_ po pn
mut $P/extensions/agi/bin/grid.py '        if len(listing) > 1:    # the UNION of every namespace' '        if False:    # the UNION of every namespace'
grid unify --check --into refs/grid --legacy refs/grid/local-maxxing --legacy $SNAP >$T/n5.out 2>&1
ok "m-first-namespace-only-reads-RED with the union line cut the check prints no union count ($(grep -c union $T/n5.out) lines, want 1)" '! grep -q "union of" $T/n5.out'
# --- the writer and the push never see the mirror
cp_ pq;snap >/dev/null 2>&1;printf 'probe edit\n' >>$P/.agi/nodes/idea/n1.md 2>/dev/null||{ mkdir -p $P/.agi/nodes/idea;nodemd 1 active probe >$P/.agi/nodes/idea/n1.md;};grid commit --all >$T/c.out 2>&1;c=$?
ok "w1-the-writer-is-not-refused-by-the-mirror with refs/grid/origin-snap holding node refs the commit path does not read it as a migrated trunk (rc $c)" '! grep -q "origin-snap" $T/c.out'
cp_ pr;mut $P/extensions/agi/bin/grid.py 'return sorted(ns - set(legacy_namespaces_for(root)) - {ORIGIN_SNAP_NS})' 'return sorted(ns - set(legacy_namespaces_for(root)))'
snap >/dev/null 2>&1;mkdir -p $P/.agi/nodes/idea;nodemd 1 active probe >$P/.agi/nodes/idea/n1.md;grid commit --all >$T/cm.out 2>&1
ok "m-mirror-not-exempt-reads-RED without the exemption the writer refuses by name because the mirror looks like a migrated trunk" 'grep -q "origin-snap" $T/cm.out'
cp_ ps;snap >/dev/null 2>&1;rm -rf $T/push.git;$G init -q --bare $T/push.git;$G -C $P remote set-url origin $T/push.git;grid push-changed >$T/p.out 2>&1
ok "p1-push-changed-never-lists-the-mirror after a snapshot, push-changed sends no refs/grid/origin-snap ref ($($G -C $P ls-remote origin 'refs/grid/*'|wc -l|tr -d ' ') refs there)" '! $G -C $P ls-remote origin "refs/grid/*"|grep -q origin-snap'
# --- R2/R3 (council 10:50:48Z 10-26): "never pushed" is TRUE. A wide `refs/grid/*:refs/grid/*` spans slashes, so `grid.py sync` carried the private mirror and the
# read-only legacy namespaces to origin too (measured, git 2.43.0); the push specs are node/ + session/ only.
cp_ ps;snap >/dev/null 2>&1;m1=$(sha $NS/$(mintn 1));$G -C $P update-ref refs/grid/session/s1 $m1;$G -C $P update-ref refs/grid/local-maxxing/node/$(mintn 1) $m1;$G -C $P update-ref refs/grid/legacy-x/node/$(mintn 1) $m1
rm -rf $T/sync.git;$G init -q --bare $T/sync.git;grid sync $T/sync.git >$T/sy.out 2>&1;sy=$?
lsr(){ $G -C $T/sync.git for-each-ref --format='%(refname)' "$@"|wc -l|tr -d ' ';}
ok "s1-sync-pushes-node-and-session-only grid.py sync <bare> (rc $sy): node/ $(lsr refs/grid/node) + session/ $(lsr refs/grid/session) at the remote; origin-snap/ $(lsr refs/grid/origin-snap) legacy local-maxxing/ $(lsr refs/grid/local-maxxing) legacy-x/ $(lsr refs/grid/legacy-x) (want 0 0 0)" '[ $sy = 0 ]&&[ "$(lsr refs/grid/node)" = 5 ]&&[ "$(lsr refs/grid/session)" = 1 ]&&[ "$(lsr refs/grid/origin-snap)" = 0 ]&&[ "$(lsr refs/grid/local-maxxing)" = 0 ]&&[ "$(lsr refs/grid/legacy-x)" = 0 ]'
cp_ pt;mut $P/extensions/agi/bin/grid.py '    return [f"{ns}/{k}/*:{ns}/{k}/*" for k in PUSH_KINDS]' '    return [f"{ns}/*:{ns}/*"]'
snap >/dev/null 2>&1;m1=$(sha $NS/$(mintn 1));$G -C $P update-ref refs/grid/local-maxxing/node/$(mintn 1) $m1;rm -rf $T/sync2.git;$G init -q --bare $T/sync2.git;grid sync $T/sync2.git >/dev/null 2>&1
ok "m-wide-push-spec-reads-RED with the one wide <ns>/* spec the mirror and the legacy namespace land at the remote (origin-snap/ $($G -C $T/sync2.git for-each-ref refs/grid/origin-snap|wc -l|tr -d ' '), local-maxxing/ $($G -C $T/sync2.git for-each-ref refs/grid/local-maxxing|wc -l|tr -d ' '); want 6 and 1 = RED)" '[ "$($G -C $T/sync2.git for-each-ref refs/grid/origin-snap|wc -l|tr -d " ")" != 0 ]'
# --- F1 (alive 12:15Z 10-26, reproduced on git 2.43.0): the snapshot fetch must not touch the LIVE namespace. `grid.py init` writes remote.origin.fetch =
# FETCH_SPECS (no +), and a command-line refspec ALSO runs through it unless `--refmap=` empties the map: the O1 fetch then fast-forwarded a live name that was
# behind origin (m2) and was rejected (rc 1) on a diverged one (m5). Two O1 runs (the QUIET path), the live listing byte-identical before and after both.
cp_ pw;for sp in "$NS/*:$NS/*" "refs/grid/session/*:refs/grid/session/*";do $G -C $P config --add remote.origin.fetch "$sp";done;refs "refs/grid/node" >$T/w.live0
snap >$T/fm1.out 2>&1;fm1=$?;snap >$T/fm2.out 2>&1;fm2=$?;refs "refs/grid/node" >$T/w.live1
ok "f1-the-snapshot-fetch-leaves-the-live-namespace-alone origin carries FETCH_SPECS, m2 is behind origin and m5 diverged: two O1 runs rc $fm1/$fm2 (0 = no fetch error), the live refs/grid/node listing byte-identical before and after, the mirror holds 6" '[ $fm1 = 0 ]&&[ $fm2 = 0 ]&&[ -n "$(cat $T/w.live0)" ]&&cmp -s $T/w.live0 $T/w.live1&&[ "$(refs $SNAP/node|wc -l|tr -d " ")" = 6 ]'
cp_ px;for sp in "$NS/*:$NS/*" "refs/grid/session/*:refs/grid/session/*";do $G -C $P config --add remote.origin.fetch "$sp";done;refs "refs/grid/node" >$T/x.live0
mut $P/extensions/agi/bin/grid.py '"--prune", "-q", "--refmap=", remote, f"+{ns}/node/*' '"--prune", "-q", remote, f"+{ns}/node/*'
snap >$T/fx1.out 2>&1;fx1=$?;snap >$T/fx2.out 2>&1;fx2=$?;refs "refs/grid/node" >$T/x.live1
ok "m-refmap-dropped-reads-RED without --refmap= the same two runs rc $fx1/$fx2 and the live listing $(cmp -s $T/x.live0 $T/x.live1 && echo unchanged || echo CHANGED) (want a changed listing or a non-zero rc = RED)" '! { [ $fx1 = 0 ]&&[ $fx2 = 0 ]&&cmp -s $T/x.live0 $T/x.live1; }'
# --- the snapshot is pruned: a name origin deleted leaves the mirror and reads as a write
cp_ pu;snap >/dev/null 2>&1;$G -C $P push -q origin :refs/grid/node/$(mintn 6) 2>&1;snap >$T/pr.out 2>&1;pr=$?
ok "pr1-a-name-origin-deleted-is-a-write origin dropped m6: the pruned mirror no longer lists it, 'name(s) origin no longer lists' counts it, rc $pr (LIVE second writer), and no QUIET verdict" '[ $pr = 2 ]&&[ -z "$(refs $SNAP/node/$(mintn 6))" ]&&grep -q "1 name(s) origin no longer lists" $T/pr.out&&[ ! -e $P/.agi/sessions/origin-snap/quiet ]'
cp_ pv;mut $P/extensions/agi/bin/grid.py '"fetch", "--no-tags", "--prune", "-q", "--refmap=", remote' '"fetch", "--no-tags", "-q", "--refmap=", remote'
snap >/dev/null 2>&1;$G -C $P push -q origin :refs/grid/node/$(mintn 6) 2>&1;snap >$T/pm.out 2>&1;pm=$?
ok "m-no-prune-reads-RED without --prune the deleted name stays in the mirror (the mirror still lists m6: $(refs $SNAP/node/$(mintn 6)|wc -l|tr -d ' ') ref) and unify could still adopt it" '[ -n "$(refs $SNAP/node/$(mintn 6))" ]'
# --- U (goal:g7.16.1.11.46.16, council 14:21:47Z; condition (2) REPLACED by a BYTE TEST in alive's [correction] 14:53:03Z 10-26): a diverged origin pair with NO merge-base is a 2-parent commit,
# tree = LIVE, ONLY when EVERY blob of origin's tip tree was SEEN at its own path class: node.md in live's own history or at a .agi/nodes path of the trunk (HEAD here); payload in live's own history
# or at the node's payload_ref path of the trunk. Anything else is a CONFLICT (BANKED when it failed on unseen bytes). No date compare survives. Dates are set per mint (GIT_COMMITTER_DATE).
#  m21 trunk-seen | m22 live-seen | m23 absent, origin NEWER than live's root (sp) | m24 absent, origin OLDER than live's root (all-is-one) | m25 trunk-seen whose ORIGIN tree carries a /home literal
#  m31 trunk-seen ONLY through a merge resolution (alive 16:50Z C2: the walks take -m) | m30 trunk-seen whose LIVE tip already carries a /home literal (tree = LIVE, so --check must read GREEN) | m26 has a merge-base, blob in live | m27 blob on the trunk only OUTSIDE .agi/nodes (alive) | m28 payload on the trunk only at ANOTHER path (sp) | m29 payload at its payload_ref path -> trunk-seen
mkd(){ dt=$1;shift;GIT_COMMITTER_DATE="$dt" GIT_AUTHOR_DATE="$dt" mk "$@";}
nodemdb(){ printf -- '---\nid: build:n%s\nmint_id: %s\ntype: build\nstatus: %s\nparents:\n  - mvp:m\npayload_ref: %s\n---\nbody %s\n' $1 $(mintn $1) $2 "$4" "$3";}
mkp(){ dt=$1;d=$2;n=$3;st=$4;tx=$5;ref=$6;pay=$7;shift 7;b=$(nodemdb $n $st "$tx" $ref|$G -C $d hash-object -w --stdin);pb=$(printf '%s' "$pay"|$G -C $d hash-object -w --stdin);t=$(printf '100644 blob %s\tnode.md\n100644 blob %s\tpayload\n' $b $pb|$G -C $d mktree);pa=;for x;do pa="$pa -p $x";done;echo "$tx"|GIT_COMMITTER_DATE="$dt" GIT_AUTHOR_DATE="$dt" $G -C $d commit-tree $t $pa;}
trk(){ mkdir -p $P/$(dirname $1);cat >$P/$1;}      # a file on the TRUNK (HEAD): `trk <path> < bytes`
mkun(){ cp_ $1 base
 r=$(mkd 2026-10-20T00:00:00Z $P 21 active liveroot21);t=$(mkd 2026-10-21T00:00:00Z $P 21 active livetip21 $r);$G -C $P update-ref $NS/$(mintn 21) $t;push $(mkd 2020-01-01T00:00:00Z $P 21 active origin21) $(mintn 21) >/dev/null;nodemd 21 active origin21|trk .agi/nodes/idea/t21.md
 r=$(mkd 2020-01-01T00:00:00Z $P 22 active same22);t=$(mkd 2021-01-01T00:00:00Z $P 22 active livetip22 $r);$G -C $P update-ref $NS/$(mintn 22) $t;push $(mkd 2026-10-22T00:00:00Z $P 22 active same22) $(mintn 22) >/dev/null
 r=$(mkd 2020-01-01T00:00:00Z $P 23 active liveroot23);t=$(mkd 2026-10-21T00:00:00Z $P 23 active livetip23 $r);$G -C $P update-ref $NS/$(mintn 23) $t;push $(mkd 2023-01-01T00:00:00Z $P 23 active origin23) $(mintn 23) >/dev/null
 r=$(mkd 2026-10-20T00:00:00Z $P 24 active liveroot24);t=$(mkd 2026-10-21T00:00:00Z $P 24 active livetip24 $r);$G -C $P update-ref $NS/$(mintn 24) $t;push $(mkd 2020-01-01T00:00:00Z $P 24 active origin24) $(mintn 24) >/dev/null
 r=$(mkd 2026-10-20T00:00:00Z $P 25 active liveroot25);t=$(mkd 2026-10-21T00:00:00Z $P 25 active livetip25 $r);$G -C $P update-ref $NS/$(mintn 25) $t;push $(mkd 2020-01-01T00:00:00Z $P 25 active /home/ubuntu/secret25) $(mintn 25) >/dev/null;nodemd 25 active /home/ubuntu/secret25|trk .agi/nodes/idea/t25.md
 r=$(mkd 2026-10-20T00:00:00Z $P 26 active root26);x=$(mkd 2026-10-21T00:00:00Z $P 26 active same26 $r);t=$(mkd 2026-10-22T00:00:00Z $P 26 active livetip26 $x);$G -C $P update-ref $NS/$(mintn 26) $t;push $(mkd 2026-10-21T00:00:01Z $P 26 active same26 $r) $(mintn 26) >/dev/null
 r=$(mkd 2026-10-20T00:00:00Z $P 27 active liveroot27);t=$(mkd 2026-10-21T00:00:00Z $P 27 active livetip27 $r);$G -C $P update-ref $NS/$(mintn 27) $t;push $(mkd 2020-01-01T00:00:00Z $P 27 active origin27) $(mintn 27) >/dev/null;nodemd 27 active origin27|trk other/y27.md
 r=$(mkp 2026-10-20T00:00:00Z $P 28 active livetext28 src/p28.txt LIVEPAY28);push $(mkp 2020-01-01T00:00:00Z $P 28 active origin28 src/p28.txt PAY28) $(mintn 28) >/dev/null;$G -C $P update-ref $NS/$(mintn 28) $r;nodemdb 28 active origin28 src/p28.txt|trk .agi/nodes/idea/t28.md;printf PAY28|trk src/other28.txt
 r=$(mkp 2026-10-20T00:00:00Z $P 29 active livetext29 .cfg/p29.txt LIVEPAY29);push $(mkp 2020-01-01T00:00:00Z $P 29 active origin29 .cfg/p29.txt PAY29) $(mintn 29) >/dev/null;$G -C $P update-ref $NS/$(mintn 29) $r;nodemdb 29 active origin29 .cfg/p29.txt|trk .agi/nodes/idea/t29.md;printf PAY29|trk .cfg/p29.txt
 r=$(mkd 2026-10-20T00:00:00Z $P 30 active "liveroot30 /home/ubuntu/live30");t=$(mkd 2026-10-21T00:00:00Z $P 30 active "livetip30 /home/ubuntu/live30" $r);$G -C $P update-ref $NS/$(mintn 30) $t;push $(mkd 2020-01-01T00:00:00Z $P 30 active origin30) $(mintn 30) >/dev/null;nodemd 30 active origin30|trk .agi/nodes/idea/t30.md
 r=$(mkd 2026-10-20T00:00:00Z $P 31 active liveroot31);t=$(mkd 2026-10-21T00:00:00Z $P 31 active livetip31 $r);$G -C $P update-ref $NS/$(mintn 31) $t;push $(mkd 2020-01-01T00:00:00Z $P 31 active origin31) $(mintn 31) >/dev/null
 $G -C $P add -A >/dev/null 2>&1;$G -C $P commit -qm "trunk evidence"
 # m31's bytes enter the trunk ONLY in a merge's RESOLUTION (neither parent has the file): S = a side commit, M = merge(HEAD, S) whose tree adds .agi/nodes/idea/t31.md
 h=$($G -C $P rev-parse HEAD);ix=$T/idx.$$;rm -f $ix;GIT_INDEX_FILE=$ix $G -C $P read-tree $h;sd=$(printf 'side\n'|$G -C $P hash-object -w --stdin);GIT_INDEX_FILE=$ix $G -C $P update-index --add --cacheinfo 100644,$sd,side.txt
 st=$(GIT_INDEX_FILE=$ix $G -C $P write-tree);sc=$(echo side|$G -C $P commit-tree $st -p $h);nb=$(nodemd 31 active origin31|$G -C $P hash-object -w --stdin);GIT_INDEX_FILE=$ix $G -C $P update-index --add --cacheinfo 100644,$nb,.agi/nodes/idea/t31.md
 mt=$(GIT_INDEX_FILE=$ix $G -C $P write-tree);mc=$(echo merge|$G -C $P commit-tree $mt -p $h -p $sc);$G -C $P update-ref HEAD $mc;rm -f $ix;}
mkun uA;snap >/dev/null 2>&1;snap >$T/u0.out 2>&1
for i in 21 22 23 24 25 26 27 28 29 30 31 5;do eval "uo_$i=$(sha $SNAP/node/$(mintn $i))";eval "ul_$i=$(sha $NS/$(mintn $i))";done
grid unify --into refs/grid --legacy $SNAP >$T/ud.out 2>&1;ud=$?
ok "u0-the-dry-run-names-the-classes dry run: m4 tree-equal + m21 m22 m25 m29 m30 m31 merge, m5 m23 m24 m26 m27 m28 CONFLICT (rc $ud), nothing written: $(grep 'classes\|trunk blob set:' $T/ud.out|cut -c1-190|tr '\n' '|')" '[ $ud = 1 ]&&grep -q "7 merged, 2 adopted, 2 unchanged, 6 conflict, 0 unread of 17" $T/ud.out&&grep -q "classes: tree-equal 1, unrelated-root tree=live 6 (origin bytes in live.s history 1, in the trunk.s 5), banked 4" $T/ud.out&&grep -q "trunk blob set: [0-9]* blobs at .agi/nodes paths of HEAD, one walk" $T/ud.out&&[ "$(sha $NS/$(mintn 21))" = "$ul_21" ]'
grid unify --into refs/grid --legacy $SNAP --write >$T/uw.out 2>&1;uw=$?
um(){ $G -C $P log -1 --format="$2" $(sha $NS/$(mintn $1));}
tl(){ [ "$($G -C $P rev-parse $(sha $NS/$(mintn $1))^{tree})" = "$($G -C $P rev-parse $2^{tree})" ];}
ok "u1-trunk-seen-bytes-merge-as-a-two-parent-commit-with-the-live-tree m21 (origin node.md only at a trunk .agi/nodes path): rc $uw, parents = live tip then origin tip, tree = LIVE's, trailers name the class" '[ "$(um 21 %P)" = "$ul_21 $uo_21" ]&&tl 21 $ul_21&&$G -C $P log -1 --format=%B $(sha $NS/$(mintn 21))|grep -q "Unify-Class: unrelated-root/trunk-seen"&&$G -C $P log -1 --format=%B $(sha $NS/$(mintn 21))|grep -q "Unify-Unrelated: $uo_21"'
ok "u2-live-seen-bytes-merge-the-same-way m22 (origin node.md = live's own root blob): tree = LIVE's, class live-seen" '[ "$(um 22 %P)" = "$ul_22 $uo_22" ]&&tl 22 $ul_22&&$G -C $P log -1 --format=%B $(sha $NS/$(mintn 22))|grep -q "unrelated-root/live-seen"'
ok "u3-unseen-bytes-stay-CONFLICT-whatever-the-date m23 (origin NEWER than live's root) and m24 (origin OLDER than live's root, the root-date test would admit it): untouched, listed by mint" '[ "$(sha $NS/$(mintn 23))" = "$ul_23" ]&&[ "$(sha $NS/$(mintn 24))" = "$ul_24" ]&&grep -q "CONFLICT $(mintn 23)" $T/uw.out&&grep -q "CONFLICT $(mintn 24)" $T/uw.out'
ok "u4-a-pair-WITH-a-merge-base-stays-CONFLICT m5 (unequal trees, a common root) and m26 (the same, and its origin blob IS in live): untouched" '[ "$(sha $NS/$(mintn 5))" = "$ul_5" ]&&[ "$(sha $NS/$(mintn 26))" = "$ul_26" ]&&grep -q "CONFLICT $(mintn 26)" $T/uw.out'
ok "u5-no-written-tip-carries-the-origin-home-path m25 (trunk-seen, origin tree has /home/ubuntu/...): the merge holds LIVE bytes, 0 home-path literals in the written tip" '[ "$(um 25 %P)" = "$ul_25 $uo_25" ]&&! $G -C $P grep -q -E "/home/[A-Za-z0-9._-]+" $(sha $NS/$(mintn 25))'
ok "u6-a-blob-on-the-trunk-only-outside-nodes-stays-CONFLICT m27 (origin node.md bytes exist on the trunk only at other/y27.md): untouched (alive's row)" '[ "$(sha $NS/$(mintn 27))" = "$ul_27" ]&&grep -q "CONFLICT $(mintn 27)" $T/uw.out'
ok "u7-a-payload-is-judged-at-its-payload_ref-path m28 (payload on the trunk only at src/other28.txt, not its payload_ref src/p28.txt) stays CONFLICT; m29 (payload at .cfg/p29.txt) merges as trunk-seen" '[ "$(sha $NS/$(mintn 28))" = "$ul_28" ]&&[ "$(um 29 %P)" = "$ul_29 $uo_29" ]&&tl 29 $ul_29&&grep -q "CONFLICT $(mintn 28)" $T/uw.out'
ok "u7b-a-blob-that-entered-the-trunk-only-in-a-merge-resolution-is-trunk-seen m31 (its node.md exists on the trunk ONLY in M, the merge's resolution; no parent has it): written as trunk-seen, tree = LIVE's (alive 16:50Z C2)" '[ "$(um 31 %P)" = "$ul_31 $uo_31" ]&&tl 31 $ul_31&&$G -C $P log -1 --format=%B $(sha $NS/$(mintn 31))|grep -q "unrelated-root/trunk-seen"'
R=$(ls $P/.agi/sessions/unify/*.classes);B=$(ls $P/.agi/sessions/unify/*.batch)
ok "u8-the-record-lists-every-mint-by-class-and-the-batch-carries-the-diffs $(cut -d" " -f1 $R|sort|uniq -c|tr -s " \n" " "|cut -c1-140)" '[ "$(wc -l <$R|tr -d " ")" = 11 ]&&grep -q "^unrelated-root/trunk-seen $(mintn 21) $uo_21 " $R&&grep -q "^banked $(mintn 23) $uo_23 bytes unseen: node.md" $R&&grep -q "^banked $(mintn 28) $uo_28 bytes unseen: payload@src/p28.txt" $R&&[ "$(grep -c "^== " $B)" = 4 ]&&grep -q "^   +body origin23" $B&&grep -q "record " $T/uw.out'
grid unify --check --into refs/grid --legacy $SNAP >$T/uc.out 2>&1;uc=$?
ok "u9-check-prints-the-same-class-line-and-an-anonymize-count --check: $(grep -E 'classes|anonymize' $T/uc.out|cut -c1-190|tr '\n' '|'); the six CONFLICT mints are its only REDs (m30, whose LIVE tip already carries a home literal, is GREEN), rc $uc" '[ $uc = 1 ]&&grep -q "classes: tree-equal 1, unrelated-root tree=live 6 (origin bytes in live.s history 1, in the trunk.s 5), banked 4" $T/uc.out&&grep -q "anonymize over the written tips: 0 carry" $T/uc.out&&[ "$(grep -c "^  RED" $T/uc.out)" = 6 ]&&! grep -q "RED $(mintn 30)" $T/uc.out&&[ "$(um 30 %P|wc -w|tr -d " ")" = 2 ]'
# --- OB (the owner's ruling 10-27, goal:g7.16.1.11.46.16 route (a)): `unify --owner-batch <record>` writes every BANKED pair of ONE stamped record as tree = LIVE,
# first parent the live tip, origin's tip the 2nd: the push is a fast-forward of origin's ref (never a force), origin's version stays in the history and in a stamped .batch
RN=$(basename $R);UD=$P/.agi/sessions/unify
# goal:g7.16.1.11.46.16.2 R1: a record is writable only when a ruling NODE BY NAME, COMMITTED at the trunk, names it (one anchored line)
rl(){ printf '%s sha256:%s' "$1" "$(sha256sum $P/.agi/sessions/unify/$1 2>/dev/null|cut -c1-64)";}
rule(){ mkdir -p $P/.agi/nodes/doc;printf -- '---\nid: doc:owner-ruling-%s\n---\n%s: %s\n' "$(echo $1|tr . -)" owner-batch-ruling "$(rl $1)" >$P/.agi/nodes/doc/owner-ruling-$(echo $1|tr . -).md;$G -C $P add .agi/nodes/doc >/dev/null 2>&1;$G -C $P commit -qm "ruling $1" >/dev/null;}
rule $RN
obw(){ for i in 23 24 27 28;do eval l=\$ul_$i o=\$uo_$i;w=$(sha $NS/$(mintn $i));[ "$(um $i %P)" = "$l $o" ]&&tl $i $l&&$G -C $P log -1 --format=%B $w|grep -q "^Unify-Owner: $o$"&&$G -C $P merge-base --is-ancestor $o $w||return 1;done;}
grid unify --into refs/grid --legacy $SNAP --owner-batch $RN >$T/ob0.out 2>&1;ob0=$?
ok "ob0-the-selector-runs-dry the record's 4 banked pairs (m23 m24 m27 m28) are selected, nothing written: $(grep 'selected' $T/ob0.out|cut -c1-190) rc $ob0" '[ $ob0 = 0 ]&&grep -q "selected 4 banked pair(s): 4 merged, 0 unchanged, 0 conflict, 0 unread" $T/ob0.out&&[ "$(sha $NS/$(mintn 23))" = "$ul_23" ]&&[ "$(sha $NS/$(mintn 28))" = "$ul_28" ]'
grid unify --into refs/grid --legacy $SNAP --owner-batch $RN --write >$T/ob1.out 2>&1;ob1=$?
ok "ob1-every-banked-pair-is-written-tree-LIVE-origin-second m23 m24 m27 m28: parents = live tip then origin tip, tree = LIVE's, Unify-Owner names origin's tip; m5 m26 (merge-base pairs, never banked) untouched, rc $ob1" '[ $ob1 = 0 ]&&obw&&[ "$(sha $NS/$(mintn 5))" = "$ul_5" ]&&[ "$(sha $NS/$(mintn 26))" = "$ul_26" ]'
$G -C $P push --porcelain $REM $(for i in 23 24 27 28;do printf '%s ' $NS/$(mintn $i):$NS/$(mintn $i);done) >$T/ob2.out 2>&1;ob2=$?
ok "ob2-the-push-is-a-fast-forward a plain push (no force) of the 4 written refs to the remote still at origin's tips: rc $ob2, $(grep -c '^!' $T/ob2.out) rejected" '[ $ob2 = 0 ]&&[ "$(grep -c "^!" $T/ob2.out)" = 0 ]&&[ "$(grep -c "^ " $T/ob2.out)" = 4 ]'
OR=$(ls -t $UD/*.classes|head -1);OB=${OR%.classes}.batch
ok "ob3-the-stamped-record-keeps-origins-version $(basename $OR): 4 owner-batch/live rows, its .batch has origin's node.md diff per mint" '[ "$OR" != "$R" ]&&[ "$(grep -c "^owner-batch/live " $OR)" = 4 ]&&grep -q "^owner-batch/live $(mintn 23) $uo_23 $(sha $NS/$(mintn 23))$" $OR&&[ "$(grep -c "^== " $OB)" = 4 ]&&grep -q "^   +body origin23" $OB&&grep -q "owner rule: tree = LIVE" $OB'
n0=$(ls $UD/*.classes|wc -l);grid unify --into refs/grid --legacy $SNAP --owner-batch $RN --write >$T/ob4.out 2>&1;ob4=$?
ok "ob4-a-second-write-moves-nothing rc $ob4: $(grep 'selected' $T/ob4.out|cut -c1-160), no new record" '[ $ob4 = 0 ]&&grep -q "0 merged, 4 unchanged, 0 conflict, 0 unread" $T/ob4.out&&[ "$(ls $UD/*.classes|wc -l)" = $n0 ]&&obw'
grid unify --check --into refs/grid --legacy $SNAP >$T/ob5.out 2>&1;ob5=$?
ok "ob5-check-reads-the-owner-merges-GREEN --check: the only REDs are m5 m26 (merge-base pairs nobody ruled): $(grep -c '^  RED' $T/ob5.out) RED, $(grep classes $T/ob5.out|cut -c1-170)" '[ $ob5 = 1 ]&&[ "$(grep -c "^  RED" $T/ob5.out)" = 2 ]&&grep -q "RED $(mintn 5) " $T/ob5.out&&grep -q "RED $(mintn 26) " $T/ob5.out&&grep -q "owner-batch tree=live 4" $T/ob5.out'
printf 'banked %s %s bytes unseen: node.md\nbanked %s %s bytes unseen: node.md\n' $(mintn 99) $uo_23 $(mintn 24) $uo_21 >$UD/zz-ob-unread.classes;rule zz-ob-unread.classes
grid unify --into refs/grid --legacy $SNAP --owner-batch zz-ob-unread.classes --write >$T/ob6.out 2>&1;ob6=$?
ok "ob6-an-unreadable-pair-is-named-never-skipped a record banking m99 (no ref) and m24 at a tip origin does not hold: rc $ob6, UNREAD m99 and CONFLICT m24 (origin moved) named, nothing written" '[ $ob6 = 1 ]&&grep -q "UNREAD $(mintn 99) " $T/ob6.out&&grep -q "CONFLICT $(mintn 24) (origin moved" $T/ob6.out&&grep -q "0 merged, 0 unchanged, 1 conflict, 1 unread" $T/ob6.out&&obw'
grid unify --into refs/grid --legacy $SNAP --owner-batch no-such.classes >$T/ob7.out 2>&1;ob7=$?
ok "ob7-a-record-that-is-not-there-is-unread rc $ob7: $(cut -c1-120 $T/ob7.out)" '[ $ob7 = 1 ]&&grep -q "unread (--owner-batch names no stamped record" $T/ob7.out'
x=$(sha $NS/$(mintn 26));w=$($G -C $P commit-tree $x^{tree} -p $x -p $uo_26 -m "unify vX forged

Unify-Owner: $uo_26
Unify-Class: owner-batch/live");$G -C $P update-ref $NS/$(mintn 26) $w $x
grid unify --check --into refs/grid --legacy $SNAP >$T/ob8.out 2>&1
ok "ob8-an-owner-merge-no-record-names-is-RED m26 hand-written with an Unify-Owner trailer (never banked, no owner-batch row): --check names it" 'grep -q "RED $(mintn 26) (an owner-batch merge no stamped owner-batch record names)" $T/ob8.out'
# --- OB re-cut (sp 20:28:34Z, aio 20:28:58Z): (a) origin's version SAVED whole: the .batch is `git diff live origin` over EVERY path, uncapped;
# (b) each pair stamped right after its compare-and-swap (a run that dies between two pairs leaves the written one recorded); (c) an unreadable diff is ONE named line
big40(){ r=$(mkd 2026-10-20T00:00:00Z $P 40 active live40);$G -C $P update-ref $NS/$(mintn 40) $r;push $(mkd 2020-01-01T00:00:00Z $P 40 active "$(seq 1 200|sed 's/^/origin line /')") $(mintn 40) >/dev/null;snap >/dev/null 2>&1;snap >/dev/null 2>&1
 printf 'banked %s %s bytes unseen: payload@src/p28.txt\nbanked %s %s bytes unseen: node.md\n' $(mintn 28) $(sha $SNAP/node/$(mintn 28)) $(mintn 40) $(sha $SNAP/node/$(mintn 40)) >$P/.agi/sessions/unify/zz-ob-a.classes;rule zz-ob-a.classes;}
oba(){ mkun $1;shift;while [ $# -ge 2 ];do mut $P/extensions/agi/bin/grid.py "$1" "$2";shift 2;done;snap >/dev/null 2>&1;snap >/dev/null 2>&1;grid unify --into refs/grid --legacy $SNAP --write >/dev/null 2>&1;big40
 grid unify --into refs/grid --legacy $SNAP --owner-batch zz-ob-a.classes --write >$T/oba.out 2>&1;echo $? >$T/oba.rc;OBA=$(ls -t $P/.agi/sessions/unify/*.batch|head -1);}
oba uOA
ok "ob9-the-batch-saves-origins-version-whole m28 (origin differs in its PAYLOAD too) and m40 (a 200-line origin node.md, past the old 150-line cap): rc $(cat $T/oba.rc), the .batch carries origin's payload line and its 200th line" '[ "$(cat $T/oba.rc)" = 0 ]&&grep -q "^   +PAY28" $OBA&&grep -q "^   +origin line 200$" $OBA&&grep -q "^== $(mintn 40) " $OBA'
gx(){ (cd $P&&FAULT=$1 python3 - "$@" <<'PY'
import os,subprocess,sys
sys.path.insert(0,"extensions/agi/bin")
import grid
f=os.environ["FAULT"];n=[0]
real_cas,real_gt=grid._cas,grid.git_try
def cas(*a):
    n[0]+=1
    if f=="die" and n[0]==2: raise SystemExit(9)      # the run dies between the 1st and 2nd pair's write
    return real_cas(*a)
def gt(root,*a,**k):
    if f=="diffunread" and a and a[0]=="diff": return subprocess.CompletedProcess(a,128,"","fatal: simulated unreadable object\n")
    if f=="buildfail" and a and a[0]=="commit-tree": return subprocess.CompletedProcess(a,128,"","fatal: simulated unbuildable merge\n")
    return real_gt(root,*a,**k)
grid._cas,grid.git_try=cas,gt
if f=="diestamp":
    def add(*a): raise SystemExit(9)     # the run dies AFTER the 1st compare-and-swap, BEFORE its stamp
    grid._OwnerStamp.add=add
sys.argv=["grid.py"]+sys.argv[2:]
grid.main()
PY
);}
obd(){ mkun $1;shift;while [ $# -ge 2 ];do mut $P/extensions/agi/bin/grid.py "$1" "$2";shift 2;done;snap >/dev/null 2>&1;snap >/dev/null 2>&1;grid unify --into refs/grid --legacy $SNAP --write >/dev/null 2>&1;RD=$(basename $(ls $P/.agi/sessions/unify/*.classes));rule $RD
 gx die unify --into refs/grid --legacy $SNAP --owner-batch $RD --write >$T/obd.out 2>&1;echo $? >$T/obd.rc;OD=$(ls -t $P/.agi/sessions/unify/*.classes|head -1)
 OW=;for i in 23 24 27 28;do [ "$(um $i %P|wc -w|tr -d ' ')" = 2 ]&&OW="$OW $i";done;}
obd uOD
ok "ob10-a-death-between-two-pairs-leaves-the-written-one-stamped the run dies (rc $(cat $T/obd.rc)) after ONE pair's write: written m$(echo $OW|tr -d ' '), its owner row in $(basename $OD) names its commit" '[ "$(cat $T/obd.rc)" = 9 ]&&[ "$(echo $OW|wc -w|tr -d " ")" = 1 ]&&[ "$OD" != "$P/.agi/sessions/unify/$RD" ]&&grep -q "^owner-batch/live $(mintn $(echo $OW|tr -d " ")) .* $(sha $NS/$(mintn $(echo $OW|tr -d " ")))$" $OD'
grid unify --into refs/grid --legacy $SNAP --owner-batch $RD --write >$T/obd2.out 2>&1;obd2=$?
ok "ob10b-a-re-run-finishes-the-batch rc $obd2: $(grep selected $T/obd2.out|cut -c1-150)" '[ $obd2 = 0 ]&&grep -q "3 merged, 1 unchanged, 0 conflict, 0 unread" $T/obd2.out'
obc(){ mkun $1;shift;while [ $# -ge 2 ];do mut $P/extensions/agi/bin/grid.py "$1" "$2";shift 2;done;snap >/dev/null 2>&1;snap >/dev/null 2>&1;grid unify --into refs/grid --legacy $SNAP --write >/dev/null 2>&1;RC=$(basename $(ls $P/.agi/sessions/unify/*.classes));rule $RC
 gx diffunread unify --into refs/grid --legacy $SNAP --owner-batch $RC --write >$T/obc.out 2>&1;echo $? >$T/obc.rc;OC=$(ls -t $P/.agi/sessions/unify/*.batch|head -1);}
obc uOC
ok "ob11-an-unreadable-diff-is-one-named-line with git diff failing, the 4 pairs are still written (rc $(cat $T/obc.rc)) and each .batch entry holds ONE 'diff unread: <reason>' line, never an empty body" '[ "$(cat $T/obc.rc)" = 0 ]&&[ "$(grep -c "^   diff unread: fatal: simulated unreadable object$" $OC)" = 4 ]&&[ "$(grep -c "^== " $OC)" = 4 ]'
# --- goal:g7.16.1.11.46.16.2: the SCOPE (only a ruled record), the --check chain (each link RED by its own name), and the four 3/3 notes
obr(){ mkun $1;shift;while [ $# -ge 2 ];do mut $P/extensions/agi/bin/grid.py "$1" "$2";shift 2;done;snap >/dev/null 2>&1;snap >/dev/null 2>&1;grid unify --into refs/grid --legacy $SNAP --write >/dev/null 2>&1
 RR=$(basename $(ls $P/.agi/sessions/unify/*.classes));for i in 5 23 26;do eval "uo_$i=$(sha $SNAP/node/$(mintn $i))";done;}
one(){ [ "$(um 23 %P|wc -w|tr -d ' ')" = "$1" ];}
obr uOR
grid unify --into refs/grid --legacy $SNAP --owner-batch $RR --write >$T/r1.out 2>&1;r1=$?
ok "s1-a-record-no-ruling-names-is-unread rc $r1: $(cut -c1-130 $T/r1.out), 0 written" '[ $r1 = 1 ]&&grep -q "no owner ruling names $RR at HEAD" $T/r1.out&&one 1'
printf -- '---\nid: doc:owner-ruling-wt\n---\nowner-batch-ruling: %s\n' "$(rl $RR)" >$P/.agi/nodes/doc/owner-ruling-wt.md 2>/dev/null||{ mkdir -p $P/.agi/nodes/doc;printf -- '---\nid: doc:owner-ruling-wt\n---\nowner-batch-ruling: %s\n' "$(rl $RR)" >$P/.agi/nodes/doc/owner-ruling-wt.md;}
grid unify --into refs/grid --legacy $SNAP --owner-batch $RR --write >$T/r2.out 2>&1;r2=$?
ok "s2-an-UNCOMMITTED-ruling-rules-nothing a ruling node in the working tree only (never committed): rc $r2, unread, 0 written (self-perpetuating 21:35:34Z)" '[ $r2 = 1 ]&&grep -q "no owner ruling names" $T/r2.out&&one 1'
rm -f $P/.agi/nodes/doc/owner-ruling-wt.md;printf -- '---\nid: doc:card-x\n---\nquoted: the line below\nowner-batch-ruling: %s\n' "$(rl $RR)" >$P/.agi/nodes/doc/card-x.md;$G -C $P add .agi/nodes/doc >/dev/null 2>&1;$G -C $P commit -qm "a card quoting the line" >/dev/null
grid unify --into refs/grid --legacy $SNAP --owner-batch $RR --write >$T/r3.out 2>&1;r3=$?
ok "s3-a-card-that-QUOTES-the-line-rules-nothing doc:card-x at the trunk carries the exact line, no ruling node: rc $r3, unread, 0 written (self-perpetuating 21:36:33Z)" '[ $r3 = 1 ]&&grep -q "no owner ruling names" $T/r3.out&&one 1'
printf -- '---\nid: doc:owner-ruling-two\n---\nowner-batch-ruling: %s\nowner-batch-ruling: other.classes sha256:%064d\n' "$(rl $RR)" 0 >$P/.agi/nodes/doc/owner-ruling-two.md;$G -C $P add .agi/nodes/doc >/dev/null 2>&1;$G -C $P commit -qm "a ruling naming two records" >/dev/null
grid unify --into refs/grid --legacy $SNAP --owner-batch $RR --write >$T/r4.out 2>&1;r4=$?
ok "s4-a-ruling-names-ONE-record a ruling node with two ruling lines rules neither: rc $r4, unread, 0 written" '[ $r4 = 1 ]&&grep -q "no owner ruling names" $T/r4.out&&one 1'
mkdir -p $P/.agi/nodes/doc/owner-ruling-a;printf -- '---\nid: doc:owner-ruling-nested\n---\nowner-batch-ruling: %s\n' "$(rl $RR)" >$P/.agi/nodes/doc/owner-ruling-a/b.md;$G -C $P add .agi/nodes/doc >/dev/null 2>&1;$G -C $P commit -qm "a NESTED ruling node" >/dev/null
grid unify --into refs/grid --legacy $SNAP --owner-batch $RR --write >$T/r4b.out 2>&1;r4b=$?
ok "s11-a-NESTED-owner-ruling-a/b.md-rules-nothing (the gate's :(glob) never matches it, so the reader must not either; sp 22:42:55Z): rc $r4b, unread, 0 written" '[ $r4b = 1 ]&&grep -q "no owner ruling names" $T/r4b.out&&one 1'
printf -- '---\nid: doc:owner-ruling-quoted\n---\nquoted:owner-batch-ruling: %s\n' "$(rl $RR)" >$P/.agi/nodes/doc/owner-ruling-quoted.md;$G -C $P add .agi/nodes/doc >/dev/null 2>&1;$G -C $P commit -qm "a ruling node whose only line is a quote" >/dev/null
grid unify --into refs/grid --legacy $SNAP --owner-batch $RR --write >$T/r4c.out 2>&1;r4c=$?
ok "s12-the-line-is-ANCHORED a ruling node whose ONLY line is 'quoted:owner-batch-ruling: RR': rc $r4c, unread, 0 written (sp's crumb)" '[ $r4c = 1 ]&&grep -q "no owner ruling names" $T/r4c.out&&one 1'
printf -- '---\nid: doc:owner-ruling-pin2\n---\nowner-batch-ruling: %s sha256:%064d\n' $RR 0 >$P/.agi/nodes/doc/owner-ruling-pin2.md;rule $RR;grid unify --into refs/grid --legacy $SNAP --owner-batch $RR --write >$T/r4d.out 2>&1;r4d=$?
ok "s4b-two-rulings-pinning-ONE-record-to-DIFFERENT-bytes-rule-nothing (aio's crumb): rc $r4d, $(cut -c1-110 $T/r4d.out), 0 written" '[ $r4d = 1 ]&&grep -q "pin different bytes" $T/r4d.out&&one 1'
$G -C $P rm -q .agi/nodes/doc/owner-ruling-pin2.md;$G -C $P commit -qm "drop the disagreeing ruling" >/dev/null
grid unify --into refs/grid --legacy $SNAP --owner-batch $RR --write >$T/r5.out 2>&1;r5=$?
ok "s5-a-RULED-record-writes rc $r5: $(grep selected $T/r5.out|cut -c1-120)" '[ $r5 = 0 ]&&grep -q "4 merged, 0 unchanged, 0 conflict, 0 unread" $T/r5.out&&one 2'
fg(){ x=$(sha $NS/$(mintn $1));w=$($G -C $P commit-tree $x^{tree} -p $x -p $2 -m "unify vX forged

Unify-Owner: $2
Unify-Class: owner-batch/live
Unify-Record: $3");$G -C $P update-ref $NS/$(mintn $1) $w $x;echo $w;}
w26=$(fg 26 $uo_26 $RR);printf 'owner-batch/live %s %s %s\n' $(mintn 26) $uo_26 $w26 >$P/.agi/sessions/unify/zz-forge.classes
w5=$(fg 5 $uo_5 zz-unruled.classes);printf 'banked %s %s bytes unseen: node.md\nbanked %s %s bytes unseen: node.md\nowner-batch/live %s %s %s\n' $(mintn 5) $uo_5 $(mintn 26) $uo_26 $(mintn 5) $uo_5 $w5 >$P/.agi/sessions/unify/zz-unruled.classes
grid unify --check --into refs/grid --legacy $SNAP >$T/r6.out 2>&1
ok "s6-check-names-each-missing-link m26 (a stamped owner row under the RULED record, its origin tip banked ONLY by ANOTHER (unruled) record: alive's per-record key) and m5 (banked + stamped, a record no ruling names) are RED by their own names; the 4 ruled merges GREEN" 'grep -q "RED $(mintn 26) (an owner-batch merge for an origin tip its record $RR did not bank)" $T/r6.out&&grep -q "RED $(mintn 5) (an owner-batch merge under a record no owner ruling names (zz-unruled.classes))" $T/r6.out&&! grep -q "RED $(mintn 23)" $T/r6.out'
obr uOB;rule $RR;gx buildfail unify --into refs/grid --legacy $SNAP --owner-batch $RR --write >$T/r7.out 2>&1;r7=$?
ok "s7-a-merge-commit-that-cannot-be-built-is-UNREAD-by-its-own-name rc $r7, 4 'could not be built' lines, no 'compare-and-swap' line, 0 written (all-is-one)" '[ $r7 = 1 ]&&[ "$(grep -c "(the merge commit could not be built: fatal: simulated unbuildable merge; nothing written)" $T/r7.out)" = 4 ]&&! grep -q "compare-and-swap" $T/r7.out&&one 1'
obr uOS;rule $RR;gx diestamp unify --into refs/grid --legacy $SNAP --owner-batch $RR --write >$T/r8.out 2>&1;r8=$?;grid unify --check --into refs/grid --legacy $SNAP >$T/r8c.out 2>&1
ok "s8-a-death-between-a-CAS-and-its-stamp-is-RED-at-check the run dies (rc $r8) after m23's compare-and-swap, before its stamp: --check names m23 'no stamped owner-batch record names' (SM)" '[ $r8 = 9 ]&&one 2&&grep -q "RED $(mintn 23) (an owner-batch merge no stamped owner-batch record names)" $T/r8c.out'
obr uOP;rule $RR;grid unify --into refs/grid --legacy $SNAP --owner-batch $RR --write >/dev/null 2>&1;printf 'banked %s %s bytes unseen: node.md\n' $(mintn 5) $uo_5 >>$P/.agi/sessions/unify/$RR
grid unify --into refs/grid --legacy $SNAP --owner-batch $RR --write >$T/r13.out 2>&1;r13=$?;grid unify --check --into refs/grid --legacy $SNAP >$T/r13c.out 2>&1
ok "s13-the-ruling-PINS-the-records-bytes a banked row (m5) appended to the ruled record after the ruling: the writer rc $r13, unread by name, m5 untouched; --check names m23 'not the bytes the owner ruled' (sp 22:48:48Z)" '[ $r13 = 1 ]&&grep -q "is not the bytes the owner ruled" $T/r13.out&&[ "$(um 5 %P|wc -w|tr -d " ")" = 1 ]&&grep -q "RED $(mintn 23) (an owner-batch merge under a record that is not the bytes the owner ruled ($RR))" $T/r13c.out'
obx(){ mkun $1;shift;while [ $# -ge 2 ];do mut $P/extensions/agi/bin/grid.py "$1" "$2";shift 2;done;snap >/dev/null 2>&1;snap >/dev/null 2>&1;grid unify --into refs/grid --legacy $SNAP --write >/dev/null 2>&1
 lb=$(printf '\000\001\002live41\377' |$G -C $P hash-object -w --stdin);ob=$(printf '\000\003\004origin41\376'|$G -C $P hash-object -w --stdin);nm=$(nodemdb 41 active text41 bin/p41 |$G -C $P hash-object -w --stdin)
 lt=$(printf '100644 blob %s\tnode.md\n100644 blob %s\tpayload\n' $nm $lb|$G -C $P mktree);ot=$(printf '100644 blob %s\tnode.md\n100644 blob %s\tpayload\n' $nm $ob|$G -C $P mktree)
 $G -C $P update-ref $NS/$(mintn 41) $(echo l41|GIT_COMMITTER_DATE=2026-10-20T00:00:00Z $G -C $P commit-tree $lt);push $(echo o41|GIT_COMMITTER_DATE=2020-01-01T00:00:00Z $G -C $P commit-tree $ot) $(mintn 41) >/dev/null
 t42=$(printf '100644 blob %s\tnode.md\n' $(nodemd 42 active same42|$G -C $P hash-object -w --stdin)|$G -C $P mktree)
 $G -C $P update-ref $NS/$(mintn 42) $(echo l42|GIT_COMMITTER_DATE=2026-10-20T00:00:00Z $G -C $P commit-tree $t42);push $(echo o42|GIT_COMMITTER_DATE=2020-01-01T00:00:00Z $G -C $P commit-tree $t42) $(mintn 42) >/dev/null;snap >/dev/null 2>&1;snap >/dev/null 2>&1
 printf 'banked %s %s bytes unseen: payload@bin/p41\nbanked %s %s bytes unseen: node.md\n' $(mintn 41) $(sha $SNAP/node/$(mintn 41)) $(mintn 42) $(sha $SNAP/node/$(mintn 42)) >$P/.agi/sessions/unify/zz-ox.classes;rule zz-ox.classes
 grid unify --into refs/grid --legacy $SNAP --owner-batch zz-ox.classes --write >$T/ox.out 2>&1;echo $? >$T/ox.rc;OX=$(ls -t $P/.agi/sessions/unify/*.batch|head -1);}
obx uOX
ok "s9-a-binary-path-is-saved-whole m41's binary payload differs: rc $(cat $T/ox.rc), the .batch carries a 'GIT binary patch' (sp)" '[ "$(cat $T/ox.rc)" = 0 ]&&grep -q "^   GIT binary patch" $OX&&! grep -q "Binary files" $OX'
ok "s10-a-diff-that-prints-nothing-is-named m42 (live already at origin's tree): its .batch entry is ONE 'diff empty: trees equal' line (alive)" 'awk "/^== $(mintn 42) /{f=1;next} /^== /{f=0} f" $OX|grep -c . |grep -qx 2&&awk "/^== $(mintn 42) /{f=1;next} /^== /{f=0} f" $OX|grep -q "^   diff empty: trees equal$"'
obm(){ mkun $1;mut $P/extensions/agi/bin/grid.py "$2" "$3";snap >/dev/null 2>&1;snap >/dev/null 2>&1;grid unify --into refs/grid --legacy $SNAP --write >/dev/null 2>&1
 for i in 23 24 27 28;do eval "uo_$i=$(sha $SNAP/node/$(mintn $i))";eval "ul_$i=$(sha $NS/$(mintn $i))";done
 rule $(basename $(ls $P/.agi/sessions/unify/*.classes));grid unify --into refs/grid --legacy $SNAP --owner-batch $(basename $(ls $P/.agi/sessions/unify/*.classes)) --write >$T/$1.w 2>&1;echo $? >$T/$1.rc;grid unify --check --into refs/grid --legacy $SNAP >$T/$1.c 2>&1;}
# the walk fails -> every pair CONFLICT, ONE named line, nothing written
mkun uF;snap >/dev/null 2>&1;snap >/dev/null 2>&1;ulf=$(sha $NS/$(mintn 22));grid unify --into refs/grid --legacy $SNAP --write --trunk refs/heads/no-such-trunk >$T/uf.out 2>&1;uf=$?
ok "u10-an-unread-trunk-set-fails-closed with the trunk ref unreadable m22 (whose bytes ARE live's own) is NOT merged: rc $uf, the line 'trunk blob set unread' printed $(grep -c 'trunk blob set unread' $T/uf.out) time(s)" '[ $uf = 1 ]&&[ "$(sha $NS/$(mintn 22))" = "$ulf" ]&&[ "$(grep -c "trunk blob set unread" $T/uf.out)" = 1 ]&&[ "$(um 21 %P|wc -w|tr -d " ")" = 1 ]'
# mutants: each must read RED on the fixture above
mkun uB;mut $P/extensions/agi/bin/grid.py '    if absent:
        return None, "bytes unseen: "' '    if absent and not (git_try(root, "log", "-1", "--format=%ct", otip).stdout.strip() < min(git_try(root, "log", "--format=%ct", "--max-parents=0", live).stdout.split())):
        return None, "bytes unseen: "'
snap >/dev/null 2>&1;snap >/dev/null 2>&1;grid unify --into refs/grid --legacy $SNAP --write >/dev/null 2>&1
ok "m-root-date-reads-RED the root-date test in place of the byte test writes m24 (origin 2020 < live root 2026, its bytes seen nowhere): $(um 24 %P|wc -w|tr -d ' ') parents on m24, want 1 = CONFLICT, so 2 = RED" '[ "$(um 24 %P|wc -w|tr -d " ")" = 2 ]'
mkun uC;mut $P/extensions/agi/bin/grid.py '    if absent:
        return None, "bytes unseen: "' '    if absent and not (git_try(root, "log", "-1", "--format=%ct", otip).stdout.strip() < git_try(root, "log", "-1", "--format=%ct", live).stdout.strip()):
        return None, "bytes unseen: "'
snap >/dev/null 2>&1;snap >/dev/null 2>&1;grid unify --into refs/grid --legacy $SNAP --write >/dev/null 2>&1
ok "m-tip-vs-tip-reads-RED comparing origin's tip with live's TIP writes m23 (origin 2023 < live tip 2026, bytes seen nowhere): $(um 23 %P|wc -w|tr -d ' ') parents on m23, so 2 = RED" '[ "$(um 23 %P|wc -w|tr -d " ")" = 2 ]'
mkun uD;mut $P/extensions/agi/bin/grid.py '"--format=", trunk, "--", ".agi/nodes")' '"--format=", trunk)'
snap >/dev/null 2>&1;snap >/dev/null 2>&1;grid unify --into refs/grid --legacy $SNAP --write >/dev/null 2>&1
ok "m-unlimited-set-reads-RED the trunk set taken from EVERY path (not .agi/nodes) writes m27, whose bytes sit only at other/y27.md: $(um 27 %P|wc -w|tr -d ' ') parents on m27, so 2 = RED" '[ "$(um 27 %P|wc -w|tr -d " ")" = 2 ]'
mkun uE;mut $P/extensions/agi/bin/grid.py '"--format=", self.trunk, "--", path)' '"--format=", self.trunk)'
snap >/dev/null 2>&1;snap >/dev/null 2>&1;grid unify --into refs/grid --legacy $SNAP --write >/dev/null 2>&1
ok "m-payload-path-filter-dropped-reads-RED the payload set taken from EVERY path writes m28, whose payload sits only at src/other28.txt: $(um 28 %P|wc -w|tr -d ' ') parents on m28, so 2 = RED" '[ "$(um 28 %P|wc -w|tr -d " ")" = 2 ]'
mkun uM;mut $P/extensions/agi/bin/grid.py '"--no-renames", "-m", "--format=", trunk, "--", ".agi/nodes")' '"--no-renames", "--format=", trunk, "--", ".agi/nodes")'
snap >/dev/null 2>&1;snap >/dev/null 2>&1;grid unify --into refs/grid --legacy $SNAP --write >/dev/null 2>&1
ok "m-merge-resolutions-invisible-reads-RED the trunk walk WITHOUT -m cannot see m31's bytes (only in a merge resolution): $(um 31 %P|wc -w|tr -d ' ') parents on m31, want 2 = trunk-seen, so 1 = CONFLICT = RED" '[ "$(um 31 %P|wc -w|tr -d " ")" = 1 ]'
mkun uG;mut $P/extensions/agi/bin/grid.py '    if mb.returncode == 0 and mb.stdout.strip():
        return None, "has a merge-base"' '    if False:
        return None, "has a merge-base"'
snap >/dev/null 2>&1;snap >/dev/null 2>&1;grid unify --into refs/grid --legacy $SNAP --write >/dev/null 2>&1
ok "m-merge-base-ignored-reads-RED without the no-merge-base condition m26 (a common root, its origin blob in live) is merged: $(um 26 %P|wc -w|tr -d ' ') parents on m26, so 2 = RED" '[ "$(um 26 %P|wc -w|tr -d " ")" = 2 ]'
mkun uH;mut $P/extensions/agi/bin/grid.py '"commit-tree", f"{ntip}^{{tree}}", "-p", ntip, "-p", ltip, "-m", msg)
            if res.returncode != 0 or not _cas(root, nref, res.stdout.strip(), ntip):
                return "conflict"
            if classes is not None:
                classes.append((f"unrelated-root' '"commit-tree", f"{ltip}^{{tree}}", "-p", ntip, "-p", ltip, "-m", msg)
            if res.returncode != 0 or not _cas(root, nref, res.stdout.strip(), ntip):
                return "conflict"
            if classes is not None:
                classes.append((f"unrelated-root'
snap >/dev/null 2>&1;snap >/dev/null 2>&1;grid unify --into refs/grid --legacy $SNAP --write >/dev/null 2>&1;grid unify --check --into refs/grid --legacy $SNAP >$T/uh.out 2>&1
ok "m-origin-tree-picked-reads-RED with tree = ORIGIN's the written m25 tip carries the home-path literal and --check says so: $(grep 'anonymize' $T/uh.out|cut -c1-90)" '! grep -q "anonymize over the written tips: 0 carry" $T/uh.out'
mkun uI;mut $P/extensions/agi/bin/grid.py '        if res.returncode != 0:
            self.problem = f"git log {trunk} -- .agi/nodes failed' '        if False:
            self.problem = f"git log {trunk} -- .agi/nodes failed'
mut $P/extensions/agi/bin/grid.py '        if not self.nodes:
            self.problem = f"git log {trunk} -- .agi/nodes yielded 0 blobs"' '        if False:
            self.problem = f"git log {trunk} -- .agi/nodes yielded 0 blobs"'
snap >/dev/null 2>&1;snap >/dev/null 2>&1;grid unify --into refs/grid --legacy $SNAP --write --trunk refs/heads/no-such-trunk >$T/ui.out 2>&1
ok "m-error-swallowed-reads-RED with the failed walk read as an empty set m22 (live's own bytes) is written anyway: $(um 22 %P|wc -w|tr -d ' ') parents on m22, so 2 = RED" '[ "$(um 22 %P|wc -w|tr -d " ")" = 2 ]'
# A: the whole-verdict cadence has a falsifier. The stub turns _origin_quiet non-None from its 3rd call: call 1 = the pre-run gate, call 2 = just before the FIRST unrelated write (m21), call 3 = before
# the second (EVERY=1 here) -> that pair reads `unread`, nothing written, and the tree-equal m4 (not counted by the cadence) is still merged.
mkun uQ;mut $P/extensions/agi/bin/grid.py 'UNRELATED_QUIET_EVERY = 50' 'UNRELATED_QUIET_EVERY = 1'
mut $P/extensions/agi/bin/grid.py 'def _origin_quiet(root: Path) -> str | None:' '_STUB = [0]


def _origin_quiet(root: Path) -> str | None:
    _STUB[0] += 1
    if _STUB[0] > 2:
        return "stub: the mirror moved"'
snap >/dev/null 2>&1;snap >/dev/null 2>&1;grid unify --into refs/grid --legacy $SNAP --write >$T/uq.out 2>&1;uq=$?
ok "u12-a-mirror-that-moves-mid-run-stops-the-next-unrelated-write the whole verdict turns non-QUIET after the first unrelated write: m21 written, m22 NOT (unread), tree-equal m4 still merged, rc $uq" '[ $uq = 1 ]&&[ "$(um 21 %P|wc -w|tr -d " ")" = 2 ]&&[ "$(um 22 %P|wc -w|tr -d " ")" = 1 ]&&[ "$(um 4 %P|wc -w|tr -d " ")" = 2 ]&&grep -q "unread" $T/uq.out'
mkun uR;mut $P/extensions/agi/bin/grid.py 'UNRELATED_QUIET_EVERY = 50' 'UNRELATED_QUIET_EVERY = 1'
mut $P/extensions/agi/bin/grid.py 'def _origin_quiet(root: Path) -> str | None:' '_STUB = [0]


def _origin_quiet(root: Path) -> str | None:
    _STUB[0] += 1
    if _STUB[0] > 2:
        return "stub: the mirror moved"'
mut $P/extensions/agi/bin/grid.py 'if (classes is None or sum(1 for c in classes if c[0].startswith("unrelated-root/")) % UNRELATED_QUIET_EVERY == 0) and _origin_quiet(root):' 'if False:'
snap >/dev/null 2>&1;snap >/dev/null 2>&1;grid unify --into refs/grid --legacy $SNAP --write >/dev/null 2>&1
ok "m-cadence-dropped-reads-RED without the mid-run whole-verdict check the second unrelated pair m22 is written against a mirror that moved: $(um 22 %P|wc -w|tr -d ' ') parents on m22, want 1 = unread, so 2 = RED" '[ "$(um 22 %P|wc -w|tr -d " ")" = 2 ]'
# C1 mutant: the whole-tree grep back (a live tip that already carries a literal reads RED for a reason the write did not cause)
mkun uS;mut $P/extensions/agi/bin/grid.py '        added = _home_added(root, first, merge)' '        added = git_try(root, "grep", "-I", "-q", "-E", "/home/[A-Za-z0-9._-]+", merge).returncode == 0'
snap >/dev/null 2>&1;snap >/dev/null 2>&1;grid unify --into refs/grid --legacy $SNAP --write >/dev/null 2>&1;grid unify --check --into refs/grid --legacy $SNAP >$T/us.out 2>&1
ok "m-whole-tree-grep-reads-RED with the whole-tree home grep back m30 (LIVE's own tip carries /home/ubuntu/live30) reads RED at --check: $(grep -c "RED $(mintn 30)" $T/us.out) RED line(s) on m30, want 0 = GREEN, so 1 = RED" 'grep -q "RED $(mintn 30)" $T/us.out'
mkun uE2;snap >/dev/null 2>&1;snap >/dev/null 2>&1;y=$(mkd 2020-02-02T00:00:00Z $P 21 active moved21);$G -C $P push -q -f $REM $y:refs/grid/node/$(mintn 21) >/dev/null 2>&1;snap >/dev/null 2>&1
grid unify --into refs/grid --legacy $SNAP --write >$T/ue.out 2>&1;ue=$?
ok "u11-a-mirror-that-moved-after-the-verdict-writes-nothing origin moved m21 after the QUIET verdict and the mirror was re-read: unify --write is refused (rc $ue), no unrelated-root merge written" '[ $ue = 1 ]&&grep -q "not QUIET" $T/ue.out&&[ "$(um 21 %P|wc -w|tr -d " ")" = 1 ]'
obm uM1 '        res = git_try(root, "commit-tree", ltree, "-p", ntip, "-p", otip, "-m", msg)' '        res = git_try(root, "commit-tree", f"{otip}^{{tree}}", "-p", ntip, "-p", otip, "-m", msg)'
ok "m-owner-tree-origin-reads-RED the owner write with ORIGIN's tree: --check names m23 (want GREEN, so a RED line = caught): $(grep -c "^  RED" $T/uM1.c) RED" 'grep -q "RED $(mintn 23) (the unrelated-root merge does not carry the live tree" $T/uM1.c'
obm uM2 '        res = git_try(root, "commit-tree", ltree, "-p", ntip, "-p", otip, "-m", msg)' '        res = git_try(root, "commit-tree", ltree, "-p", otip, "-m", msg)'
ok "m-owner-live-dropped-reads-RED a forced ref (the written tip drops the live tip, origin's alone): --check names m23 as an old tip not inside it" 'grep -q "RED $(mintn 23) (an old tip is not an ancestor of the new tip)" $T/uM2.c'
obm uM3 '                tally["unread"] += 1
                named.append(f"  UNREAD {mint}' '                tally["unchanged"] += 1; continue
                named.append(f"  UNREAD {mint}'
printf 'banked %s %s bytes unseen: node.md\n' $(mintn 99) $uo_23 >$P/.agi/sessions/unify/zz-ob-unread.classes;rule zz-ob-unread.classes
grid unify --into refs/grid --legacy $SNAP --owner-batch zz-ob-unread.classes >$T/uM3.u 2>&1;um3=$?
ok "m-owner-unread-skipped-reads-RED an unreadable pair folded into unchanged: rc $um3, no UNREAD line (want rc 1 + the line, so rc 0 = caught)" '[ $um3 = 0 ]&&! grep -q UNREAD $T/uM3.u'
oba uMA '"diff", "--no-color", "--binary", live, otip)' '"diff", "--no-color", f"{live}:node.md", f"{otip}:node.md")' '        body = (res.stdout.splitlines() if' '        body = (res.stdout.splitlines()[:150] if'
ok "m-owner-batch-capped-nodemd-diff-reads-RED the old node.md-only diff capped at 150 lines: origin's payload line or its 200th line is missing from the .batch" '! { grep -q "^   +PAY28" $OBA&&grep -q "^   +origin line 200$" $OBA;}'
obd uMD '                stamp.add(mint, ntip, otip, res.stdout.strip())    # stamped NOW' '                _DEFERRED.append((mint, ntip, otip, res.stdout.strip()))    # stamped NOW' '        if stamp.path is not None:
            print(f"grid unify: record {stamp.path.name}' '        for _d in _DEFERRED: stamp.add(*_d)
        if stamp.path is not None:
            print(f"grid unify: record {stamp.path.name}' 'OWNER_CLASS = "owner-batch/live"' 'OWNER_CLASS = "owner-batch/live"
_DEFERRED = []'
ok "m-owner-stamp-after-the-loop-reads-RED stamping once after the loop: the run that dies after one write leaves it UNSTAMPED (no new owner record)" '[ "$(echo $OW|wc -w|tr -d " ")" = 1 ]&&! grep -q "^owner-batch/live " $OD'
obc uMC '        body = (res.stdout.splitlines() if res.returncode == 0 else' '        body = (res.stdout.splitlines() if True else'
ok "m-owner-diff-unread-as-empty-reads-RED a failed diff folded into an empty body: no 'diff unread' line" '[ "$(grep -c "diff unread" $OC)" = 0 ]'
obr uMS1 '    rulings = _owner_rulings(root, trunk)    # goal:g7.16.1.11.46.16.2 R1' '    rulings = {record: sha}    # MUTANT: every record ruled'
grid unify --into refs/grid --legacy $SNAP --owner-batch $RR --write >/dev/null 2>&1
ok "m-ruling-check-cut-reads-RED with the ruling check cut an UNRULED record writes: m23 has $(um 23 %P|wc -w|tr -d ' ') parents (want 1)" 'one 2'
obr uMS2 '    res = git_try(root, "grep", "-E", f"^{RULING_KEY}: [^ ]+ sha256:[0-9a-f]{{64}}$", trunk, "--", RULING_GLOB)' '    res = git_try(root, "grep", "--untracked", "-E", f"^{RULING_KEY}: [^ ]+ sha256:[0-9a-f]{{64}}$", "--", RULING_GLOB); trunk = ""'
mkdir -p $P/.agi/nodes/doc;printf -- '---\nid: doc:owner-ruling-wt\n---\nowner-batch-ruling: %s\n' "$(rl $RR)" >$P/.agi/nodes/doc/owner-ruling-wt.md;grid unify --into refs/grid --legacy $SNAP --owner-batch $RR --write >/dev/null 2>&1
ok "m-working-tree-ruling-reads-RED a reader that opens the WORKING TREE takes the uncommitted ruling and writes: m23 has $(um 23 %P|wc -w|tr -d ' ') parents (want 1)" 'one 2'
obr uMS3 'trunk, "--", RULING_GLOB)' 'trunk, "--", ".agi/nodes/doc")'
mkdir -p $P/.agi/nodes/doc;printf -- '---\nid: doc:card-x\n---\nowner-batch-ruling: %s\n' "$(rl $RR)" >$P/.agi/nodes/doc/card-x.md;$G -C $P add .agi/nodes/doc >/dev/null 2>&1;$G -C $P commit -qm card >/dev/null;grid unify --into refs/grid --legacy $SNAP --owner-batch $RR --write >/dev/null 2>&1
ok "m-every-doc-node-a-ruling-reads-RED a grep over EVERY doc node takes a card's quote as a ruling and writes: m23 has $(um 23 %P|wc -w|tr -d ' ') parents (want 1)" 'one 2'
obr uMS4 '            if (rec, ltip) not in owner.banked:' '            if ltip not in {t for _, t in owner.banked}:'
rule $RR;grid unify --into refs/grid --legacy $SNAP --owner-batch $RR --write >/dev/null 2>&1;w26=$(fg 26 $uo_26 $RR);printf 'owner-batch/live %s %s %s\n' $(mintn 26) $uo_26 $w26 >$P/.agi/sessions/unify/zz-forge.classes;printf 'banked %s %s bytes unseen: node.md\n' $(mintn 26) $uo_26 >$P/.agi/sessions/unify/zz-unruled.classes
grid unify --check --into refs/grid --legacy $SNAP >$T/ms4.out 2>&1
ok "m-banked-pooled-reads-RED a POOLED banked set (every record's rows) reads the forged m26 GREEN: its tip is banked by the unruled record, not by the record its merge names" '! grep -q "RED $(mintn 26) " $T/ms4.out'
obr uMS5 '                if res.returncode != 0:
                    tally["unread"] += 1' '                if False:
                    tally["unread"] += 1'
rule $RR;gx buildfail unify --into refs/grid --legacy $SNAP --owner-batch $RR --write >$T/ms5.out 2>&1
ok "m-build-failure-as-a-lost-CAS-reads-RED folded into the compare-and-swap name: no 'could not be built' line" '! grep -q "could not be built" $T/ms5.out'
obr uMS6 '            if owner is None or (ltip, merge) not in owner.rows:' '            if False:'
rule $RR;gx diestamp unify --into refs/grid --legacy $SNAP --owner-batch $RR --write >/dev/null 2>&1;grid unify --check --into refs/grid --legacy $SNAP >$T/ms6.out 2>&1
ok "m-stamp-check-cut-reads-RED without the stamped-row check the unstamped m23 reads GREEN at --check" 'one 2&&! grep -q "RED $(mintn 23) " $T/ms6.out'
obx uMS7 '"--no-color", "--binary", live, otip)' '"--no-color", live, otip)'
ok "m-binary-dropped-reads-RED without --binary the .batch says 'Binary files ... differ' and saves no bytes" '! grep -q "^   GIT binary patch" $OX'
obx uMS8 '            body = ["diff empty: trees equal"]' '            body = []'
ok "m-empty-diff-as-empty-body-reads-RED the empty diff written as an empty body: no 'diff empty' line" '! grep -q "diff empty" $OX'
obr uMS9 'RULING_GLOB = ":(glob).agi/nodes/doc/owner-ruling-*.md"' 'RULING_GLOB = ".agi/nodes/doc/owner-ruling-*.md"'
mkdir -p $P/.agi/nodes/doc/owner-ruling-a;printf -- '---\nid: doc:owner-ruling-nested\n---\nowner-batch-ruling: %s\n' "$(rl $RR)" >$P/.agi/nodes/doc/owner-ruling-a/b.md;$G -C $P add .agi/nodes/doc >/dev/null 2>&1;$G -C $P commit -qm nested >/dev/null;grid unify --into refs/grid --legacy $SNAP --owner-batch $RR --write >/dev/null 2>&1
ok "m-glob-magic-cut-reads-RED without :(glob) the reader's '*' crosses '/' and takes the NESTED node as a ruling: m23 has $(um 23 %P|wc -w|tr -d ' ') parents (want 1)" 'one 2'
obr uMS10 '"grep", "-E", f"^{RULING_KEY}: [^ ]+ sha256:' '"grep", "-E", f"{RULING_KEY}: [^ ]+ sha256:'
mkdir -p $P/.agi/nodes/doc;printf -- '---\nid: doc:owner-ruling-quoted\n---\nquoted:owner-batch-ruling: %s\n' "$(rl $RR)" >$P/.agi/nodes/doc/owner-ruling-quoted.md;$G -C $P add .agi/nodes/doc >/dev/null 2>&1;$G -C $P commit -qm quoted >/dev/null;grid unify --into refs/grid --legacy $SNAP --owner-batch $RR --write >/dev/null 2>&1
ok "m-anchor-cut-reads-RED without the '^' a quote-prefixed line counts as a ruling: m23 has $(um 23 %P|wc -w|tr -d ' ') parents (want 1)" 'one 2'
obr uMS11 '    if rulings[record] != sha:' '    if False:'
rule $RR;printf 'banked %s %s bytes unseen: node.md\n' $(mintn 5) $uo_5 >>$P/.agi/sessions/unify/$RR;grid unify --into refs/grid --legacy $SNAP --owner-batch $RR --write >/dev/null 2>&1
ok "m-pin-compare-cut-reads-RED without the hash compare the row appended after the ruling is WRITTEN: m5 has $(um 5 %P|wc -w|tr -d ' ') parents (want 1)" '[ "$(um 5 %P|wc -w|tr -d " ")" = 2 ]'
# --- goal:g7.16.1.11.46.16.4 (self-perpetuating 23:12:04Z, 3/3 alive 23:16:27Z): an OWN-WRITE mirror tip -- our own pushed version the live ref then moved past --
# reads GREEN only when the mirror tip O ITSELF is on the live tip L's first-parent chain AND O..L carries 0 merges; a FOREIGN O reached only through a second parent
# stays RED; every rev-list rc != 0 is `unread`, RED by name (a rev-list git cannot read prints 0 lines, and 0 lines is never 0 merges).
#  m1 own write (pushed x, live moved on to y) | m3 foreign: origin forced to f, live took f in as a SECOND parent only
ow(){ cp_ $1 base;shift;while [ $# -ge 2 ];do mut $P/extensions/agi/bin/grid.py "$1" "$2";shift 2;done;snap >/dev/null 2>&1;snap >/dev/null 2>&1;grid unify --into refs/grid --legacy $SNAP --write >/dev/null 2>&1
 x=$(mk $P 1 active own1 $(sha $NS/$(mintn 1)));$G -C $P update-ref $NS/$(mintn 1) $x;push $x $(mintn 1) >/dev/null
 fo=$(mk $P 3 active foreign3 $c0_3);$G -C $P push -q -f $REM $fo:refs/grid/node/$(mintn 3) >/dev/null 2>&1;snap >/dev/null 2>&1;snap >/dev/null 2>&1
 y=$(mk $P 1 active own1b $x);$G -C $P update-ref $NS/$(mintn 1) $y;z=$(mk $P 3 active took3 $(sha $NS/$(mintn 3)) $fo);$G -C $P update-ref $NS/$(mintn 3) $z
 grid unify --check --into refs/grid --legacy $SNAP >$T/$OW.c 2>&1;}
OW=ow1;ow ow1
ok "w1-an-own-write-mirror-tip-reads-GREEN m1's mirror tip is our pushed x, on y's first-parent chain, 0 merges: no RED on m1; the foreign m3 (2nd parent only) RED by name: $(grep RED $T/ow1.c|cut -c1-120|tr '\n' '|')" '[ "$(sha $SNAP/node/$(mintn 1))" = "$x" ]&&! grep -q "RED $(mintn 1)" $T/ow1.c&&grep -q "RED $(mintn 3) (no merge commit takes the live tip as its first parent)" $T/ow1.c'
OW=owM1;ow owM1 '    return None if otip in chain.stdout.split() and not merges.stdout.strip() else ""' '    return None if _is_ancestor(root, otip, ltip) is True else ""'
ok "m-own-write-bare-ancestor-reads-RED the whole test cut to a bare ancestor test (each half alone keeps m3 RED: a 2nd-parent-only O always leaves the merge that took it in inside O..L): the foreign m3 reads GREEN (want RED, so no RED line = caught)" '! grep -q "RED $(mintn 3)" $T/owM1.c'
OW=ow2;ow ow2 '    merges = git_try(root, "rev-list", "--merges", f"{otip}..{ltip}")' '    merges = git_try(root, "rev-list", "--merges", f"{otip}..nosuchrev")'
ok "w2-a-merges-walk-that-fails-is-unread a --merges rev-list that git cannot read (rc 128, 0 lines) reads m1 RED as unread, never 0 merges: $(grep "RED $(mintn 1)" $T/ow2.c|cut -c1-120)" 'grep -q "RED $(mintn 1) (unread: rev-list --merges rc 128)" $T/ow2.c'
OW=owM2;ow owM2 '    merges = git_try(root, "rev-list", "--merges", f"{otip}..{ltip}")' '    merges = git_try(root, "rev-list", "--merges", f"{otip}..nosuchrev")' '        if res.returncode != 0:
            return f"unread: rev-list {what}' '        if False:
            return f"unread: rev-list {what}'
ok "m-own-write-rc-cut-reads-RED the rc check cut: the failed walk reads as 0 merges and m1 GREEN (want unread, so no RED line on m1 = caught)" '! grep -q "RED $(mintn 1)" $T/owM2.c'
# a mirror ref at a MISSING object (the loose ref file names a sha the object store does not hold): RED `unread` by name, never 'not an ancestor'
owx(){ OW=$1;ow "$@";echo 1234567890abcdef1234567890abcdef12345678 >$P/.git/$SNAP/node/$(mintn 2);grid unify --check --into refs/grid --legacy $SNAP >$T/$1.c 2>&1;}
owx ow3
ok "w3-a-mirror-ref-at-a-missing-object-is-unread m2's mirror ref names an absent object: RED unread by name: $(grep "RED $(mintn 2)" $T/ow3.c|cut -c1-120)" 'grep -q "RED $(mintn 2) (unread: an ancestry or count read failed)" $T/ow3.c'
owx owM3 '        if any(a is None for a in ancestors) or any(c.returncode != 0 for c in counts):' '        if False:'
ok "m-missing-object-folded-reads-RED the unread split cut: m2 reads under the old 'not an ancestor' name (want unread, so that name = caught)" 'grep -q "RED $(mintn 2) (an old tip is not an ancestor of the new tip)" $T/owM3.c'
echo "grid-origin-snap: $nrows rows";echo "grid-origin-snap: $f FAIL";[ $f = 0 ]
