# L4 distance round: proved (distance wins 3/3 budgets, needs 2)

calibration Spearman {"12-16": 0.9841511072514111, "12-18": 0.9760095527572731, "16-18": 0.9558184976118106}; calib leak False; script e18b2e41dd6685f1d2d770ebe831da96d74bd4d9 dirty False

void checks: same k True; kept == run 1 True; full-KV bit-exact x2 True; band+random == run 1 per doc True

| budget | k | kept | distance agree | random agree min-max | band agree | distance KL | random KL min-max | band KL | distance wins |
|---|---|---|---|---|---|---|---|---|---|
| 0.75 | 13 | 0.7466 | 0.9221 | 0.8481-0.8749 | 0.8719 | 0.02772 | 0.06673-0.13505 | 0.07223 | True |
| 0.6 | 21 | 0.5907 | 0.8511 | 0.8083-0.8456 | 0.8451 | 0.09660 | 0.10569-0.22234 | 0.10034 | True |
| 0.5 | 26 | 0.4932 | 0.8286 | 0.7777-0.8201 | 0.8309 | 0.15654 | 0.18100-0.31205 | 0.11705 | True |
