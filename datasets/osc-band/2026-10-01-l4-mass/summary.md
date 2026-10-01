# L4 mass round: disproved (MASS beats random 1/3, needs 3; MASS KL < distance KL 1/3, needs 2)

calibration Spearman (mass) {"12-16": 0.9824142422926617, "12-18": 0.9907729049066435, "16-18": 0.9723187147199306}; calib leak False; script be4979294d3e04e7b205e38ae3d554b45709f292 dirty False

void checks: same k True; kept == runs 1/2 True; full-KV bit-exact x2 True; ref == runs 1/2 True

| budget | k | kept | metric | MASS | random min-max | distance | band | DIRECT | sinkcount | MASS beats random | MASS KL < distance |
|---|---|---|---|---|---|---|---|---|---|---|---|
| 0.75 | 13 | 0.7466 | agree | 0.9254 | 0.8481-0.8749 | 0.9221 | 0.8719 | 0.9546 | 0.9292 | True | True |
| 0.75 | 13 | 0.7466 | kl | 0.02477 | 0.06673-0.13505 | 0.02772 | 0.07223 | 0.00808 | 0.01985 | True | True |
| 0.6 | 21 | 0.5907 | agree | 0.8254 | 0.8083-0.8456 | 0.8511 | 0.8451 | 0.9214 | 0.8656 | False | False |
| 0.6 | 21 | 0.5907 | kl | 0.14616 | 0.10569-0.22234 | 0.09660 | 0.10034 | 0.02250 | 0.07394 | False | False |
| 0.5 | 26 | 0.4932 | agree | 0.8142 | 0.7777-0.8201 | 0.8286 | 0.8309 | 0.8888 | 0.8479 | False | False |
| 0.5 | 26 | 0.4932 | kl | 0.20745 | 0.18100-0.31205 | 0.15654 | 0.11705 | 0.04722 | 0.11325 | False | False |
