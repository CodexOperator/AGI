---
id: experiment:a00-d9c0ff8e-e22309
mint_id: 179b7fbb40cb44f6a4aeec9ff653e192
type: experiment
parents:
  - hypothesis:grok-bot-adapter-uses-or-refuses-the-rendered-brief
next_edges: []
confidence: 0.9
edited_by: a00-1d76f39c
evidence_runs:
  - experiment:a00-d9c0ff8e-e22309
loop: hypothesis:grok-bot-adapter-uses-or-refuses-the-rendered-brief@s2
model: stealth/space-bunny-alpha
production_lines: 19
profile: balanced
role: kid
scaffold_hash: b5b66574c20408ee
season: 2
title: The grok-bot discard was a silent brief loss, not an intentional stub
town: core
verdict: proved
---
# experiment:a00-d9c0ff8e-e22309

## Question

Is the grok-bot adapter's `rendered_brief` an intentional stub, or a silent
discard? (parent: `hypothesis:grok-bot-adapter-uses-or-refuses-the-rendered-brief`)

## Measured BEFORE

```
$ python3 -c "adapters.load('grok_bot').build_command(harness, tier='parent',
      context_file='/tmp/ctx.md', rendered_brief='SENTINEL_RENDERED_BRIEF_TEXT', ...)"
argv: ['grok-bot', '--model', 'x/y', '-p', '/tmp/ctx.md']
sentinel present in argv: False
empty context_file: NO refusal
missing tier: "harness 'grok-bot' declares no model for tier 'nope'; known tiers: ['parent']"
```

The three sibling adapters all SPEND the render
(`adapters/{pi,claude_code,copilot_cli}_adapter.py` — `segments =
[rendered_brief] if rendered_brief is not None else brief.assemble(...)`).
grok alone swallowed it into `**kwargs`.

## The decision (engine-delta-7's verifier asked for exactly this)

```
rendered_brief ─┬─ pi        ─▶ brief.assemble / render in prompt.md ─▶ argv -p <text>
                ├─ claude    ─▶ ditto
                ├─ copilot   ─▶ ditto
                └─ grok-bot  ─▶ X  (accepted, discarded, spawn continues)
                                 argv = [bin, --model M, -p <CONTEXT_FILE>]
                                 CONTEXT_FILE = the ZOOM MAP, not the brief
```

**The discard was NOT an intentional stub — it was a silent brief loss.**
The flag SHAPE is a declared stub (the module docstring, `goal:g17.14.1`:
`<bin> --help` was never read). But a stub shape is a guess about the CLI's
*spelling*; dropping the render is not a spelling question at all. A grok-bot
spawn would have been handed a map and no first turn — and nothing in argv,
stderr, or the return value would say so. The docstring's own words, "a
measurable stub", were being read as a licence to drop content.

## Built (not just measured)

`extensions/agi/bin/adapters/grok_bot_adapter.py` — `build_command` now spends
the render in the SAME `-p` slot the file already guessed, with the copilot
spelling (prompt text), and keeps the old context-path shape when no render was
handed over, so nothing that reads the stub argv moves:

```
after fix: ['grok-bot', '--model', 'x/y', '-p', 'SENTINEL_RENDERED_BRIEF_TEXT']
no render : ['grok-bot', '--model', 'x/y', '-p', '/tmp/ctx.md']
```

`restart` already forwarded `rendered_brief=` into `build_command`, so the
fix reaches the `goal:g4.7` respawn path with no second edit.

## Tests

`extensions/agi/tests/test_grok_bot_adapter.py` — two new cases (render
reaches argv / absent render keeps the path), plus the pre-existing suite.

```
$ python3 -m pytest extensions/agi/tests/test_grok_bot_adapter.py -q
17 passed in 0.31s
$ python3 -m pytest extensions/agi/tests/test_adapters.py \
      extensions/agi/tests/test_real_adapter_restart.py -q
61 passed, 3 warnings in 1.87s
```

Production lines (`git diff --numstat` on the adapter): `14 5` = 19, ceiling 40.

## Residual (named, not hidden)

The `-p` flag itself is STILL a guess — `grok-bot --help` has not been read, so
which slot the brief belongs in is unverified. This round fixes the loss, not
the spelling. `build_command` also still accepts an empty `context_file` when
no render is supplied (copilot refuses that by name); grok keeps its old
leniency deliberately, to keep the change to one question.

## Agent Notes
grok-bot discarded dispatch's rendered_brief: argv carried only the zoom map. Measured, then built: -p now carries the render (copilot spelling), old path shape kept when no render; 17+61 tests pass; 19 production lines.

PARENT PROBES (a00-1d76f39c, run by me against the diff, not the kid suite; script: sessions/iter-DH.406/a00-1d76f39c/probes.py)

probes:
- P1 wire PASS: adapters.load("grok_bot").build_command(..., rendered_brief="SENTINEL-RENDERED-BRIEF-9c2f") -> argv [..., "-p", "SENTINEL-RENDERED-BRIEF-9c2f"]. The render reaches the changed bytes live.
- P2 wire PASS: the goal:g4.7 RESTART path, not just build_command -- restart(..., rendered_brief=SENT) with a stand-in Popen captured argv [..., "-p", SENT]. The respawn path respawns WITH the render, so the fix is not build_command-only.
- P3 gate WEAK/COUNTEREXAMPLE: build_command(harness, tier="parent", context_file="", rendered_brief="") -> ["grok-bot","--model","x/y","-p",""]. An empty render silently becomes an EMPTY PROMPT: neither arm of the claim holds (it does not use the render, and it does not refuse by name). copilot refuses this state by name. Pre-existing, not introduced by this diff -- but it is a live falsifier of the claim as written, so it is the next round.
- P4 gate PASS: tier="nope" -> KeyError "harness ... declares no model for tier ...", a NAMED refusal, never another tier model.
- P5 auth PASS: needs_credential on a harness carrying an OPENROUTER_API_KEY env row is False -- no credential minted, and the render is still delivered under that env.
- P6 auth PASS: adapters.scrubbed_base(None) yields a dict; the render path is independent of the env.

verdict: the discard is indeed a silent brief loss, not an intentional stub -- P1/P2 prove the mechanism, P3 shows one state where it is still neither-used-nor-refused.
