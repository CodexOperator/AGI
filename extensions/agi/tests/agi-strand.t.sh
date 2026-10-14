#!/bin/sh
# agi-strand.t.sh [ROOT]: goal:g7.16.1.11.38 -- the strand guard, both doors, and the notice that reaches the POST. sh + git on SCRATCH repos (a fixture trunk, branch posts/alive, a DETACHED ~/t worktree, HOME / RUNTIME_DIRECTORY / AGI_WT in tmp); nothing live is touched; no network, no signing (the doors never sign).
# The pieces come from `sect NAME` of the .geometry/engine*.md of ROOT (default the working tree), or of PIECES=<file> (a candidate: any file holding `### name` headings with ~~~ fences). Never from ~/bin.
# ONE WRITE PATH (council 03:0xZ 10-11): agi-at alone writes posts/<post>. Neither door folds, rewrites or signs anything; both only REFUSE.
# Door 1 (pre-commit, git runs it from core.hooksPath=~/bin):
#   d1  a plain commit on a DETACHED ~/t HEAD is refused: rc != 0, the [detached] line names agi-at, no commit exists
#   d1b a commit in ANOTHER worktree that is detached (a post's w-* tree) lands          d1c a commit on an ATTACHED ~/t HEAD lands
#   d1d --no-verify lands (how the lane makes a stranded commit)                          d1e the piece chains to ~/hooks/pre-commit (a failing one refuses an attached commit)
# Door 2 (`agi-turn strand`, before the final `git checkout --detach` in agi-turn AND agi-flush):
#   s1 agi-flush, s2 agi-turn: HEAD carries a commit on NO ref -> [strand-refused] <post>: HEAD <sha> carries 1 commit(s), rc != 0, HEAD stays on the commit, posts/<post> is untouched (no fold)
#   s3 posts/<post> moved on elsewhere (a diverged tip): still refused, still not folded, the racer's tip is untouched
#   s4 the same commit reachable from ANOTHER ref (trunk ahead of the post): not a strand, rc 0, HEAD moves to the tip   s5 a clean ~/t: rc 0, no line   s6 an ATTACHED ~/t: ignored
# The other direction (a line the POST sees, not only the Stop hook's stderr):
#   o1 an uncommitted edit in ~/t -> [out-of-tree] on stderr AND in ~/.notice       n1 agi-meter prints each notice line ONCE (4 retries = 1 line) and clears the file; a second prompt prints nothing
#   n2 agi-brief calls the printer first   n3 CLAIM then print: a line appended WHILE the print runs lands in a fresh ~/.notice (kept for the next prompt); only the claimed lines are removed
#   b1 BOUNDED: 4 flushes of one strand + 2 turns of a growing out-of-tree = ONE line each (one line per label+sha)   b2 a DIFFERENT sha is a new line, the same sha is not   c1 a claim left by a crashed printer (~/.notice.PID) is printed with the next one
#   h1 core.hooksPath=~/bin makes EVERY piece name a git-hook candidate: no `### name` in engine*.md is a git hook name (githooks(5)) except pre-commit (Door 1) and reference-transaction (goal:g7.16.1.11.38.1, the ref guard)
#   r1 the notice survives the ROTATION path: the REAL unit ExecStartPre line (engine-root) runs against the scratch HOME, then the successor's first SessionStart (agi-brief) prints it on STDOUT first
# MUTANTS (PIECES=<engine*.md with the piece edited, each OLD text asserted count == 1): m1 both call sites `if agi-turn strand` -> `if :` (guard dropped: s1 s2 s3 RED) · m2 the `>>~/.notice` writes cut (stderr only: s1 o1 n1 RED) · m3 the pre-commit piece renamed away (d1 RED) · m4 the strand count against posts/<post> ONLY (s4 RED: a post sitting on the trunk would be refused every turn) · m5 the printer to stderr only (n1 n3 r1 RED: the model never reads it) · m6 print-then-truncate, no claim (n3 RED: the late append is lost) · m7 `add` without the key test (b1 b2 RED) · m8 a piece named post-checkout (h1 RED: git would run it after every checkout)
T=$(mktemp -d);trap 'rm -rf $T' 0;f=0;G=/usr/bin/git;R0=${ROOT:-${1:-$(cd "$(dirname "$0")/../../.." && pwd)}}
ok(){ if eval "$2";then echo "ok $1";else echo "FAIL $1";f=$((f+1));fi;}
sect(){ if [ -n "$PIECES" ];then cat "$PIECES";else cat $R0/.agi/nodes/.geometry/engine*.md;fi|sed -n "/^###* $1 /,/^###* /{/^~~~/,/^~~~/{//!p}}"; }
unset GIT_AUTHOR_NAME GIT_AUTHOR_EMAIL GIT_COMMITTER_NAME GIT_COMMITTER_EMAIL GIT_DIR GIT_WORK_TREE GIT_INDEX_FILE AGI_POST AGI_SEAT AGI_WT RUNTIME_DIRECTORY AGI_TRUNK
mkdir -p $T/hm $T/bin $T/run $T/wt
for n in agi-turn agi-flush agi-meter agi-brief agi-notice agi-sync pre-commit;do sect $n >$T/bin/$n;if [ -s $T/bin/$n ];then chmod +x $T/bin/$n;else rm -f $T/bin/$n;fi;done
ok x0-pieces-extracted '[ -x $T/bin/agi-turn ]&&[ -x $T/bin/agi-flush ]&&[ -x $T/bin/agi-meter ]&&[ -s $T/bin/agi-brief ]&&[ -x $T/bin/agi-notice ]&&[ -x $T/bin/pre-commit ]'
[ -x $T/bin/agi-turn ]&&[ -x $T/bin/agi-flush ]||{ echo "FAIL extract: agi-turn / agi-flush";exit 99;}
H=$T/hm;V=$H/t
# mk: a fresh fixture: trunk (one commit), posts/alive = trunk, ~/t = a detached worktree of it; core.hooksPath = the pieces dir, as the unit's .gitconfig sets it
mk(){ rm -rf $T/g $V $T/w2 $H/.notice $H/hooks;$G init -q -b trunk $T/g;g="$G -C $T/g -c user.name=x -c user.email=x@x -c commit.gpgsign=false";echo base >$T/g/README.md;$g add -A;$g commit -qm trunk;$g branch posts/alive trunk;$g worktree add -q --detach $V posts/alive;$G -C $T/g config core.hooksPath $T/bin;B0=$($G -C $T/g rev-parse posts/alive);}
run(){ (cd $V&&env -i PATH=$T/bin:/usr/bin:/bin HOME=$H GIT_CONFIG_GLOBAL=/dev/null GIT_CONFIG_SYSTEM=/dev/null AGI_POST=alive RUNTIME_DIRECTORY=$T/run AGI_WT=$T/wt "$@");}
gc(){ (cd ${CW:-$V}&&env -i PATH=$T/bin:/usr/bin:/bin HOME=$H GIT_CONFIG_GLOBAL=/dev/null GIT_CONFIG_SYSTEM=/dev/null $G -c user.name=x -c user.email=x@x -c commit.gpgsign=false commit -q "$@");}
tipb(){ $G -C $T/g rev-parse posts/alive;}
head1(){ $G -C $V rev-parse HEAD;}
# ---- Door 1
mk;gc --allow-empty -m plain 2>$T/e1;r=$?
ok d1-a-plain-commit-on-a-detached-t-is-refused "[ $r != 0 ]&&grep -qF '[detached] commit through: agi-at' $T/e1&&[ \"\$(head1)\" = $B0 ]&&[ \"\$($G -C $T/g rev-list --all --count)\" = 1 ]"
mk;$G -C $T/g worktree add -q --detach $T/w2 posts/alive;CW=$T/w2 gc --allow-empty -m other;r=$?
ok d1b-another-detached-worktree-is-untouched "[ $r = 0 ]&&[ \"\$($G -C $T/w2 rev-parse HEAD)\" != $B0 ]"
mk;$G -C $V switch -q posts/alive;gc --allow-empty -m attached;r=$?
ok d1c-an-attached-t-is-untouched "[ $r = 0 ]&&[ \"\$(tipb)\" != $B0 ]"
mk;gc --no-verify --allow-empty -m bypass;r=$?
ok d1d-no-verify-lands "[ $r = 0 ]&&[ \"\$(head1)\" != $B0 ]"
mk;mkdir -p $H/hooks;printf '#!/bin/sh\necho chained >&2;exit 7\n' >$H/hooks/pre-commit;chmod +x $H/hooks/pre-commit;$G -C $V switch -q posts/alive;gc --allow-empty -m chained 2>$T/e1;r=$?
ok d1e-the-piece-chains-to-the-hooks-dir "[ $r != 0 ]&&grep -qF chained $T/e1&&[ \"\$(tipb)\" = $B0 ]"
# ---- Door 2: s1 agi-flush, s2 agi-turn
for w in flush turn;do
 mk;gc --no-verify --allow-empty -m stranded;h=$(head1);run agi-$w >$T/o1 2>$T/e1;r=$?
 ok s-$w-1-a-stranded-commit-is-refused-by-name "[ $r != 0 ]&&grep -q '^\[strand-refused\] alive: HEAD $(echo $h|cut -c1-7)[0-9a-f]* carries 1 commit(s)' $T/e1&&[ \"\$(head1)\" = $h ]"
 ok s-$w-2-the-post-branch-is-not-folded "[ \"\$(tipb)\" = $B0 ]&&[ -z \"\$($G -C $T/g branch --contains $h)\" ]"
 ok s-$w-3-the-line-reaches-the-posts-notice "grep -q '^\[strand-refused\] alive: HEAD' $H/.notice"
