import Base
import ./NET.bend as N

law net_is_parity:
  for x0: Bool
  for x1: Bool
  for x2: Bool
  for x3: Bool
  for x4: Bool
  for x5: Bool
  for x6: Bool
  for x7: Bool
  {N.net(x0, x1, x2, x3, x4, x5, x6, x7) == N.parity(x0, x1, x2, x3, x4, x5, x6, x7) : U32}
