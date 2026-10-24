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

## pieces — depth 1, one line each (bytes on disk)
~~~
agi-brief         1369 B  walk card+seeds+claims; record; STARTUP
brief.py           810 B  the complex walk over parents: edges
agi-meter          829 B  past rotate_pct: out-line; tap chat; read: atomize
agi-at            1129 B  signed CAS commit of ~/t paths to posts/<P>
agi-atomize       3971 B  box mail -> verbatim card atoms (wake path, model)
agi-mem           10791 B  chat tap -> own 0700 store; tap, at
agi-atom          8072 B  card §7 atoms: add close move (verbatim slices)
grow.py           5140 B  the growth-order check both writers call
agi-turn           4615 B  a signed commit per changed node tree
agi-wt            1506 B  a node's tiny RAM tree: pull; drop = turn + purge
agi-track           89 B  strace sink: each path once
agi-flush           942 B  drop trees, turn (its agi-sync merges)
agi-sync           2579 B  merge the trunk each turn; a conflict said by name
agi-out           3357 B  the out-line: next keys, ring commit, re-wrap, swap
gitconfig          196 B  signed commits against root's allowed_signers
pre-commit          639 B  refuses a plain commit on a detached ~/t
agi-notice          1141 B  engine->post notices: add / claim + print
reference-transaction 1338 B  refuses a post moving a peer's ref (a mistake guard)
sysusers.conf       41 B  a post = one user in group agi
agi.rules          242 B  a post starts only its OWN unit
project.sh         161 B  what the body SHOULD be
observe.sh         255 B  what the body IS
tick.sh            254 B  diff them; start own unit; commit
agi-frontier       460 B  each active goal runs its falsifier
agi-first-start  1394 B  pieces BASE..TIP changes: a post's next-start diff
box               2904 B  mail: signed ref per send; belam's town blast
~~~

## files — depth 2, each whole; extract: sect <name> [REV]

### agi-brief (1369 B)
~~~sh
#!/bin/sh
ls ~/.notice* >/dev/null 2>&1&&agi-notice;p=$AGI_POST;cd ~/t;s=$(jq -r .source);case $AGI_HARNESS in pi*)B=${B:-40000};;esac
sect brief.py|python3 - .agi/nodes doc:card-$p,$AGI_SEEDS$(find $(git rev-parse --git-common-dir)/refs/claims -user $USER -printf ,%f 2>/dev/null) ${K:-20}>~/.brief;cat ~/.brief;cut -d' ' -f4 ~/.brief|xargs tail -n+1|head -c ${B:-0}
w=${AGI_WT:-$RUNTIME_DIRECTORY/wt};x=$(git rev-parse -q --verify refs/heads/posts/${AGI_POST:-$p});for r in $(git for-each-ref --format='%(refname)' refs/archive/${AGI_POST:-$p});do git log --format=%s $r ${x:+--not $x}|grep -q '^[^ ]*: kept '&&echo "[kept] $r: a stop left this tree whole; recover it, then git update-ref -d it";done;ls -d $w/*/ 2>/dev/null|sed 's/^/[tree] /';agi-mem at
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

### agi-meter (829 B)
~~~sh
#!/bin/sh
ls ~/.notice* >/dev/null 2>&1&&agi-notice;j=$(cat);t=$(echo "$j"|jq '.tokens//empty');[ "$t" ]||t=$(echo "$j"|jq -r .transcript_path|xargs tac 2>/dev/null|jq -nR 'first(inputs|fromjson?|select((.message.usage.input_tokens)?|type=="number")|.message.usage|.input_tokens+((.cache_read_input_tokens|numbers)//0)+((.cache_creation_input_tokens|numbers)//0))');w=$(echo "$j"|jq ".context_window//${AGI_WINDOW:-1000000}")
printf %s "$j"|agi-mem tap 2>/dev/null;case $(echo "$j"|jq -r '.prompt//empty') in "mail: box read"*)agi-atomize wake||echo "[atomize] wake rc=$?: no atoms this read (~/.atomize.log); the next read retries";;esac
[ "${t:-0}" -gt $((w*${AGI_ROTATE_PCT:-47}/100)) ] 2>/dev/null&&echo "At the line ($t/$w): write your card in its node tree (agi-wt pull), run agi-flush, then: touch ~/.fresh;kill \$PPID";:
~~~

### agi-at (1129 B)
~~~sh
#!/bin/sh
# agi-at PATH...: ONE signed commit of ~/t's paths onto posts/P by CAS on the tip read; a miss = [raced], exit 4, the edit stays; a kid, no AGI_POST or no posts/P = rc 5 before any write; a NEW .agi/nodes node must pass grow.py first, else rc 6 (the edit stays); grow.py's report-mode `Scope:` lines ride the commit message as trailers; once the CAS landed the final reset is best-effort (a failed one = [reset], rc 0); ~/t = a detached view of the tip
cd ~/t;P=$AGI_POST;b=refs/heads/posts/$P;{ [ "$P" ]&&[ "$AGI_ROLE" != kid ]&&git rev-parse -q --verify $b>/dev/null;}||{ echo "[no-branch] $P: a kid, or no posts/$P: nothing committed">&2;exit 5;};x=$(mktemp -u);trap 'rm -f $x $x.s' 0;export GIT_INDEX_FILE=$x;t=$(git rev-parse $b)&&git read-tree $t&&git add -A -- "$@"&&n=$(git write-tree)||exit 1
GROW_TRAILERS=$x.s grow.py $t>&2||exit 6
[ $n = $(git rev-parse $t^{tree}) ]&&exit;c=$({ echo "$P: $*";[ -s $x.s ]&&{ echo;cat $x.s;};}|git commit-tree -S -p $t $n)&&git update-ref $b $c $t||{ echo "[raced] $*">&2;exit 4;}
unset GIT_INDEX_FILE;git reset -q $b||echo "[reset] $b: the commit landed, HEAD not moved">&2
~~~

### agi-atom (8072 B)
~~~sh
#!/bin/sh
# agi-atom add SLICE SRC [target:X] | close ID STATE | move ID.. FLOW [ARGS] | grandfather (only rows under a `**throw ..**` heading; any other legacy row is refused by name): card §7 rows `| a<n> | "<slice>" | src:<box sha>|src:<node id>#OWNER | <state> | lap<n> |` (goal:g7.16.1.11.46.2-.4); SRC is read here, the slice must be a byte substring of it; STATE closes a target: row once into leaf:<goal id>|idea:<id>|decision:<doc>#<line>|out:<reason> (the id must exist); move writes the slices into the flow's ARGS json and closes the rows moved:<flow>, then ONE agi-at of both files
set -f;T=$(readlink -f "${AGI_T:-$HOME/t}");C=$(readlink -f "${AGI_ATOM_CARD:-$T/.agi/sessions/quorum/${AGI_POST:?}.md}")||exit 1;N=$T/.agi/nodes;[ -f "$C" ]||{ echo "agi-atom: no card $C">&2;exit 2;}
d(){ echo "agi-atom: $*">&2;exit 2;};V=$1;[ $# -gt 0 ]&&shift;LAP=lap${AGI_LAP:-$(($(date +%s)/14400))};tab='	'
n(){ f=$N/${1%%:*}/${1#*:}.md;[ -f "$f" ]&&grep -qFx "id: $1" "$f";}
row(){ awk -F'|' -v i="$1" '{y=$2;gsub(/ /,"",y)}y==i&&NF>=7{print;exit}' "$C";}
sf(){ printf "%s\n" "$1"|awk -F'|' -v k=$(($2-0)) '{v=$(k);sub(/^ +/,"",v);sub(/ +$/,"",v);if(k==3){sub(/^"/,"",v);sub(/"$/,"",v)};printf "%s",v}';}
put(){ w=$(mktemp "$C.XXXXXX")&&cat >"$w"&&cat "$w">"$C";rm -f "$w";}
ins(){ export R;awk 'BEGIN{r=ENVIRON["R"]}{L[NR]=$0}END{for(i=1;i<=NR;i++)if(L[i]~/^## §7/){s=i;break}
  if(!s){for(i=1;i<=NR;i++)print L[i];print "";print "## §7 ATOMS (agi-atom add|close; open = target:, older than one lap = red)";print ""}else{e=NR;for(i=s+1;i<=NR;i++)if(L[i]~/^## /){e=i-1;break};while(e>s&&L[e]~/^[ \t]*$/)e--;for(i=1;i<=e;i++){print L[i];if(L[i]~/^\| # \| atom .*source/)h=1}}
  if(!h){if(s)print "";print "| # | atom (verbatim slice) | source | state | lap |";print "|---|---|---|---|---|"};print r;if(s)for(i=e+1;i<=NR;i++)print L[i]}' "$C"|put;}
case $V in
add)[ $# -ge 2 ]||d "add SLICE SRC [target:X]";s=$1;r=$2;g=${3:-target:?};case $s in ""|*"|"*|*'
'*)d "[slice] empty, or carries | or a newline: cut it there";;esac;case $g in target:?*);;*)d "[state] add opens target:<x>";;esac
 case $r in src:*#OWNER)i=${r#src:};i=${i%#OWNER};f=$N/${i%%:*}/${i#*:}.md;[ -f "$f" ]||d "[src] no node $i";S=$(awk '/^## /{p=/^## OWNER.*verbatim/}p' "$f");[ "$S" ]||d "[src] $i has no '## OWNER ... verbatim' section";;
 src:*)h=${r#src:};case $h in *[!0-9a-f]*|"")d "[src] $r";;esac;[ "$(git -C "$T" cat-file -t "$h" 2>/dev/null)" = commit ]||d "[src] no commit $h";S=$(git -C "$T" log -1 --format=%B "$h");;*)d "[src] src:<box commit sha> or src:<node id>#OWNER";;esac
 case $S in *"$s"*);;*)d "[verbatim] the slice is not a byte substring of $r";;esac
 grep -qF "| \"$s\" | $r |" "$C"&&d "[dup] already on the card"
 k=$(awk -F'|' '{gsub(/ /,"",$2)}$2~/^a[0-9]+$/&&substr($2,2)+0>m{m=substr($2,2)+0}END{print m+1}' "$C");R=$(printf '| a%s | "%s" | %s | %s | %s |' "$k" "$s" "$r" "$g" "$LAP")
 ins;echo "a$k";;
close)[ $# = 2 ]||d "close ID STATE";i=$1;g=$2;x=$(row "$i");[ "$x" ]||d "[row] no row $i in agi-atom form (grandfather the old rows first)";case $x in *"| target:"*|*"| red:"*);;*)d "[closed] $i is terminal";;esac
 case $g in leaf:*)v=${g#leaf:};v=goal:${v#goal:};n "$v"||d "[state] no goal node $v";;idea:?*)v=${g#idea:};n idea:${v#idea:}||d "[state] no idea node $g";;out:?*);;
 decision:?*)v=${g#decision:};p=${v%%#*};case $p in doc:*);;*)p=doc:$p;;esac;n "$p"||d "[state] no doc node $p";case $v in *#*)l=${v#*#};case $l in ""|*[!0-9]*)d "[state] #<line> is a number";;esac;[ "$l" -le "$(wc -l <"$N/doc/${p#doc:}.md")" ]||d "[state] $p has fewer than $l lines";;esac;;
 *)d "[state] leaf:<goal id> | idea:<id> | decision:<doc>#<line> | out:<reason> (moved: is move's alone)";;esac
 case $g in *"|"*)d "[state] no |";;esac;G=$g I=$i awk -F'|' -v OFS='|' '{y=$2;gsub(/ /,"",y)}y==ENVIRON["I"]&&NF>=7&&$5~/^ (target|red):/{$5=" "ENVIRON["G"]" "}{print}' "$C"|put;;
move)a=;while [ $# -gt 0 ]&&case $1 in a[0-9]*);;*)false;;esac;do a="$a $1";shift;done;[ "$a" ]&&[ $# -ge 1 ]&&[ $# -le 2 ]||d "move ID.. FLOW [ARGS]";fl=$1;case $fl in ""|*[!a-z0-9-]*)d "[flow] $fl";;esac
 A=$T/${2:-.agi/sessions/quorum/$fl.args.json};case $A in "$T"/*);;*)d "[args] under ~/t";;esac;case $A in *..*)d "[args] no ..";;esac;mkdir -p "${A%/*}";[ -f "$A" ]||echo '{}'>"$A";J=$(cat "$A")
 for i in $a;do x=$(row $i);[ "$x" ]||d "[row] no row $i";case $x in *"| target:"*);;*)d "[closed] $i is terminal";;esac;case $x in *"| src:doc |"*)d "[src] $i is grandfathered, not verbatim";;esac
  J=$(printf %s "$J"|jq -c --arg i $i --arg r "$(sf "$x" 4)" --arg s "$(sf "$x" 3)" --arg h "$(sf "$x" 3|sha256sum|cut -c1-12)" 'if (.atoms//[])|any(.src==$r and .slice==$s) then error("already in ARGS") else .atoms+=[{id:$i,src:$r,slice:$s,sha:$h}] end')||d "[args] $i would sit in two places";done
 printf '%s\n' "$J">"$A.n"&&mv "$A.n" "$A";for i in $a;do h=$(sf "$(row $i)" 3|sha256sum|cut -c1-12);I=$i G=moved:$fl H=$h awk -F'|' -v OFS='|' '{y=$2;gsub(/ /,"",y)}y==ENVIRON["I"]&&NF>=7{$3=" \"sha:"ENVIRON["H"]"\" ";$5=" "ENVIRON["G"]" "}{print}' "$C"|put;done
 exec ${AGI_ATOM_COMMIT:-agi-at} "${C#$T/}" "${A#$T/}";;
grandfather)r=$(awk -F'|' '/^## /{s=/^## §7/;t=0}s&&/^\*\*/{t=/^\*\*throw/}s&&NF==5&&$2~/^ [0-9]+\.[0-9]+ $/&&!t{gsub(/ /,"",$2);print "[src] "$2" is not under a throw: give it its real src"}' "$C");[ -z "$r" ]||d "$r"
 awk -F'|' -v OFS='|' -v L="$LAP" '/^## /{s=/^## §7/}s&&/^\|[-| ]+\|$/&&NF==5{print "|---|---|---|---|---|";next}s&&$2~/^ # $/&&NF==5{print "| # | atom (owner ask, short) | source | state | lap |";next}
 s&&NF==5&&$2~/^ [0-9]+\.[0-9]+ $/{t=$3;sub(/^ +/,"",t);sub(/ +$/,"",t);print "|"$2"| \""t"\" | src:doc |"$4"| "L" |";next}{print}' "$C"|put;;
