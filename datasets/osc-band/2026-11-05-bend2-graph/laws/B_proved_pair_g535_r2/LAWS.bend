import Base
import ./G.bend as G
import ./VALUES.bend as V

# goal:g5.35 line 1: The harness's own test passes, and the null run's committed results.json shows the null hit rate inside chance (1/5) at the one-sided binomial 95% band over n = 200. A null rate outside it = the harne
law b_g535_f1_null:
  {G.code(False{}, U32.is_lt(V.g535_null_hits(), V.g535_band())) == 1 : U32}

# goal:g5.35 line 2: Mutant, which must read RED: a viewer that is GIVEN the revealed salt (a planted leak) must score above the band. If it does not, the harness cannot detect a leak and is vacuous.
law b_g535_f2_salt:
  {G.code(False{}, U32.is_ge(V.g535_salt_hits(), V.g535_band())) == 1 : U32}
