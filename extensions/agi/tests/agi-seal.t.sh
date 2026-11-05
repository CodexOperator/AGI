#!/bin/sh
# agi-seal.t.sh [ROOT]: goal:g7.16.1.11.46.15 SEAL -- agi-out seals the capsule share with age to the NEW generation's ssh-ed25519 key; the retired seal format still opens.
# sh + git + ssh-keygen + apt/dpkg-deb (the age lane) + python3 cryptography (ONLY the fixtures that make a share in the RETIRED format; agi-out itself carries none). A SCRATCH HOME, a SCRATCH trunk, 0 USD, no root, no network except
# `apt-get download` of the pinned package. The age under test is the ARCHIVE PACKAGE the council pinned (age=1.1.1-1ubuntu0.24.04.3, alive 20:23:34Z 10-25): the lane downloads that .deb, checks its sha256 against the archive's own
# Packages entry, unpacks it into scratch with `dpkg-deb -x` (no root) and puts it on the PATH of the piece under test ONLY, never on the real PATH. AGE_DEB=<file> tests another build (the mutant), AGE_PIN=<ver> another pin.
# The piece under test is `sect agi-out` of ROOT's .geometry/engine*.md (default: this working tree); AGI_OUT=<file> tests a candidate or a mutation. A tree without the piece exits 99.
# Rows: p* the pin (deb sha == archive entry, Version == pin, `age --version` == the upstream part; mutant: another build reads RED)  rt* a ROUND TRIP on every input: old-seal -> old-open == input == agi-out's age share opened with
#   age -d -i the NEW key, and once more across a second generation (age -> age); mutant: the wrong -R reads RED  pw* a passphrase-protected key never hangs (rc 75, the reason by name, nothing committed, under the timeout);
#   a hung age is cut by the timeout  ring* the legacy ring line is carried, never regenerated; a post with none gets none  na* no age on the PATH: refuse before any state changes  gr* the piece carries 0 of python3|cryptography|X25519
#   (mutant: the pre-switch piece reads non-zero)  cs* the census prints `opened k/m` (k == m > 0), `unread` + rc 1 for m == 0 or an unreadable share (mutant: a share that does not open counted as opened reads RED).
# Honest limits: the INSTALLED set's sha256 against these bytes is belam's host act after the land (dpkg-query -W age == the pin; sha256sum of the installed piece == the printed one); the census on the LIVE shares is the holder's.
R0=${ROOT:-${1:-$(cd "$(dirname "$0")/../../.." && pwd)}};GEO=.agi/nodes/.geometry;D=$(mktemp -d);trap 'rm -rf $D' EXIT;f=0
unset GIT_DIR GIT_WORK_TREE GIT_INDEX_FILE GIT_AUTHOR_NAME GIT_AUTHOR_EMAIL GIT_COMMITTER_NAME GIT_COMMITTER_EMAIL AGI_CAPSULE
export GIT_CONFIG_GLOBAL=/dev/null          # a post's own global config carries the ref-guard hook; the scratch repos are not that post's
PIN=${AGE_PIN:-1.1.1-1ubuntu0.24.04.3};OTHER=1.1.1-1build1
ok(){ if eval "$2";then echo "ok $1";else echo "FAIL $1";f=$((f+1));fi;}
sect(){ cat $R0/$GEO/engine*.md|sed -n "/^###* $1 /,/^###* /{/^~~~/,/^~~~/{//!p}}"; }
SEALOPEN=$R0/extensions/agi/bin/legacy/seal-open;CENSUS=$R0/extensions/agi/bin/agi-seal-census
# --- the age lane: acquire(deb) -> 0 when the deb is the pinned package; prints one line of facts
acquire(){ d=$1;w=$(apt-cache show age=$PIN 2>/dev/null|awk '/^SHA256:/{print $2;exit}');h=$(sha256sum $d|cut -d' ' -f1);v=$(dpkg-deb -f $d Version)
 echo "age deb $(basename $d) sha256 $h, archive entry ${w:-none}, Version $v, pin $PIN";[ -n "$w" ]&&[ "$h" = "$w" ]&&[ "$v" = "$PIN" ];}
