#!/bin/sh
# agi-hook.t.sh [ROOT]: goal:g7.16.1.11.38.1, belam's host act 4c -- the root piece `agi-hook` installs the engine piece `reference-transaction` AS OF a landed sha into the repo's .git/hooks. sh + git on a SCRATCH repo (fixture engine-post.md at three commits, a trunk ref, a side branch); no root needed (the piece does not test the uid: run as root it writes root-owned files); nothing live is touched.
# The pieces come from `sect NAME` of the .geometry/engine*.md of ROOT (default the working tree), or of PIECES=<file> (a candidate). `sect` itself is extracted the same way and put on PATH, as the root unit has it.
# Rows: i1 an install at a landed sha writes EXACTLY `sect reference-transaction <sha>`, mode 755, and prints that file's sha256   i2 the same sha again: the same bytes, no .rt.* left behind   i3 a newer landed sha upgrades the bytes, by RENAME (a hard link taken before the upgrade still holds the OLD bytes: an in-place write would change both; git never reads a half-written hook)   i4 a sha NOT on the trunk (a side branch) is refused: rc 1, 'refused: ... not on the trunk', the installed hook unchanged   i5 a landed sha that carries no such piece is refused by name, the hook unchanged and no .rt.* left   i6 no sha prints the installed sha256 and writes nothing (mtime unchanged)   i7 a non-sha word is refused   i8 AGI_TRUNK unset fails (the piece never guesses the trunk)   i9 a NON-OWNER uid (GIT_TEST_ASSUME_DIFFERENT_OWNER=1: git's own 'dubious ownership' switch) installs the same bytes   i10 a dir git will not read is named as itself ('refused: git will not read'), never as 'not on the trunk', and nothing is written (rc 1 + the message carry the row; the dir check is a tripwire: nothing under the row's own dir, no $T/hooks; a non-root runner cannot create /hooks either way)
# MUTANTS (PIECES=<engine*.md edited, each OLD text asserted count == 1): the ancestor test dropped (i4) · the empty-piece test dropped (i5) · the rename replaced by an in-place write (i3) · chmod dropped (i1) · the AGI_TRUNK default added (i8) · the old plain git, no safe.directory (i9, i10)
T=$(mktemp -d);trap 'rm -rf $T' 0;f=0;G=/usr/bin/git;R0=${ROOT:-${1:-$(cd "$(dirname "$0")/../../.." && pwd)}}
ok(){ if eval "$2";then echo "ok $1";else echo "FAIL $1";f=$((f+1));fi;}
sect0(){ if [ -n "$PIECES" ];then cat "$PIECES";else cat $R0/.agi/nodes/.geometry/engine*.md;fi|sed -n "/^###* $1 /,/^###* /{/^~~~/,/^~~~/{//!p}}"; }
mkdir -p $T/bin;for n in agi-hook sect;do sect0 $n >$T/bin/$n;chmod +x $T/bin/$n;done
ok x0-pieces-extracted '[ -s $T/bin/agi-hook ]&&[ -s $T/bin/sect ]'
[ -s $T/bin/agi-hook ]&&[ -s $T/bin/sect ]||{ echo "FAIL extract";exit 99;}
unset GIT_DIR GIT_WORK_TREE GIT_INDEX_FILE AGI_TRUNK
R=$T/r;$G init -q -b trunk $R;g="$G -C $R -c user.name=x -c user.email=x@x -c commit.gpgsign=false -c core.hooksPath=/dev/null";mkdir -p $R/.agi/nodes/.geometry
piece(){ printf '# engine-post\n\n## files\n\n### reference-transaction (%s B)\n~~~sh\n#!/bin/sh\necho %s\n~~~\n' 0 "$1" >$R/.agi/nodes/.geometry/engine-post.md;}
printf '# engine-post\n\n## files\n\n### agi-at (3 B)\n~~~sh\nx\n~~~\n' >$R/.agi/nodes/.geometry/engine-post.md;$g add -A;$g commit -qm nopiece;C0=$($g rev-parse HEAD)
piece one;$g add -A;$g commit -qm one;C1=$($g rev-parse HEAD)
piece two;$g add -A;$g commit -qm two;C2=$($g rev-parse HEAD)
$g branch trunk2 $C2;$g checkout -q -b side $C1;piece side;$g add -A;$g commit -qm side;CS=$($g rev-parse HEAD);$g checkout -q trunk
H=$R/.git/hooks/reference-transaction
run(){ (cd $R&&env -i PATH=$T/bin:/usr/bin:/bin HOME=$T AGI_TRUNK=${TR-trunk} sh $T/bin/agi-hook "$@");}
want(){ (cd $R&&env -i PATH=$T/bin:/usr/bin:/bin sh $T/bin/sect reference-transaction $1);}
out=$(run $C1 2>$T/e);r=$?;want $C1 >$T/w1
ok i1-an-install-at-a-landed-sha-writes-exactly-the-piece-at-that-sha "[ $r = 0 ]&&cmp -s $H $T/w1&&[ \"\$(stat -c %a $H)\" = 755 ]&&[ \"\$out\" = \"\$(sha256sum <$H)\" ]&&grep -q one $H"
run $C1 >/dev/null 2>&1
ok i2-the-same-sha-again-is-the-same-bytes-and-leaves-no-temp "cmp -s $H $T/w1&&[ -z \"\$(ls -A $R/.git/hooks | grep '^\.rt\.')\" ]"
ln $H $T/oldhook;run $C2 >/dev/null 2>&1;want $C2 >$T/w2
ok i3-a-newer-landed-sha-upgrades-by-rename "cmp -s $H $T/w2&&grep -q two $H&&cmp -s $T/oldhook $T/w1"
sum0=$(sha256sum <$H);run $CS >/dev/null 2>$T/e4;r=$?
ok i4-a-sha-off-the-trunk-is-refused-and-nothing-changes "[ $r = 1 ]&&grep -q 'refused: .* is not on the trunk' $T/e4 2>/dev/null||{ [ $r = 1 ]&&run $CS 2>&1 | grep -q 'not on the trunk'; }&&[ \"\$(sha256sum <$H)\" = \"\$sum0\" ]"
out4=$(run $CS 2>&1);ok i4b-the-refusal-line-names-the-sha-and-the-trunk "echo \"\$out4\"|grep -q 'refused: $CS is not on the trunk'"
out5=$(run $C0 2>&1);r5=$?
ok i5-a-landed-sha-without-the-piece-is-refused-by-name "[ $r5 = 1 ]&&echo \"\$out5\"|grep -q 'refused: no reference-transaction at'&&[ \"\$(sha256sum <$H)\" = \"\$sum0\" ]&&[ -z \"\$(ls -A $R/.git/hooks | grep '^\.rt\.')\" ]"
m0=$(stat -c %Y.%N $H);out6=$(run 2>&1);r6=$?
ok i6-no-sha-prints-the-installed-sha256-and-writes-nothing "[ $r6 = 0 ]&&[ \"\$out6\" = \"\$sum0\" ]&&[ \"\$(stat -c %Y.%N $H)\" = \"$m0\" ]"
run zzz >/dev/null 2>&1;r7=$?
ok i7-a-non-sha-word-is-refused "[ $r7 = 1 ]&&[ \"\$(sha256sum <$H)\" = \"\$sum0\" ]"
(cd $R&&env -i PATH=$T/bin:/usr/bin:/bin HOME=$T sh $T/bin/agi-hook $C1 >/dev/null 2>&1);r8=$?
ok i8-no-AGI_TRUNK-is-a-failure-not-a-guess "[ $r8 != 0 ]&&[ \"\$(sha256sum <$H)\" = \"\$sum0\" ]"
rm -f $H;outo=$(cd $R&&env -i PATH=$T/bin:/usr/bin:/bin HOME=$T AGI_TRUNK=trunk GIT_TEST_ASSUME_DIFFERENT_OWNER=1 sh $T/bin/agi-hook $C1 2>&1);ro=$?;want $C1 >$T/w1
ok i9-a-non-owner-uid-installs-the-same-bytes "[ $ro = 0 ]&&cmp -s $H $T/w1&&[ \"\$outo\" = \"\$(sha256sum <$H)\" ]"
mkdir $T/nr;outn=$(cd $T/nr&&env -i PATH=$T/bin:/usr/bin:/bin HOME=$T AGI_TRUNK=trunk sh $T/bin/agi-hook $C1 2>&1);rn=$?
ok i10-a-dir-git-will-not-read-is-named-as-itself-and-writes-no-hook "[ $rn = 1 ]&&echo \"\$outn\"|grep -q 'refused: git will not read'&&! echo \"\$outn\"|grep -q 'not on the trunk'&&[ -z \"\$(ls -A $T/nr)\" ]&&[ ! -e $T/hooks ]"
echo "agi-hook: $f FAIL";exit $f
