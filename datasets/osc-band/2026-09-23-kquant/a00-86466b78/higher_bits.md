# largest-safe-step search above 3.5 bits

| arm | avg bits | agree | mean KL | holds |
|---|---|---|---|---|
| energy_3p5 | 3.5 | 0.564453 | 1.381633 | False |
| energy_6p0 | 6.0 | 0.826904 | 0.258263 | False |
| energy_8p0 | 8.0 | 0.93335 | 0.034139 | False |
| uniform_w8 | 8.25 | 0.928711 | 0.038262 | False |
| energy_9p0 | 9.0 | 0.981934 | 0.001932 | True |
| rand_9p0_s1 | 9.0 | 0.95166 | 0.01739 | False |
| rand_9p0_s2 | 9.0 | 0.928467 | 0.041971 | False |
| rand_9p0_s3 | 9.0 | 0.950684 | 0.018682 | False |
| uniform_w9 | 9.25 | 0.963135 | 0.007634 | False |
| uniform_w10 | 10.25 | 0.983154 | 0.00231 | True |
| energy_10p5 | 10.5 | 0.98584 | 0.001306 | True |
| uniform_w11 | 11.25 | 0.989502 | 0.000488 | True |
| uniform_w12 | 12.25 | 0.994629 | 0.000135 | True |
| energy_13p0 | 13.0 | 0.998779 | 9e-06 | True |

lowest avg bits holding both bars: energy_9p0
per family: {'energy': 9.0, 'uniform': 10.25}
