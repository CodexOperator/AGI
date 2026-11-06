import Base
import ./G.bend as G
import ./VALUES.bend as V

# goal:g5.41 line 2: S-MECH (plasma) PROVED iff step 0's BLEND share >= 50% of g5.39's invalid samples AND, in step 1, S's BLEND share of its own invalid samples is below G's on 5/5 seeds; RED if either fails. A seed wher
law g541_l2:
  for r_step1_s_below_g_5of5: Bool
  {G.code(False{}, (U32.is_ge((2 * V.g541_blend0() : U32), V.g541_invalid0()) && r_step1_s_below_g_5of5)) == 0 : U32}
