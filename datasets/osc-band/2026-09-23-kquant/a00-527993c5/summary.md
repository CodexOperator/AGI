# OSC-CTL.10 kquant control arm a00-527993c5

eval: 8 prompts x 512 = 4096 tokens (OSC.04 build_eval, disjoint from hop 1)
bars: agree >= 0.98 and mean per-token KL <= 0.02

| arm | avg_bits | avg_data_bits | C | agree | KL |
|---|---|---|---|---|---|
| blockwise4 | 4.5 | 4.0 | 2.0 | 0.636963 | 1.022623 |
| energy_2.25 | 2.25 | 2.0 | 1.0 | 0.063721 | 6.88805 |
| energy_2.5 | 2.5 | 2.0 | 2.0 | 0.074463 | 6.523471 |
| energy_2.75 | 2.75 | 2.25 | 2.0 | 0.21167 | 3.808879 |
| energy_3.0 | 3.0 | 2.5 | 2.0 | 0.381348 | 2.327351 |
| energy_3.25 | 3.25 | 3.0 | 1.0 | 0.351562 | 2.769425 |
| energy_3.5 | 3.5 | 3.0 | 2.0 | 0.570557 | 1.245039 |
| random_2.25_s1 | 2.25 | 2.0 | 1.0 | 0.063721 | 6.88805 |
| random_2.25_s2 | 2.25 | 2.0 | 1.0 | 0.063721 | 6.88805 |
| random_2.25_s3 | 2.25 | 2.0 | 1.0 | 0.063721 | 6.88805 |
| random_2.5_s1 | 2.5 | 2.0 | 2.0 | 0.092041 | 5.929442 |
| random_2.5_s2 | 2.5 | 2.0 | 2.0 | 0.108887 | 5.447042 |
| random_2.5_s3 | 2.5 | 2.0 | 2.0 | 0.071533 | 7.200797 |
| random_2.75_s1 | 2.75 | 2.25 | 2.0 | 0.071289 | 6.6999 |
| random_2.75_s2 | 2.75 | 2.25 | 2.0 | 0.06665 | 6.462626 |
| random_2.75_s3 | 2.75 | 2.25 | 2.0 | 0.094482 | 5.809161 |
| random_3.0_s1 | 3.0 | 2.5 | 2.0 | 0.059814 | 7.069855 |
| random_3.0_s2 | 3.0 | 2.5 | 2.0 | 0.098389 | 5.600891 |
| random_3.0_s3 | 3.0 | 2.5 | 2.0 | 0.103271 | 5.385601 |
| random_3.25_s1 | 3.25 | 3.0 | 1.0 | 0.351562 | 2.769425 |
| random_3.25_s2 | 3.25 | 3.0 | 1.0 | 0.351562 | 2.769425 |
| random_3.25_s3 | 3.25 | 3.0 | 1.0 | 0.351562 | 2.769425 |
| random_3.5_s1 | 3.5 | 3.0 | 2.0 | 0.096191 | 5.764528 |
| random_3.5_s2 | 3.5 | 3.0 | 2.0 | 0.32251 | 2.950648 |
| random_3.5_s3 | 3.5 | 3.0 | 2.0 | 0.265869 | 3.288806 |
| ubudget_2.25 | 2.25 | 2.0 | 1.0 | 0.063721 | 6.88805 |
| ubudget_2.5 | 2.25 | 2.0 | 1.0 | 0.063721 | 6.88805 |
| ubudget_2.75 | 2.25 | 2.0 | 1.0 | 0.063721 | 6.88805 |
| ubudget_3.0 | 2.25 | 2.0 | 1.0 | 0.063721 | 6.88805 |
| ubudget_3.25 | 3.25 | 3.0 | 1.0 | 0.351562 | 2.769425 |
| ubudget_3.5 | 3.25 | 3.0 | 1.0 | 0.351562 | 2.769425 |
| umatch_2.25 | 2.25 | 2.0 | 1.0 | 0.063721 | 6.88805 |
| umatch_2.5 | 2.25 | 2.0 | 1.0 | 0.063721 | 6.88805 |
| umatch_2.75 | 2.25 | 2.0 | 1.0 | 0.063721 | 6.88805 |
| umatch_3.0 | 2.25 | 2.0 | 1.0 | 0.063721 | 6.88805 |
| umatch_3.25 | 3.25 | 3.0 | 1.0 | 0.351562 | 2.769425 |
| umatch_3.5 | 3.25 | 3.0 | 1.0 | 0.351562 | 2.769425 |
| uniform_w2 | 2.25 | 2.0 | 1.0 | 0.063721 | 6.88805 |
| uniform_w3 | 3.25 | 3.0 | 1.0 | 0.351562 | 2.769425 |
| uniform_w4 | 4.25 | 4.0 | 1.0 | 0.62207 | 1.0519 |
| uniform_w5 | 5.25 | 5.0 | 1.0 | 0.671875 | 0.899372 |

## falsifier verdicts
{
 "3.5": {
  "a_energy_holds": false,
  "b_beats_uniform_matched": true,
  "b_delta": {
   "agree": 0.218995,
   "kl": -1.524386
  },
  "c_beats_random_mean": true,
  "c_random_mean": {
   "agree": 0.22819,
   "kl": 4.001327
  }
 },
 "3.25": {
  "a_energy_holds": false,
  "b_beats_uniform_matched": false,
  "b_delta": {
   "agree": 0.0,
   "kl": 0.0
  },
  "c_beats_random_mean": false,
  "c_random_mean": {
   "agree": 0.351562,
   "kl": 2.769425
  }
 },
 "3.0": {
  "a_energy_holds": false,
  "b_beats_uniform_matched": true,
  "b_delta": {
   "agree": 0.317627,
   "kl": -4.560699
  },
  "c_beats_random_mean": true,
  "c_random_mean": {
   "agree": 0.087158,
   "kl": 6.018782
  }
 },
 "2.75": {
  "a_energy_holds": false,
  "b_beats_uniform_matched": true,
  "b_delta": {
   "agree": 0.147949,
   "kl": -3.079171
  },
  "c_beats_random_mean": true,
  "c_random_mean": {
   "agree": 0.077474,
   "kl": 6.323896
  }
 },
 "2.5": {
  "a_energy_holds": false,
  "b_beats_uniform_matched": true,
  "b_delta": {
   "agree": 0.010742,
   "kl": -0.364579
  },
  "c_beats_random_mean": false,
  "c_random_mean": {
   "agree": 0.09082,
   "kl": 6.192427
  }
 },
 "2.25": {
  "a_energy_holds": false,
  "b_beats_uniform_matched": false,
  "b_delta": {
   "agree": 0.0,
   "kl": 0.0
  },
  "c_beats_random_mean": false,
  "c_random_mean": {
   "agree": 0.063721,
   "kl": 6.88805
  }
 }
}

## largest safe step
{
 "lowest_budget_holding_both_bars_energy": null,
 "energy_holds": [],
 "lowest_budget_holding_both_bars_uniform_matched": null
}
