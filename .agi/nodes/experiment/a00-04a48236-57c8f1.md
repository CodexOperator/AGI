---
id: experiment:a00-04a48236-57c8f1
mint_id: 3c20c3c480e6424284cc0ff165687a15
type: experiment
parents:
  - hypothesis:a-no-model-round-refuses-a-model-load-in-every-process-it-spawns
next_edges: []
confidence: 0.8
edited_by: a00-cc3f676b
evidence_runs:
  - experiment:a00-04a48236-57c8f1
line_ceiling: 110
loop: hypothesis:a-no-model-round-refuses-a-model-load-in-every-process-it-spawns@s2
model: stealth/space-bunny-alpha
production_lines: 107
profile: balanced
rebrief_answer: proceed with ceiling 110
rebrief_request: "\"slice COMPLETE and green (9 new passed; dispatch suite 247 passed 1 pre-existing env failure; kid-1 fence suite 26 passed 1 xfailed). 107 production lines added: 86 dispatch.py (flag + opt-in resolver + env builder + 2 call sites + dry-run mirror, ~40 of them help text/docstrings), 21 sitecustomize.py (loud fail-open). Ceiling needed: 110.\""
role: kid
scaffold_hash: 68481b93d632c9c6
season: 2
title: "dispatch puts a no-model round in the inherited fence: both env cells, live"
town: core
verdict: proved
---
# experiment:a00-04a48236-57c8f1

## What I built (kid-2 slice: dispatch wiring + a LOUD fail-open)

| piece | path | role |
|---|---|---|
| the flag | `extensions/agi/bin/dispatch.py` `--no-model` (store_true) | per-invocation opt-in; the config default is `spawn.no_model` (bool, absent = unfenced) |
| the env builder | `dispatch.apply_model_fence_env(env, cfg, enabled, cap)` | writes BOTH cells into the env a child is spawned with **and** into `os.environ` |
| the opt-in resolver | `dispatch.model_fence_requested(cfg, flag)` | flag wins; else `spawn.no_model` |
| the cap | `--model-fence-max-bytes N` | `AGI_MODEL_FENCE_MAX_BYTES` written **only** when the override is passed |
| the loud fail-open | `extensions/agi/fence/sitecustomize.py` | stderr marker + `AGI_MODEL_FENCE_STATUS` (residual C) |
| the falsifiers | `extensions/agi/tests/test_dispatch_model_fence.py` (9 tests) | f1/f4/f5 + the live-wiring proof |

**Why both cells, and why `os.environ`.** The parent's PASS-F probe showed a
one-cell round is silently unfenced, so `PYTHONPATH += <paths.core.model_fence_dir>`
AND `AGI_MODEL_FENCE_SRC = <paths.core.model_fence_src>` are always written
together. They go into `os.environ` of the dispatcher as well as into `spawn_env`,
so a NESTED dispatch (which reads `scrubbed_env()`) is fenced too — the cells are
inheritable, never per-child argv.

## Commands and results

```
$ python3 -m pytest extensions/agi/tests/test_dispatch_model_fence.py -q
9 passed in 0.86s

$ python3 -m pytest extensions/agi/tests/test_dispatch.py \
    extensions/agi/tests/test_dispatch_dry_run.py \
    extensions/agi/tests/test_dispatch_model_allowlist.py \
    extensions/agi/tests/test_dispatch_forward_env.py \
    extensions/agi/tests/test_dispatch_alarms.py \
    extensions/agi/tests/test_dispatch_no_stdout_secrets.py \
    extensions/agi/tests/test_dispatch_render_thread.py \
    extensions/agi/tests/test_dispatch_restart_render.py \
    extensions/agi/tests/test_dispatch_scaffold_unregistered.py \
    extensions/agi/tests/test_dispatch_transient_respawn.py \
    extensions/agi/tests/test_dispatch_model_fence.py -q
247 passed, 1 failed in 20.48s        # FALSIFIER 5: no regression

  the ONE failure is PRE-EXISTING and environmental, not mine:
  test_dispatch_forward_env.py::test_listed_name_reaches_the_child_...
  asserts "TYPESAFE_KEY" not in os.environ -- this box's shell HAS
  TYPESAFE_KEY exported (`env | grep -c TYPESAFE` -> 2), so the test's own
  premise is false here. It fails the same way in isolation and touches no
  dispatch.py code path (it calls adapters.child_env with base={}).

$ PYTHONPATH=<paths.local_maxxing.osc_test_pythonpath> python3 -m pytest \
    .agi/context/local-maxxing/osc/test_model_fence_env.py \
    .agi/context/local-maxxing/osc/test_model_load_guard.py \
    .agi/context/local-maxxing/osc/test_model_load_allowlist.py -q
26 passed, 1 xfailed in 1.10s        # kid-1's falsifiers 1-3 UNCHANGED
```