red)[ $# = 3 ]||d "red c:CHUNK TOKEN SLICE";grep -q "^| r$2 |" "$C"&&exit 0;case $3 in ""|*"|"*)d "[slice] empty, or carries |";;esac;agi-mem show $1|sed '1,/^---$/d'|grep -qF -- "$3"||d "[verbatim] the slice is not in chunk $1";R=$(printf '| r%s | "%s" | src:chunk:%s | red:unnamed-reply | %s |' "$2" "$3" "$1" "$LAP");ins;;
derive)M=$(mktemp);trap 'rm -f $M $M.n' 0;agi-mem map>$M;live=$(git -C "$T" show ${AGI_TRUNK:-trunk}:.agi/nodes/.geometry/secrets.md 2>/dev/null|sed -n 's/^credits_live: *//p'|head -1)
 if [ "$1" = check ];then awk -F'|' -v live="$live" -v M=$M 'BEGIN{while((getline l<M)>0){split(l,f,"\t");a[f[1]]=" "f[5]" ";n=split(f[5],z," ");for(i=1;i<=n;i++){if(f[4]=="ask")as[z[i]]=1;if(f[4]=="ack")ak[z[i]]=1};if(f[2]=="owner"&&f[5]=="?")q++};for(i in as)if(i in ak)k++}
  /^## /{s=/^## §7/}s&&NF>=8&&$7~/^ chunks:/{y=$2;gsub(/ /,"",y);m=split($7,z," ");for(j=2;j<=m;j++){t++;if(index(a[z[j]]," "y" ")==0){print "[chunks] " y ": " z[j] " names " y " in no chunk";bad=1}}}
  END{print "chunks: " t+0 " listed";r=(live=="true"&&k+0==0);print "done-when(4): " k+0 " rows ask+ack, " q+0 " owner chunks ?" (r?" RED: the atomizer is live and no row holds an ask and its ack":" (open: the stub stands in until C1-C3)");exit bad||r}' "$C";exit;fi
 awk -F'|' -v M=$M -v out=$M.n 'BEGIN{while((getline l<M)>0){split(l,f,"\t");n=split(f[5],z," ");for(i=1;i<=n;i++)c[z[i]]=c[z[i]]" "f[1]}}
  /^## /{s=/^## §7/}s&&NF>=7&&$2~/^ (a[0-9]+|[0-9]+\.[0-9]+|r[0-9a-f]+) $/{y=$2;gsub(/ /,"",y);w=c[y];h=NF>=8?$7:"";gsub(/^ +| +$/,"",h);if(w==""&&h==""){print>out;next}o="";for(i=1;i<=6;i++)o=o $i "|";if(w!="")o=o " chunks:" w " |";if(h!=""&&h!="chunks:" w)print "[derive] " y ": the chunks list was [" h "], rewritten" >"/dev/stderr";t+=split(w,z," ");print o>out;next}{print>out}END{print "chunks: " t+0 " listed"}' "$C";cmp -s $M.n "$C"||put <$M.n;;
where)[ $# -ge 1 ]||d "where WORDS";h=$(agi-mem find "$*");[ "$h" ]||{ echo "no chunk";exit 1;};echo "$h"|while IFS='	' read -r c p t k a;do for i in ${a:-?};do case $i in \?|none)e="no exit yet";st=-;;*)x=$(row $i);e=$([ "$x" ]&&sf "$x" 5||echo "no row $i");case $e in leaf:*)g=${e#leaf:};g=${g#goal:};st=$(sed -n 's/^status: //p' $N/goal/$g.md 2>/dev/null|head -1);;*)st=-;;esac;;esac;echo "asked ${t%%T*} $(echo ${t#*T}|cut -c1-5)Z ($c) · $i · $e · ${st:--}";done;done;;
*)d "add | close | move | grandfather | red | derive [check] | where WORDS";;esac
~~~

