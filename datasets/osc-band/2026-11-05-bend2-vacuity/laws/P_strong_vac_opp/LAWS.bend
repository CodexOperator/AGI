import Base
import ./A.bend as A
import ./LIT.bend as D

# P_strong: planted strong gate: score <= 0.05 over ALL histograms
law vac:
  {A.b2u(A.vac_score_le(D.s0(), 64, 1, 20)) == 1 : U32}
