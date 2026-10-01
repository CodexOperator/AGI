# L4 run 5 (served 9B): BLOCKED before any model pass -- memory gate never opened

- Pre-registered and committed (c72c99802743): head-window.patch (applies to llama.cpp 552f18f912a32ea86edf82e2b76431cb7131538d), build.sh, params.json with calibration docs 12/16/18 and fresh docs 32/33/34 (9B tokenizer, >= 2064 tokens; runs 1-4 docs excluded), osc_l4_9b.py (120 lines) + osc_l4_9b_test.py (4/4 pass).
- Built: base + patched llama-perplexity / llama-tokenize at the pinned sha, CPU only, inside a --memory 7g --cpus 6 container (logs/build.log).
- Gate (box rule): MemAvailable >= 8000 MiB AND memory PSI some avg10 < 5 before loading the 9B. --rank ran under model_slot.py from 10:50Z to 13:17Z: 49 checks every 180 s, MemAvailable 3555-6763 MiB, never >= 8000 (logs/run.log). Stopped by the builder at 13:17Z so the box-wide model slot was not held further. No model loaded, no base logits, no ranking, no score.
- Resume (every pass checkpoints by its log under params scratch): python3 .agi/context/local-maxxing/model_slot.py -- python3 .agi/context/local-maxxing/osc/osc_l4_9b.py --rank ; then --freeze, commit params.json + ranking.json, then --score.
