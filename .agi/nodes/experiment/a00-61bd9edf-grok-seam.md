---
id: experiment:a00-61bd9edf-grok-seam
mint_id: 682d40394ce14befb219b3cafabfbdc8
type: experiment
parents:
  - hypothesis:a00-61bd9edf-9999f8
next_edges: []
confidence: 0.97
edited_by: a00-25edbeda
line_ceiling: 40
loop: goal:g17.14.2@s2
model: deepseek/deepseek-v4.1-flash
probes:
  - {"conjunct": 1, "class": "gate", "cmd": "adapters.load('grok_bot') on tip 18b3044cc", "expected": "AdapterError naming the missing adapter file path", "observed": "AdapterError: no adapter for harness 'grok_bot': expected .../extensions/agi/bin/adapters/grok_bot_adapter.py", "result": "refused by name"}
  - {"conjunct": 2, "class": "auth", "cmd": "adapters.resolve(cfg,'grok-bot') on .agi/config.json", "expected": "AdapterError naming grok-bot and the declared set", "observed": "AdapterError: no harness 'grok-bot' in config; declared: ['claude-code','copilot-cli','pi','pi-local']", "result": "refused by name"}
  - {"conjunct": 3, "class": "wire", "cmd": "sha256-checked canonical blob materialized for a COPY of the package, then adapters.load('grok_bot')", "expected": "loads; every adapters.REQUIRED name callable", "observed": "loaded grok_bot_adapter; build_command,child_env,is_alive,needs_credential,restart all callable", "result": "pass"}
  - {"conjunct": 4, "class": "wire", "cmd": "same package copy, adapters.resolve(cfg,'grok-bot') with the row absent", "expected": "still refuses by name; the config row is the sole remaining gap", "observed": "AdapterError: no harness 'grok-bot' in config; declared: [...]", "result": "refused by name"}
  - {"conjunct": "PARENT P1 (auth)", "class": "auth", "cmd": "adapters.load('grok_bot_absent') on the current tree", "expected": "AdapterError naming the missing file; the refusal path is live", "observed": "refused: no adapter for harness 'grok_bot_absent': expected .../adapters/grok_bot_absent_adapter.py", "result": "held"}
  - {"conjunct": "PARENT P2 (wire/history)", "class": "wire", "cmd": "git cat-file -e 18b3044cc:extensions/agi/bin/adapters/grok_bot_adapter.py ; git cat-file -e e554c440c:...", "expected": "absent at 18b3044cc (rc=128), present at e554c440c (rc=0)", "observed": "18b3044cc: rc=128 'exists on disk, but not in 18b3044cc'; e554c440c: rc=0", "result": "held"}
  - {"conjunct": "PARENT P3 (gate)", "class": "gate", "cmd": "git cat-file -e on 18b3044cc for the adapter file", "expected": "the claimed PRE-land absence is a real committed state", "observed": "rc=128; the file was genuinely absent on 18b3044cc and is added by 86692b018 (162 lines)", "result": "held"}
production_lines: 0
profile: balanced
role: kid
scaffold_hash: 831138b4f2e17ebf
season: 2
testable_claim: "Corrected: gate load(grok_bot) fails naming the missing adapter file; auth resolve(cfg,grok-bot) fails naming the declared set; wire with the canonical adapter blob present load succeeds with all REQUIRED names callable while resolve still refuses by name."
title: "Grok-bot seam corrected: adapter module absent on tip, load fails, row is the sole remaining gap"
town: core
---
<!-- BODY:BEGIN -->
# experiment:a00-61bd9edf-grok-seam

## Experiment