### agi-atomize (3971 B)
~~~sh
#!/bin/sh
# agi-atomize [wake]: `wake` = the call agi-meter (the UserPromptSubmit hook) makes on the prompt "mail: box read": credits_live not true on the trunk -> ONE named skip line appended to ~/.atomize.log and NOTHING on stdout (a hook'"'"'s stdout enters the post'"'"'s context), no model call, exit 0; true -> the run below under timeout 45, stderr to ~/.atomize.log. The WAKE-PATH step after `box read` (goal:g7.16.1.11.46.3): cut each box message to this post that is not yet marked refs/atomized/P/<sha> into verbatim, non-overlapping atoms with targets (agi-infer: Haiku AGI_ATOMIZE_MODEL, Sonnet AGI_ATOMIZE_MODEL2 once if a target is ?), then `agi-atom add` each as a card §7 row and mark the commit; `>` lines never reach the model; kind fyi|report = 0 atoms, ask >= 1; a reply that paraphrases, overlaps or has no atoms for an ask marks nothing (the next wake retries)
set -f;P=${AGI_POST:?};T=$(readlink -f "${AGI_T:-$HOME/t}");M=refs/atomized/$P
[ "$1" = wake ]&&{ c=$(git -C "$T" show ${AGI_TRUNK:-trunk}:.agi/nodes/.geometry/secrets.md 2>/dev/null|sed -n 's/^credits_live: *//p'|head -1);[ "$c" = true ]||{ echo "$(date -u +%FT%TZ) [atomize] skipped: credits_live is ${c:-unreadable}, no model call">>$HOME/.atomize.log;exit 0;};exec timeout 45 "$(readlink -f "$0")" 2>>$HOME/.atomize.log;}
W=$(mktemp -d);trap 'rm -rf $W' 0;cd "$T"||exit 1;add=0
ids=$(grep -rlE "Assigned to \*\*$P\*\*" .agi/nodes/goal 2>/dev/null|xargs -r grep -l '^status: active$'|sed 's|.*/||;s|\.md$||'|tr '\n' ' ')
printf '%s' '{"type":"object","properties":{"kind":{"enum":["ask","fyi","report"]},"atoms":{"type":"array","items":{"type":"object","properties":{"slice":{"type":"string"},"target":{"type":"string"}},"required":["slice","target"]}}},"required":["kind","atoms"]}'>$W/s
go(){ { printf 'Cut this message into atoms. kind: ask (it asks the recipient to do something), fyi (nothing to do), report (numbers). Only an ask has atoms: each atom is {slice, target}, a VERBATIM, non-overlapping slice of the message (never reworded, no | and no newline in a slice), target = one of the leaf ids below, idea, decision, or ?. Reply as JSON only.\nleaf ids: %s\n--- message\n' "$ids";cat $W/b;}|AGI_INFER_SCHEMA=$W/s ${AGI_ATOMIZE_INFER:-agi-infer} $1>$W/r;}
ck(){ k=$(jq -er '.kind' $W/r 2>/dev/null)||return 1;case $k in fyi|report):>$W/a;return 0;;ask);;*)return 1;;esac
 jq -r '.atoms[]|.slice+"\t"+.target' $W/r>$W/a 2>/dev/null&&[ -s $W/a ]||return 1;cut -f1 $W/a>$W/l;case $(cat $W/l) in *"	"*)return 1;;esac
 awk 'NR==FNR{b=b $0 "\n";next}{p=index(b,$0);if(p==0||$0=="")x=1;print p+0,p+length($0)-1}END{exit x}' $W/b $W/l>$W/p&&sort -n $W/p|awk 'NR>1&&$1<=e{x=1}{e=$2}END{exit x}';}
