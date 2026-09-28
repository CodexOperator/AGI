# true q4_0-analog post-RoPE key baseline (a00-3d746bb5)

16-bit anchor: max abs logit diff 5.758e-02, agree 1.0, KL 7.38e-07; patched-hook True.

| arm | bits | agree | mean KL | both bars |
|---|---|---|---|---|
| true_uniform_4p5 | 4.5 | 0.599609 | 1.439806 | False |
| energy_4p5 | 4.5 | 0.739502 | 0.545099 | False |

vs OLD ternary bw4 {'agree': 0.102783, 'kl': 5.749527, 'bits': 4.5}: {'agree': 0.496826, 'kl': -4.309721}
vs ddd4762f u45 matched control {'agree': 0.638916, 'kl': 1.021206}: {'agree': -0.039307, 'kl': 0.4186}
energy minus true uniform: {'agree': 0.139893, 'kl': -0.894707}
