#!/bin/sh
# land-split.t.sh: goal:g7.16.1.11.46.18 G1b-2 falsifier 1 + rows 8 (A14) and 9 (I14) -- a land is a SPLIT: `grid.py split --base B --gated G --write`
# writes ONE grid commit per changed node of B..G on refs/grid/node/<mint> (grid.py's builder mint_node_ref, under GridLock), each ref moved by a CAS on
# the tip it read; a tip that moved since = a `held merge` row for that mint, that node not written, rc 1. The recomposed tree (recompose.py) == the
# gated tree. sh + git + python3 on a SCRATCH repo (the grid-double-mint.t.sh recipe). The fixture: n1 idea MODIFIED, n2 RETIRED (moved to deprecated/),
# n3 a build whose PAYLOAD alone changed, n5 a NEW node, n4 untouched, README.md carried: k = 4 changed nodes. Every mutant (m-*) must read RED.
T=$(mktemp -d);trap 'kill $HP 2>/dev/null;rm -rf $T' 0;f=0;nrows=0;HP=;G=/usr/bin/git;R0=${ROOT:-$(cd "$(dirname "$0")/../../.." && pwd)};BIN=${BIN:-$R0/extensions/agi/bin}
ok(){ nrows=$((nrows+1));if eval "$2";then echo "ok $1";else echo "FAIL $1";f=$((f+1));fi;}
unset GIT_AUTHOR_NAME GIT_AUTHOR_EMAIL GIT_COMMITTER_NAME GIT_COMMITTER_EMAIL GIT_DIR GIT_WORK_TREE GIT_INDEX_FILE AGI_TRUNK
printf '[user]\n\tname=t\n\temail=t@t\n[commit]\n\tgpgsign=false\n[safe]\n\tdirectory=*\n' >$T/gitconfig;export GIT_CONFIG_GLOBAL=$T/gitconfig GIT_CONFIG_SYSTEM=/dev/null
export PYTHONDONTWRITEBYTECODE=1
NS=refs/grid/node;TR=refs/heads/posts/belam;GT=refs/heads/sim/gated
mn(){ printf '%032x' $1;}
# nd <file> <id> <mint n> <type> <status> [extra frontmatter] [body]
nd(){ mkdir -p $(dirname $P/$1);printf -- "---\nid: %s\nmint_id: %s\ntype: %s\nstatus: %s\nparents:\n  - goal:g\n%b---\n# node\n%s\n" "$2" $(mn $3) "$4" "$5" "$6" "${7:-body}" >$P/$1;}
mut(){ python3 - "$1" "$2" "$3" <<'PY'
import sys
s=open(sys.argv[1]).read();a,b=sys.argv[2],sys.argv[3]
assert s.count(a)==1,("mutant anchor",a)
open(sys.argv[1],"w").write(s.replace(a,b))
PY
}
grid(){ (cd $P&&python3 extensions/agi/bin/grid.py "$@");}
rc(){ (cd $P&&python3 extensions/agi/bin/recompose.py --trunk $GT "$@");}
refs(){ $G -C $P for-each-ref --format='%(refname) %(objectname)' refs/;}
mkfix(){ P=$1;rm -rf $P;mkdir -p $P/.agi/nodes $P/extensions/agi;$G init -q $P;cp -r $BIN $P/extensions/agi/bin;cp -r ${SRC:-$R0/extensions/agi/src} $P/extensions/agi/src
 find $P/extensions/agi -name __pycache__ -prune -exec rm -rf {} +;echo '{"grid":{"storage_trunk":"refs/grid"}}' >$P/.agi/config.json
 printf 'readme\n' >$P/README.md;mkdir -p $P/src;printf 'PAY3\n' >$P/src/p3.txt
 nd .agi/nodes/idea/n1.md idea:n1 1 idea active '' one;nd .agi/nodes/idea/n2.md idea:n2 2 idea active '' two
 nd .agi/nodes/build/b3.md build:b3 3 build active 'payload_ref: src/p3.txt\n' three;nd .agi/nodes/idea/n4.md idea:n4 4 idea active '' four
 $G -C $P add -A;$G -C $P commit -qm base;$G -C $P update-ref $TR HEAD;grid commit --all >$T/seed.out 2>&1
 # the gated land: n1 modified, n2 retired (moved + status), b3's payload changed, n5 new, README carried
 nd .agi/nodes/idea/n1.md idea:n1 1 idea active '' one-v2;$G -C $P mv .agi/nodes/idea/n2.md .agi/nodes/deprecated/idea/n2.md 2>/dev/null||{ mkdir -p $P/.agi/nodes/deprecated/idea;$G -C $P mv .agi/nodes/idea/n2.md .agi/nodes/deprecated/idea/n2.md;}
 nd .agi/nodes/deprecated/idea/n2.md idea:n2 2 idea deprecated '' two;printf 'PAY3-v2\n' >$P/src/p3.txt;nd .agi/nodes/idea/n5.md idea:n5 5 idea active '' five;printf 'readme 2\n' >$P/README.md
 $G -C $P add -A;$G -C $P commit -qm gated;$G -C $P update-ref $GT HEAD;$G -C $P checkout -q --detach $TR;}
