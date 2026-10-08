#!/bin/sh
# box-carry.t.sh: AA1.M / M2 for the carrier (hypothesis g716111-aa1m-one-root-carrier-...) and the signers fix: sh + git + jq, scratch only, throwaway keys,
# ONE uid (AGI_RUN=none: every `as POST` is a plain call; the runuser pipe between real uids is HOST ACT 1, belam's GO). One ok/FAIL line per case; exit = number of FAILs.
# BOX CARRY SIGNERS = the piece files under test (default: `sect <piece>` read from the .geometry engine*.md of ROOT, the working tree)
T=$(mktemp -d);trap 'rm -rf $T' 0;f=0;G=/usr/bin/git;R0=${ROOT:-$(cd "$(dirname "$0")/../../.." && pwd)}
sect(){ cat $R0/.agi/nodes/.geometry/engine*.md|sed -n "/^###* $1 /,/^###* /{/^~~~/,/^~~~/{//!p}}";}
[ -n "$BOX" ]||{ sect box>$T/box;BOX=$T/box;};[ -n "$CARRY" ]||{ sect box-carry>$T/carry;CARRY=$T/carry;};[ -n "$SIGNERS" ]||{ sect agi-signers>$T/signers.sh;SIGNERS=$T/signers.sh;}
[ -s $BOX ]&&[ -s $CARRY ]&&[ -s $SIGNERS ]||{ echo "FAIL extract: box $(wc -c<$BOX) carry $(wc -c<$CARRY) signers $(wc -c<$SIGNERS)";exit 99;}
mkdir $T/bin;cat >$T/bin/sect<<XX
#!/bin/sh
$G -C $T/r show \${2:-HEAD}:.agi/nodes/.geometry/engine-post.md|sed -n "/^###* \$1 /,/^###* /{/^~~~/,/^~~~/{//!p}}"
XX
chmod +x $T/bin/sect
ok(){ if eval "$2";then echo "ok $1";else echo "FAIL $1";f=$((f+1));fi;}
# --- fixture: keys, signers, per-post gitconfig, a repo holding the matrix (rows carry their box cell), per-post bare stores on two boxes, one hub
mkdir $T/k $T/c;: >$T/allowed
for u in belam sm alive dg5;do ssh-keygen -q -t ed25519 -N '' -f $T/k/$u -C $u>/dev/null
 echo "$u@agi namespaces=\"git\" $(cut -d' ' -f1,2 $T/k/$u.pub)">>$T/allowed
 printf '[user]\n\tname=%s\n\temail=%s@agi\n\tsigningkey=%s\n[gpg]\n\tformat=ssh\n[gpg "ssh"]\n\tallowedSignersFile=%s\n[commit]\n\tgpgsign=false\n[safe]\n\tdirectory=*\n' $u $u $T/k/$u $T/allowed>$T/c/$u;done
$G init -q $T/r;mkdir -p $T/r/.agi/nodes/.geometry
cat >$T/r/.agi/nodes/.geometry/posts.md<<'XX'
  - {"name":"belam","parent":"owner","harness":"claude","box":"A"}
  - {"name":"council","parent":"belam","box":"A"}
  - {"name":"hang","parent":"council","harness":"claude","box":"A"}
  - {"name":"alive","parent":"council","harness":"claude","box":"A"}
  - {"name":"dg5","parent":"council","harness":"claude","box":"B"}
  - {"name":"sm","parent":"council","harness":"claude","box":"A"}
  - {"name":"dg1","parent":"sm","harness":"claude","box":"B"}
