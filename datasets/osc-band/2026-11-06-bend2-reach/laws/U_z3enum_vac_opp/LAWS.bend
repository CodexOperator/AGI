import Base
import ./A.bend as A
import ./LIT.bend as D

law vac_opp:
  {A.b2u(A.vac_score_le(D.s(), 64, 1, 20)) == 1 : U32}
