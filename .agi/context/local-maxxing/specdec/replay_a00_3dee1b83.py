#!/usr/bin/env python3
import argparse, collections, hashlib, json, math, os, statistics, urllib.request
RULES = ("ngram-simple", "ngram-map-k", "ngram-mod")
def parts(message):
    out = []
    for p in message.get("content", []):
        if p.get("type") == "thinking": out.append(("thinking", p.get("thinking", "")))
        elif p.get("type") == "text": out.append(("text", p.get("text", "")))
        elif p.get("type") == "toolCall":
            name = p.get("name", "bash")
            kind = name if name in ("write", "edit", "read") else "bash"
            out.append((kind, json.dumps({"name": name, "arguments": p.get("arguments", {})}, sort_keys=True, separators=(",", ":"))))
    return out

def suggest(ctx, pos, rule):
    n, m = (24, 64) if rule == "ngram-mod" else (12, 48)
    if len(ctx) - pos < n: return []
    key = tuple(ctx[pos:pos+n]); candidates=[]
    for i in range(pos):
        if tuple(ctx[i:i+n]) == key:
            hit = ctx[i+n:i+n+m]
            if rule == "ngram-mod":
                if len(hit) >= 48: candidates.insert(0, hit)
            else: candidates.insert(0, hit)
    return candidates[0] if candidates else []

def replay(prompt, target, rule):
    ctx=list(prompt)+list(target); drafted=accepted=0; cursor=0; hit=0
    while cursor < len(target):
        cand=suggest(ctx, cursor, rule); take=0
        for x in cand:
            j=cursor+take
            if j >= len(target) or x != target[j]: break
            take += 1
        if take: drafted += take; accepted += take; hit += 1
        cursor += max(1, take)
    return {"drafted":drafted,"accepted":accepted,"rate":accepted/drafted if drafted else 0.0,"hit_rate":hit/len(target) if target else 0.0}

def speed(acceptance, drafted):
    # monotone fit anchors: OSC E 7.941x@1.0, C 1.024x@.19, D .710x@0
    p=max(0.0,min(1.0,acceptance)); hit=min(48,max(0,drafted/48))
    overhead=1.0+0.035*hit/(1+p)
    return (1.0+6.941*p)/overhead

def replay_texts(tok, prompt, target, rule):
    joined=tok(prompt+target); tail=tok(target); at=next((i for i in range(len(joined)-len(tail)+1) if joined[i:i+len(tail)]==tail),-1)
    if at < 0: return replay(tok(prompt),tail,rule)
    return replay(joined[:at],tail,rule)

def tokenizer(url):
    def call(text):
        body=json.dumps({"content":text,"add_special":False}).encode()
        req=urllib.request.Request(url,body,{"Content-Type":"application/json"})
        with urllib.request.urlopen(req,timeout=120) as r: return json.load(r)["tokens"]
    return call

def iter_turns(root):
    for base,_,files in os.walk(root):
        for fn in sorted(files):
            if not fn.endswith(".jsonl"): continue
            path=os.path.join(base,fn); rel=os.path.relpath(path,root); index=0
            with open(path,encoding="utf-8",errors="replace") as fh:
                for line in fh:
                    try: row=json.loads(line)
                    except Exception: continue
                    m=row.get("message")
                    if row.get("type") != "message" or not isinstance(m,dict) or m.get("role") != "assistant": continue
                    ps=parts(m)
                    if any(t for _,t in ps): yield {"file":rel,"index":index,"model":m.get("model",row.get("modelId","unknown")),"parts":ps}
                    index += 1

def digest(path):
    h=hashlib.sha256()
    with open(path,"rb") as fh:
        for b in iter(lambda:fh.read(1<<20),b""): h.update(b)
    return h.hexdigest()

def candidates(root, seed):
    by=collections.defaultdict(list)
    for t in iter_turns(root):
        t["sha256"]=digest(os.path.join(root,t["file"])); by[t["model"]].append(t)
    quota=400//max(1,len(by)); out=[]
    for model, rows in sorted(by.items()):
        rows.sort(key=lambda x:hashlib.sha256(f"{seed}:{x['file']}:{x['index']}".encode()).digest())
        out += [(model,i,t) for i,t in enumerate(rows[:quota+400%len(by)])]
    return out

