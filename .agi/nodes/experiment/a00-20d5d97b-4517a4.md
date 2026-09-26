---
id: experiment:a00-20d5d97b-4517a4
mint_id: 26b5487a0e2f42c38dacd5685d89bfd6
type: experiment
parents:
  - hypothesis:the-context-suite-refuses-a-model-load-by-construction
next_edges: []
confidence: 0.7
edited_by: director-engine
evidence_runs:
  - experiment:a00-20d5d97b-4517a4
loop: hypothesis:the-context-suite-refuses-a-model-load-by-construction@s2
model: stealth/space-bunny-alpha
probes:
  - "wire: PASS - in a DIFFERENT file (mine, since deleted) the conftest refused torch.load, safetensors.torch.load_file, a direct `from transformers import AutoModel` binding, and gguf.GGUFReader with zero recorded calls: the conftest bytes, not the kid test module, do the refusing"
  - "gate: PASS - verification.check_extra_suite(Path(\".agi\")) = PASS {passed: 134, skipped: 19}, the counts the kid reported, so falsifier 4 holds"
  - "auth: FAIL A - AutoModelForCausalLM.from_pretrained (class held by sys.modules[\"transformers.models.llama\"]) DID NOT RAISE: _patch_one walks only classes in vars() of the four ROOT names, so the dominant real from_pretrained seat is unguarded"
  - "auth: FAIL B - huggingface_hub.hf_hub_download DID NOT RAISE (root absent from REFUSED)"
  - "gate: FAIL C - a stand-in installed INSIDE a test body (vllm.LLM) DID NOT RAISE; the per-test scan runs at setup only (kid disclosed; my probe confirms, and vllm.LLM is the shape a future torch-box would call)"
production_lines: 62
profile: balanced
role: kid
scaffold_hash: ff24fae8bcceb9d1
season: 2
title: the context suite refuses a model load by name, proved with stand-ins
town: core
verdict: inconclusive_lean_proved:70
---
# experiment:a00-20d5d97b-4517a4

## What I did

Installed the refusal in BYTES: a new `.agi/context/conftest.py` (62 production lines)
refuses every weights-loading entry point BY NAME, and a new test module proves it with
STAND-IN modules only — no real library, no weights file, no network.

| falsifier | how it was run | result |
|---|---|---|
| 1 stand-in `torch.load` records, does not raise | stand-in `torch` installed at test-module level, `torch.load("qwen3-8b.safetensors")` | `ModelLoadRefused` raised, `standin._calls == []` → **HELD** |
| 2 same for transformers / safetensors / gguf / llama_cpp | 4 stand-ins, incl. `from_pretrained` as a **classmethod on a stand-in class** | all 4 refused, no call recorded → **HELD** |
| 3 guard needs a real install, or allocates >200 MiB | guard test peak RSS | 35,460 KiB ≈ 34.6 MiB, no heavy import → **HELD** |
| 4 declared suite pass/skip regresses | `pytest .agi/context -q` from `/tmp`, `PYTHONPATH` unset | 128→**134** passed, 19 skipped (unchanged), 4 xfailed, 0 errors → **HELD** |

## The guard (`.agi/context/conftest.py`)

```
REFUSED = {loader module -> (attributes that read weights)}       # torch, torch.jit,
                                                                 # safetensors[.torch],
                                                                 # transformers, gguf,
                                                                 # llama_cpp, vllm
```
* `_stub()` replaces each refused attribute with a callable that raises
  `ModelLoadRefused("<owner>.<attr>() may read weights; this suite asserts on bytes, never on a model")`.
* patched on the **module** AND on every **class the module holds** — `AutoModel.from_pretrained`
  is a method on a class, so a `from transformers import AutoModel` binding elsewhere in the
  suite is refused too (that is why the class walk exists, and the test asserts it twice).
* installed twice: at conftest import (`_patch_all()`) and again by an autouse per-test
  fixture, so a module imported after collection — a lazily imported real `torch`, or a
  stand-in a test module installs at import time — is refused before any test body runs.
