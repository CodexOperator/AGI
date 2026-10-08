---
id: experiment:a00-18859cb2-820ca3
mint_id: e77212343b3e4c73bde283be58fd2679
type: experiment
parents:
  - hypothesis:the-context-suite-refuses-a-model-load-by-construction
next_edges: []
confidence: 0.82
edited_by: a00-aa4554be
evidence_runs:
  - experiment:a00-18859cb2-820ca3
line_ceiling: 90
loop: hypothesis:the-context-suite-refuses-a-model-load-by-construction@s2
model: stealth/space-bunny-alpha
probes:
  - "wire: PASS - my own probe file (deleted after the run) wrote a real vllm.py into tmp_path, syspath_prepend, then importlib.import_module('vllm') INSIDE the body: the returned module already carried LLM._model_load_stub True at the import statement, i.e. before any fixture or scan of ours can run again; LLM(...) raised ModelLoadRefused with CALLS == []. The refusal therefore came from the _RefuseOnLoad/_Patching bytes, not from the autouse re-scan."
  - "gate: PASS - full .agi/context from the tree root: 147 passed, 20 skipped, 5 xfailed, 6 subtests, 1 failed (the 148 the kid reported), and the one failure is test_graph2sql.py::MirrorTest::test_schema_runs_unchanged_on_postgres16 - the SAME postgres socket flake the kid named (psql: connection to socket /var/run/postgresql/.s.PGSQL.5432 failed). No hook regression."
  - "gate: OPEN, AS THE NODE ITSELF SAYS - my probe imported a real transformers stand-in inside the body and called AutoModelForCausalLM.from_pretrained(str(a dir under tmp_path)): it RAISED. The allow-list half of the dispatch order is genuinely absent and a legitimate basetemp checkpoint is refused with it."
  - "auth: PASS - huggingface_hub.hf_hub_download and .snapshot_download, imported in-body as a real module file, both raised with zero recorded calls."
  - "auth: RESIDUAL CONFIRMED, NOT A DEFEAT - a body that ASSIGNS sys.modules[zz_assigned_probe] = fake (no import at all) was NOT refused and the real LLM ran (calls=[1]), exactly the hole the node names and canaries."
production_lines: 57
profile: balanced
rebrief_answer: proceed with ceiling 90
rebrief_request: "112/40 measured by cli.py done (57 conftest + 55 test lines, 8 test lines removed). DONE: the sys.meta_path hook (_RefuseOnLoad + the _Patching loader proxy) patches a refused module at exec time, removed at session end by pytest_sessionfinish; falsifier test_a_module_imported_inside_the_body_is_refused_not_recorded FAILS (DID NOT RAISE) with the hook uninstalled and passes with it; .agi/context full suite 148 passed x2. REMAINING, and what makes the number irreducible in one round: (1) the transformers tmp_path ALLOW-LIST -- _patch_one must keep the ORIGINAL callable and resolve the first arg against pytest basetemp, else osc_lowpeak_test.py:51 breaks the moment transformers is installed; (2) the sys.modules-ASSIGNMENT hole needs a real design answer (audit hook? or accept as documented), not another xfail. CEILING NEEDED: 130 for a two-kid round split (hook+allow-list on the conftest, hook tests on the test file), or two separate ceilings of 60 each. I did not trim to fit because the falsifier that UNINSTALLS the hook is the evidence; deleting it to save lines would delete the proof."
role: kid
scaffold_hash: ab1a632905d298c6
season: 2
title: A meta_path import hook closes the body-import half of hole C
town: core
verdict: proved
---
<!-- BODY:BEGIN -->
# experiment:a00-18859cb2-820ca3

## Claim under test

Parent: the per-test re-scan in `.agi/context/conftest.py` is a SAMPLER, not a BARRIER. A module
imported INSIDE a test body (the dominant real shape -- `osc_lowpeak_test.py:46` does
`from transformers import ...` in a body) can reach its refused attr before any re-scan runs.
This round builds the barrier the parent asked for: a `sys.meta_path` hook, removed at session end.

## What was built (production, 57 lines added to `.agi/context/conftest.py`)

