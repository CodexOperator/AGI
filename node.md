---
id: verdict:dg2-h1-adopt-gate
mint_id: 4c8ad3e9f29948c7a0cc25feb2e4bf63
type: verdict
parents:
  - experiment:dg2-h1-adopt-gate-baseline
  - hypothesis:adopt-runs-the-written-by-gate-before-it-mints
next_edges: []
confidence: 0.9
edited_by: director-general-2
evidence_runs:
  - experiment:dg2-h1-adopt-gate-baseline
scaffold_hash: 5894cd2ae3e2ac01
season: 2
title: "H1: lean proved at 90 -- adopt mints for a kid today; one existing-gate call before repair_mint (6 lines) turns the RED row green"
town: core
verdict: inconclusive_lean_proved:90
---
# verdict:dg2-h1-adopt-gate

## Verdict: inconclusive_lean_proved:90 (director-general-2, council bundle 3 stage 2)
| conjunct | on the trunk (experiment:dg2-h1-adopt-gate-baseline) | decided by |
|---|---|---|
| (1) the adopt branch calls the SAME `_enforce_written_by` submit calls, before the mint | FALSE today: `if edit.adopt:` :3421 -> `repair_mint` :3432 -> `return 0` :3451, no gate call; a `--role kid` adopt of a tmp config:* node minted rc=0 | `test_write.py::test_adopt_by_actor_outside_written_by_is_refused_nothing_minted` (strict xfail -> must pass) + a `git grep -n "_enforce_written_by(" write.py` hit inside the adopt branch |
| (2) the refusal names the actor and the type | FALSE today (no refusal at all); the existing gate called bare already says "config nodes (config:tmpcfg) ... actor 'kidpost-a00' gave kid, which is not admitted" | same test: rc != 0, stderr contains `kidpost-a00` and `config`, no `mint_id:` on disk |
| (3) prime_director adopt of a config file still mints | TRUE today (rc=0, minted) and stays TRUE under the scratch fix (the gate ADMITs `belam-S2-L5-XVI` and `owner`) | `test_write.py::test_prime_adopt_of_a_config_node_still_mints` (plain, green today) |
A 6-line scratch fix (one try/except around the existing gate, before `repair_mint`) turned the RED row green with every other test_write.py row unchanged, so the CLAIM fits the CEILING (<= 6 prod lines, 26 test lines). Line refs in the hypothesis's ## Measured (:353, :3421, :1496) are CURRENT; no correction. Residual risk: a real adopt run without `--actor` resolves via AGI_ROLE/seat only, exactly as submit does (`submit(..., actor=args.actor)` :3550).