mkfix $T/base;P=$T/base
cp_(){ rm -rf $T/$1;cp -a $T/base $T/$1;P=$T/$1;}
# the seed: 4 refs at v1; recompose of the trunk = diff 0
ok "f0-the-fixture-seeds-four-refs-and-the-trunk-recomposes $(tail -1 $T/seed.out|cut -c1-90)" '[ $($G -C $P for-each-ref $NS|wc -l) = 4 ]&&(cd $P&&python3 extensions/agi/bin/recompose.py --trunk $TR >/dev/null 2>&1)'
# --- dry run: the plan, nothing written
cp_ s0;refs >$T/s0.before;grid split --base $TR --gated $GT >$T/s0.out 2>&1;s0=$?;refs >$T/s0.after
ok "s0-without-write-the-plan-is-printed-and-nothing-written rc $s0: $(tail -1 $T/s0.out|cut -c1-120)" '[ $s0 = 0 ]&&grep -q "split: 4 changed node(s); 4 grid commit(s) planned" $T/s0.out&&cmp -s $T/s0.before $T/s0.after'
# --- falsifier 1: k = 4 changed nodes -> 4 grid commits, each the ONLY new commit on its ref; the recomposed tree == the gated tree
cp_ f1;refs >$T/f1.before;grid split --base $TR --gated $GT --write >$T/f1.out 2>&1;f1=$?;refs >$T/f1.after
moved=$(diff $T/f1.before $T/f1.after|grep -c '^>');one=0;for i in 1 2 3 5;do t=$($G -C $P rev-parse $NS/$(mn $i));o=$(grep "^$NS/$(mn $i) " $T/f1.before|cut -d' ' -f2)
 if [ -n "$o" ];then [ "$($G -C $P rev-parse $t^)" = "$o" ]&&[ $($G -C $P rev-list --count $o..$t) = 1 ]&&one=$((one+1));else [ $($G -C $P rev-list --count $t) = 1 ]&&one=$((one+1));fi;done
