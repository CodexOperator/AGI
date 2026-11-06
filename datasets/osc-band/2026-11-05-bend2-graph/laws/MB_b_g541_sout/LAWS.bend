import Base
import ./G.bend as G
import ./VALUES.bend as V

# goal:g5.41 line 1: S-OUT (plasma) PROVED iff S's valid fraction >= 0.5 AND the paired per-seed delta S - G(sigma* on val) on score is > 0 on 5/5 seeds with mean > 0.05; RED if either fails.
law b_g541_sout:
  {G.code(False{}, U32.is_ge((2 * V.g541_s_valid() : U32), V.g541_s_total())) == 0 : U32}
