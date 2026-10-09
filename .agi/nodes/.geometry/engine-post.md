---
id: config:engine-post
mint_id: fa9a95e8a5d549ef9813dd728f5cefcf
type: config
parents:
  - goal:g7.16.1.11.5
next_edges: []
edited_by: belam
scaffold_hash: 7996e6cf607efb67
season: 2
town: core
---
# config:engine-post

EXPANSION of config:engine: the post body (brief, meter, turn, links, trees, tick, frontier)
Read through `sect <name> [REV]` (every `.geometry/engine*.md` at one REV) and the unit's extraction loop (engine.md + engine-post + engine-wrap); every piece is in config:engine's map.

## files — depth 2, each whole; extract: sect <name> [REV]

### agi-brief (1276 B)
~~~sh
#!/bin/sh
p=$AGI_SEAT;cd ~/t;s=$(jq -r .source);case $AGI_HARNESS in pi*)B=${B:-40000};;esac
sect brief.py|python3 - .agi/nodes doc:card-$p,$AGI_SEEDS$(find $(git rev-parse --git-common-dir)/refs/claims -user $USER -printf ,%f 2>/dev/null) ${K:-20}>~/.brief;cat ~/.brief;cut -d' ' -f4 ~/.brief|xargs tail -n+1|head -c ${B:-0}
w=${AGI_WT:-$RUNTIME_DIRECTORY/wt};for r in $(git for-each-ref --format='%(refname)' refs/archive/${AGI_POST:-$p});do git log --format=%s $r --not refs/heads/posts/${AGI_POST:-$p}|grep -q '^[^ ]*: kept '&&echo "[kept] $r: a stop left this tree whole; recover it, then git update-ref -d it";done;ls -d $w/*/ 2>/dev/null|sed 's/^/[tree] /'
[ "$s" = compact ]&&exit;jq -n "{seat:\"$p\",rotation:\"engine-v4\",result:\"success\",source:\"$s\",pid:0,window:\"\",recorded_at:\"$(date -u +%FT%TZ)\"}">$O/.agi/sessions/rotations/$p.$(date -u +%Y%m%dT%H%M%SZ).json
[ "$s" = resume ]||{ echo "## STARTUP OUTPUT";sed -n "/^  $AGI_ROLE:/,/^  [a-z_]*:\$/{/first_turn:/,/after_join:/s/^        - //p}" .agi/nodes/.geometry/rotations.md|jq -r '"\(.label)\t\(.byte_cap//3000)\t\(.cmd)"'|sed "s|{seat}|$p|g;s|{repo}|$O|g;s|{worktree}|$PWD|g;s|{prime_ref}|belam|g"|while IFS='	' read -r l b c;do echo "### $l";timeout 30 sh -c "$c" 2>&1|head -c $b;done|head -c 8000;}
~~~

### brief.py (810 B)
~~~py
import os,re,sys,cmath
R,S,k=sys.argv[1:];q=cmath.exp(.5j);P={};A={};M={};f=lambda r,h:re.search(r,h,re.M)
for d,_,F in os.walk(R):
 for n in F:
  h=open(d+'/'+n,errors='ignore').read(4000);i=f(r'^id: (\S+)',h)
  if i and i[1] not in P:
   i=i[1];P[i]=d+'/'+n;M[(f(r'^mint_id: (\S+)',h)or'00')[1]]=i
   for t in re.findall(r'^  - (\S+)',(f(r'^parents:\n((?:  - .*\n)*)',h)or'00')[1],re.M):A.setdefault(i,[]).append((t,q));A.setdefault(t,[]).append((i,1/q))
S=[M.get(s,s) for s in S.split(',') if M.get(s,s) in P];x={s:1/len(S) for s in S}
for _ in range(30):
 y={s:.15/len(S) for s in S}
 for u,v in x.items():
  for w,z in A.get(u,()):y[w]=y.get(w,0)+.85*v*z/len(A[u])
 x=y
for i in sorted([i for i in x if i in P],key=lambda i:-abs(x[i]))[:int(k)]:print('%.3f %+.1f'%(abs(x[i]),cmath.phase(x[i])/.5),i,P[i])
~~~

### agi-meter (574 B)
~~~sh
#!/bin/sh
j=$(cat);t=$(echo "$j"|jq '.tokens//empty');[ "$t" ]||t=$(echo "$j"|jq -r .transcript_path|xargs tac 2>/dev/null|jq -nR 'first(inputs|fromjson?|select((.message.usage.input_tokens)?|type=="number")|.message.usage|.input_tokens+((.cache_read_input_tokens|numbers)//0)+((.cache_creation_input_tokens|numbers)//0))');w=$(echo "$j"|jq ".context_window//${AGI_WINDOW:-1000000}")
[ "${t:-0}" -gt $((w*${AGI_ROTATE_PCT:-47}/100)) ] 2>/dev/null&&echo "At the line ($t/$w): write your card in its node tree (agi-wt pull), run agi-flush, then: touch ~/.fresh;kill \$PPID";:
~~~

### agi-at (759 B)
~~~sh
#!/bin/sh
# agi-at PATH...: ONE signed commit of ~/t's paths onto posts/P by CAS on the tip read; a miss = [raced], exit 4, the edit stays; a kid, no AGI_POST or no posts/P = rc 5 before any write; ~/t = a detached view of the tip
cd ~/t;P=$AGI_POST;b=refs/heads/posts/$P;{ [ "$P" ]&&[ "$AGI_ROLE" != kid ]&&git rev-parse -q --verify $b>/dev/null;}||{ echo "[no-branch] $P: a kid, or no posts/$P: nothing committed">&2;exit 5;};x=$(mktemp -u);trap 'rm -f $x' 0;export GIT_INDEX_FILE=$x;t=$(git rev-parse $b)&&git read-tree $t&&git add -A -- "$@"&&n=$(git write-tree)||exit 1
[ $n = $(git rev-parse $t^{tree}) ]&&exit;c=$(echo "$P: $*"|git commit-tree -S -p $t $n)&&git update-ref $b $c $t||{ echo "[raced] $*">&2;exit 4;}
unset GIT_INDEX_FILE;git reset -q $b
~~~

### agi-turn (3064 B)
~~~sh
#!/bin/sh
# agi-turn: each changed node tree = ONE grid commit on posts/P (temp index from the tip, signed, CAS); the tip moved it since pull = archived + dropped; a tree is purged ONLY once its commit is proven AND the whole tree is clean against it (agi-turn chk DIR COMMIT: a file outside .p keeps it, [dirty]; a git failure keeps it too); agi-turn purge DIR = that check then rm, else EVERY file of the tree goes to refs/archive/P/<dir> (signed, CAS), [kept] names it, rc 1; a kid (AGI_ROLE=kid, which agi-kid sets), no AGI_POST or no posts/P = rc 5, nothing committed (the SAME guard line first in agi-at, agi-turn and agi-flush; a Stop hook must never exit 2); any failure keeps the tree (rc != 0, a [label]); ~/t = a detached read view
cd ~/t;P=$AGI_POST;b=refs/heads/posts/$P;x=$(mktemp -u);trap 'rm -f $x $x.l' 0;export GIT_INDEX_FILE=$x;k=0
c(){ [ "$2" ]&&git read-tree $2&&git --work-tree=$1 diff --name-only --diff-filter=MT>$x.l&&git --work-tree=$1 ls-files -o>>$x.l||return 2;l=$(grep -vxF -e .p -e .b $x.l|tr '\n' ' ');[ -z "$l" ];}
[ "$1" = chk ]&&{ c $2 $3;r=$?;[ $r = 0 ]&&exit;[ $r = 1 ]&&echo "[dirty] $(basename $2): kept, not in the commit: $l">&2||echo "[dirty] $(basename $2): kept, cannot read it against '$3'">&2;exit 1;}
{ [ "$P" ]&&[ "$AGI_ROLE" != kid ]&&git rev-parse -q --verify $b>/dev/null;}||{ echo "[no-branch] $P: a kid, or no posts/$P: nothing committed">&2;exit 5;}
[ "$1" = purge ]&&{ d=${2%/};m=${d##*/};c $d $(cat $d/.b 2>/dev/null||git rev-parse $b);[ $? = 0 ]&&{ rm -rf $d;exit;};a=refs/archive/$P/$m;o=$(git rev-parse -q --verify $a||:)
 t=$(git rev-parse $b)&&git read-tree $t&&git --work-tree=$d add --ignore-removal -f -- . ':!.p' ':!.b'&&n=$(git write-tree)&&e=$(echo "$P: kept $m"|git commit-tree -S -p $t ${o:+-p $o} $n)&&git update-ref $a $e "$o"&&s="whole tree committed to $a"||s="NOT SAVED: the ref write failed";echo "[kept] $m: ${l:-unreadable}: $s">&2;exit 1;}
