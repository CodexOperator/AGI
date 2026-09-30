---
id: config:engine
mint_id: e228cdddac334a71b2764fb2fb26821b
type: config
parents:
  - goal:g7.16.1.11
next_edges: []
edited_by: belam
scaffold_hash: 1a5628596065214d
season: 2
town: core
---
# config:engine — the whole engine, one read
Depth 0 = diagram · 1 = loop + pieces, one line each · 2 = one piece: `sect <name>` · 3 = this file. Every piece is a small template over raw commands; its parameters are cells. Reasoning: doc:radically-simple-engine.

## diagram — depth 0
~~~
              GRAPH = git @trunk: nodes · .agi/n/<mint> real files · addresses + parents = symlinks
   boot ──▶ agi-seed ──▶ agi-project (read FROM this node) ──▶ BODY: users · units · settings · keys
   BODY ──▶ post unit ──▶ harness start|resume|compact ──▶ agi-brief: b = walk(card + claims)
   session ──▶ plain paths in its OWN checkout ──turn end──▶ one signed commit on its own ref
   post refs ──▶ the master merges ──▶ trunk moves ──▶ agi-project re-runs ──▶ next brief sees it
   tick: project(graph) == observe(body)?  equal = alive · differ = heal + a drift commit
   frontier: each active goal runs its falsifier ──▶ met | red | mute ──▶ the pool; claim = one CAS
   gates at every landing: the projection is non-empty and reproduces itself · V = red + mute never
   rises without a new owner goal · every at-REV read follows the links (git cat-file --follow-symlinks)
~~~

## loop — depth 1
~~~
1 BOOT   agi-seed extracts agi-project from this node @trunk; it projects the body from the graph
2 START  a post's unit starts its harness; start, resume and compact all run agi-brief first
3 WORK   the agent reads and writes plain paths in ~/t; every turn end = one signed commit on its ref
4 LAND   the master merges post refs; the gates refuse an empty or non-reproducing projection, or V up
5 TICK   tick.sh heals drift and commits it; agi-frontier calls every unmet goal into the pool
~~~

## pieces — depth 1, one line each (bytes on disk)
~~~
agi-post@.service    340 B  a post IS one unit instance: its uid, its checkout ~/t, its key, the harness under strace; a restart is a rotation
agi-inbox@.path       37 B  mail wakes a post: a change in its drop box ...
agi-inbox@.service    69 B  ... types "mail" into its session
settings.json        458 B  the harness wiring every post gets: the meter (rotate at the line), the brief at every start, one commit at every turn end
agi.ts               372 B  the same wiring for pi: the brief in the system prompt on every turn, one commit at every turn end
agi-brief            722 B  what a session sees first: the walk from its card + its own claims; the vector, then whole nodes by |b|
brief.py             562 B  b = a sum((1-a) P_theta)^k e: the complex walk over parent symlinks; |b| = how near, phase = how far up
gitconfig             79 B  every commit is signed by the post's own key
agi-flush            125 B  on exit: commit, merge, push: a dying session loses nothing
pre-receive          355 B  a push may touch only paths whose owner group the pusher is in
signers               65 B  allowed_signers = the posts' public keys
sysusers.conf         34 B  a post = one user in one group
project.sh           282 B  what the body SHOULD be, read from the graph
observe.sh           317 B  what the body IS, read from the box
tick.sh              221 B  the homeostat: diff them; heal what drifted and commit the wound
simhash.awk          241 B  stage-0 latent sense: near-duplicate and misfiled prose, no package
agi-project          982 B  the genome: units for every post row, read from this node @REV; its own unit re-reads it
agi-seed.service     383 B  the ONE installed unit: at boot, run agi-project from this node @trunk
agi-frontier         632 B  the hunger: every active goal runs its falsifier: met | red | mute
sect                  257 B  the narrowed read: ONE section or piece of this node, byte-exact, at any REV
~~~

## files — depth 2, each whole; extract: sect <name> [REV]

### agi-post@.service (340 B)
~~~ini
[Service]
User=agi-%i
WorkingDirectory=%h/t
EnvironmentFile=%h/env
ExecStartPre=-sh -c 'ssh-keygen -qN "" -ted25519 -f%h/.ssh/id_ed25519<&-;cp %h/.ssh/id_ed25519.pub .agi/keys/%i'
ExecStart=dtach -N %t/agi-%i strace -qqfe%%file -o%h/r sh -c '${H} go'
ExecStopPost=agi-flush
Restart=always
MemoryHigh=4G
[Install]
WantedBy=multi-user.target
~~~

### agi-inbox@.path (37 B)
~~~ini
[Path]
PathChanged=/var/spool/agi/%i
~~~

### agi-inbox@.service (69 B)
~~~ini
[Service]
User=agi-%i
ExecStart=sh -c 'echo mail|dtach -p %t/agi-%i'
~~~

