import Base

type Col is Data:
  Col{b: U32, w: +List<U32>}

type Pr is Data:
  Pr{h: +List<U32>, n: +List<U32>}

def sgn(x: U32) -> U32:
  U32.xor(x, 2147483648)

def dot(w: +List<U32>, +h: +List<U32>, acc: U32) -> U32:
  match w h:
    case Nil{} _:
      acc
    case Con{x, wt} Nil{}:
      acc
    case Con{x, wt} Con{y, ht}:
      dot(wt, ht, (acc + x * y : U32))

def sel(c: Bool, x: U32, y: U32) -> U32:
  match c:
    case True{}:
      x
    case False{}:
      y

def b2u(x: Bool) -> U32:
  match x:
    case True{}:
      1
    case False{}:
      0

def hit(bi: U32, tie: Bool, +label: U32) -> U32:
  b2u(Bool.not(tie) && U32.is_eq(bi, label))

def scan(ns: +List<U32>, +cols: +List<Col>, +h: +List<U32>, +label: U32, +j: U32, bi: U32, +bv: U32, tie: Bool) -> U32:
  match ns cols:
    case Nil{} _:
      hit(bi, tie, label)
    case Con{n, nt} Nil{}:
      hit(bi, tie, label)
    case Con{+n, nt} Con{Col{+b, w}, ct}:
      +v = ((n + b : U32) + dot(w, h, 0) : U32)
      +gt = U32.is_gt(sgn(v), sgn(bv))
      +eq = U32.is_eq(v, bv)
      scan(nt, ct, h, label, (j + 1 : U32), sel(gt, j, bi), sel(gt, v, bv), Bool.not(gt) && (eq || tie))

def pair_hit(p: Pr, +cols: +List<Col>, +a: U32, +b: U32) -> U32:
  match p:
    case Pr{h, ns}:
      scan(ns, cols, h, ((a + b : U32) % 113 : U32), 0, 0, 2147483648, False{})

def row(ps: List<Pr>, +cols: +List<Col>, +a: U32, +b: U32, acc: U32) -> U32:
  match ps:
    case Nil{}:
      acc
    case Con{p, t}:
      row(t, cols, a, (b + 1 : U32), (acc + pair_hit(p, cols, a, b) : U32))

def rows(rs: List<List<Pr>>, +cols: +List<Col>, +a: U32, acc: U32) -> U32:
  match rs:
    case Nil{}:
      acc
    case Con{r, t}:
      rows(t, cols, (a + 1 : U32), (acc + row(r, cols, a, 0, 0) : U32))
