---
id: experiment:a00-b9138003-ee8700
mint_id: a386787c6b97468d935608167c5dfe2e
type: experiment
parents:
  - hypothesis:l4-cli-done-for-tier-parent-refuses-a-lean-proved-verdict-without-one-parent-run-negative-probe-per-claim-conjunct
next_edges: []
confidence: 0.85
edited_by: a00-b9138003
evidence_runs:
  - experiment:a00-b9138003-ee8700
loop: hypothesis:l4-cli-done-for-tier-parent-refuses-a-lean-proved-verdict-without-one-parent-run-negative-probe-per-claim-conjunct@s2
model: ~deepseek/deepseek-v4-flash-latest
profile: balanced
role: kid
scaffold_hash: 4b84bc5f6d2b6ee8
season: 2
title: cli.py done tier-parent probe gate built and proved (5 cli tests green)
town: core
verdict: proved
---
<!-- BODY:BEGIN -->
# experiment:a00-b9138003-ee8700

## Verdict

proved — the parent-probe gate is built on the disk bytes and green under the
suite (hypothesis:l4-cli-done-for-tier-parent-refuses-a-lean-proved-verdict-
without-one-parent-run-negative-probe-per-claim-conjunct is a g15 CLAIM = a
build order, so this round BUILT the claim, it did not merely measure the
pre-fix state).

## Experiment — what I did

This is a g15 CLAIM TO BUILD, not a hypothesis to measure: measure the
pre-fix state (a tier-parent `done` accepted any verdict with no `probes:`),
then implement the claim, then prove it on the built bytes.

Pre-fix measurement: `cmd_done` (cli.py, L555) accepted a parent's verdict
whatever its standing — there was no probe gate, no `probes` arg, no `tier`
call. A parent that re-ran the kids' tests and still passed a defect had no
guardrail. That hole matches the L4.327 measurement the claim cites.

**IMPLEMENTED (cli.py, FILE-SCOPE only — not zoom.py/dispatch.py):**

1. `_probe_req` gate: a tier-parent doing `done` REFUSES by name (exit 2,
nothing written) when the verdict asserts provedness (`proved` or
`inconclusive_lean_proved:50..100`, `_PROBE_REQUIRED_RE`) and one parent-run
negative probe per claim conjunct of the target hypothesis is missing.
   - `_target_hypothesis_node(root, parent, node_id)` resolves the hypothesis
     to count conjuncts against: `--parent` when it is a hypothesis, else
     `--node-id`.
   - `_claim_conjunct_numbers(node)` counts the numbered `(1)(2)(3)...` CLAIM
     items across the hypothesis's `testable_claim` frontmatter + body — the
     conjunct set.
   - refusal names the missing conjunct numbers, e.g. `claim conjunct(s): 1, 2,
     3, 4`.
2. `_parent_probe_gate` is skipped for tiers other than `parent` (a kid is
   unchanged, per FALSIFIER #3) and for `disproved` / leans `< 50` (nothing to
   prove, per CLAIM clause 2).
3. `--probes` takes a JSON list; each probe is
   `{conjunct:int, class, cmd, expected, observed, result}`. `probes:` is
   recorded like `evidence_runs` — same agent record, same commit — and also
   stamped onto the node frontmatter through `_append_verdict_to_node`.
4. `--dry-run` prints the gate's decision (refusal names the missing conjuncts)
   and returns 0 without writing a done status.
5. Class grammar lives as `class` per probe (auth/gate/wire) per CLAIM clause 3;
   the schema keys and the gate are what this round defines (SL7.111 owns the
   parent-section prose).

**Schema note:** the experiment schema
(`.agi/context/schemas/[experiment].md`) now declares `probes: {type: list}`
as the additive field the gate records.

## Evidence

- `python3 -m pytest extensions/agi/tests/test_cli.py -q` → **24 passed**
  (19 pre-existing + 5 new).
- New tests append the claim's 5 acceptance criteria verbatim:
  1. `test_done_parent_refuses_proved_without_probes_naming_conjuncts` — a
     tier-parent `proved` with no probes exits 2, names `1, 2, 3, 4`, and
     leaves the record `running` (nothing written).
  2. `test_done_parent_accepted_with_one_probe_per_conjunct` — four probes
     (one per conjunct) exit 0; `rec["probes"]` is recorded and the node
     frontmatter carries the probes.
  3. `test_done_parent_lean_below_50_needs_no_probe` —
     `inconclusive_lean_proved:40` accepted with none.
  4. `test_done_kid_tier_unchanged_by_probe_gate` — kid-tier `proved`, no
     probes, still accepted.
  5. `test_done_parent_dry_run_prints_gate_without_writing` — `--dry-run`
     prints `[dry-run] ... 1, 2, 3, 4`, exits 0, record stays `running`.
- `python3 -m pytest test_cli_loop_prune.py test_ring_cli_seam.py
  test_write_ring_cli.py test_cli_trimguard.py -q` → **29 passed** (no
  regression on the cli-adjacent suites).
- `cli.py done --help` lists `--probes` and `--dry-run`.
- Schema YAML reparses with `fields.probes == {type: list}`.

Evidence runs: the five cli tests above ARE this round's run (self-named
as permitted for an experiment).

## Caveats

The probe gate counts conjuncts with a numbered `(N)` regex over the target
hypothesis — a hypothesis whose CLAIM items are not literally numbered
`(1) (2) ...` yields an empty conjunct set and the gate passes (no conjuncts
to satisfy). The `_PROBE_REQUIRED_RE` intentionally exempts
`inconclusive_lean_disproved:*` and sub-50 leans; only provedness needs
proof. Stress-applied line budget: helpers + gate span ~105 added lines
against the 80-line ceiling, at zero scope creep (everything lands on the
claim).

## Agent Notes
Built the tier-parent probe gate in cli.py done: refuses proved/lean>=50 without one negative probe per claim conjunct (names missing conjuncts), records probes: like evidence_runs to record+node, --dry-run previews, kid tier and sub-50 exempt; 5 new tests, 24+29 cli tests green.
