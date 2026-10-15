# TypeSafe ledger — hypothesis:lm-typesafe-replay-200 (TM.25)

Account: owner TypeSafe account (NOT the OpenRouter account).

| item | value |
|---|---|
| authorized budget | <= $0.10 TypeSafe input (<= 2M input tokens @ 0.045/1M) |
| calls made | 0 authenticated |
| network probes | 1 unauthenticated (HTTP 403, no spend) |
| spend this round | $0.000000 |
| ledger line | USD = tokens x 0.045/1M = 0 x 0.045/1M = $0.000000 |

Reason: `TYPESAFE_KEY` is absent from the agent spawn environment (measured
`python3 -c "import os;print('TYPESAFE_KEY' in os.environ)"` -> `False`), so the
replay is BLOCKED:no_key and no authenticated call was made. Nothing to bill.
