#!/bin/sh
# lab-repack-loose.t.sh: goal:g7.16.1.14 A2 (E), the L-FIRE ('lab-repack.sh loose') + the counter's tmp_* line, council
# 3/3 18:05Z 11-17 (sp's (E); E1 all-is-one + sp's M2 amend; alive's de-dup; all-is-one's gap line). A scratch git repo
# as the test's own uid (AS_OWNER= SU= : no sudo, no lab, no NFS, 0 USD). ROOT=<tree> (or $1).
# Rows: e1 the four items on a repo of 3 packs + reachable loose + unreachable debris + a tmp_obj file (packs kept by
# inode, 0 loose after, every listed id reads back, the tmp file untouched, the gap >= WAIT_S between the two steps);
# m* one corrupt (0-byte) loose object: rc 4 twice, NO prune, ONE alarm naming it (de-dup), a green run clears the
# state; c* the counter counts objects, not tmp_*; x* mutants of the script, each must turn its row RED.
# Honest limits: NFS readers are not here (E2/E3 ran them on the lab, one sample each); nor a pack-objects killed partway.
R0=${ROOT:-${1:-$(cd "$(dirname "$0")/../../.." && pwd)}};S=$R0/extensions/agi/guard/lab-repack;T=$(mktemp -d);trap 'rm -rf "${T:?}"' 0;f=0
ok(){ if eval "$2";then echo "ok $1";else echo "FAIL $1";f=$((f+1));fi;}
export GIT_CONFIG_NOSYSTEM=1 HOME=$T/hm GIT_AUTHOR_NAME=t GIT_AUTHOR_EMAIL=t@t GIT_COMMITTER_NAME=t GIT_COMMITTER_EMAIL=t@t;mkdir -p $T/hm
# mk DIR: 3 packs (each repack, no -a/-d, packs only the new objects), 2 reachable loose commits, 3 unreachable blobs, a tmp_obj
mk(){ r=$1;git init -q $r;git -C $r config gc.auto 0;for i in 1 2 3;do echo $i >$r/f$i;git -C $r add f$i;git -C $r commit -qm c$i;git -C $r repack -q;done
  for i in 4 5;do echo $i >$r/f$i;git -C $r add f$i;git -C $r commit -qm c$i;done
  for i in a b c;do echo "debris $i" | git -C $r hash-object -w --stdin >/dev/null;done
  d=$r/.git/objects/$(ls $r/.git/objects | grep -E '^[0-9a-f]{2}$' | head -1);: >$d/tmp_obj_test;}