### settings.json (458 B)
~~~json
{"hooks":{"UserPromptSubmit":[{"hooks":[{"type":"command","command":"jq -r .transcript_path|xargs tail -1|jq -e '.message.usage|.input_tokens+.cache_read_input_tokens+.cache_creation_input_tokens>470000'>/dev/null&&echo 'At the line: write your card, git commit it, then run: kill $PPID'"}]}],"SessionStart":[{"hooks":[{"type":"command","command":"agi-brief"}]}],"Stop":[{"hooks":[{"type":"command","command":"cd ~/t;git add -A;git commit -qm$USER||:"}]}]}}
~~~

### agi.ts (372 B)
~~~ts
import{execSync as x}from"node:child_process";let b="";const c=()=>{try{x("cd ~/t;git add -A;git commit -qm$USER",{stdio:"ignore"})}catch{}}
export default(pi:any)=>{pi.on("session_start",()=>{try{b=x("agi-brief",{encoding:"utf8"})}catch{}})
pi.on("before_agent_start",(e:any)=>b?{systemPrompt:e.systemPrompt+"\n\n"+b}:undefined);pi.on("turn_end",c);pi.on("agent_end",c)}
~~~

### agi-brief (722 B)
~~~sh
#!/bin/sh
# agi-brief: b = the walk from e (the card + this post's own claims); the vector, then whole nodes by |b| up to B bytes. Every harness start runs it.
p=${AGI_POST:-${USER#agi-}};cd "${AGI_ROOT:-$HOME/t}/.agi"||exit 0;c=$(readlink -f nodes/doc/card-$p.md)||exit 0;c=${c%/node.md}
e=${c##*/}$(git for-each-ref refs/claims --format='%(authorname) %(refname:lstrip=2)'|sed -n "s/^agi-$p /,/p"|tr -d '\n')
python3 ${BRIEF:-brief.py} n $e ${K:-20}|while read a f m;do echo "$a $f $(sed -n '/^id:/{s/^id: *//p;q}' n/$m/node.md) .agi/n/$m/node.md";done>~/.brief
echo "# brief: $p (|b| · levels up · address · path)";cat ~/.brief;cut -d' ' -f4 ~/.brief|sed 's|^.agi/||'|xargs tail -n+1 2>/dev/null|head -c ${B:-40000}
~~~

### brief.py (562 B)
~~~py
import os,sys,cmath
R,S,k=sys.argv[1],sys.argv[2].split(','),int(sys.argv[3]);q=cmath.exp(.5j)
A={}
for m in os.listdir(R):
 for p in os.listdir(f'{R}/{m}/p'):
  t=os.readlink(f'{R}/{m}/p/{p}')[6:]
  if os.path.isdir(f'{R}/{t}'):A.setdefault(m,[]).append((t,q));A.setdefault(t,[]).append((m,1/q))
x={s:1/len(S) for s in S}
for _ in range(30):
 y={s:.15/len(S) for s in S}
 for u,v in x.items():
  for w,z in A.get(u,()):y[w]=y.get(w,0)+.85*v*z/len(A[u])
 x=y
for m in sorted(x,key=lambda m:-abs(x[m]))[:k]:print(f'{abs(x[m]):.3f} {cmath.phase(x[m])/.5:+.1f}',m)
~~~

### gitconfig (79 B)
~~~ini
[gpg]
format=ssh
[commit]
gpgsign=true
[user]
signingkey=~/.ssh/id_ed25519.pub
~~~

### agi-flush (125 B)
~~~sh
#!/bin/sh
cd ~/t;grep -o '"/[^"]*"' ~/r|sort -u>~/track;git add -A;git commit -qSm$USER;git pull -q --no-rebase&&git push -q
~~~

### pre-receive (355 B)
~~~sh
#!/bin/sh
e=$(git hash-object -t tree /dev/null)
while read o n r;do case $n in *[!0]*);;*)continue;;esac;case $o in *[!0]*);;*)o=$(git merge-base HEAD $n 2>/dev/null||echo $e);;esac
f=$(git diff --name-only $o $n)||exit 1;for p in $f;do g=$(git check-attr --source=$n owner -- "$p"|cut -d' ' -f3);id -nG|grep -qw "$g"||{ echo "$p: $g";exit 1;};done;done
~~~

### signers (65 B)
~~~sh
#!/bin/sh
for f in .agi/keys/*;do echo "${f##*/} $(cat $f)";done
~~~

### sysusers.conf (34 B)
~~~ini
u agi-alive -
m agi-alive council
~~~

### project.sh (282 B)
~~~sh
#!/bin/sh
r(){ echo "$1:$2"|git cat-file --batch --follow-symlinks|{ read o t s;[ "$t" = blob ]&&head -c $s;};}
r HEAD .agi/nodes/.geometry/posts.md|grep -o '"name": "[^"]*"'|cut -d'"' -f4|sort -u|while read p;do printf 'user agi-%s\nunit agi-post@%s\nbrief agi-%s\n' $p $p $p;done
~~~