## Evidence — the flag REACHES the real env (the classic near miss, closed)

Every live-wiring test runs dispatch's REAL live spawn path with `subprocess.Popen`
captured and reads the env object handed to the child (the `GIT_CONFIG_VALUE_0`
capture seam the existing `test_dispatch_dry_run.py` uses). Nothing is launched.

| test | what it proves |
|---|---|
| `test_live_spawn_env_carries_both_fence_cells` | `--no-model` -> `AGI_MODEL_FENCE_SRC == <repo>/extensions/agi/model_fence.py` (file exists) and `PYTHONPATH[-1] == <repo>/extensions/agi/fence` (sitecustomize exists); no cap cell |
| `test_a_process_with_the_captured_env_refuses_the_standin_loader` | that env, in a fresh non-pytest interpreter + a STAND-IN `transformers.models.llama.AutoModelForCausalLM.from_pretrained` (the TMM.228 shape) -> `REFUSED-ModelLoadRefused-CALLS=0`, `STATUS=installed` |
| `test_a_cap_override_is_the_only_thing_that_writes_the_cap` | `--model-fence-max-bytes 1234` -> `AGI_MODEL_FENCE_MAX_BYTES=1234`; absent without the flag |
| `test_without_the_flag_the_round_is_unfenced` | CONTROL: no flag -> neither cell (the fence is not vacuous) |
| `test_the_config_default_fences_without_the_flag` | `spawn.no_model: true` -> both cells, no flag |
| `test_the_fence_cells_are_inheritable_from_the_dispatcher_itself` | `os.environ` carries them after the spawn (a nested dispatch inherits) |
| `test_the_dry_run_shows_both_cells` | `dispatch --dry-run --no-model` prints `model fence: dir=... src=... max_bytes=-` |
| `test_fail_open_is_loud_and_assertable` | residual C fixed: unresolvable table -> still `NOT-REFUSED` (fails open, does not break python, rc 0) but stderr carries `AGI-MODEL-FENCE: NOT INSTALLED -- ...` and the child reports `STATUS=unresolved: ...` |
| `test_falsifier_4_the_minus_S_bypass_is_real_and_named` | the residual below, MEASURED, so it cannot quietly become a claim of closure |

## Falsifier 4 — NAMED RESIDUAL (not closed)

`python -S` (and `python -I`) skips `site`, so `sitecustomize.py` never runs and
the NAME fence does not apply. The exact command that escapes, under a fully
fenced env (fence dir on `PYTHONPATH`, `AGI_MODEL_FENCE_SRC` set):

```
python3 -S -c "import transformers.models.llama as L; L.AutoModelForCausalLM.from_pretrained('osc03')"
# -> NOT-REFUSED, and NO stderr marker
```

The second layer is **not** name-based: `mem_cap.wrap_argv` (`extensions/agi/bin/mem_cap.py`,
config cell `spawn.memory_max`) bounds the round by cgroup/`RLIMIT_AS`, which every
descendant inherits, so the escaping process is still capped -- it is simply not
REFUSED BY NAME. No argv-level fix reaches a grandchild's own `python -S`, so this
is stated, not papered over. `test_falsifier_4_the_minus_S_bypass_is_real_and_named`
asserts the escape still happens; if it ever stops, that test fails and the node
must be rewritten as CLOSED.

## Config cells this slice needs (a round cannot commit `.agi/config.json`)

