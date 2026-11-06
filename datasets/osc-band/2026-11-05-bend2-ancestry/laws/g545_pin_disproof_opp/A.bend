import Base

# goal:g5.47: reachability over commit records. An id is a sha1 as 5 big-endian U32 words; a level is the generation
# number (1 + max over parents). proof_ok: the path starts at X, ends at Y, and every step is a LISTED edge.
# disproof_ok: R starts with X's record; for every record r in R: r is not Y, and every parent p of r (ALL listed, with
# levels) has level(p) < level(r), agrees with R's own record of p if R lists one, and is in R or below level(Y).

type Par is Data:
  Par{id: +List<U32>, lev: U32}

type Rec is Data:
  Rec{id: +List<U32>, lev: U32, ps: +List<Par>}

type Edge is Data:
  Edge{c: +List<U32>, p: +List<U32>}

def b2u(x: Bool) -> U32:
  match x:
    case True{}:
      1
    case False{}:
      0

def ideq(a: +List<U32>, b: +List<U32>) -> Bool:
  match a b:
    case Nil{} Nil{}:
      True{}
    case Nil{} Con{y, bt}:
      False{}
    case Con{x, at} Nil{}:
      False{}
    case Con{x, at} Con{y, bt}:
      U32.is_eq(x, y) && ideq(at, bt)

def edge_is(e: Edge, +c: +List<U32>, +p: +List<U32>) -> Bool:
  match e:
    case Edge{ec, ep}:
      ideq(ec, c) && ideq(ep, p)

def has_edge(es: +List<Edge>, +c: +List<U32>, +p: +List<U32>) -> Bool:
  match es:
    case Nil{}:
      False{}
    case Con{e, t}:
      edge_is(e, c, p) || has_edge(t, c, p)

def steps(rest: +List<+List<U32>>, +prev: +List<U32>, +es: +List<Edge>, +y: +List<U32>) -> Bool:
  match rest:
    case Nil{}:
      ideq(prev, y)
    case Con{+n, t}:
      has_edge(es, prev, n) && steps(t, n, es, y)

def proof_ok(+x: +List<U32>, +y: +List<U32>, path: +List<+List<U32>>, +es: +List<Edge>) -> Bool:
  match path:
    case Nil{}:
      False{}
    case Con{+h, t}:
      ideq(h, x) && steps(t, h, es, y)

def rec_is(r: Rec, +id: +List<U32>) -> Bool:
  match r:
    case Rec{rid, rl, ps}:
      ideq(rid, id)

def in_recs(rs: +List<Rec>, +id: +List<U32>) -> Bool:
  match rs:
    case Nil{}:
      False{}
    case Con{r, t}:
      rec_is(r, id) || in_recs(t, id)

def lev_agrees(r: Rec, +id: +List<U32>, +lev: U32) -> Bool:
  match r:
    case Rec{rid, rl, ps}:
      Bool.not(ideq(rid, id)) || U32.is_eq(rl, lev)

def levs_agree(rs: +List<Rec>, +id: +List<U32>, +lev: U32) -> Bool:
  match rs:
    case Nil{}:
      True{}
    case Con{r, t}:
      lev_agrees(r, id, lev) && levs_agree(t, id, lev)

def par_ok(+all: +List<Rec>, +clev: U32, +ylev: U32, p: Par) -> Bool:
  match p:
    case Par{+pid, +pl}:
      U32.is_lt(pl, clev) && levs_agree(all, pid, pl) && (in_recs(all, pid) || U32.is_lt(pl, ylev))

def pars_ok(+all: +List<Rec>, +clev: U32, +ylev: U32, ps: +List<Par>) -> Bool:
  match ps:
    case Nil{}:
      True{}
    case Con{p, t}:
      par_ok(all, clev, ylev, p) && pars_ok(all, clev, ylev, t)

def rec_ok(+all: +List<Rec>, +y: +List<U32>, +ylev: U32, r: Rec) -> Bool:
  match r:
    case Rec{rid, rl, ps}:
      Bool.not(ideq(rid, y)) && pars_ok(all, rl, ylev, ps)

def recs_ok(+all: +List<Rec>, +y: +List<U32>, +ylev: U32, rs: +List<Rec>) -> Bool:
  match rs:
    case Nil{}:
      True{}
    case Con{r, t}:
      rec_ok(all, y, ylev, r) && recs_ok(all, y, ylev, t)

def head_is(rs: +List<Rec>, +x: +List<U32>) -> Bool:
  match rs:
    case Nil{}:
      False{}
    case Con{r, t}:
      rec_is(r, x)

def disproof_ok(+x: +List<U32>, +y: +List<U32>, +ylev: U32, +rs: +List<Rec>) -> Bool:
  head_is(rs, x) && recs_ok(rs, y, ylev, rs)
