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

### agi-brief (938 B)
~~~sh
#!/bin/sh
p=$AGI_SEAT;cd ~/t;s=$(jq -r .source);case $AGI_HARNESS in pi*)B=${B:-40000};;esac
sect brief.py|python3 - .agi/nodes doc:card-$p,$AGI_SEEDS$(find $(git rev-parse --git-common-dir)/refs/claims -user $USER -printf ,%f 2>/dev/null) ${K:-20}>~/.brief;cat ~/.brief;cut -d' ' -f4 ~/.brief|xargs tail -n+1|head -c ${B:-0}
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

### agi-meter (547 B)
~~~sh
#!/bin/sh
j=$(cat);t=$(echo "$j"|jq '.tokens//empty');[ "$t" ]||t=$(echo "$j"|jq -r .transcript_path|xargs tac 2>/dev/null|jq -nR 'first(inputs|fromjson?|select((.message.usage.input_tokens)?|type=="number")|.message.usage|.input_tokens+((.cache_read_input_tokens|numbers)//0)+((.cache_creation_input_tokens|numbers)//0))');w=$(echo "$j"|jq ".context_window//${AGI_WINDOW:-1000000}")
[ "${t:-0}" -gt $((w*${AGI_ROTATE_PCT:-47}/100)) ] 2>/dev/null&&echo "At the line ($t/$w): write your card, git commit it, then run: touch ~/.fresh;kill \$PPID";:
~~~

### agi-turn (269 B)
~~~sh
#!/bin/sh
cd ~/t;b=$(git rev-parse HEAD);for d in ${AGI_WT:-$RUNTIME_DIRECTORY/wt}/*/;do m=$(basename $d);git show-ref -q refs/claims/$m||agi-wt drop $m;done 2>/dev/null
git add -A;git commit -qm$USER>/dev/null 2>&1;[ $b = $(git rev-parse HEAD) ]||agi-link $b>~/link;:
~~~

### agi-link (358 B)
~~~sh
#!/bin/sh
git diff --name-only ${1:-HEAD~} HEAD -- ${AGI_LINK_ROOTS:-extensions skills src}|while read f;do n=$(git grep -lE "^payload_ref: \"?$f\"?$" HEAD -- .agi/nodes/build|head -1)
[ "$n" ]&&echo "$(git show $n|sed -n 's/^id: //p;/^id:/q') $f"||{ echo "unlinked $f";[ "$AGI_LINK_MINT" ]&&python3 extensions/agi/bin/level3.py --mint-missing-only;};done;:
~~~

### agi-wt (688 B)
~~~sh
#!/bin/sh
set -e;cd ~/t;r=${3:-HEAD};w=${AGI_WT:-$RUNTIME_DIRECTORY/wt};f=$(git grep -lE "^(id|mint_id): $2$" $r -- .agi/nodes|head -1|cut -d: -f2-);[ "$f" ]||exit 2;d=$w/$(git show $r:$f|sed -n 's/^mint_id: //p')
P="$f $(git show $r:$f|sed -n 's/^payload_ref: "\{0,1\}\([^"]*\)"\{0,1\}$/\1/p')";case $1 in pull)[ -d $d ]&&{ echo $d;exit;};mkdir -p $w
[ $(df --output=pcent $w|tail -1|tr -dc 0-9) -lt ${AGI_WT_HOLD:-60} ]||{ echo "hold $w";exit 3;};mkdir $d;git archive $r $P|tar -xC $d;git rev-parse $r>$d/.b;echo $d;;
drop)git diff --quiet $(cat $d/.b) -- $P||{ s=${AGI_POST:-$AGI_SEAT};[ "$s" ]||{ echo "agi-wt: no AGI_POST/AGI_SEAT, $2 not archived" >&2;exit 5;}
(x=$(mktemp -u);trap "rm -f $x" EXIT;b=$(cat $d/.b);export GIT_INDEX_FILE=$x;git read-tree $b&&git --work-tree=$d add -A -- $P&&git update-ref refs/archive/worktrees/$s@$(basename $d) $(git commit-tree $(git write-tree) -p $b -m wt))||{ echo "agi-wt: archive of $2 failed" >&2;exit 5;};echo "moved $2";exit 4;};tar -cC $d --exclude=.b .|tar -x;git add $P;git commit -qm"$USER: $2">/dev/null||:;rm -rf $d;;esac
~~~

### agi-track (89 B)
~~~sh
#!/bin/sh
grep --line-buffered -o '"/[^"]*"'|awk '!s[$0]++{print;fflush()}'>>$HOME/track
~~~

### agi-flush (181 B)
~~~sh
#!/bin/sh
cd ~/t;k=0;for d in ${AGI_WT:-$RUNTIME_DIRECTORY/wt}/*/;do [ -d $d ]||continue;agi-wt drop $(basename $d);[ $? = 5 ]&&k=5;done;agi-turn;git merge -q --no-edit ${AGI_TRUNK:-trunk}||git merge --abort;exit $k
~~~

