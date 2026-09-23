---
id: experiment:a00-80ab4cd5-dc9f32
mint_id: 52b5d275e7b3410da0015a353a167d5b
type: experiment
parents:
  - hypothesis:secrets-error-own-type-and-hook-reads-graph-secrets-node
next_edges: []
confidence: 0.9
edited_by: a00-88ea6269
evidence_runs:
  - experiment:a00-80ab4cd5-dc9f32
loop: hypothesis:secrets-error-own-type-and-hook-reads-graph-secrets-node@s2
model: deepseek/deepseek-v4.1-flash
production_lines: 12
profile: balanced
role: kid
scaffold_hash: 306c4e458c1fc152
season: 2
title: SecretsError own type + anonymize hook resolves the graph secrets node
town: core
verdict: proved
---
<!-- BODY:BEGIN -->
# experiment:a00-80ab4cd5-dc9f32

## Experiment

Claim (goal:g15.29.16): after the fix a malformed `required_any` raises a
`SecretsError` that is **not** a `ValueError`, and `anonymize.py check --root
<repo root>` refuses text carrying a declared key's env value.

Pre-fix state (measured, files read on this worktree):

| seam | pre-fix byte | defect |
|---|---|---|
| `envfile.py:121` | `class SecretsError(ValueError)` | own type widened to `ValueError`; any unrelated `except ValueError` swallows it |
| `test_envfile.py:839` | `pytest.raises(ValueError, ...)` | the test encoded the wrong contract |
| `anonymize.py:25` | `node = Path(root) / SECRETS_NODE` | hook passes `--root = source_root` (repo root); node lives at `<repo>/.agi/nodes/...` -> not found -> ZERO secret values checked |

## Changes

1. `envfile.py` — `class SecretsError(Exception)`, docstring states it is its own type.
2. `anonymize.py` `_secret_tokens` — resolve the graph root (`locations.shared_project_root(root) or locations.find_project_root(root)`) instead of assuming `root` is the graph root.
3. `test_envfile.py` — M1 residue flipped: `pytest.raises(agi_secrets.SecretsError)` plus `assert not isinstance(exc.value, ValueError)`.
4. `test_anonymize_guard.py` — new test (8): graph with `required_keys: [FIXTURE_GUARD_KEY]`, env value, `--root` = the repo root; `_secret_tokens`, `scan`, and `cmd_check` all find/refuse the `secret` class.

Production lines: 12 added / 2 removed (envfile.py 5/1, anonymize.py 7/1).

## Evidence

Red on pre-fix bytes (both new/changed assertions fail, 2 failed / 65 passed):

```
FAILED test_anonymize_guard.py::test_check_from_repo_root_refuses_declared_key_value
  AssertionError: assert ('secret', 'sk-fake-guard-value') in []
FAILED test_envfile.py::test_malformed_required_any_entry_is_refused_by_name
  AssertionError: SecretsError must be its own type, not a ValueError
```

Green after the fix, named files only (`env -u TMUX -u TMUX_PANE`):

```
extensions/agi/tests/test_anonymize_guard.py extensions/agi/tests/test_envfile.py -> 67 passed
```

Neighbouring consumers green: `test_provisioning.py test_verification.py` pass
(157 passed in the combined run; the one `test_dispatch_forward_env.py`
failure is environmental and pre-existing — `TYPESAFE_KEY` is in this kid's
spawn `os.environ`, asserted absent before any code of mine runs).

## Falsifiers checked

- new committed test green on pre-fix bytes -> **no**, both red (above)
- named test files red after the fix -> **no**, 67 passed
- change outside FILE SCOPE -> **no**, only `envfile.py`, `anonymize.py`, their two tests
- fixture values only, no real secret printed -> **yes**, fake `sk-fake-guard-value`

<!-- BODY:END -->

## Agent Notes
SecretsError is now its own Exception (not ValueError); anonymize._secret_tokens resolves the graph root so the installed hook reads <repo>/.agi/nodes/.geometry/secrets.md; both committed tests red on pre-fix bytes (2 failed), green after (67 passed).

<!-- THOUGHT:BEGIN — authored, not derived; carried across regenerating scans. The reasoning behind THIS version. -->
Parent review EF.72 a00-88ea6269. Diff de78c4e52b..510d2aa1f9 read as bytes (envfile.py, anonymize.py, the two named tests, this node). Verdict stays proved, on two parent-run probes. Conjunct 1 (gate): SecretsError is now `Exception`, so `except ValueError` no longer swallows a malformed-required_any refusal; pre-fix bytes (git show de78c4e52b:envfile.py) show issubclass(SecretsError, ValueError)=True, i.e. red. Conjunct 2 (wire): the exact invocation cmd_install_hook writes (`anonymize.py check --root <source_root>`) now refuses a declared key's env value -- fixture repo outside any git repo, graph secrets node with required_keys=[FIXTURE_GUARD_KEY], rc=1 class `secret`; control with no value rc=0, --root graph root rc=1, undeclared value rc=0. Pre-fix the same call read <repo>/nodes/.geometry/secrets.md, found nothing, rc=0. Blast radius checked: only bin/envfile.py references SecretsError; provisioning.py and boxes.py wrap envfile.resolve in `except Exception`, so widening the base from ValueError to Exception cannot escape them. Named suite green on tip: 67 passed under env -u TMUX -u TMUX_PANE.
<!-- THOUGHT:END -->

PARENT REVIEW EF.72 (a00-88ea6269) -- ACCEPTED, verdict proved unchanged. Both claim conjuncts reproduced with parent-run negative probes; both tests red on the pre-fix bytes and green on the tip.

probes: [{"conjunct":1,"class":"gate","cmd":"raise SecretsError through the malformed required_any branch; import base and tip envfile","expected":"refused as SecretsError, NOT caught by except ValueError","observed":"tip issubclass(SecretsError,ValueError)=False and the branch landed in except SecretsError; base issubclass=True","result":"HOLD (base red)"},{"conjunct":2,"class":"wire","cmd":"anonymize.py check --root <repo root> --text <declared key env value> in a /tmp fixture repo (graph .agi/nodes/.geometry/secrets.md required_keys=[FIXTURE_GUARD_KEY], .env value), fixture-only","expected":"rc=1, class secret","observed":"tip rc=1 REFUSED secret; control no-value rc=0, --root graph-root rc=1, undeclared value rc=0; base bytes rc=0","result":"HOLD (base red)"}]

Falsifiers checked: new tests green on pre-fix bytes -> NO (both red); named files red after fix -> NO (67 passed); change outside FILE SCOPE -> NO (only envfile.py, anonymize.py, their two tests, this node). No caller/suite outside those files references SecretsError. HAZARD held: fixture values only, no real secret printed.
