import Base
import ./G.bend as G
import ./VALUES.bend as V

# goal:g5.36 line 1: PROVED iff N_f <= 64 AND the random picks (5 seeds, same solve) need N_r >= 2 x N_f to reach 0.99. RED if N_f > 64, or if the random picks reach 0.99 at N_r < 2 x N_f (the circuit knowledge did not ma
law g536_l1:
  {G.code(False{}, (U32.is_eq(V.g536_nf_reached(), 1) && U32.is_le(V.g536_nf(), 64) && U32.is_ge(V.g536_nr(), (2 * V.g536_nf() : U32)))) == 2 : U32}
