import Base
import ./A.bend as A
import ./LIT.bend as D

# g541_M1C: M1-C = G-chamfer with ONE draw frozen per seed and cue scores <= 0.05 on every seed
law ex:
  {A.b2u(A.ex_score_le(D.s0(), 64, 1, 20)) == 1 : U32}