| cell | value | who reads it |
|---|---|---|
| `paths.core.model_fence_dir` | `extensions/agi/fence` | `dispatch._fence_cell` (default = same literal) |
| `paths.core.model_fence_src` | `extensions/agi/model_fence.py` | `dispatch._fence_cell` (default = same literal) |
| `spawn.no_model` | `false` (or `true` per post) | `dispatch.model_fence_requested` — the per-invocation default behind `--no-model` |

Both path cells are read through `_fence_cell` with the shipped literals as
defaults, so nothing breaks before the director commits them; `paths.py audit`
stops reporting the two literals only once they exist as cells.

## Line ceiling

Measured with the one allowed `git diff --numstat` read over the production paths
(tests excluded): `86 added / 1 deleted` in `dispatch.py`, `21 added / 5 deleted`
in `fence/sitecustomize.py` = **107 added**. Over the 2x=80 line, so the request is
recorded rather than assumed (see the frontmatter `rebrief_request`). Roughly 40 of
the dispatch lines are the two `--help` strings and the docstrings the engine
convention requires; the executable core is ~45. `re-brief_request` names what is
done so the parent only has to answer with a ceiling.

## Agent Notes
dispatch --no-model (default spawn.no_model) writes BOTH fence cells into the env a real spawn hands the child AND into the dispatcher's own env; a process with that env refuses the stand-in TMM.228 loader (CALLS=0, STATUS=installed); the unresolvable-table fail-open is now LOUD (stderr marker + AGI_MODEL_FENCE_STATUS); falsifier 4 CLOSED-BY-NAMING: python -S escapes, exact command in the body, mem_cap is the non-name second layer; falsifier 5: 247 passed, 1 pre-existing env-dependent failure. Config cells: paths.core.model_fence_dir, paths.core.model_fence_src, spawn.no_model

PARENT REVIEW (a00-cc3f676b, DH.415). Read the BYTES, not the report: dispatch.py:1103-1150 (the two defaults, model_fence_requested, apply_model_fence_env), 1472-1474 and 2756-2759 (the two call sites, one in the dry-run/env path and one in the live spawn_env path), 1510-1518 (dry-run report), 1663-1676 (--no-model / --model-fence-max-bytes), fence/sitecustomize.py (the _fail_open marker + AGI_MODEL_FENCE_STATUS), extensions/agi/tests/test_dispatch_model_fence.py (9 tests). Every deliverable the node names is in the tree. Its suite is its CLAIM; these are MY probes, run in fresh interpreters, stand-in transformers only (the TMM.228 shape, nothing real imported or downloaded):
probes: WIRE the real builder (apply_model_fence_env, enabled via the config default, no flag) produces AGI_MODEL_FENCE_SRC=<repo>/extensions/agi/model_fence.py and PYTHONPATH[-1]=<repo>/extensions/agi/fence, and BOTH resolved paths exist on disk. A child launched with that env refuses transformers.models.llama.AutoModelForCausalLM.from_pretrained("osc03") -> REFUSED ModelLoadRefused, STATUS=installed. The flag reaches the function; the env is the mechanism, not a string in the source.
probes: GATE a grandchild (python spawning python) with that same env is ALSO refused (STATUS=installed). Inheritance holds across two hops.
probes: AUTH the round the claim never authorises -- model_fence_requested({}, False) is False, apply_model_fence_env writes NO cells, and in a CLEAN process the stand-in load RUNS (NOT-REFUSED). The fence is not vacuous and the opt-in is honest. My first attempt at this probe printed REFUSED and I nearly recorded a defect: the builder also writes os.environ, so my own earlier probe had fenced MY probe process. That is a real property, not a kid bug -- see caveats.
probes: GATE the unresolvable-table case (residual C from kid 1) is now LOUD and assertable: the load still runs, rc 0, but stderr carries "AGI-MODEL-FENCE: NOT INSTALLED -- no model_fence table..." and the child reports STATUS=unresolved:... The silent fail-closed-to-prose path is closed. Accepted.
probes: GATE falsifier 4, measured by me: python -S -c <the exact TMM.228 call> under a fully fenced env -> NOT-REFUSED, no marker. That is the residual the node names verbatim, with mem_cap as the non-name second layer. A NAMED residual is an accepted falsifier-4 pass; the node even ships a test that asserts the escape still happens so it cannot silently become a claim of closure.
probes: FALSIFIER 5, checked adversarially because "pre-existing, environmental" is the easiest thing in the world to claim: extensions/agi/tests/test_dispatch_forward_env.py FAILS 1/9 in this shell, and PASSES 9/9 under `env -u TYPESAFE_KEY -u TYPESAFE_API_KEY`. The failure is this box exporting TYPESAFE_KEY, not the diff. Falsifier 5 holds.
RESIDUAL, NAMED (not a demotion): the ONE-CELL near miss is still silent -- AGI_MODEL_FENCE_SRC set but the fence dir absent from PYTHONPATH means sitecustomize never runs, so nothing can warn (I measured it). The builder always writes both cells together, so a dispatch is safe; the only way to reach that state is to hand-write the env. A cheap future guard: a test asserting both cells are present whenever either is.
VERDICT: ACCEPTED as proved for the kid-2 slice (dispatch wiring + live proof + loud fail-open + falsifier 4 named + falsifier 5 clean). Title is real, not derived.

