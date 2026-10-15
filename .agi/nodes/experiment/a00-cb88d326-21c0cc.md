---
id: experiment:a00-cb88d326-21c0cc
mint_id: 13032d9967d44f06822093fbc630d7a2
type: experiment
parents:
  - hypothesis:lm-uno-diffusion-draft-on-l4
next_edges: []
confidence: 0.55
edited_by: a00-59c581e7
evidence_runs:
  - experiment:a00-cb88d326-21c0cc
line_ceiling: 150
loop: hypothesis:lm-uno-diffusion-draft-on-l4@s2
model: deepseek/deepseek-v4.1-flash
probes:
  - {"conjunct": 1, "class": "wire", "cmd": "camber job get 27689 --output json + camber job list --output json", "expected": "one XS GPU job, with_gpu=true, XSMALL, 1 node, COMPLETED, nothing RUNNING, no second job", "observed": "27689 with_gpu=True node_size=XSMALL num_nodes=1 COMPLETED created 2026-09-18T13:24:18Z started 13:28:10Z finished 13:32:21Z; list total=2 (27649 step-1, 27689) running=[]", "result": "pass"}
  - {"conjunct": 2, "class": "wire", "cmd": "camber job logs 27689 | grep -E MARK|OutOfMemory", "expected": "stack installs and 16.38+0.70 GB load beside base within 20 min", "observed": "install markers real: torch_ready 54s fa2_ready 69s deps_ready 73s repo_ready 134s download_exit 0 download_done 154s; then arm_base_FAILED torch.OutOfMemoryError 21.69 GiB of 22.03 GiB during load_model BEFORE any KV cache -> the fit assertion is REFUTED on the actual 22.03 GiB device", "result": "pass"}
  - {"conjunct": 3, "class": "gate", "cmd": "python3 json scan of uno/rows.jsonl + bench/20260918T134243Z.jsonl for any positive tok_s or identical>0", "expected": "the >=1.5x / >=1.3x + byte-identical success gate CANNOT be certified from the committed bytes; values absent, not fabricated", "observed": "uno_base_batch1_tok_s=null, uno_batch8_tok_s=null, uno_identical_prompts=0/20; log MARK rows_written 0; no fabricated ratio", "result": "pass"}
  - {"conjunct": 4, "class": "gate", "cmd": "grep rows.jsonl for tpf|acceptance|per-prompt rows", "expected": "no TPF or acceptance rate recorded because no arm generated a token", "observed": "0 matches; per-prompt rows absent (rows_written 0); only 3 summary rows", "result": "pass"}
  - {"conjunct": 5, "class": "auth", "cmd": "git diff ab58f9857..c4f1f4972 -- uno/ bench/ node | grep -Ei host|ip|GPU model|key id", "expected": "box aliases only, no host name, IP, key id; every row key uno_*; GPU-minutes derive from the real job lifecycle", "observed": "no host/IP/key; all row keys uno_*; billed wall started->finished 251s = 4.18 GPU-min matches the lifecycle; ONE public paper GPU model name (H200-class) in the node prose describing the PAPER, not the rental", "result": "pass"}
production_lines: 68
profile: balanced
role: kid
scaffold_hash: d32d2558923ae97c
season: 2
title: "Uno step 2 on one XS GPU job: stack and 16 GiB bundle load in 134s/154s but the 8B base OOMs at weight load on 22.03 GiB (21.69 GiB live) and my runner cannot survive a failed arm"
town: local-maxxing
verdict: inconclusive_lean_disproved:55
---
<!-- BODY:BEGIN -->
# experiment:a00-cb88d326-21c0cc

## Experiment

Step 2 of `hypothesis:lm-uno-diffusion-draft-on-l4`: ONE one-shot Camber GPU
XSMALL (device visible = 22563 MiB = 22.03 GiB), job **27689**, run
2026-09-18 13:28:10Z -> 13:32:21Z (wall 251 s; created 13:24:18Z). Command log
appended to `.agi/context/local-maxxing/uno/cmds.md`; rows in
`uno/rows.jsonl` and `bench/20260918T134243Z.jsonl`.

The entire remote script (`work.sh`, embedding `run_arm.py` + the 20 prompts)
was base64'd into the single `--cmd`, with `timeout -s TERM 2820` so the command
self-limits to 47 min. Nothing was uploaded to any shared place; model bytes
landed on the rental only.

### What worked (fast)

| step | observed |
|---|---|
| uv + CPython 3.10.12 (box had 3.11.7) | 2 s |
| torch 2.11.0 cu128 installed | `torch_ready 54s` |
| FlashAttention-2 wheel (pinned cp310 cu12torch2.11) | `fa2_ready 69s` |
| deps (transformers 4.55.0, triton 3.6.0, ...) | `deps_ready 73s` |
| `git clone ifm-ai/uno` + `pip install -e . --no-deps` | `repo_ready 134s` |
| download `s-sahoo/uno-qwen3-8B` (16 GiB bundle, hf_transfer, 8 workers) | `download_done 154s` (~106 MB/s observed) |
| `torch.cuda.is_available()` | True, `dev_mem_MiB 22563` |

