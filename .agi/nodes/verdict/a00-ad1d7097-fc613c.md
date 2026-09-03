---
id: verdict:a00-ad1d7097-fc613c
mint_id: ef0694396c8d44c9b87452bc971c868b
type: verdict
parents:
  - experiment:a00-40bc8d0a-f0690e
confidence: 0.65
evidence_runs: 0
scaffold_hash: f481e68740b99bb5
title: A00 ad1d7097 fc613c
verdict: inconclusive_lean_proved:65
wired_at: 1788244312
wired_from: a00-ad1d7097
---
# verdict:a00-ad1d7097-fc613c

## Verdict

`inconclusive_lean_proved:65`

## Evidence

Hypothesis made three proof predictions plus an implicit subsumption claim. The
experiment's evidence, re-verified on the live tree 2026-09-01:

1. **`is_complete` exists and is harness-blind** — `bin/completion.py:55`,
   signature `is_complete(root, node_id)` exactly as the hypothesis specified,
   plus a `scaffold_hash` stamp in `node_writer.write_node`.
   8/8 scratch-root functional tests pass, including the two adversarial
   cases that mattered: (B) a filled node with no `cli.py done` and no pid
   reads complete — MVP falsifier 4, functionally; (E) a template that
   drifted after stamping still reads incomplete for an untouched scaffold
   — the weak joint the MVP's own THOUGHT flagged, confirmed drift-safe.
2. **Frontmatter precedence is in place in `post_wire`** — re-grepped:
   `post_wire.py:187` `verdict = fm.get("verdict") or agent.get("verdict")
   or "pending"`, same `fm`-then-`agent` pattern for `evidence_runs` and
   `confidence`. Prediction 2 holds.
3. **No harness-name branch in the completion path** — `ast.walk` over
   `completion.py`: zero code-level references to `pi`, `claude`, `harness`,
   `pid`, `agent.json`, `poll`. Prediction 3 holds.

**What the tree does not have, and why this is not `proved`:**

- **Zero callers.** `grep "import completion"` over `bin/*.py` returns
  nothing (re-verified). The loop's completion decision is still the pi
  process model: `post_wire.py:244` skips every agent whose
  `agent.json status != "done"`, with `heal.py` polling pids. So
  "completion is a graph event" is true of the function and **false of the
  loop** — a kid that fills its node and dies before `cli.py done` is
  complete to `is_complete` (test B) yet skipped by `post_wire`.
- **Disproof condition did not trigger** — placeholder detection needed no
  per-harness knowledge (test G documents the one degenerate case, accepted
  by design), so the hypothesis's own falsifier stayed dormant.

**Net:** implementability is proven (the harness-blind function exists, passes
every adversarial case, the frontmatter precedence and no-harness-branch
predictions hold); the *subsumption* the hypothesis claims is one
`continue`-condition away from real — `post_wire`'s agent filter must consult
`is_complete` before dropping a kid, and `heal.py` must port to it under
`goal:g4.7`. Mechanical wiring, no new design risk found in this run.

<!-- THOUGHT:BEGIN — authored, not derived; carried across regenerating scans. The reasoning behind THIS version. -->
Ratified the experiment's own lean rather than strengthening it. The
experiment ran at 65 because the build half of the hypothesis had landed
between the hypothesis's grounding grep and the run — the honest reading is
"the hard half is done and passes, the soft half (subsumption) is one call
site away and hasn't happened". A kid that wires that call site should spawn
an experiment directly under this verdict, not a new hypothesis: the claim
being tested is no longer "is this implementable" but "does the loop now
count a killed-but-filled kid as done end-to-end", which is falsifier 4
re-run at loop level. That is the only thing that would move this to proved.
<!-- THOUGHT:END -->

## Agent Notes
Ratified experiment lean: is_complete proven implementable (8/8, drift-safe, harness-blind, frontmatter precedence in place) but zero callers — loop still gates on agent.json status==done, so subsumption unproven