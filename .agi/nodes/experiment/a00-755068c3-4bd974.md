---
id: experiment:a00-755068c3-4bd974
mint_id: fd8ba739046d4ecdb5679ceb7f86959c
type: experiment
parents:
  - hypothesis:envfile-required-any-lets-either-openrouter-key-satisfy-secrets
next_edges: []
confidence: 0.95
edited_by: a00-2d5c90ea
evidence_runs:
  - experiment:a00-755068c3-4bd974
loop: hypothesis:envfile-required-any-lets-either-openrouter-key-satisfy-secrets@s2
model: deepseek/deepseek-v4.1-flash
probes:
  - {"conjunct": "required_any absent means no groups (no invented refusal)", "class": "gate", "cmd": "node with NO required_any cell, env has neither OpenRouter key -> envfile.check(res)", "expected": "required_any == [] and no group problem", "observed": "required_any == [] and problems does not mention either key", "result": "held"}
  - {"conjunct": "a group is satisfied by any one key present non-empty", "class": "gate", "cmd": "OPENROUTER_API_KEY=   (whitespace only), OPENROUTER_PROVISIONING_KEY unset -> check(res)", "expected": "problem naming OPENROUTER_PROVISIONING_KEY (whitespace counts absent)", "observed": "problem: none of OPENROUTER_API_KEY, OPENROUTER_PROVISIONING_KEY is set", "result": "held"}
  - {"conjunct": "a group with none present is a PROBLEM naming every key", "class": "gate", "cmd": "neither OpenRouter key set -> check(res)", "expected": "problem naming BOTH OPENROUTER_API_KEY and OPENROUTER_PROVISIONING_KEY", "observed": "one problem naming both keys", "result": "held"}
  - {"conjunct": "required_keys stays enforced as before", "class": "gate", "cmd": "required_keys=[MANDATORY_KEY] + required_any group; env has only the group key -> check(res)", "expected": "problem naming MANDATORY_KEY while the group is satisfied", "observed": "MANDATORY_KEY is missing or empty; no group problem", "result": "held"}
  - {"conjunct": "only OPENROUTER_PROVISIONING_KEY set -> the secrets check passes", "class": "wire", "cmd": "envfile.main([fixture, --check]) with only OPENROUTER_PROVISIONING_KEY; and with neither key", "expected": "exit 0 with provisioning only; exit 1 with neither", "observed": "exit codes (0, 1)", "result": "held"}
production_lines: 15
profile: balanced
role: kid
scaffold_hash: 66abf30ffe3b1aa2
season: 2
title: "envfile.py reads required_any: either OpenRouter key satisfies the secrets check, neither fails naming both"
town: core
verdict: proved
---
<!-- BODY:BEGIN -->
# experiment:a00-755068c3-4bd974

## Experiment

BUILD ORDER (g15): implement `required_any` in `extensions/agi/bin/envfile.py`
and prove it with committed tests that are red on the pre-fix bytes.

### What was broken (verified before editing)

- `.agi/nodes/.geometry/secrets.md` carries
  `required_any: [[OPENROUTER_API_KEY, OPENROUTER_PROVISIONING_KEY]]` and
  `required_keys: []`.
- `envfile.py` read neither: `grep -n required_any extensions/agi/bin/envfile.py`
  returned nothing. `check()` walked `required_keys` only, so `--check` passed
  with NEITHER OpenRouter key set.

### The change (envfile.py, 15 production lines)

| Where | Change |
|---|---|
| `Resolution.__init__` | read `required_any` as a list of groups (`res.required_any`); absent cell -> `[]` |
| `Resolution.as_dict` | expose `required_any` |
| `check()` | after the `required_keys` loop: one problem per group with no key present non-empty, naming every key in the group |

A group is satisfied when ANY key is present with a non-empty value;
`.strip()` makes an empty/whitespace-only value count as absent.
`required_keys` is unchanged. No value is ever printed — problems name keys
and lengths only.

### Tests added (test_envfile.py, 6)

1. `test_required_any_reads_the_groups`
2. `test_required_any_satisfied_by_provisioning_key_alone`
3. `test_required_any_satisfied_by_api_key_alone`
4. `test_required_any_with_neither_key_names_both`
5. `test_required_any_empty_value_counts_as_absent`
6. `test_required_keys_still_enforced_alongside_required_any`

All use the existing `make_project` / `write_node` / `write_env` fixtures with
`tmp_path` and fixture values only; no real secret is read or copied.

## Evidence

### RED before the fix (unmodified envfile.py)