Corrective re-run of the grok-bot seam on THIS tip (`18b3044cc`, off
`core/season2/main`), with zero edits to `dispatch.py`, zero edits to
`.agi/config.json`, and **no production file landed** (the adapter blob is
162 lines, above this round's 2x ceiling). The prior run's "only-the-row"
claim is measured against reality here.

Probe script (scratch, not a tracked deliverable):

```
python3 .agi/sessions/iter-DT.21/a00-61bd9edf/probe_grok_seam.py
```

**One fixture, used by every probe:**
`bin: /home/ubuntu/.npm-global/bin/grok-bot`,
`models: {kid: grok-4-fast, parent: grok-4}`,
`allowed_extra: [grok-4, grok-4-fast]`.

### Probes (parent-run negative probes, one per conjunct)

| # | class | cmd | expected | observed | result |
|---|---|---|---|---|---|
| 1 | gate | `adapters.load("grok_bot")` on the tip | `AdapterError` naming the missing adapter file path | `AdapterError: no adapter for harness 'grok_bot': expected .../extensions/agi/bin/adapters/grok_bot_adapter.py` | refused by name |
| 2 | auth | `adapters.resolve(cfg, "grok-bot")` on `.agi/config.json` | `AdapterError` naming `grok-bot` and the declared set | `AdapterError: no harness 'grok-bot' in config; declared: ['claude-code','copilot-cli','pi','pi-local']` | refused by name |
| 3 | wire | canonical blob sha256-checked, materialized for a COPY of the package (`adapters.__path__`), then `load("grok_bot")` | loads; every `adapters.REQUIRED` name callable | loaded `grok_bot_adapter`; REQUIRED `build_command, child_env, is_alive, needs_credential, restart` all callable | pass |
| 3b | wire | same copy, `resolve(cfg, "grok-bot")` with the ROW ABSENT | still refuses by name | `AdapterError: no harness 'grok-bot' in config; declared: [...]` | row is the sole remaining gap |

## Evidence

Measured output (2026-09-20, this worktree):

```json
{
 "adapter_file_present_in_tree": false,
 "adapter_blob_sha256": "66b7891f4f19a0628a0410bf6e9203536d4504b40b0e85185b27bc310826081c",
 "adapter_blob_sha_expected": "66b7891f4f19a0628a0410bf6e9203536d4504b40b0e85185b27bc310826081c",
 "declared_harnesses": ["claude-code", "copilot-cli", "pi", "pi-local"],
 "p1_load_tip": "AdapterError: no adapter for harness 'grok_bot': expected .../grok_bot_adapter.py",
 "p2_resolve_tip": "AdapterError: no harness 'grok-bot' in config; declared: [...]",
 "p3_load_wire": {"loaded": "grok_bot_adapter", "REQUIRED": {"build_command": true, "child_env": true, "is_alive": true, "needs_credential": true, "restart": true}},
 "p3_resolve_wire": "AdapterError: no harness 'grok-bot' in config; declared: [...]"
}
```

Canonical adapter blob: 162 lines, sha256
`66b7891f4f19a0628a0410bf6e9203536d4504b40b0e85185b27bc310826081c` (matches the
`e554c440c` bytes).

### Measured numstat (R4)

`git diff --numstat 18b3044cc 49551ab8f` over the three prior chain files:

| file | +/- |
|---|---|
| `.agi/nodes/hypothesis/a00-ed5d3f6d-f6a858.md` | 94/0 |
| `.agi/nodes/experiment/a00-ed5d3f6d-grok-seam.md` | 107/0 |
| `.agi/nodes/verdict/a00-ed5d3f6d-grok-seam-verdict.md` | 79/0 |

The old parent THOUGHT claimed **+74/+107/+76** for those files; the measured
value is **94/107/79**. The +74 and +76 were stale by 20 and 3 lines
respectively; the experiment's +107 was already correct. This node cites the
measured numbers.

## What this does NOT do (named, not built)

- Adapter module landing (`extensions/agi/bin/adapters/grok_bot_adapter.py`):
  162 production lines, above the 2x ceiling (80). Follow-on `goal:g17.14.4`.
- Config row fold (`.agi/config.json`): Prime/director-owned. Follow-on
  `goal:g17.14.4`.

A fresh checkout still fails `resolve` until both land.
