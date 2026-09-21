#!/usr/bin/env python3
"""TEL.02 probe: GGUF arch keys, same-position cache fidelity, shifted-span negative."""
import json, random, struct, sys, time, urllib.request
PORT = sys.argv[1] if len(sys.argv) > 1 else '49525'
OUT = sys.argv[2] if len(sys.argv) > 2 else '.'
MODEL = sys.argv[3] if len(sys.argv) > 3 else '/data/ml/models/Qwen3.5-9B-Q4_K_M.gguf'
N, M = 24, 20
W = ('amber birch cinder delta ember fable gable harbor ivory jade kestrel lantern meadow nimbus '
     'opal quartz raven sable tundra umber violet willow xenon yarrow zephyr basalt cobble dune '
     'flint gorge hollow inlet juniper kelp ledge marsh nectar orbit prism quill ridge signal '
     'thistle upland vale wisp yonder almond brook cedar drift elm fern grove heath iris kale '
     'larch moss oak pine quince reed sedge thorn vetch wren yew zinc').split()
T = {0: '<B', 1: '<b', 2: '<H', 3: '<h', 4: '<I', 5: '<i', 6: '<f', 7: '<?', 10: '<Q', 11: '<q', 12: '<d'}
def gguf(path):
    f = open(path, 'rb'); assert f.read(4) == b'GGUF'
    h = lambda s: struct.unpack(s, f.read(struct.calcsize(s)))[0]
    ver, _, nk = h('<I'), h('<Q'), h('<Q')
    def val(t):
        if t == 8:
            return f.read(h('<Q')).decode('utf-8', 'replace')
        if t == 9:
            et, n = h('<I'), h('<Q'); return [val(et) for _ in range(n)]
        return h(T[t])
    kv = {}
    for _ in range(nk):
        k = f.read(h('<Q')).decode('utf-8', 'replace'); kv[k] = val(h('<I'))
    return {'version': ver, 'kv_count': nk,
            'kv': {k: v for k, v in kv.items() if 'qwen35.' in k or 'architecture' in k}}
def ask(p, cache, np):
    body = {'prompt': p, 'n_predict': np, 'temperature': 0, 'seed': 1,
            'cache_prompt': cache, 'return_tokens': True}
    r = urllib.request.Request('http://127.0.0.1:%s/completion' % PORT,
                               data=json.dumps(body).encode(),
                               headers={'Content-Type': 'application/json'})
    return json.load(urllib.request.urlopen(r, timeout=600))
def tm(o):
    t = o['timings']
    return {'prompt_n': t['prompt_n'], 'cache_n': t['cache_n'], 'prompt_ms': t['prompt_ms']}
wr = lambda n, o: open('%s/%s' % (OUT, n), 'w').write(json.dumps(o, indent=1))
rng = random.Random(20260921); mk = lambda n: ' '.join(rng.choice(W) for _ in range(n)) + ' Sum:'
wr('gguf-qwen35-keys.json', gguf(MODEL))
t0, rows, agree, hits = time.time(), [], 0, 0
for i in range(N):
    p = mk(rng.randint(20, 34)); fr = ask(p, False, M); ask(p, True, 1); re_ = ask(p, True, M)
    tf, tr = fr.get('tokens') or [], re_.get('tokens') or []
    hit = sum(1 for a, b in zip(tf[:M], tr[:M]) if a == b)
    agree += int(len(tf) >= M and len(tr) >= M and tf[:M] == tr[:M]); hits += hit
    ft, rt = tm(fr), tm(re_)
    rows.append({'i': i, 'fresh': ft, 'reuse': rt, 'token_hits_20': hit,
                 'compute_frac': round(rt['prompt_ms'] / ft['prompt_ms'], 4)})
wr('fidelity-samepos.json', {'port': PORT, 'N': N, 'M': M, 'wall_s': round(time.time() - t0, 1),
   'exact_agreement': agree, 'exact_agreement_pct': round(100.0 * agree / N, 2),
   'token_hits_pct': round(100.0 * hits / (N * M), 2),
   'mean_compute_frac': round(sum(r['compute_frac'] for r in rows) / N, 4), 'rows': rows})

A = 'A ' + ' '.join(rng.choice(W) for _ in range(40)) + ' a0:'
X = 'X ' + ' '.join(rng.choice(W) for _ in range(40)) + ' x0:'
S = 'S ' + ' '.join(rng.choice(W) for _ in range(170)) + ' s0:'
B = ' B ' + ' '.join(rng.choice(W) for _ in range(20)) + ' b0.'
r1, r2 = ask(A + S + B, False, 1), ask(A + S + B, True, 1)
r3, r4 = ask(X + S + B, True, 1), ask(X + S + B, False, 1)
d = {'S_words': len(S.split()), 'r1_fresh_ASB': tm(r1), 'r2_samepos_ASB': tm(r2),
     'r3_shifted_XSB': tm(r3), 'r4_fresh_XSB': tm(r4)}
d['r3_compute_frac_of_fresh'] = round(tm(r3)['prompt_ms'] / tm(r4)['prompt_ms'], 4)
wr('shift-negative.json', d)
print(json.dumps(d))