for r in $(git for-each-ref --format='%(refname)' refs/box|grep "/$P$");do f=${r#refs/box/};f=${f%/*}
 for c in $(git rev-list --reverse $r);do git rev-parse -q --verify $M/$c>/dev/null&&continue;[ $(($(date +%s)-$(git log -1 --format=%ct $c))) -le ${AGI_ATOMIZE_AGE:-86400} ]||continue
  git verify-commit --raw $c 2>&1|grep -q "for $f@agi with"||continue;git log -1 --format=%B $c|grep -v '^>'>$W/b;grep -q '[^[:space:]]' $W/b&&! grep -q '^\[town\]' $W/b||{ git update-ref $M/$c $c "";continue;}
  rm -f $W/a1;go ${AGI_ATOMIZE_MODEL:-claude-haiku-5-5}&&ck||{ echo "[atomize] $c: no usable reply from ${AGI_ATOMIZE_MODEL:-claude-haiku-5-5}, nothing marked">&2;continue;}
  grep -q "	[?]$" $W/a&&cp $W/a $W/a1&&go ${AGI_ATOMIZE_MODEL2:-claude-sonnet-5-5}&&ck||{ [ ! -s $W/a1 ]||cp $W/a1 $W/a;}
  ok=1;while IFS='	' read -r s t;do t=${t#goal:};if [ -f .agi/nodes/goal/$t.md ];then t=target:goal:$t;else case $t in idea|decision)t=target:$t;;*)t=target:?;;esac;fi
   agi-atom add "$s" src:$c "$t">/dev/null||{ ok=;break;};add=1;done<$W/a
  [ "$ok" ]&&git update-ref $M/$c $c ""||echo "[atomize] $c: an atom was refused, the commit is not marked">&2;done;done
[ $add = 0 ]||exec ${AGI_ATOM_COMMIT:-agi-at} "$(readlink -f "${AGI_ATOM_CARD:-$T/.agi/sessions/quorum/$P.md}"|sed "s|^$T/||")"
~~~

### agi-mem (10791 B)
~~~sh
#!/bin/sh
# agi-mem tap|at (goal:g7.16.1.11.46.13): `mem: full` rows only. tap = the hook (agi-meter at UserPromptSubmit, the Stop hook): stdin = the hook JSON; sweep the session transcript from its cursor, owner lines (a user string or queued_command whose origin.kind is human, whose first non-blank text is no tag opener or [SYSTEM NOTIFICATION, never a nudge, compact summary, meta or tool_result) and the post's text blocks, REDACTED (anonymize.py redact), into ~/.mem/<mint>.git: its own bare dir, 0700, no ACL, no remote, a commit of mem/<date>/c-<sha12>.md per sweep; rc 0 always, a failure = ONE [mem] warn line. at = `mem: tapped <chunks>/<eligible>` (RED when fewer), `mem: unread`, then the walk's check-2 lines. goal:g7.16.1.11.46.14 (M7): label [--redo c:ID..] = tier 0 on POST chunks only (a<n> bare; a dotted id only marked `atom 10.2` | `atoms: 10.2 5.5` | `[10.2]`, no version tail; nothing inside a > line, a fenced block (a block closes only on a fence of the opener's character at >= its length, so a ~~~ or a shorter fence inside it is text; an unmatched fence runs to the chunk end), a backtick span or a double-quoted span (even across lines) counts; none named = `none`); an owner chunk stays `?` until the atomizer is live; --redo recomputes the named chunks (one that matches no chunk prints `label --redo: no chunk ID`, rc 1); nested [fix] = `nested-fence chunks: N` + their ids (live post chunks with a fence inside a fence; fix runs label --redo on them; an unreadable store prints `mem: unread`, rc 1, never 0); map / find RE / show c:ID read the store; scrub = RETIRE (move, bytes unchanged) an owner chunk whose body opens with a tag to mem/retired/ and clear its session cursor (at, map, find, label read mem/<date>/ only; at is RED on k != m); walk = after label, a `kind: ask` chunk whose next post chunk names no atom id is a red row (agi-atom red) + a [unnamed-reply] notice, a reply naming one closes it; tap ends with label, agi-atom derive, walk
P=$AGI_POST;E=${AGI_ENGINE:-$HOME/t};S=${AGI_MEM_DIR:-$HOME/.mem}/${AGI_MINT:-$P}.git
px=$(git -C $E show ${AGI_TRUNK:-trunk}:.agi/nodes/.geometry/posts.md 2>/dev/null)||{ case $1 in at)echo "mem: unread";;tap)echo "[mem] warn: posts.md unreadable at ${AGI_TRUNK:-trunk} (the turn goes on)";;esac;exit 0;}
[ "$(printf %s "$px"|sed -n 's/^  - {/{/p'|jq -rR "fromjson?|select(.name==\"$P\")|.mem//empty"|head -1)" = full ]||exit 0
NU='[[:space:]]*(<[a-z][a-z-]*[ >]|mail: box read|keepalive:|Caveat:|[[]Request interrupted|[[]SYSTEM NOTIFICATION|This session is being continued)'
FZ='{l=$0;sub(/^[[:space:]]*/,"",l);c=substr(l,1,1);n=0;if(c=="`"||c=="~")while(substr(l,n+1,1)==c)n++;r=substr(l,n+1);o=n>=3&&(c=="~"||index(r,"`")==0);if(f){if(o&&c==ch&&n>=len&&r~/^[[:space:]]*$/)f=0;else if(o&&m=="n")print "nested";next}if(o){f=1;ch=c;len=n;next}if(m=="s")print}'
Q='def tx:if type=="string" then . else [.[]|select(.type=="text" and (.text|startswith("<system-reminder>")|not))|.text]|join("\n") end;select(.isSidechain!=true)|(if .type=="user" and .isMeta!=true and .isCompactSummary!=true and (.message.content|type=="string" or all(.[];.type!="tool_result")) and .origin.kind=="human" then {sp:"owner",b:(.message.content|tx)} elif .type=="attachment" and .attachment.type=="queued_command" and .attachment.origin.kind=="human" then {sp:"owner",b:(.attachment.prompt|strings)} elif .type=="assistant" then {sp:"post",b:(.message.content|tx)} else empty end)+{u:.uuid,t:.timestamp,l:input_line_number}|select((.b|length)>0 and (.sp=="post" or (.b|test("^('"$NU"')")|not)))'
w(){ echo "[mem] warn: $* (the turn goes on)";}
cm(){ c=$(git -C $S -c user.name=mem -c user.email=mem@agi -c commit.gpgsign=false commit-tree $(git -C $S write-tree) ${tip:+-p $tip} -m "$1")&&git -C $S update-ref refs/heads/mem $c $tip;}
case $1 in
tap)j=$(cat);exec 2>/dev/null;f=$(printf %s "$j"|jq -r '.transcript_path//empty');s=$(printf %s "$j"|jq -r '.session_id//empty');[ "$f" ]||exit 0;D=$(mktemp -d);trap 'rm -rf "${D:?}"' 0
 [ -r "$f" ]||{ w "no transcript $f";exit 0;}
 [ -d $S ]||(umask 077;mkdir -p ${S%/*}&&chmod 700 ${S%/*}&&git init -q --bare $S&&chmod 700 $S&&setfacl -bk $S ${S%/*} 2>/dev/null;git -C $S config core.hooksPath /dev/null)||{ w "store $S not creatable";exit 0;}
 n=$(cat $S/cursor-$s 2>/dev/null||echo 0);tot=$(wc -l <$f);tail -n +$((n+1)) $f|jq -c "$Q"|head -n ${AGI_MEM_BATCH:-60}|python3 $E/extensions/agi/bin/anonymize.py redact --root $E>$D/r||{ w "redact failed";exit 0;}
 tip=$(git -C $S rev-parse -q --verify refs/heads/mem);have=$D/h;{ [ -z "$tip" ]||git -C $S ls-tree -r --name-only $tip;}>$have;[ -z "$tip" ]||GIT_INDEX_FILE=$D/i git -C $S read-tree $tip;export GIT_INDEX_FILE=$D/i;new=0;last=$n
 while read -r r;do printf %s "$r">$D/o;jq -j .b $D/o>$D/b;u=$(jq -r .u $D/o);sp=$(jq -r .sp $D/o);t=$(jq -r .t $D/o);last=$(jq .l $D/o);last=$((n+last))
  id=$({ printf '%s\0%s\0%s\0' $sp $s $u;cat $D/b;}|sha256sum|cut -c1-12);grep -q "c-$id.md" $have&&continue
  { printf -- '---\nid: c:%s\nspeaker: %s\ns: %s\nu: %s\nt: %s\nkind: ?\natom: ?\nredacted: %s\n---\n' $id $sp $s $u $t $(jq .n $D/o);cat $D/b;}>$D/c
  b=$(git -C $S hash-object -w $D/c)&&git -C $S update-index --add --cacheinfo 100644,$b,mem/${t%%T*}/c-$id.md||{ w "store $S not writable";exit 0;};new=$((new+1));done<$D/r
 if [ $new -gt 0 ];then cm "tap $s"||{ w "store $S not writable";exit 0;};fi
 [ $(wc -l <$D/r) -lt ${AGI_MEM_BATCH:-60} ]&&last=$tot;echo $last>$S/cursor-$s||w "cursor not writable";agi-mem label;agi-atom derive;agi-mem walk;exit 0;;
at)s=$(cat ~/.session 2>/dev/null);f=$(ls ~/.claude/projects/*/$s.jsonl 2>/dev/null|head -1);m=$(jq -c "$Q" $f 2>/dev/null|jq -s '[.[]|select(.sp=="owner")]|length' 2>/dev/null)
 [ "$m" ]&&git -C $S rev-parse -q --git-dir>/dev/null 2>&1&&{ [ -r $S/cursor-$s ]||[ "$m" = 0 ];}||{ echo "mem: unread";exit 0;}
 k=$(git -C $S grep --all-match -l -e "^s: $s\$" -e '^speaker: owner$' refs/heads/mem -- mem ':!mem/retired' 2>/dev/null|wc -l);echo "mem: tapped $k/$m$([ $k -lt $m ]&&echo ' RED')$([ $k -gt $m ]&&echo " RED ($((k-m)) owner chunk not owner by the current filter)")";agi-mem walk ls;;
map)git -C $S grep -h -m5 -E '^(id|speaker|t|kind|atom): ' refs/heads/mem -- mem ':!mem/retired' 2>/dev/null|awk '/^id: /{if(i)print i"\t"p"\t"t"\t"k"\t"a;i=substr($0,5);p=t=k=a=""}/^speaker: /{p=substr($0,10)}/^t: /{t=substr($0,4)}/^kind: /{k=substr($0,7)}/^atom: /{a=substr($0,7)}END{if(i)print i"\t"p"\t"t"\t"k"\t"a}'|sort -t'	' -k3,3;;
show)git -C $S show refs/heads/mem:$(git -C $S ls-tree -r --name-only refs/heads/mem|grep "c-${2#c:}.md") 2>/dev/null;;
find)for x in $(git -C $S grep -l -i -E "$2" refs/heads/mem -- mem ':!mem/retired' 2>/dev/null|sed 's/^[^:]*://');do git -C $S show refs/heads/mem:$x|sed '1,/^---$/d'|grep -qiE "$2"&&echo c:${x##*c-}|sed 's/\.md$//';done|while read -r i;do agi-mem map|awk -F'	' -v i=$i '$1==i';done;;
scrub)exec 2>/dev/null;tip=$(git -C $S rev-parse -q --verify refs/heads/mem)||exit 0;D=$(mktemp -d);trap 'rm -rf "${D:?}"' 0;export GIT_INDEX_FILE=$D/i;git -C $S read-tree $tip;new=0
 for x in $(git -C $S grep -l '^speaker: owner$' $tip -- mem ':!mem/retired'|sed 's/^[^:]*://');do git -C $S show $tip:$x|sed '1,/^---$/d;/^[[:space:]]*$/d'|head -1|grep -qE "^$NU"&&{ printf '0 %040d\t%s\n100644 %s\tmem/retired/%s\n' 0 $x $(git -C $S rev-parse $tip:$x) ${x#mem/}|git -C $S update-index --index-info;rm -f $S/cursor-$(git -C $S show $tip:$x|sed -n 's/^s: //p'|head -1);new=$((new+1));};done
 [ $new -gt 0 ]&&cm "speaker not human: the body opens with a tag or [SYSTEM NOTIFICATION; moved to mem/retired, bytes unchanged (agi-mem scrub)";exit 0;;
label)exec 2>/dev/null;shift;tip=$(git -C $S rev-parse -q --verify refs/heads/mem)||exit 0;D=$(mktemp -d);trap 'rm -rf "${D:?}"' 0;export GIT_INDEX_FILE=$D/i;git -C $S read-tree $tip;new=0
 ids=" $(awk -F'|' '/^## /{s=/^## §7/}s{y=$2;gsub(/ /,"",y)}s&&y~/^(a[0-9]+|[0-9]+\.[0-9]+|r[0-9a-f]+)$/{printf "%s ",y}' ${AGI_ATOM_CARD:-$E/.agi/sessions/quorum/$P.md}) "
 miss=0;: >$D/rl;if [ "$1" = --redo ];then shift;[ $# -gt 0 ]||{ echo "label --redo: no chunk named";miss=1;};for i in "$@";do git -C $S ls-tree -r --name-only $tip -- mem|grep -v retired|grep "/c-${i#c:}.md$">>$D/rl||{ echo "label --redo: no chunk $i";miss=1;};done;else git -C $S grep -l '^atom: ?$' $tip -- mem ':!mem/retired'|sed 's/^[^:]*://'>$D/rl;fi
 for x in $(cat $D/rl);do git -C $S show $tip:$x>$D/c;p=$(sed -n 's/^speaker: //p' $D/c|head -1);[ $p = post ]||continue;a=;b=$(sed '1,/^---$/d' $D/c|awk -v m=s "$FZ"|sed '/^[[:space:]]*>/d'|sed ':a;$!{N;ba};s/`[^`]*`//g;s/"[^"]*"//g');I='(?:a[0-9]+|[0-9]+\.[0-9]+)(?![A-Za-z0-9]|\.[0-9])';L="(?:$I[,[:space:]]*)+"
  for i in $({ printf %s "$b"|grep -oP '(?<![A-Za-z0-9.])a[0-9]+(?![A-Za-z0-9]|\.[0-9])';printf %s "$b"|grep -oP "\\batoms?:?[[:space:]]+\\K$L"|grep -oE 'a[0-9]+|[0-9]+\.[0-9]+';printf %s "$b"|grep -oP "\\[\\K$L(?=\\])"|grep -oE 'a[0-9]+|[0-9]+\.[0-9]+';}|sort -u);do case "$ids" in *" $i "*)a="$a$i ";;esac;done;a=${a% };k=
  if [ "$a" ];then v=$a;k=ack;else v=none;k=chatter;fi
  awk -v a="$v" -v k="$k" '/^---$/{n++}n<2&&/^atom: /{print "atom: " a;next}n<2&&/^kind: /&&k!=""{print "kind: " k;next}{print}' $D/c>$D/n&&b=$(git -C $S hash-object -w $D/n)&&git -C $S update-index --cacheinfo 100644,$b,$x&&new=$((new+1));done
 [ $new -gt 0 ]&&cm label;exit $miss;;
nested)exec 2>/dev/null;D=$(mktemp -d);trap 'rm -rf "${D:?}"' 0;tip=$(git -C $S rev-parse -q --verify refs/heads/mem)&&git -C $S ls-tree -r --name-only $tip -- mem>$D/l||{ echo "mem: unread";exit 1;};: >$D/n
 for x in $(grep -v retired $D/l);do git -C $S show $tip:$x>$D/c||{ echo "mem: unread";exit 1;};sed -n 's/^speaker: //p' $D/c|head -1|grep -qx post||continue;sed '1,/^---$/d' $D/c|awk -v m=n "$FZ"|grep -q nested&&echo c:${x##*c-}|sed 's/\.md$//'>>$D/n;done
 echo "nested-fence chunks: $(wc -l <$D/n|tr -d ' ')";cat $D/n;[ "$2" = fix ]&&[ -s $D/n ]&&agi-mem label --redo $(cat $D/n);exit 0;;
walk)exec 2>/dev/null;agi-mem label;C=${AGI_ATOM_CARD:-$E/.agi/sessions/quorum/$P.md};M=$(agi-mem map)
 if [ "$2" = ls ];then for i in $(awk -F'|' '/^## /{s=/^## §7/}s{y=$2;gsub(/ /,"",y)}s&&$5~/^ target:/&&y~/^(a[0-9]+|[0-9]+\.[0-9]+)$/{print y}' $C);do echo "$M"|awk -F'	' -v i=$i '$2=="post"{n=split($5,z," ");for(j=1;j<=n;j++)if(z[j]==i)f=1}END{exit !f}'||echo "[walk] $i: no ack chunk yet";done;exit 0;fi
 echo "$M"|awk -F'	' '$4=="ask"{q[++n]=$1;next}$2=="post"&&n{for(i=1;i<=n;i++)print ($5=="none"||$5=="?"?"RED":"OK"),q[i],$1;n=0}'|while read -r v q r;do h=$(echo ${q#c:}|cut -c1-8)
  case $v in RED)agi-atom red $q $h "$(agi-mem show $q|sed '1,/^---$/d'|head -1|cut -c1-80)";agi-notice add "[unnamed-reply] $h $q was answered by $r naming no atom id: name the row id (a<n>) in your next reply";;OK)grep -q "^| r$h |" $C&&agi-atom close r$h out:named;; esac;done;exit 0;;