### agi-out (3120 B)
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
 git -C t commit -qm "out-line $P" -- $R||{ git -C t checkout -q -- $R;rm -rf $N ${C:+"$C.new"};x "the ring commit failed";}
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

### agi.rules (211 B)
~~~js
polkit.addRule(function(a,s){if(a.id=="org.freedesktop.systemd1.manage-units"&&a.lookup("verb")=="start"&&/^agi-post@[a-z0-9-]+\.service$/.test(a.lookup("unit"))&&s.isInGroup("agi"))return polkit.Result.YES;});
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
grep '^< unit' .agi/drift/$USER|cut -d' ' -f3|xargs -rn1 systemctl start;git add .agi/drift;git commit -qm"drift: $USER"
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

### orient (1010 B)
~~~sh
#!/bin/sh
# orient (g5.34.7.2 + g5.34.7.6): connect verb + once at shell start. Clear, header, dump.
# After ===== end startup =====: captive exact `ok` (gate-e C4). 0 B to i; never truncates o.
cd ~/t||exit 1;P=${AGI_POST:?};f=$(mktemp);agi-sync "$PWD" "$f" >/dev/null 2>&1||{ rm -f "$f";echo "[refused] orient: agi-sync">&2;exit 1;}
k=$(git show ${AGI_TRUNK:-HEAD}:.agi/nodes/.geometry/posts.md|sed -n 's/^  - {/{/p'|jq -r --arg p $P 'select(.name==$p and has("grokbot"))|.engine.rotate_pct//empty'|head -1)
c=$(git rev-parse -q --short HEAD:.agi/nodes/doc/card-$P.md);printf 'c'
printf 'orient %s rev=%s dump_sha256=%s pin=%s card=%s
===== startup %s =====
' $P $(git rev-parse --short HEAD) $(sha256sum<"$f"|cut -c1-64) ${k:--} ${c:--} $P
cat "$f";printf '===== end startup =====

';rm -f "$f"
# g5.34.7.6 captive ok-gate (print AFTER end mark so dump_sha256 stays clean)
printf 'orient ready — type ok to continue
'
while IFS= read -r line || [ -n "$line" ]; do [ "$line" = ok ] && break; done
~~~

