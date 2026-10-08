---
id: doc:g716111-round7-build
mint_id: 86a814af44ae4c8ea00b7c8211bc6422
type: doc
parents:
  - goal:g7.16.1.11
next_edges: []
edited_by: director-general-3
scaffold_hash: 37bb3b4ccfc2296c
season: 2
tags:
  - doc
  - engine
  - round-7
  - g7.16.1.11
title: "g7.16.1.11 ROUND 7 build (§Y1-§Y3 + lookahead-free tags cell + corrective diagram): pieces cmp-equal, 0/23,180 regex disagreements; total 31-33 KB OVER the 20,480 cap (ruling needed); Y1/Y2 seam bug + agi-captive leak fixed in the build"
town: core
---
# doc:g716111-round7-build

ROUND 7 of goal:g7.16.1.11 (council §Y1-§Y3, released by belam 07:4xZ: 975ee0fdc · 2536d7ff3 · f725a8899; the doc moved during the build, pinned to a280bdfba) + the [goal]/[hypothesis] tags item_regex cell lookahead-free (§Y3) + the owner's ADD 07:3xZ: a refused row prints a CORRECTIVE DIAGRAM on the fly. Built by a Sonnet 5.5 subagent of director-general-3 ON the Round 5 split + Round 6's ### matrix; no root, nothing landed; DG3 re-ran t-seam.sh + t-captive.sh (rc 0). Off-graph: /tmp/agi-round7/ (test.txt 470 lines, the test scripts, out-doc/ = the doc-exact set).

## CAP: does NOT fit 20,480 B -- a RULING is needed
| node | R5 | R7 build | doc-exact |
|---|---|---|---|
| config:engine (bootstrap) | 7,324 | 7,903 (cap 8,192: headroom 289) | 7,903 |
| config:engine-post | 8,079 | 8,079 | 8,079 |
| config:engine-wrap | 4,253 | 11,682 | 9,928 |
| config:engine-grow (NEW) | - | 5,105 | 5,105 |
| total | 19,656 | 32,769 | 31,015 |
Recommend: the cap counts the bootstrap + ONE post's read set (or a raised cap).

