---
id: config:engine-wrap
mint_id: b613fd9a93a643f188209ffdf8bb3870
type: config
parents:
  - goal:g7.16.1.11.5
next_edges: []
edited_by: belam
scaffold_hash: eb92bfc5bf8775e1
season: 2
town: core
---
# config:engine-wrap

EXPANSION of config:engine: the post wrappers (pane command, hook wiring, pi bridge, the kid, raw inference, the captive hook)
Read through `sect <name> [REV]` (every `.geometry/engine*.md` at one REV) and the unit's extraction loop (engine.md + engine-post + engine-wrap); every piece is in config:engine's map.

## files — depth 2, each whole; extract: sect <name> [REV]

### agi-run (501 B)
~~~sh
#!/bin/sh
cd ~/t;c=-c;[ -e ~/.fresh ]&&rm ~/.fresh&&c=;stty cols 200 rows 50;i=$RUNTIME_DIRECTORY/i;f=$O/.agi/sessions/inbox/$AGI_SEAT.md
(while sleep 300;do m=$((${AGI_PANE_MAX_MB:-64}<<20));[ $(stat -c%s ~/o) -gt $m ]&&tail -c $((m/2)) ~/o>~/o.t&&cat ~/o.t>~/o;rm -f ~/o.t;done)&
case $H in claude*)(s=$(stat -c%s $f 2>/dev/null||echo 0);while sleep 5;do n=$(stat -c%s $f 2>/dev/null||echo 0);[ $n -gt $s ]&&printf "mail: send.py read $AGI_SEAT">$i&&sleep 1&&printf '\r'>$i;s=$n;done)&;;esac
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

### agi-captive (576 B)
~~~sh
#!/bin/sh
# PreToolUse while a fill window is open: ONLY ONE agi-fill command passes (no chaining, no substitution; the quoted heredoc is the way to send text); exit 2 = refused (claude natively; pi through cccc.ts)
[ -e "${AGI_FILL:-$HOME/.fill}" ]||exit 0;jq -r '.tool_input.command//""'|awk 'NR==1{f=$0}{n++}$0=="EOF"{e++;l=n}END{exit!((f~/^agi-fill (call|row) <<\047EOF\047$/&&e==1&&l==n)||(n==1&&f~/^agi-fill (open|call|row|close|check)( [^;&|`$()<>\\]*)?$/))}'&&exit 0;echo "captive: a fill window is open -- ONE agi-fill call | row | close, nothing chained" >&2;exit 2
~~~

<!-- THOUGHT:BEGIN — authored, not derived; carried across regenerating scans. The reasoning behind THIS version. -->
PROPOSED v5 (round 5, §Q): v4c's wrapper pieces cut whole + agi-infer (owner 05:50Z): one OpenAI-compatible chat call; cells infer_url/infer_model/infer_key (a var NAME, never a key). ROUND 7: + agi-captive (the patched copy: the doc one lets `agi-fill close; cmd` through) + one PreToolUse line in settings.json + agi-infer cell infer_schema. agi-run + a pane trim loop (cell pane_max_mb, default 64). SPLIT: agi-fill moved to engine-grow.
<!-- THOUGHT:END -->
