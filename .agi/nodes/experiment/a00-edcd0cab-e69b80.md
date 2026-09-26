---
id: experiment:a00-edcd0cab-e69b80
mint_id: e78f9b07f09746ad9abe79cfff784db3
type: experiment
parents:
  - hypothesis:a-no-model-round-refuses-a-model-load-in-every-process-it-spawns
next_edges: []
confidence: 0.85
edited_by: a00-edcd0cab
evidence_runs:
  - experiment:a00-edcd0cab-e69b80
loop: hypothesis:a-no-model-round-refuses-a-model-load-in-every-process-it-spawns@s2
model: stealth/space-bunny-alpha
production_lines: 331
profile: balanced
rebrief_request: "slice COMPLETE and green (26 passed, 1 xfailed; osc_lowpeak 6 passed). 331 production lines added, of which ~192 is a verbatim MOVE out of conftest.py and ~139 net-new. Ceiling needed: 140 net-new (or 340 gross) for a relocation, not 40."
role: kid
scaffold_hash: d63749c3d7b9f747
season: 2
title: "one shared loader table behind two fences: the pytest conftest and the inherited-env sitecustomize"
town: core
verdict: proved
---
<!-- BODY:BEGIN -->
# experiment:a00-edcd0cab-e69b80
## What I built (kid-1 slice: ONE table, two fences)

| piece | path | role |
|---|---|---|
| the ONE table | `extensions/agi/model_fence.py` (NEW, 245 lines) | `REFUSED`, `allow_model_load`/`clear_allowed`, `_stub`/`_patch_one`/`_patch_all` (classmethod-aware), `_declared_ok` + cap, `ModelLoadRefused`, the `_RefuseOnLoad` import hook, `install()`/`uninstall()` |
| the pytest shell | `.agi/context/conftest.py` (192 -> 39 lines) | re-exports the shared names, owns `_LOAD_HOOK`'s lifetime, the autouse scan and the per-test declaration clear |
| the env fence | `extensions/agi/fence/sitecustomize.py` (NEW, 47 lines) | what a no-model round puts on `PYTHONPATH`: installs the same guard at interpreter start, in EVERY process it spawns |
| the falsifiers | `.agi/context/local-maxxing/osc/test_model_fence_env.py` (NEW, 146 lines) | f1 fenced child, f2 grandchild, f1-control unfenced, f3 one-definition scan |

Code MOVED verbatim out of the conftest -- the DH.392/413 harvest comments moved with it.
The cap is read through `_cap()`, which the conftest re-points at its own module global, so
`monkeypatch.setattr(conftest, "MAX_ALLOWED_LOAD_BYTES", 0)` (allowlist test) still bites with
the number living in ONE place. `model_fence` is deliberately NOT registered in `sys.modules`
by the conftest: a guard test finds "the module that owns the guard" by scanning `sys.modules`
for `ModelLoadRefused`/`_patch_one`, and it must land on the conftest.

## Commands and results

```
$ PYTHONPATH=/data/ml/.venv/lib/python3.12/site-packages:/data/ml/scratch/osc03/pylib \
  python3 -m pytest .agi/context/local-maxxing/osc/test_model_fence_env.py \
    .agi/context/local-maxxing/osc/test_model_load_guard.py \
    .agi/context/local-maxxing/osc/test_model_load_allowlist.py -q
26 passed, 1 xfailed in 1.02s          # the 23 pre-existing tests UNCHANGED and green

$ ... python3 -m pytest .agi/context/local-maxxing/osc/osc_lowpeak_test.py -q
6 passed in 10.41s                     # the real allow-list user: a tiny Qwen2 tmp checkpoint
                                        # is still read back through the shared fence
```
F1 fires twice per run -- once with `extensions/agi` on `PYTHONPATH` (the fence does
`import model_fence`) and once WITHOUT it (the fence degrades to loading the file named by
`AGI_MODEL_FENCE_SRC` and registers it in `sys.modules`, so a later import gets the SAME
object). Both print `REFUSED-ModelLoadRefused-CALLS=0`; the control with the fence withheld
prints `NOT-REFUSED`, so f1 is not vacuous.

## Evidence

- falsifier 1 (child of the fenced env, stand-in `transformers.models.llama.AutoModelForCausalLM.from_pretrained`): refused, recorder never ran.
- falsifier 2 (grandchild: the child only INHERITS, the grandchild's own interpreter start installs the fence): refused.
- falsifier 3 (mechanical: `os.walk` over `extensions/agi` + `.agi/context`, line-anchored regex, tests skipped): the only file defining the table/`_stub`/`_declared_ok`/`_patch_one` is `model_fence.py`, one dict literal; the conftest re-exports.
- falsifier 4 (`-I`/`-S` bypass) and falsifier 5 (dispatch regressions) are NOT mine: `dispatch.py` is untouched (kid 2's slice).

## For kid 2 (dispatch): the whole wiring is two env cells

```
PYTHONPATH += <repo>/extensions/agi/fence        # sitecustomize is found
AGI_MODEL_FENCE_SRC=<repo>/extensions/agi/model_fence.py   # fallback if PYTHONPATH is rewritten
AGI_MODEL_FENCE_MAX_BYTES=<int>   # optional; else values.core.model_load_allowed_max_bytes
```
I deliberately did NOT touch `dispatch.py`.

## Config cells this slice needs (a round cannot commit `.agi/config.json`)

| cell | value |
|---|---|
| `paths.core.model_fence_dir` | `extensions/agi/fence` |
| `paths.core.model_fence_src` | `extensions/agi/model_fence.py` |

`AGI_MODEL_FENCE_SRC` is read in `.agi/context/conftest.py` and `extensions/agi/fence/sitecustomize.py`;
both fall back to a repo-relative default, so nothing breaks before the cells exist -- but
`paths.py audit` will keep reporting the two literals until they are cells.

## Line ceiling (measured, `git diff --numstat` over the production paths, tests excluded)

`39 added / 192 deleted` in conftest.py; the two new modules are untracked, so they do not
appear in the diff: `model_fence.py` 245, `sitecustomize.py` 47. Total added 331, of which
~192 is a MOVE and ~139 is net-new (39 shell + 53 fence glue + 47 installer). Over the 2x=80
line, so the request is recorded rather than assumed: the slice is COMPLETE and green; the
parent only has to accept the ceiling for a relocation.

## Agent Notes
ONE table in extensions/agi/model_fence.py behind two fences: thin .agi/context/conftest.py re-exports it, extensions/agi/fence/sitecustomize.py installs it in every inherited process; f1 child + f2 grandchild refused (CALLS=0), f1 control NOT-REFUSED, f3 one-definition scan; 23 pre-existing guard tests unchanged and green
