import Base
import ./G.bend as G
import ./VALUES.bend as V

# goal:g5.42 line 2: STEP 1 RED iff X_all < 12642 (0.99 x 12769) or X_test / 8939 < 0.99: quantization broke the cut.
law g542_l2:
  {G.code(False{}, (U32.is_ge(V.g542_x_all(), 12642) && U32.is_ge((100 * V.g542_x_test() : U32), (99 * V.g542_n_test() : U32)))) == 1 : U32}
