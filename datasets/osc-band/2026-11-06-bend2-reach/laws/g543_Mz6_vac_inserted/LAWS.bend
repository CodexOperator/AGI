import Base
import ./A.bend as A
import ./LIT.bend as D

law vac:
  {A.b2u(A.vac_dist_le(D.s0(), 15)) == 1 : U32}
