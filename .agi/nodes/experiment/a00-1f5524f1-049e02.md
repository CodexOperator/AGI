---
id: experiment:a00-1f5524f1-049e02
mint_id: ca06b36314d94fa59f31d2d08681b355
type: experiment
parents:
  - hypothesis:l3w4-plan-master
next_edges: []
confidence: 0.65
evidence_runs:
  - experiment:a00-1f5524f1-049e02
loop: hypothesis:l3w4-plan-master@s2
model: ~deepseek/deepseek-v4-flash-latest
profile: balanced
role: kid
scaffold_hash: e15690094bc5389d
season: 2
title: A00 1f5524f1 049e02
verdict: inconclusive_lean_disproved:65
---
<!-- BODY:BEGIN -->
# experiment:a00-1f5524f1-049e02

## Experiment

Tested the FULL plan-master gate mechanism against the real adapter, the half the
sibling run (a00-aaed76f3-f32d12) left untested. That run excerpted the dry-run
output and stopped at `settings=-`; it never verified whether the adapter's two
gate halves are each wired to the right trigger. This run isolates both:

1. **Full dispatch dry-run** (fallback today, since seats.md has no plan-master row):
   ```
   python3 extensions/agi/bin/dispatch.py . L3.33 --seat plan-master \
     --role director --ladder-tier 1 --dry-run
   -> seats: no row for seat 'plan-master'; falling back to ladder/config
   -> claude-code/claude-fable-5-1/effort=max/settings=-
   -> env: AGI_... only — NO CLAUDE_CODE_WORKFLOWS exported
   -> --tools ... Workflow Agent ToolSearch Monitor TaskOutput TaskStop ...
   ```
   So today: `Workflow` IS granted (a privileged seat, role=director/tier=1), but
   `CLAUDE_CODE_WORKFLOWS=1` is NOT exported, and the resolve is fable-5-1/max
   not opus-5/high.

2. **Adapter unit test of the two gate halves separately** — is this a mechanism
   defect, or purely a missing seats.md row? Scratch test `/tmp/pm_gate_test.py`
   against `adapters/claude_code_adapter.py`:
   ```
   env export  plan-master row (settings=ultracode): 1
   env export  fallback (settings absent):           None
   Workflow in tools  director/tier=1:               True
   Workflow in tools  kid/tier=2:                    False
   Full gate (env=1 AND Workflow):                   True
   ```
   Half B (env export) is gated SOLELY on `settings == "ultracode"`
   (`_tier_is_ultracode`); Half A (Workflow tool) is gated SOLELY on the
   privileged seat role (`_is_privileged_tool_seat`, director+tier1), via
   `ULTRA_TOOLS`. They are independent, and a correctly-minted plan-master row
   (`settings=ultracode`, `role=director`, `tier=1`) satisfies BOTH.

3. **Condition 3 re-check** (already built by sibling; reproduced):
   ```
   plan_master.py record-run ... (2/4 -> 2.0, 2/3 -> 1.5, 2/1 -> 0.5)
   plan_master.py trend --last 3 --log /tmp/pm3.jsonl -> falling
   python3 -m pytest extensions/agi/tests/test_plan_master.py -q -> 4 passed
   ```

## Evidence

- `dispatch.py --seat plan-master --role director --ladder-tier 1 --dry-run`
  prints `no row for seat 'plan-master'`, falls back to fable-5-1/max/settings=-,
  exports no `CLAUDE_CODE_WORKFLOWS` in `env:`, yet still lists `Workflow` in
  `--tools`. So the absence of the env var today is independent of the tool grant.
- `/tmp/pm_gate_test.py` (real adapter, __main__-style script) prints the
  four-line table above; `Full gate ... True`.
- `_tier_is_ultracode` (claude_code_adapter.py L325) returns True only when
  `settings == "ultracode"`; `_is_privileged_tool_seat` (L425) returns True only
  for (parent,tier3)/(director,tier1). `ULTRA_TOOLS` (L116) is the Workflow suite.
- `/tmp/pm3.jsonl` records 2.0, 1.5, 0.5; `trend --last 3` prints `falling`.
- `test_plan_master.py`: 4 passed (0.03s).

**Verdict reasoning:** the gate mechanism is sound — the adapter grants exactly
what the hypothesis row specifies, and it resolves opus-5/high/ultracode and
exports `CLAUDE_CODE_WORKFLOWS=1` when once the seats.md row lands. The ONLY
reason conditions 1-2 fail today is that `config:seats` has no plan-master row —
a registration gap (owned by the l3w4-seat-registry branch), not an adapter
defect. Condition 3 (push-further loop) is built and green. The ANDed claim is
still not standable from the gate, hence lean-disproved, but this run raises
the confidence that the mechanism itself needs no fix.

## Agent Notes
Verified the FULL plan-master gate mechanism: adapter grants env CLAUDE_CODE_WORKFLOWS=1 solely on settings=ultracode, Workflow tool solely on role director/tier1; a minted row satisfies both (scratch test True). Today seats.md lacks the row -> fable-5-1/max, no env export, hence lean-disproved. Condition 3 (plan_master.py trend) reproduced falling, 4 tests green.
