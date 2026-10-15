#!/usr/bin/env python3
"""Rhythm-bank metronome toy -- C2.02 a00-762dba58 (hypothesis:c2-kuramoto-metronome-rhythm-bank).

K=8 steering tones, frequencies f_k = 0.008 + 0.002*k cycles/step (k=0..7), distinct.
Each oscillator i draws S_i ~ U{10..200} read-sites (synthesis rank 1 wording), each
read-site picks one of the 8 tones uniformly WITH replacement and carries a weight
w ~ U[0.3,1] union [-1,-0.3] (redraw if |w|<0.3); read-sites on the same tone accumulate.
  psi_i(t) = arg sum_k W_ik * exp(i*theta_k(t))     (weighted circular mean)
  phi_i(t+1) = phi_i(t) + KC*sin(psi_i(t)-phi_i(t)) + omega_i   (Kuramoto push + natural drift)
  E(t) = mean_i (1 - cos(phi_i(t) - psi_i(t)))      (alignment-cost energy, 0=locked, 2=anti)
ONE driver-bit flip at step FLIP. --flip-mode sign (default, the C2.2 arm): steering tone k=4
has its frequency SIGN inverted (f4 -> -f4). --flip-mode phase: tone 4 advances by pi once at the
flip step, its frequency and all subscription weights untouched.
Energy readout: --energy signed (default, C2.2) E = mean_i (1 - cos(phi_i - psi_i));
--energy modpi E = mean_i (1 - cos(2*(phi_i - psi_i))), so a lock offset by up to pi scores 0.
Both traces are always recorded; --energy only selects which one drives the top-level metrics.
"""
import argparse, json, math, os, time
import numpy as np

K=8; F0=0.008; DF=0.002; TAU=2*math.pi
FLIP=2000; LOCKW=500; KC=0.5; DRIFT=0.002  # BAND lives in the relock_step_* fields below

def run(N, T, seed, flip_mode="sign", energy_mode="signed"):
    rng=np.random.default_rng(seed)
    S=rng.integers(10,201,N); W=np.zeros((N,K)); distinct=np.zeros(N,dtype=int)
    for i in range(N):
        idx=rng.integers(0,K,S[i]); mag=rng.uniform(0.3,1.0,S[i]); sgn=rng.choice([-1.0,1.0],S[i])
        np.add.at(W[i],idx,mag*sgn); distinct[i]=len(np.unique(idx))
    phi=rng.uniform(0,TAU,N); omega=rng.normal(0,DRIFT,N)
    f=np.array([F0+DF*k for k in range(K)]); Es=np.empty(T); Em=np.empty(T); off=np.empty(T); inc=np.zeros(N)
    th=rng.uniform(0,TAU,K)                    # tone phases, integrated so a sign flip is a velocity reversal
    for t in range(T):
        if t==FLIP:
            if flip_mode=="phase": th[4]=(th[4]+math.pi)%TAU
            else: f[4]=-f[4]
        th=(th+TAU*f)%TAU; psi=np.angle(W@np.exp(1j*th))
        kick=KC*np.sin(psi-phi); d=phi-psi
        Es[t]=np.mean(1-np.cos(d)); Em[t]=np.mean(1-np.cos(2*d)); off[t]=np.angle(np.mean(np.exp(1j*d)))
        if FLIP-LOCKW<=t<FLIP: inc+=kick+omega
        phi=(phi+kick+omega)%TAU
    E=Es if energy_mode=="signed" else Em
    rates=inc/(TAU*LOCKW)                      # cycles/step, time-averaged over last LOCKW pre-flip steps
    def stats(tr):                             # same metric set for either scoring, so cells compare on one run
        pre=tr[FLIP-LOCKW:FLIP].mean(); post=tr[FLIP:]
        sm=np.convolve(tr, np.ones(20)/20, mode='same')
        def relock(band):                      # first step after flip where smoothed tr <= pre*(1+band) for 100 steps
            for j in range(FLIP, T-100):
                if all(sm[k]<=pre*(1+band) for k in range(j,j+100)): return int(j-FLIP)
            return None
        r10=relock(0.10)
        return dict(energy_preflip_mean=round(float(pre),5), energy_max_flipwindow=round(float(post[:200].max()),5),
            energy_max_overall=round(float(tr.max()),5), post_flip_floor=round(float(post[1000:].mean()),5),
            post_over_pre_ratio=round(float(post[1000:].mean()/pre),2), relock_step_10pct=r10,
            relock_step_25pct=relock(0.25), relock_step_50pct=relock(0.50), relock_step_100pct=relock(1.00),
            relocked_10pct_within_1000=bool(r10 is not None and r10<=1000))
    cnt,edges=np.histogram(rates, bins=np.arange(rates.min()-5e-4, rates.max()+1.5e-3, 5e-4))
    peaks=[float(x) for x in np.unique(np.round(rates,3))]
    d0=dict(N=int(N),seed=int(seed),T=int(T),flip_step=FLIP,flip_mode=flip_mode,energy_mode=energy_mode,
        flip="tone k=4 phase advanced by pi" if flip_mode=="phase" else "tone k=4 frequency sign inverted",
        freqs=[round(float(x),4) for x in [F0+DF*k for k in range(K)]],
        sub_slots=[int(S.min()),int(S.max())], sub_distinct_mean=round(float(distinct.mean()),2),
        offset_pre=round(float(off[FLIP-LOCKW:FLIP].mean()),4), offset_post=round(float(off[FLIP+1000:].mean()),4),
        offset_post_abs=round(float(np.abs(np.sin(off[FLIP+1000:])).mean()),4), energy=[round(float(x),5) for x in E],
        energy_signed=[round(float(x),5) for x in Es], energy_modpi=[round(float(x),5) for x in Em],
        rate_hist_counts=[int(x) for x in cnt], rate_hist_edges=[round(float(x),4) for x in edges],
        band_count=len(peaks), band_locations=peaks, rates=[round(float(x),5) for x in rates],
        relock_band_basis="first post-flip step where 20-step-smoothed E <= pre*(1+band) sustained 100 steps",
        metrics_signed=stats(Es), metrics_modpi=stats(Em))
    d0.update(stats(E))                        # top-level metric names keep the C2.2 contract
    return d0

