import Base
import ./G.bend as G
import ./VALUES.bend as V

# goal:g5.38 line 3: H3 (less-is-more) PROVED iff some N_w <= 32 reaches >= 0.99 held-out AND (c) at that same N stays < 0.99; RED otherwise.
law g538_l3:
  {G.code(False{}, U32.is_ge(V.g538_nw_hits(), 1)) == 1 : U32}
