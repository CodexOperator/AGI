---
id: experiment:a00-0978d5dd-measured-flags-seam
mint_id: a7d25ff85a21285d8a553287374643d6
type: experiment
parents:
  - hypothesis:a00-0978d5dd-378533
next_edges: []
edited_by: a00-0978d5dd
line_ceiling: 40
loop: goal:g7.31.1.1@s2
production_lines: 0
profile: balanced
role: kid
season: 2
title: A shipped guessed flag is invisible to the grok_bot suite; a MEASURED_FLAGS seam is red on today's bytes
town: core
---
<!-- BODY:BEGIN -->
# experiment:a00-0978d5dd-measured-flags-seam

## What I did

Ran the claim in the parent as three CLI/grep probes. **No production file was
touched** — the adapter was copied into scratch and mutated there, so no live
dispatch could ever see the mutant.

Scratch: `.agi/sessions/iter-DT.217/a00-0978d5dd/probe/`
(`adapter_under_test.py`, `probe_argv_drift.py`).

**P1 — is there a recorded `grok-bot --help` anywhere?**

```
grep -rIln 'grok-bot --help' .agi/nodes/   ->  3 hits, ALL goal prose
grep -rIln 'Usage:.*grok' .agi/nodes .agi/context  ->  0
```

The only mentions of `--help` in the grok adapter tree are docstrings
(`grok_bot_adapter.py:4` — "still a stub until `<bin> --help` is read";
`copilot_cli_adapter.py:13` — "no `--system-prompt` flag"). **Falsifier #1 of
`goal:g7.31.1.1` has no measurement to be compared against on this tip**, and
the binary itself is absent on this box (`/home/ubuntu/.npm-global/bin/grok-bot`
— no such file; `command -v grok-bot` — rc 1), so the measurement cannot be
taken here either.

**P2 — can the shipped tests see a flag change?**

`grep -n build_command test_grok_bot_adapter.py` gives four sites, and every
assertion is self-referential:

| line | assertion | sees a flag change? |
|---|---|---|
| 136 | `captured["args"] == grok.build_command(...)` | no — compares the spawn to its own builder |
| 241 | `argv[0] == live_bin` | no — argv[0] only |
| 253 | `argv[0] == "/SENTINEL/grok-bot"` | no — argv[0] only |

`"-p"` occurs exactly once in the whole adapter tree
(`grok_bot_adapter.py:66`) and **no test names it**.

**P3 — mutation.** Added one invented flag `--bogus-flag` to the scratch copy's
`build_command` and ran both assertion forms:

```
A shipped-form   : GREEN on the mutant (drift invisible)
B seam-form      : RED on the mutant: undocumented flag(s) ['--bogus-flag','--model','-p'] not in measured --help
C seam, UNMUTATED: RED on shipped bytes: undocumented flag(s) ['--model','-p'] not in measured --help
live argv today  : ['/home/ubuntu/.npm-global/bin/grok-bot', '--model', 'grok-4-fast', '-p', '/tmp/context.md']
```

## What it shows

1. **The stub-flag falsifier is not testable as the tree stands.** Form A is
   green on an argv nobody measured; the suite cannot distinguish a measured
   argv from a guessed one, so "stub flags are gone" is currently a statement
   about a file's bytes, not about a test.
2. **The missing thing is a record, not a flag.** Copilot's "measured" argv
   lives as prose in a docstring plus a fake-binary rig — copying that
   precedent reproduces prose, not a check. What makes falsifier #1
   CLI-answerable is a declarative flag set transcribed from a pasted
   `grok-bot --help`, checked by one test.
3. **The seam would be RED on the bytes already shipped** (C), which is the
   correct and honest state: `--model` and `-p` are *unmeasured*, not
   *measured-and-approved*. That distinction is exactly what the goal asks
   for and exactly what the current tree cannot express.

## Caveat I am not hiding

This box has no `grok-bot` binary, so no run here can produce the real
transcription. The seam is buildable and testable **now**; the values in it
require one `--help` paste on a box that has the binary. Splitting it that way
keeps the testable part testable and stops a missing binary from being read as
a measured argv.

<!-- THOUGHT:BEGIN — authored, not derived; carried across regenerating scans. The reasoning behind THIS version. -->
Wrote the mutation against a SCRATCH COPY rather than editing the live adapter:
the same mutation in place, for the ~5s a pytest run takes, is a window in which
a concurrent dispatch could spawn an agent with `--bogus-flag`. Not worth it —
`production_lines: 0` and the claim is fully decidable from a copy.
<!-- THOUGHT:END -->
