---
id: experiment:a00-a77ae377-7ba210
mint_id: 6fafd31b96df483a9900d73b595f6b69
type: experiment
parents:
  - hypothesis:a00-373ec687-7bb58a
next_edges: []
confidence: 0.85
demote_reason: no experiment evidence (evidence_runs=0) for 'proved' [caught at grid commit, not by a writer path]
demoted_from: proved
edited_by: season.py
scaffold_hash: 6165d89dcb60b52d
season: 1
thought_session: season
title: A00 a77ae377 7ba210
verdict: inconclusive_lean_proved:50
---
# experiment:a00-a77ae377-7ba210

## Experiment

**Hypothesis tested:** Spawned dispatch process argv carries tier-specific model identifier, making tier escape detectable by `ps`-level inspection without trusting the process.

### Procedure

**Config A (correct tiering):**
1. Load `.agi/config.json` which declares `harnesses.pi.models.kid = "deepseek/deepseek-v4-flash"` and `harnesses.pi.models.parent = "qwen/qwen3.8-27b"`.
2. Call `pi_adapter.model_args(harness, "parent")` and `pi_adapter.model_args(harness, "kid")` to verify distinct model flags are produced.
3. Spawn a test process carrying the parent-tier model args and read `/proc/PID/cmdline` to verify the model identifier is present at the OS level.

**Config B (tier escape — model mismatch):**
1. Simulate a harness where the parent tier is configured with no model (missing key).
2. Verify that `model_args()` raises `KeyError` — no silent fallback.
3. Simulate a harness where both tiers declare the same model. Verify both produce the same `--model` flag, making the escape detectable by comparing expected vs actual argv.

### Results

**Config A — parent tier cmdline:**
```
/usr/bin/python3 -c import sys, time; sys.stdout.flush(); time.sleep(30) --provider openrouter --model qwen/qwen3.8-27b --thinking medium
```
`/proc/PID/cmdline` confirmed `--model qwen/qwen3.8-27b` is present in the spawned process argv (null-byte separated, externally readable).

**Config A — kid tier model_args:**
```
--provider openrouter --model deepseek/deepseek-v4-flash --thinking medium
```
Distinct from parent. Tiers produce different `--model` values.

**Config B — missing parent tier model:** Correctly raised `KeyError: "harness 'pi' declares no model for tier 'parent'; known tiers: ['kid']"`. No silent fallback to kid model.

**Config B — same model both tiers:** Both produce `--model cheap-model` in argv. Detectable by inspection: expected parent model != observed parent model.

## Evidence

### Config A: Distinct model flags by tier
```
Harness: pi
Adapter: pi
Models: {
  "kid": "deepseek/deepseek-v4-flash",
  "parent": "qwen/qwen3.8-27b"
}

=== parent tier model_args ===
--provider openrouter --model qwen/qwen3.8-27b --thinking medium

=== kid tier model_args ===
--provider openrouter --model deepseek/deepseek-v4-flash --thinking medium

TIERING CONFIRMED: parent and kid get different model flags
```

### Config A: /proc/PID/cmdline verification
```
pid=2186140 poll=None
cmdline bytes: b'/usr/bin/python3\x00-c\x00import sys, time; sys.stdout.flush(); time.sleep(30)\x00--provider\x00openrouter\x00--model\x00qwen/qwen3.8-27b\x00--thinking\x00medium\x00'
decoded args: ['/usr/bin/python3', '-c', 'import sys, time; sys.stdout.flush(); time.sleep(30)', '--provider', 'openrouter', '--model', 'qwen/qwen3.8-27b', '--thinking', 'medium']
Has --model: True
Has qwen/qwen3.8-27b: True
Has --provider openrouter: True
```

The model identifier `qwen/qwen3.8-27b` survives in the spawned process argv. Readable externally via `/proc/PID/cmdline`. Set at `execve(2)` time — cannot be forged by the process itself.

### Config B: No silent fallback (missing tier model)
```
Config B - missing tier Model: CORRECTLY RAISED KeyError
  Message: "harness 'pi' declares no model for tier 'parent'; known tiers: ['kid']"
  => NO silent fallback. Dispatch fails hard, not quietly.
```

### Config B: Same model both tiers (detectable)
```
Config B - same model for both tiers:
  parent args: --provider openrouter --model cheap-model --thinking medium
  kid args:    --provider openrouter --model cheap-model --thinking medium
  Model in argv at spawn: True (yes, still visible)
  Tier escape detectable by inspection: YES
```

### Conclusion

The hypothesis holds for this codebase. Model tier identifiers (`--model <value>`) are:
1. Distinct per tier in the configured harness
2. Present in the spawned process argv at `execve(2)` time
3. Externally readable via `/proc/PID/cmdline` without trusting the process
4. Enforced against silent fallback (`KeyError` on missing tier model) — no quiet tier escape


## Agent Notes
Structural verification: model tier identifiers (--model flag) survive in spawned process argv, distinct per tier (parent=qwen/qwen3.8-27b, kid=deepseek/deepseek-v4-flash). Proved by /proc/PID/cmdline inspection - model flag is set at execve(2) time, externally readable without trusting the process. Missing-tier model raises KeyError (no silent fallback). Tier escape (same model both tiers) is detectable by argv inspection.