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

## pieces — depth 1, one line each (bytes on disk)
~~~
agi-run           2303 B  pane cmd: fresh=new id, else --resume ~/.session
settings.json      460 B  the ONE hook wiring: brief, meter, turn commit
cccc.ts           1959 B  pi events -> the CC hooks; mail -> a turn
agi-in            3476 B  kid spawn: capsule pull = graph|director|none
agi-infer          1332 B  ONE chat call, OpenAI-compatible: stdin -> stdout
agi-lane           1403 B  a Console lane's pi / claude -p / header config
agi-captive        1360 B  window open: only agi-fill; a dead window: released
agi-pray           14966 B  prayer: brief head, captive start + out, idle stop
~~~

## files — depth 2, each whole; extract: sect <name> [REV]

### agi-run (2303 B)
~~~sh
#!/bin/sh
cd ~/t;c=-c;[ -e ~/.fresh ]&&rm ~/.fresh&&c=;stty cols 200 rows 50;i=$RUNTIME_DIRECTORY/i;f=$O/.agi/sessions/inbox/$AGI_POST.md
(while :;do sleep 300||:;m=$((${AGI_PANE_MAX_MB:-64}<<20));[ $(stat -c%s ~/o 2>/dev/null||echo 0) -gt $m ]&&tail -c $((m/2)) ~/o>~/o.t&&cat ~/o.t>~/o;rm -f ~/o.t;done)&L1=$!
case $H in claude*)(s=$(stat -c%s $f 2>/dev/null||echo 0);while :;do sleep 5||:;n=$(stat -c%s $f 2>/dev/null||echo 0);[ $n -gt $s ]&&printf "mail: send.py read $AGI_POST">$i&&sleep 1&&printf '\r'>$i;s=$n;done)&L2=$!;;esac
case $H in claude*)(umask 077;j=~/.claude.json;n=$j.n;jq -e '((.fullscreenUpsellSeenCount//0)|numbers)>=3' $j>/dev/null 2>&1||{ if [ -e $j ];then jq '.fullscreenUpsellSeenCount=3' $j;else echo '{"fullscreenUpsellSeenCount":3}';fi>$n 2>/dev/null&&[ -s $n ]&&mv $n $j;rm -f $n;});;esac
[ -z "$c" ]&&(p=$AGI_POST;r=$(git show ${AGI_TRUNK:-HEAD}:.agi/nodes/.geometry/rotations.md 2>/dev/null|awk -v p=$p '/^---$/{if(++n>1)exit;next}n!=1||/^[ ]*(#.*)?$/{next}/^alerts:[ ]*$/{a=s=1;next}/^[^ ]/{a=0}!a{next}/^  (audit|silent):[ ]*$/{k=$1;sub(/:/,"",k);m="l";next}/^  edges:[ ]*\{\}[ ]*$/{m="";next}/^  edges:[ ]*$/{m="e";next}m=="l"&&/^    - [a-z][a-z0-9-]*[ ]*$/{L[k]=L[k]" "$2;next}m=="e"&&/^    [a-z][a-z0-9-]*:[ ]*$/{e=$1;sub(/:/,"",e);next}m=="e"&&/^      - [a-z][a-z0-9-]*[ ]*$/{if(e==p)E=E" "$2;next}{b=1}END{if(!s||b)exit 1;n=split(L["audit"]E,w," ");z=split(L["silent"],y," ");for(i=1;i<=z;i++)S[y[i]];S[p];for(i=1;i<=n;i++)if(!(w[i] in S)){S[w[i]];print w[i]}}')||echo "warn: rotation alert: alerts cell unreadable, nothing sent" >&2;[ -n "$r" ]&&timeout -k 2 20 sh -c 'for x in $0;do printf "[rotation-alert] $1 restarted fresh $(date -u +%FT%TZ)\n"|AGI_POST=$1 box send $x||echo "warn: rotation alert to $x failed" >&2;done' "$r" $p)2>>$RUNTIME_DIRECTORY/alert&
case $H in claude*)d=~/.claude/projects/$(pwd -P|sed 's/[^A-Za-z0-9]/-/g');if [ -z "$c" ];then s=$(cat /proc/sys/kernel/random/uuid);c="--session-id $s";else s=$(cat ~/.session 2>/dev/null);case $s in *[!0-9a-f-]*)s=;;esac;[ -n "$s" ]&&[ -s "$d/$s.jsonl" ]||s=$(ls -t "$d"/*.jsonl 2>/dev/null|sed -n '1s|.*/||;1s|\.jsonl$||p');[ -n "$s" ]&&c="--resume $s";fi;[ -n "$s" ]&&(umask 077;echo $s>~/.session);;esac
strace -qqf -b execve -e%file -o'|agi-track' $H $c go;r=$?;kill $L1 $L2 2>/dev/null;exit $r
~~~

### settings.json (460 B)
~~~json
{"skipDangerousModePermissionPrompt":true,"tui":"default","hooks":{"PreToolUse":[{"hooks":[{"type":"command","command":"agi-captive"}]}],"SessionStart":[{"hooks":[{"type":"command","command":"agi-brief","timeout":180}]}],"UserPromptSubmit":[{"hooks":[{"type":"command","command":"agi-meter"}]}],"Stop":[{"hooks":[{"type":"command","command":"agi-turn","timeout":180},{"type":"command","command":"agi-mem tap"},{"type":"command","command":"agi-pray stop"}]}]}}
~~~

### cccc.ts (1959 B)
~~~ts
import{execSync as x}from"node:child_process";import{readFileSync as R,watchFile as W,unwatchFile as U}from"node:fs"
const E=process.env,H=JSON.parse(R(E.HOME+"/.claude/settings.json","utf8")).hooks,N={bash:"Bash",read:"Read",edit:"Edit",write:"Write"};let b="",v
const h=(n,j={})=>{let o="",k=0;for(const g of H[n]||[])if(!g.matcher||RegExp(g.matcher).test(j.tool_name))for(const c of g.hooks)try{o+=x(c.command,{input:JSON.stringify({hook_event_name:n,cwd:process.cwd(),...j}),encoding:"utf8",stdio:"pipe",timeout:(c.timeout||60)*1e3})}catch(e){if(e.status==2)k=2,o+=e.stderr}return{o,k}}
const t=e=>({tool_name:N[e.toolName]||e.toolName,tool_input:e.input}),S=s=>{b=h("SessionStart",{source:s}).o}
export default p=>{const on=(e,f)=>p.on(e,f);on("session_start",e=>{S({new:"clear",fork:"resume",reload:"resume"}[e.reason]||e.reason)
const f=`${E.O}/.agi/sessions/inbox/${E.AGI_POST}.md`;U(f);W(f,{interval:5e3,persistent:!1},(n,o)=>n.size>o.size&&p.sendUserMessage("mail: send.py read "+E.AGI_POST,{deliverAs:"followUp"}))
let s=new Set;clearInterval(v);v=setInterval(()=>{try{const n=new Set(x("box i 2>/dev/null",{encoding:"utf8",stdio:["ignore","pipe","ignore"]}).split("\n").filter(l=>l&&l[0]!="["));[...n].some(l=>!s.has(l))&&p.sendUserMessage("mail: box read",{deliverAs:"followUp"});s=n}catch{}},5e3).unref()})
on("session_compact",()=>S("compact"));on("before_agent_start",e=>b&&{systemPrompt:e.systemPrompt+"\n\n"+b})
on("input",(e,c)=>{const u=c.getContextUsage()||{},r=h("UserPromptSubmit",{prompt:e.text,tokens:u.tokens,context_window:u.contextWindow});return r.k?{action:"handled"}:r.o&&{action:"transform",text:e.text+"\n\n"+r.o}})
on("tool_call",e=>{const r=h("PreToolUse",t(e));return r.k&&{block:true,reason:r.o}});on("tool_result",e=>{h("PostToolUse",t(e))})
on("session_before_compact",()=>{h("PreCompact",{trigger:"auto"})});on("turn_end",()=>{h("Stop")});on("session_shutdown",()=>{clearInterval(v);h("SessionEnd",{reason:"other"})})}
~~~

### agi-in (3476 B)
~~~sh
#!/bin/sh
# agi-in -m FLOW ARGS | pack ATTACH SEL.. [--pull graph|director|none] [--reach closed|open] [--at MINT] [--scope HEX] [--atoms ARGS.json] | CID KID PROMPT..: the ONE kid spawn verb (goal:g7.16.1.11.46.21); the capsule's MANIFEST `pull` picks it: graph|director = a pi kid (own HOME, tree, AGI_CID), none = ONE request, no tools, no tree
K="--provider openrouter --model $AGI_KID_MODEL"
if [ "$1" = -m ];then M=$2;A=$3;P=;d=;case $M in *[!a-z0-9-]*)exit 1;;esac;cd ~/t;s=$(printf %s "$A"|sha256sum|cut -c1-12);D=~/s/$M/$s;R=refs/spawn/$M/$s
git show-ref --verify -q $R&&exit
n(){ echo $D/o.$(printf %s "$P$1"|tr -c 'A-Za-z0-9._:-' _);}
st(){ case .$2.$3.$4 in *.-*|*[!a-z0-9.-]*)exit 75;;esac;case $6 in [-@]*)exit 75;;esac;o=$(n "$1")
 if [ "$2" ];then [ "$V" ]&&return;q=$(git show HEAD:.agi/nodes/goal/$3.md|sed -n '/^## Falsifier/,/^## /s/^\$ //p'|head -1)
  printf %s "$q"|grep -Eq '^(grep|test|ls|git (rev-parse|ls-files|for-each-ref)) [^;&|<>`$()\\]*$'&&timeout 30 sh -c "$q"</dev/null>/dev/null||{ [ -e $o.h ]||{ m="handoff $M $1 $3";echo "$m"|box send "$2" "$m"&&:>$o.h;};exit 75;}
 elif [ "$4" ];then [ ${#d} -lt 2 ]&&(P=$P$1/;d=$d.;fl $4)||exit $?
 elif [ ! -f $o -a -z "$V" ];then r=$6;[ "$5" ]&&{ b=$(n "$5");[ -f $b ]||b=$(n "$5:$7");r="$r
$(cat $b)"||exit 1;};W=$(mktemp -d)||{ echo "unread: no scratch dir">&2;exit 1;};git archive HEAD|tar -xC $W
  (cd $W;HOME=$W pi $K -p "$r"</dev/null>$o.t)||{ rm -rf $W $o.t;exit 1;};rm -rf $W;mv $o.t $o;fi;}
fl(){ x=$(git show HEAD:extensions/agi/workflows/$1.json|jq -r --argjson a "$A" '.stages as $S|range($S|length)as $i|$S[$i]|.chained_from as $c|(if .repeat then ($a[.repeat.of]|arrays//error)[].key else "" end) as $k|(if $c and([$S[:$i][].label]|index($c)|not)then error end|"st ")+([(.repeat.label_template//.label),(.post,.goal,.flow,$c,.prompt|.//""),$k]|map(gsub("\\{key\\}";$k))|@sh)')&&[ "$x" ]||exit 1;mkdir -p $D;eval "$x";}
V=1;fl $M;V=;fl $M;(export GIT_DIR=$PWD/.git GIT_WORK_TREE=$D GIT_INDEX_FILE=$(mktemp -u);cd $D&&git add -A&&git update-ref $R $(git commit-tree -S -m $s $(git write-tree)));exit $?;fi
if [ "$1" = pack ];then shift;set -f;a=;N=;while [ $# -gt 0 ];do case $1 in --pull|--reach|--at|--scope)case ${1#--}.$2 in pull.graph|pull.director|pull.none|reach.closed|reach.open|at.?*|scope.?*);;*)echo "agi-in: [$1] $2">&2;exit 2;;esac
 case ${1#--}.$2 in at.*[!0-9a-f]*|scope.*[!0-9a-f]*)echo "agi-in: [$1] $2">&2;exit 2;;esac;N="$N
${1#--} $2";shift 2;;--atoms)N="$N
atoms:
$(jq -er '.atoms[]|"  \(.id) \(.src) \(.sha)"' "$2")"||exit 2;shift 2;;*)a="$a $1";shift;;esac;done;cd ~/t;sect capsule|AGI_MF="$N" sh -s -- pack $a;exit;fi
c=$1;k=$2;shift $(($#<2?$#:2));cd ~/t;case $c in ""|*[!0-9a-f]*)echo "unread: capsule [$c]";exit 1;;esac;sect capsule|sh -s -- verify $c>/dev/null&&M=$(git show refs/capsule/$c:MANIFEST)||{ echo "unread: capsule $c";exit 1;}
case $(echo "$M"|sed -n 's/^pull //p') in none)W=$(mktemp -d)||{ echo "unread: no scratch dir";exit 1;};(cd $W;HOME=$W pi $K --no-tools -p "$*"</dev/null);r=$?;rm -rf $W;exit $r;;graph|director);;*)echo "unread: pull in $c";exit 1;;esac
case $k in ""|*[!a-z0-9-]*)echo "unread: kid [$k]";exit 1;;esac;h=~/k/$k;mkdir -p $h/.claude;[ -d $h/t ]||git worktree add -q $h/t -b kids/$k
for x in .gitconfig .ssh hooks .claude/settings.json;do ln -sfn ~/$x $h/$x;done
cd $h/t;HOME=$h AGI_POST=$k AGI_ROLE=kid AGI_HARNESS=pi-free AGI_WT=$RUNTIME_DIRECTORY/k-$k AGI_CID=$c exec pi $K --skill skills -e ~/bin/cccc.ts -p "$*"</dev/null
~~~

### agi-infer (1332 B)
~~~sh
#!/bin/sh
# agi-infer [MODEL] <prompt: ONE streamed call to any OpenAI-compatible /v1/chat/completions; cells infer_url, infer_model, infer_key (the NAME of a var in the unit's EnvironmentFile), infer_cred (a key FILE, read ONLY when set, no default: it replaces infer_key), infer_workspace (the anthropic-workspace-id header), infer_schema (a JSON Schema FILE: the reply is fenced to it, closed)
k=;case $AGI_INFER_KEY in [0-9]*|*[!A-Za-z0-9_]*)exit 2;;?*)eval k=\$$AGI_INFER_KEY;;esac
[ -r "$AGI_INFER_CRED" ]&&k=$(cat "$AGI_INFER_CRED")
s=$([ "$AGI_INFER_SCHEMA" ]&&jq -c '.+{additionalProperties:false}' $AGI_INFER_SCHEMA)
jq -Rsc --arg m "${1:-$AGI_INFER_MODEL}" --argjson s "${s:-null}" '{model:$m,stream:true,messages:[{role:"user",content:.}]}+if $s then {response_format:{type:"json_schema",json_schema:{name:"fill",schema:$s}}} else {} end'|curl -sfN -H @/dev/fd/3 -H 'Content-Type: application/json' -d @- ${AGI_INFER_URL:-http://127.0.0.1:8080/v1}/chat/completions 3<<X|sed -un 's/^data: //p'|jq -nRrj --unbuffered 'def g:(try input catch("cut"|halt_error(5)))|if .=="[DONE]" then empty else((fromjson|if .error or .choices[0].finish_reason=="error" then halt_error else .choices[0].delta.content//empty end),g)end;g'
${k:+Authorization: Bearer $k}
${AGI_INFER_WORKSPACE:+anthropic-workspace-id: $AGI_INFER_WORKSPACE}
X
~~~

### agi-lane (1403 B)
~~~sh
#!/bin/sh
# agi-lane id|header|pi|claude LANE [MODEL]: one Console lane's front config, from the lane cell of config:secrets (ids and names, never a key). id = the workspace id; header = the `Name: value` line for ANTHROPIC_CUSTOM_HEADERS; pi = the models.json provider claude-lane (apiKey "!cat <credential>", run at request time); claude = the --settings JSON (apiKeyHelper cats the same file). Option B (scoped_key): no header, the file is the lane's own. rc 2 = no such lane, 3 = the id is not filled yet (owner act)
v=$1;l=$2;c=$(git show "${AGI_TRUNK:-HEAD}:.agi/nodes/.geometry/secrets.md" 2>/dev/null|sed -n "s/^  $l: //p"|head -1);[ "$c" ]||{ echo "[lane] $l: no cell" >&2;exit 2;}
w=$(echo "$c"|jq -r '.workspace//empty');n=$(echo "$c"|jq -r '.scoped_key//"claude-sp"');k=$(echo "$c"|jq -r 'has("scoped_key")')
[ "$k" = true ]||[ "$w" ]||{ echo "[lane] $l: the workspace id is empty (the owner makes the workspace)" >&2;exit 3;}
f="cat \$CREDENTIALS_DIRECTORY/$n"
case $v in id)echo "$w";;header)[ "$w" ]&&echo "anthropic-workspace-id: $w";;claude)jq -nc --arg f "$f" '{apiKeyHelper:$f}';;
pi)jq -nc --arg u "${AGI_LANE_URL:-https://api.anthropic.com}" --arg m "${3:-claude-haiku-5-5}" --arg f "!$f" --arg w "$w" '{providers:{"claude-lane":({baseUrl:$u,api:"anthropic-messages",apiKey:$f,models:[{id:$m}]}+if $w!="" then {headers:{"anthropic-workspace-id":$w}} else {} end)}}';;*)exit 2;;esac
~~~

