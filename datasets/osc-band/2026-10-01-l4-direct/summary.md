# L4 direct round: proved (DIRECT beats random 3/3, needs 3; DIRECT KL < sinkcount KL 3/3, needs 2)

fresh docs [20, 21, 22, 24, 25, 28, 29, 31]; script 33f22d9bf702409add66ac04634a10cf28bddcbb dirty False; params sha256 c3aba30f8c4c61309050533fa6806a294c2eb6658eb26dc17faae87f054b3383

void checks: fresh overlap False; frozen == run 3 True; full-KV bit-exact x2 True; same k True; kept == runs 1/3 True

| budget | k | kept | metric | DIRECT | random min-max | sinkcount | distance | band | DIRECT beats random | DIRECT KL < sinkcount |
|---|---|---|---|---|---|---|---|---|---|---|
| 0.75 | 13 | 0.7466 | agree | 0.9547 | 0.8384-0.8713 | 0.9241 | 0.9159 | 0.8672 | True | True |
| 0.75 | 13 | 0.7466 | kl | 0.00845 | 0.07618-0.14187 | 0.02239 | 0.03221 | 0.07610 | True | True |
| 0.6 | 21 | 0.5907 | agree | 0.9225 | 0.7953-0.8517 | 0.8646 | 0.8480 | 0.8405 | True | True |
| 0.6 | 21 | 0.5907 | kl | 0.02547 | 0.11354-0.25833 | 0.07916 | 0.10406 | 0.10771 | True | True |
| 0.5 | 26 | 0.4932 | agree | 0.8912 | 0.7599-0.8096 | 0.8357 | 0.8264 | 0.8309 | True | True |
| 0.5 | 26 | 0.4932 | kl | 0.05448 | 0.19736-0.35613 | 0.12626 | 0.17101 | 0.12764 | True | True |

| budget | k | joint KL | solo sum (fresh) | ratio | solo sum (run 3 calib) | ratio_run3 |
|---|---|---|---|---|---|---|
| 0.75 | 13 | 0.00845 | 0.00725 | 1.16546 | 0.00625 | 1.35134 |
| 0.6 | 21 | 0.02547 | 0.02409 | 1.05747 | 0.02143 | 1.18843 |
| 0.5 | 26 | 0.05448 | 0.04773 | 1.14127 | 0.04187 | 1.30114 |