### monitor (2596 B)
~~~sh
#!/bin/sh
# monitor (g5.34.8.1 K1-K6/K8 A1-A7): check|wait. Tip-sha mail only; 0 B to i. Sole wake until agi-wake.
# Usage: monitor check <post> · monitor wait <post>… [--cursor-dir D]
set -eu
CDIR=${MONITOR_CURSOR_DIR:-/var/lib/agi-monitor/${USER:-monitor}}
# parse
cmd=${1:-};shift||true
posts="";while [ $# -gt 0 ];do case $1 in --cursor-dir)CDIR=$2;shift 2;;*)posts="$posts $1";shift;;esac;done
posts=${posts# }
[ -n "$cmd" ]&&[ -n "$posts" ]||{ echo "usage: monitor check|wait <post>… [--cursor-dir D]" >&2;exit 2;}
mkdir -p "$CDIR";chmod 700 "$CDIR" 2>/dev/null||true
mk(){ p=$1;git -C /var/lib/agi/$p/t for-each-ref --format='%(refname) %(objectname)' "refs/box/*/$p" 2>/dev/null|while read r s;do f=${r#refs/box/};f=${f%/*};h=$(git -C /var/lib/agi/$p/t rev-parse -q --verify refs/held/$p/$f 2>/dev/null||true);[ "$s" = "$h" ]||echo "$f $s";done;}
seenf(){ echo "$CDIR/$1.seen";}
cursf(){ echo "$CDIR/$1.cursor";}
lastw(){ echo "$CDIR/$1.last-woken";}
excerpt(){ git -C /var/lib/agi/$1/t log -1 --format=%s "$2" 2>/dev/null||echo "";}
check_one(){ p=$1;sf=$(seenf $p);# mail
 for pair in $(mk $p|tr ' ' ':');do f=${pair%%:*};s=${pair#*:};grep -qx "$s" "$sf" 2>/dev/null&&continue
  if git -C /var/lib/agi/$p/t merge-base --is-ancestor "$s" "refs/held/$p/$f" 2>/dev/null;then continue;fi
  echo "$p mail $s $(excerpt $p $s)";return 0;done
 # mail-unhandled: last-woken tip still unread
 if [ -f "$(lastw $p)" ];then lw=$(cat "$(lastw $p)");grep -qx "$lw" "$sf" 2>/dev/null||true
  for pair in $(mk $p|tr ' ' ':');do s=${pair#*:};[ "$s" = "$lw" ]&&{ echo "$p mail-unhandled $s $(excerpt $p $s)";return 0;};done;fi
 # card
 if [ -f /var/lib/agi/$p/.pin-crossed ]&&[ -f /var/lib/agi/$p/.pin-card ];then
  pc=$(stat -c %Y /var/lib/agi/$p/.pin-crossed 2>/dev/null||echo 0)
  lwts=$(stat -c %Y "$(lastw $p)" 2>/dev/null||echo 0)
  [ "$pc" -gt "$lwts" ]&&{ echo "$p card $pc pin-crossed";return 0;};fi
 # orient-dirty / incomplete via o tail (corroboration)
 o=/var/lib/agi/$p/o; [ -f "$o" ]||return 1
 # heartbeat file age
 hb=$CDIR/$p.heartbeat; [ -f "$hb" ]||touch "$hb"
 age=$(( $(date +%s) - $(stat -c %Y "$hb") )); [ "$age" -ge 21600 ]&&{ echo "$p heartbeat $age 6h";touch "$hb";return 0;}
 return 1;}
mark_seen(){ p=$1;cls=$2;sha=$3;echo "$sha">>$(seenf $p);echo "$sha">$(lastw $p);printf '%s\n' "$sha" >>$(cursf $p);}
case $cmd in
 check) ok=1;for p in $posts;do check_one $p&&ok=0;done;exit $ok;;
 wait) while :;do for p in $posts;do if out=$(check_one $p);then set -- $out;mark_seen "$1" "$2" "$3";echo "$out";exit 0;fi;done;sleep 2;done;;
 *) echo "unknown $cmd" >&2;exit 2;;
esac
~~~
### sm-dg-multiplex (2182 B)
~~~sh
#!/bin/sh
# sm-dg-multiplex (g5.34.8.2 O1/K3/A1/O4): SM arms ONE root monitor wait over belam SSH for manned DGs.
# Usage: sm-dg-multiplex arm <dg…> · sm-dg-multiplex drop <dg> · sm-dg-multiplex status
# Cursor: /var/lib/agi-monitor/sanctuary-master/ (700). Never SM-pane uid. Optional V3 /run/agi-<p>/driver lock.
set -eu
CDIR=${MONITOR_CURSOR_DIR:-/var/lib/agi-monitor/sanctuary-master}
STATE=$CDIR/manned.list
HOST=${BELAM_SSH_HOST:-belam}
KEY=${BELAM_SSH_KEY:-$HOME/.ssh/sanctuary_ed25519}
SSH="ssh -i $KEY -o StrictHostKeyChecking=no -o ServerAliveInterval=15 -o ServerAliveCountMax=3 $HOST"
cmd=${1:-};shift||true
mkdir -p "$CDIR";chmod 700 "$CDIR";touch "$STATE"
arm(){ for p in "$@";do grep -qx "$p" "$STATE" 2>/dev/null||echo "$p">>"$STATE";done
 posts=$(tr '\n' ' ' <"$STATE"); [ -n "$posts" ]||return 0
 # kill prior multiplex pid if any
 if [ -f "$CDIR/multiplex.pid" ];then kill "$(cat "$CDIR/multiplex.pid")" 2>/dev/null||true;fi
 # root multiplex over belam SSH (A1)
 $SSH "sudo MONITOR_CURSOR_DIR=$CDIR monitor wait $posts" &
 echo $!> "$CDIR/multiplex.pid"; echo "armed: $posts pid=$(cat $CDIR/multiplex.pid)";}
drop(){ p=$1;grep -vx "$p" "$STATE" >"$STATE.tmp" 2>/dev/null||true;mv "$STATE.tmp" "$STATE"
 if [ -f "$CDIR/multiplex.pid" ];then kill "$(cat "$CDIR/multiplex.pid")" 2>/dev/null||true;fi
 posts=$(tr '\n' ' ' <"$STATE"); [ -z "$posts" ]&&{ echo "dropped $p; none manned";return 0;}
 $SSH "sudo MONITOR_CURSOR_DIR=$CDIR monitor wait $posts" &
 echo $!> "$CDIR/multiplex.pid"; echo "re-armed without $p: $posts";}
# V3 optional driver lock
driver_lock(){ p=$1;id=$2;printf '%s\n' "$id">/run/agi-$p/driver;}
driver_check(){ p=$1;id=$2;[ -f /run/agi-$p/driver ]||return 0;cur=$(cat /run/agi-$p/driver);[ "$cur" = "$id" ]||{ echo "[refused] driver lock held by $cur" >&2;return 1;};}
case $cmd in
 arm) arm "$@";;
 drop) drop "$1";;
 status) echo "manned: $(tr '\n' ' ' <"$STATE")"; [ -f $CDIR/multiplex.pid ]&&echo "pid=$(cat $CDIR/multiplex.pid)"||echo "pid=none";;
 driver-lock) driver_lock "$1" "$2";;
 driver-check) driver_check "$1" "$2";;
 *) echo "usage: sm-dg-multiplex arm|drop|status|driver-lock|driver-check …" >&2;exit 2;;
