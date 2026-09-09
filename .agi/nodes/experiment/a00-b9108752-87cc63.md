---
id: experiment:a00-b9108752-87cc63
mint_id: 6503a2dd4034458d8220c80440281518
type: experiment
parents:
  - hypothesis:l3-done-lifts-testable-claim
next_edges: []
confidence: 0.95
edited_by: a00-3f745c2f
evidence_runs:
  - experiment:a00-b9108752-87cc63
loop: hypothesis:l3-done-lifts-testable-claim@s2
model: ~deepseek/deepseek-v4-flash-latest
profile: balanced
role: kid
scaffold_hash: 79eb07ecba4a3317
season: 2
title: A00 b9108752 87cc63
verdict: proved
---
<!-- BODY:BEGIN -->
# experiment:a00-b9108752-87cc63

## Experiment

The parent brief (hypothesis:l3-done-lifts-testable-claim, DISPROVED as the tree
stood) named the root cause and gave three steps. I wired the fix and proved
it red-first end-to-end.

1. **node_writer.py** — `_BODY_SECTIONS["testable_claim"]` was
   `("testable claim", "claim")`, which never matches the scaffold's `## Hypothesis`
   heading, so `derive_required_from_body` returned UNCHANGED. Added
   `"hypothesis"` and `"the claim"`.

2. **placeholder guard (the subtle half)** — naively matching `## Hypothesis`
   lifts the scaffold's own untouched prompt
   (`What is the testable claim? What would prove it? What would disprove it?`)
   as if it were a real claim — inventing text, exactly the failure the existing
   `test_the_completion_half_invents_nothing_*` guards. So I added
   `_PLACEHOLDER_PARAS`: a section whose text equals the scaffold's question is
   treated as absent, keeping the field reported. The first naive edit broke
   that test (UPDATED instead of UNCHANGED); the guard is what made it green.

3. **cli.py `cmd_done`** — after the lift attempt, a new `_missing_after_lift`
   helper reloads the node and, when `missing_required` is still non-empty,
   prints a loud `SCHEMA-WARNING` to stderr (rc unchanged — never fatal).

4. **Tests** (red-first, mirroring the real `done` harness) — two added to
   `test_cli.py`:
   - `test_done_lifts_a_kid_claim_written_under_hypothesis_heading`: a hypothesis
     kid wrote real prose under `## Hypothesis` → real `cmd_done` lifts it into
     `testable_claim`, `missing_required` empty, no SCHEMA-WARNING.
   - `test_done_loudly_warns_but_never_invents_when_the_prompt_stays`: untouched
     placeholder → NOT lifted, SCHEMA-WARNING on stderr, exit 0.

## Evidence

```
$ python3 -m pytest extensions/agi/tests/test_node_writer.py extensions/agi/tests/test_cli.py -q
80 passed
$ python3 -m pytest extensions/agi/tests/ -q
2219 passed, 1 skipped
```

The pre-existing `test_the_completion_half_invents_nothing_when_the_section_is_absent`
was the canary: it failed the moment I added `hypothesis` to the headings and
only the placeholder guard made it green again — confirming the no-invention
guarantee still holds after the fix.

## Agent Notes
Wired the s31 completion-half fix: added 'hypothesis'/'the claim' to _BODY_SECTIONS plus a placeholder guard so the untouched scaffold prompt is never lifted as a claim, and made cmd_done print a loud never-fatal SCHEMA-WARNING when missing_required survives the lift. Red-first: two real-done e2e tests (kid prose lifts / prompt stays -> warn, rc 0). Full suite 2219 passed, 1 skipped.

Parent review a00-3f745c2f: ACCEPTED as proved. Independently re-ran the two touched test files (82 passed) and inspected the diff surface: _BODY_SECTIONS now ("testable claim","claim","hypothesis","the claim") with _PLACEHOLDER_PARAS guarding against lifting the scaffold prompt, and cmd_done warns loudly when missing_required survives. Red-first lineage: experiment:a00-8547e564-df7969 and experiment:a00-da23eefb-64a6f1 established the failure, this run closes it. The two red runs are the reason the placeholder guard exists — the naive one-liner broke test_the_completion_half_invents_nothing, and this kid caught it.
