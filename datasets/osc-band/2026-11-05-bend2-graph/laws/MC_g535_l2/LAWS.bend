import Base
import ./G.bend as G
import ./VALUES.bend as V

# goal:g5.35 line 2: Mutant, which must read RED: a viewer that is GIVEN the revealed salt (a planted leak) must score above the band. If it does not, the harness cannot detect a leak and is vacuous.
law g535_l2_mc:
  {G.code(U32.is_lt(V.g535_salt_hits(), V.g535_band()), U32.is_ge(V.g535_salt_hits(), V.g535_band())) == 2 : U32}
