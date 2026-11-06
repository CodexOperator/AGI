import Base
import ./A.bend as A
import ./LIT.bend as D

# g546_M2: M2 the scorer arm as in g5.39
law vac:
  {A.b2u(A.vac_score_ge(D.s0(), 64, 9, 10) && A.vac_valid_le(D.s1(), 64, 1, 20)) == 1 : U32}
