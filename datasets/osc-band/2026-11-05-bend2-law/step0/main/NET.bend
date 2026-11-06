import Base

def b2u(x: Bool) -> U32:
  match x:
    case True{}:
      1
    case False{}:
      0

def ge(+s: U32, k: U32) -> U32:
  b2u(U32.is_ge(s, k))

def net(x0: Bool, x1: Bool, x2: Bool, x3: Bool, x4: Bool, x5: Bool, x6: Bool, x7: Bool) -> U32:
  +s = (((((((b2u(x0) + b2u(x1) : U32) + b2u(x2) : U32) + b2u(x3) : U32) + b2u(x4) : U32) + b2u(x5) : U32) + b2u(x6) : U32) + b2u(x7) : U32)
  (((((((((1 * ge(s, 1) : U32)) + ((4294967295 * ge(s, 2) : U32)) : U32) + ((1 * ge(s, 3) : U32)) : U32) + ((4294967295 * ge(s, 4) : U32)) : U32) + ((1 * ge(s, 5) : U32)) : U32) + ((4294967295 * ge(s, 6) : U32)) : U32) + ((1 * ge(s, 7) : U32)) : U32) + ((4294967295 * ge(s, 8) : U32)) : U32)

def parity(x0: Bool, x1: Bool, x2: Bool, x3: Bool, x4: Bool, x5: Bool, x6: Bool, x7: Bool) -> U32:
  ((((((((b2u(x0) + b2u(x1) : U32) + b2u(x2) : U32) + b2u(x3) : U32) + b2u(x4) : U32) + b2u(x5) : U32) + b2u(x6) : U32) + b2u(x7) : U32) % 2 : U32)
