import Base
import ./A.bend as A
import ./LIT.bend as D

# g541_M1S: M1-S = S with every unit frozen at its likelier state scores <= 0.05 on every seed
law wit:
  {A.b2u(A.wit_score_le(D.s0(), D.w0(), D.w1(), 64, 1, 20)) == 1 : U32}
