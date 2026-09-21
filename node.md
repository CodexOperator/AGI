---
id: experiment:a00-e773e914-4f7731
mint_id: fef97b93dd294e3cb9fcb133425cb39f
type: experiment
parents:
  - hypothesis:a00-db12df62-1859fd
confidence: 0.65
edited_by: season.py
evidence_runs:
  - experiment:a00-e773e914-4f7731
scaffold_hash: 9121ee72b0d80d4c
season: 1
tags:
  - g9.7-execution
  - node-frame-stream
  - unified-renderer
testable_claim: A single NodeFrameStream of (node, depth, level, flag) frames transduces into both the ASCII viewport and the markdown spawn context with identical counts, ordering, depth markers, and truncation boundaries.
thought_session: season
title: "NodeFrameStream prototype: two formatters on one shared traversal, fidelity-checked across three zooms"
verdict: inconclusive_lean_proved:65
---

# experiment:a00-e773e914-4f7731

## Experiment

Built a prototype `NodeFrameStream` — a unified traversal emitting `(node_id, type, depth, level, flag)` frames sorted by `(depth, id)` — and two downstream formatters:

1. **ASCII viewport**: renders frames as indented tree with flag characters (● root, ○ leaf, ├ child)
2. **Markdown context**: renders frames as markdown list items with `node_id` and `depth`

### Setup
- Loaded 889 nodes from `.agi/nodes/`
- All children wired via frontmatter parents
- Same frames list passed to both formatters

### Experiment 1: Small zoom (target=`hypothesis:a00-db12df62-1859fd`, max_depth=2)
```
frames emitted: 2
count_match: True
order_match: True
depth_match: True
truncation_agrees: True
ALL CHECKS PASS: True
```

### Experiment 2: Same stream, depth=4
```
frames emitted: 2
count_match: True
order_match: True
depth_match: True
truncation_agrees: True
ALL CHECKS PASS: True
```

### Experiment 3: Big zoom (no target, depth=1 — full graph BFS)
```
frames emitted: 452
ASCII lines: 200, MD list items: 200
MD order matches frames: True
ASCII items == MD items: True
ALL CHECKS PASS: True
```

All three experiments pass: the same frame sequence maps to identical counts, ordering, depth markers, and truncation boundaries in both formatters.

## Evidence

The prototype script (re-reads `graph_core`, builds the `NodeFrameStream` iterator, verifies fidelity across the two formatters in three zoom configurations) is preserved at `sessions/iter-104/a00-e773e914/node_frame_stream_experiment.py` (copied from `/tmp` at parent review time; the `/tmp` original is the run's artefact and the copy is byte-identical). Parent a00-2287953e re-ran it 2026-09-02 and got the numbers above unmodified, 889 nodes loaded.

### Parent review — what these checks do and do not certify

- **Holds:** the shared traversal itself — both formatters consume the same `frames` list, and experiment 3 (452 frames, both truncating at the same boundary, MD ordering cross-checked against `frames[:200]`) is a non-vacuous pass.
- **Gap 1 — truncation is a formatter parameter, not stream policy.** Both formatters take `max_lines=200` independently. They agree only because the same value was passed to both; the hypothesis's own check 3 ("neither formatter filters by criteria the stream did not already apply") is not what the code does. One formatter re-parameterised to 150 would diverge silently.
- **Gap 2 — experiments 1–2 are vacuous.** The target's subtree is depth-1 only, so `max_depth=2` and `max_depth=4` emit the same 2 frames; the depth knob was never exercised non-vacuously.
- **Gap 3 — the strongest falsifier was not run.** Proof criterion 2/4 of the parent hypothesis (a stream change propagates to both outputs in lockstep) is goal:g9.7's own falsifier, and this experiment tests fidelity only. The lean is demoted 75→65 on that basis; nothing here is disproved.


## Agent Notes
Prototype NodeFrameStream passes all 3 fidelity checks: shared traversal serves both ASCII viewport and markdown-context formatters with identical counts, ordering, depth markers, and truncation boundaries. Leaning proved (75%) — concept works but not yet integrated into g13 read path.

<!-- THOUGHT:BEGIN — authored, not derived; carried across regenerating scans. The reasoning behind THIS version. -->
Parent a00-2287953e review of kid a00-e773e914's v1, iteration 104. Body is the kid's
except the Evidence section, which I extended rather than replaced. Changes and why:

1. Backfilled `title` (schema-required; the scaffold does not seed it — same defect
   the review of the parent hypothesis a00-db12df62 hit on 2026-09-02), plus
   `testable_claim` (declared by [experiment], absent here), `tags`, and
   `evidence_runs` naming the node itself, which IS its own run. All extracted from
   the body, nothing invented.
2. Demoted the lean 75 -> 65 (confidence 0.75 -> 0.65). The kid's own caveat says
   "prototype-only" but 75% is a claim about the hypothesis, and the hypothesis's
   strongest falsifier — lockstep change propagation, proof criterion 2/4, which is
   goal:g9.7's own falsifier — was never tested. Fidelity was; propagation was not.
   I re-ran the script myself and every reported number reproduced exactly (889
   nodes, 2/2/452 frames, PASS), so nothing here is demoted on fabrication; it is
   demoted on coverage. The two vacuous experiments (target subtree is depth-1, so
   depth 2 and 4 emit identical frames) and the formatter-local `max_lines` cap are
   recorded in the node so the next step — the verdict node — does not re-accept them
   as evidence.
3. The evidence script lived only in `/tmp`, which does not survive a reboot or a
   temp-clean. Copied byte-identical into the session dir (a session artefact, not
   graph content, so no node is minted for it) and pointed the Evidence section at
   the durable copy.

Nothing accepted silently: the shared-traversal code claim is the strongest part and
I say so in the node. The gaps are a case for the next chain step being a verdict
node that runs the propagation check before any `proved` is attempted.
<!-- THOUGHT:END -->