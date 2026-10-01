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
ROUND 7 (§Y1/§Y2): the three growth tools byte for byte from the doc (grow-check 1298 B, grow-gate 1435 B, grow-project 1185 B), + agi-fill (§Y2 + the corrective diagram + the const seam fix) moved here whole (SPLIT, byte for byte). Why: a post's start read = engine + engine-post + engine-wrap <= 20,480 B, and the hub's = engine + this node.
<!-- THOUGHT:END -->
