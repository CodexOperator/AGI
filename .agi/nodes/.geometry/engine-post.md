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

### agi-meter (439 B)
~~~sh
#!/bin/sh
j=$(cat);t=$(echo "$j"|jq '.tokens//empty');[ "$t" ]||t=$(echo "$j"|jq -r .transcript_path|xargs tail -1 2>/dev/null|jq '.message.usage|.input_tokens+.cache_read_input_tokens+.cache_creation_input_tokens');w=$(echo "$j"|jq ".context_window//${AGI_WINDOW:-1000000}")
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
drop)git diff --quiet $(cat $d/.b) -- $P||{ echo "moved $2";exit 4;};tar -cC $d --exclude=.b .|tar -x;git add $P;git commit -qm"$USER: $2">/dev/null||:;rm -rf $d;;esac
~~~

### agi-track (89 B)
~~~sh
#!/bin/sh
grep --line-buffered -o '"/[^"]*"'|awk '!s[$0]++{print;fflush()}'>>$HOME/track
~~~

### agi-flush (181 B)
~~~sh
#!/bin/sh
cd ~/t;for d in ${AGI_WT:-$RUNTIME_DIRECTORY/wt}/*/;do [ -d $d ]&&agi-wt drop $(basename $d);done;agi-turn;git merge -q --no-edit ${AGI_TRUNK:-trunk}||git merge --abort;:
~~~

### gitconfig (180 B)
~~~ini
[gpg]
format=ssh
[gpg "ssh"]
allowedSignersFile=~/.signers
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

### signers (65 B)
~~~sh
#!/bin/sh
for f in .agi/keys/*;do echo "${f##*/} $(cat $f)";done
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

<!-- THOUGHT:BEGIN — authored, not derived; carried across regenerating scans. The reasoning behind THIS version. -->
PROPOSED v5 (round 5, §Q): v4c's body pieces cut whole out of config:engine, byte for byte. SPLIT: agi-post@.service moved to engine-root (root reads it, a post does not).
<!-- THOUGHT:END -->
