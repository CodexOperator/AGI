import Base
import ./A.bend as A
import ./LIT.bend as D

# P_taut: planted tautology: valid count >= 0
law ex:
  {A.b2u(A.ex_valid_ge(D.s0(), 64, 0, 1)) == 1 : U32}