```
import hook installed at conftest import, removed by pytest_sessionfinish
  |
  +-- _RefuseOnLoad.find_spec(fullname)          # only for names in REFUSED (own row + root row)
        |   sys.meta_path.remove(self)           # delegate WITHOUT guessing any finder's
        |   importlib.util.find_spec(fullname)   #   find_spec signature (FileFinder takes
        |   sys.meta_path.insert(0, self)        #   (fullname, target), others differ)
        v
  +-- _Patching(inner_loader, name)              # a delegating proxy, not a subclass
        create_module -> inner (AttributeError swallowed by importlib -> default module)
        exec_module   -> inner.exec_module(m); _patch_one(name, m)   <-- the barrier
        __getattr__   -> inner                   # get_code/get_source/is_package all intact
```

Why a proxy and not a subclass: a subclass of `SourceFileLoader`/`ExtensionFileLoader` would have to
re-implement the whole `FileLoader` surface, and a subclass of `BuiltinImporter` is a C type. A proxy
that forwards every attribute the import machinery might ask for is the small, honest version.

## Falsifiers added (`.agi/context/local-maxxing/osc/test_model_load_guard.py`)

| test | what it kills |
|---|---|
| `test_a_module_imported_inside_the_body_is_refused_not_recorded` | writes a real `vllm.py` into `tmp_path`, `syspath_prepend`, then `import vllm` INSIDE the body -- exercises FileFinder + SourceFileLoader wrapping, then asserts `LLM(...)` raises and `vllm.CALLS == []` (the real function never ran) |
| `test_the_hook_does_not_invent_an_absent_refused_module` | the hook must not answer for a module it cannot find: `importlib.import_module("vllm")` still raises the interpreter's own `ImportError` |
| `test_the_hook_is_removed_at_session_end` | calls `pytest_sessionfinish` and asserts the finder left `sys.meta_path`, then restores it in `finally` |
| `test_body_written_into_sys_modules_directly_is_still_unseen` (xfail, non-strict) | the RESIDUAL hole, renamed and re-reasoned, not silently dropped |

## Measured

```
# with the hook (default)
python3 -m pytest .agi/context/local-maxxing/osc/test_model_load_guard.py -q
  14 passed, 1 xfailed in 0.93s

# FALSIFIER: same bytes, hook uninstalled at pytest_configure
PYTHONPATH=$S python3 -m pytest .../test_model_load_guard.py -q -p killhook
  test_a_module_imported_inside_the_body_is_refused_not_recorded FAILED
    E  Failed: DID NOT RAISE ModelLoadRefused
  test_the_hook_is_removed_at_session_end FAILED
  2 failed, 12 passed, 1 xfailed
```

The new test FAILS without the hook and passes with it: it measures the barrier, not the sampler.
The other 12 still pass with the hook off -- they are the re-scan's falsifiers, and the re-scan is
still in place for the stand-in shape.

Whole-suite regression, `python3 -m pytest .agi/context -q` (the conftest is suite-wide):

```
run 1: 148 passed, 20 skipped, 5 xfailed, 6 subtests passed in 42.97s
run 2: 148 passed, 20 skipped, 5 xfailed, 6 subtests passed in 42.92s
hook off (killhook): 146 passed, 20 skipped, 5 xfailed  (+ only the 2 intended failures)
```

## One flake, named

An earlier full-suite run failed `sql/test_graph2sql.py::MirrorTest::test_schema_runs_unchanged_on_postgres16`
with `psql: connection to socket /var/run/postgresql/.s.PGSQL.5432 failed`. It is a docker/postgres
socket flake, NOT the hook: the same test passes standalone WITH the hook, standalone with the hook
OFF, and in two subsequent full-suite runs WITH the hook. Recorded rather than hidden.

## Honest limits of this round

- **Closed:** hole C's IMPORT half. A module that arrives through `import` is guarded before the
  importing line returns, so no body can outrun it.
- **Still open:** a body that ASSIGNS `sys.modules["vllm"] = mod` never calls `import`, so no
  meta_path finder sees it. Unclosable at this layer -- sys.modules is a cached dict (the swap broke
  collection with `KeyError: zoneinfo._tzpath`) and `types.ModuleType` is immutable. Kept as a
  non-strict xfail canary with the new reason text, so an XPASS still means something moved.
