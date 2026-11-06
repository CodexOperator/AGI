import Base
import ./A.bend as A
import ./LIT.bend as D

# g539_M2: M2 the scorer: 64 true target lines per cue (32 per class) score >= 0.9, and 64 Bernoulli(0.5) images have valid fraction <= 0.05
law vac:
  {A.b2u(A.vac_score_ge(D.s0(), 64, 9, 10) && A.vac_valid_le(D.s1(), 64, 1, 20)) == 1 : U32}
