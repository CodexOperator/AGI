#!/bin/sh
# grid-collapse.t.sh: goal:g4.13.1 (design + 11-line patch: doc:rse-aa1-boxes AA1.N, alive/aa1n @5cc55defa): a grid tick never overwrites a COLLAPSE. A collapse = ONE grid commit on a container's ref: tree = the container's tip tree + nest/<member mint> (each member's tip tree), parents = the container's tip + each member's tip. Three defects make it last ONE tick: G1 the unchanged-check compares the node tree with the WHOLE tip tree (an unedited container is re-versioned and nest/ leaves), G2 the version number counts ALL parents (v8, not v4), G3 `update-ref` has no old value (a tick that read the tip BEFORE a collapse overwrites it).
# sh + git + python3 on a SCRATCH repo (the grid-payload-commit.t.sh recipe: the engine's bin dir is COPIED under the scratch root, so grid.py's own repo IS the scratch project). BIN = the extensions/agi/bin dir under test (default: ROOT's); a mutation / reference = BIN=<an edited copy of that dir>. 0 USD, no live ref, no network. One ok/FAIL line per case; exit = FAIL count.
# Fixture: container CA (a build node with a payload) and members M1 M2 (idea nodes), each versioned TWICE (v1, v2), then CA absorbs M1 + M2 by the doc's nest recipe: CA's first-parent chain = v1 v2 collapse (3), `rev-list --count` = 7 (2 + 1 + 2 members x 2). x1 x2 are plain nodes that sort AFTER CA (a CAS refusal on CA must not stop them). The RACE is a git shim on PATH: when grid.py runs `update-ref` on CA's ref, the shim first lands the collapse (a concurrent writer), then runs the real command.
# Lanes: a the race is refused and the collapse survives (+ a2 the next tick lands v4 on it) · b an UNEDITED collapsed container stays unchanged (v8 -> nest 0 vs nest 2) · c an edit after a collapse numbers by --first-parent (v4) and keeps nest 2 · d a refusal skips THAT node with ONE reason line and the --all run goes on · e the other --count readers (diff, versions, payload --version near lines 1302 1319 1336) agree with first-parent · f no non-delete update-ref in commit_file lacks its old value (grep/AST lane). Honest limits are named in the lane text.
T=$(mktemp -d);trap 'rm -rf $T' 0;f=0;G=/usr/bin/git;R0=${ROOT:-$(cd "$(dirname "$0")/../../.." && pwd)};BIN=${BIN:-$R0/extensions/agi/bin}
ok(){ if eval "$2";then echo "ok $1";else echo "FAIL $1";f=$((f+1));fi;}
unset GIT_AUTHOR_NAME GIT_AUTHOR_EMAIL GIT_COMMITTER_NAME GIT_COMMITTER_EMAIL GIT_DIR GIT_WORK_TREE AGI_TRUNK
printf '[user]\n\tname=t\n\temail=t@t\n[commit]\n\tgpgsign=false\n[safe]\n\tdirectory=*\n' >$T/gitconfig;export GIT_CONFIG_GLOBAL=$T/gitconfig GIT_CONFIG_SYSTEM=/dev/null
CA=aaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaa;M1=bbbbbbbbbbbbbbbbbbbbbbbbbbbbbbbb;M2=cccccccccccccccccccccccccccccccc;X1=dddddddddddddddddddddddddddddddd;X2=eeeeeeeeeeeeeeeeeeeeeeeeeeeeeeee;NS=refs/grid/node
grid(){ (cd $P&&PYTHONDONTWRITEBYTECODE=1 PYTHONPATH=$R0/extensions/agi/src python3 extensions/agi/bin/grid.py "$@");}
tip(){ $G -C $P rev-parse -q --verify $NS/$1 2>/dev/null;}
fp(){ $G -C $P rev-list --count --first-parent $NS/$1;}
pc(){ $G -C $P rev-list --count $NS/$1;}
nestn(){ $G -C $P ls-tree $NS/$1:nest 2>/dev/null|wc -l|tr -d ' ';}
subj(){ $G -C $P log -1 --format=%s $NS/$1;}
bld(){ printf -- '---\nid: build:%s\nmint_id: %s\ntype: build\nparents:\n  - idea:y\npayload_ref: extensions/%s.sh\n---\nbody %s %s\n' $1 $2 $1 $1 "$3">$P/.agi/nodes/build/$1.md;}
idn(){ printf -- '---\nid: idea:%s\nmint_id: %s\ntype: idea\nparents:\n  - goal:g\n---\nbody %s %s\n' $1 $2 $1 "$3">$P/.agi/nodes/idea/$1.md;}
# the doc's nest recipe, run in $P (real git): collapse M1 M2 into CA's ref
nest(){ P_=$NS;N=$1;shift;(cd $P;t=$($G mktree </dev/null);t=$(for m;do printf '040000 tree %s\t%s\n' $($G rev-parse $P_/$m^{tree}) $m;done|$G mktree);r=$( { $G ls-tree $P_/$N|grep -v '	nest$';printf '040000 tree %s\tnest\n' $t; }|$G mktree);a="-p $($G rev-parse $P_/$N)";for m;do a="$a -p $($G rev-parse $P_/$m)";done;c=$(echo "nest $# into $N"|$G commit-tree $r $a)&&$G update-ref $P_/$N $c $($G rev-parse $P_/$N)&&echo $c);}
# fixture: tpl0 = all five nodes at v1 + v2 (NOT collapsed); tpl1 = tpl0 + the collapse
P=$T/tpl0;mkdir -p $P/.agi/nodes/build $P/.agi/nodes/idea $P/extensions;mkdir -p $P/extensions/agi;cp -r $BIN $P/extensions/agi/bin;find $P/extensions/agi/bin -name __pycache__ -prune -exec rm -rf {} +
$G init -q $P;echo '{}'>$P/.agi/config.json;echo 'echo ca1'>$P/extensions/ca.sh
bld ca $CA one;idn m1 $M1 one;idn m2 $M2 one;idn x1 $X1 one;idn x2 $X2 one;$G -C $P add -A;$G -C $P commit -qm fixture
grid init >/dev/null 2>&1;grid commit --all >$T/v1.out 2>&1
echo 'echo ca2'>>$P/extensions/ca.sh;bld ca $CA two;idn m1 $M1 two;idn m2 $M2 two;idn x1 $X1 two;idn x2 $X2 two;grid commit --all >$T/v2.out 2>&1
ok "base-two-versions the five nodes each have 2 versions on their own refs (ca $(fp $CA), m1 $(fp $M1), m2 $(fp $M2), x1 $(fp $X1), x2 $(fp $X2))" '[ "$(fp $CA)" = 2 ]&&[ "$(fp $M1)" = 2 ]&&[ "$(fp $M2)" = 2 ]&&[ "$(fp $X1)" = 2 ]&&[ "$(fp $X2)" = 2 ]'
cp -a $P $T/tpl1;P=$T/tpl1;COL=$(nest $CA $M1 $M2)
ok "base-collapse the fixture collapse is ONE commit on CA's ref: tip = $(echo $COL|cut -c1-8), first-parent versions $(fp $CA) (want 3), rev-list --count $(pc $CA) (want 7: 2 + 1 + 2 members x 2), nest entries $(nestn $CA) (want 2)" '[ -n "$COL" ]&&[ "$(tip $CA)" = "$COL" ]&&[ "$(fp $CA)" = 3 ]&&[ "$(pc $CA)" = 7 ]&&[ "$(nestn $CA)" = 2 ]'
# --- b: an UNEDITED collapsed container stays unchanged (G1: today the tick re-versions it as v8 and nest/ leaves)
rm -rf $T/pb;cp -a $T/tpl1 $T/pb;P=$T/pb;grid commit --all >$T/b.out 2>&1
ok "b-unedited-keeps-nest a tick over the UNEDITED collapsed container makes no new version (tip $(tip $CA|cut -c1-8), want the collapse $(echo $COL|cut -c1-8)) and the nest/ entries stay (nest $(nestn $CA), want 2); today it is re-versioned (v8) with nest 0" '[ "$(tip $CA)" = "$COL" ]&&[ "$(nestn $CA)" = 2 ]&&! grep -q "v8" $T/b.out'
# --- c: an EDIT after a collapse numbers by --first-parent (G2) and keeps the members (G1)
rm -rf $T/pc;cp -a $T/tpl1 $T/pc;P=$T/pc;bld ca $CA three;grid commit --all >$T/c.out 2>&1
ok "c1-edit-numbers-first-parent an edit of the collapsed container is v4 (subject '$(subj $CA)', want 'v4 build:ca'): the number counts the container's own chain, not the 7 commits it reaches" '[ "$(subj $CA)" = "v4 build:ca" ]'
ok "c2-edit-keeps-nest the edit's tree still carries the 2 nest/ entries (nest $(nestn $CA)) and its first parent is the collapse (chain $(fp $CA), want 4)" '[ "$(nestn $CA)" = 2 ]&&[ "$(fp $CA)" = 4 ]&&[ "$($G -C $P rev-parse $NS/$CA^)" = "$COL" ]'
# --- a: the race (G3): a tick that read CA's tip BEFORE the collapse; the shim lands the collapse just before grid.py's update-ref on CA
rm -rf $T/pa;cp -a $T/tpl0 $T/pa;P=$T/pa;mkdir -p $T/shim;cat >$T/collapse.sh <<EOF
#!/bin/sh
cd "\$CP"||exit 1
G=/usr/bin/git;P_=$NS;N=$CA
t=\$(for m in $M1 $M2;do printf '040000 tree %s\t%s\n' \$(\$G rev-parse \$P_/\$m^{tree}) \$m;done|\$G mktree)
r=\$( { \$G ls-tree \$P_/\$N|grep -v '	nest\$';printf '040000 tree %s\tnest\n' \$t; }|\$G mktree)
c=\$(echo "nest 2 into \$N"|\$G commit-tree \$r -p \$(\$G rev-parse \$P_/\$N) -p \$(\$G rev-parse \$P_/$M1) -p \$(\$G rev-parse \$P_/$M2))
\$G update-ref \$P_/\$N \$c \$(\$G rev-parse \$P_/\$N)&&echo \$c>$T/injected.sha
EOF
cat >$T/shim/git <<EOF
#!/bin/sh
case " \$* " in *" update-ref $NS/$CA "*)[ -e $T/injected ]||{ : >$T/injected;sh $T/collapse.sh;};;esac
exec /usr/bin/git "\$@"
EOF
chmod +x $T/shim/git
shimrun(){ (cd $P&&CP=$P PATH=$T/shim:$PATH PYTHONDONTWRITEBYTECODE=1 PYTHONPATH=$R0/extensions/agi/src python3 extensions/agi/bin/grid.py "$@");}
bld ca $CA race;shimrun commit --all >$T/a.out 2>&1;INJ=$(cat $T/injected.sha 2>/dev/null)
ok "a-race-refused a tick that read CA's tip BEFORE the collapse is REFUSED and the collapse SURVIVES: the shim landed the collapse ($(echo "${INJ:-NOT LANDED}"|cut -c1-8)), CA's tip is still it ($(tip $CA|cut -c1-8)) and carries nest $(nestn $CA) (want 2); today the tick overwrites it" '[ -n "$INJ" ]&&[ "$(tip $CA)" = "$INJ" ]&&[ "$(nestn $CA)" = 2 ]'
grid commit --all >$T/a2.out 2>&1
ok "a2-next-tick-lands-on-the-collapse the NEXT tick (no race) re-versions the still-edited container on the new tip: v4 ('$(subj $CA)') with nest $(nestn $CA) (want 2)" '[ "$(subj $CA)" = "v4 build:ca" ]&&[ "$(nestn $CA)" = 2 ]'
# --- d: a refusal skips THAT node with ONE reason line and the --all run goes on with the rest (x1 x2 sort after CA)
rm -rf $T/pd $T/injected $T/injected.sha;cp -a $T/tpl0 $T/pd;P=$T/pd
bld ca $CA race;idn x1 $X1 three;idn x2 $X2 three;shimrun commit --all >$T/d.out 2>&1;drc=$?
nl=$(grep -c "$CA\|build:ca" $T/d.out|tr -d ' ');rl=$(grep "$CA\|build:ca" $T/d.out|grep -v '^v[0-9]'|wc -l|tr -d ' ')
ok "d1-run-goes-on the refusal of CA does not stop the run: x1 and x2 still get their v3 ($(fp $X1), $(fp $X2)); the run exited $drc (not asserted)" '[ "$(fp $X1)" = 3 ]&&[ "$(fp $X2)" = 3 ]'
ok "d2-one-reason-line the refusal prints exactly ONE reason line naming CA (its mint id or build:ca, not a 'vN' version line): $rl line(s): $(grep "$CA\|build:ca" $T/d.out|grep -v '^v[0-9]'|head -2|cut -c1-110|tr '\n' '|')" '[ "$rl" = 1 ]&&[ "$(tip $CA)" = "$(cat $T/injected.sha 2>/dev/null)" ]'
# --- e: the other version readers agree with the first-parent numbering (the collapsed fixture: 3 own versions, 7 reachable)
P=$T/tpl1;nv=$(grid versions build:ca 2>&1)
ok "e1-versions-first-parent grid.py versions build:ca prints the container's OWN version count: $nv (want 3, not the 7 commits it reaches)" '[ "$nv" = 3 ]'
grid diff build:ca --back 3 >$T/e2.out 2>&1;e2rc=$?
ok "e2-diff-back-bound grid.py diff build:ca --back 3 is refused by the first-parent bound (rc $e2rc): 'only 3 version(s)' ($(head -1 $T/e2.out|cut -c1-70))" '[ $e2rc != 0 ]&&grep -q "only 3 version" $T/e2.out'
grid diff build:ca --back 2 >$T/e2b.out 2>&1;e2brc=$?
ok "e2b-diff-back-2-works --back 2 (v1 against the collapse) still works (rc $e2brc, $(wc -l <$T/e2b.out|tr -d ' ') lines)" '[ $e2brc = 0 ]&&[ -s $T/e2b.out ]'
pv2=$(grid payload build:ca --version 2 2>&1)
ok "e3-payload-version-2 grid.py payload build:ca --version 2 returns v2's payload (the 2 lines ca1 / ca2): got '$(echo "$pv2"|tr '\n' ' '|cut -c1-60)'" '[ "$pv2" = "echo ca1
echo ca2" ]'
grid payload build:ca --version 4 >$T/e4.out 2>&1;e4rc=$?
ok "e4-payload-version-4-refused grid.py payload build:ca --version 4 names the first-parent range: 'has 3 version(s); v4 does not exist' (rc $e4rc: $(head -1 $T/e4.out|cut -c1-80))" '[ $e4rc != 0 ]&&grep -q "has 3 version" $T/e4.out'
# --- f: no non-delete update-ref in commit_file without its old value (AST): the third positional after `update-ref` (ref, new, OLD) must be there
cat >$T/chkupd.py <<'PYEOF'
import ast,sys
src=open(sys.argv[1]).read();t=ast.parse(src);bad=[]
class V(ast.NodeVisitor):
    fn=None
    def visit_FunctionDef(self,n):
        o=self.fn;self.fn=n.name;self.generic_visit(n);self.fn=o
    def visit_Call(self,n):
        a=[x.value if isinstance(x,ast.Constant) else None for x in n.args]
        if "update-ref" in a:
            i=a.index("update-ref");rest=n.args[i+1:]
            need=3
            if len(rest)<need and not (rest and isinstance(rest[0],ast.Constant) and rest[0].value=="-d" and len(rest)>=3):bad.append((self.fn,n.lineno,len(rest)))
        self.generic_visit(n)
V().visit(t)
cf=[b for b in bad if b[0]=="commit_file"];oth=[b for b in bad if b[0]!="commit_file"]
print("commit_file:",cf);print("elsewhere (named, not counted):",oth)
sys.exit(1 if cf else 0)
PYEOF
python3 $T/chkupd.py $BIN/grid.py >$T/f.out 2>&1;frc=$?
ok "f-update-ref-carries-old commit_file's update-ref of a node's grid ref carries the OLD tip (a CAS): $(head -1 $T/f.out|cut -c1-80). NOT counted, named: $(sed -n 2p $T/f.out|cut -c1-120)" '[ $frc = 0 ]'
echo "grid-collapse: $f FAIL"
exit $f