The INSTALL did not fail: the whole stack was ready in 134 s and the 16 GiB
bundle in 154 s. Nothing in this round is evidence for the "does not install"
falsifier.

### What failed

Both arms raised before generating a single token.

```
MARK arm_base_FAILED
torch.OutOfMemoryError: CUDA out of memory. Tried to allocate 96.00 MiB.
GPU 0 has a total capacity of 22.03 GiB of which 65.12 MiB is free.
this process has 21.96 GiB memory in use. Of the allocated memory 21.69 GiB is
allocated by PyTorch; 65.15 MiB is reserved by PyTorch but unallocated.
  at .../nano_vllm_uno/utils/loader.py:34  weight_dict = {k: f.get_tensor(k) ...}
  at .../nano_vllm_uno/engine/model_runner.py:113  load_model(self.model, config.model)
MARK arm_uno_FAILED
ValueError: trying to initialize the default process group twice!
  at .../engine/model_runner.py:87  dist.init_process_group(...)
METRIC uno_identical_prompts=0/20
```

96.00 MiB = 4096 x 12288 x 2 B, i.e. one MLP weight matrix in bf16, so the
dtype was bf16 as intended. The checkpoint index reports `total_size`
16,381,470,720 B = 15.26 GiB (8.19 B params bf16), yet **21.69 GiB** was live
by the time the last shard was copied. The OOM is inside `load_model`, BEFORE
`warmup_model` and `allocate_kv_cache` -- so it is not KV cache and not the
gpu_memory_utilization reserve.

Two independent defects, and the second is mine:

1. **Peak GPU during weight load ~= 21.7 GiB on a 22.03 GiB device.** The
   checkpoint is 15.26 GiB, so ~6.4 GiB is live beyond the parameters. The most
   likely mechanism is `torch.set_default_device("cuda")` (model_runner.py:101)
   being active while the loader builds a whole shard's `weight_dict`:
   `safe_open(file, "pt", "cpu")` is passed "cpu", but any tensor materialised
   without an explicit device inside that window lands on the GPU, so peak =
   params + one shard. 15.26 + ~4 GiB (largest shard) + context is in the right
   range. UNVERIFIED -- it is a hypothesis about the engine, not a measurement.
2. **My driver does not survive a failed arm.** The first `LLM.__init__` raised
   after `dist.init_process_group` ran, so the second arm hit "default process
   group twice". `run_arm.py` must fork one subprocess per arm (or call
   `torch.distributed.destroy_process_group()` / `sys.exit`) so a failed arm
   cannot poison the next.

### Consequence for the claim

NO tok/s measurement exists. The claim is neither proved nor disproved by this
round; the only thing it establishes is that the *default-shaped* invocation
(`max_model_len` 8192, `max_num_batched_tokens` 8192) OOMs an L4-class 22.03 GiB
device during weight load. The paper ran this engine on an H200-class device,
and the brief's "16.38 + 0.70 GB fits 24 GB" did not account for any load-time
peak above the parameter bytes.

### The retry recipe (one job, if granted)

- run each arm in its own subprocess (fix 2), so a failure is isolated;
- `max_model_len 4096`, `max_num_batched_tokens 1024` (nothing in this round
  needs more: 8 seqs x 256 tokens = 2048), and export
  `PYTORCH_CUDA_ALLOC_CONF=expandable_segments:True`;
- add a cheap **fallback arm** that always fits: `IFM/K2-Horizon-0.9B` +
  `IFM/K2-Horizon-0.9B-Uno` (2.16 + 0.22 GiB, Apache-2.0) measured the same way,
  so even if the 8B still will not fit, the round returns Uno-vs-base tok/s and
  the identical-greedy check at 0.9B scale;
- keep FA3 skipped (Hopper-only) and the linear sampler only.

### Escalation (banked)

The kid brief says ONE Camber job ONLY and the Prime wrote "No further Camber
job of any size without its own per-job line through me". The sanctioned unit
was one XS GPU-hour; this job billed ~4.2 GPU-min. A retry that fixes the two
defects above would still sit inside that hour, but it needs an explicit
per-job line. **Requested: one more XS GPU job line for the recipe above.**

## Evidence

- `MARK`/`METRIC` lines and both tracebacks: `camber job logs 27689`
  (saved to the session scratch `job.log`).
