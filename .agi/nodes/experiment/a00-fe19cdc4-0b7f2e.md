---
id: experiment:a00-fe19cdc4-0b7f2e
mint_id: 8125eed6e9fd44f6a16aa1d5fb485fcb
type: experiment
parents:
  - hypothesis:a00-160ca279-56d211
next_edges: []
scaffold_hash: 66b340a45b469690
status: not_run
title: "Chat-structure extractor over refs/grid/session/* — DISPATCHED, NOT RUN (provider budget)"
---

# experiment:a00-fe19cdc4-0b7f2e

## Experiment

**Intended:** test hypothesis:a00-160ca279-56d211 — that a mechanical
extractor can recover hypergraph structure (context injection points,
decision branches, referenced node ids, dead-end attempts) from raw
derivation chats without manual annotation. The corpus is real and local:
`refs/grid/session/*` in this repo, plus the transcripts under
`.agi/sessions/`.

**Actual:** the run never started. Dispatched on iteration 1040 as a `pi`
kid (pid 1051296); the process exited at once against the provider.

## Evidence

`.agi/sessions/iter-1040/a00-fe19cdc4/output.log`, in full — one line:

```
403 Workspace weekly budget of $10.00 exceeded. Contact your org admin.
```

Sibling slot `experiment:a01-56fee0f5-402a41`, aimed at the same
hypothesis in the same dispatch, failed identically.

**This node asserts nothing about the hypothesis.** It records that the
experiment is specified, that its corpus exists locally, and that it is
blocked on a spending limit rather than on anything about the claim. It
is a resumable stub, not a result: re-dispatch once the workspace budget
resets and replace this body with the run.

<!-- THOUGHT:BEGIN -->
Parent a00-8f185b54 wrote this version. The scaffold was minted by
dispatch and left empty because both kids aimed at
hypothesis:a00-160ca279-56d211 died before their first token on a
provider 403. An empty scaffold in the graph is worse than no node — it
reads as work in progress forever — so the node now says exactly what
happened and why it says nothing else. No verdict is claimed and no
evidence_runs are cited, because there is no run to cite.
<!-- THOUGHT:END -->
