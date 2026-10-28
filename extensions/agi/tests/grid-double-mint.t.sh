#!/bin/sh
# grid-double-mint.t.sh: goal:g7.16.1.11.46.16.1 -- the grid writer REFUSES to create a NEW refs/grid/node/<mint> when another mint already carries the
# same `id:` (the census-orphans decision, alive 07:42:38Z 10-26, row (5)): 22 orphans at the G1a census included five double-mint ghosts
# (goal:g7.31.3.3.1-.5), minted twice on 09-29. Where the other mint's id is READ: from that mint's FILE in the commit's own view; from its ref TIP
# only for a mint with no file in that view (ghosts, never-landed). MUTANT PAIR the council demanded: (i) a goal RENUMBER (`M1: g7.1 -> g7.2`) plus a NEW
# mint at the vacated id in ONE commit PASSES in EITHER processing order (the false-refusal control); (ii) two live files, one id, two mints: the second is
# REFUSED, both mints printed, its file left for review. A check with only (ii) is not accepted.
# sh + git + python3 on a SCRATCH repo (the grid-namespace.t.sh recipe). Every mutant (m*) must read RED.
T=$(mktemp -d);trap 'rm -rf $T' 0;f=0;nrows=0;G=/usr/bin/git;R0=${ROOT:-$(cd "$(dirname "$0")/../../.." && pwd)};BIN=${BIN:-$R0/extensions/agi/bin}
ok(){ nrows=$((nrows+1));if eval "$2";then echo "ok $1";else echo "FAIL $1";f=$((f+1));fi;}
unset GIT_AUTHOR_NAME GIT_AUTHOR_EMAIL GIT_COMMITTER_NAME GIT_COMMITTER_EMAIL GIT_DIR GIT_WORK_TREE AGI_TRUNK
printf '[user]\n\tname=t\n\temail=t@t\n[commit]\n\tgpgsign=false\n[safe]\n\tdirectory=*\n' >$T/gitconfig;export GIT_CONFIG_GLOBAL=$T/gitconfig GIT_CONFIG_SYSTEM=/dev/null
export PYTHONDONTWRITEBYTECODE=1 PYTHONPATH=$R0/extensions/agi/src
NS=refs/grid/node
mintn(){ printf '%032x' $1;}
# node <dir> <file> <node id> <mint n> [status]: one node file
node(){ printf -- '---\nid: %s\nmint_id: %s\ntype: idea\nstatus: %s\nparents:\n  - goal:g\n---\nbody of %s\n' "$3" $(mintn $4) "${5:-active}" "$3" >$1/.agi/nodes/idea/$2.md;}
mkfix(){ P=$1;rm -rf $P;mkdir -p $P/.agi/nodes/idea $P/extensions/agi;$G init -q $P;cp -r $BIN $P/extensions/agi/bin;find $P/extensions/agi/bin -name __pycache__ -prune -exec rm -rf {} +
 echo '{"grid":{"storage_trunk":"refs/grid"}}' >$P/.agi/config.json
 node $P n1 idea:n1 1;node $P n2 idea:n2 2;node $P n3 idea:n3 3
 $G -C $P add -A;$G -C $P commit -qm fixture;(cd $P&&python3 extensions/agi/bin/grid.py commit --all >/dev/null 2>&1);}
grid(){ (cd $P&&python3 extensions/agi/bin/grid.py "$@");}
refs(){ $G -C $P for-each-ref --format='%(refname) %(objectname)' "$@";}
mut(){ python3 - "$1" "$2" "$3" <<'PY'
import sys
s=open(sys.argv[1]).read();a,b=sys.argv[2],sys.argv[3]
assert s.count(a)==1,("mutant anchor",a)
open(sys.argv[1],"w").write(s.replace(a,b))
PY
}
cp_(){ rm -rf $T/$1;cp -a $T/base $T/$1;P=$T/$1;}
mkfix $T/base;P=$T/base
ok "base-fixture three mints, three refs (idea:n1..n3), each ref one version" '[ "$(refs $NS|wc -l|tr -d " ")" = 3 ]'
# --- (ii) two live files, one id, two mints: the NEW one is refused
cp_ a;node $P dup idea:n1 9;grid commit --all >$T/a.out 2>&1;a=$?
ok "d1-a-new-mint-at-a-taken-id-is-refused a new file with mint 9 at idea:n1 (carried by mint 1): rc $a, no ref for mint 9, both mints printed, the file left: $(grep -m1 '^refuse' $T/a.out|cut -c1-190)" '[ $a = 1 ]&&[ -z "$(refs $NS/$(mintn 9))" ]&&grep -q "^refuse (double mint: idea:n1 is already carried by mint $(mintn 1) (its node file); this file.s mint is $(mintn 9)" $T/a.out&&[ -f $P/.agi/nodes/idea/dup.md ]&&[ "$(refs $NS|wc -l|tr -d " ")" = 3 ]'
# --- (i) the renumber control, in BOTH processing orders (files are walked sorted by path)
for order in before after;do
 cp_ r$order;if [ $order = before ];then newf=a-new;else newf=z-new;fi
 node $P n1 idea:n7 1;node $P $newf idea:n1 8;grid commit --all >$T/r$order.out 2>&1;r=$?
 ok "d2-renumber-plus-new-mint-passes-$order a goal RENUMBER (mint 1: idea:n1 -> idea:n7) and a NEW mint 8 at the vacated idea:n1 in ONE commit, the new file sorting $order the renumbered one: rc $r, mint 8's ref created, mint 1 got its second version, nothing refused" '[ $r = 0 ]&&[ -n "$(refs $NS/$(mintn 8))" ]&&[ "$($G -C $P rev-list --count $NS/$(mintn 1))" = 2 ]&&! grep -q "^refuse" $T/r'$order'.out'
