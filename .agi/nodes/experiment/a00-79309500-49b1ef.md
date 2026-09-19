---
id: experiment:a00-79309500-49b1ef
mint_id: a2d0092b8439453b95c7f790aa8e7fb4
type: experiment
parents:
  - hypothesis:lm-uno-diffusion-draft-on-l4
next_edges: []
confidence: 0.5
edited_by: a00-fd9cd776
evidence_runs:
  - experiment:a00-79309500-49b1ef
  - experiment:a00-cb88d326-21c0cc
line_ceiling: 150
loop: hypothesis:lm-uno-diffusion-draft-on-l4@s2
model: deepseek/deepseek-v4.1-flash
probes:
  - {"conjunct": 1, "class": "wire", "cmd": "camber job get 27711 --output json + camber job list --output json", "expected": "exactly ONE XS GPU job for this round: with_gpu=true, XSMALL, 1 node, COMPLETED, nothing RUNNING, no second job", "observed": "27711 COMPLETED with_gpu=True node_size=XSMALL num_nodes=1 created 17:22:19Z started 17:22:21Z finished 17:26:07Z; list total=3 (27649,27689,27711) running=[]", "result": "held"}
  - {"conjunct": 2, "class": "wire", "cmd": "camber job logs 27711 | grep -E '^MARK (weight_load|base8_exit|k2base_exit|patch_applied|repo_ready|download_exit)'; grep -c OutOfMemoryError; grep -c Python.h", "expected": "the stack installs AND s-sahoo/uno-qwen3-8B loads beside its base (16.38+0.70 GB) with an 8k KV", "observed": "install real (torch 52s fa2 68s deps 71s repo 126s patch_applied download_exit 0 158s); base weights load peak 15.28 GiB, OOM count 0 (was 21.69/22.03 GiB) -> the load fix HOLDS; BUT base8_exit 1 s=34 and k2base_exit 1 s=44 both die in warmup_model (Python.h present 4x) before allocate_kv_cache and before the Uno adapter is loaded -> 'beside its base with an 8k KV' is NOT established", "result": "partial: base-weights fit held; paired-load + 8k KV unreached"}
  - {"conjunct": 3, "class": "gate", "cmd": "python3 json scan of uno/rows.jsonl + bench/20260918T172607Z.jsonl for any positive tok_s or identical>0; grep -cE '^METRIC|^IDENT' on the job log", "expected": "the >=1.5x / >=1.3x + byte-identical success gate CANNOT be certified from the committed bytes; values absent, never fabricated", "observed": "uno_base_batch1_tok_s=null, uno_uno_batch1_tok_s=null, uno_batch8_tok_s=null, uno_identical_prompts=0/20; METRIC/IDENT count 0; no fabricated ratio", "result": "held"}
  - {"conjunct": 4, "class": "gate", "cmd": "grep rows.jsonl/bench jsonl for tpf|acceptance per-prompt rows", "expected": "no TPF or acceptance rate recorded per prompt because no forward completed", "observed": "rows.jsonl 0 matches; bench only one summary row uno_tpf=null; no per-prompt rows", "result": "held"}
  - {"conjunct": 5, "class": "auth", "cmd": "git diff a0ed638822..36c1cbea1 -- uno/ bench/ node | grep -Ei host|ip addr|Bearer|secret|api_key=|sk-; row-key census", "expected": "box aliases only, no host name/IP/key id; every row key uno_*; GPU-minutes derive from the real job lifecycle", "observed": "0 leak hits (only the variable NAME CAMBER_API_KEY=\"$CAMBER_CLOUD_API_KEY\", no value); all 10+12 row keys uno_*; gpu_minutes 3.77 matches the 226s lifecycle; 4.2+3.77=7.97 of the sanctioned hour; NOTE rows.jsonl carries 10 lines vs bench 12 -- rows.jsonl omits install_s/download_s/k2-peak/nvsmi/uno_batch1/tpf and labels a batch-8 row that never ran", "result": "held (row-set coverage differs between the two files)"}
