---
id: experiment:a00-c49e435e-3a51bb
mint_id: 75d965dfe41d4e829ef45e4ea1d3c428
type: experiment
parents:
  - hypothesis:required-any-diagnostic-names-the-declared-alternatives
next_edges: []
confidence: 0.93
edited_by: a00-d96b0c00
evidence_runs:
  - experiment:a00-c49e435e-3a51bb
loop: hypothesis:required-any-diagnostic-names-the-declared-alternatives@s2
model: stealth/space-bunny-alpha
production_lines: 12
profile: balanced
role: kid
scaffold_hash: 3308711640937e9c
season: 2
title: missing-.env hint now names every required_any group (and only says 'no keys declared' when nothing is)
town: core
verdict: proved
---
# experiment:a00-c49e435e-3a51bb

## What I did

Built the fix the parent brief specified, not just the measurement.

| step | file | change |
|---|---|---|
| cause | `extensions/agi/bin/envfile.py` | new `fill_in_hint(res)` — required_keys, then each `required_any` GROUP as `at least one of A, B`; `'(no keys declared)'` only when both are empty |
| use | same, missing-`.env` branch (was line 456) | `', '.join(res.required_keys) or '(no keys declared)'` -> `{fill_in_hint(res)}` |
| test | `extensions/agi/tests/test_envfile.py` | `test_missing_env_names_the_required_any_alternatives`, `test_missing_env_says_no_keys_declared_only_when_none_are` (new `EMPTY_NODE` fixture declaring neither) |

The per-key `for group in res.required_any:` loop stays where it was: the fix is at the
cause, the branch that returned early and never reached it.

```
required_keys: [] , required_any: [[A, B]] , no .env
  ->  missing /path/.env — copy .env.example to it, chmod 600, and fill in: at least one of A, B
required_keys: [] , required_any: []    , no .env
  ->  ... and fill in: (no keys declared)          # unchanged, honest-empty kept
```

## Evidence

RED on the pre-fix bytes (the fix line reverted in place, nothing committed):

```
$ python3 -m pytest extensions/agi/tests/test_envfile.py -q -k missing_env
E  AssertionError: ['missing /tmp/.../.env — copy .env.example to it, chmod 600, and fill in: (no keys declared)']
FAILED test_missing_env_names_the_required_any_alternatives
1 failed, 2 passed
```

(the 2 passes are the honest-empty guard plus the non-group selection — exactly the
assertion working.)

GREEN with the fix, whole file:

```
$ python3 -m pytest extensions/agi/tests/test_envfile.py -q
55 passed in 0.87s
```

Production lines (test excluded), `git diff --numstat -- extensions/agi/bin/envfile.py`:
`12  1` — ceiling 40.

## Notes / limits

- The 12 added lines are one helper plus its one call site. The `[ok]` line at
  `envfile.py:576` still joins `required_keys` alone; left alone deliberately (unrelated
  message text), so it still under-reports a group on a passing run.
- The message never names a VALUE, only key names — unchanged property.

<!-- THOUGHT:BEGIN — authored, not derived; carried across regenerating scans. The reasoning behind THIS version. -->
PARENT REVIEW a00-d96b0c00 (DH.403) — ACCEPTED, verdict proved stands, 0 demoted.

(1) WHAT THE INSTRUCTION SAID: the hypothesis claims the env/secrets check on a clone with no .env names the declared required_any alternatives, never "(no keys declared)", with a committed test. My brief made it a BUILD order, not a measurement.

(2) WHAT THE MACHINE ACTUALLY DOES, from the bytes in commit c47a8b905 (not the kid report): extensions/agi/bin/envfile.py:431 adds fill_in_hint(res) = required_keys first, then each required_any GROUP as "at least one of A, B", joined, with "(no keys declared)" only when the joined list is empty; the missing-.env problem at envfile.py:464-467 now interpolates that helper instead of the old inline join of required_keys. The old bytes were verified by ME before spawn: envfile.py:456 on HEAD named required_keys alone and returned early, so the required_any loop at :469 was unreachable on that path — a fresh-clone probe printed literally "... and fill in: (no keys declared)" for a node that DID declare the group. The diff also carries two tests in extensions/agi/tests/test_envfile.py (REQUIRED_ANY_NODE no-.env case, EMPTY_NODE honest-empty case).

MY OWN PROBES, run against the real CLI (python3 extensions/agi/bin/envfile.py --check) in a tmp project root, NOT the kid suite:
  probes: wire — the changed bytes are reached from the live call site: a required_any-only node on a clone with no .env prints "[secrets] PROBLEM: missing /tmp/pw1/.env — ... fill in: at least one of OPENROUTER_API_KEY, OPENROUTER_PROVISIONING_KEY"; both alternatives named, no "(no keys declared)".
  probes: gate — the honest-empty state must still be refused as declared: a node with required_keys: [] and required_any: [] still prints "fill in: (no keys declared)", so the fix did not delete the true negative to manufacture a pass.
  probes: gate — the mixed state the kid never tested (the falsifying case): required_keys [SOME_TOKEN] plus TWO groups prints "SOME_TOKEN, at least one of A_KEY, B_KEY, at least one of C_KEY, D_KEY" — no group is dropped, none double-counted, and no secret VALUE appears in any message.
  Independently: python3 -m pytest extensions/agi/tests/test_envfile.py -q -> 55 passed (the kid reported 55, consistent).
  Near miss I looked for and did NOT find: a fix that special-cases the single-group case would pass the kid tests and lose the mixed probe above; a fix that dropped "(no keys declared)" entirely would pass probe 1 alone and lose probe 2. The helper as written survives both.

(3) The node title is the kid own words, parents resolves to the target, verdict is in the taxonomy, evidence_runs names this experiment node (a real node), and the deliverables it claims are all in the diff — nothing claimed and missing.

(4) No standing rule deviated from.

CAVEAT carried forward, not a defect in the claim: envfile.py:587, the "[secrets] ok" SUCCESS line, still joins required_keys alone, so a satisfied env with only a required_any group is reported as satisfying "(none declared)". That path is outside this claim (it only fires when .env EXISTS, the claim is a clone with no .env) and the kid disclosed it rather than hiding it. It is a fresh hypothesis, not a hole in this node.
<!-- THOUGHT:END -->

## Agent Notes
Built the fix: fill_in_hint() in envfile.py names every required_any group as 'at least one of A, B' on the missing-.env path, keeping '(no keys declared)' for the honest-empty case; two committed tests, RED pre-fix / GREEN post-fix, 55 passed, 12 production lines.

PARENT VERDICT: ACCEPTED. probes: wire (live CLI reaches fill_in_hint on the missing-.env path, both alternatives named, no "(no keys declared)"); gate (empty node still yields "(no keys declared)"); gate (mixed keys+two-groups case names every group). 55 passed in test_envfile.py. Caveat: envfile.py:587 ok-line still under-reports groups, outside this claim.
