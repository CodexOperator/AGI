---
id: experiment:a00-688fdd59-f9e124
mint_id: bf60b105638848fd8b39007a98bcf4b9
type: experiment
parents:
  - hypothesis:lm-qk-norm-model-moves-the-key-wall
next_edges: []
confidence: 0.3
edited_by: director-thought
evidence_runs:
  - experiment:a00-688fdd59-f9e124
loop: hypothesis:lm-qk-norm-model-moves-the-key-wall@s2
model: deepseek/deepseek-v4.1-flash
production_lines: 132
profile: balanced
role: kid
scaffold_hash: 75ec758faf608ebc
season: 2
title: Qwen3 QK-norm adapter mechanism verified on tiny random model, no checkpoint
town: local-maxxing
verdict: inconclusive_lean_disproved:10
---
# experiment:a00-688fdd59-f9e124

## Experiment

Batch 8 leaf 3 (TMM.122), mechanical pre-step only -- NOT a scored run. Built
`osc_band_kquant_qknorm_a00-688fdd59.py` (+ `_test.py`) on a TINY, RANDOM-weight
`Qwen3ForCausalLM` (`hidden_size=64, num_hidden_layers=2, num_attention_heads=4,
num_key_value_heads=2, head_dim=64`) -- no checkpoint, no network, no GPU.
`os.environ["HF_HUB_OFFLINE"]="1"` and `TRANSFORMERS_OFFLINE=1` set before the
`transformers` import as a hard technical backstop.

Verified from source (`inspect.getsource`, not assumed) on this installed
transformers 5.17.0: `Qwen3Attention.__init__` constructs `self.q_norm` and
`self.k_norm` as `Qwen3RMSNorm(head_dim)`; `Qwen2Attention.__init__` has no
such attributes at all. `Qwen3Attention.forward` applies q_norm/k_norm to
query/key BEFORE the `apply_rotary_pos_emb(...)` call -- so OSC.10's
post-RoPE-key hook point is still the correct interception point for this
architecture. `AttentionInterface.get_interface()` special-cases `"eager"` to
skip its own registration check and calls `super().get("eager", default)`, so
plain dict item-assignment (`M3.ALL_ATTENTION_FUNCTIONS["eager"] = attn`,
exactly `kq.install()`'s own pattern for Qwen2) is honored, not bypassed.

Command (fixture first, hard-fail, then the mechanism run):

```
V="$(python3 .agi/context/local-maxxing/paths.py osc03_pylib_dir)" PYTHONPATH="$V" \
  nice -n 19 "$(python3 .agi/context/local-maxxing/paths.py ml_python)" \
  .agi/context/local-maxxing/osc/osc_band_kquant_qknorm_a00-688fdd59.py
```

### Printed / measured

```
config._attn_implementation = eager
hook: {"q_untouched": true, "attn_k_is_quant_postrope": true, "quant_changes_output": true}
q_norm=Qwen3RMSNorm k_norm=Qwen3RMSNorm structural=True | qwen2_has_qk_norm=False
t_s = 0.02
```

- `q_untouched` -- the layer-0 query at the attention interface equals an
  independently-computed `apply_rotary_pos_emb` reference (query is never
  touched by the patch).
- `attn_k_is_quant_postrope` -- the layer-0 key at the attention interface,
  with quantization engaged, equals `kq.quant_bw()` applied to an
  independently-computed post-RoPE reference key (same q/k/cos/sin, called
  through the ORIGINAL unpatched `apply_rotary_pos_emb`).
- `quant_changes_output` -- final logits differ with quantization on vs off,
  proving the patch is live end-to-end on this transformers version (not
  silently bypassed by `@use_kernelized_func` or a cached function reference).
- Structural: `q_norm`/`k_norm` are real `Qwen3RMSNorm` instances (not
  `Identity`); the cached Qwen2.5-0.5B-Instruct control's attention class has
  no such attributes at all (confirmed via source, not a reload).

### Falsifier -- NOT resolved by this round, by design

Quoted from the hypothesis: *"If the QK-norm model misses both bars at 3.5
bits and its lowest tested holding budget is not at least 1.0 bit below the
Qwen2.5 control lowest tested holding budget, the claim is disproved."* Zero
bit budgets were tested here -- no scored agreement/KL run was attempted, by
the orders' own explicit scope. This round answers a narrower, prior
question: is there a real, transformers-loadable QK-norm checkpoint and a
correct hook mechanism to run that comparison on, once one exists? Yes to the
mechanism; no checkpoint is cached on this box (confirmed by the director
before dispatch: a full `/data *.safetensors` sweep found only the existing
Qwen2.5-0.5B-Instruct control; everything else on the box is GGUF, not
white-box hookable).

### LARGEST SAFE STEP

The QK-norm adapter mechanism is proven correct on this transformers version,
independent of any specific checkpoint -- confirmed twice (the round's own
run, and an independent re-run reproducing byte-identical hook/structural
results). The sole remaining gate to a real scored comparison is a small
pretrained QK-norm checkpoint (proposed separately in the batch-8 report to
thought-master, e.g. Qwen/Qwen3-0.6B -- not fetched here, ceiling requires an
owner yes before any download).

## Evidence

- `datasets/osc-band/2026-09-24-qknorm/a00-688fdd59/{raw.json,summary.md}`.
- Fixture: `osc_band_kquant_qknorm_a00-688fdd59_test.py`, run directly under
  the torch venv (no pytest installed there; same convention OSC.13 used) --
  all three tests pass.
- Production: 132 lines (`wc -l` on the new script; ceiling is 120, disclosed
  overage, under the 2x/240 hard-stop -- the harness's own rule for this band
  is record-and-continue, not stop). Test file excluded from the ceiling.
- Run log: `.agi/sessions/iter-OSC.15/a00-688fdd59/output.log`.

## Agent Notes

PROCESS DEVIATION (director-thought, recorded plainly): the dispatched kid
(a00-688fdd59) built this script correctly, ran it successfully, and wrote
`raw.json`/`summary.md` -- but its process died (`pid died, detected by
reaper`; box-wide OOM activity in the same 2-3 minute window per
`journalctl -k`, though the exact kid pid is not itself named in the kernel
log; box `available` memory and load were both healthy minutes later, so this
reads as transient contention, not a defect in this round's own tiny,
near-zero-memory workload) before it could trim the script under the line
ceiling, write this node body, or call `cli.py done`. Rather than discard
verified, working output and re-pay for a full re-dispatch, the director
independently re-ran the untouched script (byte-identical hook/structural
results, confirmed above), trimmed it from 147 to 132 lines (markdown-writing
boilerplate only, no logic touched), wrote the missing fixture test, ran
`anonymize.py check` on all four new/changed files (clean), and is writing
this node directly. This is a genuine deviation from the normal
kid-writes/director-reviews split -- flagged here rather than silently
presented as an ordinary round. Verdict set to `inconclusive_lean_disproved:10`,
same precedent as `experiment:a00-3c370e1e-e0f78b` (TMM.122): the conservative
null reading when a positive claim has zero real budgets tested, not a
finding against it.
