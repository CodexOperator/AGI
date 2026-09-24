# OSC.10 L3: RoPE-band-energy key bit allocation (K=4)

16-bit keys: max abs logit diff 5.758e-02, agree 1.0000, KL 7.38e-07. Hook: {'q_untouched': True, 'attn_k_is_quant_postrope_k': True, 'quant_changes_k': True}

| arm | avg bits/elem | agree | mean KL |
|---|---|---|---|
| bw4 | 4.5 | 0.102783 | 5.749527 |
| energy_3p5 | 3.5 | 0.564453 | 1.381633 |
| rand_3p5_s1 | 3.5 | 0.145508 | 5.00187 |
| rand_3p5_s2 | 3.5 | 0.149658 | 4.983416 |
| rand_3p5_s3 | 3.5 | 0.159912 | 5.136082 |
| uniform_3p5 | 3.5 | 0.376953 | 2.417574 |

| point | A energy holds both | dAgree E-U | dKL E-U | dAgree E-R | dKL E-R |
|---|---|---|---|---|---|
| 3p5 | False | 0.1875 | -1.035941 | 0.41276 | -3.658823 |

arms holding agree>=0.98 and KL<=0.02: []
