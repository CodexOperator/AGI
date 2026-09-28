# OSC.10 L3 band-energy KEY quantization

eval 4096 tokens; budgets and metrics

| setting | bits/el | agree | mean KL |
|---|---|---|---|
| q16 | 16.25 | 0.999512 | 0.0 |
| e60 | 6.0 | 0.813721 | 0.331524 |
| e80 | 8.0 | 0.943115 | 0.024007 |
| e120 | 12.0 | 0.996094 | 0.000115 |
| u60 | 6.0 | 0.783936 | 0.403038 |
| u80 | 8.0 | 0.932373 | 0.029098 |
| u120 | 12.0 | 0.994629 | 0.00023 |

q16 anchor ok: True
lowest bits both hold: e120