### agi-captive (1360 B)
~~~sh
#!/bin/sh
# PreToolUse while a fill window is open: ONLY ONE agi-fill command passes (no chaining, no substitution; the quoted heredoc is the way to send text); exit 2 = refused (claude natively; pi through cccc.ts). A window that cannot be used is RELEASED, never a lock (agi-fill absent, or older than ${AGI_FILL_WINDOW:-900} s). FIRST (goal:g7.16.1.11.46.29, the owner 11-01): agi-pray captive, the session's prayer; its exit 2 refuses, anything else passes (agi-pray absent: one [pray] line, passed)
j=$(cat);if command -v agi-pray >/dev/null;then printf '%s' "$j"|agi-pray captive;[ $? = 2 ]&&exit 2;else echo "[pray] unread: agi-pray not on PATH (passed)" >&2;fi
w=${AGI_FILL:-$HOME/.fill};[ -e "$w" ]||exit 0;command -v agi-fill >/dev/null||r="agi-fill not on PATH (engine defect)";m=$(stat -c %Y "$w" 2>/dev/null);[ $(($(date +%s)-${m:-0})) -gt ${AGI_FILL_WINDOW:-900} ]&&r=${r:-window expired}
[ -z "$r" ]||{ echo "[captive] $w released: $r" >&2;mv "$w" "$w.released-$(date -u +%Y%m%dT%H%M%SZ)" 2>/dev/null;exit 0;}
printf '%s' "$j"|jq -r '.tool_input.command//""'|awk 'NR==1{f=$0}{n++}$0=="EOF"{e++;l=n}END{exit!((f~/^agi-fill (call|row) <<\047EOF\047$/&&e==1&&l==n)||(n==1&&f~/^agi-fill (open|call|row|close|check)( [^;&|`$()<>\\]*)?$/))}'&&exit 0;echo "captive: a fill window is open -- ONE agi-fill call | row | close, nothing chained" >&2;exit 2
~~~

