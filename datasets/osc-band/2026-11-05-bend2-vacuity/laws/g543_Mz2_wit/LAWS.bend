import Base
import ./A.bend as A
import ./LIT.bend as D

# g543_Mz2: Mz2 Z3 trained with ONE uniform code PER TARGET per step ... falls to valid <= 0.1 on every seed
law wit:
  {A.b2u(A.wit_valid_le(D.s0(), D.w0(), D.w1(), 64, 1, 10)) == 1 : U32}
