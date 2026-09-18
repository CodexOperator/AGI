#!/usr/bin/env python3
"""Reference for lif.bend: the same sparse ring LIF (N=10000, 100
synapses/neuron, dt=0.1, 1000 steps, 4 seeded nets), written in C.
F32RUN=1 mirrors Bend's f32 arithmetic exactly (init as x*(1/195), dt as
(float)0.1) so the spike counts must agree bit-for-bit; the default build is
the f64 reference the f32 run drifts against. 4 nets run under OpenMP.
Usage: python3 lif_baseline.py [threads] [f32]
"""
import json
import os
import subprocess
import sys
import tempfile
import time

N, SYN, STEPS, DT = 10000, 100, 1000, 0.1
SEEDS = [7, 100010, 200013, 300016]  # batch(2n, 7) in lif.bend

C = r"""
#include <stdio.h>
#include <stdint.h>
#include <stdlib.h>
typedef uint32_t u32;
#ifdef F32RUN
typedef float real;
#define R195 (real)(1.0/195.0)
#define R1024 (real)(1.0/1024.0)
#define R10 (real)(1.0/10.0)
#define ONE (real)1.0
#else
typedef double real;
#define R195 (real)(1.0/195.0)
#define R1024 (real)(1.0/1024.0)
#define R10 (real)(1.0/10.0)
#define ONE (real)1.0
#endif
static inline u32 prng(u32 x){ x^=x<<13; x^=x>>17; x^=x<<5; return x; }
static inline real wgt(u32 i,u32 k,u32 s){
  return (real)(prng(i*97u + k*3266489917u + s) & 127u) * R1024; }
int main(void){
  const int N=10000, K=100, T=1000;
  u32 seeds[4]={7,100010,200013,300016};
  unsigned long long total=0;
  const char* dv=getenv("LIF_DRIVE"); if(!dv) dv="none";
  const char* iv=getenv("LIF_INIT"); if(!iv) iv="orig";
  const char* av=getenv("LIF_AMP"); real amp=av?(real)atof(av):ONE;
  int dm= dv[0]=='p'?1: dv[0]=='g'?2:0;
  int rep= getenv("LIF_REPORT")!=NULL;
  #pragma omp parallel for reduction(+:total) schedule(dynamic)
  for(int q=0;q<4;q++){
    u32 s=seeds[q];
    real v[10000], spk[10000];
    unsigned long cnt[10000], win[10], nactive=0; u32 gol[10000], gol2[10000];
    for(int w=0;w<10;w++) win[w]=0;
    for(int i=0;i<N;i++){ v[i]=(real)(prng((u32)i+s)&255u)*(iv[0]=='s'?(real)(1.0/256.0):R195);
                          spk[i]=0; cnt[i]=0; gol[i]=prng((u32)i*3u+s+991u)&1u; }
    for(int t=0;t<T;t++){
      for(int i=0;i<N;i++){
        real I=0;
        for(int k=0;k<K;k++){ int j=(i-1-k+4*N)%N; I+=wgt((u32)i,(u32)k,s)*spk[j]; }
        real x=0;
        if(dm==1){ u32 u=prng((u32)t*2654435761u+(u32)i*97u+(u32)s)&1048575u; if(u<2097u) x=amp; }
        else if(dm==2){ if(gol[i]) x=amp; }
        real v1=v[i]+R10*((ONE-v[i])+I+x);
        if(v1>=ONE){ v[i]=v1-ONE; spk[i]=ONE; total++; } else { v[i]=v1; spk[i]=0; }
        if(rep && spk[i]==ONE){ if(cnt[i]==0) nactive++; cnt[i]++; win[t/100]++; }
      }
      if(dm==2 && (t+1)%100==0){
        for(int r=0;r<100;r++)for(int c=0;c<100;c++){ int n=0;
          for(int dr=-1;dr<=1;dr++)for(int dc=-1;dc<=1;dc++){ if(dr==0&&dc==0)continue;
            n+=gol[((r+dr+100)%100)*100+((c+dc+100)%100)]; }
          gol2[r*100+c]= gol[r*100+c] ? (n==2||n==3) : (n==3); }
        for(int i=0;i<N;i++) gol[i]=gol2[i];
      }
    }
    if(rep) fprintf(stderr,"NET %lu %lu %lu %lu %lu %lu %lu %lu %lu %lu %lu\n",
                    nactive,win[0],win[1],win[2],win[3],win[4],win[5],win[6],win[7],win[8],win[9]);
  }
  printf("%llu\n", total);
  return 0;
}
"""

def main():
    threads = sys.argv[1] if len(sys.argv) > 1 else "1"
    f32 = len(sys.argv) > 2 and sys.argv[2] == "f32"
    d = tempfile.mkdtemp(prefix="lifbase-")
    src, exe = os.path.join(d, "b.c"), os.path.join(d, "b")
    open(src, "w").write(C)
    cmd = ["cc", "-O3", "-march=native", "-fopenmp"] + (["-DF32RUN"] if f32 else []) + [src, "-o", exe]
    subprocess.run(cmd, check=True)
    env = dict(os.environ, OMP_NUM_THREADS=threads)
    t0 = time.perf_counter()
    out = subprocess.run([exe], capture_output=True, text=True, env=env, check=True)
    if os.environ.get("LIF_REPORT"): sys.stderr.write(out.stderr)
    wall = time.perf_counter() - t0
    spikes = int(out.stdout.strip())
    ns = 4 * N * STEPS
    print(json.dumps({"baseline": "C/f32" if f32 else "C/f64", "threads": int(threads),
                      "spikes": spikes, "wall_s": round(wall, 3),
                      "neuron_steps_per_s": round(ns / wall)}))

if __name__ == "__main__":
    main()