unpack(){ rm -rf $2;mkdir -p $2;dpkg-deb -x $1 $2&&mkdir -p $D/ab/bin&&ln -sf $2/usr/bin/age $D/ab/bin/age&&ln -sf $2/usr/bin/age-keygen $D/ab/bin/age-keygen;}
if [ -n "$AGE_DEB" ];then DEB=$AGE_DEB;else mkdir -p $D/dl;(cd $D/dl&&apt-get download age=$PIN >/dev/null 2>&1);DEB=$(ls $D/dl/age_*.deb 2>/dev/null|head -1);fi
[ -f "$DEB" ]||{ echo "FAIL p0-deb no age .deb (apt-get download age=$PIN failed; AGE_DEB=<file> names one)";exit 99;}
facts=$(acquire $DEB);rc=$?;echo "$facts"
ok p1-deb-is-the-pinned-package "[ $rc = 0 ]"
unpack $DEB $D/age1||{ echo "FAIL p2-unpack";exit 99;}
ok p2-version-line-is-the-upstream-part "[ \"\$(PATH=$D/ab/bin:\$PATH age --version)\" = ${PIN%%-*} ]"
if [ -z "$AGE_DEB" ];then mkdir -p $D/dl2;(cd $D/dl2&&apt-get download age=$OTHER >/dev/null 2>&1);O=$(ls $D/dl2/age_*.deb 2>/dev/null|head -1)
 if [ -f "$O" ];then ok p3-mutant-another-build-reads-red "! acquire $O >/dev/null";else echo "ok p3-mutant-another-build-reads-red (skipped: $OTHER not downloadable here)";fi;fi
PATH=$D/ab/bin:$PATH
# --- the piece and its neighbours
sect agi-out >$D/agi-out;[ "$AGI_OUT" ]&&cp $AGI_OUT $D/agi-out;mkdir $D/bin;sect agi-at >$D/bin/agi-at;sect grow.py >$D/bin/grow.py;[ -s $D/bin/grow.py ]||rm -f $D/bin/grow.py;chmod +x $D/bin/agi-at $D/bin/grow.py 2>/dev/null
[ -s $D/agi-out -a -s $D/bin/agi-at ]||{ echo "FAIL no agi-out / agi-at piece at $R0";exit 99;}
oldwrap(){ python3 -c "import sys,base64 as B,hashlib as H;from cryptography.hazmat.primitives.asymmetric.x25519 import X25519PrivateKey as K,X25519PublicKey as P;from cryptography.hazmat.primitives.ciphers.aead import ChaCha20Poly1305 as C;e=K.generate();h=lambda x:H.sha256(x).digest();q=P.from_public_bytes(B.b64decode(open(sys.argv[1]).read().strip()));print('post1',B.b64encode(e.public_key().public_bytes_raw()+C(h(e.exchange(q))).encrypt(bytes(12),sys.stdin.buffer.read(),None)).decode())" "$1";}
# mkh N MODE [PLAIN]: a scratch HOME. MODE legacy = a share in the RETIRED format + seal.key + the ring's x25519 line; age = a share already age; none = a fresh post (no share, no seal key)
mkh(){ H=$D/h$1;rm -rf $H;mkdir -p $H/.ssh $H/t/$GEO;ssh-keygen -qN "" -ted25519 -f$H/.ssh/id_ed25519>/dev/null
 printf '[gpg]\nformat=ssh\n[commit]\ngpgsign=true\n[user]\nsigningkey=%s/.ssh/id_ed25519.pub\n[safe]\n\tdirectory=*\n' $H>$H/.gitconfig
 printf 'post1 ssh-ed25519 %s\npost1 pq-sha256 %s\n' "$(awk '{print $2}' $H/.ssh/id_ed25519.pub)" "$(head -c32 /dev/urandom|base64)">$H/t/$GEO/ring
 if [ "$2" = legacy ];then python3 -c "import base64 as B;from cryptography.hazmat.primitives.asymmetric.x25519 import X25519PrivateKey as K;k=K.generate();open('$H/seal.key','w').write(B.b64encode(k.private_bytes_raw()).decode());print(B.b64encode(k.public_key().public_bytes_raw()).decode())">$H/seal.pub
  printf 'post1 x25519 %s\n' "$(cat $H/seal.pub)">>$H/t/$GEO/ring;fi
 mkdir -p $H/t/extensions/agi/bin/legacy;cp -p $SEALOPEN $H/t/extensions/agi/bin/legacy/seal-open
 git init -q -b trunk $H/t;(cd $H/t;git -c user.name=x -c user.email=x@x -c commit.gpgsign=false add -A;git -c user.name=x -c user.email=x@x -c commit.gpgsign=false commit -qm ring0;git branch posts/post1;git checkout -q --detach posts/post1)
 mkdir -p $H/capsule;case $2 in legacy)oldwrap $H/seal.pub <${3:-/dev/null}>$H/capsule/post1;; age)age -R $H/.ssh/id_ed25519.pub -o $H/capsule/post1 <${3:-/dev/null};; esac
 sleep 1;touch $H/.fresh;}
