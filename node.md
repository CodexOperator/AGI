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
   agi-gate at every trunk landing: the projection is non-empty and reproduces itself · V = red + mute
   is published, not gated (no owner-seed cell yet) · every at-REV read follows the links (cat-file)
~~~

## loop — depth 1
~~~
1 BOOT   agi-seed extracts agi-project from this node @trunk; it projects the body from the graph
2 START  a post's unit starts its harness; start, resume and compact all run agi-brief first (CC: the vector)
3 WORK   the agent reads and writes plain paths in ~/t; every turn end = one signed commit on its ref
4 LAND   the master merges post refs; agi-gate refuses a tip whose body would not regrow
5 TICK   tick.sh starts what drifted (polkit: group agi) and commits it; agi-frontier calls every unmet goal into the pool
~~~

## pieces — depth 1, one line each (bytes on disk)
~~~
agi-post@.service    468 B  a post IS one unit instance: its uid, its checkout ~/t, its key, the harness under strace; a restart is a rotation
agi-inbox@.path       37 B  mail wakes a post: a change in its drop box ...
agi-inbox@.service    71 B  ... types "mail" into its session
settings.json        467 B  the harness wiring every post gets: the meter (rotate at the line), the brief at every start, one commit at every turn end
agi.ts               377 B  the same wiring for pi: the brief in the system prompt on every turn, one commit at every turn end
agi-brief            575 B  what a session sees first: the walk from its card + its own claims; the vector, then whole nodes by |b|
brief.py             603 B  b = a sum((1-a) P_theta)^k e: the complex walk over parent symlinks; |b| = how near, phase = how far up
gitconfig             99 B  every commit is signed by the post's own key
agi-flush            183 B  on exit: commit, merge, push: a dying session loses nothing
pre-receive          435 B  a push may touch only paths whose owner group the pusher is in
signers               65 B  allowed_signers = the posts' public keys
sysusers.conf         51 B  a post = one user in one group
agi.rules            211 B  the ONE root-owned piece: group agi may start agi-post@ units, so tick heals with no root act
project.sh           282 B  what the body SHOULD be, read from the graph
observe.sh           332 B  what the body IS, read from the box
tick.sh              250 B  the homeostat: diff them; heal what drifted and commit the wound
simhash.awk          241 B  stage-0 latent sense: near-duplicate and misfiled prose, no package
agi-project          941 B  the genome: units for every post row, read from this node @REV; its own unit re-reads it
agi-seed.service     447 B  the ONE installed unit: at boot, run agi-project from this node @trunk
agi-frontier         460 B  the hunger: every active goal runs its falsifier: met | red | mute
agi-gate             273 B  the trunk gate (pre-receive): refuse a tip whose body would not regrow
sect                 149 B  the narrowed read: ONE section or piece of this node, byte-exact, at any REV
~~~

## files — depth 2, each whole; extract: sect <name> [REV]

### agi-post@.service (468 B)
~~~ini
[Service]
User=agi-%i
WorkingDirectory=/var/lib/agi/%i/t
EnvironmentFile=/var/lib/agi/%i/env
RuntimeDirectory=agi-%i
ExecStartPre=sh -c 'mkdir -p $HOME/.ssh .agi/keys;[ -f $HOME/.ssh/id_ed25519 ]||ssh-keygen -qN "" -ted25519 -f$HOME/.ssh/id_ed25519;cp $HOME/.ssh/id_ed25519.pub .agi/keys/%i'
ExecStart=dtach -N %t/agi-%i/s sh -c 'exec strace -qqfe%%file -o$HOME/r ${H} go'
ExecStopPost=sh -c agi-flush
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

### agi-inbox@.service (71 B)
~~~ini
[Service]
User=agi-%i
ExecStart=sh -c 'echo mail|dtach -p %t/agi-%i/s'
~~~

### settings.json (467 B)
~~~json
{"hooks":{"UserPromptSubmit":[{"hooks":[{"type":"command","command":"jq -r .transcript_path|xargs tail -1|jq -e '.message.usage|.input_tokens+.cache_read_input_tokens+.cache_creation_input_tokens>470000'>/dev/null&&echo 'At the line: write your card, git commit it, then run: kill $PPID'"}]}],"SessionStart":[{"hooks":[{"type":"command","command":"B=0 agi-brief"}]}],"Stop":[{"hooks":[{"type":"command","command":"cd ~/t;git add -A .agi;git commit -qm$USER||:"}]}]}}
~~~

### agi.ts (377 B)
~~~ts
import{execSync as x}from"node:child_process";let b="";const c=()=>{try{x("cd ~/t;git add -A .agi;git commit -qm$USER",{stdio:"ignore"})}catch{}}
export default(pi:any)=>{pi.on("session_start",()=>{try{b=x("agi-brief",{encoding:"utf8"})}catch{}})
pi.on("before_agent_start",(e:any)=>b?{systemPrompt:e.systemPrompt+"\n\n"+b}:undefined);pi.on("turn_end",c);pi.on("agent_end",c)}
~~~

