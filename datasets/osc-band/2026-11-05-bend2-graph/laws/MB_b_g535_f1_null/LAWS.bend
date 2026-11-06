import Base
import ./G.bend as G
import ./VALUES.bend as V

# goal:g5.35 line 1: The harness's own test passes, and the null run's committed results.json shows the null hit rate inside chance (1/5) at the one-sided binomial 95% band over n = 200. A null rate outside it = the harne
law b_g535_f1_null:
  {G.code(False{}, U32.is_lt(V.g535_null_hits(), V.g535_band())) == 1 : U32}