esac
~~~
### g5348-joint-falsify (1735 B)
~~~sh
#!/bin/sh
# g5348-joint-falsify (g5.34.8.4): one run covering v6 bundle on one reproject.
# Retire interim watches AT LAND (Belam): /workspace/*watch* (aio mailwatch, alive-watch, tm-pane-monitor, SM weekday ping). Never git rm.
set -eu
fail=0
say(){ echo "$*";}
chk(){ if "$@";then say "OK: $*";else say "FAIL: $*";fail=1;fi;}
# 1 monitor piece exists once
chk sh -c 'n=$(sect monitor HEAD 2>/dev/null|wc -c); [ "$n" -gt 50 ]'
# 2 sm-dg-multiplex exists
chk sh -c 'n=$(sect sm-dg-multiplex HEAD 2>/dev/null|wc -c); [ "$n" -gt 50 ]'
# 3 K10 arming in agi-sync
chk sh -c 'git show HEAD:.agi/nodes/.geometry/engine-wrap.md | grep -q "monitor wait <post>"'
# 4 mail-wake no sleep>=5 SoT
chk sh -c '! git show HEAD:.agi/nodes/.geometry/engine-post.md | sed -n "/^### mail-wake /,/^### /p" | grep -E "while sleep [5-9]|while sleep [0-9]{2,}"'
# 5 agi-carry projected in agi-project
chk sh -c 'git show HEAD:.agi/nodes/.geometry/engine.md | grep -q "agi-carry@.path"'
# 6 interim watch retirement check (post-land): paths must be absent or inactive
# Pre-land: record expected retire list (never git rm from this seat)
RETIRE="/workspace/aio/mailwatch.sh /workspace/alive-watch.sh /workspace/tm-pane-monitor.sh"
say "RETIRE_AT_LAND: $RETIRE"
# 7 0 B to i across monitor/mail-wake
chk sh -c '! git show HEAD:.agi/nodes/.geometry/engine-post.md | sed -n "/^### monitor /,/^### /p" | grep -E "/run/agi-|>\\$i"'
chk sh -c '! git show HEAD:.agi/nodes/.geometry/engine-post.md | sed -n "/^### mail-wake /,/^### /p" | grep -E "/run/|>\\$i"'
# 8 exec bash == 1
chk sh -c 'c=$(git show HEAD:.agi/nodes/.geometry/engine-wrap.md | grep -c "exec bash"); [ "$c" = 1 ]'
[ "$fail" = 0 ] && say "JOINT FALSIFY PASS" || { say "JOINT FALSIFY FAIL"; exit 1; }
~~~
### mail-wake (1860 B)
~~~sh
#!/bin/sh
# mail-wake (g5.34.6.2 W1-W7 R8 + gate-e P2 W-A): ONE raw-shell watcher AFTER orient.
# SoT: tip-sha mk() + PathChanged/agi-carry ping (~/.mail-wake-ping). Poll ≤2s packed-refs fallback only.
# Notice tty/o only, 0 B to i. Enter/n/other = HOLD (W3/W4). V1: row grokbot else parent grokbot.
mk(){ git for-each-ref --format='%(refname) %(objectname)' "refs/box/*/$AGI_POST"|while read r s;do f=${r#refs/box/};f=${f%/*};[ "$s" = "$(git rev-parse -q --verify refs/held/$AGI_POST/$f)" ]||echo "$f $s";done;}
gb(){ git show ${AGI_TRUNK:-HEAD}:.agi/nodes/.geometry/posts.md|sed -n 's/^  - {/{/p'|jq -r --arg p "$1" 'select(.name==$p)|.grokbot//empty'|head -1;}
par(){ git show ${AGI_TRUNK:-HEAD}:.agi/nodes/.geometry/posts.md|sed -n 's/^  - {/{/p'|jq -r --arg p "$1" 'select(.name==$p)|.parent//empty'|head -1;}
wk(){ g=$(gb "$AGI_POST");[ -n "$g" ]||{ p=$(par "$AGI_POST");[ -n "$p" ]&&[ "$p" != owner ]&&[ "$p" != keep ]&&g=$(gb "$p");};if command -v agi-wake >/dev/null;then agi-wake "${g:--}" "$*";else echo "[unwired] wake grokbot=${g:--}: $*";fi;}
y(){ [ -s ~/.mail-pending ]||{ echo "box: no mail pending";return 1;};rm -f ~/.mail-pending;(cd ~/t&&box read);}
n(){ rm -f ~/.mail-pending;echo "box: held";};Y(){ y;};N(){ n;}
tick(){ pin 2>&1|while read -r l;do echo "$l";case $l in card-prompt*)wk "$l";;esac;done
 k=$(mk);[ -n "$k" ]&&[ "$k" != "$(cat ~/.mail-seen 2>/dev/null)" ]||return 0;printf '%s
' "$k">~/.mail-seen;printf '%s
' "$k">~/.mail-pending
 f=$(printf '%s
' "$k"|tail -n1|cut -d' ' -f1);printf '
box: mail from %s, read now? (y/N)
' "$f";wk "box: mail from $f for $AGI_POST tip $(printf '%s
' "$k"|tail -n1|cut -d' ' -f2)";}
[ "${1:-}" = watch ]&&{ cd ~/t||exit 1;touch ~/.mail-wake-ping
 while :;do tick;if command -v inotifywait >/dev/null;then inotifywait -qq -t 2 ~/.mail-wake-ping 2>/dev/null||true;else sleep 2;fi;done;}
~~~


### agi-rc (208 B)
~~~sh
# agi-rc (g5.34.7.2 + g5.34.6.2): bash --rcfile for raw-shell panes. Orient once per shell-start latch; y/Y read, n/N or Enter hold.
[ -n "$AGI_ORIENTED" ]||{ export AGI_ORIENTED=1;orient;}
. ~/bin/mail-wake
~~~

### pin (1434 B)
~~~sh
#!/bin/sh
# pin (g5.34.7.3 Path A): the driver writes ~/meter "<0..1> <epoch>" each turn (1.0 after summarization). Bound grokbot rows only (DG/DT: none).
# `pin` = check, prompt once per crossing; `pin rotate` = kill gate, refused unless card blob changed since prompt.
P=${AGI_POST:?};c=.agi/nodes/doc/card-$P.md;cd ~/t||exit 1
r=$(git show ${AGI_TRUNK:-HEAD}:.agi/nodes/.geometry/posts.md|sed -n 's/^  - {/{/p'|jq -r --arg p $P 'select(.name==$p and has("grokbot"))|.engine.rotate_pct//empty'|head -1);[ "$r" ]||exit 0
b=$(git rev-parse -q --verify HEAD:$c)
[ "${1:-}" = rotate ]&&{ [ "$b" ]&&[ "$b" != "$(cat ~/.pin-card 2>/dev/null)" ]||{ echo "[refused] rotate: card-$P unchanged since prompt; write it, git commit it";rm -f ~/.pin-crossed;exit 1;};rm -f ~/.pin-card ~/.pin-crossed;touch ~/.fresh;kill $PPID;exit 0;}
awk -v r=$r -v n=$(date +%s) '{f=$1;t=$2;k=NF} END{if(!NR||k!=2||f!~/^[0-9.]+$/||f+0>1||n-t>21600)exit 2;exit (f+0>=r/100)?0:1}' ~/meter 2>/dev/null;e=$?
[ $e = 2 ]&&{ [ -e ~/.pin-refused ]||{ touch ~/.pin-refused;echo "[refused] meter";};exit 2;};rm -f ~/.pin-refused
[ $e = 1 ]&&{ rm -f ~/.pin-crossed;exit 0;};[ -e ~/.pin-crossed ]&&exit 0;touch ~/.pin-crossed;echo "${b:-none}">~/.pin-card
echo "card-prompt $P meter=$(cut -d' ' -f1 ~/meter) rev=$(git rev-parse --short HEAD)"
echo "At the line: write your card, git commit it, then run: pin rotate   (= touch ~/.fresh;kill \$PPID, gated on the card blob)"
~~~

### season (2648 B)
~~~sh
#!/bin/sh
# season judge REPORT [--against PLAN] [--actor POST] [--session S]
# SoT: engine-post.md ### season -> /var/lib/agi/$P/bin/season (NOT extensions/agi/bin/season)
# exits 0 stamped+read-back lens non-empty · 1 [refused] · 2 usage
P=${AGI_POST:?}
T=${AGI_TRUNK:-HEAD}
refuse(){ echo "[refused] $*" >&2; exit 1; }
usage(){ echo "usage: season judge REPORT [--against PLAN] [--actor POST] [--session S]" >&2; exit 2; }
[ "$1" = judge ] || usage
shift
R=${1:?}; shift || true
A=; ACT=$P; SESS=
while [ $# -gt 0 ]; do
  case $1 in
    --against) A=${2:?}; shift 2;;
    --actor) ACT=${2:?}; shift 2;;
    --session) SESS=${2:?}; shift 2;;
    -h|--help) usage;;
    *) usage;;
  esac
