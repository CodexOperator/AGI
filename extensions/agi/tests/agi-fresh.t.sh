#!/bin/sh
# agi-fresh.t.sh: AA2 per-generation keys, ONE-BOX half (hypothesis g716111-aa2-a-key-is-fresh-per-generation-and-the-root-ring-appends-once): sh + git + ssh-keygen only, a SCRATCH home, a SCRATCH ring, AGI_RUN=none, NO live key.
# It runs the REAL post unit's ExecStartPre (extracted from the agi-post@.service block of engine-root.md, %i -> the post, %t -> a scratch run dir) and the REAL agi-signers piece (the ring writer), as the unit would at each start:
#   up      = the unit's ExecStartPre line, then agi-signers POST        (agi-run then consumes ~/.fresh: simulated by rm)
#   crash   = up with NO ~/.fresh        out-line = touch ~/.fresh, then up
# (A3.2 split the user steps in two, key step then the rest, with the root agi-signers line between: the default JOINS the sh -c lines into the one script this test models.)
# STEPS = the unit's ExecStartPre lines in file order (default: from engine-root.md of ROOT; a reorder mutation = STEPS=<edited copy>).
# UNIT = the joined sh -c lines (bytes / no-ring-write cases) (default: the `sh -c` line of the unit in .geometry/engine-root.md of ROOT); a mutation = UNIT=<file holding the edited line>. One ok/FAIL line per case; exit = FAIL count.
T=$(mktemp -d);trap 'rm -rf $T' 0;f=0;G=/usr/bin/git;R0=${ROOT:-$(cd "$(dirname "$0")/../../.." && pwd)};GEO=$R0/.agi/nodes/.geometry;CEIL=${CEIL:-828}
sect(){ cat $GEO/engine*.md|sed -n "/^###* $1 /,/^###* /{/^~~~/,/^~~~/{//!p}}";}
[ -n "$UNIT" ]||{ sed -n "/^### agi-post@.service/,/^~~~\$/{/^ExecStartPre=sh -c /p}" $GEO/engine-root.md|awk -v q="'" 'NR==1{sub(q"$","");printf "%s",$0;next}{sub("^ExecStartPre=sh -c "q,"");printf ";%s",$0}END{print ""}'>$T/unit;UNIT=$T/unit;}
[ -n "$STEPS" ]||{ sed -n "/^### agi-post@.service/,/^~~~\$/{/^ExecStartPre=/p}" $GEO/engine-root.md>$T/steps;STEPS=$T/steps;}
sect agi-signers>$T/signers.sh;[ -s $STEPS ]||{ echo "FAIL extract: no ExecStartPre lines";exit 99;}
[ -s $UNIT ]&&[ -s $T/signers.sh ]||{ echo "FAIL extract: unit $(wc -c<$UNIT) B, signers $(wc -c<$T/signers.sh) B";exit 99;}
ok(){ if eval "$2";then echo "ok $1";else echo "FAIL $1";f=$((f+1));fi;}
unset GIT_AUTHOR_NAME GIT_AUTHOR_EMAIL GIT_COMMITTER_NAME GIT_COMMITTER_EMAIL GIT_DIR GIT_WORK_TREE GIT_CONFIG_GLOBAL GIT_CONFIG_SYSTEM AGI_TRUNK
P=post1;S=$T/stores;H=$S/$P;RING=$T/ring;RUN=$T/run;mkdir -p $H $RUN/agi-$P;O=$T/main
# the scratch MAIN repo: the real engine pieces (the unit's loop writes bin/* from engine.md + engine-[pw]*.md of the worktree)
$G init -q $O;mkdir -p $O/.agi/nodes/.geometry;for x in engine.md engine-post.md engine-wrap.md;do cp $GEO/$x $O/.agi/nodes/.geometry/;done
$G -C $O add -A;$G -C $O -c user.name=x -c user.email=x@x -c commit.gpgsign=false commit -qm fixture;TR=$($G -C $O rev-parse HEAD)
# the unit line as sh would get it: the quoted script, %i and %t substituted
Q=$(sed 's/^ExecStartPre=sh -c //' $UNIT|sed "s,%i,$P,g;s,%t,$RUN,g")
up(){ (cd $H&&export HOME=$H GIT_TEST_ASSUME_DIFFERENT_OWNER=1 GIT_CONFIG_SYSTEM=/dev/null O=$O AGI_TRUNK=$TR PATH=$H/bin:$PATH&&while IFS= read -r l;do case $l in "ExecStartPre=sh -c "*)q=$(printf %s "${l#ExecStartPre=sh -c }"|sed "s,%i,$P,g;s,%t,$RUN,g");eval "sh -c $q" >>$T/up.out 2>>$T/up.err;;"ExecStartPre=+"*agi-signers*)AGI_RUN=none AGI_STORES=$S AGI_SIGNERS=$RING sh $T/signers.sh $P;;esac;done<$STEPS);}
# up = every ExecStartPre line of the unit IN FILE ORDER (key step, root agi-signers, the rest): a reorder of the lines changes what runs first and is RED below
agirun(){ rm -f $H/.fresh;}
pub(){ cut -d' ' -f1,2 $H/.ssh/id_ed25519.pub;}
lines(){ [ -f $RING ]&&wc -l<$RING|tr -d ' '||echo 0;}
# commit as the post, signed by a given private key, dated at epoch $2, in a scratch repo; prints the sha
mkdir $T/v;$G init -q $T/v
vc(){ (cd $T/v&&GIT_AUTHOR_DATE=@$2 GIT_COMMITTER_DATE=@$2 GIT_AUTHOR_NAME=$P GIT_COMMITTER_NAME=$P GIT_AUTHOR_EMAIL=$P@agi GIT_COMMITTER_EMAIL=$P@agi $G -c gpg.format=ssh -c user.signingkey=$1 commit-tree -S -m m $($G hash-object -w -t tree /dev/null));}
# vk SHA: git verify-commit's EXIT STATUS decides (a refused signature still prints "Good git signature" with no principal), its text lands in $T/vk.out
vk(){ (cd $T/v&&$G -c gpg.ssh.allowedSignersFile=$RING verify-commit $1>$T/vk.out 2>&1);}
# --- the ORDER the unit runs its steps in (mur sm17 R3: a reorder of the key / signers / rest lines stayed green): key step, then the root agi-signers, then the rest (worktree, bin, .signers)
ko=$(grep -n 'ssh-keygen' $STEPS|head -1|cut -d: -f1);so=$(grep -n 'ExecStartPre=+.*agi-signers' $STEPS|head -1|cut -d: -f1);ro=$(grep -n 'worktree add' $STEPS|head -1|cut -d: -f1)
ok "order-key-signers-rest the unit's lines are in the order key step ($ko), root agi-signers ($so), the rest ($ro)" '[ -n "$ko" ]&&[ -n "$so" ]&&[ -n "$ro" ]&&[ "$ko" -lt "$so" ]&&[ "$so" -lt "$ro" ]'
ok "order-signers-is-root the ring writer is a root step (ExecStartPre=+) with a scrubbed env (env -i)" 'sed -n "${so}p" $STEPS|grep -q "^ExecStartPre=+/usr/bin/env -i "'
# --- generation 0: the first start (no key, no worktree: the unit makes both and touches .fresh); the ring gets ONE line
up;agirun;K0=$(pub);cp $H/.ssh/id_ed25519 $T/key0;e0=$(date -u +%s)
ok "g0-first-start the first start makes the key and the worktree, and the ring holds exactly 1 line (got $(lines))" '[ -n "$K0" ]&&[ -d $H/t ]&&[ "$(lines)" = 1 ]'
# --- (a) a CRASH restart (no .fresh): the key is kept, the ring appends 0 lines
up;agirun;ok "a-crash-keeps-key a crash restart (no .fresh) keeps the same key" '[ "$(pub)" = "$K0" ]'
ok "a-crash-appends-0 and appends 0 ring lines (still $(lines))" '[ "$(lines)" = 1 ]'
up;agirun;ok "a-crash-twice two crash restarts in a row change nothing" '[ "$(pub)" = "$K0" ]&&[ "$(lines)" = 1 ]'
# --- (a) an OUT-LINE (.fresh): the key is dropped BEFORE keygen, so the successor holds a NEW key; the ring appends exactly 1 line and stamps valid-before on the previous one
sleep 2;touch $H/.fresh;e1=$(date -u +%s);up;agirun;K1=$(pub)
ok "a-fresh-new-key an out-line (.fresh) gives the successor a NEW key (old ...$(echo $K0|rev|cut -c1-6|rev), new ...$(echo $K1|rev|cut -c1-6|rev))" '[ -n "$K1" ]&&[ "$K1" != "$K0" ]'
ok "a-fresh-ring-appends-1 and the ring holds exactly 2 lines (got $(lines))" '[ "$(lines)" = 2 ]'
ok "a-fresh-valid-before the previous line is stamped valid-before and the new one is not; the new one carries valid-after" 'sed -n 1p $RING|grep -q valid-before&&! sed -n 2p $RING|grep -q valid-before&&sed -n 2p $RING|grep -q "valid-after="'
ok "a-fresh-principal both ring lines are for $P@agi (the principal form)" '[ "$(cut -d" " -f1 $RING|sort -u)" = $P@agi ]'
up;agirun;ok "a-crash-after-fresh a crash restart AFTER the rotation keeps the NEW key and appends 0 (still $(lines))" '[ "$(pub)" = "$K1" ]&&[ "$(lines)" = 2 ]'
ok "a-no-leftover the dropped generation left no key file under another name in .ssh" '[ "$(ls $H/.ssh|sort|tr "\n" " ")" = "id_ed25519 id_ed25519.pub " ]'
# --- the window between the unit's ExecStartPre and agi-run (which consumes .fresh): a start that FAILS there is retried (Restart=always) with .fresh still present. The retry must not mint ANOTHER key:
# one out-line = one generation = ONE ring line, however many times its start is retried (a naive 'drop the key whenever .fresh exists' appends a line per retry)
sleep 2;touch $H/.fresh;up;K2=$(pub);n2=$(lines);sleep 1;up;up
ok "a-fresh-retry-idempotent an out-line whose start is RETRIED twice before agi-run consumes .fresh keeps the key made by its first attempt and adds exactly 1 ring line in all (key same: $([ "$(pub)" = "$K2" ]&&echo yes||echo NO); ring $n2 -> $(lines))" '[ "$K2" != "$K1" ]&&[ "$(pub)" = "$K2" ]&&[ "$n2" = 3 ]&&[ "$(lines)" = 3 ]'
agirun
# --- a FIRST start that dies before agi-run (mur sm17 R1): its retry has .fresh from the first attempt and a key made after it: the retry keeps that key, ONE ring line
P1=$P;H1=$H;Q1=$Q;RING1=$RING;P=post2;H=$S/$P;RING=$T/ring2;mkdir -p $H $RUN/agi-$P;Q=$(sed 's/^ExecStartPre=sh -c //' $UNIT|sed "s,%i,$P,g;s,%t,$RUN,g")
up;KF=$(pub);sleep 1;up;up
ok "a-first-start-retry a first start that dies before agi-run, retried twice, keeps the key its first attempt made and the ring holds exactly 1 line (key same: $([ "$(pub)" = "$KF" ]&&echo yes||echo NO); ring $(lines))" '[ -n "$KF" ]&&[ "$(pub)" = "$KF" ]&&[ "$(lines)" = 1 ]&&[ -e $H/.fresh ]'
agirun;up;ok "a-first-start-then-crash after agi-run ate .fresh a crash restart keeps the key and adds nothing" '[ "$(pub)" = "$KF" ]&&[ "$(lines)" = 1 ]'
P=$P1;H=$H1;Q=$Q1;RING=$RING1
# --- (a) the two EDGES of the unit's key drop (DG4 audit of this file, goal:g7.16.1.11.12; mutants the rows below kill: the `! -f t/.../ring` clause dropped, the drop widened to `rm -rf .ssh/*`). keystep = ONLY the unit's key line (the first sh -c with ssh-keygen), so agi-out and the ring writer cannot answer for it
keystep(){ (cd $H&&export HOME=$H&&ksl=$(sed -n "${ko}p" $STEPS)&&q=$(printf %s "${ksl#ExecStartPre=sh -c }"|sed "s,%i,$P,g;s,%t,$RUN,g")&&eval "sh -c $q" >>$T/up.out 2>>$T/up.err);}
P1=$P;H1=$H;Q1=$Q;RING1=$RING;P=post3;H=$S/$P;RING=$T/ring3;mkdir -p $H $RUN/agi-$P
keystep;K30=$(pub);mkdir -p $H/t/.agi/nodes/.geometry;: >$H/t/.agi/nodes/.geometry/ring;sleep 2;touch $H/.fresh;keystep
ok "a-ring-in-t-keeps-the-key when t carries the ring file (agi-out rotates then) an out-line's key step does NOT drop the key (same key: $([ "$(pub)" = "$K30" ]&&echo yes||echo NO))" '[ -n "$K30" ]&&[ "$(pub)" = "$K30" ]'
rm -f $H/t/.agi/nodes/.geometry/ring;sleep 2;touch $H/.fresh;keystep;K31=$(pub)
ok "a-ring-in-t-witness the same out-line with the ring file gone DOES drop the key (the row above can fail): old ...$(echo $K30|rev|cut -c1-6|rev), new ...$(echo $K31|rev|cut -c1-6|rev)" '[ -n "$K31" ]&&[ "$K31" != "$K30" ]'
: >$H/.ssh/out-refused;echo kh >$H/.ssh/known_hosts;sleep 2;touch $H/.fresh;keystep;K32=$(pub)
ok "a-drop-touches-only-the-key-files an out-line's drop removes id_ed25519 and id_ed25519.pub and nothing else in .ssh: new key $([ -n "$K32" ]&&[ "$K32" != "$K31" ]&&echo yes||echo NO) (want yes); .ssh = [$(ls $H/.ssh|sort|tr "\n" " ")] (want [id_ed25519 id_ed25519.pub known_hosts out-refused ])" '[ -n "$K32" ]&&[ "$K32" != "$K31" ]&&[ "$(ls $H/.ssh|sort|tr "\n" " ")" = "id_ed25519 id_ed25519.pub known_hosts out-refused " ]'
# --- (a) the ring writer's own gates (agi-signers; mutants: the ring chmod 644 -> 666, the one-line check removed, the strict ed25519 key pattern loosened): each refusal leaves the ring file UNWRITTEN
P=post4;H=$S/$P;mkdir -p $H/.ssh;ssh-keygen -qN "" -ted25519 -f$H/.ssh/id_ed25519 >/dev/null;cp $H/.ssh/id_ed25519.pub $T/good4.pub
sg(){ (umask 077;AGI_RUN=none AGI_STORES=$S AGI_SIGNERS=$RING sh $T/signers.sh $P >/dev/null 2>$T/sg.err);}  # umask 077: the ring would be 600 without the piece's own chmod 644 (at the default 022 the deleted chmod still reads 644)
RING=$T/ring4;sg;rc4=$?
ok "ring-mode-644 a good key is appended (rc $rc4, want 0; $(lines) line, want 1) and the ring file is mode $(stat -c %a $RING 2>/dev/null) (want 644: readable by every verifier, writable by root alone)" '[ $rc4 = 0 ]&&[ "$(lines)" = 1 ]&&[ "$(stat -c %a $RING)" = 644 ]'
RING=$T/ring5;{ cat $T/good4.pub;echo 'evil@agi namespaces="git" ssh-ed25519 AAAAC3NzaC1lZDI1NTE5AAAAIEvilEvilEvilEvilEvilEvilEvilEvilEvilEvilEvil';} >$H/.ssh/id_ed25519.pub;sg;rc5=$?
ok "pubkey-one-line-only a key file of TWO lines (a second principal line) is refused: rc $rc5 (want != 0), the ring has $(lines) line(s) (want 0: nothing written), no evil line: $(cat $RING 2>/dev/null|grep -c evil) (want 0), the refusal says so: $(grep -c 'key file refused' $T/sg.err) line (want 1)" '[ $rc5 != 0 ]&&[ "$(lines)" = 0 ]&&! grep -q evil $RING 2>/dev/null&&grep -q "key file refused" $T/sg.err'
bad=;n=0;for k in 'ssh-ed25519 AAAAB3NzaC1yc2EAAAADAQABAAABAQCxxxxxxxxxxxxxxxxxxxxxxxxxxxxxxxxxxxxxxxx' 'ssh-ed25519 AAAAC3NzaC1lZDI1NTE5AAAA' 'ssh-ed25519 AAAAC3NzaC1lZDI1NTE5AAAAIGoodButEndsWithAnExtraCharacterThatIsNotBase64!!' 'ssh-ed25519 AAAAC3NzaC1lZDI1NTE5AAAAIGoodKeyBlobTailOfExactLength0123456789abcd' 'ssh-ed25519 AAAAC3NzaC1lZDI1NTE5AAAAIGoodKeyBlobTailOfExactLength0123456789abcdef';do n=$((n+1));RING=$T/ring6$n;echo "$k">$H/.ssh/id_ed25519.pub;sg&&bad="$bad $n-accepted";[ ! -s $RING ]||bad="$bad $n-ring-written";grep -q 'key file refused' $T/sg.err||bad="$bad $n-no-reason";done
ok "pubkey-strict-ed25519-pattern an RSA blob under the ed25519 type, a short ed25519 blob, a blob with a non-base64 tail and pure-base64 blobs one char short (47) and one char long (49) of the 48-char tail are each refused, the ring left empty, WITH the reason text (key file refused): accepted or reasonless cases [${bad# }] (want none)" '[ -z "$bad" ]'
cp $T/good4.pub $H/.ssh/id_ed25519.pub
P=$P1;H=$H1;Q=$Q1;RING=$RING1
# --- (b) a commit by generation g's key dated AFTER g+1 started fails verify-commit; inside g's window it verifies
cp $H/.ssh/id_ed25519 $T/key1
oi=$(vc $T/key0 $((e0+1)));oa=$(vc $T/key0 $(( $(date -u +%s)+3600 )));nn=$(vc $T/key1 $(( $(date -u +%s)+3 )))
ok "b-old-key-in-its-window g0's key at a date inside its own generation verifies" 'vk $oi'
ok "b-old-key-after-g1-fails g0's key dated after g1 started FAILS verify-commit (exit status, not text)" '! vk $oa'
ok "b-new-key-verifies g1's key verifies now" 'vk $nn'
# --- (c) the principal form: every commit that verifies says Good for <post>@agi and none says No principal matched
ok "c-principal-form every commit that verifies says 'for $P@agi' and never 'No principal matched'" 'vk $oi&&grep -q "for $P@agi" $T/vk.out&&! grep -q "No principal matched" $T/vk.out&&vk $nn&&grep -q "for $P@agi" $T/vk.out&&! grep -q "No principal matched" $T/vk.out'
ok "c-unit-email the unit exports the committer identity as %i@agi (the form the ring holds)" 'sed -n "/^### agi-post@.service/,/^~~~\$/p" $GEO/engine-root.md|grep -q "GIT_COMMITTER_EMAIL=%i@agi"'
# --- bounds: the unit edit is small, the ring writer is the existing root piece (not edited), no live key
ok "bytes the ExecStartPre line is <= $CEIL B ($(wc -c<$UNIT) B; today 685 B + ~35 + the idempotence guard; 745 -> 810 at OUT.7 (the stale-t skip step adds 69 B: this join 740 -> 809 B, agi-outline's 718 -> 787 B; the same ceiling as agi-outline, whose fresh-still-passes lane hands it CEIL; 810 -> 828 at OUT.8: the skip also looks on the unit PATH, +18 B, join 809 -> 827, agi-outline's 787 -> 805)" '[ $(wc -c<$UNIT) -le $CEIL ]'
ok "no-ring-write-in-unit the post-side line writes no allowed_signers / valid-after / valid-before (root does)" '! grep -qE "valid-(after|before)|allowed_signers" $UNIT'
ok "scratch-only every step ran in the scratch HOME: the keys, ring and worktree are under the scratch dir (a find of the real ~/.ssh was a flake risk and is gone)" '[ "${H#$T/}" != "$H" ]&&[ -f $H/.ssh/id_ed25519 ]&&[ -f $RING ]&&[ -d $H/t ]'
echo "agi-fresh: $f FAIL"
exit $f
