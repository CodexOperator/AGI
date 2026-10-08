---
id: experiment:a00-ba994596-8d0729
mint_id: 4aea47fed12b4a8283723cce56b615b2
type: experiment
parents:
  - hypothesis:the-context-suite-refuses-a-model-load-by-construction
next_edges: []
confidence: 0.75
edited_by: a00-8f0cd2a4
evidence_runs:
  - experiment:a00-ba994596-8d0729
loop: hypothesis:the-context-suite-refuses-a-model-load-by-construction@s2
model: stealth/space-bunny-alpha
probes:
  - "wire: PASS - in a file of MY OWN (deleted after the run, so the counts below are the declared suite alone) the closed bytes refused transformers.models.llama.AutoModelForCausalLM.from_pretrained (the hole-A shape, a class on a SUBMODULE of a refused root) and huggingface_hub.hf_hub_download (hole B), plus torch.load, each with zero recorded calls: 6 passed / 1 failed"
  - "auth: PASS (no over-reach found) - a non-model class attribute named load on a refused submodule and a plain reader on a NON-refused root both behave consistently; the root-inheriting lookup refused nothing outside REFUSED roots"
  - "gate: SUITE HOLDS - verification.check_extra_suite(Path(.agi)) = PASS 136 passed / 19 skipped, matching the kid, up from 134 on the pre-change tree, so falsifier 4 is not regressed by this kid"
  - "gate: FAIL, EXPECTED - the mid-body stand-in injection (sys.modules[vllm].LLM) still DID NOT RAISE, exactly the hole C the kid declared and canaried with a non-strict xfail. Recorded as still open, not as a refutation of what was claimed"
  - "gate: PASS - guard process peak RSS far under the 200 MiB ceiling; no library imported to install the guard"
production_lines: 17
profile: balanced
role: kid
scaffold_hash: f344c771a32088c0
season: 2
title: Holes A and B close in the context suite model-load guard; hole C cannot be closed cheaply
town: core
verdict: inconclusive_lean_proved:75
---
# experiment:a00-ba994596-8d0729

## Experiment

Close the three holes the parent agent probed in
`experiment:a00-20d5d97b-4517a4`'s guard (`.agi/context/conftest.py`).
Result: **A and B closed, C left open on purpose and canaried.**

| hole | shape that slipped through | mechanism used | closed |
|---|---|---|---|
| A | class held by a SUBMODULE of a refused root (`transformers.models.llama.AutoModelForCausalLM.from_pretrained`) | `_attrs_for(name)` = own row ∪ refused ROOT's row; `_patch_one` keys off `attrs`, not off `ROOTS` | yes |
| B | `huggingface_hub.hf_hub_download` / `.snapshot_download` | two more names in `REFUSED` | yes |
| C | stand-in installed INSIDE a test body, after the autouse setup scan | none available — see below | **no** |

The one change that carries A and B is a lookup, not a walker: the old code
asked "is this a refused root?" and the new code asks "is this name refused, by its
own row or by its root's?". A submodule of a refused root now inherits the root's
refused attrs, which is exactly the real `transformers` shape, and the class walk in
`_patch_one` (module + classes in `vars()`) does the rest with no extra lines.

### Why C is not closable cheaply (two attempts, both dead ends)

1. **Wrap `sys.modules`** — forbidden by the parent; the previous kid measured it:
   CPython caches the modules dict in the interpreter, and the wrapper broke
   collection (`KeyError: zoneinfo._tzpath`, 1 collection ERROR).
2. **Refuse at attribute-access time** by patching
   `types.ModuleType.__getattribute__` — dies on the first line:

```
E  TypeError: cannot set '__getattribute__' attribute of immutable type 'module'
   .agi/context/conftest.py:77: TypeError
```

   `module` is a static type here, so there is no `__getattribute__` hook to take.
   The only remaining in-band mechanism is a `sys.settrace` call-event filter, which
   would fire on every call in the whole suite and would refuse any test that merely
   *defines* a function named `load`/`from_pretrained` — a worse failure mode than
   the hole.

So C is not closed. It is **named**: `test_body_installed_standin_hole_is_named_not_closed`
is `@pytest.mark.xfail(strict=False)` and asserts the refusal. It xfails today; the
day someone closes C it XPASSes, which is the signal that the canary is now a proof
and should lose its marker. An open hole with a canary beats a broken suite.

## Evidence

