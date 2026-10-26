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
cp_ pj;mut $P/extensions/agi/bin/grid.py '"fetch", "--no-tags", "--prune", "-q", remote, f"+{ns}/node/*:{ORIGIN_SNAP_NS}/node/*"' '"fetch", "--no-tags", "--prune", "-q", remote, f"{ns}/node/*:{ORIGIN_SNAP_NS}/node/*"'
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
ok "m-tree-pick-reads-RED with the equal-tree rule cut, m5 (unequal trees) is merged automatically: the ORIGIN tree wins silently ($(grep -c CONFLICT $T/ml.out) conflicts listed, want 0 = RED)" '! grep -q CONFLICT $T/ml.out'
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
# --- the snapshot is pruned: a name origin deleted leaves the mirror and reads as a write
cp_ pu;snap >/dev/null 2>&1;$G -C $P push -q origin :refs/grid/node/$(mintn 6) 2>&1;snap >$T/pr.out 2>&1;pr=$?
ok "pr1-a-name-origin-deleted-is-a-write origin dropped m6: the pruned mirror no longer lists it, 'name(s) origin no longer lists' counts it, rc $pr (LIVE second writer), and no QUIET verdict" '[ $pr = 2 ]&&[ -z "$(refs $SNAP/node/$(mintn 6))" ]&&grep -q "1 name(s) origin no longer lists" $T/pr.out&&[ ! -e $P/.agi/sessions/origin-snap/quiet ]'
cp_ pv;mut $P/extensions/agi/bin/grid.py '"fetch", "--no-tags", "--prune", "-q", remote' '"fetch", "--no-tags", "-q", remote'
snap >/dev/null 2>&1;$G -C $P push -q origin :refs/grid/node/$(mintn 6) 2>&1;snap >$T/pm.out 2>&1;pm=$?
ok "m-no-prune-reads-RED without --prune the deleted name stays in the mirror (the mirror still lists m6: $(refs $SNAP/node/$(mintn 6)|wc -l|tr -d ' ') ref) and unify could still adopt it" '[ -n "$(refs $SNAP/node/$(mintn 6))" ]'
echo "grid-origin-snap: $nrows rows";echo "grid-origin-snap: $f FAIL";[ $f = 0 ]
