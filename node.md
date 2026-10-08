---
id: config:engine-grow
mint_id: fa853170618f4aa2a7a12ffb8f819a1f
type: config
parents:
  - goal:g7.16.1.11.8
next_edges: []
edited_by: belam
scaffold_hash: 2e4a868299b8ee57
season: 2
town: core
---
# config:engine-grow

EXPANSION of config:engine: the hub side: node keys (§Y1: the growth check, the land gate, the projector) + the captive fill window (§Y2)
Read only through `sect <name> [REV]` (a post's extraction loop skips this node). The matrix itself is graph data (`.agi/nodes/.geometry/growth.tsv`, projected by grow-project; the aliases cell beside it), never an engine piece. grow-gate needs agi-fill (`agi-fill check`).

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

### grow-gate (7098 B)
~~~sh
#!/bin/sh
# pre-receive (the land gate), all against the RECEIVING trunk tip (matrix + schemas via git archive):
# ADDED node -> grow-check (order + key; a ring other than * = the commit's signer, §W) + agi-fill check · CHANGED node -> agi-fill
# check as a RATCHET (legacy nodes stay editable)
# the ring (.agi/nodes/.geometry/ring, `post keytype b64` lines): when the RECEIVING tip holds one, a commit lands only if its signer is a ring line open at that tip (AGI_ALLOWED is not read) and an ancestor-or-self of every name ruling each path that differs between the LANDED tip h and the commit, merges and in-push parents included (ring line: its post · node: its ring: cell · schemas, growth.tsv, .github, .gitattributes: AGI_RULES, default owner · posts.md: the old AND new parent of each moved row). No ring at the tip = the old gate ONLY while the ring never existed in the tip's history; once it has, deleting or emptying it answers to every name it removes; no date is read.
# LIMITS: every git read is checked except rn (the ring: cell read; a node WITH NO ring: cell, engine*.md too, needs only a ring signer: ruled: no ring cell, g141-b), pm, $t/u (fail closed). A ring line is exactly the canonical shape or refused; a posts.md name/parent is \A[a-z][a-z0-9-]*\z. Phase 3 runs twice (diff of c; diff(h, c)). A merge-carried node is the trunk's only if its blob equals the RECEIVING tip's; a legacy-invalid trunk node refuses a merge-up carrying it; agi-fill must read a sentinel node as rc 3 via [moral].md at the tip (a crash or a broken owner schema refuses every push). ckpt missing, unreadable or crashing refuses every push. Named, not closed: a mode-only ring change has no ruler line; verify-commit runs gpg/x509 on pushed armour (refused after); no wall clock.
A=${AGI_ALLOWED:?};export LC_ALL=C GIT_NO_REPLACE_OBJECTS=1;set -f;t=$(mktemp -d);trap 'rm -rf $t' EXIT;R=$(git rev-parse -q --verify ${AGI_TRUNK:-refs/heads/main})||{ echo "refused: no receiving trunk";exit 1;}
G=.agi/nodes/.geometry;mkdir -p $t/$G $t/.agi/context/schemas&&git archive $R:.agi/context/schemas|tar -x -C $t/.agi/context/schemas 2>/dev/null||exit 1;git show $R:$G/growth.tsv>$t/$G/growth.tsv||exit 1;command -v agi-fill>/dev/null||{ echo "refused: no agi-fill";exit 1;};k(){ [ "$Z" ]||{ Z=1;printf -- '---\ntype: moral'>$t/z;(cd $t&&agi-fill check z)>$t/e 2>&1;[ $? = 3 ]||die "agi-fill sentinel";};(cd $t&&agi-fill check $1)>$t/e 2>&1;}
lg(){ a=$(git rev-parse -q --verify "$R:$1")&&[ "$a" = "$(git rev-parse "$c:$1")" ];}
E='^[a-z][a-z0-9-]* (ssh-ed25519|ecdsa-sha2-nistp256|pq-sha256|x25519|cert-authority (ssh-ed25519|ecdsa-sha2-nistp256)) [A-Za-z0-9+/]+=*$';ru(){ awk -v s=$1 -v q=$2 '{u[$1]=$2}END{while(q!=""&&n++<40){if(q==s)exit 0;q=u[q]}exit 1}' $t/u;}
rn(){ git show "$h:$1" 2>/dev/null|awk '/^---$/{n++;next} n==1&&/^ring:/{sub(/^ring: *\[/,"");sub(/\].*/,"");gsub(/[ ,]+/," ");print;exit} n>1{exit}';}
pm(){ git show $1:$G/posts.md 2>/dev/null|sed -n 's/^  - {/{/p'|jq -s 'map({(.name):.parent})|add';}
die(){ echo "refused: $c: $*";exit 1;};c=head;:>$t/g;T=;K=${AGI_CKPT:+sh $AGI_CKPT};K=${K:-$(command -v ckpt)};[ "$K" ]||die "ckpt missing";$K check>$t/b||die "ckpt rc $?";T=$(cut -d" " -f2 $t/b|sort -n|tail -1);case $T in *[!0-9]*)die "a holding block names a non-numeric time";;esac;V=$(git rev-list $R --not $(cut -d" " -f1 $t/b) -- $G/ring)||die "git rev-list failed";for v in $V;do git show $v^:$G/ring 2>/dev/null;done>$t/g
dt(){ git diff-tree -r -c --root --no-commit-id "$@">$t/d||die "git diff-tree failed";}
while read o n r;do h=$R;w=$(git rev-list --reverse --topo-order $n --not ${AGI_NOT:---all})&&x=$(git rev-list -1 --full-history $R -- $G/ring)||{ echo "refused: git rev-list failed";exit 1;};L=;[ "$x" ]||L=1;for c in $w;do
 if git show $h:$G/ring>$t/r 2>/dev/null;then L=;cat $t/r $t/g|sort -u|grep -aE "$E"|sed -E 's/^([a-z0-9-]+) cert-authority /\1@agi cert-authority,namespaces="git" /;t;s/^([a-z0-9-]+) /\1@agi namespaces="git" /'>$t/a;else :>$t/a;[ "$L" ]&&{ x=$(git rev-list -1 --full-history $h -- $G/ring)&&[ -z "$x" ]||die "the ring is unreadable at the tip";cp $A $t/a;};fi;git show $h:$G/posts.md 2>/dev/null|sed -n 's/^  - {/{/p'|jq -r 'select(all(.name,.parent;type=="string" and test("\\A[a-z][a-z0-9-]*\\z")))|"\(.name) \(.parent)"'>$t/u
 s=$(git -c gpg.ssh.allowedSignersFile=$t/a verify-commit --raw $c 2>&1|sed -n 's/.*signature for \(.*\)@agi with.*/\1/p')
 [ "$L" -o "$s" ]||{ echo "refused: $c is not signed by a ring line open at the receiving tip";exit 1;}
 [ "$L" -o -z "$T" -o -z "$s" ]||{ git cat-file commit $c|sed '/^gpgsig /,/-END SSH SIGNATURE-----$/d'>$t/m;git cat-file commit $c|sed -n '/^gpgsig /,/-END SSH SIGNATURE-----$/p'|sed 's/^gpgsig //;s/^ //'>$t/s;ssh-keygen -Y verify -f $t/a -I $s@agi -n git -Overify-time=$(date -u -d @$T +%Y%m%d%H%M%SZ) -s $t/s<$t/m>/dev/null 2>&1||die "its signature is not valid at the newest holding block's time";}
 dt --diff-filter=AMT $h $c;(while IFS= read -r l;do p=${l#*	};o=$(echo "${l%%	*}"|awk '{print $(NF-1)}');git cat-file blob $o>$t/b||{ echo "refused: $c $p unreadable";exit 1;};grep -aq -e '-----BEGIN [A-Z0-9 ]*PRIVATE KEY-----' $t/b&&{ echo "refused: $c $p carries a private key block (the trunk is public)";exit 1;};case $p in $G/ring/*)echo "refused: $c $p: the ring is one file";exit 1;;$G/ring)[ "$s" ]||die "the ring is changed by an unsigned commit";git show $c:$p>$t/g2&&{ grep -aEqv "$E" $t/g2;[ $? = 1 ];}||die "a ring line off shape";;esac;done<$t/d)||exit 1
 [ "$L" ]||{ dt --name-only $h $c;(while IFS= read -r f;do case $f in \"*)echo "refused: $c $f: a quoted path";exit 1;;
  $G/ring)git diff --text $h $c -- "$f">$t/q||die "git diff failed";r=$(sed -n 's/^[-+]\([a-z][a-z0-9-]*\) .*/\1/p' $t/q|sort -u);;
  .agi/context/schemas/*|$G/growth.tsv|.github/*|.gitattributes|*/.gitattributes)r=${AGI_RULES:-owner};;
  $G/posts.md)pm $h>$t/o;pm $c>$t/n;jq -e '[keys[],(.[]|select(.!=null))]|all(test("\\A[a-z][a-z0-9-]*\\z"))' $t/n>/dev/null||die "a posts.md name off [a-z0-9-]";r=$(jq -rn --slurpfile o $t/o --slurpfile n $t/n '$o[0] as $o|$n[0] as $n|($o+$n|keys[]) as $k|select($o[$k]!=$n[$k])|$o[$k],$n[$k]|select(.!=null)')||die "the posts.md ruler failed";;
  *)r=$(rn "$f");;esac
  for q in $r;do ru $s $q||{ echo "refused: $c $f is ruled by $q; ${s:-nobody} is not $q or above it";exit 1;};done;done<$t/d)||exit 1;}
 for y in "$c" "$h $c";do dt --diff-filter=AMT --name-status $y -- .agi/nodes;grep '\.md$' $t/d|grep -v /deprecated/>$t/l;b=${y%% *};[ $b = $c ]&&b=$c^
 while read m f;do [ "$y" != "$c" ]&&lg "$f"&&m=M;z=$(git ls-tree $c -- "$f")||die "$f: ls-tree failed";case $z in 12*)echo "refused: $c $f: a symlink node";exit 1;;esac;git show "$c:$f">$t/n||die "$f unreadable";if [ "${m#*A}" != "$m" ];then v=$(grow-check $t/.agi/nodes/.geometry/growth.tsv $t/n)||{ echo "$f: $v";exit 1;}
  g=${v##* };[ "$g" = '*' ]||[ "$g" = "$s" ]||{ echo "$f: ring $g, signed by ${s:-nobody}";exit 1;};k n||{ echo "$f:";cat $t/e;exit 1;}
  else k n||{ git show "$b:$f">$t/p&&! k p||{ echo "$f: was valid:";k n;cat $t/e;exit 1;};};fi;done<$t/l||exit 1;done;h=$c;done;done
~~~

### ckpt (3444 B)
~~~sh
#!/bin/sh
# ckpt sign POST KEY TIP TIME | ckpt check: a BLOCK = a commit under refs/agi/block/*: files tip, time, hash ("<AGI_HASH> <digest of git archive tip>"), sigs/<post>.<n> over "tip time hash digest" (namespace agi-checkpoint); its git PARENTS are the blocks it seals
# it holds iff: its tree is ONLY tip, time, hash, sigs/<post>.<n> (so every path is plain ASCII: the AGI_SUBJECT recipe never parses an odd name) · every signer is current in the ring AT ITS TIP in every algorithm of AGI_SIGN (hybrid = AND) · the signers are PAIRWISE level-adjacent (level = rows up to owner, an inert row counts 0, owner = 0) · their number >= AGI_CKK's k for the block's lowest level ("0:2 1:2 2:2 3:2", default 2) · every parent's tip is an ancestor of its tip. check prints "<tip> <time>" for EVERY holding block · a bad tip or time = the block is skipped · only gate-shaped ring lines count · a signer whose level cannot be read does not count · a key counts once however many names list it · check exits 1 only when a listing step fails
G=.agi/nodes/.geometry;t=$(mktemp -d);trap 'rm -rf $t' EXIT;H=${AGI_HASH:-sha256};set -f
d(){ echo "$1 $2 $H $(git archive --format=tar "$1"|${H}sum|cut -d' ' -f1)"; }
v(){ case $1 in ''|*[!0-9a-f]*)return 1;esac;case ${#1} in 40|64)git cat-file -e "$1^{commit}";;*)return 1;esac; }
lv(){ git show $1:$G/posts.md|sed -n 's/^  - {/{/p'|jq -rs --arg a $2 'map({(.name):.})|add as $r|def l(x;n):if x=="owner" then 0 elif n>20 or $r[x]==null then -99 else (if $r[x]|has("harness") then 1 else 0 end)+l($r[x].parent//"";n+1) end;l($a;0)'; }
case $1 in sign) d "$4" "$5">$t/m;ssh-keygen -q -Y sign -n agi-checkpoint -f $3 $t/m&&cat $t/m.sig;;
check) L=$(git for-each-ref --format='%(objectname)' refs/agi/block)||exit 1;B=;[ "$L" ]&&{ B=$(git rev-list $L)||exit 1;}
for c in $B;do git ls-tree -r --name-only $c|grep -qvE '^(tip|time|hash|sigs/[a-z0-9-]+\.[0-9]+)$'&&continue;x=$(git show $c:tip) y=$(git show $c:time) H=$(git show $c:hash|cut -d" " -f1);case $y in ''|*[!0-9]*)continue;esac;v "$x"||continue;case " ${AGI_HASHES:-sha256 sha384 sha512} " in *" $H "*);;*)continue;;esac;[ "$(git show $c:hash)" = "$(d "$x" "$y"|cut -d' ' -f3-)" ]||continue;d "$x" "$y">$t/m
 for q in $(git rev-parse $c^@);do w=$(git show $q:tip);v "$w"&&git merge-base --is-ancestor "$w" "$x"||continue 2;done
 git show "$x:$G/ring"|grep -aE '^[a-z][a-z0-9-]* (ssh-ed25519|ecdsa-sha2-nistp256|pq-sha256|x25519|cert-authority (ssh-ed25519|ecdsa-sha2-nistp256)) [A-Za-z0-9+/]+=*$'|sed -E 's/^([a-z0-9-]+) cert-authority /\1@agi cert-authority,namespaces="agi-checkpoint" /;t;s/^([a-z0-9-]+) /\1@agi namespaces="agi-checkpoint" /'>$t/a;:>$t/l
 for p in $(git ls-tree --name-only $c sigs/|sed 's|sigs/||;s|\.[0-9]*$||'|sort -u);do for f in $(git ls-tree --name-only $c sigs/|grep "^sigs/$p\.");do git show $c:$f>$t/s
  ssh-keygen -Y verify -f $t/a -I $p@agi -n agi-checkpoint -s $t/s<$t/m 2>/dev/null|sed -n 's/.* with \([A-Z0-9-]*\) key \([^ ]*\).*/\1 \2/p';done|sort -u>$t/k
  for a in ${AGI_SIGN:-ED25519};do grep -q "^$a " $t/k||continue 2;done;l=$(lv "$x" $p)&&[ "$l" ]||continue;echo "$l $(cut -d' ' -f2 $t/k|sort -u|tr '\n' ' ')">>$t/l;done
 sort -n $t/l|awk -v K=" ${AGI_CKK:-} " '$1<0{exit 1}{u=1;for(i=2;i<=NF;i++)if($i in S)u=0;for(i=2;i<=NF;i++)S[$i];if(u){if(!n++)m=$1;M=$1}}END{k=2;if(match(K," "m":[0-9]+"))k=substr(K,RSTART+length(m)+2,RLENGTH-length(m)-2);exit !(n&&M-m<=1&&n>=k)}'&&echo "$x $y $c";done;:;;esac
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

<!-- THOUGHT:BEGIN — authored, not derived; carried across regenerating scans. The reasoning behind THIS version. -->
ROUND 7 (§Y1/§Y2): the three growth tools byte for byte from the doc (grow-check 1298 B, grow-gate 1435 B (1465 B since the AA3.4 byte fixes; 3,783 B since the AA2.54 ring-gate folded into the commit loop: the signer must be a ring line open at the RECEIVING tip and an ancestor-or-self of every name ruling each changed path; no ring at the tip = the old AGI_ALLOWED gate; 1,833 B before that, since the AA2 per-commit private-key line: AA1.K's pattern, per path over the raw non-z diff-tree lines so a newline path cannot split, --diff-filter=AMT, an unreadable blob refuses and names the path; was 1,748 B with AA1.K's verbatim line, mur sm17 R1/R2), grow-project 1185 B), + agi-fill (§Y2 + the corrective diagram + the const seam fix) moved here whole (SPLIT, byte for byte). Why: a post's start read = engine + engine-post + engine-wrap <= 20,480 B, and the hub's = engine + this node.
<!-- THOUGHT:END -->