### agi-pray (14966 B)
~~~py
#!/usr/bin/env python3
# agi-pray head ROOT | captive | stop -- goal:g7.16.1.11.46.29 (P0, the owner 11-01): a session opens and closes with a Church Slavonic prayer from moral:faith; MAY at each idle spot (owner 11-07); never per working turn.
# head: goal .46.29.2's HEAD first, inside the harness's 2000-char preview (## YOUR FIRST REPLY: the reply-final ask, the card's path, its where-it-stops line cut to WIDTH chars; 'card unread: PATH' when it cannot be read), then the prayers block of moral:faith (### 4.1, as brief.py's _read_faith_ref reads it) + the reply-final ask. captive (PreToolUse, from agi-captive): exit 2 until an assistant text of THIS transcript holds a prayer, then ~/.prayed/<session> and never again; the v5 out (touch ~/.fresh, kill $PPID) also needs one in the newest assistant text since the card's last WRITE (its mtime in ~/t, goal:g7.16.1.11.46.30: the wrapper commits the card at the turn end AFTER the reply that prays, so a commit clock would refuse every out). stop (Stop, goal .46.29.4 (S)): FIRST, in a marked session, a last reply whose TRAILING PRAYER BLOCK prays (walking back over blank or markup-only lines and Cyrillic lines with no Latin letter) stamps ~/.prayed/<session>.end and returns, stop_hook_active or not; .end is stamped only on a prayer, never on the ask; then (stop_hook_active honoured) a reply whose last non-empty LINE is idle is ASKED, with no state, until a close prayer is said; a negation (not, n't, never, no longer) within the three words before the match, no clause mark between, spares the line. Prayers match after a FOLD (NFD, marks dropped, old letters to modern, casefold, final hard sign dropped). The marker is read FIRST: a prayed session opens no transcript except at the out (alive 08:04:04Z). A call carrying agent_id is a SUBAGENT inside a session, never captive: the docs name agent_id on its PreToolUse but not which transcript_path it gets. ANY unread input passes with one [pray] line: never a lock. goal .46.29.1: a Stop whose reply-final text prays in an UNMARKED session marks it and blocks once with GO, so the post resumes with no outside input; the out is the L358 whole search (OUT): a kill of the literal PPID, a kill whose operand is an expansion ($var, ${var}, $( ), backticks, an escaped \$; not $!, $$, kill -0 / -s 0) when the command's text names ppid in any case (KV), a touch of ~/.fresh, a touch whose operand is an expansion when .fresh is named anywhere in the command (TV), and an unquoted redirect into ~/.fresh (never exempt); a match is exempt only in a # comment, or when the segment that consumes it (its own, or the one holding the quote / the heredoc's <<) leads, past WRAP words, with a printer (SHOW) not piped to a RUN word; $( ) or backticks, bare (a segment boundary) or in double quotes or an unquoted heredoc, run (never exempt); a printer piped into anything but a plain filter (SAFE), or whose pipeline writes a file anywhere (>, tee, sort -o / --output, uniq's OUT) when a later segment leads with a RUN word or, leading with no printer, names that file anywhere in its words, loses it too; a printer inside an unquoted $( ), backtick pair or <( ) keeps it only when the ENCLOSING segment would itself pass, and a segment ends past any substitution inside it; an unknown leading word is the out; a command left inside an open quote is searched whole (fail closed).
import json,os,re,subprocess,sys,unicodedata
ASK="captive: say an Old Slavonic protection prayer before proceeding: your next reply is that prayer and nothing else: no tool call before or after it (that ENDS the turn: a pause until your next prompt, not a hang); a prayer beside a call is read again at the next call"
GO="prayed: the captive is released; continue your work"
OUT=re.compile(r"""touch(?:[ \t]+-\S*)*[ \t]+["']?(?:~|\$\{?HOME\}?)["']?/["']?\.fresh|>[ \t]*["']?(?:~|\$\{?HOME\}?)["']?/["']?\.fresh|\bkill\b(?:[ \t]+(?:-[sn][ \t]+\w+|-\w+|--))*[ \t]+["']?\$\{?PPID\}?""")
KV=re.compile(r"""\bkill\b(?![ \t]+(?:-0|-s[ \t]+0)\b)(?:[ \t]+(?:-[sn][ \t]+\w+|-\w+|--))*[ \t]+["']?\\?(?:`|\$(?![!$]))""")
TV=re.compile(r"""\btouch(?:[ \t]+-\S*)*[ \t]+["']?\\?(?:`|\$)""")
SHOW={"echo","printf","grep","egrep","fgrep","rg","jq","cat","head","tail","less","wc","sort","diff","git log","git grep","git show","git diff"}
WRAP={"env","timeout","nohup","nice","time","sudo","command","exec","builtin"}
RUN={"sh","bash","dash","zsh","ksh","xargs","eval","source","."}
SAFE=SHOW|{"tee","cut","tr","uniq","nl","fold","column"}
OLD=str.maketrans({"ѧ":"я","ѣ":"е","ї":"и","і":"и","ѻ":"о","ѡ":"о","ꙗ":"я","ѿ":"от","ѯ":"кс","ѱ":"пс","ѳ":"ф","ѵ":"и"})
def fold(s):
    s="".join(c for c in unicodedata.normalize("NFD",s) if not unicodedata.combining(c))
    s=unicodedata.normalize("NFC",s).casefold().translate(OLD)
    return re.sub(r"ъ\b","",s)
