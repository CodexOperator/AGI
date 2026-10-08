---
id: doc:g716111-round5-build
mint_id: 4ec4c05d7fbb40e3b016140d721f78c7
type: doc
parents:
  - goal:g7.16.1.11
next_edges: []
edited_by: director-general-3
scaffold_hash: 752111283cdfaa35
season: 2
tags:
  - doc
  - engine
  - round-5
  - g7.16.1.11
title: "g7.16.1.11 ROUND 5 build: config:engine bootstrap 7,324 B + engine-post 8,079 + engine-wrap 4,253 (byte-exact bodies), 35/35 tests; lands after the live parity re-measure"
town: core
---
# doc:g716111-round5-build

ROUND 5 of goal:g7.16.1.11 (owner GO 06:1xZ, goal @24ba05f43: §Q + the two §R folds + agi-infer; land as config:engine bootstrap <= 8,192 + engine-post + engine-wrap; belam verifies + lands C1-style). Built by an Opus 5.5 subagent of director-general-3, no root, nothing landed; tests re-run by DG3: test.sh rc 0, 35 PASS 0 FAIL. NOT READY TO LAND until DG5 is live (Phase C): the parity rows below are re-measured on the live post first.

| node | bytes | holds |
|---|---|---|
| config:engine (bootstrap) | 7,324 / 8,192 | diagram, loop (v4c bytes), the map of all 25 pieces, agi-project, agi-gate, sect, THOUGHT |
| config:engine-post | 8,079 | agi-post@.service + 16 moved v4c pieces |
| config:engine-wrap | 4,253 | agi-run, settings.json, cccc.ts, agi-kid, agi-infer (549 B) |
| total | 19,656 | under the 20,480 cap |

Moved pieces 20/20 byte-exact vs v4c. The 4 changed readers (sect 149->214, agi-project 1,679->1,841, agi-post@.service 1,252->1,266, agi-gate 276->404) are one-shot asserted string replacements of v4c (build/readers.py), each tested. §R folds: the gate alone refuses an empty unit template (rc 1; v4c passes it); piece ranges end at ^## (controls show the old ^### end bleeding).

## Picks where §Q/§R leave it open
1. --full-tree in sect and s() (+12 B each): the doc text finds 0 engine nodes from a subdirectory. 2. sed s|^|$r:| (branch names carry /). 3. the gate's duplicate check uses the :/ pathspec. 4. the empty-unit check in BOTH agi-project (exit 3) and the gate (27 B redundancy). 5. **OPEN, for belam: the gate passes (rc 0) with engine-wrap.md MISSING** -- one gate line checking every map name resolves (+77 B, bootstrap ~7,401) refuses it rc 1; measured, NOT built (outside the GO); DG3 recommends folding it. 6. agi-project.service ExecStart left as v4c bytes. 7. expansion nodes: parents goal:g7.16.1.11 + config:engine; mint_id/scaffold_hash minted by write.py at landing.

## Live parity re-measure (after Phase C; <c> = the post, <v5> = the landed commit)
F36 bin from 3 nodes: before landing cp -a /var/lib/agi/<c>/bin /tmp/bin.v4c; after restart diff -rq -> only sect, agi-project, agi-gate, agi-post@.service + agi-infer · row 1 projector s(): sect agi-project <v5> | sh -s /tmp/x <v5>; ls /tmp/x/multi-user.target.wants · 2 systemctl is-active agi-post@<c> · 3 drop the cell, re-run agi-project: the link goes · 4 systemctl show -p Environment agi-post@<c> | grep -c -- --model = 1 · 6 jq -c .hooks on the post's settings.json · 19 git -C <post tree> verify-commit HEAD rc 0 · 23 agi-gate <v5> rc 0 on the live tip · 35 systemctl kill agi-post@<c>: active again, bin identical · 36 systemctl show -p Slice,MemoryHigh agi-post@<c> · F37 agi-infer against a live local endpoint.

## out/engine.md (7324 B, sha256 5b3660ddd11c7265), byte-exact
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
# config:engine — the ZYGOTE: the code that runs before any post exists + the map of all 25 pieces
Depth 0 = diagram · 1 = loop + pieces · 2 = one piece: `sect <name>` (any `.geometry/engine*.md`: this node, config:engine-post, config:engine-wrap) · 3 = this file. Pieces are small templates over raw commands; parameters are cells: a row's ONE `engine` object is projected as AGI_<KEY> env. Parity: doc:g716111-stage25-parity.

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
   ZYGOTE = this read (map · sect · agi-project · agi-gate) ──sect @REV──▶ EXPANSION: config:engine-post · config:engine-wrap
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
agi-post@.service 1266 B  a post = one unit in agi.slice: own uid, tree, key, pane
agi-run            357 B  pane cmd: .fresh or -c, under strace; claude: mail -> i
settings.json      272 B  the ONE hook wiring: brief, meter, turn commit
cccc.ts           1647 B  pi events -> those CC hooks; inbox growth -> a turn
agi-kid            390 B  a pi-free kid in this unit: own HOME, tree, cccc.ts
agi-infer          549 B  ONE chat call, OpenAI-compatible: stdin -> stdout
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
agi-project       1841 B  the genome: units + cells for v4 rows
agi-frontier       460 B  each active goal runs its falsifier
agi-gate           404 B  refuse a tip whose body would not regrow; one name, one piece
sect               214 B  ONE piece of any engine*.md node, byte-exact, any REV
~~~

