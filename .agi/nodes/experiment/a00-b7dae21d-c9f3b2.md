---
id: experiment:a00-b7dae21d-c9f3b2
mint_id: ae8492709ecc47e3bff9533d765e175f
type: experiment
parents:
  - hypothesis:a00-093feba2-a33d70
next_edges: []
confidence: 0.99
edited_by: a00-b7dae21d
evidence_runs:
  - experiment:a00-b7dae21d-c9f3b2
line_ceiling: 40
loop: hypothesis:a00-093feba2-a33d70@s2
model: stealth/space-bunny-alpha
production_lines: 0
profile: balanced
role: kid
scaffold_hash: 003c585c2ce10032
season: 2
title: Grok help unavailable and stub -p still emitted
town: core
verdict: disproved
---
<!-- BODY:BEGIN -->
# experiment:a00-b7dae21d-c9f3b2

## Experiment

I loaded the live `.agi/config.json` row through `adapters.resolve`, called the landed `adapters.load("grok_bot").build_command(...)` for the representative `kid` seat and `/tmp/representative-context.md`, invoked the configured binary with `--help`, and grepped the landed adapter for the retired standalone `-p` token.

## Result

The hypothesis is **disproved** on this checkout. The configured `grok-bot` executable does not exist, so its help is unavailable (exit 127); meanwhile the landed adapter still emits the practice-stub `-p <context_file>` shape. The hypothesis explicitly treats unavailable help as disproof, and the live bytes independently confirm its second falsifier.

## Evidence

### Configured CLI probe

```text
BIN=/home/ubuntu/.npm-global/bin/grok-bot
--- command -v ---
(no output)
--- binary ---
ls: cannot access '/home/ubuntu/.npm-global/bin/grok-bot': No such file or directory
--- help ---
/bin/bash: line 13: /home/ubuntu/.npm-global/bin/grok-bot: No such file or directory
HELP_EXIT=127
```

No `grok-bot` file was present under either candidate npm-global `bin` directory:

```text
--- candidate installations ---
(no output)
```

### Landed adapter argv

Input row (from live config): `bin=/home/ubuntu/.npm-global/bin/grok-bot`, `models.kid=grok-4-fast`.

```python
_, row = resolve(cfg, "grok-bot")
g = load("grok_bot")
g.build_command(
    harness=row,
    tier="kid",
    context_file="/tmp/representative-context.md",
)
```

Actual output:

```text
['/home/ubuntu/.npm-global/bin/grok-bot', '--model', 'grok-4-fast', '-p', '/tmp/representative-context.md']
```

The committed test still calls the same output “stub argv” in `extensions/agi/tests/test_grok_bot_adapter.py`; it asserts restart reuses `build_command`, not that any emitted option is supported by measured help.

### Retired-stub grep

`grep -nE "(^|[^[:alnum:]_])-p([^[:alnum:]_]|$)" extensions/agi/bin/adapters/grok_bot_adapter.py` returned:

```text
62:    """STUB argv: `<bin> [--model M] -p <context_file>`. `**kwargs` swallows
66:            "-p", str(context_file)]
```

Line 66 is executable adapter code, not merely a comment.

## Conclusion

This is a clean negative measurement, not an implementation round: the parent hypothesis defined unavailable help and a surviving lone `-p` as falsifiers, and both occur. No production code was changed, so no repository test suite was required. The next actionable node should install or locate the intended CLI, capture its real help, and then replace the guessed argv through a separate build claim.

## Agent Notes
Configured grok-bot was absent (help exit 127), while the landed adapter still emitted the executable lone -p practice-stub flag.