loose(){ find $1/.git/objects -mindepth 2 -maxdepth 2 -path '*/objects/[0-9a-f][0-9a-f]/*' ! -name 'tmp_*' | wc -l;}
inodes(){ find $1/.git/objects/pack -maxdepth 1 -name '*.pack' -printf '%i\n' | sort;}
# run SCRIPT REPO DIR: the loose mode as this uid; stdout+stderr -> DIR/out, rc in $rc
run(){ A1_H=$2 A1_D=$3 AS_OWNER= SU= WAIT_S=2 LSTATE=$3/state LALARM="cat >> $3/alarms" sh $1 loose >$3/out 2>&1;rc=$?;}
# ---- e1: the green L-fire
mk $T/r;inodes $T/r >$T/ino.before;git -C $T/r fsck --connectivity-only 2>/dev/null | sort >$T/dang.before;lb=$(loose $T/r)
mkdir -p $T/d1;run $S/lab-repack.sh $T/r $T/d1
ok "e1-rc0-loose-ok (rc $rc; want 0)" '[ $rc = 0 ] && grep -q "^== LOOSE OK" $T/d1/out'
ok "e1-loose-$lb-to-$(loose $T/r) (want 0 after; tmp_* is not an object)" '[ "$lb" -gt 0 ] && [ "$(loose $T/r)" = 0 ]'
ok "e1-old-packs-kept-by-inode ($(comm -12 $T/ino.before $(inodes $T/r >$T/ino.after; echo $T/ino.after) | wc -l) of 3)" '[ "$(comm -12 $T/ino.before $T/ino.after | wc -l)" = 3 ] && [ "$(wc -l <$T/ino.after)" = 4 ]'
ok "e1-tmp-obj-untouched" '[ "$(find $T/r/.git/objects -name tmp_obj_test | wc -l)" = 1 ]'
ok "e1-dangling-list-byte-equal (debris PACKED, not pruned)" 'git -C $T/r fsck --connectivity-only 2>/dev/null | sort | cmp -s - $T/dang.before && [ "$(grep -c "^dangling blob" $T/dang.before)" = 3 ]'
ok "e1-every-listed-id-reads-back" 'grep -q "listed ids read back $lb of $lb, missing 0" $T/d1/out'
ok "e1-gap-between-pack-objects-and-prune >= WAIT_S ($(sed -n "s/.*; gap \([0-9]*\) s.*/\1/p" $T/d1/out) s)" '[ "$(sed -n "s/.*; gap \([0-9]*\) s.*/\1/p" $T/d1/out)" -ge 2 ]'
ok "e1-no-alarm" '[ ! -s $T/d1/alarms ]'
# ---- m: one corrupt (0-byte) loose object
mk $T/m;b=$(echo corrupt | git -C $T/m hash-object -w --stdin);o=$T/m/.git/objects/$(echo $b | cut -c1-2)/$(echo $b | cut -c3-);rm -f $o;: >$o;lm=$(loose $T/m);mkdir -p $T/dm
run $S/lab-repack.sh $T/m $T/dm;r1=$rc;run $S/lab-repack.sh $T/m $T/dm;r2=$rc
ok "m1-rc4-both-runs ($r1 $r2)" '[ $r1 = 4 ] && [ $r2 = 4 ]'
ok "m2-no-prune ($lm loose kept: $(loose $T/m))" '[ "$(loose $T/m)" = "$lm" ] && grep -q "NO prune-packed" $T/dm/out && ! grep -q "prune-packed rc" $T/dm/out'
ok "m3-ONE-alarm-over-two-runs ($(wc -l <$T/dm/alarms 2>/dev/null || echo 0))" '[ "$(wc -l <$T/dm/alarms)" = 1 ] && grep -q "already alarmed" $T/dm/out'
ok "m4-the-alarm-names-the-bad-id" 'grep -q "$b" $T/dm/alarms'
rm -f $T/m/.git/objects/$(echo $b | cut -c1-2)/$(echo $b | cut -c3-);run $S/lab-repack.sh $T/m $T/dm
ok "m5-a-green-run-clears-the-state (rc $rc)" '[ $rc = 0 ] && [ ! -e $T/dm/state ]'
# ---- c: the counter counts objects, not tmp_* (L = the real loose count: counting the tmp file would FIRE)
mk $T/c;n=$(loose $T/c);: >$T/c/.git/FETCH_HEAD;mkdir -p $T/rt
H=$T/c/.git/objects K=50 L=$n F=999999 RUNTIME_DIRECTORY=$T/rt SELF=nobody-t AS=/nonexistent sh $S/agi-lab-pack-count >$T/cout 2>&1;rc=$?
ok "c1-tmp-obj-not-counted (L=$n, rc $rc; want 0 = no FIRE)" '[ $rc = 0 ]'
# ---- x: mutants, each must turn its row RED
sed 's/ | grep -E .\^\[0-9a-f\]{40}\$. | sort > \$ids/ | sort > $ids/' $S/lab-repack.sh >$T/x1.sh;mk $T/x1r;mkdir -p $T/x1d;run $T/x1.sh $T/x1r $T/x1d
ok "x1-no-hex-filter-is-RED (rc $rc; want != 0: pack-objects reads tmp_obj as an id)" '! cmp -s $S/lab-repack.sh $T/x1.sh && [ $rc != 0 ]'
sed 's/if \[ -f \$LSTATE \] \&\& cmp -s/if false \&\& cmp -s/' $S/lab-repack.sh >$T/x2.sh;mk $T/x2r;b=$(echo c2 | git -C $T/x2r hash-object -w --stdin);o=$T/x2r/.git/objects/$(echo $b | cut -c1-2)/$(echo $b | cut -c3-);rm -f $o;: >$o;mkdir -p $T/x2d
run $T/x2.sh $T/x2r $T/x2d;run $T/x2.sh $T/x2r $T/x2d
ok "x2-no-de-dup-is-RED (alarms $(wc -l <$T/x2d/alarms); want 2)" '! cmp -s $S/lab-repack.sh $T/x2.sh && [ "$(wc -l <$T/x2d/alarms)" = 2 ]'
sed 's/; sleep \$W$/; :/' $S/lab-repack.sh >$T/x3.sh;mk $T/x3r;mkdir -p $T/x3d;run $T/x3.sh $T/x3r $T/x3d
ok "x3-no-wait-is-RED (gap $(sed -n "s/.*; gap \([0-9]*\) s.*/\1/p" $T/x3d/out) s; want < 2)" '! cmp -s $S/lab-repack.sh $T/x3.sh && [ "$(sed -n "s/.*; gap \([0-9]*\) s.*/\1/p" $T/x3d/out)" -lt 2 ]'
sed "s/ ! -name 'tmp_\*' 2>>/ 2>>/" $S/agi-lab-pack-count >$T/x4;mk $T/x4r;n=$(loose $T/x4r);: >$T/x4r/.git/FETCH_HEAD;mkdir -p $T/rt4
H=$T/x4r/.git/objects K=50 L=$n F=999999 RUNTIME_DIRECTORY=$T/rt4 SELF=nobody-t AS=/nonexistent sh $T/x4 >$T/x4out 2>&1;rc=$?
ok "x4-counting-tmp-is-RED (rc $rc; want != 0: a FIRE whose delivery fails)" '! cmp -s $S/agi-lab-pack-count $T/x4 && [ $rc != 0 ]'
echo "lab-repack-loose: $f FAIL";exit $f
