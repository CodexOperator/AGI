import Base
import ./A.bend as A
import ./LIT.bend as D

law wit:
  {A.b2u(A.wit_score_le(D.s(), D.w0(), D.w1(), 64, 1, 20)) == 1 : U32}