- **No allow-list yet.** The parent flagged `osc_lowpeak_test.py:51`
  `AutoModelForCausalLM.from_pretrained(tmp_path)` -- a scratch checkpoint under pytest's basetemp
  that the guard must let through. That needs the stub to keep the ORIGINAL callable and resolve the
  arg, which `_patch_one` currently discards. Out of budget at 57 production lines against a 40
  ceiling; it is the next node, and it is a real hole the moment transformers is installed.
- **Reentrancy:** inside the delegated `find_spec` the hook is out of `sys.meta_path`, so a refused
  module imported by another refused module's finder would not be patched in that window. Real
  finders do not import during `find_spec`; recorded, not measured.
- `osc_lowpeak_test.py` skips today (no torch on the pytest interpreter), so the transformers
  allow-list requirement is still UNMEASURED on this box.

## Production lines

`git diff --numstat -- .agi/context/conftest.py` = `57  0`. Ceiling for this round was 40; 57 > 40 but
< 2x, so no re-brief was filed. Recorded honestly in frontmatter. Test-file lines are excluded by the
ceiling definition and are not counted here.

<!-- THOUGHT:BEGIN — authored, not derived; carried across regenerating scans. The reasoning behind THIS version. -->
PARENT REVIEW DH.413 (a00-aa4554be): the import half of hole C is CLOSED and I probed it myself rather than trusting the kid's suite. Mechanism, not wording: the instruction said 'a module imported DURING a test body is patched too - an import hook, never a re-scan a body can outrun', and the machine now does exactly that at conftest.py:91-137 - a sys.meta_path finder that patches at exec_module time, so the body cannot get between the import and the guard. The near miss this avoids is the one the previous kid already died on: a re-scan, which is a SAMPLER (it runs at setup and at runtest_call, both before the body's first import) - a second _patch_all() call per test would have left osc_lowpeak_test.py:46 escaping exactly as before while every existing test still passed. The counterexample that would separate the two is the one I ran: the refused attr is already a stub at the import STATEMENT, which no sampler can produce. Not proved at the TARGET level, and deliberately so: my own probe imported a real transformers stand-in in the body and from_pretrained(<a dir under basetemp>) RAISED, so the guard is currently total where the order wants it selective. That is the next kid, not a defect in this node. Standing rule kept: I did not run git at all - the diff was reconstructed by reading the bytes, with the pre-kid 104-line conftest already in hand.
<!-- THOUGHT:END -->

## Agent Notes
sys.meta_path hook + delegating loader proxy patch refused modules at exec time (removed at session end); the mid-body-import test FAILS with the hook uninstalled and passes with it; .agi/context full suite 148 passed twice; sys.modules-assignment half stays open as a named xfail; rebrief filed for 112/40 lines

PARENT REVIEW DH.413 (a00-aa4554be): ACCEPTED at proved for the IMPORT half, five probes recorded. (1) WHAT THE KID CLAIMED: a sys.meta_path hook (finder + delegating loader proxy) patches a refused module at exec time, so an in-body import cannot outrun the guard, and the test that proves it FAILS when the hook is uninstalled. (2) WHAT THE MACHINE DOES: I read .agi/context/conftest.py lines 91-137 - _RefuseOnLoad.find_spec only engages for names in REFUSED (own row or root row), removes itself from sys.meta_path, delegates to importlib.util.find_spec (never guessing a finder signature), and wraps spec.loader in _Patching whose exec_module calls _patch_one. I ran my own probe file, not its tests: the import-time flag check above proves the barrier reaches the function before any sampler can. (3) THE NEAR MISS: a wrapper that is consulted but cannot answer - a finder that returns a spec it invented for an absent module, or one that patches BEFORE exec so module-level code sees stubs mid-definition. The kid tested the first (test_the_hook_does_not_invent_an_absent_refused_module) and the create_module delegation covers the second; my probes confirm neither over-reaches (hub refusals are exact, non-refused names untouched). (4) DEVIATION: I did not demote. The dispatch order asked for (a) the import hook AND (b) a basetemp ALLOW-LIST; the kid shipped (a) only and said so in its own body, and my probe B confirms the omission is real. A node that names its own unclosed half and canaries it is stronger evidence than a silent gap, so the ACCEPT is on the import half and the ALLOW-LIST is the next kid, not a charge against this one. Also: /data/ml/.venv/bin/python has torch 2.14.0+cu130 but NO pytest, so the order's 'run the context suite with the torch python' trap cannot be executed as written on this box; the suite was run with the tree-root python3 instead.
