import Base
import ./G.bend as G
import ./VALUES.bend as V

# goal:g5.38 line 1: H1 (remix) PROVED iff (b) reaches 0.99 held-out at N_b <= 32 AND N_r >= 2 x N_b; else RED.
law g538_l1:
  {G.code(False{}, (U32.is_eq(V.g538_nb_reached(), 1) && U32.is_le(V.g538_nb(), 32) && U32.is_ge(V.g538_nr(), (2 * V.g538_nb() : U32)))) == 1 : U32}