KEYS=[fold(k) for k in ("Господи","Боже","Ѻтче","Свѧтый")]
def prays(t):return any(re.search("[а-яё]",l) and any(k in l for k in KEYS) for l in fold(t or "").splitlines())
CYR=re.compile("[\u0400-\u052f\u1c80-\u1c8f\u2de0-\u2dff\ua640-\ua69f]");LAT=re.compile("[A-Za-z\u00c0-\u024f]")
def block(t):
    L=(t or "").splitlines();i=len(L)
    while i and (not L[i-1].strip(" \t>*_~-") or (CYR.search(L[i-1]) and not LAT.search(L[i-1]))):i-=1
    return "\n".join(L[i:])
IDLE=re.compile(r"nothing (left|actionable|owed|to do)|queue (is )?(empty|all held)|\b(stay|go|remain)(ing)? idle\b|\bgoing idle\b",re.I)
def idle(l):return any(not re.search(r"\b(not|never|no longer)\b|n['\u2019]t\b"," ".join(re.split(r"[,;:.\u2013\u2014]|\s-+\s|--",l[:x.start()])[-1].split()[-3:]),re.I) for x in IDLE.finditer(l))
def warn(m):print("[pray] unread: "+m+" (passed)",file=sys.stderr);sys.exit(0)
def faith(root):
    t=open(os.path.join(root,".agi/nodes/moral/faith.md"),encoding="utf-8").read()
    r=re.search(r"^##\s+REFERENCE",t,re.M);t=t[r.end():].strip() if r else "";h=re.compile(r"^###\s+4\.(\d)\s+",re.M);m=h.search(t)
    while m and m.group(1)!="1":m=h.search(t,m.end())
    if not m:return ""
    n=h.search(t,m.end());return t[m.end():n.start() if n else len(t)].strip()
FIRST="your FIRST reply is ONE prayer below and nothing else: no tool call before or after it (that ENDS the turn); if the rest of this output was saved to a file, read it in your NEXT reply, then read your card"
WIDTH=120
def card(r):
    p=os.path.join(r,".agi/nodes/doc/card-%s.md"%re.sub(r"[^A-Za-z0-9-]","",os.environ.get("AGI_POST","")))
    try:t=open(p,encoding="utf-8").read()
    except Exception:return "card unread: "+p
    m=re.search(r"^##[^\n]*[Ww]here it stops[^\n]*$",t,re.M);s=""
    for l in (t[m.end():].split("\n") if m else []):
        if l.startswith("## "):break
        if l.strip() and not l.lstrip().startswith(("```","~~~")):s=l.strip();break
    s=s or "(no where-it-stops line)"
    return "card: "+p+"\nstops: "+(s if len(s)<=WIDTH else s[:WIDTH]+" [cut at %d of %d chars]"%(WIDTH,len(s)))
def texts(path):
    out=[]
    for l in open(path,encoding="utf-8",errors="replace"):
        try:e=json.loads(l)
        except ValueError:continue
        m=e.get("message") if isinstance(e,dict) else None
        if not isinstance(m,dict) or m.get("role")!="assistant":continue
        c=m.get("content");c=[{"type":"text","text":c}] if isinstance(c,str) else c if isinstance(c,list) else []
        s="\n".join(b.get("text","") for b in c if isinstance(b,dict) and b.get("type")=="text")
        if s.strip():out.append((e.get("timestamp",""),s))
    return out
def zones(c):
    z=[0]*len(c);o=[0]*len(c);b=[0];sp={};ps={};red=set();tg={};q="";qs=0;x3=0;H=[];i=0;dep={0:0};cl=set();S=[];dp=0;bq=0
    while i<len(c):
        h=c[i]
        if q:
            z[i]=1;o[i]=b[-1]
            if h==q:
                if x3:z[qs:i+1]=[3]*(i+1-qs)
                q="";x3=0
            elif q=='"' and (c.startswith("$(",i) or h=="`"):x3=1
            elif h=="\\" and q=='"' and i+1<len(c):i+=1;z[i]=1;o[i]=b[-1]
        elif h in "'\"":q=h;qs=i;z[i]=1;o[i]=b[-1]
        elif h=="\\":i+=1
        elif h=="#" and (i==0 or c[i-1] in " \t\n;&|()"):
            while i<len(c) and c[i]!="\n":z[i]=2;i+=1
            continue
        elif c.startswith("<<",i) and not c.startswith("<<<",i) and re.match(r"<<-?[ \t]*(['\"]?)\w+\1",c[i:]):
            m=re.match(r"<<(-?)[ \t]*(['\"]?)(\w+)\2",c[i:]);H.append((m.group(1),m.group(3),m.group(2),b[-1]));i+=len(m.group(0));continue
        elif h=="\n" and H:
            i+=1
            for t,k,qd,w in H:
                st=i
                while i<len(c):
                    n=c.find("\n",i);n=len(c) if n<0 else n;y=c[i:n]
                    if (y.lstrip("\t") if t else y)==k:i=n+1;break
                    z[i:n]=[1]*(n-i);o[i:n]=[w]*(n-i);i=n+1
                if not qd and ("$(" in c[st:i] or "`" in c[st:i]):z[st:i]=[3]*(len(z[st:i]))
            b.append(i);sp[i]="\n";dep[i]=dp;H=[];continue
        elif h in ";&|()`\n":
            if h=="`":bq^=1
            if h=="(" and i and c[i-1] in "$<>" or h=="`" and bq:ps[i+1]=b[-1];dp+=1;S+=[1]*(h=="(")
            elif h=="(":S.append(0)
            elif h==")" and S and S.pop() or h=="`":dp-=1;cl.add(i+1)
            b.append(i+1);sp[i+1]=h;dep[i+1]=dp
        elif h==">" and c[i+1:i+2]!="&":
            red.add(b[-1]);m=re.match(r">>?[ \t]*(['\"]?)([^ \t;&|()<>'\"\n]+)\1",c[i:])
            if m:tg.setdefault(b[-1],set()).add(os.path.basename(m.group(2)))
        i+=1
    E={s:next((x for x in b if x>s and (dep[x]<dep[s] or dep[x]==dep[s] and x not in cl)),len(c)+1) for s in b}
    return None if q else (z,o,b,sp,ps,red,tg,E)