### agi-brief (575 B)
~~~sh
#!/bin/sh
p=${AGI_POST:-${USER#agi-}};cd "${AGI_ROOT:-$HOME/t}/.agi"||exit 0;c=$(readlink -f nodes/doc/card-$p.md)||exit 0;c=${c%/node.md}
e=${c##*/}$(find "$(git config remote.origin.url)/refs/claims" -type f -user agi-$p ! -name '*.lock' -printf ',%f' 2>/dev/null)
sect brief.py|python3 - n $e ${K:-20}|while read a f m;do echo "$a $f $(sed -n '/^id:/{s/^id: *//p;q}' n/$m/node.md) .agi/n/$m/node.md";done>~/.brief
echo "# brief: $p (|b| · levels up · address · path)";cat ~/.brief;cut -d' ' -f4 ~/.brief|sed 's|^.agi/||'|xargs tail -n+1 2>/dev/null|head -c ${B:-40000}
~~~

### brief.py (603 B)
~~~py
import os,sys,cmath
R,S,k=sys.argv[1],sys.argv[2].split(','),int(sys.argv[3]);q=cmath.exp(.5j)
A={}
for m in os.listdir(R):
 for p in (os.listdir(f'{R}/{m}/p') if os.path.isdir(f'{R}/{m}/p') else ()):
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

### gitconfig (99 B)
~~~ini
[gpg]
format=ssh
[commit]
gpgsign=true
[user]
signingkey=~/.ssh/id_ed25519.pub
[safe]
	directory=*
~~~

### agi-flush (183 B)
~~~sh
#!/bin/sh
cd ~/t;grep -o '"/[^"]*"' ~/r|sort -u>~/track;git add -A .agi;git commit -qm$USER;git pull -q --no-rebase origin trunk&&git push -q origin HEAD:refs/posts/${USER#agi-}/head
~~~

### pre-receive (435 B)
~~~sh
#!/bin/sh
e=$(git hash-object -t tree /dev/null)
while read o n r;do case $n in *[!0]*);;*)continue;;esac;[ $r = refs/heads/trunk ]&&{ agi-gate $n||{ echo "gate: $n";exit 1;};continue;};case $o in *[!0]*);;*)o=$(git merge-base HEAD $n 2>/dev/null||echo $e);;esac
f=$(git diff --name-only $o $n)||exit 1;for p in $f;do g=$(git check-attr --source=$n owner -- "$p"|cut -d' ' -f3);id -nG|grep -qw "$g"||{ echo "$p: $g";exit 1;};done;done
~~~

### signers (65 B)
~~~sh
#!/bin/sh
for f in .agi/keys/*;do echo "${f##*/} $(cat $f)";done
~~~

### sysusers.conf (51 B)
~~~ini
u agi-alive - - /var/lib/agi/alive
m agi-alive agi
~~~

### agi.rules (211 B)
~~~js
polkit.addRule(function(a,s){if(a.id=="org.freedesktop.systemd1.manage-units"&&a.lookup("verb")=="start"&&/^agi-post@[a-z0-9-]+\.service$/.test(a.lookup("unit"))&&s.isInGroup("agi"))return polkit.Result.YES;});
~~~

### project.sh (282 B)
~~~sh
#!/bin/sh
r(){ echo "$1:$2"|git cat-file --batch --follow-symlinks|{ read o t s;[ "$t" = blob ]&&head -c $s;};}
r HEAD .agi/nodes/.geometry/posts.md|grep -o '"name": "[^"]*"'|cut -d'"' -f4|sort -u|while read p;do printf 'user agi-%s\nunit agi-post@%s\nbrief agi-%s\n' $p $p $p;done
~~~

### observe.sh (332 B)
~~~sh
#!/bin/sh
getent passwd|cut -d: -f1|grep '^agi-'|sed 's/^/user /'
systemctl list-units --state=active --plain --no-legend 'agi-post@*'|cut -d' ' -f1|sed 's/\.service$//;s/^/unit /'
getent passwd|awk -F: '/^agi-/{print $1,$6}'|while read u h;do jq -e .hooks.SessionStart $h/.claude/settings.json>/dev/null 2>&1&&echo "brief $u";done
~~~

### tick.sh (250 B)
~~~sh
#!/bin/sh
cd ~/t;mkdir -p .agi/drift;sect project.sh|sh|sort>~/p;sect observe.sh|sh|sort>~/o;diff ~/p ~/o>.agi/drift/$USER&&exit
grep '^< unit' .agi/drift/$USER|cut -d' ' -f3|xargs -rn1 systemctl start;git add .agi/drift;git commit -qm"drift: $USER"
~~~

