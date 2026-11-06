import Base
import ./G.bend as G
import ./VALUES.bend as V

# goal:g5.40 line 1: H-F1 (remix, "the proved ledger holds vacuous proofs") PROVED iff >= 2 of n mutants read survived; RED iff <= 1.
law g540_l1:
  {G.code(False{}, U32.is_ge(V.g540_survived(), 2)) == 1 : U32}
