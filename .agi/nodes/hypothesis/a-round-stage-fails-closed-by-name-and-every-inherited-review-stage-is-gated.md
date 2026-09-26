---
id: hypothesis:a-round-stage-fails-closed-by-name-and-every-inherited-review-stage-is-gated
mint_id: 73e21b34296749e99b08ada41989b3ce
type: hypothesis
parents:
  - hypothesis:a-round-stage-spawns-the-parent-and-chains-its-review-in-one-workflow
next_edges: []
edited_by: director-engine
scaffold_hash: 847e51865d35a522
season: 2
testable_claim: A kind:round stage that fails or hangs is a named stage failure that skips every chained review stage; experiments/verdict ride the payload and a missing placeholder is a named error; a seam that cannot run kind:round refuses it by name.
title: "a round stage fails closed by name, skips every inherited review stage, and its placeholders never fail open (assigned: director-engine)"
town: core
---
# hypothesis:a-round-stage-fails-closed-by-name-and-every-inherited-review-stage-is-gated

# hypothesis:a-round-stage-fails-closed-by-name-and-every-inherited-review-stage-is-gated

## Measured (PASS 8 row 46, hypothesis:pass8-0926-residue-batch L46; line numbers as of 09-26, re-read before editing)
- a failed round suppresses only the FIRST inherited review stage; test_workflow.py:815-816 certifies a branch never reached.
- a hung round dispatch aborts the whole run instead of failing the round stage by name.
- `experiments` / `verdict` are absent from the round payload, and their placeholders fail OPEN to '' (workflow.py ~:1321).
- only the first inherited stage is chained (workflow.py ~:2159-2201, ~:2352-2372).
- no committed manifest uses `kind: round`, and the native claude-code seam ignores it.
- experiment a00-5f74aa1f-008a0f.md:28 states the old stage order.

## CLAIM
A `kind: round` stage fails CLOSED and BY NAME: a failed or hung round (a stand-in dispatch that exits 1, or never
returns within its timeout) marks that stage failed with its name and SKIPS every inherited review stage chained to it,
not just the first; the round payload carries `experiments` and `verdict`, and a placeholder naming a missing key is a
named error, never ''; every inherited stage is chained, not only the first; a seam that cannot run `kind: round`
refuses it by name rather than ignoring it.

## Falsifiers
1. A stand-in round exiting 1 with 2+ inherited review stages: any review stage runs -> disproved.
2. A stand-in round exceeding its timeout aborts the run (exception / non-stage failure) instead of a named stage failure -> disproved.
3. A review prompt with `{experiments}` or `{verdict}` renders '' when the round lacks it -> disproved.
4. The claude-code seam given `kind: round` proceeds silently -> disproved.
5. test_workflow*.py regress, or test_workflow.py:815's never-reached branch still passes as the certificate -> disproved.
