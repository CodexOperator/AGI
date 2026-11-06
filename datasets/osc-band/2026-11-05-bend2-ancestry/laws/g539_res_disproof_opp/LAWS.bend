import Base
import ./A.bend as A
import ./LIT.bend as D

law not_ancestor:
  {A.b2u(A.disproof_ok(D.x(), D.y(), D.ylev(), D.recs())) == 1 : U32}
