import Base
import ./A.bend as A
import ./LIT.bend as D

# g546_MC: MC (plasma) the distinct counter on 512 true target lines per cue reads >= 150 on every seed, MIN over cues
law ex:
  {A.b2u(A.ex_dist_ge(D.s0(), 150)) == 1 : U32}
