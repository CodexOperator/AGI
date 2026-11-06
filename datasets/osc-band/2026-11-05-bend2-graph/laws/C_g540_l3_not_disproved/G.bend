import Base

# verdict codes: 0 disproved, 1 proved, 2 void (the void gate is read first)
def code(void: Bool, proved: Bool) -> U32:
  match void:
    case True{}:
      2
    case False{}:
      match proved:
        case True{}:
          1
        case False{}:
          0
