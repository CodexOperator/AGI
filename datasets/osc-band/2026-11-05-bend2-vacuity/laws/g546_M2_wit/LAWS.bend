import Base
import ./A.bend as A
import ./LIT.bend as D

# g546_M2: M2 the scorer arm as in g5.39
law wit:
  {A.b2u(A.wit_score_ge(D.s0(), D.w0(), D.w1(), 64, 9, 10)) == 1 : U32}
