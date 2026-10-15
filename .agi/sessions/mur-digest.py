#!/usr/bin/env python3
"""Digest a merge-up-review workflow journal: one line per round, never the file whole."""
import json, sys
path = sys.argv[1]
rows = [json.loads(l) for l in open(path)]
label = {}
for r in rows:
    if r.get('type') == 'started':
        label[r['agentId']] = r.get('label', '')
res = {}
for r in rows:
    if r.get('type') == 'result':
        res[label.get(r['agentId'], r['agentId'])] = r.get('result')
keys = sorted({l.split(":",1)[1] for l in label.values() if ":" in l})
def short(s, n=140):
    s = ' '.join(str(s).split())
    return s if len(s) <= n else s[:n] + '…'
for k in keys:
    rv = res.get('review:' + k); vf = res.get('verify:' + k)
    print(f"== {k}")
    if isinstance(rv, dict):
        print(f"  review: rec={rv.get('verdict_recommendation')} tests={short(rv.get('tests_run'),90)}")
        for d in rv.get('defects') or []:
            if isinstance(d, dict):
                print(f"    defect[{d.get('severity')}]: {short(d.get('title') or d.get('summary') or d, 150)}")
            else:
                print(f"    defect: {short(d,150)}")
        if rv.get('prime_step'): print(f"  prime_step: {short(rv.get('prime_step'),200)}")
    else:
        print(f"  review: {'PENDING' if rv is None else short(rv)}")
    if isinstance(vf, dict):
        print(f"  verify: final={vf.get('final_recommendation')} refuted={[short(v.get('defect') or v.get('title') or v,60) for v in (vf.get('verdicts') or []) if isinstance(v,dict) and v.get('refuted')]}")
        if vf.get('missed'): print(f"    missed: {[short(m,120) for m in vf.get('missed')]}")
        if vf.get('note') or vf.get('summary'): print(f"    note: {short(vf.get('note') or vf.get('summary'),200)}")
    else:
        print(f"  verify: {'PENDING' if vf is None else short(vf)}")
