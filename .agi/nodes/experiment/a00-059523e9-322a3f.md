---
id: experiment:a00-059523e9-322a3f
mint_id: 85f001fa97ee424eac527a1353f173cf
type: experiment
parents:
  - hypothesis:every-secrets-reader-honours-required-any
next_edges: []
confidence: 0.9
edited_by: a00-e52c165c
evidence_runs:
  - experiment:a00-059523e9-322a3f
loop: hypothesis:every-secrets-reader-honours-required-any@s2
model: deepseek/deepseek-v4.1-flash
probes:
  - {"conjunct": 1, "class": "gate", "cmd": "python3 <scratch>/probes.py A1-A5 (fixture secrets node + fixture .env, real anonymize._secret_tokens)", "expected": "required_any-only keys collected; declared shared key collected once; undeclared key not collected; absent group key tolerated", "observed": "A1-A5 PASS: [sk-fake-a,sk-fake-b,sk-fake-shared]; sk-fake-x absent; absent key no crash", "result": "held"}
  - {"conjunct": 2, "class": "gate", "cmd": "probes.py B: hand envfile.resolve a bare string, [list,123], empty list, dict, single-char string, then a well-formed cell", "expected": "each malformed entry refused by ValueError naming the entry; well-formed cell NOT refused", "observed": "5/5 malformed refused with entry repr in message; well-formed [[GROUP_A,GROUP_B]] returned unchanged", "result": "held"}
  - {"conjunct": 3, "class": "wire", "cmd": "probes.py C: real schema_registry.load_schemas_from_dir(<root>/.agi/context/schemas) + validate_nodes_against_registry on a config node", "expected": "required_any of wrong type is a live type error on that field; a list passes", "observed": "wrong type -> (types,required_any); list -> no required_any error", "result": "held"}
  - {"conjunct": 4, "class": "gate", "cmd": "probes.py D: repaired test node (required_keys + required_any group) driven through resolve+check", "expected": "a satisfied group still reports the missing required key; a present required key still reports the unsatisfied group naming both keys", "observed": "both problems named as expected -> the repaired test is load-bearing, not vacuous", "result": "held"}
  - {"conjunct": 5, "class": "gate", "cmd": "red_prefix.py: materialize pre-fix bytes from git 73a0e3cbf9 and run D1/D2", "expected": "required_any-only key absent from the pre-fix denylist; malformed entry silently dropped", "observed": "D1 pre-fix RED -> empty; D2 pre-fix RED -> required_any=[]", "result": "held"}
production_lines: 22
profile: balanced
role: kid
scaffold_hash: 5157ef5a0346fd3b
season: 2
title: "Every secrets reader honours required_any: anonymize denylist, envfile refusal, schema cell, repaired test"
town: core
verdict: proved
---
<!-- BODY:BEGIN -->
# experiment:a00-059523e9-322a3f

## Experiment

BUILD ORDER (g15), not a measurement: implemented the four EF.59 deliverables and
proved each test RED on the pre-fix bytes, GREEN after. Fixture nodes and
fixture values (sk-fake-…) only; this box's `.env`/environment never read.

| # | Deliverable | Production bytes | Red test | Green |
|---|---|---|---|---|
| D1 | `anonymize._secret_tokens` flattens every group under `required_any` too | `anonymize.py` +5 | `test_secret_tokens_reads_required_any_groups` | passes |
| D2 | `envfile.Resolution` REFUSES a malformed `required_any` entry by name (`SecretsError`, now a `ValueError`) | `envfile.py` +15/-7 | `test_malformed_required_any_entry_is_refused_by_name` | passes |
| D3 | `[config]` schema declares `required_any` in fields + validation.types | `[config].md` +2 | `test_config_schema_declares_required_any` | passes |
| D4 | repaired `test_required_keys_still_enforced_alongside_required_any` to a node declaring BOTH cells | test only | both assertions fail against the old vacuous node (probe) | passes |

D1 does NOT change the public signature. D2 keeps a well-formed group
unchanged and names the offending entry via its `repr` in the message. D3 adds
two lines beside the three sibling env fields, no reorder.

## Evidence