done
# --- a ghost: a mint with a ref and NO file at all still holds its id (read from its ref tip)
cp_ g;rm $P/.agi/nodes/idea/n2.md;$G -C $P add -A;$G -C $P commit -qm drop-n2;node $P new idea:n2 5;grid commit --all >$T/g.out 2>&1;g=$?
ok "d3-a-ghost-holds-its-id-by-its-ref-tip mint 2 has a ref and no file anywhere; a new mint 5 at idea:n2 is refused naming mint 2 and 'its ref tip (no node file)': rc $g" '[ $g = 1 ]&&[ -z "$(refs $NS/$(mintn 5))" ]&&grep -q "carried by mint $(mintn 2) (its ref tip (no node file))" $T/g.out'
# --- two NEW files, one id, neither minted yet: the first (path order) is minted, the second refused
cp_ n;node $P aa idea:n9 6;node $P bb idea:n9 7;grid commit --all >$T/n.out 2>&1;n=$?
ok "d4-of-two-new-files-with-one-id-the-second-is-refused mints 6 (aa.md) and 7 (bb.md) both name idea:n9: rc $n, mint 6 minted, mint 7 refused naming mint 6" '[ $n = 1 ]&&[ -n "$(refs $NS/$(mintn 6))" ]&&[ -z "$(refs $NS/$(mintn 7))" ]&&grep -q "carried by mint $(mintn 6)" $T/n.out'
# --- an ordinary new mint, and a new version of an existing mint, are untouched
cp_ o;node $P fresh idea:n4 4;printf 'edit\n' >>$P/.agi/nodes/idea/n2.md;grid commit --all >$T/o.out 2>&1;o=$?
ok "d5-the-ordinary-paths-are-untouched a new mint at a free id, and a new version of an existing mint, still write: rc $o, 4 refs, mint 2 at 2 versions" '[ $o = 0 ]&&[ "$(refs $NS|wc -l|tr -d " ")" = 4 ]&&[ "$($G -C $P rev-list --count $NS/$(mintn 2))" = 2 ]'
# --- mutants
cp_ m1;mut $P/extensions/agi/bin/grid.py '    if tip is None and mint and ref == mint_node_ref(mint):' '    if False and mint and ref == mint_node_ref(mint):'
node $P dup idea:n1 9;grid commit --all >$T/m1.out 2>&1
ok "m-check-cut-reads-RED with the check removed the double mint is written: mint 9 has a ref ($(refs $NS/$(mintn 9)|wc -l|tr -d ' ') ref, want 0 = green)" '[ -n "$(refs $NS/$(mintn 9))" ]'
cp_ m2;mut $P/extensions/agi/bin/grid.py '    loose = {m: t for m, t in refs.items() if m not in files}' '    loose = dict(refs)'
mut $P/extensions/agi/bin/grid.py '        if m in v["files"]:
            if node_id in v["files"][m]:' '        if False:
            if node_id in v["files"][m]:'
node $P n1 idea:n7 1;node $P a-new idea:n1 8;grid commit --all >$T/m2.out 2>&1;m2=$?
ok "m-ref-tip-read-for-every-mint-reads-RED (the false-refusal control) reading EVERY mint from its ref tip makes the renumber commit refuse the new mint 8 (rc $m2, want 0 = green): mint 1's tip still says idea:n1 until its new version is written" '[ -z "$(refs $NS/$(mintn 8))" ]'
cp_ m3;mut $P/extensions/agi/bin/grid.py '        elif v["tip_ids"].get(m, MINTED_THIS_RUN.get(m)) == node_id:' '        elif False:'
rm $P/.agi/nodes/idea/n2.md;$G -C $P add -A;$G -C $P commit -qm drop-n2;node $P new idea:n2 5;grid commit --all >$T/m3.out 2>&1
ok "m-file-read-only-reads-RED a check that reads only files lets a ghost's id be taken again (mint 5 has a ref: $(refs $NS/$(mintn 5)|wc -l|tr -d ' '))" '[ -n "$(refs $NS/$(mintn 5))" ]'
cp_ m4;mut $P/extensions/agi/bin/grid.py '    pool = v["refs"].keys() | MINTED_THIS_RUN.keys()' '    pool = v["refs"].keys() | MINTED_THIS_RUN.keys() | v["files"].keys()'
node $P aa idea:n9 6;node $P bb idea:n9 7;grid commit --all >$T/m4.out 2>&1
ok "m-unminted-files-count-as-holders-reads-RED if a file with no ref counted as holding its id, BOTH new files at idea:n9 would be refused (refs for mints 6 and 7: $(refs $NS/$(mintn 6) $NS/$(mintn 7)|wc -l|tr -d ' '), want 1 = green)" '[ -z "$(refs $NS/$(mintn 6))" ]'
echo "grid-double-mint: $nrows rows";echo "grid-double-mint: $f FAIL";[ $f = 0 ]