done
[ "$ACT" = "$P" ] || refuse "actor $ACT != AGI_POST $P"
SEASON=$(git show "$T:.agi/nodes/.geometry/ladder.md" | sed -n "s/^current_season: //p" | head -1)
[ -n "$SEASON" ] || refuse "ladder current_season unreadable on $T"
RP=$(git grep -l --full-name "^id: ${R}$" "$T" -- .agi/nodes 2>/dev/null | head -1 | sed "s|^$T:||")
[ -n "$RP" ] || refuse "report $R not found on $T"
NODE=$(git show "$T:$RP")
TYPE=$(printf "%s\n" "$NODE" | sed -n "s/^type: //p" | head -1)
[ -n "$TYPE" ] || refuse "report $R has no type"
if [ -z "$A" ]; then
  A=$(printf "%s\n" "$NODE" | awk "/^parents:/{p=1;next} p&&/^  - /{gsub(/^  - /,\"\");print;exit} p&&/^[^ ]/{exit}")
  [ -n "$A" ] || refuse "no --against and no parents on $R"
fi
AP=$(git grep -l --full-name "^id: ${A}$" "$T" -- .agi/nodes 2>/dev/null | head -1 | sed "s|^$T:||")
[ -n "$AP" ] || refuse "against $A not found on $T"
LENS=$(git show "$T:$AP" | awk "/^parents:/{p=1;next} p&&/^  - /{gsub(/^  - /,\"\"); if(\$0~/^(goal|vision):/){print;exit}} p&&/^[^ ]/{exit}")
[ -n "$LENS" ] || refuse "empty lens — against $A has no goal/vision parent"
WARGS="--set judged_against=$A --set lens=$LENS --set season=$SEASON --actor $ACT"
[ -n "$SESS" ] && WARGS="$WARGS --session $SESS"
if command -v write.py >/dev/null 2>&1; then W=write.py
elif [ -x "${AGI_BIN:-/var/lib/agi/$P/bin}/write.py" ]; then W=${AGI_BIN:-/var/lib/agi/$P/bin}/write.py
else refuse "write.py not found"; fi
$W "$R" $WARGS || refuse "write failed for $R"
TIP=$(git rev-parse -q --verify HEAD 2>/dev/null || echo "$T")
RB=$(git show "$TIP:$RP" 2>/dev/null || git show "$T:$RP")
printf "%s\n" "$RB" | grep -q "^judged_against: ${A}$" || refuse "read-back judged_against mismatch"
printf "%s\n" "$RB" | grep -q "^lens: ${LENS}$" || refuse "read-back lens mismatch/empty"
printf "%s\n" "$RB" | grep -q "^season: ${SEASON}$" || refuse "read-back season mismatch"
echo "Judgment stamped on $R: judged_against=$A lens=$LENS season=$SEASON"
exit 0
~~~

<!-- THOUGHT:BEGIN — authored, not derived; carried across regenerating scans. The reasoning behind THIS version. -->
PROPOSED v5 (round 5, §Q): v4c's body pieces cut whole out of config:engine, byte for byte. SPLIT: agi-post@.service moved to engine-root (root reads it, a post does not).
<!-- THOUGHT:END -->
