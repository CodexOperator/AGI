import Base
import ./A.bend as A
import ./LIT.bend as D

# g546_MK: MK CV with z ZEROED in TRAINING ..., z ~ N(0, I) at sampling, scores <= 0.05 AND has <= 16 distinct valid per cue of 512 on every seed
law wit:
  {A.b2u(A.wit_score_le(D.s0(), D.w0(), D.w1(), 64, 1, 20)) == 1 : U32}