## files — depth 2, each whole; extract: sect <name> [REV]

### agi-project (1841 B)
~~~sh
#!/bin/sh
o=$1 r=$2 w=$1/multi-user.target.wants;g(){ echo "$r:.agi/nodes/.geometry/$1"|git cat-file --batch --follow-symlinks|{ read a t s;[ "$t" = blob ]&&head -c $s;};};s(){ git ls-tree --full-tree --name-only $r .agi/nodes/.geometry/|grep '/engine[^/]*\.md$'|sed "s|^|$r:|"|git cat-file --batch --follow-symlinks|sed -n "/^### $1 /,/^##/{/^~~~/,/^~~~/{//!p}}";}
mkdir -p $w;rm -f $w/agi-post@*;s agi-post@.service>$o/agi-post@.service;[ -s $o/agi-post@.service ]||exit 3;:>$o/agi-users.conf
g posts.md|sed -n 's/^  - {/{/p'|jq -r --arg b ${AGI_BOX:-local-town} 'select(.box==$b and .engine.v==4)|.+.engine|[.name,if .harness|test("^pi") then "pi --provider openrouter --model \(.model) --thinking \(.effort) --skill skills -e ../bin/cccc.ts" else "claude --remote-control \(.name) --model \(.model) --effort \(.effort) --permission-mode bypassPermissions" end,([.engine|to_entries[]|"\"AGI_\(.key|ascii_upcase)=\(.value)\""]+["AGI_ROLE=\(.role)","AGI_LADDER_TIER=\(.tier)"]|join(" "))]|@tsv'|while IFS='	' read p h e;do ln -s ../agi-post@.service $w/agi-post@$p.service;mkdir -p $o/agi-post@$p.service.d;printf '[Service]\nEnvironment="H=%s" O=%s %s\n' "$h" "$(git rev-parse --show-toplevel)" "$e">$o/agi-post@$p.service.d/h.conf;s sysusers.conf|sed s/@/$p/g>>$o/agi-users.conf;done
printf '[Service]\nType=oneshot\nWorkingDirectory=%s\nExecStart=sh -c "echo %s:.agi/nodes/.geometry/engine.md|git cat-file --batch --follow-symlinks|sed -n \047/^### agi-project /,/^### /{/^~~~/,/^~~~/{//!p}}\047|sh -s %s %s&&ls %s/multi-user.target.wants/agi-post@*>/dev/null&&systemctl daemon-reload&&systemd-sysusers %s/agi-users.conf"\n' $PWD $r $o $r $o $o>$o/agi-project.service
printf '[Path]\nPathChanged=%s/logs/%s\n' $(git rev-parse --absolute-git-dir) $(git rev-parse --symbolic-full-name $r)>$o/agi-project.path;ln -sf ../agi-project.path $w
~~~

### agi-gate (404 B)
~~~sh
#!/bin/sh
git grep -ho "^### [^ ]*" $1 -- ":/.agi/nodes/.geometry/engine*.md"|sort|uniq -d|grep -q .&&exit 2
o=$(mktemp -d);sect agi-project $1|sh -s $o $1&&[ -s $o/agi-post@.service ]&&ls $o/multi-user.target.wants/agi-post@*>/dev/null||{ rm -rf $o;exit 1;}
mv $o $o.1;sh -c "$(sed -n 's/^ExecStart=sh -c "\(.*\)&&systemctl.*/\1/p' $o.1/agi-project.service)";diff -r $o.1 $o;r=$?;rm -rf $o $o.1;exit $r
~~~

### sect (214 B)
~~~sh
#!/bin/sh
r=${2:-HEAD};git ls-tree --full-tree --name-only $r .agi/nodes/.geometry/|grep '/engine[^/]*\.md$'|sed "s|^|$r:|"|git cat-file --batch --follow-symlinks|sed -n "/^###* $1 /,/^###* /{/^~~~/,/^~~~/{//!p}}"
~~~

[THOUGHT of the proposed node, markers dropped in this doc (one THOUGHT per node, test_thought_hygiene); the landed node carries them]
PROPOSED v5, NOT MINTED (owner GO 06:1xZ; doc:radically-simple-engine §Q + §R folds): v4c cut by one rule, ZYGOTE = what runs before any post exists + the map; the body (config:engine-post) and the wrappers (config:engine-wrap, + agi-infer) are EXPANSION read by sect @REV. Only the 4 readers changed (sect, agi-project, agi-gate, agi-post@.service): every .geometry/engine*.md at the REV, ranges end at ^##; the gate refuses a duplicate name (2) and an empty unit template (1). Every other piece = v4c bytes.
[end of that THOUGHT]
~~~~~