out(){ (cd $H;env -u GIT_DIR HOME=$H GIT_CONFIG_GLOBAL=$H/.gitconfig GIT_CONFIG_SYSTEM=/dev/null GIT_TEST_ASSUME_DIFFERENT_OWNER=1 GIT_AUTHOR_NAME=post1 GIT_COMMITTER_NAME=post1 GIT_AUTHOR_EMAIL=post1@agi GIT_COMMITTER_EMAIL=post1@agi AGI_POST=post1 PATH=${XP:-$D/bin:$PATH} ${CAP:+"AGI_CAPSULE=$CAP"} ${SO:+"AGI_SEAL_OPEN=$SO"} setsid sh ${PIECE:-$D/agi-out} </dev/null)>$D/o 2>&1;return $?;}
nc(){ git -C $H/t rev-list --count refs/heads/posts/post1;}
ringown(){ git -C $H/t show refs/heads/posts/post1:$GEO/ring|awk '$1=="post1"';}
# --- inputs: empty, 1 byte (x3), no trailing newline, newline, binary, the old fixture's plaintext, around the block sizes, 64 KiB, the largest real share (a stand-in: 256 KiB), all-NUL, all-0xff, CRLF
mkdir $D/in;add(){ cat >$D/in/$(printf %02d $(( $(ls $D/in|wc -l)+1 )));}
: |add;printf '\0'|add;printf '\n'|add;printf a|add;printf abc|add;printf 'abc\n'|add;printf '1:123456789'|add;printf 'a b\tc'|add;printf 'caf\303\251 \342\202\254'|add;printf 'line1\r\nline2\r\n'|add
for n in 31 32 33 64 4095 4096 4097 65535 65536 65537;do head -c $n /dev/urandom|add;done
head -c 262144 /dev/urandom|add;head -c 1000 /dev/zero|add;head -c 1000 /dev/zero|tr '\0' '\377'|add
NI=$(ls $D/in|wc -l|tr -d ' ');ok rt0-at-least-20-inputs "[ $NI -ge 20 ]"
# rt <piece> <input> <generations>: old-seal -> old-open == input, then agi-out (that piece) once per generation; every generation's share opens with age -d -i the current key == input
rt(){ mkh rt legacy $2;[ "$("$SEALOPEN" $H/seal.key $H/capsule/post1 | cksum)" = "$(cksum <$2)" ]||{ echo "old-open != input">&2;return 1;};g=0
 while [ $g -lt $3 ];do g=$((g+1));PIECE=$1 CAP=capsule out||{ echo "agi-out rc $? ($(cat $D/o|head -2))">&2;return 1;};age -d -i $H/.ssh/id_ed25519 $H/capsule/post1 2>/dev/null|cmp -s - $2||{ echo "gen $g share != input">&2;return 1;};sleep 1;touch $H/.fresh;done;}