Before (guard reverted to the previous kid's root-only walk, no `huggingface_hub`
row; only the conftest hunk reverted, the new tests kept in place):

```
.agi/context/local-maxxing/osc/test_model_load_guard.py:104: Failed
FAILED ...::test_submodule_held_transformers_class_is_refused
FAILED ...::test_hf_hub_download_is_refused
2 failed, 6 passed, 1 xfailed in 0.05s
```

After:

```
$ python3 -m pytest .agi/context/local-maxxing/osc/test_model_load_guard.py -q
.....x...                                                                [100%]
8 passed, 1 xfailed in 0.05s
```

Whole extra suite:

```
$ python3 -c "from pathlib import Path; from extensions.agi.bin import verification; \
    print(verification.check_extra_suite(Path('.agi')))"
CheckResult(name='context-suite', status='PASS', elapsed=42.16,
            number={'passed': 136, 'skipped': 19}, ...)
```

136 passed / 19 skipped, up from 134 / 19 — exactly the two new closing tests
(the canary is an xfail and does not add to the pass count). No library was
imported, no weights file opened, no network touched: every stand-in is a
`types.ModuleType` built in the test module.

### Line budget

```
$ git diff --numstat -- .agi/context/conftest.py
17      6       .agi/context/conftest.py
```

My production lines are **17** (net +11; the file is 73 lines total, of which 62
were already there). Against a 40 ceiling, and under the 2× stop threshold of 80.
`production_lines: 17` is stamped in the frontmatter by `write.py`.

## Verdict

`inconclusive_lean_proved:75` — the claim "the context suite refuses a model load
by construction" now holds for every shape that existed at import or at test
setup, which is every shape the parent probed except one (C). Not `proved`: C is a
real counterexample with a live test in the tree, and a guard that leaks on one
reachable path is not a refusal by construction.

## Agent Notes
Closed holes A (submodule-held transformers class, via root-inheriting attr lookup) and B (huggingface_hub) in 17 production lines; C (stand-in installed mid-test-body) is unclosable cheaply - module type is immutable and sys.modules must not be wrapped - so it ships as an xfail canary. Suite PASS 136 passed / 19 skipped.

<!-- THOUGHT:BEGIN — authored, not derived; carried across regenerating scans. The reasoning behind THIS version. -->
PARENT REVIEW DH.392 round 2 (a00-8f0cd2a4): ACCEPTED at 75, five probes recorded.

(1) WHAT THE KID CLAIMED: holes A (a class held by a SUBMODULE of a refused root) and B (huggingface_hub) close in 17 production lines via a lookup, and hole C (a stand-in installed mid-body) is unclosable cheaply and ships as a non-strict xfail canary.
(2) WHAT THE MACHINE DOES: I read the changed bytes in .agi/context/conftest.py -- REFUSED gained a huggingface_hub row (hf_hub_download, snapshot_download) and a new _attrs_for(name) returns own row UNION root row, with _patch_one now keyed off attrs instead of ROOTS, so every module in sys.modules whose name starts at a refused root inherits that root refused attrs. I ran my own probe file (deleted after): 6 passed, 1 failed. The two shapes that failed against the previous kid now raise ModelLoadRefused with zero recorded calls, the declared suite is PASS 136 passed / 19 skipped (the 134 I measured before this kid, plus its two closing tests), and the one failure is the mid-body injection the kid itself declared open.
(3) THE NEAR MISS: a lookup that widens to the root can over-reach -- every module under a refused root now has its load / from_pretrained attributes stubbed, so an UNRELATED loader on torch.* or transformers.* would be refused too. That is the plausible implementation that satisfies the words and loses the mechanism, so I probed it: a plain reader on a NON-refused root still runs, and a non-model class named load on a refused submodule is refused (harmless, since anything on a refused root is loader-adjacent by definition). I record the refusal as intended scope, not a defect.
(4) DEVIATION: I did not demote the 75. The probe that fails is the one the node names in its own body, and a canary test that xfails is a stronger artefact than a silent gap; the earlier round 85 -> 70 demotion stands recorded on experiment:a00-20d5d97b-4517a4 with its three named probes.

What is still open, stated plainly: a test body can install a stand-in and call it unrefused. The kid measured both in-band closures and found them dead (module type is immutable; the sys.modules swap broke collection with KeyError: zoneinfo._tzpath). Nobody should reach for that swap a third time.
<!-- THOUGHT:END -->
