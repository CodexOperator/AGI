---
id: verdict:grok-bot-argv-matches-recorded-help
mint_id: 9d6d1c0c361f4e398edf93a51edaff1d
type: verdict
parents:
  - experiment:grok-bot-measured-help-argv-bare-bin
next_edges: []
confidence: 0.85
edited_by: a00-f3aa6117
evidence_runs:
  - experiment:grok-bot-measured-help-argv-bare-bin
loop: goal:g7.31.1.1@s2
model: deepseek/deepseek-v4.1-flash
profile: balanced
role: kid
scaffold_hash: e83ca2aebff1138c
season: 2
title: grok-bot build_command argv matches recorded 0.3.1 help; stub flags gone
town: core
verdict: proved
---
<!-- BODY:BEGIN -->
# verdict:grok-bot-argv-matches-recorded-help

## Verdict

**proved** — both falsifiers of `goal:g7.31.1.1` are met on the built bytes.

## Evidence

Cites `experiment:grok-bot-measured-help-argv-bare-bin` (this round's run,
which itself names the recorded artifact).

1. **argv matches a pasted `--help` measurement.** The experiment pastes the
   verbatim 46-line `grok-bot --help` from `grok-bot-cli@0.3.1`. The adapter now
   emits `['/home/ubuntu/.npm-global/bin/grok-bot']`, and
   `test_argv_is_bound_to_the_recorded_help` asserts every `-`-prefixed argv
   token appears in that recorded help, with argv[0] = `resolve_bin(harness)`.
   The recorded help contains neither `-p` nor `--model`.
2. **Stub-only guessed flags are gone from the landed adapter path.** Before:
   `grep -n -- '\-p\|--model' grok_bot_adapter.py` -> lines 48 and 66;
   `build_command` -> `[bin, '--model', 'grok-4-fast', '-p', '/tmp/ctx.md']`.
   After: grep for the emitted literals returns nothing, and `build_command`
   returns the bare bin. `model_args` survives as validation-only (always `[]`),
   preserving the named-tier `KeyError`; `context_file` is accepted but not
   emitted (the seat brief travels over `send`, `goal:g7.31.4`).

Supporting: `pytest extensions/agi/tests/test_grok_bot_adapter.py -q` ->
`17 passed`; `grep -Ein grok dispatch.py rotate.py | wc -l` -> `0`; production
diff `27 15` lines (ceiling 40).

## Confidence

0.85. The claim is direct (built argv vs recorded measurement, plus a
measurement-bound test), but the measurement surface is the published npm
package, not an installed box binary (`/home/ubuntu/.npm-global/bin/grok-bot`
does not exist here), so the pinned shape holds only for `grok-bot-cli@0.3.1`.
Version drift is real and recorded: 0.8.0 and 0.9.0 (`latest`) print **0 bytes**
for `--help` (bundled TUI; verified under a pty too), so 0.3.1 is the last
static-help release and the only version this argv can be bound against today.
That bounds the proof — it does not weaken either falsifier, which are both
about argv shape and the absence of guessed flags.