### observe.sh (317 B)
~~~sh
#!/bin/sh
getent passwd|cut -d: -f1|grep '^agi-'|sed 's/^/user /'
systemctl list-units --plain --no-legend 'agi-post@*'|cut -d' ' -f1|sed 's/\.service$//;s/^/unit /'
getent passwd|awk -F: '/^agi-/{print $1,$6}'|while read u h;do jq -e .hooks.SessionStart $h/.claude/settings.json>/dev/null 2>&1&&echo "brief $u";done
~~~

### tick.sh (221 B)
~~~sh
#!/bin/sh
cd ~/t;sh project.sh|sort>~/p;sh observe.sh|sort>~/o;diff ~/p ~/o>.agi/drift/$USER&&exit
grep '^< unit' .agi/drift/$USER|cut -d' ' -f3|xargs -rn1 systemctl start;git add .agi/drift;git commit -qSm"drift: $USER"
~~~

### simhash.awk (241 B)
~~~awk
BEGIN{for(i=32;i<127;i++)o[sprintf("%c",i)]=i}
{for(w=1;w<NF;w++){s=$w" "$(w+1);h=0;for(c=1;c<=length(s);c++)h=(h*31+o[substr(s,c,1)])%4294967291;for(b=0;b<32;b++)v[b]+=int(h/2^b)%2?1:-1}}
END{for(b=0;b<32;b++)x=x (v[b]>0);print x,FILENAME}
~~~

### agi-project (982 B)
~~~sh
#!/bin/sh
# agi-project OUT REV: this box's units = f(graph@REV); every piece is read FROM the engine node through the links, so no copy can drift
o=$1 r=$2 w=$1/default.target.wants;g(){ echo "$r:.agi/nodes/.geometry/$1"|git cat-file --batch --follow-symlinks;};mkdir -p $w
g engine.md|sed -n '/^### agi-post@.service /,/^### /{/^~~~/,/^~~~/{//!p}}'>$o/agi-post@.service
for p in $(g posts.md|sed -n 's/^  - {/{/p'|jq -r "select(.box==\"${AGI_BOX:-local-town}\" and .recover!=false).name//empty");do ln -sf ../agi-post@.service $w/agi-post@$p.service;done
printf '[Service]\nType=oneshot\nWorkingDirectory=%s\nExecStart=sh -c "echo %s:.agi/nodes/.geometry/engine.md|git cat-file --batch --follow-symlinks|sed -n \047/^### agi-project /,/^### /{/^~~~/,/^~~~/{//!p}}\047|sh -s %s %s;systemctl --user daemon-reload"\n' $PWD $r $o $r>$o/agi-project.service
printf '[Path]\nPathChanged=%s\n' $(git rev-parse --absolute-git-dir)/logs/$r>$o/agi-project.path;ln -sf ../agi-project.path $w
~~~

### agi-seed.service (383 B)
~~~ini
[Unit]
RequiresMountsFor=/data/work/agi
[Service]
Type=oneshot
WorkingDirectory=/data/work/agi
ExecStart=sh -c "echo trunk:.agi/nodes/.geometry/engine.md|git cat-file --batch --follow-symlinks|sed -n '/^### agi-project /,/^### /{/^~~~/,/^~~~/{//!p}}'|sh -s %t/systemd/user trunk;systemctl --user daemon-reload;systemctl --user start default.target"
[Install]
WantedBy=default.target
~~~

### agi-frontier (632 B)
~~~sh
#!/bin/sh
# agi-frontier REV: every active goal (by TYPE, over real files, so any layout) runs its first read-only falsifier; exit 0 = met ([goal].md), else it CALLS OUT: mute | red
r=$1;git grep --all-match -l -e '^type: goal$' -e '^status: active$' $r -- .agi|while IFS=: read _ f;do n=$(git show $r:$f);g=$(echo "$n"|sed -n 's/^id: goal://p')
c=$(echo "$n"|sed -n '/^## Falsifier/,/^## Out/p'|grep -o '`[^`]*`'|tr -d '`'|grep -Em1 '^(grep|test|ls|getent|git (log|show|grep|rev-parse|ls-files|diff|for-each-ref)) ')
[ "$c" ]||{ echo mute $g;continue;};timeout 30 sh -c "$c"</dev/null>/dev/null 2>&1&&echo met $g||echo red $g;done
~~~

### sect (257 B)
~~~sh
#!/bin/sh
# sect NAME [REV]: ONE section or piece of the engine node, byte-exact, at any REV, through the links (F.7)
echo "${2:-HEAD}:.agi/nodes/.geometry/engine.md"|git cat-file --batch --follow-symlinks|sed -n "/^###* $1 /,/^###* /{/^~~~/,/^~~~/{//!p}}"
~~~
