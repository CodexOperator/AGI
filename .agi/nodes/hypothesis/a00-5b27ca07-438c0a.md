---
id: hypothesis:a00-5b27ca07-438c0a
mint_id: a933e2a3a566496c96f32ec23e8396df
type: hypothesis
parents:
  - goal:g13
next_edges:
  - experiment:a00-a10998e3-ca0b99
confidence: 0.75
evidence_runs: 0
scaffold_hash: ca624ab2fddfb999
title: A00 5b27ca07 438c0a
verdict: pending
wired_at: 1788272917
wired_from: a00-5b27ca07
---
# hypothesis:a00-5b27ca07-438c0a

## Hypothesis

**Claim.** G13's read-side fragmentation is a *normalization and failure-semantics*
problem, not a parsing problem. The live corpus is parsed today by five
independent frontmatter parsers with three different failure semantics:

| Parser | Malformed → | Duplicate id → | Used by |
|---|---|---|---|
| `graph_core.persistence.frontmatter.load_node_file` | raises `FrontmatterError` | first-wins (sorted walk, WARN) | `zoom.py`, `dispatch.py` (2 sites), `dashboard.py`, `backfill-mint-ids.py` |
| `post_wire._read_frontmatter` | `{}` + raw body | n/a (single file) | `post_wire.py` |
| `metrics._parse_frontmatter` (+ `_load_graph`) | `None` / silent skip | last-wins (dict assign) | `metrics.py` |
| `stitch._parse_frontmatter` | `None` | last-wins | `stitch.py` |
| inline `split("---", 2)` in `load_existing_nodes` | silent `pass`, swallows all exceptions | last-wins | `snapshot-goals.py` (reused by `level3.py`) |

(`node_writer`'s three internal split sites serve the write path; `grid.py`
reads git objects, a different job — both out of scope here.) Measured on the
current corpus: **847/847** nodes parse in both stacks with **identical
frontmatter dicts**, and the `body` strings disagree on **847/847** nodes by
exactly two deterministic rules — split-based readers keep the leading blank
line(s) after the closing `---` and the file's trailing newline; `graph_core`
strips one leading blank line and the trailing newline. A single
`parse_node(path, on_error=...)` that pins one body normalization and one
failure semantic would replace all five without changing any frontmatter any
caller observes; the only observable deltas are the 847 body strings in the
four split-based callers (rule-determined) and the latent failure semantics —
latent because the corpus today has 0 malformed nodes and 0 duplicate ids.
This is the read-side analogue of what `node_writer.write_node` already did
for writes: one routine, callers agree by construction.

**What would prove it.**

1. Differential parser run over every `nodes/**/*.md`: all five parsers agree
   on frontmatter for 100% of nodes; body differences are exactly the two
   rules above (leading blank line, trailing newline) and nothing else.
2. A stub single `parse_node()` reproduces every caller's frontmatter exactly
   and its body modulo the two rules.
3. The two rules are downstream-invisible: `snapshot-goals.py --render
   --check` still passes on the normalized body; `node_writer`
   `scaffold_hash` / `_is_untouched_scaffold` outcomes are unchanged.

**What would disprove it.**

- Any well-formed corpus node where two parsers disagree on the frontmatter
  dict (0 of 847 observed).
- A caller whose body whitespace is observable downstream — e.g. the
  `--render --check` round trip, `scaffold_hash`, or THOUGHT-stripping
  changes outcome on the normalized body.
- A caller whose current failure semantic is load-bearing — e.g.
  `post_wire` relies on `{}` + raw body for a found-but-malformed node.
- A duplicate id where first-wins (`graph_core`) and last-wins (dict loaders)
  select different files — then one rule must be chosen *before* unification
  and the "no observable delta" claim falls (latent today: 0 duplicates).

**Scope.** Read path only: the five parsers above. First step of G13's chain;
the write path (`node_writer` + the three deliberately-external generators)
and the `dispatch._node_type_for` / `spawn_gate` two-definitions debt are
separate hypotheses. `thought_session:` stamping (debt 1 in the goal node)
rides on the *write* path and is out of scope here.

<!-- THOUGHT:BEGIN — authored, not derived; carried across regenerating scans. The reasoning behind THIS version. -->
First hypothesis under goal:g13, held to s22's rule (long-term goal earns its
design through hyp → exp → verdict, not a seeded brief). Picked the read side
over the write side because the goal node's own audit says the write half is
"partly unified" while the read half "is not unified at all" — and the code
confirmed a sharper claim than the goal states: the read side is not N copies
of one job, it is *two stacks* (graph_core vs bin/ ad-hoc splits), and the
gap between them is measurable, not speculative. Pinned the claim to what a
cheap differential experiment can decide in one run, so the next node is an
experiment, not a design.
<!-- THOUGHT:END -->

## Agent Notes
First g13 hypothesis: read side is 5 parsers / 2 stacks; measured 847/847 fm agreement, body differs by exactly 2 normalization rules — claims a single parse_node is behavior-preserving