esac
~~~

### grow.py (5140 B)
~~~python
#!/usr/bin/env python3
# grow.py TIP: the ONE growth-order check agi-turn and agi-at call on the temp index (GIT_INDEX_FILE) after the tree is written and before the commit. Every NEW .agi/nodes/**.md (an add against TIP, --no-renames, not under deprecated/; an edit is never gated) is read from its STAGED blob (diff-index -z read as BYTES: raw NUL-split paths, never C-quoted, no newline translation; strict UTF-8) and checked in-process: its parents must resolve in the STAGED tree (a parent added in the same tree counts, except a NEW add under deprecated/; a decoy file in ~/t does not; none = refused), then spawn_gate.check_spawn must APPROVE it (REJECTED, UNVERIFIED and an unknown type are all refused), so a new node is APPROVED or REFUSED, never committed unchecked. REPORT mode (goal:g7.16.1.11.46.10, never a refusal): an APPROVED add outside SCOPE(AGI_POST) = grow(row at TIP) x G, with every parent under closure(roots) (the walk reads parents from the STAGED blobs; '*' admits all; a row without both cells admits nothing; no posts.md at TIP = nothing to report against, silent) is said on stderr as [scope] and appended as `Scope: <post> <type> <parent>` to the file named by $GROW_TRAILERS, which agi-at and agi-turn put in the commit message as a trailer block; any failure of the report is [scope-report-broken], b unchanged. rc 0 = pass; 1 = [growth-order] <node> (one line per refusal); 3 = [spawn-gate-missing] / [spawn-gate-broken] (an absent or crashing checker, a failed git, a non-UTF-8 path or blob: FAILS CLOSED)
import sys,os,re,json,subprocess as S
sys.dont_write_bytecode=True
b=0
def rep(tip,post,m,q,Q,g,f):
 j={};pm=tip+":.agi/nodes/.geometry/posts.md"
 if S.run(["git","cat-file","-e",pm],capture_output=True).returncode:return
 for l in S.run(["git","show",pm],capture_output=True,check=True).stdout.decode().split("\n"):
  if l.startswith("  - {"):
   try:x=json.loads(l[4:])
   except ValueError:continue
   if x.get("name")==post:j=x;break
 G=j.get("grow");R=j.get("roots");t=g.canonical_type(m.get("type"))
 def up(x,s):
  if "*" in R or x in R:return 1
  if x in s or len(s)>64 or x not in Q:return 0
  s.add(x);y=f.read_frontmatter(S.run(["git","show",":"+Q[x]],capture_output=True,check=True).stdout.decode())
  return any(up(z,s) for z in ((y or {}).get("parents") or []))
 for y in q:
  w=("no grow/roots cells on the row" if not isinstance(G,list) or not isinstance(R,list) else "type %s not in grow"%t if "*" not in G and t not in G else "" if up(y,set()) else "parent outside roots")
  if w:
   print("[scope] %s %s %s: %s (reported, not refused)"%(post,t,y,w),file=sys.stderr)
   if os.environ.get("GROW_TRAILERS"):open(os.environ["GROW_TRAILERS"],"a").write("Scope: %s %s %s\n"%(post,t,y))
try:
 A=[p for p in(q.decode() for q in S.run(["git","diff-index","-z","--cached","--no-renames","--name-only","--diff-filter=A",sys.argv[1],"--",".agi/nodes"],capture_output=True,check=True).stdout.split(b"\0")) if p.endswith(".md")]
 L=[p for p in A if not p.startswith(".agi/nodes/deprecated/")];D={p.encode() for p in A}-{p.encode() for p in L}
 if L and not os.path.exists("extensions/agi/bin/spawn_gate.py"):print("[spawn-gate-missing] extensions/agi/bin/spawn_gate.py is not in ~/t: %d new node(s) not checked"%len(L));b=3
 elif L:
  sys.path.insert(0,"extensions/agi/bin");import spawn_gate as g,frontmatter as f
  d=g.Path(".agi").joinpath(*g.SCHEMAS_SUBDIR);R=g.load_spawn_rules(d,root=g.Path(".agi"));C=g.read_ladder_season(g.resolve_nodes_root(g.Path(".agi"),d))
  r=S.run(["git","grep","--cached","-aznE",r"^(---\s*$|(id|mint_id|type):)","--",".agi/nodes/*.md"],capture_output=True);assert r.returncode<2,r.stderr
  F={};I={};Q={}
  for x,n,t in re.findall(rb"([^\0]+)\0(\d+)\0([^\n]*)\n",r.stdout):
   if x in D:continue
   e=F.setdefault(x,{"f":0});t=t.decode("utf-8","surrogateescape")
   if t.rstrip()=="---":e["f"]+=1 if(e["f"] or n==b"1")else 2
   elif e["f"]==1:k,_,v=t.partition(":");e.setdefault(k,v.strip().strip("\"'"))
  for x,e in F.items():
   for k in("id","mint_id"):
    if e.get(k):I[e[k]]=g.canonical_type(e.get("type"));Q[e[k]]=x.decode()
  for p in L:
   m=f.read_frontmatter(S.run(["git","show",":"+p],capture_output=True,check=True).stdout.decode())
   if m is None:print("[growth-order] "+p+": no readable front matter");b=1;continue
   q=m.get("parents") or []
   if not isinstance(q,list) or [y for y in q if y not in I]:print("[growth-order] %s: parent(s) %s resolve nowhere in the staged tree"%(m.get("id") or p,q if not isinstance(q,list) else [y for y in q if y not in I]));b=1;continue
   r=g.check_spawn(m.get("type"),q,rules=R,type_index=I,fm=m,node_id=m.get("id") or p,season_parents=m.get("season_parents"),current_season=C)
   if r.status!=g.APPROVED:print("[growth-order] "+re.sub(r"^SPAWN-GATE \w+: ","",(r.messages or [r.reason])[0]).split(" Schema:")[0]);b=1
   elif os.environ.get("AGI_POST"):
    try:rep(sys.argv[1],os.environ["AGI_POST"],m,q,Q,g,f)
    except BaseException as e:print("[scope-report-broken] "+repr(e)[:120],file=sys.stderr)
except BaseException as e:print("[spawn-gate-broken] spawn_gate.py: "+repr(e)[:160]);b=3
sys.exit(b)
~~~

