# Scored Qwen3 QK-norm key quantization

offline flags: True
eval: 8x512=4096 tokens

| arm | bits | agree | KL | holds |
|---|---:|---:|---:|---|
| energy_3p5 | 3.5 | 0.019287 | 10.703563 | False |
| energy_4p5 | 4.5 | 0.133545 | 5.633689 | False |
| energy_5p5 | 4.75 | 0.140625 | 5.580092 | False |
| energy_6p5 | 5.75 | 0.481689 | 2.002619 | False |
| energy_7p5 | 6.75 | 0.794922 | 0.304308 | False |
| energy_8p5 | 7.75 | 0.915527 | 0.055774 | False |
| energy_9p0 | 9.0 | 0.965088 | 0.006433 | False |
| energy_10p0 | 10.75 | 0.992188 | 0.000435 | True |
| uniform_3p5 | 3.125 | 0.019775 | 11.257038 | False |
| random_3p5 | 3.5 | 0.023438 | 9.936828 | False |

Lowest tested energy budget holding both bars: 10.75 bits.
Comparator cited: experiment:a00-86466b78-c8d14f; cross-checks a00-527993c5 and a00-ddd4762f.
