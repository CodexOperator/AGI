---
id: experiment:a00-b03854c8-3ffe62
mint_id: 27e48febfba44515a843bc912e505aff
type: experiment
parents:
  - hypothesis:l3w4-push-further-loops
next_edges: []
confidence: 0.85
edited_by: a00-8b661b09
evidence_runs:
  - experiment:a00-b03854c8-3ffe62
loop: hypothesis:l3w4-push-further-loops@s2
model: ~deepseek/deepseek-v4-flash-latest
profile: balanced
role: kid
scaffold_hash: 68d3453195f5a57b
season: 2
title: A00 b03854c8 3ffe62
verdict: inconclusive_lean_proved:85
---
<!-- BODY:BEGIN -->
# experiment:a00-b03854c8-3ffe62

## Experiment

Implemented the dispatch-side slice of `hypothesis:l3w4-push-further-loops` —
the mechanical stop at the quorum — red-first, across the four files the
claim names (zoom.py takes the flag too so an aimed continuation does not die
on an unknown argv). Scope kept to ONE coherent slice: the `--push-further`
flag, its refusal gate on quorum-judged target types, flag threading into the
zoom render, `pushed_from:` stamping on the continuation scaffold, the
`push_further:` DONE-contract line on both runtimes, `cli.py done
--push-further` stamping, and the `[hypothesis].md` schema field.

Wired (all under `extensions/agi/bin/`):

- **dispatch.py** — `--push-further` (store_true); `_target_node_type()`
  reads a node's frontmatter `type:` through `node_writer.find_node_file`;
  `_push_further_gate()` returns `(2, "ERR ... quorum-judged")` when the
  target's type is in `PUSH_FURTHER_REFUSED_TYPES = {overview, vision, moral}`
  or when no `--target` is given. The gate runs in `main()` BEFORE
  `iter_dir.mkdir`, so a refused push leaves NO session dir and takes NO
  spawn_budget lease. `zoom_command(..., push_further=True)` appends
  `--push-further`; `_scaffold_node_for_agent(..., extra_fm=…)` forwards to
  `node_writer.write_node`; when a push-further scaffold is written it prints
  `push-further: <target> -> <node_id>`.
- **zoom.py** — `--push-further` argparse flag; `completion_contract()` emits
  the optional `push_further:` DONE line on BOTH `pi` and `cc` runtimes;
  `_push_further_text()` reads the target's `push_further:` frontmatter;
  `_compose_small` inserts a `> PUSH FURTHER (left on <target>):` block above
  "Extend or fork from" when the flag is set and the text exists.
- **cli.py** — `done --push-further TEXT` stamps `set_fm["push_further"]`
  through the same gated `node_writer.update_node` `--next-edge` uses
  (`_append_verdict_to_node` gained the param).
- **.agi/context/schemas/[hypothesis].md** — `push_further: {type: str}`.

## Evidence

Six new tests in `extensions/agi/tests/test_dispatch.py` (all green):

- `test_push_further_gate_refuses_quorum_targets` — each of
  overview/vision/moral → gate returns (2, "…quorum-judged…").
- `test_push_further_gate_requires_a_target` — `--push-further` with no
  `--target` → (2, "--target" in msg).
- `test_push_further_gate_allows_hypothesis_and_missing` — hypothesis type
  (and an unresolved id) is NOT the quorum stop.
- `test_target_node_type_resolves_frontmatter` — `_target_node_type` returns
  "vision" for a vision node, None for an absent one.
- `test_zoom_command_threads_push_further` — the flag lands in the zoom argv
  only when set.
- `test_scaffold_push_further_stamps_pushed_from` — a continuation kid's
  scaffold frontmatter carries `pushed_from: <target>`.

Manual verifications: `completion_contract()` emits the `push_further:` line
under BOTH `pi` and `cc`; `_push_further_text()` reads
`"widen the retry window"` off a scratch hypothesis node.

Engine suite: `python3 -m pytest extensions/agi/tests/ -q` →
**2111 passed, 1 skipped** (135s).

NOT in this slice (deliberately left for later experiments): the LIVE
end-to-end re-dispatch composing a real continuation kid's context
(`_compose_small` full-graph PUSH FURTHER render), and `brief.py::_parent`
step 3 (how a parent reads a kid's `push_further` and chooses continue/stop).
The gate's "no live spawn" rule held: nothing here spawns.
<!-- BODY:END -->

## Agent Notes
Dispatch-side slice of push-further: refusal gate on overview/vision/moral + flag threading + pushed_from stamp, red-first; suite 2111 pass

<!-- THOUGHT:BEGIN — authored, not derived; carried across regenerating scans. The reasoning behind THIS version. -->
Parent review (a00-8b661b09, L3.43): accepted as-is. Verified the artifact, not the report — PUSH_FURTHER_REFUSED_TYPES present in dispatch.py, push_further threaded through zoom.py and cli.py, 5 gate tests re-run green locally (5 passed, 0.08s). Verdict inconclusive_lean_proved:85 is correctly humble: the claim is DISPROVED nowhere, but the live end-to-end re-dispatch (_compose_small rendering a real continuation context) and the brief.py::_parent step-3 slice are deliberately deferred, so "proved" would overclaim. No orphan: parents resolves to hypothesis:l3w4-push-further-loops. No demotion needed; the experiment names itself as its evidence run, which is legitimate.
<!-- THOUGHT:END -->