def box():
    return dict(env={k:os.environ.get(k) for k in ["OMP_NUM_THREADS","MKL_NUM_THREADS","OPENBLAS_NUM_THREADS"]},
        nice=os.nice(0), loadavg=[round(float(x),2) for x in os.getloadavg()],
        cpus=os.cpu_count(), threadpool=os.environ.get("OMP_NUM_THREADS"),
        wall_s=round(time.time()-T0,2))

if __name__=="__main__":
    T0=time.time(); ap=argparse.ArgumentParser(); ap.add_argument("--out",default="metronome_results.json")
    ap.add_argument("--steps",type=int,default=4000); ap.add_argument("--ns",type=int,nargs="+",default=[200,1000])
    ap.add_argument("--flip-mode",dest="flip_mode",choices=["sign","phase"],default="sign")
    ap.add_argument("--energy",choices=["signed","modpi"],default="signed")
    ap.add_argument("--seeds",type=int,nargs="+",default=[0,1,2,3,4])
    ap.add_argument("--grid",action="store_true")
    a=ap.parse_args()
    if a.grid: runs=[run(n,a.steps,s,fm,em) for fm in ["sign","phase"] for em in ["signed","modpi"] for n in a.ns for s in a.seeds]
    else: runs=[run(n,a.steps,i,a.flip_mode,a.energy) for i,n in enumerate(a.ns)]
    res={"spec":__doc__.split("\n")[0],"grid":bool(a.grid),"runs":runs}
    res["box"]=box(); json.dump(res,open(a.out,"w"),separators=(",",":"))
    print("wrote",a.out,"runs",a.ns,"steps",a.steps); print("box",res["box"])
    for r in res["runs"]: print(r["N"],"bands",r["band_count"],"at",r["band_locations"],"relock10",r["relock_step_10pct"],"floor_ratio",r["post_over_pre_ratio"],"Epre",r["energy_preflip_mean"])