```
$ python3 -m pytest extensions/agi/tests/test_envfile.py -q -k required_any
3 failed, 3 passed, 45 deselected
FAILED ...::test_required_any_reads_the_groups
FAILED ...::test_required_any_with_neither_key_names_both
FAILED ...::test_required_any_empty_value_counts_as_absent
```

Honest caveat: the two "either key passes" tests pass pre-fix **vacuously** —
the bug is that the cell is ignored, so a check that never reads a group finds
no group to fail. The discriminating red tests are the three above; the
neither-key test asserted `[]` problems where a group problem was required.
Full log: `.agi/sessions/iter-EF.43/a00-755068c3/red-before.txt`.

### GREEN after the fix

```
$ python3 -m pytest extensions/agi/tests/test_envfile.py -q
51 passed in 2.12s
$ python3 -m pytest extensions/agi/tests/test_verification.py -q
60 passed in 1.09s
```

### Hand check (fixture project under /tmp, outside the worktree so
`shared_project_root` cannot redirect to the main checkout)

```
$ envfile.py /tmp/ef43-fixture --check        # .env has only OPENROUTER_PROVISIONING_KEY
[secrets] ok: /tmp/ef43-fixture/.env satisfies required keys: (none declared)
exit=0

$ envfile.py /tmp/ef43-fixture --check        # .env has neither OpenRouter key
[secrets] PROBLEM: none of OPENROUTER_API_KEY, OPENROUTER_PROVISIONING_KEY is set in /tmp/ef43-fixture/.env — at least one is required
exit=1
```

Production lines: `git diff --numstat -- extensions/agi/bin/envfile.py` ->
`15  0  extensions/agi/bin/envfile.py` (ceiling 40).

## Struggle

A fixture placed under the worktree's own scratch dir resolves through
`locations.shared_project_root` / `git_common_root` to the MAIN checkout, not
the fixture — the first hand check silently read the real project's `.env` and
returned exit 0 for both cases. The fix is to put the hand-check fixture
outside any git repo (e.g. `/tmp`); it is a real trap for anyone hand-testing
this module inside a `--branch` worktree.


<!-- THOUGHT:BEGIN — authored, not derived; carried across regenerating scans. The reasoning behind THIS version. -->
Built the fix rather than measuring the defect. required_any is read in Resolution as a list of groups and check() adds one problem per unsatisfied group, naming every key with .strip() so empty/whitespace counts absent; required_keys keeps its own loop unchanged. 15 production lines, under the 40 ceiling. Three of six new tests are red on the pre-fix bytes (the two "either key passes" tests pass vacuously pre-fix because required_any was ignored: any check that does not read the cell finds no group to fail). No secret value is read or printed; fixture values only.
<!-- THOUGHT:END -->

## Agent Notes
envfile.py now reads required_any (list of groups): a group passes when any key is non-empty (strip), an unsatisfied group is a problem naming every key; required_keys unchanged. 6 tests added, 3 red pre-fix (groups-read, neither-names-both, empty-as-absent); test_envfile.py 51 passed, test_verification.py 60 passed; hand check exit 0 with only provisioning key and exit 1 naming both with neither; 15 production lines under the 40 ceiling.

PARENT REVIEW (a00-2d5c90ea, EF.43): ACCEPTED at proved. Read the bytes, not the result file: HEAD 3402a5126 carries exactly 15 production lines in envfile.py (Resolution reads required_any as a list of groups; check() adds one problem per unsatisfied group naming every key with .strip(); required_keys loop unchanged) and 84 lines of tests; nothing else. Re-ran the suite myself against the pre-fix bytes in a scratch tree (HEAD~1:envfile.py): the 3 discriminating tests are RED (groups-read AttributeError, neither-names-both, empty-as-absent) and green after — the kid honestly flags that the two either-key tests pass vacuously pre-fix. Negative probes recorded in frontmatter, one per conjunct (4 gate, 1 wire), all held: required_any absent invents nothing; whitespace counts absent; neither names BOTH; required_keys still enforced while a group is satisfied; CLI --check exits 0 with provisioning alone and 1 with neither. KID CAVEATS (do not block): (1) a malformed group entry that is not a list (e.g. required_any: ["OPENROUTER_API_KEY"]) is SILENTLY DROPPED — a mis-shaped cell fails open; the node contract is list-of-lists, and no test pins the refusal. (2) the kid left its own node and code uncommitted at done-time; the loop auto-commit (3402a5126) landed them, so nothing was hand-landed by me. (3) DISPLAY DEFECT in dispatch dry-run: the --orders carry-forward text does not print in the dry-run tail (the addendum IS present in the assembled brief, verified by direct call), so a parent cannot eyeball its own orders before paying for the spawn.
