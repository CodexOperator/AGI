import Base
import ./A.bend as A
import ./LIT.bend as D

# P_taut: planted tautology: valid count >= 0
law wit:
  {A.b2u(A.wit_valid_ge(D.s0(), D.w0(), D.w1(), 64, 0, 1)) == 1 : U32}
