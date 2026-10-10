#!/bin/sh
# metrics-cell.t.sh: goal:g1.41 E3 (DG1 21:42Z; hypothesis:g141-e-reds-metrics-cell-and-council-report-close-four-silent-gaps): metrics_cell.py never commits a node by path while the graph's suite lock is held. It waits at most values.core.suite_lock.hold_wait_s for the release, re-checks that only <cell> and edited_by differ from HEAD, then commits; still held after the bound = ERR, rc 3, naming the lock, the node left as it is with its recover command (DG1's ruling: the lock wins, bounded).
# python3 + git on a SCRATCH repo, no root, no network, 0 USD. metrics_cell.py runs from a scratch bin dir (a COPY of the real file; every other module is a symlink to the real bin, EXCEPT write.py = a STUB that exits 3 like the held-lock refusal, leaving ONLY the cell (and edited_by) dirty). The lock is REAL: <graph>/sessions/verify-suite.lock holding the pid of a live foreign process, as verification.suite_lock_holder reads it. The stub takes the lock (the lock "taken after the checks") and, detached, releases it after STUB_RELEASE seconds. A fake `git` on PATH logs every `commit` that runs while the lock file exists.
# Lanes: e3-control-no-lock (the old by-path recovery still commits), e3-released-inside-the-bound (ONE commit, never while held, node clean), e3-held-past-the-bound / e3-the-bound-is-the-cell (ERR rc 3 naming the lock, the recover command, node dirty, HEAD unchanged, no hang), e3-hand-edit-during-the-wait / e3-hand-edit-riding-along (never laundered), e3-lock-held-at-start (the old skip).
# Honest limits: the wait is read off the fake git (a commit while the lock file exists) and off the clock (the bound is honoured within seconds); the lane drives the wrapper, not write.py's own lock wait (write.py is the stub).
T=$(mktemp -d);trap 'kill $HOLD 2>/dev/null;rm -rf $T' 0;f=0;G=/usr/bin/git;R0=${ROOT:-${1:-$(cd "$(dirname "$0")/../../.." && pwd)}};BIN=$R0/extensions/agi/bin
ok(){ if eval "$2";then echo "ok $1";else echo "FAIL $1";f=$((f+1));fi;}
unset GIT_AUTHOR_NAME GIT_AUTHOR_EMAIL GIT_COMMITTER_NAME GIT_COMMITTER_EMAIL GIT_DIR GIT_WORK_TREE
[ -f $BIN/metrics_cell.py ]&&[ -f $BIN/verification.py ]||{ echo "FAIL inputs: $BIN";exit 99;}
mkdir -p $T/bin $T/fk $T/hm;cp $BIN/metrics_cell.py $T/bin/;for m in $BIN/*.py;do b=${m##*/};[ $b = metrics_cell.py ]||[ $b = write.py ]||ln -s $m $T/bin/$b;done
cat >$T/bin/write.py<<'XX'
import os, re, subprocess, sys
node, verb = sys.argv[1], sys.argv[2]
root, actor = sys.argv[sys.argv.index("--root") + 1], sys.argv[sys.argv.index("--actor") + 1]
cell, _, line = verb[len("set "):].partition(" ")
kind, _, slug = node.partition(":")
p = os.path.join(root, "nodes", kind, slug + ".md")
t = open(p).read()
t = re.sub(r"(?m)^%s:.*$" % cell, "%s: %s" % (cell, line), t, count=1)
t = re.sub(r"(?m)^edited_by:.*$", "edited_by: " + actor, t, count=1)
if os.environ.get("STUB_EXTRA"):
    t += "a hand edit rode along\n"
open(p, "w").write(t)
lock = os.environ.get("STUB_LOCK")
if lock:                      # the suite lock taken AFTER the wrapper's checks: held by a live foreign pid
    open(lock, "w").write(os.environ["STUB_HOLDER"] + "\n")
    rel = os.environ.get("STUB_RELEASE")
    if rel:
        sh = "sleep %s; %s rm -f %s" % (rel, ("echo '# a hand edit during the wait' >> %s;" % p) if os.environ.get("STUB_HAND") else "", lock)
        pr = subprocess.Popen(["sh", "-c", sh], stdin=subprocess.DEVNULL, stdout=subprocess.DEVNULL, stderr=subprocess.DEVNULL, start_new_session=True)
        open(os.environ["STUB_PIDFILE"], "w").write(str(pr.pid))