for d in ${AGI_WT:-$RUNTIME_DIRECTORY/wt}/*/;do [ -f $d.p ]||continue;m=$(basename $d);t=$(git rev-parse $b)&&git read-tree $t&&a=$(git --work-tree=$d add -A --pathspec-from-file=$d.p 2>&1)&&n=$(git write-tree)||{ echo "[stage] $m: $(echo "${a:-git failed}"|tr '\n' ' ')">&2;k=1;continue;}
 [ $n = $(git rev-parse $t^{tree}) ]&&continue;r=$b;o=$t;q=;[ ! -f $d.b ]||(IFS='
';set -f;git diff --quiet $(cat $d.b) $t -- $(cat $d.p))||{ r=refs/archive/$P/$m;o=$(git rev-parse -q --verify $r||:);q=${o:+-p $o};}
 c=$(echo "$P: $(sed q $d.p)"|git commit-tree -S -p $t $q $n 2>&1)||{ echo "[commit] $m: cannot sign or commit: $c">&2;k=1;continue;}
 git update-ref $r $c "$o"||{ echo "[raced] $m">&2;k=4;continue;}
 [ $r = $b ]&&{ echo $c>$d.b;continue;};agi-turn chk $d $c&&{ echo "[moved] $m: changed on the tip since pull; your version is $r, the tree is dropped">&2;rm -rf $d;continue;};echo "[moved] $m: your version is $r, the tree is KEPT">&2;k=1;done
unset GIT_INDEX_FILE;git checkout -q --detach $b;git status -s|grep -q .&&echo "[out-of-tree] ~/t has $(git status -s|wc -l) unversioned change(s): edit in a node's tree (agi-wt pull)">&2;exit $k
~~~

### agi-wt (1375 B)
~~~sh
#!/bin/sh
# agi-wt pull ID [REV] | new PATH [PAYLOAD] | drop ID: a node's tiny tree (node + payload, ONE PATH PER LINE in .p) in RAM for the session; agi-turn versions it, drop purges it only after a proven turn
cd ~/t;[ "$AGI_POST" ]||{ echo "agi-wt: no AGI_POST">&2;exit 5;};IFS='
';set -f;w=${AGI_WT:-$RUNTIME_DIRECTORY/wt};r=${3:-posts/$AGI_POST};mkdir -p $w
case $1 in new)n=$(basename $2 .md);case $n in ''|[!A-Za-z0-9_-]*|*[!A-Za-z0-9._-]*)echo "agi-wt: new $2: the basename [$n] must match [A-Za-z0-9_-][A-Za-z0-9._-]*">&2;exit 7;;esac;d=$w/$n;mkdir $d||exit 3;printf '%s\n' "$2" ${3:+"$3"}>$d/.p;echo $d;exit;;esac
f=$(git grep -lE "^(id|mint_id): $2$" $r -- .agi/nodes|head -1|cut -d: -f2-);[ "$f" ]||exit 2;d=$w/$(git show $r:$f|sed -n 's/^mint_id: //p')
case $1 in pull)[ -d $d ]&&{ echo $d;exit;};[ $(df --output=pcent $w|tail -1|tr -dc 0-9) -lt ${AGI_WT_HOLD:-60} ]||{ echo "hold $w";exit 3;}
mkdir $d;printf '%s\n' "$f" $(git show $r:$f|sed -n 's/^payload_ref: "\{0,1\}\([^"]*\)"\{0,1\}$/\1/p')>$d/.p
e=$(git archive -o $d.tar $r $(cat $d/.p) 2>&1&&tar -xC $d -f $d.tar 2>&1)||{ rm -rf $d $d.tar;echo "agi-wt: pull $2 failed: $e">&2;exit 6;};rm $d.tar;git rev-parse $r>$d/.b;echo $d;;
drop)[ -d $d ]||{ echo "agi-wt: no tree $d for $2 (a 'new' tree is dropped by agi-flush)">&2;exit 2;};agi-turn&&{ [ ! -d $d ]||agi-turn chk $d $(cat $d/.b)&&rm -rf $d;};;esac
~~~

### agi-track (89 B)
~~~sh
#!/bin/sh
grep --line-buffered -o '"/[^"]*"'|awk '!s[$0]++{print;fflush()}'>>$HOME/track
~~~

### agi-flush (994 B)
~~~sh
#!/bin/sh
# agi-flush: the writer guard first (a kid, no AGI_POST or no posts/P = rc 5, nothing written), then land every tree (4 turns), then agi-turn purge each dir left under $AGI_WT, found by DIR (pulled or new): clean = removed, anything else = kept whole on refs/archive/P/<dir> and [kept]: rc 0 iff no tree remains; then merge the trunk, resolved ONCE
cd ~/t;P=$AGI_POST;b=refs/heads/posts/$P;{ [ "$P" ]&&[ "$AGI_ROLE" != kid ]&&git rev-parse -q --verify $b>/dev/null;}||{ echo "[no-branch] $P: a kid, or no posts/$P: nothing committed">&2;exit 5;};w=${AGI_WT:-$RUNTIME_DIRECTORY/wt};agi-turn||agi-turn||agi-turn||agi-turn;k=$?;for d in $w/*/;do [ -d $d ]&&{ agi-turn purge $d||[ $k != 0 ]||k=1;};done
t=$(git rev-parse $b)&&T=$(git rev-parse ${AGI_TRUNK:-trunk})&&! git merge-base --is-ancestor $T $b&&n=$(git merge-tree --write-tree $b $T)&&c=$(echo "$AGI_POST: merge ${AGI_TRUNK:-trunk}"|git commit-tree -S -p $t -p $T $n)&&git update-ref $b $c $t
git checkout -q --detach $b;exit $k
~~~

