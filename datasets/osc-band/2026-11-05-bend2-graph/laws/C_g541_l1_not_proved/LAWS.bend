import Base
import ./G.bend as G
import ./VALUES.bend as V

# goal:g5.41 line 1: S-OUT (plasma) PROVED iff S's valid fraction >= 0.5 AND the paired per-seed delta S - G(sigma* on val) on score is > 0 on 5/5 seeds with mean > 0.05; RED if either fails.
law g541_l1:
  for r_s_minus_g_5of5_mean: Bool
  {G.code(False{}, (U32.is_ge((2 * V.g541_s_valid() : U32), V.g541_s_total()) && r_s_minus_g_5of5_mean)) == 1 : U32}
