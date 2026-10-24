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
agi-run           2260 B  pane cmd: fresh=new id, else --resume ~/.session
settings.json      372 B  the ONE hook wiring: brief, meter, turn commit
cccc.ts           1913 B  pi events -> the CC hooks; mail -> a turn
agi-kid           2037 B  a pi-free kid in this unit: own HOME and tree
agi-infer          1332 B  ONE chat call, OpenAI-compatible: stdin -> stdout
agi-lane           1403 B  a Console lane's pi / claude -p / header config
agi-captive        1005 B  window open: only agi-fill; a dead window: released
~~~

## files — depth 2, each whole; extract: sect <name> [REV]

### agi-run (2260 B)
~~~sh
#!/bin/sh
cd ~/t;c=-c;[ -e ~/.fresh ]&&rm ~/.fresh&&c=;stty cols 200 rows 50;i=$RUNTIME_DIRECTORY/i;f=$O/.agi/sessions/inbox/$AGI_POST.md
(while :;do sleep 300||:;m=$((${AGI_PANE_MAX_MB:-64}<<20));[ $(stat -c%s ~/o 2>/dev/null||echo 0) -gt $m ]&&tail -c $((m/2)) ~/o>~/o.t&&cat ~/o.t>~/o;rm -f ~/o.t;done)&
case $H in claude*)(s=$(stat -c%s $f 2>/dev/null||echo 0);while :;do sleep 5||:;n=$(stat -c%s $f 2>/dev/null||echo 0);[ $n -gt $s ]&&printf "mail: send.py read $AGI_POST">$i&&sleep 1&&printf '\r'>$i;s=$n;done)&;;esac
case $H in claude*)(umask 077;j=~/.claude.json;n=$j.n;jq -e '((.fullscreenUpsellSeenCount//0)|numbers)>=3' $j>/dev/null 2>&1||{ if [ -e $j ];then jq '.fullscreenUpsellSeenCount=3' $j;else echo '{"fullscreenUpsellSeenCount":3}';fi>$n 2>/dev/null&&[ -s $n ]&&mv $n $j;rm -f $n;});;esac
[ -z "$c" ]&&(p=$AGI_POST;r=$(git show ${AGI_TRUNK:-HEAD}:.agi/nodes/.geometry/rotations.md 2>/dev/null|awk -v p=$p '/^---$/{if(++n>1)exit;next}n!=1||/^[ ]*(#.*)?$/{next}/^alerts:[ ]*$/{a=s=1;next}/^[^ ]/{a=0}!a{next}/^  (audit|silent):[ ]*$/{k=$1;sub(/:/,"",k);m="l";next}/^  edges:[ ]*\{\}[ ]*$/{m="";next}/^  edges:[ ]*$/{m="e";next}m=="l"&&/^    - [a-z][a-z0-9-]*[ ]*$/{L[k]=L[k]" "$2;next}m=="e"&&/^    [a-z][a-z0-9-]*:[ ]*$/{e=$1;sub(/:/,"",e);next}m=="e"&&/^      - [a-z][a-z0-9-]*[ ]*$/{if(e==p)E=E" "$2;next}{b=1}END{if(!s||b)exit 1;n=split(L["audit"]E,w," ");z=split(L["silent"],y," ");for(i=1;i<=z;i++)S[y[i]];S[p];for(i=1;i<=n;i++)if(!(w[i] in S)){S[w[i]];print w[i]}}')||echo "warn: rotation alert: alerts cell unreadable, nothing sent" >&2;[ -n "$r" ]&&timeout -k 2 20 sh -c 'for x in $0;do printf "[rotation-alert] $1 restarted fresh $(date -u +%FT%TZ)\n"|AGI_POST=$1 box send $x||echo "warn: rotation alert to $x failed" >&2;done' "$r" $p)2>>$RUNTIME_DIRECTORY/alert&
case $H in claude*)d=~/.claude/projects/$(pwd -P|sed 's/[^A-Za-z0-9]/-/g');if [ -z "$c" ];then s=$(cat /proc/sys/kernel/random/uuid);c="--session-id $s";else s=$(cat ~/.session 2>/dev/null);case $s in *[!0-9a-f-]*)s=;;esac;[ -n "$s" ]&&[ -s "$d/$s.jsonl" ]||s=$(ls -t "$d"/*.jsonl 2>/dev/null|sed -n '1s|.*/||;1s|\.jsonl$||p');[ -n "$s" ]&&c="--resume $s";fi;[ -n "$s" ]&&(umask 077;echo $s>~/.session);;esac
exec strace -qqf -b execve -e%file -o'|agi-track' $H $c go
~~~

### settings.json (372 B)
~~~json
{"skipDangerousModePermissionPrompt":true,"tui":"default","hooks":{"PreToolUse":[{"hooks":[{"type":"command","command":"agi-captive"}]}],"SessionStart":[{"hooks":[{"type":"command","command":"agi-brief","timeout":180}]}],"UserPromptSubmit":[{"hooks":[{"type":"command","command":"agi-meter"}]}],"Stop":[{"hooks":[{"type":"command","command":"agi-turn","timeout":180}]}]}}
~~~

### cccc.ts (1913 B)
~~~ts
import{execSync as x}from"node:child_process";import{readFileSync as R,watchFile as W,unwatchFile as U}from"node:fs"
const E=process.env,H=JSON.parse(R(E.HOME+"/.claude/settings.json","utf8")).hooks,N={bash:"Bash",read:"Read",edit:"Edit",write:"Write"};let b="",v
const h=(n,j={})=>{let o="",k=0;for(const g of H[n]||[])if(!g.matcher||RegExp(g.matcher).test(j.tool_name))for(const c of g.hooks)try{o+=x(c.command,{input:JSON.stringify({hook_event_name:n,cwd:process.cwd(),...j}),encoding:"utf8",stdio:"pipe",timeout:(c.timeout||60)*1e3})}catch(e){if(e.status==2)k=2,o+=e.stderr}return{o,k}}
const t=e=>({tool_name:N[e.toolName]||e.toolName,tool_input:e.input}),S=s=>{b=h("SessionStart",{source:s}).o}
export default p=>{const on=(e,f)=>p.on(e,f);on("session_start",e=>{S({new:"clear",fork:"resume",reload:"resume"}[e.reason]||e.reason)
const f=`${E.O}/.agi/sessions/inbox/${E.AGI_POST}.md`;U(f);W(f,{interval:5e3,persistent:!1},(n,o)=>n.size>o.size&&p.sendUserMessage("mail: send.py read "+E.AGI_POST,{deliverAs:"followUp"}))
let s=0;clearInterval(v);v=setInterval(()=>{try{const n=+x("box n 2>/dev/null|grep -vc '^\\['||:",{encoding:"utf8",stdio:["ignore","pipe","ignore"]}).trim();n>s&&p.sendUserMessage("mail: box read",{deliverAs:"followUp"});s=n}catch{}},5e3).unref()})
on("session_compact",()=>S("compact"));on("before_agent_start",e=>b&&{systemPrompt:e.systemPrompt+"\n\n"+b})
on("input",(e,c)=>{const u=c.getContextUsage()||{},r=h("UserPromptSubmit",{prompt:e.text,tokens:u.tokens,context_window:u.contextWindow});return r.k?{action:"handled"}:r.o&&{action:"transform",text:e.text+"\n\n"+r.o}})
on("tool_call",e=>{const r=h("PreToolUse",t(e));return r.k&&{block:true,reason:r.o}});on("tool_result",e=>{h("PostToolUse",t(e))})
on("session_before_compact",()=>{h("PreCompact",{trigger:"auto"})});on("turn_end",()=>{h("Stop")});on("session_shutdown",()=>{clearInterval(v);h("SessionEnd",{reason:"other"})})}
~~~

### agi-kid (2037 B)
~~~sh
#!/bin/sh
K="--provider openrouter --model $AGI_KID_MODEL"
if [ "$1" = -m ];then M=$2;A=$3;P=;d=;case $M in *[!a-z0-9-]*)exit 1;;esac;cd ~/t;s=$(printf %s "$A"|sha256sum|cut -c1-12);D=~/s/$M/$s;R=refs/spawn/$M/$s
git show-ref --verify -q $R&&exit
n(){ echo $D/o.$(printf %s "$P$1"|tr -c 'A-Za-z0-9._:-' _);}
st(){ case .$2.$3.$4 in *.-*|*[!a-z0-9.-]*)exit 75;;esac;case $6 in [-@]*)exit 75;;esac;o=$(n "$1")
 if [ "$2" ];then [ "$V" ]&&return;q=$(git show HEAD:.agi/nodes/goal/$3.md|sed -n '/^## Falsifier/,/^## /s/^\$ //p'|head -1)
  printf %s "$q"|grep -Eq '^(grep|test|ls|git (rev-parse|ls-files|for-each-ref)) [^;&|<>`$()\\]*$'&&timeout 30 sh -c "$q"</dev/null>/dev/null||{ [ -e $o.h ]||{ m="handoff $M $1 $3";echo "$m"|box send "$2" "$m"&&:>$o.h;};exit 75;}
 elif [ "$4" ];then [ ${#d} -lt 2 ]&&(P=$P$1/;d=$d.;fl $4)||exit $?
 elif [ ! -f $o -a -z "$V" ];then r=$6;[ "$5" ]&&{ b=$(n "$5");[ -f $b ]||b=$(n "$5:$7");r="$r
$(cat $b)"||exit 1;};W=$(mktemp -d);git archive HEAD|tar -xC $W
  (cd $W;HOME=$W pi $K -p "$r"</dev/null>$o.t)||{ rm -rf $W $o.t;exit 1;};rm -rf $W;mv $o.t $o;fi;}
fl(){ x=$(git show HEAD:extensions/agi/workflows/$1.json|jq -r --argjson a "$A" '.stages as $S|range($S|length)as $i|$S[$i]|.chained_from as $c|(if .repeat then ($a[.repeat.of]|arrays//error)[].key else "" end) as $k|(if $c and([$S[:$i][].label]|index($c)|not)then error end|"st ")+([(.repeat.label_template//.label),(.post,.goal,.flow,$c,.prompt|.//""),$k]|map(gsub("\\{key\\}";$k))|@sh)')&&[ "$x" ]||exit 1;mkdir -p $D;eval "$x";}
V=1;fl $M;V=;fl $M;(export GIT_DIR=$PWD/.git GIT_WORK_TREE=$D GIT_INDEX_FILE=$(mktemp -u);cd $D&&git add -A&&git update-ref $R $(git commit-tree -S -m $s $(git write-tree)));exit $?;fi
k=$1;shift;h=~/k/$k;mkdir -p $h/.claude;cd ~/t;[ -d $h/t ]||git worktree add -q $h/t -b kids/$k
for x in .gitconfig .ssh hooks .claude/settings.json;do ln -sfn ~/$x $h/$x;done
cd $h/t;HOME=$h AGI_POST=$k AGI_ROLE=kid AGI_HARNESS=pi-free AGI_WT=$RUNTIME_DIRECTORY/k-$k exec pi $K --skill skills -e ~/bin/cccc.ts -p "$*"</dev/null
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

### agi-captive (1005 B)
~~~sh
#!/bin/sh
# PreToolUse while a fill window is open: ONLY ONE agi-fill command passes (no chaining, no substitution; the quoted heredoc is the way to send text); exit 2 = refused (claude natively; pi through cccc.ts). A window that cannot be used is RELEASED, never a lock (agi-fill absent, or older than ${AGI_FILL_WINDOW:-900} s)
w=${AGI_FILL:-$HOME/.fill};[ -e "$w" ]||exit 0;command -v agi-fill >/dev/null||r="agi-fill not on PATH (engine defect)";m=$(stat -c %Y "$w" 2>/dev/null);[ $(($(date +%s)-${m:-0})) -gt ${AGI_FILL_WINDOW:-900} ]&&r=${r:-window expired}
[ -z "$r" ]||{ echo "[captive] $w released: $r" >&2;mv "$w" "$w.released-$(date -u +%Y%m%dT%H%M%SZ)" 2>/dev/null;exit 0;}
jq -r '.tool_input.command//""'|awk 'NR==1{f=$0}{n++}$0=="EOF"{e++;l=n}END{exit!((f~/^agi-fill (call|row) <<\047EOF\047$/&&e==1&&l==n)||(n==1&&f~/^agi-fill (open|call|row|close|check)( [^;&|`$()<>\\]*)?$/))}'&&exit 0;echo "captive: a fill window is open -- ONE agi-fill call | row | close, nothing chained" >&2;exit 2
~~~

<!-- THOUGHT:BEGIN — authored, not derived; carried across regenerating scans. The reasoning behind THIS version. -->
10-23 V0 (belam, Wave 0 of doc:brainstorm-unify §22, the owner's hand-off): a claude post restarts into ITS OWN session, never `-c`. `claude -c` resumes the newest transcript in the project dir, so at the 03:45Z 10-23 reboot the Fable fork (same home, more recently active) came up AS the Prime. agi-run (2260 B, was 1851) now, for a claude H only, just before the exec: a fresh start mints a uuid and runs `--session-id <uuid>`; any other start runs `--resume <id>` with the id from ~/.session when that transcript exists, else the newest transcript (the old `-c` choice, made once, so the first restart after this lands behaves as before and pins it); no transcript at all keeps `-c`. The id is written to ~/.session (umask 077) every start; a non-hex id is ignored. `c` keeps its meaning (empty = fresh) so the rotation-alert line is unchanged. The project dir is `pwd -P` with every non-alphanumeric byte as `-`, as Claude Code names it. A pi H is untouched (the arm is dormant, N12). Lane session-pin.t.sh.
10-07 goal:g7.16.1.11.20 (director-general-3; lanes DG2 b94a30851 + a1425b7d5 + 32c2f4704a + 1d03ba36cc, box-wake.t.sh, 33 lanes): messaging is box mail, with TWO sources until send.py's callers are on box (DG1 return 17:5xZ: send.py never writes box mail, only the inbox file). agi-run polls BOTH: the inbox file size exactly as the trunk's (claude only; growth types `mail: send.py read $AGI_[retired]`, s=$n every tick; md5-equal to the trunk's line) AND `box n` (claude and pi; growth types `mail: box read`, s starts 0 and follows the count down). cccc.ts keeps its inbox watchFile AND adds ONE box interval (`n>s&&send;s=n`; the pilot's `n>s&&(s=n,...)` only moved s UP, so mail after a read never woke); each source types its OWN line, with separate counters; the ~/o cap loop is KEPT.
SM mur final (DG1 return 19:27Z): the box route could not work live. R6: the unit sets AGI_[retired]=%i ONLY, the box piece needs AGI_POST (`P=${AGI_POST:?}`), so in a real pane `box n` died and the wake never fired while every lane (which exported AGI_POST) was green; both wake pieces now derive it, `AGI_POST=${AGI_POST:-$AGI_[retired]}` in agi-run and `env:{...E,AGI_POST:E.AGI_[retired]||E.AGI_POST}` in cccc.ts (R9 flipped the cccc.ts order, see below). The SENDER side needs AGI_POST too (the unit would set it) but that is a host act, banked, not this leaf. R7: stderr discipline, `2>/dev/null` and `stdio:["ignore","pipe","ignore"]`, so a dead or absent box is silent. N11: the count excludes lines starting with `[` (`[off-matrix]`, `[refused]`, which `box n` prints). A TRAP: `grep -vc` exits 1 on a zero count and execSync throws on a non-zero exit, which skips `s=n` and brings the original bug back (send 1, read, send 1 = no second wake), so the cccc.ts pipeline ends in `||:` (DG2's lanes w4/w4b found it). N10: `.unref()` on the interval, so agi-kid's `pi ... -e cccc.ts -p` can exit once pi drains. N12: agi-project projects `node <P>/pi ...` as H, so the `pi*` arm of agi-run is DORMANT today and the pi route is cccc.ts; lane w8 pins the arm's shape, not the projection. The pure-box cutover is a LATER leaf with belam's GO. Sizes: agi-run 773 B (the trunk header said 501 B; the piece measured 573), cccc.ts 1956 B (trunk 1647). R9 (mur, DG1 order 20:37Z): agi-kid execs pi with AGI_[retired]=$k and INHERITED the post env, so once the unit line AGI_POST=%i landed a kid would poll its PARENT's box, and a kid that obeys `box read` advances the parent's held ref; cccc.ts therefore prefers AGI_[retired] (`AGI_POST:E.AGI_[retired]||E.AGI_POST`, same 1956 B), so a kid's own name wins and matches no ref (`box n` reads 0); a post has both vars = %i, same result. That covered the poll only: a kid's HAND `box read` / `box send` and send.py's sender still resolved AGI_POST = the parent. goal:g7.16.1.11.24 (belam-s2-II 02:4xZ 10-10, laned under the g7.16.1.11 HOLD) therefore TOUCHES agi-kid after all (R9's option b is superseded): it execs with `AGI_[retired]=$k AGI_POST=$k` (2049 B, was 2037), so every identity reader in a kid's env resolves to the KID; cccc.ts keeps AGI_[retired] first and is NOT flipped. The shell wrap line `AGI_POST=${AGI_POST:-$AGI_[retired]}` stays, post-only (a kid never runs the wrap). 10-10 goal:g7.16.1.11.36 (director-general-4, SM 03:0xZ): agi-run (1057 B, was 773) pre-answers Claude Code's one-time "fullscreen renderer" dialog for a claude H only, before the exec: one line sets fullscreenUpsellSeenCount to 3 in ~/.claude.json (jq, tmp + mv, umask 077), idempotent (a count >= 3 is not rewritten), other keys survive, an unparsable file is left alone, never fails the start; lane claude-upsell.t.sh. The key is read from claude 2.1.295 (the leaf's bytes); that a live claude then skips the dialog was NOT measured (a scratch home without auth never reaches it). Prior THOUGHT (v5 rounds 5 and 7: the wrapper pieces, agi-infer, agi-captive, the pane trim loop): grid history. goal:g7.16.1.11.32 (DG1 10-11): agi-run's two remaining loops are `while :;do sleep N||:;` (a killed sleep no longer ends them) and its box-wake loop is gone to agi-boxwake@.service (engine-root.md); the send.py inbox loop stays until goal:g7.16.1.11.27 retires it. goal:g7.16.1.11.20.3 (DG1 10-16, council 3/3, alive [decision] 05:35:44Z): agi-captive (576 B -> 1005 B) is never a lock: with a fill window open it still passes ONLY one agi-fill command, but it RELEASES the window (one `[captive] <path> released: <reason>` stderr line, the window renamed `<path>.released-<UTC>`, kept, rc 0) when agi-fill is not on PATH (it is hub-side, engine-grow.md, so a post's PATH never had it: the gate's only exit was absent) or the window's mtime is older than ${AGI_FILL_WINDOW:-900} s (the lifetime lived only in agi-fill, so a dead session left a lock FOREVER); lane captive-release.t.sh, post-env.t.sh e4 now puts a stub agi-fill on PATH so it still tests the gate that bites.
<!-- THOUGHT:END -->
