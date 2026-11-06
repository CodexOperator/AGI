import Base
import ./G.bend as G
import ./VALUES.bend as V

# goal:g5.41 line 3: G-CHAMFER (remix) PROVED iff (i) valid fraction >= 0.5 AND coverage among valid >= 0.9 (means over seeds and cues, sigma* on val), AND (ii) the paired per-seed delta G-chamfer - G(sigma* on val) on sc
law g541_l3:
  for r_coverage_ge_0_9: Bool
  for r_gc_minus_g_5of5_mean: Bool
  {G.code(False{}, (U32.is_ge((2 * V.g541_gc_valid() : U32), V.g541_gc_total()) && r_coverage_ge_0_9 && r_gc_minus_g_5of5_mean)) == 0 : U32}