done
mk;gc --no-verify --allow-empty -m stranded;h=$(head1);$G -C $T/g -c user.name=r -c user.email=r@r -c commit.gpgsign=false commit -q --allow-empty -m racer;rt=$(tipb)
(cd $T/g&&:);$G -C $T/g update-ref refs/heads/posts/alive $($G -C $T/g -c user.name=r -c user.email=r@r commit-tree -m racer2 -p $B0 $B0^{tree}) 2>/dev/null;rt=$(tipb)
run agi-flush >$T/o1 2>$T/e1;r=$?
ok s3-a-diverged-tip-is-refused-and-left-alone "[ $r != 0 ]&&grep -q '^\[strand-refused\]' $T/e1&&[ \"\$(head1)\" = $h ]&&[ \"\$(tipb)\" = $rt ]"
# s4: trunk ahead of posts/alive, ~/t detached ON the trunk commit: reachable from a ref, not a strand
mk;$G -C $T/g -c user.name=x -c user.email=x@x -c commit.gpgsign=false commit -q --allow-empty -m trunk2;$G -C $V checkout -q --detach trunk;run agi-flush >$T/o1 2>$T/e1;r=$?
ok s4-a-commit-on-another-ref-is-not-a-strand "[ $r = 0 ]&&! grep -q 'strand-refused' $T/e1&&[ \"\$(tipb)\" = \"\$($G -C $T/g rev-parse trunk)\" ]&&[ \"\$(head1)\" = \"\$(tipb)\" ]"
mk;run agi-flush >$T/o1 2>$T/e1;r=$?
ok s5-a-clean-t-passes-silently "[ $r = 0 ]&&[ ! -s $T/e1 ]&&[ ! -e $H/.notice ]"
mk;$G -C $V switch -q posts/alive;gc --allow-empty -m attached;run agi-flush >$T/o1 2>$T/e1;r=$?
ok s6-an-attached-t-is-ignored "[ $r = 0 ]&&! grep -q 'strand-refused' $T/e1"
# ---- the other direction
mk;echo draft >$V/note.txt;run agi-turn >$T/o1 2>$T/e1;r=$?
ok o1-an-unversioned-edit-reaches-stderr-and-the-notice "grep -q '^\[out-of-tree\] ~/t has 1 unversioned' $T/e1&&grep -q '^\[out-of-tree\] ~/t has 1 unversioned' $H/.notice"
mk;gc --no-verify --allow-empty -m stranded;h=$(head1);run agi-flush >/dev/null 2>&1;echo draft >$V/note.txt;run agi-turn >/dev/null 2>&1
echo '{}' >$T/pj;run sh -c "agi-meter <$T/pj" >$T/m1 2>/dev/null;run sh -c "agi-meter <$T/pj" >$T/m2 2>/dev/null
ok n1-agi-meter-prints-each-line-once-and-clears "[ \$(grep -c '^\[strand-refused\]' $T/m1) = 1 ]&&[ \$(grep -c '^\[out-of-tree\]' $T/m1) = 1 ]&&[ ! -e $H/.notice ]&&[ ! -s $T/m2 ]"
ok n2-agi-brief-prints-the-notice-first "[ \$(grep -c '^ls ~/.notice\* >/dev/null 2>&1&&agi-notice;p=' $T/bin/agi-brief) = 1 ]"
# n3: append-only until printed: a line appended WHILE the print runs (an awk shim that appends first) survives; only the lines printed are dropped
mk;mkdir -p $T/shimawk;printf '#!/bin/sh\necho "[late] kept" >>%s/.notice\nexec /usr/bin/awk "$@"\n' $H >$T/shimawk/awk;chmod +x $T/shimawk/awk;printf '[a] one\n[b] two\n' >$H/.notice
(cd $V&&env -i PATH=$T/shimawk:$T/bin:/usr/bin:/bin HOME=$H agi-notice) >$T/n3 2>/dev/null
ok n3-a-late-append-is-kept-and-only-printed-lines-are-dropped "[ \"\$(cat $T/n3)\" = '[a] one
[b] two' ]&&[ \"\$(cat $H/.notice)\" = '[late] kept' ]"
# r1: the notice survives the ROTATION path. The REAL unit line (engine-root: the ExecStartPre that extracts every piece, run at every restart; .fresh is removed by agi-run, agi-out touches only .ssh) runs against the scratch HOME; ~/.notice is still there, and the SUCCESSOR's first SessionStart (the freshly extracted agi-brief, stdin = the hook's JSON) prints it on STDOUT, before anything else
mk;GD=$V/.agi/nodes/.geometry;mkdir -p $GD $T/run/agi-alive $T/stub $H/.ssh;if [ -n "$PIECES" ];then cp $PIECES $GD/engine.md;else cp $R0/.agi/nodes/.geometry/engine*.md $GD/;fi
printf '#!/bin/sh\nsed -n "/^###* $1 /,/^###* /{/^~~~/,/^~~~/{//!p}}" %s/engine-post.md %s/engine.md\n' $GD $GD >$T/stub/sect;chmod +x $T/stub/sect
src(){ if [ -n "$PIECES" ];then cat "$PIECES";else cat $R0/.agi/nodes/.geometry/engine*.md;fi;}
src|sed -n "s/^ExecStartPre=sh -c '\(mkdir -p .ssh bin.*\)'\$/\1/p"|sed "s|%i|alive|g;s|%t|$T/run|g" >$T/unit37.sh
printf '[strand-refused] alive: HEAD abc1234 carries 1 commit(s) on no ref\n' >$H/.notice;touch $H/.fresh
(cd $H&&env -i PATH=/usr/bin:/bin HOME=$H sh $T/unit37.sh) >$T/u37.out 2>&1;u=$?
echo '{"source":"startup"}' >$T/sj;(cd $H&&env -i PATH=$T/stub:$H/bin:/usr/bin:/bin HOME=$H AGI_SEAT=alive AGI_POST=alive AGI_ROLE=director sh -c "agi-brief <$T/sj") >$T/br1 2>/dev/null
ok r1-the-notice-survives-the-restart-and-the-successors-first-sessionstart-prints-it "[ -s $T/unit37.sh ]&&[ $u = 0 ]&&[ -x $H/bin/agi-notice ]&&[ \"\$(sed -n 1p $T/br1)\" = '[strand-refused] alive: HEAD abc1234 carries 1 commit(s) on no ref' ]&&[ ! -e $H/.notice ]"
# h1: hooksPath=~/bin -- a piece named like a git hook would RUN as one (the lane's own PIECES / ROOT text is the list of piece names)
HOOKS=" applypatch-msg pre-applypatch post-applypatch pre-commit pre-merge-commit prepare-commit-msg commit-msg post-commit pre-rebase post-checkout post-merge pre-push pre-receive update proc-receive post-receive post-update reference-transaction push-to-checkout pre-auto-gc post-rewrite sendemail-validate fsmonitor-watchman p4-changelist p4-prepare-changelist p4-post-changelist p4-pre-submit post-index-change "
if [ -n "$PIECES" ];then cat "$PIECES";else cat $R0/.agi/nodes/.geometry/engine*.md;fi|grep -o '^### [^ ]*'|cut -c5- >$T/pnames
hk=;for n in $(cat $T/pnames);do case "$HOOKS" in *" $n "*)case $n in pre-commit|reference-transaction);;*)hk="$hk $n";;esac;; esac;done
ok h1-no-piece-is-named-like-a-git-hook-but-pre-commit-and-reference-transaction "[ -s $T/pnames ]&&[ -z '$hk' ]&&grep -qx pre-commit $T/pnames"
# b1 / b2 / c1: bounded, keyed, crash-safe
mk;gc --no-verify --allow-empty -m stranded;run agi-flush >/dev/null 2>&1;run agi-flush >/dev/null 2>&1;run agi-turn >/dev/null 2>&1;echo one >$V/n1.txt;run agi-turn >/dev/null 2>&1;echo two >$V/n2.txt;run agi-turn >/dev/null 2>&1
ok b1-a-stuck-condition-is-one-line-per-key "[ \$(grep -c '^\[strand-refused\]' $H/.notice) = 1 ]&&[ \$(grep -c '^\[out-of-tree\]' $H/.notice) = 1 ]"
mk;run agi-notice add '[strand-refused] alive: HEAD aaaaaaa carries 1 commit(s)';run agi-notice add '[strand-refused] alive: HEAD aaaaaaa carries 1 commit(s)';run agi-notice add '[strand-refused] alive: HEAD bbbbbbb carries 2 commit(s)'
ok b2-a-new-sha-is-a-new-line-the-same-sha-is-not "[ \$(wc -l <$H/.notice) = 2 ]"
mk;printf '[stale] left by a crashed printer\n' >$H/.notice.4242;run agi-notice add '[out-of-tree] ~/t has 1 unversioned change(s)';run agi-notice >$T/c1 2>/dev/null
ok c1-a-stale-claim-is-printed-and-removed "grep -q '^\[stale\]' $T/c1&&grep -q '^\[out-of-tree\]' $T/c1&&[ -z \"\$(ls $H/.notice* 2>/dev/null)\" ]"
echo "agi-strand: $f FAIL";exit $f