rc >$T/f1.rc 2>&1;f1r=$?
ok "f1-k-changed-nodes-make-k-grid-commits split rc $f1, $moved ref(s) moved, $one of 4 by exactly ONE commit (n5 created at v1), n4 untouched, no ref outside $NS/ written: $(tail -1 $T/f1.out|cut -c1-100)" '[ $f1 = 0 ]&&[ $moved = 4 ]&&[ $one = 4 ]&&grep -q "^$NS/$(mn 4) " $T/f1.after&&[ "$(grep "^$NS/$(mn 4) " $T/f1.before)" = "$(grep "^$NS/$(mn 4) " $T/f1.after)" ]&&[ "$(diff $T/f1.before $T/f1.after|grep "^>"|grep -vc " $NS/")" = 0 ]&&grep -q "split: 4 changed node(s); 4 grid commit(s) written, 0 already on the grid, 0 held" $T/f1.out'
ok "f1b-the-recomposed-tree-is-the-gated-tree recompose.py --trunk $GT after the split: rc $f1r, diff 0 (the payload of b3 from its new tip, n2 at deprecated/): $(grep 'diff vs' $T/f1.rc)" '[ $f1r = 0 ]&&grep -q "diff vs the trunk [0-9a-f]*: 0 path(s)" $T/f1.rc'
ok "f1c-each-version-names-its-land v2 subject + Split-Land: <gated> trailer on n1's new tip; b3's tip carries the new payload" '$G -C $P log -1 --format=%B $NS/$(mn 1)|grep -q "^Split-Land: $($G -C $P rev-parse $GT)$"&&[ "$($G -C $P log -1 --format=%s $NS/$(mn 1))" = "v2 idea:n1" ]&&[ "$($G -C $P show $NS/$(mn 3):payload)" = PAY3-v2 ]'
# mutant (falsifier 1's): the split drops one node's commit -> the recomposed tree differs -> refused (rc 1), the dropped mint named BEHIND
cp_ f1m;mut $P/extensions/agi/bin/grid.py '        for it, ref in zip(items, refs):' '        for it, ref in list(zip(items, refs))[1:]:';grid split --base $TR --gated $GT --write >$T/f1m.out 2>&1;rc >$T/f1m.rc 2>&1;f1m=$?
ok "m-a-split-that-drops-one-node-reads-RED n1's commit dropped: recompose rc $f1m (want 0, so rc 1 = caught), $(grep BEHIND $T/f1m.rc|cut -c1-110)" '[ $f1m = 1 ]&&grep -q "BEHIND $(mn 1) .agi/nodes/idea/n1.md (trunk bytes not on the grid)" $T/f1m.rc'
# --- I14 (aio, Target 1): a tip that MOVED since the split read it is a held merge row; that node not written, never a whole-tree merge, rc 1.
# The concurrent writer is real: a reference-transaction hook in the scratch repo moves n2's ref (a concurrent version C) the moment n1's ref is committed.
i14(){ cp_ $1;shift;while [ $# -ge 2 ];do mut $P/extensions/agi/bin/grid.py "$1" "$2";shift 2;done
 o2=$($G -C $P rev-parse $NS/$(mn 2));C=$(echo concurrent|$G -C $P commit-tree $($G -C $P rev-parse $o2^{tree}) -p $o2);echo $C >$T/$OUT.C
 printf '#!/bin/sh\n[ "$1" = committed ]||exit 0\ngrep -q " %s$"||exit 0\n[ -e %s ]&&exit 0\n: >%s\ngit update-ref %s %s\n' "$NS/$(mn 1)" $T/$OUT.hooked $T/$OUT.hooked "$NS/$(mn 2)" $C >$P/.git/hooks/reference-transaction
 chmod +x $P/.git/hooks/reference-transaction;grid split --base $TR --gated $GT --write >$T/$OUT.out 2>&1;}
OUT=i14;i14 i14;i14=$?;C=$(cat $T/i14.C)
ok "i14-a-moved-tip-is-a-held-merge-row split rc $i14; n2's ref moved under it by the hook: $(grep 'held merge' $T/i14.out|cut -c1-120); n2's ref still = the concurrent version, n1 n3 n5 written" '[ $i14 = 1 ]&&[ -e $T/i14.hooked ]&&grep -q "held merge $(mn 2) .agi/nodes/deprecated/idea/n2.md (its tip moved since it was read" $T/i14.out&&[ "$($G -C $P rev-parse $NS/$(mn 2))" = "$C" ]&&grep -q "3 grid commit(s) written, 0 already on the grid, 1 held" $T/i14.out'
OUT=i14m;i14 i14m '            cas = git_try(root, "update-ref", ref, commit, tip or "")' '            cas = git_try(root, "update-ref", ref, commit)';C=$(cat $T/i14m.C)
ok "m-a-ref-write-without-old-reads-RED no <old>: the concurrent version C is LOST (not in n2's history) (want it kept, so lost = caught)" '[ -e $T/i14m.hooked ]&&! $G -C $P merge-base --is-ancestor $C $NS/$(mn 2)'
# --- A14 (alive): the split is grid.py's, under GridLock: a held lock stops it (rc 2, nothing written); mutant: no lock -> it writes under a held lock
a14(){ cp_ $1;shift;while [ $# -ge 2 ];do mut $P/extensions/agi/bin/grid.py "$1" "$2";shift 2;done
 L=$(cd $P&&python3 -c "import sys;sys.path.insert(0,'extensions/agi/bin');import grid;from pathlib import Path;print(grid.GridLock(grid.find_project_root(),1)._path)" 2>/dev/null)
 mkdir -p $(dirname $L);python3 -c "import fcntl,sys,time;f=open(sys.argv[1],'a+');fcntl.flock(f,fcntl.LOCK_EX);open(sys.argv[2],'w').close();time.sleep(60)" $L $T/$OUT.ready & HP=$!
 n=0;while [ ! -e $T/$OUT.ready ]&&[ $n -lt 100 ];do n=$((n+1));python3 -c "import time;time.sleep(0.1)";done
 refs >$T/$OUT.before;grid split --base $TR --gated $GT --write --lock-wait 1 >$T/$OUT.out 2>&1;r=$?;refs >$T/$OUT.after;kill $HP 2>/dev/null;wait $HP 2>/dev/null;HP=;return $r;}
OUT=a14;a14 a14;a14=$?
ok "a14-the-split-waits-on-GridLock with the grid lock held elsewhere: rc $a14 (2), nothing written: $(grep -o 'could not acquire the grid lock' $T/a14.out|head -1)" '[ $a14 = 2 ]&&cmp -s $T/a14.before $T/a14.after&&[ -s $T/a14.before ]'
OUT=a14m;a14 a14m '    lock = GridLock(root, lock_wait) if write else None' '    lock = None';a14m=$?
ok "m-a-split-without-the-lock-reads-RED the lock dropped: the split writes while grid_sync would hold it, rc $a14m (want rc 2 + nothing written, so moved refs = caught)" '! cmp -s $T/a14m.before $T/a14m.after'
# --- fail closed: a node DELETED (not retired) is unread, nothing written; mutant: the delete check cut -> the split writes the rest
dl(){ cp_ $1;shift;while [ $# -ge 2 ];do mut $P/extensions/agi/bin/grid.py "$1" "$2";shift 2;done;$G -C $P checkout -q $GT 2>/dev/null;$G -C $P rm -q .agi/nodes/idea/n4.md;$G -C $P commit -qm del
 $G -C $P update-ref $GT HEAD;$G -C $P checkout -q --detach $TR;refs >$T/$OUT.before;grid split --base $TR --gated $GT --write >$T/$OUT.out 2>&1;r=$?;refs >$T/$OUT.after;return $r;}
OUT=d1;dl d1;d1=$?
ok "d1-a-deleted-node-is-unread-and-nothing-is-written n4's file deleted in the land: rc $d1, 'unread .agi/nodes/idea/n4.md (deleted ... retire, never delete)', no ref moved" '[ $d1 = 1 ]&&grep -q "unread .agi/nodes/idea/n4.md (deleted with no gated file of its mint $(mn 4): retire, never delete)" $T/d1.out&&cmp -s $T/d1.before $T/d1.after'
OUT=d1m;dl d1m '            if mi and mi.group(1) not in gated_mints:' '            if False:';d1m=$?
ok "m-delete-check-cut-reads-RED the deleted node passes and the other 4 nodes are written, rc $d1m (want unread + nothing written, so moved refs = caught)" '! cmp -s $T/d1m.before $T/d1m.after'
echo "land-split: $nrows rows";echo "land-split: $f FAIL";[ $f = 0 ]
