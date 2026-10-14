#!/bin/sh
# agi-refguard.t.sh [ROOT]: goal:g7.16.1.11.38.1 -- the reference-transaction guard: a post's MISTAKE cannot move a peer's posts/<q>, refs/box/<q>/*, refs/held/<q>/*. sh + git + jq + ssh-keygen on a SCRATCH repo (never MAIN, never GIT_DIR on a live repo); the stub `id` in PATH names the user (agi-alive ...), so no second uid is needed; throwaway keys; no network.
# The pieces come from `sect NAME` of the .geometry/engine*.md of ROOT (default the working tree), or of PIECES=<file> (a candidate: any file holding `### name` headings with ~~~ fences). Never from ~/bin.
# TWO CONFIGS, as the goal's F1 says. A = a post's REAL config: HOME/.gitconfig is the gitconfig PIECE (core.hooksPath=~/bin; only the key paths are pointed at the scratch keys), the hook is the piece in HOME/bin, .git/hooks is EMPTY. B = an empty global config: GIT_CONFIG_GLOBAL=/dev/null, the hook is in the repo's .git/hooks (the MAIN install, belam's host act), HOME/bin has none.
# Rows (each under A and B where it applies):  f1 as agi-alive `update-ref refs/heads/posts/dg1` is refused: rc != 0, ONE named line, the ref UNCHANGED after git's abort  f1b its own posts/alive moves  f1c refs/box/dg1/*, refs/held/dg1/* and a DELETE of the peer's branch are refused; its own refs/box/alive/*, refs/held/alive/* move; one transaction naming own + peer is refused WHOLE (both unchanged)  f1d refs outside the three patterns move  f1e belam and root move a peer's ref (the exemption), and so does a user that is not agi-*  f1f another agi-<p> post user is refused  f1g the PRIME'S post (its unit runs as agi-belam, `systemctl show agi-post@belam -p User`) may move any ref: it answers for dead-ref cleanup and the held / box refs of the others
# Honesty (F2): f2 `git -c core.hooksPath=/dev/null update-ref` STILL moves the peer's ref -- the row passes only when the bypass works, so nobody reads the hook as a wall.
# Only `prepared` acts: np committed / aborted exit 0 at once, even on a matching line.
# No collateral (F3, config A): c1 the post's own `box send` (the REAL box piece, signed)  c2 its own `agi-at` on posts/alive (the REAL piece + grow.py, signed)  c3 a root `box carry` delivers a peer's refs/box/dg1/alive; the same fetch as agi-alive is REFUSED (the guard bites)  c4 a belam ff of the peer's branch  c5 FAIL OPEN: unparseable input, and a failing `id`, exit 0 with the [ref-guard] stderr line AND one line in ~/.notice (a second run the same day adds none)  c6 TIMING: the hook adds < 50 ms to one update-ref (mean of 30)
# Where it runs: h1 `git rev-parse --git-path hooks` under A is HOME/bin and the hook there is byte-equal to the piece.
# MUTANTS (PIECES=<engine*.md edited, each OLD text asserted count == 1): the piece renamed away; the `prepared` gate dropped; the q != p test dropped; the agi-* gate dropped; the fail-open `exit 0` -> `exit 1`; the notice write cut; the refs/held or refs/box arm cut.
T=$(mktemp -d);trap 'rm -rf $T' 0;f=0;G=/usr/bin/git;R0=${ROOT:-${1:-$(cd "$(dirname "$0")/../../.." && pwd)}}
ok(){ if eval "$2";then echo "ok $1";else echo "FAIL $1";f=$((f+1));fi;}
sect(){ if [ -n "$PIECES" ];then cat "$PIECES";else cat $R0/.agi/nodes/.geometry/engine*.md;fi|sed -n "/^###* $1 /,/^###* /{/^~~~/,/^~~~/{//!p}}"; }
unset GIT_AUTHOR_NAME GIT_AUTHOR_EMAIL GIT_COMMITTER_NAME GIT_COMMITTER_EMAIL GIT_DIR GIT_WORK_TREE GIT_INDEX_FILE AGI_POST AGI_SEAT AGI_WT RUNTIME_DIRECTORY AGI_TRUNK
mkdir -p $T/stub $T/binB $T/k $T/hm0 $T/hm/alive/bin
printf '#!/bin/sh\n[ "$FAKEDATE" ]&&{ echo "$FAKEDATE";exit 0;};exec /usr/bin/date "$@"\n' >$T/stub/date;chmod +x $T/stub/date
printf '#!/bin/sh\ncase "$*" in -un)[ "$IDFAIL" ]&&exit 1;echo "$STUBU";;*)exec /usr/bin/id "$@";;esac\n' >$T/stub/id;chmod +x $T/stub/id
for n in reference-transaction agi-notice box agi-at grow.py;do sect $n >$T/p.$n;[ -s $T/p.$n ]&&{ cp $T/p.$n $T/hm/alive/bin/$n;chmod +x $T/hm/alive/bin/$n;};done
cp $T/hm/alive/bin/agi-notice $T/binB/ 2>/dev/null
ok x0-pieces-extracted '[ -s $T/p.reference-transaction ]&&[ -x $T/hm/alive/bin/agi-notice ]&&[ -s $T/p.box ]&&[ -s $T/p.agi-at ]'
[ -s $T/p.reference-transaction ]||{ echo "FAIL extract: reference-transaction";exit 99;}
: >$T/signers;for u in alive belam;do ssh-keygen -q -t ed25519 -N '' -f $T/k/$u -C $u >/dev/null;echo "$u@agi namespaces=\"git\" $(cut -d' ' -f1,2 $T/k/$u.pub)">>$T/signers;done
sect gitconfig|sed "s|^allowedSignersFile=.*|allowedSignersFile=$T/signers|;s|^signingkey=.*|signingkey=$T/k/alive|;s|^email=.*|email=alive@agi|;s|^\[user\]|[user]\nname=alive|" >$T/hm/alive/.gitconfig
PRE="$G -c core.hooksPath=/dev/null -C $T/r"
$G init -q -b trunk $T/r;mkdir -p $T/r/.agi/nodes/.geometry
cat >$T/r/.agi/nodes/.geometry/posts.md<<'EOF'
  - {"name":"belam","parent":"owner","harness":"claude"}
  - {"name":"council","parent":"belam","members":["alive"]}
  - {"name":"alive","parent":"council","harness":"claude"}
  - {"name":"dg1","parent":"belam","harness":"claude"}