RED (pre-fix), `pytest test_anonymize_guard.py test_envfile.py -q -k "required_any or config_schema_declares_required_any or required_keys_still_enforced"`:

```
FAILED test_anonymize_guard.py::test_secret_tokens_reads_required_any_groups
E   assert ('secret', 'sk-fake-required-any-only') in []
FAILED test_envfile.py::test_malformed_required_any_entry_is_refused_by_name
E   Failed: DID NOT RAISE ValueError
FAILED test_envfile.py::test_config_schema_declares_required_any
E   AssertionError: missing fields-block entry
3 failed, 6 passed, 57 deselected
```

D4 RED probe (`.agi/sessions/iter-EF.59/a00-059523e9/d4_red_probe.py`) runs the
new interaction assertions against the OLD vacuous node (DEFAULT_NODE, no
group): `assertion1 = False`, `assertion2 = False`, `D4 RED = True` — i.e. the
old test measured nothing.

GREEN (post-fix):

```
$ pytest extensions/agi/tests/test_envfile.py extensions/agi/tests/test_anonymize_guard.py -q
66 passed in 1.70s
$ pytest test_provisioning.py test_shared_state_worktree.py test_box_guard.py -q
106 passed, 5 skipped
```

Production lines (`git diff --numstat`): anonymize.py +5, envfile.py +15/-7,
[config].md +2 = **22 added**, under the 40 ceiling.

<!-- THOUGHT:BEGIN — authored, not derived; carried across regenerating scans. The reasoning behind THIS version. -->
Parent review EF.59 a00-e52c165c, accepted proved. (1) The brief said: every secrets reader honours required_any, each conjunct proved by a test red on the pre-fix bytes. (2) The machine: the diff at 8e1ef136b1 carries all four named deliverables, and I ran my own probes (probes.py, 15 checks) plus a red-on-prefix run (red_prefix.py) against bytes materialized from 73a0e3cbf9 — pre-fix _secret_tokens returned [] for a required_any-only key and pre-fix resolve silently produced required_any=[]. Probe C used the real schema_registry validator, and it refuses a wrong-typed required_any by field, so the schema cell is live and not mere text. (3) Near miss: a kid could have made _secret_tokens read required_any while leaving envfile silently dropping the malformed entry, and its own suite would be green while the fail-open defect survived; the gate probe for conjunct 2 is what rules that out. The one judgement call I accept is SecretsError(ValueError): it satisfies the ValueError assertion and keeps except SecretsError catching it; no caller wraps envfile.resolve in a bare except ValueError, so nothing new is swallowed. (4) Deviation from the standing rule that a kid node stays the kid-authored region: this version is the parent review, and the probes recorded here are the parent own negative probes, exactly as the tier-parent gate requires.
<!-- THOUGHT:END -->

## Agent Notes
D1 anonymize._secret_tokens flattens required_any groups; D2 envfile refuses a malformed required_any entry by name (SecretsError->ValueError, message carries repr); D3 [config] schema declares required_any in fields+validation.types; D4 repaired test declares both cells and both assertions fail against the old vacuous node. 3 red pre-fix, all green: test_envfile.py+test_anonymize_guard.py 66 passed, test_provisioning/shared_state/box_guard 106 passed, test_verification 126 passed total. 22 production lines, fixture values only.

PARENT REVIEW EF.59 a00-e52c165c (ACCEPTED, verdict proved): diff read against merge-base 73a0e3cbf9 — anonymize.py +5 collects required_any groups into _secret_tokens; envfile.py +15/-7 raises SecretsError(ValueError) naming a malformed group instead of dropping it; [config].md +2 declares required_any in fields and validation.types; test_envfile.py +78 repairs the ~775 test to BOTH_NODE (required_keys + a real group) and adds the malformed-refusal + schema tests; test_anonymize_guard.py +33 drives the real _secret_tokens. 5 parent probes ran and all held (gate x4, wire x1), including a red-on-prefix run proving the required_any key was absent from the pre-fix denylist and the malformed cell was silently dropped. No deliverable named by the kid is missing from the diff. One judgement call accepted: SecretsError widened to ValueError (satisfies the test while keeping except SecretsError working); no caller wraps envfile.resolve in a bare except ValueError.
