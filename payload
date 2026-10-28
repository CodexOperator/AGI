#!/bin/sh
# land-split.t.sh: goal:g7.16.1.11.46.18 G1b-2 falsifier 1 + rows 8 (A14) and 9 (I14) -- a land is a SPLIT: `grid.py split --base B --gated G --write`
# writes ONE grid commit per changed node of B..G on refs/grid/node/<mint> (grid.py's builder mint_node_ref, under GridLock), each ref moved by a CAS on
# the tip it read; a tip that moved since = a `held merge` row for that mint, that node not written, rc 1. The recomposed tree (recompose.py) == the
# gated tree. sh + git + python3 on a SCRATCH repo (the grid-double-mint.t.sh recipe). The fixture: n1 idea MODIFIED, n2 RETIRED (moved to deprecated/),
# n3 a build whose PAYLOAD alone changed, n5 a NEW node, n4 untouched, README.md carried: k = 4 changed nodes. The same-tip amend (council 3/3 alive
# [decision] 08:38:11Z) adds A16, U4, I18, A17, A18 + U5 and I17's parity table (commit --all vs split). Every mutant (m-*) must read RED.
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
OUT=i14m;i14 i14m '    res = git_try(root, "update-ref", ref, commit, tip or "")' '    res = git_try(root, "update-ref", ref, commit)';C=$(cat $T/i14m.C)
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
# ===== the same-tip amend (council 3/3, alive [decision] 08:38:11Z): split and commit_file are ONE per-version helper (prepare_version + write_version)
# gt <name> <edit cmds...>: a fresh copy whose GATED commit = the base + the edits (run in its checkout); the copy is left checked out at the GATED commit
gt(){ cp_ $1;shift;$G -C $P checkout -q --detach $TR;(cd $P&&eval "$*");$G -C $P add -A;$G -C $P commit -qm gated2;$G -C $P update-ref $GT HEAD;}
moved(){ [ "$(grep "^$NS/$(mn $1) " $T/$OUT.before)" != "$(grep "^$NS/$(mn $1) " $T/$OUT.after)" ];}
sp(){ refs >$T/$OUT.before;grid split --base $TR --gated $GT --write >$T/$OUT.out 2>&1;r=$?;refs >$T/$OUT.after;return $r;}
cm(){ refs >$T/$OUT.before;grid commit --all >$T/$OUT.out 2>&1;r=$?;refs >$T/$OUT.after;return $r;}
E4="nd .agi/nodes/idea/n4.md idea:n4 4 idea active '' four-v2"
# A16 (alive) DOUBLE MINT: a NEW mint (n6) for the taken id idea:n1 -> unread, nothing written; mutant: the check cut -> the second ref written
gt dm "nd .agi/nodes/idea/n6.md idea:n1 6 idea active '' six;$E4";OUT=dm;sp;dm=$?
ok "a16-a-new-mint-for-a-taken-id-is-unread rc $dm: $(grep 'double mint' $T/dm.out|cut -c1-110), no ref moved" '[ $dm = 1 ]&&grep -q "unread $(mn 6) .agi/nodes/idea/n6.md (double mint: idea:n1 is already carried by mint $(mn 1)" $T/dm.out&&cmp -s $T/dm.before $T/dm.after'
gt dmm "nd .agi/nodes/idea/n6.md idea:n1 6 idea active '' six;$E4";mut $P/extensions/agi/bin/grid.py '        if other:
            return "double-mint", tree, 0, other' '        if False:
            return "double-mint", tree, 0, other';OUT=dmm;sp
