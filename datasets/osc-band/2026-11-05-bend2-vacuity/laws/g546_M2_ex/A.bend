import Base

# goal:g5.50: a mutant gate's construction-implied output space O_g, as a literal, and the gate's reading over it.
# A per-cue outcome O{a, b} = the valid counts of the cue's TWO classes (a valid sample's class lies in the cue's pair);
# v = a + b of n samples. score = (v / n) x coverage, coverage = the valid histogram's entropy in bits, bounded EXACTLY
# in integers: coverage = 0 iff a = 0 or b = 0; coverage <= 1 (two classes); coverage >= 1 - p_a^2 - p_b^2 = 2ab / v^2
# (Shannon entropy >= the Renyi-2 entropy -log(sum p^2) >= 1 - sum p^2, in nats, and bits >= nats). So
#   hi(o) = 0 if one class else v / n     lo(o) = 2ab / (n v)     (lo = hi = 0 on every one-class o; lo = v / (2n) at a = b)
# A gate reads per seed the MEAN over the 2 cues; on every seed. A for-all over O_g x O_g reduces EXACTLY to an
# extreme over O_g (the mean of two values lies between their min and max, and the pair (o, o) attains it).

type O is Data:
  O{a: U32, b: U32}

def sel(c: Bool, x: U32, y: U32) -> U32:
  match c:
    case True{}:
      x
    case False{}:
      y

def b2u(x: Bool) -> U32:
  match x:
    case True{}:
      1
    case False{}:
      0

def maxu(+x: U32, +y: U32) -> U32:
  sel(U32.is_gt(x, y), x, y)

def minu(+x: U32, +y: U32) -> U32:
  sel(U32.is_lt(x, y), x, y)

def vv(o: O) -> U32:
  match o:
    case O{a, b}:
      (a + b : U32)

def hi_num(o: O) -> U32:
  match o:
    case O{+a, +b}:
      sel(U32.is_eq(a, 0) || U32.is_eq(b, 0), 0, (a + b : U32))

# lo(o) > p/q  <=>  q 2ab > p n v  (v = 0: lo = 0, never > p/q >= 0)
def lo_gt(o: O, +n: U32, +p: U32, +q: U32) -> Bool:
  match o:
    case O{+a, +b}:
      U32.is_gt((q * ((2 * a : U32) * b : U32) : U32), ((p * n : U32) * (a + b : U32) : U32))

# lo(o) >= p/q  <=>  v > 0 and q 2ab >= p n v
def lo_ge(o: O, +n: U32, +p: U32, +q: U32) -> Bool:
  match o:
    case O{+a, +b}:
      U32.is_gt((a + b : U32), 0) && U32.is_ge((q * ((2 * a : U32) * b : U32) : U32), ((p * n : U32) * (a + b : U32) : U32))

def max_hi(os: +List<O>, +acc: U32) -> U32:
  match os:
    case Nil{}:
      acc
    case Con{+o, t}:
      max_hi(t, maxu(acc, hi_num(o)))

def min_hi(os: +List<O>, +acc: U32) -> U32:
  match os:
    case Nil{}:
      acc
    case Con{+o, t}:
      min_hi(t, minu(acc, hi_num(o)))

def max_v(os: +List<O>, +acc: U32) -> U32:
  match os:
    case Nil{}:
      acc
    case Con{+o, t}:
      max_v(t, maxu(acc, vv(o)))

def min_v(os: +List<O>, +acc: U32) -> U32:
  match os:
    case Nil{}:
      acc
    case Con{+o, t}:
      min_v(t, minu(acc, vv(o)))

def all_lo_ge(os: +List<O>, +n: U32, +p: U32, +q: U32) -> Bool:
  match os:
    case Nil{}:
      True{}
    case Con{+o, t}:
      lo_ge(o, n, p, q) && all_lo_ge(t, n, p, q)

def any_lo_gt(os: +List<O>, +n: U32, +p: U32, +q: U32) -> Bool:
  match os:
    case Nil{}:
      False{}
    case Con{+o, t}:
      lo_gt(o, n, p, q) || any_lo_gt(t, n, p, q)

def max_d(ds: +List<U32>, +acc: U32) -> U32:
  match ds:
    case Nil{}:
      acc
    case Con{+d, t}:
      max_d(t, maxu(acc, d))

def min_d(ds: +List<U32>, +acc: U32) -> U32:
  match ds:
    case Nil{}:
      acc
    case Con{+d, t}:
      min_d(t, minu(acc, d))

def o_eq(x: O, y: O) -> Bool:
  match x y:
    case O{a, b} O{c, d}:
      U32.is_eq(a, c) && U32.is_eq(b, d)

def o_in(os: +List<O>, +x: O) -> Bool:
  match os:
    case Nil{}:
      False{}
    case Con{o, t}:
      o_eq(o, x) || o_in(t, x)

def d_in(ds: +List<U32>, +x: U32) -> Bool:
  match ds:
    case Nil{}:
      False{}
    case Con{d, t}:
      U32.is_eq(d, x) || d_in(t, x)