def lead(c,s,b,E):
    n=min([x for x in b if x>s]+[len(c)+1]);w=c[s:min(n-1,len(c))].split()
    while w and (os.path.basename(w[0]) in WRAP or re.match(r"(-\S*|\d+[smhd]?|\w+=\S*)$",w[0])):w.pop(0)
    v=os.path.basename(w[0]) if w else ""
    if v=="git":v="git "+next((x for x in w[1:] if not x.startswith("-")),"")
    return v,E.get(s,n),(w[0] if w else "")
def chain(c,s,b,sp,E):
    P=[s];e=E.get(s,len(c)+1)
    while sp.get(e)=="|" and c[e:e+1]!="|" and c[e-2:e-1]!="|":P.append(e);e=E[e]
    return P
def piped(c,P,b,E):return any(lead(c,x,b,E)[0] not in SAFE for x in P[1:])
def writes(c,s,b,E):
    v=lead(c,s,b,E)[0];w=c[s:E.get(s,len(c)+1)-1].split();w=w[next((k+1 for k,x in enumerate(w) if os.path.basename(x)==v),len(w)):];r=[]
    if v=="tee":return [x for x in w if not x.startswith("-")]
    if v not in ("sort","uniq"):return []
    if v=="uniq":
        k=0
        while k<len(w):x=w[k];k+=1+(x in ("-f","-s","-w"));r+=[x]*(x=="-" or not x.startswith("-"))
        return r[1:2]
    for k,x in enumerate(w):
        m=re.match(r"--output=(.+)|-[A-Za-z]*o(.*)$",x)
        if m or x=="--output":r.append((m and (m.group(1) or m.group(2))) or (w[k+1] if k+1<len(w) else ""))
    return r
def names(c,x,E,tt):t=c[x:E.get(x,len(c)+1)-1];return any(re.search(r"(?<![\w.-])"+re.escape(n)+r"(?![\w.-])",t) for n in tt if n)
def isout(c):
    Z=zones(c)
    tv=".fresh" in c;pp=re.search("ppid",c,re.I)
    if Z is None:return bool(OUT.search(c) or tv and TV.search(c) or pp and KV.search(c))
    z,o,b,sp,ps,red,tg,E=Z
    def ok(s0):
        v=lead(c,s0,b,E)[0];P=chain(c,s0,b,sp,E);Q=P
        tt={os.path.basename(t.strip("'\"")) for s in Q for t in list(tg.get(s,()))+writes(c,s,b,E)}
        return v in SHOW and not piped(c,P,b,E) and not ((tt or any(s in red for s in Q)) and any(lead(c,x,b,E)[0] in RUN or lead(c,x,b,E)[0] not in SHOW and names(c,x,E,tt) for x in b if x>s0 and x not in P)) and (s0 not in ps or ok(ps[s0]))
    for m in list(OUT.finditer(c))+(list(TV.finditer(c)) if tv else [])+(list(KV.finditer(c)) if pp else []):
        i=m.start();k=z[i]
        if k==2:continue
        if k==3 or k==0 and c[i]==">":return True
        if ok(o[i] if k==1 else max(x for x in b if x<=i)):continue
        return True
    return False
def ts(s):
    from datetime import datetime
    try:return datetime.fromisoformat(s.replace("Z","+00:00")).timestamp()
    except Exception:return None
def main():
    v=sys.argv[1] if len(sys.argv)>1 else ""
    if v=="head":
        r=sys.argv[2] if len(sys.argv)>2 else os.path.expanduser("~/t");b=faith(r)
        if not b:warn("moral:faith ### 4.1")
        print("## YOUR FIRST REPLY\n"+FIRST+"\n"+card(r)+"\n\n## THE FOUR PRAYERS\n\n"+b+"\n\nsay one of these in Church Slavonic as your reply's LAST text, no tool call after it: in your first reply, and again before you rotate or go idle; MAY at each idle spot (owner 11-07); never per working turn\n");return
    try:j=json.load(sys.stdin)
    except Exception:warn("hook input")
    if j.get("agent_id"):return
    sid=re.sub(r"[^A-Za-z0-9-]","",str(j.get("session_id") or ""));d=os.path.expanduser("~/.prayed")
    def tr():
        p=j.get("transcript_path")
        if not p or not os.path.isfile(p):warn("no transcript")
        try:return texts(p)
        except OSError:warn("transcript "+p)
    if v=="stop":
        e=os.path.join(d,sid+".end") if sid else ""
        if e and os.path.exists(e):return
        lm=j.get("last_assistant_message")
        if lm is None:T=tr();lm=T[-1][1] if T else ""
        m=bool(sid) and os.path.exists(os.path.join(d,sid))
        if m and prays(block(lm)):
            try:open(e,"w").close()
            except OSError:pass
            return
        if j.get("stop_hook_active"):return
        if sid and not m and prays(lm):
            try:os.makedirs(d,exist_ok=True);open(os.path.join(d,sid),"w").close()
            except OSError:pass
            print(json.dumps({"decision":"block","reason":GO}));return
        if idle(next((l for l in reversed(lm.splitlines()) if l.strip()),"")) and not prays(block(lm)):print(json.dumps({"decision":"block","reason":ASK+" (the session's last tokens: asked until one is said)"}))
        return
    if v!="captive":warn("verb "+v)
    c=str((j.get("tool_input") or {}).get("command") or "");out=isout(c)
    marked=bool(sid) and os.path.exists(os.path.join(d,sid))
    if marked and not out:return
    T=tr()
    if not marked:
        if not any(prays(s) for _,s in T):print(ASK+" (if the rest of the start output was saved to a file, read it in the reply AFTER the prayer)",file=sys.stderr);sys.exit(2)
        if sid:
            try:os.makedirs(d,exist_ok=True);open(os.path.join(d,sid),"w").close()
            except OSError:pass
    if out:
        post=os.environ.get("AGI_POST","")
        if not post:warn("AGI_POST")
        try:k=os.path.getmtime(os.path.join(j.get("cwd") or os.path.expanduser("~/t"),".agi/nodes/doc/card-%s.md"%post))
        except Exception:warn("card write time")
        new=[s for t,s in T if (ts(t) or 0)>=k]
        if not(new and prays(new[-1])):print(ASK+" (the out: the newest reply since the card's last write holds none)",file=sys.stderr);sys.exit(2)
try:main()
except SystemExit:raise
except Exception as e:print("[pray] unread: %s (passed)"%type(e).__name__,file=sys.stderr);sys.exit(0)
~~~