### simhash.awk (241 B)
~~~awk
BEGIN{for(i=32;i<127;i++)o[sprintf("%c",i)]=i}
{for(w=1;w<NF;w++){s=$w" "$(w+1);h=0;for(c=1;c<=length(s);c++)h=(h*31+o[substr(s,c,1)])%4294967291;for(b=0;b<32;b++)v[b]+=int(h/2^b)%2?1:-1}}
END{for(b=0;b<32;b++)x=x (v[b]>0);print x,FILENAME}
~~~

### agi-project (941 B)
~~~sh
#!/bin/sh
o=$1 r=$2 w=$1/default.target.wants;g(){ echo "$r:.agi/nodes/.geometry/$1"|git cat-file --batch --follow-symlinks|{ read a t s;[ "$t" = blob ]&&head -c $s;};};mkdir -p $w
g engine.md|sed -n '/^### agi-post@.service /,/^### /{/^~~~/,/^~~~/{//!p}}'>$o/agi-post@.service
for p in $(g posts.md|sed -n 's/^  - {/{/p'|jq -r "select(.box==\"${AGI_BOX:-local-town}\" and .recover!=false).name//empty");do ln -sf ../agi-post@.service $w/agi-post@$p.service;done
printf '[Service]\nType=oneshot\nWorkingDirectory=%s\nExecStart=sh -c "echo %s:.agi/nodes/.geometry/engine.md|git cat-file --batch --follow-symlinks|sed -n \047/^### agi-project /,/^### /{/^~~~/,/^~~~/{//!p}}\047|sh -s %s %s&&ls %s/default.target.wants/agi-post@*>/dev/null&&systemctl --user daemon-reload"\n' $PWD $r $o $r $o>$o/agi-project.service
printf '[Path]\nPathChanged=%s\n' $(git rev-parse --absolute-git-dir)/logs/$r>$o/agi-project.path;ln -sf ../agi-project.path $w
~~~

### agi-seed.service (447 B)
~~~ini
[Unit]
RequiresMountsFor=/data/work/agi
[Service]
Type=oneshot
WorkingDirectory=/data/work/agi
ExecStart=sh -c "echo trunk:.agi/nodes/.geometry/engine.md|git cat-file --batch --follow-symlinks|sed -n '/^### agi-project /,/^### /{/^~~~/,/^~~~/{//!p}}'|sh -s %t/systemd/user trunk&&ls %t/systemd/user/default.target.wants/agi-post@*>/dev/null&&systemctl --user daemon-reload&&systemctl --user start default.target"
[Install]
WantedBy=default.target
~~~

### agi-frontier (460 B)
~~~sh
#!/bin/sh
r=$1;git grep --all-match -l -e '^type: goal$' -e '^status: active$' $r -- .agi|while IFS=: read _ f;do n=$(git show $r:$f);g=$(echo "$n"|sed -n 's/^id: goal://p')
c=$(echo "$n"|sed -n '/^## Falsifier/,/^## Out/p'|grep -o '`[^`]*`'|tr -d '`'|grep -Em1 '^(grep|test|ls|getent|git (log|show|grep|rev-parse|ls-files|diff|for-each-ref)) ')
[ "$c" ]||{ echo mute $g;continue;};timeout 30 sh -c "$c"</dev/null>/dev/null 2>&1&&echo met $g||echo red $g;done
~~~

### agi-gate (273 B)
~~~sh
#!/bin/sh
o=$(mktemp -d);sect agi-project $1|sh -s $o $1&&ls $o/default.target.wants/agi-post@*>/dev/null||{ rm -rf $o;exit 1;}
mv $o $o.1;sh -c "$(sed -n 's/^ExecStart=sh -c "\(.*\)&&systemctl.*/\1/p' $o.1/agi-project.service)";diff -r $o.1 $o;r=$?;rm -rf $o $o.1;exit $r
~~~

### sect (149 B)
~~~sh
#!/bin/sh
echo "${2:-HEAD}:.agi/nodes/.geometry/engine.md"|git cat-file --batch --follow-symlinks|sed -n "/^###* $1 /,/^###* /{/^~~~/,/^~~~/{//!p}}"
~~~

<!-- THOUGHT:BEGIN — authored, not derived; carried across regenerating scans. The reasoning behind THIS version. -->
belam gen 22, 00:48Z 10-01 (date -u): v2 = doc:radically-simple-engine §I @f37e25ced2 (11,900 B, 22 pieces): the spike's S1-S12 + S14 folded, the 2 KB Claude Code hook cap met (SessionStart carries only the vector), heal = ONE root-owned piece (agi.rules, a 214 B polkit rule: group agi may start agi-post@<name> and nothing else), F9 built as agi-gate (272 B), F10 and F11 dropped by name. Re-run on throwaway users passed F1 F9 F18 F19 P1 S2-S4 S6 F22, $0. belam verified: body == §I, 22/22 pieces byte-exact from the committed node, box clean (0 agi- users, no polkit rule, no sysusers, dtach removed; the 2 agi-* units on disk are the older memguard + ram-main). DESIGN STATE until the owner's build go.
<!-- THOUGHT:END -->
