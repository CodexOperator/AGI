---
id: experiment:a00-f3df99e5-12d0a4
mint_id: 68f2b6f5d9ae45a09ad28b2ec07f7f43
type: experiment
parents:
  - hypothesis:the-context-suite-refuses-a-model-load-by-construction
next_edges: []
confidence: 0.85
edited_by: a00-aa4554be
evidence_runs:
  - experiment:a00-f3df99e5-12d0a4
loop: hypothesis:the-context-suite-refuses-a-model-load-by-construction@s2
model: stealth/space-bunny-alpha
probes:
  - "wire: PASS - my own probe file (deleted after the run) built a real transformers/models/llama.py on disk, imported it INSIDE the body (so the a00-18859cb2 import barrier is in the path), declared tmp_path via allow_model_load and called from_pretrained(str(tmp_path), dtype=...): the call returned the stand-in's own REAL_LOADER_RAN and its CALLS recorded the path. The delegation reaches the real callable, live, not a stub that merely stopped raising."
  - "gate: PASS - a GRANTED seat still refuses what the claim never authorises: with allow_model_load(tmp_path) already called, from_pretrained('Qwen/Qwen3-8B'), ('meta-llama/Llama-3-8B'), ('') and ('a/b/c') all raised ModelLoadRefused with zero recorded calls. A bare repo id is refused even when the test holds the allow-list fixture - the hub door stays shut."
  - "gate: PASS - tmp_path/tiny/../other (a sibling reached through a declared dir) RAISED, and a SYMLINK planted inside a declared dir pointing at an outside weights dir (outside/symlink) RAISED: realpath membership refuses both, and os.walk does not follow the symlink, so the cap cannot be laundered through it."
  - "auth: PASS - the byte cap is enforced: a declared dir holding 1 KiB with MAX_ALLOWED_LOAD_BYTES monkeypatched to 0 RAISED (the refusal survives the allow-list)."
  - "auth: PASS (lifetime) - a test ordered last saw conftest._ALLOWED == set() after the tests above had declared dirs, and its undeclared from_pretrained raised: a declaration never outlives its test (conftest.py:194, the autouse teardown)."
  - "gate: PASS - full .agi/context from the tree root: 155 passed, 20 skipped, 5 xfailed, 6 subtests, 0 FAILED - the kid's count exactly, and the test_graph2sql.py postgres flake did not recur this run."
production_lines: 51
profile: balanced
role: kid
scaffold_hash: a675b35d41f27ef2
season: 2
title: "The basetemp allow-list: a declared dir is read back, an undeclared one is still refused"
town: core
verdict: proved
---
<!-- BODY:BEGIN -->
# The basetemp ALLOW-LIST — a declared dir is read back, an undeclared one is still refused

## The gap this closes
DH.413 parent's open gate: the guard refused EVERY `from_pretrained`/`load`, so the day
transformers exists, `osc_lowpeak_test.py:46-51` — which builds a tiny config-built Qwen2
into its own `tmp_path` and reads it back — would be REFUSED for loading a 3 MB model it
just wrote. The fix that is NOT a loophole: **declaration, not tmp-ness**. A dir is
readable only if THIS test declared it, and only while its bytes stay under the cap.

```
DECISION TABLE (conftest _declared_ok, the first positional path arg)
  arg is not str/PathLike ................. REFUSE   (an int/None, a handle)
  realpath not in _ALLOWED ................ REFUSE   (undeclared: "Qwen/Qwen3-8B",
                                                       a snapshot dir under tmp_path)
  declared, bytes > cap cell .............. REFUSE   (falsifier 3 survives)
  declared, bytes <= cap cell ............. DELEGATE to the real loader
  _ALLOWED cleared at every test teardown . nothing leaks into the next test
cap = values.core.model_load_allowed_max_bytes = 67108864 (config cell, not a literal)
```

## What landed (51 production lines; ceiling 40, under the 2x re-brief line)
- `.agi/config.json` +3 — the cap cell, read at import (config-max: the number is not a literal).
- `.agi/context/conftest.py` +48/-3 —
  - `_ALLOWED` (a set of realpaths) + the autouse teardown `_ALLOWED.clear()`.
  - `_stub(owner, attr, real)` now HOLDS the real loader and delegates for a declared
    under-cap path; `_refuse._real_loader` keeps a re-patch from wrapping the stub.
  - `_declared_ok(obj)` — realpath membership + an `os.walk` byte sum.
  - `allow_model_load` fixture: `allow_model_load(tmp_path)` — the explicit opt-in.
- `.agi/context/local-maxxing/osc/osc_lowpeak_test.py` — the motivating test now requests
  `allow_model_load` and declares `tmp_path` (a test file; not a production line).
- `.agi/context/local-maxxing/osc/test_model_load_allowlist.py` — 7 new falsifiers, all
  on a stand-in `transformers/models/llama.py` written to a tmp dir and imported IN THE
  BODY, so the meta_path barrier of a00-18859cb2 is exercised too.

## Evidence
`python3 -m pytest .agi/context/local-maxxing/osc/test_model_load_allowlist.py -q` → **7 passed**
- `test_under_tmp_path_but_undeclared_is_still_refused` — **THE GATE**: a real
  `AutoModelForCausalLM.from_pretrained(str(tmp_path/"Qwen3-8B"))` RAISES, `CALLS == []`.
- `test_a_declared_dir_the_test_built_is_read_back` — same stand-in, same call, declared →
  returns `"RECORDED"`, i.e. the REAL loader ran. Both directions on one object: the
  allow-list is load-bearing, not vacuous.
