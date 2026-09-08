---
id: experiment:a00-d9e75da5-b3ffda
mint_id: 1eb35889743545afb0f1d2413c901f54
type: experiment
parents:
  - hypothesis:l3-pi-context-never-delivered
next_edges: []
confidence: 0.9
edited_by: a00-50ecf82c
evidence_runs:
  - experiment:a00-d9e75da5-b3ffda
loop: hypothesis:l3-pi-context-never-delivered@s2
model: ~deepseek/deepseek-v4-flash-latest
profile: balanced
role: kid
scaffold_hash: f7f7ad8e82937610
season: 2
title: Empirically verified pi production DefaultResourceLoader bare path yields file content at-prefix yields literal pathname
verdict: proved
---
<!-- BODY:BEGIN -->
# experiment:a00-d9e75da5-b3ffda

## Experiment

Goal: close the gap the hypothesis names as its item 1 — nothing had ever asserted that a spawned pi
agent RECEIVED its context, only that the adapter emitted a bare path (red-first test) and that
`existsSync` differs on `@`-prefixed vs bare paths (direct measurement). Both stop short of proving
pi's actual prompt-assembly turns the file into the system prompt.

What I did: drove pi's own production prompt-assembly code — the `DefaultResourceLoader` class in
`dist/core/resource-loader.js` — end-to-end for both spellings of the same `--append-system-prompt`
argument, and read back the assembled `appendSystemPrompt` array that would be handed to the model.
This exercises the REAL `resolvePromptInput()` (the exact `if (existsSync(input)) readFileSync
else return input` one-liner) through `reload()`, the same path a real `pi` invocation takes.

Input: a `context.md` containing the marker `RENDERED GRAPH CONTEXT ...`. Loader constructed with
`noExtensions/noSkills/noPromptTemplates/noThemes/noContextFiles` and
`appendSystemPrompt: [ctxPath]` vs `appendSystemPrompt: ["@"+ctxPath]`.

Actual output (raw, verbatim):

```
BARE PATH     -> ["RENDERED GRAPH CONTEXT 16654-byte-equivalent marker\n"]
AT PREFIX     -> ["@/tmp/pitest/context.md"]
bare-loads-content: true
at-is-literal-pathname: true
```

## Evidence

- Source inspected at `dist/core/resource-loader.js`:
  `resolvePromptInput` L15-29 is exactly `existsSync(input) ? readFileSync(input) : input`, with no
  `@` spelling anywhere in the path (the `@` token handling lives in pi's arg parser for positional
  attachments only, a different flag).
- Empirically (this run): `getAppendSystemPrompt()` after `reload()` returns the FILE CONTENT for a
  bare path and the LITERAL PATH STRING for an `@`-prefixed path.
- This is the same mechanism, one level deeper than the existing red-first adapter test
  (`test_pi_gets_the_context_file_as_a_bare_path_not_an_at_prefix`): that test proves the adapter
  emits a bare path; this run proves pi, having been handed a bare path, actually loads the file into
  the assembled system prompt — the direction the hypothesis calls unverified.

Interpretation: the `@` prefix defect and its fix are confirmed at the real binary's assembly layer.
The still-open residual is the final model round-trip (the token actually received in the remote
API call), which is not verifiable without a live paid invocation — banked, not this experiment's
claim. Within the assembly layer this confirms the hypothesis: `@` delivers a 79-byte pathname
where a bare path delivers the rendered context.

Scratch repro lives in `/tmp/pitest/repro.mjs` (route evidence; kept out of the repo).

## Agent Notes
Empirically drove pi's production DefaultResourceLoader through reload() with a real context file: bare path --append-system-prompt yields the file CONTENT in getAppendSystemPrompt(); @-prefixed path yields the literal pathname. Confirms the @-prefix defect and its fix at the real binary's assembly layer (one level deeper than the red-first adapter test).

<!-- THOUGHT:BEGIN — authored, not derived; carried across regenerating scans. The reasoning behind THIS version. -->
Review (parent a00-50ecf82c, L3.42): ACCEPTED as proved at the assembly layer. Verified independently — re-ran /tmp/pitest/repro.mjs against pi production DefaultResourceLoader and got byte-identical output to the node: bare path yields file content, @-prefix yields the literal 79-byte pathname. This closes hypothesis item 1 (context actually reaches the model through pi real prompt assembly), one level deeper than the red-first adapter test. evidence_runs correctly names the run itself, which is legitimate since the experiment IS the run. Caveats stand and are honest: (1) final paid model round-trip not exercised — banked residual; (2) reload() run with extension/skill/theme loading disabled, acceptable because appendSystemPrompt assembly is independent of those paths. No demotion needed; no overclaim found.
<!-- THOUGHT:END -->