### agi-out (3090 B)
~~~sh
#!/bin/sh
# agi-out (ExecStartPre): the out-line g -> g+1 (AB; the full account is in the node). A ring in ~/t and .fresh newer than the key: new keys in ~/.ssh/n, the capsule share re-wrapped to the next seal FIRST, ONE ring commit signed by the CURRENT key (the self-revocation), then next moves over current. A refusal (any exit after the cd; an AGI_CAPSULE off [A-Za-z0-9._/-], absolute, with .., not resolving to ~/capsule or below) writes its reason to ~/.ssh/out-refused + stderr, exits 75; with that marker and no newer .fresh a start exits 75 silently and the unit's ExecCondition skips it; every other start clears it. Dir 0700, share 0600.
cd||exit 1;m=.ssh/out-refused;[ -e $m ]&&{ [ .fresh -nt $m ]||exit 75;};rm -f $m;x(){ echo "agi-out: $*">&2;echo "$*">$m;exit 75;};P=$AGI_SEAT;R=.agi/nodes/.geometry/ring;N=.ssh/n;C=${AGI_CAPSULE:+$AGI_CAPSULE/$P}
[ -f t/$R ]&&{ [ -d $N ]||[ .fresh -nt .ssh/id_ed25519 ];}||exit 0
c=$AGI_CAPSULE;[ -z "$c" ]||{ case $c in -*|/*|*..*|*[!A-Za-z0-9._/-]*)x "AGI_CAPSULE off the safe set";;esac;h=$(pwd -P);case $(readlink -m -- "$c") in "$h"/capsule|"$h"/capsule/?*);;*)x "AGI_CAPSULE must resolve under ~/capsule";;esac;}
y='import sys,base64 as B,hashlib as H
from cryptography.hazmat.primitives.asymmetric.x25519 import X25519PrivateKey as K,X25519PublicKey as P
from cryptography.hazmat.primitives.ciphers.aead import ChaCha20Poly1305 as C
a=sys.argv;h=lambda x:H.sha256(x).digest();d=lambda b:B.b64encode(b).decode()
if a[1]=="gen":k=K.generate();open(a[2],"w").write(d(k.private_bytes_raw()));print(d(k.public_key().public_bytes_raw()))
else:
 p,z=open(a[3]).read().split();z=B.b64decode(z);m=C(h(K.from_private_bytes(B.b64decode(open(a[2]).read())).exchange(P.from_public_bytes(z[:32])))).decrypt(bytes(12),z[32:],None);e=K.generate();print(p,d(e.public_key().public_bytes_raw()+C(h(e.exchange(P.from_public_bytes(B.b64decode(a[4]))))).encrypt(bytes(12),m,None)))'
o=$(git -C t show HEAD:$R)||x "the ring is unreadable";umask 77
[ -s $N/seal.pub -a "$(printf '%s\n' "$o"|awk -v p=$P '$1==p&&$2=="x25519"{print $3}')" = "$(cat $N/seal.pub 2>/dev/null)" ]||{
 { [ -f seal.key -a -z "$C" ]||[ -f "$C" -a ! -f seal.key ];}&&x "the capsule share cannot be re-wrapped (no capsule, or no seal key to open it with)"
 rm -rf $N ${C:+"$C.new"};mkdir -p $N ${C:+"$c"}&&ssh-keygen -qN "" -ted25519 -f$N/id_ed25519||{ rm -rf $N;x "keygen failed";}
 s=$(python3 -c "$y" gen $N/seal.key)||{ rm -rf $N;x "seal keygen failed";};echo $s>$N/seal.pub
 [ -f "$C" -a -f seal.key ]&&{ python3 -c "$y" wrap seal.key "$C" $s>"$C.new"||{ rm -rf $N "$C.new";x "the wrap failed";};}
 { printf '%s\n' "$o"|awk -v p=$P 'NF&&$1!=p';printf '%s ssh-ed25519 %s\n%s pq-sha256 %s\n%s x25519 %s\n' $P $(cut -d' ' -f2 $N/id_ed25519.pub) $P $(head -c32 /dev/urandom|base64) $P $s;}>t/$R
 agi-at $R||{ git -C t checkout -q -- $R;rm -rf $N ${C:+"$C.new"};x "the ring commit failed";}
}
[ -f "$C.new" ]&&mv "$C.new" "$C"
[ -f $N/id_ed25519.pub ]&&{ [ -f $N/id_ed25519 ]&&mv $N/id_ed25519 .ssh/;mv $N/id_ed25519.pub .ssh/;}
[ -f $N/seal.key ]&&mv $N/seal.key seal.key;rm -rf $N
~~~

### gitconfig (198 B)
~~~ini
[gpg]
format=ssh
[gpg "ssh"]
allowedSignersFile=/var/lib/agi/allowed_signers
[commit]
gpgsign=true
[user]
signingkey=~/.ssh/id_ed25519.pub
email=agi@agi
[core]
hooksPath=~/hooks
[safe]
	directory=*
~~~

### sysusers.conf (41 B)
~~~ini
u agi-@ - "@" /var/lib/agi/@
m agi-@ agi
~~~

### agi.rules (242 B)
~~~js
polkit.addRule(function(a,s){var m=/^agi-post@([a-z0-9-]+)\.service$/.exec(a.lookup("unit"));if(a.id=="org.freedesktop.systemd1.manage-units"&&a.lookup("verb")=="start"&&m&&s.user=="agi-"+m[1]&&s.isInGroup("agi"))return polkit.Result.YES;});
~~~

### project.sh (161 B)
~~~sh
#!/bin/sh
o=$(mktemp -d);sect agi-project|sh -s $o HEAD;sed -n 's/^u agi-\([^ ]*\) .*/user agi-\1\nunit agi-post@\1\nbrief agi-\1/p' $o/agi-users.conf;rm -rf $o
~~~

### observe.sh (255 B)
~~~sh
#!/bin/sh
getent passwd|awk -F: '/^agi-/{print "user",$1;system("jq -e .hooks.SessionStart "$6"/.claude/settings.json>/dev/null 2>&1&&echo brief "$1)}'
systemctl list-units --state=active --plain --no-legend 'agi-post@*'|sed 's/\.service .*//;s/^/unit /'
~~~

### tick.sh (254 B)
~~~sh
#!/bin/sh
cd ~/t;mkdir -p .agi/drift;sect project.sh|sh|sort>~/.p;sect observe.sh|sh|sort>~/.q;diff ~/.p ~/.q>.agi/drift/$USER&&exit
grep '^< unit' .agi/drift/$USER|cut -d' ' -f3|grep -x agi-post@${USER#agi-}|xargs -rn1 systemctl start;agi-at .agi/drift
~~~

### agi-frontier (460 B)
~~~sh
#!/bin/sh
r=$1;git grep --all-match -l -e '^type: goal$' -e '^status: active$' $r -- .agi|while IFS=: read _ f;do n=$(git show $r:$f);g=$(echo "$n"|sed -n 's/^id: goal://p')
c=$(echo "$n"|sed -n '/^## Falsifier/,/^## Out/p'|grep -o '`[^`]*`'|tr -d '`'|grep -Em1 '^(grep|test|ls|getent|git (log|show|grep|rev-parse|ls-files|diff|for-each-ref)) ')
[ "$c" ]||{ echo mute $g;continue;};timeout 30 sh -c "$c"</dev/null>/dev/null 2>&1&&echo met $g||echo red $g;done
~~~

### box (2005 B)
~~~sh
#!/bin/sh
# box send TO <msg | box read | box n | box carry HUB POST..: mail = signed commits on refs (doc:radically-simple-engine §AA1)
# out refs/box/P/TO (only P) · in refs/box/*/P · held refs/held/P/FROM (only P) · unread = in --not held
P=${AGI_POST:?};m=refs/box
# the matrix: a and b mail iff their levels differ by <= 1; level = rows up to owner, an inert row (no harness) counts 0
a(){ git show ${AGI_TRUNK:-HEAD}:.agi/nodes/.geometry/posts.md|sed -n 's/^  - {/{/p'|jq -se --arg a $1 --arg b $2 'map({(.name):.})|add as $r|def i(x):$r[x]|has("harness")|not;def l(x;n):if x=="owner" then 0 elif n>20 or $r[x]==null then -99 else (if i(x) then 0 else 1 end)+l($r[x].parent//"";n+1) end;l($a;0) as $x|l($b;0) as $y|$x>0 and $y>0 and ($r[$a]|has("harness")) and ($r[$b]|has("harness")) and $a!=$b and ($x-$y|fabs)<=1'>/dev/null;}
case $1 in
send)a $P $2||{ echo "[off-matrix] $P -> $2: not adjacent, nothing sent">&2;exit 1;};r=$m/$P/$2;b=$(cat);k=0
 until o=$(git rev-parse -q --verify $r);[ -z "$o" ]||git verify-commit --raw $o 2>&1|grep -q "for $P@agi with"||{ echo "[squatted] $r $o: not mine, nothing sent">&2;exit 1;}
  c=$(printf '%s\n' "$b"|GIT_AUTHOR_EMAIL=$P@agi GIT_COMMITTER_EMAIL=$P@agi git commit-tree -S ${o:+-p $o} $(git hash-object -w -t tree /dev/null))&&git update-ref $r $c "$o" 2>/dev/null;do k=$((k+1));[ $k -lt 5 ]||{ echo "[unsent] $r: the tip moved 5 times">&2;exit 1;};done;;
read|n)git for-each-ref --format='%(refname)' $m|grep "/$P$"|while read r;do f=${r#$m/};f=${f%/*};h=refs/held/$P/$f
 a $f $P||{ echo "[off-matrix] $f";continue;}
 for c in $(git rev-list --reverse $r --not $(git rev-parse -q --verify $h));do
  git verify-commit --raw $c 2>&1|grep -q "for $f@agi with"||{ echo "[refused] $f $c";break;}
  [ $1 = n ]&&echo "$f"&&continue;echo "[$f] $(git log -1 --format=%B $c)";git update-ref $h $c;done;done;;
carry)h=$2;shift 2;x=;for p;do git push -q $h "$m/$p/*:$m/$p/*";x="$x ^$m/$p/*";done;git -c transfer.fsckObjects=1 fetch -q $h "$m/*:$m/*" $x;;
esac
~~~

<!-- THOUGHT:BEGIN — authored, not derived; carried across regenerating scans. The reasoning behind THIS version. -->
PROPOSED v5 (round 5, §Q): v4c's body pieces cut whole out of config:engine, byte for byte. SPLIT: agi-post@.service moved to engine-root (root reads it, a post does not).
<!-- THOUGHT:END -->