ok "m-a-split-without-the-double-mint-check-reads-RED the check cut: the second mint for idea:n1 is WRITTEN (want unread, so its ref = caught)" 'grep -q "^$NS/$(mn 6) " $T/dmm.after'
# U4 (sp) A16's VIEW = the GATED tree: the land renumbers n1 (M1) idea:n1 -> idea:n1b AND adds a NEW idea:n1 (M6): split writes both; mutant: the view from the checkout at base -> M6 refused
U4="nd .agi/nodes/idea/n1.md idea:n1b 1 idea active '' renumbered;nd .agi/nodes/idea/n1-new.md idea:n1 6 idea active '' six"
gt u4 "$U4";$G -C $P checkout -q --detach $TR;OUT=u4;sp;u4=$?
ok "u4-the-double-mint-view-is-the-gated-tree a renumber + a new mint at the vacated id: rc $u4, both written (M1 v2, M6 v1), judged by the gated tree while the checkout sits at the base" '[ $u4 = 0 ]&&moved 1&&grep -q "^$NS/$(mn 6) " $T/u4.after'
gt u4m "$U4";$G -C $P checkout -q --detach $TR;mut $P/extensions/agi/bin/grid.py '                                                    dm_files=view, dm_key=("tree", g))' '                                                    dm_files=None, dm_key="worktree")';OUT=u4m;sp
ok "m-the-view-from-the-checkout-reads-RED the view taken from the checkout at base: M6 refused as a double mint (want both written, so the refusal = caught)" 'grep -q "unread $(mn 6) .agi/nodes/idea/n1-new.md (double mint" $T/u4m.out'
# A16's gated-tree half (sp [word] 08:51:29Z, decision 3/3 alive 08:55:55Z): TWO NEW mints (n6, n7) for one FRESH id in ONE land -> both unread, nothing written;
# mutant: file-only mints left out of the tree view's holders -> both written
FR="nd .agi/nodes/idea/n6.md idea:nx 6 idea active '' six;nd .agi/nodes/idea/n7.md idea:nx 7 idea active '' seven;$E4"
gt fr "$FR";OUT=fr;sp;fr=$?
ok "a16b-two-new-mints-for-one-fresh-id-are-unread rc $fr: $(grep -c 'double mint: idea:nx' $T/fr.out) unread double-mint line(s), refs before == after" '[ $fr = 1 ]&&grep -q "unread $(mn 6) .agi/nodes/idea/n6.md (double mint: idea:nx is already carried by mint $(mn 7)" $T/fr.out&&grep -q "unread $(mn 7) .agi/nodes/idea/n7.md (double mint: idea:nx is already carried by mint $(mn 6)" $T/fr.out&&cmp -s $T/fr.before $T/fr.after'
gt frm "$FR";mut $P/extensions/agi/bin/grid.py '        pool |= v["files"].keys()' '        pass';OUT=frm;sp
ok "m-file-only-mints-not-holders-reads-RED the tree view's holders without the file-only mints: n6 and n7 both WRITTEN (want nothing written, so the refs = caught)" 'grep -q "^$NS/$(mn 6) " $T/frm.after&&grep -q "^$NS/$(mn 7) " $T/frm.after'
# I18 (aio) THE VIEW'S CACHE is keyed by the view: ONE process judges the worktree view (M6 for idea:n1 -> held by M1) then a gated view where M1 is idea:n1b -> no holder
i18(){ cp_ $1;shift;while [ $# -ge 2 ];do mut $P/extensions/agi/bin/grid.py "$1" "$2";shift 2;done
 (cd $P&&python3 -c "import sys;sys.path.insert(0,'extensions/agi/bin');import grid;r=grid.find_project_root();grid.apply_storage_trunk(r)
a=grid.double_mint_holder(r,'$(mn 6)','idea:n1');b=grid.double_mint_holder(r,'$(mn 6)','idea:n1',{'$(mn 1)':{'idea:n1b'},'$(mn 6)':{'idea:n1'}},('tree','g'))
print('worktree',a and a[0]);print('gated',b and b[0])") >$T/$OUT.out 2>&1;}
OUT=i18;i18 i18
ok "i18-one-process-two-views-two-verdicts $(tr '\n' ' ' <$T/i18.out)" 'grep -q "^worktree $(mn 1)$" $T/i18.out&&grep -q "^gated None$" $T/i18.out'
OUT=i18m;i18 i18m '    if key in _DM_CACHE:
        return _DM_CACHE[key]' '    if _DM_CACHE:
        return next(iter(_DM_CACHE.values()))'
ok "m-the-unkeyed-cache-reads-RED the cache keyed by nothing: the gated verdict = the worktree's ($(tr '\n' ' ' <$T/i18m.out)) (want two verdicts, so one = caught)" 'grep -q "^gated $(mn 1)$" $T/i18m.out'
# A17 (alive) LIVE PAYLOAD GONE: a live build edited + its payload file deleted -> unread, nothing written; mutant: the check cut -> written with node.md only
PG="nd .agi/nodes/build/b3.md build:b3 3 build active 'payload_ref: src/p3.txt\n' three-v2;git rm -q src/p3.txt;$E4"
gt pg "$PG";OUT=pg;sp;pg=$?
ok "a17-a-live-payload-gone-is-unread rc $pg: $(grep 'payload_ref' $T/pg.out|cut -c1-110), no ref moved" '[ $pg = 1 ]&&grep -q "unread .agi/nodes/build/b3.md (live build:b3: its payload_ref src/p3.txt names no path in the gated tree)" $T/pg.out&&cmp -s $T/pg.before $T/pg.after'
gt pgm "$PG";mut $P/extensions/agi/bin/grid.py '            else:                                         # A17: a land is gated' '            elif False:                                   # A17: a land is gated';OUT=pgm;sp
ok "m-a-split-without-the-payload-check-reads-RED the check cut: b3's version written with node.md only (want unread, so its moved ref = caught)" 'moved 3'
# A18 (alive) + U5 (sp) NEST + ORDER: a failing nest read on the LAST node in sort order (n4: its tip's root tree object deleted) -> unread, refs before == after;
# mutants: the nest check cut (A18) -> written; the all-or-nothing check cut (U5: a refusal met after a write) -> the earlier node's ref moved
nst(){ gt $1 "nd .agi/nodes/idea/n1.md idea:n1 1 idea active '' one-v2;$E4";shift;while [ $# -ge 2 ];do mut $P/extensions/agi/bin/grid.py "$1" "$2";shift 2;done
 t4=$($G -C $P rev-parse $NS/$(mn 4)^{tree});rm -f $P/.git/objects/$(echo $t4|cut -c1-2)/$(echo $t4|cut -c3-);sp;}
OUT=u5;nst u5;u5=$?
ok "u5-a-refusal-on-the-last-node-writes-nothing n4's nest read fails (ls-tree rc 128): rc $u5, $(grep 'nest entry' $T/u5.out|cut -c1-90), refs before == after (n1, earlier in sort order, NOT written)" '[ $u5 = 1 ]&&grep -q "unread $(mn 4) .agi/nodes/idea/n4.md (the nest entry of its tip is unreadable" $T/u5.out&&cmp -s $T/u5.before $T/u5.after'
OUT=u5m;nst u5m '        if unread:
            for u in unread:
                print(f"  {u}")
            print(f"split: unread {len(unread)}; nothing written")
            return 1
        # WRITE' '        if False:
            return 1
        # WRITE'
ok "m-a-refusal-after-a-write-reads-RED the all-or-nothing check cut (prepare and write interleaved): n1, before n4 in sort order, is WRITTEN (want refs unmoved, so n1 moved = caught)" 'moved 1'
OUT=a18m;nst a18m '        if er.returncode != 0 or (ent and (built is None or built.returncode != 0)):
            return "nest", tree, 0, None' '        if False:
            return "nest", tree, 0, None'
ok "m-a-nest-read-without-its-rc-check-reads-RED the nest rc check cut: the unreadable nest reads as none and n4 is written (want unread, so moved = caught)" 'moved 4'
# I17 (aio) PARITY: five cases through BOTH commit --all (the checkout at the gated commit) and split --write, against ONE declared verdict table:
# cell = <case node's ref moved><the other node's (n1) ref moved>: commit --all refuses / skips / holds the case node (a live payload gone = WARN + written,
# cron) and writes the other; split reads unread and writes NOTHING; unchanged = no version in either, the other written
# fresh = TWO new mints for one fresh id, a DECLARED DIFFERENCE, not parity (aio 08:52:27Z): commit --all first wins (n6 written, n7 refused, cron); split writes nothing
TABLE="dm:commit=ny dm:split=nn pg:commit=yy pg:split=nn nest:commit=ny nest:split=nn held:commit=ny held:split=nn same:commit=ny same:split=ny fresh:commit=ny fresh:split=nn"
E1="nd .agi/nodes/idea/n1.md idea:n1 1 idea active '' one-v2"
par(){ m=$1;w=$2;shift 2;cp_ par-$m-$w;$G -C $P checkout -q --detach $TR
 case $m in dm) c=6;ed="nd .agi/nodes/idea/n6.md idea:n1 6 idea active '' six;$E1";;fresh) c=7;ed="nd .agi/nodes/idea/n6.md idea:nx 6 idea active '' six;nd .agi/nodes/idea/n7.md idea:nx 7 idea active '' seven;$E1";;pg) c=3;ed="nd .agi/nodes/build/b3.md build:b3 3 build active 'payload_ref: src/p3.txt\n' three-v2;git rm -q src/p3.txt;$E1";;
  *) c=4;ed="$E4;$E1";;esac
 (cd $P&&eval "$ed");$G -C $P add -A;$G -C $P commit -qm par;$G -C $P update-ref $GT HEAD
 case $m in nest) t4=$($G -C $P rev-parse $NS/$(mn 4)^{tree});rm -f $P/.git/objects/$(echo $t4|cut -c1-2)/$(echo $t4|cut -c3-);;
  held) echo '{"grid":{"storage_trunk":"refs/grid","legacy_namespaces":["refs/grid/lm"]}}' >$P/.agi/config.json;$G -C $P update-ref refs/grid/lm/node/$(mn 4) $(echo legacy|$G -C $P commit-tree $($G -C $P rev-parse $NS/$(mn 4)^{tree}));;
  same) o4=$($G -C $P rev-parse $NS/$(mn 4));nt=$(printf '100644 blob %s\tnode.md\n' $($G -C $P rev-parse $GT:.agi/nodes/idea/n4.md)|$G -C $P mktree);$G -C $P update-ref $NS/$(mn 4) $(echo v2|$G -C $P commit-tree $nt -p $o4);;esac
 while [ $# -ge 2 ];do mut $P/extensions/agi/bin/grid.py "$1" "$2";shift 2;done
 OUT=par-$m-$w;if [ $w = commit ];then cm;else $G -C $P checkout -q --detach $TR;sp;fi
 a=n;moved $c&&a=y;b=n;moved 1&&b=y;echo "$m:$w=$a$b";}
got=$(for m in dm pg nest held same fresh;do for w in commit split;do par $m $w;done;done|tr '\n' ' ')
ok "i17-parity-commit-all-and-split-against-one-verdict-table got: $got (fresh, the declared difference: commit --all wrote n6: $(grep -c "^$NS/$(mn 6) " $T/par-fresh-commit.after))" '[ "$got" = "$TABLE " ]&&grep -q "^$NS/$(mn 6) " $T/par-fresh-commit.after'
got=$(for m in dm pg nest held same fresh;do for w in commit split;do if [ $w = split ];then par $m $w '            else:                                         # A17: a land is gated' '            elif False:                                   # A17: a land is gated';else par $m $w;fi;done;done|tr '\n' ' ')
ok "m-one-guard-cut-in-one-writer-only-reads-RED split's live-payload guard cut (commit --all untouched): the table reads $got (want the declared table, so a differing cell = caught)" '[ "$got" != "$TABLE " ]&&echo "$got"|grep -q "pg:split=yy"'
echo "land-split: $nrows rows";echo "land-split: $f FAIL";[ $f = 0 ]
