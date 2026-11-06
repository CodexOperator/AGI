import Base
import ./A.bend as A
import ./LIT.bend as D

# g543_Mz6: Mz6 Z6-ENUM sampled through (code mod 8) ... must read distinct valid images < 16 per cue on EVERY seed
law ex:
  {A.b2u(A.ex_dist_le(D.s0(), 15)) == 1 : U32}
