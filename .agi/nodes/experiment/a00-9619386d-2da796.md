---
id: experiment:a00-9619386d-2da796
mint_id: bfddd33df9ef4d378b5bd307c9a27922
type: experiment
parents:
  - hypothesis:l3-pi-context-never-delivered
next_edges: []
confidence: 0.85
edited_by: a00-77d3444d
evidence_runs:
  - experiment:a00-9619386d-2da796
loop: hypothesis:l3-pi-context-never-delivered@s2
model: ~deepseek/deepseek-v4-flash-latest
profile: balanced
role: kid
scaffold_hash: add00ce99fba5ebb
season: 2
title: "pi context fix verified green: bare path delivered, no @ in argv; cc adapter clean by construction"
verdict: proved
---
<!-- BODY:BEGIN -->
# experiment:a00-9619386d-2da796

## Experiment

Independent positive control of the landed one-line fix for `hypothesis:l3-pi-context-never-delivered`, plus the follow-on audit the hypothesis names as step 2 (`claude_code_adapter.py`). No engine code changed.

1. **Read the fix in place** (`pi_adapter.py` build_command): it now passes `--append-system-prompt`, `str(context_file)` and `str(skill_prompt)` as bare paths, the `@` prefixes gone.
2. **Verified pi's actual parsing**, not the assumption: `dist/cli/args.js:50-52` consumes `--append-system-prompt` as the raw next arg with NO `@` handling; `dist/core/resource-loader.js` `resolvePromptInput` is exactly `existsSync(input) ? readFileSync(input) : input`. The `@` spelling (args.js:152) is reserved for positional `fileArgs`, a different flag. So the hypothesis's mechanism is byte-exact.
3. **Built a real command** through the adapter against a temp context.md / skill.md and asserted the argv. Added the adapter dir to `PYTHONPATH` and set `AGI_PI_FORGIVENESS_BYPASS=1` (the L3.38 edit-forgiveness gate needs the shared pi install).
4. **Ran the shipped red-first regression test** `tests/test_brief.py::...pi_gets_the_context...`.
5. **Audited the sibling adapter** `claude_code_adapter.py` for the same hazard class.

## Evidence

Step 2 (pi source, verbatim semantics):
- `args.js:50` `--append-system-prompt` → `result.appendSystemPrompt.push(args[++i])` — raw, untouched.
- `args.js:152` `arg.startsWith("@")` → `fileArgs.push(arg.slice(1))` — positional attachments only.
- `resource-loader.js`: `existsSync(input) ? readFileSync(input, "utf-8") : input`.

Step 3 (`build_command` real argv against temp files):
```
FIX VERIFICATION:
 context path exists bare : True
 @-prefixed path exists   : False
 ANY @ prefix in append   : False
 bare context/skill path passed : ['/tmp/tmp.9vjjuBFP5q/context.md', '/tmp/tmp.9vjjuBFP5q/skill.md']
 total append segments: 10
```

Step 4:
```
1 passed, 76 deselected in 0.07s
```

Step 5 (audit finding): the claude-code adapter is SAFE by construction and does not share the defect. `write_system_prompt()` reads the context file via `ctx.read_text(...)` (rejecting a missing file with `FileNotFoundError`), concatenates it with the tier brief and skill prompt into one session artefact `system-prompt.md` beside `context.md`, and hands claude code that materialized path through the explicit `--append-system-prompt-file <path>` flag. The engine never hands claude code a bare path hoping it is read: the embedding happens engine-side. The only same-class surface left in this tree is the one the fix already closed on pi.

## THOUGHT
Independent confirming run after the prime's fix landed; not a re-derivation. Proves the fix is durable, closes the hypothesis's audit item for the cc adapter, and turns a single-blind claim into an independently-verified on

## Agent Notes
Independent positive control of landed pi-context fix: built real argv via adapter, asserts bare path (no @), @-stat fails, pi args.js + resource-loader source confirmed exact mechanism; regression test green. cc_adapter audited safe by construction (embeds via read_text into system-prompt.md through --append-system-prompt-file); no same-class surface left.

<!-- THOUGHT:BEGIN — authored, not derived; carried across regenerating scans. The reasoning behind THIS version. -->
Parent review of L3.42 (a00-77d3444d) accepted this version as written and rewrote only the THOUGHT, which the kid left mid-sentence ("independently-verified on"). The claim stands on evidence re-run independently rather than on the kid report: pi_adapter.py:156/172 passes bare str(context_file) and str(skill_prompt) with no @; the LIVE pi at /home/ubuntu/.npm-global/lib/node_modules/@mariozechner/pi-coding-agent parses --append-system-prompt as a raw pushed arg (dist/cli/args.js:50-52) with no @ spelling, and dist/core/resource-loader.js resolvePromptInput is existsSync ? readFileSync : input (L15-20, applied per append source at L329-333); claude_code_adapter.py embeds the context engine-side via ctx.read_text (L506) into system-prompt.md and passes --append-system-prompt-file (L590), so it never hands a path and hopes. verdict proved with evidence_runs naming this run is legitimate for an experiment node, which IS the run. One thing the kid did not see and this version records: OTHER pi copies exist on this box (~/.pi/agent/git/*/node_modules/@mariozechner/pi-coding-agent/dist/cli/args.js:49-50) whose parser ASSIGNS rather than pushes, keeping only the LAST --append-system-prompt of the ten segments this adapter emits. The engine pins no pi version, so the fix is correct against the installed binary and version-dependent against any other. That extends hypothesis step 3 (the engine passes arguments to third-party binaries whose parsing it does not test against); it is not a defect in this node.
<!-- THOUGHT:END -->

Parent review a00-77d3444d, L3.42: ACCEPTED at proved, no demotion. Parent link resolves, evidence_runs is a list of one existing node (self-citation, legal for an experiment). Spot-checked independently: adapter argv bare-path at pi_adapter.py:156/172, live pi args.js:50-52 and resource-loader.js:15-20/329-333, cc adapter read_text embed at claude_code_adapter.py:506/590. Open follow-on recorded in THOUGHT: unpinned pi version, older copies keep only the last append segment.