### agi-turn (4615 B)
~~~sh
#!/bin/sh
# agi-turn: each changed node tree = ONE grid commit on posts/P (temp index from the tip, signed, CAS); the tip moved it since pull = archived + dropped; a tree is purged ONLY once its commit is proven AND the whole tree is clean against it (agi-turn chk DIR COMMIT: a file outside .p keeps it, [dirty]; a git failure keeps it too); agi-turn purge DIR = that check then rm, else EVERY file of the tree goes to refs/archive/P/<dir> (signed, CAS), [kept] names it, rc 1; a kid (AGI_ROLE=kid, which agi-kid sets), no AGI_POST or no posts/P = rc 5, nothing committed (the SAME guard line before any WRITE in agi-at, agi-turn and agi-flush (chk and c() only read, so they run before it); agi-sync runs at the end of EVERY turn, before the detach: the trunk is merged each turn or its conflict said by name; a Stop hook must never exit 2); the staged tree goes through grow.py (its report-mode `Scope:` lines become trailers of the commit; a NEW .agi/nodes node must pass spawn_gate; an edit never does; a refusal or a broken checker = ONE bracketed line, rc 1, nothing committed, the tree kept); BEFORE the detach, `agi-turn strand` (agi-flush calls it too, ONE guard): a detached HEAD that carries commits on no ref is REFUSED by name ([strand-refused], rc 1, HEAD left where it is; it never folds: agi-at is the one write path); [strand-refused] and [out-of-tree] go to stderr AND, through `agi-notice add` (one line per distinct notice), to ~/.notice, which agi-notice (called first by agi-brief and agi-meter) claims and prints once on stdout into the post's context; any failure keeps the tree (rc != 0, a [label]); ~/t = a detached read view
cd ~/t;P=$AGI_POST;b=refs/heads/posts/$P;x=$(mktemp -u);trap 'rm -f $x $x.l $x.s' 0;export GIT_INDEX_FILE=$x;k=0
c(){ [ "$2" ]&&git read-tree $2&&git --work-tree=$1 diff --name-only --diff-filter=MT>$x.l&&git --work-tree=$1 ls-files -o>>$x.l||return 2;l=$(grep -vxF -e .p -e .b $x.l|tr '\n' ' ');[ -z "$l" ];}
[ "$1" = chk ]&&{ c $2 $3;r=$?;[ $r = 0 ]&&exit;[ $r = 1 ]&&echo "[dirty] $(basename $2): kept, not in the commit: $l">&2||echo "[dirty] $(basename $2): kept, cannot read it against '$3'">&2;exit 1;}
{ [ "$P" ]&&[ "$AGI_ROLE" != kid ]&&git rev-parse -q --verify $b>/dev/null;}||{ echo "[no-branch] $P: a kid, or no posts/$P: nothing committed">&2;exit 5;}
[ "$1" = strand ]&&{ git symbolic-ref -q HEAD>/dev/null&&exit;h=$(git rev-parse -q --verify HEAD)||exit 0;n=$({ echo $h;git for-each-ref --format='^%(objectname)' refs/heads refs/remotes refs/archive refs/tags;}|git rev-list --count --stdin);[ $n = 0 ]&&exit
 m="[strand-refused] $P: HEAD $(git rev-parse --short $h) carries $n commit(s) on no ref: HEAD left where it is, nothing moved; put them on posts/$P through agi-at";echo "$m">&2;agi-notice add "$m";exit 1;}
[ "$1" = purge ]&&{ d=${2%/};m=${d##*/};c $d $(cat $d/.b 2>/dev/null||git rev-parse $b);[ $? = 0 ]&&{ rm -rf $d;exit;};a=refs/archive/$P/$m;o=$(git rev-parse -q --verify $a||:)
 t=$(git rev-parse $b)&&git read-tree $t&&git --work-tree=$d add --ignore-removal -f -- . ':!.p' ':!.b'&&n=$(git write-tree)&&e=$(echo "$P: kept $m"|git commit-tree -S -p $t ${o:+-p $o} $n)&&git update-ref $a $e "$o"&&s="whole tree committed to $a"||s="NOT SAVED: the ref write failed";echo "[kept] $m: ${l:-unreadable}: $s">&2;exit 1;}
for d in ${AGI_WT:-$RUNTIME_DIRECTORY/wt}/*/;do [ -f $d.p ]||continue;m=$(basename $d);t=$(git rev-parse $b)&&git read-tree $t&&a=$(git --work-tree=$d add -A --pathspec-from-file=$d.p 2>&1)&&n=$(git write-tree)||{ echo "[stage] $m: $(echo "${a:-git failed}"|tr '\n' ' ')">&2;k=1;continue;}
 [ $n = $(git rev-parse $t^{tree}) ]&&continue;: >$x.s;GROW_TRAILERS=$x.s grow.py $t>&2||{ k=1;continue;};r=$b;o=$t;q=;[ ! -f $d.b ]||(IFS='
';set -f;git diff --quiet $(cat $d.b) $t -- $(cat $d.p))||{ r=refs/archive/$P/$m;o=$(git rev-parse -q --verify $r||:);q=${o:+-p $o};}
 c=$({ echo "$P: $(sed q $d.p)";[ -s $x.s ]&&{ echo;cat $x.s;};}|git commit-tree -S -p $t $q $n 2>&1)||{ echo "[commit] $m: cannot sign or commit: $c">&2;k=1;continue;}
 git update-ref $r $c "$o"||{ echo "[raced] $m">&2;k=4;continue;}
 [ $r = $b ]&&{ echo $c>$d.b;continue;};agi-turn chk $d $c&&{ echo "[moved] $m: changed on the tip since pull; your version is $r, the tree is dropped">&2;rm -rf $d;continue;};echo "[moved] $m: your version is $r, the tree is KEPT">&2;k=1;done
unset GIT_INDEX_FILE;agi-sync;if agi-turn strand;then git checkout -q --detach $b;else k=1;fi;git status -s|grep -q .&&{ m="[out-of-tree] ~/t has $(git status -s|wc -l) unversioned change(s): edit in a node's tree (agi-wt pull)";echo "$m">&2;agi-notice add "$m";};exit $k
~~~

### pre-commit (639 B)
~~~sh
#!/bin/sh
# pre-commit (git runs it from core.hooksPath=~/bin, where the unit extracts every piece): Door 1 of goal:g7.16.1.11.38. A plain commit on a DETACHED HEAD in ~/t is REFUSED (rc 1): ~/t is a read view, agi-at is the one write path (signed CAS, grow.py), so a commit made there is on no ref and the next turn's detach strands it. Any other worktree, an attached HEAD, and --no-verify are untouched; then ~/hooks/pre-commit (if a post has one) runs as before
[ . -ef ~/t ]&&! git symbolic-ref -q HEAD>/dev/null&&{ echo "[detached] commit through: agi-at <path>">&2;exit 1;}
[ -x ~/hooks/pre-commit ]&&exec ~/hooks/pre-commit "$@";:
~~~

### agi-notice (1141 B)
~~~sh
#!/bin/sh
# agi-notice [add LINE]: the ONE engine->post channel, ~/.notice (a file in the post's home: it survives a rotation, the .fresh restart and agi-out, which touch .ssh, bin, .gitconfig, .claude, never this file). `add LINE` appends it unless a line with the same KEY is already there (the [label] plus any 7+ hex word, e.g. the sha), so a stuck condition is ONE line, not one per turn. No args = print: CLAIM the file atomically first (mv to ~/.notice.PID; an append during the print lands in a fresh ~/.notice and prints next turn, and a claim left by a crashed printer is printed too), print each distinct line once on STDOUT (the hook channel the model reads: agi-brief's SessionStart and agi-meter's prompt hook call it first), THEN remove the claims printed
case $1 in add)[ -e ~/.notice ]||: >~/.notice;awk -v l="$2" 'function K(x,n,a,i,r){n=split(x,a," ");for(i=1;i<=n;i++)if(a[i]~/^\[/||(length(a[i])>6&&a[i]~/^[0-9a-f]+$/))r=r a[i];return r}K($0)==K(l){f=1}END{exit f}' ~/.notice&&echo "$2">>~/.notice;exit 0;;esac
mv ~/.notice ~/.notice.$$ 2>/dev/null;f=$(ls ~/.notice.* 2>/dev/null)||exit 0;cat $f|awk '!s[$0]++';rm -f $f
~~~

### reference-transaction (1338 B)
~~~sh
#!/bin/sh
# reference-transaction (git runs it from core.hooksPath=~/bin; goal:g7.16.1.11.38.1): a post's MISTAKE cannot move a peer's ref. Git calls it for prepared, committed and aborted and honours a non-zero exit ONLY in prepared, so it acts only there: an agi-<p> user may not update refs/heads/posts/<q>, refs/box/<q>/* or refs/held/<q>/* with q != p (rc 1, one named line). Root, belam, agi-belam (the Prime's post, whose unit runs as agi-belam since the .10 move: it may move any ref), every other ref and every other user pass. It FAILS OPEN on its own error (rc 0, a stderr line, and an agi-notice once per post per day). A guard against mistakes, NOT a wall: any ref write run with git -c core.hooksPath=/dev/null still moves a peer's ref, and this file is the post's own, editable until the next unit start
[ "$1" = prepared ]||exit 0
f(){ echo "[ref-guard] fail open: $1">&2;agi-notice add "[ref-guard] fail open: $1 $(date +%Y%m%d)" 2>/dev/null;exit 0;}
u=$(id -un)&&[ "$u" ]||f "no user"
case $u in agi-belam)exit 0;;agi-?*);;*)exit 0;;esac
while read o n r;do [ "$r" ]||f "unparsed input"
 case $r in refs/heads/posts/*)q=${r#refs/heads/posts/};;refs/box/*|refs/held/*)q=${r#refs/*/};;*)continue;;esac
 [ "${q%%/*}" = "${u#agi-}" ]||{ echo "[ref-guard] $u may not move $r (a peer's ref), nothing changed">&2;exit 1;}
done
~~~

### agi-wt (1506 B)
~~~sh
#!/bin/sh
# agi-wt pull ID [REV] | new PATH [PAYLOAD] | drop ID (new / pull carry NO kid guard on purpose: they write only RAM trees; every ref write is guarded in agi-at / agi-turn / agi-flush): a node's tiny tree (node + payload, ONE PATH PER LINE in .p) in RAM for the session; agi-turn versions it, drop purges it only after a proven turn
cd ~/t;[ "$AGI_POST" ]||{ echo "agi-wt: no AGI_POST">&2;exit 5;};IFS='
';set -f;w=${AGI_WT:-$RUNTIME_DIRECTORY/wt};r=${3:-posts/$AGI_POST};mkdir -p $w
case $1 in new)n=$(basename $2 .md);case $n in ''|[!A-Za-z0-9_-]*|*[!A-Za-z0-9._-]*)echo "agi-wt: new $2: the basename [$n] must match [A-Za-z0-9_-][A-Za-z0-9._-]*">&2;exit 7;;esac;d=$w/$n;mkdir $d||exit 3;printf '%s\n' "$2" ${3:+"$3"}>$d/.p;echo $d;exit;;esac
f=$(git grep -lE "^(id|mint_id): $2$" $r -- .agi/nodes|head -1|cut -d: -f2-);[ "$f" ]||exit 2;d=$w/$(git show $r:$f|sed -n 's/^mint_id: //p')
case $1 in pull)[ -d $d ]&&{ echo $d;exit;};[ $(df --output=pcent $w|tail -1|tr -dc 0-9) -lt ${AGI_WT_HOLD:-60} ]||{ echo "hold $w";exit 3;}
mkdir $d;printf '%s\n' "$f" $(git show $r:$f|sed -n 's/^payload_ref: "\{0,1\}\([^"]*\)"\{0,1\}$/\1/p')>$d/.p
e=$(git archive -o $d.tar $r $(cat $d/.p) 2>&1&&tar -xC $d -f $d.tar 2>&1)||{ rm -rf $d $d.tar;echo "agi-wt: pull $2 failed: $e">&2;exit 6;};rm $d.tar;git rev-parse $r>$d/.b;echo $d;;
drop)[ -d $d ]||{ echo "agi-wt: no tree $d for $2 (a 'new' tree is dropped by agi-flush)">&2;exit 2;};agi-turn&&{ [ ! -d $d ]||agi-turn chk $d $(cat $d/.b)&&rm -rf $d;};;esac
~~~