print("write.py stub: the suite lock is held; node left dirty")
sys.exit(3)
XX
printf '#!/bin/sh\ncase " $* " in *" commit "*)[ -e %s/r/.agi/sessions/verify-suite.lock ]&&echo "commit while the lock file exists" >>%s/viol;;esac\nexec %s "$@"\n' $T $T $G >$T/fk/git;chmod +x $T/fk/git
sleep 600 & HOLD=$!
printf '[user]\n\tname=t\n\temail=t@t\n[commit]\n\tgpgsign=false\n[safe]\n\tdirectory=*\n' >$T/gitconfig;export GIT_CONFIG_GLOBAL=$T/gitconfig GIT_CONFIG_SYSTEM=/dev/null PYTHONDONTWRITEBYTECODE=1
LOCK=$T/r/.agi/sessions/verify-suite.lock
# mk BOUND: a fresh scratch repo, ONE commit, the cell cfg hold_wait_s = BOUND
mk(){ [ -f $T/rel.pid ]&&kill $(cat $T/rel.pid) 2>/dev/null;rm -f $T/rel.pid;rm -rf $T/r $T/viol;mkdir -p $T/r/.agi/nodes/town $T/r/.agi/sessions;printf '{"values":{"core":{"suite_lock":{"hold_wait_s":%s}}}}\n' "$1" >$T/r/.agi/config.json
 printf -- '---\nid: town:t\ntype: town\nmetric: old\nedited_by: belam\ntitle: t\n---\n# body\nline one\n' >$T/r/.agi/nodes/town/t.md;printf -- 'other node\n' >$T/r/.agi/nodes/town/u.md;$G init -q $T/r;$G -C $T/r add -A;$G -C $T/r commit -qm base;H0=$($G -C $T/r rev-parse HEAD);}
# go: metrics_cell under the fakes; extra args = env assignments; rc in $mrc, stdout $T/o, stderr $T/e, elapsed seconds in $el
go(){ s=$(date +%s);(cd $T&&env -i PATH=$T/fk:/usr/bin:/bin HOME=$T/hm GIT_CONFIG_GLOBAL=$T/gitconfig GIT_CONFIG_SYSTEM=/dev/null PYTHONDONTWRITEBYTECODE=1 STUB_HOLDER=$HOLD STUB_PIDFILE=$T/rel.pid "$@" timeout 20 python3 $T/bin/metrics_cell.py $T/r/.agi town:t metric --actor dg2 -- sh -c 'echo "line 42"' >$T/o 2>$T/e);mrc=$?;el=$(($(date +%s)-s))
 nc=$($G -C $T/r rev-list --count HEAD);dirty=$($G -C $T/r status --porcelain -- .agi/nodes/town/t.md .agi/config.json|wc -l|tr -d ' ');viol=0;[ -f $T/viol ]&&viol=$(wc -l <$T/viol|tr -d ' ');hd=$($G -C $T/r rev-parse HEAD);}
