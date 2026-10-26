#!/bin/sh
# grid-namespace.t.sh: goal:g7.16.1.11.46.16 G1a. ONE grid namespace refs/grid/node/<mint>, written ADDITIVELY.
# sh + git + python3 on a SCRATCH repo (the grid-collapse.t.sh recipe: the engine's bin dir is COPIED under the scratch root).
# Fixture (plumbing, no tick): FROZEN refs/grid/node/<m> (2 commits, the 09-21 side) and LIVE refs/grid/local-maxxing/node/<m> (3 commits, a
# different root, never an ancestor) for 24 mints, 12 with EQUAL trees and 12 UNEQUAL; plus 6 live-only mints (no frozen ref) and a mint named TBD.
# Rows: t* G1a-T (per mint: both old tips are ancestors, rev-list --count new >= max(old), tree(new) == tree(live tip), m/m, measured here by
# shell and again by `grid.py unify --check`), w* G1a-W (the writer re-pointed: a probe edit is ONE commit on refs/grid/node/<m>, live refs changed
# = 0; before the unify the writer HOLDS, never forks), d* delete 0 (legacy refs intact, a push dry-run lists no delete, push-changed never pushes a
# legacy ref), c* the census cell (five numbers, unread never 0). Every mutant (m*) must read RED.
T=$(mktemp -d);trap 'rm -rf $T' 0;f=0;nrows=0;G=/usr/bin/git;R0=${ROOT:-$(cd "$(dirname "$0")/../../.." && pwd)};BIN=${BIN:-$R0/extensions/agi/bin}
ok(){ nrows=$((nrows+1));if eval "$2";then echo "ok $1";else echo "FAIL $1";f=$((f+1));fi;}
unset GIT_AUTHOR_NAME GIT_AUTHOR_EMAIL GIT_COMMITTER_NAME GIT_COMMITTER_EMAIL GIT_DIR GIT_WORK_TREE AGI_TRUNK
printf '[user]\n\tname=t\n\temail=t@t\n[commit]\n\tgpgsign=false\n[safe]\n\tdirectory=*\n' >$T/gitconfig;export GIT_CONFIG_GLOBAL=$T/gitconfig GIT_CONFIG_SYSTEM=/dev/null
export PYTHONDONTWRITEBYTECODE=1 PYTHONPATH=$R0/extensions/agi/src
NS=refs/grid/node;LNS=refs/grid/local-maxxing/node;CFG_NEW='{"grid":{"storage_trunk":"refs/grid","legacy_namespaces":["refs/grid/local-maxxing"],"push_batch_limit":7}}';CFG_OLD='{"grid":{"storage_trunk":"refs/grid/local-maxxing","push_batch_limit":7}}'
mintn(){ printf '%032x' $1;}
nodemd(){ printf -- '---\nid: idea:n%s\nmint_id: %s\ntype: idea\nstatus: %s\nparents:\n  - goal:g\n---\nbody %s\n' $1 $(mintn $1) $2 "$3";}
# mk <dir> <n> <status> <text> [parent...] -> the commit sha of a one-file tree
mk(){ d=$1;n=$2;st=$3;tx=$4;shift 4;b=$(nodemd $n $st "$tx"|$G -C $d hash-object -w --stdin);t=$(printf '100644 blob %s\tnode.md\n' $b|$G -C $d mktree);pa=;for x;do pa="$pa -p $x";done;echo "$tx"|$G -C $d commit-tree $t $pa;}
mkfix(){ P=$1;rm -rf $P;mkdir -p $P/.agi/nodes/idea $P/extensions/agi;$G init -q $P;cp -r $BIN $P/extensions/agi/bin;find $P/extensions/agi/bin -name __pycache__ -prune -exec rm -rf {} +
 i=1;while [ $i -le 30 ];do
  st=active;[ $i = 5 ]&&st=deprecated
  if [ $i -le 24 ];then
   o1=$(mk $P $i $st "frozen-a-$i");o2=$(mk $P $i $st "frozen-b-$i" $o1);$G -C $P update-ref $NS/$(mintn $i) $o2
   if [ $((i%2)) = 0 ];then x="frozen-b-$i";else x="live-$i";fi
   l1=$(mk $P $i $st "live-a-$i");l2=$(mk $P $i $st "live-b-$i" $l1);l3=$(mk $P $i $st "$x" $l2)
  else l1=$(mk $P $i $st "live-a-$i");l2=$(mk $P $i $st "live-b-$i" $l1);l3=$(mk $P $i $st "live-c-$i" $l2);fi
  $G -C $P update-ref $LNS/$(mintn $i) $l3;i=$((i+1));done
 # one mint literally named TBD, in both namespaces
 o=$(mk $P 99 active frozen-tbd);$G -C $P update-ref $NS/TBD $o;l=$(mk $P 99 active live-tbd);$G -C $P update-ref $LNS/TBD $l
 # node files in the trunk: mints 1..20 (21..30 and TBD are orphans); file bytes == the live tip's node.md
 i=1;while [ $i -le 20 ];do $G -C $P cat-file -p $LNS/$(mintn $i):node.md >$P/.agi/nodes/idea/n$i.md;i=$((i+1));done
 echo '{}'>$P/.agi/config.json;$G -C $P add -A;$G -C $P commit -qm fixture;}
