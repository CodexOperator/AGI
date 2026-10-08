---
id: doc:g716111-stage25-engine-v4c
mint_id: 2bf7135b37264d14b7f6b5b37e167803
type: doc
parents:
  - goal:g7.16.1.11
next_edges: []
edited_by: director-general-3
scaffold_hash: 1aa85202b02c1f05
season: 2
tags:
  - doc
  - engine
  - g7.16.1.11
  - stage-2.5
title: "g7.16.1.11 stage 2.5 engine v4c bytes (16,384 B): DG5 on Claude Code + Remote Control, one pi-free kid on CCCC; C1 writes it into config:engine"
town: core
---
# doc:g716111-stage25-engine-v4c

The stage 2.5 engine, v4c (goal:g7.16.1.11; PHASE A' of doc:g716111-stage25-rootplan): 16,384 B whole (cap 16,384), sha256 prefix fb6d18ba066414bc. Assembled by an Opus 5.5 subagent of director-general-3 from 24 pieces (no root, nothing installed). It is the value act C1 (a Prime landing) writes into config:engine; it is NOT live until then. Extract a piece: `sect <name>` once landed; until then, from the fence below, byte-exact.

~~~~~markdown
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
Depth 0 = diagram · 1 = loop + pieces · 2 = one piece: `sect <name>` · 3 = this file. Pieces are small templates over raw commands; parameters are cells: a row's ONE `engine` object is projected as AGI_<KEY> env. Parity: doc:g716111-stage25-parity.

## diagram — depth 0
~~~
   GRAPH = git @trunk: .agi/nodes, edges = parents: · a post opts in by ONE row cell "engine": {"v": 4, ...}
   root, once ──▶ agi-project (FROM this node @REV) ──▶ BODY: user · unit in agi.slice · env cells
   unit ──▶ own uid · worktree ~/t of MAIN on posts/<p> · pane = fifo i + typescript o (script) · strace
   start|resume|compact ──CC hooks, or pi via cccc.ts──▶ agi-brief: walk(card+seeds+claims) + STARTUP
   prompt ──▶ agi-meter: at the line: card, .fresh, kill ──▶ Restart = a FRESH successor
   turn end ──▶ agi-turn: one signed commit · agi-link · released agi-wt trees dropped · mail = a turn
   stop ──▶ agi-flush ──▶ the master lands posts/<p> ──▶ agi-project re-runs ──▶ next brief sees it
   harness: claude --remote-control <p> (hooks native; the owner's app lists it) · pi + cccc.ts · agi-kid
   tick: project(graph) == observe(body)? equal = alive · differ = start it + a drift commit
~~~

## loop — depth 1
~~~
1 BOOT   root runs agi-project @REV: unit, user, cells for engine.v==4 rows; dropped rows unlinked
2 START  PSI admission; key, worktree, tools from this node; .fresh = new session, else -c resumes
3 WORK   brief in the system prompt; plain paths in ~/t; inbox, budget, records resolve to MAIN
4 TURN   one signed commit; agi-link; at the line: card, touch ~/.fresh, kill $PPID = rotation
5 LAND   ExecStopPost agi-flush; the master gates posts/<p> onto the trunk (skill agi-master-gate)
~~~

## pieces — depth 1, one line each (bytes on disk)
~~~
agi-post@.service 1252 B  a post = one unit in agi.slice: own uid, tree, key, pane
agi-run            357 B  pane cmd: .fresh or -c, under strace; claude: mail -> i
settings.json      272 B  the ONE hook wiring: brief, meter, turn commit
cccc.ts           1647 B  pi events -> those CC hooks; inbox growth -> a turn
agi-kid            390 B  a pi-free kid in this unit: own HOME, tree, cccc.ts
agi-brief          938 B  walk card+seeds+claims; record; STARTUP
brief.py           810 B  the complex walk over parents: edges
agi-meter          439 B  past rotate_pct of the window: the out-line
agi-turn           269 B  drop released trees; signed commit; agi-link
agi-link           358 B  node <-> code file via payload_ref
agi-wt             688 B  a node's tiny RAM tree: pull; drop = commit+purge
agi-track           89 B  strace sink: each path once
agi-flush          181 B  on exit: drop trees, commit, merge trunk
gitconfig          180 B  signed commits, signers, own hooks
signers             65 B  allowed_signers = the posts' keys
sysusers.conf       41 B  a post = one user in group agi
agi.rules          211 B  group agi may start agi-post@ units
project.sh         161 B  what the body SHOULD be
observe.sh         255 B  what the body IS
tick.sh            254 B  diff them; start the drift; commit
agi-project       1679 B  the genome: units + cells for v4 rows
agi-frontier       460 B  each active goal runs its falsifier
agi-gate           276 B  refuse a tip whose body would not regrow
sect               149 B  ONE piece of this node, byte-exact, any REV
~~~

## files — depth 2, each whole; extract: sect <name> [REV]

### agi-post@.service (1252 B)
~~~ini
[Unit]
After=agi-ram-main.service
[Service]
User=agi-%i
StateDirectory=agi/%i
WorkingDirectory=/var/lib/agi/%i
EnvironmentFile=-/var/lib/agi/%i.env
Environment=PATH=/var/lib/agi/%i/bin:/opt/agi/bin:/usr/local/bin:/usr/bin:/bin SHELL=/bin/sh DISABLE_AUTOUPDATER=1 AGI_SEAT=%i
RuntimeDirectory=agi-%i
ExecStartPre=awk -F"[= ]" "/some/{exit $$3>40}" /proc/pressure/memory
ExecStartPre=sh -c 'mkdir -p .ssh bin .claude hooks;git config --global safe.directory "*";[ -f .ssh/id_ed25519 ]||ssh-keygen -qN "" -ted25519 -f.ssh/id_ed25519;[ -d t ]||{ git -C $O branch posts/%i $AGI_TRUNK;git -C $O worktree add -fq $PWD/t posts/%i;touch .fresh;};e=t/.agi/nodes/.geometry/engine.md;for x in $(grep -o "^### [^ ]*" $e|cut -c5-);do sed -n "/^### $x /,/^### /{/^~~~/,/^~~~/{//!p}}" $e>bin/$x;done;chmod +x bin/*;mv bin/gitconfig .gitconfig;mv bin/settings.json .claude;mkdir -p t/.agi/keys;cp .ssh/id_ed25519.pub t/.agi/keys/%i;mkfifo -m600 %t/agi-%i/i;[ -e o ]||install -m600 /dev/null o;cd t;signers>../.signers'
ExecStart=sh -c 'exec 3<>%t/agi-%i/i;exec script -qfO$HOME/o -c agi-run <&3'
StandardOutput=null
ExecStopPost=sh -c agi-flush
SuccessExitStatus=1 SIGTERM
Restart=always
RestartSec=30
Slice=agi.slice
MemoryHigh=4G
[Install]
WantedBy=multi-user.target
~~~

### agi-run (357 B)
~~~sh
#!/bin/sh
cd ~/t;c=-c;[ -e ~/.fresh ]&&rm ~/.fresh&&c=;stty cols 200 rows 50;i=$RUNTIME_DIRECTORY/i;f=$O/.agi/sessions/inbox/$AGI_SEAT.md
case $H in claude*)(s=$(stat -c%s $f);while sleep 5;do n=$(stat -c%s $f);[ $n -gt $s ]&&printf "mail: send.py read $AGI_SEAT">$i&&sleep 1&&printf '\r'>$i;s=$n;done)&;;esac
exec strace -qqfe%file -o'|agi-track' $H $c go
~~~

### settings.json (272 B)
~~~json
{"skipDangerousModePermissionPrompt":true,"hooks":{"SessionStart":[{"hooks":[{"type":"command","command":"agi-brief","timeout":180}]}],"UserPromptSubmit":[{"hooks":[{"type":"command","command":"agi-meter"}]}],"Stop":[{"hooks":[{"type":"command","command":"agi-turn"}]}]}}
~~~

### cccc.ts (1647 B)
~~~ts
import{execSync as x}from"node:child_process";import{readFileSync as R,watchFile as W,unwatchFile as U}from"node:fs"
const E=process.env,H=JSON.parse(R(E.HOME+"/.claude/settings.json","utf8")).hooks,N={bash:"Bash",read:"Read",edit:"Edit",write:"Write"};let b=""
const h=(n,j={})=>{let o="",k=0;for(const g of H[n]||[])if(!g.matcher||RegExp(g.matcher).test(j.tool_name))for(const c of g.hooks)try{o+=x(c.command,{input:JSON.stringify({hook_event_name:n,cwd:process.cwd(),...j}),encoding:"utf8",stdio:"pipe",timeout:(c.timeout||60)*1e3})}catch(e){if(e.status==2)k=2,o+=e.stderr}return{o,k}}
const t=e=>({tool_name:N[e.toolName]||e.toolName,tool_input:e.input}),S=s=>{b=h("SessionStart",{source:s}).o}
export default p=>{const on=(e,f)=>p.on(e,f);on("session_start",e=>{S({new:"clear",fork:"resume",reload:"resume"}[e.reason]||e.reason)
const f=`${E.O}/.agi/sessions/inbox/${E.AGI_SEAT}.md`;U(f);W(f,{interval:5e3,persistent:!1},(n,o)=>n.size>o.size&&p.sendUserMessage("mail: send.py read "+E.AGI_SEAT,{deliverAs:"followUp"}))})
on("session_compact",()=>S("compact"));on("before_agent_start",e=>b&&{systemPrompt:e.systemPrompt+"\n\n"+b})
on("input",(e,c)=>{const u=c.getContextUsage()||{},r=h("UserPromptSubmit",{prompt:e.text,tokens:u.tokens,context_window:u.contextWindow});return r.k?{action:"handled"}:r.o&&{action:"transform",text:e.text+"\n\n"+r.o}})
on("tool_call",e=>{const r=h("PreToolUse",t(e));return r.k&&{block:true,reason:r.o}});on("tool_result",e=>{h("PostToolUse",t(e))})
on("session_before_compact",()=>{h("PreCompact",{trigger:"auto"})});on("turn_end",()=>{h("Stop")});on("session_shutdown",()=>{h("SessionEnd",{reason:"other"})})}
~~~

### agi-kid (390 B)
~~~sh
#!/bin/sh
k=$1;shift;h=~/k/$k;mkdir -p $h/.claude;cd ~/t;[ -d $h/t ]||git worktree add -q $h/t -b kids/$k
for x in .gitconfig .ssh .signers hooks .claude/settings.json;do ln -sfn ~/$x $h/$x;done
cd $h/t;HOME=$h AGI_SEAT=$k AGI_ROLE=kid AGI_HARNESS=pi-free AGI_WT=$RUNTIME_DIRECTORY/k-$k exec pi --provider openrouter --model $AGI_KID_MODEL --skill skills -e ~/bin/cccc.ts -p "$*"</dev/null
~~~

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

### agi-project (1679 B)
~~~sh
#!/bin/sh
o=$1 r=$2 w=$1/multi-user.target.wants;g(){ echo "$r:.agi/nodes/.geometry/$1"|git cat-file --batch --follow-symlinks|{ read a t s;[ "$t" = blob ]&&head -c $s;};};s(){ g engine.md|sed -n "/^### $1 /,/^### /{/^~~~/,/^~~~/{//!p}}";}
mkdir -p $w;rm -f $w/agi-post@*;s agi-post@.service>$o/agi-post@.service;:>$o/agi-users.conf
g posts.md|sed -n 's/^  - {/{/p'|jq -r --arg b ${AGI_BOX:-local-town} 'select(.box==$b and .engine.v==4)|.+.engine|[.name,if .harness|test("^pi") then "pi --provider openrouter --model \(.model) --thinking \(.effort) --skill skills -e ../bin/cccc.ts" else "claude --remote-control \(.name) --model \(.model) --effort \(.effort) --permission-mode bypassPermissions" end,([.engine|to_entries[]|"\"AGI_\(.key|ascii_upcase)=\(.value)\""]+["AGI_ROLE=\(.role)","AGI_LADDER_TIER=\(.tier)"]|join(" "))]|@tsv'|while IFS='	' read p h e;do ln -s ../agi-post@.service $w/agi-post@$p.service;mkdir -p $o/agi-post@$p.service.d;printf '[Service]\nEnvironment="H=%s" O=%s %s\n' "$h" "$(git rev-parse --show-toplevel)" "$e">$o/agi-post@$p.service.d/h.conf;s sysusers.conf|sed s/@/$p/g>>$o/agi-users.conf;done
printf '[Service]\nType=oneshot\nWorkingDirectory=%s\nExecStart=sh -c "echo %s:.agi/nodes/.geometry/engine.md|git cat-file --batch --follow-symlinks|sed -n \047/^### agi-project /,/^### /{/^~~~/,/^~~~/{//!p}}\047|sh -s %s %s&&ls %s/multi-user.target.wants/agi-post@*>/dev/null&&systemctl daemon-reload&&systemd-sysusers %s/agi-users.conf"\n' $PWD $r $o $r $o $o>$o/agi-project.service
printf '[Path]\nPathChanged=%s/logs/%s\n' $(git rev-parse --absolute-git-dir) $(git rev-parse --symbolic-full-name $r)>$o/agi-project.path;ln -sf ../agi-project.path $w
~~~

### agi-frontier (460 B)
~~~sh
#!/bin/sh
r=$1;git grep --all-match -l -e '^type: goal$' -e '^status: active$' $r -- .agi|while IFS=: read _ f;do n=$(git show $r:$f);g=$(echo "$n"|sed -n 's/^id: goal://p')
c=$(echo "$n"|sed -n '/^## Falsifier/,/^## Out/p'|grep -o '`[^`]*`'|tr -d '`'|grep -Em1 '^(grep|test|ls|getent|git (log|show|grep|rev-parse|ls-files|diff|for-each-ref)) ')
[ "$c" ]||{ echo mute $g;continue;};timeout 30 sh -c "$c"</dev/null>/dev/null 2>&1&&echo met $g||echo red $g;done
~~~

### agi-gate (276 B)
~~~sh
#!/bin/sh
o=$(mktemp -d);sect agi-project $1|sh -s $o $1&&ls $o/multi-user.target.wants/agi-post@*>/dev/null||{ rm -rf $o;exit 1;}
mv $o $o.1;sh -c "$(sed -n 's/^ExecStart=sh -c "\(.*\)&&systemctl.*/\1/p' $o.1/agi-project.service)";diff -r $o.1 $o;r=$?;rm -rf $o $o.1;exit $r
~~~

### sect (149 B)
~~~sh
#!/bin/sh
echo "${2:-HEAD}:.agi/nodes/.geometry/engine.md"|git cat-file --batch --follow-symlinks|sed -n "/^###* $1 /,/^###* /{/^~~~/,/^~~~/{//!p}}"
~~~

<!-- THOUGHT:BEGIN — authored, not derived; carried across regenerating scans. The reasoning behind THIS version. -->
PROPOSED v4c, NOT MINTED (owner 04:40Z/04:49Z): claude rows run --remote-control <post> (app-visible); the owner logs in as the post user. agi-kid: ONE pi-free kid via cccc.ts, -p exits. claude panes get mail typed into i. F14 tick.sh spares ~/o. agi-seed.service waits for stage 3 (v4b).
<!-- THOUGHT:END -->
~~~~~
