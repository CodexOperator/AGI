#!/bin/sh
# agi-outline.t.sh: AB (2) the out-line (hypothesis g716111-ab-the-out-line-writes-three-ring-lines-per-generation-and-none-on-a-crash-restart; falsifiers AA2.56 / 56b / 56c / 68): sh + git + ssh-keygen + python3 cryptography, a SCRATCH HOME, a SCRATCH trunk, NO live key, no network, nothing pushed.
# It runs the REAL post unit's ExecStartPre lines IN FILE ORDER (agi-fresh.t.sh pattern: STEPS = the agi-post@.service block of engine-root.md of ROOT; a candidate or a mutation = STEPS=<edited copy>), %i -> the post, %t -> a scratch run dir:
#   up = every ExecStartPre line (agi-run then consumes ~/.fresh: simulated by rm)      crash = up with NO ~/.fresh      out-line = touch ~/.fresh, then up
# SEAMS PINNED (a builder may not move them; DG2 flags each): ring = .agi/nodes/.geometry/ring in the post's worktree ~/t, plain lines '<post> <type> <b64>', types ssh-ed25519 / pq-sha256 / x25519 (x25519 = 32 B raw);
#   ONE out-line = ONE commit on ~/t touching ONLY the ring, replacing the post's own lines with exactly 3, signed by the CURRENT sign key (that commit IS the self-revocation statement), verified against the ring at its PARENT (the receiving tip);
#   the SEAL private key = ~/seal.key (base64 of the raw 32 B X25519 key: esc open's KEY format); the capsule dir = $AGI_CAPSULE, the post's share = ONE line '<post> <b64>' in file $AGI_CAPSULE/<post> (esc's line format), re-wrapped to the next SEAL pub at the out-line;
#   the wrap opener = the esc piece (ESC=<file>, else sect esc from the engine pieces, else the 'esc whole' block of doc:radically-simple-engine); the PQ column is read as 32 B only (the PQ program itself is order (4), not here); the unit's helper bytes are the builder's to report (the line bound counts the unit lines).
# Not here: the root agi-signers retire (order 7), the sealing of the retired SIGN key into the capsule and its later publication (order 5), the cross-box half. One ok/FAIL line per case; exit = FAIL count.
T=$(mktemp -d);trap 'rm -rf $T' 0;f=0;G=/usr/bin/git;SELF=$(cd "$(dirname "$0")" && pwd);R0=${ROOT:-$(cd "$SELF/../../.." && pwd)};GEO=$R0/.agi/nodes/.geometry;CEIL=${CEIL:-790};R=.agi/nodes/.geometry/ring
sect(){ cat $GEO/engine*.md|sed -n "/^###* $1 /,/^###* /{/^~~~/,/^~~~/{//!p}}";}
docb(){ sed -n "/^\`$1\` whole/,/^\`\`\`\$/{/^\`$1\` whole/d;/^\`\`\`/d;p}" $R0/.agi/nodes/doc/radically-simple-engine.md;}
mkdir $T/b $T/gb $T/k $T/shim;ESCF=${ESC:-$T/esc};[ -n "$ESC" ]||{ sect esc>$ESCF;[ -s $ESCF ]||docb esc>$ESCF;}
[ -n "$STEPS" ]||{ sed -n "/^### agi-post@.service/,/^~~~\$/{/^ExecStartPre=/p}" $GEO/engine-root.md>$T/steps;STEPS=$T/steps;}
sed -n "/^ExecStartPre=sh -c /p" $STEPS|awk -v q="'" 'NR==1{sub("^ExecStartPre=sh -c "q,"");sub(q"$","");printf "%s",$0;next}{sub("^ExecStartPre=sh -c "q,"");sub(q"$","");printf ";%s",$0}END{print ""}'>$T/unit
sect agi-signers>$T/signers.sh;for x in sect grow-check grow-gate agi-fill;do cat $GEO/engine*.md|sed -n "/^###* $x /,/^###* /{/^~~~/,/^~~~/{//!p}}">$T/gb/$x;done;[ "$GROW_GATE" ]&&cp $GROW_GATE $T/gb/grow-gate;chmod +x $T/gb/*
[ -s $STEPS ]&&[ -s $ESCF ]&&[ -s $T/signers.sh ]||{ echo "FAIL extract: steps $(wc -c<$STEPS) B, esc $(wc -c<$ESCF) B, signers $(wc -c<$T/signers.sh) B";exit 99;}
ok(){ if eval "$2";then echo "ok $1";else echo "FAIL $1";f=$((f+1));fi;}
unset GIT_AUTHOR_NAME GIT_AUTHOR_EMAIL GIT_COMMITTER_NAME GIT_COMMITTER_EMAIL GIT_DIR GIT_WORK_TREE GIT_CONFIG_GLOBAL GIT_CONFIG_SYSTEM AGI_TRUNK
export GIT_CONFIG_GLOBAL=/dev/null GIT_CONFIG_SYSTEM=/dev/null   # HERMETIC (SM return 05:12Z): no host gitconfig (gpg.format, allowedSignersFile, signingkey, hooks) reaches any case; the unit alone (up) reads the post's OWN ~/.gitconfig under HOME=$H
P=post1;Q=other;SM=sm;S=$T/stores;H=$S/$P;RUN=$T/run;O=$T/main;K=$T/k;CAP=$T/cap;mkdir -p $H/.ssh $RUN/agi-$P $CAP
# --- key helpers: a ring line triple for a name, from a sign key file, a PQ root (32 random bytes) and a SEAL key (esc's KEY format)
cat >$T/seal.py <<'PYEOF'
import sys,base64 as B,hashlib
from cryptography.hazmat.primitives.asymmetric.x25519 import X25519PrivateKey as K,X25519PublicKey as P
from cryptography.hazmat.primitives import serialization as S
a=sys.argv;v=a[1];N=S.NoEncryption()
if v=='gen':k=K.generate();open(a[2],'w').write(B.b64encode(k.private_bytes(S.Encoding.Raw,S.PrivateFormat.Raw,N)).decode());print(B.b64encode(k.public_key().public_bytes_raw()).decode())
if v=='pub':print(B.b64encode(K.from_private_bytes(B.b64decode(open(a[2]).read())).public_key().public_bytes_raw()).decode())
if v=='sshx':
 sd=S.load_ssh_private_key(open(a[2],'rb').read(),None).private_bytes(S.Encoding.Raw,S.PrivateFormat.Raw,N);d=bytearray(hashlib.sha512(sd).digest()[:32]);d[0]&=248;d[31]&=127;d[31]|=64;open(a[3],'w').write(B.b64encode(bytes(d)).decode())
if v=='wrap':
 from cryptography.hazmat.primitives.ciphers.aead import ChaCha20Poly1305 as C;e=K.generate();h=lambda x:hashlib.sha256(x).digest();print(B.b64encode(e.public_key().public_bytes_raw()+C(h(e.exchange(P.from_public_bytes(B.b64decode(a[2]))))).encrypt(bytes(12),sys.stdin.read().strip().encode(),None)).decode())
PYEOF
sealgen(){ python3 $T/seal.py gen $1;}
ringlines(){ printf '%s ssh-ed25519 %s\n%s pq-sha256 %s\n%s x25519 %s\n' $1 "$(cut -d' ' -f2 $2)" $1 "$(head -c32 /dev/urandom|base64)" $1 "$(sealgen $3)";}
for u in $SM $Q;do ssh-keygen -qN "" -ted25519 -f$K/$u>/dev/null;done;ssh-keygen -qN "" -ted25519 -f$H/.ssh/id_ed25519>/dev/null;cp $H/.ssh/id_ed25519 $K/key0;cp $H/.ssh/id_ed25519.pub $K/key0.pub
{ ringlines $SM $K/$SM.pub $K/$SM.seal;ringlines $P $H/.ssh/id_ed25519.pub $H/seal.key;ringlines $Q $K/$Q.pub $K/$Q.seal;}>$T/ring;cp $H/seal.key $K/seal0
# --- the scratch MAIN: the real engine pieces + the ring + the posts tree + the schemas the gate reads; the post's worktree ~/t on branch posts/<post>
$G init -q $O;mkdir -p $O/.agi/nodes/.geometry $O/.agi/context;for x in engine.md engine-post.md engine-wrap.md;do cp $GEO/$x $O/.agi/nodes/.geometry/;done;cp -r $R0/.agi/context/schemas $O/.agi/context/;cp $GEO/growth.tsv $O/.agi/nodes/.geometry/;cp $T/ring $O/$R
printf -- '---\n---\n  - {"name": "belam", "parent": "owner"}\n  - {"name": "sm", "parent": "belam"}\n  - {"name": "post1", "parent": "sm"}\n  - {"name": "other", "parent": "sm"}\n'>$O/.agi/nodes/.geometry/posts.md
$G -C $O add -A;$G -C $O -c user.name=x -c user.email=x@x -c commit.gpgsign=false commit -qm fixture;TR=$($G -C $O rev-parse HEAD);$G -C $O branch posts/$P $TR;$G -C $O worktree add -fq $H/t posts/$P
# --- the capsule: ONE secret split 2-of-2 by esc to post1's SEAL pub and other's; each holder's line in its own file
head -c 24 /dev/urandom|base64>$T/secret;sealpub(){ python3 $T/seal.py pub $1;};sealpub $H/seal.key>$T/p1.pub;sealpub $K/$Q.seal>$T/p2.pub;python3 $ESCF split 2 $T/p1.pub $T/p2.pub <$T/secret>$T/escrow
echo "$P $(sed -n 2p $T/escrow|cut -d' ' -f2)">$CAP/$P;echo "$Q $(sed -n 3p $T/escrow|cut -d' ' -f2)">$CAP/$Q;cp $CAP/$P $T/cap0;cp $CAP/$Q $T/capq0
opn(){ python3 $ESCF open $1 <$2 2>/dev/null;}   # opn KEYFILE LINEFILE: prints 'i:y' or fails
SH0=$(opn $H/seal.key $CAP/$P)
# --- the shim: `git` that fails the land (commit, commit-tree, update-ref, push, merge) while $T/failland exists
printf '#!/bin/sh\nskip=;sub=;for a in "$@";do [ -n "$skip" ]&&{ skip=;continue;};case $a in -C|-c)skip=1;continue;;-*)continue;;*)sub=$a;break;;esac;done\n[ -e %s/failland ]&&case $sub in commit|commit-tree|update-ref|push|merge)echo "shim: land refused" >&2;exit 1;;esac\nexec /usr/bin/git "$@"\n' $T>$T/shim/git;chmod +x $T/shim/git
up(){ (cd $H&&unset GIT_CONFIG_GLOBAL XDG_CONFIG_HOME&&export HOME=$H O=$O AGI_TRUNK=$TR AGI_SEAT=$P AGI_CAPSULE=$CAP RUNTIME_DIRECTORY=$RUN/agi-$P ESC=$ESCF SEALPY=$T/seal.py OLREF=$OLREF PATH=$T/shim:$H/bin:$PATH GIT_AUTHOR_NAME=$P GIT_COMMITTER_NAME=$P GIT_AUTHOR_EMAIL=$P@agi GIT_COMMITTER_EMAIL=$P@agi&&while IFS= read -r l;do case $l in "ExecStartPre=sh -c "*)q=$(printf %s "${l#ExecStartPre=sh -c }"|sed "s,%i,$P,g;s,%t,$RUN,g");eval "sh -c $q" >>$T/up.out 2>>$T/up.err;;"ExecStartPre=+"*agi-signers*)AGI_RUN=none AGI_STORES=$S AGI_SIGNERS=$T/allowed sh $T/signers.sh $P;;esac;done<$STEPS);}
agirun(){ rm -f $H/.fresh;}
pub(){ cut -d' ' -f1,2 $H/.ssh/id_ed25519.pub;}
rc(){ $G -C $H/t rev-list --count $1..HEAD -- $R;}                       # ring commits since $1
rg(){ $G -C $H/t show ${1:-HEAD}:$R;}                                      # the ring at a rev
own(){ rg $1|grep "^$P ";}
allowed(){ rg $1|awk '$2=="ssh-ed25519"{printf "%s@agi namespaces=\"git\" %s %s\n",$1,$2,$3}'>$T/al;}
# vp COMMIT: verify-commit against the ring at the commit's PARENT (the receiving tip); the EXIT STATUS decides
vp(){ allowed $1^;$G -C $H/t -c gpg.format=ssh -c gpg.ssh.allowedSignersFile=$T/al verify-commit $1>$T/vk.out 2>&1;}
fp(){ ssh-keygen -lf $1|cut -d' ' -f2;}
distinct(){ own $1|cut -d' ' -f3|sort>$T/o0;own $2|cut -d' ' -f3|sort>$T/o1;[ -z "$(comm -12 $T/o0 $T/o1)" ];}
# --- a start whose key the ring does not know: the pre-existing generation 0 (fixture): a crash restart (no .fresh): the key is kept and the ring gets NO commit
B=$($G -C $H/t rev-parse HEAD);K0=$(pub)
up;agirun;up;agirun;up;agirun
ok "a-crash-0-commits three crash restarts (no .fresh) write 0 ring commits (got $(rc $B)) and keep the key" '[ "$(rc $B)" = 0 ]&&[ "$(pub)" = "$K0" ]&&[ "$($G -C $H/t rev-parse HEAD)" = "$B" ]'
# --- (a) ONE .fresh = ONE ring commit
sleep 1;touch $H/.fresh;up;K1=$(pub);C1=$($G -C $H/t rev-parse HEAD);cp $H/.ssh/id_ed25519 $K/key1;cp $H/.ssh/id_ed25519.pub $K/key1.pub;cp $H/seal.key $K/seal1;cp $CAP/$P $T/cap1
ok "a-outline-one-commit one .fresh writes exactly 1 ring commit (got $(rc $B))" '[ "$(rc $B)" = 1 ]&&[ "$($G -C $H/t rev-list --count $B..HEAD)" = 1 ]'
ok "a-outline-ring-only that commit touches ONLY the ring file" '[ "$($G -C $H/t diff-tree --no-commit-id --name-only -r $C1)" = $R ]'
ok "a-outline-three-lines it leaves the post exactly 3 lines of its own: ssh-ed25519, pq-sha256, x25519 (not 6: the old ones are replaced)" '[ "$C1" != "$B" ]&&[ "$(own $C1|wc -l|tr -d " ")" = 3 ]&&[ "$(own $C1|cut -d" " -f2|sort|tr "\n" " ")" = "pq-sha256 ssh-ed25519 x25519 " ]'
ok "a-outline-others-untouched every other post keeps its lines byte for byte" '[ "$C1" != "$B" ]&&[ "$(rg $B|grep -v "^$P ")" = "$(rg $C1|grep -v "^$P ")" ]'
ok "a-outline-all-three-new none of the three columns repeats generation 0 (a column left unchanged would keep a retired key in force)" '[ "$C1" != "$B" ]&&distinct $B $C1'
ok "a-outline-signed-by-current the commit is signed by the CURRENT (generation 0) sign key: its key fingerprint is key0's, and verify-commit against the ring at its parent exits 0" 'vp $C1&&[ "$($G -C $H/t -c gpg.format=ssh -c gpg.ssh.allowedSignersFile=$T/al log -1 --format=%GK $C1)" = "$(fp $K/key0.pub)" ]'
ok "a-outline-key-installed after the restart the live sign key IS the ring's new ssh-ed25519 column and differs from generation 0" '[ "$(pub)" != "$K0" ]&&[ "$(own $C1|awk "\$2==\"ssh-ed25519\"{print \$2,\$3}")" = "$(pub)" ]'
# D1 (mur on 00ffbe04c; DG1 05:47Z): the unit's steps in FILE ORDER (key step, root agi-signers, the rest, agi-out) must leave the file the BOX verifies against ($T/allowed, written by the unit's own agi-signers step) holding the NEW key after the ONE start that swapped it: nv KEYFILE = a commit by post1's identity signed with that key, verified against $T/allowed (hermetic)
nv(){ echo n$2>$T/nb;nh=$($G -C $H/t hash-object -w $T/nb);ntr=$(printf "100644 blob %s\tn\n" $nh|$G -C $H/t mktree);nvc=$(env GIT_COMMITTER_NAME=$P GIT_COMMITTER_EMAIL=$P@agi GIT_AUTHOR_NAME=$P GIT_AUTHOR_EMAIL=$P@agi $G -C $H/t -c gpg.format=ssh -c user.signingkey=$1 commit-tree -S -m n $ntr)&&$G -C $H/t -c gpg.format=ssh -c gpg.ssh.allowedSignersFile=$T/allowed verify-commit $nvc>$T/nv.out 2>&1;}
ok "d1a-new-key-verifies-after-one-start after the ONE start that swapped the key (agi-out ran AFTER agi-signers in the unit's order, so a file written before the swap lacks it) a commit signed by the NEW sign key verifies against the box file as $P@agi" 'nv $H/.ssh/id_ed25519 1'
ok "d1b-old-key-commit-still-verifies the out-line commit itself (signed by the OLD key, dated before the stamp) still verifies against the box file after that start" '$G -C $H/t -c gpg.format=ssh -c gpg.ssh.allowedSignersFile=$T/allowed verify-commit $C1>/dev/null 2>&1'
ok "a-outline-pq-32 the pq-sha256 column is 32 raw bytes" '[ "$C1" != "$B" ]&&[ "$(own $C1|awk "\$2==\"pq-sha256\"{print \$3}"|base64 -d 2>/dev/null|wc -c|tr -d " ")" = 32 ]'
ok "a-outline-seal-is-ring the x25519 column is 32 raw bytes and IS the public half of ~/seal.key" '[ "$C1" != "$B" ]&&x=$(own $C1|awk "\$2==\"x25519\"{print \$3}");[ "$(echo $x|base64 -d 2>/dev/null|wc -c|tr -d " ")" = 32 ]&&[ "$x" = "$(sealpub $H/seal.key)" ]'
ok "a-outline-no-key-bytes-in-commit the commit holds no private key block (the trunk is public)" '[ "$C1" != "$B" ]&&! $G -C $H/t show $C1|grep -aq -e "-\{5\}BEGIN [A-Z0-9 ]*PRIVATE KEY-\{5\}"'
ok "a-outline-no-ring-text-left (e) no uncommitted ring text beside the one commit" '[ -z "$($G -C $H/t status --porcelain -- $R)" ]'
ok "a-outline-retired-seal-deleted the retired SEAL key survives nowhere under the post's home" '! grep -rqF "$(cat $K/seal0)" $H --exclude-dir=t'
agirun
# --- the crash restarts AFTER the out-line, and a RETRY of the out-line before agi-run consumes .fresh
up;agirun;up;agirun
ok "a-crash-after-outline two crash restarts after the out-line keep the NEW key and add 0 commits (still $(rc $B))" '[ "$(pub)" = "$K1" ]&&[ "$(rc $B)" = 1 ]'
ok "d1c-still-after-restarts after those two crash restarts the NEW key's commit still verifies against the box file (a second start cannot lose the key the first one made)" 'nv $K/key1 2'
ok "d1d-old-key-after-restarts and the OLD key's out-line commit still verifies (the old key was stamped valid-before AFTER its own commit's date)" '$G -C $H/t -c gpg.format=ssh -c gpg.ssh.allowedSignersFile=$T/allowed verify-commit $C1>/dev/null 2>&1'
sleep 1;touch $H/.fresh;up;K2=$(pub);up;up
ok "a-retry-idempotent an out-line whose start is RETRIED twice before agi-run consumes .fresh adds exactly 1 commit in all and keeps the key its first attempt made (ring commits $(rc $B), want 2)" '[ "$K2" != "$K1" ]&&[ "$(pub)" = "$K2" ]&&[ "$(rc $B)" = 2 ]'
C2=$($G -C $H/t rev-parse HEAD);agirun
ok "a-chain the second out-line is signed by generation 1 (key1's fingerprint) and verifies against the ring its parent holds; the post still holds exactly 3 lines" 'vp $C2&&[ "$($G -C $H/t -c gpg.format=ssh -c gpg.ssh.allowedSignersFile=$T/al log -1 --format=%GK $C2)" = "$(fp $K/key1.pub)" ]&&[ "$(own $C2|wc -l|tr -d " ")" = 3 ]'
ok "a-chain-all-three-new the second out-line repeats none of the first one's three columns" 'distinct $C1 $C2'
cp $H/seal.key $K/seal2;cp $CAP/$P $T/cap2
# --- (b) a crash BEFORE the land leaves the old line in force; the retry then completes
B3=$($G -C $H/t rev-parse HEAD);K3=$(pub);RG3=$(rg $B3|md5sum);sleep 1;touch $H/.fresh;: >$T/failland;up;rm -f $T/failland
ok "b-crash-before-land the land refused: the ring is unchanged, the old key still the live key, no new commit, .fresh still pending" '[ "$(rg|md5sum)" = "$RG3" ]&&[ "$(pub)" = "$K3" ]&&[ "$($G -C $H/t rev-parse HEAD)" = "$B3" ]&&[ -e $H/.fresh ]'
ok "b-old-line-in-force the old key still verifies a commit against the ring (the old line is the one in force)" 'cp $H/.ssh/id_ed25519 $K/live;vc=$($G -C $H/t -c user.name=$P -c user.email=$P@agi -c user.signingkey=$K/live -c gpg.format=ssh commit-tree -S -m m $($G -C $H/t rev-parse HEAD^{tree}) -p $B3 2>/dev/null);[ -n "$vc" ]&&vp $vc'
# --- (b) the COMMIT-failure handler of agi-out (DG1 08:43Z; the handler `git -C t checkout -q -- $R` was RED in no lane): `git commit` of the ring fails at the land: the start FAILS (rc 1), the ring is RESTORED (nothing dirty for the agi-turn sweep to commit), no ~/.ssh/n, no capsule .new, the share unchanged, 0 new commits after the sweep; the retry below then re-wraps from scratch. ex CMD = CMD under the unit's environment (the same one `up` builds), rc kept
ex(){ (cd $H&&unset GIT_CONFIG_GLOBAL XDG_CONFIG_HOME&&export HOME=$H O=$O AGI_TRUNK=$TR AGI_SEAT=$P AGI_CAPSULE=$CAP RUNTIME_DIRECTORY=$RUN/agi-$P ESC=$ESCF SEALPY=$T/seal.py OLREF=$OLREF PATH=$T/shim:$H/bin:$PATH GIT_AUTHOR_NAME=$P GIT_COMMITTER_NAME=$P GIT_AUTHOR_EMAIL=$P@agi GIT_COMMITTER_EMAIL=$P@agi&&sh -c "$1");}
Bx=$($G -C $H/t rev-parse HEAD);cp $CAP/$P $T/capx;sleep 1;touch $H/.fresh;: >$T/failland;ex agi-out>$T/ex.out 2>&1;rcx=$?;rm -f $T/failland
ok "e1-commit-failure-exits-1 the ring commit fails (the shim, no network, nothing else changed): agi-out exits 1 (got $rcx), so the start fails and .fresh stays pending" '[ "$rcx" = 1 ]&&[ -e $H/.fresh ]'
ok "e2-commit-failure-ring-restored after the refused commit \`git -C t status --porcelain -- \$R\` is EMPTY: the ring is restored, so nothing is left in the worktree for agi-flush / agi-turn to commit as a half ring naming the next keys" '[ -z "$($G -C $H/t status --porcelain -- $R)" ]'
ok "e3-commit-failure-no-leftovers no ~/.ssh/n and no capsule .new is left, and the post's share line is byte for byte as before" '[ ! -e $H/.ssh/n ]&&[ ! -e $CAP/$P.new ]&&cmp -s $CAP/$P $T/capx'
ex agi-turn>/dev/null 2>&1;Hx=$($G -C $H/t rev-parse HEAD);$G -C $H/t reset -q --hard $Bx
ok "e4-commit-failure-sweep-0-commits after the agi-turn sweep (git add -A; git commit in ~/t) there are 0 NEW commits (HEAD still the one before)" '[ "$Hx" = "$Bx" ]'
up;agirun
ok "b-retry-completes after the refused land, the next start completes the out-line with exactly 1 commit and a new key (ring commits $(rc $B3), want 1)" '[ "$(rc $B3)" = 1 ]&&[ "$(pub)" != "$K3" ]&&[ "$(own|awk "\$2==\"ssh-ed25519\"{print \$2,\$3}")" = "$(pub)" ]'
ok "e5-retry-rewraps-from-scratch after the refused commit the retry re-wraps from scratch: the live ~/seal.key opens the post's share to the SAME secret and IS the key the ring's x25519 column names; no ~/.ssh/n is left" '[ "$(opn $H/seal.key $CAP/$P)" = "$SH0" ]&&[ "$(own|awk "\$2==\"x25519\"{print \$3}")" = "$(sealpub $H/seal.key)" ]&&[ ! -e $H/.ssh/n ]'
# --- (b) a crash AFTER the land leaves a line whose key is LOST: a restart writes 0 ring commits (a post cannot vouch for itself); the PARENT re-vouches with ONE commit the gate admits (C7); a sibling is refused
B4=$($G -C $H/t rev-parse HEAD);rm -f $H/.ssh/id_ed25519 $H/.ssh/id_ed25519.pub $H/seal.key;up;agirun;KN=$(pub)
ok "b-lost-key-restart-0 the key lost after the land: a restart makes a new key and writes 0 ring commits (the ring's line is stale until the parent re-vouches)" '[ "$($G -C $H/t rev-parse HEAD)" = "$B4" ]&&[ "$(own|awk "\$2==\"ssh-ed25519\"{print \$2,\$3}")" != "$KN" ]'
revouch(){ x=$T/i;rg $B4|awk -v p=$P -v k="$(echo $KN|cut -d' ' -f2)" '$1==p&&$2=="ssh-ed25519"{$3=k}{print}'>$T/e;GIT_INDEX_FILE=$x $G -C $O read-tree $B4;GIT_INDEX_FILE=$x $G -C $O update-index --add --cacheinfo 100644,$($G -C $O hash-object -w $T/e),$R;tr=$(GIT_INDEX_FILE=$x $G -C $O write-tree);rm -f $x
 env GIT_COMMITTER_NAME=$1 GIT_COMMITTER_EMAIL=$1@agi GIT_AUTHOR_NAME=$1 GIT_AUTHOR_EMAIL=$1@agi $G -C $O -c gpg.format=ssh -c user.signingkey=$K/$1 commit-tree -S -p $B4 -m revouch $tr;}
ssh-keygen -qN "" -ted25519 -f$K/old1>/dev/null
: >$T/over;for n in $K/key0.pub $K/key1.pub $K/$SM.pub $K/$Q.pub $H/.ssh/id_ed25519.pub;do for u in $P $SM $Q;do echo "$u@agi namespaces=\"git\" $(cut -d" " -f1,2 $n)">>$T/over;done;done
gate(){ $G -C $O update-ref refs/heads/trunk $1;echo "$1 $2 refs/heads/x"|(cd $O&&PATH=$T/gb:$PATH AGI_ALLOWED=$T/over AGI_TRUNK=refs/heads/trunk AGI_NOT=$1 timeout 60 grow-gate)>$T/out 2>&1;r=$?;}
RV=$(revouch $SM);gate $B4 $RV;ok "b-revouch-by-parent sm (the post's parent) re-vouches the post's sign line in ONE commit: the gate admits it (C7)" '[ $r = 0 ]'
RO=$(revouch $Q);gate $B4 $RO;ok "b-revouch-by-sibling other (not an ancestor of the post) writing the same commit is refused" '[ $r != 0 ]&&[ $r != 124 ]'
# --- (c) the capsule shares (AA2.68): S1 gen0's SEAL opened its share; S4 the next generation's SEAL opens the re-wrap (same share); X3 the retired SEAL, X4 another post's key, S2 the PUBLISHED retired sign key do not
ok "s1-seal-opens-its-share generation 0's SEAL key opened its capsule share (the fixture, before any out-line)" '[ -n "$SH0" ]&&[ "$(opn $K/seal0 $T/cap0)" = "$SH0" ]'
ok "s4-next-seal-opens-the-rewrap the first out-line CHANGED the post's capsule line and generation 1's SEAL (the ~/seal.key the ring column names) opens it to the SAME share" '[ "$(cat $T/cap1)" != "$(cat $T/cap0)" ]&&[ "$(opn $K/seal1 $T/cap1)" = "$SH0" ]'
ok "x3-retired-seal-cannot-open the retired generation 0 SEAL does NOT open the new wrap" '[ -z "$(opn $K/seal0 $T/cap1)" ]'
ok "x4-another-post-cannot-open another post's SEAL key does NOT open it" '[ "$(cat $T/cap1)" != "$(cat $T/cap0)" ]&&[ -z "$(opn $K/$Q.seal $T/cap1)" ]'
python3 $T/seal.py sshx $K/key0 $K/key0.x;echo "$SH0"|python3 $T/seal.py wrap $(sealpub $K/key0.x)>$T/ctl.b64;echo "ctl $(cat $T/ctl.b64)">$T/ctl
ok "s2-published-sign-key-cannot-open the PUBLISHED retired sign key (generation 0, its X25519 form) does NOT open the new wrap (control: a share wrapped to that very X25519 form, the folded design, DOES open: $( [ "$(opn $K/key0.x $T/ctl)" = "$SH0" ]&&echo yes||echo NO))" '[ "$(cat $T/cap1)" != "$(cat $T/cap0)" ]&&[ -z "$(opn $K/key0.x $T/cap1)" ]&&[ "$(opn $K/key0.x $T/ctl)" = "$SH0" ]'
ok "x-other-share-untouched the other post's capsule line is byte-for-byte unchanged by $P's out-lines" 'cmp -s $CAP/$Q $T/capq0'
ok "s4b-share-survives-two-generations after the second out-line generation 2's SEAL opens the line to the same share and generation 1's does not" '[ "$(opn $K/seal2 $T/cap2)" = "$SH0" ]&&[ -z "$(opn $K/seal1 $T/cap2)" ]'
# --- (c) bounds: the unit lines, and the agi-fresh one-box cases still pass
ok "bytes the unit's sh -c ExecStartPre lines are <= $CEIL B ($(wc -c<$T/unit) B; today 695 B + <= 95 B, DG1's ceiling; the builder reports any helper's bytes beside it)" '[ $(wc -c<$T/unit) -le $CEIL ]'
ok "fresh-still-passes agi-fresh.t.sh (crash keeps the key and appends 0, the retry cases) exits 0 on ROOT's unit (its own bytes lane at THIS ceiling: the two agree) ($(CEIL=$CEIL ROOT=$R0 sh $SELF/agi-fresh.t.sh 2>&1|tail -1))" 'CEIL=$CEIL ROOT=$R0 sh $SELF/agi-fresh.t.sh >$T/fresh.out 2>&1'
ok "scratch-only every key, ring and capsule the cases touched is under the scratch dir" '[ "${H#$T/}" != "$H" ]&&[ "${CAP#$T/}" != "$CAP" ]'
echo "agi-outline: $f FAIL"
exit $f