setcfg(){ printf '%s\n' "$2">$1/.agi/config.json;}
grid(){ (cd $P&&python3 extensions/agi/bin/grid.py "$@");}
refs(){ $G -C $P for-each-ref --format='%(refname) %(objectname)' "$@";}
sha(){ $G -C $P rev-parse -q --verify "$1" 2>/dev/null;}
# the independent G1a-T measurement, in shell: prints good/total over the live namespace; $1 = the before file
measure(){ good=0;tot=0;for r in $($G -C $P for-each-ref --format='%(refname)' $LNS);do m=${r#$LNS/};tot=$((tot+1));l=$(sha $r);n=$(sha $NS/$m);o=$(awk -v r="$NS/$m" '$1==r{print $2}' $1)
  [ -n "$n" ]||continue;$G -C $P merge-base --is-ancestor $l $n||continue;[ -z "$o" ]||$G -C $P merge-base --is-ancestor $o $n||continue
  cn=$($G -C $P rev-list --count $n);cl=$($G -C $P rev-list --count $l);co=0;[ -z "$o" ]||co=$($G -C $P rev-list --count $o);mx=$cl;[ $co -gt $mx ]&&mx=$co;[ $cn -ge $mx ]||continue
  mc=$n;[ $n = $l ]||mc=$($G -C $P rev-list --first-parent --parents $n|awk -v l=$l '$2==l{print $1;exit}');[ -n "$mc" ]||continue
  [ "$($G -C $P rev-parse $mc^{tree})" = "$($G -C $P rev-parse $l^{tree})" ]||continue;good=$((good+1));done;echo "$good/$tot";}
mkfix $T/base;P=$T/base
refs $NS >$T/before.txt;refs refs/grid/local-maxxing >$T/lm0.txt
ndiv=0;neq=0;for i in $(seq 1 24);do m=$(mintn $i);a=$(sha $NS/$m);b=$(sha $LNS/$m);$G -C $P merge-base --is-ancestor $a $b&&ndiv=$((ndiv+1));$G -C $P merge-base --is-ancestor $b $a&&ndiv=$((ndiv+1));[ "$(sha $NS/$m^{tree})" = "$(sha $LNS/$m^{tree})" ]&&neq=$((neq+1));done
ok "base-fixture 25 frozen refs (24 + TBD), 31 live refs, $neq equal-tree and $((24-neq)) unequal-tree pairs, $ndiv of the 24 pairs on one line of descent (want 0: every pair diverged)" '[ "$(refs $NS|wc -l|tr -d " ")" = 25 ]&&[ "$(refs $LNS|wc -l|tr -d " ")" = 31 ]&&[ $ndiv = 0 ]&&[ $neq = 12 ]'
setcfg $P "$CFG_NEW"
# --- t: G1a-T
rm -rf $T/pa;cp -a $T/base $T/pa;P=$T/pa
grid unify >$T/dry.out 2>&1;refs >$T/dry.refs
ok "t0-dry-run-touches-nothing the dry run reports 25 merged / 6 adopted (and the TBD pair) and writes no ref: $(tr '\n' ' ' <$T/dry.out)" 'grep -q "25 merged, 6 adopted, 0 unchanged, 0 conflict, 0 unread of 31" $T/dry.out&&refs >$T/after.refs&&cmp -s $T/dry.refs $T/after.refs&&[ "$(refs $NS|wc -l|tr -d " ")" = 25 ]'
refs $NS >$T/pa.before;grid unify --write >$T/w.out 2>&1;wrc=$?
ok "t1-write-merges-additively --write: 25 merged (24 pairs + TBD), 6 adopted, rc 0: $(tr '\n' ' ' <$T/w.out)" 'grep -q "25 merged, 6 adopted, 0 unchanged, 0 conflict, 0 unread of 31" $T/w.out&&[ $wrc = 0 ]&&[ "$(refs $NS|wc -l|tr -d " ")" = 31 ]'
ok "t2-every-mint-measured-in-shell per mint: both old tips are ancestors of the new tip, rev-list --count new >= max(old), tree(new tip) == tree(live tip) at the merge, 31/31 ($(measure $T/pa.before))" '[ "$(measure $T/pa.before)" = 31/31 ]'
grid unify --check >$T/chk.out 2>&1;crc=$?
ok "t3-the-verbs-own-check-agrees unify --check reads the same: $(tr '\n' ' ' <$T/chk.out)" 'grep -q "unified 31/31" $T/chk.out&&[ $crc = 0 ]'
ok "t4-unequal-pairs-carry-the-live-tree on the 12 unequal pairs the new tip is the merge of (live, frozen) and its tree is the LIVE tree, not the 09-21 one" 'n=0;for i in $(seq 1 24);do m=$(mintn $i);[ "$(sha $NS/$m^{tree})" = "$(sha $LNS/$m^{tree})" ]||{ n=$((n+1)); [ "$(sha $NS/$m^1)" = "$(sha $LNS/$m)" ]&&[ "$(sha $NS/$m^2)" = "$(awk -v r="$NS/$m" "\$1==r{print \$2}" $T/pa.before)" ]&&continue;n=99;};done;[ $n = 0 ]'
ok "t5-live-only-mints-point-at-the-live-tip the 6 mints with no frozen ref now share the live tip exactly (adopted, no merge commit)" 'for i in $(seq 25 30);do m=$(mintn $i);[ "$(sha $NS/$m)" = "$(sha $LNS/$m)" ]||exit 1;done'
ok "t6-versions-keep-counting-the-live-chain a merged ref numbers by --first-parent from the LIVE chain (live 3 versions -> the merge is v4), so the next writer is v5" 'm=$(mintn 3);[ "$(refs $NS/$m|wc -l|tr -d " ")" = 1 ]&&[ "$($G -C $P rev-list --count --first-parent $NS/$m)" = 4 ]&&[ "$($G -C $P log -1 --format=%s $NS/$m)" = "unify v4 $m" ]'
refs $NS >$T/pa.after1;grid unify --write >$T/w2.out 2>&1;refs $NS >$T/pa.after2
ok "t7-idempotent a second --write merges and adopts nothing and moves no ref: $(tr '\n' ' ' <$T/w2.out)" 'grep -q "0 merged, 0 adopted, 31 unchanged" $T/w2.out&&cmp -s $T/pa.after1 $T/pa.after2'
# mutants of G1a-T: one version dropped / the 09-21 tree carried on an unequal pair
mut(){ python3 - "$1" "$2" "$3" <<'PY'
import sys
s=open(sys.argv[1]).read();a,b=sys.argv[2],sys.argv[3]
assert s.count(a)==1,("mutant anchor",a)
open(sys.argv[1],"w").write(s.replace(a,b))
PY
}
for mu in drop tree;do rm -rf $T/pm;cp -a $T/base $T/pm;P=$T/pm;setcfg $P "$CFG_NEW";G1=$P/extensions/agi/bin/grid.py
 if [ $mu = drop ];then mut $G1 '"-p", ltip, "-p", ntip, "-m", msg' '"-p", ltip, "-m", msg';else mut $G1 'f"{ltip}^{{tree}}", "-p"' 'f"{ntip}^{{tree}}", "-p"';fi
 grid unify --write >/dev/null 2>&1;grid unify --check >$T/mc.out 2>&1;mrc=$?
 ok "m-$mu-mutant-reads-RED ($( [ $mu = drop ]&&echo 'one version dropped: the frozen tip is no ancestor'||echo 'a 09-21 tree carried on an unequal pair')): the shell measure is short of 31/31 ($(measure $T/before.txt)) AND the verb's own check is RED rc $mrc" '[ "$(measure $T/before.txt)" != 31/31 ]&&[ $mrc = 1 ]&&grep -q RED $T/mc.out'
done
# --- t8/t9: the merge run BEFORE the config lands (--into/--legacy; the writer still on the old namespace), then the delta after the land
rm -rf $T/pp;cp -a $T/base $T/pp;P=$T/pp;setcfg $P "$CFG_OLD";refs $NS >$T/pp.before
grid unify --into refs/grid --legacy refs/grid/local-maxxing --write >$T/pp1.out 2>&1;pp1=$?
ok "t8-pre-land-run-by-flags with the config still naming the old namespace, --into/--legacy merge it all (25 merged, 6 adopted, rc $pp1) and the shell measure reads 31/31 ($(measure $T/pp.before))" 'grep -q "25 merged, 6 adopted" $T/pp1.out&&[ $pp1 = 0 ]&&[ "$(measure $T/pp.before)" = 31/31 ]'
M3=$(mintn 3);printf 'tick on the old writer\n' >>$P/.agi/nodes/idea/n3.md;grid commit --all >/dev/null 2>&1;setcfg $P "$CFG_NEW"
refs >$T/pp.r1;grid commit --all >$T/pp2.out 2>&1;pp2=$?;refs >$T/pp.r2
ok "t9a-the-delta-is-held-not-forked the old writer made one more live version before the land: with the new config the writer HOLDS exactly that mint (rc $pp2) and no ref moves" '[ $pp2 = 1 ]&&grep -q "^grid: 1 held" $T/pp2.out&&cmp -s $T/pp.r1 $T/pp.r2'
grid unify --write >$T/pp3.out 2>&1;grid unify --check >$T/pp4.out 2>&1;pp4=$?
ok "t9b-the-post-land-run-merges-only-the-delta unify --write after the land: $(tr '\n' ' ' <$T/pp3.out); the check reads 31/31 (rc $pp4) and the shell measure agrees ($(measure $T/pp.before))" 'grep -q "1 merged, 0 adopted, 30 unchanged" $T/pp3.out&&[ $pp4 = 0 ]&&grep -q "unified 31/31" $T/pp4.out&&[ "$(measure $T/pp.before)" = 31/31 ]'
grid commit --all >$T/pp5.out 2>&1;pp5=$?
ok "t9c-the-writer-is-clean-after rc $pp5, nothing held" '[ $pp5 = 0 ]'
rm -rf $T/pq;cp -a $T/base $T/pq;P=$T/pq;setcfg $P "$CFG_OLD";grid unify --into refs/grid --legacy /etc/passwd >$T/pq.out 2>&1;pq=$?
ok "t10-a-namespace-outside-refs-grid-is-unread --legacy naming a path outside refs/grid prints unread and exits 1 (rc $pq)" '[ $pq = 1 ]&&grep -q "unread" $T/pq.out'
# --- r2: --check trusts only the verb's OWN pre-write snapshot (never vacuous)
rm -rf $T/pr;cp -a $T/base $T/pr;P=$T/pr;setcfg $P "$CFG_NEW"
grid unify --check >$T/r0.out 2>&1;r0=$?
ok "r2a-check-without-a-write-is-unread no unify --write has run here: --check prints unread, rc $r0 (never unified 0/0)" '[ $r0 = 1 ]&&grep -q "unread (no pre-write snapshot" $T/r0.out'
grid unify --write >$T/r1.out 2>&1;sn=$(ls $P/.agi/sessions/unify/*.refs 2>/dev/null|head -1);nsn=$(ls $P/.agi/sessions/unify/*.refs 2>/dev/null|wc -l|tr -d ' ')
sort $sn >$T/r.got 2>/dev/null
ok "r2b-the-write-keeps-its-own-snapshot --write printed a snapshot name, wrote $nsn file holding exactly the 25 refs it started from (taken before its first CAS), and a second --write leaves it alone" 'grep -q "^grid unify: pre-write snapshot" $T/r1.out&&[ "$nsn" = 1 ]&&[ "$(wc -l <$T/r.got|tr -d " ")" = 25 ]&&grep -q "refs/grid/node/TBD" $T/r.got&&grid unify --write >/dev/null 2>&1&&[ "$(ls $P/.agi/sessions/unify/*.refs|wc -l|tr -d " ")" = 1 ]'
grid unify --check --before $T/before.txt >$T/r2.out 2>&1;r2=$?
ok "r2c-a-caller-supplied-before-file-is-refused --before is no longer an argument (argparse rc $r2): a late or empty file cannot reach the check" '[ $r2 = 2 ]'
rm -rf $T/pt;cp -a $T/pr $T/pt;P=$T/pt;rm -f $P/.agi/sessions/unify/*.refs;refs $NS >$P/.agi/sessions/unify/20990101T000000Z-1-0.refs;grid unify --check >$T/r3.out 2>&1;r3=$?
ok "r2d-a-late-snapshot-reads-RED the snapshot replaced by the state AFTER the write (every old tip = the new tip): the check is RED, rc $r3" '[ $r3 = 1 ]&&grep -q "RED" $T/r3.out'
rm -rf $T/ps;cp -a $T/base $T/ps;P=$T/ps;setcfg $P "$CFG_NEW";mut $P/extensions/agi/bin/grid.py '"-p", ltip, "-p", ntip, "-m", msg' '"-p", ltip, "-m", msg'
grid unify --write >/dev/null 2>&1;rm -f $P/.agi/sessions/unify/*.refs;refs $NS >$P/.agi/sessions/unify/20990101T000000Z-1-0.refs;grid unify --check >$T/r4.out 2>&1;r4=$?
ok "m-late-snapshot-and-a-dropped-version-reads-RED a late snapshot AND an unify that drops the frozen parent (the old check read unified m/m): RED, rc $r4" '[ $r4 = 1 ]&&grep -q "RED" $T/r4.out'
rm -rf $T/pu;cp -a $T/base $T/pu;P=$T/pu;setcfg $P "$CFG_NEW";mut $P/extensions/agi/bin/grid.py 'msg = f"unify v{n} {mint}\n\nUnify-Live: {ltip}\nUnify-Frozen: {ntip}\n"' 'msg = f"unify v{n} {mint}\n"'
grid unify --write >/dev/null 2>&1;grid unify --check >$T/r5.out 2>&1;r5=$?
ok "m-no-trailer-reads-RED a merge that carries no Unify-Frozen trailer: --check is RED, rc $r5" '[ $r5 = 1 ]&&grep -q "trailer" $T/r5.out'
# --- r3: the fetch spec is narrowed and never forced
rm -rf $T/pv $T/rem2.git;cp -a $T/base $T/pv;P=$T/pv;setcfg $P "$CFG_NEW";$G init -q --bare $T/rem2.git;$G -C $P remote add origin $T/rem2.git;$G -C $P push -q origin 'refs/grid/node/*:refs/grid/node/*' 2>&1
grid unify --write >/dev/null 2>&1;refs $NS >$T/v0.txt;grid init >$T/init.out 2>&1;$G -C $P fetch -q origin >/dev/null 2>&1;refs $NS >$T/v1.txt
ok "r3a-a-fetch-from-a-remote-at-the-frozen-tips-leaves-the-merged-tips-unchanged after unify --write, init + fetch from a remote still at the 09-21 tips moves no ref ($(wc -l <$T/v0.txt|tr -d ' ') refs); configured: $($G -C $P config --get-all remote.origin.fetch|tr '\n' ' ')" 'cmp -s $T/v0.txt $T/v1.txt&&! $G -C $P config --get-all remote.origin.fetch|grep -q "^+refs/grid"&&$G -C $P config --get-all remote.origin.fetch|grep -q "^refs/grid/node/\*:refs/grid/node/\*$"'
rm -rf $T/pw2;cp -a $T/base $T/pw2;P=$T/pw2;setcfg $P "$CFG_NEW";$G -C $P remote add origin $T/rem2.git;mut $P/extensions/agi/bin/grid.py 'return [f"{ns}/node/*:{ns}/node/*", f"{ns}/session/*:{ns}/session/*"]' 'return [f"+{ns}/*:{ns}/*"]'
grid unify --write >/dev/null 2>&1;refs $NS >$T/w0.txt;grid init >/dev/null 2>&1;$G -C $P fetch -q origin >/dev/null 2>&1;refs $NS >$T/w1.txt
ok "m-forced-wildcard-fetch-reads-RED with the old forced spec +refs/grid/*:refs/grid/* the same fetch moves merged tips back to the frozen ones ($(diff $T/w0.txt $T/w1.txt|grep -c '^>') refs moved)" '! cmp -s $T/w0.txt $T/w1.txt'
# --- r4: a malformed config fails closed; an unreadable legacy listing writes nothing
for bad in '"refs/grid/local-maxxing"' '["refs/grid/local-maxxing",7]' '["refs/other"]' '["refs/grid"]';do
 rm -rf $T/pk;cp -a $T/base $T/pk;P=$T/pk;setcfg $P "{\"grid\":{\"storage_trunk\":\"refs/grid\",\"legacy_namespaces\":$bad}}";printf 'probe edit\n' >>$P/.agi/nodes/idea/n3.md;grid commit --all >$T/k.out 2>&1;k=$?;grid unify >$T/ku.out 2>&1;ku=$?
 ok "r4-malformed-legacy-namespaces-$(echo $bad|tr -c 'a-z0-9\n' '-'|cut -c1-24) legacy_namespaces=$bad: commit refused by name (rc $k, nothing written), unify unread (rc $ku)" '[ $k != 0 ]&&grep -q "legacy_namespaces" $T/k.out&&[ "$(refs $NS|wc -l|tr -d " ")" = 25 ]&&[ $ku = 1 ]&&grep -q "unread" $T/ku.out';done
rm -rf $T/pk2;cp -a $T/base $T/pk2;P=$T/pk2;mut $P/extensions/agi/bin/grid.py '    if problem:    # goal:g7.16.1.11.46.16 R4' '    if False:    # goal:g7.16.1.11.46.16 R4'
setcfg $P '{"grid":{"storage_trunk":"refs/grid","legacy_namespaces":"refs/grid/local-maxxing"}}';printf 'probe edit\n' >>$P/.agi/nodes/idea/n3.md;grid commit --all >$T/k2.out 2>&1
ok "m-config-check-cut-reads-RED without the check the refusal no longer names the cell (the namespace guard alone fires)" '! grep -q "legacy_namespaces" $T/k2.out'
mkdir -p $T/gshim;cat >$T/gshim/git <<EOF
#!/bin/sh
case " \$* " in *" for-each-ref refs/grid/local-maxxing/node "*)echo "fatal: simulated failure" >&2;exit 128;;esac
exec /usr/bin/git "\$@"
EOF
chmod +x $T/gshim/git
shimgrid(){ (cd $P&&PATH=$T/gshim:$PATH python3 extensions/agi/bin/grid.py "$@");}
rm -rf $T/pk3;cp -a $T/base $T/pk3;P=$T/pk3;setcfg $P "$CFG_NEW";printf 'probe edit\n' >>$P/.agi/nodes/idea/n3.md;m3=$(sha $NS/$(mintn 3));shimgrid commit --all >$T/k3.out 2>&1;k3=$?
ok "r4b-an-unreadable-legacy-listing-writes-nothing the one for-each-ref of the legacy namespace fails (rc 128): commit exits $k3 saying unread, and no ref is written (a failed read is no longer 'no legacy ref')" '[ $k3 != 0 ]&&grep -q "unread" $T/k3.out&&[ "$(refs $NS|wc -l|tr -d " ")" = 25 ]&&[ "$(sha $NS/$(mintn 3))" = "$m3" ]'
rm -rf $T/pk4;cp -a $T/base $T/pk4;P=$T/pk4;setcfg $P "$CFG_NEW";m3=$(sha $NS/$(mintn 3));mut $P/extensions/agi/bin/grid.py '            if res.returncode != 0:
                sys.exit(f"grid: unread (for-each-ref' '            if False:
                sys.exit(f"grid: unread (for-each-ref';printf 'probe edit\n' >>$P/.agi/nodes/idea/n3.md;shimgrid commit --all >$T/k4.out 2>&1
ok "m-listing-rc-ignored-reads-RED with the rc ignored the failed read looks like 'no legacy ref' and the writer forks: the probe landed on the FROZEN tip: $([ "$(sha $NS/$(mintn 3))" != "$m3" ]&&echo yes||echo no) (no = green, yes is RED)" '[ "$(sha $NS/$(mintn 3))" != "$m3" ]'
# --- w: G1a-W
rm -rf $T/pw;cp -a $T/base $T/pw;P=$T/pw;setcfg $P "$CFG_NEW"
grid commit --all >$T/hold.out 2>&1;hrc=$?;refs >$T/hold.refs
ok "w0-the-writer-holds-before-the-unify with the new config and no unify, commit --all writes NO ref (31 held, rc 1, naming the verb), never a fork: $(tail -1 $T/hold.out)" '[ $hrc = 1 ]&&grep -q "held (a read-only legacy tip" $T/hold.out&&grep -q "grid.py unify --write" $T/hold.out&&[ "$(refs $NS|wc -l|tr -d " ")" = 25 ]&&[ "$(refs $LNS)" = "$(cat $T/lm0.txt|grep local-maxxing/node)" ]'
grid unify --write >/dev/null 2>&1;refs refs/grid/local-maxxing >$T/lm1.txt
M3=$(mintn 3);T0=$(sha $NS/$M3);printf 'probe edit\n' >>$P/.agi/nodes/idea/n3.md;grid commit --all >$T/probe.out 2>&1;prc=$?
ok "w1-the-probe-edit-is-one-commit-on-the-one-namespace after the unify, a probe edit of one node (SM's 'land' edit) is ONE new commit on refs/grid/node/<mint> ($(echo $T0|cut -c1-8) -> $(sha $NS/$M3|cut -c1-8), $($G -C $P rev-list --count $T0..$NS/$M3) new), rc $prc, and no other ref moved" '[ $prc = 0 ]&&[ "$($G -C $P rev-list --count $T0..$NS/$M3)" = 1 ]&&[ "$($G -C $P log -1 --format=%s $NS/$M3)" = "v5 idea:n3" ]&&[ "$(refs $NS|grep -vc " $(sha $NS/$M3)\$")" = 30 ]'
refs refs/grid/local-maxxing >$T/lm2.txt;ch=$(diff $T/lm1.txt $T/lm2.txt|grep -c '^>')
ok "w2-live-refs-changed-since-the-land-0 refs under refs/grid/local-maxxing whose tip changed since the land: $ch (the writer left the old namespace alone)" '[ "$ch" = 0 ]'
# mutant: the writer left alone (storage_trunk still the old namespace)
rm -rf $T/pn;cp -a $T/base $T/pn;P=$T/pn;setcfg $P "$CFG_OLD";printf 'probe edit\n' >>$P/.agi/nodes/idea/n3.md;grid commit --all >/dev/null 2>&1;refs refs/grid/local-maxxing >$T/lmn.txt;chn=$(diff $T/lm0.txt $T/lmn.txt|grep -c '^>')
ok "m-writer-left-alone-reads-RED the config still pointing at refs/grid/local-maxxing: the probe moves $chn live ref(s) (1 = RED) and none of refs/grid/node" '[ "$chn" = 1 ]&&[ "$(refs $NS|cmp -s - $T/before.txt;echo $?)" = 0 ]'
# mutant: the hold cut out -> a fork (a fresh v1 root on the frozen ref's mint with no unify)
rm -rf $T/pf;cp -a $T/base $T/pf;P=$T/pf;setcfg $P "$CFG_NEW";mut $P/extensions/agi/bin/grid.py 'if not LEGACY_NS or not ref.startswith' 'if True or not ref.startswith'
printf 'probe edit\n' >>$P/.agi/nodes/idea/n3.md;grid commit --all >/dev/null 2>&1
ok "m-hold-cut-out-reads-RED without the hold a probe edit writes onto the frozen tip while the live history is not in it: the live tip is no ancestor of the new tip" '! $G -C $P merge-base --is-ancestor $(sha '$LNS'/'$M3') $(sha '$NS'/'$M3')'
# the guards: undeclared + nested namespace still refuses by name; legacy declared passes
rm -rf $T/pg;cp -a $T/base $T/pg;P=$T/pg;setcfg $P '{}';printf 'probe edit\n' >>$P/.agi/nodes/idea/n3.md;grid commit --all --allow-branch >$T/g1.out 2>&1;g1=$?
ok "g1-a-stale-config-still-refuses-by-name no storage_trunk and no legacy declaration with nested refs present: refused, no ref written" '[ $g1 != 0 ]&&grep -q "refusing commit" $T/g1.out&&[ "$(refs $NS|wc -l|tr -d " ")" = 25 ]'
# --- d: delete 0
rm -rf $T/pd;cp -a $T/base $T/pd;P=$T/pd;setcfg $P "$CFG_NEW";$G init -q --bare $T/remote.git;$G -C $P remote add origin $T/remote.git;$G -C $P push -q origin 'refs/grid/*:refs/grid/*' 2>&1
refs refs/grid/local-maxxing >$T/d0.txt;$G -C $T/remote.git for-each-ref --format='%(refname) %(objectname)' >$T/rem0.txt
grid unify --write >/dev/null 2>&1;grid push-changed >$T/push.out 2>&1;$G -C $P push --dry-run origin 'refs/grid/*:refs/grid/*' >$T/dry.push 2>&1;$G -C $T/remote.git for-each-ref --format='%(refname) %(objectname)' >$T/rem1.txt
ok "d0-legacy-refs-intact the live namespace has the same refs at the same tips after the unify (delete 0, 31/31)" 'refs refs/grid/local-maxxing|grep "local-maxxing/node"|cmp -s - $T/d0.txt'
nrw=0;while read r o;do n=$($G -C $T/remote.git rev-parse -q --verify $r);[ -n "$n" ]&&$G -C $T/remote.git merge-base --is-ancestor $o $n||nrw=$((nrw+1));done <$T/rem0.txt
ok "d1-push-dry-run-lists-0-deletes the land's refspecs: git push --dry-run lists no deleted ref, and every ref the remote had is still there with its old tip an ancestor of the new one ($nrw rewritten or lost, want 0)" '! grep -qi "deleted" $T/dry.push&&[ $nrw = 0 ]&&[ "$(wc -l <$T/rem1.txt|tr -d " ")" -ge "$(wc -l <$T/rem0.txt|tr -d " ")" ]'
ok "d2-push-changed-moved-the-new-namespace-only the 31 unified tips reached the remote and no legacy ref was touched: $(tail -1 $T/push.out)" '[ "$($G -C $T/remote.git for-each-ref refs/grid/node|wc -l|tr -d " ")" = 31 ]&&[ "$(grep "local-maxxing/node" $T/rem1.txt|sha256sum)" = "$(grep "local-maxxing/node" $T/rem0.txt|sha256sum)" ]'
# a legacy ref touched locally (a stale writer) is NOT pushed again; mutant: the old ns-wide prefix pushes it
$G -C $P update-ref $LNS/$(mintn 7) $(echo stale-writer|$G -C $P commit-tree $(sha $LNS/$(mintn 7)^{tree}) -p $(sha $LNS/$(mintn 7)));grid push-changed >$T/push2.out 2>&1
ok "d3-a-legacy-ref-never-pushes-again a local change under refs/grid/local-maxxing stays local (remote still has $(sha $LNS/$(mintn 7)|cut -c1-8)? no)" '[ "$($G -C $T/remote.git rev-parse $LNS/$(mintn 7))" != "$(sha $LNS/$(mintn 7))" ]'
rm -rf $T/pe;cp -a $T/pd $T/pe;P=$T/pe;mut $P/extensions/agi/bin/grid.py 'kinds = [f"{ns}/node", f"{ns}/session"]' 'kinds = [ns]';grid push-changed >/dev/null 2>&1
ok "m-ns-wide-push-reads-RED with the bare namespace prefix the locally changed legacy ref IS pushed" '[ "$($G -C $T/remote.git rev-parse $LNS/$(mintn 7))" = "$(sha $LNS/$(mintn 7))" ]'
# mutant: a delete-bearing variant of the verb
rm -rf $T/px;cp -a $T/base $T/px;P=$T/px;setcfg $P "$CFG_NEW";mut $P/extensions/agi/bin/grid.py '    return "merged"
' '    git(root, "update-ref", "-d", lref, ltip)
    return "merged"
';grid unify --write >/dev/null 2>&1
ok "m-delete-variant-reads-RED a verb that deletes the legacy ref leaves $(refs $LNS|wc -l|tr -d " ") of 31 live refs" '! refs refs/grid/local-maxxing|grep "local-maxxing/node"|cmp -s - $T/lm0.txt'
# --- c: the census cell
rm -rf $T/pc;cp -a $T/pa $T/pc;P=$T/pc;grid census >$T/c.out 2>&1;crc=$?
EXPECT_M=31;EXPECT_RET=$($G -C $P for-each-ref --format='%(objectname):node.md' $NS|$G -C $P cat-file --batch|grep -c '^status: deprecated')
ok "c0-five-numbers the cell prints mints=31 live=$((31-EXPECT_RET)) retired=$EXPECT_RET versions orphans=11 (mints 21..30 and TBD have no node file): $(cat $T/c.out)" '[ $crc = 0 ]&&grep -q "^grid census: mints=31 live=30 retired=1 versions=[0-9]* orphans=11$" $T/c.out&&[ "$(sed "s/.*versions=\([0-9]*\).*/\1/" $T/c.out)" = "$($G -C $P rev-list --count $(refs $NS|cut -d" " -f2))" ]'
refs $NS|sed "s|^$NS/||;s| .*||"|sort >$T/a.txt;$G -C $P grep -h '^mint_id:' HEAD -- .agi/nodes|sed 's/^mint_id: *//'|sort >$T/b.txt;orph=$(comm -23 $T/a.txt $T/b.txt|wc -l|tr -d ' ')
ok "c1-orphans-are-one-pinned-command the orphan count is the set difference of 'git grep -h ^mint_id: HEAD' against the namespace listing: $orph" '[ "$orph" = 11 ]'
grid census --rev no-such-rev >$T/c1.out 2>&1;c1=$?
ok "c2-a-failing-git-command-is-unread a bad revision prints unread and exits 1, never orphans=0: $(cat $T/c1.out)" '[ $c1 = 1 ]&&grep -q "^grid census: unread" $T/c1.out&&! grep -q "orphans=" $T/c1.out'
rm -rf $T/pc0;cp -a $T/pa $T/pc0;P=$T/pc0;for r in $($G -C $P for-each-ref --format='%(refname)' $LNS);do $G -C $P update-ref -d $r;done;grid census >$T/c2.out 2>&1;c2=$?
ok "c3-an-empty-legacy-listing-is-unread the declared legacy namespace listing 0 refs prints unread, rc 1: $(cat $T/c2.out)" '[ $c2 = 1 ]&&grep -q "unread (refs/grid/local-maxxing lists no node refs)" $T/c2.out'
rm -rf $T/pc1;cp -a $T/pa $T/pc1;P=$T/pc1;for r in $($G -C $P for-each-ref --format='%(refname)' $NS);do $G -C $P update-ref -d $r;done;grid census >$T/c3.out 2>&1;c3=$?
ok "c4-an-empty-new-namespace-is-unread the one namespace listing 0 refs prints unread, rc 1: $(cat $T/c3.out)" '[ $c3 = 1 ]&&grep -q "unread (refs/grid lists no node refs)" $T/c3.out'
rm -rf $T/pc2;cp -a $T/pc0 $T/pc2;P=$T/pc2;mut $P/extensions/agi/bin/grid.py 'or not res.stdout.split():' 'or False:';grid census >$T/c4.out 2>&1;c4=$?
ok "m-census-without-the-empty-check-reads-RED the check cut out: the empty legacy namespace prints numbers rc $c4 instead of unread" '[ $c4 = 0 ]&&grep -q "mints=" $T/c4.out'
echo "grid-namespace: $nrows rows";echo "grid-namespace: $f FAIL";[ $f = 0 ]