bad=0;for x in $D/in/*;do rt $D/agi-out $x 2 2>$D/rterr||{ bad=$((bad+1));echo "  input $(basename $x) ($(wc -c <$x) B): $(head -1 $D/rterr)";};done
ok rt1-round-trip-every-input-across-two-generations "[ $bad = 0 ]"
sed 's|age -R \$N/id_ed25519.pub|age -R .ssh/id_ed25519.pub|' $D/agi-out >$D/mut-R;ok rt2-mutant-wrong-recipient-has-an-effect "! cmp -s $D/agi-out $D/mut-R"
ok rt3-mutant-wrong-recipient-reads-red "! rt $D/mut-R $D/in/07 1 2>/dev/null"
# --- the passphrase-protected key never hangs: the current key under a passphrase, the share already age
mkh pw age $D/in/07;ssh-keygen -q -p -P "" -N secret -f $H/.ssh/id_ed25519 >/dev/null 2>&1;sleep 1;touch $H/.fresh;s0=$(cksum <$H/capsule/post1);t0=$(date +%s);CAP=capsule out;rc=$?;t1=$(date +%s)
ok pw1-passphrase-key-refused-by-name-in-time "[ $rc = 75 ]&&[ $((t1-t0)) -lt 25 ]&&grep -q 'passphrase-protected key never prompts' $H/.ssh/out-refused"
ok pw2-nothing-committed-nothing-swapped "[ \"\$(nc)\" = 1 ]&&[ ! -d $H/.ssh/n ]&&[ \"\$(cksum <$H/capsule/post1)\" = \"$s0\" ]&&[ ! -e $H/capsule/post1.new ]&&[ -z \"\$(git -C $H/t status --porcelain)\" ]"
mkdir -p $D/hang;printf '#!/bin/sh\nexec sleep 100\n' >$D/hang/age;chmod +x $D/hang/age;sed 's|timeout 20|timeout 2|g' $D/agi-out >$D/mut-T
mkh pt age $D/in/07;t0=$(date +%s);XP=$D/hang:$D/bin:/usr/bin:/bin PIECE=$D/mut-T CAP=capsule out;rc=$?;t1=$(date +%s)
ok pw3-a-hung-age-is-cut-by-the-timeout "[ $rc = 75 ]&&[ $((t1-t0)) -lt 20 ]&&[ \"\$(nc)\" = 1 ]&&grep -q 'timed out or failed' $H/.ssh/out-refused"
# --- the ring: the legacy x25519 line is carried verbatim, never regenerated; a post with none gets none
mkh rg legacy $D/in/07;x0=$(ringown|awk '$2=="x25519"');CAP=capsule out;x1=$(ringown|awk '$2=="x25519"')
ok ring1-legacy-line-carried-verbatim "[ -n \"$x0\" ]&&[ \"$x0\" = \"$x1\" ]&&[ \$(ringown|wc -l) = 3 ]&&[ \"\$(nc)\" = 2 ]"
mkh rn none;CAP=capsule out;ok ring2-a-post-with-no-legacy-line-gets-none "[ \$(ringown|wc -l) = 2 ]&&! ringown|grep -q x25519&&[ \"\$(nc)\" = 2 ]&&[ ! -e $H/capsule/post1 ]"
mkh rg2 age $D/in/07;ok ring3-an-age-share-needs-no-legacy-material "[ ! -e $H/seal.key ]&&CAP=capsule out&&age -d -i $H/.ssh/id_ed25519 $H/capsule/post1|cmp -s - $D/in/07"
# --- no age on the PATH: refuse before any state changes
mkh na legacy $D/in/07;s0=$(cksum <$H/capsule/post1);k0=$(cksum <$H/.ssh/id_ed25519);mkdir -p $D/noage;for c in head cut awk sed git ssh-keygen timeout base64 cksum mv rm mkdir cat printf sh setsid env readlink;do ln -sf $(command -v $c) $D/noage/$c;done
XP=$D/bin:$D/noage CAP=capsule out;rc=$?;ok na1-no-age-refuses-first "[ $rc = 75 ]&&grep -q 'age is not installed' $H/.ssh/out-refused&&[ \"\$(nc)\" = 1 ]&&[ ! -d $H/.ssh/n ]&&[ \"\$(cksum <$H/capsule/post1)\" = \"$s0\" ]&&[ \"\$(cksum <$H/.ssh/id_ed25519)\" = \"$k0\" ]"
# --- the piece names none of the retired words (the installed set is checked against these bytes by the host act)
n=$(grep -c -E 'python3|cryptography|X25519' $D/agi-out);ok gr1-the-piece-carries-0-python-and-no-retired-word "[ $n = 0 ]"
G=$(cd $R0&&git rev-parse -q --verify 62ccf142c9^{commit} 2>/dev/null)
if [ "$G" ];then (cd $R0&&git show 62ccf142c9:$GEO/engine-post.md)|sed -n '/^### agi-out /,/^### /{/^~~~/,/^~~~/{//!p}}'>$D/old-out;m=$(grep -c -E 'python3|cryptography|X25519' $D/old-out);ok gr2-mutant-the-pre-switch-piece-reads-red "[ $m -gt 0 ]";else echo "ok gr2-mutant-the-pre-switch-piece-reads-red (skipped: no pre-switch commit here)";fi
echo "agi-out piece $(wc -c <$D/agi-out) B sha256 $(sha256sum <$D/agi-out|cut -d' ' -f1)"
# --- the census over the BOOT SET: `opened k/m (homes h/h read)`; anything not read is `unread (...)`, rc 1; the clean zero needs every home read
# mkcs NAME:MODE ...: one home per spec under $D/cs and one agi-post@NAME.service link in $D/cw (the boot set); MODE age|legacy|none (none = a readable home with an empty capsule dir)
mkcs(){ rm -rf $D/cs $D/cw;mkdir -p $D/cs $D/cw;for spec in "$@";do n=${spec%%:*};m=${spec#*:};: >$D/cw/agi-post@$n.service;mkdir -p $D/cs/$n/capsule;[ $m = none ]&&continue;mkh cs$n $m $D/in/07;cp -r $H/.ssh $D/cs/$n/.ssh;cp $H/capsule/post1 $D/cs/$n/capsule/$n;[ -f $H/seal.key ]&&cp $H/seal.key $D/cs/$n/seal.key;done;}
census(){ WANTS=$D/cw STORES=$D/cs AGI_SEAL_OPEN=$SEALOPEN sh ${CS:-$CENSUS} 2>$D/cserr;}
rest(){ chmod -R u+rwx $D/cs 2>/dev/null;}
if [ -f $CENSUS ];then
 mkcs a:age b:legacy c:age;r=$(census);rc=$?;ok cs1-all-open "[ \"\$(echo \"$r\"|head -1)\" = 'opened 3/3 (homes 3/3 read)' ]&&[ $rc = 0 ]&&echo \"$r\"|grep -q 'legacy 1/3'"
 mkcs a:age b:legacy;: >$D/cs/b/capsule/b;r=$(census);rc=$?;ok cs2-an-empty-share-is-not-opened "[ \"\$(echo \"$r\"|head -1)\" = 'opened 1/2 (homes 2/2 read)' ]&&[ $rc = 1 ]"
 mkcs a:age b:age;printf 'AAAA' >$D/cs/b/capsule/b;r=$(census);rc=$?;ok cs3-a-broken-share-is-not-opened "[ \"\$(echo \"$r\"|head -1)\" = 'opened 1/2 (homes 2/2 read)' ]&&[ $rc = 1 ]"
 mkcs a:none b:none c:none;rm -rf $D/cs/c/capsule;r=$(census);rc=$?;ok cs4-every-home-read-and-empty-is-the-clean-zero "[ \"\$(echo \"$r\"|head -1)\" = 'opened 0/0 (homes 3/3 read)' ]&&[ $rc = 0 ]"
 mkcs a:age b:age;rm -rf $D/cs/b;r=$(census);rc=$?;ok cs5-an-absent-home-is-unread-not-skipped "[ \"\$r\" = 'unread (homes b)' ]&&[ $rc = 1 ]"
 mkcs a:age b:age;chmod 000 $D/cs/b/capsule;r=$(census);rc=$?;rest;ok cs6-a-capsule-dir-mode-000-next-to-a-good-home-is-unread "[ \"\$r\" = 'unread (homes b)' ]&&[ $rc = 1 ]"
 mkcs a:age b:age;chmod 000 $D/cs/b/capsule/b;r=$(census);rc=$?;rest;ok cs7-an-unreadable-share-is-unread "[ \"\$r\" = 'unread (homes b)' ]&&[ $rc = 1 ]"
 mkcs a:none b:none;ln -s /nonexistent-share $D/cs/a/capsule/a;r=$(census);rc=$?;ok cs14-a-dangling-share-link-is-unread-not-the-clean-zero "[ \"\$r\" = 'unread (homes a)' ]&&[ $rc = 1 ]"
 mkcs a:none b:none;mkdir $D/cs/a/capsule/sub;r=$(census);rc=$?;ok cs15-a-directory-in-capsule-is-unread "[ \"\$r\" = 'unread (homes a)' ]&&[ $rc = 1 ]"
 mkcs a:none b:none;rm -rf $D/cs/b/capsule;ln -s /nonexistent-capsule $D/cs/b/capsule;r=$(census);rc=$?;ok cs18-a-dangling-capsule-link-is-unread-not-the-clean-zero "[ \"\$r\" = 'unread (homes b)' ]&&[ \$rc = 1 ]"
 mkcs a:none b:none;: >$D/cs/b/capsule/.hidden;r=$(census);rc=$?;ok cs16-a-dot-named-entry-is-not-dropped "[ \"\$(echo \"$r\"|head -1)\" != 'opened 0/0 (homes 2/2 read)' ]&&[ $rc = 1 ]"
 mkcs a:age b:none;cp $D/cs/a/capsule/a $D/cs/b/capsule/.b;cp -r $D/cs/a/.ssh $D/cs/b/.ssh;r=$(census);rc=$?;ok cs16b-a-dot-named-share-is-counted-and-opened "[ \"\$(echo \"$r\"|head -1)\" = 'opened 2/2 (homes 2/2 read)' ]&&[ $rc = 0 ]"
 mkcs a:age b:age;chmod 000 $D/cs/b;r=$(census);rc=$?;rest;ok cs8-a-home-mode-000-is-unread "[ \"\$r\" = 'unread (homes b)' ]&&[ $rc = 1 ]"
 mkcs a:none;rm -rf $D/cw;r=$(census);rc=$?;ok cs9-no-boot-set-is-unread "[ \"\$r\" = 'unread (boot set: no wants dir)' ]&&[ $rc = 1 ]"
 mkcs a:none;rm -f $D/cw/*;r=$(census);rc=$?;ok cs10-an-empty-boot-set-is-unread "[ \"\$r\" = 'unread (boot set: empty)' ]&&[ $rc = 1 ]"
 # mutants: each edit of the census must change the verdict on its fixture
 sed 's/||{ k=\$((k+1));//;s/||bad="\$bad \${F##\*\/}"/||{ k=$((k+1));bad="$bad ${F##*\/}";}/' $CENSUS >$D/mut-cs1;mkcs a:age b:age;printf 'AAAA' >$D/cs/b/capsule/b;CS=$D/mut-cs1;r=$(census);ok cs11-mutant-counting-a-failed-open-reads-red "[ \"\$(echo \"$r\"|head -1)\" != 'opened 1/2 (homes 2/2 read)' ]";CS=
 sed 's/^ \[ -d "\$H" -a -r "\$H" -a -x "\$H" \].*$/ :/' $CENSUS >$D/mut-cs2;cmp -s $CENSUS $D/mut-cs2&&echo "FAIL cs12-mutant-has-no-effect";mkcs a:age b:age;rm -rf $D/cs/b;CS=$D/mut-cs2;r=$(census);ok cs12-mutant-skipping-an-absent-home-reads-red "[ \"\$(echo \"$r\"|head -1)\" = 'opened 1/1 (homes 2/2 read)' ]&&[ \"\$r\" != 'unread (homes b)' ]";CS=
 sed 's/^ if \[ -e "\$H\/capsule" \].*$/ :/' $CENSUS >$D/mut-cs3;cmp -s $CENSUS $D/mut-cs3&&echo "FAIL cs13-mutant-has-no-effect";mkcs a:age b:age;chmod 000 $D/cs/b/capsule;CS=$D/mut-cs3;r=$(census);rest;ok cs13-mutant-skipping-an-unlistable-capsule-dir-reads-red "[ \"\$(echo \"$r\"|head -1)\" = 'opened 1/1 (homes 2/2 read)' ]";CS=
 sed 's/^  \[ -f "\$F" -a -r "\$F" \].*$/  [ -f "$F" ]||continue;m=$((m+1))/;s/ || \[ -L "\$F" \]//' $CENSUS >$D/mut-cs4;cmp -s $CENSUS $D/mut-cs4&&echo "FAIL cs17-mutant-has-no-effect";mkcs a:none b:none;ln -s /nonexistent-share $D/cs/a/capsule/a;CS=$D/mut-cs4;r=$(census);ok cs17-mutant-dropping-a-dangling-link-reads-the-clean-zero-RED "[ \"\$(echo \"$r\"|head -1)\" = 'opened 0/0 (homes 2/2 read)' ]";CS=
 sed 's/ if \[ -e "\$H\/capsule" \]||\[ -L "\$H\/capsule" \];then/ if [ -e "$H\/capsule" ];then/' $CENSUS >$D/mut-cs5;cmp -s $CENSUS $D/mut-cs5&&echo "FAIL cs18b-mutant-has-no-effect";mkcs a:none b:none;rm -rf $D/cs/b/capsule;ln -s /nonexistent-capsule $D/cs/b/capsule;CS=$D/mut-cs5;r=$(census);ok cs18b-mutant-taking-a-dangling-capsule-as-absent-reads-the-clean-zero-RED "[ \"\$(echo \"\$r\"|head -1)\" = 'opened 0/0 (homes 2/2 read)' ]";CS=
else ok cs0-the-census-command-exists false;fi
echo "agi-seal: $f FAIL";exit $f
