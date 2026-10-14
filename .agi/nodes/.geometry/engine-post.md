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
agi-brief         1358 B  walk card+seeds+claims; record; STARTUP
brief.py           810 B  the complex walk over parents: edges
agi-meter          616 B  past rotate_pct of the window: out-line
agi-at             996 B  signed CAS commit of ~/t paths to posts/<P>
grow.py           3228 B  the growth-order check both writers call
agi-turn           4486 B  a signed commit per changed node tree
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
box               2019 B  mail: one signed ref update per send (5x CAS)
~~~

## files — depth 2, each whole; extract: sect <name> [REV]

### agi-brief (1358 B)
~~~sh
#!/bin/sh
ls ~/.notice* >/dev/null 2>&1&&agi-notice;p=$AGI_POST;cd ~/t;s=$(jq -r .source);case $AGI_HARNESS in pi*)B=${B:-40000};;esac
sect brief.py|python3 - .agi/nodes doc:card-$p,$AGI_SEEDS$(find $(git rev-parse --git-common-dir)/refs/claims -user $USER -printf ,%f 2>/dev/null) ${K:-20}>~/.brief;cat ~/.brief;cut -d' ' -f4 ~/.brief|xargs tail -n+1|head -c ${B:-0}
w=${AGI_WT:-$RUNTIME_DIRECTORY/wt};x=$(git rev-parse -q --verify refs/heads/posts/${AGI_POST:-$p});for r in $(git for-each-ref --format='%(refname)' refs/archive/${AGI_POST:-$p});do git log --format=%s $r ${x:+--not $x}|grep -q '^[^ ]*: kept '&&echo "[kept] $r: a stop left this tree whole; recover it, then git update-ref -d it";done;ls -d $w/*/ 2>/dev/null|sed 's/^/[tree] /'
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

### agi-meter (616 B)
~~~sh
#!/bin/sh
ls ~/.notice* >/dev/null 2>&1&&agi-notice;j=$(cat);t=$(echo "$j"|jq '.tokens//empty');[ "$t" ]||t=$(echo "$j"|jq -r .transcript_path|xargs tac 2>/dev/null|jq -nR 'first(inputs|fromjson?|select((.message.usage.input_tokens)?|type=="number")|.message.usage|.input_tokens+((.cache_read_input_tokens|numbers)//0)+((.cache_creation_input_tokens|numbers)//0))');w=$(echo "$j"|jq ".context_window//${AGI_WINDOW:-1000000}")
[ "${t:-0}" -gt $((w*${AGI_ROTATE_PCT:-47}/100)) ] 2>/dev/null&&echo "At the line ($t/$w): write your card in its node tree (agi-wt pull), run agi-flush, then: touch ~/.fresh;kill \$PPID";:
~~~

### agi-at (996 B)
~~~sh
#!/bin/sh
# agi-at PATH...: ONE signed commit of ~/t's paths onto posts/P by CAS on the tip read; a miss = [raced], exit 4, the edit stays; a kid, no AGI_POST or no posts/P = rc 5 before any write; a NEW .agi/nodes node must pass grow.py first, else rc 6 (the edit stays); once the CAS landed the final reset is best-effort (a failed one = [reset], rc 0); ~/t = a detached view of the tip
cd ~/t;P=$AGI_POST;b=refs/heads/posts/$P;{ [ "$P" ]&&[ "$AGI_ROLE" != kid ]&&git rev-parse -q --verify $b>/dev/null;}||{ echo "[no-branch] $P: a kid, or no posts/$P: nothing committed">&2;exit 5;};x=$(mktemp -u);trap 'rm -f $x' 0;export GIT_INDEX_FILE=$x;t=$(git rev-parse $b)&&git read-tree $t&&git add -A -- "$@"&&n=$(git write-tree)||exit 1
grow.py $t>&2||exit 6
[ $n = $(git rev-parse $t^{tree}) ]&&exit;c=$(echo "$P: $*"|git commit-tree -S -p $t $n)&&git update-ref $b $c $t||{ echo "[raced] $*">&2;exit 4;}
unset GIT_INDEX_FILE;git reset -q $b||echo "[reset] $b: the commit landed, HEAD not moved">&2
~~~

### grow.py (3228 B)
~~~python
#!/usr/bin/env python3
# grow.py TIP: the ONE growth-order check agi-turn and agi-at call on the temp index (GIT_INDEX_FILE) after the tree is written and before the commit. Every NEW .agi/nodes/**.md (an add against TIP, --no-renames, not under deprecated/; an edit is never gated) is read from its STAGED blob (diff-index -z read as BYTES: raw NUL-split paths, never C-quoted, no newline translation; strict UTF-8) and checked in-process: its parents must resolve in the STAGED tree (a parent added in the same tree counts, except a NEW add under deprecated/; a decoy file in ~/t does not; none = refused), then spawn_gate.check_spawn must APPROVE it (REJECTED, UNVERIFIED and an unknown type are all refused), so a new node is APPROVED or REFUSED, never committed unchecked. rc 0 = pass; 1 = [growth-order] <node> (one line per refusal); 3 = [spawn-gate-missing] / [spawn-gate-broken] (an absent or crashing checker, a failed git, a non-UTF-8 path or blob: FAILS CLOSED)
import sys,os,re,subprocess as S
sys.dont_write_bytecode=True
b=0
try:
 A=[p for p in(q.decode() for q in S.run(["git","diff-index","-z","--cached","--no-renames","--name-only","--diff-filter=A",sys.argv[1],"--",".agi/nodes"],capture_output=True,check=True).stdout.split(b"\0")) if p.endswith(".md")]
 L=[p for p in A if not p.startswith(".agi/nodes/deprecated/")];D={p.encode() for p in A}-{p.encode() for p in L}
 if L and not os.path.exists("extensions/agi/bin/spawn_gate.py"):print("[spawn-gate-missing] extensions/agi/bin/spawn_gate.py is not in ~/t: %d new node(s) not checked"%len(L));b=3
 elif L:
  sys.path.insert(0,"extensions/agi/bin");import spawn_gate as g,frontmatter as f
  d=g.Path(".agi").joinpath(*g.SCHEMAS_SUBDIR);R=g.load_spawn_rules(d,root=g.Path(".agi"));C=g.read_ladder_season(g.resolve_nodes_root(g.Path(".agi"),d))
  r=S.run(["git","grep","--cached","-aznE",r"^(---\s*$|(id|mint_id|type):)","--",".agi/nodes/*.md"],capture_output=True);assert r.returncode<2,r.stderr
  F={};I={}
  for x,n,t in re.findall(rb"([^\0]+)\0(\d+)\0([^\n]*)\n",r.stdout):
   if x in D:continue
   e=F.setdefault(x,{"f":0});t=t.decode("utf-8","surrogateescape")
   if t.rstrip()=="---":e["f"]+=1 if(e["f"] or n==b"1")else 2
   elif e["f"]==1:k,_,v=t.partition(":");e.setdefault(k,v.strip().strip("\"'"))
  for e in F.values():
   for k in("id","mint_id"):
    if e.get(k):I[e[k]]=g.canonical_type(e.get("type"))
  for p in L:
   m=f.read_frontmatter(S.run(["git","show",":"+p],capture_output=True,check=True).stdout.decode())
   if m is None:print("[growth-order] "+p+": no readable front matter");b=1;continue
   q=m.get("parents") or []
   if not isinstance(q,list) or [y for y in q if y not in I]:print("[growth-order] %s: parent(s) %s resolve nowhere in the staged tree"%(m.get("id") or p,q if not isinstance(q,list) else [y for y in q if y not in I]));b=1;continue
   r=g.check_spawn(m.get("type"),q,rules=R,type_index=I,fm=m,node_id=m.get("id") or p,season_parents=m.get("season_parents"),current_season=C)
   if r.status!=g.APPROVED:print("[growth-order] "+re.sub(r"^SPAWN-GATE \w+: ","",(r.messages or [r.reason])[0]).split(" Schema:")[0]);b=1
except BaseException as e:print("[spawn-gate-broken] spawn_gate.py: "+repr(e)[:160]);b=3
sys.exit(b)
~~~

### agi-turn (4486 B)
~~~sh
#!/bin/sh
# agi-turn: each changed node tree = ONE grid commit on posts/P (temp index from the tip, signed, CAS); the tip moved it since pull = archived + dropped; a tree is purged ONLY once its commit is proven AND the whole tree is clean against it (agi-turn chk DIR COMMIT: a file outside .p keeps it, [dirty]; a git failure keeps it too); agi-turn purge DIR = that check then rm, else EVERY file of the tree goes to refs/archive/P/<dir> (signed, CAS), [kept] names it, rc 1; a kid (AGI_ROLE=kid, which agi-kid sets), no AGI_POST or no posts/P = rc 5, nothing committed (the SAME guard line before any WRITE in agi-at, agi-turn and agi-flush (chk and c() only read, so they run before it); agi-sync runs at the end of EVERY turn, before the detach: the trunk is merged each turn or its conflict said by name; a Stop hook must never exit 2); the staged tree goes through grow.py (a NEW .agi/nodes node must pass spawn_gate; an edit never does; a refusal or a broken checker = ONE bracketed line, rc 1, nothing committed, the tree kept); BEFORE the detach, `agi-turn strand` (agi-flush calls it too, ONE guard): a detached HEAD that carries commits on no ref is REFUSED by name ([strand-refused], rc 1, HEAD left where it is; it never folds: agi-at is the one write path); [strand-refused] and [out-of-tree] go to stderr AND, through `agi-notice add` (one line per distinct notice), to ~/.notice, which agi-notice (called first by agi-brief and agi-meter) claims and prints once on stdout into the post's context; any failure keeps the tree (rc != 0, a [label]); ~/t = a detached read view
cd ~/t;P=$AGI_POST;b=refs/heads/posts/$P;x=$(mktemp -u);trap 'rm -f $x $x.l' 0;export GIT_INDEX_FILE=$x;k=0
c(){ [ "$2" ]&&git read-tree $2&&git --work-tree=$1 diff --name-only --diff-filter=MT>$x.l&&git --work-tree=$1 ls-files -o>>$x.l||return 2;l=$(grep -vxF -e .p -e .b $x.l|tr '\n' ' ');[ -z "$l" ];}
[ "$1" = chk ]&&{ c $2 $3;r=$?;[ $r = 0 ]&&exit;[ $r = 1 ]&&echo "[dirty] $(basename $2): kept, not in the commit: $l">&2||echo "[dirty] $(basename $2): kept, cannot read it against '$3'">&2;exit 1;}
{ [ "$P" ]&&[ "$AGI_ROLE" != kid ]&&git rev-parse -q --verify $b>/dev/null;}||{ echo "[no-branch] $P: a kid, or no posts/$P: nothing committed">&2;exit 5;}
[ "$1" = strand ]&&{ git symbolic-ref -q HEAD>/dev/null&&exit;h=$(git rev-parse -q --verify HEAD)||exit 0;n=$({ echo $h;git for-each-ref --format='^%(objectname)' refs/heads refs/remotes refs/archive refs/tags;}|git rev-list --count --stdin);[ $n = 0 ]&&exit
 m="[strand-refused] $P: HEAD $(git rev-parse --short $h) carries $n commit(s) on no ref: HEAD left where it is, nothing moved; put them on posts/$P through agi-at";echo "$m">&2;agi-notice add "$m";exit 1;}
[ "$1" = purge ]&&{ d=${2%/};m=${d##*/};c $d $(cat $d/.b 2>/dev/null||git rev-parse $b);[ $? = 0 ]&&{ rm -rf $d;exit;};a=refs/archive/$P/$m;o=$(git rev-parse -q --verify $a||:)
 t=$(git rev-parse $b)&&git read-tree $t&&git --work-tree=$d add --ignore-removal -f -- . ':!.p' ':!.b'&&n=$(git write-tree)&&e=$(echo "$P: kept $m"|git commit-tree -S -p $t ${o:+-p $o} $n)&&git update-ref $a $e "$o"&&s="whole tree committed to $a"||s="NOT SAVED: the ref write failed";echo "[kept] $m: ${l:-unreadable}: $s">&2;exit 1;}
