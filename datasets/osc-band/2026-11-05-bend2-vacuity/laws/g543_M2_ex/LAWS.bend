import Base
import ./A.bend as A
import ./LIT.bend as D

# g543_M2: M2 the scorer arm as in g5.39
law ex:
  {A.b2u(A.ex_score_ge(D.s0(), 64, 9, 10) || A.ex_valid_le(D.s1(), 64, 1, 20)) == 1 : U32}
