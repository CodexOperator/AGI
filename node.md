---
id: doc:draft-paper-v0
mint_id: abc168ad2e814a0887d49794f678c79f
type: doc
parents:
  - goal:g5.4.3.2
next_edges: []
edited_by: meme-master
season: 3
tags:
  - draft
title: "DRAFT class paper -- POINTER to the private draft (no text; reader copy v0.1, current v0.3), for thought-master's team and council (goal:g5.4.3.2)"
town: core
---
# doc:draft-paper-v0

POINTER, not the text. The owner's class paper DRAFT v0.1 (a graded MATH-class paper, not yet submitted) is NOT copied into the graph: every land is pushed to the public origin, and publishing the draft before submission is the owner's call (banked for him by sanctuary-master 06:5xZ 11-17). Every sentence of it is an agent's DRAFT for the owner to rewrite in his own words.

source: meme-master private ~/meme-photos/paper/paper.tex. v0.1, the reader copy L608's experiments read, is sha256 ec794f9085bfc558182349013727b8795d3d98697ad5700475fa5e39b64835a0.
current: DRAFT v0.3 (11-17/18), the same private path, tex sha256 84c4f6f5184d, PDF sha256 061e42247c9c, in the owner's Drive (belam's upload 11-17 23:55Z). It folds the verdicts of L608's three experiments: P1 (verdict:paper-proofs-hold, the omitted hypotheses in results 4, 5 and 8), P2 (verdict:paper-numbers-rederive, the numbers below) and P3 (verdict:paper-meets-rubric, the scorers' row fixes), plus the readers' and judges' leads. It holds no text in the graph.
reader copies, OUTSIDE every repo, sha256 ec794f9085bf (paper.tex) / cdf81f453c0f (paper.pdf):
- encryption-town (group agi): /data/scratch/meme-master/paper-build/paper.tex
- local-town, inside the lab container (group = the 8 lab posts; placed by belam 10:08Z): /data/scratch/paper-reader/paper.tex
Never copy it into ~/t, a node, a box message or any pushed ref.
numbers: graphstats.py (below; quoted-id fix, plasma 11-17; parents pattern `\s*-\s+`, the fix from verdict:paper-numbers-rederive, L623) on a clean git archive of the pin 3673f941d2 (present on both boxes), re-measured 11-17 21:4xZ: live 5,890 / retired 255; parent edges 6,801; live nodes by parent count 0 / 1 / 2 / 3+ = 98 / 5,080 / 690 / 22 (sum 5,890); non-moral live roots 92; dangling parent refs 0; 1 cycle; depth max 20, mean 5.55; ancestor set mean 9.52, median 9, p95 16, max 41; leaves 3,676; commits reachable from the pin 26,319, all on or after 2026-04-30 (the 26,223 printed here before was wrong; P2's Notes). The script before the parents fix read 6,798 edges and 3,677 leaves: superseded. v0.1 (before the fix, at d7985199d4) printed 66 dangling and mean depth 5.47: superseded.
method note: graphstats.py reads the first 4000 characters of each node file; on trunk 299fb19413, 189 of 6144 nodes run past that, but 0 parent refs and 0 ids are lost (remix, measured 11-17).

## Sections
- Introduction
- Background
- Definitions
- Results
- Measuring the live graph
- How we will know it helped
- Conclusion
- A note on how this paper was made

## Rubric (owner, 11-17)
Appropriate Topic (Mathematical Depth) 15 · Abstract 5 · Clarity (organized, visually easy to follow, correct grammar and mathematical notation) 15 · Development of Ideas (appropriate background discussion, examples when necessary) 15 · Support for Main Ideas (necessary definitions, theorems, examples) 15 · Sense of Problem Solving Process (uses definitions and theorems correctly, correct overall logic) 15 · Shows Understanding of Overall Topic (big picture clear, pieces fit together) 15 · Conclusion 5 · Total 100.

## Results in the reader copy (counts from its bytes, plasma 11-17)
8 results (3 theorems, 4 propositions, 1 corollary), 7 proof blocks (the corollary has none), 7 examples, 2 uses of the TM placeholder macro, 4 of the draft-note macro.
Thm channels (n-1 vs C(n,2)) · Thm topological order iff acyclic + Cor parents-first · Prop p^k compounding · Prop checkpoints · Thm 3-vote q(p)-p = p(1-p)(2p-1) · Prop best-of-k limit mu(p>0) · Prop ancestor read bound · sign test example (n=12, P[X>=10] = 79/4096).

## Placeholders (folded into hypothesis:paper-numbers-rederive)
[TM: lands per day] · [TM: per-node token size s(u)] · [TM: small-model vs reference, only if measured] · [TM: the deck A/B result, from SM's blind, later].

## graphstats.py (the measurement behind the data table)
Run from the repo root: `python3 -I graphstats.py`.
````python
import os,re,collections,statistics,json
R='.agi/nodes'
nodes={};dep=0
for d,_,fs in os.walk(R):
    if '/.' in d: continue
    for f in fs:
        if not f.endswith('.md'): continue
        p=os.path.join(d,f); t=open(p,errors='ignore').read(4000)
        if not t.startswith('---'): continue
        fm=t.split('---',2)[1]
        m=re.search(r'^id:\s*(\S+)',fm,re.M)
        if not m: continue
        ps=[]
        # stop parents list at next key
        if 'parents:' in fm:
            blk=fm.split('parents:',1)[1]
            lines=blk.split('\n')[1:]; ps=[]
            for l in lines:
                mm=re.match(r'\s*-\s+(\S+)',l)
                if mm: ps.append(mm.group(1).strip('"\''))
                else: break
        st=re.search(r'^status:\s*(\S+)',fm,re.M)
        nid=m.group(1).strip('"\'');nodes[nid]={'type':nid.split(':')[0],'parents':ps,'dep':'/deprecated/' in p,'status':st.group(1) if st else ''}
live={k:v for k,v in nodes.items() if not v['dep']}
print('total',len(nodes),'live',len(live),'deprecated',len(nodes)-len(live))
print('live by type',collections.Counter(v['type'] for v in live.values()).most_common())
E=sum(len(v['parents']) for v in nodes.values()); print('parent edges (all)',E)
pc=collections.Counter(len(v['parents']) for v in live.values()); print('live parent-count dist',sorted(pc.items()))
roots=[k for k,v in live.items() if not v['parents']]; print('live roots by type',collections.Counter(nodes[k]['type'] for k in roots))
dangling=sum(1 for v in nodes.values() for p in v['parents'] if p not in nodes); print('dangling parent refs',dangling)
# cycle check + depth from roots (longest path via memo)
import sys; sys.setrecursionlimit(100000)
memo={};state={}
cyc=[0]
def depth(k):
    if k in memo: return memo[k]
    if state.get(k)==1: cyc[0]+=1; return 0
    state[k]=1
    ps=[p for p in nodes.get(k,{'parents':[]})['parents'] if p in nodes]
    d=0 if not ps else 1+max(depth(p) for p in ps)
    state[k]=2; memo[k]=d; return d
ds=[depth(k) for k in live]; print('cycles hit',cyc[0],'max depth',max(ds),'mean depth',round(statistics.mean(ds),2))
print('depth dist',sorted(collections.Counter(ds).items())[:25])
ch=collections.Counter(p for v in live.values() for p in v['parents'])
vals=[ch.get(k,0) for k in live]; inner=[x for x in vals if x>0]
print('children per live node: mean',round(statistics.mean(vals),2),'leaves',vals.count(0),'internal mean',round(statistics.mean(inner),2),'max',max(vals))
print('goal status',collections.Counter(v['status'] for v in live.values() if v['type']=='goal'))
print('hyp/verdict', {t:sum(1 for v in nodes.values() if v['type']==t) for t in ['hypothesis','experiment','verdict','mvp','outcome','idea']})
amemo={}
def anc(k,seen=None):
    if k in amemo: return amemo[k]
    out=set(); stack=[p for p in nodes[k]['parents'] if p in nodes]
    while stack:
        x=stack.pop()
        if x in out: continue
        out.add(x); stack+= [p for p in nodes[x]['parents'] if p in nodes]
    amemo[k]=out; return out
A=[len(anc(k)) for k in live]
print('ancestor set: mean',round(statistics.mean(A),2),'median',statistics.median(A),'max',max(A),'p95',sorted(A)[int(.95*len(A))])
norm=lambda t:{'exp':'experiment','hyp':'hypothesis'}.get(t.strip('"'),t.strip('"'))
print('live by type (normalized)',collections.Counter(norm(v['type']) for v in live.values()).most_common())
cyc=[]
for k in nodes:
    if k in anc(k): cyc.append(k)
print('nodes on a cycle',cyc[:6])
print('non-moral live roots',sum(1 for k in roots if norm(nodes[k]['type'])!='moral'))
````

<!-- THOUGHT:BEGIN — authored, not derived; carried across regenerating scans. The reasoning behind THIS version. -->
Pointer moved to DRAFT v0.3 by meme-master 11-18 00:0xZ, after all three verdicts landed (L623, L624, L627): the source line names v0.1 as the reader copy and v0.3 as current, by sha only. Script: the dead first parents pattern (always overwritten by the per-line loop) is now ps=[] (less-is-more); the numbers line prints the 3+ parents count so the row sums to 5,890 (remix). Still zero paper text.
<!-- THOUGHT:END -->
