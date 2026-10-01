# L4 window round: disproved (band wins 1/3 budgets, needs 2)

void checks: kept within +-0.00975: True; full-KV bit-exact x2: True; W=L exact: True

| budget | k | kept | band agree | random agree min-max | ref agree | band KL | random KL min-max | ref KL | band wins |
|---|---|---|---|---|---|---|---|---|---|
| 0.75 | 13 | 0.7466 | 0.8719 | 0.8481-0.8749 | 0.9292 | 0.07223 | 0.06673-0.13505 | 0.01985 | False |
| 0.6 | 21 | 0.5907 | 0.8451 | 0.8083-0.8456 | 0.8656 | 0.10034 | 0.10569-0.22234 | 0.07394 | False |
| 0.5 | 26 | 0.4932 | 0.8309 | 0.7777-0.8201 | 0.8445 | 0.11705 | 0.18100-0.31205 | 0.12032 | True |