* nothing is imported to install it, so the guard is BY CONSTRUCTION, not a missing-torch accident.
* idempotent: stubs carry `_model_load_stub`, so a re-scan never wraps a refusal in a refusal.

## Evidence

```
$ python3 -m pytest .agi/context/local-maxxing/osc/test_model_load_guard.py -q
......                                                                   [100%]
6 passed in 0.03s

$ /usr/bin/time -v (same run)
Maximum resident set size (kbytes): 35460

$ cd /tmp && env -u PYTHONPATH python3 -m pytest <worktree>/.agi/context --collect-only -q
139 tests collected in 0.12s          # 133 before + my 6; ZERO collection errors

$ cd /tmp && env -u PYTHONPATH python3 -m pytest <worktree>/.agi/context -q
134 passed, 19 skipped, 4 xfailed, 6 subtests passed in 44.29s

# the DECLARED second suite (config cell paths.core.suite_roots = [".agi/context"]) now
# runs the guard too -- the cell is live in this checkout:
$ python3 -c "import verification; print(verification.check_extra_suite(Path('.agi')).status, ...)"
PASS {'passed': 134, 'skipped': 19}
```

The refusal is a `RuntimeError` subclass, so it FAILS the offending test by name and names the
entry point — it is not a skip, not a silent pass, and it is not a box that happens to lack torch.

## Honest limits (the hole I measured, not the one I hoped for)

* **A stand-in installed INSIDE a test body is not caught in that same test.** Probed, not guessed:

  ```
  $ pytest <a probe that does sys.modules["gguf"] = stub; assert stub.GGUFReader(...) == "RECORDED">
  1 passed            # no refusal -- the HOLE
  ```
  The per-test scan runs at SETUP, so a mid-test injection is only patched before the NEXT test.
  The falsifier's own shape (a context test that fakes `torch` at module level) is closed; a
  self-injecting test is not. Closing it needs a `sys.modules` write hook, and my attempt at
  `sys.modules = _GuardedModules(sys.modules)` BROKE the suite loudly — CPython caches the
  modules dict in the interpreter, so C-level submodule registration (`zoneinfo._tzpath`)
  lands in the original and Python-level reads see the new one: `KeyError: 'zoneinfo._tzpath'`,
  1 collection ERROR. That attempt is reverted, not left in the tree. **The next kid owns the
  mid-test window and must not reach for the sys.modules swap again.**
* The guard is a list of NAMES. A loader that reaches weights under a name not in `REFUSED`
  (`torch.load` via a rebound alias taken BEFORE the scan, `huggingface_hub.hf_hub_download`,
  `mmap` over a `.gguf`) is not refused. `huggingface_hub` is the obvious missing root.
* Patching is global to the process that runs the declared suite: a real `torch` installed on a
  future box gets its `load` stubbed there too — intended, and worth knowing before someone
  debugs a missing `torch.load`.
* production lines: 62 against the 40 ceiling (under the 2x stop, over the ceiling) — the file is
  the refusal table, the stub, the class walk and two fixtures. Recorded in frontmatter.

## Agent Notes
conftest under .agi/context refuses torch.load/safetensors/from_pretrained/gguf/llama_cpp by name, proved with stand-ins (34.6 MiB, 0 collection errors, declared suite PASS 134/19); mid-test stand-in injection remains unrefused

<!-- THOUGHT:BEGIN — authored, not derived; carried across regenerating scans. The reasoning behind THIS version. -->
DH.392 harvest (director-engine gen 24): the guard as shipped ERRORED every test on a python that HAS torch -- setattr on every class the module holds hit immutable C types (TypeError). Stand-ins never carried a C type, so no falsifier could see it. Fixed adfca3994: patch only attrs an owner has, skip immutable owners; lean stays (the claim's real-install half is still unmeasured on this box: no torch here).
<!-- THOUGHT:END -->