<!-- THOUGHT:BEGIN — authored, not derived; carried across regenerating scans. The reasoning behind THIS version. -->
PARENT REVIEW, DH.415 (a00-cc3f676b) -- this THOUGHT is the parent reasoning about the version, rewritten from scratch.
(1) WHAT THE BRIEF SAID, quoted: "set BOTH fence cells ... They must be INHERITABLE: set it in the env the PARENT process exports, never per-child argv"; and "make the fence fail-open LOUD"; and "Falsifier 4: the python -I / -S bypass. Either CLOSE it ... or NAME the residual explicitly".
(2) WHAT THE MACHINE ACTUALLY DOES: dispatch.apply_model_fence_env (dispatch.py:1125-1150) writes PYTHONPATH=.../extensions/agi/fence and AGI_MODEL_FENCE_SRC=.../model_fence.py into the child env AND into os.environ (line 1145 loop), called at dispatch.py:1472 (env path) and 2756 (live spawn_env). I built the env with the real function in a fresh process, checked both files exist, and a child in that env refused the stand-in loader with STATUS=installed; its grandchild too. An unauthorised round (no flag, no spawn.no_model) writes no cells and the load runs -- the opt-in is real. The unresolvable-table case now prints AGI-MODEL-FENCE: NOT INSTALLED and exports AGI_MODEL_FENCE_STATUS=unresolved, so a misfenced round is loud instead of silent. python -S escapes, exactly as the node says.
(3) THE NEAR MISS, and the one that actually cost me a probe: a builder that writes the two cells into the child env but NOT into os.environ looks identical in the dry-run print and passes a "both cells present" test, and loses inheritance -- the nested dispatch and every grandchild the kid spawns read scrubbed_env() and are unfenced. The plausible sibling that also looks right and loses: writing os.environ makes the fence STICKY and fail-CLOSED for the life of the dispatcher, so one --no-model round leaves every later round in that process fenced. I hit this as a contaminated probe of my own and nearly recorded it as a defect in the kid; it is the design, and its direction is safe, but it is unbounded and should be named. The other near miss: a test that greps dispatch.py for the string "AGI_MODEL_FENCE_SRC" and calls that proof -- a flag that never reaches the function satisfies it. This node avoids it by capturing the env object a real Popen receives.
(4) NO DEVIATION from a standing rule. The rule I could have bent is "never run git": the kid measured its own lines with one `git diff --numstat` read, a read and not a write, and disclosed the number rather than hiding it -- that is the rule working, not bending. I ran no git at all and verified its line claim is not load-bearing for the verdict.
RESIDUALS CARRIED UP: (a) the one-cell silent near miss; (b) the sticky fail-closed dispatcher; (c) python -S/-I escapes by NAME, bounded only by mem_cap; (d) three config cells a round cannot commit -- paths.core.model_fence_dir, paths.core.model_fence_src, spawn.no_model -- which the DIRECTOR must commit, otherwise the two paths stay literals and paths.py audit keeps reporting them.
<!-- THOUGHT:END -->
