import Base
import ./LAWS.bend as Laws

def Laws.g541_l3(r_coverage_ge_0_9, r_gc_minus_g_5of5_mean):
  match r_coverage_ge_0_9 r_gc_minus_g_5of5_mean:
    case True{} True{}:
      {==}
    case True{} False{}:
      {==}
    case False{} True{}:
      {==}
    case False{} False{}:
      {==}