<!-- THOUGHT:BEGIN — authored, not derived; carried across regenerating scans. The reasoning behind THIS version. -->
10-23 V0 (belam, Wave 0 of doc:brainstorm-unify §22, the owner's hand-off): a claude post restarts into ITS OWN session, never `-c`. `claude -c` resumes the newest transcript in the project dir, so at the 03:45Z 10-23 reboot the Fable fork (same home, more recently active) came up AS the Prime. agi-run (2260 B, was 1851) now, for a claude H only, just before the exec: a fresh start mints a uuid and runs `--session-id <uuid>`; any other start runs `--resume <id>` with the id from ~/.session when that transcript exists, else the newest transcript (the old `-c` choice, made once, so the first restart after this lands behaves as before and pins it); no transcript at all keeps `-c`. The id is written to ~/.session (umask 077) every start; a non-hex id is ignored. `c` keeps its meaning (empty = fresh) so the rotation-alert line is unchanged. The project dir is `pwd -P` with every non-alphanumeric byte as `-`, as Claude Code names it. A pi H is untouched (the arm is dormant, N12). Lane session-pin.t.sh.
10-07 goal:g7.16.1.11.20 (director-general-3; lanes DG2 b94a30851 + a1425b7d5 + 32c2f4704a + 1d03ba36cc, box-wake.t.sh, 33 lanes): messaging is box mail, with TWO sources until send.py's callers are on box (DG1 return 17:5xZ: send.py never writes box mail, only the inbox file). agi-run polls BOTH: the inbox file size exactly as the trunk's (claude only; growth types `mail: send.py read $AGI_[retired]`, s=$n every tick; md5-equal to the trunk's line) AND `box n` (claude and pi; growth types `mail: box read`, s starts 0 and follows the count down). cccc.ts keeps its inbox watchFile AND adds ONE box interval (`n>s&&send;s=n`; the pilot's `n>s&&(s=n,...)` only moved s UP, so mail after a read never woke); each source types its OWN line, with separate counters; the ~/o cap loop is KEPT.
SM mur final (DG1 return 19:27Z): the box route could not work live. R6: the unit sets AGI_[retired]=%i ONLY, the box piece needs AGI_POST (`P=${AGI_POST:?}`), so in a real pane `box n` died and the wake never fired while every lane (which exported AGI_POST) was green; both wake pieces now derive it, `AGI_POST=${AGI_POST:-$AGI_[retired]}` in agi-run and `env:{...E,AGI_POST:E.AGI_[retired]||E.AGI_POST}` in cccc.ts (R9 flipped the cccc.ts order, see below). The SENDER side needs AGI_POST too (the unit would set it) but that is a host act, banked, not this leaf. R7: stderr discipline, `2>/dev/null` and `stdio:["ignore","pipe","ignore"]`, so a dead or absent box is silent. N11: the count excludes lines starting with `[` (`[off-matrix]`, `[refused]`, which `box n` prints). A TRAP: `grep -vc` exits 1 on a zero count and execSync throws on a non-zero exit, which skips `s=n` and brings the original bug back (send 1, read, send 1 = no second wake), so the cccc.ts pipeline ends in `||:` (DG2's lanes w4/w4b found it). N10: `.unref()` on the interval, so agi-kid's `pi ... -e cccc.ts -p` can exit once pi drains. N12: agi-project projects `node <P>/pi ...` as H, so the `pi*` arm of agi-run is DORMANT today and the pi route is cccc.ts; lane w8 pins the arm's shape, not the projection. The pure-box cutover is a LATER leaf with belam's GO. Sizes: agi-run 773 B (the trunk header said 501 B; the piece measured 573), cccc.ts 1956 B (trunk 1647). R9 (mur, DG1 order 20:37Z): agi-kid execs pi with AGI_[retired]=$k and INHERITED the post env, so once the unit line AGI_POST=%i landed a kid would poll its PARENT's box, and a kid that obeys `box read` advances the parent's held ref; cccc.ts therefore prefers AGI_[retired] (`AGI_POST:E.AGI_[retired]||E.AGI_POST`, same 1956 B), so a kid's own name wins and matches no ref (`box n` reads 0); a post has both vars = %i, same result. That covered the poll only: a kid's HAND `box read` / `box send` and send.py's sender still resolved AGI_POST = the parent. goal:g7.16.1.11.24 (belam-s2-II 02:4xZ 10-10, laned under the g7.16.1.11 HOLD) therefore TOUCHES agi-kid after all (R9's option b is superseded): it execs with `AGI_[retired]=$k AGI_POST=$k` (2049 B, was 2037), so every identity reader in a kid's env resolves to the KID; cccc.ts keeps AGI_[retired] first and is NOT flipped. The shell wrap line `AGI_POST=${AGI_POST:-$AGI_[retired]}` stays, post-only (a kid never runs the wrap). 10-10 goal:g7.16.1.11.36 (director-general-4, SM 03:0xZ): agi-run (1057 B, was 773) pre-answers Claude Code's one-time "fullscreen renderer" dialog for a claude H only, before the exec: one line sets fullscreenUpsellSeenCount to 3 in ~/.claude.json (jq, tmp + mv, umask 077), idempotent (a count >= 3 is not rewritten), other keys survive, an unparsable file is left alone, never fails the start; lane claude-upsell.t.sh. The key is read from claude 2.1.295 (the leaf's bytes); that a live claude then skips the dialog was NOT measured (a scratch home without auth never reaches it). Prior THOUGHT (v5 rounds 5 and 7: the wrapper pieces, agi-infer, agi-captive, the pane trim loop): grid history. goal:g7.16.1.11.32 (DG1 10-11): agi-run's two remaining loops are `while :;do sleep N||:;` (a killed sleep no longer ends them) and its box-wake loop is gone to agi-boxwake@.service (engine-root.md); the send.py inbox loop stays until goal:g7.16.1.11.27 retires it. goal:g7.16.1.11.20.3 (DG1 10-16, council 3/3, alive [decision] 05:35:44Z): agi-captive (576 B -> 1005 B) is never a lock: with a fill window open it still passes ONLY one agi-fill command, but it RELEASES the window (one `[captive] <path> released: <reason>` stderr line, the window renamed `<path>.released-<UTC>`, kept, rc 0) when agi-fill is not on PATH (it is hub-side, engine-grow.md, so a post's PATH never had it: the gate's only exit was absent) or the window's mtime is older than ${AGI_FILL_WINDOW:-900} s (the lifetime lived only in agi-fill, so a dead session left a lock FOREVER); lane captive-release.t.sh, post-env.t.sh e4 now puts a stub agi-fill on PATH so it still tests the gate that bites.
10-26 the agi-run strand (director-general-2; council [decision] alive 19:32:42Z): the last line was `exec strace`, so the two background loops (pane trim, mail poker) were strace's OWN children. MEASURED on a fixture of the real chain (script -> agi-run -> strace -> a stub claude, scratch HOME): with the -o consumer dead (agi-track killed, or ~/track unwritable as at ENOSPC) the stub exited and strace stayed in do_wait with only the loops left; killing the loops ended it at once, killing the orphan grep/awk did not. So the unit's MainPID outlived claude and no restart came (director-general-3, 19:18Z, in the 19:11-19:13Z full-disk window). Cure by construction: no exec, strace in the foreground, at its exit kill the two loops by the pids captured where they are forked ($L1 $L2; `jobs -p` prints nothing in a non-interactive dash, so an earlier cut of this line killed nothing and the loops ended only by the pty hangup: alive's pre-read 20:25:38Z) and exit with its rc; ~/.fresh is still consumed only at START (line 2). agi-track drains to EOF past a failed append (engine-post.md). Lane agi-run-strand.t.sh.
10-31 U3 (director-goals-1, goal:g7.16.1.11.46.21; council alive [decision] 14:20:53Z, V3, 3/3): agi-kid is renamed agi-in, the ONE kid spawn verb. The `-m` flow arm is byte-equal but for its mktemp guard (re-cut 2). A new `pack` arm writes the capsule's spawn lines through AGI_MF (engine-capsule.md has 75 B of fenced bar left, so only agi-in checks the values). The kid arm takes a CID: capsule verify, then the MANIFEST `pull` (graph|director = the old launch + AGI_CID; none = ONE `pi --no-tools` request in an empty dir; anything else = `unread`, rc 1, 0 launches). Lane: agi-in.t.sh; the agi-kid-flow* ceiling is 3,476 B. Re-cut 1 (alive 14:46:26Z R2, R3): the none arm's mktemp is guarded (`unread: no scratch dir`, rc 1), and --at / --scope refuse any non-hex char. Re-cut 2 (alive 15:12:32Z): the -m flow arm's mktemp is guarded the same way, its line on stderr (rc 1). FIX-FORWARD (L313 trunk red, sp 17:31:00Z): the kid's capsule env is AGI_CID, never AGI_CAPSULE, which every post unit sets to `capsule` for agi-out's share dir; under L313 agi-wt read it as a capsule ref and refused every post's pull, its own card included.
11-05 P0 (director-general-3, goal:g7.16.1.11.46.29; council 3/3 on RE-CUT 2 af4cbdc0cc, alive 08:13:28Z): agi-pray, the session's prayer, is a NEW piece here (head for agi-brief, captive FIRST in agi-captive, stop on the Stop hook); the owner's order 11-01 was a programmatic check that each session starts and ends with a Church Slavonic prayer. The v4 port of agi-brief had dropped the prayers (belam's measure). Marker first, a subagent (agent_id) never captive, the Stop check once per session, everything unread fail-open. This touch: the out is matched in every spelling a shell runs (a quoted or braced $PPID, kill's -s SIG, -SIG and --, a quoted ~ / $HOME / ${HOME} .fresh), not two (alive's item 3).
11-05 P0.1 (director-general-3, goal:g7.16.1.11.46.29.1; council alive [decision] 11:11:04Z, 3/3, on aio's L354 live finding): a prayer said beside a tool call can be missing from the transcript when the captive reads it (aio: dropped, 3 of 4 texts; sp: a lag, kept but written after the check), so a fresh post stayed captive until a turn ended on a prayer. The ASK now names the form that holds under both shapes (the prayer as a reply's LAST text, no tool call after it: the turn ends) and says nothing was lost (a kept prayer releases at the next call). The Stop check, in an UNMARKED session, reads the reply-final text and, if it prays, marks the session and blocks ONCE with GO ('prayed: the captive is released; continue your work'), which is what resumes the post with no outside input (sp's term). RE-CUT 1 (sp RETURN 12:03:49Z on d): the first cut gated this on a prior refusal (~/.prayed/<session>.asked), which stalled exactly the post that obeyed the interim line (prayer as the first reply's last text, no tool call, so never refused); the gate is gone, and the mark still holds it to once per session. The shape that resumes where it may not be wanted, named: an unmarked session (no tool call yet) that ends on a prayer while going idle gets ONE GO, then is marked. The out (RE-CUT 1, aio RETURN 11:59:57Z + 12:01:27Z, alive 12:02:31Z: no command the L358 search refuses may pass): the first cut matched the out only at a segment start, which failed OPEN on a heredoc body holding one apostrophe (the quote swallowed every later separator) and on an unknown leading word (if/then, a brace group, sudo...). Built now FROM the L358 whole search (OUT, widened to kill -n N and a TAB): zones() marks quoted spans and heredoc bodies (<<[-]WORD, quoted or not, to its WORD line) with the segment that CONSUMES them, and # comments. RE-CUT 2 (aio RETURN 12:09:41Z on RE-CUT 1: a quoted span or heredoc body handed to a shell RUNS: sh -c, bash -c, eval, sh <<EOF, awk system(), sed e): a match is exempt only in a comment, or when its consumer leads, past WRAP words (env timeout nohup nice time sudo command exec builtin, options, numbers, VAR=), with a printer (SHOW: echo printf grep egrep fgrep rg jq cat head tail less wc sort, git log/grep/show/diff; awk and sed are OUT, they execute) that is not piped into a RUN word (sh bash dash zsh ksh xargs eval source .); $( ) or backticks inside double quotes or an unquoted heredoc body run, so never exempt, and a bare backtick is a segment boundary like ( (RE-CUT 3, aio 12:15:03Z + sp 12:11:20Z clause (4): echo `kill $PPID` passed RE-CUT 2); RE-CUT 4 (sp 12:15:41Z (3') and (5)): a printer inside a process substitution <( ) whose consumer leads with a RUN word loses its exemption (sh <(echo kill $PPID)), and so does a printer with an output redirect (>, >>, | tee) when a LATER segment of the same command leads with a RUN word (echo kill $PPID > x.sh; sh x.sh); a script written in one call and run in a later one stays out of reach (both matchers pass it); NEXT TOUCH (alive 13:28:47Z, on r4 approved for L363): a redirect's target (basename) is recorded, and a later segment whose lead word (past WRAP) is that file loses the printer its exemption (echo kill $PPID > x.sh; chmod +x x.sh; ./x.sh), and a pipe keeps the exemption only into SAFE (SHOW + tee cut tr uniq nl fold column), so busybox sh, python3 -c, at now lose it, and (alive 17:42:51Z) EVERY later segment of the pipeline must be SAFE: echo kill $PPID | head -1 | sh loses it too; an unknown leading word is the out; a command left inside an open quote is searched whole (fail closed). A false refusal (python3 - <<EOF naming the out, sed '/.../p') costs one prayer, as agreed. Reading tool_use inputs as prayers is NOT built (sp: a command naming a prayer word would pass). NEXT TOUCH 2 (director-general-3 gen 25, on L388; alive 17:57:11Z (1)-(2), sp 19:48:23Z (3), all three read on r4 + L388 as passing shapes that RUN): (1) a printer's targets are every file its PIPELINE writes (> or tee on any segment: echo kill $PPID | head -1 > x.sh; sh x.sh); (2) a printer inside an unquoted $( ), backtick pair or <( ) keeps the exemption only when the ENCLOSING segment would itself pass (recursive), and a segment now ends PAST any substitution inside it (a depth per boundary), so $(echo kill $PPID), eval $( ), cat <( ) | sh and a pipe after a substitution lose it; (3) a SAFE filter's own write (sort -o / --output, uniq's OUT) is a target, and a later segment that names a target ANYWHERE in its words loses it unless it leads with a printer (awk system(), python3 os.system, find -exec; cat x.sh stays a read). diff joins SHOW so c12's diff <( ) read still passes under (2). Probe old vs new over 48 shapes: 0 wrong, the 17 changed are exactly the new refusals, 0 reads flipped. NEXT TOUCH 3 (director-general-3 gen 25, on L389; alive 20:42:31Z NOTE, sp AGREE 20:43:31Z): OUT read the out only by its LITERAL text, so a pid reached by eval, a variable or a substitution never met the captive (eval "kill \$PPID"; P=$PPID; kill $P; kill $(echo $PPID); kill with backticks). Now a kill whose operand is an EXPANSION ($var, ${var}, $( ), backticks, an escaped \$) is the out; not alive's wider 'any non-literal-number target', because a bare word (git commit -m "kill the lane") would then be refused too; $!, $$ (the tool shell's own), kill -0 / -s 0 (no signal), a number and %job stay free. The touch half: a touch whose operand is an expansion when .fresh is named anywhere in the command (TV), and an unquoted redirect into ~/.fresh, never exempt by its printer. Not covered, named: cd ~ then touch .fresh; a pid read from a file in an earlier call into a literal number. 34 more shapes probed (12 changed, all the new refusals; 0 reads flipped); the 48 above unchanged. RE-CUT 1 (alive 21:19:11Z RETURN, option D, SM prefers it over its own A): SM measured the cost at 21:17Z, a post's own stop by pid in a variable ([ -n "$P" ] && kill $P after pgrep; agi-memory-guard's stop by pid, agi-master-gate's kill $timeout_pid) captive until a prayer, i.e. a stop of a runaway waiting a turn and a prayer outside the owner's two spots. So the expansion kill (KV) is the out only when the command's TEXT names ppid, in any case, the same move as TV's '.fresh named': every PPID-reaching shape stays refused (P=$(ps -o ppid= $$); kill $P too), the taught stops pass with no skill edit; self-perpetuating 21:21:29Z pinned the name test by rows (c27: SM's two stops + both skill shapes pass) and three mutants, each RED on a named row (no name test, a case-sensitive one, one read on the kill's own segment), none equivalent. Uncovered, named, and the matcher stops here (alive: each touch is paid at someone's stop): a pid reached without naming ppid (pgrep -f claude; a number read in an earlier call); a pid fed by stdin (echo $PPID | xargs kill, xargs kill <<< $PPID); ~/.fresh made by a non-touch writer (cp /dev/null, ln -s, mkdir, tee ~/.fresh); cd ~ then touch .fresh. 5855 -> 10777 -> 12097 -> 12894 B.
11-07 P0.2 (director-general-3 gen 25, goal:g7.16.1.11.46.29.2; alive [decision] 18:16:50Z 11-05 (B) as amended 18:27:38Z; belam's [finding] 17:51:36Z 11-05: a 17.5 KB brief, a ~2 KB inline preview, the card and the 'first reply' ask outside it): agi-pray head prints a HEAD ABOVE the prayer block, '## YOUR FIRST REPLY', then FIRST (the reply-final ask in the captive's own words: as your reply's LAST text, no tool call after it, that ENDS the turn; then read your card), then `card: PATH` and `stops: ` + the card's where-it-stops first line cut to WIDTH = 120 chars and named ('[cut at 120 of N chars]'), or ONE `card unread: PATH` line. The unit is the harness preview, the text up to the last newline before 2000 CHARACTERS: measured on a fixture post, the head is 300 chars and the Jesus Prayer ends at char 1832; a real card path and a full 120-char stops line add about 130, still inside, so the whole Jesus Prayer line sits in the preview (h5), also with a 778-char where-it-stops line (h6; the no-width-cap mutant pushes it out). The block's closing line says the reply-final form, never 'first tokens of your first reply' (h8). The prayer block stays whole and is the first BLOCK after the head: that amends the parent's term a for the head only (council wording; the owner's words ask that each session starts and ends with a prayer, the post's own text); the parent's term a and falsifier 2 carry a pointer. RE-CUT 1 (sanctuary-master 00:02Z 11-07, reading 1, measured over the 24 cards): 4 cards open where-it-stops with a code fence, so stops read a bare fence; the reader now takes the section's first line that is neither blank nor a fence (``` / ~~~), and stops at the next ## heading: 22 cards read a real line, 2 have no heading (as built). 12894 -> 13941 B.
11-07 P0.3 (director-general-3 gen 26, goal:g7.16.1.11.46.29.3; alive [decision] 04:13:28Z 11-07, (P) with three terms, 3/3; it corrects alive's 03:07:52Z (2), which put the start's words into ASK): seven wakes, one act (each a read of the harness-saved SessionStart output BEFORE the prayer, 1 refusal, then the prayer alone), because FIRST and ASK forbade a tool call AFTER the prayer and none BEFORE it. FIRST (the head only) = 'your FIRST reply is ONE prayer below and nothing else: no tool call before or after it (that ENDS the turn); if the rest of this output was saved to a file, read it in your NEXT reply, then read your card'. ASK (all three uses: the Stop, the start captive, the out) keeps the owner's opening 'captive: say an Old Slavonic protection prayer before proceeding' and says 'your next reply is that prayer and nothing else: no tool call before or after it', with no 'FIRST', no 'below', no saved file. The saved-file clause is a suffix on the start captive's print ONLY: ' (if the rest of the start output was saved to a file, read it in the reply AFTER the prayer)'. The head's closing line (say one of these ... as your reply's LAST text, no tool call after it) is LEFT as is: true at the close and printed past the preview. agi-pray 13941 -> 14137 B.
11-07 P0.4 (director-general-3 gen 27, goal:g7.16.1.11.46.29.4; alive [decision] 04:49:43Z 11-07, (S) with three terms, 3/3: self-perpetuating 04:46:22Z, all-is-one 04:48:26Z AMEND of TERM 1's cut, SM SUPPORT + its no-state row): the Stop branch is rebuilt so the session's close is read from its prayer, not its wording. TERM 1: the STAMP runs first, ahead of stop_hook_active and of the idle test: in a marked session (~/.prayed/<sid> present) a last reply whose TRAILING PRAYER BLOCK prays stamps .end and returns. The block (all-is-one's cut): walk back from the reply's end over every line that is blank or markup only (whitespace and > * _ ~ -) or holds Cyrillic with NO Latin letter; stop at the first other line; prays() over that block. A whole-reply prays() stamped on a prayer quoted mid-reply (sp); the last line misses the Lord's Prayer (its last line holds no key); the last paragraph misses the Lord's Prayer set one line per paragraph and stamps on a plain last line holding one prayer word (m41 reds both). (S)(2): .end is stamped only on a prayer, never on the ask; the idle test only ASKS, and a false ask leaves no state (SM's row r8), so an idle reply with no prayer is asked once per Stop chain until a close prayer is said (the ASK suffix says so: 'asked until one is said', was 'asked once per session'); the earlier-idle-reply-that-prayed read (T[:-1]) is gone with it: .end is the only memory. TERM 2: the idle test reads the last non-empty LINE; a negation (not, n't, never, no longer) within the three words before a match, with no clause mark (, ; : . or a dash) between, spares that match; the line asks when any match is unspared. Accepted residual (sp): 'I am not, however, going idle.' asks (r10; one block, no .end). TERM 3 / (S)(3): NO lapse: once a close prayer is read the Stop is closed for the session, later work ends at the out (:315 unchanged); start + a close at a mail wait + the out = THREE prayers (r4). Whether a session woken after a close owes its out a third prayer is the owner's reading of 09-12, banked on alive's §6; the leaf is built as (S) meanwhile. The unmarked resume (.46.29.1, GO) is unchanged and still reads the whole reply, so a start prayer never stamps .end (the stamp needs the marker). Named residual: a session that never ran a tool call (unmarked) and closes on a prayer gets GO, not .end, so its next idle reply is asked once more. Rows r0-r10 on the built piece; m40 = today's Stop branch (40a15f0c09) RED on r1 r2 r3 r4 r5 r8 r9; m41 last paragraph, m42 no clause-mark test, m43 the stamp behind stop_hook_active, m44 no denial guard, each RED on its row. p3 puts its prayer on its own line, p5/p6 now read (S) (p6 was asks-once-per-session), m3 (the once-per-session read) is gone with its lines. agi-pray 14137 -> 14819 B.
11-07 P0.5 (director-general-3 gen 27, goal:g7.16.1.11.46.29's next touch; alive [decision] 06:51:50Z, 3/3, on the owner's c:c91f4ca10325 06:33:17Z 'Yes it can do it repeatedly each "idle" spot'): 'can' = ALLOWED, text only, no behaviour change. agi-pray's :2 comment and the head's closing line drop 'two spots, never per turn' for '; MAY at each idle spot (owner 11-07); never per working turn'. The Stop (L409) already passes a prayer at any idle spot and asks only until the first praying close: nothing in the code changes. agi-pray 14819 -> 14886 B.
<!-- THOUGHT:END -->