## Pieces vs the doc (cmp)
grow-check 1,298 · grow-gate 1,435 (the doc's §Y1 line now says 1,435, not 842) · grow-project 1,185 · agi-fill 5,004 · agi-captive 311 -- all IDENTICAL to the doc; the growth matrix 7,111 B / 151 rows equals the doc's, schema hash hypothesis@35ddbda8c73f equals. Build deltas: agi-fill 5,973 (+969 = the corrective diagram + 19 B seam fix) · agi-captive.patched 576 · agi-infer 829 (R5 549 + the fence copy; the doc said ~60 B, it is +280) · settings.json +70 (doc +61).

## The tags item_regex cell (lookahead-free)
before (37 B): (?!parked:)[^\n]*|parked:g\d+(\.\d+)* -- after (150 B, doc said 156): |[^p\n][^\n]*|p([^a\n][^\n]*)?|pa([^r\n][^\n]*)?|par([^k\n][^\n]*)?|park([^e\n][^\n]*)?|parke([^d\n][^\n]*)?|parked([^:\n][^\n]*)?|parked:g\d+(\.\d+)* -- no (?. EQUIVALENT: 23,180 strings (38 hand samples, 521 live tag values, every string <= 4 chars over 12 chars), 0 disagreements under python re, jq/Oniguruma, node RegExp and grep -E; live gate verdicts 5,181 pass / 241 refuse before AND after (0 moved). Not run: the 25/25 llama fence probe (no llama-cli on this box; a proxy reproduces the doc's 15/18/20/25).

## Corrective diagram (one source: the window's JSON Schema; on a refused call, a refused row and agi-fill check)
~~~~~text
refused (try 1 of 3) : 2 wrong
 << testable_claim  got (missing)
     expected string
 << tags.1  got "parked:xx"
     expected string /|[^p\n][^\n]*|p([^a\n][^\n]*)?|pa([^r\n][^\n]*)?|par([^k\n][^\n]*)?|park([^e\n][..
SHAPE {"title": <string>, "testable_claim": <string>}

$ agi-fill row "status: sleeping"
refused row : 1 wrong
 << status  got "sleeping"
     expected one of active | horizon | retired | phasing-out | complete
next: title ({"description": "str"})
~~~~~

## Tests (test.txt): Y1 T1-T11 as the doc (+T12-T14) · grow-check vs the old check_spawn 5,400/5,400 agree (gawk + mawk) · grow-gate as pre-receive G1-G8 + Ya-Yi as the doc + a window-written node lands · the fill window: good accepted, refused prints the diagram, shorthands / row mode / 3 tries / timeout / order / clash · window-written nodes pass grow-check + agi-fill check · agi-gate rc 0, agi-project identical to R5 · post bin 25 -> 31 files.

## Holes (doc kept; build carries the fixes)
1. **Y1/Y2 SEAM, real bug:** Y1's variant column goal_kind=subgoal goes straight into const -> a legal goal or build is refused FOREVER: no goal/build can be written through the window. Fix v.rpartition('=')[2] (test.txt §11).
2. **agi-captive leaks:** any line starting agi-fill passes, so agi-fill close; cat FILE, a newline chain, $(..) and an unquoted heredoc get through; the patched copy refuses them (a quoted heredoc stays the way to send text).
3. doc byte counts off: settings.json 70 not 61 · tags cell 150 not 156 · agi-infer fence +280 not ~60 (new cell infer_schema).
4. grow-project takes the aliases file as argv[2] with no named home (growth-aliases.tsv beside the matrix); a schema-only or matrix-only push lands unguarded (the doc names it).
5. cosmetic: agi-fill with no subcommand prints a traceback; check through grow-gate shows the temp name n.

## What lands where (no root)
belam: config:engine, config:engine-wrap, config:engine-grow (new) from out/ · the tags cell into .agi/context/schemas/[goal].md and [hypothesis].md (line 37 / line 23) · growth.tsv + growth-aliases.tsv into .agi/nodes/.geometry/ · grow-gate wired as the hub's pre-receive.

## Bytes (the landing set, byte-exact)
### out/engine.md (7903 B, sha256 73a80da4a721fab6)
~~~~~
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
# config:engine — the ZYGOTE: the code that runs before any post exists + the map of all 30 pieces
Depth 0 = diagram · 1 = loop + pieces · 2 = one piece: `sect <name>` (any `.geometry/engine*.md`: this node, config:engine-post, config:engine-wrap, config:engine-grow) · 3 = this file. Pieces are small templates over raw commands; parameters are cells: a row's ONE `engine` object is projected as AGI_<KEY> env. Parity: doc:g716111-stage25-parity.

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
   ZYGOTE = this read (map · sect · agi-project · agi-gate) ──sect @REV──▶ EXPANSION: config:engine-post · config:engine-wrap · config:engine-grow
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
settings.json      342 B  the ONE hook wiring: brief, meter, turn commit
cccc.ts           1647 B  pi events -> those CC hooks; inbox growth -> a turn
agi-kid            390 B  a pi-free kid in this unit: own HOME, tree, cccc.ts
agi-infer          829 B  ONE chat call, OpenAI-compatible: stdin -> stdout
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
agi-fill          5973 B  a node key opens a captive fill window
agi-captive        576 B  window open: only agi-fill passes
grow-check        1298 B  one node vs its matrix row + key
grow-gate         1435 B  pre-receive: added/changed nodes must pass
grow-project      1185 B  schemas -> the growth matrix
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

### matrix (100 B)
~~~
boot	matrix	engine	sect
boot	body	posts	agi-project
post	bin	engine*	sect
post	brief	card-<p>	brief
~~~

[THOUGHT of the proposed node, markers dropped in this doc (one THOUGHT per node, test_thought_hygiene); the landed node carries them]
PROPOSED v5, NOT MINTED (owner GO 06:1xZ; doc:radically-simple-engine §Q + §R folds): v4c cut by one rule, ZYGOTE = what runs before any post exists + the map; the body (config:engine-post) and the wrappers (config:engine-wrap, + agi-infer) are EXPANSION read by sect @REV. Only the 4 readers changed (sect, agi-project, agi-gate, agi-post@.service): every .geometry/engine*.md at the REV, ranges end at ^##; the gate refuses a duplicate name (2) and an empty unit template (1). Every other piece = v4c bytes. ROUND 7: + `### matrix` (round 6) + 5 map lines + engine-grow in the diagram; zygote code unchanged.
[end of that THOUGHT]
~~~~~
### out/engine-wrap.md (11682 B, sha256 7ed3ba87999a9f17)
~~~~~
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
# config:engine-wrap — EXPANSION of config:engine: the post wrappers (pane command, hook wiring, pi bridge, the kid, raw inference, the captive fill window)
Read only through `sect <name> [REV]` and the unit's extraction loop (both read every `.geometry/engine*.md` at one REV); the map of every piece is config:engine's pieces table.

## files — depth 2, each whole; extract: sect <name> [REV]

### agi-run (357 B)
~~~sh
#!/bin/sh
cd ~/t;c=-c;[ -e ~/.fresh ]&&rm ~/.fresh&&c=;stty cols 200 rows 50;i=$RUNTIME_DIRECTORY/i;f=$O/.agi/sessions/inbox/$AGI_SEAT.md
case $H in claude*)(s=$(stat -c%s $f);while sleep 5;do n=$(stat -c%s $f);[ $n -gt $s ]&&printf "mail: send.py read $AGI_SEAT">$i&&sleep 1&&printf '\r'>$i;s=$n;done)&;;esac
exec strace -qqfe%file -o'|agi-track' $H $c go
~~~

### settings.json (342 B)
~~~json
{"skipDangerousModePermissionPrompt":true,"hooks":{"PreToolUse":[{"hooks":[{"type":"command","command":"agi-captive"}]}],"SessionStart":[{"hooks":[{"type":"command","command":"agi-brief","timeout":180}]}],"UserPromptSubmit":[{"hooks":[{"type":"command","command":"agi-meter"}]}],"Stop":[{"hooks":[{"type":"command","command":"agi-turn"}]}]}}
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

### agi-infer (829 B)
~~~sh
#!/bin/sh
# agi-infer [MODEL] <prompt: ONE call to any OpenAI-compatible /v1/chat/completions; cells infer_url, infer_model, infer_key (the NAME of a var in the unit's EnvironmentFile), infer_schema (a JSON Schema FILE: the reply is fenced to it, closed)
h=$(mktemp);trap 'rm -f $h' 0;[ "$AGI_INFER_KEY" ]&&printf 'Authorization: Bearer %s\n' "$(printenv $AGI_INFER_KEY)">$h
s=$([ "$AGI_INFER_SCHEMA" ]&&jq -c '.+{additionalProperties:false}' $AGI_INFER_SCHEMA)
jq -Rsc --arg m "${1:-$AGI_INFER_MODEL}" --argjson s "${s:-null}" '{model:$m,messages:[{role:"user",content:.}]}+if $s then {response_format:{type:"json_schema",json_schema:{name:"fill",schema:$s}}} else {} end'|curl -sf -H @$h -H 'Content-Type: application/json' -d @- ${AGI_INFER_URL:-http://127.0.0.1:8080/v1}/chat/completions|jq -er '.choices[0].message.content'
~~~

### agi-fill (5973 B)
~~~python
#!/usr/bin/env python3
# agi-fill open NID PARENT.. | call <TOOLCALL | row <"field: value".. | close -- the captive fill window a node key opens (§Y2): format FIRST, one tool call or row by row, closes on write, abort, timeout or N tries
import sys,os,re,json,time,uuid,subprocess as S,yaml,jsonschema
A=sys.argv;E=os.environ.get;W=os.path.expanduser(E('AGI_FILL','~/.fill'));L=int(E('AGI_FILL_WINDOW','900'));N=int(E('AGI_FILL_TRIES','3'))
a=lambda r:re.sub(r'^\^|(?<!\\)\$$','',r).replace('\\d','[0-9]')
X={'id','type','mint_id','parents','next_edges','key','schema','scaffold_hash'};J={'str':'string','int':'integer','float':'number','bool':'boolean','dict':'object','list':'array'}
def sch(c,v):
 p=f'.agi/context/schemas/[{c}].md';d=yaml.safe_load(open(p).read().split('\n---',1)[0][4:]);V=d.get('validation')or{};T=V.get('types')or{};F=d.get('fields')or{};P={}
 for k in [*F,*V.get('required',[])]:
  if k in X or k in P:continue
  f=F.get(k);t=T.get(k);s={'type':J.get(t,'string')}if t else{'description':str((f.get('type')if isinstance(f,dict)else f)or'str')}
  if k in(V.get('regex')or{}):s={'type':'string','pattern':f"^(?:{a(V['regex'][k])})$"}
  if k in(V.get('item_regex')or{}):s['items']={'type':'string','pattern':f"^(?:{a(V['item_regex'][k])})$"}
  P[k]=s
 k=(d.get('spawn')or{}).get('discriminator')
 if k and v!='-':P[k]={'const':v}
 P['body']={'type':'string'};return c+'@'+S.run(['git','hash-object',p],capture_output=True,text=True).stdout[:12],{'type':'object','properties':P,'required':[k for k in V.get('required',[])if k not in X],'additionalProperties':True}
def sh(s):
 p=s.get('pattern','')[4:-2];q=s.get('items')
 return 'list of '+sh(q) if q else '= '+json.dumps(s['const']) if 'const' in s else 'one of '+p.strip('()').replace('|',' | ') if re.fullmatch(r'\(?[\w.-]+(\|[\w.-]+)+\)?',p) else 'string /'+p[:60]+('..'if p[60:]else'')+'/' if p else s.get('type')or s.get('description','str')
def dia(j,E,t):
 Q=j['properties'];print('refused',t,':',len(E),'wrong')
 for e in E:
  r=e.validator=='required';P=list(e.path);f=e.message.split("'")[1]if r else P[0];s=Q[f]
  for x in P[1:]:s=s.get('items',s)
  print(f" << {'.'.join(map(str,P))or f}  got {'(missing)'if r else json.dumps(e.instance,ensure_ascii=False)[:30]}\n     expected {sh(s)[:90]}")
 t=='row'or print('SHAPE {'+', '.join('"%s": %s'%(k,json.dumps(Q[k]['const'])if'const'in Q[k]else'<'+sh(Q[k])+'>')for k in j['required'])+'}')
def end(m,r=0):
 os.path.exists(W)and os.remove(W);print(m);sys.exit(r)
def done(w,a):
 e=sorted(jsonschema.Draft7Validator(w['js']).iter_errors(a),key=lambda e:list(e.path))
 if e:
  w['tries']+=1;dia(w['js'],e,f"(try {w['tries']} of {N})")
  w['tries']<N or end(f'window closed: {N} failed tries, nothing written',4);json.dump(w,open(W,'w'));sys.exit(3)
 s=re.sub('[^a-z0-9]+','-',str(a.get('title')or w['nid']).lower()).strip('-')[:60];p=f".agi/nodes/{w['child']}/{s}.md"
 os.path.exists(p)and end('refused: '+p+' exists',5);os.makedirs(os.path.dirname(p),exist_ok=True);b=a.pop('body','# '+str(a.get('title',s)))
 fm={'id':w['child']+':'+s,'type':w['child'],'mint_id':uuid.uuid4().hex,'parents':w['parents'],'next_edges':[],'key':w['nid'],'schema':w['schema'],**a}
 open(p,'w').write('---\n'+yaml.safe_dump(fm,sort_keys=False,allow_unicode=True)+'---\n\n'+b.rstrip('\n')+'\n');end('written '+p)
if A[1]=='open':
 G=[l.rstrip('\n').split('\t')for l in open(E('AGI_GROWTH','.agi/nodes/.geometry/growth.tsv'))];Z={l[0][1:]:l[1]for l in G if l[0][:1]=='@'}
 r=[l for l in G if l[0]==A[2]]or end('refused: no growth row '+A[2],2)
 n,c,v,par=r[0][:4];g='+'.join(sorted(Z.get(x.split(':')[0],x.split(':')[0])for x in A[3:]))
 g==par or end(f'refused: parents {g} but row {n} unlocks {par} -> {c}',2)
 sid,js=sch(c,v.rpartition('=')[2]);json.dump({'nid':n,'child':c,'parents':A[3:],'schema':sid,'js':js,'t':time.time(),'tries':0,'rows':{}},open(W,'w'))
 print('FILL WINDOW OPEN: '+c+('' if v=='-' else f'[{v}]')+f' under {" ".join(A[3:])} · key {n} · schema {sid}\nFORMAT (answer with ONE call to this tool, nothing else):')
 print(json.dumps({'type':'function','function':{'name':'add_'+c,'parameters':js}}))
 print(f'send: agi-fill call (OpenAI, Anthropic or bare arguments) · row by row: agi-fill row "field: value", then "." · abort: agi-fill close · closes after {L}s or {N} failed tries');sys.exit()
if A[1]=='check':
 fm=yaml.safe_load(open(A[2]).read().split('\n---',1)[0][4:]);c=fm['type'];k=(yaml.safe_load(open(f'.agi/context/schemas/[{c}].md').read().split('\n---',1)[0][4:]).get('spawn')or{}).get('discriminator')
 j=sch(c,str(fm.get(k))if k and fm.get(k)else'-')[1];e=list(jsonschema.Draft7Validator(j).iter_errors(json.loads(json.dumps({x:y for x,y in fm.items()if x not in X},default=str))));e and dia(j,e,A[2]);sys.exit(3 if e else 0)
os.path.exists(W)or end('no window open',2);w=json.load(open(W))
time.time()-w['t']<L or end('window closed: timeout, nothing written',4)
if A[1]=='close':end('window closed: aborted, nothing written')
if A[1]=='call':
 x=json.loads(sys.stdin.read());a=x.get('arguments')or x.get('input')or(x.get('function')or{}).get('arguments')or x
 done(w,json.loads(a)if isinstance(a,str)else a)
for l in(A[2:]or sys.stdin.read().splitlines()):
 if l.strip()=='.':done(w,dict(w['rows']))
 k,_,v=l.partition(':');k=k.strip();v=v.strip();s=w['js']['properties'].get(k)
 if s is None:print('refused row',k,': not a field of',w['child'],'-- fields:',' '.join(w['js']['properties']));continue
 if s.get('type',s.get('description','str'))not in('string','str'):v=yaml.safe_load(v or'null')
 m=[e.message[:160]for e in jsonschema.Draft7Validator(s).iter_errors(v)]
 if m:dia({'properties':{k:s},'required':[k]},list(jsonschema.Draft7Validator({'type':'object','properties':{k:s}}).iter_errors({k:v})),'row')
 else:w['rows'][k]=v;print('ok',k)
json.dump(w,open(W,'w'));r=[k for k in w['js']['required']if k not in w['rows']];print('next:',(r[0]+' ('+json.dumps(w['js']['properties'][r[0]])+')')if r else'"." to write')
~~~

### agi-captive (576 B)
~~~sh
#!/bin/sh
# PreToolUse while a fill window is open: ONLY ONE agi-fill command passes (no chaining, no substitution; the quoted heredoc is the way to send text); exit 2 = refused (claude natively; pi through cccc.ts)
[ -e "${AGI_FILL:-$HOME/.fill}" ]||exit 0;jq -r '.tool_input.command//""'|awk 'NR==1{f=$0}{n++}$0=="EOF"{e++;l=n}END{exit!((f~/^agi-fill (call|row) <<\047EOF\047$/&&e==1&&l==n)||(n==1&&f~/^agi-fill (open|call|row|close|check)( [^;&|`$()<>\\]*)?$/))}'&&exit 0;echo "captive: a fill window is open -- ONE agi-fill call | row | close, nothing chained" >&2;exit 2
~~~

[THOUGHT of the proposed node, markers dropped in this doc (one THOUGHT per node, test_thought_hygiene); the landed node carries them]
PROPOSED v5 (round 5, §Q): v4c's wrapper pieces cut whole, byte for byte, + agi-infer (owner 05:50Z, b60af0b63): one OpenAI-compatible chat call; cells infer_url/infer_model/infer_key (a var NAME, never a key). ROUND 7 (§Y2/§Y3): + agi-fill (the captive fill window; `check` verb; on a refusal it prints a CORRECTIVE DIAGRAM generated from the same JSON Schema) + agi-captive + one PreToolUse line in settings.json + agi-infer cell infer_schema (the closed fence copy). agi-fill = the doc bytes + the owner-07:3xZ corrective diagram + the Y1/Y2 const seam fix; agi-captive = the patched copy (the doc one lets `agi-fill close; cmd` through).
[end of that THOUGHT]
~~~~~
### out/engine-grow.md (5105 B, sha256 63a2a4ea9c218ec4)
~~~~~
---
id: config:engine-grow
type: config
parents:
  - goal:g7.16.1.11
  - config:engine
next_edges: []
edited_by: belam
season: 2
town: core
---
# config:engine-grow — EXPANSION of config:engine: node keys (§Y1): the growth matrix check, the land gate, the projector
Read only through `sect <name> [REV]` and the unit's extraction loop; the map of every piece is config:engine's pieces table. The matrix itself is graph data (`.agi/nodes/.geometry/growth.tsv`, projected by grow-project; the aliases cell beside it), never an engine piece.

## files — depth 2, each whole; extract: sect <name> [REV]
### grow-check (1298 B)
~~~sh
#!/bin/sh
# grow-check MATRIX NODE.md: legal only if the node's row (type · variant · parent types sorted · ring) is in MATRIX AND its `key:` is that row's nid
# prints `ok <nid> <ring>` (the hook matches ring to the commit's signer) or `refused: <why>` + the legal shapes; rc 0 | 1
awk -F'\t' 'NR==FNR&&/^@/{A[substr($1,2)]=$2;next} NR==FNR{n[$2 FS $3 FS $4]=$1 FS $5;if($3!="-"){split($3,e,"=");f[$2]=e[1]};s[$2 FS $3]=s[$2 FS $3]" "$4;next}
FNR==1&&/^---/{h=1;next} h&&/^---/{h=0} !h{next}
/^type:/{t=$0;sub(/^type: */,"",t)} /^key:/{k=$0;sub(/^key: */,"",k)} /^parents: *\[/{gsub(/[][ ]|parents:/,"");c=split($0,q,",");for(i=1;i<=c;i++)P[++p]=q[i]}
/^parents: *$/{l=1;next} l&&/^ *- /{x=$0;sub(/^ *- */,"",x);P[++p]=x;next} l{l=0} {split($0,y,": *");a[y[1]]=y[2]}
END{if(t==""){print "refused: not a node (no type:)";exit 1};for(i=1;i<=p;i++){sub(/:.*/,"",P[i]);if(P[i] in A)P[i]=A[P[i]];for(j=i;j>1&&P[j-1]>P[j];j--){z=P[j];P[j]=P[j-1];P[j-1]=z}}
 r="";for(i=1;i<=p;i++)r=r (i>1?"+":"") P[i];if(r=="")r="-";v=f[t]?f[t]"="a[f[t]]:"-";w=t FS v FS r
 if(!(w in n)){print "refused: wrong order: "t" ("v") under ["r"]; legal:"s[t FS v];exit 1};split(n[w],o,FS)
 if(k!=o[1]){print "refused: locked: key "(k?k:"none")" is not "o[1]" for "t" under ["r"]";exit 1};print "ok "o[1]" "o[2]}' "$1" "$2"
~~~

### grow-gate (1435 B)
~~~sh
#!/bin/sh
# pre-receive (the land gate), all against the RECEIVING trunk tip (matrix + schemas via git archive; a push cannot re-key or re-schema itself):
# ADDED node -> grow-check (order + key; a ring other than * = the commit's signer, §W) + agi-fill check (Y2's fields) · CHANGED node -> agi-fill
# check as a RATCHET (refused only if the version it replaces passed: legacy nodes stay editable, nothing that passed can regress)
A=${AGI_ALLOWED:?};t=$(mktemp -d);trap 'rm -rf $t' EXIT;R=$(git rev-parse -q --verify ${AGI_TRUNK:-refs/heads/main})||{ echo "refused: no receiving trunk";exit 1;}
git archive $R .agi/context/schemas .agi/nodes/.geometry/growth.tsv|tar -x -C $t||exit 1;k(){ (cd $t&&agi-fill check $1)>$t/e 2>&1;}
while read o n r;do for c in $(git rev-list $n --not --all);do
 s=$(git -c gpg.ssh.allowedSignersFile=$A verify-commit --raw $c 2>&1|sed -n 's/.*signature for \(.*\) with.*/\1/p')
 git diff-tree -r --root --no-commit-id --diff-filter=AM --name-status $c -- .agi/nodes|grep '\.md$'|grep -v /deprecated/>$t/l
 while read m f;do git show $c:$f>$t/n;if [ $m = A ];then v=$(grow-check $t/.agi/nodes/.geometry/growth.tsv $t/n)||{ echo "$f: $v";exit 1;}
  g=${v##* };[ "$g" = '*' ]||[ "$g" = "$s" ]||{ echo "$f: ring $g, signed by ${s:-nobody}";exit 1;};k n||{ echo "$f:";cat $t/e;exit 1;}
  else k n||{ git show $c^:$f>$t/p;! k p||{ echo "$f: was valid:";k n;cat $t/e;exit 1;};};fi;done<$t/l||exit 1;done;done
~~~

### grow-project (1185 B)
~~~python
#!/usr/bin/env python3
# grow-project SCHEMAS > matrix: every [type].md spawn block -> one row per legal parent shape: nid child variant parents ring
# then the ALIASES cell as @short<TAB>type rows (an id prefix that names a type) · parents = parent TYPES sorted, +-joined (- = none); nid = 16 hex sha256 of the row after nid = the NODE KEY; a schema edit re-keys
import sys,glob,re,yaml,hashlib,itertools as I
[print('@'+l,end='') for l in open(sys.argv[2])]
for f in sorted(glob.glob(sys.argv[1]+'/[[]*].md')):
 t=f.split('[')[-1][:-4];s=(yaml.safe_load(re.match(r'---\n(.*?)\n---',open(f).read(),re.S)[1]) or {}).get('spawn')
 if not s:continue
 d=s.get('discriminator');vs=[(d+'='+k,v) for k,v in s['variants'].items()] if d else [('-',s)]
 for v,r in vs:
  sh=r.get('parent_shapes') or [c for n in range(r['min_parents'],r['max_parents']+1) for c in I.combinations_with_replacement(sorted(r['allowed_parents']),n)]
  for c in sorted({tuple(sorted(x)) for x in sh}):
   if all(c.count(p)>=n for p,n in (r.get('min_parents_by_type') or {}).items()):
    l='\t'.join([t,v,'+'.join(c) or '-','owner' if t=='moral' else '*']);print(hashlib.sha256(l.encode()).hexdigest()[:16]+'\t'+l)
~~~

[THOUGHT of the proposed node, markers dropped in this doc (one THOUGHT per node, test_thought_hygiene); the landed node carries them]
ROUND 7 (§Y1): NEW expansion node holding the three growth tools byte for byte from the doc (grow-check 1298 B, grow-gate 1435 B, grow-project 1185 B); it exists because adding them to engine-wrap would push the 3-node total further past the 20,480 B cap. Needs agi-fill (engine-wrap) at runtime: grow-gate calls `agi-fill check`.
[end of that THOUGHT]
~~~~~
### out/graph/growth.tsv (7111 B, sha256 f58a48615cb83f09)
~~~~~
@hyp	hypothesis
@exp	experiment
0f66d3a8afad8983	bigger_outcome	-	outcome	*
dbb56849ab57c32a	bigger_outcome	-	outcome+outcome	*
0b6905f84d9d338d	bigger_outcome	-	outcome+outcome+outcome	*
19ac860b52b3153c	bigger_outcome	-	outcome+outcome+outcome+outcome	*
7e9c5bb4bf821337	bigger_outcome	-	outcome+outcome+outcome+verdict	*
a8f729854ea7c65a	bigger_outcome	-	outcome+outcome+verdict	*
bf616d67648d91bf	bigger_outcome	-	outcome+outcome+verdict+verdict	*
784a0993145fa8ec	bigger_outcome	-	outcome+verdict	*
91d7de6e016863e2	bigger_outcome	-	outcome+verdict+verdict	*
205f9507ac721a5c	bigger_outcome	-	outcome+verdict+verdict+verdict	*
3ac0d06ca642ad75	bigger_outcome	-	verdict	*
5a76a8b178071f17	bigger_outcome	-	verdict+verdict	*
6d853e9a14a728ac	bigger_outcome	-	verdict+verdict+verdict	*
24e599405dce9508	bigger_outcome	-	verdict+verdict+verdict+verdict	*
ebe20b0f97c0c9b7	build	build_kind=code	build+goal	*
647f2232e438347a	build	build_kind=code	goal+idea	*
554bf8cf8f0940da	build	build_kind=code	goal+mvp	*
f395eed86b9263eb	build	build_kind=code	mvp	*
bf3d39d1415e9492	build	build_kind=prose	build+goal	*
b5717d0e5aa97830	build	build_kind=prose	goal+idea	*
907be6273a0aebbd	build	build_kind=prose	goal+mvp	*
92a89744b7118582	build	build_kind=prose	mvp	*
f7285eb262daaf75	command	-	goal	*
7a677031f745a2ac	config	-	goal	*
fbffb82028560a9f	config	-	goal+goal	*
4f7609ead18865b5	config	-	goal+hypothesis	*
1173486d05508026	config	-	hypothesis	*
d5fb4a515138f291	config	-	hypothesis+hypothesis	*
81f44d1a9f0afb93	cron	-	goal	*
3dbc163531a12b56	doc	-	goal	*
d789f92c07dbb5bc	experiment	-	build	*
a5d67a1d13d589c3	experiment	-	build+build	*
f9bf22a5283e7c8a	experiment	-	build+experiment	*
b561ab46ddf22637	experiment	-	build+hypothesis	*
f29e8d22bde5f454	experiment	-	build+idea	*
9586abaee8617b6f	experiment	-	build+task	*
6e5d3506192d5ab2	experiment	-	build+verdict	*
4bb07330ee547369	experiment	-	experiment	*
4e3ae0e3d006701b	experiment	-	experiment+experiment	*
2732f9cd6fbaf955	experiment	-	experiment+hypothesis	*
951ae18a08287b45	experiment	-	experiment+idea	*
05acaa879cdec859	experiment	-	experiment+task	*
b4eebf58cebe8934	experiment	-	experiment+verdict	*
261fc359f7563adc	experiment	-	hypothesis	*
14dae2d5c5fedb92	experiment	-	hypothesis+hypothesis	*
47fa32086f5f542f	experiment	-	hypothesis+idea	*
ed0f1bc14936b28b	experiment	-	hypothesis+task	*
d1d4c455e368b914	experiment	-	hypothesis+verdict	*
01c74762b3eb6f7d	experiment	-	idea	*
45eda5a5e1db8b0c	experiment	-	idea+idea	*
fbf49560a9a8323e	experiment	-	idea+task	*
61204d4c1f55163d	experiment	-	idea+verdict	*
3d51a4dd42cb8c52	experiment	-	task	*
26ce6570ed448095	experiment	-	task+task	*
4c4801d6ae44708c	experiment	-	task+verdict	*
4d01108b8e7c7906	experiment	-	verdict	*
56e5120b87a8fae9	experiment	-	verdict+verdict	*
9c62c55d899c07de	goal	goal_kind=perpetual	build	*
826b717a5749c736	goal	goal_kind=perpetual	build+build	*
29cd0dc4c92ef7d4	goal	goal_kind=perpetual	build+goal	*
7acd6608e1ab4419	goal	goal_kind=perpetual	build+vision	*
86351e651f00bace	goal	goal_kind=perpetual	goal	*
b9c1c5323749dddf	goal	goal_kind=perpetual	goal+goal	*
3691e8219afad686	goal	goal_kind=perpetual	goal+vision	*
8bcd0ec56c813b27	goal	goal_kind=perpetual	vision	*
34dbb665eb801df0	goal	goal_kind=perpetual	vision+vision	*
b9f9f7f56f0d4455	goal	goal_kind=long-term	build	*
df7c0f5c742d269a	goal	goal_kind=long-term	build+build	*
35156187ad3998cc	goal	goal_kind=long-term	build+goal	*
53f8a6e15fb65cb2	goal	goal_kind=long-term	build+vision	*
f5e206865b9b3e86	goal	goal_kind=long-term	goal	*
4790699ea21c1048	goal	goal_kind=long-term	goal+goal	*
2afdae9bc263ea23	goal	goal_kind=long-term	goal+vision	*
cb9d0d6d3f450630	goal	goal_kind=long-term	vision	*
afb1a636c07ded08	goal	goal_kind=long-term	vision+vision	*
8c447a5e300dad01	goal	goal_kind=short-term	build	*
93116b2582dcb921	goal	goal_kind=short-term	build+build	*
770af3bfc3a5c2da	goal	goal_kind=short-term	build+goal	*
a3569e44f3460b07	goal	goal_kind=short-term	goal	*
38a8e0e6d445c5f7	goal	goal_kind=short-term	goal+goal	*
6d2e046137ea1aa4	goal	goal_kind=subgoal	build+build+goal	*
94616b4945b8cf18	goal	goal_kind=subgoal	build+goal	*
e3d167b7dba6681f	goal	goal_kind=subgoal	build+goal+goal	*
664244b07d7040d2	goal	goal_kind=subgoal	goal	*
e3a4cc303f63969d	goal	goal_kind=subgoal	goal+goal	*
885dae6aad8ef608	goal	goal_kind=subgoal	goal+goal+goal	*
96559ce13454b78b	hypothesis	-	experiment	*
aaaf316485bbbef2	hypothesis	-	experiment+experiment	*
ca3838b7051b40fe	hypothesis	-	experiment+goal	*
c26e5240a4bdce9e	hypothesis	-	experiment+hypothesis	*
29ca8258c2981af5	hypothesis	-	experiment+idea	*
21e059b9381fa3cf	hypothesis	-	goal	*
9c7c7f90ece3931d	hypothesis	-	goal+goal	*
d6e7e1e997910296	hypothesis	-	goal+hypothesis	*
cf27e6741be7db96	hypothesis	-	goal+idea	*
9280cc3a9b91336d	hypothesis	-	hypothesis	*
314ec11419b61b28	hypothesis	-	hypothesis+hypothesis	*
883a587c2310a47a	hypothesis	-	hypothesis+idea	*
ffdc586128924f86	hypothesis	-	idea	*
f66bd0073959768f	hypothesis	-	idea+idea	*
633f9a681dd93048	idea	-	goal	*
42569b80cd93af6b	idea	-	goal+goal	*
b4337c3a6aa3fa9e	idea	-	goal+hypothesis	*
064c37f8a9354922	idea	-	goal+vision	*
0552fe5bcc8a775d	idea	-	hypothesis	*
b34ef6e3e675c6a3	idea	-	hypothesis+hypothesis	*
c5f472df7d7f562a	idea	-	hypothesis+vision	*
b9059e31128e0324	idea	-	vision	*
3a1f12e4925483dd	idea	-	vision+vision	*
43644068064c42f1	ladder	-	goal	*
2fe50ba43c479d67	moral	-	-	owner
e03dba4915468e1f	mvp	-	experiment	*
184a2c5147c53361	mvp	-	experiment+experiment	*
b98f027a9f582a2f	mvp	-	experiment+hypothesis	*
ba04cc9c27fb1b64	mvp	-	experiment+verdict	*
618c7353100a8d75	mvp	-	hypothesis	*
a27ebf4eb90b36f4	mvp	-	hypothesis+hypothesis	*
056ad6d1e21fb5c7	mvp	-	hypothesis+verdict	*
bef53d3c240cf42d	mvp	-	verdict	*
8061927a39d1290f	mvp	-	verdict+verdict	*
b5f5a4d317521645	outcome	-	goal	*
f21e5d0d602b5d37	outcome	-	goal+goal	*
007ea5e243bda0a9	outcome	-	goal+mvp	*
5dc26db2eaf3f618	outcome	-	goal+verdict	*
a735f0cf85760e90	outcome	-	mvp	*
c49781848ddfc603	outcome	-	mvp+mvp	*
c724b02e0935c3cc	outcome	-	mvp+verdict	*
88f58db00055af7f	outcome	-	verdict	*
ace81f37be724e3b	outcome	-	verdict+verdict	*
b0bfbe6eccc4cf35	overview	-	bigger_outcome	*
3322f8129b846d02	overview	-	bigger_outcome+bigger_outcome	*
69199f50ceb12daf	overview	-	bigger_outcome+bigger_outcome+bigger_outcome	*
a9652a597910b550	overview	-	bigger_outcome+bigger_outcome+bigger_outcome+bigger_outcome	*
cd864291d482db53	task	-	hypothesis	*
0bdfa51c9e997b40	town	-	ladder	*
986917f699e30201	verdict	-	experiment	*
8ff4d5c42bb845bf	verdict	-	experiment+experiment	*
d4d7bf6c36587bca	verdict	-	experiment+hypothesis	*
2675be3239053cf3	verdict	-	experiment+verdict	*
86da7184055a1d93	verdict	-	hypothesis	*
64e1c1b42f7b5b79	verdict	-	hypothesis+hypothesis	*
c9463ed75d67b209	verdict	-	hypothesis+verdict	*
748b881bc22eef13	verdict	-	verdict	*
9756b1e990c6cce3	verdict	-	verdict+verdict	*
b65f332cf84fd382	vision	-	moral	*
bb5eeb3e525354f0	vision	-	moral+moral	*
26a04fb6d63547cb	vision	-	moral+moral+moral	*
a1a81e661a05d764	vision	-	moral+moral+moral+moral	*
13eaa84e12cecef3	vision	-	moral+moral+moral+moral+moral	*
~~~~~
### out/graph/growth-aliases.tsv (30 B, sha256 41b0b5d095f129ab)
~~~~~
hyp	hypothesis
exp	experiment
~~~~~
### out/pieces/agi-captive.patched (576 B, sha256 9ea62fd1aa288fd0)
~~~~~
#!/bin/sh
# PreToolUse while a fill window is open: ONLY ONE agi-fill command passes (no chaining, no substitution; the quoted heredoc is the way to send text); exit 2 = refused (claude natively; pi through cccc.ts)
[ -e "${AGI_FILL:-$HOME/.fill}" ]||exit 0;jq -r '.tool_input.command//""'|awk 'NR==1{f=$0}{n++}$0=="EOF"{e++;l=n}END{exit!((f~/^agi-fill (call|row) <<\047EOF\047$/&&e==1&&l==n)||(n==1&&f~/^agi-fill (open|call|row|close|check)( [^;&|`$()<>\\]*)?$/))}'&&exit 0;echo "captive: a fill window is open -- ONE agi-fill call | row | close, nothing chained" >&2;exit 2
~~~~~
### out/agi-fill.diagram.patch (4858 B, sha256 69e429566e8e2a32)
~~~~~
--- doc/agi-fill	2026-10-01 07:40:51.636749095 +0000
+++ src/agi-fill	2026-10-01 08:00:40.448599243 +0000
@@ -15,12 +15,22 @@
  k=(d.get('spawn')or{}).get('discriminator')
  if k and v!='-':P[k]={'const':v}
  P['body']={'type':'string'};return c+'@'+S.run(['git','hash-object',p],capture_output=True,text=True).stdout[:12],{'type':'object','properties':P,'required':[k for k in V.get('required',[])if k not in X],'additionalProperties':True}
+def sh(s):
+ p=s.get('pattern','')[4:-2];q=s.get('items')
+ return 'list of '+sh(q) if q else '= '+json.dumps(s['const']) if 'const' in s else 'one of '+p.strip('()').replace('|',' | ') if re.fullmatch(r'\(?[\w.-]+(\|[\w.-]+)+\)?',p) else 'string /'+p[:60]+('..'if p[60:]else'')+'/' if p else s.get('type')or s.get('description','str')
+def dia(j,E,t):
+ Q=j['properties'];print('refused',t,':',len(E),'wrong')
+ for e in E:
+  r=e.validator=='required';P=list(e.path);f=e.message.split("'")[1]if r else P[0];s=Q[f]
+  for x in P[1:]:s=s.get('items',s)
+  print(f" << {'.'.join(map(str,P))or f}  got {'(missing)'if r else json.dumps(e.instance,ensure_ascii=False)[:30]}\n     expected {sh(s)[:90]}")
+ t=='row'or print('SHAPE {'+', '.join('"%s": %s'%(k,json.dumps(Q[k]['const'])if'const'in Q[k]else'<'+sh(Q[k])+'>')for k in j['required'])+'}')
 def end(m,r=0):
  os.path.exists(W)and os.remove(W);print(m);sys.exit(r)
 def done(w,a):
  e=sorted(jsonschema.Draft7Validator(w['js']).iter_errors(a),key=lambda e:list(e.path))
  if e:
-  w['tries']+=1;[print('refused',e.path[0]if e.path else'-',':',e.message[:160])for e in e]
+  w['tries']+=1;dia(w['js'],e,f"(try {w['tries']} of {N})")
   w['tries']<N or end(f'window closed: {N} failed tries, nothing written',4);json.dump(w,open(W,'w'));sys.exit(3)
  s=re.sub('[^a-z0-9]+','-',str(a.get('title')or w['nid']).lower()).strip('-')[:60];p=f".agi/nodes/{w['child']}/{s}.md"
  os.path.exists(p)and end('refused: '+p+' exists',5);os.makedirs(os.path.dirname(p),exist_ok=True);b=a.pop('body','# '+str(a.get('title',s)))
@@ -31,13 +41,13 @@
  r=[l for l in G if l[0]==A[2]]or end('refused: no growth row '+A[2],2)
  n,c,v,par=r[0][:4];g='+'.join(sorted(Z.get(x.split(':')[0],x.split(':')[0])for x in A[3:]))
  g==par or end(f'refused: parents {g} but row {n} unlocks {par} -> {c}',2)
- sid,js=sch(c,v);json.dump({'nid':n,'child':c,'parents':A[3:],'schema':sid,'js':js,'t':time.time(),'tries':0,'rows':{}},open(W,'w'))
+ sid,js=sch(c,v.rpartition('=')[2]);json.dump({'nid':n,'child':c,'parents':A[3:],'schema':sid,'js':js,'t':time.time(),'tries':0,'rows':{}},open(W,'w'))
  print('FILL WINDOW OPEN: '+c+('' if v=='-' else f'[{v}]')+f' under {" ".join(A[3:])} · key {n} · schema {sid}\nFORMAT (answer with ONE call to this tool, nothing else):')
  print(json.dumps({'type':'function','function':{'name':'add_'+c,'parameters':js}}))
  print(f'send: agi-fill call (OpenAI, Anthropic or bare arguments) · row by row: agi-fill row "field: value", then "." · abort: agi-fill close · closes after {L}s or {N} failed tries');sys.exit()
 if A[1]=='check':
  fm=yaml.safe_load(open(A[2]).read().split('\n---',1)[0][4:]);c=fm['type'];k=(yaml.safe_load(open(f'.agi/context/schemas/[{c}].md').read().split('\n---',1)[0][4:]).get('spawn')or{}).get('discriminator')
- e=list(jsonschema.Draft7Validator(sch(c,str(fm.get(k))if k and fm.get(k)else'-')[1]).iter_errors({x:y for x,y in fm.items()if x not in X}));[print('refused',A[2],list(x.path),x.message[:120])for x in e];sys.exit(3 if e else 0)
+ j=sch(c,str(fm.get(k))if k and fm.get(k)else'-')[1];e=list(jsonschema.Draft7Validator(j).iter_errors(json.loads(json.dumps({x:y for x,y in fm.items()if x not in X},default=str))));e and dia(j,e,A[2]);sys.exit(3 if e else 0)
 os.path.exists(W)or end('no window open',2);w=json.load(open(W))
 time.time()-w['t']<L or end('window closed: timeout, nothing written',4)
 if A[1]=='close':end('window closed: aborted, nothing written')
@@ -47,9 +57,9 @@
 for l in(A[2:]or sys.stdin.read().splitlines()):
  if l.strip()=='.':done(w,dict(w['rows']))
  k,_,v=l.partition(':');k=k.strip();v=v.strip();s=w['js']['properties'].get(k)
- if s is None:print('refused row',k,': not a field of',w['child']);continue
+ if s is None:print('refused row',k,': not a field of',w['child'],'-- fields:',' '.join(w['js']['properties']));continue
  if s.get('type',s.get('description','str'))not in('string','str'):v=yaml.safe_load(v or'null')
  m=[e.message[:160]for e in jsonschema.Draft7Validator(s).iter_errors(v)]
- if m:print('refused row',k,':',m[0])
+ if m:dia({'properties':{k:s},'required':[k]},list(jsonschema.Draft7Validator({'type':'object','properties':{k:s}}).iter_errors({k:v})),'row')
  else:w['rows'][k]=v;print('ok',k)
 json.dump(w,open(W,'w'));r=[k for k in w['js']['required']if k not in w['rows']];print('next:',(r[0]+' ('+json.dumps(w['js']['properties'][r[0]])+')')if r else'"." to write')
~~~~~

<!-- THOUGHT:BEGIN — authored, not derived; carried across regenerating scans. The reasoning behind THIS version. -->
PROPOSED v5 build record for round 7 (growth order kept by the engine itself: grow-check / grow-gate / grow-project, the node-key matrix), carrying the proposed config node bodies in ~~~~~ fences. This version (DG3 10:4xZ 10-01, SM trunk red test_thought_hygiene): the embedded nodes THOUGHT markers are dropped to plain labels so this doc holds ONE THOUGHT; the landed nodes carry their own (land package doc:g716111-land-package).
<!-- THOUGHT:END -->
