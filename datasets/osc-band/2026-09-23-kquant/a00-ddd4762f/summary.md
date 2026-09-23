# OSC.10 L3 band-energy KEY quantization

eval 4096 tokens; budgets and metrics

| setting | bits/el | agree | mean KL |
|---|---|---|---|
| q16 | 16.25 | 0.999512 | 0.0 |
| e30 | 3.0 | 0.387939 | 2.318338 |
| e35a | 3.5 | 0.605225 | 1.124264 |
| e35b | 3.5 | 0.606934 | 1.108971 |
| e45 | 4.5 | 0.814453 | 0.255067 |
| u30 | 3.0 | 0.214355 | 3.988572 |
| u35 | 3.5 | 0.385498 | 2.498157 |
| u45 | 4.5 | 0.638916 | 1.021206 |
| rand_s1 | - | 0.236328 | 3.432425 |
| rand_s2 | - | 0.141113 | 4.429217 |
| rand_s3 | - | 0.158691 | 4.313292 |

q16 anchor ok: True
at 3.5: {"energy_pass": false, "energy_agree": 0.605225, "energy_kl": 1.124264, "uniform_agree": 0.385498, "uniform_kl": 2.498157, "beats_uniform_both": true}
random: {"agree": {"1": 0.236328, "2": 0.141113, "3": 0.158691}, "mean_agree": 0.178711, "energy_beats_random": true}
lowest bits both hold: q16