EOF
$PRE add -A;$PRE -c user.name=x -c user.email=x@x -c commit.gpgsign=false commit -qm fixture;C1=$($PRE rev-parse HEAD);C2=$(echo two|$PRE -c user.name=x -c user.email=x@x commit-tree -p $C1 $($PRE rev-parse HEAD^{tree}))
$PRE branch posts/alive $C1;$PRE branch posts/dg1 $C1
# rr CONFIG USER CMD...: run CMD in the scratch repo as post USER under config A or B; SU overrides the stub user name
rr(){ c=$1;u=$2;shift 2;if [ $c = A ];then H=$T/hm/$u;P=$T/stub:$H/bin;X=;else H=$T/hm0;P=$T/stub:$T/binB;X=GIT_CONFIG_GLOBAL=/dev/null;fi
 (cd $T/r&&env -i PATH=$P:/usr/bin:/bin HOME=$H STUBU=${SU:-agi-$u} AGI_POST=$u AGI_TRUNK=HEAD GIT_CONFIG_SYSTEM=/dev/null $X IDFAIL=$IDFAIL FAKEDATE=$FAKEDATE "$@");}
ref(){ $PRE rev-parse -q --verify $1 2>/dev/null||echo none;}
reset(){ $PRE update-ref refs/heads/posts/alive $C1;$PRE update-ref refs/heads/posts/dg1 $C1;for r in refs/box/dg1/alive refs/held/dg1/alive refs/box/alive/dg1 refs/held/alive/dg1 refs/heads/trunk2 refs/archive/x;do $PRE update-ref -d $r 2>/dev/null;done;:;}
for c in A B;do
 if [ $c = B ];then mkdir -p $T/r/.git/hooks;cp $T/p.reference-transaction $T/r/.git/hooks/reference-transaction;chmod +x $T/r/.git/hooks/reference-transaction;fi
 reset;rr $c alive $G update-ref refs/heads/posts/dg1 $C2 2>$T/e1;r=$?
 ok "$c-f1-a-peers-branch-is-refused-and-unchanged-after-the-abort" "[ $r != 0 ]&&grep -qF '[ref-guard] agi-alive may not move refs/heads/posts/dg1' $T/e1&&[ \"\$(ref refs/heads/posts/dg1)\" = $C1 ]"
 reset;rr $c alive $G update-ref refs/heads/posts/alive $C2 2>/dev/null;r=$?
 ok "$c-f1b-its-own-branch-moves" "[ $r = 0 ]&&[ \"\$(ref refs/heads/posts/alive)\" = $C2 ]"
 reset;a=0;for x in refs/box/dg1/alive refs/held/dg1/alive;do rr $c alive $G update-ref $x $C2 2>/dev/null&&a=$((a+1));done;rr $c alive $G update-ref -d refs/heads/posts/dg1 2>/dev/null&&a=$((a+1))
 printf 'update refs/heads/posts/alive %s\nupdate refs/heads/posts/dg1 %s\n' $C2 $C2|rr $c alive $G update-ref --stdin 2>/dev/null&&a=$((a+1))
 ok "$c-f1c-box-held-delete-and-a-mixed-transaction-are-refused-whole" "[ $a = 0 ]&&[ \"\$(ref refs/box/dg1/alive)\" = none ]&&[ \"\$(ref refs/held/dg1/alive)\" = none ]&&[ \"\$(ref refs/heads/posts/dg1)\" = $C1 ]&&[ \"\$(ref refs/heads/posts/alive)\" = $C1 ]"
 reset;rr $c alive $G update-ref refs/box/alive/dg1 $C2 2>/dev/null;r1=$?;rr $c alive $G update-ref refs/held/alive/dg1 $C2 2>/dev/null;r2=$?
 ok "$c-f1c2-its-own-box-and-held-refs-move" "[ $r1 = 0 ]&&[ $r2 = 0 ]&&[ \"\$(ref refs/box/alive/dg1)\" = $C2 ]"
 reset;rr $c alive $G update-ref refs/heads/trunk2 $C2 2>/dev/null;r1=$?;rr $c alive $G update-ref refs/archive/x $C2 2>/dev/null;r2=$?
 ok "$c-f1d-refs-outside-the-three-patterns-move" "[ $r1 = 0 ]&&[ $r2 = 0 ]"
 reset;SU=belam rr $c alive $G update-ref refs/heads/posts/dg1 $C2 2>/dev/null;r1=$?;SU=root rr $c alive $G update-ref refs/box/dg1/alive $C2 2>/dev/null;r2=$?;SU=owner rr $c alive $G update-ref refs/held/dg1/alive $C2 2>/dev/null;r3=$?
 ok "$c-f1e-belam-root-and-a-non-agi-user-are-exempt" "[ $r1 = 0 ]&&[ $r2 = 0 ]&&[ $r3 = 0 ]&&[ \"\$(ref refs/heads/posts/dg1)\" = $C2 ]"
 reset;SU=agi-sm rr $c alive $G update-ref refs/heads/posts/dg1 $C2 2>/dev/null;r=$?
 ok "$c-f1f-another-post-user-is-refused-too" "[ $r != 0 ]&&[ \"\$(ref refs/heads/posts/dg1)\" = $C1 ]"
 reset;SU=agi-belam rr $c alive $G update-ref refs/heads/posts/dg1 $C2 2>/dev/null;r1=$?;SU=agi-belam rr $c alive $G update-ref refs/box/dg1/alive $C2 2>/dev/null;r2=$?;SU=agi-belam rr $c alive $G update-ref refs/held/dg1/alive $C2 2>/dev/null;r3=$?
 ok "$c-f1g-the-Primes-post-runs-as-agi-belam-and-may-move-any-ref" "[ $r1 = 0 ]&&[ $r2 = 0 ]&&[ $r3 = 0 ]&&[ \"\$(ref refs/heads/posts/dg1)\" = $C2 ]"