- Timing marks: torch 54 s, fa2 69 s, deps 73 s, repo 134 s, download 154 s.
- Device: 22563 MiB visible; OOM at 21.69 GiB allocated / 22.03 GiB total.
- Checkpoint index `total_size` 16,381,470,720 B; 399 tensors; 5 shards.
- Teardown: `camber job list --output json` -> 27689 COMPLETED, nothing RUNNING.

## Agent Notes
Job 27689: one XS GPU job, 251 s wall, ~4.2 GPU-min billed. Install (134 s) and the 16 GiB bundle (154 s) SUCCEEDED; NO tok/s: base arm OOMs inside load_model at 21.69 GiB live of 22.03 GiB (checkpoint is only 15.26 GiB, so ~6.4 GiB load-time peak above params; likely torch.set_default_device('cuda') materialising a shard in the loader), and my runner then died on 'default process group twice' so the Uno arm never ran. Teardown verified, nothing RUNNING. Retry recipe (per-arm subprocess, max_model_len 4096, max_num_batched_tokens 1024, expandable_segments, add the 0.9B Uno fallback) is in the node; it needs ONE more XS GPU job line from the Prime.

<!-- THOUGHT:BEGIN — authored, not derived; carried across regenerating scans. The reasoning behind THIS version. -->
PARENT REVIEW (a00-59c581e7, TM.36) — diff read, not the result file.

(1) INSTRUCTION: a kid's tests are its claim, not my evidence; read the kid DIFF (git diff merge-base..kid-branch), run one negative probe per claim conjunct myself, record them as probes: on the kid node (SL7.110).
(2) MACHINE: the kid's whole diff is `git show --stat c4f1f4972` = 5 files, +204 lines (bench jsonl 5, cmds.md +40, prompts.jsonl 20, rows.jsonl 3, node +136). I re-ran the Camber surface myself — `camber job get 27689` (with_gpu=True, XSMALL, COMPLETED 13:28:10->13:32:21Z, 251 s), `camber job list` (total=2, running=[]), `camber job logs 27689` (torch_ready 54s, fa2_ready 69s, deps_ready 73s, repo_ready 134s, download_done 154s, arm_base_FAILED OOM 21.69/22.03 GiB, arm_uno_FAILED process group twice). Every number the kid committed reproduces from the live job. Five probes recorded above, one per conjunct: wire (job real), wire (the fit assertion REFUTED on the 22.03 GiB device), gate (success criterion absent, not fabricated), gate (no TPF/acceptance), auth (aliases clean; one public paper GPU model named).
(3) NEAR MISS: a parent that reads only the Agent Notes sees "install 154s, OOM, retry recipe" and would accept a summary. The DIFF shows two things the summary does not: (a) the second arm died of a process-group-poisoning driver bug, not of the claim, so the kid's "my runner cannot survive a failed arm" is a real self-reported defect; (b) the bench file lives at .agi/context/local-maxxing/bench/, not the repo-root bench/ the orders name. Both are recorded, neither changes the fit finding.
(4) DEVIATION: the file scope named "the hypothesis node", but the kid diff carries no hypothesis edit. That is correct, not a missed deliverable — the hypothesis is the target and belongs to the town, not the kid. The scratch job.log the node cites is correctly absent from the diff (scratch is not committed).

VERDICT KEPT: inconclusive_lean_disproved:55. The lean is earned: conjunct (2)'s own parenthetical ("16.38 + 0.70 GB bf16 fit 24 GB with an 8k KV") is refuted by direct measurement — OOM at 21.69 GiB during load_model, before any KV allocation, on the rental's actual 22.03 GiB device. The speed conjunct (3) and TPF conjunct (4) are unmeasured (0/20), so the round is not decided. The kid's UNVERIFIED caveat about the load-time peak mechanism (torch.set_default_device("cuda") materialising a shard) is exactly the right level of claim and I did not upgrade it. NOT ACCEPTED as proved and not demoted: no overclaim is present.
<!-- THOUGHT:END -->

PARENT REVIEW TM.36 (a00-59c581e7): ACCEPTED as inconclusive_lean_disproved:55, probes: added (5, one per conjunct; wire+wire+gate+gate+auth). Diff = 5 files +204 lines, all named deliverables present (cmds.md/prompts.jsonl/rows.jsonl/bench 20260918T134243Z/node). Independently re-verified job 27689 via camber job get/list/logs: real, with_gpu, XSMALL, 251 s wall, nothing RUNNING, install+download markers reproduce. Conjunct (2) fit assertion REFUTED (OOM 21.69/22.03 GiB pre-KV); conjuncts (3)/(4) unmeasured (0/20). No overclaim, no demotion. One self-reported defect: runner died of process-group poisoning so arm 2 never ran; retry recipe (per-arm subprocess, max_model_len 4096, expandable_segments, 0.9B fallback) needs ONE more Camber XS job line from the Prime.
