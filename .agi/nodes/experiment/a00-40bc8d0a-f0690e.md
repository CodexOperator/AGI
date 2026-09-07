---
id: experiment:a00-40bc8d0a-f0690e
mint_id: d0d380443abb4a099a2faec36f960636
type: experiment
parents:
  - hypothesis:a00-9bae6ee8-52d7f5
next_edges:
  - verdict:a00-ad1d7097-fc613c
confidence: 0.65
edited_by: season.py
evidence_runs: 1
scaffold_hash: 4c52118e15558a66
season: 1
thought_session: season
title: A00 40bc8d0a f0690e
verdict: inconclusive_lean_proved:65
wired_at: 1788243868
wired_from: a00-40bc8d0a
---
# experiment:a00-40bc8d0a-f0690e

## Experiment

Functional test of the hypothesis's three predictions against the live tree,
run on 2026-09-01 against a scratch project root (`/tmp/exp_is_complete/`,
no repo mutation, no git):

1. **Tree state check first — the hypothesis's grounding is stale.** It
   claimed "no `is_complete` exists anywhere in `extensions/agi/bin/`".
   `bin/completion.py` now exists with `is_complete(root, node_id)`,
   exactly the signature the hypothesis specified, plus a `scaffold_hash`
   stamp in `node_writer.write_node` (`node_writer.py:319,435`). The build
   half landed after the hypothesis's grep. The experiment therefore tested
   the built code, not the absence of it.
2. **Scratch-root functional tests** (`/tmp/exp_is_complete/test_is_complete.py`,
   real `node_writer.write_node` scaffolds, real `completion.is_complete`):
   8/8 PASS.

## Evidence

Test results (all against scratch root `/tmp/exp_is_complete/root`):

```
PASS  A: untouched stamped scaffold is incomplete
PASS  B: filled node, no cli.py done (killed) -> complete [falsifier 4]
PASS  C: legacy (no scaffold_hash), untouched -> incomplete
PASS  D: legacy (no scaffold_hash), filled -> complete
PASS  E: template drift, untouched stamped scaffold still incomplete (drift-safe)
PASS  F: unknown node id -> False (no raise)
PASS  G: kid rewrote exactly the placeholder -> incomplete (known limit, by design)
PASS  H: no harness-name/pid/agent.json branch in completion.py code (ast-verified)
```

- **B is the MVP falsifier 4, functionally:** a node with a real body and no
  `agent.json`, no `cli.py done`, no pid — `is_complete` returns `True`.
- **E is the weak joint the MVP's THOUGHT flagged:** `BODY_PROMPTS` changed
  after the stamp; the untouched scaffold still hashes to the stamp and
  still reads incomplete. Drift-safe as claimed.
- **G is the honest limit, confirmed by design:** a kid whose body is
  byte-identical to the placeholder reads incomplete. The hash resolves
  template drift (E) but not the degenerate rewrite (G); neither needs
  harness-specific knowledge, so the hypothesis's disproof condition
  (placeholder detection requiring per-harness logic) did not trigger.
- **H via `ast.walk` over `completion.py`:** zero code-level string/name
  references to `pi`, `claude`, `harness`, `pid`, `agent.json`, `poll`.
  (First pass of H failed on my naive `#`-comment strip; the three hits
  were module/function docstrings, not code — ast check is the real one.)

**Prediction 2 verified in `post_wire.py`** (`_gate`, lines ~179-195):
`verdict = fm.get("verdict") or agent.get("verdict") or "pending"`;
`evidence_runs` from frontmatter, `agent.json` fallback; `confidence`
same precedence at lines 274-279. All three fields, frontmatter primary.

**The gap the tests expose — loop integration, not the function.**
`grep "import completion"` over `bin/*.py`: **zero callers.** The loop's
completion decision is still the pi process model:
`post_wire.py:244` — `if agent.get("status") != "done": continue` (i.e.
wiring is gated on `cli.py done` having written `agent.json`, with
`heal.py` still polling pids at `heal.py:112-113`). A kid that fills its
node and dies before `cli.py done` is complete to `is_complete` (test B)
but is **skipped by `post_wire`** — falsifier 4 holds at function level,
not end-to-end.

## Verdict

`inconclusive_lean_proved:65`. Implementability is proven: the one
harness-blind function exists, passes 8/8 including the drift-safety and
kill-before-done cases, and frontmatter-precedence in `post_wire` is in
place. What the hypothesis claims but the tree does not yet have is the
*subsumption*: `is_complete` has no callers, so "completion is a graph
event" is true of the function and false of the loop. Remaining work is
wiring (call `is_complete` from `post_wire`'s agent filter, let `heal.py`
port to it under `goal:g4.7`) — mechanical, no new design risk found.

<!-- THOUGHT:BEGIN — authored, not derived; carried across regenerating scans. -->
The hypothesis aimed at a joint the tree had already half-moved past: the
build landed between the hypothesis's grounding grep and this run, so the
useful measurement is what the *built* code still doesn't do. That is the
`is_complete` no one calls — the strongest possible evidence the design is
implementable (it is implemented and passes every adversarial case I threw
at it, including the template-drift case the MVP itself flagged as the weak
joint) and the clearest statement of what remains: the loop's completion
decision is one `continue`-condition away from being a graph event.
<!-- THOUGHT:END -->

## Agent Notes
is_complete built and passes 8/8 (drift-safe, kill-before-done, harness-blind); but zero callers — post_wire still gates on agent status==done, so falsifier 4 holds at function level, not loop level