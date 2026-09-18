import Base
# Sparse LIF spiking network, f32 (Bend 2 has no f64). N = 10000 neurons,
# 100 synapses each on a ring (neuron i receives i-1..i-100), dt = 0.1 ms,
# 1000 steps, seeded hash. A step is a left-to-right sweep carrying the last
# 100 spikes as a window; 4 independent seeded nets fork for thread scaling.
# Build: bend lif.bend -o lif ; run: ./lif --threads {1,4}

def fl(n: U32, d: U32) -> F32:
  F32.div(U32.to_f32(n), U32.to_f32(d))

def prng(+x: U32) -> U32:
  +b = U32.xor(x, U32.shln(x, 13n))
  +d = U32.xor(b, U32.shrn(b, 17n))
  U32.xor(d, U32.shln(d, 5n))

def b2u(b: Bool) -> U32:
  match b:
    case False{}: 0
    case True{}: 1

def spk.go(b: Bool) -> F32:
  match b:
    case True{}: fl(1, 1)
    case False{}: fl(0, 1)

def spk(v: F32) -> F32:
  spk.go(F32.is_ge(v, fl(1, 1)))

def reset.go(v: F32, b: Bool) -> F32:
  match b:
    case True{}: F32.sub(v, fl(1, 1))
    case False{}: v

def reset(+v: F32) -> F32:
  reset.go(v, F32.is_ge(v, fl(1, 1)))

def wgt(i: U32, k: U32, s: U32) -> F32:
  F32.mul(U32.to_f32(U32.and(prng(U32.add(U32.add(U32.mul(i, 97), U32.mul(k, 3266489917)), s)), 127)), fl(1, 1024))

def dot(win: List<&2, F32>, +i: U32, +s: U32, +k: U32, fuel: Nat, acc: F32) -> F32:
  match win:
    case Nil{}: acc
    case h <> t:
      match fuel:
        case 0n: acc
        case 1n+p: dot(t, i, s, U32.add(k, 1), p, F32.add(acc, F32.mul(wgt(i, k, s), h)))

def win100(xs: List<&2, F32>) -> List<&2, F32>:
  List.take(&2, F32, xs, 100n)

def sim(t: Nat, +seed: U32, +i: U32, vs: List<&2, F32>, +win: List<&2, F32>, nv: List<&2, F32>, sp: U32, total: U32) -> List<&2, F32> & U32:
  match t:
    case 0n:
      (List.reverse(&2, F32, nv), U32.add(total, sp))
    case 1n+p:
      match vs:
        case Nil{}:
          sim(p, seed, 0, List.reverse(&2, F32, nv), win100(win), Nil{}, 0, U32.add(total, sp))
        case +h <> t2:
          +I = dot(win, i, seed, 0, 100n, fl(0, 1))
          +v1 = F32.add(h, F32.mul(fl(1, 10), F32.add(F32.sub(fl(1, 1), h), I)))
          +b = b2u(F32.is_ge(v1, fl(1, 1)))
          sim(p, seed, U32.add(i, 1), t2, spk(v1) <> win, reset(v1) <> nv, U32.add(sp, b), total)

def mk(k: Nat, +i: U32, +seed: U32, acc: List<&2, F32>) -> List<&2, F32>:
  match k:
    case 0n: List.reverse(&2, F32, acc)
    case 1n+p:
      mk(p, U32.add(i, 1), seed, F32.mul(U32.to_f32(U32.and(prng(U32.add(i, seed)), 255)), fl(1, 195)) <> acc)

def net.fin(r: List<&2, F32> & U32) -> U32:
  (vs, sp) = r
  sp

def net(+seed: U32) -> U32:
  net.fin(sim(U32.to_nat(10000999), seed, 0, mk(U32.to_nat(10000), 0, seed, Nil{}), Nil{}, Nil{}, 0, 0))

def batch(+d: Nat, +s: U32) -> U32:
  match d:
    case 0n: net(s)
    case 1n+p:
      a b = batch(p, s) batch(p, U32.add(s, U32.shln(100003, p)))
      U32.add(a, b)

def main() -> IO(Unit):
  IO.print(U32.show(batch(2n, 7)))