XX
cp $R0/.agi/nodes/.geometry/engine-post.md $T/r/.agi/nodes/.geometry/engine-post.md
$G -C $T/r add -A;$G -C $T/r -c user.name=x -c user.email=x@x commit -qm fixture;TR=$($G -C $T/r rev-parse HEAD)
# HEAD moves PAST the pin (read-at-pin): dg5 and dg1 flip to box A, and a() denies everything. Every case below must route by TR, never by HEAD.
sed -i 's/"name":"dg5","parent":"council","harness":"claude","box":"B"/"name":"dg5","parent":"council","harness":"claude","box":"A"/;s/"name":"dg1","parent":"sm","harness":"claude","box":"B"/"name":"dg1","parent":"sm","harness":"claude","box":"A"/' $T/r/.agi/nodes/.geometry/posts.md
sed -i 's/^a(){ .*$/a(){ return 1;}/' $T/r/.agi/nodes/.geometry/engine-post.md
$G -C $T/r add -A;$G -C $T/r -c user.name=x -c user.email=x@x commit -qm 'head past the pin';[ "$($G -C $T/r rev-parse HEAD)" != "$TR" ]||echo "FAIL fixture: HEAD == the pin" 
$G init -q --bare $T/hub.git
for b in A B;do mkdir -p $T/$b;done
for pb in belam:A hang:A alive:A sm:A dg5:B dg1:B;do u=${pb%:*};b=${pb#*:};$G init -q --bare $T/$b/$u/g.git;echo $T/r/.git/objects>$T/$b/$u/g.git/objects/info/alternates;done
# as BOX-LETTER POST ARGS...: the box script as POST in POST's own store, trunk pinned by sha
box(){ b=$1;u=$2;shift 2;(cd $T/$b/$u/g.git&&AGI_POST=$u AGI_TRUNK=$TR GIT_CONFIG_GLOBAL=$T/c/$u GIT_CONFIG_SYSTEM=/dev/null sh $BOX "$@");}
# carry BOX-LETTER ARGS: the carrier as root of that box (one uid: plain calls)
# CE (DG1 04:15Z, belam 04:14Z: the lane runs the REAL ownership): the carrier is root reading AGI_REPO (/data/work/agi, another uid's) and the stores; what lets it is the unit's own GIT_CONFIG_COUNT/KEY_0 words + the VALUE_0 that /etc/agi/carry.env holds (modelled here as `*`). So carry() runs with an EMPTY git config (but the hub path, below), git's different-owner seam and exactly those words, never an ambient ~/.gitconfig
printf '[safe]\n\tdirectory=%s\n' $T/hub.git >$T/hubcfg   # the hub is a stand-in for a REMOTE (no local-ownership rule there); git's file transport drops GIT_CONFIG_COUNT for the child receive-pack, so only the hub path is granted, by the global file
CE="GIT_CONFIG_GLOBAL=$T/hubcfg GIT_CONFIG_SYSTEM=/dev/null GIT_TEST_ASSUME_DIFFERENT_OWNER=1 $(sect agi-carry@.service|sed -n 's/^Environment=//p'|tr ' ' '\n'|grep '^GIT_CONFIG'|tr '\n' ' ')"
carry(){ b=$1;shift;PATH=$T/bin:$PATH AGI_RUN=${RUN:-none} AGI_BOX=$b AGI_STORES=$T/$b AGI_REPO=$T/r AGI_TRUNK=${TRK-$TR} AGI_HUB=${HUB-$T/hub.git} AGI_CARRY=$T/$b/carry.git ${CT:+timeout $CT} env $CE GIT_CONFIG_VALUE_0='*' sh $CARRY "$@";}
tip(){ $G -C $T/$1/$2/g.git rev-parse -q --verify $3||echo none;}
# --- k1: belam -> alive, same box: one carry, then alive reads it FROM ITS OWN STORE; held moves
echo order1|box A belam send alive;carry A belam 2>$T/k1.err
ok k1-delivered '[ "$(box A alive n|wc -l)" = 1 ]&&box A alive read|grep -qF "[belam] order1"&&[ "$(box A alive n|wc -l)" = 0 ]'
ok k1-no-stderr '[ ! -s $T/k1.err ]'
# --- k2: idempotent, no dup: a second carry with nothing new changes nothing; one more send arrives once
a=$(tip A alive refs/box/belam/alive);carry A belam;ok k2-idempotent '[ "$(tip A alive refs/box/belam/alive)" = "$a" ]'
echo order2|box A belam send alive;carry A belam;carry A belam
ok k2-once '[ "$(box A alive read|grep -c "^\[belam\] ")" = 1 ]'
# --- k3: a carrier for POST moves only POST'"'"'s own channels: carry sm leaves belam'"'"'s unsent-to-store message where it is
echo order3|box A belam send alive;b0=$(tip A belam refs/box/belam/alive);carry A sm
ok k3-only-own '[ "$(tip A alive refs/box/belam/alive)" != "$b0" ]'
carry A belam;ok k3-own-moves '[ "$(tip A alive refs/box/belam/alive)" = "$b0" ]'
# a post that plants someone else's channel in its OWN store gets it carried nowhere (the carrier forwards only refs/box/<POST>/*)
pl=$($G -C $T/A/sm/g.git commit-tree -m planted $($G -C $T/A/sm/g.git hash-object -w -t tree /dev/null));$G -C $T/A/sm/g.git update-ref refs/box/belam/dg5 $pl;carry A sm
ok k3b-planted-not-forwarded '! $G -C $T/hub.git rev-parse -q --verify refs/box/belam/dg5>/dev/null'
# a post-controlled REF NAME is data: a name carrying shell syntax is neither executed nor carried (local recipient, hub path, and as a sender component)
for nm in 'x;touch${IFS}PWN_LOCAL;alive' 'zz;touch${IFS}PWN_HUB;zz' '-x';do pw=$($G -C $T/A/sm/g.git commit-tree -m pwn $($G -C $T/A/sm/g.git hash-object -w -t tree /dev/null));$G -C $T/A/sm/g.git update-ref "refs/box/sm/$nm" $pw;done
(cd $T;carry A sm 2>/dev/null)
ok k3c-ref-name-not-executed '[ ! -e $T/PWN_LOCAL ]&&[ ! -e $T/PWN_HUB ]&&[ ! -e $T/A/PWN_LOCAL ]&&[ -z "$(find / -maxdepth 3 -name "PWN_*" -newer $T/r 2>/dev/null)" ]'
ok k3c-ref-name-not-carried '[ -z "$($G -C $T/hub.git for-each-ref refs/box/sm/ | grep -E "PWN|/-x")" ]&&[ -z "$($G -C $T/A/alive/g.git for-each-ref | grep PWN)" ]'
# the post-uid command failing must NEVER fall back to running it as root: a runuser that always fails + a git shim that logs: no call touches a post store
mkdir $T/fk;printf '#!/bin/sh\necho "$*">>%s/rulog\nexit 1\n' $T>$T/fk/runuser;printf '#!/bin/sh\necho "$*">>%s/gitlog\nexec %s "$@"\n' $T $G>$T/fk/git;chmod +x $T/fk/*;: >$T/gitlog
echo order5|box A belam send alive;(PATH=$T/fk:$PATH RUN=runuser carry A belam 2>/dev/null)
ok k3d-runuser-was-tried 'grep -q "agi-belam" $T/rulog'
ok k3d-no-root-fallback '! grep -q -E "/(belam|alive|sm|dg5)/g.git" $T/gitlog'
# an unreadable matrix exits non-zero (restart-bounds.t.sh a3-box-carry-a-missing-matrix); an unknown sender carries nothing and exits 0 -- goal:g1.41 A3: rc 1 restarted the unit every 5 s for a post absent at the pin
carry A ghost 2>/dev/null;ok k3e-unknown-sender-carries-nothing-and-exits-0 '[ $? = 0 ]'
# the matrix is read at a PINNED sha: an unpinned trunk (a ref, HEAD) refuses to run, and a refs/replace entry a post can write does not change a cell
echo m0|box A sm send alive;TRK=HEAD carry A sm 2>/dev/null;ok k0-unpinned-trunk-refused '[ "$(tip A alive refs/box/sm/alive)" = none ]'
old=$($G -C $T/r rev-parse $TR:.agi/nodes/.geometry/posts.md);nw=$($G -C $T/r cat-file -p $old|sed 's/"name":"dg1","parent":"sm","harness":"claude","box":"B"/"name":"dg1","parent":"sm","harness":"claude","box":"A"/'|$G -C $T/r hash-object -w --stdin);$G -C $T/r replace $old $nw
echo forge|box A sm send dg1;carry A sm 2>/dev/null;ok k0b-replace-ref-ignored '[ "$($G -C $T/hub.git rev-parse -q --verify refs/box/sm/dg1)" = "$(tip A sm refs/box/sm/dg1)" ]'
$G -C $T/r replace -d $old >/dev/null 2>&1
# hub-bound and hub-sourced refs are checked with the box's own a() (the LEVEL rule: same level or one apart; inert rows send and receive nothing): belam (level 1) and dg1 (level 3) are two apart
pl=$($G -C $T/A/belam/g.git commit-tree -m offm $($G -C $T/A/belam/g.git hash-object -w -t tree /dev/null));$G -C $T/A/belam/g.git update-ref refs/box/belam/dg1 $pl;carry A belam 2>/dev/null
ok k5c-hub-bound-off-level-not-pushed '! $G -C $T/hub.git rev-parse -q --verify refs/box/belam/dg1>/dev/null'
hp=$($G -C $T/hub.git commit-tree -m offh $($G -C $T/hub.git hash-object -w -t tree /dev/null));$G -C $T/hub.git update-ref refs/box/dg1/belam $hp;carry A --fetch 2>/dev/null
ok k5d-hub-sourced-off-level-not-delivered '[ "$(tip A belam refs/box/dg1/belam)" = none ]'
# and a pair ONE level apart still crosses to the hub (alive level 2 -> dg1 level 3, dg1 on box B): the gate is not a blanket refusal
pa=$($G -C $T/A/alive/g.git commit-tree -m onelevel $($G -C $T/A/alive/g.git hash-object -w -t tree /dev/null));$G -C $T/A/alive/g.git update-ref refs/box/alive/dg1 $pa;carry A alive 2>/dev/null
ok k5e-hub-bound-one-level-apart-pushed '[ "$($G -C $T/hub.git rev-parse -q --verify refs/box/alive/dg1)" = "$pa" ]'
# an unknown run mode delivers nothing
echo u|box A alive send sm;RUN=bogus carry A alive 2>/dev/null;ok k3f-unknown-run-mode-delivers-nothing '[ "$(tip A sm refs/box/alive/sm)" = none ]'
# a send that arrives while the carrier is running is not lost (the oneshot would coalesce it): the carrier re-scans until P's tips stop moving
mkdir $T/fk2;printf '#!/bin/sh\nif [ "$3" = pack-objects ]&&[ ! -e %s/late ];then touch %s/late;(cd %s/A/sm/g.git&&echo late|PATH=%s AGI_POST=sm AGI_TRUNK=%s GIT_CONFIG_GLOBAL=%s/c/sm GIT_CONFIG_SYSTEM=/dev/null sh %s send belam);fi\nexec %s "$@"\n' $T $T $T "$PATH" $TR $T $BOX $G>$T/fk2/git;chmod +x $T/fk2/git
echo first|box A sm send belam;(PATH=$T/fk2:$PATH carry A sm 2>/dev/null)
ok k4c-send-during-run-not-lost '[ "$(box A belam read|grep -c "^\[sm\] ")" = 2 ]'
# read-at-pin, both halves: HEAD's a() denies everything and HEAD flips dg5/dg1 to box A, the pin does not: the carrier must still deliver alive -> belam and route sm -> dg5 by the pin (k5)
echo pin|box A alive send belam;carry A alive 2>/dev/null;ok k0c-adjacency-read-at-the-pin '[ "$(tip A belam refs/box/alive/belam)" = "$(tip A alive refs/box/alive/belam)" ]&&[ "$(tip A alive refs/box/alive/belam)" != none ]'
# --- k4: a diverged tip in the recipient's store is refused, loud, and left as it is
box A alive read>/dev/null;x=$(GIT_AUTHOR_NAME=t GIT_AUTHOR_EMAIL=t@t GIT_COMMITTER_NAME=t GIT_COMMITTER_EMAIL=t@t $G -C $T/A/alive/g.git commit-tree -m diverge $($G -C $T/A/alive/g.git hash-object -w -t tree /dev/null));$G -C $T/A/alive/g.git update-ref refs/box/belam/alive $x
echo order4|box A belam send alive;carry A belam 2>$T/k4.err;rc=$?
ok k4-diverged-refused '[ "$(tip A alive refs/box/belam/alive)" = "$x" ]&&grep -q "^\[carry-failed\] refs/box/belam/alive" $T/k4.err'
# a tip the SENDER rewrote onto a sibling chain (a ref P moved by hand, not an extension of what Q holds) is refused by the ff check, never forced
box A alive read>/dev/null;$G -C $T/A/alive/g.git update-ref -d refs/box/belam/alive;carry A belam
y=$(tip A alive refs/box/belam/alive);[ "$y" = "$(tip A belam refs/box/belam/alive)" ]||echo '# k4b setup: alive not at belam tip';z=$(GIT_AUTHOR_NAME=t GIT_AUTHOR_EMAIL=t@t GIT_COMMITTER_NAME=t GIT_COMMITTER_EMAIL=t@t $G -C $T/A/belam/g.git commit-tree -m sibling $($G -C $T/A/belam/g.git hash-object -w -t tree /dev/null));$G -C $T/A/belam/g.git update-ref refs/box/belam/alive $z
carry A belam 2>$T/k4b.err;ok k4b-not-ff-refused '[ "$(tip A alive refs/box/belam/alive)" = "$y" ]&&grep -q "^\[carry-failed\] refs/box/belam/alive" $T/k4b.err'
# the tail window: tips that are STILL moving after the last pass make the carrier exit 75 (the unit restarts it), never a silent stop
mkdir $T/fk3;printf '#!/bin/sh\nif [ "$3" = pack-objects ];then (cd %s/A/sm/g.git&&echo late$$|PATH=%s AGI_POST=sm AGI_TRUNK=%s GIT_CONFIG_GLOBAL=%s/c/sm GIT_CONFIG_SYSTEM=/dev/null sh %s send belam);fi\nexec %s "$@"\n' $T "$PATH" $TR $T $BOX $G>$T/fk3/git;chmod +x $T/fk3/git
echo seed|box A sm send belam;(PATH=$T/fk3:$PATH carry A sm 2>$T/k4d.err);rc4d=$?;[ -n "$DBG" ]&&echo "# k4d rc=$rc4d sm->belam commits=$($G -C $T/A/sm/g.git rev-list --count refs/box/sm/belam) in belam store=$($G -C $T/A/belam/g.git rev-list --count refs/box/sm/belam) $(head -c 200 $T/k4d.err)";ok k4d-never-stable-exit-75 '[ $rc4d = 75 ]'
# --- k5: sm (box A) -> dg5 (box B) through the hub, and the reply back
echo hello-B|box A sm send dg5;carry A sm;carry B --fetch
ok k5-out '[ "$($G -C $T/hub.git rev-parse -q --verify refs/box/sm/dg5)" = "$(tip A sm refs/box/sm/dg5)" ]'
ok k5-delivered '[ "$(box B dg5 n|wc -l)" = 1 ]&&box B dg5 read|grep -qF "[sm] hello-B"'
echo reply-A|box B dg5 send sm;carry B dg5;carry A --fetch
[ -n "$DBG" ]&&{ echo "# k5 sm n: $(box A sm n|tr '\n' ' ')";}
ok k5-reply 'box A sm read|grep -qF "[dg5] reply-A"'
# the box-B sender's copy never lands in a store on box A except the recipient's, and a local pair never touches the hub
ok k5-local-not-pushed '! $G -C $T/hub.git rev-parse -q --verify refs/box/belam/alive>/dev/null'
# --- k6: no hub cell = a remote recipient is left in the sender'"'"'s store, nothing pushed, rc 0
echo lonely|box A sm send dg5;HUB= carry A sm 2>$T/k6.err;rc=$?;ok k6-no-hub '[ "$($G -C $T/hub.git rev-parse refs/box/sm/dg5)" != "$(tip A sm refs/box/sm/dg5)" ]&&[ $rc = 0 ]&&[ ! -s $T/k6.err ]'
# --- k8: the LOST WAKE (hypothesis g716111-aa1m-a-send-that-lands-after-the-carriers-last-scan...): a send that lands after the carrier's LAST for-each-ref of the sender's store and before its exit
# wakes nothing (systemd drops PathChanged while the oneshot runs). The shim wraps `git -C <sender store> for-each-ref`, runs the real call, THEN injects one send, so the carrier's last scan misses it.
# Calls are COUNTED first (a quiescent run = scan, re-scan, final check), then the injection fires on the LAST one. ONE sweep (box-carry --fetch) must carry it, with NO further send.
mkdir $T/fk8;printf '#!/bin/sh\nif [ "$3" = for-each-ref ]&&[ "$2" = %s/A/belam/g.git ];then n=$(cat %s/fk8/n 2>/dev/null||echo 0);n=$((n+1));echo $n>%s/fk8/n;%s "$@">%s/fk8/o;r=$?\n [ $n = "$(cat %s/fk8/want)" ]&&(cd %s/A/belam/g.git&&echo late$n|PATH=%s AGI_POST=belam AGI_TRUNK=%s GIT_CONFIG_GLOBAL=%s/c/belam GIT_CONFIG_SYSTEM=/dev/null sh %s send sm)\n cat %s/fk8/o;exit $r;fi\nexec %s "$@"\n' $T $T $T $G $T $T $T "$PATH" $TR $T $BOX $T $G>$T/fk8/git;chmod +x $T/fk8/git
echo 0>$T/fk8/want;echo seed8|box A belam send sm;rm -f $T/fk8/n;(PATH=$T/fk8:$PATH carry A belam 2>/dev/null);N=$(cat $T/fk8/n)
ok "k8-count the carrier's scans of a quiescent sender store are counted (N=$N: scan, re-scan, final)" '[ "$N" -ge 3 ]'
for HB in none hub;do
 if [ $HB = none ];then SW='HUB= carry A --fetch';else SW='carry A --fetch';fi
 echo late$HB|box A belam send sm;echo $N>$T/fk8/want;rm -f $T/fk8/n;(PATH=$T/fk8:$PATH carry A belam 2>$T/k8.err);rc=$?
 a=$(tip A belam refs/box/belam/sm);b=$(tip A sm refs/box/belam/sm);[ "$(cat $T/fk8/n)" = $N ]||echo "# k8 $HB: shim saw $(cat $T/fk8/n) scans, want $N"
 ok "k8-$HB-window-is-real the injected send is in the sender's store ($(echo $a|cut -c1-9)) but NOT in the recipient's ($(echo $b|cut -c1-9)) after the carrier exits 0 (rc=$rc)" '[ $rc = 0 ]&&[ "$a" != "$b" ]'
 eval "$SW" 2>/dev/null;c=$(tip A sm refs/box/belam/sm)
 ok "k8-$HB-sweep-carries ONE sweep (carry A --fetch$([ $HB = none ]&&echo ', no hub cell')) puts the sender's tip in the recipient's store with NO further send" '[ "$c" = "$a" ]'
 eval "$SW" 2>/dev/null;ok "k8-$HB-sweep-idempotent a second sweep changes nothing" '[ "$(tip A sm refs/box/belam/sm)" = "$c" ]'
done
# the sweep carries nothing the matrix refuses: a channel planted in sm's store under ANOTHER post's name (council -> alive: a ref alive does not hold yet, so only the carrier's own-prefix rule keeps it out) and a recipient the matrix does not know are both left alone
pl=$($G -C $T/A/sm/g.git commit-tree -m planted8 $($G -C $T/A/sm/g.git hash-object -w -t tree /dev/null));$G -C $T/A/sm/g.git update-ref refs/box/council/alive $pl;$G -C $T/A/sm/g.git update-ref refs/box/sm/ghost $pl
carry A --fetch 2>/dev/null
ok k8-sweep-planted-not-carried '[ "$(tip A alive refs/box/council/alive)" = none ]&&[ ! -e $T/A/ghost ]'
ok k8-sweep-ghost-not-pushed '[ -z "$($G -C $T/hub.git for-each-ref refs/box/sm/ghost)" ]&&[ "$($G -C $T/hub.git rev-parse -q --verify refs/box/council/alive||echo none)" != "$pl" ]'

# --- k9: a hung store of ONE post cannot starve the sweep: belam's store scan hangs 25 s, sm's send to belam must still be carried by the SAME sweep in well under that (each child is bounded: timeout 10)
mkdir $T/fk9;printf '#!/bin/sh\nif [ "$3" = for-each-ref ]&&[ "$2" = %s/A/belam/g.git ];then sleep 25;fi\nexec %s "$@"\n' $T $G>$T/fk9/git;chmod +x $T/fk9/git
echo late9|box A sm send belam;t9=$(date +%s);(PATH=$T/fk9:$PATH carry A --fetch 2>/dev/null);d9=$(( $(date +%s)-t9 ))
ok "k9-hung-child-bounded the sweep returned in ${d9}s (< 20) and sm's send to belam is in belam's store" '[ $d9 -lt 20 ]&&[ "$(tip A sm refs/box/sm/belam)" = "$(tip A belam refs/box/sm/belam)" ]'
# --- k11: the hub-less box with the install gate AS WRITTEN (mur sm17-dg3-lost-wake residue 1): the sweep lives in the --fetch pass, so a box with box.hub empty must still get agi-carry-fetch.timer ENABLED, or the closer never runs there.
# The REAL aa1m-install.sh `units` step on a scratch repo + scratch dirs (AGI_DRY_*), a stub systemctl that logs: no root, no unit touched.
INSTALL=${INSTALL:-$R0/.agi/context/local-maxxing/aa1m/aa1m-install.sh}
ins(){ hub=$1;I=$T/ins$2;mkdir -p $I/repo/.agi/nodes/.geometry $I/bin;cp $R0/.agi/nodes/.geometry/engine*.md $I/repo/.agi/nodes/.geometry/
 printf '{"box":{"alias":"A","hub":"%s","repo":"%s"}}\n' "$hub" $I/repo>$I/repo/.agi/config.json;printf '  - {"name":"belam","parent":"owner","harness":"claude","box":"A","engine":{"v":4}}\n  - {"name":"alive","parent":"belam","harness":"claude","box":"A","engine":{"v":4}}\n'>$I/repo/.agi/nodes/.geometry/posts.md
 $G -C $I/repo init -q 2>/dev/null;$G -C $I/repo add -A;$G -C $I/repo -c user.name=x -c user.email=x@x -c commit.gpgsign=false commit -qm i;it=$($G -C $I/repo rev-parse HEAD)
 printf '#!/bin/sh\necho "$*">>%s/sd.log\n' $I>$I/bin/systemctl;chmod +x $I/bin/systemctl;: >$I/sd.log
 (cd $I&&PATH=$I/bin:$PATH REPO=$I/repo AGI_DRY_OPT=$I/opt AGI_DRY_ETC=$I/etc AGI_DRY_SYSD=$I/sysd AGI_DRY_BOXREPO=$I/repo sh $INSTALL units $it >$I/out 2>$I/err);echo $?;}
rc=$(ins "" a)
ok "k11-install-ran the real install script's units step ran on the scratch repo (rc=$rc; per-post path units enabled: $(grep -c 'enable --now agi-carry@' $T/insa/sd.log))" '[ "$rc" = 0 ]&&[ "$(grep -c "enable --now agi-carry@" $T/insa/sd.log)" = 2 ]'
ok "k11-hubless-timer-enabled with box.hub EMPTY the fetch timer is still enabled (the sweep runs in that pass): sd.log has 'enable --now agi-carry-fetch.timer'" 'grep -q "enable --now agi-carry-fetch.timer" $T/insa/sd.log'
rc=$(ins "hub.example:agi/hub.git" b)
ok "k11-hub-timer-enabled with a hub cell the timer is enabled too (the gate is not narrowed)" '[ "$rc" = 0 ]&&grep -q "enable --now agi-carry-fetch.timer" $T/insb/sd.log'
ok "k11-no-unit-written-outside the dry run wrote units only under the scratch dir (4 units, nothing real)" '[ "$(ls $T/insa/sysd|wc -l|tr -d " ")" = 4 ]'
# --- k12: a post whose store HANGS must not starve the later posts. A git shim makes EVERY call on belam's store block (a FIFO ref does not: git skips it); ONE sweep (the sweep runs belam's child first, alive's after it in the matrix order)
# must still carry alive's send to sm. The whole sweep runs under an outer timeout of 25 s (the unit's own bound is 120 s): a per-child bound under ~15 s passes, an unbounded child is RED (the outer timeout kills it: rc 124).
mkdir -p $T/fk10;printf '#!/bin/sh\n[ "$2" = %s/A/hang/g.git ]&&exec sleep 40\nexec %s "$@"\n' $T $G>$T/fk10/git;chmod +x $T/fk10/git
echo late10|box A alive send sm;a10=$(tip A alive refs/box/alive/sm);b10=$(tip A sm refs/box/alive/sm)
t0=$(date +%s);(PATH=$T/fk10:$PATH CT=25 HUB= carry A --fetch >/dev/null 2>&1);rc10=$?;el=$(( $(date +%s)-t0 ))
ok "k12-sweep-returns the sweep returns inside 25 s although one post's store hangs (rc=$rc10, ${el}s; 124 = the outer timeout killed it)" '[ $rc10 != 124 ]&&[ $el -lt 25 ]'
ok "k12-later-post-carried the later post's send (alive -> sm) was carried by that one sweep (sender $(echo $a10|cut -c1-9), recipient $(echo $b10|cut -c1-9) -> $(tip A sm refs/box/alive/sm|cut -c1-9))" '[ "$a10" != "$b10" ]&&[ "$(tip A sm refs/box/alive/sm)" = "$a10" ]'
# --- k7: nothing outside the stores is written: no inbox file, no worktree change
ok k7-no-inbox-anywhere '[ -z "$(find $T -iname "*inbox*" -not -path "*/.git/*" 2>/dev/null)" ]'
ok k7-matrix-repo-untouched '[ -z "$($G -C $T/r status --porcelain)" ]&&[ "$(find $T/r -type f -not -path "*/.git/*"|wc -l)" = 2 ]'
# --- s1-s4: the signers fix (agi-signers): one root-owned file, append-only, old generations verify at their own date
mkdir -p $T/s/p/.ssh;ssh-keygen -q -t ed25519 -N '' -f $T/s/p/.ssh/id_ed25519 -C x>/dev/null;sg(){ AGI_RUN=none AGI_STORES=$T/s AGI_SIGNERS=$T/s/allowed sh $SIGNERS p;}
e0=$(date -u +%s);sg;sg;ok s1-once '[ "$(wc -l<$T/s/allowed)" = 1 ]&&grep -q "^p@agi namespaces=\"git\",valid-after=\"[0-9]*Z\" ssh-ed25519 " $T/s/allowed'
cp $T/s/p/.ssh/id_ed25519 $T/s/old;sleep 2;rm $T/s/p/.ssh/id_ed25519*;ssh-keygen -q -t ed25519 -N '' -f $T/s/p/.ssh/id_ed25519 -C y>/dev/null;sg;sg
ok s2-rotation-appends '[ "$(wc -l<$T/s/allowed)" = 2 ]&&[ "$(grep -c valid-before $T/s/allowed)" = 1 ]&&sed -n 1p $T/s/allowed|grep -q valid-before'
# the lock is real: while another process holds $F.lock the signers run BLOCKS (timeout), it neither appends nor skips
sz=$(wc -c<$T/s/allowed);flock $T/s/allowed.lock sleep 3&sleep 0.3;AGI_RUN=none AGI_STORES=$T/s AGI_SIGNERS=$T/s/allowed timeout 1 sh $SIGNERS p 2>/dev/null;ok s0-flock-blocks-while-locked '[ $? = 124 ]&&[ "$(wc -c<$T/s/allowed)" = $sz ]';wait
# a post-owned key file cannot add a line, a principal or an option: a 2-line file, a symlink to a root-only file and a non-ed25519 line are all refused and leave the file untouched
sz=$(wc -c<$T/s/allowed);mkdir -p $T/s/h/.ssh;kg=$(cut -d' ' -f1,2 $T/k/belam.pub)
printf '%s\nbelam@agi namespaces="git" %s\n' "$(cut -d' ' -f1,2 $T/s/p/.ssh/id_ed25519.pub)" "$kg">$T/s/h/.ssh/id_ed25519.pub;AGI_RUN=none AGI_STORES=$T/s AGI_SIGNERS=$T/s/allowed sh $SIGNERS h 2>/dev/null
ok s5-two-line-key-refused '[ $? != 0 ]&&[ "$(wc -c<$T/s/allowed)" = $sz ]'
# (a symlinked key file is read AS the post by runuser, so it cannot reach a root-only file: that needs two real uids = HOST ACT 1's probe, not this single-uid test)
echo 'ssh-rsa AAAAB3Nza x'>$T/s/h/.ssh/id_ed25519.pub;AGI_RUN=none AGI_STORES=$T/s AGI_SIGNERS=$T/s/allowed sh $SIGNERS h 2>/dev/null
ok s7-non-ed25519-refused '[ $? != 0 ]&&[ "$(wc -c<$T/s/allowed)" = $sz ]'
# a huge key line is refused (a post cannot make root append megabytes) and a valid-looking prefix of one is not taken for a key
sz=$(wc -c<$T/s/allowed);{ printf 'ssh-ed25519 AAAAC3NzaC1lZDI1NTE5';head -c 2000000 /dev/zero|tr '\0' A;echo;}>$T/s/h/.ssh/id_ed25519.pub;AGI_RUN=none AGI_STORES=$T/s AGI_SIGNERS=$T/s/allowed sh $SIGNERS h 2>/dev/null
ok s9-huge-key-refused '[ "$(wc -c<$T/s/allowed)" = $sz ]'
# an unknown run mode never runs anything as root
AGI_RUN=bogus AGI_STORES=$T/s AGI_SIGNERS=$T/s/allowed sh $SIGNERS p 2>/dev/null;ok s10-unknown-run-mode-refused '[ $? != 0 ]'
ok s8-allowed-only-own-principals '[ "$(cut -d@ -f1 $T/s/allowed|sort -u|tr "\n" " ")" = "p " ]'
# a post-planted bin/date (its unit PATH puts /var/lib/agi/<p>/bin first) is NOT run by agi-signers, which runs as root: it sets its own PATH
mkdir -p $T/s/q/.ssh $T/s/q/bin;ssh-keygen -q -t ed25519 -N '' -f $T/s/q/.ssh/id_ed25519 -C q>/dev/null;printf '#!/bin/sh\ntouch %s\n' $T/s/q/ran>$T/s/q/bin/date;chmod +x $T/s/q/bin/date
PATH=$T/s/q/bin:$PATH AGI_RUN=none AGI_STORES=$T/s AGI_SIGNERS=$T/s/allowed sh $SIGNERS q 2>/dev/null;ok s11-planted-date-not-run '[ $? = 0 ]&&[ ! -e $T/s/q/ran ]&&grep -q "^q@agi " $T/s/allowed'
# signed commits: the OLD key at a date inside its window verifies; the OLD key dated after valid-before is refused; the NEW key now verifies
$G init -q $T/s/v;vc(){ k=$1;d=$2;(cd $T/s/v&&GIT_AUTHOR_DATE=$d GIT_COMMITTER_DATE=$d GIT_AUTHOR_EMAIL=p@agi GIT_COMMITTER_EMAIL=p@agi $G -c gpg.format=ssh -c user.signingkey=$k commit-tree -S -m m $($G hash-object -w -t tree /dev/null));}
vk(){ (cd $T/s/v&&$G -c gpg.ssh.allowedSignersFile=$T/s/allowed verify-commit --raw $1 2>&1|grep -q "for p@agi with");}
oc=$(vc $T/s/old "@$((e0+1))");oa=$(vc $T/s/old "@$(( $(date -u +%s)+3600 ))");nc=$(vc $T/s/p/.ssh/id_ed25519 "@$(( $(date -u +%s)+3 ))")
ok s3-old-key-in-its-window 'vk $oc'
ok s3-old-key-after-valid-before-refused '! vk $oa'
ok s4-new-key-verifies 'vk $nc'
# --- negative: no Python, no cron, no inbox path, no polling loop for LOCAL delivery in the carrier or the signers piece
ok u1a-signers-unit-lines-env-i 'RT=$R0/.agi/nodes/.geometry/engine-root.md;[ "$(grep -c "^ExecStartPre=.*agi-signers" $RT)" = 2 ]&&[ "$(grep -c "^ExecStartPre=+/usr/bin/env -i PATH=/usr/sbin:/usr/bin:/bin /opt/agi/bin/agi-signers %i\$" $RT)" = 2 ]'
ok u1b-last-signers-line-after-agi-out 'RT=$R0/.agi/nodes/.geometry/engine-root.md;o=$(grep -n "^ExecStartPre=.*agi-out" $RT|tail -1|cut -d: -f1);l=$(grep -n "^ExecStartPre=.*agi-signers" $RT|tail -1|cut -d: -f1);[ -n "$o" ]&&[ -n "$l" ]&&[ "$l" -gt "$o" ]&&[ "$(grep -c "^ExecStartPre=.*agi-out" $RT)" = 1 ]'
ok n1-no-python '! grep -qi python $CARRY $SIGNERS'
ok n2-no-cron-no-inbox '! grep -q -E "cron|sessions/inbox" $CARRY $SIGNERS'
ok n3-no-polling-loop '! grep -q -E "sleep|while :|while true|until " $CARRY'
ok "k8-bytes the carrier piece is <= 3255 B ($(wc -c<$CARRY) B now)" '[ $(wc -c<$CARRY) -le 3255 ]'
echo "# box-carry $(wc -c<$CARRY) B · agi-signers $(wc -c<$SIGNERS) B"
exit $f