# ---- the conjunct readings (p/q a threshold; n the per-cue sample count) ----
# VAC: the conjunct holds for EVERY per-seed outcome in O_g x O_g.   EX: SOME outcome definitely breaks it.
# WIT: the named outcome (o0, o1) (or d) lies in O_g and definitely breaks it.

# score <= p/q (mean over cues)
def vac_score_le(+os: +List<O>, +n: U32, +p: U32, +q: U32) -> Bool:
  U32.is_le((q * max_hi(os, 0) : U32), (p * n : U32))

def ex_score_le(+os: +List<O>, +n: U32, +p: U32, +q: U32) -> Bool:
  any_lo_gt(os, n, p, q)

# mean lo > p/q  <=>  q (2 a0 b0 v1 + 2 a1 b1 v0) > 2 p n v0 v1   (both v > 0)
def mean_lo_gt(x: O, y: O, +n: U32, +p: U32, +q: U32) -> Bool:
  match x y:
    case O{+a0, +b0} O{+a1, +b1}:
      +v0 = (a0 + b0 : U32)
      +v1 = (a1 + b1 : U32)
      U32.is_gt(v0, 0) && U32.is_gt(v1, 0) && U32.is_gt((q * ((((2 * a0 : U32) * b0 : U32) * v1 : U32) + (((2 * a1 : U32) * b1 : U32) * v0 : U32) : U32) : U32), (((2 * p : U32) * n : U32) * (v0 * v1 : U32) : U32))

def wit_score_le(+os: +List<O>, +x: O, +y: O, +n: U32, +p: U32, +q: U32) -> Bool:
  o_in(os, x) && o_in(os, y) && mean_lo_gt(x, y, n, p, q)

# score >= p/q (mean over cues)
def vac_score_ge(+os: +List<O>, +n: U32, +p: U32, +q: U32) -> Bool:
  all_lo_ge(os, n, p, q)

def ex_score_ge(+os: +List<O>, +n: U32, +p: U32, +q: U32) -> Bool:
  U32.is_lt((q * min_hi(os, n) : U32), (p * n : U32))

def wit_score_ge(+os: +List<O>, +x: O, +y: O, +n: U32, +p: U32, +q: U32) -> Bool:
  o_in(os, x) && o_in(os, y) && U32.is_lt((q * (hi_num(x) + hi_num(y) : U32) : U32), ((2 * p : U32) * n : U32))

# valid fraction <= p/q (mean over cues)
def vac_valid_le(+os: +List<O>, +n: U32, +p: U32, +q: U32) -> Bool:
  U32.is_le((q * max_v(os, 0) : U32), (p * n : U32))

def ex_valid_le(+os: +List<O>, +n: U32, +p: U32, +q: U32) -> Bool:
  U32.is_gt((q * max_v(os, 0) : U32), (p * n : U32))

def wit_valid_le(+os: +List<O>, +x: O, +y: O, +n: U32, +p: U32, +q: U32) -> Bool:
  o_in(os, x) && o_in(os, y) && U32.is_gt((q * (vv(x) + vv(y) : U32) : U32), ((2 * p : U32) * n : U32))

# valid fraction >= p/q (mean over cues): the planted tautology at p = 0
def vac_valid_ge(+os: +List<O>, +n: U32, +p: U32, +q: U32) -> Bool:
  U32.is_ge((q * min_v(os, n) : U32), (p * n : U32))

def ex_valid_ge(+os: +List<O>, +n: U32, +p: U32, +q: U32) -> Bool:
  U32.is_lt((q * min_v(os, n) : U32), (p * n : U32))

def wit_valid_ge(+os: +List<O>, +x: O, +y: O, +n: U32, +p: U32, +q: U32) -> Bool:
  o_in(os, x) && o_in(os, y) && U32.is_lt((q * (vv(x) + vv(y) : U32) : U32), ((2 * p : U32) * n : U32))

# distinct valid images <= k in EVERY cue
def vac_dist_le(+ds: +List<U32>, +k: U32) -> Bool:
  U32.is_le(max_d(ds, 0), k)

def ex_dist_le(+ds: +List<U32>, +k: U32) -> Bool:
  U32.is_gt(max_d(ds, 0), k)

def wit_dist_le(+ds: +List<U32>, +x: U32, +k: U32) -> Bool:
  d_in(ds, x) && U32.is_gt(x, k)

# distinct valid images >= k, MIN over cues
def vac_dist_ge(+ds: +List<U32>, +k: U32) -> Bool:
  U32.is_ge(min_d(ds, 4294967295), k)

def ex_dist_ge(+ds: +List<U32>, +k: U32) -> Bool:
  U32.is_lt(min_d(ds, 4294967295), k)

def wit_dist_ge(+ds: +List<U32>, +x: U32, +k: U32) -> Bool:
  d_in(ds, x) && U32.is_lt(x, k)