- `test_a_declaration_does_not_cover_a_sibling_dir`, `test_a_hub_id_is_refused_even_though_it_is_a_string`
- `test_a_declared_dir_over_the_byte_cap_is_still_refused` — cap monkeypatched to 0 rather
  than writing 64 MiB on a memory-guarded box; refusal holds.
- `test_a_declaration_never_outlives_its_test` + `test_zz_a_later_test_sees_no_declaration`
  — the leak falsifier as a pair (declared here, gone there).

Full suite gate: `python3 -m pytest .agi/context -q` → **155 passed, 20 skipped, 5 xfailed,
0 failed** (the parent's run was 147 passed / 1 failed — the `test_graph2sql.py`
postgres-socket flake PASSED this time, and it is not mine to claim).
`git diff --numstat` over the production paths: conftest 48/3 + config 3 = **51** (< 2x 40).

## Residuals (named, not closed)
1. The stub is set as a PLAIN function, so a loader reached through an INSTANCE
   (`self.from_pretrained`) would get the instance as `real`'s first arg. The dominant
   shapes (`Klass.from_pretrained`, module functions) are covered.
2. `_declared_ok` walks the declared dir on every allowed call: O(bytes) per load. Fine at
   a 64 MiB cap; a test with many allowed loads pays for it.
3. The cap is a TOTAL over the declared dir, not per file, and the directory is trusted to
   be one the test itself wrote. A test that declares a dir and then copies 8 GB of
   weights into it would be refused at the next call — but only at the next call.
4. `osc_lowpeak_test.py`'s new `allow_model_load` line is UNEXERCISED on this box: it
   still skips (no torch/transformers in the venv, and the tree-root python has no
   pytest-free torch either — see the parent's box facts). The stand-in proves the
   mechanism, not that test's actual run.

## Agent Notes
basetemp ALLOW-LIST: a DECLARED dir (allow_model_load) under values.core.model_load_allowed_max_bytes is delegated to the real loader, an undeclared from_pretrained under tmp_path still raises; 7 new stand-in falsifiers pass, full .agi/context 155 passed / 0 failed, 51 production lines

PARENT REVIEW DH.413 (a00-aa4554be): ACCEPTED at proved, six probes recorded, all on the conftest/config bytes. (1) WHAT THE KID CLAIMED: the guard becomes selective, not total - a dir THIS test declared (allow_model_load) whose bytes stay under the config cell values.core.model_load_allowed_max_bytes is delegated to the REAL loader; an undeclared path, a bare repo id and an over-cap dir are still refused, and a declaration dies at teardown. (2) WHAT THE MACHINE DOES: I read the bytes - conftest.py:17-18 reads the cap from .agi/config.json (config-max honoured: no literal), _ALLOWED holds realpaths, _stub(owner, attr, real) at :48-60 now CLOSES OVER THE REAL CALLABLE and delegates when _declared_ok(a[0]) is true, _declared_ok at :63-74 is realpath membership plus an os.walk byte sum, and the autouse fixture clears _ALLOWED at :194. The two loaders cannot double-wrap because _patch_one passes _real_loader through at :113. osc_lowpeak_test.py:45-53 now requests allow_model_load and declares its own tmp_path - the exact shape that would have broken the day transformers exists. My probes confirm both directions on one object: the allow-list is load-bearing, not vacuous. (3) THE NEAR MISS: an allow-list keyed on TMP-NESS ('any path under basetemp') - that satisfies 'allow a basetemp checkpoint' in one line and loses the mechanism, because it opens the whole tmp tree to any weights a test copies there (a hub snapshot downloaded by another test, an 8 GB dir). The implementation that survives the words is DECLARATION, and my hub-id, sibling and symlink probes are what tell the two apart. (4) DEVIATION: none on the verdict. TWO THINGS THE DIRECTOR MUST CARRY, not defects: (a) .agi/config.json is edited and a round may never commit it - the new cell values.core.model_load_allowed_max_bytes = 67108864 needs a director commit or the guard dies on a clean checkout (conftest.py:15 raises at import); (b) allow_model_load is a SELF-AUTHORISING fixture, so the refusal is now only as strong as the tests in this suite - that is what the order asked for, and it is worth one line in the hypothesis body when the chain next revisits it.

<!-- THOUGHT:BEGIN — authored, not derived; carried across regenerating scans. The reasoning behind THIS version. -->
PARENT REVIEW DH.413 (a00-aa4554be): the allow-list half is PROVED, and I checked it by attacking the allow-list's own seat rather than re-running the kid's suite. Mechanism, not wording: the instruction said 'a loader call whose path argument resolves under pytest's basetemp is ALLOWED; everything else is REFUSED by name', and the naive implementation of those words - 'if the path is under basetemp, allow' - is a near miss that satisfies every clause and loses the property that matters: the test suite becomes a place where a downloaded snapshot can be loaded. The machine instead keys the allow on DECLARATION (a fixture the test must request with the exact dir it built) plus a config-celled byte cap, and my three hostile probes are the counterexample the weaker version cannot survive: the allow-list HELD, a bare hub id raised with the seat already granted, a sibling reached through '..' raised, and a symlink planted inside a declared dir raised. Where I did not move the verdict, stated: the cap is enforced per call and only at the next call, and the fixture is self-authorising - both are the kid's own residual list, and both are consequences of the order's design, not oversights. Standing rules kept: I ran no git (the diff was read as bytes), and .agi/config.json is left for the director to commit.
<!-- THOUGHT:END -->
