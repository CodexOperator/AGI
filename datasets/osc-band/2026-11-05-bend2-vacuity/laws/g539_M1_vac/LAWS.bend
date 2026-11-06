import Base
import ./A.bend as A
import ./LIT.bend as D

# g539_M1: M1 P with ONE noise draw frozen per seed and cue scores <= 0.05 on every seed
law vac:
  {A.b2u(A.vac_score_le(D.s0(), 64, 1, 20)) == 1 : U32}
