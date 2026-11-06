import Base
import ./A.bend as A
import ./LIT.bend as D

# g543_Mz1: Mz1 EVERY latent arm with its latent FIXED at sampling scores <= 0.05 on every seed
law wit:
  {A.b2u(A.wit_score_le(D.s0(), D.w0(), D.w1(), 64, 1, 20)) == 1 : U32}