### agi-track (89 B)
~~~sh
#!/bin/sh
grep --line-buffered -o '"/[^"]*"'|awk '!s[$0]++{print;fflush()}'>>$HOME/track
~~~

### agi-flush (942 B)
~~~sh
#!/bin/sh
# agi-flush: the writer guard before any write (a kid, no AGI_POST or no posts/P = rc 5, nothing written), then land every tree (4 turns), then agi-turn purge each dir left under $AGI_WT, found by DIR (pulled or new): clean = removed, anything else = kept whole on refs/archive/P/<dir> and [kept]: rc 0 iff no tree remains; then the trunk merge is agi-turn's (agi-sync, run at the end of every agi-turn, its conflict said by name); the final detach runs only if `agi-turn strand` passes (else rc 1, HEAD left)
cd ~/t;P=$AGI_POST;b=refs/heads/posts/$P;{ [ "$P" ]&&[ "$AGI_ROLE" != kid ]&&git rev-parse -q --verify $b>/dev/null;}||{ echo "[no-branch] $P: a kid, or no posts/$P: nothing committed">&2;exit 5;};w=${AGI_WT:-$RUNTIME_DIRECTORY/wt};agi-turn||agi-turn||agi-turn||agi-turn;k=$?;for d in $w/*/;do [ -d $d ]&&{ agi-turn purge $d||[ $k != 0 ]||k=1;};done
if agi-turn strand;then git checkout -q --detach $b;else k=1;fi;exit $k
~~~

### agi-sync (2579 B)
~~~sh
#!/bin/sh
# agi-sync: merge the trunk into posts/P and SAY a failure by name (goal:g7.16.1.11.41 targets 2-4). A posts/P merely BEHIND the trunk moves by CAS to the trunk tip, no commit (board_job.py land refuses a non-own commit); a clean divergence = one signed merge commit (CAS); a CONFLICT leaves the branch as it is and writes [trunk-conflict] P: N path(s) conflict with TRUNK: paths to ~/.notice (agi-notice, so it comes back once per turn while it lasts) and boxes the nearest HARNESSED ancestor (an inert council / keep row is skipped; the walk stops BELOW the row whose role is prime_director: a chain that reaches the Prime = notice only, owner 10-11 never box belam; none = notice only) once per conflict EPISODE (~/.trunk-boxed = a hash of the path set: it changes or clears when the paths do or a merge goes through; stamped even when the box is refused, so never retried every turn); any other failure = [trunk-merge-failed]. Run at the end of EVERY agi-turn and by agi-flush. A kid or no posts/P = nothing. Always rc 0.
set -f;cd ~/t;P=$AGI_POST;b=refs/heads/posts/$P;R=${AGI_TRUNK:-trunk}
{ [ "$P" ]&&[ "$AGI_ROLE" != kid ]&&t=$(git rev-parse -q --verify $b);}||exit 0
T=$(git rev-parse -q --verify $R^{commit})||{ agi-notice add "[trunk-merge-failed] $P: $R does not resolve to a commit";exit 0;}
git merge-base --is-ancestor $T $b&&{ rm -f ~/.trunk-boxed;exit 0;}
git merge-base --is-ancestor $b $T&&{ git update-ref $b $T $t||agi-notice add "[trunk-merge-failed] $P: cannot move posts/$P";rm -f ~/.trunk-boxed;exit 0;}
n=$(git merge-tree --write-tree --name-only $b $T 2>/dev/null);r=$?;[ $r = 1 ]||rm -f ~/.trunk-boxed
case $r in 0)c=$(echo "$P: merge $R"|git commit-tree -S -p $t -p $T $n)&&git update-ref $b $c $t||agi-notice add "[trunk-merge-failed] $P: cannot sign or move posts/$P";;
1)l=$(echo "$n"|sed 1d|sed '/^$/q'|grep .|sort -u);m="[trunk-conflict] $P: $(echo "$l"|grep -c .) path(s) conflict with $R: $(echo $l|cut -c1-300)";echo "$m">&2;agi-notice add "$m"
 e=$(echo "$l"|git hash-object --stdin);[ "$(cat ~/.trunk-boxed 2>/dev/null)" = $e ]||{ u=$(git show $T:.agi/nodes/.geometry/posts.md|sed -n 's/^  - {/{/p'|jq -sr --arg p $P 'map({(.name):.})|add as $r|def up(x;n):if n>20 then empty else (($r[x]//{}).parent//empty) as $q|if ($r[$q]//{}|has("harness")) then (if $r[$q].role=="prime_director" then empty else $q end) else up($q;n+1) end end;up($p;0)'|head -1);[ "$u" ]&&echo "$m (trunk $(echo $T|cut -c1-10))"|box send $u;echo $e>~/.trunk-boxed;};;
*)agi-notice add "[trunk-merge-failed] $P: git merge-tree rc $r against $R";;esac;exit 0
~~~

### agi-out (3357 B)
~~~sh
#!/bin/sh
# agi-out (ExecStartPre): the out-line g -> g+1 (AB; the full account is in the node). A ring in ~/t and .fresh newer than the key: new keys in ~/.ssh/n, the capsule share re-wrapped to the next seal FIRST, ONE ring commit signed by the CURRENT key (the self-revocation), then next moves over current. A refusal (any exit after the cd; an AGI_CAPSULE off [A-Za-z0-9._/-], absolute, with .., not resolving to ~/capsule or below) writes its reason to ~/.ssh/out-refused + stderr, exits 75; with that marker and no newer .fresh a start exits 75 silently and the unit's ExecCondition skips it; every other start clears it. Dir 0700, share 0600.
cd||exit 1;m=.ssh/out-refused;[ -e $m ]&&{ [ .fresh -nt $m ]||exit 75;};rm -f $m;x(){ echo "agi-out: $*">&2;echo "$*">$m;exit 75;};P=$AGI_POST;R=.agi/nodes/.geometry/ring;N=.ssh/n;C=${AGI_CAPSULE:+$AGI_CAPSULE/$P}
[ -f t/$R ]&&{ [ -d $N ]||[ .fresh -nt .ssh/id_ed25519 ];}||exit 0
c=$AGI_CAPSULE;[ -z "$c" ]||{ case $c in -*|/*|*..*|*[!A-Za-z0-9._/-]*)x "AGI_CAPSULE off the safe set";;esac;h=$(pwd -P);case $(readlink -m -- "$c") in "$h"/capsule|"$h"/capsule/?*);;*)x "AGI_CAPSULE must resolve under ~/capsule";;esac;}
y='import sys,base64 as B,hashlib as H
from cryptography.hazmat.primitives.asymmetric.x25519 import X25519PrivateKey as K,X25519PublicKey as P
from cryptography.hazmat.primitives.ciphers.aead import ChaCha20Poly1305 as C
a=sys.argv;h=lambda x:H.sha256(x).digest();d=lambda b:B.b64encode(b).decode()
if a[1]=="gen":k=K.generate();open(a[2],"w").write(d(k.private_bytes_raw()));print(d(k.public_key().public_bytes_raw()))
else:
 p,z=open(a[3]).read().split();z=B.b64decode(z);m=C(h(K.from_private_bytes(B.b64decode(open(a[2]).read())).exchange(P.from_public_bytes(z[:32])))).decrypt(bytes(12),z[32:],None);e=K.generate();print(p,d(e.public_key().public_bytes_raw()+C(h(e.exchange(P.from_public_bytes(B.b64decode(a[4]))))).encrypt(bytes(12),m,None)))'
b=refs/heads/posts/$AGI_POST;a=$(git -C t rev-parse -q --verify $b);[ "$a" ]&&o=$(git -C t show $a:$R)||x "the ring is unreadable";umask 77
[ -s $N/seal.pub -a "$(printf '%s\n' "$o"|awk -v p=$P '$1==p&&$2=="x25519"{print $3}')" = "$(cat $N/seal.pub 2>/dev/null)" ]||{
 { [ -f seal.key -a -z "$C" ]||[ -f "$C" -a ! -f seal.key ];}&&x "the capsule share cannot be re-wrapped (no capsule, or no seal key to open it with)"
 rm -rf $N ${C:+"$C.new"};mkdir -p $N ${C:+"$c"}&&ssh-keygen -qN "" -ted25519 -f$N/id_ed25519||{ rm -rf $N;x "keygen failed";}
 s=$(python3 -c "$y" gen $N/seal.key)||{ rm -rf $N;x "seal keygen failed";};echo $s>$N/seal.pub
 [ -f "$C" -a -f seal.key ]&&{ python3 -c "$y" wrap seal.key "$C" $s>"$C.new"||{ rm -rf $N "$C.new";x "the wrap failed";};}
 { printf '%s\n' "$o"|awk -v p=$P 'NF&&$1!=p';printf '%s ssh-ed25519 %s\n%s pq-sha256 %s\n%s x25519 %s\n' $P $(cut -d' ' -f2 $N/id_ed25519.pub) $P $(head -c32 /dev/urandom|base64) $P $s;}>t/$R
 agi-at $R||{ git -C t checkout -q -- $R;[ "$(git -C t show $b:$R|awk -v p=$P '$1==p&&$2=="ssh-ed25519"{print $3}')" = "$(cut -d' ' -f2 $N/id_ed25519.pub)" ]||{ rm -rf $N ${C:+"$C.new"};x "the ring commit failed";};echo "agi-out: the ring commit landed on $b: the new key is kept">&2;}
}
[ -f "$C.new" ]&&mv "$C.new" "$C"
[ -f $N/id_ed25519.pub ]&&{ [ -f $N/id_ed25519 ]&&mv $N/id_ed25519 .ssh/;mv $N/id_ed25519.pub .ssh/;}
[ -f $N/seal.key ]&&mv $N/seal.key seal.key;rm -rf $N
~~~

### gitconfig (196 B)
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
hooksPath=~/bin
[safe]
	directory=*
~~~

### sysusers.conf (41 B)
~~~ini
u agi-@ - "@" /var/lib/agi/@
m agi-@ agi
~~~

### agi.rules (242 B)
~~~js
polkit.addRule(function(a,s){var m=/^agi-post@([a-z0-9-]+)\.service$/.exec(a.lookup("unit"));if(a.id=="org.freedesktop.systemd1.manage-units"&&a.lookup("verb")=="start"&&m&&s.user=="agi-"+m[1]&&s.isInGroup("agi"))return polkit.Result.YES;});
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
grep '^< unit' .agi/drift/$USER|cut -d' ' -f3|grep -x agi-post@${USER#agi-}|xargs -rn1 systemctl start;agi-at .agi/drift
~~~

### agi-frontier (460 B)
~~~sh
#!/bin/sh
r=$1;git grep --all-match -l -e '^type: goal$' -e '^status: active$' $r -- .agi|while IFS=: read _ f;do n=$(git show $r:$f);g=$(echo "$n"|sed -n 's/^id: goal://p')
c=$(echo "$n"|sed -n '/^## Falsifier/,/^## Out/p'|grep -o '`[^`]*`'|tr -d '`'|grep -Em1 '^(grep|test|ls|getent|git (log|show|grep|rev-parse|ls-files|diff|for-each-ref)) ')
[ "$c" ]||{ echo mute $g;continue;};timeout 30 sh -c "$c"</dev/null>/dev/null 2>&1&&echo met $g||echo red $g;done
~~~

### agi-first-start (1394 B)
~~~sh
#!/bin/sh
set -f
# agi-first-start BASE TIP [MSG|-]: FIRST-START: <pieces> = the fenced ### pieces BASE..TIP changes, adds or deletes in the files agi-post@'s ExecStartPre extracts (the unit's AGI_PIECE_GLOB cell, read at each REV: engine.md engine-[pw]*.md, never root/grow); none = "none". With MSG (a file, or - for stdin): rc 1 + REFUSED unless a "first-start:" line says what a post gains and loses.
g(){ git show $1:.agi/nodes/.geometry/engine-root.md|sed -n 's|^Environment="AGI_PIECE_GLOB=\(.*\)"$|\1|p;s|.*for e in \(t/[^;]*\);do for x in.*|\1|;t o;b;:o;s|t/.agi/nodes/.geometry/||g;p'|head -1;}   # the cell; a REV before the cell is read by the old wording
for r in $1 $2;do [ "$(g $r)" ]||{ echo "[no-glob] the extraction line is not in engine-root.md at $r">&2;exit 2;};done
p(){ G=$(g $1)
git ls-tree --full-tree --name-only $1 .agi/nodes/.geometry/|while read f;do for g in $G;do case $f in */$g)git show $1:$f|grep -o "^### [^ ]*"|cut -c5-|while read x;do echo "$x $(git show $1:$f|sed -n "/^### $x /,/^##/{/^~~~/,/^~~~/{//!p}}"|sha1sum)";done;; esac;done;done;}
s=$({ p $1;p $2;}|sort|uniq -u|cut -d' ' -f1|sort -u|tr '\n' ' ');echo "FIRST-START: ${s:-none}"
[ -z "$s" -o -z "$3" ]&&exit 0;grep -qi '^first-start: *[^ ]' $3||{ echo "REFUSED: $1..$2 changes ${s}self-installing piece(s); add a first-start: line (what each post kind gains and loses at its next start)";exit 1;}
~~~