for d in ${AGI_WT:-$RUNTIME_DIRECTORY/wt}/*/;do [ -f $d.p ]||continue;m=$(basename $d);t=$(git rev-parse $b)&&git read-tree $t&&a=$(git --work-tree=$d add -A --pathspec-from-file=$d.p 2>&1)&&n=$(git write-tree)||{ echo "[stage] $m: $(echo "${a:-git failed}"|tr '\n' ' ')">&2;k=1;continue;}
 [ $n = $(git rev-parse $t^{tree}) ]&&continue;grow.py $t>&2||{ k=1;continue;};r=$b;o=$t;q=;[ ! -f $d.b ]||(IFS='
';set -f;git diff --quiet $(cat $d.b) $t -- $(cat $d.p))||{ r=refs/archive/$P/$m;o=$(git rev-parse -q --verify $r||:);q=${o:+-p $o};}
 c=$(echo "$P: $(sed q $d.p)"|git commit-tree -S -p $t $q $n 2>&1)||{ echo "[commit] $m: cannot sign or commit: $c">&2;k=1;continue;}
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

### box (2019 B)
~~~sh
#!/bin/sh
# box send TO <msg | box read | box n | box carry HUB POST..: mail = signed commits on refs (doc:radically-simple-engine §AA1)
# out refs/box/P/TO (only P) · in refs/box/*/P · held refs/held/P/FROM (only P) · unread = in --not held
P=${AGI_POST:?};m=refs/box
# the matrix: a and b mail iff their levels differ by <= 1; level = rows up to owner, an inert row (no harness) counts 0
a(){ git show ${AGI_TRUNK:-HEAD}:.agi/nodes/.geometry/posts.md|sed -n 's/^  - {/{/p'|jq -se --arg a $1 --arg b $2 'map({(.name):.})|add as $r|def i(x):$r[x]|has("harness")|not;def l(x;n):if x=="owner" then 0 elif n>20 or $r[x]==null then -99 else (if i(x) then 0 else 1 end)+l($r[x].parent//"";n+1) end;l($a;0) as $x|l($b;0) as $y|$x>0 and $y>0 and ($r[$a]|has("harness")) and ($r[$b]|has("harness")) and $a!=$b and ($x-$y|fabs)<=1'>/dev/null;}
case $1 in
send)a $P $2||{ echo "[off-matrix] $P -> $2: not adjacent, nothing sent">&2;exit 1;};r=$m/$P/$2;b=$(cat);k=0
 until o=$(git rev-parse -q --verify $r);[ -z "$o" ]||git verify-commit --raw $o 2>&1|grep -q "for $P@agi with"||{ echo "[squatted] $r $o: not mine, nothing sent">&2;exit 1;}
  c=$(printf '%s\n' "$b"|GIT_AUTHOR_EMAIL=$P@agi GIT_COMMITTER_EMAIL=$P@agi git commit-tree -S ${o:+-p $o} $(git hash-object -w -t tree /dev/null))&&git update-ref $r $c "$o" 2>/dev/null;do k=$((k+1));[ $k -lt 5 ]||{ echo "[unsent] $r: the tip moved 5 times">&2;exit 1;};done;;
read|n)git for-each-ref --format='%(refname)' $m|grep "/$P$"|while read r;do f=${r#$m/};f=${f%/*};h=refs/held/$P/$f
 a $f $P||{ echo "[off-matrix] $f";continue;}
 for c in $(git rev-list --reverse $r --not $(git rev-parse -q --verify $h));do
  git verify-commit --raw $c 2>&1|grep -q "for $f@agi with"||{ echo "[refused] $f $c";break;}
  [ $1 = n ]&&echo "$f"&&continue;printf '[%s] %s\n' "$f" "$(git log -1 --format=%B $c)";git update-ref $h $c;done;done;;
carry)h=$2;shift 2;x=;for p;do git push -q $h "$m/$p/*:$m/$p/*";x="$x ^$m/$p/*";done;git -c transfer.fsckObjects=1 fetch -q $h "$m/*:$m/*" $x;;
esac
~~~

<!-- THOUGHT:BEGIN — authored, not derived; carried across regenerating scans. The reasoning behind THIS version. -->
PROPOSED v5 (round 5, §Q): v4c's body pieces cut whole out of config:engine, byte for byte. SPLIT: agi-post@.service moved to engine-root (root reads it, a post does not).
<!-- THOUGHT:END -->
