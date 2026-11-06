import Base
import ./G.bend as G
import ./VALUES.bend as V

# goal:g5.38 line 2: H2 (remix): RED iff (c) reaches 0.99 at a grid step below N_b: circuit knowledge picks worse than plain numerics, a disproof in its own right. If (b) never reaches 0.99 at N <= 32, N_b := '>32' and H2
law g538_l2:
  {G.code((U32.is_eq(V.g538_nb_reached(), 0) && U32.is_eq(V.g538_nc_reached(), 0)), Bool.not((U32.is_eq(V.g538_nc_reached(), 1) && (U32.is_eq(V.g538_nb_reached(), 0) || U32.is_lt(V.g538_nc(), V.g538_nb()))))) == 1 : U32}