### box (2904 B)
~~~sh
#!/bin/sh
# box send TO <msg | box read | box n | box carry HUB POST.. | box town up|down SHA (belam only): mail = signed commits on refs (doc:radically-simple-engine §AA1)
# out refs/box/P/TO (only P) · in refs/box/*/P · held refs/held/P/FROM (only P) · unread = in --not held
P=${AGI_POST:?};m=refs/box
# the matrix: a and b mail iff their levels differ by <= 1; level = rows up to owner, an inert row (no harness) counts 0
a(){ git show ${AGI_TRUNK:-HEAD}:.agi/nodes/.geometry/posts.md|sed -n 's/^  - {/{/p'|jq -se --arg a $1 --arg b $2 'map({(.name):.})|add as $r|def i(x):$r[x]|has("harness")|not;def l(x;n):if x=="owner" then 0 elif n>20 or $r[x]==null then -99 else (if i(x) then 0 else 1 end)+l($r[x].parent//"";n+1) end;l($a;0) as $x|l($b;0) as $y|$x>0 and $y>0 and ($r[$a]|has("harness")) and ($r[$b]|has("harness")) and $a!=$b and ($x-$y|fabs)<=1'>/dev/null;}
w(){ r=$m/$P/$1;k=0
 until o=$(git rev-parse -q --verify $r);[ -z "$o" ]||git verify-commit --raw $o 2>&1|grep -q "for $P@agi with"||{ echo "[squatted] $r $o: not mine, nothing sent">&2;exit 1;}
  c=$(printf '%s\n' "$b"|GIT_AUTHOR_EMAIL=$P@agi GIT_COMMITTER_EMAIL=$P@agi git commit-tree -S ${o:+-p $o} $(git hash-object -w -t tree /dev/null))&&git update-ref $r $c "$o" 2>/dev/null;do k=$((k+1));[ $k -lt 5 ]||{ echo "[unsent] $r: the tip moved 5 times">&2;exit 1;};done;}
case $1 in
send)a $P $2||{ echo "[off-matrix] $P -> $2: not adjacent, nothing sent">&2;exit 1;};b=$(cat);case $b in "[town]"*)echo "[town] is box town's alone: nothing sent">&2;exit 1;;esac;w $2;;
town)[ "$AGI_POST" = belam ]&&[ "$(id -un)" = agi-belam ]&&[ -n "$AGI_BOX" ]&&[ $# = 3 ]&&case $2 in up|down);;*)false;;esac&&[ ${#3} = 40 ]&&case $3 in *[!0-9a-f]*)false;;esac||{ echo "[town] box town up|down SHA(40 hex), as belam (uid agi-belam) with AGI_BOX set: nothing sent">&2;exit 1;}
 b="[town] $2 $3";for q in $(git show ${AGI_TRUNK:-HEAD}:.agi/nodes/.geometry/posts.md|sed -n 's/^  - {/{/p'|jq -r --arg x "$AGI_BOX" 'select(has("harness") and .box==$x)|.name');do [ $q = belam ]||w $q;done;;
read|n)git for-each-ref --format='%(refname)' $m|grep "/$P$"|while read r;do f=${r#$m/};f=${f%/*};h=refs/held/$P/$f;a $f $P&&j=1||j=0
 for c in $(git rev-list --reverse $r --not $(git rev-parse -q --verify $h));do
  git verify-commit --raw $c 2>&1|grep -q "for $f@agi with"||{ echo "[refused] $f $c";break;}
  b=$(git log -1 --format=%B $c);case $b in "[town]"*)[ $f = belam ]&&[ "$(printf '%s\n' "$b"|wc -l)" = 1 ]&&printf '%s\n' "$b"|grep -qxE '\[town\] (up|down) [0-9a-f]{40}'||{ echo "[town-dropped] $r $c">&2;[ $1 = n ]||git update-ref $h $c;continue;};;*)[ $j = 1 ]||{ echo "[off-matrix] $f";break;};;esac
  [ $1 = n ]&&echo "$f"&&continue;printf '[%s] %s\n' "$f" "$b";git update-ref $h $c;done;done;;
carry)h=$2;shift 2;x=;for p;do git push -q $h "$m/$p/*:$m/$p/*";x="$x ^$m/$p/*";done;git -c transfer.fsckObjects=1 fetch -q $h "$m/*:$m/*" $x;;
esac
~~~

<!-- THOUGHT:BEGIN — authored, not derived; carried across regenerating scans. The reasoning behind THIS version. -->
PROPOSED v5 (round 5, §Q): v4c's body pieces cut whole out of config:engine, byte for byte. SPLIT: agi-post@.service moved to engine-root (root reads it, a post does not).
<!-- THOUGHT:END -->