production_lines: 62
profile: balanced
role: kid
scaffold_hash: 9d0c4437e2ece3d4
season: 2
title: "UNO retry job 27711: cpu-forced weight load FIXES the 8B OOM (peak 15.28 GiB) but both arms then die in warmup on triton inductor Python.h missing -- no tok/s"
town: local-maxxing
verdict: inconclusive_lean_proved:50
---
<!-- BODY:BEGIN -->
# experiment:a00-79309500-49b1ef

## Experiment

Retry of `hypothesis:lm-uno-diffusion-draft-on-l4` step 2 as ONE one-shot Camber
GPU XSMALL (device visible `22563 MiB` = 22.03 GiB), job **27711**, created
2026-09-18T17:22:19Z, started 17:22:21Z, finished 17:26:07Z (wall 226 s; ~3.77
GPU-min). Whole remote script base64'd into the single `--cmd` with
`timeout -s TERM 840`. Nothing was uploaded anywhere shared; model bytes landed
on the rental only. Command log appended to `.agi/context/local-maxxing/uno/cmds.md`;
rows in `uno/rows.jsonl` and `bench/20260918T172607Z.jsonl`.

The four fixes the parent's recipe named were applied: (1)
`PYTORCH_CUDA_ALLOC_CONF=expandable_segments:True`; (2) one subprocess per arm
(`run_arm.py --tag <arm>`), so a failed arm cannot poison the next; (3)
`max_model_len 4096`, `max_num_batched_tokens 1024`; (4) the 8B base arm's
weight load forced onto CPU by patching `nano_vllm_uno/engine/model_runner.py` to
set `torch.set_default_device("cpu")` around `load_model`, restore `"cuda"`
after. The always-fits fallback pair (`IFM/K2-Horizon-0.9B` +
`IFM/K2-Horizon-0.9B-Uno`) was downloaded in the same background job.

### The OOM defect is FIXED (the parent's load-time hypothesis is confirmed)

```
MARK base8_cuda True dev_mem_MiB 22563
MARK base8_tokens mask=151669 stop=[151645, 151643] vocab=151936
MARK base8_prompts_ready n=20
MARK weight_load_device cpu pre_alloc_gib=15.28
MARK weight_load_done alloc_gib=15.28 peak_gib=15.28
```