done
reset;rr A alive $G -c core.hooksPath=/dev/null update-ref refs/heads/posts/dg1 $C2 2>/dev/null;r=$?
ok f2-the-bypass-still-moves-a-peers-ref-it-is-a-mistake-guard-not-a-wall "[ $r = 0 ]&&[ \"\$(ref refs/heads/posts/dg1)\" = $C2 ]"
reset;np=0;for st in committed aborted;do printf '%s %s refs/heads/posts/dg1\n' $C1 $C2|rr A alive sh $T/hm/alive/bin/reference-transaction $st 2>/dev/null||np=1;done
ok np-only-prepared-acts-committed-and-aborted-exit-0-on-a-matching-line "[ $np = 0 ]"
ok h1-under-the-real-config-git-resolves-hooks-to-HOME-bin-and-the-hook-there-is-the-piece "[ \"\$(rr A alive $G rev-parse --git-path hooks|sed 's|.*/hm/|/hm/|')\" = /hm/alive/bin ]&&cmp -s $T/hm/alive/bin/reference-transaction $T/p.reference-transaction"
# ---- no collateral (config A)
reset;rm -f $T/r/.git/hooks/reference-transaction
printf 'hello\n'|rr A alive sh $T/hm/alive/bin/box send belam 2>$T/c1.err;r=$?
ok c1-its-own-box-send-lands-signed "[ $r = 0 ]&&[ \"\$(ref refs/box/alive/belam)\" != none ]&&$G -C $T/r -c gpg.ssh.allowedSignersFile=$T/signers verify-commit refs/box/alive/belam >/dev/null 2>&1"
$PRE worktree add -q --detach $T/hm/alive/t posts/alive;echo x >$T/hm/alive/t/x.txt
rr A alive sh $T/hm/alive/bin/agi-at x.txt 2>$T/c2.err;r=$?
ok c2-its-own-agi-at-lands-signed-on-posts-alive "[ $r = 0 ]&&[ \"\$(ref refs/heads/posts/alive)\" != $C1 ]&&[ \"\$($G -C $T/r -c gpg.ssh.allowedSignersFile=$T/signers log -1 --format=%G? posts/alive)\" = G ]"
$G init -q --bare $T/hub;$PRE push -q $T/hub $C2:refs/box/dg1/alive;reset
SU=root rr A alive sh $T/hm/alive/bin/box carry $T/hub alive 2>/dev/null;r1=$?;v1=$(ref refs/box/dg1/alive);$PRE update-ref -d refs/box/dg1/alive
rr A alive sh $T/hm/alive/bin/box carry $T/hub alive 2>/dev/null;r2=$?;v2=$(ref refs/box/dg1/alive)
ok c3-a-root-box-carry-delivers-a-peers-ref-and-the-same-fetch-as-a-post-is-refused "[ \"$v1\" = $C2 ]&&[ \"$v2\" = none ]"
reset;SU=belam rr A alive $G update-ref refs/heads/posts/dg1 $C2 $C1 2>/dev/null;r=$?
ok c4-a-belam-ff-of-the-peers-branch-lands "[ $r = 0 ]&&[ \"\$(ref refs/heads/posts/dg1)\" = $C2 ]"
rm -f $T/hm/alive/.notice;printf 'garbage\n'|rr A alive sh $T/hm/alive/bin/reference-transaction prepared 2>$T/c5.err;r1=$?;printf 'garbage\n'|rr A alive sh $T/hm/alive/bin/reference-transaction prepared 2>/dev/null;r2=$?
ok c5-unparseable-input-fails-open-with-a-line-on-stderr-and-ONE-notice-per-day "[ $r1 = 0 ]&&[ $r2 = 0 ]&&grep -qF '[ref-guard] fail open: unparsed input' $T/c5.err&&[ \"\$(grep -c '^\[ref-guard\] fail open' $T/hm/alive/.notice)\" = 1 ]"
rm -f $T/hm/alive/.notice;FAKEDATE=20261011 rr A alive sh $T/hm/alive/bin/reference-transaction prepared </dev/null 2>/dev/null;printf 'garbage\n'|FAKEDATE=20261011 rr A alive sh $T/hm/alive/bin/reference-transaction prepared 2>/dev/null;printf 'garbage\n'|FAKEDATE=20261012 rr A alive sh $T/hm/alive/bin/reference-transaction prepared 2>/dev/null
ok c5c-the-notice-is-once-per-post-per-DAY-a-new-day-is-a-new-line "[ \"\$(grep -c '^\[ref-guard\] fail open' $T/hm/alive/.notice)\" = 2 ]"
rm -f $T/hm/alive/.notice;IDFAIL=1 rr A alive sh $T/hm/alive/bin/reference-transaction prepared </dev/null 2>$T/c5b.err;r=$?
ok c5b-a-failing-id-fails-open-and-is-noticed "[ $r = 0 ]&&grep -qF '[ref-guard] fail open: no user' $T/c5b.err&&grep -qF '[ref-guard] fail open: no user' $T/hm/alive/.notice"
reset;t0=$(date +%s%N);i=0;while [ $i -lt 30 ];do rr A alive $G -c core.hooksPath=/dev/null update-ref refs/heads/posts/alive $C2;rr A alive $G -c core.hooksPath=/dev/null update-ref refs/heads/posts/alive $C1;i=$((i+1));done;t1=$(date +%s%N)
i=0;while [ $i -lt 30 ];do rr A alive $G update-ref refs/heads/posts/alive $C2;rr A alive $G update-ref refs/heads/posts/alive $C1;i=$((i+1));done;t2=$(date +%s%N)
d=$(( ((t2-t1)-(t1-t0)) / 60000000 ))
ok c6-the-hook-adds-less-than-50-ms-to-one-update-ref "[ $d -lt 50 ]  # mean delta ${d} ms over 60 updates"
echo "agi-refguard: $f FAIL";exit $f
