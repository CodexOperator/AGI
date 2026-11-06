import Base
import ./A.bend as A
import ./LIT.bend as D

law ancestor:
  {A.b2u(A.proof_ok(D.x(), D.y(), D.path(), D.edges())) == 1 : U32}