## out/engine-post.md (8079 B, sha256 4bc40cc3220c110a), byte-exact
~~~~~markdown
---
id: config:engine-post
type: config
parents:
  - goal:g7.16.1.11
  - config:engine
next_edges: []
edited_by: belam
season: 2
town: core
---
# config:engine-post — EXPANSION of config:engine: the post body (unit, brief, meter, turn, links, trees, tick, frontier)
Read only through `sect <name> [REV]` and the unit's extraction loop (both read every `.geometry/engine*.md` at one REV); the map of every piece is config:engine's pieces table.

## files — depth 2, each whole; extract: sect <name> [REV]

### agi-post@.service (1266 B)
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
ExecStartPre=sh -c 'mkdir -p .ssh bin .claude hooks;git config --global safe.directory "*";[ -f .ssh/id_ed25519 ]||ssh-keygen -qN "" -ted25519 -f.ssh/id_ed25519;[ -d t ]||{ git -C $O branch posts/%i $AGI_TRUNK;git -C $O worktree add -fq $PWD/t posts/%i;touch .fresh;};for e in t/.agi/nodes/.geometry/engine*.md;do for x in $(grep -o "^### [^ ]*" $e|cut -c5-);do sed -n "/^### $x /,/^##/{/^~~~/,/^~~~/{//!p}}" $e>bin/$x;done;done;chmod +x bin/*;mv bin/gitconfig .gitconfig;mv bin/settings.json .claude;mkdir -p t/.agi/keys;cp .ssh/id_ed25519.pub t/.agi/keys/%i;mkfifo -m600 %t/agi-%i/i;[ -e o ]||install -m600 /dev/null o;cd t;signers>../.signers'
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

[THOUGHT of the proposed node, markers dropped in this doc (one THOUGHT per node, test_thought_hygiene); the landed node carries them]
PROPOSED v5 (round 5, §Q): v4c's body pieces cut whole out of config:engine, byte for byte; agi-post@.service is the one changed (its extraction loop reads every engine*.md, ranges end at ^##).
[end of that THOUGHT]
~~~~~

## out/engine-wrap.md (4253 B, sha256 7c5d9096b8e047e2), byte-exact
~~~~~markdown
---
id: config:engine-wrap
type: config
parents:
  - goal:g7.16.1.11
  - config:engine
next_edges: []
edited_by: belam
season: 2
town: core
---
# config:engine-wrap — EXPANSION of config:engine: the post wrappers (pane command, hook wiring, pi bridge, the kid, raw inference)
Read only through `sect <name> [REV]` and the unit's extraction loop (both read every `.geometry/engine*.md` at one REV); the map of every piece is config:engine's pieces table.

## files — depth 2, each whole; extract: sect <name> [REV]

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

### agi-infer (549 B)
~~~sh
#!/bin/sh
# agi-infer [MODEL] <prompt: ONE call to any OpenAI-compatible /v1/chat/completions; cells infer_url, infer_model, infer_key (the NAME of a var in the unit's EnvironmentFile)
h=$(mktemp);trap 'rm -f $h' 0;[ "$AGI_INFER_KEY" ]&&printf 'Authorization: Bearer %s\n' "$(printenv $AGI_INFER_KEY)">$h
jq -Rsc --arg m "${1:-$AGI_INFER_MODEL}" '{model:$m,messages:[{role:"user",content:.}]}'|curl -sf -H @$h -H 'Content-Type: application/json' -d @- ${AGI_INFER_URL:-http://127.0.0.1:8080/v1}/chat/completions|jq -er '.choices[0].message.content'
~~~

[THOUGHT of the proposed node, markers dropped in this doc (one THOUGHT per node, test_thought_hygiene); the landed node carries them]
PROPOSED v5 (round 5, §Q): v4c's wrapper pieces cut whole, byte for byte, + agi-infer (owner 05:50Z, b60af0b63): one OpenAI-compatible chat call; cells infer_url/infer_model/infer_key (a var NAME, never a key).
[end of that THOUGHT]
~~~~~

<!-- THOUGHT:BEGIN — authored, not derived; carried across regenerating scans. The reasoning behind THIS version. -->
PROPOSED v5 build record for round 5 (doc:radically-simple-engine §Q + §R folds), carrying the proposed config:engine / engine-post / engine-wrap bodies in ~~~~~ fences. This version (DG3 10:4xZ 10-01, SM trunk red test_thought_hygiene): the embedded nodes THOUGHT markers are dropped to plain labels so this doc holds ONE THOUGHT; the landed nodes carry their own (land package doc:g716111-land-package).
<!-- THOUGHT:END -->
