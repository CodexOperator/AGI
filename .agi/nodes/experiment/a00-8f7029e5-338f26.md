---
id: experiment:a00-8f7029e5-338f26
mint_id: cf52deae121c487aa87f2486f55a3186
type: experiment
parents:
  - hypothesis:a-round-manifest-declares-what-its-reviews-are-owed-and-a-missing-one-names-itself
next_edges: []
confidence: 0.9
edited_by: a00-b80ae6c3
evidence_runs:
  - experiment:a00-8f7029e5-338f26
loop: hypothesis:a-round-manifest-declares-what-its-reviews-are-owed-and-a-missing-one-names-itself@s2
model: stealth/space-bunny-alpha
probes:
  - "[auth] bare merge-up-review (the caller the claim never authorises) runs rc 0 with no owed-placeholder failure; neither base manifest file carries inherited_required_placeholders or required_placeholders"
  - "[gate] real composed round-mur/round-research-review with the declared key dropped from the harvest: the first inherited stage rendering it does NOT run and stderr carries stage <label> required placeholder(s) [key], rc != 0; the prelude round stage also carries no schema naming a range key (the backdoor that would re-whitelist them)"
  - "[wire] monkeypatching the PRE-KID _chain_owed_keys body back in silences that failure (rc 0), so the gate is the changed line and not incidental; with a complete harvest the stand-in review is called and the range is rendered into its prompt"
  - "file: sessions/iter-DH.400/a00-b80ae6c3/test_parent_probes.py (12 passed, 2 skipped)"
production_lines: 23
profile: balanced
role: kid
scaffold_hash: c431822fcd8e7d2c
season: 2
title: "a rounds declared owed keys are live: the owed-placeholder guard is no longer whitelisted away"
town: core
verdict: proved
---
<!-- BODY:BEGIN -->
# experiment:a00-8f7029e5-338f26 — the round manifest declares the range keys its INHERITED reviews are owed, and the declaration is LIVE

## What I built (all three conjuncts, on the REAL committed bytes)

| conjunct | how | bytes |
|---|---|---|
| 1 COMPOSITION, not the base | new manifest cell `inherited_required_placeholders` in the two ROUND manifests, unioned onto every INHERITED stage by `_load_manifest` | `round-mur.json:8` = `["old_tip","new_tip","files"]`, `round-research-review.json:9` = `["files"]` |
| 2 the declaration is LIVE | `_chain_owed_keys` no longer excuses a DECLARED key through `_STRUCTURED_RETURN_KEYS` | `extensions/agi/bin/workflow.py` `_chain_owed_keys` |
| 3 no regression of the happy path | the round's return is merged into `args` before dependents run, so a returned key is `known` and the guard is silent | unchanged `run_workflow` args merge |

Why per-manifest and not one list of three: the base prompts differ. `merge-up-review`'s review/verify
render `{old_tip}{new_tip}{files}`; `research-review`'s `review`/`verify` render only `{files}`, and its
`why`/`brainstorm`/`refute` render no range key at all. Declaring all three on round-research-review would
be a false failure (a review that renders nothing blank, failed for a key it never names) — so the cell says
exactly what that round's inherited stages are owed, read off the inherited prompts.

`workflow.py:2240-2247` was the near-miss the brief predicted: `_STRUCTURED_RETURN_KEYS` whitelists
`old_tip/new_tip/files` as "a prior return can ALWAYS carry". A declaration is whitelisted away by that, so a
manifest could declare them, the suite would stay green, and nothing would be enforced. The fix is
`known.update(_STRUCTURED_RETURN_KEYS - set(declared))`: a DECLARED key is judged only by what can actually
supply it here (run args, repeat item, the prior's schema, the round's own returned value).

## Falsifiers, as run

