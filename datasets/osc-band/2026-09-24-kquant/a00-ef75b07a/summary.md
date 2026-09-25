# OSC.14 per-channel / bias-subtracted key scales at 3.5 bits (a00-ef75b07a)

16-bit anchor d=5.758e-02 agree=1.0 KL=7.38e-07; hooks chan=True bias=True

| arm | bits | agree | mean KL | clears falsifier |
|---|---|---|---|---|
| token_absmax_3p5 | 3.5 | 0.564453 | 1.381633 | - |
| uniform_3p5 | 3.5 | 0.376953 | 2.417574 | - |
| per_channel_3p5 | 3.5 | 0.596191 | 1.087602 | no |
| bias_subtracted_3p5 | 4.5 | 0.696533 | 0.716746 | no |

delta per_channel - token_absmax: {"agree": 0.031738, "kl": -0.294031}
delta bias - token_absmax: {"agree": 0.13208, "kl": -0.664887}
arm4 is 4.5 nominal bits (bias charged extra), so only arm3 is a matched-3.5 comparison.