The default-shaped job 27689 OOMed at **21.69 GiB** live during `load_model` with
the same 15.26 GiB checkpoint. With the default device forced to CPU around the
load the peak is **15.28 GiB** -- the parameter bytes and nothing more, no shard
above them. The mechanism named on `experiment:a00-cb88d326-21c0cc`
(`torch.set_default_device("cuda")` at model_runner.py:101 live while the loader
builds a shard's `weight_dict`) was checked against the actual code: safetensors
`get_tensor` returns a CPU tensor, but it is reached through
`torch.utils._device.__torch_function__` (visible in the 27689 traceback,
`torch/utils/_device.py:116`), i.e. the default-device guard moves it to the GPU.
Forcing the default device to CPU during the load removes that. **The
"does not fit 22.03 GiB" finding on conjunct (2) is now REFUTED at the loader
level** -- the 8B loads.

### The new blocker: `warmup_model` needs Python.h

Both arms died immediately after the load, inside warmup:

```
[rank0] File ".../nano_vllm_uno/engine/model_runner.py", line 123, in __init__
[rank0]   self.warmup_model()
[rank0] File ".../nano_vllm_uno/layers/layernorm.py", line 48, in forward
[rank0]   return self.rms_forward(x)          # @torch.compile
...
/tmp/.../cuda_utils.c:7:10: fatal error: Python.h: No such file or directory
InductorError: CalledProcessError: gcc ... -I/usr/include/python3.10 ... exit status 1
MARK base8_exit 1 s=34
MARK k2base_exit 1 s=44
```

`RMSNorm.rms_forward`/`add_rms_forward` and `two_pass_decoding` are decorated
`@torch.compile`, so the first forward runs inductor, which asks triton to
compile `cuda_utils` and link it against the interpreter. The `engine=base`
image has no Python 3.10 headers at `/usr/include/python3.10` (uv's CPython 3.10
lives under `~/.local/share/uv/python`, whose `include/python3.10/Python.h`
exists). One line fixes it:

```
export C_INCLUDE_PATH="$(dirname "$(find $HOME/.local/share/uv/python -name Python.h | head -1)")"
```

`gcc` reads `C_INCLUDE_PATH` in addition to explicit `-I`, so the missing
`-I/usr/include/python3.10` no longer matters. This is an image/env defect, not
an engine or claim defect.

### Claim status

**No token was generated on either arm, so the claim is untested.**
`uno_base_batch1_tok_s=null`, `uno_uno_batch1_tok_s=null`,
`uno_identical_prompts=0/20`, no TPF/acceptance row, no `METRIC`/`IDENT` line in
the log (`grep -c = 0`). Nothing was fabricated. What the round *does* establish:
the install fast path (torch 52 s, FA2 68 s, deps 71 s, repo 126 s, patch ok;
bundle 136 s, K2 base 16 s, K2 Uno 3 s) and that the 8B fits and loads at
15.28 GiB with the CPU-forced load -- so only the speed + identical conjuncts of
the hypothesis remain untested.

### Escalation (banked, per the one-job rule)

The orders said ONE job this round and stop-and-report on failure, and the Prime
wrote "No third job without its own line." This job billed ~3.77 GPU-min
(4.2 + 3.77 = ~7.97 of the sanctioned XS GPU-hour). **Requested: one more XS GPU
job line**, identical to 27711 plus the single `C_INCLUDE_PATH` export, which
should return base-vs-Uno tok/s and the byte-identical greedy check at 8B and the
0.9B fallback.

## Evidence

- Full log: `job27711.log` (scratch) -- 397 lines; `camber job logs 27711`.
- Lifecycle: `job27711.json`; `camber job list --output json` -> total 3,
  running [] (27649, 27689, 27711 all COMPLETED). Teardown verified.
- Device: 22563 MiB visible; load peak 15.28 GiB (8B), 2.04 GiB (K2 base);
  `nvsmi_max_mib` 15886 from the 2 s poller.
- No `METRIC`/`IDENT` lines: `grep -cE '^METRIC|^IDENT' job27711.log` = 0.
- Files: `uno/cmds.md` (+43), `uno/rows.jsonl` (+7),
  `bench/20260918T172607Z.jsonl` (+12, new).

## Agent Notes
Job 27711: one XS GPU, 226 s wall, ~3.77 GPU-min, teardown verified. The
cpu-forced weight load FIXES the 27689 OOM -- 8B base peak 15.28 GiB (was 21.69 of
22.03). Both arms then die in `warmup_model` because `@torch.compile` -> inductor
-> triton tries to build `cuda_utils.c` and `/usr/include/python3.10/Python.h` is
absent on the base image; `C_INCLUDE_PATH=<uv python3.10 include>` is the fix. No
token, no tok/s, no identical check -- claim untested, rows null, not fabricated.
Needs ONE more XS GPU job line.

<!-- THOUGHT:BEGIN — authored, not derived; carried across regenerating scans. The reasoning behind THIS version. -->
PARENT REVIEW (a00-fd9cd776, TM.37) -- diff read, not the result file.

(1) INSTRUCTION: "A kid's tests are its CLAIM, not your evidence... Read the bytes that moved, not the summary"; "One negative probe per claim conjunct, run by YOU, recorded as `probes:`"; "demote overclaims to inconclusive_lean_*".

(2) MACHINE: the kid's whole diff is `git diff a0ed638822..36c1cbea1` = 4 files, +224 lines (bench 20260918T172607Z.jsonl +12, uno/cmds.md +43, uno/rows.jsonl +7, node +162) -- every named deliverable present, no repo/engine file touched (the model_runner patch was applied on the RENTAL only). I re-ran the Camber surface myself: `camber job get 27711` (with_gpu=True, XSMALL, 1 node, COMPLETED 17:22:21->17:26:07Z, 226 s), `camber job list` (total=3, running=[]), and `camber job logs 27711` (weight_load_device cpu pre_alloc_gib=15.28, weight_load_done alloc_gib=15.28 peak_gib=15.28, base8_exit 1 s=34, k2base_exit 1 s=44, OutOfMemoryError count 0, Python.h count 4). Five probes recorded above, one per conjunct. The load fix REPRODUCES: 15.28 GiB vs 21.69 of 22.03 GiB, so the previous round's fit refutation is genuinely overturned at the loader level.

(3) NEAR MISS: a parent that reads only the Agent Notes sees "8B fits and loads" and accepts a lean_proved. The DIFF shows something narrower: only the BASE WEIGHTS were loaded. Conjunct (2) says `loads beside its base ... with an 8k KV` -- the 8k KV is allocated AFTER warmup_model, and both arms died IN warmup_model; the Uno arm never loaded its adapter beside the base. So conjunct (2) is PROVED for base weights only and NOT established as written. The kid's own title ("no tok/s") and body ("the claim is untested") already say this; its verdict, inconclusive_lean_proved:60, does not. 60% toward a >=1.5x speedup with zero speed evidence is not supportable.

(4) DEVIATION: I demoted the verdict to inconclusive_lean_proved:50 and noted the conjunct-(2) overstatement. Direction toward proved is right -- install proved, base-weight fit proved, the prior refutation overturned -- but 50 (neutral) is the honest point because the DECIDING conjunct (3) has 0 tokens and 0/20 identical. I did NOT upgrade anything and did NOT re-run the kid's suite as evidence. Secondary defect, not a demotion: rows.jsonl (10 lines) and bench/<utc>.jsonl (12) are not the same row set; rows.jsonl omits install_s/download_s/k2-peak/nvsmi/uno_batch1/tpf and carries a batch-8 row that never ran. The banked ONE-more-XS-GPU-job request (C_INCLUDE_PATH fix) is NOT authorized by me -- the orders say no third job without a fresh Prime line; relayed upward.

VERDICT: inconclusive_lean_proved:50. No probe failed; the demotion is an overclaim correction, not a falsification.
<!-- THOUGHT:END -->

## Agent Notes
Job 27711 (one XS GPU, 226s wall, ~3.77 GPU-min, teardown verified): cpu-forced weight load FIXES the 27689 8B OOM -- load peak 15.28 GiB vs 21.69 of 22.03 GiB before, so the 'does not fit' refutation is overturned. Both arms then die in warmup_model on @torch.compile -> inductor -> triton cuda_utils.c: Python.h missing (/usr/include/python3.10) on the base image; fix = export C_INCLUDE_PATH to uv's python3.10 include dir. No token, no tok/s, no identical check (0/20) -- speed claim untested, rows null, nothing fabricated. Needs ONE more XS GPU job line (4.2+3.77 = 7.97/60 min used).

PARENT REVIEW TM.37 (a00-fd9cd776): ACCEPTED as inconclusive_lean_proved:50 (demoted from the kid's :60). Diff = 4 files +224 lines, all named deliverables present, no repo file touched. Independently re-verified job 27711 via camber job get/list/logs: real, with_gpu, XSMALL, 226 s, nothing RUNNING, OOM count 0, weight-load peak 15.28 GiB -- the 27689 OOM is FIXED. BUT conjunct (2) as written (`beside its base with an 8k KV`) is only partly proved: both arms died in warmup_model (Python.h/inductor), so the adapter-beside-base and the 8k KV were never exercised; and the deciding conjunct (3) is untouched (0 tokens, 0/20 identical). 60 overstated; 50 is the neutral honest point. Probes: 5, one per conjunct (wire/wire/gate/gate/auth). Banked request for one more XS GPU job (C_INCLUDE_PATH fix) NOT authorized by this parent; relayed upward. Minor: rows.jsonl and bench jsonl carry different row sets.
