import numpy as np, torch, snntorch as snn, json
np.set_printoptions(linewidth=250)
LEV = {}
def lev(a, b):
    n, m = len(a), len(b)
    prev = list(range(m+1))
    for i in range(1, n+1):
        cur = [i] + [0]*m
        ai = a[i-1]
        for j in range(1, m+1):
            cost = 0 if ai == b[j-1] else 1
            cur[j] = min(prev[j]+1, cur[j-1]+1, prev[j-1]+cost)
        prev = cur
    return prev[m]

def run_chain(beta, thr, w_syn, num_steps, inp, seed=42):
    torch.manual_seed(seed)
    lif1 = snn.Leaky(beta=beta, threshold=thr, reset_mechanism='subtract')
    lif2 = snn.Leaky(beta=beta, threshold=thr, reset_mechanism='subtract')
    m1 = lif1.init_leaky(); m2 = lif2.init_leaky()
    s1 = np.zeros(num_steps, dtype=np.int8); s2 = np.zeros(num_steps, dtype=np.int8)
    for t in range(num_steps):
        sp1, m1 = lif1(inp[t], m1)
        sp2, m2 = lif2(w_syn*sp1, m2)
        s1[t] = int(sp1.item()); s2[t] = int(sp2.item())
    return s1, s2

def windows(bits, W=8, encoding='level'):
    if encoding == 'flip':
        x = np.zeros(len(bits), dtype=np.int8)
        x[0] = bits[0]
        x[1:] = bits[1:] ^ bits[:-1]
    else:
        x = bits.astype(np.int8)
    n = len(x)
    w = np.zeros(n, dtype=np.int32)
    for t in range(n):
        v = 0
        for i in range(W):
            idx = t - (W-1) + i
            if idx >= 0 and x[idx]:
                v |= (1 << i)
        w[t] = v
    return w

def dist(pred, true):
    return lev(pred.tolist(), true.tolist())

def sweep(w, true, rng, nrand=1000):
    N = len(true)
    res = {'threshold': [], 'random': [], 'oracle_hamming': None}
    # threshold LUTs: k in 0..256  (pred=1 iff word>=k)
    for k in range(257):
        pred = (w >= k).astype(np.int8)
        res['threshold'].append((dist(pred, true), k))
    # random arbitrary LUTs
    rnds = []
    for _ in range(nrand):
        lut = rng.integers(0, 2, size=256).astype(np.int8)
        pred = lut[w]
        rnds.append(dist(pred, true))
    res['random'] = rnds
    # oracle per-position Hamming LUT
    cnt = {}
    for t in range(N):
        word = int(w[t]); cnt.setdefault(word, [0,0]); cnt[word][true[t]] += 1
    lut = np.zeros(256, dtype=np.int8)
    for word,(z,o) in cnt.items():
        lut[word] = 1 if o > z else 0
    pred = lut[w]
    res['oracle_hamming'] = (dist(pred, true), int((pred!=true).sum()))
    return res

num_steps=200; thr=1.0; w_syn=0.8
# inputs, exactly as snn_setup.py
dc = torch.ones(num_steps)*0.3
torch.manual_seed(42)
spk_in = (torch.rand(num_steps) < 0.3).float()
np.save('/tmp/kidB/spk_in.npy', spk_in.numpy())

out = {'commit': 'd87863c52bfa9fd3e417449aba66adeca90654a6',
       'num_steps': num_steps, 'thr': thr, 'w_syn': w_syn,
       'input_spike_train_seed42': spk_in.numpy().astype(int).tolist()}
true_trains = {}
for beta in [0.5,0.8,0.95]:
    s1d,s2d = run_chain(beta,thr,w_syn,num_steps,dc)
    s1s,s2s = run_chain(beta,thr,w_syn,num_steps,spk_in)
    true_trains[(beta,'dc')]=(s1d,s2d); true_trains[(beta,'spk')]=(s1s,s2s)
    out[f'N1_dc_b{beta}']=s1d.tolist(); out[f'N2_dc_b{beta}']=s2d.tolist()
    out[f'N1_spk_b{beta}']=s1s.tolist(); out[f'N2_spk_b{beta}']=s2s.tolist()

rng = np.random.default_rng(12345)
table=[]
for beta in [0.5,0.8,0.95]:
    for mode in ['dc','spk']:
        s1,s2 = true_trains[(beta,mode)]
        for enc in ['level','flip']:
            w = windows(s1, 8, enc)
            r = sweep(w, s2, rng)
            bt = min(r['threshold'])
            rnd = np.array(r['random'])
            oh = r['oracle_hamming']
            row = dict(beta=beta,mode=mode,encoding=enc,
                       thr_best_dist=int(bt[0]), thr_best_pct=100*bt[0]/num_steps, thr_best_k=int(bt[1]),
                       rand_min=int(rnd.min()), rand_mean=float(rnd.mean()), rand_max=int(rnd.max()),
                       rand_mean_pct=100*float(rnd.mean())/num_steps,
                       oracle_ham_dist=int(oh[0]), oracle_ham_pct=100*oh[0]/num_steps,
                       oracle_ham_mismatch=int(oh[1]),
                       distinct_windows=int(len(np.unique(w))))
            table.append(row)
out['table']=table
out['beta8']={str(b):b**8 for b in [0.5,0.8,0.95]}
print(json.dumps(out['beta8']))
for row in table:
    print(row)
json.dump(out, open('/tmp/kidB/e3_results.json','w'))
