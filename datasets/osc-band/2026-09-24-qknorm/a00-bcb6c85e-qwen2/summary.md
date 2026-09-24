# corrected qwen2

{
 "meta": {
  "event": "meta",
  "model": "qwen2",
  "hf": "/data/ml/scratch/osc03/hf",
  "offline": true,
  "eval": {
   "wiki_slice_starts": [
    5000,
    61000,
    120000,
    240000
   ],
   "wiki_span": 512,
   "heval_task_ids": [
    "HumanEval/107",
    "HumanEval/108",
    "HumanEval/109",
    "HumanEval/11"
   ],
   "heval_padded_to": 512,
   "n_prompts": 8,
   "n_tokens": 4096,
   "hop1_wiki_starts": [
    0,
    29875,
    59751,
    89627,
    119503,
    149379,
    179254,
    209130,
    239006,
    268882
   ],
   "hop1_heval_task_ids": [
    "HumanEval/0",
    "HumanEval/1",
    "HumanEval/10",
    "HumanEval/100",
    "HumanEval/101",
    "HumanEval/102",
    "HumanEval/103",
    "HumanEval/104",
    "HumanEval/105",
    "HumanEval/106"
   ]
  },
  "bits": {
   "energy_3p5": 3.5,
   "energy_4p5": 4.5,
   "energy_5p5": 4.75,
   "energy_6p5": 5.75,
   "energy_7p5": 6.75,
   "energy_8p5": 7.75,
   "energy_9p0": 9.0,
   "energy_10p0": 10.75,
   "uniform_3p5": 3.25,
   "random_3p5": 3.5
  },
  "capture": "post_rope_per_layer"
 },
 "settings": {
  "energy_3p5": {
   "agree": 0.541748,
   "kl": 1.504528,
   "bits": 3.5,
   "holds": false
  },
  "energy_4p5": {
   "agree": 0.759277,
   "kl": 0.487235,
   "bits": 4.5,
   "holds": false
  },
  "energy_5p5": {
   "agree": 0.780029,
   "kl": 0.405527,
   "bits": 4.75,
   "holds": false
  },
  "energy_6p5": {
   "agree": 0.822266,
   "kl": 0.283447,
   "bits": 5.75,
   "holds": false
  },
  "energy_7p5": {
   "agree": 0.880371,
   "kl": 0.116572,
   "bits": 6.75,
   "holds": false
  },
  "energy_8p5": {
   "agree": 0.933838,
   "kl": 0.032084,
   "bits": 7.75,
   "holds": false
  },
  "energy_9p0": {
   "agree": 0.96582,
   "kl": 0.007731,
   "bits": 9.0,
   "holds": false
  },
  "energy_10p0": {
   "agree": 0.990234,
   "kl": 0.000439,
   "bits": 10.75,
   "holds": true
  },
  "uniform_3p5": {
   "agree": 0.319824,
   "kl": 2.98773,
   "bits": 3.25,
   "holds": false
  },
  "random_3p5": {
   "agree": 0.162598,
   "kl": 4.70796,
   "bits": 3.5,
   "holds": false
  }
 },
 "lowest_holding_energy": 10.75,
 "bench": "a00-bcb6c85e-qwen2/bench/20260924T185029Z.jsonl",
 "t_s": 311.2
}