# e3-control: no lock at all: the old recovery commits the cell by path
mk 5;go STUB_X=1
ok "e3-control-no-lock-the-cell-is-committed by path: rc $mrc (want 0), commits $nc (want 2), dirty files $dirty (want 0), commits made while a lock exists: $viol (want 0)" '[ $mrc = 0 ]&&[ $nc = 2 ]&&[ $dirty = 0 ]&&[ $viol = 0 ]'
# the lock is taken after the checks and released at 2 s, bound 10: the commit WAITS for the release
mk 10;echo 'an unrelated dirty line' >>$T/r/.agi/nodes/town/u.md;go STUB_LOCK=$LOCK STUB_RELEASE=2
ok "e3-released-inside-the-bound-one-commit-after-the-release lock held by a live pid until 2 s, hold_wait_s 10: rc $mrc (want 0), commits $nc (want 2: ONE new), dirty $dirty (want 0), commits made while the lock file existed: $viol (want 0), the node holds the line: $(grep -c '^metric: line 42$' $T/r/.agi/nodes/town/t.md) (want 1)" '[ $mrc = 0 ]&&[ $nc = 2 ]&&[ $dirty = 0 ]&&[ $viol = 0 ]&&grep -q "^metric: line 42$" $T/r/.agi/nodes/town/t.md'
files=$($G -C $T/r show --name-only --format= HEAD|tr '\n' ' ')
ok "e3-the-commit-is-by-exact-path the one commit touches only [$files] (want .agi/nodes/town/t.md), and an unrelated dirty node stays dirty: $($G -C $T/r status --porcelain -- .agi/nodes/town/u.md|wc -l|tr -d ' ') (want 1)" '[ "$files" = ".agi/nodes/town/t.md " ]&&[ "$($G -C $T/r status --porcelain -- .agi/nodes/town/u.md|wc -l|tr -d " ")" = 1 ]'
# held past the bound (never released), bound 1: ERR rc 3 naming the lock, the recover command, the node left as it is, HEAD unchanged, no hang
mk 1;go STUB_LOCK=$LOCK
ok "e3-held-past-the-bound-is-ERR-rc-3 lock held for good, hold_wait_s 1: rc $mrc (want 3), stderr names the lock: $(grep -ci 'suite lock\|verify-suite' $T/e) (want >= 1), an ERR: line: $(grep -c '^ERR:' $T/e) (want >= 1), the recover command: $(grep -c 'git -C .* add -- ' $T/e) (want >= 1), HEAD moved: $([ $hd = $H0 ]&&echo no||echo YES) (want no), node dirty files $dirty (want 1), commits while locked $viol (want 0), took ${el}s (want <= 8: the bound, not forever)" '[ $mrc = 3 ]&&[ $(grep -ci "suite lock\|verify-suite" $T/e) -ge 1 ]&&[ $(grep -c "^ERR:" $T/e) -ge 1 ]&&[ $(grep -c "git -C .* add -- " $T/e) -ge 1 ]&&[ $hd = $H0 ]&&[ $dirty = 1 ]&&[ $viol = 0 ]&&[ $el -le 8 ]'
ok "e3-the-left-node-differs-from-HEAD-only-in-the-cell the dirty node after the ERR: $($G -C $T/r diff --numstat -- .agi/nodes/town/t.md|tr '\t' ' ') (want 2 added, 2 removed: metric + edited_by)" '[ "$($G -C $T/r diff --numstat -- .agi/nodes/town/t.md|cut -f1,2|tr "\t" " ")" = "2 2" ]'
# the bound IS the cell: released at 3 s but the cell says 1 s -> ERR (and the same release inside a 10 s bound committed above)
mk 1;go STUB_LOCK=$LOCK STUB_RELEASE=3
ok "e3-the-bound-is-the-cell-not-a-constant lock released at 3 s, hold_wait_s 1: rc $mrc (want 3), HEAD moved: $([ $hd = $H0 ]&&echo no||echo YES) (want no), commits while locked $viol (want 0)" '[ $mrc = 3 ]&&[ $hd = $H0 ]&&[ $viol = 0 ]'
# a hand edit made DURING the wait is never laundered: the re-check after the wait refuses
mk 10;go STUB_LOCK=$LOCK STUB_RELEASE=2 STUB_HAND=1
ok "e3-hand-edit-during-the-wait-is-never-laundered the node gains a hand-edited body line while the commit waits (released at 2 s): rc $mrc (want != 0), HEAD moved: $([ $hd = $H0 ]&&echo no||echo YES) (want no), node dirty files $dirty (want 1), an ERR: line $(grep -c '^ERR:' $T/e) (want >= 1), the hand edit still in the file: $(grep -c 'a hand edit during the wait' $T/r/.agi/nodes/town/t.md) (want 1)" '[ $mrc != 0 ]&&[ $hd = $H0 ]&&[ $dirty = 1 ]&&[ $(grep -c "^ERR:" $T/e) -ge 1 ]&&[ $(grep -c "a hand edit during the wait" $T/r/.agi/nodes/town/t.md) = 1 ]'
# a hand edit that rides along with the write itself (no lock): still never laundered (the old rule)
mk 5;go STUB_EXTRA=1
ok "e3-hand-edit-riding-along-is-never-laundered the stub's write also edits the body, no lock: rc $mrc (want != 0), HEAD moved: $([ $hd = $H0 ]&&echo no||echo YES) (want no), dirty files $dirty (want 1), an ERR: line $(grep -c '^ERR:' $T/e) (want >= 1)" '[ $mrc != 0 ]&&[ $hd = $H0 ]&&[ $dirty = 1 ]&&[ $(grep -c "^ERR:" $T/e) -ge 1 ]'
# the old guard at the START: a live holder before anything runs -> ONE skip line, rc 0, nothing written
mk 5;echo $HOLD >$LOCK;go STUB_X=1
ok "e3-lock-held-at-start-is-the-old-skip a live holder before the run: rc $mrc (want 0), a skip: line $(grep -c '^skip:' $T/o) (want 1), HEAD moved: $([ $hd = $H0 ]&&echo no||echo YES) (want no), node dirty files $dirty (want 0)" '[ $mrc = 0 ]&&[ $(grep -c "^skip:" $T/o) = 1 ]&&[ $hd = $H0 ]&&[ $dirty = 0 ]'
# a DEAD pid in the lock file is no hold: the by-path commit proceeds at once
mk 5;sleep 0.1 & DEAD=$!;wait $DEAD;echo $DEAD >$LOCK;go STUB_X=1
ok "e3-a-stale-lock-is-no-hold a lock file naming a dead pid: rc $mrc (want 0), commits $nc (want 2), dirty $dirty (want 0), took ${el}s (want <= 3: no wait)" '[ $mrc = 0 ]&&[ $nc = 2 ]&&[ $dirty = 0 ]&&[ $el -le 3 ]'
echo "metrics-cell: $f FAIL"
exit $f