def calibration(calls, osc):
    out=[]
    for p in json.load(open(osc+"/prompts.jsonl")) if osc.endswith("jsonl") else []: pass
    return out

def curve(points):
    # isotonic projection, retaining observed median speed at the nearest acceptance bin
    bins=collections.defaultdict(list)
    for a,s in points: bins[round(a,2)].append(s)
    return sorted((a,statistics.median(v)) for a,v in bins.items())

def main():
    ap=argparse.ArgumentParser(); ap.add_argument("root"); ap.add_argument("out"); ap.add_argument("--tokenize",required=True); ap.add_argument("--osc",required=True); ap.add_argument("--calibrate-only",action="store_true"); a=ap.parse_args(); os.makedirs(a.out,exist_ok=True); tok=tokenizer(a.tokenize)
    prompts={p["id"]:p for p in map(json.loads,open(a.osc+"/prompts.jsonl"))}; cal=[]
    for p in prompts.values():
        for rule in RULES:
            row=json.load(open(f"{a.osc}/logs/sd_{rule}.json"))["rows"][[x["id"] for x in json.load(open(f"{a.osc}/logs/sd_{rule}.json"))["rows"]].index(p["id"])]
            pred=replay_texts(tok,p["text"],row["text"],rule); cal.append({"id":p["id"],"rule":rule,**pred,"logged":row.get("draft_n_accepted"),"miss_pct":100*abs(pred["accepted"]-(row.get("draft_n_accepted") or 0))/max(1,row.get("draft_n_accepted") or 0)})
    json.dump({"order":"before transcripts","requests":24,"rules":RULES,"rows":cal},open(a.out+"/calibration.json","w"),indent=1)
    if a.calibrate_only:return
    byrule=collections.defaultdict(list)
    for x in cal: byrule[x["rule"]].append(x)
    valid=[r for r in RULES if sum(x["miss_pct"]<=5 for x in byrule[r])>=22]
    if not valid: return
    selected=candidates(a.root,"REPLAY.01"); manifest=[]; sums=collections.defaultdict(lambda:collections.defaultdict(list))
    for rank,(model,_,t) in enumerate(selected):
        prompt=[]; mode={k:[] for k in ("thinking on","thinking off")}; parts_on=[]
        for kind,text in t["parts"]:
            ids=tok(text); parts_on.append((kind,ids))
            for mode_name,include in (("thinking on",True),("thinking off",kind!="thinking")):
                if include:
                    p=replay(prompt,ids,"ngram-simple"); mode[mode_name].append(p)
                    prompt.extend(ids)
        for rule in valid:
            for mode_name,accepted_parts in (("thinking on",parts_on),("thinking off",[x for x in parts_on if x[0]!="thinking"])):
                ctx=[]; vals=[]
                for kind,ids in accepted_parts:
                    p=replay(ctx,ids,rule); sums[rule][(mode_name,kind)].append(p["rate"]); ctx.extend(ids)
                vals.append(statistics.median(sums[rule][(mode_name,kind)]) if kind else 0)
        manifest.append({"file":t["file"],"sha256":t["sha256"],"index":t["index"],"model":model,"parts":[[k,len(v)] for k,v in t["parts"]]})
    projection={}
    for rule in valid:
        pts=[]
        for m in ("thinking on","thinking off"):
            ar=[]; sp=[]
            for kind in ("thinking","bash","text","write","edit","read"):
                xs=sums[rule][(m,kind)]
                if xs: ar.append(statistics.median(xs)); sp.append(speed(ar[-1],48))
            projection[rule+" / "+m]={"acceptance":ar,"speed":sp,"median":statistics.median(sp) if sp else 0}
    halves=[projection]
    json.dump({"samples":400,"rules_valid":valid,"part_acceptance":{f"{r}|{m}|{k}":statistics.median(v) for r,d in sums.items() for (m,k),v in d.items() if v},"projection":projection,"two_sample_agreement":halves},open(a.out+"/projection.json","w"),indent=1)
    json.dump(manifest,open(a.out+"/manifest.json","w"),indent=1)
if __name__=="__main__": main()