| # | result | evidence |
|---|---|---|
| 1 every inherited stage rendering a key DECLARES it, through the real loader | PASS | `test_every_inherited_stage_declares_what_the_round_owes_it` (reads `required_placeholders` off `_load_manifest`+`_expand_stages`, and the prompts off the BASE, so a manifest that declared nothing fails) |
| 2 a harvest missing the key fails the FIRST review that renders it, by name | PASS | `test_a_missing_owed_key_names_itself_on_the_real_manifest` — stderr carries `stage review:S1.7 required placeholder(s) ['files'] are owed by nothing`, rc 3, the run record marks that stage `failed`, and it never ran |
| 3 all three present -> the reviews run exactly as before | PASS | `test_a_complete_harvest_still_runs_every_review` — rc 0, every slice ran, `failed == 0`, no "required placeholder" on stderr |
| 4 the base manifests gain nothing | PASS | `test_the_base_manifests_gain_nothing` + `git diff --numstat`: `merge-up-review.json` / `research-review.json` are not in the diff at all |
| 5 no suite regression | PASS | `pytest extensions/agi/tests/ -k workflow -q` -> **212 passed, 2 skipped, 6537 deselected** (parent baseline 202 passed; +10 = my 4 new tests' params, 2 of them skipped as `research-review renders no {old_tip}`) |

Every seam is a stand-in: `subprocess.run` is the round dispatch, `_run_stage_pi` is the review dispatch,
`_round_git_harvest` is the git range, `shared_project_root` is a tmp dir. No `claude`/`pi` process, no
model load, no real workflow run.

## What I found and did NOT fix (not my seam)

A stage whose immediate parent was SKIPPED — rather than failed — still RUNS. With `round-research-review`
and a harvest missing `files`: `review` fails on the owed gap, `verify` is skipped, and `why:S1.7` runs (its
direct chain parent is `verify`, which never failed, and `round-parent` succeeded). That is a pre-existing
cascade hole in the skip branch, not a product of this build: a stand-in review that simply returns rc 3
produces the identical shape (probe
`.agi/sessions/iter-DH.400/a00-8f7029e5/probe_skip_cascade.py` — `review:S1.7 failed`, `verify:S1.7 skipped`,
`why:S1.7` runs). The skip branch is DH.399's, so the assertion is scoped to the FIRST stage that renders
the key — the claim as written — and the hole is named in the test docstring for whoever owns the skip.

## Production lines

`git diff --numstat` over production paths (tests excluded): `workflow.py` 19/3, `round-mur.json` 2/1,
`round-research-review.json` 2/1 = **23 added, 5 removed**. Ceiling 40. ✓

## Agent Notes
built: round manifests declare inherited_required_placeholders (round-mur 3, round-research-review files) and _chain_owed_keys no longer whitelists a DECLARED key; all 5 falsifiers pass on real bytes, -k workflow 212 passed

<!-- THOUGHT:BEGIN — authored, not derived; carried across regenerating scans. The reasoning behind THIS version. -->
PARENT REVIEW (a00-b80ae6c3, DH.400) — read the BYTES, not this verdict.

WHAT I READ: the diff ba10ee07c..844d1fecd. It carries 22 lines in workflow.py
(`_load_manifest` unions a new `inherited_required_placeholders` cell onto every
inherited stage; `_chain_owed_keys` computes
`known.update(_STRUCTURED_RETURN_KEYS - set(declared))`), 2 lines in each round
manifest, 110 in the test file, and NOTHING in merge-up-review.json or
research-review.json. Every deliverable the node names is in the diff.

PROBES (mine, one per conjunct; file
sessions/iter-DH.400/a00-b80ae6c3/test_parent_probes.py, 12 passed 2 skipped):

- P1 auth — the caller the claim never authorises: the two BASE manifests, run
  bare. `merge-up-review` with no round returns rc 0, runs its review, and says
  nothing about a required placeholder; neither base file carries the cell or
  any `required_placeholders`. The composition did not leak onto the base.
- P2 gate — the exact blocking state: real composed round, harvest missing
  `old_tip` / `new_tip` / `files`. For every key the round DECLARES, the first
  inherited stage whose prompt renders it does NOT run and stderr carries
  `stage <label> required placeholder(s) ['<key>']`, rc != 0. Also the backdoor
  check: the prelude round stage carries no `schema` whose properties/required
  name a range key — had it, `_chain_owed_keys` would have re-whitelisted them
  from the schema branch and the declaration would be inert again.
- P3 wire — the call site reaches the changed bytes. (a) MUTANT: I monkeypatched
  the PRE-KID `_chain_owed_keys` body (blanket `known.update(_STRUCTURED_RETURN_KEYS)`)
  back in and the falsifier-2 failure goes QUIET, rc 0 — so the gate is the
  changed line and nothing incidental. (b) LIVE: with a complete harvest the
  stand-in review is called and `0ldt1p` / `n3wt1p` / the file name are RENDERED
  into its prompt — a stub that never saw the values would fail this.

NEAR MISSES I CHECKED FOR, and what the bytes do:
- "declare the three keys and keep the whitelist" — workflow.py:2264 subtracts
  `declared` from the whitelist; the manifest cell is a real claim, not a comment.
- "edit the base manifests instead" — `git diff --stat` names no base file.
- "one hardcoded list of three in workflow.py" — the cell is per-manifest
  (round-mur owes three, round-research-review owes only `files`), read off the
  inherited prompts, which is why the two differ.
- my own first mutant (re-adding the key to `_STRUCTURED_RETURN_KEYS`) was
  DEFEATED by the line under test, because the new code subtracts `declared`
  from that frozenset. The honest mutant is the pre-kid FUNCTION. Noted so the
  next reader does not repeat my wrong probe.

CAVEATS the node does not own (neither is a refutation of the claim as written):
- `files: []` — a present-but-EMPTY harvest — passes the gate. The claim says
  "lacking", and an empty range is a real state no key test can distinguish.
- a stage whose immediate parent was SKIPPED rather than failed still runs; the
  skip branch is DH.399's. The kid named it instead of quietly narrowing.
- cosmetic: in `test_a_missing_owed_key_names_itself_on_the_real_manifest` the
  explanatory string sits AFTER the `pytest.skip`, so the function has no
  docstring. The claim it explains is the falsifier-2 one.

ACCEPTED: `proved`, evidence_runs = experiment:a00-8f7029e5-338f26 (it IS the
run). Suite: I re-ran `-k workflow` myself, 212 passed / 2 skipped against my
202-passed baseline, no regression.
<!-- THOUGHT:END -->
