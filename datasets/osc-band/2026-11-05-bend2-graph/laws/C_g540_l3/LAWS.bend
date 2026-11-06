import Base
import ./G.bend as G
import ./VALUES.bend as V

# goal:g5.40 line 3: VOID if more than 5 of 20 are NOT RUNNABLE, or n < 10.
law g540_l3:
  {G.code((U32.is_gt(V.g540_not_runnable(), 5) || U32.is_lt(V.g540_items(), 10)), Bool.not((U32.is_gt(V.g540_not_runnable(), 5) || U32.is_lt(V.g540_items(), 10)))) == 1 : U32}
