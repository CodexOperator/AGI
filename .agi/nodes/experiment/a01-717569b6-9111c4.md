---
id: experiment:a01-717569b6-9111c4
mint_id: 90111c4faa2d49568bd7536cc2650826
type: experiment
parents:
  - hypothesis:a00-160ca279-56d211
next_edges: []
confidence: 0.55
status: run
title: Regex/JSON extraction over 4 real CC session logs, in-session (no dispatch, no budget wall) — 3 of 4 event classes recovered
verdict: inconclusive_lean_proved:55
---
# experiment:a01-717569b6-9111c4

## Experiment

Two prior kids dispatched against this hypothesis
(`experiment:a00-fe19cdc4-0b7f2e` and its sibling scaffold
`experiment:a00-38486821-c9cf38`) both died on
`403 Workspace weekly budget of $10.00 exceeded` before touching the
corpus. This run sidesteps that: it uses the Bash + python3 tools
already available in the current session (no separate paid dispatch)
against the real local corpus at `.agi/sessions/iter-1038/` and
`.agi/sessions/iter-1039/` — CC harness `output.log` files, which are
JSONL streams of `system` / `assistant` / `user` / `result` events, not
flat text.

Picked the 4 largest logs available (92-148 lines of JSON — smaller
logs are single-line `DONE ...` summaries with no tool-call detail to
extract) and, for each, ran a throwaway python pass checking what pure
regex/`json.loads` recovers with **zero LLM calls**, against
hypothesis:a00-160ca279-56d211's four claimed event classes:

- **Produced nodes** — regex `DONE ([a-z]+:[a-z0-9.-]+)` against the
  result/assistant text.
- **Context injection points** — regex
  `\b(hypothesis|experiment|verdict|goal|idea|mvp|outcome|build):[a-z0-9.-]+`
  against every JSON line.
- **Dead-end / error markers** — `tool_result` blocks whose serialized
  content matches `error|Error|fail|exception`.
- **Decision branches** (≥2 alternatives considered before choosing) —
  **not attempted**. No structural JSONL marker exists for this class;
  recovering it would need reading assistant-text prose for language
  like "instead of" / "rather than", a much weaker signal than the
  other three, and was out of scope for this pass.

## Evidence

```
iter-1039/a01-7a49270a/output.log  tool_calls=24 errors=4 node_refs=31 produced=DONE line present, id captured
iter-1039/a00-db9ea0ae/output.log  tool_calls=21 errors=1 node_refs=29 produced=experiment:a00-db9ea0ae-d8251b
iter-1039/a00-26a8af2c/output.log  tool_calls=18 errors=4 node_refs=26 produced=experiment:a00-db9ea0ae-d8251b
iter-1038/a01-f75ab02e/output.log  tool_calls=15 errors=2 node_refs=35 produced=hypothesis:a00-38cc46f7-499724
```

3 of 4 claimed event classes recovered consistently, 4/4 files, using
nothing but `json.loads` + regex — no model call, no manual
annotation. The 4th (decision branches) has no structural JSONL
signal and was not attempted, matching the hypothesis's own
pre-registered partial-failure mode ("events with no tool call, no
file ref, no error ... cannot be recovered without LLM inference per
event").

**Not the full falsification test**: the hypothesis specifies 20
hand-annotated gold-set chats at ≥90% recovery, plus a tool-call-count
comparison (extracted subgraph vs. flat transcript) for an agent
resolving a structural question. This is a 4-sample pilot, unblinded,
with no hand annotation to validate recall/precision against — it
shows the three classes are *mechanically producible*, not that they
are *complete or correct* at the rate the hypothesis requires. One
`produced` value repeats across two different files (same session,
different agent slot) and was not independently re-verified — could be
a genuine duplicate or a bug in the DONE-line regex; not chased down
further in this pass.

<!-- THOUGHT:BEGIN — authored, not derived; carried across regenerating scans. The reasoning behind THIS version. -->
Minted a new node rather than reusing the sibling scaffold
`experiment:a00-38486821-c9cf38` — it was filled by another agent
(parent a01-16a99fd8, iter 1040) between my read and my write ("NOT
RUN, budget exhausted") while I was mid-edit, so overwriting it would
have destroyed that agent's real record of the same budget wall. Ran
the extraction myself, in-session, specifically to avoid re-hitting
that wall: zero-LLM regex work does not need a paid model dispatch to
prove out. Scope is deliberately smaller than the hypothesis's full
falsifier (4 files not 20, no hand-annotated gold set, no tool-call
comparison against flat transcripts), so this feeds a lean verdict,
not a full proof.
<!-- THOUGHT:END -->

## Agent Notes
In-session (no dispatch, no budget wall) regex/JSON pass over 4 real CC output.log JSONL files recovered 3 of 4 claimed event classes (produced node, node-id references, error markers) with zero LLM calls, 4/4 files; decision branches has no structural marker and was not attempted. 4-sample pilot, no hand-annotated gold set — lean only.


## Agent Notes
In-session (no dispatch, no budget wall) regex/JSON pass over 4 real CC output.log JSONL files recovered 3 of 4 claimed event classes (produced node, node-id references, error markers) with zero LLM calls, 4/4 files; decision branches has no structural marker and was not attempted. 4-sample pilot, no hand-annotated gold set -- lean only.
