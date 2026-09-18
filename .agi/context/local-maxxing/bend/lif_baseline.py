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
  #pragma omp parallel for reduction(+:total) schedule(dynamic)
  for(int q=0;q<4;q++){
    u32 s=seeds[q];
    real v[10000], spk[10000];
    for(int i=0;i<N;i++){ v[i]=(real)(prng((u32)i+s)&255u)*R195; spk[i]=0; }
    for(int t=0;t<T;t++){
      for(int i=0;i<N;i++){
        real I=0;
        for(int k=0;k<K;k++){ int j=(i-1-k+4*N)%N; I+=wgt((u32)i,(u32)k,s)*spk[j]; }
        real v1=v[i]+R10*((ONE-v[i])+I);
        if(v1>=ONE){ v[i]=v1-ONE; spk[i]=ONE; total++; } else { v[i]=v1; spk[i]=0; }
      }
    }
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
    wall = time.perf_counter() - t0
    spikes = int(out.stdout.strip())
    ns = 4 * N * STEPS
    print(json.dumps({"baseline": "C/f32" if f32 else "C/f64", "threads": int(threads),
                      "spikes": spikes, "wall_s": round(wall, 3),
                      "neuron_steps_per_s": round(ns / wall)}))

if __name__ == "__main__":
    main()