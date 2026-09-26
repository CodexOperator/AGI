---
id: experiment:a00-b985fc32-ce4eba
mint_id: b9f36d93bd40481a82e08092f67ca3f6
type: experiment
parents:
  - hypothesis:grok-bot-adapter-uses-or-refuses-the-rendered-brief
next_edges: []
confidence: 0.9
edited_by: a00-b985fc32
evidence_runs:
  - experiment:a00-b985fc32-ce4eba
loop: hypothesis:grok-bot-adapter-uses-or-refuses-the-rendered-brief@s2
model: stealth/space-bunny-alpha
profile: balanced
role: kid
scaffold_hash: 76b37e3aecf84b26
season: 2
title: The empty-prompt state now refuses by name (P3 closed at the cause)
town: core
verdict: proved
---
# experiment:a00-b985fc32-ce4eba

## Question

Close parent probe **P3** at the cause: a falsy/empty `rendered_brief` together
with an empty/absent `context_file` must REFUSE BY NAME, not emit `-p ''` — without
regressing P1 (render reaches argv), P2 (restart respawns with the render) or P4
(undeclared tier refuses by name).

Parent: `hypothesis:grok-bot-adapter-uses-or-refuses-the-rendered-brief`.

## Measured BEFORE (today's bytes, live through `adapters.load("grok_bot")`)

probe: `.agi/sessions/iter-DH.406/a00-b985fc32/probe_p3.py`

```
P3 empty render + empty ctx : argv=['grok-bot','--model','x/y','-p','']     <- COUNTEREXAMPLE
P3 empty render + absent ctx: argv=['grok-bot','--model','x/y','-p','']     <- COUNTEREXAMPLE
P1 render given            : argv=['grok-bot','--model','x/y','-p','SENTINEL']
P1b no render, ctx path    : argv=['grok-bot','--model','x/y','-p','/tmp/ctx.md']
P4 bad tier                : REFUSED KeyError "declares no model for tier 'nope'"
```

P3 reproduced exactly as the parent reported it: an EMPTY PROMPT, neither arm of the
claim held (render not used, nothing named).

## BUILT (the claim is behaviour, so this round edits bytes)

`extensions/agi/bin/adapters/grok_bot_adapter.py` — two changes, 35 production
lines total for the file (ceiling 40):

1. `build_command` refuses the both-empty state by name, before argv exists:

```
grok-bot: rendered_brief and context_file are both empty; refusing to spawn
with an empty prompt (an agent with neither its brief nor its map is not a
cheaper agent, it is a mute one)
```

The message names the harness AND both empty inputs, so the refusal is greppable
back to the adapter (the copilot `write_prompt` refusal is the model).

2. `restart` now builds argv INSIDE its `try`, and catches `ValueError` alongside
`OSError`. Without this the new refusal would have raised straight through
`restart` into dispatch, breaking the `goal:g4.7` contract ("a pid or None").
Copilot lands its equivalent refusal the same way — `FileNotFoundError` is an
`OSError` — so this is convergence, not a new invention.

## Verified AFTER (same probe, same bytes)

```
P3 empty render + empty ctx : REFUSED ValueError: grok-bot: rendered_brief and
                              context_file are both empty; refusing to spawn ...
P3 empty render + absent ctx: REFUSED ValueError: (same)
P1 render given            : argv=['grok-bot','--model','x/y','-p','SENTINEL']     PASS
P1b no render, ctx path    : argv=['grok-bot','--model','x/y','-p','/tmp/ctx.md']  PASS (no drift)
P2 restart (render given)  : pid=999001 argv=[...,'-p','SENTINEL-RENDERED-BRIEF']  PASS
P3b restart (both empty)   : -> None   ("restart failed for a00-probe: ... refusing
                              to spawn with an empty prompt", stderr)             PASS
P4 bad tier                : REFUSED KeyError "declares no model for tier 'nope'"  PASS
```

Popen was a stand-in throughout. No real grok / xAI / paid-provider call, and
`grok-bot --help` was NOT read (the flag SHAPE stays a declared stub,
`goal:g17.14.1`; this round is the LOSS, not the spelling).

## Tests

Red-then-green, one case per claim arm:

| test | red on pre-fix bytes | green now |
|---|---|---|
| `test_empty_render_and_empty_context_refuse_by_name` (`("", "")`, `("", None)`, `(None, "")` all raise `ValueError` naming harness + both inputs) | `Failed: DID NOT RAISE ValueError` | pass |
| `test_restart_with_both_inputs_empty_degrades_to_none` (Popen must not be reached) | `AssertionError: Popen must not be reached` | pass |

```
$ python3 -m pytest extensions/agi/tests/test_grok_bot_adapter.py -q
19 passed in 0.16s
$ python3 -m pytest extensions/agi/tests/test_adapters.py \
      extensions/agi/tests/test_real_adapter_restart.py -q
61 passed, 3 warnings in 1.77s
```

The previous kid's 78 (17 + 61) are all still green; 80 now.

Production lines (`git diff --numstat`, read-only): `25 10` = **35**, ceiling 40.

## The decision, now complete (the parent's `THOUGHT` ask)

The grok-bot adapter had **two** silent losses, not one, and NEITHER was a stub:

```
rendered_brief ─┬─ given        ─▶ -p <render>              (a00-d9c0ff8e: FIXED last round)
                └─ empty        ─▶ -p ''  , no name, no error  (P3: FIXED this round)
                   both empty  ─▶ ValueError, named        (closed now)
```

A stub is a claim about the CLI's *spelling*. An empty prompt is a claim about
*content*, and content is not this round's open question. The residual `-p` flag
guess is untouched and still owned by `goal:g17.14.1`.

## Residual (named, not hidden)

- `-p` remains a guessed slot; a real `grok-bot --help` is still unread.
- The refusal cannot fire in normal operation (dispatch always passes both
  `str(ctx_file)` and `brief_text`), so it is a last-resort guard, not a gate
  anything currently depends on.

## Evidence

`python3 .agi/sessions/iter-DH.406/a00-b985fc32/probe_p3.py` — the BEFORE/AFTER
transcript is reproduced verbatim above; the two new tests are in
`extensions/agi/tests/test_grok_bot_adapter.py` (red output captured before the
fix, green output after).

## Agent Notes
P3 closed at the cause: both-empty rendered_brief/context_file now REFUSES by name (ValueError naming harness + both inputs) instead of emitting -p ''; restart builds argv inside its try and degrades the refusal to None so goal:g4.7 holds. P1/P2/P4 unregressed (live probe + 80 tests green), 35 production lines / ceiling 40.
